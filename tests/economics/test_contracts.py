"""Agora's incentive contracts (Part 14)."""

import numpy as np
import pytest

from explainer.economics.agora import contracts as ct


def test_team_free_riding():
    t = ct.team(18)
    assert t["e_eq"] == pytest.approx(1 / 18) and t["e_eff"] == pytest.approx(1)
    assert ct.team(1)["lost"] == pytest.approx(0)
    assert ct.team(2)["lost"] < ct.team(18)["lost"]


def test_linear_agency_optimum():
    a = ct.linear_agency(r=2, c=1, sigma=0.5)
    assert a["beta_star"] == pytest.approx(1 / 1.5)
    # the optimum beats nearby shares
    for b in (0.5, 0.8):
        assert ct.linear_agency(r=2, c=1, sigma=0.5, beta=b)["surplus"] < a["surplus"]
    assert ct.linear_agency(r=0, c=1, sigma=0.5)["beta_star"] == pytest.approx(1)


def test_two_outcome_constraints_bind():
    t = ct.two_outcome()
    ph, pl, cost, res = 0.8, 0.4, 0.3, 2.0
    eu = ph * np.log(t["w_high"]) + (1 - ph) * np.log(t["w_low"]) - cost
    assert eu == pytest.approx(res)
    assert (ph - pl) * (np.log(t["w_high"]) - np.log(t["w_low"])) == pytest.approx(cost)
    assert t["cost_hard"] > t["fb_wage"]          # risk costs money


def test_relative_performance_raises_the_share():
    r = ct.relative_performance()
    assert r["beta_relative"] > r["beta_own"] and r["surplus_relative"] > r["surplus_own"]


def test_multitask_crowds_out_the_unmeasured_task():
    m = ct.multitask(0.5)
    assert m["e1"][-1] > m["e1"][0] and m["e2"][-1] < m["e2"][0]
    assert ct.multitask(0.0)["e2"][-1] == pytest.approx(ct.multitask(0.0)["e2"][0])


def test_tournament_and_ratchet():
    t = ct.tournament([1, 2], sigma=1)
    assert t["effort"][1] == pytest.approx(2 * t["effort"][0])
    assert ct.tournament([1], sigma=2)["effort"][0] == pytest.approx(t["effort"][0] / 2)
    r = ct.ratchet(delta=0.9)
    assert r["effort_ratchet"] == pytest.approx(0.1 * r["effort_fixed_target"])


def test_shapiro_stiglitz_has_unemployment():
    s = ct.shapiro_stiglitz()
    assert 0 < s["u_eq"] < 1 and s["w_eq"] > s["full_employment_wage"]


def test_sharecrop_interior_share():
    s = ct.sharecrop()
    assert 0 < s["s_star"] < 1 and abs(s["s_grid_best"] - s["s_star"]) < 0.01
    assert s["surplus_best"] > max(s["surplus_wage"], s["surplus_rent"])


def test_career_concerns_fade_and_explicit_pay_rises():
    r = ct.career_concerns(years=30, var_ability=0.25, var_noise=1.0, delta=0.9)
    m = r["implicit"]
    assert r["first_weight"] == pytest.approx(0.2)
    assert m[-1] == 0.0 and np.all(np.diff(m) < 0)            # the last year has no future to impress
    # the first year's incentive: the discounted weights of every later year's record
    want = sum(0.9 ** s * 1 / (4 + s) for s in range(1, 30))
    assert m[0] == pytest.approx(want)
    assert np.all(np.diff(r["explicit"]) >= 0) and r["explicit"][-1] == pytest.approx(1 / 1.5)


def test_relational_contract_is_self_enforcing_only_with_patience():
    r = ct.relational([0.1, 0.25, 0.5, 0.9], c=0.1)
    assert r["effort"] == pytest.approx([2.0, 5.0, 10.0, 10.0])
    d, e = r["delta"], r["effort"]
    # at the most effort sustained, the bonus just equals the future surplus a renege throws away (below one half)
    lhs, rhs = r["bonus"], d / (1 - d) * (e - 0.1 * e ** 2 / 2)
    assert lhs[:2] == pytest.approx(rhs[:2]) and np.all(lhs <= rhs + 1e-12)
