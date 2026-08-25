"""Télécharge et optimise les reproductions OUVERTES retenues (Wikimedia Commons),
puis enrichit les fiches d'œuvres pour l'onglet « Œuvres ».

N'intègre QUE les correspondances retenables : match_status == exact ET
rights_status == open (cf. src/commons_match.py). On ne hotlinke jamais Commons :
on télécharge une miniature (API Commons `iiurlwidth`), on la ré-encode en JPEG
optimisé, une seule copie locale par référence, dans data/exports/web/oeuvres_img/.
Le crédit et la licence exacts sont conservés et affichés sous l'image.

Produit :
  - data/exports/web/oeuvres_img/<reference>.jpg  (vignettes versionnées) ;
  - data/exports/web/images_index.json            (référence -> métadonnées image) ;
  - fusion de `image` dans data/exports/web/oeuvres/<slug>.json (front).

Cache des miniatures Commons : data/cache/commons_thumbs.json.

REPRISE (2026-08-24). Une vignette déjà écrite n'est retéléchargée que si elle
ne peut plus être réutilisée. « Réutilisable » veut dire trois choses à la fois,
et la présence du fichier n'en est qu'une (voir `fichier_reutilisable`) :
le fichier s'ouvre et se décode entièrement, l'index précédent atteste qu'il
vient bien de la source qu'on veut lui donner, et il a été produit avec le
profil d'encodage demandé. Sans ces trois conditions, on retélécharge.

Usage : uv run python src/build_vignettes.py
"""

import glob
import io
import json
import os
import sys
import time
import urllib.parse
import urllib.request
from datetime import date
from pathlib import Path

from PIL import Image

from config import DOSSIER_EXPORTS, RACINE

CORRESP = DOSSIER_EXPORTS / "commons_correspondances.json"
CORRESP_GALLICA = DOSSIER_EXPORTS / "gallica_correspondances.json"
CORRESP_IMAGERIE = DOSSIER_EXPORTS / "imagerie_commons_correspondances.json"
# Registre d'audit des images POP (build_images.py). LECTURE SEULE : ce chantier
# n'y écrit jamais, il en recopie le statut, le crédit et la date de contrôle.
REGISTRE_POP = DOSSIER_EXPORTS / "images_oeuvres.json"
DOSSIER_OEUVRES = DOSSIER_EXPORTS / "web" / "oeuvres"
DOSSIER_IMG = DOSSIER_EXPORTS / "web" / "oeuvres_img"
INDEX = DOSSIER_EXPORTS / "web" / "images_index.json"
DOSSIER_CACHE = RACINE / "data" / "cache"
CACHE_THUMBS = DOSSIER_CACHE / "commons_thumbs.json"

# L'index tel qu'il était avant ce build : sert à ne pas réécrire les dates de
# contrôle visuel (voir date_de_controle).
_INDEX_PRECEDENT: dict = {}

COMMONS_API = "https://commons.wikimedia.org/w/api.php"
UA = "inventaire-du-doute/1.0 (projet data-journalisme ; contact hericlibong@gmail.com)"
# Paramètres des reproductions OUVERTES (Commons, Gallica). Ils ne bougent pas :
# les 209 vignettes déjà produites avec eux ne doivent jamais être ré-encodées.
LARGEUR = 900        # largeur maximale de la vignette (px)
QUALITE = 82         # qualité JPEG
PAUSE = 1.0          # Wikimedia limite le rendu des miniatures (HTTP 429)

# Paramètres POP, SÉPARÉS des précédents (plan du chantier, §3.1). Les changer ne
# régénère que les vignettes POP : les vignettes ouvertes n'en dépendent pas.
# Profil D, arrêté le 2026-08-25 après la sonde de l'étape 2 : il garde les
# 800 px du profil B — la définition qui compte dans la lightbox — et descend la
# qualité à 75. Sur les images les plus détaillées, les recadrages à 100 % n'ont
# montré aucune différence perceptible avec la qualité 78, pour 6,6 % de poids en
# moins. Mesuré : 77,8 Ko de moyenne, soit environ 404 Mo pour les 5 326 images.
LARGEUR_POP = 800
QUALITE_POP = 75
PAUSE_POP = 0.2      # POP sert des fichiers statiques : pas de limite de rythme

