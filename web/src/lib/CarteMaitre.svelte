<script>
	// Carte par maître (decisions.md 2026-07-12, taille fixe retenue après test A/B).
	// Une seule question : D'OÙ viennent les notices concernées — présence et
	// distribution des musées, pas leur classement. Tous les points ont la MÊME
	// taille : une taille variable rendrait un « gros cercle » incomparable d'une
	// fiche à l'autre (échelle propre au maître) et gonflerait de petits volumes.
	// Le COMBIEN par musée reste au survol (tooltip) et dans l'onglet Graphique.
	// Couleur unique et stable. Le fond des régions est une illustration (IGN via
	// france-geojson), jamais une donnée.
	import { onMount } from 'svelte';
	import { base } from '$app/paths';
	import Infobulle from '$lib/Infobulle.svelte';
	import { nombre, lienPop } from '$lib/joconde.js';
	import { FAMILLE_PUBLIC, notices } from '$lib/familles-public.js';
	import { estProjetable, creerProjection, creerChemin, normaliserFond, ecarterPoints } from '$lib/geo.js';

	// `onVoirOeuvres(code)` remonte à la page le musée choisi : elle pose le filtre
	// et bascule sur l'onglet « Œuvres ». La carte ne filtre rien elle-même — il n'y
	// a qu'un seul système de filtrage, et son état vit dans la page (phase 2).
	let { maitre, onVoirOeuvres = null } = $props();

	// Repère fixe du dessin (le SVG scale via viewBox, la projection est calée sur
	// ces mêmes nombres → les points tombent au bon endroit quel que soit l'écran).
	const W = 420;
	const H = 460;
	const R_POINT = 5; // rayon identique pour tous les musées (présence)

	// Fond des régions, chargé une fois (statique servi sous /geo).
	let fond = $state(null);
	onMount(async () => {
		const r = await fetch(`${base}/geo/regions-metropole.geojson`);
		fond = normaliserFond(await r.json());
	});

	// Séparer ce qui se projette (métropole) de ce qui reste compté mais hors cadre.
	const projetables = $derived(maitre.musees_doute.filter((m) => estProjetable(m.lat, m.lon)));
	const horsCadre = $derived(maitre.musees_doute.filter((m) => !estProjetable(m.lat, m.lon)));

	// TOUS LES ARTISTES ONT LEUR CARTE, même ceux dont le doute n'est écrit que dans
	// un seul musée (arbitrage utilisateur, 2026-08-02). Une règle antérieure
	// remplaçait la carte par une phrase en dessous de deux musées projetables, au
	// motif qu'un point unique « ne montre pas une répartition ». Le malentendu
	// était là : cette carte n'est pas un graphique de répartition, c'est un REPÈRE
	// GÉOGRAPHIQUE. Un point unique situe l'artiste aussi sûrement que vingt, et
	// l'échelle ne bouge pas — la projection est calée sur le fond de carte, jamais
	// sur les points (geo.js, creerProjection). Trente-deux des cent deux artistes
	// sont dans ce cas.

	// « N notice(s) concernée(s) » — accord géré par notices(), puis participe accordé.
	const concernees = (n) => `${notices(n)} concernée${n > 1 ? 's' : ''}`;

	// Intitulé de l'action, accordé au singulier comme au pluriel.
	const voirOeuvres = (n) =>
		n === 1 ? 'Voir l’œuvre conservée dans ce musée' : `Voir les ${nombre(n)} œuvres conservées dans ce musée`;

	// Ventilation du musée par FAMILLE PUBLIQUE (jamais de niveau ni de jargon),
	// triée par valeur décroissante (dataviz : trier par valeur). Chaque ligne
	// porte le libellé public et la couleur STABLE de la famille (pastille).
	function ventilation(m) {
		return m.familles
			.slice()
			.sort((a, b) => b.notices - a.notices)
			.map((f) => ({
				label: FAMILLE_PUBLIC[f.code].header,
				valeur: nombre(f.notices),
				couleur: FAMILLE_PUBLIC[f.code].couleur
			}));
	}

	// Points prêts à dessiner (tous de même taille). On écarte ceux qui se
	// chevauchent (musées d'une même ville, grappe francilienne) pour qu'aucun n'en
	// cache un autre — au plus près de leur vraie position (voir ecarterPoints).
	const points = $derived.by(() => {
		if (!fond) return [];
		const projection = creerProjection(fond, W, H);
		const bruts = projetables.map((m) => {
			const [x, y] = projection([m.lon, m.lat]);
			const lignes = ventilation(m);
			const detail = lignes.map((l) => `${l.label} ${l.valeur}`).join(', ');
			// TOUS les points se choisissent, et de la même façon (2026-08-02,
			// phase 3). Le point à une seule notice était auparavant un lien direct
			// vers POP : ce lien n'est pas perdu, il a rejoint le panneau du musée,
			// où il reste lisible et cliquable — un lien utile ne doit pas dépendre
			// d'une infobulle qui s'efface au premier mouvement de souris.
			const ou = m.doute === 1 ? m.oeuvre_unique : null;
			return {
				code: m.code,
				x,
				y,
				nom: m.nom,
				ville: m.ville,
				doute: m.doute,
				lignes,
				oeuvreUnique: ou ?? null,
				tt: {
					header: `${m.nom}, ${m.ville}`,
					valeur: concernees(m.doute),
					titre: ou?.titre || null,
					lignes
				},
				resume: `${m.nom}, ${m.ville} : ${concernees(m.doute)}. ${detail}. ` +
					`Choisir ce musée pour ${voirOeuvres(m.doute).toLowerCase()}.`
			};
		});
		return ecarterPoints(bruts, 2 * R_POINT + 1.5);
	});

	// Tracé des régions (contours discrets).
	const regions = $derived.by(() => {
		if (!fond) return [];
		const path = creerChemin(creerProjection(fond, W, H));
		return fond.features.map((f) => path(f));
	});

	// Tooltip HTML custom, positionné dans le conteneur (même grammaire que le nuage).
	let regardEl;
	let actif = $state(null);
	function montre(event, p) {
		const cible = event.currentTarget.getBoundingClientRect();
		const hote = regardEl.getBoundingClientRect();
		const y = cible.top + cible.height / 2 - hote.top;
		actif = {
			tt: p.tt,
			x: cible.left + cible.width / 2 - hote.left,
			y,
			dessous: y < 90
		};
	}
	function cache() {
		actif = null;
	}

	// --- Musée CHOISI : persistant, à la différence du survol -------------------
	// Le survol renseigne, le choix engage. Deux états distincts, comme sur le
	// graphique du profil : l'infobulle s'efface dès qu'on bouge, le panneau reste
	// tant qu'on ne le ferme pas — c'est lui qui porte les liens.
	let choisi = $state(null); // code Muséofile
	const musee = $derived(points.find((p) => p.code === choisi) ?? null);

	// Changer d'artiste referme le panneau : un code de musée ne vaut que pour
	// l'artiste où il a été choisi.
	$effect(() => {
		maitre.nom;
		choisi = null;
	});

	function choisir(code) {
		choisi = choisi === code ? null : code;
		// Le panneau prend le relais de l'infobulle : la laisser ouverte afficherait
		// deux fois la même chose côte à côte, et elle recouvre le titre de la vue
		// (C8, 2026-08-03). Le survol renseigne, le choix engage — pas les deux.
		actif = null;
	}

	function auClavier(event, code) {
		if (event.key === 'Enter' || event.key === ' ') {
			event.preventDefault();
			choisir(code);
		}
	}
