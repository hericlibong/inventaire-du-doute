// Phrase factuelle sous « Répartition des mentions » (onglet Profil).
//
// UNE règle déterministe, la même pour tous les artistes publiés (cahier des
// charges 2026-07-23). La phrase décrit la FORME du graphique — pas l'ampleur du
// phénomène, qui appartient au bandeau. Elle cite les mentions par leur libellé
// public exact et ne transforme jamais une mention prudente en attribution
// certaine (« portent la mention "attribué à" », jamais « lui sont attribuées »).
//
// Fonction PURE, sans dépendance : le libellé et l'ordre canonique sont injectés.
// Elle se teste ainsi sans bundler (tests/phrase-repartition.test.js).
//   familles : [{ code, notices }] tel quel depuis artistes.json ;
//   total    : nombre d'œuvres concernées de l'artiste (maitre.doute) ;
//   label    : (code) => libellé public de la mention ;
//   ordre    : ordre canonique des codes (départage les égalités, jamais l'ordre
//              accidentel des données).
//
// Seuils (cahier des charges) :
//   — égalité d'effectif en tête : citer les mentions à égalité, au pluriel ;
//   — 1re mention ≥ 60 % : la citer seule ;
//   — sinon 1re + 2e ≥ 70 % ET 2e ≥ 20 % : citer les deux ;
//   — sinon : réparties, sans qu'une seule ne s'impose.
// Tous les pourcentages sont arrondis à l'entier (Math.round).

const NB = ' '; // espace insécable

export function phraseRepartition(familles, total, { label, ordre }) {
	if (!total) return null;

	const rang = (code) => {
		const i = ordre.indexOf(code);
		return i === -1 ? ordre.length : i;
	};
	const items = familles
		.filter((f) => f.notices > 0)
		.map((f) => ({ code: f.code, n: f.notices }))
		.sort((a, b) => b.n - a.n || rang(a.code) - rang(b.code));
	if (!items.length) return null;

	const pct = (n) => Math.round((n / total) * 100);
	const oeuvres = (n) => `${n}${NB}${n === 1 ? 'œuvre' : 'œuvres'}`;
	const men = (code) => `«${NB}${label(code)}${NB}»`;
	const portent = (n) => (n === 1 ? 'porte' : 'portent');

	// 2. Égalité d'effectif en première position : jamais de choix arbitraire.
	const max = items[0].n;
	const tetes = items.filter((i) => i.n === max);
	if (tetes.length > 1) {
		const parts = tetes.map((i, k) =>
			k === 0
				? `${oeuvres(i.n)} concernées portent la mention ${men(i.code)}`
				: `${i.n} la mention ${men(i.code)}`
		);
		// « À égalité, 7 œuvres concernées portent la mention « attribué à » et
		//   7 la mention « à sa manière ». »
		const liste =
			parts.length === 2
				? parts.join(' et ')
				: parts.slice(0, -1).join(', ') + ' et ' + parts.at(-1);
		return `À égalité, ${liste}.`;
	}

	const tete = items[0];

	// 3a. Une mention emporte au moins 60 % : on la cite seule.
	if (pct(tete.n) >= 60) {
		return (
			`${tete.n} des ${total} œuvres concernées portent la mention ${men(tete.code)}${NB}; ` +
			`les autres formulations restent minoritaires.`
		);
	}

	// 3b. Les deux premières réunissent au moins 70 %, la deuxième pèse au moins
	//     20 % : on cite les deux.
	const second = items[1];
	if (second && pct(tete.n + second.n) >= 70 && pct(second.n) >= 20) {
		return (
			`${tete.n} des ${total} œuvres concernées portent la mention ${men(tete.code)}${NB}; ` +
			`${second.n} ${portent(second.n)} la mention ${men(second.code)}.`
		);
	}

	// 3c. Dispersé.
	return 'Les œuvres concernées se répartissent entre plusieurs mentions, sans qu’une seule ne s’impose.';
}
