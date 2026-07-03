# Journal d'avancement

Notes au fil de l'eau. Une entrée par séance de travail, les plus récentes en haut.

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
