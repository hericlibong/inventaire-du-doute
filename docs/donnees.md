# Constats sur les données

Tout ce qu'on apprend sur la base Joconde au fil du projet : structure, pièges,
chiffres vérifiés. Chaque constat indique sa date et comment il a été obtenu.

## Table d'identité des maîtres : qui est écarté, et pourquoi (2026-07-21, temps 2)

Établie à partir d'un inventaire exhaustif des **246 formes d'auteur** captées par les motifs
en vigueur (mentions prudentes et certaines, comptées en références uniques), relu forme par
forme. Après application : **141 formes retenues** sur les 27 maîtres.

Cette liste est destinée à être **publiée** : elle rend la sélection contrôlable.

| Maître | Personnes écartées | Références concernées |
|---|---|---:|
| Michel-Ange | Corneille Michel-Ange, Cerquozzi, Merisi dit Le Caravage, Pace, Anselmi, Pistoletto, Challe, Slodtz, Campidoglio, Membrini, Aliprandi, Unterperger, Yrazazbal, Ricciolini, Pollet | 24 prudentes, **489 certaines** |
| Raphaël | ≈ 50 porteurs du **prénom** Raphaël (Lonne, Lardeur, Mengs, Collin, Sadeler, Freida, Delorme…), l'éditeur Raphael Tuck, Raphael-Schwartz, Giovanni Santi le père | 4 prudentes, ≈ 410 certaines |
| Véronèse | Carlo Caliari (fils), Benedetto Caliari (frère), Gabriele Caliari, Bonifazio de' Pitati, Zenone da Verona | 3 prudentes, 21 certaines |
| Nicolas Poussin | Lemaire-Poussin, Lavallée-Poussin, Gaspard Dughet dit Gaspard Poussin, Le Guaspre, Poussin-Heydeck, Lemaire | 4 prudentes, 20 certaines |
| Le Tintoret | Domenico Robusti (le fils) | 1 prudente, 12 certaines |
| Van Dyck | Philip van Dyck, Philippe Van Dyck, Pierre Van Dyck | 0, 7 certaines |
| Titien | Francesco Vecellio, Cesare Vecellio, Tiziano Aspetti | 1 prudente, 10 certaines |
| Simon Vouet | Aubin Vouet, Ferdinand Vouet | 2 prudentes, 7 certaines |
| Léonard de Vinci | Pierino da Vinci (le neveu), Marguerite Vinci, « Leonardo José » | 0, 4 certaines |
| Ingres | Ingres Jean Marie Joseph, « Madame Ingres » | 1 prudente, 4 certaines |
| Rubens | Arnold Frans Rubens, le « Rubens des batailles » | 0, 1 certaine |
| Ribera | Roman Ribera y Cirera, Pierre Ribera | 0, 3 certaines |
| Pierre Mignard | Pierre Mignard II (le neveu) | 0, 1 certaine |

Les quatorze autres maîtres n'ont **aucun homonyme** dans la base : Charles Le Brun,
Le Primatice, Rembrandt (l'exclusion Bugatti datait de 2026-07-07), François Clouet,
Annibale Carracci, Rodin, Boucher, Andrea del Sarto, Guido Reni, Greuze, Le Corrège,
Hyacinthe Rigaud, Géricault, Fragonard.

**Un faux négatif corrigé au passage** : « SANTI Raffaello », forme d'état civil de Raphaël,
n'était captée par aucun motif (ni `RAPHAEL`, ni `SANZIO` n'y figurent) — 12 mentions
prudentes par forme, **+3 références** une fois dédoublonnées avec « RAPHAEL ».

**Fautes de saisie sur le nom du maître lui-même** : la notice `06070060045` du musée Ingres
de Montauban écrit `IIngres Jean-Auguste-Dominique`, avec deux I. Aucun motif ne peut la
rattacher, et on ne cherche pas à rattraper ces cas un par un — ce serait réécrire la base.
Limite ordinaire du procédé, à dire dans la page méthode.

**Totaux après les temps 1 et 2** : doute **2 341 → 2 188**, certaines **29 995 → 28 240**.
Michel-Ange : 148 références prudentes, 3 musées (Louvre 146, Rennes 1, Dole 1), part
**39 %** contre 19 % affiché.

## Audit de fiabilité du pipeline des maîtres (2026-07-21) — constats mesurés

Scan exhaustif des **1 023 705 lignes** du CSV, reproduit indépendamment à partir du code
actuel (`src/build_artistes.py`, `markers.py`). Scripts d'audit en lecture seule, hors dépôt.
**Aucun chiffre de cette section n'est canonique** : ce sont des mesures de contrôle, en
attente du chantier de fiabilisation.

### 1. Deux défauts distincts, longtemps confondus

- **L'unité de comptage.** Le pipeline agrège des **segments** du champ `Auteur`
  (séparés par `;`), alors que l'interface et la documentation parlent de **notices**. Une
  notice qui nomme le maître deux fois sous deux graphies compte deux fois.
- **L'identité.** Le test au mot entier empêche « SERODINE → Rodin », mais pas qu'un
  **prénom ou un nom partagé** désigne une autre personne.

### 2. Effet de l'unité de comptage (doublons de graphies)

Segments actuellement publiés → références uniques, sur les maîtres touchés :
Le Primatice **269 → 197** ; Le Corrège **46 → 25** ; Le Tintoret **47 → 39** ;
Véronèse **41 → 38** ; Titien **20 → 12** ; Fragonard **31 → 30** ; Simon Vouet **51 → 48**.
Les vingt autres maîtres sont inchangés.

Cause : une même notice porte deux graphies du même homme — `LE PRIMATICE` et
`PRIMATICCIO Francesco`, `LE CORRÈGE` et `ALLEGRI Antonio`, `LE TITIEN` et
`VECELLIO Tiziano`, `MICHEL-ANGE` et `BUONARROTI Michelangelo`, `LE TINTORET` et
`ROBUSTI Jacopo`.

**Total des 27 : 2 341 segments → 2 225 références uniques.**

### 3. Effet de l'identité (homonymes)

**40 références prudentes sont rattachées au mauvais maître**, vérifiées une par une :

| Maître | Réf. fausses | Personnes réellement désignées |
|---|---:|---|
| Michel-Ange | 24 | CORNEILLE Michel-Ange (13), CERQUOZZI Michelangelo (6), MERISI Michelangelo dit Le Caravage (4), PACE Michelangelo (1) |
| Nicolas Poussin | 4 | LEMAIRE-POUSSIN, LAVALLÉE-POUSSIN Étienne de, DUGHET Gaspard, LEMAIRE Jean |
| Raphaël | 4 | COLLIN Raphaël, MENGS Anton Raphael, MASSARD Jean Marie Raphaël Léopold, VELUT Raphaël |
| Véronèse | 3 | CALIARI Benedetto (2), CALIARI Carlo (1) |
| Simon Vouet | 2 | VOUET Aubin |
| Ingres | 1 | INGRES Jean Marie Joseph |
| Le Tintoret | 1 | ROBUSTI Domenico (le fils) |
| Titien | 1 | VECELLIO Francesco |

**Total des 27 après dédoublonnage et retrait des homonymes : 2 185 références** — soit
**−156** par rapport aux 2 341 publiés.

Références témoins vérifiées : `M0347001723` (Buonarroti, rattachement correct) ;
`000PE020938` (Cerquozzi), `000PE024738`, `00000077350`, `000PE021251` (Merisi/Le Caravage),
`08940000842` (Pace), `50350011790`–`50350011803` (Corneille) — toutes incorrectes.

