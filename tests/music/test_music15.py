"""Part 15 of *Music, Built*: what the film says is what was computed, and every sound keeps the series' rules.

    python -m pytest -q tests/music/test_music15.py
"""

import numpy as np
import pytest

from explainer.music.monochord import key as K
from tests.music.partcheck import check_clips, check_ear_thread, check_scenes_and_clips, check_windows
from videos.music.music15 import compute
from videos.music.music15.manifest import SCENES
from videos.music.variations import LEDGER

load = compute.load


def test_the_profile_and_where_it_comes_from():
    h = load("hook")
    assert h["ratings"]["C"] == pytest.approx(6.35) and h["ratings"]["F♯"] == pytest.approx(2.52)
    p = load("profile")
    assert p["order"][:3] == [0, 7, 4] and p["order"][-1] == 1                       # the tonic, G, E on top; C sharp at the bottom
    g = p["group_means"]
    assert g["tonic"] > g["triad"] > g["scale"] > g["outside"]
    assert round(p["r"], 2) == 0.92 and p["quiz"]["answer"] == "B" and p["quiz"]["ratings"][1] == min(p["kk_major"])
    assert np.argsort(p["kk_minor"])[-3:].tolist() == [7, 3, 0]                      # in minor: tonic, then the minor third, then the fifth


def test_functions_and_cadences():
    f = load("functions")
    rows = {r["roman"]: r for r in f["rows"]}
    assert rows["I"]["leaning"] == [] and sorted(rows["V"]["leaning"] + rows["IV"]["leaning"]) == [2, 4, 6, 7]       # four and five hold every leaning note
    assert f["goes"]["7"]["to"] == 1 and f["goes"]["4"]["to"] == 3
    c = load("cadences")
    last = {k: v["names"][-2:] for k, v in c["cadences"].items()}
    assert last == {"authentic": ["V7", "I"], "half": ["IV", "V"], "plagal": ["IV", "I"], "deceptive": ["V7", "vi"]}
    assert c["quiz"]["order"][1] == "deceptive" and c["quiz"]["answer"] == "B"
    for name, v in c["cadences"].items():
        for a, b in zip(v["chords"], v["chords"][1:]):
            assert sum(abs(x - y) for x, y in zip(a[1:], b[1:])) <= 9               # the upper voices move little
    m = load("more")
    assert m["harmonize"]["members"]["1"] == ["I", "IV", "vi"] and all(len(v) == 3 for v in m["harmonize"]["members"].values())
    assert m["soprano"]["chords"]["perfect"][-1][-1] % 12 == 0 and m["soprano"]["chords"]["imperfect"][-1][-1] % 12 == 4


def test_the_key_finder():
    m = load("meter")
    assert m["rows"][-1]["top"][0]["key"] == "C major" and m["first_sure"] == 11
    peak = max(m["rows"], key=lambda r: r["f_major"])
    assert peak["notes"] == 9 and peak["f_major"] > 0.5                              # two long Fs, and the machine believes F major
    f = load("finder")
    acc = {k: v["accuracy"] for k, v in f["full"].items()}
    assert round(100 * acc["ratings"]) == 81 and round(100 * acc["counts"]) == 98 and round(100 * acc["last"]) == 91 and round(100 * acc["first"]) == 33
    assert f["dominant_errors"] == 72 and round(100 * f["five"]) == 91 and f["cases"] == 648 and round(100 * f["own"]) == 94
    assert f["curve"]["bayes"][f["ns"].index(4)] == pytest.approx(0.78, abs=0.01)
    mm = load("more")["mistakes"]
    assert mm["total"] == 120 and mm["dominant"] == 72 and mm["mediant"] == 36
    r = load("rare")
    rows = {x["notes"]: x["keys"] for x in r["rows"]}
    assert len(rows["C, G"]) == 6 and rows["C, D, E"] == ["C", "F", "G"] and rows["B, F"] == ["C", "F♯"] and rows["B, F, C"] == ["C"]
    assert [len(s["keys"]) for s in r["tune_steps"]] == [7, 6, 4, 3, 2, 2] and r["tune_keys_left"] == ["C", "F"]


def test_the_map_and_modulation():
    km = load("keymap")
    assert [n["key"] for n in km["near"][:5]] == ["A minor", "G major", "F major", "E minor", "C minor"] and km["far"]["key"] == "F♯ major"
    assert km["pairs"]["a"]["r"] == pytest.approx(0.65, abs=0.005) and km["pairs"]["Fs"]["r"] == pytest.approx(-0.68, abs=0.005) and km["shared"]["F♯ major"] == 2
    assert len(km["angles"]) == 24 and km["explained"] > 0.8
    mo = load("modulate")["reading"]
    assert mo["A"]["path"][0] == "C major" and "G major" in mo["A"]["path"] and mo["A"]["last"] == "C major"           # a visit
    assert mo["B"]["last"] == "G major" and mo["B"]["whole"] == "G major"                                             # a move
    piv = load("more")["pivots"]
    assert [p["shared"] for p in piv] == [7, 4, 2, 0, 0, 0, 0] and piv[1]["chords"] == ["Am", "C", "Em", "G"]
    mi = load("minor")
    assert mi["shared"] == {"parallel": 4, "relative": 7}
    odd = {o["name"]: o for o in mi["odd"]}
    assert not odd["Drunken Sailor"]["right"] and odd["Amazing Grace"]["right"] and odd["Amazing Grace"]["notes"] == 5
    md = load("more")["minor_dominant"]["chords"]
    assert 68 % 12 in {x % 12 for x in md["raised"][2]} and 68 % 12 not in {x % 12 for x in md["natural"][2]}          # the raised version has a G sharp
    col = load("more")["colour"]
    assert col["thirds"]["C"] == pytest.approx(390.2, abs=0.1) and col["thirds"]["F#"] == pytest.approx(407.8, abs=0.1)
    assert [b - a for a, b in zip(sum(col["chords"]["C"], []), sum(col["chords"]["Db"], []))] == [1] * 16              # the same cadence, a semitone higher


def test_variation_15():
    t = load("tune")
    assert len(t["phrases"]) == 14 and t["keys"][:3] == ["C major", "C major", "F major"] and t["keys"][-1] == "C major"
    assert [p["pc"] for p in t["phrases"][1:]] == [0, 5, 10, 3, 8, 1, 6, 11, 4, 9, 2, 7, 0]                            # down a fifth each time
    assert t["found_right"] == 14 and t["phrases"][-1]["roman"][-2:] == ["V7", "vi"]                                 # and a deceptive cadence
    for a, b in zip(t["phrases"][1:], t["phrases"][2:]):
        assert a["roman"][-1] == "V7/IV" and (a["pc"] + 5) % 12 == b["pc"]                                            # each home chord becomes the next key's dominant
    assert {p["signature"] for p in t["phrases"]} == set(range(-5, 7))
    v = load("variation")
    row = [r for r in LEDGER if r["part"] == 15][0]
    assert v["part"] == 15 and row["measure"] == v["measure"] and row["seconds"] == pytest.approx(v["seconds"], abs=0.05)


def test_the_part_keeps_the_series_rules():
    check_clips(compute)
    check_scenes_and_clips(compute, SCENES)
    check_windows(compute, SCENES)
    check_ear_thread(compute, SCENES)
