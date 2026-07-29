<script>
	import { FAMILLE_PUBLIC, ORDRE_FAMILLES } from '$lib/familles-public.js';
	import { nombre } from '$lib/joconde.js';
	import Infobulle from '$lib/Infobulle.svelte';

	// Mini-jauge par mention : un résumé DIRECT du graphique — mêmes mentions,
	// mêmes couleurs (var(--forme-*)), même ordre que l'axe, proportions réelles.
	// Remplace la jauge par niveaux le 2026-07-11 (decisions.md). Les mentions
	// absentes ne sont pas affichées ; un segment minuscule reste un simple trait,
	// sans fausser les proportions.
	//
	// Tooltip : un SEUL récapitulatif du maître (décision 2026-07-13), header = nom,
	// puis une ligne par mention (pastille + nombre + %). Toute la barre est une
	// seule cible survolable/focusable — les segments, sous-pixels, sont trop fins à
	// viser un par un. La grammaire des couleurs vit dans la légende fixe.
	// familles : [{ code, notices }] ; total : le doute ; nom : le maître (aria).
	let { familles, total, nom, hauteur = '0.35rem' } = $props();

	const rang = (code) => ORDRE_FAMILLES.indexOf(code);
	// Pourcentage en français, une décimale au plus : « 77,4 % », « 5,2 % ».
	const pourcentFr = (v) => `${v.toLocaleString('fr-FR', { maximumFractionDigits: 1 })} %`;

	const segments = $derived(
		[...familles]
			.sort((a, b) => rang(a.code) - rang(b.code))
			.map((f) => ({
				code: f.code,
				label: FAMILLE_PUBLIC[f.code].header,
				pourcent: total ? (f.notices / total) * 100 : 0,
				couleur: FAMILLE_PUBLIC[f.code].couleur,
				notices: f.notices
			}))
	);

	// Un seul tooltip pour toute la jauge : header = maître, lignes = mentions.
	const tt = $derived({
		header: nom,
		lignes: segments.map((s) => ({
			label: s.label,
			couleur: s.couleur,
			valeur: nombre(s.notices),
			appoint: pourcentFr(s.pourcent)
		}))
	});

	// Repli accessible (aria) : le récapitulatif en une phrase, sans jargon.
	const aria = $derived(
		`Autour de ${nom} : ` +
			segments.map((s) => `${s.label}, ${nombre(s.notices)} (${pourcentFr(s.pourcent)})`).join(' ; ') +
			'.'
	);

	// Infobulle en position FIXE (coordonnées fenêtre) : la liste des maîtres
	// défile (overflow), un panneau positionné en absolu y serait rogné.
	let actif = $state(null);

	function montre(event) {
		const cible = event.currentTarget.getBoundingClientRect();
		actif = { x: cible.left + cible.width / 2, y: cible.top };
	}

	function cache() {
		actif = null;
	}
</script>

<div
	class="barre"
	style="height: {hauteur}"
	role="button"
	tabindex="0"
	aria-label={aria}
	onmouseenter={montre}
	onmouseleave={cache}
	onfocus={montre}
	onblur={cache}
>
	{#each segments as s (s.code)}
		<span class="segment" style="width: {s.pourcent}%; background: {s.couleur}" aria-hidden="true"></span>
	{/each}
</div>

{#if actif}
	<Infobulle {tt} x={actif.x} y={actif.y} fixe={true} />
{/if}

<style>
	.barre {
		display: flex;
		/* filet séparateur : 1 px de fond entre segments, pour détacher les
		   couleurs voisines (rouge/corail, violet/prune) sans fausser les parts */
		gap: 1px;
		width: 100%;
		border-radius: 2px;
		position: relative;
		cursor: default;
	}

	/* Zone de survol/focus ÉLARGIE verticalement (invisible) : la barre fait ~5 px
	   de haut, inatteignable sans cela. */
	.barre::after {
		content: '';
		position: absolute;
		top: -0.45rem;
		bottom: -0.45rem;
		left: 0;
		right: 0;
	}

	.barre:focus-visible {
		outline: 2px solid var(--couleur-encre);
		outline-offset: 2px;
	}

	.segment {
		display: block;
		height: 100%;
	}
</style>
