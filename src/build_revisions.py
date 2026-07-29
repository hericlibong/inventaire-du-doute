"""Export « Avant / après » : les révisions d'attribution (phase 3, P3-T2).

Produit data/exports/web/revisions.json à partir du champ Ancienne_attribution :
les notices où la base garde la trace d'un ancien nom DIFFÉRENT de l'auteur
retenu aujourd'hui. Deux parties :

- des STATISTIQUES sur tout le corpus : par type de passage, par domaine, par
  siècle de l'œuvre, part datée, anciens noms qui reviennent, concentration ;
- un LOT ÉDITORIAL réduit (~32 cas lisibles) sélectionné par DIVERSITÉ (quotas
  par type de passage, plafond 2 par musée) — pour la galerie « avant → après ».

Classification : src/revisions_classify.py (classer), calé sur les 80 verdicts
humains du 2026-07-14 (tests/test_revisions.py). Sept catégories, dont trois
issues de la vérification : « Même nom, attribution plus prudente »,
« Déjà une copie ou un d'après », « Plusieurs anciens noms » (chaînes, en stats
seulement). Direction inverse (anonyme → un nom) chiffrée pour équilibrer le récit.

Anciens noms : liste curée rattachée au MOT ENTIER (piège SERODINE/RODIN),
comptée HORS « d'après » — repère/filtre, pas palmarès (donnees.md 2026-07-14).

Usage : uv run python src/build_revisions.py  (~2 min)
"""

import json
import re
import unicodedata
from collections import Counter
from datetime import datetime, timezone

import pandas as pd

import markers
import revisions_classify as rc
from config import CHEMIN_CSV, DOSSIER_EXPORTS, URL_CSV

DOSSIER_WEB = DOSSIER_EXPORTS / "web"
TAILLE_MORCEAU = 200_000

COLONNES = ["Reference", "Auteur", "Ancienne_attribution", "Titre",
            "Nom_officiel_musee", "Ville", "Domaine", "Millesime_de_creation",
            "Presence_image"]

# Ordre d'affichage des catégories dans la section statistiques.
ORDRE_CATEGORIES = ["autre_nom", "meme_nom", "anonyme", "copie",
                    "deja_copie", "plusieurs_noms", "mineur"]
# Quotas du lot éditorial V1 (cible ~32) sur les catégories montrables en carte,
# + un contingent « direction inverse » (anonyme → un nom) pour équilibrer.
QUOTAS_LOT = {"autre_nom": 9, "meme_nom": 7, "anonyme": 6, "copie": 6}
QUOTA_INVERSE = 4
PLAFOND_MUSEE = 2  # cas maximum par musée dans le lot V1 (plafond GLOBAL)

# Longueur maxi de l'ancienne attribution pour une carte lisible.
LONGUEUR_CARTE = 90

# Anciens noms « qui reviennent » : liste CURÉE, pour le filtre de la galerie ET
# une barre de fréquence. Rattachement MOT ENTIER sur le pivot (accents ôtés),
# comptage HORS « d'après ». Repère, pas palmarès. (id, libellé, motifs inclus).
ANCIENS_NOMS = [
    ("vinci", "Léonard de Vinci", ["VINCI"]),
    ("poussin", "Nicolas Poussin", ["POUSSIN"]),
    ("rubens", "Rubens", ["RUBENS"]),
    ("rembrandt", "Rembrandt", ["REMBRANDT"]),
    ("le-brun", "Charles Le Brun", ["LE BRUN"]),
    ("fragonard", "Fragonard", ["FRAGONARD"]),
    ("watteau", "Watteau", ["WATTEAU"]),
    ("durer", "Dürer", ["DURER"]),
    ("tiepolo", "Tiepolo", ["TIEPOLO"]),
    ("raphael", "Raphaël", ["RAPHAEL"]),
    ("titien", "Titien", ["TITIEN", "TIZIANO"]),
    ("michel-ange", "Michel-Ange", ["MICHEL-ANGE", "BUONARROTI"]),
    ("mantegna", "Mantegna", ["MANTEGNA"]),
    ("botticelli", "Botticelli", ["BOTTICELLI"]),
    ("chardin", "Chardin", ["CHARDIN"]),
    ("caravage", "Caravage", ["CARAVAGE"]),
    ("velasquez", "Vélasquez", ["VELASQUEZ"]),
    ("greco", "Le Greco", ["GRECO"]),
    ("correge", "Le Corrège", ["CORREGE"]),
    ("mignard", "Mignard", ["MIGNARD"]),
    ("rigaud", "Hyacinthe Rigaud", ["RIGAUD"]),
    ("boucher", "François Boucher", ["BOUCHER FRANCOIS", "BOUCHER"]),
]

