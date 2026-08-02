"""Palier 1 du chantier « vignettes » (2026-07-29) : inventorier et classer les
droits de réutilisation de la PHOTO de chaque œuvre de l'onglet « Œuvres ».

Ne modifie pas le front et ne télécharge AUCUNE image (Palier 2 après validation).

Chaîne :
  1. inventaire des références UNIQUES des fiches oeuvres/<slug>.json
     (une référence liée à deux maîtres n'est comptée qu'une fois) ;
  2. jointure au CSV Joconde : `Presence_image` (pré-filtre) et
     `Artiste_sous_droits` (signal restrictif) ;
  3. pour les références avec image : lecture de la notice POP, extraction du
     seul champ « Crédits photographiques » (clé PHOT) et de l'image principale
     (clé IMG), avec CACHE disque et requêtes limitées ;
  4. classement en cinq statuts (src/images_classify.py) ;
  5. livrables : registre CSV, JSON indexé, bilan (comptes, répartitions,
     échantillon par statut, crédits non reconnus).

Le cache (data/cache/pop_images.json) rend le script résumable : on ne
réinterroge jamais une notice déjà lue. Relancer reprend là où on s'est arrêté.

Usage : uv run python src/build_images.py
"""

import csv
import glob
import gzip
import json
import re
import sys
import time
import urllib.request
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import date

from config import CHEMIN_CSV, DOSSIER_EXPORTS, RACINE, URL_NOTICE_POP
from images_classify import classer

DOSSIER_OEUVRES = DOSSIER_EXPORTS / "web" / "oeuvres"
DOSSIER_CACHE = RACINE / "data" / "cache"
CACHE_POP = DOSSIER_CACHE / "pop_images.json"

# Image principale : chemin relatif (IMG) servi depuis le stockage objet de POP.
BASE_IMAGE = "https://popcorn-prd-perf-assets.s3.gra.io.cloud.ovh.net/"

MAX_WORKERS = 6          # requêtes concurrentes, poli pour une plateforme publique
PAUSE = 0.05             # petite pause par requête (limiter la charge)
UA = "inventaire-du-doute/1.0 (réutilisation Licence Ouverte ; contact projet)"

csv.field_size_limit(min(sys.maxsize, 2**31 - 1))


# --------------------------------------------------------------------------
# 1. Inventaire des références uniques
# --------------------------------------------------------------------------
def inventaire() -> dict:
    """ref -> {artistes:[…], musee, ville, titre}. Une référence partagée entre
    deux maîtres n'apparaît qu'une fois, avec les deux noms."""
    inv = {}
    for chemin in sorted(glob.glob(str(DOSSIER_OEUVRES / "*.json"))):
        fiche = json.load(open(chemin, encoding="utf-8"))
        for o in fiche["oeuvres"]:
            e = inv.setdefault(o["reference"], {
                "artistes": [], "musee": o.get("musee"),
                "ville": o.get("ville"), "titre": o.get("titre")})
            if fiche["nom"] not in e["artistes"]:
                e["artistes"].append(fiche["nom"])
    return inv


# --------------------------------------------------------------------------
# 2. Jointure CSV : présence d'image + artiste sous droits
# --------------------------------------------------------------------------
def joindre_csv(inv: dict) -> None:
    """Une seule passe du CSV (1,1 Go) : renseigne `presence_image` et
    `artiste_sous_droits` pour chaque référence de l'inventaire."""
    refs = set(inv)
    trouves = 0
    with open(CHEMIN_CSV, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f, delimiter="|"):
            ref = r["Reference"]
            if ref in refs:
                inv[ref]["presence_image"] = (r.get("Presence_image") or "").strip()
                inv[ref]["artiste_sous_droits"] = (r.get("Artiste_sous_droits") or "").strip()
                trouves += 1
                if trouves == len(refs):
                    break
    for e in inv.values():
        e.setdefault("presence_image", "")
        e.setdefault("artiste_sous_droits", "")


