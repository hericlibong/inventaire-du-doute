"""Export « Les presque » : le doute par maître de référence (phase 3).

Produit data/exports/web/artistes.json : pour chaque maître de la liste vedette
V1 (docs/decisions.md, 2026-07-07), la répartition des notices qui portent son
nom dans le champ Auteur — attribution ferme (« propre »), doute (ventilé par
famille et par niveau), et copie assumée (« d'après », catégorie à part) — plus
le nombre de musées et quelques notices réelles (liens POP).

Critère de la liste : maître de référence ET ≥ 20 notices de doute (hors copie),
lexique aligné sur markers.py (famille_segment).

Unité de comptage : la RÉFÉRENCE Joconde, pas le segment d'auteur (decisions.md,
2026-07-21 quater). Une notice qui nomme le maître deux fois sous deux graphies
— « VECELLIO Tiziano (attribué à) ; LE TITIEN (dit, attribué à) » — ne pesait
qu'une fois pour le public mais deux fois dans le comptage. Chaque référence est
donc résolue en UNE catégorie et UNE famille avant d'être ajoutée.

Désambiguïsation (docs/donnees.md, 2026-07-07) : chaque maître est défini par
des motifs INCLUS et EXCLUS sur le nom-pivot (parenthèses retirées, accents et
casse normalisés) pour écarter homonymes (Rembrandt ≠ R. Bugatti), familles
(Fragonard père ≠ fils) et fusionner les variantes de graphie (Le Primatice =
Primaticcio, Le Titien = Vecellio Tiziano).

Usage : uv run python src/build_artistes.py  (~2 min)
"""

import json
import re
import unicodedata
from collections import Counter, defaultdict
from datetime import datetime, timezone

import pandas as pd

import markers
from config import CHEMIN_CSV, DOSSIER_EXPORTS, URL_CSV

DOSSIER_WEB = DOSSIER_EXPORTS / "web"
DOSSIER_OEUVRES = DOSSIER_WEB / "oeuvres"
TAILLE_MORCEAU = 200_000
# artistes.json reste l'export LÉGER (répertoire + profils). Depuis le 2026-07-28,
# l'onglet « Œuvres » ne montre plus quelques exemples mais la TOTALITÉ des œuvres
# concernées par maître : elles ne peuvent pas tenir dans artistes.json (elles y
# pèseraient plus que tout le reste). Chaque maître reçoit donc un fichier à part,
# oeuvres/<slug>.json, chargé à la demande par le front (decisions.md, 2026-07-28).
# La liste par maître est l'ordre de RENCONTRE dans le CSV — comme les anciens
# exemples, elle n'est pas choisie à la main (règle methode-et-limites.md) ; le
# front la regroupe par famille pour l'affichage.

# Niveau de chaque famille de doute (échelle typologie P2-T2).
NIVEAU_FAMILLE = {
    "attribue": 1, "point_interrogation": 1, "presume": 1,
    "ecole_de": 2, "atelier_de": 2, "entourage_de": 2, "suiveur_de": 2,
    "maniere_de": 3, "genre_de": 3,
}

COLONNES = ["Reference", "Auteur", "Domaine", "Code_Museofile",
            "Nom_officiel_musee", "Ville", "Titre", "coordonnees"]

