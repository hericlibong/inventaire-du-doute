# Classification des familles de marqueurs — document de référence

Établie en phase 1, validée par deux contrôles humains (T4 : 206 notices,
T4bis : 65 notices). **Source de vérité machine : `src/markers.py`** (le
lexique versionné) — ce document en est la lecture humaine ; en cas d'écart,
le code fait foi et ce document doit être mis à jour.

Rôle à venir : cette classification alimentera la typologie du doute
(phase 2) et les visualisations (phase 3). Les catégories et les fiabilités
mesurées ci-dessous conditionnent ce qu'on pourra montrer et affirmer.

## Les quatre catégories

| Catégorie | Sens | Publiable comme |
|---|---|---|
| **doute** | incertitude déclarée sur l'auteur de l'œuvre | le chiffre central du projet |
| **copie** | copie assumée d'après un modèle — pas un doute | un phénomène voisin, raconté à part |
| **revision** | attribution passée, révisée depuis | l'histoire des changements d'avis |
| **ecarte** | détecté puis écarté par règle explicite, chiffré | la preuve de rigueur (annexe méthode) |

## Familles de la catégorie DOUTE

Sens usuel des formules : décret Marcus (1981) et usage des catalogues ;
la hiérarchisation fine par niveau de doute est l'objet de la phase 2.

| Famille (code) | Formule | Ce qu'elle dit | Notices v1 | Fiabilité mesurée |
|---|---|---|---|---|
| `attribue` | « attribué à », « attr. », `(attribué)` | œuvre donnée au maître sans certitude — le doute « classique » | 17 926 | **96,5 %** (T4, 1 faux/29) |
| `point_interrogation` | `(?)` en qualificatif, sans chiffre | doute sec, non argumenté | 2 213 | **100 %** (T4bis, 0/15) |
| `ecole_de` | « école de X », `(école)` | élève ou proche du maître, dans son sillage | 2 093 | **86,7 %** (T4bis, 2/15 — restes : écoles-lieux consacrées type Fontainebleau) |
| `atelier_de` | `(atelier)` en qualificatif | exécutée dans l'atelier du maître, main incertaine | 1 759 | **70 %** (T4bis, 6/20 — restes : ateliers-entreprises ; faux concentrés hors beaux-arts) ⚠ |
| `maniere_de` | « (à la) manière de » | imitation du style, auteur inconnu | 703 | **100 %** (T4, 0/15) |
| `entourage_de` | « entourage de » | cercle proche du maître | 503 | **93,3 %** (T4, 1/15) |
| `genre_de` | « genre de » | proche de « manière de » | 303 | **100 %** (T4, 0/15) |
| `suiveur_de` | « suiveur de » | influencé par le maître, parfois plus tardif | 80 | **90 %** (T4, 1/10) |
| `presume` | « présumé » (champs auteur) | auteur supposé | 4 | 75 % (T4, 1/4 — famille marginale) |

⚠ `atelier_de` : fiabilité moindre, sensible au domaine. Décision en phase 2
(typologie) : restriction éventuelle aux domaines beaux-arts.

## Familles de la catégorie COPIE

| Famille | Formule | Ce qu'elle dit | Notices v1 | Fiabilité |
|---|---|---|---|---|
| `d_apres` | « d'après X » | copie d'un modèle identifié, copiste éventuellement connu | 22 564 | **100 %** (T4, 0/15) |
| `copie` | « copie » | idem, formulation directe | 280 | **100 %** (T4, 0/9) |

Doctrine (2026-07-04) : `(attribué, d'après)` dans la même parenthèse → copie.

## Familles de la catégorie REVISION

| Famille | Source | Ce qu'elle dit | Notices v1 | Fiabilité |
|---|---|---|---|---|
| `champ_ancienne_attribution` | champ dédié ATTR renseigné | « on a cru que c'était X, on ne le croit plus » | 27 266 | **100 %** (T4, 0/15) |
| `anciennement_attribue` | la formule en toutes lettres | idem, rarissime en texte | 7 | 100 % (T4, 0/7) |

## Famille de la catégorie ECARTE

| Famille | Forme | Pourquoi écartée | Notices v1 | Contrôle |
|---|---|---|---|---|
| `atelier_nom` | « Atelier de X » en nom d'auteur | l'atelier EST le créateur assumé (manufactures, studios) | 1 123 | exclusion confirmée **15/15** (T4bis) |

## Règles transverses

- Une notice peut porter plusieurs familles → **les recouvrements seront
  chiffrés en phase 2** avant toute addition de chiffres.
- Cas « incertain » documenté : `anonyme (attribué)` — hors calcul, montré
  comme curiosité.
- Toute évolution du lexique doit passer les 25 tests issus des verdicts
  humains (`tests/test_markers.py`).