# Identifiant de profil inscrit dans l'index, pour les seules entrées POP. Les
# entrées Commons et Gallica n'en portent pas : leur profil est celui du script,
# et `None` les décrit exactement. C'est ce qui fait qu'un changement de profil
# POP ne les concerne pas.
PROFIL_POP = f"pop-{LARGEUR_POP}-{QUALITE_POP}"


def _get(url: str) -> bytes:
    # Backoff sur 429 (« too many requests ») et erreurs transitoires : Wikimedia
    # borne le rythme du rendu des miniatures.
    # Certaines URLs d'images POP contiennent des espaces, des parenthèses ou
    # des caractères Unicode dans leur chemin. `urllib` refuse ces URLs brutes
    # avant même d'envoyer la requête. On encode uniquement le chemin, la requête
    # et le fragment, en préservant les séquences `%xx` déjà présentes et les
    # séparateurs propres à chaque partie de l'URL.
    parties = urllib.parse.urlsplit(url)
    url_requete = urllib.parse.urlunsplit((
        parties.scheme,
        parties.netloc,
        urllib.parse.quote(parties.path, safe="/%:@"),
        urllib.parse.quote(parties.query, safe="=&%:@/?+;,"),
        urllib.parse.quote(parties.fragment, safe="%:@/?+"),
    ))
    req = urllib.request.Request(url_requete, headers={"User-Agent": UA})
    for essai in range(5):
        try:
            with urllib.request.urlopen(req, timeout=90) as r:
                return r.read()
        except urllib.error.HTTPError as ex:
            if ex.code == 429 and essai < 4:
                time.sleep(5 * (essai + 1))
                continue
            raise
        except Exception:
            if essai < 4:
                time.sleep(3 * (essai + 1))
                continue
            raise
    raise RuntimeError("échec après plusieurs tentatives")


def _cache(chemin) -> dict:
    return json.load(open(chemin, encoding="utf-8")) if chemin.exists() else {}


def _sauver(chemin, obj) -> None:
    DOSSIER_CACHE.mkdir(parents=True, exist_ok=True)
    chemin.write_text(json.dumps(obj, ensure_ascii=False), encoding="utf-8")


def urls_miniatures(fichiers: list) -> dict:
    """nom_fichier Commons -> URL de miniature (largeur bornée), par l'API."""
    cache = _cache(CACHE_THUMBS)
    a_faire = [f for f in fichiers if f not in cache]
    if a_faire:
        print(f"  {len(a_faire)} miniatures à résoudre (API Commons)…")
        for i in range(0, len(a_faire), 50):
            lot = a_faire[i:i + 50]
            params = {"action": "query", "prop": "imageinfo", "iiprop": "url",
                      "iiurlwidth": str(LARGEUR), "format": "json",
                      "titles": "|".join("File:" + f for f in lot)}
            data = json.loads(_get(COMMONS_API + "?" + urllib.parse.urlencode(params)))
            for page in data.get("query", {}).get("pages", {}).values():
                titre = page.get("title", "")
                nom = titre[5:] if titre.startswith("File:") else titre
                ii = (page.get("imageinfo") or [{}])[0]
                cache[nom] = ii.get("thumburl") or ii.get("url", "")
            _sauver(CACHE_THUMBS, cache)
            time.sleep(PAUSE)
    return cache


def jpeg_valide(chemin) -> bool:
    """Le fichier s'ouvre ET se décode entièrement.

    `verify()` ne suffit pas : il contrôle l'en-tête, pas les données. Un JPEG
    coupé en cours d'écriture garde un en-tête valide et ne se révèle qu'au
    décodage. On décode donc pour de bon, et on laisse `LOAD_TRUNCATED_IMAGES`
    à sa valeur par défaut — sans quoi Pillow compléterait silencieusement
    l'image tronquée au lieu de la refuser.
    """
    try:
        with Image.open(chemin) as im:
            im.load()
        return True
    except Exception:
        return False


