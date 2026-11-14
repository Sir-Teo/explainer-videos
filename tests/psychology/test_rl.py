import numpy as np
import pytest

from explainer.psychology.psyche import rl


def test_td_error_moves_from_reward_to_cue_and_dips_at_omission():
    D, V = rl.td_conditioning(trials=150, omit=(149,))
    assert np.argmax(D[0]) == 20 and D[0, 20] == pytest.approx(1.0)  # first trial: surprise at the reward
    assert D[140, 4] > 0.5 and abs(D[140, 20]) < 0.05  # trained: at the cue, not at the reward
    assert D[149, 20] < -0.9  # omitted: a dip when the reward was due
    assert rl.second_order()[-1] > 0.5  # a cue followed only by a trained cue acquires value


def test_bandit_fit_recovers_parameters():
    rng = np.random.default_rng(3)
    P = np.r_[np.tile([0.8, 0.2], (150, 1)), np.tile([0.2, 0.8], (150, 1))]
    C, R, _ = rl.q_learning_bandit(P, trials=300, alpha=0.3, beta=6.0, rng=rng)
    a, b, ll = rl.fit_bandit(C, R)
    assert a == pytest.approx(0.3, abs=0.15) and b == pytest.approx(6.0, rel=0.4)
    ws, ls = rl.win_stay_lose_shift(C, R)
    assert ws > 0.7 and 0.2 < ls < 0.8


def test_exploration_policies_order_by_regret():
    reg = {p: np.mean([rl.explore_regret(p, rng=np.random.default_rng(s))[-1] for s in range(20)])
           for p in ("greedy", "thompson")}
    assert reg["thompson"] < 0.6 * reg["greedy"]


def test_latent_learning_needs_a_map():
    model = np.median([rl.latent_learning(agent="model", rng=np.random.default_rng(s))[0] for s in range(15)], 0)
    free = np.median([rl.latent_learning(agent="free", rng=np.random.default_rng(s))[0] for s in range(15)], 0)
    floor = rl.latent_learning()[1]
    assert model[11:].mean() < 1.5 * floor  # one rewarded run, then near the shortest path
    assert free[11:14].mean() > 5 * floor


def test_two_step_signatures():
    def sp(w):
        return np.mean([list(rl.stay_probabilities(rl.two_step(w, rng=np.random.default_rng(s))).values())
                        for s in range(15)], 0)
    mf, mb = sp(0.0), sp(1.0)
    # model-free: reward matters, the transition does not; model-based: reward x transition interaction
    assert mf[0] - mf[2] > 0.2 and abs(mf[0] - mf[1]) < 0.06
    assert (mb[0] - mb[1]) - (mb[2] - mb[3]) > 0.25


def test_revaluation_separates_three_learners():
    r = rl.revaluation("reward")
    t = rl.revaluation("transition")
    assert r["model_free"][0] > r["model_free"][1] and r["successor"][1] > r["successor"][0]
    assert t["successor"][0] > t["successor"][1] and t["model_based"][1] > t["model_based"][0]
    M = rl.successor_matrix(np.array([[0, 1.0], [0, 0]]), 0.5)
    assert M[0, 1] == pytest.approx(0.5)


def test_distributional_units_are_expectiles_and_drugs_cannot_be_predicted_away():
    r = np.r_[np.zeros(500), np.full(300, 5.0), np.full(200, 10.0)]
    taus = np.array([0.2, 0.5, 0.8])
    v = rl.distributional_td(r, taus)
    assert v == pytest.approx([rl.expectile(r, t) for t in taus], abs=0.25)
    assert rl.redish()[-1] == pytest.approx(1.0, abs=0.01)
    assert rl.redish(drug=0.5)[-1] > 10
