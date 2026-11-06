"""Tests for the Reasoner's quantum toolkit (Part 26)."""

import math

from explainer.philosophy.reasoner import quantum as Q


def test_born_rule_sampling():
    for r in Q.born()["rows"]:
        assert abs(r["freq0"] - r["p0"]) < 0.04


def test_bell_chsh_and_tsirelson():
    c = Q.chsh()
    assert c["local_max"] == 2 and c["local_values"] == [-2, 2]
    assert math.isclose(c["abs_S"], 2 * math.sqrt(2), abs_tol=1e-4)
    assert c["grid_best"] <= 2 * math.sqrt(2) + 1e-9
    g = Q.chsh_game(trials=8000)
    assert g["classical_best"] == 0.75
    assert abs(g["quantum_rate"] - math.cos(math.pi / 8) ** 2) < 0.02


def test_ghz_and_peres_mermin():
    gz = Q.ghz()
    assert gz["eigenvalues"] == {"XXX": 1.0, "XYY": -1.0, "YXY": -1.0, "YYX": -1.0}
    assert gz["consistent_assignments"] == 0
    pm = Q.peres_mermin()
    assert pm["commuting"] and pm["row_products"] == [1, 1, 1] and pm["column_products"] == [1, 1, -1]
    assert pm["consistent_assignments"] == 0 and pm["best_constraints_met"] == 5


def test_pbr_each_outcome_forbidden_once():
    p = Q.pbr()
    assert p["orthonormal"]
    assert sorted(i for v in p["forbidden"].values() for i in v) == [0, 1, 2, 3]
    for row in p["table"].values():
        assert math.isclose(sum(row), 1.0, abs_tol=1e-3)


def test_decoherence_bohm_grw():
    d = Q.decoherence()["rows"]
    assert d[0]["coherence"] == 0.5 and all(a["coherence"] > b["coherence"] for a, b in zip(d, d[1:]))
    assert math.isclose(d[5]["coherence"], 0.5 * math.cos(0.6) ** 5, rel_tol=1e-4)
    b = Q.bohm(n_traj=20, steps=400)
    assert b["never_cross"]
    g = Q.grw()
    assert 3.0 < g["one_particle_years"] < 3.3
    assert g["left_weight_after"] > 0.999 or g["left_weight_after"] < 0.001


def test_interference_uncertainty_and_mixtures():
    m = Q.interferometer(n_phi=37)
    assert m["visibility"] == {"1.0": 1.0, "0.5": 0.5, "0.0": 0.0}
    assert m["curves"]["1.0"][0] == 1.0 and m["curves"]["0.0"][0] == 0.5
    u = Q.uncertainty(n_random=2000)
    assert u["commutator_is_minus_2iY"] and u["robertson_slack_min"] >= 0 and u["sum_sq_min"] >= 1 - 1e-9
    assert all(math.isclose(r["sum_sq"], 1.0) for r in u["named"])
    mx = Q.mixtures()
    assert mx["all_equal_half_I"] and mx["same_locally"]
    assert mx["purity"] == {"entangled": 1.0, "mixture": 0.5} and mx["singlet_test"] == {"entangled": 1.0,
                                                                                       "mixture": 0.5}


def test_mermin_pr_box_and_cabello():
    md = Q.mermin_device(runs=4000)
    assert md["worst_agree_of_9"] == 5 and md["same_setting_rate"] == 1.0 and abs(md["quantum_rate"] - 0.5) < 0.03
    pr = Q.pr_box()
    assert pr["S"] == 4 and pr["win"] == 1
    assert set(pr["alice_marginal"].values()) == {0.5} and set(pr["bob_marginal"].values()) == {0.5}
    assert set(pr["quantum_alice_marginal"].values()) == {0.5}
    cb = Q.cabello18()
    assert cb["n_vectors"] == 18 and cb["n_bases"] == 9 and cb["orthogonal"] and cb["each_in_two"]
    assert cb["consistent_assignments"] == 0 and cb["best_bases_met"] == 8


def test_branches_and_friend():
    b = Q.branch_count()
    cf = [r["count_fraction"] for r in b["rows"]]
    bw = [r["born_weight"] for r in b["rows"]]
    assert cf == sorted(cf, reverse=True) and bw == sorted(bw) and cf[-1] < 1e-10 and bw[-1] > 0.999
    f = Q.wigner_friend()
    assert f["p_unitary"] == 1.0 and f["p_collapse"] == 0.5


def test_ghz_game_and_spekkens_toy():
    g = Q.ghz_game()
    assert g["strategies"] == 64 and g["classical_best"] == 0.75 and g["quantum_win"] == 1.0
    t = Q.spekkens()
    assert t["n_states"] == 6 and t["mixtures_equal"] and set(t["overlaps"].values()) == {4}
    for r in t["table"]:
        assert sorted(r["p"]) in ([0.5, 0.5, 1.0], [0.0, 0.5, 0.5])
