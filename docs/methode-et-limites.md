# Méthode et limites — notes techniques

**La référence publique, c'est la page « Méthode » du site** (route `/methode`,
`web/src/routes/methode/+page.svelte`). Elle dit ce que le projet lit, ce qu'il
compte et ce qu'il ne prétend pas savoir, avec ses chiffres tirés des exports.
Elle fait foi.

Ce fichier ne la recopie pas : il consigne ce qui n'a pas sa place sur une page
publique — protocoles, quotas, règles de pipeline, chiffres de contrôle. Le reste
de `docs/` se répartit ainsi :

| Où | Quoi |
|---|---|
| `/methode` (site) | ce que le projet affirme publiquement, à jour |
| `docs/methode-et-limites.md` (ici) | le détail technique qui complète cette page |
| `docs/donnees.md` | constats mesurés sur les données, datés |
| `docs/decisions.md` | choix et arbitrages, datés et motivés |
| `docs/journal.md` | récit au fil de l'eau |

Les fichiers datés ne sont **jamais réécrits** : ce sont des mesures à une date,
pas des descriptions de l'état courant.

## Protocole de vérification du détecteur (206 notices, 2026-07-04)

La détection est lexicale. Sa qualité a été mesurée sur un échantillon de
206 notices jugées une à une par un humain, selon ce protocole :

- **Tirage stratifié par famille de marqueur**, reproductible (graine aléatoire
  fixée à 42, code : `src/build_sample.py`). Les familles rares sont
  sur-représentées, les familles minuscules prises en entier — un tirage
  proportionnel n'aurait montré presque que des « attribué à ». Quotas par
  famille : attribué à 30, ? 25, atelier de 25, école de 20, manière de 15,
  entourage de 15, genre de 15, suiveur de 10, présumé 4 (exhaustif),
  d'après 15, copie 10, anciennement attribué 7 (exhaustif),
  champ Ancienne_attribution 15.
- **Une ligne = un marqueur sur une notice** (une notice à deux marqueurs peut
  apparaître deux fois, chaque ligne se juge indépendamment).
- Le vérificateur voit : un **extrait** fabriqué pour la lecture (fenêtre de
  ±40 caractères autour du marqueur détecté, troncature signalée par « … »),
  les **valeurs brutes complètes** des champs concernés (non tronquées), et le
  lien vers la notice publique sur POP. Trois verdicts possibles :
  vrai / faux / incertain, avec commentaire libre.
- **Pondération obligatoire au bilan** : l'échantillon étant stratifié, le taux
  de faux positifs global n'est pas la moyenne brute des 206 lignes. Il est
  calculé par famille, puis pondéré par le poids réel de chaque famille dans la
  base (sinon les 4 « présumé » pèseraient autant que les 18 008 « attribué à »).
- **Verdicts « incertain » exclus du calcul des taux** (2 cas sur 206), mais
  conservés et documentés.
- **Résultat du premier cycle (2026-07-04)** : doute 17,0 % de faux positifs
  pondérés, copie 0 %, révision 0 % → reformulation ciblée du lexique
  (calcul : `src/evaluate_sample.py`, détail :
  `data/exports/bilan_faux_positifs.csv`). La règle de jugement appliquée :
  un marqueur ne compte que s'il qualifie l'attribution de l'œuvre de la
  notice — pas s'il apparaît dans une biographie, un nom propre ou à propos
  d'une autre œuvre.

Le lexique issu de ce cycle est versionné dans `src/markers.py` ; sa version
(`markers.VERSION`) est publiée avec les exports.

## Ce que montre l'onglet « Œuvres » d'une fiche

L'onglet montre **toutes les œuvres concernées** par le maître — pas une
sélection —, filtrables par mention et paginées. Rien n'est choisi à la main :
ni tri éditorial, ni recherche de la « meilleure » pièce.

**Une exception, déclarée : les deux notices montrées sur la page « Présentation »**
(2026-08-02, portées à deux le 2026-08-04). Celles-là sont choisies :

- « Portrait de jeune homme, dit autrefois : Portrait de Titus », musée du Louvre, champ
  auteur « Rembrandt (1606-1669) (atelier, dit) » — référence Joconde `000PE008564` ;
- « Cheval au galop », musée des beaux-arts de Chambéry, champ auteur « GERICAULT Théodore
  (attribué à) » — référence Joconde `10480003953`.

Un article s'ouvre sur des cas, pas sur un tirage au sort ; ce qui doit rester non trié, ce
sont les listes exhaustives, qu'une sélection pourrait flatter. Le choix est écrit dans
`src/build_corpus_maitres.py`, et les champs affichés sont RELUS dans l'export des œuvres à
chaque génération : si l'une de ces notices change de formulation, perd sa reproduction
réutilisable ou disparaît de la base, la génération échoue au lieu de publier un exemple
périmé. Les deux reproductions viennent de Wikimedia Commons, rattachées par identifiant
Joconde, domaine public, créditées sous l'image.

