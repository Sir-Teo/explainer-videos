"""Monochord's song studio (Part 40): drum-machine voices, patterns, sidechain, chopping, prosody and flow.

    python -m pytest -q tests/music/test_song.py
"""

import numpy as np

from explainer.music.monochord import SR
from explainer.music.monochord import song as S


def test_kick_is_a_struck_resonator():
    k = S.kick808(52.0, 0.45)
    assert abs(S.measured_pitch(k) - 52.0) < 1.0
    assert S.measured_pitch(k, 0.0, 0.01) > 60.0                       # the strike's upward detuning
    env = np.abs(k)
    a = env[int(0.10 * SR): int(0.12 * SR)].max()
    b = env[int(0.55 * SR): int(0.57 * SR)].max()
    assert abs(np.log(a / b) - 0.45 / 0.45) < 0.15                      # amplitude falls by e in one decay time


def test_hat_is_six_square_waves():
    f, spec = S.hat_spectrum()
    for hz in S.HAT_HZ:
        i = np.argmin(np.abs(f - hz))
        assert spec[i - 2: i + 3].max() > 0.05 * spec.max()
    h = S.hat808()
    F = np.fft.rfftfreq(len(h), 1 / SR)
    P = np.abs(np.fft.rfft(h)) ** 2
    assert P[F > 7000].sum() > 0.8 * P.sum()                           # high-passed


def test_patterns():
    assert S.backbeat_share(S.PATTERNS["rock"]) == 1.0 and S.PATTERNS["disco"]["kick"] == [0, 4, 8, 12]
    assert S.PATTERNS["trap"]["snare"] == [8]                           # half time


def test_sidechain_and_chop():
    y = np.ones(SR)
    z, g = S.sidechain(y, [0.1], depth_db=12.0, release=0.2)
    assert abs(20 * np.log10(g.min()) + 12.0) < 0.01
    t_back = 0.1 + 0.005 + 0.2 * np.log(12.0)                           # within 1 dB after release * ln(depth)
    assert 20 * np.log10(g[int((t_back + 0.002) * SR)]) > -1.0
    c, starts = S.chop(np.arange(1000.0), 4, [3, None, 0], slice_len=250 / SR)
    assert len(c) == 750 and c[260] == 0.0 and starts == [750 / SR, None, 0.0]


def test_prosody_and_flow():
    good = S.prosody([("BEAU", True, 0), ("ti", False, 2), ("ful", False, 3), ("DAY", True, 4)])
    bad = S.prosody([("beau", False, 0), ("TI", True, 2), ("FUL", True, 3), ("day", False, 5)])
    assert good["agree"] == 1.0 and bad["agree"] == 0.25
    syl = [("a", True, 0, None), ("b", False, 1, None), ("c", False, 2, None), ("d", True, 3, "A"), ("e", True, 6, None)]
    f = S.flow(syl, 1)
    assert f["gaps"] == [3, 3] and f["per_beat"] == 5 / 4 and f["rhyme_share"] == 0.2 and f["on_beat"] == 0.2
