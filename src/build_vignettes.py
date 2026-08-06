"""Télécharge et optimise les reproductions OUVERTES retenues (Wikimedia Commons),
puis enrichit les fiches d'œuvres pour l'onglet « Œuvres ».

N'intègre QUE les correspondances retenables : match_status == exact ET
rights_status == open (cf. src/commons_match.py). On ne hotlinke jamais Commons :
on télécharge une miniature (API Commons `iiurlwidth`), on la ré-encode en JPEG
optimisé, une seule copie locale par référence, dans data/exports/web/oeuvres_img/.
Le crédit et la licence exacts sont conservés et affichés sous l'image.

Produit :
  - data/exports/web/oeuvres_img/<reference>.jpg  (vignettes versionnées) ;
  - data/exports/web/images_index.json            (référence -> métadonnées image) ;
  - fusion de `image` dans data/exports/web/oeuvres/<slug>.json (front).

Cache résumable (data/cache/commons_thumbs.json) + vignette déjà écrite = sautée.

Usage : uv run python src/build_vignettes.py
"""

import glob
import io
import json
import time
import urllib.parse
import urllib.request
from datetime import date

from PIL import Image

from config import DOSSIER_EXPORTS, RACINE

CORRESP = DOSSIER_EXPORTS / "commons_correspondances.json"
CORRESP_GALLICA = DOSSIER_EXPORTS / "gallica_correspondances.json"
DOSSIER_OEUVRES = DOSSIER_EXPORTS / "web" / "oeuvres"
DOSSIER_IMG = DOSSIER_EXPORTS / "web" / "oeuvres_img"
INDEX = DOSSIER_EXPORTS / "web" / "images_index.json"
DOSSIER_CACHE = RACINE / "data" / "cache"
CACHE_THUMBS = DOSSIER_CACHE / "commons_thumbs.json"

COMMONS_API = "https://commons.wikimedia.org/w/api.php"
UA = "inventaire-du-doute/1.0 (projet data-journalisme ; contact hericlibong@gmail.com)"
LARGEUR = 900        # largeur maximale de la vignette (px)
QUALITE = 82         # qualité JPEG
PAUSE = 1.0          # Wikimedia limite le rendu des miniatures (HTTP 429)


def _get(url: str) -> bytes:
    # Backoff sur 429 (« too many requests ») et erreurs transitoires : Wikimedia
    # borne le rythme du rendu des miniatures.
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    for essai in range(5):
        try:
            with urllib.request.urlopen(req, timeout=90) as r:
                return r.read()
        except urllib.error.HTTPError as ex:
            if ex.code == 429 and essai < 4:
                time.sleep(5 * (essai + 1))
                continue
            raise
        except Exception:
            if essai < 4:
                time.sleep(3 * (essai + 1))
                continue
            raise
    raise RuntimeError("échec après plusieurs tentatives")


def _cache(chemin) -> dict:
    return json.load(open(chemin, encoding="utf-8")) if chemin.exists() else {}


def _sauver(chemin, obj) -> None:
    DOSSIER_CACHE.mkdir(parents=True, exist_ok=True)
    chemin.write_text(json.dumps(obj, ensure_ascii=False), encoding="utf-8")


def urls_miniatures(fichiers: list) -> dict:
    """nom_fichier Commons -> URL de miniature (largeur bornée), par l'API."""
    cache = _cache(CACHE_THUMBS)
    a_faire = [f for f in fichiers if f not in cache]
    if a_faire:
        print(f"  {len(a_faire)} miniatures à résoudre (API Commons)…")
        for i in range(0, len(a_faire), 50):
            lot = a_faire[i:i + 50]
            params = {"action": "query", "prop": "imageinfo", "iiprop": "url",
                      "iiurlwidth": str(LARGEUR), "format": "json",
                      "titles": "|".join("File:" + f for f in lot)}
            data = json.loads(_get(COMMONS_API + "?" + urllib.parse.urlencode(params)))
            for page in data.get("query", {}).get("pages", {}).values():
                titre = page.get("title", "")
                nom = titre[5:] if titre.startswith("File:") else titre
                ii = (page.get("imageinfo") or [{}])[0]
                cache[nom] = ii.get("thumburl") or ii.get("url", "")
            _sauver(CACHE_THUMBS, cache)
            time.sleep(PAUSE)
    return cache


def optimiser(donnees: bytes, chemin_sortie) -> None:
    """Ouvre l'image téléchargée, aplatit la transparence sur blanc, borne la
    largeur, ré-encode en JPEG optimisé (métadonnées retirées)."""
    im = Image.open(io.BytesIO(donnees))
    if im.mode in ("RGBA", "LA", "P"):
        im = im.convert("RGBA")
        fond = Image.new("RGB", im.size, (255, 255, 255))
        fond.paste(im, mask=im.split()[-1])
        im = fond
    else:
        im = im.convert("RGB")
    if im.width > LARGEUR:
        h = round(im.height * LARGEUR / im.width)
        im = im.resize((LARGEUR, h), Image.LANCZOS)
    im.save(chemin_sortie, "JPEG", quality=QUALITE, optimize=True, progressive=True)


