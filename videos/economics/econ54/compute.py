"""Precompute every number in Part 54 of *Economics, Built* ("Estimating Models").

    python -m videos.economics.econ54.compute            # everything missing (about five minutes)
    python -m videos.economics.econ54.compute --force lifecycle

Results are cached in ``.cache/econ54/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.  Models: Agora's
estimation harness (``agora.estimate``) with the Island's Part 54 truths, and the static unemployment-insurance model
of Part 42 (``agora.insurance``).  Data: the Federal Highway Administration's vehicle miles travelled, via FRED, for
the intermission.

Items:
    bart        McFadden's forecast, the official one, and what happened (from the Called it? record)
    commuters   the Island's commuters: a logit by maximum likelihood, its surface, Newton's path, the value of time
    history     a fuel-price history: a straight line through it against the logit, asked about a congestion
                charge
    rail        a new rail line: the logit's forecast against the truth (a nested logit), and whom rail draws from
    playit      four summary moments of the life cycle and the two parameters: the sensitivity matrix
    gmm         Hansen and Singleton on the Island's returns: estimates, the J-test, a mispriced asset rejected
    ma1         indirect inference against the naive estimator for an MA(1), in repeated samples
    lifecycle   the life-cycle household by simulated moments: the truth recovered, and the profile along the
                ridge (calibrate gamma, estimate beta)
    fragile     wealth over-stated by one percent: the shift predicted by the sensitivity matrix and found by
                estimating again, with efficient and with diagonal weights
    types       a panel with two hidden types: pooled logits against the mixture, and spurious state dependence
    sufficient  the Baily-Chetty formula against the structural model, and extrapolating one elasticity
    school      a schooling model estimated on control villages, predicting the subsidy experiment twice
    bounds      missing outcomes: Manski's bounds, with and without assumptions
    amortized   a learned estimator: simulated samples to parameters
    film        the intermission's data film: America's vehicle miles travelled, 1971-2026
    melody      its data melody
"""

from __future__ import annotations

import numpy as np
from scipy.optimize import brentq, minimize_scalar
from scipy.stats import chi2

from explainer.ai.cache import Cache
from explainer.economics import data, island, score
from explainer.economics.agora import estimate as E
from explainer.economics.agora import insurance as I

CACHE = Cache("econ54")
load = CACHE.load
TRUTH = island.truths(54)
FILM_SECONDS = 46.0
MELODY_SECONDS = FILM_SECONDS + 8.0


# ---------------------------------------------------------------------------------------------------------------
# the hook


def compute_bart() -> dict:
    """The numbers of the BART forecast, as recorded in the Called it? entry ``mcfadden_bart`` (Part 5)."""
    return {"official": 15.0, "mcfadden": 6.3, "actual": 6.2, "year_forecast": 1973, "year_actual": 1975}


# ---------------------------------------------------------------------------------------------------------------
# random utility


def commuters_data() -> dict:
    C = TRUTH["commuters"]
    return E.simulate_commuters(C["n"], C["beta"], C["asc"], C["seed"])


def compute_commuters() -> dict:
    d = commuters_data()
    r = E.logit_ml(d["X"], d["y"])
    b, cov = r["b"], r["cov"]
    vot = 60 * b[0] / b[1]
    g = np.array([60 / b[1], -60 * b[0] / b[1] ** 2])
    se_vot = float(np.sqrt(g @ cov[:2, :2] @ g))
    bt = np.linspace(-0.11, 0.01, 49)
    bc = np.linspace(-1.0, 0.1, 45)
    ll = np.array([[E.logit_loglik(d["X"], d["y"], [x, z, b[2]]) for x in bt] for z in bc])
    # the S-curve: choices binned by the fitted utility difference
    dv = (d["X"][:, 1] - d["X"][:, 0]) @ b[:2] + b[2]
    edges = np.quantile(dv, np.linspace(0, 1, 13))
    mids, obs = [], []
    for lo, hi in zip(edges[:-1], edges[1:]):
        sel = (dv >= lo) & (dv <= hi)
        mids.append(float(dv[sel].mean()))
        obs.append(float((d["y"][sel] == 1).mean()))
    xs = np.linspace(edges[0], edges[-1], 121)
    C = TRUTH["commuters"]
    return {"b": b.tolist(), "se": r["se"].tolist(), "truth": list(C["beta"]) + [C["asc"][1]],
            "loglik": r["loglik"], "iters": r["iters"], "trace": r["trace"].tolist(), "vot": float(vot),
            "se_vot": se_vot, "vot_truth": 60 * C["beta"][0] / C["beta"][1], "n": C["n"],
            "bus_share": float((d["y"] == 1).mean()), "grid_t": bt.tolist(), "grid_c": bc.tolist(),
            "ll": ll.tolist(), "ll_max": float(ll.max()), "mids": mids, "obs": obs, "xs": xs.tolist(),
            "curve": (1 / (1 + np.exp(-xs))).tolist(),
            "time_range": [15, 45, 25, 70], "cost_range": [2, 8, 0.5, 2.5]}


