// Page « Méthode et limites » — rassemble les limites dispersées dans le projet.
// Tous les chiffres viennent des exports canoniques (aucun nombre écrit à la main
// dans la page) : niveaux.json (comptages de référence), provenance.json (source,
// version), artistes.json (nombre de noms), registre.json (état des candidats
// examinés : retenus / écartés / à instruire). vue_ensemble.json n'est plus lu
// depuis le 2026-08-05 : la seule phrase qui s'en servait — « ces N noms
// réunissent X des Y notices prudentes » — a quitté la page avec la refonte de
// « Comment la liste des artistes a-t-elle été établie ? ».
export async function load({ fetch }) {
	const [niveaux, provenance, artistes, registre] = await Promise.all([
		fetch('/data/niveaux.json').then((r) => r.json()),
		fetch('/data/provenance.json').then((r) => r.json()),
		fetch('/data/artistes.json').then((r) => r.json()),
		fetch('/data/registre.json').then((r) => r.json())
	]);
	return { niveaux, provenance, artistes, registre };
}
