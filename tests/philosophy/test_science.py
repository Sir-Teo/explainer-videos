import math

import numpy as np

from explainer.philosophy.reasoner import science as Sc


def test_church_and_flagpole():
    assert Sc.church_ayer()["trivial"]
    f = Sc.flagpole(10, 45)
    assert abs(f["shadow"] - 10) < 1e-9 and abs(f["height_from_shadow"] - 10) < 1e-9
    m = Sc.moon_test()
    assert abs(m["agreement"] - 1) < 0.02


def test_no_miracles_base_rate():
    assert abs(Sc.no_miracles(0.5) - 0.95) < 1e-12
    assert abs(Sc.no_miracles(0.05) - 0.5) < 1e-12
    assert Sc.no_miracles(0.001) < 0.02


def test_fresnel_and_twins():
    d = Sc.fresnel()
    assert abs(d["brewster"] - math.degrees(math.atan(1.5))) < 1e-9 and abs(d["normal"] - 0.04) < 1e-12
    near = min(d["curve"], key=lambda r: abs(r[0] - 56.0))
    assert near[2] < 1e-3
    assert Sc.galilean_twins()["max_sep_diff"] < 1e-9


def test_ising():
    assert abs(Sc.TC - 2.269185) < 1e-5
    assert Sc.onsager_m(3.0) == 0 and Sc.onsager_m(1.0) > 0.99
    s = np.ones((9, 9), int)
    s[0, 0] = -1
    assert (Sc.block_spin(s) == 1).all()
    cold = Sc.ising_sw(27, 1.5, 30, 1, np.ones((27, 27), int))
    hot = Sc.ising_sw(27, 5.0, 30, 2)
    assert abs(cold.mean()) > 0.9 and abs(hot.mean()) < 0.3


def test_bacon_kepler():
    d = Sc.bacon()
    assert (d["found"][0]["i"], d["found"][0]["j"]) in ((3, -2), (-3, 2))


def test_risk_and_toys():
    cheap_fn = Sc.inductive_risk(1, 1)
    costly_fn = Sc.inductive_risk(1, 10)
    assert costly_fn["threshold"] < cheap_fn["threshold"]
    k = Sc.kuhn_toy()
    assert k["jump"] > 0.3 and k["t90"] is not None
    assert abs(Sc.kinetic_temperature(n=20000)["T_recovered"] - 300) < 10
    p = Sc.pendulum_idealization()
    assert p[0]["ratio"] < 1.001 and p[-1]["ratio"] > 2
