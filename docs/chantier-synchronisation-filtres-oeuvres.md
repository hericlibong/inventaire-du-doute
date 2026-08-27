# Mini-chantier — synchroniser les filtres « formulation » et « musée »

**Statut : spécification validée, à implémenter.**

## 1. Problème constaté

Dans l’onglet **Œuvres** de la page Artistes, les puces de formulation filtrent
correctement les œuvres affichées, mais le menu des musées continue d’être
calculé sur la totalité des œuvres de l’artiste.

Exemple vérifié avec Charles Le Brun :

- l’état initial porte sur **310 œuvres** ;
- « Attribué à » porte sur **52 œuvres** ;
- « Nom suivi d’un « ? » » porte sur **2 œuvres** ;
- malgré ces sélections, le menu « Musée » conserve aujourd’hui les musées et
  les effectifs des 310 œuvres.

Le menu donne donc un périmètre différent de la liste qu’il est censé filtrer.

## 2. Résultat attendu

Les filtres « formulation » et « musée » doivent être synchronisés.

Quand une formulation est choisie :

1. les œuvres affichées restent filtrées comme aujourd’hui ;
2. le menu ne propose plus que les musées présents dans ces œuvres ;
3. l’effectif de chaque musée est recalculé dans ce périmètre ;
4. l’option générale annonce le nombre de musées disponibles et le nombre
   d’œuvres correspondant à la formulation.

Exemples de libellés attendus :

- état initial : `Tous les musées (N) — 310 œuvres` ;
- « Attribué à » : `Tous les musées (N) — 52 œuvres` ;
- « Nom suivi d’un « ? » » : `Tous les musées (N) — 2 œuvres`.

`N` est toujours le nombre réel de musées proposés dans le menu pour le
périmètre courant. L’accord doit être correct pour `1 musée` / `N musées` et
`1 œuvre` / `N œuvres`. Une œuvre sans `musee_code` reste comprise dans le total
des œuvres, mais ne doit pas créer une fausse entrée de musée.

Quand un musée est ensuite choisi, la liste d’œuvres affiche l’intersection du
musée et de la formulation. Les puces de formulation continuent, comme
aujourd’hui, à être calculées dans le périmètre du musée sélectionné.

## 3. Règle de calcul

Il ne faut pas appliquer une simple chaîne de filtres dans laquelle chaque
commande serait calculée à partir du résultat final. Chaque commande doit être
calculée dans le contexte de l’autre :

- **options du menu des musées** : œuvres filtrées par la formulation active,
  sans appliquer le musée actif ;
- **puces de formulation** : œuvres filtrées par le musée actif, sans appliquer
  la formulation active ;
- **liste finale** : œuvres satisfaisant les deux sélections.

Ainsi, chaque filtre reste utilisable pour changer de choix et aucun filtre ne
se masque lui-même.

## 4. Compatibilité entre les choix

Lors d’un changement de formulation :

- conserver le musée sélectionné s’il possède au moins une œuvre correspondant
  à la nouvelle formulation ;
- sinon, remettre automatiquement le musée sur « Tous les musées » ;
- revenir à la première page et conserver le recentrage/focus existant.

Lors d’un changement de musée :

- conserver la formulation si elle existe dans ce musée ;
- sinon, la relâcher comme le fait déjà `choisirMusee` ;
- revenir à la première page et conserver le recentrage/focus existant.

Le bouton « Toutes » retire seulement la formulation. Il ne doit pas retirer un
musée encore sélectionné. La commande existante qui retire tous les filtres doit
continuer à retirer les deux.

## 5. Périmètre technique pressenti

Le défaut se trouve principalement dans
`web/src/lib/OeuvresMaitre.svelte` : `musees` dérive actuellement de toutes les
`oeuvres`, alors qu’il doit dériver du sous-ensemble correspondant à
`familleActive`.

`web/src/lib/ChoixMusee.svelte` doit rester un composant de présentation. Une
petite adaptation de ses propriétés ou de son libellé est admise pour afficher
`Tous les musées (N)` ; aucune seconde logique de filtrage ne doit y être créée.

Conserver impérativement :

- `museeActif` partagé avec la page et la carte de l’onglet Musées ;
- le chargement à la demande des œuvres ;
- l’ordre actuel des œuvres et des formulations ;
- la pagination et son recentrage accessible ;
- le comportement clavier et les attributs ARIA de `ChoixMusee` ;
- le rendu responsive existant.

Éviter de dupliquer les parcours et regroupements si une petite fonction pure
rend les trois périmètres explicites et testables.

## 6. Cas de validation

Vérifier au minimum :

1. **Charles Le Brun, aucun filtre** : 310 œuvres ; tous ses musées sont proposés
   avec leurs effectifs complets.
2. **Charles Le Brun, « Attribué à »** : 52 œuvres ; seuls les musées de ces 52
   œuvres sont proposés ; chaque effectif est celui de ce sous-ensemble.
3. **Charles Le Brun, « Nom suivi d’un « ? » »** : 2 œuvres ; seuls leur ou leurs
   musées sont proposés.
4. Choisir ensuite un musée : la liste présente exactement l’intersection des
   deux choix.
5. Passer à une formulation compatible : le musée reste sélectionné.
6. Passer à une formulation incompatible : le musée revient à « Tous les
   musées », sans état vide incompréhensible.
7. Avec un musée actif, choisir « Toutes » : toutes les formulations de ce musée
   réapparaissent, sans perdre le musée.
8. Changer d’artiste : les filtres et les effectifs repartent dans l’état prévu
   par le comportement actuel.
9. Ouvrir et utiliser le menu au clavier : aucune régression de focus, de
   sélection ou d’annonce accessible.
10. Contrôler le singulier avec un périmètre ne comprenant qu’un musée ou une
    œuvre.

Les nombres affichés doivent être issus des données, jamais écrits en dur. Les
tests existants doivent rester au vert ; ajouter des tests ciblés sur le calcul
des périmètres si la logique est extraite dans une fonction pure.

## 7. Livraison demandée

Après implémentation :

1. lancer les tests Python et front pertinents ;
2. lancer le build avec le sous-chemin de publication habituel ;
3. ouvrir un serveur local de prévisualisation du build ;
4. contrôler visuellement les cas Charles Le Brun ci-dessus, sur écran large et
   sur une largeur mobile ;
5. fournir le résumé des fichiers modifiés, des contrôles effectués et de leurs
   résultats ;
6. laisser la modification non commitée pour relecture de la diff.

