"""The laboratory (Part 2): assignment, counterbalancing, power, and the designs run on the Pool."""

import math

import numpy as np
import pytest

from explainer.psychology import lab
from explainer.psychology.pool import Pool, TRUTH
from explainer.psychology.psyche import cueing


@pytest.fixture(scope="module")
def pool():
    return Pool()


@pytest.fixture(scope="module")
def L(pool):
    return lab.Lab(pool)


def test_randomize_is_balanced_and_random():
    rng = np.random.default_rng(1)
    g = lab.randomize(101, 2, rng)
    assert sorted(np.bincount(g)) == [50, 51]
    g3 = lab.randomize(90, 3, rng)
    assert list(np.bincount(g3)) == [30, 30, 30]
    # over many shuffles each unit is treated half the time
    share = np.mean([lab.randomize(40, 2, rng) for _ in range(4000)], axis=0)
    assert np.abs(share - 0.5).max() < 0.04


def test_randomization_balances_what_was_not_measured(pool):
    ids = pool.sample(200, seed=3)
    rng = np.random.default_rng(2)
    z = [lab.balance(pool.keen[ids], lab.randomize(200, 2, rng)) for _ in range(2000)]
    assert abs(np.mean(z)) < 0.02  # no bias in expectation
    assert abs(np.std(z) - math.sqrt(4 / 200)) < 0.02  # and the spread the shuffle predicts: sqrt(1/n1 + 1/n0)


def test_latin_square_and_williams():
    for k in (3, 4, 5, 6):
        sq = lab.latin_square(k)
        counts = lab.position_counts(sq)
        assert (counts["position"] == 1).all()
        w = lab.williams(k)
        c = lab.position_counts(w)
        per = 1 if k % 2 == 0 else 2
        assert (c["position"] == per).all()
        off = c["follows"][~np.eye(k, dtype=bool)]
        assert (off == per).all()  # every condition follows every other equally often
    # the cyclic square is not balanced for carry-over: each condition always follows the same one
    assert lab.position_counts(lab.latin_square(4))["follows"].max() == 3
    assert len(lab.all_orders(4)) == 24


def test_difference_and_randomization_test_agree():
    rng = np.random.default_rng(5)
    y = np.r_[rng.normal(0, 1, 40), rng.normal(0.7, 1, 40)]
    g = np.r_[np.zeros(40, int), np.ones(40, int)]
    d = lab.difference(y, g)
    r = lab.randomization_test(y, g, 20_000, np.random.default_rng(6))
    assert abs(d.effect - r["observed"]) < 1e-12
    assert abs(d.p - r["p"]) < 0.01
    lo, hi = d.ci()
    assert lo < d.effect < hi


def test_power_formulas():
    assert abs(lab.power_two_group(0.5, 64) - 0.80) < 0.01  # Cohen's table: d = 0.5 needs 64 per group
    assert lab.n_two_group(0.5) in (63, 64)
    # pairing with correlation rho divides the people needed by 1 / (1 - rho), and halves the groups
    assert lab.n_paired(0.5, 0.0) == lab.n_two_group(0.5)
    assert lab.n_paired(0.5, 0.9) < lab.n_two_group(0.5) / 8
    assert lab.power_paired(0.5, 64, 0.5) > lab.power_two_group(0.5, 64)
    assert abs(lab.interaction_2x2([[300, 320], [340, 360]])) < 1e-12
    assert lab.interaction_2x2([[300, 320], [340, 380]]) == 20


def test_sessions_have_the_planted_structure(pool):
    ids = pool.sample(20_000, seed=9)
    first, second = pool.session_rt(ids, 0, 20, seed=1), pool.session_rt(ids, 1, 20, seed=1)
    gain = (first - second).mean()
    assert abs(gain - TRUTH["practice_mean"] * TRUTH["practice_rate"]) < 0.4
    assert 0.85 < np.corrcoef(first, second)[0, 1] < 0.93
    # the keen are quicker and younger
    assert np.corrcoef(pool.keen[ids], pool.simple_mean(ids))[0, 1] < -0.3
    assert np.corrcoef(pool.keen[ids], pool.age[ids])[0, 1] < -0.2


def test_the_randomized_experiment_is_unbiased(L):
    null = L.replicate("randomized", 300)
    assert abs(null.mean()) < 3 * null.std() / math.sqrt(300)
    real = L.replicate("randomized", 300, effect=-8.0)
    assert abs(real.mean() + 8.0) < 3 * real.std() / math.sqrt(300)
    # its intervals cover the truth about as often as they say
    hits = [lo <= -8.0 <= hi for lo, hi in (L.randomized(effect=-8.0, study=s).ci() for s in range(300))]
    assert 0.90 < np.mean(hits) < 0.99


def test_each_unsound_design_reports_an_effect_that_is_not_there(L):
    for name in lab.THREATS:
        e = L.threat(name)
        assert e.effect < 0 and e.ci()[1] < 0, name  # "the treatment speeds people up", with the true effect zero
    # and the pretest buys precision without bias
    plain, change = L.replicate("randomized", 200), L.replicate("randomized", 200, pretest=True)
    assert change.std() < 0.6 * plain.std()


def test_hans_model_reproduces_pfungst():
    r = cueing.fit_hans()
    for name, knows, sees, dist, n, share in cueing.PFUNGST_CONDITIONS:
        assert abs(r.p_correct(knows, sees, dist) - share) < 0.16, name
    assert r.p_correct(True, True, 0.4) > 0.9 and r.p_correct(False, True, 0.4) < 0.1
    assert 3.4 < r.d0 < 4.2  # Pfungst: accurate to three and a half metres, nothing beyond four and a half
    s = cueing.simulate_session(r, [3, 5, 7, 8, 4, 10, 6, 9] * 50, knows=True, seed=2)
    assert abs(s["share"] - r.p_correct(True, True, 0.4)) < 0.05
    s = cueing.simulate_session(r, [3, 5, 7, 8, 4, 10, 6, 9] * 50, knows=False, seed=2)
    assert s["share"] < 0.15
