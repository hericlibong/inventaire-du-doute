<script>
	// Carte par maître (decisions.md 2026-07-12, taille fixe retenue après test A/B).
	// Une seule question : OÙ sont conservées les œuvres concernées — présence et
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
	import { FAMILLE_PUBLIC, oeuvres } from '$lib/familles-public.js';
	import { estProjetable, creerProjection, creerChemin, normaliserFond, ecarterPoints } from '$lib/geo.js';

	let { maitre } = $props();

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

	// Repli : une carte à un seul point ne montre pas une répartition. En dessous de
	// deux musées projetables, on remplace la carte par une phrase.
	const afficheCarte = $derived(projetables.length >= 2);

	// « N œuvre(s) concernée(s) » — accord géré par oeuvres(), puis participe accordé.
	const concernees = (n) => `${oeuvres(n)} concernée${n > 1 ? 's' : ''}`;

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
		if (!fond || !afficheCarte) return [];
		const projection = creerProjection(fond, W, H);
		const bruts = projetables.map((m) => {
			const [x, y] = projection([m.lon, m.lat]);
			const lignes = ventilation(m);
			const detail = lignes.map((l) => `${l.label} ${l.valeur}`).join(', ');
			// Musée à une seule œuvre : le point devient un lien vers la fiche
			// publique POP. Le titre (s'il existe) sert d'aperçu dans le tooltip et
			// d'intitulé de lien. Les musées multi-œuvres restent non cliquables.
			const ou = m.doute === 1 ? m.oeuvre_unique : null;
			const titre = ou?.titre || null;
			const href = ou ? lienPop(ou.reference) : null;
			return {
				code: m.code,
				x,
				y,
				href,
				lienAria: href
					? `${m.nom}, ${m.ville} : ${concernees(m.doute)}, ${detail}. ` +
						`Voir la fiche publique${titre ? ` de « ${titre} »` : ' de cette œuvre'}.`
					: null,
				tt: {
					header: `${m.nom}, ${m.ville}`,
					valeur: concernees(m.doute),
					titre,
					lignes
				},
				resume: `${m.nom}, ${m.ville} : ${concernees(m.doute)}. ${detail}.`
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
</script>

<figure class="carte">
	<figcaption class="titre">Où sont conservées ces œuvres</figcaption>

	{#if afficheCarte}
	<div class="agencement">
		<div class="scene" bind:this={regardEl}>
			<svg viewBox="0 0 {W} {H}" role="img" aria-label="Carte des musées de France conservant des œuvres dont l’attribution à {maitre.nom} est incertaine">
				<!-- Fond régions : illustration discrète, aucune donnée. -->
				{#each regions as d, i (i)}
					<path {d} class="region" />
				{/each}
				<!-- Un point = un musée (tous de même taille). Musée à une seule œuvre :
				     le point est un LIEN vers la fiche publique POP (le survol/focus
				     montre l'aperçu). Musée multi-œuvres : point non cliquable, tooltip
				     seul (comportement inchangé). -->
				{#each points as p (p.code)}
					{#if p.href}
						<a
							class="lien-point"
							href={p.href}
							target="_blank"
							rel="noreferrer"
							aria-label={p.lienAria}
							onmouseenter={(e) => montre(e, p)}
							onmouseleave={cache}
							onfocus={(e) => montre(e, p)}
							onblur={cache}
						>
							<circle cx={p.x} cy={p.y} r={R_POINT} class="point" aria-hidden="true" />
						</a>
					{:else}
						<circle
							cx={p.x}
							cy={p.y}
							r={R_POINT}
							class="point"
							tabindex="0"
							role="button"
							aria-label={p.resume}
							onmouseenter={(e) => montre(e, p)}
							onmouseleave={cache}
							onfocus={(e) => montre(e, p)}
							onblur={cache}
						/>
					{/if}
				{/each}
			</svg>

			{#if actif}
				<Infobulle tt={actif.tt} x={actif.x} y={actif.y} dessous={actif.dessous} />
			{/if}
		</div>

		<div class="flanc">
			<!-- Légende : un seul repère de point (présence). Le nombre d'œuvres par
			     musée se lit au survol, pas dans la taille. -->
			<div class="legende">
				<svg class="repere" viewBox="0 0 {2 * R_POINT} {2 * R_POINT}" width={2 * R_POINT} height={2 * R_POINT} aria-hidden="true">
					<circle cx={R_POINT} cy={R_POINT} r={R_POINT} class="point" />
				</svg>
				<p class="legende-texte">
					Un point = un musée où au moins une œuvre concernée est conservée.
					Passez sur un point pour voir combien, et sous quelles formules.
				</p>
			</div>
		</div>
	</div>
	{:else if projetables.length === 1}
		<p class="repli">
			Ces œuvres sont conservées dans un seul lieu&nbsp;: {projetables[0].nom}, à
			{projetables[0].ville}.
		</p>
	{:else}
		<p class="repli">
			Ces œuvres ne sont pas conservées en France métropolitaine.
		</p>
	{/if}

	{#if horsCadre.length > 0}
		{@const total = horsCadre.reduce((s, m) => s + m.doute, 0)}
		<p class="hors-cadre">
			Hors cadre métropolitain&nbsp;:
			{#if horsCadre.length === 1}
				{oeuvres(total)} conservée{total > 1 ? 's' : ''} au {horsCadre[0].nom},
				à {horsCadre[0].ville}.
			{:else}
				{oeuvres(total)} conservées dans {nombre(horsCadre.length)} musées hors
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

	/* Survol/focus FRANC (même retour pour un point cliquable ou non) : pleine
	   opacité + halo blanc plus large → le point survolé « se lève » du fond. */
	.point:focus,
	.point:hover,
	.lien-point:hover .point,
	.lien-point:focus-visible .point {
		fill-opacity: 1;
		stroke-width: 1.8;
		outline: none;
	}

	/* Point cliquable (musée à une seule œuvre) : curseur main ; pas de distinction
	   visuelle AU REPOS (décision : le curseur suffit, deux classes visuelles
	   embrouilleraient la lecture). */
	.lien-point {
		cursor: pointer;
	}

	.lien-point:focus-visible {
		outline: 2px solid var(--couleur-encre);
		outline-offset: 2px;
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
