# Roadmap — L'inventaire du doute

Suivi des phases et des tâches. Mis à jour à chaque fin de tâche.
Chaque ⏸ est un point de validation utilisateur : on s'y arrête.

---

## ★ EN COURS (2026-08-02) — Volume 1 : Autour des maîtres

Objectif : publier un premier volume autonome, consacré aux artistes dont le nom apparaît
dans une notice avec une formulation prudente. Les autres angles (révisions d'attribution,
territoires, échelle nationale) sont la matière de volumes ultérieurs et ne sont pas
annoncés dans l'interface. Cadrage : decisions.md, 2026-08-02.

Deux points d'arrêt seulement dans tout le chantier — ⏸ 1 après la phase 1, ⏸ 2 avant la
fusion finale.

- [x] **Phase 0 — Consigner le changement de stratégie** (2026-08-02). Prototype d'analyse
      arbitré : la visualisation des mentions est conservable, la matrice des profils et la
      comparaison nationale sont abandonnées. La branche `refactor/analyse-maitres` reste
      intacte, jamais reportée en bloc.
- [x] **Phase 1 — Élargir la liste des artistes** (2026-08-02, branche `data/maitres-lot-2`).
      Lot borné aux **50 formes du registre portant au moins 25 notices prudentes** (77 % des
      notices restant à instruire). Relevé en une passe par `src/instruit_lot.py` : graphies,
      musées, domaines, dates écrites par les musées, références. Test d'identité en trois
      questions tranchées sur la source. **40 personnes retenues, 10 formes écartées avec
      leur motif** ; 39 des 40 entrent dans le volume (voir le point de contrôle). Un
      mécanisme ajouté, l'égalité stricte
      « = », pour le seul Jacques-Louis David. 21 témoins réels et 35 cas unitaires de plus.
      Chiffres : donnees.md ; arbitrages : decisions.md (bis à quinquies).
- [x] ⏸ **POINT DE CONTRÔLE 1 — validé le 2026-08-02**, avec deux arbitrages :
      1. **Barla hors périmètre** du volume, sans sortir du registre ni des totaux nationaux.
         Un cinquième statut, « hors périmètre », avec motif publié ; ce n'est **pas** un faux
         positif. Le volume publie donc **102 artistes** et **6 081 notices distinctes**
         (24,8 % du doute national, 32 % hors monoculture).
      2. **L'interface dit « artistes »**, plus « maîtres » — sauf pour décrire la relation
         d'une œuvre à un artiste (atelier, école, entourage). L'effectif sort des titres et
         se lit dans les données.
- [x] **Phase 2 — Filtrer les œuvres par musée** (2026-08-02, branche
      `feat/filtre-musee-oeuvres`). Liste native bornée aux musées qui conservent une œuvre
      concernée de l'artiste affiché, effectif à côté du nom, tri par valeur décroissante,
      reconstruite au changement d'artiste. **Deux filtres emboîtés** — le musée délimite, la
      mention découpe à l'intérieur — pour qu'aucune puce n'annonce un nombre qu'elle ne rend
      pas. Compteur, pagination et retour à la première page recalculés à chaque changement ;
      état vide avec « Tout afficher ». `musee_code` (Muséofile) ajouté à l'export des œuvres,
      avec l'invariant « œuvres par musée = points de la carte ». L'état du filtre vit dans la
      page, prêt pour la phase 3. Vérifié au navigateur, desktop et mobile 390 px.
- [x] **Phase 3 — Relier musées et œuvres** (2026-08-02). Tous les points de la carte se
      choisissent (souris, toucher, Entrée, Espace) et ouvrent un **panneau persistant** au
      flanc : nom, compte, formules, et l'action « Voir les N œuvres conservées dans ce musée »
      — jamais dans l'infobulle, qui s'efface. L'action ouvre « Œuvres » avec le musée filtré,
      artiste conservé. Accord au singulier prévu. **Le lien POP du musée à une seule notice
      est conservé**, déplacé du point vers le panneau. L'action figure aussi dans la mention
      hors cadre. Un seul état filtre (`museeActif`, dans la page) ; le point choisi est une
      sélection de lecture. Trajet inverse vérifié au navigateur, desktop et mobile 390 px.
      **Correction du même jour** : la règle « pas de carte en dessous de deux musées »
      (2026-07-12) est supprimée — **tous les artistes ont leur carte**, y compris les 32 qui
      n'ont qu'un musée. La carte est un repère géographique, pas un graphique de répartition
      (decisions.md, octies).
- [x] **Phase 4 — Construire la page Présentation** (2026-08-02, route `/presentation`).
      Six temps : la notice réelle et ses mots exacts (Rembrandt, atelier, au Louvre — choix
      déclaré, champs relus dans l'export et contrôlés) · du cas au volume · les chiffres
      essentiels · **le texte de la sélection réécrit en trois blocs** (seuil · vérification
      avec des cas réels · ce que la liste ne dit pas) · la visualisation **« Les mentions les
      plus fréquentes »** · l'entrée dans l'exploration. **Pas de scrollytelling.** Reprise
      sélective du prototype ; la ventilation par artiste et le comptage national par mention
      ont quitté l'export avec les vues abandonnées. Invariants devenus relationnels, plus
      aucun effectif figé. 290 tests au vert, desktop et mobile 390 px vérifiés.
      **Reste à faire en phase 7** : mettre la page dans la navigation.
- [x] **Phase 5 — Alléger « Explorer les artistes »** (2026-08-02). Introduction de deux
      paragraphes retirée : elle réexpliquait ce que la Présentation dit désormais. Restent le
      titre, le renvoi discret « Comment ces artistes ont-ils été sélectionnés ? » (vers
      `/presentation`, plus vers la Méthode) et la sélection. Le répertoire commence à 249 px
      du haut : l'outil entier tient sans défiler. La ligne de prudence part sans rien perdre
      — le pied de page du site la porte déjà sur toutes les pages. L'effectif d'artistes
      quitte cette page, il se lit sur la Présentation. Desktop et mobile 390 px vérifiés.
- [ ] **Phase 6 — Adapter l'accueil** : affiche conservée, titre du volume, quelques chiffres
      dynamiques, deux accès (Présentation, Explorer).
- [ ] **Phase 7 — Finaliser la navigation** : Accueil · Présentation · Explorer les artistes ·
      Méthode. « Comprendre les mentions » quitte la navigation, son URL est redirigée.
- [ ] ⏸ **POINT DE CONTRÔLE 2** — captures desktop et mobile des six écrans, fil éditorial,
      chiffres publics, limites restantes. Avant fusion.
      **Y reprendre le REGISTRE DES CORRECTIONS ci-dessous, point par point.**
### ✎ REGISTRE DES CORRECTIONS — à traiter avant la fusion

Ouvert le 2026-08-02 à la demande de l'utilisateur. Tout ce qui est repéré en chemin et
volontairement remis à plus tard s'inscrit ICI, et **rien n'en sort sans avoir été traité**.
Le registre est relu au point de contrôle 2, et les corrections sont portées en phase 8.

- [ ] **C1 — Les textes publiés doivent être retravaillés.** Toute la copie écrite pendant les
      phases 0 à 7 est une PREMIÈRE ÉCRITURE : titres, chapôs, phrases de lecture des
      graphiques, intitulés, textes de la page Présentation, notes d'unité. Elle est juste sur
      le fond et vérifiée sur les chiffres, mais elle n'a pas été retravaillée. Prévoir une
      passe éditoriale complète, page par page, avant publication — registre journalistique
      sobre (CLAUDE.md), phrases courtes, aucune formule creuse, et surtout la relecture à voix
      haute qui n'a pas eu lieu.
- [ ] **C2 — Chercher les règles héritées qui décrivent mal ce qu'on regarde.** Une a été
      trouvée et corrigée le 2026-08-02 : « pas de carte en dessous de deux musées », qui
      traitait un repère géographique comme un graphique de répartition. Le défaut n'était pas
      dans le seuil mais dans la description. En chercher d'autres du même ordre.
- [ ] **C3 — Le titre du volume et le mot « artistes ».** L'interface dit « Explorer les
      artistes » ; le volume s'intitule « Autour des maîtres ». Ici « maître » se lit dans son
      sens relationnel (les œuvres autour du maître), ce qui reste conforme à la règle du
      2026-08-02 — mais la cohabitation mérite un arbitrage.
- [ ] **C4 — Les 39 artistes du lot 2 n'ont pas de texte éditorial.** `editorial-maitres.js`
      couvre les 63 premiers ; les autres affichent l'en-tête générique, sans ligne de
      repérage sous le nom. À écrire, ou à assumer explicitement.

---

- [ ] **Phase 8 — Vérification et publication** : chiffres, combinaisons de filtres, liens,
      images et crédits, mobile, clavier, tests, build, routes et redirections, docs à jour,
      **registre des corrections soldé**, fusion des seules branches validées.

---

## ★★ CHANTIER PRIORITAIRE (2026-07-21) — fiabilisation des maîtres

**Rien ne repart côté éditorial ou graphique avant les étapes 1 à 3.** L'audit du
2026-07-21 (constats : donnees.md ; décisions : decisions.md 2026-07-21 quater) a établi
que le pipeline des maîtres compte des **segments d'auteur** là où l'interface promet des
**notices**, et qu'il rattache **40 références au mauvais artiste**. Le dénominateur affiché
sous chaque fiche est plus atteint encore que le numérateur.

Ordre imposé — chaque ⏸ est un point d'arrêt :

- [x] **1. Unité de comptage** : comptage par couple `maître + Reference` dans
      `src/build_artistes.py`. **Fait le 2026-07-21** (decisions.md, quinquies) : doute des
      27 **2 341 → 2 225**, invariants vérifiés, exports non régénérés. Références uniques
      dans le CSV (1 023 705 / 1 023 705), donc déduplication intra-ligne. Arbitrage des
      familles multiples tranché — **option (c), le « ? » l'emporte** : une référence = une
      famille, familles et niveaux restent additifs
- [x] **2. Identité** : table déclarative d'alias et d'exclusions (homonymes attestés),
      couvrant les mentions **prudentes ET certaines**. **Fait le 2026-07-21**
      (decisions.md, sexies) : inventaire des 246 formes captées → 141 retenues ; un seul
      mécanisme ajouté, l'**ancre `^`** (le nom doit être en tête, Joconde écrit « NOM
      Prénom ») ; doute **2 341 → 2 188**, certaines **29 995 → 28 240**. Michel-Ange passe
      de 19 % à 39 % et de 9 musées à 3. Liste publiable des personnes écartées :
      donnees.md
