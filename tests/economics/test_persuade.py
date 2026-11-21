"""Agora's information and persuasion (Part 53): persuasion, cheap talk, information design, Blackwell's order,
common knowledge, global games, cascades, reputation, bargaining and relational contracts."""

import numpy as np
import pytest

from explainer.economics.agora import persuade as P


def test_prosecutor_convicts_sixty_percent():
    r = P.prosecutor(0.3, 0.5)
    assert r["optimal"] == pytest.approx(0.6)
    assert r["posterior_convict"] == pytest.approx(0.5)
    assert r["full"] == pytest.approx(0.3)
    assert r["none"] == 0.0


def test_concavification_matches_lp():
    mu = np.linspace(0, 1, 201)
    v = (mu >= 0.5).astype(float)
    cv = P.concavify(mu, v)
    assert cv[60] == pytest.approx(0.6)
    assert np.all(cv >= v - 1e-12)
    G = P.simplex_grid(2, 40)
    lp = P.persuade_lp([0.3, 0.7], G, (G[:, 0] >= 0.5).astype(float))
    assert lp["value"] == pytest.approx(0.6)


def test_persuasion_three_states():
    G = P.simplex_grid(3, 20)
    vals = (G[:, 0] >= 0.5).astype(float)
    lp = P.persuade_lp([0.2, 0.3, 0.5], G, vals)
    assert lp["value"] == pytest.approx(0.4, abs=1e-6)
    used = lp["posteriors"]
    assert np.allclose(lp["weights"] @ used, [0.2, 0.3, 0.5])


def test_cheap_talk_partitions():
    r = P.cheap_talk(0.05)
    assert r["n_max"] == 3
    assert r["bounds"][0] == 0 and r["bounds"][-1] == pytest.approx(1.0)
    assert np.all(np.diff(r["bounds"]) > 0)
    # each boundary type is indifferent between the two neighbouring actions (sender's ideal is t + b)
    for i in range(1, r["N"]):
        t = r["bounds"][i]
        assert abs(t + r["b"] - r["actions"][i - 1]) == pytest.approx(abs(t + r["b"] - r["actions"][i]))
    assert P.cheap_talk(0.05, 1)["receiver_loss"] == pytest.approx(1 / 12)
    with pytest.raises(ValueError):
        P.cheap_talk(0.2, 3)


def test_bce_full_information_bound():
    # one receiver, two states: the designer wants action 1, the receiver wants to match the state
    prior = [0.7, 0.3]
    U = [np.array([[1.0], [0.0]]), np.array([[0.0], [1.0]])]
    zero = [np.zeros((2, 1)), np.zeros((2, 1))]
    obj = [np.array([[0.0], [1.0]]), np.array([[0.0], [1.0]])]
    r = P.bce_lp(prior, [U, zero], obj)
    assert r["value"] == pytest.approx(0.6)


def test_blackwell_garbling():
    Pm = [[0.9, 0.1], [0.2, 0.8]]
    M = np.array([[0.8, 0.2], [0.3, 0.7]])
    Q = np.array(Pm) @ M
    assert P.garbling(Pm, Q)["garbling"]
    assert not P.garbling(Q, Pm)["garbling"]
    U = np.array([[1.0, 0.0], [0.0, 1.0]])
    assert P.decision_value([0.5, 0.5], Pm, U) >= P.decision_value([0.5, 0.5], Q, U) - 1e-12


def test_dialogue_reaches_agreement():
    prior = [1 / 9] * 9
    A = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
    B = [[0, 1, 2, 3], [4, 5, 6, 7], [8]]
    r = P.dialogue(prior, [2, 3], A, B, 0)
    assert r["agreed"]
    assert [h["posterior"] for h in r["history"]][:2] == pytest.approx([1 / 3, 1 / 2])


def test_email_game_unravels():
    r = P.email_game(0.1)
    assert r["z"] > 0.5
    assert r["unravels"]


def test_global_game():
    flat = P.global_game(0.4, 0.1)
    assert flat["theta"] == pytest.approx(0.6)
    one = P.global_game(0.4, 0.1, prior_mean=0.5, prior_sd=0.2)
    assert one["unique_condition"] and len(one["thetas"]) == 1
    many = P.global_game(0.4, 0.1, prior_mean=0.5, prior_sd=40 ** -0.5)
    assert not many["unique_condition"] and len(many["thetas"]) == 3


def test_cascade_chain_and_simulation():
    ch = P.cascade_chain(0.7, 40)
    assert ch["right"][-1] + ch["wrong"][-1] + ch["none"][-1] == pytest.approx(1.0)
    assert ch["right"][-1] == pytest.approx(ch["limit_right"], abs=1e-4)
    sim = P.cascade_sim(0.7, 40, runs=4000, seed=1)
    assert sim["share_right"] == pytest.approx(ch["limit_right"], abs=0.03)


def test_chain_store():
    r = P.chain_store(10, 0.05, 0.5)
    assert r["k_star"] == 4
    for row in r["rows"]:
        if row["k"] > r["k_star"]:
            assert row["enter"] == 0.0
    assert r["rows"][-1]["weak_fights"] == 0.0


def test_bargaining():
    assert P.rubinstein(0.9)["first"] == pytest.approx(1 / 1.9)
    x = np.linspace(0, 1, 1001)
    nb = P.nash_bargaining(x, 1 - x)
    assert nb["x"] == pytest.approx(0.5)
    c = P.coase_two_period(1.0, 0.4, 0.5, 0.8)
    assert c["best"]["plan"] == "screen" and c["best"]["delay"] == pytest.approx(0.5)
    assert c["commitment_profit"] > c["best"]["profit"]


def test_relational_threshold():
    r = P.relational([0.5, 2 / 3 + 1e-9, 0.9])
    assert r["delta_star"] == pytest.approx(2 / 3)
    assert r["effort"][0] < r["first_best"]
    assert r["effort"][1] == pytest.approx(r["first_best"])
