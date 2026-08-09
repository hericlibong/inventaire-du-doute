<script>
	// Choix du musée dans l'onglet Œuvres — bouton + liste, à la place du `<select>`
	// natif (2026-08-08).
	//
	// Ce composant ne décide RIEN : il affiche des musées et rend un code. Le
	// filtrage, le recomptage des mentions, la pagination et l'état partagé avec la
	// carte restent où ils étaient (`choisirMusee` dans OeuvresMaitre). Il n'y a
	// donc pas de second système de filtrage, seulement une autre surface pour le
	// même geste.
	//
	// Pas de champ de recherche : un artiste conserve au plus 24 musées, et une
	// liste de 24 lignes se parcourt à l'œil plus vite qu'elle ne se tape.
	//
	// Clavier : Entrée/Espace ouvre, les flèches déplacent, Début/Fin vont aux
	// extrémités, Entrée/Espace choisit, Échap referme en rendant le focus au
	// déclencheur. Le focus est RÉEL sur chaque option (tabindex -1 + focus()),
	// plutôt qu'un `aria-activedescendant` : moins d'état à tenir, et le navigateur
	// fait défiler la liste tout seul.
	import { oeuvres as motOeuvres } from '$lib/joconde.js';

	// musees : [{ code, nom, ville, n }] · total : œuvres toutes provenances
	// valeur : code Muséofile ou null · choisir : (code|null) => void
	let { musees, total, valeur = null, choisir } = $props();

	let ouvert = $state(false);
	let racine = $state(null);
	let declencheur = $state(null);
	let liste = $state(null);

	// « Tous les musées » est une option comme les autres, en tête.
	const options = $derived([
		{ code: null, nom: 'Tous les musées', ville: '', n: total },
		...musees
	]);
	const courant = $derived(options.find((o) => o.code === valeur) ?? options[0]);
	const libelle = (o) => (o.ville ? `${o.nom}, ${o.ville}` : o.nom);

	function ouvrir() {
		ouvert = true;
		// Le focus va sur l'option sélectionnée : on reprend la lecture où elle est,
		// pas en haut d'une liste de vingt-quatre lignes.
		queueMicrotask(() => optionAt(Math.max(0, options.findIndex((o) => o.code === valeur)))?.focus());
	}

	function fermer({ rendreFocus = true } = {}) {
		if (!ouvert) return;
		ouvert = false;
		if (rendreFocus) declencheur?.focus();
	}

	const optionAt = (i) => liste?.querySelectorAll('[role="option"]')[i] ?? null;
	const indexActif = () =>
		[...(liste?.querySelectorAll('[role="option"]') ?? [])].indexOf(document.activeElement);

	function prendre(code) {
		choisir(code);
		fermer();
	}

	function auClavierDeclencheur(e) {
		if (e.key === 'Enter' || e.key === ' ' || e.key === 'ArrowDown') {
			e.preventDefault();
			ouvrir();
		}
	}

	function auClavierListe(e) {
		const n = options.length;
		const i = indexActif();
		if (e.key === 'Escape') {
			e.preventDefault();
			fermer();
		} else if (e.key === 'ArrowDown') {
			e.preventDefault();
			optionAt(Math.min(n - 1, i + 1))?.focus();
		} else if (e.key === 'ArrowUp') {
			e.preventDefault();
			optionAt(Math.max(0, i - 1))?.focus();
		} else if (e.key === 'Home') {
			e.preventDefault();
			optionAt(0)?.focus();
		} else if (e.key === 'End') {
			e.preventDefault();
			optionAt(n - 1)?.focus();
		} else if (e.key === 'Enter' || e.key === ' ') {
			e.preventDefault();
			if (i >= 0) prendre(options[i].code);
		} else if (e.key === 'Tab') {
			// Sortir au clavier ferme, sans voler le focus au suivant.
			fermer({ rendreFocus: false });
		}
	}

	// Clic hors du composant : on referme sans rendre le focus (l'utilisateur est
	// déjà parti ailleurs).
	function auClicDocument(e) {
		if (ouvert && racine && !racine.contains(e.target)) fermer({ rendreFocus: false });
	}
</script>

<svelte:window onpointerdown={auClicDocument} />

