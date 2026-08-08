<script>
	// Agrandissement d'une reproduction déjà retenue par le pipeline (2026-08-08).
	//
	// PÉRIMÈTRE STRICT : cette vue n'ouvre QUE des images déjà validées et déjà
	// servies localement (data/exports/web/oeuvres_img → static/oeuvres). Aucune
	// nouvelle source, aucun appel à un serveur distant, aucun statut de droits
	// touché. La lightbox agrandit ce qui est déjà affiché en vignette, rien d'autre.
	//
	// Le crédit vient du composant partagé CreditImage : l'attribution, la licence
	// et le lien de source sont ceux de la liste, jamais une seconde formulation.
	import { base } from '$app/paths';
	import CreditImage from '$lib/CreditImage.svelte';

	// oeuvre : { titre, image } — fermer() est appelé par Échap, le bouton ou le fond.
	let { oeuvre, fermer } = $props();

	let panneau = $state(null);
	let boutonFermer = $state(null);

	const autre = $derived(oeuvre.image.exemplaire_autre === true);

	// Le focus entre dans la lightbox à l'ouverture (sur le bouton de fermeture,
	// première action utile) et n'en sort pas tant qu'elle est ouverte. Le retour à
	// la vignette est fait par l'appelant, qui seul sait d'où l'on vient.
	$effect(() => {
		boutonFermer?.focus();
		const avant = document.body.style.overflow;
		document.body.style.overflow = 'hidden'; // la page ne défile plus derrière
		return () => {
			document.body.style.overflow = avant;
		};
	});

	function auClavier(e) {
		if (e.key === 'Escape') {
			e.preventDefault();
			fermer();
			return;
		}
		if (e.key !== 'Tab') return;
		// Piège à focus : la tabulation tourne dans le panneau.
		const cibles = panneau?.querySelectorAll('a[href], button');
		if (!cibles?.length) return;
		const premier = cibles[0];
		const dernier = cibles[cibles.length - 1];
		if (e.shiftKey && document.activeElement === premier) {
			e.preventDefault();
			dernier.focus();
		} else if (!e.shiftKey && document.activeElement === dernier) {
			e.preventDefault();
			premier.focus();
		}
	}
</script>

<svelte:window onkeydown={auClavier} />

<!-- Le fond ferme au clic. Il porte un rôle de présentation : le dialogue, lui,
     est le panneau. -->
<div
	class="fond"
	role="dialog"
	aria-modal="true"
	aria-label="Reproduction agrandie : {oeuvre.titre ?? 'œuvre'}"
	onclick={fermer}
	onkeydown={() => {}}
	tabindex="-1"
>
	<!-- Le panneau arrête le clic : cliquer SUR l'image ne referme pas. -->
	<div
		class="panneau"
		bind:this={panneau}
		onclick={(e) => e.stopPropagation()}
		onkeydown={() => {}}
		role="presentation"
	>
		<button class="fermer" bind:this={boutonFermer} onclick={fermer} type="button">
			Fermer
		</button>

		<img
			src="{base}/{oeuvre.image.url}"
			alt={autre
				? `Autre exemplaire du même tirage : ${oeuvre.titre ?? 'œuvre'}`
				: `Reproduction : ${oeuvre.titre ?? 'œuvre'}`}
		/>

		<figcaption class="legende">
			<span class="titre">{oeuvre.titre ?? 'Sans titre'}</span>
			<CreditImage image={oeuvre.image} taille="agrandie" />
		</figcaption>
	</div>
</div>

<style>
	.fond {
		position: fixed;
		inset: 0;
		z-index: 60; /* au-dessus du bandeau fixé (20) */
		display: flex;
		align-items: center;
		justify-content: center;
		padding: clamp(0.75rem, 3vw, 2.5rem);
		/* Assez dense pour que le bandeau de navigation, qui reste dans la page
		   dessous, ne transparaisse pas derrière le bouton de fermeture. */
		background: rgba(12, 18, 25, 0.97);
	}

	/* L'image occupe le plus de place possible sans jamais déborder : la hauteur
	   disponible est celle de l'écran moins la légende et les marges. `contain`
	   garde le ratio, et une image plus petite que l'espace n'est PAS agrandie —
	   on ne fabrique pas de la résolution qui n'existe pas. */
	.panneau {
		display: flex;
		flex-direction: column;
		gap: 0.85rem;
		max-width: min(100%, 1200px);
		max-height: 100%;
	}

	.panneau img {
		display: block;
		max-width: 100%;
		max-height: calc(100vh - 11rem);
		width: auto;
		height: auto;
		object-fit: contain;
		margin: 0 auto;
		background: rgba(255, 255, 255, 0.04);
	}

	.legende {
		flex: none;
		max-width: 62ch;
		margin: 0 auto;
		text-align: center;
	}

	.titre {
		display: block;
		margin-bottom: 0.3rem;
		font-family: var(--police-texte);
		font-size: 1rem;
		font-weight: 600;
		line-height: 1.35;
		color: #eef0f3;
	}

	/* Bouton de fermeture EXPLICITE, en toutes lettres : une croix seule se devine,
	   un mot se lit. Aligné à droite au-dessus de l'image. */
	.fermer {
		align-self: flex-end;
		padding: 0.4rem 0.85rem;
		background: none;
		border: 1px solid rgba(238, 240, 243, 0.45);
		border-radius: 2px;
		font-family: var(--police-ui);
		font-size: 0.8rem;
		color: #eef0f3;
		cursor: pointer;
	}

	.fermer:hover {
		background: rgba(238, 240, 243, 0.12);
		border-color: #eef0f3;
	}

	.fermer:focus-visible {
		outline: 2px solid #eef0f3;
		outline-offset: 2px;
	}

	@media (max-width: 560px) {
		.panneau img {
			max-height: calc(100vh - 13rem);
		}
	}
</style>
