# Chantier images POP — plan final

**Statut : plan arrêté le 2026-08-24 ; étapes 0 à 2 terminées ; profil D retenu
le 2026-08-25 ; étape 3 autorisée.**

Ce document remplace la proposition de travail initiale. Les constats ont été
vérifiés dans le dépôt, la contre-proposition a été rendue, et les arbitrages
ci-dessous ont été tranchés par le responsable du projet. Ce qui suit est la
consigne d'exécution : aucun point marqué « acté » n'est à rouvrir.

Aucun code n'a encore été écrit et aucun téléchargement n'a été lancé.

---

## 1. Objectif et décisions actées

Le projet doit pouvoir être évalué avec les reproductions réellement disponibles
sur POP, sans rester limité aux images ouvertes déjà trouvées sur Wikimedia
Commons et Gallica.

Décisions définitives :

1. **Les images POP sont intégrées à la version locale ET à la version publiée
   sur GitHub Pages.** La variante consistant à dissocier les deux (POP en local,
   images ouvertes seules en ligne) a été examinée et **écartée**. Cette décision
   n'est plus à rouvrir.
2. **Les JPEG restent versionnés dans Git** pour cette phase, conformément au
   pipeline et au workflow actuels. Aucun passage à Git LFS ni génération en CI.
3. Les images Wikimedia Commons et Gallica déjà en place sont conservées, sauf
   dans le cas de bascule décrit au §4.
4. Le dispositif technique et visuel existant est repris, pas dupliqué.
5. Le résultat est contrôlé dans le serveur de prévisualisation du **build**
   avant tout commit et tout push.

---

## 2. État vérifié du dispositif

Chiffres recomptés dans le dépôt le 2026-08-24 — tous conformes aux constats
initiaux.

| Constat | Valeur |
|---|---|
| Références du corpus | 6 081 |
| Références avec URL d'image POP | 5 512 |
| … dont crédit photographique renseigné | 5 377 |
| … dont crédit vide | 135 |
| Entrées de `images_index.json` | 209 (195 Commons + 14 Gallica) |
| … montrant l'objet même du musée | 192 |
| … portant `exemplaire_autre: true` | 17 |
| Entrées de l'index ayant aussi une image POP | 203 |
| Nouvelles candidates POP | 5 309 |

Statuts d'audit des images POP : `restricted` 3 192, `unknown` 2 320 (les 2 322
`unknown` du registre comptent 2 références sans URL exploitable), `unavailable`
567 — ces dernières n'ont pas d'image et sortent du périmètre.

### Ce que le code fait aujourd'hui

- `src/build_vignettes.py` **reconstruit l'index à zéro** à chaque exécution, en
  trois passes successives : Commons `exact` + `open`, puis `ajouter_gallica()`,
  puis `ajouter_imagerie_commons()`. Les deux dernières sautent toute référence
  déjà présente (`if ref in index: continue`). La priorité est donc **un ordre
  d'appel**, pas une comparaison — c'est ce mécanisme que POP prolonge.
- `fusionner_dans_oeuvres()` attache `image` dans chaque `oeuvres/<slug>.json`
  et **retire** la clé quand la référence a disparu de l'index.
- `web/scripts/sync-data.js` copie `data/exports/web/oeuvres_img/` vers
  `web/static/oeuvres/`, gitignoré côté front.
- Le workflow GitHub Pages fait `checkout` → `npm run sync:data` → build avec
  `BASE_PATH=/inventaire-du-doute`. **Les JPEG doivent donc être versionnés à la
  racine pour être publiés** : il n'existe aucun autre chemin.

### Deux défauts à corriger avant tout traitement de masse

**a. La reprise sur interruption n'existe pas.** Le code teste
`if not sortie.exists()` : il vérifie la **présence** du fichier, jamais sa
validité. Une interruption pendant `im.save()` laisse un JPEG tronqué qui ne sera
jamais retéléchargé et s'affichera cassé. Sur 209 images en une passe, le risque
est théorique ; sur plus de 5 300 images et un traitement dont la durée reste à
mesurer, une interruption doit être considérée comme normale et récupérable.

