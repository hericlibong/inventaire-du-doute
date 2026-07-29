"""Tests de la classification « Avant / après » — figés sur la vérification
manuelle du 2026-07-14 (échantillon de 80 notices, verdicts utilisateur).

Deux niveaux :
1. des cas UNITAIRES explicites, chacun figeant un comportement précis issu des
   verdicts (parsing, catégories, direction inverse) — le vrai contrat de
   régression, lisible sans le CSV ;
2. une vérification de COHÉRENCE sur le CSV annoté
   (data/exports/echantillon_revisions_annotes.csv) : tout cas jugé « OK » doit
   rester montrable en galerie, tout cas « à exclure » ou « faux passage » doit
   en être écarté.

Usage : uv run pytest
"""

import csv
import sys
from pathlib import Path

import pytest

RACINE = Path(__file__).parent.parent
sys.path.insert(0, str(RACINE / "src"))
import revisions_classify as rc  # noqa: E402

CSV_ANNOTE = RACINE / "data" / "exports" / "echantillon_revisions_annotes.csv"


# (ancienne, actuel, catégorie attendue, galerie attendue, note)
CAS_UNITAIRES = [
    # --- Vers un autre nom ---
    ("LA TOUR MAURICE QUENTIN DE (ancienne attribution)", "VALADE Jean",
     "autre_nom", True, "cas propre, deux noms distincts"),
    ("attribué à : BACKER Jacob de", "RIJCKERE Bernaert de",
     "autre_nom", True, "ancien déjà prudent, nom actuel différent"),
    # --- Même nom, attribution plus prudente (nouvelle catégorie) ---
    ("ancienne attribution : FURINI Francesco", "FURINI Francesco (attribué à)",
     "meme_nom", True, "même nom, réserve ajoutée"),
    ("ancienne attribution : Rembrandt Harmensz van Rijn",
     "Rembrandt (1606-1669) (manière de)",
     "meme_nom", True, "même nom, passage vers manière de"),
    ("attribué à : ROSA Salvator", "ROSA Salvator (école);anonyme",
     "meme_nom", True, "même nom déjà prudent → école : reste plus prudent"),
    # même personne mais plus AFFIRMÉ (école de X → X) : PAS meme_nom, hors galerie
    ("Ecole de, MAZZUOLA Francesco", "MAZZUOLA Francesco",
     "mineur", False, "confirmation, pas une mise en garde"),
    ("LE NAIN LOUIS (BRIERE)", "LE NAIN",
     "mineur", False, "précision de prénom, même famille"),
    # --- Vers l'anonyme ---
    ("ancienne attribution : DONZEL Charles", "anonyme",
     "anonyme", True, "un nom → anonyme"),
    # --- Vers une copie (précédence copie > anonyme) ---
    ("ancienne attribution : ANONYME ALLEMAND XVIe s",
     "DURER Albrecht (d'après);anonyme",
     "copie", True, "anonyme + d'après → copie, pas anonyme"),
    # --- Déjà une copie ou un d'après (hors galerie) ---
    ("Copie d'après, BAGETTI Giuseppe Pietro", "BAGETTI Giuseppe Pietro",
     "deja_copie", False, "l'avant était déjà une copie"),
    # --- Plusieurs anciens noms / chaînes (hors galerie) ---
    ("Genre de, HOLLAR Wenzel ; PATINIR Joachim", "COCK Lucas Cornelisz de",
     "plusieurs_noms", False, "deux hypothèses distinctes"),
    ("Ecole de Fontainebleau (ancienne attribution) ; Primatice (ancienne attribution)",
     "MASSYS Jan (attribué)",
     "plusieurs_noms", False, "école-lieu + un nom = deux hypothèses"),
    # --- École nationale seule → un nom : montrable avec verbatim ---
    ("ECOLE FLORENTINE 14E SIECLE (INVENTAIRE)", "PIETRO DA RIMINI",
     "autre_nom", True, "école nationale → nom, gardable avec verbatim"),
    ("Ancienne attribution : ECOLE FLAMANDE", "anonyme;GIORDANO Luca (d'après)",
     "copie", True, "école nationale → copie d'après"),
    # --- Changement mineur : anonyme national → anonyme ---
    ("ancienne attribution Anonyme espagnol", "anonyme",
     "mineur", False, "anonyme → anonyme, changement trop faible"),
]


