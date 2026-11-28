"""The Works' software company (Part 36)."""

import doctest

from explainer.industry.works import saas as W


def test_doctest():
    assert doctest.testmod(W).failed == 0


def test_operating_leverage_and_unit_economics():
    y = W.Saas().run()
    assert y["op_margin"][-1] > y["op_margin"][0]
    assert abs(y["revenue"][0] * 4 - (W.Saas().arr0 + y["arr"][0]) / 2) < 1
    u = W.Saas().unit_economics()
    assert 12 < u["payback_months"] < 36 and 0.4 < u["magic"] < 1.2


def test_sales_against_product():
    s = W.Saas()
    runs = {sh: s.run(extra=30e6, to_sales=sh, quarters=20) for sh in (0.0, 0.5, 1.0)}
    assert runs[0.5]["arr"][-1] > runs[0.0]["arr"][-1]
    assert runs[0.0]["cum_cash"] > runs[0.5]["cum_cash"] > runs[1.0]["cum_cash"]
    assert runs[0.0]["nrr"][-1] > runs[1.0]["nrr"][-1]
    assert s.run(raise_at=2)["arr"][-1] > s.run()["arr"][-1]


def test_cohorts_and_j_curve():
    m = W.cohorts(6)
    assert m[0, 5] > m[0, 0] and m[:, 5].sum() > m[:, 0].sum()
    j = W.j_curve()
    sw = j["switch"]
    assert j["switched"][sw] < j["licence"][sw] and j["switched"][-1] > j["licence"][-1]
