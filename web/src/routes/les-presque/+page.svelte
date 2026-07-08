<script>
	import BarreNiveaux from '$lib/BarreNiveaux.svelte';
	import NuageFamilles from '$lib/NuageFamilles.svelte';
	import { lienPop, nombre } from '$lib/joconde.js';
	// Archive : la piste « galaxie » est conservée dans $lib/GalaxieMaitre.svelte
	// (abandonnée dans cette vue, decisions.md 2026-07-08), non importée ici.

	let { data } = $props();
	const meta = data.artistes;
	const artistes = data.artistes.artistes;

	// Plafond COMMUN de l'axe Y du nuage : la plus grande valeur de famille sur
	// tous les maîtres (≈ 240, « école de » Le Brun). Calculé ici, pas en dur.
	const plafond = Math.max(
		...artistes.flatMap((a) => a.familles.map((f) => f.notices))
	);

	// Deux regards sur la même donnée : le nuage (le combien) ou le détail (le quoi).
	let vue = $state('nuage');

	// Recherche/filtre sur les maîtres vedettes (moteur sur toute la base = plus
	// tard, dépend d'un export de tous les noms — voir roadmap P3-T1).
	let recherche = $state('');
	const liste = $derived(
		artistes.filter((a) => a.nom.toLowerCase().includes(recherche.trim().toLowerCase()))
	);

	// Maître sélectionné pour la fiche (le plus douté par défaut).
	let selection = $state(artistes[0].nom);
	const maitre = $derived(artistes.find((a) => a.nom === selection));

	// Total d'attributions rattachées au nom (ferme + doute), pour situer le doute.
	const totalNom = (a) => a.propre + a.doute;
	const partDoute = (a) => (totalNom(a) ? (a.doute / totalNom(a)) * 100 : 0);
</script>

<h1>Les presque</h1>
<p class="chapo">
	Quand un musée n'est pas sûr qu'une œuvre soit d'un grand maître, il ne le cache
	pas : il l'écrit. « Attribué à Rembrandt », « école de Poussin », « atelier de
	Rubens », « Titien&nbsp;? »… Cette page rassemble, pour une trentaine de maîtres
	célèbres, <strong>toutes les œuvres que les musées de France ne leur attribuent
	pas tout à fait</strong>.
</p>
<p class="mode-emploi">
	👉 Choisissez un maître dans la liste. Le nuage montre <strong>quelles
	formules</strong> les musées emploient et <strong>en quelle quantité</strong>,
	sur une <strong>échelle commune à tous</strong> — plus un point est haut, plus
	ce type de doute est fréquent. Ni révélation ni trésor caché : seulement ce que
	les musées écrivent eux-mêmes.
</p>
<p class="critere">Les {artistes.length} maîtres retenus : {meta.critere}.</p>

