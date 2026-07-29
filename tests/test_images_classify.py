"""Tests du classement des droits photo (chantier vignettes, 2026-07-29).

Les quatre premiers cas sont exigés par le cahier des charges, avec les
crédits RÉELS relevés sur POP le 2026-07-29 (champ PHOT). Les suivants figent
les règles de prudence : restriction > ouvert, CC BY-NC/ND à examiner, © seul
insuffisant, domaine public de l'œuvre sans effet sur la photo.

Usage : uv run pytest tests/test_images_classify.py
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
from images_classify import (OPEN, RESTRICTED, UNKNOWN, UNAVAILABLE,  # noqa: E402
                             classer)


# --- Les quatre cas exigés (PHOT réel relevé sur POP le 2026-07-29) ----------
CAS_EXIGES = [
    ("05630000005", "© Jean-François Peiré#Licence Ouverte/Etalab", OPEN, "Licence Ouverte/Etalab"),
    ("05630000453", "Marie-Laure Le Brazidec CC BY-SA", OPEN, "CC BY-SA"),
    ("00000104589", "Réunion des musées nationaux - utilisation soumise à autorisation", RESTRICTED, None),
    ("000PE018162", "RMN-Grand Palais", UNKNOWN, None),
]


@pytest.mark.parametrize("ref,phot,statut,licence", CAS_EXIGES)
def test_cas_exiges(ref, phot, statut, licence):
    s, lic, credit, raison = classer(phot)
    assert s == statut, f"{ref} : {s} attendu {statut} ({raison})"
    if licence is not None:
        assert lic == licence, f"{ref} : licence {lic!r} attendu {licence!r}"
    assert credit == phot.strip()


# --- Règles de prudence ------------------------------------------------------

def test_restriction_l_emporte_sur_ouvert():
    # une mention ouverte NE sauve PAS une restriction explicite
    s, *_ = classer("Licence Ouverte / Etalab - utilisation soumise à autorisation")
    assert s == RESTRICTED


def test_adagp_restreint():
    assert classer("© ADAGP, Paris")[0] == RESTRICTED
    assert classer("© Musée X ; droits réservés")[0] == RESTRICTED


@pytest.mark.parametrize("phot", [
    "CC BY-NC", "CC BY-ND", "CC BY-NC-SA", "CC BY-NC-ND", "cc by-nc 4.0",
])
def test_cc_by_nc_nd_a_examiner_jamais_open(phot):
    s, lic, *_ = classer(phot)
    assert s == UNKNOWN, f"{phot} ne doit pas être open"


@pytest.mark.parametrize("phot,licence", [
    ("CC BY", "CC BY"),
    ("CC BY-SA", "CC BY-SA"),
    ("cc0", "CC0"),
    ("Licence Ouverte", "Licence Ouverte"),
    ("Etalab 2.0", "Etalab 2.0"),
])
def test_licences_ouvertes(phot, licence):
    s, lic, *_ = classer(phot)
    assert s == OPEN and lic == licence


def test_copyright_ou_nom_seul_est_unknown():
    # un © ou un nom de photographe n'est pas une licence
    assert classer("© Musée du Louvre / Dist. RMN-Grand Palais")[0] == UNKNOWN
    assert classer("Photographe : Jean Dupont")[0] == UNKNOWN


def test_credit_vide_est_unknown_si_image():
    assert classer("", presence_image=True)[0] == UNKNOWN


def test_pas_d_image_est_unavailable():
    # même avec une licence dans le champ, sans image il n'y a rien à montrer
    assert classer("Licence Ouverte", presence_image=False)[0] == UNAVAILABLE


def test_artiste_sous_droits_restreint():
    # le champ Joconde « Artiste sous droits » suffit à restreindre
    assert classer("© Musée X", artiste_sous_droits="oui")[0] == RESTRICTED


def test_authorized_jamais_automatique():
    # aucun chemin ne renvoie 'authorized' : c'est une décision manuelle
    from images_classify import AUTHORIZED
    echantillons = ["", "© X", "CC BY", "ADAGP", "Licence Ouverte", "RMN"]
    assert all(classer(p)[0] != AUTHORIZED for p in echantillons)
