"""Autres exemplaires d'imagerie populaire trouvés sur Wikimedia Commons.

Troisième source d'images, après Commons par identifiant (2026-07/08) et Gallica
(2026-08-06). Elle existe parce que les deux premières ont buté sur le même mur :
le musée de l'Image d'Épinal conserve 505 planches sans reproduction, et ni
Wikidata ni la BnF ne les rendent.

CE QUI CHANGE ICI : LA MANIÈRE DE CHERCHER
------------------------------------------
L'appariement Commons de juillet passait par l'identifiant Joconde porté par un
élément Wikidata. C'est une clé sûre, mais elle ne parle que des œuvres déjà
décrites dans Wikidata — presque aucune estampe populaire. Ici on prend le
problème par l'autre bout : on moissonne le FONDS d'images d'Épinal déjà versé
sur Commons (catégorie « Images d'Épinal » et ses sous-catégories, environ
1 500 fichiers), puis on cherche nos notices dedans.

LE NUMÉRO DE PLANCHE, ET POURQUOI IL NE SUFFIT PAS
--------------------------------------------------
Les musées relèvent ce qui est imprimé sur la feuille, et l'imagerie numérote
ses planches : « IMAGERIE D'EPINAL, N.°551 ». Ce relevé est dans le champ
Joconde `Precisions_inscriptions` (355 des 505 notices d'Épinal le portent).
C'est précieux : trois notices du musée s'intitulent « Notre-Dame de
Bon-Secours » et le numéro les sépare — 1883 chez Pellerin, 1119 chez
Olivier-Pinot, 102 chez Pinot-Sagaire. Sans lui, l'appariement de juillet
refusait les trois, faute de savoir laquelle montrer.

Mais chaque maison a SA numérotation, et les petits numéros se répètent d'une
série à l'autre. Le numéro est donc un DISCRIMINANT, jamais une clé : il départage
des candidates trouvées par le titre, il n'en désigne aucune à lui seul. Un
appariement demande les deux, et le titre doit se retrouver dans le titre du
fichier ou son intitulé d'objet — pas seulement dans la description, trop bavarde
pour être probante (elle a produit des rapprochements faux à l'essai).

CE QUE CES IMAGES MONTRENT
--------------------------
Le même que pour Gallica : un AUTRE EXEMPLAIRE du même tirage, pas la feuille
décrite par la notice. La mention est portée jusque sous l'image. Et la règle
d'indétermination tient : si deux notices du musée partagent titre ET numéro,
on n'apparie ni l'une ni l'autre.

Sorties :
  - data/exports/imagerie_commons_correspondances.{json,csv} : toutes les
    notices examinées, avec leur état et le détail de ce qui concorde ;
  - data/exports/imagerie_commons_bilan.json ;
  - data/exports/imagerie_a_verifier.csv : les correspondances que la machine
    ne peut pas trancher, à regarder une par une ;
  - vignettes déposées par build_vignettes.py (ce script ne télécharge rien).

Cache résumable : data/cache/commons_imagerie.json (le fonds moissonné).

Usage : uv run python src/build_imagerie_commons.py [--remoissonner]
"""

import csv
import json
import re
import sys
import time
import unicodedata
import urllib.parse
import urllib.request
from collections import Counter, defaultdict
from datetime import date

from config import DOSSIER_EXPORTS, RACINE

DOSSIER_OEUVRES = DOSSIER_EXPORTS / "web" / "oeuvres"
META_JSON = DOSSIER_EXPORTS / "oeuvres_metadonnees.json"
DOSSIER_CACHE = RACINE / "data" / "cache"
CACHE_FONDS = DOSSIER_CACHE / "commons_imagerie.json"
SORTIE_JSON = DOSSIER_EXPORTS / "imagerie_commons_correspondances.json"
SORTIE_CSV = DOSSIER_EXPORTS / "imagerie_commons_correspondances.csv"
BILAN = DOSSIER_EXPORTS / "imagerie_commons_bilan.json"
A_VERIFIER = DOSSIER_EXPORTS / "imagerie_a_verifier.csv"
INDEX_IMAGES = DOSSIER_EXPORTS / "web" / "images_index.json"

API = "https://commons.wikimedia.org/w/api.php"
UA = {"User-Agent": "inventaire-du-doute/1.0 (projet data-journalisme ; hericlibong@gmail.com)"}
PAUSE = 0.3

