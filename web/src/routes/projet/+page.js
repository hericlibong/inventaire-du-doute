// Page « Présentation » du volume 1 — de la notice qu'on lit sous une œuvre
// jusqu'à l'exploration des artistes.
//
// Tous les chiffres viennent des exports canoniques, aucun n'est écrit dans la
// page : corpus_maitres.json (ampleur du volume, mentions, notice d'ouverture),
// registre.json (état des candidats examinés), niveaux.json (total national, qui
// ne sert QUE de contexte ici — le sujet de la page est le volume).
import { base } from '$app/paths';

// `fetch` ne connaît pas le chemin de base : sur GitHub Pages, un appel à
// `/data/...` viserait la racine du domaine et non le sous-répertoire du site
// (2026-08-10). Le préfixe vient de `$app/paths`, jamais écrit à la main.
export async function load({ fetch }) {
	const [corpus, registre, niveaux] = await Promise.all([
		fetch(`${base}/data/corpus_maitres.json`).then((r) => r.json()),
		fetch(`${base}/data/registre.json`).then((r) => r.json()),
		fetch(`${base}/data/niveaux.json`).then((r) => r.json())
	]);
	return { corpus, registre, niveaux };
}
