"""Part 68 of *Music, Built*: what the film says is what was computed, and every sound keeps the series' rules.

    python -m pytest -q tests/music/test_music68.py
"""

import numpy as np
import pytest

from tests.music.partcheck import check_clips, check_ear_thread, check_scenes_and_clips, check_windows
from videos.music.music68 import compute
from videos.music.music68.manifest import SCENES
from videos.music.variations import LEDGER

load = compute.load


def test_the_settings_were_chosen_without_the_tune():
    c = load("calibrate")
    assert "Ah! vous dirai-je" not in " ".join(c["tunes"]) and len(c["tunes"]) == 4
    assert c["settings"]["method"] == "onset" and c["mean"][c["best"]] < c["mean"][c["best_yin"]]
    assert load("roundtrip")["settings"] == c["settings"]


def test_down_the_chain():
    d = load("chain")
    assert d["crest_after"] < d["crest_before"] - 3
    assert d["codec"]["128"]["nmr_db"] < 0 < d["codec"]["32"]["nmr_db"]          # under the mask at 128, over it at 32
    assert all(abs(d["codec"][str(k)]["kbps"] - k) / k < 0.1 for k in compute.BITRATES)
    w = load("wide")
    assert w["wide"][1] < w["cut"][1] - 30                                        # the fallback band starves the melody's band


def test_back_up_the_chain():
    r = load("roundtrip")["rows"]
    assert r["score"]["moves_found"] == 24                                       # every change of key comes back as written
    assert all(r[k]["restrikes_found"] < r[k]["restrikes"] for k in r)          # repeats are the weak spot at every stage
    assert r["master"]["pitch_errors"] - r["mic"]["pitch_errors"] >= 3          # most of the loss arrives at the master ...
    assert max(abs(r[k]["pitch_errors"] - r["master"]["pitch_errors"]) for k in ("codec128", "codec64", "codec32", "codec16")) <= 2
    assert r["played"]["key"] == "G major" and r["played"]["key_by_count"] == "C major"   # the rhythm misleads the key finder
    assert load("wide")["wide_pitch_errors"] > 2 * r["codec16"]["pitch_errors"]
    b = load("back")
    assert sorted(b["order"]) == ["codec16", "codec32", "master"]


def test_what_survives_and_the_order():
    s = load("survive")["rows"]
    assert s["room"]["filled"] > 2 * s["played"]["filled"] > 2 * s["codec16"]["filled"]   # filled by the room, emptied by the coder
    i = load("identify")["rows"]
    assert i["played"]["votes"] > 10 * i["played"]["runner_up"] and i["master"]["votes"] < 2 * i["master"]["runner_up"]
    o = load("order")
    assert o["nearest"] < o["built"] < o["random_lo"] and o["built_below_random"] < 0.05
    assert sorted(o["nearest_order"]) == list(range(1, 68))


def test_the_suite_and_variation_68():
    s = load("suite")
    parts = [p for m in ("one", "two", "three") for p in s["moves"][m]["parts"]]
    assert parts == list(range(1, 68))
    total = sum(m["seconds"] for m in s["moves"].values())
    assert 9 * 60 < total < 12 * 60                                               # the plan: ten to twelve minutes
    v = load("variation")
    row = [r for r in LEDGER if r["part"] == 68][0]
    assert v["part"] == 68 and row["measure"] == v["measure"] and row["seconds"] == pytest.approx(v["seconds"], abs=0.05)
    b = load("built")
    assert b["labs"] == 68 and b["tests"] > 800 and b["modules"] > 90


def test_the_part_keeps_the_series_rules():
    check_clips(compute)
    check_scenes_and_clips(compute, SCENES)
    check_windows(compute, SCENES)
    check_ear_thread(compute, SCENES)
