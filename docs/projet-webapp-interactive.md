# Projet connexe — Webapp interactive de L'inventaire du doute

**Statut : cadrage pour un futur projet, à lancer après la publication du site actuel.**  
**Date de décision : 2026-08-09.**

Cette note prépare la création d'un projet séparé qui réutilisera les données fiabilisées
de **L'inventaire du doute** pour construire une véritable webapp d'exploration. Elle ne
fait pas partie des phases F5 à F7 et ne doit pas retarder la publication du Volume 1.

---

## 1. Pourquoi créer un second projet

Le projet actuel a évolué vers un **site éditorial de données interactif**. Il présente le
sujet, expose la méthode, publie les résultats par volumes et propose un outil d'exploration
des artistes. Cette forme est cohérente et doit être menée jusqu'à sa publication.

L'objectif initial était toutefois plus proche d'une **webapp interactive** : une interface
centrée sur l'action, la recherche, les filtres, les comparaisons et la circulation directe
entre artistes, œuvres, formulations et musées.

Il ne faut plus transformer le site actuel pour lui faire remplir ces deux fonctions. Les
deux produits auront des rôles complémentaires :

| Produit | Fonction principale |
| --- | --- |
| Site éditorial actuel | Présenter le projet, publier les volumes, expliquer la méthode et donner un cadre de lecture. |
| Future webapp | Explorer, filtrer, comparer et interroger les données de manière intensive. |

Le second projet n'annule donc pas le premier. Il s'appuie sur son travail de recherche et
offre une autre porte d'entrée dans les mêmes données.

## 2. Principe non négociable : une seule source de vérité

La webapp ne doit pas recopier ni réécrire le pipeline de données.

Le dépôt actuel reste propriétaire de :

- la collecte et la lecture de Joconde ;
- la détection des formulations prudentes ;
- les règles de comptage et de déduplication ;
- l'identification des artistes, alias, homonymes et exclusions ;
- la classification dans les huit mentions ;
- les contrôles, témoins réels et tests de non-régression ;
- les crédits, licences et correspondances d'images validées ;
- la génération des exports publics.

La webapp doit seulement **consommer des exports validés et versionnés**. Elle ne doit pas
relire le CSV Joconde, reproduire les expressions régulières, maintenir une seconde liste
d'artistes ni recalculer ses propres totaux.

Toute correction de données est d'abord faite et testée dans le dépôt source, puis propagée
à la webapp par une nouvelle version des exports.

## 3. Contrat de données à préparer

Avant de construire l'interface, il faudra transformer les exports existants en un contrat
explicite. Le nom actuel des fichiers n'est pas encore un contrat : leur structure doit être
documentée, testée et versionnée.

Le contrat minimal devra couvrir :

1. **Manifeste du jeu de données**
   - version du contrat ;
   - date de génération ;
   - version de la source Joconde ;
   - effectifs globaux ;
   - licence et provenance.

2. **Répertoire des artistes**
   - identifiant stable et slug ;
   - nom public et noms de référence ;
   - informations biographiques validées ;
   - portrait et crédit éventuels ;
   - totaux utiles au tri et au filtrage.

3. **Profil d'un artiste**
   - répartition par mention ;
   - dénominateurs et pourcentages ;
   - musées concernés ;
   - informations nécessaires aux graphiques.

4. **Œuvres concernées**
   - référence Joconde stable ;
   - titre reproduit tel que publié ;
   - formulation et mention classée ;
   - musée et code Muséofile ;
   - lien POP ;
   - reproduction locale, source, crédit et licence lorsqu'elle est autorisée.

5. **Musées**
   - identifiant stable ;
   - nom et ville ;
   - coordonnées ;
   - effectifs par artiste et par mention.

6. **Vocabulaire public**
   - les huit codes stables ;
   - libellés, définitions et couleurs ;
   - regroupement dans les trois territoires.

Chaque export devra être validé par un schéma ou des assertions. Un changement incompatible
entraînera une nouvelle version du contrat au lieu d'une modification silencieuse.

### Mode de partage recommandé pour le premier prototype

