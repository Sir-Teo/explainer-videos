"""Lab 3: keep the Island's books three ways, invert Leontief's table, price Bo's baskets, and test a hedonic index."""

import numpy as np

from videos.coursekit import labs
from explainer.economics.agora import accounts as acc
from explainer.economics.agora import indices as ix
from explainer.economics.island import truths

TITLE = "The measure: GDP three ways, price indexes and their biases"
GOAL = ("Build the Island's input-output table, check that GDP is the same by output, spending and income, and invert "
        "the table to find how much every industry must produce for $10 more exports. Then price Bo's two baskets "
        "with Laspeyres, Paasche and Fisher against the true cost of living, for tastes from no substitution at all "
        "to easy substitution; chain the indexes over stormy and calm seasons; and run the boatyard's hedonic "
        "regression on many simulated years to see how often its interval covers the planted price change.")
TASKS = [
    "Give Bo tastes with no substitution at all (sigma = 0). Show that Laspeyres, Paasche and the true index "
    "coincide, and that chain drift disappears. Why?",
    "Move $20 of the grove's exports to the council (G up, X down). Recompute saving, investment and the trade "
    "balance, and check S = I + (X - M).",
    "Leave length out of the hedonic regression. How often does the 95% interval for the 'pure' price change cover "
    "the planted 3%? What does that say about an index that ignores quality?",
]


def ces_indexes(r, s0, sigma):
    """Price relatives r, base expenditure shares s0, elasticity of substitution sigma: Laspeyres, Paasche, Fisher
    and the exact cost-of-living index of a CES (homothetic) consumer."""
    r, s0 = np.asarray(r, float), np.asarray(s0, float)
    if abs(sigma - 1) < 1e-9:
        s1 = s0.copy()
        true = float(np.exp(s0 @ np.log(r)))
    else:
        w = s0 * r ** (1 - sigma)
        s1 = w / w.sum()
        true = float((s0 @ r ** (1 - sigma)) ** (1 / (1 - sigma)))
    L = float(s0 @ r)
    P = float(1 / (s1 @ (1 / r)))
    return {"laspeyres": L, "paasche": P, "fisher": float(np.sqrt(L * P)), "true": true}