def compute_history() -> dict:
    """Twelve years in which the price of fuel moved the cost of a car trip by between -$1 and +$1.50: the car's
    share each year from the true logit and three thousand commuters' choices; a straight line through that history,
    and the logit estimated on the cross-section, both asked about a congestion charge of $8 a trip."""
    C = TRUTH["commuters"]
    d = commuters_data()
    beta, asc = np.array(C["beta"]), np.array(C["asc"])
    rng = np.random.default_rng(541)
    shifts = np.round(rng.uniform(-1.0, 1.5, 12), 2)
    X = d["X"]

    def share(delta, b=beta, a=asc):
        v = X @ b + a[None, :]
        v[:, 0] += b[1] * delta
        return float((1 / (1 + np.exp(v[:, 1] - v[:, 0]))).mean())

    true_sh = np.array([share(s_) for s_ in shifts])
    obs = rng.binomial(C["n"], true_sh) / C["n"]
    A = np.column_stack([np.ones(len(shifts)), shifts])
    coef = np.linalg.lstsq(A, obs, rcond=None)[0]
    est = load("commuters")
    bh = np.array(est["b"])
    ah = np.array([0.0, bh[2]])
    grid = np.linspace(-1.5, 9.0, 85)
    charge = 8.0
    return {"shifts": shifts.tolist(), "obs": obs.tolist(), "line": coef.tolist(), "grid": grid.tolist(),
            "truth_curve": [share(x) for x in grid], "logit_curve": [share(x, bh[:2], ah) for x in grid],
            "charge": charge, "charge_line": float(coef[0] + coef[1] * charge), "charge_truth": share(charge),
            "charge_logit": share(charge, bh[:2], ah), "now_truth": share(0.0),
            "mean_car_cost": float(X[:, 0, 1].mean())}


def compute_rail() -> dict:
    """A rail line opens: 35 minutes and $2.50 for everyone. The truth is a nested logit in which bus and rail
    share a nest (lambda 0.5: people who dislike the car's alternatives dislike both); the forecaster has the logit
    estimated before rail existed, and gives rail the bus's constant."""
    C = TRUTH["commuters"]
    rail = C["rail"]
    d = commuters_data()
    beta = np.array(C["beta"])
    est = load("commuters")
    bh = np.array(est["b"])
    n = d["X"].shape[0]
    Xr = np.concatenate([d["X"], np.tile([[[rail["time"], rail["cost"]]]], (n, 1, 1))], axis=1)
    V_true = Xr @ beta + np.array([C["asc"][0], C["asc"][1], rail["asc"]])[None, :]
    before = E.nested_shares(V_true[:, :2], [[0], [1]], [1.0, 1.0]).mean(axis=0)
    after_true = E.nested_shares(V_true, [[0], [1, 2]], [1.0, C["nest_lambda"]]).mean(axis=0)
    V_hat = Xr @ bh[:2] + np.array([0.0, bh[2], bh[2]])[None, :]
    before_hat = E.nested_shares(V_hat[:, :2], [[0], [1]], [1.0, 1.0]).mean(axis=0)
    after_logit = E.nested_shares(V_hat, [[0], [1, 2]], [1.0, 1.0]).mean(axis=0)
    # the forecaster with the right constant, to separate the two mistakes
    V_hat2 = Xr @ bh[:2] + np.array([0.0, bh[2], rail["asc"]])[None, :]
    after_logit2 = E.nested_shares(V_hat2, [[0], [1, 2]], [1.0, 1.0]).mean(axis=0)

    def from_bus(b0, a1):
        lost_car, lost_bus = b0[0] - a1[0], b0[1] - a1[1]
        return float(lost_bus / (lost_car + lost_bus))

    return {"before": before.tolist(), "after_true": after_true.tolist(), "before_hat": before_hat.tolist(),
            "after_logit": after_logit.tolist(), "after_logit_rightconst": after_logit2.tolist(),
            "from_bus_true": from_bus(before, after_true), "from_bus_logit": from_bus(before_hat, after_logit),
            "rail": rail, "lam": C["nest_lambda"]}


