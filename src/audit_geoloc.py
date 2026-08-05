"""Contrôle des positions de musées publiées sur les cartes.

Pourquoi. Joconde publie parfois plusieurs positions sous le même code
Muséofile, et parfois une seule qui est fausse. Le 2026-08-05, le musée Goya de
Castres s'affichait dans la Manche sur la fiche de Ribera. Le pipeline choisit
désormais une position par musée (build_artistes.coord_du_musee), mais aucune
règle interne ne peut voir qu'un musée n'a jamais publié que sa mauvaise
position : il faut confronter la position à la VILLE écrite dans la notice.

Ce que fait ce script. Il compare la position de chaque musée au centre de sa
commune et signale les écarts, sur les deux exports qui portent des coordonnées
— musees.json (tous les musées versants) et artistes.json (ceux qui s'affichent
sur les cartes des fiches). Il ne corrige rien et ne produit aucun export : c'est
un contrôle, à lancer après chaque lot d'artistes et avant toute publication.

La commune est cherchée par son nom EXACT et DANS SON DÉPARTEMENT (Joconde le
donne) : sans cela, les homonymes font du bruit — Saint-Denis de Seine-Saint-Denis
contre celui de La Réunion, « La Châtre » contre « La Châtre-Langlin », à 50 km
dans le même département.

Limite connue : la référence est le centre de la commune. Dans une commune très
étendue, un musée réellement bien placé peut s'en écarter de plus de 15 km — les
deux musées d'Arles (758 km²) sortent ainsi à chaque passage. Un écart signalé
est une question, pas un verdict.

Référence. Le découpage administratif de l'État (geo.api.gouv.fr, Licence
Ouverte). C'est une source de CONTRÔLE, jamais une source de données : aucune
coordonnée n'en sort pour être affichée, aucun chiffre n'en dépend. À déclarer
comme telle si un résultat en découle (docs/decisions.md, 2026-08-05).

Usage : uv run python src/audit_geoloc.py [--seuil 15]
"""

import argparse
import json
import math
import time
import unicodedata
import urllib.parse
import urllib.request

from config import DOSSIER_EXPORTS

DOSSIER_WEB = DOSSIER_EXPORTS / "web"
API = "https://geo.api.gouv.fr/communes"


def distance_km(lat1, lon1, lat2, lon2) -> float:
    rayon = 6371
    dlat, dlon = math.radians(lat2 - lat1), math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2
         + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2))
         * math.sin(dlon / 2) ** 2)
    return 2 * rayon * math.asin(math.sqrt(a))


def _pivot(texte: str) -> str:
    """Comparaison de noms de lieux : sans accents, sans casse, sans traits."""
    sans = unicodedata.normalize("NFD", texte or "")
    sans = "".join(c for c in sans if unicodedata.category(c) != "Mn")
    return sans.lower().replace("-", " ").replace("'", " ").strip()


def centre_commune(ville: str, departement: str | None, cache: dict):
    """Centre de la commune, cherchée dans son département quand Joconde le donne.

    Rend (lat, lon, nom, département, sûr) — `sûr` est faux quand le département
    n'a pas pu être confirmé : le résultat sert alors d'indication, pas de verdict.
    Les communes déléguées (Caudebec-en-Caux, Villequier) et les libellés à
    rallonge (« Saint-Denis de La Réunion ») ne sont pas trouvés : ils ressortent
    en « non contrôlés », jamais en erreurs.
    """
    cle = (ville, departement)
    if cle in cache:
        return cache[cle]
    url = (f"{API}?nom={urllib.parse.quote(ville or '')}"
           "&fields=nom,centre,departement&limit=15&boost=population")
    try:
        with urllib.request.urlopen(url, timeout=20) as reponse:
            communes = [c for c in json.load(reponse) if c.get("centre")]
    except Exception:
        communes = []

    # Le nom doit correspondre EXACTEMENT : l'API répond aussi aux voisins par
    # préfixe, et « La Châtre » ramène « La Châtre-Langlin », à 50 km, dans le
    # même département. Le département départage ensuite les homonymes.
    trouve = None
    exactes = [c for c in communes if _pivot(c["nom"]) == _pivot(ville or "")]
    if departement:
        for commune in exactes:
            nom_dep = (commune.get("departement") or {}).get("nom", "")
            if _pivot(nom_dep) == _pivot(departement):
                lon, lat = commune["centre"]["coordinates"]
                trouve = (lat, lon, commune["nom"], nom_dep, True)
                break
    if trouve is None and len(exactes) == 1:
        commune = exactes[0]
        lon, lat = commune["centre"]["coordinates"]
        trouve = (lat, lon, commune["nom"],
                  (commune.get("departement") or {}).get("nom", "?"), True)
    if trouve is None and communes:
        commune = communes[0]
        lon, lat = commune["centre"]["coordinates"]
        trouve = (lat, lon, commune["nom"],
                  (commune.get("departement") or {}).get("nom", "?"), False)
    cache[cle] = trouve
    return trouve


