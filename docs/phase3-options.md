# Phase 3 — Options de restitution (analyse avant choix de forme)

Question posée : la carte est-elle la seule bonne option au vu de notre
classification et de notre méthode ? Faut-il continuer d'abord sur la carte ?

## Ce que nos données savent faire (rappel des assets)

| Asset (export) | Ce qu'il porte | Forme qu'il appelle |
|---|---|---|
| `niveaux.json` | l'échelle du doute (3 niveaux), familles, catégories | décodeur / clé de lecture, gradient |
| `cas.json` | 4 cas racontés (Alençon → Louvre) | récit défilant, lecture guidée |
| `recouvrements.json` | Venn doute/copie/révision | diagramme à intersections |
| `musees.json` | 555 musées, coords, total versé, part_doute | carte de points |
| `territoires.json` | départements / régions | carte choroplèthe |

## La tension réelle entre la carte et notre méthode

La carte est **l'axe le plus en tension avec nos règles non négociables** :

1. **Comparaison spatiale vs « jamais de comptages bruts entre musées ».**
   L'affordance première d'une carte est de comparer des lieux. Or c'est
   exactement ce que notre méthode interdit. Une carte « bien faite » doit donc
   brider sa propre fonction principale.
2. **Versement inégal → une carte du doute est en partie une carte de l'effort
   de catalogage.** Un département sombre peut signifier « a beaucoup versé et
   documenté », pas « recèle plus de doute ». On cartographierait une couverture,
   en la faisant passer pour un phénomène.
3. **Nos deux cas les plus forts cassent la carte.** Alençon (le cas fondateur)
   est *absent* : un blanc là où l'histoire commence. Nice/Barla (monoculture)
   écrase toute échelle de couleur (85 % de part_doute, 23,6 % du doute national).
   Les points saillants d'une carte seraient un trou et un artefact.

Conclusion : la carte n'est pas disqualifiée, mais **elle ne peut pas être la
colonne vertébrale** — la bâtir en premier reviendrait à construire la pièce
autour de notre axe le plus faible et le plus attaquable.

## Ce que nos données savent faire de PLUS solide

- **La clé de lecture (l'échelle du doute).** C'est le cœur du brief (« donner
  une clé de lecture au public ») et notre asset le plus défendable : il ne
  dépend d'aucune comparaison de lieux, juste du sens des formules. Non spatial.
- **Le récit guidé** (cases). Direction déjà pressentie dans le brief
  (« récit défilant »), et qui fait de l'absence d'Alençon une force, pas un bug.
- **L'archéologie du doute** (ancienne_attribution). Objet textuel/temporel
  (Clouet : 1904, Dimier…), pas géographique.

## Les options de forme

- **A. Récit défilant (scrollytelling)** — colonne vertébrale narrative :
  ouverture Alençon → l'échelle → les cas → la carte comme UN chapitre qualifié.
  Fort, honnête, aligné au brief. La carte y sert, elle ne commande pas.
- **B. Décodeur de formules (typologie interactive)** — le cartel expliqué :
  chaque formule, son niveau, son sens, un exemple réel, son poids. Sert
  directement la « clé de lecture ». Peut être une brique de A.
- **C. Carte d'abord** — territoriale, colorée par part_doute, avec qualificatif
  de couverture, monoculture signalée, Alençon marqué absent. Défendable mais
  met en avant notre axe le plus fragile ; risque éditorial et technique élevé.
- **D. Dashboard à filtres** — écarté par le brief lui-même (risque du « simple
  dépôt de code », pas de récit).

## Recommandation

**Colonne vertébrale = récit guidé porté par l'échelle du doute (A + B),
ouvrant sur Alençon.** La **carte reste un chapitre**, honnête et qualifié
(niveau territorial, part_doute, couverture affichée, Nice signalé, Alençon en
creux). Donc : oui, on garde la carte — mais **pas en premier, et pas comme
socle**. On construit d'abord la clé de lecture et le fil narratif ; la carte
s'y insère quand le cadre méthodologique qui la protège est déjà posé.
