"""Appariement d'une notice Joconde à un item Wikidata / fichier Commons, et
classement des droits du fichier. Logique PURE (testable sans réseau).

Deux décisions strictement séparées (cahier des charges 2026-07-29) :

  match_status  — identifie-t-on la MÊME œuvre ?  exact | a_verifier | rejete
  rights_status — la PHOTO est-elle réutilisable ? open | authorized | restricted | unknown

Une image n'est retenue que si match_status == exact ET rights_status ∈ {open, authorized}.

Règle impérative : une ressemblance de titre, d'auteur, de sujet ou de musée NE
SUFFIT JAMAIS. Une correspondance n'est « exacte » que par identifiant Joconde
(Wikidata P347) explicite. Le numéro d'inventaire + institution concordante
produit un CANDIDAT (`a_verifier`) : le passage à `exact` demande un contrôle
humain (métadonnées compatibles), qu'on ne fait pas en masse à ce palier.
"""

import re
import unicodedata

# match_status
EXACT = "exact"
A_VERIFIER = "a_verifier"
REJETE = "rejete"

# match_method
M_JOCONDE = "joconde_id"
M_INVENTORY = "inventory_number"
M_MANUAL = "manual_review"

# rights_status
OPEN = "open"
AUTHORIZED = "authorized"
RESTRICTED = "restricted"
UNKNOWN = "unknown"


# --------------------------------------------------------------------------
# Normalisations
# --------------------------------------------------------------------------
def _sans_accents(s: str) -> str:
    s = unicodedata.normalize("NFD", s or "")
    return "".join(c for c in s if unicodedata.category(c) != "Mn")


def _mots(s: str) -> set:
    return set(re.findall(r"[a-z0-9]+", _sans_accents(s).lower()))


def normaliser_inventaire(s: str) -> str:
    """« INV 3253 », « Inv. 3253 », « INV3253 » → « INV3253 ». On retire tout ce
    qui n'est pas lettre/chiffre : les graphies POP et Wikidata diffèrent surtout
    par les espaces et la ponctuation."""
    return re.sub(r"[^A-Z0-9]", "", (s or "").upper())


def institution_concorde(musee_joconde: str, label_wikidata: str) -> bool:
    """Le musée Joconde et la collection Wikidata désignent-ils la même
    institution ? Tolère les libellés emboîtés (« département des peintures du
    musée du Louvre » ⊃ « musée du Louvre ») : concordance si l'un contient
    l'autre (mots), ou fort recouvrement de mots signifiants."""
    a, b = _mots(musee_joconde), _mots(label_wikidata)
    petits = {"de", "du", "des", "d", "le", "la", "les", "l", "et", "musee"}
    a2, b2 = a - petits, b - petits
    if not a2 or not b2:
        return False
    if a2 <= b or b2 <= a:      # l'un emboîté dans l'autre
        return True
    inter = a2 & b2
    return len(inter) / min(len(a2), len(b2)) >= 0.6


# --------------------------------------------------------------------------
# Comparaison de métadonnées (preuves, jamais décisives seules)
# --------------------------------------------------------------------------
def parser_dimensions(mesures: str):
    """Extrait (hauteur, largeur) en CENTIMÈTRES du champ Joconde « Mesures »,
    ou (None, None). Formats rencontrés : « 31.5 H ; 17 L », « H. 76.5, L. 102 »,
    « H. en m 0,183 ; L. en m 0,120 », « 99 H ; 82.5 L ». On lit d'abord le nombre
    PLACÉ AVANT la lettre (« 31.5 H »), sinon celui placé APRÈS (« H. 76.5 »)."""
    if not mesures:
        return (None, None)
    s = mesures.replace("\xa0", " ")
    en_metres = bool(re.search(r"en\s*m\b", s.lower()))

    def val(lettre):
        m = re.search(r"(\d+(?:[.,]\d+)?)\s*" + lettre + r"\b", s)   # nombre AVANT
        if not m:
            m = re.search(lettre + r"[.\s]*(?:en\s*m\w*\s*)?(\d+(?:[.,]\d+)?)", s)  # APRÈS
        return float(m.group(1).replace(",", ".")) if m else None

    h, w = val("H"), val("L")
    if h is None or w is None:
        return (None, None)
    # mètres (mention « en m », ou valeurs trop petites pour des centimètres)
    if en_metres or (h < 3.5 and w < 3.5):
        h, w = h * 100, w * 100
    return (round(h, 1), round(w, 1))


def dimensions_concordent(h1, w1, h2, w2):
    """Deux paires de dimensions (cm) désignent-elles le même objet ? Tolérance
    ±5 % (ou ±0,6 cm). Renvoie True/False, ou None si une dimension manque —
    l'empreinte la plus discriminante pour départager les collisions d'inventaire."""
    if None in (h1, w1, h2, w2):
        return None

    def proche(a, b):
        return abs(a - b) <= max(0.6, 0.05 * max(a, b))

    return proche(h1, h2) and proche(w1, w2)