# Liste vedette V1. Chaque maître : (motifs inclus, motifs exclus) sur le pivot
# normalisé. Ordonnée par doute décroissant (mesuré 2026-07-07). Les deux
# familles écartées après désambiguïsation (Bruegel l'Ancien, Cranach l'Ancien,
# < 20 une fois le maître isolé) NE figurent pas ici — voir docs/decisions.md.
#
# TABLE RELUE À L'ŒIL (2026-07-21, temps 2) à partir de l'inventaire des 246
# formes d'auteur réellement captées, mentions prudentes ET certaines. Deux
# outils, pas un de plus : l'ancre « ^ » (le nom doit être en tête, voir
# _mot_entier) et l'exclusion nommée. Chaque exclusion dit QUI elle écarte :
# c'est cette liste qui sera publiée avec la page méthode.
MAITRES = [
    ("Charles Le Brun",     ["LE BRUN CHARLES"], []),
    ("Le Primatice",        ["PRIMATICCIO", "PRIMATICE"], []),
    # « MADAME INGRES » est écartée par l'ancre ; Jean Marie Joseph Ingres est
    # un autre homme.
    ("Ingres",              ["^INGRES"], ["JEAN MARIE JOSEPH"]),
    ("Rembrandt",           ["REMBRANDT"], ["BUGATTI"]),
    # L'ancre suffit à écarter les 16 homonymes qui portent Michelangelo ou
    # Michel-Ange en PRÉNOM : Corneille Michel-Ange (422 mentions certaines !),
    # Cerquozzi, Merisi dit Le Caravage, Pace, Anselmi, Pistoletto, Challe,
    # Slodtz, Campidoglio, Membrini, Aliprandi, Unterperger, Yrazazbal,
    # Ricciolini, Pollet. Aucune exclusion nommée n'est nécessaire.
    ("Michel-Ange",         ["^BUONARROTI", "^BUONAROTTI", "^MICHEL-ANGE"], []),
    # Arnold Frans Rubens et le « Rubens des batailles » (Snayers) ne sont pas lui.
    ("Rubens",              ["RUBENS"], ["ARNOLD", "BATAILLES"]),
    ("François Clouet",     ["CLOUET FRANCOIS"], []),
    ("Annibale Carracci",   ["CARRACCI ANNIBALE"], []),
    ("Rodin",               ["RODIN AUGUSTE"], []),
    ("Boucher",             ["BOUCHER FRANCOIS"], []),
    ("Andrea del Sarto",    ["SARTO ANDREA", "ANDREA DEL SARTO"], []),
    ("Guido Reni",          ["RENI GUIDO"], []),
    # Pierino da Vinci (le neveu sculpteur) et Marguerite Vinci écartés.
    ("Léonard de Vinci",    ["^VINCI", "^LEONARD DE VINCI", "^DE VINCI",
                             "^LEONARDO DA VINCI", "^LEONARDO DI SER PIERO"],
                            ["PIERINO", "MARGUERITE"]),
    # Domenico Robusti est le fils de Jacopo.
    ("Le Tintoret",         ["TINTORET", "^ROBUSTI"], ["DOMENICO"]),
    # L'ancre écarte Lemaire-Poussin, Lavallée-Poussin, Gaspard Poussin (Dughet)
    # et Le Guaspre ; reste Poussin-Heydeck, qui commence bien par Poussin.
    ("Nicolas Poussin",     ["^POUSSIN"], ["HEYDECK"]),
    # Aubin et Ferdinand Vouet sont écartés par la précision du motif.
    ("Simon Vouet",         ["VOUET SIMON"], []),
    ("Greuze",              ["GREUZE"], []),
    # Philip van Dyck, Philippe et Pierre Van Dyck ne sont pas Antoon.
    ("Van Dyck",            ["DYCK"], ["PHILIP", "PHILIPPE", "PIERRE"]),
    ("Le Corrège",          ["CORREGE", "ALLEGRI ANTONIO"], []),
    # Pierre Mignard II, le neveu.
    ("Pierre Mignard",      ["MIGNARD PIERRE"], ["PIERRE II"]),
    # Le fils Carlo, le frère Benedetto, le neveu Gabriele ; Bonifazio de'
    # Pitati et Zenone da Verona portent « Veronese » comme surnom de ville.
    ("Véronèse",            ["^VERONESE", "^CALIARI"],
                            ["CARLO", "BENEDETTO", "GABRIELE",
                             "BONIFAZIO", "BONIFACIO"]),
    # « Rigau y Ros », sa forme catalane, accompagne presque toujours « Rigaud »
    # sur la même notice (132 fois sur 134) : l'alias ne rattrape que 2 notices,
    # mais la table doit dire les noms qu'elle connaît (relevé au temps 4).
    ("Hyacinthe Rigaud",    ["RIGAUD HYACINTHE", "^RIGAU Y ROS"], []),
    ("Géricault",           ["GERICAULT"], []),
    ("Fragonard",           ["FRAGONARD JEAN-HONORE", "FRAGONARD JEAN HONORE"], []),
    # Le cas le plus pollué : 59 formes captées, « Raphaël » servant de prénom à
    # une cinquantaine de personnes (Lonne, Lardeur, Mengs, Collin, Sadeler,
    # Freida…). L'ancre les écarte toutes ; restent l'affichiste Raphael Tuck,
    # le graveur Raphael-Schwartz, et Giovanni Santi, le père.
    # L'ancre remplace aussi l'ancienne exclusion « ATELIER », qui servait à
    # écarter les noms d'atelier (« ATELIER DE RAPHAEL ») : ils ne commencent
    # pas par le nom du maître. Et « SANTI Raffaello », sa forme d'état civil,
    # n'était captée par aucun motif — un faux négatif au sein même des 27.
    ("Raphaël",             ["^RAPHAEL", "^SANZIO", "^SANTI RAFFAELLO",
                             "^RAFFAELLO"], ["TUCK", "SCHWARTZ", "GIOVANNI"]),
    # Roman Ribera y Cirera et Pierre Ribera.
    ("Ribera",              ["RIBERA"], ["CIRERA", "PIERRE"]),
    # Francesco et Cesare Vecellio sont de la famille, pas Tiziano ; Tiziano
    # Aspetti est écarté faute de motif sur le seul prénom.
    ("Titien",              ["LE TITIEN", "^VECELLIO"], ["FRANCESCO", "CESARE"]),

    # -- LOT DU 2026-07-22 (temps 5) : 36 candidats instruits un par un à partir
    # du registre des 330 formes au seuil de 10 (candidats_maitres.csv). Chacun
    # a été vérifié : identité claire, ≥ 10 références prudentes UNIQUES après
    # regroupement des graphies, homonymes et parents séparés nommément. Le
    # comptage par personne, les statuts et les motifs écartés : docs/donnees.md
    # et data/exports/maitres_instruits.csv. L'ordre ici est indicatif ; la
    # sortie retrie par doute.
    #
    # Giovanni Francesco Barbieri, dit Le Guerchin / Guercino (toutes graphies).
    ("Le Guerchin",         ["^BARBIERI GIOVANNI", "GUERCHIN", "GUERCINO"], []),
    # Edme Bouchardon seul : ses frères Jacques-Philippe et Jean-Baptiste écartés.
    ("Bouchardon",          ["BOUCHARDON EDME"], []),
    # Giulio Pippi, dit Jules Romain / Giulio Romano ; Jules-Romain Joyant écarté.
    ("Jules Romain",        ["^PIPPI GIULIO", "ROMAIN JULES", "JULES ROMAIN",
                             "GIULIO ROMANO"], ["JOYANT"]),
    # Le frère d'Annibale ; « CARRACCI l'un des » (mention collective) reste dehors.
    ("Ludovico Carracci",   ["CARRACCI LUDOVICO", "CARRACCI LODOVICO"], []),
    # David Téniers le Jeune (David II) : le père (le Vieux, Ier) et le frère
    # Abraham écartés. Les « TENIERS David » sans suffixe valent le Jeune par
    # convention Joconde (peinture de genre) — ambiguïté résiduelle documentée.
    ("David Téniers",       ["TENIERS DAVID", "TENIERS LE JEUNE"],
                            ["IER", "VIEUX", "ABRAHAM"]),
    # François, baron Gérard : l'ancre écarte les « X Gérard François ».
    ("François Gérard",     ["^GERARD FRANCOIS"], []),
    # Francesco Mazzuola/Mazzola, dit Le Parmesan / il Parmigianino.
    ("Le Parmesan",         ["MAZZUOLA FRANCESCO", "MAZZOLA FRANCESCO",
                             "PARMESAN", "PARMIGIANINO"], []),
    # Piero Bonaccorsi, dit Perino del Vaga.
    ("Perino del Vaga",     ["BONACCORSI PIERO", "PERINO DEL VAGA",
                             "PERIN DEL VAGA"], []),
    ("Adolph Menzel",       ["MENZEL ADOLPH", "MENZEL ADOLF"], []),
    # Baccio seul : Bartolommeo et Clemente Bandinelli écartés par la précision.
    ("Baccio Bandinelli",   ["BANDINELLI BACCIO"], []),
    # Antonio seul : Pieter Mulier dit « Cavalier Tempesta » n'est pas rattaché.
    ("Antonio Tempesta",    ["TEMPESTA ANTONIO"], []),
    ("Luca Giordano",       ["GIORDANO LUCA"], []),
    ("Salvator Rosa",       ["ROSA SALVATOR", "ROSA SALVATORE"], []),
    # Federico seul : son frère Ambrogio et le graveur Francesco Barocci écartés.
    ("Federico Barocci",    ["BAROCCI FEDERICO", "BAROCCIO FEDERICO",
                             "ZUCCARI FEDERICO"], ["AMBROGIO", "FRANCESCO"]),
    ("Carlo Maratti",       ["MARATTI", "MARATTA"], []),
    # Federico seul : son frère Taddeo Zuccaro (52 mentions certaines) écarté.
    ("Federico Zuccaro",    ["ZUCCARO FEDERICO", "ZUCCARI FEDERICO"], []),
    # Claude-Joseph Vernet : la dynastie (Carle, Horace) reste dehors, le motif
    # exige « Joseph ».
    ("Joseph Vernet",       ["VERNET JOSEPH", "VERNET CLAUDE JOSEPH"], []),
    # Luca seul : son fils Orazio Cambiaso écarté.
    ("Luca Cambiaso",       ["CAMBIASO LUCA"], []),
    # Polidoro Caldara, dit Polidoro da Caravaggio.
    ("Polidoro Caldara",    ["CALDARA POLIDORO", "POLIDORO DA CARAVAGGIO"], []),
    # Gaspard Dughet, dit Gaspard Poussin / Le Guaspre (beau-frère de Nicolas ;
    # « GASPARD POUSSIN » ne commence pas par Poussin, aucune collision).
    ("Gaspard Dughet",      ["DUGHET", "GASPARD POUSSIN", "GUASPRE", "GASPRE"], []),
    # Corneille de La Haye, dit Corneille de Lyon (distinct de Corneille
    # Michel-Ange, écarté des 27 par l'ancre).
    ("Corneille de Lyon",   ["CORNEILLE DE LYON"], []),
    # Francesco seul : « VANNI » sans prénom vaut plusieurs peintres siennois.
    ("Francesco Vanni",     ["VANNI FRANCESCO"], []),
    # Domenico seul : son frère Giulio Campagnola écarté.
    ("Domenico Campagnola", ["CAMPAGNOLA DOMENICO"], []),
    # Philippe seul : son neveu Jean-Baptiste de Champaigne (8 mentions
    # prudentes, sous le seuil) écarté nommément.
    ("Philippe de Champaigne", ["^CHAMPAIGNE"], ["JEAN-BAPTISTE", "JEAN BAPTISTE"]),
    # Laurent seul : Philippe (fils astronome) et Louis de La Hyre écartés.
    ("Laurent de La Hyre",  ["LA HYRE LAURENT"], []),
    ("Giorgio Vasari",      ["VASARI GIORGIO"], []),
    ("Sébastien Bourdon",   ["BOURDON SEBASTIEN"], []),
    ("Pier Francesco Mola", ["MOLA PIER FRANCESCO", "MOLA PIERRE FRANCOIS"], []),
    # Jean-Baptiste seul : son fils Jacques et Gustave Oudry écartés.
    ("Jean-Baptiste Oudry", ["OUDRY JEAN-BAPTISTE"], []),
    # Louis Léopold seul : ses fils Jules/Julien et Alphonse Boilly écartés par
    # la précision du motif (« BOILLY LOUIS » ne prend qu'eux).
    ("Louis Léopold Boilly", ["BOILLY LOUIS"], []),
    ("Nicolas de Largillière", ["LARGILLIERE"], []),
    ("Paul Bril",           ["BRIL PAUL", "BRIL PAULUS"], []),
    # Albrecht seul : son frère Hans Dürer écarté.
    ("Albrecht Dürer",      ["DURER ALBRECHT"], []),
    # Claude Gellée, dit Le Lorrain (le motif exige « Claude » : Robert Le
    # Lorrain, sculpteur, reste dehors).
    ("Claude Lorrain",      ["LORRAIN CLAUDE", "GELLEE"], []),
    # Pietro Vannucci, dit Le Pérugin.
    ("Le Pérugin",          ["VANNUCCI PIETRO", "PERUGIN"], []),
    # Alessandro Filipepi, dit Sandro Botticelli.
    ("Botticelli",          ["BOTTICELLI", "FILIPEPI"], []),

    # -- LOT 2 DU 2026-08-02 : 40 personnes retenues sur les 50 formes du registre
    # qui portaient au moins 25 notices prudentes et restaient « à instruire ».
    # Instruction par notices décroissantes, jamais par notoriété. Le test
    # d'identité tient en trois questions, toutes tranchées sur la source :
    #   1. le musée écrit-il un prénom entier (ni initiale, ni « Père », ni nom nu) ?
    #   2. un homonyme porte-t-il des notices prudentes sous une graphie que les
    #      motifs prendraient ?
    #   3. les graphies rapprochées portent-elles les mêmes dates de vie ?
    # Les dix formes écartées et leur motif : registre_maitres.py (ÉCARTÉS
    # INSTRUITS) et docs/donnees.md, 2026-08-02.
    #
    # Jean-Baptiste Barla est instruit et identifié, mais il est HORS PÉRIMÈTRE de
    # ce volume — voir HORS_PERIMETRE, plus bas.
    ("Alexandre Clausel",   ["CLAUSEL ALEXANDRE"], []),
    # Charles Pierre Joseph Normand : les autres Normand de la base (Achille,
    # Augustin, Michel, Charles Victor) ne portent aucune notice prudente et le
    # motif complet ne les prend pas.
    ("Charles Normand",     ["NORMAND CHARLES PIERRE JOSEPH"], []),
    ("Léon Tirode",         ["TIRODE LEON"], []),
    ("Louis Morinet",       ["MORINET LOUIS GEORGES ALBERT"], []),
    # Giacinto seul : Giovanni Battista Calandrucci écarté par la précision.
    ("Giacinto Calandrucci", ["CALANDRUCCI GIACINTO"], []),
    ("Georges Ferdinand Bigot", ["BIGOT GEORGES-FERDINAND",
                                 "BIGOT GEORGES FERDINAND"], []),
    # Léon Fort : Siméon Fort et Louis Fort sont d'autres hommes, sans notice
    # prudente ; « FORT-VOUILLON » est une manufacture.
    ("Léon Fort",           ["FORT LEON"], []),
    # Les frères Duthoit, d'Amiens : le musée écrit leurs dates (Louis 1807-1874,
    # Aimé 1803-1869) et les nomme ENSEMBLE sur 93 de leurs notices — l'hésitation
    # porte sur lequel des deux. Deux personnes, deux profils, une part commune
    # que l'union des notices ne compte qu'une fois.
    ("Louis Duthoit",       ["DUTHOIT LOUIS"], []),
    ("Aimé Duthoit",        ["DUTHOIT AIME"], []),
    # « PINOT Charles François » et « PINOT Charles » portent les mêmes dates
    # (1817-1874) et ne partagent aucune notice : deux graphies d'un seul imagier.
    # L'imagerie « Pinot & Sagaire » est une raison sociale, laissée dehors.
    ("Charles François Pinot", ["PINOT CHARLES"], []),
    ("André Marie Florentin Giraud", ["GIRAUD ANDRE MARIE FLORENTIN",
                                      "GIRAUD MARIE ANDRE FLORENTIN"], []),
    ("Auguste Vacquerie",   ["VACQUERIE AUGUSTE"], []),
    ("François Georgin",    ["GEORGIN FRANCOIS"], []),
    ("Louis Verjat",        ["VERJAT LOUIS VICTOR EMILE"], []),
    # Peter Hawke : John Hawke n'est pas lui.
    ("Peter Hawke",         ["HAWKE PETER"], []),
    # Auguste seul : Ludovic Alleaume, son frère, est écarté par la précision.
    ("Auguste Alleaume",    ["ALLEAUME AUGUSTE"], []),
    ("Antoine Gabriel Willermet", ["WILLERMET ANTOINE GABRIEL"], []),
    # Le fils, Lancelot-Théodore (1782-1859). Le père, que le musée n'appelle que
    # « TURPIN DE CRISSE Père », reste dehors : son identité n'est pas écrite, et
    # 34 de ses 35 notices nomment déjà le fils.
    ("Turpin de Crissé",    ["TURPIN DE CRISSE LANCELOT THEODORE",
                             "TURPIN DE CRISSE LANCELOT-THEODORE"],
                            ["HENRI ROLAND"]),
    # Le fils de Victor Hugo, photographe à Jersey ; le père (2 504 mentions
    # certaines) et Georges Victor Hugo sont écartés par la précision du motif.
    ("Charles Hugo",        ["HUGO CHARLES"], []),
    ("Gustave Lancelot",    ["LANCELOT GUSTAVE"], []),
    ("Charles du Ry",       ["RY CHARLES DU"], []),
    ("Odilon Roche",        ["ROCHE ODILON"], []),
    # Frans Hogenberg, sous ses trois graphies ; Nicolas, Abraham et Remigius
    # Hogenberg sont d'autres graveurs de la famille.
    ("Frans Hogenberg",     ["HOGENBERG FRANCOIS", "HOGENBERG FRANS",
                             "HOGENBERG FRANZ"], []),
    # « Charles Eugène », « Eugène » et « Charles » Ensfelder portent les mêmes
    # dates (1836-1876) et ne partagent aucune notice : un seul dessinateur.
    ("Charles Eugène Ensfelder", ["ENSFELDER"], []),
    # Nicolaus seul : Martin Hoffmann est un autre homme, avec ses propres notices.
    ("Nicolaus Hoffmann",   ["HOFFMANN NICOLAUS"], []),
    ("Nicasius Bernaerts",  ["BERNAERTS NICASIUS"], []),
    # Les deux Crispin de Passe, le père et le fils, distingués par le chiffre
    # que Joconde écrit après le prénom. Comme les Duthoit, ils sont nommés
    # ensemble sur 28 notices : le musée hésite entre les deux générations.
    ("Crispin de Passe l'Ancien", ["PASSE CRISPIN I VAN DE",
                                   "VAN DE PASSE CRISPIN I"], []),
    ("Crispin de Passe le Jeune", ["PASSE CRISPIN II VAN DE",
                                   "VAN DE PASSE CRISPIN II"], []),
    ("Amable Louis Crapelet", ["CRAPELET AMABLE LOUIS",
                               "CRAPELET LOUIS AMABLE"], []),
    ("Auguste Beuret",      ["BEURET AUGUSTE"], []),
    ("Jean-Charles François Leloy", ["LELOY JEAN CHARLES FRANCOIS",
                                     "LELOY JEAN-CHARLES-FRANCOIS"], []),
    ("Joseph Hussenot",     ["HUSSENOT JOSEPH"], []),
    # Antonio seul : son frère Piero del Pollaiuolo est écarté par la précision.
    ("Antonio del Pollaiuolo", ["POLLAIUOLO ANTONIO"], []),
    ("Henry Hennault",      ["HENNAULT HENRY"], []),
    ("Israël Henriet",      ["HENRIET ISRAEL", "ISRAEL HENRIET"], []),
    # René Ackermann : Rudolf, Charles et Johann Adam Ackermann sont d'autres
    # hommes ; « Ackermann & Co » est une raison sociale.
    ("René Ackermann",      ["ACKERMANN RENE"], []),
    ("Louis Hertig",        ["HERTIG LOUIS"], []),
    ("Colijn de Coter",     ["COLYN DE COTER", "COTER COLIJN DE",
                             "DE COTER COLIJN"], []),
    # Jacques-Louis David. Ses notices prudentes portent toutes « David
    # (1748-1825) », donc le pivot « DAVID » nu : seule l'égalité stricte le prend
    # sans ramasser David d'Angers, Gérard David ou Jérôme David. Ambiguïté
    # résiduelle assumée et documentée : « David (éditeur) », une trentaine de
    # mentions CERTAINES, tombe aussi dans le motif — aucune notice prudente.
    ("Jacques-Louis David", ["=DAVID", "DAVID JACQUES-LOUIS",
                             "DAVID JACQUES LOUIS", "DAVID JACQUE-LOUIS"], []),
]

