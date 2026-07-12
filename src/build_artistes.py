"""Export « Les presque » : le doute par maître de référence (phase 3).

Produit data/exports/web/artistes.json : pour chaque maître de la liste vedette
V1 (docs/decisions.md, 2026-07-07), la répartition des notices qui portent son
nom dans le champ Auteur — attribution ferme (« propre »), doute (ventilé par
famille et par niveau), et copie assumée (« d'après », catégorie à part) — plus
le nombre de musées et quelques notices réelles (liens POP).

Critère de la liste : maître de référence ET ≥ 20 notices de doute (hors copie),
comptage aligné sur markers.py (famille_segment, par segment du champ Auteur).

Désambiguïsation (docs/donnees.md, 2026-07-07) : chaque maître est défini par
des motifs INCLUS et EXCLUS sur le nom-pivot (parenthèses retirées, accents et
casse normalisés) pour écarter homonymes (Rembrandt ≠ R. Bugatti), familles
(Fragonard père ≠ fils) et fusionner les variantes de graphie (Le Primatice =
Primaticcio, Le Titien = Vecellio Tiziano).

Usage : uv run python src/build_artistes.py  (~2 min)
"""

import json
import re
import unicodedata
from datetime import datetime, timezone

import pandas as pd

import markers
from config import CHEMIN_CSV, DOSSIER_EXPORTS, URL_CSV

DOSSIER_WEB = DOSSIER_EXPORTS / "web"
TAILLE_MORCEAU = 200_000
# Notices réelles conservées par maître pour la vitrine « Œuvres » : une par
# famille présente, deux pour la famille dominante (decisions.md, 2026-07-11).
# Les exemples sont les PREMIERS rencontrés dans le CSV, pas choisis à la main
# (règle documentée dans methode-et-limites.md). 8 familles + 1 dominante = 9.
MAX_EXEMPLES = 9
EXEMPLES_PAR_FAMILLE = 2  # gardés au fil de l'eau ; la sortie n'en publie 2 que pour la dominante

# Niveau de chaque famille de doute (échelle typologie P2-T2).
NIVEAU_FAMILLE = {
    "attribue": 1, "point_interrogation": 1, "presume": 1,
    "ecole_de": 2, "atelier_de": 2, "entourage_de": 2, "suiveur_de": 2,
    "maniere_de": 3, "genre_de": 3,
}

COLONNES = ["Reference", "Auteur", "Domaine", "Code_Museofile",
            "Nom_officiel_musee", "Ville", "Titre"]

# Liste vedette V1. Chaque maître : (motifs inclus, motifs exclus) sur le pivot
# normalisé. Ordonnée par doute décroissant (mesuré 2026-07-07). Les deux
# familles écartées après désambiguïsation (Bruegel l'Ancien, Cranach l'Ancien,
# < 20 une fois le maître isolé) NE figurent pas ici — voir docs/decisions.md.
MAITRES = [
    ("Charles Le Brun",     ["LE BRUN CHARLES"], []),
    ("Le Primatice",        ["PRIMATICCIO", "PRIMATICE"], []),
    ("Ingres",              ["INGRES"], []),
    ("Rembrandt",           ["REMBRANDT"], ["BUGATTI"]),
    ("Michel-Ange",         ["BUONARROTI", "MICHELANGELO", "MICHEL-ANGE"], []),
    ("Rubens",              ["RUBENS"], []),
    ("François Clouet",     ["CLOUET FRANCOIS"], []),
    ("Annibale Carracci",   ["CARRACCI ANNIBALE"], []),
    ("Rodin",               ["RODIN AUGUSTE", "RODIN"], []),
    ("Boucher",             ["BOUCHER FRANCOIS"], []),
    ("Andrea del Sarto",    ["SARTO ANDREA", "ANDREA DEL SARTO"], []),
    ("Guido Reni",          ["RENI GUIDO"], []),
    ("Léonard de Vinci",    ["VINCI"], []),
    ("Le Tintoret",         ["TINTORET", "ROBUSTI"], []),
    ("Nicolas Poussin",     ["POUSSIN NICOLAS", "POUSSIN"], []),
    ("Simon Vouet",         ["VOUET"], []),
    ("Greuze",              ["GREUZE"], []),
    ("Van Dyck",            ["DYCK"], []),
    ("Le Corrège",          ["CORREGE", "ALLEGRI ANTONIO"], []),
    ("Pierre Mignard",      ["MIGNARD PIERRE"], []),
    ("Véronèse",            ["VERONESE", "CALIARI"], []),
    ("Hyacinthe Rigaud",    ["RIGAUD HYACINTHE"], []),
    ("Géricault",           ["GERICAULT"], []),
    ("Fragonard",           ["FRAGONARD JEAN-HONORE", "FRAGONARD JEAN HONORE"], []),
    ("Raphaël",             ["RAPHAEL", "SANZIO"], ["ATELIER"]),
    ("Ribera",              ["RIBERA"], []),
    ("Titien",              ["TIZIANO", "LE TITIEN", "VECELLIO"], []),
]

LIBELLES_NIVEAUX = {1: "Presque lui", 2: "Autour de lui", 3: "Son style, sans lui"}
LIBELLE_FAMILLE = {f.code: f.libelle for f in markers.FAMILLES}


def _sans_accents(chaine: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", chaine)
                   if unicodedata.category(c) != "Mn")


def _pivot(segment: str) -> str:
    """Nom-pivot : parenthèses retirées, espaces compactés, accents/casse ôtés."""
    sans_paren = markers._RE_PARENTHESES.sub("", segment)
    return _sans_accents(re.sub(r"\s+", " ", sans_paren).strip(" ,;").upper())


