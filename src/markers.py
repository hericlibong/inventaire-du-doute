"""Lexique des marqueurs d'incertitude sur l'auteur — version 1 (2026-07-04).

Chaque « famille » regroupe une formule d'attribution (décret Marcus, méthode
Joconde) et ses variantes de graphie. C'est un lexique versionné : toute
modification passe par ce fichier et se voit dans l'historique git.

Quatre catégories :
- « doute »    : incertitude sur l'auteur (le cœur du sujet) ;
- « copie »    : copie assumée d'après un modèle — PAS un doute, classé à part ;
- « revision » : attribution ancienne, révisée depuis ;
- « ecarte »   : détecté mais écarté par défaut, compté séparément pour contrôle.

Doctrine issue de la vérification manuelle T4 (206 notices jugées par
l'utilisateur, voir docs/decisions.md) : un marqueur ne compte que s'il
qualifie l'attribution de l'œuvre de la notice — pas s'il apparaît dans une
biographie, dans un nom propre (atelier de production, studio d'imprimeur),
ou à propos d'une autre œuvre citée.

Corrections v1 (suite au bilan T5 — doute : 17 % de faux positifs pondérés) :
1. « atelier de » (64 % de faux en v0) : on lit désormais la CONVENTION et non
   le mot — le doute Joconde s'écrit en qualificatif entre parenthèses après
   un nom (« COROT (atelier) »), tandis que « Atelier de Pistillus » en nom
   d'auteur désigne l'atelier comme créateur assumé. Détection sur mesure,
   segment par segment ; la forme « nom d'auteur » part en catégorie
   « ecarte » pour être chiffrée et contrôlée.
2. « école de » (20 %) : exclusion de la forme inversée d'école nationale
   « Hollande École de (École hollandaise) » — signal : « école de » suivi
   d'une parenthèse.
3. « ? » (16 %) : la parenthèse ne doit contenir AUCUN chiffre — « (?-1996) »
   (date de naissance inconnue) ne compte plus, en plus du « (19..-19..?) »
   déjà exclu en v0.
4. Doctrine « (attribué, d'après) » : quand les deux qualificatifs coexistent
   dans la même parenthèse, « d'après » l'emporte — la notice est une copie,
   elle sort de « attribué à ».

Pièges v0 conservés : « ? » cherché uniquement dans Auteur (ailleurs = dates) ;
« école française » sans « de » jamais compté ; Ancienne_attribution jamais
fouillé au texte (sa présence est le marqueur) ; apostrophes droites et
typographiques, accents parfois absents.
"""

import re
from dataclasses import dataclass
from typing import Callable, Optional

import pandas as pd

# Champs texte fouillés par défaut (hors Ancienne_attribution, voir plus haut).
CHAMPS_TEXTE = ("Auteur", "Precisions_sur_l_auteur")

# Rôles de production : « (atelier, graveur) » désigne un atelier-entreprise
# (studio, imprimeur), pas un doute sur un maître (verdicts utilisateur T4).
ROLES_PRODUCTION = (
    "graveur", "imprimeur", "éditeur", "editeur", "photographe",
    "fabricant", "céramiste", "ceramiste", "potier", "lithographe",
)

_RE_PARENTHESES = re.compile(r"\(([^)]*)\)")
_RE_QUALIF_ATELIER = re.compile(r"\bateliers?\s*(?:,|$)")
_RE_NOM_ATELIER = re.compile(r"^ateliers?\s+(?:de\s|du\s|des\s|d['’])", re.IGNORECASE)


def _atelier_doute(valeur: object) -> bool:
    """« atelier » en qualificatif de doute, segment par segment.

    Vrai si un segment du champ Auteur (séparateur ;) porte une parenthèse
    de qualificatifs contenant le token « atelier », ET que le nom qualifié
    n'est pas lui-même un atelier (« ATELIER DE LYON (atelier) »), ET que le
    qualificatif n'accompagne pas un rôle de production.
    """
    if not isinstance(valeur, str):
        return False
    for segment in valeur.split(";"):
        segment = segment.strip()
        if _RE_NOM_ATELIER.match(segment):
            continue  # le nom EST un atelier → créateur assumé, pas un doute
        for qualif in _RE_PARENTHESES.findall(segment):
            qualif = qualif.lower().strip()
            if not _RE_QUALIF_ATELIER.search(qualif):
                continue
            if any(role in qualif for role in ROLES_PRODUCTION):
                continue
            return True
    return False


