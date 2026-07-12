# Décisions

Chaque décision est datée et motivée. Les plus récentes en haut.

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