_RE_COPIE_ANC = re.compile(r"d['’]apr[eè]s|\bcopie", re.IGNORECASE)
_RE_DATE = re.compile(r"attribu[ée]e?\s+(?:en|vers)\s+(\d{4})"
                      r"|cat(?:alogue)?\.?\s*(\d{4})", re.IGNORECASE)


def _sans_accents(s: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", s)
                   if unicodedata.category(c) != "Mn")


def _pivot(s: str) -> str:
    sans_paren = markers._RE_PARENTHESES.sub("", s)
    return _sans_accents(re.sub(r"\s+", " ", sans_paren).strip(" ,;").upper())


def _norme_compare(valeur: str) -> str:
    """Normalisation pour l'égalité ancien/actuel (parenthèses retirées, casse
    ignorée). Reproduit le test de l'audit (26 667 notices)."""
    return re.sub(r"\(.*?\)", "", str(valeur)).strip().strip(",").strip().upper()


def _mot_entier(motif: str, pivot: str) -> bool:
    return re.search(rf"\b{re.escape(motif)}\b", pivot) is not None


def _noms_attribues(ancienne: str) -> list:
    """Ids des anciens noms curés présents (mot entier), SEULEMENT si l'ancienne
    étiquette n'était pas déjà une copie « d'après » (« autrefois donné à X »,
    pas « copie d'après X »). Sert au filtre et à la barre de fréquence."""
    if _RE_COPIE_ANC.search(ancienne):
        return []
    pivot = _pivot(ancienne)
    return [nid for nid, _, motifs in ANCIENS_NOMS
            if any(_mot_entier(m, pivot) for m in motifs)]


def _annee_revision(ancienne: str):
    """Année de la révision (« attribué en 1869 », « CAT. 1938 »), la plus
    ancienne, ou None. Distincte de la date de l'œuvre."""
    annees = [int(a or b) for a, b in _RE_DATE.findall(ancienne)]
    annees = [a for a in annees if 1700 <= a <= 2026]
    return min(annees) if annees else None


def _siecle_oeuvre(millesime):
    try:
        an = int(str(millesime)[:4])
    except (ValueError, TypeError):
        return None
    return (an - 1) // 100 + 1 if 500 <= an <= 2025 else None


