"""Agora's firm (explainer.economics.agora.firm)."""

import numpy as np
import pytest

from explainer.economics.agora import firm as fm

CD_1928 = {  # Felipe and Adams (2005), table 1: output, labour, capital, 1899 = 100
    1899: (100, 100, 100), 1900: (101, 105, 107), 1901: (112, 110, 114), 1902: (122, 118, 122),
    1903: (124, 123, 131), 1904: (122, 116, 138), 1905: (143, 125, 149), 1906: (152, 133, 163),
    1907: (151, 138, 176), 1908: (126, 121, 185), 1909: (155, 140, 198), 1910: (159, 144, 208),
    1911: (153, 145, 216), 1912: (177, 152, 226), 1913: (184, 154, 236), 1914: (169, 149, 244),
    1915: (189, 154, 266), 1916: (225, 182, 298), 1917: (227, 196, 335), 1918: (223, 200, 366),
    1919: (218, 193, 387), 1920: (231, 193, 407), 1921: (179, 147, 417), 1922: (240, 161, 431)}


def test_technologies_and_shephard():
    for tech in (fm.CobbDouglas(2.0, 0.3, 0.7), fm.CES(1.5, 0.3, 0.5, 1.0), fm.CES(1.0, 0.4, 2.0, 0.9),
                 fm.CobbDouglas(1.0, 0.3, 0.5)):
        K, L = tech.demand(10.0, 4.0, 50.0)
        assert float(tech.q(K, L)) == pytest.approx(50.0, rel=1e-6)
        assert max(fm.shephard_errors(tech, 10.0, 4.0, 50.0).values()) < 1e-5
    cd = fm.CobbDouglas(1.0, 0.25, 0.75)
    assert cd.trs(4.0, 1.0) == pytest.approx(3 * 4.0)                 # MP_L / MP_K = (b / a) K / L
    lt = fm.Leontief(2.0, 3.0)
    assert lt.cost(1.0, 1.0, 10.0) == pytest.approx(50.0)
    # CES with sigma near 1 is Cobb-Douglas
    c1 = fm.CES(1.0, 0.3, 0.999999, 1.0)
    assert float(c1.q(2.0, 3.0)) == pytest.approx(float(fm.CobbDouglas(1.0, 0.3, 0.7).q(2.0, 3.0)), rel=1e-4)


def test_isoquant():
    cd = fm.CobbDouglas(1.0, 0.5, 0.5)
    K = fm.isoquant(cd, 4.0, [1.0, 2.0, 4.0])
    assert K == pytest.approx([16.0, 8.0, 4.0], rel=1e-6)


def test_short_run_and_envelope():
    t = fm.CobbDouglas(1.0, 0.5, 0.5)
    sr = fm.ShortRun(t, 4.0, 1.0, 1.0)
    qs = np.linspace(0.5, 8, 400)
    # the short-run cost touches the long-run cost where K = 4 is the right capital
    lr = np.array([t.cost(1.0, 1.0, q) for q in qs])
    assert np.all(sr.tc(qs) >= lr - 1e-9)
    k_star = qs[np.argmin(sr.tc(qs) - lr)]
    assert t.demand(1.0, 1.0, k_star)[0] == pytest.approx(4.0, rel=0.02)
    # marginal cost cuts average variable and average total cost at their minima
    q_min = qs[np.argmin(sr.atc(qs))]
    assert sr.mc(q_min) == pytest.approx(sr.atc(q_min), rel=0.02)


def test_supply_profit_hotelling():
    t = fm.CobbDouglas(1.0, 0.3, 0.5)
    assert max(fm.hotelling_errors(t, 5.0, 1.0, 2.0).values()) < 1e-5
    lc = fm.le_chatelier(t)
    assert lc["long"] > lc["short"]
    q1, q2 = fm.cd_supply(t, 5.0, 1.0, 2.0), fm.cd_supply(t, 5.0 * 1.01, 1.0, 2.0)
    assert np.log(q2 / q1) / np.log(1.01) == pytest.approx(lc["long"], rel=1e-3)


def test_ucost_and_industry():
    u = fm.UCost(16.0, 2.0, 1.0)
    assert u.efficient_scale == pytest.approx(4.0) and u.breakeven == pytest.approx(10.0)
    assert float(u.atc(4.0)) == pytest.approx(10.0) and float(u.mc(4.0)) == pytest.approx(10.0)
    assert u.supply(9.0) == 0.0 and u.supply(9.0, long_run=False) > 0
    ind = fm.industry(1000.0, 20.0, 16.0, 2.0, 1.0)
    assert ind["price"] == pytest.approx(10.0) and ind["firms"] == pytest.approx(200.0)
    het = fm.industry(1000.0, 20.0, None, 2.0, 1.0, fixed_costs=np.linspace(4, 40, 400))
    assert het["profits"][0] > het["profits"][-1] >= 0 and het["rents"] > 0


def test_cobb_douglas_1928():
    Y, L, K = (np.array([v[i] for v in CD_1928.values()], float) for i in range(3))
    years = list(CD_1928)
    crs = fm.fit_cobb_douglas(Y, K, L, "crs")
    un = fm.fit_cobb_douglas(Y, K, L, "unrestricted")
    tr = fm.fit_cobb_douglas(Y, K, L, "trend", years=years)
    # with constant returns imposed: labour 3/4 and A = 1.01, Cobb and Douglas's P' = 1.01 L^(3/4) C^(1/4);
    # Felipe and Adams (2005), table 2: unrestricted 0.807 and 0.233; with a trend, capital's coefficient turns negative
    assert crs["labour"] == pytest.approx(0.746, abs=0.002) and np.exp(crs["const"]) == pytest.approx(1.01, abs=0.01)
    assert un["labour"] == pytest.approx(0.807, abs=0.002) and un["capital"] == pytest.approx(0.233, abs=0.002)
    assert tr["capital"] < 0 and tr["trend"] > 0


def test_boundary_of_the_firm():
    h = fm.hold_up(10.0, 0.5)
    assert h["first_best"] == pytest.approx(100.0) and h["held_up"] == pytest.approx(25.0) and h["loss"] > 0
    g = fm.ghm(4.0, 1.0, 0.8, 0.8)
    assert g["best"] == "A owns"                                       # ownership to the party whose investment matters
    g2 = fm.ghm(1.0, 4.0, 0.8, 0.8)
    assert g2["best"] == "B owns"
    assert g["first best"]["surplus"] >= g[g["best"]]["surplus"]
    mb = fm.make_or_buy(np.linspace(0, 2, 5))
    assert mb["switch"] == pytest.approx(0.4)
    hb = fm.hire(4.0, 3.0, fm.CobbDouglas(1.0, 0.25, 0.75), 16.0)
    assert hb["hired"] == hb["best"] or abs(hb["hired"] - hb["best"]) <= 1


def test_selection_finds_the_optimum():
    out = fm.selection(200, 120, -3.0, 0.15, 0.03, 1950)
    first, last = out["markups"][0], out["markups"][-1]
    assert out["best"] == pytest.approx(0.5)
    # survival pulls the markups toward the profit-maximizing 50% without any yard maximizing anything
    assert abs(np.median(last) - 0.5) < abs(np.median(first) - 0.5) + 0.05
    assert np.std(last) < np.std(first)
    assert out["closures"].sum() > 0
