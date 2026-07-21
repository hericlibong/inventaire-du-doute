// Textes ÉDITORIAUX de la fiche maître — propres à chaque maître, en français
// courant. Couche éditoriale du front : ces phrases sont écrites à la main, elles
// ne sont PAS des données Joconde (Joconde reste la seule source de données ;
// voir CLAUDE.md, principes de rédaction). Les chiffres, eux, ne sont jamais
// stockés ici : ils restent calculés dans le composant depuis artistes.json.
//
// Un seul champ :
//   bio — LIGNE DE REPÉRAGE affichée sous le nom. Elle sert à situer l'artiste
//         pour un lecteur qui ne connaît pas l'histoire de l'art. Rien d'autre.
//
// GABARIT STRICT (2026-07-20), une phrase, sans exception :
//   « [Activité principale] [nationalité] du [siècle], [dates]. »
//
// Sont PROSCRITS dans cette ligne, même quand ils sont exacts : les noms de
// mouvements (rococo, baroque, néoclassique…), les périodes de connaisseur
// (Grand Siècle, Siècle d'or, Renaissance), les écoles (école de Bologne, école
// vénitienne, école de Fontainebleau), les fonctions de cour (premier peintre du
// roi, portraitiste de la cour des Valois) et toute formule savante non expliquée.
// Ces informations sont justes mais elles n'aident pas à se repérer : elles
// demandent elles-mêmes une explication.
//
// SIÈCLE : celui où l'artiste a TRAVAILLÉ, pas celui de sa naissance — un peintre
// né en 1599 et actif à partir de 1615 est un peintre du XVIIe siècle. Quand
// l'activité couvre réellement deux siècles, on écrit « des XVe et XVIe siècles ».
//
// DATES : relevées une fois pour toutes, hors ligne (aucune requête à l'affichage).
// Vérifiées sur les notices d'autorité et les encyclopédies de référence — INHA
// (Agorha), National Gallery, Larousse, Britannica, Wikipédia. Quand la naissance
// est discutée, on écrit « vers », comme le font ces notices : la prudence sur les
// dates est du même ordre que celle des musées sur les attributions.
//   • Titien : naissance placée entre 1488 et 1490 selon les sources → « vers 1488 ».
//   • François Clouet : « vers 1515 » (INHA : « Vers 1515 - 22/09/1572 »).
//
// Le paragraphe de situation ne porte pas d'angle interprétatif (décision
// 2026-07-10, 2e passe) : la lecture du graphique est générée depuis les données
// (voir NuageFamilles et territoires.js), elle n'est pas écrite à la main ici.
//
// ---------------------------------------------------------------------------
// Second champ, OPTIONNEL (2026-07-21) :
//   graphique — { titre, sousTitre } de l'en-tête du graphique, ÉCRITS À LA MAIN.
//
// Pourquoi : la version générée posait une question puis y répondait avec les
// mêmes mots (« Comment les musées rattachent ces œuvres à X » / « Les musées les
// rattachent surtout à… »). Deux textes, une seule fonction — la répétition
// trahissait la fabrication automatique. Les deux ont désormais des rôles
// distincts (consigne rédactionnelle du 2026-07-21) :
//   • le TITRE porte l'angle propre à l'artiste, 4 à 9 mots, jamais une question,
//     sans « profil », « corpus », « distribution » ni « attribution » abstraite ;
//   • le SOUS-TITRE apporte la preuve chiffrée ou la nuance, en une phrase, sans
//     reprendre les mots du titre. « Les musées rattachent » n'y revient pas
//     partout : la tournure change d'un artiste à l'autre.
//
// LES NOMBRES NE SONT JAMAIS ÉCRITS ICI (règle du fichier, inchangée) :
// `sousTitre` est une fonction qui les reçoit depuis artistes.json —
//   n       nombre de notices de la mention la plus fréquente ;
//   total   ensemble des notices à formulation prudente (« œuvres concernées ») ;
//   second  la deuxième mention en nombre ;
//   musees  musées détenteurs concernés ;
//   notices(code)  nombre pour une famille précise (0 si absente).
// Les artistes SANS ce champ gardent l'en-tête généré : la généralisation aux 27
// attend une validation rédactionnelle (decisions.md 2026-07-21 ter).

