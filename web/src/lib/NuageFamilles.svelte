<script>
	import { nombre } from '$lib/joconde.js';
	import { FAMILLE_PUBLIC, ORDRE_FAMILLES, tooltipFamille, resumeFamille } from '$lib/familles-public.js';
	import Infobulle from '$lib/Infobulle.svelte';

	// « Le combien », comparable entre maîtres (decisions.md 2026-07-08). Scatter sur
	// grille FIXE : axe X = familles (mêmes colonnes pour tous), axe Y = volume,
	// plafond COMMUN. La hauteur porte la mesure. Le portrait du maître a été sorti
	// d'ici (il appartient au header de fiche, décision 2026-07-11) → le graphe
	// occupe désormais toute la largeur de sa zone.
	let { maitre, plafond } = $props();

	// Axe X ordonné par distance narrative au maître (docs/typologie.md), labels
	// publics et couleur stable par famille — tous deux depuis familles-public.js
	// (source unique, partagée avec la vitrine « Œuvres »). Même ordre pour tous →
	// l'axe se lit de gauche (presque lui) à droite (seulement son style).
	const FAMILLES = ORDRE_FAMILLES.map((code) => ({
		code,
		label: FAMILLE_PUBLIC[code].label,
		couleur: FAMILLE_PUBLIC[code].couleur
	}));

	// Géométrie SVG resserrée (retour 2026-07-09) : grille plus dense, points plus
	// gros, viewBox compact. `Y_HAUT` doit laisser AU MOINS le rayon max d'une bulle
	// (16, au plafond) sous le bord haut, sinon le point à 240 est rogné : on prend
	// 24 de marge en tête. `Y_BASE` reste à 236 (ligne de base et axe X inchangés).
	const X0 = 30, X_LARG = 342, Y_HAUT = 24, Y_HAUTEUR = 212;
	const Y_BASE = Y_HAUT + Y_HAUTEUR;
	const pas = X_LARG / FAMILLES.length;
	const colonneX = (i) => X0 + pas * (i + 0.5);
	const y = (v) => Y_BASE - (v / plafond) * Y_HAUTEUR;
	// Points nettement plus gros ; plancher élevé pour la présence, écart modéré.
	const rayon = (v) => 6 + (v / plafond) * 10;

	const graduations = $derived([1, 2, 3, 4].map((k) => Math.round((k * plafond) / 4)));

	const points = $derived(
		FAMILLES.map((f, i) => {
			const fam = maitre.familles.find((g) => g.code === f.code);
			if (!fam) return null;
			return {
				...f,
				x: colonneX(i),
				cy: y(fam.notices),
				r: rayon(fam.notices),
				notices: fam.notices,
				tt: tooltipFamille(f.code, maitre.nom, fam.notices),
				resume: resumeFamille(f.code, maitre.nom, fam.notices)
			};
		}).filter(Boolean)
	);

	// Tooltip HTML custom (le <title> SVG natif, non stylable, est abandonné —
	// décision 2026-07-10). `actif` porte les données à afficher + la position en
	// pixels DANS le conteneur .graphe-hote, calculée depuis la position réelle du
	// point à l'écran (le SVG a son propre repère viewBox, on ne peut pas y lire des
	// px). `dessous` bascule le panneau sous le point quand il est trop haut, pour ne
	// jamais déborder en tête de graphe. Le tooltip ne vit qu'au survol/focus : il
	// disparaît dès qu'on quitte le point, il ne masque donc pas durablement le graphe.
	let regardEl;
	let actif = $state(null);

	function montre(event, p) {
		const cible = event.currentTarget.getBoundingClientRect();
		const hote = regardEl.getBoundingClientRect();
		const y = cible.top - hote.top;
		actif = {
			tt: p.tt,
			x: cible.left + cible.width / 2 - hote.left,
			y,
			dessous: y < 90
		};
	}

	function cache() {
		actif = null;
	}
</script>

<figure class="nuage">
	<div class="graphe-hote" bind:this={regardEl}>
		<svg viewBox="0 0 380 300" class="graphe" role="img"
			aria-label="Nuage des familles de doute pour {maitre.nom}, échelle commune">
			<!-- graduations horizontales + valeurs -->
			{#each graduations as g (g)}
				<line x1={X0} x2={X0 + X_LARG} y1={y(g)} y2={y(g)} class="grille" />
				<text x={X0 - 5} y={y(g) + 3} text-anchor="end" class="axe-y">{nombre(g)}</text>
			{/each}
			<!-- ligne de base (zéro) -->
			<line x1={X0} x2={X0 + X_LARG} y1={Y_BASE} y2={Y_BASE} class="base" />
			<text x={X0 - 5} y={Y_BASE + 3} text-anchor="end" class="axe-y">0</text>

			<!-- libellés publics de familles (axe X, inclinés) -->
			{#each FAMILLES as f, i (f.code)}
				<text
					x={colonneX(i)}
					y={Y_BASE + 12}
					text-anchor="end"
					class="axe-x"
					transform="rotate(-42 {colonneX(i)} {Y_BASE + 12})">{f.label}</text
				>
			{/each}

			<!-- points : survol/focus → tooltip HTML custom ; aria-label = repli
			     textuel pour lecteur d'écran (le <title> natif a disparu). -->
			{#each points as p (p.code)}
				<circle
					cx={p.x}
					cy={p.cy}
					r={p.r}
					style="fill: {p.couleur}"
					fill-opacity="0.9"
					stroke="#fff"
					stroke-width="0.7"
					class="point"
					tabindex="0"
					role="button"
					aria-label={p.resume}
					onmouseenter={(e) => montre(e, p)}
					onmouseleave={cache}
					onfocus={(e) => montre(e, p)}
					onblur={cache}
				/>
			{/each}
		</svg>

		<!-- Infobulle partagée (Infobulle.svelte) : header / valeur / précision /
		     mention type. Le contenu accessible passe par l'aria-label du point. -->
		{#if actif}
			<Infobulle tt={actif.tt} x={actif.x} y={actif.y} dessous={actif.dessous} />
		{/if}
	</div>

	<!-- Micro-légende : la logique de distance, en une ligne. Statique (jamais de
	     bloc dépliable ni de mode d'emploi séparé — voir CLAUDE.md). -->
	<figcaption class="gradient">De gauche à droite, le lien au maître se desserre.</figcaption>
</figure>

<style>
	.nuage {
		margin: 0;
	}

	.graphe-hote {
		position: relative; /* repère du tooltip HTML positionné en absolu */
	}

	.point {
		cursor: pointer;
		transition: fill-opacity 0.12s ease;
	}

	.point:hover,
	.point:focus-visible {
		fill-opacity: 1;
	}

	.point:focus-visible {
		outline: 2px solid var(--couleur-encre);
		outline-offset: 1px;
	}

	/* Les styles du panneau d'infobulle vivent dans Infobulle.svelte (partagé). */

	.graphe {
		display: block;
		width: 100%;
		height: auto;
	}

	.grille {
		stroke: var(--couleur-trait);
		stroke-width: 1;
		stroke-dasharray: 2 4;
	}

	.base {
		stroke: var(--couleur-encre-douce);
		stroke-width: 1;
	}

	.axe-y {
		font-size: 9px;
		fill: var(--couleur-encre-douce);
		font-variant-numeric: tabular-nums;
	}

	.axe-x {
		font-size: 9px;
		fill: var(--couleur-encre);
	}

	.gradient {
		margin: 0.5rem 0 0;
		font-size: 0.8rem;
		font-style: italic;
		text-align: center;
		color: var(--couleur-encre-douce);
	}
</style>