- [x] **3. Tests de non-régression** sur références réelles. **Fait le 2026-07-21**
      (decisions.md, septies) : `tests/test_artistes.py`, 89 tests (total projet 60 → 149) ;
      `resout_reference()` extraite pour être testable sans le CSV ; témoins réels versionnés
      dans `data/exports/temoins_maitres.csv` (42 lignes, champ `Auteur` exact)
- [x] ⏸ **Validation du pipeline corrigé** avant régénération — feu vert du 2026-07-21
- [x] **4. Recalcul au seuil de 10** références prudentes uniques, tous candidats confondus.
      **Fait le 2026-07-21** (decisions.md, octies) : `src/candidats_maitres.py` →
      `data/exports/candidats_maitres.csv` (versionné). 4 834 formes portent une mention
      prudente, **330 atteignent 10** (34 dans les 27, **296 hors liste**). Le seuil
      s'applique au **maître désambiguïsé**, pas à la forme (le Titien : 11 réf., mais
      10 et 9 selon la graphie). Dispersion : 139 candidats dans un seul musée
      (10 334 notices, dont 5 791 Barla) vs 157 dans plusieurs (3 474) — **trie
      l'instruction, ne sélectionne pas** (Le Parmesan, Perino del Vaga, Menzel, Bandinelli
      sont dans un seul musée)
- [x] **5. Nouvelle sélection** selon la règle double. **Fait le 2026-07-22** (decisions.md,
      2026-07-22) — cadrage arbitré : **publication progressive sur registre exhaustif**.
      Les non-instruits sont « à instruire », **jamais « écartés »**. 36 candidats instruits
      un par un (identité claire, ≥ 10 réf. **après regroupement des alias**, parents et
      homonymes séparés nommément) → **63 maîtres retenus, 3 674 références prudentes**.
      Registre par personne : `data/exports/maitres_instruits.csv`. Registre exhaustif à
      4 états : `data/exports/candidats_maitres.csv` (74 formes retenues, 22 écartées,
      234 à instruire)
- [x] ⏸ **Validation de la nouvelle liste** (son ampleur décide de la suite) — feu vert
      du 2026-07-22
- [x] **6. Régénération des exports** : `artistes.json`, puis `vue_ensemble.json` (dérivé).
      **Fait le 2026-07-22** (decisions.md, bis) : 63 maîtres, invariants + seuil vérifiés à
      la génération. La liste pèse **3 674 notices prudentes sur 24 507, soit 15,0 %** du
      doute national (contre 9,6 %). Clés `dans_27`/`hors_27` → **`dans_liste`/`hors_liste`**
      (plus une seule occurrence de « 27 » dans le JSON généré). Correction d'une erreur de
      mesure du temps 5 : `musees_presence` ≠ `musees_doute`. À surveiller :
      `artistes.json` double, 189 → **372 Ko**
- [x] **Vérification du recouvrement entre profils** (demandée avant le temps 7,
      **faite le 2026-07-22**, decisions.md ter) : 6 notices nomment deux maîtres retenus
      (300 sur les attributions certaines). L'export distingue désormais **appartenances**
      (somme des fiches) et **notices** (références distinctes) ; `hors_liste` se calcule
      sur l'union — 20 833 → **20 839**. Invariants + 5 tests sur l'export publié.
      Conclusion fautive corrigée : « attribué à » **reste** la formule la plus fréquente
      chez les maîtres retenus (43 % contre 35 %) ; ce qui change, c'est la part d'« école
      de », 35 % contre 7,6 % au national
- [x] **7. Contrôle des effets sur le front**. **Fait le 2026-07-22** (decisions.md, quater) :
      l'axe du nuage passe du **nombre à la part** (0–100 %, échelle commune conservée) — à
      63 maîtres allant de 11 à 310 notices, la moitié des profils étaient illisibles ;
      **3 en-têtes rédigés disaient l'inverse de leurs chiffres** (Le Primatice, Raphaël,
      Michel-Ange) et les **21** qui nommaient une mention à côté d'un rang sont convertis ;
      **36 lignes de repérage** écrites (dates relevées dans la base puis croisées) ;
      seuil « vingt notices » → « dix », effectifs et libellés « 27 » rendus dynamiques,
      `nb_maitres` publié dans `vue_ensemble.json` ; les deux panneaux de « Comprendre les
      mentions » comptent désormais des **notices** (3 668), plus des appartenances.
      Restent hors périmètre : style. **Portraits faits le 2026-07-22** (60/63) ;
      **angles écrits des 36 faits le 2026-07-22**, avec un **pont de nom** dans l'en-tête
      pour les 14 maîtres connus sous un surnom — « Michel-Ange (Michelangelo Buonarroti) »,
      les notices gardant le verbatim Joconde
