# Journal d'avancement

Notes au fil de l'eau. Une entrée par séance de travail, les plus récentes en haut.

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
