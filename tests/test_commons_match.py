"""Tests de l'appariement Commons/Wikidata et du classement des droits
(chantier reproductions ouvertes, 2026-07-29).

Couvre les sept cas exigés par le cahier des charges : match par identifiant
Joconde, match par inventaire, deux œuvres de même titre mais d'inventaires
différents, image ouverte / restreinte / inconnue, et l'impossibilité de valider
un rapprochement fondé seulement sur titre + auteur + musée.

Usage : uv run pytest tests/test_commons_match.py
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
from commons_match import (A_VERIFIER, EXACT, M_INVENTORY, M_JOCONDE,  # noqa: E402
                           OPEN, REJETE, RESTRICTED, UNKNOWN,
                           classer_droits_commons, decider_match,
                           dimensions_concordent, parser_dimensions, retenable)

# Notice Joconde de référence (Charles IX, atelier de Clouet, Louvre).
META = {
    "numero_inventaire": "INV 3253",
    "titre": "Charles IX (1550-1574), roi de France",
    "auteur": "CLOUET François (atelier)",
    "musee": "musée du Louvre",
}


# --- 1. Correspondance par identifiant Joconde → EXACT -----------------------
def test_match_par_identifiant_joconde():
    cand = {"joconde_ids": ["000PE000514"], "inventaire": ["INV 3253"],
            "collection": ["département des peintures du musée du Louvre"]}
    statut, methode, ev = decider_match("000PE000514", META, cand)
    assert statut == EXACT and methode == M_JOCONDE
    assert ev.get("joconde_id_match") is True


# --- 2. Correspondance par numéro d'inventaire → A_VERIFIER (candidat) --------
def test_match_par_inventaire_est_candidat():
    cand = {"joconde_ids": [], "inventaire": ["INV 3253"],
            "collection": ["musée du Louvre"]}
    statut, methode, ev = decider_match("000PE000514", META, cand)
    assert statut == A_VERIFIER and methode == M_INVENTORY
    assert ev.get("inventory_match") and ev.get("institution_match")


# --- 3. Même titre mais inventaires différents → PAS une correspondance -------
def test_meme_titre_inventaires_differents_non_valide():
    # une autre œuvre, même titre et même musée, mais un autre numéro d'inventaire
    autre = {"joconde_ids": [], "inventaire": ["INV 9999"],
             "collection": ["musée du Louvre"], "titre": META["titre"],
             "auteur": META["auteur"]}
    statut, methode, ev = decider_match("000PE000514", META, autre)
    assert statut == REJETE
    assert not ev.get("inventory_match")


# --- 3 bis. Même inventaire mais AUTRE institution → faux rapprochement -------
def test_meme_inventaire_autre_institution_rejete():
    # un autre musée porte par coïncidence le même numéro d'inventaire
    autre = {"joconde_ids": [], "inventaire": ["INV 3253"],
             "collection": ["musée des beaux-arts de Lyon"]}
    statut, methode, ev = decider_match("000PE000514", META, autre)
    assert statut == REJETE
    assert ev.get("inventory_match") and not ev.get("institution_match")


# --- 7. Titre + auteur + musée seuls → jamais validé automatiquement ----------
def test_titre_auteur_musee_seuls_ne_valident_jamais():
    cand = {"joconde_ids": [], "inventaire": [], "collection": ["musée du Louvre"],
            "titre": META["titre"], "auteur": META["auteur"]}
    statut, methode, ev = decider_match("000PE000514", META, cand)
    assert statut == REJETE
    # des preuves faibles peuvent exister, mais ne suffisent pas
    assert "joconde_id_match" not in ev and not ev.get("inventory_match")


# --- Vérification des candidats par les dimensions ---------------------------
@pytest.mark.parametrize("mesures,attendu", [
    ("31.5 H ; 17 L", (31.5, 17.0)),
    ("H. 76.5, L. 102", (76.5, 102.0)),
    ("99 H ; 82.5 L", (99.0, 82.5)),
    ("H. en m 0,183 ; L. en m 0,120", (18.3, 12.0)),   # mètres → cm
    ("64", (None, None)),                              # illisible
    ("", (None, None)),
])
def test_parser_dimensions(mesures, attendu):
    assert parser_dimensions(mesures) == attendu


def test_dimensions_concordent():
    assert dimensions_concordent(76.5, 102, 76.5, 102) is True
    assert dimensions_concordent(76.5, 102, 77, 101.5) is True     # ±5 %
    assert dimensions_concordent(76.5, 102, 64, 54) is False       # autre objet
    assert dimensions_concordent(76.5, 102, None, 102) is None     # inconnu


def test_candidat_dimensions_concordantes_reste_a_verifier():
    # dimensions concordantes = présomption, PAS confirmation : deux objets d'un
    # même numéro d'inventaire peuvent coïncider en taille. Contrôle humain requis.
    cand = {"inventaire": ["313"], "collection": ["musée des beaux-arts de Rennes"],
            "h": 76.5, "w": 102.0, "titre": "Paysage animé"}
    meta = {"numero_inventaire": "313", "musee": "musée des beaux-arts",
            "titre": "Paysage animé", "dimensions": "H. 76.5, L. 102"}
    statut, methode, ev = decider_match("00000000000", meta, cand)
    assert statut == A_VERIFIER and methode == M_INVENTORY
    assert ev.get("dimensions_match")  # l'évidence est conservée pour le tri


def test_aucun_candidat_inventaire_n_est_exact_automatiquement():
    # seule la correspondance par identifiant Joconde peut être exacte en auto
    cand = {"inventaire": ["313"], "collection": ["musée des beaux-arts de Rennes"],
            "h": 76.5, "w": 102.0, "titre": "Paysage animé", "joconde_ids": []}
    meta = {"numero_inventaire": "313", "musee": "musée des beaux-arts",
            "titre": "Paysage animé", "dimensions": "H. 76.5, L. 102"}
    assert decider_match("00000000000", meta, cand)[0] != EXACT


def test_candidat_dimensions_incompatibles_rejete():
    # même inventaire + institution générique, mais dimensions d'un autre objet
    cand = {"inventaire": ["313"], "collection": ["musée des beaux-arts"],
            "h": 300.0, "w": 200.0}
    meta = {"numero_inventaire": "313", "musee": "musée des beaux-arts",
            "dimensions": "H. 76.5, L. 102"}
    statut, methode, ev = decider_match("00000000000", meta, cand)
    assert statut == REJETE and ev.get("dimensions_conflit")


def test_candidat_sans_dimensions_reste_a_verifier():
    cand = {"inventaire": ["313"], "collection": ["musée des beaux-arts"]}
    meta = {"numero_inventaire": "313", "musee": "musée des beaux-arts",
            "dimensions": "H. 76.5, L. 102"}
    statut, methode, ev = decider_match("00000000000", meta, cand)
    assert statut == A_VERIFIER


# --- 4/5/6. Droits du fichier Commons ----------------------------------------
def test_image_ouverte():
    for court, code in [("Public domain", "pd"), ("CC0", "cc0"),
                        ("CC BY 4.0", "cc-by-4.0"), ("CC BY-SA 4.0", "cc-by-sa-4.0"),
                        ("PDM 1.0", "")]:
        assert classer_droits_commons(court, code)[0] == OPEN, court


def test_image_restreinte_nc_nd_pas_ouverte():
    for court, code in [("CC BY-NC 4.0", "cc-by-nc-4.0"),
                        ("CC BY-ND 4.0", "cc-by-nd-4.0"),
                        ("CC BY-NC-SA 3.0", "cc-by-nc-sa-3.0")]:
        assert classer_droits_commons(court, code)[0] != OPEN, court


def test_image_statut_inconnu():
    # un fichier sans licence reconnue (ex. crédit seul) reste inconnu
    assert classer_droits_commons("", "")[0] == UNKNOWN
    assert classer_droits_commons("© Musée X", "")[0] == UNKNOWN


# --- Règle de rétention ------------------------------------------------------
def test_retenable_exige_exact_et_ouvert():
    assert retenable(EXACT, OPEN) is True
    assert retenable(A_VERIFIER, OPEN) is False   # candidat non retenu
    assert retenable(EXACT, UNKNOWN) is False      # droits non ouverts
    assert retenable(REJETE, OPEN) is False
