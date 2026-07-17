# Journal d'avancement

Notes au fil de l'eau. Une entrée par séance de travail, les plus récentes en haut.

## 2026-07-17 (septies) — Accueil refondu en affiche interactive (nouvelle direction, prototype)

Direction B jugée trop classique / catalogue. Nouvelle piste pour l'**accueil seulement** :
une **affiche interactive** bâtie sur deux illustrations fournies par l'utilisateur
(`images/accueil_01` horizontale desktop, `images/acceuil_02` verticale mobile). Les
pages intérieures **restent en Direction B** pour comparer les deux systèmes.

Fait :
- Assets versés dans `web/static/cover/` (`accueil-desktop.png`, `accueil-mobile.png`)
  + `README.md` de traçabilité (illustrations générées pour le projet, évoquent la
  **base Joconde**, pas Léonard ni le tableau).
- **`LandingCover.svelte`** : couverture plein écran (100svh, pleine largeur) via un vrai
  `<picture>` à deux sources ; textes et navigation en **vrais éléments HTML superposés**
  (jamais dans le bitmap). Titre clair dans l'aplat sombre, accroche + mention de source
  discrètes ; **`EditorialNavigation.svelte`** = les 4 entrées en annotations reliées aux
  lignes de la fiche (Explorer = entrée principale, poids supérieur ; routes réelles dont
  `/echelle`). Contraste natif (clair/sombre), **aucun voile** ni panneau opaque.
- Interactions : survol/focus = déplacement ≤ 4 px + prolongement de la ligne + contraste,
  180 ms ; focus clavier visible ; `aria-current` sur Accueil ; `prefers-reduced-motion` ;
  ordre de tabulation logique.
- Coquille (`+layout`) : masthead + spectre **masqués sur `/` uniquement**, `main` en
  pleine largeur ; les 4 pages intérieures gardent leur navigation.
- Chiffre 24 507 + source relégués **sous la ligne de flottaison** (invisibles au chargement).

Recadrage : le point faible était la **tablette en portrait** (l'asset horizontal s'y
recadrait trop, la nav quittait la fiche) → bascule sur la **composition verticale en
portrait ≤ 1024 px** (media `orientation: portrait`). Vérifié par capture sur 5 gabarits
(16:9, desktop moins large, tablette portrait, téléphone étroit, téléphone haut) : visage
jamais recouvert, nav sur ses zones, pas de scroll horizontal, couverture plein viewport ;
pages intérieures intactes. `build` OK. Détail : decisions.md 2026-07-17 septies.
Prochaine étape : juger l'accueil sur captures avant d'étendre la direction.

## 2026-07-17 (sexies) — Direction B menée à terme sur toutes les pages (fait)

**Statut.** La Direction B n'est PAS validée définitivement : son rendu est jugé trop
classique / trop proche des conventions visuelles fréquentes. On la mène jusqu'au bout
pour disposer d'une **version complète et comparable**, qui servira de modèle de travail
à une nouvelle direction (fournie ensuite par l'utilisateur). Aucun nouvel effet, folio
ou ornement hors cadrage ; textes validés et données inchangés.

Cinq pages recomposées, un commit par page :
- **Explorer / Profil** : en-tête de dossier compact (le profil apparaît au premier
  écran), portrait-origine via le bandeau, graphe élargi (répertoire resserré), onglets
  en soulignement (fin de la boîte), folio/cote discret.
- **Explorer / Œuvres** : grille de cartes blanches → **liste éditoriale continue**
  (entrées à filets) ; le **verbatim** du musée devient la matière (Fraunces, liseré de
  la mention) ; hiérarchie titre / musée / verbatim / lien POP ; **emplacement média
  réservé** par entrée (jamais d'image inventée).
- **Explorer / Musées** : fin de la petite carte centrée à 32 rem → **grande carte**
  (colonne large) + flanc légende/hors-cadre ; points fixes, POP et tooltips inchangés.
- **Comprendre les mentions** : la ligne (Spectre) porte les territoires **une seule
  fois** (pas de démonstration décorative) ; huit mentions en trois colonnes à filet
  coloré ; comparaison ample ; barres/données/réserves conservées.
- **Méthode** : sommaire numéroté en **rail collant** + contenu en colonne ; boîte grise
  retirée ; la ligne n'est PAS imposée (elle n'explique rien ici).

Toutes les boîtes grises arrondies remplacées par des filets. `build` OK à chaque page,
vérifié desktop + mobile ; interactions (onglets, tri, tooltips, liens POP) préservées.
Planche comparative complète produite (6 pages + 2 mobiles). Détail : decisions.md
2026-07-17 sexies. Suite : critique globale de cette version, puis nouvelle proposition
sur un modèle visuel plus précis fourni par l'utilisateur.

## 2026-07-17 (quinquies) — Direction artistique B « la ligne de proximité » : coquille + accueil (fait)

Revue globale de direction artistique menée (planche de l'existant, diagnostic, trois
directions maquettées avec vraies données/portraits/polices — A « le registre »,
B « la ligne de proximité », C « coupures & verbatim » ; maquettes conservées dans le
scratchpad). **Direction B retenue** par l'utilisateur (motifs : decisions.md 2026-07-17
quinquies). Début de la refonte **par pages complètes**.

Palier 1 livré :
- **Token `--spectre`** (dégradé des 8 pigments, stations centrées, température = distance)
  et **`Spectre.svelte`** (la ligne réutilisable, bande + libellés des trois territoires,
  repli mobile corrigé).
- **Coquille** (`+layout.svelte`) : filet brun de tête **remplacé par la ligne** (signature
  sur toutes les pages) ; canevas élargi 60 → 68 rem.
- **Accueil** (`+page.svelte`) recomposé : spectre à territoires, grand titre, CTA encre,
  figure de données à 8 stations, chiffre en preuve secondaire ; textes validés inchangés.

Pages non refondues (Explorer, Comprendre, Méthode) vérifiées intactes sous la nouvelle
coquille. `build` OK, vérifié desktop + mobile. Détail : decisions.md 2026-07-17 quinquies.
Suite : Explorer / Profil (portrait-origine + axe pleine largeur + folios).

## 2026-07-17 (quater) — Socle V1 bouclé : page Méthode + Accueil-couverture + nav à 4 entrées (fait)

Fin des deux zones restantes du socle éditorial V1.

**Page Méthode** (`/methode`, placeholder activé) : page unique et structurée qui
rassemble les limites dispersées. Cinq sections nettes — Périmètre · Construction des
données · Lire les chiffres · Limites · Sources et droits — avec un sommaire d'ancres.
Tous les chiffres viennent des exports (aucun saisi à la main) : `niveaux.json`,
`provenance.json`, `vue_ensemble.json`, `artistes.json`. Couvre les 13 points demandés
(Joconde, formulation prudente, détection lexicale + vérification 206 notices, critère
des 27 = seuil pas palmarès, recouvrements, copies à part, Nice/Barla + hors monoculture,
versements incomplets, pièges d'identification par les noms + corrections, constater vs
conclure, images/droits, version des données). Éditoriale, pas de FAQ ni de cartes.

**Correction de données.** Divergence trouvée et résolue : `typologie.md` affichait la
catégorie copie à **22 844** (somme naïve `d'après 22 564 + copie 280`, qui double-compte
les recouvrements) alors que la source canonique (`niveaux.json` `copie`, `vue_ensemble`
`copies_dapres.total`) donne **22 624** ; même correction pour révision (27 273 → **27 270**).
Interface (Méthode, Comprendre les mentions) et docs reprennent désormais la valeur
canonique : « d'après » = 22 564, copies au total = 22 624.

**Accueil-couverture** : l'accueil devient une couverture éditoriale à deux zones —
promesse à gauche (kicker, titre, sujet en une phrase, CTA « Explorer les 27 maîtres »,
lien « Comprendre les mentions »), **figure de données** à droite (structure média
ASSUMÉE et remplaçable : motif schématique d'index + les 8 pigments des mentions, pas
Léonard ni le tableau, légende « composition provisoire »). Le chiffre **24 507** passe
en **preuve secondaire** sous la couverture, avec renvoi à la Méthode ; le cas mono-musée
quitte l'accueil (trop technique → Méthode). Hiérarchie forte titre → promesse → figure
→ exploration → preuve chiffrée.

