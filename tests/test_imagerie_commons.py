"""Tests de l'appariement des estampes d'imagerie populaire (2026-08-07).

Ce que ces tests protègent, c'est une décision de méthode : le numéro de
planche relevé par le musée départage des candidates trouvées par le titre,
mais ne désigne jamais une image à lui seul. Les cas viennent tous du corpus
réel — trois « Notre-Dame de Bon-Secours » chez trois éditeurs, un « Cadet
Rousselle » numéroté 384 face à deux notices qui en annoncent d'autres.

Usage : uv run pytest tests/test_imagerie_commons.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
from build_imagerie_commons import (assez_distinctif, examine,  # noqa: E402
                                    licence_ouverte, numero_joconde,
                                    numeros, titre_comparable)


def fichier(nom, description="", licence="Public domain"):
    """Un candidat du fonds, tel que l'index le prépare."""
    from build_imagerie_commons import aplat
    designation = aplat(nom)
    return {"fichier": "File:" + nom, "designation": designation,
            "description": aplat(description), "licence": licence,
            "numeros": numeros(designation + " " + description)}


# --- 1. Le numéro se lit malgré les graphies du relevé -----------------------
def test_numero_lu_dans_les_inscriptions():
    # Le musée recopie ce qui est imprimé : le point se glisse où il veut.
    for relevé, attendu in [
        ("PELLERIN & Cie, imp-édit. (h.g.) ; IMAGERIE D'EPINAL, N.°551 (h.d.)", "551"),
        ("IMAGERIE D'ÉPINAL, N° 1883. (h.d.)", "1883"),
        ("Imp. OLIVIER-PINOT édit. à Epinal (b.g.)", None),
    ]:
        assert numero_joconde({"precisions_inscriptions": relevé}, "") == attendu


def test_numero_lu_a_defaut_dans_le_titre():
    meta = {"precisions_inscriptions": ""}
    assert numero_joconde(meta, "NOTRE-DAME DE BON-SECOURS. N° 1119 (titre inscrit)") == "1119"


def test_numero_de_l_imagerie_prime_sur_les_autres_nombres():
    # « à Dix centimes la feuille » et « N°1036 » cohabitent : c'est celui qui
    # suit le nom de l'imagerie qui désigne la planche.
    relevé = ("NOUVELLE IMAGERIE D'EPINAL, N° 265 (h.g.) ; à Dix centimes la "
              "feuille. (h.d.) ; DEPOSE N° 12 (b.d.)")
    assert numero_joconde({"precisions_inscriptions": relevé}, "") == "265"


# --- 2. Le titre comparable ------------------------------------------------
def test_titre_debarrasse_des_mentions_de_saisie():
    assert titre_comparable("NOTRE-DAME DE BON-SECOURS. N° 102 (titre inscrit)") \
        == "notre dame de bon secours"


def test_titre_garde_le_premier_seulement():
    # Ce qui suit le point-virgule est une traduction ou un titre factice.
    assert titre_comparable("Die drei Sprachen. (titre inscrit all.) ; les trois "
                            "langues (titre factice)") == "die drei sprachen"


def test_titre_trop_court_ou_trop_commun_est_refuse():
    assert not assez_distinctif(titre_comparable("LA CHASSE. (titre inscrit)"))
    assert assez_distinctif(titre_comparable("LES DEGRÉS DES AGES DE L'HOMME."))


# --- 3. La décision --------------------------------------------------------
def test_titre_et_numero_concordants_font_une_correspondance():
    etat, raisons = examine(
        "legende de saint eloi", "631",
        fichier("Imagerie d'Epinal. N°631, Légende de Saint Eloi - estampe.jpg"))
    assert etat == "exacte"
    assert any("631" in r for r in raisons)


def test_numeros_differents_font_un_refus():
    # Cas réel : la planche numérisée porte 384, la notice annonce 518.
    etat, raisons = examine("cadet rousselle", "518",
                            fichier("Cadet Rousselle N° 384 - estampe.jpg"))
    assert etat == "refusee"
    assert "384" in raisons[0]


def test_sans_numero_cote_fichier_on_ne_conclut_pas():
    etat, _ = examine("cadet rousselle", "518", fichier("Cadet Rousselle par Pellerin.jpg"))
    assert etat == "candidate"


def test_titre_absent_du_fichier_est_refuse_sans_raison_a_publier():
    etat, raisons = examine("le moulin merveilleux", "12",
                            fichier("Napoléon à Montereau - estampe.jpg"))
    assert etat == "refusee" and raisons == []


def test_la_description_seule_ne_prouve_pas_un_titre():
    # Sans numéro pour confirmer, un titre trouvé dans le commentaire libre du
    # fichier ne vaut rien : c'est ce qui produisait des rapprochements faux.
    etat, _ = examine("charge de cosaques", None,
                      fichier("Soldats à aspects simple et complet.jpg",
                              description="planche évoquant une charge de cosaques"))
    assert etat == "refusee"


def test_licence_non_ouverte_ecarte_le_fichier():
    etat, raisons = examine(
        "legende de saint eloi", "631",
        fichier("Imagerie d'Epinal. N°631, Légende de Saint Eloi.jpg",
                licence="Tous droits réservés"))
    assert etat == "refusee"
    assert "licence" in raisons[0]


def test_licences_acceptees():
    assert licence_ouverte("Public domain")
    assert licence_ouverte("CC BY-SA 4.0")
    assert licence_ouverte("CC0")
    assert not licence_ouverte("")
    assert not licence_ouverte("Fair use")
