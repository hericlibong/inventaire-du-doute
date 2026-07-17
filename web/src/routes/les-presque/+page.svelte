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
	// tri et la liste vivent dans le Répertoire (colonne de navigation) ; la page ne
	// garde que la sélection, partagée avec la scène du maître.
	let selection = $state(artistes[0].nom);
	const maitre = $derived(artistes.find((a) => a.nom === selection));

	// Folio discret (repère secondaire, jamais un décor) : rang dans la liste + cote
	// du musée principal, tirés des données existantes.
	const rang = $derived(artistes.findIndex((a) => a.nom === selection) + 1);
</script>

<header class="dossier">
	<h1>Les presque</h1>
	<div class="lead">
		<p>
			Ici, «&nbsp;Les presque&nbsp;» désigne les œuvres que les musées rapprochent d'un
			grand artiste sans les lui attribuer tout à fait. Dans les notices, cela passe par
			des formules comme «&nbsp;attribué à&nbsp;», «&nbsp;atelier de&nbsp;»,
			«&nbsp;école de&nbsp;», «&nbsp;entourage de&nbsp;» : le nom du maître est présent,
			mais accompagné d'une réserve.
		</p>
		<p>
			Cette rubrique rassemble {artistes.length} noms pour lesquels les musées de
			France utilisent souvent ce type de mention : au moins vingt œuvres concernées
			pour chacun. Pour chaque artiste, la jauge colorée donne un premier aperçu. Le
			graphique détaille les formules employées, les œuvres montrent des exemples
			concrets, et la carte indique où elles sont conservées en France.
		</p>
	</div>
	<p class="precaution">
		Cette rubrique ne réattribue aucune œuvre. Elle reprend les mots publiés par les
		musées dans leurs notices, avec leurs précautions.
	</p>
</header>

<div class="grille">
	<!-- Colonne de navigation : recherche + tri + liste + microprofils. La légende
	     détaillée des mentions n'est plus ici (elle vit dans « Comprendre les
	     mentions ») : le répertoire est un pur outil de choix. -->
	<Repertoire {artistes} bind:selection />

	{#if maitre}
		<section class="fiche">
			<p class="folio">
				Nº {rang} / {artistes.length}{maitre.musee_principal
					? ` · cote ${maitre.musee_principal.code}`
					: ''}
			</p>

			<!-- Bandeau « scène du maître » : portrait (origine de la ligne) + nom +
			     synthèse + chiffres. HORS de la zone d'onglet → visible sur les trois vues. -->
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

			<div class="vue">
				{#if vue === 'profil'}
					<NuageFamilles {maitre} {plafond} />
				{:else if vue === 'oeuvres'}
					<OeuvresMaitre {maitre} />
				{:else}
					<CarteMaitre {maitre} />
				{/if}
			</div>
		</section>
	{/if}
</div>

<style>
	/* En-tête de dossier compact : le profil doit apparaître dès le premier écran. */
	.dossier {
		max-width: 48rem;
		margin-bottom: var(--espace-5);
	}

	.dossier h1 {
		font-family: var(--police-titre);
		font-size: var(--taille-xl);
		margin: 0 0 var(--espace-3);
	}

	.lead p {
		font-size: 1.05rem;
		line-height: 1.6;
		margin: 0 0 var(--espace-2);
	}

	/* Précaution : plus une boîte grise (Direction B), un filet et de l'italique. */
	.precaution {
		margin: var(--espace-3) 0 0;
		border-left: 2px solid var(--couleur-accent);
		padding-left: var(--espace-3);
		font-style: italic;
		font-size: var(--taille-s);
		color: var(--couleur-encre-douce);
	}

	.grille {
		display: grid;
		grid-template-columns: minmax(13rem, 16rem) 1fr;
		gap: var(--espace-6);
		margin-top: var(--espace-4);
	}

	@media (max-width: 720px) {
		.grille {
			grid-template-columns: 1fr;
			gap: var(--espace-5);
		}
	}

	.fiche {
		/* conteneur de requête : le bandeau passe en une colonne selon la largeur
		   RÉELLE de la fiche (seuil géré dans BandeauMaitre). */
		container-type: inline-size;
	}

	/* Folio : repère secondaire, encre douce, discret. */
	.folio {
		font-family: var(--police-ui);
		font-size: var(--taille-xs);
		letter-spacing: 0.1em;
		text-transform: uppercase;
		color: var(--couleur-encre-douce);
		margin: 0 0 var(--espace-3);
	}

	/* Onglets en soulignement (fin de la boîte à fond plein). */
	.bascule {
		display: flex;
		gap: var(--espace-5);
		margin-top: var(--espace-4);
		border-bottom: var(--filet);
	}

	.bascule button {
		background: none;
		border: none;
		padding: 0 0 var(--espace-2);
		font-family: var(--police-ui);
		font-size: var(--taille-s);
		letter-spacing: 0.04em;
		text-transform: uppercase;
		color: var(--couleur-encre-douce);
		cursor: pointer;
	}

	.bascule button:hover {
		color: var(--couleur-encre);
	}

	.bascule button.actif {
		color: var(--couleur-encre);
		font-weight: 700;
		box-shadow: 0 2px 0 var(--couleur-encre);
	}

	.bascule button:focus-visible {
		outline: var(--focus-anneau);
		outline-offset: 3px;
	}

	.vue {
		margin-top: var(--espace-4);
	}
</style>
