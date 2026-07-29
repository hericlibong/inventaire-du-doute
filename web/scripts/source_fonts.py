"""Récupère les polices de la charte en LOCAL (woff2), sans CDN.

Même esprit que source_portraits.py : reproductible, provenance claire. On
interroge l'API Google Fonts CSS2 (polices sous licence OFL), on télécharge les
woff2 dans web/static/fonts/, et on écrit un web/src/lib/styles/fonts.css qui
pointe vers ces fichiers LOCAUX (servis en /fonts/…). Aucun lien vers un CDN à
l'exécution du site.

Sous-ensembles conservés : latin + latin-ext (couvrent le français, dont « œ »,
« « » » »). Les autres (vietnamien, cyrillique, grec) sont ignorés.

Polices (ambiance « Catalogue savant », charte-graphique.md) :
- Fraunces  — titres, chiffres vedettes, verbatims (variable opsz+wght) ;
- Spectral  — texte éditorial (poids 400 et 600) ;
- Public Sans — UI, labels, données (variable wght).
"""

import re
import unicodedata
from pathlib import Path
from urllib.request import Request, urlopen

RACINE = Path(__file__).resolve().parent.parent  # web/
DOSSIER_FONTS = RACINE / "static" / "fonts"
FICHIER_CSS = RACINE / "src" / "lib" / "styles" / "fonts.css"

UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0 Safari/537.36")

# family (tel qu'attendu par l'API) → requête CSS2
FAMILLES = {
    "Fraunces": "Fraunces:opsz,wght@9..144,400..700",
    # Spectral en romain (400/600) + italique 400 (micro-légendes, mentions).
    "Spectral": "Spectral:ital,wght@0,400;0,600;1,400",
    "Public Sans": "Public+Sans:wght@400..700",
}
SOUS_ENSEMBLES = {"latin", "latin-ext"}


def slug(texte):
    t = unicodedata.normalize("NFKD", texte).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", t.lower()).strip("-")


def http_get(url, binaire=False):
    req = Request(url, headers={"User-Agent": UA})
    with urlopen(req, timeout=60) as r:
        return r.read() if binaire else r.read().decode("utf-8")


def main():
    DOSSIER_FONTS.mkdir(parents=True, exist_ok=True)
    blocs_css = [
        "/* Polices auto-hébergées — voir web/scripts/source_fonts.py et "
        "docs/charte-graphique.md. Fichiers dans static/fonts/, servis en /fonts/. "
        "Ne pas éditer à la main : régénérer par le script. */\n"
    ]
    telecharges = 0

    for famille, requete in FAMILLES.items():
        css = http_get(f"https://fonts.googleapis.com/css2?family={requete}&display=swap")
        # Chaque @font-face est précédé d'un commentaire /* sous-ensemble */.
        for sous_ens, bloc in re.findall(r"/\*\s*([\w-]+)\s*\*/\s*(@font-face\s*\{.*?\})", css, re.S):
            if sous_ens not in SOUS_ENSEMBLES:
                continue
            poids = re.search(r"font-weight:\s*([^;]+);", bloc).group(1).strip()
            style = re.search(r"font-style:\s*([^;]+);", bloc).group(1).strip()
            plage_uni = re.search(r"unicode-range:\s*([^;]+);", bloc).group(1).strip()
            url = re.search(r"src:\s*url\(([^)]+)\)", bloc).group(1).strip()

            poids_slug = "var" if " " in poids else poids
            style_slug = "i" if style == "italic" else ""
            nom = f"{slug(famille)}-{poids_slug}{style_slug}-{sous_ens}.woff2"
            (DOSSIER_FONTS / nom).write_bytes(http_get(url, binaire=True))
            telecharges += 1

            blocs_css.append(
                "@font-face {\n"
                f"\tfont-family: '{famille}';\n"
                f"\tfont-style: {style};\n"
                f"\tfont-weight: {poids};\n"
                "\tfont-display: swap;\n"
                f"\tsrc: url('/fonts/{nom}') format('woff2');\n"
                f"\tunicode-range: {plage_uni};\n"
                "}"
            )
        print(f"{famille} : ok")

    FICHIER_CSS.write_text("\n\n".join(blocs_css) + "\n", encoding="utf-8")
    print(f"\n{telecharges} fichiers woff2 → {DOSSIER_FONTS.relative_to(RACINE)}")
    print(f"CSS → {FICHIER_CSS.relative_to(RACINE)}")


if __name__ == "__main__":
    main()
