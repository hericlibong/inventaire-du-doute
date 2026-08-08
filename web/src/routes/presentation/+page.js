import { redirect } from '@sveltejs/kit';
import { base } from '$app/paths';

// La page s'appelait « Présentation » et vivait à `/presentation`. Elle s'appelle
// « Le projet » depuis le 2026-08-08, et son adresse le dit maintenant aussi.
//
// L'ancienne URL ne disparaît pas : elle a circulé, et une adresse publiée ne doit
// pas tomber sur une page d'erreur. 308 — déplacement permanent, méthode conservée.
//
// L'ancre est conservée par le navigateur lui-même : elle n'est jamais envoyée au
// serveur, et survit donc à la redirection. `/presentation#chiffres` arrive bien sur
// `/projet#chiffres`.
export const prerender = true;

export function load() {
	redirect(308, `${base}/projet`);
}
