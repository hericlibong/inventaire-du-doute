# Journal d'avancement

Notes au fil de l'eau. Une entrée par séance de travail, les plus récentes en haut.

## 2026-07-29 (suite) — Les premières reproductions entrent dans les fiches

On avait 184 reproductions ouvertes identifiées avec certitude. On les a intégrées. Chaque image
est téléchargée et ré-encodée localement (pas de lien direct vers Commons), montrée à la place du
placeholder, et cliquable vers sa page source où figurent licence et crédit — rappelés en petit
sous l'image. Sur les fiches de Corneille de Lyon, de Clouet, de Rembrandt, des visages
apparaissent enfin à côté des formules prudentes des musées.

Deux garde-fous tenus. D'abord les droits : on n'affiche que du domaine public ou du CC
BY/BY-SA, et on ne met en avant le nom de l'auteur du fichier que quand la licence l'exige — pas
question d'afficher un « auteur » là où toute la fiche dit justement que l'attribution est
incertaine. Ensuite la retenue : les œuvres sans reproduction réutilisable gardent leur
emplacement neutre, jamais une image de substitution.

Détail technique du jour : Wikimedia limite le rythme de rendu des miniatures (HTTP 429). Un
backoff a suffi, mais ça rappelle qu'on est l'invité d'un commun — on télécharge une fois, on
sert local.

## 2026-07-29 — Des reproductions ouvertes, mais pas sur POP

Deux temps dans la même journée. D'abord un audit : parmi les 3 668 œuvres prudentes, combien
ont sur POP une photo qu'on a le droit d'afficher ? On a lu, notice par notice, le seul champ
« Crédits photographiques ». Réponse nette et un peu brutale : **aucune**. La photographie de nos
maîtres est massivement de la RMN, « utilisation soumise à autorisation ». Le reste, ce sont des
crédits nominatifs sans licence. Zéro image ouverte. Le constat lui-même dit quelque chose du
sujet : même les reproductions, les musées se les réservent.

Ça ne veut pas dire qu'il n'existe aucune reproduction réutilisable ailleurs. On est donc allés
voir Wikimedia Commons, en passant par les données structurées de Wikidata. La clé, c'est la
propriété « identifiant Joconde » (P347) : quand un item Wikidata la porte, il désigne
explicitement notre notice — pas une œuvre qui lui ressemble. On a tenu ce principe tout du long :
une ressemblance de titre, d'auteur ou de musée ne prouve rien. Deux tableaux peuvent partager un
titre et un musée sans être le même objet.

Résultat : **329 correspondances certaines par identifiant Joconde, dont 184 avec une image
ouverte** (surtout du domaine public). C'est 184 reproductions de plus que ce que POP autorisait.
On a aussi cherché par numéro d'inventaire pour les œuvres absentes de ce premier filet : 152
candidats à vérifier à la main, sur 47 notices. Et surtout, on a appris à se méfier : un même
numéro d'inventaire se retrouve d'un musée à l'autre (« 516 », « sans numéro »…). Sans institution
concordante, c'est un faux ami — 352 rapprochements de ce genre ont été écartés.

Rien n'est encore téléchargé ni affiché. On a préparé le terrain : les correspondances, leurs
preuves, les licences, dans un CSV vérifiable à la main. La suite — quelles images entrent
vraiment dans l'onglet « Œuvres » — se décidera ensemble.

## 2026-07-28 — L'onglet « Œuvres » montre tout, plus quelques exemples

Jusqu'ici, derrière le graphique d'un maître, l'onglet « Œuvres » ne donnait qu'une poignée
d'exemples — une notice par mention, le premier venu dans la base. On voyait la forme du
doute sans pouvoir le parcourir. Désormais l'onglet ouvre la liste **complète** des œuvres
concernées : toutes celles que le pipeline a retenues, filtrables par mention et paginées.

Le principe qu'on s'est tenu : ne rien recompter. Les œuvres sortent des mêmes résultats que
le graphique et les jauges — une référence par maître, une mention par référence, les copies
« d'après » déjà à part. Un fichier par maître (`oeuvres/<slug>.json`), écrit dans la même
passe que l'export léger, avec des garde-fous qui refusent l'écriture si le compte ne tombe
pas juste : autant d'entrées que le chiffre affiché, la ventilation par mention identique,
aucune référence en double, aucune copie égarée. Ce qu'on lit dans l'onglet ne peut donc pas
contredire le point du graphe.

Côté interface, le fichier ne se charge qu'à l'ouverture de l'onglet, et seulement pour
l'artiste affiché — pas de préchargement de soixante-trois listes. Filtres en puces (avec
l'effectif de chaque mention), huit œuvres par page, une pagination qui se resserre quand les
pages sont nombreuses. On a soigné les états qu'on oublie d'habitude : le chargement, l'erreur
avec un « Réessayer », la liste vide. Et le clavier : mention active, page active, boutons de
bord désactivés — tout est dit autrement que par la couleur.

## 2026-07-27 — Le graphique et sa légende se répondent

Jusqu'ici, survoler un point éclairait sa mention dans la légende. Le sens inverse manquait :
on pouvait lire « de son école » dans la légende sans savoir quel point c'était. Désormais
survoler ou choisir une mention allume le point et ouvre son infobulle — les deux sens du
même dialogue.

Le piège, dans ce genre de fonctionnalité, c'est de finir avec deux machines à états qui se
contredisent — une pour le graphe, une pour la légende. On a tenu à n'en avoir qu'une seule.
Un objet dit tout : quelle mention, dans quel mode (un survol passager ou une sélection qui
reste), et d'où vient l'ordre. Le point et la mention lisent le même objet ; ils ne peuvent
pas diverger.

Deux façons d'activer, donc. Le survol et le focus posent une activation passagère, qui
s'efface dès qu'on s'en va. Le clic, le toucher, Entrée ou Espace posent une sélection qui
tient : elle survit au survol qui traverse, et ne se referme que si on la rappuie, si on en
choisit une autre, si on presse Échap ou si on touche ailleurs. On a soigné la chorégraphie
des événements — un clic déclenche focus, pointer et click à la suite — pour qu'aucune
séquence n'ouvre puis referme aussitôt.

L'infobulle s'ancre toujours au vrai point, même quand c'est la légende qu'on a touchée.
Sauf sur mobile : là, la légende est sous le graphe, et si le point a défilé hors de l'écran,
l'infobulle s'affiche à la place juste sous la mention, là où le doigt vient de se poser.

Côté accessibilité, les mentions présentes sont devenues de vrais boutons — clavier, focus
visible, `aria-pressed` pour dire « celle-ci est sélectionnée », et un nom lu à voix haute qui
donne le libellé, le nombre et le pourcentage. Les mentions qu'un artiste ne porte pas
restent affichées mais éteintes : grisées, non cliquables, sans curseur trompeur, avec un
« aucune œuvre concernée » que seul le lecteur d'écran entend. Et l'état allumé ne se voit
pas qu'à la couleur : une graisse, un soulignement, un filet. Les trois titres de territoires,
eux, ne réagissent à rien — ce ne sont pas des mentions.

## 2026-07-26 — Le profil arrête de se répéter

L'onglet Profil disait deux fois la même chose. Le bandeau annonçait « "De son école" est la
mention la plus fréquente », puis le graphique, juste dessous, le montrait. On a tranché net :
le bandeau dit **l'ampleur** (combien d'œuvres, dans combien de musées), le graphique dit la
**répartition**. Chacun sa question, plus de doublon.

Le graphique a perdu ses titres d'auteur (« son école efface sa main » et les soixante-deux
autres) pour un titre unique et stable, « Répartition des mentions ». Le nom de l'artiste est
déjà en gros au-dessus, inutile de le répéter. Sous le titre, une seule phrase, produite par
une règle mécanique qui vaut pour tout le monde : si une mention dépasse 60 %, on la cite
seule ; si deux se partagent l'essentiel, on cite les deux ; sinon on dit que rien ne
s'impose ; et en cas d'égalité parfaite, on nomme les mentions à égalité. Toujours la mention
exacte, jamais « lui est attribuée » là où le musée a seulement écrit « attribué à ». La
règle vit dans un petit fichier à part, testé isolément — huit cas, dont l'égalité réelle de
Paul Bril et une égalité à trois inventée pour blinder.

Le nuage de points a maigri, au sens propre. Les bulles grossissaient avec le pourcentage,
alors que la hauteur disait déjà ce pourcentage : deux fois la même information. Points de
taille fixe désormais ; seule la hauteur compte. Chez Paul Bril, les deux mentions à égalité
tombent exactement à la même ligne — on le voit d'un coup d'œil.

Les infobulles ont troqué leur dernière ligne interprétative contre une définition sèche et
identique partout : « Œuvre rattachée à l'école de l'artiste. » Une seule source dans le code
pour ces huit définitions. Et la petite phrase « De gauche à droite, le lien à la main du
maître se desserre » a disparu : les trois territoires et la légende se suffisent.

Enfin le vocabulaire s'est aligné : dans le profil, on ne compte plus des « notices » mais
des « œuvres concernées » — le bouton de tri, l'infobulle, tout. Le mot « notice » reste dans
les onglets Œuvres et Musées, qu'on n'a pas touchés ; c'est signalé pour plus tard. La page
Méthode explique le lien : l'unité réelle est la notice, on l'appelle « œuvre concernée »
pour alléger la lecture.

Livré en deux temps, comme demandé : un prototype sur quatre artistes d'abord — Zuccaro qui
penche fort d'un côté, Lorrain pareil, Bril à l'égalité, Titien dispersé — validé à l'œil,
puis étendu aux soixante-trois.

## 2026-07-22 (septies) — Dire le même homme sous ses deux noms

Deux choses ce matin, et la première vient d'une remarque juste : sur la fiche de
Michel-Ange, le titre dit « Michel-Ange » pendant que l'onglet d'à côté montre des notices
qui commencent par « BUONARROTI Michelangelo ». Rien ne relie les deux. Un lecteur peut
croire à un autre artiste — ou pire, prendre ce nom pour le titre d'une œuvre.

L'en-tête porte maintenant les deux : **Michel-Ange (Michelangelo Buonarroti)**, le second
plus petit, sur la même ligne. Les notices, elles, ne changent pas d'un caractère : c'est ce
que le musée a écrit, et c'est ce qu'on retrouvera sur POP. Le pont est éditorial, la donnée
reste intacte.

La demande portait sur Michel-Ange. Le piège est le même pour treize autres : Le Guerchin
qui s'appelle Barbieri, Jules Romain qui s'appelle Pippi, Le Parmesan qui s'appelle
Mazzuola, Le Pérugin qui s'appelle Vannucci, Claude Lorrain qui s'appelle Gellée, Botticelli
qui s'appelle Filipepi. Quatorze en tout. Corriger Michel-Ange seul aurait laissé le même
trou treize fois.

Ensuite, les trente-six en-têtes. Ils affichaient jusqu'ici la phrase passe-partout —
« Comment les musées rattachent ces œuvres à X ». Chacun a maintenant son angle. Et à les
écrire, on voit des choses qu'aucun tableau ne montrait : **Adolph Menzel**, dont les
quarante-sept œuvres concernées sont *toutes* dites « de son école », dans un seul musée —
une formule, un lieu. **Carlo Maratti**, dont l'atelier signe pour lui trente-sept fois sur
quarante-cinq. **Nicolas de Largillière**, éparpillé dans quinze musées sans qu'aucun n'en
garde plus de deux.

Tous ces sous-titres nomment leur mention par son code, jamais par son rang — la leçon de la
semaine, apprise en trouvant trois phrases qui disaient l'inverse de leurs chiffres. Ceux-là
ne pourront pas mentir au prochain lot.

Six formulations ont sauté à la relecture. Deux ne se comprenaient qu'avec leur titre : « 37
des 45 œuvres concernées **en sortent** » — de quoi ? Une disait « 15 seulement » juste après
avoir cité 10. Et une reprenait sans le savoir l'angle de Guido Reni.

## 2026-07-22 (sexies) — Trente-trois visages, et sept désaccords sur des dates

Plus de la moitié des fiches affichaient « Pas de portrait fiable disponible ». Trente-trois
des trente-six nouveaux maîtres ont maintenant leur portrait — soixante sur soixante-trois.

Le chemin est celui des vingt-sept premiers : Wikidata donne le fichier, Commons donne la
licence et l'auteur, l'image est téléchargée en local. Ce qui a changé, c'est qu'on ne
choisit plus l'identifiant à l'œil. Un petit script le cherche puis le contrôle : est-ce bien
un humain, a-t-il un portrait, et surtout — **les dates concordent-elles avec la ligne de
repérage déjà écrite** ?

Vingt-neuf fois sur trente-six, oui. Sept fois, non. Federico Zuccaro naît en 1543 selon
Joconde, en 1539 selon Wikidata. Polidoro Caldara en 1495 ou en 1499. Paul Bril en 1554 ou
1556. Rien de spectaculaire — quelques années — mais deux de mes lignes affichaient une date
**ferme** sur un point où les sources se contredisent. Elles portent maintenant « vers ».
C'est la doctrine du projet, écrite dans le fichier éditorial lui-même : la prudence sur les
dates est du même ordre que celle des musées sur les attributions. On ne tranche pas une
question de datation qui n'est pas la nôtre.

Trois maîtres restent sans visage : Gaspard Dughet, Domenico Campagnola, Laurent de La Hyre.
Wikidata n'a rien pour eux. Leur fiche continue de le dire, plutôt que d'afficher une image
approchante — c'est exactement la règle qu'on applique aux attributions.

Trois choses trouvées en chemin, toutes du même genre : ce qui n'est pas vérifié dérive.
Les vingt-sept images étaient dans git depuis juillet, mais **le fichier qui porte leurs
crédits ne l'était pas** — il vivait dans un dossier ignoré. Une licence perdue au premier
clone. Les crédits eux-mêmes parlaient anglais et se répétaient, Commons renvoyant « Unknown
artistUnknown artist ». Et la légende produisait « par attribué à Paul Bril ».

Enfin la page Méthode promettait que chaque portrait est « domaine public ». Sur soixante
images, six ne le sont pas : trois en CC0, trois sous une licence qui **oblige** à citer
l'auteur. La phrase le dit maintenant.

## 2026-07-22 (quinquies) — Temps 8 : dire au public ce qu'on a promis

Dernière étape. Elle consistait surtout à retirer un nombre des textes — « 27 » traînait
encore dans la charte, dans la spec de la dataviz, dans des tâches ouvertes. Un titre qui
fige un effectif devient faux au premier ajout, et c'est déjà arrivé deux fois : le titre
public dit maintenant « Explorer les N maîtres », le nombre venant des données.

Ce qui n'a **pas** été touché : les journaux datés. `donnees.md` écrit « Total des 27 :
2 341 segments → 2 225 références » — c'était vrai ce jour-là, et c'est le récit de la
fabrique du chiffre. Corriger après coup reviendrait à effacer l'erreur qu'on vient de
documenter.