# ---------------------------------------------------------------------------------------------------------------
# Play it: which moment pins which parameter


def lifecycle_contrib(beta: float, gamma: float, n: int, seed: int) -> np.ndarray:
    return E.lifecycle_moments(E.lifecycle(beta, gamma), n=n, seed=seed, per_person=True)


def summary4(contrib: np.ndarray) -> np.ndarray:
    """Per-person contributions to four summary moments from the bins (ten five-year consumption bins, then wealth
    bins 5 to 10): consumption growth while young (ages 30-34 against 20-24 if the working life starts at 20),
    wealth just before retirement (55-59), wealth in the last years (65-69), and the change in consumption at
    retirement (60-69 against 50-59)."""
    c = contrib[:, :10]
    w = contrib[:, 10:]
    return np.column_stack([c[:, 2] - c[:, 0], w[:, 3], w[:, 5], (c[:, 8] + c[:, 9]) / 2 - (c[:, 6] + c[:, 7]) / 2])


def compute_playit() -> dict:
    L = TRUTH["lifecycle"]
    n = L["n"]
    base = summary4(lifecycle_contrib(L["beta"], L["gamma"], n, L["seed"]))
    m0 = base.mean(axis=0)
    V = np.cov(base, rowvar=False) / n
    G = np.empty((4, 2))
    for j, (hb, hg) in enumerate(((0.002, 0.0), (0.0, 0.05))):
        up = summary4(lifecycle_contrib(L["beta"] + hb, L["gamma"] + hg, n, L["seed"])).mean(axis=0)
        dn = summary4(lifecycle_contrib(L["beta"] - hb, L["gamma"] - hg, n, L["seed"])).mean(axis=0)
        G[:, j] = (up - dn) / (2 * (hb + hg))
    W = np.linalg.inv(V)
    Lam = -E.sensitivity(G, W)  # per unit rise in each data moment
    Sig = np.linalg.inv(G.T @ W @ G)
    std = Lam * np.sqrt(np.diag(V))[None, :] / np.sqrt(np.diag(Sig))[:, None]
    names = ["consumption growth while young", "wealth just before retirement", "wealth in the last years",
             "consumption's change at retirement"]
    return {"moments": m0.tolist(), "names": names, "G": G.tolist(), "Lambda": Lam.tolist(),
            "standardized": std.tolist(), "se": np.sqrt(np.diag(Sig)).tolist(), "Sigma": Sig.tolist(),
            "ratio": (G[:, 0] / G[:, 1]).tolist(), "truth": [L["beta"], L["gamma"]],
            "best_for": [int(np.argmax(np.abs(std[i]))) for i in range(2)]}


# ---------------------------------------------------------------------------------------------------------------
# GMM


