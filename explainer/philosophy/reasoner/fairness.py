"""Fairness, privacy and explanation for Part 41 ("Fair Machines"): group fairness criteria on a synthetic
population with unequal base rates; Chouldechova's identity and Kleinberg, Mullainathan and Raghavan's balance
conditions; group-specific thresholds; counterfactual fairness on a structural causal model; differential privacy
(the Laplace mechanism, randomized response, composition, and a reconstruction attack); and Shapley-value and
counterfactual explanations."""

from __future__ import annotations

import itertools
import math

import numpy as np


# ---------------------------------------------------------------------------
# A synthetic population (two groups with different base rates)
# ---------------------------------------------------------------------------
def population(n: int = 20000, seed: int = 2016, means=(0.3, 0.5), conc: float = 4.0) -> dict:
    """Each person has a true risk p drawn from a Beta distribution whose mean differs by group (base rates 0.3 and
    0.5), and an outcome y ~ Bernoulli(p). The score given to the classifier is p itself, so it is calibrated within
    each group by construction: among people scored s, a fraction s have y = 1."""
    rng = np.random.default_rng(seed)
    out = {}
    for g, m in zip("AB", means):
        a, b = m * conc, (1 - m) * conc
        p = rng.beta(a, b, n)
        y = (rng.random(n) < p).astype(int)
        out[g] = {"score": p, "y": y}
    return out


def rates(score, y, t: float) -> dict:
    pred = score >= t
    tp = int(np.sum(pred & (y == 1)))
    fp = int(np.sum(pred & (y == 0)))
    fn = int(np.sum(~pred & (y == 1)))
    tn = int(np.sum(~pred & (y == 0)))
    n = len(y)
    return {"tp": tp, "fp": fp, "fn": fn, "tn": tn, "base": round((tp + fn) / n, 4),
            "selected": round((tp + fp) / n, 4), "fpr": round(fp / max(1, fp + tn), 4),
            "fnr": round(fn / max(1, fn + tp), 4), "ppv": round(tp / max(1, tp + fp), 4)}


def criteria(t: float = 0.5, seed: int = 2016) -> dict:
    """One threshold for both groups: demographic parity, equal false-positive and false-negative rates, and equal
    positive predictive value, compared; then Chouldechova's identity FPR = p/(1-p) (1-PPV)/PPV (1-FNR), checked."""
    pop = population(seed=seed)
    r = {g: rates(pop[g]["score"], pop[g]["y"], t) for g in "AB"}
    ident = {}
    for g in "AB":
        p, ppv, fnr = r[g]["base"], r[g]["ppv"], r[g]["fnr"]
        ident[g] = round(p / (1 - p) * (1 - ppv) / ppv * (1 - fnr), 4)
    bal = {g: {"pos": round(float(pop[g]["score"][pop[g]["y"] == 1].mean()), 4),
               "neg": round(float(pop[g]["score"][pop[g]["y"] == 0].mean()), 4)} for g in "AB"}
    calib = {}
    for g in "AB":
        s, yy = pop[g]["score"], pop[g]["y"]
        bins = np.linspace(0, 1, 11)
        idx = np.digitize(s, bins) - 1
        calib[g] = [round(float(yy[idx == k].mean()), 3) if np.any(idx == k) else None for k in range(10)]
    return {"threshold": t, "rates": r, "identity_fpr": ident, "balance": bal, "calibration": calib}


def sweep(ts=None, seed: int = 2016) -> dict:
    """Rates for each group as one shared threshold moves: for drawing the tiles recolouring."""
    pop = population(seed=seed)
    ts = list(ts if ts is not None else np.round(np.linspace(0.1, 0.9, 17), 3))
    out = {g: [rates(pop[g]["score"], pop[g]["y"], t) for t in ts] for g in "AB"}
    hist = {}
    for g in "AB":
        for yv in (0, 1):
            h, _ = np.histogram(pop[g]["score"][pop[g]["y"] == yv], bins=20, range=(0, 1))
            hist[f"{g}{yv}"] = (h / len(pop[g]["y"])).round(4).tolist()
    return {"ts": ts, "rates": out, "hist": hist}


