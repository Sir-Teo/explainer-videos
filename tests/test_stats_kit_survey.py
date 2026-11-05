import itertools

import numpy as np

from explainer.stats.kit import survey as S


def test_meng_identity_is_exact():
    g = np.random.default_rng(0)
    y = g.normal(size=5000)
    R = g.random(5000) < 1 / (1 + np.exp(-y))  # inclusion depends on y
    m = S.meng(y, R)
    assert np.isclose(m["error"], m["identity"], rtol=1e-12)
    assert m["rho"] > 0 and m["error"] > 0


def test_srs_se_with_fpc_matches_simulation():
    g = np.random.default_rng(1)
    pop = g.exponential(size=2000)
    means = [pop[g.choice(2000, 500, replace=False)].mean() for _ in range(4000)]
    se = S.srs_mean(pop[g.choice(2000, 500, replace=False)], N=2000)["se"]
    assert abs(np.std(means) / se - 1) < 0.1
    assert np.isclose(S.srs_mean(pop[:500], N=2000)["fpc"], 0.75)


def test_neyman_allocation_minimizes_variance():
    N_h, S_h = np.array([5000, 3000, 2000]), np.array([1.0, 4.0, 10.0])
    ney = S.neyman_allocation(N_h, S_h, 300)
    prop = S.proportional_allocation(N_h, 300)
    assert np.isclose(ney.sum(), 300)
    assert S.stratified_variance(N_h, S_h, ney) < S.stratified_variance(N_h, S_h, prop)
    for d in ([5, -5, 0], [-3, 1, 2]):
        assert S.stratified_variance(N_h, S_h, ney) <= S.stratified_variance(N_h, S_h, ney + np.array(d))


def test_horvitz_thompson_unbiased_by_enumeration():
    y = np.array([3.0, 7.0, 1.0, 9.0, 4.0])
    x = np.array([1.0, 3.0, 1.0, 4.0, 2.0])
    # Poisson sampling with pi proportional to size: average the HT total over all 2^5 samples
    pi = 0.9 * x / x.max()
    tot = 0.0
    for s in itertools.product([0, 1], repeat=5):
        s = np.array(s, bool)
        prob = np.prod(np.where(s, pi, 1 - pi))
        tot += prob * S.horvitz_thompson(y[s], pi[s])
    assert np.isclose(tot, y.sum())


def test_hansen_hurwitz_unbiased():
    y = np.array([3.0, 7.0, 1.0, 9.0])
    p = np.array([0.1, 0.3, 0.2, 0.4])
    assert np.isclose(sum(pi * yi / pi for yi, pi in zip(y, p)), y.sum())
    assert np.isclose(S.hansen_hurwitz(y[[1, 3]], p[[1, 3]])["total"], (7 / 0.3 + 9 / 0.4) / 2)


def test_design_effect_and_icc():
    g = np.random.default_rng(2)
    k, m, rho = 400, 10, 0.2
    a = g.normal(0, np.sqrt(rho), k)
    y = np.repeat(a, m) + g.normal(0, np.sqrt(1 - rho), k * m)
    cl = np.repeat(np.arange(k), m)
    assert abs(S.icc(y, cl) - rho) < 0.04
    assert np.isclose(S.design_effect(10, 0.2), 2.8)
    assert np.isclose(S.kish_neff(np.ones(50)), 50) and S.kish_neff([1, 1, 4]) < 3


def test_raking_hits_both_margins():
    g = np.random.default_rng(3)
    sex = g.choice(["m", "f"], 1000, p=[0.7, 0.3])
    age = g.choice(["y", "o"], 1000, p=[0.2, 0.8])
    w, hist = S.rake([sex, age], [{"m": 0.5, "f": 0.5}, {"y": 0.4, "o": 0.6}])
    for lab, tgt in ((sex, {"m": 0.5, "f": 0.5}), (age, {"y": 0.4, "o": 0.6})):
        for c, share in tgt.items():
            assert abs(w[lab == c].sum() / w.sum() - share) < 1e-8
    assert hist[-1] < 1e-8 and np.isclose(w.mean(), 1)


def test_poststratify_and_ratio():
    grp = np.array(["a"] * 30 + ["b"] * 70)
    w = S.poststratify(grp, {"a": 0.5, "b": 0.5})
    assert np.isclose(w[grp == "a"].sum() / w.sum(), 0.5)
    x = np.array([1.0, 2.0, 3.0, 4.0])
    r = S.ratio_mean(2 * x, x, 10.0)
    assert np.isclose(r["mean"], 20.0) and np.isclose(r["se"], 0.0)
    rg = S.regression_mean(1 + 3 * x, x, 10.0)
    assert np.isclose(rg["mean"], 31.0)
