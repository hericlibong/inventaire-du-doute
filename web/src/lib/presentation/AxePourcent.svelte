<script>
	// Graduations horizontales d'une vue en colonnes : un repère chiffré tous les
	// `pas`, dans la gouttière de gauche, et un filet qui traverse les huit
	// colonnes. Règle du projet : toute quantité affichée doit être lisible — pas
	// de barres sans échelle.
	//
	// Se place en fond d'un conteneur `position: relative` dont la hauteur porte
	// l'échelle, et qui déclare la grille `--colonnes-mentions`. Sous 760 px, la
	// vue passe en lignes horizontales : l'axe disparaît et chaque barre porte
	// alors sa valeur écrite.
	let { max, pas } = $props();

	// Repères de 0 au maximum de l'échelle (inclus quand il tombe juste).
	const reperes = Array.from({ length: Math.floor(max / pas) + 1 }, (_, i) => i * pas);
</script>

<div class="axe" aria-hidden="true">
	{#each reperes as v (v)}
		<div class="grad" style="bottom: {(v / max) * 100}%">
			<span class="val">{Math.round(v * 100)}&nbsp;%</span>
			<span class="trait" class:zero={v === 0}></span>
		</div>
	{/each}
</div>

<style>
	/* L'axe couvre la ZONE DES BARRES, pas le cadre entier : la vue réserve en haut
	   une marge (--marge-haute) où les chiffres des plus grandes barres respirent. */
	.axe {
		position: absolute;
		inset: var(--marge-haute, 0) 0 0 0;
		pointer-events: none;
	}

	/* `bottom` place le BAS du bloc sur la valeur : on le redescend d'une
	   demi-hauteur pour que le filet, et non le bas du texte, tombe sur la
	   graduation. Sans quoi toutes les barres paraissent déborder sous le zéro. */
	.grad {
		position: absolute;
		left: 0;
		right: 0;
		display: grid;
		grid-template-columns: var(--colonnes-mentions);
		align-items: center;
		transform: translateY(50%);
	}

	.val {
		grid-column: 1;
		justify-self: end;
		padding-right: 0.5rem;
		transform: translateY(-0.05rem);
		font-family: var(--police-ui);
		font-size: var(--taille-xs);
		font-variant-numeric: tabular-nums;
		color: var(--couleur-encre-douce);
	}

	/* Le filet traverse les huit colonnes de mentions ; la gouttière de gauche
	   porte la valeur, et il n'y a plus de colonne de queue depuis que la vue est
	   seule (le prototype en réservait une pour les effectifs de la matrice). */
	.trait {
		grid-column: 2 / -1;
		height: 1px;
		background: var(--couleur-trait-clair);
	}

	/* La ligne de base se distingue : c'est le zéro, pas une graduation comme une autre. */
	.zero {
		background: var(--couleur-trait);
	}

	@media (max-width: 760px) {
		.axe {
			display: none;
		}
	}
</style>
