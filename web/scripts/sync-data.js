// Copie les JSON exportés par le pipeline Python vers static/data/,
// où le front statique peut les servir (fetch("/data/xxx.json")).
//
// Les JSON sont des artefacts générés (src/build_*.py) : ils ne sont pas
// versionnés côté front (voir web/.gitignore). On les resynchronise avec ce
// script après chaque nouvel export. Lancer : `npm run sync:data`.

import { cp, mkdir, readdir, rm } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const ici = dirname(fileURLToPath(import.meta.url));
const source = join(ici, '..', '..', 'data', 'exports', 'web');
const cible = join(ici, '..', 'static', 'data');

await mkdir(cible, { recursive: true });

// JSON à plat (artistes.json, musees.json…).
// `revisions.json` alimentait la rubrique « Avant / après », retirée de la
// production le 2026-08-09 (F5) : elle appartient à un volet ultérieur. L'export
// reste produit et versionné dans data/exports/web/ ; il n'est simplement plus
// servi par le site, sans quoi la donnée d'une page non publiée resterait
// accessible en ligne.
const HORS_PRODUCTION = new Set(['revisions.json']);

const fichiers = (await readdir(source)).filter(
	(f) => f.endsWith('.json') && !HORS_PRODUCTION.has(f)
);
for (const fichier of fichiers) {
	await cp(join(source, fichier), join(cible, fichier));
	console.log(`synchronisé : ${fichier}`);
}

// Sous-dossier oeuvres/ : un fichier par maître, chargé à la demande par l'onglet
// « Œuvres » (2026-07-28). On repart d'un dossier propre pour ne pas garder le
// fichier d'un maître retiré, puis on copie l'ensemble.
const sourceOeuvres = join(source, 'oeuvres');
const cibleOeuvres = join(cible, 'oeuvres');
await rm(cibleOeuvres, { recursive: true, force: true });
await cp(sourceOeuvres, cibleOeuvres, { recursive: true });
const nbOeuvres = (await readdir(sourceOeuvres)).filter((f) => f.endsWith('.json')).length;
console.log(`synchronisé : oeuvres/ (${nbOeuvres} fichiers)`);

console.log(`\n${fichiers.length + nbOeuvres} fichier(s) copié(s) vers static/data/`);

// Vignettes des reproductions ouvertes (chantier images, 2026-07-29) : copiées
// hors de data/ (ce ne sont pas des données), vers static/oeuvres/, servies en
// /oeuvres/<reference>.jpg. Absent tant que build_vignettes.py n'a pas tourné.
const sourceImg = join(ici, '..', '..', 'data', 'exports', 'web', 'oeuvres_img');
try {
	const cibleImg = join(ici, '..', 'static', 'oeuvres');
	await rm(cibleImg, { recursive: true, force: true });
	await cp(sourceImg, cibleImg, { recursive: true });
	const nbImg = (await readdir(sourceImg)).filter((f) => f.endsWith('.jpg')).length;
	console.log(`synchronisé : oeuvres/ images (${nbImg} vignettes) vers static/oeuvres/`);
} catch {
	console.log('(pas de vignettes à synchroniser)');
}
