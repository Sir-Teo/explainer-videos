"""Monochord's converters (Part 48): sampling, reconstruction, quantization, dither, shaping, one bit and jitter.

    python -m pytest -q tests/music/test_digital.py
"""

import numpy as np
import pytest

from explainer.music.monochord import digital as D


def test_alias_folds():
    assert D.alias(3000, 8000) == 3000 and D.alias(5000, 8000) == 3000 and D.alias(7000, 8000) == 1000
    assert D.alias(30000, 44100) == pytest.approx(14100)


def test_sinc_reconstruction_is_exact_in_the_middle():
    fs = 8.0
    n = np.arange(400)
    def s(t):
        return np.sin(2 * np.pi * 1.3 * t) + 0.5 * np.cos(2 * np.pi * 3.1 * t)
    t = np.linspace(20, 30, 200)
    assert np.max(np.abs(D.sinc_interp(s(n / fs), fs, t, taps=128) - s(t))) < 1e-3
    assert np.allclose(D.sinc_interp(s(n / fs), fs, n[50:60] / fs, taps=64), s(n[50:60] / fs))   # through every sample


def test_six_db_per_bit():
    t = np.arange(48000) / 48000
    for b in (8, 12, 16):
        x = (1 - D.lsb(b)) * np.sin(2 * np.pi * 997 * t)
        assert D.snr_db(x, D.quantize(x, b)) == pytest.approx(D.theory_snr(b), abs=0.5)


def test_dither_moments():
    none = D.error_moments(8, "none", 21, 500)
    rp = D.error_moments(8, "rpdf", 21, 4000)
    tp = D.error_moments(8, "tpdf", 21, 4000)
    assert max(none["mean"]) > 0.4                                         # the error depends on the input
    assert max(abs(m) for m in rp["mean"]) < 0.05                          # RPDF: mean independent
    assert max(rp["var"]) - min(rp["var"]) > 0.2                           # ... variance not
    assert max(tp["var"]) - min(tp["var"]) < 0.04 and np.mean(tp["var"]) == pytest.approx(0.25, abs=0.02)


def test_shaping_moves_noise_up():
    t = np.arange(48000) / 48000
    x = 0.5 * np.sin(2 * np.pi * 440 * t)
    lo = {}
    for order in (0, 2):
        f, P = D.noise_spectrum(D.shaped(x, 8, order) - x, 48000)
        lo[order] = np.mean(P[f < 2000])
    assert lo[2] < lo[0] - 20


def test_delta_sigma_gains():
    snr = {}
    for osr in (16, 64):
        fs = 48000 * osr
        t = np.arange(int(0.1 * fs)) / fs
        snr[osr] = D.band_snr_db(D.delta_sigma(0.5 * np.sin(2 * np.pi * 1000 * t), 2), 1000, fs, 20000)
    assert snr[64] - snr[16] == pytest.approx(30, abs=4)                   # 15 dB an octave, two octaves


def test_jitter_formula():
    a, b = D.jitter_sample(10000.0, 48000.0, 1e-9, 48000, np.random.default_rng(0))
    assert D.snr_db(a, b) == pytest.approx(D.jitter_snr_theory(10000.0, 1e-9), abs=0.3)
