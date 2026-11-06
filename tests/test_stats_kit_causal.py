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


# ------------------------------------------------------------------ statkit.causal (II)


def test_dag_dseparation_and_backdoor():
    g = C.DAG([("U", "X"), ("U", "Y"), ("X", "Y"), ("X", "C"), ("Y", "C")])
    assert g.backdoor_ok("X", "Y", {"U"}) and not g.backdoor_ok("X", "Y", set())
    assert not g.backdoor_ok("X", "Y", {"U", "C"})  # C descends from X
    chain = C.DAG([("A", "B"), ("B", "C")])
    assert chain.d_separated({"A"}, {"C"}, {"B"}) and not chain.d_separated({"A"}, {"C"})
    coll = C.DAG([("A", "B"), ("C", "B")])
    assert coll.d_separated({"A"}, {"C"}) and not coll.d_separated({"A"}, {"C"}, {"B"})  # Berkson
    m = C.DAG([("A", "T"), ("A", "M"), ("B", "M"), ("B", "Y"), ("T", "Y")])
    assert m.backdoor_ok("T", "Y", set()) and not m.backdoor_ok("T", "Y", {"M"}) and m.backdoor_ok("T", "Y", {"M", "A"})


def _obs(n, rng):
    x = rng.normal(size=(n, 2))
    e = 1 / (1 + np.exp(-(0.8 * x[:, 0] - 0.5 * x[:, 1])))
    t = rng.random(n) < e
    y = 1 + x[:, 0] + 0.5 * x[:, 1] + t * (2 + 0.5 * x[:, 0]) + rng.normal(size=n)
    return x, t, y, e


def test_weighting_and_double_robustness():
    rng = np.random.default_rng(10)
    x, t, y, e = _obs(20000, rng)
    naive = y[t].mean() - y[~t].mean()
    assert abs(naive - 2) > 0.5  # confounded
    ps = C.propensity(x, t)
    assert abs(C.ipw(y, t, ps)["est"] - 2) < 0.1
    assert abs(C.g_computation(y, t, x) - 2) < 0.05
    # AIPW: right with a wrong outcome model (constants) and the right PS; and with the right OR and a wrong PS
    wrong0, wrong1 = np.full(len(y), y[~t].mean()), np.full(len(y), y[t].mean())
    assert abs(C.aipw(y, t, wrong0, wrong1, ps)["est"] - 2) < 0.1
    D = np.column_stack([np.ones(len(y)), x])
    b1 = np.linalg.lstsq(D[t], y[t], rcond=None)[0]
    b0 = np.linalg.lstsq(D[~t], y[~t], rcond=None)[0]
    assert abs(C.aipw(y, t, D @ b0, D @ b1, np.full(len(y), t.mean()))["est"] - 2) < 0.05
    # matching and subclassification for the ATT (= 2 + 0.5 E[x0 | T = 1])
    att = 2 + 0.5 * x[t, 0].mean()
    assert abs(C.ps_match(y, t, ps)["est"] - att) < 0.15
    assert abs(C.subclassify(y, t, ps, 10, "att")["est"] - att) < 0.2
    w = np.where(t, 1 / ps, 1 / (1 - ps))
    assert abs(C.smd(x[:, 0], t, w)) < 0.05 < abs(C.smd(x[:, 0], t))


def test_dml_and_learners():
    rng = np.random.default_rng(11)
    x, t, y, e = _obs(3000, rng)

    def ols(Xtr, ytr, Xte):
        D = np.column_stack([np.ones(len(Xtr)), Xtr])
        return np.column_stack([np.ones(len(Xte)), Xte]) @ np.linalg.lstsq(D, ytr, rcond=None)[0]

    def logit(Xtr, ttr, Xte):
        return C.logit_predict(C.logit_fit(Xtr, ttr), Xte)

    r = C.dml_ate(y, t, x, ols, logit, K=2, rng=rng)
    assert r["lo"] < 2 < r["hi"]
    plr = C.dml_plr(y, t, x, ols, rng=rng)
    assert 1.5 < plr["est"] < 2.6
    cate = C.t_learner(x, y, t, x, ols)
    assert np.corrcoef(cate, 2 + 0.5 * x[:, 0])[0, 1] > 0.95


def test_causal_forest_finds_heterogeneity():
    rng = np.random.default_rng(12)
    n = 2000
    x = rng.uniform(size=(n, 3))
    t = (rng.random(n) < 0.5).astype(float)
    tau = 1 + 2 * (x[:, 0] > 0.5)
    y = x[:, 1] + t * tau + rng.normal(scale=0.5, size=n)
    cf = C.CausalForest(x, y, t, B=60, min_leaf=20, rng=rng)
    pred = cf.predict(x)
    assert abs(pred[x[:, 0] > 0.6].mean() - 3) < 0.4 and abs(pred[x[:, 0] < 0.4].mean() - 1) < 0.4


def test_sensitivity_tools():
    assert abs(C.e_value(3.9) - 7.26) < 0.01  # VanderWeele & Ding's example
    assert abs(C.e_value(1 / 3.9) - 7.26) < 0.01
    t, dof = 4.18, 1000
    rv = C.robustness_value(t, dof)
    f = t / math.sqrt(dof)
    assert abs(rv ** 2 / (1 - rv) - f ** 2) < 1e-9  # the defining equation RV^2 / (1 - RV) = f^2
    rng = np.random.default_rng(13)
    d = rng.normal(0.5, 1, 200)
    p1, p2 = C.rosenbaum_bound(d, 1.0), C.rosenbaum_bound(d, 2.0)
    assert p1 < 1e-4 and p2 > p1
    assert abs(C.cornfield_ratio(9.0) - 9.0) < 1e-12


def test_causal_graph_instrument():
    from explainer.stats.viz import CausalGraph

    g = CausalGraph({"T": (-2, 0), "Y": (2, 0), "U": (0, 1.5)}, [("U", "T"), ("U", "Y"), ("T", "Y")])
    assert len(g.arrows) == 3 and len(g.nodes) == 3
    assert len(g.path(["T", "U", "Y"])) == 2
    assert g.open(["T", "U", "Y"]) and not g.open(["T", "U", "Y"], {"U"})
    assert len(g.condition(["U"])) == 1