- [x] **8. Révision des textes publics** annonçant « 27 » ou « au moins vingt notices ».
      **Fait le 2026-07-22** (decisions.md, quinquies) : `charte-graphique.md` (le titre
      public ne fige plus d'effectif), `dataviz-les-presque.md` (sélection, effectif, et
      **note sur le changement d'axe**), `architecture-editoriale.md`, `les-presque/+page.js`,
      et les tâches ouvertes de ce fichier. La page **Méthode publie désormais l'état du
      registre** (330 formes recensées : 74 retenues, 22 écartées, 234 encore à examiner —
      libellé corrigé le 2026-07-31, « examinées » laissait croire l'inverse), explique
      les **homonymes** et dit qu'une œuvre peut concerner deux artistes sans compter deux
      fois. Nouveau petit export `data/exports/web/registre.json`. Les journaux datés
      (donnees.md, decisions.md, entrées de phases) ne sont **pas** réécrits : ce sont des
      mesures datées, pas des descriptions de l'état courant
- [x] **Arbitrage ouvert** : représentation par famille d'une référence portant deux
      formulations prudentes (3 cas, Simon Vouet) — **tranché le 2026-07-21, option (c)** :
      le « ? » l'emporte sur la formule de distance. Vouet `atelier_de` 10 → 7,
      `point_interrogation` inchangé à 4. Doctrine valable pour les cas à venir ; le fil
      « politique “?” vs formule de distance » reste ouvert côté éditorial

> Le total national de **24 507** notices prudentes n'est **pas** touché : il est produit
> ligne à ligne, sans identification de maître (vérifié dans `build_exports.py` et
> `count_markers.py`).

---

## Images des œuvres — droits et reproductions ouvertes (2026-07-29)

Objectif : afficher une reproduction quand la réutilisation est explicitement permise. Recherche
et préparation SEULEMENT (front non touché, aucune image téléchargée à ce stade).

- [x] **Audit POP** (Palier 1 « vignettes ») — champ « Crédits photographiques » (`PHOT`) des
      3 668 notices, classé en 5 statuts (`src/images_classify.py`, testé). **0 `open`** :
      2 578 `restricted` (RMN « utilisation soumise à autorisation »), 792 `unknown` (crédits
      nominatifs), 298 `unavailable`. Livrables `images_oeuvres.{csv,json}`, `images_bilan.json`.
- [ ] **Levier A — autorisations individuelles** (792 `unknown`, surtout musées municipaux) :
      **différé** (travail de contact hors code), documenté, mobilisable plus tard.
- [x] **Reproductions ouvertes Wikimedia Commons / Wikidata** — appariement strict :
      P347 (identifiant Joconde) → **exact** ; inventaire + institution → **candidat** ;
      inventaire seul / autre institution → **rejeté**. Droits lus via l'API Commons. Modules
      `src/commons_match.py` (testé) + `src/build_commons.py` (cache résumable). **329 exacts,
      dont 184 images ouvertes réutilisables** ; 152 candidats sur 47 réf. ; 352 faux
      rapprochements écartés. Livrables `commons_correspondances.{json,csv}`, `commons_bilan.json`.
- [x] **Intégration des 184 reproductions ouvertes** (2026-07-29) — `src/build_vignettes.py`
      télécharge une miniature Commons, ré-encode en JPEG optimisé (Pillow, ≤ 900 px), une copie
      locale par référence dans `data/exports/web/oeuvres_img/` (sync → `web/static/oeuvres/`).
      Index `images_index.json` fusionné dans les fiches (`build_artistes.py` le rattache aussi).
      `OeuvresMaitre.svelte` : image locale lazy à la place du placeholder, cliquable vers la page
      Commons, légende licence + source en petit corps (auteur seulement pour CC BY/BY-SA).
      Déclaré dans la page méthode. Build + tests (214) OK, vérifié desktop + mobile.
- [x] **Vérification des candidats inventaire** (2026-07-29) — recoupement par dimensions
      Wikidata (P2048/P2049) : dimensions incompatibles → rejet (262 collisions écartées, dont
      162 imagées, à ne surtout pas afficher). Dimensions concordantes → **jamais** de promotion
      auto (faux positifs constatés : « L'Ange gardien » 102×81 ↔ « Nu féminin » 102×82). Reste
      47 candidats sur 25 réf., **aucun à forte présomption** → l'inventaire n'ajoute aucune
      image fiable ; P347 reste la seule source sûre, total réutilisable **inchangé à 184**.
      Tests + bilan `commons_bilan.json` à jour. `commons_match.py` (parser/comparaison
      dimensions, testés).
- Réserve : les autres statuts (145 exacts sans image, 47 candidats inventaire faibles, 792
  `unknown` POP / Levier A) restent hors affichage — matière pour un prochain lot si on le décide.

---

## Onglet « Œuvres » — liste complète, filtres, pagination (2026-07-28)

L'onglet passe de « quelques exemples » à la **totalité des œuvres concernées** par maître
(decisions.md, journal.md, 2026-07-28).

- [x] **Phase 1 — export complet.** Un fichier `data/exports/web/oeuvres/<slug>.json` par
      maître (63 fichiers, 3 674 œuvres au total), écrit par `build_artistes.py` dans la même
      passe que l'export léger, depuis `resout_reference()` et la famille déjà retenue. `slug`
      ajouté à `artistes.json` ; anciens `exemples` retirés. Invariants à l'écriture : nombre
      d'entrées = `doute`, ventilation = `familles`, pas de doublon, référence présente, aucune
      copie. `sync-data.js` rendu récursif (dossier `oeuvres/`).
- [x] **Phase 2 — interface.** `OeuvresMaitre.svelte` réécrit : chargement à la demande du
      seul fichier de l'artiste affiché (jeton anti-course), filtres en puces (« Toutes » +
      mentions présentes avec effectif), pagination 8/page compacte (`pagination.js`, testée),
      états chargement/erreur/vide, recentrage doux au changement de page, accessibilité
      clavier/`aria-pressed`/`aria-current`. Structure éditoriale (verbatim-matière,
      emplacement média réservé) et bloc « À part » des copies conservés.
- Réserve : unification du wording « notices » du bloc copie (hors périmètre).

---

## ★ RECENTRAGE (2026-07-15) — cap actuel

**Décision.** La **V1 publique** de *L'inventaire du doute* sera centrée sur le
**dossier « Les presque »** : les œuvres que les musées rapprochent d'un grand
maître sans les lui attribuer (« attribué à », « atelier de », « école de »,
« manière de »…). Les autres rubriques et formes de doute — notamment
**« Avant / après »** — **restent documentées et conservées dans le projet**,
mais **ne font plus partie du périmètre publiable initial**. Détail et motifs :
docs/decisions.md 2026-07-15 (ter). *Le journal des phases ci-dessous est conservé
comme historique ; ce bloc est le cap qui prime.*

### 1. Périmètre V1 publique (à construire / finir)

> Organisé en 4 entrées de nav par `docs/architecture-editoriale.md` (2026-07-16,
> ⏸ à valider) : **Accueil** · **Explorer les maîtres** (= exploration de la liste) ·
> **Comprendre les mentions** (= vocabulaire + Vue d'ensemble) · **Méthode**. Les
> items ci-dessous restent la liste des briques ; l'architecture dit comment elles
> se regroupent et se hiérarchisent.

- [x] **Accueil / introduction** (2026-07-17 quater) — refondu en **couverture
      éditoriale** (architecture §3) : deux zones (promesse + figure de données
      provisoire), chiffre 24 507 en preuve secondaire, renvoi Méthode
- [x] **Vue d'ensemble des formulations prudentes** (2026-07-17 ter) — intégrée à
      « Comprendre les mentions » : deux panneaux de **barres** à échelle commune
      (Ensemble 24 507 vs 27 noms 2 341), `BarresMentions.svelte`, contraste
      « attribué à » global vs école/atelier/manière dans les 27
- [x] **Exploration des 27 noms** (rubrique interactive : graphique / œuvres /
      carte par maître) — en place, à intégrer à la charte
- [x] **Vocabulaire / clé de lecture des familles** (2026-07-17 ter) — page autonome
      « Comprendre les mentions » (route `/echelle`) : trois territoires + huit
      mentions définies + vue d'ensemble ; réutilise `territoires.js` et
      `familles-public.js`
- [x] **Méthode et limites** (2026-07-17 quater) — page dédiée `/methode`, 5 sections
      (Périmètre · Construction des données · Lire les chiffres · Limites · Sources et
      droits) ; chiffres lus depuis les exports ; divergence copies corrigée (22 624)
      **Refondue le 2026-07-31** (branche `refonte/methode`, decisions.md du jour) :
      **six questions** au lieu de cinq rubriques (la base · comment le doute s'écrit ·
      comment on compte · identifier les artistes · lire les chiffres · limites, sources
      et droits), contradictions factuelles corrigées, **références officielles** citées
      (data.gouv, méthode Joconde, décret 81-255, POP, Commons, france-geojson),
      **quatre visuels** sur des cas réels, sommaire qui suit la lecture + retour en
      haut, provenance **mesurée** au lieu d'être recopiée
- [ ] **Travail image / droits** (statuts open/authorized/pending/restricted ;
      voie Wikimedia fichier par fichier, comme les portraits)
- [~] **Charte graphique et refonte front** (identité visuelle propre — le socle
      sur lequel tout le reste s'aligne) : **direction arrêtée le 2026-07-16**
      (`docs/charte-graphique.md`, ambiance « Catalogue savant »).
      - [x] Palier 1 — **base typographique globale** (polices locales sans CDN,
            tokens manquants, typo appliquée globalement) — 2026-07-16 (bis)
      - [x] Palier 2 — **coquille « inventaire »** (header, nav en petites
            capitales + page active, structure aux tokens ; italique Spectral
            intégrée) — 2026-07-16 (ter)
      - [ ] **Chantier — Direction artistique & architecture éditoriale** (cadrage
            de plus haut niveau, INSÉRÉ avant le kit ; note de direction du
            2026-07-16, `docs/architecture-editoriale.md`) : repenser l'appli comme
            une **publication** centrée sur « Les presque », pas une suite de blocs.
            Quatre axes : (1) nav publique recentrée à 4 entrées actives — Accueil ·
            Explorer les maîtres · Comprendre les mentions · Méthode (réserve hors
            nav ; « Vue d'ensemble » dans « Comprendre les mentions ») ; (2) accueil
            = **couverture éditoriale** (promesse d'abord, chiffre ensuite,
            illustration Joconde en **figure de données**) ; (3) séparer
            **répertoire ↔ profil** dans « Explorer les maîtres » ; (4) **distance à
            la main du maître** = principe visuel central (3 territoires). ⏸ **à
            valider avant le palier 3.**
      - [~] Palier 3 — kit de composants unifié (cartes, onglets, légende, barres ;
            nombres en Public Sans tabulaire ; micro-légendes en italique Spectral)
            — **au service de l'architecture éditoriale ci-dessus**
            - [x] **Prototype** (2026-07-16 quinquies, ⏸ à valider) — `BandeauMaitre`
                  + `ChiffreVedette` + onglets Profil / Œuvres / Musées sur la fiche
                  maître réelle. Ouverts : synthèse calculée (factuelle) + plafond
                  `fractionEnMots` (decisions.md même date).
            - [x] **Zone Répertoire** (2026-07-17) — `Repertoire.svelte` : recherche,
                  tri Œuvres/A→Z, microprofils, sélection active à filet d'accent,
                  repliable en mobile ; légende détaillée retirée (→ « Comprendre les
                  mentions »).
            - [x] **Zone TroisTerritoires** (2026-07-17 bis) — `territoires.js`
                  (primitive) + nuage recadré (bandes de fond, séparateurs, titres) +
                  clé de lecture rétablie. Données/points/couleurs/tooltips inchangés.
            - [x] **Zone « Comprendre les mentions »** (2026-07-17 ter) — page
                  autonome (route `/echelle`, libellé public provisoire), 4 parties,
                  `BarresMentions.svelte` ; réutilise `territoires.js` +
                  `familles-public.js`.
            - [x] **Zone Accueil-couverture** (2026-07-17 quater) — deux zones,
                  figure de données provisoire, chiffre en preuve secondaire.
            - [x] **Zone Méthode** (2026-07-17 quater) — page `/methode`, 5 sections.
            - [x] **Recentrage complet de la nav** (2026-07-17 quater) — 4 entrées
                  actives (Accueil · Explorer les maîtres · Comprendre les mentions ·
                  Méthode) ; Révisions/Carte retirées de la nav publique (code conservé).

  **Socle V1 bouclé.** Revue globale de direction artistique menée (planche de
  l'existant + diagnostic + 3 directions maquettées). **Direction retenue :
  B « la ligne de proximité »** (decisions.md 2026-07-17 quinquies).

- [~] **Refonte Direction B — par pages complètes** (pas par microcomposants) :
      - [x] **Coquille + tokens** (2026-07-17 quinquies) — token `--spectre`, composant
            `Spectre.svelte`, signature en tête de page, canevas élargi (68 rem),
            filet brun de tête remplacé par la ligne.
      - [x] **Accueil** (2026-07-17 quinquies) — couverture à la ligne : spectre à
            territoires, grand titre, CTA encre, figure de données à 8 stations,
            chiffre en preuve secondaire.
      - [x] **Explorer / Profil** (2026-07-17 sexies) — en-tête compact, profil au 1er
            écran, graphe élargi, onglets soulignés, folio discret.
      - [x] **Explorer / Œuvres** (2026-07-17 sexies) — liste éditoriale continue,
            verbatim en matière, emplacements média réservés.
      - [x] **Explorer / Musées** (2026-07-17 sexies) — grande carte + flanc.
      - [x] **Comprendre les mentions** (2026-07-17 sexies) — ligne une fois, 3 colonnes.
      - [x] **Méthode** (2026-07-17 sexies) — sommaire en rail collant + colonne.
      - Emprunt de la dir. C effectivement utilisé : verbatims-matière (Œuvres). Non
        retenus à ce stade : portrait N&B, capitales/folios dominants.

  **Direction B menée à terme = modèle de travail (NON validée).** Rendu jugé trop
  classique/générique. Remplacée par la direction « affiche » (ci-dessous).

### ★ DIRECTION « AFFICHE » (2026-07-18) — cap actuel

Accueil validé comme **affiche interactive pleine page** (image, titre + accroche 3
étages, nav en cartouches). On **étend cette direction au reste de l'application**.
Principe : la couverture reste l'affiche ; les pages intérieures gardent une **surface
de lecture claire** mais adoptent le **langage de l'affiche** (cadre navy + cartouches
ivoire/cobalt, accents vermillon, **composition pleine largeur en zones**, fin de la
colonne centrale). Les **8 pigments de données restent inchangés**. L'accueil ne posant
plus le sujet ni les chiffres, **chaque page porte désormais son entrée narrative**.

- [x] **C1 · Charte v2 + coquille** (2026-07-18) — tokens de cadre (navy/ivoire/cobalt/
      vermillon), header/footer des pages intérieures en bandeau navy, spectre de tête
      retiré. Surface de contenu claire conservée (refonte en C2-C4).
- [x] **C2 · Explorer les maîtres — pleine page** (2026-07-18) — `/les-presque` en
      `main.pleine` avec gouttières ; entrée narrative courte revue ; scène du maître
      renforcée (portrait 16 rem, nom en xxl) ; graphe étalé ; accents cobalt/vermillon
      (kicker, onglet actif, sélection du répertoire) ; données/tooltips inchangés.
- [x] **C3 · Comprendre les mentions — pleine page** (2026-07-18) — `main.pleine` +
      gouttières ; kicker cobalt + titre « Le langage de la prudence » + chapô resserré ;
      prudence en filet vermillon ; ligne des territoires et grilles (mentions,
      comparaison) étalées ; barres/données/réserves inchangées.
- [x] **C4 · Méthode — pleine page sobre** (2026-07-18) — `main.pleine` + gouttières ;
      kicker cobalt + titre « Ce que les chiffres disent, et ne disent pas » ; prudence
      vermillon ; sommaire en rail collant (accent cobalt) + contenu **validé conservé**.
- [x] **C5 · Passe narration + nettoyage** (2026-07-18) — entrées homogènes sur les 4
      pages (kicker + titre éditorial + chapô court + précaution vermillon) ; accents
      chrome restants alignés sur le cobalt (chiffres vedettes, liens POP, onglets, tri
      et sélection du répertoire). `--couleur-accent` (brun) ne subsiste que dans la
      rubrique en réserve `/revisions` et comme couleur du point de carte (donnée).

**Direction « affiche » étendue à toute l'application (C1-C5 faits, 2026-07-18).**

- [x] **Refonte narration « Les presque »** (2026-07-18) — d'abord deux états (guide /
      maître, 2026-07-18 ter), puis **retour à un maître d'ouverture** (quater) : la page
      est un espace d'exploration dès l'arrivée (Le Brun sélectionné), entrée éditoriale
      unique et courte, **graphe borné (42 rem) + scène héros conservés** (les proportions
      étaient le vrai correctif). Guide abandonné. Détail : decisions.md 2026-07-18 (quater).
- [x] **Titre + intro « Explorer les 27 maîtres »** (2026-07-19) — appellation publique
      « Les presque » **abandonnée** (H1 = « Explorer les 27 maîtres » ; route/fichiers/
      exports inchangés) ; **nouveau texte d'intro** (3 §, seuil expliqué, prudence en
      note) ; **intro ↔ outil séparés en deux temps** (entrée éditoriale 2 colonnes sans
      encadré → « Choisir un artiste », filet + espace). Répertoire/profils/onglets/notices/
      viz **non touchés** (phase distincte). Détail : decisions.md 2026-07-19.
- [x] **Fiche artiste — hiérarchie des informations** (2026-07-19 bis) — `doute` en valeur
      principale (« 310 notices… »), dénominateur `propre + doute` (« 9 % … périmètre
      étudié »), répartition `nb_musees_doute` (19, plus le 64 général), formulation
      dominante générée (accords + égalités via `ORDRE_FAMILLES`, `fractionEnMots`
      abandonnée). Répertoire : tri « Notices » + micro-légende. Méthode : total de
      référence expliqué. Pipeline inchangé. Détail : decisions.md 2026-07-19 (bis).
- [x] **Fiche artiste — portrait éditorial (fin des compteurs)** (2026-07-20) — la scène
      devient un court texte fondé sur les données : nom → **mention la plus fréquente**
      (constat, 2e niveau visuel) → récit chiffré → repère méthodologique discret ; nombres
      **dans** les phrases (graisse + cobalt + elzéviriens). Prototype Le Brun validé puis
      **généralisé aux 27** (égalités, cas 100 %, musée unique, bios conservées). Nouveau
      champ `citation` dans `familles-public.js` ; graphique et tooltips **inchangés**.
      Vocabulaire : narratif en « œuvres associées à son nom », comptages en « notices ».
      Détail : decisions.md 2026-07-20.
  - [ ] **Reliquat à trancher** : le répertoire affiche « NOTICES CONCERNÉES » à côté d'un
        bandeau qui dit « 310 œuvres » — passe de cohérence dédiée (hors périmètre du jour).
  - [x] **Wording des comptages — « notices » partout** (2026-07-19 ter) — helper
        `notices()` (ex-`oeuvres()`) ; tooltips, vitrine (copies), carte (titre, légende,
        replis), `/echelle` (panneaux + texte + purge du reliquat « Les presque »),
        Méthode (seuil « vingt notices »). « œuvre » réservé aux objets montrés
        individuellement. Détail : decisions.md 2026-07-19 (ter).

### 2. En réserve (conservé, hors V1 publique)
- [~] **Avant / après** (`/revisions`) — construit (onglets, anneau, prototype
      cartes), **hors nav publique** (`prete: false`) ; reprise possible telle quelle
- [~] **Carte générale** qualifiée (concentration déjà connue, biais de couverture)
- [~] **Autres stats Joconde** (domaines, périodes, top musées — voir donnees.md)
- [~] **Autres formes de doute** (anonymes, copies en propre, géographie…)

### 3. Déjà fait (acquis, réutilisables en V1)
- [x] **Pipeline des 27 noms** (`build_artistes.py` → `artistes.json`, comptage
      canonique aligné sur `markers.py`, désambiguïsation)
- [x] **Graphique / œuvres / carte par maître** (nuage à grille fixe, vitrine
      « Œuvres », carte d3-geo par musée détenteur)
- [x] **Légende permanente** des mentions (couche `familles-public.js`)
- [x] **Tooltips** harmonisés (`Infobulle.svelte`, source unique de libellés)
- [x] **Export `vue_ensemble.json`** (familles global/dans‑27/hors‑27, niveaux
      global vs 27 + hors monoculture, copies à part ; `build_vue_ensemble.py`)
- [x] **Audit « Avant / après »** (pipeline, taxonomie v2, tests, front) —
      **conservé mais hors V1**

---

## Phase 0 — Initialisation ✅

- [x] Arborescence (docs/, src/, data/), .gitignore
- [x] CLAUDE.md (contexte, règles non négociables, méthode)
- [x] docs/ amorcés : journal, décisions, données, méthode-et-limites
- [x] Environnement uv + pyproject.toml, git init + premier commit
- [x] ⏸ Validation utilisateur — **validée le 2026-07-03**
  (seuils T5 confirmés, titre « L'inventaire du doute » adopté)

## Phase 1 — Test go/no-go sur la qualité des données

### T1 — Nomenclature et téléchargement ✅
- [x] Télécharger la nomenclature ODS et le CSV complet (src/download.py)
- [x] Lire la nomenclature : tableau des champs (nom CSV ↔ nom API ↔ définition)
      dans docs/donnees.md
- [x] Confirmer les champs liés à l'auteur et aux anciennes attributions
- [x] ⏸ Validation : synthèse des champs — **validée le 2026-07-03**
      (+ consigne T3 : distinguer « école de [artiste] » dans Auteur du champ
      Ecole_pays qui indique une nationalité)

### T2 — Profilage du CSV complet ✅ (en attente de validation)
- [x] Nombre réel de lignes, écart chiffré avec l'extrait API
      (1 023 705 notices ; l'API n'en expose que 70,5 %)
- [x] Taux de remplissage des champs auteur / école / ancienne attribution
- [x] Répartition par domaine (périmètre pressenti : 583 346 notices, 57 %)
- [x] ⏸ Validation : **validée le 2026-07-03** — choix du périmètre reporté à la
      fin de T3 ; consigne : taux à deux dénominateurs (toutes notices /
      notices avec Auteur non vide)

### T3 — Détecteur v0 + taux de base ✅ (en attente de validation)
- [x] src/markers.py : lexique versionné, 13 familles, 3 catégories
      (doute / copie / révision), graphies multiples, pièges intégrés
- [x] « d'après » classé à part (copie) ; « présumé » marqué suspect
- [x] Application par chunks ; champ Ancienne_attribution traité par présence
      (pas de fouille texte, pour ne pas gonfler « attribué à »)
- [x] Taux à deux dénominateurs : doute = 29 726 notices (2,90 % base /
      3,53 % avec auteur) → data/exports/comptages.csv + comptages_domaines.csv
- [x] ⏸ Validation : **validée le 2026-07-03** — taux vedette = notices avec
      auteur (base entière toujours en second) ; comptage de référence sur
      toute la base, beaux-arts en angle éditorial

### T4 — Échantillon de vérification ✅
- [x] 206 notices stratifiées par famille (rares sur-représentées, « présumé »
      et « anciennement attribué » pris en entier), graine 42
- [x] Export CSV tableur (data/exports/echantillon_verification.csv) :
      famille, champ source, extrait, contexte, lien POP testé,
      colonnes vides verdict / commentaire
- [x] Mode d'emploi : docs/verification-echantillon.md
- [x] ⏸ Validation : vérification manuelle **rendue le 2026-07-04** — 206/206
      verdicts (176 vrai / 28 faux / 2 incertain), 45 commentaires ; zéros de
      tête des références restaurés après passage par Google Sheets

### T5 — Bilan go/no-go ✅ (en attente de la décision de phase)
- [x] Réimport du CSV annoté (206/206), taux par famille et global pondéré
      (src/evaluate_sample.py → data/exports/bilan_faux_positifs.csv)
- [x] Liste des pièges confirmés (8 classes, docs/donnees.md)
- [x] Recommandation argumentée dans docs/decisions.md :
      doute 17,0 % pondéré → **REFORMULATION ciblée** (atelier de 64 %,
      école de 20 %, ? 16 % — causes identifiées et corrigeables) ;
      copie 0 %, révision 0 %
- [x] ⏸ Validation : **décision du 2026-07-04 — cycle de reformulation lancé**
      (recommandation suivie, approche « atelier » validée explicitement)

### Cycle v1 — Reformulation ciblée (T3bis/T4bis)
- [x] Lexique v1 : atelier lu comme convention (qualificatif vs nom d'auteur),
      écoles nationales inversées exclues, `(?-1996)` exclu,
      doctrine « (attribué, d'après) » implémentée
- [x] Verdicts humains T4 figés en tests automatiques
      (tests/test_markers.py, 25 cas, `uv run pytest`)
- [x] Recomptage : doute = 25 220 (2,46 % base / 2,99 % avec auteur) ;
      population « Atelier de X » écartée et chiffrée à part (1 123)
- [x] Mini-lot de contrôle : 65 lignes, familles reformulées + population
      écartée (data/exports/echantillon_recheck.csv, graine 202607)
- [x] ⏸ Vérification manuelle du mini-lot — **rendue le 2026-07-05** (65/65)
- [x] Bilan T5bis (src/evaluate_recheck.py) : doute pondéré **5,7 %
      conservateur / 3,3 % ajusté** → sous le seuil des 10 % ;
      exclusion « Atelier de X » confirmée 15/15 ; restes localisés
      (atelier 30 % famille, école 13 %) à traiter en phase 2 (typologie)
- [x] ⏸ Validation : **GO prononcé le 2026-07-05 — PHASE 1 CLOSE** ✅
      Classification des familles consignée dans docs/familles.md
      (document de référence pour la typologie et les visualisations)

## Phase 2 — Typologie et pipeline consolidé (EN COURS depuis le 2026-07-05)

### P2-T1 — Recouvrements entre catégories ✅
- [x] Venn doute / copie / révision chiffré + co-occurrences familles de doute
      → src/count_overlaps.py, data/exports/recouvrements.json
- [x] ⏸ Validation : **règles de non-addition validées le 2026-07-05**
      (chiffre vedette = doute seul ; union nommée ; Venn obligatoire ;
      doute + révision promu objet éditorial)

### P2-T2 — Typologie du doute ✅
- [x] Échelle à 3 niveaux proposée et argumentée (docs/typologie.md)
- [x] ⏸ Arbitrages rendus le 2026-07-05 : atelier restreint aux beaux-arts,
      écoles-lieux écartées (liste versionnée), « ? » au niveau 1
- [x] Lexique v2 implémenté + tests (35 cas) + recomptage complet :
      **doute = 24 507** (2,39 % base / 2,91 % avec auteur) ;
      Venn v2 : 66 420 touchées, doute + révision = 4 615

### P2-T3 — Pipeline d'exports pour la restitution ✅ (en attente de validation)
- [x] src/build_exports.py : CSV → 4 JSON légers dans data/exports/web/
      (provenance, niveaux, musees avec total versé + coords, territoires)
- [x] Provenance datée intégrée (version 2026-07-01, ETag)
- [x] Partition des niveaux vérifiée (20 014 + 3 537 + 956 = 24 507)
- [x] Deux découvertes remontées (docs/donnees.md) : monoculture Barla/Nice
      (23,6 % du doute), Alençon absent des données (109 notices, 0 doute)
- [x] ⏸ Validation : structure validée + **monoculture divulguée** (chiffre
      vedette 24 507 gardé, « hors cas Barla : 18 716 » intégré aux exports,
      drapeau musée, carte sur part_doute) — 2026-07-05

### P2-T4 — Cas racontables (EN COURS — découpé pour reprise si interruption)
Décision : Alençon = ouverture, incarnation de la limite (voir decisions.md).
Sortie visée : data/exports/web/cas.json + docs/cas.md (récit éditorial).
Sous-étapes (cocher au fil de l'eau, commit après chaque cas) :
- [x] P2-T4a — Liste des cas + schéma cas.json arrêtés (docs/cas.md)
- [x] P2-T4b — Cas « Alençon, l'absent » (via base régionale, non compté)
- [x] P2-T4c — Cas « Barla/Nice, le doute industriel » (monoculture, réel Joconde)
- [x] P2-T4d — Cas « Besançon, le vrai doute Géricault » (genre de + études Radeau)
- [x] P2-T4e — Cas « doute + révision » (l'objet le plus riche, P2-T1)
- [~] P2-T4f — cas par niveau : écarté (non nécessaire ; exemples puisables
      à la construction de l'interface)
- [x] P2-T4g — Assemblage cas.json + relecture docs/cas.md
- [x] ⏸ Validation : **4 cas validés le 2026-07-06 — PHASE 2 CLOSE** ✅

## Phase 3 — Restitution (EN COURS depuis le 2026-07-06)

Direction arrêtée (docs/decisions.md, 2026-07-06) : **application interactive
portée par la dataviz**, PAS de scrollytelling, Alençon non central. Plusieurs
dataviz d'égale importance, chacune une exploration différente. Front statique
consommant les JSON exportés (pas de serveur sauf besoin avéré). Page « méthode
et limites » au même rang que le reste.

### P3-T0 — Socle SvelteKit (fait une seule fois)

Stack arrêtée : **SvelteKit en build statique** (`adapter-static`), front isolé
dans un dossier dédié, consommant les JSON de `data/exports/web/` (décision du
2026-07-07, docs/decisions.md). Aucun serveur applicatif.

Sous-étapes (cocher au fil de l'eau) :
- [x] Échafaudage SvelteKit dans `web/` (adapter static câblé dans `vite.config.js`,
      `prerender` à la racine) ; `web/node_modules/` ignoré par git
- [x] Accès aux JSON : `npm run sync:data` (web/scripts/sync-data.js) copie
      `data/exports/web/*.json` → `web/static/data/` (servis en `/data/…`),
      dossier ignoré par git car généré (voir donnees.md)
- [x] Coquille partagée : `+layout.svelte` (en-tête, nav « une brique = une route »,
      briques à venir en placeholder), tokens de style dans `lib/styles/tokens.css`
      (couleurs des 3 niveaux)
- [x] « Hello data » : l'accueil pré-rend le chiffre vedette réel (24 507, hors
      monoculture 18 716) depuis `niveaux.json` — `npm run build` OK, HTML statique
      vérifié dans `web/build/`
- [x] ⏸ **Validation du socle le 2026-07-07** — validé sur le fond ; réserve
      indicative sur le style (« trop Claude normé », identité visuelle à
      retravailler après les dataviz, voir decisions.md + mémoire)

### P3-T1 — Entrée « par l'artiste » / « Les presque » (1re dataviz)

- [x] Liste vedette V1 : critère « maître de référence + ≥ 20 doutes (hors
      copie) », comptage canonique aligné sur markers.py (docs/decisions.md,
      2026-07-07)
- [x] Correction de repérage documentée (parenthèses vs champ entier ; écoles
      nationales ; granularité du nom-pivot) — docs/donnees.md, 2026-07-07
- [x] Désambiguïsation des familles (Fragonard = Jean-Honoré ; Bruegel/Cranach
      l'Ancien retirés car < 20 une fois le maître isolé) → **27 maîtres**
- [x] src/markers.py::famille_segment() + src/build_artistes.py →
      data/exports/web/artistes.json (par maître : propre/doute/copie,
      ventilation famille + niveau, musées, notices réelles POP)
- [x] ⏸ Réserve utilisateur : garder 27, ou réintégrer Bruegel/Cranach comme
      « famille » — **sans objet depuis le 2026-07-22** : le seuil est passé à 10 et la
      sélection se fait par instruction sur registre exhaustif (temps 5). Bruegel et Cranach
      sont dans le registre, à l'état « à instruire », comme les 232 autres
- [x] Front (route `/les-presque`) : fiche « presque » complète — échelle du
      doute (composant `BarreNiveaux`), tableau des formules, copie en bande à
      part, exemples avec liens POP ; liste des 27 maîtres filtrable. Build
      statique vérifié (build/les-presque.html, données réelles pré-rendues)
- [ ] Moteur de recherche sur **toute la base** (pas seulement les maîtres retenus) :
      dépend d'un export « tous les noms + comptages ». **Une partie existe désormais** :
      `data/exports/candidats_maitres.csv` recense les 330 formes au seuil de 10 avec leur
      état. Pour l'instant, le front filtre sur la liste retenue
- [~] Galaxie (`GalaxieMaitre.svelte`) construite puis **ABANDONNÉE dans cette vue**
      le 2026-07-08 (voir decisions.md) : encodage « 1 bulle = 1 famille » → schéma
      moléculaire, pas une constellation ; n'apporte rien qu'une barre ne montre
      mieux. Réserve : « vraie constellation » (1 point = 1 œuvre) à retenter un
      jour sur **branche séparée**, hors de cette vue
- [ ] Intro/onboarding du site à revoir au bilan : un visiteur lambda ne comprend
      pas encore l'objectif ni le fonctionnement (voir mémoire feedback)
- [x] Garde-fou éditorial en place : chapô « voici comment les musées nuancent
      autour d'un nom », copie isolée comme « copies assumées », aucun « trésor caché »

#### Réorientation « Les presque » — trois angles (décision 2026-07-08)

Cible : par maître, trois vues complémentaires — **le quoi / le combien / le où**.
Ordre de construction retenu : **barres → carte** (détail conservé tel quel).

- [x] **Détail** — *le quoi* (existant) : formules, exemples POP, copies à part.
      Conservé en l'état ; labels trop techniques à reformuler **plus tard** (non
      prioritaire). **Remplacé le 2026-07-11 par la vitrine « Œuvres »** (voir
      ①septies)
- [x] **① Barres horizontales** — livré puis **remplacé par un nuage de points**
      le 2026-07-08 : les barres, normalisées à la largeur du conteneur et
      n'affichant que les familles présentes, ne permettaient ni comparaison
      entre maîtres ni lecture des volumes réels
- [x] **①bis Nuage de points à grille fixe** — *le combien, comparable* : axe X =
      8 familles de doute (ordre canonique, « présumé » absent des 27 retiré),
      **mêmes colonnes pour tous** ; axe Y = volume, **plafond commun 240**
      (calculé côté front = max famille sur les 27, « école de » Le Brun) ;
      1 point/famille à la hauteur du volume, taille légèrement croissante
      (la hauteur porte la mesure), couleur par famille groupée par niveau,
      graduations 60/120/180/240, échelle linéaire, survol = compte exact.
      `NuageFamilles.svelte`, bascule « Nuage / Détail ». Aucune donnée nouvelle.
      Build statique vérifié
- [x] **①ter Ajustement visuel du nuage** (retour 2026-07-09 : cohérent/lisible
      mais **trop anonyme**) — fait :
      - libellés de niveau retirés de la vue nuage (inutiles ici) ;
      - **points plus gros** (rayon 6→16) + **grille resserrée** (viewBox compact) ;
      - **portrait en regard du nuage** (maquette) : layout portrait ↔ nuage,
        nuage sur petite grille → points plus présents. Illustration, pas une
        source de comptage (précédent Alençon, decisions.md 2026-07-05) ;
      - couleurs **repoussées** au palier style + légende des labels.
- [x] **①quater Portrait — vraies images** — fait (2026-07-09) : 27 portraits
      sourcés sur Wikimedia Commons via Wikidata P18 (`web/scripts/source_portraits.py`),
      **licence vérifiée fichier par fichier** (26 domaine public + 1 CC0), stockés
      **en local** dans `static/portraits/`, manifeste `static/data/portraits.json`
      (auteur, licence, source, regard). Crédit affiché en légende. 8 portraits
      « regardant à droite » retournés pour regarder le nuage (gravures à texte
      jamais retournées). Vignette de taille figée (fin des sauts). **Fallback**
      silhouette conservé. Reste **différé (palier style)** : traitement uniforme
      N&B/duotone
- [x] **①quinquies Textes de la fiche maître** — fait (2026-07-09, mode plan
      validé) : séparation des **trois natures de texte** (éditorial / mode d'emploi
      unique en bulle « Comment lire » / mentions techniques), **vocabulaire interne
      banni** de l'interface (notice→œuvre, niveau non affiché, « atelier de »),
      **légendes de portrait normées**, chiffres racontés en français. Couche
      éditoriale front `web/src/lib/editorial-maitres.js`. **Deux maîtres témoins**
      écrits main et validés (François Clouet, Rembrandt) ; les 25 autres en **angle
      dérivé** (repli). Règles gravées dans CLAUDE.md (dataviz + rédaction).
      - [ ] **Reste** : écrire à la main les **25 bios + angles** restants (montée
            en qualité, sous-étape éditoriale)
      - [ ] **Reste (hors P3-T1, page d'accueil)** : reformuler `+page.svelte`
            racine (« notices », « Détection : lexique », notation d'analyste) **en
            gardant les deux dénominateurs** (règle 2026-07-03)
- [x] **①sexies Labels du nuage** — fait (2026-07-10) : bulle « comment lire »
      retirée ; **couche de libellés publics** `web/src/lib/familles-public.js`
      (label + formule exacte + sens), axe **réordonné par distance** (option B),
      labels publics (attribué à · nom (?) · son atelier · son cercle · de son
      école · un suiveur · sa manière · dans son goût), **tooltips prudents**
      (formule exacte entre guillemets + sens, sans jargon), **micro-légende**
      statique « De gauche à droite, le lien au maître se desserre ». Règle
      « Couche de libellé public obligatoire » gravée dans CLAUDE.md.
      - [ ] **Reste** : « de son école » / « dans son goût » validés
            provisoirement (perfectibles) ; réduire chapô/bio (plus tard) ;
            ~~réutiliser la couche de traduction dans la vue Détail~~ (fait le
            2026-07-11 : les kickers de la vitrine « Œuvres » réutilisent les
            headers de familles-public.js)
- [x] **①septies Vitrine « Œuvres »** — fait (2026-07-11, validé avant code) :
      l'onglet « Détail » (échelle du doute + table des formules = redite du
      graphique) devient **« Œuvres »** : cartes groupées par forme dans l'ordre
      de l'axe, kicker = header public + pastille de la couleur du point,
      **verbatim du champ auteur en exergue** (seule citation littérale de
      l'application), lien « Voir la fiche publique → » (POP), copies « d'après »
      en bloc distinct avec un exemple lié, mention POP unique en petit corps.
      **Export enrichi** (`build_artistes.py`) : `code` de forme par exemple,
      2 exemples pour la forme dominante, `exemple_copie` par maître — le front
      ne re-parse jamais les extraits. `OeuvresMaitre.svelte` ; couleur par
      famille centralisée dans `familles-public.js`
- [x] **Palier données** (2026-07-12) : `src/build_artistes.py` exporte par maître
      `musees_doute` (1 entrée = 1 musée détenteur, doute seul, trié ; `lat`/`lon`
      explicites, `doute`, `niveaux`, `familles`), plus `nb_musees_doute`,
      `musee_principal` et `doute_sans_musee` (= 0). Invariants de comptage vérifiés
      par `assert` à la génération. Audit préalable dans donnees.md, schéma et
      garanties dans decisions.md (même date). Le champ `musees` (mixte) est
      conservé pour son libellé actuel, pas pour la carte
      **Concentration mesurée** : top musée = 89–98 % du doute chez la plupart des
      maîtres ; Ingres 3 musées, Rodin 4, Léonard 2 → prévoir un repli. Cas plus
      dispersés (bons pour la carte) : Van Dyck (21, top 35 %), Ribera (15, 14 %),
      Mignard (16, 26 %), Rigaud (19, 34 %)
- [x] **②a Fond de carte auto-hébergé** (2026-07-12, contrat validé avant sourcing) :
      `web/static/geo/regions-metropole.geojson` (13 régions, IGN Admin Express 2018
      via france-geojson, **Licence Ouverte**), simplifié mapshaper 5 % →
      **69 Ko**, **versionné**. Métropole seule ; projection `geoConicConformal`.
      Provenance reproductible dans `web/static/geo/README.md`, choix dans
      decisions.md, précaution publique dans methode-et-limites.md.
      **Outre-mer hors carte mais jamais exclu** : 1 seul point concerné (musée
      Léon Dierx, La Réunion, 1 œuvre Van Dyck) → mention explicite à afficher
      dans l'interface (spéc pour le composant)
- [x] **②b Composant carte par maître — premier rendu** — *le où* (2026-07-12,
      spéc validée avant code) : **d3-geo**, 1 point = 1 **musée détenteur** (grain
      honnête : l'œuvre est localisée par son musée), **taille FIXE** (tous les
      points identiques ; décision utilisateur après test A/B 2026-07-12 : le
      variable ∝ √doute mentait sur l'échelle inter-maîtres et gonflait les petits
      volumes → écarté), **couleur UNIQUE et stable** (`--carte-point`), fond régions
      discret, légende « un point = une présence », **tooltip = familles publiques**
      (`familles-public.js`, pastilles couleur, tri par valeur — plus aucun libellé
      de niveau ; le *combien* par musée est au survol + onglet graphique), mention
      hors-cadre. Repli **phrase** si < 2 musées projetables (onglet toujours
      visible). Nouveaux fichiers `web/src/lib/geo.js` (projection + bornes +
      normalisation d'enroulement du GeoJSON) et `web/src/lib/CarteMaitre.svelte` ;
      `Infobulle.svelte` étendu (champ `lignes`) ; onglet **Carte** branché dans
      `les-presque`. **Point technique** : france-geojson est enroulé à l'envers
      pour d3-geo → fit sur un `MultiPoint` des sommets et réinversion des anneaux
      au chargement (sinon projection dégénérée / fond en complément). Vérifié par
      captures (Le Brun, Ribera, Van Dyck, Ingres + tooltip).
      - [x] **Palier style — chevauchements** (2026-07-13) : `ecarterPoints`
            (relaxation déterministe, sans dépendance) écarte les points confondus
            (musées d'une même ville) et la grappe francilienne ; contour blanc
            renforcé, opacité 0,82. Vérifié (Le Brun, Boucher, Rubens)
      - [x] **Point-lien POP pour l'œuvre unique** (2026-07-13) : musée à 1 œuvre →
            le point devient un lien vers la notice POP (`<a>` SVG, `target=_blank`,
            `rel=noreferrer`, focus visible) ; tooltip = aperçu (titre si dispo,
            mention + pastille). Multi-œuvres non cliquables, inchangés. Pipeline :
            `oeuvre_unique {reference, titre}` exporté si `doute==1` (188 avec titre,
            2 sans). `Infobulle` : champ `titre`. Pas de nouvelle vue « œuvre »
      - [x] **Palier style** (2026-07-13) : fond « régions très estompées » (aplat
            quasi nul, frontières gris très pâle) ; survol/focus des points plus
            franc (pleine opacité + halo blanc élargi), unifié lien/non-lien, pas de
            distinction au repos des points cliquables ; carte dans une colonne
            centrée (titre/fond/légende/mentions alignés) ; légende et mention
            hors-cadre au même registre (petit corps, encre douce, filet) ; vue
            étroite vérifiée. Captures Le Brun / Van Dyck / 390 px, build OK
      - [ ] **Différé (contenu, hors style)** : éventuel repère texte du musée
            principal (« le plus concerné : … ») — à décider séparément
- [x] Caveat page méthode : **taille fixe** (un point = une présence), la carte dit
      *où* et non *combien* ; **jamais** de comparaison de catalogage entre musées
      (methode-et-limites.md mis à jour le 2026-07-12 après le choix taille fixe)
- [x] **②c Légende permanente des mentions** (2026-07-13, validée avant code) : clé
      des couleurs sous la liste des maîtres, commune aux trois vues, réutilise
      `header` + `corps` de `familles-public.js` (source unique, mêmes mots que les
      tooltips), pastilles rondes, ordre de l'axe. Repliable en mobile (état JS,
      pas un `<details>` natif). `LegendeFamilles.svelte`. Un `corps` reformulé
      (atelier). Aucune donnée touchée
- [x] **②d Harmonisation des tooltips** (2026-07-13, après revue) : les trois
      tooltips vivants (graphique / carte / jauges) passaient déjà par
      `Infobulle.svelte` → renfort, pas de fork. Header en bande grisée + pastille
      optionnelle, largeur stable (13–17 rem), lignes à nombres alignés (+ `%` gris),
      `valeur` optionnelle. Jauges : d'un tooltip par segment à un **récap du maître**
      (header = nom, lignes par mention + %), formule « du doute » supprimée. Le
      tooltip donne l'info locale ; la légende fixe porte la grammaire des couleurs.
      Fichiers : `Infobulle.svelte`, `familles-public.js` (`tooltipFamille`),
      `BarreFamilles.svelte`. Vérifié par captures (6 cas, dont singulier et 390 px)

### P3-T2 — « Avant / après » — ⏸ EN RÉSERVE depuis le recentrage 2026-07-15

> **Hors périmètre V1 publique** (voir bloc « ★ RECENTRAGE » en tête). Tout ce
> qui suit est **conservé en l'état** comme dossier futur : pipeline, taxonomie
> v2, tests, front (onglets En bref / Les chiffres / Les œuvres / Repères, anneau,
> prototype de cartes datajournalisme des 2026-07-14 et 2026-07-15). `/revisions`
> est repassé hors nav publique (`prete: false`). Rien n'est supprimé.

Choisie le 2026-07-13 après audit des données (26 667 vrais avant→après dans
`Ancienne_attribution`). Cadrage V1 simplifié le 2026-07-14. **Détail complet
dans docs/rubrique-revisions.md** (titre provisoire « Avant / après »,
structure par type de passage, lot V1 par diversité, images écartées, graphes
stats, schéma revisions.json, règles de comparaison, contrôles, garde-fous,
10 prototypes + 10 exclus).

- [x] ⏸ Validation du cadrage V1 : titre, structure, lot, absence d'images,
      graphes, schéma — **validée le 2026-07-14** (libellés publics ajustés)
- [x] Pipeline : src/build_revisions.py → data/exports/web/revisions.json
      (16,7 Ko) : passages (partition assert = 26 667), domaines, siècles,
      anciens noms **hors copie** (filtre, pas palmarès), direction inverse
      (5 584), lot V1 (32 cas, 19 musées, Louvre 6 %, plafond 2/musée global).
      Parsing renforcé (préfixe « ancienne attribution : » style Louvre)
- [x] Échantillon stratifié : src/build_revisions_sample.py →
      data/exports/echantillon_revisions.csv (80 lignes, 4 passages + 6 strates
      de pièges, graine 20260714)
- [x] ⏸ **Vérification manuelle rendue** (2026-07-14) : 44 OK / 18 à exclure /
      8 faux passage / 10 faux parsing, 80 commentaires
- [x] Refonte de la classification (`src/revisions_classify.py`) : **taxonomie
      v2 à 7 catégories** (3 nouvelles : « Même nom plus prudent », « Déjà une
      copie », « Plusieurs anciens noms ») + 5 bugs de parsing corrigés ; calée
      sur les 80 verdicts
- [x] Verdicts figés en tests (`tests/test_revisions.py`, 25 cas + cohérence
      CSV) ; `uv run pytest` = 60 passés ; `revisions.json` régénéré
- [ ] ⏸ **Validation du bilan post-vérification** (nouvelles catégories,
      répartition, lot) avant le front
- [ ] Front (route dédiée) : intro + section stats (graphes classiques) +
      galerie de cas filtrable — seulement après validation du bilan

Vérifié le 2026-07-14 : images non affichables en droit (POP = CDN interne,
pas de licence par œuvre) → cartes textuelles + lien POP. Périodes trop rares
pour une frise (16 % œuvres datables, 7 % révisions datées).

### Briques restantes (recadrées le 2026-07-13, voir decisions.md)

- [~] Décodeur de l'échelle du doute : **RÉDUIT** — plus une rubrique (la
      légende permanente des « presque » couvre l'essentiel) ; devient un
      encart « poids national par formule + exemple » de la page méthode ou
      de l'accueil
- [~] Carte nationale qualifiée : **EN PAUSE** — réponse déjà connue
      (concentration), biais de couverture, redondance avec la carte par
      maître ; réouverture seulement sur angle neuf
- [x] Page « méthode et limites » — livrée le 2026-07-17, **refondue en six questions le
      2026-07-31** (voir la brique « Méthode et limites » plus haut). L'encart décodeur
      n'y a pas été ajouté : la page renvoie à « Comprendre les mentions » plutôt que de
      redire l'échelle, pour ne pas doubler une page par une autre
- [ ] Rappels P3-T1 encore ouverts : reformuler l'accueil (deux dénominateurs
      gardés) ; 25 bios restantes ; moteur de recherche toute base
