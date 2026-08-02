<script>
	// Navigation de la couverture d'accueil (révision 2026-07-18) : des CARTOUCHES
	// éditoriaux intégrés à la fiche claire — rectangles sombres (bleu-encre), texte
	// ivoire, angles quasi droits, largeur adaptée au texte, légèrement décalés. Pas
	// de boutons arrondis, pas d'ombre, pas d'icône. « Explorer les maîtres » = entrée
	// principale (plus large, plus lourde, accent cobalt, cible généreuse). Routes
	// réelles (dont /echelle = « Comprendre les mentions »).
	import { page } from '$app/stores';

	// `decal` = décalage horizontal irrégulier (les liens n'ont ni la même largeur ni
	// un alignement de menu classique). Ils semblent appartenir aux rectangles de
	// l'illustration.
	// Pas de lien « Accueil » : cette navigation ne s'affiche QUE sur la couverture
	// d'accueil (LandingCover) — un lien vers la page où l'on se trouve déjà est inutile
	// (retrait demandé le 2026-07-18). Les autres pages ont « Accueil » dans le header.
	const liens = [
		{ href: '/les-presque', label: 'Explorer les artistes', principal: true, decal: '0rem' },
		{ href: '/echelle', label: 'Comprendre les mentions', decal: '2.8rem' },
		{ href: '/methode', label: 'Méthode', decal: '1.1rem' }
	];

	const courant = (href) =>
		href === '/' ? $page.url.pathname === '/' : $page.url.pathname.startsWith(href);
</script>

<nav class="ednav" aria-label="Navigation principale">
	<ul>
		{#each liens as l (l.href)}
			<li style="--decal: {l.decal}">
				<a
					href={l.href}
					class:principal={l.principal}
					aria-current={courant(l.href) ? 'page' : undefined}
				>
					<span class="trait" aria-hidden="true"></span>
					<span class="cartouche">{l.label}</span>
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
		gap: clamp(0.5rem, 1.6vh, 0.95rem);
	}

	li {
		margin-left: var(--decal);
	}

	a {
		display: inline-flex;
		align-items: center;
		gap: 0.55rem;
		text-decoration: none;
		width: fit-content;
	}

	/* Trait fin prolongeant les lignes de la fiche (sur le fond clair). */
	.trait {
		display: block;
		width: 1.4rem;
		height: 1px;
		background: rgba(38, 32, 24, 0.5);
		transition: width 180ms ease;
	}

	/* Cartouche : rectangle bleu-encre, texte ivoire, angles quasi droits. */
	.cartouche {
		display: block;
		background: #24303d;
		color: #efe9db;
		font-family: var(--police-ui);
		font-weight: 600;
		font-size: clamp(0.9rem, 1.15vw, 1.02rem);
		letter-spacing: 0.01em;
		padding: 0.5rem 0.85rem;
		border-radius: 1px;
		transition: background 180ms ease, transform 180ms ease;
	}

	/* Entrée principale : plus large, plus lourde, fond cobalt discret, cible généreuse. */
	a.principal .cartouche {
		background: #2d4d78;
		font-weight: 700;
		font-size: clamp(1rem, 1.4vw, 1.22rem);
		padding: 0.64rem 1.1rem;
	}

	/* Page courante (Accueil) : repère sobre, non uniquement chromatique. */
	a[aria-current='page'] .trait {
		width: 1.9rem;
		background: #9e2b12;
	}
	a[aria-current='page'] .cartouche {
		box-shadow: inset 0 0 0 1px rgba(239, 233, 219, 0.45);
	}

	/* Survol / focus : léger déplacement, prolongement du trait, fond un peu plus clair. */
	a:hover .cartouche,
	a:focus-visible .cartouche {
		transform: translateX(5px);
		background: #2f3f52;
	}
	a.principal:hover .cartouche,
	a.principal:focus-visible .cartouche {
		background: #35578a;
	}
	a:hover .trait,
	a:focus-visible .trait {
		width: 2.3rem;
	}

	a:focus-visible {
		outline: 2px solid #efe9db;
		outline-offset: 3px;
		border-radius: 2px;
	}

	@media (prefers-reduced-motion: reduce) {
		.trait,
		.cartouche {
			transition: none;
		}
		a:hover .cartouche,
		a:focus-visible .cartouche {
			transform: none;
		}
	}
</style>
