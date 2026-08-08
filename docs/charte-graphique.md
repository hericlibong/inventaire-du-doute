# Charte graphique — L'inventaire du doute

Source de vérité de la direction visuelle de **toute l'application-cadre**
*L'inventaire du doute*. Le dossier « Les presque » (périmètre V1 publique) est le
terrain principal pour l'éprouver ; la charte doit rester **extensible** aux
dossiers futurs (Avant / après, Vue d'ensemble, Méthode, autres formes de doute).

Direction arrêtée le 2026-07-15 / 16 (proposition validée, ambiance typographique
« Catalogue savant » choisie). Ce document précède l'implémentation : le code
`tokens.css` et les composants devront s'y conformer. En cas d'écart, ce document
fait foi et doit être mis à jour au même moment que le code.

> **Direction de COMPOSITION retenue le 2026-07-17 : B « la ligne de proximité ».**
> Après revue globale (trois directions maquettées), le parti de mise en page est acté :
> le sujet devient la structure — une **ligne horizontale continue** (token `--spectre`,
> composant `Spectre.svelte`), de la main du maître (chaud) à sa seule influence (froid),
> organise chaque page ; les huit pigments en sont les stations. Emprunts prévus :
> verbatims-matière + portrait N&B (dir. C), folios/cotes (dir. A). Typographie et pigments
> inchangés (« Catalogue savant »). Refonte **par pages complètes**. Détail et motifs :
> decisions.md 2026-07-17 (quinquies). Implémenté : coquille + accueil.

## 1. Concept et principes

**Concept : un inventaire, pas un tableau de bord.** Le langage visuel d'un
catalogue de musée / registre — papier crème, encre, filets fins, marges
généreuses, retenue. L'idée directrice de lecture : *la distance à la main du
maître* (la température des pigments encode le proche → lointain).

Principes (non négociables une fois la charte posée) :
1. **La couleur ne dit que du sens.** Les neutres font toute la structure ; un
   pigment n'apparaît que s'il encode une famille/catégorie. Pas de couleur
   décorative, pas d'arc-en-ciel.
2. **Position / longueur d'abord** pour les quantités ; taille et couleur en
   renfort (règle CLAUDE.md).
3. **La typographie porte l'identité**, pas des ornements d'interface.
4. **Légendes et labels expliquent** ; jamais d'encart « comment lire » séparé.
5. **Le blanc est une matière** : colonne mesurée (~66 caractères), de l'air
   autour des dataviz.
6. **Accessibilité native** : contrastes vérifiés, focus visible, jamais
   l'information par la seule couleur.
7. **Un cadre, plusieurs dossiers** : coquille + typo + espacements identiques
   partout ; chaque dossier reçoit un *emplacement d'accent*, pas une peau neuve.

## 2. Typographie (ambiance « Catalogue savant »)

Polices **libres (OFL), auto-hébergées** (woff2, sous-ensemble FR + poids utiles ;
pas de CDN — comme les portraits et les fonds de carte). Trois rôles :

| Rôle | Police | Emploi |
|---|---|---|
| **Titrage / chiffres vedettes / verbatims** | **Fraunces** (variable, `opsz`+`wght`) | h1–h3, grands nombres, citations littérales des notices |
| **Texte éditorial courant** | **Spectral** (serif humaniste, lisible à l'écran) | chapôs, paragraphes, bios |
| **UI, données, labels, chiffres** | **Public Sans** (sans neutre ; IBM Plex Sans en alternative) | nav, boutons, axes, tooltips, tableaux, étiquettes |

Règles typographiques :
- **Chiffres tabulaires** (`font-variant-numeric: tabular-nums`) partout où il y a
  des nombres (axes, légendes, tableaux, chiffres vedettes).
- **Kickers / étiquettes en petites capitales** (la signature « étiquette
  d'inventaire ») — portés par le sans.
- **Échelle typographique modulaire** définie en tokens (voir §4), longueur de
  ligne bornée.
- Georgia + `system-ui` (réglages par défaut actuels) sont **abandonnés** : c'est
  le principal facteur de l'effet « pas encore designé » (voir mémoire
  `style-front-non-normé`).

## 3. Palette (trois étages, sans élargir les teintes)

**Étage 1 — structure (neutres)** : fond crème `#f7f4ef` ; surface carte
`#fffdf9` (blanc-papier, pas blanc pur) ; encre `#1c1a17` ; encre douce `#5c554c` ;
filet `#ddd6ca` (+ un filet plus clair pour traits secondaires). Nouveaux tokens :
surface, ombre très douce, anneau de focus.

**Étage 2 — accent éditorial** : terre brûlée `#7a4a2b` (liens, actions, wordmark).

**Étage 3 — couleurs sémantiques** :
- **Boîte de pigments du doute** : les 8 formes, **inchangées** (le joyau du
  projet : luminosité alternée, daltonisme vérifié, température = distance au
  maître). Voir `tokens.css` et decisions.md 2026-07-11/12.
- **Accents par dossier** (mécanisme d'extensibilité) : `--accent-presque` (la
  gamme pigments), `--accent-revisions` `#6b5b7a`, `--accent-copie` `#6b6f76`.

**Règle d'or couleur** : on n'ajoute pas de teinte « pour décorer ». La discipline
chromatique **est** l'identité.

## 4. Tokens à ajouter (aujourd'hui absents de tokens.css)

Actuellement `tokens.css` ne porte que des couleurs et deux polices. À compléter :
- **Espacement** : échelle `--espace-1 … --espace-6` (rythme unique, fin des
  marges au jugé).
- **Rayons** : `--rayon-s`, `--rayon-m`.
- **Filets** : épaisseur + couleurs (principal / secondaire).
- **Ombre douce** : une seule élévation discrète (cartes).
- **Anneau de focus** : token unique, réutilisé partout.
- **Échelle typographique** : `--taille-…` + interlignes.

## 5. Composants communs (le kit) — validé le 2026-07-16

Kit **au service de l'architecture éditoriale** (`architecture-editoriale.md`),
pas un catalogue abstrait. Chaque primitive reste agnostique du dossier.

**Fondations éditoriales**
- **Kicker** — étiquette en petites capitales (Public Sans), option pastille de
  pigment ; matérialise la couche de libellé public (`familles-public.js`,
  `revisions-labels.js`).
- **ChiffreVedette** — grand nombre (Fraunces, tabulaire) + légende courte.
- **EnTeteSection** — kicker + titre (Fraunces) + chapô (Spectral) ; distingue
  accueil / exploration / méthode.
- **Filet** — séparateur fin (utilitaire).
- **Lien POP / Bouton** — lien normé « Consulter la notice sur POP → » + boutons.

**Navigation & profil**
- **Repertoire** — colonne de gauche d'« Explorer les maîtres » (recherche + tri +
  liste + microprofils) ; ne partage plus sa largeur avec une légende. **Fait le
  2026-07-17** (`Repertoire.svelte` : tri Œuvres/A→Z, sélection active à filet
  d'accent, repliable en mobile ; légende retirée de sous la liste).
- **BandeauMaitre** — la « scène du maître » : portrait + **court portrait éditorial
  fondé sur les données** (Nommé `BandeauMaitre` et **pas** `ProfilMaitre`, car « Profil »
  est un nom d'onglet — décision utilisateur.) Forme arrêtée le **2026-07-20**, elle
  remplace la pile de compteurs du 2026-07-19 (bis) : **plus aucun grand nombre isolé,
  aucun compteur, aucune carte de KPI**. Ordre de lecture :
  1. **nom** (`--taille-xxl`, élément le plus grand — aucun nombre ne le concurrence) ;
  2. **la mention la plus fréquente**, constat en Fraunces ~1,35 rem : deuxième niveau
     visuel, et conclusion que le graphique vient ensuite détailler ;
  3. **récit chiffré** en corps de lecture (volume, part, musées) ;
  4. **repère méthodologique** en petit corps atténué, après un filet fin.
  **Sans portrait, la colonne de gauche n'existe pas** (2026-08-06) : le texte prend la
  largeur des deux colonnes réunies. Ni image de remplacement, ni mention d'absence —
  une image posée à l'emplacement du visage affirmerait, sur la fiche d'un artiste dont
  les œuvres ne lui sont pas directement attribuées, ce que le texte refuse d'affirmer ;
  et l'absence n'a pas à être commentée. Vingt-neuf fiches sur cent deux sont dans ce cas.
  Les nombres sont **intégrés aux phrases** : graisse 600 + `--accent-cobalt` + chiffres
  elzéviriens, jamais plus grands que le texte. Phrases **générées** (`artistes.json` +
  champ `citation` de `familles-public.js`) : égalités citées toutes, ordre `ORDRE_FAMILLES` ;
  cas 100 % (« portent toutes cette mention ») et musée unique gérés. Pourcentages en
  `Math.round` ; `fractionEnMots` proscrite. Bio conservée en ligne d'identité si elle existe.
  **Vocabulaire** : narratif en « œuvres associées à son nom » (jamais « œuvres de X »),
  comptages secs en « notices » ; proscrits : « domine », « le doute passe par ».
- **Onglets** — un seul composant (unifie la bascule des presque et les onglets
  révisions) ; libellés éditoriaux **Profil · Œuvres · Musées**.

**Dataviz — le principe « distance à la main »**
- **TroisTerritoires** — **primitive conceptuelle centrale** : ligne de proximité
  en 3 zones (au plus près / autour / dans son influence), fonds légers, familles
  chromatiques, annotations, volumes. Cadre commun au nuage, à la légende, à la
  Vue d'ensemble, aux futures cartes d'œuvres. **Fait le 2026-07-17 (bis)** : primitive
  de données `territoires.js` (regroupement + annotations) + intégration dans le nuage
  (bandes, séparateurs, titres) + clé de lecture. Réutilisable par « Comprendre les
  mentions ». Une éventuelle extraction en composant SVG partagé reste ouverte (pas
  nécessaire tant que seul le nuage la rend — decisions.md 2026-07-17 bis).
- **Barre** — unifie `BarreFamilles` + `BarreNiveaux` (+ variante microprofil).
- **Legende** — `LegendeFamilles` généralisée (pastille + label + nombres) ;
  contextuelle dans le profil, autonome dans « Comprendre les mentions ».
- **Infobulle** — gardée telle quelle (déjà unifiée).
- **Nuage** (`NuageFamilles`) — conservé, **recadré dans TroisTerritoires**.
- **CarteMaitre** (carte **géographique** par maître) — conservée, spécialisée,
  repassée aux tokens (ce n'est PAS une carte-fiche).

**Média** (ossature seulement ; contenu différé)
- **Carte** (fiche d'œuvre) + **Vignette/Placeholder** — squelette à slot média,
  absorbe `CarteRevision` + `VignetteOeuvre` (galeries d'œuvres, plus tard).
- **PortraitMaitre** — conservé (image + légende), agrandi dans le bandeau.

Gouvernance : une source unique de libellés et de couleurs par catégorie. Au
placard : `GalaxieMaitre` (abandonné).

### Découpage en zones (implémentation par petites étapes, validation à chaque)

- **Prototype (fait le 2026-07-16 quinquies, ⏸ à valider)** — `BandeauMaitre` +
  `ChiffreVedette` + onglets renommés Profil / Œuvres / Musées, appliqués à la
  **fiche maître réelle**. Sans toucher au répertoire, au nuage (pas de recadrage
  TroisTerritoires), ni à l'accueil. Deux points ouverts à l'arbitrage :
  synthèse calculée réintroduite (factuelle) et plafond de `fractionEnMots`
  (voir decisions.md 2026-07-16 quinquies).
- Zone Répertoire **(faite le 2026-07-17)** · Zone TroisTerritoires **(faite le
  2026-07-17 bis)** · Zone « Comprendre les mentions » **(faite le 2026-07-17 ter :
  route `/echelle`, page autonome à 4 parties, `BarresMentions.svelte`)** · Zone
  Accueil-couverture (figure Joconde) · Zone Méthode — **après** le prototype, une
  par une.

## 6. Application prioritaire à « Les presque »

> **Titre public (2026-07-19) : « Explorer les N maîtres ».** Le nombre est **lu dans les
> données**, jamais écrit en dur : il est passé de 27 à **63** le 2026-07-22 et bougera à
> chaque lot de maîtres instruits. L'appellation « Les
> presque » est **abandonnée dans les textes publics** ; elle ne subsiste que comme
> **nom de code interne** (docs, fichiers, exports — non renommés). **La route publique,
> elle, est passée à `/artistes` le 2026-08-08** ; `/les-presque` redirige en 308. Le nom
> interne n'a pas été pourchassé pour autant : un refactor sans bénéfice visible n'en
> est pas un.
> La page s'ouvre en **deux temps** : (1) entrée éditoriale (titre + texte, deux colonnes
> sur ordinateur, sans encadré, prudence en note discrète), puis (2) exploration
> introduite par l'intitulé **« Choisir un artiste »**, détachée par un **filet + de
> l'espace** (jamais un bandeau décoratif). Vocabulaire : « artistes » dans le texte
> explicatif, « maîtres » dans le titre et la nav. Détail : decisions.md 2026-07-19.

Petites étapes, validation à chaque palier :
1. **Tokens + typographie** posés dans `tokens.css`.
2. **Coquille** (`+layout`) refaite en « inventaire » : bandeau-titre serif +
   sous-titre de dossier, filet, nav sobre.
3. **Kit** appliqué à la fiche maître (onglets, cartes, légende, jauges, tooltips,
   portrait) — sans toucher aux données.
4. **Idée « distance à la main »** rendue lisible (axe du nuage + légende).
5. **Accueil du dossier** stylé comme entrée.
6. **Vérif** : contraste, focus, mobile, lisibilité des dataviz.

## 7. Extensibilité (règles pour les dossiers futurs)

- Le **cadre** (coquille, typo, espacements, filets, primitives) est agnostique du
  dossier.
- Un dossier déclare un **accent** (`--accent-dossier`) et, si besoin, son **jeu de
  couleurs sémantiques** via un module de libellés (patron `revisions-labels.js`).
  Le *mécanisme* de la boîte de pigments se généralise, même si la gamme des 8 est
  propre aux presque.
- **Vue d'ensemble** réutilise tel quel : chiffre vedette + barres + légende +
  kicker (**pas d'anneau** — familles non partitionnées, acté 2026-07-15).
- **Avant / après** (en réserve) héritera du kit unifié à sa reprise.
- **Méthode** : pur type + filets + tableaux, zéro composant neuf.
- **Règle d'or** : un dossier ajoute une palette sémantique et de la copie
  éditoriale, mais **réutilise le cadre et les primitives** — jamais de reskin par
  dossier.

## 8. Patron « carte + panneau » — arrêté le 2026-08-06

**À reprendre tel quel dans les prochains volets.** Ce patron a été mis au point sur
la carte des musées d'une fiche d'artiste (`CarteMaitre.svelte`) ; il vaut pour toute
carte qui répond à la question « où ». Ce qui suit n'est pas un récit de ce qui a été
fait, c'est la règle à appliquer.

### Ce que la carte dit, et ne dit pas
- Une carte de ce projet est un **repère géographique**, jamais un graphique de
  répartition et jamais une comparaison entre lieux. Un point = un lieu, présence.
- **Tous les points ont la même taille.** Une taille proportionnelle rendrait un
  « gros cercle » incomparable d'une fiche à l'autre et gonflerait les petits volumes.
  Le combien se lit dans le panneau, jamais dans l'aire d'un cercle.
- **La carte existe même à un seul point.** Un point unique situe aussi sûrement que
  vingt ; l'échelle ne bouge pas, la projection est calée sur le fond, jamais sur les
  points.
- Le fond (régions, contours) est une **illustration** : aplat quasi nul, filet gris
  pâle, aucune donnée, aucune tuile en ligne.
- Les points qui se recouvrent sont **écartés au plus près de leur vraie position**
  (`geo.js`, `ecarterPoints`) : aucun point n'en cache un autre.

### Un seul espace d'information
- **Pas d'infobulle.** Rien ne suit le pointeur, rien ne se superpose à la carte. Une
  bulle s'efface au premier mouvement, recouvre le titre, et n'existe pas au toucher.
- Le **panneau au flanc** porte tout : le compte, la ventilation, les liens, la
  fermeture. C'est le seul endroit où l'information s'écrit.
- **Le survol n'informe pas, il annonce.** Il dit « ce point se choisit », rien d'autre.

### Les quatre états du point
| État | Ce qu'on voit |
|---|---|
| repos | opacité 0,82, contour blanc 1,1 px |
| survol | ×1,5, contour 2 px, pleine opacité, curseur `pointer` ; les autres points tombent à 0,55 |
| focus clavier | **exactement le même retour**, plus l'anneau de focus (2 px encre, offset 3 px) |
| choisi | cerne d'encre 2,4 px, pleine opacité — le seul état **persistant** |

- L'agrandissement passe par une **transformation** (`transform-box: fill-box`,
  `transform-origin: center`), pas par le rayon : `r` s'anime irrégulièrement d'un
  navigateur à l'autre.
- Transition 0,12 s, supprimée sous `prefers-reduced-motion`.
- L'atténuation des autres points reste **légère** : elle détache le point visé sans
  effacer la répartition, qui est le sujet de la carte.

### Le panneau
- **Deux zones.** En-tête sur aplat `--surface-entete` pleine largeur (nom en gras,
  lieu dessous en `--taille-xs` encre douce), filet dessous ; corps sur
  `--surface-carte`. Le retrait appartient à chaque zone, pas au panneau —
  `overflow: hidden` fait suivre les angles arrondis à l'aplat.
- **Prévoir les noms longs** : `overflow-wrap: anywhere` dans l'en-tête (le plus long
  du corpus fait 84 signes).
- Le gris de l'en-tête est **neutre**. Jamais une couleur de la boîte de pigments :
  elle appartient aux catégories, elle ne décore rien.
- Ordre du corps : le compte · la ventilation (triée par valeur, pastille de la
  couleur stable) · l'action · le lien externe éventuel · « Fermer ».

### Le comportement
- Le panneau s'ouvre au **clic, à Entrée, à Espace et au toucher** — un point est
  `role="button"`, `tabindex="0"`, avec un `aria-label` qui dit d'avance tout ce que
  le panneau contiendra.
- **Choisir n'est pas un bascule** : choisir deux fois le même lieu ne referme pas.
  Au toucher, un second appui involontaire effaçait ce qu'on venait d'ouvrir.
- Choisir un autre lieu **remplace** le contenu. Seul « Fermer » ferme.
- Changer d'entité (d'artiste, de dossier) referme le panneau : une clé de lieu ne
  vaut que dans le contexte où elle a été choisie.
- **Sans sélection**, le flanc porte deux lignes : ce que représente un point, puis
  l'invitation à en choisir un. Jamais un mode d'emploi du survol.
- Sur petit écran (≤ 720 px), la grille se replie et **le panneau passe sous la carte**.

### Le vocabulaire
- Côté lecteur, on parle d'**œuvres**, jamais de notices (É1, 2026-08-03). L'unité de
  calcul ne change pas pour autant.
- Le titre de la vue pose une question de lieu : « Où sont conservées ces œuvres ? ».
- Les intitulés d'action s'accordent : « Voir l'œuvre conservée dans ce musée » /
  « Voir les N œuvres conservées dans ce musée ».

### Les positions, côté données
- **Une position par lieu, valable partout.** Joconde publie parfois plusieurs
  positions sous le même code : on regroupe les positions voisines (< 15 km), on garde
  la grappe qui porte le plus de notices, puis la plus fréquente dedans
  (`build_artistes.coord_du_musee`). Jamais « la première rencontrée » : le lieu se
  mettrait à changer de place d'une fiche à l'autre.
- **Contrôler avant de publier** : `uv run python src/audit_geoloc.py` compare chaque
  position au centre de sa commune (référence de contrôle, jamais de données). À
  lancer après chaque lot.

## 9. Liens éditoriaux — arrêté le 2026-08-08

Le bleu cobalt (`--accent-cobalt`) **sert deux choses à la fois**, et c'est assumé : il
signale une **information importante** (les nombres dans une phrase — « 310 œuvres »,
« 19 musées ») et un **lien**. C'est un choix de l'utilisateur, pris le 2026-08-08 contre
la solution qui aurait réservé la couleur aux liens.

Il en découle une règle, non négociable : **la distinction ne repose jamais sur la seule
couleur.**

- **Un lien éditorial dans du texte est souligné en permanence**, dès l'état de repos.
  Soulignement natif (`text-decoration`), 1 px, couleur cobalt à 45 %, décalé de `0.18em`
  pour épargner les jambages.
- **Au survol et au focus**, le trait s'épaissit à 2 px et passe au cobalt plein. On
  n'utilise pas de `border-bottom` : il déplacerait le texte en s'épaississant.
- **Les nombres mis en valeur restent en cobalt et en gras, jamais soulignés.** Le trait
  devient ainsi le seul signe de ce qui se clique.
- **Ce qui a déjà son propre traitement visuel n'est pas souligné** : onglets, boutons,
  cartouches de la couverture, appels à l'action sur aplat plein (`.entree`), sommaire par
  ancres, navigation. Un bouton n'a pas besoin d'un trait pour se signaler.
- **Les flèches ne sont pas une convention** : celle qui suivait « Comment ces artistes
  ont-ils été sélectionnés ? » a été retirée parce qu'elle n'ajoutait rien après un point
  d'interrogation. Les autres — appels à l'action, renvois vers une fiche externe — sont
  conservées.

Portée : pages « Le projet », « Méthode » et « Explorer les artistes » (`.tete a`,
`.contenu a`, le renvoi de l'exploration). Récit daté : decisions.md, 2026-08-08 bis.

## 10. Le ruban de composition (répertoire) — arrêté le 2026-08-08

Dans le répertoire des artistes, chaque ligne porte un **ruban court** qui montre la
répartition des mentions de cet artiste — et **rien d'autre**.

- **La quantité n'est pas dans le ruban.** Elle est portée par le nombre affiché à droite
  du nom et par l'ordre du classement. Le ruban a donc **la même longueur pour tous**,
  quel que soit l'effectif.
- **Il est court et calé à gauche** : 96 px, soit moins d'un tiers de la colonne. Il ne
  rejoint jamais le nombre. C'est cette distance qui l'empêche d'être lu comme une jauge —
  une bande qui remplit sa ligne se lit toujours comme un remplissage.
- **Ses segments sont détachés** (1,5 px de blanc, coins de 1 px). Une barre de progression
  est continue ; celle-ci ne l'est pas.
- **Plancher de visibilité : 3 px par mention présente**, l'excédent étant repris au
  prorata sur les segments majoritaires. Écart assumé et déclaré : sans lui, une mention
  à 0,6 % — le « nom (?) » de Charles Le Brun — occuperait 0,6 pixel, c'est-à-dire rien.
  La hiérarchie entre mentions n'est jamais modifiée.
- **Aucune interaction.** Le ruban est décoratif (`aria-hidden`), sans `role`, sans
  `tabindex`, sans infobulle. Le répertoire est un outil de recherche et de sélection :
  la seule cible cliquable d'une ligne est la ligne elle-même.
- Couleurs et ordre des mentions : ceux de la charte, identiques au graphique du profil.

Récit daté : decisions.md, 2026-08-08 ter.
