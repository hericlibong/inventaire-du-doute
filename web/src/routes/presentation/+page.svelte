<script>
	// PAGE « PRÉSENTATION » du volume 1 — phase 4 (2026-08-02).
	//
	// Six temps, dans cet ordre : ce qu'on lit sous une œuvre · ce que ce nom ne
	// dit pas · le passage du cas au volume · comment ces artistes ont été choisis
	// · les mots que les musées emploient · l'entrée dans l'exploration.
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

	let { data } = $props();
	const { corpus, registre, niveaux } = data;

	const u = corpus.unites;
	const n = corpus.notice_ouverture;
	const mention = FAMILLE_PUBLIC[n.mention];

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
</script>

<svelte:head>
	<title>Présentation — L'inventaire du doute, volume 1</title>
	<meta
		name="description"
		content="Dans les musées de France, un nom sous une œuvre n'est pas toujours une certitude. Ce volume lit les formulations prudentes que les musées publient eux-mêmes."
	/>
</svelte:head>

<div class="page">
	<!-- OUVERTURE (révisée le 2026-08-03, texte de l'utilisateur repris tel quel) : deux
	     blocs séparés, deux titres sobres formulés comme des questions. Le premier dit ce
	     qu'est le projet et sa matière, le second ce que contient ce volet et ce qu'on peut
	     y faire — la définition ne se répète pas d'un bloc à l'autre (resserrement du
	     2026-08-03, à la relecture de l'utilisateur). Aucun récit, aucun constat nouveau.
	     Les trois effectifs sont lus dans les exports — le total national vient de
	     niveaux.json, les deux autres de corpus_maitres.json. -->
	<header class="tete">
		<p class="kicker">Volume 1 — Autour des maîtres</p>
		<h1>Qu'est-ce que L'inventaire du doute&nbsp;?</h1>
		<p class="ouverture-texte">
			L'inventaire du doute analyse les données de Joconde, le catalogue collectif des
			musées de France. Il repère les notices dans lesquelles l'auteur d'une œuvre est
			indiqué avec réserve et rassemble les formulations employées par les musées.
			On en compte aujourd'hui <strong>{nombre(niveaux.doute_total)}</strong>.
			Le projet ne cherche pas à authentifier les œuvres, mais à rendre ces incertitudes
			visibles et consultables.
		</p>
	</header>

	<section class="ouverture">
		<h2>Que présente ce premier volet&nbsp;?</h2>
		<p class="ouverture-texte">
			Ce premier volet est consacré aux artistes dont le nom apparaît régulièrement avec une
			réserve d'attribution. Il réunit actuellement
			<strong>{nombre(u.nb_artistes)} artistes</strong> et
			<strong>{nombre(u.notices_distinctes)} notices</strong>. Pour chacun, le lecteur peut
			comparer ces formulations, consulter les œuvres concernées et voir dans quels musées
			elles sont conservées. D'autres volets pourront explorer différentes
			formes de doute présentes dans Joconde.
		</p>
	</section>

	<!-- 1. LA NOTICE : un cas réel, ses mots exacts. --------------------------- -->
	<section class="cas">
		<figure class="oeuvre">
			{#if n.image}
				<a class="visuel" href={n.image.source} target="_blank" rel="noopener">
					<img src="{base}/{n.image.url}" alt="Reproduction : {n.titre}" loading="lazy" />
				</a>
				<figcaption class="credit">
					{n.titre} · {n.musee}, {n.ville} ·
					{licenceEnFrancais(n.image.licence)} ·
					<a href={n.image.source} target="_blank" rel="noopener">Wikimedia&nbsp;Commons</a>
				</figcaption>
			{/if}
		</figure>

		<div class="propos">
			<h2>Ce que le musée a écrit</h2>
			<p>
				Au Louvre, ce portrait s'intitule
				<em>«&nbsp;{n.titre}&nbsp;»</em>. Le titre lui-même revient sur une identification
				ancienne. Et à la ligne de l'auteur, le musée n'a pas écrit
				<strong>{n.artiste}</strong> tout court. Il a écrit&nbsp;:
			</p>

			<blockquote class="verbatim" style="border-left-color: {mention.couleur}">
				{n.extrait}
			</blockquote>

			<p>
				Autrement dit&nbsp;: une œuvre sortie de l'atelier de {n.artiste}, sans que sa main
				soit affirmée. Le nom est là, la réserve aussi. C'est écrit, c'est public, et
				c'est cela que ce volume rassemble.
			</p>
			<p class="renvoi">
				<a href={lienPop(n.reference)} target="_blank" rel="noopener">
					Voir cette notice sur POP, la plateforme ouverte du patrimoine&nbsp;→
				</a>
			</p>
		</div>
	</section>

	<!-- 2. DU CAS AU VOLUME ---------------------------------------------------- -->
	<section class="corpus">
		<h2>Ce n'est pas un cas isolé</h2>
		<p class="texte">
			Les musées de France versent leurs collections dans un catalogue commun,
			<strong>Joconde</strong>, publié en données ouvertes. Quand un musée n'est pas certain
			de l'auteur d'une œuvre, il ne laisse pas la case vide&nbsp;: il écrit un nom et il
			écrit sa réserve — «&nbsp;attribué à&nbsp;», «&nbsp;de son atelier&nbsp;»,
			«&nbsp;de son école&nbsp;», ou simplement un point d'interrogation.
			Ces mots sont normés, et ils se comptent.
		</p>
		<p class="texte">
			Ce volume suit une seule piste&nbsp;: les <strong>artistes</strong> dont le nom
			revient dans ces formulations. Pas tous les cas de doute de la base — d'autres
			formes existent, et feront l'objet d'autres volumes.
		</p>

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
					du doute écrit dans Joconde&nbsp;: le reste
					({nombre(niveaux.doute_total - u.notices_distinctes)} notices) ne nomme pas
					ces artistes-là
				</span>
			</li>
		</ul>
	</section>

	<!-- 3. LA SÉLECTION : seuil · vérification · ce que la liste ne dit pas ----- -->
	<section class="selection">
		<h2>Comment ces artistes ont été choisis</h2>
		<p class="texte">
			La question mérite d'être posée franchement, parce qu'une liste de noms peut vite
			devenir un palmarès. Celle-ci n'en est pas un&nbsp;: la notoriété n'entre nulle part
			dans le tri. Trois choses seulement, dans cet ordre.
		</p>

		<div class="etapes">
			<article>
				<h3><span class="rang">1</span> Un seuil, pour avoir de quoi regarder</h3>
				<p>
					Un nom entre dans la liste s'il revient dans au moins
					<strong>{registre.seuil} notices</strong> portant une réserve, une fois ses
					différentes orthographes réunies. En dessous, il n'y a pas assez de matière
					pour dire quoi que ce soit. Ce seuil ne juge de rien&nbsp;: il évite seulement
					de commenter deux ou trois cas isolés.
				</p>
				<p>
					Tous les noms qui l'atteignent ont été relevés, sans exception&nbsp;: ils sont
					<strong>{nombre(registre.formes_au_seuil)}</strong>.
				</p>
			</article>

			<article>
				<h3><span class="rang">2</span> Une vérification, nom par nom</h3>
				<p>
					Atteindre le seuil ne suffit pas. Chaque nom est examiné à la main, et beaucoup
					ne passent pas&nbsp;:
				</p>
				<ul class="exemples">
					<li>
						<b>«&nbsp;Peter&nbsp;»</b>, <b>«&nbsp;Buquet&nbsp;»</b>,
						<b>«&nbsp;Prévost&nbsp;»</b> — un nom de famille sans prénom. Impossible de
						dire de qui il s'agit.
					</li>
					<li>
						<b>«&nbsp;Varady A&nbsp;»</b> — une initiale à la place du prénom. Même problème.
					</li>
					<li>
						<b>«&nbsp;Pellerin&nbsp;»</b> — une imprimerie d'Épinal, pas une personne.
					</li>
					<li>
						<b>Les trois Mellet</b>, à Vitré — le père et ses deux fils sont nommés
						ensemble sur chacun de leurs dessins. Rien ne permet de les distinguer&nbsp;:
						aucun des trois n'est retenu.
					</li>
				</ul>
				<p>
					À l'inverse, deux personnes bien identifiées restent deux personnes, même quand
					les musées les nomment côte à côte&nbsp;: <b>Louis et Aimé Duthoit</b>, à Amiens,
					apparaissent sur les mêmes dessins, suivis chacun d'un point d'interrogation. Le
					musée hésite entre les deux frères. Chacun a sa fiche.
				</p>
				<p>
					Résultat de ce travail à ce jour&nbsp;: <strong>{nombre(registre.retenues)}</strong>
					orthographes rattachées à un artiste,
					<strong>{nombre(registre.ecartees)}</strong> écartées avec leur raison, et
					<strong>{nombre(registre.a_instruire)}</strong> qui n'ont pas encore été
					examinées. Un nom non examiné n'est pas un nom rejeté.
				</p>
			</article>

			<article>
				<h3><span class="rang">3</span> Ce que cette liste ne dit pas</h3>
				<p>
					Elle ne dit pas où se trouve le doute dans les musées de France. Elle en couvre
					<strong>{partVolume}&nbsp;%</strong>, et ce chiffre ne bougera qu'avec le
					travail de vérification, pas avec les collections.
				</p>
				<p>
					Elle ne dit pas non plus qui doute le plus. Les musées versent dans Joconde ce
					qu'ils veulent, quand ils le veulent&nbsp;: un musée absent de ces pages n'est
					pas un musée sans incertitudes, c'est souvent un musée qui n'a pas encore versé.
				</p>
				<p>
					Enfin, elle laisse volontairement de côté des cas qui passent pourtant tous les
					contrôles.
					{#if registre.hors_perimetre === 1}
						Un nom est dans ce cas&nbsp;:
					{:else}
						{nombre(registre.hors_perimetre)} noms sont dans ce cas&nbsp;:
					{/if}
					un fonds d'histoire naturelle de plusieurs milliers de planches, conservé dans un
					seul musée et noté d'un bout à l'autre «&nbsp;attribué à&nbsp;». La personne
					existe, le compte est juste — mais il ne s'agit pas d'une hésitation sur l'auteur
					d'une œuvre d'art.
				</p>
				<p class="renvoi">
					<a href="{base}/methode#les-maitres">Le détail de la méthode et ses limites&nbsp;→</a>
				</p>
			</article>
		</div>
	</section>

	<!-- 4. LA VISUALISATION, PUIS CE QUE CES MOTS VEULENT DIRE ------------------ -->
	<section class="graphique">
		<MentionsFrequentes {corpus} />
	</section>

	<section class="glossaire">
		<h2>Ce que ces mots veulent dire</h2>
		<p class="texte">
			Les huit formules, dans l'ordre du graphique. La couleur de chacune est la même
			partout sur le site.
		</p>
		<div class="zones">
			{#each TERRITOIRES as t (t.id)}
				<div class="zone">
					<h3>{t.titre}</h3>
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
	<section class="suite">
		<h2>Explorer, artiste par artiste</h2>
		<p class="texte">
			Chaque artiste a sa fiche&nbsp;: les mots employés à son sujet, la liste complète des
			œuvres concernées avec les phrases exactes des musées, et la carte des établissements
			qui les conservent.
		</p>
		<p class="renvoi">
			<a class="entree" href="{base}/les-presque">Explorer les artistes&nbsp;→</a>
		</p>
		<p class="prudence">
			Le projet reprend les formulations publiées par les musées. Il ne réattribue aucune
			œuvre et n'émet aucun avis sur les attributions.
		</p>
	</section>
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

	/* Les blocs LARGES de la page (chiffres, sélection, glossaire, graphique) se
	   bornent tous au même endroit : sans quoi chacun trouve sa propre limite et la
	   page n'a plus de colonne. Le texte courant, lui, reste plus étroit (44 rem). */
	.chiffres,
	.etapes,
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

	.tete {
		max-width: 52rem;
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

	/* --- 1. Le cas : image à gauche, propos à droite ------------------------- */
	.cas {
		display: grid;
		grid-template-columns: minmax(0, 20rem) minmax(0, 34rem);
		gap: clamp(1.5rem, 4vw, 3rem);
		align-items: start;
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

	.propos h2 {
		margin-top: 0;
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

	/* --- 2. Les chiffres essentiels ------------------------------------------ */
	.chiffres {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(14rem, 1fr));
		gap: var(--espace-4);
		margin: var(--espace-5) 0 0;
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

	/* --- 3. La sélection en trois temps -------------------------------------- */
	.etapes {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(19rem, 1fr));
		gap: clamp(1.5rem, 3vw, 2.5rem);
	}

	.etapes h3 {
		display: flex;
		align-items: baseline;
		gap: 0.5rem;
		margin: 0 0 var(--espace-3);
		font-size: var(--taille-m);
		line-height: 1.25;
	}

	.rang {
		flex: none;
		font-family: var(--police-ui);
		font-size: var(--taille-s);
		color: var(--accent-cobalt);
	}

	.etapes p {
		margin: 0 0 var(--espace-3);
		line-height: 1.6;
	}

	.exemples {
		margin: 0 0 var(--espace-3);
		padding-left: 1.1rem;
		line-height: 1.55;
	}

	.exemples li {
		margin-bottom: var(--espace-2);
	}

	/* --- Renvois et sortie ---------------------------------------------------- */
	.renvoi {
		margin: var(--espace-3) 0 0;
		font-family: var(--police-ui);
		font-size: var(--taille-s);
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

	/* --- 4 bis. Le glossaire des huit mentions ------------------------------- */
	.zones {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(17rem, 1fr));
		gap: clamp(1.5rem, 3vw, 2.5rem);
	}

	.zone h3 {
		margin: 0 0 var(--espace-3);
		padding-bottom: var(--espace-2);
		border-bottom: 1px solid var(--couleur-trait);
		font-family: var(--police-ui);
		font-size: var(--taille-xs);
		letter-spacing: 0.1em;
		text-transform: uppercase;
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
		.cas {
			grid-template-columns: minmax(0, 1fr);
		}

		.oeuvre {
			max-width: 20rem;
		}
	}
</style>
