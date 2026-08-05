<script>
	// « Méthode et limites » (refonte 2026-07-31, six questions) : page publique de
	// référence. Six sections en questions simples — la base · comment le doute
	// s'écrit · comment on compte · comment les artistes sont identifiés · lire les
	// chiffres · limites, sources et droits. Éditoriale et accessible ; les limites
	// au même rang que le récit (CLAUDE.md). Doc technique détaillée : docs/methode-et-limites.md.
	import { nombre } from '$lib/joconde.js';
	import { base } from '$app/paths';
	// Quatre visuels (palier 4) : trois schémas HTML/CSS qui expliquent chacun UNE
	// règle sur un cas réel, et une capture de l'interface pour les crédits d'image.
	import ExemplesChampAuteur from '$lib/ExemplesChampAuteur.svelte';
	import ExempleComptageUnique from '$lib/ExempleComptageUnique.svelte';
	import ExempleHomonymes from '$lib/ExempleHomonymes.svelte';
	// Rail de sommaire (palier 5). Le mécanisme — repérage de la section lue,
	// défilement doux, retour en haut — a quitté cette page le 2026-08-04 pour
	// devenir un composant : « Présentation » en avait besoin à son tour, et le
	// site ne doit pas porter deux navigations internes différentes.
	import SommaireAncres from '$lib/SommaireAncres.svelte';

	let { data } = $props();
	const n = data.niveaux;
	const prov = data.provenance;

	// Chiffres, tous issus des exports (jamais saisis à la main).
	const nbNoms = data.artistes.artistes.length;
	// Registre des candidats : l'engagement de publier qui a été examiné, et
	// avec quel résultat (decisions.md 2026-07-21 quater, décision 4).
	const nbCandidats = data.registre.formes_au_seuil;
	const nbRetenus = data.registre.retenues;
	const nbEcartes = data.registre.ecartees;
	const nbAInstruire = data.registre.a_instruire;
	// Personnes identifiées et comptées, mais dont le fonds sort de l'angle du
	// volume (2026-08-02). Ni écartées, ni faux positifs : un état à part entière.
	const nbHorsPerimetre = data.registre.hors_perimetre ?? 0;
	const dApres = n.familles.d_apres.notices;
	const copiesTotal = n.copie;
	const go = (o) => (o / 1e9).toLocaleString('fr-FR', { maximumFractionDigits: 2 });
	// « 2026-07-01 » → « 1er juillet 2026 ». La date de version reste lue dans
	// provenance.json ; seule sa mise en français se fait ici.
	const MOIS = [
		'janvier', 'février', 'mars', 'avril', 'mai', 'juin',
		'juillet', 'août', 'septembre', 'octobre', 'novembre', 'décembre'
	];
	const dateFr = (iso) => {
		const [annee, mois, jour] = iso.split('-').map(Number);
		return `${jour === 1 ? '1er' : jour} ${MOIS[mois - 1]} ${annee}`;
	};

	// Six questions simples (refonte 2026-07-31). Libellés courts pour le rail ;
	// les titres complets sont dans les <h2>.
	const sommaire = [
		['base', 'La base étudiée'],
		// Seule section à sous-parties pour l'instant (2026-08-05) : ses cinq temps
		// sont trop distincts pour tenir sous un seul repère dans le rail.
		[
			'doute',
			'Comment le doute s’écrit',
			[
				['doute-ecrit', 'Ce que le musée écrit'],
				['doute-exemples', 'Trois exemples réels'],
				['doute-references', 'Les textes de référence'],
				['doute-classement', 'Le classement utilisé'],
				['doute-reperage', 'Comment les notices sont repérées']
			]
		],
		[
			'comptage',
			'Que comptons-nous ?',
			[
				['comptage-unite', 'L’unité de calcul'],
				['comptage-mentions', 'Plusieurs mentions'],
				['comptage-copies', 'Les copies'],
				['comptage-part', 'La part affichée']
			]
		],
		[
			'artistes',
			'La liste des artistes',
			[
				['artistes-seuil', 'Un seuil commun'],
				['artistes-identites', 'Vérifier les identités'],
				['artistes-liste', 'Une liste en cours']
			]
		],
		['lire', 'Lire les chiffres et les vues'],
		['sources', 'Limites, sources et droits']
	];

	// Navigation dans une page longue (palier 5) : voir SommaireAncres.svelte, qui
	// porte désormais le repérage de la section lue et le retour en haut.
