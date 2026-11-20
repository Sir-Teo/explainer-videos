"""Agora's village (Part 46): the poverty trap, the dual economy, credit, cash, risk, schools, health, history,
fertilizer, external validity and the aid budget."""

import numpy as np
import pytest

from explainer.economics.agora import village as V


def test_trap_has_two_stable_states_and_a_threshold():
    ss = V.trap_steady_states()
    assert len(ss["roots"]) == 3
    lo, th, hi = ss["low"], ss["threshold"], ss["high"]
    assert lo == pytest.approx(9.0, abs=1e-6)              # (s a_low / delta)^2
    for k in (lo, th, hi):
        assert float(V.trap_next(k)) == pytest.approx(k, abs=1e-6)
    # stability: below the threshold capital falls back to the low state, above it rises to the high one
    assert float(V.trap_next(th * 0.98)) < th * 0.98 and float(V.trap_next(th * 1.02)) > th * 1.02
    assert float(V.trap_next(lo * 1.1)) < lo * 1.1 and float(V.trap_next(hi * 0.9)) > hi * 0.9


def test_a_transfer_works_only_for_those_it_pushes_across():
    none = V.trap_households(transfer=0.0)
    big = V.trap_households(transfer=20.0)
    assert none["share_above_end"] < 0.2 < 0.9 < big["share_above_end"]
    mid = V.trap_households(transfer=10.0)
    crossed = mid["crossed"]
    end = mid["paths"][-1]
    assert np.median(end[crossed]) > mid["threshold"] > np.median(end[~crossed])


def test_lewis_wage_is_flat_until_the_turning_point():
    L = V.lewis()
    t = L["turn"]
    assert t is not None and 5 < t < 55
    assert all(w == pytest.approx(1.0) for w in L["wage"][:t])
    assert L["wage"][-1] > 1.2 and np.all(np.diff(L["emp"]) >= -1e-9)


def test_agri_gap_formula():
    rows = [{"code": "A", "agri_emp": 60.0, "agri_va": 20.0, "gdppc": 2000.0},
            {"code": "B", "agri_emp": 2.0, "agri_va": 1.0, "gdppc": 60000.0},
            {"code": "C", "agri_emp": 30.0, "agri_va": 15.0, "gdppc": 10000.0},
            {"code": "D", "agri_emp": 10.0, "agri_va": 5.0, "gdppc": 30000.0}]
    g = V.agri_gap(rows)
    assert g["gap"][0] == pytest.approx((0.8 / 0.4) / (0.2 / 0.6))
    assert g["median_poorest"] > g["median_richest"]


def test_moneylender_rate_recovers_costs():
    m = V.moneylender(cost_of_funds=0.1, default=0.2, monitoring=0.1)
    assert (1 + m["rate"]) * 0.8 == pytest.approx(1.2)
    assert V.moneylender(default=0.0, monitoring=0.0)["rate"] == pytest.approx(0.1)


def test_microcredit_gains_sit_in_the_top_tail():
    m = V.microcredit_trial()
    assert 0 < m["itt"] < 0.05 * m["mean_control"]            # modest on average
    assert m["qte"][-1] > 5 * max(abs(q) for q in m["qte"][:10])
    assert m["take_up"] < 0.5


def test_local_multiplier_matches_closed_form():
    m = V.local_multiplier(local_share=0.75, mpc=0.8, slack=1.0)
    assert m["multiplier"] == pytest.approx(2.5, abs=1e-5)
    assert m["real_multiplier"] == pytest.approx(2.5, abs=1e-5)
    assert V.local_multiplier(slack=0.5)["real_multiplier"] < V.local_multiplier()["real_multiplier"]


def test_townsend_test_recovers_the_pooling_share():
    for pooled in (0.0, 0.5, 0.85, 1.0):
        t = V.townsend(pooled=pooled)
        assert t["within"] == pytest.approx(1 - pooled, abs=1e-9)
    t = V.townsend(pooled=0.85)
    assert t["raw"] > t["within"] + 0.05                     # village shocks make the raw slope look worse


def test_index_insurance_demand_falls_with_basis_risk_and_distrust():
    covers = [V.index_insurance(basis=b)["cover"] for b in (0.0, 0.1, 0.3, 0.5)]
    assert all(a >= b for a, b in zip(covers, covers[1:])) and covers[0] > covers[-1]
    assert V.index_insurance(basis=0.0, trust=1.0, load=0.0)["cover"] == pytest.approx(1.0, abs=1e-3)
    assert V.index_insurance(trust=0.6)["cover"] < V.index_insurance(trust=1.0)["cover"]


def test_deworming_within_school_misses_the_spillover():
    d = V.deworming()
    assert d["spillover"] < 0 and d["between_schools"] < 0
    assert abs(d["within"]) < abs(d["within"] + d["spillover"])
    assert V.deworming(spill=0.0)["spillover"] == pytest.approx(0.0, abs=0.01)


def test_inpres_wald_recovers_the_return():
    r = V.inpres()
    assert r["school_per_school"] == pytest.approx(0.15, abs=0.03)
    assert r["wald"] == pytest.approx(0.08, abs=0.025)


def test_geo_rd_and_panes_rd():
    g = V.geo_rd()
    assert g["jump"] == pytest.approx(-0.25, abs=0.06)
    rng = np.random.default_rng(1)
    x = rng.uniform(-1, 1, 4000)
    y = 0.3 * (x < 0) + 0.5 * x + 0.1 * rng.standard_normal(4000)
    r = V.panes_rd(x, y)
    assert r["jump"] == pytest.approx(0.3, abs=3 * r["se"]) and r["se"] < 0.02


def test_fertilizer_commitment_matches_a_big_subsidy():
    f = V.fertilizer()
    assert 0.18 < f["base"] < 0.32
    assert f["harvest_offer"] - f["base"] == pytest.approx(0.12, abs=0.05)
    assert abs(f["planting_subsidy"] - f["harvest_offer"]) < 0.05
    assert abs(f["late_offer"] - f["base"]) < 0.02            # the same offer later does nothing
    patient = V.fertilizer(beta_lo=1.0)
    assert patient["base"] > f["base"] + 0.1 and patient["procrastinate"] == 0.0


def test_net_demand_falls_with_price_and_paying_screens_nobody():
    d = V.net_demand()
    assert np.all(np.diff(d["take"]) < 0)
    assert 1 - d["take"][-1] / d["take"][0] == pytest.approx(0.6, abs=0.06)
    assert max(d["use_if_taken"]) - min(d["use_if_taken"]) < 0.02
    s = V.net_demand(use_slope=0.3)
    assert s["use_if_taken"][-1] > s["use_if_taken"][0] + 0.1


def test_sites_prediction_reflects_heterogeneity():
    s = V.sites(tau=0.15, se=0.05)
    width = s["next_hi"] - s["next_lo"]
    assert width > 4 * 1.96 * 0.05 / np.sqrt(12)
    assert np.var(s["shrunk"]) < np.var(s["x"])


def test_aid_allocation_equalizes_marginal_benefits():
    P = {"a": (4.0, 1.5), "b": (2.0, 6.0), "c": (5.0, 1.0)}
    r = V.aid_allocate(P, budget=6.0, step=0.01)
    assert sum(r["alloc"].values()) == pytest.approx(6.0)
    marg = [P[k][0] * np.exp(-r["alloc"][k] / P[k][1]) for k in P if r["alloc"][k] > 0]
    assert max(marg) - min(marg) < 0.05
    even = sum(float(V.aid_benefit(2.0, *P[k])) for k in P)
    assert r["total"] >= even
