<script>
	// « Méthode et limites » (architecture §3) : page unique et structurée qui
	// regroupe les limites du projet, au même rang que le récit (règle CLAUDE.md :
	// les limites sont affichées, pas cachées). Éditoriale et accessible — ni doc
	// technique, ni FAQ, ni suite de cartes. Cinq sections : Périmètre · Construction
	// des données · Lire les chiffres · Limites · Sources et droits.
	import { nombre } from '$lib/joconde.js';

	let { data } = $props();
	const n = data.niveaux;
	const prov = data.provenance;

	// Chiffres, tous issus des exports (jamais saisis à la main).
	const nbNoms = data.artistes.artistes.length;
	const douteDansListe = data.vue.totaux.doute_notices_liste;
	// Registre des candidats : l'engagement de publier qui a été examiné, et
	// avec quel résultat (decisions.md 2026-07-21 quater, décision 4).
	const nbCandidats = data.registre.formes_au_seuil;
	const nbRetenus = data.registre.retenues;
	const nbEcartes = data.registre.ecartees;
	const nbAInstruire = data.registre.a_instruire;
	const dApres = n.familles.d_apres.notices; // 22 564 (copies « d'après »)
	const copiesTotal = n.copie; // 22 624 (catégorie copie, dédupliquée)
	const pct = (v) => (v * 100).toLocaleString('fr-FR', { maximumFractionDigits: 1 });
	const go = (o) => (o / 1e9).toLocaleString('fr-FR', { maximumFractionDigits: 2 });

	const sommaire = [
		['perimetre', 'Périmètre'],
		['donnees', 'Construction des données'],
		['lire', 'Lire les chiffres'],
		['limites', 'Limites'],
		['sources', 'Sources et droits']
	];
</script>

<div class="page">
<header class="tete">
	<p class="kicker">Méthode et limites</p>
	<h1>Ce que les chiffres disent, et ne disent pas</h1>
	<p class="chapo">
		Cette page dit comment le projet lit la base Joconde, ce qu'il compte, et ce qu'il
		ne prétend pas savoir. Elle est publiée au même rang que le reste&nbsp;: les limites
		font partie du récit.
	</p>
	<p class="prudence">
		Le projet reprend les formulations publiées par les musées&nbsp;; il ne réattribue
		aucune œuvre.
	</p>
</header>

<!-- Deux zones : sommaire en rail (collant sur ordinateur) + contenu. La ligne de
     proximité n'est PAS imposée ici : elle n'expliquerait rien (Méthode = texte,
     filets, chiffres et sources). -->
