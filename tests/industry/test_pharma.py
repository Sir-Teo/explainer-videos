"""The Works' drug company (Part 20): the phases and their odds, the cost of one approved drug, a drug's life to its
cliff, and the option to stop before Phase III."""

import math

from explainer.industry.works import pharma as P


def test_reach_multiplies_the_phase_odds():
    r = P.reach()
    assert r[0] == 1.0
    assert math.isclose(r[-1], 0.520 * 0.289 * 0.578 * 0.906)
    assert math.isclose(r[-1], 0.0787, abs_tol=5e-4)              # BIO's likelihood of approval from Phase I, 7.9%
    assert all(a >= b for a, b in zip(r, r[1:]))


def test_cost_per_approval_carries_the_failures_and_the_wait():
    c = P.cost_per_approval()
    assert math.isclose(c["spend"], 25 + 60 * 0.52 + 250 * 0.52 * 0.289 + 5 * 0.52 * 0.289 * 0.578, rel_tol=1e-9)
    assert math.isclose(c["per_approval"], c["spend"] / c["p_approval"])
    assert 1150 < c["per_approval"] < 1250
    assert c["capitalized"] > 2 * c["per_approval"]               # the waiting doubles it
    assert math.isclose(P.cost_per_approval(rate=0.0)["capitalized"], c["per_approval"], rel_tol=1e-9)
    harder = list(P.PHASES)
    harder[1] = ("Phase II", 3.6, 60.0, 0.20)
    assert P.cost_per_approval(tuple(harder))["per_approval"] > c["per_approval"]


def test_a_drug_earns_almost_everything_before_its_cliff():
    d = P.Drug()
    s = d.sales()
    assert max(s) == d.peak and s[d.exclusivity - 1] == d.peak
    assert math.isclose(s[d.exclusivity], d.peak * P.CLIFF[0])
    assert P.Drug(exclusivity=14).npv() > d.npv() > P.Drug(exclusivity=10).npv()
    assert d.npv() > P.cost_per_approval()["capitalized"]          # the blockbuster pays for the misses


def test_the_option_to_stop_is_worth_something_only_when_one_branch_loses():
    o = P.Option().summary()
    assert o["big"] > 0 > o["small"]
    assert math.isclose(o["option"], o["flexible"] - o["commit"])
    assert math.isclose(o["option"], 0.7 * -o["small"], rel_tol=1e-9)
    rich = P.Option(small=P.Drug(peak=1500.0)).summary()
    assert rich["small"] > 0 and math.isclose(rich["option"], 0.0, abs_tol=1e-9)
