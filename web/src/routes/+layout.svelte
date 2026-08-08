<script>
	import '$lib/styles/tokens.css';
	import '$lib/styles/fonts.css';
	import favicon from '$lib/assets/favicon.svg';
	import { page } from '$app/stores';

	let { children } = $props();

	// Page courante = accueil sur « / » exact, sinon préfixe de la route.
	const estActif = (href) =>
		href === '/' ? $page.url.pathname === '/' : $page.url.pathname.startsWith(href);

	// L'accueil est une couverture pleine page : la coquille (masthead) y est masquée.
	const estAccueil = $derived($page.url.pathname === '/');

	// Routes en PLEINE LARGEUR (direction « affiche ») : accueil + pages refondues.
	// Elles gèrent leurs propres gouttières ; les pages pas encore refondues gardent
	// la colonne centrée.
	const estPleine = $derived(
		$page.url.pathname === '/' ||
			$page.url.pathname.startsWith('/projet') ||
			$page.url.pathname.startsWith('/artistes') ||
			$page.url.pathname.startsWith('/methode')
	);

	// Les rubriques en réserve (Les révisions, La carte) ne figurent pas ici : leur
	// code et leurs données restent au dépôt, hors de la navigation publique tant
	// qu'elles ne sont pas publiées — elles seront la matière d'autres volumes.
	//
	// Navigation publique FINALE du volume 1 (phase 7, 2026-08-02) : quatre entrées,
	// dans l'ordre de lecture. « Comprendre les mentions » en est sortie — ses
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
		{ titre: 'Explorer les artistes', href: '/artistes' },
		{ titre: 'Méthode', href: '/methode' }
	];
</script>

<svelte:head>
	<link rel="icon" href={favicon} />
</svelte:head>

{#if !estAccueil}
<header>
	<!-- Charte v2 : bandeau navy (registre de la couverture), texte ivoire. -->
	<div class="masthead">
		<a class="marque" href="/">L'inventaire du doute</a>
		<nav aria-label="Navigation principale">
			<ul>
				{#each briques as brique (brique.href)}
					<li>
						<a
							href={brique.href}
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

{#if !estAccueil}
<footer>
	<p>
		Source unique : base Joconde (Ministère de la Culture), Licence Ouverte 2.0.
		Ce projet n'authentifie aucune œuvre — il restitue ce que les musées ont
		eux-mêmes publié.
	</p>
</footer>
{/if}

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

	footer p {
		max-width: var(--largeur-max);
		margin: 0 auto;
		padding: var(--espace-5) var(--espace-5);
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
	}
</style>