<div class="grille">
	<aside class="colonne-liste">
		<label class="recherche">
			<span class="visuellement-cache">Filtrer les maîtres</span>
			<input type="search" placeholder="Filtrer un nom…" bind:value={recherche} />
		</label>
		<ul class="maitres">
			{#each liste as a (a.nom)}
				<li>
					<button
						class="maitre"
						class:actif={a.nom === selection}
						onclick={() => (selection = a.nom)}
					>
						<span class="nom">{a.nom}</span>
						<span class="compte">{nombre(a.doute)}</span>
						<BarreNiveaux niveaux={a.niveaux} hauteur="0.35rem" />
					</button>
				</li>
			{:else}
				<li class="vide">Aucun maître ne correspond.</li>
			{/each}
		</ul>
	</aside>

	{#if maitre}
		<section class="fiche">
			<header>
				<h2>{maitre.nom}</h2>
				<p class="resume">
					<strong>{nombre(maitre.doute)}</strong> notices de doute sur
					{nombre(totalNom(maitre))} attributions à ce nom
					({partDoute(maitre).toFixed(0)} %), dans {maitre.musees} musées.
				</p>
				<div class="bascule" role="tablist" aria-label="Choisir la vue">
					<button role="tab" aria-selected={vue === 'nuage'} class:actif={vue === 'nuage'} onclick={() => (vue = 'nuage')}>
						Nuage
					</button>
					<button role="tab" aria-selected={vue === 'fiche'} class:actif={vue === 'fiche'} onclick={() => (vue = 'fiche')}>
						Détail
					</button>
				</div>
			</header>

			{#if vue === 'nuage'}
				<NuageFamilles {maitre} {plafond} />
			{:else}
			<h3>L'échelle du doute</h3>
			<BarreNiveaux niveaux={maitre.niveaux} hauteur="1.1rem" etiquettes={true} />

			<h3>Les formules employées</h3>
			<table class="familles">
				<thead>
					<tr><th>Formule</th><th>Niveau</th><th class="num">Notices</th></tr>
				</thead>
				<tbody>
					{#each maitre.familles as f (f.code)}
						<tr>
							<td>{f.libelle}</td>
							<td>{f.niveau}</td>
							<td class="num">{nombre(f.notices)}</td>
						</tr>
					{/each}
				</tbody>
			</table>

			<div class="bande-copie">
				<strong>{nombre(maitre.copie)}</strong> notices « d'après {maitre.nom} »
				— des <em>copies assumées</em>, comptées à part : ce ne sont pas des doutes.
			</div>

			<h3>Quelques notices réelles</h3>
			<ul class="exemples">
				{#each maitre.exemples as ex (ex.reference)}
					<li>
						<a href={lienPop(ex.reference)} target="_blank" rel="noopener">{ex.titre}</a>
						<span class="ex-meta">{ex.musee}, {ex.ville}</span>
						<span class="ex-extrait">« {ex.extrait} »</span>
					</li>
				{/each}
			</ul>
			{/if}
		</section>
	{/if}
</div>

<style>
	.chapo {
		font-size: 1.15rem;
		max-width: 44rem;
	}

	.mode-emploi {
		max-width: 44rem;
		padding: 0.6rem 0.9rem;
		background: rgba(122, 74, 43, 0.06);
		border-radius: 4px;
	}

	.critere {
		font-size: 0.85rem;
		color: var(--couleur-encre-douce);
		font-style: italic;
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

	.maitre {
		width: 100%;
		text-align: left;
		background: none;
		border: none;
		border-bottom: 1px solid var(--couleur-trait);
		padding: 0.5rem 0.25rem;
		cursor: pointer;
		display: grid;
		grid-template-columns: 1fr auto;
		gap: 0.15rem 0.5rem;
		font: inherit;
	}

	.maitre :global(.barre) {
		grid-column: 1 / -1;
		margin-top: 0.25rem;
	}

	.maitre:hover {
		background: rgba(122, 74, 43, 0.06);
	}

	.maitre.actif {
		background: rgba(184, 85, 31, 0.1);
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

	.fiche h2 {
		font-family: var(--police-titre);
		margin: 0;
	}

	.fiche h3 {
		margin: 1.75rem 0 0.5rem;
		font-size: 1.05rem;
	}

	.resume {
		margin: 0.25rem 0 0;
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

	.familles {
		width: 100%;
		border-collapse: collapse;
		font-size: 0.95rem;
	}

	.familles th,
	.familles td {
		text-align: left;
		padding: 0.35rem 0.5rem;
		border-bottom: 1px solid var(--couleur-trait);
	}

	.familles .num {
		text-align: right;
		font-variant-numeric: tabular-nums;
	}

	.bande-copie {
		margin-top: 1.25rem;
		padding: 0.75rem 1rem;
		border-left: 4px solid var(--couleur-copie);
		background: rgba(74, 107, 122, 0.07);
		font-size: 0.95rem;
	}

	.exemples {
		list-style: none;
		margin: 0.5rem 0 0;
		padding: 0;
		display: flex;
		flex-direction: column;
		gap: 0.75rem;
	}

	.exemples li {
		display: flex;
		flex-direction: column;
	}

	.exemples a {
		color: var(--couleur-accent);
		font-weight: 600;
	}

	.ex-meta,
	.ex-extrait {
		font-size: 0.85rem;
		color: var(--couleur-encre-douce);
	}
</style>
