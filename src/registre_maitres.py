"""Registre d'instruction des artistes (ouvert au temps 5, tenu à chaque lot).

Deux livrables. Le premier demande une passe sur le CSV, le second non — d'où
l'option `--formes`, qui ne recalcule que les statuts (lot 2, 2026-08-02).

1. data/exports/maitres_instruits.csv — un artiste par ligne, pour les personnes
   RETENUES (27 au 2026-07-07, +36 au 2026-07-22, +40 au 2026-08-02). Comptage
   par personne, en références Joconde uniques (unité des temps 1-2) : doute,
   attributions certaines, copies « d'après », musées détenteurs. C'est la vue
   qui prouve que chaque maître retenu dépasse bien le seuil de 10 APRÈS
   regroupement de ses graphies.

2. data/exports/candidats_maitres.csv — le registre EXHAUSTIF des 330 formes au
   seuil de 10 (généré au temps 4), enrichi d'une colonne « statut » à quatre
   valeurs (cadrage utilisateur, 2026-07-22) :
     - « retenu » : la forme se rattache à un maître de la table ;
     - « écarté » : l'entité n'est pas une personne (manufacture, imprimerie,
       « anonyme », mention collective) ou est un pur accident de saisie ;
     - « à instruire » : personne possible, pas encore vérifiée. PAR DÉFAUT.
   « à instruire » n'est PAS « écarté » : rien n'est retiré par les données, la
   sélection reste ouverte à des lots ultérieurs.

Usage : uv run python src/registre_maitres.py            (passe complète, ~25 min)
        uv run python src/registre_maitres.py --formes   (statuts seuls, instantané)
"""

import csv
import json
import re
import sys
from datetime import datetime, timezone

import pandas as pd

import markers
from build_artistes import MAITRES, _pivot, _trouve_maitre, resout_reference
from config import CHEMIN_CSV, DOSSIER_EXPORTS

# Les 27 du lot initial (2026-07-07) ; le reste vient du lot du temps 5.
LOT_INITIAL = {
    "Charles Le Brun", "Le Primatice", "Ingres", "Rembrandt", "Michel-Ange",
    "Rubens", "François Clouet", "Annibale Carracci", "Rodin", "Boucher",
    "Andrea del Sarto", "Guido Reni", "Léonard de Vinci", "Le Tintoret",
    "Nicolas Poussin", "Simon Vouet", "Greuze", "Van Dyck", "Le Corrège",
    "Pierre Mignard", "Véronèse", "Hyacinthe Rigaud", "Géricault", "Fragonard",
    "Raphaël", "Ribera", "Titien",
}

# Le lot du 2026-08-02 : 40 personnes retenues parmi les 50 formes du registre
# qui portaient au moins 25 notices prudentes et restaient « à instruire ».
LOT_2 = {
    "Jean-Baptiste Barla", "Alexandre Clausel", "Charles Normand", "Léon Tirode",
    "Louis Morinet", "Giacinto Calandrucci", "Georges Ferdinand Bigot",
    "Léon Fort", "Louis Duthoit", "Aimé Duthoit", "Charles François Pinot",
    "André Marie Florentin Giraud", "Auguste Vacquerie", "François Georgin",
    "Louis Verjat", "Peter Hawke", "Auguste Alleaume",
    "Antoine Gabriel Willermet", "Turpin de Crissé", "Charles Hugo",
    "Gustave Lancelot", "Charles du Ry", "Odilon Roche", "Frans Hogenberg",
    "Charles Eugène Ensfelder", "Nicolaus Hoffmann", "Nicasius Bernaerts",
    "Crispin de Passe l'Ancien", "Crispin de Passe le Jeune",
    "Amable Louis Crapelet", "Auguste Beuret", "Jean-Charles François Leloy",
    "Joseph Hussenot", "Antonio del Pollaiuolo", "Henry Hennault",
    "Israël Henriet", "René Ackermann", "Louis Hertig", "Colijn de Coter",
    "Jacques-Louis David",
}

