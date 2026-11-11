"""The optional-stopping display must retain both the winning atom and the tail."""

import numpy as np
import pytest

from videos.quant.quant4.compute import _firstpassage_histogram


def test_stopped_walk_histogram_retains_all_mass_and_the_true_mean():
    values = [-500, -150, -2, 0, 1, 1]
    record = _firstpassage_histogram(values)
    assert np.sum(record["hist"]) == len(values)
    assert record["hist"][-1] == 2  # the +1 atom was formerly beyond the last edge
    assert record["hist"][-2] == 1  # zero is not merged with the winning atom
    assert record["hist"][0] == 2
    assert record["frac_hit"] == pytest.approx(2 / 6)
    assert record["below_view"] == pytest.approx(1 / 6)
    assert record["mean"] == pytest.approx(np.mean(values))  # no clipped-mean substitution
