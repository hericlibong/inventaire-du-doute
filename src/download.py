"""Téléchargement des ressources du jeu de données Joconde.

Récupère dans data/raw/ :
- le CSV complet (~1,1 Go) — la matière de référence du projet ;
- la nomenclature ODS qui décrit les champs.

Un fichier déjà présent n'est pas retéléchargé (supprimer le fichier pour forcer).
Usage : uv run python src/download.py
"""

import sys

import requests

from config import CHEMIN_CSV, CHEMIN_NOMENCLATURE, URL_CSV, URL_NOMENCLATURE

BLOC = 1024 * 1024  # lecture par blocs de 1 Mo


def telecharger(url: str, destination) -> None:
    """Télécharge `url` vers `destination` en flux, avec progression sommaire."""
    if destination.exists():
        taille_mo = destination.stat().st_size / BLOC
        print(f"déjà présent : {destination.name} ({taille_mo:.0f} Mo) — ignoré")
        return

    print(f"téléchargement de {destination.name}…")
    provisoire = destination.with_suffix(destination.suffix + ".part")
    reponse = requests.get(url, stream=True, timeout=60)
    reponse.raise_for_status()

    recu = 0
    with open(provisoire, "wb") as fichier:
        for bloc in reponse.iter_content(chunk_size=BLOC):
            fichier.write(bloc)
            recu += len(bloc)
            print(f"\r  {recu / BLOC:.0f} Mo reçus", end="", flush=True)
    print()

    # On ne renomme qu'à la fin : pas de fichier tronqué en cas d'interruption.
    provisoire.rename(destination)
    print(f"  → {destination}")


def main() -> None:
    CHEMIN_CSV.parent.mkdir(parents=True, exist_ok=True)
    telecharger(URL_NOMENCLATURE, CHEMIN_NOMENCLATURE)
    telecharger(URL_CSV, CHEMIN_CSV)


if __name__ == "__main__":
    sys.exit(main())