### 4. Le dénominateur est plus atteint que le numérateur (constat nouveau)

Le chiffre affiché sous chaque fiche (« *n* sur *N* œuvres rattachées à son nom ») utilise
`propre + doute`. Or la partie `propre` capte **beaucoup plus d'homonymes** que la partie
prudente, parce qu'elle est bien plus volumineuse :

- **Michel-Ange** : 749 références « certaines », dont **422 pour CORNEILLE Michel-Ange** —
  soit **deux fois plus que Buonarroti lui-même (212)**. Treize autres homonymes suivent
  (ANSELMI, PISTOLETTO, CHALLE, CAMPIDOGLIO, SLODTZ, MEMBRINI, ALIPRANDI, UNTERPERGER,
  YRAZAZBAL, RICCIOLINI, CARAVAGGIO, POLLET). **19 formes d'auteur distinctes en tout.**
- **Raphaël** : **52 formes**, 1 743 références « certaines ». « Raphaël » est capté comme
  **prénom** : LONNE Raphaël (129), LARDEUR Raphaël (51), MENGS Anton Raphael (33),
  COLLIN Raphaël (20), RAPHAEL-SCHWARTZ (18)…
- Plus discrets, même mécanisme : Titien (ASPETTI Tiziano, 8 ; VECELLIO Cesare, 2),
  Van Dyck (DYCK Philip van, 4 ; VAN DYCK Pierre, 2), Le Tintoret (ROBUSTI Domenico, 10),
  Poussin (LEMAIRE-POUSSIN 8, LAVALLÉE-POUSSIN 6, GASPARD POUSSIN 3), Véronèse (CALIARI
  Carlo 11, Benedetto 8), Simon Vouet (VOUET Aubin 6), Léonard (VINCI Pierino da 2,
  VINCI Marguerite 1), Ingres (INGRES Jean Marie Joseph 3, « MADAME INGRES » 1).

**Conséquence éditoriale** : la part affichée sur ces fiches est fausse dans les deux termes.
Michel-Ange annonce aujourd'hui « 172 sur 921 » ; le calcul corrigé donne un ordre de
grandeur de **148 sur ≈ 405** — d'environ 19 % à environ 37 %.

### 5. Michel-Ange, profil recalculé (contrôle)

Références uniques, homonymes écartés : **doute 148** (contre 172) ; « de son école » **110**,
« attribué à » **37**, « ? » **1**, « genre de » **0** ; **3 musées** — Louvre **146**,
Rennes 1, Dole 1 (contre 9 musées affichés). Mention dominante : « de son école »,
110 sur 148, ≈ 74 %.

Dénominateur : une seule référence (`02110002116`) appartient à la fois aux ensembles
« certain » et « prudent ». L'union se situe autour de **405** références selon l'étendue de
la table d'homonymes retenue — **valeur à figer avec la table définitive**, elle bouge de
±50 selon que l'on écarte 4 ou 16 formes.

### 6. Références portant plusieurs formulations prudentes

Sur les 27 maîtres, **trois références seulement**, toutes chez Simon Vouet :
`M0332004170`, `M0332004171`, `M0332004172` — chacune porte `VOUET Simon (?)` **et**
`VOUET Simon (atelier, dessinateur)`. Elles doivent compter pour **trois** références au
total, non pour six. Leur ventilation par famille dépend d'un arbitrage encore ouvert
(priorité entre « ? » et une formule de distance) : voir decisions.md.

### 7. Ce que l'erreur n'atteint pas (vérifié dans le code)

- `src/build_exports.py` (→ `niveaux.json`, `musees.json`) et `src/count_markers.py`
  travaillent **par ligne** (`det[...].any(axis=1)`), sans identifier de maître : une notice
  y compte **une seule fois**. Le total national de **24 507** notices prudentes n'est donc
  pas invalidé par ce défaut.
- Les **familles globales peuvent se recouvrir** (une notice porte parfois deux formules) :
  déjà documenté ici même et dans `vue_ensemble.json` — elles ne sont jamais additionnées,
  et aucun diagramme en anneau n'est utilisé pour cette section.
- `src/build_cases.py` (→ `cas.json`) et `src/build_revisions.py` (→ `revisions.json`) ne
  dépendent pas de l'identification des maîtres.

**Dépendent d'`artistes.json`** : `vue_ensemble.json` (recalculé depuis lui), la route
`/les-presque` (fiches, graphique, carte, répertoire, jauges, en-têtes rédigés), la route
`/echelle` (via `vue_ensemble.json`) et la page `/methode` (nombre de noms, total des
notices prudentes des maîtres).

### 8. Candidats : pourquoi un seuil quantitatif ne suffit pas

Comptage de **toutes** les formes d'auteur de la base par références prudentes uniques :
**332 formes atteignent 10 références**, dont **298 hors des 27 actuels**. Elles se
répartissent ainsi :

- **18 ne sont pas des personnes** : Imprimerie de Wissembourg (392), « anonyme » (152),
  « CARRACCI l'un des » (78), Manufacture de Creil (60), « COYPEL l'un des » (60),
  Faïencerie de Sarreguemines (51), Manufacture de cristaux du Creusot (46)…
