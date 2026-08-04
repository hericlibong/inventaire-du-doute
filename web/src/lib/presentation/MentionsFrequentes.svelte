<script>
	// LE GRAPHIQUE DES MENTIONS — l'unique visualisation reprise du prototype
	// d'analyse (2026-08-01), renommée et rendue autonome le 2026-08-02.
	// Elle s'appelait « Le corpus », un mot de chantier que personne ne lit.
	//
	// Le titre de section (« Les mentions en chiffres ») est remonté dans la page
	// le 2026-08-04 : il coiffe désormais le bandeau de chiffres ET ce graphique.
	// Ce qui reste ici est le chapô du graphique seul — il l'introduit, à sa place,
	// juste avant les barres.
	//
	// Une colonne par mention, dans l'ordre de PROXIMITÉ à l'artiste — jamais par
	// valeur : c'est une échelle ordonnée, et c'est elle qui raconte quelque chose
	// (de sa main, à gauche, jusqu'à son seul style, à droite). La hauteur encode
	// la part : position et longueur, jamais une aire ni une intensité.
	//
	// UNITÉ : les notices distinctes du volume portant chaque mention. Leur somme
	// dépasse le nombre de notices, parce qu'une notice porte parfois deux de ces
	// mentions. La note sous le graphique le dit — c'est la seule façon honnête de
	// publier des parts qui ne font pas 100 %.
	//
	// Le prototype partageait sa grille, sa bande de tête et son état de survol
	// avec deux autres vues. Ces vues sont abandonnées : tout est réuni ici, et le
	// composant ne dépend plus que des nomenclatures publiques du projet.
	import { ORDRE_FAMILLES, FAMILLE_PUBLIC } from '$lib/familles-public.js';
	import { TERRITOIRES, indicesTerritoire } from '$lib/territoires.js';
	import { nombre, fractionEnMots } from '$lib/joconde.js';
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

	// Bande des trois territoires : elle donne le sens de lecture de l'axe. +2 car
	// la grille commence par la gouttière de gauche (l'axe chiffré).
	const zones = TERRITOIRES.map((t) => {
		const { debut, fin } = indicesTerritoire(t);
		return { ...t, colonne: `${debut + 2} / ${fin + 3}` };
	});

	// Phrase de lecture : elle NOMME des mentions, elle doit donc les chercher par
	// leur code, jamais par un rang (piège corrigé le 2026-07-22 — un classement
	// qui bascule, et la phrase se met à mentir).
	const part = (code) => corpus.mentions[code].corpus_notices / u.notices_distinctes;

	// « Plus de la moitié », « environ un tiers »… : la proportion est DITE, jamais
	// écrite en dur — un classement qui bascule et la phrase se met à mentir.
	const fractionEnMotsCap = (p) => {
		const mots = fractionEnMots(Math.round(p * 100));
		return mots.charAt(0).toUpperCase() + mots.slice(1);
	};
</script>

