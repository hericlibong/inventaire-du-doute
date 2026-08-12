# Demandes d'autorisation pour publier une reproduction

Établi le 2026-08-12. L'audit des droits photo du 2026-07-29
(`src/images_classify.py`) a été **rejoué sur le corpus complet** : il ne portait
que sur les 3 668 notices des 69 artistes alors publiés, quand le site en publie
aujourd'hui 102, soit 6 081 notices. 2 413 notices n'avaient jamais été
examinées. La règle de classement, elle, n'a pas changé.

Le périmètre est celui du site, pas celui de la base : Joconde compte
24 507 notices prudentes, mais **on ne demande une image que pour ce qu'on
publie**, c'est-à-dire les œuvres des artistes retenus. Élargir la liste
supposerait d'abord élargir le site.

Généré par `src/build_demandes_autorisation.py` (regroupement) à partir de
`src/build_images.py` (lecture des crédits sur POP).

Livrables :

- `data/exports/demandes_autorisation.csv` — une ligne par institution, classée
  par nombre de notices, avec le code Muséofile, les photographes crédités et
  les artistes concernés.
- `data/exports/demandes_autorisation_notices.csv` — une ligne par notice
  (numéro d'inventaire, titre, domaine, crédit publié, lien POP), à filtrer sur
  le musée pour constituer la pièce jointe du courrier.

**La pièce jointe s'identifie par le numéro d'inventaire, pas par le titre.**
96 notices n'ont aucun intitulé — des dessins d'Ingres à Montauban. Le numéro
d'inventaire, lui, est renseigné pour les 2 351 notices : c'est la clé que le
musée reconnaît.

## Ce qu'on demande, et ce qu'on ne demande pas

Le projet ne publie une image que si sa réutilisation est explicitement permise.
Sur les 6 081 notices publiées, **aucune photographie n'est sous licence ouverte
dans POP** — le constat de juillet tient sur un corpus près de deux fois plus
grand. La répartition commande trois traitements séparés :

| Situation | Notices | Démarche |
|---|---|---|
| Crédit publié, aucune licence (`unknown`) | 2 322 | **Écrire au musée.** C'est le gisement utile : rien n'autorise, rien n'interdit, seul le musée peut le dire. |
| Agence photo (RMN-Grand Palais, Bridgeman) | 3 163 | Un interlocuteur unique, hors musée. Démarche tarifée, à décider à part. |
| Aucune photographie en ligne (`unavailable`) | 567 | Rien à demander : il n'y a pas d'image. |

Les notices « soumises à autorisation » qui ne relèvent pas d'une agence mais du
musée lui-même (39 en tout, dont 38 à Besançon) sont jointes aux demandes du
musée concerné. Total à solliciter : **2 351 notices, 97 institutions**.

Deux points à garder en tête en écrivant :

- **Le crédit nomme très souvent un photographe, pas le musée** (« © Roumagnac
  Guy », « GUENAT Pierre », « Art Shooting »). Les droits sur le cliché peuvent
  appartenir à cette personne ou à ce prestataire. Le musée reste le bon point
  d'entrée, mais il peut avoir à transmettre, et la réponse peut être « nous ne
  détenons pas les droits ».
- **Le domaine public de l'œuvre ne dit rien de la photo.** On ne demande jamais
  l'autorisation de publier l'œuvre : on demande celle de publier *cette
  reproduction*.

## La concentration : cinq courriers font les deux tiers

| | Institutions | Notices | Part |
|---|---|---|---|
| 2 premières | 2 | 907 | 39 % |
| 5 premières | 5 | 1 509 | 64 % |
| 10 premières | 10 | 1 809 | 77 % |
| 20 premières | 20 | 2 047 | 87 % |
| La longue traîne | 67 | 179 | 8 % (32 institutions n'ont qu'une notice) |

**Deux musées font 907 notices, soit 39 % du total** : Épinal et Besançon. Si une
seule démarche doit être menée, c'est celle-là — et le musée de l'image d'Épinal
est le premier destinataire du projet, avec ses 519 notices d'imagerie populaire.

### Les vingt premières

| Rang | Institution | Ville | Muséofile | Notices | Crédit dominant |
|---|---|---|---|---|---|
| 1 | musée de l'image | Épinal | M0537 | 519 | musée de l'Image – Ville d'Épinal / cliché H. Rouyer |
| 2 | musée des beaux-arts et d'archéologie | Besançon | M0332 | 388 | © Musée des beaux-arts et d'archéologie ; GUENAT Pierre |
| 3 | musée des beaux-arts et d'archéologie | Troyes | M0303 | 295 | Protte Jean-Marie ; Belle Carole |
| 4 | musée Ingres Bourdelle | Montauban | M0607 | 210 | © Roumagnac Guy ; © Jeanneteau Marc |
| 5 | musée de Picardie | Amiens | M0812 | 97 | © Hénin ; © Comdesimages |
| 6 | musée des beaux-arts et galerie David-d'Angers | Angers | M0748 | 87 | © P. David ; musées d'Angers |
| 7 | musée national de la céramique | Sèvres | M5019 | 67 | © M. de Giovanni, B. Chain – Le Studio Numérique |
| 8 | musée Crozatier | Le Puy-en-Velay | M0116 | 65 | (c) musée Crozatier, Luc Olivier |
| 9 | musée Adrien Mentienne | Bry-sur-Marne | M0424 | 44 | © Mathieu Lombard |
| 10 | musée des beaux-arts | Orléans | M0286 | 37 | © cliché François Lauginie |
| 11 | musée des beaux-arts | Rennes | M0211 | 32 | © Jean-Manuel Salingue |
| 12 | musée Rodin | Paris | M5044 | 28 | © Jean de Calan |
| 13 | musée des beaux-arts | Caen | M0657 | 26 | cliché Martine Seyve |
| 14 | musée Lambinet | Versailles | M0400 | 25 | Art Shooting |
| 15 | musée Westercamp | Wissembourg | M0022 | 25 | © Bifulco Ambre ; © Velten Laetitia |
| 16 | musée des beaux-arts | Bordeaux | M0065 | 24 | © Lysiane Gauthier |
| 17 | musée des Beaux-Arts | Nantes | M0743 | 24 | Alain Guillard |
| 18 | musée du Louvre | Paris | M5031 | 21 | © A. Dequier ; © M. Bard |
| 19 | musée des beaux-arts | Dijon | M0137 | 17 | © Dijon, musée des beaux-arts |
| 20 | musée des beaux-arts | Rouen | M0729 | 16 | © Carole Loisel ; © Catherine Lancien |

Le Louvre n'apparaît ici que pour 21 notices : ses 2 300 autres passent par la
RMN et sortent de la liste des musées.

Les 77 suivantes sont dans le CSV. Le code Muséofile ouvre la fiche officielle
de l'institution (adresse, téléphone, direction) sur `data.gouv.fr` ; les
97 institutions en ont un.

**On regroupe sur le code, jamais sur le nom.** Le musée de Troyes s'écrit
« d'archéologie » sur certaines notices et « d’archéologie » sur d'autres —
apostrophe droite contre apostrophe typographique, même code M0303. Regroupé par
nom, il se dédoublait en 165 + 129 notices, et deux courriers partaient à la même
adresse. Le nom affiché est la graphie majoritaire ; la clé est le code.

Signalé au passage, à corriger ailleurs : dans `data/exports/web/musees.json`,
une seconde entrée « musée du Louvre, Paris » porte comme code Muséofile
l'intitulé « mode d'acquisition particulier » — un champ Joconde recopié au
mauvais endroit, en amont du front.

## Deux démarches voisines, déjà repérées

Elles ne concernent pas les œuvres de Joconde ; elles sont notées ici pour
mémoire, à l'appréciation éditoriale de l'auteur du projet.

- **Portraits d'artistes** — quatre demandes ciblées, identités établies et
  images localisées : musée Rodin (Auguste Beuret, inv. Ph.00791) ; musées de
  Strasbourg, photothèque (portrait de Charles Eugène Ensfelder par Paul Reiber,
  inv. 77.2019.0.1174) ; Mémoire vive, Besançon (Louis Hertig dans son atelier) ;
  ayants droit du photographe du vitrail de Ludovic Alleaume (portrait d'Auguste
  Alleaume, 1917). Détail dans `docs/portraits-introuvables.md`. Deux d'entre
  elles vont à des institutions déjà présentes dans la liste des œuvres — le
  musée Rodin (28 notices) et Besançon (388) : autant les traiter dans le même
  courrier, en distinguant clairement les deux demandes.
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
