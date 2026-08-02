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
			$page.url.pathname.startsWith('/presentation') ||
			$page.url.pathname.startsWith('/les-presque') ||
			$page.url.pathname.startsWith('/methode')
	);

	// Les rubriques en réserve (Les révisions, La carte) ne figurent pas ici : leur
	// code et leurs données restent au dépôt, hors de la navigation publique tant
	// qu'elles ne sont pas publiées — elles seront la matière d'autres volumes.
	//
	// Navigation publique FINALE du volume 1 (phase 7, 2026-08-02) : quatre entrées,
	// dans l'ordre de lecture. « Comprendre les mentions » en est sortie — ses
	// définitions ont rejoint la Présentation, sous le graphique qui les compte, et
	// son ancienne URL redirige.
	//
	// Le champ `prete` et la branche « à venir » ont été SUPPRIMÉS avec elle. Ils
	// permettaient d'afficher une rubrique non publiée en lien inerte ; la consigne
	// est de ne pas annoncer les volumes suivants de cette façon. Retirer le
	// mécanisme, et pas seulement les entrées, évite qu'il resserve un jour.
	const briques = [
		{ titre: 'Accueil', href: '/' },
		{ titre: 'Présentation', href: '/presentation' },
		{ titre: 'Explorer les artistes', href: '/les-presque' },
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
							class:actif={estActif(brique.href)}
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
	header {
		background: var(--cadre-fond);
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

	nav a,

	nav a:hover {
		color: var(--cadre-encre);
	}

	nav a.actif {
		color: var(--cadre-encre);
		border-bottom-color: var(--accent-vermillon);
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
</style>
