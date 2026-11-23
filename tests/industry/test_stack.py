"""The cost curve's arithmetic: unit costs, break-even, the merit order and its rents, Wright's law."""

import math

import pytest

from explainer.industry.works import stack as st


def test_unit_costs_and_break_even():
    u = st.unit_costs(1_000_000, 20, 50_000)
    assert u["fixed"] == pytest.approx(20) and u["total"] == pytest.approx(40)
    assert st.break_even(1_000_000, 20, 45) == pytest.approx(40_000)
    assert math.isinf(st.break_even(1_000_000, 20, 15))
    # operating leverage: 10% more volume moves profit by leverage x 10%
    lev = st.operating_leverage(1_000_000, 20, 45, 50_000)
    p0 = (45 - 20) * 50_000 - 1_000_000
    p1 = (45 - 20) * 55_000 - 1_000_000
    assert (p1 / p0 - 1) == pytest.approx(lev * 0.10)


def test_merit_order_and_rents():
    blocks = [st.Block("gas", 50, 30), st.Block("wind", 20, 0), st.Block("coal", 30, 26), st.Block("oil", 10, 150)]
    order = [b.name for b, _, _ in st.stack(blocks)]
    assert order == ["wind", "coal", "gas", "oil"]
    c = st.clear(blocks, 70)
    assert c["price"] == 30 and c["running"]["gas"] == pytest.approx(20)
    assert c["rents"]["wind"] == pytest.approx(20 * 30) and c["rents"]["coal"] == pytest.approx(30 * 4)
    assert c["rents"]["gas"] == pytest.approx(0) and "oil" not in c["running"]
    with pytest.raises(ValueError):
        st.clear(blocks, 200)


def test_wright_recovers_its_learning_rate():
    a, b = 100.0, -math.log2(0.8)  # an 80% curve: cost x 0.8 per doubling
    cum = [2 ** k for k in range(12)]
    cost = [st.wright_cost(a, b, c) for c in cum]
    f = st.wright(cum, cost)
    assert f["learning_rate"] == pytest.approx(0.2) and f["r2"] == pytest.approx(1.0)
    assert st.scale_cost(100, 1, 2) == pytest.approx(100 * 2 ** 0.6)
