"""Agora's Keynesian economy (Part 27): the co-op, the cross, thrift, IS-LM with a zero bound, AS-AD, the machine,
sticky wages and the business cycle's spells."""

import numpy as np

from explainer.economics.agora import keynes as ks


def test_coop_recession_and_cure():
    r = ks.coop(n=150, coupons=4, target=10, weeks=200, p=0.3, seed=1, print_at=100, print_to=9)
    before, after = np.mean(r["evenings"][20:100]), np.mean(r["evenings"][120:])
    assert before < 0.15 < 0.18 < after <= r["potential"] + 0.02
    # the number of coupons is conserved except when printed
    assert abs(r["money"][50] - 4.0) < 1e-9 and abs(r["money"][150] - 9.0) < 1e-9


def test_coop_curve_is_hump_shaped():
    c = ks.coop_curve([2, 6, 9, 14, 22], seed=2)
    e = c["evenings"]
    assert e[0] < e[1] < e[2] and e[2] > e[3] > e[4]
    assert e[4] < 0.01          # too many coupons: nobody sits


def test_cross_and_multiplier_series():
    c = ks.cross(200, 0.6, 300, 200, 100)
    assert abs(c["Y"] - 1600) < 1e-9 and abs(c["multiplier"] - 2.5) < 1e-12
    up = ks.cross(200, 0.6, 300, 300, 100)
    assert abs(up["Y"] - c["Y"] - 250) < 1e-9
    # a balanced-budget rise in G and T raises Y one for one
    bb = ks.cross(200, 0.6, 300, 300, 200)
    assert abs(bb["Y"] - c["Y"] - 100) < 1e-9
    r = ks.multiplier_rounds(100, 0.6, 60)
    assert abs(r["cumulative"][-1] - r["limit"]) < 1e-6 and abs(r["limit"] - 250) < 1e-12


def test_paradox_of_thrift():
    f = ks.paradox_of_thrift(200, 0.6, 300, 0.0, 50, h=0.0)
    assert abs(f["dS"]) < 1e-9 and abs(f["dY"] + 125) < 1e-9
    g = ks.paradox_of_thrift(200, 0.6, 300, 0.0, 50, h=0.1)
    assert g["dS"] < 0 and abs(g["S1"] - g["I1"]) < 1e-9


def test_islm_policy_and_trap():
    kw = dict(a=200.0, b=0.6, T=100.0, I0=300.0, d=25.0, k=0.5, h=50.0)
    base = ks.islm(200, 600, **kw)
    # both markets clear
    assert abs(base["Y"] - ks.is_curve(200, base["i"], a=200, b=0.6, T=100, I0=300, d=25)) < 1e-9
    assert abs(600 - (0.5 * base["Y"] - 50 * base["i"])) < 1e-9
    fiscal = ks.islm(250, 600, **kw)
    assert 1 < (fiscal["Y"] - base["Y"]) / 50 < 2.5 and fiscal["i"] > base["i"]
    # in the trap, money does nothing and the full multiplier applies
    slump = {**kw, "I0": 150.0}
    m1, m2 = ks.islm(200, 800, **slump), ks.islm(200, 1200, **slump)
    assert m1["trap"] and m2["trap"] and abs(m1["Y"] - m2["Y"]) < 1e-9
    g = ks.islm(250, 800, **slump)
    assert abs((g["Y"] - m1["Y"]) / 50 - 2.5) < 1e-9
    # expected inflation lowers the real rate at the floor and raises output
    assert ks.islm(200, 800, pe=2.0, **slump)["Y"] > m1["Y"] > ks.islm(200, 800, pe=-2.0, **slump)["Y"]


def test_asad_shocks():
    kw = dict(a=200.0, b=0.6, T=100.0, I0=300.0, d=25.0, k=0.5, h=50.0)
    e0 = ks.asad(200, 600, 1450, 1.0, 300, **kw)
    d = ks.asad(200, 500, 1450, 1.0, 300, **kw)
    s = ks.asad(200, 600, 1450, 1.0, 300, cost=0.15, **kw)
    assert d["Y"] < e0["Y"] and d["P"] < e0["P"]       # demand shock: both fall
    assert s["Y"] < e0["Y"] and s["P"] > e0["P"]       # supply shock: opposite ways
    # AD turns vertical in the trap: deflation stops raising demand
    ad = ks.ad_curve([0.5, 0.6], 200, 600, **kw)
    assert abs(ad[0] - ad[1]) < 1e-9


def test_moniac_converges_to_multiplier():
    m = ks.moniac(b=0.6, tax=0.2, I=150, G=200, Y0=(350) / (1 - 0.48), speed=0.25, steps=200, shock_at=5, dG=50)
    assert abs(m["Y"][-1] - m["end"]) < 1e-6
    assert abs(m["multiplier"] - 1 / (1 - 0.6 * 0.8)) < 1e-12


def test_wage_spike_at_zero():
    w = ks.wage_changes(n=50000, mean=0.01, sd=0.04, rigid=0.8, seed=1)
    assert abs(w["share_zero"] - 0.8 * w["share_cut_wanted"]) < 0.01
    assert w["mean_got"] > w["mean_want"]


def test_spells():
    x = [0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0]
    d = [f"{1900 + k}-01-01" for k in range(len(x))]
    s = ks.spells(x, d)
    assert s["recessions"] == [3, 1] and s["expansions"] == [4]