def run(seed=0):
    lab = labs.Lab()
    t3 = truths(3)

    # GDP three ways, and the identities
    t = acc.IOTable(**t3["accounts"])
    t.check()
    g = t.gdp()
    e = t.expenditure()
    lab.row("the Island's GDP: output / spending / income", f"${g['output']:.0f} / ${g['expenditure']:.0f} / "
                                                           f"${g['income']:.0f}")
    S = g["output"] - e["C"] - e["G"]
    assert abs(S - (e["I"] + e["X"] - e["M"])) < 1e-9
    lab.row("saving = investment + net exports", f"{S:.0f} = {e['I']:.0f} + ({e['X'] - e['M']:.0f})")

    # Leontief: the inverse equals the sum of the rounds
    A = t.coefficients()
    L = t.leontief()
    f = np.array([10.0, 0, 0, 0])
    rounds = [f]
    for _ in range(40):
        rounds.append(A @ rounds[-1])
    assert np.allclose(np.sum(rounds, axis=0), L @ f, atol=1e-9)
    lab.row("$10 more fish exports: extra output by industry", ", ".join(f"{x:.2f}" for x in L @ f))
    lab.row("output multipliers", ", ".join(f"{x:.3f}" for x in L.sum(axis=0)))
    lab.row("domestic value added in exports", f"{100 * t.value_added_in('X')['share']:.1f}%")

    # Bo's baskets across tastes: P <= true <= L, and Fisher close
    b = t3["basket"]
    r = np.array(b["storm"]) / np.array(b["calm"])
    s0 = np.array(b["shares"])
    sigmas = np.linspace(0, 2, 21)
    res = [ces_indexes(r, s0, sg) for sg in sigmas]
    for x in res:
        assert x["paasche"] - 1e-12 <= x["true"] <= x["laspeyres"] + 1e-12
    worst = max(abs(x["fisher"] - x["true"]) / x["true"] for x in res)
    cd = ces_indexes(r, s0, 1.0)
    lab.row("Bo, half and half, fish x2: L / P / F / true", f"{cd['laspeyres']:.3f} / {cd['paasche']:.3f} / "
                                                          f"{cd['fisher']:.4f} / {cd['true']:.4f}")
    lab.row("Fisher's largest error, sigma from 0 to 2", f"{100 * worst:.2f}%")

    # chain drift with Cobb-Douglas tastes (agora.indices)
    n = b["seasons"]
    prices = np.array([b["calm"] if k % 2 == 0 else b["storm"] for k in range(n + 1)], float)
    qs = np.array([ix.cobb_douglas_demand(p, b["income"], s0) for p in prices])
    drift = ix.chain_drift(prices, qs)
    lab.row(f"after {n} seasons (prices back where they began)", ", ".join(f"{k} {v:.3f}" for k, v in drift.items()))
    assert drift["laspeyres"] > 1.5 and drift["paasche"] < 0.7 and abs(drift["fisher"] - 1) < 1e-9

    # hedonic regression: coverage of the 95% interval over many simulated years
    h = t3["boats"]
    rng = np.random.default_rng(1000 + seed)
    est, cover, naive = [], 0, []
    reps = 400
    for _ in range(reps):
        yr, Ls, Ps = [], [], []
        for year in (0, 1):
            mu, sd = h["length"][year]
            ln = np.clip(rng.normal(mu, sd, h["n"]), 3.5, 8.0)
            pr = h["A"] * ln ** h["B"] * (1 + h["inflation"]) ** year * np.exp(rng.normal(0, h["noise"], h["n"]))
            yr += [year] * h["n"]
            Ls += list(ln)
            Ps += list(pr)
        yr, Ls, Ps = np.array(yr, float), np.array(Ls), np.array(Ps)
        X = np.column_stack([np.ones_like(Ls), np.log(Ls), yr])
        beta, *_ = np.linalg.lstsq(X, np.log(Ps), rcond=None)
        res_ = np.log(Ps) - X @ beta
        se = np.sqrt(res_ @ res_ / (len(Ps) - 3) * np.linalg.inv(X.T @ X)[2, 2])
        truth = np.log(1 + h["inflation"])
        cover += abs(beta[2] - truth) <= 1.96 * se
        est.append(np.exp(beta[2]) - 1)
        naive.append(Ps[yr == 1].mean() / Ps[yr == 0].mean() - 1)
    lab.row("hedonic pure price change: mean of 400 years", f"{100 * np.mean(est):.2f}% (planted "
                                                            f"{100 * h['inflation']:.0f}%)")
    lab.row("95% interval covers the truth", f"{100 * cover / reps:.1f}% of years")
    lab.row("average price change, ignoring quality", f"{100 * np.mean(naive):.1f}%")
    assert abs(np.mean(est) - h["inflation"]) < 0.005 and 0.9 < cover / reps < 0.99

    # the Gini of a list of incomes
    hh = t3["households"]
    rng = np.random.default_rng(hh["seed"])
    w = np.exp(rng.normal(0, hh["wage_sigma"], hh["n"] - 2))
    inc = np.concatenate([w / w.sum() * t.wages.sum(), [hh["friday"], hh["crusoe"]]])
    srt = np.sort(inc)
    gini = (2 * np.arange(1, len(srt) + 1) - len(srt) - 1) @ srt / (len(srt) * srt.sum())
    pairs = np.abs(inc[:, None] - inc[None, :]).sum() / (2 * len(inc) ** 2 * inc.mean())
    assert abs(gini - pairs) < 1e-12
    lab.row("Gini of wages plus the two owners' profits", f"{gini:.3f}")
    lab.note = ("The three measures of GDP agree by bookkeeping; Leontief's inverse is the sum of the rounds; for any "
                "homothetic consumer the truth lies between Paasche and Laspeyres, and Fisher stays within 1% "
                "of it; a regression that holds quality fixed finds the planted price change.")

    fig, ax = labs.figure(2, size=(11, 4.2))
    ax[0].plot(sigmas, [x["laspeyres"] for x in res], color=labs.ORANGE, lw=2.2, label="Laspeyres")
    ax[0].plot(sigmas, [x["paasche"] for x in res], color=labs.BLUE, lw=2.2, label="Paasche")
    ax[0].plot(sigmas, [x["fisher"] for x in res], color=labs.GREY, lw=2.2, ls="--", label="Fisher")
    ax[0].plot(sigmas, [x["true"] for x in res], color="#7BD88F", lw=2.6, label="true cost of living")
    ax[0].set(title="Fish doubles: how much dearer is living?", xlabel="elasticity of substitution", ylabel="index")
    ax[0].legend()
    ax[1].hist(100 * np.array(est), bins=30, color=labs.ORANGE, alpha=0.8, label="hedonic")
    ax[1].hist(100 * np.array(naive), bins=30, color=labs.GREY, alpha=0.6, label="average price")
    ax[1].axvline(100 * h["inflation"], color="#7BD88F", lw=2, label="planted")
    ax[1].set(title="The boatyard, 400 simulated years", xlabel="estimated price change, %", ylabel="years")
    ax[1].legend()
    lab.fig = fig
    return lab
