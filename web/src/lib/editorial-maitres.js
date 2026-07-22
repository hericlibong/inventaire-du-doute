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
//
// PIÈGE (corrigé le 2026-07-22) : `n` et `second` désignent des RANGS, pas des
// mentions. Trois sous-titres nommaient la mention en dur à côté d'un rang — « n
// œuvres portent la mention "attribué à" » — et se sont mis à mentir le jour où
// le classement a basculé : Le Primatice et Raphaël annonçaient l'inverse de
// leurs données, Michel-Ange disait « deux fois plus » pour un rapport devenu
// proche de trois. Dès qu'une phrase NOMME une mention, elle doit la chercher
// par son code avec `notices('ecole_de')`, jamais par son rang.
// Les artistes SANS ce champ gardent l'en-tête généré : les 36 maîtres instruits
// le 2026-07-22 sont dans ce cas, écrire 36 angles demandant une passe
// rédactionnelle à part (decisions.md 2026-07-21 ter).

// Espace insécable : les guillemets français et le point-virgule ne doivent pas
// se retrouver seuls en début de ligne.
const NB = ' ';

export const EDITORIAL = {
	'Charles Le Brun': {
		bio: 'Peintre et décorateur français du XVIIe siècle, 1619–1690.',
		graphique: {
			titre: 'Charles Le Brun, l’école en tête',
			sousTitre: ({ total, notices }) =>
				`${notices('ecole_de')} des ${total} œuvres concernées portent la mention «${NB}de son école${NB}», ` +
				`loin devant «${NB}attribué à${NB}», qui en réunit ${notices('attribue')}.`
		}
	},
	'Le Primatice': {
		bio: 'Peintre et décorateur italien du XVIe siècle, 1504–1570.',
		graphique: {
			titre: 'Le Primatice, son école devant sa main',
			sousTitre: ({ total, notices }) =>
				`${notices('ecole_de')} des ${total} œuvres concernées sont dites ` +
				`«${NB}de son école${NB}», ${notices('attribue')} lui sont directement attribuées.`
		}
	},
	Ingres: {
		bio: 'Peintre français du XIXe siècle, 1780–1867.',
		graphique: {
			titre: 'Ingres, au plus près du maître',
			sousTitre: ({ total, notices }) =>
				`${notices('attribue')} des ${total} œuvres concernées portent la mention «${NB}attribué à${NB}»${NB}; ` +
				'aucune autre formulation n’atteint la dizaine.'
		}
	},
	Rembrandt: {
		bio: 'Peintre et graveur néerlandais du XVIIe siècle, 1606–1669.',
		graphique: {
			titre: 'Rembrandt, surtout dans son influence',
			sousTitre: ({ total, notices }) =>
				`${notices('maniere_de')} des ${total} œuvres concernées portent la mention «${NB}à sa manière${NB}»${NB}; ` +
				`son atelier et son école n’en rassemblent que ${notices('atelier_de') + notices('ecole_de')}.`
		}
	},
	'Michel-Ange': {
		bio: 'Sculpteur, peintre et architecte italien des XVe et XVIe siècles, 1475–1564.',
		graphique: {
			titre: 'Michel-Ange, d’abord son école',
			sousTitre: ({ total, notices }) =>
				`${notices('ecole_de')} des ${total} œuvres concernées sont dites ` +
				`«${NB}de son école${NB}», contre ${notices('attribue')} attribuées à sa main.`
		}
	},
	Rubens: {
		bio: 'Peintre flamand du XVIIe siècle, 1577–1640.',
		graphique: {
			titre: 'Rubens, presque tout à son école',
			sousTitre: ({ total, musees, notices }) =>
				`${notices('ecole_de')} des ${total} œuvres concernées sont dites «${NB}de son école${NB}», dispersées ` +
				`dans ${musees} musées${NB}; la mention «${NB}attribué à${NB}» n’en couvre que ${notices('attribue')}.`
		}
	},
	'François Clouet': {
		bio: 'Peintre portraitiste français du XVIe siècle, vers 1515–1572.',
		graphique: {
			titre: 'François Clouet, l’atelier en premier',
			sousTitre: ({ total, musees, notices }) =>
				`${notices('atelier_de')} des ${total} œuvres concernées sont rattachées à son atelier, ` +
				`dans ${musees} musées différents.`
		}
	},
	'Annibale Carracci': {
		bio: 'Peintre italien des XVIe et XVIIe siècles, 1560–1609.',
		graphique: {
			titre: 'Annibale Carracci, surtout son cercle proche',
			sousTitre: ({ total, notices }) =>
				`${notices('entourage_de')} des ${total} œuvres concernées renvoient à son cercle${NB}; la mention ` +
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
			sousTitre: ({ total, notices }) =>
				`Aucune mention n’atteint la moitié${NB}: «${NB}de son école${NB}» en réunit ${notices('ecole_de')} ` +
				`sur ${total}, «${NB}attribué à${NB}» ${notices('attribue')}.`
		}
	},
	'Andrea del Sarto': {
		bio: 'Peintre italien du XVIe siècle, 1486–1530.',
		graphique: {
			titre: 'Andrea del Sarto, l’école avant tout',
			sousTitre: ({ total, musees, notices }) =>
				`${notices('ecole_de')} des ${total} œuvres concernées sont dites «${NB}de son école${NB}», ` +
				`dans ${musees} musées seulement.`
		}
	},
	'Guido Reni': {
		bio: 'Peintre italien du XVIIe siècle, 1575–1642.',
		graphique: {
			titre: 'Guido Reni, deux lectures voisines',
			sousTitre: ({ total, notices }) =>
				`«${NB}De son école${NB}» et «${NB}attribué à${NB}» se tiennent de près${NB}: ` +
				`${notices('ecole_de')} contre ${notices('attribue')}, sur ${total} œuvres concernées.`
		}
	},
	'Nicolas Poussin': {
		bio: 'Peintre français du XVIIe siècle, 1594–1665.',
		graphique: {
			titre: 'Nicolas Poussin, sa main d’abord',
			sousTitre: ({ total, notices }) =>
				`${notices('attribue')} des ${total} œuvres concernées portent la mention «${NB}attribué à${NB}»${NB}; ` +
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
			sousTitre: ({ total, musees, notices }) =>
				`${notices('ecole_de')} des ${total} œuvres concernées sont dites «${NB}de son école${NB}», ` +
				`et ${musees} musées les conservent toutes.`
		}
	},
	Greuze: {
		bio: 'Peintre français du XVIIIe siècle, 1725–1805.',
		graphique: {
			titre: 'Greuze, sa main puis son style',
			sousTitre: ({ total, notices }) =>
				`${notices('attribue')} des ${total} œuvres concernées portent la mention «${NB}attribué à${NB}»${NB}; ` +
				`${notices('maniere_de') + notices('suiveur_de') + notices('genre_de')} relèvent ` +
				'seulement de son style.'
		}
	},
	'Le Tintoret': {
		bio: 'Peintre italien du XVIe siècle, 1518–1594.',
		graphique: {
			titre: 'Le Tintoret, presque toujours « attribué à »',
			sousTitre: ({ total, second, notices }) =>
				`${notices('attribue')} des ${total} œuvres concernées portent cette mention, ` +
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
			sousTitre: ({ total, notices }) =>
				`${notices('ecole_de')} des ${total} œuvres concernées sont dites «${NB}de son école${NB}»${NB}; ` +
				'sa main n’est presque jamais avancée.'
		}
	},
	'Pierre Mignard': {
		bio: 'Peintre portraitiste français du XVIIe siècle, 1612–1695.',
		graphique: {
			titre: 'Pierre Mignard, entre sa main et son entourage',
			sousTitre: ({ total, notices }) =>
				`${notices('attribue')} des ${total} œuvres concernées lui sont attribuées${NB}; les autres ` +
				'renvoient à son école ou à son atelier.'
		}
	},
	'Véronèse': {
		bio: 'Peintre italien du XVIe siècle, 1528–1588.',
		graphique: {
			titre: 'Véronèse, l’atelier en tête',
			sousTitre: ({ total, notices }) =>
				`${notices('atelier_de')} des ${total} œuvres concernées sortent de son atelier, ` +
				`${notices('attribue')} lui sont attribuées directement.`
		}
	},
	'Hyacinthe Rigaud': {
		bio: 'Peintre portraitiste français des XVIIe et XVIIIe siècles, 1659–1743.',
		graphique: {
			titre: 'Hyacinthe Rigaud, deux mentions à égalité',
			sousTitre: ({ total, notices }) =>
				`«${NB}Attribué à${NB}» et «${NB}de son école${NB}» comptent chacune ${notices('attribue')} ` +
				`des ${total} œuvres concernées.`
		}
	},
	'Géricault': {
		bio: 'Peintre français du XIXe siècle, 1791–1824.',
		graphique: {
			titre: 'Géricault, sa main le plus souvent',
			sousTitre: ({ total, notices }) =>
				`${notices('attribue')} des ${total} œuvres concernées portent la mention «${NB}attribué à${NB}»${NB}; ` +
				`${notices('genre_de')} relèvent seulement de son goût.`
		}
	},
	Fragonard: {
		bio: 'Peintre français du XVIIIe siècle, 1732–1806.',
		graphique: {
			titre: 'Fragonard, presque toujours sa main',
			sousTitre: ({ total, second, notices }) =>
				`${notices('attribue')} des ${total} œuvres concernées portent la mention «${NB}attribué à${NB}»${NB}; ` +
				`la suivante n’en réunit que ${second}.`
		}
	},
	'Raphaël': {
		bio: 'Peintre et architecte italien du XVIe siècle, 1483–1520.',
		graphique: {
			titre: 'Raphaël, plusieurs formes de proximité',
			sousTitre: ({ total, notices }) =>
				`${notices('ecole_de')} des ${total} œuvres concernées sont dites ` +
				`«${NB}de son école${NB}», ${notices('attribue')} lui sont attribuées, ` +
				`${notices('atelier_de')} renvoient à son atelier.`
		}
	},
	Ribera: {
		bio: 'Peintre espagnol du XVIIe siècle, 1591–1652.',
		graphique: {
			titre: 'Ribera, un petit ensemble très dispersé',
			sousTitre: ({ total, musees, notices }) =>
				`${total} œuvres concernées seulement, réparties dans ${musees} musées${NB}; ` +
				`«${NB}attribué à${NB}» en réunit ${notices('attribue')}.`
		}
	},
	Titien: {
		bio: 'Peintre italien du XVIe siècle, vers 1488–1576.',
		graphique: {
			titre: 'Titien, un partage entre sa main et son atelier',
			sousTitre: ({ total, notices }) =>
				`${notices('attribue')} des ${total} œuvres concernées portent la mention «${NB}attribué à${NB}», ` +
				`${notices('atelier_de')} renvoient à son atelier.`
		}
	},

	// -------------------------------------------------------------------------
	// LOT DU 2026-07-22 — les 36 maîtres instruits au temps 5 du chantier de
	// fiabilisation. Même gabarit strict que ci-dessus, sans exception.
	//
	// DATES : relevées d'abord DANS LA BASE elle-même — le champ Auteur de Joconde
	// porte souvent les années entre parenthèses (« Bouchardon Edme (1698-1762) »,
	// 1 128 notices concordantes) — puis croisées avec les notices d'autorité. Le
	// « vers » est posé partout où la base se contredit ou où les notices hésitent :
	//   • Barocci : la base donne 1535 (×6), 1540 (×3) et 1528 (×1) → « vers 1535 ».
	//   • Campagnola : 1484 et 1500 à égalité dans la base → « vers 1500 ».
	//   • Botticelli : la base donne 1444, les notices d'autorité 1445 → « vers 1445 ».
	//   • Giordano : la base donne 1632 (×17) contre 1634 (×7) ; les notices
	//     d'autorité donnent 1634, qui est retenu.
	// Adolph Menzel est le seul dont la base ne porte AUCUNE date.
	//
	// Ces artistes n'ont PAS d'en-tête de graphique écrit à la main : ils gardent
	// l'en-tête généré, comme le prévoit la règle ci-dessus. Écrire 36 angles
	// demande une passe rédactionnelle à part.
	'Le Guerchin': { bio: 'Peintre italien du XVIIe siècle, 1591–1666.' },
	Bouchardon: { bio: 'Sculpteur français du XVIIIe siècle, 1698–1762.' },
	'Jules Romain': { bio: 'Peintre et architecte italien du XVIe siècle, vers 1499–1546.' },
	'Ludovico Carracci': { bio: 'Peintre italien des XVIe et XVIIe siècles, 1555–1619.' },
	'David Téniers': { bio: 'Peintre flamand du XVIIe siècle, 1610–1690.' },
	'François Gérard': { bio: 'Peintre français des XVIIIe et XIXe siècles, 1770–1837.' },
	'Le Parmesan': { bio: 'Peintre italien du XVIe siècle, 1503–1540.' },
	'Perino del Vaga': { bio: 'Peintre italien du XVIe siècle, 1501–1547.' },
	'Adolph Menzel': { bio: 'Peintre et graveur allemand du XIXe siècle, 1815–1905.' },
	'Baccio Bandinelli': { bio: 'Sculpteur italien du XVIe siècle, 1493–1560.' },
	'Antonio Tempesta': {
		bio: 'Peintre et graveur italien des XVIe et XVIIe siècles, 1555–1630.'
	},
	'Luca Giordano': { bio: 'Peintre italien du XVIIe siècle, 1634–1705.' },
	'Salvator Rosa': { bio: 'Peintre italien du XVIIe siècle, 1615–1673.' },
	'Federico Barocci': { bio: 'Peintre italien du XVIe siècle, vers 1535–1612.' },
	'Carlo Maratti': { bio: 'Peintre italien du XVIIe siècle, 1625–1713.' },
	'Federico Zuccaro': { bio: 'Peintre italien du XVIe siècle, vers 1540–1609.' },
	'Joseph Vernet': { bio: 'Peintre français du XVIIIe siècle, 1714–1789.' },
	'Luca Cambiaso': { bio: 'Peintre italien du XVIe siècle, 1527–1585.' },
	'Polidoro Caldara': { bio: 'Peintre italien du XVIe siècle, vers 1495–1543.' },
	'Gaspard Dughet': { bio: 'Peintre français du XVIIe siècle, vers 1615–1675.' },
	'Corneille de Lyon': {
		bio: 'Peintre néerlandais installé en France au XVIe siècle, vers 1510–1575.'
	},
	'Francesco Vanni': { bio: 'Peintre italien des XVIe et XVIIe siècles, vers 1565–1610.' },
	'Domenico Campagnola': {
		bio: 'Peintre et graveur italien du XVIe siècle, vers 1500–1564.'
	},
	'Philippe de Champaigne': {
		bio: 'Peintre flamand installé en France au XVIIe siècle, 1602–1674.'
	},
	'Laurent de La Hyre': { bio: 'Peintre français du XVIIe siècle, 1606–1656.' },
	'Giorgio Vasari': { bio: 'Peintre et architecte italien du XVIe siècle, 1511–1574.' },
	'Sébastien Bourdon': { bio: 'Peintre français du XVIIe siècle, 1616–1671.' },
	'Pier Francesco Mola': { bio: 'Peintre italien du XVIIe siècle, 1612–1666.' },
	'Jean-Baptiste Oudry': { bio: 'Peintre français du XVIIIe siècle, 1686–1755.' },
	'Louis Léopold Boilly': {
		bio: 'Peintre français des XVIIIe et XIXe siècles, 1761–1845.'
	},
	'Nicolas de Largillière': {
		bio: 'Peintre français des XVIIe et XVIIIe siècles, 1656–1746.'
	},
	'Paul Bril': { bio: 'Peintre flamand des XVIe et XVIIe siècles, vers 1554–1626.' },
	'Albrecht Dürer': {
		bio: 'Peintre et graveur allemand des XVe et XVIe siècles, 1471–1528.'
	},
	'Claude Lorrain': { bio: 'Peintre français du XVIIe siècle, 1600–1682.' },
	'Le Pérugin': { bio: 'Peintre italien des XVe et XVIe siècles, vers 1450–1523.' },
	Botticelli: { bio: 'Peintre italien du XVe siècle, vers 1445–1510.' }
};

export function bioMaitre(nom) {
	return EDITORIAL[nom]?.bio ?? '';
}
