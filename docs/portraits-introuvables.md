# Les artistes sans portrait

État au **2026-08-06**. Trente-trois artistes sur cent deux n'ont pas de portrait dans
l'application. Leur fiche affiche le repli « Pas de portrait fiable disponible pour X » —
jamais une image approximative.

Cette liste existe pour qu'une recherche manuelle puisse reprendre le travail là où
l'automatisme s'arrête. Elle dit, pour chacun, **pourquoi** la recherche n'a rien donné :
les trois motifs n'appellent pas les mêmes démarches.

## Ce qu'il faut vérifier avant d'ajouter un portrait

Un portrait n'entre dans l'application que si l'on a vérifié, dans cet ordre :

1. **Que l'image représente bien la bonne personne** — les dates de la personne
   représentée doivent concorder avec celles que les musées écrivent dans Joconde.
2. **Que c'est un visage, et non une œuvre.** Voir plus bas : c'est le piège principal.
3. **L'auteur de l'image, sa page source, sa licence ou son statut de domaine public**,
   et le crédit à afficher.
4. **Le fichier est téléchargé localement.** Jamais de lien vers une image distante.

La procédure est dans `web/scripts/source_portraits.py` ; le manifeste des crédits est
`data/exports/web/portraits.json`, versionné.

## Le piège : P18 ne promet pas un portrait

Sur la fiche Wikidata d'un artiste, la propriété P18 « image » porte souvent **une de ses
œuvres** et non son visage. Le défaut ne s'était pas vu sur les 63 premiers artistes, dont
les portraits gravés sont célèbres. Il est apparu net sur le lot suivant : **quatre
candidats sur treize ont dû être écartés après avoir été regardés**, aucun indice textuel
ne les départageant de façon sûre.

**Le contrôle est visuel, et il est humain.** Il n'est pas automatisable.

## Les trente-trois, par nombre d'œuvres concernées

### Image écartée au contrôle visuel (4)

Ces artistes ont une image sur Wikidata, mais ce n'est pas leur portrait. Les QID sont
consignés dans `P18_NON_PORTRAIT` (`source_portraits.py`) pour qu'ils ne reviennent pas
par inadvertance.

| Œuvres | Artiste | Ce que P18 donne réellement |
|---:|---|---|
| 94 | Louis Duthoit | la statue de saint Joseph de la cathédrale d'Amiens |
| 29 | Nicasius Bernaerts | « Bataille de chiens et de chats », une nature morte |
| 27 | Colijn de Coter | le polyptyque de Pruszcz |
| 26 | Israël Henriet | l'inscription d'éditeur au bas d'une gravure de Stefano della Bella |

### Fiche d'autorité identifiée, mais sans aucune image (17)

Ce sont les cas les plus faciles à reprendre : la personne est identifiée avec certitude,
il ne manque que l'image. Une recherche dans les fonds numérisés (Gallica, archives
départementales, sociétés savantes locales, fonds photographiques des musées) a des
chances d'aboutir.

| Œuvres | Artiste | Fiche |
|---:|---|---|
| 295 | Alexandre Clausel | Q52154652 |
| 231 | Léon Tirode | Q131924320 |
| 107 | Léon Fort | Q22946093 |
| 93 | Aimé Duthoit | Q19849903 |
| 43 | François Georgin | Q52063671 |
| 42 | Peter Hawke | Q52149491 |
| 39 | Auguste Alleaume | Q17621651 |
| 32 | Odilon Roche | Q34322977 |
| 32 | Gustave Lancelot | Q52218625 |
| 32 | Frans Hogenberg | Q959748 |
| 30 | Nicolaus Hoffmann | Q43131556 |
| 28 | Auguste Beuret | Q139046961 |
| 27 | Joseph Hussenot | Q3185100 |
| 26 | René Ackermann | Q115255686 |
| 26 | Louis Hertig | Q110017854 |

S'y ajoutent **Gaspard Dughet**, **Domenico Campagnola** et **Laurent de La Hyre**, du
premier lot, dont l'absence de portrait était déjà constatée le 2026-07-22.

### Aucune notice d'autorité retenue (12)

Ici, la personne elle-même n'est pas établie hors de Joconde. Pour ceux-là, la piste n'est
pas Wikidata mais **le musée qui conserve leurs œuvres** — indiqué en regard, car c'est
souvent lui, et lui seul, qui possède une documentation.

| Œuvres | Artiste | Où chercher |
|---:|---|---|
| 168 | Louis Morinet | musée de l'Image, Épinal |
| 82 | Charles François Pinot | musée de l'Image, Épinal |
| 59 | André Marie Florentin Giraud | musée Crozatier, Le Puy-en-Velay |
| 48 | Charles Eugène Ensfelder | musée de l'Image, Épinal |
| 43 | Louis Verjat | musée Adrien Mentienne, Bry-sur-Marne |
| 39 | Antoine Gabriel Willermet | Sèvres — Cité de la céramique |
| 32 | Charles du Ry | Louvre, arts graphiques |
| 28 | Jean-Charles François Leloy | Sèvres — Cité de la céramique |
| 28 | Crispin de Passe le Jeune | musée des beaux-arts |
| 28 | Amable Louis Crapelet | musée Grobet-Labadié, Marseille |
| 26 | Henry Hennault | musée de l'Image, Épinal |

**Charles du Ry demande une précaution particulière.** La recherche par le nom propose
Q1066622, architecte à Kassel (1692-1757). Ce n'est pas lui : le Louvre, seul conservateur
de ces 33 dessins, donne « vers 1568-1655, école française, architecte des Bâtiments du roi
en 1636 » — le bisaïeul. Même famille, même métier, un siècle d'écart. Ne pas rouvrir sans
lire la fiche du Louvre.
