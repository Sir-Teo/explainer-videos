"""statkit.frontier (Part 62): the front door, sensitivity bounds, proximal 2SLS, exposure mappings, policy learning,
Q-learning, discovery and the surrogate index."""

import math

import numpy as np

from explainer.stats.kit import causal as C
from explainer.stats.kit import frontier as F


def test_front_door_and_criterion():
    rng = np.random.default_rng(1)
    n = 40000
    U = rng.random(n) < 0.5
    A = rng.random(n) < np.where(U, 0.8, 0.2)
    M = rng.random(n) < np.where(A, 0.75, 0.25)
    Y = 2.0 * M + 3.0 * U + rng.standard_normal(n)
    assert abs(F.front_door(Y, A, M)["ate"] - 1.0) < 0.06
    assert Y[A].mean() - Y[~A].mean() > 2.5
    g = C.DAG([("U", "A"), ("U", "Y"), ("A", "M"), ("M", "Y")])
    assert F.frontdoor_ok(g, "A", "Y", ["M"]) and not g.backdoor_ok("A", "Y", [])
    assert not F.frontdoor_ok(C.DAG([("U", "A"), ("U", "Y"), ("A", "M"), ("M", "Y"), ("U", "M")]), "A", "Y", ["M"])
    assert not F.frontdoor_ok(C.DAG([("U", "A"), ("U", "Y"), ("A", "M"), ("M", "Y"), ("A", "Y")]), "A", "Y", ["M"])


def test_msm_bounds():
    rng = np.random.default_rng(2)
    n = 3000
    x = rng.standard_normal(n)
    ps = 1 / (1 + np.exp(-x))
    t = (rng.random(n) < ps).astype(int)
    y = x + t + rng.standard_normal(n)
    b1 = F.msm_bounds(y, t, ps, 1.0)
    # Lambda = 1 is the Hajek point estimate
    w1, w0 = 1 / ps[t == 1], 1 / (1 - ps[t == 0])
    hj = np.sum(w1 * y[t == 1]) / w1.sum() - np.sum(w0 * y[t == 0]) / w0.sum()
    assert abs(b1["ate_lo"] - hj) < 1e-9 and abs(b1["ate_hi"] - hj) < 1e-9
    # the bounds widen with Lambda and agree with brute force over the extreme weight vectors
    widths = [F.msm_bounds(y, t, ps, lam)["ate_hi"] - F.msm_bounds(y, t, ps, lam)["ate_lo"] for lam in (1, 1.5, 2, 3)]
    assert all(a < b for a, b in zip(widths, widths[1:]))
    yy = rng.standard_normal(8)
    lo, hi = np.full(8, 1.0), np.full(8, 3.0)
    best = max(np.sum(np.where(m, hi, lo) * yy) / np.sum(np.where(m, hi, lo)) for m in (np.array([(k >> i) & 1 for i in range(8)], bool) for k in range(256)))
    assert abs(F._hajek_extreme(yy, lo, hi, True) - best) < 1e-12


def test_proximal_beats_naive_adjustment():
    rng = np.random.default_rng(3)
    n = 20000
    U = rng.standard_normal(n)
    Z, W = U + rng.standard_normal(n), U + rng.standard_normal(n)
    A = (0.8 * U + rng.standard_normal(n) > 0).astype(float)
    Y = 1.0 * A + 2 * U + rng.standard_normal(n)
    p = F.proximal_2sls(Y, A, Z, W)
    o = F.ols_adjusted(Y, A, np.column_stack([Z, W]))
    assert abs(p["effect"] - 1) < 3 * p["se"] and abs(o["effect"] - 1) > 10 * o["se"]
    # 2SLS with X as its own instrument is OLS
    X = np.column_stack([np.ones(n), A, Z])
    assert np.allclose(F.tsls(Y, X, X)["b"], np.linalg.lstsq(X, Y, rcond=None)[0])


