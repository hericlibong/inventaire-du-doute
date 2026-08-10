// Accueil = affiche interactive (2026-07-18), adaptée au volume 1 le 2026-08-02.
// Les chiffres de la couverture sont ceux DU VOLUME (artistes retenus, notices
// concernées), lus depuis corpus_maitres.json — jamais écrits en dur.
//
// Le total national (24 507) a QUITTÉ la couverture : il demande une explication
// (versement volontaire, monoculture divulguée, ce qu'il compte exactement) que
// l'accueil n'a pas à porter. Il vit sur la page « Présentation », qui l'explique.
import { base } from '$app/paths';

// `fetch` ne connaît pas le chemin de base : sur GitHub Pages, un appel à
// `/data/...` viserait la racine du domaine et non le sous-répertoire du site
// (2026-08-10). Le préfixe vient de `$app/paths`, jamais écrit à la main.
export async function load({ fetch }) {
	const corpus = await fetch(`${base}/data/corpus_maitres.json`).then((r) => r.json());
	return {
		artistes: corpus.unites.nb_artistes,
		notices: corpus.unites.notices_distinctes
	};
}
