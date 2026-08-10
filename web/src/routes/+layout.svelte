<script>
	import '$lib/styles/tokens.css';
	import '$lib/styles/fonts.css';
	import { page } from '$app/stores';
	import { base } from '$app/paths';

	let { children } = $props();

	// Le site est publié dans un SOUS-RÉPERTOIRE sur GitHub Pages : `pathname` vaut
	// alors « /inventaire-du-doute/artistes/ » et non « /artistes ». On le dépouille
	// de son préfixe une fois pour toutes, et tout le reste raisonne sur des routes
	// internes, comme avant (2026-08-10). Le slash final vient de
	// `trailingSlash: 'always'`, nécessaire à GitHub Pages ; il est retiré ici pour
	// que les comparaisons restent celles d'origine.
	const route = $derived(
		($page.url.pathname.slice(base.length) || '/').replace(/(.)\/$/, '$1')
	);

	// Page courante = accueil sur « / » exact, sinon préfixe de la route.
	const estActif = (href) => (href === '/' ? route === '/' : route.startsWith(href));

	// L'accueil est une couverture pleine page : la coquille (masthead) y est masquée.
	const estAccueil = $derived(route === '/');

	// Routes en PLEINE LARGEUR (direction « affiche ») : accueil + pages refondues.
	// Elles gèrent leurs propres gouttières ; les pages pas encore refondues gardent
	// la colonne centrée.
	const estPleine = $derived(
		route === '/' ||
			route.startsWith('/projet') ||
			route.startsWith('/artistes') ||
			route.startsWith('/methode')
	);

	// Les rubriques en réserve (Les révisions, La carte) ne figurent pas ici : leur
	// code et leurs données restent au dépôt, hors de la navigation publique tant
	// qu'elles ne sont pas publiées — elles seront la matière d'autres volumes.
	//
	// Navigation publique du volume 1 : trois entrées dans l'ordre de lecture.
	// « Méthode » a rejoint le footer après observation de la démonstration mobile :
	// elle reste accessible partout et depuis les renvois contextuels, sans mettre
	// au même rang l'outil principal et sa documentation. « Comprendre les mentions »
	// en est sortie auparavant — ses
	// définitions ont rejoint « Le projet », sous le graphique qui les compte, et
	// son ancienne URL redirige.
	//
	// Le champ `prete` et la branche « à venir » ont été SUPPRIMÉS avec elle. Ils
	// permettaient d'afficher une rubrique non publiée en lien inerte ; la consigne
	// est de ne pas annoncer les volumes suivants de cette façon. Retirer le
	// mécanisme, et pas seulement les entrées, évite qu'il resserve un jour.
	const briques = [
		{ titre: 'Accueil', href: '/' },
		// Libellé public renommé le 2026-08-08 : « Le projet » dit de quoi la page
		// parle, quand « Présentation » ne disait que ce qu'elle est. La route ne
		// bouge pas — elle a circulé.
		{ titre: 'Le projet', href: '/projet' },
		{ titre: 'Explorer les artistes', href: '/artistes' }
	];
</script>

<svelte:head>
	<!-- Monogramme « Id » en Fraunces vectorisée, sur l'aplat navy de la couverture
	     (2026-08-10). Il remplace le logo Svelte livré par défaut, qui aurait mis la
	     marque du framework dans l'onglet et les favoris. Les tracés sont dans le
	     SVG : aucune webfont n'est chargée pour l'afficher. -->
	<link rel="icon" href="{base}/favicon.svg" type="image/svg+xml" />
</svelte:head>

