"""Reproductions d'estampes populaires trouvées sur Gallica (BnF).

Pourquoi une source de plus, après Commons (2026-08-06) : le lot 2 d'artistes est
fait d'imagerie populaire — musée de l'Image d'Épinal en tête — quasi absente de
Wikidata. Commons a rendu 8 images sur 2 413 références. Gallica, lui, conserve
le dépôt légal des planches Pellerin et les publie en domaine public.

CE QUE CETTE SOURCE PEUT DIRE, ET CE QU'ELLE NE PEUT PAS
--------------------------------------------------------
Une planche d'Épinal a été tirée à des milliers d'exemplaires. Le musée décrit
LE SIEN ; Gallica montre CELUI DE LA BnF — son tampon de dépôt légal est souvent
visible sur l'image. Ce n'est donc jamais « la reproduction de l'œuvre décrite
par la notice », mais un AUTRE EXEMPLAIRE DU MÊME TIRAGE. L'application le dit
sous l'image ; on ne fait pas passer l'un pour l'autre.

Il en découle une règle stricte : **si le musée possède plusieurs notices portant
le même titre, on n'apparie pas.** On serait incapable de dire à laquelle des
notices rattacher l'image, et rattacher au hasard serait une affirmation fausse.
161 titres sur 234 sont dans ce cas favorable (relevé du 2026-08-06).

Confirmation exigée — jamais le seul titre :
  1. le titre, comparé sur une forme normalisée (accents, casse, ponctuation) ;
  2. l'ÉDITEUR : la notice Gallica doit nommer Pellerin, comme Joconde ;
  3. la notice Gallica doit être une ESTAMPE (dc:type image, pas un livre) ;
  4. la DATE, quand les deux la portent : écart de 2 ans toléré (le dépôt légal
     suit parfois l'impression) ; au-delà, refus.
Le reste — dimensions, technique — DIVERGE normalement d'un exemplaire à
l'autre (marges rognées, catalogage « lithographie » ici et « gravure sur bois »
là) et ne peut donc pas servir de preuve. On ne s'en sert pas.

Sorties :
  - data/exports/gallica_correspondances.{json,csv} : toutes les recherches,
    avec leur état (exacte / candidate / refusee / introuvable) et le détail des
    éléments concordants ;
  - data/exports/gallica_bilan.json ;
  - vignettes déposées par build_vignettes.py (ce script ne télécharge rien).

Cache résumable : data/cache/gallica_sru.json — aucune requête n'est refaite.

Usage : uv run python src/build_gallica.py [--limite N]
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
CACHE_SRU = DOSSIER_CACHE / "gallica_sru.json"
SORTIE_JSON = DOSSIER_EXPORTS / "gallica_correspondances.json"
SORTIE_CSV = DOSSIER_EXPORTS / "gallica_correspondances.csv"
BILAN = DOSSIER_EXPORTS / "gallica_bilan.json"

UA = {"User-Agent": "inventaire-du-doute/1.0 (projet data-journalisme ; hericlibong@gmail.com)"}
SRU = "https://gallica.bnf.fr/SRU"
PAUSE = 0.6


# --------------------------------------------------------------------------
# Normalisation et comparaison
# --------------------------------------------------------------------------
def aplat(texte: str) -> str:
    """Forme comparable : sans accent, sans ponctuation, en minuscules.

    Les titres inscrits sont saisis tels qu'ils figurent SUR la planche, en
    capitales, avec une ponctuation flottante (« REMÈDE contre LE SPLEEN »)
    quand Gallica écrit « Remède contre le spleen ».
    """
    t = unicodedata.normalize("NFD", texte or "")
    t = "".join(c for c in t if unicodedata.category(c) != "Mn")
    t = re.sub(r"[^a-zA-Z0-9]+", " ", t.lower())
    return re.sub(r"\s+", " ", t).strip()


def titre_de_recherche(titre_joconde: str) -> str:
    """Le titre Joconde porte des mentions de saisie et le numéro de planche."""
    t = re.sub(r"\(titre[^)]*\)", " ", titre_joconde)
    t = re.sub(r"N[°ᵒ][\s.]*\d+\s*(bis|ter)?", " ", t, flags=re.I)
    t = t.replace("/", " ").replace(";", " ")
    return re.sub(r"\s+", " ", t).strip(" .,")


def annee(texte: str):
    m = re.search(r"\b(1[6-9]\d\d|20\d\d)\b", texte or "")
    return int(m.group(1)) if m else None


# --------------------------------------------------------------------------
# Gallica
# --------------------------------------------------------------------------
def sru(query: str, essais: int = 3) -> str:
    url = (f"{SRU}?operation=searchRetrieve&version=1.2&maximumRecords=10"
           f"&query={urllib.parse.quote(query)}")
    for essai in range(essais):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=60) as r:
                return r.read().decode("utf-8", "replace")
        except Exception:
            if essai == essais - 1:
                raise
            time.sleep(2 * (essai + 1))
    return ""


def notices(xml: str):
    """Découpe la réponse SRU en notices, avec leurs champs Dublin Core."""
    out = []
    for bloc in re.findall(r"<srw:record>(.*?)</srw:record>", xml, re.S):
        champs = defaultdict(list)
        for tag in ("title", "creator", "date", "publisher", "format",
                    "rights", "identifier", "type", "source"):
            for v in re.findall(rf"<dc:{tag}>(.*?)</dc:{tag}>", bloc, re.S):
                champs[tag].append(re.sub(r"\s+", " ", v).strip())
        if champs:
            out.append(dict(champs))
    return out


def ark_de(notice) -> str:
    for ident in notice.get("identifier", []):
        if ident.startswith("https://gallica.bnf.fr/ark:"):
            return ident
    return ""


# --------------------------------------------------------------------------
# Décision
# --------------------------------------------------------------------------
def examine(oeuvre, meta, notice):
    """Renvoie (etat, raisons) pour une notice Gallica face à une notice Joconde.

    `exacte` n'affirme PAS que c'est la même feuille — cette source ne peut pas
    le dire. Elle affirme : même planche éditoriale, même éditeur, dates
    compatibles. L'affichage porte la mention « autre exemplaire du même tirage ».
    """
    raisons, contre = [], []
    titres = notice.get("title", [])
    voulu = aplat(titre_de_recherche(oeuvre["titre"]))
    # Gallica préfixe « Imagerie d'Epinal. N° 340, » devant le titre de la planche.
    trouve = next((t for t in titres if voulu and voulu in aplat(t)), None)
    if not trouve:
        return "refusee", ["le titre ne se retrouve pas dans la notice Gallica"]
    raisons.append(f'titre retrouvé dans « {trouve[:70]} »')

    editeur_joconde = "pellerin" in aplat(meta.get("auteur", ""))
    editeur_gallica = any("pellerin" in aplat(p) for p in
                          notice.get("publisher", []) + notice.get("creator", []) + titres)
    if editeur_joconde and not editeur_gallica:
        contre.append("l'éditeur Pellerin n'est pas nommé côté Gallica")
    elif editeur_gallica:
        raisons.append("éditeur Pellerin des deux côtés")

    est_image = any("image" in aplat(t) or "estampe" in aplat(t)
                    for t in notice.get("type", []) + titres)
    if not est_image:
        contre.append("la notice Gallica n'est pas une estampe")

    a_j, a_g = annee(meta.get("millesime", "")), annee(" ".join(notice.get("date", [])))
    if a_j and a_g:
        if abs(a_j - a_g) <= 2:
            raisons.append(f"dates compatibles ({a_j} / {a_g})")
        else:
            contre.append(f"dates incompatibles ({a_j} / {a_g})")

    libre = any("domaine public" in aplat(r) or "public domain" in aplat(r)
                for r in notice.get("rights", []))
    if not libre:
        contre.append("le domaine public n'est pas déclaré")
    else:
        raisons.append("domaine public déclaré par la BnF")

    if contre:
        return "refusee", contre
    # Éditeur + estampe + titre = les trois piliers exigés.
    if editeur_gallica and est_image:
        return "exacte", raisons
    return "candidate", raisons + ["confirmation incomplète : à contrôler à l'œil"]


# --------------------------------------------------------------------------
def main() -> None:
    limite = None
    if "--limite" in sys.argv:
        limite = int(sys.argv[sys.argv.index("--limite") + 1])

    meta = json.loads(META_JSON.read_text(encoding="utf-8"))
    DOSSIER_CACHE.mkdir(parents=True, exist_ok=True)
    cache = json.loads(CACHE_SRU.read_text(encoding="utf-8")) if CACHE_SRU.exists() else {}

    # Périmètre : les œuvres SANS image dont Joconde nomme Pellerin comme éditeur.
    # C'est l'imagerie populaire, la seule matière que Gallica puisse rendre ici.
    oeuvres, par_titre = [], Counter()
    for fiche in sorted(DOSSIER_OEUVRES.glob("*.json")):
        données = json.loads(fiche.read_text(encoding="utf-8"))
        for o in (données if isinstance(données, list) else données.get("oeuvres", [])):
            if o.get("image"):
                continue
            m = meta.get(o["reference"], {})
            if "pellerin" not in aplat(m.get("auteur", "")):
                continue
            o = dict(o, _artiste=fiche.stem)
            oeuvres.append(o)
            par_titre[aplat(titre_de_recherche(o["titre"]))] += 1

    print(f"{len(oeuvres)} œuvres sans image éditées par Pellerin.")

    resultats, etats = [], Counter()
    interrogees = 0
    for o in oeuvres:
        cle = aplat(titre_de_recherche(o["titre"]))
        m = meta.get(o["reference"], {})
        ligne = {
            "reference_joconde": o["reference"],
            "titre_joconde": o["titre"],
            "artiste": o["_artiste"],
            "musee": o.get("musee", ""),
            "numero_inventaire": m.get("numero_inventaire", ""),
            "etat": "", "raisons": [], "ark": "", "titre_gallica": "",
            "licence": "", "source": "Gallica (BnF)",
        }

        # Plusieurs notices du musée portent ce titre : on ne saurait pas à
        # laquelle rattacher l'image. On n'apparie pas.
        if par_titre[cle] > 1:
            ligne["etat"] = "refusee"
            ligne["raisons"] = [f"le musée conserve {par_titre[cle]} notices de ce titre : "
                                "l'exemplaire visé serait indéterminé"]
            resultats.append(ligne); etats["refusee"] += 1
            continue
        if len(cle) < 8:
            ligne["etat"] = "refusee"
            ligne["raisons"] = ["titre trop court ou trop générique pour être probant"]
            resultats.append(ligne); etats["refusee"] += 1
            continue

        requete = f'dc.title all "{titre_de_recherche(o["titre"])}" and dc.type all "image"'
        if requete in cache:
            xml = cache[requete]
        else:
            if limite is not None and interrogees >= limite:
                break
            try:
                xml = sru(requete)
            except Exception as e:
                print(f"!! {o['reference']} : {e}")
                continue
            cache[requete] = xml
            interrogees += 1
            time.sleep(PAUSE)
            if interrogees % 25 == 0:
                CACHE_SRU.write_text(json.dumps(cache, ensure_ascii=False), encoding="utf-8")
                print(f"  {interrogees} recherches…")

        meilleur = None
        for notice in notices(xml):
            etat, raisons = examine(o, m, notice)
            rang = {"exacte": 0, "candidate": 1, "refusee": 2}[etat]
            if meilleur is None or rang < meilleur[0]:
                meilleur = (rang, etat, raisons, notice)
            if rang == 0:
                break

        if meilleur is None:
            ligne["etat"] = "introuvable"
            ligne["raisons"] = ["aucune notice Gallica pour ce titre"]
        else:
            _, etat, raisons, notice = meilleur
            ligne["etat"] = etat
            ligne["raisons"] = raisons
            if etat != "refusee":
                ligne["ark"] = ark_de(notice)
                ligne["titre_gallica"] = (notice.get("title") or [""])[0]
                ligne["licence"] = "domaine public"
                # IIIF : image entière, 1200 px de large, suffisant pour une vignette.
                ligne["image_url"] = f"{ligne['ark'].replace('https://gallica.bnf.fr/', 'https://gallica.bnf.fr/iiif/')}/f1/full/1200,/0/native.jpg"
        etats[ligne["etat"]] += 1
        resultats.append(ligne)

    CACHE_SRU.write_text(json.dumps(cache, ensure_ascii=False), encoding="utf-8")
    SORTIE_JSON.write_text(json.dumps(resultats, ensure_ascii=False, indent=1), encoding="utf-8")
    with open(SORTIE_CSV, "w", newline="", encoding="utf-8") as f:
        colonnes = ["reference_joconde", "titre_joconde", "artiste", "musee",
                    "numero_inventaire", "etat", "titre_gallica", "ark", "licence",
                    "source", "raisons"]
        w = csv.DictWriter(f, fieldnames=colonnes, extrasaction="ignore")
        w.writeheader()
        for r in resultats:
            w.writerow({**r, "raisons": " ; ".join(r["raisons"])})

    bilan = {
        "date": str(date.today()),
        "perimetre": "œuvres sans image dont Joconde nomme Pellerin comme éditeur",
        "oeuvres_examinees": len(resultats),
        "par_etat": dict(etats),
        "regle": ("un titre porté par plusieurs notices du musée n'est jamais apparié : "
                  "l'exemplaire visé serait indéterminé"),
        "mention_obligatoire": "autre exemplaire du même tirage (BnF / Gallica)",
    }
    BILAN.write_text(json.dumps(bilan, ensure_ascii=False, indent=1), encoding="utf-8")

    print("\n=== BILAN ===")
    for etat in ("exacte", "candidate", "refusee", "introuvable"):
        print(f"  {etat:12} : {etats[etat]}")
    print(f"Livrables → gallica_correspondances.{{json,csv}}, gallica_bilan.json")


if __name__ == "__main__":
    main()
