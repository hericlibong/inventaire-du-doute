<script>
	// Accueil = affiche interactive (nouvelle direction, 2026-07-17). Le premier
	// viewport est EXCLUSIVEMENT la couverture (LandingCover, 100svh, pleine largeur,
	// sans header ni spectre — masqués par la coquille sur cette route). Le chiffre
	// vedette et le contenu secondaire vivent SOUS la ligne de flottaison.
	import LandingCover from '$lib/LandingCover.svelte';
	import { nombre } from '$lib/joconde.js';

	let { data } = $props();
	const n = data.niveaux;
	const prov = data.provenance;
	const pct = (v) => (v * 100).toLocaleString('fr-FR', { maximumFractionDigits: 1 });
</script>

<LandingCover />

<!-- Sous la couverture : preuve chiffrée secondaire, jamais visible au chargement. -->
<section class="apres">
	<div class="dedans">
		<p class="chiffre">{nombre(n.doute_total)}</p>
		<p class="note">
			formulations prudentes repérées dans la base — soit {pct(n.taux_doute_avec_auteur)}&nbsp;%
			des notices où un auteur est renseigné.
			<a href="/methode">Comment ces chiffres sont établis&nbsp;→</a>
		</p>
		<p class="source">
			Source&nbsp;: {prov.source}, version du {prov.version_donnee}, {prov.licence}.
		</p>
	</div>
</section>

<style>
	.apres {
		padding: var(--espace-6) var(--espace-5);
	}

	.dedans {
		max-width: var(--largeur-max);
		margin: 0 auto;
	}

	.chiffre {
		font-family: var(--police-titre);
		font-size: var(--taille-xl);
		font-weight: 700;
		color: var(--forme-attribue);
		font-variant-numeric: tabular-nums;
		margin: 0;
		line-height: 1;
	}

	.note {
		font-size: var(--taille-base);
		margin: var(--espace-2) 0 0;
		line-height: 1.55;
		max-width: 46rem;
	}

	.note a {
		color: var(--forme-attribue);
		white-space: nowrap;
	}

	.source {
		font-family: var(--police-ui);
		font-size: var(--taille-xs);
		color: var(--couleur-encre-douce);
		margin: var(--espace-3) 0 0;
	}
</style>
