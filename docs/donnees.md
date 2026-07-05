# Constats sur les données

Tout ce qu'on apprend sur la base Joconde au fil du projet : structure, pièges,
chiffres vérifiés. Chaque constat indique sa date et comment il a été obtenu.

## Constats de l'exploration initiale (2026-07-03, via l'API Opendatasoft)

### L'écart de volumétrie entre portails est éclairci

- data.gouv.fr annonce « + 1 000 000 notices » pour le CSV complet (1,1 Go).
- Le portail du ministère expose un dataset nommé `base-joconde-extrait` :
  **721 629 notices** (interrogé le 2026-07-03). C'est donc un **extrait**,
  pas la base complète. L'écart (~30 %) sera chiffré précisément en T2 ;
  sa nature (quelles notices manquent ?) reste à comprendre si nécessaire.

### Champs pertinents repérés (noms API, à mapper avec le CSV en T1)

| Champ API | Usage pour le projet |
|---|---|
| `auteur` | champ principal : porte les qualificatifs d'attribution |
| `precisions_sur_l_auteur` | précisions en texte libre |
| `ancienne_attribution` | attributions révisées — champ dédié ! |
| `ecole_pays` | école / pays |
| `domaine` | filtrage du périmètre (peinture, dessin, sculpture…) — champ multivalué |
| `denomination` | type d'objet |
| `nom_officiel_musee`, `ville`, `region`, `departement` | localisation |
| `code_museofile` | identifiant musée (jointure possible avec Muséofile) |
| `coordonnees` | geo_point_2d → **cartographie possible sans géocodage** |
| `reference` | identifiant de notice → lien vers la fiche POP |
| `sujet_represente`, `precisions_sujets_representes` | garde-fou « présumé » côté sujet |

### La donnée est plus structurée qu'espéré

Le champ `auteur` suit une convention de qualificatifs entre parenthèses :

- `MODERNO (attribué)`
- `LESCHER (attribué, ?)`
- `LOMBARD (?, attribué)`
- `anonyme (attribué, attribué)` — doublons possibles dans les qualificatifs

C'est une convention documentaire (méthode Joconde), pas du texte libre :
la détection pourra s'appuyer dessus, en plus de la recherche plein texte.

### Premiers ordres de grandeur (sur l'extrait API, 721 629 notices)

Recherche plein texte dans le champ `auteur` :

| Motif | Notices |
|---|---|
| « attribué » | 16 860 |
| « atelier de » | 1 390 |
| « école de » | 500 |
| « entourage de » | 156 |
| « anciennement attribué » | 1 (mais champ dédié ci-dessous) |
| `ancienne_attribution` non vide | **25 906** |

Lecture : la matière existe, et le champ dédié `ancienne_attribution` est plus
riche que la mention textuelle. Ces chiffres sont des minima sur un extrait —
le comptage de référence se fera sur le CSV complet (T3).

## T1 — Structure du CSV et mapping des champs (2026-07-03)

CSV téléchargé le 2026-07-03 (version du mercredi 2026-07-01 a priori) :
**1,19 Go, 67 colonnes, séparateur `|`**, en-têtes identiques aux noms de champs
de l'API. La nomenclature ODS liste 77 intitulés (dont des champs propres à la
plateforme POP absents du CSV : crédits photo, copyright, historique…).
Les champs multivalués utilisent `;` comme séparateur interne (ex. `Domaine` :
`archéologie;gallo-romain;numismatique`).

### Champs au cœur du projet (détection de l'incertitude)

| Colonne CSV | Étiquette Joconde | Champ API | Définition (nomenclature) |
|---|---|---|---|
| `Auteur` | AUTR | `auteur` | Auteur — porte les qualificatifs entre parenthèses |
| `Precisions_sur_l_auteur` | PAUT | `precisions_sur_l_auteur` | Précisions auteur (texte libre) |
| `Ancienne_attribution` | ATTR | `ancienne_attribution` | Ancienne attribution — champ dédié |
| `Ecole_pays` | ECOL | `ecole_pays` | École-pays |

### Champs de garde-fou (piège « présumé » côté sujet)

| Colonne CSV | Étiquette | Champ API |
|---|---|---|
| `Sujet_Represente` | REPR | `sujet_represente` |
| `Precisions_sujets_representes` | PREP | `precisions_sujets_representes` |
| `Titre` | TITR | `titre` |

### Champs de contexte (périmètre, localisation, restitution)

| Colonne CSV | Étiquette | Usage |
|---|---|---|
| `Reference` | REF | identifiant → lien POP `pop.culture.gouv.fr/notice/joconde/{ref}` |
| `Domaine` | DOMN | périmètre (peinture, dessin, sculpture…) — multivalué `;` |
| `Denomination` | DENO | type d'objet |
| `Nom_officiel_musee` | NOMOFF | musée |
| `Code_Museofile` | MUSEO | identifiant musée (jointure Muséofile possible) |
| `Ville` / `Departement` / `Region` | VILLE_M / DPT / — | localisation administrative |
| `coordonnees` | — (ajout POP) | lat, lon → cartographie sans géocodage |

