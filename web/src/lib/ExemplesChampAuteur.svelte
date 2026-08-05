<script>
	// TROIS EXTRAITS RÉELS du champ « Auteur » (2026-08-05). Remplace le schéma
	// annoté qui occupait cette place depuis le 2026-07-31 : il se lisait comme une
	// planche technique posée au milieu du texte, et ne disait pas de QUELLES
	// notices il parlait. Ici, chaque exemple est une notice identifiée — œuvre,
	// musée, valeur publiée, lien vers POP —, et la suite se lit comme le reste de
	// la page : des lignes séparées par un filet, pas une carte.
	//
	// Les valeurs du champ sont reproduites MOT POUR MOT. Elles sont écrites ici
	// plutôt que lues dans un export : ce sont trois citations choisies, contrôlées
	// le 2026-08-05 contre data/exports/web/oeuvres/*.json (références, titres,
	// musées, villes et champ « Auteur » concordants) et contre POP (liens en 200).
	//
	// La couleur de la réserve est celle de sa famille dans la charte (tokens.css) :
	// rouge pour « attribué », ocre-orangé pour le point d'interrogation seul. Elle
	// ne décore pas, elle désigne la même chose que partout ailleurs sur le site.
	const EXEMPLES = [
		{
			titre: "Jeanne d'Albret, reine de Navarre",
			lieu: 'musée Condé, Chantilly',
			nom: 'CLOUET François',
			reserve: '(attribué)',
			couleur: 'var(--forme-attribue)',
			explication:
				"La parenthèse indique que l'attribution à François Clouet est proposée avec réserve.",
			pop: 'https://pop.culture.gouv.fr/notice/joconde/00000077133'
		},
		{
			titre: 'La Présentation au Temple',
			lieu: 'musée Greuze, Tournus',
			nom: 'VOUET Simon',
			reserve: '(?)',
			couleur: 'var(--forme-point-interrogation)',
			explication: "Le point d'interrogation signale directement l'incertitude sur l'auteur.",
			pop: 'https://pop.culture.gouv.fr/notice/joconde/01810000027'
		},
		{
			titre: 'Chien-barbet chassant des canards sauvages',
			lieu: 'musée national du château de Fontainebleau',
			nom: 'OUDRY Jean-Baptiste',
			reserve: '(attribué, ?)',
			couleur: 'var(--forme-attribue)',
			explication: 'La notice associe une attribution proposée à un point d’interrogation.',
			pop: 'https://pop.culture.gouv.fr/notice/joconde/50130000371'
		}
	];
</script>

<ul class="exemples">
	{#each EXEMPLES as e (e.pop)}
		<li style="--pigment: {e.couleur}">
			<p class="oeuvre">{e.titre}</p>
			<p class="lieu">{e.lieu}</p>
			<p class="champ">
				<span class="etiquette">Champ Auteur</span>
				<span class="valeur">{e.nom} <span class="reserve">{e.reserve}</span></span>
			</p>
			<p class="explication">{e.explication}</p>
			<p class="renvoi">
				<a href={e.pop} target="_blank" rel="noopener">Consulter la notice sur POP&nbsp;→</a>
			</p>
		</li>
	{/each}
</ul>

<style>
	.exemples {
		list-style: none;
		margin: var(--espace-5) 0;
		padding: 0;
		max-width: 44rem;
	}

	/* Un filet entre deux exemples, rien autour : la suite appartient à la colonne
	   de texte, elle ne s'en détache pas. */
	.exemples li + li {
		margin-top: var(--espace-5);
		padding-top: var(--espace-5);
		border-top: var(--filet-clair);
	}

	.oeuvre {
		margin: 0;
		font-family: var(--police-titre);
		font-size: var(--taille-m);
		line-height: 1.3;
	}

	.lieu {
		margin: var(--espace-1) 0 0;
		font-family: var(--police-ui);
		font-size: var(--taille-xs);
		color: var(--couleur-encre-douce);
	}

	/* Le champ reproduit : son nom à gauche, sa valeur à droite. Les deux passent
	   l'un sous l'autre dès que la place manque. */
	.champ {
		display: flex;
		flex-wrap: wrap;
		align-items: baseline;
		gap: var(--espace-1) var(--espace-3);
		margin: var(--espace-3) 0 0;
	}

	.etiquette {
		font-family: var(--police-ui);
		font-size: var(--taille-xs);
		letter-spacing: 0.06em;
		text-transform: uppercase;
		color: var(--couleur-encre-douce);
	}

	.valeur {
		font-family: var(--police-titre);
		font-size: var(--taille-m);
	}

	/* Seule la parenthèse est mise en évidence : c'est elle que le projet lit. */
	.reserve {
		color: var(--pigment);
	}

	.explication {
		margin: var(--espace-2) 0 0;
		line-height: 1.65;
	}

	.renvoi {
		margin: var(--espace-2) 0 0;
		font-family: var(--police-ui);
		font-size: var(--taille-xs);
	}

	/* Sur petit écran, l'étiquette passe systématiquement au-dessus de la valeur :
	   laissée au retour à la ligne automatique, elle restait à côté dans deux
	   exemples sur trois et changeait de place d'un exemple à l'autre. */
	@media (max-width: 480px) {
		.champ {
			display: block;
		}

		.valeur {
			display: block;
			margin-top: var(--espace-1);
		}
	}

	/* Le lien est écrit ici : le style de la page ne franchit pas la frontière d'un
	   composant, et sans cette règle il sortirait en bleu souligné du navigateur. */
	.renvoi a {
		color: var(--accent-cobalt);
		text-decoration: none;
		border-bottom: 1px solid transparent;
	}

	.renvoi a:hover,
	.renvoi a:focus-visible {
		border-bottom-color: var(--accent-cobalt);
	}
</style>
