"""Monochord's machines that compose (Part 65): the chorale-tune corpus and its split, variable-order Markov models,
copy measures, constrained sampling, recombination, tokens and the judges.

    python -m pytest -q tests/music/test_machines.py
"""

import numpy as np
import pytest

from explainer.music.monochord import machines as M


@pytest.fixture(scope="module")
def corpus():
    ts = M.tunes()
    train, test = M.split(ts, 0.2, seed=0)
    return ts, train, test, M.train_grams(train)


def test_tunes_are_in_c_and_split_by_hymn_tune(corpus):
    ts, train, test, _ = corpus
    assert len(ts) > 100
    for t in ts:
        assert t["notes"][-1][2] and all(d in M.LENGTHS for _, d, _ in t["notes"])
    assert np.mean([t["notes"][-1][0] % 12 == 0 for t in ts]) > 0.85      # nearly all end on the tonic, now C
    assert not ({t["group"] for t in train} & {t["group"] for t in test})
    assert len({t["group"] for t in test}) == len(test)                  # one harmonization of each test tune


def test_markov_orders_trade_prediction_for_copying(corpus):
    _, train, test, grams = corpus
    bits = {o: M.Markov(o).fit(train).bits(test) for o in (0, 2, 8)}
    assert bits[2] < bits[0] and bits[2] < bits[8]                       # a middle order predicts best
    low = np.mean([M.copied_share(M.Markov(1).fit(train).sample(seed=s), grams, 8) for s in range(6)])
    high = np.mean([M.copied_share(M.Markov(8).fit(train).sample(seed=s), grams, 8) for s in range(6)])
    assert low < 0.1 < 0.6 < high


def test_copy_measures():
    grams = M.train_grams([{"name": "a", "notes": [(60, 4, False), (62, 4, False), (64, 4, False), (65, 4, True)]}])
    seq = [(67, 4, False), (60, 4, False), (62, 4, False), (64, 4, False), (72, 8, True)]
    lc = M.longest_copy(seq, grams)
    assert lc["length"] == 3 and lc["start"] == 1 and lc["source"] == "a"
    assert M.copied_share(seq, grams, 3) == pytest.approx(3 / 5)


def test_constrained_sampling_obeys_its_constraints(corpus):
    _, train, _, _ = corpus
    for s in range(3):
        r = M.constrained(train, length=24, seed=s)
        x = r["notes"]
        assert len(x) == 24 and x[-1][2] and x[-1][0] % 12 == 0 and x[-1][1] >= 8
        assert all((not f) or p % 12 in (0, 4, 7) for p, _, f in x[:-1])
    assert 0 < r["p_legal"] < 0.2                                        # a free draw rarely ends that way


def test_recombination_joins_by_step_from_different_tunes(corpus):
    _, train, _, _ = corpus
    r = M.recombine(train, seed=1)
    assert len({s for s, _ in r["sources"]}) == 4 and max(r["joins"]) <= 2
    assert r["notes"][-1][0] % 12 == 0


def test_tokens_round_trip(corpus):
    ts, _, _, _ = corpus
    for t in ts[:20]:
        assert M.decode(M.encode(t["notes"])) == t["notes"]
    reps = M.representations(ts)
    assert reps["split"]["vocab"] < reps["note"]["vocab"] and reps["grid"]["mean_length"] > reps["split"]["mean_length"]


def test_judges(corpus):
    _, _, test, _ = corpus
    assert M.intervals_kl(test, test) == pytest.approx(0.0, abs=1e-9)
    leaps = [[(60, 4, False), (72, 4, False), (60, 4, False), (72, 4, True)]] * 5
    assert M.intervals_kl(leaps, test) > 1.0
    assert 0.6 < M.cadence_share(test) < 0.95                            # Bach's phrases mostly end on the tonic triad
    sop, ferm, voice = M.soprano_beats([(60, 4, False), (62, 2, False), (64, 2, False), (67, 8, True)])
    assert sop == [60, 62, 67, 67] and ferm == [2, 3] and voice[-1][1] == 48
