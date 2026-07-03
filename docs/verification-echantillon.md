# Vérification manuelle de l'échantillon (T4) — mode d'emploi

Fichier à vérifier : `data/exports/echantillon_verification.csv`
(206 lignes, tirage reproductible, graine 42).

## Principe

Chaque ligne = **un marqueur détecté sur une notice**. La question à laquelle tu
réponds, ligne par ligne :

> **Le marqueur détecté exprime-t-il bien ce que sa famille prétend ?**

- famille de catégorie « doute » → est-ce vraiment un doute sur l'**auteur** ?
- « d'après » / « copie » → est-ce vraiment une copie d'après un modèle ?
- « ancienne attribution » → est-ce vraiment une attribution révisée ?

Une notice peut apparaître deux fois (deux marqueurs) : c'est normal, chaque
ligne se juge indépendamment.

## Comment faire

1. Ouvrir le CSV dans LibreOffice/Excel (encodage UTF-8, séparateur virgule).
2. Lire l'`extrait` (le texte autour du marqueur) et les colonnes de contexte
   (`auteur`, `precisions_auteur`, `titre`…). En cas d'hésitation, le `lien_pop`
   ouvre la notice complète sur le site du ministère.
3. Remplir `verdict` avec une de ces trois valeurs :
   - `vrai` — le marqueur dit bien ce que sa famille prétend ;
   - `faux` — c'est autre chose (date inconnue, nom d'atelier de production,
     tournure de phrase, doute sur le sujet et non l'auteur…) ;
   - `incertain` — impossible de trancher (le noter, c'est une info aussi).
4. `commentaire` : libre, surtout pour les `faux` (dire *pourquoi* c'est faux —
   c'est ce qui permettra d'améliorer le lexique en T5).
5. Enregistrer **au même format CSV, même emplacement** (ou en copie
   `echantillon_verification_annote.csv` dans le même dossier).

## Points d'attention connus (à l'affût)

- « atelier de » : `ATELIER DE MOULAGE`, `ATELIER DE ROME` sont des noms
  d'ateliers de production, pas un doute sur un maître → `faux`.
- « genre de » et « copie » en texte libre : tournures banales possibles.
- « école de » suivi d'un lieu (`école de Paris` ?) : à juger au cas par cas.

Pas de contrainte de rythme : T5 (le bilan) démarre quand le fichier annoté
est prêt.
