import { redirect } from '@sveltejs/kit';
import { base } from '$app/paths';

// `/les-presque` était le nom de travail de la rubrique — « les presque », pour les
// œuvres presque attribuées. Il n'a jamais rien dit au visiteur, et l'interface
// appelle cette page « Explorer les artistes » depuis longtemps. L'adresse suit le
// 2026-08-08 : `/artistes`.
//
// L'ancienne URL survit en redirection permanente (308). Le nom interne, lui, n'est
// pas pourchassé : les fichiers et identifiants qui portent « presque » restent tels
// quels tant qu'ils ne s'affichent pas — un refactor sans bénéfice visible n'en est
// pas un.
export const prerender = true;

export function load() {
	redirect(308, `${base}/artistes`);
}
