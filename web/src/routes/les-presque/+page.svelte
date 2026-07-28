<script>
	import NuageFamilles from '$lib/NuageFamilles.svelte';
	import OeuvresMaitre from '$lib/OeuvresMaitre.svelte';
	import CarteMaitre from '$lib/CarteMaitre.svelte';
	import BandeauMaitre from '$lib/BandeauMaitre.svelte';
	import Repertoire from '$lib/Repertoire.svelte';
	import { base } from '$app/paths';
	import { enLettresCap } from '$lib/joconde.js';
	// Archive : la piste « galaxie » est conservée dans $lib/GalaxieMaitre.svelte
	// (abandonnée dans cette vue, decisions.md 2026-07-08), non importée ici.

	let { data } = $props();
	const artistes = data.artistes.artistes;
	const portraits = data.portraits;

	// Nombre de maîtres dérivé des données DÉJÀ chargées (artistes.json) — pas de
	// seconde source dans le composant (decisions.md 2026-07-19). Le détail du seuil
	// et le total de notices ont QUITTÉ l'introduction le 2026-07-20 : ils vivent
	// dans la page Méthode, atteignable par le lien « Pourquoi ces N artistes ? ».
	const nbMaitres = artistes.length;

	// Le nombre s'écrit en toutes lettres dans le corps du texte (CLAUDE.md).
	const nbMaitresTexte = enLettresCap(nbMaitres);

	// Onglets de la fiche maître : profil (graphique) · oeuvres · musees.
	let vue = $state('profil');

	// Un premier maître est sélectionné à l'ouverture (decisions.md 2026-07-18 quater) :
	// la page est un espace d'exploration DÈS l'arrivée.
	let selection = $state(artistes[0].nom);
	const maitre = $derived(artistes.find((a) => a.nom === selection));
</script>

<!-- Disposition refondue (2026-07-28) : une SEULE grille continue à deux colonnes,
     mêmes limites sur toute la page. L'introduction (titre + texte + lien Méthode)
     rejoint la colonne gauche, au-dessus de la recherche et de la liste ; plus de
     bandeau horizontal pleine largeur ni de séparation entre entrée et exploration.
     La colonne droite porte le profil de l'artiste sélectionné. -->
