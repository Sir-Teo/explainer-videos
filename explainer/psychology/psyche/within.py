"""Psyche over time and within persons (Part 47): when a finding about people is a finding about a person.

The language-as-fixed-effect fallacy as a simulation (participants and items both sampled; by-participant tests
against crossed random effects, fitted with *Statistics, Built*'s ``statkit.mixed``), power as a function of the
number of stimuli, shrinkage of person-level slopes, Simpson's paradox inside a person (between and within
slopes of opposite sign, separated by person-mean centring), a population built to be non-ergodic (group
correlations unlike any individual's), experience-sampling autoregression with its small-T bias, and critical
slowing down before a transition in a double-well system, with its false alarms.  numpy and scipy only, plus
statkit.
"""

from __future__ import annotations

import numpy as np
from scipy import stats

from explainer.stats.kit.mixed import lmm, vc_lmm


# ----------------------------------------------------------------------------------------------------------------
# Items are a sample too
# ----------------------------------------------------------------------------------------------------------------
def priming_study(n_subj: int = 30, n_items: int = 20, effect: float = 0.0, subj_sd: float = 0.5,
                  item_sd: float = 0.5, slope_sd: float = 0.0, noise: float = 1.0, seed: int = 0) -> dict:
    """A priming experiment: every participant sees every item once; half the items are 'related', half
    'unrelated' (items nested in condition).  Response = effect x related + participant + item + noise, with an
    optional participant-specific effect (slope_sd).  Returns long-format arrays."""
    rng = np.random.default_rng(seed)
    subj = np.repeat(np.arange(n_subj), n_items)
    item = np.tile(np.arange(n_items), n_subj)
    cond = (item < n_items // 2).astype(float)
    u = rng.normal(0, subj_sd, n_subj)
    s = rng.normal(0, slope_sd, n_subj)
    w = rng.normal(0, item_sd, n_items)
    y = (effect + s[subj]) * cond + u[subj] + w[item] + rng.normal(0, noise, len(subj))
    return {"y": y, "subj": subj, "item": item, "cond": cond}


def by_subject_test(d: dict) -> float:
    """The traditional F1 analysis: each participant's mean in each condition, then a paired t-test across
    participants; items are treated as fixed."""
    n = d["subj"].max() + 1
    m1 = np.array([d["y"][(d["subj"] == i) & (d["cond"] == 1)].mean() for i in range(n)])
    m0 = np.array([d["y"][(d["subj"] == i) & (d["cond"] == 0)].mean() for i in range(n)])
    return float(stats.ttest_rel(m1, m0).pvalue)


def by_item_test(d: dict) -> float:
    """The F2 analysis: each item's mean over participants, then a two-sample t-test between conditions."""
    k = d["item"].max() + 1
    mi = np.array([d["y"][d["item"] == j].mean() for j in range(k)])
    ci = np.array([d["cond"][d["item"] == j][0] for j in range(k)])
    return float(stats.ttest_ind(mi[ci == 1], mi[ci == 0]).pvalue)


def crossed_test(d: dict) -> dict:
    """Crossed random intercepts for participants and items (statkit's ``vc_lmm``, REML); the condition effect
    tested with a t on (items - 2) degrees of freedom, since the effect varies only between items."""
    X = np.column_stack([np.ones(len(d["y"])), d["cond"]])
    f = vc_lmm(d["y"], X, {"subj": d["subj"], "item": d["item"]})
    se = float(np.sqrt(f["cov_beta"][1, 1]))
    df = int(d["item"].max() + 1) - 2
    t = float(f["beta"][1] / se)
    return {"est": float(f["beta"][1]), "se": se, "p": float(2 * stats.t.sf(abs(t), df)), "var": f["var"],
            "sigma2": f["sigma2"]}


def min_f_test(d: dict) -> dict:
    """Clark's (1973) min F': both participants and items treated as random, from the two ordinary analyses:
    min F' = F1 F2 / (F1 + F2) on (1, (F1 + F2)^2 / (F1^2/df2 + F2^2/df1)) degrees of freedom.  Fast, a little
    conservative; for this balanced design a crossed mixed model (``crossed_test``) agrees closely."""
    n = d["subj"].max() + 1
    m1 = np.array([d["y"][(d["subj"] == i) & (d["cond"] == 1)].mean() for i in range(n)])
    m0 = np.array([d["y"][(d["subj"] == i) & (d["cond"] == 0)].mean() for i in range(n)])
    t1 = stats.ttest_rel(m1, m0).statistic
    k = d["item"].max() + 1
    mi = np.array([d["y"][d["item"] == j].mean() for j in range(k)])
    ci = np.array([d["cond"][d["item"] == j][0] for j in range(k)])
    t2 = stats.ttest_ind(mi[ci == 1], mi[ci == 0]).statistic
    F1, F2 = t1 ** 2, t2 ** 2
    df1, df2 = n - 1, k - 2
    mf = F1 * F2 / (F1 + F2)
    df = (F1 + F2) ** 2 / (F1 ** 2 / df2 + F2 ** 2 / df1)
    return {"minF": float(mf), "df": float(df), "p": float(stats.f.sf(mf, 1, df))}


def false_positive_rates(reps: int = 200, seed: int = 0, **kw) -> dict:
    """With no effect at all: how often each analysis is significant at 5%."""
    f1 = f2 = mx = 0
    for r in range(reps):
        d = priming_study(effect=0.0, seed=seed + r, **kw)
        f1 += by_subject_test(d) < 0.05
        f2 += by_item_test(d) < 0.05
        mx += min_f_test(d)["p"] < 0.05
    return {"F1": f1 / reps, "F2": f2 / reps, "minF": mx / reps, "reps": reps}


def stimulus_power(effect: float, n_items_list, n_subj: int = 30, reps: int = 100, seed: int = 0, **kw) -> dict:
    """Power of the analysis that treats both participants and items as random (min F'), as the number of items
    grows, with the participants fixed."""
    out = []
    for k in n_items_list:
        hits = sum(min_f_test(priming_study(n_subj=n_subj, n_items=k, effect=effect, seed=seed + 1000 * k + r,
                                              **kw))["p"] < 0.05 for r in range(reps))
        out.append(hits / reps)
    return {"n_items": np.asarray(n_items_list), "power": np.array(out)}


# ----------------------------------------------------------------------------------------------------------------
# Shrinkage of person-level slopes
# ----------------------------------------------------------------------------------------------------------------
def person_slopes(n_people: int = 40, n_obs: int = 8, slope_mean: float = 0.5, slope_sd: float = 0.3,
                  noise: float = 1.0, seed: int = 0) -> dict:
    """Each person's own regression line (few observations each) against the multilevel model's BLUPs."""
    rng = np.random.default_rng(seed)
    g = np.repeat(np.arange(n_people), n_obs)
    x = rng.normal(0, 1, len(g))
    a = rng.normal(0, 0.8, n_people)
    b = rng.normal(slope_mean, slope_sd, n_people)
    y = a[g] + b[g] * x + rng.normal(0, noise, len(g))
    ols = np.array([np.polyfit(x[g == i], y[g == i], 1)[0] for i in range(n_people)])
    X = np.column_stack([np.ones(len(g)), x])
    fit = lmm(y, X, g, slopes=[1])
    blup = fit.beta[1] + fit.blup[:, 1]
    return {"true": b, "ols": ols, "blup": blup, "beta": fit.beta, "G": fit.G, "sigma2": fit.sigma2,
            "rmse_ols": float(np.sqrt(np.mean((ols - b) ** 2))), "rmse_blup": float(np.sqrt(np.mean((blup - b) ** 2)))}


# ----------------------------------------------------------------------------------------------------------------
# Within against between
# ----------------------------------------------------------------------------------------------------------------
def simpson_cloud(n_people: int = 12, n_obs: int = 15, between: float = 1.0, within: float = -0.6,
                  spread: float = 2.0, seed: int = 0) -> dict:
    """People whose averages rise together (between slope positive) but within whom y falls as x rises (within
    slope negative): e.g. typing speed and errors across typists against within one typist."""
    rng = np.random.default_rng(seed)
    g = np.repeat(np.arange(n_people), n_obs)
    mx = rng.normal(0, spread, n_people)
    my = between * mx + rng.normal(0, 0.3, n_people)
    dx = rng.normal(0, 0.8, len(g))
    x = mx[g] + dx
    y = my[g] + within * dx + rng.normal(0, 0.3, len(g))
    pooled = float(np.polyfit(x, y, 1)[0])
    xc = x - np.array([x[g == i].mean() for i in range(n_people)])[g]
    yc = y - np.array([y[g == i].mean() for i in range(n_people)])[g]
    w = float(np.polyfit(xc, yc, 1)[0])
    bmx = np.array([x[g == i].mean() for i in range(n_people)])
    bmy = np.array([y[g == i].mean() for i in range(n_people)])
    b = float(np.polyfit(bmx, bmy, 1)[0])
    return {"x": x, "y": y, "g": g, "pooled": pooled, "within": w, "between": b, "true_within": within,
            "true_between": between}


def nonergodic(n_people: int = 200, T: int = 100, seed: int = 0) -> dict:
    """A population in which every person's two variables are related differently over time (a person-specific
    correlation drawn from a wide distribution, centred near zero), while the cross-sectional correlation at any
    moment is strong because people differ stably in both: group statistics that describe no one."""
    rng = np.random.default_rng(seed)
    r_person = np.clip(rng.normal(0.0, 0.45, n_people), -0.95, 0.95)
    lvl = rng.multivariate_normal([0, 0], [[1, 0.8], [0.8, 1]], n_people)
    xs, ys = np.zeros((n_people, T)), np.zeros((n_people, T))
    for i in range(n_people):
        C = np.array([[1, r_person[i]], [r_person[i], 1]]) * 0.3
        z = rng.multivariate_normal([0, 0], C, T)
        xs[i], ys[i] = lvl[i, 0] + z[:, 0], lvl[i, 1] + z[:, 1]
    cross = np.array([np.corrcoef(xs[:, t], ys[:, t])[0, 1] for t in range(T)])
    within = np.array([np.corrcoef(xs[i], ys[i])[0, 1] for i in range(n_people)])
    return {"cross": cross, "within": within, "r_person": r_person, "cross_mean": float(cross.mean()),
            "share_near": float(np.mean(np.abs(within - cross.mean()) < 0.1))}


def ar1_series(phi: float, T: int, mu: float = 0.0, sd: float = 1.0, seed: int = 0) -> np.ndarray:
    rng = np.random.default_rng(seed)
    x = np.zeros(T)
    x[0] = rng.normal(0, sd / np.sqrt(1 - phi ** 2))
    for t in range(1, T):
        x[t] = phi * x[t - 1] + rng.normal(0, sd)
    return x + mu


def inertia_bias(phi: float = 0.4, Ts=(10, 20, 50, 100, 200), reps: int = 2000, seed: int = 0) -> dict:
    """The person-level autoregression estimated from T observations around the person's own mean is biased down
    by about (1 + 3 phi)/T (Kendall's small-sample bias; Nickell's in panels)."""
    rng = np.random.default_rng(seed)
    out = []
    for T in Ts:
        est = []
        for r in range(reps):
            x = ar1_series(phi, T, seed=int(rng.integers(1 << 30)))
            xc = x - x.mean()
            est.append(np.sum(xc[1:] * xc[:-1]) / np.sum(xc[:-1] ** 2))
        out.append(np.mean(est))
    return {"T": np.asarray(Ts), "mean_est": np.array(out), "phi": phi,
            "kendall": phi - (1 + 3 * phi) / np.asarray(Ts, float)}


# ----------------------------------------------------------------------------------------------------------------
# Tipping points: critical slowing down
# ----------------------------------------------------------------------------------------------------------------
def double_well(T: int = 4000, dt: float = 0.05, noise: float = 0.25, c_start: float = -0.6, c_end: float = 0.45,
                seed: int = 0, ramp: bool = True) -> dict:
    """dx = (x - x^3 + c) dt + noise dW, starting in the lower well; c rises slowly (``ramp``), flattening the lower
    well until it vanishes near c = 0.385 and the system tips into the upper one.  Without the ramp, c stays at
    c_start: a system that never tips."""
    rng = np.random.default_rng(seed)
    c = np.linspace(c_start, c_end, T) if ramp else np.full(T, c_start)
    x = np.zeros(T)
    x[0] = -1.1
    for t in range(1, T):
        x[t] = x[t - 1] + (x[t - 1] - x[t - 1] ** 3 + c[t - 1]) * dt + noise * np.sqrt(dt) * rng.normal()
    tip = int(np.argmax(x > 0.3)) if np.any(x > 0.3) else T
    return {"x": x, "c": c, "tip": tip}


def rolling_indicators(x, window: int = 400) -> dict:
    """Lag-1 autocorrelation and variance in a sliding window (after removing each window's mean): the two
    early-warning indicators of critical slowing down."""
    x = np.asarray(x, float)
    ac, var = np.full(len(x), np.nan), np.full(len(x), np.nan)
    for t in range(window, len(x)):
        w = x[t - window:t] - x[t - window:t].mean()
        var[t] = w.var()
        ac[t] = np.sum(w[1:] * w[:-1]) / np.sum(w ** 2)
    return {"ac": ac, "var": var}


def kendall_trend(series) -> float:
    """Kendall's tau between an indicator and time (the usual early-warning statistic), ignoring NaNs."""
    s = np.asarray(series, float)
    ok = np.isfinite(s)
    return float(stats.kendalltau(np.arange(len(s))[ok], s[ok]).statistic)


def warning_rates(n: int = 100, window: int = 300, threshold: float = 0.5, seed: int = 0, thin: int = 1,
                  noise_obs: float = 0.0) -> dict:
    """How often a rising autocorrelation (Kendall tau above ``threshold`` before the end of the record) is seen in
    systems that tip, and in systems that never do.  ``thin`` keeps every thin-th point (a diary once a day rather
    than a continuous record) and ``noise_obs`` adds measurement error to each kept point; ``window`` is in kept
    points."""
    rng = np.random.default_rng(seed + 77)
    hits = false = 0
    for r in range(n):
        d = double_well(T=3000, seed=seed + r)
        end = max((window + 50) * thin, d["tip"] - 50)
        x = d["x"][:end:thin] + noise_obs * rng.normal(size=len(d["x"][:end:thin]))
        hits += kendall_trend(rolling_indicators(x, window)["ac"]) > threshold
        d0 = double_well(T=3000, seed=seed + 10_000 + r, ramp=False)
        x0 = d0["x"][:end:thin] + noise_obs * rng.normal(size=len(d0["x"][:end:thin]))
        false += kendall_trend(rolling_indicators(x0, window)["ac"]) > threshold
    return {"hit": hits / n, "false_alarm": false / n, "n": n}


# ----------------------------------------------------------------------------------------------------------------
# Additions: time-varying predictors, own-versus-group prediction, and how many waves a within-person lag needs
# ----------------------------------------------------------------------------------------------------------------
def growth_split(n: int = 200, waves: int = 5, between: float = -0.4, within: float = 0.5, seed: int = 0) -> dict:
    """Children measured over ``waves``, with practice hours x varying over time; children who practise more on
    average score lower (between), while any child scores higher in a week they practise more (within).  A growth
    model with x entered once mixes the two; split into the child's mean and the week's departure, it separates
    them.  Random intercepts by statkit's ``lmm``."""
    rng = np.random.default_rng(seed)
    g = np.repeat(np.arange(n), waves)
    t = np.tile(np.arange(waves), n).astype(float)
    mu = rng.normal(0, 1, n)
    x = mu[g] + rng.normal(0, 0.7, len(g))
    xbar = np.array([x[g == i].mean() for i in range(n)])[g]
    u = rng.normal(0, 0.8, n)
    y = 1.0 * t + between * mu[g] + within * (x - mu[g]) + u[g] + rng.normal(0, 1, len(g))
    one = np.ones(len(g))
    f1 = lmm(y, np.column_stack([one, t, x]), g)
    f2 = lmm(y, np.column_stack([one, t, x - xbar, xbar]), g)
    return {"mixed": float(f1.beta[2]), "within": float(f2.beta[2]), "between": float(f2.beta[3]),
            "true_within": within, "true_between": between}


def own_vs_group(n_people: int = 200, k_list=(5, 10, 20, 40), T: int = 100, seed: int = 0) -> dict:
    """In the non-ergodic population: is a person's correlation over their remaining occasions better predicted by
    the group's cross-sectional correlation or by their own first k occasions?"""
    r = nonergodic(n_people=n_people, T=T, seed=seed)
    rng = np.random.default_rng(seed + 1)
    # rebuild the series with the same generator to get each person's occasions
    rng = np.random.default_rng(seed)
    r_person = np.clip(rng.normal(0.0, 0.45, n_people), -0.95, 0.95)
    lvl = rng.multivariate_normal([0, 0], [[1, 0.8], [0.8, 1]], n_people)
    xs, ys = np.zeros((n_people, T)), np.zeros((n_people, T))
    for i in range(n_people):
        C = np.array([[1, r_person[i]], [r_person[i], 1]]) * 0.3
        z = rng.multivariate_normal([0, 0], C, T)
        xs[i], ys[i] = lvl[i, 0] + z[:, 0], lvl[i, 1] + z[:, 1]
    group = r["cross_mean"]
    out = {"k": np.asarray(k_list), "own_err": [], "group_err": []}
    for k in k_list:
        own = np.array([np.corrcoef(xs[i, :k], ys[i, :k])[0, 1] for i in range(n_people)])
        later = np.array([np.corrcoef(xs[i, k:], ys[i, k:])[0, 1] for i in range(n_people)])
        out["own_err"].append(float(np.mean(np.abs(own - later))))
        out["group_err"].append(float(np.mean(np.abs(group - later))))
    out["own_err"], out["group_err"] = np.array(out["own_err"]), np.array(out["group_err"])
    return out


def crosslag_waves(waves_list=(3, 5, 10, 20, 50), n: int = 500, lag: float = 0.2, auto: float = 0.3,
                   reps: int = 20, seed: int = 0) -> dict:
    """Two traits with stable person levels (correlated 0.6) and a true within-person cross-lag; the lag estimated
    by regressing each person's departures from their own observed mean: biased toward the autoregression's small-T
    bias when waves are few, and accurate with many."""
    rng = np.random.default_rng(seed)
    out = []
    for T in waves_list:
        est = []
        for _ in range(reps):
            B = rng.multivariate_normal([0, 0], [[1, 0.6], [0.6, 1]], n)
            wx, wy = np.zeros((n, T)), np.zeros((n, T))
            wx[:, 0], wy[:, 0] = rng.normal(0, 1, n), rng.normal(0, 1, n)
            for t in range(1, T):
                wx[:, t] = auto * wx[:, t - 1] + rng.normal(0, 1, n)
                wy[:, t] = auto * wy[:, t - 1] + lag * wx[:, t - 1] + rng.normal(0, 1, n)
            x, y = B[:, [0]] + wx, B[:, [1]] + wy
            xc, yc = x - x.mean(1, keepdims=True), y - y.mean(1, keepdims=True)
            X = np.column_stack([yc[:, :-1].ravel(), xc[:, :-1].ravel()])
            coef = np.linalg.lstsq(X, yc[:, 1:].ravel(), rcond=None)[0]
            est.append(coef[1])
        out.append(float(np.mean(est)))
    return {"waves": np.asarray(waves_list), "est": np.array(out), "true": lag}