- La citation entre guillemets est le **contenu exact du champ auteur** de la
  notice (verbatim, capitales et abréviations comprises).
- Chaque œuvre renvoie à sa **fiche publique sur POP**, qui vit sa vie
  indépendamment de notre version de référence et peut avoir changé depuis.
- L'ordre place en premier les œuvres qui ont une reproduction, puis suit
  l'ordre public des mentions (`ORDRE_FAMILLES`), puis l'ordre de rencontre.
  C'est un ordre d'affichage, jamais une hiérarchie de doute
  (decisions.md, 2026-07-29).

## Les reproductions d'œuvres (Wikimedia Commons)

Une reproduction n'est affichée que si sa réutilisation est **explicitement
permise** et si elle est rattachée **avec certitude** à la notice.

- **Pourquoi pas les images de POP ?** Les crédits photographiques des
  3 668 notices ont été vérifiés sur POP : **aucune** n'est sous licence ouverte
  (l'essentiel est de la RMN, « utilisation soumise à autorisation »).
- **D'où viennent celles qui sont montrées ?** De **Wikimedia Commons**, en ne
  retenant que les fichiers sous **domaine public, CC0, CC BY ou CC BY-SA**. Le
  rattachement se fait par l'**identifiant Joconde** (via Wikidata), jamais par
  une ressemblance de titre ou de musée. **184 œuvres** sur les 3 668 en ont une
  à ce jour (bilan : `data/exports/images_bilan.json`).
- L'appariement par **numéro d'inventaire** a été tenté puis écarté : recoupé
  avec les dimensions relevées sur Wikidata, il n'a produit aucune
  correspondance assez solide — mais il a évité d'afficher 162 fausses
  reproductions (journal.md, 2026-07-29).
- **C'est une illustration, jamais une donnée** ni un comptage. L'image est
  téléchargée et servie localement (pas de lien vers un serveur externe), et
  cliquable vers sa page Commons, où figurent licence et crédit — rappelés sous
  l'image.
- Les œuvres sans reproduction réutilisable connue gardent un **emplacement
  neutre** : jamais d'image inventée.

## La carte par maître : ce qu'elle montre

- **Un point = un musée détenteur**, pas une œuvre. **Tous les points ont la même
  taille** : la carte montre *où* les œuvres concernées sont conservées, pas
  *combien* par lieu. Le nombre exact, et sous quelles formules, se lit au survol.
  Une taille variable a été testée puis écartée : l'échelle aurait été propre à
  chaque maître (un « gros point » n'aurait pas voulu dire la même chose d'une
  fiche à l'autre) et aurait gonflé de tout petits nombres.
- La carte montre une **dispersion**, pas un palmarès : elle ne compare pas les
  musées entre eux et ne dit rien de l'importance d'une collection. Le doute est
  souvent concentré dans un musée — c'est un fait de versement dans Joconde, pas
  un jugement patrimonial.
- Les points sont **localisés par leur musée** (coordonnées publiées dans
  Joconde), jamais par l'œuvre elle-même.

**Le fond de carte est une source secondaire d'illustration.** Contours des
régions françaises (IGN Admin Express 2018, via france-geojson, Licence Ouverte),
stockés localement — aucune tuile en ligne. **Aucun chiffre n'en vient** ; il ne
sert qu'à situer les points.

**Outre-mer.** Le fond n'affiche que la France métropolitaine. Une œuvre
conservée outre-mer **reste comptée et présente dans les totaux**, mais
n'apparaît pas sur le fond : une mention le signale (« Hors cadre métropolitain :
1 œuvre conservée à Saint-Denis de La Réunion »). Un point hors carte n'est
jamais un point exclu.

## La source et sa version

Jeu de données « Collections des musées de France : base Joconde », ministère de
la Culture, publié sur data.gouv.fr sous **Licence Ouverte 2.0**.

Version de référence : le CSV du **mercredi 1ᵉʳ juillet 2026**
(1 191 002 260 octets, MD5 `4cc723bb0c3aebdecd2245b7644fb00a`). La base est mise
à jour chaque mercredi à 6 h : **toute publication date son chiffre**.

Cette datation n'est pas saisie à la main. `src/download.py` note ce que le
serveur répond (`Last-Modified`, MD5, taille) dans un relevé écrit à côté du
fichier ; `src/build_exports.py` mesure le CSV réellement lu et refuse de dater
des chiffres issus d'une base qu'il ne peut pas identifier
(decisions.md, 2026-07-31 ter). L'ETag servi par data.gouv **est** le MD5 du
contenu, ce qui permet de tout vérifier hors ligne (donnees.md, T1).
