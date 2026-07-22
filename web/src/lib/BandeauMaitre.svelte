<script>
	// « La scène du maître » (docs/charte-graphique.md §5) : portrait + court PORTRAIT
	// ÉDITORIAL fondé sur les données. Refonte du 2026-07-20 (decisions.md) : la pile
	// de compteurs (grand nombre + %, puis phrases techniques) est abandonnée au profit
	// d'un seul bloc de lecture. Hiérarchie, dans cet ordre :
	//   1. le nom de l'artiste (élément le plus grand) ;
	//   2. la mention la plus fréquente — l'enseignement que le graphique détaille ensuite ;
	//   3. le récit chiffré (volume concerné, part de la mention, nombre de musées) ;
	//   4. le repère méthodologique, en registre secondaire.
	// Les nombres vivent DANS les phrases : ni compteur, ni carte, ni KPI.
	//
	// Vocabulaire public : « œuvres associées à son nom » — jamais « œuvres de X »,
	// puisqu'elles ne lui sont précisément PAS directement attribuées. L'unité technique
	// reste la notice Joconde, expliquée en page Méthode (cadrage 2026-07-19/20).
	//
	// Toutes les phrases sont générées depuis artistes.json (aucun texte écrit à la main
	// par artiste, aucune valeur en dur) : accords, égalités entre mentions, mention
	// intégralement portée par la couche de libellés publics (familles-public.js).
	import PortraitMaitre from '$lib/PortraitMaitre.svelte';
	import { nombre } from '$lib/joconde.js';
	import { FAMILLE_PUBLIC, ORDRE_FAMILLES } from '$lib/familles-public.js';
	import { bioMaitre, nomCivilMaitre } from '$lib/editorial-maitres.js';

	let { maitre, portrait } = $props();

	// Espace des milliers VISIBLE et insécable : l'espace fine de toLocaleString (U+202F)
	// ne se voit pas dans Spectral → espace insécable normale (U+00A0), localement.
	const fr = (n) => nombre(n).replace(/[\u202f\u00a0\s]/g, '\u00a0');

	// Total de RÉFÉRENCE = attributions directes + formulations prudentes (propre + doute).
	// Il n'inclut PAS les copies « d'après » ni les catégories exclues par le pipeline :
	// d'où « copies mises à part » dans la phrase de contexte (voir page Méthode).
	const totalNom = $derived(maitre.propre + maitre.doute);
	const pctDoute = $derived(totalNom ? Math.round((maitre.doute / totalNom) * 100) : 0);

	// Mention(s) la (les) plus fréquente(s). En cas d'ÉGALITÉ EXACTE, on garde toutes les
	// familles au maximum, ordonnées par ORDRE_FAMILLES (jamais l'ordre accidentel des
	// données) : aucune n'est choisie arbitrairement.
	const dominance = $derived.by(() => {
		const max = Math.max(...maitre.familles.map((f) => f.notices));
		const codes = maitre.familles
			.filter((f) => f.notices === max)
			.map((f) => f.code)
			.sort((a, b) => ORDRE_FAMILLES.indexOf(a) - ORDRE_FAMILLES.indexOf(b));
		return { codes, notices: max, toutes: max === maitre.doute };
	});

	// Énumération française des mentions citées : la première garde sa majuscule (elle
	// ouvre la phrase), les suivantes passent en bas de casse — « "Attribué à" et
	// "de son école" sont les mentions les plus fréquentes. »
	const bas = (s) => s.charAt(0).toLowerCase() + s.slice(1);
	const citations = $derived(
		dominance.codes.map((c, i) => {
			const t = FAMILLE_PUBLIC[c].citation;
			return i === 0 ? t : bas(t);
		})
	);
	const sep = (i, len) => (i === len - 1 ? '' : i === len - 2 ? ' et ' : ', ');
</script>

