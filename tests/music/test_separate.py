"""Monochord's separators (Part 64): the STFT and its inverse, SDR and SI-SDR, stereo tricks, FastICA, HPSS, supervised
NMF, the oracle masks, Griffin-Lim and the mask network.

    python -m pytest -q tests/music/test_separate.py
"""

import numpy as np
import pytest

from explainer.music.monochord.mir import separate as S
from explainer.music.monochord.partkit import organ_tone

SR = 48000


def tones(midis, seconds=2.0, partials=6):
    y = np.zeros(int(seconds * SR))
    for k, m in enumerate(midis):
        z = organ_tone(440 * 2 ** ((m - 69) / 12), 0.45, partials=partials, rolloff=0.7)
        i = int(k * 0.5 * SR)
        y[i:i + len(z)] += z[: len(y) - i]
    return y


def clicks(seconds=2.0, every=0.25, seed=0):
    """Short noise bursts, as loud overall as the tones."""
    rng = np.random.default_rng(seed)
    y = np.zeros(int(seconds * SR))
    n = int(0.01 * SR)
    for t in np.arange(0.05, seconds - 0.05, every):
        i = int(t * SR)
        y[i:i + n] += rng.standard_normal(n) * np.exp(-np.arange(n) / (0.002 * SR))
    return y * 0.9 / np.std(y)


def test_stft_round_trip_and_scores():
    x = np.random.default_rng(1).standard_normal(SR)
    y = S.istft(S.stft(x), len(x))
    assert np.max(np.abs(y[2048:-2048] - x[2048:-2048])) < 1e-9
    assert S.sdr(x, 0.5 * x) == pytest.approx(20 * np.log10(2), abs=1e-6)          # 6.02 dB: a gain counts as error
    assert S.si_sdr(x, 0.5 * x) > 100                                             # ...but not for the scale-invariant score
    assert S.sdr(x, -x) == pytest.approx(-20 * np.log10(2), abs=1e-6)


def test_centre_cancellation_and_pan_masks():
    a, b = tones([60, 64, 67, 72]), tones([55, 59, 62, 67], partials=4)
    th = np.pi / 4 * (1 + 60 / 90)                                                 # b panned 60 degrees left
    L, R = np.sin(np.pi / 4) * a + np.sin(th) * b, np.cos(np.pi / 4) * a + np.cos(th) * b
    side = S.centre_cancel(L, R)
    assert np.corrcoef(side, b)[0, 1] > 0.999                                      # the centred source is gone
    ib = (np.sin(th) - np.cos(th)) / (np.sin(th) + np.cos(th))
    (est,) = S.pan_masks(L, R, centres=[ib], width=0.15)
    assert S.sdr((np.sin(th) + np.cos(th)) / 2 * b, est) > 5


def test_fastica_unmixes_an_instantaneous_mixture():
    rng = np.random.default_rng(2)
    s = np.array([rng.laplace(size=20000), rng.uniform(-1, 1, 20000)])
    X = np.array([[0.9, 0.35], [0.4, 0.85]]) @ s
    out = S.fastica(X)["S"]
    for src in s:
        assert max(abs(np.corrcoef(src, o)[0, 1]) for o in out) > 0.99


def test_hpss_splits_lines_from_stripes():
    h, p = tones([60, 64, 67, 72]), clicks()
    r = S.hpss(h + p)
    assert S.sdr(h, r["harmonic"]) > 8 and S.sdr(p, r["percussive"]) > 3
    assert 0 <= r["mask"].min() and r["mask"].max() <= 1


def test_oracles_bound_and_nmf_separates():
    a, b = tones([60, 62, 64, 65]), tones([48, 50, 52, 53], partials=3)
    o = S.oracle_masks({"a": a, "b": b})
    assert S.sdr(a, o["irm"]["a"]) > 10 and S.sdr(a, o["true_phase"]["a"]) >= S.sdr(a, o["irm"]["a"]) - 0.5
    est = S.nmf_separate(a + b, {"a": tones([61, 63, 64, 66]), "b": tones([47, 50, 51, 53], partials=3)}, rank=6, iters=80)
    assert S.sdr(a, est["a"]) > 5 and S.sdr(b, est["b"]) > 3


def test_griffin_lim_is_consistent_not_correct():
    x = tones([60, 64, 67, 72])
    mag = np.abs(S.stft(x))
    y = S.griffin_lim(mag, len(x), iters=40)
    incons = np.linalg.norm(np.abs(S.stft(y)) - mag) / np.linalg.norm(mag)
    assert incons < 0.35                                                           # a spectrogram close to the target
    assert S.sdr(x, y) < 3                                                         # but not the signal itself


def test_mask_network_learns_a_source():
    a = [tones([60 + k, 64 + k, 67 + k, 72 + k], seconds=2.0) for k in range(4)]
    b = [clicks(seed=k) for k in range(4)]
    fit = S.mask_net_train([x + y for x, y in zip(a, b)], a, epochs=8, hidden=64)
    assert fit["losses"][-1] < fit["losses"][0]
    test_a, test_b = tones([62, 65, 69, 74]), clicks(seed=9)
    est = S.mask_net_apply(fit, test_a + test_b)
    assert S.sdr(test_a, est) > S.sdr(test_a, test_a + test_b)                     # better than doing nothing
