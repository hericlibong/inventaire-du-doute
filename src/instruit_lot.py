"""Instruction d'un lot de candidats — tout ce qu'il faut pour trancher, en une passe.

Le registre `candidats_maitres.csv` liste des FORMES, pas des personnes : il dit
que « PINOT Charles François » porte 71 notices prudentes, pas que « PINOT
Charles » (11 notices) est le même homme, ni que « Pellerin » est une imagerie
et non quelqu'un. Instruire un candidat demande de voir toutes ses graphies
ensemble, ses musées, ses domaines et de vraies notices.

Ce script fait ce relevé pour une liste de RACINES de noms, en une seule lecture
du CSV (~2 min). Il ne décide rien : il rassemble les pièces. La décision
— identité, homonymes, parents, ateliers, raisons sociales — se prend ensuite à
l'œil, une personne à la fois, et s'inscrit dans la table de `build_artistes.py`.

Sortie : data/exports/lot_instruction.json (relevé complet, versionné — c'est la
pièce sur laquelle chaque verdict du lot a été rendu) + un rapport lisible sur la
sortie standard.

Usage : uv run python src/instruit_lot.py
"""

import json
import re
import sys
from collections import Counter, defaultdict

import pandas as pd

import markers
from build_artistes import _pivot
from candidats_maitres import nom_seul
from config import CHEMIN_CSV, DOSSIER_EXPORTS

TAILLE_MORCEAU = 200_000
COLONNES = ["Reference", "Auteur", "Domaine", "Code_Museofile",
            "Nom_officiel_musee", "Ville", "Titre"]
SORTIE = DOSSIER_EXPORTS / "lot_instruction.json"

# Racines du lot 2 (2026-08-02) : les 50 formes « à instruire » du registre qui
# portent au moins 25 notices prudentes. Une racine est un fragment de nom, pas
# un nom complet : « PINOT » rassemble « PINOT Charles François » et « PINOT
# Charles » — c'est précisément ce qu'on cherche à voir. Quelques racines sont
# volontairement larges (DAVID, PETER, PREVOST) : elles servent à mesurer
# l'homonymie, pas à rattacher.
RACINES = [
    "BARLA", "CLAUSEL", "NORMAND", "TIRODE", "MORINET", "CALANDRUCCI",
    "BIGOT", "FORT", "DUTHOIT", "PINOT", "GIRAUD", "VACQUERIE", "GEORGIN",
    "VERJAT", "HAWKE", "MELLET", "PETER", "ALLEAUME", "WILLERMET",
    "PELLERIN", "TURPIN", "HUGO", "LANCELOT", "DU RY", "RY CHARLES",
    "BUQUET", "ROCHE ODILON", "HOGENBERG", "MURSHIDABAD", "MOGHOLE",
    "ENSFELDER", "HOFFMANN", "BERNAERTS", "PASSE CRISPIN", "VAN DE PASSE",
    "CRAPELET", "VARADY", "BEURET", "LELOY", "HUSSENOT", "DAVID",
    "POLLAIUOLO", "PREVOST", "HENNAULT", "HENRIET", "ACKERMANN", "HERTIG",
    "COTER",
]

# Les racines les plus courtes ne valent que comme MOT ENTIER, sinon « FORT »
# ramasse « BEAUFORT » et « HUGO » ramasse « HUGOT ».
_MOTS = {re.compile(rf"\b{re.escape(r)}\b") for r in RACINES}


def _racines_du_pivot(pivot: str) -> list[str]:
    return [r for r in RACINES if re.search(rf"\b{re.escape(r)}\b", pivot)]


# Les dates de vie écrites par le musée dans le champ Auteur — « Barla
# Jean-Baptiste (1817-1896) ». C'est le seul indice d'identité présent dans la
# source elle-même : il sépare deux homonymes et rapproche deux graphies d'un
# même homme mieux que n'importe quelle intuition.
_RE_DATES = re.compile(r"\(\s*(?:vers\s+|actif\s+|c\.\s*)?"
                       r"(\d{3,4}\??)\s*-\s*(\d{0,4}\??)\s*\)")


