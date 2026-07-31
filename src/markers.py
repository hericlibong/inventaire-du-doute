"""Lexique des marqueurs d'incertitude sur l'auteur — version 2 (2026-07-05).

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

Arbitrages v2 (typologie P2-T2, décisions utilisateur du 2026-07-05) :
1. « atelier » est restreint aux domaines beaux-arts : le contrôle T4bis a
   montré que les faux (ateliers-entreprises) vivent en ethnologie/artisanat.
   Hors beaux-arts, la détection bascule dans la famille écartée
   « atelier_hors_beaux_arts » (chiffrée, pas supprimée). Cette règle exige
   la colonne Domaine dans les données passées à detections().
2. Écoles-lieux consacrées (Fontainebleau, Paris, Barbizon, Pont-Aven,
   Nancy) : noms de mouvements, pas le sillage d'un maître — liste
   d'exclusion versionnée ci-dessous, bascule en famille écartée
   « ecole_lieu ».
3. Le « ? » reste au niveau 1 de la typologie (identification fragile).

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

# Domaines beaux-arts : périmètre de validité de la famille « atelier » (v2).
BEAUX_ARTS = frozenset({
    "peinture", "dessin", "sculpture", "estampe", "beaux-arts",
    "arts graphiques", "miniature", "pastel",
})

# Écoles-lieux consacrées : mouvements artistiques, pas le sillage d'un
# maître (arbitrage utilisateur 2026-07-05). Liste courte, amendable.
MOTIF_ECOLE_LIEU = (
    r"[ée]coles?\s+de\s+(?:fontainebleau|paris|barbizon|pont[- ]aven|nancy)"
)

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


# Version du lexique, affichée sur la page « Méthode » du site : une seule
# source, ici, pour qu'un lexique v3 ne laisse pas « v2 » publié en ligne.
VERSION = "v2 (2026-07-05)"


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
        exclusion=MOTIF_ECOLE_LIEU,  # écoles-lieux consacrées → ecole_lieu
    ),
    Famille(
        "ecole_lieu", "école-lieu consacrée (écartée)", "ecarte",
        MOTIF_ECOLE_LIEU,
        champs=("Auteur", "Ecole_pays"),
    ),
    Famille(
        "atelier_de", "atelier (qualificatif, beaux-arts)", "doute",
        # restreint aux domaines beaux-arts en post-traitement (detections)
        motif="", champs=("Auteur",), fonction=_atelier_doute,
    ),
    Famille(
        "atelier_hors_beaux_arts", "atelier hors beaux-arts (écarté)", "ecarte",
        # alimentée par le post-traitement de detections(), jamais directement
        motif="", champs=("Auteur",), fonction=lambda v: False,
    ),
    Famille(
        "atelier_nom", "Atelier de X en nom d'auteur (écarté)", "ecarte",
        motif="", champs=("Auteur",), fonction=_atelier_nom,
        suspect=True,  # écarté par défaut ; contrôle T4bis : confirmé 15/15
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


def _dans_beaux_arts(domaine: object) -> bool:
    """La notice a-t-elle au moins un domaine beaux-arts ? (champ multivalué ;)"""
    if not isinstance(domaine, str):
        return False
    return any(d.strip().lower() in BEAUX_ARTS for d in domaine.split(";"))


def detections(morceau: pd.DataFrame) -> pd.DataFrame:
    """Applique le lexique à un morceau du CSV.

    Renvoie un DataFrame de booléens aligné sur `morceau` : une colonne par
    code de famille, True si la notice porte le marqueur dans au moins un
    des champs de la famille.

    Exige la colonne « Domaine » (restriction beaux-arts de « atelier », v2).
    """
    if "Domaine" not in morceau.columns:
        raise ValueError(
            "detections() exige la colonne Domaine "
            "(restriction beaux-arts de la famille atelier, lexique v2)"
        )
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

    # Post-traitement v2 : « atelier » n'est un doute qu'en beaux-arts ;
    # ailleurs, la détection bascule dans la famille écartée dédiée.
    beaux_arts = morceau["Domaine"].map(_dans_beaux_arts)
    resultat["atelier_hors_beaux_arts"] = resultat["atelier_de"] & ~beaux_arts
    resultat["atelier_de"] &= beaux_arts
    return resultat


# Familles de doute, ordonnées du niveau le plus léger au plus détaché
# (échelle typologie P2-T2) : sert à choisir UNE famille quand un segment en
# porterait plusieurs (co-occurrences quasi nulles, voir P2-T1).
DOUTE_PAR_NIVEAU = (
    "attribue", "point_interrogation", "presume",       # niveau 1
    "ecole_de", "atelier_de", "entourage_de", "suiveur_de",  # niveau 2
    "maniere_de", "genre_de",                            # niveau 3
)


def famille_segment(segment: str, en_beaux_arts: bool = True):
    """Catégorise UN segment du champ Auteur, rattaché à un seul auteur.

    Sert aux agrégats PAR AUTEUR (src/build_artistes.py) : « quel lien cette
    notice affirme-t-elle avec ce nom ? ». Réutilise exactement les motifs de
    detections() pour ne pas diverger du lexique. Renvoie (categorie, code) où
    categorie ∈ {copie, ecarte, doute, propre} et code est la famille retenue
    (None pour propre).

    Ordre de résolution (doctrine T4/v2) : la copie l'emporte ; puis les
    familles écartées ; puis le doute (famille la plus légère si plusieurs) ;
    sinon propre. « atelier » ne vaut doute qu'en beaux-arts (v2). Le doute est
    cherché dans TOUT le segment, parenthèses ou non (docs/donnees.md, 2026-07-07).
    """
    if _COMPILES["d_apres"].search(segment):
        return "copie", "d_apres"
    if _COMPILES["copie"].search(segment):
        return "copie", "copie"
    if _atelier_nom(segment):
        return "ecarte", "atelier_nom"
    if re.search(MOTIF_ECOLE_LIEU, segment, re.IGNORECASE):
        return "ecarte", "ecole_lieu"
    for code in DOUTE_PAR_NIVEAU:
        if code == "atelier_de":
            if _atelier_doute(segment):
                return ("doute", "atelier_de") if en_beaux_arts \
                    else ("ecarte", "atelier_hors_beaux_arts")
        elif _COMPILES[code].search(segment):
            return "doute", code
    return "propre", None
