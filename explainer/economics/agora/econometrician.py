"""The Island's econometrician (Agora, Part 4): data whose truth is planted, and the estimators that try to find it.

Every dataset here is simulated from parameters in ``explainer.economics.island`` (Part 4's truths), so an
estimator can be graded against the truth rather than against another estimator:

* :func:`fish_season`: a season of the fish market in which feast days shift demand and storms shift supply.  The
  day's price and quantity are where the day's lines cross, so the cloud of (price, quantity) points is neither curve
  (Working 1927).  :func:`simultaneity_slope` gives the probability limit of the least-squares slope.
* :func:`wald` (a binary instrument) and :func:`iv` (two-stage least squares, from statkit's ``quasi.tsls``): weather
  moves supply only, so it identifies demand (Wright 1928).
* :func:`schooling_records`: ability raises both schooling and wages; a school built on one side of the Island moves
  schooling only.  :func:`ols` is biased upward by the omitted-variable formula (:func:`ovb`); the instrument is not.
* :func:`lucas_islands`: output answers only to surprise inflation, with adaptive expectations; the regression of
  output on inflation estimated in calm years breaks when a council tries to exploit it (Lucas 1976).
* :func:`did`: the two-by-two difference in differences (Card and Krueger 1994).

numpy only, with statkit for two-stage least squares; no manim.
"""

from __future__ import annotations

import numpy as np

from explainer.stats.kit import quasi


def fish_season(days: int, a: float, b: float, c: float, d: float, feast=(0.25, 70.0), storm=(0.15, 80.0),
                noise=(12.0, 12.0), seed: int = 0) -> dict:
    """Demand q = a - b p + F f + u, supply q = c + d p - S s + v, with f (feast) and s (storm) Bernoulli and u, v
    normal.  Returns each day's price, quantity, feast and storm flags, and the planted slopes."""
    rng = np.random.default_rng(seed)
    f = (rng.random(days) < feast[0]).astype(float)
    s = (rng.random(days) < storm[0]).astype(float)
    u = rng.normal(0, noise[0], days)
    v = rng.normal(0, noise[1], days)
    dem = a + feast[1] * f + u          # demand intercept of the day
    sup = c - storm[1] * s + v          # supply intercept of the day
    p = (dem - sup) / (b + d)
    q = dem - b * p
    return {"p": p, "q": q, "feast": f, "storm": s, "demand_slope": -b, "supply_slope": d,
            "dem_intercept": dem, "sup_intercept": sup}


def simultaneity_slope(b: float, d: float, var_u: float, var_v: float) -> float:
    """The probability limit of the least-squares slope of q on p when demand shocks have variance var_u and supply
    shocks var_v: (d var_u - b var_v) / (var_u + var_v).  Demand shocks trace supply; supply shocks trace demand."""
    return (d * var_u - b * var_v) / (var_u + var_v)


def ols(y, x) -> dict:
    """Least squares of y on a constant and x (one regressor or several columns): coefficients and classical SEs."""
    y = np.asarray(y, float)
    X = np.column_stack([np.ones(len(y)), np.asarray(x, float)])
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    r = y - X @ beta
    s2 = r @ r / (len(y) - X.shape[1])
    se = np.sqrt(np.diag(s2 * np.linalg.inv(X.T @ X)))
    return {"beta": beta, "se": se, "slope": float(beta[1]), "slope_se": float(se[1])}


def wald(y, x, z) -> dict:
    """The Wald estimator for a binary instrument z: (mean y | z=1 - mean y | z=0) / (mean x | z=1 - mean x | z=0)."""
    y, x, z = (np.asarray(v, float) for v in (y, x, z))
    dy = y[z == 1].mean() - y[z == 0].mean()
    dx = x[z == 1].mean() - x[z == 0].mean()
    return {"estimate": float(dy / dx), "dy": float(dy), "dx": float(dx),
            "means": {"y1": float(y[z == 1].mean()), "y0": float(y[z == 0].mean()),
                      "x1": float(x[z == 1].mean()), "x0": float(x[z == 0].mean())}}


def iv(y, x, z, controls=None) -> dict:
    """Two-stage least squares of y on x with instruments z (statkit's quasi.tsls), and the first-stage F."""
    res = quasi.tsls(np.asarray(y, float), np.asarray(x, float), np.asarray(z, float).reshape(len(y), -1),
                     X=None if controls is None else np.asarray(controls, float))
    F = quasi.first_stage_F(np.asarray(x, float), np.asarray(z, float).reshape(len(y), -1),
                            None if controls is None else np.asarray(controls, float))
    return {"estimate": float(res["beta"]), "se": float(res["se"]), "F": float(F)}


def schooling_records(n: int, base: float, ability_on_school: float, near_school: float, school_noise: float,
                      return_: float, ability_on_wage: float, wage_noise: float, seed: int = 0) -> dict:
    """Islanders' ability (unobserved), whether they grew up near the new school, years of schooling and log wages."""
    rng = np.random.default_rng(seed)
    ability = rng.normal(0, 1, n)
    near = (rng.random(n) < 0.5).astype(float)
    school = base + ability_on_school * ability + near_school * near + rng.normal(0, school_noise, n)
    logw = 1.0 + return_ * school + ability_on_wage * ability + rng.normal(0, wage_noise, n)
    return {"ability": ability, "near": near, "school": school, "logw": logw, "return": return_}


