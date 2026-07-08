// « Hello data » du socle : on charge un vrai chiffre depuis les JSON exportés.
// fetch("/data/...") lit static/data/, synchronisé par `npm run sync:data`.
export async function load({ fetch }) {
	const niveaux = await (await fetch('/data/niveaux.json')).json();
	const provenance = await (await fetch('/data/provenance.json')).json();
	return { niveaux, provenance };
}
