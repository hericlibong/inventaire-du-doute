"""Export « Les presque » : le doute par maître de référence (phase 3).

Produit data/exports/web/artistes.json : pour chaque maître de la liste vedette
V1 (docs/decisions.md, 2026-07-07), la répartition des notices qui portent son
nom dans le champ Auteur — attribution ferme (« propre »), doute (ventilé par
famille et par niveau), et copie assumée (« d'après », catégorie à part) — plus
le nombre de musées et quelques notices réelles (liens POP).

Critère de la liste : maître de référence ET ≥ 20 notices de doute (hors copie),
lexique aligné sur markers.py (famille_segment).

Unité de comptage : la RÉFÉRENCE Joconde, pas le segment d'auteur (decisions.md,
2026-07-21 quater). Une notice qui nomme le maître deux fois sous deux graphies
— « VECELLIO Tiziano (attribué à) ; LE TITIEN (dit, attribué à) » — ne pesait
qu'une fois pour le public mais deux fois dans le comptage. Chaque référence est
donc résolue en UNE catégorie et UNE famille avant d'être ajoutée.

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
#
# TABLE RELUE À L'ŒIL (2026-07-21, temps 2) à partir de l'inventaire des 246
# formes d'auteur réellement captées, mentions prudentes ET certaines. Deux
# outils, pas un de plus : l'ancre « ^ » (le nom doit être en tête, voir
# _mot_entier) et l'exclusion nommée. Chaque exclusion dit QUI elle écarte :
# c'est cette liste qui sera publiée avec la page méthode.
MAITRES = [
    ("Charles Le Brun",     ["LE BRUN CHARLES"], []),
    ("Le Primatice",        ["PRIMATICCIO", "PRIMATICE"], []),
    # « MADAME INGRES » est écartée par l'ancre ; Jean Marie Joseph Ingres est
    # un autre homme.
    ("Ingres",              ["^INGRES"], ["JEAN MARIE JOSEPH"]),
    ("Rembrandt",           ["REMBRANDT"], ["BUGATTI"]),
    # L'ancre suffit à écarter les 16 homonymes qui portent Michelangelo ou
    # Michel-Ange en PRÉNOM : Corneille Michel-Ange (422 mentions certaines !),
    # Cerquozzi, Merisi dit Le Caravage, Pace, Anselmi, Pistoletto, Challe,
    # Slodtz, Campidoglio, Membrini, Aliprandi, Unterperger, Yrazazbal,
    # Ricciolini, Pollet. Aucune exclusion nommée n'est nécessaire.
    ("Michel-Ange",         ["^BUONARROTI", "^BUONAROTTI", "^MICHEL-ANGE"], []),
    # Arnold Frans Rubens et le « Rubens des batailles » (Snayers) ne sont pas lui.
    ("Rubens",              ["RUBENS"], ["ARNOLD", "BATAILLES"]),
    ("François Clouet",     ["CLOUET FRANCOIS"], []),
    ("Annibale Carracci",   ["CARRACCI ANNIBALE"], []),
    ("Rodin",               ["RODIN AUGUSTE"], []),
    ("Boucher",             ["BOUCHER FRANCOIS"], []),
    ("Andrea del Sarto",    ["SARTO ANDREA", "ANDREA DEL SARTO"], []),
    ("Guido Reni",          ["RENI GUIDO"], []),
    # Pierino da Vinci (le neveu sculpteur) et Marguerite Vinci écartés.
    ("Léonard de Vinci",    ["^VINCI", "^LEONARD DE VINCI", "^DE VINCI",
                             "^LEONARDO DA VINCI", "^LEONARDO DI SER PIERO"],
                            ["PIERINO", "MARGUERITE"]),
    # Domenico Robusti est le fils de Jacopo.
    ("Le Tintoret",         ["TINTORET", "^ROBUSTI"], ["DOMENICO"]),
    # L'ancre écarte Lemaire-Poussin, Lavallée-Poussin, Gaspard Poussin (Dughet)
    # et Le Guaspre ; reste Poussin-Heydeck, qui commence bien par Poussin.
    ("Nicolas Poussin",     ["^POUSSIN"], ["HEYDECK"]),
    # Aubin et Ferdinand Vouet sont écartés par la précision du motif.
    ("Simon Vouet",         ["VOUET SIMON"], []),
    ("Greuze",              ["GREUZE"], []),
    # Philip van Dyck, Philippe et Pierre Van Dyck ne sont pas Antoon.
    ("Van Dyck",            ["DYCK"], ["PHILIP", "PHILIPPE", "PIERRE"]),
    ("Le Corrège",          ["CORREGE", "ALLEGRI ANTONIO"], []),
    # Pierre Mignard II, le neveu.
    ("Pierre Mignard",      ["MIGNARD PIERRE"], ["PIERRE II"]),
    # Le fils Carlo, le frère Benedetto, le neveu Gabriele ; Bonifazio de'
    # Pitati et Zenone da Verona portent « Veronese » comme surnom de ville.
    ("Véronèse",            ["^VERONESE", "^CALIARI"],
                            ["CARLO", "BENEDETTO", "GABRIELE",
                             "BONIFAZIO", "BONIFACIO"]),
    ("Hyacinthe Rigaud",    ["RIGAUD HYACINTHE"], []),
    ("Géricault",           ["GERICAULT"], []),
    ("Fragonard",           ["FRAGONARD JEAN-HONORE", "FRAGONARD JEAN HONORE"], []),
    # Le cas le plus pollué : 59 formes captées, « Raphaël » servant de prénom à
    # une cinquantaine de personnes (Lonne, Lardeur, Mengs, Collin, Sadeler,
    # Freida…). L'ancre les écarte toutes ; restent l'affichiste Raphael Tuck,
    # le graveur Raphael-Schwartz, et Giovanni Santi, le père.
    # L'ancre remplace aussi l'ancienne exclusion « ATELIER », qui servait à
    # écarter les noms d'atelier (« ATELIER DE RAPHAEL ») : ils ne commencent
    # pas par le nom du maître. Et « SANTI Raffaello », sa forme d'état civil,
    # n'était captée par aucun motif — un faux négatif au sein même des 27.
    ("Raphaël",             ["^RAPHAEL", "^SANZIO", "^SANTI RAFFAELLO",
                             "^RAFFAELLO"], ["TUCK", "SCHWARTZ", "GIOVANNI"]),
    # Roman Ribera y Cirera et Pierre Ribera.
    ("Ribera",              ["RIBERA"], ["CIRERA", "PIERRE"]),
    # Francesco et Cesare Vecellio sont de la famille, pas Tiziano ; Tiziano
    # Aspetti est écarté faute de motif sur le seul prénom.
    ("Titien",              ["LE TITIEN", "^VECELLIO"], ["FRANCESCO", "CESARE"]),
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
    normalisé (majuscules, sans accents).

    Un motif préfixé de « ^ » ne vaut qu'en TÊTE du nom. Joconde écrit l'auteur
    « NOM Prénom » : sans cette ancre, « Raphaël » se rattache à Raphaël Collin ou
    Anton Raphael Mengs, et « Michel-Ange » à Corneille Michel-Ange
    (donnees.md, 2026-07-21). L'ancre n'est posée que là où elle est nécessaire :
    « ÉCOLE DE PRIMATICCIO » doit rester pris, le nom n'y est pas en tête."""
    if motif.startswith("^"):
        return re.match(rf"{re.escape(motif[1:])}\b", pivot) is not None
    return re.search(rf"\b{re.escape(motif)}\b", pivot) is not None


