<script>
	// Schéma nº 2 de la page « Méthode » (palier 4, 2026-07-31) : un homonyme
	// correctement séparé. Cas RÉEL et vérifié une notice à une (docs/donnees.md,
	// « effet de l'identité ») : sous le nom de Michel-Ange, la base range quatre
	// autres personnes. Schéma en HTML/CSS, pas une image : lisible au zoom et
	// accessible. La couleur ne porte jamais seule l'information — chaque ligne
	// écartée dit en toutes lettres de qui il s'agit.

	// Formes du champ « Auteur » réellement relevées sous ce nom. `lui` = la seule
	// qui désigne vraiment Michel-Ange ; les autres sont d'autres personnes.
	const formes = [
		{ forme: 'BUONARROTI Michelangelo', qui: 'Michel-Ange lui-même', lui: true },
		{ forme: 'CORNEILLE Michel-Ange', qui: 'peintre lyonnais du XVIIᵉ siècle' },
		{ forme: 'CERQUOZZI Michelangelo', qui: 'peintre romain du XVIIᵉ siècle' },
		{ forme: 'MERISI Michelangelo', qui: 'le Caravage' },
		{ forme: 'PACE Michelangelo', qui: 'peintre romain du XVIIᵉ siècle' }
	];
</script>

<figure class="schema">
	<p class="titre-schema">Un même nom, plusieurs personnes</p>

	<div class="colonnes">
		<div class="colonne">
			<p class="chapeau">Ce que le nom ramène, cherché tel quel</p>
			<ul class="formes">
				{#each formes as f (f.forme)}
					<li class:autre={!f.lui}>
						<span class="mot">{f.forme}</span>
						<span class="glose">{f.qui}</span>
					</li>
				{/each}
			</ul>
		</div>

		<p class="fleche" aria-hidden="true">→</p>

		<div class="colonne">
			<p class="chapeau">Ce que le projet compte</p>
			<ul class="formes">
				<li class="retenu">
					<span class="mot">Michel-Ange</span>
					<span class="glose">Michelangelo Buonarroti, et lui seul</span>
				</li>
			</ul>
			<p class="sortie">
				Les quatre autres sont d’autres artistes&nbsp;: ils sortent de ce décompte
				et sont comptés sous leur propre nom.
			</p>
		</div>
	</div>

	<figcaption>
		Cas réel, vérifié notice par notice&nbsp;: sous ce seul nom, 24 notices prudentes
		désignaient en réalité quelqu’un d’autre.
	</figcaption>
</figure>

<style>
	.schema {
		margin: var(--espace-5) 0;
		padding: var(--espace-4);
		background: var(--surface-carte);
		border: var(--filet);
		border-radius: var(--rayon-m);
	}

	.titre-schema {
		font-family: var(--police-ui);
		font-size: var(--taille-xs);
		letter-spacing: 0.08em;
		text-transform: uppercase;
		color: var(--couleur-encre-douce);
		margin: 0 0 var(--espace-4);
	}

	/* Avant → après. La flèche devient verticale sur mobile (media query). */
	.colonnes {
		display: grid;
		grid-template-columns: 1fr auto 1fr;
		gap: var(--espace-4);
		/* Les deux chapeaux sur la même ligne ; seule la flèche est centrée. */
		align-items: start;
	}

	.chapeau {
		font-family: var(--police-ui);
		font-size: var(--taille-xs);
		line-height: 1.4;
		color: var(--couleur-encre-douce);
		margin: 0 0 var(--espace-3);
	}

	.formes {
		list-style: none;
		margin: 0;
		padding: 0;
		display: grid;
		gap: var(--espace-2);
	}

	.formes li {
		padding-left: var(--espace-3);
		border-left: 2px solid var(--couleur-trait);
	}

	.mot {
		display: block;
		font-family: var(--police-titre);
		font-size: var(--taille-base);
		line-height: 1.3;
	}

	.glose {
		display: block;
		font-family: var(--police-ui);
		font-size: var(--taille-xs);
		color: var(--couleur-encre-douce);
	}

	/* Les autres personnes : encre estompée, filet neutre. */
	.autre .mot {
		color: var(--couleur-encre-douce);
	}

	/* Le seul retenu : filet à l'accent du projet, encre pleine. */
	.retenu {
		border-left-color: var(--couleur-accent) !important;
	}

	.fleche {
		margin: 0;
		font-size: var(--taille-l);
		color: var(--couleur-encre-douce);
		text-align: center;
		align-self: center;
	}

	.sortie {
		margin: var(--espace-3) 0 0;
		font-family: var(--police-ui);
		font-size: var(--taille-xs);
		line-height: 1.5;
		color: var(--couleur-encre-douce);
	}

	figcaption {
		margin-top: var(--espace-4);
		padding-top: var(--espace-3);
		border-top: var(--filet-clair);
		font-family: var(--police-ui);
		font-size: var(--taille-xs);
		line-height: 1.5;
		color: var(--couleur-encre-douce);
	}

	@media (max-width: 640px) {
		.colonnes {
			grid-template-columns: 1fr;
			gap: var(--espace-3);
		}
		.fleche {
			transform: rotate(90deg);
			line-height: 1;
		}
	}
</style>
