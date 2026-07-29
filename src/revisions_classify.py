"""Classification d'une révision « avant / après » (rubrique P3-T2).

Séparé de build_revisions.py pour être testable unitairement (tests/test_revisions.py
figera les verdicts humains du 2026-07-14). Analyse les DEUX côtés :

- côté « avant » (Ancienne_attribution) : combien d'hypothèses distinctes, et de
  quelle nature (nom de personne, école/nationalité, anonyme, copie « d'après »,
  note de prose) ;
- côté « aujourd'hui » (Auteur) : via le lexique markers.py (famille_segment).

Catégories publiques produites (couche de libellé obligatoire, CLAUDE.md) —
voir LIBELLE_CATEGORIE. Le détail des choix : docs/decisions.md 2026-07-14 (bis).
"""

import re
import unicodedata

import markers

# ---- Libellés publics des catégories (jamais le code interne dans l'UI) ----
LIBELLE_CATEGORIE = {
    "autre_nom": "Un nom en remplace un autre",
    "meme_nom": "Le nom demeure, avec réserve",
    "anonyme": "Le nom n'est plus retenu",
    "copie": "L'œuvre est reclassée comme copie",
    "deja_copie": "L'ancienne attribution était déjà une copie",
    "plusieurs_noms": "Plusieurs noms se succèdent",
    "mineur": "Cas particuliers",
}
# Catégories montrables comme cartes « avant / après » dans la galerie V1.
CATEGORIES_GALERIE = frozenset({"autre_nom", "meme_nom", "anonyme", "copie"})

_RE_PAR = markers._RE_PARENTHESES
_RE_PREFIXE = re.compile(
    r"^\s*(?:anciennes?\s+attributions?"
    r"|(?:anciennement\s+)?attribu[ée]e?(?:\s+à)?|attr\.)\s*[:,]?\s*",
    re.IGNORECASE)
# Marqueurs de rôle/doute EN TÊTE de segment : on les retire pour isoler le nom
# de personne, mais on garde l'information (école, copie…) via des drapeaux.
_RE_ROLE = re.compile(
    r"^\s*(?:copie\s+d['’]apr[eè]s|d['’]apr[eè]s|[ée]coles?\s+de|genre\s+de"
    r"|mani[èe]re\s+de|entourage\s+de|suiveur\s+de)\s*[:,]?\s*",
    re.IGNORECASE)
# Le segment est une NOTE de prose (réattribution commentée), pas un nom.
_RE_PROSE = re.compile(
    r"changement\s+d['’]attribution|r[ée]attribu|l['’]?\s*œuvre|l['’]?\s*oeuvre"
    r"|dessin\s+r[ée]attribu|a\s+rappel[ée]|a\s+propos[ée]|\bselon\b|\bnote\b"
    r"|a\s+dessin[ée]|a\s+grav[ée]|a\s+peint|\bd'après\s+une\s+note",
    re.IGNORECASE)
# « avant » qui n'est pas un artiste : manufacture, atelier-entreprise, centre.
_RE_NON_ARTISTE = re.compile(r"^\s*(?:manufacture|fabrique|centre|usine)\b",
                             re.IGNORECASE)
_RE_COPIE = re.compile(r"d['’]apr[eè]s|\bcopie", re.IGNORECASE)
_RE_ANON = re.compile(r"\banonymes?\b", re.IGNORECASE)
# Marqueur de doute DANS l'« avant » (« attribué à », « école de », « ? »…) —
# « attribu[ée] » borné ne matche pas « attribution » (donnees.md 2026-07-13).
_RE_DOUTE_AVANT = re.compile(
    r"\battribu[ée]e?\b|[ée]coles?\s+de|\bmani[èe]re\s+de|\bgenre\s+de"
    r"|\bentourage\b|\bsuiveurs?\b|\batelier\b|\(\s*\?\s*\)", re.IGNORECASE)


def _sans_accents(s: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", s)
                   if unicodedata.category(c) != "Mn")


def _segments_pv(s: str) -> list:
    """Découpe sur « ; » MAIS uniquement hors parenthèses : un « ; » à
    l'intérieur d'une parenthèse est biographique (« DYCK (Anvers, 1599 ;
    Blackfriars, 1641) »), pas un séparateur d'attributions."""
    s = s.lstrip(" (")  # parenthèse ouvrante orpheline en tête (saisie malformée)
    out, buf, depth = [], "", 0
    for ch in s:
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth = max(0, depth - 1)
        if ch == ";" and depth == 0:
            out.append(buf)
            buf = ""
        else:
            buf += ch
    out.append(buf)
    return [x.strip(" ,;([") for x in out if x.strip(" ,;([")]


