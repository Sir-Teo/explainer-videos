"""Lab 9: twins with the truth planted, a broken assumption, a gene that does nothing, and a genome-wide scan."""

import numpy as np

from videos.coursekit import labs
from explainer.psychology.psyche import genes as G

TITLE = "From twin correlations to a polygenic score, and where each step can mislead"
GOAL = ("Simulate identical and fraternal twins with known shares for genes, the shared home and the rest; recover "
        "the shares with Falconer's formula and by maximum likelihood; break each assumption of the design and "
        "watch the estimate move; check the result against adoption; analyse a gene that does nothing in eighteen "
        "ways; run a genome-wide scan at three sample sizes; and build a polygenic score, test it on new people, "
        "and compare its effect between strangers and between siblings.")
TASKS = [
    "In twin_study, set mz_extra to 0.2, 0.4 and 0.6 and record Falconer's h2. Write the estimate as a formula in "
    "a2, e2 and mz_extra, and say how large mz_extra would have to be for a trait with no genetic variance to "
    "show a 'heritability' of 0.3.",
    "Run the genome-wide scan with 1,000, 4,000 and 16,000 people and, for the hits at each size, compare the "
    "estimated effects with the true ones. Why are the first hits exaggerated, and why does the exaggeration fade?",
    "In sibling_design, set nurture to 0 and strata_gap and strata_env to 1. The population slope is still larger "
    "than the within-family one. What does that say about reading the gap between the two as 'genetic nurture'?",
]


