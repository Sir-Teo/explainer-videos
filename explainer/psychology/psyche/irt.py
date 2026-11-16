"""Psyche's item response theory (Part 45): one person meeting one item.

The probability that a person of ability theta answers an item correctly is a logistic function of ability
minus the item's difficulty, scaled by its discrimination a, with a floor c for guessing (Rasch; Birnbaum; Lord).
Here are the model and its information function, marginal maximum likelihood by EM on a quadrature grid (Bock and
Aitkin), conditional maximum likelihood for the Rasch model through the elementary symmetric functions (the sum
score is sufficient, so ability drops out), ability estimates (maximum likelihood and expected a posteriori), an
adaptive test, Samejima's graded response model for rating scales, Mantel and Haenszel's test for differential item
functioning, mean-sigma linking, plausible values, Bayesian knowledge tracing (Corbett and Anderson) and Elo for
learners and items.  numpy and scipy only.
"""

from __future__ import annotations

import numpy as np
from scipy import optimize, special, stats

NODES = np.linspace(-6.0, 6.0, 81)


def prior_weights(nodes=NODES, mu: float = 0.0, sd: float = 1.0) -> np.ndarray:
    w = stats.norm.pdf(nodes, mu, sd)
    return w / w.sum()


# ----------------------------------------------------------------------------------------------------------------
# The model
# ----------------------------------------------------------------------------------------------------------------
def prob(theta, a, b, c=0.0) -> np.ndarray:
    """P(correct) for abilities ``theta`` (n,) and items (k,): an (n, k) array (3PL; c = 0 gives 2PL; a = 1 Rasch)."""
    theta = np.atleast_1d(np.asarray(theta, float))[:, None]
    a, b, c = (np.broadcast_to(np.asarray(v, float), np.shape(b)) for v in (a, b, c))
    return c + (1 - c) * special.expit(a * (theta - b))


def info(theta, a, b, c=0.0) -> np.ndarray:
    """Item information at ``theta``: a^2 (P - c)^2 Q / ((1 - c)^2 P), an (n, k) array."""
    P = prob(theta, a, b, c)
    a, c = np.asarray(a, float), np.asarray(c, float)
    return a ** 2 * (P - c) ** 2 * (1 - P) / ((1 - c) ** 2 * P)


def simulate(theta, a, b, c=0.0, seed: int = 0) -> np.ndarray:
    rng = np.random.default_rng(seed)
    P = prob(theta, a, b, c)
    return (rng.random(P.shape) < P).astype(float)


# ----------------------------------------------------------------------------------------------------------------
# Marginal maximum likelihood by EM (Bock and Aitkin 1981)
# ----------------------------------------------------------------------------------------------------------------
def _loglik_nodes(X, a, b, c, nodes) -> np.ndarray:
    """log P(response pattern | node) for each person and node: (n, q).  NaN responses are skipped."""
    P = np.clip(prob(nodes, a, b, c), 1e-12, 1 - 1e-12)  # (q, k)
    obs = ~np.isnan(X)
    Xz = np.where(obs, X, 0.0)
    return Xz @ np.log(P).T + (obs * (1 - Xz)) @ np.log(1 - P).T


def marginal_loglik(X, a, b, c=0.0, nodes=NODES, mu: float = 0.0, sd: float = 1.0) -> float:
    ll = _loglik_nodes(np.asarray(X, float), a, b, c, nodes)
    return float(special.logsumexp(ll + np.log(prior_weights(nodes, mu, sd)), axis=1).sum())


