<script>
	import MetaPage from '$lib/MetaPage.svelte';
	import { metaAccueil } from '$lib/meta.js';

	// Accueil = affiche interactive, UN SEUL ÉCRAN (révision 2026-07-18). C'est l'entrée
	// dans l'application. La couverture porte le titre du volume, un slogan et les
	// chiffres DU VOLUME (phase 6, 2026-08-02) — lus depuis corpus_maitres.json via
	// +page.js, jamais écrits en dur.
	import LandingCover from '$lib/LandingCover.svelte';

	let { data } = $props();
</script>

<MetaPage {...metaAccueil(data.artistes)} chemin="/" />


<LandingCover artistes={data.artistes} notices={data.notices} />
