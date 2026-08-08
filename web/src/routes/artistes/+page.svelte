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
					<button
						role="tab"
						data-label="Profil"
						aria-selected={vue === 'profil'}
						class:actif={vue === 'profil'}
						onclick={() => (vue = 'profil')}>Profil</button>
					<button
						role="tab"
						data-label="Œuvres"
						aria-selected={vue === 'oeuvres'}
						class:actif={vue === 'oeuvres'}
						onclick={() => (vue = 'oeuvres')}>Œuvres</button>
					<button
						role="tab"
						data-label="Musées"
						aria-selected={vue === 'musees'}
						class:actif={vue === 'musees'}
						onclick={() => (vue = 'musees')}>Musées</button>
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
	/* LES TROIS COMMANDES DE LA VISUALISATION (2026-08-08, deuxième version).
	   La première tentative avait fait une barre : un filet courant sur toute la
	   largeur, sous trois libellés. Elle regroupait mieux, mais le filet attirait
	   l'œil plus que les commandes, se lisait comme un séparateur de section, et les
	   onglets restaient des liens éditoriaux. Il n'y a donc plus de filet horizontal
	   au-delà de « Musées » : un GROUPE de trois boutons contigus, cerné d'une seule
	   bordure fine, séparés par des filets verticaux. Rien ne se prolonge dans la
	   page. Ni arrondi, ni ombre, ni icône. */
	.bascule {
		display: inline-flex;
		width: max-content;
		max-width: 100%;
		margin-top: var(--espace-5);
		border: 1px solid var(--couleur-trait);
		border-radius: 2px;
		overflow: hidden;
	}

	.bascule button {
		background: var(--couleur-surface, #fffdf9);
		border: none;
		/* Séparation verticale entre les boutons ; le premier n'en a pas. */
		border-left: 1px solid var(--couleur-trait);
		/* Cible d'au moins 44 px de haut. */
		padding: 0.78rem 1.35rem;
		font-family: var(--police-ui);
		font-size: var(--taille-s);
		font-weight: 600;
		letter-spacing: 0.05em;
		text-transform: uppercase;
		color: var(--couleur-encre);
		cursor: pointer;
		transition: background 140ms ease, color 140ms ease;
	}

	.bascule button:first-child {
		border-left: none;
	}

	/* La graisse de l'onglet actif est plus forte que celle des autres : sans
	   précaution, le groupe changerait de largeur à chaque clic et la page
	   bougerait. Chaque bouton réserve donc en permanence la place de son propre
	   libellé en gras — un double invisible, de hauteur nulle. */
	.bascule button::after {
		content: attr(data-label);
		display: block;
		height: 0;
		overflow: hidden;
		visibility: hidden;
		font-weight: 800;
		pointer-events: none;
	}

	.bascule button:hover {
		background: rgba(53, 87, 138, 0.1);
		color: var(--accent-cobalt);
	}

	/* Actif : aplat cobalt franc et texte clair. Rien ne déborde du groupe. */
	.bascule button.actif {
		background: var(--accent-cobalt);
		color: #f4f1ea;
		font-weight: 800;
	}

	.bascule button.actif:hover {
		background: #2d4d78;
		color: #f4f1ea;
	}

	.bascule button:focus-visible {
		outline: var(--focus-anneau);
		outline-offset: -3px;
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

		/* Le groupe prend toute la largeur disponible, les trois boutons se la
		   partagent à parts égales et restent sur UNE ligne. Le corps et les marges
		   se resserrent juste assez pour qu'aucun libellé ne soit tronqué —
		   « Musées » est le plus long des trois. */
		.bascule {
			display: flex;
			width: 100%;
		}

		.bascule button {
			flex: 1 1 0;
			padding: 0.8rem 0.35rem;
			font-size: 0.8rem;
			letter-spacing: 0.02em;
			text-align: center;
			white-space: nowrap;
		}
	}
</style>
