// Page « Méthode et limites » — rassemble les limites dispersées dans le projet.
// Tous les chiffres viennent des exports canoniques (aucun nombre écrit à la main
// dans la page) : niveaux.json (comptages de référence), provenance.json (source,
// version), vue_ensemble.json (doute dans la liste), artistes.json (nombre de noms).
export async function load({ fetch }) {
	const [niveaux, provenance, vue, artistes] = await Promise.all([
		fetch('/data/niveaux.json').then((r) => r.json()),
		fetch('/data/provenance.json').then((r) => r.json()),
		fetch('/data/vue_ensemble.json').then((r) => r.json()),
		fetch('/data/artistes.json').then((r) => r.json())
	]);
	return { niveaux, provenance, vue, artistes };
}
