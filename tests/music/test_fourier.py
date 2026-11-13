"""Monochord's analysis (Part 3): each transform against a reference that does not share its code.

    python -m pytest -q tests/music/test_fourier.py
"""

import math

import numpy as np
import pytest
from scipy import signal

from explainer.music.monochord.dsp import fourier as F

SR = 48_000


def test_the_fast_transform_is_the_slow_one():
    rng = np.random.default_rng(0)
    x = rng.standard_normal(256) + 1j * rng.standard_normal(256)
    assert np.allclose(F.dft(x), np.fft.fft(x), atol=1e-9)
    count = [0]
    assert np.allclose(F.fft(x, count), np.fft.fft(x), atol=1e-10)
    assert count[0] == 128 * 8                       # (N / 2) log2 N multiplications, against N squared = 65,536
    with pytest.raises(ValueError):
        F.fft(np.zeros(100))


@pytest.mark.parametrize("name,side,lobe", [("rect", -13.3, 2.0), ("hann", -31.5, 4.0), ("hamming", -42.7, 4.0),
                                            ("blackman", -58.1, 6.0)])
def test_windows_have_their_textbook_side_lobes(name, side, lobe):
    got = F.leakage(name)
    assert got["side_lobe_db"] == pytest.approx(side, abs=0.6)       # Harris (1978), table 1
    assert got["main_lobe_bins"] == pytest.approx(lobe, abs=0.15)


def test_stft_is_scipys():
    rng = np.random.default_rng(1)
    x = rng.standard_normal(SR // 2)
    f, t, S = F.stft(x, SR, 1024, 256)
    f2, t2, S2 = signal.stft(x, SR, window="hann", nperseg=1024, noverlap=768, boundary="zeros", padded=False)
    m = min(S.shape[1], S2.shape[1])
    assert np.allclose(f, f2)
    assert np.allclose(np.abs(S[:, 2:m - 2]), np.abs(S2[:, 2:m - 2]) * 512, rtol=1e-6, atol=1e-6)   # scipy scales by the window's sum


def test_constant_q_keeps_its_promise():
    t = np.arange(SR) / SR
    freqs, times, C, q = F.cqt(np.sin(2 * np.pi * 440.0 * t), SR, fmin=110.0, n_bins=48)
    mag = np.abs(C[:, C.shape[1] // 2])
    assert freqs[int(np.argmax(mag))] == pytest.approx(440.0, rel=1e-6)          # A4 is bin 24 above A2
    assert q == pytest.approx(16.82, abs=0.01)
    # every bin is as wide, in semitones, as every other: a tone a quarter-tone off drops by the same amount low and high
    drops = []
    for f0 in (220.0, 880.0):
        _, _, Ck, _ = F.cqt(np.sin(2 * np.pi * f0 * 2 ** (0.5 / 12) * t), SR, fmin=110.0, n_bins=48)
        k = int(round(12 * math.log2(f0 / 110.0)))
        _, _, C0, _ = F.cqt(np.sin(2 * np.pi * f0 * t), SR, fmin=110.0, n_bins=48)
        m = Ck.shape[1] // 2
        drops.append(20 * math.log10(abs(Ck[k, m]) / abs(C0[k, m])))
    assert drops[0] == pytest.approx(drops[1], abs=0.3) and drops[0] < -1.0


def test_gabors_limit():
    floor = 1 / (4 * math.pi)
    t = (np.arange(4096) - 2048) / SR
    dt, df = F.spreads(np.exp(-0.5 * (t / 0.004) ** 2), SR)
    assert dt * df == pytest.approx(floor, rel=2e-3)                 # a Gaussian sits on the limit
    for name in ("hann", "hamming", "blackman", "rect"):
        dt, df = F.spreads(np.concatenate([np.zeros(1024), F.window(name, 2048), np.zeros(1024)]), SR)
        assert dt * df > floor * 1.001, name
    a, b = F.spreads(np.exp(-0.5 * (t / 0.002) ** 2), SR)             # half as long: twice as wide
    assert b / df != 0 and a * b == pytest.approx(floor, rel=5e-3)


@pytest.mark.parametrize("beta,slope", [(0.0, 0.0), (1.0, -3.01), (2.0, -6.02)])
def test_noise_has_its_colour(beta, slope):
    y = F.colored_noise(SR * 8, beta, SR, seed=3)
    assert F.octave_slope(y, SR) == pytest.approx(slope, abs=0.25)


def test_reassignment_sharpens_a_chirp():
    t = np.arange(SR // 2) / SR
    chirp = signal.chirp(t, 500.0, t[-1], 6000.0)
    freqs, times, plain, sharp = F.reassigned(chirp, SR)
    assert F.cells_for(sharp) < F.cells_for(plain) / 3            # the same energy in a third of the cells, or fewer
    # and the ridge is where the chirp is
    m = sharp.shape[1] // 2
    want = 500.0 + (6000.0 - 500.0) * times[m] / t[-1]
    assert freqs[int(np.argmax(sharp[:, m]))] == pytest.approx(want, abs=1.5 * SR / 1024)


def test_describing_a_tone():
    y = F.additive(200.0, [1, 0.5, 0.25], 1.0, SR)
    spec = np.abs(np.fft.rfft(y[4800:]))                              # after the attack
    f = np.fft.rfftfreq(len(y) - 4800, 1 / SR)
    assert f[int(np.argmax(spec))] == pytest.approx(200.0, abs=1.5)
    bright = F.additive(200.0, [1, 1, 1, 1, 1, 1], 1.0, SR)
    assert F.centroid(bright, SR) > 1.5 * F.centroid(y, SR)
    slow = F.additive(200.0, [1], 1.0, SR, attack=0.2)
    assert F.attack_time(slow, SR) == pytest.approx(0.16, abs=0.02) and F.attack_time(y, SR) < 0.01
    # reversing a sound in time leaves the strength of every frequency exactly as it was
    rng = np.random.default_rng(5)
    x = rng.standard_normal(4096)
    assert np.allclose(np.abs(np.fft.rfft(x)), np.abs(np.fft.rfft(x[::-1])), atol=1e-9)
