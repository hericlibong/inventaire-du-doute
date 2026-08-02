// 1re dataviz — « Les presque » : le doute autour des maîtres de référence.
// Données : artistes.json (critère « maître de référence ET ≥ 10 notices
// prudentes hors copie » ; 103 maîtres au 2026-08-02, l'effectif suit la liste).
export async function load({ fetch }) {
	// portraits.json : source SECONDAIRE D'ILLUSTRATION (Wikimedia Commons),
	// jamais de donnée ni de comptage (docs/decisions.md 2026-07-09). Crédits
	// (auteur + licence) affichés en légende du portrait.
	const [artistes, portraits] = await Promise.all([
		fetch('/data/artistes.json').then((r) => r.json()),
		fetch('/data/portraits.json').then((r) => r.json())
	]);
	return { artistes, portraits };
}
