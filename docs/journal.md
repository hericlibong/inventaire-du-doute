# Journal d'avancement

Notes au fil de l'eau. Une entrée par séance de travail, les plus récentes en haut.

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