</script>

<div class="page">
<div class="grille">
<!-- Le bandeau de titre vit DANS la grille depuis le 2026-08-05, en tête de la
     colonne de contenu : la page n'a plus qu'une seule ligne de départ, et le rail
     monte à hauteur du titre. Il reste premier dans le document (le titre se lit
     avant le sommaire) ; le repli à 760 px le remet au-dessus de la barre de liens.
     Même disposition que « Présentation » : passer d'une page à l'autre ne doit pas
     déplacer le titre. -->
<header class="tete">
	<p class="kicker">Méthode et limites</p>
	<!-- tabindex : cible du focus au retour en haut (le clavier suit le regard). -->
	<h1 id="haut-de-page" tabindex="-1">Comment L'inventaire du doute a été construit</h1>
	<!-- Ouverture réécrite par l'utilisateur le 2026-08-05 : elle annonce le plan de la
	     page au lieu de la commenter. Le second paragraphe garde le rang de la ligne de
	     prudence — même place, même petit corps qu'auparavant. -->
	<p class="chapo">
		Cette page présente les données utilisées, les règles appliquées pour repérer et
		compter les notices, la façon dont les artistes ont été identifiés et les limites
		des résultats.
	</p>
	<p class="prudence">
		L'inventaire reprend les informations publiées dans
		<a
			href="https://www.data.gouv.fr/fr/datasets/collections-des-musees-de-france-base-joconde/"
			target="_blank"
			rel="noopener">Joconde</a>. Il ne cherche pas à déterminer l'auteur des œuvres.
	</p>
</header>

	<SommaireAncres sections={sommaire} ancreHaut="haut-de-page" />

	<div class="contenu">
<!-- 1. Quelles données ? ------------------------------------------------------
     Texte de l'utilisateur (2026-08-05). Les trois valeurs citées viennent des
     exports : la date de version et la licence de provenance.json, l'effectif de
     niveaux.json. Aucune n'est écrite dans la page. -->
<section id="base" tabindex="-1">
	<h2>Quelles données avons-nous utilisées&nbsp;?</h2>
	<p>
		<strong>Joconde</strong> est le catalogue collectif des collections des musées de
		France. Chaque notice rassemble les informations transmises par un musée sur un bien
		ou un ensemble conservé dans ses collections&nbsp;: titre, auteur, datation,
		technique, dimensions ou lieu de conservation.
	</p>
	<p>
		Pour cette enquête, nous avons utilisé la
		<strong>version du {dateFr(prov.version_donnee)}</strong>, diffusée par le ministère
		de la Culture
		<a href="https://www.data.gouv.fr/fr/datasets/collections-des-musees-de-france-base-joconde/" target="_blank" rel="noopener">sur data.gouv.fr</a>
		sous <strong>{prov.licence}</strong>. Elle contient {nombre(n.notices_total)} notices.
		Les résultats présentés sur ce site correspondent donc à cette version précise de la
		base.
	</p>
	<details>
		<summary>Détails de version</summary>
		<p>
			Fichier d'environ {go(prov.taille_octets)}&nbsp;Go, mis à jour {prov.mise_a_jour_source}.
			Lexique de détection&nbsp;: {prov.lexique}.
		</p>
	</details>
</section>

<!-- 2. Comment une attribution incertaine est-elle indiquée ? ------------------
     Section refondue le 2026-08-05, texte de l'utilisateur. Cinq sous-parties, une
     ancre chacune : elles apparaissent en retrait sous la section dans le rail
     (SommaireAncres accepte un troisième élément par entrée). Les h3 portent donc
     id et tabindex, comme les sections. -->
