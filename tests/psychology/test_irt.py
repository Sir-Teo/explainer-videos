"""Psyche's item response theory (Part 45)."""

import numpy as np


from explainer.psychology.psyche import irt


def test_information_peaks_at_difficulty():
    th = np.linspace(-4, 4, 801)
    I = irt.info(th, 1.5, 0.7)[:, 0]
    assert abs(th[np.argmax(I)] - 0.7) < 0.01
    assert abs(I.max() - 1.5 ** 2 / 4) < 1e-6


def test_em_matches_direct_and_recovers():
    rng = np.random.default_rng(3)
    th = rng.normal(size=2000)
    a, b = np.array([0.8, 1.2, 1.5, 0.7, 1.0]), np.array([-1.0, -0.3, 0.2, 0.8, 1.2])
    X = irt.simulate(th, a, b, seed=4)
    em = irt.fit_mml(X, "2pl")
    di = irt.fit_direct(X, "2pl")
    assert abs(em["loglik"] - di["loglik"]) < 1e-3
    assert np.max(np.abs(em["b"] - b)) < 0.25 and np.max(np.abs(em["a"] - a)) < 0.3


def test_rasch_sum_score_sufficient():
    b = np.array([-1.0, 0.0, 0.5, 1.5])
    pats = [np.array(p) for p in ([1, 1, 0, 0], [1, 0, 1, 0], [0, 0, 1, 1], [0, 1, 0, 1], [1, 0, 0, 1],
                                  [0, 1, 1, 0])]
    assert abs(sum(irt.pattern_given_score(p, b) for p in pats) - 1) < 1e-12
    for t in (-2.0, 0.0, 2.0):  # P(pattern | score) computed with ability agrees, at any ability
        P = irt.prob(t, 1.0, b)[0]
        lik = [np.prod(np.where(p == 1, P, 1 - P)) for p in pats]
        assert np.allclose(np.array(lik) / sum(lik), [irt.pattern_given_score(p, b) for p in pats])


def test_cml_matches_mml_differences():
    rng = np.random.default_rng(5)
    X = irt.simulate(rng.normal(size=3000), 1.0, np.array([-1.2, -0.4, 0.3, 1.0, 1.6]), seed=6)
    c = irt.fit_cml(X)["b"]
    m = irt.fit_mml(X, "rasch")
    assert np.allclose(np.diff(c), np.diff(m["b"]) * m["a"][0], atol=0.03)


def test_cat_shortens_test():
    a = np.full(200, 1.5)
    b = np.linspace(-3, 3, 200)
    r = irt.cat(1.0, a, b, stop_se=0.35, max_items=60, seed=1)
    assert r["se"] < 0.35 and len(r["items"]) < 25


def test_mantel_haenszel_no_dif_under_impact():
    rng = np.random.default_rng(7)
    g = np.repeat([0, 1], 3000)
    th = rng.normal(size=6000) - 0.8 * g  # the groups differ in ability, the items do not differ
    b = np.linspace(-1.5, 1.5, 15)
    X = irt.simulate(th, 1.0, b, seed=8)
    r = irt.mantel_haenszel(X, g, 7)
    assert abs(r["delta"]) < 0.6 and irt.raw_gap(X, g, 7) > 0.1

    bb7 = np.where(g == 1, b[7] + 0.8, b[7])
    X2 = X.copy()
    X2[:, 7] = rng.random(6000) < 1 / (1 + np.exp(-(th - bb7)))
    assert irt.mantel_haenszel(X2, g, 7)["category"] == "C"


def test_grm_probabilities_sum_to_one():
    P = irt.grm_prob(np.linspace(-3, 3, 7), 1.3, [-1.0, 0.0, 1.2])
    assert np.allclose(P.sum(1), 1)


def test_bkt_filter_and_fit():
    Y, _ = irt.bkt_simulate(400, 12, 0.2, 0.15, 0.2, 0.1, seed=9)
    f = irt.bkt_fit(Y)
    assert abs(f["T"] - 0.15) < 0.05 and abs(f["G"] - 0.2) < 0.06 and abs(f["S"] - 0.1) < 0.05
    k = irt.bkt_filter([1, 1, 1], 0.2, 0.15, 0.2, 0.1)["known"]
    assert np.all(np.diff(k) > 0)


def test_mean_sigma_recovers_transform():
    b_old = np.array([-1.0, -0.2, 0.4, 1.3])
    A, B = irt.mean_sigma((b_old - 0.5) / 1.2, b_old)
    assert abs(A - 1.2) < 1e-12 and abs(B - 0.5) < 1e-12


def test_lsat_matches_published_fit():
    from explainer.psychology import opendata

    X = opendata.lsat_1000()["X"]
    r = irt.fit_mml(X, "rasch")
    assert abs(r["loglik"] + 2466.938) < 0.01
    assert np.allclose(r["b"], [-3.615, -1.322, -0.318, -1.730, -2.780], atol=2e-3)
