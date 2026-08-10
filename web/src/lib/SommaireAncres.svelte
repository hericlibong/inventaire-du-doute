<script>
	// RAIL DE SOMMAIRE d'une page longue — extrait de « Méthode et limites » le
	// 2026-08-04, quand la page « Présentation » en a eu besoin à son tour. Le site
	// n'a qu'UN système de navigation interne : le comportement, les repères de
	// lecture et les styles vivent ici ; chaque page ne fournit que sa liste de
	// sections et la grille qui accueille le rail.
	//
	//   sections   — [[ancre, libellé court], …], dans l'ordre de la page. Les
	//                titres complets restent dans les <h2> : un rail de 16 rem ne
	//                les tiendrait pas. Une entrée peut porter un TROISIÈME élément —
	//                [[ancre, libellé], …] — : les sous-parties de la section, en
	//                retrait sous elle (2026-08-05). Ce n'est pas une seconde
	//                navigation : la liste est aplatie avant d'être mesurée, et
	//                mesure, défilement et focus restent ceux du rail.
	//   ancreHaut  — id de l'élément qui reçoit le focus au retour en haut (le h1).
	//   etiquette  — nom accessible du <nav>.
	//
	// Chaque section visée doit porter son id et `tabindex="-1"` (cible du focus au
	// clic), et un `scroll-margin-top` pour ne pas se coller au bord de la fenêtre.
	//
	// Rien d'automatique ne bouge à l'écran : la page ne prend jamais la main sur le
	// défilement du lecteur.
	import { untrack } from 'svelte';

	let { sections, ancreHaut = 'haut-de-page', etiquette = 'Sections de la page' } = $props();

	// Toutes les ancres, principales et secondaires, dans l'ordre de la page : c'est
	// cette liste-là qui est mesurée et qui répond aux ancres reçues dans l'URL.
	const ancres = sections.flatMap(([ancre, , sous = []]) => [ancre, ...sous.map(([a]) => a)]);

	// Section principale à laquelle appartient une ancre — elle-même si c'est une
	// entrée de premier niveau. Sert à garder la section allumée pendant qu'on lit
	// l'une de ses sous-parties.
	const sectionDe = (id) =>
		sections.find(([ancre, , sous = []]) => ancre === id || sous.some(([a]) => a === id))?.[0] ??
		null;

	// La liste est fixe pour une page donnée : on la lit une fois, sans en faire une
	// dépendance (untrack), pour que le premier lien soit déjà marqué au rendu serveur.
	let actif = $state(untrack(() => sections[0]?.[0] ?? null));
	let hautVisible = $state(false);
	let sectionActive = $derived(sectionDe(actif));

	// Section DEMANDÉE par un clic du sommaire ou par l'ancre de l'URL. Elle l'emporte
	// sur la mesure jusqu'au prochain geste de défilement du lecteur : quand la page
	// est déjà en butée basse, les deux dernières sections tiennent dans le même écran
	// et la mesure désignerait la dernière, alors que le lecteur vient d'en demander
	// une autre. Le rail doit répondre de ce qu'on lui a demandé.
	//
	// Volontairement PAS un $state : l'affichage passe par `actif`. Réactive, elle
	// serait lue et écrite par le même effet, qui se relancerait sans fin.
	let demandee = null;

	// Repérage de la section courante. Mesure directe à chaque défilement plutôt
	// qu'un IntersectionObserver : quelques éléments, un calcul par image, et
	// surtout une règle qu'on peut énoncer — « la dernière section dont le titre est
	// passé au-dessus du quart supérieur de la fenêtre ». Les cas limites (haut de
	// page, dernière section trop courte pour occuper l'écran) sont traités
	// explicitement.
	$effect(() => {
		const cibles = ancres.map((ancre) => document.getElementById(ancre)).filter(Boolean);
		if (!cibles.length) return;

		let attendue = false;

		const mesurer = () => {
			attendue = false;
			const seuil = window.innerHeight * 0.25;
			let courante = cibles[0];
			for (const el of cibles) {
				if (el.getBoundingClientRect().top <= seuil) courante = el;
			}
			// Arrivé au pied de page, la dernière section est la bonne réponse même
			// si elle n'a pas atteint le seuil (elle ne le pourra jamais).
			const fin =
				window.scrollY + window.innerHeight >= document.documentElement.scrollHeight - 4;
			if (fin) courante = cibles[cibles.length - 1];

			actif = demandee ?? courante.id;
			hautVisible = window.scrollY > window.innerHeight;
		};

		const auDefilement = () => {
			if (attendue) return;
			attendue = true;
			requestAnimationFrame(mesurer);
		};

		// Un geste de défilement du lecteur rend la main à la mesure.
		const relacher = () => {
			demandee = null;
			auDefilement();
		};

		// Une ancre reçue dans l'URL est une demande, au même titre qu'un clic dans le
		// rail : le repère doit désigner la section reçue, même quand la page est déjà
		// en butée basse et que la mesure pencherait pour la suivante. Vaut au
		// chargement comme à chaque changement d'ancre (lien interne, bouton Retour).
		const lireAncre = () => {
			const recue = decodeURIComponent(window.location.hash.slice(1));
			demandee = ancres.includes(recue) ? recue : null;
			auDefilement();
		};

		lireAncre();
		mesurer();
		// Arrivée par un lien vers une ancre : le navigateur saute à la cible avant
		// que cette mesure ne soit installée, sans émettre d'événement de défilement.
		// On remesure donc une fois la page posée, sinon le rail annoncerait la
		// première section alors qu'on est à la quatrième.
		const differee = setTimeout(mesurer, 250);

		window.addEventListener('scroll', auDefilement, { passive: true });
		window.addEventListener('resize', auDefilement);
		window.addEventListener('hashchange', lireAncre);
		window.addEventListener('wheel', relacher, { passive: true });
		window.addEventListener('touchstart', relacher, { passive: true });
		window.addEventListener('keydown', relacher);
		return () => {
			clearTimeout(differee);
			window.removeEventListener('scroll', auDefilement);
			window.removeEventListener('resize', auDefilement);
			window.removeEventListener('hashchange', lireAncre);
			window.removeEventListener('wheel', relacher);
			window.removeEventListener('touchstart', relacher);
			window.removeEventListener('keydown', relacher);
		};
	});

	// Défilement doux, sauf si le système demande de limiter les animations.
	const douceur = () =>
		window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth';

	// Clic sur le sommaire : on garde le comportement natif (l'ancre reste dans
	// l'URL, le lien fonctionne sans JavaScript) et on y ajoute le défilement doux
	// et le passage du focus clavier à la section atteinte.
	function allerA(evenement, ancre) {
		const cible = document.getElementById(ancre);
		if (!cible) return;
		evenement.preventDefault();
		demandee = ancre;
		actif = ancre;
		cible.scrollIntoView({ behavior: douceur(), block: 'start' });
		cible.focus({ preventScroll: true });
		history.replaceState(null, '', `#${ancre}`);
	}

	function retourHaut() {
		demandee = null;
		window.scrollTo({ top: 0, behavior: douceur() });
		document.getElementById(ancreHaut)?.focus({ preventScroll: true });
		history.replaceState(null, '', window.location.pathname);
	}