# Personnes instruites, identifiées, correctement comptées — et HORS PÉRIMÈTRE du
# volume 1 (décision utilisateur, 2026-08-02).
#
# Ce ne sont PAS des faux positifs, et il faut le dire à chaque fois qu'on en
# parle : l'identité est établie, le comptage est juste, les notices restent dans
# les statistiques nationales (24 507), qui ne dépendent pas de cette table. Elles
# sortent du volume parce que leur fonds n'entre pas dans son angle éditorial —
# les attributions artistiques.
#
# La quatrième valeur est le motif. Il est publiable tel quel, comme les motifs
# d'écart : une sortie de périmètre non motivée serait une sélection opaque.
HORS_PERIMETRE = [
    ("Jean-Baptiste Barla", ["BARLA JEAN-BAPTISTE"], [],
     "fonds botanique sériel, concentré dans un seul musée, hors de l'angle "
     "éditorial du volume consacré aux attributions artistiques"),
]

# Toutes les personnes instruites, périmètre compris ou non. Sert au registre,
# qui doit prouver que Barla a bien été identifié et compté — jamais aux exports
# du volume, qui ne connaissent que MAITRES.
TOUTES_PERSONNES = MAITRES + [(n, i, e) for n, i, e, _ in HORS_PERIMETRE]
MOTIF_HORS_PERIMETRE = {n: m for n, _i, _e, m in HORS_PERIMETRE}