<div class="page">
	<div class="grille">
		<!-- COLONNE GAUCHE : entrée éditoriale, puis sélection (recherche + tri + liste). -->
		<div class="colonne-gauche">
			<header class="intro">
				<h1>Explorer les {nbMaitres} maîtres</h1>
				<p>
					Dans les inventaires, le nom d'un artiste ne désigne pas toujours l'auteur certain
					d'une œuvre. «&nbsp;Attribué à&nbsp;», «&nbsp;de son atelier&nbsp;», «&nbsp;de son
					école&nbsp;» ou «&nbsp;à sa manière&nbsp;» décrivent différents degrés de proximité
					avec le maître.
				</p>
				<p>
					{nbMaitresTexte} artistes réunissent ici assez d'œuvres pour être explorés et
					comparés.
				</p>
				<p class="renvoi">
					<a href="{base}/methode#les-maitres">Pourquoi ces {nbMaitres} artistes&nbsp;?&nbsp;→</a>
				</p>
				<p class="prudence">
					Le projet reprend les formulations publiées par les musées&nbsp;; il ne réattribue
					aucune œuvre.
				</p>
			</header>

			<!-- Sélection : intitulé simple, puis recherche + tri + liste (Repertoire). -->
			<h2 class="outil-titre">Choisir un artiste</h2>
			<Repertoire {artistes} bind:selection />
		</div>

		<!-- COLONNE DROITE : profil de l'artiste — portrait/identité + chiffres, onglets,
		     contenu de l'onglet actif. Le graphe et ses interactions sont inchangés. -->
		<div class="colonne-droite">
			{#if maitre}
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

				<div class="vue" class:vue-profil={vue === 'profil'}>
					{#if vue === 'profil'}
						<NuageFamilles {maitre} />
					{:else if vue === 'oeuvres'}
						<OeuvresMaitre {maitre} />
					{:else}
						<CarteMaitre {maitre} />
					{/if}
				</div>
			{/if}
		</div>
	</div>
</div>

<style>
	.page {
		/* padding horizontal porté par <main> (layout) ; ici, seulement le vertical. */
		padding-block: var(--espace-4) var(--espace-6);
	}

	/* --- Grille continue à deux colonnes, mêmes limites sur toute la page. --- */
	.grille {
		display: grid;
		grid-template-columns: clamp(16.5rem, 22vw, 20rem) minmax(0, 1fr);
		gap: clamp(1.75rem, 3.5vw, 3rem);
		align-items: start;
	}

	/* Colonne gauche : sticky sur desktop, elle se fige quand on défile ; sa hauteur
	   est bornée à l'écran et son contenu (surtout la liste) défile en interne, sans
	   bloquer le défilement principal de la colonne droite. */
	.colonne-gauche {
		position: sticky;
		top: var(--espace-4);
		align-self: start;
		max-height: calc(100vh - var(--espace-4) - var(--espace-5));
		overflow-y: auto;
		overscroll-behavior: contain;
		padding-right: 0.4rem; /* air pour la barre de défilement interne */
	}

	/* Titre de rubrique : aligné en haut de colonne (donc sur le portrait à droite). */
	.intro h1 {
		font-family: var(--police-titre);
		font-size: clamp(1.6rem, 2.2vw, 2.1rem);
		line-height: 1.06;
		margin: 0 0 var(--espace-4);
	}

	.intro p {
		font-size: var(--taille-m);
		line-height: 1.55;
		margin: 0 0 var(--espace-3);
	}

	/* Renvoi vers la Méthode : discret, registre UI, jamais un bouton. */
	.intro p.renvoi {
		margin: var(--espace-2) 0 var(--espace-3);
		font-family: var(--police-ui);
		font-size: var(--taille-s);
	}

	.intro p.renvoi a {
		color: var(--accent-cobalt);
		text-decoration: none;
		border-bottom: 1px solid transparent;
	}

	.intro p.renvoi a:hover,
	.intro p.renvoi a:focus-visible {
		border-bottom-color: var(--accent-cobalt);
	}

	/* Prudence : note secondaire et discrète (pas un encadré d'alerte). */
	.intro p.prudence {
		margin: 0 0 var(--espace-4);
		font-size: var(--taille-s);
		line-height: 1.5;
		color: var(--couleur-encre-douce);
		font-style: italic;
	}

	/* Intitulé de l'outil de sélection : registre UI, repère cobalt devant. */
	.outil-titre {
		display: flex;
		align-items: center;
		gap: var(--espace-3);
		margin: var(--espace-3) 0 var(--espace-4);
		font-family: var(--police-ui);
		font-size: var(--taille-s);
		font-weight: 700;
		letter-spacing: 0.12em;
		text-transform: uppercase;
		color: var(--couleur-encre);
	}

	.outil-titre::before {
		content: '';
		width: 1.6rem;
		height: 3px;
		background: var(--accent-cobalt);
		flex: none;
	}

	/* Colonne droite : conteneur de requête pour le bandeau (portrait / identité). */
	.colonne-droite {
		container-type: inline-size;
		min-width: 0;
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

	/* Le graphe est une figure de SUPPORT : borné, aligné à gauche. */
	.vue {
		margin-top: var(--espace-4);
		max-width: 42rem;
	}

	/* Onglet Profil : la légende est au flanc du graphe, la vue porte donc les deux
	   colonnes (le graphe garde sa proportion). Œuvres et Musées gardent leur largeur. */
	.vue-profil {
		max-width: 60rem;
	}

	/* --- Mobile (≤ 720 px, seuil du Repertoire) : une seule colonne. Ordre :
	   titre + intro, sélecteur repliable, profil, onglets, contenu actif. Le
	   Repertoire est replié d'emblée → la liste ne s'affiche pas avant le profil. --- */
	@media (max-width: 720px) {
		.grille {
			grid-template-columns: 1fr;
			gap: var(--espace-5);
		}
		.colonne-gauche {
			position: static;
			max-height: none;
			overflow: visible;
			padding-right: 0;
		}
	}
</style>
