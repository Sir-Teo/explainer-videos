"""Part 9 of *Music, Built*: what the film says is what was computed, and every sound keeps the series' rules.

    python -m pytest -q tests/music/test_music9.py
"""

import math

import numpy as np
import pytest

from tests.music.partcheck import check_clips, check_ear_thread, check_scenes_and_clips, check_windows
from videos.music.music9 import compute
from videos.music.music9.manifest import SCENES

load = compute.load


def cents(a, b):
    return 1200 * math.log2(a / b)


def test_a_skin():
    h = load("hook")
    assert [round(r, 2) for r in h["drum"][:5]] == [1.0, 1.59, 2.14, 2.3, 2.65]
    s = load("skin")
    assert s["zeros"]["j11"] / s["zeros"]["j01"] == pytest.approx(1.5933, abs=1e-4)
    assert cents(s["modes"][1]["ratio"], 1.0) == pytest.approx(806, abs=1) and abs(s["minor_sixth_cents"]) < 10
    centre, off = np.asarray(s["centre"]), np.asarray(s["off"])
    m = [r["m"] for r in s["modes"]]
    assert all((c > 0.3) == (k == 0) for c, k in zip(centre[:8], m[:8]))             # a blow at the centre: only the circles
    assert (off[:6] > 0.1).all() and s["quiz_answer"] == "B"


def test_two_ways_to_give_a_skin_a_note():
    t = load("timpani")
    plain, est, meas = t["plain"], t["estimate"], t["measured"]
    assert [round(v, 2) for v in plain] == [1.0, 1.34, 1.67, 1.98, 2.29]
    assert all(p < e < m_ + 0.3 for p, e, m_ in zip(plain[1:], est[1:], meas[1:]))                # the air moves every mode the right way
    assert max(abs(c) for c in t["off_measured"]) < 60 < min(abs(c) for c in t["off_plain"][1:])
    assert t["kettle_salience"] > t["bare_salience"] + 0.2
    assert abs(cents(t["kettle_pitch"], t["hz"] / 2)) < 30                                        # the model hears the octave below
    b = load("tabla")
    ratios = [r["ratio"] for r in b["rows"]]
    assert b["loaded_misfit"] < 70 and b["bare_misfit"] > 500
    assert abs(ratios[1] - 2) < 0.08 and abs(ratios[2] - 3) < 0.08 and abs(ratios[3] - 3) < 0.08 and abs(ratios[4] - 4) < 0.08
    miss = np.asarray(b["misfit"])
    assert miss[0] > 500 and miss[-1] < 60 and (np.diff(miss) <= 1e-9).all()                      # heavier is better, with less and less gained


def test_bars_and_bells():
    a = load("bars")
    assert list(np.round(a["uniform"][:3], 2)) == [1.0, 2.76, 5.4]
    m, x = a["marimba"], a["xylophone"]
    assert m["ratios"][1] == pytest.approx(4.0, abs=1e-3) and m["ratios"][2] == pytest.approx(10.0, abs=0.1)
    assert x["ratios"][1] == pytest.approx(3.0, abs=1e-3) and abs(x["ratios"][2] - 6) < 0.2 and x["depth"] < m["depth"]
    assert m["octaves_down"] == pytest.approx(1.62, abs=0.02) and abs(a["two_octave_error"]) < 0.1
    assert np.asarray(a["profile_marimba"]).min() == pytest.approx(1 - m["depth"], abs=0.01)
    e = load("bells")
    names = [q["name"] for q in e["partials"]]
    assert names[:5] == ["hum", "prime", "tierce", "quint", "nominal"]
    assert abs(e["upper_cents"]) < 5                                                              # 2 : 3 : 4 gives the prime
    assert e["tierce_cents"] == pytest.approx(315.6, abs=0.1) and e["major_cents"] == pytest.approx(386.3, abs=0.1) and e["quiz_answer"] == "B"


def test_plates_gongs_and_pans():
    p = load("plates")
    assert len(p["figs"]) == 8 and [f["pitch"] for f in p["figs"]] == sorted(f["pitch"] for f in p["figs"])
    g = load("gongs")
    assert g["down"][0] > g["down"][-1] and g["up"][0] < g["up"][-1]                              # one falls, one rises
    assert g["down_cents"] == pytest.approx(196, abs=1) and g["cymbal_modes"] == 420
    assert load("pan")["partials"] == [1, 2, 3, 4]


def test_two_drums_one_spectrum():
    s = load("shape")
    assert s["area"] == 3.5 and s["largest_gap"] < 1e-9
    assert np.allclose(s["ours"], s["driscoll"], rtol=2e-3)
    assert not np.allclose(s["ratios"][:6], s["square_ratios"][:6], atol=0.05) and s["quiz_answer"] == "B"
    counted, weyl = np.asarray(s["counted"]), np.asarray(s["weyl"])
    assert np.abs(counted - weyl)[50:].max() < 6                                                  # Weyl's law, from area and rim alone
    assert np.abs(np.asarray(s["a0"])).max() > 0.9 and not np.allclose(s["a0"], s["b0"])          # the modes differ; the notes do not


def test_variation_9():
    t = load("tune")
    assert t["plan"][0] == ["marimba"] and len(t["plan"][5]) == 4 and all(n["voices"] == t["plan"][n["phrase"]] for n in t["notes"])
    v = load("variation")
    assert v["part"] == 9 and "4.00" in v["measure"]


def test_the_part_keeps_the_series_rules():
    check_clips(compute)
    check_scenes_and_clips(compute, SCENES)
    check_windows(compute, SCENES)
    check_ear_thread(compute, SCENES)
