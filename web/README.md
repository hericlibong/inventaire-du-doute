# Frontend de L'inventaire du doute

Ce dossier contient le site statique SvelteKit de
[L'inventaire du doute](../README.md).

Les données servies par l'interface sont générées par le pipeline Python puis versionnées
dans `../data/exports/web/`. Avant un lancement local ou un build, elles sont copiées vers
`static/data/` avec `npm run sync:data`.

## Développement

```bash
npm ci
npm run sync:data
npm run dev
```

## Vérification

```bash
node --test tests/*.test.js
npm run build
```

Le déploiement GitHub Pages utilise le même build avec
`BASE_PATH=/inventaire-du-doute`. La procédure complète, l'architecture, les chiffres et
les licences sont documentés dans le [README principal](../README.md).