</script>

<figure class="carte">
	<figcaption class="titre">D'où viennent ces notices</figcaption>

	<div class="agencement">
		<div class="scene" bind:this={regardEl}>
			<svg viewBox="0 0 {W} {H}" role="img" aria-label="Carte des musées de France ayant publié des notices où le nom de {maitre.nom} est accompagné d’une formulation prudente">
				<!-- Fond régions : illustration discrète, aucune donnée. -->
				{#each regions as d, i (i)}
					<path {d} class="region" />
				{/each}
				<!-- Un point = un musée (tous de même taille, et tous choisissables de
				     la même façon : souris, toucher, Entrée ou Espace). Le survol
				     renseigne, le choix ouvre le panneau au flanc — c'est lui qui porte
				     les liens, jamais l'infobulle. -->
				{#each points as p (p.code)}
					<circle
						cx={p.x}
						cy={p.y}
						r={R_POINT}
						class="point"
						class:choisi={choisi === p.code}
						tabindex="0"
						role="button"
						aria-pressed={choisi === p.code}
						aria-label={p.resume}
						onclick={() => choisir(p.code)}
						onkeydown={(e) => auClavier(e, p.code)}
						onmouseenter={(e) => montre(e, p)}
						onmouseleave={cache}
						onfocus={(e) => montre(e, p)}
						onblur={cache}
					/>
				{/each}
			</svg>

			{#if actif}
				<Infobulle tt={actif.tt} x={actif.x} y={actif.y} dessous={actif.dessous} />
			{/if}
		</div>

		<div class="flanc">
			<!-- Panneau du musée choisi : le seul endroit où vivent les liens. Il
			     remplace la légende tant qu'un musée est choisi. -->
			{#if musee}
				<div class="panneau-musee" role="group" aria-label="Musée choisi">
					<p class="panneau-nom">{musee.nom}<span class="panneau-ville">{musee.ville}</span></p>
					<p class="panneau-compte">{concernees(musee.doute)}</p>
					<ul class="panneau-mentions">
						{#each musee.lignes as l (l.label)}
							<li>
								<span class="pastille" style="background: {l.couleur}"></span>
								<span class="mention-label">{l.label}</span>
								<span class="mention-n">{l.valeur}</span>
							</li>
						{/each}
					</ul>
					{#if onVoirOeuvres}
						<button type="button" class="action" onclick={() => onVoirOeuvres(musee.code)}>
							{voirOeuvres(musee.doute)}&nbsp;→
						</button>
					{/if}
					{#if musee.oeuvreUnique}
						<!-- Le lien POP du musée à une seule notice, conservé : il a quitté
						     le point pour ce panneau, où il reste cliquable. -->
						<a class="lien-pop" href={lienPop(musee.oeuvreUnique.reference)} target="_blank" rel="noreferrer">
							Voir la fiche publique{musee.oeuvreUnique.titre ? ` de « ${musee.oeuvreUnique.titre} »` : ''}&nbsp;→
						</a>
					{/if}
					<button type="button" class="fermer" onclick={() => (choisi = null)}>Fermer</button>
				</div>
			{:else}
				<!-- Légende : un seul repère de point (présence). Le nombre de notices par
				     musée se lit au survol, pas dans la taille. -->
				<div class="legende">
					<svg class="repere" viewBox="0 0 {2 * R_POINT} {2 * R_POINT}" width={2 * R_POINT} height={2 * R_POINT} aria-hidden="true">
						<circle cx={R_POINT} cy={R_POINT} r={R_POINT} class="point" />
					</svg>
					<p class="legende-texte">
						Un point = un musée ayant publié au moins une notice concernée.
						Passez sur un point pour voir combien, et sous quelles formules&nbsp;;
						choisissez-le pour ouvrir ses œuvres.
					</p>
				</div>
			{/if}
		</div>
	</div>
	{#if projetables.length === 0}
		<p class="repli">
			Aucune de ces notices ne relève d'un musée de France métropolitaine.
		</p>
	{/if}

	{#if horsCadre.length > 0}
		{@const total = horsCadre.reduce((s, m) => s + m.doute, 0)}
		<p class="hors-cadre">
			Hors cadre métropolitain&nbsp;:
			{#if horsCadre.length === 1}
				{notices(total)} rattachée{total > 1 ? 's' : ''} au {horsCadre[0].nom},
				à {horsCadre[0].ville}.
				{#if onVoirOeuvres}
					<button type="button" class="action action-en-ligne" onclick={() => onVoirOeuvres(horsCadre[0].code)}>
						{voirOeuvres(horsCadre[0].doute)}&nbsp;→
					</button>
				{/if}
			{:else}
				{notices(total)} rattachées à {nombre(horsCadre.length)} musées hors
				métropole (outre-mer ou étranger).
			{/if}
		</p>
	{/if}
</figure>

<style>
	/* Direction B : la carte occupe l'espace. Plus de colonne bornée à 32 rem —
	   une grande carte à gauche, la légende et les mentions au flanc. */
	.carte {
		margin: 0;
	}

	.titre {
		font-family: var(--police-titre);
		font-size: var(--taille-l);
		line-height: 1.2;
		color: var(--couleur-encre);
		margin: 0 0 var(--espace-4);
	}

	/* Grande carte (colonne large) + flanc (légende, hors-cadre). */
	.agencement {
		display: grid;
		grid-template-columns: minmax(0, 1.9fr) 1fr;
		gap: var(--espace-6);
		align-items: start;
	}

	.scene {
		position: relative; /* repère du tooltip positionné en absolu */
	}

	.flanc {
		position: sticky;
		top: var(--espace-4);
	}

	@media (max-width: 720px) {
		.agencement {
			grid-template-columns: 1fr;
			gap: var(--espace-4);
		}
		.flanc {
			position: static;
		}
	}

	svg {
		width: 100%;
		height: auto;
		display: block;
	}

	/* Fond = illustration discrète (choix « régions très estompées », 2026-07-13) :
	   aplat quasi nul, frontières régionales en trait gris très pâle. Repère
	   géographique sans jamais concurrencer les points. */
	.region {
		fill: rgba(122, 74, 43, 0.03);
		stroke: rgba(92, 85, 76, 0.25);
		stroke-width: 0.5;
	}

	.point {
		fill: var(--carte-point);
		fill-opacity: 0.82;
		stroke: #fff;
		stroke-width: 1.1;
		transition: fill-opacity 0.12s, stroke-width 0.12s;
	}

	/* Survol/focus FRANC : pleine opacité + halo blanc plus large → le point
	   survolé « se lève » du fond. Tous les points sont choisissables, le retour
	   est donc le même pour tous. */
	.point:focus,
	.point:hover {
		fill-opacity: 1;
		stroke-width: 1.8;
		outline: none;
	}

	.point {
		cursor: pointer;
	}

	.point:focus-visible {
		outline: 2px solid var(--couleur-encre);
		outline-offset: 2px;
	}

	/* Point CHOISI : le seul état persistant de la carte. Cerné d'encre, pour se
	   distinguer du survol (qui, lui, s'efface). */
	.point.choisi {
		fill-opacity: 1;
		stroke: var(--couleur-encre);
		stroke-width: 2.2;
	}

	/* --- Panneau du musée choisi : il porte les liens, l'infobulle jamais. --- */
	.panneau-musee {
		display: flex;
		flex-direction: column;
		align-items: flex-start;
		gap: var(--espace-2);
		padding: var(--espace-3);
		background: var(--surface-carte);
		border: 1px solid var(--couleur-trait);
		border-radius: var(--rayon-s);
	}

	.panneau-nom {
		margin: 0;
		font-family: var(--police-ui);
		font-size: var(--taille-xs);
		font-weight: 600;
		line-height: 1.3;
		color: var(--couleur-encre);
	}

	.panneau-ville {
		display: block;
		font-weight: 400;
		color: var(--couleur-encre-douce);
	}

	.panneau-compte {
		margin: 0;
		font-family: var(--police-ui);
		font-size: var(--taille-xs);
		color: var(--couleur-encre-douce);
	}

	.panneau-mentions {
		margin: 0;
		padding: 0;
		list-style: none;
		display: flex;
		flex-direction: column;
		gap: 0.2rem;
		width: 100%;
		font-family: var(--police-ui);
		font-size: var(--taille-xs);
	}

	.panneau-mentions li {
		display: flex;
		align-items: baseline;
		gap: 0.4rem;
	}

	.pastille {
		flex: none;
		width: 0.5rem;
		height: 0.5rem;
		border-radius: 50%;
	}

	.mention-label {
		flex: 1;
		color: var(--couleur-encre-douce);
	}

	.mention-n {
		font-variant-numeric: tabular-nums;
		color: var(--couleur-encre);
	}

	/* Action principale : c'est elle qui relie la carte aux œuvres. */
	.action {
		font-family: var(--police-ui);
		font-size: var(--taille-xs);
		text-align: left;
		color: var(--couleur-accent);
		background: none;
		border: 0;
		padding: 0;
		text-decoration: underline;
		cursor: pointer;
	}

	.action-en-ligne {
		display: inline;
	}

	.action:focus-visible,
	.lien-pop:focus-visible,
	.fermer:focus-visible {
		outline: var(--focus-anneau);
		outline-offset: 2px;
	}

	.lien-pop {
		font-family: var(--police-ui);
		font-size: var(--taille-xs);
		color: var(--couleur-encre-douce);
	}

	.fermer {
		font-family: var(--police-ui);
		font-size: var(--taille-xs);
		color: var(--couleur-encre-douce);
		background: none;
		border: 0;
		padding: 0;
		text-decoration: underline;
		cursor: pointer;
	}


	.legende {
		display: flex;
		align-items: baseline;
		gap: 0.55rem;
		flex-wrap: wrap;
	}

	.repere {
		flex: none;
		width: 10px;
		height: 10px;
	}

	.legende-texte {
		flex: 1;
		min-width: 11rem;
		margin: 0;
		font-size: 0.8rem;
		line-height: 1.45;
		color: var(--couleur-encre-douce);
	}

	/* Phrase de repli : c'est le contenu quand il n'y a pas de carte → lisible,
	   pas une note de bas de page. */
	.repli {
		font-size: 0.95rem;
		line-height: 1.45;
		color: var(--couleur-encre);
	}

	/* Mention hors-cadre : même registre que la légende (petit corps, encre douce,
	   filet de séparation). */
	.hors-cadre {
		margin-top: 0.7rem;
		padding-top: 0.55rem;
		border-top: 1px solid var(--couleur-trait);
		font-size: 0.8rem;
		font-style: italic;
		line-height: 1.45;
		color: var(--couleur-encre-douce);
	}
</style>
