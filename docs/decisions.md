# Décisions

Chaque décision est datée et motivée. Les plus récentes en haut.

## 2026-07-08 — « Les presque » : barres → nuage de points à grille fixe (décision utilisateur)

Les barres horizontales (livrées le jour même) corrigeaient la galaxie mais deux
défauts à l'usage : (1) **pas de comparabilité entre maîtres** — chaque maître
n'affiche que *ses* familles présentes, la grille change à chaque artiste, chaque
graphe est un îlot ; (2) **pas de repère de mesure stable** — barres normalisées à
la largeur du conteneur, donc une barre « pleine » d'un petit maître paraît aussi
grande que celle d'un gros. On ne lit pas les volumes réels.

**Décision : remplacer les barres par un nuage de points (scatter) sur une grille
FIXE et COMMUNE.** C'est la grille stable qui rend les maîtres comparables —
objectif éditorial central de la vue.
- **Axe X** : les familles de doute, **toujours toutes, même ordre** (ordre
  canonique du lexique v2). « Présumé » retiré : absent des 27 maîtres (colonne
  vide par construction) → **8 colonnes**.
- **Axe Y** : volume, de 0 à un **plafond commun = 240** (la plus grande valeur de
  famille sur les 27, « école de » Le Brun). **Calculé côté front** depuis
  `artistes.json` (max sur les 27), pas en dur, pas de dépendance pipeline.
- **1 point par famille** à la hauteur de son volume ; zéro = pas de point ;
  taille **légèrement** croissante avec le volume (appui, pas la mesure) ;
  couleur par famille, groupée par teinte de niveau + libellés de niveau au-dessus
  des groupes (la lecture « échelle du doute » survit) ; graduations
  60/120/180/240 ; **échelle linéaire** (honnêteté des volumes) ; survol = compte
  exact ; libellés d'axe raccourcis, technique complet au survol.

**Justification de la forme (position sur Y commun plutôt que taille de bulle) :**
l'œil compare précisément des **hauteurs sur une échelle commune**, mais **mal des
aires de cercles**. L'échelle Y fixe et partagée permet de voir d'un coup que le
doute autour de Le Brun (pic « école » à 240) est d'un autre ordre que celui
d'Andrea del Sarto (« école » à 57) — les deux se lisent sur la même règle. Le
grossissement léger ajoute une charge narrative (le volume « pèse ») sans remplacer
la mesure. Compromis lisibilité/récit adapté au data-journalisme.

**Coût assumé (signalé) :** les familles à faible volume et les petits maîtres
collent au plancher sous un plafond à 240 — c'est la vérité (le doute se concentre
sur « attribué à » + « école de ») ; contré par le cadrage (sous-titre disant le
plafond, graduations, survol, plancher de taille de point), pas en trichant sur
l'échelle. La galaxie reste archivée dans `lib/GalaxieMaitre.svelte`.

## 2026-07-08 — « Les presque » : galaxie abandonnée, barres + carte par maître (décision utilisateur)

Refonte de la 1re dataviz après examen de la v1 (galaxie + détail) et du document
`docs/dataviz-les-presque.md`.

**Galaxie abandonnée dans cette vue.** L'encodage retenu était « 1 bulle = 1
famille » (4-5 ronds par maître) : un schéma moléculaire, pas une constellation ;
l'œil compare mal des aires de disques ; la vue n'apportait rien qu'une barre ne
montre mieux. La « vraie constellation » (1 point = 1 œuvre) est **reportée en
réserve, sur une branche séparée** — hors périmètre de cette vue.

**Trois angles complémentaires par maître** (le quoi / le combien / le où) :
1. **Détail** (existant) — formules, exemples POP, copies à part. Conservé ;
   labels trop techniques à reformuler plus tard (non prioritaire).
2. **Barres horizontales** (remplace la galaxie) — une barre par famille, longueur
   ∝ notices. Montre « la forme du doute » propre à chaque maître. Aucune donnée
   nouvelle requise.
3. **Carte par maître** (nouveau) — voir ci-dessous.