def _pivot(s: str) -> str:
    return _sans_accents(re.sub(r"\s+", " ", _RE_PAR.sub("", s)).strip(" ,;").upper())


def _nom_personne(brut_avant_paren: str):
    """Isole un nom de PERSONNE dans un segment (déjà coupé avant la 1re
    parenthèse). Retire préfixe-artefact, marqueurs de rôle, et coupe à la
    première virgule ou au premier chiffre (les qualificatifs et dates suivent
    le nom : « GIOTTO, attribué en 1859 » → « GIOTTO »). Renvoie le nom nettoyé
    (casse d'origine) ou None si ce n'est pas une personne (école nationale,
    anonyme, prose, manufacture, vide)."""
    t = brut_avant_paren.lstrip(" ,;([")  # « (PIERRE DE CORTONE… » → nom capté
    if _RE_NON_ARTISTE.match(t) or _RE_PROSE.search(t) or _RE_ANON.search(t):
        return None
    t = _RE_PREFIXE.sub("", t)
    # retirer d'éventuels marqueurs de rôle empilés (« copie d'après, école de »)
    for _ in range(3):
        t2 = _RE_ROLE.sub("", t)
        if t2 == t:
            break
        t = t2
    # le nom s'arrête à la 1re virgule ou au 1er chiffre (qualificatif/date après)
    t = re.split(r"[,\d]", t, maxsplit=1)[0].strip(" ,;")
    if not t:
        return None
    pivot = _pivot(t)
    if not pivot:
        return None
    # Après retrait du rôle « école de », tout ce qui commence encore par
    # « ECOLE » est une école (nationale, régionale, ou de style « caravagesque »),
    # jamais une personne. Évite de prendre « ÉCOLE CARAVAGESQUE » pour un nom.
    if pivot.startswith("ECOLE"):
        return None
    # un nom de personne a au moins un mot alphabétique de 3 lettres
    if not re.search(r"[A-Za-zÀ-ÿ]{3,}", t) or len(t) > 45:
        return None
    return t


def _analyse_avant(ancienne: str) -> dict:
    """Décrit le côté « avant » : hypothèses distinctes, natures, drapeaux."""
    segments = _segments_pv(ancienne)
    noms, ecoles = [], []
    a_anonyme = a_prose = False
    for seg in segments:
        avant_paren = seg.split("(")[0]
        nettoye = _RE_PREFIXE.sub("", avant_paren).strip(" ,;")  # préfixe-artefact ôté
        nom = _nom_personne(avant_paren)
        if nom:
            noms.append(nom)
        elif _RE_ANON.search(seg):
            a_anonyme = True
        elif _pivot(nettoye).startswith("ECOLE"):
            ecoles.append(_pivot(nettoye))
        elif _RE_PROSE.search(seg):
            a_prose = True
    noms_distincts = list(dict.fromkeys(_pivot(n) for n in noms))
    ecoles_distinctes = list(dict.fromkeys(ecoles))
    # nombre d'HYPOTHÈSES distinctes (noms + écoles ; l'anonyme n'en est pas une)
    n_hypotheses = len(noms_distincts) + len(ecoles_distinctes)
    return {
        "noms": noms,                         # noms de personne (casse d'origine)
        "noms_distincts": noms_distincts,     # pivots
        "n_hypotheses": n_hypotheses,
        "n_segments": len(segments),
        "a_anonyme": a_anonyme,
        "a_ecole": bool(ecoles_distinctes),
        "a_prose": a_prose,
        "a_copie": bool(_RE_COPIE.search(ancienne)),
        "a_doute": bool(_RE_DOUTE_AVANT.search(ancienne)),
        # « avant » affichable en carte : au moins une hypothèse OU un anonyme
        # national (pas une pure note de prose).
        "affichable": n_hypotheses >= 1 or a_anonyme,
    }