# Le fonds moissonné. Une seule racine pour l'instant : c'est là que se trouve
# l'imagerie populaire versée sur Commons.
CATEGORIES_RACINES = ["Category:Images d'Épinal"]
PROFONDEUR = 2

# Maisons d'imagerie citées par Joconde comme éditeur ou imprimeur. Sert à
# délimiter le périmètre, pas à décider d'un appariement.
IMAGERIES = ("pellerin", "pinot", "imagerie d epinal", "imagerie epinal",
             "gangel", "didion", "wentzel", "burckardt", "olivier")

# Licences acceptées : celles qui autorisent la reproduction, crédit porté.
LICENCES_OUVERTES = ("public domain", "cc0", "cc by", "cc by-sa")

# Confirmées à l'œil (référence Joconde -> nom du fichier Commons).
#
# Le script sait dire qu'un titre concorde ; il ne sait pas dire qu'une image
# montre bien la planche décrite. Quand le fonds ne porte pas de numéro, la
# machine s'arrête à « candidate » et c'est un humain qui regarde l'image, la
# compare au relevé d'inscriptions du musée et tranche. Rien n'entre ici sans
# ce contrôle. La liste à examiner est écrite dans imagerie_a_verifier.csv.
CONFIRMEES = {
    # Le titre, la mention d'éditeur au même endroit de la feuille (« Fabrique
    # de PELLERIN, Imprimeur-Libraire, à ÉPINAL », bas centre), les couplets
    # relevés par le musée et le monogramme du graveur, tout concorde.
    "M0537039802": "File:Donnera-t-on quelque chose à crédit Quand le coq chantera,"
                   " crédit on donnera - estampe - G. F. (François Georgin)"
                   " - btv1b55001802z.jpg",
}

# Écartées à l'œil (référence -> raison, publiable telle quelle).
#
# Toutes ces images portent bien le titre de la notice. Aucune ne montre la
# planche décrite. Une image populaire se réédite pendant un siècle : la même
# composition ressort chez un concurrent, avec un autre numéro, un autre texte
# et une autre adresse d'imprimeur. Le titre ne prouve donc rien à lui seul —
# c'est ce que ces dix cas ont montré.
ECARTEES = {
    "M0537000075": "la feuille numérisée est un tirage antérieur, sans numéro, "
                   "et son texte n'est pas celui que le musée a relevé",
    "M0537008158": "la feuille numérisée ne porte aucun numéro : rien ne dit "
                   "lequel des deux exemplaires du musée elle montre",
    "M0537007954": "la feuille numérisée ne porte aucun numéro : rien ne dit "
                   "lequel des deux exemplaires du musée elle montre",
    "M0537001788": "la feuille numérisée est imprimée par Pellerin & Cie, "
                   "la notice décrit un tirage de la Fabrique de Pellerin",
    "M0537043716": "la feuille numérisée porte le numéro 384, et le musée en "
                   "relève un autre",
    "M0537053035": "la feuille numérisée porte le numéro 384, et le musée en "
                   "relève un autre",
    "M0537007855": "la feuille numérisée sort de chez Pellerin, la notice décrit "
                   "une planche de Pinot & Sagaire",
    "M0537053037": "le fichier ne montre qu'une case découpée, pas la feuille",
    "M0537040328": "le fichier ne montre qu'une fable, quand la notice décrit "
                   "une feuille qui en réunit douze",
    "M0537040272": "la feuille numérisée compte quatre colonnes et porte une "
                   "autre adresse d'imprimeur : c'est une autre édition",
}


# --------------------------------------------------------------------------
# Normalisation
# --------------------------------------------------------------------------
def aplat(texte: str) -> str:
    """Forme comparable : sans balise, sans accent, sans ponctuation.

    Les titres inscrits sont saisis tels qu'ils figurent SUR la planche, en
    capitales et avec une ponctuation flottante ; Commons écrit en bas de casse.
    Les descriptions Commons arrivent en HTML.
    """
    t = re.sub(r"<[^>]+>", " ", texte or "")
    t = unicodedata.normalize("NFD", t)
    t = "".join(c for c in t if unicodedata.category(c) != "Mn")
    t = re.sub(r"[^a-zA-Z0-9]+", " ", t.lower())
    return re.sub(r"\s+", " ", t).strip()


