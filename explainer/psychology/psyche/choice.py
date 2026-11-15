"""Psyche's choices (Part 26): gambles, prospect theory, heuristics, time and experience.

A *lottery* is an array of rows ``(p, x)``: probability and outcome.  Everything here is a small, checkable
calculation: expected value and utility, the St Petersburg game, the probability triangle, cumulative prospect theory
(Tversky and Kahneman 1992) with its certainty equivalents and the fourfold pattern, a choice rule fitted to open
choice data, Bayes's rule in probabilities and natural frequencies, take-the-best against regression out of
sample, the hot-hand streak bias (Miller and Sanjurjo 2018) by exact enumeration, discounting over time, choices
from small samples, and decision by sampling.

Nothing here imports manim.
"""

from __future__ import annotations

import itertools

import numpy as np
from scipy.optimize import brentq, minimize

__all__ = [
    "lottery", "ev", "eu", "st_petersburg_ev", "st_petersburg_ce", "triangle", "eu_slope",
    "TK92", "value", "w_tk", "w_prelec", "cpt", "ce", "fourfold", "pad", "cpt_batch", "MODELS", "predict",
    "fit_model", "cv_models", "framing", "bayes", "natural_frequencies", "environment", "ttb_order",
    "compare_pairs", "heuristics_cv", "streak_props", "streak_exact", "streak_sim", "discount", "reversal_delay",
    "p_never_seen", "sample_choices", "dbs_value",
]


# ---------------------------------------------------------------------------------------------------- lotteries
def lottery(*pairs) -> np.ndarray:
    """``lottery((0.33, 2500), (0.66, 2400), (0.01, 0))``: rows (p, x); zero-probability rows are dropped and the
    probabilities must sum to one."""
    L = np.array(pairs, dtype=float).reshape(-1, 2)
    L = L[L[:, 0] > 0]
    if abs(L[:, 0].sum() - 1) > 1e-9:
        raise ValueError(f"probabilities sum to {L[:, 0].sum()}")
    return L


def ev(L) -> float:
    L = np.asarray(L, float)
    return float((L[:, 0] * L[:, 1]).sum())


def eu(L, u) -> float:
    L = np.asarray(L, float)
    return float((L[:, 0] * u(L[:, 1])).sum())


def st_petersburg_ev(n_terms: int) -> np.ndarray:
    """Expected value of the St Petersburg game cut off after ``k`` tosses, for k = 1..n: a head first at toss k
    (probability 2^-k) pays 2^k ducats, so every term adds one ducat and the sum grows without bound."""
    return np.arange(1, n_terms + 1, dtype=float)


def st_petersburg_ce(wealth: float, terms: int = 200) -> float:
    """What a Bernoulli (log-utility) player with ``wealth`` would pay for the game: the price c solving
    sum_k 2^-k log(w - c + 2^k) = log w (Bernoulli 1738).  With w = 0 the game alone is worth 4 ducats in log terms;
    this returns the buying price, which needs w > 0."""
    k = np.arange(1, terms + 1, dtype=float)
    p = 0.5 ** k

    def f(c):
        return (p * np.log(wealth - c + 2.0 ** k)).sum() - np.log(wealth)

    return float(brentq(f, 0.0, wealth + 1.999999))


def triangle(L, outcomes) -> tuple:
    """A lottery over three outcomes x1 < x2 < x3 as a point of the Marschak–Machina triangle: (p1, p3), the
    probabilities of the worst and the best outcome."""
    L = np.asarray(L, float)
    x1, _, x3 = outcomes
    p1 = L[np.isclose(L[:, 1], x1), 0].sum()
    p3 = L[np.isclose(L[:, 1], x3), 0].sum()
    return float(p1), float(p3)


def eu_slope(u1: float, u2: float, u3: float) -> float:
    """The slope dp3/dp1 of every expected-utility indifference line in the triangle, (u2 - u1) / (u3 - u2): all
    parallel, whatever the utility, which is the independence axiom drawn."""
    return (u2 - u1) / (u3 - u2)


# ------------------------------------------------------------------------------------------- prospect theory
TK92 = {"alpha": 0.88, "beta": 0.88, "lam": 2.25, "gamma": 0.61, "delta": 0.69}  # Tversky and Kahneman (1992)


