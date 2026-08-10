# Roadmap de corrections de la demonstration

Ouverte le 2026-08-10 apres observation de la version publiee sur GitHub Pages.
Cette roadmap complete `docs/roadmap.md` sans reecrire l'historique du projet.

La demonstration reste publiee depuis `feat/profils-et-images`. Les corrections sont
integrees par lots courts, verifies sur mobile et sur ordinateur, puis poussees sur cette
branche. La fusion dans `main` reste reservee a la cloture de F6/F7.

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

- [ ] **G1 — Footer global et identite du projet**
  - nom de l'auteur ;
  - adresse electronique ;
  - portfolio ;
  - depot GitHub ;
  - source, licence et acces a la Methode.
- [ ] **G2 — Navigation principale**
  - conserver Accueil, Le projet et Explorer les artistes ;
  - deplacer Methode dans le footer sous « Methode, sources et limites » ;
  - conserver les renvois contextuels vers la Methode.
- [ ] **G3 — Sommaire mobile de la page Le projet**
  - rail lateral conserve sur ordinateur ;
  - commande compacte persistante sur mobile ;
  - section active visible et defilement fluide.
- [ ] **G4 — Liens d'action de la page Le projet**
  - actions POP harmonisees avec l'onglet Oeuvres ;
  - liens editoriaux internes conserves comme liens de lecture.
- [ ] **G5 — Accueil mobile**
  - recadrer l'image pour rendre le visage visible ;
  - replacer le texte sans masquer le sujet ;
  - conserver autant que possible l'affiche dans un ecran.

## Lot 2 - Exploration des artistes sur mobile

- [x] **M1 — Profil : graphique, legende et infobulles**
  - supprimer tout debordement horizontal ;
  - remplacer les bulles flottantes par un detail en flux sur mobile ;
  - rapprocher les commandes du graphique ;
  - rendre l'effet d'une selection visible sans aller-retour vertical.
  - verifie a 320, 390 et 430 px, sans debordement horizontal ;
  - sur mobile, le detail actif reste dans le flux au lieu de flotter hors ecran.
- [ ] **M2 — Contexte mobile de l'artiste**
  - bandeau compact quand le grand portrait sort de l'ecran ;
  - nom de l'artiste et onglets toujours accessibles ;
  - aucun grand portrait fixe qui occuperait l'ecran.
- [x] **M3 — Carte et panneau de musee**
  - panneau lateral conserve sur ordinateur ;
  - panneau immediatement visible depuis le bas de l'ecran sur mobile ;
  - fermeture, focus et retour du focus verifies.
  - feuille mobile verifiee a 320, 390 et 430 px, avec defilement interne borne.
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
