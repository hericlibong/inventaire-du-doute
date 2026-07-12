# Méthode et limites

Embryon de la future page publique. Cette page sera publiée au même rang que le
récit : les limites du projet sont affichées, pas cachées.

## Ce que mesurent les chiffres — et ce qu'ils ne mesurent pas

- **Les chiffres ne reflètent que ce qui a été versé dans Joconde.** Les versements
  sont volontaires et inégaux selon les musées : un musée absent des résultats n'est
  pas un musée sans incertitudes, c'est peut-être un musée qui n'a pas (encore)
  versé ses notices. Aucune comparaison entre musées sur des comptages bruts.
- **Le projet lit des notices, pas des œuvres.** Il restitue ce que les musées ont
  écrit dans leur inventaire public. Il n'authentifie rien et n'émet aucun avis
  d'attribution.
- **La détection est lexicale.** Elle repère des formules écrites, avec un taux de
  faux positifs mesuré sur un échantillon vérifié à la main (voir phase 1). Le
  lexique de détection est versionné et public.

## Méthode de vérification du détecteur (phase 1, T4-T5)

La détection est vérifiée sur un échantillon de 206 notices jugées à la main
par un humain, selon le protocole suivant :

- **Tirage stratifié par famille de marqueur**, reproductible (graine aléatoire
  fixée à 42, code : `src/build_sample.py`). Les familles rares sont
  sur-représentées, les familles minuscules prises en entier — un tirage
  proportionnel n'aurait montré presque que des « attribué à ». Quotas par
  famille : attribué à 30, ? 25, atelier de 25, école de 20, manière de 15,
  entourage de 15, genre de 15, suiveur de 10, présumé 4 (exhaustif),
  d'après 15, copie 10, anciennement attribué 7 (exhaustif),
  champ Ancienne_attribution 15.
- **Une ligne = un marqueur sur une notice** (une notice à deux marqueurs peut
  apparaître deux fois, chaque ligne se juge indépendamment).
- Le vérificateur voit : un **extrait** fabriqué pour la lecture (fenêtre de
  ±40 caractères autour du marqueur détecté, troncature signalée par « … »),
  les **valeurs brutes complètes** des champs concernés (non tronquées), et le
  lien vers la notice publique sur POP. Trois verdicts possibles :
  vrai / faux / incertain, avec commentaire libre.
- **Pondération obligatoire au bilan (T5)** : l'échantillon étant stratifié,
  le taux de faux positifs global ne sera PAS la moyenne brute des 206 lignes.
  Il sera calculé par famille, puis pondéré par le poids réel de chaque famille
  dans la base (sinon les 4 « présumé » pèseraient autant que les
  18 008 « attribué à »).
- **Verdicts « incertain » exclus du calcul des taux** (2 cas sur 206), mais
  conservés et documentés.
- **Résultat du premier cycle (2026-07-04)** : doute 17,0 % de faux positifs
  pondérés, copie 0 %, révision 0 % → reformulation ciblée du lexique
  (calcul : `src/evaluate_sample.py`, détail :
  `data/exports/bilan_faux_positifs.csv`). La règle de jugement appliquée :
  un marqueur ne compte que s'il qualifie l'attribution de l'œuvre de la
  notice — pas s'il apparaît dans une biographie, un nom propre ou à propos
  d'une autre œuvre.

## Les œuvres montrées en exemple (vitrine « Œuvres », 2026-07-11)

Sur chaque fiche de maître, l'onglet « Œuvres » montre quelques cas concrets.
Ces exemples sont **pris automatiquement dans la base, pas choisis à la main** :
pour chaque forme de doute présente autour d'un nom, le pipeline retient la
**première œuvre rencontrée** dans le fichier de référence (deux pour la forme
la plus fréquente), plus une copie « d'après ». Ni tri, ni sélection éditoriale,
ni recherche de la « meilleure » pièce : aucun risque de mise en scène.

Conséquences assumées :
- l'échantillon n'est **ni représentatif ni exhaustif** (jusqu'à 9 œuvres quand
  un maître peut en compter des centaines) — c'est une illustration, jamais un
  comptage ;
- la citation affichée entre guillemets est le **contenu exact du champ auteur**
  de la fiche Joconde (verbatim, capitales et abréviations comprises) ;
- chaque exemple renvoie à sa **fiche publique sur POP** (plateforme ouverte du
  patrimoine) ; cette fiche vit sa vie indépendamment de notre version de
  référence du fichier et peut avoir été mise à jour depuis.

## Source

Jeu de données « Collections des musées de France : base Joconde »,
ministère de la Culture, publié sur data.gouv.fr sous Licence Ouverte 2.0.
Version de référence utilisée : à préciser lors du téléchargement (T1).

*(À enrichir au fil du projet : périmètre retenu, taux de faux positifs mesuré,
choix de classification des formules…)*
