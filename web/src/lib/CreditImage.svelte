<script>
	// Crédit d'une reproduction — SOURCE UNIQUE de la ligne d'attribution.
	//
	// Extrait de OeuvresMaitre.svelte le 2026-08-08, quand la lightbox a eu besoin
	// d'afficher le même crédit sous l'image agrandie. Le dupliquer aurait créé deux
	// formulations d'une obligation légale, vouées à diverger : une licence, un
	// auteur et un lien de source ne se recopient pas.
	//
	// Trois cas, dans cet ordre de priorité :
	//   1. `exemplaire_autre` — l'image ne montre PAS la feuille décrite par la
	//      notice, mais un autre exemplaire du même tirage. La réserve passe avant
	//      le crédit et sur sa propre ligne : elle dit ce que l'image est, ce qui
	//      prime sur d'où elle vient. Elle se lit sur la DONNÉE, jamais sur la
	//      provenance (2026-08-07) ;
	//   2. licence CC BY* — l'attribution de l'auteur est obligatoire, le nom de la
	//      licence est cliquable vers son texte ;
	//   3. domaine public ou CC0 — la source suffit.
	//
	// `taille` : 'vignette' (0,62 rem, sous la liste) ou 'agrandie' (0,78 rem, sous
	// la lightbox, où la ligne est plus longue et lue de plus loin).
	let { image, taille = 'vignette' } = $props();

	const autre = $derived(image.exemplaire_autre === true);
	const bnf = $derived(image.source_type === 'gallica_bnf');
</script>

<span class="credit" class:agrandie={taille === 'agrandie'}>
	{#if autre}
		<span class="credit-reserve">Autre exemplaire du même tirage</span>
		{#if bnf}
			Domaine public · source <a href={image.source} target="_blank" rel="noopener">Gallica&nbsp;(BnF)</a>
		{:else}
			{#if image.credit}<span class="credit-auteur" title={image.credit}>{image.credit}</span> ·&nbsp;{/if}{image.licence === 'CC0' ? 'CC0' : image.licence || 'Domaine public'} · source <a href={image.source} target="_blank" rel="noopener">Wikimedia&nbsp;Commons</a>
		{/if}
	{:else if image.licence.startsWith('CC BY')}
		{#if image.creator}<span class="credit-auteur" title={image.creator}>{image.creator}</span> ·&nbsp;{/if}<a href={image.licence_url || image.source} target="_blank" rel="noopener">{image.licence}</a> · <a href={image.source} target="_blank" rel="noopener">Wikimedia&nbsp;Commons</a>
	{:else}
		{image.licence === 'CC0' ? 'CC0' : 'Domaine public'} · source <a href={image.source} target="_blank" rel="noopener">Wikimedia&nbsp;Commons</a>
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
