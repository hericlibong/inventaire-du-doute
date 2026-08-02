import { redirect } from '@sveltejs/kit';
import { base } from '$app/paths';

// « Comprendre les mentions » est sortie de la publication en phase 7 (2026-08-02).
// Son URL survit en REDIRECTION : elle a circulé, et une adresse publiée ne doit pas
// tomber sur une page d'erreur.
//
// Elle redirige vers la Présentation, qui a repris ce qui lui restait d'utile : le
// graphique des mentions et, depuis la phase 7, leurs définitions une à une. La
// comparaison chiffrée avec le total national, elle, a été abandonnée le 2026-08-02
// avec les autres vues du prototype — elle ne revient pas.
//
// 308 : déplacement permanent, méthode conservée. En build statique, le prérendu écrit
// une page de renvoi ; les hébergeurs qui savent lire `_redirects` feront mieux.
export const prerender = true;

export function load() {
	redirect(308, `${base}/presentation`);
}
