"""Monochord's string instruments against closed forms and published values.

    python -m pytest -q tests/music/test_strings.py
"""

import math

import numpy as np
import pytest

from explainer.music.monochord.instruments import strings as S


def test_karplus_strong_pitch_and_decay():
    y = S.karplus_strong(220.0, 2.0)
    spec = np.abs(np.fft.rfft(y[:48000] * np.hanning(48000)))
    f = np.fft.rfftfreq(48000, 1 / 48000)
    near = (f > 200) & (f < 240)
    assert abs(f[near][int(np.argmax(spec[near]))] - S.ks_pitch(220.0)) < 1.0 and abs(S.ks_pitch(220.0) - 220.0) < 0.5
    hi = lambda seg: np.abs(np.fft.rfft(seg))[2000:6000].sum() / np.abs(np.fft.rfft(seg))[100:400].sum()    # noqa: E731
    assert hi(y[:9600]) > 3 * hi(y[48000:57600])                                   # the high partials die first


def test_the_hammer():
    d = S.hammer_strike(velocity=1.5)
    assert 1.5e-3 < d["contact"] < 3.0e-3                                          # Chaigne and Askenfelt: about 2 ms at middle C
    assert d["hammer_out"] < 0 and 0 < d["energy_in"] < 0.5 * 2.97e-3 * 1.5 ** 2   # the hammer rebounds, leaving some of its energy
    n = d["n"]
    b = S.PIANO_C4.B
    assert np.allclose(d["hz"], n * S.PIANO_C4.f1 * np.sqrt(1 + b * n * n), rtol=1e-9)     # a stiff string's partials
    assert 3e-4 < b < 5e-4
    lv = S.partial_levels(d)
    assert lv[7] < lv[6] - 8 and lv[7] < lv[5] - 8                                 # struck at 12%: the 8th partial is nearly absent
    soft, loud = S.hammer_strike(velocity=0.5), S.hammer_strike(velocity=4.0)
    assert loud["contact"] < d["contact"] < soft["contact"]                        # a harder blow is a shorter one
    assert S.strike_centroid(loud) > 1.15 * S.strike_centroid(d) > 1.15 ** 2 * S.strike_centroid(soft) * 0.9   # and a brighter one
    assert loud["peak_force"] / soft["peak_force"] > 8                             # the felt stiffens: more than proportional


def test_a_struck_note_has_its_partials_where_the_stiff_string_puts_them():
    d = S.hammer_strike(velocity=1.5)
    y = S.struck(strike=d, seconds=2.0)
    seg = y[4800: 4800 + 96000 - 9600]
    spec = np.abs(np.fft.rfft(seg * np.hanning(len(seg)), 1 << 20))
    f = np.fft.rfftfreq(1 << 20, 1 / 48000)
    for hz in d["hz"][:7]:
        band = (f > hz - 6) & (f < hz + 6)
        assert abs(f[band][int(np.argmax(spec[band]))] - hz) < 0.3
    assert d["hz"][6] / (7 * d["hz"][0]) > 1.008                                   # the seventh partial is 15 cents sharp


def test_two_strings_on_one_bridge():
    one = S.pair(single=True)
    unison = S.pair(0.0, unequal=0.0)
    apart = S.pair(1.0, unequal=0.03)
    at = lambda d, t: float(np.interp(t, d["t"], d["db"]))                         # noqa: E731
    assert unison["rates"][0] == pytest.approx(0.25 + 2 * 1.6) and unison["rates"][1] == pytest.approx(0.25)
    assert at(unison, 1.0) < at(one, 1.0) - 10                                     # together they lose energy to the bridge twice as fast
    early = (at(apart, 0.5) - at(apart, 0.0)) / 0.5
    late = (at(apart, 5.5) - at(apart, 3.5)) / 2.0
    assert early < -20 and -6 < late < -1                                          # a fast decay, then a slow one
    assert at(apart, 5.0) > at(one, 5.0) + 20                                      # the aftersound outlasts a single string


