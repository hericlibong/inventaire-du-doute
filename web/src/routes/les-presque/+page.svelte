<script>
	import NuageFamilles from '$lib/NuageFamilles.svelte';
	import OeuvresMaitre from '$lib/OeuvresMaitre.svelte';
	import CarteMaitre from '$lib/CarteMaitre.svelte';
	import BandeauMaitre from '$lib/BandeauMaitre.svelte';
	import Repertoire from '$lib/Repertoire.svelte';
	import { nombre } from '$lib/joconde.js';
	// Archive : la piste « galaxie » est conservée dans $lib/GalaxieMaitre.svelte
	// (abandonnée dans cette vue, decisions.md 2026-07-08), non importée ici.

	let { data } = $props();
	const artistes = data.artistes.artistes;
	const portraits = data.portraits;

	// Chiffres de l'introduction, dérivés des données DÉJÀ chargées (artistes.json) —
	// pas de seconde source dans le composant (decisions.md 2026-07-19) :
	//   • nbMaitres = les 27 retenus ;
	//   • totalNotices = 2 341, somme des notices prudentes des 27.
	// Le seuil « au moins vingt notices » (critère du fichier) reste en toutes lettres.
	const nbMaitres = artistes.length;
	const totalNotices = artistes.reduce((s, a) => s + a.doute, 0);
	// Séparateur de milliers VISIBLE et insécable : l'espace fine de toLocaleString
	// (U+202F) ne se voit pas dans Spectral ici → on la remplace par une espace
	// insécable normale (U+00A0), localement (sans toucher joconde.js ni la scène).
	const totalNoticesTexte = nombre(totalNotices).replace(/[\u202f\u00a0\s]/g, '\u00a0');

	// Plafond COMMUN de l'axe Y du nuage (≈ 240). Calculé ici, pas en dur.
	const plafond = Math.max(...artistes.flatMap((a) => a.familles.map((f) => f.notices)));

	// Onglets de la fiche maître : profil (graphique) · oeuvres · musees.
	let vue = $state('profil');

	// Un premier maître est sélectionné à l'ouverture (decisions.md 2026-07-18 quater) :
	// la page est un espace d'exploration DÈS l'arrivée, pas un guide. On garde les
	// proportions de la refonte du 2026-07-18 (ter) — graphe borné, scène héros — mais
	// on abandonne l'état « guide » (seconde introduction supprimée). Recherche/tri/liste
	// = Répertoire (rail de gauche).
	let selection = $state(artistes[0].nom);
	const maitre = $derived(artistes.find((a) => a.nom === selection));

	// Folio discret (repère secondaire) : rang + cote du musée principal.
	const rang = $derived(artistes.findIndex((a) => a.nom === selection) + 1);
</script>

