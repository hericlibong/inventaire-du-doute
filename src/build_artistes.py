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
            "Nom_officiel_musee", "Ville", "Titre", "coordonnees"]

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


def _mot_entier(motif: str, pivot: str) -> bool:
    """Le motif apparaît-il comme MOT ENTIER dans le pivot ? On a longtemps testé
    par simple sous-chaîne (`motif in pivot`), ce qui rattachait à tort des noms
    différents partageant une racine : « SERODINE » → Rodin, « VINCIDOR » → Vinci,
    « SOLDYCK » → Van Dyck, « RIBERAT » → Ribera, « TINTORETTO Domenico » (le fils)
    → Le Tintoret (decisions.md / donnees.md, 2026-07-13). Le test mot entier lève
    l'ambiguïté ; les vraies notices restent prises (« Le Tintoret ou il Tintoretto »
    contient bien le mot « Tintoret »). Frontières de mot sur le pivot déjà
    normalisé (majuscules, sans accents)."""
    return re.search(rf"\b{re.escape(motif)}\b", pivot) is not None


def _trouve_maitre(pivot: str):
    for nom, inclus, exclus in MAITRES:
        if any(_mot_entier(e, pivot) for e in exclus):
            continue
        if any(_mot_entier(i, pivot) for i in inclus):
            return nom
    return None


def _vide() -> dict:
    return {"propre": 0, "doute": 0, "copie": 0, "musees": set(),
            "familles": {}, "niveaux": {1: 0, 2: 0, 3: 0},
            "exemples": {}, "exemple_copie": None,
            # Références déjà retenues en exemple pour CE maître, toutes familles
            # confondues : une même notice ne doit illustrer la vitrine qu'une fois.
            # Une notice peut en effet nommer le maître DEUX FOIS sous deux graphies
            # (« VECELLIO Tiziano (attribué à) » et « LE TITIEN (dit, attribué à) »
            # sur la même œuvre du Louvre) : sans ce garde-fou, on publiait deux
            # entrées pour la même œuvre.
            "refs_exemples": set(),
            # ventilation du doute SEUL par musée détenteur (carte par maître) :
            # code -> {doute, nom, ville, coord, familles, niveaux}
            "musees_doute": {},
            # doute rattaché à aucun code musée (non cartographiable) : sert à
            # boucler l'invariant de comptage. Attendu ~0.
            "doute_sans_code": 0}


def _exemple(ref, titre, musee, ville, segment) -> dict:
    """Une notice réelle pour la vitrine : lien POP + les mots exacts du musée."""
    return {
        "reference": ref,
        "titre": titre if isinstance(titre, str) else None,
        "musee": musee if isinstance(musee, str) else None,
        "ville": ville if isinstance(ville, str) else None,
        "extrait": segment,
    }


def _lat_lon(valeur):
    """« lat, lon » (champ Joconde, au grain musée) → (lat, lon) arrondis, ou
    (None, None). On sépare lat et lon EXPLICITEMENT pour écarter tout risque
    d'inversion côté carte D3-geo (decisions.md, 2026-07-12)."""
    if not isinstance(valeur, str) or "," not in valeur:
        return None, None
    try:
        lat, lon = (float(x) for x in valeur.split(",")[:2])
    except ValueError:
        return None, None
    return round(lat, 5), round(lon, 5)