<section id="doute" tabindex="-1">
	<h2>Comment une attribution incertaine est-elle indiquée dans Joconde&nbsp;?</h2>

	<h3 id="doute-ecrit" tabindex="-1">Ce que le musée écrit</h3>
	<p>
		Dans une notice Joconde, le musée dispose d'un champ pour indiquer l'auteur. Lorsqu'une
		attribution est incertaine, le nom peut être accompagné d'un point d'interrogation ou
		d'une précision comme «&nbsp;attribué à&nbsp;», «&nbsp;atelier de&nbsp;»,
		«&nbsp;école de&nbsp;», «&nbsp;entourage de&nbsp;», «&nbsp;suiveur de&nbsp;»,
		«&nbsp;manière de&nbsp;» ou «&nbsp;genre de&nbsp;». L'inventaire reprend ces
		indications telles qu'elles ont été publiées.
	</p>

	<h3 id="doute-exemples" tabindex="-1">Trois exemples réels</h3>
	<ExemplesChampAuteur />

	<h3 id="doute-references" tabindex="-1">Les textes de référence</h3>
	<p>
		Ces usages sont documentés dans la
		<a href="https://www.culture.gouv.fr/content/download/197593/file/methode.pdf?inLanguage=fre-FR" target="_blank" rel="noopener">méthode de rédaction informatisée</a>
		publiée par le ministère de la Culture. Celle-ci indique qu'un point d'interrogation ou
		des termes comme «&nbsp;attribué à&nbsp;», «&nbsp;atelier de&nbsp;» et
		«&nbsp;école de&nbsp;» peuvent exprimer un doute sur l'auteur.
	</p>
	<p>
		Plusieurs de ces expressions sont également définies par le
		<a href="https://www.legifrance.gouv.fr/loda/id/LEGITEXT000006063458/" target="_blank" rel="noopener">décret du 3 mars 1981</a>
		relatif aux transactions d'œuvres d'art. Ce décret ne régit pas la rédaction des
		notices Joconde&nbsp;: il précise la portée de termes comme «&nbsp;attribué à&nbsp;»,
		«&nbsp;atelier de&nbsp;», «&nbsp;école de&nbsp;» ou «&nbsp;manière de&nbsp;».
	</p>

	<h3 id="doute-classement" tabindex="-1">Le classement utilisé</h3>
	<p>
		Pour comparer les notices, le projet rassemble huit indications en trois groupes&nbsp;:
		«&nbsp;Au plus près&nbsp;», «&nbsp;Autour du maître&nbsp;» et «&nbsp;Dans son
		influence&nbsp;». Ce classement a été créé pour cette application. Il ne correspond ni
		à une catégorie officielle de Joconde ni à une échelle juridique. Son détail est
		expliqué dans la <a href="{base}/presentation">Présentation</a>.
	</p>

	<h3 id="doute-reperage" tabindex="-1">Comment les notices sont repérées</h3>
	<p>
		Pour établir le total national, le traitement recherche ces indications dans les champs
		de Joconde consacrés à l'auteur et à son attribution. Pour construire les profils
		d'artistes, il utilise uniquement le champ «&nbsp;Auteur&nbsp;», où le nom et la
		réserve peuvent être reliés sans ambiguïté. Le repérage a été contrôlé sur 206 notices
		afin d'écarter les cas où les mêmes mots avaient un autre sens.
	</p>
	<p class="note-methode">
		Le terme «&nbsp;présumé&nbsp;» a également été retenu dans
		{nombre(n.familles.presume.notices)} notices du total national. Cette forme très rare
		ne fait pas partie des huit catégories utilisées pour comparer les artistes.
	</p>
</section>

<!-- 3. Que comptons-nous, et comment ? ----------------------------------------
     Section refondue le 2026-08-05, texte de l'utilisateur. Quatre sous-parties
     ancrées, comme la section précédente. Le paragraphe sur le musée de Nice est
     parti dans « Limites, sources et droits » : il ne répondait pas à la question
     du comptage, il énonçait une limite de lecture. Ses chiffres n'ont pas bougé. -->
