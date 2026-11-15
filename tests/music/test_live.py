"""Monochord's live sound (Part 59): Nyquist's gain before feedback, ringing out, the potential acoustic gain,
point and line sources, cardioid subwoofers, delay towers, air absorption, the dual-channel measurement, wireless
intermodulation, the speech transmission index and the noise dose.

    python -m pytest -q tests/music/test_live.py
"""

import math

import numpy as np
import pytest

from explainer.music.monochord import live as LV

SR = 48000


def delayed_echo_ir(delay_s=0.01, gain=0.5):
    h = np.zeros(int(0.05 * SR))
    h[int(delay_s * SR)] = gain
    return h


def test_speed_of_sound_and_delay_tower():
    assert LV.speed_of_sound(20.0) == pytest.approx(343.42)
    assert LV.delay_time(90.0, 30.0, 20.0) == pytest.approx(60.0 / 343.42 + 0.010)
    assert LV.delay_time(90.0, 30.0, 10.0) > LV.delay_time(90.0, 30.0, 30.0)


def test_feedback_by_nyquist():
    # a pure delay of gain 1/2: G H = g/2 e^{-i w tau} reaches +1 at f = k/tau when g = 2, i.e. +6 dB
    fb = LV.feedback(delayed_echo_ir(0.01, 0.5), fmin=50, fmax=1000)
    assert fb["max_gain_db"] == pytest.approx(20 * math.log10(2), abs=0.01)
    assert fb["howl_hz"] == pytest.approx(round(fb["howl_hz"] / 100) * 100, abs=1.0)
    # the closed loop just under the limit decays, just over it grows
    x = np.zeros(SR // 2)
    x[0] = 1.0
    ir = delayed_echo_ir(0.01, 0.5)
    under = LV.closed_loop(x, ir, fb["max_gain_db"] - 1.0)
    over = LV.closed_loop(x, ir, fb["max_gain_db"] + 1.0)
    assert np.max(np.abs(under[-SR // 10:])) < 0.2 and np.max(np.abs(over[-SR // 10:])) > 10


def test_ring_out_buys_gain():
    rng = np.random.default_rng(1)
    h = rng.standard_normal(4000) * np.exp(-np.arange(4000) / 800)
    h[:200] = 0
    steps = LV.ring_out(h, notches=4)
    gains = [s["max_gain_db"] for s in steps]
    assert gains[-1] > gains[0] + 1.0
    assert all(b >= a - 0.5 for a, b in zip(gains, gains[1:]))


def test_pag_nag():
    r = LV.pag_nag(d0=10.0, d1=5.0, ds=0.5, d2=10.0, nom=1, fsm=6.0)
    assert r["pag"] == pytest.approx(20 * math.log10(10 * 5 / (0.5 * 10)) - 6)
    assert r["nag"] == pytest.approx(20.0)
    assert LV.pag_nag(10, 5, 0.5, 10, nom=2)["pag"] == pytest.approx(r["pag"] - 10 * math.log10(2))


def test_point_falls_6_db_per_doubling():
    lv = LV.field([(0.0, 0.0)], 1000.0, [10.0, 20.0, 40.0], [0.0], air=False)[0]
    assert lv[0] - lv[1] == pytest.approx(6.02, abs=0.05) and lv[1] - lv[2] == pytest.approx(6.02, abs=0.05)


def test_line_array_geometry():
    pos, ang = LV.line_array(5, 0.35)
    assert pos[0] == (0.0, 12.0) and pos[-1][1] == pytest.approx(12.0 - 4 * 0.35) and ang == [0.0] * 5
    pos, ang = LV.line_array(3, 0.35, splay_deg=[2.0, 3.0])
    assert ang == [0.0, 2.0, 5.0]
    assert math.dist(pos[1], pos[2]) == pytest.approx(0.35)


def test_cardioid_sub_cancels_behind():
    f = np.array([40.0, 63.0, 100.0])
    r = LV.cardioid_sub(f, 0.9)
    assert np.all(r["back_db"] < -100)
    # in front the two arrive 2 d / c apart, inverted: |sin(2 pi f d / c)| -- strongest where d is a quarter wave
    c = LV.speed_of_sound()
    assert r["front_db"][1] == pytest.approx(20 * math.log10(abs(math.sin(2 * math.pi * 63 * 0.9 / c))), abs=0.1)


def test_air_absorption_iso():
    # ISO 9613-1 at 20 C, 50 % RH: about 0.005 dB/m at 1 kHz and 0.1 dB/m at 8 kHz
    a = LV.air_absorption_db_per_m(np.array([1000.0, 8000.0]), 20.0, 50.0)
    assert 0.003 < a[0] < 0.007 and 0.07 < a[1] < 0.14
    assert LV.air_absorption_db_per_m(np.array([4000.0]), 20.0, 20.0)[0] > LV.air_absorption_db_per_m(np.array([4000.0]), 20.0, 80.0)[0]


def test_transfer_function_finds_the_delay():
    rng = np.random.default_rng(2)
    x = rng.standard_normal(SR * 3)
    d = 480
    y = np.r_[np.zeros(d), 0.5 * x[:-d]] + 0.01 * rng.standard_normal(len(x))
    tf = LV.transfer_function(x, y, 8192)
    assert tf["delay_s"] == pytest.approx(d / SR)
    band = (tf["f"] > 100) & (tf["f"] < 10000)
    assert np.median(np.abs(tf["H"][band])) == pytest.approx(0.5, rel=0.05)
    assert np.median(tf["coherence"][band]) > 0.9


def test_imd_and_planner():
    assert sorted(LV.imd3([500.0, 501.0])) == [499.0, 502.0]
    assert 500.0 + 502.0 - 501.0 in LV.imd3([500.0, 501.0, 502.0])
    plan = LV.plan_channels(470.0, 500.0, 10, exclude=[(482.0, 488.0)])
    prods = LV.imd3(plan)
    assert all(min(abs(p - c) for p in prods) >= 0.1 - 1e-9 for c in plan)
    assert all(not (482.0 <= c <= 488.0) for c in plan)
    assert min(np.diff(plan)) >= 0.35 - 1e-9


def test_sti_and_dose():
    assert LV.sti(0.3, 30.0) > LV.sti(1.0, 30.0) > LV.sti(3.0, 30.0)
    assert LV.sti(1.0, 30.0) > LV.sti(1.0, 0.0)
    assert 0.0 <= LV.sti(10.0, -20.0) < 0.1
    assert LV.allowed_hours(85.0) == pytest.approx(8.0) and LV.allowed_hours(100.0) == pytest.approx(0.25)
    assert LV.dose([85.0], [8.0]) == pytest.approx(100.0)
    assert LV.dose([91.0, 85.0], [1.0, 4.0]) == pytest.approx(100.0)
