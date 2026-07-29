# L'inventaire du doute

**Que savent vraiment les musées de France des œuvres qu'ils conservent — et
comment avouent-ils, par écrit, ce qu'ils ne savent pas ?**

Quand un musée n'est pas certain de l'auteur d'une œuvre, il l'écrit avec des
formules précises et encadrées : « attribué à », « école de », « atelier de »,
« entourage de », « anciennement attribué à », un simple point d'interrogation…
Chaque formule a un sens et un niveau de doute différents. Ce projet lit la base
Joconde — l'inventaire public des collections des musées de France —, repère ces
formules, les compte, les classe et les raconte.

Cas de réutilisation du jeu de données
[Collections des musées de France : base Joconde](https://www.data.gouv.fr/fr/datasets/collections-des-musees-de-france-base-joconde/)
(ministère de la Culture, Licence Ouverte 2.0).

## Ce que ce projet ne fait pas

- Il n'authentifie aucune œuvre et n'émet aucun avis d'attribution : il restitue
  ce que les musées eux-mêmes ont publié.
- Il ne parle jamais de valeur marchande et ne promet aucun « chef-d'œuvre caché ».
- Il ne compare pas les musées entre eux sur des comptages bruts : les versements
  dans Joconde sont volontaires et inégaux (voir `docs/methode-et-limites.md`).

## État du projet

**Phase 3 en cours — restitution web, recentrée sur « Les presque ».** Depuis le
2026-07-15, la **première version publique** est centrée sur un seul dossier :
**« Les presque »**, les œuvres que les musées rapprochent d'un grand maître sans
les lui attribuer tout à fait. Les autres rubriques et formes de doute (dont
« Avant / après ») **restent conservées et documentées dans le projet, mais hors
du périmètre publiable initial**.

Les phases 1 (test go/no-go sur la qualité des données) et 2 (typologie du doute,
pipeline d'exports) sont terminées. Le front est une application statique
SvelteKit (`web/`) qui consomme les JSON exportés par le pipeline Python ;
l'exploration des 27 noms (graphique / œuvres / carte par maître) est en place, et
un export « Vue d'ensemble » des formulations prudentes est prêt. Suivi détaillé
et périmètre V1 dans `docs/roadmap.md` (bloc « ★ RECENTRAGE »).

## Installation

Pipeline de données :

```bash
uv sync
uv run python src/download.py   # télécharge le CSV (1,1 Go) et la nomenclature
```

Front (après avoir généré les exports) :

```bash
cd web
npm install
npm run sync:data   # copie data/exports/web/*.json vers web/static/data/
npm run dev
```
