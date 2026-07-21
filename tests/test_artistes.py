"""Tests du rattachement des maîtres — figés sur l'audit du 2026-07-21.

Deux niveaux, comme pour les révisions :
1. des cas UNITAIRES explicites, lisibles sans le CSV, qui figent les deux
   règles de comptage (une référence = un poids ; catégorie la plus prudente,
   famille la plus explicite) ;
2. une vérification sur des RÉFÉRENCES RÉELLES de la base
   (data/exports/temoins_maitres.csv) : chaque témoin d'homonymie relevé par
   l'audit, chaque doublon de graphie, avec le verdict attendu.

Le CSV source (1,1 Go) n'est pas nécessaire : les témoins sont versionnés.

Usage : uv run pytest
"""

import csv
import sys
from pathlib import Path

import pytest

RACINE = Path(__file__).parent.parent
sys.path.insert(0, str(RACINE / "src"))
import markers  # noqa: E402
from build_artistes import (_pivot, _trouve_maitre,  # noqa: E402
                            resout_reference)

TEMOINS = RACINE / "data" / "exports" / "temoins_maitres.csv"


# --------------------------------------------------------------------------
# 1. Identité : qui se cache derrière un nom (temps 2)
# --------------------------------------------------------------------------

# (segment du champ Auteur, maître attendu ou None, motif)
CAS_IDENTITE = [
    # --- l'ancre « ^ » : le nom du maître doit être en tête (Joconde : NOM Prénom)
    ("BUONARROTI Michelangelo", "Michel-Ange", "le maître"),
    ("MICHEL-ANGE (dit)", "Michel-Ange", "sa graphie courte"),
    ("Corneille Michel-Ange (1642-1708)", None, "Michel-Ange en prénom"),
    ("CERQUOZZI Michelangelo (attribué)", None, "Michelangelo en prénom"),
    ("MERISI Michelangelo (école)", None, "Le Caravage"),
    ("MICHELANGELO DI PIETRO MEMBRINI", None, "Membrini, malgré le nom en tête"),
    ("RAPHAEL (dit)", "Raphaël", "le maître"),
    ("SANTI Raffaello (atelier)", "Raphaël", "sa forme d'état civil, longtemps oubliée"),
    ("SANZIO Raffaello", "Raphaël", "son autre forme d'état civil"),
    ("COLLIN Raphaël", None, "Raphaël en prénom"),
    ("MENGS Anton Raphael", None, "Raphaël en deuxième prénom"),
    ("SANZIO Giovanni", None, "Giovanni Santi, le père"),
    ("POUSSIN Nicolas (attribué à)", "Nicolas Poussin", "le maître"),
    ("LEMAIRE-POUSSIN (dit)", None, "Jean Lemaire"),
    ("LAVALLEE-POUSSIN Etienne de (attribué)", None, "Lavallée-Poussin"),
    ("GASPARD POUSSIN", None, "Gaspard Dughet"),
    ("Madame Ingres (dessinateur)", None, "son épouse"),
    # --- l'ancre ne s'applique QUE là où elle est nécessaire
    ("ECOLE DE PRIMATICCIO", "Le Primatice", "121 références : le nom n'est pas en tête"),
    ("D'APRES CLOUET François", "François Clouet", "idem, formule en tête"),
    # --- exclusions nommées : l'homonyme porte pourtant le nom en tête
    ("ROBUSTI Domenico (attribué à)", None, "le fils du Tintoret"),
    ("ROBUSTI Jacopo (attribué à)", "Le Tintoret", "le père"),
    ("VECELLIO Francesco (attribué à)", None, "de la famille du Titien"),
    ("VECELLIO Tiziano (attribué à)", "Titien", "le maître"),
    ("CALIARI Carlo (attribué)", None, "le fils de Véronèse"),
    ("CALIARI Paolo", "Véronèse", "le maître"),
    ("MIGNARD Pierre II (peintre)", None, "le neveu"),
    ("Mignard Pierre I (1610-1695)", "Pierre Mignard", "le maître"),
    ("VOUET Aubin", None, "le frère"),
    ("VOUET Simon (?)", "Simon Vouet", "le maître"),
    ("DYCK Philip Van", None, "Philip van Dyck"),
    ("DYCK Antoon van (attribué à)", "Van Dyck", "le maître"),
    ("VINCI Pierino da (inspiré par)", None, "le neveu de Léonard"),
    ("VINCI Leonardo da", "Léonard de Vinci", "le maître"),
    ("RIBERA Y CIRERA Roman", None, "un autre Ribera"),
    ("RIBERA Jusepe de", "Ribera", "le maître"),
    # --- faux amis par racine commune, corrigés le 2026-07-13 : ne pas revenir en arrière
    ("SERODINE Giovanni", None, "contient « rodin »"),
    ("VINCIDOR Tommaso", None, "contient « vinci »"),
    ("TINTORETTO Domenico", None, "contient « tintoret »"),
]


