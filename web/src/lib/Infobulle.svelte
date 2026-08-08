<script>
	// Infobulle PARTAGÉE — une seule grammaire de tooltip dans toute l'application
	// (graphique, carte, jauges de la liste). La LÉGENDE fixe porte désormais la
	// grammaire des couleurs ; le tooltip ne donne que l'information LOCALE au point
	// survolé. Vocabulaire public partout (mots de familles-public.js), jamais
	// « famille / niveau / au doute / presque lui / autour de lui ».
	//
	// Hiérarchie visible, chaque vue ne remplit que ce qui la concerne :
	//   header          — bande grisée en tête (toujours).
	//   headerPastille? — couleur → pastille dans le header (graphique : la mention).
	//   valeur?         — corps principal : le nombre local, accordé.
	//   corps?          — phrase de sens courte (graphique).
	//   lignes?         — ventilation : [{ label, couleur, valeur, appoint? }]
	//                     (carte, jauge). `appoint` = complément gris, p. ex. « 73 % ».
	//   mentionType?    — footer discret « Mention type : … » (graphique, si utile).
	//
	// `aria-hidden` : le contenu accessible passe par l'aria-label de l'élément
	// survolé/focusé chez l'appelant.
	//
	// x, y    : position en px — dans le conteneur relatif de l'appelant
	//           (fixe=false), ou dans la fenêtre (fixe=true).
	// dessous : bascule le panneau sous la cible (quand elle est trop haute).
	// fixe    : position: fixed — nécessaire quand l'appelant vit dans un
	//           conteneur à overflow (la liste des maîtres défile), qui
	//           rognerait un panneau positionné en absolu.
	// enFlux  : rendu EN FLUX (position statique, pleine largeur) — additif et
	//           rétrocompatible (défaut false). Sert le repli mobile du graphe :
	//           quand le point est hors de la fenêtre, le même contenu s'affiche
	//           sous la mention active de la légende. x/y sont alors ignorés.
	let { tt, x, y, dessous = false, fixe = false, enFlux = false } = $props();
</script>

<div
	class="tooltip"
	class:dessous
	class:fixe
	class:en-flux={enFlux}
	role="tooltip"
	aria-hidden="true"
	style={enFlux ? undefined : `left: ${x}px; top: ${y}px`}
