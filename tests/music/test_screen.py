"""Monochord's music for picture and play (Part 44): click arithmetic, the tempo finder, the chip, the adaptive score
and ducking.

    python -m pytest -q tests/music/test_screen.py
"""

import numpy as np
import pytest

from explainer.music.monochord import SR
from explainer.music.monochord import screen as S


def test_click_arithmetic():
    assert S.click(120) == (12, 0, 12.0)
    w, e, f = S.click(100)
    assert (w, e) == (14, 3) and f == pytest.approx(14.4)
    assert S.click_bpm(12, 0) == pytest.approx(120.0) and S.click_bpm(14, 3) == pytest.approx(100.17, abs=0.01)


def test_tempo_finder_lands_every_hit():
    hits = [3.2, 7.95, 11.4]
    r = S.find_tempo(hits, start=0.5, lo=70, hi=160, tol_frames=1.0)
    assert r["solutions"]
    for s in r["solutions"]:
        per = 60.0 / s["bpm"]
        for h, b in zip(hits, s["beats"]):
            assert abs((h - 0.5) - b * per) * 24 <= 1.0 + 1e-9
    exact = S.variable_click(hits, [4, 11, 16], 0.5)
    t = 0.5
    for seg, (b0, b1) in enumerate(zip([0, 4, 11], [4, 11, 16])):
        t += (b1 - b0) * 60.0 / exact[seg]
        assert t == pytest.approx(hits[seg])


def test_pulse_harmonics_and_chip():
    h = S.pulse_harmonics(0.25, 12)
    assert h[3] < 1e-12 and h[7] < 1e-12 and h[0] == pytest.approx(1.0)
    assert all(S.pulse_harmonics(0.5, 10)[1::2] < 1e-12)
    chip = S.Chip()
    y = chip.pulse(440.0, 0.5, 0.25)
    assert abs(np.mean(y > 0) - 0.25) < 0.01                             # high a quarter of the time
    t = chip.triangle(110.0, 0.2)
    assert len(np.unique(np.round(t, 6))) <= 16                         # 4 bits
    a = chip.arpeggio([261.6, 329.6, 392.0], 0.5, rate=60.0)
    assert len(a) == int(0.5 * SR)


def test_adaptive_score_waits_for_boundaries():
    g = S.simulate(3, 48.0)
    sc = S.Score(120.0)
    for q, unit in (("beat", 0.5), ("bar", 2.0), ("phrase", 4.0)):
        plan = S.adapt(g, sc, q)
        for sw in plan["switches"]:
            assert 0 <= sw["delay"] < unit + 1e-9 and abs(sw["switch"] / unit - round(sw["switch"] / unit)) < 1e-9
    assert S.adapt(g, sc, "now")["mean_delay"] == 0.0
    d = [s["delay"] for seed in range(100) for s in S.adapt(S.simulate(seed, 120.0), sc, "bar")["switches"][1:]]
    assert np.mean(d) == pytest.approx(S.expected_delay(2.0), abs=0.08)


def test_ducking_makes_room():
    t = np.arange(SR * 2) / SR
    music = 0.5 * np.sin(2 * np.pi * 2000 * t)
    voice = np.where((t > 0.5) & (t < 1.5), 0.3 * np.sin(2 * np.pi * 1500 * t), 0.0)
    r = S.duck(music, voice, depth_db=10.0)
    assert r["ratio_after_db"] > r["ratio_before_db"] + 3
    assert np.min(20 * np.log10(r["gain"])) == pytest.approx(-10.0, abs=0.01)
