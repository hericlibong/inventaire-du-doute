// Fenêtre de pagination compacte, isolée pour être testée sans le composant.
//
// À partir de la page active et du nombre total de pages, renvoie la suite à
// afficher : la première page, la dernière, la page active et ses voisines
// immédiates, avec « … » là où des pages sont masquées. Un seul numéro manquant
// n'est jamais remplacé par « … » (on montre le numéro plutôt qu'une ellipse
// qui coûterait un clic de plus). Le marqueur d'ellipse est la chaîne '…'.
//
//   fenetrePagination(3, 39)  → [1, 2, 3, 4, '…', 39]
//   fenetrePagination(20, 39) → [1, '…', 19, 20, 21, '…', 39]
//   fenetrePagination(39, 39) → [1, '…', 38, 39]
export function fenetrePagination(page, nbPages) {
	if (nbPages <= 1) return [1];

	// pages toujours candidates : bornes + fenêtre de ±1 autour de l'active
	const candidates = new Set([1, nbPages, page - 1, page, page + 1]);
	const visibles = [...candidates]
		.filter((p) => p >= 1 && p <= nbPages)
		.sort((a, b) => a - b);

	const sortie = [];
	let precedent = 0;
	for (const p of visibles) {
		if (p - precedent === 2) {
			// un seul numéro manquant : on le montre au lieu d'une ellipse
			sortie.push(precedent + 1);
		} else if (p - precedent > 2) {
			sortie.push('…');
		}
		sortie.push(p);
		precedent = p;
	}
	return sortie;
}
