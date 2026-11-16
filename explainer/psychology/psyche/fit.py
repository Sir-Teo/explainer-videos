"""Psyche's fitting harness, in the open (Part 48): when is a model of behaviour more than a curve fit?

Learning curves that average into shapes no individual has (Estes's single-jump learners; exponential learners that
average into a power law), maximum-likelihood fitting with restarts, parameter recovery for Part 17's Q-learner, the
trade-off between learning rate and inverse temperature, model recovery and its confusion matrix (Q-learning, Q-
learning with perseveration, win-stay lose-shift, a biased coin), BIC and cross-validation, empirical-Bayes shrinkage
of individual parameters (a hierarchical model by its Laplace approximation), and a posterior predictive check that
a model reproduces a qualitative effect.  numpy and scipy only.
"""

from __future__ import annotations

import numpy as np
from scipy import optimize, special

from explainer.psychology.psyche.rl import softmax


# ----------------------------------------------------------------------------------------------------------------
# Averages that describe no one
# ----------------------------------------------------------------------------------------------------------------
def jump_learners(n: int = 200, trials: int = 40, p_jump: float = 0.12, floor: float = 0.1, ceil: float = 0.95,
                  seed: int = 0) -> dict:
    """Estes's point: each learner jumps from guessing to knowing on one trial (geometric), so each curve is a step;
    the average of the steps is a smooth, gradual curve."""
    rng = np.random.default_rng(seed)
    jump = rng.geometric(p_jump, n)
    t = np.arange(1, trials + 1)
    P = np.where(t[None, :] >= jump[:, None], ceil, floor)
    return {"t": t, "each": P, "mean": P.mean(0), "jump": jump,
            "smooth": floor + (ceil - floor) * (1 - (1 - p_jump) ** t)}


def practice_curves(n: int = 60, trials: int = 200, seed: int = 0) -> dict:
    """Heathcote, Brown and Mewhort's point: each person's response time falls exponentially, at their own rate;
    the average of the exponentials is better fitted by a power law.  Returns the per-person curves (with noise), the
    average, and the residual sums of squares of exponential and power fits to each person and to the average."""
    rng = np.random.default_rng(seed)
    t = np.arange(1, trials + 1, dtype=float)
    a = rng.normal(400, 40, n)
    b = rng.normal(600, 80, n)
    rate = np.exp(rng.normal(np.log(0.03), 2.0, n))  # rates spanning orders of magnitude
    Y = a[:, None] + b[:, None] * np.exp(-rate[:, None] * t[None, :]) + rng.normal(0, 40, (n, trials))

    def exp_f(t, A, B, c):
        return A + B * np.exp(-c * t)

    def pow_f(t, A, B, c):
        return A + B * t ** (-c)

    def rss(f, y, p0):
        try:
            p, _ = optimize.curve_fit(f, t, y, p0=p0, maxfev=20000)
            return float(np.sum((y - f(t, *p)) ** 2)), p
        except RuntimeError:
            return np.inf, None

    ind = []
    for y in Y:
        re, _ = rss(exp_f, y, [400, 600, 0.03])
        rp, _ = rss(pow_f, y, [300, 700, 0.5])
        ind.append((re, rp))
    ind = np.array(ind)
    m = Y.mean(0)
    re, pe = rss(exp_f, m, [400, 600, 0.03])
    rp, pp = rss(pow_f, m, [300, 700, 0.5])
    return {"t": t, "Y": Y, "mean": m, "rate": rate, "exp_wins_individual": float(np.mean(ind[:, 0] < ind[:, 1])),
            "avg_rss_exp": re, "avg_rss_pow": rp, "avg_exp": exp_f(t, *pe), "avg_pow": pow_f(t, *pp)}


# ----------------------------------------------------------------------------------------------------------------
# Models of a two-armed bandit, as generative programs and likelihoods
# ----------------------------------------------------------------------------------------------------------------
MODELS = ("random", "wsls", "q", "q_persev")
N_PARAMS = {"random": 1, "wsls": 1, "q": 2, "q_persev": 3}