**Pourquoi la carte devient possible ici alors qu'une carte globale était exclue.**
Une carte de tous les doutes (~18 000 points) était écartée : trop dense et
malhonnête (inviterait à comparer les musées sur des comptages bruts, interdit vu
les versements inégaux). Une carte **par maître** lève le piège : quelques dizaines
de points, et on ne compare plus les musées entre eux — on montre **où se disperse
le doute autour d'un seul nom**. Angle neuf : la géographie du doute d'un maître.

**Grain honnête retenu (constaté sur les données) :** une notice n'a pas de
coordonnées propres, elle est localisée par son **musée détenteur**
(`Code_Museofile` → coord dans `musees.json`, couverture 98,7 %). Donc **1 point =
1 musée**, taille ∝ nb d'œuvres douteuses de ce maître. Mesure de dispersion :
~1 doute/musée pour la plupart (doute très semé), seule concentration nette = Le
Primatice (Fontainebleau). Caveat page méthode : la taille reflète le nombre
d'œuvres douteuses **de ce maître** dans ce musée, jamais une comparaison de
catalogage entre musées.

**Dépendance données à traiter avant la carte :** le champ `musees` d'`artistes.json`
confond ferme/copie/doute (« Raphaël 108 musées » pour 28 doutes) — inexploitable.
Il faut enrichir `build_artistes.py` : par maître, la liste des **musées du doute
+ comptes**.

