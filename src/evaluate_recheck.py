"""Bilan T5bis — taux de faux positifs après reformulation (lexique v1).

Combine deux sources de verdicts humains :
- le mini-contrôle T4bis (echantillon_recheck_annote.csv) pour les familles
  reformulées en v1 : ?, école de, atelier ;
- la vérification T4 (echantillon_verification_annote.csv) pour les familles
  non touchées : leurs taux restent valables.

Cas particulier « attribué à » : son seul faux T4 était « (attribué, d'après) »,
désormais exclu par le lexique v1 (prouvé par tests/test_markers.py). On
publie néanmoins le calcul CONSERVATEUR (faux maintenu) à côté du calcul
ajusté : sous-estimer sa propre qualité est plus défendable que l'inverse.

Poids : comptages v1 (data/exports/comptages.csv, régénéré après reformulation).
Usage : uv run python src/evaluate_recheck.py
"""

import pandas as pd

import markers
from config import DOSSIER_EXPORTS

# familles dont le taux vient du mini-contrôle T4bis
FAMILLES_RECHECK = {
    "? (point d'interrogation)",
    "école de",
    "atelier (qualificatif de doute)",
    "Atelier de X en nom d'auteur (écarté)",
}
# libellés v0 → v1 (la famille atelier a été renommée en v1)
RENOMMAGES = {"atelier de": "atelier (qualificatif de doute)"}


def taux_par_famille(annote: pd.DataFrame) -> pd.DataFrame:
    """Taux de faux positifs par famille (« incertain » exclus du calcul)."""
    annote = annote.copy()
    annote["verdict"] = annote["verdict"].str.strip().str.lower()
    annote["famille"] = annote["famille"].replace(RENOMMAGES)
    juges = annote[annote["verdict"].isin(["vrai", "faux"])]
    return juges.groupby("famille")["verdict"].agg(
        juges="count", faux=lambda v: (v == "faux").sum()
    )


def main() -> None:
    t4 = taux_par_famille(
        pd.read_csv(DOSSIER_EXPORTS / "echantillon_verification_annote.csv", dtype=str)
    )
    t4bis = taux_par_famille(
        pd.read_csv(DOSSIER_EXPORTS / "echantillon_recheck_annote.csv", dtype=str)
    )
    comptages = pd.read_csv(DOSSIER_EXPORTS / "comptages.csv").set_index("libelle")

    lignes = []
    for famille in markers.FAMILLES:
        libelle = famille.libelle
        source = "T4bis" if libelle in FAMILLES_RECHECK else "T4"
        verdicts = t4bis if source == "T4bis" else t4
        if libelle not in verdicts.index:
            continue
        juges, faux = verdicts.loc[libelle, ["juges", "faux"]]
        taux = faux / juges
        poids = int(comptages.loc[libelle, "notices"])
        lignes.append({
            "famille": libelle,
            "categorie": famille.categorie,
            "source_verdicts": source,
            "juges": juges,
            "faux": faux,
            "taux_faux_positifs": round(taux, 4),
            "notices_base_v1": poids,
            "faux_estimes": round(poids * taux),
        })

    bilan = pd.DataFrame(lignes)
    bilan.to_csv(DOSSIER_EXPORTS / "bilan_faux_positifs_v1.csv", index=False)

    print("Taux de faux positifs par famille (lexique v1) :\n")
    for _, r in bilan.sort_values(["categorie", "notices_base_v1"],
                                  ascending=[True, False]).iterrows():
        print(f"  {r['categorie']:<9} {r['famille']:<40} "
              f"{r['faux']:>2}/{r['juges']:<3} = {r['taux_faux_positifs']:6.1%} "
              f"[{r['source_verdicts']}]  (~{r['faux_estimes']:,} sur {r['notices_base_v1']:,})".replace(",", " "))

    print("\nTaux globaux pondérés (catégorie doute) :")
    doute = bilan[bilan["categorie"] == "doute"]
    detections = doute["notices_base_v1"].sum()
    faux_conservateur = doute["faux_estimes"].sum()
    # calcul ajusté : le faux « attribué à » de T4 est exclu par le lexique v1
    ajuste = doute.copy()
    ajuste.loc[ajuste["famille"] == "attribué à", "faux_estimes"] = 0
    faux_ajuste = ajuste["faux_estimes"].sum()
    print(f"  conservateur : {faux_conservateur:>5,} faux / {detections:,} = "
          f"{faux_conservateur / detections:5.1%}".replace(",", " "))
    print(f"  ajusté       : {faux_ajuste:>5,} faux / {detections:,} = "
          f"{faux_ajuste / detections:5.1%}  "
          f"(faux « attribué, d'après » prouvé exclu par les tests)".replace(",", " "))

    print(f"\n→ export : {DOSSIER_EXPORTS / 'bilan_faux_positifs_v1.csv'}")


if __name__ == "__main__":
    main()
