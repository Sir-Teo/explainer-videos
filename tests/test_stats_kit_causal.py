import math

import numpy as np

from explainer.stats.kit import causal as C


def test_neyman_exact_variance_by_enumeration():
    rng = np.random.default_rng(0)
    n, n1 = 10, 5
    y0 = rng.normal(0, 1, n)
    y1 = y0 + rng.normal(1, 0.8, n)  # heterogeneous effects
    ests, cons = [], []
    for z in C.complete_assignments(n, n1):
        y = np.where(z, y1, y0)
        r = C.diff_means(y, z)
        ests.append(r["est"])
        cons.append(r["se"] ** 2)
    v = C.neyman_true_var(y0, y1, n1)
    assert abs(np.mean(ests) - v["ate"]) < 1e-12  # unbiased over the randomization
    assert abs(np.var(ests) - v["true"]) < 1e-12  # Neyman's exact variance
    assert abs(np.mean(cons) - v["conservative"]) < 1e-12 and v["conservative"] >= v["true"]


def test_fisher_exact_and_ci():
    y = np.array([3.0, 5, 6, 8, 1, 2, 2, 4])
    z = np.array([1, 1, 1, 1, 0, 0, 0, 0], bool)
    r = C.fisher_test(y, z)
    assert len(r["dist"]) == math.comb(8, 4)
    assert 0 < r["p"] < 0.2
    ci = C.fisher_ci(y, z, np.linspace(-4, 9, 27), reps=400, rng=np.random.default_rng(1))
    assert ci["lo"] < 3.25 < ci["hi"]


def test_lin_and_ancova_and_blocks():
    rng = np.random.default_rng(2)
    n = 400
    x = rng.normal(size=n)
    z = rng.random(n) < 0.5
    y = 1 + 2 * x + z * (1 + x) + rng.normal(size=n)
    a, l, d = C.ancova(y, z, x), C.lin(y, z, x), C.diff_means(y, z)
    assert abs(l["est"] - 1) < 0.3 and l["se"] < d["se"]
    assert abs(a["est"] - 1) < 0.4
    b = C.blocked(y, z, x > 0)
    assert abs(b["est"] - 1) < 0.5


def test_iv_cluster_two_stage():
    rng = np.random.default_rng(3)
    n = 20000
    z = rng.random(n) < 0.5
    t = rng.choice(3, n, p=[0.6, 0.3, 0.1])  # complier, never, always
    d = np.where(t == 0, z, t == 2)
    y = rng.normal(size=n) + 2.0 * d + 0.5 * (t == 1)
    r = C.iv_late(y, z, d)
    assert abs(r["itt_d"] - 0.6) < 0.03 and abs(r["est"] - 2.0) < 0.15
    # clusters
    cl = np.repeat(np.arange(100), 50)
    zc = rng.random(100) < 0.5
    u = rng.normal(0, 1, 100)[cl]
    yy = u + rng.normal(size=len(cl)) + 0.3 * zc[cl]
    c = C.cluster_diff(yy, zc, cl)
    assert c["cluster"]["se"] > 3 * c["naive"]["se"]
    assert abs(C.design_effect(50, 0.5) - 25.5) < 1e-12
    # two-stage: protection positive
    g = np.repeat(np.arange(40), 50)
    psi = np.repeat([0, 1], 20)
    share = np.where(psi == 0, 0.3, 0.7)
    v = rng.random(len(g)) < share[g]
    p = 0.2 * (1 - 0.6 * v) * (1 - 0.6 * share[g])
    inf = rng.random(len(g)) < p
    h = C.two_stage(inf, v, g, psi)
    assert h["direct0"] > 0 and h["indirect"] > 0 and h["total"] > h["direct0"]


def test_group_sequential_boundaries():
    assert abs(C.pocock(5) - 2.413) < 0.01  # Pocock (1977), K = 5, two-sided 0.05
    obf = C.obrien_fleming(5)
    assert abs(obf[-1] - 2.040) < 0.01 and abs(obf[0] - 4.562) < 0.02
    ld = C.spending_bounds([0.2, 0.4, 0.6, 0.8, 1.0])
    assert np.allclose(ld, [4.877, 3.357, 2.680, 2.290, 2.031], atol=0.01)  # Lan-DeMets OBF-type
    assert abs(C.crossing_probs([1.96]).sum() - 0.05) < 1e-3
    assert abs(C.peeking_sim(5, 20000, np.random.default_rng(0)) - 0.142) < 0.01  # Armitage et al.: 14.2%


def test_prentice_and_transport():
    rng = np.random.default_rng(4)
    n = 3000
    z = rng.random(n) < 0.5
    s = 1.0 * z + rng.normal(size=n)
    y = 2.0 * s + rng.normal(size=n)  # a perfect surrogate
    pr = C.prentice(y, s, z)
    assert pr["z_on_s"][1] > 5 and pr["s_on_y"][1] > 5 and abs(pr["z_given_s"][1]) < 3
    # transport: effect grows with x; the trial over-samples low x
    xt = rng.normal(-0.5, 1, 4000)
    xg = rng.normal(0.5, 1, 4000)
    zt = rng.random(4000) < 0.5
    yt = zt * (1 + xt) + rng.normal(size=4000)
    r = C.transport(yt, zt, xt[:, None], xg[:, None])
    assert abs(r["est"] - 1.5) < 0.2


def test_science_table():
    from explainer.stats.viz import ScienceTable

    t = ScienceTable([150, 160, 145], [140, 158, 139], extra=[(r"age", [61, 70, 55])])
    assert len(t.rows) == 4 and t.names[-3:] == ["y0", "y1", "tau"]
    z = np.array([1, 0, 1], bool)
    assert len(t.mask(z)) == 6 and len(t.observed(z)) == 3
    assert len(t.column("tau")) == 4
