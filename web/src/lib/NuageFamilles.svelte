<script>
	import { FAMILLE_PUBLIC, ORDRE_FAMILLES, tooltipFamille, resumeFamille } from '$lib/familles-public.js';
	import { TERRITOIRES, indicesTerritoire } from '$lib/territoires.js';
	import { phraseRepartition } from '$lib/phrase-repartition.js';
	import Infobulle from '$lib/Infobulle.svelte';

	// Comparable entre maîtres (decisions.md 2026-07-08). Scatter sur grille FIXE :
	// axe X = familles (mêmes colonnes pour tous), axe Y = PART des œuvres
	// concernées du maître, de 0 à 100 %. Depuis 2026-07-17, l'axe est recadré en
	// TROIS TERRITOIRES de proximité (territoires.js) : le graphe donne à voir le
	// principe éditorial central — la distance à la main du maître.
	//
	// L'axe portait le NOMBRE d'œuvres, sur un plafond commun (le maximum de tous
	// les maîtres, 240). Il a changé le 2026-07-22, quand la liste est passée de 27
	// à 63 maîtres : de 11 à 310 œuvres concernées, la moitié des profils
	// s'écrasaient au sol d'une échelle graduée jusqu'à 240 — plus aucune hiérarchie
	// lisible, donc « la forme est mauvaise » (CLAUDE.md). La part rend chaque
	// profil lisible ET garde une échelle commune et fixe, la comparaison portant
	// sur la FORME du profil. Le volume, lui, n'est pas perdu : il est écrit dans le
	// bandeau, classé dans le répertoire, et donné en nombre exact dans chaque
	// infobulle (« 30 œuvres sur 37 — 81 % »).
	let { maitre } = $props();

	// Axe X ordonné par distance narrative au maître (docs/typologie.md), labels
	// publics et couleur stable par famille — tous deux depuis familles-public.js
	// (source unique, partagée avec la vitrine « Œuvres »). Même ordre pour tous →
	// l'axe se lit de gauche (presque lui) à droite (seulement son style).
	const FAMILLES = ORDRE_FAMILLES.map((code) => ({
		code,
		label: FAMILLE_PUBLIC[code].label,
		couleur: FAMILLE_PUBLIC[code].couleur
	}));

	// Géométrie SVG. Un bandeau de tête (0 → Y_BANDE_HAUT) accueille les titres de
	// territoire ; les bandes de fond descendent de là jusqu'à la ligne de base. Le
	// plot commence assez bas (Y_HAUT) pour qu'un point à 100 % ne morde pas sur
	// les titres.
	const X0 = 30, X_LARG = 342, Y_HAUT = 40, Y_HAUTEUR = 196;
	const Y_BASE = Y_HAUT + Y_HAUTEUR;
	const Y_BANDE_HAUT = 18; // haut des bandes de territoire (sous les titres)
	const pas = X_LARG / FAMILLES.length;
	const bordG = (i) => X0 + pas * i; // bord gauche de la colonne i
	const colonneX = (i) => X0 + pas * (i + 0.5);
	// Part des œuvres concernées du maître (0 → 1). Le dénominateur est son propre
	// total prudent : une notice ne relève que d'une famille (invariant du temps 1),
	// les parts somment donc exactement à 100 %.
	const part = (v) => (maitre.doute ? v / maitre.doute : 0);
	const y = (v) => Y_BASE - part(v) * Y_HAUTEUR;
	// position d'une graduation exprimée en pourcentage (l'axe, pas les points)
	const yPart = (p) => Y_BASE - (p / 100) * Y_HAUTEUR;
	// Rayon VARIABLE (rétabli le 2026-07-27, choix utilisateur) : plus la mention
	// est fréquente, plus le point est gros — de 6 (part nulle) à 16 (100 %). La
	// taille constante essayée le 2026-07-23 est abandonnée. Le point ACTIF est
	// agrandi de +2 par-dessus sa taille propre (survol/focus/sélection).
	const rayon = (v) => 6 + part(v) * 10;
	const RENFORT_ACTIF = 2;

	// Bandes de territoire : plages de colonnes contiguës, calculées depuis la
	// primitive (territoires.js) et l'ordre de l'axe. x1/x2 = bords des colonnes.
	const bandes = TERRITOIRES.map((t, i) => {
		const { debut, fin } = indicesTerritoire(t, ORDRE_FAMILLES);
		const x1 = bordG(debut);
		const x2 = bordG(fin + 1);
		return { id: t.id, titre: t.titre, x1, x2, cx: (x1 + x2) / 2, premier: i === 0 };
	});

	// Graduations fixes, identiques sur les 63 fiches : un quart, la moitié, etc.
	const graduations = [25, 50, 75, 100];

	const points = $derived(
		FAMILLES.map((f, i) => {
			const fam = maitre.familles.find((g) => g.code === f.code);
			if (!fam) return null;
			return {
				...f,
				x: colonneX(i),
				cy: y(fam.notices),
				notices: fam.notices,
				tt: tooltipFamille(f.code, maitre.nom, fam.notices),
				resume: resumeFamille(f.code, maitre.nom, fam.notices)
			};
		}).filter(Boolean)
	);

	// --- Interaction graphique ↔ légende : UN SEUL état partagé (2026-07-27) ------
	// `interaction` pilote À LA FOIS le point actif, l'entrée de légende active et
	// l'ouverture de l'infobulle. Deux modes dans le même objet :
	//   temporaire  — survol ou focus (souris/clavier), refermé au départ / au blur ;
	//   selectionne — clic, Entrée, Espace ou toucher : persistant jusqu'à un second
	//                 appui, une autre sélection, Échap ou un appui extérieur.
	// `ancre` dit OÙ placer l'infobulle : au POINT (défaut) ou, si le point est hors
	// de la fenêtre (mobile, légende sous le graphe), sous la MENTION de la légende.
	// Le tooltip <title> SVG natif reste abandonné (décision 2026-07-10).
	let regardEl;
	let svgEl;
	let interaction = $state(null); // { code, mode, source, ancre, x?, y?, dessous? }

	// Un changement d'artiste remet l'interaction à zéro.
	$effect(() => {
		maitre.nom;
		interaction = null;
	});

	// Mentions RÉELLEMENT présentes (un point existe) et leur compte : sert le nom
	// accessible de la légende et écarte les mentions absentes (non interactives).
	const compte = $derived(new Map(maitre.familles.map((f) => [f.code, f.notices])));
	const present = (code) => compte.has(code);
	const pointActif = $derived(
		interaction ? points.find((p) => p.code === interaction.code) ?? null : null
	);

	// Position de l'infobulle : TOUJOURS les coordonnées réelles du point dans le
	// SVG. Exception (repli mobile) : si le point est hors de la fenêtre et que
	// l'activation vient de la légende, on ancre sous la mention (ancre = legende).
	function positionner(code, source) {
		const circle = svgEl?.querySelector(`circle[data-code="${code}"]`);
		if (!circle || !regardEl) return { ancre: 'point', x: 0, y: 0, dessous: false };
		const c = circle.getBoundingClientRect();
		const hote = regardEl.getBoundingClientRect();
		const visible = c.top >= 0 && c.bottom <= window.innerHeight;
		if (source === 'legende' && !visible) return { ancre: 'legende' };
		const y = c.top - hote.top;
		return { ancre: 'point', x: c.left + c.width / 2 - hote.left, y, dessous: y < 90 };
	}

	// Ouvre (ou remplace) l'interaction. Un SURVOL n'écrase jamais une sélection.
	function ouvrir(code, mode, source) {
		if (!present(code)) return;
		if (mode === 'temporaire' && interaction?.mode === 'selectionne') return;
		interaction = { code, mode, source, ...positionner(code, source) };
	}

	// Ferme une activation TEMPORAIRE seulement (départ souris / perte de focus) :
	// une sélection persistante survit au survol qui passe.
	function relacher() {
		if (interaction?.mode === 'temporaire') interaction = null;
	}

	// Sélection persistante : bascule (un second appui sur la même mention ferme).
	// stopPropagation empêche le gestionnaire fenêtre de refermer aussitôt.
	function selectionner(event, code, source) {
		event?.stopPropagation();
		if (!present(code)) return;
		if (interaction?.mode === 'selectionne' && interaction.code === code) {
			interaction = null;
			return;
		}
		ouvrir(code, 'selectionne', source);
	}

	function fermer() {
		interaction = null;
	}

	// Nom accessible d'une mention de la légende : libellé + nombre + pourcentage.
	function nomAccessible(code) {
		const n = compte.get(code) ?? 0;
		const mot = n === 1 ? 'œuvre' : 'œuvres';
		const pct = maitre.doute ? Math.round((n / maitre.doute) * 100) : 0;
		return `${FAMILLE_PUBLIC[code].label}, ${n} ${mot}, ${pct} %`;
	}

	// Opacité d'un point : plein s'il est actif, atténué si un AUTRE est actif.
	const opacite = (code) => (!interaction ? 0.9 : interaction.code === code ? 1 : 0.35);

	// Titre STABLE, identique pour tous les artistes (2026-07-23) : le graphique
	// répond à « comment se répartissent les mentions ? ». Le nom de l'artiste est
	// déjà porté par le bandeau, on ne le répète pas. Les anciens titres littéraires
	// (editorial-maitres.js) restent archivés dans les données mais ne commandent
	// plus l'interface. La phrase factuelle sous le titre suit une règle déterministe
	// unique (phrase-repartition.js), testée hors bundler.
	const titre = 'Répartition des mentions';
	const sousTitre = $derived(
		phraseRepartition(maitre.familles, maitre.doute, {
			label: (c) => FAMILLE_PUBLIC[c].label,
			ordre: ORDRE_FAMILLES
		})
	);
