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

	// Chiffres DU VOLUME, lus depuis corpus_maitres.json (+page.js) : le nombre
	// d'artistes retenus et celui des notices concernées. Le total national a quitté
	// la couverture le 2026-08-02 — il demande une explication que l'accueil n'a pas
	// à porter, et il vit désormais sur la page « Le projet ».
	let { artistes, notices } = $props();

	// `toLocaleString('fr-FR')` sépare les milliers par une espace fine insécable
	// (U+202F). Elle convient au texte courant, mais à ce corps et dans la police de
	// titre elle se referme presque entièrement : on lisait « 6081 ». Sur l'affiche
	// seulement, on la remplace par une espace insécable ordinaire — le nombre reste
	// insécable, et le millier redevient visible.
	const enVedette = (v) => nombre(v).replace(/\u202f/g, '\u00a0');
</script>

<section class="cover">
	<picture class="fond">
		<!-- Composition verticale sur mobile ET sur tablette en portrait (l'asset
		     horizontal se recadrerait trop dans un viewport très vertical). L'asset
		     horizontal reste pour l'ordinateur et la tablette « large » (paysage). -->
		<source
			media="(max-width: 767px), (orientation: portrait) and (max-width: 1024px)"
			srcset="{base}/cover/accueil-mobile.jpg"
		/>
		<img
			src="{base}/cover/accueil-desktop.jpg"
			alt="Composition évoquant la base de données Joconde : fiches, cadres, blocs de notices et un visage d'archive."
		/>
	</picture>

	<!-- Bloc éditorial de la couverture. Réécrit le 2026-08-08 (phase 2 de la
	     finalisation), sur le texte de l'utilisateur, repris tel quel.
	     Ce qu'il remplace disait « Quand le musée n'est pas sûr, il l'écrit » —
	     une généralité qui ne nommait ni de quoi ni de qui il s'agit, et que
	     l'utilisateur lui-même ne comprenait plus.
	     Trois règles portées par ce texte :
	       · il ne commence PAS par « Dans Joconde » — on comprend le sujet avant
	         d'apprendre le nom de la source ;
	       · il n'énumère AUCUNE mention (« attribué à », « de son atelier »…) :
	         leur explication appartient à la page « Le projet » ;
	       · les chiffres deviennent une information autonome, sortie des phrases,
	         chaque nombre restant collé à son unité.
	     Les deux valeurs sont lues dans corpus_maitres.json (+page.js), jamais
	     écrites en dur. -->
	<div class="titre">
		<h1>L’inventaire<br />du doute</h1>
		<p class="volume">Volume 1 — Autour des maîtres</p>

		<div class="phrases">
			<p class="e1">
				Le nom d’un artiste peut accompagner une œuvre sans que le musée la lui
				attribue directement.
			</p>
			<p class="e2">
				Ce premier volume explore ces liens autour de {nombre(artistes)} artistes :
				les œuvres concernées, la manière dont elles sont décrites et les musées qui
				les conservent.
			</p>
		</div>

		<!-- Les chiffres, détachés du récit : deux quantités qu'on lit d'un coup
		     d'œil. Chaque nombre garde son unité contre lui, et la paire reste
		     insécable — jamais un nombre seul en fin de ligne. -->
		<p class="chiffres">
			<span class="paire"><span class="chiffre">{enVedette(artistes)}</span> artistes</span>
			<span class="sep" aria-hidden="true">·</span>
			<span class="paire"><span class="chiffre">{enVedette(notices)}</span> notices</span>
		</p>

		<p class="source">Source : Joconde, catalogue collectif des musées de France.</p>
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

	/* --- Bloc éditorial (sur l'aplat sombre) ---
	   La largeur est passée de 34 % à 46 % le 2026-08-08. L'ancienne borne venait
	   d'une contrainte qui n'existait pas : le code répétait que « l'aplat sombre est
	   étroit », alors qu'il occupe environ 700 × 620 px sur un écran de 1440. Le texte
	   n'en utilisait qu'un tiers, et se cassait en lignes de trois mots. */
	.titre {
		position: absolute;
		top: 6%;
		left: 4%;
		max-width: 46%;
		color: #e9edf1; /* clair légèrement froid */
		isolation: isolate; /* contexte d'empilement pour le voile local */
	}

	/* Correction de contraste LOCALE derrière le bloc, sur grand écran aussi
	   (2026-08-08). L'aplat sombre de l'illustration se referme en escalier, et sa
	   position dépend du recadrage : ce qui tient sur un écran 16/10 déborde sur un
	   16/9. Plutôt que de calibrer le texte au pixel près sur une forme irrégulière
	   — réglage qui casse au premier format non testé —, on garantit le fond.
	   Le voile est très faible là où l'illustration est déjà sombre, et se dissipe
	   complètement sur la droite et en bas : ce n'est pas un cache posé sur l'image,
	   c'est une assurance de lisibilité. Même procédé que sur mobile, en plus léger. */
	.titre::before {
		content: '';
		position: absolute;
		z-index: -1;
		inset: -1rem -3rem -1.5rem -2rem;
		pointer-events: none;
		background: linear-gradient(
			100deg,
			rgba(17, 25, 35, 0.55),
			rgba(17, 25, 35, 0.42) 58%,
			rgba(17, 25, 35, 0) 92%
		);
		-webkit-mask-image: linear-gradient(to bottom, transparent, #000 6%, #000 90%, transparent);
		mask-image: linear-gradient(to bottom, transparent, #000 6%, #000 90%, transparent);
	}

	.titre h1 {
		font-family: var(--police-titre);
		font-weight: 600;
		font-size: clamp(2.4rem, 5.2vw, 5.2rem);
		line-height: 0.95;
		letter-spacing: -0.015em;
		margin: 0;
	}

	/* Titre du volume : sous le nom du site, dans le registre UI, discret mais net.
	   C'est lui qui dit ce qu'on va lire — le site en publiera d'autres. */
	.volume {
		margin: 0.7rem 0 0;
		font-family: var(--police-ui);
		font-size: clamp(0.72rem, 0.95vw, 0.86rem);
		letter-spacing: 0.14em;
		text-transform: uppercase;
		color: #c8b89a;
	}

	/* Les deux paragraphes.
	   Les bornes sont en `vw`, et non en caractères : l'aplat sombre est une forme
	   de l'illustration, sa largeur suit donc celle de la fenêtre, pas la chasse de
	   la police. Mesuré le 2026-08-08 sur les deux formats d'écran courants — le
	   plus serré est le 16/10 (1440 × 900), où la zone sombre ne laisse que 26 % de
	   la largeur à hauteur des paragraphes, 19 % à hauteur des chiffres et 15 % à
	   hauteur de la source. Le plafond en `rem` évite qu'une ligne devienne
	   illisible sur un très grand écran. */
	.phrases {
		margin: 1.5rem 0 0;
		font-family: var(--police-texte);
		max-width: min(23vw, 32rem);
	}

	.phrases p {
		margin: 0;
		line-height: 1.45;
	}

	/* Première phrase : c'est elle qui pose le sujet. Elle porte donc le poids. */
	.e1 {
		font-size: clamp(1.05rem, 1.5vw, 1.4rem);
		font-weight: 600;
		color: #f4eee0;
	}

	/* Seconde : ce que le volume contient. Un cran en dessous, et détachée pour
	   qu'on voie deux temps et non un pavé. */
	.e2 {
		margin-top: 0.85rem;
		font-size: clamp(0.95rem, 1.2vw, 1.1rem);
		color: #dcd4c4;
	}

	/* Les chiffres, information autonome (2026-08-08). Ils ne sont plus dans une
	   phrase : ils se lisent seuls, sous le texte, séparés par un point médian. Un
	   filet les détache sans les encadrer. Ils restent nettement sous le titre —
	   c'est une indication d'ampleur, pas l'accroche. */
	.chiffres {
		margin: 1.2rem 0 0;
		padding-top: 0.8rem;
		border-top: 1px solid rgba(200, 184, 154, 0.32);
		/* L'aplat se referme en escalier vers le bas : ce qui tient à hauteur des
		   paragraphes déborde plus bas. « des musées de » passait sur le clair. */
		max-width: min(17vw, 19rem);
		font-family: var(--police-ui);
		font-size: clamp(0.9rem, 1.1vw, 1.02rem);
		color: #d9d0be;
		display: flex;
		flex-wrap: wrap;
		align-items: baseline;
		gap: 0.5rem 0.7rem;
	}

	/* Le nombre et son unité ne se séparent jamais, même au retour à la ligne. */
	.paire {
		white-space: nowrap;
	}

	.sep {
		color: rgba(200, 184, 154, 0.6);
	}

	/* Nombre en vedette : police titre, ivoire chaud, chiffres à chasse fixe.
	   Le séparateur de milliers est élargi en amont (voir `enVedette`). */
	.chiffre {
		font-family: var(--police-titre);
		font-weight: 600;
		font-size: 1.35em;
		letter-spacing: -0.01em;
		color: #eaddc2;
		font-variant-numeric: tabular-nums;
		white-space: nowrap;
	}

	.source {
		margin: 0.8rem 0 0;
		max-width: min(13vw, 14rem);
		font-family: var(--police-ui);
		font-size: clamp(0.7rem, 0.85vw, 0.8rem);
		letter-spacing: 0.03em;
		line-height: 1.4;
		color: #b3bcc6;
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
		/* Le texte et le visage ne se disputent plus le même espace. Le haut de
		   l'affiche prolonge l'aplat sombre de l'image ; le bitmap commence ensuite,
		   sans agrandissement ni voile, et garde son sujet dans la moitié basse. */
		.fond {
			background: #111923;
		}

		.fond img {
			inset: 47% 0 auto;
			width: 100%;
			height: auto;
			max-width: none;
			object-fit: contain;
			object-position: center top;
		}

		.titre {
			top: 4%;
			left: 6%;
			max-width: 88%;
		}

		.titre::before {
			display: none;
		}
		.titre h1 {
			font-size: clamp(2.4rem, 12vw, 3.6rem);
		}
		/* Étages plus compacts sur mobile (réduire taille/espacement avant d'en retirer). */
		.phrases {
			margin-top: 1rem;
			max-width: 100%;
		}
		.e1 {
			font-size: 1.08rem;
		}
		.e2 {
			margin-top: 0.7rem;
			font-size: 0.96rem;
		}
		.chiffres,
		.source {
			max-width: 100%;
		}
		.chiffres {
			margin-top: 1.1rem;
			padding-top: 0.75rem;
		}
		.source {
			margin-top: 0.85rem;
		}
		.nav-zone {
			top: auto;
			right: auto;
			bottom: 9%;
			left: 30%;
		}
	}

	/* Téléphone étroit / court : compresser titre et étages pour que tout tienne dans
	   le premier écran (le bitmap est réduit, le texte HTML ne l'est pas). */
	@media (max-width: 400px) {
		.titre h1 {
			font-size: 1.95rem;
		}
		.phrases {
			margin-top: 0.75rem;
		}
		.e1 {
			font-size: 0.98rem;
		}
		.e2 {
			margin-top: 0.5rem;
			font-size: 0.88rem;
		}
		.chiffres {
			margin-top: 0.85rem;
			padding-top: 0.6rem;
			font-size: 0.86rem;
		}
		.source {
			margin-top: 0.7rem;
			font-size: 0.68rem;
		}
	}
</style>