LIBELLES_NIVEAUX = {1: "Presque lui", 2: "Autour de lui", 3: "Son style, sans lui"}
LIBELLE_FAMILLE = {f.code: f.libelle for f in markers.FAMILLES}


def _sans_accents(chaine: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", chaine)
                   if unicodedata.category(c) != "Mn")


def _pivot(segment: str) -> str:
    """Nom-pivot : parenthèses retirées, espaces compactés, accents/casse ôtés."""
    sans_paren = markers._RE_PARENTHESES.sub("", segment)
    return _sans_accents(re.sub(r"\s+", " ", sans_paren).strip(" ,;").upper())


def _slug(nom: str) -> str:
    """Identifiant stable d'un maître pour nommer son fichier d'œuvres :
    « Charles Le Brun » → « charles-le-brun », « Léonard de Vinci » →
    « leonard-de-vinci ». Sans accents, minuscules, tout ce qui n'est pas
    lettre ou chiffre devient un tiret. Les noms des maîtres sont distincts et
    le restent après slugification (vérifié par une assertion à l'export)."""
    base = _sans_accents(nom).lower()
    return re.sub(r"[^a-z0-9]+", "-", base).strip("-")


def _mot_entier(motif: str, pivot: str) -> bool:
    """Le motif apparaît-il comme MOT ENTIER dans le pivot ? On a longtemps testé
    par simple sous-chaîne (`motif in pivot`), ce qui rattachait à tort des noms
    différents partageant une racine : « SERODINE » → Rodin, « VINCIDOR » → Vinci,
    « SOLDYCK » → Van Dyck, « RIBERAT » → Ribera, « TINTORETTO Domenico » (le fils)
    → Le Tintoret (decisions.md / donnees.md, 2026-07-13). Le test mot entier lève
    l'ambiguïté ; les vraies notices restent prises (« Le Tintoret ou il Tintoretto »
    contient bien le mot « Tintoret »). Frontières de mot sur le pivot déjà
    normalisé (majuscules, sans accents).

    Un motif préfixé de « ^ » ne vaut qu'en TÊTE du nom. Joconde écrit l'auteur
    « NOM Prénom » : sans cette ancre, « Raphaël » se rattache à Raphaël Collin ou
    Anton Raphael Mengs, et « Michel-Ange » à Corneille Michel-Ange
    (donnees.md, 2026-07-21). L'ancre n'est posée que là où elle est nécessaire :
    « ÉCOLE DE PRIMATICCIO » doit rester pris, le nom n'y est pas en tête.

    Un motif préfixé de « = » exige le nom TOUT ENTIER, rien de plus (lot 2,
    2026-08-02). Il ne sert qu'à un cas, mais un cas qu'aucun autre outil ne
    résout : Jacques-Louis David signe ses notices « David (1748-1825) », soit
    le pivot « DAVID » tout court. L'ancre ne suffit pas — elle prendrait aussi
    David d'Angers, Gérard David, Jérôme David et une soixantaine d'autres, et
    il faudrait les nommer un par un pour les écarter. L'égalité stricte prend
    le nom nu et lui seul. Les dates, qui distingueraient les homonymes, sont
    entre parenthèses : la normalisation les a déjà retirées."""
    if motif.startswith("="):
        return pivot == motif[1:]
    if motif.startswith("^"):
        return re.match(rf"{re.escape(motif[1:])}\b", pivot) is not None
    return re.search(rf"\b{re.escape(motif)}\b", pivot) is not None