def fit_mml(X, model: str = "2pl", nodes=NODES, iters: int = 500, tol: float = 1e-7) -> dict:
    """Fit ``model`` ('rasch': one common discrimination; '2pl': one per item) to binary responses ``X`` (n, k) by
    EM, with abilities N(0, 1).  Returns a, b, the marginal log-likelihood, the number of EM cycles and the
    posterior weights."""
    X = np.asarray(X, float)
    n, k = X.shape
    obs = ~np.isnan(X)
    Xz = np.where(obs, X, 0.0)
    pw = prior_weights(nodes)
    p = np.clip(Xz.sum(0) / obs.sum(0), 0.02, 0.98)
    a = np.ones(k)
    d = special.logit(p) * 1.7  # slope-intercept form: logit = a * theta + d
    last = -np.inf
    for it in range(iters):
        b = -d / a
        ll = _loglik_nodes(X, a, b, 0.0, nodes) + np.log(pw)
        tot = special.logsumexp(ll, axis=1, keepdims=True)
        W = np.exp(ll - tot)  # (n, q) posterior weights
        cur = float(tot.sum())
        nq = obs.T.astype(float) @ W  # (k, q): expected people answering item j at node q
        rq = Xz.T @ W  # (k, q): expected correct
        a, d = _mstep(nodes, nq, rq, a, d, common=(model == "rasch"))
        if cur - last < tol:
            break
        last = cur
    b = -d / a
    return {"a": a, "b": b, "loglik": marginal_loglik(X, a, b, 0.0, nodes), "iters": it + 1, "W": W}


def _mstep(nodes, nq, rq, a, d, common: bool, steps: int = 20):
    """Newton steps on the expected complete-data log-likelihood (a weighted logistic regression on the nodes)."""
    k = len(d)
    for _ in range(steps):
        z = a[:, None] * nodes[None, :] + d[:, None]
        P = special.expit(z)
        g = rq - nq * P  # (k, q) score in z
        h = nq * P * (1 - P)  # (k, q) information in z
        if common:
            # parameters (a, d_1..d_k)
            G = np.concatenate([[np.sum(g * nodes)], g.sum(1)])
            H = np.zeros((k + 1, k + 1))
            H[0, 0] = np.sum(h * nodes ** 2)
            H[0, 1:] = H[1:, 0] = (h * nodes).sum(1)
            H[1:, 1:] = np.diag(h.sum(1))
            step = np.linalg.solve(H + 1e-9 * np.eye(k + 1), G)
            a = a + step[0]
            d = d + step[1:]
        else:
            ga, gd = (g * nodes).sum(1), g.sum(1)
            haa, had, hdd = (h * nodes ** 2).sum(1), (h * nodes).sum(1), h.sum(1)
            det = haa * hdd - had ** 2 + 1e-12
            da = (hdd * ga - had * gd) / det
            dd = (haa * gd - had * ga) / det
            a, d = a + da, d + dd
        if np.max(np.abs(step if common else np.concatenate([da, dd]))) < 1e-10:
            break
    return a, d


def fit_direct(X, model: str = "2pl", nodes=NODES) -> dict:
    """The same fit by maximizing the marginal log-likelihood directly (a check on the EM)."""
    X = np.asarray(X, float)
    k = X.shape[1]

    def unpack(v):
        if model == "rasch":
            return np.full(k, v[0]), v[1:]
        return v[:k], v[k:]

    def nll(v):
        a, d = unpack(v)
        return -marginal_loglik(X, a, -d / a, 0.0, nodes)

    v0 = np.concatenate([[1.0] if model == "rasch" else np.ones(k), np.zeros(k)])
    r = optimize.minimize(nll, v0, method="BFGS", options={"gtol": 1e-7})
    a, d = unpack(r.x)
    return {"a": a, "b": -d / a, "loglik": -r.fun, "hess_inv": r.hess_inv}


# ----------------------------------------------------------------------------------------------------------------
# The Rasch model's sufficiency: conditional maximum likelihood
# ----------------------------------------------------------------------------------------------------------------
def esf(eps) -> np.ndarray:
    """Elementary symmetric functions gamma_0..gamma_k of eps_j = exp(-b_j)."""
    g = np.zeros(len(eps) + 1)
    g[0] = 1.0
    for e in eps:
        g[1:] = g[1:] + e * g[:-1]
    return g