def _lire(fichier):
    return json.loads((DOSSIER_WEB / fichier).read_text(encoding="utf-8"))


def positions_publiees() -> dict:
    """code Muséofile -> (nom, ville, département, {positions}, notices de doute,
    sur_les_cartes). Les deux exports sont réunis : musees.json donne la ville et
    le département de tous les musées versants, artistes.json dit lesquels
    s'affichent réellement sur une carte de fiche."""
    musees = {}
    for m in _lire("musees.json"):
        if m.get("coord"):
            musees[m["code_museofile"]] = {
                "nom": m["nom"], "ville": m["ville"],
                "departement": m.get("departement"),
                "positions": {tuple(m["coord"])}, "doute": m["doute"],
                "carte": False}

    for artiste in _lire("artistes.json")["artistes"]:
        for m in artiste.get("musees_doute", []):
            if m.get("lat") is None:
                continue
            entree = musees.setdefault(m["code"], {
                "nom": m["nom"], "ville": m["ville"], "departement": None,
                "positions": set(), "doute": 0, "carte": True})
            entree["carte"] = True
            entree["positions"].add((m["lat"], m["lon"]))
    return musees


def main() -> None:
    parseur = argparse.ArgumentParser(description=__doc__)
    parseur.add_argument("--seuil", type=float, default=15,
                         help="écart en km au-delà duquel on signale (défaut : 15)")
    options = parseur.parse_args()

    musees = positions_publiees()
    cache, suspects, indices, non_controles, instables = {}, [], [], [], []

    for code, m in sorted(musees.items()):
        if len(m["positions"]) > 1:
            instables.append(f"{code} {m['nom']} ({m['ville']})")
        reference = centre_commune(m["ville"] or "", m["departement"], cache)
        time.sleep(0.03)
        if not reference:
            non_controles.append(f"{code} {m['nom']} ({m['ville']})")
            continue
        for lat, lon in m["positions"]:
            ecart = distance_km(lat, lon, reference[0], reference[1])
            if ecart <= options.seuil:
                continue
            ligne = (round(ecart, 1), code, m["nom"], m["ville"], m["doute"],
                     m["carte"], lat, lon)
            (suspects if reference[4] else indices).append(ligne)

    total_carte = sum(1 for m in musees.values() if m["carte"])
    print(f"musées contrôlés            : {len(musees)} "
          f"(dont {total_carte} affichés sur une carte de fiche)")
    print(f"positions instables         : {len(instables)} "
          "(un musée à deux endroits selon la fiche — ne doit plus arriver)")
    for ligne in instables:
        print(f"    {ligne}")

    print(f"\nécarts confirmés > {options.seuil:g} km   : {len(suspects)}")
    for ecart, code, nom, ville, doute, carte, lat, lon in sorted(suspects, reverse=True):
        marque = "CARTE" if carte else "     "
        print(f"    {marque} {ecart:>7} km  {code}  {nom} ({ville}) — "
              f"{doute} notice(s) prudente(s) → {lat}, {lon}")

    print(f"\nà vérifier à la main        : {len(indices) + len(non_controles)}")
    print("  (département non confirmé — homonymes de communes)")
    for ecart, code, nom, ville, doute, carte, lat, lon in sorted(indices, reverse=True):
        print(f"    {ecart:>7} km  {code}  {nom} ({ville})")
    print("  (commune introuvable — communes déléguées, libellés à rallonge)")
    for ligne in non_controles:
        print(f"    {ligne}")

    if not suspects and not instables:
        print("\nAucune position aberrante confirmée.")


if __name__ == "__main__":
    main()
