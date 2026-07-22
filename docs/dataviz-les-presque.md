# La dataviz « Les presque » — état actuel (technique & esthétique)

Document autonome destiné à être **analysé de l'extérieur** (par un tiers ou un
autre outil). Il décrit, sans supposer la connaissance du code, ce qu'est
aujourd'hui la première dataviz du projet, comment elle est faite, à quoi elle
ressemble, et **en quoi elle s'éloigne encore de la vision visée** (une
« galaxie » et un récit, pas un tableau de bord technique).

État daté du 2026-07-08. Route concernée : `/les-presque`.

> **Mise à jour du 2026-07-22 — l'axe vertical a changé de nature.** Le graphique de la
> fiche maître (`NuageFamilles.svelte`, qui a remplacé la galaxie décrite en §7) portait le
> **nombre** d'œuvres sur un plafond commun à tous les maîtres, égal au maximum observé
> (240). Il porte désormais la **part des œuvres concernées du maître, de 0 à 100 %**.
>
> Motif : la liste est passée de 27 à 63 maîtres, allant de **11 à 310** notices prudentes.
> Sur une échelle absolue graduée jusqu'à 240, la moitié des profils s'écrasaient au sol —
> Botticelli (17 notices) affichait quatre points indistinguables sur la ligne de base. La
> règle du projet est double : échelle **commune et fixe** entre entités comparées, ET
> lisibilité d'une hiérarchie. L'échelle absolue ne pouvait plus tenir les deux ; la part
> les tient. La comparaison porte sur la **forme** du profil ; le volume reste écrit dans
> l'en-tête, dans le classement du répertoire et dans chaque infobulle.
>
> Détail et mesures : `docs/decisions.md`, 2026-07-22 (quater).

---

## 1. Ce que cette dataviz veut faire

**Projet englobant.** « L'inventaire du doute » lit la base Joconde (collections
des musées de France, données ouvertes) et repère les œuvres dont l'auteur est
**incertain** — celles où les musées écrivent « attribué à », « école de »,
« atelier de », « ? », etc. La question centrale : combien d'œuvres portent une
mention d'incertitude, lesquelles, où, sous quelles formules.

**Rôle de « Les presque » dans l'ensemble.** C'est l'**entrée par l'artiste** :
prendre un grand maître célèbre (Rembrandt, Poussin, Rubens…) et montrer toutes
les œuvres que les musées **ne lui attribuent pas tout à fait**. Angle éditorial :
« voici comment les musées nuancent autour d'un nom », **jamais** « trésor caché »
ou « chef-d'œuvre oublié ».

**Règles non négociables qui contraignent la forme :**
- le projet **n'authentifie rien**, n'émet aucun avis d'attribution ; il restitue
  ce que les musées ont eux-mêmes publié ;