def group_thresholds(fpr_target: float = 0.2, ppv_target: float = 0.7, seed: int = 2016) -> dict:
    """Group-specific thresholds. Choose each group's threshold to give the same false-positive rate (20%): the
    false-negative rates and positive predictive values then differ. Choose them instead to give the same PPV
    (0.70): the error rates differ. (Equalizing both error rates at once needs randomized thresholds, as in Hardt,
    Price and Srebro 2016, and still leaves PPV unequal.)"""
    pop = population(seed=seed)
    grid = np.round(np.linspace(0.05, 0.95, 181), 3)
    R = {g: [(float(t), rates(pop[g]["score"], pop[g]["y"], t)) for t in grid] for g in "AB"}
    out = {}
    for key, target in (("fpr", fpr_target), ("ppv", ppv_target), ("selected", 0.3)):
        pick = {}
        for g in "AB":
            t, r = min(R[g], key=lambda tr: abs(tr[1][key] - target))
            pick[g] = {"t": t, **r, "accuracy": round((r["tp"] + r["tn"]) / len(pop[g]["y"]), 4)}
        out[key] = pick
    single = {g: {"t": 0.5, **rates(pop[g]["score"], pop[g]["y"], 0.5)} for g in "AB"}
    for g in "AB":
        single[g]["accuracy"] = round((single[g]["tp"] + single[g]["tn"]) / len(pop[g]["y"]), 4)
    out["single"] = single
    return {"fpr_target": fpr_target, "ppv_target": ppv_target, "selected_target": 0.3, **out}


def unawareness(n: int = 20000, seed: int = 1971, proxy: float = 0.8) -> dict:
    """Fairness through unawareness fails. Leave the group out of the model, but keep a feature (say, a
    neighbourhood) that matches the group 80% of the time. A model that predicts from the neighbourhood alone
    reproduces most of the gap between the groups' selection rates."""
    pop = population(n=n, seed=seed)
    rng = np.random.default_rng(seed)
    zs, ys, gs = [], [], []
    for gi, g in enumerate("AB"):
        z = np.where(rng.random(n) < proxy, gi, 1 - gi)
        zs.append(z)
        ys.append(pop[g]["y"])
        gs.append(np.full(n, gi))
    z, y, grp = np.concatenate(zs), np.concatenate(ys), np.concatenate(gs)
    pred_rate = {int(k): float(y[z == k].mean()) for k in (0, 1)}
    score = np.array([pred_rate[int(k)] for k in z])
    t = float(np.mean(list(pred_rate.values())))
    sel = {g: round(float((score[grp == gi] > t).mean()), 4) for gi, g in enumerate("AB")}
    base = {g: round(float(y[grp == gi].mean()), 4) for gi, g in enumerate("AB")}
    return {"proxy_match": proxy, "rate_by_zone": {str(k): round(v, 4) for k, v in pred_rate.items()},
            "selected": sel, "base": base}


