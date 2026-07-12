<script>
	import { FAMILLE_PUBLIC, ORDRE_FAMILLES, oeuvres } from '$lib/familles-public.js';
	import Infobulle from '$lib/Infobulle.svelte';

	// Mini-jauge par famille : un résumé DIRECT du graphique — mêmes familles,
	// mêmes couleurs (var(--forme-*)), même ordre que l'axe, proportions réelles.
	// Remplace la jauge par niveaux le 2026-07-11 (decisions.md) : agrégée par
	// niveau, elle contredisait le graphique (l'« école » bleue de Le Brun y
	// apparaissait ocre). Les familles absentes ne sont pas affichées ; un
	// segment minuscule reste un simple trait, sans fausser les proportions.
	//
	// Chaque segment est survolable ET focusable (2026-07-12) : la couleur n'est
	// pas le seul canal, la jauge s'explique au survol — infobulle partagée
	// (header public + « N œuvres · X % du doute »), aria-label complet en repli.
	// familles : [{ code, notices }] ; total : le doute ; nom : le maître (aria).
	let { familles, total, nom, hauteur = '0.35rem' } = $props();

	const rang = (code) => ORDRE_FAMILLES.indexOf(code);
	// Pourcentage en français, une décimale au plus : « 77,4 % », « 5,2 % ».
	const pourcentFr = (v) => `${v.toLocaleString('fr-FR', { maximumFractionDigits: 1 })} %`;

	const segments = $derived(
		[...familles]
			.sort((a, b) => rang(a.code) - rang(b.code))
			.map((f) => {
				const part = total ? (f.notices / total) * 100 : 0;
				const header = FAMILLE_PUBLIC[f.code].header;
				return {
					code: f.code,
					pourcent: part,
					couleur: FAMILLE_PUBLIC[f.code].couleur,
					tt: { header, valeur: `${oeuvres(f.notices)} · ${pourcentFr(part)} du doute` },
					aria: `${header} : ${oeuvres(f.notices)}, ${pourcentFr(part)} du doute autour de ${nom}.`
				};
			})
	);

	// Infobulle en position FIXE (coordonnées fenêtre) : la liste des maîtres
	// défile (overflow), un panneau positionné en absolu y serait rogné.
	let actif = $state(null);

	function montre(event, s) {
		const cible = event.currentTarget.getBoundingClientRect();
		actif = { tt: s.tt, x: cible.left + cible.width / 2, y: cible.top };
	}

	function cache() {
		actif = null;
	}
</script>

<div class="barre" style="height: {hauteur}" role="group" aria-label="Répartition du doute autour de {nom}, comme sur le graphique">
	{#each segments as s (s.code)}
		<span
			class="segment"
			style="width: {s.pourcent}%; background: {s.couleur}"
			tabindex="0"
			role="button"
			aria-label={s.aria}
			onmouseenter={(e) => montre(e, s)}
			onmouseleave={cache}
			onfocus={(e) => montre(e, s)}
			onblur={cache}
		></span>
	{/each}
</div>

{#if actif}
	<Infobulle tt={actif.tt} x={actif.x} y={actif.y} fixe={true} />
{/if}

<style>
	.barre {
		display: flex;
		/* filet séparateur : 1 px de fond entre segments, pour détacher les
		   couleurs voisines (rouge/corail, violet/prune) sans fausser les parts */
		gap: 1px;
		width: 100%;
		border-radius: 2px;
	}

	.segment {
		display: block;
		height: 100%;
		position: relative;
	}

	/* Zone de survol/focus ÉLARGIE verticalement (invisible) : un segment de
	   0,6 % fait ~2 px de large sur ~5 px de haut — inatteignable sans cela.
	   Pas d'élargissement horizontal (il volerait le survol des voisins). */
	.segment::after {
		content: '';
		position: absolute;
		top: -0.45rem;
		bottom: -0.45rem;
		left: 0;
		right: 0;
	}

	.segment:focus-visible {
		outline: 2px solid var(--couleur-encre);
		outline-offset: 2px;
	}
</style>
