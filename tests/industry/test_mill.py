import pytest

from explainer.industry.works import mill as m


def test_mill_arithmetic():
    a = m.Mill("t", capacity=2.0, fixed=400.0, variable=500.0)
    assert a.profit(700, 1.0) == pytest.approx(0.0)
    assert a.breakeven_rate(700) == pytest.approx(1.0)
    assert a.breakeven_price(1.0) == pytest.approx(700, abs=1e-6)
    assert a.unit_cost(0.5) == pytest.approx(900)          # fixed cost spread over half the tonnes doubles


def test_minimill_costs_follow_the_price():
    mm = m.MINIMILL
    assert mm.var_cost(1000) == pytest.approx(mm.variable)
    assert mm.var_cost(600) < mm.var_cost(1000)
    assert m.INTEGRATED.var_cost(600) == m.INTEGRATED.var_cost(1000)
    assert mm.breakeven_price(1.0) < m.INTEGRATED.breakeven_price(1.0)


def test_glut_game():
    g = {s: m.glut(strategy=s)["total"] for s in ("price", "output", "bank")}
    assert all(v < 0 for v in g.values())
    assert g["price"] > g["output"]                       # for one mill, running full loses least
    ip = m.industry_glut()
    assert min(ip) < min(m.GLUT_PRICE)                    # if everyone runs full, the price falls further
    h = {s: m.glut(strategy=s, prices=ip)["total"] for s in ("price", "bank")}
    assert h["bank"] > h["price"]                         # and then banking the furnace wins
    b = m.glut(strategy="bank")
    assert any(b["banked"]) and b["rate"][b["banked"].index(True)] == 0.0


def test_kilns():
    a, b = m.Kiln("A", 0.0, 100.0), m.Kiln("B", 200.0, 100.0)
    res = m.market([a, b], [0.0, 50.0, 100.0, 150.0], haul=0.1)
    assert [r_["winner"] for r_ in res][:2] == ["A", "A"] and res[-1]["winner"] == "B"
    assert res[0]["price"] == pytest.approx(120.0)        # at A's gate the price is capped by B's delivered cost
    assert res[2]["margin"] == pytest.approx(0.0)         # halfway, the two meet
    assert m.radius(160, 100, 0.1) == pytest.approx(600)
    assert m.doubling_distance(22, 0.2) == pytest.approx(110)


def test_chemistry():
    assert m.calcination_co2(1.0) == pytest.approx(0.785, abs=0.001)    # pure lime
    assert m.hydrogen_per_tonne_iron() == pytest.approx(0.0541, abs=0.0002)
    h = m.hydrogen_cost(4.0, kwh_per_kg=50)
    assert h["kg"] == pytest.approx(54.15, abs=0.05) and h["cost"] == pytest.approx(216.6, abs=0.3)
    s = m.smelter_power(500_000, 14_000)
    assert s["twh"] == pytest.approx(7.0) and s["mw"] == pytest.approx(799, abs=1)
