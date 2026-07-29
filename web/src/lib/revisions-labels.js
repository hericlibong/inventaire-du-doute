// Source de vérité UNIQUE, côté front, pour tout ce que revisions.json ne porte
// pas déjà : couleur de catégorie, appartenance aux deux groupes éditoriaux,
// phrase d'introduction par filtre (onglet « Les œuvres »), phrase de récit par
// carte. Le NOM de chaque catégorie reste porté par les données
// (`libelles_categorie` dans revisions.json, généré par src/revisions_classify.py)
// : on ne le duplique pas ici, pour éviter les variantes.
//
// Règles respectées (voir docs/decisions.md 2026-07-14 quinquies) :
// - pas de logique rouge/vert ni de hiérarchie morale entre catégories ;
// - deux familles de couleurs cohérentes autour de l'accent violet : la famille
//   violette pour les passages les plus lisibles, une famille chaude et sobre
//   (ocre/taupe) pour les trajectoires plus complexes. La couleur distingue,
//   elle ne juge pas.

// Ordre d'affichage dans l'anneau : groupe 1 (4) puis groupe 2 (3), pour que les
// deux familles éditoriales se regroupent visuellement sur la couronne.
export const ORDRE = [
	'autre_nom',
	'anonyme',
	'copie',
	'meme_nom',
	'mineur',
	'plusieurs_noms',
	'deja_copie'
];

// Couleur + groupe + textes éditoriaux, par code de catégorie.
export const CATEGORIES = {
	autre_nom: {
		groupe: 'lisibles',
		couleur: '#4f4270',
		introFiltre:
			'La notice conserve deux noms différents : celui autrefois associé à l’œuvre et celui indiqué aujourd’hui.',
		phraseCarte: 'Un autre nom est désormais indiqué.'
	},
	anonyme: {
		groupe: 'lisibles',
		couleur: '#6f5f92',
		introFiltre:
			'Une ancienne attribution nominative laisse place à une formulation qui ne retient plus de nom d’auteur.',
		phraseCarte: 'L’ancien nom n’est plus retenu dans l’attribution actuelle.'
	},
	copie: {
		groupe: 'lisibles',
		couleur: '#9187ac',
		introFiltre:
			'Le lien avec un artiste demeure, mais sa nature change : l’œuvre est désormais décrite comme copie, « d’après » ou selon une formulation voisine.',
		phraseCarte: 'L’œuvre est désormais décrite comme une copie ou une œuvre d’après.'
	},
	meme_nom: {
		groupe: 'lisibles',
		couleur: '#bcb4cd',
		introFiltre:
			'Le nom reste présent, mais l’attribution actuelle introduit une distance ou une incertitude.',
		phraseCarte: 'Le nom demeure, mais avec une formulation plus prudente.'
	},
	mineur: {
		groupe: 'complexes',
		couleur: '#9a7b4f',
		introFiltre: '',
		phraseCarte: ''
	},
	plusieurs_noms: {
		groupe: 'complexes',
		couleur: '#b89b6d',
		introFiltre: '',
		phraseCarte: ''
	},
	deja_copie: {
		groupe: 'complexes',
		couleur: '#d3c2a1',
		introFiltre: '',
		phraseCarte: ''
	}
};

// Les deux groupes éditoriaux (séparation de lecture uniquement : les 7
// catégories restent dans le même anneau).
export const GROUPES = [
	{ id: 'lisibles', titre: 'Les passages les plus lisibles', codes: ['autre_nom', 'anonyme', 'copie', 'meme_nom'] },
	{ id: 'complexes', titre: 'Les trajectoires plus complexes', codes: ['mineur', 'plusieurs_noms', 'deja_copie'] }
];

// Pseudo-catégorie transversale de la galerie : les cas où le mouvement va de
// l'anonymat vers un nom (champ `cas.inverse`). N'entre pas dans la partition
// des 7 (ce n'est pas une 8e part du tout), d'où sa définition séparée. Le
// libellé décrit le contenu de la notice, sans affirmer que le véritable auteur
// a été retrouvé.
export const INVERSE = {
	code: 'inverse',
	libelle: 'De l’anonymat à une attribution nominative',
	couleur: '#175c50',
	introFiltre:
		'Le mouvement peut aussi aller dans l’autre sens : une œuvre autrefois présentée comme anonyme possède aujourd’hui une attribution nominative, parfois encore prudente.',
	phraseCarte: 'Une attribution nominative remplace une ancienne mention anonyme.'
};

// Couleur d'une catégorie (fallback neutre si code inconnu).
export function couleurCategorie(code) {
	if (code === INVERSE.code) return INVERSE.couleur;
	return CATEGORIES[code]?.couleur ?? 'var(--couleur-revision)';
}
