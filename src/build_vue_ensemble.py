"""Export « Vue d'ensemble » des formulations prudentes (dossier « Les presque »).

Produit data/exports/web/vue_ensemble.json à partir des agrégats DÉJÀ validés
(artistes.json + niveaux.json + musees.json) — pas de nouvelle passe sur le CSV
de 1,1 Go : tout est recalculé depuis les exports source de vérité, avec des
`assert` de cohérence.

Message central porté par cette vue (docs/donnees.md 2026-07-15) :
> « Attribué à » reste la formulation la plus fréquente parmi les maîtres
> retenus (43 %), mais « école de » y occupe une place beaucoup plus importante
> que dans l'ensemble de Joconde : 35 % contre 7,6 %. C'est ce contraste qui
> porte la section « Vue d'ensemble » — pas un renversement de hiérarchie.

Les clés se nommaient `dans_27` / `hors_27` : la liste ayant grandi (27, puis 63,
puis 103 au lot du 2026-08-02), elles s'appellent `dans_liste` / `hors_liste`. Un
nom de champ qui fige un effectif devient faux au premier ajout.

Garde-fous méthodologiques (repris du rapport de reconnaissance) :
- Les familles PEUVENT SE RECOUVRIR (une notice porte parfois plusieurs formules)
  → on ne les additionne pas en un tout, et surtout PAS de diagramme en anneau
  pour cette section (contrairement à « Avant / après »).
- Aucun classement PAR NOM hors de la liste : au-dehors, seul le total par
  famille est publiable (les homonymes n'y sont pas désambiguïsés).
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

    # --- Familles DANS la liste : somme des tallies par artiste ---
    # (ce sont des APPARTENANCES : une notice à deux maîtres y compte deux fois)
    dans_liste = {code: 0 for code in FAMILLES}
    for a in artistes["artistes"]:
        for f in a["familles"]:
            if f["code"] in dans_liste:
                dans_liste[f["code"]] += f["notices"]

    # Notices DISTINCTES par famille : mesurées sur le CSV par build_artistes,
    # pas déduites d'une somme de profils (six notices nomment deux maîtres).
    fam_notices = artistes["totaux"]["familles_notices"]

    familles = []
    for code in FAMILLES:
        g = fam_global[code]["notices"]
        d = dans_liste[code]
        n = fam_notices.get(code, 0)
        familles.append({
            "code": code,
            "libelle": fam_global[code]["libelle"],
            "niveau": NIVEAU_FAMILLE[code],
            "global": g,
            # appartenances : ce que totalisent les fiches des maîtres
            "dans_liste": d,
            # notices distinctes : ce qui est comparable au total national
            "dans_liste_notices": n,
            "hors_liste": g - n,
        })
        assert n <= d, f"notices > appartenances pour {code}"
        assert n <= g, f"dans_liste_notices > global pour {code}"

    # --- Niveaux : global, dans la liste, et global hors monoculture ---
    n_global = [niveaux["niveaux"][str(k)]["notices"] for k in (1, 2, 3)]
    n_dans_liste = [sum(a["niveaux"][i] for a in artistes["artistes"]) for i in range(3)]

    mono = niveaux["monoculture_divulguee"]
    musee_mono = next(m for m in musees if m["code_museofile"] == mono["code_museofile"])
    n_mono = musee_mono["niveaux"]  # [5791, 0, 0] : monoculture 100 % niveau 1
    n_hors_mono = [n_global[i] - n_mono[i] for i in range(3)]

    assert sum(n_hors_mono) == niveaux["doute_hors_monoculture"], \
        "niveaux hors monoculture incohérents avec doute_hors_monoculture"

    niv_notices = artistes["totaux"]["niveaux_notices"]
    libelles_niveaux = {int(k): v["libelle"] for k, v in niveaux["niveaux"].items()}
    niveaux_vue = [
        {
            "niveau": k,
            "libelle": libelles_niveaux[k],
            "global": n_global[k - 1],
            "dans_liste": n_dans_liste[k - 1],
            "dans_liste_notices": niv_notices[str(k)],
            "global_hors_monoculture": n_hors_mono[k - 1],
        }
        for k in (1, 2, 3)
    ]

    # --- Totaux : appartenances ET notices distinctes ---
    # Des notices nomment DEUX artistes retenus (artistes.json →
    # references_partagees) : 6 avec les 63 premiers, 157 depuis le lot du
    # 2026-08-02, où les musées nomment souvent deux frères sur la même notice.
    # La somme des profils dépasse donc les références distinctes d'autant.
    # « hors liste » se déduit de l'UNION, jamais de la somme (decisions.md,
    # 2026-07-22 ter).
    app = artistes["totaux"]["appartenances_doute"]
    notices = artistes["totaux"]["notices_doute"]
    assert app == sum(a["doute"] for a in artistes["artistes"]), \
        "appartenances ≠ somme des profils"
    assert app == sum(n_dans_liste), "appartenances incohérentes avec les niveaux"
    assert notices <= app, "union > somme"
    assert notices <= niveaux["doute_total"], "union > doute national"

    totaux = {
        "doute_total": niveaux["doute_total"],
        # ce que totalisent les fiches (un lien maître-notice par ligne)
        "doute_appartenances_liste": app,
        # les références Joconde distinctes : la seule mesure comparable au total
        "doute_notices_liste": notices,
        "doute_notices_partagees": artistes["totaux"]["notices_partagees"],
        "doute_hors_liste": niveaux["doute_total"] - notices,
        "doute_hors_monoculture": niveaux["doute_hors_monoculture"],
    }
    assert totaux["doute_hors_liste"] + notices == totaux["doute_total"], \
        "hors liste + union ≠ total national"

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
        "critere_liste": artistes["critere"],
        # effectif de la liste : lu par « Comprendre les mentions », qui n'a pas
        # à charger artistes.json (372 Ko) pour connaître un nombre
        "nb_maitres": len(artistes["artistes"]),
        "date_generation": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "message_central": (
            "« Attribué à » reste la formulation la plus fréquente parmi les "
            "maîtres retenus, mais « école de » y occupe une place beaucoup "
            "plus importante que dans l'ensemble de Joconde : 35 % contre 7,6 %."
        ),
        "note_methodo": (
            "Les familles peuvent se recouvrir : on ne les additionne pas et on "
            "n'utilise pas de diagramme en anneau. Hors de cette liste, seul le "
            "total par famille est publiable (pas de classement par nom). La "
            "monoculture divulguée (planches Barla, Nice) pèse une large part du "
            "doute national ; « global hors monoculture » permet de la neutraliser. "
            "Deux mesures distinctes pour la liste : les APPARTENANCES (un lien "
            "maître-notice, ce que totalisent les fiches) et les NOTICES "
            "distinctes (les références Joconde, seule mesure comparable au "
            "total national). Six notices nomment deux maîtres retenus : la "
            "somme des fiches vaut donc plus que le nombre d'œuvres. « Hors "
            "liste » est calculé sur les notices, jamais par soustraction d'une "
            "somme d'appartenances."
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
    print(f"\ndoute total {totaux['doute_total']} | notices de la liste "
          f"{totaux['doute_notices_liste']} "
          f"({totaux['doute_notices_liste'] / totaux['doute_total']:.1%}) | "
          f"appartenances {totaux['doute_appartenances_liste']} "
          f"(dont {totaux['doute_notices_partagees']} notices à deux maîtres) | "
          f"hors liste {totaux['doute_hors_liste']} | hors monoculture {totaux['doute_hors_monoculture']}")
    print("\nfamille                global  liste   hors  niv")
    for f in familles:
        print(f"{f['libelle']:26} {f['global']:6} {f['dans_liste']:6} {f['hors_liste']:6}   {f['niveau']}")
    print("\nniveau                       global   liste  global_hors_mono")
    for n in niveaux_vue:
        print(f"{n['niveau']} {n['libelle']:24} {n['global']:6} {n['dans_liste']:6} {n['global_hors_monoculture']:6}")
    print(f"\ncopies « d'après » (à part) : {copies['total']} (dont d'après {copies['dont_d_apres']})")


if __name__ == "__main__":
    main()