def _vide() -> dict:
    return {"prudentes": set(), "certaines": set(), "copies": set(),
            "familles": Counter(), "domaines": Counter(),
            "musees": defaultdict(set), "noms_musees": {},
            "graphies": Counter(), "dates": Counter(), "exemples": []}


def main() -> None:
    # clé = nom débarrassé de sa formule (l'unité du registre)
    releve: dict[str, dict] = defaultdict(_vide)
    racine_du_nom: dict[str, set] = defaultdict(set)
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
            if not isinstance(aut, str) or not isinstance(ref, str):
                continue
            en_ba = markers._dans_beaux_arts(dom)
            for segment in aut.split(";"):
                segment = segment.strip()
                if not segment:
                    continue
                pivot = _pivot(segment)
                racines = _racines_du_pivot(pivot)
                if not racines:
                    continue
                nom = nom_seul(segment) or pivot
                categorie, famille = markers.famille_segment(segment, en_ba)
                r = releve[nom]
                racine_du_nom[nom].update(racines)
                r["graphies"][segment] += 1
                for d1, d2 in _RE_DATES.findall(segment):
                    r["dates"][f"{d1}-{d2}"] += 1
                if isinstance(dom, str):
                    r["domaines"][dom.split(";")[0].strip()] += 1
                if categorie == "doute":
                    r["prudentes"].add(ref)
                    r["familles"][famille] += 1
                    if isinstance(code, str) and code.strip():
                        r["musees"][code].add(ref)
                        r["noms_musees"][code] = f"{musee} · {ville}"
                    if len(r["exemples"]) < 6:
                        r["exemples"].append({
                            "reference": ref, "segment": segment,
                            "titre": titre if isinstance(titre, str) else None,
                            "musee": r["noms_musees"].get(code),
                            "domaine": dom if isinstance(dom, str) else None,
                        })
                elif categorie == "copie":
                    r["copies"].add(ref)
                else:
                    r["certaines"].add(ref)
        print(f"\r  {total:,} notices lues".replace(",", " "), end="", flush=True)
    print()

    sortie = {}
    for nom, r in releve.items():
        sortie[nom] = {
            "racines": sorted(racine_du_nom[nom]),
            "prudentes": len(r["prudentes"]),
            "certaines": len(r["certaines"]),
            "copies": len(r["copies"]),
            "familles": dict(r["familles"].most_common()),
            "domaines": dict(r["domaines"].most_common(6)),
            "graphies": dict(r["graphies"].most_common()),
            "dates": dict(r["dates"].most_common(8)),
            # les références prudentes elles-mêmes : c'est ce qui permet de voir
            # que les 41 notices de « MELLET Jacques Père » sont EXACTEMENT
            # celles de « MELLET Jules Fils ». Plafonnées : au-delà, le
            # recouvrement ne se mesure plus à l'œil de toute façon.
            "references": sorted(r["prudentes"])[:400],
            "musees": [{"code": c, "nom": r["noms_musees"].get(c, ""),
                        "prudentes": len(refs)}
                       for c, refs in sorted(r["musees"].items(),
                                             key=lambda x: -len(x[1]))],
            "exemples": r["exemples"],
        }

    SORTIE.parent.mkdir(parents=True, exist_ok=True)
    SORTIE.write_text(json.dumps(sortie, ensure_ascii=False, indent=1),
                      encoding="utf-8")
    print(f"\n{len(sortie)} noms relevés → {SORTIE}")

    for racine in RACINES:
        noms = [(n, d) for n, d in sortie.items() if racine in d["racines"]]
        noms.sort(key=lambda x: -x[1]["prudentes"])
        total_r = sum(d["prudentes"] for _, d in noms)
        print(f"\n=== {racine} — {len(noms)} formes, {total_r} notices prudentes")
        for nom, d in noms[:12]:
            if not d["prudentes"] and not d["certaines"]:
                continue
            mus = d["musees"][0]["nom"] if d["musees"] else "—"
            print(f"  {d['prudentes']:>5} prud. {d['certaines']:>5} cert. "
                  f"{len(d['musees']):>3} mus.  {nom[:44]:<44} {mus[:44]}")
        if len(noms) > 12:
            print(f"  … et {len(noms) - 12} autres formes")


if __name__ == "__main__":
    sys.exit(main())
