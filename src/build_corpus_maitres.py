"""Export léger de la page « Présentation » du volume 1.

Produit data/exports/web/corpus_maitres.json à partir des exports DÉJÀ validés
(artistes.json + vue_ensemble.json + niveaux.json) — aucune passe sur le CSV de
1,1 Go, aucune mesure nouvelle : ce fichier est une PROJECTION, contrôlée par des
`assert`, de chiffres qui existent ailleurs.

Pourquoi un export dédié plutôt que artistes.json (380 Ko) : la page n'a besoin
que de quelques totaux et de huit comptages. artistes.json embarque
`musees_doute` (géo, ventilation par musée), qui pèse l'essentiel du fichier et
ne sert pas ici.

Écrit pour le prototype d'analyse à trois vues (2026-08-01), CONSERVÉ et réduit
le 2026-08-02 quand deux de ces trois vues ont été abandonnées (decisions.md).
Ont disparu de l'export avec elles :
  - la ventilation par artiste, qui n'alimentait que la matrice des profils ;
  - le comptage national PAR MENTION, qui n'alimentait que la comparaison.
Ce qui n'est pas exporté ne peut pas revenir par la porte de derrière. Les deux
séries restent CALCULÉES ici : elles servent aux invariants.

TROIS UNITÉS, JAMAIS INTERCHANGEABLES (le point de vigilance de cet export) :

  notices distinctes ......... références Joconde du volume. C'est l'ampleur
                               annoncée, la seule mesure comparable au total
                               national.
  occurrences de mentions .... une notice porte parfois DEUX mentions (par ex.
                               « attribué à » et « ? »). Somme des notices
                               distinctes par mention.
  associations artiste-notice  ce que totalisent les profils : des notices
                               nomment deux artistes retenus et comptent donc
                               dans deux profils.

La page n'emploie que les deux premières, et écrit sous le graphique laquelle
elle compte.

AUCUN CHIFFRE N'EST FIGÉ ICI. Les invariants sont RELATIONNELS (a < b, a + b == c) :
un effectif écrit en dur redevient faux au premier lot d'artistes suivant —
c'est arrivé, et c'est la raison de cette note.

L'export ne porte que des chiffres et des codes de mentions. Il ne redéfinit ni
ordre d'affichage, ni libellé, ni couleur, ni regroupement en territoires : ces
nomenclatures publiques vivent une seule fois côté front (familles-public.js,
territoires.js). D'où un objet `mentions` indexé par code, et non une liste :
personne ne peut lire un ordre d'affichage dans ce fichier.

Usage : uv run python src/build_corpus_maitres.py  (instantané)
"""

import json
from datetime import datetime, timezone
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
WEB = RACINE / "data" / "exports" / "web"

# Les huit mentions de doute « solides » retenues par le projet. Même ensemble
# que build_vue_ensemble.FAMILLES ; l'ordre est ici sans portée (l'objet exporté
# est indexé par code, l'ordre d'affichage est celui d'ORDRE_FAMILLES côté front).
MENTIONS = [
    "attribue", "point_interrogation", "ecole_de", "atelier_de",
    "maniere_de", "entourage_de", "genre_de", "suiveur_de",
]


# Notice d'ouverture de la page. Elle est CHOISIE — c'est un exemple éditorial,
# pas un échantillon —, et le choix est déclaré dans docs/methode-et-limites.md.
# La règle « rien n'est choisi à la main » porte sur les listes exhaustives de
# l'onglet « Œuvres », qu'un tri arbitraire pourrait flatter ; elle ne demande pas
# qu'un article s'ouvre au hasard.
#
# Pourquoi celle-ci : le musée y écrit le nom de Rembrandt ET son atelier, et le
# titre porte lui-même une rétractation — « dit autrefois : Portrait de Titus ».
# Un cas dit tout le sujet en une ligne, sans commentaire.
#
# Rien n'est recopié : les champs sont relus dans l'export des œuvres, à la
# référence indiquée, et l'export échoue si la notice a changé de mention ou
# disparu. Un exemple qui vieillit en silence serait pire que pas d'exemple.
EXEMPLE_SLUG = "rembrandt"
EXEMPLE_REFERENCE = "000PE008564"
EXEMPLE_MENTION = "atelier_de"


def charger(nom):
    return json.loads((WEB / nom).read_text(encoding="utf-8"))


