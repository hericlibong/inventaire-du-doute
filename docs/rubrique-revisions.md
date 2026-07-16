# Rubrique « Avant / après » — cadrage V1 (2026-07-14)

> **⏸ EN RÉSERVE depuis le 2026-07-15 (recentrage).** Cette rubrique **ne fait
> plus partie du périmètre publiable initial** : la V1 publique est centrée sur le
> dossier « Les presque » (voir docs/roadmap.md, bloc « ★ RECENTRAGE », et
> decisions.md 2026-07-15 ter). Tout le travail décrit ci-dessous est **conservé
> en l'état** pour une reprise ultérieure ; `/revisions` est hors nav publique.

> **MISE À JOUR 2026-07-14 (ter) — FRONT V1 CONSTRUIT.** Bilan v2 et taxonomie
> à 7 catégories **validés** ; front V1 **simplifié** livré (décisions.md ter).
> Route `/revisions` : intro courte → 2 cartes exemples → **un seul** graphe
> (« Où mènent les anciennes attributions ? », les 7 catégories) → galerie de 32
> cartes groupées et filtrables → note de méthode. Écarts assumés vs ce cadrage :
> les autres graphes (§5 : daté/non daté, anciens noms, siècles, domaines) sont
> **différés / réservés à la page méthode** (choix utilisateur : pas de page
> dashboard) ; pas de ligne éditoriale par carte (verbatims seuls) ; direction
> inverse = **une phrase forte dans l'intro**, pas de graphe dédié. Libellé
> `meme_nom` = « Le même nom, avec réserve ». Composant `web/src/lib/CarteRevision.svelte`.

> **MISE À JOUR 2026-07-14 (bis) — après vérification manuelle.** Les listes de
> catégories des §3 et §5 ci-dessous (« 4 destinations ») sont **dépassées** :
> la vérification des 80 lignes a produit une **taxonomie v2 à 7 catégories**
> (voir docs/decisions.md 2026-07-14 bis et docs/donnees.md). Source de vérité
> du code : `src/revisions_classify.py` (+ `tests/test_revisions.py`). Le reste
> de ce cadrage (titre, images écartées, sélection par diversité, garde-fous,
> graphes classiques) reste valable. **État : bilan v2 en attente de validation
> utilisateur avant tout front.**

Cadrage éditorial, fonctionnel et méthodologique avant toute ligne de front.
Titre validé **provisoirement** : « Avant / après » (sous-titre non figé, à
retravailler plus tard — priorité au contenu). Décision de priorité :
docs/decisions.md (2026-07-13). Constats de données : docs/donnees.md
(2026-07-13 et 2026-07-14).

## Objectif

Montrer que certaines œuvres ont changé d'attribution dans les notices
Joconde : avant, un nom ; aujourd'hui, la notice dit autre chose. Ce
changement est le travail normal de recherche et de catalogage. **On ne juge
pas, on ne révèle pas une erreur : on montre ce que la notice conserve comme
trace.**

Texte de présentation (provisoire, non figé) :
> Une attribution n'est pas toujours figée. Dans certaines notices, les musées
> conservent l'ancien nom associé à une œuvre, puis l'attribution retenue
> aujourd'hui. Cette rubrique montre ces passages d'un nom à l'autre : parfois
> vers un autre artiste, parfois vers l'anonyme, parfois vers une formule plus
> prudente.
>
> Il ne s'agit pas de pointer des erreurs, mais de rendre visible le travail
> normal de révision des collections. Les exemples présentés reprennent les
> mots des notices Joconde : l'ancien nom, l'attribution actuelle, l'œuvre et
> le musée qui les conserve.

## 1. Base de tri — sur quoi on choisit les cas affichés

Refus explicite du tri par prestige seul (anti-sensationnalisme). Critères
retenus, par ordre de poids :

1. **Lisibilité** : ancienne attribution courte (≤ 85 car.) et **mono-segment**
   (pas de chaîne `A ; B ; C` illisible en carte) ;