def compute_gmm() -> dict:
    T = TRUTH["euler"]
    dat = E.euler_data(T=T["T"], beta=T["beta"], gamma=T["gamma"], seed=T["seed"])
    f = E.euler_moments(dat)
    r = E.gmm(f, [0.95, 2.0])
    # a third asset whose return is one point higher than the model can price
    rng = np.random.default_rng(T["seed"] + 1)
    su = 0.06
    c = -np.log(T["beta"]) - su ** 2 / 2 + T["bad_premium"]
    R3 = np.exp(c + T["gamma"] * dat["g"][1:] + su * rng.standard_normal(T["T"]))
    bad = {"g": dat["g"], "R": np.column_stack([dat["R"], R3])}
    rb = E.gmm(E.euler_moments(bad), [0.95, 2.0])
    W = r["W"]
    bs = np.linspace(0.90, 1.04, 57)
    gs = np.linspace(0.0, 6.0, 49)
    obj = np.array([[float(r["n"] * f([b, g]).mean(axis=0) @ W @ f([b, g]).mean(axis=0)) for b in bs] for g in gs])
    xs = np.linspace(0, 40, 201)
    return {"theta": r["theta"].tolist(), "se": r["se"].tolist(), "J": r["J"], "df": r["df"], "p_J": r["p_J"],
            "bad_theta": rb["theta"].tolist(), "bad_se": rb["se"].tolist(), "bad_J": rb["J"], "bad_df": rb["df"],
            "bad_p": rb["p_J"], "truth": [T["beta"], T["gamma"]], "T": T["T"], "premium": T["bad_premium"],
            "grid_b": bs.tolist(), "grid_g": gs.tolist(), "obj": obj.tolist(), "crit": float(chi2.ppf(0.95, r["df"])),
            "bad_crit": float(chi2.ppf(0.95, rb["df"])), "chi_x": xs.tolist(),
            "chi_pdf": chi2.pdf(xs, r["df"]).tolist(), "bad_chi_pdf": chi2.pdf(xs, rb["df"]).tolist(),
            "corr": float(r["cov"][0, 1] / np.sqrt(r["cov"][0, 0] * r["cov"][1, 1]))}


# ---------------------------------------------------------------------------------------------------------------
# indirect inference


def compute_ma1() -> dict:
    M = TRUTH["ma1"]
    naive, ii = [], []
    for k in range(M["reps"]):
        y = E.ma1_data(M["theta"], M["n"], 5400 + k)
        r = E.indirect_ma1(y, seed=9000 + k)
        naive.append(r["naive"])
        ii.append(r["theta"])
    naive, ii = np.array(naive), np.array(ii)
    bins = np.linspace(-0.1, 1.0, 23)

    def summ(a):
        return {"mean": float(a.mean()), "sd": float(a.std()), "rmse": float(np.sqrt(np.mean((a - M["theta"]) ** 2))),
                "hist": np.histogram(a, bins)[0].tolist()}

    y = E.ma1_data(M["theta"], M["n"], 5400)
    one = E.indirect_ma1(y, seed=9000)
    return {"naive": summ(naive), "ii": summ(ii), "bins": bins.tolist(), "theta": M["theta"], "n": M["n"],
            "reps": M["reps"], "example": y[:80].tolist(), "aux": one["aux"].tolist(), "one_ii": one["theta"],
            "one_naive": one["naive"], "r1": one["r1"]}


# ---------------------------------------------------------------------------------------------------------------
# the life cycle by simulated moments


def _simulator(L):
    def simulate(th):
        sol = E.lifecycle(float(th[0]), float(th[1]))
        return np.mean([E.lifecycle_moments(sol, n=L["n"], seed=100 + s) for s in range(L["S"])], axis=0)

    return simulate


def _data(L, bump: float = 0.0):
    sol = E.lifecycle(L["beta"], L["gamma"])
    contrib = E.lifecycle_moments(sol, n=L["n"], seed=L["seed"], per_person=True)
    if bump:
        contrib = contrib.copy()
        contrib[:, 10:] *= 1 + bump
    return contrib


