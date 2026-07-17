<script>
	// Navigation éditoriale de la couverture d'accueil : les quatre entrées comme des
	// annotations inscrites sur la « fiche » claire de l'illustration, reliées à ses
	// lignes horizontales. Pas de boutons, pas de cartes, pas de barre. Charbon sur la
	// fiche claire (contraste natif, sans panneau ni voile). Interactions sobres
	// (déplacement ≤ 4 px, prolongement de la ligne, contraste) et accessibles.
	import { page } from '$app/stores';

	// Routes réelles du projet (dont /echelle = « Comprendre les mentions »).
	const liens = [
		{ href: '/', label: 'Accueil' },
		{ href: '/les-presque', label: 'Explorer les maîtres', principal: true },
		{ href: '/echelle', label: 'Comprendre les mentions' },
		{ href: '/methode', label: 'Méthode' }
	];

	const courant = (href) =>
		href === '/' ? $page.url.pathname === '/' : $page.url.pathname.startsWith(href);
</script>

<nav class="ednav" aria-label="Navigation principale">
	<ul>
		{#each liens as l (l.href)}
			<li>
				<a
					href={l.href}
					class:principal={l.principal}
					aria-current={courant(l.href) ? 'page' : undefined}
				>
					<span class="ligne" aria-hidden="true"></span>
					<span class="txt">{l.label}</span>
				</a>
			</li>
		{/each}
	</ul>
</nav>

<style>
	.ednav ul {
		list-style: none;
		margin: 0;
		padding: 0;
		display: flex;
		flex-direction: column;
		gap: clamp(0.7rem, 2.2vh, 1.5rem);
	}

	a {
		display: flex;
		align-items: center;
		gap: 0.7rem;
		text-decoration: none;
		font-family: var(--police-ui);
		font-size: clamp(0.95rem, 1.3vw, 1.15rem);
		letter-spacing: 0.01em;
		/* Charbon sur la fiche claire — contraste natif, pas de panneau. */
		color: #2b2621;
		width: fit-content;
	}

	/* Ligne-annotation : rappelle les lignes horizontales de la fiche. Elle se
	   prolonge au survol/focus (repère non chromatique de l'état actif). */
	.ligne {
		display: block;
		width: 1.6rem;
		height: 2px;
		background: currentColor;
		opacity: 0.55;
		transition: width 180ms ease, opacity 180ms ease;
	}

	.txt {
		transition: transform 180ms ease, color 180ms ease;
	}

	/* Entrée principale : poids légèrement supérieur, ligne un peu plus longue. */
	a.principal {
		font-weight: 700;
		font-size: clamp(1.05rem, 1.5vw, 1.35rem);
	}

	a.principal .ligne {
		width: 2.2rem;
		opacity: 0.75;
	}

	/* Page courante (Accueil) : ligne pleine, marquée sans dépendre de la couleur. */
	a[aria-current='page'] .ligne {
		opacity: 1;
	}

	a[aria-current='page'] .txt {
		font-weight: 700;
	}

	a:hover .ligne,
	a:focus-visible .ligne {
		width: 3rem;
		opacity: 1;
	}

	a:hover .txt,
	a:focus-visible .txt {
		transform: translateX(4px);
		color: #000;
	}

	a:focus-visible {
		outline: 2px solid #1a3a5a;
		outline-offset: 4px;
		border-radius: 2px;
	}

	@media (prefers-reduced-motion: reduce) {
		.ligne,
		.txt {
			transition: none;
		}
		a:hover .txt,
		a:focus-visible .txt {
			transform: none;
		}
	}
</style>
