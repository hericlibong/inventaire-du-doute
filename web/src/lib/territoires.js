// Les trois territoires de la « distance à la main du maître » — primitive du
// projet (architecture-editoriale.md §5). SOURCE UNIQUE du regroupement des huit
// mentions en trois zones de proximité, avec un titre et une courte annotation
// éditoriale par zone. Réutilisée par le graphique (onglet Profil) et par la future
// rubrique « Comprendre les mentions ».
//
// On ne redéfinit AUCUN libellé de mention ici : les labels et couleurs restent
// dans familles-public.js (couche publique unique). Ce module ne fait que
// regrouper des codes de familles et porter le texte éditorial des zones.

import { ORDRE_FAMILLES } from '$lib/familles-public.js';

export const TERRITOIRES = [
	{
		id: 'plus-pres',
		titre: 'Au plus près',
		// Annotations factuelles, courtes : elles disent le DEGRÉ de distance, sans
		// interpréter l'œuvre (on lit ce que les musées écrivent).
		annotation: 'Sa main est probable, sans certitude.',
		codes: ['attribue', 'point_interrogation'],
		concentration: () =>
			'Les musées les rattachent surtout au maître lui-même, avec une attribution néanmoins prudente.',
		nominal: 'le maître lui-même'
	},
	{
		id: 'autour',
		titre: 'Autour du maître',
		annotation: 'Son atelier, son cercle, son école — plus que sa main.',
		codes: ['atelier_de', 'entourage_de', 'ecole_de'],
		// Ici la précision est concrète : « à son atelier », « à son cercle », « à son
		// école ». La citation publique arrive sous la forme « de son école » — on
		// retire l'article, la phrase apporte déjà sa préposition.
		concentration: (precision) =>
			`Les musées les rattachent surtout à son entourage, principalement à ${precision.replace(/^de /, '')}.`,
		nominal: 'son entourage'
	},
	{
		id: 'influence',
		titre: 'Dans son influence',
		annotation: 'Son style, repris sans lui.',
		codes: ['suiveur_de', 'maniere_de', 'genre_de'],
		// Le lien est un lien de style : on cite la mention employée, telle qu'elle
		// s'écrit, plutôt que de gloser une « distance ».
		concentration: (precision) =>
			`Les musées les rattachent surtout à son influence, principalement avec la mention « ${precision} ».`,
		nominal: 'son influence'
	}
];

// Phrase de lecture placée sous le titre du graphique (onglet Profil). Elle dit,
// en mots ordinaires, ce que le lecteur verrait s'il savait lire le graphe : à quoi
// les musées rattachent ces œuvres — au maître lui-même, à son entourage, à son
// influence. La fiche, au-dessus, donne la mention la plus fréquente ; les deux ne
// doivent pas se répéter mot pour mot.
//
// Formulations FIXÉES par l'utilisateur (2026-07-20) : on n'en invente pas d'autres.
// Vocabulaire proscrit : « corpus », « profil d'attribution », « distribution »,
// « domine », « nettement », « doute ».
//
// Règles, appliquées dans cet ordre (seuils inchangés) :
//   1. un territoire ≥ 60 % des notices → c'est le territoire principal ;
//   2. sinon, les deux premiers séparés de moins de 5 points → les œuvres se partagent ;
//   3. sinon → aucune tendance ne s'impose.
//
// `parNotices` : objet code de mention → nombre de notices (les huit familles).
// `citationMention` : fonction (code de mention) → mention publique en bas de casse
// (« de son école », « à sa manière »), fournie par l'appelant depuis la couche de
// libellés publics — aucun libellé n'est réécrit ici.
export function lectureProfil(parNotices, citationMention) {
	const zones = TERRITOIRES.map((t) => ({
		t,
		notices: t.codes.reduce((s, c) => s + (parNotices[c] ?? 0), 0)
	}));
	const total = zones.reduce((s, z) => s + z.notices, 0);
	if (!total) return null;

	const classees = zones.slice().sort((a, b) => b.notices - a.notices);
	const part = (z) => (z.notices / total) * 100;

	if (part(classees[0]) >= 60) {
		// Mention la plus fréquente À L'INTÉRIEUR du territoire principal (pas la
		// dominante globale : elle peut appartenir à un autre territoire).
		const tete = classees[0].t.codes
			.slice()
			.sort((a, b) => (parNotices[b] ?? 0) - (parNotices[a] ?? 0))[0];
		return classees[0].t.concentration(citationMention(tete));
	}

	if (part(classees[0]) - part(classees[1]) < 5) {
		return `Les œuvres se partagent surtout entre ${classees[0].t.nominal} et ${classees[1].t.nominal}.`;
	}

	return 'Les musées utilisent plusieurs formes de rapprochement, sans qu’une seule ne s’impose.';
}

// Garde-fou : les trois territoires doivent couvrir EXACTEMENT les huit mentions de
// familles-public.js, dans le même ordre (l'axe du graphe et ses bandes s'appuient
// sur cette correspondance). Un simple avertissement en dev si l'un dérive.
const _aplat = TERRITOIRES.flatMap((t) => t.codes);
if (import.meta.env.DEV && _aplat.join('|') !== ORDRE_FAMILLES.join('|')) {
	console.warn(
		'[territoires] désaligné de ORDRE_FAMILLES :',
		_aplat,
		'≠',
		ORDRE_FAMILLES
	);
}

// Bornes de colonnes d'un territoire dans un axe ordonné (défaut : ORDRE_FAMILLES).
// Rend les index de première et dernière colonne du territoire — les codes étant
// contigus et dans l'ordre, la bande couvre `[debut, fin]`.
export function indicesTerritoire(t, ordre = ORDRE_FAMILLES) {
	const idx = t.codes.map((c) => ordre.indexOf(c));
	return { debut: Math.min(...idx), fin: Math.max(...idx) };
}
