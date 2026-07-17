<script>
	// « Comprendre les mentions » — chapitre autonome sur le vocabulaire muséal de la
	// prudence (architecture-editoriale.md §3). Referme la boucle laissée ouverte par
	// le retrait de la légende détaillée du répertoire. Quatre parties : introduction,
	// les trois territoires, les huit mentions, la vue d'ensemble chiffrée.
	import { FAMILLE_PUBLIC } from '$lib/familles-public.js';
	import { TERRITOIRES } from '$lib/territoires.js';
	import { nombre } from '$lib/joconde.js';
	import BarresMentions from '$lib/BarresMentions.svelte';

	let { data } = $props();
	const vue = data.vue;

	// Comptages par mention pour chaque série (objet code → nombre).
	const valGlobal = Object.fromEntries(vue.familles.map((f) => [f.code, f.global]));
	const val27 = Object.fromEntries(vue.familles.map((f) => [f.code, f.dans_27]));
	const totalGlobal = vue.totaux.doute_total; // 24 507
	const total27 = vue.totaux.doute_dans_27; // 2 341

	// Échelle COMMUNE aux deux panneaux : la plus grande part observée, toutes séries
	// confondues (« attribué à » dans l'ensemble). Les barres deviennent comparables.
	const maxPart = Math.max(
		...vue.familles.flatMap((f) => [f.global / totalGlobal, f.dans_27 / total27])
	);

	// Formule type affichée UNIQUEMENT là où elle apporte quelque chose (règle
	// anti-répétition déjà encodée dans familles-public.js). Nom générique « un
	// maître » (l'élision « d'un maître » est gérée par deNom).
	const formuleType = (code) =>
		FAMILLE_PUBLIC[code].montrerMention ? FAMILLE_PUBLIC[code].mention('un maître') : null;
</script>

<h1>Comprendre les mentions</h1>

<!-- 1. Introduction éditoriale ------------------------------------------------ -->
<div class="intro">
	<p class="chapo">
		Un musée ne dit pas seulement qu'une œuvre est, ou n'est pas, d'un artiste. Quand
		il hésite, il l'écrit — avec des mots choisis. Selon les cas, il note que l'œuvre
		est sans doute de sa main, qu'elle sort de son atelier, qu'elle vient de son école,
		ou qu'elle reprend seulement son style. Chaque formule dit une chose différente&nbsp;:
		la <em>nature</em> du lien avec le nom de l'artiste, et sa <em>force</em>.
	</p>
	<p class="chapo">
		Cette page réunit ces formules, les explique en clair, et montre lesquelles
		reviennent le plus souvent.
	</p>
	<p class="prudence">
		Le projet reprend les formulations publiées par les musées&nbsp;; il ne réattribue
		aucune œuvre.
	</p>
</div>

