"""Monochord's codecs (Part 58): entropy, a bit-exact lossless coder, the MDCT's alias cancellation, the masking
model, the perceptual coder's rate control, ABX statistics and residual vector quantization.

    python -m pytest -q tests/music/test_codec.py
"""

import math

import numpy as np
import pytest

from explainer.music.monochord import codec as K

SR = 48000


def test_entropy():
    assert K.entropy_bits([0, 1] * 500) == pytest.approx(1.0)
    assert K.entropy_bits([7] * 100) == pytest.approx(0.0)
    x = np.array([0] * 900 + [1] * 100)
    assert K.entropy_bits(x) == pytest.approx(-(0.9 * math.log2(0.9) + 0.1 * math.log2(0.1)))


def test_zigzag_and_rice():
    e = np.array([0, -1, 1, -2, 2, -3])
    assert K.zigzag(e).tolist() == [0, 1, 2, 3, 4, 5] and np.array_equal(K.unzigzag(K.zigzag(e)), e)
    assert K.rice_cost(np.array([13]), 2) == 3 + 1 + 2


def test_lossless_round_trip():
    rng = np.random.default_rng(0)
    t = np.arange(SR) / SR
    x = (9000 * np.sin(2 * np.pi * 330 * t) + 200 * rng.standard_normal(SR)).astype(np.int64)
    x[5000] = 32767
    x[5001] = -32768
    e = K.lossless_encode(x)
    assert np.array_equal(K.lossless_decode(e["data"]), x)
    assert e["bits"] < 0.8 * 16 * len(x)
    noise = rng.integers(-32768, 32768, 20000)
    assert np.array_equal(K.lossless_decode(K.lossless_encode(noise)["data"]), noise)


def test_mdct_cancels_its_aliases():
    rng = np.random.default_rng(1)
    for N in (64, 256, 1024):
        x = rng.standard_normal(10 * N + 17)
        y = K.frames_imdct(K.frames_mdct(x, N), N, len(x))
        assert np.max(np.abs(y - x)) < 1e-11
    N = 32
    f = rng.standard_normal(2 * N)
    single = K.imdct(K.mdct(f, N), N)
    assert np.max(np.abs(single - np.sin(np.pi * (np.arange(2 * N) + 0.5) / (2 * N)) * f)) > 0.1    # alone, it is not the frame
    _, w = K.mdct_matrix(N)
    assert np.allclose(w[:N] ** 2 + w[N:] ** 2, 1.0)


def test_mask():
    N = 1024
    t = np.arange(2 * N) / SR
    x = 0.5 * np.sin(2 * np.pi * 1000 * t)
    m = K.mask(K.mdct(x, N), N)
    i = int(np.argmax(m["energy"]))
    assert m["allowed"][i] < m["energy"][i] / 10 and m["alpha"] > 0.5            # a tone: the threshold well below it
    assert m["allowed"][i + 3] < m["allowed"][i]                                  # masking falls away above
    assert K.spreading_db(0.0) == pytest.approx(0.0, abs=0.01)
    assert K.spreading_db(-1.0) < K.spreading_db(1.0)                            # steeper below than above


def test_coder_meets_its_rate():
    rng = np.random.default_rng(2)
    t = np.arange(2 * SR) / SR
    x = 0.2 * np.sin(2 * np.pi * 440 * t) + 0.1 * rng.standard_normal(len(t))
    lo, hi = K.encode(x, 24), K.encode(x, 96)
    assert lo["kbps"] == pytest.approx(24, rel=0.1) and hi["kbps"] == pytest.approx(96, rel=0.1)
    easy = K.encode(0.2 * np.sin(2 * np.pi * 440 * t), 96)
    assert easy["kbps"] <= 96 * 1.02                                             # an easy signal never takes more than asked
    assert hi["margin_db"] > lo["margin_db"]
    snr = lambda y: 10 * np.log10(np.sum(x ** 2) / np.sum((x - y) ** 2))      # noqa: E731
    assert snr(hi["y"]) > snr(lo["y"])


def test_abx():
    assert K.abx_threshold(16) == 12 and K.abx_threshold(100) == 59
    assert K.abx_power(16, 0.5) < 0.05
    assert K.abx_power(50, 0.7) > K.abx_power(16, 0.7)


def test_rvq_refines():
    rng = np.random.default_rng(3)
    V = rng.standard_normal((4000, 4))
    books = K.rvq_train(V, 3, 16)
    errs = [np.mean((V - K.rvq_encode(V, books, s)[0]) ** 2) for s in (1, 2, 3)]
    assert errs[0] > errs[1] > errs[2]