@pytest.mark.parametrize("ancienne,actuel,cat,gal,note", CAS_UNITAIRES)
def test_categorie_et_galerie(ancienne, actuel, cat, gal, note):
    res = rc.classer(ancienne, actuel)
    assert res["categorie"] == cat, f"{note} — attendu {cat}, obtenu {res['categorie']}"
    assert res["galerie"] == gal, f"{note} — galerie attendue {gal}"


# ---- Parsing : bugs repérés à la vérification, figés ----

def test_parenthese_imbriquee_nom_propre():
    """« Santi Di Tito (16e siècle (2e moitié), Italie) » → nom nettoyé."""
    res = rc.classer("ancienne attribution : Santi Di Tito (16e siècle (2e moitié), Italie)",
                     "anonyme")
    assert res["ancien_nom"] == "Santi Di Tito"


def test_prose_pas_un_nom():
    """« Changement d'attribution » n'est pas un ancien nom affichable."""
    res = rc.classer("Changement d'attribution",
                     "OMMEGANCK Balthasar Paul (peintre, d'après)")
    assert res["ancien_nom"] is None
    assert res["galerie"] is False


def test_nom_avec_date_nettoye():
    """« GIOTTO, attribué en 1859 » → « GIOTTO » (coupe à virgule/chiffre)."""
    assert rc._nom_personne("GIOTTO, attribué en 1859") == "GIOTTO"


def test_point_virgule_dans_parentheses():
    """Un « ; » biographique dans une parenthèse ne coupe pas en deux hypothèses."""
    res = rc.classer("DYCK Antoon van (Anvers, 1599 ; Blackfriars, 1641)",
                     "SCHUT Cornelis I")
    assert res["categorie"] == "autre_nom"
    assert res["avant"]["n_hypotheses"] == 1


def test_parenthese_orpheline_en_tete():
    """« (PIERRE DE CORTONE … ; PUGET … » → deux hypothèses (chaîne)."""
    res = rc.classer("(PIERRE DE CORTONE (ancienne attribution) ; PUGET PIERRE (ROSSI)",
                     "anonyme")
    assert res["categorie"] == "plusieurs_noms"


def test_manufacture_pas_un_artiste():
    res = rc.classer("manufacture Wedgwood (ancienne attribution)", "Centre Indéterminé")
    assert res["galerie"] is False


def test_mot_entier_pas_de_sous_chaine():
    """« ÉCOLE CARAVAGESQUE » ne fournit pas Caravage comme personne."""
    assert rc._nom_personne("ECOLE CARAVAGESQUE") is None


def test_direction_inverse():
    """Anonyme → un nom : direction inverse signalée."""
    res = rc.classer("ancienne attribution : ANONYME ITALIEN fin XVIIe s",
                     "Calandrucci Giacinto (1646-1707)")
    assert res["inverse"] is True
    assert res["categorie"] == "autre_nom"


# ---- Cohérence avec le CSV annoté (80 verdicts humains) ----

def _lignes_annotees():
    if not CSV_ANNOTE.exists():
        pytest.skip("CSV annoté absent")
    with CSV_ANNOTE.open(encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def test_ok_restent_en_galerie():
    manques = []
    for r in _lignes_annotees():
        if r["verdict"].strip() != "OK":
            continue
        res = rc.classer(r["ancienne_attribution_brut"], r["auteur_actuel_brut"])
        if not res["galerie"]:
            manques.append(r["ancienne_attribution_brut"][:50])
    assert not manques, f"cas OK exclus à tort de la galerie : {manques}"


def test_exclus_hors_galerie():
    fuites = []
    for r in _lignes_annotees():
        if r["verdict"].strip() not in ("à exclure", "faux passage"):
            continue
        res = rc.classer(r["ancienne_attribution_brut"], r["auteur_actuel_brut"])
        if res["galerie"]:
            fuites.append(r["ancienne_attribution_brut"][:50])
    assert not fuites, f"cas à exclure restés en galerie : {fuites}"
