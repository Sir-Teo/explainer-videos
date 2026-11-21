"""Agora's model of a research field (Part 67): studies with true effects, specification search, a publication
filter, replication, many analysts on one dataset, a correction for publication bias, an agent-based market beside the
equilibrium one, and an audit of the series' Dials.

* **A literature** (:func:`literature`): true effects, standard errors, a researcher who (with a probability that
  depends on the design) tries other specifications when the first is not significant, and a journal that publishes
  insignificant results less often.  The published z-statistics show Brodeur et al.'s two-humped camel.
* **Diagnostics** (:func:`caliper`, :func:`selection_mle`): the caliper ratio around 1.96 and a maximum-likelihood
  estimate of the relative publication probability of insignificant results (Andrews and Kasy's step model).
* **Replication** (:func:`replicate`): high-powered repeats of the published significant results.
* **Many analysts** (:func:`many_analysts`): teams that make defensible choices on the same data, and the spread of
  their estimates against the standard errors each reports.
* **An agent-based market** (:func:`brock_hommes`): Brock and Hommes's cobweb with traders who switch between a costly
  rational forecast and a free naive one; the route to chaos as they switch faster.
* **The audit** (:func:`dial_audit`): what the series' Dials say, and how far apart their estimates are.

numpy and scipy.
"""

from __future__ import annotations

import numpy as np

DESIGNS = {"RCT": 0.10, "RDD": 0.15, "DiD": 0.30, "IV": 0.45}     # the chance of searching when not significant


def literature(n: int = 40000, search: float = 0.3, tries: int = 5, rho: float = 0.6, publish_ns: float = 0.35,
               null_share: float = 0.5, tau: float = 2.0, seed: int = 67) -> dict:
    """``n`` studies.  A share ``null_share`` have no effect; the rest have true z (effect over standard error)
    drawn from N(0, tau^2).  Each first estimate is z_true + N(0, 1).  If it is not significant (|z| < 1.96), with
    probability ``search`` the researcher tries up to ``tries`` other specifications, each correlated ``rho`` with the
    first, and reports the first that is significant (or the best).  Journals publish significant results and a share
    ``publish_ns`` of the rest.  Returns the published |z| and their true z, and the first-try |z| of all studies."""
    rng = np.random.default_rng(seed)
    real = rng.random(n) > null_share
    zt = np.where(real, rng.normal(0, tau, n), 0.0)
    z0 = zt + rng.normal(0, 1, n)
    z = z0.copy()
    searched = (np.abs(z0) < 1.96) & (rng.random(n) < search)
    for i in np.nonzero(searched)[0]:
        best = z0[i]
        for _ in range(tries):
            alt = zt[i] + rho * (z0[i] - zt[i]) + np.sqrt(1 - rho ** 2) * rng.normal()
            if abs(alt) > abs(best):
                best = alt
            if abs(best) >= 1.96:
                break
        z[i] = best
    sig = np.abs(z) >= 1.96
    pub = sig | (rng.random(n) < publish_ns)
    return {"z": np.abs(z[pub]), "z_true": (zt * np.sign(z))[pub], "real": real[pub],
            "first": np.abs(z0), "search": search, "publish_ns": publish_ns, "n": n,
            "searched_share": float(searched.mean()), "published": int(pub.sum())}


def caliper(z, width: float = 0.25, cut: float = 1.96) -> dict:
    """Counts of published |z| just below and just above the cutoff, and their ratio: about one without selection,
    well above one with it."""
    z = np.asarray(z)
    below = int(((z >= cut - width) & (z < cut)).sum())
    above = int(((z >= cut) & (z < cut + width)).sum())
    return {"below": below, "above": above, "ratio": above / max(below, 1)}


