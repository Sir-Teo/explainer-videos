"""Precompute every number in Part 15 of *Statistics, Built* ("First Bayes").

    python -m videos.stats.stats15.compute            # everything missing (a few minutes)
    python -m videos.stats.stats15.compute --force board

Results are cached in ``.cache/stats15/<name>.json``.  The Paris births, the horse kicks and the Challenger flights are
the Museum's; heights are the World's (seed 1662); the billiard table is a seeded simulation.

Items:
    billiard    Bayes's table: a hidden ball and twelve more; the posterior after each
    laplace     Paris baptisms 1745-1770: P(p <= 1/2 | data); the rule of succession and the sunrise
    conjugate   beta-binomial, gamma-Poisson (the horse kicks), normal-normal (a guess about heights)
    summaries   a skewed posterior: mean, median, mode, equal-tailed and HPD intervals
    predictive  the beta-binomial predictive vs the plug-in binomial
    priors      four priors, at n = 10 and n = 100; a flat prior on p is not flat on the odds
    normalt     eight of the World's adults: the reference posterior is Part 8's t-interval
    grid        the Challenger logistic posterior on a 2-D grid; the posterior of p(31 F)
    mcmc        the same posterior by Metropolis: three step sizes, traces, acceptance, ESS
    bf          Bayes factors vs p-values at fixed z = 1.96 (Lindley's warning, first look)
    board       Coverage Board rows: credible intervals at fixed theta, right and wrong priors
"""

from __future__ import annotations

from dataclasses import asdict

import numpy as np
from scipy import special, stats

from explainer.ai.cache import Cache
from explainer.stats import museum
from explainer.stats.board import Row, save_rows
from explainer.stats.kit import bayes as B
from explainer.stats.world import World

CACHE = Cache("stats15")
load = CACHE.load
W = World()
R_BOARD = 10_000


def rng(seed: int) -> np.random.Generator:
    return np.random.Generator(np.random.PCG64(seed))


