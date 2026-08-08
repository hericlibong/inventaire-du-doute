<script>
	import NuageFamilles from '$lib/NuageFamilles.svelte';
	import OeuvresMaitre from '$lib/OeuvresMaitre.svelte';
	import CarteMaitre from '$lib/CarteMaitre.svelte';
	import BandeauMaitre from '$lib/BandeauMaitre.svelte';
	import Repertoire from '$lib/Repertoire.svelte';
	import { base } from '$app/paths';
	// Archive : la piste « galaxie » est conservée dans $lib/GalaxieMaitre.svelte
	// (abandonnée dans cette vue, decisions.md 2026-07-08), non importée ici.

	let { data } = $props();
	const artistes = data.artistes.artistes;
	const portraits = data.portraits;

	// L'effectif d'artistes ne s'affiche plus ici : l'introduction qui le portait a
	// été retirée en phase 5 (2026-08-02). Il se lit sur la page « Présentation »,
	// où il vient des mêmes exports.

	// Onglets de la fiche maître : profil (graphique) · oeuvres · musees.
	let vue = $state('profil');

	// Un premier maître est sélectionné à l'ouverture (decisions.md 2026-07-18 quater) :
	// la page est un espace d'exploration DÈS l'arrivée.
	let selection = $state(artistes[0].nom);
	const maitre = $derived(artistes.find((a) => a.nom === selection));

	// Musée filtré dans l'onglet « Œuvres » (code Muséofile, ou null). Il vit ICI,
	// pas dans l'onglet : les onglets sont démontés quand on en change, et la carte
	// du profil doit pouvoir le poser avant d'ouvrir « Œuvres » (phase 3). Un seul
	// système de filtrage, un seul endroit où l'état est tenu.
	let museeActif = $state(null);
	// Changer d'artiste vide le filtre : un code de musée ne vaut que pour l'artiste
	// où il a été choisi.
	$effect(() => {
		selection;
		museeActif = null;
	});

	// Carte → œuvres (phase 3) : le musée choisi sur la carte devient le filtre de
	// l'onglet « Œuvres », et on y bascule. L'artiste ne change pas. Un seul
	// système de filtrage : la carte ne filtre rien, elle pose l'état commun.
	function voirOeuvresDuMusee(code) {
		museeActif = code;
		vue = 'oeuvres';
	}
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
			<!-- ENTRÉE DIRECTE (phase 5, 2026-08-02). L'introduction de deux paragraphes a
			     été retirée : elle réexpliquait, au-dessus du répertoire, ce que la page
			     « Présentation » dit désormais mieux et plus longuement. Cette page-ci est
			     un outil — on y vient pour chercher un artiste, pas pour lire. Reste le
			     titre, un renvoi discret, et la sélection. -->
			<header class="intro">
				<h1>Explorer les artistes</h1>
				<p class="renvoi">
					<a href="{base}/projet">
						Comment ces artistes ont-ils été sélectionnés&nbsp;?
					</a>
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
						<OeuvresMaitre {maitre} bind:museeActif />
					{:else}
						<CarteMaitre {maitre} onVoirOeuvres={voirOeuvresDuMusee} />
					{/if}
				</div>
			{/if}
		</div>
	</div>
</div>