2. **Ancien nom extractible** proprement (premier segment hors parenthèses,
   sans chiffre ni « ? » ni « école », 3–40 car.) ;
3. **Attribution actuelle claire** (un nom, un anonyme, une formule prudente) ;
4. **Titre présent** (obligatoire : sans titre, la carte ne se lit pas) ;
5. **Diversité des destinations** : quota par type de passage (voir §2) ;
6. **Diversité des musées** : **plafond 2 cas par musée** — c'est ce qui
   défait mécaniquement la concentration Louvre/dessins (testé : lot à 19 %
   de Louvre au lieu de 59,5 %) ;
7. Image POP disponible : **critère de départage seulement** (à cas égal, on
   préfère une œuvre illustrée sur POP), **jamais un critère d'inclusion** —
   voir §4, les images ne sont pas affichées en V1.

Le prestige de l'ancien nom **n'est pas** un critère de tri. Les grands noms
apparaissent parce qu'ils sont nombreux dans les anciennes étiquettes, pas
parce qu'on les met en avant.

## 2. Choix des œuvres — logique de sélection V1

Lot éditorial **réduit** (cible **32**, fourchette 24–40), réparti par
destination avec plafond 2/musée. Testé sur le corpus (script de sélection,
2026-07-14) :

| Destination (type de passage) | Candidats lisibles | Quota V1 |
|---|---|---|
| vers un autre artiste | 5 115 | 10 |
| vers l'anonyme | 2 262 | 8 |
| vers un autre artiste, encore prudent | 1 763 | 7 |
| vers une copie « d'après » | 890 | 7 |

Résultat mesuré : **32 cas, 10 musées, Louvre 19 %**, tous illustrés sur POP.
~10 000 candidats lisibles au total → large marge pour varier le lot.

- Cas ambigus **exclus de l'interface**, gardés pour la page méthode (chaînes,
  prose, écoles nationales — voir §8).
- **Pas d'exhaustivité dans l'interface** : les 26 667 vivent dans la section
  statistiques (§5), pas dans la galerie.

## 3. Organisation de la rubrique — **par type de passage** (recommandé)

Options évaluées :

| Organisation | Verdict |
|---|---|
| **par type de passage** (autre artiste / anonyme / prudent / copie) | **RECOMMANDÉ** : catégories propres, chiffrables, non sensationnalistes ; c'est le vrai sujet (« où mène la révision ») |
| par grand nom ancien | **repère secondaire** (filtre), jamais structure principale — sinon palmarès |
| par période | écarté comme structure : seulement 16 % d'œuvres datables, 7 % de révisions datées |
| par type d'œuvre | écarté : 63 % dessin, structure déséquilibrée |
| par musée | interdit comme structure (règle non négociable : pas de comparaison entre musées) |

**Recommandation = structure primaire par type de passage** (l'intuition
utilisateur est confirmée par les données), **grands noms en filtre
secondaire** au mot entier. Trois blocs :

