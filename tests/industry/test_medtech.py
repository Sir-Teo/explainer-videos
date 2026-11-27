"""The Works' device maker (Part 21): selling a surgical robot against placing it for a fee per operation, and what one
robot costs a hospital over five years."""

import math

from explainer.industry.works import medtech as M


def test_buyers_are_the_hospitals_above_the_threshold():
    m = M.Market()
    s = m.sell(2.0e6)
    assert s["buyers"] == sum(1 for n in m.volumes if n >= s["threshold"])
    assert 240 < s["threshold"] < 255
    assert m.sell(3.0e6)["buyers"] < s["buyers"] < m.sell(1.0e6)["buyers"]


def test_placing_reaches_everyone_and_small_placements_lose():
    m = M.Market()
    p = m.place(1000.0)
    assert p["takers"] == len(m.volumes)
    assert p["ops"] == sum(m.volumes)
    assert p["losers"] == sum(1 for n in m.volumes if n < p["breakeven"])
    assert m.place(m.value - m.instrument + 1)["takers"] == 0       # a fee above the hospital's gain: nobody takes one


def test_the_matching_fee_equalizes_the_two():
    m = M.Market()
    f = m.fee_to_match(2.0e6)
    assert math.isclose(m.place(f)["value"], m.sell(2.0e6)["value"], rel_tol=1e-6)
    assert m.place(f - 50)["value"] < m.sell(2.0e6)["value"] < m.place(f + 50)["value"]


def test_hospital_spend_adds_up():
    h = M.hospital_spend()
    assert math.isclose(sum(h["parts"].values()), h["total"])
    assert math.isclose(sum(h["shares"].values()), 1.0)
    assert h["shares"]["instruments"] > 0.5
    assert M.hospital_spend(ops=500)["per_op"] < h["per_op"] < M.hospital_spend(ops=150)["per_op"]