Mais le vrai sujet du jour était ailleurs. Le 21 juillet, on avait décidé que « la liste des
candidats examinés est publiée avec leur nombre de notices, y compris ceux écartés et le
motif ». Le registre existait depuis le temps 5. **Le site n'en disait rien.** Un engagement
qui vit dans un fichier CSV que personne ne lit n'est pas un engagement tenu.

La page Méthode le dit maintenant, en français ordinaire : trois cent trente noms atteignent
le seuil, chacun porte un état, et — la phrase qui compte — *un nom encore à examiner n'est
pas un nom rejeté*. Soixante-quatorze formes d'écriture rattachées aux soixante-trois
artistes, vingt-deux écartées parce que ce ne sont pas des personnes, deux cent
trente-quatre à examiner. La liste s'agrandira par lots, et on le dit.

Deux manques comblés dans la foulée. Les **homonymes** n'étaient nulle part expliqués au
public, alors que c'est le piège le plus coûteux du projet : sous « Michel-Ange », les musées
ont aussi rangé Corneille Michel-Ange, peintre lyonnais. Et le fait qu'une œuvre puisse
concerner **deux artistes** — quand un musée hésite entre deux noms, la notice est sur les
deux fiches mais ne compte qu'une œuvre.

Une première version de ce paragraphe disait « puis examinés un par un » deux lignes avant
« 234 restent à examiner ». Deux phrases qui se contredisaient dans le même paragraphe.
C'est exactement ce que ce chantier apprend à voir.

## 2026-07-22 (quater) — Temps 7 : trois phrases qui disaient l'inverse des chiffres

Contrôle du front avec la liste élargie. Rien ne s'est cassé — et c'est bien le problème :
le site continuait à s'afficher, calmement, en racontant des choses fausses.

**Le plus grave d'abord.** Trois en-têtes de graphique écrits à la main annonçaient
l'inverse de leurs propres données. Le Primatice : « 125 œuvres portent la mention
“attribué à”, 71 celle “de son école” » — c'était exactement le contraire. Raphaël, pareil.
Michel-Ange annonçait « deux fois plus » pour un rapport devenu proche de trois.

La cause est instructive. Ces phrases recevaient des variables nommées `n` et `second` :
des **rangs**, pas des mentions. Tant que le classement ne bougeait pas, écrire « n œuvres
portent la mention “attribué à” » disait vrai. Le jour où l'école est passée devant chez ces
deux artistes, la phrase a continué de tourner sans rien signaler. Vingt et un sous-titres
étaient bâtis ainsi. Tous sont convertis : quand une phrase nomme une mention, elle va la
chercher par son nom, jamais par sa place au classement.

**Ensuite, un graphique devenu illisible.** Le nuage des mentions portait le nombre d'œuvres
sur une échelle commune plafonnée à 240. Avec vingt-sept maîtres allant de 20 à 310 notices,
cela passait. Avec soixante-trois qui commencent à onze, la moitié des profils s'écrasent au
sol : Botticelli montrait quatre points collés sur la ligne du zéro, alors qu'il a bien
douze œuvres dites « de son école » sur dix-sept. Un graphique où l'on ne lit plus de
hiérarchie est un mauvais graphique — la charte le dit elle-même.

L'axe porte maintenant la **part** des œuvres du maître, de zéro à cent pour cent. L'échelle
reste commune et fixe pour les soixante-trois — la comparaison est sauve, elle porte
désormais sur la forme du profil. Le volume, lui, n'a pas disparu : il est écrit dans la
phrase d'en-tête, il classe le répertoire, il s'affiche au survol de chaque point. Botticelli
montre enfin ce qu'il a à montrer : son école à 71 %.

**Trente-six artistes sans présentation.** Un visiteur tombait sur « Perino del Vaga » sans
une ligne pour le situer. Les trente-six lignes sont écrites. Les dates viennent d'abord de
la base elle-même — Joconde écrit souvent les années entre parenthèses, et il suffit de les
compter : « Bouchardon Edme (1698-1762) » revient dans 1 128 notices concordantes. Puis on
croise avec les notices d'autorité. Le « vers » est posé partout où la base hésite : Barocci
donne 1535, 1540 et 1528 ; Campagnola 1484 et 1500 à égalité. Adolph Menzel est le seul dont
la base ne dit rien.

Le reste tient du ménage, mais du ménage qui ment quand on ne le fait pas : la page Méthode
promettait encore « au moins vingt notices » quand le seuil est à dix ; le nombre en toutes
lettres venait d'une table qui s'arrêtait à trente et rendait « 63 » en chiffres ; et le
panneau de « Comprendre les mentions » annonçait « 3 674 notices » là où 3 674 sont des
appartenances — il compte maintenant les 3 668 œuvres réelles, comme le panneau national
d'en face.

Restent dehors, et c'est assumé : le style, les portraits des trente-six, et leurs angles
écrits à la main. Ils gardent l'en-tête généré, qui est juste mais anonyme.

## 2026-07-22 (ter) — Six notices où le musée hésite entre deux noms

Vérification demandée avant d'ouvrir le temps 7 : le total de la liste était une **somme de
fiches**. Or une notice peut nommer deux maîtres retenus, et elle est alors comptée deux
fois. Mesure faite sur toute la base.

L'écart est petit — 3 674 liens pour 3 668 œuvres — mais il existe, et ce qu'il désigne est
intéressant. Six notices portent deux maîtres. Sur ces six, **cinq portent le point
d'interrogation pour les deux noms** : Michel-Ange ou Andrea del Sarto ; Annibale ou Ludovico
Carracci ; Francesco Vanni ou Ludovico Carracci ; Luca Giordano ou Pier Francesco Mola. Ce
sont les notices où le musée ne dit pas seulement « ce n'est peut-être pas lui », mais « ce
pourrait être l'un ou l'autre ». La forme de doute la plus franche de toute la base. Elles
sont publiées en clair dans l'export, plutôt que gommées.

Sur les attributions certaines, le recouvrement est bien plus large : **300 notices** citent
deux maîtres retenus comme auteurs fermes — œuvres à plusieurs mains, ou notices à plusieurs
auteurs.

La règle qui en découle est simple à dire : une somme de fiches n'est pas un nombre
d'œuvres. L'export publie maintenant les deux, sous deux noms distincts, et « hors liste » se
calcule sur les œuvres — 24 507 moins 3 668, soit 20 839. Six de plus qu'avant. Les familles
et les niveaux ne s'additionnent pas davantage : une notice partagée entre Rubens (« atelier »)
et Van Dyck (« ? ») compte dans deux familles et deux niveaux.

**Et une conclusion à retirer.** J'avais écrit qu'un musée doutant d'un grand nom dit « plus
souvent “école de” que “attribué à” ». Les chiffres disent l'inverse : 43 % contre 35 %. La
formulation juste est plus modeste et tout aussi parlante — « attribué à » reste la formule
la plus fréquente chez les maîtres retenus, mais « école de » y prend une place quatre fois
et demie plus grande que dans le reste de Joconde, 35 % contre 7,6 %. Un déplacement de
proportion, pas un renversement.

## 2026-07-22 (bis) — Temps 6 : les fichiers publiés bougent enfin

Depuis l'audit, tout avait été mesuré sans rien publier : à chaque contrôle, l'export était
restauré à sa version d'avant. C'est terminé. `artistes.json` contient 63 maîtres,
`vue_ensemble.json` en a été redérivé.

Le chiffre qui compte : les maîtres retenus réunissent **3 674 notices prudentes sur les
24 507** de la base, soit **15 %** du doute écrit dans les musées de France. Avec 27 noms,
c'était 9,6 %. On voit désormais un septième du phénomène au lieu d'un dixième.

Et le constat qui fait tenir la section « Vue d'ensemble » est confirmé, pas seulement
maintenu : dans l'ensemble de Joconde, « attribué à » écrase tout — 73 % des mentions
prudentes. Chez les maîtres retenus, il tombe à 43 %, tandis que « école de » monte à 35 %
alors qu'il ne fait que 7,6 % au national. **« Attribué à » reste la formulation la plus
fréquente chez les maîtres retenus** ; ce qui change, c'est la place que « école de » y
prend — quatre fois et demie sa part nationale. Ce n'est pas un renversement de hiérarchie,
c'est un déplacement de proportion.

