<script>
	// « La scène du maître » (docs/charte-graphique.md §5) : portrait + nom + hiérarchie
	// d'informations CALCULÉE. Refonte de la hiérarchie le 2026-07-19 (decisions.md) :
	// le SUJET de la rubrique est le doute (les notices à formulation prudente), pas le
	// volume total sous le nom. On met donc `doute` en valeur principale, puis sa part
	// (dénominateur = propre + doute, « périmètre étudié »), puis la répartition entre
	// musées (même corpus que la vue Musées), puis la formulation dominante.
	//
	// Toutes les phrases sont FACTUELLES et générées depuis artistes.json (aucun texte
	// écrit à la main par artiste) : accords singulier/pluriel, égalités entre familles
	// gérées, libellés publics issus de la source canonique (familles-public.js).
	import PortraitMaitre from '$lib/PortraitMaitre.svelte';
	import { nombre } from '$lib/joconde.js';
	import { FAMILLE_PUBLIC, ORDRE_FAMILLES } from '$lib/familles-public.js';
	import { bioMaitre } from '$lib/editorial-maitres.js';

	let { maitre, portrait } = $props();

	// Espace des milliers VISIBLE et insécable : l'espace fine de toLocaleString (U+202F)
	// ne se voit pas dans Spectral → espace insécable normale (U+00A0), localement.
	const fr = (n) => nombre(n).replace(/[\u202f\u00a0\s]/g, '\u00a0');

	// Total de RÉFÉRENCE = attributions directes + formulations prudentes (propre + doute).
	// Il n'inclut PAS les copies « d'après » ni les catégories exclues par le pipeline :
	// d'où « dans le périmètre étudié » (voir page Méthode).
	const totalNom = $derived(maitre.propre + maitre.doute);
	const pctDoute = $derived(totalNom ? Math.round((maitre.doute / totalNom) * 100) : 0);

	// Formulation(s) dominante(s). En cas d'ÉGALITÉ, on garde toutes les familles au
	// maximum, ordonnées par ORDRE_FAMILLES (jamais l'ordre accidentel des données).
	const dominance = $derived.by(() => {
		const max = Math.max(...maitre.familles.map((f) => f.notices));
		const codes = maitre.familles
			.filter((f) => f.notices === max)
			.map((f) => f.code)
			.sort((a, b) => ORDRE_FAMILLES.indexOf(a) - ORDRE_FAMILLES.indexOf(b));
		return {
			labels: codes.map((c) => FAMILLE_PUBLIC[c].label),
			notices: max,
			part: maitre.doute ? Math.round((max / maitre.doute) * 100) : 0
		};
	});

	// Répartition entre musées : même corpus que la vue Musées (nb_musees_doute).
	const phraseMusees = $derived.by(() => {
		const n = maitre.doute;
		const x = maitre.nb_musees_doute;
		if (x <= 0) return null;
		const sujet = n === 1 ? 'Cette notice' : `Ces ${fr(n)} notices`;
		if (x === 1) {
			return n === 1 ? 'Cette notice relève d’un musée.' : `${sujet} relèvent d’un même musée.`;
		}
		return `${sujet} se répartissent entre ${fr(x)} musées.`;
	});

	// Accord « notice / notices » et connecteur d'énumération française (« a, b et c »).
	const noticeMot = (n) => (n === 1 ? 'notice' : 'notices');
	const sep = (i, len) => (i === len - 1 ? '' : i === len - 2 ? ' et ' : ', ');
</script>

