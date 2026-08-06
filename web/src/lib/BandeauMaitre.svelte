<script>
	// « La scène du maître » (docs/charte-graphique.md §5) : portrait + court PORTRAIT
	// ÉDITORIAL fondé sur les données. Refonte du 2026-07-23 : le bandeau répond à UNE
	// seule question — « quelle est l'ampleur du phénomène pour cet artiste ? ». La
	// répartition des mentions (quelle formule domine, dans quelle proportion) a QUITTÉ
	// le bandeau : elle appartient au seul graphique, qui ne doit plus la raconter deux
	// fois. Le bandeau garde donc, dans cet ordre :
	//   1. le nom de l'artiste (le plus grand), avec le pont vers son nom Joconde ;
	//   2. la courte bio factuelle ;
	//   3. le volume d'œuvres concernées et le nombre de musées ;
	//   4. le repère de contexte, en registre secondaire.
	// Les nombres vivent DANS les phrases : ni compteur, ni carte, ni KPI.
	//
	// Vocabulaire public : « œuvres associées à son nom » — jamais « œuvres de X »,
	// puisqu'elles ne lui sont précisément PAS directement attribuées. L'unité technique
	// reste la notice Joconde, expliquée en page Méthode (cadrage 2026-07-19/20).
	//
	// Toutes les valeurs viennent d'artistes.json (aucune écrite à la main par artiste).
	import PortraitMaitre from '$lib/PortraitMaitre.svelte';
	import { nombre } from '$lib/joconde.js';
	import { bioMaitre, nomCivilMaitre } from '$lib/editorial-maitres.js';

	let { maitre, portrait } = $props();

	// Espace des milliers VISIBLE et insécable : l'espace fine de toLocaleString (U+202F)
	// ne se voit pas dans Spectral → espace insécable normale (U+00A0), localement.
	const fr = (n) => nombre(n).replace(/[\u202f\u00a0\s]/g, '\u00a0');

	// Total de RÉFÉRENCE = attributions directes + formulations prudentes (propre + doute).
	// Il n'inclut PAS les copies « d'après » ni les catégories exclues par le pipeline :
	// d'où « copies mises à part » dans la phrase de contexte (voir page Méthode). Le
	// nombre de musées est celui des seules notices prudentes (maitre.nb_musees_doute).
	const totalNom = $derived(maitre.propre + maitre.doute);
	const pctDoute = $derived(totalNom ? Math.round((maitre.doute / totalNom) * 100) : 0);
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

		<!-- AMPLEUR : le volume d'œuvres concernées, et où elles sont conservées.
		     Ni mention dominante, ni proportion : cela appartient au graphique. -->
		<p class="recit">
			<strong class="donnee">{fr(maitre.doute)}&nbsp;œuvres</strong> sont associées à son
			nom sans lui être directement attribuées.
			{#if maitre.nb_musees_doute > 1}
				Elles sont réparties dans
				<strong class="donnee">{fr(maitre.nb_musees_doute)}&nbsp;musées</strong>.
			{:else if maitre.nb_musees_doute === 1}
				Elles sont toutes conservées dans un même musée.
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
		/* Prévoir les noms longs, comme le panneau de la carte le fait déjà
		   (charte §8). Le plus long du corpus, avec son nom d'état civil, fait
		   58 signes. */
		overflow-wrap: anywhere;
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
		/* Insécable sur grand écran seulement : « (Michelangelo Buonarroti) » se
		   lit mal coupé en deux. Sur mobile, la coupure vaut mieux que le
		   débordement — mesuré le 2026-08-06 : la page partait à 569 px de large
		   dans une fenêtre de 390 px, et le défaut existait déjà avant ce lot
		   (Michel-Ange à 407 px). */
		white-space: nowrap;
	}

	@media (max-width: 760px) {
		.nom-civil {
			white-space: normal;
		}
	}

	.bio {
		margin: var(--espace-1) 0 0;
		color: var(--couleur-encre-douce);
		font-style: italic;
	}

	/* Ampleur du phénomène : texte courant, le nom reste l'élément dominant. Le
	   volume et les musées sont les seules données du bandeau. */
	.recit {
		margin: var(--espace-4) 0 0;
		font-size: var(--taille-m);
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
	}
</style>
