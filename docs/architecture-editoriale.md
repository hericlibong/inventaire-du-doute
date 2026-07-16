# Architecture éditoriale — dossier « Les presque »

Note de direction consolidée le **2026-07-16**, à partir d'une note d'évaluation
externe et des précisions de l'utilisateur. **Statut : cadrage à valider avant
toute implémentation.** Aucune ligne de front n'est modifiée par ce document.

Le constat de départ : la charte graphique (couleurs, typographies, coquille) est
désormais cohérente. Ce qui manque, ce n'est plus de la charte, c'est une
**direction artistique** et une **architecture éditoriale**. L'application se lit
encore comme une succession de blocs fonctionnels — « une base, un filtre, des
graphiques » — au lieu d'une **publication** : *entre la main d'un maître et son
influence la plus lointaine, les musées ont inventé tout un langage de la
prudence ; voici comment il se déploie.*

Cadre du projet : **L'inventaire du doute**. Dossier publié : **Les presque**.

## 1. Principe directeur

- **Une publication éditoriale, pas une suite de pages identiques.** L'accueil,
  l'exploration et la méthode n'ont pas le même rôle et ne doivent pas se
  ressembler.
- **Un principe visuel central** organise tout : *la distance à la main du
  maître* (voir §5). Il donne sa personnalité au projet, bien plus qu'un
  énième réglage de palette.
- **Hiérarchiser l'ambition** : d'abord la promesse et le sujet, ensuite les
  preuves (chiffres) et les réserves (méthode) — pas l'inverse.

## 2. Navigation publique recentrée

Quatre entrées réellement actives, reflétant immédiatement le recentrage :

1. **Accueil**
2. **Explorer les maîtres**
3. **Comprendre les mentions**
4. **Méthode**

- Les rubriques en réserve (Avant / après, L'échelle du doute, La carte) **ne
  figurent plus dans la navigation publique** tant qu'elles ne sont pas intégrées
  à la publication recentrée (elles restent dans le projet de recherche).
- Fin des entrées grisées « à venir » en nav publique : elles font croire à une
  application inachevée.
- **« Vue d'ensemble » n'est PAS une entrée de menu** : elle vit à l'intérieur de
  « Comprendre les mentions » (voir §3), comme le contraste chiffré du vocabulaire.
- Libellés de menu proposés (« Explorer les maîtres », « Comprendre les
  mentions ») et framing « L'inventaire du doute / Les presque » : **à confirmer**
  (le choix des titres reste ouvert, décision différée).

## 3. Rôle de chaque page

### Accueil — une couverture éditoriale (pas la 1re page d'un rapport)

L'accueil doit d'abord **faire ressentir le sujet**, pas exposer le traitement des
données. Composition asymétrique pressentie :
- à gauche : le titre + une **promesse courte** + **un seul** appel à l'action ;
- à droite : l'**illustration Joconde traitée en figure de données** (voir §6),
  occupant une grande part de l'écran ; quelques lignes graphiques traversant/
  encadrant le texte.

Contenu (exemple, à affiner) :
> **L'inventaire du doute — Les presque**
> Une exploration des œuvres que les musées rapprochent d'un grand maître sans les
> lui attribuer tout à fait.
> **Explorer les 27 maîtres →**
>
> phrase secondaire : « attribué à », « atelier de », « école de », « manière
> de » : les mots changent à mesure que l'œuvre s'éloigne de la main du maître.

- Le **grand nombre global (24 507)** ne domine plus le premier écran : il vient
  **plus bas / en bandeau secondaire**, comme preuve, pas comme sujet.
- L'**exception des 5 791 notices de Nice** est trop technique pour l'accueil →
  elle part en **Méthode** (ou en note accessible depuis le chiffre).
- L'accueil doit **prendre possession de l'écran** (fin de la colonne étroite qui
  laisse la page vide autour et le contenu comprimé dedans).

### Explorer les maîtres — répertoire ↔ profil

Séparer nettement **présenter le dossier** et **fournir l'outil**. En-tête court :
> **Explorer les maîtres** — Vingt-sept noms pour lesquels Joconde conserve au
> moins vingt œuvres accompagnées d'une formule de réserve.

Puis une structure **maître–détail en deux zones franches** (voir §4).

### Comprendre les mentions — le langage de la prudence

Chapitre **autonome**, non rattaché à un seul artiste, consacré au **vocabulaire
muséal** (les 8 formules) et à sa lecture. Il absorbe :
- ce qui est aujourd'hui une **longue légende permanente** sous la liste (elle
  n'a plus à vivre collée au répertoire) ;
- la **« Vue d'ensemble »** : le contraste chiffré déjà prêt (`vue_ensemble.json`)
  — dans l'ensemble de Joconde « attribué à » domine ; dans les 27, école /
  atelier / manière prennent le dessus. **Barres, pas d'anneau** (familles non
  partitionnées, acté 2026-07-15).
- Organisé selon les **trois territoires** de la distance à la main (voir §5) :
  définition de chaque formule, volume global, place sur l'échelle de proximité.

### Méthode — une page unique et structurée

Aujourd'hui la méthode est **éparpillée** (intro, encadré, source, nav, pied). À
regrouper :
- **une seule** phrase de prudence reste visible ailleurs : « Le projet reprend
  les formulations publiées par les musées ; il ne réattribue aucune œuvre. » ;
