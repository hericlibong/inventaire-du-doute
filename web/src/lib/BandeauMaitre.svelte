<script>
	// « La scène du maître » (docs/charte-graphique.md §5) : portrait agrandi + nom
	// + phrase de synthèse CALCULÉE + chiffres vedettes. Nommé BandeauMaitre et pas
	// ProfilMaitre : « Profil » est un nom d'onglet (décision utilisateur 2026-07-16).
	// Absorbe l'ancien bloc <header>.profil de la fiche ; le kit prend le relais des
	// styles au jugé (portrait, chiffres, disposition) via les tokens.
	//
	// La phrase de synthèse est FACTUELLE et calculée depuis artistes.json (mention
	// dominante + part racontée en français), pas un angle interprétatif : on nomme
	// la formule que les musées emploient le plus, sans dire ce qu'elle « signifie »
	// (le sens reste aux tooltips et au graphique). Le paragraphe de situation, lui,
	// ne fait toujours que situer volume et dispersion (décision 2026-07-10).
	import PortraitMaitre from '$lib/PortraitMaitre.svelte';
	import ChiffreVedette from '$lib/ChiffreVedette.svelte';
	import { nombre, deNom, fractionEnMots } from '$lib/joconde.js';
	import { FAMILLE_PUBLIC } from '$lib/familles-public.js';
	import { bioMaitre } from '$lib/editorial-maitres.js';

	let { maitre, portrait } = $props();

	// Total d'attributions rattachées au nom (ferme + doute) : situe le volume.
	const totalNom = $derived(maitre.propre + maitre.doute);

	// Synthèse calculée : la forme de doute la plus employée pour ce maître, et sa
	// part parmi les œuvres concernées. Familles = les 8 formes de doute (toutes
	// comparables), on prend simplement la plus nombreuse.
	const dominante = $derived.by(() => {
		const f = maitre.familles.reduce((a, b) => (b.notices > a.notices ? b : a));
		return {
			label: FAMILLE_PUBLIC[f.code].label,
			part: maitre.doute ? Math.round((f.notices / maitre.doute) * 100) : 0
		};
	});
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

		<!-- Synthèse : nomme la formule dominante, sans l'interpréter. -->
		<p class="synthese">
			Le plus souvent&nbsp;: <span class="forme">«&nbsp;{dominante.label}&nbsp;»</span>,
			{fractionEnMots(dominante.part)} des œuvres concernées.
		</p>

		<div class="chiffres">
			<ChiffreVedette valeur={nombre(totalNom)} legende={`œuvres sous le nom ${deNom(maitre.nom)}`} />
			<ChiffreVedette valeur={nombre(maitre.musees)} legende="musées où elles sont conservées" />
		</div>
	</div>
</div>

<style>
	/* Portrait (largeur bornée, AGRANDI dans le bandeau — charte §5) à gauche, texte
	   à droite. justify-content: start → le bloc reste calé à gauche, pas étalé. */
	.bandeau {
		display: grid;
		grid-template-columns: 14rem minmax(0, 26rem);
		justify-content: start;
		gap: var(--espace-6);
		align-items: start;
		margin-top: var(--espace-2);
	}

	.bandeau-portrait {
		width: 14rem;
		max-width: 100%;
	}

	.bandeau-texte {
		display: flex;
		flex-direction: column;
		gap: var(--espace-3);
	}

	h2 {
		font-family: var(--police-titre);
		font-size: var(--taille-xl);
		line-height: 1.1;
		margin: 0;
	}

	.bio {
		margin: 0;
		color: var(--couleur-encre-douce);
		font-style: italic;
	}

	.synthese {
		margin: 0;
		font-size: var(--taille-m);
		line-height: 1.55;
	}

	/* La formule dominante ressort en Fraunces, comme un verbatim court (charte §4) —
	   c'est le mot du musée, pas une glose. */
	.forme {
		font-family: var(--police-titre);
		color: var(--couleur-encre);
	}

	.chiffres {
		display: flex;
		flex-wrap: wrap;
		gap: var(--espace-5);
		margin-top: var(--espace-2);
	}

	/* Bandeau étroit : une seule colonne — portrait puis texte, calés à gauche. Le
	   seuil porte sur la largeur RÉELLE de la fiche (conteneur de requête défini par
	   la fiche parente), donc le passage se fait « plus tôt » quand l'aside comprime
	   la colonne (même logique que l'ancien header). */
	@container (max-width: 34rem) {
		.bandeau {
			grid-template-columns: 1fr;
			gap: var(--espace-4);
		}
		.bandeau-portrait {
			justify-self: start;
		}
	}
</style>
