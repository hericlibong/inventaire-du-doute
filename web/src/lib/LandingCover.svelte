<script>
	// Couverture d'accueil = affiche interactive (nouvelle direction, 2026-07-17).
	// Le premier écran est entièrement occupé par l'illustration (asset horizontal sur
	// écran large, composition verticale autonome sur mobile via <picture>). Tous les
	// textes et la navigation sont de vrais éléments HTML SUPERPOSÉS — jamais intégrés
	// au bitmap. L'illustration évoque la base de données Joconde (archive, fiches,
	// index), pas Léonard ni le tableau.
	import { base } from '$app/paths';
	import EditorialNavigation from '$lib/EditorialNavigation.svelte';
	import { nombre } from '$lib/joconde.js';

	// Chiffre vedette (doute_total = 24 507), lu depuis niveaux.json (+page.js).
	let { doute } = $props();
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

	<!-- Titre + accroche à trois étages, dans l'aplat sombre (haut-gauche). Contraste
	     natif sur le bleu sombre. Accroche PROVISOIRE (stabilise la composition, pas un
	     texte éditorial définitif) : échelle, sujet, approche — sans aucun chiffre précis. -->
	<div class="titre">
		<h1>L'inventaire<br />du doute</h1>
		<div class="phrases">
			<p class="e1">Un million de notices.</p>
			<p class="e3">Une enquête dans les données des musées.</p>
		</div>

		<!-- Preuve secondaire : le chiffre vedette (24 507) et sa glose. Il remplace
		     l'étage « des milliers d'attributions incertaines » (redondant) : c'est le
		     point de départ de l'enquête, en corps réduit pour ne pas concurrencer le titre. -->
		<div class="preuve">
			<p class="chiffre">{nombre(doute)}</p>
			<p class="glose">
				œuvres pour lesquelles un musée de France a écrit un doute sur l'auteur.
			</p>
		</div>

		<p class="source">À partir de la base Joconde.</p>
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
		isolation: isolate; /* contexte d'empilement pour le voile local (mobile) */
	}

	.titre h1 {
		font-family: var(--police-titre);
		font-weight: 600;
		font-size: clamp(2.4rem, 5.2vw, 5.2rem);
		line-height: 0.95;
		letter-spacing: -0.015em;
		margin: 0;
	}

	/* Trois étages : Spectral ivoire franc, présence réelle sans concurrencer le titre,
	   progression légère (taille + tonalité), rythme compact d'affiche. */
	.phrases {
		margin: 1.2rem 0 0;
		font-family: var(--police-texte);
		max-width: 20ch;
	}

	.phrases p {
		margin: 0;
		line-height: 1.28;
	}

	.e1 {
		font-size: clamp(1.1rem, 1.6vw, 1.45rem);
		font-weight: 600;
		color: #f4eee0;
	}

	.e2 {
		margin-top: 0.35rem;
		font-size: clamp(1rem, 1.35vw, 1.2rem);
		color: #ece4d2;
	}

	.e3 {
		margin-top: 0.3rem;
		font-size: clamp(1rem, 1.35vw, 1.2rem);
		color: #d8cfbd;
	}

	/* --- Preuve secondaire : chiffre vedette + glose (aplat sombre) --- */
	.preuve {
		margin: 1.2rem 0 0;
		max-width: 24ch;
	}

	.chiffre {
		margin: 0;
		font-family: var(--police-titre);
		font-weight: 600;
		font-size: clamp(1.9rem, 3.2vw, 3rem);
		line-height: 1;
		letter-spacing: -0.01em;
		color: #eaddc2; /* ivoire chaud, distinct des étages */
		font-variant-numeric: tabular-nums;
	}

	.glose {
		margin: 0.45rem 0 0;
		font-family: var(--police-texte);
		font-size: clamp(0.86rem, 1vw, 0.98rem);
		line-height: 1.4;
		color: #cfd6dd;
	}

	.source {
		margin: 1.3rem 0 0;
		font-family: var(--police-ui);
		font-size: clamp(0.68rem, 0.85vw, 0.78rem);
		letter-spacing: 0.03em;
		color: #9fa9b3;
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
		/* Correction de contraste LOCALE et légère derrière le bloc titre (le bitmap
		   est réduit sur petit écran, l'aplat sombre ne descend pas assez). Dégradé
		   feutré en haut/bas (mask), fondu à droite : pas un voile sur l'image. */
		.titre::before {
			content: '';
			position: absolute;
			z-index: -1;
			inset: -0.6rem -2.6rem -1rem -1.6rem;
			pointer-events: none;
			background: linear-gradient(
				100deg,
				rgba(17, 25, 35, 0.78),
				rgba(17, 25, 35, 0.5) 55%,
				rgba(17, 25, 35, 0) 88%
			);
			-webkit-mask-image: linear-gradient(to bottom, transparent, #000 10%, #000 92%, transparent);
			mask-image: linear-gradient(to bottom, transparent, #000 10%, #000 92%, transparent);
		}
		.titre h1 {
			font-size: clamp(2.4rem, 12vw, 3.6rem);
		}
		/* Étages plus compacts sur mobile (réduire taille/espacement avant d'en retirer). */
		.phrases {
			margin-top: 0.9rem;
			max-width: 24ch;
		}
		.e1 {
			font-size: 1.12rem;
		}
		.e2,
		.e3 {
			font-size: 1rem;
		}
		.preuve {
			margin-top: 1.05rem;
			max-width: 30ch;
		}
		.chiffre {
			font-size: 2.1rem;
		}
		.glose {
			font-size: 0.9rem;
		}
		.source {
			margin-top: 1rem;
		}
		.nav-zone {
			top: auto;
			right: auto;
			bottom: 9%;
			left: 30%;
		}
	}

	/* Téléphone étroit / court : compresser titre + étages pour qu'ils tiennent dans
	   l'aplat sombre (le bitmap est réduit, le texte HTML ne l'est pas). */
	@media (max-width: 400px) {
		.titre h1 {
			font-size: 1.95rem;
		}
		.phrases {
			margin-top: 0.65rem;
			max-width: 22ch;
		}
		.e1 {
			font-size: 1rem;
		}
		.e2,
		.e3 {
			font-size: 0.9rem;
		}
		.e2 {
			margin-top: 0.25rem;
		}
		.e3 {
			margin-top: 0.2rem;
		}
		.preuve {
			margin-top: 0.8rem;
		}
		.chiffre {
			font-size: 1.7rem;
		}
		.glose {
			font-size: 0.82rem;
		}
		.source {
			margin-top: 0.7rem;
		}
	}
</style>
