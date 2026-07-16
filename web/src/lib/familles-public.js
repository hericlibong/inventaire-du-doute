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
//   corps       — PRÉCISION très courte (lisible en une seconde), pas une
//                 définition complète : le tooltip n'est pas un dictionnaire des
//                 labels, sinon le lecteur relit huit fois la même notice. Peut
//                 rester vide si le header se suffit à lui-même ;
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
		mention: (nom) => `attribué à ${nom}`,
		montrerMention: false,
		couleur: 'var(--forme-attribue)'
	},
	point_interrogation: {
		label: 'nom (?)',
		header: 'Nom suivi d’un « ? »',
		corps: 'Doute noté sans autre précision.',
		mention: (nom) => `${nom} (?)`,
		montrerMention: true,
		couleur: 'var(--forme-point-interrogation)'
	},
	atelier_de: {
		label: 'son atelier',
		header: 'Son atelier',
		corps: 'Sorti de son atelier, pas forcément de sa main.',
		mention: (nom) => `atelier ${deNom(nom)}`,
		montrerMention: false,
		couleur: 'var(--forme-atelier)'
	},
	entourage_de: {
		label: 'son cercle',
		header: 'Son cercle proche',
		corps: 'Son entourage immédiat.',
		mention: (nom) => `entourage ${deNom(nom)}`,
		montrerMention: true,
		couleur: 'var(--forme-entourage)'
	},
	ecole_de: {
		label: 'de son école',
		header: 'De son école',
		corps: 'Plutôt son école que sa main.',
		mention: (nom) => `école ${deNom(nom)}`,
		montrerMention: false,
		couleur: 'var(--forme-ecole)'
	},
	suiveur_de: {
		label: 'un suiveur',
		header: 'Un suiveur',
		corps: 'Dans sa suite, sous son influence.',
		mention: (nom) => `suiveur ${deNom(nom)}`,
		montrerMention: false,
		couleur: 'var(--forme-suiveur)'
	},
	maniere_de: {
		label: 'sa manière',
		header: 'À sa manière',
		corps: 'Son style, auteur inconnu.',
		mention: (nom) => `à la manière ${deNom(nom)}`,
		montrerMention: false,
		couleur: 'var(--forme-maniere)'
	},
	genre_de: {
		label: 'dans son goût',
		header: 'Dans son goût',
		corps: 'Lien de style lointain.',
		mention: (nom) => `dans le genre ${deNom(nom)}`,
		montrerMention: true,
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

// Valeur accordée en nombre : « 1 œuvre », « 2 œuvres ». Jamais de concaténation
// directe `${n} œuvres` (fauterait le singulier). En français, seul 1 (et -1) est
// singulier ; 0 et ≥ 2 prennent le pluriel.
export function oeuvres(n) {
	return `${nombre(n)} ${Math.abs(n) === 1 ? 'œuvre' : 'œuvres'}`;
}

// Données du tooltip d'un point, prêtes à afficher (header / corps / valeur /
// mention type). `n` est le nombre BRUT d'œuvres (entier), accordé ici. `corps`
// est une précision courte (peut être vide). `mentionType` vaut null quand la
// règle anti-répétition l'écarte.
export function tooltipFamille(code, nomMaitre, n) {
	const f = FAMILLE_PUBLIC[code];
	return {
		header: f.header,
		headerPastille: f.couleur, // pastille de la mention, dans la bande de tête
		corps: f.corps,
		valeur: oeuvres(n),
		mentionType: f.montrerMention ? f.mention(nomMaitre) : null
	};
}

// Résumé linéaire pour les technologies d'assistance (lecteur d'écran) : le
// tooltip HTML est visuel, on garde donc un équivalent textuel sur le point
// lui-même (aria-label), puisque le <title> SVG natif disparaît.
export function resumeFamille(code, nomMaitre, n) {
	const t = tooltipFamille(code, nomMaitre, n);
	const base = t.corps ? `${t.header} : ${t.corps} ${t.valeur}.` : `${t.header} : ${t.valeur}.`;
	return t.mentionType ? `${base} Mention type : « ${t.mentionType} ».` : base;
}