- **280 sont des noms de personnes** — mais beaucoup relèvent de **fonds locaux massifs**,
  sans rapport avec un maître de référence : BARLA Jean-Baptiste (**5 791**, la monoculture
  d'histoire naturelle de Nice déjà connue), CLAUSEL Alexandre (295), NORMAND (244),
  TIRODE (231), MORINET (168), DUTHOIT (94 et 93)…
- **106 dépassent 20 références**, **174 se situent entre 10 et 19**.

**Faux négatifs (constat nouveau).** Des maîtres de référence évidents dépassent largement
l'ancien seuil de 20 et sont pourtant **absents** de la liste, composée à la main en
2026-07-07 : BARBIERI Giovanni Francesco, dit **Le Guerchin** (93) ; **BOUCHARDON** Edme
(86) ; PIPPI Giulio, dit **Jules Romain** (78) ; **CARRACCI Ludovico** (76) ; **TÉNIERS**
David (67) ; **GÉRARD** François (65) ; MAZZUOLA Francesco, dit **Le Parmesan** (63) ;
BONACCORSI Piero, dit **Perino del Vaga** (53) ; **MENZEL** (47) ; **BANDINELLI** (45) ;
**TEMPESTA** (43) ; **GIORDANO** Luca (42). Dans la tranche 10-19 : **DÜRER** (19),
**Le Sueur** (18), **Fra Bartolomeo** (18), **Rosso Fiorentino** (18), **Ostade** (17),
**Jean Goujon** (17), **Dolci** (19), **Nicolò dell'Abate** (19).

Ces nombres sont **par forme d'auteur**, avant fusion des graphies et avant
désambiguïsation : ils indiquent des pistes à instruire, pas des profils prêts à publier.

### 9. Autres constats de forme

- Le qualificatif n'est **pas toujours entre parenthèses** : le nom-pivot d'Ingres apparaît
  sous la forme `INGRES JEAN-AUGUSTE-DOMINIQUE ATTRIBUE A` (189 références). La convention
  « qualificatifs entre parenthèses » est fréquente, pas universelle — déjà relevé en
  2026-07-07, confirmé ici à grande échelle.
- Un nom-pivot dégénéré `A` totalise 19 références prudentes : bruit de saisie à écarter.

## Reconnaissance pour la « Vue d'ensemble » des formulations prudentes (2026-07-15)

Tour d'horizon avant de cadrer une future section « Vue d'ensemble » du dossier
« Les presque ». Chiffres croisés depuis les exports déjà validés (`artistes.json`,
`niveaux.json`, `musees.json`) ; export dédié : `data/exports/web/vue_ensemble.json`
(script `src/build_vue_ensemble.py`, cohérence vérifiée par `assert`).

**Message central (à porter par la section).** Dans l'ensemble de Joconde,
« attribué à » domine fortement (niveau 1 « Presque lui » = 20 014 / 24 507, 81,7 %,
et encore 76 % une fois la monoculture de Nice retirée). **Dans les 27 noms
retenus, le rapport s'inverse** : les liens plus indirects — école, atelier,
manière (niveau 2 « Autour de lui ») — prennent le dessus (niveaux dans les 27 :
901 / 1 234 / 206, soit 52,7 % de niveau 2). C'est ce **contraste** qui doit
porter la vue.

**Périmètre.** Les 27 noms ne pèsent que **2 341** des 24 507 doutes (≈ 9,6 %).
La « Vue d'ensemble » parle donc d'un corpus dix fois plus grand que les 27.

**Familles de doute (recouvrements possibles → jamais additionnées) — global /
dans 27 / hors 27 :** attribué à 17 926 / 876 / 17 050 ; ? 2 213 / 25 / 2 188 ;
école de 1 871 / 919 / 952 ; atelier 1 236 / 230 / 1 006 ; manière 703 / 181 / 522 ;
entourage 503 / 77 / 426 ; genre 303 / 25 / 278 ; suiveur 80 / 8 / 72. (Famille
`presume`, n=4, marginale, exclue de l'export.)

**Monoculture divulguée.** Muséum d'histoire naturelle de Nice — planches Barla
« attribué à » = **5 791** doutes (23,6 % du doute national), 100 % niveau 1, un
naturaliste et non un maître de l'art. `doute_hors_monoculture` = 18 716. Le
hors‑27 (22 166) en est largement composé.

**Fiabilité du hors‑27.** Au niveau **famille**, fiable (fiabilités mesurées T4/
T4bis : 86,7 % à 100 % selon la formule). Au niveau **« rattaché à un maître »,
non validé** hors des 27 (seuls noms désambiguïsés). → publiable **par famille**,
**jamais par nom** hors des 27 ; toujours distinguer « avec / sans monoculture ».

**Copies « d'après » : tenues à part.** Catégorie distincte, jamais mêlée au
doute : `d'après` 22 564 + `copie` 280 = **22 624**.

**Domaines (réserve, avec caveat).** `comptages_domaines.csv` donne le doute par
domaine (dessin 13 324, peinture 4 851, estampe 2 198…), mais le champ Domaine est
**multi‑valué** : la somme (29 127) dépasse le total (24 507) → double‑comptage,
à ne montrer qu'en parts indicatives. Hors export « Vue d'ensemble » pour l'instant.

**Période : écartée en V1.** Non exportée pour le doute ; générable depuis
`Millesime_de_creation` mais ~16 % de datables → trop lacunaire pour une frise
honnête.

**Top musées : laissés en réserve** pour cette section (données présentes dans
`musees.json`/`territoires.json`, mais non incluses dans l'export à ce stade).

## Le champ Ancienne_attribution au microscope (2026-07-13, audit avant rubrique « Révisions »)

Scans complets du CSV (trois passes par morceaux) avant de cadrer la rubrique
« Révisions ». Périmètre : notices où l'ancienne attribution **diffère** de
l'auteur actuel après normalisation (parenthèses retirées, casse ignorée).

**Volumes.** 27 266 notices ont le champ renseigné ; 26 846 ont aussi un
auteur actuel ; **26 667 portent un nom différent** (98 % — le champ n'est
presque jamais une redite). Destination de l'auteur actuel (classée au
lexique v2, segment par segment) :

| Destination | Notices | Part |
|---|---|---|
| un autre nom franc | 14 036 | 52,6 % |
| anonyme | 5 824 | 21,8 % |
| un autre nom, encore prudent (attribué, ?, école…) | 4 559 | 17,1 % |
| anonyme + « d'après » (devenue copie) | 2 102 | 7,9 % |
| copie seule | 128 | 0,5 % |
| autre | 18 | 0,1 % |

**Au moins cinq formats cohabitent dans le champ :**

1. `NOM (ancienne attribution)` — le plus courant ;
2. `NOM (attribué en 1869)` / `(attribué vers …)` — **attribution datée** :
   1 551 notices (Louvre, Versailles, Orsay…) ;
3. `NOM (CAT. 1938)` — référence de catalogue : 378 (musée Magnin surtout) ;
4. **chaînes** `A (CAT. 1922) ; B (CAT. 1938)` — 5 798 notices ont ≥ 2
   segments (jusqu'à 4 et plus) : de vraies chronologies d'attribution ;
5. prose libre (« ATTRIBUTION FAITE PAR BENJAMIN COUILLEAUX EN 2012 ») — rare.

Au total **1 907 notices (7,2 %) portent au moins une date fiable**, étalées
de 1790 aux années 2000 → trop peu pour une frise vedette ; assez pour dater
les cas qui le permettent.

**Concentration** : 59,5 % musée du Louvre, 62,9 % domaine dessin — le
phénomène est en grande partie le quotidien des cabinets d'arts graphiques.
146 musées concernés ; hors Louvre : 10 805 notices.

**Pièges — dont deux commis par notre propre audit rapide, corrigés le jour
même** (la preuve que les contrôles type SERODINE/RODIN restent nécessaires) :

- un motif trop large a pris les **années de vie** `(1452-1519)` pour des
  dates de catalogue → seules formes fiables : `CAT. AAAA`, `INVENTAIRE`,
  `attribué en AAAA` ;
- « attribu » en sous-chaîne matche « attribution » — mot présent dans le
  libellé même du champ ! → toujours `attribu[ée]` borné par `\b` ;
- grands noms en sous-chaîne : « ÉCOLE CARAVAGESQUE » compté pour Caravage
  (4 pollutions mesurées sur ~2 300 rattachements — faible ici, mais réel) →
  **mot entier obligatoire**, comme pour les 27 maîtres ;
- **23,1 % des anciennes attributions portaient déjà un doute** (« école
  de », « ? », « attribué ») : l'« avant » n'était pas un verdict ;
- « d'après » dans l'ancienne attribution : 1 198 cas (l'œuvre était déjà
  tenue pour copie — avant/après de copiste, pas d'auteur) ;
- noms proches avant/après **légitimes** (24 % partagent un token ≥ 4
  lettres) : père/fils (WILLE Jean Georges → WILLE Pierre Alexandre),
  graphies (PRIMATICE → PRIMATICCIO), même nom passé en « d'après » — à
  afficher verbatim, jamais fusionner ;
- **le dernier segment d'une chaîne peut être l'attribution actuelle**
  (Bellechose, Louvre) : comparer segment par segment, jamais le champ entier ;
- la **direction inverse existe** : « ANONYME, 18E SIECLE (CAT. 1938) » →
  GUARDI — une œuvre peut gagner un nom (à chiffrer au pipeline) ;
- extraction d'un nom lisible : fiable pour **59 %** des anciens noms (règle
  stricte : premier segment, hors parenthèses, sans chiffre ni « ? » ni
  « école », ≤ 45 caractères) et **99,5 %** des auteurs actuels.

**Remplissage utile** (sur les 26 667) : Titre 96,5 %, Ville 100 %,
Dénomination 34,8 %. Grands noms au **mot entier** dans les anciennes
attributions : Vinci 511, Poussin 350, Rubens 236, Rembrandt 227, Le Brun 115,
Fragonard 114, Watteau 107…

## Images des œuvres : Joconde n'en fournit pas d'exploitable en droit (2026-07-14)

Audit pour savoir si la rubrique « Avant / après » peut être illustrée
(champs CSV + test POP réel).

- **Le CSV ne porte aucune URL d'image ni chemin.** Il a `Presence_image`, un
  **booléen** : sur le corpus révisions, **92 % = « oui »** (24 529 / 26 667),
  8 % = « non ». C'est « une image existe sur POP », pas un droit d'usage.
- `Source_de_la_representation` (remplie 5 %) décrit le **sujet** (Nouveau
  Testament, mythologie…), pas la source du cliché. `Lien_site_associe`
  (58 %) pointe vers le site du musée (ex. arts-graphiques.louvre.fr).
- **Test POP** (notice `000DE023183`) : POP affiche bien l'image, servie
  depuis un **bucket S3 interne**
  (`popcorn-prd-perf-assets.s3.gra.io.cloud.ovh.net/joconde/{ref}/…`). Le
  nom de fichier est le numéro d'inventaire.
- **Droits** : POP n'affiche **aucune mention par œuvre** ; seulement « Licence
  Etalab 2.0 sauf mention contraire » en pied de site. La Licence Ouverte
  couvre les **métadonnées textuelles** de Joconde, **pas les photographies**,
  dont les droits reviennent le plus souvent à chaque musée (« mention
  contraire »).

**Conclusion** : pas d'affichage d'image en V1. Reconstruire l'URL = hotlinker
un CDN gouvernemental interne (instable) et on ne peut pas vérifier la licence
cliché par cliché sur 26 667 œuvres (règle CLAUDE.md : image externe = source
secondaire, licence vérifiée par fichier). La carte reste **textuelle + lien
POP** ; illustration manuelle d'une poignée de cas via Wikimedia Commons
possible plus tard (précédent des 27 portraits).

## Périodes et types du corpus révisions (2026-07-14)

Sur les 26 667 avant≠après : **domaine** dessin 63,5 %, peinture 23,8 %,
beaux-arts 5,3 %, arts décoratifs 2 %, sculpture 1,4 %, estampe 0,6 %… — le
dessin domine encore plus que dans la base (cabinets d'arts graphiques).
**Datation de l'œuvre** : seulement **16,4 %** ont un millésime propre
(4 375) — bien moins que la base (51,6 %), car les dessins sont peu datés ;
ces datables se concentrent aux **16ᵉ–18ᵉ s.** (966 / 1 239 / 1 111). À
distinguer de la **date de la révision** (« attribué en 1869 », « CAT. 1938 »),
présente sur seulement **7,2 %** (1 907). Deux « dates » différentes, toutes
deux trop rares pour porter une frise — assez pour dater des cas isolés.

## Révisions : constats du pipeline (2026-07-14, build_revisions.py)

Construction de l'export `revisions.json`. Ce que le pipeline a confirmé ou
révélé (chiffres définitifs, à jour) :

- **Types de passage** (partition validée par `assert`, somme = 26 667) : vers
  un autre nom **14 056** (52,7 %), vers l'anonyme **5 824** (21,8 %), vers une
  attribution prudente **4 557** (17,1 %), vers une copie **2 230** (8,4 %). Le
  résidu (~18, ni nom ni anonyme ni copie — ex. « Atelier de X » écarté) est
  rangé en « autre nom ».
- **Direction inverse** (l'ancien label était anonyme, l'actuel porte un nom) :
  **5 584** notices — presque autant que « vers l'anonyme » (5 824). Constat
  éditorial fort : la base enregistre presque autant d'œuvres qui **gagnent**
  un nom que d'œuvres qui en perdent un. Désamorce tout récit de « chute ».

- **Deux styles de catalogage** dans le champ, à gérer au parsing :
  1. *parenthétique* (Magnin, Crozatier…) : `NOM (ancienne attribution)`,
     `NOM (CAT. 1938)` — propre ;
  2. *prose préfixée* (Louvre surtout) : `ancienne attribution : NOM`,
     `anciennes attributions : NOM ; NOM2` — le champ **répète son propre nom**
     en préfixe. L'extraction naïve gardait « ancienne attribution : CARUCCI
     Jacopo » comme « nom ». Corrigé : on retire le préfixe-artefact
     (`anciennes? attributions? :`, `(anciennement) attribué à :`, `attr.`)
     avant extraction, et on rejette `anonyme`/`école`/chiffre/« ? ».

- **Le graphe « anciens noms fréquents » n'est PAS un classement fiable** — deux
  contaminations mesurées :
  1. *copie d'après* : beaucoup d'anciens labels disent déjà « copie d'après
     X » (X n'a jamais été l'attribution). Michel-Ange : 233 bruts → **119**
     hors copie. Rubens 236 → 197, Rembrandt 228 → 192, Poussin 350 → 316. Le
     comptage retenu **exclut** les labels « d'après/copie ».
  2. *effet mono-musée* : sur Michel-Ange, **202 des 233 viennent du seul
     Louvre** (qui pèse déjà 59,5 % du corpus). Toute fréquence nationale de
     noms est en partie une fréquence Louvre.
  → Décision : les anciens noms servent de **filtre de navigation**, pas de
  palmarès chiffré (comptage hors copie exporté quand même : Vinci 499,
  Poussin 316, Rubens 197, Rembrandt 192, Titien 124, Le Brun…).

- Rappel de rattachement **mot entier** confirmé utile : « TIZIANO » ajouté à
  Titien (44 → 138), « BUONARROTI » à Michel-Ange (vérifié réel), sans capter
  « ÉCOLE CARAVAGESQUE » pour Caravage.

## Révisions : ce que la vérification manuelle a appris (2026-07-14 bis)

80 lignes jugées par l'utilisateur. Enseignements sur les données (les choix de
catégories sont dans decisions.md) :

- **Deux structures de « ; » à ne pas confondre.** Le « ; » sépare des
  hypothèses d'attribution SAUF quand il est **dans une parenthèse** : là il est
  biographique (« DYCK Antoon van (Anvers, 1599 ; Blackfriars, 1641) » = une
  seule attribution). Un découpage naïf comptait deux hypothèses. → découpage à
  profondeur de parenthèses nulle.
- **Une chaîne peut répéter le même nom.** « Champaigne (Villot) ; Champaigne
  (Brière) » ou « Oudry (1869) ; Oudry (1912) ; Oudry (1930) » = un seul nom,
  plusieurs sources/dates — pas « plusieurs noms ». Il faut compter les
  hypothèses **distinctes**, pas les segments.
- **Parenthèses imbriquées** (« Santi Di Tito (16e siècle (2e moitié), Italie) »)
  et **parenthèse ouvrante orpheline** en tête (« (PIERRE DE CORTONE… ») :
  saisies réelles qui cassent une extraction naïve.
- **Le champ contient des notes de prose** (« Changement d'attribution »,
  « Dessin réattribué par Antoine Schnapper », « X a rappelé la présence au
  Salon… ») : ce ne sont pas des noms, à écarter de l'extraction et de la galerie.
- **Des lieux ressemblent à des noms** (« anciennement attribué à
  Midden-Beemster » — un lieu de naissance) : rare, non détectable à coup sûr ;
  ces cas sont des chaînes/prose, donc hors galerie de toute façon.
- **L'ancien label est souvent déjà prudent** : « attribué à », « école de »
  dans l'avant. Un passage « attribué à Rosa → Rosa (école) » reste un vrai
  cas « même nom, plus prudent » ; « école de Mazzuola → Mazzuola » est au
  contraire une **confirmation** (moins de réserve), pas une mise en garde.
- **Répartition définitive** (7 catégories, partition = 26 667) : autre nom
  13 125 (49,2 %), plusieurs anciens noms 3 177 (11,9 %), mineur/complexe 3 222
  (12,1 %), vers l'anonyme 3 371 (12,6 %), vers une copie 1 742 (6,5 %), même
  nom plus prudent 1 062 (4,0 %), déjà une copie 968 (3,6 %). Direction inverse
  (anonyme → un nom) : 5 283.

## Le champ Region est dédoublé par l'accent (2026-07-13)

`Île-de-France` (265 926 notices) et `Ile-de-France` (265 765) coexistent :
la même région coupée en deux par une variante de graphie. À normaliser avant
tout usage territorial du CSV. (Les exports actuels n'y passent pas : la
carte par maître utilise les coordonnées des musées.)

## Homonymes et racines de noms partagées (2026-07-13, signalé par un lecteur)

Le champ `auteur` contient des noms différents qui **partagent une racine** avec un
maître de la liste. Tant que le rattachement se faisait par sous-chaîne, ils étaient
comptés à tort pour le maître (corrigé le même jour, voir decisions.md). Cas relevés
par un scan de toute la base :

- **SERODINE** Giovanni, **PERRODIN** Auguste-François → captés par « RODIN » ;
- **VINCIDOR** Tommaso → capté par « VINCI » ;
- **SOLDYCK**, **DYCKHOFF** → captés par « DYCK » (Van Dyck) ;
- **RIBERAT**, **VALRIBERA** → captés par « RIBERA » ;
- **POUSSINES**, **CORREGES** → captés par « POUSSIN », « CORREGE ».

Cas particulier **père/fils** : « **Tintoretto Domenico** » (Domenico Tintoretto,
1560-1635) est le fils de Jacopo Robusti dit **Le Tintoret** (1518-1594). Les deux
partagent le nom italien ; seul Jacopo est dans la liste. Les vraies notices de
Jacopo sont cataloguées « **Le Tintoret** ou il Tintoretto (Jacopo Robusti dit) » —
le mot français « Tintoret » y figure, ce qui permet de les distinguer du fils.

Coquilles de saisie observées : « **IIngres** » (double I) pour Ingres — non
rattrapée par le test mot entier (perte assumée d'une notice en propre).

Leçon : un nom d'auteur n'est pas un identifiant ; le rapprochement doit se faire sur
le **mot entier**, et les homonymes proches (père/fils, racines communes) sont un
piège récurrent de la base.

## Constats de l'exploration initiale (2026-07-03, via l'API Opendatasoft)

### L'écart de volumétrie entre portails est éclairci

- data.gouv.fr annonce « + 1 000 000 notices » pour le CSV complet (1,1 Go).
- Le portail du ministère expose un dataset nommé `base-joconde-extrait` :
  **721 629 notices** (interrogé le 2026-07-03). C'est donc un **extrait**,
  pas la base complète. L'écart (~30 %) sera chiffré précisément en T2 ;
  sa nature (quelles notices manquent ?) reste à comprendre si nécessaire.

### Champs pertinents repérés (noms API, à mapper avec le CSV en T1)

| Champ API | Usage pour le projet |
|---|---|
| `auteur` | champ principal : porte les qualificatifs d'attribution |
| `precisions_sur_l_auteur` | précisions en texte libre |
| `ancienne_attribution` | attributions révisées — champ dédié ! |
| `ecole_pays` | école / pays |
| `domaine` | filtrage du périmètre (peinture, dessin, sculpture…) — champ multivalué |
| `denomination` | type d'objet |
| `nom_officiel_musee`, `ville`, `region`, `departement` | localisation |
| `code_museofile` | identifiant musée (jointure possible avec Muséofile) |
| `coordonnees` | geo_point_2d → **cartographie possible sans géocodage** |
| `reference` | identifiant de notice → lien vers la fiche POP |
| `sujet_represente`, `precisions_sujets_representes` | garde-fou « présumé » côté sujet |

### La donnée est plus structurée qu'espéré

Le champ `auteur` suit une convention de qualificatifs entre parenthèses :

- `MODERNO (attribué)`
- `LESCHER (attribué, ?)`
- `LOMBARD (?, attribué)`
- `anonyme (attribué, attribué)` — doublons possibles dans les qualificatifs

C'est une convention documentaire (méthode Joconde), pas du texte libre :
la détection pourra s'appuyer dessus, en plus de la recherche plein texte.

### Premiers ordres de grandeur (sur l'extrait API, 721 629 notices)

Recherche plein texte dans le champ `auteur` :

| Motif | Notices |
|---|---|
| « attribué » | 16 860 |
| « atelier de » | 1 390 |
| « école de » | 500 |
| « entourage de » | 156 |
| « anciennement attribué » | 1 (mais champ dédié ci-dessous) |
| `ancienne_attribution` non vide | **25 906** |

Lecture : la matière existe, et le champ dédié `ancienne_attribution` est plus
riche que la mention textuelle. Ces chiffres sont des minima sur un extrait —
le comptage de référence se fera sur le CSV complet (T3).

## T1 — Structure du CSV et mapping des champs (2026-07-03)

CSV téléchargé le 2026-07-03. **Version confirmée** par les en-têtes HTTP du
serveur (vérifié le 2026-07-05) : `Last-Modified: Wed, 01 Jul 2026 01:37:45 GMT`,
`Content-Length: 1 191 002 260` octets (identique à l'octet à notre fichier),
`ETag: 4cc723bb0c3aebdecd2245b7644fb00a`. **La photo de référence du projet est
donc la version du mercredi 1er juillet 2026.** Le CSV est mis à jour chaque
mercredi 6h : toute publication doit dater son chiffre (« données arrêtées au
1er juillet 2026 »). Caractéristiques : **1,19 Go, 67 colonnes, séparateur `|`**,
en-têtes identiques aux noms de champs de l'API. La nomenclature ODS liste 77 intitulés (dont des champs propres à la
plateforme POP absents du CSV : crédits photo, copyright, historique…).
Les champs multivalués utilisent `;` comme séparateur interne (ex. `Domaine` :
`archéologie;gallo-romain;numismatique`).

### Champs au cœur du projet (détection de l'incertitude)

| Colonne CSV | Étiquette Joconde | Champ API | Définition (nomenclature) |
|---|---|---|---|
| `Auteur` | AUTR | `auteur` | Auteur — porte les qualificatifs entre parenthèses |
| `Precisions_sur_l_auteur` | PAUT | `precisions_sur_l_auteur` | Précisions auteur (texte libre) |
| `Ancienne_attribution` | ATTR | `ancienne_attribution` | Ancienne attribution — champ dédié |
| `Ecole_pays` | ECOL | `ecole_pays` | École-pays |

### Champs de garde-fou (piège « présumé » côté sujet)

| Colonne CSV | Étiquette | Champ API |
|---|---|---|
| `Sujet_Represente` | REPR | `sujet_represente` |
| `Precisions_sujets_representes` | PREP | `precisions_sujets_representes` |
| `Titre` | TITR | `titre` |

### Champs de contexte (périmètre, localisation, restitution)

| Colonne CSV | Étiquette | Usage |
|---|---|---|
| `Reference` | REF | identifiant → lien POP `pop.culture.gouv.fr/notice/joconde/{ref}` |
| `Domaine` | DOMN | périmètre (peinture, dessin, sculpture…) — multivalué `;` |
| `Denomination` | DENO | type d'objet |
| `Nom_officiel_musee` | NOMOFF | musée |
| `Code_Museofile` | MUSEO | identifiant musée (jointure Muséofile possible) |
| `Ville` / `Departement` / `Region` | VILLE_M / DPT / — | localisation administrative |
| `coordonnees` | — (ajout POP) | lat, lon → cartographie sans géocodage |

Lecture pandas validée : `pd.read_csv(sep='|', usecols=…, chunksize=…)` passe
sans erreur sur les premières lignes ; le comptage complet et le profilage sont
l'objet de T2.

## T2 — Profil du CSV complet (2026-07-03)

Obtenu par `src/profile_data.py` (rapport brut : `data/exports/profil.txt`).

### Volumétrie

- **1 023 705 notices**, 555 musées distincts (`Code_Museofile`).
- Écart avec l'extrait API (721 629 notices le 2026-07-03) : **302 076 notices,
  soit 29,5 % de la base absents de l'API**. L'annonce « + 1 000 000 » de
  data.gouv est exacte ; le comptage de référence se fait bien sur le CSV.

### Taux de remplissage des champs cœur

| Champ | Renseigné | Taux |
|---|---|---|
| `Auteur` | 841 953 | 82,2 % |
| `Precisions_sur_l_auteur` | 457 756 | 44,7 % |
| `Ecole_pays` | 416 091 | 40,6 % |
| `Ancienne_attribution` | 27 266 | 2,7 % |

À noter : ~18 % des notices n'ont **pas** de champ Auteur. Une absence d'auteur
n'est pas un marqueur d'incertitude au sens du projet (beaucoup d'objets
archéologiques ou ethnologiques n'ont pas d'auteur attendu) — mais c'est un
chiffre de contexte intéressant pour le récit.

### Champs de contexte

- `Domaine` : 100 % renseigné — le filtrage de périmètre est fiable.
- `coordonnees` : **99,8 %** renseigné — la cartographie couvrira presque tout.
- `Code_Museofile` : 100 % — les agrégats par musée (avec total versé) sont sûrs.

### Répartition par domaine (multivalué : une notice peut compter plusieurs fois)

Top : dessin 300 156 · arts graphiques 152 140 · estampe 141 891 ·
photographie 109 472 · archéologie 105 889 · peinture 91 450 ·
ethnologie 76 745 · céramique 57 141 · sculpture 50 139…

**Périmètre pressenti** (au moins un domaine parmi peinture / dessin /
sculpture / estampe) : **583 346 notices, 57,0 % de la base**.

## T3 — Détecteur v0 et taux de base (2026-07-03)

Lexique : `src/markers.py` (13 familles, 3 catégories : doute / copie / révision).
Comptage : `src/count_markers.py` → `data/exports/comptages.csv` et
`comptages_domaines.csv`.

### Taux de base (les deux dénominateurs, décision utilisateur)

| Agrégat | Notices | / toute la base | / notices avec auteur |
|---|---|---|---|
| Au moins un marqueur de **doute** | 29 726 | 2,90 % | 3,53 % |
| « d'après » (copie, classé à part) | 22 564 | 2,20 % | 2,68 % |
| Champ `Ancienne_attribution` renseigné (révision) | 27 266 | 2,66 % | 3,19 % |

Périmètre peinture/dessin/sculpture/estampe : 23 939 notices avec doute
sur 583 346 (4,10 %) — soit **80,5 % de tout le doute détecté**.

### Ventilation du doute (familles principales)

attribué à 18 008 · atelier de 5 558 · école de 2 865 · ? 2 731 ·
manière de 703 · entourage de 503 · genre de 303 · suiveur de 80 · présumé 4.

### Taux de doute par domaine (≥ 10 000 notices, top)

peinture **6,00 %** · dessin 4,72 % · artisanat-industrie 4,55 % ·
histoire 4,49 % · gallo-romain 3,92 % · … · sculpture 2,27 % · estampe 2,22 %.
La peinture est bien le domaine le plus « douteux », mais le dessin fournit le
plus gros volume (14 170 notices).

### Constats et pièges rencontrés en construisant le détecteur

- **Piège « ? » de dates (corrigé)** : dans `Auteur`, la parenthèse peut contenir
  des dates incertaines — `Aquaviva Oscar (19..-19..?)`. Le motif exclut
  désormais les parenthèses contenant un chiffre : 9 710 → 2 731 détections
  (~72 % du signal brut était du bruit de dates !).
- **Piège « école des Beaux-Arts » (corrigé)** : dans `Precisions_sur_l_auteur`,
  les biographies citent les écoles-institutions. « école de » n'est plus cherché
  que dans `Auteur` et `Ecole_pays` ; le qualificatif `(école)` — vu dans
  `PALMA Giovane (école)` — est ajouté. Perte assumée : les « école de Rembrandt »
  éventuels en texte libre de PAUT.
- **« présumé » est quasi absent des champs auteur (4 cas)** : le piège annoncé
  (« portrait présumé de X ») vit dans Titre/Sujet_represente, champs que le
  détecteur ne fouille pas. Le garde-fou était le bon : ne pas fouiller ces champs.
- **« anciennement attribué » en texte libre est rarissime (7 cas)** : cette
  information passe par le champ dédié `Ancienne_attribution` (27 266). La
  structure de la base est plus fiable que son texte.
- **« ATELIER DE MOULAGE », « ATELIER DE ROME »** : « atelier de » peut être un
  nom d'atelier de production (moulages de musées !), pas un doute sur un maître
  → à surveiller de près en T4.
- Graphies sans accent confirmées : « attribue à Fleuret » (sic) détecté.

## Cycle v1 — Recomptage après reformulation (2026-07-04)

| Agrégat | v0 | v1 | Δ |
|---|---|---|---|
| Au moins un marqueur de doute | 29 726 | **25 220** | −4 506 (bruit retiré) |
| — taux base entière / avec auteur | 2,90 % / 3,53 % | **2,46 % / 2,99 %** | |
| attribué à | 18 008 | 17 926 | −82 (doctrine « attribué, d'après ») |
| ? | 2 731 | 2 213 | −518 (dates `(?-1996)`) |
| école de | 2 865 | 2 093 | −772 (écoles nationales inversées) |
| atelier (qualificatif) | 5 558 | **1 759** | la famille la plus corrigée |
| Atelier de X en nom d'auteur (écarté) | — | 1 123 | population chiffrée à part |

Le périmètre beaux-arts concentre 21 161 des 25 220 doutes (83,9 %).
Peinture : 5,33 % de taux de doute (v0 : 6,00 %).

## P2-T3 — Deux découvertes majeures à l'export (2026-07-05)

### 1. La monoculture de Nice fausse le chiffre national

Le muséum d'histoire naturelle de Nice arrive **en tête du doute national**
(5 791 notices, devant le Louvre) — et ces 5 791 doutes sont **un seul auteur**,
`Barla Jean-Baptiste (1817-1896) (attribué à)` : des planches naturalistes
(mycologie, botanique) où un catalogueur a appliqué « (attribué à) » à toute
une collection. Classées en « dessin », elles passent le filtre beaux-arts.

**À lui seul, ce cas = 23,6 % du doute national (5 791 / 24 507).** Or c'est un
singleton : la 2e concentration (musée Westercamp, 382) est 15× plus petite,
et après Barla tout est sous 2 %. Ce n'est pas un phénomène, c'est un artefact
documentaire — un même geste de catalogage répété des milliers de fois.
Hors cas Barla, le doute national tombe à **~18 716 notices**.

Enjeu : ni la carte ni aucun classement ne doivent laisser un musée écraser
tous les autres. Décision utilisateur requise (voir docs/decisions.md).

### 2. Le cas Alençon est absent des données ouvertes — cause vérifiée (2026-07-05)

Le musée des beaux-arts et de la dentelle d'Alençon (M0694), point d'entrée
narratif du projet : **109 notices versées, 0 doute détecté**.

**Cause établie par examen des données** : le musée n'a versé dans Joconde que
sa collection de **dentelle** — les 109 notices sont à ~95 % dentellerie /
costume / textile (titres réels : « Mouchoir », « Dessin pour feuille
d'éventail »). **Aucun tableau.** Ses peintures — dont la « tête de gorgone »
et « le naufragé » liées au cycle du Radeau — existent dans la **base régionale
des musées de Normandie** (`collections.musees-normandie.fr`, base distincte),
non reversée au niveau national.

Recoupements confirmant l'absence :
- sur les **525 notices Joconde mentionnant Géricault**, aucune à Alençon ;
- sur **toutes** les notices au titre « gorgone/naufragé/méduse/radeau »,
  aucune à Alençon.

Correction d'une formulation antérieure trop rapide (« pas dans les données ») :
la cause exacte est un **versement partiel** (dentelle versée, beaux-arts non).
C'est **l'illustration vivante de la limite centrale du projet** : le cas
fondateur est lui-même invisible dans l'open data nationale.

Note utile pour le récit : le doute « à la Géricault » EST réel et détectable
ailleurs dans Joconde — ex. Besançon (M0332), `Géricault (genre de)` sur un
« Naufrage », plus de vraies études pour le Radeau. Le phénomène existe ; c'est
Alençon qui manque, faute de versement.

### Vérification approfondie (2026-07-05, à la demande de l'utilisateur)

La section « beaux-arts » fait pourtant partie intégrante du musée
(museedentelle.cu-alencon.fr) : l'absence de tableaux méritait un contrôle
serré. Trois recherches convergentes sur le CSV complet :
- par **code muséofile** `M0694` (toutes villes confondues) : **109 notices**,
  toutes à Alençon → pas de second code caché ;
- par **nom de musée contenant « dentelle »** : 109 notices, uniquement M0694 →
  un seul établissement ;
- domaines beaux-arts parmi ces 109 : **1 peinture, 2 beaux-arts, 3 sculpture,
  0 estampe** — le reste est dentellerie/costume/textile.

**Confirmation par source indépendante** : l'API du ministère
(`data.culture.gouv.fr`, dataset `base-joconde-extrait`) renvoie
**exactement 109** notices pour `code_museofile='M0694'`. Le chiffre est stable,
ce n'est pas un artefact de notre CSV.

**Est-ce possible / normal ? Oui.** Le versement dans Joconde est volontaire et
souvent partiel : un musée numérise et verse d'abord une collection, pas
forcément toutes. Ici la logique est même lisible — Alençon est mondialement
connu pour son **Point d'Alençon** (dentelle, patrimoine immatériel UNESCO) :
le musée a versé sa collection phare, la dentelle, et pas (encore) ses
peintures. Ces dernières sont numérisées, mais dans la **base régionale de
Normandie**, système distinct non agrégé à Joconde. C'est un cas d'école du
versement sélectif — le socle même de la limite affichée du projet.

## P2-T1 — Recouvrements entre catégories (2026-07-05)

Source : `src/count_overlaps.py` → `data/exports/recouvrements.json`.

**66 911 notices (6,54 % de la base) portent au moins un marqueur**, toutes
catégories confondues. Répartition (chaque notice comptée une seule fois) :

| Combinaison | Notices |
|---|---|
| révision seule | 19 873 |
| doute seul | 19 690 |
| copie seule | 19 279 |
| **doute + révision** | **4 724** |
| copie + révision | 2 539 |
| doute + copie | 672 |
| les trois | 134 |

Contrôle de cohérence : 19 690 + 4 724 + 672 + 134 = 25 220 = total doute v1 ✓.

Constats :
- **Près d'1 doute sur 5 (19 %) porte aussi une ancienne attribution** : la
  notice dit à la fois « on n'est pas sûr » et « on a déjà changé d'avis ».
  Ce croisement est peut-être la matière narrative la plus riche du projet.
- Les co-occurrences entre familles de doute sont marginales (max :
  attribué × ? = 128 notices) — les familles sont presque disjointes, la
  ventilation par famille est donc saine.
- Les trois catégories ont des poids étonnamment proches (~19-20 000 chacune
  en exclusif) : trois récits d'égale ampleur.

## T5 — Pièges confirmés par la vérification manuelle (2026-07-04)

206 lignes jugées par l'utilisateur (176 vrai / 28 faux / 2 incertain).
Classes de faux positifs identifiées par ses commentaires :

1. **Ateliers de production donnés comme auteurs assumés** : `Atelier de
   Pistillus`, `ATELIER DU CENTRE DE LA GAULE (céramiste)`, `Atelier du jubé
   de la cathédrale de Strasbourg` — l'atelier EST l'auteur, aucun doute.
2. **Studios d'imprimeurs/photographes** : `Ateliers de reproductions
   artistiques`, `Moulin (Atelier photographique)`.
3. **Mentions biographiques dans Precisions_sur_l_auteur** : « entra dans
   l'atelier de formation… », « il est un des suiveurs du Pérugin » — la bio
   parle du parcours de l'artiste, pas de l'attribution de l'œuvre.
4. **École nationale sous forme inversée** : `Hollande École de (École
   hollandaise)` dans le champ Auteur — c'est le piège « école française »
   de T1, sous un déguisement inattendu. Signal d'exclusion : la parenthèse
   `(École …)` qui suit.
5. **`?` de date de naissance** : `(?-1996)` — la correction T3 n'excluait que
   les chiffres avant le `?`, pas après.
6. **« présumé » sur une autre œuvre citée en bio** : « on lui attribue aussi
   un portrait présumé de son époux ».
7. Les faux positifs arrivent **en grappes** : un même auteur mal formaté
   (Der Balian Sarkis) = toutes ses œuvres fausses. Corriger un motif élimine
   des grappes entières.
8. Curiosité à documenter : `anonyme (attribué)` — « attribué à… anonyme »
   (traité en « incertain », hors calcul, décision utilisateur).

## Phase 3 — Compter le doute PAR AUTEUR : deux corrections de repérage (2026-07-07)

Constaté en construisant la liste vedette de l'entrée « par l'artiste »
(voir docs/decisions.md, 2026-07-07). Compter le doute **autour d'un nom**
(nom-pivot = segment du champ Auteur, parenthèses retirées) fait apparaître
deux pièges qu'une première sonde artisanale a révélés — et que le détecteur
canonique `markers.py` évite déjà :

1. **Le qualificatif n'est pas toujours entre parenthèses.** Une sonde qui ne
   lit le doute qu'entre parenthèses **sous-compte** : `INGRES Jean-Auguste-
   Dominique attribué à` s'écrit souvent **hors parenthèses** (≈ 189 occurrences).
   Effet mesuré pour Ingres : **13 doutes (parenthèses seules) → 204 (champ
   entier)**. Règle : chercher le marqueur dans **tout le segment**, comme le
   fait `markers.py` (`str.contains` sur le champ). Une détection par-auteur
   doit reprendre cette logique, pas se limiter aux parenthèses.

2. **Les écoles nationales se déguisent en « école ».** `(école allemande)`,
   `(école flamande)`, `(école italienne)` sont des **nationalités**, pas
   « école de [maître] ». Une sonde qui compte le mot « école » **sur-compte** :
   pour Dürer, **161 (mot « école ») → 19 (canonique)**, l'écart étant
   quasi entièrement des `(école allemande)`. Le motif `ecole_de` de v2 exige
   « école **de** X » (ou `(école)` seul en fin de token) et exclut la forme
   nationale — c'est le même piège « école française » de T1/T5, ici côté
   comptage par auteur.

**Granularité du nom-pivot (à traiter avant l'export `artistes.json`)** —
le rattachement d'un doute à « un maître » n'est pas trivial :
- **homonymes** : `BUGATTI Rembrandt` (le sculpteur, 82 notices) n'est pas
  Rembrandt le peintre → exclusion explicite nécessaire ;
- **familles sous un même nom** : Bruegel (l'Ancien / le Jeune / Jan),
  Cranach (l'Ancien / le Jeune), Fragonard (Jean-Honoré vs son fils
  Alexandre-Évariste, majoritaire en volume) — à désambiguïser par
  prénom/génération ;
- **variantes de graphie d'une même personne** : `LE PRIMATICE` = `PRIMATICCIO
  FRANCESCO`, `LE TITIEN` = `VECELLIO TIZIANO` (français ↔ italien) — à
  réconcilier, sous peine de fragmenter le comptage d'un maître ;
- **absence de prénom** : `CLOUET (attribué à)` ne se rattache ni à Jean ni à
  François. Vérifié pour Clouet : pas de réservoir « sans prénom » (le doute
  Clouet est porté par François, 105, pas par Jean, 15).

- **Formule non répertoriée repérée** : `(attribution incertaine)` (vu chez
  Corot) — hors des familles du lexique v2. À examiner sur toute la base pour
  décider si elle rejoint la famille « attribué à » (récit en réserve).

## Circulation des JSON vers le front (P3-T0, 2026-07-07)

Le front SvelteKit (dossier `web/`) est statique et ne lit **jamais** la base :
il consomme uniquement les JSON agrégés de `data/exports/web/` (règle « jamais
la base entière dans l'application »). Ces JSON sont des artefacts générés par le
pipeline Python (`src/build_*.py`), donc **non versionnés** — ni côté `data/`,
ni côté front.

Frontière unique et sens de circulation : Python écrit `data/exports/web/*.json`
→ `npm run sync:data` (web/scripts/sync-data.js) les copie dans
`web/static/data/` → servis par le front en `/data/…`. Après tout nouvel export,
resynchroniser. `web/static/data/` est dans le `.gitignore` du front. Aucun autre
couplage back ↔ front que ces fichiers.

## Exemples d'œuvres dans artistes.json — structure enrichie (2026-07-11)

Pour la vitrine « Œuvres » (décision du même jour), `build_artistes.py` exporte
désormais, par maître :

- `exemples` : jusqu'à 9 œuvres réelles, **une par famille de doute présente, deux
  pour la famille dominante**, chacune avec son **`code` de famille** (le front ne
  re-parse jamais les extraits), `reference` (lien POP), `titre`, `musee`, `ville`
  et `extrait` (le segment du champ Auteur, **verbatim**). Ordre d'export = ordre
  canonique de l'échelle (`DOUTE_PAR_NIVEAU`).
- `exemple_copie` : une œuvre « d'après » (même structure, sans code), pour donner
  une preuve au bloc « À part ». Présente pour les 27 maîtres.

Les exemples sont les **premiers rencontrés dans le CSV**, pas choisis (voir
methode-et-limites.md). Champs `titre`/`musee`/`ville` parfois absents dans la
base → `null` dans le JSON, repli géré côté front (« Sans titre »). Les titres
sont souvent saisis en capitales : affichés tels que publiés, jamais réécrits.
Aucun comptage modifié par cet enrichissement (vérifié à la régénération).

## Carte par maître — audit de dispersion (2026-07-12)

Audit préalable au « palier données » de la carte (roadmap P3-T1). Scan du CSV
complet, doute **seul** (ni ferme, ni copie) ventilé par musée détenteur, sur
5 maîtres témoins. But : savoir si la donnée permet une carte honnête avant d'en
coder une.

Constats (chiffres mesurés le 2026-07-12) :

- **Le champ `musees` d'`artistes.json` est inexploitable pour la carte** :
  `build_artistes.py` l'alimente pour tout segment du maître, **catégories
  confondues** (ferme + doute + copie). Le Brun y affiche 64 musées ; le doute
  seul n'en concerne que 19. Il faut un décompte du doute par musée, à part.
- **Concentration très forte.** Un seul musée porte l'essentiel du doute de
  chaque maître : Le Brun 89 % au Louvre (276/310), Le Primatice 97 % au Louvre
  (262/269), Ingres 98 % au musée Ingres Bourdelle de Montauban (200/204),
  Rembrandt 90 % au Louvre (169/187), Rodin 96 % au Louvre (78/81 — et non au
  musée Rodin). Une carte « taille ∝ nombre » donnera un point géant et une
  poussière autour : à traiter au design (échelle en racine, taille plancher
  visible, valeur au survol), et à assumer en légende — c'est une **dispersion**,
  pas un palmarès.
- **Peu de points pour certains maîtres** : Ingres 3 musées, Rodin 4, Le Primatice
  6. Sous un seuil (~3 musées), une carte apporte peu : prévoir un repli (ne pas
  afficher la carte, ou la remplacer par une mention « conservé surtout à … »).
- **Couverture géographique bonne** : sur ces 5 maîtres, 0 musée sans coordonnées,
  0 en outre-mer. Au global (`musees.json`), 548/555 musées géolocalisés ; les 7
  sans coordonnées sont des **codes fantômes sans nom** (`M0000`, `X0000`…), pas
  de vrais détenteurs. 6 musées en outre-mer (Guadeloupe, Réunion, Martinique,
  Guyane) existent dans la base : à prévoir dans le fond de carte ou à écarter
  explicitement.
- **Les coordonnées sont au grain musée** : le champ `coordonnees` du CSV est
  celui du musée (constant par `Code_Museofile`), porté sur chaque notice. Prendre
  la première vue par code est correct et cohérent avec « 1 point = 1 musée ».
  La source géo reste **secondaire** (localise le détenteur, jamais l'œuvre, et
  ne compte rien).

## Pièges métier connus (à vérifier sur les données réelles)

- « présumé » porte souvent sur le **sujet représenté** (« portrait présumé de X »),
  pas sur l'auteur → source de faux positifs, garde-fou prévu dans le détecteur.
- « d'après X » = le plus souvent copie assumée d'après un modèle → classé à part.
- Graphies multiples attendues (« attribué à », « attr. », « ? »…) : saisies par
  des musées différents sur des décennies.
- **`Ecole_pays` : « école française » = nationalité, pas un doute** (précision
  utilisateur, 2026-07-03). Le marqueur de doute « école de [artiste] » se trouve
  plutôt dans `Auteur`. Le détecteur (T3) devra distinguer « école de + nom
  d'artiste » (doute) de « école + adjectif de nationalité » (classification).
