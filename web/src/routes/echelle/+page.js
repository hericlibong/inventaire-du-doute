// « Comprendre les mentions » — le langage de la prudence des musées.
// Données : vue_ensemble.json (contraste « attribué à » global vs école/atelier/
// manière dans les noms retenus). La route garde le slug /echelle (prévu de longue date
// pour « l'échelle du doute ») ; seul le libellé public change (nav).
export async function load({ fetch }) {
	const vue = await fetch('/data/vue_ensemble.json').then((r) => r.json());
	return { vue };
}
