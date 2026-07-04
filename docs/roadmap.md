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
- [ ] ⏸ Vérification manuelle du mini-lot par l'utilisateur
- [ ] Bilan T5bis : taux pondérés recalculés → si doute < 10 % : **GO**
- [ ] ⏸ Validation : décision de phase — fin de la phase 1

## Phase 2 — Typologie et pipeline consolidé (esquisse, dépend du go/no-go)

- [ ] Chiffrer les recouvrements entre les trois familles (doute / d'après /
      ancienne attribution) : une même notice peut porter plusieurs marqueurs,
      ne jamais publier des chiffres qui s'additionnent à tort (décision 2026-07-03)
- [ ] Classification des formules par niveau de doute (échelle inspirée du décret Marcus)
- [ ] Pipeline reproductible CSV → JSON légers agrégés (par musée avec total versé,
      par formule, par domaine)
- [ ] Fiches des cas racontables (dont Alençon, notice publique uniquement)

## Phase 3 — Restitution (esquisse, forme arrêtée après la phase 1)

- [ ] Forme retenue : carte D3.js + récit guidé pressenti (coordonnées disponibles)
- [ ] Page « méthode et limites » publiée au même rang que le récit
- [ ] Front consommant les JSON exportés (statique si possible, Flask/FastAPI
      seulement si besoin serveur avéré)
