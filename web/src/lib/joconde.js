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

// « 1 œuvre » / « 310 œuvres » : même règle d'accord, pour les libellés qui
// comptent des œuvres côté lecteur (onglet Œuvres). Le vocabulaire « notice »
// reste réservé à la méthode et aux données (É1, 2026-08-03).
export function oeuvres(n) {
	return `${nombre(n)} ${Math.abs(n) === 1 ? 'œuvre' : 'œuvres'}`;
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

// Nombre écrit en toutes lettres, pour le corps de texte (CLAUDE.md : « écrire
// les chiffres en français, pas en notation d'analyste »). Une table figée allait
// de vingt-quatre à trente : elle est tombée en panne le jour où la liste des
// maîtres est passée à soixante-trois. Couvre 0 à 99, repli sur le chiffre
// au-delà — un effectif à trois chiffres ne se raconterait plus en lettres.
const PETITS = [
	'zéro', 'un', 'deux', 'trois', 'quatre', 'cinq', 'six', 'sept', 'huit', 'neuf',
	'dix', 'onze', 'douze', 'treize', 'quatorze', 'quinze', 'seize',
	'dix-sept', 'dix-huit', 'dix-neuf'
];
const DIZAINES = {
	20: 'vingt', 30: 'trente', 40: 'quarante',
	50: 'cinquante', 60: 'soixante', 80: 'quatre-vingt'
};

export function enLettres(n) {
	if (!Number.isInteger(n) || n < 0 || n > 99) return String(n);
	if (n < 20) return PETITS[n];
	// soixante-dix et quatre-vingt-dix se construisent sur soixante et quatre-vingt
	const dizaine = Math.floor(n / 10) * 10;
	const base = dizaine === 70 || dizaine === 90 ? dizaine - 10 : dizaine;
	const reste = n - base;
	if (reste === 0) return base === 80 ? 'quatre-vingts' : DIZAINES[base];
	// « vingt et un », « soixante et onze » — mais « quatre-vingt-un »
	if ((reste === 1 || reste === 11) && base !== 80 && DIZAINES[base]) {
		if (reste === 1) return `${DIZAINES[base]} et un`;
		if (base === 60) return `${DIZAINES[base]} et onze`;
	}
	return `${DIZAINES[base]}-${PETITS[reste]}`;
}

// Même chose, première lettre en capitale (début de phrase).
export function enLettresCap(n) {
	const mot = enLettres(n);
	return mot.charAt(0).toUpperCase() + mot.slice(1);
}
