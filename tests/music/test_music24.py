"""Part 24 of *Music, Built*: what the film says is what was computed, and every sound keeps the series' rules.

    python -m pytest -q tests/music/test_music24.py
"""

import pytest

from tests.music.partcheck import check_clips, check_ear_thread, check_scenes_and_clips, check_windows
from videos.music.music24 import compute
from videos.music.music24.manifest import SCENES
from videos.music.variations import LEDGER

load = compute.load


def test_thirds_and_imitation():
    t = load("thirds")["census"]
    assert t["fourteenth century"]["pieces"] == 89 and t["Palestrina"]["pieces"] == 1318 and t["Monteverdi"]["pieces"] == 48
    assert t["fourteenth century"]["third"] == pytest.approx(0.515, abs=0.002) and t["Palestrina"]["third"] == pytest.approx(0.840, abs=0.002)
    assert t["Palestrina"]["triad"] > 2.5 * t["fourteenth century"]["triad"]
    assert t["fourteenth century"]["final_third"] < 0.02 < 0.9 < t["Palestrina"]["final_third"]
    im = load("imitation")
    assert im["share"] == pytest.approx(0.701, abs=0.002) and im["exact"] == 1669 and im["followers"] == 2062
    top = sorted(im["intervals"].items(), key=lambda x: -x[1])[:3]
    assert [k for k, _ in top] == ["0", "5", "7"]


def test_dissonance_and_melody():
    g = load("dissonance")["groups"]
    pal = g["Palestrina"]
    assert pal["total"] == 102279 and pal["shares"]["free"] == pytest.approx(0.026, abs=0.001)
    assert pal["shares"]["passing"] > pal["shares"]["suspension"] > pal["shares"]["neighbour"] > pal["shares"]["free"]
    free = [g[k]["shares"]["free"] for k in g]
    assert free == sorted(free)                                   # Palestrina, then Books 3, 4, 5: rising
    m = load("melody")["groups"]
    assert m["Palestrina"]["forbidden_per_1000"] < 1.0 < m["fourteenth century"]["forbidden_per_1000"] < m["Monteverdi"]["forbidden_per_1000"]


def test_style_and_tuning():
    s = load("style")
    assert s["composer"]["accuracy"] == pytest.approx(0.948, abs=0.002) and s["composer"]["confusion"]["Palestrina"]["Palestrina"] == 48
    assert s["books"]["accuracy"] == pytest.approx(0.729, abs=0.002) and s["books"]["cruda_pred"] == "Books 4-5"
    c = load("tuning")["cents"]
    assert c["pythagorean"][0] - c["just"][0] == pytest.approx(21.51, abs=0.01) and abs(c["31-tone"][0] - c["just"][0]) < 1.0
    q = load("quiz")
    assert q["A"]["free"] > 10 and q["B"]["free"] == 0


def test_variation_24():
    t = load("tune")
    assert t["dissonant_beats"] == 0 and t["beats"] == 12
    v = load("variation")
    row = [r for r in LEDGER if r["part"] == 24][0]
    assert v["part"] == 24 and row["measure"] == v["measure"] and row["seconds"] == pytest.approx(v["seconds"], abs=0.05)


def test_the_part_keeps_the_series_rules():
    check_clips(compute)
    check_scenes_and_clips(compute, SCENES)
    check_windows(compute, SCENES)
    check_ear_thread(compute, SCENES)
