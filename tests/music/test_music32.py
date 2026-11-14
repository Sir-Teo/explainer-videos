"""Part 32 of *Music, Built*: what the film says is what was computed, and every sound keeps the series' rules.

    python -m pytest -q tests/music/test_music32.py
"""

import pytest

from tests.music.partcheck import check_clips, check_ear_thread, check_scenes_and_clips, check_windows
from videos.music.music32 import compute
from videos.music.music32.manifest import SCENES
from videos.music.variations import LEDGER

load = compute.load


def test_hook_strip_triangle():
    assert load("hook")["same_pitches"]
    s = load("strip")
    assert len(s["points"]) == 78
    assert {p[1] for p in s["motions"]["parallel"]["points"]} == {3} and {p[0] for p in s["motions"]["contrary"]["points"]} == {2.0}
    d = load("duet")
    assert d["actual"] == [int(x) for x in d["sizes"]]                                   # every step a shortest path
    t = load("triangle")
    assert len(t["points"]) == 91 and t["walk_even"][-1] == pytest.approx(0) and t["walk_even"] == sorted(t["walk_even"], reverse=True)
    n = load("neutral")
    assert min(n["even"]) == n["even"][2]


def test_sizes_and_evenness():
    v = load("vlsize")
    assert v["answer"] == "A" and v["ways"]["A"]["taxicab"] == 3 and v["ways"]["B"]["taxicab"] == 15 and v["ways"]["C"]["taxicab"] == 9
    tri = v["triads"]
    assert sorted(k for k, x in tri.items() if x == 6) == ["Bb", "D", "F#"] and sum(1 for x in tri.values() if x == 2) == 5
    e = load("even")
    better = sorted(tuple(r["prime"]) for r in e["rows"] if r["vl"] < r["size"])
    assert better == [(0, 1, 5, 7), (0, 2, 5, 8), (0, 3, 5, 8), (0, 3, 7)]
    assert [x["size"] for x in e["demos"]] == [2, 2, 1]
    s = load("scales")
    assert s["count"] == 38 and s["top"][0]["name"] == "diatonic" and s["melodic_minor"]["rank"] == 2 and s["harmonic_minor"]["rank"] == 3
    assert s["circle"] == {str(k): float(min((7 * k) % 12, 12 - (7 * k) % 12)) for k in range(12)}


def test_optic_fourier_bach():
    o = load("optic")
    assert o["3"]["OP"] == 364 and o["3"]["OPT"] == 31 and o["3"]["OPTIC"] == 19 and o["4"]["OPTIC"] == 48
    f = load("fourier")
    assert f["answer"] == "B" and f["order"][1] == "pentatonic"
    b = load("bach")
    assert b["upper"]["n"] == 17339 and 0.6 < b["upper"]["minimal_share"] < 0.7 and 0.35 < b["all"]["minimal_share"] < 0.45
    assert b["upper"]["mean_minimal"] < b["upper"]["mean_actual"] < b["upper"]["mean_shuffled"]
    assert b["answer"] == "A" and b["tot_a"] < b["tot_b"]


def test_variation_32():
    t = load("tune")
    assert t["plain"]["chain"][0] == t["plain"]["chain"][-1] == "C" and t["far"]["total"] - t["plain"]["total"] == 2
    v = load("variation")
    row = [r for r in LEDGER if r["part"] == 32][0]
    assert v["part"] == 32 and row["measure"] == v["measure"] and row["seconds"] == pytest.approx(v["seconds"], abs=0.05)


def test_the_part_keeps_the_series_rules():
    check_clips(compute)
    check_scenes_and_clips(compute, SCENES)
    check_windows(compute, SCENES)
    check_ear_thread(compute, SCENES)