**Technique de carte : D3-geo auto-hébergé** (arbitrage utilisateur 2026-07-08).
GeoJSON France + départements en open data (licence ouverte, cité comme source
secondaire d'affichage, jamais de comptage), dans `static/`, rendu SVG dans Svelte,
**aucune tuile externe / aucun serveur**, pré-rendable. Écartés : Leaflet + tuiles
OSM (dépendance live à un service tiers, hors esprit « source unique », réactive le
réflexe de comparer les lieux) ; Leaflet sans tuiles (bancal, D3 fait mieux).

**Ordre de construction retenu : barres → (palier données) → carte** (arbitrage
utilisateur). Les barres d'abord car sans donnée nouvelle et retirent la galaxie
tout de suite ; la carte ensuite car elle porte la dépendance données + le nouvel
outil. Détail conservé en l'état.

## 2026-07-07 — Style du front : rejet du look générique (remarque utilisateur, indicative)

Socle P3-T0 validé sur le fond. **Remarque à titre indicatif, pas un arbitrage à
appliquer maintenant** : l'utilisateur ne veut pas de la présentation générique
que produit Claude par défaut (« toutes les applications créées par Claude ont la
même allure »). Ce n'est pas le sujet au stade actuel (on construit les dataviz),
mais c'est consigné pour plus tard.

Conséquence pratique : les tokens et la mise en page actuels
(`web/src/lib/styles/tokens.css`, coquille) sont **provisoires, fonctionnels**,
non une direction artistique. Quand le style deviendra le sujet (après les
dataviz), proposer une **identité visuelle affirmée et singulière**, pas les
réglages par défaut. Ne pas investir dans le polish visuel d'ici là.

## 2026-07-07 — Stack du front : SvelteKit retenu (décision utilisateur, phase 3)

Le choix de socle laissé en suspens à P3-T0 (SvelteKit recommandé vs vanilla +
Vite) est tranché : **SvelteKit**, en **build statique** (`adapter-static`,
`prerender`). Aucun serveur applicatif : le front reste un site statique qui
consomme les JSON déjà exportés dans `data/exports/web/` (règle non négociable
« jamais la base entière dans l'application »).

Pourquoi SvelteKit plutôt que du vanilla + Vite :
- **Le routage intégré sert directement la structure éditoriale.** Chaque brique
  (« Les presque », le décodeur de l'échelle, les révisions, la carte) et la page
  « méthode et limites » deviennent des routes de même rang — la règle « méthode
  au même rang que le reste » se lit dans l'arborescence du code.
- **Composants + coquille partagée** (en-tête, navigation entre briques, tokens
  de style des 3 niveaux) sans réinventer un système de gabarits à la main.
- **Cohabite bien avec D3.js** : Svelte gère le DOM et l'état, D3 les échelles et
  la géométrie ; pas de conflit de propriété du DOM si on laisse D3 calculer et
  Svelte rendre.
- **Reste lisible pour un développeur intermédiaire** (pièce de portfolio) : la
  syntaxe Svelte est proche du HTML/CSS/JS, moins de cérémonie que React.

Coût assumé : une chaîne de build Node à côté du pipeline Python (`uv`). Front
isolé dans un dossier dédié (voir roadmap P3-T0). Les JSON restent la seule
frontière entre le back Python et le front — aucun couplage au-delà.

## 2026-07-07 — Export « Les presque » : désambiguïsation → liste vedette à 27 (mise en œuvre)

Formalisation de l'entrée « par l'artiste » :
- `src/markers.py` : ajout d'une fonction publique `famille_segment(segment,
  en_beaux_arts)` — catégorise **un** segment du champ Auteur (copie > écarté >
  doute > propre) en réutilisant les motifs du lexique v2, sans diverger.
  35 tests toujours verts.
- `src/build_artistes.py` → `data/exports/web/artistes.json` (44 Ko) : par maître,
  `propre` / `doute` / `copie`, ventilation par famille **et** par niveau (échelle
  P2-T2), nombre de musées, et une notice réelle par famille (lien POP).

**Désambiguïsation des trois familles †** (annoncée « avant l'export »), faite
sur les nom-pivots réels :
- **Fragonard** : Jean-Honoré isolé = **31** doutes (son fils Alexandre-Évariste
  = 3) → conservé.
- **Cranach l'Ancien** (Lucas le Vieux + l'Ancien) = **17** → sous 20 (les 30
  incluaient le fils, Lucas le Jeune, 13) → **retiré**.
- **Bruegel l'Ancien** (Pieter I + le Vieux) ≈ **15** → sous 20 (les 51 étaient
  surtout **Jan** Brueghel, ~23, un autre homme) → **retiré**.

**Conséquence : la liste vedette publiée passe de 29 à 27 maîtres.** Ce n'est pas
une exception au critère mais le critère ≥ 20 appliqué au bon niveau (le maître
isolé, pas la famille). Réserve laissée à l'utilisateur, sans arbitrage par
défaut (on garde les 27) : réintégrer Bruegel/Cranach comme « famille » assumée,
ou échanger « Bruegel l'Ancien » contre **Jan Brueghel** (~23, qualifie seul).

## 2026-07-07 — Liste vedette V1 : 29 maîtres de référence (décision utilisateur, phase 3)

Première brique de l'entrée « par l'artiste » (« Les presque ») : une **sélection
vedette** de maîtres mis en avant sur la page, distincte du moteur de recherche
(qui, lui, porte sur tous les noms de la base).

**Critère unique retenu : maître de référence ET ≥ 20 notices de doute (hors copie).**
Le doute n'est pas exigé pour la notoriété, mais il l'est pour la mise en avant
vedette : sans ≥ 20 « presque », il n'y a pas de matière à montrer. La curation
de notoriété est assumée et publiable (panthéon lisible, primitifs → modernes) ;
le seuil de 20 la rend non arbitraire.

**Comment le doute est compté (la fabrique du chiffre).** Comptage **par segment**
du champ `Auteur` (séparateur `;`), rattaché au nom-pivot (parenthèses retirées,
casse/accents normalisés), avec les **regex réelles de `markers.py` v2** :
copie (« d'après ») l'emporte ; familles écartées (atelier-nom, école-lieu,
atelier hors beaux-arts) exclues ; sinon doute si une famille de doute matche ;
sinon propre. Deux corrections de repérage décisives par rapport aux sondes
initiales (parenthèses seules) :
- le doute est cherché dans **tout le segment**, parenthèses ou non — une sonde
  « entre parenthèses seulement » **sous-comptait** (ex. Ingres : « attribué à »
  souvent écrit hors parenthèses → 13 devient **204**) ;
- les **écoles nationales** « (école allemande/flamande) » ne comptent pas
  (nationalité, pas « école de X ») — la sonde initiale **sur-comptait**
  (ex. Dürer : 161 devient **19**).

**Les 29 maîtres retenus** (doute canonique) :
Le Brun 310 · Le Primatice 269 · Ingres 204 · Rembrandt 187 · Michel-Ange 172 ·
Rubens 121 · François Clouet 105 · Annibale Carracci 86 · Rodin 81 · Boucher 78 ·
Andrea del Sarto 63 · Guido Reni 60 · Léonard de Vinci 56 · Le Tintoret 53 ·
Poussin 52 · Simon Vouet 51 · Bruegel l'Ancien 51† · Greuze 49 · Van Dyck 46 ·
Le Corrège 46 · Pierre Mignard 43 · Véronèse 41 · Hyacinthe Rigaud 41 ·
Géricault 40 · Fragonard 37† · Cranach 30† · Raphaël 28 · Ribera 21 · Titien 20.

**Exclusions assumées — maîtres de référence sous le seuil** (le critère fait loi,
choix « A » de l'utilisateur) : Dürer 19, Delacroix 17, Watteau 17, Corot 16,
Jean Clouet 15, Holbein 15, Botticelli 15, Murillo 14, Courbet 11, Millet 11,
puis ≤ 9 (Fra Angelico, Van Eyck, Zurbarán, Mantegna, Giotto, Goya, Vélasquez,
Fouquet, Georges de La Tour, Chardin, Le Caravage, Houdon, Cézanne). **Les
modernes ne sont pas doutés** (Manet, Monet, Degas, Van Gogh, Picasso : 0) —
c'est un constat, pas un oubli.
- **Trois des 20 noms présumés au départ tombent sous le seuil** après correction
  du comptage : Dürer (19), Corot (16), **Jean Clouet (15)**. Ils sortent.
  Vérifié : le doute « Clouet » est porté par **François Clouet (105)**, pas par
  Jean (pas de réservoir « CLOUET sans prénom » qui le sauverait).

**Caveat à traiter avant l'export `artistes.json`** — † trois entrées agrègent
plusieurs personnes sous un même nom-pivot, à désambiguïser (prénom/génération) :
**Bruegel** (l'Ancien / le Jeune / Jan), **Cranach** (l'Ancien / le Jeune),
**Fragonard** (Jean-Honoré vs son fils Alexandre-Évariste, majoritaire en volume).
Repérage à affiner, non cassé. Un raté connu sans effet ici : « Le Greco »
(motif à corriger), de toute façon très sous le seuil.

Chiffres indicatifs, susceptibles de légers écarts quand l'export officiel sera
produit par le pipeline — mais la **méthode est déjà alignée sur `markers.py`**.

## 2026-07-06 — Direction de restitution (décision utilisateur, phase 3)

**Application interactive soutenue par les données, matérialisée par une
dataviz ou une série de dataviz.** Deux refus explicites :
- **pas de scrollytelling / récit défilant** (jugé bancal, nécessiterait des
  enquêtes ; éventuellement plus tard, pas maintenant) ;
- **Alençon n'est pas le fil rouge ni le point de départ** — seulement
  l'étincelle du projet, noté, non central. Ne plus le placer au centre.

Corrige l'orientation « récit guidé » de docs/phase3-options.md : la colonne
vertébrale n'est PAS narrative mais l'interaction avec les données elles-mêmes.
Reste à définir la ou les dataviz (en cours).

## 2026-07-05 — Ouverture du récit : Alençon en incarnation de la limite (décision utilisateur, P2-T4)

Le cas fondateur (Alençon) est absent de Joconde : le musée n'a versé que sa
dentelle (109 notices), pas ses beaux-arts — vérifié et confirmé par l'API du
ministère (docs/donnees.md). **Décision : en faire l'ouverture, assumée comme
telle** — « le cas qui a inspiré ce projet est lui-même invisible dans
l'inventaire national ». On l'illustre via la base régionale de Normandie
(citée comme source secondaire d'illustration, jamais de comptage — la source
canonique reste Joconde). Alençon devient la démonstration vivante de la limite
« les chiffres ne reflètent que ce qui a été versé ».

## 2026-07-05 — Traitement de la monoculture Barla/Nice (décision utilisateur, P2-T3)

Le muséum d'histoire naturelle de Nice (M7050) concentre 5 791 doutes, tous
« Barla (attribué à) » — 23,6 % du doute national, un artefact de catalogage.
**Décision : garder 24 507 comme chiffre vedette (rien n'est caché) ET
divulguer partout le « hors ce cas : 18 716 ».**
Mise en œuvre (src/build_exports.py, exception nommée, pas de seuil auto) :
- `niveaux.json` porte `monoculture_divulguee` + `doute_hors_monoculture` ;
- le musée concerné porte un drapeau `monoculture: true` dans `musees.json` ;
- **règle de restitution : la carte se fonde sur `part_doute`, jamais sur le
  doute brut** — aucun musée ne doit écraser les autres ;
- Barla sera un cas raconté en P2-T4 (le geste de catalogage en série).

## 2026-07-05 — Typologie du doute validée + règles de non-addition (décisions utilisateur)

**Règles de non-addition (P2-T1)** : le chiffre vedette reste le doute seul ;
66 420 publiable uniquement comme « au moins une mention » (union nommée) ;
les trois catégories ne se montrent ensemble qu'en diagramme à intersections ;
le croisement doute + révision (4 615) devient un objet éditorial à part.

**Typologie (P2-T2)** — échelle à 3 niveaux validée (« Presque lui »,
« Autour de lui », « Son style, sans lui », voir docs/typologie.md), avec
trois arbitrages :
1. **atelier restreint aux beaux-arts** (523 notices hors → écartées) ;
2. **écoles-lieux consacrées écartées** (liste versionnée : Fontainebleau,
   Paris, Barbizon, Pont-Aven, Nancy — 222 notices) ;
3. **« ? » au niveau 1** (identification fragile).
Lexique v2 en conséquence ; nouveau doute total : **24 507** (2,39 % / 2,91 %).
Tests étendus à 35 cas (dont restriction domaine).

## 2026-07-05 — Bilan T5bis : recommandation GO (proposition, à valider)

Mini-contrôle T4bis rendu (65/65 verdicts). Résultats des familles reformulées :
- **? : 0 faux sur 15** (16 % en v0) — corrigé ;
- **« Atelier de X » écarté : 15/15 confirmés** — l'exclusion ne jette aucun
  vrai doute, le choix précision-contre-exhaustivité est validé par les faits ;
- **école de : 2/15 (13 %)** — restes : « École de Fontainebleau » (aire
  artistique) et « Nouvelle École de Paris » (mouvement, champ Ecole_pays) ;
- **atelier : 6/20 (30 %)** — restes : des ateliers-entreprises portant le
  qualificatif « (atelier) » (VAUCANSON, JACQUEMIN Frères…). Signal net : les
  faux vivent en ethnologie/artisanat, les vrais en peinture/dessin.

Taux global pondéré (catégorie doute, calcul : src/evaluate_recheck.py) :
- **5,7 % conservateur** (< 10 %) ; 3,3 % ajusté (le faux « attribué,
  d'après » de T4 est prouvé exclu par les tests).

**Recommandation : GO.** Le seuil de phase est franchi. Les faiblesses
résiduelles sont localisées, chiffrées et publiables comme telles ; à traiter
en phase 2 dans la typologie plutôt que par une nouvelle itération de regex :
- la famille « atelier » (7 % du doute) sera marquée « fiabilité moindre,
  sensible au domaine » — option : la restreindre aux domaines beaux-arts ;
- « École de Fontainebleau / de Paris » : liste d'exclusion des écoles-lieux
  consacrées, à trancher en construisant la typologie ;
- taux par famille publiés avec le chiffre global (transparence).

## 2026-07-04 — Lexique v1 : lire la convention, pas le mot (cycle validé par l'utilisateur)

Principe directeur de la reformulation « atelier de » (validé explicitement) :
**le doute Joconde s'écrit en qualificatif entre parenthèses après un nom**
(« COROT (atelier) »), tandis que « Atelier de Pistillus » en nom d'auteur
désigne un créateur assumé. On lit la convention d'écriture des conservateurs,
plus le mot isolé. Choix assumé de **précision contre exhaustivité** : mieux
vaut sous-compter en le disant que sur-compter en silence.

Corrections v1 (détail en tête de `src/markers.py`) :
1. « atelier » : qualificatif seulement, détection segment par segment ;
   garde-fous : nom commençant par « atelier », rôles de production
   (graveur, imprimeur, photographe…). La forme « Atelier de X » en nom
   d'auteur part en catégorie « ecarte » (1 123 notices), chiffrée à part et
   soumise au mini-contrôle : on vérifie qu'on ne jette pas de vrais doutes.
2. « école de » : exclusion de la forme inversée « Hollande École de (École
   hollandaise) » ; qualificatif « (école) » en fin de token seulement.
3. « ? » : la parenthèse ne doit contenir aucun chiffre (« (?-1996) » exclu).
4. Doctrine « (attribué, d'après) » → copie, implémentée en exclusion.

Les verdicts humains de T4 sont figés en **tests automatiques**
(`tests/test_markers.py`, 25 cas) : toute future retouche du lexique doit
repasser devant eux. Recomptage v1 : doute = 25 220 notices (2,46 % base /
2,99 % avec auteur). Mini-contrôle T4bis : 65 lignes
(`data/exports/echantillon_recheck.csv`, graine 202607).

## 2026-07-04 — Bilan T5 : recommandation REFORMULATION (proposition, à valider)

Verdict chiffré (détail : `data/exports/bilan_faux_positifs.csv`, calcul :
`src/evaluate_sample.py`, taux pondérés par le poids réel des familles) :

| Catégorie | Faux positifs pondérés | Lecture |
|---|---|---|
| doute | **17,0 %** | tranche « reformulation » (seuils : <10 go, 10–25 reformulation, >25 no-go) |
| copie (« d'après ») | 0,0 % | impeccable |
| révision (Ancienne_attribution) | 0,0 % | impeccable |

Le 17 % n'est pas diffus : il est concentré dans des familles précises avec
des causes identifiées et corrigeables :
- **atelier de : 64 % de faux** (~3 600 notices) — trois causes : ateliers de
  production donnés comme auteurs assumés (`Atelier de Pistillus`), studios
  d'imprimeurs/photographes, mentions biographiques dans Précisions ;
- **école de : 20 %** — la forme inversée `Hollande École de (École
  hollandaise)` = école nationale, pas un doute (signal d'exclusion net :
  la parenthèse `(École …)` qui suit) ;
- **? : 16 %** — le `?` de date de naissance `(?-1996)` (la correction T3
  n'excluait que les chiffres AVANT le `?`) ;
- le reste tient très bien : attribué à 3,5 %, manière de 0 %, genre de 0 %.

**Recommandation : ni go ni no-go — reformulation ciblée.**
1. Lexique v1 : corriger les trois familles ci-dessus + intégrer la doctrine
   (`(attribué, d'après)` → copie ; mentions biographiques hors jeu) ;
2. recompter la base entière ;
3. mini-contrôle manuel (~60-80 lignes, familles reformulées uniquement) ;
4. si le doute pondéré passe sous 10 % → go définitif.
La matière, elle, est validée : abondante, structurée, et deux catégories
sur trois sortent sans aucune erreur.

## 2026-07-04 — Doctrine de vérification (décisions utilisateur, T4→T5)

Règle générale dégagée par la vérification manuelle des 206 lignes :
**un marqueur ne compte que s'il qualifie l'attribution de l'œuvre de la
notice** — pas s'il apparaît dans une biographie, dans un nom propre (atelier
de production, studio d'imprimeur), ou à propos d'une autre œuvre citée.

Deux points arbitrés explicitement :
- **Qualificatifs combinés `(attribué, d'après)` : « d'après » l'emporte** —
  la notice est une copie, elle sort de la catégorie doute.
- **`anonyme (attribué)` : cas documenté tel quel**, ni vrai ni faux positif
  (verdict « incertain », exclu du calcul des taux mais conservé et montré
  comme curiosité de la base).

## 2026-07-03 — Règle permanente : documenter tout ce qui touche à l'approche (décision utilisateur)

Toute modification ou implémentation concernant l'approche (détection,
échantillonnage, comptage, périmètre…) est documentée au moment où elle est
faite. Motif : l'approche devra être expliquée et justifiée publiquement, et
elle fait partie de la narration du projet — la fabrique du chiffre est une
partie de l'histoire. Règle inscrite dans CLAUDE.md.

## 2026-07-03 — Validation T3 : dénominateur vedette et périmètre (décisions utilisateur)

- **Le taux mis en avant est celui sur les notices avec auteur renseigné**
  (3,53 % au comptage v0) : c'est le doute mesuré là où un doute peut exister.
  **Le taux sur la base entière (2,90 %) est toujours donné en second**, jamais
  omis. C'est un choix d'écriture, pas de calcul : les deux chiffres restent
  publiés côte à côte.
- **Le comptage de référence porte sur toute la base** (la question centrale
  vise « les musées de France », pas un domaine). **Les beaux-arts
  (peinture/dessin/sculpture/estampe) sont l'angle éditorial** : ils
  concentrent ~80 % du doute détecté. Les deux lectures s'emboîtent, on ne
  choisit pas entre elles.
- Pour la phase 2 : **chiffrer les recouvrements entre les trois familles**
  (doute / d'après / ancienne attribution) — une même notice peut porter
  plusieurs marqueurs, il ne faut jamais publier des chiffres qui
  s'additionnent à tort. Tâche ajoutée à la roadmap.

## 2026-07-03 — Méthode de comptage (T3, décision utilisateur)

- **Tous les taux sont produits avec deux dénominateurs** : sur l'ensemble des
  notices ET sur les seules notices dont `Auteur` est non vide. Motif : ~18 % des
  notices n'ont pas d'auteur renseigné (archéologie, ethnologie…) ; un taux sur
  la base entière dilue le phénomène, un taux sur les notices « avec auteur »
  le mesure là où il peut exister. **Le choix du taux à mettre en avant sera
  fait avec l'utilisateur à la validation de T3.**
- Choix du périmètre (tout Joconde vs peinture/dessin/sculpture/estampe) reporté
  à la fin de T3, au vu de la ventilation réelle du doute par domaine (T2 validée).
- Rappel actif pour T3 : « école française » dans `Ecole_pays` = nationalité,
  pas un doute ; le marqueur est « école de [artiste] », plutôt dans `Auteur`.

## 2026-07-03 — Décisions d'initialisation (phase 0)

- **CSV complet = matière de référence de la phase 1.** C'est la source canonique
  citée dans la publication finale ; l'API du ministère n'est qu'un extrait
  (~30 % de notices en moins). L'API sert aux contre-vérifications ponctuelles.
- **pandas en lecture par morceaux** (`chunksize` + `usecols`) : on ne lit que
  ~15 colonnes sur ~70, mémoire maîtrisée, code lisible. Pas de base de données
  ni de framework à ce stade.
- **Détection par lexique de motifs regex versionné dans le code** (pas de NLP) :
  auditable et explicable — conforme à la posture « on lit ce qui est écrit ».
- **Environnement uv + pyproject.toml** (choix utilisateur).
- **Échantillon de vérification au format CSV tableur** (choix utilisateur) :
  colonnes `verdict` et `commentaire` à remplir, lien vers la notice POP.
- **`data/` non versionné** (1,1 Go) ; `src/download.py` permet de tout récupérer.

## Roadmap et points de validation

### Phase 0 — Initialisation ✅ (en attente de relecture)
Arborescence, CLAUDE.md, docs/, environnement uv, git.
⏸ Relecture de CLAUDE.md et des docs avant de toucher aux données.

### Phase 1 — Test go/no-go sur la qualité des données
- **T1** Nomenclature + téléchargement → mapping des champs documenté. ⏸
- **T2** Profilage du CSV complet → chiffres, choix du périmètre. ⏸
- **T3** Détecteur v0 → taux de base global et par domaine, ventilation par marqueur. ⏸
- **T4** Échantillon stratifié ~200 notices → CSV de vérification manuelle. ⏸
- **T5** Bilan des faux positifs → recommandation go / reformulation / no-go. ⏸
Seuils indicatifs discutés : < 10 % de faux positifs = go, 10–25 % = reformulation
du lexique, > 25 % = no-go.

### Phases suivantes (esquisse, dépendent du go/no-go)
- **Phase 2** — Typologie du doute (échelle inspirée du décret Marcus) et pipeline
  consolidé CSV → JSON légers agrégés (toujours avec le total versé par musée).
- **Phase 3** — Restitution web (carte D3.js + récit guidé pressenti, forme arrêtée
  après la phase 1), page « méthode et limites » publiée au même rang que le récit.