<section id="comptage" tabindex="-1">
	<h2>Que comptons-nous, et comment&nbsp;?</h2>

	<h3 id="comptage-unite" tabindex="-1">L’unité de calcul</h3>
	<p>
		Tous les chiffres sont calculés à partir des notices Joconde. Une notice correspond
		généralement à une œuvre, mais elle peut aussi décrire un ensemble ou plusieurs
		éléments. Dans l'interface, le mot «&nbsp;œuvre&nbsp;» est employé lorsqu'un objet est
		présenté au lecteur&nbsp;; les calculs reposent toujours sur les références des
		notices.
	</p>

	<h3 id="comptage-mentions" tabindex="-1">Lorsqu’une notice contient plusieurs mentions</h3>
	<p>
		Une même notice peut contenir plusieurs indications pour un même artiste. Dans le
		total national, elle ne compte qu'une seule fois. Dans la répartition nationale par
		formulation, elle peut cependant apparaître dans plusieurs catégories&nbsp;: ces
		résultats ne doivent donc pas être additionnés.
	</p>
	<p>
		Dans le profil d'un artiste, chaque notice est classée une seule fois, sous une seule
		mention. Lorsqu'un point d'interrogation est présent, c'est cette mention qui est
		retenue&nbsp;; dans les autres cas, le classement suit un ordre défini à l'avance.
	</p>
	<p>
		Une notice peut aussi citer deux artistes différents. Elle apparaît alors dans chacun
		de leurs profils, mais ne compte toujours qu'une fois dans le total national.
	</p>

	<ExempleComptageUnique />

	<h3 id="comptage-copies" tabindex="-1">Les copies sont comptées séparément</h3>
	<p>
		La mention «&nbsp;d'après&nbsp;» indique généralement qu'une œuvre reprend un modèle
		connu. Dans ce projet, elle est donc classée parmi les copies et non parmi les
		attributions incertaines. La base contient {nombre(copiesTotal)} notices classées
		comme copies, dont {nombre(dApres)} portent la mention «&nbsp;d'après&nbsp;». Elles
		restent consultables séparément, mais n'entrent pas dans le total du doute.
	</p>

	<h3 id="comptage-part" tabindex="-1">Comment la part affichée pour un artiste est calculée</h3>
	<p>
		La fiche d'un artiste compare deux ensembles&nbsp;: les notices qui lui attribuent
		directement une œuvre et celles qui associent son nom à une réserve. Par exemple,
		l'indication «&nbsp;9&nbsp;%&nbsp;» signifie que 9&nbsp;% des notices retenues pour cet
		artiste comportent une incertitude sur l'attribution. Les copies
		«&nbsp;d'après&nbsp;» ne sont pas incluses dans ce calcul.
	</p>
	<p>
		Ce pourcentage mesure la fréquence des réserves dans les notices associées à
		l'artiste. Il ne mesure ni l'authenticité des œuvres ni le degré de certitude du
		musée.
	</p>
</section>

<!-- 4. Comment les artistes ont-ils été identifiés ? ------------------------ -->
<section id="artistes" tabindex="-1">
	<!-- Ancre visée par le lien « Pourquoi ces N artistes ? » de « Explorer les
	     artistes » : à conserver. Elle porte sur le TITRE et non sur le paragraphe
	     qui suit — sinon le visiteur arrivait sous le titre, sans savoir à quelle
	     question il répond. -->
	<h2 id="les-maitres" tabindex="-1">Comment la liste des artistes a-t-elle été établie&nbsp;?</h2>

	<h3 id="artistes-seuil" tabindex="-1">Un seuil commun</h3>
	<p>
		Nous avons d'abord relevé les artistes dont le nom apparaît dans au moins dix notices
		exprimant un doute sur l'attribution. Les différentes écritures d'un même nom sont
		réunies et les copies «&nbsp;d'après&nbsp;» sont comptées séparément. Ce seuil ne
		mesure ni la célébrité ni l'importance d'un artiste&nbsp;: il garantit simplement un
		nombre suffisant de notices pour construire son profil.
	</p>

	<h3 id="artistes-identites" tabindex="-1">Une vérification des identités</h3>
	<p>
		Chaque nom est ensuite vérifié dans les notices. Un nom de famille isolé, une initiale
		ou le nom d'une entreprise ne suffisent pas pour identifier une personne. Les homonymes
		sont séparés et les variantes d'un même nom sont regroupées. Cette vérification évite,
		par exemple, d'attribuer à Michel-Ange des notices qui concernent Corneille Michel-Ange
		ou d'autres artistes portant le même prénom.
	</p>

	<h3 id="artistes-liste" tabindex="-1">Une liste encore en cours d’examen</h3>
	<p>
		Au total, {nombre(nbCandidats)} formes de noms atteignent le seuil. À ce jour,
		{nombre(nbRetenus)} ont été rattachées à {nombre(nbNoms)} artistes.
		{nombre(nbEcartes)} ont été retirées parce qu'elles ne permettaient pas d'identifier
		précisément une personne,
		{nbHorsPerimetre === 1
			? 'une personne identifiable a été placée'
			: `${nombre(nbHorsPerimetre)} personnes identifiables ont été placées`}
		hors du périmètre de ce volet, et {nombre(nbAInstruire)} restent à examiner. Un nom qui
		n'a pas encore été examiné n'est pas rejeté&nbsp;: la liste est complétée
		progressivement.
	</p>

	<ExempleHomonymes />

	<p class="note-methode">Chaque correction est vérifiée à partir de notices réelles.</p>
