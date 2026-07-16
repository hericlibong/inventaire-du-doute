<script>
	// Rubrique « Avant / après » — palier de réorganisation ÉDITORIALE (décision
	// 2026-07-14 quater) : mêmes éléments de fond qu'en V1, mais rangés en quatre
	// onglets pour une lecture guidée, sans refonte graphique ni images.
	//   En bref → Les chiffres → Les œuvres → Repères.
	// Titre + chapô PERMANENTS au-dessus des onglets ; chaque bloc dans son onglet.
	import CarteRevision from '$lib/CarteRevision.svelte';
	import AnneauRevisions from '$lib/AnneauRevisions.svelte';
	import { CATEGORIES, INVERSE } from '$lib/revisions-labels.js';
	import { nombre } from '$lib/joconde.js';

	let { data } = $props();
	const r = data.revisions;
	const t = r.totaux;

	// Valeurs du constat, calculées à partir des données (jamais codées en dur).
	const parCat = Object.fromEntries(r.passages.map((p) => [p.categorie, p.notices]));
	const pctFr = (n) =>
		((n / t.revisions) * 100).toLocaleString('fr-FR', {
			minimumFractionDigits: 1,
			maximumFractionDigits: 1
		});
	const constatNb = parCat.autre_nom;
	const constatPct = pctFr(constatNb);
	// Trajectoires « complexes » = les trois catégories hors galerie.
	const complexeNb = parCat.mineur + parCat.plusieurs_noms + parCat.deja_copie;
	const complexePct = pctFr(complexeNb);

	// --- Onglets ---
	const onglets = [
		{ code: 'bref', titre: 'En bref' },
		{ code: 'chiffres', titre: 'Les chiffres' },
		{ code: 'oeuvres', titre: 'Les œuvres' },
		{ code: 'reperes', titre: 'Repères' }
	];
	let onglet = $state('bref');

	// --- Carte emblématique de l'onglet « En bref » : la plus lisible du lot
	// (un grand nom qui s'efface). Puisée dans le même lot que la galerie. ---
	const exemple = r.cas.find((c) => c.reference === '000DE023181') ?? r.cas[0];

	// --- Galerie (onglet « Les œuvres ») : un seul groupe visible à la fois,
	// jamais les 32 d'un coup. Chips par type + un filtre transversal « inverse ».
	const ORDRE_GALERIE = ['autre_nom', 'anonyme', 'copie', 'meme_nom'];
	const groupes = ORDRE_GALERIE.map((code) => ({
		code,
		libelle: r.libelles_categorie[code],
		cartes: r.cas.filter((c) => c.categorie === code)
	})).filter((g) => g.cartes.length);
	const groupeInverse = {
		code: 'inverse',
		libelle: INVERSE.libelle,
		cartes: r.cas.filter((c) => c.inverse)
	};
	const chips = [...groupes, groupeInverse];

	let filtre = $state('autre_nom');
	const groupeVisible = $derived(chips.find((g) => g.code === filtre) ?? groupes[0]);
	// Le filtre transversal « inverse » puise dans une autre catégorie : ses
	// cartes reçoivent le libellé, le récit et la couleur de « inverse ».
	const estInverse = $derived(groupeVisible.code === 'inverse');
	const premiere = $derived(groupeVisible.cartes[0]);
	const reste = $derived(groupeVisible.cartes.slice(1));
	const introFiltre = $derived(
		estInverse ? INVERSE.introFiltre : (CATEGORIES[groupeVisible.code]?.introFiltre ?? '')
	);
</script>

<h1>Avant / après</h1>
<p class="chapo-permanent">
	Quand un musée révise l'attribution d'une œuvre, la notice Joconde en conserve
	parfois la trace. Cette rubrique observe les passages d'une formulation à une
	autre, sans décider laquelle constitue la bonne attribution.
</p>

