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

import json
from datetime import datetime, timezone

import pandas as pd

import markers
from config import CHEMIN_CSV, CHEMIN_NOMENCLATURE, DOSSIER_EXPORTS, URL_CSV

DOSSIER_WEB = DOSSIER_EXPORTS / "web"
TAILLE_MORCEAU = 200_000

# Échelle du doute (docs/typologie.md), du plus léger au plus détaché.
NIVEAUX = {
    1: ["attribue", "point_interrogation", "presume"],
    2: ["ecole_de", "atelier_de", "entourage_de", "suiveur_de"],
    3: ["maniere_de", "genre_de"],
}
CODES_DOUTE = [c for codes in NIVEAUX.values() for c in codes]
CODES_COPIE = [f.code for f in markers.FAMILLES if f.categorie == "copie"]
CODES_REVISION = [f.code for f in markers.FAMILLES if f.categorie == "revision"]

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


def provenance() -> dict:
    """Métadonnées de version : la photo datée voyage avec les données."""
    # Valeurs confirmées le 2026-07-05 via les en-têtes HTTP du serveur
    # (voir docs/donnees.md). Figées ici pour ne pas dépendre du réseau.
    return {
        "source": "Collections des musées de France : base Joconde",
        "editeur": "Ministère de la Culture",
        "licence": "Licence Ouverte 2.0",
        "url_source": URL_CSV,
        "version_donnee": "2026-07-01",  # Last-Modified du CSV
        "empreinte_etag": "4cc723bb0c3aebdecd2245b7644fb00a",
        "taille_octets": 1191002260,
        "mise_a_jour_source": "chaque mercredi 06:00",
        "date_generation_exports": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "lexique": "markers.py v2 (2026-07-05)",
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
    ecrire("niveaux.json", {
        "notices_total": total,
        "notices_avec_auteur": int(total_auteur),
        "doute_total": doute_total,
        "taux_doute_base": round(doute_total / total, 5),
        "taux_doute_avec_auteur": round(doute_total / total_auteur, 5),
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