- jamais de valeur marchande, pas de sensationnalisme ;
- les copies assumées (« d'après X ») ne sont **pas** des doutes : elles doivent
  être montrées à part.

**Intention visuelle initiale (la « galaxie »).** Une maquette existe
(`images/maquette_galaxie.png`) : le maître au centre, chaque œuvre incertaine en
orbite, plus l'attribution est probable plus elle est proche, plus le doute est
fort plus elle est loin ; les copies « d'après » en anneau extérieur. L'idée est
**narrative et sensible** (une constellation autour d'un nom), pas un graphique
d'analyste.

---

## 2. Les données consommées

Un seul fichier : `data/exports/web/artistes.json` (~44 Ko), généré par le
pipeline Python (`src/build_artistes.py`) à partir de la base Joconde. Il n'est
**pas** recalculé côté front : le front ne fait que le lire.

**Sélection : 63 maîtres** (2026-07-22 ; 27 à l'origine) retenus sur le critère « maître
de référence **ET** ≥ 10 notices prudentes uniques, hors copie, après regroupement des
graphies ». L'effectif est **lu dans les données**, jamais écrit en dur : il bougera à
chaque lot instruit. Ce ne sont donc pas tous les artistes de la
base, mais une liste vedette curatée.

**Structure (par maître) :**
```json
{
  "nom": "Charles Le Brun",
  "propre": 3034,        // attributions fermes à ce nom
  "doute": 310,          // notices de doute rattachées au nom
  "copie": 354,          // « d'après X » — copies, comptées à part
  "musees": 64,
  "niveaux": [54, 256, 0],   // doute ventilé sur l'échelle à 3 niveaux
  "familles": [
    { "code": "attribue", "libelle": "attribué à", "niveau": 1, "notices": 52 },
    { "code": "ecole_de", "libelle": "école de", "niveau": 2, "notices": 240 },
    ...
  ],
  "exemples": [
    { "reference": "000PE001736", "titre": "L'AUTOMNE",
      "musee": "musée du Louvre", "ville": "Paris",
      "extrait": "LE BRUN Charles (atelier)" }
    // une notice réelle par famille, avec lien vers la notice publique POP
  ]
}
```

**L'échelle du doute à 3 niveaux** (définie ailleurs dans le projet, `docs/typologie.md`) :
| Niveau | Libellé actuel | Sens |
|---|---|---|
| 1 | **Presque lui** | l'attribution est probable mais non certaine (« attribué à », « ? ») |
| 2 | **Autour de lui** | son atelier, son école, son entourage |
| 3 | **Son style, sans lui** | sa manière, son genre, un suiveur |

**Point important pour l'analyse :** les `familles[].libelle` viennent directement
du lexique de détection. Certains sont bruts et **techniques** — par ex.
`"atelier (qualificatif, beaux-arts)"`, `"? (point d'interrogation)"`,
`"école-lieu consacrée (écartée)"`. Tels quels à l'écran, ils sonnent comme du
vocabulaire d'ingénierie de données, pas comme un récit.

---

## 3. Forme technique actuelle

**Stack.** SvelteKit (Svelte 5), build **entièrement statique** (`adapter-static`,
tout est pré-rendu en HTML). Aucun serveur applicatif. Le front vit dans `web/`,
isolé du pipeline Python ; il consomme les JSON via `fetch('/data/artistes.json')`.

**Fichiers de cette brique :**
- `web/src/routes/les-presque/+page.js` — charge `artistes.json`.
- `web/src/routes/les-presque/+page.svelte` — la page : intro, liste des maîtres,
  fiche du maître sélectionné, bascule entre deux vues.
- `web/src/lib/GalaxieMaitre.svelte` — la vue « galaxie » (SVG).
- `web/src/lib/BarreNiveaux.svelte` — barre empilée des 3 niveaux (réutilisable).
- `web/src/lib/joconde.js` — helpers : lien POP, métadonnées des 3 niveaux,
  formatage des nombres.
- `web/src/lib/styles/tokens.css` — couleurs et typographie partagées.

**Structure de la page (mise en page à deux colonnes) :**
1. **En-tête de page** : titre « Les presque », un chapô explicatif, un
   « mode d'emploi » (« 👉 Choisissez un maître… »), une ligne sur le critère de la liste.
2. **Colonne gauche** : un champ de filtre + la **liste des maîtres**. Chaque
   entrée montre le nom, le nombre de doutes, et une mini-barre des 3 niveaux.
   Cliquer sélectionne le maître.
3. **Colonne droite (la « fiche »)** : nom, une phrase de résumé (X doutes sur Y
   attributions, dans Z musées), puis une **bascule « Galaxie / Détail »** :
   - **Galaxie** (vue par défaut) : le composant SVG décrit au §4 ;
   - **Détail** : l'échelle du doute (barre + légende), un **tableau** des formules
     (colonnes Formule / Niveau / Notices), une bande « d'après X » (copies, à
     part), et une liste de notices réelles avec liens vers POP.

**Interactions.** Tout est côté client, sans rechargement : filtre texte,
sélection d'un maître, bascule de vue. Aucune animation. La « recherche » ne porte
que sur les **maîtres retenus** (un moteur sur toute la base de noms demanderait un
autre export, pas encore produit).

**Encodage de la galaxie (paramètres réels, `GalaxieMaitre.svelte`) :**
- SVG `viewBox 0 0 440 440`, centre (220, 220), largeur max ~30 rem.
- 3 **orbites** en pointillés, une par niveau : rayons 66 / 106 / 146 px
  (niveau 1 le plus proche du centre).
- 1 **anneau extérieur** en pointillés (rayon 184) pour les copies « d'après ».
- **Une bulle par famille** posée sur l'orbite de son niveau, répartie en angle
  (`i / nbFamilles × 360°`). Rayon de bulle = `min(22, 5 + √notices × 0.9)`
  (racine carrée pour ne pas écraser les petites familles).
- **Centre** : disque blanc cerclé, nom du maître + « N en doute ».
- Chaque bulle porte une étiquette texte (« libellé · nombre ») et une info-bulle.
- Une phrase de lecture sous le dessin : « position indicative, pas une mesure
  d'authenticité ».

**Note d'honnêteté sur l'encodage.** Une bulle = **une famille de formules**, pas
une œuvre. Le nombre d'œuvres n'est rendu que par la **taille** de la bulle. La
maquette, elle, suggérait plutôt un semis de points (une œuvre = un point). C'est
un premier écart entre l'intention et la réalisation.

---

## 4. Forme esthétique actuelle

**Palette (`tokens.css`).** Fond crème `#f7f4ef`, encre `#1c1a17`, accent brun
`#7a4a2b`. **Échelle du doute** en dégradé chaud terre → sable :
niveau 1 `#b8551f`, niveau 2 `#d98a3d`, niveau 3 `#e8c07a`. Copies en bleu-gris
`#4a6b7a`, révisions en violet `#6b5b7a` (non utilisé ici).

**Typographie.** Titres en serif (Georgia), texte en sans-serif système. Nombres
en chiffres tabulaires.

**Registre visuel.** Sobre, éditorial, lisible. **Mais** — et c'est le cœur du
retour utilisateur — l'ensemble reste **générique** (« ça ressemble à toutes les
interfaces générées par IA ») et **trop technique** dans ses mots : les libellés
de familles, les colonnes « Niveau / Notices », le mot « notices » lui-même
appartiennent au vocabulaire de la donnée, pas à celui d'un récit grand public.

**Ce qui marche déjà (retour utilisateur du 2026-07-08) :** la galaxie est jugée
**lisible** ; le principe proche/loin passe.

**Ce qui ne va pas encore :**
1. **Le style** est à refaire — identité visuelle propre, non générique, attendue
   (formulé à plusieurs reprises ; à traiter, mais après les briques).
2. **Les labels sont trop techniques** : ils exposent la mécanique de détection
   (« atelier (qualificatif, beaux-arts) », « niveau 2 », « notices ») au lieu de
   raconter (« œuvres sorties de son atelier », « on lui a longtemps prêté cette
   toile »…).
3. **Distance à la vision « galaxie »** : le rendu actuel est une figure
   d'orbites propre et statique ; l'intention était une **constellation** plus
   sensible, où l'on ressent la masse des « presque » autour d'un nom (semis
   d'œuvres, profondeur, peut-être mouvement).
4. **Le récit manque** : la page juxtapose des éléments (liste, galaxie, tableau)
   sans fil narratif ; on n'entre pas dans une histoire, on consulte une fiche.

---

## 5. Écarts entre l'intention et l'état actuel (synthèse pour l'analyse)

| Axe | Intention | État actuel | Écart |
|---|---|---|---|
| Métaphore | Galaxie / constellation sensible | Diagramme d'orbites propre | Trop « schéma », pas assez « ciel » |
| Grain | Une œuvre = un point (maquette) | Une famille = une bulle | On perd la masse, le fourmillement |
| Mots | Récit grand public | Vocabulaire de la donnée | Jargon technique à l'écran |
| Style | Identité propre, singulière | Générique « IA » | À refondre |
| Structure | Récit qui emmène | Fiche que l'on consulte | Pas de fil narratif |
| Émotion | Le vertige du doute | Lecture neutre | Manque d'intention sensible |

---

## 6. Ce sur quoi un regard extérieur serait utile

1. **La métaphore galaxie** est-elle la bonne, et comment la rendre plus sensible
   sans trahir la rigueur (position « indicative », pas une mesure d'authenticité) ?
   Faut-il passer à **une œuvre = un point** (semis) plutôt qu'une bulle par famille ?
2. **Comment dé-jargonniser les labels** tout en restant exact ? (Reformuler les
   familles et les niveaux en langage courant, sans mentir sur ce qu'ils recouvrent.)
3. **Quel récit** peut porter cette entrée « par l'artiste » ? Par où entre le
   visiteur, que ressent-il, où va-t-il ensuite ?
4. **Quelle direction esthétique** donnerait une identité propre (hors du registre
   générique), cohérente avec un sujet patrimonial et l'idée de doute ?

---

## 7. Spécification technique (pour analyse par une autre IA)

Section formelle et exhaustive. Objectif : qu'un agent puisse **reconstruire ou
critiquer** l'implémentation sans lire le dépôt. Toutes les valeurs ci-dessous
sont celles réellement dans le code au 2026-07-08.

### 7.1 Environnement & dépendances

```
Runtime      : Node.js 22.x
Framework    : SvelteKit (Svelte 5, runes activées)
Bundler      : Vite 8
Rendu        : 100 % statique (prerender), aucun serveur, aucune API runtime
Racine front : web/
```
`package.json` (devDependencies) :
```
@sveltejs/adapter-static ^3.0.10
@sveltejs/kit            ^2.63.0
@sveltejs/vite-plugin-svelte ^7.1.2
svelte                   ^5.56.1
vite                     ^8.0.16
```
Particularité Svelte 5 / Kit récent : **pas de `svelte.config.js`**. L'adapter et
les `compilerOptions` sont câblés dans `vite.config.js` via
`sveltekit({ adapter: adapter(), compilerOptions: { runes: … } })`.
`export const prerender = true;` est posé une fois dans `src/routes/+layout.js`.
Sortie de build : `web/build/`, la route est écrite en `build/les-presque.html`.

### 7.2 Flux de données

```
Pipeline Python (hors périmètre front)
  └─ data/exports/web/artistes.json
       └─ npm run sync:data  (copie ⇒ web/static/data/artistes.json)
            └─ +page.js: fetch('/data/artistes.json')  [au build, prerender]
                 └─ +page.svelte reçoit `data.artistes`
```
Le front est **lecture seule** : aucun recalcul, aucune agrégation. Toute la
sémantique (comptage du doute, niveaux, exclusions) est figée en amont dans le JSON.

### 7.3 Schéma de `artistes.json`

```jsonc
{
  "critere": "string",         // libellé du critère de sélection des vedettes
  "lexique": "string",         // version du lexique de détection (traçabilité)
  "version_donnee": "YYYY-MM-DD",
  "date_generation": "ISO-8601",
  "source": "string",
  "url_source": "string(url)",
  "niveaux": {                 // dictionnaire libellés des 3 niveaux
    "1": "Presque lui",
    "2": "Autour de lui",
    "3": "Son style, sans lui"
  },
  "artistes": [ Artiste ]      // longueur = effectif de la liste, triés par doute décroissant
}

Artiste = {
  "nom":    "string",
  "propre": "int >= 0",        // attributions fermes au nom
  "doute":  "int >= 20",       // total doute (= somme de familles[].notices de catégorie doute)
  "copie":  "int >= 0",        // « d'après X » (hors doute)
  "musees": "int >= 1",
  "niveaux": [n1, n2, n3],     // ints ; n1+n2+n3 == doute ; index 0 => niveau 1
  "familles": [ Famille ],     // 1..n, uniquement les familles présentes pour ce maître
  "exemples": [ Exemple ]      // ~1 par famille
}

Famille = {
  "code":    "string",         // identifiant stable (ex. "attribue", "ecole_de")
  "libelle": "string",         // libellé lisible MAIS technique (ex. "atelier (qualificatif, beaux-arts)")
  "niveau":  1 | 2 | 3,        // rattachement à l'échelle du doute
  "notices": "int >= 1"
}

Exemple = {
  "reference": "string",       // identifiant notice Joconde (ex. "000PE001736")
  "titre":     "string",
  "musee":     "string",
  "ville":     "string",
  "extrait":   "string"        // texte brut du champ Auteur, ex. "LE BRUN Charles (atelier)"
}
```
Invariants exploitables : `sum(niveaux) == doute` ; chaque `famille.niveau`
correspond à l'index dans `niveaux` (`niveau 1 → niveaux[0]`). `copie` n'entre
jamais dans `doute` ni dans `niveaux`.

### 7.4 Arbre des fichiers front (brique concernée)

```
web/
├─ vite.config.js                 # adapter static + runes
├─ src/
│  ├─ routes/
│  │  ├─ +layout.js               # export const prerender = true
│  │  ├─ +layout.svelte           # coquille : header, nav, footer
│  │  └─ les-presque/
│  │     ├─ +page.js              # load(): fetch artistes.json
│  │     └─ +page.svelte          # la page (liste + fiche + bascule)
│  └─ lib/
│     ├─ joconde.js               # lienPop(), NIVEAUX[], nombre()
│     ├─ BarreNiveaux.svelte      # barre empilée 3 niveaux
│     ├─ GalaxieMaitre.svelte     # vue galaxie (SVG)
│     └─ styles/tokens.css        # variables CSS (couleurs, typo)
```

### 7.5 Contrats des composants

**`joconde.js`** (module) :
```js
lienPop(reference) => `https://pop.culture.gouv.fr/notice/joconde/${reference}`
NIVEAUX = [
  { n:1, libelle:'Presque lui',           variable:'--niveau-1', sens:"l'attribution est probable mais non certaine" },
  { n:2, libelle:'Autour de lui',         variable:'--niveau-2', sens:'son atelier, son école, son entourage' },
  { n:3, libelle:'Son style, sans lui',   variable:'--niveau-3', sens:'sa manière, son genre, un suiveur' }
]
nombre(v) => v.toLocaleString('fr-FR')   // séparateur = espace insécable étroit U+202F
```

**`BarreNiveaux.svelte`** — props :
```
niveaux   : [int, int, int]   (requis)
hauteur   : string CSS        (défaut '0.7rem')
etiquettes: boolean           (défaut false ; si true, affiche une légende sous la barre)
```
Rendu : un conteneur flex 100 % ; pour chaque niveau i où `niveaux[i] > 0`, un
segment de largeur `niveaux[i]/sum * 100 %`, couleur `var(--niveau-(i+1))`.
Fond du conteneur `var(--couleur-trait)` (visible si somme = 0).

**`GalaxieMaitre.svelte`** — props : `maitre: Artiste`. SVG statique, sans D3.

**`+page.svelte`** — état (runes Svelte 5) :
```
vue       : 'galaxie' | 'fiche'   (état, défaut 'galaxie')
recherche : string                (état, défaut '')
selection : string                (état, défaut artistes[0].nom)
liste     : dérivé = artistes.filter(nom.includes(recherche, casse/espaces normalisés))
maitre    : dérivé = artistes.find(a => a.nom === selection)
totalNom(a)  = a.propre + a.doute
partDoute(a) = totalNom(a) ? a.doute / totalNom(a) * 100 : 0
```
Toutes les interactions sont client-side, sans navigation ni requête.

### 7.6 Algorithme de rendu de la galaxie (déterministe)

Système de coordonnées SVG : `viewBox="0 0 440 440"`, centre `C = (220, 220)`.

```
Constantes
  RAYONS      = { 1: 66, 2: 106, 3: 146 }   // px, orbite par niveau
  RAYON_COPIE = 184                          // px, anneau externe (copies)

Conversion polaire → cartésien (0° = haut, sens horaire)
  polaire(rayon, angleDeg):
    a = (angleDeg - 90) * π / 180
    return ( 220 + rayon*cos(a) , 220 + rayon*sin(a) )

Taille d'une bulle (compression par racine carrée)
  rayonBulle(notices) = min(22, 5 + sqrt(notices) * 0.9)

Placement des bulles (une par élément de maitre.familles, ordre du tableau)
  pour i, f dans enumerate(maitre.familles):
    angle   = (i / len(familles)) * 360 + 18        // décalage fixe de 18°
    r       = rayonBulle(f.notices)
    centre  = polaire(RAYONS[f.niveau], angle)       // position de la bulle
    label   = polaire(RAYONS[f.niveau] + r + 10, angle)  // texte, décalé vers l'extérieur
    ancre   = 'end' si label.x < 215 ; 'start' si label.x > 225 ; sinon 'middle'
    couleur = var(--niveau-{f.niveau})
```
Éléments dessinés, dans l'ordre (z-order) :
1. 3 cercles d'orbite (pointillés `3 4`, `stroke-opacity 0.6`) + libellé du niveau
   posé en haut de chaque orbite.
2. 1 cercle « copies » (pointillés `1 6`) + libellé « copies "d'après" — à part ».
   ⚠️ Ce cercle est **décoratif** : aucune bulle n'y est placée, `maitre.copie`
   n'est pas rendu dans la galaxie (seulement dans la vue « Détail »).
3. Les bulles de familles (disques pleins, `fill-opacity 0.85`) + `<title>` (info-bulle
   native) + étiquette texte « libellé · nombre ».
4. Le cœur : disque blanc cerclé rayon 40, nom + « N en doute ».

**Limite formelle de l'encodage :** cardinalité **1 bulle ⇄ 1 famille**, pas
1 point ⇄ 1 œuvre. Le volume d'œuvres n'est encodé que par l'aire de la bulle
(∝ notices via `rayonBulle`). L'angle ne porte **aucune information** (purement
esthétique). Le rayon encode le **niveau** (variable ordinale à 3 valeurs), pas
une grandeur continue.

### 7.7 Design tokens (valeurs exactes, `tokens.css`)

```
--couleur-fond        #f7f4ef      --niveau-1        #b8551f
--couleur-encre       #1c1a17      --niveau-2        #d98a3d
--couleur-encre-douce #5c554c      --niveau-3        #e8c07a
--couleur-trait       #ddd6ca      --couleur-copie   #4a6b7a
--couleur-accent      #7a4a2b      --couleur-revision#6b5b7a  (non utilisé ici)
--police-titre  Georgia, 'Times New Roman', serif
--police-texte  system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif
--largeur-max   60rem
```
Mise en page de la page : grille `grid-template-columns: minmax(14rem,20rem) 1fr`,
`gap 2rem` ; passe en une colonne sous 720 px. La liste des maîtres est un
`max-height: 32rem; overflow-y: auto`.

### 7.8 Points d'attaque suggérés pour une refonte (pour l'agent analyste)

- Remplacer l'encodage **famille→bulle** par **œuvre→point** : nécessite un export
  amont enrichi (coordonnées ou au moins un point par notice de doute, échantillonné
  si trop nombreux). Impact : `artistes.json` grossit ; prévoir un plafond/échantillon.
- **Angle porteur de sens** possible (aujourd'hui inutilisé) : par famille, par
  musée, par date… à décider selon le récit.
- **Dé-jargonniser** : introduire une couche de libellés « récit » distincte des
  `code`/`libelle` techniques (mapping `code → phrase grand public`), sans toucher
  au JSON source (table de correspondance côté front ou côté export).
- **Transition/mouvement** : le rendu est statique ; une entrée animée des points
  renforcerait la métaphore « constellation » (attention perf et accessibilité).
- Tout doit rester **pré-rendable statiquement** (contrainte non négociable).

### 7.9 Reproduction

```bash
cd web
npm install
npm run sync:data     # copie data/exports/web/*.json -> static/data/
npm run dev           # http://localhost:5173  (route /les-presque)
npm run build         # -> web/build/les-presque.html (statique, données pré-rendues)
```

---

## Annexes utiles à l'analyse

- Maquette d'intention : `images/maquette_galaxie.png` (et `images/maquette.png`).
- Données réelles : `data/exports/web/artistes.json` (63 maîtres au 2026-07-22).
- Code de la vue galaxie : `web/src/lib/GalaxieMaitre.svelte`.
- Code de la page : `web/src/routes/les-presque/+page.svelte`.
- Palette et typo : `web/src/lib/styles/tokens.css`.
- Chiffres de cadrage du projet : 24 507 notices de doute au total (dont 18 716
  hors une monoculture particulière au muséum de Nice) ; ces maîtres n'en sont
  qu'une entrée « par les noms célèbres ».
