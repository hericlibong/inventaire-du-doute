# Décisions

Chaque décision est datée et motivée. Les plus récentes en haut.

## 2026-07-03 — Validation T3 : dénominateur vedette et périmètre (décisions utilisateur)

- **Le taux mis en avant est celui sur les notices avec auteur renseigné**
  (3,53 % au comptage v0) : c'est le doute mesuré là où un doute peut exister.
  **Le taux sur la base entière (2,90 %) est toujours donné en second**, jamais
  omis. C'est un choix d'écriture, pas de calcul : les deux chiffres restent
  publiés côte à côte.
- **Le comptage de référence porte sur toute la base** (la question centrale
  vise « les musées de France », pas un domaine). **Les beaux-arts
  (peinture/dessin/sculpture/estampe) sont l'angle éditorial** : ils
  concentrent ~80 % du doute détecté. Les deux lectures s'emboîtent, on ne
  choisit pas entre elles.
- Pour la phase 2 : **chiffrer les recouvrements entre les trois familles**
  (doute / d'après / ancienne attribution) — une même notice peut porter
  plusieurs marqueurs, il ne faut jamais publier des chiffres qui
  s'additionnent à tort. Tâche ajoutée à la roadmap.

## 2026-07-03 — Méthode de comptage (T3, décision utilisateur)

- **Tous les taux sont produits avec deux dénominateurs** : sur l'ensemble des
  notices ET sur les seules notices dont `Auteur` est non vide. Motif : ~18 % des
  notices n'ont pas d'auteur renseigné (archéologie, ethnologie…) ; un taux sur
  la base entière dilue le phénomène, un taux sur les notices « avec auteur »
  le mesure là où il peut exister. **Le choix du taux à mettre en avant sera
  fait avec l'utilisateur à la validation de T3.**
- Choix du périmètre (tout Joconde vs peinture/dessin/sculpture/estampe) reporté
  à la fin de T3, au vu de la ventilation réelle du doute par domaine (T2 validée).
- Rappel actif pour T3 : « école française » dans `Ecole_pays` = nationalité,
  pas un doute ; le marqueur est « école de [artiste] », plutôt dans `Auteur`.

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