**b. Le rythme est calibré pour Wikimedia, pas pour POP.** `PAUSE = 1.0` seconde
existe parce que « Wikimedia limite le rendu des miniatures (HTTP 429) ». POP
sert des fichiers statiques depuis un stockage objet OVH. À une seconde par
image, 5 326 images coûtent **89 minutes de pauses seules**, hors téléchargement
et ré-encodage. Une constante `PAUSE_POP` distincte sera calibrée sur la sonde.

### Le point de rupture unique côté front

`web/src/lib/CreditImage.svelte` est le **seul** composant à modifier. Sa branche
finale `{:else}` écrit en dur « Domaine public · source Wikimedia Commons » : une
entrée POP non traitée afficherait une **fausse licence et une fausse source**.
De plus, `image.licence.startsWith('CC BY')` lève une exception si `licence` est
absente.

`OeuvresMaitre.svelte` et `LightboxOeuvre.svelte` ne lisent que `o.image.url` et
`o.image.exemplaire_autre`, et délèguent tout le crédit. Ils n'ont **aucun
changement fonctionnel** à recevoir (§7).

---

## 3. Paramètres, profils et budget

### 3.1 Séparer les paramètres POP des paramètres Commons/Gallica — acté

Les constantes `LARGEUR = 900` et `QUALITE = 82` restent celles de
Commons/Gallica. POP reçoit ses propres constantes (`LARGEUR_POP`,
`QUALITE_POP`). **Aucun des fichiers existants ne doit être ré-encodé** lorsqu'un
profil POP plus léger est retenu.

### 3.2 Sonde temporaire de 30 images — terminée

Quatre profils ont été mesurés sur le même **échantillon stratifié et
reproductible de 30 images POP**. Il représente les principaux cas qui
influent sur l'encodage et sur le rendu : formats verticaux et horizontaux,
photographies sombres, fonds clairs, dessins au trait, images très détaillées,
petites dimensions d'origine et rapports de forme atypiques.

| Profil | Largeur | Qualité |
|---|---|---|
| A — actuel | 900 px | 82 |
| B | 800 px | 78 |
| C — léger | 600 px | 75 |
| **D — retenu** | **800 px** | **75** |

Le profil **D est définitivement retenu**. Il conserve la largeur de 800 pixels
du profil B — donc la même définition utile dans la lightbox — tout en abaissant
la qualité JPEG de 78 à 75. Sur les images les plus détaillées de la sonde, les
recadrages B/D à 100 % n'ont montré aucune différence perceptible.

La sonde a mesuré le poids moyen et médian par profil, les dimensions d'origine,
les temps de réponse, le taux d'échec et la durée par image. Elle a produit une
extrapolation aux 5 326 images et une comparaison visuelle des quatre profils
sur les mêmes œuvres.

Résultat du profil D : **77,8 Ko de moyenne**, 72,7 Ko de médiane, 33,1 à
194,4 Ko selon les images ; **404 Mo extrapolés** pour les 5 326 fichiers et
**440 Mo pour le build complet**. Sa marge estimée est de 10,1 % sous le budget
des images et de 20 % sous celui du build.

### 3.3 Budget arrêté

| Poste | Plafond |
|---|---|
| Nouvelles images POP | **450 Mo** |
| Build GitHub Pages complet | **550 Mo** |

Pour que les contrôles soient reproductibles, ces plafonds sont mesurés en
octets avec la convention **1 Mo = 1 024² octets**.

Conséquences calculées :

- 450 Mo pour 5 326 images ⇒ **86,5 Ko par image en moyenne, plafond absolu** ;
- la sonde mesure le profil A à 104,3 Ko de moyenne, soit **542 Mo d'images POP**
  et un build estimé à **578 Mo** : il dépasse les deux budgets ;