Commencer simplement : un script de synchronisation exécuté au build copie les exports
versionnés du dépôt source vers le projet de la webapp et vérifie leur manifeste. Cette
solution convient à une publication statique, évite un backend prématuré et garde une trace
de la version réellement publiée.

Une API ou un paquet partagé ne sera envisagé que si plusieurs consommateurs, des mises à
jour très fréquentes ou des volumes de données plus importants le justifient.

## 4. Expérience recherchée

La première vue doit être l'outil utilisable, pas une nouvelle page de présentation. Le site
éditorial remplit déjà cette fonction.

La webapp devra privilégier :

- une recherche immédiatement disponible ;
- des filtres visibles et combinables ;
- des résultats mis à jour sans rechargement ;
- une navigation directe entre artistes, œuvres et musées ;
- la comparaison de plusieurs profils ;
- un état partageable par URL ;
- des vues denses mais lisibles sur ordinateur ;
- une adaptation mobile pensée comme une interface, pas comme la réduction du bureau ;
- un usage complet à la souris, au clavier et au toucher ;
- des explications courtes et contextuelles plutôt que de longs chapitres.

Les données doivent rester attribuées à Joconde et les limites méthodologiques doivent être
accessibles, mais elles ne doivent pas interrompre chaque interaction.

## 5. Premier périmètre fonctionnel proposé

Le MVP doit démontrer un parcours complet plutôt qu'accumuler des graphiques.

### Parcours principal

1. Chercher ou sélectionner un artiste.
2. Lire immédiatement son profil de formulations.
3. Filtrer ses œuvres par mention et par musée.
4. Ouvrir une œuvre et retrouver sa notice POP.
5. Sélectionner un musée et voir les œuvres concernées qu'il conserve.
6. Comparer le profil de deux ou trois artistes.
7. Copier l'URL pour retrouver ou partager exactement cet état.

### Fonctions du MVP

- répertoire recherchable et filtrable ;
- profil interactif d'un artiste ;
- liste paginée ou virtualisée des œuvres ;
- filtres croisés mention × musée ;
- carte reliée aux résultats ;
- comparaison de profils sur une même échelle ;
- panneau de détail d'une œuvre ;
- URL contenant la sélection, les filtres et la vue active ;
- états de chargement, absence de résultat et absence d'image ;
- aide contextuelle sur les huit mentions.

### Hors MVP

- comptes utilisateurs et favoris synchronisés ;
- annotations collaboratives ;
- modification des données ;
- authentification d'œuvres ;
- backend spécifique sans besoin démontré ;
- intégration immédiate de tous les futurs volumes ;
- visualisations ajoutées uniquement parce que les données le permettent.

## 6. Architecture technique recommandée au démarrage

- **Projet séparé**, dans un nouveau dossier et idéalement un nouveau dépôt Git.
- **SvelteKit** peut être conservé : l'équipe connaît déjà la pile et les composants utiles
  pourront être réinterprétés sans copier toute l'interface actuelle.
- **Déploiement statique** pour le premier prototype, si le volume des exports le permet.
- **État d'interface dans l'URL** pour les sélections partageables.
- **Chargement par vue ou par artiste** plutôt qu'un unique fichier contenant tout le détail.
- **Schémas et tests de contrat** à la frontière avec les exports.
- **Tests d'interaction** sur les parcours principaux, en plus des tests unitaires.

Nom de dossier de travail possible : `inventaire-du-doute-app`. Le nom public devra être
tranché séparément ; il peut rester rattaché à L'inventaire du doute sans reproduire le titre
du Volume 1.

## 7. Direction visuelle

La webapp peut reprendre l'identité du projet sans reproduire sa mise en page éditoriale :

- mêmes familles typographiques et palette de base ;
- mêmes couleurs stables pour les huit mentions ;
- même exigence sur les crédits et la provenance ;
- interface plus dense, avec davantage d'espace consacré aux données ;
- panneaux, filtres, sélecteurs et comparateurs conçus comme des outils ;
- textes d'aide courts, accessibles à la demande ;
- aucune obligation de conserver l'affiche plein écran ou la structure en chapitres.

