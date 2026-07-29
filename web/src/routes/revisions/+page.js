// Rubrique « Avant / après » : les révisions d'attribution dans les notices.
// Données : revisions.json (statistiques sur tout le corpus + lot éditorial de
// 32 cartes lisibles). Cadrage : docs/rubrique-revisions.md ; décisions du
// 2026-07-14 (bis) et (ter). Aucune source secondaire ici (pas d'image en V1).
export async function load({ fetch }) {
	const revisions = await fetch('/data/revisions.json').then((r) => r.json());
	return { revisions };
}