def main() -> None:
    recs = json.load(open(CORRESP, encoding="utf-8"))
    retenus = [r for r in recs
               if r["match_status"] == "exact" and r["rights_status"] == "open"
               and r["commons_file"] and r["file_url"]]
    # une seule entrée par référence (au cas où)
    par_ref = {}
    for r in retenus:
        par_ref.setdefault(r["reference_joconde"], r)
    print(f"{len(par_ref)} reproductions ouvertes à intégrer.")

    thumbs = urls_miniatures(sorted({r["commons_file"] for r in par_ref.values()}))

    DOSSIER_IMG.mkdir(parents=True, exist_ok=True)
    index = {}
    telecharges = 0
    for ref, r in sorted(par_ref.items()):
        sortie = DOSSIER_IMG / f"{ref}.jpg"
        url = thumbs.get(r["commons_file"]) or r["file_url"]
        if not sortie.exists():
            try:
                optimiser(_get(url), sortie)
                telecharges += 1
                if telecharges % 25 == 0:
                    print(f"    {telecharges} vignettes téléchargées", flush=True)
                time.sleep(PAUSE)
            except Exception as ex:
                print(f"    ⚠ {ref} : {str(ex)[:80]}")
                continue
        index[ref] = {
            "statut": "open",
            "source_type": "wikimedia_commons",
            "url": f"oeuvres/{ref}.jpg",
            "credit": r["credit"],
            "creator": r["creator"],
            "licence": r["license"],
            "licence_url": r["license_url"],
            "source": r["source_page_url"],
            "verifie_le": r["verified_at"],
        }
    ajouter_gallica(index)

    INDEX.write_text(json.dumps(index, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{len(index)} entrées → {INDEX.name} ; {telecharges} nouvelles vignettes.")

    fusionner_dans_oeuvres(index)


def ajouter_gallica(index: dict) -> int:
    """Ajoute les estampes populaires trouvées sur Gallica (voir build_gallica.py).

    Ces images ne montrent PAS la feuille décrite par la notice : une planche
    d'Épinal a été tirée à des milliers d'exemplaires, le musée conserve le sien
    et la BnF le sien. `exemplaire_autre` porte cette réserve jusqu'à la légende,
    qui l'écrit sous l'image. Sans cette mention, on ferait passer un exemplaire
    pour un autre.
    """
    if not CORRESP_GALLICA.exists():
        return 0
    recs = json.loads(CORRESP_GALLICA.read_text(encoding="utf-8"))
    retenus = [r for r in recs if r.get("etat") == "exacte" and r.get("image_url")]
    if not retenus:
        return 0
    print(f"{len(retenus)} estampes retenues sur Gallica.")
    DOSSIER_IMG.mkdir(parents=True, exist_ok=True)
    ajoutees = 0
    for r in sorted(retenus, key=lambda x: x["reference_joconde"]):
        ref = r["reference_joconde"]
        # Une reproduction Commons, qui montre l'exemplaire même du musée quand
        # elle existe, l'emporte toujours sur un autre exemplaire.
        if ref in index:
            continue
        sortie = DOSSIER_IMG / f"{ref}.jpg"
        if not sortie.exists():
            try:
                optimiser(_get(r["image_url"]), sortie)
                ajoutees += 1
                if ajoutees % 10 == 0:
                    print(f"    {ajoutees} vignettes Gallica", flush=True)
                time.sleep(PAUSE)
            except Exception as ex:
                print(f"    ⚠ {ref} : {str(ex)[:80]}")
                continue
        index[ref] = {
            "statut": "open",
            "source_type": "gallica_bnf",
            "url": f"oeuvres/{ref}.jpg",
            "credit": "Bibliothèque nationale de France",
            "creator": "",
            "licence": "domaine public",
            "licence_url": "",
            "source": r["ark"],
            # La réserve, portée jusqu'à l'écran.
            "exemplaire_autre": True,
            "titre_source": r.get("titre_gallica", ""),
            "verifie_le": str(date.today()),
        }
    print(f"{ajoutees} nouvelles vignettes Gallica.")
    return ajoutees


def fusionner_dans_oeuvres(index: dict) -> int:
    """Attache `image` aux œuvres concernées dans chaque oeuvres/<slug>.json."""
    total = 0
    for chemin in glob.glob(str(DOSSIER_OEUVRES / "*.json")):
        d = json.load(open(chemin, encoding="utf-8"))
        change = False
        for o in d["oeuvres"]:
            img = index.get(o["reference"])
            if img and o.get("image") != img:
                o["image"] = img
                change = True
                total += 1
            elif not img and "image" in o:
                del o["image"]
                change = True
        if change:
            chemin_p = __import__("pathlib").Path(chemin)
            chemin_p.write_text(json.dumps(d, ensure_ascii=False, indent=1),
                                encoding="utf-8")
    print(f"{total} œuvres enrichies d'une image dans les fiches.")
    return total


if __name__ == "__main__":
    main()
