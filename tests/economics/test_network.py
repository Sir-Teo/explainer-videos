"""Agora's economy as a network (Part 63): checked against closed forms and the truths the simulations plant."""

import numpy as np
import pytest

from explainer.economics.agora import network as N


def test_domar_weights_sum_paths_and_exceed_one():
    L = N.leontief(max_len=60)
    lam = np.array(L["domar"])
    assert np.allclose(L["partial"][-1], lam, atol=1e-8)          # the paths add up to Leontief's inverse
    assert L["sum_domar"] > 1
    assert np.allclose(lam, N.CONSUMPTION @ np.linalg.inv(np.eye(8) - N.SHARES))


def test_hulten_exact_for_cobb_douglas():
    H = N.which_failure(shock=-0.1, theta=1.0)
    for r in H["rows"]:
        assert r["loss"] == pytest.approx(r["hulten"], abs=1e-10)


def test_complements_amplify_large_losses():
    R = N.gdp_response("energy", shocks=[-0.6, -0.01, 0.0, 0.3], thetas=(0.15, 1.0, 1.5))
    h = np.array(R["hulten"])
    assert R["theta_0.15"][0] < h[0] < R["theta_1.5"][0]          # complements lose more, substitutes less
    assert R["theta_0.15"][1] == pytest.approx(h[1], rel=0.02)    # first order: Hulten
    assert R["theta_0.15"][3] < h[3]                              # and gain less from good shocks


def test_granular_and_network_volatility():
    G = N.granular()
    eq = [r["equal"] for r in G["rows"]]
    zf = [r["zipf"] for r in G["rows"]]
    assert eq[-1] == pytest.approx(0.12 / 100)
    assert zf[-1] > 10 * eq[-1]
    S = G["shapes"]
    assert S["ring"][-1] < S["ring"][0] / 5 and S["star"][-1] > 0.6 * S["star"][0]


def test_quake_fades_with_distance_and_needs_specific_links():
    Q = N.quake()
    dn = [r["loss"] for r in Q["rows"]["downstream"]]
    assert dn[0] > dn[1] > dn[2] > 0
    assert Q["total_loss"] > 2 * Q["direct_only"]
    G = N.quake(replace_specific=0.95)
    assert G["direct_specific"] < Q["direct_specific"] and G["total_loss"] < Q["total_loss"]


def test_clearing_vector_and_contagion():
    B = N.bank_example()
    assert B["payments"] == pytest.approx([5.5, 6.0, 7.0, 0.0])
    C = N.contagion(shocks=[0.5, 5.0, 30.0])
    assert C["complete"]["defaults"][1] <= C["ring"]["defaults"][1]
    assert C["complete"]["defaults"][2] == 10
    ring = np.zeros((3, 3))
    for i in range(3):
        ring[i, (i + 1) % 3] = 10
    assert N.clearing(ring, [0, 0, 0])["payments"] == pytest.approx([10, 10, 10])   # the greatest clearing vector


def test_oring_sorting_and_weak_link():
    O = N.oring()
    assert O["gain"] > 0
    assert O["one_weak"] == pytest.approx(0.6 / 0.99)


def test_weak_ties_peak_and_diffusion_order():
    assert 0 < N.weak_ties()["peak"] < 0.5
    D = N.diffusion(reps=60)
    assert D["most central"][-1] > D["at random"][-1] > D["least central"][-1]


def test_key_player_is_not_the_hub():
    K = N.key_player()
    assert K["key"] != K["most_links"]
    x = np.array(K["effort"])
    G = np.array(K["G"])
    assert np.allclose(x, 1 + K["delta"] * G @ x)


def test_formation_thresholds():
    d = 0.6
    F = N.formation(delta=d, costs=[0.1, 0.4, 0.8, 1.1])
    rows = F["rows"]
    assert [r["efficient_links"] for r in rows] == [6, 3, 3, 0]
    assert rows[1]["star_stable"] and not rows[2]["star_stable"]  # stable only while c < delta


def test_fragility_cliff_moves_with_suppliers():
    F = N.fragility()
    assert F["n_5"]["cliff"] < F["n_3"]["cliff"] < F["n_2"]["cliff"]
    assert F["n_3"]["at_cliff"] > 0.5


def test_dial_estimates_near_planted_truths():
    S = N.substitution_estimate()
    assert S["lo"] < S["theta"] < S["hi"] + 0.02
    R = N.granular_residual(reps=150)
    assert R["lo"] < R["truth"] < R["hi"]