def nest(obj):
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    if isinstance(obj, dict):
        return {str(k): nest(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [nest(v) for v in obj]
    if isinstance(obj, (np.floating, np.integer)):
        return obj.item()
    if isinstance(obj, np.bool_):
        return bool(obj)
    return obj


def compute_billiard():
    g = rng(1788)  # a representative draw: the posterior mean lands near the hidden ball
    u0 = float(g.uniform(0.2, 0.8))
    balls = g.random((12, 2))
    left = balls[:, 0] < u0
    s = np.cumsum(left)
    n = np.arange(1, 13)
    post = [(1 + int(si), 1 + int(ni - si)) for si, ni in zip(s, n)]
    a, b = post[-1]
    d = stats.beta(a, b)
    return nest({"u0": u0, "balls": balls, "left": left, "post": post, "mean": d.mean(), "ci": B.credible(d),
                 "p_between": float(d.cdf(0.5) - d.cdf(0.2))})


def compute_laplace():
    pb = museum.PARIS_BIRTHS
    a, b = pb["boys"] + 1, pb["girls"] + 1
    d = stats.beta(a, b)
    # P(p <= 1/2) via the normal approximation on the log scale (the exact tail underflows double precision's cdf)
    m, sd = d.mean(), d.std()
    z = (0.5 - m) / sd
    logp = stats.norm.logcdf(z)
    exact = float(special.betainc(a, b, 0.5))
    days = 1_826_213
    return nest({"a": a, "b": b, "mean": m, "sd": sd, "ci": B.credible(d), "z": z, "log10_p": logp / np.log(10), "exact": exact,
                 "share_boys": pb["boys"] / (pb["boys"] + pb["girls"]), "days": days, "sunrise": B.rule_of_succession(days, days)})


def compute_conjugate():
    bb = {"prior": (2, 2), "data": (7, 3), "post": B.beta_update(2, 2, 7, 3)}
    deaths = int(np.dot(museum.HORSEKICK_K, museum.HORSEKICK_N))
    years = int(np.sum(museum.HORSEKICK_N))
    gp = {"prior": (1.0, 1.0), "data": (deaths, years), "post": B.gamma_update(1.0, 1.0, deaths, years)}
    sh, rt = gp["post"]
    gd = stats.gamma(sh, scale=1 / rt)
    idx = W.sample(10, among=W.adult, seed=15)
    h = W.height[idx]
    m, s = B.normal_update(170.0, 10.0, float(h.mean()), 9.0, 10)
    return nest({"bb": bb, "bb_mean": bb["post"][0] / sum(bb["post"]), "bb_ci": B.credible(stats.beta(*bb["post"])),
                 "gp": gp, "gp_mean": gd.mean(), "gp_ci": B.credible(gd), "kicks_mle": deaths / years,
                 "nn": {"prior": (170.0, 10.0), "xbar": float(h.mean()), "sigma": 9.0, "n": 10, "post": (m, s)},
                 "heights": h, "truth": W.truth("mean_height"), "w_data": (10 / 81) / (10 / 81 + 1 / 100)})


def compute_summaries():
    d = stats.beta(3, 12)
    return nest({"a": 3, "b": 12, "mean": d.mean(), "median": d.median(), "mode": 2 / 13, "et": B.credible(d), "hpd": B.hpd(d)})


def compute_predictive():
    a, b = 9, 5
    k = np.arange(11)
    pred = B.beta_binomial_pmf(k, 10, a, b)
    plug = stats.binom.pmf(k, 10, 7 / 10)
    return nest({"k": k, "pred": pred, "plug": plug, "pred_sd": float(np.sqrt(np.sum(pred * k ** 2) - np.sum(pred * k) ** 2)),
                 "plug_sd": float(np.sqrt(10 * 0.7 * 0.3))})


def compute_priors():
    priors = {"uniform": (1, 1), "Jeffreys": (0.5, 0.5), "sceptic": (20, 20), "pessimist": (2, 8)}
    out = {}
    for n, s in ((10, 7), (100, 70)):
        out[n] = {k: {"mean": (a + s) / (a + b + n), "ci": B.credible(stats.beta(a + s, b + n - s))} for k, (a, b) in priors.items()}
    # a flat prior on p, pushed to the odds p/(1-p): density 1/(1+o)^2
    o = np.linspace(0, 10, 400)
    return nest({"priors": priors, "post": out, "odds": o, "odds_density": 1 / (1 + o) ** 2})


def compute_normalt():
    idx = W.sample(8, among=W.adult, seed=158)
    x = W.height[idx]
    r = B.normal_unknown_var(x)
    t = stats.t(r["df"], loc=r["loc"], scale=r["scale"])
    return nest({"x": x, "post": r, "ci": B.credible(t), "t_ci": stats.t.interval(0.95, 7, loc=x.mean(), scale=stats.sem(x)),
                 "truth": W.truth("mean_height")})


T = np.asarray(museum.CHALLENGER_TEMP, float)
Y = (np.asarray(museum.CHALLENGER_DISTRESS) > 0).astype(float)


def challenger_logpost(b0, b1):
    eta = b0[..., None] + b1[..., None] * T
    return np.sum(Y * eta - np.logaddexp(0.0, eta), axis=-1)


def compute_grid():
    gx = np.linspace(-5, 45, 251)
    gy = np.linspace(-0.7, 0.1, 241)
    dens, mx, my = B.grid_posterior_2d(gx, gy, challenger_logpost)
    # the posterior of p(31): sample grid cells by weight
    g = rng(31)
    w = dens.ravel() / dens.sum()
    pick = g.choice(len(w), 20_000, p=w)
    X, Yg = np.meshgrid(gx, gy)
    b0s = X.ravel()[pick] + g.uniform(-0.1, 0.1, 20_000)
    b1s = Yg.ravel()[pick] + g.uniform(-0.0017, 0.0017, 20_000)
    p31 = special.expit(b0s + 31 * b1s)
    return nest({"gx": gx, "gy": gy, "dens": dens[::4, ::4], "gx4": gx[::4], "gy4": gy[::4], "mx": mx, "my": my,
                 "b1_mean": float(np.trapezoid(my * gy, gy)), "p31_median": float(np.median(p31)), "p31_lo": float(np.quantile(p31, 0.025)),
                 "p_gt_09": float(np.mean(p31 > 0.9)), "p_b1_neg": float(np.trapezoid(my[gy < 0], gy[gy < 0])),
                 "p31_hist": np.histogram(p31, bins=40, range=(0, 1))[0], "cells": int(dens.size)})


def challenger_logpost_c(a, b):
    """The same posterior with temperature centred at 70 F: a = logit p(70), b the slope."""
    eta = a[..., None] + b[..., None] * (T - 70)
    return np.sum(Y * eta - np.logaddexp(0.0, eta), axis=-1)


def compute_mcmc():
    lp = lambda th: float(challenger_logpost(np.array(th[0]), np.array(th[1])))  # noqa: E731
    lpc = lambda th: float(challenger_logpost_c(np.array(th[0]), np.array(th[1])))  # noqa: E731
    out = {}
    for name, step in (("tiny", (0.05, 0.005)), ("good", (1.0, 0.1)), ("huge", (10.0, 1.0))):
        ch = B.metropolis(lpc, [-1.2, -0.23], step, 6000, rng(1953))
        out[name] = {"b1": ch.draws[:, 1], "acc": ch.acceptance, "ess": B.ess(ch.draws[1000:, 1])}
    raw = B.metropolis(lp, [15.0, -0.23], (1.0, 0.1), 6000, rng(1953))
    rawg = B.metropolis(lp, [15.0, -0.23], (4.0, 0.06), 6000, rng(1953))
    full = B.metropolis(lpc, [0.0, 0.0], (1.0, 0.1), 20_000, rng(1954))
    b = full.draws[2000:]
    p31 = special.expit(b[:, 0] + (31 - 70) * b[:, 1])
    return nest({"chains": {k: {"b1": v["b1"][:1500], "acc": v["acc"], "ess": v["ess"]} for k, v in out.items()},
                 "raw": {"b1": rawg.draws[:1500, 1], "acc": rawg.acceptance, "ess": B.ess(rawg.draws[1000:, 1]),
                         "acc_same_step": raw.acceptance},
                 "start0_trace": full.draws[:600, 1], "full_mean": float(b[:, 1].mean()), "full_sd": float(b[:, 1].std()),
                 "p31_median": float(np.median(p31)), "p31_lo": float(np.quantile(p31, 0.025)), "p_gt_09": float(np.mean(p31 > 0.9)),
                 "acc": full.acceptance, "ess": B.ess(b[:, 1]), "n": len(b), "b1_draws": b[::20, 1], "a_draws": b[::20, 0]})


def compute_bf():
    rows = []
    for n in (100, 1000, 10_000, 100_000):
        s = int(round(n / 2 + 1.96 * np.sqrt(n) / 2))
        p = 2 * stats.binom.sf(s - 1, n, 0.5)
        rows.append({"n": n, "s": s, "p": float(p), "bf10": B.bayes_factor_binomial(s, n)})
    bf60 = B.bayes_factor_binomial(60, 100)
    return nest({"rows": rows, "bf60": bf60, "p60": float(2 * stats.binom.sf(59, 100, 0.5))})


def compute_board():
    g = rng(15_000)
    n = 50
    res = {}

    def cover(p_true, a, b, draw_prior=False):
        hits = 0
        for _ in range(R_BOARD):
            p = g.beta(a, b) if draw_prior else p_true
            s = g.binomial(n, p)
            lo, hi = stats.beta.ppf([0.025, 0.975], a + s, b + n - s)
            hits += lo <= p <= hi
        return hits / R_BOARD

    res["jeff"] = cover(0.05, 0.5, 0.5)
    res["unif"] = cover(0.05, 1, 1)
    res["wrong"] = cover(0.05, 18, 2)
    res["right"] = cover(0.9, 18, 2)
    res["drawn"] = cover(None, 18, 2, draw_prior=True)
    hits = 0
    for _ in range(R_BOARD):
        x = W.height[W.sample(10, among=W.adult, seed=int(g.integers(1 << 30)))]
        r = B.normal_unknown_var(x)
        lo, hi = stats.t.interval(0.95, r["df"], loc=r["loc"], scale=r["scale"])
        hits += lo <= W.truth("mean_height") <= hi
    res["normal"] = hits / R_BOARD
    bs = r"binomial, \ $n = 50$"
    rows = [
        Row(15, r"credible, \ Jeffreys prior", bs + r", \ $p = 0.05$", "coverage", 0.95, res["jeff"], R_BOARD),
        Row(15, r"credible, \ uniform prior", bs + r", \ $p = 0.05$", "coverage", 0.95, res["unif"], R_BOARD),
        Row(15, r"credible, \ Beta(18, 2) prior", bs + r", \ $p = 0.05$", "coverage", 0.95, res["wrong"], R_BOARD),
        Row(15, r"credible, \ Beta(18, 2) prior", bs + r", \ $p = 0.9$", "coverage", 0.95, res["right"], R_BOARD),
        Row(15, r"credible, \ Beta(18, 2) prior", bs + r", \ $p \sim$ the prior", "coverage", 0.95, res["drawn"], R_BOARD),
        Row(15, r"credible, \ reference prior", r"the World's heights, \ $n = 10$", "coverage", 0.95, res["normal"], R_BOARD),
    ]
    save_rows(15, rows)
    return {"rows": [asdict(r) | {"verdict": r.verdict, "se": r.se} for r in rows]}


ITEMS = {
    "billiard": compute_billiard, "laplace": compute_laplace, "conjugate": compute_conjugate, "summaries": compute_summaries,
    "predictive": compute_predictive, "priors": compute_priors, "normalt": compute_normalt, "grid": compute_grid,
    "mcmc": compute_mcmc, "bf": compute_bf, "board": compute_board,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
