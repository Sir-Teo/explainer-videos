"""Psyche's body module against closed forms and its own known behaviour."""

import math

import numpy as np
import pytest

from explainer.psychology.psyche import body as B


def rng(seed):
    return np.random.default_rng(seed)


def test_the_clock_runs_a_little_longer_than_a_day_when_left_alone():
    assert B.free_running_period() == pytest.approx(24.15, abs=0.1)


def test_an_ordinary_day_entrains_the_clock_and_a_28_hour_day_does_not():
    day = B.entrain()
    assert day["locked"] and day["period"] == pytest.approx(24.0, abs=0.02)
    assert 3.0 < day["minimum_at"] < 6.0                       # the temperature minimum falls before dawn
    long = B.entrain(day=28.0, lux=40.0)
    assert not long["locked"] and long["period"] == pytest.approx(24.2, abs=0.2)
    assert B.entrain(day=25.0)["locked"] and B.entrain(day=23.0)["locked"]


def test_light_before_the_minimum_delays_and_light_after_it_advances():
    p = B.phase_response(steps=12)
    h, s = p["hours_from_minimum"], p["shift"]
    assert s[(h > -6) & (h < -2)].min() < -0.5                 # evening and early-night light: later
    assert s[(h > 0.5) & (h < 5)].max() > 0.4                  # morning light: earlier


def test_jet_lag_takes_days_and_more_zones_take_longer():
    three, six = B.jet_lag(3), B.jet_lag(6)
    assert 2 <= three["days_to_adjust"] <= 6 and six["days_to_adjust"] >= three["days_to_adjust"]
    assert abs(six["hours_off"][0]) > 4


def test_sleep_pressure_follows_its_two_exponentials():
    r = B.two_process(hours=96, s0=0.5)
    t, S, asleep = r["t"], r["S"], r["asleep"]
    i = np.where(~asleep[:-1] & ~asleep[1:])[0][100]
    dt = t[1] - t[0]
    assert (1 - S[i + 1]) / (1 - S[i]) == pytest.approx(math.exp(-dt / B.TAU_RISE), rel=1e-6)
    j = np.where(asleep[:-1] & asleep[1:])[0][100]
    assert S[j + 1] / S[j] == pytest.approx(math.exp(-dt / B.TAU_FALL), rel=1e-6)


def test_the_model_sleeps_about_eight_hours_at_night():
    r = B.two_process(hours=144, s0=0.5)
    for start, end in r["episodes"][2:]:
        assert end - start == pytest.approx(8.0, abs=0.5)
        assert 21.5 < start % 24 < 24.0 or start % 24 < 0.5


def test_recovery_sleep_after_a_lost_night_is_only_a_little_longer():
    r = B.two_process(hours=144, s0=0.5, keep_awake=[(40.0, 71.0)])
    recovery = [e - s for s, e in r["episodes"] if s >= 70.9][0]
    assert 8.2 < recovery < 10.5                                # forty hours awake, and nothing like sixteen hours of sleep


def test_lapses_grow_with_cumulative_excess_wakefulness():
    assert np.allclose(B.lapses(8.16), 1.0)
    six, four = B.lapses(6.0), B.lapses(4.0)
    assert np.all(np.diff(six) > 0) and four[-1] > six[-1] > 1.0
    assert (four[-1] - 1) / (six[-1] - 1) == pytest.approx((20 - 15.84) / (18 - 15.84), rel=1e-6)


def test_the_stress_loop_has_a_morning_peak_and_switches_a_stressor_off():
    base = B.hpa()
    day = base["t"] > 48
    peak_at = base["t"][day][base["cortisol"][day].argmax()] % 24
    assert 5.0 < peak_at < 10.0
    hit = B.hpa(stress=[(58.0, 1.0, 3.0)])
    extra = hit["cortisol"] - base["cortisol"]
    assert extra.max() > 0.05 and abs(extra[-1]) < 0.01 * extra.max()
    worn = B.hpa(stress=[(58.0, 1.0, 3.0)], feedback=0.3)
    worn_base = B.hpa(feedback=0.3)
    assert (worn["cortisol"] - worn_base["cortisol"]).max() > extra.max()
    assert worn_base["cortisol"][day].mean() > base["cortisol"][day].mean()


def test_the_hill_equation_and_a_competitive_antagonist():
    assert B.occupancy(1.0) == pytest.approx(0.5) and B.occupancy(9.0) == pytest.approx(0.9)
    assert B.occupancy(2.0, kd=2.0, n=3.0) == pytest.approx(0.5)
    assert B.with_antagonist(10.0, antagonist=9.0) == pytest.approx(B.occupancy(1.0))   # ten times the dose for the same effect


def test_two_ways_out_of_the_body():
    assert B.first_order(5.0, half_life=5.0) == pytest.approx(0.5) and B.first_order(10.0, half_life=5.0) == pytest.approx(0.25)
    assert B.zero_order(2.0, dose=1.0, rate=0.15) == pytest.approx(0.7) and B.zero_order(10.0) == 0.0
    d = B.dosing([8.0], hours=40.0, half_life=5.0)
    late = d["level"][np.searchsorted(d["t"], 30.0)] / d["level"][np.searchsorted(d["t"], 25.0)]
    assert late == pytest.approx(0.5, abs=0.01)


def test_tolerance_and_withdrawal_come_from_one_slow_process():
    o = B.opponent(doses=10)
    assert o["felt"][0] > 2 * o["felt"][-1]                    # the same dose is felt less
    assert o["troughs"][-1] < 3 * o["troughs"][0] < 0          # and the after-effect deepens


def test_a_new_place_removes_part_of_the_tolerance():
    out = B.conditioned_tolerance(1.6, 0.75, 0.45, rng=rng(1))
    assert out["usual"] < out["new"] < out["none"]
    assert out["usual"] == pytest.approx(0.32, abs=0.04) and out["none"] > 0.85


def test_midsleep_and_social_jetlag_wrap_around_midnight():
    assert B.midsleep(23.0, 7.0) == pytest.approx(3.0) and B.midsleep(1.0, 9.0) == pytest.approx(5.0)
    assert B.social_jetlag(23.0, 7.0, 1.0, 9.0) == pytest.approx(2.0)
