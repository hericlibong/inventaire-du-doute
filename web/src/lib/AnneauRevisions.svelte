<script>
	// Anneau de composition des 26 667 notices avec ancienne attribution.
	// Répond à : « comment se répartissent ces notices ? » — une part-d'un-tout,
	// pas un classement. Les 7 catégories forment la partition exacte du total.
	// La légende chiffrée (à droite / dessous) est la couche accessible et
	// suffit à comprendre sans interaction ; les segments sont un renfort.
	import { nombre } from '$lib/joconde.js';
	import { ORDRE, CATEGORIES, GROUPES } from '$lib/revisions-labels.js';

	// `passages` : [{ categorie, libelle, notices }] ; `total` : 26 667.
	let { passages, total } = $props();

	const parCode = Object.fromEntries(passages.map((p) => [p.categorie, p]));
	// Segments dans l'ordre éditorial (groupe 1 puis groupe 2), avec angles.
	const segments = (() => {
		let acc = 0;
		return ORDRE.map((code) => {
			const p = parCode[code];
			const frac = p.notices / total;
			const seg = {
				code,
				libelle: p.libelle,
				notices: p.notices,
				pct: (frac * 100).toLocaleString('fr-FR', {
					minimumFractionDigits: 1,
					maximumFractionDigits: 1
				}),
				couleur: CATEGORIES[code].couleur,
				debut: acc * 360,
				fin: (acc + frac) * 360
			};
			acc += frac;
			return seg;
		});
	})();
	const indexParCode = Object.fromEntries(segments.map((s, i) => [s.code, i]));

	// Géométrie de la couronne.
	const CX = 110;
	const CY = 110;
	const R_EXT = 100;
	const R_INT = 62;

	const point = (r, angle) => {
		const a = ((angle - 90) * Math.PI) / 180;
		return [CX + r * Math.cos(a), CY + r * Math.sin(a)];
	};
	const secteur = (debut, fin) => {
		const large = fin - debut > 180 ? 1 : 0;
		const [x1, y1] = point(R_EXT, debut);
		const [x2, y2] = point(R_EXT, fin);
		const [x3, y3] = point(R_INT, fin);
		const [x4, y4] = point(R_INT, debut);
		return `M${x1} ${y1} A${R_EXT} ${R_EXT} 0 ${large} 1 ${x2} ${y2} L${x3} ${y3} A${R_INT} ${R_INT} 0 ${large} 0 ${x4} ${y4} Z`;
	};
	// Léger décalage vers l'extérieur du segment actif (mise en avant discrète).
	const decalage = (debut, fin) => {
		const [dx, dy] = point(1, (debut + fin) / 2);
		return [(dx - CX) * 5, (dy - CY) * 5];
	};

	let actif = $state(null); // index du segment mis en avant, ou null
</script>

