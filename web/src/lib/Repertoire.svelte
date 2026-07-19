<script>
	// Répertoire — la colonne de gauche d'« Explorer les maîtres » (architecture-
	// editoriale.md §4, charte §5) : un OUTIL DE NAVIGATION, séparé du profil du
	// maître (à droite). Recherche + tri + liste des 27 + microprofils colorés. Ne
	// partage plus sa largeur avec une légende détaillée : la légende des mentions
	// rejoindra « Comprendre les mentions » (retirée d'ici le 2026-07-17).
	import BarreFamilles from '$lib/BarreFamilles.svelte';
	import { nombre } from '$lib/joconde.js';

	// `selection` est liée à la fiche (bind:selection côté page) : le répertoire
	// choisit, la scène du maître affiche.
	let { artistes, selection = $bindable() } = $props();

	// Recherche par nom (filtre local sur les 27 ; moteur sur toute la base = plus
	// tard, roadmap P3-T1).
	let recherche = $state('');

	// Tri : par nombre d'œuvres concernées (défaut, ordre naturel du dossier) ou
	// alphabétique. « Trier par valeur, sauf ordre naturel » (CLAUDE.md) : le doute
	// EST la valeur, on la garde par défaut ; l'alphabétique aide à retrouver un nom.
	let tri = $state('nombre'); // 'nombre' | 'alpha'

	const liste = $derived.by(() => {
		const q = recherche.trim().toLowerCase();
		const filtres = artistes.filter((a) => a.nom.toLowerCase().includes(q));
		return [...filtres].sort((a, b) =>
			tri === 'alpha' ? a.nom.localeCompare(b.nom, 'fr') : b.doute - a.doute
		);
	});

	// Responsive : sur petit écran, le répertoire se replie pour que le profil reste
	// atteignable sans un long défilement (architecture §4 : « colonne fixe ou
	// repliable »). matchMedia plutôt qu'un <details> natif (piège de réouverture
	// selon la largeur, cf. LegendeFamilles 2026-07-13). En SSR/pré-rendu, l'effet
	// ne tourne pas → état par défaut « déployé », correct pour le desktop.
	let estMobile = $state(false);
	let ouvert = $state(true);
	$effect(() => {
		const mq = window.matchMedia('(max-width: 720px)');
		const sync = () => {
			estMobile = mq.matches;
			if (!mq.matches) ouvert = true; // desktop : toujours déployé
		};
		estMobile = mq.matches;
		ouvert = !mq.matches; // replié d'emblée sur mobile (profil d'abord)
		mq.addEventListener('change', sync);
		return () => mq.removeEventListener('change', sync);
	});

	function choisir(nom) {
		selection = nom;
		if (estMobile) ouvert = false; // referme après le choix, découvre le profil
	}
</script>

