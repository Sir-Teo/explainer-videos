"""Part 16 of *Music, Built*: what the film says is what was computed, and every sound keeps the series' rules.

    python -m pytest -q tests/music/test_music16.py
"""

import pytest

from explainer.music.monochord import counterpoint as K
from tests.music.partcheck import check_clips, check_ear_thread, check_scenes_and_clips, check_windows
from videos.music.music16 import compute
from videos.music.music16.manifest import SCENES
from videos.music.variations import LEDGER

load = compute.load


def test_organum_and_the_hook():
    h = load("hook")
    assert [a - b for a, b in zip(h["tune"], h["organum"])] == [7] * len(h["tune"])               # a fifth below, all the way
    assert h["independence"]["organum"]["fused"] == 1.0 and h["independence"]["organum"]["parallel"] == 1.0
    assert h["independence"]["counterpoint"]["fused"] == 0.0 and h["independence"]["counterpoint"]["contrary"] > 0.5
    assert h["violations"] == []                                                                  # the hook's counterpoint obeys every rule
    o = load("organum")
    assert [r[0] - r[1] for r in zip(*o["composite"][:2])] == [12] * 7                            # composite organum: octave doublings


def test_fusion_motion_and_onsets():
    f = load("fusion")
    s = dict(zip(f["names"], f["strength"]))
    assert s["octave"] == 1.0 and s["P5"] == 0.5 and s["P4"] == pytest.approx(1 / 3) and s["M3"] == 0.25
    assert max(v for k, v in s.items() if k not in ("unison", "octave", "P5")) < 0.5             # nothing else fuses like the fifth
    assert f["quiz"]["answer"] == "B"
    m = load("motions")
    assert m["best"]["contrary"] == pytest.approx(0.9) and m["valid"]["oblique"] == 0.0             # first species has no oblique motion
    assert m["valid"]["contrary"] > m["consonant_only"]["contrary"]                                 # the rules favour contrary motion
    on = load("onsets")
    assert on["delay_ms"] == 35 and on["together_by_species"]["1"] == 1.0 and on["together_by_species"]["4"] == pytest.approx(0.05)


def test_fux_and_the_count():
    f = load("fux")
    assert f["cf"] == K.FUX_DORIAN and K.check(f["cf"], f["best"]) == []
    assert f["motions"].count("contrary") == 9 and f["best"][-2] % 12 == 1 and f["verticals"][0] == f["verticals"][-1] == 12   # C sharp, octave to octave
    assert len(f["rules"]) == 12
    c = load("counting")
    funnel = dict(c["funnel"])
    assert c["total"] == 4_628_074_479_616 and c["valid"] == 152 == K.count(K.FUX_DORIAN)
    assert funnel["direct"] == funnel["parallel"] == funnel["run"] == 234                          # after direct motion, parallels and runs add nothing
    assert c["tune_count"] == 23_921_887_999 and c["tune_digits"] == 50


def test_removing_a_rule():
    d = load("damage")
    rows = {r["rule"]: r for r in d["rows"]}
    assert d["full"] == 152 and rows["parallel"]["count"] == 152 and rows["direct"]["count"] == 410
    assert rows["consonance"]["count"] == 28_038 and rows["consonance"]["dissonant"] > 0.3
    assert rows["direct"]["fused"] > 0.05 and d["base"]["fused"] == 0.0
    assert rows["unison"]["unison"] > 0 and rows["melodic"]["big"] > 3 * d["base"]["big"]
    assert len(d["direct_at"]) >= 1 and len(d["dissonant_at"]) >= 3


def test_the_species():
    s = load("species")
    cf = K.FUX_DORIAN
    for n in ("2", "3"):
        ev = s[n]["events"]
        for i, (p, a, _) in enumerate(ev):                                                         # dissonances off the beat, by step
            bar = int(a // 4)
            if bar < len(cf) and (p - cf[bar]) % 12 not in K.CONSONANT:
                assert a % 4 != 0 and abs(p - ev[i - 1][0]) <= 2 and abs(ev[i + 1][0] - p) <= 2
        assert len(s[n]["dissonances"]) >= 4
    assert s["2"]["notes"] == 21 and s["3"]["notes"] == 41
    for p, a, d, iv in s["4"]["suspensions"]:
        assert iv in (10, 11, 5, 2)                                                                 # sevenths, fourths, seconds held over
    assert len(s["4"]["suspensions"]) >= 2 and len(s["5"]["suspensions"]) >= 1
    rows = {r["name"]: r for r in load("independence")["rows"]}
    together = [rows[k]["together"] for k in ("first species", "second species", "third species", "fourth species")]
    assert together == sorted(together, reverse=True) and rows["organum"]["fused"] == 1.0
    assert all(rows[k]["fused"] == 0.0 for k in rows if k != "organum")


def test_variation_16():
    t = load("tune")
    st = {x["name"]: x for x in t["stats"]}
    assert st["organum, a fifth below"]["together"] == 1.0 and st["fourth species"]["together"] == 0.0
    assert len(t["phrase_starts"]) == 6 and t["clip"]["seconds"] == pytest.approx(52.2, abs=0.05)
    v = load("variation")
    row = [r for r in LEDGER if r["part"] == 16][0]
    assert v["part"] == 16 and row["measure"] == v["measure"] and row["seconds"] == pytest.approx(v["seconds"], abs=0.05)


def test_the_added_passages():
    m = load("more")
    st = m["stages"]
    ind = st["independence"]
    assert ind["parallel"]["fused"] == 1.0 and ind["free"]["fused"] == 0.0 and ind["free"]["contrary"] > 0.6
    assert 0 < ind["oblique"]["fused"] < 1 and ind["oblique"]["contrary"] == 0.0
    assert min(st["voices"]["oblique"]) == 60 and st["voices"]["oblique"][-1] == st["tune"][-1]               # a floor at C; a unison at the end
    assert all((p - o) in (0, 5, 7, 12) for p, o in zip(st["tune"], st["voices"]["free"]))
    t = m["toy"]
    assert t["total"] == 14 == len(t["lines"]) and sorted(w for _, _, w in t["cells"][0]) == [4, 4, 6]
    assert t["pick"] in t["lines"] and all(abs(sum(q for _, q in row) - 1) < 1e-9 for row in t["probs"])
    b = m["below"]
    assert b["count"] == 42 and b["above"] == 152 and b["start_rule"]["fifth"] == 302 and b["violations"] == []
    assert b["verticals"][0] == 12 and b["verticals"][-1] == 0 and b["line"][-2] % 12 == 1
    assert m["ladder"]["delays"] == [0, 10, 20, 35, 60]
    su = m["suspension"]
    assert [e[0] for e in su["A"]] == [e[0] for e in su["B"]] and [s[2] for s in su["suspensions"]] == [11, 10, 10]


def test_the_part_keeps_the_series_rules():
    check_clips(compute)
    check_scenes_and_clips(compute, SCENES)
    check_windows(compute, SCENES)
    check_ear_thread(compute, SCENES)
