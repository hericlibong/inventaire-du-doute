"""Liste des institutions à solliciter pour publier une reproduction.

Suite de l'audit des droits photo du 2026-07-29 (`images_classify.py`), qui a
classé les 3 668 notices prudentes en cinq statuts. Ce script ne classe rien de
nouveau : il regroupe par institution les notices dont la réutilisation de la
photo n'est PAS établie, pour que les demandes d'autorisation se fassent musée
par musée, avec la liste des notices concernées en pièce jointe.

Deux groupes, deux interlocuteurs différents :

- `unknown` — le musée a publié un crédit (souvent le nom du photographe) mais
  aucune licence. Rien n'interdit la réutilisation, rien ne l'autorise : c'est
  au musée de le dire. C'est le vrai gisement de demandes.
- `restricted` — mention explicite « utilisation soumise à autorisation ». La
  quasi-totalité est de la RMN-Grand Palais, une agence unique : un seul
  interlocuteur, et une démarche de nature différente (tarifée). On l'isole.

Les notices dont le crédit nomme la RMN sont rattachées à la RMN, quel que soit
leur statut : écrire au musée ne servirait à rien, il ne détient pas les droits.

Sortie : data/exports/demandes_autorisation.csv (une ligne par institution) et
data/exports/demandes_autorisation_notices.csv (une ligne par notice, à
découper par musée pour la pièce jointe).
"""

import csv
import json
import re
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

EXPORTS = Path("data/exports")
SOURCE = EXPORTS / "images_oeuvres.csv"
METADONNEES = EXPORTS / "oeuvres_metadonnees.json"
SORTIE_INSTITUTIONS = EXPORTS / "demandes_autorisation.csv"
SORTIE_NOTICES = EXPORTS / "demandes_autorisation_notices.csv"

# Agences photo : le musée n'est pas l'interlocuteur.
AGENCES = ("rmn", "grand palais", "reunion des musees nationaux", "bridgeman")


def _norm(chaine: str) -> str:
    sans = unicodedata.normalize("NFD", chaine or "")
    sans = "".join(c for c in sans if unicodedata.category(c) != "Mn")
    return re.sub(r"\s+", " ", sans).strip().lower()


def est_agence(credit: str) -> bool:
    return any(mot in _norm(credit) for mot in AGENCES)


def est_code(code: str) -> bool:
    """Un code Muséofile est un M suivi de chiffres.

    Le contrôle n'est pas décoratif : l'export des musées contient au moins un
    code parasite — l'intitulé « mode d'acquisition particulier » recopié à la
    place du code, sur une seconde entrée « musée du Louvre ».
    """
    return bool(re.fullmatch(r"M\d+", code or ""))


def main() -> None:
    lignes = list(csv.DictReader(SOURCE.open(encoding="utf-8")))
    # Le titre manque sur une centaine de notices (des dessins d'Ingres sans
    # intitulé) ; le numéro d'inventaire, lui, est renseigné partout, et c'est
    # de toute façon ce qui identifie l'œuvre au musée. Ce fichier porte aussi
    # le code Muséofile, seul identifiant stable de l'institution.
    metadonnees = json.loads(METADONNEES.read_text(encoding="utf-8"))

    groupes = defaultdict(
        lambda: {"notices": [], "credits": Counter(), "artistes": Counter(),
                 "noms": Counter(), "villes": Counter()}
    )
    agence = {"notices": [], "credits": Counter()}

    for ligne in lignes:
        if ligne["statut"] not in ("unknown", "restricted"):
            continue  # `unavailable` : aucune photo à demander
        if est_agence(ligne["credit"]):
            agence["notices"].append(ligne)
            agence["credits"][ligne["credit"].strip()] += 1
            continue
        fiche = metadonnees.get(ligne["reference"], {})
        code = fiche.get("code_museofile", "")
        # On regroupe sur le CODE, jamais sur le nom : le musée de Troyes
        # s'écrit « d'archéologie » et « d’archéologie » selon la notice, et se
        # dédoublait en deux destinataires. À défaut de code, le nom fait office
        # de clé — c'est le cas de deux institutions.
        cle = code if est_code(code) else f"{ligne['musee']} — {ligne['ville']}"
        entree = groupes[cle]
        entree["notices"].append(ligne)
        entree["credits"][ligne["credit"].strip() or "(crédit vide)"] += 1
        entree["noms"][ligne["musee"]] += 1
        entree["villes"][ligne["ville"]] += 1
        for artiste in ligne["artistes"].split("|"):
            if artiste.strip():
                entree["artistes"][artiste.strip()] += 1

    classement = sorted(groupes.items(), key=lambda item: -len(item[1]["notices"]))

    with SORTIE_INSTITUTIONS.open("w", newline="", encoding="utf-8") as fichier:
        plume = csv.writer(fichier)
        plume.writerow(
            [
                "rang",
                "musee",
                "ville",
                "code_museofile",
                "notices",
                "sans_licence",
                "soumises_a_autorisation",
                "photographes_credites",
                "artistes_principaux",
                "exemple_notice_pop",
            ]
        )
        for rang, (cle, entree) in enumerate(classement, start=1):
            statuts = Counter(n["statut"] for n in entree["notices"])
            plume.writerow(
                [
                    rang,
                    entree["noms"].most_common(1)[0][0],
                    entree["villes"].most_common(1)[0][0],
                    cle if est_code(cle) else "",
                    len(entree["notices"]),
                    statuts["unknown"],
                    statuts["restricted"],
                    " | ".join(credit for credit, _ in entree["credits"].most_common(4)),
                    ", ".join(artiste for artiste, _ in entree["artistes"].most_common(5)),
                    entree["notices"][0]["notice_pop"],
                ]
            )

    with SORTIE_NOTICES.open("w", newline="", encoding="utf-8") as fichier:
        plume = csv.writer(fichier)
        plume.writerow(
            [
                "musee",
                "ville",
                "reference",
                "numero_inventaire",
                "titre",
                "domaine",
                "artistes",
                "statut",
                "credit",
                "notice_pop",
            ]
        )
        for cle, entree in classement:
            musee = entree["noms"].most_common(1)[0][0]
            ville = entree["villes"].most_common(1)[0][0]
            for notice in sorted(entree["notices"], key=lambda n: n["titre"]):
                fiche = metadonnees.get(notice["reference"], {})
                plume.writerow(
                    [
                        musee,
                        ville,
                        notice["reference"],
                        fiche.get("numero_inventaire", ""),
                        notice["titre"] or fiche.get("denomination", ""),
                        fiche.get("domaine", ""),
                        notice["artistes"],
                        notice["statut"],
                        notice["credit"],
                        notice["notice_pop"],
                    ]
                )

    total = sum(len(e["notices"]) for _, e in classement)
    print(f"{len(classement)} institutions à solliciter, {total} notices")
    for cle, entree in classement[:12]:
        nom = entree["noms"].most_common(1)[0][0]
        ville = entree["villes"].most_common(1)[0][0]
        print(f"  {len(entree['notices']):4d}  {nom} — {ville} ({cle})")
    print(f"\nHors périmètre musée (agences photo) : {len(agence['notices'])} notices")
    for credit, nombre in agence["credits"].most_common(5):
        print(f"  {nombre:5d}  {credit}")


if __name__ == "__main__":
    main()
