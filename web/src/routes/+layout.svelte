<script>
	import '$lib/styles/tokens.css';
	import '$lib/styles/fonts.css';
	import favicon from '$lib/assets/favicon.svg';
	import { page } from '$app/stores';

	let { children } = $props();

	// Page courante = accueil sur « / » exact, sinon préfixe de la route.
	const estActif = (href) =>
		href === '/' ? $page.url.pathname === '/' : $page.url.pathname.startsWith(href);

	// Coquille de navigation : une brique = une route. Seule l'accueil existe
	// au stade du socle ; les autres sont affichées « à venir » pour montrer
	// la structure éditoriale sans casser le pré-rendu (pas de lien mort).
	const briques = [
		{ titre: 'Accueil', href: '/', prete: true },
		{ titre: 'Les presque', href: '/les-presque', prete: true },
		{ titre: "L'échelle du doute", href: '/echelle', prete: false },
		{ titre: 'Les révisions', href: '/revisions', prete: false },
		{ titre: 'La carte', href: '/carte', prete: false },
		{ titre: 'Méthode et limites', href: '/methode', prete: false }
	];
</script>

<svelte:head>
	<link rel="icon" href={favicon} />
</svelte:head>

<header>
	<div class="masthead">
		<a class="marque" href="/">L'inventaire du doute</a>
		<nav aria-label="Navigation principale">
			<ul>
				{#each briques as brique (brique.href)}
					<li>
						{#if brique.prete}
							<a
								href={brique.href}
								class:actif={estActif(brique.href)}
								aria-current={estActif(brique.href) ? 'page' : undefined}
							>
								{brique.titre}
							</a>
						{:else}
							<span class="a-venir" title="À venir">{brique.titre}</span>
						{/if}
					</li>
				{/each}
			</ul>
		</nav>
	</div>
</header>

<main>
	{@render children()}
</main>

<footer>
	<p>
		Source unique : base Joconde (Ministère de la Culture), Licence Ouverte 2.0.
		Ce projet n'authentifie aucune œuvre — il restitue ce que les musées ont
		eux-mêmes publié.
	</p>
</footer>

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
	header {
		border-top: 3px solid var(--couleur-accent);
		border-bottom: var(--filet);
	}

	.masthead {
		max-width: var(--largeur-max);
		margin: 0 auto;
		padding: var(--espace-4) var(--espace-5);
		display: flex;
		flex-wrap: wrap;
		align-items: baseline;
		justify-content: space-between;
		gap: var(--espace-2) var(--espace-5);
	}

	.marque {
		font-family: var(--police-titre);
		font-size: var(--taille-l);
		font-weight: 600;
		letter-spacing: -0.01em;
		color: var(--couleur-encre);
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
	.a-venir {
		font-size: var(--taille-xs);
		text-transform: uppercase;
		letter-spacing: 0.07em;
		font-weight: 500;
		text-decoration: none;
		color: var(--couleur-encre-douce);
		padding-bottom: 2px;
		border-bottom: 2px solid transparent;
	}

	nav a:hover {
		color: var(--couleur-encre);
	}

	nav a.actif {
		color: var(--couleur-accent);
		border-bottom-color: var(--couleur-accent);
	}

	.a-venir {
		opacity: 0.45;
		cursor: default;
	}

	main {
		max-width: var(--largeur-max);
		margin: 0 auto;
		padding: var(--espace-6) var(--espace-5);
	}

	footer {
		max-width: var(--largeur-max);
		margin: 0 auto;
		padding: var(--espace-6) var(--espace-5) 3rem;
		border-top: var(--filet);
		color: var(--couleur-encre-douce);
		font-family: var(--police-ui);
		font-size: var(--taille-s);
	}
</style>
