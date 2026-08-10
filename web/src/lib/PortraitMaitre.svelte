<script>
	import { base } from '$app/paths';
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
		// Élision devant voyelle ou h muet : « Portrait d'Auguste Vacquerie », et
		// non « de Auguste Vacquerie » (relevé le 2026-08-06, en ajoutant les
		// portraits du lot 2). Onze noms du corpus commencent par une voyelle —
		// Auguste Vacquerie, Antonio del Pollaiuolo, Albrecht Dürer, Ingres…
		// « Hyacinthe Rigaud » et « Henry Hennault » prennent aussi l'élision :
		// leur h est muet, comme celui de tous les prénoms concernés ici.
		const de = /^[aeiouyàâäéèêëîïôöùûüh]/i.test(maitre.nom) ? "d'" : 'de ';
		const sujet = estAutoportrait
			? `Autoportrait ${de}${maitre.nom}`
			: mention
				? `Portrait ${de}${maitre.nom}, ${portrait.auteur}`
				: `Portrait ${de}${maitre.nom}, par ${portrait.auteur}`;
		// Quand le crédit Commons nomme celui qui a PHOTOGRAPHIÉ le portrait et
		// non celui qui l'a fait, son nom se dit à part. Écrire « Portrait d'Aimé
		// Duthoit, par Bycro » attribuerait à un contributeur de 2021 une
		// photographie du XIXe siècle. La licence CC BY-SA exige ce crédit : il
		// est donné, à sa juste place.
		return {
			sujet,
			de,
			reproduction: portrait.reproduction ?? '',
			// Presque tous les portraits viennent de Commons, mais pas tous
			// (2026-08-06) : celui d'Alexandre Clausel a été trouvé ailleurs.
			// Une image ne se crédite jamais d'une source qui n'est pas la sienne.
			sourceNom: portrait.source_nom ?? 'Wikimedia Commons',
			licence: licenceEnFrancais(portrait.licence),
			source: portrait.source
		};
	});
</script>

<figure class="portrait">
	{#if portrait}
		<!-- regard === 'droite' : portrait retourné pour regarder le texte de la fiche
		     (placé à sa gauche). Flip conservé tel quel (décision 2026-07-11). -->
		<!-- `portrait.fichier` vient des données et commence par « / » : le préfixe de
		     publication s'ajoute à l'affichage, pas dans l'export (2026-08-10). -->
		<img
			class="visage"
			class:retourne={portrait.regard === 'droite'}
			src="{base}{portrait.fichier}"
			alt="Portrait {legende.de}{maitre.nom}"
			loading="lazy"
		/>
		<figcaption class="portrait-legende">
			{legende.sujet}.
			{#if legende.reproduction}Reproduction&nbsp;{legende.reproduction},{/if}
			{#if legende.source}<a href={legende.source} target="_blank" rel="noopener">{legende.sourceNom}</a>{:else}{legende.sourceNom}{/if},
			{legende.licence}.
		</figcaption>
	{/if}
	<!-- Sans portrait, ce composant ne rend RIEN : c'est le bandeau qui retire la
	     colonne et donne la place au texte (2026-08-06). La silhouette de
	     remplacement et la mention « Pas de portrait fiable disponible » ont été
	     supprimées — on ne comble pas une lacune par un ornement, et on ne la
	     commente pas non plus. -->
</figure>

<style>
	.portrait {
		margin: 0;
		display: flex;
		flex-direction: column;
		/* Aligné à GAUCHE depuis le 2026-08-08 : le crédit, centré sur trois lignes,
		   paraissait détaché du portrait comme du reste de la fiche. Calé sur le
		   bord gauche de l'image, il lui appartient visiblement. */
		align-items: flex-start;
		gap: 0.45rem;
		/* pas de cadre : l'image flotte, posée dans la marge du texte */
	}

	.visage {
		/* Vignette de gabarit FIXE : les portraits Commons ont des ratios variés ;
		   sans hauteur figée, chaque maître change la hauteur du header et fait
		   « sauter » la page au changement. Boîte constante + object-fit: contain =
		   même empreinte pour tous, sans rogner les visages. */
		width: 100%;
		/* 13 rem depuis le 2026-08-08 (au lieu de 15) : le portrait et sa légende
		   fixaient toute la hauteur du bandeau et laissaient 76 px de vide sous le
		   texte, à droite. Assez resserré pour que ce soit désormais le TEXTE qui
		   commande la hauteur ; assez grand pour rester un portrait et non une
		   vignette d'identification. */
		height: 13rem;
		object-fit: contain;
		/* `left bottom` et non `bottom` : l'image est calée sur le même bord que son
		   crédit, sinon un portrait étroit flotte au centre d'une boîte alignée à
		   gauche. */
		object-position: left bottom;
		/* pas de cadre : l'image flotte, ombre douce pour la détacher du fond */
		filter: drop-shadow(0 4px 10px rgba(43, 30, 20, 0.18));
	}

	.visage.retourne {
		transform: scaleX(-1);
	}

	/* Crédit d'image en petit corps, format normé (sujet, auteur, source, licence). */
	/* Crédit d'image : format normé (sujet, auteur, source, licence), aligné à
	   gauche sous l'image. Il tient généralement sur deux lignes ; il n'est JAMAIS
	   tronqué — une attribution, une licence et un lien sont des obligations, pas
	   des ornements que l'on coupe pour gagner de la place. */
	.portrait-legende {
		/* 0,7 rem sur une colonne de 14,5 rem : environ 41 signes par ligne. Le
		   crédit médian du corpus en compte 82 — il tient donc sur deux lignes dans
		   la majorité des cas, et sur trois pour les plus longs (Corneille de Lyon,
		   122 signes), sans jamais être coupé. */
		font-size: 0.7rem;
		text-align: left;
		color: var(--couleur-encre-douce);
		line-height: 1.35;
		max-width: 100%;
	}

	/* En colonne étroite, l'image suit la largeur de sa colonne (9 rem) : sans cela
	   une boîte de 13 rem de haut pour 9 rem de large étirerait le blanc autour d'un
	   portrait déjà petit. */
	@container (max-width: 38rem) {
		.visage {
			height: 9rem;
		}
	}

	.portrait-legende a {
		color: inherit;
		text-decoration: underline;
	}
</style>
