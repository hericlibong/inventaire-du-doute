// Textes ÉDITORIAUX de la fiche maître — propres à chaque maître, en français
// courant. Couche éditoriale du front : ces phrases sont écrites à la main, elles
// ne sont PAS des données Joconde (Joconde reste la seule source de données ;
// voir CLAUDE.md, principes de rédaction). Les chiffres, eux, ne sont jamais
// stockés ici : ils restent calculés dans le composant depuis artistes.json.
//
// Champ optionnel :
//   nomCivil — PONT entre le nom courant et celui que portent les notices
//         (2026-07-22). Quatorze maîtres sont connus sous un surnom qui
//         n'apparaît jamais tel quel dans Joconde : la fiche titre « Michel-Ange »
//         quand ses œuvres portent « BUONARROTI Michelangelo (attribué à) ». Sans
//         passerelle, le lecteur ne relie pas les deux. L'en-tête affiche donc
//         « Michel-Ange (Michelangelo Buonarroti) », en ordre naturel ; les
//         notices, elles, gardent le verbatim de Joconde, jamais réécrit.
//
// Un autre champ :
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
// Les 63 premiers artistes ont leur en-tête écrit ; les 39 du lot du
// 2026-08-02 n'en ont pas encore, l'en-tête généré
// ne sert plus que de filet pour un maître qu'on ajouterait sans l'écrire.

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
		nomCivil: 'Francesco Primaticcio',
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
		nomCivil: 'Michelangelo Buonarroti',
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
		nomCivil: 'Jacopo Robusti',
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
		nomCivil: 'Antonio Allegri',
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
		nomCivil: 'Paolo Caliari',
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
		nomCivil: 'Raffaello Sanzio',
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
		nomCivil: 'Tiziano Vecellio',
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
	// Leurs en-têtes de graphique ont été écrits le 2026-07-22, après les portraits :
	// même gabarit que les 27 (titre = l'angle, sous-titre = la preuve chiffrée),
	// et mention toujours nommée par son code, jamais par son rang.
	'Le Guerchin': { nomCivil: 'Giovanni Francesco Barbieri',
		bio: 'Peintre italien du XVIIe siècle, 1591–1666.',
		graphique: {
			titre: 'Le Guerchin, l’école et la main à égalité',
			sousTitre: ({ notices }) =>
				`${notices('ecole_de')} œuvres sont dites «${NB}de son école${NB}» et ${notices('attribue')} lui sont attribuées${NB}: trois notices séparent les deux formules.`
		}
	},
	Bouchardon: { bio: 'Sculpteur français du XVIIIe siècle, 1698–1762.',
		graphique: {
			titre: 'Bouchardon, sa main, et son école derrière',
			sousTitre: ({ total, musees, notices }) =>
				`${notices('attribue')} des ${total} œuvres concernées lui sont attribuées, ${notices('ecole_de')} renvoient à son école${NB}; ${musees} musées les conservent toutes.`
		}
	},
	'Jules Romain': { nomCivil: 'Giulio Pippi',
		bio: 'Peintre et architecte italien du XVIe siècle, vers 1499–1546.',
		graphique: {
			titre: 'Jules Romain, sa main et son école côte à côte',
			sousTitre: ({ notices }) =>
				`${notices('attribue')} œuvres lui sont attribuées, ${notices('ecole_de')} sont dites «${NB}de son école${NB}»${NB}: les musées n’ont pas tranché.`
		}
	},
	'Ludovico Carracci': { bio: 'Peintre italien des XVIe et XVIIe siècles, 1555–1619.',
		graphique: {
			titre: 'Ludovico Carracci, presque tout sur son nom',
			sousTitre: ({ total, notices }) =>
				`${notices('attribue')} des ${total} œuvres concernées portent la mention «${NB}attribué à${NB}»${NB}; aucune autre formule n’en réunit plus de deux.`
		}
	},
	'David Téniers': { bio: 'Peintre flamand du XVIIe siècle, 1610–1690.',
		graphique: {
			titre: 'David Téniers, dispersé et jamais tranché',
			sousTitre: ({ total, musees }) =>
				`Ses ${total} œuvres concernées se répartissent dans ${musees} musées, et la formule la plus fréquente n’en couvre qu’un tiers.`
		}
	},
	'François Gérard': { bio: 'Peintre français des XVIIIe et XIXe siècles, 1770–1837.',
		graphique: {
			titre: 'François Gérard, sa main puis son atelier',
			sousTitre: ({ total, notices }) =>
				`${notices('attribue')} des ${total} œuvres concernées lui sont attribuées${NB}; ${notices('atelier_de')} sortent de son atelier.`
		}
	},
	'Le Parmesan': { nomCivil: 'Francesco Mazzuola',
		bio: 'Peintre italien du XVIe siècle, 1503–1540.',
		graphique: {
			titre: 'Le Parmesan, tout entier dans un seul musée',
			sousTitre: ({ total, notices }) =>
				`Les ${total} œuvres concernées sont conservées par un unique établissement${NB}; ${notices('attribue')} lui sont attribuées, ${notices('ecole_de')} renvoient à son école.`
		}
	},
	'Perino del Vaga': { nomCivil: 'Piero Bonaccorsi',
		bio: 'Peintre italien du XVIe siècle, 1501–1547.',
		graphique: {
			titre: 'Perino del Vaga, de sa main à son atelier',
			sousTitre: ({ notices }) =>
				`${notices('attribue')} œuvres lui sont attribuées, ${notices('atelier_de')} à son atelier et ${notices('ecole_de')} à son école${NB}: la distance se creuse par degrés.`
		}
	},
	'Adolph Menzel': { bio: 'Peintre et graveur allemand du XIXe siècle, 1815–1905.',
		graphique: {
			titre: 'Adolph Menzel, une seule formule, un seul musée',
			sousTitre: ({ total }) =>
				`Les ${total} œuvres concernées sont toutes dites «${NB}de son école${NB}», et un même établissement les conserve.`
		}
	},
	'Baccio Bandinelli': { bio: 'Sculpteur italien du XVIe siècle, 1493–1560.',
		graphique: {
			titre: 'Baccio Bandinelli, l’école devant la main',
			sousTitre: ({ notices }) =>
				`${notices('ecole_de')} œuvres sont dites «${NB}de son école${NB}», ${notices('attribue')} lui sont attribuées — toutes au même endroit.`
		}
	},
	'Antonio Tempesta': {
		bio: 'Peintre et graveur italien des XVIe et XVIIe siècles, 1555–1630.',
		graphique: {
			titre: 'Antonio Tempesta, une seule réserve revient',
			sousTitre: ({ total, notices }) =>
				`${notices('attribue')} des ${total} œuvres concernées portent la mention «${NB}attribué à${NB}»${NB}; les autres formules n’apparaissent qu’une fois chacune.`
		}
	},
	'Luca Giordano': { bio: 'Peintre italien du XVIIe siècle, 1634–1705.',
		graphique: {
			titre: 'Luca Giordano, entre sa main et son atelier',
			sousTitre: ({ musees, notices }) =>
				`${notices('attribue')} œuvres lui sont attribuées, ${notices('atelier_de')} à son atelier${NB}; elles circulent dans ${musees} musées.`
		}
	},
	'Salvator Rosa': { bio: 'Peintre italien du XVIIe siècle, 1615–1673.',
		graphique: {
			titre: 'Salvator Rosa, un style qui a fait suite',
			sousTitre: ({ notices }) =>
				`${notices('ecole_de')} œuvres sont dites «${NB}de son école${NB}» et ${notices('suiveur_de') + notices('maniere_de') + notices('genre_de')} ne retiennent que sa façon de peindre${NB}; ${notices('attribue')} lui sont attribuées directement.`
		}
	},
	'Federico Barocci': { bio: 'Peintre italien du XVIe siècle, vers 1535–1612.',
		graphique: {
			titre: 'Federico Barocci, deux tiers sur son nom',
			sousTitre: ({ total, notices }) =>
				`${notices('attribue')} des ${total} œuvres concernées lui sont attribuées, ${notices('ecole_de')} renvoient à son école.`
		}
	},
	'Carlo Maratti': { bio: 'Peintre italien du XVIIe siècle, 1625–1713.',
		graphique: {
			titre: 'Carlo Maratti, son atelier signe pour lui',
			sousTitre: ({ total, notices }) =>
				`${notices('atelier_de')} des ${total} œuvres concernées sortent de son atelier${NB}; ${notices('attribue')} seulement lui sont attribuées directement.`
		}
	},
	'Federico Zuccaro': { bio: 'Peintre italien du XVIe siècle, vers 1540–1609.',
		graphique: {
			titre: 'Federico Zuccaro, son école efface sa main',
			sousTitre: ({ total, notices }) =>
				`${notices('ecole_de')} des ${total} œuvres concernées sont dites «${NB}de son école${NB}»${NB}; ${notices('attribue')} seulement portent son nom sans détour.`
		}
	},
	'Joseph Vernet': { bio: 'Peintre français du XVIIIe siècle, 1714–1789.',
		graphique: {
			titre: 'Joseph Vernet, sa main, et peu d’autre chose',
			sousTitre: ({ total, musees, notices }) =>
				`${notices('attribue')} des ${total} œuvres concernées lui sont attribuées, dans ${musees} musées différents.`
		}
	},
	'Luca Cambiaso': { bio: 'Peintre italien du XVIe siècle, 1527–1585.',
		graphique: {
			titre: 'Luca Cambiaso, la réserve la plus légère',
			sousTitre: ({ total, notices }) =>
				`${notices('attribue')} des ${total} œuvres concernées portent la mention «${NB}attribué à${NB}», la plus proche de sa main${NB}; aucune autre n’en réunit plus de trois.`
		}
	},
	'Polidoro Caldara': { bio: 'Peintre italien du XVIe siècle, vers 1495–1543.',
		graphique: {
			titre: 'Polidoro Caldara, sa main et son entourage',
			sousTitre: ({ musees, notices }) =>
				`${notices('attribue')} œuvres lui sont attribuées, ${notices('entourage_de')} renvoient à son entourage${NB}; ${musees} musées les conservent.`
		}
	},
	'Gaspard Dughet': { bio: 'Peintre français du XVIIe siècle, vers 1615–1675.',
		graphique: {
			titre: 'Gaspard Dughet, autant son style que sa main',
			sousTitre: ({ notices }) =>
				`${notices('attribue')} œuvres lui sont attribuées, mais ${notices('maniere_de') + notices('genre_de')} ne retiennent que sa façon de peindre et ${notices('ecole_de')} son école.`
		}
	},
	'Corneille de Lyon': {
		bio: 'Peintre néerlandais installé en France au XVIe siècle, vers 1510–1575.',
		graphique: {
			titre: 'Corneille de Lyon, un atelier plus qu’un homme',
			sousTitre: ({ total, notices }) =>
				`${notices('atelier_de')} des ${total} œuvres concernées sortent de son atelier${NB}; ${notices('attribue')} seulement lui sont attribuées.`
		}
	},
	'Francesco Vanni': { bio: 'Peintre italien des XVIe et XVIIe siècles, vers 1565–1610.',
		graphique: {
			titre: 'Francesco Vanni, la même réserve d’un bout à l’autre',
			sousTitre: ({ total, notices }) =>
				`${notices('attribue')} des ${total} œuvres concernées portent la mention «${NB}attribué à${NB}»${NB}; ${total - notices('attribue')} seulement portent une autre formule.`
		}
	},
	'Domenico Campagnola': {
		bio: 'Peintre et graveur italien du XVIe siècle, vers 1500–1564.',
		graphique: {
			titre: 'Domenico Campagnola, son nom presque partout',
			sousTitre: ({ total, notices }) =>
				`${notices('attribue')} des ${total} œuvres concernées lui sont attribuées${NB}; les quelques autres se répartissent entre trois formules.`
		}
	},
	'Philippe de Champaigne': {
		bio: 'Peintre flamand installé en France au XVIIe siècle, 1602–1674.',
		graphique: {
			titre: 'Philippe de Champaigne, la moitié sur son nom',
			sousTitre: ({ total, musees, notices }) =>
				`${notices('attribue')} des ${total} œuvres concernées lui sont attribuées${NB}; les autres renvoient à son atelier, son école ou son entourage, dans ${musees} musées.`
		}
	},
	'Laurent de La Hyre': { bio: 'Peintre français du XVIIe siècle, 1606–1656.',
		graphique: {
			titre: 'Laurent de La Hyre, une réserve unique ou presque',
			sousTitre: ({ total, notices }) =>
				`${notices('attribue')} des ${total} œuvres concernées portent la mention «${NB}attribué à${NB}»${NB}; ${notices('ecole_de') + notices('atelier_de')} seulement renvoient à son école ou à son atelier.`
		}
	},
	'Giorgio Vasari': { bio: 'Peintre et architecte italien du XVIe siècle, 1511–1574.',
		graphique: {
			titre: 'Giorgio Vasari, son école passe devant',
			sousTitre: ({ total, notices }) =>
				`${notices('ecole_de')} des ${total} œuvres concernées sont dites «${NB}de son école${NB}», ${notices('attribue')} lui sont attribuées.`
		}
	},
	'Sébastien Bourdon': { bio: 'Peintre français du XVIIe siècle, 1616–1671.',
		graphique: {
			titre: 'Sébastien Bourdon, sa main, dispersée',
			sousTitre: ({ total, musees, notices }) =>
				`${notices('attribue')} des ${total} œuvres concernées lui sont attribuées, réparties dans ${musees} musées.`
		}
	},
	'Pier Francesco Mola': { bio: 'Peintre italien du XVIIe siècle, 1612–1666.',
		graphique: {
			titre: 'Pier Francesco Mola, peu d’œuvres, peu d’écarts',
			sousTitre: ({ total, notices }) =>
				`${notices('attribue')} des ${total} œuvres concernées lui sont attribuées${NB}; ${total - notices('attribue')} seulement portent une formule plus distante.`
		}
	},
	'Jean-Baptiste Oudry': { bio: 'Peintre français du XVIIIe siècle, 1686–1755.',
		graphique: {
			titre: 'Jean-Baptiste Oudry, la même réserve partout',
			sousTitre: ({ total, musees, notices }) =>
				`${notices('attribue')} des ${total} œuvres concernées portent la mention «${NB}attribué à${NB}», dans ${musees} musées différents.`
		}
	},
	'Louis Léopold Boilly': {
		bio: 'Peintre français des XVIIIe et XIXe siècles, 1761–1845.',
		graphique: {
			titre: 'Louis Léopold Boilly, jamais deux fois au même endroit',
			sousTitre: ({ total, musees, notices }) =>
				`Ses ${total} œuvres concernées se répartissent dans ${musees} musées${NB}; ${notices('attribue')} portent la mention «${NB}attribué à${NB}».`
		}
	},
	'Nicolas de Largillière': {
		bio: 'Peintre français des XVIIe et XVIIIe siècles, 1656–1746.',
		graphique: {
			titre: 'Nicolas de Largillière, aucun musée en tête',
			sousTitre: ({ total, musees }) =>
				`Ses ${total} œuvres concernées se dispersent dans ${musees} musées, sans qu’aucun n’en réunisse plus de deux.`
		}
	},
	'Paul Bril': { bio: 'Peintre flamand des XVIe et XVIIe siècles, vers 1554–1626.',
		graphique: {
			titre: 'Paul Bril, sa main et son style à parts égales',
			sousTitre: ({ notices }) =>
				`${notices('attribue')} œuvres lui sont attribuées et autant ne retiennent que sa manière${NB}; aucune formule ne l’emporte.`
		}
	},
	'Albrecht Dürer': {
		bio: 'Peintre et graveur allemand des XVe et XVIe siècles, 1471–1528.',
		graphique: {
			titre: 'Albrecht Dürer, plus son école que lui',
			sousTitre: ({ total, notices }) =>
				`${notices('ecole_de')} des ${total} œuvres concernées sont dites «${NB}de son école${NB}», ${notices('attribue')} lui sont attribuées.`
		}
	},
	'Claude Lorrain': { nomCivil: 'Claude Gellée',
		bio: 'Peintre français du XVIIe siècle, 1600–1682.',
		graphique: {
			titre: 'Claude Lorrain, un ensemble court et net',
			sousTitre: ({ total, notices }) =>
				`${notices('attribue')} des ${total} œuvres concernées lui sont attribuées${NB}; ${notices('ecole_de')} renvoient à son école.`
		}
	},
	'Le Pérugin': { nomCivil: 'Pietro Vannucci',
		bio: 'Peintre italien des XVe et XVIe siècles, vers 1450–1523.',
		graphique: {
			titre: 'Le Pérugin, son école et son atelier',
			sousTitre: ({ total, notices }) =>
				`${notices('ecole_de')} des ${total} œuvres concernées sont dites «${NB}de son école${NB}», ${notices('atelier_de')} renvoient à son atelier${NB}; ${notices('attribue')} seulement lui sont attribuées.`
		}
	},
	Botticelli: { nomCivil: 'Alessandro Filipepi',
		bio: 'Peintre italien du XVe siècle, vers 1445–1510.',
		graphique: {
			titre: 'Botticelli, son école, presque jamais lui',
			sousTitre: ({ total, notices }) =>
				`${notices('ecole_de')} des ${total} œuvres concernées sont dites «${NB}de son école${NB}», ${notices('atelier_de')} renvoient à son atelier${NB}; son nom seul n’est presque jamais avancé.`
		}
	},

	// =========================================================================
	// LOT 2 (2026-08-06) — les 39 artistes entrés au volume le 2026-08-02.
	//
	// Ils ne ressemblent pas aux 63 premiers : ce ne sont pas des maîtres
	// anciens mais, pour la plupart, des figures locales du XIXe siècle —
	// l'imagerie d'Épinal (Pinot, Georgin, Morinet, Ensfelder, Hennault), la
	// manufacture de Sèvres (Leloy, Willermet), les sculpteurs d'Amiens (les
	// frères Duthoit), le cercle de Rodin (Beuret, Roche), celui de Victor Hugo
	// (Charles Hugo, Vacquerie). Beaucoup n'ont pas de notice d'autorité.
	//
	// MÉTHODE (docs/decisions.md, 2026-08-06) — trois sources, dans cet ordre :
	//   1. JOCONDE ELLE-MÊME. Les musées écrivent les dates et le métier dans le
	//      champ auteur : « Hussenot Joseph (1827-1896) (dessinateur) ». C'est la
	//      source la plus proche du corpus, et le seul arbitre valable face aux
	//      homonymes. Dates pour 31 des 39, fonction pour 26.
	//   2. Une notice d'autorité (Wikidata, BnF, INHA, Louvre-arts graphiques,
	//      ministère de la Culture) — retenue SEULEMENT si ses dates concordent
	//      avec celles des musées.
	//   3. Rien. Quand ni l'une ni l'autre ne dit, on n'écrit pas.
	//
	// L'ACTIVITÉ ANNONCÉE REND COMPTE DU CORPUS, pas de la notoriété. Auguste
	// Vacquerie est connu comme écrivain, mais ses 366 notices sont des
	// photographies : la ligne dit d'abord photographe. Même règle pour Charles
	// Hugo. C'est ce que le lecteur a sous les yeux qui commande.
	//
	// DEUX EXTENSIONS DU GABARIT, arrêtées le 2026-08-06 :
	//   • « actif entre X et Y » quand aucune date de vie n'est attestée. Un seul
	//     cas, Henry Hennault, dont Joconde et le musée de l'Image ne connaissent
	//     que les années de collaboration avec Pellerin.
	//   • « après Y » quand la mort n'est pas datée (Willermet, d'après le
	//     ministère de la Culture : « 1783-après 1848 »).
	//
	// DIVERGENCES DE DATES relevées et tranchées en faveur des musées, sauf
	// mention : Aimé Duthoit (Joconde 1803, Wikidata 1805), Frans Hogenberg
	// (Joconde 1592, Wikidata 1590 — retenu 1590, plus courant), Colijn de Coter
	// et Antonio del Pollaiuolo (écarts de quelques années, d'où le « vers »).
	// Détail dans docs/donnees.md.
	//
	// UN HOMONYME ÉVITÉ, à ne pas rouvrir : « Charles du Ry ». La recherche
	// propose Q1066622, architecte à Kassel (1692-1757). Ce n'est pas lui : le
	// Louvre, seul conservateur de ces 33 dessins, donne « vers 1568-1655,
	// école française, architecte des Bâtiments du roi en 1636 » — le
	// bisaïeul. Même famille, même métier, un siècle d'écart.
	// =========================================================================

	'Alexandre Clausel': {
		bio: 'Photographe français du XIXe siècle, 1802–1884.'
	},
	'Charles Normand': { nomCivil: 'Charles Pierre Joseph Normand',
		bio: 'Dessinateur et graveur français des XVIIIe et XIXe siècles, 1765–1840.'
	},
	'Léon Tirode': {
		bio: 'Peintre français des XIXe et XXe siècles, 1873–1956.'
	},
	'Louis Morinet': {
		bio: 'Dessinateur français des XIXe et XXe siècles, 1863–1926.'
	},
	'Giacinto Calandrucci': {
		bio: 'Peintre et dessinateur italien du XVIIe siècle, 1646–1707.'
	},
	'Georges Ferdinand Bigot': {
		bio: 'Dessinateur et graveur français des XIXe et XXe siècles, 1860–1927.'
	},
	'Léon Fort': {
		bio: 'Peintre et dessinateur français du XXe siècle, 1870–1965.'
	},
	'Louis Duthoit': {
		bio: 'Sculpteur et dessinateur français du XIXe siècle, 1807–1874.'
	},
	'Aimé Duthoit': {
		bio: 'Sculpteur et dessinateur français du XIXe siècle, 1803–1869.'
	},
	'Charles François Pinot': {
		bio: 'Dessinateur et imprimeur français du XIXe siècle, 1817–1874.'
	},
	'André Marie Florentin Giraud': {
		bio: 'Dessinateur français du XIXe siècle, 1781–1864.'
	},
	'Auguste Vacquerie': {
		bio: 'Photographe et écrivain français du XIXe siècle, 1819–1895.'
	},
	'Charles Eugène Ensfelder': {
		bio: 'Dessinateur français du XIXe siècle, 1836–1876.'
	},
	'François Georgin': {
		bio: 'Graveur français du XIXe siècle, 1801–1863.'
	},
	'Louis Verjat': {
		bio: 'Photographe français des XIXe et XXe siècles, 1857–1933.'
	},
	// Nationalité laissée de côté à dessein : Wikidata le dit « artiste
	// britannique » dans sa description et français par sa citoyenneté. Tant que
	// la contradiction n'est pas levée, la ligne ne tranche pas.
	'Peter Hawke': {
		bio: 'Dessinateur et lithographe du XIXe siècle, 1801–1887.'
	},
	'Auguste Alleaume': {
		bio: 'Peintre verrier et dessinateur français des XIXe et XXe siècles, 1854–1940.'
	},
	'Antoine Gabriel Willermet': {
		bio: 'Peintre et dessinateur français du XIXe siècle, 1783 – après 1848.'
	},
	'Turpin de Crissé': { nomCivil: 'Lancelot Théodore Turpin de Crissé',
		bio: 'Peintre et dessinateur français du XIXe siècle, 1782–1859.'
	},
	'Charles Hugo': {
		bio: 'Photographe et journaliste français du XIXe siècle, 1826–1871.'
	},
	'Gustave Lancelot': {
		bio: 'Photographe et dessinateur français du XIXe siècle, 1830–1906.'
	},
	'Charles du Ry': {
		bio: 'Architecte et dessinateur français du XVIIe siècle, vers 1568–1655.'
	},
	'Odilon Roche': {
		bio: 'Dessinateur français du XXe siècle, 1868–1947.'
	},
	'Frans Hogenberg': {
		bio: 'Graveur flamand du XVIe siècle, 1535–1590.'
	},
	'Nicolaus Hoffmann': {
		bio: 'Dessinateur allemand des XVIIIe et XIXe siècles, 1740–1823.'
	},
	'Nicasius Bernaerts': {
		bio: 'Peintre flamand du XVIIe siècle, 1620–1678.'
	},
	// Apostrophe DROITE : la clé doit reprendre le nom du corpus au signe près
	// (artistes.json), sinon la fiche perd sa ligne sans rien signaler.
	"Crispin de Passe l'Ancien": {
		bio: 'Graveur néerlandais des XVIe et XVIIe siècles, 1564–1637.'
	},
	'Crispin de Passe le Jeune': {
		bio: 'Graveur néerlandais du XVIIe siècle, 1593–1670.'
	},
	'Amable Louis Crapelet': {
		bio: 'Peintre et dessinateur français du XIXe siècle, 1822–1867.'
	},
	'Auguste Beuret': {
		bio: 'Dessinateur français des XIXe et XXe siècles, 1866–1934.'
	},
	'Jean-Charles François Leloy': {
		bio: 'Dessinateur d’ornements français du XIXe siècle, 1774–1846.'
	},
	'Joseph Hussenot': {
		bio: 'Dessinateur français du XIXe siècle, 1827–1896.'
	},
	'Colijn de Coter': {
		bio: 'Peintre flamand des XVe et XVIe siècles, vers 1455 – vers 1539.'
	},
	'Antonio del Pollaiuolo': {
		bio: 'Peintre et sculpteur italien du XVe siècle, vers 1433–1498.'
	},
	// Aucune date de vie attestée : ni Joconde, ni le musée de l'Image, ni
	// Gallica ne connaissent autre chose que ses années chez Pellerin.
	'Henry Hennault': {
		bio: 'Dessinateur français, actif entre 1891 et 1901.'
	},
	'Israël Henriet': {
		bio: 'Graveur et éditeur français du XVIIe siècle, 1590–1661.'
	},
	'René Ackermann': {
		bio: 'Imprimeur et lithographe français du XIXe siècle, 1853–1913.'
	},
	'Louis Hertig': {
		bio: 'Sculpteur français du XXe siècle, 1880–1958.'
	},
	'Jacques-Louis David': {
		bio: 'Peintre français des XVIIIe et XIXe siècles, 1748–1825.'
	}
};

export function bioMaitre(nom) {
	return EDITORIAL[nom]?.bio ?? '';
}

// Nom d'état civil, quand le maître est connu sous un surnom. Sert de pont avec
// le nom que portent ses notices Joconde ; vide pour les autres.
export function nomCivilMaitre(nom) {
	return EDITORIAL[nom]?.nomCivil ?? '';
}