def _atelier_nom(valeur: object) -> bool:
    """« Atelier de X » comme nom d'auteur (catégorie « ecarte »)."""
    if not isinstance(valeur, str):
        return False
    return any(_RE_NOM_ATELIER.match(s.strip()) for s in valeur.split(";"))


@dataclass(frozen=True)
class Famille:
    code: str
    libelle: str
    categorie: str  # doute | copie | revision | ecarte
    motif: str  # regex, compilée insensible à la casse
    champs: tuple = CHAMPS_TEXTE
    suspect: bool = False  # True = faux positifs attendus, à surveiller
    exclusion: str = ""  # regex : si elle matche aussi, la détection tombe
    fonction: Optional[Callable] = None  # détection sur mesure (remplace motif)


FAMILLES = [
    Famille(
        "attribue", "attribué à", "doute",
        # « attribué », « attribuée », « attr. » — mais pas « anciennement attribué »
        r"(?<!anciennement )attribu[ée]|\battr\.",
        # doctrine T4 : « (attribué, d'après) » dans la même parenthèse = copie
        exclusion=r"\([^)]*attribu[ée][^)]*d['’]apr[èe]s[^)]*\)|\([^)]*d['’]apr[èe]s[^)]*attribu[ée][^)]*\)",
    ),
    Famille(
        "point_interrogation", "? (point d'interrogation)", "doute",
        # parenthèse contenant un ? et AUCUN chiffre : « (?) », « (attribué, ?) »
        # — « (19..-19..?) » et « (?-1996) » sont des dates inconnues
        r"\([^)\d]*\?[^)\d]*\)",
        champs=("Auteur",),
    ),
    Famille(
        "ecole_de", "école de", "doute",
        # « école de X » (jamais « école française », le « de » est obligatoire,
        # ni « École de (École hollandaise) », forme inversée de nationalité)
        # ou qualificatif « (école) » en fin de token
        r"[ée]coles?\s+(?:de\s+(?!\()|du\s|des\s|d['’])|\([^)]*\b[ée]coles?\s*[,)]",
        champs=("Auteur", "Ecole_pays"),
    ),
    Famille(
        "atelier_de", "atelier (qualificatif de doute)", "doute",
        motif="", champs=("Auteur",), fonction=_atelier_doute,
    ),
    Famille(
        "atelier_nom", "Atelier de X en nom d'auteur (écarté)", "ecarte",
        motif="", champs=("Auteur",), fonction=_atelier_nom,
        suspect=True,  # écarté par défaut ; mini-contrôle T4bis pour valider
    ),
    Famille("entourage_de", "entourage de", "doute", r"\bentourage\b"),
    Famille("suiveur_de", "suiveur de", "doute", r"\bsuiveurs?\b"),
    Famille(
        "maniere_de", "(à la) manière de", "doute",
        r"mani[èe]res?\s+d[e'’]",
    ),
    Famille("genre_de", "genre de", "doute", r"\bgenre\s+de\b"),
    Famille(
        "presume", "présumé", "doute",
        r"pr[ée]sum[ée]",
        suspect=True,  # peut viser une autre œuvre citée en biographie (T4)
    ),
    Famille(
        "d_apres", "d'après (copie d'un modèle)", "copie",
        r"d['’]apr[èe]s",
    ),
    Famille("copie", "copie", "copie", r"\bcopies?\b", suspect=True),
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
_EXCLUSIONS = {
    f.code: re.compile(f.exclusion, re.IGNORECASE) for f in FAMILLES if f.exclusion
}


def detections(morceau: pd.DataFrame) -> pd.DataFrame:
    """Applique le lexique à un morceau du CSV.

    Renvoie un DataFrame de booléens aligné sur `morceau` : une colonne par
    code de famille, True si la notice porte le marqueur dans au moins un
    des champs de la famille.
    """
    resultat = pd.DataFrame(index=morceau.index)
    for famille in FAMILLES:
        colonnes = []
        for champ in famille.champs:
            serie = morceau[champ]
            if famille.fonction:
                colonne = serie.map(famille.fonction)
            elif famille.motif:
                colonne = serie.str.contains(_COMPILES[famille.code], na=False)
                if famille.exclusion:
                    colonne &= ~serie.str.contains(
                        _EXCLUSIONS[famille.code], na=False
                    )
            else:
                # Famille « présence de champ » (Ancienne_attribution)
                colonne = serie.notna()
            colonnes.append(colonne)
        resultat[famille.code] = pd.concat(colonnes, axis=1).any(axis=1)
    return resultat