<div class="grille">
	<nav class="sommaire" aria-label="Sections de la page">
		<ol>
			{#each sommaire as [ancre, titre], i (ancre)}
				<li><a href="#{ancre}"><span class="num">{i + 1}</span>{titre}</a></li>
			{/each}
		</ol>
	</nav>

	<div class="contenu">
<!-- 1. Périmètre ------------------------------------------------------------- -->
<section id="perimetre">
	<h2>Périmètre</h2>
	<p>
		<strong>Joconde</strong> est le catalogue collectif des collections des musées de
		France, publié par le ministère de la Culture. Il rassemble plus d'un million de
		notices — une notice par objet — décrites par les musées eux-mêmes. Le projet en
		lit une seule chose&nbsp;: la manière dont les musées écrivent qu'ils ne sont
		<em>pas certains</em> de l'auteur d'une œuvre.
	</p>
	<p>
		On appelle ici <strong>formulation prudente</strong> une notice où le nom d'un
		artiste est présent, mais accompagné d'une réserve&nbsp;: «&nbsp;attribué à&nbsp;»,
		«&nbsp;atelier de&nbsp;», «&nbsp;école de&nbsp;», «&nbsp;entourage de&nbsp;»,
		«&nbsp;suiveur de&nbsp;», «&nbsp;à la manière de&nbsp;», «&nbsp;dans le genre
		de&nbsp;», ou un simple «&nbsp;?&nbsp;» après le nom. Le projet repère ces formules,
		les compte et les classe — il n'en invente aucune.
	</p>
</section>

<!-- 2. Construction des données --------------------------------------------- -->
<section id="donnees">
	<h2>Construction des données</h2>
	<p>
		La détection est <strong>lexicale</strong>&nbsp;: elle s'appuie sur une convention
		d'écriture des musées, le qualificatif noté entre parenthèses dans le champ auteur
		(«&nbsp;LE BRUN Charles (attribué)&nbsp;», «&nbsp;(école)&nbsp;», «&nbsp;(?)&nbsp;»).
		En lisant toute la base, on trouve <strong>{nombre(n.doute_total)}</strong> notices
		porteuses d'au moins une formulation prudente, soit {pct(n.taux_doute_avec_auteur)}&nbsp;%
		des notices où un auteur est renseigné.
	</p>
	<p>
		Le repérage a été <strong>vérifié à la main</strong>&nbsp;: un échantillon de 206
		notices a été jugé une à une (vrai / faux / incertain), ce qui a permis de mesurer
		les fausses détections, puis de reformuler le lexique. Ce lexique est versionné et
		public&nbsp;; sa version est indiquée plus bas.
	</p>
	<!-- Ancre visée par le lien « Pourquoi ces N artistes ? » de la rubrique
	     « Explorer les maîtres » (2026-07-20) : le détail du seuil a quitté
	     l'introduction de la rubrique, il vit ici. -->
	<p id="les-maitres">
		Une partie du site se concentre sur <strong>{nombre(nbNoms)} noms</strong> de
		référence. Le critère est explicite&nbsp;: un artiste connu <em>et</em> au moins
		dix notices portant une formulation prudente (copies exclues), une fois le nom bien
		isolé. Ce n'est <strong>pas un palmarès des plus grands</strong>&nbsp;: c'est un
		seuil, choisi pour avoir assez de matière à montrer. Ces {nombre(nbNoms)} noms
		réunissent {nombre(douteDansListe)} des formulations prudentes.
	</p>
	<p>
		<strong>Cette liste n'est pas close, et elle se vérifie.</strong> Tous les noms qui
		atteignent le seuil ont été relevés — ils sont {nombre(nbCandidats)} — puis examinés
		un par un. Chacun porte un état&nbsp;: retenu, écarté avec sa raison, ou
		<em>encore à examiner</em>. Un nom encore à examiner n'est pas un nom rejeté&nbsp;:
		c'est un nom dont la vérification n'a pas été faite. Aujourd'hui, {nombre(nbRetenus)}
		formes d'écriture sont rattachées aux {nombre(nbNoms)} artistes retenus,
		{nombre(nbEcartes)} sont écartées parce qu'il ne s'agit pas d'une personne
		— une manufacture, une imprimerie, «&nbsp;anonyme&nbsp;», ou une mention qui ne porte
		aucun nom d'auteur — et {nombre(nbAInstruire)} restent à examiner. La liste
		s'agrandira par lots.
	</p>
	<p>
		Rattacher une formule au bon artiste demande de la prudence, car le nom est cherché
		dans un texte libre. Trois pièges ont été corrigés en chemin&nbsp;: les
		<strong>fausses correspondances par sous-chaîne</strong> (une œuvre de Serodine ne
		doit pas être rattachée à Rodin) — réglées en n'acceptant que le mot entier&nbsp;;
		les mentions de <strong>nationalité</strong> («&nbsp;école allemande&nbsp;») qui ne
		sont pas un doute sur un artiste et sont écartées&nbsp;; enfin le doute écrit
		<strong>hors des parenthèses</strong>, qu'il fallait aussi savoir lire. Le piège le plus
		coûteux était ailleurs&nbsp;: des <strong>homonymes</strong>. Sous «&nbsp;Michel-Ange&nbsp;»,
		les musées ont aussi rangé Corneille Michel-Ange, peintre lyonnais du XVII<sup>e</sup>
		siècle&nbsp;; sous «&nbsp;Raphaël&nbsp;», une cinquantaine de personnes qui le portent
		comme prénom. Chaque artiste est donc séparé nommément de ses homonymes et de sa
		famille — le fils du Tintoret n'est pas le Tintoret.
	</p>
</section>

<!-- 3. Lire les chiffres ----------------------------------------------------- -->
<section id="lire">
	<h2>Lire les chiffres</h2>
	<p>
		<strong>Les formules peuvent se recouvrir.</strong> Une même notice peut porter
		plusieurs mentions. Les catégories ne sont donc pas les tranches exclusives d'un
		tout&nbsp;: on ne les additionne pas, et on n'utilise jamais de diagramme en anneau.
		Chaque chiffre se lit pour lui-même.
	</p>
	<p>
		<strong>Les copies «&nbsp;d'après&nbsp;» sont comptées à part.</strong> Écrire
		«&nbsp;d'après Rembrandt&nbsp;», c'est le plus souvent désigner une copie assumée
		d'un modèle&nbsp;: ce n'est pas un doute sur l'auteur, mais un statut. Ces
		{nombre(dApres)} notices «&nbsp;d'après&nbsp;» ({nombre(copiesTotal)} notices de
		copies au total) restent donc hors du décompte du doute.
	</p>
	<p>
		<strong>Le «&nbsp;périmètre étudié&nbsp;» d'un artiste.</strong> Sur la fiche d'un
		artiste, la part affichée (par exemple «&nbsp;9&nbsp;% des notices associées à son
		nom&nbsp;») se rapporte à un <strong>total de référence</strong>&nbsp;: les notices
		classées comme attribution directe ou comme formulation prudente. Les copies
		«&nbsp;d'après&nbsp;» et les autres catégories exclues par le pipeline sont comptées
		séparément et n'entrent pas dans ce dénominateur&nbsp;: c'est pourquoi l'interface
		parle du «&nbsp;périmètre étudié&nbsp;» et non de l'ensemble absolu des notices.
	</p>
	<p>
		<strong>Un seul musée peut peser lourd.</strong> {nombre(n.monoculture_divulguee.doute)}
		formulations prudentes — près d'un quart du total national — viennent d'un seul
		établissement&nbsp;: {n.monoculture_divulguee.libelle}, dont les planches naturalistes
		sont massivement notées «&nbsp;attribué à&nbsp;». Cela ne veut pas dire que ce musée
		doute plus que les autres&nbsp;: c'est un effet de versement. Pour le neutraliser, on
		donne aussi le total <strong>hors ce cas</strong>&nbsp;: {nombre(n.doute_hors_monoculture)}.
	</p>
