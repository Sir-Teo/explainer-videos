"""Psyche's scaling (Part 46): turning comparisons and answers into numbers.

Thurstone's law of comparative judgment (Case V), Bradley-Terry-Luce by Hunter's MM algorithm, the multinomial and
conditional logit with Gumbel random utility, the red-bus/blue-bus failure of independence from irrelevant
alternatives, a pairwise-comparison sampler that produces the attraction (decoy) and compromise effects, a
choice-based conjoint designer and estimator, a response-style simulator (acquiescence, satisficing) and the net
promoter score.  numpy and scipy only.
"""

from __future__ import annotations

import itertools

import numpy as np
from scipy import optimize, special, stats


# ----------------------------------------------------------------------------------------------------------------
# Thurstone (1927)
# ----------------------------------------------------------------------------------------------------------------
def thurstone_probs(s, sigma: float = 1.0) -> np.ndarray:
    """Case V: each stimulus evokes a normal discriminal process with mean s_i and SD sigma, independent, so
    P(i judged above j) = Phi((s_i - s_j) / (sigma sqrt 2))."""
    s = np.asarray(s, float)
    return stats.norm.cdf((s[:, None] - s[None, :]) / (sigma * np.sqrt(2)))


def simulate_pairs(s, n_judges: int, sigma: float = 1.0, seed: int = 0) -> np.ndarray:
    """Counts W[i, j] of judges preferring i to j, every pair judged once by each judge."""
    rng = np.random.default_rng(seed)
    P = thurstone_probs(s, sigma)
    k = len(s)
    W = np.zeros((k, k))
    for i, j in itertools.combinations(range(k), 2):
        w = rng.binomial(n_judges, P[i, j])
        W[i, j], W[j, i] = w, n_judges - w
    return W


def thurstone_scale(W, clip: float = 0.98) -> np.ndarray:
    """Case V scale values from a complete matrix of counts: z_ij = Phi^-1(p_ij), s_i = mean over j of z_ij (the
    least-squares solution), centred, in units of sigma sqrt 2."""
    W = np.asarray(W, float)
    N = W + W.T
    with np.errstate(invalid="ignore", divide="ignore"):
        P = np.where(N > 0, W / N, 0.5)
    np.fill_diagonal(P, 0.5)
    Z = stats.norm.ppf(np.clip(P, 1 - clip, clip))
    s = Z.mean(1)
    return s - s.mean()


# ----------------------------------------------------------------------------------------------------------------
# Luce (1959): Bradley-Terry
# ----------------------------------------------------------------------------------------------------------------
def btl_probs(v) -> np.ndarray:
    """P(i over j) = v_i / (v_i + v_j)."""
    v = np.asarray(v, float)
    return v[:, None] / (v[:, None] + v[None, :])


def btl_fit(W, iters: int = 2000, tol: float = 1e-12) -> dict:
    """Maximum likelihood for Bradley-Terry by Hunter's (2004) MM algorithm: v_i <- w_i / sum_j n_ij/(v_i + v_j),
    each step increasing the likelihood.  Returns the strengths (geometric mean 1), their logs and the number of
    steps."""
    W = np.asarray(W, float)
    N = W + W.T
    w = W.sum(1)
    v = np.ones(len(w))
    for it in range(iters):
        denom = (N / (v[:, None] + v[None, :])).sum(1)
        new = w / denom
        new = new / np.exp(np.mean(np.log(new)))
        if np.max(np.abs(new - v)) < tol:
            v = new
            break
        v = new
    return {"v": v, "log": np.log(v), "iters": it + 1}


def iia_check(v, i: int, j: int, menus) -> list:
    """Luce's axiom: the ratio P(i)/P(j) is the same in every menu that holds both (v_i / v_j)."""
    v = np.asarray(v, float)
    out = []
    for m in menus:
        p = v[list(m)] / v[list(m)].sum()
        out.append(float(p[list(m).index(i)] / p[list(m).index(j)]))
    return out


# ----------------------------------------------------------------------------------------------------------------
# Random utility: the logit
# ----------------------------------------------------------------------------------------------------------------
def logit_probs(V) -> np.ndarray:
    V = np.asarray(V, float)
    return special.softmax(V, axis=-1)


