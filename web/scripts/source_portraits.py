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
import json, os, re, sys, time, unicodedata
import urllib.parse, urllib.request

UA = {'User-Agent': 'InventaireDuDoute/1.0 (portfolio data-journalisme; hericlibong@gmail.com)'}
ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(ICI)
DEST_IMG = os.path.join(RACINE, 'static', 'portraits')
# Le manifeste est un EXPORT VERSIONNÉ, pas un fichier de travail : `web/static/data`
# est ignoré par git, et les 27 images étaient versionnées sans leurs crédits — une
# licence perdue au premier clone (relevé le 2026-07-22). Il s'écrit donc dans
# data/exports/web/ et `npm run sync:data` le recopie vers static/data.
DEST_JSON = os.path.join(os.path.dirname(RACINE), 'data', 'exports', 'web', 'portraits.json')

# Maîtres dont le portrait regarde vers la DROITE : on le retourne
# horizontalement à l'affichage pour qu'il regarde son nuage (placé à gauche).
# Constaté à l'œil sur les fichiers (2026-07-09). Les gravures à texte (Le
# Primatice, François Clouet, Le Corrège) ne sont jamais dans cette liste : les
# retourner inverserait leur texte.
REGARD_DROITE = {
    'Annibale Carracci', 'Boucher', 'Guido Reni', 'Simon Vouet', 'Greuze',
    'Hyacinthe Rigaud', 'Fragonard', 'Ribera',
    # Lot du 2026-07-22, relu sur planche de contact : seuls ces deux visages sont
    # nettement tournés vers la droite. Les autres sont de face ou tournés à
    # gauche. Les gravures portant du texte (Antonio Tempesta, Federico Zuccaro,
    # Polidoro Caldara, Le Pérugin, Claude Lorrain) ne sont JAMAIS retournées —
    # cela inverserait leur inscription.
    'Adolph Menzel', 'Baccio Bandinelli',
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

    # Lot du 2026-07-22 (les 36 maîtres instruits au temps 5). QID obtenus par
    # recherche Wikidata puis VÉRIFIÉS par scripts/verifie_qid.py : le libellé, la
    # description, la qualité d'être humain (P31=Q5) et surtout les DATES doivent
    # concorder avec la ligne de repérage écrite dans editorial-maitres.js. Sept
    # divergences de dates relevées et documentées (docs/donnees.md, 2026-07-22).
    #
    # Trois maîtres n'ont PAS de portrait sur Wikidata (aucun P18) et n'y figurent
    # donc pas : Gaspard Dughet, Domenico Campagnola, Laurent de La Hyre. La fiche
    # affiche alors le repli « Pas de portrait fiable disponible » — on ne comble
    # pas un manque par une image approximative.
    "Le Guerchin": 'Q334262',
    "Bouchardon": 'Q987687',
    "Jules Romain": 'Q215305',
    "Ludovico Carracci": 'Q380553',
    "David Téniers": 'Q335022',
    "François Gérard": 'Q163543',
    "Le Parmesan": 'Q9348',
    "Perino del Vaga": 'Q918778',
    "Adolph Menzel": 'Q164961',
    "Baccio Bandinelli": 'Q358348',
    "Antonio Tempesta": 'Q605447',
    "Luca Giordano": 'Q332494',
    "Salvator Rosa": 'Q359421',
    "Federico Barocci": 'Q316731',
    "Carlo Maratti": 'Q538998',
    "Federico Zuccaro": 'Q345605',
    "Joseph Vernet": 'Q315819',
    "Luca Cambiaso": 'Q712512',
    "Polidoro Caldara": 'Q964822',
    "Corneille de Lyon": 'Q720941',
    "Francesco Vanni": 'Q960581',
    "Philippe de Champaigne": 'Q314814',
    "Giorgio Vasari": 'Q128027',
    "Sébastien Bourdon": 'Q553795',
    "Pier Francesco Mola": 'Q1192715',
    "Jean-Baptiste Oudry": 'Q737137',
    "Louis Léopold Boilly": 'Q715909',
    "Nicolas de Largillière": 'Q550302',
    "Paul Bril": 'Q540753',
    "Albrecht Dürer": 'Q5580',
    "Claude Lorrain": 'Q214074',
    "Le Pérugin": 'Q5827',
    "Botticelli": 'Q5669',

    # Lot du 2026-08-06 (les 39 artistes entrés au volume le 2026-08-02). QID
    # retenus en phase 2 : les dates de Wikidata doivent concorder avec celles
    # que les MUSÉES écrivent dans le champ auteur de Joconde (docs/donnees.md,
    # 2026-08-06). Neuf seulement ont un P18 qui soit réellement un portrait —
    # voir P18_NON_PORTRAIT juste dessous, qui explique les autres.
    "Charles Normand": 'Q2959914',
    "Giacinto Calandrucci": 'Q957255',
    "Georges Ferdinand Bigot": 'Q1135613',
    "Auguste Vacquerie": 'Q940439',
    "Turpin de Crissé": 'Q3216954',
    "Charles Hugo": 'Q663856',
    "Crispin de Passe l'Ancien": 'Q140096',
    "Antonio del Pollaiuolo": 'Q318640',
    "Jacques-Louis David": 'Q83155',
}

