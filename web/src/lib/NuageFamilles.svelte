<script>
	import { nombre } from '$lib/joconde.js';
	import { FAMILLE_PUBLIC, ORDRE_FAMILLES, tooltipFamille, resumeFamille } from '$lib/familles-public.js';
	import { TERRITOIRES, indicesTerritoire } from '$lib/territoires.js';
	import Infobulle from '$lib/Infobulle.svelte';

	// « Le combien », comparable entre maîtres (decisions.md 2026-07-08). Scatter sur
	// grille FIXE : axe X = familles (mêmes colonnes pour tous), axe Y = volume,
	// plafond COMMUN. La hauteur porte la mesure. Depuis 2026-07-17, l'axe est
	// recadré en TROIS TERRITOIRES de proximité (territoires.js) : le graphe donne à
	// voir le principe éditorial central — la distance à la main du maître — sans
	// changer ni les données, ni les points, ni les couleurs, ni les infobulles.
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

	// Géométrie SVG. Un bandeau de tête (0 → Y_BANDE_HAUT) accueille les titres de
	// territoire ; les bandes de fond descendent de là jusqu'à la ligne de base. Le
	// plot commence assez bas (Y_HAUT) pour que la plus grosse bulle (rayon 16 au
	// plafond) ne morde pas sur les titres.
	const X0 = 30, X_LARG = 342, Y_HAUT = 40, Y_HAUTEUR = 196;
	const Y_BASE = Y_HAUT + Y_HAUTEUR;
	const Y_BANDE_HAUT = 18; // haut des bandes de territoire (sous les titres)
	const pas = X_LARG / FAMILLES.length;
	const bordG = (i) => X0 + pas * i; // bord gauche de la colonne i
	const colonneX = (i) => X0 + pas * (i + 0.5);
	const y = (v) => Y_BASE - (v / plafond) * Y_HAUTEUR;
	// Points nettement plus gros ; plancher élevé pour la présence, écart modéré.
	const rayon = (v) => 6 + (v / plafond) * 10;

	// Bandes de territoire : plages de colonnes contiguës, calculées depuis la
	// primitive (territoires.js) et l'ordre de l'axe. x1/x2 = bords des colonnes.
	const bandes = TERRITOIRES.map((t, i) => {
		const { debut, fin } = indicesTerritoire(t, ORDRE_FAMILLES);
		const x1 = bordG(debut);
		const x2 = bordG(fin + 1);
		return { id: t.id, titre: t.titre, x1, x2, cx: (x1 + x2) / 2, premier: i === 0 };
	});

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
	// décision 2026-07-10). Position calculée depuis la position réelle du point à
	// l'écran (le SVG a son propre repère viewBox). `dessous` bascule le panneau sous
	// le point quand il est trop haut, pour ne jamais déborder en tête de graphe.
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
			aria-label="Graphique des mentions de doute pour {maitre.nom}, en trois territoires de proximité (au plus près, autour du maître, dans son influence), échelle commune à tous les maîtres">
			<!-- Bandes de territoire (fond très léger) : posées EN PREMIER, sous tout le
			     reste. Contiguës, sans marge ni cadre → une seule ligne de proximité,
			     pas trois blocs séparés. -->
			{#each bandes as b (b.id)}
				<rect
					x={b.x1}
					y={Y_BANDE_HAUT}
					width={b.x2 - b.x1}
					height={Y_BASE - Y_BANDE_HAUT}
					class="bande"
					data-zone={b.id}
				/>
			{/each}

			<!-- graduations horizontales + valeurs -->
			{#each graduations as g (g)}
				<line x1={X0} x2={X0 + X_LARG} y1={y(g)} y2={y(g)} class="grille" />
				<text x={X0 - 5} y={y(g) + 3} text-anchor="end" class="axe-y">{nombre(g)}</text>
			{/each}

			<!-- Séparateurs entre territoires : hairline discrète aux frontières
			     internes (pas de bord au début du premier). -->
			{#each bandes as b (b.id)}
				{#if !b.premier}
					<line x1={b.x1} x2={b.x1} y1={Y_BANDE_HAUT} y2={Y_BASE} class="separateur" />
				{/if}
			{/each}

			<!-- ligne de base (zéro) -->
			<line x1={X0} x2={X0 + X_LARG} y1={Y_BASE} y2={Y_BASE} class="base" />
			<text x={X0 - 5} y={Y_BASE + 3} text-anchor="end" class="axe-y">0</text>

			<!-- Titres de territoire, centrés sur leur bande, en tête du graphe. -->
			{#each bandes as b (b.id)}
				<text x={b.cx} y={12} text-anchor="middle" class="titre-zone">{b.titre}</text>
			{/each}

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

	<!-- Clé de lecture minimale, rétablie dans l'onglet Profil (la légende détaillée
	     a quitté le répertoire). Elle reprend les trois territoires : progression
	     gauche → droite, titre + annotation courte, et les mentions de chaque zone
	     avec leur pastille de couleur (labels depuis la source unique). Trois cellules
	     contiguës, pas trois cartes : le même dégradé de proximité que le graphe. -->
	<figcaption class="cle">
		<p class="cle-intro">De gauche à droite, le lien à la main du maître se desserre.</p>
		<ol class="territoires">
			{#each TERRITOIRES as t (t.id)}
				<li class="zone" data-zone={t.id}>
					<span class="zone-titre">{t.titre}</span>
					<span class="zone-note">{t.annotation}</span>
					<span class="zone-mentions">
						{#each t.codes as code (code)}
							<span class="mention">
								<span class="pastille" style="background: {FAMILLE_PUBLIC[code].couleur}"></span>
								{FAMILLE_PUBLIC[code].label}
							</span>
						{/each}
					</span>
				</li>
			{/each}
		</ol>
	</figcaption>
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

	/* Bandes de territoire : lavis très légers, une température par zone. */
	.bande[data-zone='plus-pres'] {
		fill: var(--territoire-pres);
	}
	.bande[data-zone='autour'] {
		fill: var(--territoire-autour);
	}
	.bande[data-zone='influence'] {
		fill: var(--territoire-influence);
	}

	.separateur {
		stroke: var(--couleur-trait);
		stroke-width: 1;
	}

	.titre-zone {
		font-family: var(--police-ui);
		font-size: 8.5px;
		font-weight: 600;
		letter-spacing: 0.04em;
		fill: var(--couleur-encre-douce);
		text-transform: uppercase;
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

	/* Clé de lecture : intro + trois cellules contiguës qui reprennent les bandes. */
	.cle {
		margin: 0.75rem 0 0;
	}

	.cle-intro {
		margin: 0 0 0.5rem;
		font-size: 0.8rem;
		font-style: italic;
		text-align: center;
		color: var(--couleur-encre-douce);
	}

	.territoires {
		list-style: none;
		margin: 0;
		padding: 0;
		display: grid;
		grid-template-columns: repeat(3, 1fr);
		/* filets internes seulement : les cellules se touchent (une seule bande),
		   pas trois cartes détachées. */
		gap: 0;
		border: var(--filet);
		border-radius: var(--rayon-s);
		overflow: hidden;
	}

	.zone {
		padding: 0.5rem 0.6rem 0.6rem;
		display: flex;
		flex-direction: column;
		gap: 0.3rem;
		border-left: var(--filet);
	}

	.zone:first-child {
		border-left: none;
	}

	.zone[data-zone='plus-pres'] {
		background: var(--territoire-pres);
	}
	.zone[data-zone='autour'] {
		background: var(--territoire-autour);
	}
	.zone[data-zone='influence'] {
		background: var(--territoire-influence);
	}

	.zone-titre {
		font-family: var(--police-ui);
		font-size: 0.72rem;
		font-weight: 700;
		letter-spacing: 0.04em;
		text-transform: uppercase;
		color: var(--couleur-encre);
	}

	.zone-note {
		font-family: var(--police-texte);
		font-style: italic;
		font-size: 0.82rem;
		line-height: 1.35;
		color: var(--couleur-encre-douce);
	}

	.zone-mentions {
		display: flex;
		flex-direction: column;
		gap: 0.2rem;
		margin-top: 0.15rem;
	}

	.mention {
		display: flex;
		align-items: center;
		gap: 0.4rem;
		font-size: 0.8rem;
		color: var(--couleur-encre);
	}

	.pastille {
		width: 0.6rem;
		height: 0.6rem;
		border-radius: 50%;
		flex: none;
	}

	/* Mobile : les trois territoires s'empilent, mais restent une bande continue
	   (filets horizontaux entre eux, la progression se lit de haut en bas). */
	@media (max-width: 560px) {
		.territoires {
			grid-template-columns: 1fr;
		}
		.zone {
			border-left: none;
			border-top: var(--filet);
		}
		.zone:first-child {
			border-top: none;
		}
	}
</style>
