// Tests de la règle déterministe de phrase (onglet Profil).
// Exécution : node --test  (Node 22, runner natif ; aucune dépendance).
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { phraseRepartition } from '../src/lib/phrase-repartition.js';

// Ordre canonique réel (copie de ORDRE_FAMILLES ; le test reste hors bundler).
const ordre = [
	'attribue', 'point_interrogation', 'atelier_de', 'entourage_de',
	'ecole_de', 'suiveur_de', 'maniere_de', 'genre_de'
];
// Libellés publics (mêmes valeurs que familles-public.js).
const LABEL = {
	attribue: 'attribué à', point_interrogation: 'nom (?)', atelier_de: 'son atelier',
	entourage_de: 'son cercle', ecole_de: 'de son école', suiveur_de: 'un suiveur',
	maniere_de: 'sa manière', genre_de: 'dans son goût'
};
// insécables normalisés en espace simple pour des assertions lisibles
const P = (familles, total) =>
	phraseRepartition(familles, total, { label: (c) => LABEL[c], ordre })?.replace(/\u00A0/g, ' ');

const F = (o) => Object.entries(o).map(([code, notices]) => ({ code, notices }));

test('Federico Zuccaro — une mention ≥ 60 %, citée seule', () => {
	const s = P(F({ ecole_de: 30, attribue: 3, entourage_de: 2, point_interrogation: 1, maniere_de: 1 }), 37);
	assert.match(s, /^30 des 37 œuvres concernées portent la mention «.de son école.»/u);
	assert.match(s, /les autres formulations restent minoritaires\.$/u);
});

test('Claude Lorrain — forte majorité « attribué à », citée seule', () => {
	const s = P(F({ attribue: 17, ecole_de: 3 }), 20);
	assert.match(s, /^17 des 20 œuvres concernées portent la mention «.attribué à.»/u);
	assert.match(s, /minoritaires\.$/u);
});

test('Paul Bril — égalité en tête (7 = 7), les deux citées au pluriel', () => {
	const s = P(F({ attribue: 7, maniere_de: 7, ecole_de: 3, genre_de: 3, point_interrogation: 1, suiveur_de: 1 }), 22);
	assert.match(s, /^À égalité, /u);
	// ordre canonique : attribué à AVANT sa manière
	assert.ok(s.indexOf('attribué à') < s.indexOf('sa manière'), 'ordre canonique respecté');
	assert.match(s, /7 œuvres concernées portent la mention/u);
});

test('Titien — dispersé (36 %, deux premières < 70 %)', () => {
	const s = P(F({ attribue: 4, atelier_de: 3, entourage_de: 2, point_interrogation: 1, suiveur_de: 1 }), 11);
	assert.equal(s, 'Les œuvres concernées se répartissent entre plusieurs mentions, sans qu’une seule s’impose.');
});

test('Cas « deux mentions » — 1re+2e ≥ 70 % et 2e ≥ 20 %', () => {
	const s = P(F({ attribue: 11, ecole_de: 6, atelier_de: 3 }), 20); // 55% + 30% = 85%, 2e = 30%
	assert.match(s, /^11 des 20 œuvres concernées portent la mention «.attribué à.»/u);
	assert.match(s, /; 6 portent la mention «.de son école.»\.$/u);
});

test('Égalité synthétique à trois mentions — pluriel et ordre canonique', () => {
	const s = P(F({ ecole_de: 5, attribue: 5, atelier_de: 5 }), 15);
	assert.match(s, /^À égalité, /u);
	assert.ok(s.indexOf('attribué à') < s.indexOf('son atelier'), 'attribué à en tête');
	assert.ok(s.indexOf('son atelier') < s.indexOf('de son école'), 'atelier avant école');
});

test('Cas « deux » — accord pluriel « portent » sur la seconde mention', () => {
	const s = P(F({ attribue: 8, ecole_de: 4, atelier_de: 2 }), 14); // 57%+29%=86%, 2e=29% → deux
	assert.match(s, /^8 des 14 œuvres concernées portent la mention «.attribué à.»/u);
	assert.match(s, /; 4 portent la mention «.de son école.»\.$/u);
});

test('Total nul — pas de phrase', () => {
	assert.ok(P(F({ attribue: 0 }), 0) == null);
});
