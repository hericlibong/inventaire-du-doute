<script>
	// Un panneau de comparaison : les huit mentions en barres horizontales, groupées
	// par territoire (territoires.js), colorées par la couleur STABLE de chaque
	// mention (familles-public.js). Sert de « petit multiple » : deux panneaux à
	// échelle COMMUNE (même maxPart) rendent comparables l'ensemble de Joconde et les
	// 27 noms. Les mentions se recouvrent → ce ne sont PAS les parts exclusives d'un
	// total (aucun empilement, aucun anneau) : chaque barre est une part indépendante
	// des notices concernées, et les parts ne s'additionnent pas à 100 %.
	import { nombre } from '$lib/joconde.js';
	import { FAMILLE_PUBLIC } from '$lib/familles-public.js';
	import { TERRITOIRES } from '$lib/territoires.js';

	// titre     — nom de la série (« Ensemble de Joconde »)
	// total     — base de la série (pour les %), affichée en sous-titre
	// valeurs   — objet code → nombre de notices pour cette série
	// maxPart   — part maximale sur LES DEUX séries (échelle commune, 0–1)
	let { titre, total, valeurs, maxPart } = $props();

	// « <1 » plutôt que « 0 » quand la part est non nulle mais arrondirait à zéro :
	// une barre visible ne doit pas afficher « 0 % ».
	const pct = (v) => {
		const p = (v / total) * 100;
		return v > 0 && p < 0.5 ? '<1' : Math.round(p);
	};
	const largeur = (v) => `${(v / total / maxPart) * 100}%`;
</script>

<figure class="panneau">
	<figcaption class="tete">
		<span class="serie">{titre}</span>
		<span class="base">{nombre(total)} notices concernées</span>
	</figcaption>

	{#each TERRITOIRES as t (t.id)}
		<div class="groupe" data-zone={t.id}>
			<span class="zone-titre">{t.titre}</span>
			{#each t.codes as code (code)}
				{@const v = valeurs[code] ?? 0}
				<div class="ligne">
					<span class="lib">{FAMILLE_PUBLIC[code].label}</span>
					<span class="piste">
						<span class="barre" style="width: {largeur(v)}; background: {FAMILLE_PUBLIC[code].couleur}"></span>
					</span>
					<span class="val"><b>{pct(v)}&nbsp;%</b><span class="brut">{nombre(v)}</span></span>
				</div>
			{/each}
		</div>
	{/each}
</figure>

<style>
	.panneau {
		margin: 0;
	}

	.tete {
		display: flex;
		flex-wrap: wrap;
		align-items: baseline;
		gap: 0.15rem 0.6rem;
		padding-bottom: var(--espace-2);
		border-bottom: var(--filet);
		margin-bottom: var(--espace-3);
	}

	.serie {
		font-family: var(--police-ui);
		font-weight: 700;
		font-size: var(--taille-m);
		color: var(--couleur-encre);
	}

	.base {
		font-family: var(--police-ui);
		font-size: var(--taille-s);
		color: var(--couleur-encre-douce);
		font-variant-numeric: tabular-nums;
	}

	.groupe {
		margin-bottom: var(--espace-3);
	}

	.zone-titre {
		display: block;
		font-family: var(--police-ui);
		font-size: var(--taille-xs);
		font-weight: 600;
		letter-spacing: 0.04em;
		text-transform: uppercase;
		color: var(--couleur-encre-douce);
		margin-bottom: 0.35rem;
	}

	/* label | piste | valeur — grille alignée, colonnes fixes pour label et valeur. */
	.ligne {
		display: grid;
		grid-template-columns: 6.5rem 1fr auto;
		align-items: center;
		gap: 0.5rem;
		padding: 0.15rem 0;
	}

	.lib {
		font-family: var(--police-texte);
		font-size: var(--taille-s);
		color: var(--couleur-encre);
		text-align: right;
	}

	.piste {
		display: block;
		height: 0.7rem;
		background: var(--couleur-trait-clair);
		border-radius: 2px;
		overflow: hidden;
	}

	.barre {
		display: block;
		height: 100%;
		min-width: 1px; /* une valeur non nulle reste visible ; zéro reste vide */
		border-radius: 2px;
	}

	.val {
		font-family: var(--police-ui);
		font-variant-numeric: tabular-nums;
		font-size: var(--taille-s);
		display: flex;
		align-items: baseline;
		gap: 0.4rem;
		white-space: nowrap;
	}

	.val b {
		color: var(--couleur-encre);
		font-weight: 700;
	}

	.brut {
		color: var(--couleur-encre-douce);
		font-size: var(--taille-xs);
	}
</style>
