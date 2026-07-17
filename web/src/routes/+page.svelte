<script>
	// Accueil — couverture éditoriale, Direction B « la ligne de proximité »
	// (charte-graphique.md). Le sujet devient la structure : une ligne horizontale,
	// de la main du maître (chaud) à sa seule influence (froid), ouvre la page ; les
	// huit pigments en sont les stations. Composition ample, le grand chiffre en
	// preuve SECONDAIRE. La figure « Joconde » reste une figure de DONNÉES (archive /
	// index / open data), provisoire et remplaçable — jamais Léonard ni le tableau.
	import Spectre from '$lib/Spectre.svelte';
	import { nombre } from '$lib/joconde.js';
	import { FAMILLE_PUBLIC, ORDRE_FAMILLES } from '$lib/familles-public.js';

	let { data } = $props();
	const n = data.niveaux;
	const prov = data.provenance;
	const pct = (v) => (v * 100).toLocaleString('fr-FR', { maximumFractionDigits: 1 });

	// Les huit pigments dans l'ordre de proximité (stations de la ligne).
	const pigments = ORDRE_FAMILLES.map((code) => FAMILLE_PUBLIC[code].couleur);
	// Rangées de « notices » schématiques (largeurs variées) pour évoquer l'index.
	const rangees = [210, 150, 240, 120, 190, 165];
</script>

