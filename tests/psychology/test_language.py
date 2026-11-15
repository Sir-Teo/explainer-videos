"""Psyche's language module, Part 23: Zipf's law and the typing monkey, the interactive activation model, the
transitional-probability segmenter, the past-tense learner, the Kneser-Ney model and surprisal, the reading-time
regression, readability; and the Natural Stories open data."""

import numpy as np
import pytest

from explainer.psychology import opendata
from explainer.psychology.psyche import language as LG


def test_zipf_recovers_an_exponent():
    r = np.arange(1, 2001)
    counts = dict(enumerate((1e6 * r ** -1.1).astype(int) + 1))
    z = LG.zipf_fit(counts, top=1000)
    assert z["s"] == pytest.approx(1.1, abs=0.02) and z["r2"] > 0.99


def test_typing_monkey_obeys_a_power_law():
    z = LG.zipf_fit(LG.random_typing(n_chars=2_000_000, rng=np.random.default_rng(1)), top=2000)
    assert 0.9 < z["s"] < 1.5


def test_fourteen_segment_letters_are_distinct():
    shapes = {tuple(sorted(v)) for v in LG.SEGMENTS.values()}
    assert len(shapes) == 26
    f = LG.letter_features("A")
    assert f.sum() == 14 and LG.letter_features(None).sum() == 0


def test_word_superiority_in_the_interactive_activation_model():
    words = ["WORK", "WORD", "WORE", "FORK", "CORK", "WARD", "WOOD", "LORD", "FORM", "WORM", "PORK", "TORN"]
    m = LG.InteractiveActivation(words)
    pw = m.forced_choice(list("WORK"), 3, "K", "D", mask_at=16)
    pa = m.forced_choice([None, None, None, "K"], 3, "K", "D", mask_at=16)
    assert pw > pa > 0.5
    L, W = m.run(list("WORK"), 20)
    assert W[-1].argmax() == m.words.index("WORK")


def test_unit_update_respects_the_bounds():
    m = LG.InteractiveActivation(["WORK"])
    L, W = m.run(list("WORK"), 60)
    assert L.max() <= 1.0 and L.min() >= -0.2 and W.max() <= 1.0


def test_transitional_probabilities_and_segmentation():
    st = LG.syllable_stream(n=200, rng=np.random.default_rng(3))
    tp = LG.transitional_probabilities(st)
    assert tp[("tu", "pi")] == pytest.approx(1.0) and tp[("pi", "ro")] == pytest.approx(1.0)
    across = [v for (a, b), v in tp.items() if a == "ro"]
    assert all(0.15 < v < 0.55 for v in across)
    seg = LG.segment(st, tp)
    assert np.mean([w in LG.SAFFRAN_WORDS for w in seg]) > 0.95
    assert LG.word_score("golabu", tp) > LG.word_score("labubi", tp)


def test_past_tense_learner_shows_a_dip():
    irr, reg = list(LG.IRREGULAR), list(LG.REGULAR)
    r = LG.past_tense_learner([irr[:10] + reg[:2], irr[:10] + reg], epochs_per_stage=12, lr=0.3, l2=1e-3,
                              rng=np.random.default_rng(1986))
    k = int((r["stage"] == 0).sum())
    assert r["right"][k - 1] > 0.8
    assert r["right"][k:k + 4].min() < r["right"][k - 1] - 0.03
    assert r["over"][k:k + 4].max() > r["over"][k - 1]
    assert LG.regular_past("try") == "tried" and LG.regular_past("bake") == "baked"


def test_kneser_ney_is_a_distribution():
    toks = ("the cat sat on the mat . the dog sat on the log . a cat saw a dog . " * 30).split()
    lm = LG.KneserNey(toks, vocab_size=50)
    vocab = sorted(lm.vocab | {"<unk>"})
    total = sum(lm.prob("the", "cat", w) for w in vocab)
    assert total == pytest.approx(1.0, abs=0.02)
    s = lm.surprisal("the cat sat on the mat".split())
    assert s.shape == (6,) and np.all(s > 0)
    assert lm.prob("the", "cat", "sat") > lm.prob("the", "cat", "log")


def test_rt_regression_recovers_slopes():
    rng = np.random.default_rng(0)
    n = 4000
    s, L, f = rng.gamma(3, 2, n), rng.integers(1, 12, n).astype(float), rng.normal(3, 1, n)
    prev = rng.gamma(3, 2, n)
    rt = 300 + 2.0 * s + 3.0 * L - 5.0 * f + 1.0 * prev + rng.normal(0, 10, n)
    r = LG.rt_regression(rt, s, L, f, prev)
    assert np.allclose(r["coef"][1:], [2.0, 3.0, -5.0, 1.0], atol=0.3)


def test_cohort_shrinks():
    lex = ["trespass", "trespassed", "tree", "trend", "trial", "cat", "candle", "can"]
    c = LG.cohort("trespass", lex)
    assert c[0] == 5 and c[-1] == 2 and all(a >= b for a, b in zip(c, c[1:]))


def test_flesch_orders_texts():
    easy = LG.flesch("The cat sat. The dog ran. We had fun.")
    hard = LG.flesch("Notwithstanding considerable methodological heterogeneity, the investigators "
                     "nevertheless characterized the phenomenon comprehensively.")
    assert easy["score"] > hard["score"]
    assert LG.syllable_count("table") == 2 and LG.syllable_count("cat") == 1


def test_natural_stories_open_data():
    if not opendata.available("naturalstories_words"):
        pytest.skip("the Natural Stories data could not be fetched")
    ns = opendata.natural_stories()
    assert len(ns["word"]) == 10256 and set(np.unique(ns["story"])) == set(range(1, 11))
    assert 250 < np.median(ns["rt"]) < 450 and np.median(ns["n"]) > 50
    assert ns["word"][0] == "If"
