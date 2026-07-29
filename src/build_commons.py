"""Recherche de reproductions OUVERTES sur Wikimedia Commons / Wikidata pour les
œuvres de l'onglet « Œuvres » (chantier 2026-07-29). Recherche + vérification +
préparation SEULEMENT : ne touche pas au front, ne télécharge aucune image.

Deux passes (cahier des charges) :
  1. par identifiant Joconde exact  — Wikidata P347 → correspondance EXACTE ;
  2. par numéro d'inventaire         — Wikidata P217 + institution concordante
                                        → CANDIDAT à vérifier (a_verifier).
Aucune correspondance sur le seul titre/auteur/musée (règle impérative).

Les droits de CHAQUE fichier sont lus sur Commons (API imageinfo, extmetadata),
jamais devinés. On sépare strictement l'identification de l'œuvre (match_status)
et les droits de l'image (rights_status) : cf. src/commons_match.py.

Caches résumables sous data/cache/ (aucune requête refaite). Requêtes limitées.

Usage : uv run python src/build_commons.py
"""

import csv
import json
import sys
import time
import urllib.parse
import urllib.request
from collections import Counter
from datetime import date

from config import DOSSIER_EXPORTS, RACINE
import commons_match as cm

DOSSIER_OEUVRES = DOSSIER_EXPORTS / "web" / "oeuvres"
META_JSON = DOSSIER_EXPORTS / "oeuvres_metadonnees.json"
DOSSIER_CACHE = RACINE / "data" / "cache"
CACHE_P1 = DOSSIER_CACHE / "commons_pass1.json"     # P347 → items
CACHE_P2 = DOSSIER_CACHE / "commons_pass2.json"     # inventaire → items
CACHE_FILES = DOSSIER_CACHE / "commons_files.json"  # fichier Commons → droits
CACHE_CANDMETA = DOSSIER_CACHE / "commons_candmeta.json"  # QID candidat → métadonnées

UA = "inventaire-du-doute/1.0 (projet data-journalisme ; contact hericlibong@gmail.com)"
SPARQL = "https://query.wikidata.org/sparql"
COMMONS_API = "https://commons.wikimedia.org/w/api.php"
PAUSE = 0.4

csv.field_size_limit(min(sys.maxsize, 2**31 - 1))