def selection_mle(z, cut: float = 1.96) -> dict:
    """Andrews and Kasy's step model for |z| with a unit standard error.  The latent z is a mixture: with weight w a
    null effect, N(0, 1), otherwise N(mu, 1 + s^2) (a normal distribution of true effects plus sampling noise); a
    result with |z| < cut is published with relative probability beta.  Maximum likelihood for (w, mu, s, beta) on
    the published |z|; beta near one means no selection.  Search and the journals' filter both remove insignificant
    results, so beta measures their joint effect."""
    from scipy import optimize, stats

    z = np.abs(np.asarray(z, float))

    def folded(x, m, sd):
        return stats.norm.pdf(x, m, sd) + stats.norm.pdf(-x, m, sd)

    def inside(m, sd):
        return stats.norm.cdf(cut, m, sd) - stats.norm.cdf(-cut, m, sd)

    def nll(par):
        lw, mu, ls, lb = par
        w, beta = 1 / (1 + np.exp(-lw)), 1 / (1 + np.exp(-lb))
        sd = np.sqrt(1 + np.exp(ls) ** 2)
        dens = w * folded(z, 0.0, 1.0) + (1 - w) * folded(z, mu, sd)
        p_in = w * inside(0.0, 1.0) + (1 - w) * inside(mu, sd)
        wt = np.where(z < cut, beta, 1.0)
        return -np.sum(np.log(wt * dens / (beta * p_in + 1 - p_in) + 1e-300))

    best = None
    for x0 in ([-1.0, 0.0, np.log(2.0), 0.0], [0.0, 0.5, np.log(1.5), -1.0], [1.0, 0.0, np.log(3.0), 1.0]):
        res = optimize.minimize(nll, x0=x0, method="Nelder-Mead",
                                options={"maxiter": 6000, "xatol": 1e-6, "fatol": 1e-8})
        if best is None or res.fun < best.fun:
            best = res
    lw, mu, ls, lb = best.x
    return {"w": float(1 / (1 + np.exp(-lw))), "mu": float(mu), "sd": float(np.sqrt(1 + np.exp(ls) ** 2)),
            "beta": float(1 / (1 + np.exp(-lb))), "ok": bool(best.success)}


def replicate(lit: dict, power: float = 0.9, seed: int = 671) -> dict:
    """Replicate every published significant result with a sample large enough for ``power`` against the original
    estimate (the replication's z has mean z_true * k with k = (z_power / z_orig)).  Success: significant in the same
    direction.  Also the average ratio of the replication's effect to the original's."""
    from scipy import stats

    rng = np.random.default_rng(seed)
    z, zt = np.asarray(lit["z"]), np.asarray(lit["z_true"])          # z_true is signed in the reported direction
    sig = z >= 1.96
    zo, ztr = z[sig], zt[sig]
    zpow = stats.norm.ppf(power) + 1.96
    k = zpow / zo                                     # the replication's precision relative to the original's
    zr = ztr * k + rng.normal(0, 1, len(zo))
    success = zr >= 1.96
    ratio = (zr / k) / zo                              # replication effect over original effect
    return {"rate": float(success.mean()), "ratio": float(ratio.mean()), "n": int(sig.sum()),
            "zpow": float(zpow), "true_ratio": float(np.mean(ztr / zo)), "null_share": float(np.mean(ztr == 0))}


CHOICES = {"ages": ([18, 65], [18, 55], [18, 50], [22, 65], [22, 55], [22, 50], [25, 65], [25, 55], [25, 50]),
           "outliers": (False, True), "age_bands": (False, True), "log_prior": (False, True),
           "regions": (False, True), "treated": ("enrolled", "finished")}


def analysts_data(n: int = 4000, seed: int = 672) -> dict:
    """The many-analysts dataset: does a training programme raise earnings (log points)?  The programme's effect
    differs by age (larger for the young), take-up is higher among the young, the poor and in some regions, earnings
    have heavy tails and a few miscoded records, and three in ten who enrol do not finish."""
    rng = np.random.default_rng(seed)
    age = rng.uniform(18, 65, n)
    prior = rng.normal(10, 0.6, n)                               # log earnings before the programme
    reg = rng.integers(0, 8, n)
    reg_fx = rng.normal(0, 0.2, 8)
    lean = -0.4 + 0.05 * (40 - age) - 0.8 * (prior - 10) + 0.5 * (reg % 3 == 0)
    enrol = rng.random(n) < 1 / (1 + np.exp(-lean))
    finish = enrol & (rng.random(n) < 0.7)
    effect = np.where(age < 30, 0.25, np.where(age < 50, 0.10, -0.02))
    y = (prior + 0.012 * (age - 40) - 0.0006 * (age - 40) ** 2 + reg_fx[reg] + effect * finish
         + 0.04 * enrol + 0.30 * rng.standard_t(3, n))
    bad = rng.random(n) < 0.006
    y[bad] += rng.choice([-1, 1], bad.sum()) * rng.uniform(2, 4, bad.sum())
    return {"age": age, "prior": prior, "reg": reg, "enrol": enrol, "finish": finish, "y": y, "effect": effect}


