<script>
	// Infobulle PARTAGÉE (graphique + jauges de la liste) : une seule grammaire
	// de tooltip dans toute l'application (décision 2026-07-12, extraite de
	// NuageFamilles). Hiérarchie visible : header / valeur / précision courte /
	// mention type optionnelle (grammaire du 2026-07-10). `aria-hidden` : le
	// contenu accessible passe par l'aria-label de l'élément survolé/focusé
	// chez l'appelant.
	//
	// tt      : { header, valeur, corps?, mentionType? }
	// x, y    : position en px — dans le conteneur relatif de l'appelant
	//           (fixe=false), ou dans la fenêtre (fixe=true).
	// dessous : bascule le panneau sous la cible (quand elle est trop haute).
	// fixe    : position: fixed — nécessaire quand l'appelant vit dans un
	//           conteneur à overflow (la liste des maîtres défile), qui
	//           rognerait un panneau positionné en absolu.
	let { tt, x, y, dessous = false, fixe = false } = $props();
</script>

<div
	class="tooltip"
	class:dessous
	class:fixe
	role="tooltip"
	aria-hidden="true"
	style="left: {x}px; top: {y}px"
>
	<p class="tt-header">{tt.header}</p>
	<p class="tt-valeur">{tt.valeur}</p>
	{#if tt.corps}
		<p class="tt-corps">{tt.corps}</p>
	{/if}
	{#if tt.mentionType}
		<p class="tt-mention">Mention type : «&nbsp;{tt.mentionType}&nbsp;»</p>
	{/if}
</div>

<style>
	/* Panneau sobre (fond clair, pas de pavé noir), ne vit qu'au survol/focus.
	   Au-dessus de la cible par défaut (translate -100%), dessous via .dessous. */
	.tooltip {
		position: absolute;
		z-index: 5;
		transform: translate(-50%, calc(-100% - 10px));
		max-width: 15rem;
		padding: 0.5rem 0.65rem;
		background: #fff;
		border: 1px solid var(--couleur-trait);
		border-radius: 4px;
		box-shadow: 0 4px 14px rgba(43, 30, 20, 0.16);
		pointer-events: none;
		text-align: left;
	}

	.tooltip.fixe {
		position: fixed;
	}

	.tooltip.dessous {
		transform: translate(-50%, 12px);
	}

	.tt-header {
		margin: 0;
		font-family: var(--police-titre);
		font-size: 0.9rem;
		font-weight: bold;
		color: var(--couleur-encre);
	}

	.tt-corps {
		margin: 0.25rem 0 0;
		font-size: 0.82rem;
		line-height: 1.35;
		color: var(--couleur-encre);
	}

	.tt-valeur {
		margin: 0.4rem 0 0;
		font-size: 0.9rem;
		font-weight: bold;
		font-variant-numeric: tabular-nums;
		color: var(--couleur-encre);
	}

	.tt-mention {
		margin: 0.35rem 0 0;
		padding-top: 0.3rem;
		border-top: 1px solid var(--couleur-trait);
		font-size: 0.72rem;
		font-style: italic;
		color: var(--couleur-encre-douce);
	}
</style>