# --------------------------------------------------------------------------
# Réseau
# --------------------------------------------------------------------------
def _get_json(url: str, data: bytes = None) -> dict:
    req = urllib.request.Request(url, data=data, headers={
        "User-Agent": UA, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=90) as r:
        return json.load(r)


def _sparql(query: str) -> list:
    # POST (et non GET) : les requêtes par lots dépassent la taille d'URL admise
    # (HTTP 431). Corps urlencodé, résultat JSON.
    corps = urllib.parse.urlencode({"query": query, "format": "json"}).encode("utf-8")
    req = urllib.request.Request(SPARQL, data=corps, headers={
        "User-Agent": UA, "Accept": "application/sparql-results+json",
        "Content-Type": "application/x-www-form-urlencoded"})
    for essai in range(3):
        try:
            with urllib.request.urlopen(req, timeout=90) as r:
                return json.load(r)["results"]["bindings"]
        except Exception:
            if essai == 2:
                raise
            time.sleep(2 + essai * 3)
    return []


import re as _re


def _texte(html: str) -> str:
    """Les crédits Commons (extmetadata Artist/Credit) arrivent en HTML
    (« <bdi><a…>Charles Le Brun</a></bdi> »). On garde le TEXTE exact du crédit,
    sans le balisage, pour un CSV lisible et un affichage futur propre."""
    if not html:
        return ""
    sans = _re.sub(r"<[^>]+>", " ", html)
    sans = (sans.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
            .replace("&#160;", " ").replace("&nbsp;", " ").replace("&quot;", '"'))
    return _re.sub(r"\s+", " ", sans).strip()


def _nom_fichier_commons(url_p18: str) -> str:
    """P18 renvoie …/Special:FilePath/Nom%20du%20fichier.jpg → « Nom du fichier.jpg »."""
    if not url_p18:
        return ""
    nom = url_p18.rsplit("/", 1)[-1]
    return urllib.parse.unquote(nom)


# --------------------------------------------------------------------------
# Chargement local
# --------------------------------------------------------------------------
def charger_inventaire() -> dict:
    """ref -> {artistes:[…], musee, ville, titre} depuis les 63 fiches."""
    import glob
    inv = {}
    for chemin in glob.glob(str(DOSSIER_OEUVRES / "*.json")):
        d = json.load(open(chemin, encoding="utf-8"))
        for o in d["oeuvres"]:
            e = inv.setdefault(o["reference"], {
                "artistes": [], "musee": o.get("musee"),
                "ville": o.get("ville"), "titre": o.get("titre")})
            if d["nom"] not in e["artistes"]:
                e["artistes"].append(d["nom"])
    return inv


def _cache(chemin) -> dict:
    return json.load(open(chemin, encoding="utf-8")) if chemin.exists() else {}


def _sauver(chemin, obj) -> None:
    DOSSIER_CACHE.mkdir(parents=True, exist_ok=True)
    chemin.write_text(json.dumps(obj, ensure_ascii=False), encoding="utf-8")


# --------------------------------------------------------------------------
# Passe 1 — identifiant Joconde (P347)
# --------------------------------------------------------------------------
def passe1(refs: list) -> dict:
    """ref -> {qid, image, inventaire:[…], collection:[…], joconde_ids:[ref]}."""
    cache = _cache(CACHE_P1)
    a_faire = [r for r in refs if r not in cache]
    if a_faire:
        print(f"  Passe 1 (P347) : {len(a_faire)} références à interroger…")
        B = 300
        for i in range(0, len(a_faire), B):
            lot = a_faire[i:i + B]
            vals = " ".join('"%s"' % r for r in lot)
            q = ("SELECT ?item ?jid ?image ?inv ?collLabel WHERE { "
                 "VALUES ?jid { %s } ?item wdt:P347 ?jid . "
                 "OPTIONAL { ?item wdt:P18 ?image. } "
                 "OPTIONAL { ?item wdt:P217 ?inv. } "
                 "OPTIONAL { ?item wdt:P195 ?coll. ?coll rdfs:label ?collLabel. "
                 'FILTER(lang(?collLabel)="fr") } }') % vals
            trouve = {}
            for r in _sparql(q):
                jid = r["jid"]["value"]
                e = trouve.setdefault(jid, {"qid": r["item"]["value"].rsplit("/", 1)[-1],
                                            "image": "", "inventaire": set(),
                                            "collection": set(), "joconde_ids": [jid]})
                if r.get("image") and not e["image"]:
                    e["image"] = _nom_fichier_commons(r["image"]["value"])
                if r.get("inv"):
                    e["inventaire"].add(r["inv"]["value"])
                if r.get("collLabel"):
                    e["collection"].add(r["collLabel"]["value"])
            for r in lot:                       # mémoriser aussi les absences
                e = trouve.get(r)
                cache[r] = None if e is None else {
                    "qid": e["qid"], "image": e["image"],
                    "inventaire": sorted(e["inventaire"]),
                    "collection": sorted(e["collection"]),
                    "joconde_ids": e["joconde_ids"]}
            _sauver(CACHE_P1, cache)
            print(f"    {min(i + B, len(a_faire))}/{len(a_faire)} "
                  f"(appariés : {sum(1 for v in cache.values() if v)})", flush=True)
            time.sleep(PAUSE)
    return {r: v for r, v in cache.items() if v}


# --------------------------------------------------------------------------
# Passe 2 — numéro d'inventaire (P217) pour les références sans P347
# --------------------------------------------------------------------------
def passe2(refs_restantes: list, meta: dict) -> dict:
    """ref -> [candidats] : items Wikidata dont un P217 égale l'inventaire de la
    notice. On restreint aux items EN COLLECTION (P195) pour limiter le bruit ;
    l'institution est contrôlée ensuite (commons_match). Candidats seulement."""
    cache = _cache(CACHE_P2)
    # index inventaire normalisé -> [refs] (plusieurs notices peuvent partager un
    # inventaire brut, mais l'institution départagera)
    par_inv = {}
    for r in refs_restantes:
        inv = meta.get(r, {}).get("numero_inventaire", "")
        if inv:
            par_inv.setdefault(inv, []).append(r)
    invs = [i for i in par_inv if i not in cache.get("_inv_faits", [])]
    faits = set(cache.get("_inv_faits", []))
    if invs:
        print(f"  Passe 2 (inventaire) : {len(invs)} inventaires à interroger…")
        B = 120
        for i in range(0, len(invs), B):
            lot = invs[i:i + B]
            vals = " ".join('"%s"' % v.replace('"', '\\"') for v in lot)
            q = ("SELECT ?item ?inv ?image ?collLabel ?itemLabel WHERE { "
                 "VALUES ?inv { %s } ?item wdt:P217 ?inv . ?item wdt:P195 ?coll . "
                 "OPTIONAL { ?item wdt:P18 ?image. } "
                 '?coll rdfs:label ?collLabel. FILTER(lang(?collLabel)="fr") '
                 '?item rdfs:label ?itemLabel. FILTER(lang(?itemLabel)="fr") }') % vals
            par_item = {}
            for r in _sparql(q):
                inv = r["inv"]["value"]
                qid = r["item"]["value"].rsplit("/", 1)[-1]
                key = (inv, qid)
                e = par_item.setdefault(key, {"qid": qid, "inv": inv, "image": "",
                                              "collection": set(), "titre": ""})
                if r.get("image") and not e["image"]:
                    e["image"] = _nom_fichier_commons(r["image"]["value"])
                if r.get("collLabel"):
                    e["collection"].add(r["collLabel"]["value"])
                if r.get("itemLabel"):
                    e["titre"] = r["itemLabel"]["value"]
            # rattacher chaque item trouvé aux notices qui portent cet inventaire
            for (inv, qid), e in par_item.items():
                for ref in par_inv.get(inv, []):
                    cand = {"qid": qid, "image": e["image"],
                            "inventaire": [e["inv"]], "collection": sorted(e["collection"]),
                            "titre": e["titre"], "joconde_ids": []}
                    cache.setdefault(ref, [])
                    if not isinstance(cache[ref], list):
                        cache[ref] = []
                    cache[ref].append(cand)
            faits.update(lot)
            cache["_inv_faits"] = sorted(faits)
            _sauver(CACHE_P2, cache)
            print(f"    {min(i + B, len(invs))}/{len(invs)} inventaires", flush=True)
            time.sleep(PAUSE)
    return {r: v for r, v in cache.items() if r != "_inv_faits" and v}


# --------------------------------------------------------------------------
# Métadonnées Wikidata des candidats (vérification par les dimensions)
# --------------------------------------------------------------------------
def metadonnees_candidats(qids: list) -> dict:
    """QID -> {h, w, creator, inception, label}. Dimensions (P2048/P2049) en cm,
    créateur (P170), datation (P571), libellé — de quoi confirmer ou écarter un
    candidat par recoupement des métadonnées."""
    cache = _cache(CACHE_CANDMETA)
    a_faire = [q for q in qids if q not in cache]
    if a_faire:
        print(f"  {len(a_faire)} candidats à documenter (Wikidata)…")
        B = 120
        for i in range(0, len(a_faire), B):
            lot = a_faire[i:i + B]
            vals = " ".join("wd:" + q for q in lot)
            q = ("SELECT ?item ?h ?w ?creatorLabel ?inception ?itemLabel WHERE { "
                 "VALUES ?item { %s } "
                 "OPTIONAL { ?item wdt:P2048 ?h. } OPTIONAL { ?item wdt:P2049 ?w. } "
                 "OPTIONAL { ?item wdt:P170 ?creator. ?creator rdfs:label ?creatorLabel. "
                 'FILTER(lang(?creatorLabel)="fr") } '
                 "OPTIONAL { ?item wdt:P571 ?inception. } "
                 '?item rdfs:label ?itemLabel. FILTER(lang(?itemLabel)="fr") }') % vals
            def _nombre(bind):
                # certaines valeurs sont « inconnues » (nœud anonyme) : on ignore.
                if not bind or bind.get("type") != "literal":
                    return None
                try:
                    return float(bind["value"])
                except ValueError:
                    return None

            trouve = {}
            for r in _sparql(q):
                qid = r["item"]["value"].rsplit("/", 1)[-1]
                e = trouve.setdefault(qid, {})
                if "h" not in e and _nombre(r.get("h")) is not None:
                    e["h"] = _nombre(r["h"])
                if "w" not in e and _nombre(r.get("w")) is not None:
                    e["w"] = _nombre(r["w"])
                if r.get("creatorLabel") and "creator" not in e:
                    e["creator"] = r["creatorLabel"]["value"]
                if r.get("inception") and "inception" not in e:
                    e["inception"] = r["inception"]["value"][:4]
                if r.get("itemLabel") and "label" not in e:
                    e["label"] = r["itemLabel"]["value"]
            for qid in lot:
                cache[qid] = trouve.get(qid, {})
            _sauver(CACHE_CANDMETA, cache)
            time.sleep(PAUSE)
    return cache


# --------------------------------------------------------------------------
# Droits des fichiers Commons (imageinfo / extmetadata)
# --------------------------------------------------------------------------
def droits_fichiers(fichiers: set) -> dict:
    """nom_fichier -> {license_short, license_code, license_url, credit, creator,
    file_url, page_url, rights_status, licence}. En lots de 50 (limite API)."""
    cache = _cache(CACHE_FILES)
    a_faire = sorted(f for f in fichiers if f and f not in cache)
    if a_faire:
        print(f"  Droits Commons : {len(a_faire)} fichiers à contrôler…")
        B = 50
        for i in range(0, len(a_faire), B):
            lot = a_faire[i:i + B]
            titres = "|".join("File:" + f for f in lot)
            params = {"action": "query", "prop": "imageinfo",
                      "iiprop": "extmetadata|url", "format": "json",
                      "iiextmetadatafilter": "LicenseShortName|License|LicenseUrl|Artist|Credit|UsageTerms",
                      "titles": titres}
            url = COMMONS_API + "?" + urllib.parse.urlencode(params)
            data = _get_json(url)
            pages = data.get("query", {}).get("pages", {})
            # relier chaque page à son nom de fichier (sans « File: »)
            for page in pages.values():
                titre = page.get("title", "")
                nom = titre[5:] if titre.startswith("File:") else titre
                ii = (page.get("imageinfo") or [{}])[0]
                ext = ii.get("extmetadata", {})
                def val(k):
                    return (ext.get(k, {}) or {}).get("value", "") if isinstance(ext.get(k), dict) else ""
                short = val("LicenseShortName")
                code = val("License")
                rights, licence = cm.classer_droits_commons(short, code)
                cache[nom] = {
                    "license_short": short, "license_code": code,
                    "license_url": val("LicenseUrl"),
                    "credit": val("Credit"), "creator": val("Artist"),
                    "file_url": ii.get("url", ""),
                    "page_url": ii.get("descriptionurl", "")
                                or ("https://commons.wikimedia.org/wiki/File:"
                                    + urllib.parse.quote(nom)),
                    "rights_status": rights, "licence": licence}
            for f in lot:
                cache.setdefault(f, {"rights_status": cm.UNKNOWN, "licence": "",
                                     "license_short": "", "license_code": "",
                                     "license_url": "", "credit": "", "creator": "",
                                     "file_url": "", "page_url":
                                     "https://commons.wikimedia.org/wiki/File:"
                                     + urllib.parse.quote(f)})
            _sauver(CACHE_FILES, cache)
            print(f"    {min(i + B, len(a_faire))}/{len(a_faire)}", flush=True)
            time.sleep(PAUSE)
    return cache


# --------------------------------------------------------------------------
# Assemblage des correspondances
# --------------------------------------------------------------------------
def _record(ref, inv_local, cand, statut, methode, evidence, droits):
    return {
        "reference_joconde": ref,
        "source_type": "wikimedia_commons",
        "source_page_url": droits.get("page_url", ""),
        "file_url": droits.get("file_url", ""),
        "credit": _texte(droits.get("credit", "")),
        "creator": _texte(droits.get("creator", "")),
        "license": droits.get("license_short", "") or droits.get("licence", ""),
        "license_url": droits.get("license_url", ""),
        "rights_status": droits.get("rights_status", cm.UNKNOWN),
        "match_status": statut,
        "match_method": methode,
        "match_evidence": evidence,
        "wikidata_qid": cand.get("qid", ""),
        "commons_file": cand.get("image", ""),
        "artistes": inv_local["artistes"],
        "musee_joconde": inv_local["musee"],
        "titre_joconde": inv_local["titre"],
        "verified_by": "auto",
        "verified_at": date.today().isoformat(),
        "note_verification": "",
    }


def main() -> None:
    print("Chargement local…")
    inv = charger_inventaire()
    meta = json.load(open(META_JSON, encoding="utf-8"))
    refs = list(inv)
    print(f"  {len(refs)} références.")

    print("Passe 1 — identifiant Joconde (P347)…")
    p1 = passe1(refs)
    print(f"  {len(p1)} références avec item Wikidata (P347).")

    restantes = [r for r in refs if r not in p1]
    print(f"Passe 2 — numéro d'inventaire ({len(restantes)} références restantes)…")
    p2 = passe2(restantes, meta)
    print(f"  {len(p2)} références avec au moins un candidat par inventaire.")

    # Vérification des candidats : on récupère les métadonnées Wikidata (surtout
    # les DIMENSIONS) pour confirmer ou écarter chaque candidat — jamais sur le
    # seul inventaire (voir commons_match.decider_match).
    qids = {c["qid"] for cands in p2.values() for c in cands if c.get("qid")}
    print(f"Vérification : métadonnées Wikidata de {len(qids)} candidats…")
    cmeta = metadonnees_candidats(sorted(qids))
    for cands in p2.values():
        for c in cands:
            info = cmeta.get(c.get("qid"), {})
            c["h"] = info.get("h")
            c["w"] = info.get("w")
            c["auteur"] = info.get("creator", "")
            if info.get("label"):
                c["titre"] = info["label"]

    # fichiers Commons à contrôler (exacts + candidats)
    fichiers = {c["image"] for c in p1.values() if c.get("image")}
    for cands in p2.values():
        for c in cands:
            if c.get("image"):
                fichiers.add(c["image"])
    print(f"Contrôle des droits de {len(fichiers)} fichiers Commons…")
    droits = droits_fichiers(fichiers)

    print("Assemblage des correspondances…")
    records = []
    for ref in refs:
        m = meta.get(ref, {})
        loc = inv[ref]
        if ref in p1:
            cand = p1[ref]
            statut, methode, ev = cm.decider_match(ref, m, cand)
            dr = droits.get(cand.get("image", ""), {}) if cand.get("image") else {}
            records.append(_record(ref, loc, cand, statut, methode, ev, dr))
        elif ref in p2:
            # on GARDE les rejetés (collisions d'inventaire entre institutions) :
            # ce sont les faux rapprochements, utiles à documenter et à contrôler.
            vus = set()
            for cand in p2[ref]:
                if cand.get("qid") in vus:
                    continue
                vus.add(cand.get("qid"))
                statut, methode, ev = cm.decider_match(ref, m, cand)
                dr = droits.get(cand.get("image", ""), {}) if cand.get("image") else {}
                rec = _record(ref, loc, cand, statut, methode, ev, dr)
                # trace du recoupement (dimensions/titre) : trie les candidats pour
                # l'œil humain, ne tranche jamais
                dim, tit = ev.get("dimensions_match"), ev.get("title_match")
                if ev.get("dimensions_conflit"):
                    rec["note_verification"] = "rejeté : dimensions incompatibles"
                elif dim and tit:
                    rec["note_verification"] = "forte présomption : dimensions ET titre concordants — à confirmer"
                elif dim:
                    rec["note_verification"] = "dimensions concordantes, titre différent — à vérifier"
                elif tit:
                    rec["note_verification"] = "titre concordant, dimensions absentes — à vérifier"
                else:
                    rec["note_verification"] = "à vérifier (dimensions/titre non concluants)"
                records.append(rec)

    _ecrire(records, len(refs), len(p1), len(p2))


def _ecrire(records, n_refs, n_p1, n_p2):
    DOSSIER_EXPORTS.mkdir(parents=True, exist_ok=True)
    # 1. Export structuré JSON.
    (DOSSIER_EXPORTS / "commons_correspondances.json").write_text(
        json.dumps(records, ensure_ascii=False, indent=1), encoding="utf-8")

    # 2. CSV lisible pour vérification manuelle.
    colonnes = ["reference_joconde", "match_status", "match_method", "rights_status",
                "license", "titre_joconde", "musee_joconde", "artistes",
                "wikidata_qid", "commons_file", "source_page_url", "file_url",
                "credit", "creator", "license_url", "match_evidence",
                "verified_by", "verified_at", "note_verification"]
    with open(DOSSIER_EXPORTS / "commons_correspondances.csv", "w",
              newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=colonnes, extrasaction="ignore")
        w.writeheader()
        for r in sorted(records, key=lambda x: (x["match_status"], x["reference_joconde"])):
            row = dict(r)
            row["artistes"] = " ; ".join(r["artistes"])
            row["match_evidence"] = ";".join(k for k, v in r["match_evidence"].items() if v)
            w.writerow(row)

    # 3. Bilan chiffré + échantillon de contrôle.
    par_match = Counter(r["match_status"] for r in records)
    exacts = [r for r in records if r["match_status"] == cm.EXACT]
    exacts_avec_image = [r for r in exacts if r["commons_file"]]
    exacts_sans_image = [r for r in exacts if not r["commons_file"]]
    candidats = [r for r in records if r["match_status"] == cm.A_VERIFIER]
    rejetes = [r for r in records if r["match_status"] == cm.REJETE]
    par_licence_detail = Counter(r["license"] for r in exacts_avec_image if r["rights_status"] == cm.OPEN)
    retenables = [r for r in exacts if cm.retenable(r["match_status"], r["rights_status"])]

    def _echant(liste, n=6):
        return [{"reference_joconde": r["reference_joconde"],
                 "titre_joconde": r["titre_joconde"], "musee_joconde": r["musee_joconde"],
                 "artistes": r["artistes"], "wikidata_qid": r["wikidata_qid"],
                 "commons_file": r["commons_file"], "license": r["license"],
                 "rights_status": r["rights_status"],
                 "evidence": [k for k, v in r["match_evidence"].items() if v]}
                for r in liste[:n]]

    exacts_p347 = [r for r in exacts if r["match_method"] == cm.M_JOCONDE]
    rejetes_dim = [r for r in rejetes if r["match_evidence"].get("dimensions_conflit")]
    # candidats les plus prometteurs pour le contrôle humain : dimensions ET titre
    presomption = [r for r in candidats
                   if r["match_evidence"].get("dimensions_match")
                   and r["match_evidence"].get("title_match")]
    bilan = {
        "date": date.today().isoformat(),
        "references_examinees": n_refs,
        "correspondances_exactes": len(exacts),
        "exactes_par_identifiant_joconde": len(exacts_p347),
        "exactes_avec_image": len(exacts_avec_image),
        "exactes_sans_image": len(exacts_sans_image),
        "candidats_a_verifier": len(candidats),
        "candidats_refs_distinctes": len(set(r["reference_joconde"] for r in candidats)),
        "candidats_forte_presomption": len(presomption),
        "faux_rapprochements_rejetes": len(rejetes),
        "dont_rejetes_par_dimensions": len(rejetes_dim),
        "images_reutilisables": len(retenables),
        "licences_ouvertes_detail": dict(par_licence_detail),
        "refs_avec_item_p347": n_p1,
        "refs_avec_candidat_inventaire": n_p2,
        "echantillon_controle": {
            "exact_par_joconde_id": _echant([r for r in exacts_avec_image
                                             if r["match_method"] == cm.M_JOCONDE]),
            "candidat_forte_presomption": _echant(presomption),
            "exact_sans_image": _echant(exacts_sans_image, 4),
            "candidat_par_inventaire": _echant(candidats),
            "faux_rapprochement_rejete_dimensions": _echant(rejetes_dim),
        },
    }
    (DOSSIER_EXPORTS / "commons_bilan.json").write_text(
        json.dumps(bilan, ensure_ascii=False, indent=1), encoding="utf-8")

    print("\n=== BILAN ===")
    print(f"  références examinées            : {n_refs}")
    print(f"  correspondances exactes (P347)  : {len(exacts)}")
    print(f"    dont avec image réutilisable  : {len(retenables)}")
    print(f"    dont sans image sur Commons   : {len(exacts_sans_image)}")
    print(f"  candidats à vérifier (invent.)  : {len(candidats)} "
          f"sur {len(set(r['reference_joconde'] for r in candidats))} références")
    print(f"    dont forte présomption        : {len(presomption)} (dimensions + titre)")
    print(f"  faux rapprochements rejetés     : {len(rejetes)} "
          f"(dont {len(rejetes_dim)} par dimensions)")
    print(f"  images réutilisables (inchangé) : {len(retenables)}")
    print(f"Livrables → commons_correspondances.{{json,csv}}, commons_bilan.json")


if __name__ == "__main__":
    main()