def fit_cml(X) -> dict:
    """Conditional ML for the Rasch model: the likelihood of each pattern given its sum score involves the items
    only, so the difficulties are estimated with ability conditioned away.  Difficulties are centred to mean 0."""
    X = np.asarray(X, float)
    k = X.shape[1]
    r = X.sum(1).astype(int)
    keep = (r > 0) & (r < k)
    X, r = X[keep], r[keep]
    s = X.sum(0)
    nr = np.bincount(r, minlength=k + 1)

    def nll(bfree):
        b = np.concatenate([bfree, [-bfree.sum()]])
        g = esf(np.exp(-b))
        return float(s @ b + nr @ np.log(g))

    res = optimize.minimize(nll, np.zeros(k - 1), method="BFGS", options={"gtol": 1e-9})
    b = np.concatenate([res.x, [-res.x.sum()]])
    return {"b": b, "n_used": int(keep.sum()), "loglik": -res.fun}


def pattern_given_score(x, b) -> float:
    """P(pattern | sum score) under the Rasch model: exp(-sum x b) / gamma_r; free of ability."""
    x = np.asarray(x, float)
    g = esf(np.exp(-np.asarray(b, float)))
    return float(np.exp(-x @ b) / g[int(x.sum())])


# ----------------------------------------------------------------------------------------------------------------
# Ability
# ----------------------------------------------------------------------------------------------------------------
def eap(X, a, b, c=0.0, nodes=NODES, mu: float = 0.0, sd: float = 1.0) -> dict:
    """Expected a posteriori ability and posterior SD for each row of ``X`` (NaN = not asked)."""
    X = np.atleast_2d(np.asarray(X, float))
    ll = _loglik_nodes(X, a, b, c, nodes) + np.log(prior_weights(nodes, mu, sd))
    W = np.exp(ll - special.logsumexp(ll, axis=1, keepdims=True))
    m = W @ nodes
    return {"theta": m, "sd": np.sqrt(np.maximum(W @ nodes ** 2 - m ** 2, 0)), "W": W}


def mle_theta(x, a, b, c=0.0, lo: float = -6.0, hi: float = 6.0) -> float:
    """The maximum-likelihood ability for one pattern (bounded to [lo, hi]; all right or all wrong hit a bound)."""
    x = np.asarray(x, float)
    ok = ~np.isnan(x)

    def nll(t):
        P = np.clip(prob(t, a, b, c)[0], 1e-12, 1 - 1e-12)
        return -np.sum(np.where(ok, x * np.log(P) + (1 - x) * np.log(1 - P), 0.0))

    return float(optimize.minimize_scalar(nll, bounds=(lo, hi), method="bounded").x)


def latent_em(X, a, b, groups, iters: int = 200, nodes=NODES) -> dict:
    """The conditioning model of a large-scale survey: with the items fixed, estimate each group's mean and SD of
    ability by EM (posterior moments averaged within groups)."""
    X = np.atleast_2d(np.asarray(X, float))
    groups = np.asarray(groups, int)
    G = groups.max() + 1
    mu, sd = np.zeros(G), np.ones(G)
    ll0 = _loglik_nodes(X, a, b, 0.0, nodes)
    for _ in range(iters):
        logp = np.log(np.stack([prior_weights(nodes, mu[g], sd[g]) for g in range(G)]))[groups]
        ll = ll0 + logp
        W = np.exp(ll - special.logsumexp(ll, axis=1, keepdims=True))
        m1, m2 = W @ nodes, W @ nodes ** 2
        new_mu = np.array([m1[groups == g].mean() for g in range(G)])
        new_sd = np.array([np.sqrt(m2[groups == g].mean() - new_mu[g] ** 2) for g in range(G)])
        if np.max(np.abs(new_mu - mu)) + np.max(np.abs(new_sd - sd)) < 1e-8:
            mu, sd = new_mu, new_sd
            break
        mu, sd = new_mu, new_sd
    return {"mu": mu, "sd": sd}


