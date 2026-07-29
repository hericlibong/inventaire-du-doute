<script>
	// Carte d'une révision d'attribution. Deux variantes :
	// - « principale » : horizontale (vignette à gauche, contenu à droite),
	//   pour ouvrir chaque catégorie de la galerie ;
	// - « secondaire » : verticale (vignette en haut, contenu dessous), pour la
	//   grille à deux colonnes.
	// Vocabulaire imposé (brief datajournalisme 2026-07-15) : « Attribution
	// antérieure » / « Attribution actuelle » / « Consulter la notice sur POP → ».
	// On ne montre que du VERBATIM entre guillemets ; l'attribution antérieure
	// n'est jamais barrée ni présentée comme fausse. Une courte phrase de récit,
	// dérivée de la CATÉGORIE (jamais d'une interprétation inventée), aide à lire.
	import { lienPop } from '$lib/joconde.js';
	import { CATEGORIES, couleurCategorie } from '$lib/revisions-labels.js';
	import VignetteOeuvre from '$lib/VignetteOeuvre.svelte';

	// `cas` : un enregistrement de revisions.json (champ `cas`).
	// `variant` : 'secondaire' (défaut) | 'principale'.
	// `libelle`/`recit`/`couleur` : surcharges facultatives (utile pour le filtre
	// transversal « inverse », dont les cartes appartiennent à une autre catégorie).
	let {
		cas,
		variant = 'secondaire',
		avecEtiquette = true,
		libelle = null,
		recit = null,
		couleur = null
	} = $props();

	const teinte = $derived(couleur ?? couleurCategorie(cas.categorie));
	const libelleAffiche = $derived(libelle ?? cas.libelle);
	const recitAffiche = $derived(recit ?? CATEGORIES[cas.categorie]?.phraseCarte ?? '');
	const href = $derived(lienPop(cas.reference));
</script>

<article class="carte {variant}" style={`border-left-color:${teinte}`}>
	<div class="media">
		<VignetteOeuvre image={cas.image} {href} titre={cas.titre} />
	</div>

	<div class="corps">
		{#if avecEtiquette}
			<span class="etiquette" style={`color:${teinte}`}>{libelleAffiche}</span>
		{/if}

		<h3 class="titre">{cas.titre ?? 'Sans titre'}</h3>
		<p class="lieu">{cas.musee}{#if cas.ville} · {cas.ville}{/if}</p>

		<div class="attributions">
			<div class="attr anterieure">
				<span class="role">Attribution antérieure</span>
				<span class="verbatim">«&nbsp;{cas.ancienne_brut}&nbsp;»</span>
			</div>
			<div class="transition" aria-hidden="true">↓</div>
			<div class="attr actuelle">
				<span class="role">Attribution actuelle</span>
				<span class="verbatim">«&nbsp;{cas.auteur_brut}&nbsp;»</span>
			</div>
		</div>

		{#if recitAffiche}
			<p class="recit">{recitAffiche}</p>
		{/if}

		<a class="lien-pop" {href} target="_blank" rel="noopener">Consulter la notice sur POP&nbsp;→</a>
	</div>
</article>

<style>
	.carte {
		background: #fff;
		border: 1px solid var(--couleur-trait);
		border-left: 3px solid var(--couleur-revision);
		border-radius: 5px;
		padding: 1rem 1.1rem;
	}

	/* Variante verticale : vignette en haut, contenu dessous. */
	.carte.secondaire {
		display: flex;
		flex-direction: column;
		gap: 0.75rem;
	}

	/* Variante horizontale : vignette à gauche, contenu à droite. */
	.carte.principale {
		display: grid;
		grid-template-columns: minmax(12rem, 17rem) 1fr;
		gap: 1.5rem;
		align-items: start;
	}

	.corps {
		display: flex;
		flex-direction: column;
		gap: 0.5rem;
		min-width: 0;
	}

	.etiquette {
		font-size: 0.78rem;
		font-weight: 600;
	}

	/* Titres souvent en capitales dans la base : corps modéré (comme OeuvresMaitre). */
	.titre {
		margin: 0;
		font-family: var(--police-titre);
		font-size: 1.05rem;
		font-weight: 600;
		line-height: 1.3;
	}

	.carte.principale .titre {
		font-size: 1.25rem;
	}

	.lieu {
		margin: 0;
		font-size: 0.9rem;
		color: var(--couleur-encre-douce);
	}

	.attributions {
		display: flex;
		flex-direction: column;
		gap: 0.2rem;
		margin-top: 0.15rem;
	}

	.attr {
		display: flex;
		flex-direction: column;
	}

	.role {
		font-size: 0.72rem;
		text-transform: uppercase;
		letter-spacing: 0.03em;
		color: var(--couleur-encre-douce);
	}

	.verbatim {
		font-size: 1rem;
	}

	/* L'antérieure est un peu plus discrète, sans être barrée ni dévalorisée. */
	.attr.anterieure .verbatim {
		color: var(--couleur-encre-douce);
	}

	.attr.actuelle .verbatim {
		color: var(--couleur-encre);
	}

	.transition {
		color: var(--couleur-revision);
		font-size: 1.05rem;
		line-height: 1;
		margin: 0.1rem 0;
	}

	.recit {
		margin: 0.1rem 0 0;
		font-size: 0.9rem;
		font-style: italic;
		color: var(--couleur-encre-douce);
	}

	.lien-pop {
		margin-top: 0.2rem;
		font-size: 0.9rem;
		color: var(--couleur-accent);
		text-decoration: none;
	}

	.lien-pop:hover {
		text-decoration: underline;
	}

	@media (max-width: 640px) {
		.carte.principale {
			grid-template-columns: 1fr;
			gap: 0.75rem;
		}
	}
</style>