<nav class="repertoire" aria-label="Répertoire des maîtres">
	{#if estMobile}
		<button class="replier" aria-expanded={ouvert} onclick={() => (ouvert = !ouvert)}>
			<span class="replier-titre">{ouvert ? 'Masquer la liste' : 'Choisir un maître'}</span>
			<span class="replier-compte">{artistes.length} maîtres</span>
		</button>
	{/if}

	{#if ouvert}
		<div class="panneau">
			<div class="controles">
				<label class="recherche">
					<span class="visuellement-cache">Filtrer les maîtres par nom</span>
					<input type="search" placeholder="Filtrer un nom…" bind:value={recherche} />
				</label>
				<div class="tri" role="group" aria-label="Trier la liste">
					<span class="tri-label">Trier&nbsp;:</span>
					<button
						class:actif={tri === 'nombre'}
						aria-pressed={tri === 'nombre'}
						onclick={() => (tri = 'nombre')}
					>
						Notices
					</button>
					<button
						class:actif={tri === 'alpha'}
						aria-pressed={tri === 'alpha'}
						onclick={() => (tri = 'alpha')}
					>
						A→Z
					</button>
				</div>
			</div>

			<!-- Micro-légende : le nombre à droite de chaque nom est le MÊME `doute` que
			     la valeur principale du profil (notices à formulation prudente). -->
			<p class="legende-liste">
				<span>Artiste</span><span>Notices concernées</span>
			</p>

			<ul class="maitres">
				{#each liste as a (a.nom)}
					<!-- La jauge (microprofil coloré) vit HORS du bouton : ses segments sont
					     focusables (infobulle au survol/focus), or un élément interactif ne
					     peut pas être imbriqué dans un <button> (2026-07-12). -->
					<li class="rang" class:actif={a.nom === selection}>
						<button
							class="maitre"
							aria-current={a.nom === selection ? 'true' : undefined}
							onclick={() => choisir(a.nom)}
						>
							<span class="nom">{a.nom}</span>
							<span class="compte">{nombre(a.doute)}</span>
						</button>
						<BarreFamilles familles={a.familles} total={a.doute} nom={a.nom} hauteur="0.35rem" />
					</li>
				{:else}
					<li class="vide">Aucun maître ne correspond.</li>
				{/each}
			</ul>
		</div>
	{/if}
</nav>

<style>
	.repertoire {
		display: block;
	}

	/* Bouton de repli (mobile seulement) : ouvre/masque le panneau de navigation. */
	.replier {
		width: 100%;
		display: flex;
		justify-content: space-between;
		align-items: baseline;
		gap: var(--espace-3);
		padding: 0.6rem 0.75rem;
		background: var(--surface-carte);
		border: var(--filet);
		border-radius: var(--rayon-m);
		font-family: var(--police-ui);
		cursor: pointer;
	}

	.replier-titre {
		font-weight: 600;
		color: var(--couleur-encre);
	}

	.replier-compte {
		font-size: var(--taille-s);
		color: var(--couleur-encre-douce);
		font-variant-numeric: tabular-nums;
	}

	.panneau {
		margin-top: var(--espace-2);
	}

	/* Barre de contrôles : recherche (souple) + tri (compact). */
	.controles {
		display: flex;
		flex-wrap: wrap;
		gap: var(--espace-2) var(--espace-3);
		align-items: center;
	}

	.recherche {
		flex: 1 1 10rem;
	}

	.recherche input {
		width: 100%;
		box-sizing: border-box;
		padding: 0.5rem 0.6rem;
		border: var(--filet);
		border-radius: var(--rayon-s);
		font: inherit;
		font-family: var(--police-ui);
		background: #fff;
	}

	.recherche input:focus-visible {
		outline: var(--focus-anneau);
		outline-offset: 1px;
	}

	/* Tri : petit segment de deux options, registre UI sobre (Public Sans). */
	.tri {
		display: inline-flex;
		align-items: center;
		gap: var(--espace-2);
	}

	.tri-label {
		font-family: var(--police-ui);
		font-size: var(--taille-s);
		color: var(--couleur-encre-douce);
	}

	.tri button {
		font-family: var(--police-ui);
		font-size: var(--taille-s);
		padding: 0.25rem 0.55rem;
		border: var(--filet);
		background: var(--surface-carte);
		color: var(--couleur-encre-douce);
		cursor: pointer;
	}

	.tri button:first-of-type {
		border-radius: var(--rayon-s) 0 0 var(--rayon-s);
	}

	.tri button:last-of-type {
		border-radius: 0 var(--rayon-s) var(--rayon-s) 0;
		border-left: none;
	}

	.tri button.actif {
		background: var(--accent-cobalt);
		border-color: var(--accent-cobalt);
		color: #fff;
	}

	.tri button:focus-visible {
		outline: var(--focus-anneau);
		outline-offset: 1px;
		position: relative; /* passe l'anneau au-dessus du voisin */
	}

	.visuellement-cache {
		position: absolute;
		width: 1px;
		height: 1px;
		overflow: hidden;
		clip: rect(0 0 0 0);
	}

	/* Micro-légende : en-tête discret de la liste, aligné sur nom | compte. */
	.legende-liste {
		display: flex;
		justify-content: space-between;
		gap: var(--espace-3);
		margin: var(--espace-3) 0 0;
		padding: 0 0.5rem var(--espace-1);
		font-family: var(--police-ui);
		font-size: var(--taille-xs);
		letter-spacing: 0.04em;
		text-transform: uppercase;
		color: var(--couleur-encre-douce);
	}

	.maitres {
		list-style: none;
		margin: var(--espace-2) 0 0;
		padding: 0;
		max-height: 34rem;
		overflow-y: auto;
	}

	/* La ligne porte l'état (sélection, survol) ; le bouton ne couvre que nom +
	   compte, la jauge est sa sœur (segments focusables, interdits dans un <button>). */
	.rang {
		border-bottom: var(--filet);
		/* filet d'accent à gauche, transparent au repos : réservé à la sélection,
		   il ne fait donc pas « sauter » la largeur quand un rang devient actif. */
		border-left: 3px solid transparent;
		padding: 0.5rem 0.5rem 0.6rem;
	}

	.rang:hover {
		background: rgba(122, 74, 43, 0.06);
	}

	/* Sélection active clairement identifiable : filet d'accent + fond soutenu +
	   nom en pleine encre (le survol reste plus léger). */
	.rang.actif {
		background: rgba(53, 87, 138, 0.1);
		border-left-color: var(--accent-cobalt);
	}

	.maitre {
		width: 100%;
		text-align: left;
		background: none;
		border: none;
		padding: 0;
		cursor: pointer;
		display: grid;
		grid-template-columns: 1fr auto;
		gap: 0.15rem 0.5rem;
		font: inherit;
	}

	.maitre:focus-visible {
		outline: var(--focus-anneau);
		outline-offset: 2px;
	}

	.rang :global(.barre) {
		margin-top: 0.35rem;
	}

	.maitre .nom {
		font-weight: 600;
		color: var(--couleur-encre);
	}

	.maitre .compte {
		color: var(--couleur-encre-douce);
		font-variant-numeric: tabular-nums;
		font-family: var(--police-ui);
	}

	.vide {
		color: var(--couleur-encre-douce);
		padding: 0.5rem 0;
	}
</style>
