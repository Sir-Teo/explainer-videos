"""Part 59 of *Music, Built*: what the film says is what was computed, and every sound keeps the series' rules.

    python -m pytest -q tests/music/test_music59.py
"""

import pytest

from tests.music.partcheck import check_clips, check_ear_thread, check_scenes_and_clips, check_windows
from videos.music.music59 import compute
from videos.music.music59.manifest import SCENES
from videos.music.variations import LEDGER

load = compute.load


def test_feedback_and_ringout():
    f = load("feedback")
    assert f["answer"] == "second" and abs(f["found_hz"] - f["howl_hz"]) < 5
    assert f["tail_db"]["m6"] < f["tail_db"]["m2"] < f["tail_db"]["m05"]
    gains = [r["max_gain_db"] for r in f["ringout"]]
    assert gains[-1] > gains[0] + 2
    assert f["pag"]["pag"] < f["pag"]["nag"]


def test_arrays_subs_delay_air():
    a = load("arrays")
    pd = a["per_doubling"]["1000"]
    assert pd["point"] == pytest.approx(6.0, abs=0.1) and pd["line_near"] < 4.0 < pd["line_far"]
    assert -12 < a["levels"]["80"] < a["levels"]["40"] < 0
    s = load("subs")
    assert s["at63"]["back"] < -60 and s["at63"]["front"] > -3
    d = load("delay")
    assert d["answer"] == "first" and 180 < d["delay_ms"] < 190 and d["drift_ms"]["10"] > 0 > d["drift_ms"]["30"]
    lo = load("air")["loss100"]
    assert lo["1000"] < 1 < lo["4000"] < lo["8000"] < lo["16000"]


def test_measure_wireless_sti_dose():
    m = load("measure")
    assert m["delay_ms"] == pytest.approx(m["true_delay_ms"], abs=0.05)
    w = load("wireless")
    assert w["hits_plan"] == 0 and w["hits_even"] == len(w["even"]) and len(w["plan"]) >= 20
    s = load("sti")["conds"]
    assert s["good"]["sti"] > 0.6 > s["fair"]["sti"] > 0.3 > s["bad"]["sti"]
    rows = load("dose")["rows"]
    assert rows[0]["dose"] > 1000 and rows[2]["dose"] < 100


def test_variation_59():
    v = load("variation")
    row = [r for r in LEDGER if r["part"] == 59][0]
    assert v["part"] == 59 and row["measure"] == v["measure"] and row["seconds"] == pytest.approx(v["seconds"], abs=0.05)
    t = load("tune59")["levels_db"]
    assert t["carpark"] < t["back"] < 0


def test_the_part_keeps_the_series_rules():
    check_clips(compute)
    check_scenes_and_clips(compute, SCENES)
    check_windows(compute, SCENES)
    check_ear_thread(compute, SCENES)
