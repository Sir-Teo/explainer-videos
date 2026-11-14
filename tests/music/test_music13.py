"""Part 13 of *Music, Built*: what the film says is what was computed, and every sound keeps the series' rules.

    python -m pytest -q tests/music/test_music13.py
"""

import numpy as np
import pytest

from explainer.music.monochord import chords as C
from tests.music.partcheck import check_clips, check_ear_thread, check_scenes_and_clips, check_windows
from videos.music.music13 import compute
from videos.music.music13.manifest import SCENES
from videos.music.variations import LEDGER

load = compute.load


def test_intervals_and_the_line_of_fifths():
    i = load("intervals")
    assert [r["short"] for r in i["rows"]] == ["P1", "m2", "M2", "m3", "M3", "P4", "A4", "P5", "m6", "M6", "m7", "M7", "P8"]
    for r in i["rows"][:-1]:
        assert r["number"] + int(r["inverse"][1:]) == 9
    assert [e["short"] for e in i["line"]] == ["d5", "m2", "m6", "m3", "m7", "P4", "P1", "P5", "M2", "M6", "M3", "M7", "A4"]
    assert [e["label"] for e in i["line"]][0] == "G♭" and [e["label"] for e in i["line"]][-1] == "F♯"
    # in quarter-comma meantone the two tritones are a diesis apart, and near 7:5 and 10:7
    assert i["dim5"] - i["aug4"] == pytest.approx(41.06, abs=0.01)
    assert abs(i["aug4"] - i["septimal"][0]) < 4 and abs(i["dim5"] - i["septimal"][1]) < 4


def test_triads_are_what_is_left():
    t = load("triads")
    assert [k["thirds"] for k in t["kinds"]] == [[4, 3], [3, 4], [3, 3], [4, 4]]
    assert [k["fundamental"] for k in t["kinds"]][:2] == [[1, 4], [1, 10]]                  # 4:5:6 and 10:12:15
    assert t["count"] == 19 and t["no_step"] == 4
    assert sorted(s["name"] for s in t["shapes"] if not s["step"]) == ["augmented triad", "diminished triad", "major triad", "minor triad"]
    assert sorted(s["name"] for s in t["clean"]) == ["augmented triad", "major triad", "minor triad"]
    s = load("scale")
    assert s["counts"] == {"major": 3, "minor": 3, "diminished": 1} and s["covered"] == list("ABCDEFG")
    assert [r["roman"] for r in s["rows"]] == ["I", "ii", "iii", "IV", "V", "vi", "vii°"]


def test_inversion_and_roots():
    v = load("inversion")
    assert [p["figure"] for p in v["positions"]] == ["5/3", "6", "6/4"] and [p["figures"] for p in v["positions"]] == [[5, 3], [6, 3], [6, 4]]
    assert v["puzzle"]["stack"] == ["G", "B", "D", "F"] and v["puzzle"]["figure"] == "4/2" and v["puzzle"]["root"] == "G"
    r = {x["label"]: x for x in load("roots")["table"]}
    assert r["C major"]["saliences"][0] == 18 and r["C minor"]["saliences"][0] == 15 and r["C minor"]["saliences"][3] == 13
    assert sorted(r["B diminished"]["tied"]) == ["B", "D", "F", "G"]                        # G is not in the chord
    assert len(r["C augmented"]["tied"]) == 3 and len(r["diminished seventh"]["tied"]) == 8
    assert r["A minor seventh"]["root_name"] == "C" and r["A minor seventh"]["second"] == "A" and r["C suspended"]["root_name"] == "F"
    assert r["C major"]["ambiguity"] < r["C minor"]["ambiguity"] < r["C augmented"]["ambiguity"] < r["B diminished"]["ambiguity"]
    ear = {e["kind"]: e for e in load("roots")["ear"]}
    assert ear["major"]["name"] == "C2" and ear["minor"]["name"] == "C3"                    # two octaves and one octave below middle C
    assert ear["major"]["strength"] > ear["minor"]["strength"] > max(ear["diminished"]["strength"], ear["augmented"]["strength"])


def test_sevenths():
    s = load("sevenths")
    assert [k["symbol"] for k in s["kinds"]] == ["Cmaj7", "C7", "Cm7", "Cm7♭5", "Cdim7"]
    assert [c["roman"] for c in s["scale"]] == ["Imaj7", "ii7", "iii7", "IVmaj7", "V7", "vi7", "viiø7"]
    assert [c["kind"] for c in s["scale"]].count("7") == 1
    assert s["cents"]["harmonic"] == pytest.approx(968.8, abs=0.1) and s["roughness"]["just"] < s["roughness"]["equal"]
    assert s["tall"]["letters"] == list("ABCDEFG") and [f["figure"] for f in s["inversions"]] == ["7", "6/5", "4/3", "4/2"]


