#!/usr/bin/env python3
"""Source les portraits des maîtres vedettes depuis Wikimedia Commons.

Route : Wikidata (propriété P18 « image ») -> fichier Commons -> API imageinfo
pour la licence + l'auteur, puis téléchargement LOCAL (pas de hotlink).

Rappel de statut (docs/decisions.md 2026-07-09) : ces portraits sont une SOURCE
SECONDAIRE D'ILLUSTRATION uniquement — jamais de donnée ni de comptage. Même
statut que le GeoJSON de la carte. Le crédit exigé par la licence (auteur +
licence) est conservé dans portraits.json et affiché dans la page.

Sortie :
  - static/portraits/<slug>.<ext>  (images ~480px de large)
  - static/data/portraits.json     (manifeste : crédit, licence, source, QID)
"""
import json, os, re, time, unicodedata
import urllib.parse, urllib.request

UA = {'User-Agent': 'InventaireDuDoute/1.0 (portfolio data-journalisme; hericlibong@gmail.com)'}
ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(ICI)
DEST_IMG = os.path.join(RACINE, 'static', 'portraits')
DEST_JSON = os.path.join(RACINE, 'static', 'data', 'portraits.json')

# Maîtres dont le portrait regarde vers la DROITE : on le retourne
# horizontalement à l'affichage pour qu'il regarde son nuage (placé à gauche).
# Constaté à l'œil sur les fichiers (2026-07-09). Les gravures à texte (Le
# Primatice, François Clouet, Le Corrège) ne sont jamais dans cette liste : les
# retourner inverserait leur texte.
REGARD_DROITE = {
    'Annibale Carracci', 'Boucher', 'Guido Reni', 'Simon Vouet', 'Greuze',
    'Hyacinthe Rigaud', 'Fragonard', 'Ribera',
}

# QID Wikidata vérifiés manuellement (recherche + description, 2026-07-09).
QID = {
    'Charles Le Brun': 'Q271676', 'Le Primatice': 'Q333366', 'Ingres': 'Q23380',
    'Rembrandt': 'Q5598', 'Michel-Ange': 'Q5592', 'Rubens': 'Q5599',
    'François Clouet': 'Q336747', 'Annibale Carracci': 'Q7824', 'Rodin': 'Q30755',
    'Boucher': 'Q180932', 'Andrea del Sarto': 'Q5571', 'Guido Reni': 'Q109061',
    'Léonard de Vinci': 'Q762', 'Le Tintoret': 'Q9319', 'Nicolas Poussin': 'Q41554',
    'Simon Vouet': 'Q317920', 'Greuze': 'Q347139', 'Van Dyck': 'Q150679',
    'Le Corrège': 'Q8457', 'Pierre Mignard': 'Q360010', 'Véronèse': 'Q9440',
    'Hyacinthe Rigaud': 'Q49898', 'Géricault': 'Q184212', 'Fragonard': 'Q127171',
    'Raphaël': 'Q5597', 'Ribera': 'Q297838', 'Titien': 'Q47551',
}


def get_json(url):
    return json.load(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30))


def slug(nom):
    s = unicodedata.normalize('NFKD', nom).encode('ascii', 'ignore').decode()
    return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')


def sans_html(txt):
    if not txt:
        return ''
    txt = re.sub(r'<[^>]+>', '', txt)
    return re.sub(r'\s+', ' ', txt).strip()


def image_p18(qid):
    u = f'https://www.wikidata.org/w/api.php?action=wbgetentities&ids={qid}&props=claims&format=json'
    claims = get_json(u)['entities'][qid]['claims']
    if 'P18' not in claims:
        return None
    return claims['P18'][0]['mainsnak']['datavalue']['value']  # nom de fichier Commons


def infos_commons(fichier, largeur=480):
    titre = 'File:' + fichier
    u = ('https://commons.wikimedia.org/w/api.php?action=query&format=json&prop=imageinfo'
         '&iiprop=extmetadata|url|mime&iiurlwidth=' + str(largeur)
         + '&titles=' + urllib.parse.quote(titre))
    pages = get_json(u)['query']['pages']
    page = next(iter(pages.values()))
    ii = page['imageinfo'][0]
    ex = ii.get('extmetadata', {})
    def champ(k):
        return sans_html(ex.get(k, {}).get('value', ''))
    return {
        'thumburl': ii.get('thumburl', ii['url']),
        'mime': ii.get('mime', ''),
        'descriptionurl': ii.get('descriptionurl', ''),
        'licence': champ('LicenseShortName'),
        'licence_url': ex.get('LicenseUrl', {}).get('value', ''),
        'auteur': champ('Artist'),
        'credit': champ('Credit'),
        'usage': champ('UsageTerms'),
    }


def main():
    os.makedirs(DEST_IMG, exist_ok=True)
    manifeste = {}
    for nom, qid in QID.items():
        try:
            fichier = image_p18(qid)
            if not fichier:
                print(f'!! {nom}: pas de P18'); continue
            info = infos_commons(fichier)
            ext = {'image/jpeg': 'jpg', 'image/png': 'png'}.get(info['mime'], 'jpg')
            nom_fichier = f'{slug(nom)}.{ext}'
            with urllib.request.urlopen(urllib.request.Request(info['thumburl'], headers=UA), timeout=60) as r:
                data = r.read()
            with open(os.path.join(DEST_IMG, nom_fichier), 'wb') as f:
                f.write(data)
            manifeste[nom] = {
                'fichier': f'/portraits/{nom_fichier}',
                'auteur': info['auteur'] or 'Auteur non précisé sur Commons',
                'licence': info['licence'] or 'voir la page du fichier',
                'licence_url': info['licence_url'],
                'source': info['descriptionurl'],
                'wikidata': f'https://www.wikidata.org/wiki/{qid}',
                # 'droite' => retourné à l'affichage pour regarder le nuage (à gauche).
                'regard': 'droite' if nom in REGARD_DROITE else 'gauche',
            }
            print(f'ok {nom}: {nom_fichier}  [{info["licence"]}]  {info["auteur"][:50]}')
            time.sleep(0.4)
        except Exception as e:
            print(f'!! {nom} ({qid}): {e}')
    with open(DEST_JSON, 'w', encoding='utf-8') as f:
        json.dump(manifeste, f, ensure_ascii=False, indent=2)
    print(f'\n{len(manifeste)}/{len(QID)} portraits -> {DEST_JSON}')


if __name__ == '__main__':
    main()