<section class="couverture">
	<Spectre hauteur="6px" zones />

	<div class="hero">
		<div class="texte">
			<p class="kicker">Base Joconde · Collections des musées de France</p>
			<h1>L'inventaire du doute</h1>
			<p class="promesse">
				«&nbsp;attribué à&nbsp;», «&nbsp;atelier de&nbsp;», «&nbsp;école de&nbsp;»,
				«&nbsp;à la manière de&nbsp;»&nbsp;: les mots des musées changent à mesure que
				l'œuvre s'éloigne de la main du maître. Ce projet lit ces formules dans les
				collections des musées de France et suit cette ligne.
			</p>
			<div class="actions">
				<a class="cta" href="/les-presque">Explorer les 27 maîtres&nbsp;→</a>
				<a class="lien" href="/echelle">Comprendre les mentions</a>
			</div>
		</div>

		<figure class="figure" aria-label="Figure de données évoquant la base Joconde (composition provisoire)">
			<p class="fig-cap">Figure de données — base Joconde (provisoire)</p>
			<svg viewBox="0 0 300 220" role="presentation">
				<g class="rangees">
					{#each rangees as w, i (i)}
						<rect x="0" y={18 + i * 22} width={w} height="5" rx="1.5" />
					{/each}
				</g>
				<line class="axe" x1="0" x2="300" y1="150" y2="150" />
				{#each pigments as couleur, i (i)}
					<circle cx={12 + i * 40.5} cy="150" r="6.5" style="fill: {couleur}" />
				{/each}
				<text class="bout" x="0" y="182">De la main…</text>
				<text class="bout" x="300" y="182" text-anchor="end">…à l'influence</text>
			</svg>
		</figure>
	</div>

	<div class="preuve">
		<p class="chiffre">{nombre(n.doute_total)}</p>
		<p class="chiffre-note">
			formulations prudentes repérées dans la base — soit {pct(n.taux_doute_avec_auteur)}&nbsp;%
			des notices où un auteur est renseigné.
			<a href="/methode">Comment ces chiffres sont établis&nbsp;→</a>
		</p>
		<p class="source">
			Source&nbsp;: {prov.source}, version du {prov.version_donnee}, {prov.licence}.
		</p>
	</div>
</section>

<style>
	/* Le spectre et le hero prennent toute la largeur du canevas (fin de la colonne
	   étroite). On remonte le spectre sous la coquille en annulant le padding haut. */
	.couverture {
		margin-top: calc(var(--espace-6) * -1 + var(--espace-2));
	}

	.hero {
		display: grid;
		grid-template-columns: 1.15fr 0.85fr;
		gap: var(--espace-6);
		align-items: center;
		margin: var(--espace-6) 0;
	}

	.kicker {
		font-family: var(--police-ui);
		font-size: var(--taille-xs);
		text-transform: uppercase;
		letter-spacing: 0.18em;
		color: var(--couleur-encre-douce);
		margin: 0 0 var(--espace-3);
	}

	h1 {
		font-family: var(--police-titre);
		font-size: var(--taille-xxl);
		line-height: 0.98;
		letter-spacing: -0.015em;
		margin: 0 0 var(--espace-4);
	}

	.promesse {
		font-size: var(--taille-m);
		line-height: 1.6;
		max-width: 34ch;
		margin: 0 0 var(--espace-5);
	}

	.actions {
		display: flex;
		flex-wrap: wrap;
		align-items: center;
		gap: var(--espace-3) var(--espace-5);
	}

	/* Direction B : l'appel principal en encre sobre (pas un bouton de landing). */
	.cta {
		display: inline-block;
		font-family: var(--police-ui);
		font-weight: 600;
		font-size: var(--taille-base);
		background: var(--couleur-encre);
		color: var(--couleur-fond);
		padding: 0.7rem 1.2rem;
		border-radius: 2px;
		text-decoration: none;
	}

	.cta:hover {
		background: #000;
	}

	.cta:focus-visible,
	.lien:focus-visible {
		outline: var(--focus-anneau);
		outline-offset: 3px;
	}

	.lien {
		font-family: var(--police-ui);
		font-size: var(--taille-s);
		color: var(--couleur-encre);
		text-decoration: none;
		border-bottom: 2px solid var(--forme-atelier);
		padding-bottom: 2px;
	}

	.lien:hover {
		color: var(--forme-atelier);
	}

	/* Figure de données : posée dans la marge droite, séparée par un filet, pas
	   encadrée dans une boîte (Direction B). */
	.figure {
		margin: 0;
		border-left: var(--filet);
		padding-left: var(--espace-5);
	}

	.fig-cap {
		font-family: var(--police-ui);
		font-size: var(--taille-xs);
		letter-spacing: 0.12em;
		text-transform: uppercase;
		color: var(--couleur-encre-douce);
		margin: 0 0 var(--espace-3);
	}

	.figure svg {
		display: block;
		width: 100%;
		height: auto;
	}

	.rangees rect {
		fill: var(--couleur-trait);
	}

	.axe {
		stroke: var(--couleur-trait);
		stroke-width: 1;
	}

	.bout {
		font-family: var(--police-ui);
		font-size: 9px;
		letter-spacing: 0.14em;
		text-transform: uppercase;
		fill: var(--couleur-encre-douce);
	}

	/* Preuve chiffrée, secondaire : une bande en pied de couverture. */
	.preuve {
		border-top: var(--filet);
		padding-top: var(--espace-5);
		max-width: 46rem;
	}

	.chiffre {
		font-family: var(--police-titre);
		font-size: var(--taille-xl);
		font-weight: 700;
		color: var(--forme-attribue);
		font-variant-numeric: tabular-nums;
		margin: 0;
		line-height: 1;
	}

	.chiffre-note {
		font-size: var(--taille-base);
		margin: var(--espace-2) 0 0;
		line-height: 1.55;
	}

	.chiffre-note a {
		color: var(--forme-attribue);
		white-space: nowrap;
	}

	.source {
		font-family: var(--police-ui);
		font-size: var(--taille-xs);
		color: var(--couleur-encre-douce);
		margin: var(--espace-3) 0 0;
	}

	@media (max-width: 720px) {
		.hero {
			grid-template-columns: 1fr;
			gap: var(--espace-5);
		}
		h1 {
			font-size: var(--taille-xl);
		}
		.figure {
			border-left: none;
			padding-left: 0;
			border-top: var(--filet);
			padding-top: var(--espace-4);
		}
	}
</style>
