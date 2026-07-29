"""Métadonnées Joconde des œuvres, pour l'appariement Wikimedia Commons/Wikidata.

Les exports web (oeuvres/<slug>.json) sont volontairement LÉGERS : référence,
titre, musée, ville, famille, verbatim. L'appariement à Commons a besoin de plus
— surtout le NUMÉRO D'INVENTAIRE et de quoi contrôler une correspondance
(technique, dimensions, datation, domaine). On ne charge pas ces champs dans
l'export web (front) : on produit un fichier à part, `oeuvres_metadonnees.json`,
lu par le pipeline d'appariement.

On conserve les formulations ORIGINALES du CSV (aucune normalisation de sens) :
elles serviront de preuves de correspondance et, plus tard, de crédit.

Usage : uv run python src/build_metadonnees.py  (~1 passe du CSV, ~1-2 min)
"""

import csv
import glob
import json
import sys

from config import CHEMIN_CSV, DOSSIER_EXPORTS

DOSSIER_OEUVRES = DOSSIER_EXPORTS / "web" / "oeuvres"
SORTIE = DOSSIER_EXPORTS / "oeuvres_metadonnees.json"

# Colonnes reprises telles quelles (étiquette Joconde entre parenthèses).
CHAMPS = {
    "numero_inventaire": "Numero_inventaire",   # INV/MR… — clé de la Passe 2
    "titre": "Titre",
    "auteur": "Auteur",                          # formulation exacte (qualificatifs)
    "musee": "Nom_officiel_musee",
    "ville": "Ville",
    "domaine": "Domaine",                        # type d'objet (peinture, dessin…)
    "denomination": "Denomination",
    "technique": "Materiaux_techniques",
    "dimensions": "Mesures",
    "millesime": "Millesime_de_creation",
    "date_creation": "Date_creation",
    "epoque": "Epoque",
}

csv.field_size_limit(min(sys.maxsize, 2**31 - 1))


def references_publiees() -> set:
    """Les références uniques présentes dans les 63 fiches d'œuvres."""
    refs = set()
    for chemin in glob.glob(str(DOSSIER_OEUVRES / "*.json")):
        for o in json.load(open(chemin, encoding="utf-8"))["oeuvres"]:
            refs.add(o["reference"])
    return refs


def main() -> None:
    refs = references_publiees()
    print(f"{len(refs)} références à enrichir.")
    meta = {}
    with open(CHEMIN_CSV, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f, delimiter="|"):
            ref = r["Reference"]
            if ref in refs:
                meta[ref] = {"reference": ref}
                for cle, col in CHAMPS.items():
                    meta[ref][cle] = (r.get(col) or "").strip()
                if len(meta) == len(refs):
                    break
    SORTIE.write_text(json.dumps(meta, ensure_ascii=False, indent=1), encoding="utf-8")
    manquants = len(refs) - len(meta)
    avec_inv = sum(1 for m in meta.values() if m["numero_inventaire"])
    print(f"{len(meta)} enrichies → {SORTIE.name} "
          f"({SORTIE.stat().st_size / 1024:.0f} Ko)")
    print(f"  avec numéro d'inventaire : {avec_inv} "
          f"({avec_inv / len(meta):.0%})")
    if manquants:
        print(f"  ⚠ {manquants} références absentes du CSV (à examiner)")


if __name__ == "__main__":
    main()
