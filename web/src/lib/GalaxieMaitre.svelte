<script>
	import { NIVEAUX, nombre } from '$lib/joconde.js';

	// Galaxie d'un maître : lui au centre, chaque famille de doute en orbite.
	// Plus une œuvre est « presque lui », plus elle est proche ; plus le doute
	// est fort, plus elle est loin. Les copies « d'après » forment un anneau
	// extérieur, à part (ce ne sont pas des doutes).
	let { maitre } = $props();

	const CENTRE = 220;
	const RAYONS = { 1: 66, 2: 106, 3: 146 }; // orbite par niveau
	const RAYON_COPIE = 184;

	// Position sur un cercle (angle en degrés, 0 = haut, sens horaire).
	function polaire(rayon, angleDeg) {
		const a = ((angleDeg - 90) * Math.PI) / 180;
		return { x: CENTRE + rayon * Math.cos(a), y: CENTRE + rayon * Math.sin(a) };
	}

	// Taille d'une bulle selon le nombre de notices (racine pour ne pas écraser).
	const rayonBulle = (notices) => Math.min(22, 5 + Math.sqrt(notices) * 0.9);

	// Une bulle par famille, répartie tout autour du cercle.
	const noeuds = $derived.by(() => {
		const fams = maitre.familles;
		return fams.map((f, i) => {
			const angle = (i / fams.length) * 360 + 18;
			const r = rayonBulle(f.notices);
			const pos = polaire(RAYONS[f.niveau], angle);
			const lab = polaire(RAYONS[f.niveau] + r + 10, angle);
			return {
				...f,
				x: pos.x,
				y: pos.y,
				r,
				lx: lab.x,
				ly: lab.y,
				ancre: lab.x < CENTRE - 5 ? 'end' : lab.x > CENTRE + 5 ? 'start' : 'middle',
				couleur: `var(--niveau-${f.niveau})`
			};
		});
	});
</script>

<figure class="galaxie">
	<figcaption>
		Autour de <strong>{maitre.nom}</strong> : les {nombre(maitre.doute)} œuvres
		que les musées ne lui attribuent <em>pas avec certitude</em>. Plus un point
		est <strong>proche du centre</strong>, plus l'attribution est probable ;
		plus il est <strong>loin</strong>, plus le doute est fort.
	</figcaption>

	<svg viewBox="0 0 440 440" role="img" aria-label="Galaxie du doute autour de {maitre.nom}">
		<!-- orbites (une par niveau) -->
		{#each NIVEAUX as niv (niv.n)}
			<circle
				cx={CENTRE}
				cy={CENTRE}
				r={RAYONS[niv.n]}
				fill="none"
				stroke="var({niv.variable})"
				stroke-dasharray="3 4"
				stroke-opacity="0.6"
			/>
			<text
				x={CENTRE}
				y={CENTRE - RAYONS[niv.n] - 4}
				text-anchor="middle"
				class="orbite-label"
				fill="var({niv.variable})">{niv.libelle}</text
			>
		{/each}

		<!-- anneau des copies « d'après », à part -->
		<circle
			cx={CENTRE}
			cy={CENTRE}
			r={RAYON_COPIE}
			fill="none"
			stroke="var(--couleur-copie)"
			stroke-dasharray="1 6"
			stroke-opacity="0.7"
		/>
		<text
			x={CENTRE}
			y={CENTRE - RAYON_COPIE - 4}
			text-anchor="middle"
			class="orbite-label"
			fill="var(--couleur-copie)">copies « d'après » — à part</text
		>

		<!-- bulles des familles -->
		{#each noeuds as n (n.code)}
			<circle cx={n.x} cy={n.y} r={n.r} fill={n.couleur} fill-opacity="0.85">
				<title>{n.libelle} : {nombre(n.notices)} notices</title>
			</circle>
			<text x={n.lx} y={n.ly} text-anchor={n.ancre} class="bulle-label" dominant-baseline="middle">
				{n.libelle} · {nombre(n.notices)}
			</text>
		{/each}

		<!-- centre : le maître -->
		<circle cx={CENTRE} cy={CENTRE} r="40" class="coeur" />
		<text x={CENTRE} y={CENTRE - 4} text-anchor="middle" class="coeur-nom">{maitre.nom}</text>
		<text x={CENTRE} y={CENTRE + 12} text-anchor="middle" class="coeur-sous"
			>{nombre(maitre.doute)} en doute</text
		>
	</svg>

	<p class="lecture">
		Chiffres réels (base Joconde). La position sur l'orbite est indicative : elle
		traduit le <em>niveau</em> de doute, pas une mesure d'authenticité.
	</p>
</figure>

<style>
	.galaxie {
		margin: 0;
	}

	figcaption {
		font-size: 1rem;
		max-width: 42rem;
		margin-bottom: 0.75rem;
		color: var(--couleur-encre);
	}

	svg {
		width: 100%;
		max-width: 30rem;
		height: auto;
		display: block;
		margin: 0 auto;
	}

	.orbite-label {
		font-size: 9px;
		font-weight: 600;
		letter-spacing: 0.02em;
	}

	.bulle-label {
		font-size: 9px;
		fill: var(--couleur-encre-douce);
	}

	.coeur {
		fill: #fff;
		stroke: var(--couleur-encre);
		stroke-width: 1.5;
	}

	.coeur-nom {
		font-family: var(--police-titre);
		font-size: 11px;
		font-weight: bold;
		fill: var(--couleur-encre);
	}

	.coeur-sous {
		font-size: 9px;
		fill: var(--couleur-encre-douce);
	}

	.lecture {
		font-size: 0.8rem;
		color: var(--couleur-encre-douce);
		max-width: 42rem;
		margin: 0.75rem auto 0;
		text-align: center;
	}
</style>