def gumbel_choice_shares(V, n: int = 200_000, seed: int = 0) -> np.ndarray:
    """Utility V_j plus independent standard Gumbel noise; the share of draws in which each option is best."""
    rng = np.random.default_rng(seed)
    U = np.asarray(V, float)[None, :] + rng.gumbel(size=(n, len(V)))
    return np.bincount(U.argmax(1), minlength=len(V)) / n


def normal_choice_shares(V, cov, n: int = 200_000, seed: int = 0) -> np.ndarray:
    """The same with correlated normal noise (a probit), e.g. two near-identical buses."""
    rng = np.random.default_rng(seed)
    U = np.asarray(V, float)[None, :] + rng.multivariate_normal(np.zeros(len(V)), cov, n)
    return np.bincount(U.argmax(1), minlength=len(V)) / n


def fit_clogit(X, choice) -> dict:
    """McFadden's conditional logit: X is (tasks, alternatives, attributes), ``choice`` the chosen alternative per
    task.  Newton-Raphson on the concave log-likelihood; returns coefficients, SEs and the log-likelihood."""
    X = np.asarray(X, float)
    y = np.asarray(choice, int)
    T, J, K = X.shape
    b = np.zeros(K)
    for _ in range(100):
        P = special.softmax(X @ b, axis=1)  # (T, J)
        xbar = np.einsum("tj,tjk->tk", P, X)
        g = (X[np.arange(T), y] - xbar).sum(0)
        D = X - xbar[:, None, :]
        H = -np.einsum("tj,tjk,tjl->kl", P, D, D)
        step = np.linalg.solve(H, -g)
        b = b + step
        if np.max(np.abs(step)) < 1e-10:
            break
    P = special.softmax(X @ b, axis=1)
    ll = float(np.log(P[np.arange(T), y]).sum())
    return {"b": b, "se": np.sqrt(np.diag(np.linalg.inv(-H))), "loglik": ll}


# ----------------------------------------------------------------------------------------------------------------
# Context effects: a pairwise-comparison sampler
# ----------------------------------------------------------------------------------------------------------------
def pairwise_sampler(options, steps: int = 12, n: int = 20_000, noise: float = 0.0, seed: int = 0,
                     weights=None, loss: float = 2.0, power: float = 0.5) -> np.ndarray:
    """Choice shares from a sequential sampler that attends, at each step, to one random pair of options on one
    random attribute (with probabilities ``weights``): the better of the two gains d^power and the worse loses
    loss * d^power, where d is their difference (``noise`` swaps the two with that probability).  The option with
    the highest total after ``steps`` is chosen (ties at random).  A dominated decoy hands its dominator gains on
    every attribute: the attraction effect.  Losses loom larger than gains and grow less than in proportion, so a
    middle option, which never loses by much, beats the extremes: the compromise effect.
    In the spirit of the comparison-based sequential accounts of multi-alternative choice (Part 25)."""
    rng = np.random.default_rng(seed)
    O = np.asarray(options, float)
    m, k = O.shape
    w = np.full(k, 1 / k) if weights is None else np.asarray(weights, float) / np.sum(weights)
    pairs = np.array(list(itertools.combinations(range(m), 2)))
    score = np.zeros((n, m))
    for _ in range(steps):
        pr = pairs[rng.integers(0, len(pairs), n)]
        at = rng.choice(k, size=n, p=w)
        a, b = O[pr[:, 0], at], O[pr[:, 1], at]
        flip = rng.random(n) < noise
        d = np.where(flip, b - a, a - b)  # positive: the first of the pair looks better
        g = np.abs(d) ** power
        score[np.arange(n), pr[:, 0]] += np.where(d > 0, g, -loss * g)
        score[np.arange(n), pr[:, 1]] += np.where(d < 0, g, -loss * g)
    jitter = rng.random((n, m)) * 1e-3
    return np.bincount((score + jitter).argmax(1), minlength=m) / n


