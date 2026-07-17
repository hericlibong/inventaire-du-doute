<script>
	// Accueil — couverture éditoriale de « L'inventaire du doute » (architecture §3).
	// Rompt avec la colonne documentaire : composition à deux zones (promesse à
	// gauche, figure de données à droite), le grand chiffre en preuve SECONDAIRE.
	// La figure « Joconde » est une figure de DONNÉES (archive / index / open data),
	// jamais Léonard ni le tableau : ici, une STRUCTURE média assumée et remplaçable
	// (motif schématique + les pigments des mentions), pas un visuel définitif — la
	// direction artistique viendra ensuite (architecture §6).
	import { nombre } from '$lib/joconde.js';
	import { FAMILLE_PUBLIC, ORDRE_FAMILLES } from '$lib/familles-public.js';

	let { data } = $props();
	const n = data.niveaux;
	const prov = data.provenance;
	const pct = (v) => (v * 100).toLocaleString('fr-FR', { maximumFractionDigits: 1 });

	// Couleurs des 8 mentions, dans l'ordre de proximité — pour le motif de la figure
	// (réutilise la source unique, aucune couleur nouvelle).
	const pigments = ORDRE_FAMILLES.map((code) => FAMILLE_PUBLIC[code].couleur);
	// Rangées de « notices » schématiques (largeurs variées) pour évoquer l'index.
	const rangees = [82, 64, 91, 48, 74, 58, 86, 40, 70];
</script>

<section class="couverture">
	<div class="texte">
		<p class="kicker">Base Joconde · Collections des musées de France</p>
		<h1>L'inventaire du doute</h1>
		<p class="promesse">
			Quand un musée n'est pas sûr de l'auteur d'une œuvre, il l'écrit — avec des mots
			choisis&nbsp;: «&nbsp;attribué à&nbsp;», «&nbsp;atelier de&nbsp;»,
			«&nbsp;école de&nbsp;», «&nbsp;à la manière de&nbsp;»… Ce projet lit ces formules
			dans les collections des musées de France&nbsp;; il montre lesquelles reviennent,
			autour de quels noms, et jusqu'où va la prudence.
		</p>
		<div class="actions">
			<a class="cta" href="/les-presque">Explorer les 27 maîtres&nbsp;→</a>
			<a class="lien" href="/echelle">Comprendre les mentions</a>
		</div>
	</div>

	<figure class="figure" aria-label="Figure de données évoquant la base Joconde (composition provisoire)">
		<svg class="motif" viewBox="0 0 200 150" role="presentation">
			<!-- Rangées de « notices » : un index d'archive, schématique. -->
			{#each rangees as w, i (i)}
				<rect class="notice" x="18" y={14 + i * 12} width={w} height="4" rx="1.5" />
			{/each}
			<!-- Ligne de proximité + les 8 pigments des mentions (gauche → droite). -->
			<line class="axe" x1="120" x2="188" y1="78" y2="78" />
			{#each pigments as couleur, i (i)}
				<circle cx={124 + i * 9} cy="78" r={3.4} style="fill: {couleur}" />
			{/each}
		</svg>
		<figcaption>Figure de données — base Joconde. Composition provisoire.</figcaption>
	</figure>
</section>

<!-- Preuve chiffrée, secondaire (le sujet, ce sont les mots ; le nombre en est la
     preuve). Le cas mono-musée est trop technique pour l'accueil → renvoyé en Méthode. -->
<section class="preuve">
	<p class="chiffre">{nombre(n.doute_total)}</p>
	<p class="chiffre-note">
		formulations prudentes repérées dans la base — soit {pct(n.taux_doute_avec_auteur)}&nbsp;%
		des notices où un auteur est renseigné.
		<a href="/methode">Comment ces chiffres sont établis&nbsp;→</a>
	</p>
	<p class="source">
		Source&nbsp;: {prov.source}, version du {prov.version_donnee}, {prov.licence}.
	</p>
</section>

<style>
	/* --- Couverture : deux zones, promesse à gauche, figure à droite. --- */
	.couverture {
		display: grid;
		grid-template-columns: 1.05fr 0.95fr;
		gap: var(--espace-6);
		align-items: center;
		margin-bottom: var(--espace-6);
	}

	.kicker {
		font-family: var(--police-ui);
		font-size: var(--taille-xs);
		text-transform: uppercase;
		letter-spacing: 0.08em;
		color: var(--couleur-encre-douce);
		margin: 0 0 var(--espace-2);
	}

	h1 {
		font-family: var(--police-titre);
		font-size: var(--taille-xxl);
		line-height: 1.05;
		margin: 0 0 var(--espace-3);
	}

	.promesse {
		font-size: var(--taille-m);
		line-height: 1.6;
		max-width: 32rem;
		margin: 0 0 var(--espace-5);
	}

	.actions {
		display: flex;
		flex-wrap: wrap;
		align-items: center;
		gap: var(--espace-3) var(--espace-5);
	}

	.cta {
		display: inline-block;
		font-family: var(--police-ui);
		font-weight: 600;
		font-size: var(--taille-base);
		background: var(--couleur-accent);
		color: #fff;
		padding: 0.6rem 1.1rem;
		border-radius: var(--rayon-m);
		text-decoration: none;
	}

	.cta:hover {
		background: #6a3f24;
	}

	.cta:focus-visible,
	.lien:focus-visible {
		outline: var(--focus-anneau);
		outline-offset: 2px;
	}

	.lien {
		font-family: var(--police-ui);
		font-size: var(--taille-s);
		color: var(--couleur-encre);
		text-decoration: none;
		border-bottom: 1px solid var(--couleur-accent);
		padding-bottom: 1px;
	}

	.lien:hover {
		color: var(--couleur-accent);
	}

	/* --- Figure de données : zone média assumée, motif schématique + pigments. --- */
	.figure {
		margin: 0;
		background: var(--surface-carte);
		border: var(--filet);
		border-radius: var(--rayon-m);
		padding: var(--espace-4);
		box-shadow: var(--ombre-douce);
	}

	.motif {
		display: block;
		width: 100%;
		height: auto;
	}

	.notice {
		fill: var(--couleur-trait);
	}

	.axe {
		stroke: var(--couleur-encre-douce);
		stroke-width: 0.8;
	}

	.figure figcaption {
		margin-top: var(--espace-3);
		font-family: var(--police-texte);
		font-style: italic;
		font-size: var(--taille-xs);
		color: var(--couleur-encre-douce);
		text-align: center;
	}

	/* --- Preuve chiffrée, secondaire. --- */
	.preuve {
		border-top: var(--filet);
		padding-top: var(--espace-5);
		max-width: 44rem;
	}

	.chiffre {
		font-family: var(--police-titre);
		font-size: var(--taille-xl);
		font-weight: 700;
		color: var(--couleur-accent);
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
		color: var(--couleur-accent);
		white-space: nowrap;
	}

	.source {
		font-family: var(--police-ui);
		font-size: var(--taille-xs);
		color: var(--couleur-encre-douce);
		margin: var(--espace-3) 0 0;
	}

	/* --- Responsive : la figure passe sous le texte. --- */
	@media (max-width: 720px) {
		.couverture {
			grid-template-columns: 1fr;
			gap: var(--espace-5);
		}
		h1 {
			font-size: var(--taille-xl);
		}
	}
</style>