def _analyse_apres(auteur: str, en_beaux_arts: bool) -> dict:
    """Décrit le côté « aujourd'hui » via le lexique markers.py."""
    noms, a_doute, a_anonyme, a_copie = [], False, False, False
    for seg in _segments_pv(auteur):
        if _RE_ANON.search(seg):
            a_anonyme = True
            continue
        categorie, _ = markers.famille_segment(seg, en_beaux_arts)
        if categorie in ("propre", "doute"):
            nom = _nom_personne(seg.split("(")[0])
            if nom:
                noms.append(_pivot(nom))
            if categorie == "doute":
                a_doute = True
        elif categorie == "copie":
            a_copie = True
    return {"noms": list(dict.fromkeys(noms)), "a_doute": a_doute,
            "a_anonyme": a_anonyme, "a_copie": a_copie,
            "a_nom": bool(noms)}


def classer(ancienne: str, auteur: str, en_beaux_arts: bool = True) -> dict:
    """Classe une révision. Renvoie un dict :
      categorie   : code interne (voir LIBELLE_CATEGORIE)
      inverse     : bool — l'« avant » n'avait aucun nom (anonyme/école) et
                    l'« aujourd'hui » en porte un (direction inverse à valoriser)
      ancien_nom  : nom lisible unique si UNE seule hypothèse de personne, sinon None
      galerie     : bool — montrable comme carte « avant / après » V1
      avant, apres: les deux analyses (pour tests / débogage)
    """
    av = _analyse_avant(ancienne)
    ap = _analyse_apres(auteur, en_beaux_arts)

    ancien_nom = av["noms"][0] if len(av["noms_distincts"]) == 1 and av["noms"] else None
    avait_un_nom = av["n_hypotheses"] >= 1 and bool(av["noms_distincts"])

    def _meme_personne() -> bool:
        """Même personne avant/après : noms égaux, ou l'un inclus dans l'autre
        (précision de prénom — « Le Nain Louis » ↔ « Le Nain »)."""
        if not (avait_un_nom and ap["noms"]):
            return False
        av_toks = set(av["noms_distincts"][0].split())
        ap_toks = set(ap["noms"][0].split())
        return av_toks <= ap_toks or ap_toks <= av_toks

    # 1) Plusieurs hypothèses distinctes côté « avant » → chaîne (stats, pas carte)
    if av["n_hypotheses"] >= 2:
        categorie = "plusieurs_noms"
    # 2) L'« avant » disait déjà « copie / d'après » → cas à part
    elif av["a_copie"]:
        categorie = "deja_copie"
    # 3) L'« aujourd'hui » nomme un artiste (précédence : nom > copie > anonyme)
    elif ap["a_nom"]:
        if _meme_personne():
            # même personne : « plus prudent » seulement si l'aujourd'hui ajoute
            # une réserve que l'avant n'avait pas (Furini → Furini attribué).
            # Sinon (école de Mazzuola → Mazzuola : confirmation ; Le Nain Louis
            # → Le Nain : précision) → changement mineur, hors galerie.
            categorie = "meme_nom" if ap["a_doute"] else "mineur"
        else:
            categorie = "autre_nom"
    # 4) L'« aujourd'hui » est une copie « d'après » (avant non copie)
    elif ap["a_copie"]:
        categorie = "copie"
    # 5) L'« aujourd'hui » est anonyme (un vrai « vers l'anonyme » suppose un nom avant)
    elif ap["a_anonyme"]:
        categorie = "anonyme" if avait_un_nom else "mineur"
    else:
        categorie = "mineur"

    # direction inverse : on GAGNE une identité (l'avant n'avait pas de nom)
    inverse = (not avait_un_nom) and (ap["a_nom"] or ap["a_doute"]) \
        and categorie in ("autre_nom", "copie")

    # « avant » simple = montrable en carte : un seul segment, OU une seule
    # hypothèse répétée sans mélange avec un anonyme (« Champaigne ; Champaigne »
    # oui ; « anonyme ; Bacci » non — trop composite, verdicts 2026-07-14).
    avant_simple = (av["n_segments"] <= 1
                    or (av["n_hypotheses"] == 1 and not av["a_anonyme"]))
    galerie = (categorie in CATEGORIES_GALERIE and av["affichable"]
               and avant_simple and not av["a_prose"])

    return {"categorie": categorie, "inverse": inverse,
            "ancien_nom": ancien_nom, "galerie": galerie,
            "avant": av, "apres": ap}
