"""Monochord's performer (Part 43): rules of expression, the kinematic ritardando, vibrato, phase correction and the
identity test.

    python -m pytest -q tests/music/test_perform.py
"""

import numpy as np
import pytest

from explainer.music.monochord import SR
from explainer.music.monochord import perform as P


def test_deadpan_and_rules():
    sc, ph = P.tune_score()
    dp = P.deadpan(sc, bpm=120)
    assert dp[1]["t"] == pytest.approx(0.5) and len(dp) == len(sc) == 42
    pf = P.perform(sc, ph)
    dev, vel = P.deviations(pf, sc)
    first = [i for i in range(len(ph)) if i == 0 or ph[i] != ph[i - 1]]
    mids = [i + 3 for i in first]
    assert all(dev[i] > dev[m] for i, m in zip(first, mids))            # slower at phrase starts than in the middle
    assert max(vel) - min(vel) > 0.2 and dev[-1] > 1.0                  # loudness moves; the end is slowed
    assert P.perform(sc, ph, k=0.0)[5]["t"] == pytest.approx(dp[5]["t"] * 120 / 100)


def test_kinematic_ritardando():
    x = np.linspace(0, 1, 11)
    for q in (1, 2, 3):
        v = P.ritardando(x, 0.5, q)
        assert v[0] == pytest.approx(1.0) and v[-1] == pytest.approx(0.5) and np.all(np.diff(v) < 0)
    v2 = P.ritardando(x, 0.5, 2)
    assert np.allclose(v2 ** 2, 1 - 0.75 * x)                          # speed squared falls linearly: constant braking
    assert P.ritardando(0.48, 0.5, 2) == pytest.approx(0.8, abs=1e-6)
    assert P.ritardando(0.5, 0.5, 3) > P.ritardando(0.5, 0.5, 2) > P.ritardando(0.5, 0.5, 1)


def test_vibrato_tone_has_its_mean_pitch():
    y = P.vibrato_tone(440.0, 2.0, rate=5.5, cents=60.0)
    seg = y[int(0.5 * SR): int(1.95 * SR)]
    S = np.abs(np.fft.rfft(seg * np.hanning(len(seg)), 1 << 18))
    f = np.fft.rfftfreq(1 << 18, 1 / SR)
    band = (f > 380) & (f < 500)
    centroid = (f[band] * S[band] ** 2).sum() / (S[band] ** 2).sum()
    assert abs(centroid - 440.0) < 3.0


def test_phase_correction_matches_its_formula_and_bounds():
    for a in (0.3, 1.0, 1.7):
        r = P.phase_correction([a / 2, a / 2], n=20000, rng=np.random.default_rng(3))
        sd = r["asynchrony"][200:, 1].std()
        assert sd == pytest.approx(np.sqrt(P.asynchrony_variance(a)), rel=0.06)
    assert P.asynchrony_variance(0.0) == float("inf") and P.asynchrony_variance(2.0) == float("inf")
    r = P.phase_correction([0.0, 0.0], n=50, period=[0.5, 0.51], timer_sd=0.0, motor_sd=0.0)
    assert r["asynchrony"][-1, 1] == pytest.approx(49 * 0.01)            # no correction: the tempo difference accumulates
    r = P.phase_correction([0.1, 2.3], n=60, rng=np.random.default_rng(1))
    assert abs(r["asynchrony"][-1, 1]) > 1.0                            # beyond 2: unstable


def test_identity_of_a_time_stretched_copy():
    sc, ph = P.tune_score()
    curves = {i: P.tempo_curve(P.play(P.pianist(i), sc, ph)) for i in range(6)}
    copy = P.tempo_curve(P.play(P.pianist(4), sc, ph, stretch=1.04))
    rank = P.identify(curves, copy)
    assert rank[0][0] == 4 and rank[0][1] > 0.9999 and rank[1][1] < 0.97
