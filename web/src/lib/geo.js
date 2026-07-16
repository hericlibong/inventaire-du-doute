// Briques géographiques partagées de la carte par maître.
// Périmètre volontairement minimal (decisions.md 2026-07-12) : projeter des
// couples lat/lon sur le fond des régions métropolitaines, et savoir dire si un
// point tombe dans ce cadre ou non. Aucune donnée n'est portée par le fond :
// c'est une illustration (source IGN via france-geojson), jamais un comptage.

import { geoConicConformal, geoPath } from 'd3-geo';

// Fenêtre lat/lon de la France métropolitaine (Corse comprise), en degrés.
// Sert À LA FOIS à décider ce qu'on projette et à repérer le hors-cadre
// (util partagé : une seule vérité, jamais deux seuils qui divergent).
// L'outre-mer (La Réunion, lon ≈ 55) tombe naturellement hors de ces bornes :
// on ne le projette pas, mais il reste compté par ailleurs.
export const BORNES_METROPOLE = {
	latMin: 41,
	latMax: 51.6,
	lonMin: -5.5,
	lonMax: 9.8
};

// Un musée est-il projetable sur le fond métropolitain ? Faux si les
// coordonnées manquent ou tombent hors de la fenêtre (outre-mer, étranger).
export function estProjetable(lat, lon) {
	if (lat == null || lon == null) return false;
	const b = BORNES_METROPOLE;
	return lat >= b.latMin && lat <= b.latMax && lon >= b.lonMin && lon <= b.lonMax;
}

// Tous les sommets d'un GeoJSON, aplatis en une liste [lon, lat].
function sommets(geojson) {
	const pts = [];
	const parcours = (a) => {
		if (typeof a[0] === 'number') pts.push(a);
		else a.forEach(parcours);
	};
	geojson.features.forEach((f) => parcours(f.geometry.coordinates));
	return pts;
}

// Projection conique conforme calée sur la France (parallèles standard métropole,
// méridien central 3°E). On AJUSTE sur un semis de POINTS (les sommets du fond),
// pas sur les polygones : les anneaux de ce GeoJSON sont enroulés à l'envers pour
// d3-geo, qui lirait alors « tout le globe sauf la France » et renverrait une
// étendue démesurée. Les points, eux, se projettent sans ambiguïté.
export function creerProjection(fond, largeur, hauteur, marge = 8) {
	return geoConicConformal()
		.parallels([44, 49])
		.rotate([-3, 0])
		.fitExtent(
			[
				[marge, marge],
				[largeur - marge, hauteur - marge]
			],
			{ type: 'MultiPoint', coordinates: sommets(fond) }
		);
}

// Le même enroulement inversé ferait remplir le COMPLÉMENT des régions (toute la
// carte sauf la France). On réinverse chaque anneau une fois au chargement pour
// que le tracé se remplisse à l'endroit. Renvoie une nouvelle FeatureCollection.
export function normaliserFond(fond) {
	const inverse = (a) => (typeof a[0][0] === 'number' ? a.slice().reverse() : a.map(inverse));
	return {
		...fond,
		features: fond.features.map((f) => ({
			...f,
			geometry: { ...f.geometry, coordinates: inverse(f.geometry.coordinates) }
		}))
	};
}

// Générateur de tracé SVG (contours des régions) pour la projection donnée.
export function creerChemin(projection) {
	return geoPath(projection);
}

// Écarte les points qui se chevauchent (relaxation déterministe, sans dépendance).
// À taille fixe, deux musées peuvent se cacher : soit ils partagent des coordonnées
// quasi identiques (deux musées d'une même ville), soit ils tombent à quelques
// pixels l'un de l'autre (Paris/Versailles). On repousse chaque paire trop proche
// jusqu'à `minDist`, en gardant les points au plus près de leur vraie position ;
// les points confondus sont séparés selon l'angle d'or (déterministe → rendu
// stable d'une exécution à l'autre). Renvoie une NOUVELLE liste (x/y ajustés, les
// autres champs préservés).
export function ecarterPoints(points, minDist, iterations = 80) {
	const p = points.map((d) => ({ ...d }));
	const n = p.length;
	for (let it = 0; it < iterations; it++) {
		let bouge = false;
		for (let i = 0; i < n; i++) {
			for (let j = i + 1; j < n; j++) {
				let dx = p[j].x - p[i].x;
				let dy = p[j].y - p[i].y;
				let d = Math.hypot(dx, dy);
				if (d >= minDist) continue;
				if (d < 0.01) {
					// points confondus : direction déterministe (angle d'or)
					const a = i * 2.399963;
					dx = Math.cos(a);
					dy = Math.sin(a);
					d = 1;
				}
				const pousse = (minDist - d) / 2;
				const ux = (dx / d) * pousse;
				const uy = (dy / d) * pousse;
				p[i].x -= ux;
				p[i].y -= uy;
				p[j].x += ux;
				p[j].y += uy;
				bouge = true;
			}
		}
		if (!bouge) break;
	}
	return p;
}
