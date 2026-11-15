"""Monochord's auditory scene (Part 45): the scale illusion, the streaming model, interleaving, grouping cues,
Shepard tones and the timbre space.

    python -m pytest -q tests/music/test_scene.py
"""

import numpy as np
import pytest

from explainer.music.monochord import SR
from explainer.music.monochord import scene as S


def test_erb_rate_and_scale_illusion():
    assert S.erb_rate(1000.0) == pytest.approx(15.6, abs=0.1)
    s = S.scale_illusion(60)
    assert sorted(s["right"] + s["left"]) == sorted(s["up"] + s["down"])
    assert S.leaps(s["right"]) > 4 * S.leaps(s["heard_high"])           # each ear leaps; the heard lines step
    assert s["heard_high"] == [72, 71, 69, 67, 67, 69, 71, 72]


def test_streaming_model_is_a_straight_line():
    k = 30.0
    for trt in (0.05, 0.1, 0.15):
        b = float(S.boundary(trt, 1000.0, tau=1.0, width=k))
        assert S.streams(b + 0.5, trt, 1000.0, tau=1.0, width=k) and not S.streams(b - 0.5, trt, 1000.0, tau=1.0, width=k)
    dz = [float(S.erb_rate(1000 * 2 ** (S.boundary(t, 1000.0, 1.0, k) / 12)) - S.erb_rate(1000.0)) for t in (0.05, 0.1, 0.15)]
    assert dz[1] - dz[0] == pytest.approx(dz[2] - dz[1], rel=1e-6) and dz[0] == pytest.approx(k * 0.05)
    f = S.fit_boundary(S.VAN_NOORDEN_TCB)
    assert f["rms_st"] < 0.5


def test_interleaving_and_grouping_stimuli():
    a, b = [60, 62, 64, 65], [64, 60, 66, 62]
    assert S.interleave(a, b) == [60, 64, 62, 60, 64, 66, 65, 62] and S.crossings(a, b) == 3
    y = S.harmonic_complex(200.0, 10, 1.0, mistune=0.03, which=4)
    sp = np.abs(np.fft.rfft(y[int(0.1 * SR):int(0.9 * SR)]))
    f = np.fft.rfftfreq(int(0.8 * SR), 1 / SR)
    assert abs(f[np.argmax(sp * ((f > 780) & (f < 860)))] - 824.0) < 3.0
    assert S.pop_out(0.03) > 0 and S.pop_out(0.005) == 0.0
    g = S.continuity(0.15, "silence")
    mid = int(0.8 * SR)
    assert np.all(g[mid - 100: mid + 100] == 0.0)


def test_shepard_tones_return_to_the_start():
    y = S.shepard(13, 1.0, tone=0.2, gap=0.0)
    n = int(0.2 * SR)
    first, last = y[:n], y[12 * n: 13 * n]
    assert np.corrcoef(first, last)[0, 1] > 0.999


def test_features_and_space():
    t = np.arange(SR) / SR
    slow = np.sin(2 * np.pi * 220 * t) * np.clip(t / 0.2, 0, 1)
    fast = np.sin(2 * np.pi * 220 * t) * np.clip(t / 0.002, 0, 1) * np.exp(-3 * t)
    fs, ff = S.features(slow, 220.0), S.features(fast, 220.0)
    assert fs["attack_ms"] > 10 * ff["attack_ms"] and ff["decay_db_s"] < fs["decay_db_s"]
    sq = np.sign(np.sin(2 * np.pi * 220 * t))
    assert S.features(sq, 220.0)["odd_even_db"] > 20                    # a square wave has odd harmonics only
    feats = {f"x{i}": {"attack_ms": 1 + i, "brightness": 1 + (i % 3), "odd_even_db": i % 2, "irregularity_db": i, "decay_db_s": -i} for i in range(6)}
    sp = S.timbre_space(feats)
    assert len(sp["coords"]) == 6 and 0 < sum(sp["share"]) <= 1.0 + 1e-9