{#if !estAccueil}
<header>
	<!-- Charte v2 : bandeau navy (registre de la couverture), texte ivoire. -->
	<div class="masthead">
		<a class="marque" href="{base}/">L'inventaire du doute</a>
		<nav aria-label="Navigation principale">
			<ul>
				{#each briques as brique (brique.href)}
					<li>
						<a
							href="{base}{brique.href}"
							aria-current={estActif(brique.href) ? 'page' : undefined}
						>
							{brique.titre}
						</a>
					</li>
				{/each}
			</ul>
		</nav>
	</div>
</header>
{/if}

<main class:pleine={estPleine}>
	{@render children()}
</main>

<footer>
	<div class="footer-interieur">
		<div class="footer-identite">
			<p class="footer-auteur">Un projet de Héric Libong</p>
			<p class="footer-liens">
				<a href="mailto:heric.afrimages@gmail.com">E-mail</a>
				<a href="https://hericlibong.github.io/">Portfolio</a>
				<a href="https://github.com/hericlibong/inventaire-du-doute">GitHub</a>
				<a href="{base}/methode">Méthode, sources et limites</a>
			</p>
		</div>
		<p class="footer-source">
			Source unique : base Joconde (Ministère de la Culture), Licence Ouverte 2.0.
			Ce projet n'authentifie aucune œuvre : il restitue ce que les musées ont
			eux-mêmes publié.
		</p>
	</div>
</footer>

<style>
	/* Le header étant fixé en tête, une ancre atteinte par un lien du sommaire
	   arriverait SOUS lui. `scroll-padding-top` réserve sa hauteur sur le conteneur
	   de défilement : 4,5 rem couvre le bandeau d'une ligne, 7,5 rem celui de deux
	   lignes sur petit écran. Les pages qui posent déjà un `scroll-margin-top` sur
	   leurs titres s'y ajoutent — c'est voulu : mieux vaut un titre qui respire
	   qu'un titre à demi caché. */
	:global(html) {
		scroll-padding-top: 4.5rem;
	}

	:global(body) {
		margin: 0;
		background: var(--couleur-fond);
		color: var(--couleur-encre);
		font-family: var(--police-texte); /* Spectral — texte éditorial */
		font-optical-sizing: auto;
		-webkit-font-smoothing: antialiased;
		line-height: 1.6;
	}

	/* --- Base typographique globale (palier « identité typo », charte-graphique.md).
	   On ne refait PAS les composants ici : on pose seulement les défauts. --- */

	/* Titres de haut niveau en Fraunces, sans en abuser (h1/h2 seulement ;
	   les petits titres restent en Spectral tant que le kit n'est pas fait). */
	:global(h1),
	:global(h2) {
		font-family: var(--police-titre);
		font-weight: 600;
		line-height: 1.15;
	}

	/* Interface et données en Public Sans (chiffres tabulaires pour l'alignement). */
	:global(button),
	:global(input),
	:global(select),
	:global(textarea),
	:global(table) {
		font-family: var(--police-ui);
	}

	:global(th),
	:global(td) {
		font-variant-numeric: tabular-nums;
	}

	/* --- Coquille « inventaire » (palier 2). Filet d'accent en tête, masthead
	   aligné sur la colonne de contenu, nav en petites capitales. --- */
	/* Bandeau de tête « affiche » : aplat navy, pleine largeur, texte ivoire. */
	/* Header FIXÉ EN TÊTE (2026-08-08, phase 3). Il reste dans le flux — `sticky` et
	   non `fixed` : la page n'a donc aucune compensation de hauteur à faire, et le
	   pied de page comme les ancres continuent de se comporter normalement.
	   Le fond reste l'aplat navy de la couverture, PLEINEMENT opaque : du texte
	   éditorial qui défile dessous doit disparaître, pas transparaître. Pas de flou,
	   pas d'ombre portée — seulement un filet clair très discret, qui suffit à poser
	   le bandeau au-dessus du contenu. */
	header {
		position: sticky;
		top: 0;
		z-index: 20;
		background: var(--cadre-fond);
		border-bottom: 1px solid rgba(238, 240, 243, 0.12);
	}

	.masthead {
		max-width: var(--largeur-max);
		margin: 0 auto;
		padding: var(--espace-4) var(--espace-5);
		display: flex;
		flex-wrap: wrap;
		align-items: center;
		justify-content: space-between;
		gap: var(--espace-2) var(--espace-5);
	}

	.marque {
		font-family: var(--police-titre);
		font-size: var(--taille-l);
		font-weight: 600;
		letter-spacing: -0.01em;
		color: var(--cadre-encre);
		text-decoration: none;
	}

	nav ul {
		display: flex;
		flex-wrap: wrap;
		gap: var(--espace-4);
		list-style: none;
		margin: 0;
		padding: 0;
		font-family: var(--police-ui);
	}

	/* Le MENU n'est pas un lien éditorial : il ne porte donc pas le soulignement
	   permanent adopté le 2026-08-08 pour le texte courant (charte § 9). Ici, la
	   position dans le bandeau suffit à dire qu'on peut cliquer ; c'est l'état
	   ACTIF qui a besoin d'un signe, pas la nature du lien.
	   Le filet vit sous le libellé seul (le lien est en ligne) : ni bouton, ni
	   pastille, ni carte. */
	nav a {
		display: inline-block;
		padding-bottom: 2px;
		color: var(--cadre-encre-douce);
		text-decoration: none;
		border-bottom: 2px solid transparent;
		transition: color 140ms ease, border-color 140ms ease;
	}

	nav a:hover {
		color: var(--cadre-encre);
		border-bottom-color: rgba(238, 240, 243, 0.35);
	}

	/* Rubrique courante : deux signes, la graisse et le filet d'accent. La couleur
	   seule ne suffirait pas. L'état vient d'`aria-current`, jamais d'une classe
	   décorative posée à part. */
	nav a[aria-current='page'] {
		color: var(--cadre-encre);
		font-weight: 600;
		border-bottom-color: var(--accent-vermillon);
	}

	nav a:focus-visible {
		outline: 2px solid var(--cadre-encre);
		outline-offset: 3px;
		border-radius: 2px;
	}

	@media (prefers-reduced-motion: reduce) {
		nav a {
			transition: none;
		}
	}


	main {
		max-width: var(--largeur-max);
		margin: 0 auto;
		padding: var(--espace-6) var(--espace-5);
	}

	/* Accueil : couverture pleine page, aucune contrainte ni marge. */
	main.pleine {
		max-width: none;
		margin: 0;
		padding: 0;
	}

	/* Pied au même registre que le bandeau (cadre l'affiche). */
	footer {
		background: var(--cadre-fond);
		color: var(--cadre-encre-douce);
		font-family: var(--police-ui);
		font-size: var(--taille-s);
		margin-top: var(--espace-6);
	}

	.footer-interieur {
		max-width: var(--largeur-max);
		margin: 0 auto;
		padding: var(--espace-5) var(--espace-5);
		display: grid;
		grid-template-columns: minmax(15rem, 0.8fr) minmax(20rem, 1.2fr);
		gap: var(--espace-5);
		align-items: start;
	}

	.footer-auteur,
	.footer-liens,
	.footer-source {
		margin: 0;
	}

	.footer-auteur {
		font-family: var(--police-titre);
		font-size: var(--taille-m);
		font-weight: 600;
		color: var(--cadre-encre);
	}

	.footer-liens {
		display: flex;
		flex-wrap: wrap;
		gap: 0.35rem var(--espace-4);
		margin-top: var(--espace-2);
	}

	.footer-liens a {
		color: var(--cadre-encre);
		text-underline-offset: 0.18em;
	}

	.footer-liens a:hover,
	.footer-liens a:focus-visible {
		text-decoration-thickness: 2px;
	}

	.footer-source {
		line-height: 1.55;
	}

	/* Petit écran : les quatre entrées et le nom du projet ne tiennent pas sur une
	   ligne — « Explorer les artistes » fait à lui seul la moitié de la largeur. Le
	   bandeau passe donc sobrement sur DEUX lignes, le nom au-dessus, le menu
	   dessous, tous deux calés à gauche. Pas de menu escamotable : quatre entrées se
	   montrent, elles ne se cachent pas derrière un bouton. */
	@media (max-width: 620px) {
		.masthead {
			flex-direction: column;
			align-items: flex-start;
			gap: var(--espace-3);
			padding: var(--espace-3) var(--espace-4);
		}

		.marque {
			font-size: var(--taille-m);
		}

		nav ul {
			gap: var(--espace-3) var(--espace-4);
			font-size: var(--taille-s);
		}

		/* Le bandeau à deux lignes est plus haut : les ancres réservent d'autant. */
		:global(html) {
			scroll-padding-top: 7.5rem;
		}

		.footer-interieur {
			grid-template-columns: 1fr;
			gap: var(--espace-4);
			padding: var(--espace-5) var(--espace-4);
		}
	}
</style>