def test_interference_exposures():
    rng = np.random.default_rng(4)
    n = 300
    pos = rng.random((n, 2))
    D = np.sqrt(((pos[:, None] - pos[None]) ** 2).sum(-1))
    adj = ((D < 0.08) & (D > 0)).astype(int)
    z = (rng.random(n) < 0.3).astype(int)
    e = F.exposures(z, adj)
    assert set(np.unique(e)) <= {0, 1, 2, 3} and np.all((e >= 2) == (z == 1))
    pi = F.exposure_probs(adj, 0.3, rng, 3000)
    assert np.allclose(pi.sum(1), 1, atol=1e-3)
    # an isolated unit's exposure probabilities are (0.7, 0, 0.3, 0)
    iso = np.flatnonzero(adj.sum(1) == 0)
    if len(iso):
        assert abs(pi[iso[0], 0] - 0.7) < 0.03 and pi[iso[0], 1] < 0.01
    ests = []
    y0 = rng.standard_normal(n)
    for _ in range(200):
        z = (rng.random(n) < 0.3).astype(int)
        y = y0 + 2 * z + 1.0 * ((adj @ z) > 0)
        ests.append(F.exposure_hajek(y, z, adj, pi))
    assert abs(np.mean([h["direct"] for h in ests]) - 2) < 0.1 and abs(np.mean([h["spill"] for h in ests]) - 1) < 0.1


def test_policy_and_q_learning():
    rng = np.random.default_rng(5)
    x = rng.uniform(-1, 1, 4000)
    gamma = (x - 0.3) + 0.1 * rng.standard_normal(4000)
    rule = F.ewm_threshold(x, gamma)
    assert rule["s"] == 1 and abs(rule["c"] - 0.3) < 0.05
    assert abs(F.policy_value(gamma, F.apply_rule(x, rule)) - rule["value"]) < 1e-12
    # the AIPW scores average to the ATE
    t = (rng.random(4000) < 0.5).astype(float)
    y = x + t * 0.5 + rng.standard_normal(4000)
    G = F.aipw_scores(y, t, x, x + 0.5, 0.5)
    assert abs(G.mean() - 0.5) < 0.1
    # Q-learning recovers a known stage-2 rule: treat iff X2 > 0.2
    n = 20000
    X1 = rng.standard_normal(n)
    A1 = (rng.random(n) < 0.5).astype(float)
    X2 = 0.5 * X1 + rng.standard_normal(n)
    A2 = (rng.random(n) < 0.5).astype(float)
    Y = X2 + A2 * (X2 - 0.2) + rng.standard_normal(n)
    q = F.q_learning(X1, A1, X2, A2, Y)
    assert abs(-q["b2"][2] / q["b2"][3] - 0.2) < 0.05


def test_discovery_and_surrogates():
    rng = np.random.default_rng(6)
    # a chain X0 -> X1 -> X2: PC removes 0 - 2 given 1 and keeps the chain
    n = 5000
    X0 = rng.standard_normal(n)
    X1 = X0 + rng.standard_normal(n)
    X2 = X1 + rng.standard_normal(n)
    pc = F.pc_skeleton(np.column_stack([X0, X1, X2]), 0.01, 1)
    assert pc["adj"][0, 1] and pc["adj"][1, 2] and not pc["adj"][0, 2] and pc["sep"][(0, 2)] == (1,)
    s = F.random_linear_sem(8, 0.4, rng, 3000)
    if np.any(s["B"]):
        assert F.varsortability(s["X"], s["B"]) > 0.8
        Xs = (s["X"] - s["X"].mean(0)) / s["X"].std(0)
        assert F.varsortability(Xs, s["B"]) < F.varsortability(s["X"], s["B"])
    # the surrogate index is unbiased under surrogacy
    So = rng.standard_normal((20000, 1))
    Yo = 2 * So[:, 0] + rng.standard_normal(20000)
    te = (rng.random(20000) < 0.5).astype(float)
    Se = (0.5 * te + rng.standard_normal(20000))[:, None]
    si = F.surrogate_index(So, Yo, Se, te)
    assert abs(si["effect"] - 1.0) < 4 * si["se"]
    assert math.isfinite(si["se"]) and si["se"] > 0
