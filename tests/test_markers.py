"""Tests du lexique — construits sur les verdicts de la vérification manuelle T4.

Chaque cas vient d'une notice réelle jugée par l'utilisateur (2026-07-04).
Toute modification de src/markers.py doit repasser devant ces verdicts :
c'est le contrat entre le lexique et la vérification humaine.

Usage : uv run pytest
"""

import sys
from pathlib import Path

import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
import markers  # noqa: E402

# (valeur du champ Auteur, code famille, détection attendue)
# Sauf mention contraire, Domaine = « peinture » (voir CAS_DOMAINE pour v2).
CAS_JUGES = [
    # --- atelier : le doute est un qualificatif, pas un nom (T5, 64 % de faux en v0)
    ("ATELIER DE LYON (atelier)", "atelier_de", False),
    ("Atelier de Pistillus", "atelier_de", False),
    ("ATELIER DU CENTRE DE LA GAULE (céramiste)", "atelier_de", False),
    ("Atelier du jubé de la cathédrale de Strasbourg", "atelier_de", False),
    ("Buquet (atelier, graveur);Lamy Godard Frères (imprimeur)", "atelier_de", False),
    ("Alphonse Giroux & Cie (-);Moulin (Atelier photographique) (-)", "atelier_de", False),
    ("COROT Jean-Baptiste Camille (atelier)", "atelier_de", True),
    ("ATELIER DE ROME (?);RAFFAELLI (?, atelier)", "atelier_de", True),
    # la forme « nom d'auteur » part en catégorie écartée, chiffrée à part
    ("Atelier de Pistillus", "atelier_nom", True),
    ("COROT Jean-Baptiste Camille (atelier)", "atelier_nom", False),
    # --- école : jamais les écoles nationales, même inversées (T5, 20 % de faux en v0)
    ("Hollande École de (École hollandaise) (-)", "ecole_de", False),
    ("Bartolozzi Francesco (1727-1815);Italie École de (École italienne) (-)", "ecole_de", False),
    ("école française", "ecole_de", False),
    ("PALMA Giovane (école);JACOPO NEGRETTI (dit, école)", "ecole_de", True),
    ("école de Rembrandt", "ecole_de", True),
    # --- ? : jamais les dates inconnues (T5, 16 % de faux en v0)
    ("Der Balian Sarkis (?-1996)", "point_interrogation", False),
    ("Aquaviva Oscar (19..-19..?)", "point_interrogation", False),
    ("Klein Martin M. (1...-?)", "point_interrogation", False),
    ("LESCHER (attribué, ?)", "point_interrogation", True),
    ("LOMBARD (?, attribué)", "point_interrogation", True),
    # --- doctrine : « (attribué, d'après) » = copie, sort du doute
    ("MASSARD Léopold;DUMONSTIER Daniel (attribué, d’après)", "attribue", False),
    ("TOMBEUR Jean-François (attribué)", "attribue", True),
    ("anonyme (attribué, attribué)", "attribue", True),
    # --- anciennement attribué ne compte pas comme attribué
    ("anciennement attribué à BOSSCHAERT Ambrosius", "attribue", False),
    ("anciennement attribué à BOSSCHAERT Ambrosius", "anciennement_attribue", True),
    # --- v2 : écoles-lieux consacrées écartées (arbitrage 2026-07-05)
    ("ECOLE DE FONTAINEBLEAU (verrier)", "ecole_de", False),
    ("ECOLE DE FONTAINEBLEAU (verrier)", "ecole_lieu", True),
    ("Abstraction;Nouvelle Ecole de Paris", "ecole_de", False),
    ("école de Rembrandt", "ecole_lieu", False),
]

# v2 : « atelier » n'est un doute qu'en beaux-arts (arbitrage 2026-07-05).
# (Auteur, Domaine, code famille, détection attendue)
CAS_DOMAINE = [
    ("COROT Jean-Baptiste Camille (atelier)", "peinture", "atelier_de", True),
    ("COROT Jean-Baptiste Camille (atelier)", "peinture", "atelier_hors_beaux_arts", False),
    ("MINELLE (atelier)", "tabletterie;ethnologie", "atelier_de", False),
    ("MINELLE (atelier)", "tabletterie;ethnologie", "atelier_hors_beaux_arts", True),
    ("Vignier Henri (atelier)", "céramique;ethnologie", "atelier_de", False),
    # multivalué : un domaine beaux-arts suffit
    ("DUPONT (atelier)", "peinture;ethnologie", "atelier_de", True),
]


def _detecter(valeur, domaine="peinture"):
    df = pd.DataFrame({
        "Auteur": [valeur],
        "Precisions_sur_l_auteur": [None],
        "Ancienne_attribution": [None],
        "Ecole_pays": [None],
        "Domaine": [domaine],
    })
    return markers.detections(df)


@pytest.mark.parametrize("valeur,code,attendu", CAS_JUGES)
def test_cas_juge(valeur, code, attendu):
    assert bool(_detecter(valeur).loc[0, code]) == attendu


@pytest.mark.parametrize("valeur,domaine,code,attendu", CAS_DOMAINE)
def test_cas_domaine(valeur, domaine, code, attendu):
    assert bool(_detecter(valeur, domaine).loc[0, code]) == attendu
