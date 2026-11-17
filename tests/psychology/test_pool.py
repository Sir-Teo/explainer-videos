"""The Pool's planted truths are recoverable from large samples (and so a method can be graded against them)."""

import math

import numpy as np
import pytest

from explainer.psychology import pool as pool_mod
from explainer.psychology.pool import Pool, TRUTH


@pytest.fixture(scope="module")
def pool():
    return Pool()


def test_is_seeded(pool):
    again = Pool()
    assert np.array_equal(pool.age, again.age) and np.array_equal(pool.sense, again.sense)
    assert not np.array_equal(pool.sense, Pool(seed=2).sense)
    assert np.array_equal(pool.sample(50, seed=3), pool.sample(50, seed=3))


def test_stage_medians_spreads_and_loadings(pool):
    for name, (median, s, lam) in TRUTH["rt_stages"].items():
        x = getattr(pool, name).copy()
        if name == "respond":
            x = x - TRUTH["age_slope"] * (pool.age - pool_mod.AGE_REF)
        z = np.log(x)
        assert np.median(x) == pytest.approx(median, rel=0.01)
        assert z.std() == pytest.approx(s, rel=0.02)
        assert np.corrcoef(z, pool.speed)[0, 1] == pytest.approx(lam, abs=0.01)


def test_age_slope_and_strategy_share(pool):
    slope = np.polyfit(pool.age, pool.respond, 1)[0]
    assert slope == pytest.approx(TRUTH["age_slope"], abs=0.03)
    assert pool.gonogo_decides.mean() == pytest.approx(TRUTH["gonogo_decides"], abs=0.01)


def test_subtraction_recovers_true_differences_with_enough_trials(pool):
    ids = pool.sample(300, seed=1)
    tr = pool.run_rt(ids, 400, seed=2)
    truth = pool.true_stage(ids)
    rt = {m: tr.rt[tr.condition == m].reshape(len(ids), -1).mean(axis=1) for m in "abc"}
    assert np.corrcoef(rt["b"] - rt["c"], truth["b_minus_c"])[0, 1] > 0.97
    assert np.corrcoef(rt["c"] - rt["a"], truth["c_minus_a"])[0, 1] > 0.97
    # people who decide in go/no-go show no b - c difference: Wundt's objection, planted
    dec = pool.gonogo_decides[ids]
    assert abs((rt["b"] - rt["c"])[dec].mean()) < 2.0
    assert (rt["b"] - rt["c"])[~dec].mean() == pytest.approx(truth["choose"][~dec].mean(), rel=0.05)


def test_one_persons_models_match_the_vectorized_run(pool):
    i = int(pool.sample(1, seed=9)[0])
    models = pool.rt_models(i)
    tr = pool.run_rt([i], 20_000, seed=4)
    for m in "abc":
        assert tr.mean_rt(m) == pytest.approx(models[m].mean, rel=0.01)
    assert models["b"].mean - models["a"].mean == pytest.approx(
        pool.discriminate[i] + pool.choose_bit[i] * math.log2(5))
