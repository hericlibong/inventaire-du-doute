<script>
	import MetaPage from '$lib/MetaPage.svelte';
	import { META } from '$lib/meta.js';

	// PAGE « PRÉSENTATION » du volume 1 — phase 4 (2026-08-02).
	//
	// Cinq temps, dans cet ordre : ce qu'est le projet et ce que contient ce volet ·
	// des exemples de notices réelles · comment ces artistes ont été choisis · les
	// mots que les musées emploient · l'entrée dans l'exploration.
	//
	// Le titre « Ce n'est pas un cas isolé » et ses deux paragraphes ont été retirés
	// le 2026-08-04 : ils redisaient Joconde, la réserve d'attribution et l'objet du
	// volet, tous posés par l'ouverture. Le BANDEAU DE CHIFFRES qu'ils coiffaient
	// reste : il donne l'ampleur d'un coup d'œil, sans phrase.
	//
	// PAS de scrollytelling (choix utilisateur, réserve du 2026-07-08) : une page
	// qui se lit, avec une seule visualisation, à sa place. Le brief l'autorisait ;
	// la préférence tenue depuis le début du projet l'écarte.
	//
	// AUCUN CHIFFRE N'EST ÉCRIT ICI. Tous viennent des exports (+page.js). Un
	// effectif dans un titre redevient faux au premier lot d'artistes suivant.
	import { base } from '$app/paths';
	import { nombre, lienPop, licenceEnFrancais } from '$lib/joconde.js';
	import { FAMILLE_PUBLIC } from '$lib/familles-public.js';
	import { TERRITOIRES } from '$lib/territoires.js';
	import MentionsFrequentes from '$lib/presentation/MentionsFrequentes.svelte';
	// Même rail de sommaire que « Méthode et limites » (composant partagé depuis le
	// 2026-08-04) : repérage de la section lue, défilement doux, retour en haut.
	import SommaireAncres from '$lib/SommaireAncres.svelte';

	let { data } = $props();
	const { corpus, registre, niveaux } = data;

	const u = corpus.unites;

	// Les deux notices montrées en tête, relues et contrôlées à l'export
	// (build_corpus_maitres.py) : référence, mention, image réutilisable, licence
	// et page source. La page n'en recopie aucun champ.
	const exemples = corpus.exemples;

	// Une phrase par mention, et une seule. Écrite ici parce qu'elle explique une
	// FORMULE, pas une œuvre : elle vaudrait mot pour mot pour n'importe quelle
	// autre notice portant la même mention.
	const EXPLICATION = {
		atelier_de:
			'La mention «\u00a0atelier\u00a0» signifie que l’œuvre est rattachée à l’atelier de ' +
			'Rembrandt, sans être attribuée directement au peintre.',
		attribue:
			'La mention «\u00a0attribué à\u00a0» signifie que le musée considère cet artiste ' +
			'comme un auteur possible, sans présenter cette attribution comme certaine.',
		point_interrogation:
			'Le point d’interrogation signale que l’identification de l’auteur reste incertaine.'
	};

	// Part du volume dans le total national, en toutes lettres plutôt qu'en
	// décimales : le récit prime (CLAUDE.md).
	const partVolume = Math.round(corpus.national.part_du_volume * 100);

	// Définitions des huit mentions. Elles vivaient sur « Comprendre les mentions »,
	// page retirée de la navigation en phase 7 : elles ont déménagé ICI, sous le
	// graphique qui les compte — c'est là qu'un lecteur se demande ce que veut dire
	// « de son école ». Elles n'existent qu'à un seul endroit du site.
	// Formule type affichée UNIQUEMENT là où elle apporte quelque chose (règle
	// anti-répétition encodée dans familles-public.js).
	const formuleType = (code) =>
		FAMILLE_PUBLIC[code].montrerMention ? FAMILLE_PUBLIC[code].mention('un artiste') : null;

	// Les sept sections de la page, dans l'ordre de lecture. Identifiants stables et
	// sans accents : ils entrent dans l'URL et peuvent être partagés. Les libellés
	// du rail sont ceux des titres, raccourcis pour les deux questions — un rail de
	// 16 rem ne tient pas « Qu'est-ce que L'inventaire du doute ? ». Les titres
	// complets restent dans le h1 et les h2, seuls textes publiés.
	const sommaire = [
		['le-projet', 'L’inventaire du doute'],
		['ce-volet', 'Ce premier volet'],
		['exemples', 'Exemples de notices Joconde'],
		['selection', 'Comment ces artistes ont été choisis'],
		['chiffres', 'Les mentions en chiffres'],
		['definitions', 'Ce que ces mots veulent dire'],
		['explorer', 'Explorer, artiste par artiste']
	];
