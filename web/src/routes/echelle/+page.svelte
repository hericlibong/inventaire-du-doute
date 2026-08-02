<script>
	// « Comprendre les mentions » — chapitre autonome sur le vocabulaire muséal de la
	// prudence (architecture-editoriale.md §3). Referme la boucle laissée ouverte par
	// le retrait de la légende détaillée du répertoire. Quatre parties : introduction,
	// les trois territoires, les huit mentions, la vue d'ensemble chiffrée.
	// Direction B (2026-07-17) : la ligne de proximité porte les territoires une seule
	// fois (pas de démonstration décorative du spectre) ; hiérarchie et rythme
	// retravaillés ; plus de boîte grise.
	import { FAMILLE_PUBLIC } from '$lib/familles-public.js';
	import { TERRITOIRES } from '$lib/territoires.js';
	import { nombre, enLettres } from '$lib/joconde.js';
	import BarresMentions from '$lib/BarresMentions.svelte';
	import Spectre from '$lib/Spectre.svelte';

	let { data } = $props();
	const vue = data.vue;

	// Comptages par mention pour chaque série (objet code → nombre).
	const valGlobal = Object.fromEntries(vue.familles.map((f) => [f.code, f.global]));
	// Les DEUX panneaux comptent des notices distinctes : le total national à
	// gauche, celui de la liste à droite. La somme des profils de maîtres
	// compterait deux fois les notices qui nomment deux artistes (6 avec les 63
	// premiers, 157 depuis le lot du 2026-08-02) — elle ne peut pas porter un
	// libellé « notices » (decisions.md, 2026-07-22 ter).
	const valListe = Object.fromEntries(vue.familles.map((f) => [f.code, f.dans_liste_notices]));
	const totalGlobal = vue.totaux.doute_total; // 24 507
	const totalListe = vue.totaux.doute_notices_liste;
	// L'effectif de la liste vient des données : il a déjà changé deux fois
	// (27 → 63 → 103) et changera encore à chaque lot instruit.
	const nbNoms = vue.nb_maitres;

	// Échelle COMMUNE aux deux panneaux : la plus grande part observée, toutes séries
	// confondues (« attribué à » dans l'ensemble). Les barres deviennent comparables.
	const maxPart = Math.max(
		...vue.familles.flatMap((f) => [f.global / totalGlobal, f.dans_liste_notices / totalListe])
	);

	// Formule type affichée UNIQUEMENT là où elle apporte quelque chose (règle
	// anti-répétition déjà encodée dans familles-public.js). Nom générique « un
	// maître » (l'élision « d'un maître » est gérée par deNom).
	const formuleType = (code) =>
		FAMILLE_PUBLIC[code].montrerMention ? FAMILLE_PUBLIC[code].mention('un maître') : null;
</script>

<div class="page">
<header class="tete">
	<p class="kicker">Comprendre les mentions</p>
	<h1>Le langage de la prudence</h1>
	<div class="lead">
		<p>
			Un musée ne dit pas seulement qu'une œuvre est, ou n'est pas, d'un artiste. Quand
			il hésite, il l'écrit — avec des mots choisis. Chaque formule dit une chose
			différente&nbsp;: la <em>nature</em> du lien avec le nom de l'artiste, et sa
			<em>force</em>. Voici ces mots, ce qu'ils veulent dire, et lesquels reviennent.
		</p>
	</div>
	<p class="prudence">
		Le projet reprend les formulations publiées par les musées&nbsp;; il ne réattribue
		aucune œuvre.
	</p>
</header>

