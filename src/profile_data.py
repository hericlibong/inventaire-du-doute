"""Profilage du CSV Joconde complet (T2).

Parcourt le CSV par morceaux et produit :
- le nombre réel de notices (à comparer aux annonces des portails) ;
- le taux de remplissage des champs liés à l'auteur ;
- la répartition des notices par domaine (champ multivalué) ;
- le nombre de musées et de notices géolocalisées.

Résultats affichés en console et exportés dans data/exports/profil.txt.
Usage : uv run python src/profile_data.py  (~1 à 2 min sur le CSV de 1,2 Go)
"""

from collections import Counter

import pandas as pd

from config import CHEMIN_CSV, DOSSIER_EXPORTS

# Colonnes lues (sur les 67 du CSV) : cœur de la détection + contexte.
COLONNES = [
    "Reference",
    "Auteur",
    "Precisions_sur_l_auteur",
    "Ancienne_attribution",
    "Ecole_pays",
    "Domaine",
    "Denomination",
    "Nom_officiel_musee",
    "Code_Museofile",
    "coordonnees",
]

# Domaines servant à discuter le périmètre (comparés en minuscules).
DOMAINES_PERIMETRE = ["peinture", "dessin", "sculpture", "estampe"]

TAILLE_MORCEAU = 200_000


def profiler() -> str:
    """Parcourt le CSV et renvoie le rapport de profilage (texte)."""
    total = 0
    non_vides = Counter()  # champ -> nb de notices renseignées
    domaines = Counter()  # domaine (minuscule) -> nb de notices
    nb_domaines_perimetre = 0  # notices dont un domaine est dans DOMAINES_PERIMETRE
    musees = set()

    morceaux = pd.read_csv(
        CHEMIN_CSV, sep="|", usecols=COLONNES, dtype=str, chunksize=TAILLE_MORCEAU
    )
    for morceau in morceaux:
        total += len(morceau)
        for champ in COLONNES[1:]:
            non_vides[champ] += morceau[champ].notna().sum()
        musees.update(morceau["Code_Museofile"].dropna().unique())

        # Domaine est multivalué (séparateur ;) : une notice compte une fois
        # par domaine dans la répartition, une seule fois pour le périmètre.
        listes = (
            morceau["Domaine"].fillna("(sans domaine)").str.lower().str.split(";")
        )
        for liste in listes:
            domaines.update(set(d.strip() for d in liste))
            if any(d.strip() in DOMAINES_PERIMETRE for d in liste):
                nb_domaines_perimetre += 1

        print(f"\r  {total:,} notices lues".replace(",", " "), end="", flush=True)
    print()

    lignes = [
        f"Notices au total : {total:,}".replace(",", " "),
        f"Musées distincts (Code_Museofile) : {len(musees):,}".replace(",", " "),
        "",
        "Taux de remplissage des champs lus :",
    ]
    for champ in COLONNES[1:]:
        n = non_vides[champ]
        lignes.append(f"  {champ:<28} {n:>9,} ({n / total:5.1%})".replace(",", " "))

    lignes += [
        "",
        f"Notices avec au moins un domaine du périmètre pressenti "
        f"{DOMAINES_PERIMETRE} : {nb_domaines_perimetre:,} "
        f"({nb_domaines_perimetre / total:.1%})".replace(",", " "),
        "",
        "Domaines les plus fréquents (une notice peut en porter plusieurs) :",
    ]
    for domaine, n in domaines.most_common(25):
        lignes.append(f"  {domaine:<35} {n:>9,}".replace(",", " "))

    return "\n".join(lignes)


def main() -> None:
    rapport = profiler()
    print()
    print(rapport)
    DOSSIER_EXPORTS.mkdir(parents=True, exist_ok=True)
    (DOSSIER_EXPORTS / "profil.txt").write_text(rapport + "\n", encoding="utf-8")
    print(f"\n→ rapport écrit dans {DOSSIER_EXPORTS / 'profil.txt'}")


if __name__ == "__main__":
    main()