<div class="onglets" role="tablist" aria-label="Sections de la rubrique">
	{#each onglets as o (o.code)}
		<button
			role="tab"
			aria-selected={onglet === o.code}
			class:actif={onglet === o.code}
			onclick={() => (onglet = o.code)}
		>
			{o.titre}
		</button>
	{/each}
</div>

{#if onglet === 'bref'}
	<div class="panneau" role="tabpanel" tabindex="0" aria-label="En bref">
		<p class="texte">
			Une attribution n'est pas gravée. En rapprochant une œuvre d'un catalogue,
			d'une archive ou d'un autre tableau, un musée peut réviser le nom qu'il lui
			associe. La base Joconde en garde souvent la trace&nbsp;: l'ancien nom d'un
			côté, celui retenu aujourd'hui de l'autre.
		</p>
		<p class="texte">
			Il ne s'agit pas d'erreurs corrigées&nbsp;: c'est le travail ordinaire des
			collections. Et le mouvement va dans les deux sens — il arrive qu'une œuvre
			longtemps restée anonyme retrouve un nom (c'est le cas de
			{nombre(t.direction_inverse)} notices).
		</p>

		<div class="exemple">
			<CarteRevision cas={exemple} />
		</div>
		<button class="lien-onglet" onclick={() => (onglet = 'oeuvres')}>
			Voir toutes les œuvres&nbsp;→
		</button>
	</div>
{:else if onglet === 'chiffres'}
	<div class="panneau" role="tabpanel" tabindex="0" aria-label="Les chiffres">
		<h2>Ce que deviennent les anciennes attributions</h2>
		<p class="texte">
			Sur {nombre(t.revisions)} notices qui conservent une ancienne attribution, le
			cas le plus fréquent est le remplacement d'un nom par un autre. Mais plus de la
			moitié du corpus suit une autre trajectoire&nbsp;: disparition du nom,
			reclassement comme copie, maintien avec réserve ou succession plus complexe
			d'attributions.
		</p>

		<div class="constat">
			<span class="constat-pct">{constatPct}&nbsp;%</span>
			<p class="constat-phrase">Dans près d'une notice sur deux, un nom en remplace un autre.</p>
			<p class="constat-detail">{nombre(constatNb)} notices sur {nombre(t.revisions)}</p>
		</div>

		<AnneauRevisions passages={r.passages} total={t.revisions} />

		<ul class="enseignements">
			<li>Près d'une notice sur deux associe aujourd'hui l'œuvre à un autre nom.</li>
			<li>Dans une notice sur huit, l'ancien nom n'est plus retenu.</li>
			<li>
				Plus d'un quart des notices suivent une trajectoire complexe ou composée de
				plusieurs étapes.
				<span class="ens-detail">({complexePct}&nbsp;%, soit {nombre(complexeNb)} notices)</span>
			</li>
		</ul>
	</div>
{:else if onglet === 'oeuvres'}
	<div class="panneau" role="tabpanel" tabindex="0" aria-label="Les œuvres">
		<h2>Les changements, œuvre par œuvre</h2>
		<p class="texte">
			Derrière chaque catégorie se trouvent des histoires particulières. Ces exemples
			permettent de lire les formulations conservées dans Joconde, entre attribution
			antérieure et attribution actuelle.
		</p>

		<div class="chips" role="group" aria-label="Filtrer par type de passage">
			{#each chips as g (g.code)}
				<button
					class:actif={filtre === g.code}
					aria-pressed={filtre === g.code}
					onclick={() => (filtre = g.code)}
				>
					{g.libelle} <span class="compte">· {g.cartes.length} exemples</span>
				</button>
			{/each}
		</div>

		{#if introFiltre}
			<p class="filtre-intro">{introFiltre}</p>
		{/if}

		{#if premiere}
			<div class="galerie-principale">
				<CarteRevision
					cas={premiere}
					variant="principale"
					libelle={estInverse ? INVERSE.libelle : null}
					recit={estInverse ? INVERSE.phraseCarte : null}
					couleur={estInverse ? INVERSE.couleur : null}
				/>
			</div>
		{/if}

		{#if reste.length}
			<div class="galerie-grille">
				{#each reste as cas (cas.reference)}
					<CarteRevision
						{cas}
						variant="secondaire"
						libelle={estInverse ? INVERSE.libelle : null}
						recit={estInverse ? INVERSE.phraseCarte : null}
						couleur={estInverse ? INVERSE.couleur : null}
					/>
				{/each}
			</div>
		{/if}
	</div>
{:else}
	<div class="panneau" role="tabpanel" tabindex="0" aria-label="Repères">
		<p class="texte">
			Ces chiffres ne portent que sur ce qui a été versé dans Joconde, où les
			musées contribuent de façon inégale.
		</p>
		<p class="texte">
			Les révisions sont très concentrées&nbsp;: le Louvre en réunit près de six
			sur dix, et les dessins près des deux tiers — l'effet des grands cabinets
			d'arts graphiques, pas un palmarès entre musées.
		</p>
		<p class="texte">
			Certaines notices, trop denses (plusieurs noms successifs) ou déjà des copies
			au départ, comptent dans les chiffres mais pas dans les cartes. Le détail
			sera exposé dans la page «&nbsp;Méthode et limites&nbsp;».
		</p>
	</div>
{/if}

<style>
	.chapo-permanent {
		font-size: 1.2rem;
		max-width: 44rem;
	}

	/* --- Barre d'onglets (même esprit que la bascule de « Les presque ») --- */
	.onglets {
		display: flex;
		flex-wrap: wrap;
		gap: 0.25rem;
		border-bottom: 1px solid var(--couleur-trait);
		margin: 1.5rem 0 0;
	}

	.onglets button {
		font: inherit;
		font-size: 1rem;
		padding: 0.5rem 1rem;
		border: none;
		background: none;
		color: var(--couleur-encre-douce);
		cursor: pointer;
		border-bottom: 2px solid transparent;
		margin-bottom: -1px;
	}

	.onglets button.actif {
		color: var(--couleur-encre);
		border-bottom-color: var(--couleur-revision);
		font-weight: 600;
	}

	.panneau {
		margin-top: 1.5rem;
	}

	.texte {
		max-width: 44rem;
		font-size: 1.05rem;
	}

	h2 {
		font-family: var(--police-titre);
		margin-bottom: 0.2rem;
	}

	/* --- Onglet En bref : carte emblématique + lien vers la galerie --- */
	.exemple {
		max-width: 24rem;
		margin: 1.5rem 0 1rem;
	}

	.lien-onglet {
		font: inherit;
		font-size: 0.95rem;
		background: none;
		border: none;
		padding: 0;
		color: var(--couleur-accent);
		cursor: pointer;
	}

	.lien-onglet:hover {
		text-decoration: underline;
	}

	/* --- Onglet Les chiffres : constat + enseignements --- */
	.constat {
		margin: 1.5rem 0 0.5rem;
		padding-left: 1rem;
		border-left: 3px solid var(--couleur-revision);
	}

	.constat-pct {
		font-family: var(--police-titre);
		font-size: 2.6rem;
		font-weight: 600;
		line-height: 1;
		color: var(--couleur-revision);
	}

	.constat-phrase {
		margin: 0.3rem 0 0;
		font-size: 1.15rem;
		max-width: 40rem;
	}

	.constat-detail {
		margin: 0.1rem 0 0;
		font-size: 0.9rem;
		color: var(--couleur-encre-douce);
	}

	.enseignements {
		list-style: none;
		margin: 2rem 0 0;
		padding: 0;
		display: grid;
		gap: 0.75rem;
		max-width: 44rem;
	}

	.enseignements li {
		padding-left: 1rem;
		border-left: 2px solid var(--couleur-trait);
		font-size: 1.02rem;
	}

	.ens-detail {
		color: var(--couleur-encre-douce);
		font-size: 0.9rem;
	}

	/* --- Galerie : chips + un seul groupe visible à la fois --- */
	.chips {
		display: flex;
		flex-wrap: wrap;
		gap: 0.5rem;
		margin: 1.25rem 0 1.5rem;
	}

	.chips button {
		font: inherit;
		font-size: 0.9rem;
		padding: 0.3rem 0.8rem;
		border: 1px solid var(--couleur-trait);
		border-radius: 999px;
		background: #fff;
		color: var(--couleur-encre);
		cursor: pointer;
	}

	.chips button.actif {
		background: var(--couleur-revision);
		border-color: var(--couleur-revision);
		color: #fff;
	}

	.chips .compte {
		opacity: 0.7;
		font-size: 0.85em;
	}

	.filtre-intro {
		max-width: 44rem;
		margin: 0 0 1.5rem;
		font-size: 1.02rem;
		color: var(--couleur-encre-douce);
	}

	.galerie-principale {
		margin-bottom: 1.25rem;
	}

	/* Grille des cartes secondaires : deux colonnes au plus (jamais trois),
	   pour laisser respirer les formulations longues. Une colonne sur mobile. */
	.galerie-grille {
		display: grid;
		grid-template-columns: repeat(2, 1fr);
		gap: 1rem;
	}

	@media (max-width: 640px) {
		.galerie-grille {
			grid-template-columns: 1fr;
		}
	}
</style>
