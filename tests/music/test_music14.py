"""Part 14 of *Music, Built*: what the film says is what was computed, and every sound keeps the series' rules.

    python -m pytest -q tests/music/test_music14.py
"""

import numpy as np
import pytest

from explainer.music.monochord import melody as M
from tests.music.partcheck import check_clips, check_ear_thread, check_scenes_and_clips, check_windows
from videos.music.music14 import compute
from videos.music.music14.manifest import SCENES
from videos.music.variations import LEDGER

load = compute.load


def test_the_hook_and_the_disguises():
    h = load("hook")
    assert h["tunes"] == 54 and 1850 < h["notes"] < 1950 and h["leaps"] == 446
    assert round(100 * h["real"]) == 63 and round(100 * h["chance"]) == 79          # shuffled notes turn back more often than tunes do
    assert sorted(h["shuffled"]["pitches"]) == sorted(h["tune"]["pitches"])
    c = load("contour")
    o = c["original"]["pitches"]
    assert [p % 12 for p in c["scrambled"]] == [p % 12 for p in o]                  # A: every note has the right name
    assert c["same_contour"] and c["stretched"] != o and c["scrambled_kept"] < 9    # B keeps the shape; A does not
    assert all(b - a == 2 * (y - x) for a, b, x, y in zip(c["stretched"], c["stretched"][1:], o, o[1:]))
    m = load("more")
    assert m["parsons"]["contour"][m["parsons"]["n"].index(8)] == 54 and m["parsons"]["contour"][m["parsons"]["n"].index(5)] == 40
    assert m["parsons"]["tune_code"] == "RURURDDRDRDRD"


def test_steps_range_and_the_arch():
    s = load("steps")
    sh = s["shares"]
    assert round(100 * sh["step"]) == 50 and round(100 * sh["repeat"]) == 25 and round(100 * sh["leap"]) == 25 and round(sh["mean_size"], 1) == 2.0
    assert s["most_common"] == -2 and s["down"]["whole_tone"] > s["up"]["whole_tone"] and s["up"]["fourth"] > s["down"]["fourth"]
    assert s["urn_mean"] > 2.5 * s["walk_mean"] and all(p % 12 in M.MAJOR for p in s["urn"] + s["walk"])
    r = load("range")
    assert r["median"] == 12 and r["within_octave"] == 42 and r["of"] == 54 and r["narrowest"][1] == "Hot Cross Buns" and r["widest"][0] == 17
    assert np.argmax(r["around"]) == 9 and 0.55 < r["near"] < 0.65 and 10 <= 1 / r["top_share"] <= 12
    a = load("arch")
    assert a["phrases"] == 275 and list(a["shapes"])[:4] == ["falling", "arch", "rising", "valley"]
    assert a["peak_at"] in (2, 3, 4) and -0.7 < a["end_minus_start"] < -0.3
    p = load("more")["peak"]
    assert p["median"] == pytest.approx(0.25, abs=0.03) and p["second_half"] == 17 and p["fifths"][0] > p["fifths"][4]


def test_the_leap_rule_is_regression_to_the_mean():
    k = load("leaps")["kinds"]
    assert k["all"]["real"] < k["all"]["shuffled"] - 5 * k["all"]["shuffled_sd"]
    assert k["departing"]["real"] > 0.7 and k["approaching"]["real"] < 0.25 and abs(k["approaching"]["real"] - k["approaching"]["shuffled"]) < 0.06
    assert k["departing"]["shuffled"] > 0.9 and k["all"]["urn"] > 0.7
    d = load("more")["dice"]
    assert (d["cases"], d["fall"], d["rise"], d["same"]) == (60, 40, 10, 10) and d["share"] == pytest.approx(0.8) and d["mean_landing"] == pytest.approx(5.0)


def test_what_chance_does_not_explain():
    t = load("tendency")
    assert {k: v["to"] for k, v in t["goes"].items() if k in "2467"} == {"2": 1, "4": 3, "6": 5, "7": 1}
    assert t["goes"]["6"]["p"] > 0.5 and 0.6 < t["triad"] < 0.72
    g = t["gap_fill"]
    assert g["real"] > 1.5 * g["walks"] and g["walks"] > 2 * g["notes_shuffled"]              # partly arithmetic, but not only
    i = load("more")["inertia"]
    assert i["real"]["down"] > i["chance"]["down"] + 0.1 and i["real"]["up"] > i["chance"]["up"] + 0.05 and i["real"]["down"] > i["real"]["up"]
    assert i["leaps_on_triad"] > 0.7 > 0.55 > i["steps_on_triad"]
    m = load("motive")
    assert m["phrases_repeated"] == 60 and m["phrases"] == 275 and m["moved"] == 13 and m["kuckuck_seq"]["shift"] == 1
    f = load("more")["form"]
    assert f[M.THE_TUNE] == "ABCCAB" and f["Frère Jacques"] == "AABBCCDD" and f["Au clair de la lune"] == "ABABCDAB"
    p = load("phrase")
    assert p["common"][0] == 8 and 2.0 < p["lengthening"] < 2.4 and p["final_end"]["1"] > 0.95 and max(p["mid_end"], key=p["mid_end"].get) == "5"


def test_information_and_the_model():
    i = load("info")
    assert i["alphabet"] == 20 and i["uniform"] == pytest.approx(4.32, abs=0.01) and i["best_order"] == 1
    assert [round(x, 1) for x in i["by_order"][:3]] == [3.2, 2.6, 2.6] and -1.5 < i["zipf"]["slope"] < -1.1
    g = load("more")["guess"]
    assert round(100 * g["first"]) == 33 and round(100 * g["three"]) == 77 and g["chance_first"] == pytest.approx(0.05)
    m = load("model")
    assert m["peak_at"] == 2 and m["peak"] > 5 and m["after"]["C, C"][0]["note"] == "C" and m["after"]["C, C, G, G, A, A"][0]["note"] == "G"
    assert m["gen_surprise"]["0"] > m["gen_surprise"]["2"]
    e = load("more")["extremes"]
    assert e["easy"]["name"] == "Ode to Joy" and e["hard"]["name"] == "Korobeiniki" and e["hard"]["bits"] > 2.5 * e["easy"]["bits"] and e["tune_rank"] == 17
    f = load("frontier")
    assert f["ngram"] < f["unigram"] - 0.5 and abs(f["proximity"] - f["unigram"]) < 0.1


def test_variation_14():
    t = load("tune")
    assert len(t["phrases"]) == 8 and t["phrases"][0]["pitches"] == [0, 0, 7, 7, 9, 9, 7]
    assert t["phrases"][4]["pitches"] == [12, 12, 5, 5, 4, 4, 5] and t["phrases"][5]["pitches"] == [7, 9, 9, 7, 7, 0, 0]
    for ph in t["phrases"][:4]:
        assert sum(ph["beats"]) == pytest.approx(8.0) and all(p % 12 in M.MAJOR for p in ph["pitches"])
    assert t["bits_most"] < t["bits_plain"] < t["bits_least"] and t["most"] == [5, 4, 2, 0, 2, 4, 5]
    v = load("variation")
    row = [r for r in LEDGER if r["part"] == 14][0]
    assert v["part"] == 14 and row["measure"] == v["measure"] and row["seconds"] == pytest.approx(v["seconds"], abs=0.05)


def test_the_part_keeps_the_series_rules():
    check_clips(compute)
    check_scenes_and_clips(compute, SCENES)
    check_windows(compute, SCENES)
    check_ear_thread(compute, SCENES)
