"""Échantillon de vérification manuelle pour la rubrique « Avant / après ».

Produit data/exports/echantillon_revisions.csv : ~70 notices STRATIFIÉES pour
que l'utilisateur juge (colonnes `verdict` et `commentaire` à remplir) :
- la classification du TYPE DE PASSAGE est-elle juste ?
- l'extraction de l'ancien nom est-elle fiable (pas de sous-chaîne) ?
- les cas-pièges sont-ils bien gérés (chaînes, écoles nationales, noms proches,
  copies « d'après », direction inverse) ?

Strates (graine fixe, reproductible) : les 4 types de passage sur des cas
propres, plus 6 strates de pièges. Réutilise EXACTEMENT la logique du pipeline
(src/build_revisions.py) pour tester ce qui sera publié, pas une variante.

Usage : uv run python src/build_revisions_sample.py  (~2 min)
"""

import csv
import random
import re
import unicodedata

import pandas as pd

import build_revisions as br
import markers
from config import CHEMIN_CSV, DOSSIER_EXPORTS, URL_NOTICE_POP

GRAINE = 20260714
TAILLE_MORCEAU = 200_000
COLONNES = ["Reference", "Auteur", "Ancienne_attribution", "Titre",
            "Nom_officiel_musee", "Ville", "Domaine"]

# Mots vides pour le repérage « noms proches » (prénoms, génériques).
_STOP = {"ECOLE", "ANCIENNE", "ATTRIBUTION", "ATTRIBUTIONS", "SIECLE", "ANONYME",
         "MAITRE", "JEAN", "PIERRE", "JACQUES", "LOUIS", "CHARLES", "ANTOINE",
         "FRANCOIS", "ANDREA", "GIOVANNI", "BATTISTA", "SUPPL", "TAUZIA",
         "BRIERE", "INVENTAIRE", "CATALOGUE"}


def _tokens(valeur: str) -> set:
    return {t for t in re.split(r"[^A-Z]+", br._pivot(valeur)) if len(t) >= 4} - _STOP


def main() -> None:
    rng = random.Random(GRAINE)
    lignes = []

    morceaux = pd.read_csv(CHEMIN_CSV, sep="|", usecols=COLONNES, dtype=str,
                           chunksize=TAILLE_MORCEAU)
    for morceau in morceaux:
        for ref, aut, anc, titre, musee, ville, dom in zip(
            morceau["Reference"], morceau["Auteur"],
            morceau["Ancienne_attribution"], morceau["Titre"],
            morceau["Nom_officiel_musee"], morceau["Ville"], morceau["Domaine"],
        ):
            if not isinstance(aut, str) or not isinstance(anc, str):
                continue
            aut, anc = aut.strip(), anc.strip()
            if not aut or not anc:
                continue
            if br._norme_compare(anc) == br._norme_compare(aut):
                continue
            en_ba = markers._dans_beaux_arts(dom)
            passage = br._type_passage(aut, en_ba)
            lignes.append({
                "reference": ref if isinstance(ref, str) else "",
                "lien_pop": URL_NOTICE_POP.format(reference=ref)
                if isinstance(ref, str) else "",
                "type_passage_predit": br.LIBELLE_PASSAGE[passage],
                "ancienne_attribution_brut": anc,
                "auteur_actuel_brut": aut,
                "ancien_nom_extrait": br._ancien_nom_lisible(anc) or "",
                "anciens_noms_reconnus": " ; ".join(br._noms_presents(anc)),
                "annee_revision": br._annee_revision(anc) or "",
                "titre": titre.strip() if isinstance(titre, str) else "",
                "musee": musee.strip() if isinstance(musee, str) else "",
                "ville": ville.strip() if isinstance(ville, str) else "",
                # étiquettes internes de strate (aident au tri, pas un verdict)
                "_passage": passage,
                "_chaine": ";" in anc,
                "_ecole": br._pivot(anc).startswith("ECOLE"),
                "_copie_anc": bool(br._RE_COPIE_ANC.search(anc)),
                "_datee": br._annee_revision(anc) is not None,
                "_proche": bool(_tokens(anc) & _tokens(aut)),
                "_inverse": bool(re.search(r"\banonymes?\b", anc, re.I))
                and passage in ("autre_nom", "prudent"),
            })
        print(f"\r  {len(lignes):,} révisions collectées".replace(",", " "),
              end="", flush=True)
    print()

    # ---- Strates (cible ~70). Cas propres = ni chaîne ni école. ----
    def propres(p):
        return [l for l in lignes
                if l["_passage"] == p and not l["_chaine"] and not l["_ecole"]]

    strates = [
        ("passage : vers un autre nom", propres("autre_nom"), 8),
        ("passage : vers une attribution prudente", propres("prudent"), 8),
        ("passage : vers l'anonyme", propres("anonyme"), 8),
        ("passage : vers une copie", propres("copie"), 8),
        ("piège : chaîne d'attributions (≥2 segments)",
         [l for l in lignes if l["_chaine"]], 10),
        ("piège : école nationale en ancien nom",
         [l for l in lignes if l["_ecole"]], 8),
        ("piège : noms proches avant/après",
         [l for l in lignes if l["_proche"] and not l["_ecole"]], 8),
        ("piège : ancienne attribution datée",
         [l for l in lignes if l["_datee"]], 8),
        ("piège : ancien label déjà « d'après » (exclu du comptage noms)",
         [l for l in lignes if l["_copie_anc"]], 6),
        ("contrôle : direction inverse (anonyme → un nom)",
         [l for l in lignes if l["_inverse"]], 8),
    ]

    choisies = []
    vus = set()
    for nom_strate, population, cible in strates:
        rng.shuffle(population)
        pris = 0
        for l in population:
            if l["reference"] in vus:
                continue
            vus.add(l["reference"])
            ligne = {k: v for k, v in l.items() if not k.startswith("_")}
            ligne["strate"] = nom_strate
            ligne["verdict"] = ""       # OK / faux passage / faux parsing / autre
            ligne["commentaire"] = ""
            choisies.append(ligne)
            pris += 1
            if pris >= cible:
                break
        print(f"  {pris:>2}/{cible}  {nom_strate}")

    champs = ["strate", "reference", "lien_pop", "type_passage_predit",
              "ancienne_attribution_brut", "auteur_actuel_brut",
              "ancien_nom_extrait", "anciens_noms_reconnus", "annee_revision",
              "titre", "musee", "ville", "verdict", "commentaire"]
    chemin = DOSSIER_EXPORTS / "echantillon_revisions.csv"
    with chemin.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=champs)
        w.writeheader()
        w.writerows(choisies)

    print(f"\n{len(choisies)} notices → {chemin}")
    print("Colonnes verdict / commentaire à remplir. Références = texte "
          "(garder les zéros de tête au passage tableur).")


if __name__ == "__main__":
    main()
