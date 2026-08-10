<script>
	// Carte par maître (decisions.md 2026-07-12, taille fixe retenue après test A/B).
	// Une seule question : OÙ sont conservées les œuvres concernées — présence et
	// distribution des musées, pas leur classement. Tous les points ont la MÊME
	// taille : une taille variable rendrait un « gros cercle » incomparable d'une
	// fiche à l'autre (échelle propre au maître) et gonflerait de petits volumes.
	// Couleur unique et stable. Le fond des régions est une illustration (IGN via
	// france-geojson), jamais une donnée.
	//
	// UN SEUL ESPACE D'INFORMATION depuis le 2026-08-06 : le panneau. L'infobulle
	// qui suivait le pointeur a été retirée — elle disait la même chose que le
	// panneau, s'effaçait au premier mouvement, recouvrait le titre de la vue, et
	// n'existait pas au toucher. Le survol ne renseigne plus : il ANNONCE que le
	// point se choisit (il grossit, son contour se renforce, les autres s'atténuent),
	// et le clic ouvre le panneau. Le clavier reçoit exactement le même retour.
	import { onMount } from 'svelte';
	import { base } from '$app/paths';
	import { nombre, lienPop } from '$lib/joconde.js';
	import { FAMILLE_PUBLIC } from '$lib/familles-public.js';
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

	// Vocabulaire de la vue : « œuvre », jamais « notice » (É1, 2026-08-03 — le mot
	// du lecteur d'un côté, celui de la méthode de l'autre). L'unité de calcul, elle,
	// ne bouge pas : c'est toujours la référence Joconde.
	const concernees = (n) =>
		`${nombre(n)} œuvre${n > 1 ? 's' : ''} concernée${n > 1 ? 's' : ''}`;

	// Intitulé de l'action, accordé au singulier comme au pluriel.
	const voirOeuvres = (n) => (n === 1 ? 'Voir l’œuvre' : `Voir les ${nombre(n)} œuvres`);

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
				// Nom accessible du point : tout ce que le panneau dira, dit d'avance.
				// Un lecteur d'écran n'a jamais eu l'infobulle ; il ne perd donc rien à
				// sa disparition, et il sait ce qu'ouvre le point avant de l'activer.
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

	// --- Musée CHOISI : le seul état de la carte -------------------------------
	// Il persiste jusqu'à ce qu'on choisisse un autre musée ou qu'on ferme le
	// panneau. Rien d'autre ne s'affiche au passage de la souris.
	let choisi = $state(null); // code Muséofile
	const musee = $derived(points.find((p) => p.code === choisi) ?? null);
	let sceneEl = $state();
	let popupEl = $state();
	let popup = $state({ left: 0, top: 0, flecheX: 24, placement: 'dessous', pret: false });

	// Changer d'artiste referme le panneau : un code de musée ne vaut que pour
	// l'artiste où il a été choisi.
	$effect(() => {
		maitre.nom;
		choisi = null;
	});

	// Sur mobile, le panneau devient une bulle attachée au point. Sa position est
	// calculée après son rendu réel : les musées à une œuvre et ceux à plusieurs
	// œuvres n'ont pas la même hauteur.
	function positionnerPopup(code = choisi) {
		if (!code || !sceneEl || !popupEl || !window.matchMedia('(max-width: 720px)').matches) return;
		const pointEl = sceneEl.querySelector(`[data-point="${CSS.escape(code)}"]`);
		if (!pointEl) return;

		const sceneRect = sceneEl.getBoundingClientRect();
		const pointRect = pointEl.getBoundingClientRect();
		const largeur = popupEl.offsetWidth;
		const hauteur = popupEl.offsetHeight;
		const marge = 8;
		const ecart = 12;
		const xPoint = pointRect.left + pointRect.width / 2 - sceneRect.left;
		const yPoint = pointRect.top + pointRect.height / 2 - sceneRect.top;
		const left = Math.min(Math.max(xPoint - largeur / 2, marge), sceneRect.width - largeur - marge);
		const placeHaut = yPoint - ecart;
		const placeBas = sceneRect.height - yPoint - ecart;
		const placement = placeHaut >= hauteur || placeHaut >= placeBas ? 'dessus' : 'dessous';
		const topBrut = placement === 'dessus' ? yPoint - hauteur - ecart : yPoint + ecart;
		// La bulle peut dépasser légèrement du dessin : la contraindre au rectangle
		// de la carte la rabattait sur les points du sud à 320 px. La scène n'est pas
		// rognée, et le contrôle de fenêtre ci-dessous garantit sa visibilité.
		const top = topBrut;

		popup = {
			left,
			top,
			flecheX: Math.min(Math.max(xPoint - left, 14), largeur - 14),
			placement,
			pret: true
		};

		// Le point et la bulle se déplacent ensemble avec la page. On ne défile que
		// lorsque l'ensemble sortirait effectivement de la fenêtre visible.
		requestAnimationFrame(() => {
			const rect = popupEl?.getBoundingClientRect();
			if (!rect) return;
			const hautVisible = 108;
			const basVisible = window.innerHeight - 12;
			if (rect.top < hautVisible) {
				window.scrollBy({ top: rect.top - hautVisible, behavior: 'auto' });
			} else if (rect.bottom > basVisible) {
				window.scrollBy({ top: rect.bottom - basVisible, behavior: 'auto' });
			}
		});
	}

	function programmerPopup(code = choisi) {
		if (!code || !window.matchMedia('(max-width: 720px)').matches) return;
		popup.pret = false;
		requestAnimationFrame(() => requestAnimationFrame(() => positionnerPopup(code)));
	}

	// Choisir un musée remplace le contenu sans refermer un second appui.
	function choisir(code) {
		choisi = code;
		programmerPopup(code);
	}

	// Fermeture : la croix ou Échap. Le focus retourne AU POINT d'où l'on vient —
	// sans quoi le clavier repartirait du haut de la page, et l'on perdrait
	// l'endroit de la carte qu'on était en train de lire.
	function fermerPanneau() {
		const code = choisi;
		choisi = null;
		queueMicrotask(() => document.querySelector(`[data-point="${code}"]`)?.focus());
	}

	function auClavierPage(event) {
		if (choisi && event.key === 'Escape') {
			event.preventDefault();
			fermerPanneau();
		}
	}

	function auClavier(event, code) {
		if (event.key === 'Enter' || event.key === ' ') {
			event.preventDefault();
			choisir(code);
		}
	}

	function auRedimensionnement() {
		if (choisi) programmerPopup(choisi);
	}