*(Rédaction initiale fautive, corrigée le 2026-07-22 : elle affirmait qu'un musée doutant
d'un grand nom dit « plus souvent “école de” que “attribué à” ». Les chiffres disent
l'inverse — 43 % contre 35 %. Une conclusion qui contredit ses propres chiffres est le seul
type d'erreur que ce projet ne peut pas se permettre.)*

Deux choses corrigées en route.

Les clés du fichier s'appelaient `dans_27` et `hors_27`. Elles auraient menti dès cette
régénération. Elles s'appellent maintenant `dans_liste` et `hors_liste`, et le JSON généré
ne contient plus une seule fois le nombre 27 — y compris dans les phrases embarquées qui
décrivaient la méthode. Un nom de champ qui fige un effectif devient faux au premier ajout.

Et une erreur à moi, trouvée en relisant : j'avais écrit hier que « David Téniers est
prudemment attribué dans 57 musées ». Non. Il **apparaît** dans 57 musées ; le doute n'est
écrit que dans **24**. Les deux mesures sont désormais publiées côte à côte, et la
documentation est corrigée. C'est précisément le genre de glissement que ce chantier existe
pour corriger — il ne fallait pas l'introduire en le réparant.

Un point à surveiller : le fichier double, 189 à 372 Ko, et c'est le navigateur qui le
charge. Un lot de maîtres de plus et il faudra séparer le détail du répertoire d'entrée.

Le front compile. Ce qu'il **montre** n'a pas encore été regardé : c'est le temps 7.

## 2026-07-22 — Temps 5 : ce qu'on ne sait pas encore n'est pas un refus

La proposition de départ disait : instruire une trentaine de candidats, et publier les
autres comme « écartés faute d'instruction ». Reformulation refusée, à juste titre. Ils ne
sont pas écartés par les données — ils sont **encore à instruire**. Écrire l'inverse aurait
réintroduit exactement ce qu'on venait de corriger : une sélection arbitraire, déguisée en
résultat.

La règle est donc : registre exhaustif, publication progressive. Les 330 formes restent
toutes au fichier, chacune avec un état — retenue, écartée pour une raison précise, ambiguë,
ou à instruire. Seules les personnes vérifiées entrent dans l'application. Les autres
attendent un prochain lot, sans qu'on préjuge de rien.

Première chose à faire : cesser de compter des graphies. Le Guerchin apparaît sous
« Barbieri Giovanni Francesco », sous « Guercino », sous « Le Guerchin » ; réunis, ce ne sont
pas 93 notices prudentes mais **101**. Salvator Rosa passe de 38 à 50, Carlo Maratti de 37 à
45, Botticelli de 15 à 17. Le seuil de dix doit se mesurer sur un homme, pas sur une façon
de l'écrire.

Ensuite, séparer les familles. Federico Zuccaro n'est pas son frère Taddeo. Philippe de
Champaigne n'est pas son neveu Jean-Baptiste. Louis Léopold Boilly n'est pas son fils Jules,
lithographe. David Téniers le Jeune n'est ni son père ni son frère Abraham. Chacun de ces
parents a été écarté nommément — et tous sont sous le seuil de leur côté, donc on ne perd
personne au passage.

**Trente-six maîtres instruits, soixante-trois retenus en tout, 3 674 notices prudentes.**
Le plus bas est le Titien, à onze. Deux profils sortent du lot : Adolph Menzel porte plus de
mentions prudentes que d'attributions certaines (47 contre 12), Corneille de Lyon presque
trois fois plus (29 contre 11). Chez eux, l'incertitude est la situation ordinaire.

Sur le registre exhaustif : 74 formes retenues, **22 écartées**, 234 à instruire. Les écarts
sont vérifiés un par un — manufactures de Creil, de Sèvres, de Delft, imprimerie de
Wissembourg, faïencerie de Sarreguemines, « Carracci l'un des », « anonyme ». Et trois
mentions qui ne portent **aucun nom** : le champ auteur contient seulement « Attribué à ».
Trente notices où un musée a écrit sa prudence sans dire de qui il doutait.

Un détecteur a été corrigé en route : il écartait « Mellet Jules Fils » et « Lacour Pierre
Fils » sur le mot « fils », alors que « Mellet Jacques Père » restait à instruire. Le mot
désigne une personne d'une dynastie, pas un atelier. Ces noms repassent à instruire.

Enfin, « DAVID (1748-1825) » — vingt-six notices prudentes dans dix-sept musées. C'est
presque certainement Jacques-Louis David. Il reste **à instruire** : le nom-pivot n'est qu'un
patronyme et la vérification n'a pas été faite. C'est le premier candidat du prochain lot.

Les tests ont fait leur travail : deux références réelles ont changé de verdict, `M0350002026`
et `50350011790`, qui revenaient à Gaspard Dughet et à Jules Romain, désormais retenus à leur
nom. Rien n'a été régénéré : la liste doit être validée avant que le front bouge.

## 2026-07-21 (octies) — Temps 4 : à qui d'autre les musées ont-ils dit « peut-être » ?

La liste des 27 avait été composée à la main. Personne n'avait demandé à la base qui d'autre
portait autant de mentions prudentes. C'est fait : `candidats_maitres.py` compte toutes les
formes d'auteur, et publie celles qui atteignent dix notices.

**4 834 noms** portent au moins une mention prudente dans les musées de France. **330**
atteignent dix. Trente-quatre sont déjà dans la liste ; **296 n'y sont pas**.

Le fichier est trié, et il se lit tout seul si l'on regarde une colonne : le nombre de
musées. D'un côté, 139 noms n'existent que dans **un seul** musée — Jean-Baptiste Barla et
ses 5 791 planches d'histoire naturelle à Nice, l'imprimerie de Wissembourg, les frères
Duthoit à Amiens : des fonds locaux, versés en bloc. De l'autre, 157 noms circulent entre
plusieurs musées, et ce sont presque tous des maîtres : Le Guerchin dans six musées,
Téniers dans vingt-deux, Giordano dans dix-neuf, Bouchardon, Jules Romain, Ludovico
Carracci, François Gérard, Champaigne, Dürer, Delacroix, Botticelli, Murillo, Donatello.

Tentant d'en faire une règle. Mais elle serait fausse : Le Parmesan (63 notices), Perino del
Vaga (53), Menzel (47), Bandinelli (45) ne sont chacun que dans un musée — et dans la liste
actuelle, Michel-Ange n'est que dans trois, Léonard dans deux. La dispersion dit par où
commencer à lire, pas qui garder.

Deux choses vues au passage. Le seuil ne peut pas s'appliquer à une graphie : le Titien
porte onze notices prudentes, mais dix sous « Le Titien » et neuf sous « Vecellio Tiziano ».
Compté par graphie, il sortirait de sa propre liste. Et « Rigau y Ros Hyacinthe », la forme
catalane du nom de Rigaud, apparaissait avec vingt notices sans être reconnue — elle
accompagne « Rigaud » sur la même notice 132 fois sur 134, l'alias ne rattrape que deux
œuvres, mais il est ajouté : une table doit dire les noms qu'elle connaît.

Reste ce que le seuil ramasse et qu'il faudra écarter à la main : des manufactures, des
faïenceries, « anonyme », « Carracci l'un des », et de purs accidents de saisie — un nom
réduit à la lettre « A », trente notices dans six musées.

## 2026-07-21 (septies) — Temps 3 : figer ce qui vient d'être corrigé

Un correctif qu'aucun test ne protège se défait tout seul à la modification suivante. D'où
cette étape avant le point d'arrêt : 89 tests, qui portent le projet de 60 à 149.

Il a fallu commencer par dégager la règle. Elle était enfermée dans la boucle de lecture du
CSV, donc intestable sans le fichier de 1,1 Go. Elle vit maintenant dans une fonction à
part, `resout_reference()` : on lui donne un champ `Auteur`, elle répond ce que la notice
dit de chaque maître. Les chiffres du pipeline sont identiques avant et après.

Les tests disent trois choses. Que Corneille Michel-Ange n'est pas Buonarroti, que Domenico
Robusti n'est pas son père, que Carlo Caliari n'est pas Véronèse — la liste complète des
homonymes de l'audit, chacun face au maître qu'il imitait. Qu'une notice nommant le Titien
deux fois ne compte qu'une œuvre. Et que l'ancre ne doit **pas** s'appliquer partout :
« ÉCOLE DE PRIMATICCIO », 121 notices, n'a pas le nom en tête et doit rester prise.

Le troisième niveau est le plus utile pour la suite : `data/exports/temoins_maitres.csv`,
42 lignes réelles de la base, avec le champ `Auteur` **tel que le musée l'a saisi** et le
verdict attendu en face. Ça se relit sans lire de code.

En l'écrivant, une notice du musée Ingres de Montauban est apparue : `IIngres
Jean-Auguste-Dominique`, avec deux I. Aucun motif ne peut la rattacher. On ne cherchera pas à
rattraper les fautes de frappe une par une — ce serait réécrire la base. C'est une limite
ordinaire du procédé, à dire dans la page méthode.

**Les étapes 1 à 3 sont faites. On est au point d'arrêt** : rien ne repart avant validation.

## 2026-07-21 (sexies) — Temps 2 : savoir de qui on parle

Avant d'écrire quoi que ce soit, on a demandé à la base ce qu'elle contenait vraiment : la
liste des **246 formes d'auteur** que les motifs actuels ramassent, prudentes et certaines,
avec leurs comptes. Puis on les a lues une par une. C'est en les lisant qu'on voit le
problème en face : sous « Michel-Ange », le Louvre et treize autres musées ont surtout
rangé **Corneille Michel-Ange**, un peintre lyonnais du XVIIe, 422 œuvres à lui seul.

La solution tient en un signe. En Joconde, l'auteur s'écrit « NOM Prénom » : le nom vient en
tête. Un motif marqué `^` ne vaut donc qu'en tête, et Corneille Michel-Ange, Anton Raphael
Mengs, Gaspard Poussin ou Madame Ingres sortent d'eux-mêmes — sans qu'on ait à les nommer.
Là où l'homonyme porte quand même le nom en tête (Domenico Robusti, le fils du Tintoret ;
Carlo Caliari, le fils de Véronèse ; Pierre Mignard II, le neveu), il a fallu l'écarter
nommément. Cette liste-là est faite pour être publiée : elle rend la sélection vérifiable.

Deux choses trouvées en chemin. Une exclusion posée sur Raphaël en juillet, **jamais
documentée**, qui écartait les « ateliers » — l'ancre fait le travail plus proprement.
Et surtout un oubli : **« SANTI Raffaello », le nom d'état civil de Raphaël**, n'était capté
par aucun motif. On cherchait « Raphael » et « Sanzio », pas « Santi ». Trois notices
prudentes de plus. C'est aussi ce qui explique qu'on arrive à 2 188 là où l'audit annonçait
2 185.

Le chiffre du doute descend de 2 341 à 2 188. Mais le vrai mouvement est ailleurs : les
attributions certaines tombent de 29 995 à 28 240, et **c'est la part affichée sous chaque
fiche qui bascule**. Michel-Ange passait pour un maître à 19 % de notices prudentes ; il est
à **39 %**. Le Tintoret passe de 27 % à 48 %, Véronèse de 15 % à 27 %. Michel-Ange n'est plus
présent dans 9 musées mais dans **3** : le Louvre, Rennes, Dole. Les six autres ne
détenaient que des homonymes.

Ces phrases-là devront être relues, pas seulement recalculées. C'est noté pour le temps 7.
Les exports restent gelés. Suite : temps 3, les tests sur références réelles.

## 2026-07-21 (quinquies) — Temps 1 : on compte des œuvres, plus des mentions

Reprise après le plantage de la machine : l'audit était bien commité (`0a566f7`), rien de
perdu. Première étape du chantier appliquée, dans `build_artistes.py` uniquement.

Avant de coder, une question à lever : la référence Joconde est-elle une vraie clé ? Scan
complet du CSV — 1 023 705 lignes, autant de références distinctes, **aucun doublon**. La
déduplication se fait donc ligne par ligne, sans rien garder en mémoire. La boucle collecte
ce que la notice dit du maître, puis compte une seule fois.

Deux règles de résolution ont dû être posées. Quand une notice porte plusieurs liens avec le
même maître, **le plus prudent l'emporte** — le doute avant la copie, la copie avant
l'attribution ferme : c'est ce qui rend les trois catégories disjointes. Et quand elle porte
deux formulations prudentes (les trois Vouet), **le « ? » l'emporte** sur « atelier »
(arbitrage utilisateur). Ce second choix a une conséquence qui dépasse les trois cas : une
notice ne relève que d'une famille, donc les familles et les trois niveaux totalisent
exactement le doute. Les jauges du front restent justes sans qu'on y touche.

Chiffres conformes à l'audit : doute des 27 **2 341 → 2 225**. Le Primatice perd 72 notices,
Le Corrège 21, Titien 8 — tous des maîtres nommés sous deux graphies. Le dénominateur
bouge autant : 29 995 → 29 229 attributions fermes, Titien passant de 211 à 104. Les
invariants tiennent sur les 27 fiches ; les 60 tests passent.

**Les exports ne sont pas régénérés.** Le plan les place au temps 6, après le point d'arrêt :
publier maintenant donnerait des chiffres corrigés sur l'unité mais toujours faux sur
l'identité. `artistes.json` est resté à sa version d'avant. Suite : temps 2, la table
déclarative d'alias et d'exclusions.

## 2026-07-21 (quater) — Audit de fiabilité : le chiffre des maîtres est faux

Trois notices rattachées à Michel-Ange — dont un Caravage et un Cerquozzi — ont déclenché un
audit complet du pipeline des maîtres. Scan exhaustif du CSV, reproduit indépendamment.
**Les constats sont confirmés, et le défaut est plus large qu'annoncé.**

Deux défauts distincts, longtemps confondus. **L'unité de comptage** : on agrège des
segments du champ `Auteur` alors que l'interface promet des notices — une œuvre nommant le
maître sous deux graphies pèse double (Le Primatice 269 → 197, Le Corrège 46 → 25, Titien
20 → 12). **L'identité** : 40 références prudentes sont rattachées au mauvais artiste, faute
d'exclure les homonymes (Corneille Michel-Ange, Vouet Aubin, Robusti Domenico, quatre
« Poussin », quatre « Raphaël »…). Total des 27 : **2 341 → 2 185 références**, soit −156.

**Ce que l'audit a trouvé en plus.** Le **dénominateur** est plus atteint que le numérateur :
sur les 749 attributions certaines de Michel-Ange, **422 appartiennent à Corneille
Michel-Ange**, contre 212 à Buonarroti. Raphaël capte 52 formes d'auteur, « Raphaël » étant
pris comme prénom (Lonne, Lardeur, Mengs, Collin…). La part affichée sur ces fiches est donc
fausse dans ses deux termes : Michel-Ange annonce 19 %, la réalité tourne autour de 37 %.
Et il y a des **faux négatifs** : Le Guerchin (93 notices), Bouchardon (86), Jules Romain
(78), Ludovico Carracci (76), Téniers (67)… dépassent largement l'ancien seuil et n'ont
jamais été examinés — la liste des 27 avait été composée à la main.

**Décisions** (decisions.md 2026-07-21 quater) : l'unité devient la **référence Joconde
unique** ; l'identité passe par une **table déclarative** d'alias et d'exclusions ; le seuil
descend **de 20 à 10**, sur l'unité corrigée. Le seuil ne sélectionne pas seul : au seuil de
10, 298 formes hors des 27 qualifient — imprimeries, manufactures, « anonyme », et le fonds
Barla de Nice avec 5 791 notices. Le critère double (maître de référence **et** seuil) est
maintenu, avec publication des candidats écartés et de leur motif.

Le total national de 24 507 n'est pas touché : il est calculé ligne à ligne, sans
identification de maître — vérifié dans le code.

**Rien n'a été modifié** : ni pipeline, ni exports, ni front. Prochaine étape = validation du
plan en huit temps inscrit à la roadmap, avant toute reprise éditoriale ou graphique.

## 2026-07-21 (ter) — L'en-tête du graphique cesse de se répondre à lui-même

Le titre posait une question, le sous-titre y répondait avec les mêmes mots — la marque de
la génération automatique. Les deux ont maintenant des rôles séparés : **le titre porte
l'angle** de l'artiste (4 à 9 mots, jamais une question), **le sous-titre la preuve
chiffrée**, en une phrase qui ne reprend rien du titre.

Quatre artistes témoins seulement, validés avant écriture du code :

- Ingres, au plus près du maître — « 194 des 204 œuvres concernées portent la mention
  “attribué à” ; aucune autre formulation n'atteint la dizaine. »
- Charles Le Brun, l'école en tête — « 240 des 310 … loin devant “attribué à”, qui en
  réunit 52. »
- Rembrandt, surtout dans son influence — « 165 des 187 … son atelier et son école n'en
  rassemblent que 18. »
- François Clouet, l'atelier en premier — « 95 des 105 … dans 8 musées différents. »

**Généralisé aux 27 dans la foulée**, après validation des quatre : chaque fiche a désormais
son angle propre. Onze titres relèvent de la mention très majoritaire, cinq d'un territoire
majoritaire, six de deux tendances proches, cinq d'une répartition sans tendance ; trois
sortent du gabarit parce que leur fait marquant est ailleurs (Rodin et sa mention unique,
Van Dyck et Ribera et leur dispersion). Trois défauts corrigés en relisant la sortie complète
— dont Van Dyck, qui affichait « 21 musées » et « 21 œuvres » dans la même phrase.

Un détour à noter : l'utilisateur a signalé que **seul Le Brun s'affichait et que les liens
ne répondaient plus**. Le site n'était pas en cause — `vite preview` indexe `build/` au
démarrage, et j'avais rebuildé deux fois sans redémarrer le serveur : tout le JavaScript
partait en 404, la page restait figée sur son rendu pré-généré. **Rebuilder impose de
redémarrer le preview.**

Les textes
sont écrits à la main mais **les nombres restent lus dans `artistes.json`** (le sous-titre
est une fonction) — sinon ils mentiraient dès la prochaine régénération, ce qui va arriver
avec la correction du double comptage. Sortie contrôlée en exécutant réellement les quatre
fonctions sur les données. Détail : decisions.md 2026-07-21 (ter).

## 2026-07-21 (bis) — L'onglet « Œuvres » de Titien était cassé

Signalé en relisant le site. La vitrine ne s'affichait pas sur **Titien** — ni sur **Le
Tintoret**, que personne n'avait vu. La cause était dans les données : sur une même œuvre du
Louvre, la base nomme le maître **deux fois sous deux graphies** (« VECELLIO Tiziano
(attribué à) » et « LE TITIEN (dit, attribué à) »). Le pipeline lit chaque segment d'auteur
à part et retenait donc deux fois la même notice ; le composant liste ses entrées par
référence, et deux clés identiques font échouer le rendu de toute la liste.

Corrigé à la source : `build_artistes.py` mémorise les références déjà retenues par maître,
une notice n'illustre la vitrine qu'une fois. Les deux artistes gagnent au passage un vrai
second exemple à la place du doublon ; **aucun comptage ne bouge** (diff limité à deux
exemples). Garde-fou ajouté au front pour qu'une régression ne puisse plus faire disparaître
une page entière. Export régénéré, `sync:data` + `build` OK. Détail : decisions.md
2026-07-21 (bis).

À retenir pour la suite : le piège des graphies multiples ne se limite pas à deux notices
différentes — il existe **à l'intérieur d'une même notice**.

## 2026-07-21 — Purge des quatre reliquats de vocabulaire

Petite passe de langue, sans effet sur les données ni les graphiques. « Corpus » disparaît
des textes affichés (intro de `/les-presque`, repère du bandeau maître, où il devient
« copies mises à part » — ce que le mot cachait) ; le répertoire dit désormais « Œuvres
concernées » comme le bandeau voisin ; « une formule domine largement » devient « revient
bien plus souvent que les autres » sur `/echelle`.

Au passage, la ligne de partage œuvres/notices est **reformulée** : ce n'est plus narratif
contre comptage sec, mais **la distance à la base** — « œuvres » dans ce que le visiteur lit
comme un propos sur les collections (en-têtes de liste compris), « notices » là où l'on parle
de la base elle-même (légendes de graphique, tooltips, seuils, Méthode). Détail :
decisions.md 2026-07-21. `build` OK. Restent hors périmètre : `/revisions` (rubrique en
réserve) et les commentaires de code.

## 2026-07-20 (bis) — Trois textes de la fiche remis en langue ordinaire

Passe d'édition ciblée, données et graphique inchangés. (1) **Ligne biographique** : gabarit
strict « [Activité] [nationalité] du [siècle], [dates]. » appliqué aux 27 — dehors le rococo,
le Grand Siècle, la cour des Valois et les écoles ; le siècle est celui de l'activité, pas de
la naissance. (2) **Titre du graphique** : « Le profil d'attribution de X » devient
**« Comment les musées rattachent ces œuvres à X »** — on nomme l'acteur et l'action, on
bannit profil/corpus/distribution. (3) **Phrase de lecture** sous le titre : cinq
formulations fixées, générées depuis les données, jamais improvisées.

Contrôlé en capture sur Boucher, Le Brun, Clouet, Rembrandt (les quatre tombent sur la phrase
attendue), et les 27 phrases relues en sortie de `lectureProfil`. Constat à garder en tête :
**la branche « les œuvres se partagent » n'est déclenchée par aucun artiste** avec les seuils
actuels — non traité ici, les seuils étaient hors périmètre. Détail : decisions.md 2026-07-20 (bis).
Reliquats signalés, non traités : « corpus » subsiste dans l'intro de `/les-presque` et dans
`BandeauMaitre`, et le répertoire dit toujours « NOTICES CONCERNÉES ».

## 2026-07-20 — Fiche artiste : portrait éditorial, généralisé aux 27

La scène du maître n'est plus une pile de compteurs (grand `310`, `9 %`, puis deux phrases
techniques) mais un **court portrait éditorial** : nom → **mention la plus fréquente**
(constat en Fraunces, deuxième niveau visuel) → récit chiffré en corps de lecture → repère
méthodologique discret. Les nombres sont **dans** les phrases (graisse + cobalt + chiffres
elzéviriens), jamais isolés. Prototype validé sur Le Brun, puis **généralisé aux 27**.

Deux acquis à retenir : (1) le **vocabulaire narratif public passe à « œuvres »** —
« œuvres associées à son nom », jamais « œuvres de X » — tandis que les **comptages secs
restent en « notices »** ; (2) nouveau champ **`citation`** dans `familles-public.js`
(forme citable en sujet de phrase, distincte du label d'axe et du header de tooltip) —
labels, headers, couleurs et tooltips inchangés, donc le graphique ne bouge pas.

Cas limites vérifiés en capture : égalité (Rigaud, « … sont les mentions les plus
fréquentes » + « chacune de ces mentions »), 100 % (Rodin, « portent toutes cette
mention »), bio conservée (Rembrandt, Clouet), 2 musées (Vinci). Les 27 phrases ont été
relues une à une avant rendu. `build` OK. Détail : decisions.md 2026-07-20.
Reliquat signalé, non traité : le répertoire dit encore « NOTICES CONCERNÉES ».

## 2026-07-19 (ter) — Wording des comptages : « notices » partout

Passe de cohérence sur toute la copie publique après la refonte de la fiche : tout
comptage se dit désormais en **notices** (tooltips du graphique via `notices()`,
ex-`oeuvres()` ; bande des copies de la vitrine ; carte des musées — titre « D'où
viennent ces notices », légende « ayant publié », replis, hors-cadre ; panneaux et texte
de `/echelle` ; seuil « vingt notices » de la page Méthode). « œuvre » reste réservé aux
objets montrés individuellement (vitrine, aperçu de carte). Au passage : purge du
reliquat public « Les presque » sur `/echelle` → « la rubrique "Explorer les maîtres" ».
Copie seule, aucune donnée ni calcul modifiés. `build` OK. Doctrine complète :
decisions.md 2026-07-19 (ter).

## 2026-07-19 (bis) — Fiche artiste : hiérarchie des informations

Refonte de la hiérarchie de la scène (`BandeauMaitre.svelte`) : `doute` en valeur
principale (« 310 notices… »), part sur le total de référence `propre + doute` (« 9 % …
périmètre étudié »), répartition sur `nb_musees_doute` (19, pas 64), formulation dominante
générée (famille dominante réelle + notices + part + libellé public + accords + égalités
via `ORDRE_FAMILLES`). `fractionEnMots` abandonnée (l'ancienne « près des deux tiers » était
fausse : 240/310 = 77 %). Répertoire : tri « Notices » + micro-légende « notices
concernées ». Page Méthode : explication du total de référence. Pipeline **non** touché.
Vérifié (Le Brun, Ingres, Rembrandt, Titien, Rigaud/égalité ; 3 onglets ; desktop + mobile ;
cohérence sur les 27). `build` OK. Prochaine phase (à part) : notices de l'onglet Œuvres.

## 2026-07-19 — Rubrique « Explorer les 27 maîtres » : titre, intro, séparation intro ↔ outil

Séance ciblée (périmètre volontairement restreint) sur `/les-presque` :
- Titre public **« Les presque » abandonné** → H1 **« Explorer les 27 maîtres »**.
- **Nouveau texte d'intro** (3 paragraphes fournis) expliquant la rubrique et le seuil,
  phrase de prudence en note discrète ; ancien texte (énumération de formules) retiré.
- **Deux temps séparés** : entrée éditoriale en deux colonnes (titre/texte, sans encadré),
  puis exploration introduite par **« Choisir un artiste »** (filet + espace, repère
  cobalt). Répertoire, profils, onglets, notices, viz **non touchés**.
- Chiffres 27 / 2 341 dérivés des données chargées ; « vingt » en toutes lettres ;
  correction locale de l'espace des milliers (U+00A0). Vérifié desktop (1280×760, début
  du répertoire visible dans le 1er écran) + mobile (empilement lisible). `build` OK.
- Avant cette séance (mêmes fils, en amont) : retour d'un maître d'ouverture sur
  `/les-presque` ; retour du chiffre vedette 24 507 sur l'accueil **avec formulation
  corrigée** (24 507 = notices prudentes, jamais « œuvres »), retrait du lien « Accueil »
  de la couverture. Détails : decisions.md 2026-07-18 (quater→sexies) et 2026-07-19.
- Preview désormais sur **port fixe 4340**.

## 2026-07-18 (quinquies) — PAUSE (limite tokens) · point de reprise

Fait à ce jour : direction « affiche » (couverture d'accueil + pages intérieures pleine
largeur, cadre navy/ivoire, accents cobalt/vermillon) étendue à toute l'application
(commits `6368cdc` C1 → `7209d6e` C5). `build` OK. Serveur de preview à relancer au
retour (`npm run preview` dans `web/`).

**POINT DE REPRISE (à faire, parti arrêté, non codé)** : refonte narration de
`/les-presque` en **deux états** — GUIDE à l'arrivée (aucun maître par défaut, l'intro
oriente), SCÈNE au clic d'un nom (portrait + profil/œuvres/musées), **graphe borné**,
intro qui recule en kicker en état B. **Spec complète et exécutable en une passe :
decisions.md 2026-07-18 (ter)** ; suivi : roadmap ★ REPRISE. Reprendre là après `/clear`.

## 2026-07-18 (quater) — C3-C4-C5 : direction « affiche » étendue à toute l'application

- **C3 · Comprendre les mentions** en pleine page (`main.pleine` + gouttières) : kicker
  cobalt + titre « Le langage de la prudence » + chapô resserré ; prudence vermillon ;
  ligne des territoires et grilles (mentions, comparaison) étalées ; données inchangées.
- **C4 · Méthode** en pleine page : kicker + titre « Ce que les chiffres disent, et ne
  disent pas » ; sommaire en rail collant (accent cobalt) ; contenu validé conservé.
- **C5 · nettoyage** : entrées homogènes sur les 4 pages ; accents chrome restants au
  cobalt (chiffres vedettes, liens POP). `--couleur-accent` (brun) ne reste que dans la
  rubrique en réserve `/revisions` (hors nav) et comme couleur du point de carte (donnée).

Toute l'application est désormais dans la direction « affiche » : couverture d'accueil +
pages intérieures pleine largeur, cadre navy/ivoire, accents cobalt/vermillon, **pigments
de données intacts**. `build` OK à chaque chantier, vérifié par capture. Détail :
decisions.md 2026-07-18 (bis). Suite : jugement d'ensemble.

## 2026-07-18 (ter) — C2 : Explorer les maîtres en pleine page

`/les-presque` passe en pleine largeur (`main.pleine` + gouttières `clamp`, fin de la
colonne centrale). Entrée narrative **courte revue** (kicker « Explorer les 27 maîtres »
+ chapô resserré : l'accueil ne pose plus le sujet). **Scène du maître renforcée**
(BandeauMaitre : portrait 14→16 rem, nom en `--taille-xxl`). **Graphe étalé** (le nuage
remplit la large colonne). Accents chrome → **cobalt** (kicker, onglet actif, tri +
sélection du répertoire) et **vermillon** (filet de précaution). Données, couleurs de
pigments, tooltips et interactions **inchangés**. `build` OK, vérifié desktop + mobile.
Détail : decisions.md 2026-07-18 (ter). Suite : C3 — Comprendre les mentions.

## 2026-07-18 (bis) — Extension de la direction « affiche » : C1 charte v2 + coquille

Décision d'étendre la direction d'accueil (affiche pleine page) à toute l'application.
Plan en 5 chantiers (roadmap.md ★ DIRECTION « AFFICHE ») : C1 charte+coquille, C2 Explorer
pleine page, C3 Comprendre, C4 Méthode, C5 narration. Principe : surface de lecture claire
+ **cadre au registre de l'affiche** (navy/ivoire/cobalt/vermillon), **pleine largeur en
zones** (fin de la colonne centrale), **pigments de données inchangés** ; chaque page porte
désormais son **entrée narrative** (l'accueil ne la pose plus).

**C1 fait** : tokens de cadre (`--cadre-fond` navy, `--cadre-encre` ivoire, `--accent-cobalt`,
`--accent-vermillon`) ; header des pages intérieures en **bandeau navy** (wordmark + nav
ivoire, actif souligné vermillon), **spectre de tête retiré** ; pied de page au même
registre. La surface de contenu reste claire (refonte page par page en C2-C4, sans casse
transitoire). `build` OK, vérifié par capture. Détail : decisions.md 2026-07-18 (bis).
Suite : C2 — Explorer les maîtres en pleine page.

## 2026-07-18 — Accueil : révision de l'affiche (un seul écran, accroche 3 étages, nav en cartouches)

Le prototype d'affiche va dans la bonne direction ; on garde l'image, le plein écran et
le principe, mais on précise l'accueil comme **pure entrée** dans l'application (ni stats,
ni méthode). **Accueil seulement** ; pages intérieures inchangées (Direction B).

- **Un seul écran** : suppression de tout ce qui suivait la couverture (bloc 24 507, %,
  lien « Comment ces chiffres… », source développée). `+page.js` ne charge plus de données.
  **Pied de page masqué sur `/` uniquement** (conservé ailleurs). Pas de défilement sur
  ordinateur. Les chiffres → « Comprendre les mentions » ; calcul/sources → « Méthode ».
- **Accroche remplacée** (provisoire, formulation imposée) en **trois étages** : « Un
  million de notices. / Des milliers d'attributions incertaines. / Une enquête dans les
  données des musées. », Spectral ivoire, progression légère (taille + tonalité), rythme
  d'affiche ; plus une mention très discrète « À partir de la base Joconde. ». Aucun autre
  paragraphe. Titre Fraunces inchangé.
- **Navigation en cartouches** (`EditorialNavigation` réécrit) : rectangles bleu-encre,
  texte ivoire, angles quasi droits, largeurs propres, décalés horizontalement, reliés par
  un trait fin ; ni boutons, ni cartes, ni menu, ni ombre, ni icône. « Explorer les
  maîtres » = entrée principale (plus large, plus lourde, fond cobalt, cible généreuse).
  Public Sans affirmé. Accueil marqué d'un trait vermillon (repère non uniquement
  chromatique). Survol/focus : déplacement ~5 px + prolongement du trait + fond plus clair,
  180 ms ; focus visible ; `prefers-reduced-motion`.
- **Contraste** : natif (clair/aplat sombre, ivoire/cartouches). Sur **téléphone étroit**,
  les étages débordaient sur la zone claire → **correction locale légère** (dégradé feutré,
  masqué haut/bas, mobile uniquement, derrière le bloc titre — pas un voile sur l'image) +
  compression des tailles sous 400 px.

Vérifié par capture : desktop 16:9, tablette portrait, téléphone étroit (360) et haut (400)
— titre/visage/entrée principale visibles vite, cartouches sur leurs zones, pas de scroll
horizontal, couverture plein viewport ; pages intérieures intactes. `build` OK. Détail :
decisions.md 2026-07-18.

## 2026-07-17 (septies) — Accueil refondu en affiche interactive (nouvelle direction, prototype)

Direction B jugée trop classique / catalogue. Nouvelle piste pour l'**accueil seulement** :
une **affiche interactive** bâtie sur deux illustrations fournies par l'utilisateur
(`images/accueil_01` horizontale desktop, `images/acceuil_02` verticale mobile). Les
pages intérieures **restent en Direction B** pour comparer les deux systèmes.

Fait :
- Assets versés dans `web/static/cover/` (`accueil-desktop.png`, `accueil-mobile.png`)
  + `README.md` de traçabilité (illustrations générées pour le projet, évoquent la
  **base Joconde**, pas Léonard ni le tableau).
- **`LandingCover.svelte`** : couverture plein écran (100svh, pleine largeur) via un vrai
  `<picture>` à deux sources ; textes et navigation en **vrais éléments HTML superposés**
  (jamais dans le bitmap). Titre clair dans l'aplat sombre, accroche + mention de source
  discrètes ; **`EditorialNavigation.svelte`** = les 4 entrées en annotations reliées aux
  lignes de la fiche (Explorer = entrée principale, poids supérieur ; routes réelles dont
  `/echelle`). Contraste natif (clair/sombre), **aucun voile** ni panneau opaque.
- Interactions : survol/focus = déplacement ≤ 4 px + prolongement de la ligne + contraste,
  180 ms ; focus clavier visible ; `aria-current` sur Accueil ; `prefers-reduced-motion` ;
  ordre de tabulation logique.
- Coquille (`+layout`) : masthead + spectre **masqués sur `/` uniquement**, `main` en
  pleine largeur ; les 4 pages intérieures gardent leur navigation.
- Chiffre 24 507 + source relégués **sous la ligne de flottaison** (invisibles au chargement).

Recadrage : le point faible était la **tablette en portrait** (l'asset horizontal s'y
recadrait trop, la nav quittait la fiche) → bascule sur la **composition verticale en
portrait ≤ 1024 px** (media `orientation: portrait`). Vérifié par capture sur 5 gabarits
(16:9, desktop moins large, tablette portrait, téléphone étroit, téléphone haut) : visage
jamais recouvert, nav sur ses zones, pas de scroll horizontal, couverture plein viewport ;
pages intérieures intactes. `build` OK. Détail : decisions.md 2026-07-17 septies.
Prochaine étape : juger l'accueil sur captures avant d'étendre la direction.

## 2026-07-17 (sexies) — Direction B menée à terme sur toutes les pages (fait)

**Statut.** La Direction B n'est PAS validée définitivement : son rendu est jugé trop
classique / trop proche des conventions visuelles fréquentes. On la mène jusqu'au bout
pour disposer d'une **version complète et comparable**, qui servira de modèle de travail
à une nouvelle direction (fournie ensuite par l'utilisateur). Aucun nouvel effet, folio
ou ornement hors cadrage ; textes validés et données inchangés.

Cinq pages recomposées, un commit par page :
- **Explorer / Profil** : en-tête de dossier compact (le profil apparaît au premier
  écran), portrait-origine via le bandeau, graphe élargi (répertoire resserré), onglets
  en soulignement (fin de la boîte), folio/cote discret.
- **Explorer / Œuvres** : grille de cartes blanches → **liste éditoriale continue**
  (entrées à filets) ; le **verbatim** du musée devient la matière (Fraunces, liseré de
  la mention) ; hiérarchie titre / musée / verbatim / lien POP ; **emplacement média
  réservé** par entrée (jamais d'image inventée).
- **Explorer / Musées** : fin de la petite carte centrée à 32 rem → **grande carte**
  (colonne large) + flanc légende/hors-cadre ; points fixes, POP et tooltips inchangés.
- **Comprendre les mentions** : la ligne (Spectre) porte les territoires **une seule
  fois** (pas de démonstration décorative) ; huit mentions en trois colonnes à filet
  coloré ; comparaison ample ; barres/données/réserves conservées.
- **Méthode** : sommaire numéroté en **rail collant** + contenu en colonne ; boîte grise
  retirée ; la ligne n'est PAS imposée (elle n'explique rien ici).

Toutes les boîtes grises arrondies remplacées par des filets. `build` OK à chaque page,
vérifié desktop + mobile ; interactions (onglets, tri, tooltips, liens POP) préservées.
Planche comparative complète produite (6 pages + 2 mobiles). Détail : decisions.md
2026-07-17 sexies. Suite : critique globale de cette version, puis nouvelle proposition
sur un modèle visuel plus précis fourni par l'utilisateur.

## 2026-07-17 (quinquies) — Direction artistique B « la ligne de proximité » : coquille + accueil (fait)

Revue globale de direction artistique menée (planche de l'existant, diagnostic, trois
directions maquettées avec vraies données/portraits/polices — A « le registre »,
B « la ligne de proximité », C « coupures & verbatim » ; maquettes conservées dans le
scratchpad). **Direction B retenue** par l'utilisateur (motifs : decisions.md 2026-07-17
quinquies). Début de la refonte **par pages complètes**.

Palier 1 livré :
- **Token `--spectre`** (dégradé des 8 pigments, stations centrées, température = distance)
  et **`Spectre.svelte`** (la ligne réutilisable, bande + libellés des trois territoires,
  repli mobile corrigé).
- **Coquille** (`+layout.svelte`) : filet brun de tête **remplacé par la ligne** (signature
  sur toutes les pages) ; canevas élargi 60 → 68 rem.
- **Accueil** (`+page.svelte`) recomposé : spectre à territoires, grand titre, CTA encre,
  figure de données à 8 stations, chiffre en preuve secondaire ; textes validés inchangés.

Pages non refondues (Explorer, Comprendre, Méthode) vérifiées intactes sous la nouvelle
coquille. `build` OK, vérifié desktop + mobile. Détail : decisions.md 2026-07-17 quinquies.
Suite : Explorer / Profil (portrait-origine + axe pleine largeur + folios).

## 2026-07-17 (quater) — Socle V1 bouclé : page Méthode + Accueil-couverture + nav à 4 entrées (fait)

Fin des deux zones restantes du socle éditorial V1.

**Page Méthode** (`/methode`, placeholder activé) : page unique et structurée qui
rassemble les limites dispersées. Cinq sections nettes — Périmètre · Construction des
données · Lire les chiffres · Limites · Sources et droits — avec un sommaire d'ancres.
Tous les chiffres viennent des exports (aucun saisi à la main) : `niveaux.json`,
`provenance.json`, `vue_ensemble.json`, `artistes.json`. Couvre les 13 points demandés
(Joconde, formulation prudente, détection lexicale + vérification 206 notices, critère
des 27 = seuil pas palmarès, recouvrements, copies à part, Nice/Barla + hors monoculture,
versements incomplets, pièges d'identification par les noms + corrections, constater vs
conclure, images/droits, version des données). Éditoriale, pas de FAQ ni de cartes.

**Correction de données.** Divergence trouvée et résolue : `typologie.md` affichait la
catégorie copie à **22 844** (somme naïve `d'après 22 564 + copie 280`, qui double-compte
les recouvrements) alors que la source canonique (`niveaux.json` `copie`, `vue_ensemble`
`copies_dapres.total`) donne **22 624** ; même correction pour révision (27 273 → **27 270**).
Interface (Méthode, Comprendre les mentions) et docs reprennent désormais la valeur
canonique : « d'après » = 22 564, copies au total = 22 624.

