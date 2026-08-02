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
	import SchemaChampAuteur from '$lib/SchemaChampAuteur.svelte';
	import SchemaComptageUnique from '$lib/SchemaComptageUnique.svelte';
	import SchemaHomonymes from '$lib/SchemaHomonymes.svelte';

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
	// Personnes identifiées et comptées, mais dont le fonds sort de l'angle du
	// volume (2026-08-02). Ni écartées, ni faux positifs : un état à part entière.
	const nbHorsPerimetre = data.registre.hors_perimetre ?? 0;
	const dApres = n.familles.d_apres.notices;
	const copiesTotal = n.copie;
	const pct = (v) => (v * 100).toLocaleString('fr-FR', { maximumFractionDigits: 1 });
	const go = (o) => (o / 1e9).toLocaleString('fr-FR', { maximumFractionDigits: 2 });

	// Six questions simples (refonte 2026-07-31). Libellés courts pour le rail ;
	// les titres complets sont dans les <h2>.
	const sommaire = [
		['base', 'La base étudiée'],
		['doute', 'Comment le doute s’écrit'],
		['comptage', 'Comment on compte'],
		['artistes', 'Identifier les artistes'],
		['lire', 'Lire les chiffres et les vues'],
		['sources', 'Limites, sources et droits']
	];

	// --- Navigation dans une page longue (palier 5) --------------------------
	// Le rail de sommaire indique où l'on se trouve, et un retour en haut apparaît
	// quand on a défilé. Rien d'automatique ne bouge à l'écran : la page ne prend
	// jamais la main sur le défilement du lecteur.

	let actif = $state(sommaire[0][0]);
	let hautVisible = $state(false);

	// Repérage de la section courante. Mesure directe à chaque défilement plutôt
	// qu'un IntersectionObserver : six éléments, un calcul par image, et surtout
	// une règle qu'on peut énoncer — « la dernière section dont le titre est passé
	// au-dessus du quart supérieur de la fenêtre ». Les cas limites (haut de page,
	// dernière section trop courte pour occuper l'écran) sont traités explicitement.
	$effect(() => {
		const cibles = sommaire
			.map(([ancre]) => document.getElementById(ancre))
			.filter(Boolean);
		if (!cibles.length) return;

		let attendue = false;

		const mesurer = () => {
			attendue = false;
			const seuil = window.innerHeight * 0.25;
			let courante = cibles[0];
			for (const el of cibles) {
				if (el.getBoundingClientRect().top <= seuil) courante = el;
			}
			// Arrivé au pied de page, la dernière section est la bonne réponse même
			// si elle n'a pas atteint le seuil (elle ne le pourra jamais).
			const fin =
				window.scrollY + window.innerHeight >= document.documentElement.scrollHeight - 4;
			if (fin) courante = cibles[cibles.length - 1];

			actif = courante.id;
			hautVisible = window.scrollY > window.innerHeight;
		};

		const auDefilement = () => {
			if (attendue) return;
			attendue = true;
			requestAnimationFrame(mesurer);
		};

		mesurer();
		// Arrivée par un lien vers une ancre (« Pourquoi ces N artistes ? ») : le
		// navigateur saute à la cible avant que cette mesure ne soit installée, sans
		// émettre d'événement de défilement. On remesure donc une fois la page posée,
		// sinon le rail annoncerait la première section alors qu'on est à la quatrième.
		const differee = setTimeout(mesurer, 250);

		window.addEventListener('scroll', auDefilement, { passive: true });
		window.addEventListener('resize', auDefilement);
		window.addEventListener('hashchange', auDefilement);
		return () => {
			clearTimeout(differee);
			window.removeEventListener('scroll', auDefilement);
			window.removeEventListener('resize', auDefilement);
			window.removeEventListener('hashchange', auDefilement);
		};
	});

	// Défilement doux, sauf si le système demande de limiter les animations.
	const douceur = () =>
		window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth';

	// Clic sur le sommaire : on garde le comportement natif (l'ancre reste dans
	// l'URL, le lien fonctionne sans JavaScript) et on y ajoute le défilement doux
	// et le passage du focus clavier à la section atteinte.
	function allerA(evenement, ancre) {
		const cible = document.getElementById(ancre);
		if (!cible) return;
		evenement.preventDefault();
		cible.scrollIntoView({ behavior: douceur(), block: 'start' });
		cible.focus({ preventScroll: true });
		history.replaceState(null, '', `#${ancre}`);
	}

	function retourHaut() {
		window.scrollTo({ top: 0, behavior: douceur() });
		document.getElementById('haut-de-page')?.focus({ preventScroll: true });
		history.replaceState(null, '', window.location.pathname);
	}