def _trouve_maitre(pivot: str, table=None):
    """Le nom de la personne que désigne ce pivot, ou None.

    `table` vaut MAITRES par défaut — les personnes DU VOLUME. Le registre passe
    TOUTES_PERSONNES pour retrouver aussi celles qui sont hors périmètre : il doit
    prouver qu'elles ont été identifiées et comptées, pas les faire disparaître.
    """
    for nom, inclus, exclus in (MAITRES if table is None else table):
        if any(_mot_entier(e, pivot) for e in exclus):
            continue
        if any(_mot_entier(i, pivot) for i in inclus):
            return nom
    return None


def _categorie_retenue(categories: set) -> str | None:
    """Une même référence peut nommer le maître plusieurs fois, avec des liens
    différents (« POUSSIN Nicolas (attribué à) ; POUSSIN Nicolas »). Elle ne
    compte qu'UNE fois, et du côté le plus prudent : le doute l'emporte sur la
    copie, la copie sur l'attribution ferme. C'est ce qui rend propre / doute /
    copie réellement disjoints, donc additionnables (decisions.md, 2026-07-21).
    Les segments écartés (atelier hors beaux-arts, école-lieu) ne comptent pas."""
    for categorie in ("doute", "copie", "propre"):
        if categorie in categories:
            return categorie
    return None


def _famille_retenue(familles: dict) -> str:
    """Même chose au grain de la famille : trois références de Simon Vouet
    (M0332004170 à 172) portent à la fois « VOUET Simon (?) » et « VOUET Simon
    (atelier, dessinateur) ». Le « ? » l'emporte — c'est le marqueur de doute le
    plus explicite — puis l'ordre canonique des familles. Une référence = une
    famille : les familles et les niveaux totalisent exactement le doute
    (arbitrage utilisateur, option c, decisions.md 2026-07-21)."""
    if "point_interrogation" in familles:
        return "point_interrogation"
    return next(c for c in markers.DOUTE_PAR_NIVEAU if c in familles)


def _vide() -> dict:
    return {"propre": 0, "doute": 0, "copie": 0, "musees": set(),
            "familles": {}, "niveaux": {1: 0, 2: 0, 3: 0},
            # TOUTES les œuvres de doute du maître (onglet « Œuvres »), dans
            # l'ordre de rencontre : une entrée par référence, jamais une copie.
            "oeuvres": [], "exemple_copie": None,
            # ventilation du doute SEUL par musée détenteur (carte par maître) :
            # code -> {doute, nom, ville, coord, familles, niveaux}
            "musees_doute": {},
            # doute rattaché à aucun code musée (non cartographiable) : sert à
            # boucler l'invariant de comptage. Attendu ~0.
            "doute_sans_code": 0}


def _exemple(ref, titre, musee, ville, segment) -> dict:
    """Une notice réelle pour la vitrine : lien POP + les mots exacts du musée."""
    return {
        "reference": ref,
        "titre": titre if isinstance(titre, str) else None,
        "musee": musee if isinstance(musee, str) else None,
        "ville": ville if isinstance(ville, str) else None,
        "extrait": segment,
    }


