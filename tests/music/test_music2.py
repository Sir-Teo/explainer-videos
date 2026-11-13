"""Part 2 of *Music, Built*: what the film says is what was computed, and every sound keeps the series' rules.

    python -m pytest -q tests/music/test_music2.py

The cache is filled on first use (about two minutes).
"""

import math

import numpy as np
import pytest

from tests.music.partcheck import check_part
from videos.music.music2 import compute
from videos.music.music2.manifest import SCENES

load = compute.load


def test_krakatoa_and_the_jar():
    k = load("krakatoa")
    assert 4.0 < k["rows"][2]["hours"] < 4.6 and 33 < k["circuit_hours"] < 38
    assert [round(r["db"]) for r in load("vacuum")["rows"]] == [0, -10, -20, -30]


def test_the_speed_of_sound_comes_from_the_gas_law():
    s = load("speed")
    assert s["newton_sim"] == pytest.approx(s["newton"], rel=2e-3) and s["laplace_sim"] == pytest.approx(s["laplace"], rel=2e-3)
    assert s["short"] == pytest.approx(1 - 1 / math.sqrt(1.4), abs=1e-6)
    assert s["cents"] == pytest.approx(s["cents_formula"], abs=0.3) and 2.8 < s["per_degree"] < 3.1


def test_decibels():
    d = load("decibel")
    assert d["mean"]["2"] == pytest.approx(3.0, abs=0.6) and d["mean"]["10"] == pytest.approx(10.0, abs=0.8)
    assert 5.0 < d["measured"]["10"] < 12.0 and d["quiz_answer"] == "B"
    p = load("parcels")["sizes"][1]
    assert p["pa"] == pytest.approx(0.02) and 8 < p["nm_1khz"] < 14


def test_spreading_diffraction_and_interference():
    s = load("spread")
    assert s["space_exponent"] == pytest.approx(-1.0, abs=0.01) and s["per_doubling_db"] == pytest.approx(6.02, abs=0.05)
    assert s["plane_exponent"] == pytest.approx(-0.5, abs=0.05)
    d = load("diffraction")
    assert d["worst_vs_maekawa"] < 3.0
    assert [t["db"] for t in d["table"]] == sorted([t["db"] for t in d["table"]], reverse=True)   # worse with every octave
    i = load("interfere")
    assert i["worst"] < 0.1 and i["quiet_db"] < -20


def test_pipes_and_the_bottle():
    t = load("tubes")
    assert t["rows"]["open"]["worst_cents"] < 0.1 and t["rows"]["stopped"]["worst_cents"] < 0.1
    assert t["rows"]["stopped"]["sim"][0] == pytest.approx(t["rows"]["open"]["sim"][0] / 2, rel=1e-3)
    assert t["plane_f1"] < t["plane_ideal"] and 0.3 < t["plane_extra_widths"] < 1.5
    a, b = t["quiz_partials"]["A"], t["quiz_partials"]["B"]
    assert max(a[1], a[3], a[5]) < 0.02 < min(b[1], b[3])            # the stopped pipe has no even partials
    assert t["half_hz"] == pytest.approx(t["open_hz"], rel=1e-3)
    bt = load("bottle")
    assert abs(bt["sim_cents"]) < 3 and 40 < bt["lumped_cents"] < 70 and 20 < bt["q"] < 50
    assert all(abs(1200 * math.log2(r["sim"] / r["exact"])) < 8 for r in bt["sweep"])


def test_impedance_doppler_and_the_frontier():
    i = load("impedance")
    assert i["r_sim"] == pytest.approx(i["r_formula"], abs=0.02) and i["sudden"] == pytest.approx(i["sudden_formula"], abs=0.01)
    assert i["horn"] > 0.95 and i["through_water"] == pytest.approx(0.0011, abs=0.0002)
    d = load("doppler")
    assert d["curves"]["train"]["cents"] == pytest.approx(200.0, abs=0.01) and 65 < d["ballot_kmh"] < 76
    assert d["curves"]["fast"]["cents"] > 1.9 * d["curves"]["slow"]["cents"]
    n = load("nonlinear")
    assert n["worst"] < 0.01
    assert n["horn"][2]["shock_m"] < n["tube_m"] < n["horn"][1]["shock_m"]


def test_variation_two():
    t = load("tune")
    assert len(t["notes"]) == 42 and t["worst_cents"] < 2.0
    fills = [k["fill"] for k in t["checks"]]
    assert fills == sorted(fills) and fills[0] == pytest.approx(0.0, abs=1e-6) and fills[-1] < 0.8
    assert load("variation")["part"] == 2


def test_the_part_keeps_the_series_rules():
    check_part(compute, SCENES)
