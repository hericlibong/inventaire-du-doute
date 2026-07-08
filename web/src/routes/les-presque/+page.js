// 1re dataviz — « Les presque » : le doute autour des maîtres de référence.
// Données : artistes.json (27 maîtres, critère « ≥ 20 doutes hors copie »).
export async function load({ fetch }) {
	const artistes = await (await fetch('/data/artistes.json')).json();
	return { artistes };
}
