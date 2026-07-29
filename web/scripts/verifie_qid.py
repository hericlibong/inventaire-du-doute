#!/usr/bin/env python3
"""Vérifie les QID Wikidata des maîtres avant de sourcer leur portrait.

Contrôle croisé : pour chaque nom cherché, on affiche le libellé, la description,
les dates (P569/P570), le métier (P106) et la présence d'un portrait (P18). Les
dates servent de garde-fou — elles doivent concorder avec la ligne de repérage
écrite dans web/src/lib/editorial-maitres.js. Un QID dont les dates ne collent
pas est un mauvais QID (ou une bio à corriger).

Usage : python3 scripts/verifie_qid.py
"""
import json
import sys
import time
import urllib.parse
import urllib.request

UA = {'User-Agent': 'InventaireDuDoute/1.0 (portfolio data-journalisme; hericlibong@gmail.com)'}

# (nom d'affichage du projet, terme de recherche, dates attendues d'après la bio)
CHERCHE = [
    ('Le Guerchin', 'Guercino', '1591-1666'),
    ('Bouchardon', 'Edme Bouchardon', '1698-1762'),
    ('Jules Romain', 'Giulio Romano', '1499-1546'),
    ('Ludovico Carracci', 'Ludovico Carracci', '1555-1619'),
    ('David Téniers', 'David Teniers the Younger', '1610-1690'),
    ('François Gérard', 'François Gérard', '1770-1837'),
    ('Le Parmesan', 'Parmigianino', '1503-1540'),
    ('Perino del Vaga', 'Perino del Vaga', '1501-1547'),
    ('Adolph Menzel', 'Adolph Menzel', '1815-1905'),
    ('Baccio Bandinelli', 'Baccio Bandinelli', '1493-1560'),
    ('Antonio Tempesta', 'Antonio Tempesta', '1555-1630'),
    ('Luca Giordano', 'Luca Giordano', '1634-1705'),
    ('Salvator Rosa', 'Salvator Rosa', '1615-1673'),
    ('Federico Barocci', 'Federico Barocci', '1535-1612'),
    ('Carlo Maratti', 'Carlo Maratta', '1625-1713'),
    ('Federico Zuccaro', 'Federico Zuccari', '1540-1609'),
    ('Joseph Vernet', 'Claude Joseph Vernet', '1714-1789'),
    ('Luca Cambiaso', 'Luca Cambiaso', '1527-1585'),
    ('Polidoro Caldara', 'Polidoro da Caravaggio', '1495-1543'),
    ('Gaspard Dughet', 'Gaspard Dughet', '1615-1675'),
    ('Corneille de Lyon', 'Corneille de Lyon', '1510-1575'),
    ('Francesco Vanni', 'Francesco Vanni', '1565-1610'),
    ('Domenico Campagnola', 'Domenico Campagnola', '1500-1564'),
    ('Philippe de Champaigne', 'Philippe de Champaigne', '1602-1674'),
    ('Laurent de La Hyre', 'Laurent de La Hyre', '1606-1656'),
    ('Giorgio Vasari', 'Giorgio Vasari', '1511-1574'),
    ('Sébastien Bourdon', 'Sébastien Bourdon', '1616-1671'),
    ('Pier Francesco Mola', 'Pier Francesco Mola', '1612-1666'),
    ('Jean-Baptiste Oudry', 'Jean-Baptiste Oudry', '1686-1755'),
    ('Louis Léopold Boilly', 'Louis-Léopold Boilly', '1761-1845'),
    ('Nicolas de Largillière', 'Nicolas de Largillière', '1656-1746'),
    ('Paul Bril', 'Paul Bril', '1554-1626'),
    ('Albrecht Dürer', 'Albrecht Dürer', '1471-1528'),
    ('Claude Lorrain', 'Claude Lorrain', '1600-1682'),
    ('Le Pérugin', 'Pietro Perugino', '1450-1523'),
    ('Botticelli', 'Sandro Botticelli', '1445-1510'),
]


def get_json(url):
    return json.load(urllib.request.urlopen(
        urllib.request.Request(url, headers=UA), timeout=30))


def cherche(terme):
    u = ('https://www.wikidata.org/w/api.php?action=wbsearchentities&format=json'
         '&language=fr&uselang=fr&limit=3&search=' + urllib.parse.quote(terme))
    return [(r['id'], r.get('description', '')) for r in get_json(u).get('search', [])]


def fiche(qid):
    u = ('https://www.wikidata.org/w/api.php?action=wbgetentities&format=json'
         f'&ids={qid}&props=claims|labels&languages=fr')
    e = get_json(u)['entities'][qid]
    cl = e.get('claims', {})

    def annee(p):
        try:
            t = cl[p][0]['mainsnak']['datavalue']['value']['time']
            return t[1:5].lstrip('0') or t[1:5]
        except Exception:
            return '?'
    return {
        'label': e.get('labels', {}).get('fr', {}).get('value', ''),
        'naissance': annee('P569'),
        'mort': annee('P570'),
        'portrait': 'P18' in cl,
        'humain': any(s['mainsnak'].get('datavalue', {}).get('value', {}).get('id') == 'Q5'
                      for s in cl.get('P31', [])),
    }


def main():
    retenus, problemes = {}, []
    for nom, terme, dates_bio in CHERCHE:
        try:
            candidats = cherche(terme)
            if not candidats:
                problemes.append((nom, 'aucun résultat')); continue
            qid, desc = candidats[0]
            f = fiche(qid)
            attendu = tuple(dates_bio.split('-'))
            obtenu = (f['naissance'], f['mort'])
            concorde = obtenu == attendu
            drapeau = 'ok ' if (concorde and f['portrait'] and f['humain']) else '⚠  '
            print(f"{drapeau}{nom:24} {qid:10} {f['naissance']}–{f['mort']:5} "
                  f"bio {dates_bio:10} {'P18' if f['portrait'] else 'SANS PORTRAIT':14} "
                  f"{desc[:38]}")
            if not concorde:
                problemes.append((nom, f"dates : bio {dates_bio}, Wikidata "
                                       f"{f['naissance']}–{f['mort']}"))
            if f['portrait'] and f['humain']:
                retenus[nom] = qid
            time.sleep(0.3)
        except Exception as e:
            problemes.append((nom, str(e)))
    print(f"\n{len(retenus)}/{len(CHERCHE)} portraits disponibles")
    if problemes:
        print("\nÀ REGARDER :")
        for nom, quoi in problemes:
            print(f"  {nom:24} {quoi}")
    print("\nQID = " + json.dumps(retenus, ensure_ascii=False, indent=4))


if __name__ == '__main__':
    main()
