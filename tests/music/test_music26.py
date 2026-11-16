"""Part 26 of *Music, Built*: what the film says is what was computed, and every sound keeps the series' rules.

    python -m pytest -q tests/music/test_music26.py
"""

import numpy as np
import pytest

from tests.music.partcheck import check_clips, check_ear_thread, check_scenes_and_clips, check_windows
from videos.music.music26 import compute
from videos.music.music26.manifest import SCENES
from videos.music.variations import LEDGER

load = compute.load


def test_phrases_and_plan():
    p = load("phrases")
    assert p["answer"] == "B" and p["cadences"] == 146
    g = {int(k): v for k, v in p["gaps"].items()}
    assert max(g, key=g.get) == 4 and g[4] == 14 and g[8] == 10       # the peaks: four bars, then eight
    per = p["periodic"]
    assert per["mozart"] == pytest.approx(0.296, abs=0.002) and per["haydn"] == pytest.approx(0.105, abs=0.002)
    pl = load("plan")
    assert pl["bars"] == 154 and pl["exp_bar"] == 16 and pl["rec_bar"] == 102 and pl["answer"] == "B"
    keys = [tuple(t["key"]) for t in pl["plan"]]
    late = [tuple(t["key"]) for t in pl["plan"] if t["bar"] >= 90]
    assert keys[0] == (0, "major") and (7, "major") in keys
    assert max(set(late), key=late.count) == (0, "major")        # home again in the recapitulation


def test_the_census_and_the_wrong_key():
    k = load("keys")
    assert k["agree"] == 20 and k["major"] == 18 and k["minor"] == 2
    assert k["tally"]["major|V"] == 14 and k["tally"]["minor|III"] == 2
    w = [tuple(x["key"]) for x in k["plan4"][:4]]
    assert w[0] == (0, "major") and (4, "minor") in w      # Op. 59 No. 2's finale: C major first, then E minor
    assert k["settle"] == 46


def test_texture_three_and_style():
    t = load("texture")["by"]
    assert t["haydn"]["shares"][0] == pytest.approx(0.620, abs=0.002) and t["beethoven"]["shares"][0] == pytest.approx(0.545, abs=0.002)
    s = load("three")["stats"]
    assert (s["haydn"]["movements"], s["mozart"]["movements"], s["beethoven"]["movements"]) == (9, 15, 9)
    assert s["beethoven"]["span"] > s["haydn"]["span"] + 8
    st = load("style")
    assert st["n"] == 33 and st["acc26"] == pytest.approx(17 / 33) and st["acc24"] == pytest.approx(14 / 33)
    assert st["chance"] == pytest.approx(15 / 33) and st["conf26"]["beethoven"]["beethoven"] == 6
    assert st["p_perm"] == pytest.approx(109 / 2001) and np.mean(st["null"]) == pytest.approx(1 / 3, abs=0.02)
    assert st["singles"][0][0] == "register span"
    m = load("minuet")
    assert m["in34"] == 11 and m["bar_beats"] == 3.0


def test_variation_26():
    t = load("tune")
    assert t["notes"] == {"theme": 14, "minore": 14, "adagio": 28, "finale": 26}
    v = load("variation")
    row = [r for r in LEDGER if r["part"] == 26][0]
    assert v["part"] == 26 and row["measure"] == v["measure"] and row["seconds"] == pytest.approx(v["seconds"], abs=0.05)


def test_the_part_keeps_the_series_rules():
    check_clips(compute)
    check_scenes_and_clips(compute, SCENES)
    check_windows(compute, SCENES)
    check_ear_thread(compute, SCENES)
