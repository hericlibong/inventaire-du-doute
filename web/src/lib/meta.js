// Métadonnées publiques du site — SOURCE UNIQUE.
//
// Un même texte alimente le `<title>`, la `meta description` et les balises de
// partage (Open Graph, Twitter). Les dupliquer dans chaque page reviendrait à
// laisser deux versions d'une même phrase diverger au premier ajustement.
//
// L'URL publique n'est écrite QU'ICI. Elle sert à trois choses qui exigent une
// adresse absolue — `og:url`, `og:image` et le sitemap — parce qu'un partage se
// fait hors du site : un chemin relatif n'y veut rien dire.
//
// Publication GitHub Pages, en Project Page, dans un sous-répertoire du domaine
// github.io. Cette adresse reste celle de la publication depuis main.
export const SITE_URL = 'https://hericlibong.github.io/inventaire-du-doute';

export const SITE_NOM = 'L’inventaire du doute';

// Image de partage : 1200 × 630, l'illustration de couverture recadrée, avec le
// titre et le volume. Chemin relatif ici, absolu à l'usage (voir `absolu`).
export const OG_IMAGE = '/cover/partage.jpg';

// Une entrée par route publique. `titre` est le <title> complet ; `descr` sert
// à la fois de meta description et de description de partage.
//
// Les effectifs ne sont PAS écrits ici : ils viennent des données, et les pages
// qui en citent un le passent en argument (voir `metaAccueil`).
export const META = {
	projet: {
		titre: 'Le projet — L’inventaire du doute, volume 1',
		descr:
			'Dans les musées de France, un nom sous une œuvre n’est pas toujours une certitude. ' +
			'Ce volume lit les formulations prudentes que les musées publient eux-mêmes.'
	},
	artistes: {
		titre: 'Explorer les artistes — L’inventaire du doute',
		descr:
			'Les artistes du volume : les œuvres associées à leur nom avec une réserve ' +
			'd’attribution, les formulations employées par les musées, et les lieux de conservation.'
	},
	methode: {
		titre: 'Méthode et limites — L’inventaire du doute',
		descr:
			'Comment les notices sont repérées, ce qui est compté, comment la liste des artistes ' +
			'a été établie, et ce que ces chiffres ne disent pas.'
	}
};

// L'accueil cite l'effectif du volume : il est lu dans les données, jamais figé.
export function metaAccueil(nbArtistes) {
	return {
		titre: 'L’inventaire du doute — Volume 1 : Autour des maîtres',
		descr:
			'Le nom d’un artiste peut accompagner une œuvre sans que le musée la lui attribue ' +
			`directement. Ce volume explore ces liens autour de ${nbArtistes} artistes, ` +
			'à partir de la base Joconde.'
	};
}

// Chemin du site → URL absolue, pour les seules balises qui l'exigent.
export const absolu = (chemin) => `${SITE_URL}${chemin}`;