</section>

<!-- 4. Limites --------------------------------------------------------------- -->
<section id="limites">
	<h2>Limites</h2>
	<p>
		<strong>Les chiffres ne reflètent que ce qui a été versé dans Joconde.</strong> Les
		versements sont volontaires et inégaux d'un musée à l'autre. Un musée absent des
		résultats n'est pas un musée sans incertitudes&nbsp;: c'est peut-être un musée qui
		n'a pas (encore) versé ses notices. C'est pourquoi le projet ne compare jamais deux
		musées sur des comptages bruts.
	</p>
	<p>
		Ce que l'application permet de <strong>constater</strong>&nbsp;: quelles œuvres les
		musées entourent d'une réserve, sous quelles formules, et où elles sont conservées.
		Ce qu'elle ne permet <strong>pas de conclure</strong>&nbsp;: elle n'authentifie
		aucune œuvre, n'en réattribue aucune, et ne dit rien de la valeur d'une pièce ni de
		la richesse d'une collection.
	</p>
</section>

<!-- 5. Sources et droits ----------------------------------------------------- -->
<section id="sources">
	<h2>Sources et droits</h2>
	<p>
		<strong>Données.</strong> Jeu «&nbsp;{prov.source}&nbsp;», {prov.editeur}, publié sur
		data.gouv.fr sous {prov.licence}. Version utilisée&nbsp;: celle du
		<strong>{prov.version_donnee}</strong> (fichier d'environ {go(prov.taille_octets)}&nbsp;Go,
		mis à jour {prov.mise_a_jour_source}). Lexique de détection&nbsp;: {prov.lexique}.
	</p>
	<p>
		<strong>Portraits.</strong> Les portraits des artistes viennent de Wikimedia Commons.
		Ce sont des <em>illustrations</em>, jamais une donnée ni un comptage&nbsp;: chaque
		image porte en légende son auteur et sa licence, vérifiés fichier par fichier — le
		plus souvent le domaine public, parfois une licence Creative Commons qui impose de
		citer l'auteur. Trois artistes n'ont <strong>pas</strong> de portrait fiable
		disponible&nbsp;: leur fiche le dit plutôt que d'afficher une image approchante.
		Aucune image n'est reprise des fiches Joconde elles-mêmes&nbsp;; chaque exemple
		renvoie plutôt à sa notice publique sur POP.
	</p>
	<p>
		<strong>Fond de carte.</strong> Les contours des régions viennent de france-geojson
		(IGN Admin Express 2018), sous Licence Ouverte, stockés localement — aucune tuile en
		ligne. C'est une illustration&nbsp;: aucun chiffre n'en provient, il ne sert qu'à
		situer les points.
	</p>
