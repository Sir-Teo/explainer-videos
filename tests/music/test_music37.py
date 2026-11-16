"""Part 37 of *Music, Built*: what the film says is what was computed, and every sound keeps the series' rules.

    python -m pytest -q tests/music/test_music37.py
"""

import pytest

from tests.music.partcheck import check_clips, check_ear_thread, check_scenes_and_clips, check_windows
from videos.music.music37 import compute
from videos.music.music37.manifest import SCENES
from videos.music.variations import LEDGER

load = compute.load


def test_pattern_and_scale():
    s = load("scale")
    assert s["steps"] == s["major_steps"] == [2, 2, 1, 2, 2, 2, 1]
    assert [s["intervals"][str(k)] for k in range(1, 7)] == [2, 5, 4, 3, 6, 1]
    h = load("hook")
    assert h["onsets"] == [0, 2, 4, 5, 7, 9, 11]


def test_measures_as_said():
    m = load("metrics")
    rows = {r["name"]: r for r in m["rows"]}
    assert rows["standard pattern (12)"]["offbeat"] == 3 and not rows["standard pattern (12)"]["oddity"]
    sixteen = {k: r["uneven"] for k, r in rows.items() if k.endswith("(16)")}
    assert min(sixteen, key=sixteen.get) == "bossa nova (16)" and max(sixteen, key=sixteen.get) == "soukous (16)"
    assert [k for k in ("son clave (16)", "rumba clave (16)", "bossa nova (16)") if rows[k]["oddity"]] == ["son clave (16)", "rumba clave (16)", "bossa nova (16)"]
    assert m["most_central"] == "son clave (16)" and m["centrality"]["son clave (16)"] == 6 and m["centrality"]["bossa nova (16)"] == 8
    t = load("threetwo")
    assert len(t["on_four"]) == 2 and len(t["on_six"]) == 3 and len(t["on_three"]) == 2


def test_hocket_and_inherent():
    h = load("hocket")
    assert all((a is None) != (b is None) for a, b in zip(h["ira"], h["arka"]))
    i = load("inherent")
    assert i["answer"] == "B" and i["options"]["B"] == [p for _, p in sorted(i["target"])]
    assert i["high_a"] != i["options"]["B"] and len(i["high_a"]) + len(i["high_b"]) == 12
    assert i["rate_fast"] == pytest.approx(10.0) and i["rate_slow"] < 4


def test_clave_and_son():
    c = load("clave")
    assert c["three_two"] == [0, 3, 6, 10, 12] and c["two_three"] == [2, 4, 8, 11, 14]
    s = load("son")
    assert s["chords"] == ["C", "F", "G", "F"]
    # In sixteenth-note units, 3–2 son clave spans two 4/4 bars.
    assert s["clave_period"] == 32
    assert s["clave"] == [0, 6, 12, 20, 24]
    assert [o for o in s["clave"] if o < 16] == [0, 6, 12]
    assert [o - 16 for o in s["clave"] if o >= 16] == [4, 8]


def test_variation_37():
    t = load("tune")
    assert len(t["high_a"]) + len(t["high_b"]) == 14 and t["n"] == 48
    assert t["high_a"] != [m for m, _, _ in t["melody"]] and t["high_b"] != [m for m, _, _ in t["melody"]]
    v = load("variation")
    row = [r for r in LEDGER if r["part"] == 37][0]
    assert v["part"] == 37 and row["measure"] == v["measure"] and row["seconds"] == pytest.approx(v["seconds"], abs=0.05)


def test_the_part_keeps_the_series_rules():
    check_clips(compute)
    check_scenes_and_clips(compute, SCENES)
    check_windows(compute, SCENES)
    check_ear_thread(compute, SCENES)