# --------------------------------------------------------------------------
# 3. Lecture des notices POP (champ PHOT + image), avec cache
# --------------------------------------------------------------------------
_RE_PHOT = re.compile(r'\\"PHOT\\":\\"(.*?)\\"')
_RE_COPY = re.compile(r'\\"COPY\\":\\"(.*?)\\"')
_RE_IMG = re.compile(r'\\"IMG\\":\[\\"(.*?)\\"')


def _extraire(html: str) -> dict:
    """Depuis la notice POP (Next.js, données JSON embarquées) : le champ
    « Crédits photographiques » (PHOT), les mentions légales (COPY) et le chemin
    de l'image principale (IMG). On ne lit QUE ces champs — jamais le reste de
    la page (dont le pied cite Etalab pour le site lui-même)."""
    mp = _RE_PHOT.search(html)
    mc = _RE_COPY.search(html)
    mi = _RE_IMG.search(html)
    return {
        "phot": mp.group(1) if mp else None,
        "copy": mc.group(1) if mc else None,
        "img": mi.group(1) if mi else None,
    }


def _lire_notice(ref: str) -> dict:
    """Récupère et extrait une notice ; renvoie aussi le code HTTP."""
    url = URL_NOTICE_POP.format(reference=ref)
    req = urllib.request.Request(url, headers={
        "User-Agent": UA, "Accept-Encoding": "gzip"})
    try:
        with urllib.request.urlopen(req, timeout=30) as rep:
            raw = rep.read()
            if rep.headers.get("Content-Encoding") == "gzip":
                raw = gzip.decompress(raw)
            data = _extraire(raw.decode("utf-8", "replace"))
            data["http"] = rep.status
    except urllib.error.HTTPError as ex:
        data = {"phot": None, "copy": None, "img": None, "http": ex.code}
    except Exception as ex:  # réseau, délai… : à réessayer plus tard
        data = {"phot": None, "copy": None, "img": None, "http": 0,
                "erreur": str(ex)[:80]}
    time.sleep(PAUSE)
    return data


def lire_notices(refs_a_lire: list, cache: dict) -> None:
    """Lit en parallèle les notices manquantes, met le cache à jour au fil de
    l'eau (sauvegarde périodique → résumable)."""
    aujourdhui = date.today().isoformat()
    a_faire = [r for r in refs_a_lire if r not in cache or cache[r].get("http") in (0, None)]
    total = len(a_faire)
    if not total:
        print("  cache complet, aucune notice à lire.")
        return
    print(f"  {total} notices à lire (cache : {len(cache)} déjà présentes)…")
    faits = 0
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
        futs = {pool.submit(_lire_notice, r): r for r in a_faire}
        for fut in as_completed(futs):
            ref = futs[fut]
            data = fut.result()
            data["verifie_le"] = aujourdhui
            cache[ref] = data
            faits += 1
            if faits % 200 == 0:
                _sauver_cache(cache)
                print(f"    {faits}/{total} lues", flush=True)
    _sauver_cache(cache)
    print(f"    {faits}/{total} lues (terminé).")


def _charger_cache() -> dict:
    if CACHE_POP.exists():
        return json.load(open(CACHE_POP, encoding="utf-8"))
    return {}


def _sauver_cache(cache: dict) -> None:
    DOSSIER_CACHE.mkdir(parents=True, exist_ok=True)
    CACHE_POP.write_text(json.dumps(cache, ensure_ascii=False), encoding="utf-8")