def analyse(D: dict, ch: dict) -> dict:
    """One analyst's choices applied to the dataset: OLS of earnings on the programme with the chosen sample and
    controls, and a heteroskedasticity-robust (HC0) standard error."""
    age, y, enrol, finish = D["age"], D["y"], D["enrol"], D["finish"]
    n = len(y)
    lo, hi = ch["ages"]
    keep = (age >= lo) & (age <= hi)
    if ch["outliers"]:
        med = np.median(y)
        keep &= np.abs(y - med) < 4 * 1.4826 * np.median(np.abs(y - med))
    d = (enrol if ch["treated"] == "enrolled" else finish).astype(float)
    if ch["treated"] == "finished":
        keep &= ~(enrol & ~finish)                                    # drop those who quit
    X = [np.ones(n), d]
    if ch["age_bands"]:
        X += [((age >= b0) & (age < b0 + 10)).astype(float) for b0 in (25, 35, 45, 55)]
    else:
        X.append(age)
    X.append(D["prior"] if ch["log_prior"] else np.exp(D["prior"]) / 1e4)
    if ch["regions"]:
        X += [(D["reg"] == r).astype(float) for r in range(1, 8)]
    Xm = np.column_stack(X)[keep]
    yy = y[keep]
    beta, *_ = np.linalg.lstsq(Xm, yy, rcond=None)
    e = yy - Xm @ beta
    XtX = np.linalg.pinv(Xm.T @ Xm)
    V = XtX @ (Xm.T * e ** 2) @ Xm @ XtX
    return {"est": float(beta[1]), "se": float(np.sqrt(V[1, 1])), "n": int(keep.sum())}


def many_analysts(teams: int = 7, n: int = 4000, seed: int = 672) -> dict:
    """``teams`` analysts each make choices a referee would accept (from :data:`CHOICES`, drawn at random) on the
    dataset of :func:`analysts_data`.  Returns each team's estimate, robust standard error, sample size and choices;
    the spread of the estimates against the mean reported standard error; and the effect among those who finished,
    which no team was told to target."""
    D = analysts_data(n, seed)
    trng = np.random.default_rng(seed + 11)
    rows = []
    for t in range(teams):
        ch = {"ages": [int(trng.choice([18, 22, 25])), int(trng.choice([50, 55, 65]))],
              "outliers": bool(trng.random() < 0.5), "age_bands": bool(trng.random() < 0.5),
              "log_prior": bool(trng.random() < 0.6), "regions": bool(trng.random() < 0.6),
              "treated": str(trng.choice(["enrolled", "finished"]))}
        rows.append({"team": t + 1, **analyse(D, ch), **ch})
    est = np.array([r["est"] for r in rows])
    se = np.array([r["se"] for r in rows])
    return {"rows": rows, "spread": float(est.std(ddof=1)), "mean_se": float(se.mean()),
            "ratio": float(est.std(ddof=1) / se.mean()), "ate": float(D["effect"][D["finish"]].mean()),
            "n_sizes": len({r["n"] for r in rows})}


def specification_curve(n: int = 4000, seed: int = 672) -> dict:
    """Every combination of the choices in :data:`CHOICES` (9 x 2^5 = 288 specifications) on the same dataset,
    sorted by estimate: the specification curve, and the share significant at 5%."""
    import itertools

    D = analysts_data(n, seed)
    keys = list(CHOICES)
    rows = []
    for combo in itertools.product(*[CHOICES[k] for k in keys]):
        ch = dict(zip(keys, combo))
        rows.append({**analyse(D, ch), **{k: (list(v) if isinstance(v, list) else v) for k, v in ch.items()}})
    rows.sort(key=lambda r: r["est"])
    est = np.array([r["est"] for r in rows])
    se = np.array([r["se"] for r in rows])
    return {"rows": rows, "n_specs": len(rows), "share_sig": float(np.mean(np.abs(est / se) >= 1.96)),
            "lo": float(est.min()), "hi": float(est.max()), "median": float(np.median(est))}