</script>

<div class="page">
<header class="tete">
	<p class="kicker">Méthode et limites</p>
	<!-- tabindex : cible du focus au retour en haut (le clavier suit le regard). -->
	<h1 id="haut-de-page" tabindex="-1">Ce que les chiffres disent, et ne disent pas</h1>
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

<div class="grille">
	<nav class="sommaire" aria-label="Sections de la page">
		<ol>
			{#each sommaire as [ancre, titre], i (ancre)}
				<li>
					<a
						href="#{ancre}"
						class:actif={ancre === actif}
						aria-current={ancre === actif ? 'true' : undefined}
						onclick={(e) => allerA(e, ancre)}
					>
						<span class="num">{i + 1}</span>{titre}
					</a>
				</li>
			{/each}
		</ol>
	</nav>

	<div class="contenu">
<!-- 1. La base étudiée ------------------------------------------------------- -->
<section id="base" tabindex="-1">
	<h2>La base étudiée</h2>
	<p>
		<strong>Joconde</strong> est le catalogue collectif des collections des musées de
		France, publié par le ministère de la Culture
		<a href="https://www.data.gouv.fr/fr/datasets/collections-des-musees-de-france-base-joconde/" target="_blank" rel="noopener">sur data.gouv.fr</a>
		sous <strong>{prov.licence}</strong>. Il rassemble plus d'un million de notices,
		décrites par les musées eux-mêmes&nbsp;; une notice correspond généralement à un
		bien muséal, parfois à un ensemble ou à plusieurs éléments. Le projet en lit une
		seule chose&nbsp;: la manière dont les musées écrivent qu'ils ne sont
		<em>pas certains</em> de l'auteur d'une œuvre.
	</p>
	<p>
		Les chiffres de ce site se rapportent à la <strong>version du {prov.version_donnee}</strong>
		de la base. C'est une photographie datée d'un inventaire vivant.
	</p>
	<details>
		<summary>Détails de version</summary>
		<p>
			Fichier d'environ {go(prov.taille_octets)}&nbsp;Go, mis à jour {prov.mise_a_jour_source}.
			Lexique de détection&nbsp;: {prov.lexique}.
		</p>
	</details>
</section>

<!-- 2. Comment le doute s'écrit dans Joconde -------------------------------- -->
<section id="doute" tabindex="-1">
	<h2>Comment le doute s’écrit dans Joconde</h2>
	<p>Trois choses sont à distinguer&nbsp;: ce que les musées écrivent, ce que ces mots
		veulent dire, et la manière dont nous les regroupons.</p>
	<p>
		<strong>1. Ce que les musées publient.</strong> On appelle
		<strong>formulation prudente</strong> une notice où le nom d'un artiste est présent,
		mais accompagné d'une réserve&nbsp;: «&nbsp;attribué à&nbsp;», «&nbsp;atelier
		de&nbsp;», «&nbsp;école de&nbsp;», «&nbsp;entourage de&nbsp;», «&nbsp;suiveur
		de&nbsp;», «&nbsp;à la manière de&nbsp;», «&nbsp;dans le genre de&nbsp;», ou un
		simple «&nbsp;?&nbsp;» après le nom. Ces formules sont celles des musées — le projet
		n'en invente aucune.
	</p>

	<SchemaChampAuteur />

	<p>
		<strong>2. Leur sens.</strong> Il est fixé par la
		<a href="https://www.culture.gouv.fr/thematiques/musees/pour-les-professionnels/conserver-et-gerer-les-collections/informatiser-les-collections-d-un-musee-de-france/organisation-operationnelle-de-l-informatisation-des-collections-d-un-musee-de-france/methode-de-redaction-informatisee-des-notices-d-objets-de-musees" target="_blank" rel="noopener">méthode d'inventaire du ministère</a>
		(la «&nbsp;méthode Joconde&nbsp;»), référence directe des conventions de saisie.
		Pour certains termes, il remonte au
		<a href="https://www.legifrance.gouv.fr/loda/id/LEGITEXT000006063458/" target="_blank" rel="noopener">décret n°&nbsp;81-255 du 3 mars 1981</a>&nbsp;:
		«&nbsp;attribué à&nbsp;» (art. 4), «&nbsp;atelier de&nbsp;» (art. 5), «&nbsp;école
		de&nbsp;» (art. 6), et les termes sans garantie comme «&nbsp;d'après&nbsp;» ou
		«&nbsp;à la manière de&nbsp;» (art. 7). Le simple «&nbsp;?&nbsp;», lui, ne vient
		<em>pas</em> du décret&nbsp;: c'est une convention de saisie propre à Joconde.
	</p>
	<p>
		<strong>3. Notre regroupement.</strong> Ces formules, nous les rangeons en
		<strong>huit familles</strong> et <strong>trois territoires</strong> —
		«&nbsp;Presque lui&nbsp;», «&nbsp;Autour de lui&nbsp;», «&nbsp;Son style, sans
		lui&nbsp;» —, de la plus proche à la plus lointaine du maître. C'est une
		<strong>construction éditoriale</strong>, pas une catégorie officielle&nbsp;; son
		détail est expliqué dans la <a href="{base}/presentation">Présentation</a>.
	</p>
	<p>
		<strong>Comment on les repère.</strong> La détection est lexicale&nbsp;: le
		qualificatif noté entre parenthèses dans le champ auteur («&nbsp;LE BRUN Charles
		(attribué)&nbsp;», «&nbsp;(école)&nbsp;», «&nbsp;(?)&nbsp;»). En lisant toute la
		base, on trouve <strong>{nombre(n.doute_total)}</strong> notices porteuses d'au moins
		une formulation prudente, soit {pct(n.taux_doute_avec_auteur)}&nbsp;% des notices où
		un auteur est renseigné. Le repérage a été <strong>vérifié à la main</strong>&nbsp;:
		un échantillon de 206 notices jugé une à une, le 4 juillet 2026 (vrai / faux /
		incertain), pour mesurer les fausses détections puis reformuler le lexique.
	</p>
</section>

<!-- 3. Comment les notices ont-elles été comptées ? ------------------------- -->
<section id="comptage" tabindex="-1">
	<h2>Comment les notices ont-elles été comptées&nbsp;?</h2>
	<p>
		<strong>Notices et «&nbsp;œuvres concernées&nbsp;».</strong> L'unité du calcul est la
		<strong>notice Joconde</strong>. L'interface emploie parfois «&nbsp;œuvre
		concernée&nbsp;» pour faciliter la lecture, mais une notice peut exceptionnellement
		décrire un ensemble ou plusieurs éléments.
	</p>
	<p>
		<strong>Deux façons de compter, à ne pas confondre.</strong> Dans les
		<strong>comptages nationaux</strong>, une même notice peut porter plusieurs
		mentions&nbsp;: les familles ne sont donc pas les tranches exclusives d'un tout — on
		ne les additionne pas, et on n'utilise jamais de diagramme en anneau. Dans les
		<strong>profils d'artistes</strong>, la règle est plus stricte&nbsp;: <strong>pour un
		artiste donné, une référence Joconde est comptée une seule fois et rattachée à une
		seule famille</strong>, selon une priorité documentée (le «&nbsp;?&nbsp;» l'emporte,
		puis l'ordre des familles). Une même notice peut concerner deux artistes&nbsp;: elle
		apparaît alors dans deux profils, <strong>sans être comptée deux fois</strong> dans
		le total national.
	</p>

	<SchemaComptageUnique />

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
		séparément et n'entrent pas dans ce dénominateur.
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

<!-- 4. Comment les artistes ont-ils été identifiés ? ------------------------ -->
<section id="artistes" tabindex="-1">
	<!-- Ancre visée par le lien « Pourquoi ces N artistes ? » de « Explorer les
	     artistes » : à conserver. Elle porte sur le TITRE et non sur le paragraphe
	     qui suit — sinon le visiteur arrivait sous le titre, sans savoir à quelle
	     question il répond. -->
	<h2 id="les-maitres" tabindex="-1">Comment les artistes ont-ils été identifiés&nbsp;?</h2>
	<p>
		Une partie du site se concentre sur <strong>{nombre(nbNoms)} noms</strong> de
		référence. Le critère est explicite, et il ne demande jamais si l'artiste est
		célèbre&nbsp;: le musée doit écrire un <strong>nom de personne identifiable</strong>
		— un prénom entier, pas une initiale ni un nom de famille tout seul —, cette personne
		doit être séparée de ses homonymes, et son nom doit porter <strong>au moins dix
		notices</strong> à formulation prudente, copies exclues, une fois ses différentes
		graphies réunies. Ce n'est <strong>pas un palmarès des plus grands</strong>&nbsp;:
		c'est un seuil, choisi pour avoir assez de matière à montrer. Ces {nombre(nbNoms)}
		noms réunissent {nombre(douteDansListe)} des {nombre(n.doute_total)} notices prudentes
		relevées dans toute la base.
	</p>
	<p>
		<strong>Cette liste n'est pas close, et elle se vérifie.</strong> Tous les noms qui
		atteignent le seuil ont été relevés — ils sont {nombre(nbCandidats)}. Chacun reçoit un
		état à mesure qu'il est examiné&nbsp;: retenu, écarté avec sa raison, mis
		<em>hors du sujet de cette partie</em>, ou <em>encore à examiner</em>. Un nom encore à
		examiner n'est pas un nom rejeté&nbsp;: c'est un nom dont la vérification n'a pas été
		faite. Aujourd'hui, {nombre(nbRetenus)} formes d'écriture sont rattachées aux
		{nombre(nbNoms)} artistes retenus, {nombre(nbEcartes)} sont écartées — une
		manufacture, une imprimerie, «&nbsp;anonyme&nbsp;», un nom de famille sans prénom qui
		peut désigner plusieurs personnes, ou une mention qui ne porte aucun nom d'auteur —
		et {nombre(nbAInstruire)} restent à examiner. La liste s'agrandira par lots.
	</p>
	<p>
		<strong>Une personne peut être bien identifiée et rester hors de cette partie.</strong>
		{nbHorsPerimetre === 1 ? 'Un nom est dans ce cas' : `${nombre(nbHorsPerimetre)} noms sont dans ce cas`}&nbsp;:
		un fonds d'histoire naturelle de plusieurs milliers de planches, conservé dans un seul
		musée et noté d'un bout à l'autre «&nbsp;attribué à&nbsp;». Le comptage est juste, la
		personne existe, ses notices restent dans les totaux nationaux de ce site&nbsp;— mais
		il ne s'agit pas d'une hésitation sur l'auteur d'une œuvre d'art, qui est le sujet de
		cette partie. Ce n'est <strong>pas une erreur repérée</strong>&nbsp;: c'est un sujet
		différent.
	</p>
	<p>
		<strong>Séparer les personnes, pas seulement les mots.</strong> Rattacher une formule
		au bon artiste demande de la prudence, car le nom est cherché dans un texte libre, et
		un même nom peut cacher plusieurs personnes. Chaque artiste est défini nommément et
		<strong>séparé de ses homonymes</strong> — sous «&nbsp;Michel-Ange&nbsp;», les musées
		ont aussi rangé Corneille Michel-Ange, peintre lyonnais du XVII<sup>e</sup> siècle —
		et de sa famille&nbsp;: le fils du Tintoret n'est pas le Tintoret. Ses
		<strong>graphies multiples</strong> sont regroupées, et chaque référence n'est
		<strong>comptée qu'une fois</strong>. Ces choix sont contrôlés sur des
		<strong>références réelles</strong> (des cas-témoins versionnés) et protégés par des
		<strong>tests de non-régression</strong>, pour qu'une correction n'en défasse pas une
		autre.
	</p>

	<SchemaHomonymes />

	<details>
		<summary>Les trois pièges corrigés en chemin</summary>
		<p>
			Les <strong>fausses correspondances par sous-chaîne</strong> (une œuvre de Serodine
			ne doit pas être rattachée à Rodin) — réglées en n'acceptant que le mot entier&nbsp;;
			les mentions de <strong>nationalité</strong> («&nbsp;école allemande&nbsp;»), qui ne
			sont pas un doute sur un artiste et sont écartées&nbsp;; enfin le doute écrit
			<strong>hors des parenthèses</strong>, qu'il fallait aussi savoir lire.
		</p>
	</details>
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

<!-- Retour en haut : n'apparaît qu'après un écran de défilement, jamais au-dessus
     du texte (il se range dans la gouttière dès qu'il y a la place). -->
<button
	class="retour-haut"
	class:visible={hautVisible}
	inert={!hautVisible}
	onclick={retourHaut}
>
	<span aria-hidden="true">↑</span> <span class="libelle">Haut de page</span>
</button>
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

	/* Section en cours de lecture : le filet se remplit. Le repère est doublé par
	   aria-current, pour ne pas dépendre de la seule couleur. */
	.sommaire a.actif {
		color: var(--couleur-encre);
		border-left-color: var(--accent-cobalt);
		font-weight: 600;
	}

	.sommaire .num {
		font-variant-numeric: tabular-nums;
		color: var(--couleur-encre-douce);
	}

	.sommaire a.actif .num {
		color: var(--accent-cobalt);
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

	/* Décalage d'ancre : au saut, la cible ne colle pas au bord haut de la fenêtre.
	   Vaut pour les sections du sommaire ET pour les titres visés de l'extérieur
	   (#les-maitres, depuis « Explorer les artistes »). */
	section,
	section h2 {
		scroll-margin-top: var(--espace-5);
	}

	section h2 {
		font-family: var(--police-titre);
	}

	/* Le focus posé sur une section au clic du sommaire ne dessine pas de cadre à
	   la souris — mais reste visible au clavier, où il sert de repère. */
	section:focus:not(:focus-visible),
	section h2:focus:not(:focus-visible),
	h1:focus:not(:focus-visible) {
		outline: none;
	}

	.contenu h3 {
		font-family: var(--police-ui);
		font-size: var(--taille-s);
		letter-spacing: 0.08em;
		text-transform: uppercase;
		color: var(--couleur-encre-douce);
		margin: var(--espace-5) 0 0;
	}

	section p {
		line-height: 1.7;
	}

	/* Liens de contenu : cobalt discret, jamais le poids d'un bouton. */
	.contenu a {
		color: var(--accent-cobalt);
		text-decoration: none;
		border-bottom: 1px solid transparent;
	}

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

	/* Retour en haut : pastille discrète en bas de fenêtre, du registre UI.
	   Absente tant qu'on n'a pas défilé d'au moins un écran. */
	.retour-haut {
		position: fixed;
		right: clamp(1rem, 3vw, 2rem);
		bottom: clamp(1rem, 3vw, 2rem);
		display: inline-flex;
		align-items: center;
		gap: var(--espace-2);
		padding: var(--espace-2) var(--espace-3);
		background: var(--surface-carte);
		color: var(--couleur-encre-douce);
		border: var(--filet);
		border-radius: var(--rayon-m);
		box-shadow: var(--ombre-douce);
		font-size: var(--taille-xs);
		cursor: pointer;
		opacity: 0;
		visibility: hidden;
		transform: translateY(0.4rem);
		transition: opacity 0.2s ease, transform 0.2s ease, visibility 0.2s;
	}

	.retour-haut.visible {
		opacity: 1;
		visibility: visible;
		transform: none;
	}

	.retour-haut:hover {
		color: var(--couleur-encre);
		border-color: var(--couleur-encre-douce);
	}

	/* Le mouvement est un confort, pas une information : on le retire si le
	   système demande de limiter les animations. */
	@media (prefers-reduced-motion: reduce) {
		.retour-haut {
			transition: none;
			transform: none;
		}
	}

	@media print {
		.sommaire,
		.retour-haut {
			display: none;
		}
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
		/* Le filet de gauche disparaît en liste horizontale : le repère passe
		   dessous, sinon la section en cours ne se distingue plus. */
		.sommaire a.actif {
			border-bottom: 2px solid var(--accent-cobalt);
		}

		/* Sur petit écran, le bouton se réduit à sa flèche pour couvrir le moins de
		   texte possible. Le libellé reste dans le document (nom accessible du
		   bouton), seulement retiré de la vue. */
		.retour-haut {
			padding: var(--espace-2);
			border-radius: 50%;
			line-height: 1;
		}

		.retour-haut .libelle {
			position: absolute;
			width: 1px;
			height: 1px;
			overflow: hidden;
			clip-path: inset(50%);
			white-space: nowrap;
		}
	}

	strong {
		font-weight: 600;
	}

	section :global(strong) {
		font-variant-numeric: tabular-nums;
	}
</style>
