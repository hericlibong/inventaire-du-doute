<script>
	// LE GRAPHIQUE DES MENTIONS — l'unique visualisation reprise du prototype
	// d'analyse (2026-08-01), renommée et rendue autonome le 2026-08-02.
	// Elle s'appelait « Le corpus », un mot de chantier que personne ne lit.
	//
	// Le titre de section (« Les mentions en chiffres ») est remonté dans la page
	// le 2026-08-04 : il coiffe désormais le bandeau de chiffres ET ce graphique.
	// Ce qui reste ici est le chapô du graphique seul.
	//
	// REFONTE DU 2026-08-04 — ce que le lecteur doit pouvoir lire sans mode d'emploi :
	//   hauteur de la barre  = fréquence de la mention (intitulé d'axe, axe gradué) ;
	//   position horizontale = groupe auquel elle appartient (trois zones dessinées) ;
	//   couleur              = la mention elle-même (pigment stable du projet).
	// Les trois groupes ne sont plus une bande de titres flottant au-dessus des
	// colonnes : ce sont trois ZONES continues, fond léger et limites nettes, qui
	// englobent leur titre, leurs barres et leurs libellés. Le titre appartient à
	// sa zone parce qu'il est DANS son cadre, pas parce qu'il est au-dessus.
	//
	// INTERACTION : elle porte sur la zone, jamais sur une colonne isolée — survol,
	// focus clavier ou toucher mettent en évidence les trois ou deux mentions du
	// groupe et atténuent les autres. AUCUNE infobulle : les valeurs exactes (part
	// et nombre de notices) sont écrites au-dessus de chaque barre, en permanence.
	//
	// UNITÉ : les notices distinctes du volume portant chaque mention. Leur somme
	// dépasse le nombre de notices, parce qu'une notice porte parfois deux de ces
	// mentions. La note sous le graphique le dit — c'est la seule façon honnête de
	// publier des parts qui ne font pas 100 %.
	import { ORDRE_FAMILLES, FAMILLE_PUBLIC } from '$lib/familles-public.js';
	import { TERRITOIRES, indicesTerritoire } from '$lib/territoires.js';
	import { nombre } from '$lib/joconde.js';
	import AxePourcent from '$lib/presentation/AxePourcent.svelte';

	let { corpus } = $props();

	const u = corpus.unites;
	const barres = ORDRE_FAMILLES.map((code) => ({
		code,
		f: FAMILLE_PUBLIC[code],
		notices: corpus.mentions[code].corpus_notices,
		part: corpus.mentions[code].corpus_notices / u.notices_distinctes
	}));

	// Échelle arrondie au palier de 5 points au-dessus du maximum observé : la
	// barre la plus haute ne touche pas le plafond du cadre.
	const MAX = Math.ceil(Math.max(...barres.map((b) => b.part)) * 20) / 20;

	// Pourcentage public : un chiffre rond, et jamais « 0 % » sous une barre visible.
	const pourcent = (p) => (p > 0 && p < 0.005 ? '< 1 %' : `${Math.round(p * 100)} %`);

	// Habillage de chaque zone. Les fonds sont des TOKENS existants, écrits pour
	// cet usage (tokens.css : « fonds TRÈS légers derrière les groupes de
	// mentions ») ; le trait reprend le pigment REPÈRE de la zone. Passés en
	// variables inline plutôt qu'en classes `zone-{id}` : une classe construite à
	// l'exécution ferait passer les sélecteurs pour du CSS mort à la compilation.
	const HABILLAGE = {
		'plus-pres': { fond: 'var(--territoire-pres)', trait: 'var(--forme-attribue)' },
		autour: { fond: 'var(--territoire-autour)', trait: 'var(--forme-atelier)' },
		influence: { fond: 'var(--territoire-influence)', trait: 'var(--forme-maniere)' }
	};

	// Une zone = un titre, ses colonnes contiguës, sa place dans la grille. +2 car
	// la grille commence par la gouttière de gauche (l'axe chiffré).
	const parCode = Object.fromEntries(barres.map((b) => [b.code, b]));
	const zones = TERRITOIRES.map((t) => {
		const { debut, fin } = indicesTerritoire(t);
		return {
			...t,
			colonne: `${debut + 2} / ${fin + 3}`,
			barres: t.codes.map((c) => parCode[c]),
			habillage: HABILLAGE[t.id]
		};
	});

	// Les deux mentions les plus fréquentes, cherchées PAR LEUR VALEUR : le constat
	// sous le graphique les nomme, il ne doit pas les écrire en dur (un classement
	// qui bascule, et la phrase se met à mentir — piège corrigé le 2026-07-22).
	const [premiere, seconde] = barres.slice().sort((a, b) => b.notices - a.notices);

	// Mise en évidence d'une zone. Deux états : le survol (ou le focus), qui suit le
	// lecteur, et l'ÉPINGLE, posée au clic ou au toucher — sans quoi rien ne tient
	// sur un écran tactile, où il n'y a pas de survol. Refermer : retoucher la même
	// zone, ou Échap.
	let zoneActive = $state(null);
	let epinglee = $state(false);

	// Le survol se pose et se retire zone par zone (`mouseenter` / `mouseleave` sur
	// chaque groupe) plutôt qu'au niveau du cadre : passer d'une zone à sa voisine
	// déclenche la sortie AVANT l'entrée, l'enchaînement se fait donc sans clignoter.
	const survoler = (id) => {
		if (!epinglee) zoneActive = id;
	};
	const quitter = () => {
		if (!epinglee) zoneActive = null;
	};
	const basculer = (id) => {
		const meme = epinglee && zoneActive === id;
		epinglee = !meme;
		zoneActive = meme ? null : id;
	};
	const fermer = () => {
		epinglee = false;
		zoneActive = null;
	};
