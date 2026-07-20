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

export const EDITORIAL = {
	'Charles Le Brun': {
		bio: 'Peintre et décorateur français du XVIIe siècle, 1619–1690.'
	},
	'Le Primatice': {
		bio: 'Peintre et décorateur italien du XVIe siècle, 1504–1570.'
	},
	Ingres: {
		bio: 'Peintre français du XIXe siècle, 1780–1867.'
	},
	Rembrandt: {
		bio: 'Peintre et graveur néerlandais du XVIIe siècle, 1606–1669.'
	},
	'Michel-Ange': {
		bio: 'Sculpteur, peintre et architecte italien des XVe et XVIe siècles, 1475–1564.'
	},
	Rubens: {
		bio: 'Peintre flamand du XVIIe siècle, 1577–1640.'
	},
	'François Clouet': {
		bio: 'Peintre portraitiste français du XVIe siècle, vers 1515–1572.'
	},
	'Annibale Carracci': {
		bio: 'Peintre italien des XVIe et XVIIe siècles, 1560–1609.'
	},
	Rodin: {
		bio: 'Sculpteur français des XIXe et XXe siècles, 1840–1917.'
	},
	Boucher: {
		bio: 'Peintre français du XVIIIe siècle, 1703–1770.'
	},
	'Andrea del Sarto': {
		bio: 'Peintre italien du XVIe siècle, 1486–1530.'
	},
	'Guido Reni': {
		bio: 'Peintre italien du XVIIe siècle, 1575–1642.'
	},
	'Nicolas Poussin': {
		bio: 'Peintre français du XVIIe siècle, 1594–1665.'
	},
	'Simon Vouet': {
		bio: 'Peintre français du XVIIe siècle, 1590–1649.'
	},
	'Léonard de Vinci': {
		bio: 'Peintre et ingénieur italien des XVe et XVIe siècles, 1452–1519.'
	},
	Greuze: {
		bio: 'Peintre français du XVIIIe siècle, 1725–1805.'
	},
	'Le Tintoret': {
		bio: 'Peintre italien du XVIe siècle, 1518–1594.'
	},
	'Van Dyck': {
		bio: 'Peintre portraitiste flamand du XVIIe siècle, 1599–1641.'
	},
	'Le Corrège': {
		bio: 'Peintre italien du XVIe siècle, 1489–1534.'
	},
	'Pierre Mignard': {
		bio: 'Peintre portraitiste français du XVIIe siècle, 1612–1695.'
	},
	'Véronèse': {
		bio: 'Peintre italien du XVIe siècle, 1528–1588.'
	},
	'Hyacinthe Rigaud': {
		bio: 'Peintre portraitiste français des XVIIe et XVIIIe siècles, 1659–1743.'
	},
	'Géricault': {
		bio: 'Peintre français du XIXe siècle, 1791–1824.'
	},
	Fragonard: {
		bio: 'Peintre français du XVIIIe siècle, 1732–1806.'
	},
	'Raphaël': {
		bio: 'Peintre et architecte italien du XVIe siècle, 1483–1520.'
	},
	Ribera: {
		bio: 'Peintre espagnol du XVIIe siècle, 1591–1652.'
	},
	Titien: {
		bio: 'Peintre italien du XVIe siècle, vers 1488–1576.'
	}
};

export function bioMaitre(nom) {
	return EDITORIAL[nom]?.bio ?? '';
}