Lecture pandas validée : `pd.read_csv(sep='|', usecols=…, chunksize=…)` passe
sans erreur sur les premières lignes ; le comptage complet et le profilage sont
l'objet de T2.

## T2 — Profil du CSV complet (2026-07-03)

Obtenu par `src/profile_data.py` (rapport brut : `data/exports/profil.txt`).

### Volumétrie

- **1 023 705 notices**, 555 musées distincts (`Code_Museofile`).
- Écart avec l'extrait API (721 629 notices le 2026-07-03) : **302 076 notices,
  soit 29,5 % de la base absents de l'API**. L'annonce « + 1 000 000 » de
  data.gouv est exacte ; le comptage de référence se fait bien sur le CSV.

### Taux de remplissage des champs cœur

| Champ | Renseigné | Taux |
|---|---|---|
| `Auteur` | 841 953 | 82,2 % |
| `Precisions_sur_l_auteur` | 457 756 | 44,7 % |
| `Ecole_pays` | 416 091 | 40,6 % |
| `Ancienne_attribution` | 27 266 | 2,7 % |

À noter : ~18 % des notices n'ont **pas** de champ Auteur. Une absence d'auteur
n'est pas un marqueur d'incertitude au sens du projet (beaucoup d'objets
archéologiques ou ethnologiques n'ont pas d'auteur attendu) — mais c'est un
chiffre de contexte intéressant pour le récit.

### Champs de contexte

- `Domaine` : 100 % renseigné — le filtrage de périmètre est fiable.
- `coordonnees` : **99,8 %** renseigné — la cartographie couvrira presque tout.
- `Code_Museofile` : 100 % — les agrégats par musée (avec total versé) sont sûrs.

### Répartition par domaine (multivalué : une notice peut compter plusieurs fois)

Top : dessin 300 156 · arts graphiques 152 140 · estampe 141 891 ·
photographie 109 472 · archéologie 105 889 · peinture 91 450 ·
ethnologie 76 745 · céramique 57 141 · sculpture 50 139…

**Périmètre pressenti** (au moins un domaine parmi peinture / dessin /
sculpture / estampe) : **583 346 notices, 57,0 % de la base**.

## T3 — Détecteur v0 et taux de base (2026-07-03)

Lexique : `src/markers.py` (13 familles, 3 catégories : doute / copie / révision).
Comptage : `src/count_markers.py` → `data/exports/comptages.csv` et
`comptages_domaines.csv`.

### Taux de base (les deux dénominateurs, décision utilisateur)

| Agrégat | Notices | / toute la base | / notices avec auteur |
|---|---|---|---|
| Au moins un marqueur de **doute** | 29 726 | 2,90 % | 3,53 % |
| « d'après » (copie, classé à part) | 22 564 | 2,20 % | 2,68 % |
| Champ `Ancienne_attribution` renseigné (révision) | 27 266 | 2,66 % | 3,19 % |

Périmètre peinture/dessin/sculpture/estampe : 23 939 notices avec doute
sur 583 346 (4,10 %) — soit **80,5 % de tout le doute détecté**.

### Ventilation du doute (familles principales)

attribué à 18 008 · atelier de 5 558 · école de 2 865 · ? 2 731 ·
manière de 703 · entourage de 503 · genre de 303 · suiveur de 80 · présumé 4.

### Taux de doute par domaine (≥ 10 000 notices, top)

peinture **6,00 %** · dessin 4,72 % · artisanat-industrie 4,55 % ·
histoire 4,49 % · gallo-romain 3,92 % · … · sculpture 2,27 % · estampe 2,22 %.
La peinture est bien le domaine le plus « douteux », mais le dessin fournit le
plus gros volume (14 170 notices).

### Constats et pièges rencontrés en construisant le détecteur

- **Piège « ? » de dates (corrigé)** : dans `Auteur`, la parenthèse peut contenir
  des dates incertaines — `Aquaviva Oscar (19..-19..?)`. Le motif exclut
  désormais les parenthèses contenant un chiffre : 9 710 → 2 731 détections
  (~72 % du signal brut était du bruit de dates !).
- **Piège « école des Beaux-Arts » (corrigé)** : dans `Precisions_sur_l_auteur`,
  les biographies citent les écoles-institutions. « école de » n'est plus cherché
  que dans `Auteur` et `Ecole_pays` ; le qualificatif `(école)` — vu dans
  `PALMA Giovane (école)` — est ajouté. Perte assumée : les « école de Rembrandt »
  éventuels en texte libre de PAUT.
- **« présumé » est quasi absent des champs auteur (4 cas)** : le piège annoncé
  (« portrait présumé de X ») vit dans Titre/Sujet_represente, champs que le
  détecteur ne fouille pas. Le garde-fou était le bon : ne pas fouiller ces champs.
- **« anciennement attribué » en texte libre est rarissime (7 cas)** : cette
  information passe par le champ dédié `Ancienne_attribution` (27 266). La
  structure de la base est plus fiable que son texte.