@pytest.mark.parametrize("segment,attendu,motif", CAS_IDENTITE)
def test_identite(segment, attendu, motif):
    assert _trouve_maitre(_pivot(segment)) == attendu, motif


# --------------------------------------------------------------------------
# 2. Comptage : une référence, un poids (temps 1)
# --------------------------------------------------------------------------

# (champ Auteur, maître, catégorie attendue, famille attendue, motif)
CAS_COMPTAGE = [
    ("VECELLIO Tiziano (attribué à);LE TITIEN (dit, attribué à)",
     "Titien", "doute", "attribue",
     "deux graphies du même homme : la notice ne pèse qu'une fois"),
    ("VOUET Simon (?);VOUET Simon (atelier, dessinateur)",
     "Simon Vouet", "doute", "point_interrogation",
     "deux formulations prudentes : le « ? » l'emporte (arbitrage 2026-07-21)"),
    ("BUONARROTI Michelangelo (école);MICHEL-ANGE (dit)",
     "Michel-Ange", "doute", "ecole_de",
     "prudent et ferme sur la même notice : le prudent l'emporte"),
    ("POUSSIN Nicolas (attribué à);POUSSIN Nicolas (d'après)",
     "Nicolas Poussin", "doute", "attribue",
     "prudent et copie : le prudent l'emporte"),
    ("MICHEL-ANGE (dit, d'après);BUONARROTI Michelangelo (d'après)",
     "Michel-Ange", "copie", None,
     "copie et attribution ferme : la copie l'emporte sur le ferme"),
    ("RENI Guido", "Guido Reni", "propre", None, "attribution ferme simple"),
]


@pytest.mark.parametrize("auteur,maitre,categorie,famille,motif", CAS_COMPTAGE)
def test_comptage(auteur, maitre, categorie, famille, motif):
    resolu = resout_reference(auteur)
    assert maitre in resolu, motif
    assert resolu[maitre][0] == categorie, motif
    assert resolu[maitre][1] == famille, motif


def test_une_notice_peut_nommer_deux_maitres():
    """Le poids est par COUPLE (maître, référence), pas par notice : une notice
    qui nomme deux maîtres compte une fois pour chacun."""
    resolu = resout_reference("BUONARROTI Michelangelo (?);SARTO Andrea del (?, manière de)")
    assert set(resolu) == {"Michel-Ange", "Andrea del Sarto"}
    assert all(v[0] == "doute" for v in resolu.values())


def test_une_famille_par_maitre_et_par_reference():
    """Invariant qui rend familles et niveaux additifs : quelles que soient les
    formules portées par la notice, un maître n'y relève que d'une famille."""
    resolu = resout_reference(
        "VOUET Simon (?);VOUET Simon (atelier, dessinateur);VOUET Simon (école)")
    assert len(resolu) == 1
    assert resolu["Simon Vouet"][1] == "point_interrogation"


# --------------------------------------------------------------------------
# 3. Références réelles de la base (témoins de l'audit)
# --------------------------------------------------------------------------

def _temoins():
    with open(TEMOINS, encoding="utf-8") as f:
        return list(csv.DictReader(f, delimiter="|"))


@pytest.mark.parametrize("ligne", _temoins(),
                         ids=lambda l: f"{l['Reference']}-{l['maitre_attendu'] or 'ecarte'}")
def test_reference_reelle(ligne):
    """Chaque témoin cité par l'audit, avec la valeur exacte de son champ Auteur."""
    resolu = resout_reference(ligne["Auteur"],
                              markers._dans_beaux_arts(ligne["Domaine"]))
    attendu = ligne["maitre_attendu"]
    if not attendu:
        # aucun maître ne doit être rattaché — sauf ceux qu'une autre ligne du
        # fichier revendique explicitement pour cette même référence
        revendiques = {l["maitre_attendu"] for l in _temoins()
                       if l["Reference"] == ligne["Reference"] and l["maitre_attendu"]}
        assert set(resolu) <= revendiques, f"{ligne['motif']} → {sorted(resolu)}"
        return
    assert attendu in resolu, ligne["motif"]
    categorie, famille, _ = resolu[attendu]
    assert categorie == ligne["categorie_attendue"], ligne["motif"]
    assert famille == (ligne["famille_attendue"] or None), ligne["motif"]
