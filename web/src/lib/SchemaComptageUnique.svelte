<script>
	// Schéma nº 3 de la page « Méthode » (palier 4, 2026-07-31) : la règle de
	// comptage des profils d'artistes — une notice peut nommer le même artiste
	// deux fois, avec deux mentions différentes ; elle n'est comptée qu'une fois,
	// sous la plus prudente. Cas RÉEL (notice M0332004170, Besançon), celui-là
	// même qui a servi à écrire la règle (src/build_artistes.py, _famille_retenue).
	// Vocabulaire public : « mention », jamais le mot de code interne.
</script>

<figure class="schema">
	<p class="titre-schema">Une notice qui nomme deux fois le même artiste</p>

	<div class="notice">
		<span class="etiquette">Auteur</span>
		<ul class="mentions">
			<li class="prudente">
				<span class="pastille" style="--teinte: var(--forme-point-interrogation)"></span>
				<span class="mot">VOUET Simon (?)</span>
				<span class="marque">retenue</span>
			</li>
			<li>
				<span class="pastille" style="--teinte: var(--forme-atelier)"></span>
				<span class="mot">VOUET Simon (atelier, dessinateur)</span>
			</li>
		</ul>
	</div>

	<p class="regle">
		<span class="fleche" aria-hidden="true">↓</span>
		Comptée <strong>une seule fois</strong>, sous la mention la plus prudente&nbsp;: le
		point d’interrogation l’emporte. Sans cette règle, la même œuvre serait comptée deux
		fois dans le profil de l’artiste.
	</p>

	<figcaption>
		Notice réelle du musée des beaux-arts et d’archéologie de Besançon
		(référence M0332004170), reproduite telle quelle.
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

	.notice {
		display: flex;
		flex-wrap: wrap;
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
		align-self: start;
	}

	.mentions {
		list-style: none;
		margin: 0;
		padding: 0;
		display: grid;
		gap: var(--espace-2);
		min-width: 0;
	}

	.mentions li {
		display: flex;
		flex-wrap: wrap;
		align-items: baseline;
		gap: var(--espace-2);
	}

	/* Pastille = couleur stable de la mention (tokens.css). Renfort, jamais la
	   seule information : le mot « retenue » dit la même chose en toutes lettres. */
	.pastille {
		width: 0.55rem;
		height: 0.55rem;
		border-radius: 50%;
		background: var(--teinte);
		flex: none;
	}

	.mot {
		font-family: var(--police-titre);
		font-size: var(--taille-base);
		color: var(--couleur-encre-douce);
	}

	.prudente .mot {
		color: var(--couleur-encre);
	}

	.marque {
		font-family: var(--police-ui);
		font-size: var(--taille-xs);
		letter-spacing: 0.06em;
		text-transform: uppercase;
		color: var(--couleur-accent);
	}

	.regle {
		margin: var(--espace-4) 0 0;
		font-family: var(--police-ui);
		font-size: var(--taille-s);
		line-height: 1.6;
	}

	.fleche {
		color: var(--couleur-encre-douce);
		margin-right: var(--espace-2);
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
