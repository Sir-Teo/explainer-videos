import numpy as np
import pytest
from scipy import stats

from explainer.stats.kit import tests as T

G = np.random.Generator(np.random.PCG64(10))
X, Y = G.normal(0.3, 1, 12), G.normal(0, 2, 9)
DARWIN = [49, -67, 8, 16, 6, 23, 28, 41, 14, 29, 56, 24, 75, 60, -48]


@pytest.mark.parametrize("alt", T.ALTERNATIVES)
def test_t_tests_match_scipy(alt):
    r = T.t_test(X, mu0=0.1, alternative=alt)
    s = stats.ttest_1samp(X, 0.1, alternative=alt)
    assert r["t"] == pytest.approx(s.statistic) and r["p"] == pytest.approx(s.pvalue)
    r = T.t_test(X, Y, alternative=alt)
    s = stats.ttest_ind(X, Y, alternative=alt)
    assert r["t"] == pytest.approx(s.statistic) and r["p"] == pytest.approx(s.pvalue)
    r = T.welch_test(X, Y, alternative=alt)
    s = stats.ttest_ind(X, Y, equal_var=False, alternative=alt)
    assert r["t"] == pytest.approx(s.statistic) and r["p"] == pytest.approx(s.pvalue)
    r = T.t_test(X[:9], Y, paired=True, alternative=alt)
    s = stats.ttest_rel(X[:9], Y, alternative=alt)
    assert r["p"] == pytest.approx(s.pvalue)


def test_z_test():
    r = T.z_test(X, 0, 1)
    z = X.mean() * np.sqrt(len(X))
    assert r["z"] == pytest.approx(z) and r["p"] == pytest.approx(2 * stats.norm.sf(abs(z)))


def test_darwin_sign_flips_reproduce_fisher():
    r = T.sign_flip_test(DARWIN, alternative="greater")
    assert r["stat"] == 314 and r["count"] == 863 and r["total"] == 32768
    assert T.sign_flip_test(DARWIN)["p"] == pytest.approx(1726 / 32768)


def test_exact_permutation_matches_scipy():
    a, b = X[:6], Y[:5]
    r = T.permutation_test(a, b, reps=None)
    s = stats.permutation_test((a, b), lambda u, v: u.mean() - v.mean(), permutation_type="independent",
                               n_resamples=np.inf, alternative="two-sided")
    assert r["p"] == pytest.approx(s.pvalue)
    mc = T.permutation_test(a, b, reps=20_000, seed=1)
    assert abs(mc["p"] - r["p"]) < 0.02


def test_sign_test_arbuthnot():
    assert T.sign_test(82, 82)["p"] == pytest.approx(0.5 ** 82)
    assert T.sign_test(9, 10)["p"] == pytest.approx(stats.binomtest(9, 10, alternative="greater").pvalue)
    assert T.sign_test(2, 10, "two-sided")["p"] == pytest.approx(stats.binomtest(2, 10).pvalue)


def test_tea_and_fisher_exact():
    r = T.fisher_exact([[4, 0], [0, 4]])
    assert r["p"] == pytest.approx(1 / 70)
    assert [round(v * 70) for v in r["pmf"].values()] == [1, 16, 36, 16, 1]
    t = [[3, 1], [1, 3]]
    assert T.fisher_exact(t)["p"] == pytest.approx(stats.fisher_exact(t, alternative="greater").pvalue)
    t2 = [[7, 2], [3, 8]]
    assert T.fisher_exact(t2, "two-sided")["p"] == pytest.approx(stats.fisher_exact(t2).pvalue)


def test_chisq_mendel_and_independence():
    r = T.chisq_test([315, 108, 101, 32], [9 / 16, 3 / 16, 3 / 16, 1 / 16])
    s = stats.chisquare([315, 108, 101, 32], np.array([9, 3, 3, 1]) / 16 * 556)
    assert r["chi2"] == pytest.approx(s.statistic) and r["p"] == pytest.approx(s.pvalue) and r["df"] == 3
    tab = [[30, 10], [20, 40]]
    r = T.chisq_test(tab)
    s = stats.chi2_contingency(tab, correction=False)
    assert r["chi2"] == pytest.approx(s.statistic) and r["p"] == pytest.approx(s.pvalue)


def test_lrt_bonferroni_power():
    assert T.lrt(-10.0, -8.0, 1)["p"] == pytest.approx(stats.chi2.sf(4.0, 1))
    assert list(T.bonferroni([0.001, 0.02, 0.4], 0.05)) == [True, False, False]
    assert T.power_z(0, 1, 30) == pytest.approx(0.05)
    n = T.n_for_power(0.5, 1.0)
    assert n == 32 and T.power_z(0.5, 1.0, n) >= 0.8 > T.power_z(0.5, 1.0, n - 1)


def test_sign_flip_limit():
    with pytest.raises(ValueError):
        T.sign_flip_test(np.ones(21))