</script>

<svelte:window onkeydown={auClavierPage} onresize={auRedimensionnement} />

{#snippet panneauMusee()}
	<div class="panneau-musee" role="group" aria-label="Musée choisi">
		<header class="panneau-entete">
			<div class="entete-texte">
				<p class="panneau-nom">{musee.nom}</p>
				<p class="panneau-ville">{musee.ville}</p>
			</div>
			<button type="button" class="fermer" aria-label="Fermer le panneau" onclick={fermerPanneau}>
				<span aria-hidden="true">×</span>
			</button>
		</header>
		<div class="panneau-corps">
			<p class="panneau-compte">{concernees(musee.doute)}</p>
			{#if musee.oeuvreUnique?.titre}
				<p class="oeuvre-unique">{musee.oeuvreUnique.titre}</p>
			{/if}
			<ul class="panneau-mentions">
				{#each musee.lignes as l (l.label)}
					<li>
						<span class="pastille" style="background: {l.couleur}"></span>
						<span class="mention-label">{l.label}</span>
						<span class="mention-n">{l.valeur}</span>
					</li>
				{/each}
			</ul>
			<div class="panneau-actions">
				{#if onVoirOeuvres}
					<button type="button" class="ligne-action interne" onclick={() => onVoirOeuvres(musee.code)}>
						<span>{voirOeuvres(musee.doute)}</span>
						<span class="fleche" aria-hidden="true">›</span>
					</button>
				{/if}
				{#if musee.oeuvreUnique}
					<a
						class="ligne-action externe"
						href={lienPop(musee.oeuvreUnique.reference)}
						target="_blank"
						rel="noreferrer"
					>
						<span>Consulter la notice sur POP</span>
						<span class="fleche" aria-hidden="true">↗</span>
					</a>
				{/if}
			</div>
		</div>
	</div>
{/snippet}

<figure class="carte">
	<figcaption class="titre">Où sont conservées ces œuvres&nbsp;?</figcaption>

	<div class="agencement">
		<div class="scene" bind:this={sceneEl}>
			<svg viewBox="0 0 {W} {H}" role="img" aria-label="Carte des musées de France conservant des œuvres où le nom de {maitre.nom} est accompagné d’une formulation prudente">
				<!-- Fond régions : illustration discrète, aucune donnée. -->
				{#each regions as d, i (i)}
					<path {d} class="region" />
				{/each}
				<!-- Un point = un musée (tous de même taille, et tous choisissables de
				     la même façon : souris, toucher, Entrée ou Espace). Le survol
				     annonce seulement qu'on peut le choisir ; le clic ouvre le panneau,
				     seul endroit où l'information s'écrit. -->
				{#each points as p (p.code)}
					<circle
						cx={p.x}
						cy={p.y}
						r={R_POINT}
						class="point"
						class:choisi={choisi === p.code}
						data-point={p.code}
						tabindex="0"
						role="button"
						aria-pressed={choisi === p.code}
						aria-label={p.resume}
						onclick={() => choisir(p.code)}
						onkeydown={(e) => auClavier(e, p.code)}
					/>
				{/each}
			</svg>
			{#if musee}
				<div
					class="popup-mobile"
					class:dessus={popup.placement === 'dessus'}
					class:pret={popup.pret}
					bind:this={popupEl}
					style="left: {popup.left}px; top: {popup.top}px; --fleche-x: {popup.flecheX}px"
				>
					{@render panneauMusee()}
				</div>
			{/if}
		</div>

		<div class="flanc" class:avec-selection={musee}>
			<!-- Panneau du musée choisi : le seul endroit où vivent les liens. Il
			     remplace la légende tant qu'un musée est choisi. -->
			{#if musee}
				<div class="panneau-desktop">{@render panneauMusee()}</div>
			{:else}
				<!-- Aucun musée choisi : ce que le point représente, et ce qu'on peut en
				     faire. Plus de mode d'emploi du survol — il n'affiche plus rien. -->
				<div class="legende">
					<svg class="repere" viewBox="0 0 {2 * R_POINT} {2 * R_POINT}" width={2 * R_POINT} height={2 * R_POINT} aria-hidden="true">
						<circle cx={R_POINT} cy={R_POINT} r={R_POINT} class="point" />
					</svg>
					<p class="legende-texte">
						Chaque point représente un musée conservant au moins une œuvre concernée.
					</p>
					<p class="invite">
						Sélectionnez un musée pour consulter les œuvres qui y sont conservées.
					</p>
				</div>
			{/if}
		</div>
	</div>
	{#if projetables.length === 0}
		<p class="repli">
			Aucune de ces œuvres n'est conservée dans un musée de France métropolitaine.
		</p>
	{/if}

	{#if horsCadre.length > 0}
		{@const total = horsCadre.reduce((s, m) => s + m.doute, 0)}
		<p class="hors-cadre">
			Hors de France métropolitaine&nbsp;:
			{#if horsCadre.length === 1}
				{concernees(total)} au {horsCadre[0].nom}, à {horsCadre[0].ville}.
				{#if onVoirOeuvres}
					<button type="button" class="action action-en-ligne" onclick={() => onVoirOeuvres(horsCadre[0].code)}>
						{voirOeuvres(horsCadre[0].doute)}&nbsp;→
					</button>
				{/if}
			{:else}
				{concernees(total)}, dans {nombre(horsCadre.length)} musées hors métropole
				(outre-mer ou étranger).
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

	.popup-mobile {
		display: none;
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

		.panneau-desktop,
		.flanc.avec-selection {
			display: none;
		}

		/* Sur mobile, le détail reste dans la carte et près du point choisi. Il ne
		   devient ni une feuille fixe ni un second écran. */
		.popup-mobile {
			display: block;
			position: absolute;
			z-index: 20;
			width: min(14.5rem, calc(100% - 1rem));
			opacity: 0;
			pointer-events: none;
			transition: opacity 0.1s ease-out;
		}

		.popup-mobile.pret {
			opacity: 1;
			pointer-events: auto;
		}

		.popup-mobile::after {
			content: '';
			position: absolute;
			left: var(--fleche-x);
			top: -6px;
			transform: translateX(-50%);
			border-right: 6px solid transparent;
			border-bottom: 6px solid rgba(255, 253, 249, 0.95);
			border-left: 6px solid transparent;
		}

		.popup-mobile.dessus::after {
			top: auto;
			bottom: -6px;
			border-top: 6px solid rgba(255, 253, 249, 0.95);
			border-bottom: 0;
		}

		.popup-mobile .panneau-musee {
			max-height: min(15rem, calc(100dvh - 8rem));
			overflow-x: hidden;
			overflow-y: auto;
			background: rgba(255, 253, 249, 0.95);
			box-shadow: 0 0.45rem 1.25rem rgba(43, 30, 20, 0.16);
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

	/* Le point grossit sur PLACE : la transformation part de son propre centre
	   (transform-box + origin), sinon un scale l'enverrait vers le coin du SVG.
	   Le rayon lui-même ne change pas — animer `r` est moins régulier d'un
	   navigateur à l'autre que d'animer une transformation. */
	.point {
		fill: var(--carte-point);
		fill-opacity: 0.82;
		stroke: #fff;
		stroke-width: 1.1;
		cursor: pointer;
		transform-box: fill-box;
		transform-origin: center;
		transition:
			transform 0.12s ease-out,
			fill-opacity 0.12s ease-out,
			stroke-width 0.12s ease-out;
	}

	/* Survol et focus clavier : le MÊME retour, franc — le point grossit de moitié,
	   son contour blanc s'épaissit, il passe en pleine opacité. Il n'annonce plus
	   une information (l'infobulle est partie) : il annonce qu'il se choisit. */
	.point:hover,
	.point:focus-visible {
		transform: scale(1.5);
		fill-opacity: 1;
		stroke-width: 2;
	}

	/* Le focus clavier ajoute son anneau : il doit rester repérable sans souris,
	   et sur un point déjà choisi. */
	.point:focus-visible {
		outline: 2px solid var(--couleur-encre);
		outline-offset: 3px;
	}

	.point:focus:not(:focus-visible) {
		outline: none;
	}

	/* Les autres points s'effacent LÉGÈREMENT pendant qu'on en vise un : de quoi
	   détacher le point visé sans faire disparaître la répartition, qui est le
	   sujet de la carte. Le point choisi, lui, ne s'atténue jamais. */
	svg:hover .point:not(:hover):not(.choisi),
	svg:focus-within .point:not(:focus-visible):not(.choisi) {
		fill-opacity: 0.55;
	}

	/* Point CHOISI : le seul état persistant de la carte. Cerné d'encre, il se
	   distingue du survol, qui s'efface dès qu'on s'éloigne. */
	.point.choisi {
		fill-opacity: 1;
		stroke: var(--couleur-encre);
		stroke-width: 2.4;
	}

	.point.choisi:hover,
	.point.choisi:focus-visible {
		stroke-width: 2.8;
	}

	/* Le mouvement est un confort, pas une information. */
	@media (prefers-reduced-motion: reduce) {
		.point {
			transition: none;
		}
	}

	/* --- Panneau du musée choisi : il porte les liens, et lui seul. ------------
	   Deux zones : un en-tête gris qui dit QUI l'on regarde, un corps clair qui
	   dit ce qu'on y trouve. Le panneau ne porte plus de retrait — chaque zone a
	   le sien, sinon le fond de l'en-tête ne pourrait pas courir jusqu'aux bords.
	   `overflow: hidden` fait suivre les angles arrondis à l'aplat gris. */
	.panneau-musee {
		background: var(--surface-carte);
		border: 1px solid var(--couleur-trait);
		border-radius: var(--rayon-s);
		overflow: hidden;
	}

	/* En-tête : le nom, la ville dessous, la croix au coin. Le filet le sépare du
	   corps ; le fond gris reste celui posé le 2026-08-06. */
	.panneau-entete {
		display: flex;
		align-items: flex-start;
		gap: var(--espace-2);
		padding: var(--espace-3);
		background: var(--surface-entete);
		border-bottom: 1px solid var(--couleur-trait);
	}

	.entete-texte {
		flex: 1;
		min-width: 0;
	}

	/* Croix : cible de 44 px — la taille d'un doigt —, symbole petit et discret.
	   Les marges négatives absorbent l'excédent pour que la cible ne pousse pas
	   l'en-tête : elle déborde dans le rembourrage existant au lieu de l'agrandir.
	   Pas de fond au repos, le panneau est petit et un bouton plein y ferait une
	   tache. */
	.fermer {
		flex: none;
		width: 2.75rem;
		height: 2.75rem;
		display: flex;
		align-items: center;
		justify-content: center;
		margin: -0.85rem -0.7rem -0.85rem 0;
		padding: 0;
		background: none;
		border: 0;
		border-radius: 2px;
		font-size: 1.15rem;
		line-height: 1;
		color: var(--couleur-encre-douce);
		cursor: pointer;
	}

	.fermer:hover {
		background: rgba(43, 30, 20, 0.08);
		color: var(--couleur-encre);
	}

	.fermer:focus-visible {
		outline: var(--focus-anneau);
		outline-offset: 1px;
	}

	.panneau-corps {
		display: flex;
		flex-direction: column;
		align-items: flex-start;
		gap: var(--espace-2);
		padding: var(--espace-3);
	}

	/* Nom du musée : un cran au-dessus du corps du panneau, en gras. Certains sont
	   très longs (« Viséum-musée de la lunette (collections du musée de la lunette
	   et du musée Jourdain) », 84 signes) : la coupure est autorisée dans les mots
	   pour qu'aucun ne déborde de la colonne, et l'interligne reste aéré. */
	.panneau-nom {
		margin: 0;
		font-family: var(--police-ui);
		font-size: var(--taille-s);
		font-weight: 600;
		line-height: 1.35;
		color: var(--couleur-encre);
		overflow-wrap: anywhere;
		hyphens: auto;
	}

	.panneau-ville {
		margin: 0.15rem 0 0;
		font-family: var(--police-ui);
		font-size: var(--taille-xs);
		line-height: 1.3;
		color: var(--couleur-encre-douce);
		overflow-wrap: anywhere;
	}

	/* Le nombre d'œuvres est la mesure du panneau : il se lit avant la ventilation
	   qui le détaille. */
	.panneau-compte {
		margin: 0;
		font-family: var(--police-ui);
		font-size: var(--taille-s);
		font-weight: 700;
		color: var(--couleur-encre);
	}

	/* Musée à une seule œuvre : le titre exact publié par le musée. */
	.oeuvre-unique {
		margin: 0;
		font-family: var(--police-texte);
		font-size: var(--taille-s);
		line-height: 1.35;
		color: var(--couleur-encre);
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

	/* Effectifs dans une COLONNE FIXE à droite : ils s'alignent d'une ligne à
	   l'autre, on les compare sans les chercher. */
	.panneau-mentions li {
		display: grid;
		grid-template-columns: 0.5rem 1fr 2.4rem;
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
		text-align: right;
		font-variant-numeric: tabular-nums;
		color: var(--couleur-encre);
	}

	/* Zone d'actions : des LIGNES, pas des blocs. Un filet l'ouvre, chaque ligne
	   prend toute la largeur du panneau et se sépare de la suivante par un trait
	   très clair. Le panneau fait dix lignes : deux aplats pleins y pesaient plus
	   que tout le reste (2026-08-08 bis). */
	.panneau-actions {
		display: flex;
		flex-direction: column;
		margin-top: var(--espace-2);
		border-top: 1px solid var(--couleur-trait);
	}

	.ligne-action {
		display: flex;
		align-items: center;
		justify-content: space-between;
		gap: var(--espace-2);
		width: 100%;
		padding: 0.6rem 0.15rem;
		background: none;
		border: 0;
		border-radius: 2px;
		font-family: var(--police-ui);
		font-size: var(--taille-xs);
		text-align: left;
		text-decoration: none;
		cursor: pointer;
	}

	/* Séparation discrète entre les deux actions — un trait plus clair que celui
	   qui ouvre la zone : elles se distinguent sans se cloisonner. */
	.ligne-action + .ligne-action {
		border-top: 1px solid var(--couleur-trait-clair);
	}

	/* Interne : cobalt, un peu plus grasse. C'est le chemin principal. */
	.ligne-action.interne {
		color: var(--accent-cobalt);
		font-weight: 600;
	}

	/* Externe : plus discrète, mais jamais grisée — elle reste une action. */
	.ligne-action.externe {
		color: var(--couleur-encre-douce);
	}

	.ligne-action:hover {
		background: rgba(53, 87, 138, 0.07);
	}

	.ligne-action.externe:hover {
		color: var(--couleur-encre);
	}

	.ligne-action:focus-visible {
		outline: 2px solid var(--accent-cobalt);
		outline-offset: -2px;
	}

	/* L'icône dit où l'on va : chevron pour rester dans la page, flèche oblique
	   pour sortir du site. Caractères et non fichiers — le projet n'a pas de jeu
	   d'icônes, et on n'en ajoute pas une dépendance pour deux glyphes. */
	.fleche {
		flex: none;
		font-size: 1.05em;
		line-height: 1;
		opacity: 0.75;
	}

	.ligne-action.externe .fleche {
		font-size: 0.9em;
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

	/* Ce qu'on peut faire de la carte, à la place du panneau vide. Même corps que
	   la légende, mais en encre pleine : c'est une invitation, pas une note. */
	.invite {
		flex-basis: 100%;
		margin: var(--espace-2) 0 0;
		font-size: 0.8rem;
		line-height: 1.45;
		color: var(--couleur-encre);
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

	/* La bulle mobile garde le même contenu que le panneau latéral, mais resserré
	   pour rester un détail lié au point et non une fenêtre dans la fenêtre. */
	@media (max-width: 720px) {
		.popup-mobile .panneau-entete {
			position: sticky;
			top: 0;
			z-index: 1;
			padding: 0.45rem 0.55rem;
			background: rgba(242, 239, 233, 0.97);
		}

		.popup-mobile .fermer {
			width: 2.25rem;
			height: 2.25rem;
			margin: -0.55rem -0.45rem -0.55rem 0;
		}

		.popup-mobile .panneau-corps {
			gap: 0.28rem;
			padding: 0.5rem 0.55rem;
		}

		.popup-mobile .panneau-nom,
		.popup-mobile .panneau-compte,
		.popup-mobile .oeuvre-unique {
			font-size: 0.78rem;
		}

		.popup-mobile .oeuvre-unique {
			line-height: 1.25;
		}

		.popup-mobile .panneau-mentions,
		.popup-mobile .ligne-action {
			font-size: 0.72rem;
		}

		.popup-mobile .panneau-actions {
			margin-top: 0.15rem;
		}

		.popup-mobile .ligne-action {
			padding: 0.35rem 0.08rem;
		}
	}
</style>