- **« ATELIER DE MOULAGE », « ATELIER DE ROME »** : « atelier de » peut être un
  nom d'atelier de production (moulages de musées !), pas un doute sur un maître
  → à surveiller de près en T4.
- Graphies sans accent confirmées : « attribue à Fleuret » (sic) détecté.

## Cycle v1 — Recomptage après reformulation (2026-07-04)

| Agrégat | v0 | v1 | Δ |
|---|---|---|---|
| Au moins un marqueur de doute | 29 726 | **25 220** | −4 506 (bruit retiré) |
| — taux base entière / avec auteur | 2,90 % / 3,53 % | **2,46 % / 2,99 %** | |
| attribué à | 18 008 | 17 926 | −82 (doctrine « attribué, d'après ») |
| ? | 2 731 | 2 213 | −518 (dates `(?-1996)`) |
| école de | 2 865 | 2 093 | −772 (écoles nationales inversées) |
| atelier (qualificatif) | 5 558 | **1 759** | la famille la plus corrigée |
| Atelier de X en nom d'auteur (écarté) | — | 1 123 | population chiffrée à part |

Le périmètre beaux-arts concentre 21 161 des 25 220 doutes (83,9 %).
Peinture : 5,33 % de taux de doute (v0 : 6,00 %).

## P2-T1 — Recouvrements entre catégories (2026-07-05)

Source : `src/count_overlaps.py` → `data/exports/recouvrements.json`.

**66 911 notices (6,54 % de la base) portent au moins un marqueur**, toutes
catégories confondues. Répartition (chaque notice comptée une seule fois) :

| Combinaison | Notices |
|---|---|
| révision seule | 19 873 |
| doute seul | 19 690 |
| copie seule | 19 279 |
| **doute + révision** | **4 724** |
| copie + révision | 2 539 |
| doute + copie | 672 |
| les trois | 134 |

Contrôle de cohérence : 19 690 + 4 724 + 672 + 134 = 25 220 = total doute v1 ✓.

Constats :
- **Près d'1 doute sur 5 (19 %) porte aussi une ancienne attribution** : la
  notice dit à la fois « on n'est pas sûr » et « on a déjà changé d'avis ».
  Ce croisement est peut-être la matière narrative la plus riche du projet.
- Les co-occurrences entre familles de doute sont marginales (max :
  attribué × ? = 128 notices) — les familles sont presque disjointes, la
  ventilation par famille est donc saine.
- Les trois catégories ont des poids étonnamment proches (~19-20 000 chacune
  en exclusif) : trois récits d'égale ampleur.

## T5 — Pièges confirmés par la vérification manuelle (2026-07-04)

206 lignes jugées par l'utilisateur (176 vrai / 28 faux / 2 incertain).
Classes de faux positifs identifiées par ses commentaires :

1. **Ateliers de production donnés comme auteurs assumés** : `Atelier de
   Pistillus`, `ATELIER DU CENTRE DE LA GAULE (céramiste)`, `Atelier du jubé
   de la cathédrale de Strasbourg` — l'atelier EST l'auteur, aucun doute.
2. **Studios d'imprimeurs/photographes** : `Ateliers de reproductions
   artistiques`, `Moulin (Atelier photographique)`.
3. **Mentions biographiques dans Precisions_sur_l_auteur** : « entra dans
   l'atelier de formation… », « il est un des suiveurs du Pérugin » — la bio
   parle du parcours de l'artiste, pas de l'attribution de l'œuvre.
4. **École nationale sous forme inversée** : `Hollande École de (École
   hollandaise)` dans le champ Auteur — c'est le piège « école française »
   de T1, sous un déguisement inattendu. Signal d'exclusion : la parenthèse
   `(École …)` qui suit.
5. **`?` de date de naissance** : `(?-1996)` — la correction T3 n'excluait que
   les chiffres avant le `?`, pas après.
6. **« présumé » sur une autre œuvre citée en bio** : « on lui attribue aussi
   un portrait présumé de son époux ».
7. Les faux positifs arrivent **en grappes** : un même auteur mal formaté
   (Der Balian Sarkis) = toutes ses œuvres fausses. Corriger un motif élimine
   des grappes entières.
8. Curiosité à documenter : `anonyme (attribué)` — « attribué à… anonyme »
   (traité en « incertain », hors calcul, décision utilisateur).

## Pièges métier connus (à vérifier sur les données réelles)

- « présumé » porte souvent sur le **sujet représenté** (« portrait présumé de X »),
  pas sur l'auteur → source de faux positifs, garde-fou prévu dans le détecteur.
- « d'après X » = le plus souvent copie assumée d'après un modèle → classé à part.
- Graphies multiples attendues (« attribué à », « attr. », « ? »…) : saisies par
  des musées différents sur des décennies.
- **`Ecole_pays` : « école française » = nationalité, pas un doute** (précision
  utilisateur, 2026-07-03). Le marqueur de doute « école de [artiste] » se trouve
  plutôt dans `Auteur`. Le détecteur (T3) devra distinguer « école de + nom
  d'artiste » (doute) de « école + adjectif de nationalité » (classification).