def compute_lifecycle() -> dict:
    """The Island's households by simulated moments (efficient weights), and the profile: for each value of gamma,
    the best beta and how well it fits."""
    L = TRUTH["lifecycle"]
    contrib = _data(L)
    dm = contrib.mean(axis=0)
    simulate = _simulator(L)
    r = E.smm(dm, contrib, simulate, L["start"], step=[0.01, 0.5], S=L["S"])
    keep, W, target = r["keep"], r["W"], r["target"]

    def obj(th):
        diff = simulate(th)[keep] - target
        return float(diff @ W @ diff)

    prof = []
    for g in np.linspace(1.0, 4.0, 13):
        b0 = L["beta"] - 0.011 * (g - L["gamma"])
        rr = minimize_scalar(lambda b: obj([b, g]), bounds=(b0 - 0.01, b0 + 0.01), method="bounded",
                             options={"xatol": 1e-7})
        prof.append({"gamma": float(g), "beta": float(rr.x), "obj": float(rr.fun) / (1 + 1 / L["S"])})
    fit = r["fitted"]
    full_fit = np.full(len(dm), np.nan)
    full_fit[keep] = fit
    ages = (np.arange(10) * 5 + 2.5 + 20).tolist()
    Lam = -E.sensitivity(r["G"], W)  # per unit rise in each data moment (the conditions are model minus data)
    std = Lam * np.sqrt(np.diag(r["V"]))[None, :] / r["se"][:, None]
    return {"theta": r["theta"].tolist(), "se": r["se"].tolist(), "truth": [L["beta"], L["gamma"]],
            "start": list(L["start"]), "J": r["J"], "df": r["df"], "p_J": r["p_J"], "evals": r["evals"],
            "data": dm.tolist(), "fitted": full_fit.tolist(), "keep": keep.tolist(), "ages": ages,
            "wealth_ages": ages[4:], "profile": prof, "Lambda": Lam.tolist(), "standardized": std.tolist(),
            "n": L["n"], "S": L["S"], "G": r["G"].tolist(),
            "corr": float(r["cov"][0, 1] / np.sqrt(r["cov"][0, 0] * r["cov"][1, 1])),
            "crit": float(chi2.ppf(0.95, r["df"]))}


def compute_fragile() -> dict:
    """What a one-percent over-statement of wealth in the data does to the estimates: predicted by Andrews, Gentzkow
    and Shapiro's sensitivity matrix and found by estimating again, with efficient weights and with weights that
    ignore the moments' correlations."""
    L = TRUTH["lifecycle"]
    bump = 0.01
    simulate = _simulator(L)
    base = load("lifecycle")
    out = {"bump": bump}
    for name, diag in (("efficient", False), ("diagonal", True)):
        c0 = _data(L)
        r0 = E.smm(c0.mean(axis=0), c0, simulate, base["theta"], step=[0.003, 0.1], S=L["S"], diagonal=diag)
        c1 = _data(L, bump)
        r1 = E.smm(c1.mean(axis=0), c1, simulate, r0["theta"], step=[0.003, 0.1], S=L["S"], diagonal=diag)
        Lam = E.sensitivity(r0["G"], r0["W"])
        dm = c1.mean(axis=0) - c0.mean(axis=0)
        # the conditions are simulated minus data moments: a rise dm in the data moves the estimate by -Lambda dm
        out[name] = {"theta": r0["theta"].tolist(), "se": r0["se"].tolist(),
                     "pred": (-Lam @ dm[r0["keep"]]).tolist(), "actual": (r1["theta"] - r0["theta"]).tolist(),
                     "per_data_gamma": (-Lam[1]).tolist()}
    return out


# ---------------------------------------------------------------------------------------------------------------
# heterogeneity