def value(x, alpha=0.88, beta=0.88, lam=2.25):
    """The value function: x^alpha for gains, -lam (-x)^beta for losses, measured from the reference point."""
    x = np.asarray(x, float)
    return np.where(x >= 0, np.abs(x) ** alpha, -lam * np.abs(x) ** beta)


def w_tk(p, gamma):
    """Tversky and Kahneman's (1992) weighting function p^g / (p^g + (1 - p)^g)^(1/g)."""
    p = np.clip(np.asarray(p, float), 0.0, 1.0)
    a = p ** gamma
    return a / (a + (1 - p) ** gamma) ** (1 / gamma)


def w_prelec(p, a, b=1.0):
    """Prelec's (1998) weighting function exp(-b (-ln p)^a)."""
    p = np.clip(np.asarray(p, float), 1e-300, 1.0)
    return np.exp(-b * (-np.log(p)) ** a)


def pad(lotteries) -> tuple:
    """A list of lotteries as padded arrays (P, X), each row sorted by outcome; padding has p = 0 and x = 0."""
    k = max(len(L) for L in lotteries)
    P = np.zeros((len(lotteries), k))
    X = np.zeros((len(lotteries), k))
    for i, L in enumerate(lotteries):
        L = np.asarray(L, float)
        o = np.argsort(L[:, 1], kind="stable")
        P[i, :len(L)] = L[o, 0]
        X[i, :len(L)] = L[o, 1]
    o = np.argsort(X, axis=1, kind="stable")
    return np.take_along_axis(P, o, 1), np.take_along_axis(X, o, 1)


def cpt_batch(P, X, alpha=0.88, beta=0.88, lam=2.25, gamma=0.61, delta=0.69) -> np.ndarray:
    """Cumulative prospect theory's value of many lotteries at once (rows of the padded, sorted arrays).  A gain's
    decision weight is w+(P(X >= x)) - w+(P(X > x)); a loss's is w-(P(X <= x)) - w-(P(X < x))."""
    head_le = np.cumsum(P, 1)
    head_lt = head_le - P
    tail_ge = np.cumsum(P[:, ::-1], 1)[:, ::-1]
    tail_gt = tail_ge - P
    pi = np.where(X >= 0, w_tk(tail_ge, gamma) - w_tk(tail_gt, gamma),
                  w_tk(head_le, delta) - w_tk(head_lt, delta))
    return (pi * value(X, alpha, beta, lam)).sum(1)


def cpt(L, alpha=0.88, beta=0.88, lam=2.25, gamma=0.61, delta=0.69) -> float:
    P, X = pad([L])
    return float(cpt_batch(P, X, alpha, beta, lam, gamma, delta)[0])


def ce(L, alpha=0.88, beta=0.88, lam=2.25, gamma=0.61, delta=0.69) -> float:
    """The certainty equivalent: the sure amount whose value equals the lottery's."""
    V = cpt(L, alpha, beta, lam, gamma, delta)
    return float(V ** (1 / alpha)) if V >= 0 else float(-((-V / lam) ** (1 / beta)))


def fourfold(params=None, probs=(0.01, 0.05, 0.1, 0.25, 0.5, 0.75, 0.9, 0.95, 0.99), amount=100.0) -> dict:
    """Certainty equivalents of "``amount`` with probability p, else nothing", for gains and losses: below the
    expected value is risk aversion, above it risk seeking."""
    q = {**TK92, **(params or {})}
    gains = np.array([ce(lottery((p, amount), (1 - p, 0.0)), **q) for p in probs])
    losses = np.array([ce(lottery((p, -amount), (1 - p, 0.0)), **q) for p in probs])
    return {"p": np.array(probs), "gain_ce": gains, "loss_ce": losses, "ev": np.array(probs) * amount}


def framing(params=None, n=600) -> dict:
    """The disease problem (Tversky and Kahneman 1981) valued by cumulative prospect theory.  Saved frame
    (reference: all die): 200 saved for sure, or 1/3 chance all 600 saved.  Death frame (reference: all live): 400
    die for sure, or 2/3 chance all 600 die.  Same outcomes, opposite preferences."""
    q = {**TK92, **(params or {})}
    sure_g = cpt(lottery((1.0, n / 3)), **q)
    risk_g = cpt(lottery((1 / 3, n), (2 / 3, 0.0)), **q)
    sure_l = cpt(lottery((1.0, -2 * n / 3)), **q)
    risk_l = cpt(lottery((2 / 3, -n), (1 / 3, 0.0)), **q)
    return {"saved_sure": sure_g, "saved_risky": risk_g, "die_sure": sure_l, "die_risky": risk_l,
            "saved_choice": "sure" if sure_g > risk_g else "risky",
            "die_choice": "sure" if sure_l > risk_l else "risky"}