<figure class="mentions">
	<figcaption class="tete">
		<p class="sous-titre">
			Sur les {nombre(u.notices_distinctes)} notices de ce volume, voici les mots que les musées
			emploient. Ils sont rangés du plus proche de la main de l'artiste au plus lointain,
			jusqu'à ceux qui ne parlent plus que de son style.
		</p>
	</figcaption>

	<div class="cadre">
		<!-- Bande de tête : les trois territoires, écrits une seule fois. -->
		<div class="territoires">
			{#each zones as t (t.id)}
				<span class="territoire" style="grid-column: {t.colonne}">{t.titre}</span>
			{/each}
		</div>

		<div class="graphe" style="--max: {MAX}">
			<AxePourcent max={MAX} pas={0.1} />

			<div class="colonnes">
				{#each barres as b, i (b.code)}
					<div
						class="col"
						style="grid-column: {i + 2}; --part: {(b.part / MAX) * 100}%; --teinte: {b.f.couleur}"
					>
						<span class="chiffres">
							<b>{pourcent(b.part)}</b>
							<span class="brut">{nombre(b.notices)}</span>
						</span>
						<span class="piste">
							<span class="barre"></span>
						</span>
						<span class="lib">{b.f.label}</span>
					</div>
				{/each}
			</div>
		</div>

		<!-- Libellés sous l'axe (grand écran) : chaque barre porte son nom. -->
		<div class="pieds" aria-hidden="true">
			{#each barres as b, i (b.code)}
				<span class="pied" style="grid-column: {i + 2}">{b.f.label}</span>
			{/each}
		</div>
	</div>

	<p class="lecture">
		{fractionEnMotsCap(part('attribue'))} de ces notices portent la mention
		«&nbsp;attribué à&nbsp;»&nbsp;: {nombre(corpus.mentions.attribue.corpus_notices)} sur
		{nombre(u.notices_distinctes)}. Le musée donne un nom, et dit dans le même geste qu'il
		n'en est pas sûr. Vient ensuite «&nbsp;de son école&nbsp;»
		({pourcent(part('ecole_de'))}), qui ne parle plus de sa main mais de son milieu de
		travail&nbsp;: l'œuvre vient de là, pas de lui.
	</p>

	<p class="unite">
		Chaque barre compte des notices. Une notice porte parfois deux de ces mentions&nbsp;:
		on relève {nombre(u.occurrences_mentions)} mentions sur {nombre(u.notices_distinctes)}
		notices, et ces parts ne s'additionnent donc pas à 100&nbsp;%.
	</p>
</figure>

<style>
	.mentions {
		margin: 0;
		/* Grille commune à la bande de tête, aux barres et aux libellés de pied :
		   gouttière de l'axe | huit colonnes de mentions. Déclarée une seule fois. */
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

	.cadre {
		margin-top: var(--espace-5);
	}

	/* --- Bande des territoires : le sens de lecture de l'axe ------------------ */
	.territoires {
		display: grid;
		grid-template-columns: var(--colonnes-mentions);
		align-items: end;
		gap: 0 0.25rem;
		padding-bottom: 0.35rem;
		border-bottom: 1px solid var(--couleur-trait-clair);
	}

	.territoire {
		font-family: var(--police-ui);
		font-size: var(--taille-xs);
		letter-spacing: 0.04em;
		text-transform: uppercase;
		color: var(--couleur-encre-douce);
	}

	.graphe {
		--marge-haute: 2rem; /* place des chiffres au-dessus de la plus haute barre */
		position: relative;
		height: 18rem; /* hauteur de la ZONE DES BARRES (content-box) */
		padding-top: var(--marge-haute);
		margin-top: var(--espace-3);
	}

	.colonnes {
		display: grid;
		grid-template-columns: var(--colonnes-mentions);
		height: 100%;
	}

	/* Une colonne : la barre monte du bas à hauteur de sa part ; les chiffres se
	   posent JUSTE AU-DESSUS d'elle (hors du flux, sinon ils mangeraient la hauteur
	   disponible et la barre la plus haute chevaucherait l'axe). */
	.col {
		position: relative;
		display: flex;
		flex-direction: column;
		justify-content: flex-end;
		padding-right: 0.4rem;
		min-width: 0;
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

	.chiffres {
		position: absolute;
		left: 0;
		bottom: var(--part);
		padding-bottom: 0.2rem;
		display: flex;
		flex-direction: column;
		line-height: 1.15;
		white-space: nowrap;
		font-family: var(--police-ui);
		font-variant-numeric: tabular-nums;
	}

	.chiffres b {
		font-size: var(--taille-s);
		color: var(--couleur-encre);
	}

	.brut {
		font-size: var(--taille-xs);
		color: var(--couleur-encre-douce);
	}

	/* Le libellé dans la colonne ne sert qu'au mobile ; sur grand écran il est
	   porté par la ligne de pied, sous l'axe. */
	.lib {
		display: none;
	}

	.pieds {
		display: grid;
		grid-template-columns: var(--colonnes-mentions);
		gap: 0 0.25rem;
		margin-top: 0.4rem;
		padding-top: 0.4rem;
	}

	.pied {
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

	.unite {
		max-width: 44rem;
		margin: var(--espace-3) 0 0;
		font-family: var(--police-ui);
		font-size: var(--taille-xs);
		line-height: 1.5;
		color: var(--couleur-encre-douce);
	}

	/* --- Mobile : huit lignes, même ordre, mêmes couleurs. --------------------- */
	@media (max-width: 760px) {
		.territoires,
		.pieds {
			display: none;
		}

		.graphe {
			height: auto;
			padding-top: 0;
			margin-top: var(--espace-4);
		}

		.colonnes {
			display: flex;
			flex-direction: column;
			gap: 0.35rem;
		}

		.col {
			display: grid;
			grid-template-columns: 6.5rem 1fr auto;
			grid-column: auto !important;
			align-items: center;
			gap: 0.5rem;
			padding-right: 0;
		}

		.lib {
			display: block;
			order: -1;
			font-family: var(--police-texte);
			font-size: var(--taille-s);
			text-align: right;
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

		.chiffres {
			position: static;
			padding-bottom: 0;
			order: 1;
			flex-direction: row;
			align-items: baseline;
			gap: 0.4rem;
			white-space: nowrap;
		}
	}
</style>