Le nouveau projet doit commencer par des parcours et des maquettes fonctionnelles. Il ne
doit pas dériver de la page actuelle par une simple refonte CSS.

## 8. Relation entre les deux publications

À terme :

- le site éditorial peut proposer un accès « Explorer les données » vers la webapp ;
- la webapp peut renvoyer vers « Comprendre le projet et la méthode » sur le site ;
- chaque produit possède ses propres URL, métadonnées et navigation ;
- ils partagent la même version déclarée des données, mais pas nécessairement le même rythme
  de publication ;
- un volume éditorial peut introduire un nouvel angle avant son intégration dans la webapp.

## 9. Risques à éviter

- maintenir deux pipelines qui finissent par produire des chiffres différents ;
- copier les composants actuels avant d'avoir défini les nouveaux usages ;
- transformer la webapp en catalogue de graphiques sans parcours clair ;
- charger les données des 102 artistes et toutes leurs œuvres dès le premier écran ;
- employer « œuvre » et « notice » sans conserver les unités réelles dans le contrat ;
- laisser l'interface produire une interprétation plus affirmative que les données Joconde ;
- faire dépendre les couleurs seules de la compréhension ou de l'interaction ;
- commencer le développement avant d'avoir stabilisé les URL d'état et le MVP.

## 10. Plan de lancement du nouveau projet

### Étape 0 — Clore le site actuel

- terminer F5, F6 et F7 ;
- publier le Volume 1 ;
- noter la version exacte des exports utilisée en production.

### Étape 1 — Cadrage produit

- écrire trois à cinq scénarios d'usage concrets ;
- définir les utilisateurs prioritaires ;
- arrêter le MVP et ses non-objectifs ;
- choisir le nom, l'adresse et la relation visible avec le site éditorial.

### Étape 2 — Contrat de données

- inventorier les exports actuels ;
- supprimer les dépendances à leur organisation historique ;
- définir manifeste, schémas, version et tests ;
- créer la commande de synchronisation vers la webapp.

### Étape 3 — Prototype d'un parcours

- utiliser un petit échantillon représentatif d'artistes ;
- prototyper sélection → profil → filtres → œuvre → musée ;
- vérifier l'URL partageable, le clavier et le mobile dès ce stade ;
- valider le parcours avant de généraliser les composants.

### Étape 4 — Comparaison et montée en charge

- ajouter la comparaison de profils ;
- charger les données à la demande ;
- mesurer les performances avec les exports complets ;
- décider seulement alors si un backend est nécessaire.

### Étape 5 — Publication

- tests fonctionnels et d'accessibilité ;
- vérification des chiffres contre les exports sources ;
- métadonnées, crédits, licences et méthode ;
- liens réciproques avec le site éditorial.

## 11. Décisions à prendre lors de l'ouverture du projet

1. Qui utilise prioritairement la webapp : grand public, chercheurs, professionnels des
   musées, enseignants, ou plusieurs publics avec des niveaux d'interface différents ?
2. Quelle action doit être possible dans les dix premières secondes ?
3. La comparaison porte-t-elle d'abord sur les artistes, les musées ou les formulations ?
4. Le premier prototype reste-t-il limité au Volume 1 ?
5. Quel état doit pouvoir être partagé par URL ?
6. Le projet garde-t-il le nom « L'inventaire du doute » avec un sous-titre fonctionnel ?
7. Quel hébergement et quel processus publient les exports versionnés ?

## 12. Critère de départ

Le développement de la webapp peut commencer lorsque les éléments suivants existent :

- le site actuel est publié ;
- un scénario principal est validé ;
- le MVP tient sur une page ;
- le contrat de données possède une première version ;
- un échantillon d'exports est synchronisable ;
- la frontière entre calcul source et affichage est écrite ;
- le prototype peut être évalué sans rouvrir les règles de classification.

Cette note doit être copiée ou liée dans le README du nouveau dépôt au moment de sa création.
Elle constitue un cadrage initial, pas une spécification figée : les usages pourront évoluer,
mais la source unique des données et la séparation entre les deux produits devront rester
stables.
