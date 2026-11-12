"""Lab 29: mine formulas on a market made of noise, and combine many weak alphas."""

import warnings

import numpy as np

from videos.quant import labs
from explainer.quant.house import alphas

TITLE = "Mining alphas out of noise"
GOAL = ("Generate a market with no predictability at all, search 400 random formulas over it, and compare each "
        "formula's in-sample information coefficient with its out-of-sample one. Then combine K weak but real "
        "alphas and watch estimation error eat the diversification.")
TASKS = [
    "Plant one real signal (add 0.02 x yesterday's rank of volume to tomorrow's return). Does the search find it?",
    "Search 4,000 formulas instead of 400. What happens to the best in-sample IC and to its out-of-sample IC?",
    "In the combination, set known_cov=False. How much more does the estimated covariance cost?",
]


def noise_market(T=260, N=60, seed=0):
    rng = np.random.default_rng(seed)
    ret = rng.normal(0, 0.02, (T, N))
    close = 100 * np.exp(np.cumsum(ret, axis=0))
    spread = np.abs(rng.normal(0, 0.01, (T, N)))
    F = {"close": close, "high": close * (1 + spread), "low": close * (1 - spread), "ret": ret,
         "volume": np.exp(rng.normal(12, 1, (T, N))), "vwap": close * (1 + rng.normal(0, 0.003, (T, N)))}
    fwd = np.vstack([ret[1:], np.full((1, N), np.nan)])  # tomorrow's return, unknown today
    return F, fwd


def run(seed=0):
    F, fwd = noise_market(seed=seed)
    T, N = fwd.shape
    mask = np.ones((T, N), bool)
    train, valid = np.arange(30, 170), np.arange(170, T - 1)
    with warnings.catch_warnings():  # a random formula may be undefined on its first days
        warnings.simplefilter("ignore", RuntimeWarning)
        found = alphas.random_search(F, fwd, mask, train, valid, 400, np.random.default_rng(seed + 1), max_depth=4)
    tr = np.array([a for a, _, _ in found])
    va = np.array([b for _, b, _ in found])
    ok = np.isfinite(tr) & np.isfinite(va)
    tr, va = tr[ok], va[ok]
    best = int(np.argmax(np.abs(tr)))
    name = [s for (_, _, s), keep in zip(found, ok) if keep][best]
    lab = labs.Lab()
    lab.row("Formulas searched", f"{ok.sum()} (of {alphas.count_trees(4)[-1]:.2e} with depth up to 4)")
    lab.row("Best in-sample |IC|", f"{abs(tr[best]):.3f}   formula: {name[:70]}")
    lab.row("The same formula out of sample", f"IC {np.sign(tr[best]) * va[best]:+.3f}")
    top = np.argsort(-np.abs(tr))[:20]
    lab.row("Top 20 in sample: mean |IC|", f"in sample {np.abs(tr[top]).mean():.3f}   out of sample "
                                           f"{np.mean(np.sign(tr[top]) * va[top]):+.3f}")
    sr_star, Tm = 0.25, 120
    Ks = np.array([1, 5, 20, 50, 100, 200])
    rng = np.random.default_rng(seed + 2)
    sim = [alphas.sr_oos_sim(np.full(K, sr_star / np.sqrt(K)), Tm, 300, rng).mean() for K in Ks]
    theory = [alphas.sr_oos_theory(sr_star, int(K), Tm) for K in Ks]
    lab.row("Combining K alphas, total Sharpe fixed", "  ".join(f"K={K}: {s / sr_star:.0%}" for K, s in zip(Ks, sim)))
    lab.note = ("The winner of a search over noise is selected for its luck. And spreading a fixed amount of signal "
                "over more alphas only adds weights to estimate.")
    assert abs(tr[best]) > 0.03 and abs(va[best]) < 0.5 * abs(tr[best])
    assert abs(np.mean(np.sign(tr[top]) * va[top])) < 0.5 * np.abs(tr[top]).mean()
    assert np.allclose(sim, theory, atol=0.035) and sim[-1] < 0.7 * sim[0]

    fig, ax = labs.figure(2, size=(11, 4.2))
    ax[0].scatter(tr, va, s=8, color=labs.SPOT, alpha=0.7)
    ax[0].plot(tr[best], va[best], "o", color=labs.LOSS, ms=8, label="the in-sample winner")
    lim = 1.15 * np.abs(tr).max()
    ax[0].plot([-lim, lim], [-lim, lim], color=labs.MUTED, ls=":", lw=1)
    ax[0].axhline(0, color=labs.MUTED, lw=0.8)
    ax[0].set(title="400 formulas on a market of pure noise", xlabel="in-sample IC", ylabel="out-of-sample IC",
              xlim=(-lim, lim), ylim=(-lim, lim))
    ax[0].legend(fontsize=8)
    ax[1].semilogx(Ks, np.array(sim) / sr_star, "o", color=labs.SPOT, label="simulated")
    grid = np.logspace(0, 2.4, 60)
    ax[1].semilogx(grid, [alphas.sr_oos_theory(sr_star, int(k), Tm) / sr_star for k in grid], color=labs.P,
                   label="SR* / sqrt(1 + K / (T SR*^2))")
    ax[1].set(title="Share of the true Sharpe ratio kept out of sample", xlabel="alphas combined, K", ylim=(0, 1.05))
    ax[1].legend(fontsize=8)
    lab.fig = fig
    return lab
