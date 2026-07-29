"""Classement des droits de réutilisation de la PHOTO d'une notice Joconde.

Chantier « vignettes » (2026-07-29). L'onglet « Œuvres » ne montrera une
reproduction que lorsque la réutilisation de l'image est explicitement permise.
Ce module ne décide RIEN d'autre : il lit le seul champ « Crédits
photographiques » d'une notice POP (clé `PHOT` du modèle Joconde) et en tire un
des cinq statuts. Le domaine public de l'œuvre ne dit rien des droits sur sa
photographie : on ne regarde que ce que le musée a écrit sur la photo.

Le champ `PHOT` mêle souvent crédit ET licence, séparés par « # » ou simplement
accolés : « © Jean-François Peiré#Licence Ouverte/Etalab », « Marie-Laure Le
Brazidec CC BY-SA », « RMN-Grand Palais ». On scanne donc tout le champ.

RÈGLES DE PRUDENCE (cahier des charges) :
- une restriction explicite l'emporte TOUJOURS sur une mention ouverte ;
- « CC BY » n'est pas reconnu par simple sous-chaîne : CC BY-NC / CC BY-ND et
  leurs variantes restent à examiner (statut `unknown`), jamais `open` ;
- un © ou un nom de photographe n'est pas une licence ;
- `authorized` n'est JAMAIS déduit automatiquement (autorisation individuelle) ;
- en cas de contradiction, `unknown`.

La classification porte UNIQUEMENT sur le champ PHOT (jamais sur le reste de la
page POP : son pied de page cite Etalab pour le site lui-même).
"""

import re
import unicodedata

OPEN = "open"
AUTHORIZED = "authorized"
RESTRICTED = "restricted"
UNKNOWN = "unknown"
UNAVAILABLE = "unavailable"


def _norm(chaine: str) -> str:
    """Minuscule, sans accents, tirets unifiés, espaces compactés."""
    if not chaine:
        return ""
    sans = unicodedata.normalize("NFD", chaine)
    sans = "".join(c for c in sans if unicodedata.category(c) != "Mn")
    sans = sans.replace("‑", "-").replace("–", "-").replace("—", "-")
    return re.sub(r"\s+", " ", sans).strip().lower()


# Restrictions explicites : priorité absolue. Formulations relevées sur POP
# (« utilisation soumise à autorisation » de la RMN, ADAGP, droits réservés…).
RESTRICTIONS = [
    "utilisation soumise a autorisation",
    "soumise a autorisation",
    "sauf autorisation",
    "adagp",
    "tous droits reserves",
    "droits reserves",
    "droit reserve",
    "droits de reproduction",
    "reproduction reserv",
    "representation reserv",
    "reproduction ou de representation",
]


def _licence_ouverte(n: str):
    """Licence ouverte reconnue dans le champ normalisé, ou None."""
    if "licence ouverte" in n:
        return "Licence Ouverte/Etalab" if "etalab" in n else "Licence Ouverte"
    if "etalab" in n:  # « Etalab 2.0 », « etalab-2.0 » sans « licence ouverte »
        return "Etalab 2.0"
    if re.search(r"\bcc0\b", n):
        return "CC0"
    return None


def _creative_commons_by(n: str):
    """Renvoie ('open', libellé) pour CC BY / CC BY-SA, ('examiner', libellé)
    pour les variantes NC/ND (à ne jamais reconnaître comme ouvertes), ou None.
    On capture le jeton CC BY complet pour distinguer -SA de -NC/-ND."""
    m = re.search(r"cc[ -]by[-a-z]*", n)
    if not m:
        return None
    jeton = m.group(0).replace(" ", "-")  # cc-by, cc-by-sa, cc-by-nc-nd…
    if "nc" in jeton or "nd" in jeton:
        return ("examiner", jeton.upper())
    if jeton in ("cc-by", "cc-by-sa"):
        return ("open", "CC BY-SA" if jeton == "cc-by-sa" else "CC BY")
    return ("examiner", jeton.upper())  # variante inconnue : prudence


def classer(phot, presence_image=True, artiste_sous_droits=""):
    """Statut de réutilisation de la photo d'une notice.

    Renvoie (statut, licence, credit, raison). `licence` et `credit` sont vides
    quand ils ne s'appliquent pas. `raison` documente la décision (traçabilité).
    """
    credit = (phot or "").strip()

    # Aucune image : rien à montrer, peu importe le crédit.
    if not presence_image:
        return (UNAVAILABLE, "", "", "aucune image sur POP")

    # Œuvre dont l'auteur est encore sous droits (champ Joconde) : la photo d'une
    # œuvre protégée reste restreinte, sauf autorisation explicite (Palier 2).
    if (artiste_sous_droits or "").strip():
        return (RESTRICTED, "", credit, "artiste sous droits")

    n = _norm(phot)
    cc = _creative_commons_by(n)
    ouverte = _licence_ouverte(n)

    # 1. Restriction explicite : l'emporte sur tout le reste.
    for motif in RESTRICTIONS:
        if motif in n:
            return (RESTRICTED, "", credit, f"mention restrictive : {motif}")

    # 2. Variante CC restrictive (NC/ND) : à examiner, jamais ouverte.
    if cc and cc[0] == "examiner":
        return (UNKNOWN, cc[1], credit, "licence CC à examiner (NC/ND)")

    # 3. Licence ouverte reconnue.
    if ouverte:
        return (OPEN, ouverte, credit, "licence ouverte")
    if cc and cc[0] == "open":
        return (OPEN, cc[1], credit, "licence Creative Commons ouverte")

    # 4. Image présente mais pas de licence reconnue.
    if not n:
        return (UNKNOWN, "", "", "crédit photographique absent")
    return (UNKNOWN, "", credit, "crédit sans licence explicite")
