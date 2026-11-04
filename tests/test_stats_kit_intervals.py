import numpy as np
import pytest
from scipy import stats

from explainer.stats.kit import intervals as I


def test_clopper_pearson_and_jeffreys_match_scipy():
    for x, n in ((0, 20), (3, 20), (20, 20), (17, 50)):
        ci = stats.binomtest(x, n).proportion_ci(method="exact")
        assert I.clopper_pearson(x, n) == pytest.approx((ci.low, ci.high), abs=1e-9)
        w = stats.binomtest(x, n).proportion_ci(method="wilson")
        assert I.wilson(x, n) == pytest.approx((w.low, w.high), abs=1e-9)


def test_lr_interval_endpoints_sit_on_the_cutoff():
    lo, hi = I.likelihood_ratio(7, 20)
    ll = lambda p: 7 * np.log(p) + 13 * np.log(1 - p)  # noqa: E731
    top = ll(0.35)
    assert 2 * (top - ll(lo)) == pytest.approx(stats.chi2.ppf(0.95, 1), abs=1e-6)
    assert 2 * (top - ll(hi)) == pytest.approx(stats.chi2.ppf(0.95, 1), abs=1e-6)


def test_exact_coverage_matches_simulation():
    g = np.random.Generator(np.random.PCG64(11))
    n, p = 30, 0.12
    xs = g.binomial(n, p, 40000)
    for m in (I.wald, I.wilson, I.clopper_pearson):
        sim = np.mean([m(x, n)[0] <= p <= m(x, n)[1] for x in xs])
        assert I.binom_coverage(m, n, [p])[0] == pytest.approx(sim, abs=0.006)


def test_clopper_pearson_never_undercovers():
    ps = np.linspace(0.01, 0.99, 197)
    assert I.binom_coverage(I.clopper_pearson, 25, ps).min() >= 0.95 - 1e-9
    assert I.binom_coverage(I.wald, 25, ps).min() < 0.8


def test_pivots_cover():
    g = np.random.Generator(np.random.PCG64(12))
    hits_t = hits_v = hits_r = 0
    R = 4000
    for _ in range(R):
        x = g.normal(3, 2, 8)
        lo, hi = I.t_interval(x)
        hits_t += lo <= 3 <= hi
        lo, hi = I.var_interval(x)
        hits_v += lo <= 4 <= hi
        e = g.exponential(1 / 0.5, 6)
        lo, hi = I.rate_interval(e)
        hits_r += lo <= 0.5 <= hi
    for h in (hits_t, hits_v, hits_r):
        assert abs(h / R - 0.95) < 0.012


def test_fieller_three_shapes():
    assert I.fieller(10, 5, 1, 1)[0] == "bounded"
    assert I.fieller(1, 5, 1, 1)[0] == "complement"
    assert I.fieller(0.5, 0.5, 1, 1)[0] == "all"
    kind, lo, hi = I.fieller(10, 5, 1, 1)
    assert lo < 0.5 < hi


def test_dkw_and_order_statistics():
    x, lo, hi, eps = I.dkw_band(np.arange(100.0))
    assert eps == pytest.approx(np.sqrt(np.log(40) / 200))
    assert np.all(lo <= hi)
    assert I.order_stat_coverage(19) == pytest.approx(0.9)
    g = np.random.Generator(np.random.PCG64(3))
    s = g.exponential(size=(20000, 20))
    assert np.mean((s[:, -1] > s[:, :-1].min(1)) & (s[:, -1] < s[:, :-1].max(1))) == pytest.approx(I.order_stat_coverage(19), abs=0.01)
