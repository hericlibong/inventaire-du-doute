<script>
	// Vignette d'une œuvre au format 4:3. Deux états :
	// - image affichée SEULEMENT si les droits sont clarifiés (statut open ou
	//   authorized) + url + credit. L'image entière devient alors un lien vers la
	//   notice POP ; le crédit apparaît DIRECTEMENT sous l'image (jamais caché).
	// - sinon : un placeholder soigné (bordure fine, pictogramme discret, mention
	//   « Reproduction non affichée »). Jamais un rectangle gris vide, jamais une
	//   fausse reproduction fabriquée.
	// Le modèle de données est prévu pour accueillir les images plus tard sans
	// reconstruire les cartes (décision 2026-07-14 ter, enrichie 2026-07-15).

	// `image` : { statut, url, alt, credit, licence, source } ; `href` : notice
	// POP (pour rendre l'image cliquable) ; `titre` : repli pour le texte alt.
	let { image = {}, href = null, titre = '' } = $props();

	const affichee = $derived(
		['open', 'authorized'].includes(image.statut) && !!image.url && !!image.credit
	);
</script>

{#if affichee}
	<figure class="vignette">
		{#if href}
			<a href={href} target="_blank" rel="noopener">
				<img src={image.url} alt={image.alt ?? titre} loading="lazy" />
			</a>
		{:else}
			<img src={image.url} alt={image.alt ?? titre} loading="lazy" />
		{/if}
		<figcaption>
			{image.credit}{#if image.licence} · {image.licence}{/if}
		</figcaption>
	</figure>
{:else}
	<div class="placeholder" role="img" aria-label="Reproduction non affichée, droits de réutilisation en cours de vérification">
		<svg viewBox="0 0 24 24" class="picto" aria-hidden="true">
			<rect x="3" y="5" width="18" height="14" rx="1.5" fill="none" stroke="currentColor" stroke-width="1.3" />
			<circle cx="8.5" cy="10" r="1.4" fill="currentColor" />
			<path d="M4 17l5-4 3.5 2.5L16 11l4 4" fill="none" stroke="currentColor" stroke-width="1.3" stroke-linejoin="round" />
		</svg>
		<p class="ph-titre">Reproduction non affichée</p>
		<p class="ph-sous">Droits de réutilisation en cours de vérification</p>
	</div>
{/if}

<style>
	.vignette {
		margin: 0;
	}

	.vignette img {
		display: block;
		width: 100%;
		aspect-ratio: 4 / 3;
		object-fit: cover;
		border-radius: 3px;
	}

	.vignette figcaption {
		margin-top: 0.3rem;
		font-size: 0.72rem;
		color: var(--couleur-encre-douce);
	}

	.placeholder {
		aspect-ratio: 4 / 3;
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		gap: 0.3rem;
		text-align: center;
		padding: 0.75rem;
		border: 1px solid var(--couleur-trait);
		border-radius: 3px;
		background: rgba(28, 26, 23, 0.015);
		color: var(--couleur-encre-douce);
	}

	.picto {
		width: 1.9rem;
		height: 1.9rem;
		opacity: 0.55;
	}

	.ph-titre {
		margin: 0.1rem 0 0;
		font-size: 0.82rem;
	}

	.ph-sous {
		margin: 0;
		font-size: 0.7rem;
		opacity: 0.8;
	}
</style>
