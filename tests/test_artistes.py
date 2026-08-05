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
import json
import sys
from collections import Counter
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
    # « Gaspard Poussin » n'est pas Nicolas (écarté par l'ancre) mais Gaspard
    # Dughet, son beau-frère — retenu à son propre nom au temps 5.
    ("GASPARD POUSSIN", "Gaspard Dughet", "Dughet dit Gaspard Poussin"),
    ("DUGHET Gaspard (dit) POUSSIN Gaspard", "Gaspard Dughet", "sa forme complète"),
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
    # --- lot du temps 5 (2026-07-22) : maîtres retenus et parents séparés
    ("BARBIERI Giovanni Francesco", "Le Guerchin", "Barbieri = Guercino = Guerchin"),
    ("GUERCINO Il", "Le Guerchin", "sa graphie italienne"),
    ("BOUCHARDON Edme", "Bouchardon", "le maître"),
    ("BOUCHARDON Jacques Philippe", None, "son frère"),
    ("ZUCCARO Federico", "Federico Zuccaro", "le maître"),
    ("ZUCCARO Taddeo", None, "son frère, 52 mentions certaines, séparé"),
    ("CHAMPAIGNE Philippe de", "Philippe de Champaigne", "le maître"),
    ("CHAMPAIGNE Jean-Baptiste de", None, "son neveu"),
    ("BOILLY Louis Léopold", "Louis Léopold Boilly", "le maître"),
    ("BOILLY Jules", None, "son fils lithographe"),
    ("BOILLY Julien Léopold", None, "le même fils, autre graphie"),
    ("TENIERS David II", "David Téniers", "le Jeune, le maître"),
    ("TENIERS David Ier, dit le Vieux", None, "son père"),
    ("TENIERS Abraham", None, "son frère"),
    ("GELLEE Claude", "Claude Lorrain", "Claude Gellée dit Le Lorrain"),
    ("FILIPEPI Alessandro Mariano", "Botticelli", "son état civil"),
    ("VANNUCCI Pietro", "Le Pérugin", "Pietro Vannucci dit Le Pérugin"),
    ("CORNEILLE DE LYON", "Corneille de Lyon", "distinct de Corneille Michel-Ange"),
    ("PIPPI Giulio", "Jules Romain", "Giulio Pippi dit Jules Romain"),
    ("JOYANT Jules Romain", None, "homonyme écarté"),

    # --- lot 2 (2026-08-02) : l'égalité stricte « = », le nom nu et rien d'autre
    ("David (1748-1825) (attribué à)", "Jacques-Louis David", "le maître"),
    ("DAVID Jacques-Louis", "Jacques-Louis David", "son état civil"),
    ("DAVID D'ANGERS Pierre-Jean", None, "le sculpteur, 1 363 mentions certaines"),
    ("DAVID Gérard (attribué à)", None, "le primitif flamand"),
    ("DAVID Jérôme (?)", None, "le graveur"),
    ("DAVID Michel-Antoine", None, "encore un autre"),
    ("TENIERS David (attribué à)", "David Téniers", "David en prénom, déjà retenu"),
    # --- lot 2 : les graphies rapprochées, vérifiées sur les dates du musée
    ("PINOT Charles François (dessinateur, attribué à)", "Charles François Pinot",
     "sa graphie longue"),
    ("PINOT Charles (dessinateur, attribué à)", "Charles François Pinot",
     "sa graphie courte, mêmes dates (1817-1874)"),
    ("IMAGERIE PINOT-SAGAIRE", None, "la raison sociale, pas l'homme"),
    ("Ensfelder Eugène (1836-1876) (attribué à)", "Charles Eugène Ensfelder",
     "« Eugène » et « Charles Eugène » ont les mêmes dates"),
    ("HOGENBERG Frans", "Frans Hogenberg", "sa graphie flamande"),
    ("HOGENBERG Nicolas", None, "un autre graveur de la famille"),
    ("COTER Colijn de", "Colijn de Coter", "l'ordre inverse du même nom"),
    # --- lot 2 : les parents séparés, jamais fusionnés
    ("DUTHOIT Louis (?)", "Louis Duthoit", "le frère cadet"),
    ("DUTHOIT Aimé (?)", "Aimé Duthoit", "le frère aîné"),
    ("PASSE Crispin I Van de (?, graveur)", "Crispin de Passe l'Ancien", "le père"),
    ("PASSE Crispin II Van de (?, graveur)", "Crispin de Passe le Jeune",
     "le fils : « I » ne capture pas « II »"),
    ("TURPIN DE CRISSE Lancelot Théodore Comte de (?)", "Turpin de Crissé",
     "le fils, retenu"),
    ("TURPIN DE CRISSE Père (?, dessinateur)", None,
     "le père, désigné par son seul rang de famille"),
    ("ALLEAUME Ludovic", None, "son frère"),
    ("POLLAIUOLO Piero", None, "son frère"),
    ("HUGO Charles (?)", "Charles Hugo", "le fils photographe"),
    ("HUGO Victor", None, "le père écrivain"),
    # --- lot 2 : ce qui n'est pas une personne, ou pas une personne nommée
    ("MELLET Jules Fils (?)", None, "atelier de famille, aucun prénom individualisant"),
    ("PELLERIN (imprimeur, éditeur, attribué à)", None, "l'imagerie d'Épinal"),
    ("MOGHOLE DE MURSHIDABAD (école)", None, "une école régionale"),
    ("PETER (attribué à)", None, "un nom sans prénom"),
    ("VARADY A (attribué à)", None, "un prénom réduit à une initiale"),
    ("BUQUET (atelier)", None, "un nom nu et un atelier"),
    ("Prévost (atelier)", None, "un nom nu et un atelier"),
    ("Barla Jean-Baptiste (1817-1896) (attribué à)", None,
     "identifié, mais hors du périmètre du volume (voir test_hors_perimetre)"),
    ("BARLA Antoinette", None, "une autre Barla"),
]


