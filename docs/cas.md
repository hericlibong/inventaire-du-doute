# Cas racontables — matière narrative (P2-T4)

Cas sélectionnés pour la restitution, tous fondés sur des notices publiques
(Joconde, ou base régionale de Normandie pour Alençon — citée comme
illustration, jamais comptée). Le projet lit et restitue ; il n'authentifie
rien, ne parle pas de valeur, ne verse pas dans le sensationnalisme.

Lien notice Joconde : `https://pop.culture.gouv.fr/notice/joconde/{reference}`

---

## Cas 1 — Alençon, l'absent (OUVERTURE)

**Angle** : le cas qui a inspiré ce projet est lui-même invisible dans
l'inventaire national. Le musée des beaux-arts et de la dentelle d'Alençon
(M0694) n'a versé dans Joconde que sa collection de dentelle — 109 notices,
~6 relèvent des beaux-arts, aucun des tableaux liés à Géricault. Vérifié et
confirmé par l'API du ministère (docs/donnees.md).

**Les œuvres existent** — dans la base régionale des musées de Normandie
(système distinct, non agrégé à Joconde) :
- « tête de gorgone » : collections.musees-normandie.fr/ark:/16418/mbd1160142
- « le naufragé » : collections.musees-normandie.fr/ark:/16418/mbd1160140

**Ce que ça montre** : la limite centrale du projet, incarnée par son propre
point de départ — « les chiffres ne reflètent que ce qui a été versé ». On
ouvre en montrant un trou, pas une découverte. La logique du trou est même
lisible : Alençon est mondialement connu pour son Point d'Alençon (dentelle,
UNESCO) ; le musée a versé sa collection phare, pas encore ses peintures.

**Statut donnée** : absent de Joconde. Illustration via base régionale.

---

## Cas 2 — Nice, le doute industriel

**Angle** : à quoi ressemble le doute quand il est produit en série. Le muséum
d'histoire naturelle de Nice (M7050) porte 5 791 notices « en doute » — plus
que le Louvre — mais ce sont **toutes le même geste** : `Barla Jean-Baptiste
(attribué à)` sur des planches naturalistes (mycologie, botanique, faune).

**Exemple** : notice 70500001179, « cnidaire », auteur « Barla Jean-Baptiste
(1817-1896) (attribué à) ». Une parmi 5 791 quasi identiques.

**Ce que ça montre** : « attribué à » n'est pas toujours un mystère d'histoire
de l'art — ici c'est une mention de catalogage appliquée en masse à un fonds
d'un seul dessinateur. À lui seul, ce cas = 23,6 % du doute national : d'où la
règle de ne jamais classer les musées sur des comptages bruts, et de divulguer
le chiffre « hors ce cas » (18 716). L'envers du décor du mot « attribué à ».

**Statut donnée** : Joconde, réel. Monoculture divulguée (voir niveaux.json).

---

## Cas 3 — Besançon, le doute qui existe vraiment (miroir d'Alençon)

**Angle** : le doute « à la Géricault » que le projet cherche existe bel et
bien dans Joconde — au musée des beaux-arts et d'archéologie de Besançon
(M0332), qui conserve un riche fonds Géricault autour du cycle du Radeau de la
Méduse, avec toute la gradation du doute visible d'une notice à l'autre :

- **Certitude** : 000PE… non — M0332014262, « Deux études pour Le Radeau de la
  Méduse » — auteur « Géricault Théodore (1791-1824) », sans réserve.
- **Doute** : M0332013239, « Etude d'un cheval mort » — « Géricault
  (attribué à) ». Même musée, même artiste, même thème : l'un est donné, l'autre
  supposé.
- Autour, des « genre de » et « d'après » Géricault (copies et pastiches).

**Ce que ça montre** : dans un seul fonds, on lit l'échelle entière — de « c'est
lui » à « c'est peut-être lui » à « c'est à sa manière ». Miroir exact
d'Alençon : ce qu'Alençon aurait pu montrer s'il avait versé ses beaux-arts.

**Statut donnée** : Joconde, réel et détecté.

---

## Cas 4 — Le Louvre, l'archéologie d'un doute (doute + révision)

**Angle** : l'objet le plus riche du projet — les notices qui cumulent un doute
actuel ET la trace écrite des attributions passées (4 615 notices, P2-T1). Au
Louvre, le champ « ancienne attribution » se lit comme un journal d'avis
savants datés.

**Exemple** : notice 000PE000505, « Pierre Forget, seigneur de Fresnes
(1544-1610) ».
- Auteur aujourd'hui : « CLOUET François (atelier) » — niveau 2 de l'échelle,
  l'entourage du maître.
- Ancienne attribution : « CLOUET FRANCOIS (attribué en 1904) ; DECOURT LE
  PRESUME JEAN (DIMIER II) » — on lit littéralement le changement d'avis, avec
  la date (1904) et le nom des catalogueurs (Dimier).

Autre : 000PE000509, « Portrait de femme inconnue » — « Clouet (atelier)
aujourd'hui, jadis « École française 2e moitié 16e siècle » (Brière), puis
« Anonyme Lecurieux » (Dimier).

**Ce que ça montre** : l'attribution est une histoire, pas un verdict. Les
musées écrivent noir sur blanc non seulement ce qu'ils ne savent pas, mais ce
qu'ils ont cru savoir. C'est le cœur savant du sujet.

**Statut donnée** : Joconde, réel et détecté (doute + révision).

---

## Cas complémentaires possibles (à arbitrer, P2-T4f)

Un exemple net par niveau de l'échelle, si le récit en a besoin — à puiser dans
les familles déjà fiables (attribué à, école de, manière de). Non bloquant.