def _trouve_maitre(pivot: str):
    for nom, inclus, exclus in MAITRES:
        if any(_mot_entier(e, pivot) for e in exclus):
            continue
        if any(_mot_entier(i, pivot) for i in inclus):
            return nom
    return None


def _categorie_retenue(categories: set) -> str | None:
    """Une même référence peut nommer le maître plusieurs fois, avec des liens
    différents (« POUSSIN Nicolas (attribué à) ; POUSSIN Nicolas »). Elle ne
    compte qu'UNE fois, et du côté le plus prudent : le doute l'emporte sur la
    copie, la copie sur l'attribution ferme. C'est ce qui rend propre / doute /
    copie réellement disjoints, donc additionnables (decisions.md, 2026-07-21).
    Les segments écartés (atelier hors beaux-arts, école-lieu) ne comptent pas."""
    for categorie in ("doute", "copie", "propre"):
        if categorie in categories:
            return categorie
    return None


def _famille_retenue(familles: dict) -> str:
    """Même chose au grain de la famille : trois références de Simon Vouet
    (M0332004170 à 172) portent à la fois « VOUET Simon (?) » et « VOUET Simon
    (atelier, dessinateur) ». Le « ? » l'emporte — c'est le marqueur de doute le
    plus explicite — puis l'ordre canonique des familles. Une référence = une
    famille : les familles et les niveaux totalisent exactement le doute
    (arbitrage utilisateur, option c, decisions.md 2026-07-21)."""
    if "point_interrogation" in familles:
        return "point_interrogation"
    return next(c for c in markers.DOUTE_PAR_NIVEAU if c in familles)


