# Roadmap — L'inventaire du doute

Suivi des phases et des tâches. Mis à jour à chaque fin de tâche.
Chaque ⏸ est un point de validation utilisateur : on s'y arrête.

## Phase 0 — Initialisation ✅

- [x] Arborescence (docs/, src/, data/), .gitignore
- [x] CLAUDE.md (contexte, règles non négociables, méthode)
- [x] docs/ amorcés : journal, décisions, données, méthode-et-limites
- [x] Environnement uv + pyproject.toml, git init + premier commit
- [x] ⏸ Validation utilisateur — **validée le 2026-07-03**
  (seuils T5 confirmés, titre « L'inventaire du doute » adopté)

## Phase 1 — Test go/no-go sur la qualité des données

### T1 — Nomenclature et téléchargement ✅
- [x] Télécharger la nomenclature ODS et le CSV complet (src/download.py)
- [x] Lire la nomenclature : tableau des champs (nom CSV ↔ nom API ↔ définition)
      dans docs/donnees.md
- [x] Confirmer les champs liés à l'auteur et aux anciennes attributions
- [x] ⏸ Validation : synthèse des champs — **validée le 2026-07-03**
      (+ consigne T3 : distinguer « école de [artiste] » dans Auteur du champ
      Ecole_pays qui indique une nationalité)

### T2 — Profilage du CSV complet ✅ (en attente de validation)
- [x] Nombre réel de lignes, écart chiffré avec l'extrait API
      (1 023 705 notices ; l'API n'en expose que 70,5 %)
- [x] Taux de remplissage des champs auteur / école / ancienne attribution
- [x] Répartition par domaine (périmètre pressenti : 583 346 notices, 57 %)
- [x] ⏸ Validation : **validée le 2026-07-03** — choix du périmètre reporté à la
      fin de T3 ; consigne : taux à deux dénominateurs (toutes notices /
      notices avec Auteur non vide)

### T3 — Détecteur v0 + taux de base ✅ (en attente de validation)
- [x] src/markers.py : lexique versionné, 13 familles, 3 catégories
      (doute / copie / révision), graphies multiples, pièges intégrés
- [x] « d'après » classé à part (copie) ; « présumé » marqué suspect
- [x] Application par chunks ; champ Ancienne_attribution traité par présence
      (pas de fouille texte, pour ne pas gonfler « attribué à »)
- [x] Taux à deux dénominateurs : doute = 29 726 notices (2,90 % base /
      3,53 % avec auteur) → data/exports/comptages.csv + comptages_domaines.csv
- [x] ⏸ Validation : **validée le 2026-07-03** — taux vedette = notices avec
      auteur (base entière toujours en second) ; comptage de référence sur
      toute la base, beaux-arts en angle éditorial

### T4 — Échantillon de vérification ✅
- [x] 206 notices stratifiées par famille (rares sur-représentées, « présumé »
      et « anciennement attribué » pris en entier), graine 42
- [x] Export CSV tableur (data/exports/echantillon_verification.csv) :
      famille, champ source, extrait, contexte, lien POP testé,
      colonnes vides verdict / commentaire
- [x] Mode d'emploi : docs/verification-echantillon.md
- [x] ⏸ Validation : vérification manuelle **rendue le 2026-07-04** — 206/206
      verdicts (176 vrai / 28 faux / 2 incertain), 45 commentaires ; zéros de
      tête des références restaurés après passage par Google Sheets

### T5 — Bilan go/no-go ✅ (en attente de la décision de phase)
- [x] Réimport du CSV annoté (206/206), taux par famille et global pondéré
      (src/evaluate_sample.py → data/exports/bilan_faux_positifs.csv)
- [x] Liste des pièges confirmés (8 classes, docs/donnees.md)
- [x] Recommandation argumentée dans docs/decisions.md :
      doute 17,0 % pondéré → **REFORMULATION ciblée** (atelier de 64 %,
      école de 20 %, ? 16 % — causes identifiées et corrigeables) ;
      copie 0 %, révision 0 %
- [x] ⏸ Validation : **décision du 2026-07-04 — cycle de reformulation lancé**
      (recommandation suivie, approche « atelier » validée explicitement)

### Cycle v1 — Reformulation ciblée (T3bis/T4bis)
- [x] Lexique v1 : atelier lu comme convention (qualificatif vs nom d'auteur),
      écoles nationales inversées exclues, `(?-1996)` exclu,
      doctrine « (attribué, d'après) » implémentée
- [x] Verdicts humains T4 figés en tests automatiques
      (tests/test_markers.py, 25 cas, `uv run pytest`)
- [x] Recomptage : doute = 25 220 (2,46 % base / 2,99 % avec auteur) ;
      population « Atelier de X » écartée et chiffrée à part (1 123)
- [x] Mini-lot de contrôle : 65 lignes, familles reformulées + population
      écartée (data/exports/echantillon_recheck.csv, graine 202607)
- [x] ⏸ Vérification manuelle du mini-lot — **rendue le 2026-07-05** (65/65)
- [x] Bilan T5bis (src/evaluate_recheck.py) : doute pondéré **5,7 %
      conservateur / 3,3 % ajusté** → sous le seuil des 10 % ;
      exclusion « Atelier de X » confirmée 15/15 ; restes localisés
      (atelier 30 % famille, école 13 %) à traiter en phase 2 (typologie)
- [x] ⏸ Validation : **GO prononcé le 2026-07-05 — PHASE 1 CLOSE** ✅
      Classification des familles consignée dans docs/familles.md
      (document de référence pour la typologie et les visualisations)

## Phase 2 — Typologie et pipeline consolidé (EN COURS depuis le 2026-07-05)

### P2-T1 — Recouvrements entre catégories ✅
- [x] Venn doute / copie / révision chiffré + co-occurrences familles de doute
      → src/count_overlaps.py, data/exports/recouvrements.json
- [x] ⏸ Validation : **règles de non-addition validées le 2026-07-05**
      (chiffre vedette = doute seul ; union nommée ; Venn obligatoire ;
      doute + révision promu objet éditorial)

### P2-T2 — Typologie du doute ✅
- [x] Échelle à 3 niveaux proposée et argumentée (docs/typologie.md)
- [x] ⏸ Arbitrages rendus le 2026-07-05 : atelier restreint aux beaux-arts,
      écoles-lieux écartées (liste versionnée), « ? » au niveau 1
- [x] Lexique v2 implémenté + tests (35 cas) + recomptage complet :
      **doute = 24 507** (2,39 % base / 2,91 % avec auteur) ;
      Venn v2 : 66 420 touchées, doute + révision = 4 615

### P2-T3 — Pipeline d'exports pour la restitution ✅ (en attente de validation)
- [x] src/build_exports.py : CSV → 4 JSON légers dans data/exports/web/
      (provenance, niveaux, musees avec total versé + coords, territoires)
- [x] Provenance datée intégrée (version 2026-07-01, ETag)
- [x] Partition des niveaux vérifiée (20 014 + 3 537 + 956 = 24 507)
- [x] Deux découvertes remontées (docs/donnees.md) : monoculture Barla/Nice
      (23,6 % du doute), Alençon absent des données (109 notices, 0 doute)
- [x] ⏸ Validation : structure validée + **monoculture divulguée** (chiffre
      vedette 24 507 gardé, « hors cas Barla : 18 716 » intégré aux exports,
      drapeau musée, carte sur part_doute) — 2026-07-05

### P2-T4 — Cas racontables (EN COURS — découpé pour reprise si interruption)
Décision : Alençon = ouverture, incarnation de la limite (voir decisions.md).
Sortie visée : data/exports/web/cas.json + docs/cas.md (récit éditorial).
Sous-étapes (cocher au fil de l'eau, commit après chaque cas) :
- [x] P2-T4a — Liste des cas + schéma cas.json arrêtés (docs/cas.md)
- [x] P2-T4b — Cas « Alençon, l'absent » (via base régionale, non compté)
- [x] P2-T4c — Cas « Barla/Nice, le doute industriel » (monoculture, réel Joconde)
- [x] P2-T4d — Cas « Besançon, le vrai doute Géricault » (genre de + études Radeau)
- [x] P2-T4e — Cas « doute + révision » (l'objet le plus riche, P2-T1)
- [~] P2-T4f — cas par niveau : écarté (non nécessaire ; exemples puisables
      à la construction de l'interface)
- [x] P2-T4g — Assemblage cas.json + relecture docs/cas.md
- [x] ⏸ Validation : **4 cas validés le 2026-07-06 — PHASE 2 CLOSE** ✅

## Phase 3 — Restitution (EN COURS depuis le 2026-07-06)

Direction arrêtée (docs/decisions.md, 2026-07-06) : **application interactive
portée par la dataviz**, PAS de scrollytelling, Alençon non central. Plusieurs
dataviz d'égale importance, chacune une exploration différente. Front statique
consommant les JSON exportés (pas de serveur sauf besoin avéré). Page « méthode
et limites » au même rang que le reste.

### P3-T0 — Socle SvelteKit (fait une seule fois)

Stack arrêtée : **SvelteKit en build statique** (`adapter-static`), front isolé
dans un dossier dédié, consommant les JSON de `data/exports/web/` (décision du
2026-07-07, docs/decisions.md). Aucun serveur applicatif.

Sous-étapes (cocher au fil de l'eau) :
- [x] Échafaudage SvelteKit dans `web/` (adapter static câblé dans `vite.config.js`,
      `prerender` à la racine) ; `web/node_modules/` ignoré par git
- [x] Accès aux JSON : `npm run sync:data` (web/scripts/sync-data.js) copie
      `data/exports/web/*.json` → `web/static/data/` (servis en `/data/…`),
      dossier ignoré par git car généré (voir donnees.md)
- [x] Coquille partagée : `+layout.svelte` (en-tête, nav « une brique = une route »,
      briques à venir en placeholder), tokens de style dans `lib/styles/tokens.css`
      (couleurs des 3 niveaux)
- [x] « Hello data » : l'accueil pré-rend le chiffre vedette réel (24 507, hors
      monoculture 18 716) depuis `niveaux.json` — `npm run build` OK, HTML statique
      vérifié dans `web/build/`
- [x] ⏸ **Validation du socle le 2026-07-07** — validé sur le fond ; réserve
      indicative sur le style (« trop Claude normé », identité visuelle à
      retravailler après les dataviz, voir decisions.md + mémoire)

### P3-T1 — Entrée « par l'artiste » / « Les presque » (1re dataviz)

- [x] Liste vedette V1 : critère « maître de référence + ≥ 20 doutes (hors
      copie) », comptage canonique aligné sur markers.py (docs/decisions.md,
      2026-07-07)
- [x] Correction de repérage documentée (parenthèses vs champ entier ; écoles
      nationales ; granularité du nom-pivot) — docs/donnees.md, 2026-07-07
- [x] Désambiguïsation des familles (Fragonard = Jean-Honoré ; Bruegel/Cranach
      l'Ancien retirés car < 20 une fois le maître isolé) → **27 maîtres**
- [x] src/markers.py::famille_segment() + src/build_artistes.py →
      data/exports/web/artistes.json (par maître : propre/doute/copie,
      ventilation famille + niveau, musées, notices réelles POP)
- [ ] ⏸ Réserve utilisateur : garder 27, ou réintégrer Bruegel/Cranach comme
      « famille », ou échanger contre Jan Brueghel (~23)
- [x] Front (route `/les-presque`) : fiche « presque » complète — échelle du
      doute (composant `BarreNiveaux`), tableau des formules, copie en bande à
      part, exemples avec liens POP ; liste des 27 maîtres filtrable. Build
      statique vérifié (build/les-presque.html, données réelles pré-rendues)
- [ ] Moteur de recherche sur **toute la base** (pas seulement les 27 vedettes) :
      dépend d'un export « tous les noms + comptages » qui n'existe pas encore
      (à produire côté pipeline). Pour l'instant : filtre sur les 27 vedettes
- [~] Galaxie (`GalaxieMaitre.svelte`) construite puis **ABANDONNÉE dans cette vue**
      le 2026-07-08 (voir decisions.md) : encodage « 1 bulle = 1 famille » → schéma
      moléculaire, pas une constellation ; n'apporte rien qu'une barre ne montre
      mieux. Réserve : « vraie constellation » (1 point = 1 œuvre) à retenter un
      jour sur **branche séparée**, hors de cette vue
- [ ] Intro/onboarding du site à revoir au bilan : un visiteur lambda ne comprend
      pas encore l'objectif ni le fonctionnement (voir mémoire feedback)
- [x] Garde-fou éditorial en place : chapô « voici comment les musées nuancent
      autour d'un nom », copie isolée comme « copies assumées », aucun « trésor caché »

#### Réorientation « Les presque » — trois angles (décision 2026-07-08)

Cible : par maître, trois vues complémentaires — **le quoi / le combien / le où**.
Ordre de construction retenu : **barres → carte** (détail conservé tel quel).

- [x] **Détail** — *le quoi* (existant) : formules, exemples POP, copies à part.
      Conservé en l'état ; labels trop techniques à reformuler **plus tard** (non
      prioritaire)
- [x] **① Barres horizontales** — livré puis **remplacé par un nuage de points**
      le 2026-07-08 : les barres, normalisées à la largeur du conteneur et
      n'affichant que les familles présentes, ne permettaient ni comparaison
      entre maîtres ni lecture des volumes réels
- [x] **①bis Nuage de points à grille fixe** — *le combien, comparable* : axe X =
      8 familles de doute (ordre canonique, « présumé » absent des 27 retiré),
      **mêmes colonnes pour tous** ; axe Y = volume, **plafond commun 240**
      (calculé côté front = max famille sur les 27, « école de » Le Brun) ;
      1 point/famille à la hauteur du volume, taille légèrement croissante
      (la hauteur porte la mesure), couleur par famille groupée par niveau,
      graduations 60/120/180/240, échelle linéaire, survol = compte exact.
      `NuageFamilles.svelte`, bascule « Nuage / Détail ». Aucune donnée nouvelle.
      Build statique vérifié
- [ ] **Palier données** : enrichir `src/build_artistes.py` pour exporter, par
      maître, les **musées détenteurs d'œuvres douteuses + comptes** (le champ
      `musees` actuel confond ferme/copie/doute — inexploitable pour la carte) ;
      idéalement ventilation famille/niveau par musée
- [ ] **② Carte par maître** — *le où* : **D3-geo auto-hébergé** (décidé
      2026-07-08), GeoJSON France + départements en open data dans `static/`,
      **aucune tuile externe**, pré-rendable. 1 point = 1 **musée détenteur**
      (grain honnête : l'œuvre est localisée par son musée), taille ∝ nb d'œuvres
      douteuses de ce maître ; survol = titre/musée/formule ; zoom léger (d3-zoom).
      Change à chaque maître, jamais de carte globale. Coords musées à 98,7 %
      (7/555 sans coord → note « N non localisées »)
- [ ] Caveat page méthode : taille d'un point = nb d'œuvres douteuses **de ce
      maître** dans ce musée, **jamais** une comparaison de catalogage entre musées

### Briques suivantes (ordre à confirmer)

- [ ] Le décodeur de l'échelle du doute (clé de lecture, consomme niveaux.json)
- [ ] Les révisions « on a cru → aujourd'hui » (Ancienne_attribution)
- [ ] La carte, qualifiée (part_doute, jamais brut ; monoculture signalée) —
      chapitre, pas socle (docs/phase3-options.md)
- [ ] Page « méthode et limites »
