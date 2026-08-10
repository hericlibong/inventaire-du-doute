<script>
	import { FAMILLE_PUBLIC, ORDRE_FAMILLES } from '$lib/familles-public.js';

	// Profil des mentions d'un artiste, dans le répertoire : un ruban COURT, à
	// longueur fixe, qui montre la COMPOSITION et rien d'autre.
	//
	// Ce qu'il était jusqu'au 2026-08-08 : une bande occupant toute la largeur de
	// la colonne. Elle disait déjà la composition — 100 % de l'artiste affiché —,
	// mais posée juste sous le nombre et remplissant la ligne, elle se lisait comme
	// une jauge de quantité. Charles Le Brun (310 œuvres) et Michel-Ange (148) y
	// avaient exactement la même longueur, ce qui laissait croire à des effectifs
	// équivalents. La quantité est portée par le NOMBRE et par l'ordre du tri ;
	// ce ruban ne porte que le profil.
	//
	// Trois choix de forme découlent de là (decisions.md, 2026-08-08 ter) :
	//   · une longueur fixe et COURTE — moins d'un tiers de la ligne : un ruban qui
	//     ne remplit rien ne se lit pas comme un remplissage ;
	//   · des segments DÉTACHÉS par un blanc : une barre de progression est
	//     continue, celle-ci ne l'est pas ;
	//   · aucune interaction. La jauge portait une infobulle qui recouvrait la
	//     liste pendant qu'on cherchait un nom, et qui répétait le graphique du
	//     profil. Elle est supprimée : le répertoire est un outil de sélection.
	//
	// Le ruban est donc DÉCORATIF (aria-hidden) : il n'ajoute rien qu'un lecteur
	// d'écran ne trouve déjà dans le nom, le nombre et la fiche de l'artiste — et
	// il ne crée plus d'arrêt de tabulation.
	//
	// familles : [{ code, notices }] ; total : le nombre d'œuvres concernées.
	let { familles, total, largeur = 96, hauteur = 7, ecart = 1.5, plancher = 3 } = $props();

	const rang = (code) => ORDRE_FAMILLES.indexOf(code);

	// Largeurs en pixels, avec un PLANCHER de visibilité.
	//
	// Écart assumé, et déclaré : une mention présente doit se voir. Le « nom (?) »
	// de Charles Le Brun pèse 0,6 % — 0,6 pixel sur ce ruban, c'est-à-dire rien.
	// Les segments sous le plancher sont donc portés à `plancher` px, et ce qui est
	// ajouté est repris sur les segments majoritaires, au prorata. La hiérarchie
	// entre mentions n'en est jamais modifiée : seules les parts déjà infimes sont
	// arrondies vers le haut.
	const segments = $derived.by(() => {
		const parts = [...familles]
			.sort((a, b) => rang(a.code) - rang(b.code))
			.map((f) => ({
				code: f.code,
				couleur: FAMILLE_PUBLIC[f.code].couleur,
				brut: total ? (f.notices / total) * (largeur - ecart * (familles.length - 1)) : 0
			}));

		const manque = parts.reduce((s, p) => s + Math.max(0, plancher - p.brut), 0);
		const majoritaires = parts.reduce((s, p) => s + (p.brut > plancher ? p.brut : 0), 0) || 1;

		return parts.map((p) => ({
			code: p.code,
			couleur: p.couleur,
			large: p.brut < plancher ? plancher : p.brut - manque * (p.brut / majoritaires)
		}));
	});
</script>

<div class="ruban" style="height: {hauteur}px; gap: {ecart}px" aria-hidden="true">
	{#each segments as s (s.code)}
		<span class="segment" style="width: {s.large}px; background: {s.couleur}"></span>
	{/each}
</div>

<style>
	.ruban {
		display: flex;
		width: max-content;
		max-width: 100%;
	}

	.segment {
		display: block;
		height: 100%;
		border-radius: 1px;
	}
</style>
