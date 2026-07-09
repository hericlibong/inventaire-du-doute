<script>
	import { NIVEAUX, nombre } from '$lib/joconde.js';

	// « Le combien », comparable entre maîtres (decisions.md 2026-07-08), en regard
	// d'un portrait du maître (maquette 2026-07-09 : portrait libre de droit à venir,
	// ici un placeholder — l'idée est de donner de la présence à la visualisation).
	// Scatter sur grille FIXE : axe X = familles (mêmes colonnes pour tous), axe Y =
	// volume, plafond COMMUN. La hauteur porte la mesure, la taille l'accentue.
	let { maitre, plafond } = $props();

	// Axe X : ordre canonique du lexique, « présumé » retiré (absent des 27).
	// Libellés d'axe courts ; le libellé technique complet reste au survol.
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

	// Géométrie SVG resserrée (retour 2026-07-09) : grille plus dense, points plus
	// gros, viewBox compact pour tenir dans une colonne en regard du portrait.
	const X0 = 30, X_LARG = 342, Y_HAUT = 10, Y_HAUTEUR = 226;
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
				libelle: fam.libelle
			};
		}).filter(Boolean)
	);
</script>

<figure class="nuage">
	<figcaption>
		La <strong>forme du doute</strong> autour de {maitre.nom}, sur une échelle
		<strong>commune à tous les maîtres</strong> (plafond {nombre(plafond)} : le
		record, « école de » Le Brun). Un nuage bas = un doute modeste face au record.
	</figcaption>

	<div class="regard">
		<!-- Placeholder du portrait (image libre de droit à sourcer — maquette) -->
		<div class="portrait" aria-label="Portrait de {maitre.nom} (à venir)">
			<svg viewBox="0 0 100 130" class="silhouette" role="img" aria-hidden="true">
				<rect width="100" height="130" fill="#efe9df" />
				<circle cx="50" cy="48" r="24" fill="#cdc3b2" />
				<path d="M14 130 Q14 84 50 84 Q86 84 86 130 Z" fill="#cdc3b2" />
			</svg>
			<span class="portrait-legende">{maitre.nom}<br /><em>portrait libre de droit — à venir</em></span>
		</div>

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

			<!-- libellés de familles (axe X, inclinés) -->
			{#each FAMILLES as f, i (f.code)}
				<text
					x={colonneX(i)}
					y={Y_BASE + 12}
					text-anchor="end"
					class="axe-x"
					transform="rotate(-40 {colonneX(i)} {Y_BASE + 12})">{f.court}</text
				>
			{/each}

			<!-- points -->
			{#each points as p (p.code)}
				<circle cx={p.x} cy={p.cy} r={p.r} fill={p.couleur} fill-opacity="0.9" stroke="#fff" stroke-width="0.7">
					<title>{p.libelle} — {NIVEAUX[p.niveau - 1].libelle} : {nombre(p.notices)} notices</title>
				</circle>
			{/each}
		</svg>
	</div>

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

	.regard {
		display: flex;
		align-items: stretch;
		gap: 1rem;
	}

	.portrait {
		flex: 0 0 30%;
		max-width: 12rem;
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: 0.5rem;
		padding: 0.5rem;
		border: 1px solid var(--couleur-trait);
		border-radius: 3px;
		background: #fff;
	}

	.silhouette {
		width: 100%;
		height: auto;
		border-radius: 2px;
	}

	.portrait-legende {
		font-size: 0.8rem;
		text-align: center;
		color: var(--couleur-encre-douce);
		line-height: 1.3;
	}

	.graphe {
		flex: 1 1 auto;
		min-width: 0;
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

	.lecture {
		font-size: 0.8rem;
		color: var(--couleur-encre-douce);
		max-width: 42rem;
		margin: 0.75rem 0 0;
	}

	@media (max-width: 560px) {
		.regard {
			flex-direction: column;
		}
		.portrait {
			flex-basis: auto;
			max-width: 10rem;
			align-self: flex-start;
		}
	}
</style>