>
	<p class="tt-header">
		{#if tt.headerPastille}
			<span class="tt-header-pastille" style="background: {tt.headerPastille}"></span>
		{/if}
		<span>{tt.header}</span>
	</p>
	{#if tt.valeur}
		<p class="tt-valeur">{tt.valeur}</p>
	{/if}
	{#if tt.titre}
		<p class="tt-titre">«&nbsp;{tt.titre}&nbsp;»</p>
	{/if}
	{#if tt.corps}
		<p class="tt-corps">{tt.corps}</p>
	{/if}
	{#if tt.lignes}
		<ul class="tt-lignes">
			{#each tt.lignes as l (l.label)}
				<li>
					<span class="tt-pastille" style="background: {l.couleur}"></span>
					<span class="tt-label">{l.label}</span>
					<span class="tt-compte">
						{l.valeur}{#if l.appoint}<span class="tt-appoint"> · {l.appoint}</span>{/if}
					</span>
				</li>
			{/each}
		</ul>
	{/if}
	{#if tt.mentionType}
		<p class="tt-mention">Mention type : «&nbsp;{tt.mentionType}&nbsp;»</p>
	{/if}
</div>

<style>
	/* Panneau sobre (fond clair, pas de pavé noir), ne vit qu'au survol/focus.
	   Au-dessus de la cible par défaut (translate -100%), dessous via .dessous.
	   Largeur STABLE : contenu ajusté mais borné (min/max), le texte passe à la
	   ligne plutôt que d'élargir → pas de saut de largeur d'une ligne à l'autre. */
	.tooltip {
		position: absolute;
		z-index: 5;
		transform: translate(-50%, calc(-100% - 10px));
		width: max-content;
		min-width: 13rem;
		max-width: 17rem;
		padding: 0;
		overflow: hidden;
		/* Finition du 2026-08-08 : fond très légèrement translucide (96 %), bordure
		   plus fine et plus chaude, ombre adoucie. Le TEXTE reste à pleine opacité —
		   c'est le panneau qui s'allège, jamais sa lisibilité. */
		background: rgba(255, 253, 249, 0.96);
		border: 1px solid rgba(198, 186, 168, 0.75);
		border-radius: 5px;
		box-shadow: 0 3px 10px rgba(43, 30, 20, 0.1);
		pointer-events: none;
		text-align: left;
	}

	.tooltip.fixe {
		position: fixed;
	}

	/* Rendu en flux (repli mobile) : le panneau s'insère sous la mention active de
	   la légende, en pleine largeur, sans positionnement absolu ni translation. */
	.tooltip.en-flux {
		position: static;
		transform: none;
		width: auto;
		min-width: 0;
		max-width: 100%;
		margin: 0.4rem 0 0.2rem;
		box-shadow: 0 2px 6px rgba(43, 30, 20, 0.08);
	}

	.tooltip.dessous {
		transform: translate(-50%, 12px);
	}

	/* Dernier bloc : marge basse, puisque le panneau n'a plus de padding vertical. */
	.tooltip > :last-child {
		margin-bottom: 0.5rem;
	}

	/* Header : bande légèrement grisée, séparée du corps par un filet. Texte grisé,
	   pastille optionnelle (la couleur de la mention, côté graphique). */
	.tt-header {
		display: flex;
		align-items: center;
		gap: 0.4rem;
		margin: 0 0 0.5rem;
		padding: 0.4rem 0.65rem;
		background: rgba(43, 30, 20, 0.05);
		border-bottom: 1px solid var(--couleur-trait);
		font-family: var(--police-titre);
		font-size: 0.82rem;
		font-weight: bold;
		line-height: 1.25;
		color: var(--couleur-encre-douce);
	}

	.tt-header-pastille {
		flex: none;
		width: 0.62rem;
		height: 0.62rem;
		border-radius: 50%;
	}

	.tt-valeur {
		margin: 0;
		padding: 0 0.65rem;
		font-size: 0.95rem;
		font-weight: bold;
		font-variant-numeric: tabular-nums;
		color: var(--couleur-encre);
	}

	/* Un peu plus d'air entre la mesure et l'explication : deux registres
	   différents, ils ne doivent pas se lire comme un paragraphe (2026-08-08). */
	.tt-corps {
		margin: 0.45rem 0 0;
		padding: 0 0.65rem;
		font-size: 0.82rem;
		line-height: 1.35;
		color: var(--couleur-encre);
	}

	/* Titre de l'œuvre unique (aperçu carte) : les mots du musée, entre guillemets. */
	.tt-titre {
		margin: 0.25rem 0 0;
		padding: 0 0.65rem;
		font-size: 0.82rem;
		font-style: italic;
		line-height: 1.35;
		color: var(--couleur-encre);
	}

	/* Ventilation : une ligne par mention, pastille + libellé + nombre aligné à
	   droite (tabulaire, comparable), % éventuel en gris. */
	.tt-lignes {
		list-style: none;
		margin: 0.4rem 0 0;
		padding: 0 0.65rem;
	}

	.tt-lignes li {
		display: flex;
		align-items: center;
		gap: 0.45rem;
		font-size: 0.82rem;
		line-height: 1.6;
		color: var(--couleur-encre);
	}

	.tt-pastille {
		flex: none;
		width: 0.6rem;
		height: 0.6rem;
		border-radius: 50%;
	}

	.tt-label {
		flex: 1;
	}

	.tt-compte {
		flex: none;
		font-variant-numeric: tabular-nums;
		font-weight: bold;
		white-space: nowrap;
	}

	.tt-appoint {
		font-weight: normal;
		color: var(--couleur-encre-douce);
	}

	.tt-mention {
		margin: 0.4rem 0 0;
		padding: 0.35rem 0.65rem 0;
		border-top: 1px solid var(--couleur-trait);
		font-size: 0.72rem;
		font-style: italic;
		color: var(--couleur-encre-douce);
	}
</style>
