# Roadmap — L'inventaire du doute

Suivi des phases et des tâches. Mis à jour à chaque fin de tâche.
Chaque ⏸ est un point de validation utilisateur : on s'y arrête.

## Phase 0 — Initialisation ✅

- [x] Arborescence (docs/, src/, data/), .gitignore
- [x] CLAUDE.md (contexte, règles non négociables, méthode)
- [x] docs/ amorcés : journal, décisions, données, méthode-et-limites
- [x] Environnement uv + pyproject.toml, git init + premier commit
- [x] ⏸ Validation utilisateur — **validée le 2026-07-03**
  (seuils T5 confirmés, titre « L'inventaire du doute » adopté)

## Phase 1 — Test go/no-go sur la qualité des données

### T1 — Nomenclature et téléchargement ✅ (en attente de validation)
- [x] Télécharger la nomenclature ODS et le CSV complet (src/download.py)
- [x] Lire la nomenclature : tableau des champs (nom CSV ↔ nom API ↔ définition)
      dans docs/donnees.md
- [x] Confirmer les champs liés à l'auteur et aux anciennes attributions
- [ ] ⏸ Validation : synthèse des champs présentée

### T2 — Profilage du CSV complet
- [ ] Nombre réel de lignes, écart chiffré avec l'extrait API
- [ ] Taux de remplissage des champs auteur / école / ancienne attribution
- [ ] Répartition par domaine
- [ ] ⏸ Validation : chiffres présentés, choix du périmètre
      (tout Joconde vs peinture/dessin/sculpture/estampe — les deux comptages fournis)

### T3 — Détecteur v0 + taux de base
- [ ] src/markers.py : lexique versionné des formules (attribué à, ?, école de,
      atelier de, entourage de, suiveur de, manière de, anciennement attribué à,
      présumé…), graphies multiples
- [ ] « d'après » détecté mais classé à part ; « présumé » signalé suspect côté sujet
- [ ] Application par chunks sur auteur, precisions_sur_l_auteur,
      ancienne_attribution, ecole_pays
- [ ] Taux de base global et par domaine, ventilation par famille de marqueur
      → data/exports/comptages.csv
- [ ] ⏸ Validation : présentation des taux et de la ventilation

### T4 — Échantillon de vérification
- [ ] ~200 notices stratifiées par famille de marqueur (marqueurs rares
      sur-représentés), graine aléatoire fixée
- [ ] Export CSV tableur : référence, marqueur, champ source, extrait, titre,
      auteur, musée, ville, lien POP, colonnes vides verdict / commentaire
- [ ] Mode d'emploi court
- [ ] ⏸ Validation : vérification manuelle par l'utilisateur (à son rythme)

### T5 — Bilan go/no-go
- [ ] Réimport du CSV annoté, taux de faux positifs global et par marqueur
- [ ] Liste des pièges de champ rencontrés
- [ ] Recommandation argumentée dans docs/decisions.md
      Seuils confirmés : **< 10 % = go, 10–25 % = reformulation, > 25 % = no-go**
- [ ] ⏸ Validation : décision de phase — fin de la phase 1

## Phase 2 — Typologie et pipeline consolidé (esquisse, dépend du go/no-go)

- [ ] Classification des formules par niveau de doute (échelle inspirée du décret Marcus)
- [ ] Pipeline reproductible CSV → JSON légers agrégés (par musée avec total versé,
      par formule, par domaine)
- [ ] Fiches des cas racontables (dont Alençon, notice publique uniquement)

## Phase 3 — Restitution (esquisse, forme arrêtée après la phase 1)

- [ ] Forme retenue : carte D3.js + récit guidé pressenti (coordonnées disponibles)
- [ ] Page « méthode et limites » publiée au même rang que le récit
- [ ] Front consommant les JSON exportés (statique si possible, Flask/FastAPI
      seulement si besoin serveur avéré)
