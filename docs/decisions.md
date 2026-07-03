# Décisions

Chaque décision est datée et motivée. Les plus récentes en haut.

## 2026-07-03 — Décisions d'initialisation (phase 0)

- **CSV complet = matière de référence de la phase 1.** C'est la source canonique
  citée dans la publication finale ; l'API du ministère n'est qu'un extrait
  (~30 % de notices en moins). L'API sert aux contre-vérifications ponctuelles.
- **pandas en lecture par morceaux** (`chunksize` + `usecols`) : on ne lit que
  ~15 colonnes sur ~70, mémoire maîtrisée, code lisible. Pas de base de données
  ni de framework à ce stade.
- **Détection par lexique de motifs regex versionné dans le code** (pas de NLP) :
  auditable et explicable — conforme à la posture « on lit ce qui est écrit ».
- **Environnement uv + pyproject.toml** (choix utilisateur).
- **Échantillon de vérification au format CSV tableur** (choix utilisateur) :
  colonnes `verdict` et `commentaire` à remplir, lien vers la notice POP.
- **`data/` non versionné** (1,1 Go) ; `src/download.py` permet de tout récupérer.

## Roadmap et points de validation

### Phase 0 — Initialisation ✅ (en attente de relecture)
Arborescence, CLAUDE.md, docs/, environnement uv, git.
⏸ Relecture de CLAUDE.md et des docs avant de toucher aux données.

### Phase 1 — Test go/no-go sur la qualité des données
- **T1** Nomenclature + téléchargement → mapping des champs documenté. ⏸
- **T2** Profilage du CSV complet → chiffres, choix du périmètre. ⏸
- **T3** Détecteur v0 → taux de base global et par domaine, ventilation par marqueur. ⏸
- **T4** Échantillon stratifié ~200 notices → CSV de vérification manuelle. ⏸
- **T5** Bilan des faux positifs → recommandation go / reformulation / no-go. ⏸
Seuils indicatifs discutés : < 10 % de faux positifs = go, 10–25 % = reformulation
du lexique, > 25 % = no-go.

### Phases suivantes (esquisse, dépendent du go/no-go)
- **Phase 2** — Typologie du doute (échelle inspirée du décret Marcus) et pipeline
  consolidé CSV → JSON légers agrégés (toujours avec le total versé par musée).
- **Phase 3** — Restitution web (carte D3.js + récit guidé pressenti, forme arrêtée
  après la phase 1), page « méthode et limites » publiée au même rang que le récit.
