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