**Accueil-couverture** : l'accueil devient une couverture éditoriale à deux zones —
promesse à gauche (kicker, titre, sujet en une phrase, CTA « Explorer les 27 maîtres »,
lien « Comprendre les mentions »), **figure de données** à droite (structure média
ASSUMÉE et remplaçable : motif schématique d'index + les 8 pigments des mentions, pas
Léonard ni le tableau, légende « composition provisoire »). Le chiffre **24 507** passe
en **preuve secondaire** sous la couverture, avec renvoi à la Méthode ; le cas mono-musée
quitte l'accueil (trop technique → Méthode). Hiérarchie forte titre → promesse → figure
→ exploration → preuve chiffrée.

**Nav publique recentrée à 4 entrées actives** : Accueil · Explorer les maîtres ·
Comprendre les mentions · Méthode. « Les révisions » et « La carte » **retirées de la nav
publique** (code et données conservés au dépôt, routes non liées). `build` OK, vérifié
desktop + mobile, a11y (titres sémantiques, focus visibles, ancres). Détail : decisions.md
2026-07-17 (quater). **Fin du développement par petites zones** : prochaine étape = revue
globale de direction artistique et d'architecture visuelle (captures + compositions).

## 2026-07-17 (ter) — Zone « Comprendre les mentions » (page autonome, fait)

