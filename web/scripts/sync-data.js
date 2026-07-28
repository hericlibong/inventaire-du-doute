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
const fichiers = (await readdir(source)).filter((f) => f.endsWith('.json'));
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
