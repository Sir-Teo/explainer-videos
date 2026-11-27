"""The Works' waste route, landfill and regulated water company (Part 14)."""

from explainer.industry.works import route, utility


def test_density_and_split_street():
    r = route.Route()
    assert r.cost_per_stop(1.0) < r.cost_per_stop(0.5) < r.cost_per_stop(0.25)
    out = route.split_street(r, price=r.cost_per_stop(1.0) * 1.25)
    assert out[1.0]["profit"] > 0 > out[0.5]["profit"] or out[0.5]["profit"] < out[1.0]["profit"] / 2


def test_landfill_life_and_value():
    lf = route.Landfill(airspace=30, tons_per_year=1.5)
    assert abs(lf.life() - 20) < 1e-9
    assert route.Landfill(tip_fee=70).value() > lf.value() > 0
    assert route.Landfill(airspace=45).value() > lf.value()
    path = route.airspace_price(50, 15, 80)
    assert path[0] == 80 and path[14] == 80 and path[15] == 50


def test_water_and_leverage():
    w = utility.WaterCo()
    y = w.year()
    assert abs(y["ret"] - 400) < 1e-9 and y["revenue"] == w.opex + y["dep"] + y["ret"]
    assert y["next_rcv"] > w.rcv
    assert abs(utility.equity_return(0.05, 0.0, 0.03) - 0.05) < 1e-12
    # cheap debt and high gearing lift the equity return; dear debt cuts it
    assert utility.equity_return(0.05, 0.8, 0.03) > utility.equity_return(0.05, 0.55, 0.03) > 0.05
    assert utility.equity_return(0.05, 0.8, 0.07) < 0.05


def test_valley_landfill_run_it():
    g = route.run_it()
    # a long permit makes the ceiling pay; a short one shrinks every plan's value
    assert g[("ceiling", 15)]["pv"] > g[("fill", 15)]["pv"]
    assert g[("ceiling", 5)]["pv"] < g[("ceiling", 15)]["pv"]
    assert g[("fill", 15)]["full"] == 12
    lf = route.ValleyLandfill()
    assert abs(lf.play("fill", 0)["pv"] - lf.play("ceiling", 0)["pv"]) < 1e-9
    assert sum(r["tons"] for r in g[("expand", 15)]["rows"]) <= lf.airspace + lf.expansion + 1e-9
