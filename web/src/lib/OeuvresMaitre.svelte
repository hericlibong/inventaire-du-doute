<script>
	import { tick } from 'svelte';
	import { base } from '$app/paths';
	import { lienPop } from '$lib/joconde.js';
	import { FAMILLE_PUBLIC, ORDRE_FAMILLES, notices } from '$lib/familles-public.js';
	import { fenetrePagination } from '$lib/pagination.js';

	// Onglet « Œuvres » (refonte 2026-07-28) : la TOTALITÉ des œuvres concernées
	// par le maître, pas quelques exemples. Le fichier oeuvres/<slug>.json est
	// chargé à la demande (jamais celui des autres maîtres), filtrable par mention
	// et paginé. Chaque entrée montre les MOTS EXACTS publiés par le musée — le
	// verbatim est la seule citation littérale de l'application — et un lien POP.
	//
	// La composition éditoriale est celle de la direction B (entrées séparées par
	// des filets, pas une grille de cartes ; un emplacement média réservé, jamais
	// d'image inventée). Le front ne re-classe ni ne re-parse rien : la famille
	// (`code`) et l'extrait viennent tels quels de l'export (decisions.md 2026-07-28).
	let { maitre } = $props();

	const PAR_PAGE = 8;

	let statut = $state('chargement'); // 'chargement' | 'ok' | 'erreur'
	let fichier = $state(null); // contenu de oeuvres/<slug>.json
	let familleActive = $state(null); // null = « Toutes »
	let page = $state(1);
	let jeton = 0; // anti-course : seule la dernière requête lancée fait foi
	let hautListe; // ancre de recentrage après un changement de page/filtre

	// Rang d'une famille dans l'ordre public (axe du graphique) : sert au tri des
	// puces ET des œuvres. Un code inconnu (jamais produit aujourd'hui) va en fin.
	const rang = (code) => {
		const i = ORDRE_FAMILLES.indexOf(code);
		return i === -1 ? ORDRE_FAMILLES.length : i;
	};
	const fam = (code) => FAMILLE_PUBLIC[code] ?? { header: '', couleur: 'var(--couleur-copie)' };

	function charger(slug) {
		const monJeton = ++jeton;
		statut = 'chargement';
		fichier = null;
		fetch(`${base}/data/oeuvres/${slug}.json`)
			.then((r) => {
				if (!r.ok) throw new Error(String(r.status));
				return r.json();
			})
			.then((json) => {
				if (monJeton === jeton) {
					fichier = json;
					statut = 'ok';
				}
			})
			.catch(() => {
				if (monJeton === jeton) statut = 'erreur';
			});
	}

	// Changement d'artiste : on repart de zéro (filtre + page) et on recharge.
	$effect(() => {
		const slug = maitre.slug;
		familleActive = null;
		page = 1;
		charger(slug);
	});

	// Œuvres dans l'ordre public des mentions (tri stable : l'ordre de rencontre
	// est conservé au sein d'une même famille).
	const oeuvres = $derived(
		[...(fichier?.oeuvres ?? [])].sort((a, b) => rang(a.code) - rang(b.code))
	);

	// Puces de filtre : « Toutes » puis les familles PRÉSENTES, ordre public,
	// avec leur effectif. Les familles absentes ne paraissent pas.
	const puces = $derived([
		{ code: null, label: 'Toutes', n: maitre.doute },
		...(fichier?.familles ?? [])
			.filter((f) => FAMILLE_PUBLIC[f.code])
			.sort((a, b) => rang(a.code) - rang(b.code))
			.map((f) => ({ code: f.code, label: fam(f.code).header, n: f.notices }))
	]);

	const oeuvresFiltrees = $derived(
		familleActive ? oeuvres.filter((o) => o.code === familleActive) : oeuvres
	);
	const nbFiltre = $derived(oeuvresFiltrees.length);
	const nbPages = $derived(Math.max(1, Math.ceil(nbFiltre / PAR_PAGE)));
	// Bornes de la tranche affichée (la page est déjà remise à 1 aux changements).
	const debut = $derived((page - 1) * PAR_PAGE);
	const pageOeuvres = $derived(oeuvresFiltrees.slice(debut, debut + PAR_PAGE));
	const premier = $derived(nbFiltre === 0 ? 0 : debut + 1);
	const dernier = $derived(Math.min(debut + PAR_PAGE, nbFiltre));
	const fenetre = $derived(fenetrePagination(page, nbPages));

	// Recentre la lecture au début de la liste, sans à-coup, et y place le focus
	// (l'annonce du changement pour les lecteurs d'écran passe par ce déplacement).
	async function versHautListe() {
		await tick();
		hautListe?.scrollIntoView({ behavior: 'smooth', block: 'start' });
		hautListe?.focus({ preventScroll: true });
	}

	function choisirFamille(code) {
		if (familleActive === code) return;
		familleActive = code;
		page = 1;
		versHautListe();
	}

	function allerPage(p) {
		if (p < 1 || p > nbPages || p === page) return;
		page = p;
		versHautListe();
	}

	// « musée, ville » en gérant les champs manquants de la base.
	const lieu = (o) => [o.musee, o.ville].filter(Boolean).join(', ');
