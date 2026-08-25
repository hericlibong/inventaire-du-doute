"""Tests de la reprise et de l'invalidation des vignettes (chantier POP, 2026-08-24).

Ce que ces tests protègent, c'est une règle de méthode : une vignette porte le
nom `<reference>.jpg` et RIEN dans le fichier ne dit d'où elle vient. Tant que
chaque référence n'avait qu'une source possible, la présence du fichier suffisait
à décider de ne pas le retélécharger. Ce n'est plus vrai : des estampes vont
passer de Wikimedia Commons à POP, sous le même nom de fichier. Sans les
contrôles testés ici, l'ancien JPEG resterait en place et l'index lui donnerait
le crédit et le lien de la nouvelle source — une fausse attribution.

Les cas destructifs (JPEG tronqué, échec d'écriture) travaillent tous dans le
répertoire temporaire de pytest : ni les exports versionnés ni le registre
d'audit ne sont touchés.

Les tests de priorité et de bascule Commons → POP viendront avec `ajouter_pop()`,
à l'étape 3 du chantier.

Usage : uv run pytest tests/test_vignettes_pop.py
"""

import io
import json
import sys
import urllib.parse
from pathlib import Path

import pytest
from PIL import Image

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
import build_vignettes as bv  # noqa: E402


# --- fabrique d'images de test ------------------------------------------------


def test_get_encode_les_chemins_pop_non_ascii(monkeypatch):
    """Espaces, ponctuation et Unicode d'une URL POP atteignent bien urllib."""
    recue = {}

    class Reponse:
        def __enter__(self):
            return self

        def __exit__(self, *_args):
            return False

        def read(self):
            return b"image"

    def ouvrir(req, timeout):
        recue["url"] = req.full_url
        recue["timeout"] = timeout
        return Reponse()

    monkeypatch.setattr(bv.urllib.request, "urlopen", ouvrir)
    brute = ("https://stockage.example/joconde/REF/"
             "BOUCHER (d'après) © musée.jpg?taille=grand format")

    assert bv._get(brute) == b"image"
    assert recue["timeout"] == 90
    assert " " not in recue["url"]
    assert "©" not in recue["url"]
    assert urllib.parse.unquote(urllib.parse.urlsplit(recue["url"]).path) == (
        "/joconde/REF/BOUCHER (d'après) © musée.jpg"
    )


def test_get_ne_double_pas_une_url_deja_encodee(monkeypatch):
    recue = {}

    class Reponse:
        def __enter__(self):
            return self

        def __exit__(self, *_args):
            return False

        def read(self):
            return b"image"

    def ouvrir(req, timeout):
        recue["url"] = req.full_url
        return Reponse()

    monkeypatch.setattr(bv.urllib.request, "urlopen", ouvrir)
    bv._get("https://stockage.example/a%20b.jpg?x=d%C3%A9j%C3%A0")

    assert recue["url"] == "https://stockage.example/a%20b.jpg?x=d%C3%A9j%C3%A0"

def octets_jpeg(largeur=1200, hauteur=900, couleur=(120, 90, 60)) -> bytes:
    """Une image en mémoire, comme celle que renvoie un téléchargement."""
    tampon = io.BytesIO()
    Image.new("RGB", (largeur, hauteur), couleur).save(tampon, "JPEG", quality=90)
    return tampon.getvalue()


@pytest.fixture
def atelier(tmp_path, monkeypatch):
    """Un dossier de vignettes isolé + un index précédent vierge.

    `DOSSIER_IMG` et `_INDEX_PRECEDENT` sont des variables de module : on les
    remplace le temps du test, pour que rien n'écrive dans data/exports/.
    """
    dossier = tmp_path / "oeuvres_img"
    dossier.mkdir()
    monkeypatch.setattr(bv, "DOSSIER_IMG", dossier)
    monkeypatch.setattr(bv, "_INDEX_PRECEDENT", {})
    return dossier


# --- validité d'un JPEG -------------------------------------------------------

def test_jpeg_complet_est_valide(atelier):
    chemin = atelier / "ref.jpg"
    chemin.write_bytes(octets_jpeg())
    assert bv.jpeg_valide(chemin)