<style>
	/* La route est en pleine largeur (main.pleine) : elle gère elle-même sa
	   gouttière. Conteneur centré (2026-07-28) — la grille n'est plus collée au bord
	   gauche : largeur fluide bornée, centrée, padding horizontal responsive. Le
	   masthead reste à sa propre largeur ; ici on aère l'exploration. */
	.page {
		box-sizing: border-box;
		width: 100%;
		max-width: 92rem;
		margin-inline: auto;
		padding-inline: clamp(1.25rem, 3vw, 3rem);
		/* espace masthead → grille : ~1,5 rem (mobile) à ~3,5 rem (desktop). */
		padding-top: clamp(1.5rem, 3.5vw, 3.5rem);
		padding-bottom: var(--espace-6);
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

	/* Renvoi vers la Présentation : discret, registre UI, jamais un bouton. */
	.intro p.renvoi {
		margin: var(--espace-2) 0 var(--espace-3);
		font-family: var(--police-ui);
		font-size: var(--taille-s);
	}

	/* Liens éditoriaux : cobalt ET soulignement permanent (2026-08-08, phase 3).
	   Le cobalt seul ne suffisait pas à dire qu'un mot se clique : la même couleur
	   met en valeur les nombres importants, qui ne sont pas des liens. La couleur
	   reste, le trait la double — et l'information ne repose plus sur elle seule.
	   Le soulignement est natif (`text-decoration`) et non un `border-bottom` :
	   il ne déplace pas le texte quand il s'épaissit au survol, et il évite les
	   jambages. */
	.intro p.renvoi a {
		color: var(--accent-cobalt);
		text-decoration: underline;
		text-decoration-color: rgba(53, 87, 138, 0.45);
		text-decoration-thickness: 1px;
		text-underline-offset: 0.18em;
	}

	.intro p.renvoi a:hover,
	.intro p.renvoi a:focus-visible {
		text-decoration-color: var(--accent-cobalt);
		text-decoration-thickness: 2px;
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
	/* BARRE D'ONGLETS (refaite le 2026-08-08, phase 3).
	   Avant : trois libellés en petit corps, espacés de 1,5 rem sous le portrait. Ils
	   se lisaient comme une série de liens, et rien ne disait qu'ils commandent les
	   TROIS VUES de l'exploration. Ils forment maintenant une barre : un filet qui
	   court sur toute la largeur de la zone d'exploration la délimite, des filets
	   verticaux séparent les emplacements, et les libellés se touchent presque. Pas
	   d'arrondi, pas d'ombre, pas de fond de carte — c'est une barre éditoriale, pas
	   un groupe de boutons. */
	.bascule {
		display: flex;
		gap: 0;
		margin-top: var(--espace-5);
		border-bottom: 2px solid var(--couleur-trait);
	}

	.bascule button {
		background: none;
		border: none;
		/* Le filet vertical fait le groupe : il sépare les emplacements sans les
		   transformer en boutons. Le premier n'en a pas — une barre ne s'ouvre pas
		   sur un trait. */
		border-left: 1px solid var(--couleur-trait-clair);
		/* Le filet de l'onglet actif se pose SOUS celui de la barre : ils se
		   superposent au lieu de s'additionner, la ligne de base ne bouge pas. */
		margin-bottom: -2px;
		border-bottom: 2px solid transparent;
		/* Cible généreuse : 44 px de haut au minimum, y compris au toucher. */
		padding: 0.72rem 1.15rem;
		font-family: var(--police-ui);
		font-size: var(--taille-s);
		font-weight: 600;
		letter-spacing: 0.05em;
		text-transform: uppercase;
		/* Encre pleine et non encre douce : un onglet inactif reste un choix
		   disponible, il ne doit pas avoir l'air désactivé. */
		color: var(--couleur-encre);
		cursor: pointer;
		transition: background 140ms ease, color 140ms ease;
	}

	.bascule button:first-child {
		border-left: none;
	}

	.bascule button:hover {
		background: rgba(53, 87, 138, 0.06);
		color: var(--accent-cobalt);
	}

	/* L'onglet actif cumule QUATRE signes : la couleur, la graisse, un filet
	   inférieur épais et un fond très atténué. Aucun ne porte l'information seul. */
	.bascule button.actif {
		color: var(--accent-cobalt);
		font-weight: 700;
		border-bottom-color: var(--accent-cobalt);
		background: rgba(53, 87, 138, 0.07);
	}

	.bascule button:focus-visible {
		outline: var(--focus-anneau);
		outline-offset: -2px;
	}

	@media (prefers-reduced-motion: reduce) {
		.bascule button {
			transition: none;
		}
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

		/* Les trois onglets se partagent la largeur à parts égales et restent sur UNE
		   ligne : trois vues, trois emplacements, aucun repli. Le corps et les marges
		   se resserrent juste assez pour qu'aucun libellé ne soit tronqué — « Œuvres »
		   est le plus long des trois. */
		.bascule button {
			flex: 1 1 0;
			padding: 0.8rem 0.4rem;
			font-size: 0.8rem;
			letter-spacing: 0.03em;
			text-align: center;
			white-space: nowrap;
		}
	}
</style>