Chapitre autonome sur le vocabulaire muséal de la prudence (architecture §3), qui
**referme la boucle** ouverte par le retrait de la légende du répertoire. Route
existante **`/echelle`** activée (placeholder « L'échelle du doute »), libellé public
provisoire **« Comprendre les mentions »** (`prete: true`). Quatre parties :
1. **Intro éditoriale** courte + phrase de prudence commune verbatim.
2. **Trois territoires** : bande de progression continue (réutilise `territoires.js`,
   mêmes tints, titres, annotations) + flèche « plus près / plus loin de sa main ».
3. **Huit mentions** : liste scannable groupée par territoire, définition = `corps`
   de `familles-public.js` (source unique), formule type affichée seulement où
   `montrerMention` (nom générique « un maître »). Aucun libellé ni définition créé.
4. **Vue d'ensemble chiffrée** (`vue_ensemble.json`) : deux panneaux de **barres**
   (jamais d'anneau) à **échelle commune** — Ensemble (24 507) vs 27 noms (2 341) —
   nouveau composant `BarresMentions.svelte`, groupé par territoire, couleurs stables,
   % + effectifs affichés (« <1 % » si non nul mais arrondi à 0). Le basculement se
   lit d'un coup d'œil : « attribué à » 73 % → 37 %, « de son école » → 39 %.

Réserves respectées : mentions qui se recouvrent (pas de partition à 100 %, note
explicite), copies « d'après » comptées à part (22 564), concentration mono-musée
renvoyée à la page Méthode (pas de récit Nice/Barla ici). `vue_ensemble.json`
synchronisé (`npm run sync:data`), `build` OK, vérifié desktop + mobile. Détail :
decisions.md 2026-07-17 (ter). Reste (nav) : recentrage complet à 4 entrées (retirer
Révisions/Carte de la nav publique, « Les presque » → « Explorer les maîtres ») —
non fait ici, hors périmètre. Zones suivantes du kit : Accueil-couverture, Méthode.

## 2026-07-17 (bis) — Charte palier 3 : zone TroisTerritoires sur l'onglet Profil (fait)

Le principe éditorial central — la distance à la main du maître — devient **visible
dans le graphique** (architecture §5). Les 8 mentions, déjà ordonnées par distance,
se regroupent en **trois territoires contigus** : *Au plus près* (attribué à, nom ?) ·
*Autour du maître* (atelier, cercle, école) · *Dans son influence* (suiveur, manière,
goût). Correspondance exacte avec `ORDRE_FAMILLES` (plages 0-1 / 2-4 / 5-7).

- **Primitive `territoires.js`** : source unique du regroupement + titre + annotation
  courte par zone, réutilisable par la future rubrique « Comprendre les mentions ».
  Ne redéfinit aucun libellé (labels/couleurs restent dans `familles-public.js`) ;
  garde-fou dev qui vérifie l'alignement sur `ORDRE_FAMILLES`.
- **`NuageFamilles`** recadré **sans toucher aux données, points, couleurs, tooltips** :
  fonds très légers par zone (nouveaux tokens `--territoire-*`, température = distance),
  séparateurs fins, titres de territoire en tête. Bandes contiguës, sans cadre → **une
  seule ligne de proximité**, pas trois blocs.
- **Clé de lecture rétablie** sous le graphe (la légende détaillée a quitté le
  répertoire) : intro « de gauche à droite, le lien se desserre » + trois cellules
  contiguës (titre, annotation, mentions à pastilles). Les **annotations vivent dans
  la clé HTML** (le SVG ne sait pas revenir à la ligne → illisible en mobile).

Vérifié par capture sur trois profils opposés : Ingres (dominante *attribué à*, gros
point à gauche), Le Brun (*école*, au centre), Rembrandt (*manière*, à droite) — le
volume principal change de territoire selon le maître. Mobile : répertoire replié,
graphe lisible, clé empilée en trois blocs. `build` OK. Détail : decisions.md
2026-07-17 (bis). Reste (zones suivantes) : « Comprendre les mentions » (réutilisera
`territoires.js`), Accueil-couverture, Méthode.

## 2026-07-17 — Charte palier 3 : zone Répertoire (fait)

Deuxième zone du kit (après le prototype bandeau) : la colonne de gauche d'« Explorer
les maîtres » devient un **vrai outil de navigation**, séparé du profil (architecture
§4). Nouveau composant **`Repertoire.svelte`** qui absorbe recherche + liste et ajoute :
- **tri** par nombre d'œuvres concernées (défaut, ordre naturel du dossier) ou
  **alphabétique** (A→Z, `localeCompare` fr) — petit segment de deux boutons ;
- **microprofils colorés** conservés (jauge `BarreFamilles`, mêmes couleurs de familles) ;
- **sélection active** renforcée : filet d'accent à gauche + fond soutenu + `aria-current`
  (le filet transparent au repos évite tout saut de largeur) ;
- **responsive** : sur mobile le répertoire se **replie** (bouton « Choisir un maître /
  Masquer la liste »), replié d'emblée pour montrer le profil, refermé après le choix ;
  matchMedia plutôt qu'un `<details>` natif (piège de réouverture, cf. 2026-07-13).

La **légende détaillée des mentions** (`LegendeFamilles`) est **retirée** de sous la
liste : elle rejoindra « Comprendre les mentions » (architecture §3). Le composant
`LegendeFamilles.svelte` reste au dépôt pour cette reprise. `les-presque/+page.svelte`
ne garde que `selection` (liée au répertoire), le CSS de liste a migré dans le
composant. `build` OK ; vérifié par capture desktop + mobile. Piège de séance :
`vite preview` lancé avant un rebuild sert un ancien manifeste (chunks CSS hachés en
404 → page « déshabillée ») → **redémarrer le preview après un build**. Détail :
decisions.md 2026-07-17. Reste (zones suivantes) : TroisTerritoires, « Comprendre les
mentions », Accueil-couverture, Méthode.

## 2026-07-16 (quinquies) — Charte, palier 3 : prototype BandeauMaitre + ChiffreVedette (fait, ⏸)

Reprise après plantage machine : d'abord un commit de sauvegarde de tout le
travail non versionné depuis « Les presque : vitrine » (rubrique Avant/après,
Vue d'ensemble, charte paliers 1-2), `museum.zip` (backup local, 1,1 Go) exclu
via `.gitignore`. Puis **prototype du kit** (charte §5) sur la fiche maître réelle,
sans toucher au répertoire, au nuage ni à l'accueil :
- **`ChiffreVedette.svelte`** — primitive : grand nombre (Fraunces tabulaire) +
  légende courte.
- **`BandeauMaitre.svelte`** — « scène du maître » : portrait **agrandi** (14 rem)
  + nom + **phrase de synthèse calculée** + deux ChiffreVedette (œuvres sous le nom /
  musées). Absorbe l'ancien bloc `header.profil` de `les-presque/+page.svelte`.
- **Onglets renommés** Graphique/Œuvres/Carte → **Profil · Œuvres · Musées**
  (libellés éditoriaux, charte §5) ; état interne `vue` : `profil`/`oeuvres`/`musees`.
- CSS migré du `+page` vers le bandeau ; `build` OK ; vérifié par capture (Le Brun).

Deux points laissés à l'arbitrage (decisions.md même date) : (1) la synthèse
calculée **réintroduit** une phrase dérivée retirée le 2026-07-10 — assumée car
purement factuelle (nomme la formule dominante, ne l'interprète pas) ; (2)
`fractionEnMots` **plafonne à « près des deux tiers » (62 %)** alors que la mention
dominante peut monter à ~77 % (école de Le Brun) → sous-estimation à corriger si
validé. Reste : validation utilisateur, puis zones suivantes du kit (répertoire,
TroisTerritoires, accueil…).

## 2026-07-16 (quater) — Chantier direction artistique & architecture éditoriale

Cadrage de plus haut niveau inséré avant le kit de composants : repenser l'appli
comme une publication éditoriale centrée sur « Les presque ». Document créé :
`docs/architecture-editoriale.md` (nav recentrée à 4 entrées ; accueil = couverture ;
séparation répertoire ↔ profil ; distance à la main = principe visuel central ;
illustration Joconde = figure de DONNÉES, pas Léonard ni *La Joconde* œuvre). Inscrit
en roadmap (avant palier 3). ⏸ à valider. Aucun code, nav du front non modifiée.
Détail : decisions.md 2026-07-16 (quater).

## 2026-07-16 (ter) — Charte, palier 2 : coquille « inventaire »

Header/nav/structure refaits (`+layout.svelte`) : filet d'accent en tête, masthead
aligné sur la colonne, nav en petites capitales Public Sans avec page courante
soulignée, rythme aux tokens. Italique Spectral intégrée (regénération
`source_fonts.py`, 10 woff2). Espaces fines des grands nombres vérifiées (OK).
Limité : ni fiche maître ni composants internes. Vérifié par capture avant/après.
Détail : decisions.md 2026-07-16 (ter).

## 2026-07-16 (bis) — Charte, palier 1 : base typographique

Polices intégrées en local (Fraunces, Spectral, Public Sans ; woff2 latin +
latin-ext, ~277 Ko) via `web/scripts/source_fonts.py` → `static/fonts/` +
`fonts.css`, aucun CDN. Tokens manquants ajoutés (`tokens.css` : polices, échelle
typo, espacement, rayons, filets, surface, ombre, focus). Base typographique
appliquée globalement seulement (`+layout.svelte`) : Spectral en texte, Fraunces
en h1/h2 + wordmark, Public Sans en UI/nav/pied ; composants non refaits. Vérifié
par capture avant/après (accueil + Les presque). Détail : decisions.md 2026-07-16 (bis).

## 2026-07-16 — Charte graphique : direction arrêtée

Proposition de direction graphique pour l'application-cadre (audit de l'existant,
principes, palette, typo, composants, application aux presque, extensibilité).
Ambiance typographique retenue : « Catalogue savant » (Fraunces + Spectral +
Public Sans, auto-hébergées). Source de vérité créée : `docs/charte-graphique.md`.
Décision : decisions.md 2026-07-16. Pas de code — prochain palier = tokens + typo.

## 2026-07-15 (sexies) — Réalignement documentaire du recentrage

Mise à jour des docs de pilotage pour refléter la décision : la V1 publique est
centrée sur « Les presque » ; les autres rubriques (dont « Avant / après »)
restent conservées et documentées, hors périmètre publiable initial. `roadmap.md`
reçoit un bloc « ★ RECENTRAGE » en tête (périmètre V1 / en réserve / déjà fait) et
sa section P3-T2 est marquée EN RÉSERVE ; `rubrique-revisions.md` reçoit un bandeau
de mise en réserve ; `README.md` (État du projet) est corrigé ; `decisions.md`
2026-07-15 (ter) reste la décision canonique. Réalignement purement documentaire :
aucun code, aucune suppression, aucun déplacement de fichier.

## 2026-07-15 (quinquies) — « Vue d'ensemble » : reconnaissance + export préparé

Tour d'horizon des données pour une future section « Vue d'ensemble » des
formulations prudentes (rapport → docs/donnees.md 2026-07-15). Constat clé : les
27 noms = ~10 % du doute ; le hors‑27 est dominé par la monoculture de Nice
(Barla, 5 791). Message central retenu : « attribué à » domine au global, mais
école/atelier/manière prennent le dessus dans les 27. Export `vue_ensemble.json`
généré (`src/build_vue_ensemble.py`) — familles global/dans‑27/hors‑27, niveaux
global vs 27 + hors monoculture, copies à part. Cadré prudemment : pas d'anneau
(recouvrements), pas de classement par nom hors 27, pas de période, domaines/top
musées en réserve. Pas de front. Détail : decisions.md 2026-07-15 (quater).

## 2026-07-15 (ter) — Recentrage du projet sur « Les presque »

Décision de cadrage : « Les presque » devient la première publication complète de
*L'inventaire du doute* ; les autres rubriques (Avant/après, échelle, carte)
passent en pause / réserve, sans rien supprimer (dossiers futurs). `/revisions`
repasse hors nav publique (`prete: false`). Titre et périmètre de la v1 restent à
décider ; on pense figer d'abord la charte graphique sur « Les maîtres » comme
socle. Détail et garde-fous : decisions.md 2026-07-15 (ter). (Les paliers
datajournalisme du jour sur /revisions — anneau, prototype Les œuvres — sont
consignés dans decisions.md 2026-07-15 et bis ; ils restent valides, en réserve.)

## 2026-07-14 (quater) — « Avant / après » : réorganisation en onglets

La V1 (tout en vrac sur une page) jugée non publiable. Palier ÉDITORIAL (pas de
style, pas d'images) : `/revisions` passe en 4 onglets (En bref · Les chiffres ·
Les œuvres · Repères) sous un titre + chapô permanents. Le graphe des chiffres
est scindé en « constat principal » (4 familles galerie) / « cas secondaires »
(3 familles atténuées), même échelle. La galerie ne déroule qu'un groupe à la
fois via des chips (+ chip transversal « Un nom réapparaît »). Labels publics
refondus en phrases (« Un autre nom apparaît », « Le nom disparaît »…), renommés
dans `revisions_classify.py`, rebuild + sync. Modèle image RÉSERVÉ dans chaque
`cas` (`image: {statut,url,credit,source}`, tous « pending ») et dans
`CarteRevision` (vignette affichée seulement si droits clarifiés, jamais de
hotlink POP). `pytest` = 60, `npm run build` OK, 4 onglets + filtre vérifiés par
capture (playwright pour cliquer les onglets). Reste hors palier : charte, images
affichées, autres graphes, page méthode complète.

## 2026-07-14 (ter) — « Avant / après » : front V1 construit

Bilan v2 et taxonomie à 7 catégories validés par l'utilisateur, avec V1
**simplifiée** (pas de page dashboard). Renommé le libellé `meme_nom` en « Le
même nom, avec réserve » (`revisions_classify.py`), rebuild `revisions.json`
(`uv run python src/build_revisions.py`), `pytest` = 60 OK, `npm run sync:data`.
Page `/revisions` (SvelteKit) : intro courte + phrase forte sur la direction
inverse (5 283) + 2 cartes exemples (Vinci → anonyme ; École française → Van Loo,
« un nom rendu ») + **un seul** graphe (7 catégories triées, familles-galerie en
plein, familles-stats atténuées, légende qui dit lesquelles se visitent en
cartes) + galerie de 32 cartes groupées par catégorie et filtrables + note de
méthode (limite Joconde, concentration Louvre/dessins divulguée). Composant
réutilisable `web/src/lib/CarteRevision.svelte` (verbatims seuls, sans image,
lien POP). Route activée dans la nav. `npm run build` OK, vérifié par capture.
Différé : autres graphes (daté/non daté, anciens noms, siècles, domaines) →
page méthode ou V2. Reste à faire côté style : identité visuelle propre (fil
ouvert commun à tout le front).

## 2026-07-14 (bis) — « Avant / après » : bilan de vérification + refonte de la classification (fait, ⏸)

Import du CSV annoté (80 lignes) : 44 OK, 18 à exclure, 8 faux passage, 10 faux
parsing. Les commentaires ont fait émerger un modèle plus fin que mes 4
catégories → **taxonomie v2 à 7 catégories** dans un module dédié testable
(`src/revisions_classify.py`) : ajout de « Même nom, attribution plus prudente »,
« Déjà une copie ou un d'après », « Plusieurs anciens noms » (chaînes, stats
seulement). Cinq bugs de parsing corrigés, tous venus de l'échantillon :
parenthèses imbriquées, date collée au nom, prose prise pour nom, « ; »
biographique dans une parenthèse, parenthèse orpheline en tête. Distinctions
fines validées : chaîne du même nom ≠ plusieurs noms ; inclusion de prénom (Le
Nain Louis ↔ Le Nain) ; « plus prudent » = réserve ajoutée (sinon confirmation) ;
écoles nationales gardées en galerie via le verbatim. Verdicts figés dans
`tests/test_revisions.py` (25 cas + cohérence CSV : 44/44 OK en galerie, 0 fuite ;
`uv run pytest` = 60 passés). `revisions.json` régénéré (7 catégories, lot 32
cas / 20 musées / Louvre 6 % / 4 en direction inverse). Docs à jour. **En attente
de validation du bilan avant tout front.**

## 2026-07-14 — « Avant / après » : pipeline + échantillon de vérification (fait, ⏸)

Cadrage V1 validé (libellés publics ajustés). Construit le pipeline
`src/build_revisions.py` → `revisions.json` et `src/build_revisions_sample.py`
→ `echantillon_revisions.csv` (80 lignes). Front non touché.

Le travail de données a fait remonter trois choses concrètes : (1) **parsing** —
deux styles de catalogage (parenthétique vs prose « ancienne attribution : NOM »
du Louvre), le second polluait l'extraction du nom → corrigé ; (2) **anciens
noms fragiles** — contamination « copie d'après » (Michel-Ange 233→119) et effet
mono-musée (202/233 Louvre) → comptés hors copie, servent de filtre et non de
palmarès ; (3) **direction inverse** — 5 584 œuvres gagnent un nom, presque
autant que celles qui en perdent (5 824) : constat qui équilibre le récit.
L'échantillon (4 passages + 6 strates de pièges : chaînes, écoles, noms proches,
datées, copies-after, inverse) a servi immédiatement à repérer le défaut de
parsing avant tout front. Invariants `assert` en place. Constats dans donnees.md,
arbitrages dans decisions.md. **Prochaine étape : vérification manuelle par
l'utilisateur.**

## 2026-07-14 — « Avant / après » : cadrage V1 simplifié + audit images (proposé, ⏸)

Reprise du cadrage sur base plus simple. Titre provisoire « Avant / après ».
Trois vérifications neuves : (1) **images** — le CSV n'a pas d'URL, POP sert
l'image depuis un CDN interne sans droits par œuvre, la Licence Ouverte couvre
le texte pas les clichés → **pas d'images en V1**, carte textuelle + lien POP ;
(2) **périodes** — 16 % d'œuvres datables, 7 % de révisions datées → pas de
frise, structure par type de passage ; (3) **sélection V1** — lot par diversité
(plafond 2/musée, quotas par destination) testé : 32 cas, 10 musées, Louvre
ramené de 59,5 % à 19 %. Structure recommandée : par type de passage, grands
noms en filtre. Stats sur tout le corpus en graphes classiques (barres, donut,
colonnes). Cadrage réécrit dans **docs/rubrique-revisions.md** ; constats
images/périodes dans donnees.md ; arbitrages dans decisions.md. Aucun code
front. En attente de validation.

## 2026-07-13 — Audit des rubriques restantes + cadrage « Révisions » (proposé, ⏸)

Retour aux données avant de choisir la suite (demande utilisateur : « ce que
les données rendent lisible, pas ce que la roadmap prévoyait »). Trois passes
de scan du CSV complet. Verdict : révisions solide (26 667 avant→après réels,
destinations chiffrées, 5 formats de champ identifiés), carte nationale en
pause, décodeur réduit en encart. Deux faux positifs commis par notre propre
audit rapide et corrigés dans la foulée (grands noms testés en sous-chaîne ;
années de vie lues comme dates de catalogue) — la preuve que les contrôles
type SERODINE/RODIN restent nécessaires partout. Constats dans donnees.md
(+ dédoublement Île/Ile-de-France du champ Region) ; décision et garde-fous
dans decisions.md ; cadrage complet (titres, angle, forme, schéma
revisions.json, règles de comparaison, contrôles, 10 prototypes lisibles +
10 cas à exclure) dans **docs/rubrique-revisions.md**, en attente de
validation. Aucun code front.

## 2026-07-13 — « Les presque » : réécriture de l'intro (fait)

L'ancien chapô était trop évocateur, pas assez explicatif (retour utilisateur).
Nouveau texte (validé) : le titre « Les presque » est conservé mais **glosé dès la
première phrase** ; deux paragraphes disent ce que la rubrique montre, justifient le
choix des 27 noms (noms de référence, au moins vingt œuvres concernées — pas « les
plus grands ») et **orientent** le lecteur (jauge colorée → graphique → œuvres →
carte). Encadré refait **sans émoticône** : « Cette rubrique ne réattribue aucune
œuvre. Elle reprend les mots publiés par les musées dans leurs notices, avec leurs
précautions. » Ligne « critère » redondante supprimée. Vocabulaire public tenu (pas
de « famille / niveau / au doute », pas d'« erreur » des musées, pas d'expertise
sous-entendue). Guillemets figés (espaces insécables) pour éviter les « » orphelins.
`les-presque/+page.svelte` (texte + retrait de la règle CSS `.critere`).

## 2026-07-13 — Carte : palier style (fait)

Finition visuelle, sans toucher données ni comportement. Fond « régions très
estompées » (choix utilisateur) : aplat quasi nul, frontières gris très pâle, points
bien au-dessus. Survol/focus des points plus franc (pleine opacité + halo blanc
élargi), même retour pour points cliquables et non ; pas de distinction au repos des
cliquables (curseur seul). Carte ramenée dans une colonne centrée (titre, fond,
légende, mentions alignés). Légende et mention hors-cadre au même registre (petit
corps, encre douce, filet). Vérifié : Le Brun (dense), Van Dyck (dispersé +
hors-cadre), 390 px ; build OK. Différé (contenu) : repère texte du musée principal.

## 2026-07-13 — Faux rattachement de maître par sous-chaîne, corrigé (fait)

Un lecteur signale la notice `07980002404` (« Archimède », MUDO Beauvais) classée
« attribué à Rodin » alors que l'auteur est **Serodine** (« SE‑RODIN‑E » contient
« RODIN »). La détection de la formule était juste ; c'est l'identification du maître
qui déraillait (`_trouve_maitre` en sous-chaîne). Scan complet : 8 maîtres, 77
segments faux, dont 13 en doute (Tintoret 6, Léonard 6, Rodin 1). Correctif : test
**mot entier** (`\bALIAS\b`) — vérifié qu'il garde les vraies notices de Le Tintoret
et n'écarte que le fils « Tintoretto Domenico » ; seule perte, la coquille
« IIngres ». Exports régénérés : doute Tintoret 53→47, Léonard 56→50, Rodin 81→80 ;
aucun maître sous le seuil de 20 (liste des 27 intacte). Sync + build OK. Constats
dans donnees.md, choix dans decisions.md.