<div class="choix" bind:this={racine}>
	<button
		type="button"
		class="declencheur"
		bind:this={declencheur}
		aria-haspopup="listbox"
		aria-expanded={ouvert}
		onclick={() => (ouvert ? fermer() : ouvrir())}
		onkeydown={auClavierDeclencheur}
	>
		<span class="d-nom">{libelle(courant)}</span>
		<span class="d-n">{motOeuvres(courant.n)}</span>
		<span class="chevron" aria-hidden="true" class:ouvert></span>
	</button>

	{#if ouvert}
		<ul class="liste" role="listbox" aria-label="Choisir un musée" bind:this={liste} onkeydown={auClavierListe}>
			{#each options as o, i (o.code ?? 'tous')}
				<!-- Le clavier de la liste est géré UNE FOIS sur le <ul> (`auClavierListe`,
				     motif listbox : flèches, Début, Fin, Entrée, Espace, Échap). Le
				     compilateur ne voit pas cette délégation et réclame un gestionnaire
				     sur chaque option ; en ajouter 25 dupliquerait le même code sans rien
				     changer au comportement, vérifié touche par touche le 2026-08-08. -->
				<!-- svelte-ignore a11y_click_events_have_key_events -->
				<!-- svelte-ignore a11y_no_noninteractive_element_interactions -->
				<li
					role="option"
					tabindex="-1"
					aria-selected={o.code === valeur}
					class:choisi={o.code === valeur}
					class:tous={o.code === null}
					aria-label="{libelle(o)}, {motOeuvres(o.n)}"
					onclick={() => prendre(o.code)}
				>
					<!-- La coche double la graisse et le fond : l'état choisi ne repose
					     jamais sur la seule couleur. -->
					<span class="coche" aria-hidden="true">{o.code === valeur ? '✓' : ''}</span>
					<span class="o-nom">{libelle(o)}</span>
					<!-- Le nombre seul à l'écran ; le libellé accessible du <li> dit
					     « N œuvres », accordé. -->
					<span class="o-n" aria-hidden="true">{o.n}</span>
				</li>
			{/each}
		</ul>
	{/if}
</div>

<style>
	.choix {
		position: relative;
		min-width: 0;
		flex: 1 1 22rem;
		max-width: 30rem;
	}

	/* Déclencheur : nom à gauche, effectif à droite, chevron. Fond de papier et
	   filet fin — rien du gris de formulaire système. */
	.declencheur {
		display: flex;
		align-items: center;
		gap: 0.6rem;
		width: 100%;
		padding: 0.5rem 0.7rem;
		background: var(--surface-carte);
		border: 1px solid var(--couleur-trait);
		border-radius: 2px;
		font-family: var(--police-ui);
		font-size: var(--taille-s);
		color: var(--couleur-encre);
		text-align: left;
		cursor: pointer;
	}

	.declencheur:hover {
		border-color: var(--couleur-encre-douce);
	}

	.declencheur:focus-visible {
		outline: var(--focus-anneau);
		outline-offset: 2px;
	}

	.d-nom {
		flex: 1;
		min-width: 0;
		overflow: hidden;
		text-overflow: ellipsis;
		white-space: nowrap;
	}

	.d-n {
		flex: none;
		color: var(--couleur-encre-douce);
		font-variant-numeric: tabular-nums;
	}

	/* Chevron dessiné en CSS : pas d'icône à charger, pas de glyphe dépendant de
	   la police. */
	.chevron {
		flex: none;
		width: 0.55rem;
		height: 0.55rem;
		border-right: 1.5px solid var(--couleur-encre-douce);
		border-bottom: 1.5px solid var(--couleur-encre-douce);
		transform: translateY(-2px) rotate(45deg);
		transition: transform 140ms ease;
	}

	.chevron.ouvert {
		transform: translateY(1px) rotate(-135deg);
	}

	.liste {
		position: absolute;
		z-index: 15;
		top: calc(100% + 4px);
		left: 0;
		width: 100%;
		max-height: 19rem;
		overflow-y: auto;
		margin: 0;
		padding: 0;
		list-style: none;
		background: var(--surface-carte);
		border: 1px solid var(--couleur-trait);
		border-radius: 2px;
		box-shadow: 0 3px 10px rgba(43, 30, 20, 0.1);
	}

	.liste li {
		display: grid;
		/* Colonne de droite FIXE : les effectifs s'alignent, on compare d'un coup
		   d'œil. Le nom prend ce qui reste et passe à la ligne s'il est long — on
		   ne coupe pas le nom d'un musée. */
		grid-template-columns: 1.1rem 1fr 3.2rem;
		align-items: baseline;
		gap: 0.5rem;
		padding: 0.5rem 0.7rem;
		font-family: var(--police-ui);
		font-size: var(--taille-s);
		line-height: 1.35;
		color: var(--couleur-encre);
		cursor: pointer;
	}

	.liste li:hover {
		background: rgba(43, 30, 20, 0.05);
	}

	.liste li:focus-visible {
		outline: var(--focus-anneau);
		outline-offset: -2px;
	}

	/* « Tous les musées » ouvre la liste et s'en détache par un filet : il ne
	   désigne pas un lieu, il les lève tous. */
	.liste li.tous {
		border-bottom: 1px solid var(--couleur-trait);
	}

	.liste li.choisi {
		background: rgba(53, 87, 138, 0.08);
		font-weight: 700;
	}

	.coche {
		color: var(--accent-cobalt);
		font-size: 0.8em;
	}

	.o-n {
		text-align: right;
		color: var(--couleur-encre-douce);
		font-variant-numeric: tabular-nums;
	}

	.liste li.choisi .o-n {
		color: inherit;
	}

	@media (prefers-reduced-motion: reduce) {
		.chevron {
			transition: none;
		}
	}
</style>
