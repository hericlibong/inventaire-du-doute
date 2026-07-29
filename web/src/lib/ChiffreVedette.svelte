<script>
	// Primitive du kit (docs/charte-graphique.md §5) : un grand nombre (Fraunces,
	// tabulaire) surmontant une légende courte. Repère de profil, JAMAIS la mesure
	// principale d'une dataviz (celle-ci passe par position/longueur — CLAUDE.md).
	//
	//   valeur  — nombre DÉJÀ mis en forme en français (« 3 344 »), pas un entier
	//             brut : la mise en forme (espace insécable, accord) vit chez
	//             l'appelant, qui connaît le sens du nombre.
	//   legende — glose courte sous le nombre (« œuvres sous le nom de… »).
	let { valeur, legende } = $props();
</script>

<p class="chiffre-vedette">
	<span class="valeur">{valeur}</span>
	<span class="legende">{legende}</span>
</p>

<style>
	.chiffre-vedette {
		margin: 0;
		display: flex;
		flex-direction: column;
		gap: 0.1rem;
	}

	/* Le nombre porte l'appui visuel : Fraunces (police des titres et des chiffres
	   vedettes, charte §4), chiffres tabulaires pour aligner les valeurs empilées. */
	.valeur {
		font-family: var(--police-titre);
		font-size: var(--taille-l);
		font-weight: 700;
		line-height: 1.1;
		color: var(--accent-cobalt);
		font-variant-numeric: tabular-nums;
	}

	.legende {
		font-size: var(--taille-s);
		line-height: 1.4;
		color: var(--couleur-encre-douce);
	}
</style>