- tout le reste (jeu de données, critère des 27 = ≥ 20 notices de doute hors
  copie après désambiguïsation — pas un panthéon, monoculture de Nice, copies à
  part, ambiguïtés de noms, limites de Joconde, droits des images, ce que
  l'application ne permet pas de conclure) vit dans la page Méthode.

## 4. Séparation répertoire / profil maître

Sur ordinateur, « Explorer les maîtres » se divise en deux zones qui ne partagent
plus leur largeur :

**À gauche — le répertoire** (navigation) : recherche ; tri (alphabétique ou par
nombre de notices) ; liste des maîtres ; microprofils colorés. Colonne fixe ou
repliable. Elle **ne partage pas** sa largeur avec une légende détaillée.

**À droite — la scène du maître** (profil exploré) : un vrai **bandeau de profil**
— portrait plus grand, nom, et une **phrase de synthèse calculée** qui donne
d'emblée la lecture (le lecteur n'a pas à relier seul 310, 3 344 et 64) :
> **Charles Le Brun** — 310 œuvres sont rattachées à son nom avec une réserve, sur
> 3 344 mentionnant son nom dans Joconde. La plupart relèvent de son école.

Sous le bandeau, les vues : **Profil** (plus éditorial que « Graphique ») ·
**Œuvres** · **Musées** (· **Comparer**, plus tard).

Les cinq fonctions aujourd'hui empilées au même niveau (présentation du dossier /
choix d'un artiste / profil / exploration / aide à la lecture) sont ainsi
**réparties** : présentation → en-tête de page ; choix → répertoire ; profil +
chiffres → bandeau ; exploration → vues ; aide à la lecture → « Comprendre les
mentions ».

## 5. Principe visuel central : la distance à la main du maître

L'originalité naît du **sujet**, pas d'effets décoratifs. Le doute se matérialise
en une **ligne de proximité** divisée en **trois territoires** :

```
AU PLUS PRÈS            AUTOUR DU MAÎTRE              DANS SON INFLUENCE
attribué à · ?          atelier · cercle · école      suiveur · manière · goût
```

Chaque territoire porte : un fond très léger, une **famille chromatique** (la
« boîte de pigments » déjà en place, température = distance), une **annotation
éditoriale**, et les volumes (points / colonnes). La visualisation cesse d'être un
simple graphique statistique : elle devient une **représentation du vocabulaire
muséal**.

Ce principe se retrouve **partout** : micro-jauges du répertoire, « Comprendre les
mentions », futures cartes d'œuvres, transitions entre vues, comparaison des
maîtres. C'est cette **cohérence conceptuelle** qui donne sa présence à
l'application.

## 6. L'illustration Joconde = une figure de DONNÉES (précision importante)

L'illustration ne renvoie **ni à Léonard de Vinci ni à *La Joconde* comme œuvre**.
Elle renvoie à la **base de données Joconde** : son nom, son imaginaire d'archive,
de notices, de données ouvertes et d'interface patrimoniale.

Si elle sert de couverture, elle est traitée comme une **figure de données** :
- visage / archive / **grille** / **index** ; **couches de notices** ; signes de
  base de données / d'open data ; esthétique numérique **sobre** ;
- **pas** une reproduction artistique de *La Joconde* ; **pas** un chapitre sur
  Léonard.

Le langage visuel doit être **reproductible**, jamais dépendre d'une seule image :
il se décline avec des silhouettes / portraits d'autres maîtres, des cadrages
partiels, des formes abstraites, les mêmes rectangles / lignes / points / aplats.

**Note droits** (règle CLAUDE.md) : viser une **figure originale** (composition
abstraite évoquant l'archive), pas la reproduction d'un cliché sous droits. Tout
élément d'image externe = source secondaire d'illustration, licence vérifiée
fichier par fichier, déclarée dans decisions.md et en page Méthode.

## 7. Traité plus tard (hors de ce cadrage)

- **Images / galerie éditoriale** : œuvre principale + secondaires, label de
  proximité sur/sous l'image, verbatim Joconde en zone typographique distincte,
  musée + lien POP, crédit sous la reproduction.
- **Placeholders** : repris de la direction artistique (aplats bleu nuit, cadre
  doré, silhouette/motif, titre, mention discrète « reproduction non affichée ») —
  une **partie du design**, pas un vide provisoire.
- **Kit de composants** (palier 3 de la charte) : cartes, onglets, légende,
  barres, nombres en Public Sans tabulaire, micro-légendes en italique Spectral.

## 8. À éviter (rappels)

Menu rempli de futures rubriques grisées ; accueil dominé par les avertissements
méthodologiques ; portrait réduit à une vignette ; tout dans un seul écran central ;
longue légende permanente sous la liste ; style identique pour accueil /
exploration / méthode ; cartes rectangulaires répétées partout ; originalité
décorative sans rapport avec le doute.

## Statut et suite

Cadrage **à valider**. Une fois validé, il précède et oriente le **palier 3 (kit
de composants)** de la charte : on ne reconstruit les composants qu'au service de
cette architecture (répertoire ↔ profil, trois territoires, couverture éditoriale).
Les libellés de menu et titres restent à confirmer.
