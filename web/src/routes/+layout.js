// Site entièrement pré-rendu : aucun serveur applicatif, l'adapter statique
// génère du HTML pour chaque route. Réglage fait une fois, ici à la racine.
export const prerender = true;

// GitHub Pages sert des fichiers statiques : pour qu'un accès direct à
// `/inventaire-du-doute/artistes/` fonctionne, il faut un dossier `artistes/`
// contenant un `index.html`. C'est ce que produit `trailingSlash: 'always'` ;
// sans lui, l'adaptateur écrit `artistes.html`, que GitHub Pages ne sert pas
// sous l'URL sans extension (2026-08-10).
export const trailingSlash = 'always';