- le profil D retenu projette **404 Mo d'images POP** et un build d'environ
  **440 Mo**. L'étape 6 contrôlera les poids réels, l'extrapolation sur trente
  images ne constituant pas une garantie absolue ;
- projection du build : 11,6 Mo (hors images) + 24,0 Mo (192 vignettes
  conservées) + 450 Mo (POP) = **486 Mo**, soit 64 Mo de marge sous le plafond
  de 550 Mo ;
- dépôt Git : ~72 Mo aujourd'hui + ~450 Mo ⇒ **~520 Mo**, sous la limite de 1 Go
  de GitHub.

**Critère d'arrêt.** Le profil D satisfait l'extrapolation budgétaire de la
sonde. Les poids réels seront de nouveau contrôlés au lot témoin puis sur la
génération complète ; aucun dépassement ne sera versionné ou publié sans nouvel
arbitrage.

---

## 4. Priorité éditoriale — arbitrage final

La priorité ne se lit plus sur la **provenance** mais sur **ce que l'image
montre**. Ordre définitif :

1. **Commons**, lorsqu'il montre exactement l'objet du musée ;
2. **POP**, lorsqu'il montre l'objet du musée ;
3. **Commons ou Gallica**, lorsqu'il s'agit d'un autre exemplaire.

Cet ordre est cohérent avec la règle déjà écrite dans le code : la réserve se lit
sur la donnée, jamais sur la provenance.

### Conséquence : les 17 bascules

Les **17 entrées portant `exemplaire_autre: true` disposent toutes d'une image
POP**. Elles montrent une autre feuille du même tirage — une planche d'Épinal
imprimée à des milliers d'exemplaires, dont le musée conserve la sienne et la
bibliothèque la sienne. L'image POP, elle, montre l'objet du musée.

**Ces 17 entrées sont donc remplacées par POP.**

### Composition de l'index après application

| Origine | Entrées |
|---|---|
| Commons / Gallica conservées (objet du musée) | 192 |
| POP en remplacement des « autres exemplaires » | 17 |
| POP nouvelles | 5 309 |
| **Total** | **5 518** |