def _trouve_maitre(pivot: str):
    for nom, inclus, exclus in MAITRES:
        if any(e in pivot for e in exclus):
            continue
        if any(i in pivot for i in inclus):
            return nom
    return None


def _vide() -> dict:
    return {"propre": 0, "doute": 0, "copie": 0, "musees": set(),
            "familles": {}, "niveaux": {1: 0, 2: 0, 3: 0},
            "exemples": {}, "exemple_copie": None}


def _exemple(ref, titre, musee, ville, segment) -> dict:
    """Une notice réelle pour la vitrine : lien POP + les mots exacts du musée."""
    return {
        "reference": ref,
        "titre": titre if isinstance(titre, str) else None,
        "musee": musee if isinstance(musee, str) else None,
        "ville": ville if isinstance(ville, str) else None,
        "extrait": segment,
    }


def main() -> None:
    agg = {nom: _vide() for nom, *_ in MAITRES}
    total = 0

    morceaux = pd.read_csv(CHEMIN_CSV, sep="|", usecols=COLONNES, dtype=str,
                           chunksize=TAILLE_MORCEAU)
    for morceau in morceaux:
        total += len(morceau)
        for ref, aut, dom, code, musee, ville, titre in zip(
            morceau["Reference"], morceau["Auteur"], morceau["Domaine"],
            morceau["Code_Museofile"], morceau["Nom_officiel_musee"],
            morceau["Ville"], morceau["Titre"],
        ):
            if not isinstance(aut, str):
                continue
            en_ba = markers._dans_beaux_arts(dom)
            for segment in aut.split(";"):
                segment = segment.strip()
                if not segment:
                    continue
                nom = _trouve_maitre(_pivot(segment))
                if nom is None:
                    continue
                a = agg[nom]
                categorie, famille = markers.famille_segment(segment, en_ba)
                if isinstance(code, str):
                    a["musees"].add(code)
                if categorie == "propre":
                    a["propre"] += 1
                elif categorie == "copie":
                    a["copie"] += 1
                    # une notice réelle de copie « d'après », pour le bloc « À part »
                    if a["exemple_copie"] is None and isinstance(ref, str):
                        a["exemple_copie"] = _exemple(ref, titre, musee, ville, segment)
                elif categorie == "doute":
                    a["doute"] += 1
                    a["familles"][famille] = a["familles"].get(famille, 0) + 1
                    a["niveaux"][NIVEAU_FAMILLE[famille]] += 1
                    # jusqu'à 2 notices réelles par famille (les premières
                    # rencontrées) ; la sortie n'en publie 2 que pour la dominante
                    exs = a["exemples"].setdefault(famille, [])
                    if len(exs) < EXEMPLES_PAR_FAMILLE and isinstance(ref, str):
                        exs.append(_exemple(ref, titre, musee, ville, segment))
        print(f"\r  {total:,} notices lues".replace(",", " "), end="", flush=True)
    print()

    artistes = []
    for nom, *_ in MAITRES:
        a = agg[nom]
        familles = {code: a["familles"][code]
                    for code in markers.DOUTE_PAR_NIVEAU if code in a["familles"]}
        # Exemples pour la vitrine : ordre canonique des familles (le même que
        # l'axe du graphique), code de famille EXPORTÉ avec chaque exemple (le
        # front ne re-parse jamais les extraits), 2 exemples pour la dominante.
        dominante = max(familles, key=familles.get) if familles else None
        exemples = []
        for code in markers.DOUTE_PAR_NIVEAU:
            if code not in a["exemples"]:
                continue
            garde = 2 if code == dominante else 1
            for ex in a["exemples"][code][:garde]:
                exemples.append({"code": code, **ex})
        artistes.append({
            "nom": nom,
            "propre": a["propre"],
            "doute": a["doute"],
            "copie": a["copie"],
            "musees": len(a["musees"]),
            "niveaux": [a["niveaux"][1], a["niveaux"][2], a["niveaux"][3]],
            "familles": [
                {"code": code, "libelle": LIBELLE_FAMILLE[code],
                 "niveau": NIVEAU_FAMILLE[code], "notices": n}
                for code, n in familles.items()
            ],
            "exemples": exemples[:MAX_EXEMPLES],
            "exemple_copie": a["exemple_copie"],
        })
    artistes.sort(key=lambda x: x["doute"], reverse=True)

    sortie = {
        "critere": "maître de référence ET ≥ 20 notices de doute (hors copie)",
        "lexique": "markers.py v2 (famille_segment, par segment du champ Auteur)",
        "version_donnee": "2026-07-01",
        "date_generation": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "source": "Collections des musées de France : base Joconde",
        "url_source": URL_CSV,
        "niveaux": {str(n): LIBELLES_NIVEAUX[n] for n in (1, 2, 3)},
        "artistes": artistes,
    }

    DOSSIER_WEB.mkdir(parents=True, exist_ok=True)
    chemin = DOSSIER_WEB / "artistes.json"
    chemin.write_text(json.dumps(sortie, ensure_ascii=False, indent=1),
                      encoding="utf-8")

    print(f"\n{len(artistes)} maîtres exportés → {chemin} "
          f"({chemin.stat().st_size / 1024:.1f} Ko)")
    print(f"{'maître':22} {'doute':>6} {'propre':>7} {'copie':>6} {'musées':>7}")
    for art in artistes:
        print(f"{art['nom']:22} {art['doute']:>6} {art['propre']:>7} "
              f"{art['copie']:>6} {art['musees']:>7}")


if __name__ == "__main__":
    main()
