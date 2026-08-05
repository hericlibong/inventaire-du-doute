<script>
	// UNE NOTICE, DEUX MENTIONS (2026-08-05). Remplace le schéma encadré qui tenait
	// cette place depuis le 2026-07-31 : même notice, même règle, mais l'exemple
	// appartient maintenant à la lecture de la section — deux volets, « ce que la
	// notice écrit » puis « ce que le projet compte », sans carte autour.
	//
	// Cas RÉEL : la notice M0332004170 du musée des beaux-arts et d'archéologie de
	// Besançon, celle-là même qui a servi à écrire la règle (build_artistes.py,
	// _famille_retenue : le « ? » l'emporte, puis l'ordre canonique des familles).
	// Contrôlée le 2026-08-05 contre data/exports/web/oeuvres/simon-vouet.json
	// (référence, titre, musée, ville, mention retenue = point_interrogation) et
	// contre POP. La valeur du champ est reproduite telle quelle, point-virgule
	// compris : c'est ainsi que Joconde sépare deux segments d'auteur.
	const POP = 'https://pop.culture.gouv.fr/notice/joconde/M0332004170';
</script>

<div class="exemple">
	<p class="titre">Une notice, deux mentions pour Simon Vouet</p>
	<p class="oeuvre">Femme assise dans les nuées tenant une palme</p>
	<p class="lieu">
		musée des beaux-arts et d’archéologie de Besançon · référence M0332004170
	</p>

	<div class="volets">
		<div class="volet">
			<p class="entete">Ce que la notice écrit</p>
			<p class="etiquette">Champ Auteur</p>
			<p class="valeur">
				VOUET Simon <span class="reserve interro">(?)</span>&nbsp;;
				VOUET Simon <span class="reserve atelier">(atelier, dessinateur)</span>
			</p>
		</div>

		<p class="fleche" aria-hidden="true">→</p>

		<div class="volet">
			<p class="entete">Ce que le projet compte</p>
			<ul class="resultat">
				<li><strong>Une</strong> notice dans le total national</li>
				<li><strong>Une</strong> notice dans le profil de Simon Vouet</li>
				<li>Mention retenue&nbsp;: nom suivi d’un point d’interrogation</li>
			</ul>
		</div>
	</div>

	<p class="renvoi">
		<a href={POP} target="_blank" rel="noopener">Consulter la notice sur POP&nbsp;→</a>
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
		color: var(--couleur-encre-douce);
	}

	.oeuvre {
		margin: var(--espace-2) 0 0;
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

	/* Les deux temps de l'exemple, séparés par une flèche : ce qui est écrit, puis
	   ce qui est compté. Un filet vertical tient lieu de cadre — l'exemple reste
	   dans la colonne de texte. */
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
		margin: 0 0 var(--espace-2);
		font-family: var(--police-ui);
		font-size: var(--taille-xs);
		color: var(--couleur-encre-douce);
	}

	.etiquette {
		margin: 0;
		font-family: var(--police-ui);
		font-size: var(--taille-xs);
		letter-spacing: 0.06em;
		text-transform: uppercase;
		color: var(--couleur-encre-douce);
	}

	.valeur {
		margin: var(--espace-1) 0 0;
		font-family: var(--police-titre);
		line-height: 1.5;
	}

	/* Chaque réserve dans la couleur de sa famille — celles du site, partout. */
	.interro {
		color: var(--forme-point-interrogation);
	}

	.atelier {
		color: var(--forme-atelier);
	}

	.fleche {
		margin: 0;
		align-self: center;
		font-size: var(--taille-l);
		color: var(--couleur-encre-douce);
	}

	.resultat {
		list-style: none;
		margin: 0;
		padding: 0;
		font-size: var(--taille-s);
		line-height: 1.5;
	}

	.resultat li + li {
		margin-top: var(--espace-2);
	}

	.renvoi {
		margin: var(--espace-3) 0 0;
		font-family: var(--police-ui);
		font-size: var(--taille-xs);
	}

	.renvoi a {
		color: var(--accent-cobalt);
		text-decoration: none;
		border-bottom: 1px solid transparent;
	}

	.renvoi a:hover,
	.renvoi a:focus-visible {
		border-bottom-color: var(--accent-cobalt);
	}

	/* En colonne étroite, les deux volets s'empilent et la flèche se redresse. */
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