# ------------------------------------------------------------------------------------ fitting choice data
# each model: parameter names, starting values, bounds; the last parameter is the choice rule's sensitivity
MODELS = {
    "ev": (("tau",), (0.1,), ((1e-4, 10.0),)),
    "eu": (("alpha", "tau"), (0.8, 0.2), ((0.2, 1.5), (1e-4, 10.0))),
    "pt_noweight": (("alpha", "lam", "tau"), (0.8, 1.5, 0.2), ((0.2, 1.5), (0.3, 6.0), (1e-4, 10.0))),
    "cpt": (("alpha", "lam", "gamma", "delta", "tau"), (0.88, 2.25, 0.61, 0.69, 0.2),
            ((0.2, 1.5), (0.3, 6.0), (0.2, 1.5), (0.2, 1.5), (1e-4, 10.0))),
}


def _values(model, theta, P, X):
    if model == "ev":
        return (P * X).sum(1)
    if model == "eu":
        return (P * value(X, theta[0], theta[0], 1.0)).sum(1)
    if model == "pt_noweight":
        return (P * value(X, theta[0], theta[0], theta[1])).sum(1)
    a, lam, g, d = theta[:4]
    return cpt_batch(P, X, a, a, lam, g, d)


def predict(model, theta, A, B) -> np.ndarray:
    """P(choose B) by a logistic choice rule on the value difference; ``A`` and ``B`` are padded (P, X) pairs."""
    d = _values(model, theta, *B) - _values(model, theta, *A)
    z = np.clip(theta[-1] * d, -60, 60)
    return 1 / (1 + np.exp(-z))


def fit_model(model, A, B, rate, start=None) -> dict:
    """Least squares on the choice rates (as the choice prediction competitions score), by Nelder–Mead within the
    bounds; returns the parameters by name and the mean squared error."""
    names, s0, bounds = MODELS[model]
    lo = np.array([b[0] for b in bounds])
    hi = np.array([b[1] for b in bounds])

    def loss(t):
        if np.any(t < lo) or np.any(t > hi):
            return 1e3
        return float(((predict(model, t, A, B) - rate) ** 2).mean())

    best = None
    for s in ([s0] if start is None else [start]) + ([] if len(s0) == 1 else [np.array(s0) * 0.8]):
        r = minimize(loss, np.array(s, float), method="Nelder-Mead",
                     options={"maxiter": 4000, "xatol": 1e-5, "fatol": 1e-9})
        if best is None or r.fun < best.fun:
            best = r
    return {"model": model, "theta": best.x, "params": dict(zip(names, best.x)), "mse": float(best.fun)}


def _take(A, idx):
    return A[0][idx], A[1][idx]


def cv_models(A, B, rate, models=("ev", "eu", "pt_noweight", "cpt"), k=10, seed=0) -> dict:
    """K-fold cross-validated mean squared error of each model, and of always predicting the training mean."""
    n = len(rate)
    fold = np.random.default_rng(seed).permutation(np.arange(n) % k)
    out = {m: np.zeros(n) for m in models}
    out["mean"] = np.zeros(n)
    for f in range(k):
        tr, te = fold != f, fold == f
        out["mean"][te] = rate[tr].mean()
        for m in models:
            fit = fit_model(m, _take(A, tr), _take(B, tr), rate[tr])
            out[m][te] = predict(m, fit["theta"], _take(A, te), _take(B, te))
    return {m: float(((p - rate) ** 2).mean()) for m, p in out.items()}


# ---------------------------------------------------------------------------------- Bayes and base rates
def bayes(base: float, hit: float, false_alarm: float) -> float:
    """P(condition | positive) from a base rate, a hit rate and a false-alarm rate."""
    return base * hit / (base * hit + (1 - base) * false_alarm)


