# Charte graphique — L'inventaire du doute

Source de vérité de la direction visuelle de **toute l'application-cadre**
*L'inventaire du doute*. Le dossier « Les presque » (périmètre V1 publique) est le
terrain principal pour l'éprouver ; la charte doit rester **extensible** aux
dossiers futurs (Avant / après, Vue d'ensemble, Méthode, autres formes de doute).

Direction arrêtée le 2026-07-15 / 16 (proposition validée, ambiance typographique
« Catalogue savant » choisie). Ce document précède l'implémentation : le code
`tokens.css` et les composants devront s'y conformer. En cas d'écart, ce document
fait foi et doit être mis à jour au même moment que le code.

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
  liste + microprofils) ; ne partage plus sa largeur avec une légende.
- **BandeauMaitre** — la « scène du maître » : portrait agrandi + nom + **phrase de
  synthèse calculée** + chiffres vedettes. (Nommé `BandeauMaitre` et **pas**
  `ProfilMaitre`, car « Profil » est un nom d'onglet — décision utilisateur.)
- **Onglets** — un seul composant (unifie la bascule des presque et les onglets
  révisions) ; libellés éditoriaux **Profil · Œuvres · Musées**.

**Dataviz — le principe « distance à la main »**
- **TroisTerritoires** — **primitive conceptuelle centrale** : ligne de proximité
  en 3 zones (au plus près / autour / dans son influence), fonds légers, familles
  chromatiques, annotations, volumes. Cadre commun au nuage, à la légende, à la
  Vue d'ensemble, aux futures cartes d'œuvres.
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

- **Prototype (en cours)** — BandeauMaitre + ChiffreVedette + onglets renommés
  Profil / Œuvres / Musées, appliqués à une **fiche maître réelle**. Sans toucher
  au répertoire, au nuage (pas de recadrage TroisTerritoires), ni à l'accueil.
- Zone Répertoire · Zone TroisTerritoires · Zone « Comprendre les mentions » ·
  Zone Accueil-couverture (figure Joconde) · Zone Méthode — **après** le prototype,
  une par une.

## 6. Application prioritaire à « Les presque »

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
