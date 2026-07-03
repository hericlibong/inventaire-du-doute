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

## Pièges métier connus (à vérifier sur les données réelles)

- « présumé » porte souvent sur le **sujet représenté** (« portrait présumé de X »),
  pas sur l'auteur → source de faux positifs, garde-fou prévu dans le détecteur.
- « d'après X » = le plus souvent copie assumée d'après un modèle → classé à part.
- Graphies multiples attendues (« attribué à », « attr. », « ? »…) : saisies par
  des musées différents sur des décennies.