def _oeuvre(ref, titre, code, musee, ville, famille, segment) -> dict:
    """Une œuvre de doute pour l'onglet « Œuvres » : le nécessaire pour la lister
    et ouvrir sa fiche POP. `code` est la famille RETENUE par le pipeline (le
    front ne re-classe jamais) ; `extrait` est le segment publié tel quel par le
    musée (seule citation littérale de l'application)."""
    return {
        "reference": ref,
        "titre": titre if isinstance(titre, str) else None,
        # `musee_code` est le code Muséofile — la CLÉ du musée, celle que porte
        # déjà la carte du profil (`musees_doute`). Elle est exportée depuis le
        # 2026-08-02 pour que le filtre par musée de l'onglet « Œuvres » et les
        # points de la carte désignent le même objet : deux noms de musée
        # identiques dans deux villes ne doivent jamais se confondre, et le lien
        # carte → œuvres ne doit pas se rejouer par rapprochement de libellés.
        "musee_code": code if isinstance(code, str) and code.strip() else None,
        "musee": musee if isinstance(musee, str) else None,
        "ville": ville if isinstance(ville, str) else None,
        "code": famille,
        "extrait": segment,
    }


def _lat_lon(valeur):
    """« lat, lon » (champ Joconde, au grain musée) → (lat, lon) arrondis, ou
    (None, None). On sépare lat et lon EXPLICITEMENT pour écarter tout risque
    d'inversion côté carte D3-geo (decisions.md, 2026-07-12)."""
    if not isinstance(valeur, str) or "," not in valeur:
        return None, None
    try:
        lat, lon = (float(x) for x in valeur.split(",")[:2])
    except ValueError:
        return None, None
    return round(lat, 5), round(lon, 5)


def resout_reference(auteur: str, en_beaux_arts: bool = True,
                     table=None) -> dict:
    """Ce qu'UNE référence dit de chaque maître, résolu en un seul verdict.

    Renvoie {maître: (categorie, famille, segment)} — famille et segment valent
    None pour l'attribution ferme. C'est le cœur des temps 1 et 2 : le champ
    `Auteur` peut nommer le même homme dans plusieurs segments, sous plusieurs
    graphies et avec plusieurs formules ; la référence ne pèse qu'une fois par
    maître, dans la catégorie la plus prudente et la famille la plus explicite.
    Isolée de main() pour être testable sans le CSV (tests/test_artistes.py).
    `table` est passée telle quelle à `_trouve_maitre` : le registre y met
    TOUTES_PERSONNES, les exports du volume laissent le défaut."""
    vus = {}  # maître -> {categories: set, familles: {code: segment}, copie: segment}
    for segment in auteur.split(";"):
        segment = segment.strip()
        if not segment:
            continue
        nom = _trouve_maitre(_pivot(segment), table)
        if nom is None:
            continue
        categorie, famille = markers.famille_segment(segment, en_beaux_arts)
        vu = vus.setdefault(nom, {"categories": set(), "familles": {}, "copie": None})
        vu["categories"].add(categorie)
        if categorie == "doute":
            # on garde le premier segment vu pour chaque famille : c'est lui qui
            # fournira l'extrait cité dans la vitrine « Œuvres »
            vu["familles"].setdefault(famille, segment)
        elif categorie == "copie" and vu["copie"] is None:
            vu["copie"] = segment

    resolu = {}
    for nom, vu in vus.items():
        categorie = _categorie_retenue(vu["categories"])
        if categorie == "doute":
            famille = _famille_retenue(vu["familles"])
            resolu[nom] = ("doute", famille, vu["familles"][famille])
        elif categorie == "copie":
            resolu[nom] = ("copie", None, vu["copie"])
        elif categorie == "propre":
            resolu[nom] = ("propre", None, None)
    return resolu


def _ecrire_oeuvres(artistes: list, agg: dict, meta: dict) -> int:
    """Écrit un fichier oeuvres/<slug>.json par maître : la TOTALITÉ de ses
    œuvres de doute, chargées à la demande par l'onglet « Œuvres ». Le dossier
    est d'abord vidé (les fichiers sont des artefacts générés, pas de reste
    d'un maître retiré). Chaque fichier est contrôlé par les mêmes invariants
    que le reste du pipeline, référence par référence."""
    if DOSSIER_OEUVRES.exists():
        for ancien in DOSSIER_OEUVRES.glob("*.json"):
            ancien.unlink()
    DOSSIER_OEUVRES.mkdir(parents=True, exist_ok=True)

    # Reproductions ouvertes déjà préparées (src/build_vignettes.py) : on rattache
    # `image` aux œuvres concernées, pour que la régénération complète ne les perde
    # pas. Absent au premier passage (l'index est produit ensuite) : sans effet.
    index_images = {}
    chemin_index = DOSSIER_WEB / "images_index.json"
    if chemin_index.exists():
        index_images = json.loads(chemin_index.read_text(encoding="utf-8"))

    total = 0
    for art in artistes:
        oeuvres = agg[art["nom"]]["oeuvres"]
        for o in oeuvres:
            img = index_images.get(o["reference"])
            if img:
                o["image"] = img
        # effectifs par famille présente, ordre canonique (repris de art["familles"])
        familles = [{"code": f["code"], "notices": f["notices"]}
                    for f in art["familles"]]
        attendu = {f["code"]: f["notices"] for f in familles}

        # --- Invariants de l'export (le front s'y fie sans re-vérifier) ---
        assert len(oeuvres) == art["doute"], \
            f"œuvres ≠ doute ({art['nom']} : {len(oeuvres)} ≠ {art['doute']})"
        obtenu = dict(Counter(o["code"] for o in oeuvres))
        assert obtenu == attendu, \
            f"familles des œuvres ≠ maitre.familles ({art['nom']})"
        refs = [o["reference"] for o in oeuvres]
        assert all(refs), f"œuvre sans référence Joconde ({art['nom']})"
        assert len(set(refs)) == len(refs), \
            f"référence en double ({art['nom']})"
        # aucune copie « d'après » : garanti par construction (les entrées ne sont
        # ajoutées que dans la branche « doute »), on le réaffirme ici.
        assert "d_apres" not in obtenu and "copie" not in obtenu, \
            f"une copie s'est glissée dans la liste ({art['nom']})"
        # Le filtre par musée de l'onglet « Œuvres » compte les œuvres ; la carte
        # du profil affiche `musees_doute`. Les deux doivent dire la même chose,
        # musée par musée, sinon le lecteur lit deux chiffres différents pour le
        # même point (invariant posé le 2026-08-02, phase 2).
        par_musee = Counter(o["musee_code"] for o in oeuvres if o["musee_code"])
        attendu_musees = {m["code"]: m["doute"] for m in art["musees_doute"]}
        assert dict(par_musee) == attendu_musees, \
            f"œuvres par musée ≠ carte du profil ({art['nom']})"
        assert sum(1 for o in oeuvres if not o["musee_code"]) == \
            art["doute_sans_musee"], \
            f"œuvres sans musée ≠ doute_sans_musee ({art['nom']})"

        fichier = {
            "slug": art["slug"],
            "nom": art["nom"],
            "doute": art["doute"],
            "familles": familles,
            "oeuvres": oeuvres,
            **meta,
        }
        chemin = DOSSIER_OEUVRES / f"{art['slug']}.json"
        chemin.write_text(json.dumps(fichier, ensure_ascii=False, indent=1),
                          encoding="utf-8")
        total += len(oeuvres)
    return total