def titre_comparable(titre_joconde: str) -> str:
    """Le titre Joconde porte des mentions de saisie, des traductions et le numéro.

    « NOTRE-DAME DE BON-SECOURS. N° 1119 (titre inscrit) » → « notre dame de
    bon secours ». On garde le premier titre : les suivants, après « ; », sont
    des traductions (néerlandais, allemand) ou des titres factices du musée.
    """
    t = re.split(r";", titre_joconde or "")[0]
    t = re.sub(r"\(titre[^)]*\)", " ", t)
    t = re.sub(r"\bN[°ºo][\s.=]*\d+\s*(bis|ter)?", " ", t, flags=re.I)
    t = t.replace("/", " ")
    return aplat(t)


# Le musée recopie le numéro tel qu'il est imprimé, et l'imagerie l'écrit de
# toutes les façons : « N°551 », « N.°551 », « N° 1883 », « N.°.23. ». Le point
# se glisse aussi bien avant le degré qu'après.
NUM = re.compile(r"\bn[\s.]*[°ºo]?[\s.=]*(\d{1,4})\b")
NUM_JOCONDE = r"N[\s.]*[°ºo][\s.=]*(\d{1,4})"


def numeros(texte: str) -> set:
    """Les numéros de planche lisibles dans un texte déjà aplati."""
    return set(NUM.findall(aplat(texte)))


def numero_joconde(meta: dict, titre: str):
    """Le numéro de planche relevé par le musée, s'il y en a un.

    Il se lit d'abord dans les précisions d'inscriptions — le relevé de ce qui
    est imprimé sur la feuille — puis, à défaut, dans le titre lui-même, où
    certains musées le recopient.
    """
    inscr = meta.get("precisions_inscriptions", "") or ""
    # D'abord le numéro annoncé juste après le nom de l'imagerie : c'est celui
    # de la planche. Les autres nombres du relevé peuvent être un prix, une
    # date ou un numéro de série.
    m = re.search(r"[EÉ]PINAL[,.\s]*" + NUM_JOCONDE, inscr, re.I)
    if m:
        return m.group(1)
    m = re.search(NUM_JOCONDE, inscr, re.I)
    if m:
        return m.group(1)
    m = re.search(NUM_JOCONDE, titre or "", re.I)
    return m.group(1) if m else None


def licence_ouverte(libelle: str) -> bool:
    return any(l in aplat(libelle) for l in LICENCES_OUVERTES)


# --------------------------------------------------------------------------
# Le fonds Commons
# --------------------------------------------------------------------------
def api(**params):
    # En POST : les lots de titres de fichiers dépassent la longueur d'URL
    # admise (HTTP 414) dès que les noms sont un peu longs, ce qui est la règle
    # sur ce fonds (« Imagerie d'Epinal. N° 770, Types des premiers… »).
    params.update(action="query", format="json")
    corps = urllib.parse.urlencode(params).encode("utf-8")
    for essai in range(4):
        try:
            req = urllib.request.Request(API, data=corps, headers=UA)
            with urllib.request.urlopen(req, timeout=90) as r:
                return json.load(r)
        except Exception:
            if essai == 3:
                raise
            time.sleep(2 * (essai + 1))
    return {}


def membres(categorie: str, genre: str) -> list:
    out, suite = [], {}
    while True:
        r = api(list="categorymembers", cmtitle=categorie, cmlimit="500",
                cmtype=genre, **suite)
        out += [m["title"] for m in r["query"]["categorymembers"]]
        if "continue" not in r:
            return out
        suite = r["continue"]


def fichiers_du_fonds() -> list:
    """Parcourt les catégories racines et leurs sous-catégories."""
    vus, fichiers = set(), set()
    a_voir = [(c, 0) for c in CATEGORIES_RACINES]
    while a_voir:
        cat, niveau = a_voir.pop()
        if cat in vus:
            continue
        vus.add(cat)
        fichiers.update(membres(cat, "file"))
        if niveau < PROFONDEUR:
            for sous in membres(cat, "subcat"):
                if sous not in vus:
                    a_voir.append((sous, niveau + 1))
    print(f"{len(vus)} catégories parcourues, {len(fichiers)} fichiers.")
    return sorted(fichiers)


