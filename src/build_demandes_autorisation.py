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
MUSEES = EXPORTS / "web" / "musees.json"
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


def codes_museofile() -> dict:
    """Rattache (nom, ville) au code Muséofile, qui ouvre la fiche de contact.

    Deux prudences : on n'accepte qu'un code de la forme M + chiffres (la base
    contient au moins un code parasite, un intitulé de champ Joconde recopié à
    sa place), et à nom et ville égaux on garde l'entrée la plus fournie.
    """
    codes: dict = {}
    volumes: dict = {}
    for musee in json.loads(MUSEES.read_text(encoding="utf-8")):
        code = musee.get("code_museofile") or ""
        if not re.fullmatch(r"M\d+", code):
            continue
        cle = (_norm(musee.get("nom") or ""), _norm(musee.get("ville") or ""))
        if musee.get("notices_versees", 0) >= volumes.get(cle, -1):
            codes[cle] = code
            volumes[cle] = musee.get("notices_versees", 0)
    return codes


def main() -> None:
    lignes = list(csv.DictReader(SOURCE.open(encoding="utf-8")))
    codes = codes_museofile()
    # Le titre manque sur 97 notices (des dessins d'Ingres sans intitulé) : le
    # numéro d'inventaire est de toute façon ce qui identifie l'œuvre au musée.
    metadonnees = json.loads(METADONNEES.read_text(encoding="utf-8"))

    groupes = defaultdict(lambda: {"notices": [], "credits": Counter(), "artistes": Counter()})
    agence = {"notices": [], "credits": Counter()}

    for ligne in lignes:
        if ligne["statut"] not in ("unknown", "restricted"):
            continue  # `unavailable` : aucune photo à demander
        if est_agence(ligne["credit"]):
            agence["notices"].append(ligne)
            agence["credits"][ligne["credit"].strip()] += 1
            continue
        entree = groupes[(ligne["musee"], ligne["ville"])]
        entree["notices"].append(ligne)
        entree["credits"][ligne["credit"].strip() or "(crédit vide)"] += 1
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
        for rang, ((musee, ville), entree) in enumerate(classement, start=1):
            statuts = Counter(n["statut"] for n in entree["notices"])
            plume.writerow(
                [
                    rang,
                    musee,
                    ville,
                    codes.get((_norm(musee), _norm(ville)), ""),
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
        for (musee, ville), entree in classement:
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
    for (musee, ville), entree in classement[:10]:
        print(f"  {len(entree['notices']):4d}  {musee} — {ville}")
    print(f"\nHors périmètre musée (agences photo) : {len(agence['notices'])} notices")
    for credit, nombre in agence["credits"].most_common(5):
        print(f"  {nombre:5d}  {credit}")


if __name__ == "__main__":
    main()
