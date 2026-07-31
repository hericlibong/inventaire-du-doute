<script>
	// Schéma nº 1 de la page « Méthode » (palier 4, 2026-07-31) : comment le doute
	// s'écrit dans une notice. Reproduction typographique annotée du champ
	// « Auteur », sur trois formes RÉELLES relevées dans la base (jamais un
	// exemple inventé). Schéma en HTML/CSS et non en image : thémable, lisible au
	// zoom, accessible aux lecteurs d'écran, sans dépendance externe.
</script>

<figure class="schema">
	<p class="titre-schema">Le doute s’écrit entre parenthèses, après le nom</p>

	<!-- Premier exemple, annoté sous chaque partie. -->
	<div class="fiche">
		<span class="etiquette">Auteur</span>
		<span class="valeur">
			<span class="jeton">
				<span class="mot">CLOUET François</span>
				<span class="note">le nom de l’artiste</span>
			</span>
			<span class="jeton reserve">
				<span class="mot">(attribué)</span>
				<span class="note">la réserve du musée</span>
			</span>
		</span>
	</div>

	<!-- Les deux autres formes, sans annotation redondante. -->
	<ul class="variantes">
		<li>
			<span class="etiquette">Auteur</span>
			<span class="mot">VOUET Simon <span class="marque">(?)</span></span>
			<span class="glose">le doute tient dans un seul signe</span>
		</li>
		<li>
			<span class="etiquette">Auteur</span>
			<span class="mot">OUDRY Jean-Baptiste <span class="marque">(attribué, ?)</span></span>
			<span class="glose">les deux à la fois, dans la même parenthèse</span>
		</li>
	</ul>

	<figcaption>
		Trois champs «&nbsp;Auteur&nbsp;» de la base Joconde, reproduits tels quels.
		C’est cette parenthèse que le projet lit.
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

	/* Fac-similé : l'étiquette du champ à gauche, sa valeur à droite. */
	.fiche {
		display: flex;
		flex-wrap: wrap;
		align-items: baseline;
		gap: var(--espace-3);
	}

	.etiquette {
		font-family: var(--police-ui);
		font-size: var(--taille-xs);
		letter-spacing: 0.06em;
		text-transform: uppercase;
		color: var(--couleur-encre-douce);
		border-bottom: var(--filet);
		padding-bottom: 2px;
	}

	.valeur {
		display: flex;
		flex-wrap: wrap;
		align-items: start;
		gap: var(--espace-1) var(--espace-2);
	}

	/* Chaque partie du champ porte son annotation dessous, séparée par un filet
	   qui joue le rôle d'accolade. Les jetons passent à la ligne sur mobile. */
	.jeton {
		display: inline-grid;
		justify-items: start;
		gap: var(--espace-1);
	}

	.mot {
		font-family: var(--police-titre);
		font-size: var(--taille-m);
	}

	.note {
		font-family: var(--police-ui);
		font-size: var(--taille-xs);
		line-height: 1.35;
		color: var(--couleur-encre-douce);
		border-top: 1px solid var(--couleur-trait);
		padding-top: var(--espace-1);
		width: 100%;
	}

	/* La réserve : marquée du rouge de la mention « attribué à », couleur stable
	   du projet (tokens.css). */
	.reserve .mot,
	.marque {
		color: var(--forme-attribue);
	}

	.reserve .note {
		border-top-color: var(--forme-attribue);
		color: var(--forme-attribue);
	}

	.variantes {
		list-style: none;
		margin: var(--espace-5) 0 0;
		padding: var(--espace-4) 0 0;
		border-top: var(--filet-clair);
		display: grid;
		gap: var(--espace-3);
	}

	.variantes li {
		display: flex;
		flex-wrap: wrap;
		align-items: baseline;
		gap: var(--espace-3);
	}

	.variantes .mot {
		font-size: var(--taille-base);
	}

	.glose {
		font-family: var(--police-ui);
		font-size: var(--taille-xs);
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
</style>
