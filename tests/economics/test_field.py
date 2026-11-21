"""Agora's research field (Part 67): search and selection, the caliper ratio, Andrews and Kasy's selection model,
replication and the winner's curse, forking paths, the meta-study correction, many analysts, the specification
curve, Brock and Hommes's switching cobweb and the audit of the Dials."""

import numpy as np
import pytest
from scipy import stats

from explainer.economics.agora import field as F


def test_no_search_no_filter_leaves_a_smooth_density():
    L = F.literature(n=40000, search=0.0, publish_ns=1.0, seed=1)
    assert L["published"] == 40000 and np.allclose(L["z"], L["first"])
    c = F.caliper(L["z"], width=0.2)
    assert 0.75 < c["ratio"] < 1.05                                      # slightly below one: the density falls
    assert F.selection_mle(L["z"])["beta"] > 0.9


def test_search_and_selection_make_the_bump_and_the_model_sees_it():
    L = F.literature(n=40000, search=0.3, publish_ns=0.35, seed=2)
    assert F.caliper(L["z"], width=0.2)["ratio"] > 2.5
    sel = F.selection_mle(L["z"])
    assert sel["ok"] and sel["beta"] < 0.6
    # the filter alone, without search: beta recovers the publication probability
    P = F.literature(n=60000, search=0.0, publish_ns=0.3, null_share=0.3, seed=3)
    assert F.selection_mle(P["z"])["beta"] == pytest.approx(0.3, abs=0.06)


def test_more_search_by_design_more_missing_results():
    M = F.mixed_field(n=80000, null_share=0.3, tau=2.0, publish_ns=0.35)
    beta = {d: F.selection_mle(M["z"][M["design"] == d])["beta"] for d in F.DESIGNS}
    assert beta["RCT"] > beta["DiD"] > beta["IV"]


def test_replication_and_the_winners_curse():
    M = F.mixed_field(n=80000, null_share=0.3, tau=2.0, publish_ns=0.35)
    R = F.replicate(M)
    assert 0.5 < R["rate"] < 0.7 and 0.6 < R["ratio"] < 0.8
    B = F.replicate_by_z(M)["rows"]
    rates = [r["rate"] for r in B[:4]]
    assert rates == sorted(rates)                                         # stronger evidence, better odds
    assert all(r["true_over_orig"] < 1 for r in B)                        # published effects are exaggerated
    # the closed form of the curse for a true z of 1: E[Z | Z > 1.96]
    m = 1 + stats.norm.pdf(0.96) / stats.norm.sf(0.96)
    rng = np.random.default_rng(0)
    z = 1 + rng.normal(size=400000)
    assert z[z > 1.96].mean() == pytest.approx(m, abs=0.01)


def test_forking_paths():
    fp = F.false_positive([1, 5, 20], 0.0, sims=40000, seed=1)
    for k, p in zip((1, 5, 20), fp):
        assert p == pytest.approx(1 - 0.95 ** k, abs=0.01)               # independent tests
    a, b = F.false_positive([10], 0.3, sims=20000)[0], F.false_positive([10], 0.9, sims=20000)[0]
    assert a > b > 0.05                                                    # correlation shrinks the garden


def test_the_meta_study_correction_moves_to_the_truth():
    M = F.meta_literature(theta=-0.01, tau=0.005, beta_ns=0.3, beta_pos=0.3)
    A = F.ak_meta(M["est"], M["se"])
    naive = float(np.mean(M["est"]))
    assert naive < -0.014 and abs(A["theta"] + 0.01) < 0.003
    assert A["b_ns"] == pytest.approx(0.3, abs=0.1)
    P = F.pet(M["est"], M["se"])
    assert P["mean"] == pytest.approx(naive)


def test_many_analysts_and_the_curve():
    A = F.many_analysts()
    assert len(A["rows"]) == 7 and A["n_sizes"] == 7 and A["ratio"] > 1.5
    C = F.specification_curve()
    assert C["n_specs"] == 9 * 2 ** 5
    est = [r["est"] for r in C["rows"]]
    assert est == sorted(est) and C["share_sig"] > 0.9
    D = F.analysts_data()
    for r in A["rows"]:                                                    # every team is a point on the curve
        ch = {k: r[k] for k in F.CHOICES}
        assert F.analyse(D, ch)["est"] == pytest.approx(r["est"])
        assert any(abs(c["est"] - r["est"]) < 1e-12 for c in C["rows"])


def test_brock_hommes_steady_state_cycle_and_chaos():
    b = 1.35
    n_star = (b - 1) / (2 * b)
    flip = np.log(1 / n_star - 1)
    assert flip == pytest.approx(1.904, abs=0.002)
    for beta, lo, hi in ((flip - 0.4, 1, 1), (flip + 1.0, 2, 2), (9.0, 20, 10 ** 6)):
        x = np.array(F.brock_hommes([beta], T=3000, keep=200)["x"])
        k = len(np.unique(np.round(x, 4)))
        assert lo <= k <= hi, (beta, k)
    P = F.brock_hommes_path(beta=4.0, T=400)
    assert abs(P["x"][-1] + P["x"][-2]) < 1e-6                            # a two-cycle: x, -x
    assert np.mean(P["n"][-50:]) == pytest.approx(n_star, abs=1e-6)      # at the share that makes it neutral


def test_dial_audit_counts():
    A = F.dial_audit()
    from explainer.economics import dials

    assert A["n_dials"] == len(dials.DIALS) and sum(A["statuses"].values()) == A["n_dials"]
    assert A["n_estimates"] == sum(len(d.estimates) for d in dials.DIALS.values())
    assert A["widest"][0]["spread"] >= A["widest"][-1]["spread"]
