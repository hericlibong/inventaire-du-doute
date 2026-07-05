# Décisions

Chaque décision est datée et motivée. Les plus récentes en haut.

## 2026-07-05 — Bilan T5bis : recommandation GO (proposition, à valider)

Mini-contrôle T4bis rendu (65/65 verdicts). Résultats des familles reformulées :
- **? : 0 faux sur 15** (16 % en v0) — corrigé ;
- **« Atelier de X » écarté : 15/15 confirmés** — l'exclusion ne jette aucun
  vrai doute, le choix précision-contre-exhaustivité est validé par les faits ;
- **école de : 2/15 (13 %)** — restes : « École de Fontainebleau » (aire
  artistique) et « Nouvelle École de Paris » (mouvement, champ Ecole_pays) ;
- **atelier : 6/20 (30 %)** — restes : des ateliers-entreprises portant le
  qualificatif « (atelier) » (VAUCANSON, JACQUEMIN Frères…). Signal net : les
  faux vivent en ethnologie/artisanat, les vrais en peinture/dessin.

Taux global pondéré (catégorie doute, calcul : src/evaluate_recheck.py) :
- **5,7 % conservateur** (< 10 %) ; 3,3 % ajusté (le faux « attribué,
  d'après » de T4 est prouvé exclu par les tests).

**Recommandation : GO.** Le seuil de phase est franchi. Les faiblesses
résiduelles sont localisées, chiffrées et publiables comme telles ; à traiter
en phase 2 dans la typologie plutôt que par une nouvelle itération de regex :
- la famille « atelier » (7 % du doute) sera marquée « fiabilité moindre,
  sensible au domaine » — option : la restreindre aux domaines beaux-arts ;
- « École de Fontainebleau / de Paris » : liste d'exclusion des écoles-lieux
  consacrées, à trancher en construisant la typologie ;
- taux par famille publiés avec le chiffre global (transparence).

## 2026-07-04 — Lexique v1 : lire la convention, pas le mot (cycle validé par l'utilisateur)

Principe directeur de la reformulation « atelier de » (validé explicitement) :
**le doute Joconde s'écrit en qualificatif entre parenthèses après un nom**
(« COROT (atelier) »), tandis que « Atelier de Pistillus » en nom d'auteur
désigne un créateur assumé. On lit la convention d'écriture des conservateurs,
plus le mot isolé. Choix assumé de **précision contre exhaustivité** : mieux
vaut sous-compter en le disant que sur-compter en silence.

Corrections v1 (détail en tête de `src/markers.py`) :
1. « atelier » : qualificatif seulement, détection segment par segment ;
   garde-fous : nom commençant par « atelier », rôles de production
   (graveur, imprimeur, photographe…). La forme « Atelier de X » en nom
   d'auteur part en catégorie « ecarte » (1 123 notices), chiffrée à part et
   soumise au mini-contrôle : on vérifie qu'on ne jette pas de vrais doutes.
2. « école de » : exclusion de la forme inversée « Hollande École de (École
   hollandaise) » ; qualificatif « (école) » en fin de token seulement.
3. « ? » : la parenthèse ne doit contenir aucun chiffre (« (?-1996) » exclu).
4. Doctrine « (attribué, d'après) » → copie, implémentée en exclusion.

Les verdicts humains de T4 sont figés en **tests automatiques**
(`tests/test_markers.py`, 25 cas) : toute future retouche du lexique doit
repasser devant eux. Recomptage v1 : doute = 25 220 notices (2,46 % base /
2,99 % avec auteur). Mini-contrôle T4bis : 65 lignes
(`data/exports/echantillon_recheck.csv`, graine 202607).

## 2026-07-04 — Bilan T5 : recommandation REFORMULATION (proposition, à valider)

Verdict chiffré (détail : `data/exports/bilan_faux_positifs.csv`, calcul :
`src/evaluate_sample.py`, taux pondérés par le poids réel des familles) :

| Catégorie | Faux positifs pondérés | Lecture |
|---|---|---|
| doute | **17,0 %** | tranche « reformulation » (seuils : <10 go, 10–25 reformulation, >25 no-go) |
| copie (« d'après ») | 0,0 % | impeccable |
| révision (Ancienne_attribution) | 0,0 % | impeccable |

Le 17 % n'est pas diffus : il est concentré dans des familles précises avec
des causes identifiées et corrigeables :
- **atelier de : 64 % de faux** (~3 600 notices) — trois causes : ateliers de
  production donnés comme auteurs assumés (`Atelier de Pistillus`), studios
  d'imprimeurs/photographes, mentions biographiques dans Précisions ;
- **école de : 20 %** — la forme inversée `Hollande École de (École
  hollandaise)` = école nationale, pas un doute (signal d'exclusion net :
  la parenthèse `(École …)` qui suit) ;
- **? : 16 %** — le `?` de date de naissance `(?-1996)` (la correction T3
  n'excluait que les chiffres AVANT le `?`) ;
- le reste tient très bien : attribué à 3,5 %, manière de 0 %, genre de 0 %.

**Recommandation : ni go ni no-go — reformulation ciblée.**
1. Lexique v1 : corriger les trois familles ci-dessus + intégrer la doctrine
   (`(attribué, d'après)` → copie ; mentions biographiques hors jeu) ;
2. recompter la base entière ;
3. mini-contrôle manuel (~60-80 lignes, familles reformulées uniquement) ;
4. si le doute pondéré passe sous 10 % → go définitif.
La matière, elle, est validée : abondante, structurée, et deux catégories
sur trois sortent sans aucune erreur.

## 2026-07-04 — Doctrine de vérification (décisions utilisateur, T4→T5)

Règle générale dégagée par la vérification manuelle des 206 lignes :
**un marqueur ne compte que s'il qualifie l'attribution de l'œuvre de la
notice** — pas s'il apparaît dans une biographie, dans un nom propre (atelier
de production, studio d'imprimeur), ou à propos d'une autre œuvre citée.

Deux points arbitrés explicitement :
- **Qualificatifs combinés `(attribué, d'après)` : « d'après » l'emporte** —
  la notice est une copie, elle sort de la catégorie doute.
- **`anonyme (attribué)` : cas documenté tel quel**, ni vrai ni faux positif
  (verdict « incertain », exclu du calcul des taux mais conservé et montré
  comme curiosité de la base).

## 2026-07-03 — Règle permanente : documenter tout ce qui touche à l'approche (décision utilisateur)

Toute modification ou implémentation concernant l'approche (détection,
échantillonnage, comptage, périmètre…) est documentée au moment où elle est
faite. Motif : l'approche devra être expliquée et justifiée publiquement, et
elle fait partie de la narration du projet — la fabrique du chiffre est une
partie de l'histoire. Règle inscrite dans CLAUDE.md.

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