**Nav publique recentrée à 4 entrées actives** : Accueil · Explorer les maîtres ·
Comprendre les mentions · Méthode. « Les révisions » et « La carte » **retirées de la nav
publique** (code et données conservés au dépôt, routes non liées). `build` OK, vérifié
desktop + mobile, a11y (titres sémantiques, focus visibles, ancres). Détail : decisions.md
2026-07-17 (quater). **Fin du développement par petites zones** : prochaine étape = revue
globale de direction artistique et d'architecture visuelle (captures + compositions).

## 2026-07-17 (ter) — Zone « Comprendre les mentions » (page autonome, fait)

Chapitre autonome sur le vocabulaire muséal de la prudence (architecture §3), qui
**referme la boucle** ouverte par le retrait de la légende du répertoire. Route
existante **`/echelle`** activée (placeholder « L'échelle du doute »), libellé public
provisoire **« Comprendre les mentions »** (`prete: true`). Quatre parties :
1. **Intro éditoriale** courte + phrase de prudence commune verbatim.
2. **Trois territoires** : bande de progression continue (réutilise `territoires.js`,
   mêmes tints, titres, annotations) + flèche « plus près / plus loin de sa main ».
3. **Huit mentions** : liste scannable groupée par territoire, définition = `corps`
   de `familles-public.js` (source unique), formule type affichée seulement où
   `montrerMention` (nom générique « un maître »). Aucun libellé ni définition créé.
4. **Vue d'ensemble chiffrée** (`vue_ensemble.json`) : deux panneaux de **barres**
   (jamais d'anneau) à **échelle commune** — Ensemble (24 507) vs 27 noms (2 341) —
   nouveau composant `BarresMentions.svelte`, groupé par territoire, couleurs stables,
   % + effectifs affichés (« <1 % » si non nul mais arrondi à 0). Le basculement se
   lit d'un coup d'œil : « attribué à » 73 % → 37 %, « de son école » → 39 %.

Réserves respectées : mentions qui se recouvrent (pas de partition à 100 %, note
explicite), copies « d'après » comptées à part (22 564), concentration mono-musée
renvoyée à la page Méthode (pas de récit Nice/Barla ici). `vue_ensemble.json`
synchronisé (`npm run sync:data`), `build` OK, vérifié desktop + mobile. Détail :
decisions.md 2026-07-17 (ter). Reste (nav) : recentrage complet à 4 entrées (retirer
Révisions/Carte de la nav publique, « Les presque » → « Explorer les maîtres ») —
non fait ici, hors périmètre. Zones suivantes du kit : Accueil-couverture, Méthode.

## 2026-07-17 (bis) — Charte palier 3 : zone TroisTerritoires sur l'onglet Profil (fait)

Le principe éditorial central — la distance à la main du maître — devient **visible
dans le graphique** (architecture §5). Les 8 mentions, déjà ordonnées par distance,
se regroupent en **trois territoires contigus** : *Au plus près* (attribué à, nom ?) ·
*Autour du maître* (atelier, cercle, école) · *Dans son influence* (suiveur, manière,
goût). Correspondance exacte avec `ORDRE_FAMILLES` (plages 0-1 / 2-4 / 5-7).

- **Primitive `territoires.js`** : source unique du regroupement + titre + annotation
  courte par zone, réutilisable par la future rubrique « Comprendre les mentions ».
  Ne redéfinit aucun libellé (labels/couleurs restent dans `familles-public.js`) ;
  garde-fou dev qui vérifie l'alignement sur `ORDRE_FAMILLES`.
- **`NuageFamilles`** recadré **sans toucher aux données, points, couleurs, tooltips** :
  fonds très légers par zone (nouveaux tokens `--territoire-*`, température = distance),
  séparateurs fins, titres de territoire en tête. Bandes contiguës, sans cadre → **une
  seule ligne de proximité**, pas trois blocs.
- **Clé de lecture rétablie** sous le graphe (la légende détaillée a quitté le
  répertoire) : intro « de gauche à droite, le lien se desserre » + trois cellules
  contiguës (titre, annotation, mentions à pastilles). Les **annotations vivent dans
  la clé HTML** (le SVG ne sait pas revenir à la ligne → illisible en mobile).

Vérifié par capture sur trois profils opposés : Ingres (dominante *attribué à*, gros
point à gauche), Le Brun (*école*, au centre), Rembrandt (*manière*, à droite) — le
volume principal change de territoire selon le maître. Mobile : répertoire replié,
graphe lisible, clé empilée en trois blocs. `build` OK. Détail : decisions.md
2026-07-17 (bis). Reste (zones suivantes) : « Comprendre les mentions » (réutilisera
`territoires.js`), Accueil-couverture, Méthode.

## 2026-07-17 — Charte palier 3 : zone Répertoire (fait)

Deuxième zone du kit (après le prototype bandeau) : la colonne de gauche d'« Explorer
les maîtres » devient un **vrai outil de navigation**, séparé du profil (architecture
§4). Nouveau composant **`Repertoire.svelte`** qui absorbe recherche + liste et ajoute :
- **tri** par nombre d'œuvres concernées (défaut, ordre naturel du dossier) ou
  **alphabétique** (A→Z, `localeCompare` fr) — petit segment de deux boutons ;
- **microprofils colorés** conservés (jauge `BarreFamilles`, mêmes couleurs de familles) ;
- **sélection active** renforcée : filet d'accent à gauche + fond soutenu + `aria-current`
  (le filet transparent au repos évite tout saut de largeur) ;
- **responsive** : sur mobile le répertoire se **replie** (bouton « Choisir un maître /
  Masquer la liste »), replié d'emblée pour montrer le profil, refermé après le choix ;
  matchMedia plutôt qu'un `<details>` natif (piège de réouverture, cf. 2026-07-13).

La **légende détaillée des mentions** (`LegendeFamilles`) est **retirée** de sous la
liste : elle rejoindra « Comprendre les mentions » (architecture §3). Le composant
`LegendeFamilles.svelte` reste au dépôt pour cette reprise. `les-presque/+page.svelte`
ne garde que `selection` (liée au répertoire), le CSS de liste a migré dans le
composant. `build` OK ; vérifié par capture desktop + mobile. Piège de séance :
`vite preview` lancé avant un rebuild sert un ancien manifeste (chunks CSS hachés en
404 → page « déshabillée ») → **redémarrer le preview après un build**. Détail :
decisions.md 2026-07-17. Reste (zones suivantes) : TroisTerritoires, « Comprendre les
mentions », Accueil-couverture, Méthode.

## 2026-07-16 (quinquies) — Charte, palier 3 : prototype BandeauMaitre + ChiffreVedette (fait, ⏸)

Reprise après plantage machine : d'abord un commit de sauvegarde de tout le
travail non versionné depuis « Les presque : vitrine » (rubrique Avant/après,
Vue d'ensemble, charte paliers 1-2), `museum.zip` (backup local, 1,1 Go) exclu
via `.gitignore`. Puis **prototype du kit** (charte §5) sur la fiche maître réelle,
sans toucher au répertoire, au nuage ni à l'accueil :
- **`ChiffreVedette.svelte`** — primitive : grand nombre (Fraunces tabulaire) +
  légende courte.
- **`BandeauMaitre.svelte`** — « scène du maître » : portrait **agrandi** (14 rem)
  + nom + **phrase de synthèse calculée** + deux ChiffreVedette (œuvres sous le nom /
  musées). Absorbe l'ancien bloc `header.profil` de `les-presque/+page.svelte`.
- **Onglets renommés** Graphique/Œuvres/Carte → **Profil · Œuvres · Musées**
  (libellés éditoriaux, charte §5) ; état interne `vue` : `profil`/`oeuvres`/`musees`.
- CSS migré du `+page` vers le bandeau ; `build` OK ; vérifié par capture (Le Brun).

Deux points laissés à l'arbitrage (decisions.md même date) : (1) la synthèse
calculée **réintroduit** une phrase dérivée retirée le 2026-07-10 — assumée car
purement factuelle (nomme la formule dominante, ne l'interprète pas) ; (2)
`fractionEnMots` **plafonne à « près des deux tiers » (62 %)** alors que la mention
dominante peut monter à ~77 % (école de Le Brun) → sous-estimation à corriger si
validé. Reste : validation utilisateur, puis zones suivantes du kit (répertoire,
TroisTerritoires, accueil…).

## 2026-07-16 (quater) — Chantier direction artistique & architecture éditoriale

Cadrage de plus haut niveau inséré avant le kit de composants : repenser l'appli
comme une publication éditoriale centrée sur « Les presque ». Document créé :
`docs/architecture-editoriale.md` (nav recentrée à 4 entrées ; accueil = couverture ;
séparation répertoire ↔ profil ; distance à la main = principe visuel central ;
illustration Joconde = figure de DONNÉES, pas Léonard ni *La Joconde* œuvre). Inscrit
en roadmap (avant palier 3). ⏸ à valider. Aucun code, nav du front non modifiée.
Détail : decisions.md 2026-07-16 (quater).

## 2026-07-16 (ter) — Charte, palier 2 : coquille « inventaire »

Header/nav/structure refaits (`+layout.svelte`) : filet d'accent en tête, masthead
aligné sur la colonne, nav en petites capitales Public Sans avec page courante
soulignée, rythme aux tokens. Italique Spectral intégrée (regénération
`source_fonts.py`, 10 woff2). Espaces fines des grands nombres vérifiées (OK).
Limité : ni fiche maître ni composants internes. Vérifié par capture avant/après.
Détail : decisions.md 2026-07-16 (ter).

## 2026-07-16 (bis) — Charte, palier 1 : base typographique

Polices intégrées en local (Fraunces, Spectral, Public Sans ; woff2 latin +
latin-ext, ~277 Ko) via `web/scripts/source_fonts.py` → `static/fonts/` +
`fonts.css`, aucun CDN. Tokens manquants ajoutés (`tokens.css` : polices, échelle
typo, espacement, rayons, filets, surface, ombre, focus). Base typographique
appliquée globalement seulement (`+layout.svelte`) : Spectral en texte, Fraunces
en h1/h2 + wordmark, Public Sans en UI/nav/pied ; composants non refaits. Vérifié
par capture avant/après (accueil + Les presque). Détail : decisions.md 2026-07-16 (bis).

## 2026-07-16 — Charte graphique : direction arrêtée

Proposition de direction graphique pour l'application-cadre (audit de l'existant,
principes, palette, typo, composants, application aux presque, extensibilité).
Ambiance typographique retenue : « Catalogue savant » (Fraunces + Spectral +
Public Sans, auto-hébergées). Source de vérité créée : `docs/charte-graphique.md`.
Décision : decisions.md 2026-07-16. Pas de code — prochain palier = tokens + typo.

## 2026-07-15 (sexies) — Réalignement documentaire du recentrage

Mise à jour des docs de pilotage pour refléter la décision : la V1 publique est
centrée sur « Les presque » ; les autres rubriques (dont « Avant / après »)
restent conservées et documentées, hors périmètre publiable initial. `roadmap.md`
reçoit un bloc « ★ RECENTRAGE » en tête (périmètre V1 / en réserve / déjà fait) et
sa section P3-T2 est marquée EN RÉSERVE ; `rubrique-revisions.md` reçoit un bandeau
de mise en réserve ; `README.md` (État du projet) est corrigé ; `decisions.md`
2026-07-15 (ter) reste la décision canonique. Réalignement purement documentaire :
aucun code, aucune suppression, aucun déplacement de fichier.

## 2026-07-15 (quinquies) — « Vue d'ensemble » : reconnaissance + export préparé

Tour d'horizon des données pour une future section « Vue d'ensemble » des
formulations prudentes (rapport → docs/donnees.md 2026-07-15). Constat clé : les
27 noms = ~10 % du doute ; le hors‑27 est dominé par la monoculture de Nice
(Barla, 5 791). Message central retenu : « attribué à » domine au global, mais
école/atelier/manière prennent le dessus dans les 27. Export `vue_ensemble.json`
généré (`src/build_vue_ensemble.py`) — familles global/dans‑27/hors‑27, niveaux
global vs 27 + hors monoculture, copies à part. Cadré prudemment : pas d'anneau
(recouvrements), pas de classement par nom hors 27, pas de période, domaines/top
musées en réserve. Pas de front. Détail : decisions.md 2026-07-15 (quater).

## 2026-07-15 (ter) — Recentrage du projet sur « Les presque »

Décision de cadrage : « Les presque » devient la première publication complète de
*L'inventaire du doute* ; les autres rubriques (Avant/après, échelle, carte)
passent en pause / réserve, sans rien supprimer (dossiers futurs). `/revisions`
repasse hors nav publique (`prete: false`). Titre et périmètre de la v1 restent à
décider ; on pense figer d'abord la charte graphique sur « Les maîtres » comme
socle. Détail et garde-fous : decisions.md 2026-07-15 (ter). (Les paliers
datajournalisme du jour sur /revisions — anneau, prototype Les œuvres — sont
consignés dans decisions.md 2026-07-15 et bis ; ils restent valides, en réserve.)

## 2026-07-14 (quater) — « Avant / après » : réorganisation en onglets

La V1 (tout en vrac sur une page) jugée non publiable. Palier ÉDITORIAL (pas de
style, pas d'images) : `/revisions` passe en 4 onglets (En bref · Les chiffres ·
Les œuvres · Repères) sous un titre + chapô permanents. Le graphe des chiffres
est scindé en « constat principal » (4 familles galerie) / « cas secondaires »
(3 familles atténuées), même échelle. La galerie ne déroule qu'un groupe à la
fois via des chips (+ chip transversal « Un nom réapparaît »). Labels publics
refondus en phrases (« Un autre nom apparaît », « Le nom disparaît »…), renommés
dans `revisions_classify.py`, rebuild + sync. Modèle image RÉSERVÉ dans chaque
`cas` (`image: {statut,url,credit,source}`, tous « pending ») et dans
`CarteRevision` (vignette affichée seulement si droits clarifiés, jamais de
hotlink POP). `pytest` = 60, `npm run build` OK, 4 onglets + filtre vérifiés par
capture (playwright pour cliquer les onglets). Reste hors palier : charte, images
affichées, autres graphes, page méthode complète.

## 2026-07-14 (ter) — « Avant / après » : front V1 construit

Bilan v2 et taxonomie à 7 catégories validés par l'utilisateur, avec V1
**simplifiée** (pas de page dashboard). Renommé le libellé `meme_nom` en « Le
même nom, avec réserve » (`revisions_classify.py`), rebuild `revisions.json`
(`uv run python src/build_revisions.py`), `pytest` = 60 OK, `npm run sync:data`.
Page `/revisions` (SvelteKit) : intro courte + phrase forte sur la direction
inverse (5 283) + 2 cartes exemples (Vinci → anonyme ; École française → Van Loo,
« un nom rendu ») + **un seul** graphe (7 catégories triées, familles-galerie en
plein, familles-stats atténuées, légende qui dit lesquelles se visitent en
cartes) + galerie de 32 cartes groupées par catégorie et filtrables + note de
méthode (limite Joconde, concentration Louvre/dessins divulguée). Composant
réutilisable `web/src/lib/CarteRevision.svelte` (verbatims seuls, sans image,
lien POP). Route activée dans la nav. `npm run build` OK, vérifié par capture.
Différé : autres graphes (daté/non daté, anciens noms, siècles, domaines) →
page méthode ou V2. Reste à faire côté style : identité visuelle propre (fil
ouvert commun à tout le front).

## 2026-07-14 (bis) — « Avant / après » : bilan de vérification + refonte de la classification (fait, ⏸)

Import du CSV annoté (80 lignes) : 44 OK, 18 à exclure, 8 faux passage, 10 faux
parsing. Les commentaires ont fait émerger un modèle plus fin que mes 4
catégories → **taxonomie v2 à 7 catégories** dans un module dédié testable
(`src/revisions_classify.py`) : ajout de « Même nom, attribution plus prudente »,
« Déjà une copie ou un d'après », « Plusieurs anciens noms » (chaînes, stats
seulement). Cinq bugs de parsing corrigés, tous venus de l'échantillon :
parenthèses imbriquées, date collée au nom, prose prise pour nom, « ; »
biographique dans une parenthèse, parenthèse orpheline en tête. Distinctions
fines validées : chaîne du même nom ≠ plusieurs noms ; inclusion de prénom (Le
Nain Louis ↔ Le Nain) ; « plus prudent » = réserve ajoutée (sinon confirmation) ;
écoles nationales gardées en galerie via le verbatim. Verdicts figés dans
`tests/test_revisions.py` (25 cas + cohérence CSV : 44/44 OK en galerie, 0 fuite ;
`uv run pytest` = 60 passés). `revisions.json` régénéré (7 catégories, lot 32
cas / 20 musées / Louvre 6 % / 4 en direction inverse). Docs à jour. **En attente
de validation du bilan avant tout front.**

## 2026-07-14 — « Avant / après » : pipeline + échantillon de vérification (fait, ⏸)

Cadrage V1 validé (libellés publics ajustés). Construit le pipeline
`src/build_revisions.py` → `revisions.json` et `src/build_revisions_sample.py`
→ `echantillon_revisions.csv` (80 lignes). Front non touché.

Le travail de données a fait remonter trois choses concrètes : (1) **parsing** —
deux styles de catalogage (parenthétique vs prose « ancienne attribution : NOM »
du Louvre), le second polluait l'extraction du nom → corrigé ; (2) **anciens
noms fragiles** — contamination « copie d'après » (Michel-Ange 233→119) et effet
mono-musée (202/233 Louvre) → comptés hors copie, servent de filtre et non de
palmarès ; (3) **direction inverse** — 5 584 œuvres gagnent un nom, presque
autant que celles qui en perdent (5 824) : constat qui équilibre le récit.
L'échantillon (4 passages + 6 strates de pièges : chaînes, écoles, noms proches,
datées, copies-after, inverse) a servi immédiatement à repérer le défaut de
parsing avant tout front. Invariants `assert` en place. Constats dans donnees.md,
arbitrages dans decisions.md. **Prochaine étape : vérification manuelle par
l'utilisateur.**

## 2026-07-14 — « Avant / après » : cadrage V1 simplifié + audit images (proposé, ⏸)

Reprise du cadrage sur base plus simple. Titre provisoire « Avant / après ».
Trois vérifications neuves : (1) **images** — le CSV n'a pas d'URL, POP sert
l'image depuis un CDN interne sans droits par œuvre, la Licence Ouverte couvre
le texte pas les clichés → **pas d'images en V1**, carte textuelle + lien POP ;
(2) **périodes** — 16 % d'œuvres datables, 7 % de révisions datées → pas de
frise, structure par type de passage ; (3) **sélection V1** — lot par diversité
(plafond 2/musée, quotas par destination) testé : 32 cas, 10 musées, Louvre
ramené de 59,5 % à 19 %. Structure recommandée : par type de passage, grands
noms en filtre. Stats sur tout le corpus en graphes classiques (barres, donut,
colonnes). Cadrage réécrit dans **docs/rubrique-revisions.md** ; constats
images/périodes dans donnees.md ; arbitrages dans decisions.md. Aucun code
front. En attente de validation.

## 2026-07-13 — Audit des rubriques restantes + cadrage « Révisions » (proposé, ⏸)

Retour aux données avant de choisir la suite (demande utilisateur : « ce que
les données rendent lisible, pas ce que la roadmap prévoyait »). Trois passes
de scan du CSV complet. Verdict : révisions solide (26 667 avant→après réels,
destinations chiffrées, 5 formats de champ identifiés), carte nationale en
pause, décodeur réduit en encart. Deux faux positifs commis par notre propre
audit rapide et corrigés dans la foulée (grands noms testés en sous-chaîne ;
années de vie lues comme dates de catalogue) — la preuve que les contrôles
type SERODINE/RODIN restent nécessaires partout. Constats dans donnees.md
(+ dédoublement Île/Ile-de-France du champ Region) ; décision et garde-fous
dans decisions.md ; cadrage complet (titres, angle, forme, schéma
revisions.json, règles de comparaison, contrôles, 10 prototypes lisibles +
10 cas à exclure) dans **docs/rubrique-revisions.md**, en attente de
validation. Aucun code front.

## 2026-07-13 — « Les presque » : réécriture de l'intro (fait)

L'ancien chapô était trop évocateur, pas assez explicatif (retour utilisateur).
Nouveau texte (validé) : le titre « Les presque » est conservé mais **glosé dès la
première phrase** ; deux paragraphes disent ce que la rubrique montre, justifient le
choix des 27 noms (noms de référence, au moins vingt œuvres concernées — pas « les
plus grands ») et **orientent** le lecteur (jauge colorée → graphique → œuvres →
carte). Encadré refait **sans émoticône** : « Cette rubrique ne réattribue aucune
œuvre. Elle reprend les mots publiés par les musées dans leurs notices, avec leurs
précautions. » Ligne « critère » redondante supprimée. Vocabulaire public tenu (pas
de « famille / niveau / au doute », pas d'« erreur » des musées, pas d'expertise
sous-entendue). Guillemets figés (espaces insécables) pour éviter les « » orphelins.
`les-presque/+page.svelte` (texte + retrait de la règle CSS `.critere`).

## 2026-07-13 — Carte : palier style (fait)

Finition visuelle, sans toucher données ni comportement. Fond « régions très
estompées » (choix utilisateur) : aplat quasi nul, frontières gris très pâle, points
bien au-dessus. Survol/focus des points plus franc (pleine opacité + halo blanc
élargi), même retour pour points cliquables et non ; pas de distinction au repos des
cliquables (curseur seul). Carte ramenée dans une colonne centrée (titre, fond,
légende, mentions alignés). Légende et mention hors-cadre au même registre (petit
corps, encre douce, filet). Vérifié : Le Brun (dense), Van Dyck (dispersé +
hors-cadre), 390 px ; build OK. Différé (contenu) : repère texte du musée principal.

## 2026-07-13 — Faux rattachement de maître par sous-chaîne, corrigé (fait)

Un lecteur signale la notice `07980002404` (« Archimède », MUDO Beauvais) classée
« attribué à Rodin » alors que l'auteur est **Serodine** (« SE‑RODIN‑E » contient
« RODIN »). La détection de la formule était juste ; c'est l'identification du maître
qui déraillait (`_trouve_maitre` en sous-chaîne). Scan complet : 8 maîtres, 77
segments faux, dont 13 en doute (Tintoret 6, Léonard 6, Rodin 1). Correctif : test
**mot entier** (`\bALIAS\b`) — vérifié qu'il garde les vraies notices de Le Tintoret
et n'écarte que le fils « Tintoretto Domenico » ; seule perte, la coquille
« IIngres ». Exports régénérés : doute Tintoret 53→47, Léonard 56→50, Rodin 81→80 ;
aucun maître sous le seuil de 20 (liste des 27 intacte). Sync + build OK. Constats
dans donnees.md, choix dans decisions.md.