// Espace insécable : les guillemets français et le point-virgule ne doivent pas
// se retrouver seuls en début de ligne.
const NB = ' ';

export const EDITORIAL = {
	'Charles Le Brun': {
		bio: 'Peintre et décorateur français du XVIIe siècle, 1619–1690.',
		graphique: {
			titre: 'Charles Le Brun, l’école en tête',
			sousTitre: ({ n, total, second }) =>
				`${n} des ${total} œuvres concernées portent la mention «${NB}de son école${NB}», ` +
				`loin devant «${NB}attribué à${NB}», qui en réunit ${second}.`
		}
	},
	'Le Primatice': {
		bio: 'Peintre et décorateur italien du XVIe siècle, 1504–1570.',
		graphique: {
			titre: 'Le Primatice, entre sa main et son école',
			sousTitre: ({ n, second }) =>
				`${n} œuvres portent la mention «${NB}attribué à${NB}», ${second} celle ` +
				`«${NB}de son école${NB}»${NB}: les deux lectures se valent presque.`
		}
	},
	Ingres: {
		bio: 'Peintre français du XIXe siècle, 1780–1867.',
		graphique: {
			titre: 'Ingres, au plus près du maître',
			sousTitre: ({ n, total }) =>
				`${n} des ${total} œuvres concernées portent la mention «${NB}attribué à${NB}»${NB}; ` +
				'aucune autre formulation n’atteint la dizaine.'
		}
	},
	Rembrandt: {
		bio: 'Peintre et graveur néerlandais du XVIIe siècle, 1606–1669.',
		graphique: {
			titre: 'Rembrandt, surtout dans son influence',
			sousTitre: ({ n, total, notices }) =>
				`${n} des ${total} œuvres concernées portent la mention «${NB}à sa manière${NB}»${NB}; ` +
				`son atelier et son école n’en rassemblent que ${notices('atelier_de') + notices('ecole_de')}.`
		}
	},
	'Michel-Ange': {
		bio: 'Sculpteur, peintre et architecte italien des XVe et XVIe siècles, 1475–1564.',
		graphique: {
			titre: 'Michel-Ange, d’abord son école',
			sousTitre: ({ n, second }) =>
				`Deux fois plus d’œuvres sont dites «${NB}de son école${NB}» (${n}) que ` +
				`directement attribuées (${second}).`
		}
	},
	Rubens: {
		bio: 'Peintre flamand du XVIIe siècle, 1577–1640.',
		graphique: {
			titre: 'Rubens, presque tout à son école',
			sousTitre: ({ n, total, musees, notices }) =>
				`${n} des ${total} œuvres concernées sont dites «${NB}de son école${NB}», dispersées ` +
				`dans ${musees} musées${NB}; la mention «${NB}attribué à${NB}» n’en couvre que ${notices('attribue')}.`
		}
	},
	'François Clouet': {
		bio: 'Peintre portraitiste français du XVIe siècle, vers 1515–1572.',
		graphique: {
			titre: 'François Clouet, l’atelier en premier',
			sousTitre: ({ n, total, musees }) =>
				`${n} des ${total} œuvres concernées sont rattachées à son atelier, ` +
				`dans ${musees} musées différents.`
		}
	},
	'Annibale Carracci': {
		bio: 'Peintre italien des XVIe et XVIIe siècles, 1560–1609.',
		graphique: {
			titre: 'Annibale Carracci, surtout son cercle proche',
			sousTitre: ({ n, total, notices }) =>
				`${n} des ${total} œuvres concernées renvoient à son cercle${NB}; la mention ` +
				`«${NB}attribué à${NB}», qui suppose sa main, n’en couvre que ${notices('attribue')}.`
		}
	},
	Rodin: {
		bio: 'Sculpteur français des XIXe et XXe siècles, 1840–1917.',
		graphique: {
			titre: 'Rodin, une seule mention',
			sousTitre: ({ total, musees }) =>
				`Les ${total} œuvres concernées portent toutes la mention «${NB}attribué à${NB}», ` +
				`réparties dans ${musees} musées.`
		}
	},
	Boucher: {
		bio: 'Peintre français du XVIIIe siècle, 1703–1770.',
		graphique: {
			titre: 'Boucher, plusieurs formes de proximité',
			sousTitre: ({ n, total, second }) =>
				`Aucune mention n’atteint la moitié${NB}: «${NB}de son école${NB}» en réunit ${n} ` +
				`sur ${total}, «${NB}attribué à${NB}» ${second}.`
		}
	},
	'Andrea del Sarto': {
		bio: 'Peintre italien du XVIe siècle, 1486–1530.',
		graphique: {
			titre: 'Andrea del Sarto, l’école avant tout',
			sousTitre: ({ n, total, musees }) =>
				`${n} des ${total} œuvres concernées sont dites «${NB}de son école${NB}», ` +
				`dans ${musees} musées seulement.`
		}
	},
	'Guido Reni': {
		bio: 'Peintre italien du XVIIe siècle, 1575–1642.',
		graphique: {
			titre: 'Guido Reni, deux lectures voisines',
			sousTitre: ({ n, total, second }) =>
				`«${NB}De son école${NB}» et «${NB}attribué à${NB}» se tiennent de près${NB}: ` +
				`${n} contre ${second}, sur ${total} œuvres concernées.`
		}
	},
	'Nicolas Poussin': {
		bio: 'Peintre français du XVIIe siècle, 1594–1665.',
		graphique: {
			titre: 'Nicolas Poussin, sa main d’abord',
			sousTitre: ({ n, total }) =>
				`${n} des ${total} œuvres concernées portent la mention «${NB}attribué à${NB}»${NB}; ` +
				'les autres formes de proximité restent marginales.'
		}
	},
	'Simon Vouet': {
		bio: 'Peintre français du XVIIe siècle, 1590–1649.',
		graphique: {
			titre: 'Simon Vouet, aucune mention en tête',
			sousTitre: ({ n, total, musees }) =>
				`La mention la plus fréquente ne couvre que ${n} des ${total} œuvres ` +
				`concernées, dispersées dans ${musees} musées.`
		}
	},
	'Léonard de Vinci': {
		bio: 'Peintre et ingénieur italien des XVe et XVIe siècles, 1452–1519.',
		graphique: {
			titre: 'Léonard de Vinci, l’école plutôt que la main',
			sousTitre: ({ n, total, musees }) =>
				`${n} des ${total} œuvres concernées sont dites «${NB}de son école${NB}», ` +
				`et ${musees} musées les conservent toutes.`
		}
	},
	Greuze: {
		bio: 'Peintre français du XVIIIe siècle, 1725–1805.',
		graphique: {
			titre: 'Greuze, sa main puis son style',
			sousTitre: ({ n, total, notices }) =>
				`${n} des ${total} œuvres concernées portent la mention «${NB}attribué à${NB}»${NB}; ` +
				`${notices('maniere_de') + notices('suiveur_de') + notices('genre_de')} relèvent ` +
				'seulement de son style.'
		}
	},
	'Le Tintoret': {
		bio: 'Peintre italien du XVIe siècle, 1518–1594.',
		graphique: {
			titre: 'Le Tintoret, presque toujours « attribué à »',
			sousTitre: ({ n, total, second }) =>
				`${n} des ${total} œuvres concernées portent cette mention, ` +
				`contre ${second} pour la suivante.`
		}
	},
	'Van Dyck': {
		bio: 'Peintre portraitiste flamand du XVIIe siècle, 1599–1641.',
		graphique: {
			titre: 'Van Dyck, éparpillé entre les musées',
			// Pas de chiffre de mention ici : « 21 musées » et « 21 œuvres » se
			// lisaient dans la même phrase, deux nombres identiques pour deux choses
			// différentes.
			sousTitre: ({ total, musees }) =>
				`Ses ${total} œuvres concernées se répartissent dans ${musees} musées, ` +
				'et aucune mention n’en réunit la moitié.'
		}
	},
	'Le Corrège': {
		bio: 'Peintre italien du XVIe siècle, 1489–1534.',
		graphique: {
			titre: 'Le Corrège, l’école presque partout',
			sousTitre: ({ n, total }) =>
				`${n} des ${total} œuvres concernées sont dites «${NB}de son école${NB}»${NB}; ` +
				'sa main n’est presque jamais avancée.'
		}
	},
	'Pierre Mignard': {
		bio: 'Peintre portraitiste français du XVIIe siècle, 1612–1695.',
		graphique: {
			titre: 'Pierre Mignard, entre sa main et son entourage',
			sousTitre: ({ n, total }) =>
				`${n} des ${total} œuvres concernées lui sont attribuées${NB}; les autres ` +
				'renvoient à son école ou à son atelier.'
		}
	},
	'Véronèse': {
		bio: 'Peintre italien du XVIe siècle, 1528–1588.',
		graphique: {
			titre: 'Véronèse, l’atelier en tête',
			sousTitre: ({ n, total, second }) =>
				`${n} des ${total} œuvres concernées sortent de son atelier, ` +
				`${second} lui sont attribuées directement.`
		}
	},
	'Hyacinthe Rigaud': {
		bio: 'Peintre portraitiste français des XVIIe et XVIIIe siècles, 1659–1743.',
		graphique: {
			titre: 'Hyacinthe Rigaud, deux mentions à égalité',
			sousTitre: ({ n, total }) =>
				`«${NB}Attribué à${NB}» et «${NB}de son école${NB}» comptent chacune ${n} ` +
				`des ${total} œuvres concernées.`
		}
	},
	'Géricault': {
		bio: 'Peintre français du XIXe siècle, 1791–1824.',
		graphique: {
			titre: 'Géricault, sa main le plus souvent',
			sousTitre: ({ n, total, notices }) =>
				`${n} des ${total} œuvres concernées portent la mention «${NB}attribué à${NB}»${NB}; ` +
				`${notices('genre_de')} relèvent seulement de son goût.`
		}
	},
	Fragonard: {
		bio: 'Peintre français du XVIIIe siècle, 1732–1806.',
		graphique: {
			titre: 'Fragonard, presque toujours sa main',
			sousTitre: ({ n, total, second }) =>
				`${n} des ${total} œuvres concernées portent la mention «${NB}attribué à${NB}»${NB}; ` +
				`la suivante n’en réunit que ${second}.`
		}
	},
	'Raphaël': {
		bio: 'Peintre et architecte italien du XVIe siècle, 1483–1520.',
		graphique: {
			titre: 'Raphaël, plusieurs formes de proximité',
			sousTitre: ({ n, total, second }) =>
				`${n} des ${total} œuvres concernées lui sont attribuées, ${second} renvoient ` +
				'à son école, le reste à son atelier ou à son cercle.'
		}
	},
	Ribera: {
		bio: 'Peintre espagnol du XVIIe siècle, 1591–1652.',
		graphique: {
			titre: 'Ribera, un petit ensemble très dispersé',
			sousTitre: ({ n, total, musees }) =>
				`${total} œuvres concernées seulement, réparties dans ${musees} musées${NB}; ` +
				`«${NB}attribué à${NB}» en réunit ${n}.`
		}
	},
	Titien: {
		bio: 'Peintre italien du XVIe siècle, vers 1488–1576.',
		graphique: {
			titre: 'Titien, un partage entre sa main et son atelier',
			sousTitre: ({ n, total, second }) =>
				`${n} des ${total} œuvres concernées portent la mention «${NB}attribué à${NB}», ` +
				`${second} renvoient à son atelier.`
		}
	}
};

export function bioMaitre(nom) {
	return EDITORIAL[nom]?.bio ?? '';
}