def compute_types() -> dict:
    T = TRUTH["types"]
    rng = np.random.default_rng(T["seed"])
    P, n_t = T["people"], T["T"] + 1
    low = rng.random(P) < T["share_low"]
    alpha = np.where(low, T["alpha"][0], T["alpha"][1])
    g = np.repeat(np.arange(P), n_t)
    x = rng.standard_normal(P * n_t)
    y = (rng.random(P * n_t) < 1 / (1 + np.exp(-(alpha[g] + T["b"] * x)))).astype(float)
    lag = np.roll(y, 1)
    keep = np.tile(np.arange(n_t) > 0, P)
    xk, yk, lk, gk = x[keep], y[keep], lag[keep], g[keep]
    p1 = E.pooled_logit(xk, yk)
    p2 = E.pooled_logit(np.column_stack([xk, lk]), yk)
    m1 = E.mixture_logit_em(xk, yk, T["T"], gk)
    m2 = E.mixture_logit_em(np.column_stack([xk, lk]), yk, T["T"], gk)
    # people's shares of ones, for the picture
    rate = np.bincount(gk, weights=yk) / T["T"]
    return {"truth": {"alpha": list(T["alpha"]), "b": T["b"], "share_low": T["share_low"], "lag": 0.0},
            "pooled_b": float(p1["b"][1]), "pooled_b_se": float(p1["se"][1]),
            "pooled_lag": float(p2["b"][2]), "pooled_lag_se": float(p2["se"][2]),
            "mix_alpha": m1["alpha"].tolist(), "mix_b": m1["b"], "mix_share": m1["share_low"],
            "mix_lag": float(m2["b"][1]), "mix_lag_b": float(m2["b"][0]), "people": P, "T": T["T"],
            "rate_hist": np.histogram(rate, np.linspace(0, 1, T["T"] + 2))[0].tolist(),
            "rate_low": np.histogram(rate[low], np.linspace(0, 1, T["T"] + 2))[0].tolist()}


# ---------------------------------------------------------------------------------------------------------------
# sufficient statistics


def compute_sufficient() -> dict:
    m = I.Baily(**island.truths(42)["baily"])
    bs = np.round(np.linspace(0.02, 0.60, 59), 4)
    sides = [m.sides(float(b)) for b in bs]
    welfare = np.array([s["welfare"] for s in sides])
    slope = np.gradient(welfare, bs)
    formula = np.array([s["gain"] - s["cost"] for s in sides])
    bstar = m.optimum()
    b0 = 0.2
    eps0 = m.elasticity(b0)
    # an analyst with one experiment at b0: the elasticity assumed the same at every benefit
    eps_b = [m.elasticity(float(b)) for b in bs]

    def gap(b):
        s = m.sides(b)
        return s["gain"] - eps0 / s["e"]

    b_const = brentq(gap, 0.05, 0.6)
    return {"b": bs.tolist(), "welfare": welfare.tolist(), "slope": slope.tolist(), "formula": formula.tolist(),
            "gain": [s["gain"] for s in sides], "cost": [s["cost"] for s in sides], "eps": eps_b,
            "bstar": bstar, "b0": b0, "eps0": eps0, "b_const": float(b_const),
            "drop0": m.sides(b0)["drop"], "e0": m.sides(b0)["e"]}


# ---------------------------------------------------------------------------------------------------------------
# validation and bounds


def compute_school() -> dict:
    S = TRUTH["school"]
    out = {}
    for name, lab in (("money", 0.0), ("label", S["label_effect"])):
        d = E.school_villages(S["villages"], S["per"], subsidy=S["subsidy"], label_effect=lab, seed=S["seed"])
        v = E.validate_subsidy(d)
        out[name] = {k: (val.tolist() if isinstance(val, np.ndarray) else val) for k, val in v.items()}
    out["subsidy"] = S["subsidy"]
    out["label_effect"] = S["label_effect"]
    out["villages"] = S["villages"]
    out["per"] = S["per"]
    return out


def compute_bounds() -> dict:
    from explainer.stats.kit import quasi

    S = TRUTH["school"]
    d = E.school_villages(S["villages"], S["per"], subsidy=S["subsidy"], seed=S["seed"])
    rng = np.random.default_rng(S["seed"] + 2)
    y, t = d["y"], d["treated"]
    # records are missing more often for children who do not attend (a school's register misses dropouts)
    p_miss = np.where(y > 0, 0.6 * S["missing"], 1.5 * S["missing"])
    r = rng.random(len(y)) >= p_miss
    mb = quasi.manski(y, t, r, 0.0, 1.0)
    arms = {k: list(v) for k, v in mb["arms"].items()}
    obs = {k: float(y[r & m].mean()) for k, m in (("1", t), ("0", ~t))}
    miss = {k: float(1 - r[m].mean()) for k, m in (("1", t), ("0", ~t))}
    # monotone missingness: those missing attend no more often than those observed
    mono = {k: (arms[k][0], obs[k]) for k in ("1", "0")}
    truth = {k: float(y[m].mean()) for k, m in (("1", t), ("0", ~t))}
    return {"arms": arms, "effect": [mb["lo"], mb["hi"]], "observed": obs, "missing": miss,
            "naive_effect": obs["1"] - obs["0"], "mono": {k: list(v) for k, v in mono.items()},
            "mono_effect": [mono["1"][0] - mono["0"][1], mono["1"][1] - mono["0"][0]], "truth": truth,
            "true_effect": truth["1"] - truth["0"]}


