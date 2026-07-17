<script>
	import NuageFamilles from '$lib/NuageFamilles.svelte';
	import OeuvresMaitre from '$lib/OeuvresMaitre.svelte';
	import CarteMaitre from '$lib/CarteMaitre.svelte';
	import BandeauMaitre from '$lib/BandeauMaitre.svelte';
	import Repertoire from '$lib/Repertoire.svelte';
	// Archive : la piste « galaxie » est conservée dans $lib/GalaxieMaitre.svelte
	// (abandonnée dans cette vue, decisions.md 2026-07-08), non importée ici.

	let { data } = $props();
	const artistes = data.artistes.artistes;
	// Manifeste des portraits (Commons) : source secondaire d'illustration.
	const portraits = data.portraits;

	// Plafond COMMUN de l'axe Y du nuage : la plus grande valeur de famille sur
	// tous les maîtres (≈ 240, « école de » Le Brun). Calculé ici, pas en dur.
	const plafond = Math.max(
		...artistes.flatMap((a) => a.familles.map((f) => f.notices))
	);

	// Onglets de la fiche maître (libellés éditoriaux, charte §5) :
	//   profil  — le graphique des formes et volumes du doute (NuageFamilles) ;
	//   oeuvres — les cas concrets, avec les mots publiés (OeuvresMaitre) ;
	//   musees  — où ces œuvres sont conservées, sur la carte (CarteMaitre).
	let vue = $state('profil');

	// Maître sélectionné pour la fiche (le plus douté par défaut). La recherche, le
	// tri et la liste vivent désormais dans le Répertoire (colonne de navigation) ;
	// la page ne garde que la sélection, partagée avec la scène du maître.
	let selection = $state(artistes[0].nom);
	const maitre = $derived(artistes.find((a) => a.nom === selection));
</script>

<h1>Les presque</h1>
<p class="chapo">
	Ici, «&nbsp;Les presque&nbsp;» désigne les œuvres que les musées rapprochent d'un
	grand artiste sans les lui attribuer tout à fait. Dans les notices, cela passe par
	des formules comme «&nbsp;attribué à&nbsp;», «&nbsp;atelier de&nbsp;»,
	«&nbsp;école de&nbsp;», «&nbsp;entourage de&nbsp;» : le nom du maître est présent,
	mais accompagné d'une réserve.
</p>
<p class="chapo">
	Cette rubrique rassemble {artistes.length} noms pour lesquels les musées de
	France utilisent souvent ce type de mention : au moins vingt œuvres concernées
	pour chacun. Pour chaque artiste, la jauge colorée donne un premier aperçu. Le
	graphique détaille les formules employées, les œuvres montrent des exemples
	concrets, et la carte indique où elles sont conservées en France.
</p>
<p class="mode-emploi">
	Cette rubrique ne réattribue aucune œuvre. Elle reprend les mots publiés par les
	musées dans leurs notices, avec leurs précautions.
</p>

<div class="grille">
	<!-- Colonne de navigation : recherche + tri + liste + microprofils. La légende
	     détaillée des mentions n'est plus ici (elle rejoindra « Comprendre les
	     mentions », architecture §3) : le répertoire est un pur outil de choix. -->
	<Repertoire {artistes} bind:selection />

	{#if maitre}
		<section class="fiche">
			<!-- Bandeau « scène du maître » : portrait + nom + synthèse + chiffres.
			     HORS de la zone d'onglet → visible sur les trois vues, sans saut au
			     changement (charte §5, ancien header.profil absorbé). -->
			<BandeauMaitre {maitre} portrait={portraits[maitre.nom]} />

			<div class="bascule" role="tablist" aria-label="Choisir la vue">
				<button role="tab" aria-selected={vue === 'profil'} class:actif={vue === 'profil'} onclick={() => (vue = 'profil')}>
					Profil
				</button>
				<button role="tab" aria-selected={vue === 'oeuvres'} class:actif={vue === 'oeuvres'} onclick={() => (vue = 'oeuvres')}>
					Œuvres
				</button>
				<button role="tab" aria-selected={vue === 'musees'} class:actif={vue === 'musees'} onclick={() => (vue = 'musees')}>
					Musées
				</button>
			</div>

			{#if vue === 'profil'}
				<NuageFamilles {maitre} {plafond} />
			{:else if vue === 'oeuvres'}
				<OeuvresMaitre {maitre} />
			{:else}
				<CarteMaitre {maitre} />
			{/if}
		</section>
	{/if}
</div>

<style>
	.chapo {
		font-size: 1.15rem;
		max-width: 44rem;
	}

	.chapo:first-of-type {
		font-size: 1.2rem;
	}

	.mode-emploi {
		max-width: 44rem;
		padding: 0.6rem 0.9rem;
		background: rgba(122, 74, 43, 0.06);
		border-radius: 4px;
	}

	.grille {
		display: grid;
		grid-template-columns: minmax(14rem, 20rem) 1fr;
		gap: 2rem;
		margin-top: 1.5rem;
	}

	@media (max-width: 720px) {
		.grille {
			grid-template-columns: 1fr;
		}
	}

	.fiche {
		/* conteneur de requête : le bandeau passe en une colonne selon la largeur
		   RÉELLE de la fiche (pas celle de l'écran), donc « plus tôt » quand l'aside
		   comprime la colonne (décision 2026-07-11 ; seuil géré dans BandeauMaitre). */
		container-type: inline-size;
	}

	.bascule {
		display: inline-flex;
		gap: 0;
		margin-top: 0.75rem;
		border: 1px solid var(--couleur-trait);
		border-radius: 4px;
		overflow: hidden;
	}

	.bascule button {
		background: #fff;
		border: none;
		padding: 0.35rem 0.9rem;
		font: inherit;
		cursor: pointer;
		color: var(--couleur-encre-douce);
	}

	.bascule button.actif {
		background: var(--couleur-accent);
		color: #fff;
	}
</style>