def natural_frequencies(n: int, base: float, hit: float, false_alarm: float) -> dict:
    """The same problem as counts out of ``n`` (Gigerenzer and Hoffrage 1995)."""
    sick = round(n * base)
    tp = round(sick * hit)
    fp = round((n - sick) * false_alarm)
    return {"n": n, "sick": sick, "well": n - sick, "true_pos": tp, "false_pos": fp,
            "posterior": tp / (tp + fp)}


# --------------------------------------------------------------------------- take-the-best and regression
def environment(n_objects: int, weights, rng, noise: float = 1.0, p_cue: float = 0.5) -> tuple:
    """Objects with binary cues and a criterion = cues @ weights + noise.  Steeply falling weights make a
    non-compensatory world, equal weights a compensatory one."""
    w = np.asarray(weights, float)
    C = (rng.random((n_objects, len(w))) < p_cue).astype(float)
    y = C @ w + noise * rng.standard_normal(n_objects)
    return C, y


def _pairs(n, rng, m):
    i = rng.integers(0, n, m)
    j = rng.integers(0, n, m)
    keep = i != j
    return i[keep], j[keep]


def ttb_order(C, y) -> tuple:
    """Cue validities over all discriminating pairs of the training objects (ties in the criterion skipped):
    the proportion of pairs a cue discriminates in which it points the right way; returns order and validities."""
    i, j = np.triu_indices(len(y), 1)
    dy = np.sign(y[i] - y[j])
    val = np.full(C.shape[1], 0.5)
    for c in range(C.shape[1]):
        d = C[i, c] - C[j, c]
        m = (d != 0) & (dy != 0)
        if m.any():
            val[c] = float((np.sign(d[m]) == dy[m]).mean())
    return np.argsort(-val, kind="stable"), val


def compare_pairs(rule, C, i, j, *, order=None, val=None, beta=None) -> np.ndarray:
    """Which of each pair (i, j) has the larger criterion, +1 for i, -1 for j, by a rule: ``"ttb"`` (the first
    discriminating cue in validity order, with its direction), ``"tally"`` (count of cues each way, unit weights,
    signed by validity) or ``"regression"`` (the fitted linear score).  Undecided pairs are guessed as 0."""
    D = C[i] - C[j]
    if rule == "ttb":
        sign = np.where(val >= 0.5, 1.0, -1.0)
        out = np.zeros(len(i))
        done = np.zeros(len(i), bool)
        for c in order:
            hit = (~done) & (D[:, c] != 0)
            out[hit] = sign[c] * D[hit, c]
            done |= hit
        return out
    if rule == "tally":
        sign = np.where(val >= 0.5, 1.0, -1.0)
        return np.sign(D @ sign)
    if rule == "regression":
        return np.sign(D @ beta)
    raise ValueError(rule)


def heuristics_cv(weights, train_sizes, reps: int = 200, n_objects: int = 120, noise: float = 1.0,
                  seed: int = 0) -> dict:
    """Accuracy in new pairs (out of sample) of take-the-best, tallying and least-squares regression, each fitted to
    a training sample of objects of the given size and tested on the remaining objects (Czerlinski, Gigerenzer and
    Goldstein 1999's design, on a simulated world).  A guess counts one half."""
    rng = np.random.default_rng(seed)
    acc = {r: np.zeros((len(train_sizes), reps)) for r in ("ttb", "tally", "regression")}
    for t, m in enumerate(train_sizes):
        for r in range(reps):
            C, y = environment(n_objects, weights, rng, noise)
            perm = rng.permutation(n_objects)
            tr, te = perm[:m], perm[m:]
            order, val = ttb_order(C[tr], y[tr])
            Xd = np.column_stack([np.ones(m), C[tr]])
            beta = np.linalg.lstsq(Xd, y[tr], rcond=None)[0][1:]
            i, j = np.triu_indices(len(te), 1)
            i, j = te[i], te[j]
            truth = np.sign(y[i] - y[j])
            for rule in acc:
                g = compare_pairs(rule, C, i, j, order=order, val=val, beta=beta)
                acc[rule][t, r] = float(np.where(g == 0, 0.5, g == truth).mean())
    return {"train": np.array(train_sizes), **{k: v.mean(1) for k, v in acc.items()},
            **{k + "_se": v.std(1) / np.sqrt(reps) for k, v in acc.items()}}