## 2026-07-13 — Carte : point-lien POP pour l'œuvre unique (fait)

Quand un musée ne conserve qu'une œuvre concernée, son point devient un lien vers la
fiche publique POP. Pipeline : `build_artistes.py` retient la 1re notice par musée
(`ref1`/`titre1`) et exporte `oeuvre_unique {reference, titre}` seulement si
`doute==1` (188 avec titre, 2 sans). Front : dans `CarteMaitre`, point à 1 œuvre →
`<a>` SVG vers `lienPop` (`target=_blank`, `rel=noreferrer`, focus clavier visible) ;
tooltip = aperçu (titre en italique si dispo, mention + pastille, « 1 œuvre
concernée »). Multi-œuvres inchangés (non cliquables). `Infobulle` gagne un champ
`titre`. Pas de nouvelle vue « œuvre ». Vérifié (URL POP, aria, sans-titre, focus,
Louvre non cliquable) ; build statique OK.

## 2026-07-13 — Carte : écartement des points qui se chevauchent (fait)

À taille fixe, deux musées pouvaient se cacher : coordonnées quasi identiques (deux
musées d'une même ville — Marseille/Marseille, Versailles/Versailles à ~0,1 px) ou
points très proches (Paris/Versailles ~5,7 px, Lille/Douai ~9,7 px). Ajout d'un
`ecarterPoints` dans `geo.js` : relaxation itérative déterministe (sans dépendance)
qui repousse chaque paire trop proche jusqu'à `2·R + 1,5 px`, en gardant les points
au plus près de leur vraie place ; les points confondus sont séparés selon l'angle
d'or (rendu stable). Contour blanc des points renforcé (1,1 px) et opacité 0,82 pour
détacher les voisins. Vérifié par captures (Le Brun, Boucher, Rubens) : Île-de-France
et paires régionales désormais lisibles.

## 2026-07-13 — Harmonisation des tooltips (fait)

Les trois tooltips vivants (graphique, carte, jauges) passaient déjà par
`Infobulle.svelte` : pas de fork, juste un renfort. `Infobulle` reçoit un header
en bande grisée (pastille optionnelle), une largeur stable (max-content bornée
13–17 rem), des lignes de ventilation à nombres alignés (+ `%` gris via `appoint`),
et `valeur` devient optionnelle. `tooltipFamille` fournit la pastille de header au
graphique. Les **jauges** passent d'un tooltip par segment à un **récap complet du
maître** (header = nom, lignes par mention + %) — cohérent avec la carte, et la
formule « % du doute » (mot banni) disparaît. Vérifié par captures : graphique
multi / 1 œuvre / mention type, carte multi / 1 œuvre concernée, jauge, 390 px.

## 2026-07-13 — Légende permanente des mentions sous la liste (fait)

Nouvelle brique `LegendeFamilles.svelte` sous la liste des maîtres, commune aux
trois vues : la clé des couleurs avant interaction. Réutilise `header` + `corps`
de `familles-public.js` (source unique, mêmes mots que les tooltips), pastilles
rondes, ordre de l'axe. Un `corps` reformulé au passage (atelier). Repliable en
mobile (état JS via `matchMedia`, pas un `<details>` natif — son contenu fermé
n'est pas ré-affichable en CSS selon la largeur, vérifié sur Chromium). Validé
par captures desktop + mobile.

Reste (palier séparé) : harmoniser le style des tooltips.

## 2026-07-12 — Carte par maître : revue (taille fixe, tooltip, légende) (fait)

Revue du premier rendu, trois sujets traités.

1. **Test A/B taille variable vs fixe** (captures Le Brun / Ribera / Van Dyck /
   Ingres). Le variable (∝ √doute) ne tient que sur un vrai dégradé (Van Dyck) :
   ailleurs son échelle **propre au maître** trompe (un gros cercle Ribera = 3
   œuvres vaut un gros cercle Le Brun = 276) et gonfle les petits volumes en gros
   disques qui se chevauchent. **Taille fixe retenue** (décision utilisateur) : la
   carte dit *où*, le *combien* reste au survol et dans l'onglet graphique.
2. **Tooltip refait** : il réintroduisait « Presque lui / Autour de lui » (niveaux).
   Remplacé par les **familles publiques** (`familles-public.js`) avec pastilles de
   couleur, tri par valeur, accord singulier/pluriel. `Infobulle.svelte` reçoit un
   champ optionnel `lignes`. Exemple : « musée du Louvre, Paris / 276 œuvres
   concernées / De son école 225 · Attribué à 37 · Son atelier 14 ».
3. **Légende** adaptée au point fixe : « Un point = un musée où au moins une œuvre
   concernée est conservée. Passez sur un point pour voir combien… ».

Nettoyage : rayon variable, calibres, bascule de test `?carte=fixe` retirés.
Piège CSS corrigé (la règle globale `svg { width:100% }` gonflait le point-repère
de légende → largeur figée sur `.repere`). Revalidé par captures.

## 2026-07-12 — Carte par maître : premier rendu (fait)

Deux mini-paliers rapprochés, après validation de la spéc (decisions.md même date) :

1. **`web/src/lib/geo.js`** — projection `geoConicConformal` calée France (parallèles
   44/49, méridien 3°E), bornes métropole partagées + `estProjetable`, normalisation
   de l'enroulement du GeoJSON.
2. **`web/src/lib/CarteMaitre.svelte`** — onglet **Carte** ajouté après Graphique /
   Œuvres. 1 point = 1 musée, rayon ∝ √doute (3–22 px), couleur unique, fond régions
   discret, légende de calibres, tooltip (musée/ville/nb/ventilation), mention
   hors-cadre, repli phrase si < 2 musées projetables.

**Piège d3-geo résolu.** Les anneaux de france-geojson sont enroulés à l'envers pour
d3-geo : `fitExtent` sur les polygones lisait « tout le globe sauf la France » (échelle
microscopique, tout s'effondrait) et le fond se remplissait en complément (grand
aplat). Correction : ajuster la projection sur un `MultiPoint` des sommets (les points
se projettent sans ambiguïté) et réinverser les anneaux au chargement pour le tracé.

Vérifié par captures : Le Brun (concentration extrême au Louvre), Rubens et Van Dyck
(dispersés), Ingres (concentré à Montauban), Van Dyck déclenche bien la mention
« Hors cadre métropolitain : 1 œuvre au musée Léon Dierx, Saint-Denis de La Réunion ».
Reste : palier style (fond, points, chevauchements Île-de-France, calibres).

## 2026-07-12 — Relecture de CLAUDE.md : remise en accord avec la réalité (fait)

Revue complète demandée par l'utilisateur. Trois écarts corrigés dans CLAUDE.md :
- la roadmap était annoncée dans `decisions.md` alors qu'elle vit dans
  `docs/roadmap.md` depuis le 2026-07-03 ;
- la stack affichait encore « à terme D3.js » : le front SvelteKit statique
  (décision du 2026-07-07), les dataviz Svelte/SVG et `npm run sync:data`
  sont désormais décrits ;
- « `data/` n'est pas versionné » était imprécis : seul `data/raw/` est ignoré,
  `data/exports/` est suivi par git (de même `web/static/data/`, généré, ignoré).

Dans la foulée : README remis à jour (il annonçait encore « Phase 1 en cours »,
installation du front ajoutée) et note d'orientation en tête de la section
roadmap historique de `decisions.md` (esquisse phase 0 conservée comme trace).

## 2026-07-10 — Nuage : labels publics, axe réordonné, tooltips prudents (fait)

Chantier « labels » du nuage traité (deux tours de proposition, validés avant
implémentation). Fait :
- **Couche de traduction** `web/src/lib/familles-public.js` (label public + formule
  exacte + sens), réutilisable par Détail plus tard.
- **Labels publics** sur l'axe : attribué à · nom (?) · son atelier · son cercle ·
  de son école · un suiveur · sa manière · dans son goût. Plus de « ? » seul.
- **Axe réordonné** par distance au maître (option B, typologie.md) : la lecture
  gauche-droite est désormais honnête.
- **Micro-légende** statique (1 ligne) « De gauche à droite, le lien au maître se
  desserre. » — remplace la bulle rejetée, aucun saut.
- **Tooltips** réécrits : `label — « formule exacte » : sens prudent. N œuvres.`
  Sans niveau/famille/marqueur. Vérifié (Le Brun/école = 240).
- **CLAUDE.md** : règle « Couche de libellé public obligatoire ».

Contrôlé par capture (ordre, pas de chevauchement même « dans son goût ») et
`npm run build` OK. Périmètre tenu (nuage seul). Reste noté : accueil, Alençon
dans CLAUDE.md, refonte Détail — non traités volontairement.

## 2026-07-09 — Nuage : bulle « comment lire » rejetée + les labels à retravailler (à faire)

Retour utilisateur : la bulle dépliable « Comment lire ce graphique » est **très
mauvaise**, non validable. **Supprimée** (même branche). Deux défauts :
- **technique** : le `<details>` en se dépliant pousse brutalement le bloc
  graphe+portrait de 3-4 cm → saut de page inacceptable ;
- **de fond** : expliquer le graphe dans un bloc à part, avec des indications
  éparpillées, **complique la lecture**. Un graphe se lit sans notice : il lui
  faut une bonne **légende** et des **labels clairs**, pas un mode d'emploi.

Constat plus large assumé : « **de gros progrès à faire en narration** ».

**Prochain chantier décidé (rien n'est encore fait) — retravailler les LABELS du
nuage**, avant toute légende. Trois axes de travail donnés par l'utilisateur :
1. **les noms** — aujourd'hui « attribué à », « ? », « école de », « atelier »,
   « entourage », « suiveur », « manière de », « genre de » sont **jetés tels
   quels** sur l'axe ;
2. **leur valeur / signification** — le lecteur ne sait pas ce que veut dire
   « attribué à », « manière de »… ; le sens n'est donné nulle part ;
3. **leur forme et leur présentation** — labels mal mis en évidence ; cas criant :
   le label « **?** » seul **n'a aucun sens** affiché ainsi.

Ordre : on travaille les labels d'abord (noms + sens + présentation), la légende
ensuite. La réflexion « forme de légende » (pistes groupée/à plat) est **en
attente**, ne pas l'implémenter. Chapô/bio à réduire aussi, mais **plus tard**.

## 2026-07-09 — Refonte des textes de « Les presque » : séparer les trois natures

Constat utilisateur : les textes de la fiche maître étaient « n'importe quoi » —
techniques, non publiables. Diagnostic partagé : le défaut est **structurel**, le
mode d'emploi de la dataviz avait envahi l'éditorial. Trois natures de texte
mélangées (éditorial / mode d'emploi / mentions techniques).

Fait (mode plan validé, deux maîtres témoins jugés sur pièce avant généralisation) :
- **Éditorial séparé** : nouveau `web/src/lib/editorial-maitres.js` (bio + angle
  par maître, couche éditoriale du front, pas des données). Témoins écrits main :
  **François Clouet** (doute proche, « atelier ») et **Rembrandt** (doute lointain,
  « à la manière de »). Les 25 autres : angle **dérivé** de la famille dominante
  (repli honnête). Chiffres racontés en français (`fractionEnMots`).
- **Mode d'emploi sorti une seule fois** : bulle dépliable « Comment lire ce
  graphique » à côté de la bascule ; retiré de chaque fiche (figcaption + lecture
  du nuage supprimés). La mise en garde d'attribution y est déplacée.
- **Légende de portrait normée** : sujet + auteur + source + licence (plus de note
  de méthode déguisée en légende).
- **Vocabulaire interne banni** de l'interface : notice→œuvre, plus de « niveau »
  affiché, « atelier (qualificatif, beaux-arts) »→« atelier de », vue Détail
  nettoyée (colonne « Niveau » retirée, « Œuvres »).
- **CLAUDE.md** : ajout des blocs « Principes de dataviz » et « Principes de
  rédaction » pour que ces règles s'appliquent d'office. Consigné dans decisions.md.

Vérifié par captures (Le Brun = angle dérivé, Clouet, Rembrandt, vue Détail) et
`npm run build` OK. Reste (P3-T1) : écrire les 25 bios/angles à la main ;
reformuler l'accueil (« notices », « lexique ») en gardant les deux dénominateurs.

## 2026-07-09 — Retour sur le nuage : plus cohérent, mais trop anonyme

Verdict utilisateur sur le nuage : **plus cohérent narrativement et plus lisible**
que la galaxie et les barres — mais **manque de présence visuelle, trop anonyme**.
À traiter (consigné, pas encore implémenté) :
- **Retirer les libellés de niveau** (« Presque lui / Autour de lui / Son style ») :
  jugés inutiles ici → à enlever.
- **Ajustement proportionnel** : **points plus gros** + **grille plus resserrée**
  (trop d'écart entre les points hauts/bas et gauche/droite) → viz plus dense,
  plus forte.
- **Couleurs : plus tard** (au moment du style + de la légende des labels) ;
  aujourd'hui elles renforcent l'anonymat, on n'y touche pas maintenant.
- **Idée à évaluer (portrait) :** placer un **portrait libre de droit du peintre**
  (dessin/photo/gravure, via Wikimedia Commons) **en face** de la visualisation,
  celle-ci sur une **plus petite grille** pour que les points soient plus présents.
  Évaluation dans docs/roadmap.md + réponse à l'utilisateur (faisabilité PD,
  cohérence des images, illustration ≠ source de comptage).

Choix utilisateur : « ajustements + maquette portrait ». Implémenté (même branche) :
libellés de niveau retirés, points plus gros (rayon 6→16), grille resserrée
(viewBox compact), **layout portrait ↔ nuage** avec un **placeholder** (silhouette
inline) pour juger les proportions avant de sourcer les vraies images. Build OK.
Reste (①quater) : sourcer les 27 portraits PD + traitement uniforme + crédits +
fallback, après validation du layout. Contrainte notée : sourcing réseau incertain
dans l'environnement → images à fournir ou à tester le moment venu.

## 2026-07-08 — « Les presque » : barres → nuage de points à grille fixe

- Les barres livrées le matin ne permettaient ni comparaison entre maîtres (grille
  changeante) ni lecture des volumes réels (normalisation à la largeur). Remplacées
  par un **nuage de points sur grille fixe/commune** (decisions.md).
- Vérifié sur données : 8 familles réelles chez les 27 (« présumé » absent → colonne
  retirée) ; plafond Y commun = 240 (« école de » Le Brun), calculable côté front
  (aucune modif pipeline). Coût assumé signalé : petits volumes/petits maîtres au
  plancher — contré par le cadrage, pas en trichant sur l'échelle.
- Implémenté sur la même branche `feat/les-presque-barres` : `NuageFamilles.svelte`
  (axe X familles, axe Y volume plafonné, couleur/famille groupée par niveau,
  graduations, survol), bascule « Nuage / Détail », `BarresFamilles.svelte` retiré
  (remplacé, l'historique git le garde). Galaxie toujours archivée. Build OK.
- Stop pour validation avant le palier données géo + carte.

## 2026-07-08 — Réorientation « Les presque » : galaxie abandonnée, barres + carte

- Suite au brief utilisateur : galaxie abandonnée dans cette vue (schéma
  moléculaire, pas une constellation ; « vraie constellation » reportée en réserve,
  branche séparée). Remplacée par des **barres horizontales** (1 barre = 1 famille,
  longueur ∝ notices). Ajout d'une **carte par maître** (nouveauté).
- Faisabilité carte vérifiée sur données réelles : grain = musée détenteur
  (coord via musees.json, 98,7 %) ; doute très dispersé (~1/musée, sauf Le
  Primatice). Piège repéré : le champ `musees` d'artistes.json confond
  ferme/copie/doute → export à enrichir avant la carte.
- Arbitrages utilisateur : technique carte = **D3-geo auto-hébergé** (GeoJSON
  France/départements open data, aucune tuile externe, pré-rendable) ; ordre =
  **barres → carte**. Consigné dans decisions.md + roadmap.md (P3-T1 réorienté).
- Rien implémenté (mode plan). Prochain palier : ① barres horizontales.

## 2026-07-08 — Doc d'analyse de « Les presque »

- Galaxie jugée **lisible** par l'utilisateur. Restent à travailler : le style
  (identité propre, non générique), les labels (trop techniques) et le récit
  (la forme actuelle s'éloigne de la vision « galaxie/constellation » voulue).
- À sa demande, rédigé `docs/dataviz-les-presque.md` : document **autonome**
  (compréhensible sans le code) décrivant la dataviz sur les plans technique et
  esthétique, avec la synthèse des écarts intention ↔ réalisation et les
  questions ouvertes. Destiné à être analysé de l'extérieur.
- Rien changé au code : c'est un état des lieux pour décider de la suite.

## 2026-07-07 — P3-T1 : galaxie + retour « incompréhensible »

- Retour utilisateur fort : le front actuel est incompréhensible pour un visiteur
  lambda (on ne sait pas ce que fait le site, son objectif, son fonctionnement ;
  les fiches sont du jargon). Décision commune : **finir les tâches de la roadmap
  puis faire un bilan compréhension**, ne pas tout refondre maintenant. Noté en
  mémoire (feedback [[front-probleme-comprehension]]).
- Galaxie construite (`lib/GalaxieMaitre.svelte`) et branchée en bascule
  « Galaxie / Détail » sur `/les-presque` (galaxie par défaut). Maître au centre,
  familles de doute en orbites (proche = probable, loin = doute fort), copies
  « d'après » en anneau extérieur à part. Rendue auto-explicative pour attaquer
  le problème de compréhension : titre en clair, centre légendé, orbites nommées,
  note de lecture (« position indicative, pas une mesure d'authenticité »).
- Intro de `/les-presque` réécrite en langage courant (mode d'emploi « 👉 choisissez
  un maître… force du doute »). Build statique OK, une seule galaxie rendue.
- Reste : regarder le rendu ; l'onboarding global du site (accueil) reste à revoir
  au bilan.

## 2026-07-07 — P3-T0 validé + P3-T1 : « Les presque » (1re dataviz)

- Socle validé par l'utilisateur (sur le fond). Réserve indicative : le style est
  jugé « trop Claude normé », générique ; identité visuelle à retravailler plus
  tard (après les dataviz). Noté en mémoire (feedback) et decisions.md ; on n'y
  touche pas maintenant.
- 1re dataviz montée : route `/les-presque`. Composants réutilisables créés :
  `lib/joconde.js` (lien POP aligné sur src/config.py, métadonnées des 3 niveaux)
  et `lib/BarreNiveaux.svelte` (barre empilée du doute, avec/sans légende).
- Fiche « presque » : échelle du doute, tableau des formules employées, bande
  « d'après X » isolée (copies assumées, jamais comptées comme doute), exemples
  réels avec liens POP. Liste des 27 maîtres filtrable à gauche.
- Garde-fou éditorial en place (chapô « comment les musées nuancent », pas de
  « trésor caché »). Build statique OK, données réelles vérifiées dans build/.
- Limite assumée : le « moteur de recherche sur toute la base » (roadmap) n'est
  pas fait — il faut d'abord un export de tous les noms + comptages (pas encore
  produit). Pour l'instant le filtre porte sur les 27 vedettes.
- Reste : validation utilisateur de « Les presque » ; réserve Bruegel/Cranach
  toujours ouverte ; style à reprendre ; puis brique suivante.

## 2026-07-07 — P3-T0 : socle SvelteKit monté (en attente de validation)

- Échafaudage `sv create` dans `web/` : SvelteKit 2 / Svelte 5, JavaScript (pas
  TS, choix lisibilité), adapter static. Surprise notée : la nouvelle version
  câble l'adapter dans `vite.config.js` (`sveltekit({ adapter: adapter() })`),
  pas dans un `svelte.config.js` — ce dernier n'existe pas, c'est normal.
- Site entièrement pré-rendu : `export const prerender = true` à la racine.
- Accès aux données : `npm run sync:data` copie `data/exports/web/*.json` vers
  `web/static/data/` (servis en `/data/…`). Dossier généré, ignoré par git ;
  à resynchroniser après chaque export du pipeline Python.
- Coquille : `+layout.svelte` (en-tête, nav « une brique = une route », briques
  futures en placeholder pour ne pas casser le pré-rendu), tokens de style
  (`lib/styles/tokens.css`, couleurs des 3 niveaux).
- « Hello data » : l'accueil pré-rend le chiffre vedette réel **24 507**
  (+ 18 716 hors monoculture, provenance datée) depuis `niveaux.json`.
- `npm run build` OK, chiffre vérifié dans le HTML statique de `web/build/`.
- Reste : ⏸ validation utilisateur du socle avant la 1re dataviz (« Les presque »).

## 2026-07-07 — Stack du front arrêtée : SvelteKit

- Choix de socle tranché par l'utilisateur : **SvelteKit en build statique**
  (`adapter-static`), front isolé dans un dossier dédié, consommant les JSON de
  `data/exports/web/`. Aucun serveur (règle « jamais la base dans l'appli »).
- Motifs consignés (docs/decisions.md) : routage = structure éditoriale (méthode
  au même rang), coquille partagée par composants, bonne cohabitation avec D3,
  lisible pour un dev intermédiaire.
- Roadmap : P3-T0 réécrit en « Socle SvelteKit » avec sous-étapes
  (échafaudage → accès aux JSON → coquille → hello data → ⏸ validation).
- Prochaine action : monter le socle SvelteKit avant la 1re dataviz (« Les presque »).

## 2026-07-07 — P3-T1 : entrée « par l'artiste » (liste vedette + export)

- Ouverture de la phase 3 côté données : la 1re dataviz sera « Les presque »
  (doute autour d'un maître connu). Critère de la liste vedette arrêté par
  l'utilisateur : maître de référence + ≥ 20 doutes (hors copie), choix « A »
  (le critère fait loi).
- Correction de repérage majeure trouvée en chemin (docs/donnees.md) : le doute
  s'écrit aussi HORS parenthèses (Ingres 13 → 204) et les « (école allemande) »
  sont des nationalités, pas du doute (Dürer 161 → 19). Comptage refait avec les
  regex réelles de markers.py, par segment.
- Désambiguïsation des familles : Fragonard = Jean-Honoré (31, conservé) ;
  Bruegel et Cranach l'Ancien retirés (< 20 une fois le maître isolé du fils).
  Liste finale : **27 maîtres**.
- Code : markers.py::famille_segment() (public, réutilise le lexique, 35 tests
  verts) + src/build_artistes.py → data/exports/web/artistes.json (44 Ko).
- Roadmap phase 3 réécrite (P3-T1 en cours). Reste : réserve Bruegel/Cranach à
  trancher, puis le front de « Les presque ».

## 2026-07-06 — P2-T4 : cas racontables

- Décision : Alençon = ouverture, incarnation de la limite (vérif. approfondie
  la veille : versement partiel confirmé par l'API).
- docs/cas.md : 4 cas rédigés avec données réelles — Alençon (l'absent),
  Nice/Barla (doute industriel), Besançon (vrai doute Géricault, miroir
  d'Alençon), Louvre/Clouet (doute + révision, généalogie d'avis datés).
- src/build_cases.py → data/exports/web/cas.json (notices réelles par référence).
- Interruption (classifieur Bash indisponible) absorbée sans perte grâce au
  découpage repris-si-interrompu ; repris le 2026-07-06.
- Reste : P2-T4f (cas par niveau, optionnel) + validation utilisateur.

## 2026-07-05 — P2-T3 : pipeline d'exports + deux découvertes

- src/build_exports.py : 4 JSON légers (provenance 0,5 Ko, niveaux 2 Ko,
  musees 182 Ko, territoires 14 Ko). Provenance datée intégrée. Niveaux en
  partition stricte (chaque doute au niveau le plus léger). Bug NaN→null corrigé.
- Découverte 1 : le muséum de Nice = 5 791 doutes, tous « Barla (attribué à) »
  (planches naturalistes), soit 23,6 % du doute national — un singleton qui
  écrase le classement. Hors Barla : ~18 716. Décision utilisateur à prendre.
- Découverte 2 : Alençon, le cas fondateur, a 109 notices versées et 0 doute —
  preuve vivante de la limite « versements incomplets ». Matière pour P2-T4.
- En attente : validation de la structure + arbitrage monoculture.

## 2026-07-05 — P2-T1 et P2-T2 : recouvrements, typologie validée, lexique v2

- P2-T1 : Venn chiffré, règles de non-addition validées par l'utilisateur.
- P2-T2 : échelle à 3 niveaux validée (« Presque lui » / « Autour de lui » /
  « Son style, sans lui »), trois arbitrages rendus (atelier → beaux-arts
  seulement, écoles-lieux écartées, ? au niveau 1).
- Lexique v2 : restriction par domaine (post-traitement dans detections(),
  colonne Domaine désormais exigée), liste versionnée des écoles-lieux,
  deux nouvelles familles écartées. 35 tests passent.
- Recomptages : doute 25 220 → **24 507** ; écartés totaux 1 868 ;
  Venn v2 : 66 420 touchées, doute + révision 4 615.
- Prochaine étape : P2-T3, pipeline d'exports JSON pour la restitution.

## 2026-07-05 — GO : phase 1 close, ouverture de la phase 2

- GO validé par l'utilisateur : la phase 1 (test go/no-go) est close.
- À sa demande, classification des familles consignée en document de
  référence : `docs/familles.md` (14 familles, 4 catégories, sens des
  formules, volumes v1, fiabilités mesurées par les deux contrôles humains).
  Rôle déterminant attendu pour la typologie (P2-T2) et les visualisations.
- Phase 2 détaillée dans la roadmap : P2-T1 recouvrements, P2-T2 typologie,
  P2-T3 pipeline JSON, P2-T4 cas racontables. Première tâche : P2-T1.

## 2026-07-05 — T5bis : bilan du mini-contrôle → recommandation GO

- Mini-lot annoté récupéré (onglet « echantillon_recheck » du même classeur
  Google Sheets ; export xlsx pour lire le second onglet, zéros restaurés).
- ? : 0/15 faux. « Atelier de X » écarté : 15/15 confirmés — on ne jette
  aucun vrai doute. École : 2/15 (écoles-lieux consacrées). Atelier : 6/20
  (ateliers-entreprises ; les faux vivent en ethnologie/artisanat, les vrais
  en peinture/dessin — piste domaine pour la phase 2).
- Doute pondéré : 5,7 % conservateur, 3,3 % ajusté → **seuil GO franchi**.
- En attente : décision de phase (fin de la phase 1).

## 2026-07-04 — Cycle v1 : reformulation du lexique

- Lexique v1 écrit et testé : l'idée-force est de lire la convention
  d'écriture (qualificatif entre parenthèses) plutôt que le mot. Détection
  « atelier » segment par segment ; nouvelle catégorie « ecarte » pour la
  population « Atelier de X » (1 123 notices), chiffrée au lieu d'être jetée
  en silence.
- Les 25 verdicts clés de l'utilisateur sont devenus des tests pytest :
  le lexique a maintenant un contrat de non-régression humain.
- Recomptage : doute 29 726 → 25 220 (−15 %). Familles corrigées :
  atelier 5 558 → 1 759, école 2 865 → 2 093, ? 2 731 → 2 213.
- Mini-lot T4bis généré : 65 lignes (graine 202607, distincte de T4).
  En attente de la vérification utilisateur.

## 2026-07-04 — T5 : bilan de la vérification manuelle

- Échantillon annoté récupéré depuis Google Sheets (206/206 verdicts ; zéros
  de tête des références restaurés — piège tableur à retenir).
- Doctrine consignée : un marqueur ne compte que s'il qualifie l'attribution
  de l'œuvre de la notice ; `(attribué, d'après)` → copie ;
  `anonyme (attribué)` → incertain, hors calcul.
- `src/evaluate_sample.py` : taux pondérés par le poids réel des familles.
  Doute : **17,0 %** de faux positifs → tranche « reformulation ».
  Copie et révision : **0 %**. Le problème est concentré (atelier de 64 %,
  école de 20 %, ? 16 %) et chaque cause est identifiée.
- Recommandation : reformulation ciblée du lexique (v1), recomptage,
  mini-contrôle sur les familles corrigées. En attente : décision de phase.

## 2026-07-03 — T4 : échantillon de vérification

- T3 validée ; décisions consignées (taux vedette = notices avec auteur ;
  comptage de référence sur toute la base, beaux-arts en angle) ; tâche
  « recouvrements entre familles » ajoutée à la phase 2.
- `src/build_sample.py` : 206 lignes tirées (stratifié, graine 42), familles
  rares sur-représentées, « présumé » (4) et « anciennement attribué » (7)
  pris en entier.
- Liens POP testés (redirection www corrigée dans config.py).
- Mode d'emploi rédigé : `docs/verification-echantillon.md`. En attente de la
  vérification manuelle de l'utilisateur — T5 démarre au retour du CSV annoté.

## 2026-07-03 — T3 : détecteur v0 et taux de base

- `src/markers.py` (lexique versionné, 13 familles) + `src/count_markers.py`.
- Deux corrections en cours de route, repérées sur les exemples réels : le « ? »
  de dates (72 % du signal brut de cette famille était du bruit !) et « école
  des Beaux-Arts » dans les biographies. Détail dans `donnees.md`.
- Résultat : 29 726 notices avec au moins un marqueur de doute (2,90 % de la
  base, 3,53 % des notices avec auteur). « d'après » : 22 564 (à part).
  Champ Ancienne_attribution : 27 266. La peinture est le domaine au taux le
  plus élevé (6,00 %), le dessin le plus gros volume.
- En attente : validation T3, choix du dénominateur vedette et du périmètre.

## 2026-07-03 — T2 : profilage du CSV complet

- T1 validée. Consigne métier ajoutée à `donnees.md` : distinguer « école de
  [artiste] » (doute, dans Auteur) de `Ecole_pays` (nationalité).
- `src/profile_data.py` : parcours du CSV en une passe (~1 min).
- Résultats clés : 1 023 705 notices, 555 musées ; l'extrait API omet 29,5 % de
  la base ; Auteur renseigné à 82,2 % ; coordonnées à 99,8 % (carto quasi
  intégrale possible) ; périmètre peinture/dessin/sculpture/estampe = 57 % de
  la base. Détail dans `donnees.md`, rapport brut dans `data/exports/profil.txt`.
- En attente : validation T2 et choix du périmètre.

## 2026-07-03 — T1 : téléchargement et nomenclature

- Phase 0 validée par l'utilisateur ; seuils T5 confirmés ; titre adopté :
  « L'inventaire du doute ». Création de `docs/roadmap.md` (suivi par cases à cocher).
- CSV téléchargé : 1,19 Go, 67 colonnes, séparateur `|`, en-têtes identiques aux
  noms de champs de l'API. Nomenclature ODS lue (77 intitulés, étiquettes
  documentaires REF/AUTR/ATTR/PAUT/ECOL…).
- Mapping des champs documenté dans `donnees.md` : champs cœur (Auteur,
  Precisions_sur_l_auteur, Ancienne_attribution, Ecole_pays), garde-fous
  (Sujet_Represente, Titre…), contexte (Domaine multivalué `;`, coordonnees…).
- Lecture pandas validée sur échantillon. Prochaine étape : T2 (profilage complet).

## 2026-07-03 — Initialisation du projet (phase 0)

- Brief validé, plan approuvé, arborescence créée (CLAUDE.md, docs/, src/, data/).
- Exploration préalable menée via l'API du ministère (voir `donnees.md`) :
  l'écart de volumétrie entre data.gouv (> 1 M notices) et le portail du ministère
  (~700 k) est éclairci — le dataset API est un **extrait**.
- Premiers sondages encourageants : les formules d'incertitude existent bien dans
  les données et le champ auteur suit une convention structurée (qualificatifs
  entre parenthèses).
- Prochaine étape : T1 — téléchargement du CSV et de la nomenclature ODS,
  documentation du mapping des champs.