<div class="page">
	<!-- PREMIER TEMPS — entrée éditoriale (titre à gauche, texte à droite sur ordinateur).
	     Aucun encadré : la composition tient par la typographie et l'espace. Le titre
	     public de la rubrique est « Explorer les N maîtres » ; l'appellation « Les presque »
	     est abandonnée (decisions.md 2026-07-19). -->
	<header class="intro">
		<div class="intro-titre">
			<h1>Explorer les {nbMaitres} maîtres</h1>
		</div>
		<div class="intro-texte">
			<p>
				Dans un inventaire, le nom d'un artiste n'est pas toujours celui de l'auteur. Il
				peut désigner une attribution probable, le travail d'un atelier, une école ou une
				influence.
			</p>
			<p>
				Nous avons retenu {nbMaitres} artistes pour lesquels ces formulations apparaissent
				dans au moins vingt notices de la base Joconde. Ensemble, ils réunissent
				{totalNoticesTexte} notices accompagnées d'une formulation prudente. Ce seuil
				n'établit aucun palmarès&nbsp;: il permet de comparer des situations suffisamment
				documentées.
			</p>
			<p>
				Choisissez un nom pour découvrir les formulations employées, quelques œuvres
				concernées et les musées qui les conservent.
			</p>
			<p class="prudence">
				Le projet reprend les formulations publiées par les musées&nbsp;; il ne réattribue
				aucune œuvre.
			</p>
		</div>
	</header>

	<!-- SECOND TEMPS — l'exploration. Séparée du premier temps par un filet et de
	     l'espace (pas un nouveau bandeau) ; introduite par un intitulé simple. L'outil
	     lui-même (répertoire + scène + onglets + vues) est inchangé. -->
	<section class="exploration" aria-labelledby="titre-outil">
		<h2 id="titre-outil" class="outil-titre">Choisir un artiste</h2>

	<div class="grille">
		<!-- Répertoire en rail : recherche + tri + liste + microprofils. -->
		<Repertoire {artistes} bind:selection />

		{#if maitre}
			<section class="zone">
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
	</section>
</div>

<style>
	/* Pleine page : gouttières propres, pas de colonne centrale. */
	.page {
		padding: var(--espace-5) clamp(1rem, 4vw, 3rem) var(--espace-6);
	}

	/* --- PREMIER TEMPS : entrée éditoriale, deux colonnes (titre | texte). --- */
	.intro {
		display: grid;
		grid-template-columns: minmax(14rem, 22rem) minmax(0, 42rem);
		gap: clamp(1.5rem, 4vw, 3.5rem);
		align-items: start;
		max-width: 72rem;
		/* Respire, mais sans repousser l'exploration hors du premier écran. */
		margin: var(--espace-2) 0 clamp(2.25rem, 5vh, 3.5rem);
	}

	.intro-titre h1 {
		font-family: var(--police-titre);
		font-size: clamp(1.9rem, 3.4vw, var(--taille-xxl));
		line-height: 1.05;
		margin: 0;
	}

	.intro-texte p {
		font-size: var(--taille-m);
		line-height: 1.6;
		margin: 0 0 var(--espace-4);
	}

	.intro-texte p:last-child {
		margin-bottom: 0;
	}

	/* Prudence commune : note secondaire et discrète (pas un encadré d'alerte). */
	.intro-texte p.prudence {
		font-size: var(--taille-s);
		line-height: 1.5;
		color: var(--couleur-encre-douce);
		font-style: italic;
		margin-top: var(--espace-4);
	}

	/* --- SECOND TEMPS : l'exploration, détachée par un filet + de l'espace. --- */
	.exploration {
		border-top: var(--filet);
		padding-top: clamp(1.75rem, 4vh, 2.75rem);
	}

	/* Intitulé simple de l'outil : registre UI, repère cobalt discret devant. */
	.outil-titre {
		display: flex;
		align-items: center;
		gap: var(--espace-3);
		font-family: var(--police-ui);
		font-size: var(--taille-s);
		font-weight: 700;
		letter-spacing: 0.12em;
		text-transform: uppercase;
		color: var(--couleur-encre);
		margin: 0 0 var(--espace-5);
	}

	.outil-titre::before {
		content: '';
		width: 1.6rem;
		height: 3px;
		background: var(--accent-cobalt);
		flex: none;
	}

	@media (max-width: 760px) {
		/* Mobile : titre, texte et note s'empilent ; « Choisir un artiste » marque le
		   passage à l'outil. */
		.intro {
			grid-template-columns: 1fr;
			gap: var(--espace-4);
			margin-bottom: clamp(1.75rem, 5vh, 2.5rem);
		}
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

	/* La zone de droite : scène du maître (portrait + synthèse) puis onglets + vue. */
	.zone {
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

	/* Le graphe est une figure de SUPPORT, pas le héros (la scène raconte déjà le
	   maître). Borné à ~640 px, aligné à gauche : fin du graphe qui remplit ~900 px. */
	.vue {
		margin-top: var(--espace-4);
		max-width: 42rem;
	}
</style>
