"""Part 55 of *Music, Built*: what the film says is what was computed, and every sound keeps the series' rules.

    python -m pytest -q tests/music/test_music55.py
"""

import pytest

from tests.music.partcheck import check_clips, check_ear_thread, check_scenes_and_clips, check_windows
from videos.music.music55 import compute
from videos.music.music55.manifest import SCENES
from videos.music.variations import LEDGER

load = compute.load


def test_reverberation_claims():
    h = load("hook")
    assert h["answer"] == "first" and h["T"][0] == pytest.approx(5.6) and h["T"][1] < 1.2
    c = load("cushions")
    assert c["Ts"][0] > c["Ts"][1] > c["Ts"][2] and all(a > b for a, b in zip(c["T"], c["T"][1:]))
    k = load("check")
    for r in k["rt"]:
        assert r["eyring"] < r["sabine"]
        assert r["image"] == pytest.approx(r["sabine"], rel=0.17)
    assert k["worst_hz"] < 0.5


def test_mode_claims():
    m = load("modes")
    assert len(m["modes"]) == m["counts"][-1] == 18 and m["weyl"][-1] == pytest.approx(20.2, abs=0.1)
    assert m["fs_room"] > 250 and m["fs_hall"] < 25
    assert load("images")["counts"]["8"] == 833


def test_diffusion_and_hall_claims():
    d = load("diffuser")
    assert d["residues"] == [0, 1, 4, 2, 2, 4, 1]
    for f in ("1000", "2000"):
        assert d["coef"][f]["qrd"] > 3 * d["coef"][f]["flat"]
    assert load("flutter")["gap_ms"] == pytest.approx(1000 * 12 / 343, abs=0.01)
    h = load("halls")
    assert h["lf_pair"]["narrow"] > 0.15 > h["lf_pair"]["wide"] and h["lf"][0] > h["lf"][-1]


def test_head_and_panning_claims():
    c = load("cues")
    assert c["itd_max_us"] == pytest.approx(656, abs=1) and c["fc_head"] == pytest.approx(624, abs=1)
    cone = load("cone")
    assert cone["answer"] == "neither" and cone["max_diff"] < 1e-9 and cone["itd_30_us"] == pytest.approx(cone["itd_150_us"])
    p = load("pan")
    assert min(p["lin_power_db"]) == pytest.approx(-3.01, abs=0.01) and max(abs(v) for v in p["pw_power_db"]) < 1e-9
    assert p["phantom"][1] == pytest.approx(13.45, abs=0.01)
    a = load("ambi")
    assert a["res"]["basic"]["rE"][0] == pytest.approx(2 / 3) and a["res"]["maxre"]["rE"][0] == pytest.approx(0.7071, abs=1e-4)


def test_variation_55():
    v = load("variation")
    row = [r for r in LEDGER if r["part"] == 55][0]
    assert v["part"] == 55 and row["measure"] == v["measure"] and row["seconds"] == pytest.approx(v["seconds"], abs=0.05)


def test_the_part_keeps_the_series_rules():
    check_clips(compute)
    check_scenes_and_clips(compute, SCENES)
    check_windows(compute, SCENES)
    check_ear_thread(compute, SCENES)