def simulate(model: str, params, p_reward=(0.7, 0.3), trials: int = 200, reversal: int | None = 100,
             seed: int = 0) -> tuple:
    """Choices and rewards of a model on a two-armed bandit whose arms swap at ``reversal``."""
    rng = np.random.default_rng(seed)
    p = np.array(p_reward, float)
    q = np.full(2, 0.5)
    prev_a, prev_r = None, None
    C, R = np.zeros(trials, int), np.zeros(trials)
    for t in range(trials):
        if reversal is not None and t == reversal:
            p = p[::-1].copy()
        probs = _probs(model, params, q, prev_a, prev_r)
        a = int(rng.random() < probs[1])
        r = float(rng.random() < p[a])
        if model in ("q", "q_persev"):
            q[a] += params[0] * (r - q[a])
        C[t], R[t] = a, r
        prev_a, prev_r = a, r
    return C, R


def _probs(model, params, q, prev_a, prev_r):
    if model == "random":
        b = params[0]
        return np.array([1 - b, b])
    if model == "wsls":
        eps = params[0]
        if prev_a is None:
            return np.array([0.5, 0.5])
        stay = prev_a if prev_r > 0 else 1 - prev_a
        out = np.full(2, eps / 2)
        out[stay] += 1 - eps
        return out
    if model == "q":
        return softmax(q, params[1])
    persev = np.zeros(2)
    if prev_a is not None:
        persev[prev_a] = params[2]
    z = params[1] * q + persev
    z = z - z.max()
    e = np.exp(z)
    return e / e.sum()


def loglik(model: str, params, choices, rewards) -> float:
    q = np.full(2, 0.5)
    prev_a, prev_r = None, None
    ll = 0.0
    for a, r in zip(choices, rewards):
        p = _probs(model, params, q, prev_a, prev_r)
        ll += np.log(max(p[a], 1e-12))
        if model in ("q", "q_persev"):
            q[a] += params[0] * (r - q[a])
        prev_a, prev_r = a, r
    return float(ll)


BOUNDS = {"random": [(0.01, 0.99)], "wsls": [(0.01, 0.99)], "q": [(0.01, 1.0), (0.1, 20.0)],
          "q_persev": [(0.01, 1.0), (0.1, 20.0), (-3.0, 3.0)]}
STARTS = {"random": [[0.5]], "wsls": [[0.2], [0.6]], "q": [[0.1, 2.0], [0.5, 5.0], [0.9, 10.0]],
          "q_persev": [[0.1, 2.0, 0.0], [0.5, 5.0, 0.5], [0.9, 10.0, -0.5]]}


def fit(model: str, choices, rewards) -> dict:
    """Maximum likelihood from several starting points (local optima are common), bounded; with BIC."""
    best = None
    for x0 in STARTS[model]:
        r = optimize.minimize(lambda p: -loglik(model, p, choices, rewards), x0=x0, method="L-BFGS-B",
                              bounds=BOUNDS[model])
        if best is None or r.fun < best.fun:
            best = r
    n = len(choices)
    return {"params": best.x, "ll": float(-best.fun), "bic": float(2 * best.fun + N_PARAMS[model] * np.log(n)),
            "aic": float(2 * best.fun + 2 * N_PARAMS[model])}


def recovery(alphas, betas, reps: int = 4, trials: int = 200, seed: int = 0) -> dict:
    """Parameter recovery for the Q-learner: simulate at each (alpha, beta), fit, and record the estimates."""
    rows = []
    for i, a in enumerate(alphas):
        for j, b in enumerate(betas):
            for r in range(reps):
                C, R = simulate("q", (a, b), trials=trials, seed=seed + 1000 * i + 100 * j + r)
                f = fit("q", C, R)
                rows.append((a, b, f["params"][0], f["params"][1]))
    rows = np.array(rows)
    return {"true_alpha": rows[:, 0], "true_beta": rows[:, 1], "est_alpha": rows[:, 2], "est_beta": rows[:, 3],
            "r_alpha": float(np.corrcoef(rows[:, 0], rows[:, 2])[0, 1]),
            "r_beta": float(np.corrcoef(rows[:, 1], rows[:, 3])[0, 1])}


def tradeoff_surface(choices, rewards, alphas, betas) -> np.ndarray:
    """The log-likelihood over a grid of (alpha, beta): a ridge shows the two trading off."""
    return np.array([[loglik("q", (a, b), choices, rewards) for b in betas] for a in alphas])


