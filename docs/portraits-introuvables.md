# Les artistes sans portrait

État au **2026-08-06 (mis à jour le soir)**. **Trente et un** artistes sur cent deux n'ont
pas de portrait dans l'application. Leur fiche affiche le repli « Pas de portrait fiable
disponible pour X » — jamais une image approximative.

## Premier retour de recherche manuelle (2026-08-06)

Huit candidats proposés, **deux intégrés**. Le détail, ligne par ligne, est dans
`data/exports/portraits_a_chercher.csv` (colonnes `candidate_url`, `source`, `credit`,
`license`, `commentaire`, `verdict`).

**Intégrés** — Aimé et Louis Duthoit, par une même planche imprimée du XIXe siècle que
Commons publie sous CC BY-SA 4.0. Elle porte les deux frères côte à côte, chacun légendé
avec ses dates ; celles d'Aimé sont exactement celles de Joconde. L'image a été **découpée
en deux**, pour que chaque fiche montre un seul visage.

**Six refus, tous pour la même raison : le droit de réutilisation n'est pas établi.**
Aucun ne porte sur l'identité, qui est sûre dans quatre cas sur six.

| Artiste | Ce qui a été trouvé | Pourquoi c'est refusé |
|---|---|---|
| Auguste Beuret | « Portrait d'Auguste Beuret et sa femme Nini Doré », musée Rodin, inv. Ph.00791 | aucune licence publiée |
| Charles Eugène Ensfelder | dessin de Paul Reiber, musées de Strasbourg, inv. 77.2019.0.1174 — dates identiques à Joconde | « veuillez contacter la photothèque » |
| Louis Hertig | « Louis Hertig dans son atelier », Mémoire vive, Besançon | mentions légales sans clause de réutilisation |
| Auguste Alleaume | portrait **en vitrail** par son frère Ludovic (1917), Inventaire des Pays de la Loire | © du photographe seul |
| Alexandre Clausel | portrait sur un blog local | aucune provenance, aucune licence |
| Gustave Lancelot | portrait sur le même blog | aucune provenance, aucune licence |

**Les quatre premiers ne sont plus des introuvables.** Le portrait existe, il est
identifié, il est localisé dans une institution nommée. Il ne manque qu'une autorisation
— quatre demandes ciblées, à des interlocuteurs précis. C'est une piste ouverte, pas un
échec.

**Rappel de la règle du projet** : un crédit n'est pas une autorisation, un © seul n'est
pas une licence, et une image sans provenance ne s'utilise pas — même quand elle est
manifestement la bonne.

---

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

## Les trente et un, par nombre d'œuvres concernées

### Image écartée au contrôle visuel (3)

Ces artistes ont une image sur Wikidata, mais ce n'est pas leur portrait. Les QID sont
consignés dans `P18_NON_PORTRAIT` (`source_portraits.py`) pour qu'ils ne reviennent pas
par inadvertance.

| Œuvres | Artiste | Ce que P18 donne réellement |
|---:|---|---|
| 29 | Nicasius Bernaerts | nature morte « Bataille de chiens et de chats » |
| 27 | Colijn de Coter | le polyptyque de Pruszcz |
| 26 | Israël Henriet | l’inscription d’éditeur au bas d’une gravure |


### Fiche d'autorité identifiée, mais sans aucune image (14)

Ce sont les cas les plus faciles à reprendre : la personne est identifiée avec certitude,
il ne manque que l'image. Une recherche dans les fonds numérisés (Gallica, archives
départementales, sociétés savantes locales, fonds photographiques des musées) a des
chances d'aboutir.

| Œuvres | Artiste | Fiche | Déjà cherché ? |
|---:|---|---|---|
| 295 | Alexandre Clausel | Q52154652 | **oui** — voir le retour ci-dessus |
| 231 | Léon Tirode | Q131924320 | — |
| 107 | Léon Fort | Q22946093 | — |
| 43 | François Georgin | Q52063671 | — |
| 42 | Peter Hawke | Q52149491 | — |
| 39 | Auguste Alleaume | Q17621651 | **oui** — voir le retour ci-dessus |
| 32 | Gustave Lancelot | Q52218625 | **oui** — voir le retour ci-dessus |
| 32 | Odilon Roche | Q34322977 | — |
| 32 | Frans Hogenberg | Q959748 | — |
| 30 | Nicolaus Hoffmann | Q43131556 | — |
| 28 | Auguste Beuret | Q139046961 | **oui** — voir le retour ci-dessus |
| 27 | Joseph Hussenot | Q3185100 | — |
| 26 | René Ackermann | Q115255686 | — |
| 26 | Louis Hertig | Q110017854 | **oui** — voir le retour ci-dessus |


### Aucune notice d'autorité retenue (14)

Ici, la personne elle-même n'est pas établie hors de Joconde. Pour ceux-là, la piste n'est
pas Wikidata mais **le musée qui conserve leurs œuvres** — indiqué en regard, car c'est
souvent lui, et lui seul, qui possède une documentation.

| Œuvres | Artiste | Où chercher |
|---:|---|---|
| 168 | Louis Morinet | Musée de l’Image, Épinal · BnF/Gallica (imagerie populaire) |
| 82 | Charles François Pinot | Musée de l’Image, Épinal · BnF/Gallica · Archives des Vosges |
| 59 | André Marie Florentin Giraud | Musée Crozatier, Le Puy-en-Velay · Archives de la Haute-Loire |
| 48 | Charles Eugène Ensfelder | Musée de l’Image, Épinal · Archives des Vosges |
| 43 | Louis Verjat | Musée Adrien Mentienne, Bry-sur-Marne · Archives du Val-de-Marne |
| 39 | Domenico Campagnola | Louvre, arts graphiques · INHA (Agorha) · Uffizi |
| 39 | Antoine Gabriel Willermet | Sèvres — Cité de la céramique (89 dessins) · Archives de la manufacture |
| 32 | Gaspard Dughet | Louvre, arts graphiques · INHA (Agorha) · National Gallery |
| 32 | Charles du Ry | Louvre, département des arts graphiques |
| 28 | Crispin de Passe le Jeune | Rijksmuseum · RKD (Pays-Bas) · British Museum |
| 28 | Amable Louis Crapelet | Musée Grobet-Labadié, Marseille · Musée d’Orsay · Louvre, arts graphiques |
| 28 | Jean-Charles François Leloy | Sèvres — Cité de la céramique (1 770 dessins) · Archives de la manufacture |
| 26 | Laurent de La Hyre | Louvre, arts graphiques · INHA (Agorha) · musée des Beaux-Arts de Rouen |
| 26 | Henry Hennault | Musée de l’Image, Épinal · BnF/Gallica (imagerie Pellerin) |


**Charles du Ry demande une précaution particulière.** La recherche par le nom propose
Q1066622, architecte à Kassel (1692-1757). Ce n'est pas lui : le Louvre, seul conservateur
de ces 33 dessins, donne « vers 1568-1655, école française, architecte des Bâtiments du roi
en 1636 » — le bisaïeul. Même famille, même métier, un siècle d'écart. Ne pas rouvrir sans
lire la fiche du Louvre.
