"""Agora's games (Part 11), each result checked against a closed form or a second method."""

import numpy as np
import pytest

from explainer.economics.agora import games as g


def test_prisoners_dilemma_dominance_and_nash():
    A = np.array([[3, 0], [5, 1]])        # row: cooperate, defect
    B = A.T
    assert g.pure_nash(A, B) == [(1, 1)]
    ie = g.iterated_elimination(A, B)
    assert ie["rows"] == [1] and ie["cols"] == [1]


def test_support_enumeration_battle_of_the_sexes():
    A = np.array([[2, 0], [0, 1]])
    B = np.array([[1, 0], [0, 2]])
    eqs = g.support_enumeration(A, B)
    assert len(eqs) == 3
    mixed = [e for e in eqs if 0 < e["p"][0] < 1][0]
    m = g.mixed_2x2(A, B)
    assert mixed["p"][0] == pytest.approx(m["p"]) == pytest.approx(2 / 3)
    assert mixed["q"][0] == pytest.approx(m["q"]) == pytest.approx(1 / 3)


def test_matching_pennies_has_only_the_mixed_equilibrium():
    A = np.array([[1, -1], [-1, 1]])
    eqs = g.support_enumeration(A, -A)
    assert len(eqs) == 1 and np.allclose(eqs[0]["p"], 0.5) and np.allclose(eqs[0]["q"], 0.5)


def test_cognitive_hierarchy_and_level_k():
    lk = g.level_k(2 / 3, 3)
    assert np.allclose(lk, [50, 100 / 3, 200 / 9, 400 / 27])
    ch = g.cognitive_hierarchy(1.5)
    assert ch["choices"][1] == pytest.approx(100 / 3)                       # level 1 best-responds to level 0
    assert g.cognitive_hierarchy(0.01)["mean"] == pytest.approx(50, abs=0.5)  # almost all level 0
    tau = g.fit_tau(36.73)
    assert g.cognitive_hierarchy(tau)["mean"] == pytest.approx(36.73, abs=1e-6)
    assert g.fit_tau(18.9) > tau                                            # lower means need deeper thinking


def test_guessing_winner():
    w = g.guessing_winner([0, 30, 60])
    assert w["target"] == pytest.approx(20) and w["winner"] == 30


def test_backward_induction_centipede_and_entry():
    c = g.backward_induction(g.centipede(4))
    assert c["path"] == ["take"] and c["value"] == pytest.approx((0.4, 0.1))
    e = g.backward_induction(g.entry_game())
    assert e["path"] == ["enter", "accommodate"]                            # the threat to fight is empty


def test_rubinstein_and_grim():
    assert g.rubinstein(0.9)["proposer"] == pytest.approx(1 / 1.9)
    assert g.grim_threshold(5, 3, 1, 0) == pytest.approx(0.5)


def test_folk_region_contains_mutual_cooperation():
    A = np.array([[3, 0], [5, 1]])
    fr = g.folk_region(A, A.T)
    assert fr["minmax"] == (1.0, 1.0)
    from matplotlib.path import Path
    assert Path(fr["rational"]).contains_point((3, 3)) and not Path(fr["rational"]).contains_point((0.5, 4))


def test_tournament_tft_beats_alld_overall_and_noise_hurts_it():
    t = g.tournament(["ALLC", "ALLD", "TFT", "GRIM", "TF2T", "WSLS", "RANDOM", "JOSS"], repeats=3)
    s = dict(zip(t["names"], t["score"]))
    assert s["TFT"] > s["ALLD"] and s["TFT"] > s["RANDOM"]
    m0 = g.play_match("TFT", "TFT", noise=0.0)
    m1 = g.play_match("TFT", "TFT", noise=0.05, seed=3)
    assert m0["a"] == 600 and m1["a"] < 500                                 # echoes of a mistake
    mw = g.play_match("WSLS", "WSLS", noise=0.05, seed=3)
    assert mw["a"] > m1["a"]                                                # win-stay lose-shift recovers


def test_correlated_equilibrium_beats_mixed_in_chicken():
    A = np.array([[0, 7], [2, 6]])        # row: dare, chicken (Aumann's example)
    B = A.T
    ce = g.correlated_equilibrium(A, B)
    mixed = g.mixed_2x2(A, B)
    assert ce["row_payoff"] + ce["col_payoff"] > mixed["row_payoff"] + mixed["col_payoff"] + 1e-6
    assert ce["P"][0, 0] == pytest.approx(0, abs=1e-9)                      # never both dare


def test_replicator_hawk_dove_and_ess():
    V, C = 2.0, 4.0
    A = np.array([[(V - C) / 2, V], [0, V / 2]])
    x = g.replicator(A, [0.1, 0.9], T=60)
    assert x[-1][0] == pytest.approx(V / C, abs=1e-3)
    assert g.is_ess(A, [V / C, 1 - V / C]) and not g.is_ess(A, [1, 0])


def test_fictitious_play_and_regret_matching_find_rps_equilibrium():
    A = np.array([[0, -1, 1], [1, 0, -1], [-1, 1, 0]])
    fp = g.fictitious_play(A, -A, rounds=6000)
    assert np.allclose(fp["row"][-1], 1 / 3, atol=0.03)
    rm = g.regret_matching(A, -A, rounds=20000)
    assert np.allclose(rm["row"][-1], 1 / 3, atol=0.03) and rm["regret_row"] < 0.02


def test_bayes_nash():
    # row is a tough type (prior 0.3) who always wants to fight, or a weak one who wants to concede
    tough = np.array([[3, 1], [0, 0]])
    weak = np.array([[0, -1], [1, 0]])
    col_vs_tough = np.array([[0, 1], [2, 2]])
    col_vs_weak = np.array([[3, 1], [0, 2]])
    eqs = g.bayes_nash_2x2([tough, weak], [col_vs_tough, col_vs_weak], [0.3, 0.7])
    assert any(e["plan"] == (0, 1) for e in eqs)