# ------------------------------------------------------------------------------------------------ hot hand
def streak_props(seq: np.ndarray, k: int) -> np.ndarray:
    """For each row of a 0/1 matrix, the proportion of successes on trials that follow ``k`` successes in a row
    (NaN where no trial does): the statistic Gilovich, Vallone and Tversky (1985) compared with the overall rate."""
    seq = np.asarray(seq)
    n = seq.shape[1]
    run = np.ones((seq.shape[0], n - k), bool)
    for d in range(k):
        run &= seq[:, d:n - k + d] == 1
    nxt = seq[:, k:]
    cnt = run.sum(1)
    with np.errstate(invalid="ignore", divide="ignore"):
        return np.where(cnt > 0, (run & (nxt == 1)).sum(1) / np.maximum(cnt, 1), np.nan)


def streak_exact(n: int, k: int = 1, p: float = 0.5) -> dict:
    """The expected proportion, over all 2^n sequences weighted by their probability and among those where it is
    defined, of successes after ``k`` successes in a row (Miller and Sanjurjo 2018): below p, though each flip is
    independent."""
    seqs = np.array(list(itertools.product((0, 1), repeat=n)), dtype=np.int8)
    pr = p ** seqs.sum(1) * (1 - p) ** (n - seqs.sum(1))
    props = streak_props(seqs, k)
    m = ~np.isnan(props)
    return {"n": n, "k": k, "expected": float((pr[m] * props[m]).sum() / pr[m].sum()),
            "defined": float(pr[m].sum()), "table": (seqs, props)}


def streak_sim(n: int, k: int, p: float = 0.5, reps: int = 100_000, seed: int = 0) -> dict:
    rng = np.random.default_rng(seed)
    seqs = (rng.random((reps, n)) < p).astype(np.int8)
    props = streak_props(seqs, k)
    m = ~np.isnan(props)
    return {"n": n, "k": k, "expected": float(props[m].mean()), "defined": float(m.mean()),
            "props": props[m]}


# --------------------------------------------------------------------------------------------- over time
def discount(D, kind: str = "hyperbolic", *, k: float = 0.05, delta: float = 0.99, beta: float = 0.7):
    """The weight of a reward ``D`` periods away: exponential delta^D, hyperbolic 1 / (1 + kD) (Mazur 1987), or
    quasi-hyperbolic 1 now and beta delta^D later (Laibson 1997)."""
    D = np.asarray(D, float)
    if kind == "exponential":
        return delta ** D
    if kind == "hyperbolic":
        return 1 / (1 + k * D)
    if kind == "beta_delta":
        return np.where(D == 0, 1.0, beta * delta ** D)
    raise ValueError(kind)


def reversal_delay(small: float, large: float, gap: float, k: float) -> float:
    """For a hyperbolic discounter, the front-end delay t at which small-at-t and large-at-(t + gap) are equally
    good: nearer than t the small reward wins, further away the large one does."""
    # small / (1 + k t) = large / (1 + k (t + gap))  ->  t = (small (1 + k gap) - large) / (k (large - small))
    return (small * (1 + k * gap) - large) / (k * (large - small))


# ------------------------------------------------------------------------------------ from experience
def p_never_seen(p: float, n) -> np.ndarray:
    """The chance that ``n`` draws never show an outcome of probability ``p``."""
    return (1 - p) ** np.asarray(n, float)


def sample_choices(risky, sure: float, n_draws: int, reps: int = 20_000, seed: int = 0) -> float:
    """Decisions from experience: draw ``n_draws`` outcomes of the risky option, choose it when their mean beats the
    sure amount (a tie is a coin flip).  Returns P(choose risky)."""
    rng = np.random.default_rng(seed)
    L = np.asarray(risky, float)
    draws = rng.choice(L[:, 1], size=(reps, n_draws), p=L[:, 0])
    m = draws.mean(1)
    return float(((m > sure) + 0.5 * (m == sure)).mean())


def dbs_value(x, sample) -> np.ndarray:
    """Decision by sampling (Stewart, Chater and Brown 2006): an amount's subjective value is its rank among
    amounts remembered, the proportion of the sample it beats (ties count one half)."""
    s = np.sort(np.asarray(sample, float))
    x = np.asarray(x, float)
    lo = np.searchsorted(s, x, "left")
    hi = np.searchsorted(s, x, "right")
    return (lo + 0.5 * (hi - lo)) / len(s)
