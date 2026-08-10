// Page « Méthode et limites » — rassemble les limites dispersées dans le projet.
// Tous les chiffres viennent des exports canoniques (aucun nombre écrit à la main
// dans la page) : niveaux.json (comptages de référence), provenance.json (source,
// version), artistes.json (nombre de noms), registre.json (état des candidats
// examinés : retenus / écartés / à instruire). vue_ensemble.json n'est plus lu
// depuis le 2026-08-05 : la seule phrase qui s'en servait — « ces N noms
// réunissent X des Y notices prudentes » — a quitté la page avec la refonte de
// « Comment la liste des artistes a-t-elle été établie ? ».
import { base } from '$app/paths';

// `fetch` ne connaît pas le chemin de base : sur GitHub Pages, un appel à
// `/data/...` viserait la racine du domaine et non le sous-répertoire du site
// (2026-08-10). Le préfixe vient de `$app/paths`, jamais écrit à la main.
export async function load({ fetch }) {
	const [niveaux, provenance, artistes, registre] = await Promise.all([
		fetch(`${base}/data/niveaux.json`).then((r) => r.json()),
		fetch(`${base}/data/provenance.json`).then((r) => r.json()),
		fetch(`${base}/data/artistes.json`).then((r) => r.json()),
		fetch(`${base}/data/registre.json`).then((r) => r.json())
	]);
	return { niveaux, provenance, artistes, registre };
}
