// Accueil = affiche interactive (2026-07-18), adaptée au volume 1 le 2026-08-02.
// Les chiffres de la couverture sont ceux DU VOLUME (artistes retenus, notices
// concernées), lus depuis corpus_maitres.json — jamais écrits en dur.
//
// Le total national (24 507) a QUITTÉ la couverture : il demande une explication
// (versement volontaire, monoculture divulguée, ce qu'il compte exactement) que
// l'accueil n'a pas à porter. Il vit sur la page « Présentation », qui l'explique.
export async function load({ fetch }) {
	const corpus = await fetch('/data/corpus_maitres.json').then((r) => r.json());
	return {
		artistes: corpus.unites.nb_artistes,
		notices: corpus.unites.notices_distinctes
	};
}
