"""Regression checks for the numerical examples in The Machinery of Markets."""

import numpy as np
import pytest


def test_price_limit_example_respects_simple_return_bounds():
    from videos.quant.quant2.compute import compute_limits

    result = compute_limits()
    # The paths are stored as log returns, but the exchange's limit is on price.
    price_moves = np.expm1(result["ro"])
    assert price_moves.max() == pytest.approx(0.10, abs=1e-12)
    assert price_moves.min() == pytest.approx(-0.10, abs=1e-12)