def test_voicing_and_what_can_be_left_out():
    v = load("voicing")
    r = v["third_roughness"]
    assert all(b > a for a, b in zip(r, r[1:])) and 10 < r[-1] / r[0] < 12.5                # about eleven times rougher at the bottom
    b = v["third_bands"]
    assert b[0] > 1.4 and b[1] > 1 > b[2] and b[4] < 0.35                                   # the third falls inside one critical band below middle C
    lim = v["limits"]
    assert lim["3"] > lim["4"] > lim["7"] > lim["12"] and lim["4"] == 48
    assert v["count"] == 41 and v["worst"] == [36, 40, 43, 48] and v["best"][1] - v["best"][0] == 19
    assert 4.5 < v["worst_roughness"] / v["best_roughness"] < 5.6
    d = load("doubling")
    amb = {x["label"]: x["ambiguity"] for x in d["rows"]}
    assert amb["root doubled"] < amb["one of each"] < amb["fifth doubled"] < amb["third doubled"]
    assert -9 < d["partials_db"][2] < -6                                                    # the fifth is already in the root's sound
    p = d["power"]
    assert 1.8 < p["third"]["driven"] / p["fifth"]["driven"] < 2.3 and p["triad"]["driven"] > p["third"]["driven"]
    assert all(p[k]["driven"] > p[k]["clean"] for k in p)


def test_symbols_and_the_map():
    s = load("symbols")
    assert s["keys"]["C"]["symbols"] == ["C", "C/E", "F", "G7", "C"] and s["keys"]["Eb"]["symbols"] == ["E♭", "E♭/G", "A♭", "B♭7", "E♭"]
    assert s["roman"] == ["I", "I6", "IV", "V7", "I"] and [x["symbol"] for x in s["two"]] == ["Am7/C", "C6"]
    t = load("tonnetz")
    assert {k: (m["to"], m["cost"], len(m["kept"])) for k, m in t["moves"].items()} == {"P": ("Cm", 1, 2), "L": ("Em", 1, 2), "R": ("Am", 2, 2)}
    assert [x[2] for x in t["cycles"]["PL"]] == ["C", "Cm", "A♭", "A♭m", "E", "Em"] and len(t["cycles"]["PR"]) == 8 and len(t["cycles"]["LR"]) == 24
    assert t["lr_motion"] == 36 and t["commas"]["diesis"] == pytest.approx(41.06, abs=0.01)
    for a, b in zip(t["hexa_voicings"], t["hexa_voicings"][1:]):
        assert C.motion(a, b) == 1                                                          # one voice, one semitone, every time
    assert t["hexa_voicings"][0] == t["hexa_voicings"][-1]


def test_the_frontier():
    f = load("frontier")
    assert f["listeners"] == ["major", "minor", "diminished", "augmented"]
    assert f["by_roughness"] == f["by_fusion"] == ["major", "minor", "augmented", "diminished"]      # both models misplace the augmented triad
    assert all(row["4"] == 24 for row in f["accuracy"].values())
    assert f["variation_right"] == 19 and f["variation_of"] == 24
    wrong = [r for v in f["variation"] for r in v["rows"] if not r["ok"]]
    assert sum(r["heard"] == "Am" and r["want"] == "C" for r in wrong) == len(wrong) - 1
    assert np.argsort(f["chroma"])[-3:].tolist().__len__() == 3 and set(np.argsort(f["chroma"])[-3:].tolist()) == {0, 4, 7}


def test_variation_13():
    t = load("tune")
    assert len(t["phrases"]) == 6 and t["chords"] == 24 and t["block_motion"] == 372 and t["voiced_motion"] == 60
    assert [c["midis"] for c in t["phrases"][0]["chords"]] == [[60, 64, 67], [60, 64, 67], [53, 57, 60], [60, 64, 67]]
    for a, b in zip(t["phrases"][1]["chords"], t["phrases"][1]["chords"][1:]):
        assert C.motion(a["midis"], b["midis"]) == 3
    shells = [c["midis"][1:] for c in t["phrases"][3]["chords"]]
    assert shells == [[64, 71], [64, 69], [64, 71], [65, 71]]                               # third and seventh, moving by step
    for ph in t["phrases"]:
        for c in ph["chords"]:
            pcs = {m % 12 for m in c["midis"]}
            root = {1: 0, 4: 5, 5: 7}[c["degree"]]
            assert root in pcs and (root + 4) % 12 in pcs                                   # every chord keeps its root and its third
    v = load("variation")
    assert v["part"] == 13 and "60 semitones" in v["measure"] and "372" in v["measure"]
    row = [r for r in LEDGER if r["part"] == 13][0]
    assert row["measure"] == v["measure"] and row["seconds"] == pytest.approx(v["seconds"], abs=0.05)


def test_the_part_keeps_the_series_rules():
    check_clips(compute)
    check_scenes_and_clips(compute, SCENES)
    check_windows(compute, SCENES)
    check_ear_thread(compute, SCENES)
