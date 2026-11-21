"""Agora's climate (Part 48): resources, fisheries, the fitted climate, the DICE-style model and the rest."""

import numpy as np
import pytest

from explainer.economics.agora import climate as cl


def test_hotelling_rent_rises_at_the_rate_of_interest():
    h = cl.hotelling(stock=200, choke=10, slope=1, r=0.05, cost=2)
    p, c = np.array(h["price"]), np.array(h["cost"])
    rent = (p - c)[: h["exhausted"] - 1]
    assert np.allclose(rent[1:] / rent[:-1], 1.05, atol=1e-9)
    assert abs(sum(h["quantity"]) - 200) < 1e-6
    assert p[h["exhausted"]] == pytest.approx(10)


def test_falling_costs_make_a_u():
    h = cl.hotelling(stock=200, choke=10, slope=1, r=0.05, cost=6, cost_growth=-0.04)
    p = np.array(h["price"][: h["exhausted"]])
    k = int(p.argmin())
    assert 0 < k < len(p) - 1 and p[0] > p[k] < p[-1]


def test_fishery_ordering_and_rent():
    f = cl.fishery_curves(growth=0.5, capacity=1, catchability=1, price=1, cost=0.2)
    assert f["e_mey"] < f["e_msy"] < f["e_open"]
    assert f["rent_open"] == pytest.approx(0, abs=1e-12)
    assert f["rent_mey"] > 0 and f["stock_mey"] > f["stock_open"]


def test_fishery_quota_keeps_the_stock():
    kw = dict(growth=0.5, capacity=1, catchability=1, price=1, cost=0.2, entry=2, stock0=1, effort0=0.02)
    open_ = cl.fishery_dynamics(**kw)
    quota = cl.fishery_dynamics(**kw, quota=0.1)
    assert min(open_["stock"]) < 0.1 < quota["stock"][-1]


def test_carbon_cycle_pulse():
    E = np.zeros(200)
    E[0] = 100 / cl.GTC_PER_GTCO2      # 100 GtC
    ppm = cl.carbon_cycle(E)["ppm"]
    added = (ppm - cl.PREINDUSTRIAL_PPM) / cl.PPM_PER_GTC
    assert added[0] == pytest.approx(100, rel=1e-9)
    assert 0.35 < added[100] / 100 < 0.45            # AR5: about 40 percent left after a century
    assert cl.carbon_cycle(np.zeros(10))["ppm"][-1] == pytest.approx(cl.PREINDUSTRIAL_PPM)


def test_ebm_settles_at_the_sensitivity():
    T, D = cl.ebm(np.full(3000, cl.F2X), ecs=3.0)
    assert T[-1] == pytest.approx(3.0, abs=0.02)
    assert 1.5 < cl.tcr(3.0) < 2.2


@pytest.fixture(scope="module")
def dice():
    years = np.arange(1850, 2025)
    E = np.linspace(2, 40, len(years))
    fit = {"speed": 0.47, "land_weight": 0.55, "ghg_scale": 1.36, "aerosol": 0.44, "ecs": 3.0}
    cc = cl.carbon_cycle(E, fit["speed"])
    T, D = cl.ebm(cl.forcing(cc["ppm"], np.full(len(years), 50.0), fit["ghg_scale"], fit["aerosol"]))
    return cl.Dice(fit, cc["boxes"], (T[-1], D[-1]), years=150)


def test_scc_falls_with_the_discount_rate(dice):
    mu = np.full(150, 0.05)
    s = dice.scc(mu, rates=(0.02, 0.03, 0.05))
    assert s["r0.02"] > s["r0.03"] > s["r0.05"] > 0
    assert s["ramsey"] > 0


def test_optimum_beats_business_as_usual(dice):
    mu = np.full(150, 0.05)
    base = dice.welfare(dice.run(mu))
    opt = dice.optimize(n_nodes=12)
    assert opt["welfare"] >= base
    assert opt["run"]["T"].max() < dice.run(mu)["T"].max()


def test_fat_tails_keep_growing():
    t = cl.tail_losses([6, 10, 20], n=50000)
    assert t["thin"][-1] - t["thin"][0] < 0.01
    assert t["fat"][-1] > 3 * t["fat"][0]


def test_club_needs_a_tariff():
    assert cl.club(tariff=0.0)["members"] == 0
    assert cl.club(tariff=0.2)["members"] == 15


def test_learning_curve_recovers_the_rate():
    q = 2.0 ** np.arange(10)
    p = 10 * q ** np.log2(0.8)
    assert cl.learning_curve(q, p)["learning_rate"] == pytest.approx(0.2, abs=1e-9)


def test_temporary_policy_redirects_innovation():
    lf = cl.directed_change(tax=0.0, subsidy=0.0)
    mix = cl.directed_change(tax=0.2, subsidy=0.5, policy_years=40)
    assert lf["clean_share"][-1] < 0.05 and mix["clean_share"][-1] > 0.9
    assert mix["research_clean"][-1] == 1.0


def test_temperature_growth_recovers_an_optimum():
    rng = np.random.default_rng(0)
    codes, years, T, G = [], [], [], []
    for c in range(40):
        base = rng.uniform(0, 28)
        for y in range(1980, 2010):
            t = base + rng.normal(0, 0.8)
            codes.append(f"C{c}")
            years.append(y)
            T.append(t)
            G.append(0.01 * t - 0.0004 * t ** 2 + rng.normal(0, 0.01))
    r = cl.temperature_growth(codes, years, T, G, trends=1)
    assert r["optimum"] == pytest.approx(12.5, abs=2.0)


def test_merit_order_and_withholding():
    cap, cost, owner = (5, 8, 10, 7, 7, 5, 3), (5, 12, 35, 45, 48, 95, 160), (0, 0, 0, 1, 1, 0, 0)
    assert cl.merit_order(cap, cost, [20, 35, 41])["price"] == [35.0, 48.0, 95.0]
    w = cl.withholding(cap, cost, owner, 1, 35.0, cap_price=250, steps=57)
    assert w["profit_none"] < w["best_profit"] and w["best_price"] > w["price_none"]
