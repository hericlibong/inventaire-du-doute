<script>
	// UN MÊME NOM, PLUSIEURS PERSONNES (2026-08-05). Reprend le schéma du
	// 2026-07-31 — mêmes formes réelles, même cas — mais dans la composition des
	// autres exemples de la page : deux volets reliés par une flèche, dans la
	// colonne de texte, sans carte autour.
	//
	// Cas RÉEL, vérifié notice par notice (docs/donnees.md, « l'effet de
	// l'identité ») : sous le nom de Michel-Ange, la base range quatre autres
	// personnes, pour 24 notices prudentes au total — CORNEILLE Michel-Ange (13),
	// CERQUOZZI Michelangelo (6), MERISI Michelangelo (4), PACE Michelangelo (1).
	//
	// Ce que le volet de droite NE dit PAS (2026-08-05) : que ces personnes sont
	// publiées ailleurs sur le site. Elles ne sont pas rattachées à ce profil, et
	// c'est tout ce que le projet peut affirmer ici.
	//
	// La couleur ne porte jamais seule l'information : chaque ligne écartée dit en
	// toutes lettres de qui il s'agit.
	const formes = [
		{ forme: 'BUONARROTI Michelangelo', qui: 'Michel-Ange lui-même', lui: true },
		{ forme: 'CORNEILLE Michel-Ange', qui: 'peintre lyonnais du XVIIᵉ siècle' },
		{ forme: 'CERQUOZZI Michelangelo', qui: 'peintre romain du XVIIᵉ siècle' },
		{ forme: 'MERISI Michelangelo', qui: 'le Caravage' },
		{ forme: 'PACE Michelangelo', qui: 'peintre romain du XVIIᵉ siècle' }
	];
</script>

<div class="exemple">
	<p class="titre">Pourquoi tous les «&nbsp;Michelangelo&nbsp;» ne désignent-ils pas Michel-Ange&nbsp;?</p>

	<div class="volets">
		<div class="volet">
			<p class="entete">Personnes trouvées dans les notices</p>
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

		<div class="volet">
			<p class="entete">Personne rattachée au profil de Michel-Ange</p>
			<ul class="formes">
				<li class="retenu">
					<span class="mot">Michel-Ange</span>
					<span class="glose">Michelangelo Buonarroti</span>
				</li>
			</ul>
			<p class="sortie">Les autres ne sont pas rattachées à ce profil.</p>
		</div>
	</div>

	<p class="bilan">
		Vingt-quatre notices repérées à partir du nom «&nbsp;Michelangelo&nbsp;» concernaient en
		réalité une autre personne. Elles ne sont pas comptées dans le profil de Michelangelo
		Buonarroti.
	</p>
</div>

<style>
	.exemple {
		margin: var(--espace-5) 0;
		max-width: 44rem;
	}

	.titre {
		margin: 0;
		font-family: var(--police-ui);
		font-size: var(--taille-xs);
		letter-spacing: 0.06em;
		text-transform: uppercase;
		line-height: 1.4;
		color: var(--couleur-encre-douce);
	}

	.volets {
		display: grid;
		grid-template-columns: 1fr auto 1fr;
		align-items: start;
		gap: var(--espace-4);
		margin-top: var(--espace-4);
	}

	.volet {
		padding-left: var(--espace-3);
		border-left: 2px solid var(--couleur-trait);
	}

	.entete {
		margin: 0 0 var(--espace-3);
		font-family: var(--police-ui);
		font-size: var(--taille-xs);
		line-height: 1.4;
		color: var(--couleur-encre-douce);
	}

	.formes {
		list-style: none;
		margin: 0;
		padding: 0;
	}

	.formes li + li {
		margin-top: var(--espace-3);
	}

	.mot {
		display: block;
		font-family: var(--police-titre);
		line-height: 1.3;
	}

	.glose {
		display: block;
		font-family: var(--police-ui);
		font-size: var(--taille-xs);
		color: var(--couleur-encre-douce);
	}

	/* Les personnes qui ne sont pas Michel-Ange : le nom passe en gris, et la ligne
	   dit de qui il s'agit — la couleur ne porte pas l'information toute seule. */
	.autre .mot {
		color: var(--couleur-encre-douce);
	}

	.retenu .mot {
		color: var(--forme-attribue);
	}

	.sortie {
		margin: var(--espace-3) 0 0;
		font-family: var(--police-ui);
		font-size: var(--taille-xs);
		line-height: 1.5;
		color: var(--couleur-encre-douce);
	}

	.fleche {
		margin: 0;
		align-self: center;
		font-size: var(--taille-l);
		color: var(--couleur-encre-douce);
	}

	.bilan {
		margin: var(--espace-4) 0 0;
		font-size: var(--taille-s);
		line-height: 1.6;
	}

	@media (max-width: 640px) {
		.volets {
			grid-template-columns: minmax(0, 1fr);
			gap: var(--espace-3);
		}

		.fleche {
			align-self: start;
			transform: rotate(90deg);
			padding-left: var(--espace-3);
		}
	}
</style>
