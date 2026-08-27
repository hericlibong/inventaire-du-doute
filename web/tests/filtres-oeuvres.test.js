// Tests des périmètres des deux filtres de l'onglet Œuvres (musée × mention).
// Exécution : node --test  (Node 22, runner natif ; aucune dépendance).
import { test } from 'node:test';
import assert from 'node:assert/strict';
import {
	regrouperMusees,
	filtrerParFamille,
	filtrerParMusee,
	museeCompatible
} from '../src/lib/filtres-oeuvres.js';

// Corpus miniature calqué sur la forme réelle de oeuvres/<slug>.json.
const O = [
	{ reference: '1', musee_code: 'M1', musee: 'Musée A', ville: 'Arles', code: 'attribue' },
	{ reference: '2', musee_code: 'M1', musee: 'Musée A', ville: 'Arles', code: 'attribue' },
	{ reference: '3', musee_code: 'M1', musee: 'Musée A', ville: 'Arles', code: 'ecole_de' },
	{ reference: '4', musee_code: 'M2', musee: 'Musée B', ville: 'Brest', code: 'ecole_de' },
	{ reference: '5', musee_code: 'M3', musee: 'Musée C', ville: 'Caen', code: 'point_interrogation' },
	{ reference: '6', musee_code: null, musee: null, ville: null, code: 'ecole_de' }
];

test('regrouperMusees : un objet par musée, effectif du périmètre, tri par valeur', () => {
	const m = regrouperMusees(O);
	assert.deepEqual(
		m.map((x) => [x.code, x.n]),
		[
			['M1', 3],
			['M2', 1],
			['M3', 1]
		]
	);
	assert.equal(m[0].nom, 'Musée A');
	assert.equal(m[0].ville, 'Arles');
});

test('regrouperMusees : une œuvre sans code Muséofile ne crée pas d’entrée', () => {
	const n = regrouperMusees(O).reduce((s, m) => s + m.n, 0);
	assert.equal(n, 5); // 6 œuvres, dont une sans musée
	assert.equal(regrouperMusees([{ musee_code: null }]).length, 0);
});

test('regrouperMusees : départage alphabétique à effectif égal', () => {
	const m = regrouperMusees([
		{ musee_code: 'MZ', musee: 'Zurbaran' },
		{ musee_code: 'MA', musee: 'Ancenis' }
	]);
	assert.deepEqual(m.map((x) => x.code), ['MA', 'MZ']);
});

test('menu des musées : borné à la mention active, effectifs recalculés', () => {
	const menu = regrouperMusees(filtrerParFamille(O, 'attribue'));
	assert.deepEqual(menu.map((x) => [x.code, x.n]), [['M1', 2]]);

	const menuQ = regrouperMusees(filtrerParFamille(O, 'point_interrogation'));
	assert.deepEqual(menuQ.map((x) => [x.code, x.n]), [['M3', 1]]);
});

test('total annoncé par « Tous les musées » : les œuvres de la mention, sans musée exclu', () => {
	assert.equal(filtrerParFamille(O, null).length, 6);
	assert.equal(filtrerParFamille(O, 'ecole_de').length, 3); // dont celle sans musée
});

test('puces de mention : calculées dans le musée actif, sans la mention active', () => {
	const codes = filtrerParMusee(O, 'M1').map((o) => o.code);
	assert.deepEqual(codes, ['attribue', 'attribue', 'ecole_de']);
	assert.equal(filtrerParMusee(O, null).length, 6);
});

test('liste finale : intersection des deux choix', () => {
	assert.deepEqual(
		filtrerParFamille(filtrerParMusee(O, 'M1'), 'attribue').map((o) => o.reference),
		['1', '2']
	);
	assert.deepEqual(filtrerParFamille(filtrerParMusee(O, 'M2'), 'attribue'), []);
});

test('museeCompatible : le musée survit à une mention qu’il conserve', () => {
	assert.equal(museeCompatible(O, 'M1', 'ecole_de'), true);
	assert.equal(museeCompatible(O, 'M1', 'point_interrogation'), false);
});

test('museeCompatible : « Toutes » et « Tous les musées » ne cassent rien', () => {
	assert.equal(museeCompatible(O, 'M3', null), true); // bouton « Toutes »
	assert.equal(museeCompatible(O, null, 'attribue'), true); // aucun musée choisi
});
