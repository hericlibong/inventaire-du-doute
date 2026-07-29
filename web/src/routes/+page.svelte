<script>
	// Accueil = affiche interactive, UN SEUL ÉCRAN (révision 2026-07-18). C'est l'entrée
	// dans l'application. La couverture porte, en preuve secondaire, le chiffre vedette
	// (24 507, lu depuis niveaux.json via +page.js) : c'est sur ces données qu'on travaille.
	import LandingCover from '$lib/LandingCover.svelte';

	let { data } = $props();
</script>

<LandingCover doute={data.doute} />