1. **Intro** (texte provisoire ci-dessus) + divulgation en clair de la
   concentration (cabinets d'arts graphiques).
2. **Statistiques générales** sur tout le corpus (§5) — graphes classiques.
3. **Galerie « avant → aujourd'hui »** : le lot V1, groupé par type de
   passage, filtrable par ancien nom. Cartes : titre, musée + ville,
   **verbatim ancien entre guillemets**, **verbatim actuel entre guillemets**,
   année si datée, lien « Voir la fiche publique → » (POP).

## 4. Images — verdict : **pas d'affichage en V1** (vérifié le 2026-07-14)

Audit mené (champs CSV + test POP réel) :

- **Le CSV ne contient aucune URL d'image** ni chemin. Il porte
  `Presence_image` (booléen : **92 %** du corpus = « oui ») — un drapeau
  « une image existe », pas un droit d'usage.
- **POP affiche bien une image** : test sur la notice `000DE023183` — l'URL
  pointe vers un bucket S3 interne
  (`popcorn-prd-perf-assets.s3.gra.io.cloud.ovh.net/joconde/{ref}/…`).
- **Aucune mention de droits par œuvre** : POP affiche « Licence Etalab 2.0
  sauf mention contraire » en pied de site. La Licence Ouverte couvre les
  **métadonnées textuelles** de Joconde, **pas les photographies** : les
  droits des clichés reviennent le plus souvent à chaque musée (« mention
  contraire »).
- Conséquences : (a) construire l'URL image revient à **hotlinker un CDN
  gouvernemental interne** (instable, non prévu pour ça) ; (b) on ne peut pas
  **vérifier la licence œuvre par œuvre** sur 26 667 clichés, ce qu'exige
  notre règle (CLAUDE.md : toute image externe = source secondaire, licence
  vérifiée par fichier — précédent portraits, sourcés sur Wikimedia Commons).

**Décision V1 : carte textuelle, sans image, avec lien POP** (POP montre
l'image en contexte, avec les droits que le musée détient). Le verbatim des
deux attributions est la matière ; l'image est chez POP.

**Piste ultérieure (hors V1, manuelle)** : illustrer **une poignée** de cas
phares en sourçant l'image sur Wikimedia Commons, licence vérifiée fichier par
fichier (exactement le workflow des 27 portraits). À décider séparément ; ne
rien promettre avant sourcing.

## 5. Statistiques générales — graphes classiques uniquement

Section sur **tout le corpus** (26 667), même si la galerie est réduite.
Aucune visualisation expérimentale.

| Graphe | Forme | Données (vérifiées) |
|---|---|---|
| Où mène la révision | **barres horizontales** triées | autre artiste 14 036 · anonyme 5 824 · autre artiste prudent 4 559 · copie « d'après » 2 230 · composite/autre 146 |
| Datée / non datée | **donut** (binaire, adapté) | datée 1 907 (7,2 %) / non datée 24 760 |
| Types d'œuvre | **barres** | dessin 63,5 % · peinture 23,8 % · beaux-arts 5,3 % · arts déco 2 % · sculpture 1,4 % … |
| Anciens noms fréquents | **barres**, top ~15, **mot entier** | Vinci 511 · Poussin 350 · Rubens 236 · Rembrandt 227 · Le Brun 115 · Fragonard 114 · Watteau 107 … + caveat « filtre, pas palmarès » |
| Siècle de l'œuvre | **colonnes** | 16 % datables (4 375) ; concentrées 16ᵉ–18ᵉ (966 / 1 239 / 1 111) + caveat couverture |
| Concentration musée | **une phrase + une barre** | Louvre 59,5 % · dessin 62,9 % ; divulgué, jamais comparé |

Chiffres racontés en français dans le texte d'accompagnement (« une fois sur
trois, le nouveau nom est plus prudent que l'ancien », « la révision n'est pas
qu'une affaire du XIXᵉ siècle »).

## 6. Export dédié : `data/exports/web/revisions.json`

Produit par un futur `src/build_revisions.py` (même facture que
build_artistes.py : invariants vérifiés par `assert`).

```
{
  "provenance": { ...bloc commun aux exports... },
  "totaux": {
    "revisions": 26667,
    "destinations": { "autre_nom":14036, "anonyme":5824,
                      "autre_nom_doute":4559, "copie_dapres":2230,
                      "autre":146 },
    "datees": 1907, "non_datees": 24760,
    "part_louvre": 0.595, "part_dessin": 0.629, "n_musees": 146,
    "vers_un_nom": <direction inverse anonyme→nom, à chiffrer>
  },
  "domaines":  [ { "label":"dessin", "n":16933 }, ... ],
  "siecles":   [ { "siecle":16, "n":966 }, ... ],       // œuvres datables
  "anciens_noms": [ { "id":"vinci", "label":"Léonard de Vinci", "n":511,
                      "destinations": { ... } }, ... ], // top ~15, mot entier
  "cas": [                                              // LOT V1 réduit (~32)
    { "reference":"000DE023183",
      "titre":"Tête d'étude", "musee":"musée Crozatier", "ville":"Le Puy-en-Velay",
      "ancienne_brut":"VINCI LEONARD DE (ancienne attribution)",
      "auteur_brut":"anonyme",
      "ancien_nom":"Léonard de Vinci",       // extrait fiable, sinon null
      "destination":"anonyme",
      "annee": null,                          // 1836… si datée fiable
      "domaine":"dessin",
      "image_presente": true }                // métadonnée ; NON affichée en V1
  ]
}
```

`image_presente` est conservé par honnêteté (drapeau POP), **non utilisé pour
l'affichage** en V1. La `Ville` est remplie à 100 %, le `Titre` à 96,5 %.

## 7. Règles de comparaison avant/après (méthodo, publiable)

1. **La présence du champ est le marqueur** ; la comparaison ne sert qu'à
   écarter les redites où le champ répète l'auteur actuel (~1 %).
2. Normalisation : parenthèses retirées, casse ignorée. « Différent » =
   chaînes normalisées différentes. Jamais de rapprochement flou.
3. Rattachement à un nom vedette : **mot entier** (frontières non
   alphabétiques) — règle héritée de SERODINE/RODIN. Vérifié : « ÉCOLE
   CARAVAGESQUE » ne compte pas pour Caravage.
4. Extraction d'un nom lisible : premier segment hors parenthèses ; **refusée**
   si chiffre, « ? », « école » ou > 40 car. → le cas garde son verbatim.
5. Noms proches **jamais fusionnés** : WILLE père → WILLE fils = vraie
   révision ; PRIMATICE → PRIMATICCIO = graphie. On affiche, on ne juge pas.
6. Chaînes (≥ 2 segments) : **exclues de la galerie V1** (lisibilité),
   comptées dans les totaux ; **le dernier segment peut être l'attribution
   actuelle** (Bellechose, Louvre) → comparaison segment par segment.
7. Direction inverse (anonyme → un nom) : **chiffrée** au pipeline, pas
   découverte par le lecteur.

## 8. Contrôles qualité obligatoires (avant tout front)

1. **Tests mot entier** figés (cas : ÉCOLE CARAVAGESQUE ≠ CARAVAGE ; « attribu »
   borné par `\b` pour ne pas matcher « attribution »).
2. **Échantillon stratifié** (~60–80 lignes) pour vérification manuelle
   utilisateur, croisant destinations × formats (anonymes, noms proches,
   chaînes, écoles nationales, datées, prose) — CSV tableur verdict/commentaire.
3. **Verdicts figés en tests automatiques** après retour.
4. **Invariants `assert`** : partition des destinations = 26 667 ; aucun cas
   embarqué sans référence POP ; plafond 2/musée respecté.

## 9. Garde-fous éditoriaux

- **Registre** : « la notice a porté le nom de X ; elle dit aujourd'hui Y ».
  Jamais « déchu », « démasqué », « erreur ».
- **Le champ est la preuve du travail, pas de la faute** : c'est le musée qui
  garde la trace ; certaines anciennes attributions sont des propositions de
  catalogues savants (« CAT. 1938 »), pas des affirmations du musée.
- **Pas de palmarès** : les noms vedettes = un filtre au mot entier, jamais un
  classement. L'intro explique le biais d'attraction (les inventaires anciens
  donnaient volontiers aux grands noms ; le travail moderne resserre).
- **Concentration divulguée** (Louvre/dessins), jamais comparée.
- **Verbatims seuls** : les deux formules exactes entre guillemets ; aucun
  avant/après reconstruit quand l'extraction n'est pas fiable.
- 23,1 % des anciennes attributions portaient **déjà** un doute : l'« avant »
  n'était pas un verdict — le verbatim empêche de le durcir.

## 10. Prototypes — 10 cartes lisibles (verbatim réels, lot testé)

Gabarit : *[Titre]* — [musée], [ville]. A porté : « [verbatim ancien] ».
Aujourd'hui : « [verbatim actuel] ».

1. *Tête d'étude* — Crozatier, Le Puy-en-Velay. « VINCI LEONARD DE (ancienne
   attribution) » → « anonyme ». *(vers l'anonyme)*
2. *Portrait de Mme Adélaïde de France* — Condé, Chantilly. « LA TOUR MAURICE
   QUENTIN DE (ancienne attribution) » → « VALADE Jean ». *(autre artiste)*
3. *Le Serment des Horaces* — beaux-arts, Rennes. « DAVID LOUIS, ECOLE DE
   (ancienne attribution) » → « CARAFFE Armand Charles ». *(autre artiste)*
4. *Nature morte, coq et poule* — Tessé, Le Mans. « HONDECOETER MELCHIOR DE
   (CAT 1932) » → « VALLAYER-COSTER Anne ». *(autre artiste)*
5. *Saint Jérôme lisant* — Louvre, Paris. « LA TOUR GEORGES DE (attribué en
   1972) » → « anonyme ; LA TOUR Georges de (d'après) ». *(copie ; datée 1972)*
6. *Le Sommeil des Amours* — Louvre, Paris. « BOUCHER FRANCOIS (BRIERE) » →
   « Boucher François (atelier) ». *(prudent : de la main au atelier)*
7. *Anne d'Autriche en Sagesse* — Versailles. « CHAMPAIGNE (attribué en 1832) »
   → « SEVE Gilbert de (attribué) ». *(autre artiste, encore prudent)*
8. *Assaut de la Grenade* — franco-américain, Blérancourt. « WILLE JEAN
   GEORGES (ancienne attribution) » → « WILLE Pierre Alexandre ». *(du père au
   fils : même famille)*
9. *Cérès* — Magnin, Dijon. « PRIMATICCIO (CAT. 1938) » → « PRIMATICCIO
   Francesco (d'après) ; anonyme ». *(le même nom passe en « d'après »)*
10. *Portrait de la marquise de Pompadour* — beaux-arts, Caen. « COURNERIE
    Louis (ancienne attribution) » → « Boucher François (d'après) ».
    *(copie : le nom monte d'un cran, mais en modèle copié)*

## 11. Cas ambigus — exclus de la galerie, réservés à la page méthode

1. Prose/chaîne longue : « PATEL LE PERE (CAT. 1860) ; … ; …, D'APRES (CAT.
   1876) ; … » — 5 segments, illisible en carte.
2. « OUDRY (attribué en 1869) ; … (1912) ; … (BRIERE) ; … (1930) » → BOYER
   (Louvre) — chronologie riche mais dense.
3. « ECOLE FRANCAISE 17E SIECLE (INVENTAIRE) » → Natoire — l'« avant » n'est
   pas un nom, pas d'extraction.
4. « ECOLE LOMBARDE, ?, PREMIER TIERS 16E SIECLE (CAT. 1938) » → Corenzio —
   non-nom + « ? » dans l'ancien.
5. « ECOLE DE FERRARE (CAT. 1922) ; ITALIE DU NORD… » → anonyme — chaîne de
   non-noms.
6. « ATTRIBUTION FAITE PAR BENJAMIN COUILLEAUX EN 2012 » — prose pure.
7. « ANCIENNES ATTRIBUTIONS : COPIE D'APRÈS SANTI RAFFA… » — prose + pollution
   sous-chaîne (VINCI) si l'on n'était pas au mot entier.
8. « MARTIN JEAN BAPTISTE, D'APRES (CAT 1932) » → « anonyme ; VAN DER MEULEN
   (d'après) ; LE BRUN (d'après) » — déjà copie (1 198 cas) : avant/après de
   copiste, pas d'auteur.
9. « BOULLONGNE LOUIS DE (SUPPL. TAUZIA) ; … (BRIERE) » → « BOULLOGNE Bon » —
   noms quasi identiques (graphies + fratrie), illisible sans expertise.
10. « … BELLECHOSE HENRI (BRIERE) ; BELLECHOSE HENRI (attribué en 1949) » →
    « BELLECHOSE Henri » — le dernier segment EST l'attribution actuelle : un
    avant/après naïf serait faux.