# ÉCARTÉS INSTRUITS — les formes examinées une par une et NON retenues, avec le
# motif exact. Elles ne sont pas « à instruire » : elles l'ont été, et la réponse
# est non. Le motif est publiable tel quel : c'est ce qui rend la sélection
# contrôlable au lieu d'être un panthéon opaque (decisions.md, 2026-07-21 quater,
# décision 4). La clé est le nom du registre, sa formule retirée.
ECARTES_INSTRUITS = {
    "MELLET JACQUES PERE": "atelier de famille : les mêmes 41 notices nomment "
                           "les trois Mellet, aucun prénom n'individualise",
    "MELLET JULES FILS": "atelier de famille : les mêmes 41 notices nomment "
                         "les trois Mellet, aucun prénom n'individualise",
    "MELLET HENRI FILS": "atelier de famille : les mêmes 41 notices nomment "
                         "les trois Mellet, aucun prénom n'individualise",
    "TURPIN DE CRISSE PERE": "désigné seulement comme « le père » ; 34 de ses "
                             "35 notices nomment le fils, retenu à son nom",
    "PETER": "nom sans prénom : plusieurs Peter dans la base",
    "VARADY": "prénom réduit à une initiale (« VARADY A »)",
    "BUQUET": "nom nu, mention « atelier » ; plusieurs Buquet dans la base",
    "PREVOST": "nom nu, mention « atelier » ; plusieurs Prévost dans la base",
    "PELLERIN": "raison sociale (imagerie d'Épinal), pas une personne",
    "PELLERIN & CIE": "raison sociale (imagerie d'Épinal), pas une personne",
    "IMAGERIE PELLERIN": "raison sociale (imagerie d'Épinal), pas une personne",
    "MOGHOLE DE MURSHIDABAD": "école régionale, pas une personne",
}

# Marqueurs d'une entité qui n'est pas une seule personne (mots entiers sur le
# nom-pivot déjà normalisé). CONSERVATEUR : au moindre doute, on laisse « à
# instruire » plutôt que d'écarter. On n'écarte PAS sur « fils », « père » ou
# « frères » : ces mots désignent souvent une personne d'une dynastie (Mellet
# Jules Fils, Lacour Pierre Fils), pas un atelier — les écarter serait une
# sélection arbitraire (cadrage utilisateur, 2026-07-22). Ne restent que les
# formes de raison sociale ou de collectif sans ambiguïté.
NON_PERSONNE = re.compile(
    r"\b(MANUFACTURE|IMPRIMERIE|IMPRIMEUR|FAIENCERIE|FAIENCERIES|FABRIQUE|"
    r"ATELIER|ANONYME|ECOLE|TISSAGE|SUCCESSEURS|CIE|LTD|L'UN DES)\b")

def statut_forme(nom: str, pivot_exemple: str) -> tuple[str, str]:
    """Statut d'une forme du registre exhaustif + le maître ou le motif.

    `nom` est le nom débarrassé de sa formule ; `pivot_exemple` la mention réelle
    d'où il vient. Les deux servent : « Manufacture de Fulda (attribué à) » se
    réduit au nom « FULDA », c'est la mention qui dit que ce n'est pas quelqu'un.
    """
    maitre = _trouve_maitre(pivot_exemple)
    if maitre:
        return "retenu", maitre
    # instruit à l'œil et non retenu : le motif prime sur le tri automatique
    if nom in ECARTES_INSTRUITS:
        return "écarté", ECARTES_INSTRUITS[nom]
    # un nom réduit à une lettre ou à rien : la mention ne portait qu'une
    # formule (« Attribué à », 30 notices) ou un caractère isolé
    if len(nom.replace(")", "").replace("-", "").strip()) <= 1:
        return "écarté", "mention sans nom d'auteur"
    if NON_PERSONNE.search(nom) or NON_PERSONNE.search(pivot_exemple):
        return "écarté", "entité non personnelle"
    return "à instruire", ""