def _vide() -> dict:
    return {"propre": 0, "doute": 0, "copie": 0, "musees": set(),
            "familles": {}, "niveaux": {1: 0, 2: 0, 3: 0},
            "exemples": {}, "exemple_copie": None,
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
            # Premier temps : que dit CETTE référence de CHAQUE maître ? On
            # collecte sans rien compter — le comptage vient après, une fois par
            # couple (maître, référence). Les références sont uniques dans le CSV
            # (vérifié le 2026-07-21 : 1 023 705 lignes, 1 023 705 références),
            # la déduplication tient donc entièrement dans la ligne courante.
            vus = {}  # maître -> {categories: set, familles: {code: segment}, copie: segment}
            for segment in aut.split(";"):
                segment = segment.strip()
                if not segment:
                    continue
                nom = _trouve_maitre(_pivot(segment))
                if nom is None:
                    continue
                categorie, famille = markers.famille_segment(segment, en_ba)
                vu = vus.setdefault(nom, {"categories": set(), "familles": {},
                                          "copie": None})
                vu["categories"].add(categorie)
                if categorie == "doute":
                    # on garde le premier segment vu pour chaque famille : c'est
                    # lui qui fournira l'extrait cité dans la vitrine « Œuvres »
                    vu["familles"].setdefault(famille, segment)
                elif categorie == "copie" and vu["copie"] is None:
                    vu["copie"] = segment

            # Second temps : une référence, un poids, par maître.
            for nom, vu in vus.items():
                a = agg[nom]
                if isinstance(code, str):
                    a["musees"].add(code)
                categorie = _categorie_retenue(vu["categories"])
                if categorie == "propre":
                    a["propre"] += 1
                elif categorie == "copie":
                    a["copie"] += 1
                    # une notice réelle de copie « d'après », pour le bloc « À part »
                    if a["exemple_copie"] is None and isinstance(ref, str):
                        a["exemple_copie"] = _exemple(ref, titre, musee, ville,
                                                      vu["copie"])
                elif categorie == "doute":
                    famille = _famille_retenue(vu["familles"])
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
                    # (une référence ne traverse ce bloc qu'une fois par maître :
                    # elle ne peut plus illustrer deux familles, comme le faisait
                    # l'œuvre du Louvre nommant Titien sous deux graphies)
                    exs = a["exemples"].setdefault(famille, [])
                    if len(exs) < EXEMPLES_PAR_FAMILLE and isinstance(ref, str):
                        exs.append(_exemple(ref, titre, musee, ville,
                                            vu["familles"][famille]))
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
        "lexique": "markers.py v2 (famille_segment) — unité : référence Joconde unique",
        "unite": "reference",
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