</script>

<svelte:window
	onclick={fermer}
	onkeydown={(e) => {
		if (e.key === 'Escape') fermer();
	}}
/>

<figure class="nuage">
	<!-- En-tête du graphique (2026-07-23) : titre STABLE « Répartition des mentions »
	     (le nom de l'artiste vit dans le bandeau, pas ici) ; sous-titre = une phrase
	     factuelle générée par règle déterministe (phrase-repartition.js). -->
	<figcaption class="entete">
		<h3 class="titre-graphe">{titre}</h3>
		{#if sousTitre}
			<p class="lecture">{sousTitre}</p>
		{/if}
	</figcaption>

	<div class="agencement">
	<div class="graphe-hote" bind:this={regardEl}>
		<svg bind:this={svgEl} viewBox="0 0 380 300" class="graphe" role="img"
			aria-label="Graphique des mentions de doute pour {maitre.nom}, en trois territoires de proximité (au plus près, autour du maître, dans son influence). Axe vertical : part des œuvres concernées, de 0 à 100 %, échelle commune à tous les maîtres">
			<!-- Bandes de territoire (fond très léger) : posées EN PREMIER, sous tout le
			     reste. Contiguës, sans marge ni cadre → une seule ligne de proximité,
			     pas trois blocs séparés. -->
			{#each bandes as b (b.id)}
				<rect
					x={b.x1}
					y={Y_BANDE_HAUT}
					width={b.x2 - b.x1}
					height={Y_BASE - Y_BANDE_HAUT}
					class="bande"
					data-zone={b.id}
				/>
			{/each}

			<!-- graduations horizontales + valeurs -->
			{#each graduations as g (g)}
				<line x1={X0} x2={X0 + X_LARG} y1={yPart(g)} y2={yPart(g)} class="grille" />
				<text x={X0 - 5} y={yPart(g) + 3} text-anchor="end" class="axe-y">{g} %</text>
			{/each}

			<!-- Séparateurs entre territoires : hairline discrète aux frontières
			     internes (pas de bord au début du premier). -->
			{#each bandes as b (b.id)}
				{#if !b.premier}
					<line x1={b.x1} x2={b.x1} y1={Y_BANDE_HAUT} y2={Y_BASE} class="separateur" />
				{/if}
			{/each}

			<!-- ligne de base (zéro) -->
			<line x1={X0} x2={X0 + X_LARG} y1={Y_BASE} y2={Y_BASE} class="base" />
			<text x={X0 - 5} y={Y_BASE + 3} text-anchor="end" class="axe-y">0</text>

			<!-- Titres de territoire, centrés sur leur bande, en tête du graphe. -->
			{#each bandes as b (b.id)}
				<text x={b.cx} y={12} text-anchor="middle" class="titre-zone">{b.titre}</text>
			{/each}

			<!-- libellés publics de familles (axe X, inclinés) -->
			{#each FAMILLES as f, i (f.code)}
				<text
					x={colonneX(i)}
					y={Y_BASE + 12}
					text-anchor="end"
					class="axe-x"
					transform="rotate(-42 {colonneX(i)} {Y_BASE + 12})">{f.label}</text
				>
			{/each}

			<!-- points : survol/focus → activation temporaire ; clic/Entrée/Espace/toucher
			     → sélection persistante (état partagé avec la légende). `data-code`
			     permet à la légende de retrouver la position réelle du point.
			     aria-label = repli textuel pour lecteur d'écran. -->
			{#each points as p (p.code)}
				<circle
					data-code={p.code}
					cx={p.x}
					cy={p.cy}
					r={interaction && interaction.code === p.code
						? rayon(p.notices) + RENFORT_ACTIF
						: rayon(p.notices)}
					style="fill: {p.couleur}"
					fill-opacity={opacite(p.code)}
					stroke="#fff"
					stroke-width="0.7"
					class="point"
					tabindex="0"
					role="button"
					aria-label={p.resume}
					onpointerenter={() => ouvrir(p.code, 'temporaire', 'point')}
					onpointerleave={relacher}
					onfocus={() => ouvrir(p.code, 'temporaire', 'point')}
					onblur={relacher}
					onclick={(e) => selectionner(e, p.code, 'point')}
					onkeydown={(e) => {
						if (e.key === 'Enter' || e.key === ' ') {
							e.preventDefault();
							selectionner(e, p.code, 'point');
						}
					}}
				/>
			{/each}
		</svg>

		<!-- Infobulle ancrée AU POINT (cas normal). Le contenu accessible passe par
		     l'aria-label du point. -->
		{#if pointActif && interaction?.ancre === 'point'}
			<Infobulle
				tt={pointActif.tt}
				x={interaction.x}
				y={interaction.y}
				dessous={interaction.dessous}
			/>
		{/if}
	</div>

	<!-- Clé de lecture : passée EN COLONNE À DROITE du graphe (2026-07-20), elle ne
	     s'intercale plus entre le graphique et la suite de la page. Légende légère :
	     ni cadre, ni fond plein — un filet de couleur par zone suffit à rappeler les
	     bandes du graphe. Libellés depuis la source unique (familles-public.js). -->
	<!-- Pas de phrase d'introduction (retirée le 2026-07-25) : les trois intitulés
	     de territoire et la légende suffisent à expliquer l'organisation. -->
	<div class="cle">
		<ol class="territoires">
			{#each TERRITOIRES as t (t.id)}
				<li class="zone" data-zone={t.id}>
					<!-- Les titres de territoire NE sont PAS interactifs (seules les huit
					     mentions le sont). -->
					<span class="zone-titre">{t.titre}</span>
					<span class="zone-mentions">
						{#each t.codes as code (code)}
							{#if present(code)}
								<!-- Mention présente : vrai bouton, symétrique du point. Survol/focus
								     → activation temporaire ; clic/Entrée/Espace → sélection. -->
								<button
									type="button"
									class="mention"
									class:active={interaction?.code === code}
									class:selectionne={interaction?.mode === 'selectionne' &&
										interaction.code === code}
									aria-pressed={interaction?.mode === 'selectionne' &&
										interaction.code === code}
									aria-label={nomAccessible(code)}
									onpointerenter={() => ouvrir(code, 'temporaire', 'legende')}
									onpointerleave={relacher}
									onfocus={() => ouvrir(code, 'temporaire', 'legende')}
									onblur={relacher}
									onclick={(e) => selectionner(e, code, 'legende')}
								>
									<span
										class="pastille"
										style="background: {FAMILLE_PUBLIC[code].couleur}"
									></span>
									<span class="mention-label">{FAMILLE_PUBLIC[code].label}</span>
								</button>
								<!-- Repli mobile : quand le point est hors de la fenêtre, l'infobulle
								     s'affiche EN FLUX, sous la mention active. -->
								{#if interaction?.ancre === 'legende' && interaction.code === code && pointActif}
									<Infobulle tt={pointActif.tt} enFlux />
								{/if}
							{:else}
								<!-- Mention absente : ni bouton, ni focus, ni curseur d'interaction ;
								     libellé atténué + indication accessible. -->
								<span class="mention absente">
									<span
										class="pastille"
										style="background: {FAMILLE_PUBLIC[code].couleur}"
									></span>
									<span class="mention-label">{FAMILLE_PUBLIC[code].label}</span>
									<span class="visuellement-cache"> — aucune œuvre concernée</span>
								</span>
							{/if}
						{/each}
					</span>
				</li>
			{/each}
		</ol>
	</div>
	</div>
</figure>

<style>
	.nuage {
		margin: 0;
	}

	/* --- En-tête : le graphe est le portrait d'un artiste, il porte son nom. --- */
	.entete {
		margin: 0 0 var(--espace-4);
	}

	.titre-graphe {
		font-family: var(--police-titre);
		font-size: var(--taille-l);
		line-height: 1.2;
		margin: 0;
	}

	/* Phrase de lecture : ce que dit la forme du profil, en clair. */
	.lecture {
		margin: var(--espace-2) 0 0;
		font-size: var(--taille-m);
		line-height: 1.5;
		max-width: 42rem;
		color: var(--couleur-encre);
	}

	/* --- Deux colonnes : le graphe garde la place, la légende tient le flanc. --- */
	.agencement {
		display: grid;
		grid-template-columns: minmax(0, 7fr) minmax(11rem, 3fr);
		gap: var(--espace-5);
		align-items: start;
	}

	.graphe-hote {
		position: relative; /* repère du tooltip HTML positionné en absolu */
	}

	.point {
		cursor: pointer;
		/* l'opacité est portée par l'attribut fill-opacity (état d'interaction) */
		transition: fill-opacity 0.12s ease, r 0.1s ease;
	}

	.point:focus-visible {
		outline: 2px solid var(--couleur-encre);
		outline-offset: 1px;
	}

	/* Les styles du panneau d'infobulle vivent dans Infobulle.svelte (partagé). */

	.graphe {
		display: block;
		width: 100%;
		height: auto;
	}

	/* Bandes de territoire : lavis très légers, une température par zone. */
	.bande[data-zone='plus-pres'] {
		fill: var(--territoire-pres);
	}
	.bande[data-zone='autour'] {
		fill: var(--territoire-autour);
	}
	.bande[data-zone='influence'] {
		fill: var(--territoire-influence);
	}

	.separateur {
		stroke: var(--couleur-trait);
		stroke-width: 1;
	}

	.titre-zone {
		font-family: var(--police-ui);
		font-size: 8.5px;
		font-weight: 600;
		letter-spacing: 0.04em;
		fill: var(--couleur-encre-douce);
		text-transform: uppercase;
	}

	.grille {
		stroke: var(--couleur-trait);
		stroke-width: 1;
		stroke-dasharray: 2 4;
	}

	.base {
		stroke: var(--couleur-encre-douce);
		stroke-width: 1;
	}

	.axe-y {
		font-size: 9px;
		fill: var(--couleur-encre-douce);
		font-variant-numeric: tabular-nums;
	}

	.axe-x {
		font-size: 9px;
		fill: var(--couleur-encre);
	}

	/* Clé de lecture en colonne : légère, sans cadre ni fond plein. Un filet de
	   couleur à gauche de chaque zone rappelle les bandes du graphe. */
	.cle {
		padding-top: 2.5rem; /* aligne la légende sur le haut du plot, pas sur le SVG */
	}

	.territoires {
		list-style: none;
		margin: 0;
		padding: 0;
		display: flex;
		flex-direction: column;
		gap: var(--espace-3);
	}

	.zone {
		display: flex;
		flex-direction: column;
		gap: 0.25rem;
		padding-left: 0.6rem;
		border-left: 3px solid var(--couleur-trait);
	}

	.zone[data-zone='plus-pres'] {
		border-left-color: var(--forme-attribue);
	}
	.zone[data-zone='autour'] {
		border-left-color: var(--forme-ecole);
	}
	.zone[data-zone='influence'] {
		border-left-color: var(--forme-maniere);
	}

	.zone-titre {
		font-family: var(--police-ui);
		font-size: 0.72rem;
		font-weight: 700;
		letter-spacing: 0.04em;
		text-transform: uppercase;
		color: var(--couleur-encre);
	}

	.zone-mentions {
		display: flex;
		flex-direction: column;
		gap: 0.2rem;
	}

	/* Mention PRÉSENTE = vrai bouton (reset des styles natifs), symétrique du point. */
	.mention {
		display: flex;
		align-items: center;
		gap: 0.4rem;
		width: 100%;
		margin: 0;
		padding: 0.12rem 0.3rem;
		font-family: inherit;
		font-size: 0.8rem;
		text-align: left;
		color: var(--couleur-encre);
		background: none;
		border: 0;
		border-radius: 3px;
		transition: background 0.1s ease;
	}

	button.mention {
		cursor: pointer;
	}

	button.mention:focus-visible {
		outline: 2px solid var(--couleur-encre);
		outline-offset: 1px;
	}

	/* État ACTIF (survol/focus, temporaire OU sélectionné) — signalé AUSSI hors
	   couleur : fond léger, graisse, libellé souligné. */
	.mention.active {
		background: rgba(43, 30, 20, 0.08);
		font-weight: 600;
	}
	.mention.active .mention-label {
		text-decoration: underline;
		text-underline-offset: 2px;
	}

	/* SÉLECTION persistante : un filet encadre en plus, distinct du simple survol. */
	.mention.selectionne {
		box-shadow: inset 0 0 0 1px var(--couleur-encre-douce);
	}

	/* Mention ABSENTE : non interactive, atténuée, curseur normal. */
	.mention.absente {
		color: var(--couleur-encre-douce);
		opacity: 0.55;
		cursor: default;
	}

	.pastille {
		width: 0.6rem;
		height: 0.6rem;
		border-radius: 50%;
		flex: none;
	}

	/* Visible pour les lecteurs d'écran, masqué à l'affichage. */
	.visuellement-cache {
		position: absolute;
		width: 1px;
		height: 1px;
		padding: 0;
		margin: -1px;
		overflow: hidden;
		clip: rect(0 0 0 0);
		white-space: nowrap;
		border: 0;
	}

	/* Tablette et mobile : la légende repasse SOUS le graphique (une colonne de 30 %
	   deviendrait illisible), et ses trois zones s'étalent tant qu'il y a la place. */
	@container (max-width: 46rem) {
		.agencement {
			grid-template-columns: 1fr;
			gap: var(--espace-4);
		}
		.cle {
			padding-top: 0;
		}
		.territoires {
			flex-direction: row;
			flex-wrap: wrap;
			gap: var(--espace-4);
		}
		.zone {
			flex: 1 1 10rem;
		}
	}

	@container (max-width: 30rem) {
		.territoires {
			flex-direction: column;
			gap: var(--espace-3);
		}
		/* Sans cela, le flex-grow du palier précédent étire chaque zone en HAUTEUR
		   une fois la liste repassée en colonne (filets de couleur démesurés). */
		.zone {
			flex: 0 0 auto;
		}
	}
</style>
