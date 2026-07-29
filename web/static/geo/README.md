# Fond de carte — régions de France métropolitaine

Fond de carte auto-hébergé pour la brique « Les presque » (carte par maître).
**Source secondaire d'affichage : il ne porte aucune donnée et ne compte rien.**
Aucune tuile externe, aucun appel réseau à l'exécution.

- **Fichier final** : `regions-metropole.geojson` — 13 régions métropolitaines
  (Corse comprise, aucun DROM), propriétés `code` (INSEE) et `nom`.
- **Poids** : 69 Ko (70 619 octets).
- **Projection prévue côté front** : `d3.geoConicConformal()` (conique conforme
  Lambert), `fitSize` sur ce fichier.

## Provenance

- **Source** : dépôt [france-geojson](https://github.com/gregoiredavid/france-geojson)
  (Grégoire David), fichier `regions.geojson`.
- **URL exacte du fichier source** :
  `https://raw.githubusercontent.com/gregoiredavid/france-geojson/master/regions.geojson`
- **Tracés d'origine** : IGN — Admin Express COG, édition 2018.
- **Licence** : Licence Ouverte / Etalab (conditions d'utilisation d'Admin Express).
- **Date de récupération** : 2026-07-12.
- **Poids du fichier source** : 1 452 343 octets (~1,42 Mo).

Le fichier source `regions.geojson` ne contient **déjà que les 13 régions
métropolitaines** (codes INSEE 11 à 94) : aucun filtrage des DROM n'a été
nécessaire. L'outre-mer est traité hors de cette carte (voir plus bas).

## Refaire le fond (reproductible)

```bash
# 1. Récupérer la source (pleine précision, ~1,42 Mo)
curl -sS -o regions-source.geojson \
  https://raw.githubusercontent.com/gregoiredavid/france-geojson/master/regions.geojson

# 2. Simplifier avec mapshaper (0.7.45) : 5 %, formes préservées, ~11 m de précision
npx -y mapshaper regions-source.geojson \
  -simplify 5% keep-shapes \
  -o regions-metropole.geojson precision=0.0001 format=geojson
```

- **Simplification** : Visvalingam (défaut mapshaper), rétention 5 % des points,
  `keep-shapes` (aucune région ne disparaît), `precision=0.0001` (~11 m).
- **Poids avant → après** : 1 452 343 → 70 619 octets (−95 %).

## Outre-mer — traité hors carte, jamais exclu du comptage

Le fond couvre la métropole seule. Un seul musée détenteur d'œuvre douteuse est
hors métropole (mesuré le 2026-07-12) : **musée Léon Dierx, Saint-Denis de La
Réunion — 1 œuvre (Van Dyck)**. Ce point **reste présent dans les données
(`musees_doute`) et dans les totaux** ; il n'est simplement pas projeté sur le
fond métropolitain. Le front doit l'annoncer explicitement, par exemple :

> Hors cadre métropolitain : 1 œuvre conservée à Saint-Denis de La Réunion.

## Crédit à afficher dans l'interface (petit corps, sous la carte)

> Fond de carte : contours des régions françaises (IGN Admin Express 2018,
> via france-geojson) — Licence Ouverte.
