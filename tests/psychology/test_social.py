"""Psyche's social module (Part 34)."""

import numpy as np

from explainer.psychology.psyche import social as S


def test_granovetter_one_person_changes_the_crowd():
    t = np.arange(100)
    assert S.cascade_size(t) == 100
    t[1] = 2
    assert S.cascade_size(t) == 1
    c = S.cascade_curve(sds=[2, 20])
    assert c["size"][0] == 0 and c["size"][1] == 100


def test_degroot_consensus_is_the_left_eigenvector_average():
    rng = np.random.default_rng(3)
    W = rng.random((6, 6)) + np.eye(6)
    W /= W.sum(axis=1, keepdims=True)
    x0 = rng.normal(size=6)
    end = S.degroot(W, x0, steps=300)[-1]
    assert np.allclose(end, end[0]) and np.isclose(end[0], S.influence_weights(W) @ x0)


def test_bounded_confidence_leaves_more_clusters_when_eps_is_small():
    x0 = np.linspace(0, 1, 101)
    wide = S.clusters(S.bounded_confidence(x0, 0.3, 60)[-1], 1e-2)
    narrow = S.clusters(S.bounded_confidence(x0, 0.05, 60)[-1], 1e-2)
    assert wide == 1 and 6 <= narrow <= 12


def test_complex_contagion_needs_clustering():
    L = S.ring_lattice(400, 2)
    R = S.rewire(L, 1.0, seed=1)
    assert sorted(len(a) for a in R) == sorted(len(a) for a in L)
    seeds = [0, 1, 2, 3]
    assert S.contagion(L, seeds, need=2)[-1] == 400
    assert S.contagion(R, seeds, need=2)[-1] < 40
    assert len(S.contagion(R, seeds, need=1)) < len(S.contagion(L, seeds, need=1))


def test_diversity_prediction_identity_and_influence():
    rng = np.random.default_rng(0)
    x = rng.normal(3, 2, 500)
    c = S.crowd(x, 2.0)
    assert np.isclose(c["collective"], c["individual"] - c["diversity"])
    r = S.influence_rounds(rounds=6)
    assert np.allclose(r["collective"], r["collective"][0])
    assert r["diversity"][-1] < 0.05 * r["diversity"][0]
    assert r["truth_in_range"][0] and not r["truth_in_range"][-1]


def test_social_influence_makes_markets_unequal_and_unpredictable():
    soc = S.music_market(listeners=1500, worlds=4, social=0.8, seed=2)
    ind = S.music_market(listeners=1500, worlds=4, social=0.0, seed=2)
    assert soc["gini"].mean() > ind["gini"].mean() and soc["unpredictability"] > ind["unpredictability"]
    assert np.isclose(S.gini(np.ones(10)), 0) and S.gini([0, 0, 0, 1]) > 0.7


def test_bystanders_drive_and_mentions():
    b = S.bystanders([1, 2, 5, 10], p1=0.85, beta=1.0)
    assert np.isclose(b["any"][0], 0.85) and b["any"][-1] > 0.55
    assert np.all(np.diff(S.bystanders([1, 2, 5, 10], beta=1.5)["any"]) < 0)
    assert S.drive(1, 0, 2) > S.drive(1, 0, 1) and S.drive(0, 1, 2) < S.drive(0, 1, 1)
    assert np.all(np.diff(S.mentions(0.3, [1, 2, 3])) > 0)
    assert np.allclose(S.social_impact([1, 4, 9]), [1, 2, 3])


def test_inverse_planning_infers_the_goal():
    shape, walls, goals = (7, 9), [(r, 4) for r in range(1, 6)], [(0, 8), (6, 8), (3, 0)]
    up = S.goal_posterior([(3, 3), (2, 3), (1, 3), (0, 3), (0, 4)], shape, walls, goals)
    down = S.goal_posterior([(3, 3), (4, 3), (5, 3), (6, 3), (6, 4)], shape, walls, goals)
    assert np.allclose(up[0], 1 / 3) and np.allclose(up.sum(axis=1), 1)
    assert up[-1].argmax() == 0 and down[-1].argmax() == 1 and up[-1, 0] > 0.9
    assert np.all(np.diff(up[:, 0]) > 0)
    D = S.grid_distances(shape, walls, goals[1])
    assert D[3, 3] == 8 and np.isinf(D[3, 4])


