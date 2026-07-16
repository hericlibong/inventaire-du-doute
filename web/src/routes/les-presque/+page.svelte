<script>
	import BarreFamilles from '$lib/BarreFamilles.svelte';
	import NuageFamilles from '$lib/NuageFamilles.svelte';
	import OeuvresMaitre from '$lib/OeuvresMaitre.svelte';
	import CarteMaitre from '$lib/CarteMaitre.svelte';
	import LegendeFamilles from '$lib/LegendeFamilles.svelte';
	import PortraitMaitre from '$lib/PortraitMaitre.svelte';
	import { nombre, deNom, musees } from '$lib/joconde.js';
	import { oeuvres } from '$lib/familles-public.js';
	import { bioMaitre } from '$lib/editorial-maitres.js';
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

	// Deux regards sur la même donnée : le graphique (les formes et volumes du
	// doute) ou les œuvres (les cas concrets, avec les mots publiés).
	let vue = $state('graphique');

	// Recherche/filtre sur les maîtres vedettes (moteur sur toute la base = plus
	// tard, dépend d'un export de tous les noms — voir roadmap P3-T1).
	let recherche = $state('');
	const liste = $derived(
		artistes.filter((a) => a.nom.toLowerCase().includes(recherche.trim().toLowerCase()))
	);

	// Maître sélectionné pour la fiche (le plus douté par défaut).
	let selection = $state(artistes[0].nom);
	const maitre = $derived(artistes.find((a) => a.nom === selection));

	// Total d'attributions rattachées au nom (ferme + doute), pour situer le volume.
	const totalNom = (a) => a.propre + a.doute;
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
	<aside class="colonne-liste">
		<label class="recherche">
			<span class="visuellement-cache">Filtrer les maîtres</span>
			<input type="search" placeholder="Filtrer un nom…" bind:value={recherche} />
		</label>
		<ul class="maitres">
			{#each liste as a (a.nom)}
				<!-- La jauge vit HORS du bouton : ses segments sont focusables
				     (infobulle au survol/focus), or un élément interactif ne peut
				     pas être imbriqué dans un <button> (2026-07-12). -->
				<li class="rang" class:actif={a.nom === selection}>
					<button class="maitre" onclick={() => (selection = a.nom)}>
						<span class="nom">{a.nom}</span>
						<span class="compte">{nombre(a.doute)}</span>
					</button>
					<BarreFamilles familles={a.familles} total={a.doute} nom={a.nom} hauteur="0.35rem" />
				</li>
			{:else}
				<li class="vide">Aucun maître ne correspond.</li>
			{/each}
		</ul>
		<!-- Clé des couleurs, commune aux trois vues : sous la liste, hors de la
		     zone d'onglet (décision 2026-07-13). La liste scrolle dans son cadre,
		     la légende reste visible. -->
		<LegendeFamilles />
	</aside>

	{#if maitre}
		<section class="fiche">
			<header>
				<!-- Bloc profil : nom pleine largeur, puis portrait à GAUCHE + texte à
				     DROITE (décision 2026-07-11, 2e disposition). Le profil est HORS de la
				     zone d'onglet → portrait visible en Graphique comme en Détail, sans
				     duplication ni saut au changement. -->
				<h2>{maitre.nom}</h2>
				<div class="profil">
					<div class="profil-portrait">
						<PortraitMaitre {maitre} portrait={portraits[maitre.nom]} />
					</div>
					<div class="profil-texte">
						{#if bioMaitre(maitre.nom)}
							<p class="bio">{bioMaitre(maitre.nom)}</p>
						{/if}
						<!-- Deux blocs empilés où le CHIFFRE porte l'appui visuel (volume, puis
						     dispersion) : la colonne pèse assez pour répondre au portrait, on
						     obtient un vrai bloc de profil (décision 2026-07-11, disposition B).
						     Le chiffre reste un repère de profil, pas la mesure — la vraie
						     mesure est dans le graphe. -->
						<p class="situation">
							<span class="chiffre">{oeuvres(totalNom(maitre))}</span>
							sous le nom {deNom(maitre.nom)}.
						</p>
						<p class="situation">
							<span class="chiffre">{musees(maitre.musees)}</span>
							où ces œuvres sont conservées.
						</p>
					</div>
				</div>

				<div class="bascule" role="tablist" aria-label="Choisir la vue">
					<button role="tab" aria-selected={vue === 'graphique'} class:actif={vue === 'graphique'} onclick={() => (vue = 'graphique')}>
						Graphique
					</button>
					<button role="tab" aria-selected={vue === 'oeuvres'} class:actif={vue === 'oeuvres'} onclick={() => (vue = 'oeuvres')}>
						Œuvres
					</button>
					<button role="tab" aria-selected={vue === 'carte'} class:actif={vue === 'carte'} onclick={() => (vue = 'carte')}>
						Carte
					</button>
				</div>
			</header>

			{#if vue === 'graphique'}
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

	.recherche input {
		width: 100%;
		box-sizing: border-box;
		padding: 0.5rem 0.6rem;
		border: 1px solid var(--couleur-trait);
		border-radius: 3px;
		font: inherit;
		background: #fff;
	}

	.visuellement-cache {
		position: absolute;
		width: 1px;
		height: 1px;
		overflow: hidden;
		clip: rect(0 0 0 0);
	}

	.maitres {
		list-style: none;
		margin: 0.75rem 0 0;
		padding: 0;
		max-height: 32rem;
		overflow-y: auto;
	}

	/* La ligne (li) porte l'état (bordure, survol, sélection) ; le bouton ne
	   couvre que nom + compte, la jauge est sa sœur (segments focusables —
	   interdits à l'intérieur d'un <button>). */
	.rang {
		border-bottom: 1px solid var(--couleur-trait);
		padding: 0.5rem 0.25rem 0.6rem;
	}

	.rang:hover {
		background: rgba(122, 74, 43, 0.06);
	}

	.rang.actif {
		background: rgba(184, 85, 31, 0.1);
	}

	.maitre {
		width: 100%;
		text-align: left;
		background: none;
		border: none;
		padding: 0;
		cursor: pointer;
		display: grid;
		grid-template-columns: 1fr auto;
		gap: 0.15rem 0.5rem;
		font: inherit;
	}

	.rang :global(.barre) {
		margin-top: 0.35rem;
	}

	.maitre .nom {
		font-weight: 600;
	}

	.maitre .compte {
		color: var(--niveau-1);
		font-variant-numeric: tabular-nums;
	}

	.vide {
		color: var(--couleur-encre-douce);
		padding: 0.5rem 0;
	}

	.fiche {
		/* conteneur de requête : le portrait passe sous le texte selon la largeur
		   RÉELLE de la fiche (pas celle de l'écran), donc « plus tôt » quand l'aside
		   comprime la colonne (décision 2026-07-11). */
		container-type: inline-size;
	}

	/* Bloc profil : portrait (largeur bornée) à gauche, texte (largeur souple) à
	   droite, centrés l'un par rapport à l'autre → bloc compact, pas de portrait
	   qui flotte seul. */
	.profil {
		display: grid;
		/* colonne texte bornée : elle « répond » au portrait, elle ne s'étale pas
		   comme une phrase de page. justify-content: start → le bloc reste à gauche. */
		grid-template-columns: 12rem minmax(0, 24rem);
		justify-content: start;
		gap: 1.75rem;
		align-items: start; /* texte calé en HAUT du portrait, pas centré */
		margin-top: 0.5rem;
	}

	.profil-portrait {
		width: 12rem;
		max-width: 100%;
	}

	/* Colonne de texte : blocs empilés, espacés, pour occuper la hauteur du portrait. */
	.profil-texte {
		display: flex;
		flex-direction: column;
		gap: 1.1rem;
	}

	.situation {
		margin: 0;
		font-size: 1.05rem;
		line-height: 1.55;
	}

	/* Le chiffre en point d'appui : gros, en couleur d'accent, sur sa propre ligne,
	   pour donner du poids à la colonne face au portrait. Repère de profil, pas la
	   mesure principale (celle-ci reste dans le graphe). */
	.chiffre {
		display: block;
		font-family: var(--police-titre);
		font-size: 1.5rem;
		font-weight: bold;
		color: var(--couleur-accent);
		line-height: 1.15;
	}

	/* Fiche étroite : une seule colonne — portrait puis texte, alignés à gauche
	   (pas deux colonnes écrasées). Le seuil porte sur la largeur RÉELLE de la
	   fiche, donc le passage se fait « plus tôt » quand l'aside comprime la colonne. */
	@container (max-width: 32rem) {
		.profil {
			grid-template-columns: 1fr;
			gap: 0.75rem;
		}
		.profil-portrait {
			justify-self: start;
		}
	}

	.fiche h2 {
		font-family: var(--police-titre);
		margin: 0;
	}

	.bio {
		margin: 0;
		color: var(--couleur-encre-douce);
		font-style: italic;
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
