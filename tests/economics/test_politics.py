"""Agora's political economy (Part 47): collective action, rent seeking, voters, agency, the franchise, audits,
election cycles, conflict, persuasion and close elections."""

import numpy as np
import pytest

from explainer.economics.agora import politics as P


def test_olson_effort_falls_with_group_size():
    e = P.olson_effort(100.0, [1, 4, 25, 100], K=1.0)
    assert e[0] == pytest.approx(9.0) and e[1] == pytest.approx(4.0) and e[2] == pytest.approx(1.0)
    assert e[3] == 0.0 and np.all(np.diff(e) <= 0)


def test_small_group_beats_large_group():
    g = P.group_contest(n_small=10, B_small=100.0, n_large=10000, B_large=1000.0)
    assert g["p_pass"] > 0.99 and g["E_small"] > g["E_large"]
    even = P.group_contest(10, 100.0, 10, 100.0)
    assert even["p_pass"] == pytest.approx(0.5)


def test_tullock_dissipation_and_first_order_condition():
    t = P.tullock(400.0, 10)
    assert t["each"] == pytest.approx(36.0) and t["dissipated"] == pytest.approx(0.9)
    # no player gains by deviating from the symmetric equilibrium
    x = t["each"]

    def u(xi):
        return 400 * xi / (xi + 9 * x) - xi
    assert all(u(x) >= u(x + d) - 1e-9 for d in (-5, -1, 1, 5))
    g = P.tokens_game()
    assert g["best_payoff"] > 3 * g["nash_payoff"]


def test_probabilistic_voting_favours_swing_and_organized_groups():
    v = P.probabilistic_voting([0.5, 0.5], [1.0, 2.0], [1.0, 1.0])
    assert v["c"][1] == pytest.approx(2 * v["c"][0]) and sum(0.5 * c for c in v["c"]) == pytest.approx(1.0)
    w = P.probabilistic_voting([0.5, 0.5], [1.0, 1.0], [1.0, 1.0], organized=[0, 1], h=1.0)
    assert w["transfer"][1] > 0 > w["transfer"][0]


def test_rd_local_linear_recovers_a_jump():
    rng = np.random.default_rng(0)
    x = rng.uniform(-50, 50, 4000)
    y = 50 + 0.2 * x + 7.0 * (x >= 0) + 5 * rng.standard_normal(4000)
    r = P.rd_local_linear(x, y, h=20.0)
    assert r["jump"] == pytest.approx(7.0, abs=3 * r["se"]) and r["se"] < 1.0
    b = P.rd_bins(x, y, -50, 50, 5)
    assert len(b["mids"]) == 20


def test_agency_threshold_and_mayors():
    a = P.agency(W=0.2, R=1.0, delta=0.5)
    assert a["r_star"] == pytest.approx(0.5 * 1.2 - 0.2)
    assert P.agency(W=0.2, R=1.0, delta=0.9)["r_star"] == 0.0 and a["lame_duck"] == 1.0
    m = P.mayors()
    assert m["first_term"] < m["lame_duck"] and 0.15 < m["fewer"] < 0.4


def test_franchise_regions():
    assert P.franchise(0.1, 0.6)["outcome"] == "democratize"
    assert P.franchise(0.9, 0.6)["outcome"] == "promise"
    assert P.franchise(0.5, 0.3)["outcome"] == "revolution"
    f = P.franchise(0.3, 0.6)
    assert f["V_democracy"] > f["V_promise"]


def test_road_projects_audit_effect():
    effects = [P.road_projects(seed=s)["audit"] for s in range(20)]
    assert np.mean(effects) == pytest.approx(-0.08, abs=0.01)
    r = P.road_projects()
    assert abs(r["perception_corr"]) < 0.2


def test_election_cycle_lowers_unemployment_before_elections():
    c = P.election_cycle()
    u = np.array(c["u"])
    for e in c["elections"]:
        assert u[e] < u[e - 3]
    assert c["pi"][-1] > c["pi"][0]


def test_rain_conflict_iv_beats_ols():
    ivs, olss = [], []
    for s in range(30):
        r = P.rain_conflict(seed=s)
        ivs.append(r["iv"])
        olss.append(r["ols"])
    assert np.mean(ivs) == pytest.approx(-2.0, abs=0.35)
    assert abs(np.mean(olss)) < abs(np.mean(ivs))


def test_persuasion_rate():
    assert P.persuasion_rate(0.51, 0.50, 0.30, 0.20) == pytest.approx(0.2)