def main() -> None:
    agg = {nom: _vide() for nom, *_ in MAITRES}
    total = 0

    morceaux = pd.read_csv(CHEMIN_CSV, sep="|", usecols=COLONNES, dtype=str,
                           chunksize=TAILLE_MORCEAU)
    for morceau in morceaux:
        total += len(morceau)
        for ref, aut, dom, code, musee, ville, titre, coord in zip(
            morceau["Reference"], morceau["Auteur"], morceau["Domaine"],
            morceau["Code_Museofile"], morceau["Nom_officiel_musee"],
            morceau["Ville"], morceau["Titre"], morceau["coordonnees"],
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
                    # ventilation du doute par musée détenteur (carte par maître).
                    # Alimentée UNIQUEMENT ici : jamais sur le ferme ni la copie.
                    if isinstance(code, str) and code.strip():
                        md = a["musees_doute"].get(code)
                        if md is None:
                            md = a["musees_doute"][code] = {
                                "doute": 0,
                                "nom": musee if isinstance(musee, str) else None,
                                "ville": ville if isinstance(ville, str) else None,
                                "coord": coord if isinstance(coord, str) else None,
                                "familles": {}, "niveaux": {1: 0, 2: 0, 3: 0},
                                # Première (et, si doute==1, unique) notice du musée :
                                # sert à rendre les points « 1 œuvre » cliquables vers
                                # POP (n'est exporté que dans ce cas, voir plus bas).
                                "ref1": ref if isinstance(ref, str) else None,
                                "titre1": titre if isinstance(titre, str) else None}
                        md["doute"] += 1
                        md["familles"][famille] = md["familles"].get(famille, 0) + 1
                        md["niveaux"][NIVEAU_FAMILLE[famille]] += 1
                    else:
                        a["doute_sans_code"] += 1
                    # jusqu'à 2 notices réelles par famille (les premières
                    # rencontrées) ; la sortie n'en publie 2 que pour la dominante
                    exs = a["exemples"].setdefault(famille, [])
                    if (len(exs) < EXEMPLES_PAR_FAMILLE and isinstance(ref, str)
                            and ref not in a["refs_exemples"]):
                        exs.append(_exemple(ref, titre, musee, ville, segment))
                        a["refs_exemples"].add(ref)
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

        # Musées du doute : 1 entrée = 1 musée détenteur, doute SEUL, trié.
        musees_doute = []
        for code, md in a["musees_doute"].items():
            fam_liste = [{"code": c, "notices": md["familles"][c]}
                         for c in markers.DOUTE_PAR_NIVEAU if c in md["familles"]]
            niveaux = [md["niveaux"][1], md["niveaux"][2], md["niveaux"][3]]
            lat, lon = _lat_lon(md["coord"])
            # Invariants de comptage par musée : aucune ambiguïté possible.
            assert sum(f["notices"] for f in fam_liste) == md["doute"], \
                f"familles ≠ doute ({nom} / {code})"
            assert sum(niveaux) == md["doute"], \
                f"niveaux ≠ doute ({nom} / {code})"
            entree = {
                "code": code,
                "nom": md["nom"],
                "ville": md["ville"],
                "lat": lat,
                "lon": lon,
                "doute": md["doute"],
                "niveaux": niveaux,
                "familles": fam_liste,
            }
            # Musée à UNE seule œuvre concernée : on joint la référence (et le titre
            # s'il existe) de cette œuvre, pour rendre le point cliquable vers sa
            # fiche publique POP. Les entrées multi-œuvres restent inchangées.
            if md["doute"] == 1 and md["ref1"]:
                entree["oeuvre_unique"] = {
                    "reference": md["ref1"],
                    "titre": md["titre1"],
                }
            musees_doute.append(entree)
        musees_doute.sort(key=lambda m: m["doute"], reverse=True)
        # Invariant par maître : doute cartographié + doute sans code = doute total.
        assert (sum(m["doute"] for m in musees_doute) + a["doute_sans_code"]
                == a["doute"]), f"somme musées ≠ doute maître ({nom})"

        principal = musees_doute[0] if musees_doute else None
        musee_principal = None if principal is None else {
            "code": principal["code"],
            "nom": principal["nom"],
            "doute": principal["doute"],
            "part": round(principal["doute"] / a["doute"], 3) if a["doute"] else 0,
        }

        artistes.append({
            "nom": nom,
            "propre": a["propre"],
            "doute": a["doute"],
            "copie": a["copie"],
            "musees": len(a["musees"]),
            "nb_musees_doute": len(musees_doute),
            "musee_principal": musee_principal,
            "doute_sans_musee": a["doute_sans_code"],
            "niveaux": [a["niveaux"][1], a["niveaux"][2], a["niveaux"][3]],
            "familles": [
                {"code": code, "libelle": LIBELLE_FAMILLE[code],
                 "niveau": NIVEAU_FAMILLE[code], "notices": n}
                for code, n in familles.items()
            ],
            "exemples": exemples[:MAX_EXEMPLES],
            "exemple_copie": a["exemple_copie"],
            "musees_doute": musees_doute,
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
    print(f"{'maître':22} {'doute':>6} {'propre':>7} {'copie':>6} "
          f"{'mus.doute':>9} {'top %':>6}")
    for art in artistes:
        part = art["musee_principal"]["part"] if art["musee_principal"] else 0
        print(f"{art['nom']:22} {art['doute']:>6} {art['propre']:>7} "
              f"{art['copie']:>6} {art['nb_musees_doute']:>9} {part:>6.0%}")
    total_sans_musee = sum(art["doute_sans_musee"] for art in artistes)
    print(f"\nDoute sans code musée (non cartographiable) : {total_sans_musee}")


if __name__ == "__main__":
    main()
