"""Téléchargement des ressources du jeu de données Joconde.

Récupère dans data/raw/ :
- le CSV complet (~1,1 Go) — la matière de référence du projet ;
- la nomenclature ODS qui décrit les champs.

Un fichier déjà présent n'est pas retéléchargé (supprimer le fichier pour forcer).
Usage : uv run python src/download.py
"""

import hashlib
import json
import sys
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime

import requests

from config import (
    CHEMIN_CSV,
    CHEMIN_NOMENCLATURE,
    URL_CSV,
    URL_NOMENCLATURE,
    chemin_releve,
)

BLOC = 1024 * 1024  # lecture par blocs de 1 Mo


def _date_version(reponse: requests.Response) -> str | None:
    """Date de la version servie (en-tête Last-Modified), au format AAAA-MM-JJ.

    C'est la date que le site affiche sous les chiffres : elle vient du serveur,
    jamais d'une saisie."""
    entete = reponse.headers.get("Last-Modified")
    if not entete:
        return None
    return parsedate_to_datetime(entete).date().isoformat()


def _ecrire_releve(destination, reponse: requests.Response, empreinte: str) -> None:
    """Note ce que le serveur a répondu, à côté du fichier téléchargé.

    Le relevé voyage avec la donnée : c'est lui qui permettra à
    `build_exports.py` de dater les exports sans qu'aucune valeur ne soit
    recopiée dans le code."""
    releve = {
        "url": reponse.url,
        "version_donnee": _date_version(reponse),
        "empreinte_md5": empreinte,
        "taille_octets": destination.stat().st_size,
        "telecharge_le": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }
    chemin_releve(destination).write_text(
        json.dumps(releve, ensure_ascii=False, indent=1) + "\n", encoding="utf-8"
    )


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
    somme = hashlib.md5()
    with open(provisoire, "wb") as fichier:
        for bloc in reponse.iter_content(chunk_size=BLOC):
            fichier.write(bloc)
            somme.update(bloc)
            recu += len(bloc)
            print(f"\r  {recu / BLOC:.0f} Mo reçus", end="", flush=True)
    print()

    # On ne renomme qu'à la fin : pas de fichier tronqué en cas d'interruption.
    provisoire.rename(destination)
    _ecrire_releve(destination, reponse, somme.hexdigest())
    print(f"  → {destination}")


def main() -> None:
    CHEMIN_CSV.parent.mkdir(parents=True, exist_ok=True)
    telecharger(URL_NOMENCLATURE, CHEMIN_NOMENCLATURE)
    telecharger(URL_CSV, CHEMIN_CSV)


if __name__ == "__main__":
    sys.exit(main())
