// Accueil = affiche interactive (2026-07-18). On lit le chiffre vedette (doute_total,
// = 24 507) depuis niveaux.json pour l'afficher en preuve secondaire sur la couverture
// (retour du chiffre demandé le 2026-07-18) — jamais en dur, toujours depuis l'export.
export async function load({ fetch }) {
	const niveaux = await fetch('/data/niveaux.json').then((r) => r.json());
	return { doute: niveaux.doute_total };
}
