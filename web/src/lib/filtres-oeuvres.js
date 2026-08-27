// Périmètres des deux filtres de l'onglet Œuvres — musée et formulation.
//
// Les deux commandes ne s'enchaînent pas : chacune est calculée dans le contexte
// de l'AUTRE, jamais sur le résultat final. Le menu des musées est calculé sur
// les œuvres de la formulation active (sans le musée), les puces de formulation
// sur les œuvres du musée actif (sans la formulation), et la liste affichée est
// l'intersection des deux. Sans cela, un filtre se masque lui-même : une fois un
// musée choisi, il serait le seul proposé, et une fois une formulation choisie,
// le menu continuerait d'annoncer des musées et des effectifs qui ne
// correspondent plus à ce que la liste montre (chantier du 2026-08-27).
//
// Fonctions pures, hors composant, pour que ces trois périmètres soient
// explicites et testables.

// Regroupe des œuvres par musée : un objet par établissement, avec son effectif
// DANS CE PÉRIMÈTRE. Tri par valeur décroissante (CLAUDE.md), départage
// alphabétique pour que l'ordre soit stable d'un rendu à l'autre.
// Une œuvre sans code Muséofile compte dans le total des œuvres mais ne crée
// aucune entrée de musée : la base en contient, et une ligne « musée inconnu »
// serait une fausse entrée.
export function regrouperMusees(oeuvres) {
	return Object.values(
		oeuvres.reduce((acc, o) => {
			if (!o.musee_code) return acc;
			const m = (acc[o.musee_code] ??= {
				code: o.musee_code,
				nom: o.musee,
				ville: o.ville,
				n: 0
			});
			m.n += 1;
			return acc;
		}, {})
	).sort((a, b) => b.n - a.n || (a.nom ?? '').localeCompare(b.nom ?? '', 'fr'));
}

// Œuvres d'une formulation (code de famille). `null` = toutes.
export function filtrerParFamille(oeuvres, code) {
	return code ? oeuvres.filter((o) => o.code === code) : oeuvres;
}

// Œuvres d'un musée (code Muséofile). `null` = tous.
export function filtrerParMusee(oeuvres, code) {
	return code ? oeuvres.filter((o) => o.musee_code === code) : oeuvres;
}

// Un musée reste-t-il tenable avec la formulation demandée ? Sert au changement
// de formulation : on garde le musée s'il conserve au moins une œuvre de cette
// formulation, sinon on revient à « Tous les musées » plutôt que de laisser une
// liste vide sans raison lisible.
export function museeCompatible(oeuvres, museeCode, familleCode) {
	if (!museeCode) return true;
	return oeuvres.some((o) => o.musee_code === museeCode && (!familleCode || o.code === familleCode));
}
