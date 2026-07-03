"""Lexique des marqueurs d'incertitude sur l'auteur (T3) — le cœur du projet.

Chaque « famille » regroupe une formule d'attribution (décret Marcus, méthode
Joconde) et ses variantes de graphie, sous forme d'une expression régulière
insensible à la casse. C'est un lexique versionné : toute modification passe
par ce fichier et se voit dans l'historique git.

Trois catégories :
- « doute »    : incertitude sur l'auteur (le cœur du sujet) ;
- « copie »    : copie assumée d'après un modèle — PAS un doute, classé à part ;
- « revision » : attribution ancienne, révisée depuis.

Pièges intégrés (voir docs/donnees.md) :
- le « ? » n'est cherché que dans Auteur, entre parenthèses (convention
  Joconde) — ailleurs il peut marquer une date inconnue (« ?, 1467 ») ;
- « école de [artiste] » exige un « de/du/des/d' » : « école française »
  (nationalité, champ Ecole_pays) ne matche pas ;
- « présumé » est marqué suspect : il porte souvent sur le sujet représenté ;
- le champ Ancienne_attribution n'est pas fouillé au texte (son contenu —
  « Attribué à Moderno. » — gonflerait la famille « attribué à ») : c'est sa
  simple présence qui fait marqueur, en famille dédiée ;
- apostrophes droites et typographiques (d'après / d’après), accents parfois
  absents (ecole, presume) : les motifs acceptent les deux.
"""

import re
from dataclasses import dataclass, field

import pandas as pd

# Champs texte fouillés par défaut (hors Ancienne_attribution, voir plus haut).
CHAMPS_TEXTE = ("Auteur", "Precisions_sur_l_auteur")


@dataclass(frozen=True)
class Famille:
    code: str
    libelle: str
    categorie: str  # doute | copie | revision
    motif: str  # regex, compilée insensible à la casse
    champs: tuple = CHAMPS_TEXTE
    suspect: bool = False  # True = faux positifs attendus, à surveiller en T4


FAMILLES = [
    Famille(
        "attribue", "attribué à", "doute",
        # « attribué », « attribuée », « attr. » — mais pas « anciennement attribué »
        r"(?<!anciennement )attribu[ée]|\battr\.",
    ),
    Famille(
        "point_interrogation", "? (point d'interrogation)", "doute",
        # uniquement entre parenthèses dans Auteur : « (?) », « (attribué, ?) » —
        # et sans chiffre avant le ? : « (19..-19..?) » est une date inconnue
        r"\([^)\d]*\?",
        champs=("Auteur",),
    ),
    Famille(
        "ecole_de", "école de", "doute",
        # « école de X » (le « de » est obligatoire : « école française » ne
        # matche pas) ou qualificatif « (école) » — champs Auteur et Ecole_pays
        # seulement : dans Precisions_sur_l_auteur, les biographies citent sans
        # cesse « l'école des Beaux-Arts » (faux positifs massifs)
        r"[ée]coles?\s+(?:de\s|du\s|des\s|d['’])|\([^)]*\b[ée]coles?\b",
        champs=("Auteur", "Ecole_pays"),
    ),
    Famille(
        "atelier_de", "atelier de", "doute",
        # « atelier de X » ou qualificatif « (atelier) » dans Auteur
        r"ateliers?\s+(?:de\s|du\s|des\s|d['’])|\(ateliers?\b",
    ),
    Famille("entourage_de", "entourage de", "doute", r"\bentourage\b"),
    Famille("suiveur_de", "suiveur de", "doute", r"\bsuiveurs?\b"),
    Famille(
        "maniere_de", "(à la) manière de", "doute",
        r"mani[èe]res?\s+d[e'’]",
    ),
    Famille(
        "genre_de", "genre de", "doute",
        r"\bgenre\s+de\b",
        suspect=True,  # « genre de » peut être une tournure banale en texte libre
    ),
    Famille(
        "presume", "présumé", "doute",
        r"pr[ée]sum[ée]",
        suspect=True,  # porte souvent sur le sujet (« portrait présumé de X »)
    ),
    Famille(
        "d_apres", "d'après (copie d'un modèle)", "copie",
        r"d['’]apr[èe]s",
    ),
    Famille(
        "copie", "copie", "copie",
        r"\bcopies?\b",
        suspect=True,  # texte libre : « copie d'inventaire », etc.
    ),
    Famille(
        "anciennement_attribue", "anciennement attribué à", "revision",
        r"anciennement\s+attribu[ée]",
    ),
    # Famille particulière : la simple présence du champ dédié ATTR.
    Famille(
        "champ_ancienne_attribution", "champ Ancienne_attribution renseigné",
        "revision", motif="", champs=("Ancienne_attribution",),
    ),
]

_COMPILES = {
    f.code: re.compile(f.motif, re.IGNORECASE) for f in FAMILLES if f.motif
}


def detections(morceau: pd.DataFrame) -> pd.DataFrame:
    """Applique le lexique à un morceau du CSV.

    Renvoie un DataFrame de booléens aligné sur `morceau` : une colonne par
    code de famille, True si la notice porte le marqueur dans au moins un
    des champs de la famille.
    """
    resultat = pd.DataFrame(index=morceau.index)
    for famille in FAMILLES:
        if famille.motif:
            colonnes = [
                morceau[champ].str.contains(_COMPILES[famille.code], na=False)
                for champ in famille.champs
            ]
            resultat[famille.code] = pd.concat(colonnes, axis=1).any(axis=1)
        else:
            # Famille « présence de champ » (Ancienne_attribution)
            resultat[famille.code] = morceau[famille.champs[0]].notna()
    return resultat