# --------------------------------------------------------------------------
# 4. + 5. Classement et livrables
# --------------------------------------------------------------------------
def main() -> None:
    print("Inventaire des références uniques…")
    inv = inventaire()
    nb_fiches = len(glob.glob(str(DOSSIER_OEUVRES / "*.json")))
    print(f"  {len(inv)} références uniques ({nb_fiches} fiches).")

    print("Jointure au CSV Joconde (présence d'image, artiste sous droits)…")
    joindre_csv(inv)
    avec_image = [r for r, e in inv.items() if e["presence_image"] == "oui"]
    print(f"  {len(avec_image)} avec image, {len(inv) - len(avec_image)} sans.")

    print("Lecture des notices POP (champ PHOT), cache + requêtes limitées…")
    cache = _charger_cache()
    lire_notices(avec_image, cache)

    print("Classement…")
    records = {}
    credits_non_reconnus = Counter()
    for ref, e in inv.items():
        pop = cache.get(ref, {})
        presence = e["presence_image"] == "oui"
        phot = pop.get("phot")
        statut, licence, credit, raison = classer(
            phot, presence_image=presence,
            artiste_sous_droits=e["artiste_sous_droits"])
        img = pop.get("img")
        records[ref] = {
            "reference": ref,
            "statut": statut,
            "licence": licence,
            "credit": credit,
            "raison": raison,
            "artistes": e["artistes"],
            "musee": e["musee"],
            "ville": e["ville"],
            "titre": e["titre"],
            "presence_image": e["presence_image"],
            "artiste_sous_droits": e["artiste_sous_droits"],
            "image": (BASE_IMAGE + img) if img else "",
            "img_rel": img or "",
            "notice_pop": URL_NOTICE_POP.format(reference=ref),
            "http": pop.get("http"),
            "verifie_le": pop.get("verifie_le", ""),
        }
        if statut == "unknown" and credit and "examiner" not in raison:
            credits_non_reconnus[credit] += 1

    _ecrire_livrables(records, credits_non_reconnus)


def _ecrire_livrables(records: dict, credits_non_reconnus: Counter) -> None:
    DOSSIER_EXPORTS.mkdir(parents=True, exist_ok=True)

    # 5a. Registre CSV humainement vérifiable.
    chemin_csv = DOSSIER_EXPORTS / "images_oeuvres.csv"
    colonnes = ["reference", "statut", "licence", "credit", "raison",
                "artistes", "musee", "ville", "titre", "presence_image",
                "artiste_sous_droits", "image", "notice_pop", "http", "verifie_le"]
    with open(chemin_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=colonnes, extrasaction="ignore")
        w.writeheader()
        for ref in sorted(records):
            r = dict(records[ref])
            r["artistes"] = " ; ".join(r["artistes"])
            w.writerow(r)

    # 5b. JSON indexé par référence (pour le pipeline / Palier 2).
    chemin_json = DOSSIER_EXPORTS / "images_oeuvres.json"
    chemin_json.write_text(json.dumps(records, ensure_ascii=False, indent=1),
                           encoding="utf-8")

    # 5c. Bilan : comptes, répartitions, échantillon, crédits non reconnus.
    par_statut = Counter(r["statut"] for r in records.values())
    par_musee = defaultdict(Counter)
    par_artiste = defaultdict(Counter)
    for r in records.values():
        par_musee[r["musee"]][r["statut"]] += 1
        for a in r["artistes"]:
            par_artiste[a][r["statut"]] += 1

    echantillon = {}
    for statut in ("open", "authorized", "restricted", "unknown", "unavailable"):
        exemples = [r for r in records.values() if r["statut"] == statut][:8]
        echantillon[statut] = [
            {"reference": r["reference"], "credit": r["credit"],
             "licence": r["licence"], "musee": r["musee"], "raison": r["raison"]}
            for r in exemples]

    bilan = {
        "date": date.today().isoformat(),
        "total_references": len(records),
        "par_statut": dict(par_statut),
        "par_musee": {m: dict(c) for m, c in sorted(
            par_musee.items(), key=lambda kv: -sum(kv[1].values()))},
        "par_artiste": {a: dict(c) for a, c in sorted(
            par_artiste.items(), key=lambda kv: -sum(kv[1].values()))},
        "echantillon_par_statut": echantillon,
        "credits_non_reconnus": credits_non_reconnus.most_common(),
    }
    (DOSSIER_EXPORTS / "images_bilan.json").write_text(
        json.dumps(bilan, ensure_ascii=False, indent=1), encoding="utf-8")

    # Résumé console.
    print("\n=== BILAN ===")
    for statut in ("open", "authorized", "restricted", "unknown", "unavailable"):
        print(f"  {statut:12} {par_statut.get(statut, 0):>5}")
    print(f"  {'TOTAL':12} {len(records):>5}")
    print(f"\nCrédits non reconnus (distincts) : {len(credits_non_reconnus)}")
    print(f"Livrables → {chemin_csv.name}, {chemin_json.name}, images_bilan.json")


if __name__ == "__main__":
    main()