@pytest.mark.parametrize("segment,attendu,motif", CAS_IDENTITE)
def test_identite(segment, attendu, motif):
    assert _trouve_maitre(_pivot(segment)) == attendu, motif


# --------------------------------------------------------------------------
# 1 bis. Hors périmètre : identifié, compté, mais pas dans le volume
# --------------------------------------------------------------------------

def test_hors_perimetre_reste_identifie():
    """Une personne hors périmètre n'est PAS un faux positif : les exports du
    volume l'ignorent, le registre la retrouve et la compte (2026-08-02)."""
    from build_artistes import (HORS_PERIMETRE, MOTIF_HORS_PERIMETRE,
                                TOUTES_PERSONNES)
    segment = "Barla Jean-Baptiste (1817-1896) (attribué à)"
    assert _trouve_maitre(_pivot(segment)) is None, "absent du volume"
    assert _trouve_maitre(_pivot(segment), TOUTES_PERSONNES) == \
        "Jean-Baptiste Barla", "mais bien identifié par le registre"
    # chaque sortie de périmètre porte un motif publiable, comme les écarts
    assert all(m.strip() for m in MOTIF_HORS_PERIMETRE.values())
    assert len(HORS_PERIMETRE) == len(MOTIF_HORS_PERIMETRE)


def test_hors_perimetre_absent_de_la_table_du_volume():
    """Aucune personne hors périmètre ne doit se glisser dans MAITRES."""
    from build_artistes import MAITRES, MOTIF_HORS_PERIMETRE
    assert not {n for n, *_ in MAITRES} & set(MOTIF_HORS_PERIMETRE)


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

# --------------------------------------------------------------------------
# 4. Statuts du registre des candidats (temps 5)
# --------------------------------------------------------------------------

# (nom débarrassé de sa formule, mention réelle d'où il vient, statut attendu)
CAS_STATUT = [
    ("BARBIERI GIOVANNI FRANCESCO", "BARBIERI Giovanni Francesco (attribué à)",
     "retenu", "instruit au temps 5"),
    ("MANUFACTURE DE CREIL", "Manufacture de Creil (attribué à)",
     "écarté", "n'est pas une personne"),
    ("FULDA", "Manufacture de Fulda (attribué à)", "écarté",
     "le nom seul ne le dit pas, la mention si"),
    ("CARRACCI L'UN DES", "CARRACCI l'un des (attribué à)", "écarté",
     "mention collective"),
    ("A", "Attribué à", "écarté", "la mention ne porte aucun nom"),
    # --- instruits au lot 2 (2026-08-02) : la réponse est écrite, dans un sens
    # comme dans l'autre
    ("BARLA JEAN-BAPTISTE", "Barla Jean-Baptiste (1817-1896) (attribué à)",
     "hors périmètre", "identifié et compté, mais hors de l'angle du volume"),
    ("DAVID", "David (1748-1825) (attribué à)", "retenu",
     "Jacques-Louis David, pris par égalité stricte"),
    ("MELLET JULES FILS", "MELLET Jules Fils (?)", "écarté",
     "instruit puis écarté : les mêmes notices nomment les trois Mellet"),
    ("PELLERIN", "Pellerin (imprimeur, éditeur, attribué à)", "écarté",
     "instruit puis écarté : une raison sociale"),
    # celui-là reste OUVERT : rien dans les données ne permet de le retirer, et
    # il n'a pas encore été regardé
    ("CASTIGLIONE GIOVANNI BENEDETTO",
     "Castiglione Giovanni Benedetto (1609-1664) (attribué à)",
     "à instruire", "sous le seuil du lot 2, jamais examiné"),
]