def moissonne(remoissonner: bool) -> dict:
    """Le fonds, avec crédit et licence de chaque fichier. Repris du cache."""
    DOSSIER_CACHE.mkdir(parents=True, exist_ok=True)
    fonds = {}
    if CACHE_FONDS.exists() and not remoissonner:
        fonds = json.loads(CACHE_FONDS.read_text(encoding="utf-8"))
    fichiers = fichiers_du_fonds()
    reste = [f for f in fichiers if f not in fonds]
    print(f"{len(fonds)} fichiers en cache, {len(reste)} à décrire.")
    for i in range(0, len(reste), 40):
        r = api(titles="|".join(reste[i:i + 40]), prop="imageinfo",
                iiprop="url|extmetadata|size", iiurlwidth="1200")
        for page in r["query"]["pages"].values():
            info = (page.get("imageinfo") or [{}])[0]
            extra = info.get("extmetadata", {})

            def champ(cle):
                return (extra.get(cle) or {}).get("value", "")

            fonds[page["title"]] = {
                "url": info.get("url", ""),
                "miniature": info.get("thumburl", ""),
                "licence": champ("LicenseShortName"),
                "licence_url": champ("LicenseUrl"),
                "auteur": champ("Artist"),
                "credit": champ("Credit"),
                "description": champ("ImageDescription"),
                "objet": champ("ObjectName"),
            }
        CACHE_FONDS.write_text(json.dumps(fonds, ensure_ascii=False), encoding="utf-8")
        time.sleep(PAUSE)
    return fonds


def index_du_fonds(fonds: dict) -> list:
    """Prépare une fois pour toutes les formes comparables de chaque fichier."""
    index = []
    for nom, v in fonds.items():
        # Le nom du fichier et l'intitulé d'objet sont des désignations ; la
        # description est un commentaire libre. Les deux premiers seuls font
        # preuve de titre, la troisième ne sert qu'à confirmer un numéro.
        designation = aplat(nom[5:] + " " + v.get("objet", ""))
        index.append({
            "fichier": nom,
            "designation": designation,
            "description": aplat(v.get("description", "")),
            "numeros": numeros(designation + " " + v.get("description", "")),
            **v,
        })
    return index


# --------------------------------------------------------------------------
# Décision
# --------------------------------------------------------------------------
MOTS_VIDES = {"de", "la", "le", "les", "des", "du", "et", "un", "une", "au",
              "aux", "en", "dans", "sur", "par", "pour", "a", "l", "d"}


def assez_distinctif(titre: str) -> bool:
    """Un titre trop court ou trop commun ne prouve rien.

    « Les poupées », « La chasse » se retrouvent dans des dizaines de fichiers
    du fonds : les accepter reviendrait à tirer au sort.
    """
    mots = [m for m in titre.split() if m not in MOTS_VIDES and len(m) > 2]
    return len(titre) >= 12 and len(mots) >= 2


def examine(titre, num_joconde, candidat):
    """(etat, raisons) pour un fichier du fonds face à une notice du musée."""
    raisons = []
    if titre in candidat["designation"]:
        raisons.append(f'titre retrouvé dans « {candidat["fichier"][5:80]} »')
        par_titre = True
    elif num_joconde and titre in candidat["description"]:
        raisons.append("titre retrouvé dans la description du fichier")
        par_titre = False
    else:
        return "refusee", []

    if not licence_ouverte(candidat["licence"]):
        return "refusee", [f'licence non ouverte ({candidat["licence"] or "non déclarée"})']

    if num_joconde:
        if num_joconde in candidat["numeros"]:
            raisons.append(f"numéro de planche {num_joconde} des deux côtés")
            return "exacte", raisons
        if candidat["numeros"]:
            return "refusee", [f'numéros de planche différents '
                               f'({num_joconde} contre {"/".join(sorted(candidat["numeros"]))})']
        # Le musée numérote, pas le fichier : rien ne contredit, rien ne confirme.
        return "candidate", raisons + ["le fichier ne porte aucun numéro de planche"]

    if not par_titre:
        return "refusee", []
    if candidat["numeros"]:
        return "candidate", raisons + ["le fichier porte un numéro que la notice n'a pas"]
    return "candidate", raisons + ["aucun numéro de part ni d'autre : titre seul"]


