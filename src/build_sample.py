"""Échantillon de vérification manuelle (T4).

Tire ~200 notices détectées par le lexique, stratifiées par famille de
marqueur : les familles rares sont sur-représentées (un tirage proportionnel
ne contiendrait presque que des « attribué à »), les familles minuscules
(présumé : 4 cas) sont prises en entier. Graine aléatoire fixée : le tirage
est reproductible.

Sortie : data/exports/echantillon_verification.csv, à ouvrir dans un tableur.
L'utilisateur remplit les colonnes `verdict` et `commentaire` (mode d'emploi :
docs/verification-echantillon.md). Une ligne = un marqueur sur une notice ;
une notice portant deux marqueurs peut donc apparaître deux fois.

Usage : uv run python src/build_sample.py           (échantillon complet T4)
        uv run python src/build_sample.py recheck   (mini-contrôle T4bis :
        familles reformulées en v1 uniquement, graine différente)
"""

import sys

import pandas as pd

import markers
from config import CHEMIN_CSV, DOSSIER_EXPORTS, URL_NOTICE_POP

GRAINE = 42

# Nombre de notices tirées par famille (≈ 206 au total). Les familles jugées
# fiables mais massives sont échantillonnées ; les suspectes et les rares
# sont sur-représentées ou prises en entier.
QUOTAS = {
    "attribue": 30,
    "point_interrogation": 25,
    "atelier_de": 25,  # à surveiller : « ATELIER DE MOULAGE » n'est pas un doute
    "ecole_de": 20,
    "maniere_de": 15,
    "entourage_de": 15,
    "genre_de": 15,  # suspect
    "suiveur_de": 10,
    "presume": 4,  # la famille entière
    "d_apres": 15,
    "copie": 10,  # suspect
    "anciennement_attribue": 7,  # la famille entière
    "champ_ancienne_attribution": 15,
}

# Mini-contrôle T4bis : uniquement les familles touchées par le lexique v1,
# plus la population écartée (vérifier qu'on ne jette pas de vrais doutes).
# Graine différente de T4 pour limiter le recouvrement avec le premier tirage.
GRAINE_RECHECK = 202607
QUOTAS_RECHECK = {
    "atelier_de": 20,
    "atelier_nom": 15,
    "ecole_de": 15,
    "point_interrogation": 15,
}

COLONNES = [
    "Reference", "Auteur", "Precisions_sur_l_auteur", "Ancienne_attribution",
    "Ecole_pays", "Domaine", "Titre", "Denomination",
    "Nom_officiel_musee", "Ville",
]
TAILLE_MORCEAU = 200_000


def champ_et_extrait(famille: markers.Famille, ligne: pd.Series) -> tuple[str, str]:
    """Renvoie (champ où le marqueur a été trouvé, extrait autour du marqueur)."""
    for champ in famille.champs:
        valeur = ligne[champ]
        if pd.isna(valeur):
            continue
        valeur = str(valeur)
        if famille.fonction or not famille.motif:
            # détection sur mesure ou « présence de champ » : pas de motif à
            # encadrer, on montre le début du champ
            return champ, valeur[:120]
        m = markers._COMPILES[famille.code].search(valeur)
        if m:
            debut, fin = max(0, m.start() - 40), m.end() + 40
            return champ, ("…" if debut else "") + valeur[debut:fin] + (
                "…" if fin < len(valeur) else ""
            )
    return "", ""


def main() -> None:
    recheck = len(sys.argv) > 1 and sys.argv[1] == "recheck"
    quotas = QUOTAS_RECHECK if recheck else QUOTAS
    graine = GRAINE_RECHECK if recheck else GRAINE
    nom_sortie = (
        "echantillon_recheck.csv" if recheck else "echantillon_verification.csv"
    )

    # 1. Une passe sur le CSV : on garde toutes les notices détectées, par famille.
    candidats = {code: [] for code in quotas}
    lus = 0
    morceaux = pd.read_csv(
        CHEMIN_CSV, sep="|", usecols=COLONNES, dtype=str, chunksize=TAILLE_MORCEAU
    )
    for morceau in morceaux:
        det = markers.detections(morceau)
        for code in quotas:
            trouves = morceau[det[code]]
            if len(trouves):
                candidats[code].append(trouves)
        lus += len(morceau)
        print(f"\r  {lus:,} notices lues".replace(",", " "), end="", flush=True)
    print()

    # 2. Tirage stratifié, graine fixée.
    lignes = []
    for famille in markers.FAMILLES:
        code = famille.code
        if code not in quotas:
            continue
        pool = pd.concat(candidats[code]).drop_duplicates("Reference")
        tirage = pool.sample(n=min(quotas[code], len(pool)), random_state=graine)
        print(f"  {famille.libelle:<40} {len(tirage):>3} tirées / {len(pool):,} détectées".replace(",", " "))
        for _, ligne in tirage.iterrows():
            champ, extrait = champ_et_extrait(famille, ligne)
            lignes.append({
                "famille": famille.libelle,
                "categorie": famille.categorie,
                "champ_source": champ,
                "extrait": extrait,
                "auteur": ligne["Auteur"],
                "precisions_auteur": ligne["Precisions_sur_l_auteur"],
                "ancienne_attribution": ligne["Ancienne_attribution"],
                "titre": ligne["Titre"],
                "denomination": ligne["Denomination"],
                "domaine": ligne["Domaine"],
                "musee": ligne["Nom_officiel_musee"],
                "ville": ligne["Ville"],
                "reference": ligne["Reference"],
                "lien_pop": URL_NOTICE_POP.format(reference=ligne["Reference"]),
                "verdict": "",
                "commentaire": "",
            })

    echantillon = pd.DataFrame(lignes)
    DOSSIER_EXPORTS.mkdir(parents=True, exist_ok=True)
    destination = DOSSIER_EXPORTS / nom_sortie
    # utf-8-sig : accents corrects à l'ouverture directe dans Excel/LibreOffice
    echantillon.to_csv(destination, index=False, encoding="utf-8-sig")
    print(f"\n→ {len(echantillon)} lignes écrites dans {destination}")


if __name__ == "__main__":
    main()
