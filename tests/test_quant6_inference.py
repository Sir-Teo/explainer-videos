import numpy as np
import pytest

from videos.quant.quant6.inference import grs_test, shanken_covariance


def test_zero_premium_does_not_add_factor_variance_again():
    fm_cov = np.array([[0.03, 0.002], [0.002, 0.05]])
    np.testing.assert_allclose(shanken_covariance(fm_cov, [[0.4]], [0.0], 40), fm_cov)


def test_shanken_inflates_only_the_nonfactor_variance_component():
    periods = 80
    factor_cov = np.array([[0.4, 0.1], [0.1, 0.3]])
    premium = np.array([0.2, -0.1])
    factor_component = np.zeros((3, 3))
    factor_component[1:, 1:] = factor_cov / periods
    residual_component = np.diag([0.01, 0.02, 0.03])
    c = premium @ np.linalg.solve(factor_cov, premium)
    corrected = shanken_covariance(factor_component + residual_component, factor_cov, premium, periods)
    np.testing.assert_allclose(corrected - factor_component, (1 + c) * residual_component)


def test_single_asset_grs_is_the_squared_alpha_t_statistic():
    rng = np.random.default_rng(63)
    factors = 0.8 + rng.standard_normal(40)
    returns = 0.25 + 0.6 * factors + 0.4 * rng.standard_normal(40)
    X = np.column_stack([np.ones(40), factors])
    coefficients = np.linalg.lstsq(X, returns, rcond=None)[0]
    residuals = returns - X @ coefficients
    variance = residuals @ residuals / (len(returns) - 2)
    alpha_t2 = coefficients[0] ** 2 / (variance * np.linalg.inv(X.T @ X)[0, 0])
    for scale in (1.0, 4.0, -0.3):
        result = grs_test(returns[:, None], scale * factors)
        assert result["F"] == pytest.approx(alpha_t2, rel=1e-12)
        assert result["df"] == (1, 38)