def ovb(gamma: float, cov_sa: float, var_s: float) -> float:
    """The omitted-variable bias of the schooling coefficient: gamma * cov(S, A) / var(S), where gamma is ability's
    effect on log wages."""
    return gamma * cov_sa / var_s


def lucas_islands(ystar: float, b: float, noise: float, lam: float, pi_calm=(2.0, 2.0), pi_push: float = 8.0,
                  years=(30, 20), seed: int = 0) -> dict:
    """Years of calm (inflation pi ~ N(pi_calm)) then years in which the council pushes inflation to pi_push to keep
    output up.  Expected inflation adapts: E_t = E_{t-1} + lam (pi_{t-1} - E_{t-1}).  Output y = y* + b (pi - E) + e."""
    rng = np.random.default_rng(seed)
    T1, T2 = years
    pi = np.concatenate([rng.normal(pi_calm[0], pi_calm[1], T1), pi_push + rng.normal(0, 0.5, T2)])
    E = np.empty_like(pi)
    E[0] = pi_calm[0]
    for t in range(1, len(pi)):
        E[t] = E[t - 1] + lam * (pi[t - 1] - E[t - 1])
    y = ystar + b * (pi - E) + rng.normal(0, noise, len(pi))
    return {"pi": pi, "expected": E, "y": y, "calm": np.arange(len(pi)) < T1, "b": b, "ystar": ystar}


def apprenticeship(n: int, effect: float, select: float, ability_on_wage: float, base: float, wage_noise: float,
                   seed: int) -> dict:
    """One population, two ways of deciding who is treated.  ``chose``: each islander signs up with probability
    logistic(-select * ability), so those with poorer prospects choose the programme; ``lottery``: a fair coin.
    Earnings are log w = base + effect * treated + ability_on_wage * ability + noise, computed for each way.  Returns
    ability, both assignments, both earnings, and each comparison of means with its standard error."""
    rng = np.random.default_rng(seed)
    ability = rng.standard_normal(n)
    noise = rng.normal(0.0, wage_noise, n)
    chose = rng.random(n) < 1.0 / (1.0 + np.exp(select * ability))
    lottery = rng.permutation(np.arange(n) < n // 2)

    def outcome(d):
        return base + effect * d + ability_on_wage * ability + noise

    def compare(y, d):
        a, b = y[d], y[~d]
        return {"diff": float(a.mean() - b.mean()), "se": float(np.sqrt(a.var(ddof=1) / len(a) + b.var(ddof=1) / len(b))),
                "n1": int(d.sum()), "n0": int((~d).sum()), "ability1": float(ability[d].mean()),
                "ability0": float(ability[~d].mean())}

    y_chose, y_lottery = outcome(chose), outcome(lottery)
    return {"ability": ability, "chose": chose, "lottery": lottery, "y_chose": y_chose, "y_lottery": y_lottery,
            "by_choice": compare(y_chose, chose), "by_lottery": compare(y_lottery, lottery), "effect": effect,
            "bias": ability_on_wage * float(ability[chose].mean() - ability[~chose].mean())}


def village_trial(villages: int, per_village: int, saturations, direct: float, spill: float, ability_on_wage: float,
                  base: float, wage_noise: float, village_noise: float, seed: int) -> dict:
    """A two-level randomized trial: each village draws a share from ``saturations`` (equal numbers of villages per
    share), then that share of its people, chosen at random, is treated.  Log earnings are base + direct * treated
    + spill * share + ability_on_wage * ability + village shock + noise.  Returns the people's records and the
    estimates: within-village (treated minus untreated, villages with both), the slope of earnings on the share for
    the untreated, and the total effect of treating everyone against no one."""
    rng = np.random.default_rng(seed)
    sats = np.array(saturations, float)
    share = rng.permutation(np.resize(sats, villages))
    v = np.repeat(np.arange(villages), per_village)
    s = share[v]
    treated = np.zeros(len(v), bool)
    for j in range(villages):
        idx = np.flatnonzero(v == j)
        k = int(round(share[j] * per_village))
        treated[rng.choice(idx, k, replace=False)] = True
    ability = rng.standard_normal(len(v))
    y = (base + direct * treated + spill * s + ability_on_wage * ability + rng.normal(0, village_noise, villages)[v]
         + rng.normal(0, wage_noise, len(v)))
    # within each village that has both, treated minus untreated; then the average over those villages
    diffs = [y[(v == j) & treated].mean() - y[(v == j) & ~treated].mean() for j in range(villages)
             if 0 < share[j] < 1]
    within = float(np.mean(diffs))
    within_se = float(np.std(diffs, ddof=1) / np.sqrt(len(diffs)))
    means = {f"{q:g}": {"treated": float(y[(s == q) & treated].mean()) if ((s == q) & treated).any() else None,
                        "untreated": float(y[(s == q) & ~treated].mean()) if ((s == q) & ~treated).any() else None}
             for q in sats}
    un = ~treated
    spill_hat = ols(y[un], s[un])["slope"]
    total = float(y[s == 1].mean() - y[s == 0].mean())
    return {"village": v, "share": s, "treated": treated, "y": y, "within": within, "within_se": within_se,
            "spill_hat": spill_hat,
            "total": total, "means": means, "truth_total": direct + spill}


def did(before_t: float, after_t: float, before_c: float, after_c: float) -> float:
    """The difference in differences: (treated after - before) - (control after - before)."""
    return (after_t - before_t) - (after_c - before_c)
