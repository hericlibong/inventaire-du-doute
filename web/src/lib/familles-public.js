// Couche de traduction PUBLIQUE des familles de formules d'attribution incertaine.
//
// Règle du projet (CLAUDE.md) : aucune catégorie technique ne s'affiche telle
// quelle dans l'interface. Chaque famille du détecteur reçoit ici de quoi
// composer un tooltip à hiérarchie visible (header / corps / valeur / mention
// type), et non plus une phrase linéaire qui répète le label, la formule et le
// sens (décision 2026-07-10, docs/decisions.md).
//
//   label       — libellé court affiché sur l'axe X (français public, pas de jargon) ;
//   header      — titre du tooltip, générique (jamais le nom du maître → stable
//                 d'une fiche à l'autre, donc comparable) ;
//   corps       — PRÉCISION très courte (lisible en une seconde). Sert la page
//                 « Comprendre les mentions » (route /echelle). Peut rester vide ;
//   definition  — DÉFINITION factuelle et stable de la mention, source canonique
//                 unique de la dernière ligne de l'infobulle du graphique
//                 (cahier des charges 2026-07-25) : neutre, identique pour tous
//                 les artistes, sans interprétation (« Attribution proposée avec
//                 réserve. » plutôt que « Sans certitude qu'il s'agisse de sa
//                 main. »). Distincte de `corps`, qui reste au service de /echelle ;
//   mention        — fonction (nom → chaîne) TOUJOURS définie : la mention type
//                    reconstruite avec le nom du maître (élision gérée), p. ex.
//                    « école de Charles Le Brun », « attribué à Ingres ». Sert au
//                    paragraphe de situation (mention dominante) ET, quand utile,
//                    au footer du tooltip. Reconstruite, pas un verbatim de la
//                    notice : d'où « Mention type » côté interface (et non
//                    « Formule Joconde »).
//   montrerMention — booléen : afficher la mention en footer du tooltip UNIQUEMENT
//                    quand elle apporte quelque chose (règle anti-répétition), soit
//                    la mention brute est elle-même le fait marquant (« Ingres (?) »),
//                    soit le terme réel du musée diffère du libellé public
//                    (« entourage » ≠ « cercle », « genre » ≠ « goût »). Partout
//                    ailleurs elle redirait le header → false.
//   citation       — forme CITABLE de la mention, écrite pour tenir en sujet de
//                    phrase dans la copie éditoriale : «&nbsp;De son école&nbsp;»
//                    est la mention la plus fréquente. Distincte de `label` (une
//                    étiquette de colonne, trop télégraphique : « son atelier »)
//                    et de `header` (un titre de tooltip). Majuscule initiale
//                    incluse ; l'abaisser pour les termes énumérés en second
//                    (« X et y sont les mentions les plus fréquentes »).
//                    Introduite le 2026-07-20 avec le bandeau éditorial.
//   couleur        — couleur STABLE de la famille, partout dans l'application
//                    (CLAUDE.md : une couleur par catégorie) : points du graphique,
//                    pastilles de la vitrine « Œuvres ». Référence un token
//                    `var(--forme-*)` : les hex vivent UNIQUEMENT dans tokens.css
//                    (grammaire « boîte de pigments », decisions.md 2026-07-11).
//
// Sens et définitions s'appuient sur docs/familles.md et docs/typologie.md.

import { nombre, deNom } from '$lib/joconde.js';

export const FAMILLE_PUBLIC = {
	attribue: {
		label: 'attribué à',
		header: 'Attribué à',
		corps: 'Sans certitude qu’il s’agisse bien de sa main.',
		definition: 'Attribution proposée avec réserve.',
		mention: (nom) => `attribué à ${nom}`,
		montrerMention: false,
		citation: 'Attribué à',
		couleur: 'var(--forme-attribue)'
	},
	point_interrogation: {
		label: 'nom (?)',
		header: 'Nom suivi d’un « ? »',
		corps: 'Doute noté sans autre précision.',
		definition: 'Nom de l’artiste indiqué avec un point d’interrogation.',
		mention: (nom) => `${nom} (?)`,
		montrerMention: true,
		citation: 'Nom suivi d’un point d’interrogation',
		couleur: 'var(--forme-point-interrogation)'
	},
	atelier_de: {
		label: 'son atelier',
		header: 'Son atelier',
		corps: 'Sorti de son atelier, pas forcément de sa main.',
		definition: 'Œuvre rattachée à l’atelier de l’artiste.',
		mention: (nom) => `atelier ${deNom(nom)}`,
		montrerMention: false,
		citation: 'De son atelier',
		couleur: 'var(--forme-atelier)'
	},
	entourage_de: {
		label: 'son cercle',
		header: 'Son cercle proche',
		corps: 'Son entourage immédiat.',
		definition: 'Œuvre rattachée à son entourage proche.',
		mention: (nom) => `entourage ${deNom(nom)}`,
		montrerMention: true,
		citation: 'De son cercle',
		couleur: 'var(--forme-entourage)'
	},
	ecole_de: {
		label: 'de son école',
		header: 'De son école',
		corps: 'Plutôt son école que sa main.',
		definition: 'Œuvre rattachée à l’école de l’artiste.',
		mention: (nom) => `école ${deNom(nom)}`,
		montrerMention: false,
		citation: 'De son école',
		couleur: 'var(--forme-ecole)'
	},
	suiveur_de: {
		label: 'un suiveur',
		header: 'Un suiveur',
		corps: 'Dans sa suite, sous son influence.',
		definition: 'Œuvre rattachée à un suiveur de l’artiste.',
		mention: (nom) => `suiveur ${deNom(nom)}`,
		montrerMention: false,
		citation: 'D’un suiveur',
		couleur: 'var(--forme-suiveur)'
	},
	maniere_de: {
		label: 'sa manière',
		header: 'À sa manière',
		corps: 'Son style, auteur inconnu.',
		definition: 'Œuvre réalisée dans un style proche du sien.',
		mention: (nom) => `à la manière ${deNom(nom)}`,
		montrerMention: false,
		citation: 'À sa manière',
		couleur: 'var(--forme-maniere)'
	},
	genre_de: {
		label: 'dans son goût',
		header: 'Dans son goût',
		corps: 'Lien de style lointain.',
		definition: 'Œuvre présentant une proximité de goût ou de style.',
		mention: (nom) => `dans le genre ${deNom(nom)}`,
		montrerMention: true,
		citation: 'Dans son goût',
		couleur: 'var(--forme-genre)'
	}
};

