# Roadmap de corrections de la demonstration

Ouverte le 2026-08-10 apres observation de la version publiee sur GitHub Pages.
Cette roadmap complete `docs/roadmap.md` sans reecrire l'historique du projet.

La demonstration reste publiee depuis `feat/profils-et-images`. Les corrections sont
integrees par lots courts, verifies sur mobile et sur ordinateur, puis poussees sur cette
branche. La fusion dans `main` reste reservee a la cloture de F6/F7.

## Reprise visuelle du 2026-08-10

Les premiers correctifs mobiles ont resolu des symptomes fonctionnels, mais M1 et G5 ont
ete valides trop tot : la legende du profil a perdu sa composition editoriale et le
recadrage de l'accueil n'a pas rendu le sujet plus lisible. M3 fonctionne, mais son panneau
est disproportionne par rapport a la carte. Ces trois points sont rouverts.

Regle de cette reprise : travail local, captures avant/apres a 390 et 430 px, validation
visuelle explicite, puis seulement commit et push. Une verification technique ne vaut pas
a elle seule validation graphique.

- [x] **R1 — Restaurer le recit du graphique mobile**
  - retirer la grille de grandes commandes ajoutee au-dessus du graphique ;
  - restaurer les trois territoires et leur hierarchie visuelle ;
  - conserver l'interaction partagee entre points et mentions ;
  - rapprocher la legende sans la transformer en interface de tableau de bord.
  - Etat : implemente localement ; captures controlees a 320, 390 et 430 px ;
    les trois territoires sont maintenant alignes sur une seule ligne et leur
    hauteur est reduite ; rendu valide par l'utilisateur.
- [x] **R2 — Replacer l'infobulle dans le graphique**
  - conserver le lien spatial avec le point selectionne ;
  - adapter sa largeur et sa position aux bords du graphique ;
  - ne jamais la remplacer par un detail eloigne dans le flux mobile.
  - Etat : implemente localement ; quatre positions de point controlees aux trois
    largeurs, sans debordement ; rendu valide par l'utilisateur.
- [x] **R3 — Reproportionner le panneau mobile de la carte**
  - abandonner le panneau inferieur sur mobile ;
  - conserver le panneau lateral actuel sur ordinateur ;
  - ouvrir au clic une bulle compacte attachee au point sur ecran etroit ;
  - maintenir le point et toute la bulle dans la zone visible ;
  - verifier les cas a une oeuvre et a plusieurs oeuvres.
  - Etat : implemente localement ; panneau lateral desktop conserve ; bulle mobile
    controlee dans les deux cas a 320, 390 et 430 px, point et bulle visibles ;
    rendu valide par l'utilisateur.
- [x] **R4 — Reprendre la couverture mobile**
  - supprimer l'assombrissement ajoute sans gain de lisibilite ;
  - rendre le sujet reellement visible sans masquer le texte ;
  - supprimer l'espace blanc avant le footer.
  - Etat : composition locale validee par l'utilisateur ; ne plus modifier l'accueil.
- [x] **R5 — Alleger le footer**
  - conserver l'identite, le contact, le site web, GitHub et la Methode ;
  - retirer le paragraphe de source deja developpe dans la Methode.
  - Etat : paragraphe de source retire ; signature resserree en « Auteur : Heric
    Libong », adresse corrigee, contacts accompagnes de pictogrammes discrets et
    lien Methode isole sur la ligne suivante ; controle a 390 et 1440 px.

Verification locale de la reprise : build statique OK, 306 tests Python et tests
front au vert. Captures produites a 320, 390, 430 et 1440 px. Aucun debordement
horizontal ; le panneau lateral de la carte reste reserve a l'ordinateur.

## Principes

- Le coeur du chantier est une **adaptation mobile specifique**, pas une simple reduction
  de la composition desktop.
- Les comportements desktop qui fonctionnent sont conserves.
- Aucun dispositif technique n'est presente comme une protection contre les captures
  d'ecran : un site web public ne peut pas les empecher de facon fiable.
- Aucune reproduction n'est publiee sans licence ouverte explicite ou autorisation.
- La recherche d'images et les demandes d'autorisation avancent en parallele ; elles ne
  bloquent pas les corrections d'interface.

