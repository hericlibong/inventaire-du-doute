import adapter from '@sveltejs/adapter-static';
import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig({
	plugins: [
		sveltekit({
			compilerOptions: {
				// Force runes mode for the project, except for libraries. Can be removed in svelte 6.
				runes: ({ filename }) => filename.split(/[/\\]/).includes('node_modules') ? undefined : true
			},
			// CHEMIN DE BASE (2026-08-10) : le site se publie en démonstration sur
			// GitHub Pages dans un SOUS-RÉPERTOIRE — /inventaire-du-doute/ — et non à
			// la racine d'un domaine, qui appartient au site personnel. SvelteKit doit
			// le savoir au moment du build, sans quoi toutes les URL internes
			// viseraient la racine.
			//
			// Il est lu dans `BASE_PATH`, donc appliqué SEULEMENT au build de
			// publication : en développement la variable est absente, la base reste
			// vide, et le site tourne à la racine de localhost comme avant.
			//
			// Le code n'en sait rien : il importe `base` depuis `$app/paths`. Aucun
			// composant ne concatène ce préfixe à la main.
			//
			// Cette configuration vit ICI et non dans un `svelte.config.js` : dès que
			// des options sont passées au plugin Vite, SvelteKit ignore ce fichier —
			// il le dit d'ailleurs en clair au build.
			paths: { base: process.env.BASE_PATH ?? '' },
			// Site entièrement prérendu. `fallback` écrit un 404.html : GitHub Pages
			// le sert sur toute URL inconnue sous le chemin de base, plutôt que sa
			// propre page d'erreur.
			adapter: adapter({ fallback: '404.html' })
		})
	]
});