# --------------------------------------------------------------------------
def notices_a_chercher(meta: dict) -> list:
    """Les estampes d'imagerie populaire du corpus.

    Sans exclure celles qui portent déjà une image : c'est ce script qui en a
    posé une partie, et les écarter ferait disparaître ses propres trouvailles
    à la deuxième exécution. La priorité entre sources se règle plus loin, dans
    build_vignettes, où une reproduction de l'exemplaire même du musée l'emporte
    toujours sur un autre exemplaire.
    """
    oeuvres = []
    for fiche in sorted(DOSSIER_OEUVRES.glob("*.json")):
        données = json.loads(fiche.read_text(encoding="utf-8"))
        for o in données.get("oeuvres", []):
            m = meta.get(o["reference"], {})
            if "estampe" not in aplat(m.get("domaine", "")):
                continue
            signature = aplat(m.get("auteur", "") + " " +
                              (m.get("precisions_inscriptions", "") or ""))
            if not any(i in signature for i in IMAGERIES):
                continue
            oeuvres.append(dict(o, _artiste=fiche.stem))
    return oeuvres


def main() -> None:
    remoissonner = "--remoissonner" in sys.argv
    meta = json.loads(META_JSON.read_text(encoding="utf-8"))
    fonds = moissonne(remoissonner)
    index = index_du_fonds(fonds)
    ouvertes = sum(1 for c in index if licence_ouverte(c["licence"]))
    print(f"{len(index)} fichiers dans le fonds, dont {ouvertes} sous licence ouverte.")

    oeuvres = notices_a_chercher(meta)
    print(f"{len(oeuvres)} estampes d'imagerie populaire sans reproduction.")

    # Deux notices D'UN MÊME MUSÉE, de même titre et de même numéro, décrivent
    # deux feuilles qu'on ne saurait pas départager. On ne les apparie ni l'une
    # ni l'autre. Le musée fait partie de la clé : deux villes qui conservent
    # chacune leur « Cadet Rousselle » ne s'empêchent pas mutuellement.
    par_cle = Counter()
    for o in oeuvres:
        m = meta.get(o["reference"], {})
        par_cle[(o.get("musee_code", ""), titre_comparable(o["titre"]),
                 numero_joconde(m, o["titre"]))] += 1

    resultats, etats = [], Counter()
    for o in oeuvres:
        m = meta.get(o["reference"], {})
        titre = titre_comparable(o["titre"])
        num = numero_joconde(m, o["titre"])
        cle = (o.get("musee_code", ""), titre, num)
        ligne = {
            "reference_joconde": o["reference"],
            "titre_joconde": o["titre"],
            "artiste": o["_artiste"],
            "musee": o.get("musee", ""),
            "numero_inventaire": m.get("numero_inventaire", ""),
            "numero_planche": num or "",
            "etat": "", "raisons": [], "fichier": "", "licence": "",
            "credit": "", "auteur_image": "", "image_url": "",
            "source": "Wikimedia Commons",
        }

        if o["reference"] in ECARTEES:
            ligne["etat"] = "refusee"
            ligne["raisons"] = [ECARTEES[o["reference"]] + " (contrôle visuel)"]
        elif not assez_distinctif(titre):
            ligne["etat"] = "refusee"
            ligne["raisons"] = ["titre trop court ou trop commun pour être probant"]
        elif par_cle[cle] > 1:
            ligne["etat"] = "refusee"
            ligne["raisons"] = [
                f"le musée conserve {par_cle[cle]} notices de ce titre"
                + (f" et de ce numéro ({num})" if num else " sans numéro de planche")
                + " : l'exemplaire visé serait indéterminé"]
        else:
            meilleur = None
            for candidat in index:
                etat, raisons = examine(titre, num, candidat)
                if etat == "refusee" and not raisons:
                    continue
                rang = {"exacte": 0, "candidate": 1, "refusee": 2}[etat]
                if meilleur is None or rang < meilleur[0]:
                    meilleur = (rang, etat, raisons, candidat)
                if rang == 0:
                    break
            if meilleur is None:
                ligne["etat"] = "introuvable"
                ligne["raisons"] = ["aucun fichier du fonds ne porte ce titre"]
            else:
                _, etat, raisons, candidat = meilleur
                # Un contrôle visuel l'emporte sur la machine : c'est le seul
                # moyen de conclure quand le fonds ne porte pas de numéro.
                confirme = CONFIRMEES.get(o["reference"])
                if confirme:
                    retenu = next((c for c in index if c["fichier"] == confirme), None)
                    if retenu is None:
                        raise SystemExit(
                            f"CONFIRMEES : {o['reference']} désigne « {confirme} », "
                            "absent du fonds moissonné. Vérifier le nom du fichier.")
                    candidat, etat = retenu, "exacte"
                    raisons = ["image regardée et confirmée à l'œil"]
                ligne["etat"] = etat
                ligne["raisons"] = raisons
                if etat != "refusee":
                    ligne["fichier"] = candidat["fichier"]
                    ligne["licence"] = candidat["licence"]
                    ligne["licence_url"] = candidat["licence_url"]
                    ligne["credit"] = re.sub(r"<[^>]+>", " ", candidat["credit"])[:300].strip()
                    ligne["auteur_image"] = re.sub(r"<[^>]+>", " ", candidat["auteur"])[:200].strip()
                    ligne["image_url"] = candidat["miniature"] or candidat["url"]
                    ligne["page_source"] = ("https://commons.wikimedia.org/wiki/"
                                            + urllib.parse.quote(candidat["fichier"].replace(" ", "_")))
        etats[ligne["etat"]] += 1
        resultats.append(ligne)

    SORTIE_JSON.write_text(json.dumps(resultats, ensure_ascii=False, indent=1),
                           encoding="utf-8")
    with open(SORTIE_CSV, "w", newline="", encoding="utf-8") as f:
        colonnes = ["reference_joconde", "titre_joconde", "artiste", "musee",
                    "numero_inventaire", "numero_planche", "etat", "fichier",
                    "licence", "credit", "auteur_image", "source", "raisons"]
        w = csv.DictWriter(f, fieldnames=colonnes, extrasaction="ignore")
        w.writeheader()
        for r in resultats:
            w.writerow({**r, "raisons": " ; ".join(r["raisons"])})

    # La liste de travail : ce que la machine ne peut pas trancher seule, et
    # qui vaut la peine d'être regardé — une notice déjà illustrée par ailleurs
    # n'attend rien de nous.
    illustrees = set()
    if INDEX_IMAGES.exists():
        illustrees = set(json.loads(INDEX_IMAGES.read_text(encoding="utf-8")))
    a_verifier = [r for r in resultats
                  if r["etat"] == "candidate"
                  and r["reference_joconde"] not in illustrees]
    with open(A_VERIFIER, "w", newline="", encoding="utf-8") as f:
        colonnes = ["reference_joconde", "titre_joconde", "numero_planche", "musee",
                    "numero_inventaire", "fichier", "licence", "page_source",
                    "image_url", "manque"]
        w = csv.DictWriter(f, fieldnames=colonnes, extrasaction="ignore")
        w.writeheader()
        for r in a_verifier:
            w.writerow({**r, "manque": " ; ".join(r["raisons"][1:])})
    print(f"{len(a_verifier)} correspondances à regarder → {A_VERIFIER.name}")

    bilan = {
        "date": str(date.today()),
        "perimetre": "estampes d'imagerie populaire sans reproduction",
        "fonds_commons": {"categories_racines": CATEGORIES_RACINES,
                          "fichiers": len(index), "sous_licence_ouverte": ouvertes},
        "oeuvres_examinees": len(resultats),
        "par_etat": dict(etats),
        "regle_du_numero": ("le numéro de planche départage des candidates trouvées "
                            "par le titre ; il ne désigne jamais une image à lui seul, "
                            "chaque maison ayant sa propre numérotation"),
        "regle_d_indetermination": ("deux notices de même titre et de même numéro "
                                    "ne sont appariées ni l'une ni l'autre"),
        "confirmees_a_l_oeil": len(CONFIRMEES),
        "a_verifier": len(a_verifier),
        "mention_obligatoire": "autre exemplaire du même tirage (Wikimedia Commons)",
    }
    BILAN.write_text(json.dumps(bilan, ensure_ascii=False, indent=1), encoding="utf-8")

    print("\n=== BILAN ===")
    for etat in ("exacte", "candidate", "refusee", "introuvable"):
        print(f"  {etat:12} : {etats[etat]}")
    print("Livrables → imagerie_commons_correspondances.{json,csv}, "
          "imagerie_commons_bilan.json")


if __name__ == "__main__":
    main()