def comparer_metadonnees(meta: dict, cand: dict) -> dict:
    """Renvoie les drapeaux de preuve (booléens) entre une notice Joconde et un
    candidat Wikidata. Purement INDICATIF : sert le contrôle. Les dimensions,
    quand elles concordent, valent confirmation (voir decider_match)."""
    ev = {}
    if meta.get("numero_inventaire") and cand.get("inventaire"):
        ev["inventory_match"] = any(
            normaliser_inventaire(meta["numero_inventaire"]) == normaliser_inventaire(c)
            for c in cand["inventaire"])
    if meta.get("musee") and cand.get("collection"):
        ev["institution_match"] = any(
            institution_concorde(meta["musee"], c) for c in cand["collection"])
    if meta.get("titre") and cand.get("titre"):
        a, b = _mots(meta["titre"]), _mots(cand["titre"])
        ev["title_match"] = bool(a & b) and len(a & b) / min(len(a), len(b)) >= 0.5
    if meta.get("auteur") and cand.get("auteur"):
        # le nom de famille du maître apparaît-il des deux côtés ? (indicatif :
        # jamais un motif de REJET — la divergence d'attribution est le sujet)
        ev["author_match"] = bool(_mots(meta["auteur"]) & _mots(cand["auteur"]))
    # Dimensions : empreinte discriminante.
    hc, wc = parser_dimensions(meta.get("dimensions", ""))
    conc = dimensions_concordent(hc, wc, cand.get("h"), cand.get("w"))
    if conc is True:
        ev["dimensions_match"] = True
    elif conc is False:
        ev["dimensions_conflit"] = True
    return ev


# --------------------------------------------------------------------------
# Décision d'appariement
# --------------------------------------------------------------------------
def decider_match(reference: str, meta: dict, cand: dict) -> tuple:
    """(match_status, match_method, match_evidence).

    - identifiant Joconde (P347) explicite → EXACT ;
    - numéro d'inventaire exact + institution concordante → A_VERIFIER (candidat) ;
    - le reste (titre/auteur/musée seuls) → REJETE : jamais validé automatiquement.
    """
    ev = comparer_metadonnees(meta, cand)

    # 1. Identifiant Joconde explicite : la seule preuve suffisante à elle seule.
    if reference and reference in (cand.get("joconde_ids") or []):
        ev["joconde_id_match"] = True
        return (EXACT, M_JOCONDE, ev)

    # 2. Numéro d'inventaire exact + institution concordante.
    if ev.get("inventory_match") and ev.get("institution_match"):
        # Dimensions présentes mais incompatibles → objet différent (collision) :
        # les numéros d'inventaire se répètent entre musées homonymes (« musée des
        # Beaux-Arts »). REJETÉ.
        if ev.get("dimensions_conflit"):
            return (REJETE, M_INVENTORY, ev)
        # Sinon : CANDIDAT à vérifier. On ne promeut JAMAIS en exact
        # automatiquement — même des dimensions concordantes peuvent coïncider
        # entre deux objets d'un même numéro (« L'Ange gardien » 102×81 vs « Nu »
        # 102×82). Le cahier des charges exige un contrôle humain (« après
        # contrôle »). L'évidence (dimensions, titre) sert à trier, pas à trancher.
        return (A_VERIFIER, M_INVENTORY, ev)

    # 3. Inventaire identique mais AUTRE institution : faux rapprochement. Les
    # numéros d'inventaire (« INV 3253 », « 1 », « D 1 ») se répètent d'un musée
    # à l'autre ; sans institution concordante, c'est un autre objet → REJETE.
    if ev.get("inventory_match"):
        return (REJETE, M_INVENTORY, ev)

    # 4. Titre / auteur / musée seuls : NE SUFFIT JAMAIS.
    return (REJETE, M_MANUAL, ev)


# --------------------------------------------------------------------------
# Droits du fichier Commons
# --------------------------------------------------------------------------
def classer_droits_commons(license_short: str, license_code: str = "") -> tuple:
    """(rights_status, licence_normalisee) à partir des métadonnées Commons
    (extmetadata : LicenseShortName et code License). Ouvert = domaine public /
    PDM / CC0 / CC BY / CC BY-SA (toutes versions). NC/ND restent à examiner
    (jamais ouverts). Un crédit photo n'est pas une licence."""
    court = (license_short or "").strip()
    code = (license_code or "").strip().lower()
    n = _sans_accents(f"{court} {code}").lower()

    # Variantes restreintes : à ne jamais reconnaître comme ouvertes.
    if "cc" in n and ("-nc" in n or " nc" in n or "-nd" in n or " nd" in n):
        return (UNKNOWN, court or code.upper())

    # Domaine public / marques équivalentes.
    if any(t in n for t in ["public domain", "domaine public", "pdm",
                            "pd-", "pd ", "cc-pd", "cc pd"]) or code in ("pd", "cc-pd-mark"):
        return (OPEN, court or "Domaine public")
    if re.search(r"\bcc0\b", n) or code == "cc0":
        return (OPEN, "CC0")
    if "cc-by-sa" in n or "cc by-sa" in n:
        return (OPEN, court or "CC BY-SA")
    if "cc-by" in n or "cc by" in n:
        return (OPEN, court or "CC BY")
    if "no restrictions" in n:
        return (OPEN, court or "No restrictions")

    # Fichier présent mais licence non reconnue / crédit seul.
    return (UNKNOWN, court)


def retenable(match_status: str, rights_status: str) -> bool:
    """Une image n'est retenue que si l'œuvre est identifiée avec certitude ET la
    photo est réutilisable."""
    return match_status == EXACT and rights_status in (OPEN, AUTHORIZED)
