import math

import numpy as np
import pytest

from explainer.psychology.psyche import infer as I


def test_gaussian_posterior_is_a_reliability_weighted_average():
    m, s = I.posterior(0.0, 1.0, 2.0, 1.0)
    assert m == pytest.approx(1.0) and s == pytest.approx(1 / math.sqrt(2))
    m, s, w = I.combine([10.0, 20.0], [1.0, 2.0])
    assert w == pytest.approx([0.8, 0.2]) and m == pytest.approx(12.0)
    assert s == pytest.approx(1 / math.sqrt(1.25))
    assert s < 1.0


def test_two_interval_fit_recovers_the_cue_noise_and_the_combination_beats_each_cue():
    rng = np.random.default_rng(3)
    d = np.linspace(-12, 12, 13)
    fv = I.fit_cumulative(d, I.two_interval(2.0, d, 2000, rng), 2000)
    fh = I.fit_cumulative(d, I.two_interval(4.0, d, 2000, rng), 2000)
    assert fv["sd"] == pytest.approx(2.0, rel=0.08) and fh["sd"] == pytest.approx(4.0, rel=0.08)
    _, pred, w = I.combine([0, 0], [fv["sd"], fh["sd"]])
    fc = I.fit_cumulative(d, I.two_interval(None, d, 2000, rng, weights=w, sds=(2.0, 4.0)), 2000)
    assert fc["sd"] == pytest.approx(pred, rel=0.08) and fc["sd"] < fv["sd"]
    # a conflict in the standard shifts the point of equality by the weighted conflict
    fcon = I.fit_cumulative(d, I.two_interval(None, d, 4000, rng, weights=w, sds=(2.0, 4.0), conflict=6.0), 4000)
    assert fcon["pse"] == pytest.approx(3 * w[0] - 3 * w[1], abs=0.4)


def test_slow_prior_slows_low_contrast_and_rotates_edge_motion():
    s = I.speed_estimate(1.0, [1.0, 0.3, 0.1])
    assert s[0] > s[1] > s[2]
    cons = I.edge_constraints((1.0, 0.0), (20, 60))
    for n, sp in cons:
        assert n @ np.array([1.0, 0.0]) == pytest.approx(sp)
    hi = I.map_velocity(cons, 0.01)
    lo = I.map_velocity(cons, 1.0)
    assert hi == pytest.approx([1.0, 0.0], abs=0.01)
    assert np.linalg.norm(lo) < 0.6 and abs(math.atan2(lo[1], lo[0])) > math.radians(15)


def test_checker_shadow_squares_are_equal_and_retinex_separates_them():
    cs = I.checker_shadow()
    L, A, B = cs["luminance"], cs["A"], cs["B"]
    assert L[A] == pytest.approx(L[B], rel=0.03)
    assert cs["reflectance"][B] > cs["reflectance"][A]
    R = I.retinex(L)
    assert R[B] > 1.5 * R[A]


def test_disparity_and_stereogram():
    assert I.disparity_arcmin(1.0, 0.0) == 0.0
    assert I.disparity_arcmin(0.5, 0.01) > I.disparity_arcmin(1.0, 0.01) * 3.5
    left, right = I.random_dot_stereogram(80, 30, 4, seed=1)
    a, b = 25, 55
    assert np.array_equal(right[a:b, a - 4:b - 4], left[a:b, a:b])
    assert np.array_equal(right[:a], left[:a])
    assert I.perceived_size(10.0, 2.0) == pytest.approx(2 * I.perceived_size(10.0, 1.0))


def test_tiny_network_learns_paired_images_and_follows_texture_on_conflicts():
    X, y, _ = I.shape_texture_images(240, mode="paired", seed=1)
    net = I.TinyConvNet(seed=0)
    losses = net.fit(X, y, steps=150, lr=0.1)
    assert losses[-1] < losses[0]
    Xt, yt, _ = I.shape_texture_images(120, mode="paired", seed=2)
    assert (net.predict(Xt) == yt).mean() > 0.9
    assert I.texture_bias(net, 150)["texture_share"] > 0.55  # texture wins more often than shape
