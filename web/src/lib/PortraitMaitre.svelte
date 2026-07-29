<script>
	import { licenceEnFrancais } from '$lib/joconde.js';

	// Portrait du maître : il incarne le profil consulté, il appartient donc à la
	// fiche entière (header), pas à un onglet (décision 2026-07-11). Sorti de
	// NuageFamilles. Source SECONDAIRE d'illustration (Wikimedia Commons, stockée
	// en local) : jamais une donnée, jamais un comptage. Données et sourcing
	// inchangés — le composant consomme le même manifeste portraits.json.
	// `portrait` = entrée du manifeste (fichier, auteur, licence, source, regard)
	// ou undefined → placeholder neutre.
	let { maitre, portrait } = $props();

	// Légende au format normé (CLAUDE.md) : sujet, auteur de l'image, source,
	// licence — rien d'autre. « Autoportrait » quand l'auteur de l'image est le
	// maître lui-même.
	const legende = $derived.by(() => {
		if (!portrait) return null;
		// Comparaison insensible aux accents, traits d'union et casse : le manifeste
		// écrit « Louis-Léopold Boilly » là où le projet écrit « Louis Léopold Boilly ».
		// Égalité STRICTE seulement : « d'après Philippe de Champaigne » contient le nom
		// mais n'est pas un autoportrait — on ne l'affirme que si les deux coïncident.
		const aplat = (s) =>
			s
				.normalize('NFD')
				.replace(/[\u0300-\u036f]/g, '')
				.replace(/[-\s]+/g, ' ')
				.toLowerCase()
				.trim();
		const estAutoportrait = aplat(portrait.auteur) === aplat(maitre.nom);
		// Certaines fiches Commons ne donnent pas un nom mais une mention de statut
		// (« attribué à Jacopo Zucchi », « d'après Philippe de Champaigne », « auteur
		// inconnu »). On n'écrit pas « par attribué à… » : la mention se suffit.
		const mention = /^(attribué à|d'après|entourage de|atelier de|auteur inconnu)/.test(
			portrait.auteur
		);
		const sujet = estAutoportrait
			? `Autoportrait de ${maitre.nom}`
			: mention
				? `Portrait de ${maitre.nom}, ${portrait.auteur}`
				: `Portrait de ${maitre.nom}, par ${portrait.auteur}`;
		return { sujet, licence: licenceEnFrancais(portrait.licence), source: portrait.source };
	});
</script>

<figure class="portrait">
	{#if portrait}
		<!-- regard === 'droite' : portrait retourné pour regarder le texte de la fiche
		     (placé à sa gauche). Flip conservé tel quel (décision 2026-07-11). -->
		<img
			class="visage"
			class:retourne={portrait.regard === 'droite'}
			src={portrait.fichier}
			alt="Portrait de {maitre.nom}"
			loading="lazy"
		/>
		<figcaption class="portrait-legende">
			{legende.sujet}.
			{#if legende.source}<a href={legende.source} target="_blank" rel="noopener">Wikimedia Commons</a>{:else}Wikimedia Commons{/if},
			{legende.licence}.
		</figcaption>
	{:else}
		<svg viewBox="0 0 100 130" class="silhouette" role="img" aria-label="Pas de portrait fiable pour {maitre.nom}">
			<circle cx="50" cy="48" r="24" fill="#cdc3b2" />
			<path d="M14 130 Q14 84 50 84 Q86 84 86 130 Z" fill="#cdc3b2" />
		</svg>
		<figcaption class="portrait-legende">
			<em>Pas de portrait fiable disponible pour {maitre.nom}.</em>
		</figcaption>
	{/if}
</figure>

<style>
	.portrait {
		margin: 0;
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: 0.4rem;
		/* pas de cadre : l'image flotte, posée dans la marge du texte */
	}

	.visage,
	.silhouette {
		/* Vignette de gabarit FIXE : les portraits Commons ont des ratios variés ;
		   sans hauteur figée, chaque maître change la hauteur du header et fait
		   « sauter » la page au changement. Boîte constante + object-fit: contain =
		   même empreinte pour tous, sans rogner les visages. */
		width: 100%;
		height: 15rem;
		object-fit: contain;
		object-position: bottom;
		/* pas de cadre : l'image flotte, ombre douce pour la détacher du fond */
		filter: drop-shadow(0 4px 10px rgba(43, 30, 20, 0.18));
	}

	.visage.retourne {
		transform: scaleX(-1);
	}

	/* Crédit d'image en petit corps, format normé (sujet, auteur, source, licence). */
	.portrait-legende {
		font-size: 0.72rem;
		text-align: center;
		color: var(--couleur-encre-douce);
		line-height: 1.3;
	}

	.portrait-legende a {
		color: inherit;
		text-decoration: underline;
	}
</style>