def fichier_reutilisable(ref: str, source_voulue: str, profil_voulu=None) -> bool:
    """La vignette déjà sur le disque peut-elle servir telle quelle ?

    Trois conditions, et la présence du fichier n'en est qu'une. Le piège que
    ce contrôle ferme : les vignettes portent toutes le nom `<reference>.jpg`,
    sans marque de provenance. Si une référence change de source — c'est prévu
    pour les estampes qui passeront de Commons à POP — le fichier existant
    resterait en place et l'index lui donnerait pourtant le crédit et le lien de
    la NOUVELLE source. Une fausse attribution, exactement ce que le crédit est
    censé empêcher.

    L'état de référence est l'index précédent (`images_index.json`, versionné) :
    lui seul dit de quelle source vient chaque fichier. Aucun second registre
    n'est tenu à côté, qui pourrait diverger de celui-là.

    `profil_voulu` vaut None pour Commons et Gallica : leurs entrées n'en
    portent pas, et `None == None` les déclare à jour. Changer le profil POP ne
    peut donc pas les atteindre.
    """
    sortie = DOSSIER_IMG / f"{ref}.jpg"
    if not sortie.exists():
        return False
    precedent = _INDEX_PRECEDENT.get(ref)
    if precedent is None:
        # Fichier orphelin : rien n'atteste d'où il vient. On refait plutôt que
        # de lui prêter une provenance qu'on ne peut pas vérifier.
        print(f"    ↻ {ref} : origine non attestée par l'index — régénérée")
        return False
    if precedent.get("source_type") != source_voulue:
        print(f"    ↻ {ref} : {precedent.get('source_type')} → {source_voulue}")
        return False
    if precedent.get("profil") != profil_voulu:
        print(f"    ↻ {ref} : profil {precedent.get('profil')} → {profil_voulu}")
        return False
    if not jpeg_valide(sortie):
        print(f"    ↻ {ref} : fichier illisible ou tronqué — régénérée")
        return False
    return True


def nettoyer_temporaires() -> int:
    """Retire les `.jpg.tmp` laissés par une exécution interrompue."""
    restes = list(DOSSIER_IMG.glob("*.jpg.tmp")) if DOSSIER_IMG.exists() else []
    for reste in restes:
        reste.unlink(missing_ok=True)
    if restes:
        print(f"{len(restes)} fichier(s) temporaire(s) d'une exécution interrompue retiré(s).")
    return len(restes)


def optimiser(donnees: bytes, chemin_sortie, largeur: int = LARGEUR,
              qualite: int = QUALITE) -> None:
    """Ouvre l'image téléchargée, aplatit la transparence sur blanc, borne la
    largeur, ré-encode en JPEG optimisé (métadonnées retirées).

    L'écriture est ATOMIQUE (2026-08-24) : le JPEG est produit à côté, relu pour
    vérifier qu'il se décode, et seulement alors mis en place par `os.replace`.
    Une interruption, un disque plein ou une image source corrompue ne peuvent
    donc plus laisser une vignette à moitié écrite — que la reprise prendrait
    pour un fichier valide et ne referait jamais. En cas d'échec, le fichier
    précédent reste intact.
    """
    temporaire = chemin_sortie.parent / (chemin_sortie.name + ".tmp")
    try:
        im = Image.open(io.BytesIO(donnees))
        if im.mode in ("RGBA", "LA", "P"):
            im = im.convert("RGBA")
            fond = Image.new("RGB", im.size, (255, 255, 255))
            fond.paste(im, mask=im.split()[-1])
            im = fond
        else:
            im = im.convert("RGB")
        if im.width > largeur:
            h = round(im.height * largeur / im.width)
            im = im.resize((largeur, h), Image.LANCZOS)
        im.save(temporaire, "JPEG", quality=qualite, optimize=True, progressive=True)
        if not jpeg_valide(temporaire):
            raise OSError("le JPEG produit ne se relit pas")
        os.replace(temporaire, chemin_sortie)
    except Exception:
        temporaire.unlink(missing_ok=True)
        raise


