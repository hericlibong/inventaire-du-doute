<script>
	import { lienPop } from '$lib/joconde.js';
	import { FAMILLE_PUBLIC, ORDRE_FAMILLES, oeuvres } from '$lib/familles-public.js';

	// Vitrine « Œuvres » (décision 2026-07-11) : quelques cas concrets derrière
	// les points du graphique. Chaque carte montre une œuvre réelle avec les MOTS
	// EXACTS publiés par son musée — l'extrait est la seule citation littérale de
	// l'application (le tooltip du graphique, lui, affiche une mention reconstruite)
	// — et un lien vers sa fiche publique POP. Les exemples sont pris
	// automatiquement dans la base (les premiers rencontrés), pas choisis à la
	// main : règle documentée dans docs/methode-et-limites.md. Le code de forme
	// vient de l'export : le front ne re-parse JAMAIS les extraits.
	let { maitre } = $props();

	// Cartes dans l'ordre de l'axe du graphique (l'export suit l'ordre de
	// l'échelle, l'axe intercale école/atelier différemment → on retrie). Kicker
	// et pastille = les mêmes mots et la même couleur que le point correspondant.
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

	<div class="cartes">
		{#each cartes as c (c.reference)}
			<article class="carte">
				<p class="kicker">
					<span class="pastille" style="background: {c.couleur}"></span>{c.header}
				</p>
				<p class="titre">{c.titre ?? 'Sans titre'}</p>
				{#if lieu(c)}<p class="lieu">{lieu(c)}</p>{/if}
				<p class="verbatim">«&nbsp;{c.extrait}&nbsp;»</p>
				<a class="lien-fiche" href={lienPop(c.reference)} target="_blank" rel="noopener">
					Voir la fiche publique →
				</a>
			</article>
		{/each}
	</div>

	<!-- Copies « d'après », à part : des copies assumées, pas des doutes. Bloc
	     distinct (couleur propre, hors gamme du doute), jamais mêlé aux cartes. -->
	<div class="bande-copie">
		<p class="copie-texte">
			À part : <strong>{oeuvres(maitre.copie)}</strong> «&nbsp;d'après
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
		margin: 1.5rem 0 0.25rem;
		font-size: 1.05rem;
	}

	.amorce {
		margin: 0 0 1rem;
		color: var(--couleur-encre-douce);
		font-size: 0.9rem;
	}

	/* Vitrine en petits blocs, pas une table : cartes fluides, 2 colonnes max. */
	.cartes {
		display: grid;
		grid-template-columns: repeat(auto-fill, minmax(15rem, 1fr));
		gap: 0.9rem;
	}

	.carte {
		background: #fff;
		border: 1px solid var(--couleur-trait);
		border-radius: 4px;
		padding: 0.75rem 0.85rem;
		display: flex;
		flex-direction: column;
		gap: 0.35rem;
	}

	/* Kicker = le même mot et la même couleur que le point du graphique. La
	   couleur est portée par la pastille (pas par le texte : certaines teintes
	   claires manqueraient de contraste sur fond clair). */
	.kicker {
		margin: 0;
		font-size: 0.72rem;
		font-weight: 600;
		letter-spacing: 0.06em;
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

	/* Titres souvent en capitales dans la base : corps modéré pour qu'ils ne
	   crient pas. On les affiche tels que publiés, on ne réécrit rien. */
	.titre {
		margin: 0;
		font-weight: 600;
		font-size: 0.9rem;
		line-height: 1.35;
	}

	.lieu {
		margin: 0;
		font-size: 0.8rem;
		color: var(--couleur-encre-douce);
	}

	/* Le verbatim est la pièce centrale de la carte : les mots exacts du musée. */
	.verbatim {
		margin: 0.25rem 0 0;
		font-family: var(--police-titre);
		font-size: 1rem;
		line-height: 1.4;
	}

	.lien-fiche {
		margin-top: auto;
		padding-top: 0.4rem;
		font-size: 0.8rem;
		color: var(--couleur-accent);
	}

	.bande-copie {
		margin-top: 1.25rem;
		padding: 0.75rem 1rem;
		border-left: 4px solid var(--couleur-copie);
		background: rgba(74, 107, 122, 0.07);
		font-size: 0.95rem;
	}

	.copie-texte {
		margin: 0;
	}

	.copie-exemple {
		margin: 0.4rem 0 0;
		font-size: 0.8rem;
		color: var(--couleur-encre-douce);
	}

	.copie-exemple a {
		color: inherit;
	}

	.mention-pop {
		margin: 1rem 0 0;
		font-size: 0.75rem;
		color: var(--couleur-encre-douce);
	}
</style>
