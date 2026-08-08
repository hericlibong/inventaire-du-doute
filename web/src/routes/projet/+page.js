// Page « Présentation » du volume 1 — de la notice qu'on lit sous une œuvre
// jusqu'à l'exploration des artistes.
//
// Tous les chiffres viennent des exports canoniques, aucun n'est écrit dans la
// page : corpus_maitres.json (ampleur du volume, mentions, notice d'ouverture),
// registre.json (état des candidats examinés), niveaux.json (total national, qui
// ne sert QUE de contexte ici — le sujet de la page est le volume).
export async function load({ fetch }) {
	const [corpus, registre, niveaux] = await Promise.all([
		fetch('/data/corpus_maitres.json').then((r) => r.json()),
		fetch('/data/registre.json').then((r) => r.json()),
		fetch('/data/niveaux.json').then((r) => r.json())
	]);
	return { corpus, registre, niveaux };
}
