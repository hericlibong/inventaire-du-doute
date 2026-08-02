"""Tests du contrat de données de la page « Présentation ».

L'export `corpus_maitres.json` ne mesure rien : il projette des chiffres déjà
validés (artistes.json, vue_ensemble.json, niveaux.json). Ce que ces tests
protègent, ce sont les INVARIANTS D'UNITÉS — le seul endroit où la page peut
mentir sans que le build s'en aperçoive :

    notices distinctes ≠ occurrences de mentions ≠ associations artiste-notice

La page emploie les deux premières et écrit laquelle elle compte. Les confondre
reviendrait à publier un chiffre faux.

AUCUN EFFECTIF N'EST ÉCRIT EN DUR ICI (2026-08-02). La version précédente figeait
3 668 / 3 669 / 3 674 / 63 : ces quatre nombres sont devenus faux en une journée,
au premier lot d'artistes instruit. Un test qui fige un effectif ne protège rien —
il oblige seulement à le réécrire. Ce qui doit tenir, ce sont les RELATIONS.

Usage : uv run pytest
"""

import json
from pathlib import Path

import pytest

RACINE = Path(__file__).parent.parent
EXPORT = RACINE / "data" / "exports" / "web" / "corpus_maitres.json"
ARTISTES = RACINE / "data" / "exports" / "web" / "artistes.json"

# Les huit mentions publiées, telles que la couche publique du front les attend
# (web/src/lib/familles-public.js). Un code qui disparaît ici casse l'affichage.
MENTIONS = {
    "attribue", "point_interrogation", "ecole_de", "atelier_de",
    "maniere_de", "entourage_de", "genre_de", "suiveur_de",
}


@pytest.fixture(scope="module")
def corpus():
    if not EXPORT.exists():
        pytest.skip("corpus_maitres.json absent — lancer src/build_corpus_maitres.py")
    return json.loads(EXPORT.read_text(encoding="utf-8"))


def test_les_trois_unites_ne_se_confondent_pas(corpus):
    """Trois mesures, trois valeurs — l'ampleur est toujours la plus petite."""
    u = corpus["unites"]
    assert u["notices_distinctes"] <= u["occurrences_mentions"]
    assert u["notices_distinctes"] <= u["associations_artiste_notice"]


def test_notices_partagees(corpus):
    """Une notice qui nomme deux artistes retenus compte deux fois dans les
    profils, une seule fois dans l'ampleur du volume. L'écart, c'est exactement
    le nombre de ces notices."""
    u = corpus["unites"]
    assert u["notices_distinctes"] + u["notices_partagees"] == \
        u["associations_artiste_notice"]


def test_somme_des_mentions_vaut_les_occurrences(corpus):
    """Le graphique compte des notices par mention : leur somme vaut les
    occurrences, jamais les notices distinctes."""
    total = sum(m["corpus_notices"] for m in corpus["mentions"].values())
    assert total == corpus["unites"]["occurrences_mentions"]


def test_les_huit_mentions_publiees(corpus):
    """Le front attend ces huit codes, ni plus ni moins."""
    assert set(corpus["mentions"]) == MENTIONS
    assert corpus["unites"]["nb_mentions"] == len(MENTIONS)


def test_aucune_mention_ne_depasse_le_volume(corpus):
    """Une mention ne peut pas concerner plus de notices que le volume n'en a."""
    ampleur = corpus["unites"]["notices_distinctes"]
    for code, m in corpus["mentions"].items():
        assert 0 <= m["corpus_notices"] <= ampleur, code


def test_le_volume_est_une_part_du_national(corpus):
    """Le volume n'est PAS tout le doute de Joconde, et la part publiée le dit."""
    u, n = corpus["unites"], corpus["national"]
    assert 0 < u["notices_distinctes"] < n["notices_prudentes"]
    part = u["notices_distinctes"] / n["notices_prudentes"]
    assert abs(n["part_du_volume"] - part) < 0.0001


def test_effectif_d_artistes_accorde_avec_l_export_principal(corpus):
    """Le nombre d'artistes se lit dans les données, jamais dans un titre : les
    deux exports doivent en annoncer le même."""
    if not ARTISTES.exists():
        pytest.skip("artistes.json absent")
    artistes = json.loads(ARTISTES.read_text(encoding="utf-8"))
    assert corpus["unites"]["nb_artistes"] == len(artistes["artistes"])
    assert corpus["unites"]["notices_distinctes"] == \
        artistes["totaux"]["notices_doute"]


def test_les_vues_abandonnees_ne_sont_pas_exportees(corpus):
    """La matrice des profils et la comparaison nationale par mention ont été
    abandonnées le 2026-08-02. Ce qui les alimentait ne doit pas rester dans
    l'export : ce qui n'est pas publié ne revient pas par la porte de derrière."""
    assert "artistes" not in corpus, "la ventilation par artiste est de retour"
    for code, m in corpus["mentions"].items():
        assert set(m) == {"corpus_notices"}, f"série de trop pour {code} : {set(m)}"