def main() -> None:
    total_notices = 0
    corpus = 0
    categories = Counter()
    inverse_total = 0
    domaines = Counter()
    siecles = Counter()
    n_datees = 0
    noms_freq = Counter()
    musees_corpus = set()
    n_louvre = 0
    n_dessin = 0
    candidats = {c: [] for c in QUOTAS_LOT}  # cas de galerie, par catégorie

    morceaux = pd.read_csv(CHEMIN_CSV, sep="|", usecols=COLONNES, dtype=str,
                           chunksize=TAILLE_MORCEAU)
    for morceau in morceaux:
        total_notices += len(morceau)
        for ref, aut, anc, titre, musee, ville, dom, mil, img in zip(
            morceau["Reference"], morceau["Auteur"],
            morceau["Ancienne_attribution"], morceau["Titre"],
            morceau["Nom_officiel_musee"], morceau["Ville"],
            morceau["Domaine"], morceau["Millesime_de_creation"],
            morceau["Presence_image"],
        ):
            if not isinstance(aut, str) or not isinstance(anc, str):
                continue
            aut, anc = aut.strip(), anc.strip()
            if not aut or not anc:
                continue
            if _norme_compare(anc) == _norme_compare(aut):
                continue  # le champ répète l'auteur actuel : pas une révision

            corpus += 1
            en_ba = markers._dans_beaux_arts(dom)
            res = rc.classer(anc, aut, en_ba)
            cat = res["categorie"]
            categories[cat] += 1
            if res["inverse"]:
                inverse_total += 1

            dom1 = dom.split(";")[0].strip().lower() if isinstance(dom, str) else ""
            if dom1:
                domaines[dom1] += 1
            if isinstance(musee, str) and musee.strip():
                musees_corpus.add(musee.strip())
                if musee.strip() == "musée du Louvre":
                    n_louvre += 1
            if dom1 == "dessin":
                n_dessin += 1

            s = _siecle_oeuvre(mil)
            if s:
                siecles[s] += 1
            for nid in _noms_attribues(anc):
                noms_freq[nid] += 1
            annee = _annee_revision(anc)
            if annee is not None:
                n_datees += 1

            # candidat au lot V1 : montrable en carte + titre + verbatim court
            if (res["galerie"] and cat in candidats
                    and isinstance(titre, str) and titre.strip()
                    and len(anc) <= LONGUEUR_CARTE):
                candidats[cat].append({
                    "reference": ref if isinstance(ref, str) else None,
                    "titre": titre.strip(),
                    "musee": musee.strip() if isinstance(musee, str) else None,
                    "ville": ville.strip() if isinstance(ville, str) else None,
                    "ancienne_brut": anc,
                    "auteur_brut": aut,
                    "ancien_nom": res["ancien_nom"],
                    "categorie": cat,
                    "libelle": rc.LIBELLE_CATEGORIE[cat],
                    "inverse": res["inverse"],
                    "annee": annee,
                    "domaine": dom1 or None,
                    "anciens_noms_ids": _noms_attribues(anc),
                    "image_presente": isinstance(img, str)
                    and img.strip().lower() == "oui",
                    # Emplacement RÉSERVÉ pour une vignette future (décision
                    # 2026-07-14 ter). On NE hotlinke PAS POP : la Licence
                    # Ouverte couvre le texte, pas les clichés. Tant que les
                    # droits ne sont pas clarifiés fichier par fichier, statut
                    # « pending » et rien à afficher. Le front n'affiche une
                    # image que si statut ∈ {open, authorized} + url + credit.
                    "image": {
                        "statut": "pending",  # open|authorized|pending|restricted
                        "url": None,           # jamais un lien POP
                        "alt": None,           # texte alternatif, si affichée
                        "credit": None,        # auteur, si affichée
                        "licence": None,       # licence / statut de réutilisation
                        "source": None,        # ex. « Wikimedia Commons »
                    },
                })
        print(f"\r  {total_notices:,} notices lues".replace(",", " "),
              end="", flush=True)
    print()

    assert sum(categories.values()) == corpus, "catégories ≠ corpus"

    # ---- Lot V1 : quotas par catégorie + contingent inverse, plafond 2/musée ----
    lot, vus = [], Counter()

    def _prendre(population, quota):
        pris = 0
        for cas in sorted(population, key=lambda c: not c["image_presente"]):
            if any(c["reference"] == cas["reference"] for c in lot):
                continue
            if vus[cas["musee"]] >= PLAFOND_MUSEE:
                continue
            vus[cas["musee"]] += 1
            lot.append(cas)
            pris += 1
            if pris >= quota:
                break
        return pris

    # d'abord un contingent « direction inverse » (puisé dans toutes les catégories)
    inverses = [c for cat in candidats for c in candidats[cat] if c["inverse"]]
    _prendre(inverses, QUOTA_INVERSE)
    # puis les quotas par catégorie
    for cat, quota in QUOTAS_LOT.items():
        pris = _prendre(candidats[cat], quota)
        assert pris >= min(quota, 1), f"catégorie de galerie vide : {cat}"

    assert all(c["reference"] for c in lot), "cas sans référence POP"
    cap = Counter(c["musee"] for c in lot)
    assert all(v <= PLAFOND_MUSEE for v in cap.values()), "plafond musée dépassé"

    # ---- Mise en forme des sorties ----
    passages = [
        {"categorie": c, "libelle": rc.LIBELLE_CATEGORIE[c],
         "notices": categories[c], "galerie": c in rc.CATEGORIES_GALERIE}
        for c in ORDRE_CATEGORIES if categories[c]
    ]
    domaines_top = [{"label": d, "notices": n} for d, n in domaines.most_common(10)]
    siecles_liste = [{"siecle": s, "notices": siecles[s]} for s in sorted(siecles)]
    label_nom = {nid: lib for nid, lib, _ in ANCIENS_NOMS}
    anciens_noms = [{"id": nid, "label": label_nom[nid], "notices": n}
                    for nid, n in noms_freq.most_common(15)]

    sortie = {
        "source": "Collections des musées de France : base Joconde",
        "url_source": URL_CSV,
        "version_donnee": "2026-07-01",
        "lexique": "markers.py v2 + revisions_classify.py (verdicts 2026-07-14)",
        "date_generation": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "libelles_categorie": rc.LIBELLE_CATEGORIE,
        "categories_galerie": sorted(rc.CATEGORIES_GALERIE),
        "totaux": {
            "revisions": corpus,
            "categories": {c: categories[c] for c in ORDRE_CATEGORIES},
            "datees": n_datees,
            "non_datees": corpus - n_datees,
            "n_musees": len(musees_corpus),
            "part_louvre": round(n_louvre / corpus, 3),
            "part_dessin": round(n_dessin / corpus, 3),
            "direction_inverse": inverse_total,
        },
        "passages": passages,
        "domaines": domaines_top,
        "siecles": siecles_liste,
        "anciens_noms": anciens_noms,
        "cas": lot,
    }

    DOSSIER_WEB.mkdir(parents=True, exist_ok=True)
    chemin = DOSSIER_WEB / "revisions.json"
    chemin.write_text(json.dumps(sortie, ensure_ascii=False, indent=1),
                      encoding="utf-8")

    # ---- Récapitulatif console ----
    print(f"\nCorpus « Avant / après » : {corpus} révisions "
          f"sur {len(musees_corpus)} musées")
    print(f"Export → {chemin} ({chemin.stat().st_size / 1024:.1f} Ko)\n")
    print(f"{'catégorie':36} {'notices':>8}  {'part':>5}  galerie")
    for p in passages:
        print(f"{p['libelle']:36} {p['notices']:>8}  "
              f"{100 * p['notices'] / corpus:>4.1f}%   {'oui' if p['galerie'] else '—'}")
    print(f"\ndirection inverse (anonyme → un nom) : {inverse_total} "
          f"| datées : {n_datees} ({100*n_datees/corpus:.1f}%)")
    print(f"concentration : Louvre {100*n_louvre/corpus:.1f}% | "
          f"dessin {100*n_dessin/corpus:.1f}%")
    louvre_lot = sum(1 for c in lot if c["musee"] == "musée du Louvre")
    print(f"\nLot V1 : {len(lot)} cas | {len(cap)} musées | "
          f"Louvre {100*louvre_lot/len(lot):.0f}% | "
          f"inverse {sum(c['inverse'] for c in lot)} | "
          f"illustrés POP {sum(c['image_presente'] for c in lot)}/{len(lot)}")
    print("anciens noms (top 5, hors copie) : "
          + ", ".join(f"{label_nom[n]} {c}" for n, c in noms_freq.most_common(5)))


if __name__ == "__main__":
    main()
