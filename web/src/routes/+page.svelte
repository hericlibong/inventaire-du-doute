<script>
	let { data } = $props();

	// Chiffre vedette (docs/decisions.md) : le doute seul. On affiche toujours
	// le second dénominateur et le « hors monoculture » à côté, jamais seuls.
	const n = data.niveaux;
	const nombre = (v) => v.toLocaleString('fr-FR');
	const pourcent = (v) => (v * 100).toLocaleString('fr-FR', { maximumFractionDigits: 2 });
</script>

<h1>L'inventaire du doute</h1>
<p class="chapo">
	Combien d'œuvres, dans les musées de France, portent une mention d'incertitude
	sur leur auteur — et sous quelles formules ?
</p>

<section class="vedette">
	<p class="grand-chiffre">{nombre(n.doute_total)}</p>
	<p class="legende">
		notices porteuses d'un doute d'attribution, soit
		{pourcent(n.taux_doute_avec_auteur)} % des notices avec un auteur renseigné
		({pourcent(n.taux_doute_base)} % de toute la base).
	</p>
	<p class="nuance">
		Dont {nombre(n.monoculture_divulguee.doute)} pour un seul musée
		({n.monoculture_divulguee.libelle}). Hors ce cas :
		{nombre(n.doute_hors_monoculture)}.
	</p>
</section>

<p class="provenance">
	Source : {data.provenance.source} — version du {data.provenance.version_donnee},
	{data.provenance.licence}. Détection : {data.provenance.lexique}.
</p>

<style>
	h1 {
		font-family: var(--police-titre);
		font-size: 2.4rem;
		margin-bottom: 0.5rem;
	}

	.chapo {
		font-size: 1.2rem;
		color: var(--couleur-encre-douce);
		max-width: 42rem;
	}

	.vedette {
		margin: 2.5rem 0;
		padding: 1.5rem;
		border-left: 4px solid var(--niveau-1);
		background: rgba(184, 85, 31, 0.05);
	}

	.grand-chiffre {
		font-family: var(--police-titre);
		font-size: 3.5rem;
		font-weight: bold;
		color: var(--niveau-1);
		margin: 0;
		line-height: 1;
	}

	.legende {
		font-size: 1.05rem;
		margin: 0.5rem 0 0;
	}

	.nuance {
		font-size: 0.95rem;
		color: var(--couleur-encre-douce);
		margin: 0.75rem 0 0;
	}

	.provenance {
		font-size: 0.8rem;
		color: var(--couleur-encre-douce);
	}
</style>
