"""Bilan de la vérification manuelle (T5) — taux de faux positifs.

Croise l'échantillon annoté par l'utilisateur avec les comptages de T3 :
- taux de faux positifs PAR FAMILLE (verdicts « incertain » exclus du calcul,
  décision utilisateur du 2026-07-04) ;
- taux global PONDÉRÉ par le poids réel de chaque famille dans la base —
  jamais la moyenne brute des 206 lignes, l'échantillon étant stratifié ;
- estimation du nombre de notices « doute » corrigé des faux positifs.

Sortie : data/exports/bilan_faux_positifs.csv + rapport console.
Usage : uv run python src/evaluate_sample.py
"""

import pandas as pd

from config import DOSSIER_EXPORTS

CHEMIN_ANNOTE = DOSSIER_EXPORTS / "echantillon_verification_annote.csv"
CHEMIN_COMPTAGES = DOSSIER_EXPORTS / "comptages.csv"


def main() -> None:
    annote = pd.read_csv(CHEMIN_ANNOTE, dtype=str)
    annote["verdict"] = annote["verdict"].str.strip().str.lower()
    comptages = pd.read_csv(CHEMIN_COMPTAGES).set_index("libelle")

    lignes = []
    for libelle, groupe in annote.groupby("famille", sort=False):
        juges = groupe[groupe["verdict"].isin(["vrai", "faux"])]
        n_faux = (juges["verdict"] == "faux").sum()
        taux_fp = n_faux / len(juges)
        poids = int(comptages.loc[libelle, "notices"])
        lignes.append({
            "famille": libelle,
            "categorie": comptages.loc[libelle, "categorie"],
            "verifiees": len(groupe),
            "incertaines": (groupe["verdict"] == "incertain").sum(),
            "faux": n_faux,
            "taux_faux_positifs": round(taux_fp, 4),
            "notices_base": poids,
            "faux_estimes_base": round(poids * taux_fp),
        })

    bilan = pd.DataFrame(lignes).sort_values(
        ["categorie", "notices_base"], ascending=[True, False]
    )
    bilan.to_csv(DOSSIER_EXPORTS / "bilan_faux_positifs.csv", index=False)

    print("Taux de faux positifs par famille :\n")
    for _, r in bilan.iterrows():
        print(f"  {r['categorie']:<9} {r['famille']:<40} "
              f"{r['faux']:>2}/{r['verifiees'] - r['incertaines']:<3} "
              f"= {r['taux_faux_positifs']:6.1%}   "
              f"(~{r['faux_estimes_base']:,} faux sur {r['notices_base']:,})".replace(",", " "))

    print("\nTaux globaux pondérés par le poids réel des familles :")
    for categorie, groupe in bilan.groupby("categorie"):
        detections = groupe["notices_base"].sum()
        faux = groupe["faux_estimes_base"].sum()
        print(f"  {categorie:<9} {faux:>6,} faux estimés / {detections:,} détections "
              f"= {faux / detections:6.1%}".replace(",", " "))

    print(f"\n→ export : {DOSSIER_EXPORTS / 'bilan_faux_positifs.csv'}")


if __name__ == "__main__":
    main()