<!-- 2. Les trois territoires : la ligne, une fois, avec ses annotations -------- -->
<section class="bloc">
	<h2>Trois territoires, de la main du maître à sa seule influence</h2>
	<p class="texte">
		Les formules se rangent le long d'une même ligne&nbsp;: à gauche, l'œuvre est au
		plus près de la main de l'artiste&nbsp;; à droite, il n'en reste que le style. Entre
		les deux, tout son environnement.
	</p>
	<div class="ligne">
		<Spectre hauteur="8px" zones />
		<ol class="annot">
			{#each TERRITOIRES as t (t.id)}
				<li>{t.annotation}</li>
			{/each}
		</ol>
	</div>
</section>

<!-- 3. Les huit mentions ------------------------------------------------------- -->
<section class="bloc">
	<h2>Les huit mentions, une à une</h2>
	<p class="texte">
		Voici les huit formules, dans l'ordre de cette ligne. La couleur de chacune est la
		même partout dans le site.
	</p>
	<div class="mentions-cols">
		{#each TERRITOIRES as t (t.id)}
			<div class="mentions-zone" data-zone={t.id}>
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
	</div>
</section>

<!-- 4. Vue d'ensemble chiffrée ------------------------------------------------- -->
<section class="bloc">
	<h2>Ce que disent les chiffres</h2>
	<p class="texte">
		Sur l'ensemble des œuvres concernées, une formule revient bien plus souvent que les
		autres&nbsp;: «&nbsp;attribué à&nbsp;», qui reste au plus près de la main de
		l'artiste. Elle reste aussi la plus fréquente chez les {enLettres(nbNoms)} noms de
		référence de la rubrique «&nbsp;Explorer les artistes&nbsp;». Ce qui change, c'est la
		place qu'y prennent les liens plus indirects — l'école, l'atelier, la manière&nbsp;:
		«&nbsp;de son école&nbsp;» y pèse plus de quatre fois sa part dans l'ensemble de la
		base.
	</p>

	<div class="comparaison">
		<BarresMentions titre="Ensemble de Joconde" total={totalGlobal} valeurs={valGlobal} {maxPart} />
		<BarresMentions titre="Les {enLettres(nbNoms)} noms de référence" total={totalListe} valeurs={valListe} {maxPart} />
	</div>

	<p class="reserve">
		Une même notice peut porter plusieurs de ces mentions&nbsp;: les parts ne s'additionnent
		pas à 100&nbsp;% et ne se lisent pas comme les tranches d'un tout. Les copies assumées
		(«&nbsp;d'après&nbsp;»), qui ne sont pas un doute, sont comptées à part&nbsp;:
		{nombre(vue.copies_dapres.dont_d_apres)} notices. Enfin, un même musée peut peser lourd
		dans l'ensemble&nbsp;; ce détail relève de la page Méthode.
	</p>
</section>
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

	h1 {
		font-family: var(--police-titre);
		font-size: var(--taille-xl);
		margin: 0;
	}

	.tete {
		max-width: 52rem;
	}

	.lead p {
		font-size: var(--taille-m);
		line-height: 1.65;
		margin: var(--espace-3) 0 0;
	}

	/* Prudence : filet vermillon (accent d'alerte de la charte v2). */
	.prudence {
		margin-top: var(--espace-4);
		border-left: 2px solid var(--accent-vermillon);
		padding-left: var(--espace-3);
		font-style: italic;
		font-size: var(--taille-s);
		color: var(--couleur-encre-douce);
	}

	.bloc {
		margin-top: var(--espace-6);
	}

	.bloc h2 {
		font-family: var(--police-titre);
	}

	.texte {
		max-width: 46rem;
		line-height: 1.65;
	}

	/* --- Partie 2 : la ligne (Spectre) + annotations alignées sur les territoires. --- */
	.ligne {
		margin-top: var(--espace-4);
	}

	.annot {
		list-style: none;
		margin: var(--espace-3) 0 0;
		padding: 0;
		display: grid;
		grid-template-columns: 2fr 3fr 3fr;
		gap: var(--espace-4);
	}

	.annot li {
		font-family: var(--police-texte);
		font-style: italic;
		font-size: var(--taille-s);
		line-height: 1.4;
		color: var(--couleur-encre-douce);
		padding-right: var(--espace-3);
	}

	/* --- Partie 3 : trois colonnes de définitions, filet d'accent par territoire. --- */
	.mentions-cols {
		display: grid;
		grid-template-columns: 2fr 3fr 3fr;
		gap: var(--espace-6);
		margin-top: var(--espace-4);
	}

	.mentions-zone {
		border-top: 3px solid var(--couleur-trait);
		padding-top: var(--espace-3);
	}

	.mentions-zone[data-zone='plus-pres'] {
		border-top-color: var(--forme-attribue);
	}
	.mentions-zone[data-zone='autour'] {
		border-top-color: var(--forme-atelier);
	}
	.mentions-zone[data-zone='influence'] {
		border-top-color: var(--forme-maniere);
	}

	.zone-titre {
		font-family: var(--police-ui);
		font-weight: 700;
		font-size: var(--taille-s);
		letter-spacing: 0.04em;
		text-transform: uppercase;
		color: var(--couleur-encre);
		margin: 0 0 var(--espace-2);
	}

	.mentions {
		margin: 0;
	}

	.mention {
		padding: var(--espace-3) 0;
		border-top: var(--filet-clair);
	}

	.mention:first-of-type {
		border-top: none;
	}

	.mention dt {
		display: flex;
		align-items: baseline;
		gap: 0.5rem;
		font-weight: 600;
		margin-bottom: 0.15rem;
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
		font-size: var(--taille-s);
		color: var(--couleur-encre);
	}

	.formule {
		display: block;
		margin-top: 0.15rem;
		font-style: italic;
		color: var(--couleur-encre-douce);
	}

	/* --- Partie 4 : comparaison en barres, deux panneaux à échelle commune. --- */
	.comparaison {
		display: grid;
		grid-template-columns: 1fr 1fr;
		gap: var(--espace-6);
		margin: var(--espace-4) 0;
	}

	.reserve {
		max-width: 50rem;
		font-style: italic;
		font-size: var(--taille-s);
		color: var(--couleur-encre-douce);
		line-height: 1.55;
	}

	@media (max-width: 720px) {
		.annot,
		.mentions-cols,
		.comparaison {
			grid-template-columns: 1fr;
			gap: var(--espace-4);
		}
	}
</style>