<div class="bandeau">
	<div class="bandeau-portrait">
		<PortraitMaitre {maitre} {portrait} />
	</div>

	<div class="bandeau-texte">
		<!-- Pont de nom (2026-07-22) : le titre porte le nom courant, suivi du nom
		     d'état civil quand il diffère — c'est celui que le lecteur retrouvera,
		     à l'envers, sur les notices de l'onglet « Œuvres »
		     (« BUONARROTI Michelangelo (attribué à) »). -->
		<h2>{maitre.nom}{#if nomCivilMaitre(maitre.nom)}<span class="nom-civil"
				>({nomCivilMaitre(maitre.nom)})</span
			>{/if}</h2>
		{#if bioMaitre(maitre.nom)}
			<p class="bio">{bioMaitre(maitre.nom)}</p>
		{/if}

		<!-- CONSTAT : la mention réellement la plus fréquente, égalités comprises. -->
		<p class="constat">
			{#each citations as c, i}«&nbsp;{c}&nbsp;»{sep(i, citations.length)}{/each}
			{citations.length === 1 ? 'est la mention la plus fréquente.' : 'sont les mentions les plus fréquentes.'}
		</p>

		<!-- RÉCIT CHIFFRÉ : les nombres intégrés aux phrases, jamais isolés. -->
		<p class="recit">
			{#if dominance.toutes}
				<!-- Toutes les œuvres concernées portent la même mention (aucune autre
				     famille) : « 80 … portent toutes cette mention » évite le doublon
				     « parmi les 80 …, 80 portent ». -->
				Les <strong class="donnee">{fr(maitre.doute)}&nbsp;œuvres</strong> associées à son
				nom sans lui être directement attribuées portent toutes cette mention.
			{:else}
				Parmi les <strong class="donnee">{fr(maitre.doute)}&nbsp;œuvres</strong> associées
				à son nom sans lui être directement attribuées,
				<strong class="donnee">{fr(dominance.notices)}</strong>
				{dominance.notices === 1 ? 'porte' : 'portent'}
				{citations.length === 1 ? 'cette mention' : 'chacune de ces mentions'}.
			{/if}
			{#if maitre.nb_musees_doute > 1}
				Ces œuvres sont réparties dans
				<strong class="donnee">{fr(maitre.nb_musees_doute)}&nbsp;musées</strong>.
			{:else if maitre.nb_musees_doute === 1}
				Ces œuvres sont toutes conservées dans un même musée.
			{/if}
		</p>

		<!-- REPÈRE méthodologique : registre secondaire, sans mise en évidence. -->
		<p class="repere">
			En contexte&nbsp;: {fr(maitre.doute)} sur {fr(totalNom)} œuvres rattachées à son
			nom, copies mises à part, soit {pctDoute}&nbsp;%.
		</p>
	</div>
</div>

<style>
	/* Portrait (largeur bornée, charte §5) à gauche, texte à droite ; gouttière
	   resserrée pour que l'image et le bloc éditorial forment une seule composition.
	   justify-content: start → le bloc reste calé à gauche, pas étalé. */
	.bandeau {
		display: grid;
		grid-template-columns: 16rem minmax(0, 34rem);
		justify-content: start;
		gap: var(--espace-5);
		align-items: start;
		margin-top: var(--espace-2);
	}

	.bandeau-portrait {
		width: 16rem;
		max-width: 100%;
	}

	.bandeau-texte {
		display: flex;
		flex-direction: column;
	}

	/* Le nom reste l'élément typographique le plus grand : aucun nombre ne doit le
	   concurrencer. */
	h2 {
		font-family: var(--police-titre);
		font-size: var(--taille-xxl);
		line-height: 1.02;
		letter-spacing: -0.015em;
		margin: 0;
	}

	/* Ligne d'identité (qui, époque) quand elle est écrite — editorial-maitres.js. */
	/* Le nom d'état civil accompagne le titre sans le concurrencer : même ligne,
	   corps plus petit, encre atténuée. */
	.nom-civil {
		/* l'espace vient d'ici : Svelte supprime celui du balisage */
		margin-left: 0.35em;
		font-size: 0.5em;
		font-weight: 400;
		letter-spacing: 0.01em;
		color: var(--couleur-encre-douce, #6b6459);
		white-space: nowrap;
	}

	.bio {
		margin: var(--espace-1) 0 0;
		color: var(--couleur-encre-douce);
		font-style: italic;
	}

	/* Deuxième niveau visuel : le constat éditorial, en Fraunces. Plus présent que
	   chacun des nombres, sans jamais atteindre le corps du nom. */
	.constat {
		margin: var(--espace-3) 0 0;
		font-family: var(--police-titre);
		font-size: 1.35rem;
		font-weight: 600;
		line-height: 1.3;
		letter-spacing: -0.005em;
		max-width: 30rem;
	}

	.recit {
		margin: var(--espace-3) 0 0;
		font-size: var(--taille-base);
		line-height: 1.65;
		max-width: 32rem;
	}

	/* Nombres légèrement soulignés DANS la phrase : poids supérieur, accent cobalt,
	   chiffres elzéviriens (fournis par Spectral) — jamais plus grands que le texte. */
	.donnee {
		font-weight: 600;
		color: var(--accent-cobalt);
		font-variant-numeric: oldstyle-nums;
		white-space: nowrap;
	}

	/* Repère méthodologique : registre secondaire, séparé par un filet fin. */
	.repere {
		margin: var(--espace-4) 0 0;
		padding-top: var(--espace-2);
		border-top: var(--filet);
		font-size: var(--taille-s);
		line-height: 1.5;
		color: var(--couleur-encre-douce);
		max-width: 32rem;
	}

	/* Bandeau étroit : une seule colonne — portrait puis texte, calés à gauche, même
	   ordre narratif. Le seuil porte sur la largeur RÉELLE de la fiche (conteneur de
	   requête défini par la fiche parente). */
	@container (max-width: 38rem) {
		.bandeau {
			grid-template-columns: 1fr;
			gap: var(--espace-4);
		}
		.bandeau-portrait {
			justify-self: start;
		}
		.constat {
			font-size: 1.25rem;
		}
	}
</style>