def plausible_values(X, a, b, m: int = 5, seed: int = 0, nodes=NODES, mu=0.0, sd=1.0) -> np.ndarray:
    """``m`` draws per person from the posterior of ability (on the grid, jittered within a cell).  ``mu`` and
    ``sd`` may be one per person: the prior from a conditioning model (:func:`latent_em`)."""
    rng = np.random.default_rng(seed)
    X = np.atleast_2d(np.asarray(X, float))
    mu = np.broadcast_to(np.asarray(mu, float), (X.shape[0],))
    sd = np.broadcast_to(np.asarray(sd, float), (X.shape[0],))
    ll = _loglik_nodes(X, a, b, 0.0, nodes) + np.log(np.maximum(stats.norm.pdf(nodes[None, :], mu[:, None],
                                                                                   sd[:, None]), 1e-300))
    W = np.exp(ll - special.logsumexp(ll, axis=1, keepdims=True))
    cdf = np.cumsum(W, axis=1)
    u = rng.random((W.shape[0], m))
    idx = np.array([np.searchsorted(cdf[i], u[i]) for i in range(W.shape[0])])
    h = nodes[1] - nodes[0]
    return nodes[np.minimum(idx, len(nodes) - 1)] + rng.uniform(-h / 2, h / 2, idx.shape)


# ----------------------------------------------------------------------------------------------------------------
# Adaptive testing
# ----------------------------------------------------------------------------------------------------------------
def cat(theta_true: float, a, b, c=0.0, stop_se: float = 0.3, max_items: int = 30, seed: int = 0,
        nodes=NODES) -> dict:
    """An adaptive test for one simulee: start at 0, give the unused item with the most information at the
    current EAP estimate, update, stop when the posterior SD falls below ``stop_se`` or at ``max_items``."""
    rng = np.random.default_rng(seed)
    a, b = np.asarray(a, float), np.asarray(b, float)
    c = np.broadcast_to(np.asarray(c, float), b.shape)
    x = np.full(len(b), np.nan)
    est, se = 0.0, 1.0
    order, path, ses = [], [est], [se]
    for _ in range(max_items):
        inf = info(est, a, b, c)[0]
        inf[order] = -1
        j = int(np.argmax(inf))
        order.append(j)
        x[j] = float(rng.random() < prob(theta_true, a[j], b[j], c[j])[0, 0])
        r = eap(x, a, b, c, nodes)
        est, se = float(r["theta"][0]), float(r["sd"][0])
        path.append(est)
        ses.append(se)
        if se < stop_se:
            break
    return {"items": order, "theta": est, "se": se, "path": np.array(path), "ses": np.array(ses),
            "responses": x[order]}


def fixed_form_se(theta, a, b, c=0.0) -> np.ndarray:
    """The asymptotic SE of ability from a fixed form: 1 / sqrt(test information)."""
    return 1 / np.sqrt(info(theta, a, b, c).sum(1))


# ----------------------------------------------------------------------------------------------------------------
# Rating scales: Samejima's graded response model
# ----------------------------------------------------------------------------------------------------------------
def grm_prob(theta, a: float, bs) -> np.ndarray:
    """Category probabilities (n, K) for one item with discrimination ``a`` and ordered thresholds ``bs`` (K-1)."""
    theta = np.atleast_1d(np.asarray(theta, float))
    star = special.expit(a * (theta[:, None] - np.asarray(bs, float)[None, :]))
    up = np.column_stack([np.ones(len(theta)), star])
    lo = np.column_stack([star, np.zeros(len(theta))])
    return np.clip(up - lo, 1e-12, 1)


