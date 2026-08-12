# Demandes d'autorisation pour publier une reproduction

Établi le 2026-08-12. Reprend l'audit des droits photo du 2026-07-29
(`src/images_classify.py`) sans rien reclasser : il ne fait que le regrouper par
interlocuteur. Généré par `src/build_demandes_autorisation.py`.

Livrables :

- `data/exports/demandes_autorisation.csv` — une ligne par institution, classée
  par nombre de notices, avec le code Muséofile, les photographes crédités et
  les artistes concernés.
- `data/exports/demandes_autorisation_notices.csv` — une ligne par notice
  (numéro d'inventaire, titre, domaine, crédit publié, lien POP), à filtrer sur
  le musée pour constituer la pièce jointe du courrier.

**La pièce jointe s'identifie par le numéro d'inventaire, pas par le titre.**
96 notices n'ont aucun intitulé — des dessins d'Ingres à Montauban, la plus
grosse demande de la liste. Le numéro d'inventaire, lui, est renseigné pour les
802 notices : c'est la clé que le musée reconnaît.

## Ce qu'on demande, et ce qu'on ne demande pas

Le projet ne publie une image que si sa réutilisation est explicitement permise.
Sur les 3 668 notices prudentes du corpus, **aucune photographie n'est sous
licence ouverte dans POP**. La répartition commande trois traitements séparés :

| Situation | Notices | Démarche |
|---|---|---|
| Crédit publié, aucune licence (`unknown`) | 792 | **Écrire au musée.** C'est le gisement utile : rien n'autorise, rien n'interdit, seul le musée peut le dire. |
| Agence photo (RMN-Grand Palais, Bridgeman) | 2 568 | Un interlocuteur unique, hors musée. Démarche tarifée, à décider à part. |
| Aucune photographie en ligne (`unavailable`) | 298 | Rien à demander : il n'y a pas d'image. |

Une dizaine de notices « soumises à autorisation » ne relèvent pas d'une agence
mais du musée lui-même (Besançon, Dole, Cherbourg, Auxonne, Bry-sur-Marne) :
elles sont jointes aux demandes du musée concerné. Total à solliciter :
**802 notices, 93 institutions**.

Deux points à garder en tête en écrivant :

- **Le crédit nomme très souvent un photographe, pas le musée** (« © Roumagnac
  Guy », « GUENAT Pierre », « Art Shooting »). Les droits sur le cliché peuvent
  appartenir à cette personne ou à ce prestataire. Le musée reste le bon point
  d'entrée, mais il peut avoir à transmettre, et la réponse peut être « nous ne
  détenons pas les droits ».
- **Le domaine public de l'œuvre ne dit rien de la photo.** On ne demande jamais
  l'autorisation de publier l'œuvre : on demande celle de publier *cette
  reproduction*.

## La concentration : dix courriers font les deux tiers

| | Institutions | Notices | Part |
|---|---|---|---|
| 10 premières | 10 | 508 | 63 % |
| 20 premières | 20 | 609 | 76 % |
| 30 premières | 30 | 678 | 85 % |
| La longue traîne | 63 | 124 | 15 % (34 institutions n'ont qu'une notice) |

**Deux musées à eux seuls font 341 notices, soit 43 % du total** : Montauban et
Besançon. Si une seule démarche doit être menée, c'est celle-là.

### Les vingt premières

| Rang | Institution | Ville | Muséofile | Notices | Crédit dominant |
|---|---|---|---|---|---|
| 1 | musée Ingres Bourdelle | Montauban | M0607 | 210 | © Roumagnac Guy ; © Jeanneteau Marc |
| 2 | musée des beaux-arts et d'archéologie | Besançon | M0332 | 131 | GUENAT Pierre |
| 3 | musée des beaux-arts | Rennes | M0211 | 32 | © Jean-Manuel Salingue |
| 4 | musée Lambinet | Versailles | M0400 | 25 | Art Shooting |
| 5 | musée des Beaux-Arts | Nantes | M0743 | 24 | Alain Guillard |
| 6 | musée des beaux-arts | Bordeaux | M0065 | 23 | © Lysiane Gauthier |
| 7 | musée des beaux-arts | Dijon | M0137 | 17 | © Dijon, musée des beaux-arts |
| 8 | musée des beaux-arts | Rouen | M0729 | 16 | © Carole Loisel ; © Catherine Lancien |
| 9 | musée de Grenoble | Grenoble | M0994 | 16 | © Ville de Grenoble / J.-L. Lacroix |
| 10 | musée des beaux-arts | Chambéry | M1048 | 14 | Bouchayer, Giroud |
| 11 | musée des beaux-arts et galerie David-d'Angers | Angers | M0748 | 12 | © P. David ; musées d'Angers |
| 12 | musée Condé | Chantilly | M5052 | 12 | © Lynda Frénois |
| 13 | musée du Louvre | Paris | M5031 | 12 | © A. Dequier ; © M. Bard |
| 14 | musée Rolin | Autun | M0161 | 11 | © Stéphane Prost |
| 15 | musée des beaux-arts | Nîmes | M0457 | 10 | © Musée des Beaux-arts, Nîmes |
| 16 | musée Granet | Aix-en-Provence | M0894 | 10 | © Claude Almodovar |
| 17 | musée des Augustins | Toulouse | M0562 | 9 | Bernard Delorme ; Daniel Martin |
| 18 | musée des beaux-arts et d'archéologie | Dole | M0347 | 9 | © Jean-Loup Mathieu (Eurêka) |
| 19 | musée des beaux-arts | Caen | M0657 | 8 | cliché Martine Seyve |
| 20 | musée des Beaux-Arts de Saint-Denis | Reims | — | 8 | © Christian Devleeschauwer |

Les 73 suivantes sont dans le CSV. Le code Muséofile ouvre la fiche officielle
de l'institution (adresse, téléphone, direction) sur `data.gouv.fr` ; deux
institutions n'y ont pas de code sous ce nom, à retrouver à la main.

**Le fichier des musées porte un code parasite.** Une seconde entrée
« musée du Louvre, Paris » (6 notices) a pour code Muséofile l'intitulé
« mode d'acquisition particulier » — un champ Joconde recopié au mauvais
endroit, en amont. Le script ne retient que les codes de la forme `M` + chiffres
et garde l'entrée la mieux fournie, mais le défaut reste à traiter dans
`musees.json`.

## Deux démarches voisines, déjà repérées

Elles ne concernent pas les œuvres de Joconde ; elles sont notées ici pour
mémoire, à l'appréciation éditoriale de l'auteur du projet.

- **Portraits d'artistes** — quatre demandes ciblées, identités établies et
  images localisées : musée Rodin (Auguste Beuret, inv. Ph.00791) ; musées de
  Strasbourg, photothèque (portrait de Charles Eugène Ensfelder par Paul Reiber,
  inv. 77.2019.0.1174) ; Mémoire vive, Besançon (Louis Hertig dans son atelier) ;
  ayants droit du photographe du vitrail de Ludovic Alleaume (portrait d'Auguste
  Alleaume, 1917). Détail dans `docs/portraits-introuvables.md`.
- **Paris Musées** — pas une autorisation mais une clé d'API, délivrée sur
  demande. Elle donnerait accès aux photographies de Jersey de la Maison de
  Victor Hugo en CC0, à confronter aux 52 notices d'Auguste Vacquerie et
  Charles Hugo conservées au musée d'Orsay.

## Courrier type

À adapter par institution : le nom, le nombre de notices, un ou deux titres
réels pris dans le CSV, et le nom du photographe crédité quand il y en a un.
Les passages entre crochets sont les seuls à remplacer.

> **Objet :** Demande d'autorisation de publication — [N] reproductions
> d'œuvres du [nom du musée] (projet de restitution de la base Joconde)
>
> Madame, Monsieur,
>
> Je réalise un travail documentaire sur les mentions d'incertitude
> d'attribution dans les collections des musées de France, à partir de la base
> Joconde publiée en Licence Ouverte sur data.gouv.fr. Le site restitue,
> musée par musée, les notices dont les rédacteurs ont eux-mêmes signalé un
> doute sur l'auteur (« attribué à », « école de », « entourage de »…). Il
> n'émet aucun avis d'attribution, ne compare pas les musées entre eux et ne
> mentionne jamais de valeur marchande : il rend compte de ce que les musées
> ont publié.
>
> [N] notices du [nom du musée] entrent dans ce corpus, dont [titre d'une
> œuvre] et [titre d'une seconde œuvre]. La liste complète, avec les numéros
> de notice Joconde, est en pièce jointe.
>
> Les crédits photographiques publiés sur POP mentionnent [nom du photographe
> ou du service crédité], sans indication de licence. Je ne publie une
> reproduction que lorsque sa réutilisation est explicitement permise : en
> l'absence de cette mention, aucune image de vos collections ne figure
> aujourd'hui sur le site, remplacée par un cadre vide.
>
> Je souhaiterais donc savoir si vous autorisez la publication de ces
> reproductions dans ce cadre, et sous quelles conditions. Je m'engage à :
>
> - n'utiliser les images que sur ce site, à des fins documentaires et non
>   commerciales, en reproduction de petit format ;
> - afficher sous chaque image le crédit exact que vous m'indiquerez, ainsi
>   que le numéro d'inventaire et un lien vers la notice ;
> - retirer toute image sur simple demande de votre part ;
> - vous communiquer l'adresse des pages concernées avant leur mise en ligne.
>
> Si les droits sur ces clichés ne sont pas détenus par l'établissement, je
> vous serais reconnaissant de m'indiquer l'interlocuteur à solliciter.
>
> Je reste à votre disposition pour toute précision sur le projet et sur
> l'usage prévu des images.
>
> Je vous remercie de votre attention et vous prie d'agréer, Madame, Monsieur,
> l'expression de ma considération.
>
> [Prénom Nom]
> [adresse électronique] — [téléphone]
> [adresse du site]

### Ce que le courrier ne doit pas dire

- Ne pas écrire « œuvres douteuses », « attribution contestée » ni rien qui
  suggère un jugement sur la collection : la formule prudente est celle du
  musée, et le courrier doit le rappeler explicitement.
- Ne pas annoncer un nombre d'œuvres : le corpus compte des **notices**, et la
  distinction tient dans tout le projet.
- Ne pas promettre une visibilité ou une audience.
- Ne pas demander « les images en haute définition » : on demande le droit de
  publier, en petit format ; le fichier vient après, s'il vient.
