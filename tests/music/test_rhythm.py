"""Monochord's rhythm engine (Part 11): metres, syncopation, the pulse, polyrhythms, swing, clicks, the telephone game.

    python -m pytest -q tests/music/test_rhythm.py
"""

import math

import numpy as np
import pytest

from explainer.music.monochord import ear, rhythm as R, tune
from explainer.music.monochord.audio import SR


def test_metres_as_nested_groupings():
    assert R.meter_weights((2, 2, 2, 2)) == [5, 1, 2, 1, 3, 1, 2, 1, 4, 1, 2, 1, 3, 1, 2, 1]
    assert R.meter_weights((3, 2)) == [3, 1, 2, 1, 2, 1]                      # three-four: three beats, each of two eighths
    assert R.meter_weights((2, 3)) == [3, 1, 1, 2, 1, 1]                      # six-eight: two beats, each of three
    assert len(R.meter_weights((3, 2))) == len(R.meter_weights((2, 3))) == 6      # the same six pulses, counted another way


def test_syncopation_index():
    four = (2, 2, 2, 2)
    assert R.syncopation("x...x...x...x...", four) == 0 and R.syncopation("x.x.x.x.x.x.x.x.", four) == 0
    assert R.syncopation("x" * 16, four) == 0                                 # every pulse sounded: nothing is displaced
    clave, bossa, offs = R.syncopation("x..x..x...x.x...", four), R.syncopation("x..x..x...x..x..", four), R.syncopation("..x...x...x...x.", four)
    assert 0 < clave < bossa < offs
    assert R.syncopation(".x.x.x.x.x.x.x.x", four) > offs
    assert R.syncopation("x..x..", (2, 3)) == 0 and R.syncopation("x.x.x.", (2, 3)) > 0       # three in the time of two beats: a hemiola
    with pytest.raises(ValueError):
        R.syncopation("x..x", four)


def test_the_pulse_of_the_tune():
    ev = tune.events(0.55)
    r = R.pulse([e["t"] for e in ev])
    assert r["period"] == pytest.approx(0.55, rel=0.02) and r["phase"] == pytest.approx(0.0, abs=0.011)
    fast = R.pulse([e["t"] / 4 for e in ev])                                  # four times as fast: the beat is no longer the note
    assert fast["period"] / (0.55 / 4) == pytest.approx(round(fast["period"] / (0.55 / 4)), abs=0.05) and fast["period"] > 0.25
    assert float(R.resonance(0.55)) == 1.0 and R.resonance(0.2) < R.resonance(0.4) < 1 and R.resonance(2.2) < R.resonance(1.1)


def test_polyrhythm_and_additive_metres():
    p = R.polyrhythm(3, 2)
    assert p["grid"] == 6 and p["composite"] == [0, 2, 3, 4] and p["gaps"] == [2, 1, 1, 2] and p["together"] == [0]
    q = R.polyrhythm(4, 3)
    assert q["grid"] == 12 and q["gaps"] == [3, 1, 2, 2, 1, 3]
    assert R.compositions(7) == [(2, 2, 3), (2, 3, 2), (3, 2, 2)] and R.compositions(5) == [(2, 3), (3, 2)]
    counts = [len(R.compositions(n)) for n in range(2, 13)]
    assert counts == [1, 1, 1, 2, 2, 3, 4, 5, 7, 9, 12]
    assert all(counts[k] == counts[k - 2] + counts[k - 3] for k in range(3, len(counts)))     # Padovan's rule


def test_swing_and_acceleration():
    assert R.swing(2, 0.6, 1.0) == pytest.approx([0.0, 0.3, 0.6, 0.9])
    assert R.swing(2, 0.6, 2.0) == pytest.approx([0.0, 0.4, 0.6, 1.0])        # the triplet feel
    t = R.accelerando(2.0, 200.0, 20.0)
    rate = 1.0 / np.diff(t)
    assert rate[0] == pytest.approx(2.0, rel=0.15) and rate[-1] == pytest.approx(200.0, rel=0.02) and (np.diff(rate) > 0).all()


def test_a_fast_click_train_has_a_pitch():
    hz = 150.0
    y = R.clicks(np.arange(0, 0.6, 1 / hz), 0.6)
    f, strength = ear.pitch(y[2000:], SR, lo=60, hi=600)
    assert 1200 * abs(math.log2(f / hz)) < 10 and strength > 0.6
    both = R.clicks(np.arange(0, 0.6, 1 / 200.0), 0.6) + R.clicks(np.arange(0, 0.6, 1 / 300.0), 0.6)      # two against three, a hundred times a second
    spec = np.abs(np.fft.rfft(both * np.hanning(len(both))))
    freqs = np.fft.rfftfreq(len(both), 1 / SR)
    peaks = [freqs[int(np.argmax(spec * (abs(freqs - c) < 15)))] for c in (200.0, 300.0)]
    assert 1200 * math.log2(peaks[1] / peaks[0]) == pytest.approx(702, abs=8)                              # a perfect fifth


def test_the_telephone_game_finds_the_listeners_expectations():
    pk = np.array([R.simplex_point(r) for r in R.INTEGER_RHYTHMS])
    rng = np.random.default_rng(0)
    seeds = rng.dirichlet([1, 1, 1], 400)
    seeds = seeds[seeds.min(axis=1) > 0.12]
    w_a = np.array([1.0 if set(r) <= {1, 2} else 0.02 for r in R.INTEGER_RHYTHMS])
    w_b = np.array([1.0 if 3 in r or r == (1, 1, 1) else 0.02 for r in R.INTEGER_RHYTHMS])
    a, b = R.iterate(seeds, pk, w_a, 5, seed=1), R.iterate(seeds, pk, w_b, 5, seed=1)
    assert np.allclose(a.sum(axis=2), 1.0) and a.shape == (6, len(seeds), 3)
    d0, d5 = R.nearest_ratio(a[0], pk)[:, 1].mean(), R.nearest_ratio(a[5], pk)[:, 1].mean()
    assert d5 < 0.6 * d0                                                      # the rhythms have gathered at whole-number ratios
    share = lambda pts, w: float(np.mean(w[R.nearest_ratio(pts, pk)[:, 0].astype(int)] > 0.5))       # noqa: E731
    assert share(a[5], w_a) > 0.85 and share(b[5], w_b) > 0.85 and share(a[5], w_b) < share(b[5], w_b) - 0.3     # and at different ones for the two listeners