def test_jpeg_tronque_est_refuse(atelier):
    """Le cas d'une exécution interrompue pendant l'écriture.

    L'en-tête reste valide : c'est pour cela qu'un simple `verify()` ne suffit
    pas et qu'on décode l'image en entier.
    """
    entier = octets_jpeg()
    chemin = atelier / "ref.jpg"
    chemin.write_bytes(entier[: len(entier) // 2])
    assert not bv.jpeg_valide(chemin)


def test_fichier_vide_est_refuse(atelier):
    chemin = atelier / "ref.jpg"
    chemin.write_bytes(b"")
    assert not bv.jpeg_valide(chemin)


# --- écriture atomique --------------------------------------------------------

def test_ecriture_ne_laisse_pas_de_temporaire(atelier):
    sortie = atelier / "ref.jpg"
    bv.optimiser(octets_jpeg(), sortie)
    assert sortie.exists()
    assert bv.jpeg_valide(sortie)
    assert list(atelier.glob("*.tmp")) == []


def test_largeur_et_qualite_sont_parametrables(atelier):
    """Le profil POP doit pouvoir différer de celui de Commons sans le toucher."""
    sortie = atelier / "ref.jpg"
    bv.optimiser(octets_jpeg(1200, 900), sortie, largeur=600, qualite=75)
    with Image.open(sortie) as im:
        assert im.width == 600
        assert im.height == 450  # proportions conservées


def test_echec_laisse_le_fichier_precedent_intact(atelier):
    """Une source illisible ne doit pas détruire la vignette déjà en place."""
    sortie = atelier / "ref.jpg"
    bv.optimiser(octets_jpeg(couleur=(10, 20, 30)), sortie)
    avant = sortie.read_bytes()

    with pytest.raises(Exception):
        bv.optimiser(b"ceci n'est pas une image", sortie)

    assert sortie.read_bytes() == avant
    assert list(atelier.glob("*.tmp")) == []


def test_echec_du_remplacement_atomique_preserve_le_fichier(atelier, monkeypatch):
    """Même un échec au dernier instant ne détruit pas le JPEG précédent."""
    sortie = atelier / "ref.jpg"
    bv.optimiser(octets_jpeg(couleur=(10, 20, 30)), sortie)
    avant = sortie.read_bytes()

    def remplacement_impossible(*_args):
        raise OSError("remplacement simulé impossible")

    monkeypatch.setattr(bv.os, "replace", remplacement_impossible)
    with pytest.raises(OSError, match="remplacement simulé impossible"):
        bv.optimiser(octets_jpeg(couleur=(200, 210, 220)), sortie)

    assert sortie.read_bytes() == avant
    assert list(atelier.glob("*.tmp")) == []


def test_nettoyage_des_temporaires(atelier):
    (atelier / "a.jpg.tmp").write_bytes(b"reste")
    (atelier / "b.jpg.tmp").write_bytes(b"reste")
    (atelier / "c.jpg").write_bytes(octets_jpeg())
    assert bv.nettoyer_temporaires() == 2
    assert list(atelier.glob("*.tmp")) == []
    assert (atelier / "c.jpg").exists()


# --- réutilisation d'une vignette déjà présente -------------------------------

def test_absent_du_disque_non_reutilisable(atelier):
    assert not bv.fichier_reutilisable("ref", "wikimedia_commons")


def test_meme_source_meme_profil_reutilisable(atelier, monkeypatch):
    (atelier / "ref.jpg").write_bytes(octets_jpeg())
    monkeypatch.setattr(bv, "_INDEX_PRECEDENT",
                        {"ref": {"source_type": "wikimedia_commons"}})
    assert bv.fichier_reutilisable("ref", "wikimedia_commons")


def test_changement_de_source_invalide_le_fichier(atelier, monkeypatch):
    """LE cas du chantier : une estampe Commons qui passe à POP.

    Le fichier est là, il est valide, et il ne doit PAS être réutilisé : il
    montre un autre exemplaire, et l'index s'apprête à lui donner le crédit POP.
    """
    (atelier / "ref.jpg").write_bytes(octets_jpeg())
    monkeypatch.setattr(bv, "_INDEX_PRECEDENT",
                        {"ref": {"source_type": "wikimedia_commons"}})
    assert not bv.fichier_reutilisable("ref", "pop_joconde", bv.PROFIL_POP)


def test_changement_de_profil_pop_invalide_le_fichier(atelier, monkeypatch):
    (atelier / "ref.jpg").write_bytes(octets_jpeg())
    monkeypatch.setattr(bv, "_INDEX_PRECEDENT",
                        {"ref": {"source_type": "pop_joconde", "profil": "pop-900-82"}})
    assert not bv.fichier_reutilisable("ref", "pop_joconde", "pop-800-78")


def test_meme_profil_pop_reste_reutilisable(atelier, monkeypatch):
    (atelier / "ref.jpg").write_bytes(octets_jpeg())
    monkeypatch.setattr(bv, "_INDEX_PRECEDENT",
                        {"ref": {"source_type": "pop_joconde", "profil": "pop-800-78"}})
    assert bv.fichier_reutilisable("ref", "pop_joconde", "pop-800-78")


def test_changement_de_profil_pop_epargne_commons(atelier, monkeypatch):
    """Le point exigé par le plan (§3.1) : les 192 vignettes ouvertes ne bougent pas.

    Une entrée Commons ne porte pas de `profil`, et on ne lui en demande pas :
    aucune valeur de profil POP ne peut donc la rendre périmée.
    """
    (atelier / "ref.jpg").write_bytes(octets_jpeg())
    monkeypatch.setattr(bv, "_INDEX_PRECEDENT",
                        {"ref": {"source_type": "wikimedia_commons"}})
    for profil_pop in ("pop-900-82", "pop-800-78", "pop-600-75"):
        assert bv.fichier_reutilisable("ref", "wikimedia_commons"), profil_pop


def test_fichier_orphelin_non_reutilisable(atelier):
    """Fichier sur le disque, aucune entrée dans l'index précédent.

    Rien n'atteste sa provenance : on préfère le refaire plutôt que lui prêter
    une source invérifiable.
    """
    (atelier / "ref.jpg").write_bytes(octets_jpeg())
    assert not bv.fichier_reutilisable("ref", "wikimedia_commons")


def test_fichier_tronque_non_reutilisable(atelier, monkeypatch):
    """La reprise après interruption : même source, même profil, mais illisible."""
    entier = octets_jpeg()
    (atelier / "ref.jpg").write_bytes(entier[: len(entier) // 3])
    monkeypatch.setattr(bv, "_INDEX_PRECEDENT",
                        {"ref": {"source_type": "wikimedia_commons"}})
    assert not bv.fichier_reutilisable("ref", "wikimedia_commons")


def test_identifiant_de_profil_suit_les_constantes():
    """Le profil suit les constantes et reste propre à POP.

    Le plan laisse encore 900/82 comme candidat. Interdire l'égalité numérique
    avec Commons rendrait ce choix impossible sans raison : c'est le préfixe
    ``pop-`` qui sépare les familles et protège leur invalidation. Changer la
    largeur ou la qualité doit en parallèle changer l'identifiant.
    """
    assert bv.PROFIL_POP == f"pop-{bv.LARGEUR_POP}-{bv.QUALITE_POP}"
    assert bv.PROFIL_POP.startswith("pop-")


# --- passe POP : après Commons exact, avant les sources de repli ----------------
#
# Le registre d'audit et le réseau sont remplacés par des doublures : ces tests
# décrivent une RÈGLE DE PRIORITÉ, pas la disponibilité d'un serveur. Tout se
# passe dans le répertoire temporaire de pytest.

REGISTRE = {
    "NEUVE": {
        "statut": "unknown", "credit": "© GUENAT Pierre",
        "image": "https://stockage.example/joconde/NEUVE/x.jpg",
        "notice_pop": "https://pop.culture.gouv.fr/notice/joconde/NEUVE",
        "verifie_le": "2026-07-29",
    },
    "SANSCREDIT": {
        "statut": "restricted", "credit": "",
        "image": "https://stockage.example/joconde/SANSCREDIT/x.jpg",
        "notice_pop": "https://pop.culture.gouv.fr/notice/joconde/SANSCREDIT",
        "verifie_le": "2026-07-29",
    },
    "COMMONS": {
        "statut": "unknown", "credit": "© Quelqu'un",
        "image": "https://stockage.example/joconde/COMMONS/x.jpg",
        "notice_pop": "https://pop.culture.gouv.fr/notice/joconde/COMMONS",
        "verifie_le": "2026-07-29",
    },
    "AUTREEX": {
        "statut": "unknown", "credit": "musée de l'Image / cliché H. Rouyer",
        "image": "https://stockage.example/joconde/AUTREEX/x.jpg",
        "notice_pop": "https://pop.culture.gouv.fr/notice/joconde/AUTREEX",
        "verifie_le": "2026-07-29",
    },
}


@pytest.fixture
def passe_pop(atelier, tmp_path, monkeypatch):
    """`ajouter_pop` branché sur un registre de test et un réseau simulé."""
    registre = tmp_path / "images_oeuvres.json"
    registre.write_text(json.dumps(REGISTRE, ensure_ascii=False), encoding="utf-8")
    monkeypatch.setattr(bv, "REGISTRE_POP", registre)
    monkeypatch.setattr(bv.time, "sleep", lambda *_: None)

    telecharges = []

    def reseau(url):
        telecharges.append(url)
        if "ECHEC" in url:
            raise OSError("téléchargement simulé en échec")
        return octets_jpeg(1000, 800, couleur=(30, 140, 200))

    monkeypatch.setattr(bv, "_get", reseau)
    return telecharges


def index_commons(exemplaire_autre=False):
    """Une entrée d'index telle que les passes ouvertes la produisent."""
    entree = {
        "statut": "open", "source_type": "wikimedia_commons",
        "url": "oeuvres/COMMONS.jpg", "credit": "Own work", "creator": "X",
        "licence": "Public domain", "licence_url": "",
        "source": "https://commons.wikimedia.org/wiki/File:X.jpg",
        "verifie_le": "2026-08-06",
    }
    if exemplaire_autre:
        entree["exemplaire_autre"] = True
    return entree


def test_commons_exact_n_est_jamais_remplace(atelier, passe_pop, monkeypatch):
    """Priorité 1 : une image qui montre l'objet du musée reste en place."""
    monkeypatch.setattr(bv, "_INDEX_PRECEDENT", {"COMMONS": index_commons()})
    index = {"COMMONS": index_commons()}
    bilan = bv.ajouter_pop(index, references={"COMMONS"})

    assert index["COMMONS"]["source_type"] == "wikimedia_commons"
    assert bilan["ignorees"] == 1
    assert bilan["ajoutees"] == 0 and bilan["remplacees"] == 0
    assert passe_pop == []  # aucun téléchargement déclenché


def test_exemplaire_autre_bascule_sur_pop(atelier, passe_pop, monkeypatch):
    """Priorité 2 : POP montre la feuille du musée, l'autre tirage cède."""
    (atelier / "AUTREEX.jpg").write_bytes(octets_jpeg(couleur=(200, 10, 10)))
    ancien = (atelier / "AUTREEX.jpg").read_bytes()
    monkeypatch.setattr(bv, "_INDEX_PRECEDENT",
                        {"AUTREEX": {"source_type": "gallica_bnf"}})
    index = {"AUTREEX": index_commons(exemplaire_autre=True)}
    bilan = bv.ajouter_pop(index, references={"AUTREEX"})

    assert bilan["remplacees"] == 1
    assert index["AUTREEX"]["source_type"] == "pop_joconde"
    # Le JPEG a bien été refait malgré un nom identique.
    assert (atelier / "AUTREEX.jpg").read_bytes() != ancien
    # Et la réserve d'exemplaire ne survit pas : POP montre l'objet du musée.
    assert "exemplaire_autre" not in index["AUTREEX"]


def test_echec_pop_conserve_l_ancien_exemplaire(atelier, passe_pop, monkeypatch):
    """Un échec réseau ne doit pas dégrader ce qui était déjà publiable."""
    (atelier / "AUTREEX.jpg").write_bytes(octets_jpeg(couleur=(200, 10, 10)))
    ancien = (atelier / "AUTREEX.jpg").read_bytes()
    registre = json.loads(bv.REGISTRE_POP.read_text(encoding="utf-8"))
    registre["AUTREEX"]["image"] = "https://stockage.example/ECHEC/x.jpg"
    bv.REGISTRE_POP.write_text(json.dumps(registre, ensure_ascii=False), encoding="utf-8")
    monkeypatch.setattr(bv, "_INDEX_PRECEDENT",
                        {"AUTREEX": {"source_type": "gallica_bnf"}})

    index = {"AUTREEX": index_commons(exemplaire_autre=True)}
    bilan = bv.ajouter_pop(index, references={"AUTREEX"})

    assert len(bilan["echecs"]) == 1
    assert index["AUTREEX"]["source_type"] == "wikimedia_commons"
    assert index["AUTREEX"]["exemplaire_autre"] is True
    assert (atelier / "AUTREEX.jpg").read_bytes() == ancien


def test_echec_pop_ne_cree_aucune_entree(atelier, passe_pop, monkeypatch):
    """Priorité 3, en échec : la fiche garde son emplacement vide.

    Une entrée d'index sans fichier ferait afficher une image cassée ; l'absence
    d'entrée fait afficher le placeholder, qui est la bonne réponse.
    """
    registre = json.loads(bv.REGISTRE_POP.read_text(encoding="utf-8"))
    registre["NEUVE"]["image"] = "https://stockage.example/ECHEC/x.jpg"
    bv.REGISTRE_POP.write_text(json.dumps(registre, ensure_ascii=False), encoding="utf-8")

    index = {}
    bilan = bv.ajouter_pop(index, references={"NEUVE"})

    assert index == {}
    assert bilan["ajoutees"] == 0 and len(bilan["echecs"]) == 1
    assert not (atelier / "NEUVE.jpg").exists()


def test_selection_limitee_au_lot(atelier, passe_pop):
    """Le lot restreint ne doit traiter que ce qu'on lui demande."""
    index = {}
    bv.ajouter_pop(index, references={"NEUVE"})
    assert set(index) == {"NEUVE"}


def test_lot_preserve_les_entrees_pop_precedentes_hors_lot(
        atelier, passe_pop, monkeypatch):
    """Rejouer quelques échecs ne doit pas amputer l'index déjà produit."""
    (atelier / "SANSCREDIT.jpg").write_bytes(octets_jpeg())
    precedente = {
        "source_type": "pop_joconde",
        "profil": bv.PROFIL_POP,
    }
    monkeypatch.setattr(bv, "_INDEX_PRECEDENT", {"SANSCREDIT": precedente})

    index = {}
    bilan = bv.ajouter_pop(index, references={"NEUVE"})

    assert set(index) == {"NEUVE", "SANSCREDIT"}
    assert index["SANSCREDIT"]["source_type"] == "pop_joconde"
    assert bilan["conservees_hors_lot"] == 1
    assert len(passe_pop) == 1  # seule NEUVE a été téléchargée


def test_lot_refuse_d_effacer_une_image_pop_hors_lot_invalide(
        atelier, passe_pop, monkeypatch):
    """Un lot partiel s'arrête si une entrée extérieure devrait être réparée."""
    monkeypatch.setattr(bv, "_INDEX_PRECEDENT", {
        "SANSCREDIT": {
            "source_type": "pop_joconde",
            "profil": bv.PROFIL_POP,
        }
    })

    index = {}
    with pytest.raises(RuntimeError, match="hors lot à régénérer"):
        bv.ajouter_pop(index, references={"NEUVE"})

    assert index == {}
    assert passe_pop == []


def test_sans_lot_tout_le_corpus_est_traite(atelier, passe_pop):
    """Le mode production ne demande aucune réécriture : `references=None`."""
    index = {}
    bilan = bv.ajouter_pop(index)
    assert set(index) == set(REGISTRE)
    assert bilan["ajoutees"] == len(REGISTRE)


def test_main_place_pop_avant_les_sources_alternatives(tmp_path, monkeypatch):
    """Une relance ne doit jamais laisser Gallica réécrire un JPEG POP."""
    correspondances = tmp_path / "commons.json"
    correspondances.write_text("[]", encoding="utf-8")
    monkeypatch.setattr(bv, "CORRESP", correspondances)
    monkeypatch.setattr(bv, "INDEX", tmp_path / "images_index.json")
    monkeypatch.setattr(bv, "DOSSIER_IMG", tmp_path / "images")

    ordre = []
    monkeypatch.setattr(
        bv, "ajouter_pop",
        lambda index, references=None: ordre.append("pop") or {}
    )
    monkeypatch.setattr(
        bv, "ajouter_gallica",
        lambda index: ordre.append("gallica") or 0
    )
    monkeypatch.setattr(
        bv, "ajouter_imagerie_commons",
        lambda index: ordre.append("imagerie_commons") or 0
    )
    monkeypatch.setattr(bv, "fusionner_dans_oeuvres", lambda index: 0)

    bv.main(references={"TEMOIN"})

    assert ordre == ["pop", "gallica", "imagerie_commons"]


def test_forme_complete_des_metadonnees(atelier, passe_pop):
    index = {}
    bv.ajouter_pop(index, references={"NEUVE"})
    e = index["NEUVE"]
    assert e == {
        "statut": "unknown",
        "source_type": "pop_joconde",
        "url": "oeuvres/NEUVE.jpg",
        "credit": "© GUENAT Pierre",
        "licence": "",
        "source": "https://pop.culture.gouv.fr/notice/joconde/NEUVE",
        "profil": "pop-800-75",
        "verifie_le": "2026-07-29",
    }


def test_statut_recopie_jamais_ouvert(atelier, passe_pop):
    """Aucune image POP ne doit se retrouver déclarée réutilisable."""
    index = {}
    bv.ajouter_pop(index)
    for e in index.values():
        assert e["statut"] in ("restricted", "unknown")
        assert e["licence"] == ""


def test_credit_vide_reste_vide_dans_la_donnee(atelier, passe_pop):
    """Le repli d'affichage vit dans CreditImage.svelte, pas dans l'index."""
    index = {}
    bv.ajouter_pop(index, references={"SANSCREDIT"})
    assert index["SANSCREDIT"]["credit"] == ""
    assert "non précisé" not in json.dumps(index, ensure_ascii=False)


def test_source_pointe_la_fiche_jamais_le_stockage(atelier, passe_pop):
    index = {}
    bv.ajouter_pop(index)
    for ref, e in index.items():
        assert e["source"] == f"https://pop.culture.gouv.fr/notice/joconde/{ref}"
        assert "stockage.example" not in e["source"]
        assert not e["source"].endswith(".jpg")


def test_profil_pop_inscrit_dans_l_entree(atelier, passe_pop):
    """Sans lui, l'invalidation sur changement de profil serait aveugle."""
    index = {}
    bv.ajouter_pop(index, references={"NEUVE"})
    assert index["NEUVE"]["profil"] == bv.PROFIL_POP


def test_vignette_pop_encodee_au_profil_retenu(atelier, passe_pop):
    index = {}
    bv.ajouter_pop(index, references={"NEUVE"})
    with Image.open(atelier / "NEUVE.jpg") as im:
        assert im.width == bv.LARGEUR_POP  # l'original de test fait 1000 px
        assert im.height == 640            # proportions conservées


def test_lot_demande_lit_le_fichier(tmp_path):
    fichier = tmp_path / "lot.txt"
    fichier.write_text("# lot témoin\nAAA\n\nBBB  # commentaire en bout de ligne\n",
                       encoding="utf-8")
    assert bv.lot_demande(["--lot", str(fichier)]) == {"AAA", "BBB"}
    assert bv.lot_demande([]) is None


@pytest.mark.parametrize("arguments", [["--lot"], ["inconnu"], ["--lot", "a", "b"]])
def test_lot_demande_refuse_une_ligne_de_commande_invalide(arguments):
    with pytest.raises(SystemExit, match="usage"):
        bv.lot_demande(arguments)


def test_absence_du_registre_pop_bloque_l_execution(atelier, tmp_path, monkeypatch):
    monkeypatch.setattr(bv, "REGISTRE_POP", tmp_path / "absent.json")
    with pytest.raises(FileNotFoundError, match="registre POP introuvable"):
        bv.ajouter_pop({})
