<script>
	// Légende permanente des mentions de prudence — la clé des couleurs, AVANT
	// interaction (décision utilisateur 2026-07-13). Vit sous la liste des maîtres,
	// commune aux trois vues (graphique / œuvres / carte). Elle réutilise TELS QUELS
	// les libellés publics (header) et les phrases de sens (corps) de
	// familles-public.js : une seule nomenclature, exactement les mêmes mots que les
	// tooltips → le lecteur relie la légende et les infobulles sans effort.
	//
	// Desktop : toujours dépliée (intitulé simple). Mobile : repliable (bouton), pour
	// ne pas repousser la carte. On pilote l'état nous-mêmes plutôt qu'un <details>
	// natif, dont le contenu fermé n'est pas ré-affichable en CSS selon la largeur.
	import { onMount } from 'svelte';
	import { FAMILLE_PUBLIC, ORDRE_FAMILLES } from '$lib/familles-public.js';

	let mobile = $state(false);
	let ouvert = $state(true); // desktop par défaut ; refermé au montage en mobile

	onMount(() => {
		const mq = window.matchMedia('(max-width: 720px)');
		const sync = () => {
			mobile = mq.matches;
			ouvert = !mq.matches; // dépliée sur desktop, repliée sur mobile
		};
		sync();
		mq.addEventListener('change', sync);
		return () => mq.removeEventListener('change', sync);
	});
</script>

<section class="legende">
	{#if mobile}
		<button class="titre" aria-expanded={ouvert} aria-controls="legende-liste" onclick={() => (ouvert = !ouvert)}>
			<span class="chevron" class:ouvert>▸</span> Les mentions
		</button>
	{:else}
		<p class="titre">Les mentions</p>
	{/if}

	{#if ouvert}
		<ul id="legende-liste">
			{#each ORDRE_FAMILLES as code (code)}
				{@const f = FAMILLE_PUBLIC[code]}
				<li>
					<span class="pastille" style="background: {f.couleur}"></span>
					<span class="texte">
						<span class="label">{f.header}</span>
						<span class="sens">{f.corps}</span>
					</span>
				</li>
			{/each}
		</ul>
	{/if}
</section>

<style>
	.legende {
		margin-top: 1.25rem;
		padding-top: 1rem;
		border-top: 1px solid var(--couleur-trait);
	}

	.titre {
		margin: 0;
		font-family: var(--police-titre);
		font-size: 0.82rem;
		letter-spacing: 0.02em;
		color: var(--couleur-encre-douce);
	}

	/* Intitulé cliquable en mobile : remis à plat, look d'un titre. */
	button.titre {
		display: flex;
		align-items: center;
		width: 100%;
		padding: 0;
		background: none;
		border: none;
		text-align: left;
		cursor: pointer;
	}

	.chevron {
		display: inline-block;
		margin-right: 0.4rem;
		transition: transform 0.15s;
	}

	.chevron.ouvert {
		transform: rotate(90deg);
	}

	ul {
		list-style: none;
		margin: 0.6rem 0 0;
		padding: 0;
		display: grid;
		gap: 0.5rem;
	}

	li {
		display: grid;
		grid-template-columns: auto 1fr;
		gap: 0.5rem;
		align-items: start;
	}

	.pastille {
		width: 0.7rem;
		height: 0.7rem;
		margin-top: 0.15rem;
		border-radius: 50%;
		flex: none;
	}

	.texte {
		display: block;
		line-height: 1.3;
	}

	.label {
		display: block;
		font-size: 0.85rem;
		font-weight: 600;
		color: var(--couleur-encre);
	}

	.sens {
		display: block;
		font-size: 0.78rem;
		color: var(--couleur-encre-douce);
	}
</style>