## 2026-07-13 — Carte : point-lien POP pour l'œuvre unique (fait)

Quand un musée ne conserve qu'une œuvre concernée, son point devient un lien vers la
fiche publique POP. Pipeline : `build_artistes.py` retient la 1re notice par musée
(`ref1`/`titre1`) et exporte `oeuvre_unique {reference, titre}` seulement si
`doute==1` (188 avec titre, 2 sans). Front : dans `CarteMaitre`, point à 1 œuvre →
`<a>` SVG vers `lienPop` (`target=_blank`, `rel=noreferrer`, focus clavier visible) ;
tooltip = aperçu (titre en italique si dispo, mention + pastille, « 1 œuvre
concernée »). Multi-œuvres inchangés (non cliquables). `Infobulle` gagne un champ
`titre`. Pas de nouvelle vue « œuvre ». Vérifié (URL POP, aria, sans-titre, focus,
Louvre non cliquable) ; build statique OK.

## 2026-07-13 — Carte : écartement des points qui se chevauchent (fait)

À taille fixe, deux musées pouvaient se cacher : coordonnées quasi identiques (deux
musées d'une même ville — Marseille/Marseille, Versailles/Versailles à ~0,1 px) ou
points très proches (Paris/Versailles ~5,7 px, Lille/Douai ~9,7 px). Ajout d'un
`ecarterPoints` dans `geo.js` : relaxation itérative déterministe (sans dépendance)
qui repousse chaque paire trop proche jusqu'à `2·R + 1,5 px`, en gardant les points
au plus près de leur vraie place ; les points confondus sont séparés selon l'angle
d'or (rendu stable). Contour blanc des points renforcé (1,1 px) et opacité 0,82 pour
détacher les voisins. Vérifié par captures (Le Brun, Boucher, Rubens) : Île-de-France
et paires régionales désormais lisibles.

## 2026-07-13 — Harmonisation des tooltips (fait)

Les trois tooltips vivants (graphique, carte, jauges) passaient déjà par
`Infobulle.svelte` : pas de fork, juste un renfort. `Infobulle` reçoit un header
en bande grisée (pastille optionnelle), une largeur stable (max-content bornée
13–17 rem), des lignes de ventilation à nombres alignés (+ `%` gris via `appoint`),
et `valeur` devient optionnelle. `tooltipFamille` fournit la pastille de header au
graphique. Les **jauges** passent d'un tooltip par segment à un **récap complet du
maître** (header = nom, lignes par mention + %) — cohérent avec la carte, et la
formule « % du doute » (mot banni) disparaît. Vérifié par captures : graphique
multi / 1 œuvre / mention type, carte multi / 1 œuvre concernée, jauge, 390 px.

## 2026-07-13 — Légende permanente des mentions sous la liste (fait)

Nouvelle brique `LegendeFamilles.svelte` sous la liste des maîtres, commune aux
trois vues : la clé des couleurs avant interaction. Réutilise `header` + `corps`
de `familles-public.js` (source unique, mêmes mots que les tooltips), pastilles
rondes, ordre de l'axe. Un `corps` reformulé au passage (atelier). Repliable en
mobile (état JS via `matchMedia`, pas un `<details>` natif — son contenu fermé
n'est pas ré-affichable en CSS selon la largeur, vérifié sur Chromium). Validé
par captures desktop + mobile.

Reste (palier séparé) : harmoniser le style des tooltips.

## 2026-07-12 — Carte par maître : revue (taille fixe, tooltip, légende) (fait)

Revue du premier rendu, trois sujets traités.

1. **Test A/B taille variable vs fixe** (captures Le Brun / Ribera / Van Dyck /
   Ingres). Le variable (∝ √doute) ne tient que sur un vrai dégradé (Van Dyck) :
   ailleurs son échelle **propre au maître** trompe (un gros cercle Ribera = 3
   œuvres vaut un gros cercle Le Brun = 276) et gonfle les petits volumes en gros
   disques qui se chevauchent. **Taille fixe retenue** (décision utilisateur) : la
   carte dit *où*, le *combien* reste au survol et dans l'onglet graphique.
2. **Tooltip refait** : il réintroduisait « Presque lui / Autour de lui » (niveaux).
   Remplacé par les **familles publiques** (`familles-public.js`) avec pastilles de
   couleur, tri par valeur, accord singulier/pluriel. `Infobulle.svelte` reçoit un
   champ optionnel `lignes`. Exemple : « musée du Louvre, Paris / 276 œuvres
   concernées / De son école 225 · Attribué à 37 · Son atelier 14 ».
3. **Légende** adaptée au point fixe : « Un point = un musée où au moins une œuvre
   concernée est conservée. Passez sur un point pour voir combien… ».

Nettoyage : rayon variable, calibres, bascule de test `?carte=fixe` retirés.
Piège CSS corrigé (la règle globale `svg { width:100% }` gonflait le point-repère
de légende → largeur figée sur `.repere`). Revalidé par captures.

## 2026-07-12 — Carte par maître : premier rendu (fait)

Deux mini-paliers rapprochés, après validation de la spéc (decisions.md même date) :

1. **`web/src/lib/geo.js`** — projection `geoConicConformal` calée France (parallèles
   44/49, méridien 3°E), bornes métropole partagées + `estProjetable`, normalisation
   de l'enroulement du GeoJSON.
2. **`web/src/lib/CarteMaitre.svelte`** — onglet **Carte** ajouté après Graphique /
   Œuvres. 1 point = 1 musée, rayon ∝ √doute (3–22 px), couleur unique, fond régions
   discret, légende de calibres, tooltip (musée/ville/nb/ventilation), mention
   hors-cadre, repli phrase si < 2 musées projetables.

**Piège d3-geo résolu.** Les anneaux de france-geojson sont enroulés à l'envers pour
d3-geo : `fitExtent` sur les polygones lisait « tout le globe sauf la France » (échelle
microscopique, tout s'effondrait) et le fond se remplissait en complément (grand
aplat). Correction : ajuster la projection sur un `MultiPoint` des sommets (les points
se projettent sans ambiguïté) et réinverser les anneaux au chargement pour le tracé.

Vérifié par captures : Le Brun (concentration extrême au Louvre), Rubens et Van Dyck
(dispersés), Ingres (concentré à Montauban), Van Dyck déclenche bien la mention
« Hors cadre métropolitain : 1 œuvre au musée Léon Dierx, Saint-Denis de La Réunion ».
Reste : palier style (fond, points, chevauchements Île-de-France, calibres).

## 2026-07-12 — Relecture de CLAUDE.md : remise en accord avec la réalité (fait)

Revue complète demandée par l'utilisateur. Trois écarts corrigés dans CLAUDE.md :
- la roadmap était annoncée dans `decisions.md` alors qu'elle vit dans
  `docs/roadmap.md` depuis le 2026-07-03 ;
- la stack affichait encore « à terme D3.js » : le front SvelteKit statique
  (décision du 2026-07-07), les dataviz Svelte/SVG et `npm run sync:data`
  sont désormais décrits ;
- « `data/` n'est pas versionné » était imprécis : seul `data/raw/` est ignoré,
  `data/exports/` est suivi par git (de même `web/static/data/`, généré, ignoré).

Dans la foulée : README remis à jour (il annonçait encore « Phase 1 en cours »,
installation du front ajoutée) et note d'orientation en tête de la section
roadmap historique de `decisions.md` (esquisse phase 0 conservée comme trace).

## 2026-07-10 — Nuage : labels publics, axe réordonné, tooltips prudents (fait)

Chantier « labels » du nuage traité (deux tours de proposition, validés avant
implémentation). Fait :
- **Couche de traduction** `web/src/lib/familles-public.js` (label public + formule
  exacte + sens), réutilisable par Détail plus tard.
- **Labels publics** sur l'axe : attribué à · nom (?) · son atelier · son cercle ·
  de son école · un suiveur · sa manière · dans son goût. Plus de « ? » seul.
- **Axe réordonné** par distance au maître (option B, typologie.md) : la lecture
  gauche-droite est désormais honnête.
- **Micro-légende** statique (1 ligne) « De gauche à droite, le lien au maître se
  desserre. » — remplace la bulle rejetée, aucun saut.
- **Tooltips** réécrits : `label — « formule exacte » : sens prudent. N œuvres.`
  Sans niveau/famille/marqueur. Vérifié (Le Brun/école = 240).
- **CLAUDE.md** : règle « Couche de libellé public obligatoire ».

Contrôlé par capture (ordre, pas de chevauchement même « dans son goût ») et
`npm run build` OK. Périmètre tenu (nuage seul). Reste noté : accueil, Alençon
dans CLAUDE.md, refonte Détail — non traités volontairement.

## 2026-07-09 — Nuage : bulle « comment lire » rejetée + les labels à retravailler (à faire)

Retour utilisateur : la bulle dépliable « Comment lire ce graphique » est **très
mauvaise**, non validable. **Supprimée** (même branche). Deux défauts :
- **technique** : le `<details>` en se dépliant pousse brutalement le bloc
  graphe+portrait de 3-4 cm → saut de page inacceptable ;
- **de fond** : expliquer le graphe dans un bloc à part, avec des indications
  éparpillées, **complique la lecture**. Un graphe se lit sans notice : il lui
  faut une bonne **légende** et des **labels clairs**, pas un mode d'emploi.

Constat plus large assumé : « **de gros progrès à faire en narration** ».

**Prochain chantier décidé (rien n'est encore fait) — retravailler les LABELS du
nuage**, avant toute légende. Trois axes de travail donnés par l'utilisateur :
1. **les noms** — aujourd'hui « attribué à », « ? », « école de », « atelier »,
   « entourage », « suiveur », « manière de », « genre de » sont **jetés tels
   quels** sur l'axe ;
2. **leur valeur / signification** — le lecteur ne sait pas ce que veut dire
   « attribué à », « manière de »… ; le sens n'est donné nulle part ;
3. **leur forme et leur présentation** — labels mal mis en évidence ; cas criant :
   le label « **?** » seul **n'a aucun sens** affiché ainsi.

Ordre : on travaille les labels d'abord (noms + sens + présentation), la légende
ensuite. La réflexion « forme de légende » (pistes groupée/à plat) est **en
attente**, ne pas l'implémenter. Chapô/bio à réduire aussi, mais **plus tard**.

## 2026-07-09 — Refonte des textes de « Les presque » : séparer les trois natures

Constat utilisateur : les textes de la fiche maître étaient « n'importe quoi » —
techniques, non publiables. Diagnostic partagé : le défaut est **structurel**, le
mode d'emploi de la dataviz avait envahi l'éditorial. Trois natures de texte
mélangées (éditorial / mode d'emploi / mentions techniques).

Fait (mode plan validé, deux maîtres témoins jugés sur pièce avant généralisation) :
- **Éditorial séparé** : nouveau `web/src/lib/editorial-maitres.js` (bio + angle
  par maître, couche éditoriale du front, pas des données). Témoins écrits main :
  **François Clouet** (doute proche, « atelier ») et **Rembrandt** (doute lointain,
  « à la manière de »). Les 25 autres : angle **dérivé** de la famille dominante
  (repli honnête). Chiffres racontés en français (`fractionEnMots`).
- **Mode d'emploi sorti une seule fois** : bulle dépliable « Comment lire ce
  graphique » à côté de la bascule ; retiré de chaque fiche (figcaption + lecture
  du nuage supprimés). La mise en garde d'attribution y est déplacée.
- **Légende de portrait normée** : sujet + auteur + source + licence (plus de note
  de méthode déguisée en légende).
- **Vocabulaire interne banni** de l'interface : notice→œuvre, plus de « niveau »
  affiché, « atelier (qualificatif, beaux-arts) »→« atelier de », vue Détail
  nettoyée (colonne « Niveau » retirée, « Œuvres »).
- **CLAUDE.md** : ajout des blocs « Principes de dataviz » et « Principes de
  rédaction » pour que ces règles s'appliquent d'office. Consigné dans decisions.md.

Vérifié par captures (Le Brun = angle dérivé, Clouet, Rembrandt, vue Détail) et
`npm run build` OK. Reste (P3-T1) : écrire les 25 bios/angles à la main ;
reformuler l'accueil (« notices », « lexique ») en gardant les deux dénominateurs.

## 2026-07-09 — Retour sur le nuage : plus cohérent, mais trop anonyme

Verdict utilisateur sur le nuage : **plus cohérent narrativement et plus lisible**
que la galaxie et les barres — mais **manque de présence visuelle, trop anonyme**.
À traiter (consigné, pas encore implémenté) :
- **Retirer les libellés de niveau** (« Presque lui / Autour de lui / Son style ») :
  jugés inutiles ici → à enlever.
- **Ajustement proportionnel** : **points plus gros** + **grille plus resserrée**
  (trop d'écart entre les points hauts/bas et gauche/droite) → viz plus dense,
  plus forte.
- **Couleurs : plus tard** (au moment du style + de la légende des labels) ;
  aujourd'hui elles renforcent l'anonymat, on n'y touche pas maintenant.
- **Idée à évaluer (portrait) :** placer un **portrait libre de droit du peintre**
  (dessin/photo/gravure, via Wikimedia Commons) **en face** de la visualisation,
  celle-ci sur une **plus petite grille** pour que les points soient plus présents.
  Évaluation dans docs/roadmap.md + réponse à l'utilisateur (faisabilité PD,
  cohérence des images, illustration ≠ source de comptage).

Choix utilisateur : « ajustements + maquette portrait ». Implémenté (même branche) :
libellés de niveau retirés, points plus gros (rayon 6→16), grille resserrée
(viewBox compact), **layout portrait ↔ nuage** avec un **placeholder** (silhouette
inline) pour juger les proportions avant de sourcer les vraies images. Build OK.
Reste (①quater) : sourcer les 27 portraits PD + traitement uniforme + crédits +
fallback, après validation du layout. Contrainte notée : sourcing réseau incertain
dans l'environnement → images à fournir ou à tester le moment venu.

## 2026-07-08 — « Les presque » : barres → nuage de points à grille fixe

- Les barres livrées le matin ne permettaient ni comparaison entre maîtres (grille
  changeante) ni lecture des volumes réels (normalisation à la largeur). Remplacées
  par un **nuage de points sur grille fixe/commune** (decisions.md).
- Vérifié sur données : 8 familles réelles chez les 27 (« présumé » absent → colonne
  retirée) ; plafond Y commun = 240 (« école de » Le Brun), calculable côté front
  (aucune modif pipeline). Coût assumé signalé : petits volumes/petits maîtres au
  plancher — contré par le cadrage, pas en trichant sur l'échelle.
- Implémenté sur la même branche `feat/les-presque-barres` : `NuageFamilles.svelte`
  (axe X familles, axe Y volume plafonné, couleur/famille groupée par niveau,
  graduations, survol), bascule « Nuage / Détail », `BarresFamilles.svelte` retiré
  (remplacé, l'historique git le garde). Galaxie toujours archivée. Build OK.
- Stop pour validation avant le palier données géo + carte.

## 2026-07-08 — Réorientation « Les presque » : galaxie abandonnée, barres + carte

- Suite au brief utilisateur : galaxie abandonnée dans cette vue (schéma
  moléculaire, pas une constellation ; « vraie constellation » reportée en réserve,
  branche séparée). Remplacée par des **barres horizontales** (1 barre = 1 famille,
  longueur ∝ notices). Ajout d'une **carte par maître** (nouveauté).
- Faisabilité carte vérifiée sur données réelles : grain = musée détenteur
  (coord via musees.json, 98,7 %) ; doute très dispersé (~1/musée, sauf Le
  Primatice). Piège repéré : le champ `musees` d'artistes.json confond
  ferme/copie/doute → export à enrichir avant la carte.
- Arbitrages utilisateur : technique carte = **D3-geo auto-hébergé** (GeoJSON
  France/départements open data, aucune tuile externe, pré-rendable) ; ordre =
  **barres → carte**. Consigné dans decisions.md + roadmap.md (P3-T1 réorienté).
- Rien implémenté (mode plan). Prochain palier : ① barres horizontales.

## 2026-07-08 — Doc d'analyse de « Les presque »

- Galaxie jugée **lisible** par l'utilisateur. Restent à travailler : le style
  (identité propre, non générique), les labels (trop techniques) et le récit
  (la forme actuelle s'éloigne de la vision « galaxie/constellation » voulue).
- À sa demande, rédigé `docs/dataviz-les-presque.md` : document **autonome**
  (compréhensible sans le code) décrivant la dataviz sur les plans technique et
  esthétique, avec la synthèse des écarts intention ↔ réalisation et les
  questions ouvertes. Destiné à être analysé de l'extérieur.
- Rien changé au code : c'est un état des lieux pour décider de la suite.

## 2026-07-07 — P3-T1 : galaxie + retour « incompréhensible »

- Retour utilisateur fort : le front actuel est incompréhensible pour un visiteur
  lambda (on ne sait pas ce que fait le site, son objectif, son fonctionnement ;
  les fiches sont du jargon). Décision commune : **finir les tâches de la roadmap
  puis faire un bilan compréhension**, ne pas tout refondre maintenant. Noté en
  mémoire (feedback [[front-probleme-comprehension]]).
- Galaxie construite (`lib/GalaxieMaitre.svelte`) et branchée en bascule
  « Galaxie / Détail » sur `/les-presque` (galaxie par défaut). Maître au centre,
  familles de doute en orbites (proche = probable, loin = doute fort), copies
  « d'après » en anneau extérieur à part. Rendue auto-explicative pour attaquer
  le problème de compréhension : titre en clair, centre légendé, orbites nommées,
  note de lecture (« position indicative, pas une mesure d'authenticité »).
- Intro de `/les-presque` réécrite en langage courant (mode d'emploi « 👉 choisissez
  un maître… force du doute »). Build statique OK, une seule galaxie rendue.
- Reste : regarder le rendu ; l'onboarding global du site (accueil) reste à revoir
  au bilan.

## 2026-07-07 — P3-T0 validé + P3-T1 : « Les presque » (1re dataviz)

- Socle validé par l'utilisateur (sur le fond). Réserve indicative : le style est
  jugé « trop Claude normé », générique ; identité visuelle à retravailler plus
  tard (après les dataviz). Noté en mémoire (feedback) et decisions.md ; on n'y
  touche pas maintenant.
- 1re dataviz montée : route `/les-presque`. Composants réutilisables créés :
  `lib/joconde.js` (lien POP aligné sur src/config.py, métadonnées des 3 niveaux)
  et `lib/BarreNiveaux.svelte` (barre empilée du doute, avec/sans légende).
- Fiche « presque » : échelle du doute, tableau des formules employées, bande
  « d'après X » isolée (copies assumées, jamais comptées comme doute), exemples
  réels avec liens POP. Liste des 27 maîtres filtrable à gauche.
- Garde-fou éditorial en place (chapô « comment les musées nuancent », pas de
  « trésor caché »). Build statique OK, données réelles vérifiées dans build/.
- Limite assumée : le « moteur de recherche sur toute la base » (roadmap) n'est
  pas fait — il faut d'abord un export de tous les noms + comptages (pas encore
  produit). Pour l'instant le filtre porte sur les 27 vedettes.
- Reste : validation utilisateur de « Les presque » ; réserve Bruegel/Cranach
  toujours ouverte ; style à reprendre ; puis brique suivante.

## 2026-07-07 — P3-T0 : socle SvelteKit monté (en attente de validation)

- Échafaudage `sv create` dans `web/` : SvelteKit 2 / Svelte 5, JavaScript (pas
  TS, choix lisibilité), adapter static. Surprise notée : la nouvelle version
  câble l'adapter dans `vite.config.js` (`sveltekit({ adapter: adapter() })`),
  pas dans un `svelte.config.js` — ce dernier n'existe pas, c'est normal.
- Site entièrement pré-rendu : `export const prerender = true` à la racine.
- Accès aux données : `npm run sync:data` copie `data/exports/web/*.json` vers
  `web/static/data/` (servis en `/data/…`). Dossier généré, ignoré par git ;
  à resynchroniser après chaque export du pipeline Python.
- Coquille : `+layout.svelte` (en-tête, nav « une brique = une route », briques
  futures en placeholder pour ne pas casser le pré-rendu), tokens de style
  (`lib/styles/tokens.css`, couleurs des 3 niveaux).
- « Hello data » : l'accueil pré-rend le chiffre vedette réel **24 507**
  (+ 18 716 hors monoculture, provenance datée) depuis `niveaux.json`.
- `npm run build` OK, chiffre vérifié dans le HTML statique de `web/build/`.
- Reste : ⏸ validation utilisateur du socle avant la 1re dataviz (« Les presque »).

## 2026-07-07 — Stack du front arrêtée : SvelteKit

- Choix de socle tranché par l'utilisateur : **SvelteKit en build statique**
  (`adapter-static`), front isolé dans un dossier dédié, consommant les JSON de
  `data/exports/web/`. Aucun serveur (règle « jamais la base dans l'appli »).
- Motifs consignés (docs/decisions.md) : routage = structure éditoriale (méthode
  au même rang), coquille partagée par composants, bonne cohabitation avec D3,
  lisible pour un dev intermédiaire.
- Roadmap : P3-T0 réécrit en « Socle SvelteKit » avec sous-étapes
  (échafaudage → accès aux JSON → coquille → hello data → ⏸ validation).
- Prochaine action : monter le socle SvelteKit avant la 1re dataviz (« Les presque »).

## 2026-07-07 — P3-T1 : entrée « par l'artiste » (liste vedette + export)

- Ouverture de la phase 3 côté données : la 1re dataviz sera « Les presque »
  (doute autour d'un maître connu). Critère de la liste vedette arrêté par
  l'utilisateur : maître de référence + ≥ 20 doutes (hors copie), choix « A »
  (le critère fait loi).
- Correction de repérage majeure trouvée en chemin (docs/donnees.md) : le doute
  s'écrit aussi HORS parenthèses (Ingres 13 → 204) et les « (école allemande) »
  sont des nationalités, pas du doute (Dürer 161 → 19). Comptage refait avec les
  regex réelles de markers.py, par segment.
- Désambiguïsation des familles : Fragonard = Jean-Honoré (31, conservé) ;
  Bruegel et Cranach l'Ancien retirés (< 20 une fois le maître isolé du fils).
  Liste finale : **27 maîtres**.
- Code : markers.py::famille_segment() (public, réutilise le lexique, 35 tests
  verts) + src/build_artistes.py → data/exports/web/artistes.json (44 Ko).
- Roadmap phase 3 réécrite (P3-T1 en cours). Reste : réserve Bruegel/Cranach à
  trancher, puis le front de « Les presque ».

## 2026-07-06 — P2-T4 : cas racontables

- Décision : Alençon = ouverture, incarnation de la limite (vérif. approfondie
  la veille : versement partiel confirmé par l'API).
- docs/cas.md : 4 cas rédigés avec données réelles — Alençon (l'absent),
  Nice/Barla (doute industriel), Besançon (vrai doute Géricault, miroir
  d'Alençon), Louvre/Clouet (doute + révision, généalogie d'avis datés).
- src/build_cases.py → data/exports/web/cas.json (notices réelles par référence).
- Interruption (classifieur Bash indisponible) absorbée sans perte grâce au
  découpage repris-si-interrompu ; repris le 2026-07-06.
- Reste : P2-T4f (cas par niveau, optionnel) + validation utilisateur.

## 2026-07-05 — P2-T3 : pipeline d'exports + deux découvertes

- src/build_exports.py : 4 JSON légers (provenance 0,5 Ko, niveaux 2 Ko,
  musees 182 Ko, territoires 14 Ko). Provenance datée intégrée. Niveaux en
  partition stricte (chaque doute au niveau le plus léger). Bug NaN→null corrigé.
- Découverte 1 : le muséum de Nice = 5 791 doutes, tous « Barla (attribué à) »
  (planches naturalistes), soit 23,6 % du doute national — un singleton qui
  écrase le classement. Hors Barla : ~18 716. Décision utilisateur à prendre.
- Découverte 2 : Alençon, le cas fondateur, a 109 notices versées et 0 doute —
  preuve vivante de la limite « versements incomplets ». Matière pour P2-T4.
- En attente : validation de la structure + arbitrage monoculture.

## 2026-07-05 — P2-T1 et P2-T2 : recouvrements, typologie validée, lexique v2

- P2-T1 : Venn chiffré, règles de non-addition validées par l'utilisateur.
- P2-T2 : échelle à 3 niveaux validée (« Presque lui » / « Autour de lui » /
  « Son style, sans lui »), trois arbitrages rendus (atelier → beaux-arts
  seulement, écoles-lieux écartées, ? au niveau 1).
- Lexique v2 : restriction par domaine (post-traitement dans detections(),
  colonne Domaine désormais exigée), liste versionnée des écoles-lieux,
  deux nouvelles familles écartées. 35 tests passent.
- Recomptages : doute 25 220 → **24 507** ; écartés totaux 1 868 ;
  Venn v2 : 66 420 touchées, doute + révision 4 615.
- Prochaine étape : P2-T3, pipeline d'exports JSON pour la restitution.

## 2026-07-05 — GO : phase 1 close, ouverture de la phase 2

- GO validé par l'utilisateur : la phase 1 (test go/no-go) est close.
- À sa demande, classification des familles consignée en document de
  référence : `docs/familles.md` (14 familles, 4 catégories, sens des
  formules, volumes v1, fiabilités mesurées par les deux contrôles humains).
  Rôle déterminant attendu pour la typologie (P2-T2) et les visualisations.
- Phase 2 détaillée dans la roadmap : P2-T1 recouvrements, P2-T2 typologie,
  P2-T3 pipeline JSON, P2-T4 cas racontables. Première tâche : P2-T1.

## 2026-07-05 — T5bis : bilan du mini-contrôle → recommandation GO

- Mini-lot annoté récupéré (onglet « echantillon_recheck » du même classeur
  Google Sheets ; export xlsx pour lire le second onglet, zéros restaurés).
- ? : 0/15 faux. « Atelier de X » écarté : 15/15 confirmés — on ne jette
  aucun vrai doute. École : 2/15 (écoles-lieux consacrées). Atelier : 6/20
  (ateliers-entreprises ; les faux vivent en ethnologie/artisanat, les vrais
  en peinture/dessin — piste domaine pour la phase 2).
- Doute pondéré : 5,7 % conservateur, 3,3 % ajusté → **seuil GO franchi**.
- En attente : décision de phase (fin de la phase 1).

## 2026-07-04 — Cycle v1 : reformulation du lexique

- Lexique v1 écrit et testé : l'idée-force est de lire la convention
  d'écriture (qualificatif entre parenthèses) plutôt que le mot. Détection
  « atelier » segment par segment ; nouvelle catégorie « ecarte » pour la
  population « Atelier de X » (1 123 notices), chiffrée au lieu d'être jetée
  en silence.
- Les 25 verdicts clés de l'utilisateur sont devenus des tests pytest :
  le lexique a maintenant un contrat de non-régression humain.
- Recomptage : doute 29 726 → 25 220 (−15 %). Familles corrigées :
  atelier 5 558 → 1 759, école 2 865 → 2 093, ? 2 731 → 2 213.
- Mini-lot T4bis généré : 65 lignes (graine 202607, distincte de T4).
  En attente de la vérification utilisateur.

## 2026-07-04 — T5 : bilan de la vérification manuelle

- Échantillon annoté récupéré depuis Google Sheets (206/206 verdicts ; zéros
  de tête des références restaurés — piège tableur à retenir).
- Doctrine consignée : un marqueur ne compte que s'il qualifie l'attribution
  de l'œuvre de la notice ; `(attribué, d'après)` → copie ;
  `anonyme (attribué)` → incertain, hors calcul.
- `src/evaluate_sample.py` : taux pondérés par le poids réel des familles.
  Doute : **17,0 %** de faux positifs → tranche « reformulation ».
  Copie et révision : **0 %**. Le problème est concentré (atelier de 64 %,
  école de 20 %, ? 16 %) et chaque cause est identifiée.
- Recommandation : reformulation ciblée du lexique (v1), recomptage,
  mini-contrôle sur les familles corrigées. En attente : décision de phase.

## 2026-07-03 — T4 : échantillon de vérification

- T3 validée ; décisions consignées (taux vedette = notices avec auteur ;
  comptage de référence sur toute la base, beaux-arts en angle) ; tâche
  « recouvrements entre familles » ajoutée à la phase 2.
- `src/build_sample.py` : 206 lignes tirées (stratifié, graine 42), familles
  rares sur-représentées, « présumé » (4) et « anciennement attribué » (7)
  pris en entier.
- Liens POP testés (redirection www corrigée dans config.py).
- Mode d'emploi rédigé : `docs/verification-echantillon.md`. En attente de la
  vérification manuelle de l'utilisateur — T5 démarre au retour du CSV annoté.

## 2026-07-03 — T3 : détecteur v0 et taux de base

- `src/markers.py` (lexique versionné, 13 familles) + `src/count_markers.py`.
- Deux corrections en cours de route, repérées sur les exemples réels : le « ? »
  de dates (72 % du signal brut de cette famille était du bruit !) et « école
  des Beaux-Arts » dans les biographies. Détail dans `donnees.md`.
- Résultat : 29 726 notices avec au moins un marqueur de doute (2,90 % de la
  base, 3,53 % des notices avec auteur). « d'après » : 22 564 (à part).
  Champ Ancienne_attribution : 27 266. La peinture est le domaine au taux le
  plus élevé (6,00 %), le dessin le plus gros volume.
- En attente : validation T3, choix du dénominateur vedette et du périmètre.

## 2026-07-03 — T2 : profilage du CSV complet

- T1 validée. Consigne métier ajoutée à `donnees.md` : distinguer « école de
  [artiste] » (doute, dans Auteur) de `Ecole_pays` (nationalité).
- `src/profile_data.py` : parcours du CSV en une passe (~1 min).
- Résultats clés : 1 023 705 notices, 555 musées ; l'extrait API omet 29,5 % de
  la base ; Auteur renseigné à 82,2 % ; coordonnées à 99,8 % (carto quasi
  intégrale possible) ; périmètre peinture/dessin/sculpture/estampe = 57 % de
  la base. Détail dans `donnees.md`, rapport brut dans `data/exports/profil.txt`.
- En attente : validation T2 et choix du périmètre.

## 2026-07-03 — T1 : téléchargement et nomenclature

- Phase 0 validée par l'utilisateur ; seuils T5 confirmés ; titre adopté :
  « L'inventaire du doute ». Création de `docs/roadmap.md` (suivi par cases à cocher).
- CSV téléchargé : 1,19 Go, 67 colonnes, séparateur `|`, en-têtes identiques aux
  noms de champs de l'API. Nomenclature ODS lue (77 intitulés, étiquettes
  documentaires REF/AUTR/ATTR/PAUT/ECOL…).
- Mapping des champs documenté dans `donnees.md` : champs cœur (Auteur,
  Precisions_sur_l_auteur, Ancienne_attribution, Ecole_pays), garde-fous
  (Sujet_Represente, Titre…), contexte (Domaine multivalué `;`, coordonnees…).
- Lecture pandas validée sur échantillon. Prochaine étape : T2 (profilage complet).

## 2026-07-03 — Initialisation du projet (phase 0)

- Brief validé, plan approuvé, arborescence créée (CLAUDE.md, docs/, src/, data/).
- Exploration préalable menée via l'API du ministère (voir `donnees.md`) :
  l'écart de volumétrie entre data.gouv (> 1 M notices) et le portail du ministère
  (~700 k) est éclairci — le dataset API est un **extrait**.
- Premiers sondages encourageants : les formules d'incertitude existent bien dans
  les données et le champ auteur suit une convention structurée (qualificatifs
  entre parenthèses).
- Prochaine étape : T1 — téléchargement du CSV et de la nomenclature ODS,
  documentation du mapping des champs.
