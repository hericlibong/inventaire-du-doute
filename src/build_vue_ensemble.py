"""Export « Vue d'ensemble » des formulations prudentes (dossier « Les presque »).

Produit data/exports/web/vue_ensemble.json à partir des agrégats DÉJÀ validés
(artistes.json + niveaux.json + musees.json) — pas de nouvelle passe sur le CSV
de 1,1 Go : tout est recalculé depuis les exports source de vérité, avec des
`assert` de cohérence.

Message central porté par cette vue (docs/donnees.md 2026-07-15) :
> Dans l'ensemble de Joconde, « attribué à » domine fortement. Dans les 27 noms
> retenus, les liens plus indirects — école, atelier, manière — prennent plus de
> place. C'est ce contraste qui doit porter la future section « Vue d'ensemble ».

Garde-fous méthodologiques (repris du rapport de reconnaissance) :
- Les familles PEUVENT SE RECOUVRIR (une notice porte parfois plusieurs formules)
  → on ne les additionne pas en un tout, et surtout PAS de diagramme en anneau
  pour cette section (contrairement à « Avant / après »).
- Aucun classement PAR NOM hors des 27 : hors des 27, seul le total par famille
  est publiable (pas de désambiguïsation des homonymes).
- Pas de période en V1 (couverture ~16 % de datables, trop lacunaire).
- Domaines et top musées volontairement laissés hors de cet export (réserve).
"""

import json
from datetime import datetime, timezone
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
WEB = RACINE / "data" / "exports" / "web"

# Les 8 familles de doute « solides », dans l'ordre de fréquence globale. La
# famille marginale `presume` (n=4, suspecte) est volontairement exclue.
FAMILLES = [
    "attribue", "point_interrogation", "ecole_de", "atelier_de",
    "maniere_de", "entourage_de", "genre_de", "suiveur_de",
]

# Niveau de l'échelle du doute par famille (docs/typologie.md) :
# 1 « Presque lui », 2 « Autour de lui », 3 « Son style, sans lui ».
NIVEAU_FAMILLE = {
    "attribue": 1, "point_interrogation": 1,
    "ecole_de": 2, "atelier_de": 2, "entourage_de": 2,
    "maniere_de": 3, "suiveur_de": 3, "genre_de": 3,
}


def charger(nom):
    return json.loads((WEB / nom).read_text(encoding="utf-8"))


def main():
    artistes = charger("artistes.json")
    niveaux = charger("niveaux.json")
    musees = charger("musees.json")

    fam_global = niveaux["familles"]  # {code: {libelle, categorie, notices}}

    # --- Familles DANS les 27 : somme des tallies par artiste ---
    dans_27 = {code: 0 for code in FAMILLES}
    for a in artistes["artistes"]:
        for f in a["familles"]:
            if f["code"] in dans_27:
                dans_27[f["code"]] += f["notices"]

    familles = []
    for code in FAMILLES:
        g = fam_global[code]["notices"]
        d = dans_27[code]
        familles.append({
            "code": code,
            "libelle": fam_global[code]["libelle"],
            "niveau": NIVEAU_FAMILLE[code],
            "global": g,
            "dans_27": d,
            "hors_27": g - d,
        })
        assert d <= g, f"dans_27 > global pour {code}"

    # --- Niveaux : global, dans les 27, et global hors monoculture ---
    n_global = [niveaux["niveaux"][str(k)]["notices"] for k in (1, 2, 3)]
    n_dans_27 = [sum(a["niveaux"][i] for a in artistes["artistes"]) for i in range(3)]

    mono = niveaux["monoculture_divulguee"]
    musee_mono = next(m for m in musees if m["code_museofile"] == mono["code_museofile"])
    n_mono = musee_mono["niveaux"]  # [5791, 0, 0] : monoculture 100 % niveau 1
    n_hors_mono = [n_global[i] - n_mono[i] for i in range(3)]

    assert sum(n_hors_mono) == niveaux["doute_hors_monoculture"], \
        "niveaux hors monoculture incohérents avec doute_hors_monoculture"

    libelles_niveaux = {int(k): v["libelle"] for k, v in niveaux["niveaux"].items()}
    niveaux_vue = [
        {
            "niveau": k,
            "libelle": libelles_niveaux[k],
            "global": n_global[k - 1],
            "dans_27": n_dans_27[k - 1],
            "global_hors_monoculture": n_hors_mono[k - 1],
        }
        for k in (1, 2, 3)
    ]

    # --- Totaux ---
    doute_dans_27 = sum(a["doute"] for a in artistes["artistes"])
    assert doute_dans_27 == sum(n_dans_27), "doute des 27 incohérent avec ses niveaux"

    totaux = {
        "doute_total": niveaux["doute_total"],
        "doute_dans_27": doute_dans_27,
        "doute_hors_27": niveaux["doute_total"] - doute_dans_27,
        "doute_hors_monoculture": niveaux["doute_hors_monoculture"],
    }

    # --- Copies « d'après » : tenues À PART, jamais additionnées au doute ---
    copies = {
        "total": niveaux["copie"],
        "dont_d_apres": fam_global["d_apres"]["notices"],
    }

    vue = {
        "source": artistes["source"],
        "url_source": artistes["url_source"],
        "version_donnee": artistes["version_donnee"],
        "lexique": artistes["lexique"],
        "critere_27": artistes["critere"],
        "date_generation": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "message_central": (
            "Dans l'ensemble de Joconde, « attribué à » domine fortement. Dans "
            "les 27 noms retenus, les liens plus indirects — école, atelier, "
            "manière — prennent plus de place."
        ),
        "note_methodo": (
            "Les familles peuvent se recouvrir : on ne les additionne pas et on "
            "n'utilise pas de diagramme en anneau. Hors des 27 noms, seul le "
            "total par famille est publiable (pas de classement par nom). La "
            "monoculture divulguée (planches Barla, Nice) pèse une large part du "
            "doute national ; « global hors monoculture » permet de la neutraliser."
        ),
        "totaux": totaux,
        "monoculture": {
            "musee": musee_mono["nom"],
            "ville": musee_mono["ville"],
            "libelle": mono["libelle"],
            "doute": mono["doute"],
            "part_du_doute_national": mono["part_du_doute_national"],
        },
        "familles": familles,
        "niveaux": niveaux_vue,
        "copies_dapres": copies,
    }

    sortie = WEB / "vue_ensemble.json"
    sortie.write_text(json.dumps(vue, ensure_ascii=False, indent=2), encoding="utf-8")

    # --- Récapitulatif console ---
    print(f"Écrit : {sortie.relative_to(RACINE)}")
    print(f"\ndoute total {totaux['doute_total']} | dans 27 {totaux['doute_dans_27']} "
          f"({totaux['doute_dans_27'] / totaux['doute_total']:.1%}) | "
          f"hors 27 {totaux['doute_hors_27']} | hors monoculture {totaux['doute_hors_monoculture']}")
    print("\nfamille                global   dans27   hors27  niv")
    for f in familles:
        print(f"{f['libelle']:26} {f['global']:6} {f['dans_27']:6} {f['hors_27']:6}   {f['niveau']}")
    print("\nniveau                       global  dans27  global_hors_mono")
    for n in niveaux_vue:
        print(f"{n['niveau']} {n['libelle']:24} {n['global']:6} {n['dans_27']:6} {n['global_hors_monoculture']:6}")
    print(f"\ncopies « d'après » (à part) : {copies['total']} (dont d'après {copies['dont_d_apres']})")


if __name__ == "__main__":
    main()
