"""The Galton board's geometry and Part 6's exact sample-size search."""

import numpy as np

from explainer.stats import GaltonBoard


def test_path_lands_in_the_bin_of_its_rightward_bounces():
    b = GaltonBoard(rows=6)
    p = b.path([1, 0, 1, 1, 0, 1])
    assert np.isclose(p.get_end()[0], b.bin_x(4))
    assert b.heights[4] == 1
    p2 = b.path([1, 1, 1, 1, 0, 0])
    assert b.heights[4] == 2 and p2.get_end()[1] > p.get_end()[1]  # the second ball stacks on the first


def test_bars_scale_to_the_bin():
    b = GaltonBoard(rows=4)
    bars = b.bars([1, 4, 6, 4, 1])
    assert len(bars) == 5
    assert np.isclose(max(r.height for r in bars), b.bin_height * 0.92)


def test_bernoulli_exact_sample_size():
    from videos.stats.stats6.compute import exact_n

    held, first = exact_n(0.6, 0.02, 1 / 1001, 5000, 8000)
    assert first <= held < 25550