def grm_simulate(theta, a, B, seed: int = 0) -> np.ndarray:
    """Responses 0..K-1 of people ``theta`` to items with discriminations ``a`` and thresholds rows ``B``."""
    rng = np.random.default_rng(seed)
    out = np.zeros((len(theta), len(a)), int)
    for j, (aj, bj) in enumerate(zip(a, B)):
        P = grm_prob(theta, aj, bj)
        out[:, j] = (rng.random((len(theta), 1)) > np.cumsum(P, 1)[:, :-1]).sum(1)
    return out


def fit_grm(Y, K: int, nodes=NODES, iters: int = 200, tol: float = 1e-6) -> dict:
    """Marginal ML for the graded response model by EM; ``Y`` holds categories 0..K-1."""
    Y = np.asarray(Y, int)
    n, k = Y.shape
    pw = prior_weights(nodes)
    a = np.ones(k)
    B = np.tile(np.linspace(-1.5, 1.5, K - 1), (k, 1))
    onehot = np.stack([(Y == m).astype(float) for m in range(K)], axis=2)  # (n, k, K)
    last = -np.inf
    for it in range(iters):
        logP = np.stack([np.log(grm_prob(nodes, a[j], B[j])) for j in range(k)], axis=1)  # (q, k, K)
        ll = np.einsum("ijm,qjm->iq", onehot, logP) + np.log(pw)
        tot = special.logsumexp(ll, axis=1, keepdims=True)
        W = np.exp(ll - tot)
        cur = float(tot.sum())
        R = np.einsum("iq,ijm->jqm", W, onehot)  # expected counts (k, q, K)
        for j in range(k):
            def nll(v, j=j):
                bs = np.cumsum(np.concatenate([[v[1]], np.exp(v[2:])]))
                return -float(np.sum(R[j] * np.log(grm_prob(nodes, v[0], bs))))
            v0 = np.concatenate([[a[j], B[j, 0]], np.log(np.maximum(np.diff(B[j]), 1e-3))])
            v = optimize.minimize(nll, v0, method="BFGS").x
            a[j] = v[0]
            B[j] = np.cumsum(np.concatenate([[v[1]], np.exp(v[2:])]))
        if cur - last < tol:
            break
        last = cur
    return {"a": a, "B": B, "loglik": cur, "iters": it + 1}


# ----------------------------------------------------------------------------------------------------------------
# Fairness: Mantel-Haenszel DIF
# ----------------------------------------------------------------------------------------------------------------
def mantel_haenszel(X, group, item: int) -> dict:
    """Mantel and Haenszel's test of differential item functioning for ``item``, matching on the total score.
    ``group`` is 0 (reference) or 1 (focal).  Returns the common odds ratio, the ETS delta (-2.35 log alpha), the
    continuity-corrected chi-square and its p-value, and the ETS category (A, B or C)."""
    X = np.asarray(X, float)
    g = np.asarray(group, int)
    score = X.sum(1)
    num = den = sa = sea = sva = 0.0
    for s in np.unique(score):
        m = score == s
        A = np.sum(X[m & (g == 0), item])
        Bn = np.sum(1 - X[m & (g == 0), item])
        C = np.sum(X[m & (g == 1), item])
        D = np.sum(1 - X[m & (g == 1), item])
        N = A + Bn + C + D
        if N < 2:
            continue
        num += A * D / N
        den += Bn * C / N
        nR, nF, m1, m0 = A + Bn, C + D, A + C, Bn + D
        sa += A
        sea += nR * m1 / N
        sva += nR * nF * m1 * m0 / (N ** 2 * (N - 1))
    alpha = num / den
    chi2 = (abs(sa - sea) - 0.5) ** 2 / sva
    delta = -2.35 * np.log(alpha)
    p = float(stats.chi2.sf(chi2, 1))
    cat_ = "A" if abs(delta) < 1 or p > 0.05 else ("C" if abs(delta) >= 1.5 else "B")
    return {"alpha": float(alpha), "delta": float(delta), "chi2": float(chi2), "p": p, "category": cat_}


