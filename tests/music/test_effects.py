"""Monochord's effects rack (Part 49): filters, combs, rooms, sweeps and reverberators.

    python -m pytest -q tests/music/test_effects.py
"""

import numpy as np
import pytest
from scipy.signal import butter, freqz

from explainer.music.monochord import effects as F

SR = 48000


def test_biquads_hit_their_specs():
    f = np.array([100.0, 1000.0, 10000.0])
    lp = F.response(*F.biquad("lowpass", 1000, SR), SR, f)["db"]
    assert lp[0] == pytest.approx(0, abs=0.1) and lp[1] == pytest.approx(-3.01, abs=0.05) and lp[2] < -35
    pk = F.response(*F.biquad("peak", 1000, SR, 1.0, 9.0), SR, f)["db"]
    assert pk[1] == pytest.approx(9.0, abs=0.01) and abs(pk[0]) < 1.0
    ls = F.response(*F.biquad("lowshelf", 200, SR, 0.7071, 6.0), SR, np.array([20.0, 20000.0]))["db"]
    assert ls[0] == pytest.approx(6.0, abs=0.2) and abs(ls[1]) < 0.1


def test_bilinear_butterworth_matches_scipy():
    b, a = F.butter2_bilinear(1000, SR)
    bs, as_ = butter(2, 1000, fs=SR)
    assert np.allclose(b, bs) and np.allclose(a, as_)


def test_allpass_keeps_every_level():
    w, h = freqz([-0.6, 1.0], [1.0, -0.6], worN=512)
    assert np.allclose(np.abs(h), 1.0)


def test_comb_feedback_pitch():
    x = np.zeros(SR)
    x[0] = 1
    y = F.comb_fb(x, 218, 0.98)
    spec = np.abs(np.fft.rfft(y))
    f = np.fft.rfftfreq(len(y), 1 / SR)
    peaks = f[1:][np.argsort(spec[1:])[-1]]
    assert min(abs(peaks - k * SR / 218) for k in range(0, 120)) < 2.0
    assert SR / 218 == pytest.approx(220.18, abs=0.01)


def test_room_matches_sabine_and_eyring():
    dims = (2.6, 2.1, 2.5)
    ir = F.room_ir(dims, (0.6, 0.7, 1.5), (1.9, 1.4, 1.4), 0.15, SR, 0.8)
    rt = F.rt60(ir, SR)
    assert F.eyring(dims, 0.15) * 0.85 < rt < F.sabine(dims, 0.15) * 1.15


def test_sweep_deconvolution_recovers_an_impulse():
    s = F.ess(20, 20000, 1.0, SR)
    inv = F.ess_inverse(20, 20000, 1.0, SR)
    d = F.convolve(s, inv)
    k = int(np.argmax(np.abs(d)))
    assert k == pytest.approx(len(s) - 1, abs=2)
    side = np.r_[d[: k - 200], d[k + 200:]]
    assert np.max(np.abs(side)) < 0.05 * np.abs(d[k])


def test_reverberators_hit_their_decay():
    x = np.zeros(int(2.5 * SR))
    x[0] = 1
    assert F.rt60(F.schroeder(x, SR, 2.0), SR) == pytest.approx(2.0, rel=0.05)
    assert F.hadamard(8) @ F.hadamard(8).T == pytest.approx(np.eye(8))


def test_plate_is_stable():
    p = F.plate_ir(seconds=0.05)
    assert p["mu"] <= 0.25 and np.all(np.isfinite(p["ir"]))