def main() -> None:
    agg = {nom: _vide() for nom, *_ in MAITRES}
    total = 0

    # --- Recouvrement entre profils (mesuré le 2026-07-22) ---------------
    # Une même notice peut nommer DEUX maîtres retenus : « BUONARROTI
    # Michelangelo (?) ; SARTO Andrea del (?, manière de) » compte pour
    # Michel-Ange ET pour Andrea del Sarto. Additionner les profils compte donc
    # cette notice deux fois. On tient les deux mesures séparément :
    #   - appartenances : le lien maître-notice, ce que compte chaque fiche ;
    #   - notices : les références Joconde distinctes, ce qu'on peut comparer au
    #     total national et ce dont on déduit « hors liste ».
    # Jamais de soustraction sur une somme d'appartenances (decisions.md).
    refs = {"doute": set(), "propre": set(), "copie": set()}
    appartenances = {"doute": 0, "propre": 0, "copie": 0}
    fam_refs = defaultdict(set)      # famille -> références distinctes
    niv_refs = defaultdict(set)      # niveau  -> références distinctes
    partagees = {}                   # référence -> [(maître, famille), …]

    morceaux = pd.read_csv(CHEMIN_CSV, sep="|", usecols=COLONNES, dtype=str,
                           chunksize=TAILLE_MORCEAU)
    for morceau in morceaux:
        total += len(morceau)
        for ref, aut, dom, code, musee, ville, titre, coord in zip(
            morceau["Reference"], morceau["Auteur"], morceau["Domaine"],
            morceau["Code_Museofile"], morceau["Nom_officiel_musee"],
            morceau["Ville"], morceau["Titre"], morceau["coordonnees"],
        ):
            if not isinstance(aut, str):
                continue
            # Une référence, un poids, par maître : la résolution (catégorie la
            # plus prudente, famille la plus explicite) est faite d'un bloc par
            # resout_reference(). Les références sont uniques dans le CSV
            # (vérifié le 2026-07-21 : 1 023 705 lignes, 1 023 705 références),
            # la déduplication tient donc entièrement dans la ligne courante.
            resolu = resout_reference(aut, markers._dans_beaux_arts(dom))
            # recouvrement : ce que cette référence apporte à la liste entière
            doutes = [(n, f) for n, (c, f, _s) in resolu.items() if c == "doute"]
            if len(doutes) > 1:
                partagees[ref] = sorted(doutes)
            for nom, (categorie, famille, _s) in resolu.items():
                appartenances[categorie] += 1
                refs[categorie].add(ref)
                if categorie == "doute":
                    fam_refs[famille].add(ref)
                    niv_refs[NIVEAU_FAMILLE[famille]].add(ref)

            for nom, (categorie, famille, segment) in resolu.items():
                a = agg[nom]
                if isinstance(code, str):
                    a["musees"].add(code)
                if categorie == "propre":
                    a["propre"] += 1
                elif categorie == "copie":
                    # une notice réelle de copie « d'après », pour le bloc « À part »
                    a["copie"] += 1
                    if a["exemple_copie"] is None and isinstance(ref, str):
                        a["exemple_copie"] = _exemple(ref, titre, musee, ville,
                                                      segment)
                elif categorie == "doute":
                    a["doute"] += 1
                    a["familles"][famille] = a["familles"].get(famille, 0) + 1
                    a["niveaux"][NIVEAU_FAMILLE[famille]] += 1
                    # ventilation du doute par musée détenteur (carte par maître).
                    # Alimentée UNIQUEMENT ici : jamais sur le ferme ni la copie.
                    if isinstance(code, str) and code.strip():
                        md = a["musees_doute"].get(code)
                        if md is None:
                            md = a["musees_doute"][code] = {
                                "doute": 0,
                                "nom": musee if isinstance(musee, str) else None,
                                "ville": ville if isinstance(ville, str) else None,
                                "coord": coord if isinstance(coord, str) else None,
                                "familles": {}, "niveaux": {1: 0, 2: 0, 3: 0},
                                # Première (et, si doute==1, unique) notice du musée :
                                # sert à rendre les points « 1 œuvre » cliquables vers
                                # POP (n'est exporté que dans ce cas, voir plus bas).
                                "ref1": ref if isinstance(ref, str) else None,
                                "titre1": titre if isinstance(titre, str) else None}
                        md["doute"] += 1
                        md["familles"][famille] = md["familles"].get(famille, 0) + 1
                        md["niveaux"][NIVEAU_FAMILLE[famille]] += 1
                    else:
                        a["doute_sans_code"] += 1
                    # TOUTES les œuvres de doute (onglet « Œuvres »). Une référence
                    # ne traverse ce bloc qu'une fois par maître (resout_reference
                    # a déjà résolu la référence en UNE famille) : pas de doublon
                    # possible, la référence servira de clé de liste côté front.
                    a["oeuvres"].append(
                        _oeuvre(ref, titre, code, musee, ville, famille,
                                segment))
        print(f"\r  {total:,} notices lues".replace(",", " "), end="", flush=True)
    print()

    artistes = []
    for nom, *_ in MAITRES:
        a = agg[nom]
        familles = {code: a["familles"][code]
                    for code in markers.DOUTE_PAR_NIVEAU if code in a["familles"]}

        # Musées du doute : 1 entrée = 1 musée détenteur, doute SEUL, trié.
        musees_doute = []
        for code, md in a["musees_doute"].items():
            fam_liste = [{"code": c, "notices": md["familles"][c]}
                         for c in markers.DOUTE_PAR_NIVEAU if c in md["familles"]]
            niveaux = [md["niveaux"][1], md["niveaux"][2], md["niveaux"][3]]
            lat, lon = _lat_lon(md["coord"])
            # Invariants de comptage par musée : aucune ambiguïté possible.
            assert sum(f["notices"] for f in fam_liste) == md["doute"], \
                f"familles ≠ doute ({nom} / {code})"
            assert sum(niveaux) == md["doute"], \
                f"niveaux ≠ doute ({nom} / {code})"
            entree = {
                "code": code,
                "nom": md["nom"],
                "ville": md["ville"],
                "lat": lat,
                "lon": lon,
                "doute": md["doute"],
                "niveaux": niveaux,
                "familles": fam_liste,
            }
            # Musée à UNE seule œuvre concernée : on joint la référence (et le titre
            # s'il existe) de cette œuvre, pour rendre le point cliquable vers sa
            # fiche publique POP. Les entrées multi-œuvres restent inchangées.
            if md["doute"] == 1 and md["ref1"]:
                entree["oeuvre_unique"] = {
                    "reference": md["ref1"],
                    "titre": md["titre1"],
                }
            musees_doute.append(entree)
        musees_doute.sort(key=lambda m: m["doute"], reverse=True)
        # Invariant par maître : doute cartographié + doute sans code = doute total.
        assert (sum(m["doute"] for m in musees_doute) + a["doute_sans_code"]
                == a["doute"]), f"somme musées ≠ doute maître ({nom})"

        principal = musees_doute[0] if musees_doute else None
        musee_principal = None if principal is None else {
            "code": principal["code"],
            "nom": principal["nom"],
            "doute": principal["doute"],
            "part": round(principal["doute"] / a["doute"], 3) if a["doute"] else 0,
        }

        artistes.append({
            "nom": nom,
            # identifiant stable : nomme le fichier oeuvres/<slug>.json chargé à la
            # demande par l'onglet « Œuvres » (le front n'a que ce slug à connaître).
            "slug": _slug(nom),
            "propre": a["propre"],
            "doute": a["doute"],
            "copie": a["copie"],
            "musees": len(a["musees"]),
            "nb_musees_doute": len(musees_doute),
            "musee_principal": musee_principal,
            "doute_sans_musee": a["doute_sans_code"],
            "niveaux": [a["niveaux"][1], a["niveaux"][2], a["niveaux"][3]],
            "familles": [
                {"code": code, "libelle": LIBELLE_FAMILLE[code],
                 "niveau": NIVEAU_FAMILLE[code], "notices": n}
                for code, n in familles.items()
            ],
            "exemple_copie": a["exemple_copie"],
            "musees_doute": musees_doute,
        })
    artistes.sort(key=lambda x: x["doute"], reverse=True)

    # Slugs distincts : garantit qu'aucun fichier oeuvres/<slug>.json n'en écrase
    # un autre (les noms des maîtres sont uniques et le restent après slugification).
    slugs = [art["slug"] for art in artistes]
    assert len(set(slugs)) == len(slugs), "collision de slug entre deux maîtres"

    # --- Totaux de la liste : appartenances ET notices distinctes -----------
    # Invariants : une union ne peut pas dépasser la somme dont elle est tirée,
    # et l'écart est exactement le nombre de liens en trop portés par les
    # références partagées.
    for cat in ("doute", "propre", "copie"):
        assert len(refs[cat]) <= appartenances[cat], f"union > somme ({cat})"
    ecart_doute = appartenances["doute"] - len(refs["doute"])
    assert ecart_doute == sum(len(d) - 1 for d in partagees.values()), \
        "écart doute ≠ liens en trop des références partagées"
    assert sum(a["doute"] for a in artistes) == appartenances["doute"], \
        "somme des profils ≠ appartenances"

    totaux = {
        "appartenances_doute": appartenances["doute"],
        "notices_doute": len(refs["doute"]),
        "appartenances_propre": appartenances["propre"],
        "notices_propre": len(refs["propre"]),
        "appartenances_copie": appartenances["copie"],
        "notices_copie": len(refs["copie"]),
        "notices_partagees": len(partagees),
        # notices distinctes par famille et par niveau : ces deux ventilations
        # NE S'ADDITIONNENT PAS en `notices_doute` (une notice partagée peut
        # relever de deux familles, donc de deux niveaux)
        "familles_notices": {code: len(fam_refs[code])
                             for code in markers.DOUTE_PAR_NIVEAU
                             if code in fam_refs},
        "niveaux_notices": {str(n): len(niv_refs[n]) for n in (1, 2, 3)},
    }
    # les références nommant deux maîtres retenus, publiées en clair
    references_partagees = [
        {"reference": ref,
         "maitres": [{"nom": n, "famille": f} for n, f in couples]}
        for ref, couples in sorted(partagees.items())
    ]

    sortie = {
        "critere": "maître de référence ET ≥ 10 notices de doute (hors copie)",
        "lexique": "markers.py v2 (famille_segment) — unité : référence Joconde unique",
        "unite": "reference",
        "totaux": totaux,
        "references_partagees": references_partagees,
        "version_donnee": "2026-07-01",
        "date_generation": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "source": "Collections des musées de France : base Joconde",
        "url_source": URL_CSV,
        "niveaux": {str(n): LIBELLES_NIVEAUX[n] for n in (1, 2, 3)},
        "artistes": artistes,
    }

    DOSSIER_WEB.mkdir(parents=True, exist_ok=True)
    chemin = DOSSIER_WEB / "artistes.json"
    chemin.write_text(json.dumps(sortie, ensure_ascii=False, indent=1),
                      encoding="utf-8")

    # Un fichier d'œuvres par maître (onglet « Œuvres », chargé à la demande) :
    # mêmes métadonnées de provenance que l'export léger.
    meta_oeuvres = {
        "version_donnee": sortie["version_donnee"],
        "date_generation": sortie["date_generation"],
        "source": sortie["source"],
        "url_source": sortie["url_source"],
    }
    total_oeuvres = _ecrire_oeuvres(artistes, agg, meta_oeuvres)

    print(f"\n{len(artistes)} maîtres exportés → {chemin} "
          f"({chemin.stat().st_size / 1024:.1f} Ko)")
    print(f"{total_oeuvres} œuvres de doute → {DOSSIER_OEUVRES}/ "
          f"({len(artistes)} fichiers)")
    print(f"{'maître':22} {'doute':>6} {'propre':>7} {'copie':>6} "
          f"{'mus.doute':>9} {'top %':>6}")
    for art in artistes:
        part = art["musee_principal"]["part"] if art["musee_principal"] else 0
        print(f"{art['nom']:22} {art['doute']:>6} {art['propre']:>7} "
              f"{art['copie']:>6} {art['nb_musees_doute']:>9} {part:>6.0%}")
    total_sans_musee = sum(art["doute_sans_musee"] for art in artistes)
    print(f"\nDoute sans code musée (non cartographiable) : {total_sans_musee}")
    print(f"\nAppartenances maître-notice : {appartenances['doute']} · "
          f"notices distinctes : {len(refs['doute'])} · "
          f"partagées entre deux maîtres : {len(partagees)}")
    for ref, couples in sorted(partagees.items()):
        print(f"  {ref} : " + " · ".join(f"{n} [{f}]" for n, f in couples))


if __name__ == "__main__":
    main()