@pytest.mark.parametrize("nom,mention,attendu,motif", CAS_STATUT)
def test_statut_registre(nom, mention, attendu, motif):
    """« à instruire » n'est jamais « écarté » : on ne retire un candidat que
    lorsqu'on a vérifié que ce n'est pas une personne (cadrage 2026-07-22)."""
    from registre_maitres import statut_forme
    assert statut_forme(nom, _pivot(mention))[0] == attendu, motif


# --------------------------------------------------------------------------
# 5. Recouvrement entre profils : somme ≠ union (mesuré le 2026-07-22)
# --------------------------------------------------------------------------

EXPORT = RACINE / "data" / "exports" / "web" / "artistes.json"


@pytest.fixture(scope="module")
def export():
    if not EXPORT.exists():
        pytest.skip("artistes.json non généré")
    return json.loads(EXPORT.read_text(encoding="utf-8"))


def test_somme_des_profils_egale_les_appartenances(export):
    t = export["totaux"]
    assert sum(a["doute"] for a in export["artistes"]) == t["appartenances_doute"]


def test_union_inferieure_ou_egale_a_la_somme(export):
    """Une notice qui nomme deux maîtres compte deux fois dans la somme des
    fiches, une seule fois dans les références distinctes."""
    t = export["totaux"]
    for cat in ("doute", "propre", "copie"):
        assert t[f"notices_{cat}"] <= t[f"appartenances_{cat}"], cat


def test_ecart_explique_par_les_references_partagees(export):
    """L'écart n'est pas une approximation : il vaut exactement le nombre de
    liens en trop portés par les notices à plusieurs maîtres."""
    t = export["totaux"]
    partagees = export["references_partagees"]
    liens_en_trop = sum(len(p["maitres"]) - 1 for p in partagees)
    assert t["appartenances_doute"] - t["notices_doute"] == liens_en_trop
    assert t["notices_partagees"] == len(partagees)


def test_familles_et_niveaux_ne_s_additionnent_pas_en_union(export):
    """Garde-fou : une notice partagée peut relever de deux familles, donc de
    deux niveaux. Additionner les ventilations ne redonne PAS l'union — il ne
    faut jamais s'en servir pour déduire « hors liste »."""
    t = export["totaux"]
    assert sum(t["familles_notices"].values()) >= t["notices_doute"]
    assert sum(t["niveaux_notices"].values()) >= t["notices_doute"]
    for code, n in t["familles_notices"].items():
        assert n <= t["notices_doute"], code


def test_chaque_maitre_atteint_le_seuil(export):
    """Le seuil de 10 porte sur la personne, après regroupement des graphies."""
    for a in export["artistes"]:
        assert a["doute"] >= 10, a["nom"]


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


# --------------------------------------------------------------------------
# 4. Position d'un musée (2026-08-05)
# --------------------------------------------------------------------------
# Joconde publie parfois plusieurs positions sous le même code Muséofile : 59
# musées sur 548 au 2026-08-05. Tant que le pipeline retenait la première
# rencontrée, le musée Goya de Castres s'affichait dans la Manche sur la fiche
# de Ribera — et le même musée pouvait sauter d'une fiche à l'autre. Les cas
# ci-dessous sont les valeurs RÉELLES relevées dans la base ce jour-là.

def test_coord_musee_retient_la_position_majoritaire():
    """Castres : 1 114 notices dans le Tarn, 143 dans la Manche."""
    from build_artistes import coord_du_musee
    retenue = coord_du_musee(Counter({"43.604813, 2.239888": 1114,
                                      "49.15731, -1.236823": 143}))
    assert retenue == "43.604813, 2.239888"


def test_coord_musee_regroupe_les_positions_voisines():
    """Chantilly : la position isolée est la plus fréquente (6 567), mais les
    deux écritures de Chantilly totalisent 7 049 — c'est la grappe qui compte,
    sinon le musée Condé part en Lot-et-Garonne."""
    from build_artistes import coord_du_musee
    retenue = coord_du_musee(Counter({
        "44.204302, 0.648652": 6567,
        "49.19397, 2.48522": 4348,
        "49.19413375188932, 2.485123295821842": 2701}))
    assert retenue.startswith("49.19")


def test_coord_musee_sans_position_utilisable():
    from build_artistes import coord_du_musee
    assert coord_du_musee(Counter({"nan": 12})) is None
    assert coord_du_musee(Counter()) is None