def test_kelley_cube_and_dunning_kruger_from_noise():
    T = np.zeros((5, 5, 4))
    T[:, 0, :] = 1  # everyone, only with entity 0, every time: the entity
    k = S.kelley(T)
    assert np.isclose(k["shares"]["entity"], 1) and k["consensus"] == 1 and k["consistency"] == 1
    dk = S.dunning_kruger(rho=0.3, shift=15, seed=1)
    assert dk["perceived"][0] > dk["actual"][0] + 30 and dk["perceived"][3] < dk["actual"][3]
    flat = S.dunning_kruger(rho=1.0, shift=0, seed=1)
    assert np.allclose(flat["perceived"], flat["actual"], atol=2)


def test_tajfel_matrix_separates_the_strategies():
    M = S.tajfel_matrix()
    assert S.allocate(M, joint=1) == S.allocate(M, ingroup=1) == M.shape[1] - 1
    assert S.allocate(M, difference=1) == 0
    j = S.allocate(M, fairness=1)
    assert M[0, j] == M[1, j] == 13


def test_iat_reliability_limits_prediction_but_not_the_group_mean():
    stable = S.iat_study(n=300, state_sd=0.0, seed=1)
    noisy = S.iat_study(n=300, state_sd=0.12, seed=1)
    assert noisy["retest"] < stable["retest"]
    assert noisy["r_behaviour"] < stable["r_behaviour"] < 0.3
    assert noisy["t"] > 10 and noisy["mean_d"] > 0.2


def test_list_experiment_pipeline_and_illusory_correlation():
    est = [S.list_experiment(n=1000, prevalence=0.2, seed=s)["estimate"] for s in range(100)]
    assert abs(np.mean(est) - 0.2) < 0.02
    share = S.pipeline(levels=8, keep=0.5, advantage=0.1)
    assert share[0] == 0.5 and np.all(np.diff(share) < 0) and 0.3 < share[-1] < 0.4
    ic = S.illusory_correlation()
    assert ic["actual"][0] == ic["actual"][1] and ic["judged"][1] > ic["judged"][0]


def test_inequity_aversion_and_the_ultimatum_game():
    assert S.fs_threshold(0.0) == 0.0 and abs(S.fs_threshold(1.0) - 1 / 3) < 1e-12
    assert S.fs_utility(2, 8, alpha=1, beta=0) < 0 < S.fs_utility(5, 5, alpha=1, beta=0.5)
    u = S.ultimatum(np.r_[np.zeros(30), np.linspace(0.3, 1.5, 70)])
    assert 0.3 <= u["best"] <= 0.45 and u["accept"][0] == 0.3


def test_punishment_sustains_public_goods():
    plain = S.public_goods(seed=1)
    punished = S.public_goods(punishment=True, seed=1)
    assert plain[-1] < plain[0] / 3 and punished[-1] > punished[0]


def test_divorce_prediction_overfits_without_cross_validation():
    r = [S.overfit_divorce(seed=s) for s in range(30)]
    assert np.mean([x["insample"] for x in r]) > 0.85
    assert np.mean([x["loo"] for x in r]) < np.mean([x["base"] for x in r]) + 0.02


def test_stable_matching_gives_matched_couples_either_way():
    best = S.stable_matching(n=150, taste=0.5, seed=1)
    alike = S.stable_matching(n=150, taste=0.5, similar=True, seed=1)
    assert best["r"] > 0.7 and alike["r"] > 0.7
    assert len(set(best["a"].round(12))) == 150  # each person is matched exactly once
