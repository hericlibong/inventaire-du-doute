<script>
	import { NIVEAUX, nombre } from '$lib/joconde.js';

	// « Le combien » : une barre horizontale par famille de formule, longueur
	// proportionnelle au nombre d'œuvres. Montre d'un coup la « forme du doute »
	// propre à un maître (dominé par « école de », par « manière de »…).
	// Couleur = niveau sur l'échelle du doute. Remplace la galaxie (decisions.md,
	// 2026-07-08). Une barre = une famille (pas une œuvre) — assumé.
	let { maitre } = $props();

	// Familles triées par volume décroissant ; échelle relative au plus gros.
	const rangs = $derived(
		[...maitre.familles].sort((a, b) => b.notices - a.notices)
	);
	const maxi = $derived(Math.max(1, ...rangs.map((f) => f.notices)));
	const largeur = (n) => `${Math.max(1.5, (n / maxi) * 100)}%`;
	const libelleNiveau = (n) => NIVEAUX[n - 1].libelle;
</script>

<figure class="barres">
	<figcaption>
		La <strong>forme du doute</strong> autour de {maitre.nom} : quelles formules
		les musées emploient, et en quelles quantités.
	</figcaption>

	<ul class="lignes">
		{#each rangs as f (f.code)}
			<li>
				<span class="libelle">{f.libelle}</span>
				<span class="piste">
					<span
						class="barre"
						style="width: {largeur(f.notices)}; background: var(--niveau-{f.niveau})"
						title="{f.libelle} — {libelleNiveau(f.niveau)} : {nombre(f.notices)}"
					></span>
				</span>
				<span class="valeur">{nombre(f.notices)}</span>
			</li>
		{/each}
	</ul>

	<ul class="legende" aria-label="Les 3 niveaux de doute">
		{#each NIVEAUX as niv (niv.n)}
			<li>
				<span class="puce" style="background: var({niv.variable})"></span>
				{niv.libelle}
			</li>
		{/each}
	</ul>
</figure>

<style>
	.barres {
		margin: 0;
	}

	figcaption {
		font-size: 1rem;
		max-width: 42rem;
		margin-bottom: 1rem;
	}

	.lignes {
		list-style: none;
		margin: 0;
		padding: 0;
		display: flex;
		flex-direction: column;
		gap: 0.5rem;
	}

	.lignes li {
		display: grid;
		grid-template-columns: minmax(8rem, 14rem) 1fr auto;
		align-items: center;
		gap: 0.75rem;
	}

	.libelle {
		font-size: 0.9rem;
		text-align: right;
	}

	.piste {
		display: block;
		background: var(--couleur-trait);
		border-radius: 2px;
	}

	.barre {
		display: block;
		height: 1.1rem;
		border-radius: 2px;
		min-width: 2px;
	}

	.valeur {
		font-variant-numeric: tabular-nums;
		font-weight: 600;
		color: var(--couleur-encre-douce);
	}

	.legende {
		list-style: none;
		display: flex;
		flex-wrap: wrap;
		gap: 1rem;
		margin: 1.25rem 0 0;
		padding: 0;
		font-size: 0.85rem;
		color: var(--couleur-encre-douce);
	}

	.legende li {
		display: flex;
		align-items: center;
		gap: 0.4rem;
	}

	.puce {
		display: inline-block;
		width: 0.8rem;
		height: 0.8rem;
		border-radius: 2px;
	}

	@media (max-width: 520px) {
		.lignes li {
			grid-template-columns: 1fr auto;
		}
		.libelle {
			grid-column: 1 / -1;
			text-align: left;
		}
	}
</style>
