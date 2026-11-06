"""Tests for statkit.qual, the PhD problem bank of Part 55."""

import math

import numpy as np
from scipy import stats

from explainer.stats.kit import qual as Q


def rng(seed=0):
    return np.random.default_rng(seed)


def test_borel_cantelli_and_optional_stopping():
    assert abs(Q.bc_partial_sums(2, 10 ** 5)[-1] - (math.pi ** 2 / 6 - 1)) < 1e-4
    assert Q.bc_partial_sums(1, 10 ** 5)[-1] > 10  # the harmonic series diverges
    x = rng(1).exponential(size=200000)
    assert len(Q.exceedances(x, 1.5)) < 5 < len(Q.exceedances(x, 0.9))
    assert abs(Q.running_max_ratio(x)[-1] - 1) < 0.15
    fp = Q.first_passage(400)
    assert abs(fp["hit"][3] - 0.625) < 1e-12 and abs(Q.first_passage_pmf(2) - 0.125) < 1e-12
    assert np.allclose(fp["tail_mean"], -fp["hit"])  # E S_{T ^ m} = 0
    # P(T > 2k - 1) = C(2k, k) / 4^k
    k = 50
    assert abs((1 - fp["hit"][2 * k - 1]) - math.comb(2 * k, k) / 4 ** k) < 1e-10
    assert Q.ruin(3, 7) == {"p_b": 0.3, "ET": 21}


def test_umvue_blyth_and_conditional_test():
    u = Q.poisson_umvue(10, 2.0)
    assert u["crlb"] < u["var_umvue"] < u["mle_mse"]
    # Monte Carlo check of the UMVUE's mean and variance
    T = rng(2).poisson(20.0, 400000)
    est = (0.9) ** T
    assert abs(est.mean() - math.exp(-2)) < 1e-3 and abs(est.var() / u["var_umvue"] - 1) < 0.03
    b1, b2 = Q.blyth_ratio([10, 1000], 1), Q.blyth_ratio([10, 1000], 2)
    assert b1[1] < 0.01 and b2[1] > 12
    assert abs(Q.poisson_conditional_size(5.0, randomized=True) - 0.05) < 1e-9
    assert Q.poisson_conditional_size(5.0) < 0.05
    assert abs(Q.poisson_conditional_test(12, 4)["p"] - 2 * stats.binom.sf(11, 16, 0.5)) < 1e-12


def test_local_power_brackets_median():
    p = Q.logistic_local_powers(3.0)
    s = Q.logistic_local_power_sim(3.0, 400, rng(3), reps=4000)
    for k in ("score", "t", "sign"):
        assert abs(s[k] - p[k]) < 0.04
    assert p["sign"] < p["t"] < p["score"]
    br = Q.halfline_brackets(0.1)
    assert len(br) == 101 and abs(np.diff(br).max() - 0.01) < 1e-12
    assert 1.25 < Q.bracketing_integral(lambda e: np.log(np.ceil(1 / e ** 2))) < 1.4
    x = rng(4).standard_normal(20000)
    assert abs(np.var(Q.median_if(x, 0.0, stats.norm.pdf(0))) - math.pi / 2) < 0.05
    cov = np.mean([(lambda w: w["lo"] <= 0 <= w["hi"])(Q.median_wald(rng(5 + i).standard_normal(200))) for i in range(400)])
    assert 0.9 < cov < 0.99


def test_fano_bernstein_lasso_contraction():
    f = Q.sparse_fano(1000, 10, 100)
    assert 0 < f["lower"] < f["rate"]
    assert Q.sparse_fano(10 ** 5, 10, 100)["lower"] > f["lower"]  # grows with log d
    b = Q.bounded_covariance_error(400, 50, rng(6), reps=100)
    assert b["mean"] < b["mean_bound"] and b["coverage"] == 1.0
    o = Q.lasso_oracle(200, 400, 5, rng(7), reps=10)
    assert o["pred"] < o["pred_bound"] and o["l1"] < o["l1_bound"] and o["event"] >= 0.8
    a = [Q.sequence_contraction(n, 1.0, 1.0) for n in (10 ** 3, 10 ** 5)]
    ratio = [x["total"] / x["rate2"] for x in a]
    assert abs(ratio[0] / ratio[1] - 1) < 0.15  # the rate n^(-2/3) is exact up to a constant
