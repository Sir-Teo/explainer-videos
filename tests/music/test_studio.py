"""Monochord's studio (Part 56): stereo pairs, combs, gain staging, crossfades, the console, the masking map, width
and the automatic mixer.

    python -m pytest -q tests/music/test_studio.py
"""

import math

import numpy as np
import pytest

from explainer.music.monochord import studio as S

SR = 48000


def test_pairs():
    c = S.pair_cues("XY", 90.0)
    assert float(c["dL"]) == pytest.approx(20 * math.log10((0.5 + 0.5 * math.cos(math.radians(45))) / (0.5 + 0.5 * math.cos(math.radians(135)))))
    assert float(S.pair_cues("AB", 90.0)["dt"]) == pytest.approx(1000 * 0.6 / S.C)
    assert float(S.pair_cues("XY", 30.0)["dt"]) == 0.0 and float(S.pair_cues("AB", 30.0)["dL"]) == 0.0
    for k in S.PAIRS:                                    # symmetric: a source on the right mirrors one on the left
        a, b = S.pair_cues(k, 25.0), S.pair_cues(k, -25.0)
        assert float(a["dL"]) == pytest.approx(-float(b["dL"])) and float(a["dt"]) == pytest.approx(-float(b["dt"]))
    assert S.recording_angle("Blumlein") < S.recording_angle("ORTF") < S.recording_angle("XY")
    assert S.image_position(15.0, 0.0) == pytest.approx(1.0) and S.image_position(0.0, 0.55) == pytest.approx(0.5)


def test_pair_render_delays():
    x = np.zeros(4800)
    x[100] = 1.0
    y = S.pair_render(x, "AB", 90.0)
    lag = (np.argmax(y[:, 1]) - np.argmax(y[:, 0])) / SR
    assert lag == pytest.approx(0.6 / S.C, abs=2 / SR)


def test_comb():
    tau = 0.005
    assert float(S.comb_db(np.array([1 / (2 * tau)]), tau, 1.0)[0]) < -100
    assert float(S.comb_db(np.array([1 / tau]), tau, 1.0)[0]) == pytest.approx(20 * math.log10(2))
    hi, lo = S.comb_extremes(1 / 3)
    assert hi == pytest.approx(2.4988, abs=1e-3) and lo == pytest.approx(-3.5218, abs=1e-3)


def test_chain():
    r = S.chain(spl=94.0, sens_mv=7.746, gain_db=40.0, fs_dbu=18.0)
    assert r["mic_dbu"] == pytest.approx(-40.0, abs=1e-3) and r["pre_dbu"] == pytest.approx(0.0, abs=1e-3)
    assert r["peak_dbfs"] == pytest.approx(-18.0, abs=1e-3) and not r["clips"]
    assert S.chain(gain_db=70.0)["clips"]
    q = S.quantize(np.linspace(-0.9, 0.9, 1001), 8)
    assert np.max(np.abs(q - np.linspace(-0.9, 0.9, 1001))) <= 2 ** -8 + 1e-12


def test_crossfades():
    fo, fi = S.fade_pair(1000, "power")
    assert np.allclose(fo ** 2 + fi ** 2, 1.0)
    fo, fi = S.fade_pair(1000, "linear")
    assert np.allclose(fo + fi, 1.0)
    a = np.ones(1000)
    y = S.crossfade(a, a, 200, "linear")
    assert len(y) == 1800 and np.allclose(y, 1.0)


def test_pan_laws():
    for law in (0.0, -3.0, -4.5, -6.0):
        gL, gR = S.pan_gains(np.array([0.0]), law)
        assert 20 * math.log10(gL[0]) == pytest.approx(law, abs=0.03)
        gL, gR = S.pan_gains(np.array([-1.0]), law)
        assert gL[0] == pytest.approx(1.0) and gR[0] == pytest.approx(0.0, abs=1e-12)
    p = np.linspace(-1, 1, 101)
    gL, gR = S.pan_gains(p, -3.0)
    assert np.allclose(gL ** 2 + gR ** 2, 1.0)


def test_console():
    rng = np.random.default_rng(0)
    x = rng.standard_normal(SR)
    m = S.mix([S.Channel("a", x, gain_db=-6.0, pan=-1.0), S.Channel("b", x, gain_db=0.0, pan=1.0)], law=-3.0)
    assert np.allclose(m["y"][:, 0], 10 ** (-6 / 20) * x) and np.allclose(m["y"][:, 1], x)
    st = np.stack([x, -x], axis=1)
    narrow = S.place(st, 0.0, width=0.0)
    assert np.allclose(narrow, 0.0)
    e = S.echo_bus(0.1, 0.5, 20000.0)(np.stack([np.r_[1.0, np.zeros(SR - 1)]] * 2, axis=1))
    first = np.nonzero(np.abs(e).sum(axis=1) > 1e-3)[0][0]
    assert first == pytest.approx(int(0.1 * SR), abs=2)


def test_masking_map():
    t = np.arange(SR) / SR
    loud = np.sin(2 * np.pi * 1000 * t)
    quiet = 0.01 * np.sin(2 * np.pi * 1010 * t)
    far = 0.01 * np.sin(2 * np.pi * 6000 * t)
    m = S.masking_map({"loud": loud, "quiet": quiet, "far": far})
    assert m["overall"]["quiet"] > 0.9 and m["overall"]["far"] < 0.1 and m["overall"]["loud"] < 0.1
    pm = S.masking_map({"loud": np.stack([loud, 0 * loud], axis=1), "quiet": np.stack([0 * quiet, quiet], axis=1)})
    assert pm["overall"]["quiet"] < 0.1                   # panned apart, nothing masks


def test_width():
    rng = np.random.default_rng(1)
    x = rng.standard_normal(SR)
    assert S.correlation(x, x) == pytest.approx(1.0) and S.mono_loss_db(x, x) == pytest.approx(0.0, abs=1e-9)
    assert S.mono_loss_db(x, rng.standard_normal(SR)) == pytest.approx(-3.0, abs=0.1)
    M, Sd = S.ms_encode(x, 0.5 * x)
    L, R = S.ms_decode(M, Sd)
    assert np.allclose(L, x) and np.allclose(R, 0.5 * x)
    h = S.haas(x, 12.0)
    assert abs(S.correlation(h[:, 0], h[:, 1])) < 0.05


def test_automix_rules():
    rng = np.random.default_rng(2)
    t = np.arange(SR) / SR
    bass = 0.3 * np.sin(2 * np.pi * 60 * t)
    hat = 0.01 * rng.standard_normal(SR)
    vox = 0.1 * np.sin(2 * np.pi * 2000 * t)
    am = S.automix({"bass": bass, "hat": hat, "vox": vox}, lead="vox")
    ch = {c.name: c for c in am["channels"]}
    assert ch["bass"].pan == 0.0 and ch["vox"].pan == 0.0 and ch["hat"].pan != 0.0
    assert ch["hat"].hpf == 80.0 and ch["bass"].hpf is None
    out = S.mix(am["channels"])["stems"]
    louds = {k: S.lufs(v) for k, v in out.items()}
    assert louds["vox"] - louds["bass"] == pytest.approx(3.0, abs=0.6)
