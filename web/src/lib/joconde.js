// Helpers partagés autour de la base Joconde, réutilisables par toutes les briques.

// Notice publique sur POP (plateforme ouverte du patrimoine).
// Même gabarit que src/config.py (URL_NOTICE_POP), source de vérité côté back.
export const lienPop = (reference) => `https://pop.culture.gouv.fr/notice/joconde/${reference}`;

// L'échelle du doute à 3 niveaux (docs/typologie.md), du plus proche au plus
// lointain de l'auteur. La couleur pointe vers un token CSS (lib/styles/tokens.css).
export const NIVEAUX = [
	{ n: 1, libelle: 'Presque lui', variable: '--niveau-1', sens: "l'attribution est probable mais non certaine" },
	{ n: 2, libelle: 'Autour de lui', variable: '--niveau-2', sens: 'son atelier, son école, son entourage' },
	{ n: 3, libelle: 'Son style, sans lui', variable: '--niveau-3', sens: 'sa manière, son genre, un suiveur' }
];

// Entier en français (espace insécable comme séparateur de milliers).
export const nombre = (v) => v.toLocaleString('fr-FR');

// Élision de « de » devant un nom à initiale vocalique : « sous le nom de Le Brun »
// mais « sous le nom d'Ingres ». On n'élide que devant une voyelle — le « h »
// français est ambigu (h aspiré : « de Hals »), on le laisse donc en « de ».
export function deNom(nom) {
	// Contraction de l'article : « Le Tintoret » → « du Tintoret » (corrigé le
	// 2026-07-20 — on lisait « entourage de Le Tintoret » dans les infobulles).
	// Concerne Le Primatice, Le Tintoret, Le Corrège ; « Charles Le Brun » n'est pas
	// touché, l'article n'y est pas en tête.
	if (nom.startsWith('Le ')) return `du ${nom.slice(3)}`;
	return /^[aeiouyàâäéèêëîïôöùûü]/i.test(nom) ? `d’${nom}` : `de ${nom}`;
}

// Même contraction pour « à » : « rattachent ces œuvres au Primatice », et non
// « à Le Primatice ». Pas d'élision devant voyelle ici (« à Ingres » est correct).
export function aNom(nom) {
	return nom.startsWith('Le ') ? `au ${nom.slice(3)}` : `à ${nom}`;
}

// « 1 musée » / « 64 musées » : accord en nombre (jamais de `${n} musées` brut).
export function musees(n) {
	return `${nombre(n)} ${Math.abs(n) === 1 ? 'musée' : 'musées'}`;
}

// Un ratio (en %) raconté en français, pour le récit : « plus de la moitié »
// vaut mieux que « 59 % » quand la lecture prime. Le chiffre exact reste donné
// à côté (nombres bruts, survol, vue Détail) — cette phrase n'est qu'une glose.
export function fractionEnMots(part) {
	const seuils = [
		[62, 'près des deux tiers'],
		[55, 'plus de la moitié'],
		[47, 'près de la moitié'],
		[40, 'plus d’un tiers'],
		[30, 'environ un tiers'],
		[26, 'plus d’une sur quatre'],
		[22, 'un peu plus d’une sur cinq'],
		[18, 'environ une sur cinq'],
		[14, 'près d’une sur six'],
		[11, 'environ une sur huit'],
		[8, 'environ une sur dix'],
		[0, 'une petite part']
	];
	return (seuils.find(([s]) => part >= s) ?? seuils.at(-1))[1];
}

// Libellé de famille de doute lisible par le public. « atelier (qualificatif,
// beaux-arts) » est un nom de code interne (voir docs/familles.md) : on le
// raccourcit à l'affichage. Les autres libellés restent inchangés pour l'instant
// (leur reformulation narrative est un chantier distinct).
export function libelleFamillePublic(libelle) {
	if (libelle && libelle.startsWith('atelier (qualificatif')) return 'atelier de';
	return libelle;
}

// Nom de licence en français pour les crédits d'image.
export function licenceEnFrancais(licence) {
	const table = { 'Public domain': 'domaine public', CC0: 'CC0' };
	return table[licence] ?? licence;
}