# ---------------------------------------------------------------------------
# Counterfactual fairness (Kusner, Loftus, Russell and Silva 2017)
# ---------------------------------------------------------------------------
def counterfactual(n: int = 8, seed: int = 2017) -> dict:
    """A linear structural causal model: group A in {0, 1}; ability U ~ N(0, 1); a test score X = U - 1.0 A + noise
    (group 1 is disadvantaged in schooling); the outcome Y = U. Predictor 1 uses X alone; predictor 2 uses the
    abducted ability U_hat = X + 1.0 A. For each person, compute the counterfactual prediction had their group been
    different, holding U and the noise fixed."""
    rng = np.random.default_rng(seed)
    A = np.array([0, 1] * (n // 2))
    U = rng.normal(0, 1, n).round(2)
    E = rng.normal(0, 0.1, n).round(2)
    X = U - 1.0 * A + E
    out = []
    for i in range(n):
        a_cf = 1 - A[i]
        x_cf = U[i] - 1.0 * a_cf + E[i]
        p1, p1_cf = X[i], x_cf
        p2, p2_cf = X[i] + 1.0 * A[i], x_cf + 1.0 * a_cf
        out.append({"A": int(A[i]), "U": float(U[i]), "X": round(float(X[i]), 2), "pred_x": round(float(p1), 2),
                    "pred_x_cf": round(float(p1_cf), 2), "pred_u": round(float(p2), 2),
                    "pred_u_cf": round(float(p2_cf), 2)})
    return {"people": out, "shift_x": 1.0, "fair_u": all(abs(o["pred_u"] - o["pred_u_cf"]) < 1e-9 for o in out)}


# ---------------------------------------------------------------------------
# Differential privacy (Dwork, McSherry, Nissim and Smith 2006)
# ---------------------------------------------------------------------------
def laplace(eps_list=(0.1, 0.5, 1.0, 2.0)) -> dict:
    """The Laplace mechanism for a counting query (sensitivity 1): release the count plus Laplace(1/eps) noise.
    For neighbouring databases with counts c and c + 1, the densities at any output differ by a factor of at most
    e^eps; the expected absolute error is 1/eps."""
    xs = np.linspace(-8, 8, 321)
    out = []
    for e in eps_list:
        b = 1 / e
        dens = np.exp(-np.abs(xs) / b) / (2 * b)
        dens1 = np.exp(-np.abs(xs - 1) / b) / (2 * b)
        ratio = float(np.max(np.maximum(dens / dens1, dens1 / dens)))
        out.append({"eps": e, "scale": b, "density": dens.round(5).tolist(), "shifted": dens1.round(5).tolist(),
                    "max_ratio": round(ratio, 4), "bound": round(math.exp(e), 4), "error": round(b, 3)})
    return {"x": xs.round(3).tolist(), "mechanisms": out}


def randomized_response(n: int = 2000, true_p: float = 0.3, seed: int = 1965) -> dict:
    """Warner (1965): flip a coin; heads, answer truthfully; tails, flip again and answer yes on heads. Each answer
    is yes with probability 1/2 p + 1/4, so p is estimated as 2 (share of yes) - 1/2; each person's answer is
    eps-private with eps = ln 3."""
    rng = np.random.default_rng(seed)
    truth = rng.random(n) < true_p
    first = rng.random(n) < 0.5
    second = rng.random(n) < 0.5
    ans = np.where(first, truth, second)
    share = float(ans.mean())
    est = 2 * share - 0.5
    se = 2 * math.sqrt(share * (1 - share) / n)
    return {"n": n, "true_p": true_p, "share_yes": round(share, 4), "estimate": round(est, 4), "se": round(se, 4),
            "eps": round(math.log(3), 4), "sample_true": round(float(truth.mean()), 4)}


def composition(eps: float = 0.1, ks=(1, 10, 100, 1000), delta: float = 1e-6) -> dict:
    """Privacy loss adds up: k eps-private queries are k eps-private (basic composition), or, with probability
    1 - delta, sqrt(2 k ln(1/delta)) eps + k eps (e^eps - 1) (advanced composition; Dwork, Rothblum and Vadhan 2010)."""
    rows = []
    for k in ks:
        basic = k * eps
        adv = math.sqrt(2 * k * math.log(1 / delta)) * eps + k * eps * (math.exp(eps) - 1)
        rows.append({"k": k, "basic": round(basic, 3), "advanced": round(adv, 3)})
    return {"eps": eps, "delta": delta, "rows": rows}


def reconstruction(n: int = 64, noise_levels=(0.0, 1.0, 2.0, 4.0, 8.0, 16.0), seed: int = 2003) -> dict:
    """Dinur and Nissim (2003): answer many random subset-sum queries about a secret bit vector with bounded noise,
    and the vector can be reconstructed. Here 4n queries, uniform noise of the given size, reconstruction by least
    squares and rounding; report the fraction of bits recovered."""
    rng = np.random.default_rng(seed)
    secret = rng.integers(0, 2, n)
    m = 4 * n
    Q = rng.integers(0, 2, (m, n))
    exact = Q @ secret
    out = []
    for E in noise_levels:
        noisy = exact + rng.uniform(-E, E, m)
        est, *_ = np.linalg.lstsq(Q.astype(float), noisy, rcond=None)
        rec = (est > 0.5).astype(int)
        out.append({"noise": E, "recovered": round(float((rec == secret).mean()), 3)})
    return {"n": n, "queries": m, "results": out, "sqrt_n": round(math.sqrt(n), 2)}


# ---------------------------------------------------------------------------
# Explanation
# ---------------------------------------------------------------------------
def credit_model(x):
    """A toy credit score: income and years of history count, debt counts against, and income and history
    interact."""
    inc, hist, debt = x
    return 0.4 * inc + 0.3 * hist - 0.5 * debt + 0.2 * inc * hist


def explain(x=(1.0, 0.5, 1.2), baseline=(0.0, 0.0, 0.0), threshold: float = 0.2) -> dict:
    """Exact Shapley values of the credit model at x against a baseline (features absent take baseline values),
    checked to add up to f(x) - f(baseline); then the smallest single-feature change that flips a rejection into
    an acceptance: a counterfactual explanation (Wachter, Mittelstadt and Russell 2017)."""
    names = ["income", "history", "debt"]
    n = len(x)

    def v(S):
        z = [x[i] if i in S else baseline[i] for i in range(n)]
        return credit_model(z)

    phi = [0.0] * n
    for order in itertools.permutations(range(n)):
        S = set()
        for i in order:
            before = v(S)
            S.add(i)
            phi[i] += (v(S) - before) / math.factorial(n)
    fx, fb = credit_model(x), credit_model(baseline)
    cfs = []
    for i in range(n):
        for d in sorted(np.round(np.arange(-2.0, 2.0001, 0.01), 2), key=lambda v: (abs(v), v)):
            z = list(x)
            z[i] = round(x[i] + d, 2)
            if credit_model(z) >= threshold:
                cfs.append({"feature": names[i], "change": float(d), "new": float(z[i])})
                break
    best = min(cfs, key=lambda c: abs(c["change"])) if cfs else None
    return {"names": names, "x": list(x), "phi": [round(p, 4) for p in phi], "f": round(fx, 4), "f0": round(fb, 4),
            "sum_ok": abs(sum(phi) - (fx - fb)) < 1e-9, "threshold": threshold, "accepted": fx >= threshold,
            "counterfactuals": cfs, "best": best}
