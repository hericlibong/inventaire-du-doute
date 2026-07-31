"""Pipeline d'exports pour la restitution web (P2-T3).

Passe une dernière fois sur le CSV complet et sérialise des JSON légers,
consommables côté front sans jamais recharger la base. Produit dans
data/exports/web/ :

- provenance.json  : version datée de la donnée + métadonnées de génération ;
- niveaux.json     : totaux globaux (échelle du doute, catégories, familles) ;
- musees.json      : un objet par musée, avec TOUJOURS le total versé
                     (garde-fou anti-palmarès) et ses coordonnées ;
- territoires.json  : agrégats par département et par région.

Règles de comptage (docs/decisions.md) :
- le doute est l'union des familles de doute (chiffre vedette) ;
- chaque notice de doute est classée au NIVEAU LE PLUS LÉGER qu'elle porte,
  pour que niveau1 + niveau2 + niveau3 = doute exactement (partition, jamais
  d'addition trompeuse) ;
- doute / copie / révision restent séparés ; leur union est nommée
  « au moins une mention », jamais une somme.

Usage : uv run python src/build_exports.py  (~3 min)
"""

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

import markers
from config import CHEMIN_CSV, CHEMIN_NOMENCLATURE, DOSSIER_EXPORTS, URL_CSV, chemin_releve

DOSSIER_WEB = DOSSIER_EXPORTS / "web"
TAILLE_MORCEAU = 200_000

# Photo de référence du projet : le CSV du mercredi 1er juillet 2026, confirmé
# le 2026-07-05 par les en-têtes HTTP du serveur (docs/donnees.md, T1). Sert de
# repli pour les CSV téléchargés avant que download.py n'écrive son relevé ; le
# MD5 permet de vérifier hors ligne qu'il s'agit bien de ce fichier.
CSV_REFERENCE = {
    "version_donnee": "2026-07-01",
    "empreinte_md5": "4cc723bb0c3aebdecd2245b7644fb00a",
}

# Échelle du doute (docs/typologie.md), du plus léger au plus détaché.
NIVEAUX = {
    1: ["attribue", "point_interrogation", "presume"],
    2: ["ecole_de", "atelier_de", "entourage_de", "suiveur_de"],
    3: ["maniere_de", "genre_de"],
}
CODES_DOUTE = [c for codes in NIVEAUX.values() for c in codes]
CODES_COPIE = [f.code for f in markers.FAMILLES if f.categorie == "copie"]
CODES_REVISION = [f.code for f in markers.FAMILLES if f.categorie == "revision"]

# Monoculture divulguée (décision utilisateur 2026-07-05) : le muséum d'histoire
# naturelle de Nice concentre 23,6 % du doute national, tous « Barla (attribué
# à) » — un artefact de catalogage. On ne l'exclut pas du chiffre vedette, on le
# divulgue : un chiffre « hors ce cas » l'accompagne partout, et le musée est
# marqué pour que la restitution puisse le signaler. Exception nommée et
# documentée, pas un seuil automatique (voir docs/decisions.md).
MONOCULTURE_CODE = "M7050"
MONOCULTURE_LIBELLE = (
    "Muséum d'histoire naturelle de Nice — planches de Barla (attribué à)"
)

COLONNES = [
    "Reference", "Auteur", "Precisions_sur_l_auteur", "Ancienne_attribution",
    "Ecole_pays", "Domaine", "Code_Museofile", "Nom_officiel_musee",
    "Ville", "Departement", "Region", "coordonnees",
]


def _texte(valeur: object):
    """Valeur texte ou None (jamais NaN : produirait un JSON invalide)."""
    return valeur if isinstance(valeur, str) else None


def _coord(valeur: object):
    """« lat, lon » → [lat, lon] arrondis, ou None."""
    if not isinstance(valeur, str) or "," not in valeur:
        return None
    try:
        lat, lon = (float(x) for x in valeur.split(",")[:2])
        return [round(lat, 5), round(lon, 5)]
    except ValueError:
        return None


def lire_releve_source() -> dict | None:
    """Relevé écrit par `download.py` à côté du CSV, s'il existe."""
    chemin = chemin_releve(CHEMIN_CSV)
    if not chemin.exists():
        return None
    return json.loads(chemin.read_text(encoding="utf-8"))


