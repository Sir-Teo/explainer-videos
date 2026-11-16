"""Psyche's meta-science (Part 50): reading a literature that has been filtered.

Simulated literatures with a known truth, heterogeneity, publication filters and p-hacking; random-effects pooling
with prediction intervals and the Hartung-Knapp correction; meta-regression and its power; funnel asymmetry
(Egger's test), PET, PEESE and PET-PEESE; trim-and-fill (Duval and Tweedie's L0); the three-parameter selection
model; p-curve's right-skew test and effect estimate; a grading harness that runs every method on many literatures;
forensic checks (GRIM, a SPRITE search, recomputed p-values); a specification-curve engine; and summaries of the
series' own Ledger.  numpy and scipy only.
"""

from __future__ import annotations

import itertools

import numpy as np
from scipy import optimize, stats


# ----------------------------------------------------------------------------------------------------------------
# Literatures
# ----------------------------------------------------------------------------------------------------------------
def literature(k: int = 200, true_d: float = 0.2, tau: float = 0.0, n_lo: int = 15, n_hi: int = 80,
               publish_null: float = 1.0, hack: float = 0.0, seed: int = 0) -> dict:
    """``k`` two-group studies with per-group n uniform in [n_lo, n_hi] and true effects N(true_d, tau^2).  A study is
    published if significant in the predicted direction (one-sided p < 0.025) or otherwise with probability
    ``publish_null``.  With probability ``hack`` a non-significant study is p-hacked: re-run up to four analyses
    (independent-ish noise) and the best is reported.  Returns all studies and the published flag."""
    rng = np.random.default_rng(seed)
    n = rng.integers(n_lo, n_hi + 1, k)
    theta = rng.normal(true_d, tau, k)
    v = 2 / n + theta ** 2 / (4 * n)
    d = rng.normal(theta, np.sqrt(v))
    hacked = np.zeros(k, bool)
    for i in range(k):
        if d[i] / np.sqrt(v[i]) <= 1.96 and rng.random() < hack:
            tries = theta[i] + 0.6 * (d[i] - theta[i]) + np.sqrt(0.64) * rng.normal(0, np.sqrt(v[i]), 4)
            d[i] = max(d[i], tries.max())
            hacked[i] = True
    sig = d / np.sqrt(v) > 1.96
    pub = sig | (rng.random(k) < publish_null)
    return {"d": d, "v": v, "se": np.sqrt(v), "n": n, "published": pub, "significant": sig, "hacked": hacked,
            "theta": theta}


# ----------------------------------------------------------------------------------------------------------------
# Pooling
# ----------------------------------------------------------------------------------------------------------------
def random_effects(y, v, hk: bool = False) -> dict:
    """DerSimonian and Laird, with the 95% interval (z, or Hartung-Knapp's t with k - 1 df) and the 95% prediction
    interval for a new study's true effect (Higgins, Thompson and Spiegelhalter)."""
    y, v = np.asarray(y, float), np.asarray(v, float)
    k = len(y)
    w = 1 / v
    fixed = float(np.sum(w * y) / w.sum())
    Q = float(np.sum(w * (y - fixed) ** 2))
    tau2 = max(0.0, (Q - (k - 1)) / (w.sum() - (w ** 2).sum() / w.sum()))
    ws = 1 / (v + tau2)
    mu = float(np.sum(ws * y) / ws.sum())
    se = float(np.sqrt(1 / ws.sum()))
    if hk and k > 1:
        q = float(np.sum(ws * (y - mu) ** 2) / (k - 1))
        se = float(np.sqrt(q / ws.sum()))
        crit = stats.t.ppf(0.975, k - 1)
    else:
        crit = 1.96
    tcrit = stats.t.ppf(0.975, max(k - 2, 1))
    half = tcrit * np.sqrt(tau2 + se ** 2)
    return {"mu": mu, "se": se, "lo": mu - crit * se, "hi": mu + crit * se, "tau2": tau2, "tau": float(np.sqrt(tau2)),
            "I2": max(0.0, (Q - (k - 1)) / Q) if Q > 0 else 0.0, "Q": Q, "fixed": fixed, "k": k,
            "pi_lo": mu - half, "pi_hi": mu + half}


