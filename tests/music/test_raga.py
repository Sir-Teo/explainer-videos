"""Monochord's raga and tala (Part 34)."""

import numpy as np

from explainer.music.monochord import raga as R


def test_jawari_brightens():
    plain = R.jawari_string(130.0, 1.0, bridge=False)
    jaw = R.jawari_string(130.0, 1.0, bridge=True)
    _, cp = R.centroid_track(plain)
    _, cj = R.centroid_track(jaw)
    assert cj[:6].mean() > 2 * cp[:6].mean()
    assert np.isfinite(jaw).all() and abs(np.abs(jaw).max() - 1) < 1e-9


def test_scales():
    assert len(R.thaat_space()) == 32 and all(v in R.thaat_space() for v in R.THAATS.values())
    m = R.melakartas()
    assert len(m) == 72 and len(set(m)) == 72
    assert R.melakarta_number((0, 2, 4, 5, 7, 9, 11)) == 29 and R.melakarta_number((0, 2, 4, 6, 7, 9, 11)) == 65
    assert R.melakarta_number((0, 1, 4, 5, 7, 8, 11)) == 15
    assert len(R.SHRUTIS) == 22 and abs(R.cents(R.SHRUTIS[4]) - R.cents(R.SHRUTIS[3]) - 21.51) < 0.01


def test_tihai():
    assert R.tihai(16, 5, [3], [2])[0]["end"] == 16
    assert R.tihai(16, 3, [5], [0])[0]["end"] == 16
    assert R.tihai(16, 5, [3], [1]) == []
    for st in range(1, 17):                                        # the defining equation, checked by brute counting
        for sol in R.tihai(16, st, range(1, 9), range(0, 5)):
            strokes = []
            pos = st - 1
            for _ in range(3):
                strokes += list(range(pos, pos + sol["p"]))
                pos += sol["p"] + sol["g"]
            assert strokes[-1] % 16 == 0


def test_strokes_and_contours():
    for b in ("dha", "dhin", "tin", "ta", "na", "ge", "ka", "tirakita"):
        y = R.stroke(b)
        assert abs(np.abs(y).max() - 1) < 1e-9
    c = R.gamaka_contour([(0, 0.5), (4, 0.5)], glide=0.1)
    assert c[0] == 0 and abs(c[-1] - 4) < 1e-9
    cents, h = R.pitch_histogram(c)
    assert h.sum() == len(c)