</script>

<MetaPage {...META.projet} chemin="/projet/" />


<div class="page">
	<!-- OUVERTURE (révisée le 2026-08-03, texte de l'utilisateur repris tel quel) : deux
	     blocs séparés, deux titres sobres formulés comme des questions. Le premier dit ce
	     qu'est le projet et sa matière, le second ce que contient ce volet et ce qu'on peut
	     y faire — la définition ne se répète pas d'un bloc à l'autre (resserrement du
	     2026-08-03, à la relecture de l'utilisateur). Aucun récit, aucun constat nouveau.
	     Les trois effectifs sont lus dans les exports — le total national vient de
	     niveaux.json, les deux autres de corpus_maitres.json.
	     Premier paragraphe réécrit le 2026-08-04, sur le texte de l'utilisateur : le projet
	     se définit d'abord, puis son OBJECTIF, énoncé sans sujet humain. Le musée n'est
	     jamais présenté comme une personne qui hésite ou qui avoue — c'est une institution,
	     et le projet lit ce qu'elle publie. « Notices » est répété d'une phrase à l'autre
	     À DESSEIN : le total national compte des notices, jamais des œuvres, et une reprise
	     par « on en compte 24 507 » laisserait le chiffre sans antécédent. -->
	<div class="grille">
	<!-- Le bandeau de titre est la PREMIÈRE section du sommaire. Il vit DANS la
	     grille depuis le 2026-08-05, en tête de la colonne de contenu : la page n'a
	     plus qu'une seule ligne de départ, et le rail monte à hauteur du titre — ce
	     qui le pose comme une navigation, et non comme le premier contenu de la
	     page. Il reste premier dans le document (le titre se lit avant le sommaire),
	     et le repli à 760 px le remet naturellement au-dessus de la barre de liens.
	     Il est aussi la cible du retour en haut (tabindex : le clavier suit le
	     regard). -->
	<header class="tete" id="le-projet" tabindex="-1">
		<p class="kicker">Volume 1 — Autour des maîtres</p>
		<h1>Qu'est-ce que L'inventaire du doute&nbsp;?</h1>
		<p class="ouverture-texte">
			L'inventaire du doute est un projet d'analyse et d'exploration de la
			<a
				href="https://www.data.gouv.fr/fr/datasets/collections-des-musees-de-france-base-joconde/"
				target="_blank"
				rel="noopener">base Joconde</a>,
			le catalogue collectif des musées de France. L'objectif est de repérer les notices
			qui portent une incertitude ou une réserve sur l'auteur d'une œuvre. On compte
			aujourd'hui <strong>{nombre(niveaux.doute_total)}</strong> notices qui présentent
			une forme de doute. Le projet ne cherche pas à authentifier les œuvres, mais à
			rendre ces incertitudes visibles et consultables.
		</p>
	</header>

	<SommaireAncres sections={sommaire} ancreHaut="le-projet" />

	<div class="contenu">
	<section class="ouverture" id="ce-volet" tabindex="-1">
		<h2>Que présente ce premier volet&nbsp;?</h2>
		<p class="ouverture-texte">
			Ce premier volet est consacré aux artistes dont le nom apparaît régulièrement avec une
			réserve d'attribution. Pour chacun, le lecteur peut comparer ces formulations, consulter
			les œuvres concernées et voir dans quels musées elles sont conservées. D'autres volets
			pourront explorer différentes formes de doute présentes dans Joconde.
		</p>
	</section>

	<!-- EXEMPLES DE NOTICES (2026-08-04) : même structure pour chacun — image,
	     titre, musée, champ Auteur au mot près, UNE phrase d'explication, lien POP.
	     Aucune carte décorative, aucun récit. Le titre n'annonce pas de compte : il
	     survit à l'ajout ou au retrait d'un exemple.
	     Ce que les exemples ont en commun est dit UNE FOIS, en chapô (2026-08-04) :
	     la phrase « le musée renseigne ainsi le champ consacré à l'auteur » était
	     répétée à l'identique sous chaque titre, et ne disait pas COMMENT. Le chapô
	     nomme le champ reproduit et dit ce qui accompagne le nom, pour que la
	     citation qui suit se lise sans explication ; chaque exemple ne garde plus
	     que ce qui lui est propre. Chapô écrit par l'utilisateur, repris tel quel.
	     ⚠ Il annonce DEUX exemples : à modifier si la liste en gagne ou en perd un. -->
	<section class="notices-exemples" id="exemples" tabindex="-1">
		<h2>Exemples de notices Joconde</h2>
		<p class="texte">
			Les deux exemples ci-dessous reproduisent le champ «&nbsp;Auteur&nbsp;» de Joconde.
			Le nom de l'artiste est accompagné d'une réserve inscrite dans la notice.
		</p>

		<div class="liste-exemples">
			{#each exemples as e (e.reference)}
				<article class="exemple">
					<figure class="oeuvre">
						<a class="visuel" href={e.image.source} target="_blank" rel="noopener">
							<img src="{base}/{e.image.url}" alt="Reproduction : {e.titre}" loading="lazy" />
						</a>
						<figcaption class="credit">
							{licenceEnFrancais(e.image.licence)}
							{#if e.image.creator} · {e.image.creator}{/if} ·
							<a href={e.image.source} target="_blank" rel="noopener">Wikimedia&nbsp;Commons</a>
						</figcaption>
					</figure>

					<div class="propos">
						<h3>{e.titre}</h3>
						<p class="lieu">{e.musee}, {e.ville}</p>

						<blockquote
							class="verbatim"
							style="border-left-color: {FAMILLE_PUBLIC[e.mention].couleur}"
						>
							{e.extrait}
						</blockquote>

						<p>{EXPLICATION[e.mention]}</p>

						<p class="renvoi">
							<a href={lienPop(e.reference)} target="_blank" rel="noopener">
								Consulter la notice complète sur POP&nbsp;→
							</a>
						</p>
					</div>
				</article>
			{/each}
		</div>

		<!-- Vers la section de la page Méthode qui décrit ce que ces exemples montrent :
		     « Comment le doute s'écrit dans Joconde » (#doute), celle qui porte le schéma
		     du champ Auteur. Ancre directe, pas le haut de la page. -->
		<p class="renvoi renvoi-methode">
			<a href="{base}/methode#doute">
				Plus d'informations sur le traitement des notices&nbsp;→
			</a>
		</p>
	</section>

	<!-- 3. LA SÉLECTION (réécrite le 2026-08-04, texte de l'utilisateur) : UN SEUL
	     paragraphe, puis le renvoi vers la méthode. Il remplace les trois blocs
	     « seuil · vérification · ce que la liste ne dit pas », dont le détail vit
	     désormais sur la seule page Méthode. Les trois chiffres restent lus dans les
	     exports : le seuil vient du registre, l'effectif et les notices du corpus. -->
	<section class="selection" id="selection" tabindex="-1">
		<h2>Comment ces artistes ont été choisis</h2>
		<p class="texte">
			Cette sélection a été construite en filtrant et en classant les notices de
			Joconde&nbsp;: elle réunit les artistes dont le nom apparaît dans au moins
			<strong>{registre.seuil} notices</strong> comportant une réserve sur l'auteur.
			Ce seuil permet de disposer de plusieurs cas à examiner pour chacun. Les
			différentes écritures d'un même nom ont été regroupées, puis chaque identité a
			été vérifiée afin de rattacher les notices au bon artiste.
		</p>
		<p class="renvoi">
			<a href="{base}/methode#les-maitres">Le détail de la méthode et ses limites&nbsp;→</a>
		</p>
	</section>

	<!-- 4. LES MENTIONS EN CHIFFRES : le bandeau, puis le graphique -------------
	     Déplacement du 2026-08-04. Les trois chiffres vivaient plus haut, seuls
	     dans leur propre section, et donnaient l'ampleur avant qu'on sache de quoi
	     elle était l'ampleur. Ils n'existent plus qu'ICI, sous le titre et devant
	     le graphique qui détaille les mêmes notices.
	     Le TITRE de la section est désormais porté par la page, plus par le
	     composant : c'est lui qui coiffe le bandeau ET le graphique.
	     ⚠ RÈGLE : les trois chiffres du volet (artistes, notices, part du total)
	     ne se disent qu'ICI. Les paragraphes d'ouverture et de sélection les
	     répétaient ; ils ont été allégés le 2026-08-04. Un chiffre répété d'un
	     bloc à l'autre se lit comme un chiffre différent. -->
	<section class="graphique" id="chiffres" tabindex="-1">
		<h2>Les mentions en chiffres</h2>

		<ul class="chiffres">
			<li>
				<b>{nombre(u.nb_artistes)}</b>
				<span>artistes dont le nom porte une réserve dans au moins {registre.seuil} notices</span>
			</li>
			<li>
				<b>{nombre(u.notices_distinctes)}</b>
				<span>notices concernées, dans les musées de France</span>
			</li>
			<li>
				<b>{partVolume}&nbsp;%</b>
				<span>
					des notices prudentes repérées dans Joconde&nbsp;: le reste
					({nombre(niveaux.doute_total - u.notices_distinctes)} notices) ne nomme pas
					ces artistes-là
				</span>
			</li>
		</ul>

		<MentionsFrequentes {corpus} />
	</section>

	<!-- LE GLOSSAIRE, détaché de la section chiffrée le 2026-08-04 : il se lisait
	     comme une seconde légende du graphique, alors que c'est le SEUL endroit du
	     site où les huit mentions sont définies. Un filet et une respiration l'en
	     séparent ; le chapô ne renvoie plus à « l'ordre du graphique ». Les huit
	     définitions elles-mêmes ne sont pas retouchées. -->
	<section class="glossaire" id="definitions" tabindex="-1">
		<h2>Ce que ces mots veulent dire</h2>
		<p class="texte">
			Les huit mentions employées par les musées, définies une à une. La couleur de chacune
			est la même partout sur le site.
		</p>
		<div class="zones">
			{#each TERRITOIRES as t (t.id)}
				<div class="zone">
					<h3>{t.titre}</h3>
					<!-- Les trois en-têtes sont VOLONTAIREMENT celles du graphique : c'est ce
					     qui fait comprendre que le glossaire définit les groupes qu'on vient de
					     voir (source unique, territoires.js). L'annotation de zone, écrite là
					     depuis longtemps mais affichée nulle part sur cette page, évite que la
					     reprise soit une copie sèche : elle dit en une ligne ce que le groupe
					     recouvre, avant les définitions mention par mention (2026-08-05). -->
					<p class="annotation">{t.annotation}</p>
					<dl>
						{#each t.codes as code (code)}
							<div class="entree-mention">
								<dt>
									<span class="pastille" style="background: {FAMILLE_PUBLIC[code].couleur}"></span>
									{FAMILLE_PUBLIC[code].label}
								</dt>
								<dd>
									{FAMILLE_PUBLIC[code].corps}
									{#if formuleType(code)}
										<span class="formule">
											Elle s'écrit par exemple «&nbsp;{formuleType(code)}&nbsp;».
										</span>
									{/if}
								</dd>
							</div>
						{/each}
					</dl>
				</div>
			{/each}
		</div>
	</section>

	<!-- 5. LA SUITE ------------------------------------------------------------ -->
	<section class="suite" id="explorer" tabindex="-1">
		<h2>Explorer, artiste par artiste</h2>
		<p class="texte">
			Chaque artiste a sa fiche&nbsp;: les mots employés à son sujet, la liste complète des
			œuvres concernées avec les phrases exactes des musées, et la carte des établissements
			qui les conservent.
		</p>
		<p class="renvoi">
			<a class="entree" href="{base}/artistes">Explorer les artistes&nbsp;→</a>
		</p>
		<p class="prudence">
			Le projet reprend les formulations publiées par les musées. Il ne réattribue aucune
			œuvre et n'émet aucun avis sur les attributions.
		</p>
	</section>
	</div>
	</div>
</div>

<style>
	/* Enveloppe IDENTIQUE à celle d'« Explorer les artistes » (2026-08-03) : même
	   largeur maximale, même centrage, mêmes gouttières, même retrait sous le
	   bandeau. Les deux pages doivent se poser au même endroit de l'écran — sinon
	   passer de l'une à l'autre donne l'impression de changer de site. La page était
	   restée sans limite après son passage en pleine largeur : sur un grand écran,
	   elle courait d'un bord à l'autre. */
	.page {
		box-sizing: border-box;
		width: 100%;
		max-width: 92rem;
		margin-inline: auto;
		padding-inline: clamp(1.25rem, 3vw, 3rem);
		padding-top: clamp(1.5rem, 3.5vw, 3.5rem);
		padding-bottom: var(--espace-6);
	}

	/* Deux zones, comme sur « Méthode et limites » : rail de sommaire (collant sur
	   ordinateur) + contenu. Le rail vient du composant partagé ; la page ne fournit
	   que la colonne. Le bandeau de titre occupe la première ligne de la colonne de
	   contenu (2026-08-05) : titre, texte et blocs partent tous de la même abscisse.
	   Le rail, lui, court sur les deux lignes — sa zone de grille descend jusqu'au
	   bas du contenu, ce dont son `position: sticky` a besoin pour suivre la
	   lecture. Le placement est explicite parce que l'ordre du document ne suit pas
	   celui de la grille : le titre est écrit avant le sommaire. */
	.grille {
		display: grid;
		grid-template-columns: 16rem minmax(0, 1fr);
		gap: var(--espace-6);
		align-items: start;
	}

	.grille > :global(.sommaire) {
		grid-column: 1;
		grid-row: 1 / span 2;
	}

	.tete {
		grid-column: 2;
		grid-row: 1;
		max-width: 52rem;
	}

	/* Contrairement à la page Méthode, la colonne de contenu n'est PAS bornée à la
	   largeur d'un paragraphe : elle porte aussi le bandeau de chiffres, le
	   graphique et le glossaire, qui ont besoin de place. Ce sont les blocs de texte
	   qui se bornent eux-mêmes, plus bas (44 à 52 rem). */
	.contenu {
		grid-column: 2;
		grid-row: 2;
		min-width: 0;
	}

	/* Le rail et le texte partent de la même ligne : la première section ne reprend
	   pas la marge haute commune aux sections. */
	.contenu > section:first-child {
		margin-top: 0;
	}

	/* Décalage d'ancre : au saut, la cible ne colle pas au bord haut de la fenêtre.
	   Le bandeau du site défile avec la page (il n'est pas collant) : ce retrait
	   suffit à dégager le titre visé. */
	.tete,
	section {
		scroll-margin-top: var(--espace-5);
	}

	/* Le focus posé sur une section au clic du sommaire ne dessine pas de cadre à la
	   souris — mais reste visible au clavier, où il sert de repère. */
	.tete:focus:not(:focus-visible),
	section:focus:not(:focus-visible) {
		outline: none;
	}

	/* Les blocs LARGES de la page (glossaire, mentions en chiffres) se bornent tous au
	   même endroit : sans quoi chacun trouve sa propre limite et la page n'a plus de
	   colonne. Le texte courant, lui, reste plus étroit (44 rem). La sélection a
	   quitté cette liste le 2026-08-04 : elle n'est plus qu'un paragraphe de texte ;
	   le bandeau de chiffres aussi, mais parce qu'il est passé DANS .graphique, qui
	   le borne déjà. */
	.zones,
	.graphique {
		max-width: 72rem;
	}

	.kicker {
		font-family: var(--police-ui);
		font-size: var(--taille-xs);
		letter-spacing: 0.14em;
		text-transform: uppercase;
		color: var(--accent-cobalt);
		margin: 0 0 var(--espace-2);
	}

	/* Liens de contenu : cobalt discret, filet au survol — le traitement écrit pour
	   la page Méthode (2026-08-05). Cette page laissait le bleu souligné du
	   navigateur, seule rupture de charte des deux pages. */
	/* Liens éditoriaux : cobalt ET soulignement permanent (2026-08-08, phase 3).
	   Le cobalt seul ne suffisait pas à dire qu'un mot se clique : la même couleur
	   met en valeur les nombres importants, qui ne sont pas des liens. La couleur
	   reste, le trait la double — et l'information ne repose plus sur elle seule.
	   Le soulignement est natif (`text-decoration`) et non un `border-bottom` :
	   il ne déplace pas le texte quand il s'épaissit au survol, et il évite les
	   jambages.
	   Les appels à l'action (`.entree`, cartouche plein) gardent leur propre
	   traitement : un bouton n'a pas besoin d'être souligné pour se signaler. */
	.tete a:not(.entree),
	.contenu a:not(.entree) {
		color: var(--accent-cobalt);
		text-decoration: underline;
		text-decoration-color: rgba(53, 87, 138, 0.45);
		text-decoration-thickness: 1px;
		text-underline-offset: 0.18em;
	}

	.tete a:not(.entree):hover,
	.tete a:not(.entree):focus-visible,
	.contenu a:not(.entree):hover,
	.contenu a:not(.entree):focus-visible {
		text-decoration-color: var(--accent-cobalt);
		text-decoration-thickness: 2px;
	}

	h1 {
		font-family: var(--police-titre);
		font-size: var(--taille-xl);
		margin: 0;
		line-height: 1.15;
	}

	/* Ouverture : les deux blocs ont le même traitement, pour qu'ils se lisent comme
	   deux réponses de même rang — seul le niveau de titre les distingue (h1 pour le
	   titre de la page, h2 pour le second). */
	.ouverture h2 {
		margin: 0;
		font-family: var(--police-titre);
		font-size: var(--taille-l);
		line-height: 1.2;
	}

	.ouverture-texte {
		max-width: 46rem;
		margin: var(--espace-4) 0 0;
		font-size: var(--taille-m);
		line-height: 1.6;
	}

	section {
		margin-top: var(--espace-6);
	}

	.ouverture {
		max-width: 52rem;
		margin-top: var(--espace-5);
	}

	h2 {
		margin: 0 0 var(--espace-4);
	}

	.texte {
		max-width: 44rem;
		margin: 0 0 var(--espace-4);
		line-height: 1.65;
	}

	/* --- Le bandeau de chiffres ----------------------------------------------
	   Depuis le 2026-08-04 il ouvre la section « Les mentions en chiffres » : il
	   lui faut donc une marge basse, pour ne pas coller au chapô du graphique qui
	   le suit immédiatement. */
	.chiffres {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(14rem, 1fr));
		gap: var(--espace-4);
		margin: 0 0 var(--espace-6);
		padding: 0;
		list-style: none;
	}

	.chiffres li {
		padding-top: var(--espace-3);
		border-top: 2px solid var(--couleur-trait);
	}

	.chiffres b {
		display: block;
		font-family: var(--police-titre);
		font-size: var(--taille-l);
		line-height: 1.1;
		font-variant-numeric: tabular-nums;
	}

	.chiffres span {
		display: block;
		margin-top: var(--espace-2);
		font-size: var(--taille-s);
		line-height: 1.45;
		color: var(--couleur-encre-douce);
	}

	/* --- Les deux exemples : même gabarit, l'un sous l'autre ----------------- */
	.liste-exemples {
		display: flex;
		flex-direction: column;
		gap: clamp(2rem, 4vw, 3rem);
		max-width: 60rem;
	}

	/* Un exemple : image à gauche, contenu de la notice à droite. Les deux
	   exemples partagent EXACTEMENT cette grille — c'est ce qui les rend
	   comparables d'un coup d'œil. */
	.exemple {
		display: grid;
		grid-template-columns: minmax(0, 17rem) minmax(0, 34rem);
		gap: clamp(1.5rem, 4vw, 3rem);
		align-items: start;
		padding-top: var(--espace-5);
		border-top: 1px solid var(--couleur-trait-clair);
	}

	.exemple h3 {
		margin: 0;
		font-family: var(--police-titre);
		font-size: var(--taille-m);
		line-height: 1.3;
	}

	.exemple .lieu {
		margin: 0.35rem 0 var(--espace-4);
		font-family: var(--police-ui);
		font-size: var(--taille-xs);
		color: var(--couleur-encre-douce);
	}

	.oeuvre {
		margin: 0;
	}

	.visuel {
		display: block;
		background: var(--surface-carte);
		border: 1px solid var(--couleur-trait);
	}

	.visuel img {
		display: block;
		width: 100%;
		height: auto;
	}

	.credit {
		margin-top: var(--espace-2);
		font-family: var(--police-ui);
		font-size: var(--taille-xs);
		line-height: 1.4;
		color: var(--couleur-encre-douce);
	}

	.propos p {
		max-width: 34rem;
		line-height: 1.65;
	}

	/* La seule citation littérale de la page : les mots exacts du musée. */
	.verbatim {
		margin: var(--espace-4) 0;
		padding: var(--espace-2) 0 var(--espace-2) var(--espace-3);
		border-left: 3px solid var(--couleur-trait);
		font-family: var(--police-titre);
		font-size: var(--taille-m);
		line-height: 1.4;
	}

	/* La grille en trois colonnes de la sélection (.etapes, .rang, .exemples) est
	   partie le 2026-08-04 avec les trois blocs qu'elle mettait en page. La section
	   ne contient plus qu'un paragraphe : elle se contente de .texte et de .renvoi. */

	/* --- Renvois et sortie ---------------------------------------------------- */
	.renvoi {
		margin: var(--espace-3) 0 0;
		font-family: var(--police-ui);
		font-size: var(--taille-s);
	}

	/* Renvoi de fin de section : il suit la liste des exemples, pas le dernier
	   d'entre eux — il lui faut donc plus d'air que sous un bloc de notice. */
	.renvoi-methode {
		margin-top: var(--espace-5);
	}

	.entree {
		display: inline-block;
		padding: 0.55rem 1rem;
		background: var(--accent-cobalt);
		color: var(--cadre-encre);
		text-decoration: none;
		border-radius: var(--rayon-s);
	}

	.entree:hover,
	.entree:focus-visible {
		text-decoration: underline;
	}

	.prudence {
		max-width: 44rem;
		margin: var(--espace-4) 0 0;
		font-family: var(--police-ui);
		font-size: var(--taille-xs);
		line-height: 1.5;
		color: var(--couleur-encre-douce);
	}

	/* --- 4 bis. Le glossaire des huit mentions -------------------------------
	   Il ne prolonge pas la section chiffrée : un filet et une respiration franche
	   marquent le changement de nature (des définitions, plus des mesures). */
	.glossaire {
		max-width: 72rem;
		margin-top: var(--espace-6);
		padding-top: var(--espace-6);
		border-top: 1px solid var(--couleur-trait);
	}

	.zones {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(17rem, 1fr));
		gap: clamp(1.5rem, 3vw, 2.5rem);
	}

	.zone h3 {
		margin: 0 0 var(--espace-2);
		padding-bottom: var(--espace-2);
		border-bottom: 1px solid var(--couleur-trait);
		font-family: var(--police-ui);
		font-size: var(--taille-xs);
		letter-spacing: 0.1em;
		text-transform: uppercase;
		color: var(--couleur-encre-douce);
	}

	/* L'annotation de zone reste du texte courant : en capitales, elle passerait pour
	   un second en-tête, alors qu'elle se lit comme une phrase. */
	.zone .annotation {
		margin: 0 0 var(--espace-3);
		font-size: var(--taille-s);
		line-height: 1.5;
		color: var(--couleur-encre-douce);
	}

	.zone dl {
		margin: 0;
	}

	.entree-mention + .entree-mention {
		margin-top: var(--espace-4);
	}

	.entree-mention dt {
		display: flex;
		align-items: baseline;
		gap: 0.45rem;
		font-weight: 600;
	}

	.pastille {
		flex: none;
		width: 0.55rem;
		height: 0.55rem;
		border-radius: 50%;
	}

	.entree-mention dd {
		margin: 0.25rem 0 0;
		line-height: 1.55;
		color: var(--couleur-encre-douce);
	}

	.formule {
		display: block;
		margin-top: 0.2rem;
		font-family: var(--police-ui);
		font-size: var(--taille-xs);
	}

	@media (max-width: 860px) {
		.exemple {
			grid-template-columns: minmax(0, 1fr);
		}

		.oeuvre {
			max-width: 17rem;
		}
	}

	/* Le rail passe en barre de liens horizontale au-dessus du contenu. Le seuil de
	   760 px est celui du composant : les deux doivent basculer ensemble. */
	@media (max-width: 760px) {
		.grille {
			grid-template-columns: minmax(0, 1fr);
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
</style>
