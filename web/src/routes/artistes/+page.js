// 1re dataviz — « Les presque » : le doute autour des maîtres de référence.
// Données : artistes.json (critère « maître de référence ET ≥ 10 notices
// prudentes hors copie » ; 102 artistes au 2026-08-02, l'effectif suit la liste).
import { base } from '$app/paths';

// `fetch` ne connaît pas le chemin de base : sur GitHub Pages, un appel à
// `/data/...` viserait la racine du domaine et non le sous-répertoire du site
// (2026-08-10). Le préfixe vient de `$app/paths`, jamais écrit à la main.
export async function load({ fetch }) {
	// portraits.json : source SECONDAIRE D'ILLUSTRATION (Wikimedia Commons),
	// jamais de donnée ni de comptage (docs/decisions.md 2026-07-09). Crédits
	// (auteur + licence) affichés en légende du portrait.
	const [artistes, portraits] = await Promise.all([
		fetch(`${base}/data/artistes.json`).then((r) => r.json()),
		fetch(`${base}/data/portraits.json`).then((r) => r.json())
	]);
	return { artistes, portraits };
}