def run(seed=0):
    out = labs.Lab()
    rng = lambda k: np.random.default_rng(seed + k)  # noqa: E731
    true = dict(a2=0.5, c2=0.2, e2=0.3)

    # 1. many small genes
    for L in (1, 5, 50):
        k, p = G.allele_sum(L)
        out.row(f"{L} gene(s): kinds of people; share within one step of the middle", f"{len(k)}; {p[abs(k - L) <= 1].sum():.2f}")
    mid, child = G.midparent_offspring(60_000, 0.6, 0.4, rng(1))
    slope = float(np.polyfit(mid, child, 1)[0])
    out.row("children on their parents' average: slope (planted heritability 0.6)", f"{slope:.2f}")
    assert abs(slope - 0.6) < 0.03

    # 2. twins
    d = G.twin_study(40_000, 40_000, **true, rng=rng(2))
    f = G.falconer(d.r_mz, d.r_dz)
    out.row("twin correlations, identical and fraternal (planted .70 and .45)", f"{d.r_mz:.2f}, {d.r_dz:.2f}")
    out.row("Falconer: genes, shared home, the rest (planted .5, .2, .3)", f"{f['h2']:.2f}, {f['c2']:.2f}, {f['e2']:.2f}")
    one = G.twin_study(1_000, 1_000, **true, rng=rng(3))
    fit = G.ace_fit(one)
    out.row("one study of 1,000 + 1,000 pairs, by maximum likelihood", f"{fit['a2']:.2f}, {fit['c2']:.2f}, {fit['e2']:.2f}")
    out.row("standard error of Falconer's h2 with 50, 200, 1,000, 5,000 pairs of each kind",
            ", ".join(f"{G.falconer_se(0.7, 0.45, n, n):.2f}" for n in (50, 200, 1000, 5000)))
    assert abs(f["h2"] - 0.5) < 0.04 and abs(f["c2"] - 0.2) < 0.04

    # 3. each assumption broken
    cases = [("identical twins treated more alike", dict(true), dict(mz_extra=0.4)),
             ("like marries like", dict(true), dict(assort=0.5)),
             ("genes that do not simply add", dict(a2=0.2, c2=0.1, e2=0.3), dict(d2=0.4)),
             ("parents' genes shape the home", dict(true), dict(rge=0.5))]
    est = {}
    for k, (name, comp, kw) in enumerate(cases):
        t = G.twin_study(40_000, 40_000, **comp, **kw, rng=rng(10 + k))
        est[name] = G.falconer(t.r_mz, t.r_dz)
        out.row(f"{name}: Falconer's genes and home", f"{est[name]['h2']:.2f}, {est[name]['c2']:.2f}")
    ad = G.adoption_study(60_000, **true, rng=rng(20))
    out.row("adoption: adoptive siblings, parent and child apart, identical twins apart",
            f"{ad['adoptive_siblings']:.2f}, {ad['parent_child_apart']:.2f}, {ad['mz_apart']:.2f}")
    assert est["identical twins treated more alike"]["h2"] > 0.65 and est["genes that do not simply add"]["c2"] < 0
    assert abs(ad["mz_apart"] - 0.5) < 0.03

    # 4. what heritability is not
    fields = G.two_fields(20_000, rng=rng(30))
    out.row("two fields: heritability within each; the gap; the genetic part of the gap",
            f"{fields['h2_rich']:.2f}, {fields['h2_poor']:.2f}; {fields['gap']:.1f}; {abs(fields['genetic_gap']):.2f}")
    out.row("pooled heritability of the two fields (0.9 within each)", f"{0.9 / (1 + 1.5 ** 2):.2f}")

    # 5. candidate genes
    out.row("a variant explaining 0.02%: people for 80% power at .05; at 5e-8", f"{G.n_for_r2(0.0002):,}; {G.n_for_r2(0.0002, alpha=5e-8):,}")
    out.row("... the chance of detecting it with 1,000 people", f"{100 * G.power_for_r2(1000, 0.0002):.0f}%")
    g = rng(40)
    studies = [G.candidate_gene_study(800, g) for _ in range(600)]
    planned = np.mean([s["planned"] < 0.05 for s in studies])
    best = np.mean([s["smallest"] < 0.05 for s in studies])
    out.row("a gene that does nothing: studies significant as planned; with the best of 18 analyses",
            f"{100 * planned:.0f}%; {100 * best:.0f}%")
    assert planned < 0.09 and best > 0.25

    # 6. a genome-wide scan and a score
    X = G.simulate_genotypes(12_000, 1_500, rng(50))
    y, beta = G.polygenic_trait(X, 0.5, 300, rng(51))
    line = 0.05 / X.shape[1]
    for n in (1_000, 4_000, 10_000):
        res = G.gwas(X[:n], y[:n])
        hit = res["p"] < line
        out.row(f"{n:,} people: hits of 300 real positions; false hits", f"{int((hit & (beta != 0)).sum())}; {int((hit & (beta == 0)).sum())}")
    res = G.gwas(X[:10_000], y[:10_000])
    score = G.polygenic_score(X[10_000:], res["beta"])
    r2 = float(np.corrcoef(score, y[10_000:])[0, 1] ** 2)
    out.row("a score built on 10,000 people, tested on 2,000 others: variance predicted; the formula",
            f"{100 * r2:.0f}%; {100 * G.expected_r2(10_000, 1_500, 0.5):.0f}%")
    assert abs(r2 - G.expected_r2(10_000, 1_500, 0.5)) < 0.07

    # 7. within and between families; choosing among embryos
    fam = G.sibling_design(200_000, rng(60), direct=0.3, nurture=0.4)
    out.row("a score's effect between strangers and between siblings (direct effect 0.3)",
            f"{fam['population']:.2f}, {fam['within']:.2f}")
    st = G.stratified_association(4_000, rng(61))
    out.row("a variant with no effect in two pooled populations: p pooled; p within each",
            f"{st['pooled']:.0e}; {st['within_a']:.2f}, {st['within_b']:.2f}")
    out.row("expected gain in IQ points from the best of 10 and of 100 embryos (score predicts 3.6% between siblings)",
            f"{G.embryo_gain(10, 0.036):.1f}, {G.embryo_gain(100, 0.036):.1f}")
    assert abs(fam["within"] - 0.3) < 0.02 and st["pooled"] < 1e-8
    out.note = ("Twin correlations give back the planted shares when the design's assumptions hold, slowly: a "
                "heritability known to a tenth needs thousands of pairs. Each assumption that fails moves the "
                "estimate, two of them toward the genes and two toward the home. Heritability belongs to a "
                "population in its environments: pool two fields and it falls from 0.9 to 0.28 with no gene "
                "changed. A variant of realistic size is invisible to a study of a thousand, and a flexible "
                "analysis finds a gene that does nothing a third of the time. A genome-wide scan with a corrected "
                "threshold finds only real positions, and misses most of them. A score predicts new people about "
                "as well as the formula says, and its effect between siblings is the direct one.")

    fig, ax = labs.figure(2, size=(11, 4.2))
    ax[0].scatter(d.mz[:400, 0], d.mz[:400, 1], s=6, color=labs.BLUE, alpha=0.6, label=f"identical, r = {d.r_mz:.2f}")
    ax[0].scatter(d.dz[:400, 0], d.dz[:400, 1], s=6, color=labs.PINK, alpha=0.6, label=f"fraternal, r = {d.r_dz:.2f}")
    ax[0].set(title="Twin pairs with planted shares .5, .2, .3", xlabel="one twin", ylabel="the other twin")
    ax[0].legend(loc="upper left", fontsize=8)
    lp = -np.log10(np.maximum(res["p"], 1e-300))
    cols = np.where(beta != 0, labs.GREEN, labs.GREY)
    ax[1].scatter(np.arange(len(lp)), np.minimum(lp, 40), s=4, c=cols)
    ax[1].axhline(-np.log10(line), color=labs.PINK, lw=1.2, ls="--")
    ax[1].set(title="A scan of 1,500 positions in 10,000 people (green: real)", xlabel="position",
              ylabel="-log10 p")
    out.fig = fig
    return out