# ----------------------------------------------------------------------------------------------------------------
# Conjoint analysis
# ----------------------------------------------------------------------------------------------------------------
def conjoint_design(levels, n_tasks: int, n_alts: int = 3, seed: int = 0) -> np.ndarray:
    """Random choice tasks: each alternative draws one level per attribute (``levels``: list of level counts);
    returns integer codes (tasks, alts, attributes), with no two identical alternatives in a task."""
    rng = np.random.default_rng(seed)
    out = np.zeros((n_tasks, n_alts, len(levels)), int)
    for t in range(n_tasks):
        while True:
            task = np.column_stack([rng.integers(0, L, n_alts) for L in levels])
            if len({tuple(r) for r in task}) == n_alts:
                out[t] = task
                break
    return out


def dummy_code(design, levels, numeric=None) -> np.ndarray:
    """Effects of each non-reference level (level 0 is the reference) as columns; an attribute named in
    ``numeric`` (index -> values per level) enters as one linear column instead (e.g. price)."""
    numeric = numeric or {}
    cols = []
    for a, L in enumerate(levels):
        if a in numeric:
            cols.append(np.asarray(numeric[a], float)[design[..., a]][..., None])
        else:
            cols.append(np.stack([(design[..., a] == l).astype(float) for l in range(1, L)], axis=-1))
    return np.concatenate(cols, axis=-1)


def simulate_conjoint(X, beta_mean, beta_sd, n_people: int, seed: int = 0) -> tuple:
    """Each person has part-worths drawn around ``beta_mean`` (SD ``beta_sd``) and answers the tasks (one block per
    person) with Gumbel noise; returns the stacked tasks and choices."""
    rng = np.random.default_rng(seed)
    T = X.shape[0]
    Xs, ys = [], []
    for p in range(n_people):
        b = np.asarray(beta_mean) + np.asarray(beta_sd) * rng.standard_normal(len(beta_mean))
        idx = rng.choice(T, size=min(12, T), replace=False)
        U = X[idx] @ b + rng.gumbel(size=(len(idx), X.shape[1]))
        Xs.append(X[idx])
        ys.append(U.argmax(1))
    return np.concatenate(Xs), np.concatenate(ys)


# ----------------------------------------------------------------------------------------------------------------
# Answers: response styles and summary scores
# ----------------------------------------------------------------------------------------------------------------
def styled_answers(trait, style, keys, loading: float = 0.6, style_loading: float = 0.4, seed: int = 0,
                   points: int = 5) -> np.ndarray:
    """Answers (people x items, 1..points) to items keyed +1 or -1 on ``trait``, all pushed up by an acquiescent
    ``style`` (agreeing regardless of content).  Reverse-keyed items are scored back, so the style cancels in a
    balanced scale and adds up in an unbalanced one."""
    rng = np.random.default_rng(seed)
    keys = np.asarray(keys, float)
    rest = np.sqrt(1 - loading ** 2 - style_loading ** 2)
    y = (loading * keys[None, :] * np.asarray(trait)[:, None] + style_loading * np.asarray(style)[:, None]
         + rest * rng.standard_normal((len(trait), len(keys))))
    cuts = {5: (-1.5, -0.5, 0.5, 1.5), 7: (-1.75, -1.05, -0.35, 0.35, 1.05, 1.75)}[points]
    raw = 1 + np.searchsorted(np.asarray(cuts), y)
    return np.where(keys[None, :] > 0, raw, points + 1 - raw)


def straightline(answers, share: float, seed: int = 0) -> np.ndarray:
    """A share of respondents satisfice by giving the same answer to every item of a grid."""
    rng = np.random.default_rng(seed)
    A = np.array(answers, copy=True)
    who = rng.random(len(A)) < share
    A[who] = rng.integers(A.min(), A.max() + 1, who.sum())[:, None]
    return A


def nps(ratings) -> float:
    """Net promoter score: percent of 9-10 minus percent of 0-6, on a 0-10 scale."""
    r = np.asarray(ratings)
    return float(100 * (np.mean(r >= 9) - np.mean(r <= 6)))


def nps_se(ratings) -> float:
    """The standard error of the net promoter score (a difference of two proportions from one multinomial)."""
    r = np.asarray(ratings)
    p, d = np.mean(r >= 9), np.mean(r <= 6)
    return float(100 * np.sqrt((p + d - (p - d) ** 2) / len(r)))
