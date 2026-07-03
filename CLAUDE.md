# L'inventaire du doute — base Joconde

Projet data-journalistique de portfolio. Cas de réutilisation de données ouvertes
publiées sur data.gouv.fr, mené par un développeur Python en reconversion,
ancien journaliste.

## La question centrale

> Combien d'œuvres dans les musées de France portent une mention d'incertitude
> sur leur auteur, lesquelles, où, et sous quelles formules ?

Problématique éditoriale : que savent vraiment les musées de France des œuvres
qu'ils conservent — et comment avouent-ils, par écrit, ce qu'ils ne savent pas ?

Quand un musée ne sait pas avec certitude qui a créé une œuvre, il utilise des
formules encadrées (décret Marcus, méthode Joconde) : « attribué à », « école de »,
« atelier de », « entourage de », « d'après », « anciennement attribué à », « ? »…
Le projet lit la base Joconde, repère ces formules, les compte, les classe et
les raconte. Le cas du musée d'Alençon (deux tableaux liés au *Radeau de la Méduse*
avec des formules prudentes) sert de point d'entrée narratif.

## Règles non négociables

- **Le projet n'authentifie aucune œuvre** et n'émet aucun avis d'attribution.
  Il lit et restitue ce que les musées eux-mêmes ont publié.
- **Jamais de valeur marchande.**
- **Pas de sensationnalisme** : aucun « chef-d'œuvre caché » promis.
- Le cas Alençon est un point d'entrée narratif, **pas une enquête à mener** :
  la comparaison catalogues savants ↔ notices publiques est hors périmètre.
- **Jamais de comparaison entre musées sur des comptages bruts** : les versements
  dans Joconde sont volontaires et inégaux. Toujours contextualiser (part relative,
  total versé par musée).
- La limite « les chiffres ne reflètent que ce qui a été versé dans Joconde »
  est **affichée**, pas cachée : page « méthode et limites » au même rang que le récit.

## Source de données (canonique, unique)

Jeu « Collections des musées de France : base Joconde » sur data.gouv.fr,
Licence Ouverte 2.0. On ne s'éparpille pas sur d'autres sources.

- **CSV complet** (référence citée) : 1,1 Go, > 1 M notices, MAJ le mercredi 6h00.
  `https://www.data.gouv.fr/api/1/datasets/r/7e3307c2-f2ff-455c-bbca-bb6f11aec7bb`
- **Nomenclature ODS** (à lire en premier) :
  `https://www.data.gouv.fr/api/1/datasets/r/2a7f0292-5a9e-47fe-8a11-168158c40617`
- **API Opendatasoft** (exploration, contre-vérifications) — attention, c'est un
  **extrait** (~721 k notices, dataset `base-joconde-extrait`) :
  `https://data.culture.gouv.fr/api/explore/v2.1/catalog/datasets/base-joconde-extrait/records`

Pièges métier connus (ne pas les redécouvrir) :
- « présumé » porte souvent sur le **sujet représenté**, pas sur l'auteur → faux positifs.
- « d'après X » = copie assumée le plus souvent, pas un doute → classé à part.
- Graphies multiples (saisies par des musées différents sur des décennies).
- Le champ `auteur` porte des qualificatifs entre parenthèses : `MODERNO (attribué)`,
  `LESCHER (attribué, ?)` — convention à exploiter.

## Méthode de travail

- **Toute modification ou implémentation qui touche à l'approche doit être
  documentée au moment où elle est faite** (dans `docs/methode-et-limites.md`
  si elle relève de la méthode publiable, dans `docs/decisions.md` si c'est un
  choix, dans `docs/donnees.md` si c'est un constat sur les données). L'approche
  devra être expliquée, voire justifiée, publiquement : **elle fait partie de la
  narration**. Un ajustement de regex, un champ exclu, un quota d'échantillon —
  rien de tout cela n'est un détail technique : c'est du récit en réserve.

- **Implémentation par petites étapes, validation fréquente de l'utilisateur.**
  Pas de grosses livraisons non relues. La roadmap et les points de validation
  sont dans `docs/decisions.md`.
- La vérification manuelle des échantillons appartient à l'utilisateur.
- `docs/` est la mémoire du projet : journal, décisions, constats sur les données.
  À tenir à jour au fil de l'eau.
- **Tout en français** (docs, commentaires, README), simple et sans jargon.
- Pas de complexité inutile : le code doit rester lisible par un développeur
  intermédiaire (pièce de portfolio).
- Stack : Python (pandas) pour le traitement ; à terme D3.js pour la visualisation ;
  exports JSON légers côté front (jamais la base entière dans l'application).
- Environnement : `uv` (`uv sync`, `uv run python src/...`). `data/` n'est pas versionné.
