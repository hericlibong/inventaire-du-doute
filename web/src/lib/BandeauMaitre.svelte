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

<!-- Sans portrait, la vignette disparaît et le texte prend la largeur : ni image de
     remplacement, ni mention d'absence. Décision du 2026-08-06 — une silhouette
     dessinée ou une œuvre posée à l'emplacement du visage affirmerait, sur la fiche
     d'un artiste dont les œuvres ne lui sont justement PAS directement attribuées,
     ce que tout le texte refuse d'affirmer. -->
<div class="bandeau" class:sans-portrait={!portrait}>
	{#if portrait}
		<div class="bandeau-portrait">
			<PortraitMaitre {maitre} {portrait} />
		</div>
	{/if}

	<div class="bandeau-titre">
		<!-- Pont de nom (2026-07-22) : le titre porte le nom courant, suivi du nom
		     d'état civil quand il diffère — c'est celui que le lecteur retrouvera,
		     à l'envers, sur les notices de l'onglet « Œuvres »
		     (« BUONARROTI Michelangelo (attribué à) »). -->
		<h2>{maitre.nom}{#if nomCivilMaitre(maitre.nom)}{' '}<span class="nom-civil"
				>({nomCivilMaitre(maitre.nom)})</span
			>{/if}</h2>
	</div>

	<div class="bandeau-texte">
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
	/* Colonne du portrait ramenée de 16 à 13 rem le 2026-08-08 (phase 3).
	   Le portrait et sa légende fixaient toute la hauteur du bandeau : le texte, à
	   droite, s'arrêtait 76 px plus haut et laissait un vide, et le départ des
	   onglets dépendait de l'image et non du contenu. Resserrée, la colonne de
	   gauche devient la plus courte : c'est le TEXTE qui commande la hauteur, et le
	   bandeau se termine sur le contenu. Le portrait garde sa présence — il n'est
	   pas ramené au rang de vignette. */
	.bandeau {
		display: grid;
		grid-template-columns: 14.5rem minmax(0, 36rem);
		/* Trois zones plutôt que deux blocs : le NOM est une zone à lui seul. Sur
		   ordinateur il occupe la colonne de droite, au-dessus des informations ;
		   sur mobile il vient se placer À CÔTÉ du portrait, et les informations
		   reprennent dessous sur toute la largeur. */
		grid-template-areas:
			'portrait titre'
			'portrait texte';
		justify-content: start;
		gap: 0 var(--espace-5);
		align-items: start;
		margin-top: var(--espace-2);
	}

	.bandeau-titre {
		grid-area: titre;
	}

	.bandeau-texte {
		grid-area: texte;
	}

	/* Sans portrait, le texte occupe la largeur des deux colonnes réunies
	   (16 + 34 + la gouttière) : la composition garde son empreinte, la fiche ne
	   saute pas d'un artiste à l'autre, et aucune colonne ne reste vide. */
	.bandeau.sans-portrait {
		grid-template-columns: minmax(0, 50rem);
		grid-template-areas:
			'titre'
			'texte';
	}

	.bandeau-portrait {
		grid-area: portrait;
		width: 14.5rem;
		max-width: 100%;
		/* Le haut de l'image est aligné sur la PREMIÈRE LIGNE du nom, et non sur le
		   haut de sa boîte : une capitale de 3 rem laisse au-dessus d'elle un blanc
		   d'interligne, et sans cette correction le portrait paraît monter plus haut
		   que le titre. */
		margin-top: 0.35rem;
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
		   58 signes.
		   `break-word` et NON `anywhere` (corrigé le 2026-08-06) : `anywhere`
		   autorise la coupure au milieu d'un mot dès qu'elle arrange la mise en
		   page. Le nom d'état civil, insécable, ne trouvait pas sa place et
		   faisait casser le nom lui-même — « Charles Norman / d ». `break-word`
		   ne coupe un mot que s'il ne tient pas seul sur une ligne. */
		overflow-wrap: break-word;
	}

	/* Ligne d'identité (qui, époque) quand elle est écrite — editorial-maitres.js. */
	/* Le nom d'état civil accompagne le titre sans le concurrencer : même ligne,
	   corps plus petit, encre atténuée. */
	.nom-civil {
		/* L'espace est un VRAI caractère, écrit `{' '}` dans le balisage. Une marge
		   gauche faisait office d'espace, mais une marge ne se résorbe pas en fin
		   de ligne : quand le nom d'état civil passait à la ligne suivante, il
		   partait décalé de quelques pixels vers la droite (2026-08-06). */
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

	/* Bandeau étroit (2026-08-08) : le portrait et le NOM passent côte à côte, et les
	   informations reprennent dessous sur toute la largeur.
	   Auparavant tout s'empilait : un portrait pleine largeur, sa légende, puis le
	   nom — le lecteur descendait sur près de 400 px avant de savoir de qui il
	   s'agissait, et les onglets arrivaient encore plus bas. Le seuil porte sur la
	   largeur RÉELLE de la fiche (conteneur de requête défini par la fiche parente). */
	@container (max-width: 38rem) {
		.bandeau {
			grid-template-columns: 9rem minmax(0, 1fr);
			grid-template-areas:
				'portrait titre'
				'texte texte';
			gap: 0 var(--espace-4);
		}

		.bandeau.sans-portrait {
			grid-template-columns: 1fr;
			grid-template-areas:
				'titre'
				'texte';
		}

		.bandeau-portrait {
			width: 9rem;
			justify-self: start;
			margin-top: 0.2rem;
		}

		/* Le nom partage la ligne : il descend d'un cran dans l'échelle pour tenir
		   sans compression ni césure sauvage. Il reste le plus grand de la fiche. */
		h2 {
			font-size: var(--taille-xl);
		}

		/* Les informations démarrent sous la ligne portrait + nom, jamais collées à
		   elle. */
		.bandeau-texte {
			margin-top: var(--espace-3);
		}
	}
</style>