# ─────────────────────────────────────────────────────────────────────────────
# P18 N'EST PAS UNE PROMESSE DE PORTRAIT (constat du 2026-08-06)
#
# Sur l'élément Wikidata d'un artiste, la propriété P18 « image » porte souvent
# UNE DE SES ŒUVRES et non son visage. Le piège ne s'était pas vu sur les 63
# premiers maîtres, dont les portraits gravés sont célèbres ; il est apparu net
# sur ce lot. Quatre des treize candidats ont été écartés APRÈS AVOIR ÉTÉ
# REGARDÉS, planche de contact à l'appui — aucun indice textuel ne les
# départageait de façon sûre :
#
#   Colijn de Coter     P18 = « Coter Pruszcz Polyptych », un polyptyque
#   Louis Duthoit       P18 = la statue de saint Joseph de la cathédrale d'Amiens
#   Nicasius Bernaerts  P18 = « Bataille de chiens et de chats », une nature morte
#   Israël Henriet      P18 = l'inscription d'éditeur au bas d'une gravure de
#                             Stefano della Bella — pas même une figure
#
# Ces quatre-là gardent le repli « Pas de portrait fiable disponible ». Mettre
# une œuvre à la place d'un visage tromperait le lecteur sur ce qu'il regarde,
# et ce site ne montre que ce qu'il peut nommer.
#
# LA RÈGLE : aucun QID n'entre dans la table ci-dessus sans que son P18 ait été
# OUVERT ET REGARDÉ. Le contrôle est humain ; il n'est pas automatisable.
# ─────────────────────────────────────────────────────────────────────────────
P18_NON_PORTRAIT = {
    'Q1108307': 'Colijn de Coter — polyptyque',
    'Q19849909': 'Louis Duthoit — statue de la cathédrale d’Amiens',
    'Q7024540': 'Nicasius Bernaerts — nature morte',
    'Q3155663': 'Israël Henriet — inscription d’éditeur sur une gravure',
}


def get_json(url, essais=4):
    """Commons et Wikidata répondent HTTP 429 quand on va trop vite (rencontré le
    2026-08-06 en téléchargeant treize vignettes d'affilée). On patiente et on
    recommence plutôt que d'abandonner un portrait pour une question de cadence."""
    for i in range(essais):
        try:
            req = urllib.request.Request(url, headers=UA)
            return json.load(urllib.request.urlopen(req, timeout=30))
        except urllib.error.HTTPError as e:
            if e.code != 429 or i == essais - 1:
                raise
            time.sleep(5 * (i + 1))
        except Exception:
            if i == essais - 1:
                raise
            time.sleep(2 * (i + 1))


def slug(nom):
    s = unicodedata.normalize('NFKD', nom).encode('ascii', 'ignore').decode()
    return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')


# Enrobages anglais de Commons : ce ne sont pas des noms, mais des mentions de
# statut. Le crédit exigé par la licence garde le NOM ; le reste se dit en
# français, comme tout le site. « d'après » est ici au sens du crédit d'image
# (l'œuvre reproduite copie un modèle) — même mot que dans les notices Joconde.
ENROBAGES = [
    ('Unknown artist', 'auteur inconnu'),
    # Commons emploie les deux formes ; la seconde était passée en anglais dans
    # la légende de Georges Ferdinand Bigot (relevé le 2026-08-06).
    ('Unknown author', 'auteur inconnu'),
    ('unknown author', 'auteur inconnu'),
    ('Attributed to ', 'attribué à '),
    ('After ', "d'après "),
    ('Circle of ', 'entourage de '),
    ('Workshop of ', 'atelier de '),
]


def nettoie_auteur(txt):
    """Crédit d'auteur lisible : Commons répète parfois deux fois le même nom
    (« Unknown artistUnknown artist ») quand la fiche porte plusieurs éléments."""
    txt = (txt or '').strip()
    moitie = len(txt) // 2
    if len(txt) % 2 == 0 and txt[:moitie] == txt[moitie:]:
        txt = txt[:moitie]
    for anglais, francais in ENROBAGES:
        if anglais in txt:
            txt = txt.replace(anglais, francais)
    return txt.strip()


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
        'auteur': nettoie_auteur(champ('Artist')),
        'credit': champ('Credit'),
        'usage': champ('UsageTerms'),
    }


def main():
    os.makedirs(DEST_IMG, exist_ok=True)

    # Garde-fou : un QID dont on a constaté que le P18 n'est pas un portrait ne
    # doit pas revenir dans la table par inadvertance (2026-08-06).
    fautifs = {n: q for n, q in QID.items() if q in P18_NON_PORTRAIT}
    if fautifs:
        for n, q in fautifs.items():
            print(f'!! {n} ({q}) : {P18_NON_PORTRAIT[q]} — retirer de QID')
        raise SystemExit('P18 déjà constaté « pas un portrait » : voir ci-dessus.')

    # Reprise INCRÉMENTALE par défaut : on ne retélécharge pas les portraits déjà
    # au manifeste. Refaire les 60 pour en ajouter 9 coûte soixante requêtes,
    # déclenche les 429 et exposerait les portraits validés à un changement
    # survenu depuis sur Wikidata. `--tout` force la régénération complète.
    tout = '--tout' in sys.argv
    manifeste = {}
    if not tout and os.path.exists(DEST_JSON):
        with open(DEST_JSON, encoding='utf-8') as f:
            manifeste = json.load(f)
        print(f'manifeste existant : {len(manifeste)} portraits conservés '
              f'(--tout pour tout refaire)')

    a_faire = {n: q for n, q in QID.items() if tout or n not in manifeste}
    print(f'{len(a_faire)} portrait(s) à chercher\n')
    for nom, qid in a_faire.items():
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