</section>

<!-- 5. Lire les chiffres et les vues ---------------------------------------- -->
<section id="lire" tabindex="-1">
	<h2>Lire les chiffres et les vues</h2>
	<p>
		<strong>Le graphique d'un artiste</strong> place chaque mention à sa
		<strong>part</strong> (en&nbsp;%) parmi les œuvres concernées, regroupée dans les
		trois territoires. On y compare la <em>forme</em> du doute, pas des volumes bruts&nbsp;;
		le sens de chaque mention est donné dans la <a href="{base}/presentation">Présentation</a>.
	</p>
	<p>
		<strong>Le nombre de musées</strong> d'une fiche ne compte que ceux ayant publié
		<strong>au moins une notice prudente</strong> pour l'artiste, non l'ensemble des
		musées où il apparaît.
	</p>
	<p>
		<strong>La carte</strong> montre où le doute se disperse autour d'un seul
		nom&nbsp;: <strong>un point = un musée détenteur</strong>, jamais une comparaison
		entre musées.
	</p>
	<p>
		<strong>Les reproductions</strong> sont des illustrations&nbsp;: chacune porte sa
		source et sa licence (voir plus bas), jamais une preuve d'attribution.
	</p>
</section>

<!-- 6. Limites, sources et droits ------------------------------------------- -->
<section id="sources" tabindex="-1">
	<h2>Limites, sources et droits</h2>
	<p>
		<strong>Les chiffres ne reflètent que ce qui a été versé dans Joconde.</strong> Les
		versements sont volontaires et inégaux d'un musée à l'autre. Un musée absent des
		résultats n'est pas un musée sans incertitudes&nbsp;: c'est peut-être un musée qui
		n'a pas (encore) versé ses notices. C'est pourquoi le projet ne compare jamais deux
		musées sur des comptages bruts.
	</p>
	<!-- Venu de « Que comptons-nous, et comment ? » le 2026-08-05 : le poids d'un seul
	     versement est une limite de lecture, pas une règle de comptage. Chiffres
	     inchangés, toujours lus dans niveaux.json. -->
	<p>
		<strong>Un seul musée peut peser lourd.</strong> {nombre(n.monoculture_divulguee.doute)}
		formulations prudentes — près d'un quart du total national — viennent d'un seul
		établissement&nbsp;: {n.monoculture_divulguee.libelle}, dont les planches naturalistes
		sont massivement notées «&nbsp;attribué à&nbsp;». Cela ne veut pas dire que ce musée
		doute plus que les autres&nbsp;: c'est un effet de versement. Pour le neutraliser, on
		donne aussi le total <strong>hors ce cas</strong>&nbsp;: {nombre(n.doute_hors_monoculture)}.
	</p>
	<p>
		Ce que l'application permet de <strong>constater</strong>&nbsp;: quelles œuvres les
		musées entourent d'une réserve, sous quelles formules, et où elles sont conservées.
		Ce qu'elle ne permet <strong>pas de conclure</strong>&nbsp;: elle n'authentifie
		aucune œuvre, n'en réattribue aucune, et ne dit rien de la valeur d'une pièce ni de
		la richesse d'une collection.
	</p>
	<p>
		<strong>Portraits et reproductions.</strong> Les portraits des artistes et, lorsqu'elles
		existent sous licence libre, les reproductions des œuvres viennent de Wikimedia
		Commons. Ce sont des <em>illustrations</em>, jamais une donnée ni un comptage&nbsp;:
		chaque image porte son auteur et sa licence, vérifiés fichier par fichier — le plus
		souvent le domaine public, parfois une licence Creative Commons qui impose de citer
		l'auteur. Une reproduction n'est retenue que si elle est rattachée <strong>avec
		certitude</strong> à la notice par son identifiant Joconde. Les photographies des
		fiches POP elles-mêmes ne sont <strong>pas</strong> reprises&nbsp;: leurs crédits ne
		portent pas de licence de réutilisation ouverte. Chaque œuvre renvoie à sa notice
		publique sur POP.
	</p>

	<!-- Visuel nº 4 (palier 4) : capture RÉELLE de l'interface, recadrée sur une
	     seule œuvre — la règle des crédits telle qu'elle s'applique, pas un schéma. -->
	<figure class="capture">
		<img
			src="{base}/methode/vignette-credit.png"
			width="848"
			height="576"
			alt="Une œuvre dans l’application : la reproduction à gauche, avec sous l’image le crédit « After François Clouet », la licence CC BY-SA 3.0 et le lien vers Wikimedia Commons ; à droite la mention du musée, le titre, le lieu de conservation et la formule exacte de la notice."
		/>
		<figcaption>
			Une œuvre telle qu’elle apparaît dans l’application&nbsp;: sous la reproduction, le
			crédit, la licence et le lien vers le fichier d’origine&nbsp;; à côté, la formule
			exacte publiée par le musée. Capture du 31 juillet 2026.
		</figcaption>
	</figure>

	<h3>Références</h3>
	<ul class="refs">
		<li>Données&nbsp;: <a href="https://www.data.gouv.fr/fr/datasets/collections-des-musees-de-france-base-joconde/" target="_blank" rel="noopener">jeu «&nbsp;{prov.source}&nbsp;»</a>, {prov.editeur}, {prov.licence} — et la nomenclature des champs (fichier joint au jeu).</li>
		<li>Conventions de saisie&nbsp;: <a href="https://www.culture.gouv.fr/thematiques/musees/pour-les-professionnels/conserver-et-gerer-les-collections/informatiser-les-collections-d-un-musee-de-france/organisation-operationnelle-de-l-informatisation-des-collections-d-un-musee-de-france/methode-de-redaction-informatisee-des-notices-d-objets-de-musees" target="_blank" rel="noopener">méthode d'inventaire du ministère (méthode Joconde)</a>.</li>
		<li>Certains termes&nbsp;: <a href="https://www.legifrance.gouv.fr/loda/id/LEGITEXT000006063458/" target="_blank" rel="noopener">décret n°&nbsp;81-255 du 3 mars 1981</a> (Légifrance).</li>
		<li>POP, plateforme ouverte du patrimoine&nbsp;: <a href="https://pop.culture.gouv.fr/conditions-generales-utilisation" target="_blank" rel="noopener">conditions d'utilisation</a> · <a href="https://pop.culture.gouv.fr/aide" target="_blank" rel="noopener">aide</a> · <a href="https://pop.culture.gouv.fr/donnees-ouvertes" target="_blank" rel="noopener">données ouvertes</a>.</li>
		<li>Reproductions&nbsp;: Wikimedia Commons — <a href="https://commons.wikimedia.org/wiki/Commons:Reusing_content_outside_Wikimedia" target="_blank" rel="noopener">réutilisation</a> et <a href="https://commons.wikimedia.org/wiki/Commons:Reuse_of_PD-Art_photographs" target="_blank" rel="noopener">photographies d'œuvres du domaine public</a>.</li>
		<li>Fond de carte&nbsp;: <a href="https://github.com/gregoiredavid/france-geojson" target="_blank" rel="noopener">france-geojson</a> (contours IGN Admin Express, Licence Ouverte), stockés localement — aucune tuile en ligne, aucun chiffre n'en provient.</li>
	</ul>
