import numpy as np
import pytest
from scipy import stats

from explainer.stats import museum
from explainer.stats.kit import bootstrap as Bt


def corr(a, b):
    return np.corrcoef(a, b)[0, 1]


def test_jackknife_mean_is_exact():
    x = np.array([1.0, 4, 2, 8, 5])
    j = Bt.jackknife(x, np.mean)
    assert j["bias"] == pytest.approx(0, abs=1e-12)
    assert j["se"] == pytest.approx(x.std(ddof=1) / np.sqrt(5))


def test_bootstrap_law_and_bca_against_scipy():
    L, G = np.asarray(museum.LAW_LSAT, float), np.asarray(museum.LAW_GPA, float)
    g = np.random.Generator(np.random.PCG64(1979))
    reps = Bt.bootstrap((L, G), corr, 4000, g)
    assert 0.1 < reps.std() < 0.2
    j = Bt.jackknife((L, G), corr)
    (lo, hi), z0, a = Bt.bca_ci(reps, corr(L, G), j["loo"])
    s = stats.bootstrap((L, G), corr, paired=True, vectorized=False, n_resamples=4000, method="BCa",
                        random_state=np.random.Generator(np.random.PCG64(7)))
    assert lo == pytest.approx(s.confidence_interval.low, abs=0.05) and hi == pytest.approx(s.confidence_interval.high, abs=0.03)
    plo, phi = Bt.percentile_ci(reps)
    assert plo < corr(L, G) < phi


def test_kde_and_cv():
    x = np.random.Generator(np.random.PCG64(5)).normal(size=400)
    gx = np.linspace(-5, 5, 1001)
    f = Bt.kde(x, gx, Bt.silverman(x))
    assert np.trapezoid(f, gx) == pytest.approx(1, abs=1e-3)
    assert np.allclose(f, stats.gaussian_kde(x, bw_method=Bt.silverman(x) / x.std(ddof=1))(gx), atol=1e-6)
    g = np.random.Generator(np.random.PCG64(6))
    xx = np.linspace(0, 1, 60)
    yy = np.sin(2 * np.pi * xx) + 0.3 * g.normal(size=60)
    assert Bt.kfold_poly_cv(xx, yy, 3, 5, g) < Bt.kfold_poly_cv(xx, yy, 1, 5, g)