<!-- 2. Les trois territoires --------------------------------------------------- -->
<section class="bloc">
	<h2>Trois territoires, de la main du maître à sa seule influence</h2>
	<p class="texte">
		Les formules se rangent le long d'une même ligne&nbsp;: à gauche, l'œuvre est au
		plus près de la main de l'artiste&nbsp;; à droite, il n'en reste que le style. Entre
		les deux, tout son environnement.
	</p>
	<ol class="progression">
		{#each TERRITOIRES as t (t.id)}
			<li class="zone" data-zone={t.id}>
				<span class="zone-titre">{t.titre}</span>
				<span class="zone-note">{t.annotation}</span>
			</li>
		{/each}
	</ol>
	<p class="fleche"><span>plus près de sa main</span><span aria-hidden="true">→</span><span>plus loin de sa main</span></p>
</section>

<!-- 3. Les huit mentions ------------------------------------------------------- -->
<section class="bloc">
	<h2>Les huit mentions, une à une</h2>
	<p class="texte">
		Voici les huit formules, dans l'ordre de cette ligne. La couleur de chacune est la
		même partout dans le site.
	</p>
	{#each TERRITOIRES as t (t.id)}
		<div class="mentions-zone">
			<h3 class="zone-titre">{t.titre}</h3>
			<dl class="mentions">
				{#each t.codes as code (code)}
					<div class="mention">
						<dt>
							<span class="pastille" style="background: {FAMILLE_PUBLIC[code].couleur}"></span>
							<span class="lib">{FAMILLE_PUBLIC[code].label}</span>
						</dt>
						<dd>
							{FAMILLE_PUBLIC[code].corps}
							{#if formuleType(code)}
								<span class="formule">Elle s'écrit par exemple «&nbsp;{formuleType(code)}&nbsp;».</span>
							{/if}
						</dd>
					</div>
				{/each}
			</dl>
		</div>
	{/each}
</section>

<!-- 4. Vue d'ensemble chiffrée ------------------------------------------------- -->
<section class="bloc">
	<h2>Ce que disent les chiffres</h2>
	<p class="texte">
		Dans l'ensemble des œuvres concernées, une formule domine largement&nbsp;:
		«&nbsp;attribué à&nbsp;», qui reste au plus près de la main de l'artiste. Mais parmi
		les vingt-sept noms de référence réunis dans «&nbsp;Les presque&nbsp;», les liens plus
		indirects — l'atelier, l'école, la manière — prennent beaucoup plus de place.
	</p>

	<div class="comparaison">
		<BarresMentions titre="Ensemble de Joconde" total={totalGlobal} valeurs={valGlobal} {maxPart} />
		<BarresMentions titre="Les 27 noms de référence" total={total27} valeurs={val27} {maxPart} />
	</div>

	<p class="reserve">
		Une même œuvre peut porter plusieurs de ces mentions&nbsp;: les parts ne s'additionnent
		pas à 100&nbsp;% et ne se lisent pas comme les tranches d'un tout. Les copies assumées
		(«&nbsp;d'après&nbsp;»), qui ne sont pas un doute, sont comptées à part&nbsp;:
		{nombre(vue.copies_dapres.dont_d_apres)} œuvres. Enfin, un même musée peut peser lourd
		dans l'ensemble&nbsp;; ce détail relève de la page Méthode.
	</p>
</section>

<style>
	h1 {
		font-family: var(--police-titre);
	}

	.intro {
		max-width: 44rem;
	}

	.chapo {
		font-size: var(--taille-m);
		line-height: 1.65;
	}

	.chapo:first-child {
		font-size: 1.2rem;
	}

	/* Phrase de prudence commune au projet : encart discret, registre « mention ». */
	.prudence {
		margin-top: var(--espace-4);
		padding: 0.6rem 0.9rem;
		background: rgba(122, 74, 43, 0.06);
		border-left: 3px solid var(--couleur-accent);
		border-radius: var(--rayon-s);
		font-size: var(--taille-s);
		font-family: var(--police-ui);
		color: var(--couleur-encre);
	}

	.bloc {
		margin-top: var(--espace-6);
	}

	.bloc h2 {
		font-family: var(--police-titre);
	}

	.texte {
		max-width: 44rem;
		line-height: 1.65;
	}

	/* --- Partie 2 : progression continue (une bande, pas trois cartes) --- */
	.progression {
		list-style: none;
		margin: var(--espace-4) 0 var(--espace-2);
		padding: 0;
		display: grid;
		grid-template-columns: repeat(3, 1fr);
		gap: 0;
		border: var(--filet);
		border-radius: var(--rayon-s);
		overflow: hidden;
	}

	.progression .zone {
		padding: var(--espace-4);
		border-left: var(--filet);
		display: flex;
		flex-direction: column;
		gap: 0.3rem;
	}

	.progression .zone:first-child {
		border-left: none;
	}

	.zone[data-zone='plus-pres'] {
		background: var(--territoire-pres);
	}
	.zone[data-zone='autour'] {
		background: var(--territoire-autour);
	}
	.zone[data-zone='influence'] {
		background: var(--territoire-influence);
	}

	.zone-titre {
		font-family: var(--police-ui);
		font-weight: 700;
		font-size: var(--taille-s);
		letter-spacing: 0.04em;
		text-transform: uppercase;
		color: var(--couleur-encre);
	}

	.zone-note {
		font-family: var(--police-texte);
		font-style: italic;
		color: var(--couleur-encre-douce);
		line-height: 1.4;
	}

	/* Micro-légende de progression, en italique. */
	.fleche {
		display: flex;
		align-items: center;
		justify-content: space-between;
		gap: var(--espace-3);
		max-width: 30rem;
		margin: 0.4rem 0 0;
		font-family: var(--police-texte);
		font-style: italic;
		font-size: var(--taille-s);
		color: var(--couleur-encre-douce);
	}

	.fleche span[aria-hidden] {
		flex: 1;
		text-align: center;
		font-style: normal;
		color: var(--couleur-trait);
		letter-spacing: 0.3em;
	}

	/* --- Partie 3 : les huit mentions, définitions scannables (pas de cartes) --- */
	.mentions-zone {
		margin-top: var(--espace-4);
	}

	.mentions-zone .zone-titre {
		margin: 0 0 var(--espace-2);
	}

	.mentions {
		margin: 0;
		max-width: 46rem;
	}

	.mention {
		display: grid;
		grid-template-columns: 9rem 1fr;
		gap: 0.4rem 1rem;
		padding: 0.5rem 0;
		border-top: var(--filet-clair);
	}

	.mention dt {
		display: flex;
		align-items: baseline;
		gap: 0.5rem;
		font-weight: 600;
	}

	.mention dt .lib {
		font-family: var(--police-texte);
	}

	.pastille {
		width: 0.65rem;
		height: 0.65rem;
		border-radius: 50%;
		flex: none;
		transform: translateY(1px);
	}

	.mention dd {
		margin: 0;
		line-height: 1.5;
		color: var(--couleur-encre);
	}

	.formule {
		display: block;
		margin-top: 0.15rem;
		font-style: italic;
		font-size: var(--taille-s);
		color: var(--couleur-encre-douce);
	}

	/* --- Partie 4 : comparaison en barres, deux panneaux à échelle commune --- */
	.comparaison {
		display: grid;
		grid-template-columns: 1fr 1fr;
		gap: var(--espace-6);
		margin: var(--espace-4) 0;
	}

	.reserve {
		max-width: 46rem;
		font-style: italic;
		font-size: var(--taille-s);
		color: var(--couleur-encre-douce);
		line-height: 1.55;
	}

	/* --- Responsive --- */
	@media (max-width: 640px) {
		.progression {
			grid-template-columns: 1fr;
		}
		.progression .zone {
			border-left: none;
			border-top: var(--filet);
		}
		.progression .zone:first-child {
			border-top: none;
		}
		.comparaison {
			grid-template-columns: 1fr;
			gap: var(--espace-5);
		}
		.mention {
			grid-template-columns: 1fr;
			gap: 0.2rem;
		}
	}
</style>
