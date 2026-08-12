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
import sys
import unicodedata
import urllib.request
from collections import Counter, defaultdict
from pathlib import Path

EXPORTS = Path("data/exports")
# Répertoire des Musées de France (base Muséofile, Licence Ouverte) : il donne
# l'adresse postale, le téléphone et le site de chaque institution. C'est ce qui
# transforme une liste de noms en liste de destinataires.
MUSEOFILE = Path("data/cache/museofile.csv")
URL_MUSEOFILE = "https://ministere-culture.s3.sbg.io.cloud.ovh.net/POP/museofile.csv"
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


def coordonnees() -> dict:
    """Adresse, téléphone et site de chaque musée, indexés par code Muséofile."""
    if not MUSEOFILE.exists():
        print("Téléchargement de la base Muséofile…")
        MUSEOFILE.parent.mkdir(parents=True, exist_ok=True)
        urllib.request.urlretrieve(URL_MUSEOFILE, MUSEOFILE)
    csv.field_size_limit(min(sys.maxsize, 2**31 - 1))
    with MUSEOFILE.open(encoding="utf-8", newline="") as fichier:
        return {
            row["Identifiant"].strip(): row
            for row in csv.DictReader(fichier, delimiter="|")
        }


def main() -> None:
    lignes = list(csv.DictReader(SOURCE.open(encoding="utf-8")))
    contacts = coordonnees()
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
                "destinataire",
                "nature",
                "ville",
                "code_museofile",
                "adresse",
                "code_postal",
                "commune",
                "telephone",
                "site",
                "notices",
                "sans_licence",
                "soumises_a_autorisation",
                "photographes_credites",
                "artistes_principaux",
                "exemple_notice_pop",
            ]
        )
        # L'agence photo est le PREMIER destinataire de la liste, avant tous les
        # musées : c'est le crédit le plus fréquent du corpus, et une seule
        # demande le couvre. L'exclure de la liste des adresses, comme on l'a
        # d'abord fait, laissait le plus gros interlocuteur invisible.
        plume.writerow(
            [
                0,
                "RMN-Grand Palais (agence photographique)",
                "agence photo",
                "Paris",
                "",
                "254-256 rue de Bercy",
                "75577",
                "Paris Cedex 12",
                "01 40 13 48 00",
                "https://www.photo.rmn.fr",
                len(agence["notices"]),
                "",
                len(agence["notices"]),
                " | ".join(credit for credit, _ in agence["credits"].most_common(2)),
                "",
                agence["notices"][0]["notice_pop"],
            ]
        )
        for rang, (cle, entree) in enumerate(classement, start=1):
            statuts = Counter(n["statut"] for n in entree["notices"])
            fiche = contacts.get(cle, {})
            # Le « lieu » précise le bâtiment (« abbaye Saint-Loup », « hôtel
            # Biron ») : il fait partie de l'adresse postale.
            rue = " ".join(
                p.strip() for p in (fiche.get("Adresse", ""), fiche.get("Lieu", "")) if p.strip()
            )
            plume.writerow(
                [
                    rang,
                    entree["noms"].most_common(1)[0][0],
                    "musée",
                    entree["villes"].most_common(1)[0][0],
                    cle if est_code(cle) else "",
                    rue,
                    fiche.get("Code_postal", ""),
                    fiche.get("Ville", ""),
                    fiche.get("Telephone", ""),
                    fiche.get("URL", ""),
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
        # Les notices de l'agence d'abord, sous son nom : c'est une pièce jointe
        # comme les autres, pour un destinataire comme les autres.
        blocs = [("RMN-Grand Palais", "Paris", agence["notices"])]
        blocs += [
            (e["noms"].most_common(1)[0][0], e["villes"].most_common(1)[0][0], e["notices"])
            for _, e in classement
        ]
        for musee, ville, notices in blocs:
            for notice in sorted(notices, key=lambda n: n["titre"]):
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
    print(f"1 agence photo ({len(agence['notices'])} notices) + "
          f"{len(classement)} musées ({total} notices)")
    for cle, entree in classement[:12]:
        nom = entree["noms"].most_common(1)[0][0]
        ville = entree["villes"].most_common(1)[0][0]
        print(f"  {len(entree['notices']):4d}  {nom} — {ville} ({cle})")
    print(f"\nHors périmètre musée (agences photo) : {len(agence['notices'])} notices")
    for credit, nombre in agence["credits"].most_common(5):
        print(f"  {nombre:5d}  {credit}")


if __name__ == "__main__":
    main()
