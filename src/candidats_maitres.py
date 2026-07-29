"""Temps 4 — tous les candidats de la base, au seuil de 10 notices prudentes.

La liste des 27 maîtres avait été composée à la main le 2026-07-07 : personne
n'avait vérifié qui d'autre, dans la base, portait autant de mentions prudentes.
L'audit du 2026-07-21 a montré que Le Guerchin, Bouchardon ou Jules Romain
dépassaient largement l'ancien seuil sans avoir jamais été examinés.

Ce script compte, pour TOUTE forme d'auteur de la base, le nombre de RÉFÉRENCES
distinctes portant une formulation prudente (copies « d'après » exclues), et
publie celles qui atteignent 10 — retenues comme écartées. C'est la pièce qui
rend la sélection contrôlable : sans elle, la liste des maîtres est un panthéon
opaque (decisions.md, 2026-07-21 quater, décision 4).

Le comptage est fait PAR FORME, avant fusion des graphies et avant
désambiguïsation : « LE PRIMATICE » et « PRIMATICCIO Francesco » y figurent
séparément. Ce sont des pistes à instruire, pas des profils prêts à publier —
le rapprochement des graphies et l'écart des homonymes se font au temps 5, un
candidat à la fois, dans la table de build_artistes.py.

Usage : uv run python src/candidats_maitres.py  (~2 min)
"""

import csv
import re
from datetime import datetime, timezone

import pandas as pd

import markers
from build_artistes import MAITRES, _pivot, _trouve_maitre
from config import CHEMIN_CSV, DOSSIER_EXPORTS

SEUIL = 10
TAILLE_MORCEAU = 200_000
COLONNES = ["Reference", "Auteur", "Domaine", "Code_Museofile"]
SORTIE = DOSSIER_EXPORTS / "candidats_maitres.csv"

# Formules à retirer du nom : le qualificatif n'est pas toujours entre
# parenthèses (« INGRES Jean-Auguste-Dominique attribué à », 189 références —
# donnees.md, 2026-07-21). Sans ce nettoyage, chaque formule fabriquerait un
# candidat distinct.
CODES_FORMULES = list(markers.DOUTE_PAR_NIVEAU) + [
    "d_apres", "copie", "anciennement_attribue"]
_RE_A_ISOLE = re.compile(r"^A\s+|\s+A$")


def nom_seul(segment: str) -> str:
    """Le nom d'auteur débarrassé de sa formule, dans et hors parenthèses."""
    pivot = _pivot(segment)
    for code in CODES_FORMULES:
        if code in markers._COMPILES:
            pivot = markers._COMPILES[code].sub(" ", pivot)
    pivot = " ".join(pivot.split())
    # « attribué à » laisse un « à » orphelin une fois la formule retirée
    pivot = " ".join(_RE_A_ISOLE.sub(" ", pivot).split())
    return pivot.strip(" ,;-")


def main() -> None:
    candidats = {}   # nom -> {refs: set, musees: set, graphies: set, exemple: (ref, segment)}
    total = 0

    morceaux = pd.read_csv(CHEMIN_CSV, sep="|", usecols=COLONNES, dtype=str,
                           chunksize=TAILLE_MORCEAU)
    for morceau in morceaux:
        total += len(morceau)
        for ref, aut, dom, code in zip(
            morceau["Reference"], morceau["Auteur"],
            morceau["Domaine"], morceau["Code_Museofile"],
        ):
            if not isinstance(aut, str) or not isinstance(ref, str):
                continue
            en_ba = markers._dans_beaux_arts(dom)
            for segment in aut.split(";"):
                segment = segment.strip()
                if not segment:
                    continue
                categorie, _ = markers.famille_segment(segment, en_ba)
                if categorie != "doute":
                    continue
                nom = nom_seul(segment)
                if not nom:
                    continue
                c = candidats.get(nom)
                if c is None:
                    c = candidats[nom] = {"refs": set(), "musees": set(),
                                          "graphies": set(), "exemple": (ref, segment)}
                c["refs"].add(ref)
                c["graphies"].add(_pivot(segment))
                if isinstance(code, str) and code.strip():
                    c["musees"].add(code)
        print(f"\r  {total:,} notices lues".replace(",", " "), end="", flush=True)
    print()

    retenus = [(nom, c) for nom, c in candidats.items() if len(c["refs"]) >= SEUIL]
    retenus.sort(key=lambda x: -len(x[1]["refs"]))

    lignes = []
    for nom, c in retenus:
        # le candidat est-il déjà l'un des 27 ? on interroge la table d'identité
        # elle-même, sur sa graphie la plus fréquente
        maitre = next((m for m in (_trouve_maitre(g) for g in sorted(c["graphies"]))
                       if m), None)
        lignes.append({
            "nom": nom,
            "notices_prudentes": len(c["refs"]),
            "musees": len(c["musees"]),
            "graphies": len(c["graphies"]),
            "deja_retenu": maitre or "",
            "exemple_reference": c["exemple"][0],
            "exemple_mention": c["exemple"][1],
        })

    SORTIE.parent.mkdir(parents=True, exist_ok=True)
    with open(SORTIE, "w", encoding="utf-8", newline="") as f:
        ecrivain = csv.DictWriter(f, fieldnames=list(lignes[0]), delimiter="|")
        ecrivain.writeheader()
        ecrivain.writerows(lignes)

    dedans = sum(1 for l in lignes if l["deja_retenu"])
    print(f"\n{len(candidats)} formes d'auteur portent au moins une mention prudente")
    print(f"{len(lignes)} atteignent le seuil de {SEUIL} références "
          f"({dedans} rattachées aux 27 actuels, {len(lignes) - dedans} hors liste)")
    print(f"→ {SORTIE}  (généré le "
          f"{datetime.now(timezone.utc).isoformat(timespec='seconds')})")
    print(f"\n{'notices':>8}{'musées':>8}  candidat (hors 27, les 40 premiers)")
    for l in [x for x in lignes if not x["deja_retenu"]][:40]:
        print(f"{l['notices_prudentes']:>8}{l['musees']:>8}  {l['nom'][:70]}")


if __name__ == "__main__":
    main()
