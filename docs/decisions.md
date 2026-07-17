# Décisions

Chaque décision est datée et motivée. Les plus récentes en haut.

## 2026-07-17 (bis) — Charte palier 3 : zone TroisTerritoires (principe visuel central)

Rendre lisible, dans le graphique lui-même, la **distance à la main du maître**
(architecture §5). Choix consignés :

1. **Regroupement, pas nouvelle nomenclature.** Les huit mentions restent celles de
   `familles-public.js` (labels + couleurs, source unique) ; on ne fait que les
   **grouper** en trois territoires, dans une primitive dédiée `territoires.js`
   (titre + annotation courte par zone). Réutilisable telle quelle par « Comprendre
   les mentions ». L'ordre de l'axe (`ORDRE_FAMILLES`) fait déjà correspondre chaque
   territoire à une plage contiguë de colonnes (0-1 / 2-4 / 5-7) ; un garde-fou en
   dev signale toute dérive entre les deux modules.

2. **Une seule ligne de proximité, pas trois cartes.** Les territoires sont matérialisés
   par des **fonds très légers contigus** (tokens `--territoire-pres/autour/influence`,
   dérivés des pigments repères, température = distance), des **séparateurs fins** aux
   frontières internes, et des **titres** en tête. Aucun cadre ni marge entre les zones :
   le graphe reste un continuum gauche → droite. À éviter explicitement (architecture §8) :
   l'effet « trois blocs décoratifs indépendants ».

3. **Annotations éditoriales dans la clé HTML, pas dans le SVG.** Le texte SVG ne revient
   pas à la ligne : une annotation par territoire y serait illisible en mobile. Les
   annotations vivent donc dans la **clé de lecture** sous le graphe, qui **rétablit du
   même coup la clé minimale** que la sortie de la légende du répertoire (2026-07-17)
   avait retirée. La clé reprend les trois territoires (titre, annotation, mentions à
   pastilles), en cellules contiguës qui rejouent les bandes du graphe.

4. **Données, points, couleurs, tooltips inchangés.** Recadrage purement visuel : la
   géométrie a été ajustée (bandeau de titres en tête, plot descendu) mais l'échelle
   commune, les positions et l'infobulle harmonisée sont intactes. Accessibilité :
   `aria-label` du graphe enrichi (les trois territoires), `aria-label` des points
   conservé.

Nouveaux fichiers : `web/src/lib/territoires.js` ; tokens `--territoire-*` dans
`tokens.css`. Vérifié sur trois profils opposés (Ingres/Le Brun/Rembrandt : le volume
principal tombe dans un territoire différent) et en mobile.

## 2026-07-17 — Charte palier 3 : zone Répertoire (colonne de navigation)

Deuxième zone du kit. Choix consignés :

1. **Un composant dédié `Repertoire.svelte`**, pour matérialiser la séparation
   répertoire ↔ profil (architecture §4) : la page ne garde que `selection` (liée),
   toute la logique de choix (recherche, tri, liste) vit dans le répertoire.

2. **Tri : « Œuvres concernées » par défaut, « A→Z » en option.** Motif :
   « trier par valeur, sauf ordre naturel » (CLAUDE.md) — le doute EST la valeur du
   dossier, on garde donc l'ordre décroissant par défaut ; l'alphabétique n'est qu'une
   aide pour retrouver un nom précis. Libellés publics (« Œuvres », pas « doute » ni
   « notices »). Tri alphabétique sur le nom affiché complet (`localeCompare` fr).

