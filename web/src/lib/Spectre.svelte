<script>
	// Spectre — la « ligne de proximité », signature de la Direction B (charte-
	// graphique.md). Une bande horizontale continue, de la main du maître (chaud) à
	// sa seule influence (froid) : le dégradé des huit pigments (token --spectre).
	// Réutilisable partout — fine dans la coquille, plus haute avec les libellés de
	// territoires en tête d'un dossier.
	import { TERRITOIRES } from '$lib/territoires.js';

	// hauteur — épaisseur de la bande (ex. '3px' en coquille, '6px' en tête de page)
	// zones   — afficher les trois territoires sous la bande (au plus près / autour /
	//           dans son influence), alignés sur les segments de l'axe.
	let { hauteur = '3px', zones = false } = $props();
</script>

<div class="spectre-bloc" role="presentation">
	<div class="bande" style="height: {hauteur}"></div>
	{#if zones}
		<div class="zones">
			{#each TERRITOIRES as t (t.id)}
				<span>{t.titre}</span>
			{/each}
		</div>
	{/if}
</div>

<style>
	.spectre-bloc {
		width: 100%;
	}

	.bande {
		width: 100%;
		background: var(--spectre);
	}

	/* Colonnes proportionnelles au nombre de mentions par territoire (2 · 3 · 3) :
	   chaque libellé se cale au début de son segment sur l'axe. */
	.zones {
		display: grid;
		grid-template-columns: 2fr 3fr 3fr;
		font-family: var(--police-ui);
		font-size: var(--taille-xs);
		letter-spacing: 0.12em;
		text-transform: uppercase;
		color: var(--couleur-encre-douce);
		padding-top: var(--espace-2);
	}

	.zones span {
		white-space: nowrap;
		overflow: hidden;
		text-overflow: ellipsis;
		padding-right: 0.4rem;
	}

	/* Petit écran : les trois libellés doivent tenir sans se chevaucher. */
	@media (max-width: 560px) {
		.zones {
			font-size: 0.6rem;
			letter-spacing: 0.02em;
		}
	}
</style>
