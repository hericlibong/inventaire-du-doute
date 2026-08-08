<script>
	import { tick } from 'svelte';
	import { base } from '$app/paths';
	import CreditImage from '$lib/CreditImage.svelte';
	import LightboxOeuvre from '$lib/LightboxOeuvre.svelte';
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
	// `museeActif` (code Muséofile, ou null) est PARTAGÉ avec la page : il survit
	// au changement d'onglet, et la carte du profil pourra le poser elle-même sans
	// qu'un second système de filtrage voie le jour (phase 3). L'onglet ne le remet
	// jamais à zéro tout seul — c'est la page qui le fait au changement d'artiste,
	// sinon un musée choisi sur la carte serait effacé à l'ouverture de l'onglet.
	let { maitre, museeActif = $bindable(null) } = $props();

	// Agrandissement d'une reproduction (2026-08-08). N'ouvre QUE des images déjà
	// retenues par le pipeline et déjà servies localement : la lightbox agrandit ce
	// que la vignette montre, elle ne va rien chercher ailleurs.
	// `ouvreurAgrandi` retient la vignette d'où l'on vient, pour lui rendre le focus
	// à la fermeture — sans quoi le clavier repartirait du haut de la page.
	let agrandie = $state(null);
	let ouvreurAgrandi = null;

	function agrandir(o, event) {
		ouvreurAgrandi = event?.currentTarget ?? null;
		agrandie = o;
	}

	function refermerAgrandie() {
		agrandie = null;
		ouvreurAgrandi?.focus();
		ouvreurAgrandi = null;
	}

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

	// Ordre d'affichage : les œuvres AVEC reproduction d'abord (pour qu'on les voie
	// en premier, dès la page 1), puis l'ordre public des mentions, puis l'ordre de
	// rencontre (tri stable). Vaut aussi filtre par filtre.
	const oeuvres = $derived(
		[...(fichier?.oeuvres ?? [])].sort((a, b) => {
			const ia = a.image ? 0 : 1;
			const ib = b.image ? 0 : 1;
			if (ia !== ib) return ia - ib;
			return rang(a.code) - rang(b.code);
		})
	);

	// Menu des musées : ceux qui conservent au moins une œuvre concernée de CET
	// artiste, jamais les autres. Effectif à côté du nom, tri par valeur
	// décroissante (CLAUDE.md), départage alphabétique pour que l'ordre soit
	// stable. La liste se refait toute seule quand l'artiste change, puisqu'elle
	// dérive du fichier chargé.
	const musees = $derived(
		Object.values(
			oeuvres.reduce((acc, o) => {
				if (!o.musee_code) return acc;
				const m = (acc[o.musee_code] ??= {
					code: o.musee_code,
					nom: o.musee,
					ville: o.ville,
					n: 0
				});
				m.n += 1;
				return acc;
			}, {})
		).sort((a, b) => b.n - a.n || (a.nom ?? '').localeCompare(b.nom ?? '', 'fr'))
	);

	// Le musée choisi, s'il concerne bien l'artiste affiché (garde-fou : un code
	// venu d'ailleurs ne doit pas vider la liste en silence).
	const musee = $derived(musees.find((m) => m.code === museeActif) ?? null);

	// DEUX FILTRES EMBOÎTÉS, dans cet ordre : le musée d'abord, la mention ensuite.
	// C'est ce qui permet aux puces de mention d'annoncer un nombre exact — une
	// puce « attribué à 276 » qui ne rendrait que 3 œuvres une fois un musée choisi
	// serait un chiffre faux (CLAUDE.md : toute quantité affichée doit être lisible).
	const oeuvresMusee = $derived(
		musee ? oeuvres.filter((o) => o.musee_code === musee.code) : oeuvres
	);

	// Puces de filtre : « Toutes » puis les mentions PRÉSENTES dans le périmètre
	// courant, ordre public, avec leur effectif. Les mentions absentes ne
	// paraissent pas — pas plus au sein d'un musée que pour l'artiste entier.
	const puces = $derived.by(() => {
		const compte = new Map();
		for (const o of oeuvresMusee) compte.set(o.code, (compte.get(o.code) ?? 0) + 1);
		return [
			{ code: null, label: 'Toutes', n: oeuvresMusee.length },
			...[...compte.entries()]
				.filter(([code]) => FAMILLE_PUBLIC[code])
				.sort((a, b) => rang(a[0]) - rang(b[0]))
				.map(([code, n]) => ({ code, label: fam(code).header, n }))
		];
	});

	const oeuvresFiltrees = $derived(
		familleActive ? oeuvresMusee.filter((o) => o.code === familleActive) : oeuvresMusee
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

	// Changer de musée remet la lecture à la première page. Si la mention choisie
	// n'existe pas dans le nouveau musée, elle est relâchée plutôt que de laisser
	// une liste vide sans raison lisible.
	function choisirMusee(code) {
		const suivant = code || null;
		if (museeActif === suivant) return;
		museeActif = suivant;
		const restantes = new Set(
			(suivant ? oeuvres.filter((o) => o.musee_code === suivant) : oeuvres).map((o) => o.code)
		);
		if (familleActive && !restantes.has(familleActive)) familleActive = null;
		page = 1;
		versHautListe();
	}

	// Retirer tous les filtres d'un coup — sortie de l'état vide, et retour au
	// périmètre complet de l'artiste.
	function toutAfficher() {
		if (!familleActive && !museeActif) return;
		familleActive = null;
		museeActif = null;
		page = 1;
		versHautListe();
	}

	// Accord du décompte : « 1 œuvre », « 8 œuvres ».
	const oeuvreS = (n) => `${n} œuvre${n === 1 ? '' : 's'}`;

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
		<!-- Filtre par musée : liste native (clavier, souris et tactile sans code
		     ajouté), bornée aux musées qui conservent une œuvre concernée de cet
		     artiste, chacun avec son effectif. -->
		{#if musees.length > 1 || musee}
			<div class="filtre-musee">
				<label for="filtre-musee">Musée</label>
				<select
					id="filtre-musee"
					value={museeActif ?? ''}
					onchange={(e) => choisirMusee(e.currentTarget.value)}
				>
					<option value="">Tous les musées ({oeuvres.length})</option>
					{#each musees as m (m.code)}
						<option value={m.code}>
							{m.nom}{m.ville ? `, ${m.ville}` : ''} — {m.n}
						</option>
					{/each}
				</select>
				<!-- Retrait direct : la liste dit DÉJÀ quel musée est actif, inutile de
				     le répéter en toutes lettres ; ce qui manquait, c'est le moyen d'en
				     sortir sans rouvrir le menu. C'est aussi la porte de sortie du
				     lecteur venu de la carte (phase 3). -->
				{#if musee}
					<button type="button" class="retirer" onclick={() => choisirMusee(null)}>
						Retirer ce filtre
					</button>
				{/if}
			</div>
		{/if}

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
				Aucune œuvre à afficher.
			{:else if nbFiltre <= PAR_PAGE}
				{oeuvreS(nbFiltre)}
			{:else}
				Œuvres <strong>{premier}</strong> à <strong>{dernier}</strong> sur <strong>{nbFiltre}</strong>
			{/if}
		</p>

		{#if nbFiltre === 0}
			<p class="etat vide">
				Aucune œuvre ne correspond à cette combinaison de filtres.
				<button type="button" class="reessayer" onclick={toutAfficher}>Tout afficher</button>
			</p>
		{:else}
			<ol class="entrees">
				{#each pageOeuvres as o (o.reference)}
					<li class="entree">
						{#if o.image}
							<!-- Reproduction ouverte, copie locale. L'image occupe toute la
							     vignette (même gabarit que le placeholder), en object-fit:
							     contain — proportions gardées, jamais rognée ni déformée. Aucun
							     texte par-dessus : la légende est UNE ligne discrète sous la
							     vignette.
							     Toutes ne montrent pas la même chose. Certaines montrent
							     l'exemplaire même décrit par la notice ; d'autres ne peuvent
							     montrer QU'UN AUTRE EXEMPLAIRE du même tirage — une planche
							     d'Épinal a été imprimée à des milliers d'exemplaires, le musée
							     conserve le sien et la bibliothèque le sien. La réserve est
							     écrite sous l'image, jamais sous-entendue.
							     Elle se lit sur `exemplaire_autre`, porté par la donnée, et NON
							     sur la provenance : depuis le 2026-08-07, des estampes venues de
							     Wikimedia Commons sont dans ce cas elles aussi, et s'en remettre
							     à la seule source ferait passer un exemplaire pour un autre. -->
							{@const autre = o.image.exemplaire_autre === true}
							{@const bnf = o.image.source_type === 'gallica_bnf'}
							<figure class="media-figure">
								<!-- La vignette OUVRE L'AGRANDISSEMENT, elle ne quitte plus le
								     site : c'est le geste attendu sur une image, et le lien vers
								     la source reste juste dessous, dans le crédit, où l'exige
								     l'attribution. Bouton et non lien : l'action est locale. -->
								<button
									class="media media-image"
									type="button"
									onclick={(e) => agrandir(o, e)}
									aria-label="Agrandir la reproduction : {o.titre ?? 'œuvre'}"
								>
									<img src="{base}/{o.image.url}" alt={autre ? `Autre exemplaire du même tirage : ${o.titre ?? 'œuvre'}` : `Reproduction : ${o.titre ?? 'œuvre'}`} loading="lazy" />
								</button>
								<figcaption>
									<CreditImage image={o.image} />
								</figcaption>
							</figure>
						{:else}
							<!-- Pas de reproduction réutilisable connue. Le cadre vide occupait
							     autant de place qu'une image : sur un fonds sans reproduction, la
							     liste devenait une colonne de boîtes vides (C10, 2026-08-03). Il
							     est remplacé par une mention brève, en tête de la même colonne —
							     l'alignement du texte est conservé, les entrées qui PORTENT une
							     image ne changent pas. -->
							<p class="media-absente">Reproduction non disponible</p>
						{/if}
						<div class="corps">
							<p class="kicker">
								<span class="trait-famille" style="background: {fam(o.code).couleur}"></span>{fam(o.code).header}
							</p>
							<h4 class="titre">{o.titre ?? 'Sans titre'}</h4>
							<!-- Le lieu disparaît quand un filtre par musée est actif : toutes les
							     entrées viennent alors du même établissement, et le répéter sous
							     chacune n'ajoute rien (C9, 2026-08-03). -->
							{#if lieu(o) && !musee}<p class="lieu">{lieu(o)}</p>{/if}
							<p class="verbatim" style="border-left-color: {fam(o.code).couleur}">«&nbsp;{o.extrait}&nbsp;»</p>
							<a class="lien-fiche" href={lienPop(o.reference)} target="_blank" rel="noopener">
								Voir la notice sur POP
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

{#if agrandie}
	<LightboxOeuvre oeuvre={agrandie} fermer={refermerAgrandie} />
{/if}


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
	/* --- Filtre par musée : une liste native, dans le registre UI des puces. --- */
	.filtre-musee {
		display: flex;
		align-items: center;
		flex-wrap: wrap;
		gap: var(--espace-2) var(--espace-3);
		margin: 0 0 var(--espace-3);
		font-family: var(--police-ui);
		font-size: var(--taille-xs);
	}

	.filtre-musee label {
		letter-spacing: 0.04em;
		text-transform: uppercase;
		color: var(--couleur-encre-douce);
	}

	.filtre-musee select {
		/* Le nom officiel d'un musée est long : la liste prend la largeur qu'il lui
		   faut, plafonnée, sans jamais pousser la colonne (min-width: 0). Elle ne
		   s'étire PAS jusqu'au bord : le bouton de retrait doit rester à côté
		   d'elle, pas plaqué contre la marge droite. */
		flex: 0 1 26rem;
		min-width: 0;
		max-width: 100%;
		padding: 0.3rem 0.5rem;
		font-family: inherit;
		font-size: inherit;
		color: var(--couleur-encre);
		background: var(--surface-carte);
		border: 1px solid var(--couleur-trait);
		border-radius: var(--rayon-s);
		cursor: pointer;
	}

	.filtre-musee select:focus-visible {
		outline: var(--focus-anneau);
		outline-offset: 2px;
	}

	.retirer {
		font-family: inherit;
		font-size: inherit;
		color: var(--couleur-accent);
		background: none;
		border: 0;
		padding: 0;
		text-decoration: underline;
		cursor: pointer;
	}

	.retirer:focus-visible {
		outline: var(--focus-anneau);
		outline-offset: 2px;
	}

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
		grid-template-columns: 11rem 1fr;
		gap: var(--espace-5);
		padding: var(--espace-4) 0;
		border-top: var(--filet);
	}

	/* Emplacement média réservé : cadre neutre, pas une image. Même boîte 4/5
	   pour le placeholder ET la reproduction (gabarit identique). */
	.media {
		aspect-ratio: 4 / 5;
		background: var(--surface-carte);
		border: var(--filet);
		display: flex;
		align-items: center;
		justify-content: center;
		text-align: center;
		overflow: hidden;
	}

	.media span {
		font-family: var(--police-ui);
		font-size: 0.62rem;
		letter-spacing: 0.05em;
		text-transform: uppercase;
		line-height: 1.35;
		color: var(--couleur-trait);
	}

	/* Reproduction réelle : l'ancre EST la boîte média (classe .media), l'image la
	   remplit en object-fit: contain — proportions gardées, jamais rognée. */
	/* Mention compacte à la place du cadre : quelques millimètres au lieu d'une
	   boîte de 14 rem, dans la colonne du média pour que les titres restent alignés
	   d'une entrée à l'autre. */
	/* Reproduction absente : une mention COMPACTE, jamais un cadre vide.
	   Elle n'est plus masquée aux lecteurs d'écran (2026-08-08) : l'information est
	   utile — la notice existe, l'image manque — et elle est désormais explicite au
	   lieu de dire « non affichée », qui laissait croire à un choix d'affichage.
	   Ni bordure de boîte, ni fond, ni curseur : rien qui ressemble à une image
	   cliquable. */
	.media-absente {
		margin: 0;
		/* sans quoi l'élément s'étire sur toute la hauteur de la ligne de grille et
		   sa boîte reste aussi haute que l'ancien cadre, pour trois mots */
		align-self: start;
		padding-top: 0.35rem;
		border-top: var(--filet-clair);
		font-family: var(--police-ui);
		font-size: 0.68rem;
		letter-spacing: 0.03em;
		line-height: 1.35;
		color: var(--couleur-encre-douce);
	}

	.media-figure {
		margin: 0;
		min-width: 0;
	}

	/* La vignette est un bouton depuis le 2026-08-08 : on remet à zéro ce que le
	   navigateur lui ajoute, `.media` fournissant déjà le cadre. */
	.media-image {
		padding: 0;
		width: 100%;
		font: inherit;
		color: inherit;
		cursor: zoom-in;
	}

	.media-image img {
		width: 100%;
		height: 100%;
		object-fit: contain;
		display: block;
		transition: transform 180ms ease;
	}

	/* Signe d'agrandissement au survol : l'image avance très légèrement et le cadre
	   prend l'accent. Aucun voile sombre — on ne masque pas une œuvre pour annoncer
	   qu'on peut la voir en grand. */
	.media-image:hover img,
	.media-image:focus-visible img {
		transform: scale(1.03);
	}

	.media-image:hover {
		border-color: var(--accent-cobalt);
	}

	@media (prefers-reduced-motion: reduce) {
		.media-image img {
			transition: none;
		}
		.media-image:hover img,
		.media-image:focus-visible img {
			transform: none;
		}
	}

	.media-image:focus-visible {
		outline: var(--focus-anneau);
		outline-offset: 2px;
	}

	/* Crédit : UNE ligne discrète sous la vignette. Liens accessibles mais atténués,
	   jamais le traitement du lien principal « Voir la fiche publique sur POP ». */
	.credit {
		margin-top: 0.4rem;
		font-family: var(--police-ui);
		font-size: 0.62rem;
		line-height: 1.4;
		color: var(--couleur-encre-douce);
	}

	/* La réserve passe AVANT le crédit et sur sa propre ligne : elle dit ce que
	   l'image est, et cela prime sur d'où elle vient. Une planche d'Épinal existe
	   en milliers d'exemplaires ; celui de la BnF n'est pas celui du musée. */
	.credit-reserve {
		display: block;
		font-style: italic;
	}

	.credit a {
		color: inherit;
		text-decoration: underline;
		text-underline-offset: 1px;
	}

	.credit a:hover,
	.credit a:focus-visible {
		color: var(--couleur-encre);
	}

	.corps {
		min-width: 0;
	}

	/* Repère de famille : un TRAIT et non plus une pastille (2026-08-08). Le point
	   rond appartient au graphique, où il porte une mesure ; répété ici, il évoquait
	   une puce ou un état cliquable. Un trait couché sous le même angle que le
	   libellé se lit comme un repère de catégorie, rien d'autre.
	   Le filet VERTICAL devant le verbatim est conservé et garde son rôle propre :
	   le trait nomme la famille, le filet accompagne les mots du musée. */
	.trait-famille {
		flex: none;
		width: 20px;
		height: 3px;
		/* Le libellé est en capitales : son axe optique est un peu au-dessus du
		   centre de la ligne. Sans ce décalage, le trait paraît tomber. */
		margin-top: 1px;
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

	/* Action vers la notice publique : un vrai lien, présenté en BOUTON SECONDAIRE
	   (2026-08-08). Contour fin et fond transparent — l'action existe sur chaque
	   entrée de la liste, un aplat plein en ferait huit taches par page. La flèche
	   est retirée : le libellé dit déjà qu'on sort du site, et l'onglet s'ouvre à
	   part. N'étant pas un lien de texte courant, il ne prend pas le soulignement
	   permanent de la charte (§ 9) : le contour tient ce rôle. */
	.lien-fiche {
		display: inline-block;
		padding: 0.34rem 0.7rem;
		border: 1px solid rgba(53, 87, 138, 0.45);
		border-radius: 2px;
		font-family: var(--police-ui);
		font-size: var(--taille-s);
		color: var(--accent-cobalt);
		text-decoration: none;
		transition: background 140ms ease, border-color 140ms ease;
	}

	.lien-fiche:hover {
		background: rgba(53, 87, 138, 0.08);
		border-color: var(--accent-cobalt);
	}

	.lien-fiche:focus-visible {
		outline: 2px solid var(--accent-cobalt);
		outline-offset: 2px;
	}

	@media (prefers-reduced-motion: reduce) {
		.lien-fiche {
			transition: none;
		}
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
			grid-template-columns: 7rem 1fr;
			gap: var(--espace-4);
		}
		.verbatim {
			font-size: 1.15rem;
		}
	}
</style>
