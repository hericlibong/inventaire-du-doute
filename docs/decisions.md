# Décisions

Chaque décision est datée et motivée. Les plus récentes en haut.

## 2026-08-08 (septies) — L'infobulle du graphique dit enfin combien, et de quoi

Quatrième point de la phase 3, sur le seul contenu des infobulles du graphique Profil : ni
les données, ni les axes, ni les points, ni la légende n'ont bougé.

**La mesure porte désormais la part.** L'infobulle affichait « 240 œuvres » ; elle affiche
« **240 œuvres · 77 %** », sur une seule ligne, séparés par un point médian — sans filet ni
ligne décorative. Le raisonnement de 2026-07-27, qui écartait le pourcentage parce que « la
part se lit sur l'axe », demandait au lecteur de quitter l'infobulle des yeux pour estimer
une hauteur. La part est **toujours calculée** sur le total des œuvres concernées de
l'artiste, jamais saisie.

**Règle de format, centralisée dans `familles-public.js`** : pourcentage entier ; accord du
nombre (« 1 œuvre », « 2 œuvres ») ; et **« < 1 % » pour toute part non nulle inférieure à
1 %**. Afficher « 0 % » sous un point visible serait faux. Le seuil est 1 et non 0,5 : « 1 % »
pour une part de 0,7 % surestimerait, et le graphique montre justement des mentions très
minoritaires — le « nom (?) » de Charles Le Brun pèse 0,6 %.

**Les explications passent au général.** Elles décrivaient une œuvre au singulier (« L'œuvre
est rattachée à l'école de l'artiste. ») alors qu'un point du graphique en compte un
ensemble. Les huit définitions parlent maintenant d'œuvres au pluriel : « Œuvres rattachées
à l'école de l'artiste. », « Œuvres réalisées à la manière de l'artiste. », etc. **Elles sont
réécrites dans la table `FAMILLE_PUBLIC` existante — aucune seconde table n'a été créée**,
et le champ `definition` reste la source canonique unique.

**Finition visuelle, sans agrandir ni ajouter de pointeur** : ombre adoucie (10 % au lieu de
16 %, et plus courte), bordure plus fine et plus chaude, fond très légèrement translucide
(96 %) — **le texte, lui, garde sa pleine opacité** —, et un peu plus d'air entre la mesure
et l'explication, qui sont deux registres et ne doivent pas se lire comme un paragraphe.

**Vérifié par interaction réelle**, et non par lecture du code : mention très représentée
(« 240 œuvres · 77 % »), part sous 1 % (« 2 œuvres · < 1 % »), mention à une seule œuvre
(« 1 œuvre · < 1 % », singulier correct), mention absente (aucun point rendu, donc aucune
infobulle), premier et dernier point de l'axe (aucun débordement), survol, focus clavier et
toucher depuis la légende sur mobile — les quatre voies donnent le même contenu.

## 2026-08-08 (sexies) — Le bandeau de l'artiste, rééquilibré

Suite du point précédent, sur décision de l'utilisateur : **principe de la proposition 1**
(portrait resserré, crédit aligné, composition stable), mais **sans la réduction à 11 rem**,
qui aurait fait du portrait une vignette.

**Le défaut, mesuré.** Le portrait et sa légende fixaient toute la hauteur du bandeau. Le
texte, à droite, s'arrêtait **76 px plus haut** et laissait un vide, et le départ des onglets
dépendait de l'image et non du contenu. La légende, centrée sur trois lignes, paraissait
détachée du portrait comme du reste de la fiche.

**Ce qui change sur ordinateur :**
- colonne du portrait ramenée de **16 à 14,5 rem**, image de **15 à 13 rem** de haut. Assez
  resserré pour que ce soit désormais le TEXTE qui commande la hauteur ; assez grand pour
  que le portrait garde sa présence ;
- **crédit aligné à gauche** sous l'image, et non plus centré : calé sur le même bord que
  la photographie, il lui appartient visiblement. L'image reçoit `object-position: left
  bottom` pour partager ce bord ;
- corps du crédit à **0,7 rem sur 14,5 rem**, soit environ 41 signes par ligne. Le crédit
  médian du corpus en compte 82 : il tient donc **sur deux lignes dans la majorité des
  cas**, sur trois pour les plus longs (Corneille de Lyon, 122 signes). **Jamais tronqué** —
  une attribution, une licence et un lien sont des obligations, pas des ornements ;
- **le vide a disparu** : les deux colonnes se terminent désormais à la même hauteur, à
  0 px près (mesuré sur la fiche Le Brun).

**Ce qui change sur mobile.** Le bandeau empilait un portrait pleine largeur, sa légende,
puis le nom : le lecteur descendait près de 400 px avant de savoir de qui il s'agissait.
**Le portrait (9 rem) et le nom passent côte à côte**, et les informations reprennent
dessous sur toute la largeur. Le nom descend d'un cran dans l'échelle typographique pour
tenir sans compression — il reste le plus grand élément de la fiche. **Les onglets
apparaissent environ 450 px plus tôt.**

Pour y parvenir, le nom est devenu une **zone de grille à part** (`grid-template-areas`) :
sur ordinateur il occupe la colonne de droite au-dessus des informations, sur mobile il se
place à côté du portrait. Aucun texte, aucun chiffre, aucune image, aucun crédit n'a été
modifié.

**Artistes sans portrait** (29 sur 102) : rien ne change. Pas de placeholder, pas de mention
d'absence, le texte prend la largeur et enchaîne proprement sur les onglets.

**Vérifié sur cinq cas** : nom court avec portrait (Le Brun), nom long (Giacinto
Calandrucci), nom d'état civil (Michel-Ange / Michelangelo Buonarroti), sans portrait (Léon
Tirode), et les trois onglets successivement. **Le groupe d'onglets ne bouge pas d'un pixel
au changement de vue** — position et dimensions identiques, mesurées sur ordinateur et sur
mobile.

## 2026-08-08 (quinquies) — Les onglets deviennent des commandes

Reprise du point précédent : la première version ne répondait pas à l'objectif (constat
utilisateur).

**Ce qui n'allait pas.** La barre regroupait mieux les trois libellés, mais **le long filet
horizontal qui courait au-delà de « Musées » attirait l'œil plus que les commandes**. Il se
lisait comme un séparateur de section, et les onglets restaient des liens éditoriaux : rien
ne donnait envie de cliquer.

**Ce qui remplace.** Un **groupe de trois boutons contigus**, cerné d'une bordure fine, avec
des filets verticaux entre eux. **Plus aucun filet ne se prolonge dans la page.** L'onglet
actif porte un aplat cobalt franc et un texte clair ; les inactifs gardent un fond clair et
l'encre pleine, pour rester des choix disponibles.

**Un détail qui compte** : la graisse de l'actif est plus forte que celle des autres. Sans
précaution, le groupe changerait de largeur à chaque clic et la page tressauterait. Chaque
bouton réserve donc en permanence la place de son propre libellé en gras, par un double
invisible de hauteur nulle.

Sur ordinateur, le groupe s'ajuste à ses libellés et s'aligne sur le début de la zone de
visualisation. Sur mobile, il prend toute la largeur, à parts égales, sur une seule ligne.

Balisage `tablist` / `tab` / `aria-selected` inchangé ; les réserves **A1** et **A2**
restent hors de ce correctif. Règle de forme : charte graphique, § 11.

## 2026-08-08 (quater) — Trois vues, et une barre qui le dit

Troisième point de la phase 3.

**Le défaut.** « Profil », « Œuvres » et « Musées » étaient trois libellés en petit corps,
espacés de 1,5 rem sous le portrait, posés sur un filet fin. L'onglet actif se repérait,
mais l'ensemble se lisait comme une série de liens : rien ne disait que ces trois mots
commandent les **trois vues** de l'exploration d'un artiste.

**Ce qui change**, sans une ligne de texte explicatif :
- un filet de 2 px court sur **toute la largeur de la zone d'exploration** et délimite la
  barre ;
- des **filets verticaux** séparent les trois emplacements — c'est ce qui les fait lire
  comme un groupe segmenté, et non comme des liens voisins ;
- les libellés se **touchent presque**, avec une cible d'au moins 44 px de haut ;
- la typographie gagne en présence (graisse 600, interlettrage un peu plus ouvert).

**L'onglet actif cumule quatre signes** : couleur cobalt, graisse renforcée, filet inférieur
épais, fond cobalt à 7 %. Aucun ne porte l'information seul. Le filet de l'actif se pose
**sous** celui de la barre (marge négative) : les deux se superposent au lieu de
s'additionner, et la ligne de base ne bouge pas d'un onglet à l'autre.

**Les onglets inactifs passent de l'encre douce à l'encre pleine.** Un onglet non
sélectionné reste un choix disponible : il ne doit pas avoir l'air désactivé.

**Sur mobile**, les trois se partagent la largeur à parts égales et tiennent sur une seule
ligne. Le corps et les marges se resserrent juste assez pour qu'aucun libellé ne soit
tronqué — « Œuvres » est le plus long des trois.

Ni les vues, ni les données, ni leur contenu ne sont touchés. **Aucun second système de
navigation n'a été créé** : le balisage `tablist` / `tab` / `aria-selected` existant est
conservé tel quel.

**Réserve signalée, non traitée ici** : les vues ne portent pas de `role="tabpanel"` ni de
liaison `aria-controls`. La structure reste utilisable, mais elle est incomplète au regard
du motif ARIA. À joindre au point **A1** (navigation clavier du répertoire) plutôt qu'à un
correctif visuel.

## 2026-08-08 (ter) — Le répertoire cesse de faire croire qu'il mesure

Deuxième point de la phase 3.

**Le défaut.** Sous chaque nom du répertoire, une bande colorée occupait toute la largeur
de la colonne. Elle montrait la composition des mentions — 100 % de l'artiste affiché —,
mais posée juste sous le nombre et remplissant la ligne, elle se lisait comme une jauge de
quantité. Charles Le Brun (310 œuvres) et Michel-Ange (148) avaient des bandes strictement
identiques.

**Trois options ont été examinées** : garder la longueur identique en changeant la forme ;
faire varier la longueur selon l'effectif ; supprimer la représentation. La deuxième a été
écartée sur les chiffres : la distribution va de 11 à 310, **69 artistes sur 102 sont sous
50 œuvres**, et leur ruban aurait fait moins de 16 % de celui de Le Brun — trente pixels
pour y loger jusqu'à sept segments. Elle aurait sacrifié la lisibilité des deux tiers de la
liste pour une information que le nombre et le tri donnent déjà.

**Décision (utilisateur) : la première option.** La quantité reste portée par le nombre et
par l'ordre du classement ; la couleur ne montre plus que le profil.

**La forme retenue est le ruban court** (proposition A, choisie sur maquette contre un
anneau miniature) : 96 px pour tous, calé à gauche, segments détachés par un blanc.
L'anneau était plus élégant et plus compact, mais à 18 px il ne disait plus que la couleur
dominante — ce qui ne justifiait plus de conserver les proportions.

**Un écart assumé, déclaré ici et dans le code** : un plancher de 3 px garantit qu'une
mention présente se voit. Sans lui, le « nom (?) » de Charles Le Brun, à 0,6 %, occuperait
0,6 pixel. L'excédent est repris au prorata sur les segments majoritaires, et la hiérarchie
entre mentions n'est jamais modifiée.

**L'infobulle du répertoire est supprimée** (décision utilisateur). Elle recouvrait la liste
au moment même où l'on cherchait un nom, et répétait ce que le graphique du profil dit en
mieux. Avec elle disparaissent le `role="button"`, le `tabindex`, les gestionnaires de
survol et de focus, et l'`aria-label` de la barre : le ruban devient décoratif, et la ligne
de l'artiste redevient le seul contrôle de sélection.

**Effet de bord mesuré, et volontairement laissé de côté** : la tabulation du répertoire
passe de **204 à 102 arrêts**. C'est un progrès, pas une solution — 102 arrêts avant
d'atteindre le reste de la page restent beaucoup. Le sujet est consigné comme point **A1**
de la phase 3 (roadmap), à traiter séparément.

La règle de forme est dans `docs/charte-graphique.md` (§ 10).

## 2026-08-08 (bis) — Le cobalt garde ses deux rôles, le trait fait la différence

Premier point de la phase 3, traité seul, comme le veut la règle de cette phase.

**Le défaut.** Sur « Explorer les artistes », le lien « Comment ces artistes ont-ils été
sélectionnés ? » et les nombres « 310 œuvres » et « 19 musées » ont exactement la même
couleur — `--accent-cobalt`, `#35578a` — et le lien n'était même pas souligné au repos.
Rien ne disait ce qui se clique. Le même motif régnait sur les pages « Le projet » et
« Méthode » : `text-decoration: none` et un filet qui n'apparaissait qu'au survol.

**La décision (utilisateur).** Le cobalt **peut** signaler à la fois une information
importante et un lien ; ce qui ne peut pas rester, c'est que la distinction repose sur la
seule couleur. Les nombres gardent donc leur cobalt et leur graisse ; **les liens
éditoriaux sont soulignés en permanence**, avec un survol et un focus nettement plus
marqués.

C'est l'option que je n'avais pas recommandée — je proposais de réserver la couleur aux
liens. La décision est meilleure sur un point que j'avais négligé : elle ne coûte rien à
la lisibilité des chiffres, qui sont la matière du projet.

**Mise en œuvre.** Soulignement natif plutôt que `border-bottom` : il ne déplace pas le
texte quand il s'épaissit au survol, et il évite les jambages (`text-underline-offset`).
Au repos, 1 px de cobalt à 45 % ; au survol et au focus, 2 px de cobalt plein.

**Ce qui n'est pas touché** : onglets, boutons, cartouches de la couverture, sommaire par
ancres, navigation — ils ont déjà leur propre traitement. L'appel à l'action « Explorer les
artistes », cartouche sur aplat cobalt, est explicitement exclu (`:not(.entree)`) : un
bouton n'a pas besoin d'un trait.

**Une flèche retirée, une seule.** Celle qui suivait « Comment ces artistes ont-ils été
sélectionnés ? » n'ajoutait rien après un point d'interrogation, et le libellé tient
désormais sur une ligne, y compris à 390 px. Les autres flèches — appel à l'action, renvoi
vers une notice POP — sont conservées : la demande portait sur celle-là.

La règle est inscrite dans `docs/charte-graphique.md` (§ 9), et pas seulement ici : c'est
une convention, elle doit se retrouver sans avoir à relire un journal.

## 2026-08-08 — L'accueil dit enfin de quoi il s'agit (phase 2, texte utilisateur)

Le texte de la couverture est remplacé **en entier**. Ce qu'il disait — « Quand le musée
n'est pas sûr, il l'écrit. 102 artistes, 6 081 notices où il l'a écrit. Une enquête dans les
données des musées. » — énonçait une généralité sans nommer de quoi ni de qui il s'agissait,
répétait son verbe d'une ligne à l'autre, et se terminait par une formule de dossier de
presse. Verdict de l'utilisateur, réitéré le 2026-08-08 : « même moi je ne comprends pas ».
C'était **C5**, la seule correction que le registre qualifiait de non publiable.

**Le nouveau texte est de l'utilisateur, repris tel quel :**
> Le nom d'un artiste peut accompagner une œuvre sans que le musée la lui attribue
> directement.
>
> Ce premier volume explore ces liens autour de 102 artistes : les œuvres concernées, la
> manière dont elles sont décrites et les musées qui les conservent.

**Trois interdits l'accompagnent, et ils sont tenus :**
1. **Aucune énumération de mentions** sur l'accueil — ni « attribué à », ni « de son
   atelier », ni « de son école ». Leur explication appartient à la page « Le projet ».
2. **Le texte ne commence pas par « Dans Joconde »** : on comprend le sujet avant
   d'apprendre le nom de la source.
3. **Les chiffres sortent des phrases** et deviennent une information autonome —
   « 102 artistes · 6 081 notices », sous un filet. Chaque nombre reste collé à son unité,
   la paire est insécable, et les deux valeurs continuent d'être lues dans
   `corpus_maitres.json`.

La source, enfin, se nomme complètement : « Source : Joconde, catalogue collectif des musées
de France. » remplace « À partir de la base Joconde. »

**« Présentation » devient « Le projet »** (décision utilisateur). Le libellé disait ce que
la page est ; il dit maintenant de quoi elle parle. Changé aux quatre endroits publics : la
navigation de la couverture, le bandeau général, le titre de la page, et le lien qui y mène
depuis la Méthode. **La route `/presentation` ne bouge pas** — elle a circulé, et une URL
publiée ne se renomme pas. Aucun remplacement mécanique : « La Présentation au Temple »,
titre d'œuvre affiché sur la page Méthode, est resté intact (vérifié sur le rendu).

**Ce que la composition a changé, et pourquoi.**

*La contrainte qui bridait l'écriture était fausse.* Le code répétait depuis le 2026-07-18
que l'aplat sombre est étroit et n'accepte que « trois lignes courtes ». Mesuré le
2026-08-07 : il occupe environ 700 × 620 px sur un écran de 1440, et le texte n'en utilisait
qu'un tiers. La colonne était bornée deux fois — 34 % du bloc et 23 caractères —, ce qui
cassait les phrases en lignes de trois mots, avec « il » orphelin en fin de ligne. C'est
exactement le genre de règle héritée que **C2** cherche : elle ne décrivait pas ce qu'on
regarde, et elle a servi de plafond à la réécriture pendant trois semaines.

*Les largeurs sont désormais relatives à la fenêtre, pas à la police.* L'aplat sombre est
une forme de l'illustration : sa largeur suit celle de l'écran, jamais la chasse des
caractères. Mesures faites sur les formats courants — le plus serré est le 16/10, où la zone
sombre laisse 26 % de la largeur à hauteur des paragraphes, 19 % à hauteur des chiffres et
15 % à hauteur de la source, l'aplat se refermant en escalier vers le bas.

*Et un voile local garantit le fond.* Calibrer le texte au pixel près sur une forme
irrégulière casse au premier format non testé : à 1280 × 720, où l'illustration s'affiche
entière, la fin des paragraphes retombait sur le clair. Le procédé déjà employé sur mobile —
un dégradé feutré derrière le seul bloc de texte, fondu en haut, en bas et à droite — est
étendu à l'ordinateur, en deux fois plus léger. Là où l'illustration est déjà sombre, il ne
se voit pas ; ailleurs, il assure la lisibilité. Ce n'est pas un cache posé sur l'image.

*Le millier redevient lisible.* `toLocaleString('fr-FR')` sépare par une espace fine
insécable (U+202F), qui se referme presque entièrement dans la police de titre : on lisait
« 6081 ». Sur l'affiche seulement, elle est remplacée par une espace insécable ordinaire.

*La navigation ne zigzague plus.* Les trois cartouches partaient en escalier — 0, puis
1,6 rem, puis 2,9 rem — et l'œil devait suivre un décalage qui ne disait rien. Ils partent
d'un axe commun. La hiérarchie se lit où elle doit se lire : sur la taille, le poids et la
couleur du cartouche. « Explorer les artistes » reste l'entrée principale, en cobalt.

**Contrastes vérifiés** sur l'aplat : de 8,4:1 (titre du volume) à 14,2:1 (accroche), la
source la plus faible à 8,6:1 — tous au-dessus des seuils. Les cartouches sont à 11,1:1 et
7,1:1. Les états de focus, le repli sans animation et les cibles de clic sont inchangés.

**Les deux adresses héritées changent aussi** (décision utilisateur, même phase).
`/presentation` devient **`/projet`**, `/les-presque` devient **`/artistes`**. La seconde
était un nom de travail — « les presque », pour les œuvres presque attribuées — qui n'a
jamais rien dit à un visiteur, quand l'interface appelle cette page « Explorer les artistes »
depuis le 2026-07-19. Les libellés publics, eux, ne bougent pas.

**Rien n'est supprimé.** Trois redirections permanentes : `/presentation` → `/projet`,
`/les-presque` → `/artistes`, et `/echelle` → `/projet` (elle pointait sur l'ancienne
adresse). En 308 : déplacement permanent, méthode conservée. En build statique, le prérendu
écrit une page de renvoi ; les hébergeurs qui lisent `_redirects` feront mieux. **Les ancres
survivent sans effort** : un fragment n'est jamais envoyé au serveur, `/presentation#chiffres`
arrive donc sur `/projet#chiffres`.

**Le nom interne n'est pas pourchassé.** Les fichiers, identifiants et exports qui portent
« presque » restent tels quels : ils ne s'affichent nulle part, et un refactor sans bénéfice
visible n'en est pas un. Seule la charte graphique est corrigée, parce qu'elle citait la
route comme exemple de nom de code.

Vérifié : `/projet`, `/artistes` et `/methode` répondent en 200 ; les trois anciennes URL
renvoient un 308 vers la bonne cible, sans boucle ; la navigation marque la bonne entrée
comme active sur les deux nouvelles routes ; plus aucun lien servi ne pointe vers les
anciennes adresses ; le build statique contient bien `projet.html`, `artistes.html` et les
trois pages de renvoi.

**Point noté pour F4, hors périmètre ici** : la page Méthode emploie « le projet » au sens
courant (« Le projet montre quelles réserves les musées publient »). Ce n'est pas fautif,
mais le mot désigne désormais aussi une page. À relire.

## 2026-08-07 (bis) — Le projet entre en finalisation (décision utilisateur)

Le fond du volume 1 est arrêté : données, profils, portraits et reproductions. **Rien de
tout cela ne se rouvre.** Ce qui reste relève de la finition et de la mise en publication,
et se conduit selon un plan en sept phases fixé par l'utilisateur, inscrit en tête de
`docs/roadmap.md`.

**F1** réalignement des documents · **F2** l'accueil, avec le titre du volume · **F3** les
finitions visuelles, point par point · **F4** la relecture de l'exploration · **F5** la
préparation technique au déploiement · **F6** la vérification finale · **F7** la fusion et
le déploiement.

**Trois règles de conduite, posées par l'utilisateur :**
1. **Aucun nouveau chantier**, et pas de retour sur les données, les portraits ou les images.
2. **Une phase à la fois** — jamais deux en parallèle.
3. **En phase 3, on procède élément par élément** : montrer le défaut observé, poser une
   question ciblée, proposer deux options concrètes au plus, attendre la décision, appliquer
   ce qui est validé. Pas de refonte globale, pas de série de corrections d'un bloc.

S'y ajoutent deux principes de rythme, l'un ancien et l'autre né de la séance précédente :
les vérifications sont **proportionnées** à chaque changement, le contrôle exhaustif étant
réservé à F6 ; et **aucune collecte ne démarre sans que son rendement ait été chiffré et
annoncé** — la recherche d'images du matin même a coûté cinquante minutes pour trois
reproductions, alors qu'un sondage à deux sur quinze permettait de conclure avant de
construire.

**Ce qui bloque la publication est nommé, et le reste est assumé.** Bloquant : le texte de
l'accueil (C5), le titre du volume (C3), la relecture des pages reprises (C1), les réglages
d'une page publiable — langue du document, favicon, titres et descriptions —, et la
vérification finale. Non bloquant : la longueur des pages sur mobile (C11), la recherche
d'autres règles héritées mal décrites (C2), le contrôle mot à mot de « notice » et
« œuvre » (C6, dont la règle est tranchée depuis le 2026-08-03).

**Deux tâches étaient faites sans être cochées**, constat fait en réalignant : la page
Méthode (É4), refondue le 2026-07-31 puis reprise quatre fois les 4 et 5 août, et la page
Présentation (É2), dont les trois derniers arbitrages datent du 5 août. Les constats datés
n'ont pas été réécrits : les mises à jour sont ajoutées et signalées comme telles.

**Rien ne se fusionne ni ne se déploie avant F7**, et la branche `refactor/analyse-maitres`
reste séparée.

## 2026-08-07 — Le numéro de planche, et la fin de la recherche d'images

Reprise de la phase 4 sur les artistes du lot 2. Cinq sources ont été instruites ; deux
sont écartées pour des raisons qui méritent d'être écrites, une a rendu trois images, et
le reste est un mur qu'il faut nommer.

**Le musée du Louvre est écarté, et ce n'est pas un oubli.** C'est le plus gros bloc du
lot 2 — 461 dessins sans reproduction, dont ceux de Charles Normand et de Calandrucci. Ses
conditions autorisent le téléchargement pour un usage privé, muséographique, scientifique
ou pédagogique ; toute autre diffusion suppose une demande écrite. Seul le **texte** des
notices est en Licence Ouverte, pas les photographies. Le projet ne publie que des images
sous licence ouverte : on n'en prend aucune. La question posée dans la feuille de route —
« l'audit POP portait sur les crédits POP, pas sur collections.louvre.fr » — est donc
tranchée : la réponse est la même des deux côtés.

**Limédia galeries est écarté pour une raison technique, et on ne la contourne pas.** La
bibliothèque numérique du Sillon lorrain (Nancy, Metz, Thionville, Épinal) place ses
documents du domaine public sous licence ouverte, et conserve l'imagerie populaire : c'était
la piste la plus prometteuse. Son site est protégé par une vérification anti-robot qui
bloque tout outil. Même règle que pour Geneanet lors des portraits : **une source peut se
consulter sans se moissonner**, et on ne force pas la porte.

**Le numéro de planche entre dans la méthode.** Les musées relèvent ce qui est imprimé sur
la feuille, et l'imagerie numérote ses planches : « IMAGERIE D'EPINAL, N.°551 ». Ce relevé
vit dans le champ Joconde `Precisions_inscriptions`, que le pipeline ne lisait pas ; il est
désormais repris (`build_metadonnees.py`). **410 des 465 estampes du corpus portent leur
numéro.** Il résout ce qui bloquait en juillet : trois notices du musée s'intitulent
« Notre-Dame de Bon-Secours », et le numéro les sépare — 1883 chez Pellerin, 1119 chez
Olivier-Pinot, 102 chez Pinot-Sagaire.

**Mais le numéro ne désigne jamais une image à lui seul.** Chaque maison a sa numérotation,
et les petits numéros se répètent d'une série à l'autre. C'est un **discriminant** : il
départage des candidates trouvées par le titre. Un appariement exige les deux. Le titre,
lui, doit se retrouver dans le nom du fichier ou son intitulé d'objet, jamais dans la seule
description — trop bavarde, elle a produit des rapprochements faux à l'essai.

**Une source de plus : le fonds d'imagerie déjà versé sur Wikimedia Commons**
(`src/build_imagerie_commons.py`). L'appariement de juillet passait par l'identifiant
Joconde porté par un élément Wikidata — une clé sûre, mais qui ne parle que des œuvres déjà
décrites dans Wikidata, c'est-à-dire presque aucune estampe populaire. Ici, on prend le
problème par l'autre bout : on moissonne la catégorie « Images d'Épinal » et ses
sous-catégories — **1 507 fichiers, tous sous licence ouverte** — puis on y cherche nos
notices. Bilan sur 465 estampes : **4 exactes, 6 candidates déjà illustrées par ailleurs,
289 refusées, 182 introuvables**, soit **trois images nouvelles** (209 œuvres illustrées).

**Onze correspondances ont été regardées une par une, et dix ont été écartées.** Toutes
portaient pourtant le bon titre. C'est le principal enseignement du chantier : **une image
populaire se réédite pendant un siècle**, et la même composition ressort chez un concurrent
avec un autre numéro, un autre texte et une autre adresse d'imprimeur. Deux cas suffisent
à le montrer :
- « Cadet Rousselle » : la planche numérisée porte le numéro **384**, quand les deux notices
  du musée en annoncent 518 et 261. Sans regarder l'image, on publiait un faux.
- « Histoire de l'enfant prodigue » : la planche numérisée sort de la « Fabrique de
  Pellerin » (vers 1843) et n'a pas de numéro ; la notice décrit un tirage « Pellerin & Cie »
  postérieur à 1888, au texte différent.

Les motifs de refus sont conservés en clair dans `ECARTEES`, au code, et sont publiables
tels quels.

**Ce qui reste sans image ne relève plus de la recherche.** Sur les 2 391 œuvres du lot 2
sans reproduction, les deux tiers sont des **objets uniques** — dessins et photographies
anciennes conservés à Troyes, Besançon, Amiens, Angers, Sèvres, Rodin, Le Puy, L'Isle-Adam.
Aucune bibliothèque tierce ne détient l'objet : la seule source possible est le musée
lui-même. Vérification faite, aucun de ces musées n'a versé ses collections sous licence
ouverte — leurs catégories Commons comptent quelques dizaines de photographies de
bâtiments. **La recherche d'images est close pour ce corpus**, sauf ouverture nouvelle d'une
institution.

Reste une démarche possible, qui appartient à l'utilisateur comme les autorisations de
portraits : **l'API de Paris Musées** demande une clé, délivrée sur demande. Elle donnerait
accès aux photographies de Jersey de la Maison de Victor Hugo en CC0, à confronter aux
52 notices d'Auguste Vacquerie et Charles Hugo conservées au musée d'Orsay — là encore, un
autre tirage du même négatif, avec la mention qui va avec.

## 2026-08-06 (decies) — Gallica : montrer un autre exemplaire, et le dire

Commons épuisé, la phase 4 se poursuit sur **Gallica**, qui conserve le dépôt légal des
planches Pellerin et les publie en domaine public. **Quatorze estampes intégrées** ;
206 œuvres illustrées au total.

**Ce que cette source peut dire, et ce qu'elle ne peut pas.** Une planche d'Épinal a été
tirée à des milliers d'exemplaires. Le musée décrit **le sien**, Gallica montre **celui de
la BnF** — son tampon de dépôt légal est souvent visible sur l'image. Ce n'est donc jamais
la reproduction de la feuille décrite par la notice.

**Décision (utilisateur) : on affiche, et on écrit ce que c'est.** Sous chaque image de
cette provenance, en italique et avant le crédit : **« Autre exemplaire du même tirage »**,
puis « Domaine public · source Gallica (BnF) ». Sans cette mention, on ferait passer un
exemplaire pour un autre.

**Règles d'appariement** (`src/build_gallica.py`) :
- le titre inscrit doit se retrouver dans la notice Gallica, sur forme normalisée ;
- **l'éditeur Pellerin doit être nommé des deux côtés** ;
- la notice Gallica doit être une **estampe**, pas un livre sur l'imagerie ;
- les dates, quand les deux les portent, doivent concorder à deux ans près ;
- **si le musée conserve plusieurs notices du même titre, on n'apparie pas** :
  l'exemplaire visé serait indéterminé. C'est le premier motif de refus, 255 cas.
- Les **dimensions et la technique ne servent pas de preuve** : elles divergent
  normalement d'un exemplaire à l'autre (marges rognées ; « lithographie » ici,
  « gravure sur bois » là). S'en servir aurait rejeté des correspondances justes.

**Bilan sur 355 œuvres Pellerin sans image** : 14 exactes, 0 candidate, 255 refusées,
86 introuvables. Les titres néerlandais du musée de l'Image n'ont jamais de correspondance :
Gallica n'a que les éditions françaises.

**Les quatorze ont été regardées une par une.** Toutes portent, imprimée sur la planche,
la mention « De la fabrique de Pellerin, imprimeur-libraire, à Épinal » ou « Imagerie
d'Épinal n° … » — la confirmation est **dans l'image**, comme pour le portrait de Clausel.

## 2026-08-06 (nonies) — Commons est épuisé pour ce corpus

Reprise de la recherche d'images d'œuvres (phase 4). Premier constat : la recherche de
juillet portait sur **3 668 références**, le corpus des 63 artistes d'alors. Le lot 2 l'a
porté à **6 081** — **2 413 références n'avaient jamais été examinées**. Ce n'était donc
pas un mécanisme à inventer, mais un trou à combler.

**Rendement : 22 correspondances exactes de plus, dont 8 avec image libre.** Soit 0,9 %,
quand le premier lot donnait 9 %. Total : 351 exactes, **192 images ouvertes**.

**Et l'apport ne va pas où on l'attendait** : sept des huit images sont des Jacques-Louis
David, qui appartient au corpus initial — Wikidata s'est enrichi depuis juillet. **Une
seule** concerne un artiste du lot 2 (Nicasius Bernaerts, « Combat de coqs et de poules »).

La raison est structurelle et vaut d'être écrite : le lot 2 est fait d'imagerie populaire
et de musées régionaux, quasi absents de Wikidata. Le musée de l'Image d'Épinal porte à
lui seul 519 œuvres sans reproduction. **Chercher davantage sur Commons ne donnera rien** ;
la suite passe par les bibliothèques numériques et les collections ouvertes de musées.

**Contrôle visuel des huit, une par une**, comme pour les portraits. Toutes correspondent
à leur titre Joconde. Deux cas notés, gardés :
- « Combat de coqs et de poules » : Joconde l'attribue à Nicasius Bernaerts, le fichier
  Commons à Peter van Boucle. L'appariement porte sur l'**œuvre** (identifiant Joconde
  P347), pas sur l'attribution — et cette divergence est précisément le sujet du projet.
- Deux « Marat assassiné », au Louvre et à Reims : deux versions de la même composition,
  pas un doublon.

## 2026-08-06 (octies) — Sans portrait, on ne met rien (décision utilisateur)

Vingt-neuf artistes sur cent deux n'ont pas de visage. Leur fiche affichait jusqu'ici une
silhouette dessinée et la mention « Pas de portrait fiable disponible pour X ». **Les deux
sont supprimées.** La vignette disparaît, le bloc de texte prend la largeur, et rien ne
signale l'absence.

**Deux remplacements ont été examinés et écartés.**

1. **Une image à la place** — silhouette mieux dessinée, portrait d'homme de profil, ou
   une œuvre libre de droits de l'artiste. Écartée : sur la fiche d'un artiste dont les
   œuvres ne lui sont justement **pas** directement attribuées, une image posée à
   l'emplacement du visage affirme ce que tout le texte refuse d'affirmer. Le lecteur lit
   cet endroit comme « voici lui ». Cela vaut pour les vingt-neuf fiches à la fois, et
   contredit la première règle du projet.
2. **Une phrase à la place** — « On ne connaît aucun portrait de X ». Essayée sur une
   fiche témoin, **rejetée par l'utilisateur** : l'absence n'a pas à être commentée. Le
   projet ne s'excuse pas de ce qu'il n'a pas ; il montre ce qu'il a. La table
   `portraits-absents.js` écrite pour la porter a été supprimée.

**Ce qui a été fait.** Le bandeau retire la colonne de portrait quand il n'y en a pas et
donne au texte la largeur des deux colonnes réunies : retirer l'image sans élargir la
colonne aurait remplacé un ornement par un blanc. `PortraitMaitre.svelte` ne rend plus
rien sans portrait — sa silhouette SVG et sa légende de repli sont supprimées.

**Effet de bord constaté, favorable.** Sans vignette, le nom de l'artiste s'aligne avec
les onglets et avec le titre du graphique : la fiche a une seule ligne de départ. Avec
portrait, le nom reste décalé de seize rem alors que tout ce qui suit est calé à gauche.
**Le titre saute donc d'une fiche à l'autre** selon qu'il y a ou non un portrait. Accepté
en l'état ; l'alignement du bandeau reste à reprendre, il relève de la composition, pas
de ce chantier.

Les motifs d'absence restent documentés dans `docs/portraits-introuvables.md` et dans
`data/exports/portraits_a_chercher.csv` — ils servent la recherche, pas l'affichage.

## 2026-08-06 (septies) — Ensfelder : une source qui se consulte mais ne se télécharge pas

Le seul portrait connu de Charles Eugène Ensfelder est hébergé sur Geneanet, déposé par un
généalogiste. **Le site répond 403 à tout outil** — sur la page comme sur l'URL directe de
l'image (protection Cloudflare, constatée deux fois). On ne contourne pas une protection :
l'utilisateur a enregistré le fichier depuis son navigateur, et le script le reprend tel quel.

D'où une **quatrième route** dans `web/scripts/source_portraits.py` : `FICHIER_LOCAL`, qui
lit une image déposée dans `web/scripts/portraits-fournis/` au lieu de la télécharger. Ce
dossier est **versionné** : sans ces fichiers, la commande ne serait plus rejouable. Les
quatre routes vont désormais de la plus automatique à la plus déclarée — P18 Wikidata,
fichier Commons désigné, source hors Commons décrite, fichier déjà sur le disque.

**Ce que porte l'image** : une photographie au format carte de visite, vers 1860-1875 —
redingote, main dans le gilet, fond de studio dégradé. **Aucune mention imprimée** : ni nom
d'atelier, ni tampon, ni légende. Contrairement à Clausel, il n'y avait rien à lire dessus.
La légende écrit donc « auteur inconnu ».

**Les droits sont acquis, et pour deux motifs indépendants** : le cliché est anonyme et le
sujet est mort en 1876 ; et une reproduction fidèle d'une photographie ancienne ne crée
aucun droit nouveau au profit de celui qui la met en ligne. Le crédit nomme **Geneanet**,
la source — jamais le déposant, qui héberge sans être auteur.

**Deux corrections tirées de ce cas :**

1. **Le repli d'auteur ne peut plus nommer Commons pour une image qui n'en vient pas.**
   Le manifeste écrivait « Auteur non précisé sur Commons » sous une image de Geneanet.
   Hors Commons, l'absence d'auteur se dit « auteur inconnu » — mention que la légende
   sait déjà écrire sans la faire précéder de « par ».
2. **Un portrait en pied se recadre.** Tout le corpus est en buste ; la boîte d'affichage
   fait 15 rem de haut. Laissée entière, la photographie aurait donné un visage de vingt
   pixels. Cadrage à hauteur des mains, en gardant la main dans le gilet, qui fait la pose.
   Le recadrage est déclaré dans le manifeste, comme pour les frères Duthoit et Clausel.

**La piste Reiber reste ouverte** : ce n'est pas le dessin conservé par les musées de
Strasbourg (inv. 77.2019.0.1174), qui demande une autorisation de photothèque.

Compte : **73 portraits**, 29 artistes sans visage.

## 2026-08-06 (sexies) — Clausel, ou pourquoi il faut regarder l'image avant sa page

Alexandre Clausel avait été refusé le matin même : portrait trouvé sur un blog local, sans
provenance ni licence. **Il est finalement intégré, et c'est le refus qui était mauvais.**

En ouvrant l'image, on lit sa provenance **imprimée sous le portrait** :

> ALEXANDRE-JEAN-PIERRE CLAUSEL — Peintre et Photographe troyen
> D'après un portrait à l'huile peint par lui-même en 1869
> PHOT. LOUVRIER · IMP. P. NOUEL

C'est un **autoportrait** de 1869, reproduit en phototypie et publié dans un ouvrage
ancien. Le blog n'avait fait qu'en photographier la page. Peintre mort en 1884,
reproduction du XIXe : le domaine public est acquis des deux côtés. Rien de tout cela
n'était sur la page web — tout était dans l'image.

**La leçon vaut au-delà de ce cas** : la provenance d'une image n'est pas toujours à côté
d'elle, elle est parfois dedans. Le contrôle visuel, déjà nécessaire pour distinguer un
visage d'une œuvre, sert aussi à lire ce que la page tait. Il précède le jugement sur les
droits, il ne le suit pas. Le contre-exemple est dans le même dossier : le portrait de
Gustave Lancelot, sur le même blog, ne porte aucune mention imprimée — il reste refusé.

**Une troisième route dans le mécanisme : les sources hors Commons** (`SOURCE_EXTERNE`).
Ce n'est pas un raccourci : tout ce que Commons fournissait seul — auteur, licence, page
source — doit y être établi à la main et écrit noir sur blanc. Surtout, **la légende nomme
la source réelle** : « Autoportrait d'Alexandre Clausel. Reproduction phototypie Louvrier,
Troyes-en-Champagne, domaine public. » Le nom « Wikimedia Commons » était codé en dur dans
le composant ; il devient une valeur par défaut, jamais une affirmation. Une image ne se
crédite pas d'une source qui n'est pas la sienne.

**Un candidat en attente.** Le portrait d'Ensfelder proposé sur Geneanet n'a pas pu être
récupéré : le site est derrière Cloudflare, qui renvoie 403 à tout outil et affiche une
vérification anti-bot. Cette protection ne se contourne pas — l'image devra être fournie
en fichier. À noter que le musée de Strasbourg conserve par ailleurs un dessin de Paul
Reiber le représentant, daté 1836-1876, soit exactement les dates de Joconde.

**Cadrage des demandes d'autorisation** (décision de l'utilisateur, ce jour) : elles ne
concerneront **que les œuvres et les images de Joconde**, et c'est lui qui les mènera. Les
portraits d'artistes relèvent de son appréciation éditoriale. Le rôle du projet s'y limite
à établir l'identité et à créditer exactement.

Portraits : **72**. Restent 30 artistes sans visage.

## 2026-08-06 (quinquies) — Premier retour de recherche manuelle : deux portraits sur huit

Huit candidats rapportés à la main sur la liste des introuvables. **Deux intégrés, six
refusés.** Le corpus passe à 71 portraits ; 31 artistes restent sans visage.

**Aucun des six refus ne porte sur l'identité** — elle est sûre dans quatre cas sur six.
Tous portent sur le **droit de réutilisation**, qui n'est pas établi :

| Artiste | Ce qui a été trouvé | Motif du refus |
|---|---|---|
| Auguste Beuret | musée Rodin, inv. Ph.00791, épreuve aristotype | aucune licence publiée |
| Charles Eugène Ensfelder | musées de Strasbourg, dessin de Paul Reiber, inv. 77.2019.0.1174 | « veuillez contacter la photothèque » |
| Louis Hertig | Mémoire vive, Besançon, « dans son atelier » | mentions légales sans clause de réutilisation |
| Auguste Alleaume | portrait **en vitrail** par son frère Ludovic (1917) | © du photographe seul |
| Alexandre Clausel | blog local | aucune provenance |
| Gustave Lancelot | même blog | aucune provenance |

La règle du projet tient : **un crédit n'est pas une autorisation, un © seul n'est pas une
licence, une image sans provenance ne s'utilise pas** — même quand elle est manifestement
la bonne. Le cas d'Ensfelder est le plus net : le dessin porte « 1836-1876 », exactement
les dates que Joconde écrit, et il reste inutilisable.

**Ces quatre-là ne sont plus des introuvables**, et c'est le vrai gain de ce retour. Le
portrait existe, il est identifié, il est localisé dans une institution nommée. Il ne
manque qu'une autorisation : quatre demandes ciblées, à des interlocuteurs précis. À
distinguer du Levier A différé sur les œuvres (792 notices, interlocuteurs inconnus) —
ici, quatre courriers suffiraient.

**Deux portraits intégrés, par une seule image.** Commons publie sous CC BY-SA 4.0 une
planche imprimée du XIXe portant **les deux frères Duthoit côte à côte**, chacun légendé
avec ses dates ; celles d'Aimé — 1803-1869 — sont exactement celles de Joconde. Deux
conséquences, toutes deux nouvelles pour le mécanisme :

1. **Une seconde route, le fichier choisi à la main** (`FICHIER_CHOISI`). Aucun des deux
   frères n'était atteignable par P18 : Aimé n'a aucune image sur sa fiche, et celle de
   Louis est la statue de la cathédrale d'Amiens, déjà écartée le matin même. La licence
   et le crédit continuent d'être lus sur Commons ; on n'écrit à la main que le nom du
   fichier et la raison de l'avoir choisi.
2. **Un recadrage** (`RECADRAGE`, en fractions). Une planche à deux visages ne peut pas
   servir telle quelle : sur la fiche d'Aimé, on verrait aussi Louis. On découpe, et le
   manifeste le déclare.

**Le crédit disait faux, et c'est le point à retenir.** La légende affichait « Portrait
d'Aimé Duthoit, par Bycro ». Bycro est le contributeur qui a photographié la planche en
2021 — pas l'auteur du portrait. La formule lui attribuait une œuvre qui n'est pas la
sienne et vieillissait le portrait de cent cinquante ans. Le manifeste distingue désormais
l'auteur du **reproducteur** : « Portrait d'Aimé Duthoit, auteur inconnu. Reproduction
Bycro, Wikimedia Commons, CC BY-SA 4.0. » La licence exige ce crédit ; il est donné, à sa
juste place. **Le constat de juillet se confirme : sur Commons, le crédit nomme le
contributeur, pas l'auteur** — il est à relire chaque fois avant affichage.

Les verdicts des huit candidats sont inscrits dans `data/exports/portraits_a_chercher.csv`
(colonnes `candidate_url`, `source`, `credit`, `license`, `commentaire`, `verdict`), et le
bilan est en tête de `docs/portraits-introuvables.md`.

## 2026-08-06 (quater) — Neuf portraits de plus, et quatre œuvres refusées

Suite du chantier des profils. Quarante-deux artistes sur cent deux n'avaient pas de
portrait ; ils sont désormais trente-trois. **Neuf portraits ajoutés, tous en domaine
public**, téléchargés localement comme les soixante précédents.

**P18 ne promet pas un portrait.** C'est le constat de ce lot, et il vaut pour la suite.
Sur la fiche Wikidata d'un artiste, la propriété P18 « image » porte souvent **une de ses
œuvres** et non son visage. Le défaut ne s'était pas vu sur les 63 premiers maîtres, dont
les portraits gravés sont célèbres. Ici, **quatre candidats sur treize** étaient des
œuvres :

| Artiste | Ce que P18 donnait |
|---|---|
| Louis Duthoit | la statue de saint Joseph de la cathédrale d'Amiens |
| Nicasius Bernaerts | « Bataille de chiens et de chats », une nature morte |
| Colijn de Coter | le polyptyque de Pruszcz |
| Israël Henriet | l'inscription d'éditeur au bas d'une gravure — pas même une figure |

**Aucun indice textuel ne les départageait.** Le titre de fichier, la description et les
catégories Commons donnent des signaux contradictoires : « Beaux-Arts de Carcassonne -
Bataille de chiens et de chats - Nicasius Bernaerts.jpg » porte le nom de l'artiste et
aucun mot suspect. Les treize candidats ont donc été **téléchargés et regardés**, en
planche de contact. Le contrôle est visuel et il est humain ; il n'est pas automatisable.
Mettre une œuvre à la place d'un visage tromperait le lecteur sur ce qu'il regarde.

Les quatre QID écartés sont consignés dans **`P18_NON_PORTRAIT`** (`source_portraits.py`),
et le script **refuse de démarrer** si l'un d'eux revient dans la table des QID. Une
vérification humaine qui n'est pas gravée quelque part se refait, ou pire, s'oublie.

**Deux changements au script, tirés de l'expérience.**
- **Reprise incrémentale par défaut.** Refaire les soixante portraits existants pour en
  ajouter neuf coûtait soixante requêtes, déclenchait les HTTP 429 de Commons et exposait
  des portraits déjà validés à un changement survenu depuis sur Wikidata. `--tout` force
  la régénération complète quand on la veut vraiment.
- **Patience sur les 429.** Commons refuse au-delà d'une certaine cadence ; on attend et
  on recommence plutôt que de perdre un portrait pour une question de rythme.

**Trois corrections de rédaction relevées en chemin**, toutes visibles à l'écran :
- **L'élision manquait** : « Portrait de Auguste Vacquerie ». Onze noms du corpus
  commencent par une voyelle. La légende écrit désormais « Portrait d'Auguste Vacquerie ».
- **Un anglicisme passait dans la légende** : « par Unknown author ». Commons emploie deux
  formes, seule la première était traduite.
- **Un débordement sur mobile**, mesuré à 569 px de large dans une fenêtre de 390. Le nom
  d'état civil était en `white-space: nowrap`, insécable même quand il ne tenait pas. Il
  reste insécable sur grand écran — « (Michelangelo Buonarroti) » se lit mal coupé — et
  se coupe désormais sous 760 px. **Le défaut préexistait à ce chantier** (Michel-Ange
  débordait déjà à 407 px) ; le lot 2 l'a seulement rendu voyant.

**Un `nomCivil` retiré.** « Turpin de Crissé (Lancelot Théodore Turpin de Crissé) »
répétait le nom au lieu d'y faire pont. Le champ ne sert qu'aux artistes connus sous un
surnom que Joconde n'écrit jamais.

La liste des trente-trois qui restent sans portrait est publiée dans
**`docs/portraits-introuvables.md`**, avec le motif de chaque échec et, pour ceux qu'aucune
notice d'autorité ne documente, le musée où chercher. Ce sont surtout les musées locaux —
l'Image à Épinal, Sèvres, Crozatier, Grobet-Labadié — qui détiennent cette documentation.

## 2026-08-06 (ter) — Les 39 artistes du lot 2 ont leur ligne de repérage

C4 est soldée : les 102 artistes du volume portent désormais la phrase qui les situe sous
leur nom. Restait le lot entré le 2026-08-02, dont aucun n'en avait.

**Ces 39-là ne ressemblent pas aux 63 premiers.** Ce ne sont pas des maîtres anciens
documentés par des siècles de littérature, mais pour l'essentiel des figures locales du
XIXe : l'imagerie d'Épinal (Pinot, Georgin, Morinet, Ensfelder, Hennault), la manufacture
de Sèvres (Leloy, Willermet), les sculpteurs d'Amiens (les frères Duthoit), le cercle de
Rodin (Beuret, Roche), celui de Victor Hugo (Charles Hugo, Vacquerie). Dix d'entre eux
n'ont aucune fiche Wikidata. La méthode des 63 premiers — chercher une notice d'autorité,
vérifier les dates — ne pouvait pas s'appliquer telle quelle.

**Trois sources, dans cet ordre.**

1. **Joconde elle-même**, d'abord. Les musées écrivent les dates et le métier dans le champ
   auteur : « Hussenot Joseph (1827-1896) (dessinateur) », « Hennault Henry (actif
   1891-1901) (dessinateur) ». C'est la source la plus proche du corpus, et surtout le seul
   arbitre valable face aux homonymes. Elle donne les dates de **31 artistes sur 39** et la
   fonction de **26**.
2. **Une notice d'autorité** — Wikidata, BnF, INHA, Louvre-arts graphiques, ministère de la
   Culture —, retenue **seulement si ses dates concordent** avec celles des musées.
3. **Rien.** Quand ni l'une ni l'autre ne dit, on n'écrit pas. Aucune ligne n'a finalement
   dû être laissée vide, mais la règle tenait.

**L'activité annoncée rend compte du corpus, pas de la notoriété.** Auguste Vacquerie est
connu comme écrivain ; ses 366 notices sont des photographies. La ligne dit donc d'abord
photographe. Même règle pour Charles Hugo. Ce que le lecteur a sous les yeux commande.

**Deux extensions du gabarit** (validées par l'utilisateur avant rédaction) :
- « **actif entre X et Y** » quand aucune date de vie n'est attestée. Un seul cas, Henry
  Hennault, dont ni Joconde, ni le musée de l'Image, ni Gallica ne connaissent autre chose
  que ses années chez Pellerin.
- « **après Y** » quand la mort n'est pas datée : Willermet, « 1783-après 1848 » d'après le
  ministère de la Culture.

**Un homonyme évité, à ne pas rouvrir.** La recherche sur « Charles du Ry » propose
Q1066622, architecte à Kassel (1692-1757). Ce n'est pas lui. Le Louvre, seul conservateur
de ces 33 dessins, donne « vers 1568-1655, école française, architecte des Bâtiments du roi
en 1636 » : le bisaïeul. Même famille, même métier, un siècle d'écart — le genre d'erreur
qu'un contrôle par le nom seul ne rattrape jamais. C'est le musée qui a tranché.

**Une nationalité laissée de côté à dessein.** Wikidata dit Peter Hawke « artiste
britannique » dans sa description et français par sa citoyenneté. Tant que la contradiction
n'est pas levée, la ligne ne tranche pas : « Dessinateur et lithographe du XIXe siècle,
1801-1887. »

**Un défaut de méthode corrigé en chemin**, qui vaut d'être noté : le premier rapprochement
nom → graphies Joconde procédait par mots communs. Il donnait à « Charles du Ry » les dates
de Jean-Charles François Leloy et le surnom de Charles Hugo — trois personnes fondues en
une parce qu'elles partagent le mot « Charles ». Le rapprochement passe désormais par la
table canonique `MAITRES` et `_trouve_maitre` de `build_artistes.py`, celle-là même qui
compte les notices. **Un outil d'analyse ne doit pas réimplémenter l'appariement du
pipeline : il doit l'appeler.** Le nombre d'artistes datés par Joconde est passé de 27 à 31
au passage — l'ancienne méthode en manquait autant qu'elle en inventait.

Divergences de dates relevées, tranchées en faveur des musées sauf mention, détail dans
`donnees.md` : Aimé Duthoit (Joconde 1803, Wikidata 1805), Frans Hogenberg (1592 / 1590 —
retenu 1590, plus courant), Colijn de Coter et Antonio del Pollaiuolo (quelques années
d'écart, d'où le « vers »).

## 2026-08-06 (bis) — Le panneau de la carte prend un en-tête

Le panneau du musée choisi empilait tout à plat : le nom, la ville, le compte, les mentions,
les liens. On ne voyait pas d'un coup d'œil **de quel musée** on parlait.

**Deux zones désormais.** Un en-tête qui dit qui l'on regarde — nom du musée en gras, ville
dessous en petit corps et encre douce — sur un **aplat gris pleine largeur**, fermé par un
filet. Puis le corps, qui garde le blanc-papier du panneau. Le retrait a quitté le panneau pour
chacune de ses zones : sans cela, l'aplat n'aurait pas pu courir jusqu'aux bords. `overflow:
hidden` fait suivre les angles arrondis à l'aplat.

**Un token de plus, `--surface-entete` (#f1efeb)** : un gris très clair, à peine chaud pour
tenir dans la gamme crème du site, mais **neutre** — aucune teinte de la boîte de pigments, qui
appartient aux mentions et ne doit jamais servir de décor. Contrastes mesurés au rendu : le nom
à 15,1:1, la ville à 6,4:1.

**Noms longs prévus.** Le plus long du corpus fait 84 signes (« Viséum-musée de la lunette
(collections du musée de la lunette et du musée Jourdain) ») : la coupure est autorisée à
l'intérieur des mots, l'en-tête passe à trois lignes sans rien faire déborder.

Aucune donnée, aucun texte, aucune interaction ne change.

## 2026-08-06 — La carte n'a plus qu'un seul espace d'information

**L'infobulle de la carte des musées est supprimée.** Elle disait exactement ce que dit le
panneau, s'effaçait au premier mouvement de souris, recouvrait le titre de la vue (défaut C8,
corrigé une première fois le 2026-08-03 en la fermant au clic) et n'existait pas au toucher.
Deux surfaces pour une seule information : le panneau reste, elle part. Rien ne suit plus le
pointeur, rien ne se superpose à la carte.

**Le survol change de rôle.** Il ne renseigne plus, il **annonce que le point se choisit** :
le point grossit de moitié (transformation depuis son propre centre, `transform-box: fill-box`
— animer `r` est moins régulier d'un navigateur à l'autre), son contour blanc s'épaissit, il
passe en pleine opacité, et les autres points s'atténuent légèrement (0,55) sans disparaître —
la répartition reste lisible, c'est le sujet de la carte. Le curseur est un pointeur, la
transition dure 0,12 s et disparaît si le système demande de limiter les animations.

**Le clavier reçoit le même retour**, à l'anneau de focus près : `:hover` et `:focus-visible`
partagent la règle. Le point choisi, lui, garde son cerne d'encre — un état persistant, distinct
du survol qui s'efface.

**Choisir deux fois le même musée ne referme plus le panneau.** Le geste était un bascule ; sur
un écran tactile, un second appui involontaire effaçait ce qu'on venait d'ouvrir. Le panneau se
remplace en choisissant un autre musée, et ne se ferme que par « Fermer ».

**Le flanc dit quoi faire quand rien n'est choisi** : le repère du point (« un point = un musée
conservant au moins une œuvre concernée ») et l'invitation « Sélectionnez un musée sur la carte
pour afficher les œuvres concernées ». L'ancien mode d'emploi du survol est devenu faux — il
n'affiche plus rien.

**Vocabulaire de la vue** : « œuvre » partout, jamais « notice » (É1, 2026-08-03 — le mot du
lecteur d'un côté, celui de la méthode de l'autre). Le titre devient **« Où sont conservées ces
œuvres ? »**. L'unité de calcul ne bouge pas : c'est toujours la référence Joconde.

## 2026-08-05 (septies) — Une position par musée, la même sur toutes les fiches

**Erreur repérée par l'utilisateur** : sur la fiche de Ribera, le musée Goya de Castres (Tarn)
s'affichait dans la Manche, à 670 km de sa ville. Le contrôle a montré que ce n'était pas un
cas isolé mais un **défaut de règle**.

**Ce que publie la source.** Joconde donne parfois plusieurs positions sous le même code
Muséofile : **59 musées sur 548** au 2026-08-05, dont **11 avec plus de 100 km d'écart**. Le
musée Goya est publié 1 114 fois dans le Tarn et 143 fois dans la Manche ; le musée Condé,
6 567 fois en Lot-et-Garonne et 7 049 fois à Chantilly, sous deux écritures.

**Ce que faisait le pipeline.** Il retenait la position de la **première notice rencontrée**
pour ce musée *et pour cet artiste*. Deux conséquences : la position pouvait être la
minoritaire (Castres), et le même musée pouvait se placer à deux endroits selon la fiche
consultée — **11 musées sur 116 étaient dans ce cas**, dont Chantilly avec 570 km d'écart.

**Règle adoptée** (`build_artistes.coord_du_musee`), sans source extérieure : on regroupe les
positions **voisines** (moins de 15 km), on garde la grappe qui porte le plus de notices, puis
dans celle-ci la position la plus fréquente. Le regroupement n'est pas un raffinement : sans
lui, la simple majorité expédiait le musée Condé en Lot-et-Garonne. Le calcul se fait **une
fois pour toutes, sur l'ensemble de la base** — la position d'un musée ne dépend donc plus ni
de l'artiste regardé ni de l'ordre du fichier. Trois tests unitaires figent les cas réels.

**Ce que la règle ne peut pas voir.** Quand un musée n'a publié qu'une seule position et
qu'elle est fausse, aucune règle interne ne le détecte. Un contrôle séparé le fait :
`src/audit_geoloc.py` compare chaque position publiée au centre de sa commune, cherchée par son
nom exact **et dans son département** — sans quoi les homonymes noient le résultat (« La
Châtre » ramène « La Châtre-Langlin », à 50 km dans le même département). **Sa référence est le
découpage administratif de l'État (geo.api.gouv.fr, Licence Ouverte) — source de CONTRÔLE,
jamais de données** : aucune coordonnée n'en sort pour être affichée, aucun chiffre n'en
dépend. À lancer après chaque lot d'artistes.

**Ce que le contrôle a trouvé, après correction** (548 musées, dont 116 affichés sur une carte
de fiche) : **plus aucune position instable**, et **7 écarts de plus de 15 km**, dont **un seul
sur une carte publiée** — le musée municipal de Louhans-Châteaurenaud (M0171), à 26 km de sa
commune, avec une notice. Joconde n'en publie qu'une position, et elle est fausse : rien à
choisir. Quatre autres musées sont faux mais **ne s'affichent nulle part aujourd'hui** (Nancy
294 km, Avallon 153 km, Nogent-sur-Seine 76 km, Mirecourt 43 km) ; tous ont pourtant une
position juste parmi leurs variantes, que la majorité écrase. Les deux musées d'Arles sortent à
chaque passage sans être faux : la commune fait 758 km², son centre est loin de son centre-ville.

**Rien n'est corrigé à la main pour l'instant.** Le projet restitue ce que les musées publient,
et les cinq cas restants sont soit invisibles, soit minuscules à l'échelle de la carte. Si l'un
d'eux devient voyant, la voie propre est d'**arbitrer entre les positions que le musée a
lui-même publiées** — jamais d'en inventer une —, et de figer cet arbitrage dans un fichier
versionné plutôt que d'appeler une API au moment du build.

## 2026-08-05 (sexies) — La page Méthode se ferme sur « Limites et sources »

Deux décisions de l'utilisateur closent la passe éditoriale sur cette page, qui passe de six
sections à **cinq**.

**« Lire les chiffres et les vues » est supprimée.** Quatre paragraphes qui disaient comment
lire le graphique d'un artiste, ce que compte le nombre de musées d'une fiche, ce que montre
la carte et ce que sont les reproductions. **C'était le mode d'emploi de l'interface, pas la
méthode** : ces explications doivent vivre à côté des vues qu'elles décrivent. Rien n'a été
déplacé ailleurs sur la page — c'était la consigne.

⚠️ **Une précision perd son seul point d'énoncé** : « le nombre de musées d'une fiche ne compte
que ceux ayant publié au moins une notice prudente ». La carte porte déjà « un point = un musée
ayant publié au moins une notice concernée » (`CarteMaitre.svelte`), mais le compteur du
bandeau, lui, affiche « N musées » sans cette réserve (`BandeauMaitre.svelte`). À reprendre
quand on travaillera la fiche.

**« Limites, sources et droits » devient « Limites et sources »**, en quatre sous-parties
ancrées : ce que couvrent les chiffres · un fonds qui pèse lourd dans le total · ce que le
projet permet d'affirmer · les données et les images. Les « droits » quittent le titre — les
licences se lisent dans la dernière.

**Le fonds de Nice prend sa rédaction définitive** et rejoint cette section. Elle dit ce que
l'arbitrage du 2026-08-02 avait posé et que la page n'écrivait pas encore aussi nettement :
**le comptage est exact**, mais ce fonds ne relève pas de l'attribution d'œuvres d'art étudiée
dans ce volet. Les trois nombres viennent de `niveaux.json` (24 507 · 5 791 · 18 716) et le nom
de l'établissement est **extrait du libellé de l'export**, jamais recopié : celui-ci porte un
intitulé de travail (« … — planches de Barla (attribué à) ») dont la page ne cite que le musée.

**Les liens officiels sont conservés et complétés** : Joconde et POP dans le texte, la Licence
Ouverte pointe désormais vers Etalab, Wikimedia Commons vers ses conditions de réutilisation.
La liste « Références » reste en pied de section, avec la méthode d'inventaire, le décret, POP,
Commons et le fond de carte — c'est là que le projet déclare ses sources secondaires. Aucun
visuel ajouté ; la capture des crédits reste, elle montre la phrase qui la précède.

## 2026-08-05 (quinquies) — « Comment la liste des artistes a-t-elle été établie ? »

Refonte de la quatrième section de la page Méthode, texte de l'utilisateur. Trois sous-parties
ancrées — un seuil commun · une vérification des identités · une liste encore en cours d'examen
— suivies de l'exemple des homonymes. L'ancre `#les-maitres`, visée depuis « Explorer les
artistes », **reste sur le titre de section**.

**Les six effectifs sont lus dans `registre.json`** (330 formes au seuil, 115 rattachées, 102
artistes, 33 retirées, 1 hors périmètre, 181 à examiner) : contrôlés au rendu, ils concordent
exactement avec l'export.

**L'exemple des homonymes prend la composition des autres** (`ExempleHomonymes`, sans carte,
deux volets reliés par une flèche). Deux changements de fond dans ce qu'il affirme :

- Le volet de droite ne dit plus que les quatre autres personnes « sont comptées sous leur
  propre nom ». **Rien ne le garantit** — elles n'ont pas forcément atteint le seuil, ni été
  instruites. Il dit seulement qu'elles **ne sont pas rattachées à ce profil**.
- Le bilan quitte la légende pour devenir une phrase pleine : vingt-quatre notices repérées sous
  ce nom concernaient quelqu'un d'autre, et ne sont pas comptées dans ce profil. (Chiffre de
  `docs/donnees.md` : CORNEILLE 13, CERQUOZZI 6, MERISI 4, PACE 1.)

**Trois passages quittent la page publique**, sur demande : les tests de non-régression, les
cas-témoins versionnés, et le repli « Les trois pièges corrigés en chemin » (fausses
correspondances par sous-chaîne, mentions de nationalité, doute hors parenthèses). Tout cela
reste écrit dans `docs/donnees.md` et `docs/decisions.md` — c'est de la documentation interne,
pas du récit publiable.

⚠️ **Deux chiffres publics disparaissent avec cette refonte**, effet de bord à arbitrer : « ces
102 noms réunissent 6 081 des 24 507 notices prudentes de toute la base » et « soit 2,9 % des
notices où un auteur est renseigné » (partie, celle-là, avec la refonte de la section 2). Plus
rien sur la page ne relie la liste des artistes au total national. `vue_ensemble.json` n'est
donc plus chargé par la page.

## 2026-08-05 (quater) — « Que comptons-nous, et comment ? »

Refonte de la troisième section de la page Méthode, texte de l'utilisateur. Quatre
sous-parties ancrées, sur le mécanisme posé le matin même : l'unité de calcul · lorsqu'une
notice contient plusieurs mentions · les copies sont comptées séparément · comment la part
affichée pour un artiste est calculée.

**Ce qui change dans le propos.** La section expliquait les règles en langue de pipeline
(« les familles ne sont pas les tranches exclusives d'un tout », « on n'utilise jamais de
diagramme en anneau ») ; elle dit maintenant ce qu'on compte et ce qu'on ne compte pas, sans
nommer un seul objet interne. Le pourcentage d'une fiche est explicitement borné : il mesure
une fréquence de réserves, **ni l'authenticité des œuvres ni le degré de certitude du musée**.

**L'exemple sort de son cadre.** `SchemaComptageUnique` devient `ExempleComptageUnique` : même
notice réelle (M0332004170, Besançon), même règle, mais deux volets — **« Ce que la notice
écrit » → « Ce que le projet compte »** — dans la colonne de texte, sans fond ni bordure de
carte. La valeur du champ est reproduite entière, point-virgule compris (`VOUET Simon (?) ;
VOUET Simon (atelier, dessinateur)`), chaque réserve dans la couleur de sa famille. Le résultat
est énoncé en trois lignes plutôt que dans une phrase, et la notice est consultable sur POP.
Sous 640 px, les deux volets s'empilent et la flèche se redresse.

**Conformité vérifiée** contre `build_artistes.py` : `_famille_retenue` retient le point
d'interrogation s'il est présent, puis suit l'ordre canonique des familles — c'est bien « un
ordre défini à l'avance ». La part d'une fiche vaut `doute / (propre + doute)`
(`BandeauMaitre.svelte`), copies exclues. Les deux effectifs de copies restent lus dans
`niveaux.json` (`copie`, `familles.d_apres.notices`).

**Un paragraphe déménage.** « Un seul musée peut peser lourd » (les 5 791 notices du muséum de
Nice, et le total hors ce cas) quitte le comptage pour **« Limites, sources et droits »** : ce
n'est pas une règle de calcul, c'est une limite de lecture. Chiffres inchangés, toujours lus
dans l'export.

## 2026-08-05 (ter) — « Comment une attribution incertaine est-elle indiquée dans Joconde ? »

Refonte de la deuxième section de la page Méthode, texte de l'utilisateur. Elle tenait en
quatre paragraphes numérotés à la main ; elle se lit maintenant en **cinq sous-parties
titrées** : ce que le musée écrit · trois exemples réels · les textes de référence · le
classement utilisé · comment les notices sont repérées.

**Le rail de sommaire descend d'un niveau.** `SommaireAncres.svelte` accepte un troisième
élément par entrée — la liste de ses sous-parties — et les montre en retrait, sans numéro.
Ce n'est **pas une seconde navigation** : les ancres sont aplaties en une seule liste avant
d'être mesurées, le clic, le défilement doux et le passage du focus sont ceux du rail. La
section reste allumée pendant qu'on lit l'une de ses sous-parties (classe `branche`), et
`aria-current` ne désigne que l'entrée exactement visée. **Sur petit écran, les sous-parties
quittent la barre** : elle passerait de six à onze liens en tête d'écran. Leurs ancres restent
valides, leurs titres restent lus dans la page.

**Le schéma du champ « Auteur » devient trois exemples identifiés.** `SchemaChampAuteur` était
une planche technique posée au milieu du texte, et ne disait pas de quelles notices il parlait.
`ExemplesChampAuteur` le remplace : trois lignes éditoriales séparées par un filet, sans cadre
ni carte, chacune avec l'œuvre, le musée et sa ville, la valeur du champ **mot pour mot**, une
explication et le lien vers POP. Seule la parenthèse est mise en évidence, dans la couleur de sa
famille (rouge « attribué », orangé pour le point d'interrogation seul) — la couleur désigne ce
qu'elle désigne partout ailleurs sur le site.

Les trois citations sont **contrôlées le 2026-08-05** contre `data/exports/web/oeuvres/*.json`
(références 00000077133, 01810000027, 50130000371 : titres, musées, villes et champ « Auteur »
concordants) et contre POP (les trois liens répondent). Elles sont écrites dans le composant,
pas lues dans un export : ce sont trois citations choisies, pas un échantillon.

**Deux formulations corrigées sur le fond.**

- Le sens des termes n'est plus « fixé » par deux textes. La méthode de rédaction du ministère
  **documente** ces usages ; le décret du 3 mars 1981, lui, **ne régit pas** la rédaction des
  notices Joconde — il précise la portée de termes employés dans les transactions d'œuvres d'art.
  Le lien de la méthode pointe désormais le PDF lui-même.
- Les intitulés « Presque lui », « Autour de lui », « Son style, sans lui » disparaissent de la
  page : les trois groupes s'appellent **« Au plus près », « Autour du maître », « Dans son
  influence »** depuis la refonte de la Présentation. ⚠️ Les anciens survivent encore dans
  `lib/joconde.js` (table `NIVEAUX`) et dans les commentaires de `tokens.css` — hors du périmètre
  de cette section, à traiter quand on touchera aux pages qui les affichent.

**Une note de méthode** ferme la section : « présumé » est retenu dans 4 notices du total
national et ne fait pas partie des huit catégories comparées. L'effectif est lu dans
`niveaux.json` (`familles.presume.notices`), jamais écrit.

**Écart de conformité signalé à l'utilisateur** : la phrase « dans les champs de Joconde
consacrés à l'auteur et à son attribution » recouvre `Auteur` et `Precisions_sur_l_auteur`
(`CHAMPS_TEXTE`, markers.py), mais **pas `Ecole_pays`**, que les familles « école de » et
« école-lieu » lisent aussi. Le texte est posé tel qu'il a été écrit ; la précision reste à
arbitrer.

## 2026-08-05 (bis) — La page Méthode prend les réglages de la page Présentation

Deux pages de même nature affichaient deux calibrages. Sur un écran de 1920 px, la colonne de
« Méthode et limites » démarrait **224 px plus à gauche** que celle de « Présentation » : elle
n'avait ni largeur maximale ni centrage, et courait jusqu'au bord. Le reste suivait — gouttières,
retrait sous le bandeau, interlignes, marges des titres. **Décision de l'utilisateur : une seule
identité visuelle, Méthode s'aligne sur Présentation, sans discuter chaque valeur.**

Ce qui est repris tel quel : enveloppe de 92 rem centrée, gouttières
`clamp(1.25rem, 3vw, 3rem)`, retrait haut `clamp(1.5rem, 3.5vw, 3.5rem)`, grille
`16rem minmax(0, 1fr)`, interligne du texte courant à 1,65, chapô à 1,6 sur 46 rem, marges de
`h2`, `p` et `section` **écrites** au lieu d'être laissées au navigateur, échelle unique des
sous-titres (`--taille-xs`, capitales, 0,1 em).

**La colonne n'est plus bornée en bloc.** Elle l'était à 46 rem, visuels compris. Comme sur
« Présentation », ce sont les blocs qui se bornent : **44 rem** le texte courant, **72 rem** les
trois schémas et la capture d'écran. Conséquence à surveiller : les schémas du champ « Auteur »
et du comptage unique **ne remplissent pas** 72 rem — leur contenu est aligné à gauche, le cadre
reste vide sur sa droite. Le schéma des homonymes, lui, occupe la largeur (deux colonnes).

**Deux styles ont dû être unifiés dans l'autre sens**, parce que « Présentation » n'en avait pas :

- **Les liens.** « Méthode » les compose en cobalt sans soulignement, avec un filet au survol ;
  « Présentation » laissait le bleu souligné du navigateur. C'est le seul cas où aligner sur
  Présentation aurait retiré un style de charte : le traitement cobalt est donc porté sur les
  deux pages.
- **La ligne de prudence.** Filet vermillon et italique en tête de « Méthode », petit corps UI
  gris en pied de « Présentation ». Retenu : le petit corps gris, des deux côtés. La page Méthode
  perd son filet d'alerte d'ouverture — c'est le prix de l'unité, et la phrase reste lisible.

## 2026-08-05 — Trois arbitrages sur la page « Présentation »

Trois points étaient laissés en attente à la fin du 2026-08-04. Ils sont tranchés.

**1. Une phrase qui ne décrivait que l'écran d'ordinateur.** Sous le graphique, la précaution
disait « la hauteur des barres indique une fréquence » — faux sur petit écran, où les barres
sont horizontales. Elle devient « Ces barres indiquent une fréquence, pas un degré de certitude
sur l'attribution. » Le chapô du graphique dit déjà, six lignes plus haut, que les barres
indiquent la fréquence : la précaution n'a pas besoin de renommer la dimension, et le lecteur a
une notion de moins à retenir. Règle qui en découle : **aucun texte publié ne nomme une
direction de l'écran** (hauteur, largeur, colonne de gauche) — l'affichage change, le texte non.

**2. Le bandeau de titre entre dans la colonne de contenu** — sur « Présentation » **et** sur
« Méthode et limites ». Il gardait la pleine largeur au-dessus du rail (décision du 2026-08-04
bis, ci-dessous, que celle-ci remplace) : le titre partait donc du bord gauche, et tout le reste
de la page seize rem plus loin. Deux lignes de départ pour une page, dont une seule porte du
texte. Le titre occupe désormais la première ligne de la colonne de contenu, le rail court sur
toute la hauteur à sa gauche : une seule abscisse pour le titre, le texte et les blocs larges,
et le sommaire se lit comme une navigation plutôt que comme le premier contenu de la page.

Le titre reste **écrit avant le sommaire dans le document** (il se lit d'abord, et le repli à
760 px le remet naturellement au-dessus de la barre de liens) : le placement dans la grille est
donc explicite des deux côtés, et annulé sous 760 px. Les deux pages portent la même
disposition — passer de l'une à l'autre ne doit pas déplacer le titre.

**3. Le glossaire garde les en-têtes du graphique, et dit ce qu'elles recouvrent.** « Au plus
près », « Autour du maître », « Dans son influence » se répètent d'un bloc à l'autre : c'est
voulu, c'est ce qui fait comprendre que le glossaire définit les groupes qu'on vient de voir, et
les deux blocs lisent la même source (`territoires.js`). Pour que la reprise ne soit pas une
copie sèche, chaque en-tête du glossaire porte maintenant l'annotation de zone, écrite depuis
longtemps mais affichée nulle part sur cette page : « Sa main est probable, sans certitude. »,
« Son atelier, son cercle, son école — plus que sa main. », « Son style, repris sans lui. » Elle
reste du texte courant, pas des capitales : en en-tête, elle passerait pour un second titre.

## 2026-08-04 (bis) — Un seul sommaire pour tout le site

La page « Présentation » reçoit le rail de sommaire de la page « Méthode ». Plutôt que de le
recopier, **le mécanisme devient un composant partagé** (`lib/SommaireAncres.svelte`) : rail
collant, repérage de la section lue, défilement doux, retour en haut, bascule mobile. Les deux
pages le consomment ; aucune ne porte plus sa propre navigation interne. Le site n'aura jamais
deux comportements différents pour le même geste.

**Ce que la page fournit, ce que le composant fournit.** La page donne sa liste de sections
(identifiant + libellé court) et la grille qui accueille le rail ; le composant fait le reste.
Le seuil de bascule mobile (760 px) est le seul point à tenir synchronisé des deux côtés —
c'est écrit dans les deux fichiers.

**Sept identifiants stables, sans accents**, parce qu'ils entrent dans l'URL et se partagent :
`le-projet`, `ce-volet`, `exemples`, `selection`, `chiffres`, `definitions`, `explorer`. Les
libellés du rail reprennent les titres, raccourcis pour les deux questions (« Qu'est-ce que
L'inventaire du doute ? » ne tient pas dans 16 rem) ; les titres publiés ne changent pas.

**Deux corrections apportées au mécanisme commun**, qui profitent aussi à la page Méthode :

- **Ce qu'on demande l'emporte sur ce qu'on mesure.** Quand la page est en butée basse, les
  deux dernières sections tiennent dans le même écran et la mesure désignait toujours la
  dernière : demander « Ce que ces mots veulent dire » affichait « Explorer ». Un clic du rail
  ou une ancre reçue dans l'URL fixent désormais le repère jusqu'au prochain geste de
  défilement du lecteur.
- **Le graphique bascule sur SA largeur, plus sur celle de la fenêtre** (`@container`). Avec un
  rail de 16 rem, une fenêtre large ne garantit plus une colonne large : huit colonnes dans
  40 rem donnaient des libellés en escalier. Seuil à 45 rem, choisi au-dessus de la largeur que
  le graphique retrouve quand le rail disparaît — sinon rétrécir la fenêtre le ferait repasser
  en colonnes, ce qui se lirait comme un défaut.

**Composition.** Le bandeau de titre garde la pleine largeur au-dessus du rail — un titre de
page ne se met pas en colonne — et devient la première entrée du sommaire. *(Revu le
2026-08-05 : le titre est entré dans la colonne de contenu, sur les deux pages. Voir l'entrée
du jour.)* À la différence de
la page Méthode, la colonne de contenu n'est **pas** bornée à la largeur d'un paragraphe : elle
porte aussi le bandeau de chiffres, le graphique et le glossaire. Ce sont les blocs de texte
qui se bornent eux-mêmes (44 à 52 rem). Vérifié sans débordement horizontal de 360 à 1600 px.

## 2026-08-04 — « Les mentions en chiffres » : trois zones qu'on peut désigner

Refonte de la seule section chiffrée de la page « Présentation ». Elle s'appelait « Les
mentions les plus fréquentes » et posait trois problèmes : les chiffres clés du volet
vivaient ailleurs dans la page, les trois groupes de mentions n'étaient qu'une bande de
titres flottant au-dessus des colonnes, et ils disparaissaient complètement sous 760 px.

**Ce qui est décidé.**

- **Les trois chiffres du volet (artistes, notices, part du total) ne se disent qu'une
  fois**, dans le bandeau qui ouvre la section. Les paragraphes d'ouverture et de sélection
  les répétaient : ils ont été allégés des seules phrases qui les portaient, sans réécriture.
  Un même chiffre lu deux fois dans une page se lit comme deux chiffres différents.
- **Les groupes deviennent des zones dessinées** : fond léger (tokens `--territoire-*`,
  écrits pour cet usage), limites nettes, titre à l'intérieur du cadre. Le titre appartient
  à sa zone parce qu'il est dedans, pas parce qu'il est au-dessus. Même traitement sur
  mobile, où les trois zones deviennent trois blocs titrés au lieu de disparaître.
- **L'interaction porte sur la zone, jamais sur une colonne isolée.** Survol, focus clavier
  ou toucher mettent en évidence toutes les mentions du groupe et atténuent les deux autres.
  Une épingle (clic/toucher) tient la mise en évidence là où il n'y a pas de survol ; on
  referme en retouchant la même zone ou par Échap.
- **Plus aucune infobulle.** Les valeurs exactes — part et nombre de notices — restent
  écrites au-dessus de chaque barre, en permanence. Une donnée qu'il faut survoler pour lire
  n'existe pas sur un écran tactile.
- **L'axe est nommé** : « Part des notices dans lesquelles cette mention apparaît ».
- **Le texte sous le graphique ne commente plus, il constate** : la mention la plus fréquente
  et celle qui suit, cherchées par leur valeur et non écrites en dur. Deux précisions
  distinctes le suivent, en mentions techniques : la taille des barres mesure une fréquence
  et non un degré de certitude ; une notice pouvant porter plusieurs mentions, les parts ne
  font pas 100 %.
- **Le glossaire « Ce que ces mots veulent dire » est détaché** de la section chiffrée par un
  filet et une respiration franche : c'est le seul endroit du site où les huit mentions sont
  définies, il ne doit pas se lire comme une seconde légende du graphique. Les huit
  définitions ne sont pas retouchées.

**Inchangé** : les données, les huit couleurs, l'ordre des mentions (distance à la main de
l'artiste, jamais un classement par valeur) et la largeur du graphique, qui sera arrêtée à la
composition finale de la page.

## 2026-08-03 (bis) — « Notice » et « œuvre » : une convention, pas une correction

L'audit du point de contrôle 2 avait relevé que le même nombre s'appelle « œuvres » sur le
bandeau d'un artiste et « notices » sur sa carte, et l'avait classé **bloquant** (C6).

**Arbitrage utilisateur : ce n'est pas un défaut à corriger, c'est une convention à tenir.**

> - **« notice »** pour la méthode, les données et les explications techniques ;
> - **« œuvre »** pour l'interface, les légendes, les bulles et les textes destinés au
>   lecteur ;
> - **aucun remplacement mécanique** d'un terme par l'autre.

Les deux mots ne sont donc pas interchangeables et ne doivent pas être uniformisés : ils
marquent deux registres. Un lecteur devant une fiche regarde des œuvres ; une page qui
explique comment on a compté parle de notices, parce que c'est l'unité réelle du calcul et
qu'une notice peut exceptionnellement décrire un ensemble.

**Conséquence sur le registre des corrections** : C6 perd son statut bloquant. Il ne reste
qu'une **vérification de cohérence page par page**, faite au moment où chaque page est revue
dans le chantier éditorial — pas une passe de recherche-remplacement.

**Ce que cela ne change pas** : la règle stricte du 2026-07-18 tient toujours — on ne publie
jamais un total national en « œuvres » (« 24 507 œuvres » resterait faux), et le projet
n'authentifie rien.

## 2026-08-03 — La Présentation reprend l'enveloppe d'« Explorer les artistes »

Défaut introduit en phase 7 et signalé par l'utilisateur : la page « Présentation » courait
d'un bord à l'autre de l'écran, sans marges, illisible sur un grand moniteur.

**La cause.** En passant la route en « pleine largeur » (pour qu'elle gère ses propres
gouttières comme l'accueil et l'exploration), on lui a retiré la limite du conteneur `main`
sans lui en donner une. Elle n'avait qu'un `padding` : à 1920 px, le texte occupait toute la
largeur de l'écran.

**Le correctif.** La page reprend **exactement** l'enveloppe d'« Explorer les artistes » —
`max-width: 92rem`, `margin-inline: auto`, mêmes gouttières, même retrait sous le bandeau.
Mesuré aux trois largeurs (1920, 1440, 1280 px) : les deux pages ont le même bord gauche, la
même largeur, le même point de départ du texte. Passer de l'une à l'autre ne doit pas donner
l'impression de changer de site.

**Et une colonne intérieure.** Les blocs larges de la page — chiffres, sélection, glossaire,
graphique — se bornaient chacun où il voulait (58, 72 rem, ou rien du tout pour le graphique).
Ils partagent désormais **une seule limite**, déclarée une fois. Le texte courant garde sa
mesure plus étroite (44 rem) : c'est ce qui se lit, pas ce qui s'aligne.

## 2026-08-02 (duodecies) — Navigation finale, et les définitions déménagent

Phase 7. La navigation publique du volume 1 tient en quatre entrées, dans l'ordre de
lecture : **Accueil · Présentation · Explorer les artistes · Méthode**. Identique dans le
bandeau et sur la couverture (où « Accueil » ne figure pas : on y est).

**« Comprendre les mentions » sort de la publication.** Sa comparaison chiffrée avec le total
national faisait double emploi avec la vue abandonnée du prototype ; son graphique et ses
territoires ont rejoint la Présentation.

**Mais elle portait les définitions des huit mentions, et elles n'existaient nulle part
ailleurs.** Retirer la page sans les déplacer aurait supprimé du site le seul endroit où l'on
apprend ce que veut dire « de son école » ou « à sa manière ». Elles sont donc **déménagées
sur la Présentation, sous le graphique qui les compte** — précisément là où un lecteur qui
voit « de son école » à 22 % se demande ce que c'est. Elles n'existent toujours qu'à un seul
endroit : la consigne était « définitions déplacées sans répétition ».

**L'ancienne URL redirige** (`/echelle` → `/presentation`, 308). Elle a circulé ; une adresse
publiée ne tombe pas sur une page d'erreur. En build statique, le prérendu écrit une page de
renvoi (script + `meta refresh`). Les deux liens de la page Méthode qui pointaient vers elle
sont repointés vers la Présentation, avec leur libellé corrigé.

**Le mécanisme « à venir » est supprimé, pas seulement ses entrées.** Le bandeau savait
afficher une rubrique non publiée en lien inerte (champ `prete`, branche `.a-venir`). La
consigne est de ne pas annoncer les volumes suivants de cette façon : retirer le mécanisme
plutôt que les seules entrées évite qu'il resserve. Les rubriques en réserve (révisions,
carte) restent au dépôt, hors navigation, en attendant d'être publiées.

## 2026-08-02 (undecies) — L'accueil annonce le volume, plus le total national

Phase 6. L'affiche reste le premier écran, en un seul écran. Ce qui change, c'est ce qu'elle
annonce.

**Le titre du volume entre sur la couverture** : « Volume 1 — Autour des maîtres », sous le
nom du site, en petit corps. Le site en publiera d'autres ; l'accueil doit dire lequel on
ouvre.

**Le total national quitte la couverture.** Le chiffre vedette était 24 507 — « Dans 24 507
d'entre elles, l'attribution est formulée avec prudence ». Il est exact, mais il demande une
explication que l'accueil n'a pas à porter : versement volontaire des musées, monoculture
divulguée, ce qu'il compte au juste. Il vit maintenant sur la page « Présentation », qui
l'explique en contexte. **La couverture porte les chiffres DU VOLUME** — artistes retenus et
notices concernées — lus depuis `corpus_maitres.json`, jamais écrits en dur.

**Trois lignes, et pas quatre.** Première tentative de rédaction : un slogan long, une phrase
de chiffres développée. Résultat vérifié au navigateur : le bloc débordait de l'aplat sombre
et les deux dernières lignes tombaient sur l'illustration claire, illisibles. La contrainte
n'est pas le goût, c'est la géométrie de l'affiche — la zone sombre est étroite et recule
vers le bas. La copie est donc courte, et le commentaire du composant le dit pour la
prochaine fois.

**« Présentation » ouvre la navigation de couverture**, avant « Explorer les artistes » qui
reste l'entrée PRINCIPALE (plus large, accent cobalt). L'un est la porte de qui arrive sans
rien savoir, l'autre celle de qui veut entrer directement dans l'application. « Comprendre
les mentions » y figure encore : elle en sort en phase 7, en même temps que dans le bandeau.

## 2026-08-02 (decies) — « Explorer les artistes » redevient un outil, pas une lecture

Phase 5. L'introduction de deux paragraphes qui coiffait le répertoire est retirée. Elle
expliquait ce qu'est Joconde et ce que sont les formulations prudentes — c'est-à-dire
exactement ce que la page « Présentation » dit maintenant, mieux et plus longuement.

**Ce qui reste en tête** : le titre, un renvoi discret — « Comment ces artistes ont-ils été
sélectionnés ? » — et la sélection. Le répertoire commence désormais à 249 px du haut de la
page : sur un écran ordinaire, l'outil entier (liste à gauche, profil et onglets à droite) est
visible sans défiler. On vient ici pour chercher un artiste, pas pour lire.

**Le renvoi pointe vers la Présentation, plus vers la Méthode.** C'est la Présentation qui
explique désormais la sélection en clair ; la Méthode reste au bout, pour qui veut le détail.

**La ligne de prudence est partie sans être perdue.** Elle disait « le projet reprend les
formulations publiées par les musées ; il ne réattribue aucune œuvre ». Le pied de page du
site porte déjà « Ce projet n'authentifie aucune œuvre — il restitue ce que les musées ont
publié », sur toutes les pages, et la Présentation la reprend en propre. La retirer de
l'introduction ne retire donc rien au lecteur.

**L'effectif d'artistes ne s'affiche plus sur cette page.** Il vivait dans la phrase
d'introduction ; il se lit sur la Présentation, depuis les mêmes exports. Une donnée de moins
à tenir à jour à deux endroits.

## 2026-08-02 (nonies) — La page « Présentation » : six temps, une seule visualisation

Phase 4 du volume. Une page publique distincte (`/presentation`) mène du nom lu sous une
œuvre jusqu'à l'exploration des artistes.

**Pas de scrollytelling**, bien que le brief l'autorisât. La préférence tenue depuis le
2026-07-08 l'écarte, et le risque était réel : une page qui prend la main sur le défilement
pour dérouler six idées devient vite l'inverse de ce qui est demandé — « une succession de
longs textes et de graphiques génériques ». Une page qui se lit, avec une seule visualisation
à sa place, tient mieux.

**Six temps** : la notice réelle et ses mots exacts · du cas au volume · les chiffres
essentiels · comment ces artistes ont été choisis · les mentions les plus fréquentes ·
l'entrée dans l'exploration.

**La notice d'ouverture est choisie, et le choix est déclaré.** « Portrait de jeune homme,
dit autrefois : Portrait de Titus », au Louvre, où le musée écrit « Rembrandt (1606-1669)
(atelier, dit) ». Le titre porte lui-même une rétractation, la ligne d'auteur nomme
l'artiste et son atelier : le sujet du volume tient en une ligne. La règle « rien n'est
choisi à la main » porte sur les listes exhaustives de l'onglet « Œuvres », qu'un tri
arbitraire pourrait flatter ; elle ne demande pas qu'un article s'ouvre au hasard. **Rien
n'est recopié** : les champs sont relus dans l'export des œuvres à la référence indiquée, et
l'export échoue si la notice change de mention ou disparaît.

**Le texte de la sélection est réécrit, en trois blocs nommés** — c'était la demande, et le
texte précédent n'était pas publiable : il annonçait « un artiste connu » comme critère.
1. **Le seuil** : au moins dix notices, une fois les orthographes réunies. Il ne juge de
   rien, il évite de commenter deux ou trois cas isolés.
2. **La vérification** : nom par nom, avec des cas réels — « Peter », « Buquet », « Prévost »
   (un nom de famille sans prénom), « Varady A » (une initiale), « Pellerin » (une
   imprimerie), les trois Mellet (nommés ensemble sur chaque dessin) ; et à l'inverse Louis
   et Aimé Duthoit, deux frères que le musée nomme côte à côte et qui gardent chacun leur
   fiche.
3. **Ce que la liste ne dit pas** : la part du doute couverte, le versement volontaire des
   musées, et le cas laissé hors périmètre.
Aucune abstraction, aucun mot de chantier, un exemple derrière chaque affirmation.

**Reprise du prototype, strictement sélective** : `build_corpus_maitres.py`, ses tests, et la
seule première visualisation — renommée **« Les mentions les plus fréquentes »** ; « Le
corpus » était un mot de chantier. La matrice des profils et la comparaison nationale ne
reviennent pas, et **ce qui les alimentait a quitté l'export** : ventilation par artiste et
comptage national par mention. Ce qui n'est pas publié ne peut pas revenir par la porte de
derrière.

**Les chiffres figés sont partis avec.** L'export et ses tests contrôlaient 3 668 / 3 669 /
3 674 / 63 : quatre nombres devenus faux en une journée. Les invariants sont désormais
**relationnels** (a ≤ b, a + b = c), et un test vérifie que les deux exports annoncent le
même effectif d'artistes. Sur la page, aucun nombre n'est écrit : tous viennent des exports,
y compris la proportion en toutes lettres (« plus de la moitié »), calculée et non rédigée.

**Navigation** : la page n'est pas encore dans le menu — c'est la phase 7, qui l'y mettra en
même temps qu'elle retirera « Comprendre les mentions ». Elle est atteignable par son URL en
attendant.

## 2026-08-02 (octies) — Tous les artistes ont leur carte, même à un seul musée

Une règle datant du 2026-07-12 remplaçait la carte par une phrase quand l'artiste n'avait
qu'un musée projetable : « une carte à un seul point ne montre pas une répartition ».

**Arbitrage utilisateur : la règle est supprimée. Tous les artistes ont leur carte.**

**Le malentendu, à retenir** : cette carte n'est pas un graphique de répartition, c'est un
**repère géographique visuel**. Un point unique situe l'artiste aussi sûrement que vingt — il
dit « c'est là, et nulle part ailleurs », ce qui est précisément l'information la plus
frappante pour les fonds locaux. Et l'échelle ne bouge pas d'une fiche à l'autre : la
projection est calée sur le fond de carte, jamais sur les points (`geo.js`,
`creerProjection`), donc la comparaison reste possible.

**Portée** : trente-deux des cent deux artistes sont concernés — le lot du 2026-08-02 les a
rendus majoritaires en proportion, et c'est ce qui a rendu la règle visible. Aucun artiste
n'a zéro musée métropolitain aujourd'hui ; le cas est traité par une phrase sous la carte,
qui reste dessinée.

**Conséquence** : le repli sans carte disparaît, avec l'action qu'il portait — le point est
sur la carte, il se choisit, il mène aux œuvres comme les autres.

## 2026-08-02 (septies) — La carte mène aux œuvres, par un panneau et non par une infobulle

Phase 3 du volume. La carte du profil disait d'où viennent les notices ; elle ne menait nulle
part. Un point porte maintenant une action : **« Voir les 276 œuvres conservées dans ce
musée »**, qui ouvre l'onglet « Œuvres » avec ce musée déjà filtré, l'artiste inchangé.

**L'action ne vit pas dans l'infobulle.** C'était le piège à éviter : une infobulle s'efface
au premier mouvement de souris, on ne peut pas viser un lien dedans. Le survol renseigne, le
**choix** engage — deux états distincts, comme sur le graphique du profil depuis le
2026-07-27. Choisir un point ouvre au flanc de la carte un panneau qui reste, et c'est lui
qui porte les liens.

**Tous les points se choisissent, de la même façon.** Auparavant, un musée à une seule notice
était un lien direct vers POP et les autres n'étaient pas cliquables : deux comportements pour
un même signe, et le lien le plus utile caché derrière un survol. **Le lien POP n'est pas
perdu, il a rejoint le panneau**, où il est lisible et cliquable. Souris, toucher, Entrée et
Espace ouvrent le panneau ; le point choisi est cerné d'encre, seul état persistant de la carte.

**Le cas sans carte est traité, et il est majoritaire.** En dessous de deux musées
projetables, la carte cède la place à une phrase — c'est la situation de trente des trente-neuf
artistes entrés le 2026-08-02, dont le doute n'est écrit que dans un seul musée. L'action
figure aussi là, sous la phrase, et dans la mention « hors cadre métropolitain » quand elle ne
concerne qu'un musée.

**Un seul état filtre.** La carte ne filtre rien : elle appelle `onVoirOeuvres(code)`, et la
page pose `museeActif` puis bascule d'onglet. Le musée choisi SUR la carte (`choisi`) est une
sélection de lecture, locale et sans effet sur la liste ; le musée qui filtre
(`museeActif`) vit dans la page. Deux états, une seule autorité — c'est la consigne « ne pas
créer deux systèmes indépendants de filtrage » prise au mot.

**Trajet inverse vérifié** : arrivé sur « Œuvres », le lecteur voit le musée dans la liste
déroulante et « Retirer ce filtre » juste à côté. Le garde-fou du sélecteur a été élargi — il
s'affiche dès qu'un filtre est actif, même chez un artiste à musée unique, pour qu'aucun filtre
posé de l'extérieur ne soit sans porte de sortie.

## 2026-08-02 (sexies) — Filtrer les œuvres par musée : deux filtres emboîtés, un seul état

Phase 2 du volume. L'onglet « Œuvres » listait la totalité des œuvres concernées d'un artiste,
filtrables par mention. Il manquait le second axe que réclame la question « quelles œuvres, et
**où** » : le musée.

**Une liste native, pas des puces.** Les mentions tiennent en cinq puces ; les musées vont
jusqu'à 24 pour un seul artiste (médiane 4). Une liste déroulante native donne le clavier, la
souris et le tactile sans une ligne de code d'accessibilité, et elle ne casse pas la colonne
quand un nom officiel est long. Le menu ne contient que les musées qui conservent une œuvre
concernée de l'artiste affiché, chacun avec son effectif, **triés par valeur décroissante**
(CLAUDE.md). Il se refait tout seul au changement d'artiste, puisqu'il dérive du fichier chargé.

**Les deux filtres sont emboîtés, dans cet ordre : le musée d'abord, la mention ensuite.** Ce
n'est pas un détail d'implémentation, c'est ce qui rend les chiffres honnêtes. Si les puces
gardaient leur effectif « artiste entier », une puce « attribué à 52 » ne rendrait que 6 œuvres
une fois Besançon choisi — un nombre affiché qui ment. Les puces se recomptent donc dans le
périmètre du musée, et les mentions absentes de ce musée disparaissent, exactement comme
disparaissent celles qui sont absentes chez l'artiste. Effet secondaire voulu : la combinaison
vide devient inatteignable à la souris. L'état vide existe quand même, avec un bouton « Tout
afficher » — un code de musée venu d'ailleurs (phase 3) doit trouver une porte de sortie.

**Un seul endroit tient l'état.** Le musée filtré (`museeActif`, code Muséofile) vit dans la
page, pas dans l'onglet : les onglets sont démontés quand on en change, et la carte du profil
devra pouvoir poser le musée AVANT d'ouvrir « Œuvres » (phase 3). C'est la consigne « ne pas
créer deux systèmes indépendants de filtrage », appliquée dès maintenant. La page vide le
filtre au changement d'artiste ; l'onglet ne le remet jamais à zéro tout seul, sinon il
effacerait un musée choisi sur la carte.

**Le code Muséofile entre dans l'export des œuvres.** Chaque œuvre porte désormais
`musee_code` : c'est la clé que porte déjà la carte du profil. Sans elle, il faudrait
rapprocher un musée par son libellé — et « musée des beaux-arts » existe dans une trentaine de
villes. Un invariant nouveau, vérifié à chaque export, impose que les œuvres comptées par
musée disent exactement la même chose que les points de la carte, artiste par artiste.

**Ce qui n'a pas bougé** : la composition des entrées, les images et leurs crédits. Le rappel
du musée actif se lit dans la liste elle-même — la répéter en toutes lettres au-dessus ajoutait
une quatrième ligne d'en-tête sur mobile pour redire ce qui était déjà écrit ; seul le bouton
« Retirer ce filtre » est conservé, à côté de la liste.

## 2026-08-02 (quinquies) — Dans l'interface publique, on dit « artistes »

Le lot 2 a changé la nature de la liste : trente des quarante nouveaux n'ont leur doute écrit
que dans un seul musée, et ce sont des dessinateurs d'imagerie, des photographes, des
peintres de fonds locaux. Le mot « maîtres » ne les décrivait plus.

**Décision utilisateur : l'interface publique dit « artistes ».** « Explorer les artistes »,
« Choisir un artiste », et partout ailleurs le même mot. Le répertoire, son champ de
recherche, son état vide et ses libellés d'accessibilité suivent.

**Le mot « maître » reste, mais pour une seule chose** : décrire la relation historique
d'une œuvre à un artiste — l'atelier du maître, son école, la distance à sa main. C'est le
vocabulaire des musées eux-mêmes, et c'est le sujet du projet. « Autour du maître » reste
donc le titre du deuxième territoire, et « la nature du lien avec le maître » reste dans
l'intro. Ce qui disparaît, c'est « maîtres » comme nom des personnes listées.

**L'effectif sort des titres.** Le titre de la rubrique était « Explorer les 63 maîtres » :
un nombre dans un titre devient faux au premier lot suivant. Il devient « Explorer les
artistes », et l'effectif se lit dans le corps du texte, depuis les données.

Le code garde ses noms internes (`nbMaitres`, `BandeauMaitre.svelte`, `maitres_instruits.csv`) :
la couche de libellé public est là pour ça, et renommer le pipeline n'apporterait rien au
lecteur.

## 2026-08-02 (quater) — Barla : identifié, compté, hors périmètre du volume

Jean-Baptiste Barla passe le test d'identité sans réserve : botaniste niçois (1817-1896),
cofondateur du muséum d'histoire naturelle de Nice, à qui il a légué sa bibliothèque et
environ 6 000 aquarelles. Ses 5 791 notices prudentes sont exactes. Elles pèsent aussi 49 %
du volume et dix-huit fois le deuxième profil.

**Décision utilisateur : Barla reste dans le registre comme personne correctement
identifiée, reste dans les statistiques nationales, et sort du périmètre du volume 1.**

**Ce n'est pas un faux positif, et le dire est une obligation.** Un écart et une sortie de
périmètre ne se ressemblent pas : l'un dit « ce n'est pas une personne, ou pas une personne
identifiable », l'autre dit « c'est bien elle, le compte est juste, mais ce n'est pas notre
sujet ». Confondre les deux reviendrait à laisser croire à une erreur de méthode là où il
n'y en a pas.

**Motif publié** : fonds botanique sériel, concentré dans un seul musée, hors de l'angle
éditorial du volume — les attributions artistiques. Ce que le musée a écrit n'est pas une
hésitation sur l'auteur d'une œuvre d'art, c'est une prudence de catalogue appliquée d'un
bout à l'autre d'une collection d'histoire naturelle.

**Mise en œuvre** — une table `HORS_PERIMETRE` dans `build_artistes.py`, à côté de `MAITRES`
et jamais confondue avec elle :

- les exports du volume ne connaissent que `MAITRES` : aucune fiche Barla, aucun point sur
  les graphiques ;
- le registre passe `TOUTES_PERSONNES` à `resout_reference` : il retrouve Barla, le compte,
  et lui donne le statut **« hors périmètre »** — un cinquième état à côté de retenu,
  écarté et à instruire, avec son motif ;
- `maitres_instruits.csv` gagne une colonne `perimetre` (« volume 1 » / « hors périmètre ») :
  la personne reste dans le registre avec ses chiffres ;
- les totaux nationaux (24 507, monoculture divulguée, hors monoculture) ne bougent pas : ils
  sont calculés par `build_exports.py`, qui ne consulte aucune de ces tables.

Deux tests figent la règle : Barla est introuvable par les exports du volume, retrouvé par le
registre, et aucune personne hors périmètre ne peut se glisser dans `MAITRES`.

## 2026-08-02 (ter) — Un seul mécanisme ajouté à la table d'identité : l'égalité stricte

La table de `build_artistes.py` disposait de deux outils : le mot entier et l'ancre « ^ » (le
nom doit être en tête). Un candidat du lot 2 leur résiste : **Jacques-Louis David**. Ses
notices prudentes portent toutes « David (1748-1825) », et la normalisation retire les
parenthèses — le pivot est « DAVID » tout court. L'ancre prendrait aussi David d'Angers
(1 363 mentions certaines), Gérard David, Jérôme David, Michel-Antoine David : une
soixantaine de personnes à écarter nommément, liste illisible et fragile.

**Décision : un motif préfixé de « = » exige le nom tout entier, rien de plus.** Deux lignes,
symétriques de l'ancre, activées sur le seul cas qui les demande. Le mécanisme est publiable
en une phrase : *quand le musée n'écrit qu'un nom de famille et des dates, on ne prend que ce
nom-là, exactement.*

**Ambiguïté résiduelle assumée** : « David (éditeur) » et « David (signataire) », une
trentaine de mentions **certaines**, tombent aussi dans le motif. Aucune notice prudente n'est
concernée — le chiffre du doute est juste ; celui des attributions certaines porte 3 %
d'incertitude. Précédent identique et documenté : les « TENIERS David » sans suffixe.

## 2026-08-02 (bis) — Lot 2 des artistes : la vérification avant la notoriété

Le registre laissait 234 formes « à instruire ». Elles ont été reprises **par notices
prudentes décroissantes**, sans considération de célébrité — c'était l'angle mort de la liste
initiale, composée à la main en 2026-07-07.

**Le lot est borné aux 50 formes portant au moins 25 notices prudentes** : 21 % des formes
restantes, 77 % des notices. Sous ce seuil, l'instruction coûte autant par personne et
rapporte trois fois moins ; la suite fera l'objet d'un lot ultérieur.

**Le test d'identité est écrit et se tranche sur la source** (détail et chiffres :
donnees.md) : prénom entier écrit par le musée, absence d'homonyme prudent capturable, dates
de vie concordantes entre graphies rapprochées. Il ne demande jamais si l'artiste est connu.

**Résultat : 40 personnes retenues, 10 formes écartées avec leur motif**, chacun publiable
tel quel. La liste passe de 63 à 103 artistes, le volume de 3 668 à 11 872 notices distinctes.

**Deux conséquences à trancher au point de contrôle 1**, parce qu'elles engagent l'éditorial
et non la méthode :

1. **Barla** (5 791 notices, 49 % du volume, un seul musée) passe le test d'identité mais
   écrasera tout graphique. La règle du 2026-07-05 — publier et divulguer partout le « hors ce
   cas » — doit être étendue aux vues du volume, ou le cas traité autrement.
2. **Le lot change la nature de la liste** : 30 des 40 nouveaux n'ont leur doute écrit que
   dans un seul musée. Ce ne sont plus des maîtres dispersés mais des fonds locaux. Le titre
   « Autour des maîtres » et l'intitulé « Explorer les maîtres » ne décrivent plus exactement
   ce que la liste contient.

**Les parents ne sont jamais fusionnés.** Louis et Aimé Duthoit, Crispin de Passe l'Ancien et
le Jeune restent deux personnes, même quand 93 et 28 de leurs notices sont communes : c'est le
musée qui hésite entre les deux frères, et cette hésitation est le sujet du projet. Les
notices partagées passent de 6 à 157 ; l'union les compte une fois, la somme des profils les
compte deux fois, et les deux nombres sont publiés séparément (invariant déjà testé).

**En revanche, une famille sans prénoms n'est pas une personne.** Les trois Mellet portent les
mêmes 41 notices et aucun prénom ne les distingue : écartés. Le père Turpin de Crissé, que le
musée n'appelle que « Père », est écarté quand son fils, nommé entièrement, est retenu.

## 2026-08-02 — Le projet devient un premier volume autonome : « Autour des maîtres »

Le site cherchait depuis des semaines à être deux choses à la fois : le panorama du doute
dans Joconde (24 507 notices, tous les cas) et l'exploration des artistes qui portent une
mention prudente (une part mesurée de ce total). Chaque page devait donc s'excuser d'être
partielle, et la navigation mélangeait des rubriques qui ne racontaient pas la même histoire.

**Ce qui est décidé.** Le projet se publie par volumes. Le premier s'appelle
**« L'inventaire du doute — Volume 1 : Autour des maîtres »** et ne traite qu'un sujet :
les artistes dont le nom apparaît dans une notice avec une formulation prudente. C'est un
tout cohérent, pas un aperçu incomplet. Les autres angles déjà défrichés — les révisions
d'attribution (« Avant / après »), les territoires, l'échelle nationale — deviennent la
matière de volumes ultérieurs. Ils ne sont pas annoncés dans l'interface : pas de rubrique
grisée, pas de « à venir ».

**Conséquence sur les chiffres.** Le total national de 24 507 notices reste publié, mais
comme **contexte** dans la page de présentation, jamais comme le sujet de la page. Le chiffre
qui gouverne le volume est celui des artistes retenus et de leurs notices. Aucun de ces deux
nombres n'est écrit en dur : ni dans un titre, ni dans un composant. Ils se lisent dans les
exports.

## 2026-08-02 — Arbitrage du prototype d'analyse : une vue sur trois est conservée

Le prototype de la branche `refactor/analyse-maitres` (commit `91fa23e`, étapes 1 et 2) a été
essayé. Verdict après essai :

- **Conservable** : la première visualisation, celle des mentions les plus fréquentes, ainsi
  que son socle de données — `src/build_corpus_maitres.py`, `corpus_maitres.json` (13 Ko) et
  `tests/test_corpus_maitres.py`, qui fige les invariants de comptage.
- **Abandonnées pour la publication** : la matrice des 63 profils (63 lignes × 8 colonnes,
  illisible sur mobile et redondante avec les fiches individuelles) et la vue de comparaison
  avec le total national, qui remettait au centre un chiffre qui n'est plus le sujet. Le
  système à trois onglets disparaît avec elles.

**Ce qu'on fait de la branche.** Elle reste **intacte**, non fusionnée, comme trace de
l'essai. Aucun report global du commit expérimental : les fichiers utiles seront repris un par
un au moment de construire la page de présentation. Ce qui est abandonné ne revient pas par
la porte de derrière.

**Pourquoi le noter.** L'essai n'est pas une perte : il a produit le contrat de données à
trois unités distinctes — notices, occurrences de mentions, associations artiste-notice —
qui reste vrai et qui protège la page suivante d'un chiffre faux.

## 2026-07-31 (ter) — La provenance publiée est dérivée du fichier, plus recopiée

`build_exports.py::provenance()` codait en dur la taille, l'empreinte et la date de version du
CSV — des valeurs relevées à la main le 2026-07-05. Elles étaient exactes, mais rien ne le
garantissait : le jour où le CSV change, le site aurait continué d'afficher l'ancienne date sous
des chiffres nouveaux. Or cette date est publique (« les chiffres se rapportent à la version
du… ») : elle doit être une mesure, pas une déclaration.

**Ce qui est mesuré désormais** : la taille vient de `CHEMIN_CSV.stat()`, l'empreinte est un MD5
calculé sur le fichier réellement lu (~9 s pour 1,1 Go), et la version du lexique vient de
`markers.VERSION` — une seule source, pour qu'un lexique v3 ne laisse pas « v2 » publié en ligne.

**La date de version vient de la source.** `download.py` écrit maintenant un relevé à côté du
fichier téléchargé (`joconde.csv.releve.json` : `Last-Modified`, MD5, taille, date de
téléchargement). Ce relevé voyage avec la donnée ; `provenance()` le lit en priorité.

**Le pipeline refuse de dater ce qu'il ne peut pas identifier.** Sans relevé (cas des CSV
téléchargés avant son introduction, comme celui du dépôt), on retombe sur la photo de référence
documentée — mais seulement si l'empreinte concorde. Sinon, arrêt avec un message qui dit quoi
faire. Publier une date invérifiable serait pire que ne rien publier.

Détail utile trouvé en chemin : **l'ETag de data.gouv est le MD5 du contenu** (vérifié), d'où la
possibilité de tout contrôler hors ligne — voir `docs/donnees.md`, T1.

**Contrôle de non-régression** : exports régénérés en entier ; `niveaux.json`, `musees.json` et
`territoires.json` sont identiques à l'octet, seul `date_generation_exports` change — il était
resté au 2026-07-05 alors que les exports avaient été refaits depuis.

## 2026-07-31 (bis) — Page « Méthode », palier 5 : se repérer dans une page longue

La page fait six sections : on ajoute de quoi savoir **où l'on est** et **revenir en haut**,
sans que la page prenne jamais la main sur le défilement du lecteur.

**Le rail de sommaire marque la section en cours.** Règle énonçable plutôt qu'un réglage
opaque : la section active est *la dernière dont le haut est passé au-dessus du quart supérieur
de la fenêtre* ; au pied de page, c'est la dernière section, qui sans cela ne pourrait jamais
devenir active. Mesure directe à chaque image d'animation (six éléments) plutôt qu'un
`IntersectionObserver` : moins de magie, cas limites traités à la main. Le repère est doublé
par `aria-current` — jamais la seule couleur.

**L'ancre `#les-maitres` passe du paragraphe au titre de la section.** C'est la cible du lien
« Pourquoi ces N artistes ? » venu d'« Explorer les maîtres » : le visiteur arrivait *sous* le
titre, donc sans savoir à quelle question la réponse répondait. Un `scroll-margin-top` évite
en plus que la cible se colle au bord haut de la fenêtre.

**Défilement doux, sauf avis contraire du système** (`prefers-reduced-motion: reduce`) : le
mouvement est un confort, pas une information. Le clic dans le sommaire déplace aussi le focus
clavier sur la section atteinte — sans dessiner de cadre à la souris.

**Retour en haut** : pastille discrète, absente tant qu'on n'a pas défilé d'un écran, réduite à
sa flèche sur petit écran (le libellé reste le nom accessible du bouton). Sommaire et bouton
sont retirés à l'impression.

## 2026-07-31 — Page « Méthode », palier 4 : quatre visuels, et pas un de plus

La page méthode reçoit **quatre visuels**, chacun au service d'**une seule règle**, placés dans
la section qui l'énonce. Rien de décoratif, aucun ajout de graphique ni de carte : ces vues
existent ailleurs dans l'application, les redonner ici transformerait la page en visite guidée.

**Trois schémas en HTML/CSS, une capture d'écran.** Les schémas (conventions d'écriture,
homonymes, règle de comptage) sont du HTML mis en forme, pas des images : ils suivent la charte,
restent nets au zoom, se lisent au clavier et par un lecteur d'écran, et se corrigent en une
ligne quand un chiffre change. Une image aurait figé un texte hors de portée du correcteur.
La capture d'écran n'est employée que pour ce qu'elle seule peut montrer : **l'interface réelle**,
pour la règle des crédits d'image (`web/static/methode/vignette-credit.png`, datée dans sa
légende).

**Chaque visuel repose sur un cas réel de la base**, jamais sur un exemple fabriqué :

1. *Comment le doute s'écrit* — trois champs « Auteur » reproduits tels quels :
   `CLOUET François (attribué)`, `VOUET Simon (?)`, `OUDRY Jean-Baptiste (attribué, ?)`.
2. *Comment on compte* — la notice `M0332004170` (Besançon), qui nomme deux fois Simon Vouet
   (« (?) » et « (atelier, dessinateur) ») : c'est le cas qui a servi à écrire la règle de
   priorité dans `src/build_artistes.py`.
3. *Identifier les artistes* — les cinq formes relevées sous le nom de Michel-Ange, dont quatre
   désignent d'autres personnes (24 notices prudentes concernées, vérifiées une par une —
   `docs/donnees.md`).
4. *Droits des images* — une œuvre de l'onglet « Œuvres » avec son crédit, sa licence CC BY-SA
   et son lien vers Wikimedia Commons.

**Vocabulaire.** Les schémas disent « mention », jamais le mot de code interne : la couche de
libellé public s'applique aussi aux figures. La couleur (pastilles, réserve en rouge) reprend
les pigments stables du projet et reste un **renfort** — chaque distinction est aussi écrite en
toutes lettres (« retenue », « Michel-Ange lui-même »), pour ne pas dépendre de la vue des
couleurs.

**Correctif au passage** : dans le crédit d'image de l'onglet « Œuvres », l'espace après le nom
de l'auteur du fichier était mangé au rendu (« Clouet ·CC BY-SA 3.0 ») — insécable ajouté.

## 2026-07-29 — Onglet « Œuvres » : les reproductions d'abord

Dans l'onglet « Œuvres », les œuvres **avec reproduction** sont désormais affichées **en
premier** (donc en page 1), avant celles au placeholder. Critère de tri : présence d'image
d'abord, puis l'ordre public des mentions (`ORDRE_FAMILLES`), puis l'ordre de rencontre (tri
stable). Vaut aussi quand un filtre par mention est actif.

But : que le visiteur voie tout de suite des images plutôt qu'une suite de cadres vides.
Compromis assumé : l'ordre reflète maintenant, en tête, la **disponibilité d'une reproduction
ouverte** — une propriété extérieure à l'œuvre (elle dépend de Wikimedia Commons), pas une
hiérarchie de doute. Le groupement par mention reste lisible au second rang, et les comptages,
filtres, pagination et données sont inchangés (seul l'ordre d'affichage change).

## 2026-07-29 — Intégration des 184 reproductions ouvertes dans l'onglet « Œuvres »

Suite du chantier images : les **184 correspondances exactes à image ouverte** (Wikimedia
Commons) sont **affichées** dans l'onglet « Œuvres », à la place du placeholder.

**Téléchargement local, jamais de hotlink.** `src/build_vignettes.py` récupère une miniature
Commons (API `iiurlwidth`, avec backoff sur HTTP 429), la ré-encode en **JPEG optimisé**
(largeur ≤ 900 px, ~110 Ko en moyenne, métadonnées retirées) via Pillow, une **seule copie par
référence** dans `data/exports/web/oeuvres_img/<ref>.jpg`. `sync-data.js` les copie vers
`web/static/oeuvres/` (servies en `/oeuvres/<ref>.jpg`, dossier gitignoré). Pillow ajouté aux
dépendances.

**Enrichissement des données.** Un index `data/exports/web/images_index.json` (référence →
`{statut, url, credit, creator, licence, licence_url, source, verifie_le}`) est fusionné dans les
fiches `oeuvres/<slug>.json` (champ `image`). `build_artistes.py` rattache aussi cet index à la
régénération complète, pour que l'enrichissement survive.

**Affichage (`OeuvresMaitre.svelte`).** L'image locale **occupe toute la vignette** (colonne
média élargie à 11 rem, 7 rem en mobile), **même gabarit que le placeholder** (boîte 4/5), en
`object-fit: contain` : proportions gardées, jamais rognée ni déformée, jamais d'upscale d'une
miniature (les fichiers locaux font 900 px). `loading="lazy"`, `alt` neutre (« Reproduction :
{titre} »), **cliquable vers la page source Wikimedia Commons**. Aucun texte par-dessus l'image :
sous la vignette, **une seule ligne discrète** (petit corps, liens atténués — jamais le
traitement cobalt du lien POP) :
- domaine public : « Domaine public · source Wikimedia Commons » ;
- Creative Commons : « [auteur] · [licence] · Wikimedia Commons » (licence et Commons liées).

Wikimedia Commons est présenté comme la **source**, jamais comme le détenteur du copyright.
L'auteur n'est affiché **que pour CC BY/BY-SA** (attribution requise) — pas pour le domaine
public, afin de ne pas mettre en avant un auteur d'œuvre incertain (le projet n'attribue rien).
Les œuvres sans reproduction ouverte gardent le **placeholder** (jamais d'image inventée).
Déclaré aussi dans la page méthode (docs/methode-et-limites.md), comme l'exige la règle « image
externe = source secondaire à déclarer ».

## 2026-07-29 — Images des œuvres : audit POP, Levier A différé, cap Wikimedia Commons

**Audit des droits photo sur POP (Palier 1 du chantier « vignettes »).** Pour les 3 668
notices prudentes, on a lu le seul champ « Crédits photographiques » (clé `PHOT`) de chaque
notice POP (jamais le reste de la page : son pied cite Etalab pour le site lui-même) et classé
en cinq statuts (`src/images_classify.py`, testé). Résultat : **aucune image sous licence
ouverte** dans tout le corpus — 0 `open`. La photographie des œuvres de nos maîtres est
massivement de la RMN, mention **« utilisation soumise à autorisation »** (2 578 `restricted`,
dont 2 342 pour le seul Louvre), le reste étant des crédits nominatifs sans licence (792
`unknown`) ou l'absence d'image (298 `unavailable`). Livrables : `data/exports/images_oeuvres.csv`,
`images_oeuvres.json`, `images_bilan.json`.

**Levier A (autorisations individuelles) — DIFFÉRÉ.** Les 792 `unknown` sont surtout des
musées municipaux (Ingres Bourdelle, beaux-arts divers) qui autorisent peut-être la
réutilisation sans l'écrire dans POP. Les solliciter un par un (statut `authorized`) est un
travail de contact hors code. **On le met de côté** ; il reste possible plus tard. Aucun
statut `authorized` n'est déduit automatiquement.

**Cap retenu : chercher les reproductions ouvertes ailleurs, sur Wikimedia Commons / Wikidata.**
Le fait qu'aucun crédit POP ne soit ouvert ne dit pas que l'œuvre n'a aucune reproduction
réutilisable. On recherche donc, pour chaque notice, une reproduction Commons réutilisable et
**rattachée avec certitude** à la notice Joconde. Règles de ce chantier (détail dans donnees.md) :
identification de l'œuvre et droits de l'image **strictement séparés** (`match_status` vs
`rights_status`) ; une correspondance n'est **exacte** que par identifiant Joconde (Wikidata
P347) explicite, ou par numéro d'inventaire + institution concordants après contrôle ; une
ressemblance de titre / auteur / musée **ne suffit jamais** ; on n'intègre une image que si
`match_status = exact` ET `rights_status ∈ {open, authorized}`. Correction d'un constat
antérieur : POP présente bien un crédit par notice (champ `PHOT`) — l'ancienne note « POP ne
présente aucun crédit par notice » est dépassée (voir donnees.md).

**Règle affinée après exécution (Palier 1).** Un même numéro d'inventaire dans une AUTRE
institution est **rejeté** comme faux rapprochement (les numéros « 516 », « SN » = sans numéro,
« INV 1 » se répètent d'un musée à l'autre) : sans institution concordante, c'est un autre objet.
`authorized` n'est jamais déduit automatiquement. **Résultat : 329 correspondances exactes
(P347), dont 184 images ouvertes réutilisables** (contre 0 sur POP) ; candidats par inventaire ;
faux rapprochements écartés. Les crédits Commons viennent des contributeurs (pas des musées) :
conservés tels quels, à revérifier avant tout affichage.

**Vérification des candidats par les métadonnées (2026-07-29, suite).** On récupère les
dimensions Wikidata (P2048/P2049) des candidats inventaire pour les recouper avec la notice.
**Deux règles :** dimensions **incompatibles → rejet** (empreinte discriminante, 262 collisions
écartées, dont 162 imagées) ; dimensions **concordantes → PAS de confirmation automatique**. Ce
dernier point est tranché après avoir constaté des faux positifs : « L'Ange gardien » (102×81)
apparié par coïncidence de taille à « Nu féminin » (102×82), titres sans rapport. Deux objets d'un
même numéro d'inventaire peuvent coïncider en dimensions ; **seul l'identifiant Joconde (P347)
promeut en « exact » automatiquement**, l'inventaire reste `a_verifier` (contrôle humain, comme
l'exige le cahier des charges « après contrôle »). Bilan : **47 candidats sur 25 références, aucun
à forte présomption** (dimensions ET titre) → l'appariement par inventaire n'apporte aucune
reproduction fiable de plus pour ce corpus ; le total réutilisable reste **184**.

## 2026-07-28 — Onglet « Œuvres » : toutes les œuvres concernées, chargées à la demande

L'onglet « Œuvres » ne montrait que quelques exemples (au plus neuf, une notice par mention
et deux pour la dominante). Il montre désormais la **totalité des œuvres concernées** par le
maître, filtrables par mention et paginées.

**Un fichier par maître, à part.** Mettre toutes les références dans `artistes.json` l'aurait
alourdi bien au-delà de son rôle (répertoire + profils, chargé d'emblée). Chaque maître reçoit
donc `data/exports/web/oeuvres/<slug>.json`, écrit par `src/build_artistes.py` dans la même
passe que l'export léger (aucune seconde lecture du CSV, aucun risque de divergence). Un champ
`slug` stable est ajouté à chaque artiste de `artistes.json` : c'est tout ce que le front a
besoin de connaître pour charger le bon fichier. Les anciens `exemples` (et leur machinerie
`MAX_EXEMPLES` / `EXEMPLES_PAR_FAMILLE`) sont retirés — devenus sans emploi.

**Source de vérité inchangée.** Les entrées viennent de `resout_reference()` et de la famille
unique déjà retenue : une référence par maître, une famille par référence, homonymes et copies
« d'après » déjà écartés (chantier de fiabilisation, 2026-07-21). Aucune nouvelle détection.

**Invariants vérifiés à l'écriture de chaque fichier** (assertions, sinon l'export échoue) :
nombre d'entrées = `maitre.doute` ; somme par famille = `maitre.familles` ; aucune référence
en double ; chaque entrée a une référence Joconde ; aucune copie dans la liste. Les totaux de
l'onglet égalent donc exactement le graphique et les jauges (même source, même comptage).

**Ordre.** Le fichier garde l'ordre de rencontre dans le CSV (non choisi à la main, comme les
anciens exemples). Le front regroupe les œuvres par mention selon l'ordre public de l'axe
(`ORDRE_FAMILLES`), tri stable : l'ordre de rencontre est conservé au sein d'une même mention.

**Chargement différé.** L'onglet ne charge que le fichier de l'artiste affiché, et seulement
quand on l'ouvre — jamais celui des autres. Un jeton anti-course écarte la réponse d'un
artiste qu'on aurait quitté avant la fin du chargement. États prévus : chargement, erreur
(avec « Réessayer »), vide.

**Filtres + pagination.** Puces « Toutes » + une par mention présente (effectif affiché,
familles absentes masquées), huit œuvres par page, pagination compacte (première, dernière,
active ± voisines, « … » ailleurs — logique isolée dans `pagination.js`, testée). Un filtre
remet la page à 1 ; changer de page recentre la lecture au début de la liste sans à-coup.
Mention active et page active repérables **sans la seule couleur** (`aria-pressed`,
`aria-current="page"`, gras/bordure), boutons de bord désactivés aux extrémités.

**Wording.** L'onglet passe à « Œuvres concernées » (vocabulaire public « œuvres »). Le bloc
« À part » des copies « d'après » est conservé tel quel (il dit encore « N notices ») : son
unification reste en réserve, hors périmètre de ce chantier.

## 2026-07-28 — Refonte de la disposition de « Explorer les artistes »

Chantier de disposition (textes, données, graphique et interactions inchangés), mené sur une
branche dédiée `refacto/les-presque-disposition` puis mergé dans `feat/les-presque-barres`
(merge `f8f0d5c`).

**Une seule grille continue à deux colonnes**, mêmes limites sur toute la page. Le bandeau
introductif horizontal pleine largeur et la séparation entre entrée et exploration sont
supprimés. L'introduction (titre + texte + lien Méthode + note de prudence) rejoint la
**colonne gauche**, au-dessus de « Choisir un artiste » + recherche/tri/liste (Repertoire).
La **colonne droite** porte le profil (portrait/identité + chiffres, onglets, contenu actif).
Le haut du titre s'aligne sur le haut du portrait ; le début du graphique apparaît dès le
premier écran d'un desktop courant.

**Colonne gauche sticky** sur desktop (hauteur bornée à l'écran, défilement interne), sans
bloquer le défilement de la colonne droite. **Mobile (≤ 720 px, seuil du Repertoire)** : une
colonne — titre + intro, **sélecteur replié** (la liste ne s'affiche pas avant le profil),
profil, onglets, contenu.

**Page centrée** (2e temps du chantier) : la route est en pleine largeur (`main.pleine`), elle
gère donc sa gouttière. La grille était collée au bord gauche → conteneur centré
(`max-width: 92rem`, `width: 100%`, `margin-inline: auto`, `padding-inline: clamp(1.25rem, 3vw,
3rem)`, `box-sizing: border-box`), marges gauche/droite équilibrées, le graphe gardant sa
largeur (≈ 60 rem). Espace masthead → grille augmenté : `padding-top: clamp(1.5rem, 3.5vw,
3.5rem)`. Composition centrée, textes/répertoire/profil/graphe restant alignés à gauche.

Point resté approximatif (à résoudre à la passe éditoriale) : la recherche démarre un peu plus
bas que les onglets — le texte introductif complet remplit la colonne étroite ; l'alignement
se resserrera quand l'intro sera raccourcie.

## 2026-07-27 (quinquies) — Le graphe nomme son axe et précaution de lecture

Deux petits ajouts au graphique du Profil, pour lever toute ambiguïté sur ce que mesure la
hauteur.

**Titre de l'axe Y** : « **Part parmi les œuvres concernées** » — horizontal, au-dessus des
graduations, aligné à gauche, dans le registre visuel des titres de territoire (petites
capitales espacées, encre atténuée, un cran plus léger pour ne pas les concurrencer). La
formulation nomme le **dénominateur** sans évoquer un degré de certitude ; préférée à
« pourcentage des mentions », plus ambigu. L'horizontal évite un texte tourné de plus à côté
des libellés déjà inclinés.

**Note de lecture** sous le graphe : « **La hauteur montre la fréquence des formulations, non
le degré de certitude des attributions.** » — petit corps, italique, atténué, dans le style
d'« En contexte » et des crédits d'image. Une précaution de lecture, pas un avertissement qui
domine. Elle dit ce que la hauteur mesure **et** ce qu'elle ne mesure pas — cohérent avec la
règle du projet (on lit ce que les musées écrivent, on n'évalue aucune certitude).

Rien d'autre ne bouge : données, points, couleurs, interactivité inchangés.

**Réglage du 2026-07-28** : ces deux éléments flottaient au bord de la colonne, comme s'ils
entouraient le graphe au niveau de la page. Ils sont désormais **alignés sur la zone de
tracé** (bord gauche du plot, `margin-left: calc(100% * 30 / 380)`) et **serrés** contre le
graphe — le titre juste au-dessus, la note juste en dessous, mise en exergue par un **filet
vertical** à gauche. Ils appartiennent visuellement au graphique. La note gagne « des
points » : « La hauteur **des points** montre la fréquence des formulations… ».

## 2026-07-27 (quater) — Taille des points : un aller-retour, décision finale = constante

Même journée, la préférence d'affichage a oscillé puis s'est fixée. L'utilisateur a d'abord
demandé de revenir à la taille **variable** (`6 + part × 10`) ; la formule a été rétablie
(commit `2f4a7f1`). Il est ensuite revenu sur ce choix (mea culpa explicite) : la **taille
constante** est rétablie et **c'est la décision qui vaut** — `R = 6`, point actif à `R_ACTIF
= 8`. La hauteur (le pourcentage) porte seule la mesure ; la taille ne code rien. Aucune de
ces bascules n'a été publiée en dehors du serveur de développement. L'interactivité
(agrandissement du point actif, atténuation des autres) est conservée dans tous les cas.

## 2026-07-27 (ter) — Interaction graphique ↔ légende, bidirectionnelle

Le survol d'un point éclairait déjà sa mention dans la légende. On ajoute le sens inverse —
survoler ou sélectionner une mention active le point et ouvre son infobulle — via **un seul
état partagé**, sans deux systèmes séparés.

### Un état unique

`interaction = { code, mode, source, ancre, … }` pilote à la fois le point actif, l'entrée
de légende active et l'infobulle. Deux modes dans le même objet :

- **temporaire** — survol (`pointerenter`) ou focus ; refermé au départ (`pointerleave`) ou
  au blur ;
- **selectionne** — clic, Entrée, Espace ou toucher ; persistant jusqu'à un second appui sur
  la même mention, la sélection d'une autre, Échap, ou un appui extérieur.

Règles clés : un **survol n'écrase jamais une sélection** (garde dans `ouvrir`), un
`pointerleave`/blur ne ferme **que** le temporaire, `stopPropagation` sur les clics empêche
le gestionnaire fenêtre de refermer aussitôt (pas d'ouverture-fermeture immédiate dans la
succession focus → pointer → clic). **Tout changement d'artiste remet l'état à zéro** (un
`$effect` sur `maitre.nom`).

### Position de l'infobulle

Toujours ancrée aux **coordonnées réelles du point** (`svgEl.querySelector('circle[data-code]')`),
même quand l'activation vient de la légende. Repli mobile : si le point est **hors de la
fenêtre** et que l'activation vient de la légende, l'infobulle s'affiche **en flux, sous la
mention active** de la légende (les deux étant alors visibles ensemble, le graphe étant
défilé plus haut). Pas de défilement automatique brutal.

### Légende accessible

- Mention **présente** : vrai `<button type="button">`, symétrique du point — survol/focus →
  temporaire, clic/Entrée/Espace → sélection. `aria-pressed` signale la sélection
  persistante ; nom accessible = libellé + nombre + pourcentage. État actif visible **hors
  couleur** : fond léger + graisse + libellé souligné (temporaire), filet encadrant en plus
  (sélection).
- Mention **absente** (valeur zéro ou inexistante) : simple `<span>` atténué, **non
  focusable, sans rôle ni gestionnaire, curseur normal**, avec une indication accessible
  « — aucune œuvre concernée ». Aucune infobulle, aucune animation.

Les trois **titres de territoire** restent non interactifs.

### Composant partagé : évolution additive

`Infobulle.svelte` reçoit une prop **`enFlux`** (défaut `false`) : rendu en position statique,
pleine largeur, pour le repli mobile. Rétrocompatible — carte, jauges et graphe inchangés
quand la prop est absente.

### Vérifié

Mention à valeur forte (Michel-Ange, « de son école » 110), mention à une œuvre (Ingres,
« ? » 1/203 — « 1 œuvre »), mention absente (Adolph Menzel, sept mentions atténuées et
inertes), activation depuis la légende (point agrandi + autres atténués + infobulle au
point), repli en flux sous la légende (mobile). Build et 8 tests JS au vert ; 184 pytest
inchangés. Données, textes et structure du graphique non modifiés.

## 2026-07-26 — Onglet « Profil » : bandeau et graphique se partagent le travail

Palier de stabilisation de l'onglet Profil, cadré par l'utilisateur. Principe directeur :
**deux zones, deux questions, jamais la même information deux fois.**

- Le **bandeau** répond à *« quelle est l'ampleur du phénomène pour cet artiste ? »* ;
- le **graphique** répond à *« comment se répartissent les mentions ? »*.

Livré en deux étapes : prototype sur quatre artistes témoins (Zuccaro, Lorrain, Bril, Titien),
validé visuellement, puis généralisation aux 63.

### Le bandeau ne raconte plus la répartition

Il gardait la mention la plus fréquente, son effectif et sa part — exactement ce que le
graphique détaille ensuite. Retirés. Le bandeau porte désormais : le nom (+ pont vers le nom
Joconde), la bio, le **volume d'œuvres concernées**, le **nombre de musées**, et le repère de
contexte. Le nombre de musées ne compte que ceux ayant publié **au moins une notice
prudente** (`nb_musees_doute`), jamais l'ensemble des musées où l'artiste apparaît — la
distinction relevée le 2026-07-22 (Téniers apparaît dans 57 musées, le doute n'est écrit que
dans 24).

### Le graphique : titre stable, phrase déterministe

- **Titre unique** pour tous : « Répartition des mentions ». Les titres littéraires écrits
  par artiste (« son école efface sa main »…) sont **archivés** dans `editorial-maitres.js`
  mais ne commandent plus l'interface. Le nom de l'artiste vit dans le bandeau, on ne le
  répète pas.
- **Une seule phrase factuelle**, générée par une **règle déterministe** identique pour tous
  (`web/src/lib/phrase-repartition.js`, fonction pure, testée hors bundler) :
  1. égalité d'effectif en tête → citer les mentions à égalité, au pluriel ;
  2. 1re mention ≥ 60 % → la citer seule ;
  3. sinon 1re + 2e ≥ 70 % **et** 2e ≥ 20 % → citer les deux ;
  4. sinon → « se répartissent entre plusieurs mentions, sans qu'une seule ne s'impose ».
  La phrase **cite la mention exacte** et ne transforme jamais une formulation prudente en
  attribution certaine (« portent la mention "attribué à" », jamais « lui sont attribuées »).
  Vocabulaire écarté : corpus, profil d'attribution, domine nettement, efface sa main.

### Dot plot à points de taille constante

Le nuage encodait le pourcentage par la **position** ET par la **surface** de la bulle —
deux fois la même information (même dénominateur). Les points ont désormais un **rayon
constant** ; seule la position verticale (le pourcentage) porte la mesure. Position, mentions
sur l'axe, trois territoires, couleurs : inchangés. Le point actif est à peine renforcé au
survol/focus, et **éclaire l'entrée correspondante dans la légende**.

### Infobulles : définition factuelle depuis une source canonique

La dernière ligne, interprétative, est remplacée par une **définition neutre et stable**,
identique pour tous les artistes, tenue dans un champ unique `definition` de
`familles-public.js` (« Œuvre rattachée à l'école de l'artiste. » plutôt que « Plutôt son
école que sa main. »). Ce champ est **distinct de `corps`**, laissé au service de la page
« Comprendre les mentions » (hors périmètre de ce palier). Chaque infobulle porte : la
mention, « N œuvres sur T », le pourcentage, la définition.

### Vocabulaire « œuvres concernées »

Dans le périmètre de l'onglet Profil (bandeau, répertoire, graphique, infobulles), le
comptage se dit en **œuvres concernées** : le bouton de tri « Notices » devient « Œuvres »,
l'infobulle passe de « 30 notices » à « 30 œuvres sur 37 — 81 % ». La fonction `notices()`
reste employée **hors périmètre**, dans les onglets Œuvres et Musées — voir le signalement
ci-dessous.

### Phrase de lecture de l'échelle supprimée

« De gauche à droite, le lien à la main du maître se desserre. » est retirée sans
remplacement : les trois intitulés de territoire et la légende suffisent.

### Page Méthode

Ajout de la précision d'unité : *l'unité technique est la notice Joconde ; dans les pages de
lecture ces notices sont désignées « œuvres concernées » ; une notice peut exceptionnellement
documenter plusieurs éléments.* Rappel du seuil (dix notices prudentes uniques après
désambiguïsation) et du compte de musées (notices prudentes seulement).

### Accessibilité

Le point du graphique gagne un gestionnaire clavier (Entrée/Espace basculent l'infobulle, en
parité avec le toucher) : le focus l'affichait déjà, l'ajout lève l'avertissement a11y du
clic sans équivalent clavier.

### Le cas Claude Lorrain — tranché : on garde la règle (option A, 2026-07-26)

Claude Lorrain affiche « 17 des 20 œuvres concernées portent la mention "attribué à" ; les
autres formulations restent minoritaires ». Le cahier des charges donnait, pour illustrer le
format « deux mentions », un exemple qui reprenait **par coïncidence les chiffres exacts de
Lorrain** (17 / 20 / 3) et nommait la 2ᵉ formule (« 3 portent la mention "de son école" »).
La règle déterministe (≥ 60 % → citer seule) produit l'autre formulation. **Les deux sont
exactes et se lisent bien** : ce n'était pas un défaut, seulement un choix rédactionnel sur
un artiste très majoritaire (85 %, 2ᵉ formule = 3 œuvres). Décision : **on garde la règle**,
Lorrain reste en « cite seule ».

Correctif d'une note antérieure erronée : il avait été écrit qu'« abaisser le seuil seule »
ferait citer les deux. C'est **faux dans les deux sens**. (a) Abaisser ce seuil rend « cite
seule » *plus* fréquent, pas moins (mesuré sur les 63 : seuil 50 % → 47 « seule » ; 60 % →
40 ; 70 % → 33). (b) De toute façon Lorrain ne pourrait pas atteindre « deux » : sa 2ᵉ
formule pèse 15 %, sous le plancher de 20 % qui protège de citer une mention marginale. Le
levier réel serait de *monter* le seuil « seule » — mais à 70 % il ferait basculer 7
artistes, dont un à tort (Joseph Vernet, 69/10, tomberait en « dispersé » alors qu'une
formule domine clairement). La règle 60 / 70 / 20 est donc **conservée telle quelle**.

### Un point laissé ouvert, à trancher plus tard

**Onglets Œuvres et Musées, hors périmètre** : « notices » y subsiste (`OeuvresMaitre` :
   « À part : N notices » ; `CarteMaitre` : « D'où viennent ces notices », « N notices
   concernées »). À unifier dans un chantier ultérieur. Le champ `corps` de
   `familles-public.js` garde de même son ancienne formulation pour /echelle.

Aucun artiste n'est exactement au seuil de dix (minimum réel : Titien, 11). Le cas d'égalité
existe pour de vrai (Paul Bril, 7 = 7) et est couvert, plus un test synthétique à trois
mentions.

## 2026-07-22 (septies) — Les 36 angles écrits, et un pont entre deux noms

### Le pont de nom, demandé pour Michel-Ange, appliqué à quatorze

**Problème posé par l'utilisateur** : la fiche titre « Michel-Ange » quand ses œuvres, dans
l'onglet voisin, portent « BUONARROTI Michelangelo (attribué à) ». Rien ne relie les deux, et
le lecteur peut prendre le second pour un autre artiste — ou pour le titre d'une œuvre.

**Solution** : l'en-tête affiche le nom courant suivi du nom d'état civil, en ordre naturel —
**Michel-Ange (Michelangelo Buonarroti)** — dans un corps plus petit, sur la même ligne. Les
notices, elles, gardent le **verbatim de Joconde**, jamais réécrit : c'est ce que le musée a
écrit, et c'est ce que le lecteur retrouvera sur POP.

La demande portait sur Michel-Ange ; le défaut est le même pour **quatorze** maîtres connus
sous un surnom qui n'apparaît jamais tel quel dans la base : Le Primatice (Francesco
Primaticcio), Le Tintoret (Jacopo Robusti), Le Corrège (Antonio Allegri), Véronèse (Paolo
Caliari), Titien (Tiziano Vecellio), Raphaël (Raffaello Sanzio), Le Guerchin (Giovanni
Francesco Barbieri), Jules Romain (Giulio Pippi), Le Parmesan (Francesco Mazzuola), Perino
del Vaga (Piero Bonaccorsi), Le Pérugin (Pietro Vannucci), Claude Lorrain (Claude Gellée),
Botticelli (Alessandro Filipepi). Traiter Michel-Ange seul aurait laissé le même piège
treize fois. Les maîtres dont le titre est déjà le nom porté par les notices n'ont pas de
pont : il n'apprendrait rien.

Champ optionnel `nomCivil` dans la couche éditoriale — donc jamais une donnée Joconde.

### Les 36 en-têtes de graphique

Les 36 maîtres du lot gardaient l'en-tête généré : un titre passe-partout (« Comment les
musées rattachent ces œuvres à X ») et une phrase de lecture. Ils ont maintenant leur angle
propre, au même gabarit que les 27 — titre de 4 à 9 mots portant l'angle, sous-titre
apportant la preuve chiffrée sans reprendre les mots du titre.

**Règle du temps 7 appliquée d'emblée** : chaque mention nommée est cherchée **par son code**
(`notices('ecole_de')`), jamais par son rang. Aucun de ces 36 sous-titres ne pourra mentir si
le classement bascule au prochain lot.

Ce que les angles racontent, et qui ne se voyait pas :

- **Adolph Menzel** : ses 47 œuvres concernées sont *toutes* dites « de son école », dans un
  seul musée. Une formule, un lieu.
- **Le Parmesan** : 63 œuvres, un unique établissement.
- **Carlo Maratti** : 37 des 45 sortent de son atelier, 7 seulement lui sont attribuées —
  « son atelier signe pour lui ».
- **Federico Zuccaro** : 30 sur 37 « de son école », 3 portent son nom sans détour.
- **Nicolas de Largillière** : 23 œuvres dans 15 musées, aucun n'en réunissant plus de deux.
- **Paul Bril** : autant d'œuvres attribuées que d'œuvres ne retenant que sa manière.

Six formulations ont été resserrées à la relecture : deux ne se comprenaient qu'avec le titre
(« en sortent » sans dire de quoi), une disait « seulement » d'un nombre plus grand que celui
qui la précédait, une reprenait l'angle d'un autre maître (« deux lectures », déjà celui de
Guido Reni).

## 2026-07-22 (sexies) — Les portraits des 36 maîtres

Plus de la moitié des fiches affichaient « Pas de portrait fiable disponible ». **33 des 36**
maîtres du nouveau lot en ont un désormais ; le site en compte **60 sur 63**.

### La route est inchangée, la vérification est nouvelle

Même chemin que pour les 27 : Wikidata (propriété P18) → fichier Commons → licence et auteur
par l'API → **téléchargement local**, jamais de hotlink. Ce qui change, c'est qu'un QID n'est
plus choisi à la main : `web/scripts/verifie_qid.py` le cherche, puis contrôle le libellé, la
description, la qualité d'être humain (P31 = Q5), la présence d'un portrait — et surtout les
**dates**, qui doivent concorder avec la ligne de repérage déjà écrite.

Ce contrôle croisé a payé : 29 concordances exactes, **7 désaccords** (voir donnees.md).
Deux bios portaient une date ferme là où les sources divergent — Gaspard Dughet et Paul Bril
passent à « vers ». La règle est celle du fichier éditorial : *la prudence sur les dates est
du même ordre que celle des musées sur les attributions*.

### Trois maîtres restent sans portrait, et c'est écrit

Gaspard Dughet, Domenico Campagnola et Laurent de La Hyre n'ont aucun portrait sur Wikidata.
Leur fiche continue d'afficher le repli. **On ne comble pas un manque par une image
approximative** — c'est la même règle que pour les attributions.

### Trois corrections trouvées en chemin

1. **Le manifeste des crédits n'était pas versionné.** Les 27 images étaient dans git, mais
   `portraits.json` vivait dans `web/static/data`, ignoré par git : une licence perdue au
   premier clone. Le manifeste est désormais un export versionné
   (`data/exports/web/portraits.json`), recopié par `npm run sync:data` comme les autres.
2. **Les crédits parlaient anglais, et se répétaient.** Commons renvoie « Unknown
   artistUnknown artist » (deux éléments concaténés), « Attributed to X », « After X ». Le
   script dédoublonne et traduit ces **enrobages** — ce ne sont pas des noms, mais des
   mentions de statut. Le nom exigé par la licence est conservé intact.
3. **La légende écrivait « par attribué à Paul Bril ».** Elle distingue maintenant un nom
   d'auteur (« par X ») d'une mention de statut (« attribué à X », « d'après X », « auteur
   inconnu »), qui se suffit à elle-même. Et la détection d'autoportrait ignore accents et
   traits d'union — « Louis-Léopold Boilly » au manifeste, « Louis Léopold Boilly » dans le
   projet. Elle reste une **égalité stricte** : « d'après Philippe de Champaigne » contient
   le nom du maître sans être un autoportrait.

### Une licence affichée qui était devenue fausse

La page Méthode annonçait que chaque portrait porte « son auteur et sa licence (domaine
public) ». Sur les 60 images, **six n'y sont pas** : trois en CC0 et trois en **CC BY-SA
3.0**, qui impose de citer l'auteur. La phrase dit maintenant « le plus souvent le domaine
public, parfois une licence Creative Commons qui impose de citer l'auteur », et signale les
trois artistes sans portrait.

### Le regard

Le manifeste porte pour chaque portrait un sens de regard : ceux qui regardent à droite sont
retournés à l'affichage pour faire face au graphique, placé à leur gauche. Relecture du
nouveau lot sur planche de contact : seuls **Adolph Menzel** et **Baccio Bandinelli** sont
nettement tournés à droite. Les gravures portant une inscription (Tempesta, Zuccaro, Caldara,
Le Pérugin, Claude Lorrain) ne sont **jamais** retournées — cela inverserait leur texte.

## 2026-07-22 (quinquies) — Temps 8 : les textes publics, et l'engagement tenu

Dernière étape du chantier. Deux natures de travail, à ne pas confondre.

### Ce qu'on ne réécrit pas

Les **journaux datés** — `donnees.md`, les entrées de `decisions.md`, les phases closes de
`roadmap.md` — contiennent des phrases comme « Total des 27 : 2 341 segments → 2 225
références ». Elles sont **exactes à leur date** et racontent comment le chiffre s'est
fabriqué. Les corriger reviendrait à effacer l'erreur qu'on vient de documenter. Elles
restent telles quelles.

Seuls sont révisés les **documents vivants**, qui décrivent l'état courant.

### Ce qui a été révisé

- `charte-graphique.md` : le titre public n'est plus « Explorer les 27 maîtres » mais
  « Explorer les N maîtres », **le nombre étant lu dans les données**. Un titre qui fige un
  effectif devient faux au premier ajout — c'est déjà arrivé deux fois.
- `dataviz-les-presque.md` : sélection (27 → 63, seuil 20 → 10, regroupement des graphies),
  effectif, portée du filtre. Surtout, une **note en tête sur le changement d'axe** : la
  spec décrivait un axe portant le nombre d'œuvres sur un plafond commun, ce qui n'est plus
  vrai depuis le temps 7.
- `architecture-editoriale.md`, `les-presque/+page.js`, et les tâches encore ouvertes de la
  roadmap qui parlaient des « 27 vedettes ». La réserve « garder 27 ou réintégrer
  Bruegel/Cranach » est **sans objet** : ils sont au registre, à l'état « à instruire ».

### L'engagement de transparence, enfin tenu

La décision 4 du 2026-07-21 promettait que « la liste des candidats examinés est publiée
avec leur nombre de notices, y compris ceux écartés et le motif ». Le registre existait
depuis le temps 5 (`candidats_maitres.csv`) mais **le site n'en disait rien**. La page
Méthode porte maintenant un paragraphe qui l'énonce, avec des nombres lus dans un nouvel
export `data/exports/web/registre.json` :

> Tous les noms qui atteignent le seuil ont été relevés : ils sont **330**, et chacun porte
> un état — retenu, écarté avec sa raison, ou encore à examiner. Un nom encore à examiner
> **n'est pas un nom rejeté** : c'est un nom dont la vérification n'a pas été faite.
> Aujourd'hui **74** formes d'écriture sont rattachées aux 63 artistes retenus, **22** sont
> écartées parce qu'il ne s'agit pas d'une personne, **234** restent à examiner.

Une première rédaction disait « puis examinés un par un » **et** « 234 restent à examiner » —
deux phrases contradictoires dans le même paragraphe. Corrigé.

Deux autres passages complétés dans la même page :

- **les homonymes**, absents jusqu'ici alors qu'ils sont le piège le plus coûteux du projet :
  « sous “Michel-Ange”, les musées ont aussi rangé Corneille Michel-Ange, peintre lyonnais du
  XVII<sup>e</sup> siècle ; sous “Raphaël”, une cinquantaine de personnes qui le portent comme
  prénom » ;
- **une œuvre peut concerner deux artistes** : quand un musée hésite entre deux noms, la
  notice apparaît sur les deux fiches mais ne compte qu'une œuvre — « c'est pourquoi le total
  de la liste n'est pas la somme des fiches ». Six notices sont dans ce cas.

Le vocabulaire interne (appartenances, notices, registre, instruction) **n'apparaît nulle
part** dans ces textes : la page dit « formes d'écriture », « état », « encore à examiner ».

## 2026-07-22 (quater) — Temps 7 : ce que 63 maîtres cassent dans le front

Contrôle complet de la rubrique avec la liste élargie. Le front ne s'est pas *cassé* — il
dégradait proprement — mais il disait des choses fausses et montrait des graphiques
illisibles. Quatre corrections, dont une de fond.

### 1. L'axe du graphique passe du nombre à la part (correction de fond)

Le nuage des mentions portait le **nombre** d'œuvres sur un plafond commun à tous les
maîtres — le maximum observé, 240. Avec 27 maîtres allant de 20 à 310 notices, c'était
tenable. À 63 maîtres allant de **11 à 310**, la moitié des profils s'écrasent au sol :
Botticelli (17 notices) affichait quatre points collés à la ligne de base, indistinguables.
On ne pouvait plus « y lire une hiérarchie », donc **la forme était mauvaise** (CLAUDE.md).

L'axe porte désormais la **part des œuvres concernées du maître, de 0 à 100 %**. La règle de
la charte est respectée dans ses deux termes : l'échelle reste **commune et fixe** pour les
63 fiches, et chaque profil redevient lisible. La comparaison porte sur la **forme** du
profil plutôt que sur le volume — et le volume n'est pas perdu : il est écrit dans l'en-tête
(« Parmi les 17 œuvres… »), il classe le répertoire, et chaque infobulle donne le nombre
exact. Botticelli montre maintenant « de son école » à 71 %, son atelier à 18 %.

C'est la seule décision de fond du temps 7 ; elle est réversible d'un commit.

### 2. Trois en-têtes rédigés disaient l'inverse de leurs chiffres

Le point que la roadmap annonçait — « les nombres suivent seuls, les angles non » — s'est
vérifié, et pire que prévu : ce ne sont pas les angles qui ont dérivé, ce sont les **faits**.

| Maître | Affiché | Données |
|---|---|---|
| Le Primatice | « 125 portent “attribué à”, 71 “de son école” » | l'inverse : école 125, attribué 71 |
| Raphaël | « 12 lui sont attribuées, 8 renvoient à son école » | l'inverse : école 12, attribué 8 |
| Michel-Ange | « Deux fois plus » | 110 contre 37, soit près de trois fois |

**Cause commune** : `n` et `second` désignent des **rangs**, pas des mentions. Vingt et un
sous-titres nommaient une mention en dur à côté d'une variable de rang. Tant que le
classement ne bougeait pas, ils disaient vrai ; le jour où l'école est passée devant
« attribué à » chez Le Primatice et Raphaël, ils se sont mis à mentir sans qu'aucun test
n'existe pour le voir.

**Les 21 sont convertis** : dès qu'une phrase nomme une mention, elle la cherche par son code
(`notices('ecole_de')`), jamais par son rang. Vérification faite : les 24 sous-titres non
fautifs rendent exactement le même texte qu'avant la conversion.

### 3. Les 36 nouveaux maîtres n'avaient pas de ligne de repérage

Un visiteur tombait sur « Perino del Vaga » sans une ligne pour le situer. Les 36 lignes sont
écrites, au gabarit strict du fichier (« [Activité] [nationalité] du [siècle], [dates]. »),
sans mouvement, sans école, sans fonction de cour.

**Les dates viennent d'abord de la base elle-même** : le champ `Auteur` de Joconde porte
souvent les années entre parenthèses, et l'on peut les compter — « Bouchardon Edme
(1698-1762) » apparaît dans 1 128 notices concordantes, « Dürer Albrecht (1471-1528) » dans
344. Elles sont ensuite croisées avec les notices d'autorité. Le « vers » est posé partout où
la base se contredit (Barocci : 1535, 1540 et 1528 ; Campagnola : 1484 et 1500 à égalité) ou
diverge des notices (Botticelli : 1444 dans la base, 1445 ailleurs). Adolph Menzel est le
seul dont la base ne porte **aucune** date.

Ces 36 gardent l'**en-tête de graphique généré** : écrire 36 angles à la main demande une
passe rédactionnelle à part. Ils n'ont pas non plus de portrait — le repli « Pas de portrait
fiable disponible » s'affiche, ce qui est correct mais visible sur plus de la moitié des
fiches.

### 4. Les textes et les nombres figés

- Le nombre en toutes lettres venait d'une table allant de vingt-quatre à trente : elle a
  rendu « 63 » en chiffres dans un corps de texte. Remplacée par `enLettres()` dans
  `joconde.js`, qui couvre 0 à 99 — y compris les pièges du français (soixante et onze,
  quatre-vingts, quatre-vingt-un).
- « au moins **vingt** notices » → **dix**, dans la page Méthode (le seuil a changé au
  temps 5). Ancre `#les-27` → `#les-maitres`.
- « les **vingt-sept** noms de référence » et « Les **27** noms de référence » deviennent
  l'effectif réel, lu dans les données. `vue_ensemble.json` publie `nb_maitres` pour que
  « Comprendre les mentions » n'ait pas à charger 372 Ko pour connaître un nombre.
- La phrase de « Ce que disent les chiffres » portait encore la conclusion inversée : elle
  dit maintenant qu'« attribué à » **reste la plus fréquente** chez les maîtres retenus, et
  que ce qui change est la place de « de son école ».
- **Les deux panneaux comptent enfin la même chose** : le panneau de droite affichait
  « 3 674 notices concernées » alors que 3 674 sont des *appartenances*. Il est passé aux
  notices distinctes (**3 668**), comme le panneau national. L'avertissement « les parts ne
  s'additionnent pas à 100 % » couvrait déjà ce cas.

### Ce qui n'a pas été touché

Le style (chantier distinct, en réserve), les portraits des 36, les angles écrits des 36, et
la révision d'ensemble des textes publics — temps 8. La page Méthode ne mentionne pas encore
le registre des candidats publié au temps 5 : elle le devra.

## 2026-07-22 (ter) — Recouvrement entre profils : une somme n'est pas une union

Vérification demandée avant d'ouvrir le temps 7, et elle était nécessaire : `doute_dans_liste`
était calculé par **somme des profils**, ce qui compte deux fois toute notice nommant deux
maîtres retenus. Mesure faite sur les 1 023 705 lignes du CSV.

### Ce que vaut le recouvrement

| | somme des appartenances | union des notices | écart |
|---|---:|---:|---:|
| notices prudentes | 3 674 | **3 668** | 6 |
| attributions certaines | 34 898 | **34 598** | 300 |
| copies « d'après » | 6 778 | **6 767** | 11 |

**Six notices** portent deux maîtres retenus — les voici, publiées en clair dans
`artistes.json` (`references_partagees`) :

| Référence | Maîtres | Formule |
|---|---|---|
| `M0347001723` | Michel-Ange · Andrea del Sarto | « ? » pour les deux |
| `02860008133` | Annibale Carracci · Ludovico Carracci | « ? » pour les deux |
| `50520000014` | Francesco Vanni · Ludovico Carracci | « ? » pour les deux |
| `07480012416` | Luca Giordano · Pier Francesco Mola | « ? » pour les deux |
| `08030000599` | Simon Vouet · Sébastien Bourdon | « école de » pour les deux |
| `000PE008806` | Rubens · Van Dyck | « atelier » / « ? » |

Cinq sur six portent le point d'interrogation : ce sont des notices où le musée hésite
**entre deux noms**, ce qui est le cas de doute le plus fort qui soit. Elles méritent d'être
gardées visibles, pas gommées.

### Deux mesures désormais distinguées dans l'export

- **appartenances** : le lien maître-notice. C'est ce que totalisent les fiches, et c'est la
  bonne base pour une répartition interne (les familles y somment exactement à 100 %).
- **notices** : les références Joconde distinctes. **Seule mesure comparable au total
  national**, et seule base admissible pour en déduire ce qui est hors liste.

`doute_hors_liste` passe de 20 833 à **20 839** : il se calcule maintenant par
`24 507 − 3 668`, jamais par soustraction d'une somme d'appartenances. La part nationale
passe de 14,99 % à **14,97 %** — l'écart est minime, la règle ne l'est pas.

**Les ventilations ne s'additionnent pas non plus.** La somme des familles en notices
distinctes vaut 3 669, celle des niveaux aussi : `000PE008806` relève de « atelier » (niveau
2) pour Rubens et de « ? » (niveau 1) pour Van Dyck, donc elle est comptée dans deux familles
et deux niveaux. Interdiction confirmée d'additionner les familles — elle valait déjà pour le
recouvrement des formules, elle vaut maintenant aussi pour le recouvrement des profils.

### Invariants et tests ajoutés

Dans `build_artistes.py` : union ≤ somme pour les trois catégories ; l'écart doit valoir
**exactement** le nombre de liens en trop portés par les références partagées ; la somme des
profils doit égaler les appartenances. Dans `build_vue_ensemble.py` : `hors_liste + union =
total national`. Et cinq tests dans `tests/test_artistes.py` qui relisent l'export publié —
dont un qui vérifie que l'écart est expliqué, pas approximé.

### Correction d'une conclusion fautive

La note du temps 6 affirmait qu'un musée doutant d'un grand nom « dit plus souvent “école
de” que “attribué à” ». **Les chiffres disent l'inverse** : 43 % contre 35 %. Formulation
exacte, désormais inscrite dans `message_central` :

> « Attribué à » reste la formulation la plus fréquente parmi les maîtres retenus, mais
> « école de » y occupe une place beaucoup plus importante que dans l'ensemble de
> Joconde : 35 % contre 7,6 %.

Ce n'est pas un renversement de hiérarchie, c'est un déplacement de proportion — et c'est
déjà un constat fort. Une conclusion qui contredit ses propres chiffres est exactement ce
que ce chantier existe pour éliminer.

Côté front, deux branchements mécaniques : la page « échelle » lit les **appartenances**
(sa répartition interne doit sommer à 100 %), la page « méthode » lit les **notices** (elle
compare au total national). Aucune retouche éditoriale — temps 7 et 8.

## 2026-07-22 (bis) — Temps 6 : régénération des exports

Première fois depuis l'audit que les fichiers publiés bougent. `artistes.json` (63 maîtres)
puis `vue_ensemble.json`, qui en dérive sans repasser sur le CSV.

**Invariants revérifiés sur les 63** : familles = niveaux = somme des musées = doute ;
et le seuil lui-même est désormais vérifié à la génération — aucun maître sous 10.

### Ce que la liste élargie change dans la vue d'ensemble

| | avant (27) | après (63) |
|---|---:|---:|
| notices prudentes de la liste | 2 341 | **3 674** |
| part du doute national (24 507) | 9,6 % | **15,0 %** |

**Le message central de la section tient, et c'est vérifié, pas supposé.** « Attribué à »
domine le doute national (17 926 sur 24 507, soit 73 %) mais ne pèse que **43 %** dans la
liste ; « école de » fait **35 %** de la liste contre 7,6 % au national. Le contraste qui
justifie la section est même plus net qu'avec 27 noms. De même, le niveau 2 « Autour de
lui » reste majoritaire dans la liste (48 %) alors qu'il est minoritaire partout ailleurs.

### Deux corrections faites en régénérant

**1. Les clés `dans_27` / `hors_27` sont renommées `dans_liste` / `hors_liste`**
(et `critere_27` → `critere_liste`). Un nom de champ qui fige un effectif devient faux au
premier ajout — et il aurait menti dès cette régénération. Les textes embarqués dans
l'export qui disaient « les 27 noms retenus » et « hors des 27 noms » sont corrigés : le
JSON généré ne contient plus une seule occurrence de « 27 ». Quatre références côté front
ont suivi (`echelle`, `methode`) : **renommage mécanique uniquement**, aucune retouche
éditoriale — c'est le temps 7 et le temps 8.

**2. Une erreur de mesure dans la documentation du temps 5, corrigée.** J'avais écrit
« David Téniers est prudemment attribué dans 57 musées ». Faux : 57 est le nombre de musées
où il **apparaît**, toutes catégories confondues ; le doute n'est écrit que dans **24**.
`registre_maitres.py` publie désormais les **deux** colonnes, `musees_presence` et
`musees_doute`, et `docs/donnees.md` est corrigé. Confondre les deux ferait dire au chiffre
bien plus qu'il ne dit — c'est exactement le genre de glissement que ce chantier corrige.

Le doute est parfois très concentré : Le Parmesan (63 notices), Baccio Bandinelli (45) et
Adolph Menzel (47) ne sont concernés que dans **un seul musée** chacun.

### Un point à surveiller

`artistes.json` passe de 189 Ko à **372 Ko** — il double, et il est chargé par le front. Le
projet s'est fixé des exports légers. Ce n'est pas bloquant aujourd'hui, mais un lot
supplémentaire de maîtres reposera la question : il faudra probablement séparer le détail
par maître (musées, exemples) du répertoire d'entrée. À trancher au temps 7.

Le front compile (`npm run build` ✓) après synchronisation des données. Son **contrôle
visuel et éditorial n'est pas fait** : c'est le temps 7.

## 2026-07-22 — Temps 5 : publication progressive sur registre exhaustif

**Cadrage arbitré par l'utilisateur** (2026-07-22), après une proposition qui parlait de
« publier le reste comme candidats écartés faute d'instruction ». Formulation refusée, et
avec raison : ces candidats **ne sont pas écartés par les données, ils sont encore à
instruire**. Les présenter comme écartés serait une sélection arbitraire, contraire au seuil
de 10 qu'on vient d'adopter.

**Règle retenue : publication progressive sur registre exhaustif.**

1. Les 330 graphies restent dans un **registre complet et vérifiable**.
2. Les graphies sont **regroupées par personne canonique** : le seuil s'applique à une
   personne, jamais à une graphie.
3. On instruit une **première trentaine**, en commençant par les identités les plus nettes
   et les faux négatifs évidents.
4. Chaque candidat porte un **statut** parmi quatre : vérifié et retenu ; vérifié mais
   écarté, avec une raison précise ; ambigu ; encore à instruire.
5. **Seules les personnes vérifiées entrent dans le front.**
6. Les autres pourront être ajoutées **par lots ultérieurs**.

**Critères annoncés de la première trentaine** — la notoriété seule ne suffit pas :
identité suffisamment claire ; au moins 10 références uniques **après regroupement des
alias** ; absence de confusion familiale ou homonymique non résolue ; matière suffisante
pour une fiche ; diversité des situations, **sans exiger plusieurs musées**.

### Ce que le regroupement change

Le comptage par graphie sous-estime systématiquement. Une fois les alias réunis :
Le Guerchin passe de 93 à **101** (Barbieri + Guercino + Guerchin), Salvator Rosa de 38 à
**50** (Salvator + Salvatore), Carlo Maratti de 37 à **45** (Maratti + Maratta), Le Pérugin
de 20 à **21** (Vannucci + Pérugin), Botticelli de 15 à **17** (Botticelli + Filipepi).
C'est bien la personne, et non la graphie, qui franchit le seuil.

### 36 candidats instruits, 63 maîtres retenus au total

Tous dépassent 10 références prudentes uniques après regroupement — le plus bas est le
Titien, à 11, déjà dans la liste. **Aucun n'a été retenu sur sa seule notoriété.**

**Confusions familiales séparées nommément** : Taddeo Zuccaro (frère de Federico, 52
mentions certaines), Jean-Baptiste de Champaigne (neveu de Philippe, 8 prudentes), Jules et
Julien Boilly (fils de Louis Léopold), David Téniers le Vieux et Abraham Téniers, Giulio
Campagnola, Orazio Cambiaso, Jacques-Philippe et Jean-Baptiste Bouchardon, Bartolommeo et
Clemente Bandinelli, Ambrogio Barocci, Jacques Oudry, Philippe et Louis de La Hyre, Hans
Dürer. **Toutes sont sous le seuil de leur côté** : les séparer ne fait perdre aucun
candidat qualifiant.

**Ambiguïté résiduelle assumée et documentée** : « TENIERS David » sans suffixe vaut David
Téniers **le Jeune** par convention Joconde (peinture de genre). Les formes explicitement
« Ier » ou « le Vieux » ne portent aucune mention prudente, ce qui rend la convention sans
effet sur le chiffre publié.

### Le registre exhaustif et ses quatre états

`data/exports/candidats_maitres.csv` porte désormais une colonne **statut** sur ses
330 formes : **74 retenues** (elles se rattachent aux 63 personnes), **22 écartées**,
**234 à instruire**.

Les 22 écarts sont **vérifiés, pas déduits** : manufactures (Creil, Sèvres, Montereau,
Delft, Les Islettes, cristaux du Creusot, Pont-des-Vernes), imprimeries (Wissembourg,
Baster & Vieillemard, Champenois), faïenceries (Sarreguemines, Creil & Montereau), raisons
sociales (Pellerin & Cie, Burckardt Charles Successeurs, Tissage de Lyon), mentions
collectives (« CARRACCI l'un des » 78, « COYPEL l'un des » 60), « anonyme » (152), et trois
mentions **qui ne portent aucun nom d'auteur** : le champ contient seulement « Attribué à »
(30 notices), « attribué à) » (15), « B (atelier) » (12).

**On n'écarte pas sur un signe faible.** Les mots « fils », « père » et « frères » ont été
retirés du détecteur : « MELLET Jules Fils », « LACOUR Pierre Fils », « NEYRET Frères »
désignent souvent une personne d'une dynastie, pas un atelier. Ils repassent « à
instruire ». Le nombre d'écarts descend de 24 à 22 — le sens du registre y gagne.

### Deux découvertes

- **« DAVID (1748-1825) »**, 26 notices prudentes dans 17 musées, est presque certainement
  Jacques-Louis David. Il reste **« à instruire »** : le nom-pivot n'est qu'un patronyme, et
  la vérification n'a pas été faite. C'est le candidat le plus évident du prochain lot.
- **Deux références ont changé de verdict**, et ce sont les tests qui l'ont signalé :
  `M0350002026` (« DUGHET Gaspard (dit) POUSSIN Gaspard (entourage de) ») et `50350011790`
  (« Romain Jules ») étaient protégées comme *écartées de Nicolas Poussin et de
  Michel-Ange* ; elles reviennent maintenant à **Gaspard Dughet** et à **Jules Romain**,
  retenus à leur propre nom. Les témoins ont été mis à jour en conséquence.

Le seuil inscrit dans `artistes.json` passe de 20 à 10. **Le front n'est pas régénéré** :
point d'arrêt, la liste doit être validée avant le temps 6.

## 2026-07-21 (octies) — Temps 4 : tous les candidats de la base, au seuil de 10

`src/candidats_maitres.py` compte, pour **toute** forme d'auteur de la base, les références
distinctes portant une formulation prudente (copies exclues), et publie celles qui
atteignent 10 : `data/exports/candidats_maitres.csv`, versionné. C'est la pièce qui rend la
sélection contrôlable — sans elle, la liste des maîtres reste un panthéon opaque.

**4 834 formes** portent au moins une mention prudente. **330 atteignent le seuil de 10** :
34 appartiennent aux 27 actuels, **296 sont hors liste**.

### Le seuil s'applique au maître, jamais à la forme

Le Titien totalise 11 références prudentes, mais aucune de ses deux graphies ne les porte
seule : « LE TITIEN » en a 10, « VECELLIO Tiziano » 9. Le fichier des candidats compte **par
forme**, avant fusion des graphies : il sert à **repérer** des pistes, pas à trancher. La
sélection se fait sur le maître désambiguïsé, une fois ses graphies rapprochées.

### La dispersion géographique trie l'instruction — elle ne sélectionne pas

Sur les 296 candidats hors liste, **139 n'existent que dans un seul musée** (10 334 notices,
dont les 5 791 de Barla à Nice), et **157 sont présents dans plusieurs** (3 474 notices).
Le second groupe est presque entièrement fait de maîtres de référence : Le Guerchin (93,
6 musées), Bouchardon (86, 4), Jules Romain (78, 4), Ludovico Carracci (76, 5), Téniers
(67, 22), François Gérard (65, 11), Giordano (42, 19), Salvator Rosa, Barocci, Maratti,
Zuccaro, Joseph Vernet, Champaigne, La Hyre, Vasari, Bourdon, Oudry, Largillière, Dürer,
Le Sueur, Delacroix, Guardi, Prud'hon, Botticelli, Murillo, Callot, Holbein, Donatello…

**Mais elle ne peut pas devenir un filtre automatique** : Le Parmesan (63), Perino del Vaga
(53), Menzel (47), Bandinelli (45), Pollaiuolo (26), Pietro Testa (20) sont des maîtres de
référence **présents dans un seul musée**. Dans les 27 actuels, Michel-Ange n'a que 3 musées
et Léonard 2. La dispersion sert à **ordonner le travail d'instruction**, pas à décider.
Ce n'est pas une comparaison entre musées sur des comptages bruts (règle du projet) : c'est
une mesure de dispersion d'un candidat, et elle sert précisément de garde-fou contre les
fonds locaux.

### Ce que le seuil ramasse et qu'il faudra écarter à la main

Des **entités qui ne sont pas des personnes** (Imprimerie de Wissembourg 392, Manufacture de
Creil 60, Faïencerie de Sarreguemines 51, Manufacture de cristaux du Creusot 46), des
**mentions collectives** (« CARRACCI l'un des » 78, « COYPEL l'un des » 60), « anonyme »
(152), et du **bruit de saisie** : un nom-pivot réduit à « A » (30 notices, 6 musées), un
autre à « A) » (15), des noms sans prénom trop ambigus pour être rattachés (« PETER » 41,
« DAVID » 26, « LESCOT » 16, « FLEURET » 10).

### Un alias manquant, trouvé en lisant la liste

« RIGAU Y ROS Hyacinthe », forme catalane du nom de Rigaud, apparaît avec 20 notices
prudentes sans être rattachée. Vérification faite, elle accompagne « RIGAUD Hyacinthe » sur
la même notice **132 fois sur 134** : l'alias n'a rattrapé que 2 références, dont aucune
prudente. Il est ajouté quand même — une table d'identité doit dire les noms qu'elle
connaît.

## 2026-07-21 (septies) — Temps 3 : les tests, et ce qu'ils protègent

Troisième et dernière étape avant le point d'arrêt. `tests/test_artistes.py`, **89 tests**,
qui portent le total du projet de 60 à **149**.

**Un refactor, pour rendre la règle testable.** La résolution d'une référence — catégorie la
plus prudente, famille la plus explicite, un poids par maître — était enfermée dans la
boucle de lecture du CSV. Elle est extraite dans `resout_reference(auteur, en_beaux_arts)`,
qui renvoie `{maître: (categorie, famille, segment)}`. Les tests l'appellent directement,
sans le CSV de 1,1 Go. Chiffres vérifiés identiques avant et après : le refactor est neutre.

**Trois niveaux de protection.**

1. *Identité* (39 cas) : chaque homonyme relevé par l'audit, face au maître qu'il imite —
   Corneille Michel-Ange contre Buonarroti, Domenico Robusti contre Jacopo, Carlo Caliari
   contre Paolo, Pierre Mignard II contre Pierre I. Y figurent aussi les cas où **l'ancre ne
   doit pas s'appliquer** (« ÉCOLE DE PRIMATICCIO », « D'APRÈS CLOUET François »), et les
   faux amis par racine commune déjà corrigés en juillet (Serodine, Vincidor, Tintoretto) :
   un test qui interdit de revenir en arrière.
2. *Comptage* (8 cas) : les deux graphies du Titien sur une notice, les deux formulations
   prudentes de Vouet, prudent contre ferme, prudent contre copie, copie contre ferme, et
   l'invariant qui rend familles et niveaux additifs — **un maître ne relève que d'une
   famille par référence**.
3. *Références réelles* (42 lignes) : `data/exports/temoins_maitres.csv`, versionné, avec la
   **valeur exacte du champ `Auteur`** telle que le musée l'a saisie, la référence Joconde,
   et le verdict attendu. Un fichier relisible sans lire de code.

**Constat de forme trouvé en écrivant les tests** : la notice `06070060045` (musée Ingres,
Montauban) écrit `IIngres Jean-Auguste-Dominique` — avec deux I. Aucun motif ne peut la
rattacher, et il ne faut pas essayer : corriger les fautes de saisie une par une reviendrait
à réécrire la base. C'est la limite ordinaire du procédé, à dire dans la page méthode.

## 2026-07-21 (sexies) — Temps 2 appliqué : la table d'identité des maîtres

Deuxième étape du chantier, toujours dans `src/build_artistes.py` seul, exports non
régénérés. Méthode : inventaire préalable des **246 formes d'auteur** réellement captées par
les motifs en vigueur, mentions prudentes **et** certaines, avec leur nombre de références —
puis relecture à l'œil, forme par forme. Pas de reconnaissance d'entités, conformément à la
décision 2.

**Un seul mécanisme ajouté : l'ancre `^`.** Un motif préfixé de `^` ne vaut qu'en **tête**
du nom. Joconde écrit l'auteur « NOM Prénom » : sans ancre, « Raphaël » se rattache à
Raphaël Collin ou Anton Raphael Mengs, et « Michel-Ange » à Corneille Michel-Ange. L'ancre
n'est posée que là où elle est nécessaire — « ÉCOLE DE PRIMATICCIO » (121 références) doit
rester pris, et le nom n'y est pas en tête.

Ce choix est **plus solide qu'une liste de noms interdits** : le CSV est republié chaque
mercredi, et un nouveau « Dupont Raphaël » serait de nouveau capté par une table qui ne le
connaît pas. L'ancre, elle, tient sur une propriété de structure de la base.

**Ce que l'ancre règle seule** : les 16 homonymes de Michel-Ange (aucune exclusion nommée
n'a été nécessaire), la cinquantaine de « Raphaël » prénoms, Lemaire-Poussin,
Lavallée-Poussin, Gaspard Poussin (Dughet), Le Guaspre, Bonifazio Veronese, Zenone Veronese,
Tiziano Aspetti, Pierino da Vinci, « Madame Ingres ».

**Ce qui a demandé une exclusion nommée** (l'homonyme porte le nom en tête) : Domenico
Robusti le fils, Carlo et Benedetto Caliari, Gabriele Caliari, Philip et Pierre Van Dyck,
Francesco et Cesare Vecellio, Pierre Mignard II le neveu, Aubin et Ferdinand Vouet,
Marguerite Vinci, Poussin-Heydeck, Ribera y Cirera, Pierre Ribera, Arnold Frans Rubens et le
« Rubens des batailles », Ingres Jean Marie Joseph, Raphael Tuck, Raphael-Schwartz, Giovanni
Santi le père.

**Deux corrections non prévues par l'audit.**

1. L'exclusion `["ATELIER"]` posée sur Raphaël le 2026-07-08, **jamais documentée**, servait
   à écarter les noms d'atelier (« ATELIER DE RAPHAËL »). L'ancre le fait mieux : ces formes
   ne commencent pas par le nom du maître. Exclusion retirée.
2. **« SANTI Raffaello », la forme d'état civil de Raphaël, n'était captée par aucun
   motif** : ni `RAPHAEL`, ni `SANZIO` ne s'y trouvent. C'est un faux négatif au sein même
   des 27 — **+3 références** prudentes. Il explique l'écart entre le total prévu par
   l'audit (2 185) et le total obtenu (**2 188**).

**Résultat mesuré** : doute des 27 **2 341 → 2 188** ; attributions certaines
**29 995 → 28 240**. Invariants revérifiés sur les 27.

**L'effet attendu se confirme : c'est la part affichée qui bouge le plus.**

| Maître | part avant | part après |
|---|---:|---:|
| Michel-Ange | 19 % | **39 %** |
| Le Tintoret | 27 % | **48 %** |
| Véronèse | 15 % | **27 %** |
| Le Primatice | 31 % | **38 %** |
| Léonard de Vinci | 30 % | **36 %** |

Michel-Ange tombe de 9 musées à **3** (Louvre 146, Rennes 1, Dole 1) : les six autres ne
détenaient que des œuvres d'homonymes. Ces cinq phrases d'en-tête devront être **relues, pas
seulement recalculées** — c'est le temps 7.

## 2026-07-21 (quinquies) — Temps 1 appliqué : le comptage passe à la référence

Première étape du chantier de fiabilisation, exécutée dans `src/build_artistes.py` seul.
Les exports ne sont **pas** régénérés (ils le seront au temps 6, après le point d'arrêt).

**Contrôle préalable.** La référence Joconde est-elle bien une clé ? Scan complet du CSV :
1 023 705 lignes, **1 023 705 références distinctes, aucun doublon**. La déduplication tient
donc entièrement dans la ligne courante — aucun index en mémoire, aucun second passage.

**Mise en œuvre.** La boucle comptait à chaque segment du champ `Auteur` ; elle procède
maintenant en deux temps : on collecte ce que la référence dit de chaque maître, puis on
compte **une fois** par couple (maître, référence).

**Deux règles de résolution en découlent.**

*Catégorie* — quand une même référence porte plusieurs liens avec le même maître
(« POUSSIN Nicolas (attribué à) ; POUSSIN Nicolas »), le plus prudent l'emporte :
**doute > copie > attribution ferme**. C'est ce qui rend les trois catégories disjointes,
donc additionnables, comme l'exigeait la décision 1.

*Famille* — **arbitrage tranché : option (c)**, le « ? » l'emporte sur la formule de
distance. Motif retenu par l'utilisateur : c'est le marqueur de doute le plus explicite.
Conséquence structurelle, plus importante que les 3 cas concernés : **une référence = une
famille**, donc familles et niveaux totalisent exactement le doute. Les jauges empilées et
l'axe du graphique restent additifs, sans retouche du front. L'option (a) — la référence
dans les deux familles — aurait cassé cette égalité pour trois références.

**Résultat mesuré, conforme à l'audit** : doute des 27 **2 341 → 2 225** (−116) ;
Le Primatice 269 → 197, Le Tintoret 47 → 39, Le Corrège 46 → 25, Titien 20 → 12,
Véronèse 41 → 38, Simon Vouet 51 → 48, Fragonard 31 → 30. Le dénominateur bouge aussi,
sans que l'identité soit encore corrigée : propre 29 995 → 29 229, copie 4 883 → 4 503
(Titien 211 → 104, Véronèse 238 → 117, Le Corrège 152 → 82 — tous des maîtres à double
graphie). Invariants revérifiés sur les 27 : familles = niveaux = somme des musées = doute,
et aucune œuvre citée deux fois dans la vitrine.

**Effet de bord assumé** : le garde-fou `refs_exemples`, qui empêchait une même œuvre
d'illustrer deux familles, devient inutile — la structure l'interdit désormais. Retiré.

**Reste au temps 2** : l'identité (table déclarative d'alias et d'exclusions). Les −40
références mal rattachées ne sont **pas** dans les chiffres ci-dessus.

## 2026-07-21 (quater) — Fiabilisation des maîtres : unité de comptage, identité, seuil à 10

Décisions prises à l'issue de l'audit du 2026-07-21 (constats mesurés : donnees.md, même
date). **Aucune n'est encore appliquée** : le pipeline, les exports et le front sont
inchangés à ce stade, sur consigne. Ce qui suit fixe le cap et l'ordre d'exécution.

### Décision 1 — L'unité de comptage est la référence Joconde, pas le segment d'auteur

Le comptage **par segment** du champ `Auteur`, retenu le 2026-07-07 et documenté comme tel,
est **abandonné**. Il produit un chiffre que le public lit comme un nombre d'œuvres alors
qu'il compte des mentions : une notice nommant le maître sous deux graphies pesait double.

**Nouvelle unité : la référence Joconde unique.** Invariants à faire respecter par le
pipeline et par les tests :

- le `doute` d'un maître est un **nombre de références distinctes** ;
- aucune référence n'augmente deux fois le total d'un même maître ;
- une référence peut porter **plusieurs familles** sans peser davantage dans le total ;
- les totaux de familles ne sont **pas additionnés** en un tout (recouvrements) ;
- une somme de profils n'est publiée que si les ensembles sont réellement disjoints ;
- le front n'appelle jamais « notices » un comptage de segments.

Coût connu : **2 341 → 2 225** références sur les 27 (−116).

### Décision 2 — L'identité des maîtres passe par une table déclarative

Refus explicite du surcode : **pas** de reconnaissance d'entités, **pas** de moteur
générique. Une **table lisible**, relue à l'œil, contenant pour chaque maître : ses alias
suffisamment précis, et les **exclusions explicites** des homonymes attestés. Le rattachement
reste un test au mot entier sur le nom-pivot.

Coût connu : **−40 références** prudentes mal rattachées ; l'effet sur le dénominateur est
plus lourd encore (Michel-Ange : 422 des 749 attributions certaines appartiennent à Corneille
Michel-Ange ; Raphaël : 52 formes captées, « Raphaël » pris comme prénom).

**La table doit couvrir les deux catégories** — prudent *et* certain : l'audit montre que la
seconde est la plus polluée, et c'est elle qui fabrique le dénominateur affiché au public.

### Décision 3 — Le seuil descend de 20 à 10 références prudentes uniques

Seuil défini sur l'**unité corrigée** : références distinctes, personne précisément
identifiée, copies « d'après » exclues, une référence comptée une seule fois même si le champ
`Auteur` répète plusieurs alias.

Objectif éditorial : ne retirer automatiquement aucun artiste proche de l'ancien seuil,
élargir la matière, et disposer de plus de profils pour éprouver les vérifications.
Conséquences déjà mesurées : **Michel-Ange reste** (148), **Titien reste** (11, contre 20
affichés aujourd'hui — il serait sorti sous l'ancien seuil appliqué à l'unité corrigée).

### Décision 4 — Le seuil ne sélectionne pas seul : la règle publique reste double

Vérification faite dans la documentation : le critère en vigueur depuis le 2026-07-07 est
**« maître de référence ET seuil quantitatif »** — la curation de notoriété était déjà
assumée et publiable, le seuil servant à la rendre non arbitraire.

**Cette combinaison est maintenue** ; seul le nombre change (20 → 10). L'audit montre
qu'elle est indispensable : au seuil de 10, **298 formes d'auteur hors des 27** qualifient,
dont des manufactures, des imprimeries, « anonyme », des mentions collectives
(« CARRACCI l'un des ») et surtout des **fonds locaux massifs** — BARLA Jean-Baptiste, avec
5 791 références prudentes, écraserait à lui seul tout classement quantitatif. Un seuil nu
produirait une liste ingérable et éditorialement absurde.

**Règle publique proposée**, reproductible et énonçable en une phrase :

> Sont retenus les artistes **présents dans les répertoires d'autorité** (INHA/Agorha,
> Joconde, encyclopédies de référence), **identifiés comme une personne unique** après
> désambiguïsation, et dont **au moins 10 notices** portent une formulation prudente,
> copies « d'après » exclues.

Deux compléments nécessaires pour qu'elle soit vérifiable :
1. la liste des candidats examinés est **publiée avec leur nombre de notices**, y compris
   ceux écartés et le motif (entité non personnelle, fonds local, homonymie non résolue) —
   la sélection devient contrôlable au lieu d'être un panthéon opaque ;
2. les **faux négatifs** relevés par l'audit sont instruits au même titre que les candidats
   nouveaux : Le Guerchin (93), Bouchardon (86), Jules Romain (78), Ludovico Carracci (76),
   Téniers (67), François Gérard (65), Le Parmesan (63), Perino del Vaga (53)… dépassent
   largement l'ancien seuil et n'ont jamais été examinés, la liste ayant été composée à la
   main. **Ne pas reprendre les anciens comptes par nom** : chaque candidat repasse par la
   désambiguïsation.

### Arbitrage laissé ouvert — familles multiples sur une même référence

Trois références de Simon Vouet (`M0332004170`, `M0332004171`, `M0332004172`) portent à la
fois `VOUET Simon (?)` et `VOUET Simon (atelier, dessinateur)`. Elles comptent pour **trois**
références dans le total — cela, c'est acquis. **Ce qui reste à trancher** : comment les
représenter par famille. Trois options, aucune retenue par défaut :

- **a.** la référence apparaît dans les deux familles (les familles ne s'additionnent déjà
  pas, l'invariant tient) ;
- **b.** priorité à la formule de distance (« atelier ») sur le « ? », jugé moins informatif ;
- **c.** priorité au « ? », marqueur de doute le plus explicite.

Impact mesuré : **3 références sur 2 185**, toutes chez un seul maître. Le choix est donc
sans effet sur les totaux, mais il fixe une doctrine qui vaudra pour tous les cas à venir —
d'où l'arbitrage explicite plutôt qu'un choix silencieux. Ce fil rejoint la question déjà
ouverte « politique “?” vs formule de distance ».

### Plan d'exécution retenu (ordre imposé)

1. **Unité de comptage** — comptage par couple `maître + Reference` dans
   `build_artistes.py` ; invariants ci-dessus.
2. **Identité** — table déclarative des alias et exclusions, couvrant prudent *et* certain.
3. **Tests de non-régression** — fondés sur des **références réelles** : les témoins
   d'homonymie (Corneille, Cerquozzi, Merisi, Pace, Vouet Aubin, Robusti Domenico, Vecellio
   Francesco, Ingres Jean Marie Joseph, les quatre « Poussin », les quatre « Raphaël »), les
   doublons de graphie (Primatice, Corrège, Titien, Tintoret) et les trois références
   multi-familles de Vouet.
4. **Recalcul au seuil de 10** sur l'unité corrigée, tous candidats confondus.
5. **Nouvelle sélection** selon la règle double, avec journal des candidats écartés.
6. **Régénération des exports** (`artistes.json`, puis `vue_ensemble.json` qui en dérive).
7. **Contrôle des effets sur le front** : classement du répertoire, jauges, familles,
   niveaux, exemples d'œuvres, cartes, en-têtes rédigés des fiches (les nombres suivent
   automatiquement, **les angles doivent être relus**), page Méthode.
8. **Révision des textes publics** : tout ce qui annonce « 27 » ou « au moins vingt notices ».

**Étapes 1 à 3 avant toute reprise éditoriale ou graphique.**

## 2026-07-21 (ter) — En-tête du graphique : deux textes, deux fonctions (4 artistes témoins)

**Problème.** Le titre et le sous-titre du graphique formaient une **question suivie de sa
réponse, avec les mêmes mots** : « Comment les musées rattachent ces œuvres à X » puis « Les
musées les rattachent surtout à… ». Deux textes pour une seule fonction ; la répétition
signalait immédiatement la génération automatique.

**Règle rédactionnelle (consigne utilisateur du 2026-07-21).** Les deux textes reçoivent des
rôles distincts :
- **Titre** — l'angle propre à l'artiste ; contient son nom ; 4 à 9 mots ; jamais une
  question ; sans « profil », « corpus », « distribution », ni « attribution » employé
  abstraitement.
- **Sous-titre** — la preuve chiffrée ou la nuance qui justifie l'angle, en une phrase, sans
  reprendre les mots ni la structure du titre. « Les musées rattachent » ne doit pas revenir
  dans tous les sous-titres.

Quatre familles de titres selon la forme des données : mention très majoritaire
(« … en tête », « surtout … ») ; territoire majoritaire mais plusieurs mentions
(« principalement autour du maître ») ; deux tendances proches (« entre … et … ») ;
répartition sans tendance (« plusieurs formes de proximité »).

**Appliqué à quatre artistes témoins** (validés avant code) : Ingres, Charles Le Brun,
Rembrandt, François Clouet — puis **généralisé aux 27 le même jour**, après validation. Plus
aucune fiche n'utilise l'en-tête généré ; `lectureProfil()` et le titre générique restent
dans le code comme repli, sans artiste pour les déclencher.

**Répartition des 27 dans les quatre familles de titres** : mention très majoritaire (11) ;
territoire majoritaire (5) ; deux tendances proches (6) ; sans tendance forte (5). Trois
titres sortent du gabarit parce que les données l'imposaient : « Rodin, une seule mention »
(100 % sur une seule formule), « Van Dyck, éparpillé entre les musées » et « Ribera, un petit
ensemble très dispersé » (leur fait marquant est la dispersion, pas la mention).

**Trois corrections faites en relisant la sortie complète**, invisibles à la rédaction :
- Van Dyck lisait « se répartissent dans 21 musées ; “de son école” en réunit 21 » — deux
  nombres identiques pour deux choses différentes dans la même phrase. Le sous-titre ne cite
  plus de mention chiffrée ;
- Léonard de Vinci répétait « deux musées » dans le titre et dans le sous-titre → titre
  recentré sur « l'école plutôt que la main » ;
- Simon Vouet ouvrait sur « La plus fréquente », sans dire de quoi → « La mention la plus
  fréquente ».

**Contrôle automatisé** avant livraison : les 27 couples sont produits en exécutant réellement
les fonctions sur `artistes.json`, avec vérification de la longueur des titres (4 à 9 mots),
de l'absence des mots proscrits (profil, corpus, distribution, domine, nettement, doute) et
de l'absence de titre interrogatif. Zéro alerte.

**Écrits à la main, chiffres lus dans les données.** Le champ `graphique` de
`editorial-maitres.js` porte `titre` (chaîne) et `sousTitre` (**fonction**). La règle du
fichier — « aucun chiffre stocké ici » — est préservée : les nombres arrivent depuis
`artistes.json` via `{ n, total, second, musees, notices(code) }`. Un texte figé aurait
menti dès la première régénération d'export, ce qui va justement arriver (voir le bug de
double comptage, 2026-07-21 quater).

**Deux points assumés :**
- Le sous-titre chiffre en **notation brute** (« 240 des 310 »), là où la règle générale du
  projet préfère les mots (« plus des deux tiers »). Amendement délibéré : le titre porte
  désormais les mots, le sous-titre est l'endroit de la preuve. La règle vaut toujours
  ailleurs.
- Chez Clouet, le nombre de musées s'écrit **« 8 »** et non « huit » comme dans le texte
  validé : le projet n'a pas de conversion nombre→lettres, et écrire « huit » à la main
  reviendrait à figer une donnée. La phrase contient déjà « 95 des 105 », le chiffre reste
  cohérent.

**Dénominateur.** « les 204 œuvres concernées » = les notices à formulation prudente, pas les
4 670 rattachées au nom. Le bandeau situé juste au-dessus porte la fraction complète
(« 204 sur 4 670 ») : deux nombres voisins à l'écran, à surveiller en relecture.

## 2026-07-21 (bis) — Une notice ne peut illustrer la vitrine qu'une fois (bug Titien)

**Symptôme.** Sur la fiche **Titien**, l'onglet « Œuvres » restait inaccessible. Même
défaut, non repéré jusque-là, sur **Le Tintoret**.

**Cause — dans les données, pas dans le front.** Une même notice peut nommer le maître
**deux fois, sous deux graphies**, dans le champ auteur. Sur l'œuvre `50350228332` du
Louvre, la base porte à la fois « VECELLIO Tiziano (attribué à) » et « LE TITIEN (dit,
attribué à) ». `build_artistes.py` traite chaque segment d'auteur séparément : il retenait
donc **deux exemples pour la même œuvre**, dans la même famille. Le composant
`OeuvresMaitre.svelte` liste ses entrées avec la **référence comme clé** — deux clés
identiques font échouer le rendu de la liste, et la vitrine entière disparaît.

C'est une variante connue du piège « graphies multiples » (CLAUDE.md) : ici les deux
graphies ne sont pas sur deux notices, mais **sur la même**.

**Correction, à la source.** `build_artistes.py` tient désormais, par maître, l'ensemble des
références déjà retenues en exemple (`refs_exemples`), toutes familles confondues : **une
notice ne peut illustrer la vitrine qu'une fois**. Le quota par famille est inchangé, donc
la place libérée est reprise par l'œuvre suivante — Titien et Le Tintoret gagnent un
**vrai** second exemple pour leur famille dominante au lieu d'un doublon. Aucun comptage
n'est touché : le diff de `artistes.json` se limite à ces deux exemples.

**Garde-fou au front** (`OeuvresMaitre.svelte`) : la liste est dédoublonnée par référence
avant affichage. Le pipeline reste la correction réelle ; ce filet évite qu'une future
régression de l'export fasse à nouveau disparaître une page entière au lieu d'un doublon
visible. La règle éditoriale « exemples pris automatiquement, les premiers rencontrés »
n'est pas modifiée — elle est seulement rendue univoque.

## 2026-07-21 — Purge des derniers mots de laboratoire + ligne de partage « œuvres / notices »

**Quatre reliquats** signalés par les deux passes précédentes et laissés en l'état sont
corrigés ici. Aucune donnée, aucun calcul, aucun graphique touché.

- `les-presque/+page.svelte` — « {N} artistes disposent ici d'un **corpus suffisamment
  documenté** » → « **réunissent ici assez d'œuvres** pour être explorés et comparés ». Le
  critère de sélection reste expliqué en page Méthode (ancre `#les-27`) ; l'intro n'a pas à
  le nommer en langue d'analyste.
- `BandeauMaitre.svelte` — repère méthodologique : « … rattachées à son nom **dans le corpus
  étudié** » → « … rattachées à son nom, **copies mises à part** ». C'est exactement ce que
  disait le commentaire de code (le total exclut les « d'après ») : autant l'écrire pour le
  lecteur au lieu de le cacher derrière un mot de métier.
- `Repertoire.svelte` — en-tête de colonne « **Notices** concernées » → « **Œuvres**
  concernées ».
- `echelle/+page.svelte` — « Dans l'ensemble des **notices** concernées, une formule
  **domine largement** » → « Sur l'ensemble des **œuvres** concernées, une formule **revient
  bien plus souvent que les autres** ». « Domine » figurait déjà au vocabulaire proscrit pour
  la fiche artiste (2026-07-20) ; la règle vaut partout.

**Ligne de partage précisée** (amende le 2026-07-20, qui opposait texte narratif et comptage
sec). Le critère n'est plus la nature du texte mais **la distance à la base** :
- **« œuvres »** dans tout ce que le visiteur lit comme un propos sur les collections —
  phrases, intros, **et les en-têtes des listes qui accompagnent ces phrases** (le répertoire
  et le bandeau du maître sont côte à côte à l'écran et désignent le même nombre : ils
  doivent employer le même mot) ;
- **« notices »** là où l'on parle explicitement de la base — légendes de graphique
  (`BarresMentions`), tooltips, seuils et page Méthode.

Non traité, hors périmètre V1 : `/revisions` (rubrique en réserve, hors nav publique) dit
encore « corpus » ; les occurrences restantes sont des **commentaires de code**, pas du
texte affiché.

## 2026-07-20 (bis) — Fiche artiste : trois textes remis en langue ordinaire

**Problème.** Trois textes de la fiche parlaient encore la langue du projet, pas celle du
lecteur. La ligne sous le nom versait dans la culture savante (« rococo », « Grand Siècle »,
« portraitiste de la cour des Valois ») : des repères qui demandent eux-mêmes une explication.
Le titre du graphique annonçait « Le profil d'attribution de X » — « profil » et
« attribution » sont du vocabulaire d'analyste. Et rien ne disait, en clair, ce que le
graphe donnait à voir.

**1. Ligne biographique — gabarit strict, une phrase, sans exception :**
« [Activité principale] [nationalité] du [siècle], [dates]. » Elle sert à **situer**, rien
d'autre. Sont proscrits, même exacts : mouvements (rococo, baroque), périodes de connaisseur
(Grand Siècle, Siècle d'or, Renaissance), écoles (école de Fontainebleau), fonctions de cour
(premier peintre du roi). Le siècle est celui où l'artiste a **travaillé**, pas celui de sa
naissance ; quand l'activité couvre réellement deux siècles → « des XVe et XVIe siècles ».
Dates relevées hors ligne, vérifiées sur les notices d'autorité (INHA/Agorha, National
Gallery, Larousse, Britannica) ; « vers » quand la naissance est discutée, comme le font ces
notices — la prudence sur les dates est du même ordre que celle des musées sur les
attributions. Appliqué aux **27** artistes (`web/src/lib/editorial-maitres.js`).

**2. Titre du graphique.** « Le profil d'attribution de X » → **« Comment les musées
rattachent ces œuvres à X »**. Le titre nomme l'acteur (les musées), l'action (rattacher) et
l'objet. Vocabulaire écarté : profil, corpus, analyse, distribution. La contraction de
l'article est traitée par `aNom()` (`joconde.js`) : « au Primatice », jamais « à Le Primatice ».

**3. Phrase de lecture** (`territoires.js`, `lectureProfil`). Sous le titre, une phrase dit
la tendance en mots ordinaires. **Cinq formulations fixées, on n'en invente aucune autre** ;
« corpus » est proscrit. Seuils **inchangés** par cette passe : territoire ≥ 60 % → territoire
principal ; sinon écart < 5 points entre les deux premiers → « les œuvres se partagent » ;
sinon → « sans qu'une seule ne s'impose ». La mention citée est la plus fréquente **à
l'intérieur** du territoire principal (pas la dominante globale, qui peut appartenir à un
autre territoire), et réutilise la citation publique de `familles-public.js` — aucun libellé
n'est réécrit.

**Contrôle.** Les 27 phrases générées ont été vérifiées : 8 « au maître lui-même », 11 « à son
entourage/influence », 8 « sans qu'une seule ne s'impose ». **Aucun artiste ne déclenche
aujourd'hui la branche « les œuvres se partagent »** : avec les données actuelles, l'écart
entre les deux premiers territoires n'est jamais inférieur à 5 points sous la barre des 60 %.
La branche est conservée (les seuils ne sont pas touchés par cette passe), mais c'est un
point à réexaminer si l'on revoit un jour les seuils. Captures de contrôle : Boucher,
Charles Le Brun, François Clouet, Rembrandt.

## 2026-07-20 — Fiche artiste : portrait éditorial (fin des compteurs) + vocabulaire public « œuvres »

**Problème.** La fiche refondue la veille (2026-07-19 bis) restait une **fiche statistique** :
un très grand `310`, un `9 %` en seconde vedette, puis deux phrases techniques. Quatre blocs
indépendants que le lecteur devait relier lui-même ; le nombre `310` seul en très grand n'a
aucun sens immédiat ; l'enseignement réellement intéressant (la mention la plus fréquente)
arrivait en dernier, en petit.

**Parti retenu** (validé sur prototype Charles Le Brun avant généralisation) : la scène
devient un **court portrait éditorial fondé sur les données**, lisible en deux ou trois
phrases naturelles. Plus aucun grand nombre isolé, aucun compteur, aucune carte de KPI.

**Hiérarchie, dans cet ordre** :
1. **Nom de l'artiste** — élément typographique le plus grand (inchangé, `--taille-xxl`) ;
2. **La mention la plus fréquente** — le constat, en Fraunces 1,35 rem : c'est le deuxième
   niveau visuel, et c'est ce que le graphique situé dessous vient ensuite détailler
   (le graphe n'a plus à faire découvrir seul l'enseignement principal) ;
3. **Récit chiffré** en corps de lecture — volume concerné, part de la mention, musées ;
4. **Repère méthodologique** en registre secondaire (petit corps, contraste atténué,
   séparé par un filet fin) : « En contexte : 310 sur 3 344 œuvres…, soit 9 %. »

**Les nombres vivent DANS les phrases** : graisse 600 + accent cobalt existant + chiffres
elzéviriens (`font-variant-numeric: oldstyle-nums`, fournis par Spectral), jamais plus
grands que le texte courant. Aucun ne concurrence le nom. Polices et variables de la charte
uniquement — aucun import, aucun style global touché.

**Vocabulaire public (change la doctrine de la veille).** Dans le **texte narratif**, on
écrit **« œuvres »** — « les 310 œuvres associées à son nom » — et non « notices », qui
donne le point de vue de la base de données. Règles strictes :
- **jamais « œuvres de X »** : ces œuvres ne lui sont précisément **pas** directement
  attribuées → « œuvres **associées à son nom** » / « rapprochées de X » ;
- l'**unité technique reste la notice Joconde**, expliquée en page Méthode ;
- pas de « Dans Joconde » en ouverture de fiche ;
- **vocabulaire interdit pour le constat** : « domine », « domine nettement », « le doute
  passe par ». On écrit **« X est la mention la plus fréquente »** — neutre, exact même
  quand la mention ne pèse que 38 % (Ribera), et cohérent avec « on lit ce que les musées
  écrivent ».

Cette règle **ne revient pas** sur la passe 2026-07-19 (ter) pour les **comptages secs**
(tooltips, légendes, panneaux de `/echelle`, seuil de la Méthode) : ceux-ci restent en
« notices ». La ligne de partage est désormais **narratif → « œuvres » / comptage → « notices »**.
⚠️ Reliquat connu, non traité (hors périmètre) : le répertoire affiche « NOTICES CONCERNÉES »
à côté d'un bandeau qui dit « 310 œuvres » — à trancher dans une passe dédiée.

**Génération (les 27 artistes, aucune valeur en dur).** Le constat est construit depuis
`artistes.json` + la couche de libellés publics :
- **nouveau champ `citation`** dans `familles-public.js` — forme **citable en sujet de
  phrase** (« De son atelier »), distincte de `label` (étiquette d'axe : « son atelier »)
  et de `header` (titre de tooltip). `label`, `header`, `corps`, `mention` et `couleur`
  sont **inchangés** : ni le graphique ni les tooltips ne bougent ;
- **égalité exacte** : toutes les mentions au maximum sont citées, ordonnées par
  `ORDRE_FAMILLES` (aucune choisie arbitrairement), première en capitale, suivantes en bas
  de casse → Hyacinthe Rigaud : « "Attribué à" et "de son école" sont les mentions les plus
  fréquentes. » + « 16 portent **chacune de ces mentions** » ;
- **mention unique couvrant tout le corpus** (Rodin, 100 %) : « Les 80 œuvres … portent
  **toutes** cette mention » — évite le doublon « parmi les 80 …, 80 portent » ;
- **un seul musée** : « Ces œuvres sont toutes conservées dans un même musée » (aucun cas
  réel aujourd'hui, minimum observé = 2 ; garde-fou d'accord).

**Bio conservée** quand elle existe (`editorial-maitres.js` : François Clouet, Rembrandt),
en ligne d'identité italique sous le nom — elle situe l'artiste sans concurrencer le constat.

**Vérifié** : les 27 phrases relues une à une avant rendu ; captures desktop (Le Brun,
Rigaud) + mobile (Le Brun, Rembrandt) + planche des cas limites (Rodin 100 %, Rembrandt
bio + « À sa manière », Léonard de Vinci 2 musées, Annibale Carracci « De son cercle »).
Le bandeau reste compact : onglets et début du graphique visibles dans le premier écran en
1280×760. Données et pipeline **inchangés**.

## 2026-07-19 (ter) — Wording des comptages : « notices » partout, « œuvre » réservé à l'objet montré

**Problème.** Après la refonte de la fiche (2026-07-19 bis, qui dit « 310 notices »), le
reste de l'interface disait encore « œuvres » pour les mêmes comptages : tooltips du
graphique (« 240 œuvres » face à « 240 notices » dans la phrase de dominante), bande des
copies de la vitrine (« 237 œuvres "d'après" »), carte des musées (« N œuvres
concernées », « où au moins une œuvre concernée est conservée »), panneaux de
`/echelle` (« 24 507 œuvres concernées ») et page Méthode (seuil « vingt œuvres »).
Or le pipeline compte des **notices Joconde**, pas un ensemble certifié d'œuvres
distinctes (règle du chiffre 24 507).

**Doctrine adoptée** (vaut pour toute copie publique à venir) :
- **Tout comptage se dit en « notices »** — valeur, tooltip, légende, seuil, total.
- **« œuvre » reste permis pour un objet montré individuellement** (une entrée de la
  vitrine, l'aperçu d'un point de carte, « il ne réattribue aucune œuvre ») : là, le mot
  désigne bien un objet réel, pas un décompte.

**Application** (copie seule, aucune donnée ni calcul modifiés) :
- `familles-public.js` : helper `oeuvres()` **renommé `notices()`** (« 1 notice » /
  « n notices ») ; les tooltips du graphique et leurs aria-labels disent désormais la
  même chose que la phrase de dominante de la fiche.
- Vitrine (`OeuvresMaitre`) : « À part : 237 notices **portent la mention** "d'après
  Charles Le Brun" — des copies assumées… » (accord porte/portent géré). Le titre
  « Quelques œuvres derrière les points » est conservé (objets montrés un à un).
- Carte (`CarteMaitre`) : titre **« D'où viennent ces notices »** (les musées ont écrit
  les notices — cohérent avec « on lit ce que les musées écrivent ») ; légende « Un
  point = un musée **ayant publié** au moins une notice concernée » ; tooltips « N
  notice(s) concernée(s) » ; replis et hors-cadre reformulés (« relève(nt) d'un seul
  musée », « rattachées à N musées ») ; aria-label du SVG aligné.
- `/echelle` : « notices concernées » (panneaux + texte), « une même notice peut porter
  plusieurs mentions », copies « d'après » en notices. Au passage, **purge du reliquat
  « Les presque »** (appellation abandonnée en public le 2026-07-19) → « la rubrique
  "Explorer les maîtres" » (libellé de la nav).
- Méthode : seuil « au moins **vingt notices** portant une formulation prudente » (aligné
  sur l'intro de la rubrique) ; copies en « notices ».

## 2026-07-19 (bis) — Fiche artiste : hiérarchie des informations (le doute est le sujet)

**Problème.** La scène mettait en avant **3 344 œuvres** et **64 musées** (volume total sous
le nom) alors que le sujet de la rubrique est le **doute** (les 310 notices affichées dans
le répertoire). Le lecteur devait reconstituer la relation entre ces valeurs.

**Nouvelle hiérarchie de la fiche** (composant `BandeauMaitre.svelte`, phrases toutes
**générées depuis `artistes.json`**, aucun texte manuel par artiste) :
1. **Information principale** = `doute`, en grand (nettement plus visible) : « 310 » +
   « notices où son nom est accompagné d'une formulation prudente ». On dit **notices** (le
   pipeline compte des notices Joconde, pas un ensemble certifié d'œuvres distinctes).
2. **Dénominateur** en registre secondaire : « 9 % des 3 344 notices associées à son nom
   dans le périmètre étudié ». Total de référence = **`propre + doute`** ; part =
   `Math.round(doute / (propre + doute) * 100)`. Le total n'est PAS l'ensemble absolu des
   notices du nom (copies « d'après » et catégories exclues comptées à part) → **« dans le
   périmètre étudié »**. Explication ajoutée à la page Méthode (« Lire les chiffres »).
   3 344 n'est plus présenté comme le sujet.
3. **Répartition entre musées** : `nb_musees_doute` (19), pas le `musees` général (64,
   retiré du bandeau car il ne répond pas à la question). « Ces 310 notices se répartissent
   entre 19 musées. » Le profil et la vue Musées parlent **du même corpus** (`musees_doute`).
4. **Formulation dominante** : « La formulation la plus fréquente est "de son école" :
   240 notices, soit 77 %. » Construite depuis les données (famille dominante réelle,
   notices, part dans `doute`, libellé public canonique, accords). **Égalités** gérées : à
   part égale, on liste toutes les familles au maximum, **ordonnées par `ORDRE_FAMILLES`**
   (jamais l'ordre des données), énumération française + « chacune » (ex. Hyacinthe Rigaud :
   « "attribué à" et "de son école" : 16 notices chacune, soit 39 % »).

**Règles.** Tous les pourcentages de la fiche via `Math.round` (pas de décimale mêlée).
**`fractionEnMots` n'est plus utilisée** (l'ancienne synthèse « près des deux tiers » était
imprécise/fausse pour Le Brun : 240/310 = 77 %). Espace des milliers rendue visible
localement (U+00A0). Aucune donnée ni calcul du pipeline modifié.

**Répertoire** : le tri « Œuvres » devient **« Notices »** ; micro-légende « ARTISTE ·
NOTICES CONCERNÉES ». Le nombre à droite (= `doute`) est **le même** que la valeur
principale du profil.

**Vérifié** : Le Brun, Ingres, Rembrandt, Titien (petit volume), Rigaud (égalité) ; les
trois onglets ; desktop + mobile ; cohérence sur les 27 (somme des familles = `doute`,
`nb_musees_doute` = points de carte, aucun doute sans musée ; parts de 1 à 59 %).
**Hors périmètre (phase séparée)** : les notices de l'onglet Œuvres (wording « œuvres »).

## 2026-07-19 — « Explorer les 27 maîtres » : titre public, intro refondue, intro ↔ outil séparés

Phase limitée à **l'introduction** de la rubrique et à sa **séparation visuelle** d'avec
l'outil d'exploration. Répertoire, profils, onglets, notices d'œuvres et visualisations
**non touchés** (phase distincte à venir).

1. **Abandon de l'appellation publique « Les presque ».** Le titre public devient le
   **H1 « Explorer les {N} maîtres »** (N = `artistes.length`). « Les presque » ne figure
   plus dans les textes publics de la page. **Reste inchangé** (pas une migration
   technique) : la route `/les-presque`, les fichiers internes, les exports, les documents
   historiques. « Les presque » peut subsister comme **nom de code interne** (docs, code).

2. **Nouveau texte d'introduction** (provisoire, fourni par l'utilisateur) : trois
   paragraphes qui expliquent ce qu'est la rubrique (le nom d'un artiste ≠ l'auteur ;
   27 artistes retenus au seuil d'« au moins vingt notices » ; 2 341 notices prudentes au
   total ; le seuil n'est pas un palmarès mais un plancher de comparabilité ; invitation à
   choisir un nom). L'ancien texte (énumération de formules) est retiré. La phrase de
   prudence commune (« Le projet reprend les formulations publiées par les musées ; il ne
   réattribue aucune œuvre. ») est conservée en **note secondaire discrète**. **Interdits
   respectés** : pas de liste des huit mentions, pas de définition des familles, pas de
   nouveau chiffre, pas d'interprétation d'authenticité, pas de « distance à la main » (ce
   vocabulaire vit dans « Comprendre les mentions » et « Méthode »).

3. **Deux temps séparés.** *Premier temps* = entrée éditoriale : deux colonnes sur
   ordinateur (titre à gauche, texte à droite), largeur de lecture confortable, **aucun
   encadré**, prudence en note, espace vertical généreux dessous. *Second temps* =
   exploration, introduite par l'intitulé simple **« Choisir un artiste »** (registre UI,
   repère cobalt), détachée par un **filet + de l'espace** (pas un nouveau bandeau) ; en
   dessous, le répertoire + le profil **existants, inchangés**.

4. **Responsive.** Ordinateur : l'intro respire mais le début du répertoire reste
   perceptible dans le premier écran (vérifié 1280×760). Mobile : titre / texte / note
   s'empilent, « Choisir un artiste » marque le passage à l'outil, répertoire toujours
   repliable, aucun texte rapetissé à l'excès.

5. **Chiffres = données déjà chargées, pas de seconde source.** `nbMaitres` =
   `artistes.length` (27) ; `totalNotices` = somme des `doute` des 27 (2 341) ; le seuil
   « vingt » est écrit en toutes lettres (critère du fichier `artistes.json`). Détail :
   l'espace fine insécable de `toLocaleString` (U+202F) ne se voit pas dans Spectral →
   remplacée **localement** par une espace insécable normale (U+00A0), sans toucher
   `joconde.js` ni la scène. Vocabulaire : **« artistes »** dans le texte explicatif,
   **« maîtres »** conservé dans le titre et la nav déjà validée.

## 2026-07-18 (sexies) — Accueil : ce que dit (et ne dit pas) le chiffre 24 507

**Correction d'une formulation fausse** que j'avais mise sur la couverture (entrée
quinquies) : « 24 507 œuvres pour lesquelles un musée de France a écrit un doute sur
l'auteur. » **À proscrire.** Le nombre 24 507 ne désigne **pas** un décompte certifié
d'œuvres distinctes : ce sont les **notices retenues par le pipeline dans le corpus des
formulations prudentes**. Présenter ce total comme « 24 507 œuvres » invente une
interprétation que les données ne garantissent pas, et frôle l'idée d'authentification —
ce que le projet ne fait jamais.

**Accroche adoptée** (le nombre reste chiffre vedette de la composition, mais **dans**
sa phrase, jamais détaché) :

> Un million de notices.
> Dans **24 507** d'entre elles, l'attribution est formulée avec prudence.
> Une enquête dans les données des musées.

**Règles de formulation du chiffre (à respecter partout) :**
- La phrase « Dans 24 507 d'entre elles… » se lit comme **un tout** ; ne jamais séparer
  le nombre de son unité (les notices), ni le présenter comme « 24 507 œuvres ».
- **Bannis** : « un musée a écrit un doute », « œuvres douteuses », « œuvres inconnues »,
  « auteurs inconnus », et toute tournure suggérant que le projet authentifie ou
  réattribue une œuvre.
- Implémentation : le nombre est en vedette **inline** dans l'étage `.e2` (`<span
  class="chiffre">`, insécable), plus de bloc « preuve » isolé + glose.

## 2026-07-18 (quinquies) — Accueil : retour du chiffre 24 507 + retrait du lien « Accueil »

> ⚠️ La glose citée au point 1 (« œuvres pour lesquelles un musée… a écrit un doute »)
> est **fausse et retirée** — voir la correction 2026-07-18 (sexies) ci-dessus.

Deux touches sur la couverture d'accueil (demande utilisateur, en petites étapes).

1. **Le chiffre vedette revient sur l'affiche.** La refonte « affiche » avait vidé la
   couverture de tout chiffre (déplacé en « Comprendre les mentions » / « Méthode »).
   L'utilisateur le juge important : c'est sur ces données qu'on travaille. On le
   réaffiche en **preuve secondaire** dans l'aplat sombre, sous l'accroche : **24 507**
   (lu depuis `niveaux.json` via `+page.js`, jamais en dur) + une glose courte
   (« œuvres pour lesquelles un musée de France a écrit un doute sur l'auteur. »).
   L'étage d'accroche « Des milliers d'attributions incertaines » est **retiré** (le
   chiffre le dit, précisément → redondance levée). Corps réduit : ne concurrence pas
   le titre. Voile de contraste mobile étendu (le bloc est plus haut).
2. **Le lien « Accueil » est retiré de la nav de la couverture** (`EditorialNavigation`) :
   cette nav ne s'affiche QUE sur l'accueil → un lien vers la page courante est inutile.
   Les autres pages gardent « Accueil » dans le header (utile là). *Point que j'aurais dû
   signaler de moi-même.*

## 2026-07-18 (quater) — « Les presque » : retour à un maître d'ouverture (guide abandonné, proportions gardées)

**Revirement après essai des deux états** (2026-07-18 ter). Vu à l'écran, l'état
« guide » (arrivée sans maître, invitation + 3 étapes) faisait de la page une
**seconde introduction** : elle se posait au lieu d'explorer. Décision utilisateur :
**revenir à un premier maître déjà sélectionné dès l'ouverture** — la page est un
**espace d'exploration** dès l'arrivée, avec une sélection initiale visuellement forte
(le plus douté, Le Brun, surligné dans le répertoire).

**Ce qu'on garde de la refonte 2026-07-18 (ter)** — les vraies proportions, qui étaient
le bon correctif : **graphe borné** (`.vue { max-width: 42rem }`, aligné à gauche) et
**scène = héros** (portrait + synthèse racontent le maître ; le graphe est une figure de
support). Le problème initial (graphe géant qui écrasait l'intro) reste corrigé.

**Ce qu'on retire** : l'état A / bloc « guide » et la bascule d'état. Une **entrée
éditoriale unique et courte** (titre + chapô qui oriente vers profil/œuvres/musées +
précaution) remplace les deux introductions. `selection` démarre sur `artistes[0]`.
Aucun composant refondu. Build + capture d'ouverture vérifiés.

## 2026-07-18 (ter) — Refonte narration « Les presque » : DEUX ÉTATS (guide / maître) — ✅ CODÉ ⟶ REMPLACÉ par (quater)

**Statut : FAIT (2026-07-18, une passe, un commit).** Spec ci-dessous suivie.

**Réalisé.** `les-presque/+page.svelte` : `selection` démarre à `null`.
- État A (arrivée) : plein cadre d'intro conservé (titre + chapô + précaution) ; la
  zone de droite est un **guide** (invitation « Choisissez un nom » + 3 étapes = les
  3 onglets à venir : profil / œuvres / musées), **aucun portrait ni maître**.
- État B (clic) : l'intro recule en **kicker mince** (« Les presque · 27 noms ») ;
  la scène du maître (`BandeauMaitre` + onglets + vue) s'affiche.
- **Vue bornée** à 42 rem (~672 px), alignée à gauche (règle 1 de la spec).
- Aucun composant existant refondu (Repertoire / BandeauMaitre / Nuage / Œuvres /
  Carte réutilisés tels quels) ; `Repertoire` tolère `selection = null` sans
  surlignage. Mobile : le repli natif du répertoire (bouton « Choisir un maître »)
  fait office d'accès à la liste dans les deux états (pas de refonte de Repertoire).
- Build statique vérifié.

---

**Parti arrêté (spec d'origine, conservée pour mémoire) :**

**Problème constaté** (retour utilisateur 2026-07-18) : `/les-presque` ouvre sur un maître
par défaut (Le Brun) → la scène + le graphe « Profil » **géant** écrasent l'intro ; les
petits textes de présentation deviennent insignifiants ; l'utilisateur arrive au milieu
d'une fiche sans savoir quoi faire. La page **perd** le lecteur au lieu de l'orienter.

**Parti retenu.** Un **répertoire permanent à gauche (constant)** ; la **zone de droite
bascule** entre deux états ; **aucun maître par défaut** (le rail ne bouge pas → pas de
rupture de mise en page).

- **État A — arrivée (aucun maître sélectionné, `selection = null`)** : la zone de droite
  est un **GUIDE**, pas une fiche. Contenu : titre « Les presque » + chapô (ce que sont
  les presque) **en présence forte** + invitation « Choisissez un nom » et les **3 étapes**
  = les 3 onglets à venir (① profil — les formules du doute ; ② œuvres — les mots des
  musées ; ③ musées — la carte). **Aucun portrait, aucun maître affiché.** L'intro
  redevient le contenu principal.
- **État B — un maître sélectionné (clic sur un nom)** : la zone de droite affiche la
  **scène du maître** (portrait + nom + phrase de synthèse + chiffres) puis les onglets
  **Profil · Œuvres · Musées** et la vue. Le cadre/intro **recule** en kicker mince
  (« Les presque · 27 noms ») — il ne disparaît pas, il n'écrase plus.

**Règles d'équilibre (le vrai correctif) :**
1. **Graphe borné** : la vue (nuage / œuvres / carte) reçoit un `max-width` (~600-680 px),
   left-aligné. Fin du graphe qui remplit ~900 px.
2. **La scène est le héros du maître ; le graphe est une figure de support.** La phrase de
   **synthèse** (« le plus souvent de son école, près des deux tiers… ») reste dans la
   scène : c'est elle qui raconte le graphe → le graphe n'a plus besoin d'être énorme.
3. **L'intro change de rôle selon l'état** : plein cadre en A, kicker mince en B.

**Mobile :** État A = intro + guide, puis répertoire **déplié** (noms visibles). État B =
au choix, le répertoire se replie (« Choisir un maître »), la scène s'affiche (repli déjà
en place dans Repertoire.svelte).

**Exécution — une seule passe, un commit.** `selection` démarre à `null` → état A ; clic →
état B. Ajouter un petit bloc « guide » (composant léger OU inline dans la page ; réutilise
les libellés existants) + la logique d'état. Kicker mince en B ; borner la vue. **Aucun
composant existant refondu** (Repertoire, BandeauMaitre, Nuage, Œuvres, Carte réutilisés
tels quels) ; aucun texte de fond réécrit hors l'entrée. DoD : arrivée sans maître
(desktop + mobile), sélection, 3 onglets, retour. Fichier principal :
`web/src/routes/les-presque/+page.svelte` (état + guide + kicker + `.vue { max-width }`).

## 2026-07-18 (bis) — Extension de la direction « affiche » à l'application (C1 : charte v2 + coquille)

L'accueil « affiche » remplace la Direction B comme cap. On l'étend au reste de l'app.
Principe (roadmap ★ DIRECTION « AFFICHE ») : **surface de lecture claire** (le sombre
plein nuirait au texte et aux dataviz) + **cadre au registre de l'affiche** (navy, ivoire,
cobalt, vermillon) + **composition pleine largeur en zones** (fin de la colonne 68 rem par
défaut) + **8 pigments de données inchangés**. Narration : l'accueil étant une pure entrée,
**chaque page porte désormais son entrée** (le sujet et les chiffres n'y sont plus posés).

**C1** : tokens de cadre ajoutés (`--cadre-fond/-encre/-encre-douce`, `--accent-cobalt/
-vermillon`) ; header intérieur en **bandeau navy** (wordmark + nav ivoire, page active
soulignée vermillon), **spectre de tête supprimé** ; pied au même registre. Choix de ne
PAS retirer `max-width` de `main` en C1 : le passage pleine largeur se fait **page par
page** (via `main.pleine`, comme l'accueil) en C2-C4, pour éviter un état transitoire cassé.

## 2026-07-18 — Accueil : l'affiche précisée (entrée pure, accroche 3 étages, nav en cartouches)

Révision de l'affiche d'accueil (image et plein écran conservés). L'accueil est **l'entrée**
dans l'application : il ne résume pas les stats, n'explique pas la méthode. **Accueil seul.**

- **Un seul écran** : plus rien sous la couverture ; **pied de page masqué sur `/`**
  seulement. Répartition assumée du contenu : les chiffres détaillés → « Comprendre les
  mentions », le calcul / les sources / la version / les précautions → « Méthode ». Le
  premier viewport communique uniquement échelle (« un million de notices »), sujet
  (attributions incertaines), approche (enquête dans les données) et les chemins.
- **Accroche provisoire à trois étages** (formulation imposée, non figée éditorialement) :
  chaque phrase = un étage visuel distinct, progression légère, registre d'affiche (pas un
  chapô institutionnel). Aucun chiffre précis réintroduit pour « remplir ».
- **Navigation = cartouches éditoriaux** intégrés à la fiche (bleu-encre, texte ivoire,
  angles quasi droits, largeurs propres, décalés, trait fin), **pas** de boutons/cartes/
  menu/ombre/icône. Motif : les liens noirs fins se perdaient dans l'illustration ; les
  cartouches leur donnent un contraste franc et les ancrent aux rectangles de l'image.
  « Explorer les maîtres » = principale (plus large, plus lourde, cobalt, cible généreuse).
- **Contraste** : par les zones ; **aucun voile global**. Exception assumée et permise par
  le cadrage : sur petit écran, un **dégradé feutré local** (masqué haut/bas, mobile
  uniquement) derrière le bloc titre garantit la lisibilité des étages — jamais un panneau
  opaque ni un voile sur toute l'image. Sous 400 px, tailles/espacements réduits d'abord.
- Interactions inchangées dans l'esprit (≤ ~5 px, trait, contraste, focus visible,
  `prefers-reduced-motion`, `aria-current`).

Fichiers : `LandingCover.svelte`, `EditorialNavigation.svelte` réécrits ; `+page.svelte` /
`+page.js` réduits ; `+layout.svelte` (pied de page masqué sur `/`).

## 2026-07-17 (septies) — Accueil = affiche interactive (nouvelle direction, prototype, accueil seul)

Direction B jugée trop classique/rigide (« image de catalogue »). Nouvelle piste
**limitée à l'accueil** : une **affiche interactive** à partir de deux illustrations
fournies. Les pages intérieures **restent en Direction B** (comparaison des deux systèmes).
Prototype à juger sur captures avant toute extension.

Choix :
- **Deux assets distincts, pas un seul recadré** : `<picture>` avec l'asset horizontal
  (desktop / tablette paysage) et la composition verticale autonome (mobile / **tablette
  portrait ≤ 1024 px**, via `orientation: portrait` — sans quoi l'horizontal se recadre
  trop et la nav quitte la fiche). `object-fit: cover`, `object-position: center`.
- **Textes et nav = HTML superposé**, jamais dans le bitmap. Titre (Fraunces, clair
  légèrement froid) dans l'aplat sombre ; navigation en **annotations** reliées aux lignes
  de la fiche claire (charbon), « Explorer les maîtres » en entrée principale ; routes
  réelles (dont `/echelle`). Mention de source courte et discrète.
- **Contraste par les zones** (clair sur aplat sombre / charbon sur fiche claire),
  **aucun voile** couvrant l'image, pas de panneau opaque ni d'ombre forte.
- **Interactions sobres** : déplacement ≤ 4 px, prolongement de la ligne, contraste,
  ~180 ms ; focus clavier visible ; `aria-current` (Accueil) ; `prefers-reduced-motion`.
- **Coquille** : masthead + spectre **masqués sur `/` uniquement**, `main` pleine largeur
  (`main.pleine`). Le premier viewport est exclusivement la couverture ; le chiffre 24 507
  et la source vivent **sous la ligne de flottaison**.
- **Traçabilité** : `web/static/cover/` + `README.md` — illustrations générées pour le
  projet, évoquant la **base de données Joconde** (archive/index/open data), **pas** Léonard
  ni le tableau *La Joconde*. Outil de génération à préciser par l'auteur.

Composants créés : `LandingCover.svelte`, `EditorialNavigation.svelte` (pas davantage).

## 2026-07-17 (sexies) — Direction B : refonte des pages restantes (modèle de travail, non validé)

**Statut.** Direction B **non validée définitivement** : rendu jugé trop classique /
générique. Menée jusqu'au bout pour obtenir une version complète et comparable — un
**modèle de travail** pour une future direction fondée sur un modèle visuel plus précis.
On n'a donc ni défendu ni enrichi l'esthétique ; pas de nouvel effet, folio ou ornement
hors cadrage. Données et textes éditoriaux validés inchangés ; rubriques en réserve non
réactivées.

Choix de composition, par page (un commit chacun) :
- **Profil** : en-tête compact pour faire remonter le profil au premier écran (les
  textes validés sont conservés, seule leur mise en page change) ; répertoire resserré
  pour élargir le graphe ; onglets soulignés ; folio/cote **discrets** (repère
  secondaire, jamais un décor), tirés des données (rang + `musee_principal.code`).
- **Œuvres** : abandon de la grille de cartes blanches au profit d'une liste continue à
  filets ; le verbatim (mots exacts du musée) passe en tête de hiérarchie ; un
  **emplacement média réservé** par entrée matérialise les futures reproductions sans en
  inventer. Ordre par mention et bloc « d'après » conservés.
- **Musées** : suppression du plafond 32 rem ; grande carte + flanc (légende, hors-cadre,
  collant). Logique de projection, points fixes, liens POP et tooltips **inchangés**.
- **Comprendre les mentions** : la ligne ne sert qu'une fois (les trois territoires) ;
  définitions en trois colonnes ; comparaison chiffrée conservée (barres, échelle
  commune, réserves de recouvrement).
- **Méthode** : sommaire en rail collant + colonne de contenu ; **la ligne n'est pas
  imposée** là où elle n'explique rien (consigne). Contenu validé intégralement conservé.

Geste transversal : toutes les **boîtes grises arrondies** (précaution, « à part »,
sommaire) deviennent des **filets** — cohérence Direction B, moins d'encadrés.

## 2026-07-17 (quinquies) — Direction artistique retenue : B « la ligne de proximité » (+ coquille & accueil)

Après la revue globale (planche de l'existant, diagnostic, trois directions maquettées
avec vraies données/portraits/polices), la **Direction B « la ligne de proximité »**
est retenue.

**Pourquoi B.** Le diagnostic pointait une app « trop documentaire » : colonne centrée
étroite, boîtes grises répétées, dataviz qui flotte, pages sans rôle visuel distinct,
allure générique. B fait du **sujet la structure** : une ligne horizontale continue, de
la main du maître (chaud) à sa seule influence (froid), organise chaque page ; les huit
pigments en sont les stations. C'est la direction la plus **identifiable** (tirée de la
donnée, pas d'une métaphore extérieure), elle **occupe l'écran**, donne un **rythme
commun**, et réutilise le nuage horizontal déjà en place (donc moins de refonte dataviz).
Emprunts prévus aux autres pistes : **verbatims-matière** + **portrait N&B** + infographies
titrées/sourcées (dir. C, second choix), **folios/cotes** et traitement en « entrée »
(dir. A). Directions A et C conservées en réserve de maquettes (scratchpad).

**Implémentation, palier 1 — coquille + accueil.** Par pages complètes, jamais par
microcomposants (consigne utilisateur).
- **Token `--spectre`** (`tokens.css`) : dégradé des huit pigments, chaque couleur au
  centre de sa station (i+0,5)/8, température = distance. Signature du projet.
- **`Spectre.svelte`** : la ligne réutilisable (bande + libellés des trois territoires
  en option, alignés sur les segments de l'axe ; repli mobile sans chevauchement).
- **Coquille** (`+layout.svelte`) : le **filet brun de tête est remplacé par la ligne**
  (spectre 3 px en signature sur toutes les pages) ; canevas élargi (`--largeur-max`
  60 → **68 rem**) pour finir la colonne étroite (le texte courant reste borné page par page).
- **Accueil** (`+page.svelte`) : recomposé — spectre à territoires en tête, grand titre
  Fraunces, promesse, **CTA en encre** (plus un bouton de landing) + lien souligné ocre,
  figure de données à 8 stations, chiffre 24 507 en **preuve secondaire**. Textes validés
  inchangés (composition seule). La figure « Joconde » reste provisoire/remplaçable.

Pages non encore refondues (Explorer, Comprendre, Méthode) : intactes et fonctionnelles
sous la nouvelle coquille (vérifié). Décisions différées du bandeau maître non rouvertes.

## 2026-07-17 (quater) — Socle V1 : Méthode, Accueil-couverture, nav à 4 entrées

Clôture du socle éditorial V1. Décisions :

1. **Page Méthode = une page unique, éditoriale.** Cinq sections (Périmètre ·
   Construction des données · Lire les chiffres · Limites · Sources et droits) plutôt
   qu'une FAQ ou une suite de cartes. Tous les chiffres sont **lus depuis les exports
   canoniques** (jamais réécrits) : la page devient fausse si le pipeline change, mais
   jamais incohérente avec lui.

2. **Correction d'une divergence de données (source canonique qui fait foi).** La
   catégorie « copie » était affichée à 22 844 dans `typologie.md` (somme naïve
   `d'après 22 564 + copie 280`, qui ignore le recouvrement de 220 notices). La valeur
   canonique dédupliquée est **22 624** (`niveaux.json` `copie`, `vue_ensemble`
   `copies_dapres.total`). Corrigé dans `typologie.md` (+ révision 27 273 → **27 270**,
   même cause). Règle retenue : **l'interface et les docs reprennent la valeur de
   l'export**, pas une somme recalculée à la main. « d'après » seul reste 22 564.

3. **Accueil = couverture éditoriale, le chiffre en preuve secondaire.** Deux zones
   (promesse / figure). Le grand nombre (24 507) quitte le premier plan : il devient une
   preuve sous la couverture, avec renvoi à la Méthode. Le cas mono-musée (Nice/Barla)
   sort de l'accueil (trop technique) → Méthode uniquement (architecture §3).

4. **Figure « Joconde » = figure de DONNÉES, provisoire et assumée.** Zone média
   remplaçable : un motif schématique (rangées de « notices » + les 8 pigments des
   mentions le long d'une ligne de proximité), pas une reproduction de *La Joconde* ni un
   chapitre Léonard (architecture §6). Aucun visuel définitif imposé : la légende dit
   « composition provisoire ». La direction artistique tranchera à la revue globale.

5. **Nav publique recentrée à 4 entrées actives** : Accueil · Explorer les maîtres
   (route `/les-presque`) · Comprendre les mentions (`/echelle`) · Méthode (`/methode`).
   « Les révisions » et « La carte » **retirées de la nav publique** ; leur code et leurs
   données restent au dépôt (routes non liées, réintégrables). Fin des entrées grisées
   « à venir » (le champ `prete` et la branche sont conservés pour plus tard).

Nouveaux fichiers : `web/src/routes/methode/+page.{js,svelte}`, accueil refondu
(`web/src/routes/+page.svelte`). Ces deux pages **terminent le socle**, elles ne sont pas
l'aboutissement de la direction artistique.

## 2026-07-17 (ter) — Zone « Comprendre les mentions » (page autonome du vocabulaire)

Création du chapitre autonome prévu par l'architecture §3. Choix consignés :

1. **Réutiliser la route `/echelle`**, pas en créer une concurrente. Le placeholder
   « L'échelle du doute » devient la page du vocabulaire ; le libellé public passe à
   **« Comprendre les mentions »** (provisoire — le recentrage complet de la nav à
   4 entrées reste à faire, hors périmètre de cette tâche).

2. **Barres, jamais d'anneau** (déjà acté 2026-07-15, ici appliqué). Deux panneaux
   « petits multiples » à **échelle commune** (même `maxPart`) : l'ensemble de Joconde
   (24 507) et les 27 noms (2 341). La comparaison de FORMES rend visible le
   basculement (« attribué à » domine globalement ; école/atelier/manière montent dans
   les 27). Une **troisième série** (hors 27) n'a pas été ajoutée : sa forme recopie
   presque l'ensemble (22 166 sur 24 507), elle n'améliore pas la lecture.

3. **Ne pas présenter les barres comme les parts exclusives d'un tout.** Les mentions
   se recouvrent : aucune n'est empilée, chaque barre est une part indépendante des
   œuvres concernées, et une note dit explicitement que « les parts ne s'additionnent
   pas à 100 % ». Les copies « d'après » (22 564) sont nommées **à part** (pas un
   doute). La concentration mono-musée (Nice/Barla) est **renvoyée à la page Méthode**
   d'une phrase, sans en faire le récit de la page.

4. **Sources uniques, aucun doublon.** Définitions = champ `corps` de
   `familles-public.js` ; regroupement + annotations = `territoires.js` ; couleurs =
   tokens de pigments. La formule type n'apparaît que là où `montrerMention` est vrai
   (règle anti-répétition existante), avec un nom générique « un maître ». Aucun terme
   interne (« famille », « niveau », « presque lui »…) dans la copie.

Nouveaux fichiers : `web/src/routes/echelle/+page.{js,svelte}`, composant
`web/src/lib/BarresMentions.svelte`. `vue_ensemble.json` ajouté à `sync:data`.
Détail d'affichage : « <1 % » quand une part non nulle arrondirait à zéro.

## 2026-07-17 (bis) — Charte palier 3 : zone TroisTerritoires (principe visuel central)

Rendre lisible, dans le graphique lui-même, la **distance à la main du maître**
(architecture §5). Choix consignés :

1. **Regroupement, pas nouvelle nomenclature.** Les huit mentions restent celles de
   `familles-public.js` (labels + couleurs, source unique) ; on ne fait que les
   **grouper** en trois territoires, dans une primitive dédiée `territoires.js`
   (titre + annotation courte par zone). Réutilisable telle quelle par « Comprendre
   les mentions ». L'ordre de l'axe (`ORDRE_FAMILLES`) fait déjà correspondre chaque
   territoire à une plage contiguë de colonnes (0-1 / 2-4 / 5-7) ; un garde-fou en
   dev signale toute dérive entre les deux modules.

2. **Une seule ligne de proximité, pas trois cartes.** Les territoires sont matérialisés
   par des **fonds très légers contigus** (tokens `--territoire-pres/autour/influence`,
   dérivés des pigments repères, température = distance), des **séparateurs fins** aux
   frontières internes, et des **titres** en tête. Aucun cadre ni marge entre les zones :
   le graphe reste un continuum gauche → droite. À éviter explicitement (architecture §8) :
   l'effet « trois blocs décoratifs indépendants ».

3. **Annotations éditoriales dans la clé HTML, pas dans le SVG.** Le texte SVG ne revient
   pas à la ligne : une annotation par territoire y serait illisible en mobile. Les
   annotations vivent donc dans la **clé de lecture** sous le graphe, qui **rétablit du
   même coup la clé minimale** que la sortie de la légende du répertoire (2026-07-17)
   avait retirée. La clé reprend les trois territoires (titre, annotation, mentions à
   pastilles), en cellules contiguës qui rejouent les bandes du graphe.

4. **Données, points, couleurs, tooltips inchangés.** Recadrage purement visuel : la
   géométrie a été ajustée (bandeau de titres en tête, plot descendu) mais l'échelle
   commune, les positions et l'infobulle harmonisée sont intactes. Accessibilité :
   `aria-label` du graphe enrichi (les trois territoires), `aria-label` des points
   conservé.

Nouveaux fichiers : `web/src/lib/territoires.js` ; tokens `--territoire-*` dans
`tokens.css`. Vérifié sur trois profils opposés (Ingres/Le Brun/Rembrandt : le volume
principal tombe dans un territoire différent) et en mobile.

## 2026-07-17 — Charte palier 3 : zone Répertoire (colonne de navigation)

Deuxième zone du kit. Choix consignés :

1. **Un composant dédié `Repertoire.svelte`**, pour matérialiser la séparation
   répertoire ↔ profil (architecture §4) : la page ne garde que `selection` (liée),
   toute la logique de choix (recherche, tri, liste) vit dans le répertoire.

2. **Tri : « Œuvres concernées » par défaut, « A→Z » en option.** Motif :
   « trier par valeur, sauf ordre naturel » (CLAUDE.md) — le doute EST la valeur du
   dossier, on garde donc l'ordre décroissant par défaut ; l'alphabétique n'est qu'une
   aide pour retrouver un nom précis. Libellés publics (« Œuvres », pas « doute » ni
   « notices »). Tri alphabétique sur le nom affiché complet (`localeCompare` fr).

3. **Sélection active renforcée** : filet d'accent à gauche + fond soutenu +
   `aria-current="true"`. Le filet est transparent au repos (réservé à l'actif) pour
   ne pas décaler la largeur d'un rang quand il devient actif.

4. **Retrait de la légende détaillée** (`LegendeFamilles`) de sous la liste. Elle
   n'appartient pas au répertoire (outil de choix) : elle rejoindra « Comprendre les
   mentions » (architecture §3), chapitre autonome sur le vocabulaire. Le composant
   reste au dépôt pour cette reprise ; en attendant, les couleurs restent explicables
   par les tooltips (jauges, graphique) — état transitoire assumé.

5. **Responsive repliable** (architecture §4 « colonne fixe ou repliable ») : sur
   mobile, un bouton replie/déplie le répertoire ; replié d'emblée pour donner la
   priorité au profil, refermé après un choix. `matchMedia` en `$effect` plutôt qu'un
   `<details>` natif (piège de réouverture selon la largeur, cf. 2026-07-13) ; en
   pré-rendu l'effet ne tourne pas, l'état par défaut « déployé » sert le desktop.

Note d'outillage (pas une décision de fond) : `vite preview` charge le manifeste du
build à son démarrage — après un rebuild, **le redémarrer**, sinon il sert d'anciens
chunks CSS hachés (404) et la page s'affiche sans ses styles de composant.

## 2026-07-16 (quinquies) — Charte palier 3 : prototype du kit (BandeauMaitre, ChiffreVedette, onglets)

Premier palier de code du kit de composants (charte §5), en prototype sur la fiche
maître réelle. Trois décisions à consigner, dont une qui touche l'**approche
éditoriale** (donc à valider) :

1. **Onglets renommés** Graphique/Œuvres/Carte → **Profil · Œuvres · Musées**.
   Motif : libellés éditoriaux (ce que le lecteur y trouve), pas des noms de forme
   de dataviz. Mapping : *Profil* = le graphique des formes du doute (nuage),
   *Œuvres* = les cas concrets, *Musées* = la carte géographique. État interne
   `vue` aligné (`profil`/`oeuvres`/`musees`).

2. **Synthèse calculée dans le bandeau — réintroduction assumée.** Le bloc de profil
   avait perdu tout « angle » le 2026-07-10 (2e passe) : le paragraphe de situation
   ne faisait plus que situer volume et dispersion. La charte du 2026-07-16 demande
   une **« phrase de synthèse calculée »** dans BandeauMaitre. On la réintroduit,
   mais **strictement factuelle** : elle nomme la **formule la plus fréquente** pour
   ce maître (famille dominante d'artistes.json) et sa part, sans dire ce que la
   formule « signifie ». Cohérent avec « on lit ce que les musées écrivent » : c'est
   un constat de fréquence, pas une interprétation du doute (le sens reste aux
   tooltips et au graphique). Le paragraphe volume/dispersion, lui, ne change pas.
   **⏸ à valider** (formulation « Le plus souvent : « … », <part> des œuvres concernées »).

3. **Limite de `fractionEnMots` à corriger.** Le helper plafonne à
   « près des deux tiers » (seuil 62 %). Or la formule dominante peut monter bien
   plus haut : *école de* Le Brun ≈ 240/310 = **77 %**, rendu « près des deux tiers »
   → **sous-estimation**. Options si le point 2 est validé : ajouter des paliers
   hauts au helper (« plus des trois quarts », « la grande majorité »…) OU réserver
   `fractionEnMots` aux fractions basses/moyennes et traiter la dominante à part.
   Non tranché ici (`fractionEnMots` est partagé, ne pas le modifier sans décision).

Composants : `web/src/lib/ChiffreVedette.svelte` (grand nombre Fraunces tabulaire +
légende), `web/src/lib/BandeauMaitre.svelte` (portrait agrandi + nom + synthèse +
chiffres, seuil mono-colonne géré en `@container`). Périmètre tenu : ni répertoire,
ni nuage, ni accueil touchés.

## 2026-07-16 (quater) — Chantier direction artistique & architecture éditoriale (cadrage, ⏸ à valider)

Insertion d'un chantier de cadrage **plus haut niveau que le kit de composants** :
repenser l'application comme une **publication éditoriale** centrée sur « Les
presque », pas comme une succession de blocs fonctionnels. Le problème n'est plus
la charte (couleurs/typo/coquille cohérentes) mais la **direction artistique** et
l'**architecture éditoriale**. Document de cadrage créé : **`docs/architecture-editoriale.md`**
(note de direction, à valider ; aucun code, nav du front non modifiée).

Axes cadrés (détail dans le document) :
- **Nav publique recentrée à 4 entrées actives** : Accueil · Explorer les maîtres ·
  Comprendre les mentions · Méthode. Réserve (Avant/après, échelle, carte) **hors
  nav** ; fin des entrées grisées « à venir ». **« Vue d'ensemble » n'est pas une
  entrée** : elle vit dans « Comprendre les mentions ».
- **Accueil = couverture éditoriale** : promesse d'abord, chiffre (24 507) ensuite,
  exception de Nice renvoyée en Méthode ; composition asymétrique prenant l'écran.
- **Explorer les maîtres = séparation nette répertoire ↔ profil** (colonne de
  navigation à gauche ; scène du maître à droite avec bandeau de profil + phrase de
  synthèse calculée ; vues Profil / Œuvres / Musées).
- **Comprendre les mentions** = chapitre autonome du vocabulaire des 8 formules +
  Vue d'ensemble, organisé par les **trois territoires**.
- **Méthode** = page unique ; une seule phrase de prudence visible ailleurs.
- **Principe visuel central = la distance à la main du maître** (3 territoires :
  au plus près / autour / dans son influence), décliné partout.

**Précision utilisateur sur l'illustration Joconde** : elle renvoie à la **base de
données Joconde** (archive, notices, grille, index, open data, esthétique numérique
sobre), **pas** à *La Joconde* comme œuvre ni à Léonard. Traitée en **figure de
données**, langage visuel **reproductible** (déclinable à d'autres maîtres / formes
abstraites), jamais dépendante d'une seule image. Viser une figure **originale** ;
tout élément externe = source secondaire, licence vérifiée fichier par fichier
(règle CLAUDE.md), déclarée ici et en Méthode.

Ce cadrage **précède et oriente le palier 3 (kit de composants)** : on ne
reconstruit les composants qu'au service de cette architecture. Libellés de menu et
titres du projet **à confirmer** (décision des titres toujours différée).

## 2026-07-16 (ter) — Charte : palier 2 — coquille « inventaire » (fait)

Deuxième palier, limité à **header, navigation, structure générale** (ni fiche
maître ni composants internes touchés ; données intactes ; rubriques en réserve
intactes).

- **Coquille refaite** (`+layout.svelte`) : filet d'accent (terre brûlée) en tête
  de page ; **masthead** aligné sur la colonne de contenu (`--largeur-max`),
  wordmark en Fraunces à gauche, nav à droite ; **navigation « catalogue »** en
  Public Sans, petites capitales espacées ; **indicateur de page courante**
  (`$app/stores` → `aria-current` + soulignement d'accent) ; items en réserve
  estompés (inchangés dans leur contenu). Rythme passé aux **tokens** (`--espace-*`,
  `--filet`, `--taille-*`).
- **Italique Spectral intégrée** (demande utilisateur, pour futures micro-légendes
  / mentions) : `source_fonts.py` régénère avec `Spectral:ital,…` ; le style entre
  dans le nom de fichier (`spectral-400i-*`), le romain existant est préservé.
  10 woff2 désormais dans `static/fonts/`.
- **Espaces fines des grands nombres vérifiées** : « 24 507 » (Fraunces) affiche
  correctement l'espace fine insécable → RAS.
- Vérifié par capture avant/après (accueil + Les presque, page active soulignée),
  `npm run build` OK.

Note d'outillage (sans impact code) : `vite preview` sert un `build/` incohérent
si on rebuild à chaud → toujours redémarrer le preview après un build pour les
captures (sinon CSS de layout en 404).

Restes pour le palier 3 (kit composants) : nombres de listes/dataviz en Public
Sans tabulaire ; appliquer l'italique Spectral aux micro-légendes/mentions ;
unifier cartes/onglets/légende/barres.

## 2026-07-16 (bis) — Charte : palier 1 — base typographique globale (fait)

Premier palier d'implémentation de la charte, volontairement **limité à la typo**
(pas de refonte de composants, données intactes, fiche maître non touchée,
rubriques en réserve intactes).

- **Polices en local, sans CDN.** Script reproductible `web/scripts/source_fonts.py`
  (même esprit que `source_portraits.py`) : télécharge les woff2 (sous-ensembles
  latin + latin-ext, pour « œ ») dans `web/static/fonts/` et génère
  `web/src/lib/styles/fonts.css` (URLs locales `/fonts/…`). 8 fichiers, ~277 Ko
  au total. Fraunces et Public Sans en **variable**, Spectral en 400/600.
  Ces fichiers sont des **assets versionnés** (comme `static/portraits`, `static/geo`).
- **Tokens ajoutés à `tokens.css`** : `--police-titre` = Fraunces, `--police-texte`
  = Spectral, `--police-ui` = Public Sans (avec fallbacks) ; **échelle typo**
  (`--taille-*`), **espacement** (`--espace-1..6`), **rayons**, **filets**,
  `--surface-carte`, `--ombre-douce`, `--focus-anneau`. Georgia + system-ui retirés.
- **Base typographique globale seulement** (dans `+layout.svelte`) : `body` =
  Spectral ; `h1`/`h2` = Fraunces (h3 laissé en Spectral pour **ne pas surutiliser
  Fraunces**) ; `button`/`input`/`select`/`table` = Public Sans ; `th`/`td` en
  chiffres tabulaires ; nav et pied en Public Sans, wordmark en Fraunces.
- **Vérifié par capture avant/après** (accueil + Les presque) : identité nettement
  plus « catalogue », « œuvres » (latin-ext) OK, `npm run build` OK.

Restes connus (pour le palier composants) : nombres des dataviz/listes encore en
serif (à passer en Public Sans tabulaire) ; vérifier l'espace fine des grands
nombres en Fraunces ; italique Spectral non encore embarquée. Source de vérité de
la direction : `docs/charte-graphique.md`.

## 2026-07-16 — Charte graphique : direction arrêtée (application-cadre)

Décision de travailler la charte de **toute l'application-cadre** *L'inventaire du
doute* (pas seulement la rubrique des 27 maîtres), « Les presque » servant de
terrain d'épreuve V1, avec extensibilité aux dossiers futurs. Proposition de
direction validée ; **source de vérité = `docs/charte-graphique.md`**.

Points arrêtés :
- **Concept** : « un inventaire, pas un tableau de bord » (catalogue de musée :
  papier crème, encre, filets, marges) ; idée directrice = distance à la main du
  maître (température des pigments).
- **Ambiance typographique « Catalogue savant »** (choix utilisateur) : **Fraunces**
  (titrage / chiffres vedettes / verbatims) + **Spectral** (texte éditorial) +
  **Public Sans** (UI, données, labels ; IBM Plex Sans en alternative). Libres
  (OFL), **auto-hébergées** (woff2 sous-ensemblées, pas de CDN). Georgia +
  `system-ui` abandonnés (cause du « trop normé »). Chiffres tabulaires partout,
  kickers en petites capitales.
- **Palette** : conservée et formalisée en 3 étages (neutres / accent éditorial
  terre brûlée / couleurs sémantiques), la **boîte de pigments inchangée** ;
  mécanisme d'**accent par dossier** (`--accent-presque/-revisions/-copie`).
- **Tokens à ajouter** (absents) : espacement, rayons, filets, ombre douce, focus,
  échelle typo.
- **Kit de composants** à unifier (cartes, onglets, légende, barre) autour de
  primitives partagées ; `Infobulle` gardée ; `GalaxieMaitre` au placard.
- **Extensibilité** : cadre agnostique du dossier ; pas de reskin par dossier ;
  Vue d'ensemble = pas d'anneau.

Pas de code à ce stade (proposition de direction). Prochain palier pressenti :
tokens + typographie dans `tokens.css`, puis la coquille.

## 2026-07-15 (quater) — « Vue d'ensemble » : export préparé, cadré prudemment (pas de front)

Après le rapport de reconnaissance (docs/donnees.md 2026-07-15), l'utilisateur
valide une future section « Vue d'ensemble » des formulations prudentes, mais
**strictement sur le solide**. Export dédié créé : `data/exports/web/vue_ensemble.json`
(`src/build_vue_ensemble.py`, recalculé depuis les exports validés, `assert` de
cohérence). Contenu retenu :
- familles de doute **global / dans‑27 / hors‑27** (8 familles, `presume` exclue) ;
- **niveaux global vs 27** + **global hors monoculture** (14 223 / 3 537 / 956) ;
- bloc **monoculture** (Nice/Barla, 5 791) ; totaux ; **copies « d'après » à part** (22 624).

**Choix explicites (à respecter côté front plus tard) :**
- **Pas de diagramme en anneau** ici : les familles se recouvrent (pas une
  partition) → barres, jamais un donut.
- **Pas de classement par nom hors des 27** (désambiguïsation absente).
- **Pas de période en V1** (~16 % datables).
- **Domaines** : seulement avec caveat de double‑comptage (multi‑valué) — **hors
  export** à ce stade.
- **Top musées** : laissés **en réserve** (données dispo, non incluses).
- **Message central** porté par la vue et écrit dans le JSON (`message_central`) :
  « attribué à » domine au global ; école/atelier/manière prennent le dessus dans
  les 27 → c'est ce contraste (niveau 1 global 81,7 % vs niveau 2 dans‑27 52,7 %).

Pas de front pour l'instant. Export **non synchronisé** vers `web/static/data/`
(reste dans `data/exports/web/`) tant qu'aucune dataviz ne le consomme.

## 2026-07-15 (ter) — RECENTRAGE : « Les presque » devient la 1re publication complète

Décision de cadrage (utilisateur, après évaluation externe). Plutôt qu'une
« encyclopédie inachevée de toutes les formes de doute » (plusieurs rubriques
inégales juxtaposées), on construit **une enquête visuelle complète sur une seule
forme du doute : « Les presque »** — les œuvres que les musées rapprochent d'un
grand maître sans les lui attribuer (« attribué à », « atelier de », « école de »,
« manière de »…). Motif fort propre au projet : cela répond directement au défaut
de compréhension déjà constaté (un visiteur ne saisit pas un front à 6 chantiers).

**Conséquences actées maintenant :**
- **Les autres rubriques passent en PAUSE / réserve** : « Avant / après »
  (`/revisions`), « L'échelle du doute », « La carte ». Le code et les données
  restent dans le dépôt (rien n'est supprimé) — dossiers futurs de
  *L'inventaire du doute*. `/revisions` repasse `prete: false` (hors nav publique).
- Tout le travail « Avant / après » (pipeline `build_revisions.py`,
  `revisions.json`, tests, onglets, anneau, cartes, `revisions-labels.js`,
  `VignetteOeuvre`) est **conservé en l'état** comme dossier 2 prêt à reprendre.

**Encore OUVERT (mes recommandations, non tranché par l'utilisateur) :**
- Titre/marque : garder « L'inventaire du doute » comme cadre + sous-titre de
  dossier « Les presque — autour des grands maîtres » (reco), vs titre unique, vs
  renommage. **Non décidé.**
- Périmètre de la v1 : socle (Accueil + Les maîtres + Méthode) d'abord vs complet
  (+ Le vocabulaire du presque + Comparer) vs décider après la charte. **Non décidé.**
- Garde-fous à intégrer quand on avancera : rendre visible le critère des 27 noms
  (≥ 20 notices de doute hors copie, après désambiguïsation — pas un panthéon) ;
  ne pas garder d'onglets désactivés en nav publique ; le cas Alençon reste un fil
  narratif valide (formules prudentes = « presque »).
- **À faire plus tard** : amender le cadrage large de `CLAUDE.md` (question
  centrale + Alençon) pour refléter ce resserrement éditorial.

Prochaine étape pressentie : figer la charte graphique sur « Les maîtres » comme
socle, puis décider titre + périmètre.

**Réalignement documentaire acté le 2026-07-15 (sexies, journal).** Décision
formulée : « La V1 publique de *L'inventaire du doute* sera centrée sur le dossier
"Les presque". Les autres rubriques ou formes de doute, notamment "Avant / après",
restent documentées et conservées dans le projet, mais ne font plus partie du
périmètre publiable initial. » Répercutée dans `roadmap.md` (bloc « ★ RECENTRAGE » :
périmètre V1 / en réserve / déjà fait ; P3-T2 marquée EN RÉSERVE),
`rubrique-revisions.md` (bandeau), `README.md` (État du projet). Aucun code, aucune
suppression, aucun déplacement.

## 2026-07-15 (bis) — « Avant / après » : « Les œuvres » prototype 1 catégorie (⏸ validation)

Onglet « Les chiffres » (anneau) validé comme base (réserves notées : force
visuelle de l'anneau à revoir en passe charte ; garder « L'œuvre est reclassée
comme copie » partout). Étape 5 du brief : prototype d'UNE catégorie de « Les
œuvres » avant généralisation. Fait sur « Un nom en remplace un autre » :

- **Nouveau composant `web/src/lib/VignetteOeuvre.svelte`** : image 4:3 affichée
  seulement si statut ∈ {open, authorized} + url + credit (image cliquable vers
  POP, crédit sous l'image) ; sinon **placeholder soigné** (bordure fine,
  pictogramme discret, « Reproduction non affichée » + « Droits de réutilisation
  en cours de vérification »). Jamais de rectangle gris vide, jamais de hotlink.
- **`CarteRevision` refondu** : variantes `principale` (horizontale, vignette à
  gauche) / `secondaire` (verticale, vignette en haut) ; vocabulaire
  « Attribution antérieure » / « Attribution actuelle » / « Consulter la notice
  sur POP → » (fin de « A porté »/« Aujourd'hui ») ; antérieure un peu plus
  discrète mais **jamais barrée** ; phrase de récit dérivée de la catégorie
  (revisions-labels.js) ; bord gauche à la **couleur de la catégorie** (cohérent
  avec l'anneau). Surcharges `libelle`/`recit`/`couleur` pour le filtre
  transversal « inverse ».
- **Modèle image enrichi** dans le pipeline (`build_revisions.py`) : `image` gagne
  `alt` et `licence` (tous null/pending) — les futures images s'ajouteront sans
  reconstruire les cartes.
- **Onglet « Les œuvres »** : titre interne « Les changements, œuvre par œuvre »,
  chips « libellé · N exemples » (distinct des nombres du corpus), phrase d'intro
  propre au filtre sélectionné, **carte principale** large puis **grille 2
  colonnes** (jamais 3), 1 colonne sur mobile.

Le système de cartes est générique : la validation porte sur le MODÈLE (vu sur
« Un nom en remplace un autre »). Généralisation = vérifier les autres filtres
(verbatims longs, cartes « inverse ») + petits ajustements. `pytest` = 60,
`npm run build` OK, prototype + mobile vérifiés par capture. Restent ensuite :
« En bref » puis « Repères » (2 colonnes) puis passe mobile/a11y d'ensemble.

## 2026-07-15 — « Avant / après » : refonte datajournalisme (étapes 1-3, ⏸ validation)

Application d'un brief dirigiste (approche datajournalisme) qui garde les 4 onglets
mais retravaille chaque onglet comme un chapitre autonome. Contraintes fortes
reprises : pas de dashboard, pas de scrollytelling, pas de logique juste/faux ni
rouge/vert, ne jamais présenter une révision comme une erreur corrigée ni
l'attribution actuelle comme définitive. Vocabulaire imposé : « Attribution
antérieure » / « Attribution actuelle » / « Consulter la notice sur POP → ».

Le brief impose son propre ORDRE avec points de validation. **Fait (étapes 1-3),
en attente de validation avant « Les œuvres » :**

- **Libellés recentralisés** (3e passage). Source de vérité du NOM = pipeline
  (`revisions_classify.py` → `libelles_categorie`). Nouveaux libellés :
  `autre_nom` = « Un nom en remplace un autre » · `anonyme` = « Le nom n'est plus
  retenu » · `meme_nom` = « Le nom demeure, avec réserve » · `copie` = « L'œuvre
  est reclassée comme copie » · `deja_copie` = « L'ancienne attribution était déjà
  une copie » · `plusieurs_noms` = « Plusieurs noms se succèdent » · `mineur` =
  « Cas particuliers ». Pseudo-catégorie transversale (galerie) `inverse` =
  « De l'anonymat à une attribution nominative » (décrit la notice, n'affirme pas
  qu'on a retrouvé le véritable auteur).
- **Nouveau module front `web/src/lib/revisions-labels.js`** : source unique pour
  ce que le JSON ne porte pas — couleur par catégorie, appartenance aux deux
  groupes éditoriaux, phrase d'intro par filtre, phrase de récit par carte, def
  `inverse`. Palette : famille **violette** (passages lisibles) + famille **chaude
  ocre/taupe** (trajectoires complexes) — cohérente autour de l'accent, pas
  d'arc-en-ciel, pas de hiérarchie morale ; la couleur distingue les deux groupes.
- **Onglet « Les chiffres » refait** : barres → **diagramme en anneau**
  (`web/src/lib/AnneauRevisions.svelte`). Justification dataviz (exigée par le
  brief) : Q = « comment se répartissent les 26 667 notices ? » ; message = une
  composition d'un tout ; l'anneau lit une part-d'un-tout que des barres ne
  racontent pas. Centre = total au repos, puis pct/libellé/nombre au survol/focus.
  Légende chiffrée en 2 groupes = couche accessible (boutons focusables clavier ;
  segments décoratifs `aria-hidden`). Constat « 49,2 % » en tête + 3 enseignements ;
  **toutes les valeurs calculées depuis `revisions.json`** (constat, et 27,6 % =
  mineur+plusieurs_noms+deja_copie), aucune codée en dur.
- **Chapô permanent** remplacé (formulation « observe les passages d'une
  formulation à une autre, sans décider laquelle constitue la bonne attribution »).

Reste à faire (prochaines étapes du brief, après validation) : « Les œuvres »
(carte principale + grille 2 colonnes, intros par filtre, phrase de récit par
carte, composant placeholder image 4:3 avec statut de droits, vocabulaire
« Attribution antérieure/actuelle »), puis « En bref », puis « Repères » (deux
colonnes « Ce que montrent les données / Ce qu'elles ne permettent pas de
conclure »), puis passe mobile + accessibilité. `pytest` = 60, `npm run build` OK,
anneau vérifié par capture (repos + survol).

## 2026-07-14 (quater) — « Avant / après » : palier de réorganisation ÉDITORIALE

La V1 (tout sur une page) n'était pas publiable : contenu en vrac, narration non
structurée, labels trop techniques, cartes trop « base de données ». Palier de
réorganisation **éditoriale** (pas de refonte graphique, pas d'images) validé et
implémenté.

**Onglets** (titre + chapô permanents au-dessus) : *En bref* (présentation +
une carte emblématique + lien vers la galerie) · *Les chiffres* (le graphe en
deux temps : « Le constat principal » = 4 familles de galerie à échelle commune,
puis « Les cas secondaires » = 3 familles atténuées) · *Les œuvres* (chips par
type, **un seul groupe déroulé à la fois**, jamais les 32 d'un coup ; chip
transversal « Un nom réapparaît » = direction inverse) · *Repères* (limites
courtes, renvoi à la future page méthode).

**Labels publics refondus** (phrase qui dit ce qui arrive au NOM, plus de
« Vers… ») — source de vérité `revisions_classify.py`, rebuild fait :
`autre_nom` = « Un autre nom apparaît » · `anonyme` = « Le nom disparaît » ·
`meme_nom` = « Le nom reste, avec réserve » · `copie` = « L'œuvre est reclassée
comme copie » · `plusieurs_noms` = « Plusieurs noms se succèdent » · `deja_copie`
= « Déjà une copie au départ » · `mineur` = « Cas particuliers » ; direction
inverse (badge) = « Un nom réapparaît ».

**Images — modèle de données RÉSERVÉ, rien d'affiché.** Chaque `cas` de
`revisions.json` porte désormais `image: { statut, url, credit, source }`, statut
∈ `open | authorized | pending | restricted`, tous à **pending**. `CarteRevision`
prévoit l'emplacement mais n'affiche une vignette que si statut ∈ {open,
authorized} ET url ET credit. **Jamais de hotlink POP** (la Licence Ouverte
couvre le texte, pas les clichés) ; droits à clarifier fichier par fichier plus
tard (voie Wikimedia, comme les portraits).

**Hors de ce palier** (assumé) : charte graphique, images affichées, autres
graphes (daté/non daté, anciens noms, siècles, domaines → page méthode ou V2),
filtre par ancien nom, ligne éditoriale par carte, vraie page « Méthode et
limites ». `pytest` = 60 OK, `npm run build` OK, 4 onglets + filtre vérifiés par
capture.

## 2026-07-14 (ter) — « Avant / après » : bilan v2 VALIDÉ, cadrage front ouvert

L'utilisateur **valide le bilan post-vérification et la taxonomie à 7 catégories**.
Précisions actées :

- **« Même nom, plus prudent » maintenue comme catégorie publique à part entière**
  (minoritaire à 4 %, mais elle raconte une nuance : le nom reste, la notice ajoute
  une réserve). **Libellé public retenu : « Le même nom, avec réserve »** (préféré
  à « Même nom, attribution plus prudente »). → à répercuter dans le pipeline
  (`libelles_categorie.meme_nom` et `passages`, `revisions.json`) au moment du front.
- **Chaînes** (« Plusieurs anciens noms ») : conservées dans les statistiques,
  **hors galerie V1**.
- **Cas déjà « d'après »** (« Déjà une copie ou un d'après ») : conservés dans les
  statistiques, **hors galerie V1**.
- **Direction inverse** (anonyme → un nom, 5 283) : conservée pour **équilibrer le
  récit** (le doute ne va pas que vers moins de certitude).
- **Lot V1 = 32 cas** (par diversité, plafond 2/musée) validé.
- **Tests figés avant front** validés.

Ouvre la phase de restitution front (proposition sans code d'abord : structure,
graphes, place de la galerie, wording public des 7 catégories, cartes exemples).

## 2026-07-14 (bis) — « Avant / après » : bilan de vérification + taxonomie v2 (fait, ⏸ validation)

Vérification manuelle des 80 lignes rendue par l'utilisateur (`echantillon_
revisions_annotes.csv`) : **44 OK, 18 à exclure, 8 faux passage, 10 faux
parsing**. Le « à exclure » vaut pour la galerie seulement — pas pour les
statistiques ni la méthode (consigne explicite). Refonte de la classification
en conséquence (`src/revisions_classify.py`, testée, calée sur les 80 verdicts).

**Taxonomie v2 — 7 catégories** (au lieu de 4), 3 nées de la vérification :
- *Vers un autre nom* (galerie) — 13 125 (49,2 %)
- *Même nom, attribution plus prudente* (galerie, NOUVEAU) — 1 062 (4,0 %) :
  même artiste, mais l'aujourd'hui ajoute une réserve (« Furini → Furini
  attribué », « Rembrandt → Rembrandt manière de »). Demandé par l'utilisateur.
- *Vers l'anonyme* (galerie) — 3 371 (12,6 %)
- *Vers une copie* (galerie) — 1 742 (6,5 %)
- *Déjà une copie ou un d'après* (stats, NOUVEAU) — 968 (3,6 %) : l'ancien label
  était lui-même une copie ; pas un passage depuis une attribution pleine.
- *Plusieurs anciens noms* (stats, NOUVEAU) — 3 177 (11,9 %) : chaînes de ≥ 2
  hypothèses distinctes ; trop complexes pour une carte, gardées en statistiques.
- *Changement mineur ou complexe* (stats) — 3 222 (12,1 %) : anonyme national →
  anonyme, confirmations (« école de X → X »), notes de prose.

Règles de distinction validées : une chaîne du **même** nom (Champaigne/Villot ;
Champaigne/Brière) n'est PAS « plusieurs noms » (une hypothèse, plusieurs
sources) ; « même personne » couvre l'inclusion de prénom (Le Nain Louis ↔ Le
Nain) ; « plus prudent » exige que l'aujourd'hui porte une réserve (sinon
c'est une confirmation, rangée en mineur) ; précédence côté aujourd'hui = nom >
copie > anonyme. Écoles nationales seules (« École florentine → Pietro da
Rimini ») **gardées en galerie** avec le verbatim (plus d'exigence d'un ancien
nom extrait).

**5 bugs de parsing corrigés** (repérés par l'échantillon) : parenthèses
imbriquées (« Santi Di Tito (16e (2e moitié), Italie) » → nom sale) ; nom sali
par une date (« GIOTTO, attribué en 1859 » → coupe à virgule/chiffre) ;
« Changement d'attribution » / prose pris pour nom ; « ; » biographique DANS une
parenthèse (« Dyck (Anvers, 1599 ; …) ») qui coupait à tort en deux hypothèses
→ découpage respectant les parenthèses ; parenthèse ouvrante orpheline en tête.

**Direction inverse** recomptée : 5 283 (anonyme → un nom), à valoriser.

**Contrôle figé** (`tests/test_revisions.py`, 25 cas + cohérence CSV) : 44/44 OK
restent en galerie, 0 cas « à exclure/faux passage » n'y fuit. Suite complète
`uv run pytest` : 60 passés.

**⏸ Validation du nouveau bilan** attendue avant le front (consigne utilisateur).

## 2026-07-14 — « Avant / après » : pipeline construit + échantillon (fait, ⏸ vérif)

Orientation V1 validée par l'utilisateur (libellés publics ajustés). Construit
`src/build_revisions.py` → `data/exports/web/revisions.json` (16,7 Ko) et
`src/build_revisions_sample.py` → `data/exports/echantillon_revisions.csv`
(80 lignes stratifiées). Front non touché.

Libellés publics figés : « Vers un autre nom / une attribution prudente /
l'anonyme / une copie » (jamais « destination » ni le code interne).

Arbitrages de construction (détail dans donnees.md) :
- **Anciens noms = filtre, pas palmarès.** Le graphe de fréquence est fragile
  (copies « d'après » comptées à tort ; effet mono-musée Louvre — Michel-Ange
  202/233 au Louvre). Comptage retenu **hors « d'après »** ; on s'en sert pour
  filtrer la galerie, pas comme classement vedette.
- **Parsing renforcé** : préfixe-artefact « ancienne attribution : » (style
  Louvre) retiré avant extraction du nom ; rejet anonyme/école/chiffre.
- **Direction inverse chiffrée** (5 584, ≈ « vers l'anonyme ») : à raconter,
  elle équilibre le propos (autant d'œuvres gagnent un nom qu'en perdent).
- **Lot V1** : plafond 2/musée GLOBAL (pas par type) → 32 cas, 19 musées,
  Louvre 6 %. Sélection déterministe (graine implicite : ordre CSV + tri image).

Invariants `assert` à la génération : partition des passages = 26 667 ; quotas
du lot atteints ; aucun cas sans référence POP ; plafond musée respecté.

**⏸ Prochaine étape = vérification manuelle de l'échantillon par l'utilisateur**
(colonnes verdict/commentaire), avant de figer des tests et de coder le front.

## 2026-07-14 — « Avant / après » : cadrage V1 simplifié (arbitrages)

Reprise du cadrage sur une base plus simple (demande utilisateur). Détail
complet : **docs/rubrique-revisions.md** (réécrit V1). Arbitrages :

- **Titre provisoire : « Avant / après »** (sous-titre non figé, retravaillé
  plus tard — priorité au contenu).
- **Structure primaire = par type de passage** (autre artiste / anonyme /
  encore prudent / copie « d'après »), **grands noms en filtre secondaire** au
  mot entier. Confirmé par les données : les destinations sont propres et
  chiffrables ; par période (16 % datables) ou par musée (règle non
  négociable) = écartés comme structure. L'intuition utilisateur est suivie.
- **Lot éditorial réduit** (~32, fourchette 24–40), sélection **par diversité**
  et non par prestige : plafond **2 cas/musée**, quotas par destination,
  lisibilité (ancienne courte mono-segment, ancien nom extractible, titre
  présent). Testé : 32 cas, 10 musées, **Louvre 19 %** (au lieu de 59,5 %) —
  la diversité défait mécaniquement la concentration. Cas ambigus (chaînes,
  prose, écoles nationales) exclus de l'interface, réservés à la page méthode.
- **Images : PAS d'affichage en V1** (audit du 2026-07-14, donnees.md). Le CSV
  n'a pas d'URL ; POP sert l'image depuis un CDN interne sans mention de
  droits par œuvre ; la Licence Ouverte couvre le texte, pas les clichés
  (droits musée). On ne hotlinke pas un CDN gouvernemental et on ne peut pas
  vérifier 26 667 licences → **carte textuelle + lien POP**. Illustration
  manuelle d'une poignée de cas via Wikimedia Commons envisageable plus tard
  (précédent portraits), à décider séparément — rien promis avant sourcing.
- **Statistiques générales** sur tout le corpus, **graphes classiques
  seulement** : barres (destinations, domaines, anciens noms), donut
  (datée/non datée), colonnes (siècle), une barre + phrase (concentration).
  Pas de visualisation expérimentale.
- **Export** `revisions.json` adapté : totaux + destinations + domaines +
  siècles + anciens noms (top ~15, mot entier) + lot de cas V1. `Presence_image`
  conservé comme métadonnée honnête, **non affiché**.

⏸ En attente de validation : titre provisoire, structure par type de passage,
lot V1, absence d'images, liste des graphes, schéma d'export. Puis pipeline →
échantillon de vérification manuelle → tests → front. Rien n'est codé.

## 2026-07-13 — Audit des briques restantes : « Révisions » en prochaine rubrique, carte en pause, décodeur fondu

Déclencheur : demande utilisateur — « choisir ce que les données rendent
vraiment lisible, pas ce que la roadmap prévoyait ». Audit complet du CSV et
des exports (constats détaillés dans donnees.md, même date).

**Décidé (constat validé par l'utilisateur)** :

- **Prochaine rubrique : les révisions « on a cru → aujourd'hui »**
  (`Ancienne_attribution`). Motif : 26 667 vrais avant→après, des noms qui
  parlent (Vinci 511, Poussin 350, Rubens 236, Rembrandt 227 — comptés au mot
  entier), des destinations chiffrables, tout le matériau déjà dans le CSV.
  C'est aussi la brique qui héberge l'objet « doute + révision » promu en
  P2-T1 (4 615 notices).
- **Carte nationale qualifiée : EN PAUSE.** Sa question (« le doute est-il
  réparti ou concentré ? ») a déjà sa réponse (concentré — monoculture
  Barla) ; le *où* honnête existe déjà (carte par maître, un point = un musée
  détenteur) ; le biais de couverture ferait cartographier l'effort de
  catalogage. On ne la défend pas par principe ; réouverture seulement sur un
  angle neuf.
- **Décodeur de l'échelle du doute : réduit, plus une rubrique.** La légende
  permanente des « presque » (LegendeFamilles) couvre déjà l'essentiel
  (libellés + sens + couleurs). Ce qui manque — le poids national de chaque
  formule et un exemple réel — deviendra un encart de la page « méthode et
  limites » ou de l'accueil.

**Risques et garde-fous de la rubrique Révisions** (détail, schéma d'export
et contrôles dans **docs/rubrique-revisions.md**) :

- sensationnalisme → registre : « la notice a porté le nom de X ; elle dit
  aujourd'hui Y » ; jamais « déchu », « démasqué », « erreur » ; les verbatims
  entre guillemets sont la seule matière ;
- « les musées se sont trompés » → renversé : le champ EST la preuve du
  travail d'attribution, c'est le musée qui garde la trace ; certaines
  anciennes attributions sont des propositions de catalogues savants, pas des
  affirmations du musée ;
- palmarès des grands noms → les noms = un filtre d'accès (mot entier),
  jamais un classement ; l'intro explique le biais d'attraction (les
  inventaires anciens donnaient volontiers aux grands noms) ;
- concentration Louvre/dessins (59,5 % / 62,9 %) → divulguée dans l'intro
  (précédent : monoculture Barla, 2026-07-05) ; jamais de comparaison entre
  musées ;
- faux avant/après → règles de comparaison versionnées : normalisation hors
  parenthèses, mot entier partout, extraction stricte ou pas d'extraction,
  chaînes affichées verbatim, noms proches jamais fusionnés, comparaison
  segment par segment (le dernier segment d'une chaîne peut être
  l'attribution actuelle).

**⏸ En attente de validation utilisateur** : titre de la rubrique, forme (vue
d'ensemble des destinations + galerie de cas filtrable), schéma de
`revisions.json`, plan de contrôles (échantillon de vérification manuelle
avant tout front). Rien n'est codé côté front.

## 2026-07-13 — À TRANCHER : priorité « ? » vs formule de distance dans un même segment

Déclencheur : notice POP `M0347001723` (« Tête de femme : Le Silence », Dole),
segment `SARTO Andrea del (?, manière de)` → classée **« ? » (niveau 1)** pour Andrea
del Sarto. Cause : `famille_segment()` renvoie la **première** formule dans l'ordre
`DOUTE_PAR_NIVEAU` (niveau 1 → 3), donc « ? » (niv. 1) l'emporte sur « manière de »
(niv. 3). C'est la hiérarchie **documentée** (« famille la plus légère »), pas un bug.

Question éditoriale ouverte : le musée place l'œuvre « dans la manière de » (loin du
maître) ; la ranger en niveau 1 (« presque lui ») **surestime la proximité** — ce que
la règle « on ne surpromet pas » veut éviter.

Ampleur (scan complet, 1 023 705 lignes) : co-occurrences de ≥ 2 formules = **227
segments (0,89 %)**, rares. « ? » écrase une formule de **distance** (niv. 2/3) dans
**≈ 79 segments** base entière (atelier 51, école 15, **manière 7**, entourage 5,
genre 1) ; « ? + attribué à » (87) reste niveau 1 des deux façons (seul le libellé
fin changerait). Sous-ensemble sur les 27 maîtres = plus petit (non encore compté).

Options : **A.** « ? » gagne (actuel, surestime la proximité) · **B.** la formule de
distance gagne, le « ? » devient une nuance (plus fidèle, plus prudent) · **C.** idem
B mais formalisé (« ? » gagne seulement seul ou avec « attribué à »). **Reco : B/C.**
Non tranché, non codé (demande utilisateur : diagnostic d'abord). Prochaine étape si
on avance : compte exact par maître sur les 27, puis choix A/B/C.

## 2026-07-13 — « Les presque » : intro réécrite, plus explicative (décision utilisateur)

L'ancien chapô donnait une ambiance mais ne disait pas assez où on emmène le lecteur.
Nouveau parti pris : **titre « Les presque » conservé** (identité) mais **glosé dès la
première phrase** ; l'intro explique ce que la rubrique montre, justifie le choix des
27 noms (noms de référence pour lesquels les musées emploient souvent des formules
prudentes, au moins vingt œuvres concernées — explicitement *pas* « les plus grands »)
et **oriente** le lecteur vers les quatre lectures (jauge colorée, graphique, œuvres,
carte). Encadré refait sans émoticône, recentré sur l'invariant : « ne réattribue
aucune œuvre… reprend les mots publiés par les musées… avec leurs précautions ».
Contraintes tenues : pas de « famille/niveau/au doute » en surface, les musées ne
« se trompent » pas (incertitude = savoir honnête), aucune expertise sous-entendue.
Texte témoin de la copie publique journalistique sobre.

## 2026-07-13 — Carte, palier style (décision utilisateur)

Finition visuelle only (données et comportement figés). **Fond « régions très
estompées »** retenu (contre « silhouette France seule » et « statu quo ») : garder
les frontières régionales comme repère, mais très pâles, pour ne pas concurrencer
les points. Autres réglages actés : survol/focus des points **plus franc** (pleine
opacité + halo blanc élargi), **pas de distinction au repos** des points cliquables
(le curseur main au survol suffit — deux classes visuelles embrouilleraient) ; carte
dans une **colonne centrée** (titre/fond/légende/mentions alignés) ; légende et
mention hors-cadre au **même registre** (petit corps, encre douce, filet). Le repère
texte du **musée principal** est écarté de ce palier (c'est du contenu, pas du style).

## 2026-07-13 — Identification du maître : test MOT ENTIER au lieu de sous-chaîne (décision utilisateur)

**Déclencheur** : un lecteur signale la notice POP `07980002404` (« Archimède »,
MUDO Beauvais) classée « attribué à **Rodin** ». Son auteur réel est
« SERODINE Giovanni (attribué, peintre) » — Giovanni Serodine, peintre italien du
XVIIᵉ. La **détection de la formule** (« attribué ») était juste ; c'est
l'**identification du maître** qui déraillait : `_trouve_maitre` testait par simple
sous-chaîne (`"RODIN" in pivot`), et « SE‑RODIN‑E » contient « RODIN ».

**Ampleur mesurée** (scan de toute la base, 1 023 705 lignes) : 8 maîtres, 77
segments faussement rattachés, dont **13 notices de doute** seulement (Le Tintoret 6,
Léonard de Vinci 6, Rodin 1) ; le reste ne gonflait que des dénominateurs « sous le
nom » (propre/copie). Collisions : SERODINE/PERRODIN→Rodin, VINCIDOR→Vinci,
SOLDYCK/DYCKHOFF→Van Dyck, RIBERAT/VALRIBERA→Ribera, POUSSINES→Poussin,
CORREGES→Corrège, et « TINTORETTO Domenico » (le *fils*) → Le Tintoret.

**Correctif retenu** : `_trouve_maitre` teste désormais le **mot entier**
(`\bALIAS\b`) sur le pivot normalisé, pour les inclusions ET les exclusions.
Vérifié sur données réelles :
- règle les 8 cas ci-dessus ;
- **garde** les vraies notices de Le Tintoret : elles sont cataloguées « Le Tintoret
  ou il Tintoretto (Jacopo Robusti dit) », où « Tintoret » est un mot entier ; seul
  « Tintoretto Domenico » (une seule racine, pas de frontière) est écarté ;
- **seule perte assumée** : 1 notice avec la coquille « IIngres » (double I), en
  propre — négligeable.

**Impact sur les chiffres publiés** (doute) : Le Tintoret 53→47, Léonard 56→50,
Rodin 81→80 ; les autres maîtres inchangés en doute. **Aucun maître ne passe sous le
seuil des 20 doutes** : la liste vedette des 27 est préservée. Exports régénérés,
front synchronisé, build statique OK. (Constat sur les données dans donnees.md.)

## 2026-07-13 — Carte : écartement des points + point-lien POP pour l'œuvre unique (décision utilisateur)

Deux chantiers de la carte, même séance.

**Écartement des points (chevauchements).** À taille fixe, deux musées pouvaient se
cacher : coordonnées quasi identiques (deux musées d'une même ville — Marseille,
Versailles) ou points très proches (grappe francilienne Paris/Versailles, Lille/Douai).
`geo.js` reçoit `ecarterPoints` : relaxation itérative **déterministe et sans
dépendance** qui repousse chaque paire trop proche jusqu'à `2·R + 1,5 px`, au plus
près de la vraie position ; les points confondus sont séparés selon l'angle d'or
(rendu stable). Contour blanc renforcé (1,1 px), opacité 0,82.

**Point-lien POP pour l'œuvre unique** (validé avant code). Objectif : rendre la
carte plus concrète sans images (droits/disponibilité). Quand un musée conserve
**exactement une** œuvre concernée, on veut pouvoir aller à sa notice publique.

- **Piège tranché** : un lien DANS le tooltip serait inclicable (tooltip en
  `pointer-events: none`, s'efface au départ du curseur). Donc **pas de lien dans le
  tooltip, pas de tooltip épinglable** : c'est **le point lui-même qui devient un
  lien** (`<a>` SVG → `lienPop(reference)`, `target=_blank`, `rel=noreferrer`,
  curseur main, focus clavier visible). Le tooltip reste un **aperçu** : musée+ville,
  « 1 œuvre concernée », **titre si disponible** (entre guillemets, italique), mention
  publique + pastille. Les musées **multi-œuvres restent non cliquables**, tooltip
  inchangé. Pas de nouvelle vue « œuvre » : on enrichit juste certains points.
- **Pipeline** (`build_artistes.py`) : pendant l'agrégation par musée, on retient la
  **première** notice (`ref1`, `titre1`) — qui est l'unique quand `doute==1` ; à
  l'export, `oeuvre_unique: {reference, titre}` n'est émis **que si `doute==1`**
  (entrées multi-œuvres inchangées, poids négligeable). Le front bâtit l'URL avec
  `lienPop`. Mesuré à la génération : **188** musées à 1 œuvre avec titre, **2** sans
  titre (titre `null` géré : intitulé de lien générique « … de cette œuvre »).
- `Infobulle.svelte` reçoit un champ optionnel `titre` (ligne d'aperçu).
- Vérifié : URL POP correcte, `target/rel`, aria-label (« Voir la fiche publique de
  “titre” »), Louvre multi non cliquable (circle, pas de lien), cas sans titre,
  focus clavier affiche l'aperçu. Build statique OK.

## 2026-07-13 — Harmonisation des tooltips (graphique / carte / jauges) (décision utilisateur, après revue)

Depuis que la **légende fixe** porte la grammaire des couleurs, le tooltip ne doit
plus l'expliquer : il donne seulement l'information LOCALE au point survolé, avec
le même vocabulaire public partout et aucun retour de « famille / niveau / au
doute / presque lui / autour de lui ».

**Diagnostic.** Les trois tooltips vivants passent déjà par `Infobulle.svelte`
(pas de styles parallèles) : graphique (`NuageFamilles`), carte (`CarteMaitre`),
jauges (`BarreFamilles`). Le `title=` natif de `BarreNiveaux.svelte` n'est branché
nulle part (code mort, laissé de côté). Le travail est donc surtout du style sur
`Infobulle` + une harmonisation de données.

**Structure commune** (un seul schéma `tt`, chaque vue ne remplit que le nécessaire) :
`header` (bande grisée en tête), `headerPastille?` (couleur → pastille dans le
header, côté graphique), `valeur?` (nombre local accordé), `corps?` (phrase de
sens, graphique), `lignes?` (`[{ label, couleur, valeur, appoint? }]` — ventilation
carte/jauge, `appoint` = complément gris type « 73 % »), `mentionType?` (footer
discret « Mention type : … », graphique si utile).

**Style commun sur `Infobulle`** : largeur STABLE (`width: max-content`, bornée
`min 13rem / max 17rem` — le texte passe à la ligne au lieu d'élargir, plus de saut
de largeur) ; header en **bande légèrement grisée** (fond `rgba` très léger, texte
`--couleur-encre-douce`, filet de séparation), pastille optionnelle inline ; valeur
en évidence ; lignes = libellé à gauche, **nombre aligné à droite en chiffres
tabulaires**, `%` en gris ; ombre discrète, bordure fine, padding cohérent.

**Jauges de la liste — changement de comportement** (décision utilisateur) : d'un
tooltip PAR SEGMENT (header = mention, « N œuvres · X % du doute ») à **un seul
récapitulatif du maître** : header = nom du maître, une ligne par mention (pastille
+ nombre + %). Cohérent avec la carte, plus robuste (les segments sont sous-pixels,
trop fins à viser un par un) ; toute la barre devient une seule cible focusable
(les segments passent en présentation, `aria-hidden`), aria-label = récap complet.
La formule « % du doute » disparaît (mot banni).

**Fichiers** : `Infobulle.svelte` (style + `headerPastille` + `valeur` optionnelle
+ `appoint`), `familles-public.js` (`tooltipFamille` renvoie `headerPastille`),
`BarreFamilles.svelte` (récap maître). `NuageFamilles`/`CarteMaitre` inchangés
(leur `tt` était déjà compatible). Vérifié par captures : graphique multi + à 1
œuvre (+ « Mention type »), carte multi + à 1 œuvre concernée, jauge récap, largeur
étroite 390 px (pas de débordement).

## 2026-07-13 — Légende permanente des mentions sous la liste des maîtres (décision utilisateur, validée avant code)

Une **clé des couleurs visible avant interaction**, commune aux trois vues
(graphique / œuvres / carte), pour que les tooltips ne portent plus seuls
l'explication et harmoniser jauges / graphique / cartes œuvres / tooltips carte.

- **Emplacement** : dans l'`aside` de gauche, **sous la liste des maîtres** (hors
  de la zone d'onglet). La liste scrolle dans son cadre (`max-height` + overflow) :
  la légende reste donc toujours visible sous elle.
- **Source unique, zéro seconde nomenclature** : réutilise TELS QUELS `header`
  (libellé public) et `corps` (sens court) de `familles-public.js`, dans l'ordre
  `ORDRE_FAMILLES` (= l'axe du graphique). La légende dit exactement les mêmes mots
  que les tooltips → le lecteur relie les deux sans effort.
- Chaque entrée : **pastille ronde** (couleur stable de la famille, comme les
  points de carte et les pastilles de tooltip) + libellé public + une phrase de
  sens très brève. Intitulé discret « Les mentions ». Pas de « famille / niveau /
  au doute / presque lui / autour de lui » dans l'interface.
- **Un `corps` reformulé** (source unique, sert aussi les tooltips) : atelier,
  « Son atelier, pas forcément sa main. » → **« Sorti de son atelier, pas forcément
  de sa main. »** (évite de répéter le libellé « Son atelier » dans la légende).
- **Mobile (< 720 px)** : l'`aside` s'empile au-dessus de la fiche → la légende est
  **repliable** (bouton « Les mentions » + chevron), **repliée par défaut** pour ne
  pas repousser la carte ; **toujours dépliée sur desktop** (intitulé simple).
  L'état est piloté en JS (`matchMedia`) et non par un `<details>` natif : le
  contenu d'un `<details>` fermé n'est pas ré-affichable en CSS selon la largeur
  (constaté sur Chromium, même avec `!important`).
- **Aucune donnée touchée** : la légende lit `FAMILLE_PUBLIC`, statique.
- Nouveau composant `web/src/lib/LegendeFamilles.svelte`, importé dans
  `les-presque/+page.svelte`. Vérifié par captures (desktop + mobile replié/déplié).

Palier suivant, séparé (non fait) : harmonisation du **style des tooltips**
(largeur, header grisé, espacements, typographie).

## 2026-07-12 — Carte par maître : taille de point FIXE (décision utilisateur, après test A/B)

Le premier rendu utilisait un rayon ∝ √doute (taille variable). À la revue,
confusion signalée : l'échelle étant **propre au maître affiché**, un gros cercle
chez Ribera (3 œuvres) paraissait aussi important qu'un gros cercle chez Le Brun
(276). Test A/B sur captures (Le Brun, Ribera, Van Dyck, Ingres), variable vs fixe :

- **variable** : ne « marche » que sur un vrai dégradé (Van Dyck) ; ailleurs il
  ment sur l'échelle inter-maîtres, gonfle de petits volumes (Ribera : gros disques
  qui se chevauchent au nord pour 3 œuvres) et empiète sur le rôle de l'onglet
  graphique (le *combien*) ;
- **fixe** : lisible pour les 27 maîtres, honnête (un point = une présence, jamais
  un rang), et cohérent avec la règle « jamais de comparaison entre musées sur des
  comptages bruts ».

**Retenu : taille fixe** (tous les points identiques, `R_POINT = 5`). La carte
répond à *où* ; le *combien* par musée reste **au survol** (tooltip) et dans
l'onglet **graphique**. Rayon variable, échelle commune, calibres de légende :
retirés. Bascule de test (`?carte=fixe`) retirée. Légende : « Un point = un musée
où au moins une œuvre concernée est conservée. Passez sur un point pour voir
combien, et sous quelles formules. »

**Tooltip refait (même séance).** L'ancien tooltip réintroduisait les libellés de
NIVEAU écartés (« Presque lui », « Autour de lui »). Remplacé par la **couche des
familles publiques** (`familles-public.js`, comme graphique / œuvres / jauges) :
en-tête « musée, ville », valeur « N œuvre(s) concernée(s) », puis une ligne par
famille **triée par valeur**, avec **pastille de couleur stable** et libellé public
(`header` : « Son atelier », « De son école », « Attribué à »…). Plus aucun
« niveau », « au doute » ni jargon. `Infobulle.svelte` étendu (additif) d'un champ
optionnel `lignes` (label + valeur + couleur) réutilisable ailleurs. Accord
singulier/pluriel géré ; `aria-label` du point conservé (résumé linéaire).

## 2026-07-12 — Carte par maître : spécification du composant (décision utilisateur, validée avant code)

Spécification arrêtée avant toute écriture de code. Le fond (régions métropole,
france-geojson) et le palier données (`musees_doute`) sont déjà validés (mêmes
date). Ce qui suit fige la **forme** du composant.

**Emplacement.** Troisième vue de la bascule existante des fiches « Les presque »,
à côté de `Graphique` et `Œuvres`. Onglet nommé **`Carte`** ; titre interne au-dessus
du fond : **« Où sont conservées ces œuvres »**. La carte est la réponse visuelle
au 2ᵉ chiffre du profil (« N musées où ces œuvres sont conservées »).

**Une carte = une question : où, et combien.** La position est géographique (donc
« prise ») ; la mesure est portée par la **taille** du point.

- **Taille.** 1 point = 1 musée détenteur. **Rayon ∝ √(doute)** (aire ∝ nombre),
  borné (min ~3 px, max ~22 px) pour que le Louvre n'écrase pas les petits musées
  et que ceux-ci restent visibles. Points dessinés du plus grand au plus petit
  (petits au-dessus). L'aire seule se comparant mal (CLAUDE.md), la taille est
  **appuyée par une légende de calibre + le survol**.
- **Couleur : unique et stable** pour tous les points (token d'accent « doute »),
  identique sur toutes les fiches (décision utilisateur). **Pas** de couleur par
  niveau sur la carte : cela ferait une 3ᵉ variable visuelle concurrente et
  dupliquerait le rôle du `Graphique`. La ventilation par niveau vit dans le tooltip.
- **Tooltip** (survol / focus clavier) : nom du musée — ville, total de doute,
  puis ventilation par niveau via les libellés publics (« Presque lui », « Autour
  de lui », « Son style, sans lui »), ligne omise si le niveau vaut 0. Jamais de
  code interne ; la formule du musée peut figurer entre guillemets.
- **Légende** minimale, dans le cadre : 2–3 cercles de calibre gradués (l'« axe »
  de la taille) + une ligne « Un cercle = un musée. Plus il est grand, plus ce
  musée conserve d'œuvres au nom de ce maître avec une mention de doute. » Pas de
  bloc « comment lire » séparé.

**Repli (carte qui n'apporte rien).** L'onglet `Carte` reste **toujours visible**
(une bascule qui change de forme d'une fiche à l'autre désoriente). C'est le contenu
qui bascule : s'il n'y a **qu'un seul musée projeté**, on affiche une phrase à la
place de la carte (« Ces œuvres sont conservées dans un seul lieu : le musée X, à
Ville. »). Sinon (≥ 2 musées projetés), carte. Cas limite assumé : Le Brun concentre
89 % à Paris mais compte 19 musées → carte affichée, la concentration se lit dans
la taille du point parisien.

**Mention hors-cadre.** Un musée dont `lat/lon` tombe hors de la fenêtre métropolitaine
n'est **pas projeté** mais **reste compté** (totaux, 2ᵉ chiffre du profil, `musees_doute`).
Ligne visible sous la carte : « Hors cadre métropolitain : N œuvre(s) conservée(s)
au musée … à Ville. » À la génération du 2026-07-12, un seul cas : Van Dyck, 1 œuvre
au musée de Saint-Denis de La Réunion. Détection par bornes lat/lon figées dans un
util partagé (`web/src/lib/geo.js`), communes à la projection et au test.

**Fichiers prévus.** Nouveaux : `web/src/lib/CarteMaitre.svelte`, `web/src/lib/geo.js`
(projection `geoConicConformal` calée France + bornes métropole + helper « projetable ? »).
Modifiés : `web/src/routes/les-presque/+page.svelte` (3ᵉ bouton + `{#if vue === 'carte'}`),
`web/src/lib/joconde.js` (libellés publics des niveaux exposés pour le tooltip),
`web/src/lib/styles/tokens.css` (token couleur des points si absent). Dépendance
`d3-geo` à ajouter dans `web/package.json`. Fond : `web/static/geo/regions-metropole.geojson`
(déjà en place). Docs à mettre à jour à la mise en œuvre : `methode-et-limites.md`
(fond IGN = illustration jamais donnée ; hors-cadre non projeté mais compté),
`roadmap.md`.

## 2026-07-12 — Carte par maître : palier données, `musees_doute` dans `artistes.json` (décision utilisateur, mise en œuvre)

Avant de coder la carte, on enrichit l'export (audit préalable dans donnees.md,
même date). La carte répondra à : « Où se trouvent les œuvres dont l'attribution
à ce maître est formulée avec prudence ? » — **1 point = 1 musée détenteur**,
taille ∝ nombre d'œuvres douteuses de ce maître dans ce musée.

`build_artistes.py` exporte désormais, par maître :

- `musees_doute` : liste triée par `doute` décroissant, **1 entrée = 1 musée**,
  alimentée **uniquement sur le doute** (jamais le ferme ni la copie). Chaque
  entrée : `code`, `nom`, `ville`, `lat`, `lon`, `doute`, `niveaux` (triplet),
  `familles` (liste ordonnée `{code, notices}`, pour la couleur et le tooltip).
- `nb_musees_doute`, `musee_principal` (`{code, nom, doute, part}`) pour piloter
  les replis côté front (peu de points / forte concentration).
- `doute_sans_musee` : notices de doute sans code musée identifiable (mesuré à
  **0** partout à la génération du 2026-07-12).

Le champ `musees` existant (entier, toutes catégories confondues) est **conservé
tel quel** : il correspond à son libellé public actuel (« où ces œuvres sont
conservées », tous statuts). Il ne doit pas servir à la carte.

**Deux garanties exigées et tenues (décision utilisateur) :**

1. **Invariants de comptage**, vérifiés par `assert` à la génération :
   par musée `somme(familles.notices) == doute` et `somme(niveaux) == doute` ;
   par maître `somme(musees_doute[].doute) + doute_sans_musee == doute`. Le build
   échoue si un invariant casse.
2. **Coordonnées explicites `lat` / `lon`** (et non `[lat, lon]`) pour écarter
   tout risque d'inversion côté carte D3-geo. Source géo **secondaire** : le champ
   `coordonnees` de Joconde localise le **musée** (constant par code), jamais
   l'œuvre, et ne compte rien.

Rappels de cadrage (contraintes non négociables) : carte **par maître** seulement,
jamais de carte globale du doute ; **pas de comparaison brute entre musées** — la
carte montre une **dispersion**, pas une vérité patrimoniale ; fond de carte local
auto-hébergé, aucune tuile externe, aucun serveur.

## 2026-07-12 — Carte par maître : fond auto-hébergé (régions métropole, france-geojson) (décision utilisateur, mise en œuvre)

Fond de carte sourcé et validé avant tout composant. Contrat arrêté :
**france-geojson · régions · métropole seule · Licence Ouverte · `static/geo/`
versionné · projection `geoConicConformal` · La Réunion hors-carte signalée.**

- **Source** : `regions.geojson` du dépôt france-geojson (Grégoire David),
  tracés IGN Admin Express COG 2018, **Licence Ouverte / Etalab**. URL, licence,
  date, commande et poids avant/après consignés dans `web/static/geo/README.md`
  (reproductible). Récupéré le 2026-07-12.
- **Fichier produit** : `web/static/geo/regions-metropole.geojson`, 13 régions
  métropolitaines (le fichier source n'inclut déjà aucun DROM), props `code`/`nom`.
  Simplifié mapshaper `-simplify 5% keep-shapes precision=0.0001` :
  1 452 343 → **70 619 octets** (−95 %). Fichier **versionné** (ressource source
  stable, pas un artefact du pipeline `sync:data`).
- **Niveau régions** (13 polygones) et non départements : fond discret, la mesure
  reste les points-musées. Bascule départements triviale plus tard si besoin.
- **Projection** : `d3.geoConicConformal()` + `fitSize` sur ce fichier. Pas de
  projection composite (elles servent à recoller les DROM, écartés ici).
- **Outre-mer — réserve utilisateur intégrée** : métropole seule sur le fond,
  mais le point hors métropole (mesuré : 1 seul, musée Léon Dierx à La Réunion,
  1 œuvre de Van Dyck) **reste dans `musees_doute` et dans les totaux**. Le front
  devra afficher une **mention explicite dans l'interface** (pas seulement en page
  méthode), du type « Hors cadre métropolitain : 1 œuvre conservée à Saint-Denis
  de La Réunion ». Spéc à honorer au moment du composant.
- **Source secondaire d'affichage** : le fond ne porte aucune donnée, ne compte
  rien, n'exclut aucun musée. Déclaré en page méthode (methode-et-limites.md) et
  crédité en petit corps sous la carte (« Fond : régions IGN Admin Express 2018,
  via france-geojson — Licence Ouverte »).

Prochaine étape (non commencée) : composant carte. Non codé tant que ce fond
n'est pas validé.

## 2026-07-12 — Palette contrastée (luminosité alternée) + jauges explicables au survol (décision utilisateur, validée sur simulation)

**Palette révisée.** La « boîte de pigments » du 2026-07-11 ne jouait que sur la
teinte ; les familles voisines restaient trop proches, en particulier pour une
perception réduite des couleurs. Nouveau principe : **luminosité alternée**
(sombre/clair) le long de l'axe — c'est la luminosité qui survit au daltonisme,
deux voisins ne diffèrent plus jamais par la seule teinte. Teintes toujours
sourdes/patrimoniales (la lisibilité prime sur l'harmonie, sans flashy) :

| forme | hex | contraste /crème | mouvement |
|---|---|---|---|
| attribué à | `#9e2b12` | 6,82 | rouge assombri |
| nom (?) | `#cd7048` | 3,19 | corail éclairci |
| son atelier | `#b3821d` | 3,12 | ocre éclairci |
| son cercle | `#556327` | 5,98 | olive assombri |
| de son école | `#3e6f9e` | 4,82 | bleu plus franc |
| un suiveur | `#175c50` | 7,13 | teal assombri |
| sa manière | `#7b5fb5` | 4,62 | violet éclairci |
| dans son goût | `#742e4f` | 8,52 | prune assombri |

Paires problématiques, séparation mesurée (distance en vision deutéranope simulée,
avant → après) : rouge/corail 15,7 → 36,5 ; bleu/teal 6,2 → 20,8 ; violet/prune
13,4 → 30,2 (elles étaient identiques en luminosité, Δ 0,002 → 0,095) ; ocre/olive
21,1 → 38,5. **Limite assumée** (choix utilisateur) : bleu/teal reste la paire la
plus proche — aller plus loin sortirait du registre patrimonial ; le survol,
l'ordre de l'axe et les labels publics compensent. Validée sur simulation en
situation réelle (graphique Carracci = 7 formes sur 8, cartes, jauges) avant code.

**Jauges explicables au survol — la couleur n'est jamais le seul canal.** Chaque
segment de jauge est désormais survolable **et focusable au clavier** : infobulle
« header public / N œuvres · X % du doute » (labels de familles-public.js, accord
par `oeuvres()`, pourcentage français à une décimale), `aria-label` complet en
repli (« De son école : 240 œuvres, 77,4 % du doute autour de Charles Le Brun. »).
La jauge reste un résumé miniature du graphique (mêmes couleurs, même ordre, mêmes
labels) mais devient lisible en détail. **Zone de survol élargie** verticalement
(pseudo-élément invisible) pour atteindre les segments de ~2 px sans fausser les
proportions affichées.

**Infobulle partagée** : le tooltip HTML custom du graphique est extrait en
`Infobulle.svelte` (header / valeur / précision / mention type) — une seule
grammaire de tooltip dans l'application, consommée par le graphique (position
absolue dans son hôte) et par les jauges (**position fixe**, coordonnées fenêtre :
la liste défile, un panneau absolu serait rogné par l'overflow). Le `title` natif
a été écarté : invisible au focus clavier.

**Restructuration de la ligne de liste** (conséquence a11y) : la jauge sort du
`<button>` de sélection — un élément focusable ne peut pas vivre dans un bouton.
Le `<li>` porte désormais l'état (bordure, survol, sélection), le bouton ne couvre
que nom + compte, la jauge est sa sœur.

Vérifié par capture : jauges palette révisée ; survol du gros segment bleu de
Le Brun (« De son école — 240 œuvres · 77,4 % du doute ») ; **focus clavier** sur
le trait de 2 px « nom (?) » (outline + « 2 œuvres · 0,6 % du doute ») ; tooltip du
graphique intact via l'infobulle partagée ; cartes Œuvres. Build sans avertissement.

## 2026-07-11 — Jauges de la liste : des niveaux aux familles (décision utilisateur, après test)

**Le choix « option A » du palier couleur (même jour, ci-dessous) est écarté après
test.** La jauge à 3 niveaux devait être « une version résumée des 8 formes » ; en
situation réelle elle **contredisait le graphique** : chez Le Brun, la masse
dominante « de son école » (bleue sur le graphique) apparaissait ocre dans la jauge
(agrégée au niveau 2). La couleur de la forme dominante disparaissait de la liste.
Vérifié sur les données avant de trancher : les jauges consommaient bien `niveaux`
= [n1, n2, n3], cohérents avec les sommes de familles par niveau (aucun bug — un
choix de langue visuelle, pas de calcul).

**Nouvelle règle : la mini-jauge de chaque maître est un résumé direct du
graphique** — mêmes familles, mêmes couleurs (`var(--forme-*)`), même ordre que
l'axe, proportions réelles (`notices / doute`). `BarreFamilles.svelte` remplace
`BarreNiveaux` dans la liste :
- familles absentes non affichées ; un segment minuscule reste un simple trait,
  jamais de largeur minimum (les proportions priment) ;
- **filet séparateur de 1 px couleur du fond** entre segments (gap), pour détacher
  les voisins proches (rouge/corail, violet/prune) sans fausser les parts ;
- le chiffre à droite reste le total de doute ;
- aucune légende dans la liste (le graphique et ses tooltips portent le sens).

Aucune modification du pipeline ni du JSON (`familles` était déjà exporté).
`BarreNiveaux.svelte` conservé en archive (précédent GalaxieMaitre) et les tokens
`--niveau-1/2/3` gardés pour de futures vues sur l'échelle du doute.

Vérifié par capture : Le Brun (masse bleue « école », conforme au graphique),
Rembrandt (masse violette « manière »), Ingres (rouge « attribué à »),
Michel-Ange (⅓ rouge + ⅔ bleu), Rodin (tout rouge).

## 2026-07-11 — Grammaire couleur « boîte de pigments » (décision utilisateur, validée sur aperçu)

**Constat.** Points, cartes « Œuvres » et jauges tenaient dans une seule gamme
orange/brun (les couleurs de familles avaient été *dérivées* des niveaux) : formes
indistinguables, rendu générique, niveau 3 délavé sur crème. Deux sources de hex,
non alignées (tokens CSS pour les niveaux, JS pour les familles).

**Système retenu.** Une **couleur stable par forme de doute**, pensée comme une
**boîte de pigments de peinture ancienne** (diverse mais légitime sur le sujet, pas
« arc-en-ciel décoratif ») :

| forme | token | pigment | contraste /crème |
|---|---|---|---|
| attribué à | `--forme-attribue` `#b8431f` | terre de Sienne brûlée | 4,96 |
| nom (?) | `--forme-point-interrogation` `#c96a4e` | terre rose | 3,38 |
| son atelier | `--forme-atelier` `#a8781f` | ocre jaune | 3,56 |
| son cercle | `--forme-entourage` `#6f7d34` | terre verte | 4,11 |
| de son école | `--forme-ecole` `#3f6b8f` | bleu de smalt | 5,16 |
| un suiveur | `--forme-suiveur` `#2f7d70` | vert-de-gris | 4,46 |
| sa manière | `--forme-maniere` `#6f5691` | violet minéral | 5,60 |
| dans son goût | `--forme-genre` `#8a5168` | lie de vin | 5,54 |

Toutes ≥ 3:1 sur le fond crème (cible objet graphique, vérifié). **Température =
distance au maître** : rouges (niveau 1) → terreux basculant au froid (niveau 2) →
pourprés (niveau 3) — la couleur *renforce* la lecture de l'axe sans la porter seule.

**Jauges : option A** (choix utilisateur — pas de mini-répartition en 8 formes dans
la liste, qui la chargerait). Les 3 couleurs de niveaux sont les **pigments repères**
de chaque zone (`--niveau-1/2/3` = attribué / atelier / manière) : la jauge à
3 niveaux devient une version résumée des 8 formes, même langue. Le niveau 3 n'est
plus délavé (violet franc). Conséquence assumée : dans la liste, une forme apparaît
à la couleur de son *niveau*, pas de sa *forme* — l'identité par forme n'existe que
dans Graphique + Œuvres (le jour où on la voudrait dans la liste = option B).

**Copie « d'après » neutre** : `--couleur-copie` passe de `#4a6b7a` (bleu-gris, qui
collisionnait avec le nouveau bleu de smalt) à `#6b6f76` (gris), hors de la gamme
colorée du doute — une copie assumée n'est pas un doute.

**Centralisation.** Tous les hex de sujet vivent désormais **uniquement dans
`tokens.css`** (`--forme-*`, `--niveau-*`, `--couleur-copie`). `familles-public.js`
ne porte plus que des références `var(--forme-*)` ; le `STYLE_FAMILLE` en dur de
`NuageFamilles` avait déjà été retiré. Détail technique : le point du graphe passe
de l'attribut SVG `fill=` à la propriété CSS `style="fill: …"`, car `var()` ne
s'applique pas aux attributs de présentation SVG (seulement aux propriétés CSS).

Validé sur aperçu (planche de swatches + vraies vues Graphique / Œuvres / liste)
avant implémentation ; re-vérifié après centralisation. Les cartes ne portent la
couleur que par la pastille + le kicker (jamais tout le bloc).

## 2026-07-11 — « Les presque » : l'onglet « Détail » devient la vitrine « Œuvres » (décision utilisateur, validée avant code)

**Constat.** La vue « Détail » répétait le graphique (échelle du doute, table des
formules = les mêmes comptes que les points) avec des titres techniques, et ses
liens POP n'avaient pas de fonction éditoriale claire.

**Rôle redéfini.** Le graphique répond à « quelles formes prend le doute autour de
ce nom ? » ; l'onglet **« Œuvres »** répond à « quelles œuvres concrètes se trouvent
derrière ces formes ? ». On passe des points aux œuvres, des libellés publics aux
**mots réellement publiés**, du résumé au **cas vérifiable**. L'`extrait` du champ
auteur est la **seule citation littérale** de l'application (le tooltip du graphique
affiche une mention *reconstruite*) : c'est le moment « on lit ce que les musées
écrivent » du projet.

**Supprimé** : « L'échelle du doute » (barre des niveaux) et « Les formules
employées » (table) — redites du graphique. **Transformé** : les exemples passent
de bas de page à contenu principal.

**Forme retenue : vitrine en cartes**, pas une table.
- **Kicker dans la carte** (pas de titres de groupes) : header public de la forme
  (« Attribué à », « Son atelier »… — les mêmes mots que le tooltip du graphique)
  + **pastille de la couleur du point**. La couleur est sur la pastille, pas sur le
  texte (contraste des teintes claires). Cartes triées dans **l'ordre de l'axe X**.
- Titre de l'œuvre **tel que publié** (souvent en capitales : on ne réécrit pas,
  corps modéré pour que ça ne crie pas ; « Sans titre » en repli), musée + ville.
- **Verbatim en exergue**, entre guillemets, sans préfixe (l'amorce l'explique une
  fois : règle anti-répétition).
- Lien explicite « **Voir la fiche publique →** » par carte (le titre cliquable
  seul a une mauvaise affordance) ; **une seule** mention technique en bas :
  « Les liens ouvrent les fiches publiques sur POP, la plateforme ouverte du
  patrimoine. » Jamais « notice » ni « base de données ».
- Titre de section : « Quelques œuvres derrière les points ». Amorce (choix
  utilisateur) : « Quelques exemples issus des fiches Joconde, avec les mots
  publiés par les musées. » — la règle de sélection automatique est documentée en
  méthode, pas dans l'interface.
- **Copies « d'après » à part**, en fin : bloc distinct (couleur hors gamme du
  doute) « À part : {N} œuvres « d'après {maître} » — des copies assumées, pas des
  attributions incertaines. » + un exemple de copie lié, en petit corps, jamais en
  carte.

**Export enrichi d'abord, vitrine codée une fois** (plutôt qu'une V1 plate refaite
ensuite) : `build_artistes.py` émettait déjà un exemple par famille mais perdait le
code au moment du JSON. Ajouts : `code` de forme sur chaque exemple, **2 exemples
pour la forme dominante** (1 pour les autres, plafond 9), `exemple_copie` par
maître. Comptages inchangés (vérifié). **Le front ne re-parse jamais les
extraits** : le code de forme vient exclusivement de l'export.

**Couleur par famille centralisée** dans `familles-public.js` (`couleur` par
entrée) : source unique pour les points du graphique et les pastilles de la
vitrine (CLAUDE.md : une couleur par catégorie, stable partout). `STYLE_FAMILLE`
local à `NuageFamilles` supprimé.

Vérifié par capture : Le Brun (5 cartes, ordre de l'axe, copie avec exemple),
Rodin (cas minimal : 2 cartes d'une seule forme, rendu digne), largeur étroite
(une colonne). Build sans avertissement.

## 2026-07-11 — Nuage « Les presque » : point au plafond rogné, corrigé (marge de tête)

Le point de la famille dominante (au plafond commun, 240 = « école de » Le Brun)
était **rogné en tête** : sa bulle, de rayon maximal 16, était centrée sur `Y_HAUT`
= 10 et débordait au-dessus du bord haut du viewBox. Corrigé en réservant assez de
marge en tête pour le rayon max : `Y_HAUT` 10 → 24, `Y_HAUTEUR` 226 → 212. `Y_BASE`
reste à 236 : la ligne de base, l'échelle et l'axe X sont **inchangés** — seul le
haut du graphe gagne de l'air. Vérifié par capture (Le Brun) : la bulle à 240 est
entièrement visible, centrée sur sa graduation.

## 2026-07-11 — « Les presque » : bloc profil, chiffres en points d'appui (décision utilisateur)

3e itération du header (après « texte gauche / portrait droite » puis « nom pleine
largeur + portrait gauche / texte droite centré »). Constat : le portrait a un vrai
poids visuel, mais le paragraphe restait une petite masse au milieu d'un vide — trois
objets côte à côte, pas un bloc de profil.

Retenu (comparé par capture A vs B) :
- **Colonne de texte calée en HAUT** du portrait (`align-items: start`), pas centrée.
- **Colonne bornée** (`grid-template-columns: 12rem minmax(0, 24rem)`, `justify-content:
  start`) : elle répond au portrait au lieu de s'étaler comme une phrase de page.
- **Deux blocs empilés** (volume, puis dispersion) espacés (`.profil-texte`, flex,
  gap 1.1 rem) pour occuper la hauteur du portrait.
- **Chiffres en points d'appui** (variante B, préférée à la version tout-texte A) :
  le nombre en gros corps, couleur d'accent, sur sa propre ligne (`.chiffre`), sous
  lui l'attribution en texte courant. Donne à la colonne le poids qui manquait.

Réserves assumées : (1) de gros chiffres colorés flirtent avec l'infographie — toléré
ici car ce bloc est une **carte de profil**, pas une dataviz ; le chiffre est un
**repère**, la vraie mesure reste dans le graphe. (2) Le 2e bloc est reformulé en
« {N} musées où ces œuvres sont conservées » (retouche de texte validée à part).

Périmètre : CSS/layout + mise en forme du texte de `+page.svelte` uniquement. Données,
graphe et tooltips non touchés. Ancienne règle `.chapo-maitre` supprimée.

## 2026-07-11 — « Les presque » : portrait sorti du graphique, remonté au header de fiche (décision utilisateur)

Le portrait n'apparaissait que dans la vue « Graphique ». Incohérent : l'image
incarne le **profil du maître consulté**, elle appartient à la fiche entière, pas
à un onglet.

**Nouveau composant `PortraitMaitre.svelte`** — reprend le markup, le placeholder
silhouette, la logique de légende et les styles du portrait, jusqu'ici dans
`NuageFamilles.svelte`. Centralise le **format de légende normé** (sujet, auteur,
Wikimedia Commons, licence — rien d'autre, CLAUDE.md). Statut inchangé : **source
secondaire d'illustration**, jamais donnée ni comptage. Données et sourcing
(`portraits.json`) **non touchés**.

**Placement (2e disposition, même jour).** La 1re version (texte à gauche / portrait
à droite) déséquilibrait la fiche : portrait flottant seul en haut à droite, texte
isolé, graphe démarrant après un grand vide. Retenu : **bloc profil compact** —
nom en **pleine largeur**, puis portrait à **gauche** (largeur bornée 12 rem, légende
dessous) + paragraphe de situation à **droite**, centrés verticalement (`.profil`).
Les onglets Graphique / Détail restent **sous** ce bloc, le contenu d'onglet en
pleine largeur dessous. Le profil étant hors de la zone qui change d'onglet, le
portrait reste visible en Graphique **comme** en Détail, sans duplication ni **saut
de mise en page** au changement.

**Responsive par requête de conteneur** (`container-type: inline-size` sur `.fiche`)
plutôt que par largeur d'écran : sous ~32 rem de largeur de fiche, le profil passe
en **une seule colonne** (nom, puis portrait, puis texte, alignés à gauche — pas
deux colonnes écrasées). Le seuil porte sur la fiche réelle → le passage se fait
« plus tôt » quand l'aside comprime la colonne, et le texte garde toujours une
largeur confortable.

`NuageFamilles.svelte` allégé : prop `portrait` retirée, wrapper flex `.regard`
remplacé par `.graphe-hote` (simple repère du tooltip), le graphe **récupère toute
la largeur** libérée.

Vérifié par capture (Chromium piloté, outil de test retiré ensuite) : (1) Graphique
avec portrait au header, (2) Détail même portrait visible, (3) ratio différent
(photo de Rodin) contenu par la vignette à hauteur fixe, (4) largeur étroite =
portrait sous le texte. Observation hors périmètre : le point au plafond (240) est
rogné en tête de graphe (géométrie du nuage, `Y_HAUT` trop court pour le rayon max)
— à traiter séparément.

## 2026-07-10 — « Les presque » : onglet « Graphique » + paragraphe de situation générique (décision utilisateur)

**Onglet renommé.** « Nuage » ne décrit pas la visualisation et n'est pas un nom
de navigation clair → **« Graphique »**. Couple d'onglets : Graphique / Détail
(état interne `vue` passé de `'nuage'` à `'graphique'`).

**Paragraphe de situation réduit au volume et à la dispersion.** L'ancien texte
disait « ils écrivent qu'ils ne sont pas certains qu'il les ait peintes » : « ils »
flou, tournure lourde, « peintes » faux pour certaines familles. Une 1re réécriture
(même jour) avait tenté un gabarit avec fraction + mention dominante + explication ;
jugé **encore trop bavard**, il réintroduisait de l'interprétation. Décision finale :
ce paragraphe **ne porte plus aucun angle** — ni fraction, ni mention dominante, ni
« attribution prudente », ni override manuel. Le doute est déjà porté par le
graphique et les tooltips. Il sert seulement à situer volume et dispersion :

> Les musées de France conservent {total} œuvres sous le nom {de/d'}{maître}. Ces
> œuvres sont conservées dans {musées} musées.

Accord singulier/pluriel sur les deux quantités (`oeuvres`, `musees`). Conséquence :
`editorial-maitres.js` perd tout son mécanisme d'explication/override (famille
dominante, `situationMaitre`, `EDITORIAL[nom].explication`) — code mort supprimé,
il ne reste que `bioMaitre`. Le refactor `mention`/`montrerMention`/`deNom` de
`familles-public.js` **reste** (toujours utilisé par les tooltips).

**Correction de langue** (exigence CLAUDE.md) : helper `deNom` gère l'élision
(« sous le nom d'Ingres », « école d'Ingres ») ; helper `musees` accorde le
singulier/pluriel (« 1 musée » / « 64 musées »). Jamais de `` `${n} musées` ``
concaténé. `deNom` est aussi branché sur les mentions type (corrige un défaut latent
des tooltips : « entourage de Ingres »).

**Refactor tooltip** au passage : `FAMILLE_PUBLIC[code].mentionType` (nul/fonction)
remplacé par `mention` (toujours définie) + `montrerMention` (booléen). Le footer du
tooltip n'affiche la mention que si `montrerMention` (règle anti-répétition
inchangée : `point_interrogation`, `entourage_de`, `genre_de`). Source unique de la
chaîne, plus de duplication paragraphe/tooltip.

## 2026-07-10 — Nuage « Les presque » : grammaire de tooltip + tooltip HTML custom (décision utilisateur)

Le tooltip issu de la décision plus bas (`{label} — « {formule} » : {sens}. {N}
œuvres.`) répétait trois fois la même chose : le label, la formule exacte et le
sens disent presque les mêmes mots. Corrigé non pas au coup par coup mais par une
**vraie grammaire de tooltip**, validée après deux tours de proposition (table
relue et amendée par l'utilisateur avant tout code).

**Structure à hiérarchie visible** (modèle Datawrapper/Flourish), plus de phrase
linéaire :
- **header** — titre court, générique (jamais le nom du maître → stable d'une
  fiche à l'autre, donc comparable) ;
- **corps** — commence par le sens réel pour le lecteur, prudent ;
- **valeur** — « N œuvres », bien séparée ;
- **mention type** — niveau secondaire optionnel.

**Règle anti-répétition (gravée dans `familles-public.js`)** : la mention type ne
s'affiche QUE dans deux cas — soit la mention brute est elle-même le fait marquant
(`point_interrogation` → « Ingres (?) »), soit le terme réel du musée diffère du
libellé public (« entourage » ≠ « cercle », « genre » ≠ « goût »). Partout ailleurs
elle redirait le header → omise (`attribue`, `atelier_de`, `ecole_de`,
`suiveur_de`, `maniere_de`).

**« Mention type », pas « Formule Joconde »** : la chaîne est reconstruite par le
code (`` `entourage de ${nom}` ``), ce n'est pas un verbatim de la notice. Le
libellé public reste donc honnête sur ce point.

**Abandon du `<title>` SVG natif → tooltip HTML custom.** Le `<title>` n'est pas
stylable et impose une seule masse de texte : impossible d'y rendre la hiérarchie
header/corps/valeur/mention. Remplacé par un panneau HTML sobre (fond clair, pas de
pavé noir), positionné en pixels depuis la position réelle du point à l'écran
(le SVG a son propre repère viewBox), basculé sous le point quand il est trop haut.
Il ne vit qu'au survol/focus, ne masque donc pas durablement le graphe ni le
portrait. Accessible au **survol et au focus clavier** (`role="button"`,
`tabindex`), et **repli lecteur d'écran** conservé via un `aria-label` linéaire
(`resumeFamille`) sur chaque point, puisque le `<title>` disparaît.

Périmètre volontairement borné à ce palier : **ni les labels de l'axe ni la
micro-légende** n'ont été touchés.

**Grammaire allégée (même jour, 2e passe).** Le tooltip n'est pas un dictionnaire
des labels : si chacun réexplique tout, le lecteur relit huit fois la même notice.
Ordre retenu = **header → valeur → précision courte → footer optionnel**. Le corps
devient une **précision d'une seconde de lecture** (peut être vide si le header se
suffit), pas une définition. Objectif : lisible en un coup d'œil.

**Accord singulier/pluriel** : helper `oeuvres(n)` → « 1 œuvre », « 240 œuvres ».
Jamais de `` `${n} œuvres` `` concaténé directement. Le tooltip reçoit désormais le
nombre BRUT (accordé côté libellé), plus une chaîne pré-formatée.

Table des formulations validées (label axe inchangé) :

| Code | Header | Précision (corps) | Mention type |
|---|---|---|---|
| `attribue` | Attribué à | Sans certitude qu'il s'agisse bien de sa main. | — |
| `point_interrogation` | Nom suivi d'un « ? » | Doute noté sans autre précision. | « [nom] (?) » |
| `atelier_de` | Son atelier | Son atelier, pas forcément sa main. | — |
| `entourage_de` | Son cercle proche | Son entourage immédiat. | « entourage de [nom] » |
| `ecole_de` | De son école | Plutôt son école que sa main. | — |
| `suiveur_de` | Un suiveur | Dans sa suite, sous son influence. | — |
| `maniere_de` | À sa manière | Son style, auteur inconnu. | — |
| `genre_de` | Dans son goût | Lien de style lointain. | « dans le genre de [nom] » |

## 2026-07-10 — Nuage « Les presque » : couche de libellés publics + axe réordonné (décision utilisateur)

Suite du chantier narration. Les labels de l'axe exposaient les familles internes
(« attribué à », « ? », « école de », « atelier »…) : exactes pour nous, opaques
pour un visiteur. Le cas criant : « ? » seul, sans aucun sens. Décidé après deux
tours de proposition (aucune implémentation avant validation) :

**Couche de traduction publique** — nouveau `web/src/lib/familles-public.js` :
par famille, un `label` public court, la `formule` exacte du musée (avec le nom du
maître) et un `sens` en clair. Source unique des libellés, réutilisable par la vue
Détail plus tard. Le tooltip se compose : `{label} — « {formule} » : {sens}. {N}
œuvres.` — sans « niveau », « famille » ni « marqueur », la formule exacte
conservée entre guillemets, explication au pluriel/neutre et prudente (on rapporte
ce que font les musées, on n'affirme rien).

**Libellés retenus** (curseur fidélité ↔ lisibilité, la formule exacte restant au
survol) : attribué à · **nom (?)** · son atelier · son cercle · **de son école** ·
un suiveur · sa manière · **dans son goût**. Choix notables : « nom (?) » (fidèle à
la notation Joconde, lisible, ≠ « ? » seul) ; « de son école » (provenance, évite
de lire « école qu'il a fondée ») ; « dans son goût » (« son genre » sonnait faux).
« de son école » et « dans son goût » validés **provisoirement** (perfectibles).

**Axe réordonné par distance narrative** (option B) — ordre
`docs/typologie.md` : niveau 1, puis niveau 2 **atelier → entourage → école →
suiveur**, puis niveau 3. L'ancien ordre plaçait « école » avant « atelier » et
cassait une lecture gauche-droite. Réordonnancement **purement cosmétique** (ordre
des colonnes dans `NuageFamilles`), aucune donnée touchée, zones de couleur
toujours contiguës, comparabilité entre maîtres intacte.

**Micro-légende** (une ligne, statique, sous le graphe) :
« De gauche à droite, le lien au maître se desserre. » Elle remplace l'ancienne
bulle « Comment lire » (rejetée : saut de page + explication éparpillée). Honnête
seulement parce que l'axe est désormais ordonné.

**Règle gravée dans CLAUDE.md** (« Couche de libellé public obligatoire ») : aucune
catégorie technique affichée telle quelle ; un graphe se lit par ses labels,
légende et infobulles, jamais par une notice séparée. But : ne pas réinjecter les
structures du JSON dans l'interface à la prochaine brique.

Périmètre tenu : **nuage seul**. Non touchés (signalés) : l'accueil (« notices »,
« lexique »), la mention d'Alençon comme point d'entrée narratif dans CLAUDE.md
(la Phase 3 l'a pourtant écarté du centre), la vue Détail (refonte différée ; la
couche de traduction est prête à y être réutilisée).

## 2026-07-09 — Séparer les trois natures de texte + bannir le vocabulaire interne (décision utilisateur)

Refonte des textes de « Les presque », après constat que les fiches maîtres
étaient bavardes et répétitives. Le problème était **structurel, pas
stylistique** : le mode d'emploi de la visualisation avait envahi le texte
éditorial. Trois natures de texte cohabitaient au même niveau.

**Règle posée (désormais dans CLAUDE.md, « Principes de rédaction ») — trois
natures de texte, jamais mélangées :**
1. **Éditorial** — propre à un maître, court, en français courant, place centrale.
2. **Mode d'emploi** de la dataviz — identique partout, écrit **une seule fois**
   (ici : bulle dépliable « Comment lire ce graphique » à côté de la bascule),
   jamais répété par fiche.
3. **Mentions techniques** — crédits, licences, méthode : petit corps, en bas,
   format normé.

**Vocabulaire interne banni de l'interface publique.** *notice → œuvre* ;
*« formule de doute »* → phrase en clair (« les musées écrivent qu'ils ne sont
pas certains… ») ; *niveau 1/2/3* non affiché (l'info est déjà dans la couleur et
la position) ; *famille / marqueur / lexique* n'apparaissent jamais. Les
**libellés de familles** (« attribué à », « école de »…) restent inchangés pour
l'instant (reformulation narrative = chantier distinct), **sauf** le nom de code
« atelier (qualificatif, beaux-arts) » raccourci en « atelier de » à l'affichage.

**Une légende d'image n'est pas une note de méthode.** La mise en garde « ces
œuvres ne sont pas attribuées avec certitude au maître » a quitté la légende du
portrait (où elle n'avait rien à faire) pour rejoindre la bulle « Comment lire ».
La légende suit la forme normée : **sujet, auteur de l'image, source, licence**.

**Chiffres racontés en français** (« plus de la moitié » plutôt que « 59 % »),
le chiffre exact restant accessible (nombres bruts, survol, vue Détail).

**Mise en œuvre (front, aucune donnée touchée) :**
- `web/src/lib/editorial-maitres.js` (nouveau) : couche éditoriale du front (bio +
  angle par maître). **Ce ne sont pas des données Joconde** — Joconde reste la
  seule source de données. Deux maîtres témoins écrits à la main (François Clouet =
  doute proche « atelier » ; Rembrandt = doute lointain « à la manière de »),
  validés sur pièce. Les 25 autres ont un **angle dérivé** de leur famille de
  doute dominante (repli honnête, pas de fiche cassée) ; leur montée en qualité
  est une sous-étape (roadmap P3-T1).
- `web/src/lib/joconde.js` : helpers `fractionEnMots`, `libelleFamillePublic`,
  `licenceEnFrancais`.
- Les chiffres ne sont jamais stockés en dur : calculés dans le composant depuis
  `artistes.json`.

**Statut des portraits Wikimedia — renforcé.** Rappel (déjà consigné plus haut le
même jour) : **source secondaire d'illustration uniquement, jamais de donnée ni
de comptage**, même rang que le futur fond de carte. Joconde = seule source de
données. À redire dans la page méthode le moment venu.

**Défaut repéré ailleurs, hors périmètre de ce palier (à traiter ensuite) :**
la page d'accueil (`web/src/routes/+page.svelte`) emploie encore « notices » et
« Détection : {lexique} », et une notation d'analyste (« X % … Y % de la base »).
À reformuler **en gardant les deux dénominateurs** (règle de rigueur du
2026-07-03), sans les supprimer.

## 2026-07-09 — Portraits : retournement des regards + vignette de taille figée (décision utilisateur)

Deux ajustements du portrait de « Les presque », après examen du rendu.

**Retournement des portraits qui regardent à droite.** Le maître doit « regarder »
son nuage, placé à sa gauche. Les portraits dont le sujet regarde vers la droite
sont donc retournés horizontalement à l'affichage (`transform: scaleX(-1)`).
Constaté à l'œil sur les fichiers, **8 concernés** : Annibale Carracci, Boucher,
Guido Reni, Simon Vouet, Greuze, Hyacinthe Rigaud, Fragonard, Ribera. Les autres
regardent déjà à gauche ou sont frontaux. **Règle d'exclusion : jamais retourner
une gravure portant du texte** (Le Primatice, François Clouet, Le Corrège) — le
miroir inverserait le texte. L'info est portée par un champ `regard`
(`gauche`/`droite`) dans `portraits.json`, et mémorisée dans le set `REGARD_DROITE`
de `source_portraits.py` pour survivre à une régénération. Coût assumé : on affiche
un tableau connu en miroir — choix cosmétique au service de la mise en scène, pas
une altération de donnée (le portrait n'est qu'illustration).

**Vignette de taille figée.** Les portraits Commons ont des ratios variés ; sans
hauteur fixe, la colonne changeait de hauteur à chaque maître et faisait « sauter »
la page au changement d'auteur. Boîte de gabarit constant (`height: 15rem;
object-fit: contain; object-position: bottom`) : même empreinte pour tous, sans
rogner les visages (le `contain` préserve l'intégralité de l'image, au prix d'un
peu d'espace transparent autour — sans cadre, il est invisible).

## 2026-07-09 — Portraits des maîtres : Wikimedia Commons, source secondaire d'illustration (décision utilisateur)

Les portraits qui accompagnent le nuage de « Les presque » sont sourcés sur
**Wikimedia Commons**. Statut fixé, non négociable :

- **Source SECONDAIRE D'ILLUSTRATION uniquement — jamais de donnée ni de
  comptage.** Même statut que le GeoJSON de la carte (décision 2026-07-08). Un
  portrait ne pèse sur aucun chiffre du projet ; il donne seulement un visage à
  la visualisation. La source canonique reste la base Joconde.
- **Stockage LOCAL, pas de hotlink** : les images sont téléchargées dans
  `web/static/portraits/` (versions ~480 px, ~2,8 Mo au total pour 27), servies
  par le site statique. Aucune dépendance live à un service tiers.
- **Licence vérifiée fichier par fichier** via l'API Commons (`imageinfo` →
  `extmetadata`). Résultat : 26 portraits en **domaine public**, 1 en **CC0**
  (Géricault). Toutes libres.
- **Crédit exigé par la licence affiché** (auteur + licence + « Wikimedia
  Commons », avec lien vers la page du fichier) **en légende sous chaque
  portrait**. Le manifeste `static/data/portraits.json` conserve, par maître :
  fichier local, auteur, licence, URL de licence, URL source Commons, QID
  Wikidata.
- **Placeholder propre** (silhouette neutre + mention « pas de portrait fiable
  disponible ») prévu pour tout maître sans portrait fiable. À ce jour les 27
  ont un portrait ; le placeholder est le filet de sécurité.
- **Légende d'attribution obligatoire** sous chaque portrait :
  « Les œuvres du nuage ne sont **pas attribuées avec certitude** au maître
  représenté. » — garde-fou contre le contresens « voici les tableaux de X ».

**Procédé (reproductible)** : `web/scripts/source_portraits.py`. Route
Wikidata (propriété P18 « image », qui ne pointe que vers des fichiers Commons
libres) → API Commons pour licence + auteur + miniature → téléchargement local
→ génération du manifeste. Les 27 QID ont été vérifiés à la main (recherche +
description) avant récupération. Rejouer le script régénère images + manifeste
à l'identique.

## 2026-07-09 — « Les presque » : portrait du maître à droite, flottant sans cadre (décision utilisateur)

Ajustement de mise en scène du nuage (`web/src/lib/NuageFamilles.svelte`). Un
portrait du maître accompagne désormais le graphe pour donner de la présence à la
visualisation. Deux choix arrêtés après examen du rendu :
- **Portrait à droite du graphe** (et non à gauche) : le nuage étant placé à la
  gauche du portrait, le maître « regarde » ses propres formules de doute. La
  vraie image (libre de droit, à sourcer) devra donc être **orientée vers la
  gauche** pour que le regard tombe sur le nuage.
- **Image flottante, sans cadre** : retrait de la bordure, du fond blanc et du
  padding ; suppression du fond opaque de la silhouette. Le portrait se pose dans
  la marge du graphe (`align-items: flex-end`) plutôt que d'être enfermé dans une
  vignette — moins « fiche signalétique », plus incarné.

En l'état, le portrait reste un **placeholder** (silhouette neutre) : l'effet de
regard ne sera visible qu'avec la vraie image. Aucune donnée ni aucun comptage
touché — pure présentation.

## 2026-07-08 — « Les presque » : barres → nuage de points à grille fixe (décision utilisateur)

Les barres horizontales (livrées le jour même) corrigeaient la galaxie mais deux
défauts à l'usage : (1) **pas de comparabilité entre maîtres** — chaque maître
n'affiche que *ses* familles présentes, la grille change à chaque artiste, chaque
graphe est un îlot ; (2) **pas de repère de mesure stable** — barres normalisées à
la largeur du conteneur, donc une barre « pleine » d'un petit maître paraît aussi
grande que celle d'un gros. On ne lit pas les volumes réels.

**Décision : remplacer les barres par un nuage de points (scatter) sur une grille
FIXE et COMMUNE.** C'est la grille stable qui rend les maîtres comparables —
objectif éditorial central de la vue.
- **Axe X** : les familles de doute, **toujours toutes, même ordre** (ordre
  canonique du lexique v2). « Présumé » retiré : absent des 27 maîtres (colonne
  vide par construction) → **8 colonnes**.
- **Axe Y** : volume, de 0 à un **plafond commun = 240** (la plus grande valeur de
  famille sur les 27, « école de » Le Brun). **Calculé côté front** depuis
  `artistes.json` (max sur les 27), pas en dur, pas de dépendance pipeline.
- **1 point par famille** à la hauteur de son volume ; zéro = pas de point ;
  taille **légèrement** croissante avec le volume (appui, pas la mesure) ;
  couleur par famille, groupée par teinte de niveau + libellés de niveau au-dessus
  des groupes (la lecture « échelle du doute » survit) ; graduations
  60/120/180/240 ; **échelle linéaire** (honnêteté des volumes) ; survol = compte
  exact ; libellés d'axe raccourcis, technique complet au survol.

**Justification de la forme (position sur Y commun plutôt que taille de bulle) :**
l'œil compare précisément des **hauteurs sur une échelle commune**, mais **mal des
aires de cercles**. L'échelle Y fixe et partagée permet de voir d'un coup que le
doute autour de Le Brun (pic « école » à 240) est d'un autre ordre que celui
d'Andrea del Sarto (« école » à 57) — les deux se lisent sur la même règle. Le
grossissement léger ajoute une charge narrative (le volume « pèse ») sans remplacer
la mesure. Compromis lisibilité/récit adapté au data-journalisme.

**Coût assumé (signalé) :** les familles à faible volume et les petits maîtres
collent au plancher sous un plafond à 240 — c'est la vérité (le doute se concentre
sur « attribué à » + « école de ») ; contré par le cadrage (sous-titre disant le
plafond, graduations, survol, plancher de taille de point), pas en trichant sur
l'échelle. La galaxie reste archivée dans `lib/GalaxieMaitre.svelte`.

## 2026-07-08 — « Les presque » : galaxie abandonnée, barres + carte par maître (décision utilisateur)

Refonte de la 1re dataviz après examen de la v1 (galaxie + détail) et du document
`docs/dataviz-les-presque.md`.

**Galaxie abandonnée dans cette vue.** L'encodage retenu était « 1 bulle = 1
famille » (4-5 ronds par maître) : un schéma moléculaire, pas une constellation ;
l'œil compare mal des aires de disques ; la vue n'apportait rien qu'une barre ne
montre mieux. La « vraie constellation » (1 point = 1 œuvre) est **reportée en
réserve, sur une branche séparée** — hors périmètre de cette vue.

**Trois angles complémentaires par maître** (le quoi / le combien / le où) :
1. **Détail** (existant) — formules, exemples POP, copies à part. Conservé ;
   labels trop techniques à reformuler plus tard (non prioritaire).
2. **Barres horizontales** (remplace la galaxie) — une barre par famille, longueur
   ∝ notices. Montre « la forme du doute » propre à chaque maître. Aucune donnée
   nouvelle requise.
3. **Carte par maître** (nouveau) — voir ci-dessous.

**Pourquoi la carte devient possible ici alors qu'une carte globale était exclue.**
Une carte de tous les doutes (~18 000 points) était écartée : trop dense et
malhonnête (inviterait à comparer les musées sur des comptages bruts, interdit vu
les versements inégaux). Une carte **par maître** lève le piège : quelques dizaines
de points, et on ne compare plus les musées entre eux — on montre **où se disperse
le doute autour d'un seul nom**. Angle neuf : la géographie du doute d'un maître.

**Grain honnête retenu (constaté sur les données) :** une notice n'a pas de
coordonnées propres, elle est localisée par son **musée détenteur**
(`Code_Museofile` → coord dans `musees.json`, couverture 98,7 %). Donc **1 point =
1 musée**, taille ∝ nb d'œuvres douteuses de ce maître. Mesure de dispersion :
~1 doute/musée pour la plupart (doute très semé), seule concentration nette = Le
Primatice (Fontainebleau). Caveat page méthode : la taille reflète le nombre
d'œuvres douteuses **de ce maître** dans ce musée, jamais une comparaison de
catalogage entre musées.

**Dépendance données à traiter avant la carte :** le champ `musees` d'`artistes.json`
confond ferme/copie/doute (« Raphaël 108 musées » pour 28 doutes) — inexploitable.
Il faut enrichir `build_artistes.py` : par maître, la liste des **musées du doute
+ comptes**.

**Technique de carte : D3-geo auto-hébergé** (arbitrage utilisateur 2026-07-08).
GeoJSON France + départements en open data (licence ouverte, cité comme source
secondaire d'affichage, jamais de comptage), dans `static/`, rendu SVG dans Svelte,
**aucune tuile externe / aucun serveur**, pré-rendable. Écartés : Leaflet + tuiles
OSM (dépendance live à un service tiers, hors esprit « source unique », réactive le
réflexe de comparer les lieux) ; Leaflet sans tuiles (bancal, D3 fait mieux).

**Ordre de construction retenu : barres → (palier données) → carte** (arbitrage
utilisateur). Les barres d'abord car sans donnée nouvelle et retirent la galaxie
tout de suite ; la carte ensuite car elle porte la dépendance données + le nouvel
outil. Détail conservé en l'état.

## 2026-07-07 — Style du front : rejet du look générique (remarque utilisateur, indicative)

Socle P3-T0 validé sur le fond. **Remarque à titre indicatif, pas un arbitrage à
appliquer maintenant** : l'utilisateur ne veut pas de la présentation générique
que produit Claude par défaut (« toutes les applications créées par Claude ont la
même allure »). Ce n'est pas le sujet au stade actuel (on construit les dataviz),
mais c'est consigné pour plus tard.

Conséquence pratique : les tokens et la mise en page actuels
(`web/src/lib/styles/tokens.css`, coquille) sont **provisoires, fonctionnels**,
non une direction artistique. Quand le style deviendra le sujet (après les
dataviz), proposer une **identité visuelle affirmée et singulière**, pas les
réglages par défaut. Ne pas investir dans le polish visuel d'ici là.

## 2026-07-07 — Stack du front : SvelteKit retenu (décision utilisateur, phase 3)

Le choix de socle laissé en suspens à P3-T0 (SvelteKit recommandé vs vanilla +
Vite) est tranché : **SvelteKit**, en **build statique** (`adapter-static`,
`prerender`). Aucun serveur applicatif : le front reste un site statique qui
consomme les JSON déjà exportés dans `data/exports/web/` (règle non négociable
« jamais la base entière dans l'application »).

Pourquoi SvelteKit plutôt que du vanilla + Vite :
- **Le routage intégré sert directement la structure éditoriale.** Chaque brique
  (« Les presque », le décodeur de l'échelle, les révisions, la carte) et la page
  « méthode et limites » deviennent des routes de même rang — la règle « méthode
  au même rang que le reste » se lit dans l'arborescence du code.
- **Composants + coquille partagée** (en-tête, navigation entre briques, tokens
  de style des 3 niveaux) sans réinventer un système de gabarits à la main.
- **Cohabite bien avec D3.js** : Svelte gère le DOM et l'état, D3 les échelles et
  la géométrie ; pas de conflit de propriété du DOM si on laisse D3 calculer et
  Svelte rendre.
- **Reste lisible pour un développeur intermédiaire** (pièce de portfolio) : la
  syntaxe Svelte est proche du HTML/CSS/JS, moins de cérémonie que React.

Coût assumé : une chaîne de build Node à côté du pipeline Python (`uv`). Front
isolé dans un dossier dédié (voir roadmap P3-T0). Les JSON restent la seule
frontière entre le back Python et le front — aucun couplage au-delà.

## 2026-07-07 — Export « Les presque » : désambiguïsation → liste vedette à 27 (mise en œuvre)

Formalisation de l'entrée « par l'artiste » :
- `src/markers.py` : ajout d'une fonction publique `famille_segment(segment,
  en_beaux_arts)` — catégorise **un** segment du champ Auteur (copie > écarté >
  doute > propre) en réutilisant les motifs du lexique v2, sans diverger.
  35 tests toujours verts.
- `src/build_artistes.py` → `data/exports/web/artistes.json` (44 Ko) : par maître,
  `propre` / `doute` / `copie`, ventilation par famille **et** par niveau (échelle
  P2-T2), nombre de musées, et une notice réelle par famille (lien POP).

**Désambiguïsation des trois familles †** (annoncée « avant l'export »), faite
sur les nom-pivots réels :
- **Fragonard** : Jean-Honoré isolé = **31** doutes (son fils Alexandre-Évariste
  = 3) → conservé.
- **Cranach l'Ancien** (Lucas le Vieux + l'Ancien) = **17** → sous 20 (les 30
  incluaient le fils, Lucas le Jeune, 13) → **retiré**.
- **Bruegel l'Ancien** (Pieter I + le Vieux) ≈ **15** → sous 20 (les 51 étaient
  surtout **Jan** Brueghel, ~23, un autre homme) → **retiré**.

**Conséquence : la liste vedette publiée passe de 29 à 27 maîtres.** Ce n'est pas
une exception au critère mais le critère ≥ 20 appliqué au bon niveau (le maître
isolé, pas la famille). Réserve laissée à l'utilisateur, sans arbitrage par
défaut (on garde les 27) : réintégrer Bruegel/Cranach comme « famille » assumée,
ou échanger « Bruegel l'Ancien » contre **Jan Brueghel** (~23, qualifie seul).

## 2026-07-07 — Liste vedette V1 : 29 maîtres de référence (décision utilisateur, phase 3)

Première brique de l'entrée « par l'artiste » (« Les presque ») : une **sélection
vedette** de maîtres mis en avant sur la page, distincte du moteur de recherche
(qui, lui, porte sur tous les noms de la base).

**Critère unique retenu : maître de référence ET ≥ 20 notices de doute (hors copie).**
Le doute n'est pas exigé pour la notoriété, mais il l'est pour la mise en avant
vedette : sans ≥ 20 « presque », il n'y a pas de matière à montrer. La curation
de notoriété est assumée et publiable (panthéon lisible, primitifs → modernes) ;
le seuil de 20 la rend non arbitraire.

**Comment le doute est compté (la fabrique du chiffre).** Comptage **par segment**
du champ `Auteur` (séparateur `;`), rattaché au nom-pivot (parenthèses retirées,
casse/accents normalisés), avec les **regex réelles de `markers.py` v2** :
copie (« d'après ») l'emporte ; familles écartées (atelier-nom, école-lieu,
atelier hors beaux-arts) exclues ; sinon doute si une famille de doute matche ;
sinon propre. Deux corrections de repérage décisives par rapport aux sondes
initiales (parenthèses seules) :
- le doute est cherché dans **tout le segment**, parenthèses ou non — une sonde
  « entre parenthèses seulement » **sous-comptait** (ex. Ingres : « attribué à »
  souvent écrit hors parenthèses → 13 devient **204**) ;
- les **écoles nationales** « (école allemande/flamande) » ne comptent pas
  (nationalité, pas « école de X ») — la sonde initiale **sur-comptait**
  (ex. Dürer : 161 devient **19**).

**Les 29 maîtres retenus** (doute canonique) :
Le Brun 310 · Le Primatice 269 · Ingres 204 · Rembrandt 187 · Michel-Ange 172 ·
Rubens 121 · François Clouet 105 · Annibale Carracci 86 · Rodin 81 · Boucher 78 ·
Andrea del Sarto 63 · Guido Reni 60 · Léonard de Vinci 56 · Le Tintoret 53 ·
Poussin 52 · Simon Vouet 51 · Bruegel l'Ancien 51† · Greuze 49 · Van Dyck 46 ·
Le Corrège 46 · Pierre Mignard 43 · Véronèse 41 · Hyacinthe Rigaud 41 ·
Géricault 40 · Fragonard 37† · Cranach 30† · Raphaël 28 · Ribera 21 · Titien 20.

**Exclusions assumées — maîtres de référence sous le seuil** (le critère fait loi,
choix « A » de l'utilisateur) : Dürer 19, Delacroix 17, Watteau 17, Corot 16,
Jean Clouet 15, Holbein 15, Botticelli 15, Murillo 14, Courbet 11, Millet 11,
puis ≤ 9 (Fra Angelico, Van Eyck, Zurbarán, Mantegna, Giotto, Goya, Vélasquez,
Fouquet, Georges de La Tour, Chardin, Le Caravage, Houdon, Cézanne). **Les
modernes ne sont pas doutés** (Manet, Monet, Degas, Van Gogh, Picasso : 0) —
c'est un constat, pas un oubli.
- **Trois des 20 noms présumés au départ tombent sous le seuil** après correction
  du comptage : Dürer (19), Corot (16), **Jean Clouet (15)**. Ils sortent.
  Vérifié : le doute « Clouet » est porté par **François Clouet (105)**, pas par
  Jean (pas de réservoir « CLOUET sans prénom » qui le sauverait).

**Caveat à traiter avant l'export `artistes.json`** — † trois entrées agrègent
plusieurs personnes sous un même nom-pivot, à désambiguïser (prénom/génération) :
**Bruegel** (l'Ancien / le Jeune / Jan), **Cranach** (l'Ancien / le Jeune),
**Fragonard** (Jean-Honoré vs son fils Alexandre-Évariste, majoritaire en volume).
Repérage à affiner, non cassé. Un raté connu sans effet ici : « Le Greco »
(motif à corriger), de toute façon très sous le seuil.

Chiffres indicatifs, susceptibles de légers écarts quand l'export officiel sera
produit par le pipeline — mais la **méthode est déjà alignée sur `markers.py`**.

## 2026-07-06 — Direction de restitution (décision utilisateur, phase 3)

**Application interactive soutenue par les données, matérialisée par une
dataviz ou une série de dataviz.** Deux refus explicites :
- **pas de scrollytelling / récit défilant** (jugé bancal, nécessiterait des
  enquêtes ; éventuellement plus tard, pas maintenant) ;
- **Alençon n'est pas le fil rouge ni le point de départ** — seulement
  l'étincelle du projet, noté, non central. Ne plus le placer au centre.

Corrige l'orientation « récit guidé » de docs/phase3-options.md : la colonne
vertébrale n'est PAS narrative mais l'interaction avec les données elles-mêmes.
Reste à définir la ou les dataviz (en cours).

## 2026-07-05 — Ouverture du récit : Alençon en incarnation de la limite (décision utilisateur, P2-T4)

Le cas fondateur (Alençon) est absent de Joconde : le musée n'a versé que sa
dentelle (109 notices), pas ses beaux-arts — vérifié et confirmé par l'API du
ministère (docs/donnees.md). **Décision : en faire l'ouverture, assumée comme
telle** — « le cas qui a inspiré ce projet est lui-même invisible dans
l'inventaire national ». On l'illustre via la base régionale de Normandie
(citée comme source secondaire d'illustration, jamais de comptage — la source
canonique reste Joconde). Alençon devient la démonstration vivante de la limite
« les chiffres ne reflètent que ce qui a été versé ».

## 2026-07-05 — Traitement de la monoculture Barla/Nice (décision utilisateur, P2-T3)

Le muséum d'histoire naturelle de Nice (M7050) concentre 5 791 doutes, tous
« Barla (attribué à) » — 23,6 % du doute national, un artefact de catalogage.
**Décision : garder 24 507 comme chiffre vedette (rien n'est caché) ET
divulguer partout le « hors ce cas : 18 716 ».**
Mise en œuvre (src/build_exports.py, exception nommée, pas de seuil auto) :
- `niveaux.json` porte `monoculture_divulguee` + `doute_hors_monoculture` ;
- le musée concerné porte un drapeau `monoculture: true` dans `musees.json` ;
- **règle de restitution : la carte se fonde sur `part_doute`, jamais sur le
  doute brut** — aucun musée ne doit écraser les autres ;
- Barla sera un cas raconté en P2-T4 (le geste de catalogage en série).

## 2026-07-05 — Typologie du doute validée + règles de non-addition (décisions utilisateur)

**Règles de non-addition (P2-T1)** : le chiffre vedette reste le doute seul ;
66 420 publiable uniquement comme « au moins une mention » (union nommée) ;
les trois catégories ne se montrent ensemble qu'en diagramme à intersections ;
le croisement doute + révision (4 615) devient un objet éditorial à part.

**Typologie (P2-T2)** — échelle à 3 niveaux validée (« Presque lui »,
« Autour de lui », « Son style, sans lui », voir docs/typologie.md), avec
trois arbitrages :
1. **atelier restreint aux beaux-arts** (523 notices hors → écartées) ;
2. **écoles-lieux consacrées écartées** (liste versionnée : Fontainebleau,
   Paris, Barbizon, Pont-Aven, Nancy — 222 notices) ;
3. **« ? » au niveau 1** (identification fragile).
Lexique v2 en conséquence ; nouveau doute total : **24 507** (2,39 % / 2,91 %).
Tests étendus à 35 cas (dont restriction domaine).

## 2026-07-05 — Bilan T5bis : recommandation GO (proposition, à valider)

Mini-contrôle T4bis rendu (65/65 verdicts). Résultats des familles reformulées :
- **? : 0 faux sur 15** (16 % en v0) — corrigé ;
- **« Atelier de X » écarté : 15/15 confirmés** — l'exclusion ne jette aucun
  vrai doute, le choix précision-contre-exhaustivité est validé par les faits ;
- **école de : 2/15 (13 %)** — restes : « École de Fontainebleau » (aire
  artistique) et « Nouvelle École de Paris » (mouvement, champ Ecole_pays) ;
- **atelier : 6/20 (30 %)** — restes : des ateliers-entreprises portant le
  qualificatif « (atelier) » (VAUCANSON, JACQUEMIN Frères…). Signal net : les
  faux vivent en ethnologie/artisanat, les vrais en peinture/dessin.

Taux global pondéré (catégorie doute, calcul : src/evaluate_recheck.py) :
- **5,7 % conservateur** (< 10 %) ; 3,3 % ajusté (le faux « attribué,
  d'après » de T4 est prouvé exclu par les tests).

**Recommandation : GO.** Le seuil de phase est franchi. Les faiblesses
résiduelles sont localisées, chiffrées et publiables comme telles ; à traiter
en phase 2 dans la typologie plutôt que par une nouvelle itération de regex :
- la famille « atelier » (7 % du doute) sera marquée « fiabilité moindre,
  sensible au domaine » — option : la restreindre aux domaines beaux-arts ;
- « École de Fontainebleau / de Paris » : liste d'exclusion des écoles-lieux
  consacrées, à trancher en construisant la typologie ;
- taux par famille publiés avec le chiffre global (transparence).

## 2026-07-04 — Lexique v1 : lire la convention, pas le mot (cycle validé par l'utilisateur)

Principe directeur de la reformulation « atelier de » (validé explicitement) :
**le doute Joconde s'écrit en qualificatif entre parenthèses après un nom**
(« COROT (atelier) »), tandis que « Atelier de Pistillus » en nom d'auteur
désigne un créateur assumé. On lit la convention d'écriture des conservateurs,
plus le mot isolé. Choix assumé de **précision contre exhaustivité** : mieux
vaut sous-compter en le disant que sur-compter en silence.

Corrections v1 (détail en tête de `src/markers.py`) :
1. « atelier » : qualificatif seulement, détection segment par segment ;
   garde-fous : nom commençant par « atelier », rôles de production
   (graveur, imprimeur, photographe…). La forme « Atelier de X » en nom
   d'auteur part en catégorie « ecarte » (1 123 notices), chiffrée à part et
   soumise au mini-contrôle : on vérifie qu'on ne jette pas de vrais doutes.
2. « école de » : exclusion de la forme inversée « Hollande École de (École
   hollandaise) » ; qualificatif « (école) » en fin de token seulement.
3. « ? » : la parenthèse ne doit contenir aucun chiffre (« (?-1996) » exclu).
4. Doctrine « (attribué, d'après) » → copie, implémentée en exclusion.

Les verdicts humains de T4 sont figés en **tests automatiques**
(`tests/test_markers.py`, 25 cas) : toute future retouche du lexique doit
repasser devant eux. Recomptage v1 : doute = 25 220 notices (2,46 % base /
2,99 % avec auteur). Mini-contrôle T4bis : 65 lignes
(`data/exports/echantillon_recheck.csv`, graine 202607).

## 2026-07-04 — Bilan T5 : recommandation REFORMULATION (proposition, à valider)

Verdict chiffré (détail : `data/exports/bilan_faux_positifs.csv`, calcul :
`src/evaluate_sample.py`, taux pondérés par le poids réel des familles) :

| Catégorie | Faux positifs pondérés | Lecture |
|---|---|---|
| doute | **17,0 %** | tranche « reformulation » (seuils : <10 go, 10–25 reformulation, >25 no-go) |
| copie (« d'après ») | 0,0 % | impeccable |
| révision (Ancienne_attribution) | 0,0 % | impeccable |

Le 17 % n'est pas diffus : il est concentré dans des familles précises avec
des causes identifiées et corrigeables :
- **atelier de : 64 % de faux** (~3 600 notices) — trois causes : ateliers de
  production donnés comme auteurs assumés (`Atelier de Pistillus`), studios
  d'imprimeurs/photographes, mentions biographiques dans Précisions ;
- **école de : 20 %** — la forme inversée `Hollande École de (École
  hollandaise)` = école nationale, pas un doute (signal d'exclusion net :
  la parenthèse `(École …)` qui suit) ;
- **? : 16 %** — le `?` de date de naissance `(?-1996)` (la correction T3
  n'excluait que les chiffres AVANT le `?`) ;
- le reste tient très bien : attribué à 3,5 %, manière de 0 %, genre de 0 %.

**Recommandation : ni go ni no-go — reformulation ciblée.**
1. Lexique v1 : corriger les trois familles ci-dessus + intégrer la doctrine
   (`(attribué, d'après)` → copie ; mentions biographiques hors jeu) ;
2. recompter la base entière ;
3. mini-contrôle manuel (~60-80 lignes, familles reformulées uniquement) ;
4. si le doute pondéré passe sous 10 % → go définitif.
La matière, elle, est validée : abondante, structurée, et deux catégories
sur trois sortent sans aucune erreur.

## 2026-07-04 — Doctrine de vérification (décisions utilisateur, T4→T5)

Règle générale dégagée par la vérification manuelle des 206 lignes :
**un marqueur ne compte que s'il qualifie l'attribution de l'œuvre de la
notice** — pas s'il apparaît dans une biographie, dans un nom propre (atelier
de production, studio d'imprimeur), ou à propos d'une autre œuvre citée.

Deux points arbitrés explicitement :
- **Qualificatifs combinés `(attribué, d'après)` : « d'après » l'emporte** —
  la notice est une copie, elle sort de la catégorie doute.
- **`anonyme (attribué)` : cas documenté tel quel**, ni vrai ni faux positif
  (verdict « incertain », exclu du calcul des taux mais conservé et montré
  comme curiosité de la base).

## 2026-07-03 — Règle permanente : documenter tout ce qui touche à l'approche (décision utilisateur)

Toute modification ou implémentation concernant l'approche (détection,
échantillonnage, comptage, périmètre…) est documentée au moment où elle est
faite. Motif : l'approche devra être expliquée et justifiée publiquement, et
elle fait partie de la narration du projet — la fabrique du chiffre est une
partie de l'histoire. Règle inscrite dans CLAUDE.md.

## 2026-07-03 — Validation T3 : dénominateur vedette et périmètre (décisions utilisateur)

- **Le taux mis en avant est celui sur les notices avec auteur renseigné**
  (3,53 % au comptage v0) : c'est le doute mesuré là où un doute peut exister.
  **Le taux sur la base entière (2,90 %) est toujours donné en second**, jamais
  omis. C'est un choix d'écriture, pas de calcul : les deux chiffres restent
  publiés côte à côte.
- **Le comptage de référence porte sur toute la base** (la question centrale
  vise « les musées de France », pas un domaine). **Les beaux-arts
  (peinture/dessin/sculpture/estampe) sont l'angle éditorial** : ils
  concentrent ~80 % du doute détecté. Les deux lectures s'emboîtent, on ne
  choisit pas entre elles.
- Pour la phase 2 : **chiffrer les recouvrements entre les trois familles**
  (doute / d'après / ancienne attribution) — une même notice peut porter
  plusieurs marqueurs, il ne faut jamais publier des chiffres qui
  s'additionnent à tort. Tâche ajoutée à la roadmap.

## 2026-07-03 — Méthode de comptage (T3, décision utilisateur)

- **Tous les taux sont produits avec deux dénominateurs** : sur l'ensemble des
  notices ET sur les seules notices dont `Auteur` est non vide. Motif : ~18 % des
  notices n'ont pas d'auteur renseigné (archéologie, ethnologie…) ; un taux sur
  la base entière dilue le phénomène, un taux sur les notices « avec auteur »
  le mesure là où il peut exister. **Le choix du taux à mettre en avant sera
  fait avec l'utilisateur à la validation de T3.**
- Choix du périmètre (tout Joconde vs peinture/dessin/sculpture/estampe) reporté
  à la fin de T3, au vu de la ventilation réelle du doute par domaine (T2 validée).
- Rappel actif pour T3 : « école française » dans `Ecole_pays` = nationalité,
  pas un doute ; le marqueur est « école de [artiste] », plutôt dans `Auteur`.

## 2026-07-03 — Décisions d'initialisation (phase 0)

- **CSV complet = matière de référence de la phase 1.** C'est la source canonique
  citée dans la publication finale ; l'API du ministère n'est qu'un extrait
  (~30 % de notices en moins). L'API sert aux contre-vérifications ponctuelles.
- **pandas en lecture par morceaux** (`chunksize` + `usecols`) : on ne lit que
  ~15 colonnes sur ~70, mémoire maîtrisée, code lisible. Pas de base de données
  ni de framework à ce stade.
- **Détection par lexique de motifs regex versionné dans le code** (pas de NLP) :
  auditable et explicable — conforme à la posture « on lit ce qui est écrit ».
- **Environnement uv + pyproject.toml** (choix utilisateur).
- **Échantillon de vérification au format CSV tableur** (choix utilisateur) :
  colonnes `verdict` et `commentaire` à remplir, lien vers la notice POP.
- **`data/` non versionné** (1,1 Go) ; `src/download.py` permet de tout récupérer.

## Roadmap et points de validation

> **Section d'origine (phase 0), conservée comme trace.** Le suivi à jour vit
> dans `docs/roadmap.md` depuis le 2026-07-03. La forme pressentie ici pour la
> phase 3 (« carte D3.js + récit guidé ») a été remplacée par une application
> interactive SvelteKit portée par la dataviz (décisions des 2026-07-06 et
> 2026-07-07).

### Phase 0 — Initialisation ✅ (en attente de relecture)
Arborescence, CLAUDE.md, docs/, environnement uv, git.
⏸ Relecture de CLAUDE.md et des docs avant de toucher aux données.

### Phase 1 — Test go/no-go sur la qualité des données
- **T1** Nomenclature + téléchargement → mapping des champs documenté. ⏸
- **T2** Profilage du CSV complet → chiffres, choix du périmètre. ⏸
- **T3** Détecteur v0 → taux de base global et par domaine, ventilation par marqueur. ⏸
- **T4** Échantillon stratifié ~200 notices → CSV de vérification manuelle. ⏸
- **T5** Bilan des faux positifs → recommandation go / reformulation / no-go. ⏸
Seuils indicatifs discutés : < 10 % de faux positifs = go, 10–25 % = reformulation
du lexique, > 25 % = no-go.

### Phases suivantes (esquisse, dépendent du go/no-go)
- **Phase 2** — Typologie du doute (échelle inspirée du décret Marcus) et pipeline
  consolidé CSV → JSON légers agrégés (toujours avec le total versé par musée).
- **Phase 3** — Restitution web (carte D3.js + récit guidé pressenti, forme arrêtée
  après la phase 1), page « méthode et limites » publiée au même rang que le récit.
