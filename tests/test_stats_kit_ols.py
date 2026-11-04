import numpy as np
import pytest
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import OLSInfluence, variance_inflation_factor

from explainer.stats.kit import ols

G = np.random.Generator(np.random.PCG64(12))
N = 60
X1, X2 = G.normal(size=N), G.normal(size=N)
Y = 1 + 2 * X1 - X2 + G.normal(size=N) * (1 + np.abs(X1))
X = ols.design(X1, X2)
R = ols.fit(X, Y)
S = sm.OLS(Y, X).fit()


def test_coefficients_and_classical_se():
    assert R.coef == pytest.approx(S.params)
    assert R.se() == pytest.approx(S.bse)
    assert R.pvalue() == pytest.approx(S.pvalues)
    assert R.r2 == pytest.approx(S.rsquared)
    assert R.adj_r2 == pytest.approx(S.rsquared_adj)
    assert R.ci() == pytest.approx(S.conf_int())


@pytest.mark.parametrize("kind", ["HC0", "HC1", "HC2", "HC3"])
def test_sandwich(kind):
    assert R.se(kind) == pytest.approx(np.sqrt(np.diag(S.get_robustcov_results(kind).cov_params())))


def test_influence():
    inf = OLSInfluence(S)
    assert R.leverage == pytest.approx(inf.hat_matrix_diag)
    assert R.student == pytest.approx(inf.resid_studentized_internal)
    assert R.cooks == pytest.approx(inf.cooks_distance[0])
    assert R.leverage.sum() == pytest.approx(3)  # trace of the hat matrix = p (Part 4)


def test_f_and_bands():
    small = ols.fit(ols.design(X1), Y)
    f = R.f_test(small)
    big = S.compare_f_test(sm.OLS(Y, ols.design(X1)).fit())
    assert f["F"] == pytest.approx(big[0]) and f["p"] == pytest.approx(big[1])
    X0 = ols.design(np.array([0.0, 1.0]), np.array([0.0, 0.5]))
    pr = S.get_prediction(X0).summary_frame(alpha=0.05)
    lo, hi = R.band(X0)
    assert lo == pytest.approx(pr["mean_ci_lower"]) and hi == pytest.approx(pr["mean_ci_upper"])
    lo, hi = R.band(X0, prediction=True)
    assert lo == pytest.approx(pr["obs_ci_lower"]) and hi == pytest.approx(pr["obs_ci_upper"])


def test_vif_and_lad():
    Z = ols.design(X1, X1 + 0.1 * X2)
    assert ols.vif(Z) == pytest.approx([variance_inflation_factor(Z, j) for j in (1, 2)])
    x = np.arange(10.0)
    y = 2 * x + 1
    y[9] = 100
    b = ols.lad(x, y)
    assert b == pytest.approx([1, 2], abs=1e-4)  # the outlier does not move the LAD line