<div class="anneau-bloc">
	<div class="anneau-wrap">
		<svg viewBox="0 0 220 220" role="img" aria-label={`Répartition des ${nombre(total)} notices avec une ancienne attribution, en sept catégories.`}>
			{#each segments as s, i (s.code)}
				{@const [dx, dy] = actif === i ? decalage(s.debut, s.fin) : [0, 0]}
				<path
					d={secteur(s.debut, s.fin)}
					fill={s.couleur}
					class="secteur"
					class:estompe={actif !== null && actif !== i}
					style={`transform: translate(${dx}px, ${dy}px)`}
					onmouseenter={() => (actif = i)}
					onmouseleave={() => (actif = null)}
					aria-hidden="true"
				/>
			{/each}
		</svg>
		<div class="centre" aria-hidden="true">
			{#if actif === null}
				<span class="c-total">{nombre(total)}</span>
				<span class="c-sous">notices avec<br />une ancienne attribution</span>
			{:else}
				<span class="c-pct">{segments[actif].pct}&nbsp;%</span>
				<span class="c-lib">{segments[actif].libelle}</span>
				<span class="c-nb">{nombre(segments[actif].notices)} notices</span>
			{/if}
		</div>
	</div>

	<!-- Légende = couche accessible (clavier + texte). Chaque bouton met le
	     segment correspondant en avant au survol comme au focus. -->
	<div class="legende">
		{#each GROUPES as g (g.id)}
			<div class="legende-groupe">
				<p class="legende-titre">{g.titre}</p>
				<ul>
					{#each g.codes as code (code)}
						{@const s = segments[indexParCode[code]]}
						<li>
							<button
								type="button"
								class:actif={actif === indexParCode[code]}
								onmouseenter={() => (actif = indexParCode[code])}
								onmouseleave={() => (actif = null)}
								onfocus={() => (actif = indexParCode[code])}
								onblur={() => (actif = null)}
							>
								<span class="puce" style={`background:${s.couleur}`}></span>
								<span class="l-nom">{s.libelle}</span>
								<span class="l-chiffres">{nombre(s.notices)} · {s.pct}&nbsp;%</span>
							</button>
						</li>
					{/each}
				</ul>
			</div>
		{/each}
	</div>
</div>

<style>
	.anneau-bloc {
		display: grid;
		grid-template-columns: minmax(15rem, 22rem) 1fr;
		gap: 2rem;
		align-items: center;
		margin-top: 1rem;
	}

	.anneau-wrap {
		position: relative;
	}

	svg {
		display: block;
		width: 100%;
		height: auto;
		overflow: visible;
	}

	.secteur {
		stroke: var(--couleur-fond);
		stroke-width: 1.5;
		transition: opacity 0.15s ease, transform 0.15s ease;
		cursor: pointer;
	}

	.secteur.estompe {
		opacity: 0.45;
	}

	.centre {
		position: absolute;
		inset: 0;
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		text-align: center;
		padding: 0 22%;
		pointer-events: none;
	}

	.c-total {
		font-family: var(--police-titre);
		font-size: 1.9rem;
		font-weight: 600;
		line-height: 1;
	}

	.c-sous {
		font-size: 0.72rem;
		color: var(--couleur-encre-douce);
		margin-top: 0.35rem;
		line-height: 1.25;
	}

	.c-pct {
		font-family: var(--police-titre);
		font-size: 1.7rem;
		font-weight: 600;
		line-height: 1;
	}

	.c-lib {
		font-size: 0.72rem;
		margin-top: 0.3rem;
		line-height: 1.2;
	}

	.c-nb {
		font-size: 0.72rem;
		color: var(--couleur-encre-douce);
		margin-top: 0.15rem;
	}

	/* --- Légende --- */
	.legende-groupe + .legende-groupe {
		margin-top: 1.1rem;
	}

	.legende-titre {
		margin: 0 0 0.35rem;
		font-size: 0.82rem;
		text-transform: uppercase;
		letter-spacing: 0.04em;
		color: var(--couleur-encre-douce);
	}

	.legende ul {
		list-style: none;
		margin: 0;
		padding: 0;
	}

	.legende button {
		display: grid;
		grid-template-columns: auto 1fr auto;
		align-items: center;
		gap: 0.6rem;
		width: 100%;
		font: inherit;
		text-align: left;
		background: none;
		border: none;
		border-radius: 4px;
		padding: 0.25rem 0.4rem;
		cursor: pointer;
		color: inherit;
	}

	.legende button.actif {
		background: rgba(28, 26, 23, 0.05);
	}

	.legende button:focus-visible {
		outline: 2px solid var(--couleur-accent);
		outline-offset: 1px;
	}

	.puce {
		width: 0.8rem;
		height: 0.8rem;
		border-radius: 2px;
	}

	.l-nom {
		font-size: 0.92rem;
	}

	.l-chiffres {
		font-size: 0.85rem;
		font-variant-numeric: tabular-nums;
		color: var(--couleur-encre-douce);
		white-space: nowrap;
	}

	@media (max-width: 720px) {
		.anneau-bloc {
			grid-template-columns: 1fr;
		}

		.anneau-wrap {
			max-width: 20rem;
			margin: 0 auto;
		}
	}
</style>
