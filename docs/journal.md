# Journal d'avancement

Notes au fil de l'eau. Une entrée par séance de travail, les plus récentes en haut.

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