def meta_regression(y, v, x) -> dict:
    """Mixed-effects meta-regression on one moderator: tau^2 by the method of moments on the residuals, then
    weighted least squares; returns slope, its SE and p."""
    y, v, x = (np.asarray(a, float) for a in (y, v, x))
    X = np.column_stack([np.ones_like(x), x])
    w = 1 / v
    W = np.diag(w)
    b = np.linalg.solve(X.T @ W @ X, X.T @ W @ y)
    r = y - X @ b
    Q = float(np.sum(w * r ** 2))
    P = W - W @ X @ np.linalg.solve(X.T @ W @ X, X.T @ W)
    tau2 = max(0.0, (Q - (len(y) - 2)) / np.trace(P))
    ws = 1 / (v + tau2)
    Ws = np.diag(ws)
    cov = np.linalg.inv(X.T @ Ws @ X)
    b = cov @ X.T @ Ws @ y
    z = b[1] / np.sqrt(cov[1, 1])
    return {"slope": float(b[1]), "se": float(np.sqrt(cov[1, 1])), "p": float(2 * stats.norm.sf(abs(z))), "tau2": tau2}


def moderator_power(k: int, diff: float, tau: float = 0.2, n_lo: int = 20, n_hi: int = 80, reps: int = 400,
                    seed: int = 0) -> float:
    """Power to detect a moderator: half the studies have true effect larger by ``diff``."""
    rng = np.random.default_rng(seed)
    hits = 0
    for r in range(reps):
        x = np.repeat([0.0, 1.0], k // 2)
        n = rng.integers(n_lo, n_hi + 1, len(x))
        th = rng.normal(0.3 + diff * x, tau)
        v = 2 / n
        y = rng.normal(th, np.sqrt(v))
        hits += meta_regression(y, v, x)["p"] < 0.05
    return hits / reps


# ----------------------------------------------------------------------------------------------------------------
# Seeing and correcting the filter
# ----------------------------------------------------------------------------------------------------------------
def egger(y, se) -> dict:
    """Egger's regression: standardized effect on precision; the intercept tests funnel asymmetry."""
    y, se = np.asarray(y, float), np.asarray(se, float)
    z, prec = y / se, 1 / se
    X = np.column_stack([np.ones_like(prec), prec])
    b, *_ = np.linalg.lstsq(X, z, rcond=None)
    r = z - X @ b
    s2 = float(r @ r / (len(z) - 2))
    cov = s2 * np.linalg.inv(X.T @ X)
    t = b[0] / np.sqrt(cov[0, 0])
    return {"intercept": float(b[0]), "p": float(2 * stats.t.sf(abs(t), len(z) - 2)), "slope": float(b[1])}


def pet(y, se) -> dict:
    """Precision-effect test: weighted regression of effect on SE; the intercept estimates the effect at SE = 0."""
    y, se = np.asarray(y, float), np.asarray(se, float)
    X = np.column_stack([np.ones_like(se), se])
    W = np.diag(1 / se ** 2)
    cov_raw = np.linalg.inv(X.T @ W @ X)
    b = cov_raw @ X.T @ W @ y
    r = y - X @ b
    s2 = float(r @ W @ r / (len(y) - 2))
    se_b = np.sqrt(s2 * np.diag(cov_raw))
    return {"est": float(b[0]), "se": float(se_b[0]), "p": float(2 * stats.t.sf(abs(b[0] / se_b[0]), len(y) - 2))}


def peese(y, se) -> dict:
    y, se = np.asarray(y, float), np.asarray(se, float)
    X = np.column_stack([np.ones_like(se), se ** 2])
    W = np.diag(1 / se ** 2)
    b = np.linalg.solve(X.T @ W @ X, X.T @ W @ y)
    return {"est": float(b[0])}


def pet_peese(y, se) -> float:
    """Stanley and Doucouliagos: PEESE if PET's intercept is significant (one-sided), else PET."""
    p = pet(y, se)
    if p["est"] > 0 and p["p"] / 2 < 0.05:
        return peese(y, se)["est"]
    return p["est"]


def trim_and_fill(y, v, max_iter: int = 50) -> dict:
    """Duval and Tweedie's trim-and-fill with the L0 estimator, assuming missing studies on the left: trim the k0
    most extreme right-side studies, re-estimate, repeat; then fill their mirror images and pool."""
    y, v = np.asarray(y, float), np.asarray(v, float)
    k = len(y)
    k0 = 0
    for _ in range(max_iter):
        order = np.argsort(y)
        keep = order[: k - k0] if k0 > 0 else order
        mu = random_effects(y[keep], v[keep])["mu"]
        dev = y - mu
        ranks = stats.rankdata(np.abs(dev))
        Tn = float(np.sum(ranks[dev > 0]))
        new = int(max(0, round((4 * Tn - k * (k + 1)) / (2 * k - 1))))
        if new == k0:
            break
        k0 = min(new, k - 3)
    order = np.argsort(y)
    extra = order[k - k0:] if k0 > 0 else np.array([], int)
    yf = np.concatenate([y, 2 * mu - y[extra]])
    vf = np.concatenate([v, v[extra]])
    return {"k0": k0, "est": random_effects(yf, vf)["mu"]}


def selection_model(y, se) -> dict:
    """The three-parameter selection model (Vevea and Hedges; Iyengar and Greenhouse): true effects N(mu, tau^2),
    and non-significant studies (one-sided p > 0.025) published with relative probability w.  Maximum likelihood."""
    y, se = np.asarray(y, float), np.asarray(se, float)
    sig = y / se > 1.96

    def nll(p):
        mu, ltau, lw = p
        tau2, w = np.exp(2 * ltau), np.exp(lw)
        s = np.sqrt(tau2 + se ** 2)
        dens = stats.norm.logpdf(y, mu, s)
        psig = stats.norm.sf((1.96 * se - mu) / s)
        norm = psig + w * (1 - psig)
        return -float(np.sum(dens + np.where(sig, 0.0, lw) - np.log(norm)))

    best = None
    for mu0 in (0.0, 0.3):
        for w0 in (-1.0, 0.0):
            r = optimize.minimize(nll, [mu0, np.log(0.1), w0], method="L-BFGS-B",
                                  bounds=[(-2, 3), (np.log(1e-3), np.log(2)), (np.log(1e-3), np.log(1.0))])
            if best is None or r.fun < best.fun:
                best = r
    return {"est": float(best.x[0]), "tau": float(np.exp(best.x[1])), "w": float(np.exp(best.x[2]))}


def pcurve(y, se) -> dict:
    """p-curve on the significant results: the right-skew test (Stouffer on pp-values) and the effect that makes
    the pp-values uniform (Kolmogorov-Smirnov), by the normal approximation; d's are in the units of y."""
    y, se = np.asarray(y, float), np.asarray(se, float)
    z = y / se
    s = z > 1.96
    z, se_s = z[s], se[s]
    if len(z) < 3:
        return {"skew_p": float("nan"), "est": float("nan"), "k": int(len(z))}
    pp0 = stats.norm.sf(z) / 0.025
    stouffer = float(np.sum(stats.norm.ppf(pp0)) / np.sqrt(len(z)))
    skew_p = float(stats.norm.cdf(stouffer))

    def ks(d):
        ncp = d / se_s
        pp = stats.norm.sf(z - ncp) / stats.norm.sf(1.96 - ncp)
        return stats.kstest(np.clip(pp, 0, 1), "uniform").statistic

    grid = np.linspace(-0.2, 1.5, 171)
    est = float(grid[int(np.argmin([ks(g) for g in grid]))])
    return {"skew_p": skew_p, "est": est, "k": int(len(z))}


METHODS = ("naive", "trim-and-fill", "PET-PEESE", "selection model", "p-curve")


def estimate_all(lit: dict) -> dict:
    pub = lit["published"]
    y, v, se = lit["d"][pub], lit["v"][pub], lit["se"][pub]
    return {"naive": random_effects(y, v)["mu"], "trim-and-fill": trim_and_fill(y, v)["est"],
            "PET-PEESE": pet_peese(y, se), "selection model": selection_model(y, se)["est"],
            "p-curve": pcurve(y, se)["est"], "k": int(pub.sum())}


def grade(scenarios, reps: int = 60, k: int = 200, seed: int = 0) -> dict:
    """Run every method on ``reps`` simulated literatures per scenario (true_d, tau, publish_null, hack): mean
    estimate and RMSE per method."""
    out = []
    for si, (d, tau, pn, hack) in enumerate(scenarios):
        ests = {m: [] for m in METHODS}
        for r in range(reps):
            lit = literature(k=k, true_d=d, tau=tau, publish_null=pn, hack=hack, seed=seed + 1000 * si + r)
            e = estimate_all(lit)
            for m in METHODS:
                ests[m].append(e[m])
        row = {"true_d": d, "tau": tau, "publish_null": pn, "hack": hack}
        for m in METHODS:
            a = np.asarray(ests[m], float)
            a = a[np.isfinite(a)]
            row[m] = (float(a.mean()), float(np.sqrt(np.mean((a - d) ** 2))))
        out.append(row)
    return {"rows": out, "methods": list(METHODS)}


# ----------------------------------------------------------------------------------------------------------------
# Forensics
# ----------------------------------------------------------------------------------------------------------------
def grim(mean: float, n: int, decimals: int = 2, items: int = 1) -> bool:
    """Brown and Heathers' GRIM test: can a mean of ``n`` integer answers (each the sum of ``items`` items)
    round to the reported mean?"""
    total = mean * n * items
    for t in (np.floor(total), np.ceil(total)):
        if round(t / (n * items) + 1e-12, decimals) == round(mean, decimals):
            return True
    return False


def sprite(mean: float, sd: float, n: int, lo: int, hi: int, decimals: int = 2, tries: int = 4000,
           seed: int = 0):
    """A SPRITE-style search (Heathers and colleagues): look for a sample of ``n`` integers in [lo, hi] whose mean
    and SD round to the reported ones, by random local moves that keep the sum fixed.  Returns a sample or None."""
    rng = np.random.default_rng(seed)
    total = int(round(mean * n))
    if not grim(mean, n, decimals):
        return None
    x = np.full(n, total // n)
    x[: total - x.sum()] += 1
    if x.min() < lo or x.max() > hi:
        return None
    for _ in range(tries):
        s = x.std(ddof=1)
        if round(s, decimals) == round(sd, decimals):
            return np.sort(x)
        i, j = rng.integers(0, n, 2)
        if i == j:
            continue
        step = 1 if s < sd else -1
        a, b = (i, j) if x[i] >= x[j] else (j, i)  # widen: move a up, b down; narrow: the reverse
        if step > 0 and x[a] < hi and x[b] > lo:
            x[a] += 1; x[b] -= 1
        elif step < 0 and x[a] - x[b] >= 2:
            x[a] -= 1; x[b] += 1
    return None


def recompute_p(t: float, df: int) -> float:
    """statcheck's core: the two-sided p of a reported t on df degrees of freedom."""
    return float(2 * stats.t.sf(abs(t), df))


def statcheck(reports) -> list:
    """For each (t, df, reported p, reported as '<' or '='), whether the reported p is consistent with the
    recomputed one (to the reported precision), and whether the error changes significance at 0.05."""
    out = []
    for t, df, p_rep, rel in reports:
        p = recompute_p(t, df)
        if rel == "<":
            ok = p < p_rep
        else:
            dec = len(f"{p_rep}".split(".")[1]) if "." in f"{p_rep}" else 2
            ok = abs(round(p, dec) - p_rep) < 10 ** (-dec) / 2 + 1e-12
        gross = (p < 0.05) != (p_rep < 0.05 if rel == "=" else p_rep <= 0.05)
        out.append({"t": t, "df": df, "reported": p_rep, "recomputed": p, "consistent": bool(ok),
                    "gross": bool(gross and not ok)})
    return out


# ----------------------------------------------------------------------------------------------------------------
# Many analysts: the specification curve
# ----------------------------------------------------------------------------------------------------------------
def spec_curve(n: int = 300, effect: float = 0.08, seed: int = 0) -> dict:
    """One simulated dataset: an outcome, a predictor with a small true effect, four covariates (two of them
    confounded with the predictor), and analytic choices: every subset of covariates (16), three outlier rules,
    and a raw or log outcome (96 specifications).  Returns the estimates sorted, their p-values, and the choices."""
    rng = np.random.default_rng(seed)
    C = rng.normal(size=(n, 4))
    x = 0.4 * C[:, 0] - 0.3 * C[:, 1] + rng.normal(size=n)
    y = effect * x + 0.3 * C[:, 0] + 0.2 * C[:, 1] + 0.2 * C[:, 2] + rng.standard_t(4, n)
    y = y - y.min() + 1.0
    specs = []
    for subset in itertools.product([0, 1], repeat=4):
        for outl in ("none", "3 SD", "2.5 MAD"):
            for tr in ("raw", "log"):
                yy = np.log(y) if tr == "log" else y.copy()
                keep = np.ones(n, bool)
                if outl == "3 SD":
                    keep = np.abs(yy - yy.mean()) < 3 * yy.std()
                elif outl == "2.5 MAD":
                    med = np.median(yy)
                    keep = np.abs(yy - med) < 2.5 * 1.4826 * np.median(np.abs(yy - med))
                cols = [np.ones(keep.sum()), x[keep] / x.std()] + [C[keep, j] for j in range(4) if subset[j]]
                X = np.column_stack(cols)
                Y = (yy[keep] - yy[keep].mean()) / yy[keep].std()
                b, *_ = np.linalg.lstsq(X, Y, rcond=None)
                res = Y - X @ b
                df = len(Y) - X.shape[1]
                cov = (res @ res / df) * np.linalg.inv(X.T @ X)
                tval = b[1] / np.sqrt(cov[1, 1])
                specs.append((float(b[1]), float(2 * stats.t.sf(abs(tval), df)), subset, outl, tr))
    specs.sort(key=lambda s: s[0])
    est = np.array([s[0] for s in specs])
    p = np.array([s[1] for s in specs])
    return {"est": est, "p": p, "n_specs": len(specs), "share_sig": float(np.mean(p < 0.05)),
            "median": float(np.median(est)), "covariates": np.array([s[2] for s in specs]),
            "outliers": [s[3] for s in specs], "transform": [s[4] for s in specs]}


# ----------------------------------------------------------------------------------------------------------------
# The Ledger, audited
# ----------------------------------------------------------------------------------------------------------------
ACTS = ((1, 4, "I"), (5, 10, "II"), (11, 15, "III"), (16, 17, "IV"), (18, 21, "V"), (22, 27, "VI"), (28, 29, "VII"),
        (30, 33, "VIII"), (34, 38, "IX"), (39, 43, "X"), (44, 50, "XI"))


def act_of(part: int) -> str:
    for lo, hi, a in ACTS:
        if lo <= part <= hi:
            return a
    return "?"


def ledger_audit(rows) -> dict:
    """Status counts overall, by act, and by the decade of the original study, from Ledger findings."""
    statuses = ("replicated", "replicated, smaller", "story and record", "contested", "failed", "retracted",
                "not directly tested")

    def bucket(f):
        return f.status if f.status in statuses else "not directly tested"

    by_act, by_decade = {}, {}
    total = {s: 0 for s in statuses}
    for f in rows:
        b = bucket(f)
        total[b] += 1
        a = act_of(f.part)
        by_act.setdefault(a, {s: 0 for s in statuses})[b] += 1
        dec = (f.original.year // 10) * 10 if f.original and f.original.year else 0
        by_decade.setdefault(dec, {s: 0 for s in statuses})[b] += 1
    return {"total": total, "by_act": by_act, "by_decade": dict(sorted(by_decade.items())), "n": len(rows)}