</script>

<section class="vitrine">
	<header class="tete">
		<h3>Œuvres concernées</h3>
		<p class="total">
			<strong>{maitre.doute}</strong>
			œuvre{maitre.doute === 1 ? '' : 's'} portent une mention prudente pour ce nom.
		</p>
	</header>

	{#if statut === 'chargement'}
		<p class="etat" role="status">Chargement des œuvres…</p>
	{:else if statut === 'erreur'}
		<p class="etat erreur" role="alert">
			Les œuvres n'ont pas pu être chargées.
			<button type="button" class="reessayer" onclick={() => charger(maitre.slug)}>
				Réessayer
			</button>
		</p>
	{:else}
		<!-- Filtres : « Toutes » + une puce par mention présente, ordre public. -->
		<div class="filtres" role="group" aria-label="Filtrer par mention">
			{#each puces as p (p.code ?? 'toutes')}
				<button
					type="button"
					class="puce"
					class:actif={familleActive === p.code}
					aria-pressed={familleActive === p.code}
					onclick={() => choisirFamille(p.code)}
				>
					{#if p.code}<span class="pastille" style="background: {fam(p.code).couleur}"></span>{/if}
					<span class="puce-label">{p.label}</span>
					<span class="puce-n">{p.n}</span>
				</button>
			{/each}
		</div>

		<!-- Ancre de recentrage + décompte de la tranche affichée. -->
		<p class="decompte" bind:this={hautListe} tabindex="-1">
			{#if nbFiltre === 0}
				Aucune œuvre pour cette mention.
			{:else}
				Œuvres <strong>{premier}</strong> à <strong>{dernier}</strong> sur <strong>{nbFiltre}</strong>
			{/if}
		</p>

		{#if nbFiltre === 0}
			<p class="etat vide">Aucune œuvre ne correspond au filtre choisi.</p>
		{:else}
			<ol class="entrees">
				{#each pageOeuvres as o (o.reference)}
					<li class="entree">
						{#if o.image}
							<!-- Reproduction ouverte (Wikimedia Commons), copie locale ; l'image
							     ouvre la page source où figurent licence et crédit. Légende
							     normée en petit corps : source + licence (+ auteur si requis). -->
							<figure class="media media-image">
								<a href={o.image.source} target="_blank" rel="noopener" title="Voir le fichier sur Wikimedia Commons">
									<img src="{base}/{o.image.url}" alt="Reproduction : {o.titre ?? 'œuvre'}" loading="lazy" />
								</a>
								<figcaption class="credit">
									{#if o.image.creator && o.image.licence.startsWith('CC BY')}<span class="credit-auteur" title={o.image.creator}>{o.image.creator}</span>{/if}
									<a href={o.image.licence_url || o.image.source} target="_blank" rel="noopener">{o.image.licence}</a>
									· <a href={o.image.source} target="_blank" rel="noopener">Wikimedia&nbsp;Commons</a>
								</figcaption>
							</figure>
						{:else}
							<!-- Pas de reproduction réutilisable connue : placeholder assumé,
							     jamais une image inventée. -->
							<div class="media" aria-hidden="true">
								<span>reproduction<br />non affichée</span>
							</div>
						{/if}
						<div class="corps">
							<p class="kicker">
								<span class="pastille" style="background: {fam(o.code).couleur}"></span>{fam(o.code).header}
							</p>
							<h4 class="titre">{o.titre ?? 'Sans titre'}</h4>
							{#if lieu(o)}<p class="lieu">{lieu(o)}</p>{/if}
							<p class="verbatim" style="border-left-color: {fam(o.code).couleur}">«&nbsp;{o.extrait}&nbsp;»</p>
							<a class="lien-fiche" href={lienPop(o.reference)} target="_blank" rel="noopener">
								Voir la fiche publique sur POP&nbsp;→
							</a>
						</div>
					</li>
				{/each}
			</ol>

			{#if nbPages > 1}
				<nav class="pagination" aria-label="Pages d'œuvres">
					<button
						type="button"
						class="nav-bord"
						onclick={() => allerPage(page - 1)}
						disabled={page === 1}
					>
						‹&nbsp;Précédente
					</button>
					<ul class="pages">
						{#each fenetre as item, i (item === '…' ? `e${i}` : item)}
							<li>
								{#if item === '…'}
									<span class="ellipse" aria-hidden="true">…</span>
								{:else}
									<button
										type="button"
										class="page-num"
										class:actif={item === page}
										aria-current={item === page ? 'page' : undefined}
										aria-label="Page {item}"
										onclick={() => allerPage(item)}
									>
										{item}
									</button>
								{/if}
							</li>
						{/each}
					</ul>
					<button
						type="button"
						class="nav-bord"
						onclick={() => allerPage(page + 1)}
						disabled={page === nbPages}
					>
						Suivante&nbsp;›
					</button>
				</nav>
			{/if}
		{/if}
	{/if}

	<!-- Copies « d'après », à part : des copies assumées, pas des doutes. Hors gamme
	     du doute (couleur neutre), jamais mêlées aux entrées. -->
	<div class="bande-copie">
		<p class="copie-texte">
			À part&nbsp;: <strong>{notices(maitre.copie)}</strong>
			porte{maitre.copie === 1 ? '' : 'nt'} la mention «&nbsp;d'après
			{maitre.nom}&nbsp;» — des copies assumées, pas des attributions incertaines.
		</p>
		{#if maitre.exemple_copie}
			<p class="copie-exemple">
				Par exemple&nbsp;: {maitre.exemple_copie.titre ?? 'Sans titre'}
				{#if lieu(maitre.exemple_copie)}({lieu(maitre.exemple_copie)}){/if}
				— «&nbsp;{maitre.exemple_copie.extrait}&nbsp;» ·
				<a href={lienPop(maitre.exemple_copie.reference)} target="_blank" rel="noopener">fiche publique</a>
			</p>
		{/if}
	</div>

	<!-- Mention technique, petit corps, écrite une seule fois. -->
	<p class="mention-pop">
		Les liens ouvrent les fiches publiques sur POP, la plateforme ouverte du patrimoine.
	</p>
</section>

<style>
	.tete {
		margin: 0 0 var(--espace-4);
	}

	.vitrine h3 {
		font-family: var(--police-titre);
		margin: 0 0 0.15rem;
		font-size: var(--taille-l);
	}

	.total {
		margin: 0;
		color: var(--couleur-encre-douce);
		font-size: var(--taille-s);
	}

	/* --- États (chargement, erreur, vide) : mêmes marges, ton mesuré. --- */
	.etat {
		margin: var(--espace-4) 0;
		font-size: var(--taille-s);
		color: var(--couleur-encre-douce);
	}

	.etat.erreur {
		color: var(--couleur-encre);
	}

	.reessayer {
		margin-left: var(--espace-3);
		font-family: var(--police-ui);
		font-size: var(--taille-xs);
		background: none;
		border: var(--filet);
		border-radius: 2px;
		padding: 0.1rem 0.5rem;
		cursor: pointer;
		color: var(--accent-cobalt);
	}

	.reessayer:hover {
		border-color: var(--accent-cobalt);
	}

	/* --- Filtres : puces cliquables, la mention active tient par la forme ET la
	   couleur (bordure épaisse + gras), jamais par la seule couleur. --- */
	.filtres {
		display: flex;
		flex-wrap: wrap;
		gap: var(--espace-3);
		margin: 0 0 var(--espace-4);
	}

	.puce {
		display: inline-flex;
		align-items: center;
		gap: 0.4rem;
		padding: 0.28rem 0.6rem;
		font-family: var(--police-ui);
		font-size: var(--taille-xs);
		background: var(--surface-carte);
		border: 1px solid var(--couleur-trait);
		border-radius: 999px;
		cursor: pointer;
		color: var(--couleur-encre);
	}

	.puce:hover {
		border-color: var(--couleur-encre-douce);
	}

	.puce.actif {
		border-color: var(--accent-cobalt);
		border-width: 2px;
		padding: calc(0.28rem - 1px) calc(0.6rem - 1px); /* compense la bordure */
		font-weight: 700;
	}

	.puce:focus-visible {
		outline: var(--focus-anneau);
		outline-offset: 2px;
	}

	.puce-n {
		font-variant-numeric: tabular-nums;
		color: var(--couleur-encre-douce);
	}

	.puce.actif .puce-n {
		color: inherit;
	}

	.pastille {
		width: 0.6rem;
		height: 0.6rem;
		border-radius: 50%;
		flex: none;
	}

	/* Décompte de tranche : sert aussi d'ancre de recentrage (tabindex=-1). */
	.decompte {
		margin: 0 0 var(--espace-3);
		font-family: var(--police-ui);
		font-size: var(--taille-xs);
		letter-spacing: 0.04em;
		text-transform: uppercase;
		color: var(--couleur-encre-douce);
	}

	.decompte:focus-visible {
		outline: var(--focus-anneau);
		outline-offset: 3px;
	}

	.etat.vide {
		font-style: italic;
	}

	/* Liste continue : entrées séparées par un filet, pas des cartes détachées. */
	.entrees {
		list-style: none;
		margin: 0;
		padding: 0;
	}

	.entree {
		display: grid;
		grid-template-columns: 7rem 1fr;
		gap: var(--espace-5);
		padding: var(--espace-4) 0;
		border-top: var(--filet);
	}

	/* Emplacement média réservé : cadre neutre, pas une image. */
	.media {
		aspect-ratio: 4 / 5;
		background: var(--surface-carte);
		border: var(--filet);
		display: flex;
		align-items: center;
		justify-content: center;
		text-align: center;
	}

	.media span {
		font-family: var(--police-ui);
		font-size: 0.62rem;
		letter-spacing: 0.05em;
		text-transform: uppercase;
		line-height: 1.35;
		color: var(--couleur-trait);
	}

	/* Reproduction réelle : l'image remplit la colonne média, la légende (source +
	   licence) tient dessous en petit corps normé. */
	.media-image {
		margin: 0;
		min-width: 0;
	}

	.media-image a {
		display: block;
	}

	.media-image img {
		display: block;
		width: 100%;
		height: auto;
		border: var(--filet);
		background: var(--surface-carte);
	}

	.credit {
		margin-top: 0.3rem;
		font-family: var(--police-ui);
		font-size: 0.6rem;
		line-height: 1.35;
		color: var(--couleur-encre-douce);
	}

	.credit a {
		color: inherit;
		text-decoration: underline;
	}

	.credit a:hover {
		color: var(--accent-cobalt);
	}

	/* Auteur exigé par la licence (CC BY/BY-SA) : borné pour ne pas déborder. */
	.credit-auteur {
		display: block;
		max-width: 100%;
		overflow: hidden;
		text-overflow: ellipsis;
		white-space: nowrap;
	}

	.corps {
		min-width: 0;
	}

	/* Kicker = le même mot et la même couleur que le point du graphique. */
	.kicker {
		margin: 0 0 0.2rem;
		font-family: var(--police-ui);
		font-size: var(--taille-xs);
		font-weight: 600;
		letter-spacing: 0.08em;
		text-transform: uppercase;
		color: var(--couleur-encre-douce);
		display: flex;
		align-items: center;
		gap: 0.4rem;
	}

	/* Titre de l'œuvre : repère, sous le verbatim dans la hiérarchie. Souvent en
	   capitales dans la base — corps modéré pour qu'il ne crie pas. */
	.titre {
		margin: 0;
		font-family: var(--police-texte);
		font-weight: 600;
		font-size: 1rem;
		line-height: 1.3;
	}

	.lieu {
		margin: 0.1rem 0 0;
		font-size: var(--taille-s);
		color: var(--couleur-encre-douce);
	}

	/* Le verbatim est la MATIÈRE : les mots exacts du musée, en tête de hiérarchie,
	   avec le liseré de couleur de la mention. */
	.verbatim {
		margin: var(--espace-3) 0 var(--espace-3);
		padding-left: var(--espace-3);
		border-left: 3px solid var(--couleur-trait);
		font-family: var(--police-titre);
		font-size: 1.3rem;
		line-height: 1.3;
	}

	.lien-fiche {
		font-family: var(--police-ui);
		font-size: var(--taille-s);
		color: var(--accent-cobalt);
		text-decoration: none;
		border-bottom: 1px solid transparent;
	}

	.lien-fiche:hover {
		border-bottom-color: var(--accent-cobalt);
	}

	/* --- Pagination : bornes + fenêtre compacte, page active repérable sans la
	   seule couleur (gras + soulignement + aria-current). --- */
	.pagination {
		display: flex;
		flex-wrap: wrap;
		align-items: center;
		gap: var(--espace-3);
		margin-top: var(--espace-5);
		padding-top: var(--espace-4);
		border-top: var(--filet);
	}

	.pages {
		list-style: none;
		display: flex;
		align-items: center;
		gap: 0.15rem;
		margin: 0;
		padding: 0;
	}

	.nav-bord,
	.page-num {
		font-family: var(--police-ui);
		font-size: var(--taille-s);
		background: none;
		border: 1px solid transparent;
		border-radius: 2px;
		padding: 0.2rem 0.5rem;
		cursor: pointer;
		color: var(--couleur-encre);
	}

	.nav-bord {
		color: var(--accent-cobalt);
	}

	.nav-bord:disabled {
		color: var(--couleur-trait);
		cursor: default;
	}

	.page-num:hover:not(.actif),
	.nav-bord:hover:not(:disabled) {
		border-color: var(--couleur-trait);
	}

	.page-num.actif {
		font-weight: 700;
		color: var(--accent-cobalt);
		border-bottom: 2px solid var(--accent-cobalt);
		border-radius: 0;
	}

	.nav-bord:focus-visible,
	.page-num:focus-visible {
		outline: var(--focus-anneau);
		outline-offset: 2px;
	}

	.ellipse {
		padding: 0 0.2rem;
		color: var(--couleur-encre-douce);
	}

	/* Copies « d'après » : bloc distinct, couleur neutre, filet à gauche. */
	.bande-copie {
		margin-top: var(--espace-5);
		padding-left: var(--espace-4);
		border-left: 3px solid var(--couleur-copie);
	}

	.copie-texte {
		margin: 0;
		font-size: var(--taille-base);
	}

	.copie-exemple {
		margin: 0.4rem 0 0;
		font-size: var(--taille-s);
		color: var(--couleur-encre-douce);
	}

	.copie-exemple a {
		color: inherit;
	}

	.mention-pop {
		margin: var(--espace-5) 0 0;
		font-size: var(--taille-xs);
		color: var(--couleur-encre-douce);
	}

	@media (max-width: 560px) {
		.entree {
			grid-template-columns: 5rem 1fr;
			gap: var(--espace-4);
		}
		.verbatim {
			font-size: 1.15rem;
		}
	}
</style>
