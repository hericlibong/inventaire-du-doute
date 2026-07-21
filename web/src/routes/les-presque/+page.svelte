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

	// Nombre de maîtres dérivé des données DÉJÀ chargées (artistes.json) — pas de
	// seconde source dans le composant (decisions.md 2026-07-19). Le détail du seuil
	// et le total de notices ont QUITTÉ l'introduction le 2026-07-20 : ils retardaient
	// l'exploration et vivent désormais dans la page Méthode, atteignable par le lien
	// « Pourquoi ces N artistes ? ».
	const nbMaitres = artistes.length;

	// Le nombre s'écrit en toutes lettres dans le corps du texte (CLAUDE.md : écrire
	// les chiffres en français quand le récit prime). Table courte autour de la valeur
	// réelle, repli sur le chiffre si la liste changeait beaucoup.
	const EN_LETTRES = {
		24: 'Vingt-quatre',
		25: 'Vingt-cinq',
		26: 'Vingt-six',
		27: 'Vingt-sept',
		28: 'Vingt-huit',
		29: 'Vingt-neuf',
		30: 'Trente'
	};
	const nbMaitresTexte = EN_LETTRES[nbMaitres] ?? String(nbMaitres);

	// Plafond COMMUN de l'axe Y du nuage (≈ 240). Calculé ici, pas en dur.
	const plafond = Math.max(...artistes.flatMap((a) => a.familles.map((f) => f.notices)));

	// Le folio « Nº 4 / 27 · cote M5031 » a été retiré (2026-07-20) : ni le rang dans
	// la liste ni la cote du musée principal ne disent quoi que ce soit du profil.
	// Le profil commence par le portrait, le nom et la ligne d'identité.

	// Onglets de la fiche maître : profil (graphique) · oeuvres · musees.
	let vue = $state('profil');

	// Un premier maître est sélectionné à l'ouverture (decisions.md 2026-07-18 quater) :
	// la page est un espace d'exploration DÈS l'arrivée, pas un guide. On garde les
	// proportions de la refonte du 2026-07-18 (ter) — graphe borné, scène héros — mais
	// on abandonne l'état « guide » (seconde introduction supprimée). Recherche/tri/liste
	// = Répertoire (rail de gauche).
	let selection = $state(artistes[0].nom);
	const maitre = $derived(artistes.find((a) => a.nom === selection));
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
			<!-- Entrée resserrée (2026-07-20) : deux paragraphes courts, puis un lien vers
			     la Méthode. Le détail du seuil, le total de notices et le mode d'emploi ont
			     quitté l'introduction — ils retardaient l'exploration et vivent à leur place
			     (page Méthode). Seule la précaution reste, en note discrète. -->
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
				<a href="{base}/methode#les-27">Pourquoi ces {nbMaitres} artistes&nbsp;?&nbsp;→</a>
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

				<div class="vue" class:vue-profil={vue === 'profil'}>
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

	/* Renvoi vers la Méthode : discret, registre UI, jamais un bouton. Le détail du
	   seuil vit là-bas, pas dans l'entrée de la rubrique. */
	.intro-texte p.renvoi {
		margin: 0;
		font-family: var(--police-ui);
		font-size: var(--taille-s);
	}

	.intro-texte p.renvoi a {
		color: var(--accent-cobalt);
		text-decoration: none;
		border-bottom: 1px solid transparent;
	}

	.intro-texte p.renvoi a:hover,
	.intro-texte p.renvoi a:focus-visible {
		border-bottom-color: var(--accent-cobalt);
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

	/* Onglet Profil seulement (2026-07-20) : la légende est passée au flanc du graphe,
	   la zone doit donc porter les deux colonnes. Le graphe garde sa proportion (≈ 70 %)
	   au lieu de rétrécir dans les 42 rem. Œuvres et Musées gardent leur largeur. */
	.vue-profil {
		max-width: 60rem;
	}
</style>
