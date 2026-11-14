"""Part 17 of *Music, Built*: what the film says is what was computed, and every sound keeps the series' rules.

    python -m pytest -q tests/music/test_music17.py
"""

import pytest

from explainer.music.monochord import fourpart as F
from tests.music.partcheck import check_clips, check_ear_thread, check_scenes_and_clips, check_windows
from videos.music.music17 import compute
from videos.music.music17.manifest import SCENES
from videos.music.variations import LEDGER

load = compute.load


def test_the_hook_and_the_book():
    h = load("hook")
    assert h["name"] == "bwv244.62" and h["mode"] == "minor" and h["parallels_full"] == []
    assert len(h["parallels_plain"]) >= 4                                                       # the chord-chooser's parallels
    assert [n[0] for n in h["plain"][0]] == [n[0] for n in h["bach"][0]]                        # both keep Bach's tune
    b = load("book")
    assert b["count"] == 364 and b["modes"]["major"] == 185 and b["modes"]["minor"] == 178
    assert b["tunes"] == 230 and b["set_more"] == 59 and len(b["passion"]) == 11 and b["notes"] == 84737
    a, z = b["two"]["voices"]
    assert [n[0] - 2 for n in a[0]] == [n[0] for n in z[0]]                                     # the same tune, a tone lower
    assert [n[0] for n in a[3]] != [n[0] + 2 for n in z[3]]                                     # and another bass


def test_ranges_motion_and_doubling():
    r = load("ranges")
    assert r["outside"][0] < 1e-4 and 0.005 < r["outside"][3] < 0.01
    assert round(r["gap_mean"]["S-A"], 1) == 5.3 and round(r["gap_mean"]["T-B"], 1) == 8.6 and 0.15 < r["gap_over_octave"]["T-B"] < 0.25
    d = r["doubling"]
    assert d["0:root"] / (d["0:root"] + d["0:third"] + d["0:fifth"]) == pytest.approx(0.87, abs=0.01)
    m = load("motion")
    st = m["stats"]
    assert st[3]["mean"] > 3 and all(s["mean"] < 2.1 for s in st[:3]) and st[1]["repeat"] == max(s["repeat"] for s in st)
    sh = m["shortest"]
    assert sh["least"] < sh["actual"] and round(sh["actual"], 1) == 3.6 and round(100 * sh["same"]) == 68 and round(100 * sh["within2"]) == 80


def test_rules_and_the_census():
    ru = load("rules")["demos"]
    assert ru["parallel"]["wrong_par"] and not ru["parallel"]["right_par"]
    for k in ("leading", "seventh", "spacing"):
        assert not ru[k]["wrong_par"] and not ru[k]["right_par"]
    assert ru["spacing"]["spacing"]["wrong"] == [False, False] and ru["spacing"]["spacing"]["right"] == [True, True]
    c = load("census")
    assert c["parallel"] == {"fifths": 52, "octaves": 23} and round(c["rate"]) == 391
    assert len(c["all"]) == 75 and c["on_beat"] == 24 and c["pairs"]["S–T"] == max(c["pairs"].values())
    assert c["hidden"] == 157 and c["overlap"] == 1735 and c["crossing"] == 733


def test_chords_cadences_and_decoration():
    v = load("vocab")
    assert [n for n, _ in v["major"]["top"][:6]] == ["I", "V", "vi", "IV", "ii", "II"]
    assert [n for n, _ in v["minor"]["top"][:4]] == ["i", "III", "iv", "V"] and round(100 * v["major"]["same_next"]) == 23
    cad = load("cadences")
    assert cad["major"]["pairs"][0][:2] == ["V", "I"] and cad["minor"]["pairs"][1][:2] == ["VII", "III"]
    assert cad["minor"]["finals"]["I"] == 104 and cad["minor"]["finals"]["i"] == 11 and cad["major"]["total"] == 1216
    d = load("decoration")
    tot = {j: sum(d["per_voice"][j].values()) for j in "0123"}
    assert tot["0"] == min(tot.values()) and tot["3"] == max(tot.values())
    assert all(d["per_voice"][j]["passing"] > d["per_voice"][j]["neighbour"] for j in "0123") and round(100 * d["share"]) == 55


def test_the_harmonizer_against_bach():
    hz = load("harmonizer")
    assert hz["beats"] == 16 and min(hz["states"]) > 100 and hz["log10_paths"] > 35
    e = load("evaluation")
    assert e["test"] == 83 and e["train"] == 280
    f, p, b = e["full"], e["plain"], e["bach"]
    assert f["parallels"] == 0 and p["parallels"] > 500 and b["parallels"] == 77
    assert 0.35 < f["same_chord"] < 0.5 and f["same_bass"] > p["same_bass"] + 0.1
    assert f["inner_motion"] < 0.6 * b["inner_motion"]
    i = load("improve")["notes_per_beat"]
    assert i["ours"] < i["decorated"] < i["bach"]


def test_variation_17():
    t = load("tune")
    assert t["parallels_full"] == [] and len(t["parallels_plain"]) >= 3 and len(t["soprano"]) == 42
    for a, z in zip(t["full"], t["full"][1:]):
        assert not F.parallels(a, z) and F.in_range(z) and F.spacing_ok(z)
    v = load("variation")
    row = [r for r in LEDGER if r["part"] == 17][0]
    assert v["part"] == 17 and row["measure"] == v["measure"] and row["seconds"] == pytest.approx(v["seconds"], abs=0.05)


def test_the_part_keeps_the_series_rules():
    check_clips(compute)
    check_scenes_and_clips(compute, SCENES)
    check_windows(compute, SCENES)
    check_ear_thread(compute, SCENES)
