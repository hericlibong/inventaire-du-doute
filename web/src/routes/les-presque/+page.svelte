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
	const portraits = data.portraits;

	// Plafond COMMUN de l'axe Y du nuage (≈ 240). Calculé ici, pas en dur.
	const plafond = Math.max(...artistes.flatMap((a) => a.familles.map((f) => f.notices)));

	// Onglets de la fiche maître : profil (graphique) · oeuvres · musees.
	let vue = $state('profil');

	// Maître sélectionné (le plus douté par défaut). Recherche/tri/liste = Répertoire.
	let selection = $state(artistes[0].nom);
	const maitre = $derived(artistes.find((a) => a.nom === selection));

	// Folio discret (repère secondaire) : rang + cote du musée principal.
	const rang = $derived(artistes.findIndex((a) => a.nom === selection) + 1);
</script>

<div class="page">
	<header class="dossier">
		<p class="kicker">Explorer les 27 maîtres</p>
		<h1>Les presque</h1>
		<p class="lead">
			Vingt-sept noms que les musées de France rapprochent d'un grand artiste sans le
			lui attribuer tout à fait — «&nbsp;attribué à&nbsp;», «&nbsp;atelier de&nbsp;»,
			«&nbsp;école de&nbsp;»… Choisissez un nom, puis lisez son profil, ses œuvres et
			les musées où elles sont conservées.
		</p>
		<p class="precaution">
			Cette rubrique ne réattribue aucune œuvre. Elle reprend les mots publiés par les
			musées dans leurs notices, avec leurs précautions.
		</p>
	</header>

	<div class="grille">
		<!-- Répertoire en rail : recherche + tri + liste + microprofils. -->
		<Repertoire {artistes} bind:selection />

		{#if maitre}
			<section class="fiche">
				<p class="folio">
					Nº {rang} / {artistes.length}{maitre.musee_principal
						? ` · cote ${maitre.musee_principal.code}`
						: ''}
				</p>

				<!-- Scène du maître : portrait + nom + synthèse + chiffres (hors onglets). -->
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
</div>

<style>
	/* Pleine page : gouttières propres, pas de colonne centrale. */
	.page {
		padding: var(--espace-5) clamp(1rem, 4vw, 3rem) var(--espace-6);
	}

	/* Entrée narrative courte (l'accueil ne pose plus le sujet). */
	.dossier {
		max-width: 58rem;
		margin-bottom: var(--espace-5);
	}

	.kicker {
		font-family: var(--police-ui);
		font-size: var(--taille-xs);
		letter-spacing: 0.14em;
		text-transform: uppercase;
		color: var(--accent-cobalt);
		margin: 0 0 var(--espace-2);
	}

	.dossier h1 {
		font-family: var(--police-titre);
		font-size: var(--taille-xl);
		margin: 0 0 var(--espace-3);
	}

	.lead {
		font-size: var(--taille-m);
		line-height: 1.6;
		max-width: 52rem;
		margin: 0;
	}

	.precaution {
		margin: var(--espace-3) 0 0;
		border-left: 2px solid var(--accent-vermillon);
		padding-left: var(--espace-3);
		font-style: italic;
		font-size: var(--taille-s);
		color: var(--couleur-encre-douce);
	}

	/* Zone principale pleine largeur : rail répertoire + scène/vues étalées. */
	.grille {
		display: grid;
		grid-template-columns: minmax(14rem, 17rem) 1fr;
		gap: var(--espace-6);
		align-items: start;
	}

	@media (max-width: 760px) {
		.grille {
			grid-template-columns: 1fr;
			gap: var(--espace-5);
		}
	}

	.fiche {
		container-type: inline-size; /* seuil du bandeau sur la largeur réelle */
		min-width: 0;
	}

	.folio {
		font-family: var(--police-ui);
		font-size: var(--taille-xs);
		letter-spacing: 0.1em;
		text-transform: uppercase;
		color: var(--couleur-encre-douce);
		margin: 0 0 var(--espace-3);
	}

	/* Onglets soulignés, actif en cobalt. */
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
		color: var(--accent-cobalt);
		font-weight: 700;
		box-shadow: 0 2px 0 var(--accent-cobalt);
	}

	.bascule button:focus-visible {
		outline: var(--focus-anneau);
		outline-offset: 3px;
	}

	.vue {
		margin-top: var(--espace-4);
	}
</style>