<div class="bandeau">
	<div class="bandeau-portrait">
		<PortraitMaitre {maitre} {portrait} />
	</div>

	<div class="bandeau-texte">
		<h2>{maitre.nom}</h2>
		{#if bioMaitre(maitre.nom)}
			<p class="bio">{bioMaitre(maitre.nom)}</p>
		{/if}

		<!-- INFORMATION PRINCIPALE : le doute, sujet de la rubrique. -->
		<p class="principal">
			<span class="valeur">{fr(maitre.doute)}</span>
			<span class="legende">notices où son nom est accompagné d’une formulation prudente</span>
		</p>

		<!-- DÉNOMINATEUR : la part, en registre secondaire. -->
		<p class="denominateur">
			<span class="pct">{pctDoute}&nbsp;%</span>
			<span class="glose">des {fr(totalNom)} notices associées à son nom dans le périmètre étudié</span>
		</p>

		<!-- RÉPARTITION entre musées (même corpus que la vue Musées). -->
		{#if phraseMusees}
			<p class="repartition">{phraseMusees}</p>
		{/if}

		<!-- FORMULATION DOMINANTE, générée depuis les données (accords + égalités). -->
		<p class="dominante">
			{#if dominance.labels.length === 1}
				La formulation la plus fréquente est <span class="forme"
					>«&nbsp;{dominance.labels[0]}&nbsp;»</span
				>&nbsp;: {fr(dominance.notices)}
				{noticeMot(dominance.notices)}, soit {dominance.part}&nbsp;%.
			{:else}
				Les formulations les plus fréquentes sont {#each dominance.labels as l, i}<span
						class="forme">«&nbsp;{l}&nbsp;»</span
					>{sep(i, dominance.labels.length)}{/each}&nbsp;: {fr(dominance.notices)}
				{noticeMot(dominance.notices)} chacune, soit {dominance.part}&nbsp;%.
			{/if}
		</p>
	</div>
</div>

<style>
	/* Portrait (largeur bornée, AGRANDI dans le bandeau — charte §5) à gauche, texte
	   à droite. justify-content: start → le bloc reste calé à gauche, pas étalé. */
	.bandeau {
		display: grid;
		grid-template-columns: 16rem minmax(0, 34rem);
		justify-content: start;
		gap: var(--espace-6);
		align-items: start;
		margin-top: var(--espace-2);
	}

	.bandeau-portrait {
		width: 16rem;
		max-width: 100%;
	}

	.bandeau-texte {
		display: flex;
		flex-direction: column;
	}

	h2 {
		font-family: var(--police-titre);
		font-size: var(--taille-xxl);
		line-height: 1.02;
		letter-spacing: -0.015em;
		margin: 0;
	}

	.bio {
		margin: var(--espace-1) 0 0;
		color: var(--couleur-encre-douce);
		font-style: italic;
	}

	/* --- Information principale : le doute domine visuellement la scène. --- */
	.principal {
		margin: var(--espace-4) 0 0;
		display: flex;
		flex-direction: column;
		gap: 0.15rem;
	}

	.principal .valeur {
		font-family: var(--police-titre);
		font-size: clamp(2.6rem, 6vw, 3.4rem);
		font-weight: 700;
		line-height: 1;
		color: var(--accent-cobalt);
		font-variant-numeric: tabular-nums;
	}

	.principal .legende {
		font-size: var(--taille-s);
		line-height: 1.4;
		color: var(--couleur-encre-douce);
		max-width: 30rem;
	}

	/* --- Dénominateur : contexte, nettement plus discret que la valeur principale. --- */
	.denominateur {
		margin: var(--espace-2) 0 0;
		display: flex;
		align-items: baseline;
		gap: var(--espace-2);
		flex-wrap: wrap;
	}

	.denominateur .pct {
		font-family: var(--police-titre);
		font-size: var(--taille-l);
		font-weight: 700;
		line-height: 1.1;
		color: var(--couleur-encre-douce);
		font-variant-numeric: tabular-nums;
	}

	.denominateur .glose {
		font-size: var(--taille-s);
		line-height: 1.4;
		color: var(--couleur-encre-douce);
		max-width: 26rem;
	}

	/* --- Répartition + formulation dominante : phrases courantes, registre de lecture. --- */
	.repartition {
		margin: var(--espace-4) 0 0;
		font-size: var(--taille-m);
		line-height: 1.5;
	}

	.dominante {
		margin: var(--espace-3) 0 0;
		font-size: var(--taille-m);
		line-height: 1.55;
	}

	/* La formule dominante ressort en Fraunces, comme un verbatim court (charte §4) —
	   c'est le mot du musée, pas une glose. */
	.forme {
		font-family: var(--police-titre);
		color: var(--couleur-encre);
	}

	/* Bandeau étroit : une seule colonne — portrait puis texte, calés à gauche. Le
	   seuil porte sur la largeur RÉELLE de la fiche (conteneur de requête défini par
	   la fiche parente). */
	@container (max-width: 38rem) {
		.bandeau {
			grid-template-columns: 1fr;
			gap: var(--espace-4);
		}
		.bandeau-portrait {
			justify-self: start;
		}
		.principal .valeur {
			font-size: clamp(2.4rem, 12vw, 3rem);
		}
	}
</style>
