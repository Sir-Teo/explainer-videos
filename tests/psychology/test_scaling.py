"""Psyche's scaling (Part 46)."""

import itertools

import numpy as np

from explainer.psychology.psyche import scaling as Sc


def test_thurstone_recovers_scale():
    s = np.array([0.0, 0.3, 0.8, 1.5, 2.4])
    W = Sc.simulate_pairs(s, 2000, seed=1)
    est = Sc.thurstone_scale(W) * np.sqrt(2)
    assert np.max(np.abs(est - (s - s.mean()))) < 0.12


def test_btl_mm_recovers_and_increases_likelihood():
    v = np.exp(np.array([0.0, 0.5, 1.0, -0.5]))
    rng = np.random.default_rng(2)
    W = np.zeros((4, 4))
    for i, j in itertools.combinations(range(4), 2):
        w = rng.binomial(3000, v[i] / (v[i] + v[j]))
        W[i, j], W[j, i] = w, 3000 - w
    f = Sc.btl_fit(W)
    lv = np.log(v) - np.log(v).mean()
    assert np.max(np.abs(f["log"] - lv)) < 0.06


def test_gumbel_noise_gives_logit():
    V = np.array([0.0, 0.7, -0.4])
    assert np.allclose(Sc.gumbel_choice_shares(V, n=400_000, seed=3), Sc.logit_probs(V), atol=0.004)


def test_iia_and_red_bus():
    v = np.array([1.0, 2.0, 3.0])
    r = Sc.iia_check(v, 0, 1, [(0, 1), (0, 1, 2)])
    assert abs(r[0] - r[1]) < 1e-12
    pb = Sc.normal_choice_shares([0.0, 0.0, 0.0], [[1, 0, 0], [0, 1, 0.999], [0, 0.999, 1]], n=200_000)
    assert abs(pb[0] - 0.5) < 0.01  # the car keeps half; the logit would say a third


def test_clogit_recovers():
    rng = np.random.default_rng(4)
    X = rng.normal(size=(3000, 3, 2))
    b = np.array([1.0, -0.5])
    y = (X @ b + rng.gumbel(size=(3000, 3))).argmax(1)
    f = Sc.fit_clogit(X, y)
    assert np.max(np.abs(f["b"] - b)) < 4 * f["se"].max()


def test_decoy_and_compromise():
    base = Sc.pairwise_sampler([[6, 4], [4, 6]], steps=40, n=20_000, noise=0.1)
    decoy = Sc.pairwise_sampler([[6, 4], [4, 6], [5.5, 3.5]], steps=40, n=20_000, noise=0.1)
    comp = Sc.pairwise_sampler([[6, 4], [4, 6], [8, 2]], steps=40, n=20_000, noise=0.1)
    assert abs(base[0] - 0.5) < 0.02
    assert decoy[0] > decoy[1] + 0.2  # the decoy helps the option that dominates it
    assert comp[0] > comp[1] + 0.03 and comp[0] > comp[2] + 0.03  # the middle option gains


def test_acquiescence_cancels_when_balanced():
    rng = np.random.default_rng(5)
    t1, t2, style = rng.normal(size=(3, 20000))
    pos = [1] * 6
    bal = [1, -1] * 3
    r_pos = np.corrcoef(Sc.styled_answers(t1, style, pos, seed=1).sum(1),
                        Sc.styled_answers(t2, style, pos, seed=2).sum(1))[0, 1]
    r_bal = np.corrcoef(Sc.styled_answers(t1, style, bal, seed=1).sum(1),
                        Sc.styled_answers(t2, style, bal, seed=2).sum(1))[0, 1]
    assert r_pos > 0.15 and abs(r_bal) < 0.03


def test_nps():
    r = np.array([10, 9, 8, 7, 6, 0, 10, 9, 5, 8])
    assert abs(Sc.nps(r) - 10.0) < 1e-9
    assert Sc.nps_se(np.repeat(r, 100)) > 0
