"""Recouvrements entre catégories et familles (P2-T1).

Une notice peut porter plusieurs marqueurs : « attribué à » ET une ancienne
attribution, un doute ET un « d'après »… Ce script chiffre ces recouvrements
pour qu'aucune publication n'additionne des ensembles qui se chevauchent
(décision utilisateur du 2026-07-03).

Produit :
- le diagramme de Venn des trois catégories doute / copie / révision
  (toutes les intersections, en nombre de notices) ;
- la matrice de co-occurrence des familles de doute entre elles ;
- data/exports/recouvrements.json (chiffres prêts pour la restitution).

Usage : uv run python src/count_overlaps.py  (~3 min)
"""

import json
from collections import Counter

import pandas as pd

import markers
from config import CHEMIN_CSV, DOSSIER_EXPORTS

COLONNES = [
    "Reference", "Auteur", "Precisions_sur_l_auteur", "Ancienne_attribution",
    "Ecole_pays",
]
TAILLE_MORCEAU = 200_000

CODES_PAR_CATEGORIE = {
    "doute": [f.code for f in markers.FAMILLES if f.categorie == "doute"],
    "copie": [f.code for f in markers.FAMILLES if f.categorie == "copie"],
    "revision": [f.code for f in markers.FAMILLES if f.categorie == "revision"],
}


def main() -> None:
    total = 0
    venn = Counter()  # combinaison ('doute','copie',…) -> notices
    codes_doute = CODES_PAR_CATEGORIE["doute"]
    cooccurrence = pd.DataFrame(0, index=codes_doute, columns=codes_doute)

    morceaux = pd.read_csv(
        CHEMIN_CSV, sep="|", usecols=COLONNES, dtype=str, chunksize=TAILLE_MORCEAU
    )
    for morceau in morceaux:
        total += len(morceau)
        det = markers.detections(morceau)

        # Venn des trois catégories
        cat = pd.DataFrame({
            nom: det[codes].any(axis=1)
            for nom, codes in CODES_PAR_CATEGORIE.items()
        })
        for combinaison, nombre in cat.value_counts().items():
            noms = tuple(
                nom for nom, present in zip(cat.columns, combinaison) if present
            )
            if noms:
                venn[noms] += nombre

        # co-occurrence des familles de doute (matrice symétrique ;
        # la diagonale porte l'effectif de chaque famille)
        doute = det[codes_doute].astype(int)
        cooccurrence += doute.T @ doute

        print(f"\r  {total:,} notices lues".replace(",", " "), end="", flush=True)
    print("\n")

    # --- rapport ---
    union = sum(venn.values())
    print(f"Notices portant au moins un marqueur (toutes catégories) : "
          f"{union:,} ({union / total:.2%} de la base)".replace(",", " "))
    print("\nVenn doute / copie / révision (notices) :")
    for noms, n in sorted(venn.items(), key=lambda x: -x[1]):
        print(f"  {' + '.join(noms):<30} {n:>8,}".replace(",", " "))

    print("\nCo-occurrences de familles de doute (paires les plus fréquentes) :")
    paires = [
        (a, b, int(cooccurrence.loc[a, b]))
        for i, a in enumerate(codes_doute)
        for b in codes_doute[i + 1:]
        if cooccurrence.loc[a, b] > 0
    ]
    for a, b, n in sorted(paires, key=lambda x: -x[2])[:10]:
        print(f"  {a} × {b:<22} {n:>6,}".replace(",", " "))

    # --- export JSON (chiffres de référence pour la restitution) ---
    export = {
        "notices_base": total,
        "notices_au_moins_un_marqueur": int(union),
        "venn": {" + ".join(noms): int(n) for noms, n in venn.items()},
        "cooccurrence_doute": {
            a: {b: int(cooccurrence.loc[a, b]) for b in codes_doute}
            for a in codes_doute
        },
    }
    DOSSIER_EXPORTS.mkdir(parents=True, exist_ok=True)
    destination = DOSSIER_EXPORTS / "recouvrements.json"
    destination.write_text(
        json.dumps(export, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"\n→ export : {destination}")


if __name__ == "__main__":
    main()
