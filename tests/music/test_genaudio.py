"""Monochord's generative audio (Part 66): mu-law, the STFT and mel round trips, residual vector quantization, the
harmonic synthesizer, features, the Fréchet distance and the watermark.  (The networks are exercised by the part's own
tests, on what it computed.)

    python -m pytest -q tests/music/test_genaudio.py
"""

import numpy as np
import pytest

from explainer.music.monochord import genaudio as G

SR = G.SR16


def tone(f=220.0, seconds=1.0, partials=8):
    t = np.arange(int(seconds * SR)) / SR
    return sum(np.sin(2 * np.pi * f * k * t) / k for k in range(1, partials + 1)) * 0.3


def test_mulaw_round_trip_and_resolution():
    x = np.linspace(-1, 1, 10001)
    assert np.max(np.abs(G.unmulaw(G.mulaw(x)) - x)) < 0.032
    q = G.mulaw(x)
    assert q.min() == 0 and q.max() == 255
    quiet = 0.01 * np.sin(np.linspace(0, 40, 4000))
    e_mu = np.mean((G.unmulaw(G.mulaw(quiet)) - quiet) ** 2)
    e_lin = np.mean((G.linear8(quiet) - quiet) ** 2)
    assert e_mu < e_lin / 10                                              # fine steps near silence


def test_stft_and_spectral_tools():
    y = tone()
    assert np.max(np.abs(G.istft(G.stft(y), len(y))[1000:-1000] - y[1000:-1000])) < 1e-9
    gl = G.griffin_lim(np.abs(G.stft(y)), len(y), iters=40)
    assert G.spectral_distance(y, gl) < 6                                 # the magnitude, recovered closely
    M = G.mel(y, 64)
    assert M.shape[0] == 64 and G.spectral_distance(y, G.mel_to_audio(M, len(y), iters=30)) < 15


def test_rvq_stages_reduce_error():
    rng = np.random.default_rng(0)
    X = rng.standard_normal((3000, 16)) @ rng.standard_normal((16, 16))
    q = G.RVQ(3, 32, seed=0).fit(X)
    errs = [np.mean((X - q.decode(q.encode(X, s))) ** 2) for s in (1, 2, 3)]
    assert errs[0] > errs[1] > errs[2]
    assert q.encode(X, 2).shape == (2, 3000) and q.encode(X).max() < 32


def test_harmonic_synth_and_features():
    f0 = np.full(250, 220.0)
    A = np.zeros((250, 4))
    A[:, 0] = 0.5
    y = G.harmonic_synth(f0, A, hop=64)
    S = np.abs(np.fft.rfft(y[2000:14000]))
    f = np.fft.rfftfreq(12000, 1 / SR)[np.argmax(S)]
    assert abs(f - 220) < 2
    feat = G.features(tone(330.0))
    assert np.median(feat["f0"]) == pytest.approx(330.0, rel=0.01)
    assert len(feat["loud"]) == len(feat["f0"])


def test_frechet_distance():
    rng = np.random.default_rng(1)
    X = rng.standard_normal((400, 4))
    assert G.frechet(X, X) == pytest.approx(0.0, abs=1e-6)
    assert G.frechet(X, X + 3.0) == pytest.approx(36.0, rel=0.05)         # |mean shift|^2 = 4 x 9


def test_watermark_detects_and_keys_differ():
    rng = np.random.default_rng(2)
    y = tone(seconds=4.0) + 0.05 * rng.standard_normal(4 * SR)
    m = G.watermark(y, 7, strength_db=-30)
    assert G.detect(m, 7) > 6 and abs(G.detect(y, 7)) < 4 and abs(G.detect(m, 8)) < 4
    shifted = np.r_[np.zeros(20), m[:-20]]
    assert G.detect(shifted, 7, max_lag=30) > 6