def notice_d_ouverture(artistes):
    """La notice de tête, relue dans l'export des œuvres et contrôlée."""
    fiche = charger(f"oeuvres/{EXEMPLE_SLUG}.json")
    o = next((x for x in fiche["oeuvres"] if x["reference"] == EXEMPLE_REFERENCE), None)
    assert o is not None, (
        f"notice d'ouverture {EXEMPLE_REFERENCE} absente de {EXEMPLE_SLUG}.json — "
        "en choisir une autre plutôt que la laisser disparaître de la page")
    assert o["code"] == EXEMPLE_MENTION, (
        f"la notice d'ouverture porte maintenant « {o['code']} » et non "
        f"« {EXEMPLE_MENTION} » : le texte de la page ne la décrit plus")
    assert o["titre"] and o["musee"], "notice d'ouverture sans titre ou sans musée"
    return {
        "reference": o["reference"],
        "titre": o["titre"],
        "musee": o["musee"],
        "ville": o["ville"],
        "mention": o["code"],
        # les mots exacts publiés par le musée — seule citation littérale de la page
        "extrait": o["extrait"],
        "artiste": fiche["nom"],
        "artiste_slug": fiche["slug"],
        "image": o.get("image"),
    }


def main():
    artistes = charger("artistes.json")
    vue = charger("vue_ensemble.json")
    niveaux = charger("niveaux.json")

    tot = artistes["totaux"]
    national = niveaux["doute_total"]

    # --- Profils : calculés pour les invariants, PAS exportés ---------------
    profils = []
    for a in artistes["artistes"]:
        par_code = {f["code"]: f["notices"] for f in a["familles"] if f["notices"]}
        inconnues = set(par_code) - set(MENTIONS)
        assert not inconnues, f"mention hors liste pour {a['nom']} : {inconnues}"
        assert sum(par_code.values()) == a["doute"], \
            f"profil non additif pour {a['nom']}"
        profils.append({"total": a["doute"], "mentions": par_code})

    associations = sum(p["total"] for p in profils)

    # --- Mentions : notices distinctes du volume portant chaque mention -----
    par_mention = {}
    occurrences = 0
    for code in MENTIONS:
        f = next(x for x in vue["familles"] if x["code"] == code)
        # mesuré sur le CSV par build_artistes, jamais déduit d'une somme de profils
        n_corpus = tot["familles_notices"][code]
        # associations : ce que totalisent les profils pour cette mention
        n_assoc = sum(p["mentions"].get(code, 0) for p in profils)
        assert n_assoc == f["dans_liste"], f"associations ≠ vue_ensemble pour {code}"
        assert n_corpus == f["dans_liste_notices"], f"notices ≠ vue_ensemble pour {code}"
        assert n_corpus <= n_assoc, f"notices > associations pour {code}"
        assert n_corpus <= f["global"], f"volume > Joconde pour {code}"
        par_mention[code] = {"corpus_notices": n_corpus}
        occurrences += n_corpus

    notices = tot["notices_doute"]
    partagees = tot["notices_partagees"]

    # --- Invariants d'unités, tous RELATIONNELS -----------------------------
    assert notices == vue["totaux"]["doute_notices_liste"], \
        "les deux exports n'annoncent pas la même ampleur"
    assert associations == tot["appartenances_doute"], \
        "associations ≠ appartenances d'artistes.json"
    assert notices + partagees == associations, \
        "notices distinctes + notices à deux artistes ≠ associations"
    assert occurrences >= notices, "moins d'occurrences de mentions que de notices"
    assert associations >= notices, "moins d'associations que de notices"
    assert len(profils) == len(artistes["artistes"]), "profils perdus en chemin"
    assert len(par_mention) == len(MENTIONS) == 8
    assert notices < national, "le volume ne peut pas dépasser le total national"

    corpus = {
        "source": artistes["source"],
        "url_source": artistes["url_source"],
        "version_donnee": artistes["version_donnee"],
        "critere_liste": artistes["critere"],
        "date_generation": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        # Les unités, nommées, avec leur effectif : le front ne les recalcule pas
        # et n'en invente pas une autre.
        "unites": {
            "notices_distinctes": notices,
            "occurrences_mentions": occurrences,
            "associations_artiste_notice": associations,
            "notices_partagees": partagees,
            "nb_artistes": len(profils),
            "nb_mentions": len(MENTIONS),
        },
        # Contexte national : le volume n'est PAS tout le phénomène.
        "national": {
            "notices_prudentes": national,
            "part_du_volume": round(notices / national, 4),
        },
        "mentions": par_mention,
        "notice_ouverture": notice_d_ouverture(artistes),
    }

    sortie = WEB / "corpus_maitres.json"
    sortie.write_text(json.dumps(corpus, ensure_ascii=False, indent=1), encoding="utf-8")

    poids = sortie.stat().st_size / 1024
    print(f"Écrit : {sortie.relative_to(RACINE)} ({poids:.1f} Ko)")
    print(f"\n{notices} notices distinctes | {occurrences} occurrences de mentions "
          f"| {associations} associations artiste-notice "
          f"({partagees} notices à deux artistes)")
    print(f"{len(profils)} artistes · {len(MENTIONS)} mentions · "
          f"{notices / national:.1%} des {national} notices prudentes de Joconde\n")
    print("mention                notices   part du volume")
    for code in MENTIONS:
        m = par_mention[code]
        print(f"{code:22} {m['corpus_notices']:7} {m['corpus_notices'] / notices:14.1%}")


if __name__ == "__main__":
    main()