def test_the_helmholtz_motion():
    d = S.bowed(196.0, S.Bow(speed=0.2, force=0.5, at=0.1), seconds=1.5)
    r = S.bow_regime(d)
    assert r["kind"] == "Helmholtz" and r["slip_fraction"] == pytest.approx(d["beta"], rel=0.06) and abs(r["pitch_ratio"] - 1) < 1e-3
    p = d["period"]
    x = d["bridge"][-40 * p:]
    spec = np.abs(np.fft.rfft(x - x.mean()))
    lv = [20 * math.log10(spec[40 * n] / spec[40]) for n in range(1, 8)]
    assert np.allclose(lv, [-20 * math.log10(n) for n in range(1, 8)], atol=0.5)   # the force on the bridge is a sawtooth: 1/n
    v = d["v"][-p:]
    stick = d["slipping"][-p:] < 0.5
    assert np.allclose(v[stick], 0.2, atol=1e-6)                                   # while it sticks, the string goes with the bow
    assert v[~stick].mean() == pytest.approx(-0.2 * (1 - d["beta"]) / d["beta"], rel=0.1)   # and flies back (1 - beta)/beta times faster


def test_schellengs_limits():
    rows = [S.bow_limits(b) for b in (0.06, 0.13, 0.19)]
    for r in rows:
        assert 0.8 < r["max"] / r["schelleng_max"] < 1.2                           # the greatest force: within 20% of his formula
        assert 1.0 < r["min"] / r["schelleng_min"] < 4.5                           # the least: above it, by a small factor
    slope_max = math.log(rows[2]["max"] / rows[0]["max"]) / math.log(rows[2]["beta"] / rows[0]["beta"])
    slope_min = math.log(rows[2]["min"] / rows[0]["min"]) / math.log(rows[2]["beta"] / rows[0]["beta"])
    assert slope_max == pytest.approx(-1.0, abs=0.15) and slope_min == pytest.approx(-2.0, abs=0.35)
    too_light = S.bow_regime(S.bowed(196.0, S.Bow(force=rows[1]["min"] / 5, at=0.13), seconds=1.5, press=rows[1]["min"] / 5))
    too_heavy = S.bow_regime(S.bowed(196.0, S.Bow(force=rows[1]["max"] * 5, at=0.13), seconds=1.5))
    assert too_light["kind"] == "multiple slips" and too_heavy["kind"] == "raucous"


def test_the_guitar_as_two_masses():
    t = S.two_mass()
    assert t["lower"] ** 2 + t["upper"] ** 2 == pytest.approx(t["helmholtz"] ** 2 + t["plate"] ** 2, rel=1e-9)
    assert t["lower"] < t["helmholtz"] < t["plate"] < t["upper"]
    assert 90 < t["lower"] < 110 and 190 < t["upper"] < 215 and 120 < t["helmholtz"] < 135    # a classical guitar (Fletcher and Rossing, ch. 9)
    g = S.guitar_body()
    f = np.linspace(60, 400, 3401)
    db = g.response_db(f)
    peaks = [f[i] for i in range(1, len(f) - 1) if db[i] > db[i - 1] and db[i] >= db[i + 1] and db[i] > db.max() - 20]
    assert abs(peaks[0] - t["lower"]) < 3 and any(abs(p - t["upper"]) < 4 for p in peaks)
    lo = t["lower"]
    dip = f[(f > lo) & (f < t["upper"])][int(np.argmin(db[(f > lo) & (f < t["upper"])]))]
    assert t["lower"] < dip < t["upper"]                                           # between them the two parts cancel


def test_bodies_ring_and_colour():
    tap = S.guitar_body().tap(0.5)
    spec = np.abs(np.fft.rfft(tap * np.hanning(len(tap))))
    f = np.fft.rfftfreq(len(tap), 1 / 48000)
    assert 85 < f[int(np.argmax(spec))] < 215                                      # a knock on a guitar sounds its two low resonances
    v = S.violin_body()
    hill, below = v.response_db(np.linspace(2000, 3000, 101)).mean(), v.response_db(np.linspace(1100, 1800, 101)).mean()
    assert hill > below + 3 and v.response_db([8000.0])[0] < hill - 12                 # the bridge hill, and the fall above it
    y = S.bowed_note(196.0, 0.8)
    out = v.play(y)
    assert len(out) > len(y) and np.abs(out).max() == pytest.approx(1.0)
