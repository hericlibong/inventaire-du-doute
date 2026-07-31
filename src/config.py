"""Chemins et URLs du projet — source unique de vérité pour tous les scripts."""

from pathlib import Path

# Racine du projet (parent de src/)
RACINE = Path(__file__).resolve().parent.parent

DOSSIER_RAW = RACINE / "data" / "raw"
DOSSIER_EXPORTS = RACINE / "data" / "exports"

# Jeu de données « Collections des musées de France : base Joconde »
# https://www.data.gouv.fr/fr/datasets/collections-des-musees-de-france-base-joconde/
# Licence Ouverte 2.0 — CSV mis à jour tous les mercredis à 6h00.
URL_CSV = "https://www.data.gouv.fr/api/1/datasets/r/7e3307c2-f2ff-455c-bbca-bb6f11aec7bb"
URL_NOMENCLATURE = "https://www.data.gouv.fr/api/1/datasets/r/2a7f0292-5a9e-47fe-8a11-168158c40617"

CHEMIN_CSV = DOSSIER_RAW / "joconde.csv"
CHEMIN_NOMENCLATURE = DOSSIER_RAW / "nomenclature.ods"


def chemin_releve(fichier: Path) -> Path:
    """Fichier voisin où `download.py` note ce que le serveur a répondu (date de
    version, empreinte, taille). Il voyage avec le téléchargement, jamais dans
    le code : c'est ce qui permet de dater les chiffres publiés sans recopier
    une valeur à la main."""
    return fichier.with_suffix(fichier.suffix + ".releve.json")

# API du portail du ministère (Opendatasoft). Attention : c'est un EXTRAIT
# (~721 000 notices), utile pour les contre-vérifications, pas comme référence.
URL_API = (
    "https://data.culture.gouv.fr/api/explore/v2.1"
    "/catalog/datasets/base-joconde-extrait/records"
)

# Gabarit du lien vers la notice publique sur POP (plateforme ouverte du patrimoine)
URL_NOTICE_POP = "https://pop.culture.gouv.fr/notice/joconde/{reference}"