</script>

<nav class="sommaire" aria-label={etiquette}>
	<label class="sommaire-mobile">
		<span>Section</span>
		<select
			aria-label={etiquette}
			value={sectionActive ?? sections[0]?.[0]}
			onchange={(e) => allerA(e, e.currentTarget.value)}
		>
			{#each sections as [ancre, titre] (ancre)}
				<option value={ancre}>{titre}</option>
			{/each}
		</select>
	</label>

	<ol class="sommaire-liste">
		{#each sections as [ancre, titre, sous = []], i (ancre)}
			<li>
				<a
					href="#{ancre}"
					class:actif={ancre === actif}
					class:branche={sectionActive === ancre && actif !== ancre}
					aria-current={ancre === actif ? 'true' : undefined}
					onclick={(e) => allerA(e, ancre)}
				>
					<span class="num">{i + 1}</span>{titre}
				</a>

				<!-- Sous-parties : mêmes liens, même mécanisme, un cran en retrait. -->
				{#if sous.length}
					<ol class="sous">
						{#each sous as [sousAncre, sousTitre] (sousAncre)}
							<li>
								<a
									href="#{sousAncre}"
									class:actif={sousAncre === actif}
									aria-current={sousAncre === actif ? 'true' : undefined}
									onclick={(e) => allerA(e, sousAncre)}
								>
									{sousTitre}
								</a>
							</li>
						{/each}
					</ol>
				{/if}
			</li>
		{/each}
	</ol>
</nav>

<!-- Retour en haut : n'apparaît qu'après un écran de défilement, jamais au-dessus
     du texte (il se range dans la gouttière dès qu'il y a la place). Position
     fixe : sa place dans le document n'a pas d'importance pour la mise en page. -->
<button class="retour-haut" class:visible={hautVisible} inert={!hautVisible} onclick={retourHaut}>
	<span aria-hidden="true">↑</span> <span class="libelle">Haut de page</span>
</button>

<style>
	/* Sommaire : repères de lecture, pas un tableau de bord. Collant sur ordinateur.
	   La page hôte fournit la colonne ; le rail s'y accroche. */
	.sommaire {
		position: sticky;
		top: var(--espace-5);
	}

	.sommaire-mobile {
		display: none;
	}

	.sommaire ol {
		list-style: none;
		margin: 0;
		padding: 0;
		font-family: var(--police-ui);
		font-size: var(--taille-s);
		border-left: var(--filet);
	}

	.sommaire li + li {
		margin-top: var(--espace-2);
	}

	.sommaire a {
		display: flex;
		gap: 0.6rem;
		align-items: baseline;
		color: var(--couleur-encre-douce);
		text-decoration: none;
		padding-left: var(--espace-3);
		margin-left: -1px;
		border-left: 2px solid transparent;
	}

	.sommaire a:hover {
		color: var(--couleur-encre);
		border-left-color: var(--accent-cobalt);
	}

	/* Section en cours de lecture : le filet se remplit. Le repère est doublé par
	   aria-current, pour ne pas dépendre de la seule couleur. */
	.sommaire a.actif {
		color: var(--couleur-encre);
		border-left-color: var(--accent-cobalt);
		font-weight: 600;
	}

	/* Section dont on lit une sous-partie : allumée, mais sans le gras réservé à
	   l'entrée exactement visée. Le rail montre ainsi où l'on est à deux niveaux. */
	.sommaire a.branche {
		color: var(--couleur-encre);
		border-left-color: var(--accent-cobalt);
	}

	/* Sous-parties : décalées sous le libellé du parent (la gouttière du numéro),
	   petit corps, sans numéro — elles se lisent comme une dépendance, pas comme
	   une seconde liste. */
	.sommaire .sous {
		list-style: none;
		margin: var(--espace-2) 0 var(--espace-3);
		padding: 0;
		font-size: var(--taille-xs);
	}

	.sommaire .sous li + li {
		margin-top: var(--espace-1);
	}

	.sommaire .sous a {
		padding-left: calc(var(--espace-3) + 1.35rem);
		line-height: 1.35;
	}

	.sommaire .num {
		font-variant-numeric: tabular-nums;
		color: var(--couleur-encre-douce);
	}

	.sommaire a.actif .num {
		color: var(--accent-cobalt);
	}

	/* Retour en haut : pastille discrète en bas de fenêtre, du registre UI.
	   Absente tant qu'on n'a pas défilé d'au moins un écran. */
	.retour-haut {
		position: fixed;
		right: clamp(1rem, 3vw, 2rem);
		bottom: clamp(1rem, 3vw, 2rem);
		display: inline-flex;
		align-items: center;
		gap: var(--espace-2);
		padding: var(--espace-2) var(--espace-3);
		background: var(--surface-carte);
		color: var(--couleur-encre-douce);
		border: var(--filet);
		border-radius: var(--rayon-m);
		box-shadow: var(--ombre-douce);
		font-size: var(--taille-xs);
		cursor: pointer;
		opacity: 0;
		visibility: hidden;
		transform: translateY(0.4rem);
		transition:
			opacity 0.2s ease,
			transform 0.2s ease,
			visibility 0.2s;
	}

	.retour-haut.visible {
		opacity: 1;
		visibility: visible;
		transform: none;
	}

	.retour-haut:hover {
		color: var(--couleur-encre);
		border-color: var(--couleur-encre-douce);
	}

	/* Le mouvement est un confort, pas une information : on le retire si le
	   système demande de limiter les animations. */
	@media (prefers-reduced-motion: reduce) {
		.retour-haut {
			transition: none;
			transform: none;
		}
	}

	@media print {
		.sommaire,
		.retour-haut {
			display: none;
		}
	}

	/* Petit écran : le rail devient une commande compacte qui reste disponible sous
	   le header. La liste horizontale précédente disparaissait dès qu'on atteignait
	   la première section et obligeait à remonter pour changer de destination. */
	@media (max-width: 760px) {
		.sommaire {
			position: sticky;
			top: 4.5rem;
			z-index: 15;
			padding: 0.45rem 0;
			background: color-mix(in srgb, var(--couleur-fond) 96%, transparent);
			border-top: 1px solid var(--couleur-trait-clair);
			border-bottom: 1px solid var(--couleur-trait);
		}

		.sommaire-mobile {
			display: grid;
			grid-template-columns: auto minmax(0, 1fr);
			align-items: center;
			gap: var(--espace-3);
			font-family: var(--police-ui);
			font-size: var(--taille-xs);
			font-weight: 700;
			letter-spacing: 0.06em;
			text-transform: uppercase;
			color: var(--couleur-encre-douce);
		}

		.sommaire-mobile select {
			min-width: 0;
			width: 100%;
			padding: 0.48rem 2rem 0.48rem 0.65rem;
			border: 1px solid var(--couleur-trait);
			border-radius: 2px;
			background: var(--surface-carte);
			color: var(--couleur-encre);
			font-size: var(--taille-s);
			font-weight: 600;
			letter-spacing: 0;
			text-transform: none;
		}

		.sommaire-liste {
			display: none;
		}

		/* Sur petit écran, le bouton se réduit à sa flèche pour couvrir le moins de
		   texte possible. Le libellé reste dans le document (nom accessible du
		   bouton), seulement retiré de la vue. */
		.retour-haut {
			padding: var(--espace-2);
			border-radius: 50%;
			line-height: 1;
		}

		.retour-haut .libelle {
			position: absolute;
			width: 1px;
			height: 1px;
			overflow: hidden;
			clip-path: inset(50%);
			white-space: nowrap;
		}
	}

	@media (max-width: 620px) {
		.sommaire {
			top: 6rem;
		}
	}
</style>
