"""Check the limiting cases used in Part 3's Ohlson explanation."""

import pytest

from explainer.quant.house import valuation


@pytest.mark.parametrize("persistence", [0.0, 0.6, 1.0])
def test_equal_information_persistence_has_a_finite_present_value(persistence):
    # Equal roots make the intermediate geometric expression 0/0, but not the value.
    value = valuation.ohlson_value(50, 4, 1, persistence, persistence, 0.08)["value"]
    direct = valuation.ohlson_monte_carlo(
        50, 4, 1, persistence, persistence, 0.08, n=1, horizon=900, sd1=0, sd2=0,
    )
    assert value == pytest.approx(direct, abs=1e-9)


def test_permanent_abnormal_earnings_use_the_finite_perpetuity_multiple():
    result = valuation.ohlson_value(100, 5, 0, 1, 0.6, 0.08)
    assert result["a1"] == pytest.approx(1 / 0.08)
    assert result["value"] == pytest.approx(162.5)
