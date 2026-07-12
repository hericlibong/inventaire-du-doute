// Textes ÉDITORIAUX de la fiche maître — propres à chaque maître, en français
// courant. Couche éditoriale du front : ces phrases sont écrites à la main, elles
// ne sont PAS des données Joconde (Joconde reste la seule source de données ;
// voir CLAUDE.md, principes de rédaction). Les chiffres, eux, ne sont jamais
// stockés ici : ils restent calculés dans le composant depuis artistes.json.
//
// Un seul champ pour l'instant :
//   bio — ligne d'identité (qui, époque), affichée sous le nom.
//
// Le paragraphe de situation ne porte plus d'angle interprétatif (décision
// 2026-07-10, 2e passe) : il ne fait que situer volume et dispersion, sans mention
// dominante ni explication du doute (portés par le graphique et les tooltips). Il
// n'a donc plus besoin de texte éditorial ici.

export const EDITORIAL = {
	'François Clouet': {
		bio: 'Portraitiste de la cour des Valois, mort en 1572.'
	},
	Rembrandt: {
		bio: 'Peintre et graveur hollandais du Siècle d’or, mort en 1669.'
	}
};

export function bioMaitre(nom) {
	return EDITORIAL[nom]?.bio ?? '';
}