def raw_gap(X, group, item: int) -> float:
    """The difference in proportion correct, reference minus focal, with no matching on ability."""
    X = np.asarray(X, float)
    g = np.asarray(group, int)
    return float(X[g == 0, item].mean() - X[g == 1, item].mean())


# ----------------------------------------------------------------------------------------------------------------
# Linking two forms through common items
# ----------------------------------------------------------------------------------------------------------------
def mean_sigma(b_new, b_old) -> tuple:
    """Constants (A, B) putting the new form's scale on the old: theta_old = A theta_new + B, from the anchor
    items' difficulties on both."""
    b_new, b_old = np.asarray(b_new, float), np.asarray(b_old, float)
    A = b_old.std() / b_new.std()
    return float(A), float(b_old.mean() - A * b_new.mean())


# ----------------------------------------------------------------------------------------------------------------
# Tracking learning
# ----------------------------------------------------------------------------------------------------------------
def bkt_simulate(n_students: int, n_steps: int, L0: float, T: float, G: float, S: float, seed: int = 0) -> tuple:
    """Bayesian knowledge tracing's generative model: a skill unknown or known, learned with probability T after
    each practice, answered right with probability G (guess) when unknown and 1 - S (no slip) when known."""
    rng = np.random.default_rng(seed)
    known = rng.random(n_students) < L0
    K = np.zeros((n_students, n_steps), bool)
    Y = np.zeros((n_students, n_steps))
    for t in range(n_steps):
        K[:, t] = known
        p = np.where(known, 1 - S, G)
        Y[:, t] = rng.random(n_students) < p
        known = known | (rng.random(n_students) < T)
    return Y, K


def bkt_filter(y, L0: float, T: float, G: float, S: float) -> dict:
    """P(known) before each answer, and P(correct) predicted, for one sequence (forward algorithm)."""
    L = L0
    pk, pc = [], []
    for obs in y:
        pk.append(L)
        pc.append(L * (1 - S) + (1 - L) * G)
        if obs:
            post = L * (1 - S) / (L * (1 - S) + (1 - L) * G)
        else:
            post = L * S / (L * S + (1 - L) * (1 - G))
        L = post + (1 - post) * T
    return {"known": np.array(pk), "correct": np.array(pc)}


def bkt_loglik(Y, L0, T, G, S) -> float:
    ll = 0.0
    for y in Y:
        p = np.clip(bkt_filter(y, L0, T, G, S)["correct"], 1e-9, 1 - 1e-9)
        ll += float(np.sum(y * np.log(p) + (1 - y) * np.log(1 - p)))
    return ll


def bkt_fit(Y) -> dict:
    """Fit (L0, T, G, S) by maximum likelihood, with G and S below 0.5 (the usual identifiability constraint)."""
    def nll(v):
        L0, T, G, S = special.expit(v[0]), special.expit(v[1]), 0.5 * special.expit(v[2]), 0.5 * special.expit(v[3])
        return -bkt_loglik(Y, L0, T, G, S)

    r = optimize.minimize(nll, np.zeros(4), method="Nelder-Mead", options={"maxiter": 2000, "xatol": 1e-5,
                                                                            "fatol": 1e-6})
    v = r.x
    return {"L0": float(special.expit(v[0])), "T": float(special.expit(v[1])), "G": float(0.5 * special.expit(v[2])),
            "S": float(0.5 * special.expit(v[3])), "loglik": -r.fun}


def elo_learn(person, item, y, n_people: int, n_items: int, k: float = 0.3) -> tuple:
    """Elo for learners and items: after each answer, ability moves up and difficulty down by k (y - P)."""
    th, b = np.zeros(n_people), np.zeros(n_items)
    for i, j, r in zip(person, item, y):
        p = special.expit(th[i] - b[j])
        th[i] += k * (r - p)
        b[j] -= k * (r - p)
    return th, b
