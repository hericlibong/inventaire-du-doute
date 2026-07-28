// Tests de la fenêtre de pagination compacte (onglet Œuvres).
// Exécution : node --test  (Node 22, runner natif ; aucune dépendance).
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { fenetrePagination } from '../src/lib/pagination.js';

test('une seule page : uniquement la page 1', () => {
	assert.deepEqual(fenetrePagination(1, 1), [1]);
	assert.deepEqual(fenetrePagination(1, 0), [1]);
});

test('peu de pages : toutes affichées, aucune ellipse', () => {
	assert.deepEqual(fenetrePagination(1, 2), [1, 2]);
	assert.deepEqual(fenetrePagination(3, 5), [1, 2, 3, 4, 5]);
});

test('début de liste : ellipse seulement du côté de la fin', () => {
	assert.deepEqual(fenetrePagination(1, 39), [1, 2, '…', 39]);
	assert.deepEqual(fenetrePagination(3, 39), [1, 2, 3, 4, '…', 39]);
});

test('milieu de liste : ellipse des deux côtés', () => {
	assert.deepEqual(fenetrePagination(20, 39), [1, '…', 19, 20, 21, '…', 39]);
});

test('fin de liste : ellipse seulement du côté du début', () => {
	assert.deepEqual(fenetrePagination(39, 39), [1, '…', 38, 39]);
	assert.deepEqual(fenetrePagination(37, 39), [1, '…', 36, 37, 38, 39]);
});

test('un seul numéro manquant : montré au lieu d’une ellipse', () => {
	// page 4 sur 6 : le trou entre 1 et 3 vaut un seul numéro (2) → pas d'ellipse
	assert.deepEqual(fenetrePagination(4, 6), [1, 2, 3, 4, 5, 6]);
	// page 3 sur 6 : trou d'un seul numéro (5) côté fin → on montre 5
	assert.deepEqual(fenetrePagination(3, 6), [1, 2, 3, 4, 5, 6]);
});

test('la première et la dernière page sont toujours présentes', () => {
	for (const page of [1, 5, 12, 25, 38]) {
		const f = fenetrePagination(page, 38);
		assert.equal(f[0], 1, `page 1 absente pour active=${page}`);
		assert.equal(f.at(-1), 38, `dernière page absente pour active=${page}`);
	}
});

test('la page active et ses voisines figurent dans la fenêtre', () => {
	const page = 15;
	const f = fenetrePagination(page, 40);
	for (const p of [page - 1, page, page + 1]) {
		assert.ok(f.includes(p), `voisine ${p} manquante`);
	}
});
