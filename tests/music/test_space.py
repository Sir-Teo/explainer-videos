"""Monochord's spaces (Part 55): modes against Weyl, diffusers against Gauss's sum, image sources against their
count, the head's cues, panning laws, Ambisonic decoding and the binaural renderer.

    python -m pytest -q tests/music/test_space.py
"""

import math

import numpy as np
import pytest

from explainer.music.monochord import space as SP


def test_room_modes():
    m = SP.room_modes((5.0, 4.0, 2.7), 120.0)
    assert m[0][0] == pytest.approx(34.3) and m[0][1] == (1, 0, 0) and m[0][2] == "axial"
    assert all(a[0] <= b[0] for a, b in zip(m, m[1:]))
    big = SP.room_modes((7.0, 5.0, 3.0), 400.0)
    assert len(big) == pytest.approx(float(SP.weyl_count((7.0, 5.0, 3.0), 400.0)), rel=0.05)


def test_schroeder_and_sabine():
    assert SP.schroeder_frequency(2.0, 20000.0) == pytest.approx(20.0)
    T = SP.sabine_bands([(100.0, [0.1, 0.2]), (50.0, [0.0, 0.4])], 300.0)
    assert T == pytest.approx([0.161 * 300 / 10.0, 0.161 * 300 / 40.0])


def test_quadratic_residue_diffuser():
    N, f0 = 7, 500.0
    d = SP.qrd_depths(N, f0)
    assert [round(x / (SP.C / f0 / (2 * N))) for x in d] == [0, 1, 4, 2, 2, 4, 1]
    for N in (5, 7, 11, 13):
        for k in range(N):
            s = sum(np.exp(2j * np.pi * (n * n + k * n) / N) for n in range(N))
            assert abs(s) == pytest.approx(math.sqrt(N))
    ang = np.linspace(-90, 90, 181)
    q = 20 * np.log10(SP.scattering(SP.qrd_depths(7, 500.0), 0.06, 1000.0, ang) + 1e-9)
    f = 20 * np.log10(SP.scattering(np.zeros(7), 0.06, 1000.0, ang) + 1e-9)
    assert SP.diffusion_coefficient(q[::5]) > 3 * SP.diffusion_coefficient(f[::5])
    assert SP.diffusion_coefficient(np.zeros(10)) == pytest.approx(1.0)


def test_image_sources():
    for k in range(1, 6):
        assert len(SP.image_sources((20.0, 15.0, 10.0), (5, 5, 2), (12, 9, 1.5), k)) == (4 * k ** 3 + 6 * k ** 2 + 8 * k + 3) // 3
    im = SP.image_sources((10.0, 8.0, 4.0), (2, 2, 1), (7, 5, 2), 1)
    assert im[0][0] == pytest.approx(math.dist((2, 2, 1), (7, 5, 2)) / SP.C) and im[0][3] == 0
    lf_narrow = SP.lateral_fraction(SP.image_sources((40.0, 14.0, 16.0), (6, 8, 1.6), (26, 5.5, 1.2), 3, beta=0.85))
    lf_wide = SP.lateral_fraction(SP.image_sources((40.0, 40.0, 16.0), (6, 21, 1.6), (26, 18.5, 1.2), 3, beta=0.85))
    assert lf_narrow > lf_wide


def test_head():
    assert float(SP.woodworth_itd(math.pi / 2)) * 1e6 == pytest.approx(SP.HEAD_A / SP.C * (math.pi / 2 + 1) * 1e6)
    assert float(SP.woodworth_itd(math.radians(30))) == pytest.approx(float(SP.woodworth_itd(math.radians(150))))
    f = np.array([100.0, 8000.0])
    near, far = np.abs(SP.head_shadow(f, 0.0)), np.abs(SP.head_shadow(f, math.pi))
    assert near[0] == pytest.approx(1.0, abs=0.02) and far[0] == pytest.approx(1.0, abs=0.02)
    assert 20 * math.log10(near[1] / far[1]) > 15
    hl, hr = SP.ear_filters(math.radians(30))
    hl2, hr2 = SP.ear_filters(math.radians(150))
    assert np.allclose(hl, hl2) and np.allclose(hr, hr2)          # the cone of confusion, for a sphere
    assert np.argmax(np.abs(hr)) < np.argmax(np.abs(hl))          # a source on the right reaches the right ear first


def test_binaural_renderer_is_smooth():
    sr = SP.SR
    x = np.sin(2 * np.pi * 440 * np.arange(sr) / sr)
    y = SP.binaural(x, lambda t: 2 * np.pi * t)
    assert y.shape == (sr, 2)
    d = np.abs(np.diff(y[2000:-2000], axis=0)).max()
    assert d < 2.5 * 2 * np.pi * 440 / sr * np.abs(y).max()       # no clicks at the block joins
    still = SP.binaural(x, lambda t: math.pi / 2)
    assert np.sqrt(np.mean(still[4000:, 1] ** 2)) > np.sqrt(np.mean(still[4000:, 0] ** 2))


def test_panning():
    p = np.linspace(-1, 1, 101)
    gL, gR = SP.pan_gains(p, "power")
    assert np.allclose(gL ** 2 + gR ** 2, 1.0)
    lL, lR = SP.pan_gains(np.array([0.0]), "linear")
    assert 10 * math.log10(lL[0] ** 2 + lR[0] ** 2) == pytest.approx(-3.0103, abs=1e-4)
    assert SP.tangent_law(1.0, 0.0) == pytest.approx(30.0) and SP.tangent_law(1.0, 1.0) == pytest.approx(0.0)
    assert abs(float(SP.tangent_law(*SP.pan_gains(np.array([0.5])))[0])) == pytest.approx(13.45, abs=0.01)


def test_ambisonics():
    spk = np.radians(np.arange(0, 360, 45))
    for th in np.radians([0, 20, 77, 200]):
        g = SP.ambisonic_decode(th, spk, "basic")
        v = SP.gerzon_vectors(g, spk)
        assert v["|rV|"] == pytest.approx(1.0) and v["|rE|"] == pytest.approx(2 / 3)
        assert (v["dir_rE"] - math.degrees(th) + 180) % 360 - 180 == pytest.approx(0.0, abs=1e-6)
        m = SP.gerzon_vectors(SP.ambisonic_decode(th, spk, "maxre"), spk)
        assert m["|rE|"] == pytest.approx(math.cos(math.pi / 4))
