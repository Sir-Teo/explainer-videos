"""Part 18 of *Music, Built*: what the film says is what was computed, and every sound keeps the series' rules.

    python -m pytest -q tests/music/test_music18.py
"""

import pytest

from explainer.music.monochord import fourpart as F
from tests.music.partcheck import check_clips, check_ear_thread, check_scenes_and_clips, check_windows
from videos.music.music18 import compute
from videos.music.music18.manifest import SCENES
from videos.music.variations import LEDGER

load = compute.load


def test_functions_motion_and_bits():
    f = load("functions")["major"]
    assert (f["TS"], f["SD"], f["DT"], f["TD"], f["DS"]) == (1246, 788, 1412, 913, 290)
    m = load("motion")
    mj = m["major"]
    assert round(100 * mj["fifth down"] / sum(mj.values())) == 39
    fw = mj["fifth down"] + mj["third down"] + mj["step up"]
    bw = mj["fifth up"] + mj["third up"] + mj["step down"]
    assert round(100 * fw / (fw + bw)) == 69
    assert not any(F.parallels(a, b) for v in (m["A"], m["B"]) for a, b in zip(v, v[1:]))
    p = load("predict")
    assert p["test"] == 84 and round(p["major"]["n2"], 1) == 3.4 and round(p["major"]["n2_shuffled"], 1) == 4.9
    assert p["guesses"]["I IV"][0][0] == "I" and p["guesses"]["V"][0][0] == "I" and p["guesses"]["V"][0][1] > 0.5


def test_sequence_rhythm_and_the_rule():
    s = load("sequence")
    assert [ch[3] % 12 for ch in s["chords"]] == [0, 5, 11, 4, 9, 2, 7, 0]
    assert not any(F.parallels(a, b) for a, b in zip(s["chords"], s["chords"][1:]))
    ch = s["chains"]
    assert ch["major"]["3"] + ch["minor"]["3"] == 770
    r = load("rhythm")["change"]
    assert r[0] > r[1] and r[2] > r[3]
    o = load("octave")
    assert o["n"] == 804 and round(100 * o["within"]) == 49 and round(100 * o["agree"]) == 28
    assert not any(F.parallels(a, b) for v in (o["up"], o["down"]) for a, b in zip(v, v[1:]))


def test_schemata_grounds_and_census():
    s = load("schemata")
    assert len(s["order"]) == 8
    for name in s["order"]:
        chs = s["schemata"][name]["chords"]
        assert [c[0] for c in chs] == s["schemata"][name]["melody"] and [c[3] for c in chs] == s["schemata"][name]["bass"]
        assert not any(F.parallels(a, b) for a, b in zip(chs, chs[1:]))
    assert not any(F.parallels(a, b) for a, b in zip(s["phrase"], s["phrase"][1:]))
    c = load("census")
    assert sum(c["chorales"]["real"].values()) == 13 and sum(c["chorales"]["shuffled"].values()) == 2
    assert c["melodies"]["6-5-4-3"]["real"] == 11 and c["melodies"]["4-3-2-1"]["real"] == 23 and c["tunes_major"] == 51
    g = load("grounds")
    assert g["order"] == ["lament", "folia", "romanesca", "passamezzo"] and g["grounds"]["romanesca"]["mode"] == "major"


def test_variation_18():
    t = load("tune")
    for name, v in t["versions"].items():
        assert v["parallels"] == []
        mel = v["melody"]
        for k, ch in enumerate(v["chords"]):
            here = [p for p, a, d in mel if 2 * k <= a < 2 * k + 2]
            assert ch[0] == here[0]                                                   # the Tune's note on top of every chord
    v = load("variation")
    row = [r for r in LEDGER if r["part"] == 18][0]
    assert v["part"] == 18 and row["measure"] == v["measure"] and row["seconds"] == pytest.approx(v["seconds"], abs=0.05)


def test_the_part_keeps_the_series_rules():
    check_clips(compute)
    check_scenes_and_clips(compute, SCENES)
    check_windows(compute, SCENES)
    check_ear_thread(compute, SCENES)
