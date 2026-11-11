"""Trading wealth keeps moving while a predictable position is held fixed."""

import numpy as np

from videos.quant.quant5.s16_representation import _marked_wealth


def test_wealth_marks_price_moves_inside_a_rebalancing_interval():
    # Hold zero on [0,1/2], then -1 on (1/2,1]; wealth is not flat there.
    wealth = _marked_wealth([0.0, 1.0, -0.5, 2.0, 1.0], 2)
    np.testing.assert_allclose(wealth, [1.0, 1.0, 1.0, -1.5, -0.5])
    np.testing.assert_allclose(wealth[::2], [1.0, 1.0, 1.0 + 2 * (-0.5) * (1.0 - (-0.5))])
