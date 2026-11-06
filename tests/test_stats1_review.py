"""Scientific regressions for the examples taught in Statistics, Built Part 1."""

import numpy as np
import pytest
from scipy import stats

from videos.stats.stats1.compute import correlation_cloud, inverse_quantiles, qq_demo


def test_displayed_inverse_quantiles_land_on_the_first_ecdf_crossing():
    # Interpolated quartiles are strictly between jumps for this even sample.
    x = np.array([1., 2., 10., 20., 30., 40., 50., 100.])
    for p, value in zip((.1, .25, .5, .75, .9), inverse_quantiles(x).values()):
        assert np.mean(x < value) < p <= np.mean(x <= value)
    assert inverse_quantiles(x)["q50"] != np.median(x)


def test_qq_demo_is_a_reproducible_random_subset_with_matching_plotting_positions():
    men = np.linspace(150, 200, 300)
    z, x = qq_demo(men)
    z_again, x_again = qq_demo(men)
    np.testing.assert_array_equal(x, x_again)
    np.testing.assert_array_equal(z, z_again)
    assert len(x) == len(np.unique(x)) == 15
    assert np.isin(x, men).all()
    assert np.diff(x).min() > 0
    np.testing.assert_allclose(stats.norm.cdf(z), (np.arange(15) + .5) / 15)
    # Taking every twentieth sorted observation would systematically choose the
    # minimum and omit the largest nineteen observations, rather than sample.
    assert not np.array_equal(x, men[::20])


@pytest.mark.parametrize("r", [-1., -.5, 0., .5, .9, 1.])
def test_correlation_examples_match_the_number_printed_beneath_them(r):
    x, y = correlation_cloud(r, 60, np.random.default_rng(11))
    assert np.corrcoef(x, y)[0, 1] == pytest.approx(r, abs=1e-14)
    assert x.std() == pytest.approx(1)
    assert y.std() == pytest.approx(1)


def test_qq_reference_line_keeps_its_location_and_scale_when_clipped(monkeypatch):
    from manim import VGroup, Rectangle
    from explainer.ai.viz import CornerAxes
    from videos.stats.stats1 import s09_qq

    def axes(x_range, y_range, **kwargs):
        ax = CornerAxes(x_range, y_range, x_length=3.8, y_length=3.6,
                        axis_config={"include_ticks": False, "include_tip": False})
        group = VGroup(ax)
        group.ax = ax
        return group

    # Force both ends of the reference line to cross the viewport boundary.
    monkeypatch.setattr(s09_qq, "axes", axes)
    monkeypatch.setattr(s09_qq, "label", lambda *a, **kw: Rectangle(width=.2, height=.1))
    monkeypatch.setattr(s09_qq, "load", lambda _: {
        "example_z": np.linspace(-3, 3, 300), "example_x": np.linspace(0, 100, 300),
        "example_fit": [50., 100.],
    })
    panel = s09_qq.QQ().panel("example", "example", [0, 0, 0], "example", "#FFFFFF")
    ax, ref = panel[0].ax, panel[1]
    for point in (ref.get_start(), ref.get_end()):
        x, y = ax.point_to_coords(point) + np.asarray(ax._off)
        assert y == pytest.approx(50 + 100 * x)
        assert -3 <= x <= 3