def main() -> None:
    # « musees » = musées où le maître APPARAÎT, toutes catégories confondues.
    # « musees_doute » = musées où une mention prudente est écrite. Les deux sont
    # publiés : confondre les deux ferait dire au chiffre bien plus qu'il ne dit
    # (David Téniers apparaît dans 57 musées, le doute n'est écrit que dans 24).
    agg = {nom: {"doute": set(), "propre": set(), "copie": set(),
                 "musees": set(), "musees_doute": set()}
           for nom, *_ in MAITRES}
    total = 0

    morceaux = pd.read_csv(CHEMIN_CSV, sep="|", dtype=str, chunksize=200_000,
                           usecols=["Reference", "Auteur", "Domaine",
                                    "Code_Museofile"])
    for morceau in morceaux:
        total += len(morceau)
        for ref, aut, dom, code in zip(
            morceau["Reference"], morceau["Auteur"],
            morceau["Domaine"], morceau["Code_Museofile"],
        ):
            if not isinstance(aut, str) or not isinstance(ref, str):
                continue
            for nom, (cat, _f, _s) in resout_reference(
                    aut, markers._dans_beaux_arts(dom)).items():
                a = agg[nom]
                a[cat].add(ref)
                if isinstance(code, str) and code.strip():
                    a["musees"].add(code)
                    if cat == "doute":
                        a["musees_doute"].add(code)
        print(f"\r  {total:,} notices lues".replace(",", " "), end="", flush=True)
    print()

    # 1. Registre par personne (retenus)
    lignes = []
    for nom, *_ in MAITRES:
        a = agg[nom]
        if nom in LOT_INITIAL:
            lot = "initial-2026-07-07"
        elif nom in LOT_2:
            lot = "lot2-2026-08-02"
        else:
            lot = "temps5-2026-07-22"
        lignes.append({
            "maitre": nom,
            "lot": lot,
            "notices_prudentes": len(a["doute"]),
            "attributions_certaines": len(a["propre"]),
            "copies_d_apres": len(a["copie"]),
            "musees_presence": len(a["musees"]),
            "musees_doute": len(a["musees_doute"]),
        })
    lignes.sort(key=lambda x: -x["notices_prudentes"])

    chemin1 = DOSSIER_EXPORTS / "maitres_instruits.csv"
    with open(chemin1, "w", encoding="utf-8", newline="") as f:
        ecr = csv.DictWriter(f, fieldnames=list(lignes[0]), delimiter="|")
        ecr.writeheader()
        ecr.writerows(lignes)

    sous_seuil = [l for l in lignes if l["notices_prudentes"] < 10]
    print(f"\n{len(lignes)} maîtres retenus → {chemin1.name}")
    if sous_seuil:
        print(f"  ⚠ SOUS LE SEUIL DE 10 : {[l['maitre'] for l in sous_seuil]}")
    else:
        print("  tous ≥ 10 notices prudentes uniques après regroupement ✓")

    statuts_des_formes(len(lignes))

    print(f"\n{'notices':>8}{'cert.':>7}{'copies':>7}{'mus.doute':>10}"
          f"{'mus.prés.':>10}  maître  ·  lot")
    for l in lignes:
        print(f"{l['notices_prudentes']:>8}{l['attributions_certaines']:>7}"
              f"{l['copies_d_apres']:>7}{l['musees_doute']:>10}"
              f"{l['musees_presence']:>10}  {l['maitre']}  · {l['lot'][:6]}")


def statuts_des_formes(nb_maitres: int) -> None:
    """Statuts du registre exhaustif + résumé pour la page Méthode.

    Séparé du reste depuis le lot 2 (2026-08-02) : cette moitié ne lit QUE
    `candidats_maitres.csv`, jamais le CSV de 1,1 Go. Corriger un motif d'écart
    ou ajouter une forme instruite ne doit pas coûter une relecture d'un million
    de notices. Appel direct : `uv run python src/registre_maitres.py --formes`.
    """
    # 2. Registre exhaustif enrichi du statut (on relit le CSV du temps 4)
    chemin2 = DOSSIER_EXPORTS / "candidats_maitres.csv"
    with open(chemin2, encoding="utf-8") as f:
        candidats = list(csv.DictReader(f, delimiter="|"))
    compte = {"retenu": 0, "écarté": 0, "à instruire": 0}
    for c in candidats:
        statut, info = statut_forme(c["nom"], _pivot(c["exemple_mention"]))
        # une forme déjà signalée « deja_retenu » l'emporte (rattachement sûr)
        if c["deja_retenu"]:
            statut, info = "retenu", c["deja_retenu"]
        c["statut"] = statut
        c["rattachement_ou_motif"] = info
        compte[statut] += 1
    champs = [k for k in candidats[0]
              if k not in ("statut", "rattachement_ou_motif")] + [
        "statut", "rattachement_ou_motif"]
    with open(chemin2, "w", encoding="utf-8", newline="") as f:
        ecr = csv.DictWriter(f, fieldnames=champs, delimiter="|")
        ecr.writeheader()
        ecr.writerows(candidats)

    print(f"\n{len(candidats)} formes au registre exhaustif → {chemin2.name}")
    for statut in ("retenu", "écarté", "à instruire"):
        print(f"  {statut:>12} : {compte[statut]}")

    # 3. Résumé du registre pour la page Méthode. Le site s'engage à publier la
    # liste des candidats examinés et leur état (decisions.md, 2026-07-21 quater,
    # décision 4) : ces quatre nombres rendent l'engagement vérifiable sans
    # charger le CSV entier.
    chemin3 = DOSSIER_EXPORTS / "web" / "registre.json"
    chemin3.parent.mkdir(parents=True, exist_ok=True)
    chemin3.write_text(json.dumps({
        "seuil": 10,
        "formes_au_seuil": len(candidats),
        "retenues": compte["retenu"],
        "ecartees": compte["écarté"],
        "a_instruire": compte["à instruire"],
        "maitres_retenus": nb_maitres,
        "date_generation": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"→ {chemin3.name}")


if __name__ == "__main__":
    if "--formes" in sys.argv:
        # les statuts seuls, sans relire le CSV : `maitres_instruits.csv` garde
        # les chiffres du dernier passage complet
        with open(DOSSIER_EXPORTS / "maitres_instruits.csv", encoding="utf-8") as f:
            statuts_des_formes(sum(1 for _ in f) - 1)
    else:
        main()
