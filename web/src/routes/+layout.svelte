<script>
	import '$lib/styles/tokens.css';
	import favicon from '$lib/assets/favicon.svg';

	let { children } = $props();

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
	<a class="marque" href="/">L'inventaire du doute</a>
	<nav aria-label="Les briques">
		<ul>
			{#each briques as brique (brique.href)}
				<li>
					{#if brique.prete}
						<a href={brique.href}>{brique.titre}</a>
					{:else}
						<span class="a-venir" title="À venir">{brique.titre}</span>
					{/if}
				</li>
			{/each}
		</ul>
	</nav>
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
		font-family: var(--police-texte);
		line-height: 1.6;
	}

	header {
		border-bottom: 1px solid var(--couleur-trait);
		padding: 1rem 1.5rem;
	}

	.marque {
		font-family: var(--police-titre);
		font-size: 1.4rem;
		font-weight: bold;
		color: var(--couleur-encre);
		text-decoration: none;
	}

	nav ul {
		display: flex;
		flex-wrap: wrap;
		gap: 1.25rem;
		list-style: none;
		margin: 0.75rem 0 0;
		padding: 0;
	}

	nav a {
		color: var(--couleur-accent);
		text-decoration: none;
	}

	nav a:hover {
		text-decoration: underline;
	}

	.a-venir {
		color: var(--couleur-encre-douce);
		opacity: 0.5;
		cursor: default;
	}

	main {
		max-width: var(--largeur-max);
		margin: 0 auto;
		padding: 2rem 1.5rem;
	}

	footer {
		max-width: var(--largeur-max);
		margin: 0 auto;
		padding: 2rem 1.5rem 3rem;
		border-top: 1px solid var(--couleur-trait);
		color: var(--couleur-encre-douce);
		font-size: 0.85rem;
	}
</style>