</section>
	</div>
</div>
</div>

<style>
	/* Enveloppe IDENTIQUE à « Présentation » et à « Explorer les artistes »
	   (2026-08-05) : même largeur maximale, même centrage, mêmes gouttières, même
	   retrait sous le bandeau. La page était restée sans limite : sur un écran de
	   1920 px, sa colonne démarrait 224 px plus à gauche que celle de
	   « Présentation ». Passer d'une page à l'autre ne doit rien déplacer. */
	.page {
		box-sizing: border-box;
		width: 100%;
		max-width: 92rem;
		margin-inline: auto;
		padding-inline: clamp(1.25rem, 3vw, 3rem);
		padding-top: clamp(1.5rem, 3.5vw, 3.5rem);
		padding-bottom: var(--espace-6);
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
		grid-column: 2;
		grid-row: 1;
		max-width: 52rem;
	}

	h1 {
		font-family: var(--police-titre);
		font-size: var(--taille-xl);
		margin: 0;
	}

	/* Chapô : mêmes corps, interligne et largeur que l'ouverture de
	   « Présentation » (.ouverture-texte). */
	.chapo {
		max-width: 46rem;
		font-size: var(--taille-m);
		line-height: 1.6;
		margin: var(--espace-4) 0 0;
	}

	/* Ligne de prudence : le traitement de « Présentation » — petit corps UI, gris,
	   sans filet. Le filet vermillon en donnait ici un troisième (2026-08-05) : deux
	   pages, deux styles pour la même phrase. */
	.prudence {
		max-width: 44rem;
		margin: var(--espace-4) 0 0;
		font-family: var(--police-ui);
		font-size: var(--taille-xs);
		line-height: 1.5;
		color: var(--couleur-encre-douce);
	}

	/* Deux zones : rail de sommaire (collant sur ordinateur) + contenu, le bandeau de
	   titre en tête de la seconde. Le rail court sur les deux lignes — sa zone de
	   grille descend jusqu'au bas du contenu, ce dont son `position: sticky` a besoin
	   pour suivre la lecture. Le placement est explicite parce que l'ordre du
	   document ne suit pas celui de la grille : le titre est écrit avant le
	   sommaire. */
	.grille {
		display: grid;
		grid-template-columns: 16rem minmax(0, 1fr);
		gap: var(--espace-6);
		align-items: start;
	}

	/* Le rail lui-même (styles, état, retour en haut) vit dans SommaireAncres.svelte
	   depuis le 2026-08-04. Cette page ne garde que la colonne qui l'accueille. */
	.grille > :global(.sommaire) {
		grid-column: 1;
		grid-row: 1 / span 2;
	}

	/* Comme sur « Présentation », la colonne de contenu n'est PAS bornée à la largeur
	   d'un paragraphe : ce sont les blocs qui se bornent eux-mêmes, chacun à la
	   valeur qu'il a là-bas — 44 rem le texte courant, 72 rem les visuels. */
	.contenu {
		grid-column: 2;
		grid-row: 2;
		min-width: 0;
	}

	section p,
	section ul,
	details {
		max-width: 44rem;
	}

	/* Les blocs LARGES : les trois schémas et la capture d'écran. Ils étaient tenus à
	   46 rem par la colonne ; ils prennent la même place que le graphique et le
	   glossaire de « Présentation ». */
	.contenu :global(.schema),
	.capture {
		max-width: 72rem;
	}

	/* Rythme vertical de « Présentation » : l'espace entre deux sections est posé
	   par le haut, et les marges des titres et des paragraphes sont écrites — la
	   page ne s'en remet plus aux valeurs par défaut du navigateur. */
	section {
		margin-top: var(--espace-6);
	}

	.contenu > section:first-child {
		margin-top: 0;
	}

	h2 {
		margin: 0 0 var(--espace-4);
	}

	section p {
		margin: 0 0 var(--espace-4);
	}

	/* Décalage d'ancre : au saut, la cible ne colle pas au bord haut de la fenêtre.
	   Vaut pour les sections du sommaire ET pour les titres visés de l'extérieur
	   (#les-maitres, depuis « Explorer les artistes »). */
	section,
	section h2,
	section h3 {
		scroll-margin-top: var(--espace-5);
	}

	section h2 {
		font-family: var(--police-titre);
	}

	/* Le focus posé sur une section au clic du sommaire ne dessine pas de cadre à
	   la souris — mais reste visible au clavier, où il sert de repère. */
	section:focus:not(:focus-visible),
	section h2:focus:not(:focus-visible),
	section h3:focus:not(:focus-visible),
	h1:focus:not(:focus-visible) {
		outline: none;
	}

	/* Sous-titres : l'échelle des h3 de « Présentation » (glossaire) — une seule
	   échelle pour tout le site. */
	.contenu h3 {
		font-family: var(--police-ui);
		font-size: var(--taille-xs);
		letter-spacing: 0.1em;
		text-transform: uppercase;
		color: var(--couleur-encre-douce);
		margin: var(--espace-5) 0 var(--espace-2);
	}

	/* Les cinq sous-parties de « Comment le doute s'écrit » sont des temps du récit,
	   pas des intertitres de service : elles réclament la respiration d'une section,
	   sinon la précédente semble se poursuivre. */
	#doute h3 {
		margin-top: var(--espace-6);
	}

	section p {
		line-height: 1.65;
	}

	/* Note de méthode : une précision de second rang, pas un paragraphe du fil.
	   Petit corps gris, comme la ligne de prudence de l'ouverture. */
	.note-methode {
		font-family: var(--police-ui);
		font-size: var(--taille-xs);
		line-height: 1.5;
		color: var(--couleur-encre-douce);
	}

	/* Liens de contenu : cobalt discret, jamais le poids d'un bouton. Le bandeau de
	   titre en porte un depuis le 2026-08-05 (Joconde, dans la ligne de prudence). */
	.tete a,
	.contenu a {
		color: var(--accent-cobalt);
		text-decoration: none;
		border-bottom: 1px solid transparent;
	}

	.tete a:hover,
	.tete a:focus-visible,
	.contenu a:hover,
	.contenu a:focus-visible {
		border-bottom-color: var(--accent-cobalt);
	}

	/* Détails repliables : sobres, registre UI. */
	details {
		margin-top: var(--espace-3);
	}

	details summary {
		cursor: pointer;
		font-family: var(--police-ui);
		font-size: var(--taille-s);
		color: var(--couleur-encre-douce);
	}

	details[open] summary {
		margin-bottom: var(--espace-2);
	}

	/* Capture d'interface : bordée comme les schémas, jamais décorative. */
	.capture {
		margin: var(--espace-5) 0;
		padding: var(--espace-4);
		background: var(--surface-carte);
		border: var(--filet);
		border-radius: var(--rayon-m);
	}

	.capture img {
		display: block;
		width: 100%;
		height: auto;
		border: var(--filet-clair);
		border-radius: var(--rayon-s);
	}

	.capture figcaption {
		margin-top: var(--espace-3);
		padding-top: var(--espace-3);
		border-top: var(--filet-clair);
		font-family: var(--police-ui);
		font-size: var(--taille-xs);
		line-height: 1.5;
		color: var(--couleur-encre-douce);
	}

	/* Références : liste serrée, petit corps, filet à gauche. */
	.refs {
		list-style: none;
		margin: var(--espace-3) 0 0;
		padding: 0;
		font-size: var(--taille-s);
		line-height: 1.6;
	}

	.refs li {
		margin-top: var(--espace-2);
		padding-left: var(--espace-3);
		border-left: var(--filet);
	}

	/* Le rail bascule en barre horizontale au même seuil : les deux media queries
	   (ici et dans SommaireAncres.svelte) doivent rester sur 760 px. */
	@media (max-width: 760px) {
		.grille {
			grid-template-columns: 1fr;
			gap: var(--espace-4);
		}

		/* Une seule colonne : les trois blocs reprennent l'ordre du document —
		   titre, barre de liens, contenu. */
		.grille > :global(.sommaire),
		.tete,
		.contenu {
			grid-column: auto;
			grid-row: auto;
		}
	}

	strong {
		font-weight: 600;
	}

	section :global(strong) {
		font-variant-numeric: tabular-nums;
	}
</style>