def empreinte_md5(chemin: Path, bloc: int = 1 << 20) -> str:
    """Empreinte MD5 du fichier, lue par blocs (le CSV pèse 1,1 Go).

    data.gouv sert l'ETag sous la forme du MD5 du contenu : calculer l'empreinte
    localement suffit donc à savoir, hors ligne, quelle version de la base on a
    sous la main."""
    somme = hashlib.md5()
    with open(chemin, "rb") as fichier:
        for morceau in iter(lambda: fichier.read(bloc), b""):
            somme.update(morceau)
    return somme.hexdigest()


def provenance() -> dict:
    """Métadonnées de version : la photo datée voyage avec les données.

    Rien n'est recopié à la main. La taille et l'empreinte viennent du CSV
    réellement lu ; la date de version vient du fichier voisin écrit par
    `download.py` (en-têtes HTTP relevés à la source). À défaut de ce fichier —
    cas des CSV téléchargés avant son introduction — on retombe sur la photo de
    référence documentée, mais SEULEMENT si l'empreinte concorde : le pipeline
    refuse de dater une base qu'il ne peut pas identifier."""
    taille = CHEMIN_CSV.stat().st_size
    empreinte = empreinte_md5(CHEMIN_CSV)
    releve = lire_releve_source()

    if releve and releve.get("empreinte_md5") == empreinte:
        version = releve["version_donnee"]
    elif empreinte == CSV_REFERENCE["empreinte_md5"]:
        version = CSV_REFERENCE["version_donnee"]
    else:
        raise SystemExit(
            f"CSV inconnu : empreinte {empreinte} ({taille} octets).\n"
            f"Ce n'est pas la photo de référence ({CSV_REFERENCE['version_donnee']}, "
            f"{CSV_REFERENCE['empreinte_md5']}) et aucun relevé de téléchargement ne "
            f"l'accompagne — le pipeline ne peut donc pas dire de quelle version de la "
            f"base viennent ses chiffres, alors que le site l'affiche.\n"
            f"Relancer `uv run python src/download.py` sur un dossier data/raw vidé "
            f"(le relevé sera écrit à côté du fichier), ou mettre à jour CSV_REFERENCE "
            f"dans ce script après avoir relevé les en-têtes HTTP du serveur."
        )

    return {
        "source": "Collections des musées de France : base Joconde",
        "editeur": "Ministère de la Culture",
        "licence": "Licence Ouverte 2.0",
        "url_source": URL_CSV,
        "version_donnee": version,  # Last-Modified du CSV, côté serveur
        "empreinte_etag": empreinte,
        "taille_octets": taille,
        "mise_a_jour_source": "chaque mercredi 06:00",
        "date_generation_exports": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "lexique": f"markers.py {markers.VERSION}",
    }