// Ordre d'affichage sur l'axe = distance narrative au maître (docs/typologie.md :
// niveau 1, puis niveau 2 dans l'ordre atelier → entourage → école → suiveur,
// puis niveau 3). Le même ordre pour tous les maîtres → l'axe se lit de gauche
// (presque lui) à droite (seulement son style).
export const ORDRE_FAMILLES = [
	'attribue',
	'point_interrogation',
	'atelier_de',
	'entourage_de',
	'ecole_de',
	'suiveur_de',
	'maniere_de',
	'genre_de'
];

// Valeur accordée en nombre : « 1 notice », « 2 notices ». Tout COMPTAGE public
// se dit en notices (le pipeline compte des notices Joconde, jamais un ensemble
// certifié d'œuvres distinctes — decisions.md 2026-07-19) ; « œuvre » reste
// réservé aux objets montrés individuellement (vitrine, aperçu de carte). Jamais
// de concaténation directe `${n} notices` (fauterait le singulier) : en français,
// seul 1 (et -1) est singulier ; 0 et ≥ 2 prennent le pluriel.
export function notices(n) {
	return `${nombre(n)} ${Math.abs(n) === 1 ? 'notice' : 'notices'}`;
}

// Valeur du tooltip du graphique : « 30 œuvres sur 37 — 81 % » (2026-07-23). Le
// point porte à la fois le nombre, le total d'œuvres concernées et la part — les
// trois reposent sur le même dénominateur, mais l'infobulle est le seul endroit
// où le lecteur lit le nombre exact (l'axe, lui, ne porte que le pourcentage).
// Vocabulaire public « œuvres » ici (dans l'onglet Profil) ; le pipeline compte
// des notices, ce que la page Méthode explique. `notices()` reste employée pour
// les onglets Œuvres et Musées, hors de ce palier.
function valeurGraphe(n, total) {
	const mot = Math.abs(n) === 1 ? 'œuvre' : 'œuvres';
	const pct = total ? Math.round((n / total) * 100) : 0;
	return `${nombre(n)} ${mot} sur ${nombre(total)} — ${pct} %`;
}

// Données du tooltip d'un point, prêtes à afficher (header / valeur / corps /
// mention type). `n` = nombre d'œuvres de la mention ; `total` = œuvres concernées
// de l'artiste. `corps` est la définition courte (peut être vide). `mentionType`
// vaut null quand la règle anti-répétition l'écarte.
export function tooltipFamille(code, nomMaitre, n, total) {
	const f = FAMILLE_PUBLIC[code];
	return {
		header: f.header,
		headerPastille: f.couleur, // pastille de la mention, dans la bande de tête
		// dernière ligne : la définition factuelle canonique (pas `corps`, plus
		// interprétatif et réservé à /echelle)
		corps: f.definition,
		valeur: valeurGraphe(n, total),
		mentionType: f.montrerMention ? f.mention(nomMaitre) : null
	};
}

// Résumé linéaire pour les technologies d'assistance (lecteur d'écran) : le
// tooltip HTML est visuel, on garde donc un équivalent textuel sur le point
// lui-même (aria-label), puisque le <title> SVG natif disparaît.
export function resumeFamille(code, nomMaitre, n, total) {
	const t = tooltipFamille(code, nomMaitre, n, total);
	const base = t.corps ? `${t.header} : ${t.corps} ${t.valeur}.` : `${t.header} : ${t.valeur}.`;
	return t.mentionType ? `${base} Mention type : « ${t.mentionType} ».` : base;
}
