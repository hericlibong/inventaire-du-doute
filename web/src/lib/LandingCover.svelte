<script>
	// Couverture d'accueil = affiche interactive (nouvelle direction, 2026-07-17).
	// Le premier écran est entièrement occupé par l'illustration (asset horizontal sur
	// écran large, composition verticale autonome sur mobile via <picture>). Tous les
	// textes et la navigation sont de vrais éléments HTML SUPERPOSÉS — jamais intégrés
	// au bitmap. L'illustration évoque la base de données Joconde (archive, fiches,
	// index), pas Léonard ni le tableau.
	import { base } from '$app/paths';
	import EditorialNavigation from '$lib/EditorialNavigation.svelte';
</script>

<section class="cover">
	<picture class="fond">
		<!-- Composition verticale sur mobile ET sur tablette en portrait (l'asset
		     horizontal se recadrerait trop dans un viewport très vertical). L'asset
		     horizontal reste pour l'ordinateur et la tablette « large » (paysage). -->
		<source
			media="(max-width: 767px), (orientation: portrait) and (max-width: 1024px)"
			srcset="{base}/cover/accueil-mobile.png"
		/>
		<img
			src="{base}/cover/accueil-desktop.png"
			alt="Composition évoquant la base de données Joconde : fiches, cadres, blocs de notices et un visage d'archive."
		/>
	</picture>

	<!-- Titre + accroche + source, dans l'aplat sombre (haut-gauche). Texte clair
	     légèrement froid — contraste natif sur le bleu sombre. -->
	<div class="titre">
		<h1>L'inventaire<br />du doute</h1>
		<p class="accroche">Les mots employés par les musées lorsqu'un nom ne suffit pas.</p>
		<p class="source">Une exploration de la base Joconde du ministère de la Culture.</p>
	</div>

	<!-- Navigation sur la fiche claire (droite sur ordinateur, moitié basse sur mobile). -->
	<div class="nav-zone">
		<EditorialNavigation />
	</div>
</section>

<style>
	.cover {
		position: relative;
		width: 100%;
		min-height: 100vh; /* repli */
		min-height: 100svh;
		overflow: hidden;
	}

	.fond,
	.fond img {
		position: absolute;
		inset: 0;
		width: 100%;
		height: 100%;
	}

	.fond img {
		object-fit: cover;
		object-position: center;
		display: block;
	}

	/* --- Titre (aplat sombre) --- */
	.titre {
		position: absolute;
		top: 6%;
		left: 4%;
		max-width: 34%;
		color: #e9edf1; /* clair légèrement froid */
	}

	.titre h1 {
		font-family: var(--police-titre);
		font-weight: 600;
		font-size: clamp(2.4rem, 5.2vw, 5.2rem);
		line-height: 0.95;
		letter-spacing: -0.015em;
		margin: 0;
	}

	.accroche {
		margin: 1.1rem 0 0;
		font-family: var(--police-texte);
		font-size: clamp(0.95rem, 1.4vw, 1.2rem);
		line-height: 1.4;
		max-width: 22ch;
		color: #d6dde4;
	}

	.source {
		margin: 1.4rem 0 0;
		font-family: var(--police-ui);
		font-size: clamp(0.7rem, 0.9vw, 0.82rem);
		letter-spacing: 0.02em;
		color: #aeb8c2;
	}

	/* --- Navigation (fiche claire, à droite sur ordinateur) --- */
	.nav-zone {
		position: absolute;
		top: 21%;
		right: 13%;
	}

	/* --- Composition verticale (mobile + tablette portrait) : titre en haut,
	   nav sur la fiche basse. Même condition que la <source> mobile ci-dessus. --- */
	@media (max-width: 767px), (orientation: portrait) and (max-width: 1024px) {
		.titre {
			top: 4%;
			left: 6%;
			max-width: 66%;
		}
		.titre h1 {
			font-size: clamp(2.4rem, 12vw, 3.6rem);
		}
		.accroche {
			font-size: 0.95rem;
			max-width: 20ch;
		}
		.nav-zone {
			top: auto;
			right: auto;
			bottom: 9%;
			left: 30%;
		}
	}
</style>
