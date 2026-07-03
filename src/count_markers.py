"""Comptage des marqueurs d'incertitude sur toute la base (T3).

Applique le lexique de markers.py au CSV complet, par morceaux, et produit :
- data/exports/comptages.csv          : par famille, avec les deux dénominateurs
  (toutes notices / notices dont Auteur est renseigné) ;
- data/exports/comptages_domaines.csv : taux de doute par domaine ;
- un rapport en console, avec des exemples réels par famille.

Usage : uv run python src/count_markers.py  (~3 min)
"""

from collections import Counter

import pandas as pd

import markers
from config import CHEMIN_CSV, DOSSIER_EXPORTS

COLONNES = [
    "Reference", "Auteur", "Precisions_sur_l_auteur", "Ancienne_attribution",
    "Ecole_pays", "Domaine",
]
TAILLE_MORCEAU = 200_000
DOMAINES_PERIMETRE = {"peinture", "dessin", "sculpture", "estampe"}
CODES_DOUTE = [f.code for f in markers.FAMILLES if f.categorie == "doute"]


def main() -> None:
    total = 0
    total_auteur = 0  # notices dont Auteur est renseigné
    par_famille = Counter()  # code famille -> notices (toutes)
    par_famille_auteur = Counter()  # idem, parmi Auteur renseigné
    doute = Counter()  # agrégats : au moins un marqueur de doute, etc.
    domaine_total = Counter()  # domaine -> notices
    domaine_doute = Counter()  # domaine -> notices avec au moins un doute
    exemples = {f.code: [] for f in markers.FAMILLES}

    morceaux = pd.read_csv(
        CHEMIN_CSV, sep="|", usecols=COLONNES, dtype=str, chunksize=TAILLE_MORCEAU
    )
    for morceau in morceaux:
        total += len(morceau)
        auteur_ok = morceau["Auteur"].notna()
        total_auteur += auteur_ok.sum()

        det = markers.detections(morceau)
        au_moins_un_doute = det[CODES_DOUTE].any(axis=1)

        for famille in markers.FAMILLES:
            colonne = det[famille.code]
            par_famille[famille.code] += colonne.sum()
            par_famille_auteur[famille.code] += (colonne & auteur_ok).sum()
            # garde jusqu'à 3 exemples réels par famille pour le rapport
            for _, ligne in morceau[colonne].head(
                3 - len(exemples[famille.code])
            ).iterrows():
                exemples[famille.code].append(ligne)

        doute["toutes"] += au_moins_un_doute.sum()
        doute["auteur"] += (au_moins_un_doute & auteur_ok).sum()

        # ventilation par domaine (multivalué ;) des notices avec doute
        listes = morceau["Domaine"].fillna("(sans domaine)").str.lower().str.split(";")
        for a_doute, liste in zip(au_moins_un_doute, listes):
            uniques = set(d.strip() for d in liste)
            domaine_total.update(uniques)
            if uniques & DOMAINES_PERIMETRE:
                doute["perimetre_total"] += 1
                doute["perimetre_doute"] += a_doute
            if a_doute:
                domaine_doute.update(uniques)

        print(f"\r  {total:,} notices lues".replace(",", " "), end="", flush=True)
    print("\n")

    # --- export par famille ---
    lignes = []
    for famille in markers.FAMILLES:
        n = par_famille[famille.code]
        n_auteur = par_famille_auteur[famille.code]
        lignes.append({
            "famille": famille.code,
            "libelle": famille.libelle,
            "categorie": famille.categorie,
            "suspect": famille.suspect,
            "notices": n,
            "taux_toutes_notices": round(n / total, 5),
            "taux_auteur_renseigne": round(n_auteur / total_auteur, 5),
        })
    df_familles = pd.DataFrame(lignes).sort_values(
        ["categorie", "notices"], ascending=[True, False]
    )
    DOSSIER_EXPORTS.mkdir(parents=True, exist_ok=True)
    df_familles.to_csv(DOSSIER_EXPORTS / "comptages.csv", index=False)

    # --- export par domaine (domaines d'au moins 10 000 notices) ---
    df_domaines = pd.DataFrame(
        {
            "domaine": d,
            "notices_total": domaine_total[d],
            "notices_doute": domaine_doute[d],
            "taux_doute": round(domaine_doute[d] / domaine_total[d], 5),
        }
        for d in domaine_total if domaine_total[d] >= 10_000
    ).sort_values("taux_doute", ascending=False)
    df_domaines.to_csv(DOSSIER_EXPORTS / "comptages_domaines.csv", index=False)

    # --- rapport console ---
    def pct(n, d):
        return f"{n / d:6.2%}"

    print(f"Notices : {total:,} — dont Auteur renseigné : {total_auteur:,}".replace(",", " "))
    print(f"\nAu moins un marqueur de DOUTE : {doute['toutes']:,} "
          f"({pct(doute['toutes'], total)} de la base ; "
          f"{pct(doute['auteur'], total_auteur)} des notices avec auteur)".replace(",", " "))
    print(f"Périmètre peinture/dessin/sculpture/estampe : "
          f"{doute['perimetre_doute']:,} notices avec doute sur "
          f"{doute['perimetre_total']:,} ({pct(doute['perimetre_doute'], doute['perimetre_total'])})".replace(",", " "))

    print("\nPar famille (taux : toutes notices | notices avec auteur) :")
    for _, r in df_familles.iterrows():
        marque = " [suspect]" if r["suspect"] else ""
        print(f"  {r['categorie']:<9} {r['libelle']:<38} {r['notices']:>8,}"
              f"  {r['taux_toutes_notices']:8.3%} | {r['taux_auteur_renseigne']:8.3%}{marque}".replace(",", " "))

    print("\nTaux de doute par domaine (≥ 10 000 notices) :")
    for _, r in df_domaines.head(15).iterrows():
        print(f"  {r['domaine']:<35} {r['notices_doute']:>7,}/{r['notices_total']:>9,}"
              f"  {r['taux_doute']:6.2%}".replace(",", " "))

    print("\nExemples par famille (champ Auteur → Précisions) :")
    for famille in markers.FAMILLES:
        print(f"  · {famille.libelle} :")
        for ligne in exemples[famille.code]:
            auteur = str(ligne["Auteur"])[:60]
            paut = str(ligne["Precisions_sur_l_auteur"])[:50]
            print(f"      {ligne['Reference']} | {auteur} | {paut}")

    print(f"\n→ exports : {DOSSIER_EXPORTS / 'comptages.csv'} et comptages_domaines.csv")


if __name__ == "__main__":
    main()