# ---------------------------------------------------------------------------------------------------------------
# the frontier


def compute_amortized() -> dict:
    r = E.amortized_ma1(n=400, train=3000, test=300, seed=54)
    return {"theta": r["theta"].tolist(), "pred": r["pred"].tolist(), "rmse": r["rmse"], "n": 400,
            "train": 3000}


# ---------------------------------------------------------------------------------------------------------------
# the intermission


def film_time(t: float, first: float = 1971.0, last: float = 2026.75) -> float:
    return 1.5 + FILM_SECONDS * (t - first) / (last - first)


def compute_film() -> dict:
    s = data.fred("M12MTVUSM227NFWA")
    pts = [(int(d[:4]) + (int(d[5:7]) - 1) / 12, v / 1e6) for d, v in zip(s["date"], s["value"]) if np.isfinite(v)]
    pts = [p for p in pts if p[0] >= 1971]
    t = [p[0] for p in pts]
    v = [p[1] for p in pts]
    k = int(np.argmax([x if tt < 2020.2 else 0 for tt, x in zip(t, v)]))
    covid = [i for i, tt in enumerate(t) if 2020 <= tt < 2022]
    low = min(covid, key=lambda i: v[i])
    return {"t": t, "v": v, "times": [film_time(x) for x in t], "first": s["date"][0], "last": s["date"][-1],
            "peak_2007": float(max(x for tt, x in zip(t, v) if 2006 <= tt < 2009)),
            "peak_2007_t": max(((x, tt) for tt, x in zip(t, v) if 2006 <= tt < 2009))[1],
            "pre_covid": v[k], "pre_covid_t": t[k], "covid_low": v[low], "covid_low_t": t[low], "end": v[-1],
            "end_t": t[-1], "start": v[0], "start_t": t[0]}


def compute_melody() -> dict:
    from explainer.music.monochord.audio import Clip, ClipStore

    f = compute_film()
    vals = np.array(f["v"])
    times = f["times"]
    mel = score.data_melody(vals, MELODY_SECONDS, times=times, act=10, log=False, low=45, high=84)
    events = {"film_end": film_time(f["t"][-1]) + 6.0, "first": times[0]}
    clip = Clip(mel["y"], score.SR, events=events,
                notes=[{"t": float(tt), "dur": 0.15, "hz": score.hz(nn), "name": f"{x:.2f} trillion miles"}
                       for tt, nn, x in zip(times, mel["notes"], vals)],
                meta={"label": "America's vehicle miles travelled over the past twelve months, 1971-2026 (Federal "
                               "Highway Administration, via FRED), as a tune (computed)", "kind": "synthesized"})
    ClipStore("econ54").save("intermission.melody", clip)
    return {"times": times, "notes": mel["notes"], "seconds": MELODY_SECONDS}


ITEMS = {
    "bart": compute_bart,
    "commuters": compute_commuters,
    "history": compute_history,
    "rail": compute_rail,
    "playit": compute_playit,
    "gmm": compute_gmm,
    "ma1": compute_ma1,
    "lifecycle": compute_lifecycle,
    "fragile": compute_fragile,
    "types": compute_types,
    "sufficient": compute_sufficient,
    "school": compute_school,
    "bounds": compute_bounds,
    "amortized": compute_amortized,
    "film": compute_film,
    "melody": compute_melody,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