3. **Sélection active renforcée** : filet d'accent à gauche + fond soutenu +
   `aria-current="true"`. Le filet est transparent au repos (réservé à l'actif) pour
   ne pas décaler la largeur d'un rang quand il devient actif.

4. **Retrait de la légende détaillée** (`LegendeFamilles`) de sous la liste. Elle
   n'appartient pas au répertoire (outil de choix) : elle rejoindra « Comprendre les
   mentions » (architecture §3), chapitre autonome sur le vocabulaire. Le composant
   reste au dépôt pour cette reprise ; en attendant, les couleurs restent explicables
   par les tooltips (jauges, graphique) — état transitoire assumé.

5. **Responsive repliable** (architecture §4 « colonne fixe ou repliable ») : sur
   mobile, un bouton replie/déplie le répertoire ; replié d'emblée pour donner la
   priorité au profil, refermé après un choix. `matchMedia` en `$effect` plutôt qu'un
   `<details>` natif (piège de réouverture selon la largeur, cf. 2026-07-13) ; en
   pré-rendu l'effet ne tourne pas, l'état par défaut « déployé » sert le desktop.

Note d'outillage (pas une décision de fond) : `vite preview` charge le manifeste du
build à son démarrage — après un rebuild, **le redémarrer**, sinon il sert d'anciens
chunks CSS hachés (404) et la page s'affiche sans ses styles de composant.

## 2026-07-16 (quinquies) — Charte palier 3 : prototype du kit (BandeauMaitre, ChiffreVedette, onglets)

Premier palier de code du kit de composants (charte §5), en prototype sur la fiche
maître réelle. Trois décisions à consigner, dont une qui touche l'**approche
éditoriale** (donc à valider) :

1. **Onglets renommés** Graphique/Œuvres/Carte → **Profil · Œuvres · Musées**.
   Motif : libellés éditoriaux (ce que le lecteur y trouve), pas des noms de forme
   de dataviz. Mapping : *Profil* = le graphique des formes du doute (nuage),
   *Œuvres* = les cas concrets, *Musées* = la carte géographique. État interne
   `vue` aligné (`profil`/`oeuvres`/`musees`).

2. **Synthèse calculée dans le bandeau — réintroduction assumée.** Le bloc de profil
   avait perdu tout « angle » le 2026-07-10 (2e passe) : le paragraphe de situation
   ne faisait plus que situer volume et dispersion. La charte du 2026-07-16 demande
   une **« phrase de synthèse calculée »** dans BandeauMaitre. On la réintroduit,
   mais **strictement factuelle** : elle nomme la **formule la plus fréquente** pour
   ce maître (famille dominante d'artistes.json) et sa part, sans dire ce que la
   formule « signifie ». Cohérent avec « on lit ce que les musées écrivent » : c'est
   un constat de fréquence, pas une interprétation du doute (le sens reste aux
   tooltips et au graphique). Le paragraphe volume/dispersion, lui, ne change pas.
   **⏸ à valider** (formulation « Le plus souvent : « … », <part> des œuvres concernées »).

3. **Limite de `fractionEnMots` à corriger.** Le helper plafonne à
   « près des deux tiers » (seuil 62 %). Or la formule dominante peut monter bien
   plus haut : *école de* Le Brun ≈ 240/310 = **77 %**, rendu « près des deux tiers »
   → **sous-estimation**. Options si le point 2 est validé : ajouter des paliers
   hauts au helper (« plus des trois quarts », « la grande majorité »…) OU réserver
   `fractionEnMots` aux fractions basses/moyennes et traiter la dominante à part.
   Non tranché ici (`fractionEnMots` est partagé, ne pas le modifier sans décision).

Composants : `web/src/lib/ChiffreVedette.svelte` (grand nombre Fraunces tabulaire +
légende), `web/src/lib/BandeauMaitre.svelte` (portrait agrandi + nom + synthèse +
chiffres, seuil mono-colonne géré en `@container`). Périmètre tenu : ni répertoire,
ni nuage, ni accueil touchés.

## 2026-07-16 (quater) — Chantier direction artistique & architecture éditoriale (cadrage, ⏸ à valider)

Insertion d'un chantier de cadrage **plus haut niveau que le kit de composants** :
repenser l'application comme une **publication éditoriale** centrée sur « Les
presque », pas comme une succession de blocs fonctionnels. Le problème n'est plus
la charte (couleurs/typo/coquille cohérentes) mais la **direction artistique** et
l'**architecture éditoriale**. Document de cadrage créé : **`docs/architecture-editoriale.md`**
(note de direction, à valider ; aucun code, nav du front non modifiée).

Axes cadrés (détail dans le document) :
- **Nav publique recentrée à 4 entrées actives** : Accueil · Explorer les maîtres ·
  Comprendre les mentions · Méthode. Réserve (Avant/après, échelle, carte) **hors
  nav** ; fin des entrées grisées « à venir ». **« Vue d'ensemble » n'est pas une
  entrée** : elle vit dans « Comprendre les mentions ».
- **Accueil = couverture éditoriale** : promesse d'abord, chiffre (24 507) ensuite,
  exception de Nice renvoyée en Méthode ; composition asymétrique prenant l'écran.
- **Explorer les maîtres = séparation nette répertoire ↔ profil** (colonne de
  navigation à gauche ; scène du maître à droite avec bandeau de profil + phrase de
  synthèse calculée ; vues Profil / Œuvres / Musées).
- **Comprendre les mentions** = chapitre autonome du vocabulaire des 8 formules +
  Vue d'ensemble, organisé par les **trois territoires**.
- **Méthode** = page unique ; une seule phrase de prudence visible ailleurs.
- **Principe visuel central = la distance à la main du maître** (3 territoires :
  au plus près / autour / dans son influence), décliné partout.

**Précision utilisateur sur l'illustration Joconde** : elle renvoie à la **base de
données Joconde** (archive, notices, grille, index, open data, esthétique numérique
sobre), **pas** à *La Joconde* comme œuvre ni à Léonard. Traitée en **figure de
données**, langage visuel **reproductible** (déclinable à d'autres maîtres / formes
abstraites), jamais dépendante d'une seule image. Viser une figure **originale** ;
tout élément externe = source secondaire, licence vérifiée fichier par fichier
(règle CLAUDE.md), déclarée ici et en Méthode.

Ce cadrage **précède et oriente le palier 3 (kit de composants)** : on ne
reconstruit les composants qu'au service de cette architecture. Libellés de menu et
titres du projet **à confirmer** (décision des titres toujours différée).

## 2026-07-16 (ter) — Charte : palier 2 — coquille « inventaire » (fait)

Deuxième palier, limité à **header, navigation, structure générale** (ni fiche
maître ni composants internes touchés ; données intactes ; rubriques en réserve
intactes).

- **Coquille refaite** (`+layout.svelte`) : filet d'accent (terre brûlée) en tête
  de page ; **masthead** aligné sur la colonne de contenu (`--largeur-max`),
  wordmark en Fraunces à gauche, nav à droite ; **navigation « catalogue »** en
  Public Sans, petites capitales espacées ; **indicateur de page courante**
  (`$app/stores` → `aria-current` + soulignement d'accent) ; items en réserve
  estompés (inchangés dans leur contenu). Rythme passé aux **tokens** (`--espace-*`,
  `--filet`, `--taille-*`).
- **Italique Spectral intégrée** (demande utilisateur, pour futures micro-légendes
  / mentions) : `source_fonts.py` régénère avec `Spectral:ital,…` ; le style entre
  dans le nom de fichier (`spectral-400i-*`), le romain existant est préservé.
  10 woff2 désormais dans `static/fonts/`.
- **Espaces fines des grands nombres vérifiées** : « 24 507 » (Fraunces) affiche
  correctement l'espace fine insécable → RAS.
- Vérifié par capture avant/après (accueil + Les presque, page active soulignée),
  `npm run build` OK.

Note d'outillage (sans impact code) : `vite preview` sert un `build/` incohérent
si on rebuild à chaud → toujours redémarrer le preview après un build pour les
captures (sinon CSS de layout en 404).

Restes pour le palier 3 (kit composants) : nombres de listes/dataviz en Public
Sans tabulaire ; appliquer l'italique Spectral aux micro-légendes/mentions ;
unifier cartes/onglets/légende/barres.

## 2026-07-16 (bis) — Charte : palier 1 — base typographique globale (fait)

Premier palier d'implémentation de la charte, volontairement **limité à la typo**
(pas de refonte de composants, données intactes, fiche maître non touchée,
rubriques en réserve intactes).

- **Polices en local, sans CDN.** Script reproductible `web/scripts/source_fonts.py`
  (même esprit que `source_portraits.py`) : télécharge les woff2 (sous-ensembles
  latin + latin-ext, pour « œ ») dans `web/static/fonts/` et génère
  `web/src/lib/styles/fonts.css` (URLs locales `/fonts/…`). 8 fichiers, ~277 Ko
  au total. Fraunces et Public Sans en **variable**, Spectral en 400/600.
  Ces fichiers sont des **assets versionnés** (comme `static/portraits`, `static/geo`).
- **Tokens ajoutés à `tokens.css`** : `--police-titre` = Fraunces, `--police-texte`
  = Spectral, `--police-ui` = Public Sans (avec fallbacks) ; **échelle typo**
  (`--taille-*`), **espacement** (`--espace-1..6`), **rayons**, **filets**,
  `--surface-carte`, `--ombre-douce`, `--focus-anneau`. Georgia + system-ui retirés.
- **Base typographique globale seulement** (dans `+layout.svelte`) : `body` =
  Spectral ; `h1`/`h2` = Fraunces (h3 laissé en Spectral pour **ne pas surutiliser
  Fraunces**) ; `button`/`input`/`select`/`table` = Public Sans ; `th`/`td` en
  chiffres tabulaires ; nav et pied en Public Sans, wordmark en Fraunces.
- **Vérifié par capture avant/après** (accueil + Les presque) : identité nettement
  plus « catalogue », « œuvres » (latin-ext) OK, `npm run build` OK.

Restes connus (pour le palier composants) : nombres des dataviz/listes encore en
serif (à passer en Public Sans tabulaire) ; vérifier l'espace fine des grands
nombres en Fraunces ; italique Spectral non encore embarquée. Source de vérité de
la direction : `docs/charte-graphique.md`.

## 2026-07-16 — Charte graphique : direction arrêtée (application-cadre)

Décision de travailler la charte de **toute l'application-cadre** *L'inventaire du
doute* (pas seulement la rubrique des 27 maîtres), « Les presque » servant de
terrain d'épreuve V1, avec extensibilité aux dossiers futurs. Proposition de
direction validée ; **source de vérité = `docs/charte-graphique.md`**.

Points arrêtés :
- **Concept** : « un inventaire, pas un tableau de bord » (catalogue de musée :
  papier crème, encre, filets, marges) ; idée directrice = distance à la main du
  maître (température des pigments).
- **Ambiance typographique « Catalogue savant »** (choix utilisateur) : **Fraunces**
  (titrage / chiffres vedettes / verbatims) + **Spectral** (texte éditorial) +
  **Public Sans** (UI, données, labels ; IBM Plex Sans en alternative). Libres
  (OFL), **auto-hébergées** (woff2 sous-ensemblées, pas de CDN). Georgia +
  `system-ui` abandonnés (cause du « trop normé »). Chiffres tabulaires partout,
  kickers en petites capitales.
- **Palette** : conservée et formalisée en 3 étages (neutres / accent éditorial
  terre brûlée / couleurs sémantiques), la **boîte de pigments inchangée** ;
  mécanisme d'**accent par dossier** (`--accent-presque/-revisions/-copie`).
- **Tokens à ajouter** (absents) : espacement, rayons, filets, ombre douce, focus,
  échelle typo.
- **Kit de composants** à unifier (cartes, onglets, légende, barre) autour de
  primitives partagées ; `Infobulle` gardée ; `GalaxieMaitre` au placard.
- **Extensibilité** : cadre agnostique du dossier ; pas de reskin par dossier ;
  Vue d'ensemble = pas d'anneau.

Pas de code à ce stade (proposition de direction). Prochain palier pressenti :
tokens + typographie dans `tokens.css`, puis la coquille.

## 2026-07-15 (quater) — « Vue d'ensemble » : export préparé, cadré prudemment (pas de front)

Après le rapport de reconnaissance (docs/donnees.md 2026-07-15), l'utilisateur
valide une future section « Vue d'ensemble » des formulations prudentes, mais
**strictement sur le solide**. Export dédié créé : `data/exports/web/vue_ensemble.json`
(`src/build_vue_ensemble.py`, recalculé depuis les exports validés, `assert` de
cohérence). Contenu retenu :
- familles de doute **global / dans‑27 / hors‑27** (8 familles, `presume` exclue) ;
- **niveaux global vs 27** + **global hors monoculture** (14 223 / 3 537 / 956) ;
- bloc **monoculture** (Nice/Barla, 5 791) ; totaux ; **copies « d'après » à part** (22 624).

**Choix explicites (à respecter côté front plus tard) :**
- **Pas de diagramme en anneau** ici : les familles se recouvrent (pas une
  partition) → barres, jamais un donut.
- **Pas de classement par nom hors des 27** (désambiguïsation absente).
- **Pas de période en V1** (~16 % datables).
- **Domaines** : seulement avec caveat de double‑comptage (multi‑valué) — **hors
  export** à ce stade.
- **Top musées** : laissés **en réserve** (données dispo, non incluses).
- **Message central** porté par la vue et écrit dans le JSON (`message_central`) :
  « attribué à » domine au global ; école/atelier/manière prennent le dessus dans
  les 27 → c'est ce contraste (niveau 1 global 81,7 % vs niveau 2 dans‑27 52,7 %).

Pas de front pour l'instant. Export **non synchronisé** vers `web/static/data/`
(reste dans `data/exports/web/`) tant qu'aucune dataviz ne le consomme.

## 2026-07-15 (ter) — RECENTRAGE : « Les presque » devient la 1re publication complète

Décision de cadrage (utilisateur, après évaluation externe). Plutôt qu'une
« encyclopédie inachevée de toutes les formes de doute » (plusieurs rubriques
inégales juxtaposées), on construit **une enquête visuelle complète sur une seule
forme du doute : « Les presque »** — les œuvres que les musées rapprochent d'un
grand maître sans les lui attribuer (« attribué à », « atelier de », « école de »,
« manière de »…). Motif fort propre au projet : cela répond directement au défaut
de compréhension déjà constaté (un visiteur ne saisit pas un front à 6 chantiers).

**Conséquences actées maintenant :**
- **Les autres rubriques passent en PAUSE / réserve** : « Avant / après »
  (`/revisions`), « L'échelle du doute », « La carte ». Le code et les données
  restent dans le dépôt (rien n'est supprimé) — dossiers futurs de
  *L'inventaire du doute*. `/revisions` repasse `prete: false` (hors nav publique).
- Tout le travail « Avant / après » (pipeline `build_revisions.py`,
  `revisions.json`, tests, onglets, anneau, cartes, `revisions-labels.js`,
  `VignetteOeuvre`) est **conservé en l'état** comme dossier 2 prêt à reprendre.

**Encore OUVERT (mes recommandations, non tranché par l'utilisateur) :**
- Titre/marque : garder « L'inventaire du doute » comme cadre + sous-titre de
  dossier « Les presque — autour des grands maîtres » (reco), vs titre unique, vs
  renommage. **Non décidé.**
- Périmètre de la v1 : socle (Accueil + Les maîtres + Méthode) d'abord vs complet
  (+ Le vocabulaire du presque + Comparer) vs décider après la charte. **Non décidé.**
- Garde-fous à intégrer quand on avancera : rendre visible le critère des 27 noms
  (≥ 20 notices de doute hors copie, après désambiguïsation — pas un panthéon) ;
  ne pas garder d'onglets désactivés en nav publique ; le cas Alençon reste un fil
  narratif valide (formules prudentes = « presque »).
- **À faire plus tard** : amender le cadrage large de `CLAUDE.md` (question
  centrale + Alençon) pour refléter ce resserrement éditorial.

Prochaine étape pressentie : figer la charte graphique sur « Les maîtres » comme
socle, puis décider titre + périmètre.

**Réalignement documentaire acté le 2026-07-15 (sexies, journal).** Décision
formulée : « La V1 publique de *L'inventaire du doute* sera centrée sur le dossier
"Les presque". Les autres rubriques ou formes de doute, notamment "Avant / après",
restent documentées et conservées dans le projet, mais ne font plus partie du
périmètre publiable initial. » Répercutée dans `roadmap.md` (bloc « ★ RECENTRAGE » :
périmètre V1 / en réserve / déjà fait ; P3-T2 marquée EN RÉSERVE),
`rubrique-revisions.md` (bandeau), `README.md` (État du projet). Aucun code, aucune
suppression, aucun déplacement.

## 2026-07-15 (bis) — « Avant / après » : « Les œuvres » prototype 1 catégorie (⏸ validation)

Onglet « Les chiffres » (anneau) validé comme base (réserves notées : force
visuelle de l'anneau à revoir en passe charte ; garder « L'œuvre est reclassée
comme copie » partout). Étape 5 du brief : prototype d'UNE catégorie de « Les
œuvres » avant généralisation. Fait sur « Un nom en remplace un autre » :

- **Nouveau composant `web/src/lib/VignetteOeuvre.svelte`** : image 4:3 affichée
  seulement si statut ∈ {open, authorized} + url + credit (image cliquable vers
  POP, crédit sous l'image) ; sinon **placeholder soigné** (bordure fine,
  pictogramme discret, « Reproduction non affichée » + « Droits de réutilisation
  en cours de vérification »). Jamais de rectangle gris vide, jamais de hotlink.
- **`CarteRevision` refondu** : variantes `principale` (horizontale, vignette à
  gauche) / `secondaire` (verticale, vignette en haut) ; vocabulaire
  « Attribution antérieure » / « Attribution actuelle » / « Consulter la notice
  sur POP → » (fin de « A porté »/« Aujourd'hui ») ; antérieure un peu plus
  discrète mais **jamais barrée** ; phrase de récit dérivée de la catégorie
  (revisions-labels.js) ; bord gauche à la **couleur de la catégorie** (cohérent
  avec l'anneau). Surcharges `libelle`/`recit`/`couleur` pour le filtre
  transversal « inverse ».
- **Modèle image enrichi** dans le pipeline (`build_revisions.py`) : `image` gagne
  `alt` et `licence` (tous null/pending) — les futures images s'ajouteront sans
  reconstruire les cartes.
- **Onglet « Les œuvres »** : titre interne « Les changements, œuvre par œuvre »,
  chips « libellé · N exemples » (distinct des nombres du corpus), phrase d'intro
  propre au filtre sélectionné, **carte principale** large puis **grille 2
  colonnes** (jamais 3), 1 colonne sur mobile.

Le système de cartes est générique : la validation porte sur le MODÈLE (vu sur
« Un nom en remplace un autre »). Généralisation = vérifier les autres filtres
(verbatims longs, cartes « inverse ») + petits ajustements. `pytest` = 60,
`npm run build` OK, prototype + mobile vérifiés par capture. Restent ensuite :
« En bref » puis « Repères » (2 colonnes) puis passe mobile/a11y d'ensemble.

## 2026-07-15 — « Avant / après » : refonte datajournalisme (étapes 1-3, ⏸ validation)

Application d'un brief dirigiste (approche datajournalisme) qui garde les 4 onglets
mais retravaille chaque onglet comme un chapitre autonome. Contraintes fortes
reprises : pas de dashboard, pas de scrollytelling, pas de logique juste/faux ni
rouge/vert, ne jamais présenter une révision comme une erreur corrigée ni
l'attribution actuelle comme définitive. Vocabulaire imposé : « Attribution
antérieure » / « Attribution actuelle » / « Consulter la notice sur POP → ».

Le brief impose son propre ORDRE avec points de validation. **Fait (étapes 1-3),
en attente de validation avant « Les œuvres » :**

- **Libellés recentralisés** (3e passage). Source de vérité du NOM = pipeline
  (`revisions_classify.py` → `libelles_categorie`). Nouveaux libellés :
  `autre_nom` = « Un nom en remplace un autre » · `anonyme` = « Le nom n'est plus
  retenu » · `meme_nom` = « Le nom demeure, avec réserve » · `copie` = « L'œuvre
  est reclassée comme copie » · `deja_copie` = « L'ancienne attribution était déjà
  une copie » · `plusieurs_noms` = « Plusieurs noms se succèdent » · `mineur` =
  « Cas particuliers ». Pseudo-catégorie transversale (galerie) `inverse` =
  « De l'anonymat à une attribution nominative » (décrit la notice, n'affirme pas
  qu'on a retrouvé le véritable auteur).
- **Nouveau module front `web/src/lib/revisions-labels.js`** : source unique pour
  ce que le JSON ne porte pas — couleur par catégorie, appartenance aux deux
  groupes éditoriaux, phrase d'intro par filtre, phrase de récit par carte, def
  `inverse`. Palette : famille **violette** (passages lisibles) + famille **chaude
  ocre/taupe** (trajectoires complexes) — cohérente autour de l'accent, pas
  d'arc-en-ciel, pas de hiérarchie morale ; la couleur distingue les deux groupes.
- **Onglet « Les chiffres » refait** : barres → **diagramme en anneau**
  (`web/src/lib/AnneauRevisions.svelte`). Justification dataviz (exigée par le
  brief) : Q = « comment se répartissent les 26 667 notices ? » ; message = une
  composition d'un tout ; l'anneau lit une part-d'un-tout que des barres ne
  racontent pas. Centre = total au repos, puis pct/libellé/nombre au survol/focus.
  Légende chiffrée en 2 groupes = couche accessible (boutons focusables clavier ;
  segments décoratifs `aria-hidden`). Constat « 49,2 % » en tête + 3 enseignements ;
  **toutes les valeurs calculées depuis `revisions.json`** (constat, et 27,6 % =
  mineur+plusieurs_noms+deja_copie), aucune codée en dur.
- **Chapô permanent** remplacé (formulation « observe les passages d'une
  formulation à une autre, sans décider laquelle constitue la bonne attribution »).

Reste à faire (prochaines étapes du brief, après validation) : « Les œuvres »
(carte principale + grille 2 colonnes, intros par filtre, phrase de récit par
carte, composant placeholder image 4:3 avec statut de droits, vocabulaire
« Attribution antérieure/actuelle »), puis « En bref », puis « Repères » (deux
colonnes « Ce que montrent les données / Ce qu'elles ne permettent pas de
conclure »), puis passe mobile + accessibilité. `pytest` = 60, `npm run build` OK,
anneau vérifié par capture (repos + survol).

## 2026-07-14 (quater) — « Avant / après » : palier de réorganisation ÉDITORIALE

La V1 (tout sur une page) n'était pas publiable : contenu en vrac, narration non
structurée, labels trop techniques, cartes trop « base de données ». Palier de
réorganisation **éditoriale** (pas de refonte graphique, pas d'images) validé et
implémenté.

**Onglets** (titre + chapô permanents au-dessus) : *En bref* (présentation +
une carte emblématique + lien vers la galerie) · *Les chiffres* (le graphe en
deux temps : « Le constat principal » = 4 familles de galerie à échelle commune,
puis « Les cas secondaires » = 3 familles atténuées) · *Les œuvres* (chips par
type, **un seul groupe déroulé à la fois**, jamais les 32 d'un coup ; chip
transversal « Un nom réapparaît » = direction inverse) · *Repères* (limites
courtes, renvoi à la future page méthode).

**Labels publics refondus** (phrase qui dit ce qui arrive au NOM, plus de
« Vers… ») — source de vérité `revisions_classify.py`, rebuild fait :
`autre_nom` = « Un autre nom apparaît » · `anonyme` = « Le nom disparaît » ·
`meme_nom` = « Le nom reste, avec réserve » · `copie` = « L'œuvre est reclassée
comme copie » · `plusieurs_noms` = « Plusieurs noms se succèdent » · `deja_copie`
= « Déjà une copie au départ » · `mineur` = « Cas particuliers » ; direction
inverse (badge) = « Un nom réapparaît ».

**Images — modèle de données RÉSERVÉ, rien d'affiché.** Chaque `cas` de
`revisions.json` porte désormais `image: { statut, url, credit, source }`, statut
∈ `open | authorized | pending | restricted`, tous à **pending**. `CarteRevision`
prévoit l'emplacement mais n'affiche une vignette que si statut ∈ {open,
authorized} ET url ET credit. **Jamais de hotlink POP** (la Licence Ouverte
couvre le texte, pas les clichés) ; droits à clarifier fichier par fichier plus
tard (voie Wikimedia, comme les portraits).

**Hors de ce palier** (assumé) : charte graphique, images affichées, autres
graphes (daté/non daté, anciens noms, siècles, domaines → page méthode ou V2),
filtre par ancien nom, ligne éditoriale par carte, vraie page « Méthode et
limites ». `pytest` = 60 OK, `npm run build` OK, 4 onglets + filtre vérifiés par
capture.

## 2026-07-14 (ter) — « Avant / après » : bilan v2 VALIDÉ, cadrage front ouvert

L'utilisateur **valide le bilan post-vérification et la taxonomie à 7 catégories**.
Précisions actées :

- **« Même nom, plus prudent » maintenue comme catégorie publique à part entière**
  (minoritaire à 4 %, mais elle raconte une nuance : le nom reste, la notice ajoute
  une réserve). **Libellé public retenu : « Le même nom, avec réserve »** (préféré
  à « Même nom, attribution plus prudente »). → à répercuter dans le pipeline
  (`libelles_categorie.meme_nom` et `passages`, `revisions.json`) au moment du front.
- **Chaînes** (« Plusieurs anciens noms ») : conservées dans les statistiques,
  **hors galerie V1**.
- **Cas déjà « d'après »** (« Déjà une copie ou un d'après ») : conservés dans les
  statistiques, **hors galerie V1**.
- **Direction inverse** (anonyme → un nom, 5 283) : conservée pour **équilibrer le
  récit** (le doute ne va pas que vers moins de certitude).
- **Lot V1 = 32 cas** (par diversité, plafond 2/musée) validé.
- **Tests figés avant front** validés.

Ouvre la phase de restitution front (proposition sans code d'abord : structure,
graphes, place de la galerie, wording public des 7 catégories, cartes exemples).

## 2026-07-14 (bis) — « Avant / après » : bilan de vérification + taxonomie v2 (fait, ⏸ validation)

Vérification manuelle des 80 lignes rendue par l'utilisateur (`echantillon_
revisions_annotes.csv`) : **44 OK, 18 à exclure, 8 faux passage, 10 faux
parsing**. Le « à exclure » vaut pour la galerie seulement — pas pour les
statistiques ni la méthode (consigne explicite). Refonte de la classification
en conséquence (`src/revisions_classify.py`, testée, calée sur les 80 verdicts).

**Taxonomie v2 — 7 catégories** (au lieu de 4), 3 nées de la vérification :
- *Vers un autre nom* (galerie) — 13 125 (49,2 %)
- *Même nom, attribution plus prudente* (galerie, NOUVEAU) — 1 062 (4,0 %) :
  même artiste, mais l'aujourd'hui ajoute une réserve (« Furini → Furini
  attribué », « Rembrandt → Rembrandt manière de »). Demandé par l'utilisateur.
- *Vers l'anonyme* (galerie) — 3 371 (12,6 %)
- *Vers une copie* (galerie) — 1 742 (6,5 %)
- *Déjà une copie ou un d'après* (stats, NOUVEAU) — 968 (3,6 %) : l'ancien label
  était lui-même une copie ; pas un passage depuis une attribution pleine.
- *Plusieurs anciens noms* (stats, NOUVEAU) — 3 177 (11,9 %) : chaînes de ≥ 2
  hypothèses distinctes ; trop complexes pour une carte, gardées en statistiques.
- *Changement mineur ou complexe* (stats) — 3 222 (12,1 %) : anonyme national →
  anonyme, confirmations (« école de X → X »), notes de prose.

Règles de distinction validées : une chaîne du **même** nom (Champaigne/Villot ;
Champaigne/Brière) n'est PAS « plusieurs noms » (une hypothèse, plusieurs
sources) ; « même personne » couvre l'inclusion de prénom (Le Nain Louis ↔ Le
Nain) ; « plus prudent » exige que l'aujourd'hui porte une réserve (sinon
c'est une confirmation, rangée en mineur) ; précédence côté aujourd'hui = nom >
copie > anonyme. Écoles nationales seules (« École florentine → Pietro da
Rimini ») **gardées en galerie** avec le verbatim (plus d'exigence d'un ancien
nom extrait).

**5 bugs de parsing corrigés** (repérés par l'échantillon) : parenthèses
imbriquées (« Santi Di Tito (16e (2e moitié), Italie) » → nom sale) ; nom sali
par une date (« GIOTTO, attribué en 1859 » → coupe à virgule/chiffre) ;
« Changement d'attribution » / prose pris pour nom ; « ; » biographique DANS une
parenthèse (« Dyck (Anvers, 1599 ; …) ») qui coupait à tort en deux hypothèses
→ découpage respectant les parenthèses ; parenthèse ouvrante orpheline en tête.

**Direction inverse** recomptée : 5 283 (anonyme → un nom), à valoriser.

**Contrôle figé** (`tests/test_revisions.py`, 25 cas + cohérence CSV) : 44/44 OK
restent en galerie, 0 cas « à exclure/faux passage » n'y fuit. Suite complète
`uv run pytest` : 60 passés.

**⏸ Validation du nouveau bilan** attendue avant le front (consigne utilisateur).

## 2026-07-14 — « Avant / après » : pipeline construit + échantillon (fait, ⏸ vérif)

Orientation V1 validée par l'utilisateur (libellés publics ajustés). Construit
`src/build_revisions.py` → `data/exports/web/revisions.json` (16,7 Ko) et
`src/build_revisions_sample.py` → `data/exports/echantillon_revisions.csv`
(80 lignes stratifiées). Front non touché.

Libellés publics figés : « Vers un autre nom / une attribution prudente /
l'anonyme / une copie » (jamais « destination » ni le code interne).

Arbitrages de construction (détail dans donnees.md) :
- **Anciens noms = filtre, pas palmarès.** Le graphe de fréquence est fragile
  (copies « d'après » comptées à tort ; effet mono-musée Louvre — Michel-Ange
  202/233 au Louvre). Comptage retenu **hors « d'après »** ; on s'en sert pour
  filtrer la galerie, pas comme classement vedette.
- **Parsing renforcé** : préfixe-artefact « ancienne attribution : » (style
  Louvre) retiré avant extraction du nom ; rejet anonyme/école/chiffre.
- **Direction inverse chiffrée** (5 584, ≈ « vers l'anonyme ») : à raconter,
  elle équilibre le propos (autant d'œuvres gagnent un nom qu'en perdent).
- **Lot V1** : plafond 2/musée GLOBAL (pas par type) → 32 cas, 19 musées,
  Louvre 6 %. Sélection déterministe (graine implicite : ordre CSV + tri image).

Invariants `assert` à la génération : partition des passages = 26 667 ; quotas
du lot atteints ; aucun cas sans référence POP ; plafond musée respecté.

**⏸ Prochaine étape = vérification manuelle de l'échantillon par l'utilisateur**
(colonnes verdict/commentaire), avant de figer des tests et de coder le front.

## 2026-07-14 — « Avant / après » : cadrage V1 simplifié (arbitrages)

Reprise du cadrage sur une base plus simple (demande utilisateur). Détail
complet : **docs/rubrique-revisions.md** (réécrit V1). Arbitrages :

- **Titre provisoire : « Avant / après »** (sous-titre non figé, retravaillé
  plus tard — priorité au contenu).
- **Structure primaire = par type de passage** (autre artiste / anonyme /
  encore prudent / copie « d'après »), **grands noms en filtre secondaire** au
  mot entier. Confirmé par les données : les destinations sont propres et
  chiffrables ; par période (16 % datables) ou par musée (règle non
  négociable) = écartés comme structure. L'intuition utilisateur est suivie.
- **Lot éditorial réduit** (~32, fourchette 24–40), sélection **par diversité**
  et non par prestige : plafond **2 cas/musée**, quotas par destination,
  lisibilité (ancienne courte mono-segment, ancien nom extractible, titre
  présent). Testé : 32 cas, 10 musées, **Louvre 19 %** (au lieu de 59,5 %) —
  la diversité défait mécaniquement la concentration. Cas ambigus (chaînes,
  prose, écoles nationales) exclus de l'interface, réservés à la page méthode.
- **Images : PAS d'affichage en V1** (audit du 2026-07-14, donnees.md). Le CSV
  n'a pas d'URL ; POP sert l'image depuis un CDN interne sans mention de
  droits par œuvre ; la Licence Ouverte couvre le texte, pas les clichés
  (droits musée). On ne hotlinke pas un CDN gouvernemental et on ne peut pas
  vérifier 26 667 licences → **carte textuelle + lien POP**. Illustration
  manuelle d'une poignée de cas via Wikimedia Commons envisageable plus tard
  (précédent portraits), à décider séparément — rien promis avant sourcing.
- **Statistiques générales** sur tout le corpus, **graphes classiques
  seulement** : barres (destinations, domaines, anciens noms), donut
  (datée/non datée), colonnes (siècle), une barre + phrase (concentration).
  Pas de visualisation expérimentale.
- **Export** `revisions.json` adapté : totaux + destinations + domaines +
  siècles + anciens noms (top ~15, mot entier) + lot de cas V1. `Presence_image`
  conservé comme métadonnée honnête, **non affiché**.

⏸ En attente de validation : titre provisoire, structure par type de passage,
lot V1, absence d'images, liste des graphes, schéma d'export. Puis pipeline →
échantillon de vérification manuelle → tests → front. Rien n'est codé.

## 2026-07-13 — Audit des briques restantes : « Révisions » en prochaine rubrique, carte en pause, décodeur fondu

Déclencheur : demande utilisateur — « choisir ce que les données rendent
vraiment lisible, pas ce que la roadmap prévoyait ». Audit complet du CSV et
des exports (constats détaillés dans donnees.md, même date).

**Décidé (constat validé par l'utilisateur)** :

- **Prochaine rubrique : les révisions « on a cru → aujourd'hui »**
  (`Ancienne_attribution`). Motif : 26 667 vrais avant→après, des noms qui
  parlent (Vinci 511, Poussin 350, Rubens 236, Rembrandt 227 — comptés au mot
  entier), des destinations chiffrables, tout le matériau déjà dans le CSV.
  C'est aussi la brique qui héberge l'objet « doute + révision » promu en
  P2-T1 (4 615 notices).
- **Carte nationale qualifiée : EN PAUSE.** Sa question (« le doute est-il
  réparti ou concentré ? ») a déjà sa réponse (concentré — monoculture
  Barla) ; le *où* honnête existe déjà (carte par maître, un point = un musée
  détenteur) ; le biais de couverture ferait cartographier l'effort de
  catalogage. On ne la défend pas par principe ; réouverture seulement sur un
  angle neuf.
- **Décodeur de l'échelle du doute : réduit, plus une rubrique.** La légende
  permanente des « presque » (LegendeFamilles) couvre déjà l'essentiel
  (libellés + sens + couleurs). Ce qui manque — le poids national de chaque
  formule et un exemple réel — deviendra un encart de la page « méthode et
  limites » ou de l'accueil.

**Risques et garde-fous de la rubrique Révisions** (détail, schéma d'export
et contrôles dans **docs/rubrique-revisions.md**) :

- sensationnalisme → registre : « la notice a porté le nom de X ; elle dit
  aujourd'hui Y » ; jamais « déchu », « démasqué », « erreur » ; les verbatims
  entre guillemets sont la seule matière ;
- « les musées se sont trompés » → renversé : le champ EST la preuve du
  travail d'attribution, c'est le musée qui garde la trace ; certaines
  anciennes attributions sont des propositions de catalogues savants, pas des
  affirmations du musée ;
- palmarès des grands noms → les noms = un filtre d'accès (mot entier),
  jamais un classement ; l'intro explique le biais d'attraction (les
  inventaires anciens donnaient volontiers aux grands noms) ;
- concentration Louvre/dessins (59,5 % / 62,9 %) → divulguée dans l'intro
  (précédent : monoculture Barla, 2026-07-05) ; jamais de comparaison entre
  musées ;
- faux avant/après → règles de comparaison versionnées : normalisation hors
  parenthèses, mot entier partout, extraction stricte ou pas d'extraction,
  chaînes affichées verbatim, noms proches jamais fusionnés, comparaison
  segment par segment (le dernier segment d'une chaîne peut être
  l'attribution actuelle).

**⏸ En attente de validation utilisateur** : titre de la rubrique, forme (vue
d'ensemble des destinations + galerie de cas filtrable), schéma de
`revisions.json`, plan de contrôles (échantillon de vérification manuelle
avant tout front). Rien n'est codé côté front.

## 2026-07-13 — À TRANCHER : priorité « ? » vs formule de distance dans un même segment

Déclencheur : notice POP `M0347001723` (« Tête de femme : Le Silence », Dole),
segment `SARTO Andrea del (?, manière de)` → classée **« ? » (niveau 1)** pour Andrea
del Sarto. Cause : `famille_segment()` renvoie la **première** formule dans l'ordre
`DOUTE_PAR_NIVEAU` (niveau 1 → 3), donc « ? » (niv. 1) l'emporte sur « manière de »
(niv. 3). C'est la hiérarchie **documentée** (« famille la plus légère »), pas un bug.

Question éditoriale ouverte : le musée place l'œuvre « dans la manière de » (loin du
maître) ; la ranger en niveau 1 (« presque lui ») **surestime la proximité** — ce que
la règle « on ne surpromet pas » veut éviter.

Ampleur (scan complet, 1 023 705 lignes) : co-occurrences de ≥ 2 formules = **227
segments (0,89 %)**, rares. « ? » écrase une formule de **distance** (niv. 2/3) dans
**≈ 79 segments** base entière (atelier 51, école 15, **manière 7**, entourage 5,
genre 1) ; « ? + attribué à » (87) reste niveau 1 des deux façons (seul le libellé
fin changerait). Sous-ensemble sur les 27 maîtres = plus petit (non encore compté).

Options : **A.** « ? » gagne (actuel, surestime la proximité) · **B.** la formule de
distance gagne, le « ? » devient une nuance (plus fidèle, plus prudent) · **C.** idem
B mais formalisé (« ? » gagne seulement seul ou avec « attribué à »). **Reco : B/C.**
Non tranché, non codé (demande utilisateur : diagnostic d'abord). Prochaine étape si
on avance : compte exact par maître sur les 27, puis choix A/B/C.

## 2026-07-13 — « Les presque » : intro réécrite, plus explicative (décision utilisateur)

L'ancien chapô donnait une ambiance mais ne disait pas assez où on emmène le lecteur.
Nouveau parti pris : **titre « Les presque » conservé** (identité) mais **glosé dès la
première phrase** ; l'intro explique ce que la rubrique montre, justifie le choix des
27 noms (noms de référence pour lesquels les musées emploient souvent des formules
prudentes, au moins vingt œuvres concernées — explicitement *pas* « les plus grands »)
et **oriente** le lecteur vers les quatre lectures (jauge colorée, graphique, œuvres,
carte). Encadré refait sans émoticône, recentré sur l'invariant : « ne réattribue
aucune œuvre… reprend les mots publiés par les musées… avec leurs précautions ».
Contraintes tenues : pas de « famille/niveau/au doute » en surface, les musées ne
« se trompent » pas (incertitude = savoir honnête), aucune expertise sous-entendue.
Texte témoin de la copie publique journalistique sobre.

## 2026-07-13 — Carte, palier style (décision utilisateur)

Finition visuelle only (données et comportement figés). **Fond « régions très
estompées »** retenu (contre « silhouette France seule » et « statu quo ») : garder
les frontières régionales comme repère, mais très pâles, pour ne pas concurrencer
les points. Autres réglages actés : survol/focus des points **plus franc** (pleine
opacité + halo blanc élargi), **pas de distinction au repos** des points cliquables
(le curseur main au survol suffit — deux classes visuelles embrouilleraient) ; carte
dans une **colonne centrée** (titre/fond/légende/mentions alignés) ; légende et
mention hors-cadre au **même registre** (petit corps, encre douce, filet). Le repère
texte du **musée principal** est écarté de ce palier (c'est du contenu, pas du style).

## 2026-07-13 — Identification du maître : test MOT ENTIER au lieu de sous-chaîne (décision utilisateur)

**Déclencheur** : un lecteur signale la notice POP `07980002404` (« Archimède »,
MUDO Beauvais) classée « attribué à **Rodin** ». Son auteur réel est
« SERODINE Giovanni (attribué, peintre) » — Giovanni Serodine, peintre italien du
XVIIᵉ. La **détection de la formule** (« attribué ») était juste ; c'est
l'**identification du maître** qui déraillait : `_trouve_maitre` testait par simple
sous-chaîne (`"RODIN" in pivot`), et « SE‑RODIN‑E » contient « RODIN ».

**Ampleur mesurée** (scan de toute la base, 1 023 705 lignes) : 8 maîtres, 77
segments faussement rattachés, dont **13 notices de doute** seulement (Le Tintoret 6,
Léonard de Vinci 6, Rodin 1) ; le reste ne gonflait que des dénominateurs « sous le
nom » (propre/copie). Collisions : SERODINE/PERRODIN→Rodin, VINCIDOR→Vinci,
SOLDYCK/DYCKHOFF→Van Dyck, RIBERAT/VALRIBERA→Ribera, POUSSINES→Poussin,
CORREGES→Corrège, et « TINTORETTO Domenico » (le *fils*) → Le Tintoret.

**Correctif retenu** : `_trouve_maitre` teste désormais le **mot entier**
(`\bALIAS\b`) sur le pivot normalisé, pour les inclusions ET les exclusions.
Vérifié sur données réelles :
- règle les 8 cas ci-dessus ;
- **garde** les vraies notices de Le Tintoret : elles sont cataloguées « Le Tintoret
  ou il Tintoretto (Jacopo Robusti dit) », où « Tintoret » est un mot entier ; seul
  « Tintoretto Domenico » (une seule racine, pas de frontière) est écarté ;
- **seule perte assumée** : 1 notice avec la coquille « IIngres » (double I), en
  propre — négligeable.

**Impact sur les chiffres publiés** (doute) : Le Tintoret 53→47, Léonard 56→50,
Rodin 81→80 ; les autres maîtres inchangés en doute. **Aucun maître ne passe sous le
seuil des 20 doutes** : la liste vedette des 27 est préservée. Exports régénérés,
front synchronisé, build statique OK. (Constat sur les données dans donnees.md.)

## 2026-07-13 — Carte : écartement des points + point-lien POP pour l'œuvre unique (décision utilisateur)

Deux chantiers de la carte, même séance.

**Écartement des points (chevauchements).** À taille fixe, deux musées pouvaient se
cacher : coordonnées quasi identiques (deux musées d'une même ville — Marseille,
Versailles) ou points très proches (grappe francilienne Paris/Versailles, Lille/Douai).
`geo.js` reçoit `ecarterPoints` : relaxation itérative **déterministe et sans
dépendance** qui repousse chaque paire trop proche jusqu'à `2·R + 1,5 px`, au plus
près de la vraie position ; les points confondus sont séparés selon l'angle d'or
(rendu stable). Contour blanc renforcé (1,1 px), opacité 0,82.

**Point-lien POP pour l'œuvre unique** (validé avant code). Objectif : rendre la
carte plus concrète sans images (droits/disponibilité). Quand un musée conserve
**exactement une** œuvre concernée, on veut pouvoir aller à sa notice publique.

- **Piège tranché** : un lien DANS le tooltip serait inclicable (tooltip en
  `pointer-events: none`, s'efface au départ du curseur). Donc **pas de lien dans le
  tooltip, pas de tooltip épinglable** : c'est **le point lui-même qui devient un
  lien** (`<a>` SVG → `lienPop(reference)`, `target=_blank`, `rel=noreferrer`,
  curseur main, focus clavier visible). Le tooltip reste un **aperçu** : musée+ville,
  « 1 œuvre concernée », **titre si disponible** (entre guillemets, italique), mention
  publique + pastille. Les musées **multi-œuvres restent non cliquables**, tooltip
  inchangé. Pas de nouvelle vue « œuvre » : on enrichit juste certains points.
- **Pipeline** (`build_artistes.py`) : pendant l'agrégation par musée, on retient la
  **première** notice (`ref1`, `titre1`) — qui est l'unique quand `doute==1` ; à
  l'export, `oeuvre_unique: {reference, titre}` n'est émis **que si `doute==1`**
  (entrées multi-œuvres inchangées, poids négligeable). Le front bâtit l'URL avec
  `lienPop`. Mesuré à la génération : **188** musées à 1 œuvre avec titre, **2** sans
  titre (titre `null` géré : intitulé de lien générique « … de cette œuvre »).
- `Infobulle.svelte` reçoit un champ optionnel `titre` (ligne d'aperçu).
- Vérifié : URL POP correcte, `target/rel`, aria-label (« Voir la fiche publique de
  “titre” »), Louvre multi non cliquable (circle, pas de lien), cas sans titre,
  focus clavier affiche l'aperçu. Build statique OK.

## 2026-07-13 — Harmonisation des tooltips (graphique / carte / jauges) (décision utilisateur, après revue)

Depuis que la **légende fixe** porte la grammaire des couleurs, le tooltip ne doit
plus l'expliquer : il donne seulement l'information LOCALE au point survolé, avec
le même vocabulaire public partout et aucun retour de « famille / niveau / au
doute / presque lui / autour de lui ».

**Diagnostic.** Les trois tooltips vivants passent déjà par `Infobulle.svelte`
(pas de styles parallèles) : graphique (`NuageFamilles`), carte (`CarteMaitre`),
jauges (`BarreFamilles`). Le `title=` natif de `BarreNiveaux.svelte` n'est branché
nulle part (code mort, laissé de côté). Le travail est donc surtout du style sur
`Infobulle` + une harmonisation de données.

**Structure commune** (un seul schéma `tt`, chaque vue ne remplit que le nécessaire) :
`header` (bande grisée en tête), `headerPastille?` (couleur → pastille dans le
header, côté graphique), `valeur?` (nombre local accordé), `corps?` (phrase de
sens, graphique), `lignes?` (`[{ label, couleur, valeur, appoint? }]` — ventilation
carte/jauge, `appoint` = complément gris type « 73 % »), `mentionType?` (footer
discret « Mention type : … », graphique si utile).

**Style commun sur `Infobulle`** : largeur STABLE (`width: max-content`, bornée
`min 13rem / max 17rem` — le texte passe à la ligne au lieu d'élargir, plus de saut
de largeur) ; header en **bande légèrement grisée** (fond `rgba` très léger, texte
`--couleur-encre-douce`, filet de séparation), pastille optionnelle inline ; valeur
en évidence ; lignes = libellé à gauche, **nombre aligné à droite en chiffres
tabulaires**, `%` en gris ; ombre discrète, bordure fine, padding cohérent.

**Jauges de la liste — changement de comportement** (décision utilisateur) : d'un
tooltip PAR SEGMENT (header = mention, « N œuvres · X % du doute ») à **un seul
récapitulatif du maître** : header = nom du maître, une ligne par mention (pastille
+ nombre + %). Cohérent avec la carte, plus robuste (les segments sont sous-pixels,
trop fins à viser un par un) ; toute la barre devient une seule cible focusable
(les segments passent en présentation, `aria-hidden`), aria-label = récap complet.
La formule « % du doute » disparaît (mot banni).

**Fichiers** : `Infobulle.svelte` (style + `headerPastille` + `valeur` optionnelle
+ `appoint`), `familles-public.js` (`tooltipFamille` renvoie `headerPastille`),
`BarreFamilles.svelte` (récap maître). `NuageFamilles`/`CarteMaitre` inchangés
(leur `tt` était déjà compatible). Vérifié par captures : graphique multi + à 1
œuvre (+ « Mention type »), carte multi + à 1 œuvre concernée, jauge récap, largeur
étroite 390 px (pas de débordement).

## 2026-07-13 — Légende permanente des mentions sous la liste des maîtres (décision utilisateur, validée avant code)

Une **clé des couleurs visible avant interaction**, commune aux trois vues
(graphique / œuvres / carte), pour que les tooltips ne portent plus seuls
l'explication et harmoniser jauges / graphique / cartes œuvres / tooltips carte.

- **Emplacement** : dans l'`aside` de gauche, **sous la liste des maîtres** (hors
  de la zone d'onglet). La liste scrolle dans son cadre (`max-height` + overflow) :
  la légende reste donc toujours visible sous elle.
- **Source unique, zéro seconde nomenclature** : réutilise TELS QUELS `header`
  (libellé public) et `corps` (sens court) de `familles-public.js`, dans l'ordre
  `ORDRE_FAMILLES` (= l'axe du graphique). La légende dit exactement les mêmes mots
  que les tooltips → le lecteur relie les deux sans effort.
- Chaque entrée : **pastille ronde** (couleur stable de la famille, comme les
  points de carte et les pastilles de tooltip) + libellé public + une phrase de
  sens très brève. Intitulé discret « Les mentions ». Pas de « famille / niveau /
  au doute / presque lui / autour de lui » dans l'interface.
- **Un `corps` reformulé** (source unique, sert aussi les tooltips) : atelier,
  « Son atelier, pas forcément sa main. » → **« Sorti de son atelier, pas forcément
  de sa main. »** (évite de répéter le libellé « Son atelier » dans la légende).
- **Mobile (< 720 px)** : l'`aside` s'empile au-dessus de la fiche → la légende est
  **repliable** (bouton « Les mentions » + chevron), **repliée par défaut** pour ne
  pas repousser la carte ; **toujours dépliée sur desktop** (intitulé simple).
  L'état est piloté en JS (`matchMedia`) et non par un `<details>` natif : le
  contenu d'un `<details>` fermé n'est pas ré-affichable en CSS selon la largeur
  (constaté sur Chromium, même avec `!important`).
- **Aucune donnée touchée** : la légende lit `FAMILLE_PUBLIC`, statique.
- Nouveau composant `web/src/lib/LegendeFamilles.svelte`, importé dans
  `les-presque/+page.svelte`. Vérifié par captures (desktop + mobile replié/déplié).

Palier suivant, séparé (non fait) : harmonisation du **style des tooltips**
(largeur, header grisé, espacements, typographie).

## 2026-07-12 — Carte par maître : taille de point FIXE (décision utilisateur, après test A/B)

Le premier rendu utilisait un rayon ∝ √doute (taille variable). À la revue,
confusion signalée : l'échelle étant **propre au maître affiché**, un gros cercle
chez Ribera (3 œuvres) paraissait aussi important qu'un gros cercle chez Le Brun
(276). Test A/B sur captures (Le Brun, Ribera, Van Dyck, Ingres), variable vs fixe :

- **variable** : ne « marche » que sur un vrai dégradé (Van Dyck) ; ailleurs il
  ment sur l'échelle inter-maîtres, gonfle de petits volumes (Ribera : gros disques
  qui se chevauchent au nord pour 3 œuvres) et empiète sur le rôle de l'onglet
  graphique (le *combien*) ;
- **fixe** : lisible pour les 27 maîtres, honnête (un point = une présence, jamais
  un rang), et cohérent avec la règle « jamais de comparaison entre musées sur des
  comptages bruts ».

**Retenu : taille fixe** (tous les points identiques, `R_POINT = 5`). La carte
répond à *où* ; le *combien* par musée reste **au survol** (tooltip) et dans
l'onglet **graphique**. Rayon variable, échelle commune, calibres de légende :
retirés. Bascule de test (`?carte=fixe`) retirée. Légende : « Un point = un musée
où au moins une œuvre concernée est conservée. Passez sur un point pour voir
combien, et sous quelles formules. »

**Tooltip refait (même séance).** L'ancien tooltip réintroduisait les libellés de
NIVEAU écartés (« Presque lui », « Autour de lui »). Remplacé par la **couche des
familles publiques** (`familles-public.js`, comme graphique / œuvres / jauges) :
en-tête « musée, ville », valeur « N œuvre(s) concernée(s) », puis une ligne par
famille **triée par valeur**, avec **pastille de couleur stable** et libellé public
(`header` : « Son atelier », « De son école », « Attribué à »…). Plus aucun
« niveau », « au doute » ni jargon. `Infobulle.svelte` étendu (additif) d'un champ
optionnel `lignes` (label + valeur + couleur) réutilisable ailleurs. Accord
singulier/pluriel géré ; `aria-label` du point conservé (résumé linéaire).

## 2026-07-12 — Carte par maître : spécification du composant (décision utilisateur, validée avant code)

Spécification arrêtée avant toute écriture de code. Le fond (régions métropole,
france-geojson) et le palier données (`musees_doute`) sont déjà validés (mêmes
date). Ce qui suit fige la **forme** du composant.

**Emplacement.** Troisième vue de la bascule existante des fiches « Les presque »,
à côté de `Graphique` et `Œuvres`. Onglet nommé **`Carte`** ; titre interne au-dessus
du fond : **« Où sont conservées ces œuvres »**. La carte est la réponse visuelle
au 2ᵉ chiffre du profil (« N musées où ces œuvres sont conservées »).

**Une carte = une question : où, et combien.** La position est géographique (donc
« prise ») ; la mesure est portée par la **taille** du point.

- **Taille.** 1 point = 1 musée détenteur. **Rayon ∝ √(doute)** (aire ∝ nombre),
  borné (min ~3 px, max ~22 px) pour que le Louvre n'écrase pas les petits musées
  et que ceux-ci restent visibles. Points dessinés du plus grand au plus petit
  (petits au-dessus). L'aire seule se comparant mal (CLAUDE.md), la taille est
  **appuyée par une légende de calibre + le survol**.
- **Couleur : unique et stable** pour tous les points (token d'accent « doute »),
  identique sur toutes les fiches (décision utilisateur). **Pas** de couleur par
  niveau sur la carte : cela ferait une 3ᵉ variable visuelle concurrente et
  dupliquerait le rôle du `Graphique`. La ventilation par niveau vit dans le tooltip.
- **Tooltip** (survol / focus clavier) : nom du musée — ville, total de doute,
  puis ventilation par niveau via les libellés publics (« Presque lui », « Autour
  de lui », « Son style, sans lui »), ligne omise si le niveau vaut 0. Jamais de
  code interne ; la formule du musée peut figurer entre guillemets.
- **Légende** minimale, dans le cadre : 2–3 cercles de calibre gradués (l'« axe »
  de la taille) + une ligne « Un cercle = un musée. Plus il est grand, plus ce
  musée conserve d'œuvres au nom de ce maître avec une mention de doute. » Pas de
  bloc « comment lire » séparé.

**Repli (carte qui n'apporte rien).** L'onglet `Carte` reste **toujours visible**
(une bascule qui change de forme d'une fiche à l'autre désoriente). C'est le contenu
qui bascule : s'il n'y a **qu'un seul musée projeté**, on affiche une phrase à la
place de la carte (« Ces œuvres sont conservées dans un seul lieu : le musée X, à
Ville. »). Sinon (≥ 2 musées projetés), carte. Cas limite assumé : Le Brun concentre
89 % à Paris mais compte 19 musées → carte affichée, la concentration se lit dans
la taille du point parisien.

**Mention hors-cadre.** Un musée dont `lat/lon` tombe hors de la fenêtre métropolitaine
n'est **pas projeté** mais **reste compté** (totaux, 2ᵉ chiffre du profil, `musees_doute`).
Ligne visible sous la carte : « Hors cadre métropolitain : N œuvre(s) conservée(s)
au musée … à Ville. » À la génération du 2026-07-12, un seul cas : Van Dyck, 1 œuvre
au musée de Saint-Denis de La Réunion. Détection par bornes lat/lon figées dans un
util partagé (`web/src/lib/geo.js`), communes à la projection et au test.

**Fichiers prévus.** Nouveaux : `web/src/lib/CarteMaitre.svelte`, `web/src/lib/geo.js`
(projection `geoConicConformal` calée France + bornes métropole + helper « projetable ? »).
Modifiés : `web/src/routes/les-presque/+page.svelte` (3ᵉ bouton + `{#if vue === 'carte'}`),
`web/src/lib/joconde.js` (libellés publics des niveaux exposés pour le tooltip),
`web/src/lib/styles/tokens.css` (token couleur des points si absent). Dépendance
`d3-geo` à ajouter dans `web/package.json`. Fond : `web/static/geo/regions-metropole.geojson`
(déjà en place). Docs à mettre à jour à la mise en œuvre : `methode-et-limites.md`
(fond IGN = illustration jamais donnée ; hors-cadre non projeté mais compté),
`roadmap.md`.

## 2026-07-12 — Carte par maître : palier données, `musees_doute` dans `artistes.json` (décision utilisateur, mise en œuvre)

Avant de coder la carte, on enrichit l'export (audit préalable dans donnees.md,
même date). La carte répondra à : « Où se trouvent les œuvres dont l'attribution
à ce maître est formulée avec prudence ? » — **1 point = 1 musée détenteur**,
taille ∝ nombre d'œuvres douteuses de ce maître dans ce musée.

`build_artistes.py` exporte désormais, par maître :

- `musees_doute` : liste triée par `doute` décroissant, **1 entrée = 1 musée**,
  alimentée **uniquement sur le doute** (jamais le ferme ni la copie). Chaque
  entrée : `code`, `nom`, `ville`, `lat`, `lon`, `doute`, `niveaux` (triplet),
  `familles` (liste ordonnée `{code, notices}`, pour la couleur et le tooltip).
- `nb_musees_doute`, `musee_principal` (`{code, nom, doute, part}`) pour piloter
  les replis côté front (peu de points / forte concentration).
- `doute_sans_musee` : notices de doute sans code musée identifiable (mesuré à
  **0** partout à la génération du 2026-07-12).

Le champ `musees` existant (entier, toutes catégories confondues) est **conservé
tel quel** : il correspond à son libellé public actuel (« où ces œuvres sont
conservées », tous statuts). Il ne doit pas servir à la carte.

**Deux garanties exigées et tenues (décision utilisateur) :**

1. **Invariants de comptage**, vérifiés par `assert` à la génération :
   par musée `somme(familles.notices) == doute` et `somme(niveaux) == doute` ;
   par maître `somme(musees_doute[].doute) + doute_sans_musee == doute`. Le build
   échoue si un invariant casse.
2. **Coordonnées explicites `lat` / `lon`** (et non `[lat, lon]`) pour écarter
   tout risque d'inversion côté carte D3-geo. Source géo **secondaire** : le champ
   `coordonnees` de Joconde localise le **musée** (constant par code), jamais
   l'œuvre, et ne compte rien.

Rappels de cadrage (contraintes non négociables) : carte **par maître** seulement,
jamais de carte globale du doute ; **pas de comparaison brute entre musées** — la
carte montre une **dispersion**, pas une vérité patrimoniale ; fond de carte local
auto-hébergé, aucune tuile externe, aucun serveur.

## 2026-07-12 — Carte par maître : fond auto-hébergé (régions métropole, france-geojson) (décision utilisateur, mise en œuvre)

Fond de carte sourcé et validé avant tout composant. Contrat arrêté :
**france-geojson · régions · métropole seule · Licence Ouverte · `static/geo/`
versionné · projection `geoConicConformal` · La Réunion hors-carte signalée.**

- **Source** : `regions.geojson` du dépôt france-geojson (Grégoire David),
  tracés IGN Admin Express COG 2018, **Licence Ouverte / Etalab**. URL, licence,
  date, commande et poids avant/après consignés dans `web/static/geo/README.md`
  (reproductible). Récupéré le 2026-07-12.
- **Fichier produit** : `web/static/geo/regions-metropole.geojson`, 13 régions
  métropolitaines (le fichier source n'inclut déjà aucun DROM), props `code`/`nom`.
  Simplifié mapshaper `-simplify 5% keep-shapes precision=0.0001` :
  1 452 343 → **70 619 octets** (−95 %). Fichier **versionné** (ressource source
  stable, pas un artefact du pipeline `sync:data`).
- **Niveau régions** (13 polygones) et non départements : fond discret, la mesure
  reste les points-musées. Bascule départements triviale plus tard si besoin.
- **Projection** : `d3.geoConicConformal()` + `fitSize` sur ce fichier. Pas de
  projection composite (elles servent à recoller les DROM, écartés ici).
- **Outre-mer — réserve utilisateur intégrée** : métropole seule sur le fond,
  mais le point hors métropole (mesuré : 1 seul, musée Léon Dierx à La Réunion,
  1 œuvre de Van Dyck) **reste dans `musees_doute` et dans les totaux**. Le front
  devra afficher une **mention explicite dans l'interface** (pas seulement en page
  méthode), du type « Hors cadre métropolitain : 1 œuvre conservée à Saint-Denis
  de La Réunion ». Spéc à honorer au moment du composant.
- **Source secondaire d'affichage** : le fond ne porte aucune donnée, ne compte
  rien, n'exclut aucun musée. Déclaré en page méthode (methode-et-limites.md) et
  crédité en petit corps sous la carte (« Fond : régions IGN Admin Express 2018,
  via france-geojson — Licence Ouverte »).

Prochaine étape (non commencée) : composant carte. Non codé tant que ce fond
n'est pas validé.

## 2026-07-12 — Palette contrastée (luminosité alternée) + jauges explicables au survol (décision utilisateur, validée sur simulation)

**Palette révisée.** La « boîte de pigments » du 2026-07-11 ne jouait que sur la
teinte ; les familles voisines restaient trop proches, en particulier pour une
perception réduite des couleurs. Nouveau principe : **luminosité alternée**
(sombre/clair) le long de l'axe — c'est la luminosité qui survit au daltonisme,
deux voisins ne diffèrent plus jamais par la seule teinte. Teintes toujours
sourdes/patrimoniales (la lisibilité prime sur l'harmonie, sans flashy) :

| forme | hex | contraste /crème | mouvement |
|---|---|---|---|
| attribué à | `#9e2b12` | 6,82 | rouge assombri |
| nom (?) | `#cd7048` | 3,19 | corail éclairci |
| son atelier | `#b3821d` | 3,12 | ocre éclairci |
| son cercle | `#556327` | 5,98 | olive assombri |
| de son école | `#3e6f9e` | 4,82 | bleu plus franc |
| un suiveur | `#175c50` | 7,13 | teal assombri |
| sa manière | `#7b5fb5` | 4,62 | violet éclairci |
| dans son goût | `#742e4f` | 8,52 | prune assombri |

Paires problématiques, séparation mesurée (distance en vision deutéranope simulée,
avant → après) : rouge/corail 15,7 → 36,5 ; bleu/teal 6,2 → 20,8 ; violet/prune
13,4 → 30,2 (elles étaient identiques en luminosité, Δ 0,002 → 0,095) ; ocre/olive
21,1 → 38,5. **Limite assumée** (choix utilisateur) : bleu/teal reste la paire la
plus proche — aller plus loin sortirait du registre patrimonial ; le survol,
l'ordre de l'axe et les labels publics compensent. Validée sur simulation en
situation réelle (graphique Carracci = 7 formes sur 8, cartes, jauges) avant code.

**Jauges explicables au survol — la couleur n'est jamais le seul canal.** Chaque
segment de jauge est désormais survolable **et focusable au clavier** : infobulle
« header public / N œuvres · X % du doute » (labels de familles-public.js, accord
par `oeuvres()`, pourcentage français à une décimale), `aria-label` complet en
repli (« De son école : 240 œuvres, 77,4 % du doute autour de Charles Le Brun. »).
La jauge reste un résumé miniature du graphique (mêmes couleurs, même ordre, mêmes
labels) mais devient lisible en détail. **Zone de survol élargie** verticalement
(pseudo-élément invisible) pour atteindre les segments de ~2 px sans fausser les
proportions affichées.

**Infobulle partagée** : le tooltip HTML custom du graphique est extrait en
`Infobulle.svelte` (header / valeur / précision / mention type) — une seule
grammaire de tooltip dans l'application, consommée par le graphique (position
absolue dans son hôte) et par les jauges (**position fixe**, coordonnées fenêtre :
la liste défile, un panneau absolu serait rogné par l'overflow). Le `title` natif
a été écarté : invisible au focus clavier.

**Restructuration de la ligne de liste** (conséquence a11y) : la jauge sort du
`<button>` de sélection — un élément focusable ne peut pas vivre dans un bouton.
Le `<li>` porte désormais l'état (bordure, survol, sélection), le bouton ne couvre
que nom + compte, la jauge est sa sœur.

Vérifié par capture : jauges palette révisée ; survol du gros segment bleu de
Le Brun (« De son école — 240 œuvres · 77,4 % du doute ») ; **focus clavier** sur
le trait de 2 px « nom (?) » (outline + « 2 œuvres · 0,6 % du doute ») ; tooltip du
graphique intact via l'infobulle partagée ; cartes Œuvres. Build sans avertissement.

## 2026-07-11 — Jauges de la liste : des niveaux aux familles (décision utilisateur, après test)

**Le choix « option A » du palier couleur (même jour, ci-dessous) est écarté après
test.** La jauge à 3 niveaux devait être « une version résumée des 8 formes » ; en
situation réelle elle **contredisait le graphique** : chez Le Brun, la masse
dominante « de son école » (bleue sur le graphique) apparaissait ocre dans la jauge
(agrégée au niveau 2). La couleur de la forme dominante disparaissait de la liste.
Vérifié sur les données avant de trancher : les jauges consommaient bien `niveaux`
= [n1, n2, n3], cohérents avec les sommes de familles par niveau (aucun bug — un
choix de langue visuelle, pas de calcul).

**Nouvelle règle : la mini-jauge de chaque maître est un résumé direct du
graphique** — mêmes familles, mêmes couleurs (`var(--forme-*)`), même ordre que
l'axe, proportions réelles (`notices / doute`). `BarreFamilles.svelte` remplace
`BarreNiveaux` dans la liste :
- familles absentes non affichées ; un segment minuscule reste un simple trait,
  jamais de largeur minimum (les proportions priment) ;
- **filet séparateur de 1 px couleur du fond** entre segments (gap), pour détacher
  les voisins proches (rouge/corail, violet/prune) sans fausser les parts ;
- le chiffre à droite reste le total de doute ;
- aucune légende dans la liste (le graphique et ses tooltips portent le sens).

Aucune modification du pipeline ni du JSON (`familles` était déjà exporté).
`BarreNiveaux.svelte` conservé en archive (précédent GalaxieMaitre) et les tokens
`--niveau-1/2/3` gardés pour de futures vues sur l'échelle du doute.

Vérifié par capture : Le Brun (masse bleue « école », conforme au graphique),
Rembrandt (masse violette « manière »), Ingres (rouge « attribué à »),
Michel-Ange (⅓ rouge + ⅔ bleu), Rodin (tout rouge).

## 2026-07-11 — Grammaire couleur « boîte de pigments » (décision utilisateur, validée sur aperçu)

**Constat.** Points, cartes « Œuvres » et jauges tenaient dans une seule gamme
orange/brun (les couleurs de familles avaient été *dérivées* des niveaux) : formes
indistinguables, rendu générique, niveau 3 délavé sur crème. Deux sources de hex,
non alignées (tokens CSS pour les niveaux, JS pour les familles).

**Système retenu.** Une **couleur stable par forme de doute**, pensée comme une
**boîte de pigments de peinture ancienne** (diverse mais légitime sur le sujet, pas
« arc-en-ciel décoratif ») :

| forme | token | pigment | contraste /crème |
|---|---|---|---|
| attribué à | `--forme-attribue` `#b8431f` | terre de Sienne brûlée | 4,96 |
| nom (?) | `--forme-point-interrogation` `#c96a4e` | terre rose | 3,38 |
| son atelier | `--forme-atelier` `#a8781f` | ocre jaune | 3,56 |
| son cercle | `--forme-entourage` `#6f7d34` | terre verte | 4,11 |
| de son école | `--forme-ecole` `#3f6b8f` | bleu de smalt | 5,16 |
| un suiveur | `--forme-suiveur` `#2f7d70` | vert-de-gris | 4,46 |
| sa manière | `--forme-maniere` `#6f5691` | violet minéral | 5,60 |
| dans son goût | `--forme-genre` `#8a5168` | lie de vin | 5,54 |

Toutes ≥ 3:1 sur le fond crème (cible objet graphique, vérifié). **Température =
distance au maître** : rouges (niveau 1) → terreux basculant au froid (niveau 2) →
pourprés (niveau 3) — la couleur *renforce* la lecture de l'axe sans la porter seule.

**Jauges : option A** (choix utilisateur — pas de mini-répartition en 8 formes dans
la liste, qui la chargerait). Les 3 couleurs de niveaux sont les **pigments repères**
de chaque zone (`--niveau-1/2/3` = attribué / atelier / manière) : la jauge à
3 niveaux devient une version résumée des 8 formes, même langue. Le niveau 3 n'est
plus délavé (violet franc). Conséquence assumée : dans la liste, une forme apparaît
à la couleur de son *niveau*, pas de sa *forme* — l'identité par forme n'existe que
dans Graphique + Œuvres (le jour où on la voudrait dans la liste = option B).

**Copie « d'après » neutre** : `--couleur-copie` passe de `#4a6b7a` (bleu-gris, qui
collisionnait avec le nouveau bleu de smalt) à `#6b6f76` (gris), hors de la gamme
colorée du doute — une copie assumée n'est pas un doute.

**Centralisation.** Tous les hex de sujet vivent désormais **uniquement dans
`tokens.css`** (`--forme-*`, `--niveau-*`, `--couleur-copie`). `familles-public.js`
ne porte plus que des références `var(--forme-*)` ; le `STYLE_FAMILLE` en dur de
`NuageFamilles` avait déjà été retiré. Détail technique : le point du graphe passe
de l'attribut SVG `fill=` à la propriété CSS `style="fill: …"`, car `var()` ne
s'applique pas aux attributs de présentation SVG (seulement aux propriétés CSS).

Validé sur aperçu (planche de swatches + vraies vues Graphique / Œuvres / liste)
avant implémentation ; re-vérifié après centralisation. Les cartes ne portent la
couleur que par la pastille + le kicker (jamais tout le bloc).

## 2026-07-11 — « Les presque » : l'onglet « Détail » devient la vitrine « Œuvres » (décision utilisateur, validée avant code)

**Constat.** La vue « Détail » répétait le graphique (échelle du doute, table des
formules = les mêmes comptes que les points) avec des titres techniques, et ses
liens POP n'avaient pas de fonction éditoriale claire.

**Rôle redéfini.** Le graphique répond à « quelles formes prend le doute autour de
ce nom ? » ; l'onglet **« Œuvres »** répond à « quelles œuvres concrètes se trouvent
derrière ces formes ? ». On passe des points aux œuvres, des libellés publics aux
**mots réellement publiés**, du résumé au **cas vérifiable**. L'`extrait` du champ
auteur est la **seule citation littérale** de l'application (le tooltip du graphique
affiche une mention *reconstruite*) : c'est le moment « on lit ce que les musées
écrivent » du projet.

**Supprimé** : « L'échelle du doute » (barre des niveaux) et « Les formules
employées » (table) — redites du graphique. **Transformé** : les exemples passent
de bas de page à contenu principal.

**Forme retenue : vitrine en cartes**, pas une table.
- **Kicker dans la carte** (pas de titres de groupes) : header public de la forme
  (« Attribué à », « Son atelier »… — les mêmes mots que le tooltip du graphique)
  + **pastille de la couleur du point**. La couleur est sur la pastille, pas sur le
  texte (contraste des teintes claires). Cartes triées dans **l'ordre de l'axe X**.
- Titre de l'œuvre **tel que publié** (souvent en capitales : on ne réécrit pas,
  corps modéré pour que ça ne crie pas ; « Sans titre » en repli), musée + ville.
- **Verbatim en exergue**, entre guillemets, sans préfixe (l'amorce l'explique une
  fois : règle anti-répétition).
- Lien explicite « **Voir la fiche publique →** » par carte (le titre cliquable
  seul a une mauvaise affordance) ; **une seule** mention technique en bas :
  « Les liens ouvrent les fiches publiques sur POP, la plateforme ouverte du
  patrimoine. » Jamais « notice » ni « base de données ».
- Titre de section : « Quelques œuvres derrière les points ». Amorce (choix
  utilisateur) : « Quelques exemples issus des fiches Joconde, avec les mots
  publiés par les musées. » — la règle de sélection automatique est documentée en
  méthode, pas dans l'interface.
- **Copies « d'après » à part**, en fin : bloc distinct (couleur hors gamme du
  doute) « À part : {N} œuvres « d'après {maître} » — des copies assumées, pas des
  attributions incertaines. » + un exemple de copie lié, en petit corps, jamais en
  carte.

**Export enrichi d'abord, vitrine codée une fois** (plutôt qu'une V1 plate refaite
ensuite) : `build_artistes.py` émettait déjà un exemple par famille mais perdait le
code au moment du JSON. Ajouts : `code` de forme sur chaque exemple, **2 exemples
pour la forme dominante** (1 pour les autres, plafond 9), `exemple_copie` par
maître. Comptages inchangés (vérifié). **Le front ne re-parse jamais les
extraits** : le code de forme vient exclusivement de l'export.

**Couleur par famille centralisée** dans `familles-public.js` (`couleur` par
entrée) : source unique pour les points du graphique et les pastilles de la
vitrine (CLAUDE.md : une couleur par catégorie, stable partout). `STYLE_FAMILLE`
local à `NuageFamilles` supprimé.

Vérifié par capture : Le Brun (5 cartes, ordre de l'axe, copie avec exemple),
Rodin (cas minimal : 2 cartes d'une seule forme, rendu digne), largeur étroite
(une colonne). Build sans avertissement.

## 2026-07-11 — Nuage « Les presque » : point au plafond rogné, corrigé (marge de tête)

Le point de la famille dominante (au plafond commun, 240 = « école de » Le Brun)
était **rogné en tête** : sa bulle, de rayon maximal 16, était centrée sur `Y_HAUT`
= 10 et débordait au-dessus du bord haut du viewBox. Corrigé en réservant assez de
marge en tête pour le rayon max : `Y_HAUT` 10 → 24, `Y_HAUTEUR` 226 → 212. `Y_BASE`
reste à 236 : la ligne de base, l'échelle et l'axe X sont **inchangés** — seul le
haut du graphe gagne de l'air. Vérifié par capture (Le Brun) : la bulle à 240 est
entièrement visible, centrée sur sa graduation.

## 2026-07-11 — « Les presque » : bloc profil, chiffres en points d'appui (décision utilisateur)

3e itération du header (après « texte gauche / portrait droite » puis « nom pleine
largeur + portrait gauche / texte droite centré »). Constat : le portrait a un vrai
poids visuel, mais le paragraphe restait une petite masse au milieu d'un vide — trois
objets côte à côte, pas un bloc de profil.

Retenu (comparé par capture A vs B) :
- **Colonne de texte calée en HAUT** du portrait (`align-items: start`), pas centrée.
- **Colonne bornée** (`grid-template-columns: 12rem minmax(0, 24rem)`, `justify-content:
  start`) : elle répond au portrait au lieu de s'étaler comme une phrase de page.
- **Deux blocs empilés** (volume, puis dispersion) espacés (`.profil-texte`, flex,
  gap 1.1 rem) pour occuper la hauteur du portrait.
- **Chiffres en points d'appui** (variante B, préférée à la version tout-texte A) :
  le nombre en gros corps, couleur d'accent, sur sa propre ligne (`.chiffre`), sous
  lui l'attribution en texte courant. Donne à la colonne le poids qui manquait.

Réserves assumées : (1) de gros chiffres colorés flirtent avec l'infographie — toléré
ici car ce bloc est une **carte de profil**, pas une dataviz ; le chiffre est un
**repère**, la vraie mesure reste dans le graphe. (2) Le 2e bloc est reformulé en
« {N} musées où ces œuvres sont conservées » (retouche de texte validée à part).

Périmètre : CSS/layout + mise en forme du texte de `+page.svelte` uniquement. Données,
graphe et tooltips non touchés. Ancienne règle `.chapo-maitre` supprimée.

## 2026-07-11 — « Les presque » : portrait sorti du graphique, remonté au header de fiche (décision utilisateur)

Le portrait n'apparaissait que dans la vue « Graphique ». Incohérent : l'image
incarne le **profil du maître consulté**, elle appartient à la fiche entière, pas
à un onglet.

**Nouveau composant `PortraitMaitre.svelte`** — reprend le markup, le placeholder
silhouette, la logique de légende et les styles du portrait, jusqu'ici dans
`NuageFamilles.svelte`. Centralise le **format de légende normé** (sujet, auteur,
Wikimedia Commons, licence — rien d'autre, CLAUDE.md). Statut inchangé : **source
secondaire d'illustration**, jamais donnée ni comptage. Données et sourcing
(`portraits.json`) **non touchés**.

**Placement (2e disposition, même jour).** La 1re version (texte à gauche / portrait
à droite) déséquilibrait la fiche : portrait flottant seul en haut à droite, texte
isolé, graphe démarrant après un grand vide. Retenu : **bloc profil compact** —
nom en **pleine largeur**, puis portrait à **gauche** (largeur bornée 12 rem, légende
dessous) + paragraphe de situation à **droite**, centrés verticalement (`.profil`).
Les onglets Graphique / Détail restent **sous** ce bloc, le contenu d'onglet en
pleine largeur dessous. Le profil étant hors de la zone qui change d'onglet, le
portrait reste visible en Graphique **comme** en Détail, sans duplication ni **saut
de mise en page** au changement.

**Responsive par requête de conteneur** (`container-type: inline-size` sur `.fiche`)
plutôt que par largeur d'écran : sous ~32 rem de largeur de fiche, le profil passe
en **une seule colonne** (nom, puis portrait, puis texte, alignés à gauche — pas
deux colonnes écrasées). Le seuil porte sur la fiche réelle → le passage se fait
« plus tôt » quand l'aside comprime la colonne, et le texte garde toujours une
largeur confortable.

`NuageFamilles.svelte` allégé : prop `portrait` retirée, wrapper flex `.regard`
remplacé par `.graphe-hote` (simple repère du tooltip), le graphe **récupère toute
la largeur** libérée.

Vérifié par capture (Chromium piloté, outil de test retiré ensuite) : (1) Graphique
avec portrait au header, (2) Détail même portrait visible, (3) ratio différent
(photo de Rodin) contenu par la vignette à hauteur fixe, (4) largeur étroite =
portrait sous le texte. Observation hors périmètre : le point au plafond (240) est
rogné en tête de graphe (géométrie du nuage, `Y_HAUT` trop court pour le rayon max)
— à traiter séparément.

## 2026-07-10 — « Les presque » : onglet « Graphique » + paragraphe de situation générique (décision utilisateur)

**Onglet renommé.** « Nuage » ne décrit pas la visualisation et n'est pas un nom
de navigation clair → **« Graphique »**. Couple d'onglets : Graphique / Détail
(état interne `vue` passé de `'nuage'` à `'graphique'`).

**Paragraphe de situation réduit au volume et à la dispersion.** L'ancien texte
disait « ils écrivent qu'ils ne sont pas certains qu'il les ait peintes » : « ils »
flou, tournure lourde, « peintes » faux pour certaines familles. Une 1re réécriture
(même jour) avait tenté un gabarit avec fraction + mention dominante + explication ;
jugé **encore trop bavard**, il réintroduisait de l'interprétation. Décision finale :
ce paragraphe **ne porte plus aucun angle** — ni fraction, ni mention dominante, ni
« attribution prudente », ni override manuel. Le doute est déjà porté par le
graphique et les tooltips. Il sert seulement à situer volume et dispersion :

> Les musées de France conservent {total} œuvres sous le nom {de/d'}{maître}. Ces
> œuvres sont conservées dans {musées} musées.

Accord singulier/pluriel sur les deux quantités (`oeuvres`, `musees`). Conséquence :
`editorial-maitres.js` perd tout son mécanisme d'explication/override (famille
dominante, `situationMaitre`, `EDITORIAL[nom].explication`) — code mort supprimé,
il ne reste que `bioMaitre`. Le refactor `mention`/`montrerMention`/`deNom` de
`familles-public.js` **reste** (toujours utilisé par les tooltips).

**Correction de langue** (exigence CLAUDE.md) : helper `deNom` gère l'élision
(« sous le nom d'Ingres », « école d'Ingres ») ; helper `musees` accorde le
singulier/pluriel (« 1 musée » / « 64 musées »). Jamais de `` `${n} musées` ``
concaténé. `deNom` est aussi branché sur les mentions type (corrige un défaut latent
des tooltips : « entourage de Ingres »).

**Refactor tooltip** au passage : `FAMILLE_PUBLIC[code].mentionType` (nul/fonction)
remplacé par `mention` (toujours définie) + `montrerMention` (booléen). Le footer du
tooltip n'affiche la mention que si `montrerMention` (règle anti-répétition
inchangée : `point_interrogation`, `entourage_de`, `genre_de`). Source unique de la
chaîne, plus de duplication paragraphe/tooltip.

## 2026-07-10 — Nuage « Les presque » : grammaire de tooltip + tooltip HTML custom (décision utilisateur)

Le tooltip issu de la décision plus bas (`{label} — « {formule} » : {sens}. {N}
œuvres.`) répétait trois fois la même chose : le label, la formule exacte et le
sens disent presque les mêmes mots. Corrigé non pas au coup par coup mais par une
**vraie grammaire de tooltip**, validée après deux tours de proposition (table
relue et amendée par l'utilisateur avant tout code).

**Structure à hiérarchie visible** (modèle Datawrapper/Flourish), plus de phrase
linéaire :
- **header** — titre court, générique (jamais le nom du maître → stable d'une
  fiche à l'autre, donc comparable) ;
- **corps** — commence par le sens réel pour le lecteur, prudent ;
- **valeur** — « N œuvres », bien séparée ;
- **mention type** — niveau secondaire optionnel.

**Règle anti-répétition (gravée dans `familles-public.js`)** : la mention type ne
s'affiche QUE dans deux cas — soit la mention brute est elle-même le fait marquant
(`point_interrogation` → « Ingres (?) »), soit le terme réel du musée diffère du
libellé public (« entourage » ≠ « cercle », « genre » ≠ « goût »). Partout ailleurs
elle redirait le header → omise (`attribue`, `atelier_de`, `ecole_de`,
`suiveur_de`, `maniere_de`).

**« Mention type », pas « Formule Joconde »** : la chaîne est reconstruite par le
code (`` `entourage de ${nom}` ``), ce n'est pas un verbatim de la notice. Le
libellé public reste donc honnête sur ce point.

**Abandon du `<title>` SVG natif → tooltip HTML custom.** Le `<title>` n'est pas
stylable et impose une seule masse de texte : impossible d'y rendre la hiérarchie
header/corps/valeur/mention. Remplacé par un panneau HTML sobre (fond clair, pas de
pavé noir), positionné en pixels depuis la position réelle du point à l'écran
(le SVG a son propre repère viewBox), basculé sous le point quand il est trop haut.
Il ne vit qu'au survol/focus, ne masque donc pas durablement le graphe ni le
portrait. Accessible au **survol et au focus clavier** (`role="button"`,
`tabindex`), et **repli lecteur d'écran** conservé via un `aria-label` linéaire
(`resumeFamille`) sur chaque point, puisque le `<title>` disparaît.

Périmètre volontairement borné à ce palier : **ni les labels de l'axe ni la
micro-légende** n'ont été touchés.

**Grammaire allégée (même jour, 2e passe).** Le tooltip n'est pas un dictionnaire
des labels : si chacun réexplique tout, le lecteur relit huit fois la même notice.
Ordre retenu = **header → valeur → précision courte → footer optionnel**. Le corps
devient une **précision d'une seconde de lecture** (peut être vide si le header se
suffit), pas une définition. Objectif : lisible en un coup d'œil.

**Accord singulier/pluriel** : helper `oeuvres(n)` → « 1 œuvre », « 240 œuvres ».
Jamais de `` `${n} œuvres` `` concaténé directement. Le tooltip reçoit désormais le
nombre BRUT (accordé côté libellé), plus une chaîne pré-formatée.

Table des formulations validées (label axe inchangé) :

| Code | Header | Précision (corps) | Mention type |
|---|---|---|---|
| `attribue` | Attribué à | Sans certitude qu'il s'agisse bien de sa main. | — |
| `point_interrogation` | Nom suivi d'un « ? » | Doute noté sans autre précision. | « [nom] (?) » |
| `atelier_de` | Son atelier | Son atelier, pas forcément sa main. | — |
| `entourage_de` | Son cercle proche | Son entourage immédiat. | « entourage de [nom] » |
| `ecole_de` | De son école | Plutôt son école que sa main. | — |
| `suiveur_de` | Un suiveur | Dans sa suite, sous son influence. | — |
| `maniere_de` | À sa manière | Son style, auteur inconnu. | — |
| `genre_de` | Dans son goût | Lien de style lointain. | « dans le genre de [nom] » |

## 2026-07-10 — Nuage « Les presque » : couche de libellés publics + axe réordonné (décision utilisateur)

Suite du chantier narration. Les labels de l'axe exposaient les familles internes
(« attribué à », « ? », « école de », « atelier »…) : exactes pour nous, opaques
pour un visiteur. Le cas criant : « ? » seul, sans aucun sens. Décidé après deux
tours de proposition (aucune implémentation avant validation) :

**Couche de traduction publique** — nouveau `web/src/lib/familles-public.js` :
par famille, un `label` public court, la `formule` exacte du musée (avec le nom du
maître) et un `sens` en clair. Source unique des libellés, réutilisable par la vue
Détail plus tard. Le tooltip se compose : `{label} — « {formule} » : {sens}. {N}
œuvres.` — sans « niveau », « famille » ni « marqueur », la formule exacte
conservée entre guillemets, explication au pluriel/neutre et prudente (on rapporte
ce que font les musées, on n'affirme rien).

**Libellés retenus** (curseur fidélité ↔ lisibilité, la formule exacte restant au
survol) : attribué à · **nom (?)** · son atelier · son cercle · **de son école** ·
un suiveur · sa manière · **dans son goût**. Choix notables : « nom (?) » (fidèle à
la notation Joconde, lisible, ≠ « ? » seul) ; « de son école » (provenance, évite
de lire « école qu'il a fondée ») ; « dans son goût » (« son genre » sonnait faux).
« de son école » et « dans son goût » validés **provisoirement** (perfectibles).

**Axe réordonné par distance narrative** (option B) — ordre
`docs/typologie.md` : niveau 1, puis niveau 2 **atelier → entourage → école →
suiveur**, puis niveau 3. L'ancien ordre plaçait « école » avant « atelier » et
cassait une lecture gauche-droite. Réordonnancement **purement cosmétique** (ordre
des colonnes dans `NuageFamilles`), aucune donnée touchée, zones de couleur
toujours contiguës, comparabilité entre maîtres intacte.

**Micro-légende** (une ligne, statique, sous le graphe) :
« De gauche à droite, le lien au maître se desserre. » Elle remplace l'ancienne
bulle « Comment lire » (rejetée : saut de page + explication éparpillée). Honnête
seulement parce que l'axe est désormais ordonné.

**Règle gravée dans CLAUDE.md** (« Couche de libellé public obligatoire ») : aucune
catégorie technique affichée telle quelle ; un graphe se lit par ses labels,
légende et infobulles, jamais par une notice séparée. But : ne pas réinjecter les
structures du JSON dans l'interface à la prochaine brique.

Périmètre tenu : **nuage seul**. Non touchés (signalés) : l'accueil (« notices »,
« lexique »), la mention d'Alençon comme point d'entrée narratif dans CLAUDE.md
(la Phase 3 l'a pourtant écarté du centre), la vue Détail (refonte différée ; la
couche de traduction est prête à y être réutilisée).

## 2026-07-09 — Séparer les trois natures de texte + bannir le vocabulaire interne (décision utilisateur)

Refonte des textes de « Les presque », après constat que les fiches maîtres
étaient bavardes et répétitives. Le problème était **structurel, pas
stylistique** : le mode d'emploi de la visualisation avait envahi le texte
éditorial. Trois natures de texte cohabitaient au même niveau.

**Règle posée (désormais dans CLAUDE.md, « Principes de rédaction ») — trois
natures de texte, jamais mélangées :**
1. **Éditorial** — propre à un maître, court, en français courant, place centrale.
2. **Mode d'emploi** de la dataviz — identique partout, écrit **une seule fois**
   (ici : bulle dépliable « Comment lire ce graphique » à côté de la bascule),
   jamais répété par fiche.
3. **Mentions techniques** — crédits, licences, méthode : petit corps, en bas,
   format normé.

**Vocabulaire interne banni de l'interface publique.** *notice → œuvre* ;
*« formule de doute »* → phrase en clair (« les musées écrivent qu'ils ne sont
pas certains… ») ; *niveau 1/2/3* non affiché (l'info est déjà dans la couleur et
la position) ; *famille / marqueur / lexique* n'apparaissent jamais. Les
**libellés de familles** (« attribué à », « école de »…) restent inchangés pour
l'instant (reformulation narrative = chantier distinct), **sauf** le nom de code
« atelier (qualificatif, beaux-arts) » raccourci en « atelier de » à l'affichage.

**Une légende d'image n'est pas une note de méthode.** La mise en garde « ces
œuvres ne sont pas attribuées avec certitude au maître » a quitté la légende du
portrait (où elle n'avait rien à faire) pour rejoindre la bulle « Comment lire ».
La légende suit la forme normée : **sujet, auteur de l'image, source, licence**.

**Chiffres racontés en français** (« plus de la moitié » plutôt que « 59 % »),
le chiffre exact restant accessible (nombres bruts, survol, vue Détail).

**Mise en œuvre (front, aucune donnée touchée) :**
- `web/src/lib/editorial-maitres.js` (nouveau) : couche éditoriale du front (bio +
  angle par maître). **Ce ne sont pas des données Joconde** — Joconde reste la
  seule source de données. Deux maîtres témoins écrits à la main (François Clouet =
  doute proche « atelier » ; Rembrandt = doute lointain « à la manière de »),
  validés sur pièce. Les 25 autres ont un **angle dérivé** de leur famille de
  doute dominante (repli honnête, pas de fiche cassée) ; leur montée en qualité
  est une sous-étape (roadmap P3-T1).
- `web/src/lib/joconde.js` : helpers `fractionEnMots`, `libelleFamillePublic`,
  `licenceEnFrancais`.
- Les chiffres ne sont jamais stockés en dur : calculés dans le composant depuis
  `artistes.json`.

**Statut des portraits Wikimedia — renforcé.** Rappel (déjà consigné plus haut le
même jour) : **source secondaire d'illustration uniquement, jamais de donnée ni
de comptage**, même rang que le futur fond de carte. Joconde = seule source de
données. À redire dans la page méthode le moment venu.

**Défaut repéré ailleurs, hors périmètre de ce palier (à traiter ensuite) :**
la page d'accueil (`web/src/routes/+page.svelte`) emploie encore « notices » et
« Détection : {lexique} », et une notation d'analyste (« X % … Y % de la base »).
À reformuler **en gardant les deux dénominateurs** (règle de rigueur du
2026-07-03), sans les supprimer.

## 2026-07-09 — Portraits : retournement des regards + vignette de taille figée (décision utilisateur)

Deux ajustements du portrait de « Les presque », après examen du rendu.

**Retournement des portraits qui regardent à droite.** Le maître doit « regarder »
son nuage, placé à sa gauche. Les portraits dont le sujet regarde vers la droite
sont donc retournés horizontalement à l'affichage (`transform: scaleX(-1)`).
Constaté à l'œil sur les fichiers, **8 concernés** : Annibale Carracci, Boucher,
Guido Reni, Simon Vouet, Greuze, Hyacinthe Rigaud, Fragonard, Ribera. Les autres
regardent déjà à gauche ou sont frontaux. **Règle d'exclusion : jamais retourner
une gravure portant du texte** (Le Primatice, François Clouet, Le Corrège) — le
miroir inverserait le texte. L'info est portée par un champ `regard`
(`gauche`/`droite`) dans `portraits.json`, et mémorisée dans le set `REGARD_DROITE`
de `source_portraits.py` pour survivre à une régénération. Coût assumé : on affiche
un tableau connu en miroir — choix cosmétique au service de la mise en scène, pas
une altération de donnée (le portrait n'est qu'illustration).

**Vignette de taille figée.** Les portraits Commons ont des ratios variés ; sans
hauteur fixe, la colonne changeait de hauteur à chaque maître et faisait « sauter »
la page au changement d'auteur. Boîte de gabarit constant (`height: 15rem;
object-fit: contain; object-position: bottom`) : même empreinte pour tous, sans
rogner les visages (le `contain` préserve l'intégralité de l'image, au prix d'un
peu d'espace transparent autour — sans cadre, il est invisible).

## 2026-07-09 — Portraits des maîtres : Wikimedia Commons, source secondaire d'illustration (décision utilisateur)

Les portraits qui accompagnent le nuage de « Les presque » sont sourcés sur
**Wikimedia Commons**. Statut fixé, non négociable :

- **Source SECONDAIRE D'ILLUSTRATION uniquement — jamais de donnée ni de
  comptage.** Même statut que le GeoJSON de la carte (décision 2026-07-08). Un
  portrait ne pèse sur aucun chiffre du projet ; il donne seulement un visage à
  la visualisation. La source canonique reste la base Joconde.
- **Stockage LOCAL, pas de hotlink** : les images sont téléchargées dans
  `web/static/portraits/` (versions ~480 px, ~2,8 Mo au total pour 27), servies
  par le site statique. Aucune dépendance live à un service tiers.
- **Licence vérifiée fichier par fichier** via l'API Commons (`imageinfo` →
  `extmetadata`). Résultat : 26 portraits en **domaine public**, 1 en **CC0**
  (Géricault). Toutes libres.
- **Crédit exigé par la licence affiché** (auteur + licence + « Wikimedia
  Commons », avec lien vers la page du fichier) **en légende sous chaque
  portrait**. Le manifeste `static/data/portraits.json` conserve, par maître :
  fichier local, auteur, licence, URL de licence, URL source Commons, QID
  Wikidata.
- **Placeholder propre** (silhouette neutre + mention « pas de portrait fiable
  disponible ») prévu pour tout maître sans portrait fiable. À ce jour les 27
  ont un portrait ; le placeholder est le filet de sécurité.
- **Légende d'attribution obligatoire** sous chaque portrait :
  « Les œuvres du nuage ne sont **pas attribuées avec certitude** au maître
  représenté. » — garde-fou contre le contresens « voici les tableaux de X ».

**Procédé (reproductible)** : `web/scripts/source_portraits.py`. Route
Wikidata (propriété P18 « image », qui ne pointe que vers des fichiers Commons
libres) → API Commons pour licence + auteur + miniature → téléchargement local
→ génération du manifeste. Les 27 QID ont été vérifiés à la main (recherche +
description) avant récupération. Rejouer le script régénère images + manifeste
à l'identique.

## 2026-07-09 — « Les presque » : portrait du maître à droite, flottant sans cadre (décision utilisateur)

Ajustement de mise en scène du nuage (`web/src/lib/NuageFamilles.svelte`). Un
portrait du maître accompagne désormais le graphe pour donner de la présence à la
visualisation. Deux choix arrêtés après examen du rendu :
- **Portrait à droite du graphe** (et non à gauche) : le nuage étant placé à la
  gauche du portrait, le maître « regarde » ses propres formules de doute. La
  vraie image (libre de droit, à sourcer) devra donc être **orientée vers la
  gauche** pour que le regard tombe sur le nuage.
- **Image flottante, sans cadre** : retrait de la bordure, du fond blanc et du
  padding ; suppression du fond opaque de la silhouette. Le portrait se pose dans
  la marge du graphe (`align-items: flex-end`) plutôt que d'être enfermé dans une
  vignette — moins « fiche signalétique », plus incarné.

En l'état, le portrait reste un **placeholder** (silhouette neutre) : l'effet de
regard ne sera visible qu'avec la vraie image. Aucune donnée ni aucun comptage
touché — pure présentation.

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

> **Section d'origine (phase 0), conservée comme trace.** Le suivi à jour vit
> dans `docs/roadmap.md` depuis le 2026-07-03. La forme pressentie ici pour la
> phase 3 (« carte D3.js + récit guidé ») a été remplacée par une application
> interactive SvelteKit portée par la dataviz (décisions des 2026-07-06 et
> 2026-07-07).

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
