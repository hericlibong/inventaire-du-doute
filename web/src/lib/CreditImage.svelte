<script>
	// Crédit d'une reproduction — SOURCE UNIQUE de la ligne d'attribution.
	//
	// Extrait de OeuvresMaitre.svelte le 2026-08-08, quand la lightbox a eu besoin
	// d'afficher le même crédit sous l'image agrandie. Le dupliquer aurait créé deux
	// formulations d'une obligation légale, vouées à diverger : une licence, un
	// auteur et un lien de source ne se recopient pas.
	//
	// Quatre cas, dans cet ordre de priorité :
	//   1. `pop_joconde` — reproduction venue de la fiche POP de l'œuvre. EN TÊTE
	//      de la chaîne depuis le 2026-08-24, et c'est délibéré : les branches
	//      suivantes nomment Wikimedia Commons et une licence libre en dur. Une
	//      image POP qui tomberait dans l'une d'elles afficherait une fausse
	//      source ET une fausse licence. La placer en premier rend cette erreur
	//      impossible, quelle que soit la forme de l'entrée.
	//      POP ne publie pas de licence de réutilisation : on n'en invente donc
	//      aucune, et on n'écrit pas davantage qu'elle manque — le crédit du
	//      photographe et le lien vers la fiche disent ce qu'on sait ;
	//   2. `exemplaire_autre` — l'image ne montre PAS la feuille décrite par la
	//      notice, mais un autre exemplaire du même tirage. La réserve passe avant
	//      le crédit et sur sa propre ligne : elle dit ce que l'image est, ce qui
	//      prime sur d'où elle vient. Elle se lit sur la DONNÉE, jamais sur la
	//      provenance (2026-08-07) ;
	//   3. licence CC BY* — l'attribution de l'auteur est obligatoire, le nom de la
	//      licence est cliquable vers son texte ;
	//   4. domaine public ou CC0 — la source suffit.
	//
	// `taille` : 'vignette' (0,62 rem, sous la liste) ou 'agrandie' (0,78 rem, sous
	// la lightbox, où la ligne est plus longue et lue de plus loin).
	let { image, taille = 'vignette' } = $props();

	const autre = $derived(image.exemplaire_autre === true);
	const bnf = $derived(image.source_type === 'gallica_bnf');
	const pop = $derived(image.source_type === 'pop_joconde');

	// Les entrées POP n'ont pas de licence : `licence` y vaut la chaîne vide. Les
	// tests qui suivent doivent donc supporter une licence vide ou absente —
	// `image.licence.startsWith(…)` levait une exception sur une entrée sans le
	// champ, et faisait disparaître toute la ligne de crédit.
	const licence = $derived(image.licence ?? '');

	// Le crédit photographique manque sur une partie des fiches POP. Le repli est
	// une formule D'AFFICHAGE, et il ne vit qu'ici : la donnée garde son champ
	// vide, parce que la source n'a jamais écrit cette phrase.
	const creditPop = $derived(image.credit?.trim() || 'Crédit photographique non précisé');
</script>

<span class="credit" class:agrandie={taille === 'agrandie'}>
	{#if pop}
		<span class="credit-auteur" title={creditPop}>{creditPop}</span> · source <a
			href={image.source}
			target="_blank"
			rel="noopener">POP</a>
	{:else if autre}
		<span class="credit-reserve">Autre exemplaire du même tirage</span>
		{#if bnf}
			Domaine public · source <a href={image.source} target="_blank" rel="noopener">Gallica&nbsp;(BnF)</a>
		{:else}
			{#if image.credit}<span class="credit-auteur" title={image.credit}>{image.credit}</span> ·&nbsp;{/if}{licence === 'CC0' ? 'CC0' : licence || 'Domaine public'} · source <a href={image.source} target="_blank" rel="noopener">Wikimedia&nbsp;Commons</a>
		{/if}
	{:else if licence.startsWith('CC BY')}
		{#if image.creator}<span class="credit-auteur" title={image.creator}>{image.creator}</span> ·&nbsp;{/if}<a href={image.licence_url || image.source} target="_blank" rel="noopener">{licence}</a> · <a href={image.source} target="_blank" rel="noopener">Wikimedia&nbsp;Commons</a>
	{:else}
		{licence === 'CC0' ? 'CC0' : 'Domaine public'} · source <a href={image.source} target="_blank" rel="noopener">Wikimedia&nbsp;Commons</a>
	{/if}
</span>

<style>
	.credit {
		display: block;
		font-family: var(--police-ui);
		font-size: 0.62rem;
		line-height: 1.4;
		color: var(--couleur-encre-douce);
	}

	.credit.agrandie {
		font-size: 0.78rem;
		line-height: 1.5;
	}

	/* La réserve dit ce que l'image EST : elle passe avant le crédit, sur sa propre
	   ligne. Une planche d'Épinal existe en milliers d'exemplaires ; celui de la
	   BnF n'est pas celui du musée. */
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

	/* Dans la lightbox, le fond est sombre : le crédit et ses liens s'y lisent en
	   clair. La règle vit ici pour que la couleur ne soit jamais fixée deux fois. */
	.credit.agrandie {
		color: rgba(238, 240, 243, 0.78);
	}

	.credit.agrandie a:hover,
	.credit.agrandie a:focus-visible {
		color: #eef0f3;
	}
</style>
