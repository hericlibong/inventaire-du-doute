"""Assemblage des cas racontables → data/exports/web/cas.json (P2-T4).

Les cas sont curatés (choisis à la main, voir docs/cas.md). Ce script en fige
la version machine : il va chercher les notices Joconde réelles par référence
et produit un cas.json prêt pour le front. Le cas « Alençon » est absent de
Joconde — sa fiche est construite en dur, avec ses liens vers la base régionale.

Usage : uv run python src/build_cases.py  (~3 min : une passe sur le CSV)
"""

import json

import pandas as pd

from config import CHEMIN_CSV, DOSSIER_EXPORTS, URL_NOTICE_POP

DOSSIER_WEB = DOSSIER_EXPORTS / "web"

# Références Joconde à embarquer, par cas (curation manuelle, docs/cas.md).
REFS_PAR_CAS = {
    "nice_barla": ["70500001179"],
    "besancon_gericault": ["M0332014262", "M0332013239"],
    "louvre_clouet": ["000PE000505", "000PE000509"],
}
TOUTES_REFS = {r for refs in REFS_PAR_CAS.values() for r in refs}

COLS = ["Reference", "Auteur", "Titre", "Ancienne_attribution", "Domaine",
        "Nom_officiel_musee", "Ville"]


def notice(r: pd.Series) -> dict:
    def val(x):
        return x if isinstance(x, str) else None
    return {
        "reference": r["Reference"],
        "titre": val(r["Titre"]),
        "auteur": val(r["Auteur"]),
        "ancienne_attribution": val(r["Ancienne_attribution"]),
        "musee": val(r["Nom_officiel_musee"]),
        "ville": val(r["Ville"]),
        "lien_pop": URL_NOTICE_POP.format(reference=r["Reference"]),
    }


def main() -> None:
    # 1. récupérer les notices Joconde curatées
    trouve = {}
    for m in pd.read_csv(CHEMIN_CSV, sep="|", usecols=COLS, dtype=str,
                         chunksize=200_000):
        for _, r in m[m["Reference"].isin(TOUTES_REFS)].iterrows():
            trouve[r["Reference"]] = notice(r)
    manquantes = TOUTES_REFS - trouve.keys()
    if manquantes:
        raise SystemExit(f"Références introuvables dans le CSV : {manquantes}")

    def notices(cas):
        return [trouve[ref] for ref in REFS_PAR_CAS[cas]]

    # 2. assembler les cas dans l'ordre du récit
    cas = [
        {
            "id": "alencon_absent",
            "ordre": 1,
            "titre_court": "Alençon, l'absent",
            "angle": "Le cas qui a inspiré ce projet est invisible dans "
                     "l'inventaire national : Alençon n'a versé que sa dentelle.",
            "statut_donnee": "absent_de_joconde",
            "musee": "musée des beaux-arts et de la dentelle",
            "ville": "Alençon",
            "notices": [],
            "liens_externes": [
                {"libelle": "« tête de gorgone » (base régionale Normandie)",
                 "url": "https://collections.musees-normandie.fr/ark:/16418/mbd1160142"},
                {"libelle": "« le naufragé » (base régionale Normandie)",
                 "url": "https://collections.musees-normandie.fr/ark:/16418/mbd1160140"},
            ],
        },
        {
            "id": "nice_barla",
            "ordre": 2,
            "titre_court": "Nice, le doute industriel",
            "angle": "5 791 notices « attribué à », un seul dessinateur (Barla) : "
                     "23,6 % du doute national tient à un geste de catalogage en série.",
            "statut_donnee": "joconde",
            "musee": "muséum d'histoire naturelle",
            "ville": "Nice",
            "notices": notices("nice_barla"),
        },
        {
            "id": "besancon_gericault",
            "ordre": 3,
            "titre_court": "Besançon, le doute qui existe vraiment",
            "angle": "Autour du Radeau de la Méduse, un même fonds montre toute "
                     "l'échelle : « Géricault » d'un côté, « Géricault (attribué à) » de l'autre.",
            "statut_donnee": "joconde",
            "musee": "musée des beaux-arts et d'archéologie",
            "ville": "Besançon",
            "notices": notices("besancon_gericault"),
        },
        {
            "id": "louvre_clouet",
            "ordre": 4,
            "titre_court": "Le Louvre, l'archéologie d'un doute",
            "angle": "Le champ « ancienne attribution » se lit comme un journal "
                     "d'avis savants datés : l'attribution est une histoire, pas un verdict.",
            "statut_donnee": "joconde",
            "musee": "musée du Louvre",
            "ville": "Paris",
            "notices": notices("louvre_clouet"),
        },
    ]

    DOSSIER_WEB.mkdir(parents=True, exist_ok=True)
    (DOSSIER_WEB / "cas.json").write_text(
        json.dumps(cas, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{len(cas)} cas écrits dans {DOSSIER_WEB / 'cas.json'}")
    for c in cas:
        print(f"  {c['ordre']}. {c['titre_court']} — {len(c['notices'])} notice(s)")


if __name__ == "__main__":
    main()
