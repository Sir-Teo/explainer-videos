import pytest

from explainer.industry.works import cracker as c


def test_yields_close_to_one():
    for feed, y in c.YIELDS.items():
        assert sum(y.values()) == pytest.approx(1.0, abs=0.01), feed     # EIA's table sums to about a tonne
    assert c.YIELDS["ethane"]["ethylene"] > 2 * c.YIELDS["naphtha"]["ethylene"]


def test_feed_prices():
    assert c.feed_price("ethane", 3.0, 70) == pytest.approx(3.0 * 51.9 / 1.05506 + c.ETHANE_FEE)
    assert c.feed_price("naphtha", 3.0, 70) == pytest.approx(70 * 9.0 * 0.9)


def test_cost_and_shale_advantage():
    e, n = c.Cracker("ethane"), c.Cracker("naphtha")
    b = e.breakdown(3.0, 70)
    assert b["cost"] == pytest.approx(e.cost(3.0, 70))
    assert b["feed_per_t"] == pytest.approx(1 / 0.8091)
    # with cheap gas and dear oil, ethane wins by hundreds of dollars a tonne
    assert n.cost(3.0, 100) - e.cost(3.0, 100) > 500
    # with gas dear and oil cheap (2005), the gap closes
    assert abs(n.cost(8.8, 54) - e.cost(8.8, 54)) < 100


def test_play_price_set_by_dearest():
    gas = {"US": {2012: 2.8}, "EU": {2012: 12.0}, "Asia": {2012: 18.0}}
    out = c.play([2012], None, {2012: 112.0}, gas, markup=50.0)
    costs = [out[s]["cost"][2012] for s in ("Texas, ethane", "Europe, naphtha", "Asia, naphtha")]
    assert out["price"][2012] == pytest.approx(max(costs) + 50)
    assert out["Texas, ethane"]["margin"][2012] > 900


def test_gas_plant_and_haber():
    g = c.GasPlant()
    assert g.cash(0.5) == pytest.approx(g.fee + 0.8 * 40 - 0.5 * 25)      # the minimum is billed
    # whatever the customer takes, the supplier's cash never falls below the fee plus the minimum, less its costs
    assert min(g.cash(t / 10) for t in range(11)) >= g.fee + 0.8 * 40 - 1.0 * 25 - 1e-9
    h = c.haber(1.0)
    assert h["hydrogen"] == pytest.approx(0.216, abs=0.001) and h["ammonia"] == pytest.approx(1.216, abs=0.001)