</section>
	</div>
</div>
</div>

<style>
	/* Pleine page : gouttières propres (direction « affiche »). */
	.page {
		padding: var(--espace-5) clamp(1rem, 4vw, 3rem) var(--espace-6);
	}

	.kicker {
		font-family: var(--police-ui);
		font-size: var(--taille-xs);
		letter-spacing: 0.14em;
		text-transform: uppercase;
		color: var(--accent-cobalt);
		margin: 0 0 var(--espace-2);
	}

	.tete {
		max-width: 52rem;
	}

	h1 {
		font-family: var(--police-titre);
		font-size: var(--taille-xl);
		margin: 0;
	}

	.chapo {
		font-size: var(--taille-m);
		line-height: 1.65;
		margin: var(--espace-3) 0 0;
	}

	/* Prudence : filet vermillon (accent d'alerte de la charte v2). */
	.prudence {
		margin: var(--espace-4) 0 0;
		border-left: 2px solid var(--accent-vermillon);
		padding-left: var(--espace-3);
		font-style: italic;
		font-size: var(--taille-s);
		color: var(--couleur-encre-douce);
	}

	/* Deux zones : rail de sommaire (collant sur ordinateur) + contenu. */
	.grille {
		display: grid;
		grid-template-columns: 16rem 1fr;
		gap: var(--espace-6);
		margin-top: var(--espace-6);
		align-items: start;
	}

	/* Sommaire : repères de lecture, pas un tableau de bord. Collant sur ordinateur. */
	.sommaire {
		position: sticky;
		top: var(--espace-5);
	}

	.sommaire ol {
		list-style: none;
		margin: 0;
		padding: 0;
		font-family: var(--police-ui);
		font-size: var(--taille-s);
		border-left: var(--filet);
	}

	.sommaire li + li {
		margin-top: var(--espace-2);
	}

	.sommaire a {
		display: flex;
		gap: 0.6rem;
		align-items: baseline;
		color: var(--couleur-encre-douce);
		text-decoration: none;
		padding-left: var(--espace-3);
		margin-left: -1px;
		border-left: 2px solid transparent;
	}

	.sommaire a:hover {
		color: var(--couleur-encre);
		border-left-color: var(--accent-cobalt);
	}

	.sommaire .num {
		font-variant-numeric: tabular-nums;
		color: var(--couleur-encre-douce);
	}

	.contenu {
		max-width: 46rem;
		min-width: 0;
	}

	section {
		margin-bottom: var(--espace-6);
	}

	section:last-child {
		margin-bottom: 0;
	}

	section h2 {
		font-family: var(--police-titre);
		/* léger décalage d'ancre : le titre ne colle pas au bord haut au clic. */
		scroll-margin-top: var(--espace-4);
	}

	section p {
		line-height: 1.7;
	}

	@media (max-width: 760px) {
		.grille {
			grid-template-columns: 1fr;
			gap: var(--espace-4);
		}
		.sommaire {
			position: static;
		}
		.sommaire ol {
			display: flex;
			flex-wrap: wrap;
			gap: var(--espace-2) var(--espace-4);
			border-left: none;
		}
		.sommaire li + li {
			margin-top: 0;
		}
		.sommaire a {
			padding-left: 0;
			border-left: none;
		}
	}

	strong {
		font-weight: 600;
	}

	section :global(strong) {
		font-variant-numeric: tabular-nums;
	}
</style>