def mixed_field(n: int = 40000, seed: int = 670, **kw) -> dict:
    """A field of four designs in equal shares, each with its own chance of specification search
    (:data:`DESIGNS`).  Returns the published |z|, signed truth and design of every published result."""
    zs, zt, des, real = [], [], [], []
    for k, (d, h) in enumerate(DESIGNS.items()):
        L = literature(n=n // len(DESIGNS), search=h, seed=seed + k, **kw)
        zs.append(L["z"])
        zt.append(L["z_true"])
        real.append(L["real"])
        des += [d] * len(L["z"])
    return {"z": np.concatenate(zs), "z_true": np.concatenate(zt), "real": np.concatenate(real),
            "design": np.array(des)}


def replicate_by_z(lit: dict, edges=(1.96, 2.5, 3.0, 4.0, 6.0, 99.0), power: float = 0.9, seed: int = 674) -> dict:
    """Replicate every published significant result (as in :func:`replicate`) and tabulate the success rate and the
    exaggeration (original z over true z) by the original |z|."""
    from scipy import stats

    rng = np.random.default_rng(seed)
    z, zt = np.asarray(lit["z"]), np.asarray(lit["z_true"])
    sig = z >= 1.96
    zo, ztr = z[sig], zt[sig]
    k = (stats.norm.ppf(power) + 1.96) / zo
    ok = (ztr * k + rng.normal(0, 1, len(zo))) >= 1.96
    rows = []
    for a, b in zip(edges[:-1], edges[1:]):
        m = (zo >= a) & (zo < b)
        rows.append({"lo": a, "hi": b, "n": int(m.sum()), "rate": float(ok[m].mean()),
                     "true_over_orig": float(np.mean(ztr[m] / zo[m]))})
    return {"rows": rows, "rate": float(ok.mean())}


def false_positive(tries, rho: float, sims: int = 20000, seed: int = 675) -> list:
    """Under the null, a researcher tries ``k`` specifications whose z-statistics are equicorrelated ``rho`` and
    reports the first significant one: the chance of a significant result, for each k in ``tries``."""
    rng = np.random.default_rng(seed)
    out = []
    for k in tries:
        k = int(k)
        common = rng.normal(size=(sims, 1))
        z = np.sqrt(rho) * common + np.sqrt(1 - rho) * rng.normal(size=(sims, min(k, 4000)))
        out.append(float((np.abs(z) >= 1.96).any(axis=1).mean()))
    return out


def meta_literature(n: int = 600, theta: float = -0.03, tau: float = 0.03, beta_ns: float = 0.33,
                    beta_pos: float = 0.33, seed: int = 676) -> dict:
    """A simulated meta-study (the shape of the minimum-wage literature): each study's true elasticity is drawn from
    N(theta, tau^2), its standard error from a wide range, its estimate is the truth plus noise.  Negative and
    significant estimates are always published; insignificant ones with probability ``beta_ns``; positive significant
    ones with ``beta_pos``.  Returns the published estimates and standard errors and the truth."""
    rng = np.random.default_rng(seed)
    se = np.exp(rng.uniform(np.log(0.008), np.log(0.12), n * 4))
    th = rng.normal(theta, tau, n * 4)
    x = th + se * rng.normal(size=n * 4)
    z = x / se
    p = np.where(z <= -1.96, 1.0, np.where(z >= 1.96, beta_pos, beta_ns))
    pub = rng.random(n * 4) < p
    idx = np.nonzero(pub)[0][:n]
    return {"est": x[idx], "se": se[idx], "theta": theta, "tau": tau, "beta_ns": beta_ns, "beta_pos": beta_pos,
            "all_est": x, "all_se": se}


def pet(est, se) -> dict:
    """Egger's regression and the precision-effect test (PET): regress the estimate on its standard error, weighted
    by 1/se^2.  The slope measures funnel asymmetry; the intercept is the effect of an infinitely precise study."""
    est, se = np.asarray(est, float), np.asarray(se, float)
    w = 1 / se ** 2
    X = np.column_stack([np.ones_like(se), se])
    W = X * w[:, None]
    b = np.linalg.solve(X.T @ W, W.T @ est)
    e = est - X @ b
    s2 = float((w * e ** 2).sum() / (len(est) - 2))
    V = s2 * np.linalg.inv(X.T @ W)
    return {"intercept": float(b[0]), "slope": float(b[1]), "se_int": float(np.sqrt(V[0, 0])),
            "se_slope": float(np.sqrt(V[1, 1])), "naive": float(np.average(est, weights=w)),
            "mean": float(est.mean())}


def ak_meta(est, se, cut: float = 1.96) -> dict:
    """Andrews and Kasy's meta-study model with study-specific standard errors: latent effects N(theta, tau^2),
    estimates N(effect, se^2), published with relative probability 1 if negative and significant, ``b_ns`` if
    insignificant and ``b_pos`` if positive and significant.  Maximum likelihood for (theta, tau, b_ns, b_pos)."""
    from scipy import optimize, stats

    x, s = np.asarray(est, float), np.asarray(se, float)
    z = x / s

    def nll(par):
        th, lt, l1, l2 = par
        tau, b1, b2 = np.exp(lt), np.exp(l1), np.exp(l2)
        sd = np.sqrt(tau ** 2 + s ** 2)
        w = np.where(z <= -cut, 1.0, np.where(z >= cut, b2, b1))
        pneg = stats.norm.cdf((-cut * s - th) / sd)
        ppos = stats.norm.sf((cut * s - th) / sd)
        pmid = 1 - pneg - ppos
        norm = pneg + b1 * pmid + b2 * ppos
        return -np.sum(np.log(w) + stats.norm.logpdf(x, th, sd) - np.log(norm))

    res = optimize.minimize(nll, x0=[float(np.median(x)), np.log(0.02), 0.0, 0.0], method="Nelder-Mead",
                            options={"maxiter": 8000, "xatol": 1e-7, "fatol": 1e-9})
    th, lt, l1, l2 = res.x
    return {"theta": float(th), "tau": float(np.exp(lt)), "b_ns": float(np.exp(l1)), "b_pos": float(np.exp(l2)),
            "ok": bool(res.success)}


def brock_hommes(betas=None, b_over_B: float = 1.35, C: float = 1.0, T: int = 600, keep: int = 120,
                 seed: int = 673) -> dict:
    """Brock and Hommes's adaptive rational equilibrium dynamics in a cobweb market (price deviations x from the
    steady state): demand -B x_t, supply b times the expected deviation.  A share n_t uses perfect foresight at a cost
    C; the rest expect last period's price, free.  Market clearing gives x_t = -b (1 - n_t) x_{t-1} / (B + b n_t).
    Traders switch by a logit with intensity beta on last period's net advantage of the rational forecast,
    (b/2)(x_{t-1} - x_{t-2})^2 - C.  For each beta, the prices after a burn-in: one point at low beta (a stable
    steady state), cycles, then chaos."""
    betas = np.linspace(0.1, 6.0, 120) if betas is None else np.asarray(betas, float)
    B, b = 1.0, b_over_B
    rng = np.random.default_rng(seed)
    pts_b, pts_x = [], []
    for be in betas:
        x1, x0 = 0.1 + 0.01 * rng.normal(), 0.0
        xs = []
        for t in range(T):
            adv = 0.5 * b * (x1 - x0) ** 2 - C
            n = 1 / (1 + np.exp(-be * adv))
            x = -b * (1 - n) * x1 / (B + b * n)
            x0, x1 = x1, x
            if t >= T - keep:
                xs.append(x)
        pts_b.extend([float(be)] * len(xs))
        pts_x.extend([float(v) for v in xs])
    return {"beta": pts_b, "x": pts_x, "betas": betas, "b_over_B": b_over_B, "C": C}


def brock_hommes_path(beta: float = 5.0, b_over_B: float = 1.35, C: float = 1.0, T: int = 120) -> dict:
    """One path of the same market: prices and the rational share over time."""
    B, b = 1.0, b_over_B
    x1, x0 = 0.1, 0.0
    xs, ns = [], []
    for _ in range(T):
        adv = 0.5 * b * (x1 - x0) ** 2 - C
        n = 1 / (1 + np.exp(-beta * adv))
        x = -b * (1 - n) * x1 / (B + b * n)
        x0, x1 = x1, x
        xs.append(float(x))
        ns.append(float(n))
    return {"x": xs, "n": ns, "beta": beta}


def dial_audit() -> dict:
    """The series' Dials: how many, their statuses, how many estimates each holds, and for dials with positive
    estimates the ratio of the largest to the smallest (how far apart the evidence is)."""
    from explainer.economics import dials

    rows = []
    for k, d in dials.DIALS.items():
        vals = np.array([e.value for e in d.estimates], float)
        film = [e for e in d.estimates if e.who.startswith("this film")]
        pos = vals[vals > 0]
        rows.append({"key": k, "name": d.name, "status": d.status, "n": len(vals), "film": len(film),
                     "spread": float(pos.max() / pos.min()) if len(pos) >= 2 and pos.min() > 0 else None,
                     "parts": list(d.parts)})
    statuses: dict = {}
    for r in rows:
        statuses[r["status"]] = statuses.get(r["status"], 0) + 1
    spreads = sorted([r for r in rows if r["spread"] is not None], key=lambda r: -r["spread"])
    return {"rows": rows, "n_dials": len(rows), "n_estimates": int(sum(r["n"] for r in rows)),
            "n_film": int(sum(r["film"] for r in rows)), "statuses": statuses, "widest": spreads[:8],
            "narrowest": spreads[-8:]}


__all__ = [n for n in dir() if not n.startswith("_") and n not in ("np", "annotations")]
