<script>
	import { lienPop } from '$lib/joconde.js';
	import { FAMILLE_PUBLIC, ORDRE_FAMILLES, oeuvres } from '$lib/familles-public.js';

	// Vitrine « Œuvres » (décision 2026-07-11) : quelques cas concrets derrière
	// les points du graphique. Chaque entrée montre une œuvre réelle avec les MOTS
	// EXACTS publiés par son musée — l'extrait est la seule citation littérale de
	// l'application — et un lien vers sa fiche publique POP. Les exemples sont pris
	// automatiquement dans la base (les premiers rencontrés), pas choisis à la main :
	// règle documentée dans docs/methode-et-limites.md. Le code de forme vient de
	// l'export : le front ne re-parse JAMAIS les extraits.
	//
	// Direction B (2026-07-17) : composition éditoriale CONTINUE (entrées séparées
	// par des filets, pas une grille de cartes blanches). Les mots publiés par les
	// musées sont la matière : le verbatim est en tête de hiérarchie. Un emplacement
	// média est réservé par entrée pour de futures reproductions — jamais inventé.
	let { maitre } = $props();

	// Entrées dans l'ordre de l'axe du graphique. Kicker et pastille = les mêmes mots
	// et la même couleur que le point correspondant.
	const rang = (code) => ORDRE_FAMILLES.indexOf(code);
	const cartes = $derived(
		[...maitre.exemples]
			.sort((a, b) => rang(a.code) - rang(b.code))
			.map((ex) => ({
				...ex,
				header: FAMILLE_PUBLIC[ex.code].header,
				couleur: FAMILLE_PUBLIC[ex.code].couleur
			}))
	);

	// « musée, ville » en gérant les champs manquants de la base.
	const lieu = (ex) => [ex.musee, ex.ville].filter(Boolean).join(', ');
</script>

<section class="vitrine">
	<h3>Quelques œuvres derrière les points</h3>
	<p class="amorce">
		Quelques exemples issus des fiches Joconde, avec les mots publiés par les musées.
	</p>

	<ol class="entrees">
		{#each cartes as c (c.reference)}
			<li class="entree">
				<!-- Emplacement réservé pour une future reproduction (droits par œuvre à
				     clarifier) : jamais une image inventée. -->
				<div class="media" aria-hidden="true">
					<span>reproduction<br />non affichée</span>
				</div>
				<div class="corps">
					<p class="kicker">
						<span class="pastille" style="background: {c.couleur}"></span>{c.header}
					</p>
					<h4 class="titre">{c.titre ?? 'Sans titre'}</h4>
					{#if lieu(c)}<p class="lieu">{lieu(c)}</p>{/if}
					<p class="verbatim" style="border-left-color: {c.couleur}">«&nbsp;{c.extrait}&nbsp;»</p>
					<a class="lien-fiche" href={lienPop(c.reference)} target="_blank" rel="noopener">
						Voir la fiche publique sur POP&nbsp;→
					</a>
				</div>
			</li>
		{/each}
	</ol>

	<!-- Copies « d'après », à part : des copies assumées, pas des doutes. Hors gamme
	     du doute (couleur neutre), jamais mêlées aux entrées. -->
	<div class="bande-copie">
		<p class="copie-texte">
			À part&nbsp;: <strong>{oeuvres(maitre.copie)}</strong> «&nbsp;d'après
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

<style>
	.vitrine h3 {
		font-family: var(--police-titre);
		margin: 0 0 0.15rem;
		font-size: var(--taille-l);
	}

	.amorce {
		margin: 0 0 var(--espace-4);
		color: var(--couleur-encre-douce);
		font-size: var(--taille-s);
	}

	/* Liste continue : entrées séparées par un filet, pas des cartes détachées. */
	.entrees {
		list-style: none;
		margin: 0;
		padding: 0;
	}

	.entree {
		display: grid;
		grid-template-columns: 7rem 1fr;
		gap: var(--espace-5);
		padding: var(--espace-4) 0;
		border-top: var(--filet);
	}

	/* Emplacement média réservé : cadre neutre, pas une image. */
	.media {
		aspect-ratio: 4 / 5;
		background: var(--surface-carte);
		border: var(--filet);
		display: flex;
		align-items: center;
		justify-content: center;
		text-align: center;
	}

	.media span {
		font-family: var(--police-ui);
		font-size: 0.62rem;
		letter-spacing: 0.05em;
		text-transform: uppercase;
		line-height: 1.35;
		color: var(--couleur-trait);
	}

	.corps {
		min-width: 0;
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

	.pastille {
		width: 0.6rem;
		height: 0.6rem;
		border-radius: 50%;
		flex: none;
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

	.lien-fiche {
		font-family: var(--police-ui);
		font-size: var(--taille-s);
		color: var(--accent-cobalt);
		text-decoration: none;
		border-bottom: 1px solid transparent;
	}

	.lien-fiche:hover {
		border-bottom-color: var(--accent-cobalt);
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
			grid-template-columns: 5rem 1fr;
			gap: var(--espace-4);
		}
		.verbatim {
			font-size: 1.15rem;
		}
	}
</style>
