import numpy as np
import pytest
import statsmodels.api as sm
import statsmodels.formula.api as smf
from scipy import stats

from explainer.stats.kit import design as D

G = np.random.Generator(np.random.PCG64(13))


def test_oneway_matches_scipy():
    groups = [G.normal(m, 1, 6) for m in (0, 0.5, 1, 1.2)]
    a = D.oneway(groups)
    s = stats.f_oneway(*groups)
    assert a["F"] == pytest.approx(s.statistic) and a["p"] == pytest.approx(s.pvalue)
    assert a["sst"] == pytest.approx(((np.concatenate(groups) - np.concatenate(groups).mean()) ** 2).sum())


def test_rcbd_matches_statsmodels():
    y = G.normal(size=(4, 5)) + np.arange(5)[None, :] + np.array([0, 1, 0, 2])[:, None]
    import pandas as pd
    df = pd.DataFrame([(t, b, y[t, b]) for t in range(4) for b in range(5)], columns=["t", "b", "y"])
    tab = sm.stats.anova_lm(smf.ols("y ~ C(t) + C(b)", df).fit())
    r = D.rcbd(y)
    assert r["F"] == pytest.approx(tab.loc["C(t)", "F"]) and r["sse"] == pytest.approx(tab.loc["Residual", "sum_sq"])


def test_latin_square_is_latin():
    sq = D.latin_square(5, np.random.Generator(np.random.PCG64(1)))
    for i in range(5):
        assert sorted(sq[i]) == list(range(5)) and sorted(sq[:, i]) == list(range(5))


def test_factorial_and_yates_agree():
    X = D.full_factorial(3)
    y = 10 + 3 * X[:, 0] - 2 * X[:, 1] + 1.5 * X[:, 0] * X[:, 1] + 0.1 * X[:, 2]
    eff = D.factorial_effects(X, y)
    assert eff["A"] == pytest.approx(6) and eff["B"] == pytest.approx(-4) and eff["AB"] == pytest.approx(3)
    yt = D.yates(y)
    assert yt[0] == pytest.approx(y.sum())
    # Yates' contrasts / 2^(k-1) are the effects, in standard order A, B, AB, C, AC, BC, ABC
    assert yt[1] / 4 == pytest.approx(eff["A"]) and yt[3] / 4 == pytest.approx(eff["AB"]) and yt[4] / 4 == pytest.approx(eff["C"])


def test_fraction_and_aliases():
    X = D.fraction(4, {"D": "ABC"})
    assert X.shape == (8, 4)
    assert np.all(X[:, 3] == X[:, 0] * X[:, 1] * X[:, 2])
    assert D.aliases("A", ["ABCD"]) == ["BCD"] and D.aliases("AB", ["ABCD"]) == ["CD"]


def test_tukey_scheffe_and_d_optimality():
    groups = [G.normal(size=8) for _ in range(4)]
    t = D.tukey_hsd(groups)
    assert t["q"] == pytest.approx(stats.studentized_range.ppf(0.95, 4, 28))
    assert D.scheffe_multiplier(4, 28) > t["q"] / np.sqrt(2)
    third = D.d_criterion([-1, 0, 1])
    assert third > D.d_criterion(np.linspace(-1, 1, 9)) and third == pytest.approx(4 / 27)


def test_cuped_and_srm_and_mde():
    x = G.normal(size=2000)
    y = 2 * x + G.normal(size=2000)
    adj, theta = D.cuped(y, x)
    assert theta == pytest.approx(2, abs=0.1) and adj.var() < 0.3 * y.var()
    assert D.srm_test(5000, 5000) == pytest.approx(1.0)
    assert D.srm_test(5000, 5300) < 0.01
    assert D.mde(32, 1.0) == pytest.approx((1.96 + 0.8416) * np.sqrt(2 / 32), rel=1e-3)


def test_field_and_bakery():
    f = D.Field()
    y = f.harvest(np.zeros((12, 12)), rng=np.random.Generator(np.random.PCG64(2)))
    assert y.shape == (12, 12) and y[:, -1].mean() > y[:, 0].mean()  # the east side is more fertile
    assert D.Bakery.truth(205, 31) == pytest.approx(85)
    assert D.Bakery.truth(225, 31) < 85
