# L'inventaire du doute

> **Combien d'œuvres, dans les musées de France, portent une mention d'incertitude sur
> leur auteur — et comment les musées avouent-ils, par écrit, ce qu'ils ne savent pas ?**

Projet data-journalistique · réutilisation de données ouvertes (data.gouv.fr).
*Démo en ligne à venir.*

![L'application « Explorer les 63 maîtres » : à gauche l'introduction et la recherche, à droite le profil de Charles Le Brun avec son portrait et le graphique de répartition des mentions.](docs/captures/explorer-profil.png)

## De quoi s'agit-il ?

Quand un musée n'est pas certain de l'auteur d'une œuvre, il l'écrit — avec des formules
encadrées : « attribué à », « de son atelier », « de son école », « à sa manière », un simple
point d'interrogation… Ce projet lit la base **Joconde**, le catalogue collectif des collections
des musées de France, repère ces formules, les compte, les classe et les raconte. Le site
permet d'explorer **63 maîtres** : quelles œuvres sont associées à leur nom, sous quelles
réserves, et dans quels musées elles sont conservées.

Chiffres arrêtés à la version du **1ᵉʳ juillet 2026** : plus de **3 600 notices prudentes**
rattachées à ces 63 noms, sur **24 507** au niveau national.

## L'angle

Le nom d'un artiste, sur un cartel, ne désigne pas toujours son auteur certain. Les musées le
savent et l'écrivent : chaque formule (héritée du décret Marcus, cadrée par la méthode Joconde)
dit un degré de proximité différent avec le maître. Le projet ne cherche pas le scoop ; il rend
visible, à l'échelle de la base, **ce que les musées reconnaissent ne pas savoir**.

## Aperçu

**Toutes les œuvres concernées par un maître, filtrables par mention, avec — quand elle existe —
une reproduction ouverte :**

![Onglet « Œuvres » de Corneille de Lyon : filtres par mention, puis la liste des œuvres avec leurs reproductions et les mots exacts publiés par les musées.](docs/captures/oeuvres-reproductions.png)

**La géographie du doute autour d'un seul nom — un point = un musée détenteur :**

![Carte de France : les musées qui conservent des œuvres rattachées à Charles Le Brun sous une mention prudente.](docs/captures/musees-carte.png)

## La méthode — comment on fabrique le chiffre

Le plus délicat n'est pas de compter, c'est de compter **honnêtement**. Quelques partis pris
(détail dans [`docs/methode-et-limites.md`](docs/methode-et-limites.md)) :

- **Source unique** : la base Joconde, rien d'autre.
- **Pièges déjoués** : « présumé » porte souvent sur le *sujet représenté*, pas sur l'auteur ;
  « d'après X » est une copie assumée, pas un doute (classée à part) ; les graphies varient d'un
  musée et d'une décennie à l'autre.
- **Unité de comptage** : la notice (la référence Joconde), jamais le segment d'auteur — une
  œuvre qui nomme deux fois le même maître ne pèse qu'une fois.
- **Homonymes séparés** : Rembrandt n'est pas Rembrandt Bugatti, Fragonard père n'est pas son
  fils… chaque maître est défini par des motifs inclus / exclus, publiés avec la méthode.
- **Reproductions** : aucune image sous licence ouverte sur POP (la plupart sont « soumises à
  autorisation »). On cherche alors sur **Wikimedia Commons**, en ne retenant que les fichiers
  rattachés *avec certitude* à la notice (identifiant Joconde, recoupé par les dimensions) et
  sous licence libre → **184 reproductions** intégrées à ce jour.

## Ce que le projet s'interdit

- Il **n'authentifie aucune œuvre** et n'émet aucun avis d'attribution : il restitue ce que les
  musées eux-mêmes ont publié.
- Il ne parle **jamais de valeur marchande** et ne promet aucun « chef-d'œuvre caché ».
- Il ne **compare pas les musées** entre eux sur des comptages bruts : les versements dans
  Joconde sont volontaires et inégaux.

## Les limites, assumées

Les chiffres ne reflètent que **ce qui a été versé dans Joconde** — un inventaire vivant et
incomplet. Cette limite n'est pas cachée : elle a sa page,
[`docs/methode-et-limites.md`](docs/methode-et-limites.md), au même rang que le récit.

## Sous le capot

- **Pipeline Python** (pandas, `uv`) : lit le CSV Joconde (~1,1 Go, plus d'un million de
  notices), détecte et classe les formules, exporte des **JSON légers**.
- **Front SvelteKit statique** (`web/`, Svelte 5) : consomme ces JSON ; dataviz en Svelte / SVG,
  carte en **D3-geo**. Aucun serveur applicatif, jamais la base entière dans l'application.

## Le dépôt en un coup d'œil

| Dossier | Contenu |
|---|---|
| `src/` | le pipeline Python (détection, désambiguïsation, exports) |
| `web/` | le front SvelteKit statique |
| `data/exports/` | les données générées, versionnées (le CSV source, lui, ne l'est pas) |
| `docs/` | **la mémoire du projet** : décisions, journal, méthode, constats sur les données |

Particularité assumée : le projet **documente ses choix au fil de l'eau**. Chaque décision de
méthode est datée et justifiée dans `docs/`, parce que la façon de fabriquer le chiffre fait
partie du récit.

## Données & licences

- **Données** : [Collections des musées de France : base Joconde](https://www.data.gouv.fr/fr/datasets/collections-des-musees-de-france-base-joconde/)
  (ministère de la Culture) — **Licence Ouverte 2.0**.
- **Reproductions** : Wikimedia Commons, licence indiquée par fichier (domaine public / Creative
  Commons), créditée sous chaque image.
- **Code** : licence à définir.

---

*Projet de portfolio. Développeur Python, ancien journaliste — d'où l'angle éditorial.*