def main() -> None:
    total = 0
    total_auteur = 0
    familles = {f.code: 0 for f in markers.FAMILLES}
    par_musee = []  # agrégats partiels (un par morceau), recollés à la fin

    morceaux = pd.read_csv(
        CHEMIN_CSV, sep="|", usecols=COLONNES, dtype=str, chunksize=TAILLE_MORCEAU
    )
    for morceau in morceaux:
        total += len(morceau)
        total_auteur += morceau["Auteur"].notna().sum()
        det = markers.detections(morceau)
        for code in familles:
            familles[code] += int(det[code].sum())

        # niveau le plus léger présent (0 = pas de doute)
        n1 = det[NIVEAUX[1]].any(axis=1)
        n2 = det[NIVEAUX[2]].any(axis=1)
        n3 = det[NIVEAUX[3]].any(axis=1)
        niveau = pd.Series(0, index=morceau.index)
        niveau = niveau.mask(n3, 3).mask(n2, 2).mask(n1, 1)

        agg = pd.DataFrame({
            "code": morceau["Code_Museofile"],
            "nom": morceau["Nom_officiel_musee"],
            "ville": morceau["Ville"],
            "departement": morceau["Departement"],
            "region": morceau["Region"],
            "coord": morceau["coordonnees"],
            "total": 1,
            "doute": (niveau > 0).astype(int),
            "niv1": n1.astype(int),
            "niv2": (n2 & ~n1).astype(int),
            "niv3": (n3 & ~n1 & ~n2).astype(int),
            "copie": det[CODES_COPIE].any(axis=1).astype(int),
            "revision": det[CODES_REVISION].any(axis=1).astype(int),
        }).dropna(subset=["code"])
        par_musee.append(agg.groupby("code", as_index=False).agg(
            nom=("nom", "first"), ville=("ville", "first"),
            departement=("departement", "first"), region=("region", "first"),
            coord=("coord", "first"), total=("total", "sum"),
            doute=("doute", "sum"), niv1=("niv1", "sum"), niv2=("niv2", "sum"),
            niv3=("niv3", "sum"), copie=("copie", "sum"), revision=("revision", "sum"),
        ))
        print(f"\r  {total:,} notices lues".replace(",", " "), end="", flush=True)
    print()

    # Recollage final : un musée peut apparaître dans plusieurs morceaux.
    musees = pd.concat(par_musee).groupby("code", as_index=False).agg(
        nom=("nom", "first"), ville=("ville", "first"),
        departement=("departement", "first"), region=("region", "first"),
        coord=("coord", "first"), total=("total", "sum"), doute=("doute", "sum"),
        niv1=("niv1", "sum"), niv2=("niv2", "sum"), niv3=("niv3", "sum"),
        copie=("copie", "sum"), revision=("revision", "sum"),
    )

    DOSSIER_WEB.mkdir(parents=True, exist_ok=True)

    def ecrire(nom, objet):
        (DOSSIER_WEB / nom).write_text(
            json.dumps(objet, ensure_ascii=False, indent=1), encoding="utf-8"
        )

    # 1. provenance
    ecrire("provenance.json", provenance())

    # 2. niveaux (totaux globaux)
    doute_total = int((musees["niv1"] + musees["niv2"] + musees["niv3"]).sum())
    ligne_mono = musees[musees["code"] == MONOCULTURE_CODE]
    doute_mono = int(ligne_mono["doute"].sum())
    ecrire("niveaux.json", {
        "notices_total": total,
        "notices_avec_auteur": int(total_auteur),
        "doute_total": doute_total,
        "taux_doute_base": round(doute_total / total, 5),
        "taux_doute_avec_auteur": round(doute_total / total_auteur, 5),
        "monoculture_divulguee": {
            "code_museofile": MONOCULTURE_CODE,
            "libelle": MONOCULTURE_LIBELLE,
            "doute": doute_mono,
            "part_du_doute_national": round(doute_mono / doute_total, 4),
        },
        "doute_hors_monoculture": doute_total - doute_mono,
        "niveaux": {
            "1": {"libelle": "Presque lui", "notices": int(musees["niv1"].sum())},
            "2": {"libelle": "Autour de lui", "notices": int(musees["niv2"].sum())},
            "3": {"libelle": "Son style, sans lui", "notices": int(musees["niv3"].sum())},
        },
        "copie": int(musees["copie"].sum()),
        "revision": int(musees["revision"].sum()),
        "familles": {
            f.code: {"libelle": f.libelle, "categorie": f.categorie,
                     "notices": familles[f.code]}
            for f in markers.FAMILLES
        },
    })

    # 3. musées (toujours le total versé + coordonnées)
    liste_musees = []
    for _, r in musees.sort_values("doute", ascending=False).iterrows():
        liste_musees.append({
            "code_museofile": r["code"],
            "nom": _texte(r["nom"]),
            "ville": _texte(r["ville"]),
            "departement": _texte(r["departement"]),
            "region": _texte(r["region"]),
            "coord": _coord(r["coord"]),
            "notices_versees": int(r["total"]),
            "doute": int(r["doute"]),
            "part_doute": round(r["doute"] / r["total"], 4) if r["total"] else 0,
            "niveaux": [int(r["niv1"]), int(r["niv2"]), int(r["niv3"])],
            "copie": int(r["copie"]),
            "revision": int(r["revision"]),
            "monoculture": r["code"] == MONOCULTURE_CODE,
        })
    ecrire("musees.json", liste_musees)

    # 4. territoires (département et région)
    def agreger(cle):
        g = musees.groupby(cle).agg(
            notices_versees=("total", "sum"), doute=("doute", "sum"),
            musees=("code", "nunique")).reset_index()
        return [
            {cle: r[cle], "notices_versees": int(r["notices_versees"]),
             "doute": int(r["doute"]), "musees": int(r["musees"]),
             "part_doute": round(r["doute"] / r["notices_versees"], 4)}
            for _, r in g.sort_values("doute", ascending=False).iterrows()
            if isinstance(r[cle], str)
        ]
    ecrire("territoires.json", {
        "departements": agreger("departement"),
        "regions": agreger("region"),
    })

    tailles = {p.name: p.stat().st_size for p in sorted(DOSSIER_WEB.glob("*.json"))}
    print(f"\n{len(liste_musees)} musées exportés. Fichiers dans {DOSSIER_WEB} :")
    for nom, octets in tailles.items():
        print(f"  {nom:<20} {octets / 1024:6.1f} Ko")


if __name__ == "__main__":
    main()