def date_de_controle(ref: str, defaut: str) -> str:
    """La date à laquelle cette image a été regardée, et pas celle du jour.

    `verifie_le` date un contrôle HUMAIN. La recalculer à chaque exécution
    donnerait à croire que quelqu'un a revu l'image le jour du build : on garde
    donc celle déjà inscrite dans l'index, quand elle existe.
    """
    return _INDEX_PRECEDENT.get(ref, {}).get("verifie_le") or defaut


def main(references=None) -> None:
    global _INDEX_PRECEDENT
    _INDEX_PRECEDENT = json.loads(INDEX.read_text(encoding="utf-8")) if INDEX.exists() else {}
    DOSSIER_IMG.mkdir(parents=True, exist_ok=True)
    nettoyer_temporaires()
    recs = json.load(open(CORRESP, encoding="utf-8"))
    retenus = [r for r in recs
               if r["match_status"] == "exact" and r["rights_status"] == "open"
               and r["commons_file"] and r["file_url"]]
    # une seule entrée par référence (au cas où)
    par_ref = {}
    for r in retenus:
        par_ref.setdefault(r["reference_joconde"], r)
    print(f"{len(par_ref)} reproductions ouvertes à intégrer.")

    thumbs = urls_miniatures(sorted({r["commons_file"] for r in par_ref.values()}))

    DOSSIER_IMG.mkdir(parents=True, exist_ok=True)
    index = {}
    telecharges = 0
    for ref, r in sorted(par_ref.items()):
        sortie = DOSSIER_IMG / f"{ref}.jpg"
        url = thumbs.get(r["commons_file"]) or r["file_url"]
        if not fichier_reutilisable(ref, "wikimedia_commons"):
            try:
                optimiser(_get(url), sortie)
                telecharges += 1
                if telecharges % 25 == 0:
                    print(f"    {telecharges} vignettes téléchargées", flush=True)
                time.sleep(PAUSE)
            except Exception as ex:
                print(f"    ⚠ {ref} : {str(ex)[:80]}")
                continue
        index[ref] = {
            "statut": "open",
            "source_type": "wikimedia_commons",
            "url": f"oeuvres/{ref}.jpg",
            "credit": r["credit"],
            "creator": r["creator"],
            "licence": r["license"],
            "licence_url": r["license_url"],
            "source": r["source_page_url"],
            "verifie_le": r["verified_at"],
        }
    # PRIORITÉ ÉDITORIALE : Commons exact → POP → autre exemplaire. POP passe
    # donc AVANT Gallica et l'imagerie Commons. Cet ordre est indispensable aux
    # relances : une entrée déjà passée de Gallica à POP doit être présente dans
    # l'index avant que la passe Gallica arrive, sinon celle-ci réécrirait son
    # ancien JPEG sous le même nom.
    ajouter_pop(index, references)
    ajouter_gallica(index)
    ajouter_imagerie_commons(index)

    INDEX.write_text(json.dumps(index, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{len(index)} entrées → {INDEX.name} ; {telecharges} nouvelles vignettes.")

    fusionner_dans_oeuvres(index)


def ajouter_gallica(index: dict) -> int:
    """Ajoute les estampes populaires trouvées sur Gallica (voir build_gallica.py).

    Ces images ne montrent PAS la feuille décrite par la notice : une planche
    d'Épinal a été tirée à des milliers d'exemplaires, le musée conserve le sien
    et la BnF le sien. `exemplaire_autre` porte cette réserve jusqu'à la légende,
    qui l'écrit sous l'image. Sans cette mention, on ferait passer un exemplaire
    pour un autre.
    """
    if not CORRESP_GALLICA.exists():
        return 0
    recs = json.loads(CORRESP_GALLICA.read_text(encoding="utf-8"))
    retenus = [r for r in recs if r.get("etat") == "exacte" and r.get("image_url")]
    if not retenus:
        return 0
    print(f"{len(retenus)} estampes retenues sur Gallica.")
    DOSSIER_IMG.mkdir(parents=True, exist_ok=True)
    ajoutees = 0
    for r in sorted(retenus, key=lambda x: x["reference_joconde"]):
        ref = r["reference_joconde"]
        # Une reproduction Commons, qui montre l'exemplaire même du musée quand
        # elle existe, l'emporte toujours sur un autre exemplaire.
        if ref in index:
            continue
        sortie = DOSSIER_IMG / f"{ref}.jpg"
        if not fichier_reutilisable(ref, "gallica_bnf"):
            try:
                optimiser(_get(r["image_url"]), sortie)
                ajoutees += 1
                if ajoutees % 10 == 0:
                    print(f"    {ajoutees} vignettes Gallica", flush=True)
                time.sleep(PAUSE)
            except Exception as ex:
                print(f"    ⚠ {ref} : {str(ex)[:80]}")
                continue
        index[ref] = {
            "statut": "open",
            "source_type": "gallica_bnf",
            "url": f"oeuvres/{ref}.jpg",
            "credit": "Bibliothèque nationale de France",
            "creator": "",
            "licence": "domaine public",
            "licence_url": "",
            "source": r["ark"],
            # La réserve, portée jusqu'à l'écran.
            "exemplaire_autre": True,
            "titre_source": r.get("titre_gallica", ""),
            "verifie_le": date_de_controle(ref, str(date.today())),
        }
    print(f"{ajoutees} nouvelles vignettes Gallica.")
    return ajoutees


def ajouter_imagerie_commons(index: dict) -> int:
    """Ajoute les estampes trouvées dans le fonds Commons d'imagerie populaire.

    Même réserve que pour Gallica — c'est un autre exemplaire du même tirage,
    pas la feuille du musée — mais la source est ici Commons, avec ses licences
    propres : le crédit et la licence du fichier sont repris tels quels, jamais
    remplacés par une formule générique.
    """
    if not CORRESP_IMAGERIE.exists():
        return 0
    recs = json.loads(CORRESP_IMAGERIE.read_text(encoding="utf-8"))
    retenus = [r for r in recs if r.get("etat") == "exacte" and r.get("image_url")]
    if not retenus:
        return 0
    print(f"{len(retenus)} estampes retenues dans le fonds d'imagerie Commons.")
    DOSSIER_IMG.mkdir(parents=True, exist_ok=True)
    ajoutees = 0
    for r in sorted(retenus, key=lambda x: x["reference_joconde"]):
        ref = r["reference_joconde"]
        if ref in index:
            continue
        sortie = DOSSIER_IMG / f"{ref}.jpg"
        if not fichier_reutilisable(ref, "wikimedia_commons"):
            try:
                optimiser(_get(r["image_url"]), sortie)
                ajoutees += 1
                time.sleep(PAUSE)
            except Exception as ex:
                print(f"    ⚠ {ref} : {str(ex)[:80]}")
                continue
        index[ref] = {
            "statut": "open",
            "source_type": "wikimedia_commons",
            "url": f"oeuvres/{ref}.jpg",
            "credit": r.get("credit", ""),
            "creator": r.get("auteur_image", ""),
            "licence": r.get("licence", ""),
            "licence_url": r.get("licence_url", ""),
            "source": r.get("page_source", ""),
            "exemplaire_autre": True,
            "titre_source": r.get("fichier", "")[5:],
            "verifie_le": date_de_controle(ref, str(date.today())),
        }
    print(f"{ajoutees} nouvelles vignettes d'imagerie Commons.")
    return ajoutees


def metadonnees_pop(ref: str, valeur: dict) -> dict:
    """Entrée publique d'une image POP, construite à un seul endroit."""
    return {
        "statut": valeur["statut"],
        "source_type": "pop_joconde",
        "url": f"oeuvres/{ref}.jpg",
        "credit": valeur.get("credit") or "",
        "licence": "",
        "source": valeur["notice_pop"],
        "profil": PROFIL_POP,
        "verifie_le": valeur.get("verifie_le", ""),
    }


def conserver_pop_hors_lot(index: dict, registre: dict, demandees: set) -> int:
    """Préserve les entrées POP précédentes qu'un lot limité ne rejoue pas.

    `main()` reconstruit l'index à zéro. Sans cette étape, `--lot` retirerait de
    l'index et des fiches toutes les images POP qui ne figurent pas dans le lot,
    tout en laissant leurs JPEG orphelins sur le disque. Une image hors lot qui
    n'est plus réutilisable bloque l'exécution : un lot partiel ne doit ni la
    régénérer en cachette, ni l'effacer silencieusement.
    """
    conservees = []
    invalides = []
    for ref, precedente in _INDEX_PRECEDENT.items():
        if precedente.get("source_type") != "pop_joconde":
            continue
        if ref in demandees or ref in index:
            continue
        valeur = registre.get(ref)
        if not valeur or not valeur.get("image"):
            invalides.append(ref)
            continue
        if not fichier_reutilisable(ref, "pop_joconde", PROFIL_POP):
            invalides.append(ref)
            continue
        conservees.append((ref, valeur))

    if invalides:
        refs = ", ".join(sorted(invalides)[:8])
        suite = "…" if len(invalides) > 8 else ""
        raise RuntimeError(
            "lot partiel impossible : image(s) POP hors lot à régénérer "
            f"({refs}{suite})"
        )

    for ref, valeur in conservees:
        index[ref] = metadonnees_pop(ref, valeur)
    return len(conservees)


def ajouter_pop(index: dict, references=None) -> dict:
    """Ajoute les reproductions POP après Commons exact, avant les replis.

    Elle applique la priorité arrêtée au §4 du plan, qui ne se lit pas sur la
    provenance mais sur CE QUE L'IMAGE MONTRE :

      1. une image Commons qui montre l'objet même du musée reste en place ;
      2. POP complète les autres références quand une image est disponible ;
      3. Gallica ou l'imagerie Commons ne passent qu'ensuite, pour les références
         encore vides — elles servent de repli quand POP est absent ou en échec.

    `references` limite l'exécution à un sous-ensemble (lot témoin, reprise
    d'un lot en échec). `None` traite tout le corpus : c'est le mode de
    production, et il ne demande aucune réécriture.

    L'ORDRE DES OPÉRATIONS est le point délicat. L'entrée d'index n'est
    remplacée qu'APRÈS un téléchargement et un encodage réussis. Si POP échoue :
    l'ancien JPEG reste (l'écriture est atomique), l'ancienne entrée Commons ou
    Gallica reste, et une référence encore sans image n'en reçoit aucune —
    l'œuvre garde son emplacement vide dans la fiche. Jamais d'entrée qui
    décrirait un fichier absent ou un fichier venu d'ailleurs.
    """
    if not REGISTRE_POP.exists():
        raise FileNotFoundError(f"registre POP introuvable : {REGISTRE_POP}")
    registre = json.loads(REGISTRE_POP.read_text(encoding="utf-8"))

    candidates = sorted(r for r, v in registre.items() if v.get("image"))
    if references is not None:
        demandees = set(references)
        conservees = conserver_pop_hors_lot(index, registre, demandees)
        candidates = [r for r in candidates if r in demandees]
        absentes = demandees - set(registre)
        sans_image = {r for r in demandees if r in registre and not registre[r].get("image")}
        for ref in sorted(absentes | sans_image):
            print(f"    · {ref} : aucune image POP au registre")

    print(f"{len(candidates)} référence(s) POP à examiner"
          + (" (lot restreint)." if references is not None else "."))

    DOSSIER_IMG.mkdir(parents=True, exist_ok=True)
    bilan = {
        "ajoutees": 0,
        "remplacees": 0,
        "reutilisees": 0,
        "conservees_hors_lot": conservees if references is not None else 0,
        "ignorees": 0,
        "echecs": [],
    }
    for ref in candidates:
        entree = index.get(ref)
        # Une reproduction ouverte qui montre l'objet du musée n'est jamais
        # remplacée. Seule une entrée « autre exemplaire » cède la place.
        if entree is not None and not entree.get("exemplaire_autre"):
            bilan["ignorees"] += 1
            continue

        v = registre[ref]
        precedente = _INDEX_PRECEDENT.get(ref, {})
        remplacement = (entree is not None
                         or precedente.get("exemplaire_autre") is True)
        source_remplacee = (entree or precedente).get("source_type")
        sortie = DOSSIER_IMG / f"{ref}.jpg"
        reutilisable = fichier_reutilisable(ref, "pop_joconde", PROFIL_POP)
        if not reutilisable:
            try:
                optimiser(_get(v["image"]), sortie, LARGEUR_POP, QUALITE_POP)
            except Exception as ex:
                # Rien n'est touché : ni le fichier (écriture atomique), ni
                # l'entrée d'index, qui reste celle d'avant ou n'existe pas.
                bilan["echecs"].append({"reference": ref, "erreur": str(ex)[:120]})
                print(f"    ⚠ {ref} : {str(ex)[:80]}")
                continue
            time.sleep(PAUSE_POP)

        index[ref] = metadonnees_pop(ref, v)
        precedente_pop = (_INDEX_PRECEDENT.get(ref, {}).get("source_type")
                           == "pop_joconde")
        if reutilisable and precedente_pop:
            bilan["reutilisees"] += 1
        elif remplacement:
            bilan["remplacees"] += 1
            print(f"    ⇄ {ref} : {source_remplacee} → pop_joconde")
        else:
            bilan["ajoutees"] += 1

    print(f"{bilan['ajoutees']} nouvelle(s) vignette(s) POP, "
          f"{bilan['remplacees']} remplacement(s), "
          f"{bilan['reutilisees']} réutilisée(s), "
          f"{bilan['conservees_hors_lot']} conservée(s) hors lot, "
          f"{bilan['ignorees']} référence(s) laissée(s) à leur source ouverte, "
          f"{len(bilan['echecs'])} échec(s).")
    return bilan


def lot_demande(arguments) -> set | None:
    """`--lot <fichier>` : une référence par ligne, `#` pour un commentaire.

    Sert au lot témoin et, plus tard, à rejouer un lot d'échecs. Sans l'option,
    le pipeline traite tout le corpus : la restriction est un argument de plus,
    pas une branche parallèle à entretenir.
    """
    if not arguments:
        return None
    if len(arguments) != 2 or arguments[0] != "--lot":
        raise SystemExit("usage : build_vignettes.py [--lot <fichier>]")
    chemin = Path(arguments[1])
    refs = {ligne.split("#")[0].strip()
            for ligne in chemin.read_text(encoding="utf-8").splitlines()}
    return {r for r in refs if r}


def fusionner_dans_oeuvres(index: dict) -> int:
    """Attache `image` aux œuvres concernées dans chaque oeuvres/<slug>.json."""
    total = 0
    for chemin in glob.glob(str(DOSSIER_OEUVRES / "*.json")):
        d = json.load(open(chemin, encoding="utf-8"))
        change = False
        for o in d["oeuvres"]:
            img = index.get(o["reference"])
            if img and o.get("image") != img:
                o["image"] = img
                change = True
                total += 1
            elif not img and "image" in o:
                del o["image"]
                change = True
        if change:
            chemin_p = __import__("pathlib").Path(chemin)
            chemin_p.write_text(json.dumps(d, ensure_ascii=False, indent=1),
                                encoding="utf-8")
    print(f"{total} œuvres enrichies d'une image dans les fiches.")
    return total


if __name__ == "__main__":
    main(lot_demande(sys.argv[1:]))