def model_confusion(reps: int = 30, trials: int = 200, seed: int = 0) -> dict:
    """Simulate from each model with plausible parameters, fit every model, and pick the lowest BIC: the confusion
    matrix P(chosen | true) and the inversion P(true | chosen) with equal priors."""
    rng = np.random.default_rng(seed)
    gens = {"random": lambda: (rng.uniform(0.3, 0.7),), "wsls": lambda: (rng.uniform(0.05, 0.4),),
            "q": lambda: (rng.uniform(0.1, 0.8), rng.uniform(2, 10)),
            "q_persev": lambda: (rng.uniform(0.1, 0.8), rng.uniform(2, 10), rng.choice([-1.5, 1.5]))}
    M = np.zeros((4, 4))
    for i, true in enumerate(MODELS):
        for r in range(reps):
            C, R = simulate(true, gens[true](), trials=trials, seed=int(rng.integers(1 << 30)))
            bics = [fit(m, C, R)["bic"] for m in MODELS]
            M[i, int(np.argmin(bics))] += 1
    conf = M / M.sum(1, keepdims=True)
    inv = conf / conf.sum(0, keepdims=True)
    return {"models": list(MODELS), "confusion": conf, "inversion": inv, "reps": reps}


# ----------------------------------------------------------------------------------------------------------------
# Hierarchy, and prediction
# ----------------------------------------------------------------------------------------------------------------
def group_fit(n_people: int = 30, trials: int = 60, seed: int = 0) -> dict:
    """Thirty people with learning rates drawn around a population mean (on the logit scale), few trials each:
    individual ML estimates against empirical-Bayes estimates that shrink each person's logit learning rate toward
    the group's, weighting by its precision (a hierarchical model, by the Laplace approximation)."""
    rng = np.random.default_rng(seed)
    la = rng.normal(special.logit(0.3), 0.6, n_people)
    alpha = special.expit(la)
    beta = 5.0
    est, var = [], []
    for i in range(n_people):
        C, R = simulate("q", (alpha[i], beta), trials=trials, seed=seed + 31 * i)

        def nll(x, C=C, R=R):
            return -loglik("q", (special.expit(x[0]), beta), C, R)

        r = optimize.minimize_scalar(lambda x: nll([x]), bounds=(-5, 5), method="bounded")
        x = r.x
        h = 1e-3
        curv = (nll([x + h]) - 2 * nll([x]) + nll([x - h])) / h ** 2
        est.append(x)
        var.append(1 / curv if curv > 1e-6 else 25.0)
    est, var = np.array(est), np.minimum(np.array(var), 25.0)
    mu, tau2 = est.mean(), max(est.var() - var.mean(), 0.01)
    for _ in range(200):
        w = 1 / (tau2 + var)
        mu = float(np.sum(w * est) / w.sum())
        tau2 = float(max(np.sum(w ** 2 * ((est - mu) ** 2 - var)) / np.sum(w ** 2), 0.01))
    shrunk = (est / var + mu / tau2) / (1 / var + 1 / tau2)
    return {"true": la, "ml": est, "eb": shrunk, "mu": mu, "tau": float(np.sqrt(tau2)),
            "rmse_ml": float(np.sqrt(np.mean((est - la) ** 2))), "rmse_eb": float(np.sqrt(np.mean((shrunk - la) ** 2)))}


def stay_after(choices, rewards) -> dict:
    """P(stay) after a win and after a loss: a model-free summary to check models against."""
    c, r = np.asarray(choices), np.asarray(rewards)
    st = c[1:] == c[:-1]
    w = r[:-1] > 0
    return {"win": float(st[w].mean()), "loss": float(st[~w].mean())}


def posterior_predictive(true: str, true_params, fitted: str, n: int = 40, trials: int = 200, seed: int = 0) -> dict:
    """Simulate data from a 'true' model, fit another, simulate from the fit, and compare stay-after-win/loss."""
    obs, pred = [], []
    for k in range(n):
        C, R = simulate(true, true_params, trials=trials, seed=seed + k)
        obs.append(list(stay_after(C, R).values()))
        f = fit(fitted, C, R)
        C2, R2 = simulate(fitted, f["params"], trials=trials, seed=seed + 5000 + k)
        pred.append(list(stay_after(C2, R2).values()))
    return {"obs": np.array(obs).mean(0), "pred": np.array(pred).mean(0)}