## Lot 1 - Structure generale du site

- [x] **G1 — Footer global et identite du projet**
  - nom de l'auteur ;
  - adresse electronique ;
  - site web ;
  - depot GitHub ;
  - source, licence et acces a la Methode.
- [x] **G2 — Navigation principale**
  - conserver Accueil, Le projet et Explorer les artistes ;
  - deplacer Methode dans le footer sous « Methode, sources et limites » ;
  - conserver les renvois contextuels vers la Methode.
- [x] **G3 — Sommaire mobile de la page Le projet**
  - rail lateral conserve sur ordinateur ;
  - commande compacte persistante sur mobile ;
  - section active visible et defilement fluide.
  - composant commun applique aussi a la Methode, sans second systeme d'ancres.
- [x] **G4 — Liens d'action de la page Le projet**
  - actions POP harmonisees avec l'onglet Oeuvres ;
  - liens editoriaux internes conserves comme liens de lecture.
- [x] **G5 — Accueil mobile — resolu par R4**
  - recadrer l'image pour rendre le visage visible ;
  - replacer le texte sans masquer le sujet ;
  - conserver autant que possible l'affiche dans un ecran.
  - cadrage verifie a 320, 390 et 430 px ; la version desktop reste inchangee.
- [x] **G6 — Expliquer les usages de l'inventaire**
  - ajouter une section apres le glossaire et avant l'entree dans l'exploration ;
  - presenter cinq usages concrets sous forme de liste editoriale ;
  - rappeler que l'incertitude d'attribution n'enleve rien a la valeur de l'oeuvre ;
  - ajouter l'ancre aux sommaires desktop et mobile.
  - rendu controle a 390 et 1440 px ; ancre, section active et lecture mobile verifies.

## Lot 2 - Exploration des artistes sur mobile

- [x] **M1 — Profil : graphique, legende et infobulles — resolu par R1/R2**
  - supprimer tout debordement horizontal ;
  - conserver l'infobulle attachee au point et la borner au graphique sur mobile ;
  - rapprocher les commandes du graphique ;
  - rendre l'effet d'une selection visible sans aller-retour vertical.
  - verifie a 320, 390 et 430 px, sans debordement horizontal ;
  - sur mobile, l'infobulle reste liee au point sans sortir de l'ecran.
- [ ] **M2 — Contexte mobile de l'artiste**
  - bandeau compact quand le grand portrait sort de l'ecran ;
  - nom de l'artiste et onglets toujours accessibles ;
  - aucun grand portrait fixe qui occuperait l'ecran.
- [x] **M3 — Carte et panneau de musee — resolu par R3**
  - panneau lateral conserve sur ordinateur ;
  - bulle compacte attachee au point selectionne sur mobile ;
  - fermeture, focus et retour du focus verifies.
  - bulle mobile verifiee a 320, 390 et 430 px, avec contenu borne.
- [ ] **M4 — Oeuvres sans reproduction**
  - composition textuelle compacte sur mobile ;
  - oeuvres illustrees prioritaires ;
  - filtres, pagination et lightbox verifies.
- [x] **M5 — Changement d'artiste**
  - retour au debut de la fiche ou de l'onglet actif ;
  - aucune position verticale heritee de l'artiste precedent.
  - sur mobile, la nouvelle fiche recoit le focus et la vue active est conservee ;
  - la reduction des animations supprime le defilement anime.

## Images - chantier parallele

- [ ] Poursuivre les demandes d'autorisation pour les images POP.
- [ ] Rechercher des correspondances exactes dans les collections ouvertes.
- [ ] Conserver la preuve de correspondance, la source, le credit et la licence.
- [ ] Ne pas utiliser le caractere non lucratif comme justification de reutilisation.

## Verification finale

- [ ] Largeurs 320, 360, 390 et 430 px.
- [ ] Tablette, ordinateur portable et grand ecran.
- [ ] Souris, toucher, clavier, focus et reduction des animations.
- [ ] Aucun chevauchement entre header, sommaire, bandeau artiste et panneaux.
- [ ] Routes directes, redirections et ressources sous le chemin GitHub Pages.
- [ ] Relecture des droits, credits et limites publiees.
- [ ] Reprise de F6 puis F7 dans `docs/roadmap.md`.