Parmi les 192 conservées, 186 ont une image POP disponible qui **n'est
délibérément pas retenue** (Commons montre déjà l'objet du musée) et 6 n'ont
aucune image POP.

### ⚠ Le piège d'invalidation — traitement obligatoire

Les 17 fichiers concernés **existent déjà sur le disque sous le même nom
`<reference>.jpg`**. Un simple changement d'ordre des passes ferait que
`ajouter_pop()` trouverait le fichier présent, **sauterait le téléchargement**, et
écrirait pourtant une entrée d'index `source_type: pop_joconde` avec le crédit
et le lien POP — pointant sur l'ancien JPEG Commons ou Gallica. Ce serait une
**fausse attribution**, exactement ce que `CreditImage` a été écrit pour
empêcher.

Le pipeline doit donc utiliser **l'index précédent déjà chargé dans
`_INDEX_PRECEDENT` comme état de référence**, sans créer un second manifeste qui
dupliquerait cette information :

- chaque nouvelle entrée POP porte un identifiant de `profil` d'encodage stable,
  en plus de son `source_type` ;
- **invalidation sur changement de source** : si le `source_type` voulu diffère
  de celui de l'index précédent, le fichier est considéré périmé et retéléchargé,
  quelle que soit sa présence sur le disque ;
- **invalidation sur changement de profil POP** : si le profil voulu diffère de
  celui de l'index précédent, seul le fichier POP concerné est régénéré. Les 192
  vignettes Commons/Gallica, qui conservent leurs paramètres actuels, ne sont
  jamais ré-encodées par un changement de profil POP ;
- **un remplacement atomique explicite** : écriture dans `<reference>.jpg.tmp`
  puis `os.replace()`, jamais d'écriture en place. Ceci corrige du même coup le
  défaut de reprise du §2-a ;
- **une validation des fichiers déjà présents** (`Image.open().verify()`) lors
  des reprises, pour détecter les JPEG tronqués d'une exécution interrompue.

La source de vérité reste ainsi le seul `images_index.json`, versionné. Sa
version précédente permet de décider si le fichier présent correspond à la
source et au profil attendus ; sa nouvelle version décrit exactement ce qui a
été produit. Le CI n'exécute jamais `build_vignettes.py`, il ne fait que
`sync:data` et le build.

### Contrôle d'intégrité final — obligatoire

Empreintes SHA-256 des 209 fichiers relevées **avant** la génération, comparées
**après** :

- **192 images existantes strictement inchangées** (empreinte identique) ;
- **17 remplacements intentionnels** : empreinte modifiée **et** entrée d'index
  passée à `source_type: pop_joconde` ;
- **aucune autre image Commons ou Gallica écrasée** : toute empreinte modifiée
  hors de ces 17 est un échec du contrôle et bloque la suite.

---

## 5. Métadonnées POP dans l'index

Chaque entrée POP porte :

| Champ | Valeur |
|---|---|
| `source_type` | `"pop_joconde"` |
| `url` | `"oeuvres/<reference>.jpg"` |
| `credit` | le crédit photographique **tel qu'extrait**, chaîne vide si absent |
| `licence` | `""` — toujours présente, jamais absente |
| `source` | le **lien de la fiche POP**, jamais l'URL brute du stockage objet |
| `statut` | `restricted` ou `unknown`, **recopié du registre d'audit** |
| `verifie_le` | la date déjà présente dans le registre |
| `profil` | l'identifiant stable du profil POP réellement utilisé |

Règles actées :

- **ne jamais créer de statut `open` ou `authorized`** pour une image POP. Le
  statut est recopié tel quel du registre d'audit ;
- `data/exports/images_oeuvres.json` est le **registre d'audit** : il n'est ni
  modifié ni réécrit par ce chantier ;
- pour les 135 images sans crédit, **le champ `credit` reste vide dans l'index**.
  Le repli d'affichage n'est pas écrit dans la donnée : la source n'a jamais
  produit cette phrase.

---

## 6. Crédits — `CreditImage.svelte`

Le composant reçoit un **cas `pop_joconde` explicite** et devient **défensif
lorsque `licence` est absente**.

Formulation retenue, sous la vignette comme dans la lightbox :

> `crédit exact · source POP`

et, en l'absence de crédit :

> `Crédit photographique non précisé · source POP`

Règles :

- **aucune mention supplémentaire de licence** — ni « licence non précisée », ni
  « domaine public », ni rien d'autre ;
- « POP » est un lien vers la **fiche de l'œuvre**, jamais vers le fichier ;
- le repli « Crédit photographique non précisé » vit **uniquement dans
  `CreditImage.svelte`** ;
- le composant reste la **source unique** de la ligne d'attribution : la vignette
  et la lightbox affichent la même, jamais deux formulations.

---

## 7. Vignettes, aperçus et zoom

`OeuvresMaitre.svelte` et `LightboxOeuvre.svelte` **ne reçoivent aucun changement
fonctionnel**. Leurs comportements existants sont **testés, pas reconstruits** :

- même gabarit (boîte 4/5 partagée avec le placeholder) ;
- `object-fit: contain`, aucune déformation ni découpe ;
- chargement différé déjà en place ;
- texte alternatif construit sur le titre de l'œuvre ;
- crédit immédiatement sous l'image, via le composant partagé ;
- œuvres illustrées avant les œuvres sans image (tri `a.image ? 0 : 1`), déjà
  agnostique de la source ;
- placeholder « Reproduction non disponible » conservé pour les 563 références
  restant sans image ;
- lightbox : même fichier local que la vignette, proportions conservées, pas
  d'agrandissement au-delà du fichier, titre et même crédit, fermeture par
  bouton / Échap / fond, piège à focus, blocage du défilement arrière, retour du
  focus à la vignette d'origine.

**Une seule retouche non fonctionnelle est prévue dans `OeuvresMaitre.svelte`** :
le commentaire du placeholder dit « Pas de reproduction **réutilisable** connue »
(ligne ~343). Cette phrase devient factuellement fausse dès lors que des images
non réutilisables sont affichées. Elle sera corrigée en commentaire — **c'est un
commentaire de code, pas un texte public**, et il n'entre pas dans le §9.

Un point à surveiller sans le traiter d'avance : avec 5 518 images au lieu de
209, une page de la liste (8 œuvres) charge jusqu'à 8 reproductions au lieu de 0
à 2. À contrôler sur le lot témoin ; c'est un argument supplémentaire en faveur
d'un profil léger.

---

## 8. Plan d'exécution

Neuf étapes courtes. Chacune s'arrête sur un point de contrôle.

### Étape 0 — fiabiliser la reprise *(terminée, aucun téléchargement)*

Écriture atomique, validation des fichiers présents et comparaison avec l'index
précédent pour l'invalidation sur source et sur profil. Rejouer le build sur les
209 images existantes : il doit annoncer **0 nouveau téléchargement** et un
index identique.

### Étape 1 — le cas POP dans `CreditImage.svelte` *(terminée, aucun téléchargement)*

Branche `pop_joconde`, repli de crédit, défense sur `licence`. Vérifiable
immédiatement sur une entrée factice, sans aucune image.

### Étape 2 — sonde temporaire de 30 images *(terminée)*

**Un script jetable, dans un répertoire temporaire.** La sonde :

- écrit dans un dossier temporaire hors du dépôt, **jamais dans
  `data/exports/`** ;
- ne touche ni `images_index.json`, ni `oeuvres_img/`, ni les fiches d'œuvres ;
- conserve ses mesures et sa planche comparative dans le répertoire temporaire
  jusqu'à la validation visuelle du profil, puis les supprime ;
- n'est **pas** committée.

Elle a produit le tableau des quatre profils, l'extrapolation aux 5 326 images
et une planche de comparaison visuelle. Le profil D (800 px / qualité 75) a été
retenu le 2026-08-25.

### Étape 3 — lot témoin intégré de 12 références *(terminée)*

Distinct de la sonde : le lot témoin **passe par le vrai pipeline** et **écrit
réellement** dans `data/exports/web/` (12 fichiers seulement). C'est lui qui
valide la chaîne complète, pas la sonde. Composition au §10.

Résultat : 11 images POP intégrées (10 nouvelles et 1 remplacement), 219
entrées dans l'index. La relance contrôlée du lot ne télécharge rien et ne
modifie aucun JPEG.

### Étape 4 — point d'arrêt et validation *(terminée)*

`sync:data`, build avec `BASE_PATH`, serveur de preview, contrôle complet,
captures. **Arrêt et présentation.** Le build du lot témoin pèse 39,4 Mo et les
219 images répondent sous le préfixe de production, sans 404 constatée dans le
crawl. Les contrôles à 390 px et 1440 px, le zoom, le clavier, les crédits, les
filtres et la pagination sont validés.

### Étape 5 — génération complète *(terminée)*

Traitement des références restantes, journal des échecs, bilan
réussis / ignorés / échoués. Résultat final après reprise ciblée : **5 324
images POP**, 192 Commons exactes conservées et **5 516 JPEG** au total. Les 11
URLs contenant des espaces ou des caractères non ASCII ont été correctement
encodées puis récupérées ; seules deux images annoncées par POP restent absentes,
car leur serveur répond réellement 404 (`M0303004360` et `M0303004387`).

### Étape 6 — contrôle d'intégrité et de volumétrie *(contrôle préalable validé)*

Le contrôle 192 / 17 / 0 du §4. Nombre d'images, poids total, poids du build
comparé aux plafonds, recherche de JPEG tronqués, de chemins manquants et de 404.
Avant synchronisation : contrôle **192 / 17 / 0** conforme, 5 516 fichiers pour
5 516 entrées, aucun fichier manquant, orphelin ou illisible, et 303,2 Mio
d'images POP. Le poids du build et le crawl final restent à mesurer après le
nouveau build.

### Étape 7 — documentation interne

`docs/decisions.md`, `docs/donnees.md`, mise à jour de ce document. **Les textes
publics ne sont pas touchés** (§9).

### Étape 8 — revue

Livraison de l'implémentation et du serveur local. Codex relit le diff, le
pipeline, les données générées et le rendu. **Ni commit ni push avant cette
revue.**

---

## 9. Textes publics — hors périmètre de la première implémentation

Les formulations publiques sont **traitées séparément et soumises une par une à
validation**. Elles ne sont **pas** réécrites pendant la première implémentation.

Passages repérés, pour mémoire :

- `web/src/routes/methode/+page.svelte:396-397` — « [les images de] POP ne sont pas
  réutilisées lorsqu'aucune autorisation explicite ne le permet. » Cette phrase
  contredit frontalement le chantier ;
- `web/src/routes/methode/+page.svelte:399-402` — « proviennent principalement de
  Wikimedia Commons » ;
- `README.md:106` — « 209 reproductions d'œuvres » ;
- `README.md:122-123` — la limite affichée sur l'absence de reproduction ;
- `web/src/routes/projet/+page.svelte:41` — commentaire de code mentionnant
  « image réutilisable ».

---

## 10. Lot témoin intégré — composition

Douze références **choisies**, non tirées au hasard :

| # | Cas |
|---|---|
| 1 | image verticale |
| 2 | image horizontale |
| 3 | image très petite ou de format atypique |
| 4 | crédit musée renseigné |
| 5 | **sans crédit** (une des 135) — vérifie le repli d'affichage |
| 6 | **crédit RMN, statut `restricted`** — vérifie la recopie du statut |
| 7 | référence ayant déjà une image Commons **exacte** — doit rester Commons |
| 8 | **une des 17 `exemplaire_autre`** — doit basculer sur POP, fichier remplacé |
| 9 | statut `unknown`, avec photographe nommé |
| 10 | crédit particulièrement long — vérifie la tenue de la légende |
| 11 | dessin au trait très détaillé — vérifie visuellement le profil retenu |
| 12 | référence d'un artiste à forte volumétrie (Le Brun, 310 œuvres) |

Vérification dans la liste **et** dans la lightbox, à 390 px et à 1440 px.

Les cas destructifs ou artificiels — URL absente, URL volontairement fausse,
fichier tronqué, interruption pendant l'écriture — sont vérifiés séparément par
les tests dans un répertoire temporaire. Ils ne modifient jamais le registre
d'audit ni le lot témoin intégré.

---

## 11. Fichiers concernés

**Modifiés — code**

| Fichier | Nature |
|---|---|
| `src/build_vignettes.py` | `ajouter_pop()`, comparaison avec l'index précédent, invalidation source/profil, remplacement atomique, `LARGEUR_POP` / `QUALITE_POP` / `PAUSE_POP`, bilan |
| `web/src/lib/CreditImage.svelte` | cas `pop_joconde`, défense sur `licence` |
| `web/src/lib/OeuvresMaitre.svelte` | **commentaire uniquement** (§7), aucun changement fonctionnel |

**Créés — code**

| Fichier | Nature |
|---|---|
| `tests/test_vignettes_pop.py` | priorité et bascules, forme des entrées, crédit vide conservé, `source` = fiche POP et jamais l'URL du stockage objet, invalidation sur changement de source ou de profil, reprise d'un JPEG tronqué, échec atomique sans corruption du fichier précédent |

**Générés — données versionnées**

- `data/exports/web/images_index.json` — 209 → 5 516 entrées dans le résultat
  effectif (cible théorique 5 518 ; deux images POP répondent 404) ;
- `data/exports/web/oeuvres/*.json` — 102 fichiers, clé `image` fusionnée ;
- `data/exports/web/oeuvres_img/*.jpg` — +5 309 fichiers, 17 remplacés.

**Modifiés — documentation interne**

`docs/decisions.md`, `docs/donnees.md`, le présent document.

**Non modifiés**

`web/src/lib/LightboxOeuvre.svelte`, `web/scripts/sync-data.js`,
`.github/workflows/pages.yml`, `src/build_images.py`, `src/images_classify.py`,
`data/exports/images_oeuvres.json`, et l'ensemble des textes publics (§9).

---

## 12. Contrôles du build et du serveur de preview

1. depuis la racine, `uv run pytest tests/` (pipeline) puis
   `node --test web/tests/*.test.js` (front) ;
2. depuis `web/`, `npm run sync:data` — contrôler le nombre de vignettes copiées ;
3. toujours depuis `web/`, `BASE_PATH=/inventaire-du-doute npm run build` —
   **avec le préfixe**, comme le workflow ;
4. `BASE_PATH=/inventaire-du-doute npm run preview` — avec le **même préfixe
   que le build**, et toujours sur le build, jamais sur le serveur de
   développement. Sans cette variable, le serveur de preview ne reproduit pas
   le chemin de GitHub Pages et les vignettes répondent en 404 ;
5. contrôles à **390 px et 1440 px** : vignettes, crédits, liens POP, zoom,
   clavier complet, filtres, pagination ;
6. crawl automatisé des `src` d'images sur un échantillon de fiches, pour
   détecter tout 404 et tout chemin sans préfixe ;
7. mesure du poids de `web/build`, comparée au plafond de 550 Mo ;
8. captures, puis remise au responsable du projet — arrêt avant tout commit.

---

## 13. Dernier arbitrage réglé

Le profil d'encodage POP définitif est **D : 800 px / qualité 75**. Il a été
retenu après mesure du poids et comparaison visuelle dans le zoom. Les étapes 3
et 4 ont confirmé son intégration sur le lot témoin ; aucun arbitrage ne reste
ouvert avant la génération complète de l'étape 5.

---

## 14. Bilan de la génération complète (étapes 5 et 6) — 2026-08-25

Rapport rédigé après exécution, pour relecture. Les chiffres sont mesurés, pas
projetés.

### 14.1 Ce qui a été produit

| | Avant | Après |
|---|---|---|
| Entrées de `images_index.json` | 209 | **5 516** |
| JPEG dans `oeuvres_img/` | 209 | **5 516** |
| Œuvres illustrées dans les fiches | 209 | **5 458** |
| Poids du dossier d'images | 28,4 Mo | **327 Mo** |
| Poids du build complet | 39,4 Mo | **342,2 Mo** |

Composition finale de l'index : **5 324 `pop_joconde`**, 192 `wikimedia_commons`,
**0 `gallica_bnf`**, **0 entrée `exemplaire_autre`**.

### 14.2 Poids réel — nettement sous le budget

| Poste | Mesuré | Plafond | Marge |
|---|---|---|---|
| Images POP | **~327 Mo** | 450 Mo | **27 %** |
| Build complet | **342,2 Mo** | 550 Mo | **38 %** |

La sonde de trente images projetait 404 Mo ; le corpus réel pèse 100 Mo de moins.
L'écart s'explique par la stratification de la sonde, construite pour couvrir les
cas lourds (grandes estampes claires, dessins très détaillés) qui sont
surreprésentés dans un échantillon de trente et minoritaires dans un corpus
dominé par de petits dessins. Le profil D est donc confirmé avec une marge plus
confortable que prévu.

Le dépôt Git passe d'environ 65 Mo à environ 390 Mo, sous la limite de 1 Go.

### 14.3 Les 17 bascules `exemplaire_autre` — toutes faites

1 au lot témoin (étape 3), 15 à la génération complète, **1 à la reprise des
échecs**. Aucune entrée `exemplaire_autre` ne subsiste : plus aucune œuvre du
volume n'est illustrée par un autre tirage que celui du musée.

`M0537021010` mérite d'être citée : sa bascule a échoué au premier passage, et le
garde-fou a fonctionné exactement comme prévu — elle a **conservé son ancien JPEG
et son ancienne entrée Gallica** jusqu'à la reprise, sans jamais afficher un
crédit POP sur un fichier Gallica. C'est le scénario que le §4 redoutait, et il
s'est produit pour de vrai.

### 14.4 Échecs : 13 au premier passage, 2 restants

**Cause principale, un défaut du code** : `_get()` passait les URL POP à `urllib`
sans les encoder. Onze images dont le nom de fichier contient une espace, une
parenthèse ou un `©` ont été refusées — « URL can't contain control characters »,
« 'ascii' codec can't encode character '\xa9' ». Corrigé depuis
(`urllib.parse.quote` sur le chemin, la requête et le fragment), et les onze ont
été récupérées par une reprise `--lot`.

**Restent 2 échecs définitifs**, `M0303004360` et `M0303004387` : HTTP 404, POP ne
sert plus ces fichiers. Elles n'ont **aucune entrée d'index** et leurs œuvres
gardent l'emplacement vide dans les fiches — le comportement voulu. Soit
0,04 % du corpus visé.

### 14.5 Contrôle d'intégrité — CONFORME

Empreintes SHA-256 des 209 fichiers d'origine, relevées avant l'étape 3 et
comparées après la génération complète :

| Contrôle | Attendu | Mesuré |
|---|---|---|
| Images d'origine inchangées | 192 | **192** ✔ |
| Remplacements intentionnels | 17 | **17** ✔ |
| Disparitions | 0 | **0** ✔ |
| Remplacées qui ne seraient pas passées à POP | 0 | **0** ✔ |
| Inchangées qui seraient étiquetées POP | 0 | **0** ✔ |

Contrôles complémentaires, tous à zéro : entrées d'index sans fichier, fichiers
sans entrée d'index, entrées POP pointant vers Commons ou Gallica, entrées POP
portant une licence non vide, entrées POP au statut `open` ou `authorized`.

### 14.6 Contrôles du build et du rendu

`sync:data` → 5 516 vignettes copiées. Build avec `BASE_PATH=/inventaire-du-doute`
→ 342,2 Mo. Preview sur le build : les fiches contrôlées (Le Brun, François
Georgin, Titien) affichent **8 vignettes sur 8, aucun emplacement vide**, contre
une majorité de « Reproduction non disponible » auparavant. Aucune réponse HTTP
en échec, aucune erreur JavaScript. Les crédits s'affichent selon la source :
« … · source POP » pour POP, mention Wikimedia inchangée pour les 192 conservées.

**Piège de procédure à retenir** : `npm run preview` sans `BASE_PATH` sert le
build à la racine et toutes les vignettes tombent en 404. Le contrôle du préfixe
exige `BASE_PATH=/inventaire-du-doute npm run preview`. À ajouter au §12.

### 14.7 Reste à traiter

Les **textes publics du §9** ne sont pas touchés. En particulier,
`web/src/routes/methode/+page.svelte:396-397` publie toujours :

> « [les images de] POP ne sont pas réutilisées lorsqu'aucune autorisation
> explicite ne le permet. »

Cette phrase contredit désormais frontalement ce que le site affiche : 5 324
reproductions POP, dont 3 086 au statut `restricted`. **Elle doit être reprise
avant toute publication en ligne**, de même que le décompte « 209 reproductions »
du README. Chaque formulation reste soumise à validation, une par une.
