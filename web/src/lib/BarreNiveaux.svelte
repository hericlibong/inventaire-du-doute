<script>
	import { NIVEAUX } from '$lib/joconde.js';

	// ARCHIVE — plus utilisé depuis le 2026-07-11 : la jauge de la liste des
	// maîtres est passée aux familles (BarreFamilles.svelte), car l'agrégation
	// par niveau contredisait le graphique (decisions.md). Conservé pour les
	// futures vues sur l'échelle du doute à 3 niveaux (tokens --niveau-* gardés).
	// niveaux : [n1, n2, n3] (nombre de notices par niveau du doute).
	// hauteur : épaisseur de la barre. etiquettes : afficher les nombres/légende.
	let { niveaux, hauteur = '0.7rem', etiquettes = false } = $props();

	const total = $derived(niveaux.reduce((s, v) => s + v, 0));
	const parts = $derived(
		NIVEAUX.map((meta, i) => ({
			...meta,
			notices: niveaux[i],
			pourcent: total ? (niveaux[i] / total) * 100 : 0
		}))
	);
</script>

<div class="barre" style="height: {hauteur}" role="img" aria-label="Répartition du doute par niveau">
	{#each parts as part (part.n)}
		{#if part.notices > 0}
			<span
				class="segment"
				style="width: {part.pourcent}%; background: var({part.variable})"
				title="{part.libelle} : {part.notices}"
			></span>
		{/if}
	{/each}
</div>

{#if etiquettes}
	<ul class="legende">
		{#each parts as part (part.n)}
			<li>
				<span class="puce" style="background: var({part.variable})"></span>
				<strong>{part.libelle}</strong>
				<span class="detail">{part.notices} · {part.sens}</span>
			</li>
		{/each}
	</ul>
{/if}

<style>
	.barre {
		display: flex;
		width: 100%;
		border-radius: 2px;
		overflow: hidden;
		background: var(--couleur-trait);
	}

	.segment {
		display: block;
		height: 100%;
	}

	.legende {
		list-style: none;
		margin: 0.75rem 0 0;
		padding: 0;
		display: flex;
		flex-direction: column;
		gap: 0.35rem;
		font-size: 0.9rem;
	}

	.puce {
		display: inline-block;
		width: 0.8rem;
		height: 0.8rem;
		border-radius: 2px;
		vertical-align: middle;
		margin-right: 0.4rem;
	}

	.detail {
		color: var(--couleur-encre-douce);
	}
</style>
