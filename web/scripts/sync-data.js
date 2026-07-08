// Copie les JSON exportés par le pipeline Python vers static/data/,
// où le front statique peut les servir (fetch("/data/xxx.json")).
//
// Les JSON sont des artefacts générés (src/build_*.py) : ils ne sont pas
// versionnés côté front (voir web/.gitignore). On les resynchronise avec ce
// script après chaque nouvel export. Lancer : `npm run sync:data`.

import { cp, mkdir, readdir } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const ici = dirname(fileURLToPath(import.meta.url));
const source = join(ici, '..', '..', 'data', 'exports', 'web');
const cible = join(ici, '..', 'static', 'data');

await mkdir(cible, { recursive: true });

const fichiers = (await readdir(source)).filter((f) => f.endsWith('.json'));
for (const fichier of fichiers) {
	await cp(join(source, fichier), join(cible, fichier));
	console.log(`synchronisé : ${fichier}`);
}

console.log(`\n${fichiers.length} fichier(s) copié(s) vers static/data/`);
