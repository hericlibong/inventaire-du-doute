<script>
	import { NIVEAUX, nombre } from '$lib/joconde.js';

	// « Le combien », version comparable entre maîtres (decisions.md 2026-07-08).
	// Scatter sur une grille FIXE : axe X = familles de doute, toujours les mêmes,
	// même ordre ; axe Y = volume, plafond COMMUN à tous les maîtres. La hauteur
	// porte la mesure (l'œil compare bien des hauteurs sur une échelle commune) ;
	// la taille du point ne fait que l'accentuer légèrement. Zéro = pas de point.
	let { maitre, plafond } = $props();

	// Axe X : ordre canonique du lexique (DOUTE_PAR_NIVEAU), « présumé » retiré
	// car absent des 27 maîtres (colonne toujours vide). Libellés d'axe courts ;
	// le libellé technique complet reste au survol.
	const FAMILLES = [
		{ code: 'attribue',            court: 'attribué à', niveau: 1, couleur: '#b8551f' },
		{ code: 'point_interrogation', court: '?',          niveau: 1, couleur: '#e08a5a' },
		{ code: 'ecole_de',            court: 'école de',   niveau: 2, couleur: '#c98a2e' },
		{ code: 'atelier_de',          court: 'atelier',    niveau: 2, couleur: '#e0a94f' },
		{ code: 'entourage_de',        court: 'entourage',  niveau: 2, couleur: '#b5934a' },
		{ code: 'suiveur_de',          court: 'suiveur',    niveau: 2, couleur: '#8f7b3d' },
		{ code: 'maniere_de',          court: 'manière de', niveau: 3, couleur: '#cbb06a' },
		{ code: 'genre_de',            court: 'genre de',   niveau: 3, couleur: '#9a9b6b' }
	];

	// Géométrie SVG (viewBox 0 0 560 400).
	const X0 = 44, X_LARG = 500, Y_HAUT = 34, Y_HAUTEUR = 292;
	const Y_BASE = Y_HAUT + Y_HAUTEUR;
	const pas = X_LARG / FAMILLES.length;
	const colonneX = (i) => X0 + pas * (i + 0.5);
	const y = (v) => Y_BASE - (v / plafond) * Y_HAUTEUR;
	// Taille modérée, avec plancher pour que les petits volumes restent visibles.
	const rayon = (v) => 3.5 + (v / plafond) * 5.5;

	const graduations = $derived([1, 2, 3, 4].map((k) => Math.round((k * plafond) / 4)));

	// Un point par famille présente (notices > 0) chez ce maître.
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
				libelle: fam.libelle
			};
		}).filter(Boolean)
	);

	// Bornes de colonnes par niveau, pour les libellés de groupe en haut.
	const groupes = $derived(
		NIVEAUX.map((niv) => {
			const idx = FAMILLES.map((f, i) => (f.niveau === niv.n ? i : -1)).filter((i) => i >= 0);
			return { ...niv, x: (colonneX(idx[0]) + colonneX(idx.at(-1))) / 2 };
		})
	);
</script>

<figure class="nuage">
	<figcaption>
		La <strong>forme du doute</strong> autour de {maitre.nom}, sur une échelle
		<strong>commune à tous les maîtres</strong> (plafond {nombre(plafond)} : le
		record, « école de » Le Brun). Un nuage bas = un doute modeste face au record.
	</figcaption>

	<svg viewBox="0 0 560 400" role="img"
		aria-label="Nuage des familles de doute pour {maitre.nom}, échelle commune">
		<!-- libellés de niveau (groupes de colonnes) -->
		{#each groupes as g (g.n)}
			<text x={g.x} y={Y_HAUT - 20} text-anchor="middle" class="groupe" fill="var({g.variable})">
				{g.libelle}
			</text>
		{/each}

		<!-- graduations horizontales + valeurs -->
		{#each graduations as g (g)}
			<line x1={X0} x2={X0 + X_LARG} y1={y(g)} y2={y(g)} class="grille" />
			<text x={X0 - 6} y={y(g) + 3} text-anchor="end" class="axe-y">{nombre(g)}</text>
		{/each}
		<!-- ligne de base (zéro) -->
		<line x1={X0} x2={X0 + X_LARG} y1={Y_BASE} y2={Y_BASE} class="base" />
		<text x={X0 - 6} y={Y_BASE + 3} text-anchor="end" class="axe-y">0</text>

		<!-- libellés de familles (axe X) -->
		{#each FAMILLES as f, i (f.code)}
			<text x={colonneX(i)} y={Y_BASE + 16} text-anchor="middle" class="axe-x">{f.court}</text>
		{/each}

		<!-- points -->
		{#each points as p (p.code)}
			<circle cx={p.x} cy={p.cy} r={p.r} fill={p.couleur} fill-opacity="0.9" stroke="#fff" stroke-width="0.5">
				<title>{p.libelle} — {NIVEAUX[p.niveau - 1].libelle} : {nombre(p.notices)} notices</title>
			</circle>
		{/each}
	</svg>

	<p class="lecture">
		La <strong>hauteur</strong> porte la mesure (nombre d'œuvres) ; la taille du
		point ne fait que l'accentuer. Échelle linéaire, chiffres réels. Survolez un
		point pour le compte exact.
	</p>
</figure>

<style>
	.nuage {
		margin: 0;
	}

	figcaption {
		font-size: 1rem;
		max-width: 42rem;
		margin-bottom: 0.75rem;
	}

	svg {
		width: 100%;
		height: auto;
		display: block;
	}

	.groupe {
		font-size: 10px;
		font-weight: 600;
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

	.lecture {
		font-size: 0.8rem;
		color: var(--couleur-encre-douce);
		max-width: 42rem;
		margin: 0.5rem 0 0;
	}
</style>
