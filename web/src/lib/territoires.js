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
		codes: ['attribue', 'point_interrogation']
	},
	{
		id: 'autour',
		titre: 'Autour du maître',
		annotation: 'Son atelier, son cercle, son école — plus que sa main.',
		codes: ['atelier_de', 'entourage_de', 'ecole_de']
	},
	{
		id: 'influence',
		titre: 'Dans son influence',
		annotation: 'Son style, repris sans lui.',
		codes: ['suiveur_de', 'maniere_de', 'genre_de']
	}
];

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
