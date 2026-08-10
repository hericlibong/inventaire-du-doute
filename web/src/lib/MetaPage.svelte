<script>
	// Balises de tête d'une page publique : titre, description, partage.
	//
	// Un seul composant pour les quatre pages — les textes viennent de `meta.js`,
	// jamais écrits dans une page. Ce qui change d'une page à l'autre tient en
	// trois valeurs : le titre, la description, et le chemin.
	import { page } from '$app/stores';
	import { OG_IMAGE, SITE_NOM, absolu } from '$lib/meta.js';

	// titre / descr : voir meta.js · chemin : route publiée, sans le préfixe de base
	let { titre, descr, chemin } = $props();

	// `og:url` et `og:image` doivent être ABSOLUES : un partage se lit hors du
	// site, où un chemin relatif ne veut rien dire. C'est le seul endroit où
	// l'adresse publique est reconstituée.
	const url = $derived(absolu(chemin));
</script>

<svelte:head>
	<title>{titre}</title>
	<meta name="description" content={descr} />

	<meta property="og:type" content="website" />
	<meta property="og:locale" content="fr_FR" />
	<meta property="og:site_name" content={SITE_NOM} />
	<meta property="og:title" content={titre} />
	<meta property="og:description" content={descr} />
	<meta property="og:url" content={url} />
	<meta property="og:image" content={absolu(OG_IMAGE)} />
	<meta property="og:image:width" content="1200" />
	<meta property="og:image:height" content="630" />
	<meta property="og:image:alt" content="L’inventaire du doute — Volume 1 : Autour des maîtres" />

	<meta name="twitter:card" content="summary_large_image" />
	<meta name="twitter:title" content={titre} />
	<meta name="twitter:description" content={descr} />
	<meta name="twitter:image" content={absolu(OG_IMAGE)} />

	<!-- Adresse canonique : la page vit à une seule adresse, quelle que soit la
	     manière dont on y est arrivé (ancienne URL redirigée, partage). -->
	<link rel="canonical" href={url} />
</svelte:head>