</script>

<figure class="mentions">
	<figcaption class="tete">
		<p class="sous-titre">
			Les barres indiquent la fréquence des huit mentions dans les notices de ce volet. Elles
			sont regroupées en trois ensembles selon le lien qu'elles décrivent avec l'artiste.
		</p>
	</figcaption>

	<!-- Intitulé de l'axe vertical, écrit à l'horizontale : une légende tournée à
	     90° se lit mal, et la phrase est trop longue pour la gouttière. -->
	<p class="intitule">Part des notices dans lesquelles cette mention apparaît</p>

	<div class="cadre">
		<div class="grille">
			<!-- L'axe gradué occupe la seule ligne des barres ; sa marge haute est
			     remise à zéro, la grille lui réserve déjà une ligne d'air au-dessus. -->
			<div class="axe-hote">
				<AxePourcent max={MAX} pas={0.1} />
			</div>

			{#each zones as z (z.id)}
				<div
					class="groupe"
					class:active={zoneActive === z.id}
					class:attenuee={zoneActive !== null && zoneActive !== z.id}
					style="grid-column: {z.colonne}; --n: {z.barres.length};
					       --fond-zone: {z.habillage.fond}; --trait-zone: {z.habillage.trait}"
					role="group"
					aria-labelledby="zone-{z.id}"
					onmouseenter={() => survoler(z.id)}
					onmouseleave={quitter}
				>
					<!-- Le titre EST la commande de la zone : son ::after couvre tout le
					     cadre, si bien qu'un clic ou un toucher n'importe où dans la zone
					     l'atteint, sans second bouton invisible dans l'arbre d'accessibilité. -->
					<button
						class="titre-zone"
						id="zone-{z.id}"
						type="button"
						aria-pressed={epinglee && zoneActive === z.id}
						onfocus={() => survoler(z.id)}
						onblur={quitter}
						onclick={() => basculer(z.id)}
						onkeydown={(e) => e.key === 'Escape' && fermer()}
					>
						{z.titre}
					</button>

					{#each z.barres as b, i (b.code)}
						<div
							class="col"
							style="grid-column: {i + 1}; --part: {(b.part / MAX) * 100}%; --teinte: {b.f
								.couleur}"
						>
							<span class="cellule">
								<span class="valeurs">
									<b>{pourcent(b.part)}</b>
									<span class="brut">{nombre(b.notices)}</span>
								</span>
								<span class="piste">
									<span class="barre"></span>
								</span>
							</span>
							<span class="lib">{b.f.label}</span>
						</div>
					{/each}
				</div>
			{/each}
		</div>
	</div>

	<p class="lecture">
		Dans cette sélection, «&nbsp;{premiere.f.label}&nbsp;» est la mention la plus
		fréquente&nbsp;; «&nbsp;{seconde.f.label}&nbsp;» arrive ensuite.
	</p>

	<p class="precision">
		La hauteur des barres indique une fréquence, pas un degré de certitude sur l'attribution.
	</p>
	<p class="precision">
		Une même notice pouvant contenir plusieurs mentions, les pourcentages ne s'additionnent pas
		nécessairement à 100&nbsp;%.
	</p>
</figure>

<style>
	.mentions {
		margin: 0;
		/* Grille commune au graphique et à l'axe gradué : gouttière de l'axe | huit
		   colonnes de mentions. Déclarée une seule fois. */
		--colonnes-mentions: 3rem repeat(8, minmax(0, 1fr));
	}

	.tete {
		max-width: 44rem;
	}

	.sous-titre {
		margin: 0;
		line-height: 1.6;
		color: var(--couleur-encre-douce);
	}

	.intitule {
		margin: var(--espace-5) 0 var(--espace-2);
		font-family: var(--police-ui);
		font-size: var(--taille-xs);
		color: var(--couleur-encre-douce);
	}

	/* La grille porte les QUATRE lignes du graphique, communes aux trois zones :
	   titre · air pour les valeurs · barres · libellés. Chaque zone s'y accroche en
	   sous-grille : c'est ce qui garde les barres et les libellés alignés d'un
	   groupe à l'autre, quelle que soit la hauteur des titres.
	   Le contexte d'empilement (z-index: 0) retient les fonds de zone, posés en
	   arrière-plan avec z-index: -1. */
	.grille {
		position: relative;
		z-index: 0;
		display: grid;
		grid-template-columns: var(--colonnes-mentions);
		grid-template-rows: auto var(--marge-haute) 18rem auto;
		--marge-haute: 2rem;
	}

	.axe-hote {
		grid-row: 3;
		grid-column: 1 / -1;
		position: relative;
		--marge-haute: 0; /* l'axe couvre sa ligne, l'air est déjà au-dessus */
	}

	/* --- Une zone : trois ou deux mentions dans un même cadre ----------------- */
	.groupe {
		position: relative;
		grid-row: 1 / -1;
		display: grid;
		grid-template-rows: subgrid;
		grid-template-columns: repeat(var(--n), minmax(0, 1fr));
		transition: opacity 0.15s ease;
	}

	/* Le fond et les limites de la zone. `inset: 0 2px` ménage la gouttière qui
	   sépare nettement deux zones voisines. */
	.groupe::before {
		content: '';
		position: absolute;
		inset: 0 2px;
		z-index: -1;
		background: var(--fond-zone);
		border: 1px solid var(--couleur-trait-clair);
		border-radius: var(--rayon-s);
		transition:
			background 0.15s ease,
			border-color 0.15s ease;
	}

	.groupe.active::before {
		background: color-mix(in srgb, var(--trait-zone) 12%, transparent);
		border-color: var(--trait-zone);
	}

	/* Les deux autres zones reculent d'un cran — assez pour que l'œil suive celle
	   qu'on désigne, pas au point de rendre leurs valeurs illisibles. */
	.groupe.attenuee {
		opacity: 0.45;
	}

	.titre-zone {
		grid-row: 1;
		grid-column: 1 / -1;
		margin: 0;
		padding: 0.4rem 0.55rem;
		background: none;
		border: 0;
		border-bottom: 1px solid var(--couleur-trait-clair);
		font-family: var(--police-ui);
		font-size: var(--taille-xs);
		letter-spacing: 0.04em;
		text-transform: uppercase;
		color: var(--couleur-encre-douce);
		text-align: left;
		cursor: pointer;
	}

	/* Toute la zone est la surface sensible, titre et barres compris. */
	.titre-zone::after {
		content: '';
		position: absolute;
		inset: 0;
		z-index: 2;
		border-radius: var(--rayon-s);
	}

	.titre-zone:focus-visible {
		outline: none;
	}

	.titre-zone:focus-visible::after {
		outline: var(--focus-anneau);
		outline-offset: 2px;
	}

	.groupe.active .titre-zone {
		color: var(--couleur-encre);
		border-bottom-color: var(--trait-zone);
	}

	/* --- Une colonne : sa barre, ses deux valeurs, son libellé ---------------- */
	.col {
		grid-row: 3 / 5;
		display: grid;
		grid-template-rows: subgrid;
		padding-right: 0.4rem;
		min-width: 0;
	}

	/* La cellule fait exactement la hauteur de l'échelle : la barre s'y appuie en
	   bas, et les valeurs se posent JUSTE au-dessus d'elle, hors du flux (sinon
	   elles mangeraient la hauteur disponible). */
	.cellule {
		grid-row: 1;
		position: relative;
		display: flex;
		flex-direction: column;
		justify-content: flex-end;
		padding-left: 0.55rem;
	}

	.piste {
		display: block;
		height: var(--part);
		min-height: 2px; /* une valeur non nulle reste visible ; zéro n'affiche rien */
	}

	.barre {
		display: block;
		height: 100%;
		background: var(--teinte);
		border-radius: 2px 2px 0 0;
	}

	.valeurs {
		position: absolute;
		left: 0.55rem;
		bottom: var(--part);
		padding-bottom: 0.2rem;
		display: flex;
		flex-direction: column;
		line-height: 1.15;
		white-space: nowrap;
		font-family: var(--police-ui);
		font-variant-numeric: tabular-nums;
	}

	.valeurs b {
		font-size: var(--taille-s);
		color: var(--couleur-encre);
	}

	.brut {
		font-size: var(--taille-xs);
		color: var(--couleur-encre-douce);
	}

	.lib {
		grid-row: 2;
		padding: 0.4rem 0 0.5rem 0.55rem;
		font-family: var(--police-ui);
		font-size: var(--taille-xs);
		line-height: 1.25;
		color: var(--couleur-encre-douce);
		hyphens: auto;
	}

	.lecture {
		max-width: 44rem;
		margin: var(--espace-5) 0 0;
		line-height: 1.6;
	}

	/* Deux précisions distinctes, en mentions techniques : ce que la hauteur mesure,
	   et pourquoi les parts ne font pas 100 %. */
	.precision {
		max-width: 44rem;
		margin: var(--espace-3) 0 0;
		font-family: var(--police-ui);
		font-size: var(--taille-xs);
		line-height: 1.5;
		color: var(--couleur-encre-douce);
	}

	/* --- Mobile : les mêmes trois zones, l'une sous l'autre -------------------
	   Les groupes ne deviennent pas invisibles quand la place manque : ils
	   redeviennent trois blocs titrés, chacun avec ses mentions en lignes. Même
	   ordre, mêmes couleurs, même interaction. */
	@media (max-width: 760px) {
		.grille {
			display: block;
			grid-template-rows: none;
		}

		.axe-hote {
			display: none;
		}

		.groupe {
			display: block;
			padding-bottom: var(--espace-3);
			margin-bottom: var(--espace-4);
		}

		.groupe::before {
			inset: 0;
		}

		.titre-zone {
			display: block;
			width: 100%;
			margin-bottom: var(--espace-3);
		}

		.col {
			display: grid;
			grid-template-columns: 6.5rem 1fr auto;
			grid-template-rows: none;
			grid-row: auto;
			align-items: center;
			gap: 0.5rem;
			padding: 0.2rem 0.55rem;
		}

		/* Les trois éléments de la ligne remontent au niveau de la grille. */
		.cellule {
			display: contents;
		}

		/* La piste redevient une gouttière pleine largeur (l'échelle se lit sur elle,
		   puisque l'axe gradué disparaît) et la barre la remplit à hauteur de sa part. */
		.piste {
			height: 0.7rem;
			min-height: 0;
			background: var(--couleur-trait-clair);
			border-radius: 2px;
			overflow: hidden;
		}

		.barre {
			width: var(--part);
			min-width: 2px;
			border-radius: 2px;
		}

		.valeurs {
			position: static;
			order: 1;
			flex-direction: row;
			align-items: baseline;
			gap: 0.4rem;
			padding-bottom: 0;
			left: auto;
		}

		.lib {
			grid-row: auto;
			order: -1;
			padding: 0;
			text-align: right;
			font-family: var(--police-texte);
			font-size: var(--taille-s);
			color: var(--couleur-encre);
		}
	}

	@media (prefers-reduced-motion: reduce) {
		.groupe,
		.groupe::before {
			transition: none;
		}
	}
</style>
