"""Monochord's melodies: the corpus reads cleanly, and its counts show what the literature reports."""

import numpy as np
import pytest

from explainer.music.monochord import melody as M
from explainer.music.monochord import tune as TUNE

C = M.corpus()


def test_the_corpus_reads():
    assert len(C) >= 50 and sum(len(m) for m in C) > 1800
    for m in C:
        assert len(m.pitches) == len(m.beats) >= 12 and all(b > 0 for b in m.beats)
        assert M.span(m) <= 19, m.name                                         # nothing sung needs more than an octave and a half
        assert max(abs(i) for i in M.intervals(m)) <= 12, m.name
        assert m.pitches[-1] % 12 in ((0, 3, 7) if m.mode == "minor" else (0, 4, 7)), m.name
        assert m.phrase_ends and m.phrase_ends[-1] == len(m) and m.phrase_ends == sorted(set(m.phrase_ends)), m.name
    tune = next(m for m in C if m.name == M.THE_TUNE)
    assert [(d, int(b)) for d, b in zip(tune.degrees(), tune.beats)] == [(d, b) for d, b in TUNE.TUNE]      # the series' Tune, note for note
    assert M.parse("1 #4 b7 5, 1' 3*.5").pitches == [0, 6, 10, -5, 12, 4] and M.parse("1 3 5", "minor").pitches == [0, 3, 7]
    with pytest.raises(ValueError):
        M.parse("8")


def test_what_melodies_do():
    s = M.shares(C)
    assert 0.45 < s["step"] < 0.6 and s["step"] > 2 * s["leap"] * 0.9 and 0.15 < s["repeat"] < 0.3      # mostly steps
    assert 1.6 < s["mean_size"] < 2.6 and s["within_fifth"] > 0.97
    h = M.interval_histogram(C)
    assert max((k for k in h if k), key=lambda k: h[k]) == -2                      # the commonest move is a whole tone down
    assert s["steps_up"] < 0.5 and h[5] > h[-5]                                    # steps mostly fall; fourths mostly rise
    assert 9 <= np.median([M.span(m) for m in C]) <= 14                            # about an octave
    a = M.arch(C)
    assert a.argmax() in (2, 3, 4) and a[0] < 0 and a[-1] < a[0]                   # up, over, and down further than it began
    d = M.degree_counts(C)
    assert d[0] + d[2] + d[4] > 0.6 and d.argmin() == 6                            # two thirds of the time on the tonic triad
    t = M.degree_transitions(C)
    assert t[6].argmax() == 0 and t[3].argmax() == 2 and t[5].argmax() == 4       # 7 to 1, 4 to 3, 6 to 5
    assert np.allclose(t.sum(axis=1), 1)


def test_leaps_reverse_no_more_than_chance():
    real = M.post_skip(C)
    chance = [M.post_skip(M.shuffled(C, seed)) for seed in range(40)]
    mean = float(np.mean([c["all"]["share"] for c in chance]))
    assert 0.55 < real["all"]["share"] < 0.7 and mean > real["all"]["share"]       # shuffled notes reverse more often than the tunes do
    assert real["departing"]["share"] > 0.65 and real["approaching"]["share"] < 0.35       # it depends on where the leap lands
    assert np.mean([c["departing"]["share"] for c in chance]) > 0.85 and np.mean([c["approaching"]["share"] for c in chance]) < 0.35
    urn = [M.urn_melody(400, seed=s) for s in range(20)]
    assert M.post_skip(urn)["all"]["share"] > 0.6                                  # and so do notes drawn from an urn
    assert M.gap_fill(C)["share"] > 3 * np.mean([M.gap_fill(M.shuffled(C, s))["share"] for s in range(10)])


def test_the_model_of_what_comes_next():
    tune = next(m for m in C if m.name == M.THE_TUNE)
    rest = [m for m in C if m.name != M.THE_TUNE]
    model = M.NGram(2).fit(rest)
    for ctx in ((), (0,), (0, 7), (99, 98)):
        assert sum(model.distribution(ctx).values()) == pytest.approx(1.0)
    s = model.surprise(tune)
    assert s[2] > 4 and s[2] == pytest.approx(s[30])                              # the leap of a fifth is the surprise, both times
    assert s.mean() < 2.8
    rng = np.random.default_rng(0)
    noise = list(rng.choice(sorted({p for m in C for p in m.pitches}), 42))
    assert model.surprise(noise).mean() > s.mean() + 1.5
    ce = [M.cross_entropy(C, o) for o in range(4)]
    assert ce[1] < ce[0] - 0.4 and min(ce) < 2.7                                   # knowing the last note is worth half a bit and more
    assert M.entropy([p for m in C for p in m.pitches]) > ce[1]
    z = M.zipf(C)
    assert -1.6 < z["slope"] < -0.9 and z["top"][0][0] == [0, 0]
    gen = model.generate(30, seed=1)
    assert len(gen) == 30 and set(gen) <= set(model.alphabet)


def test_things_to_do_to_a_tune():
    tune = next(m for m in C if m.name == M.THE_TUNE)
    inv = M.invert(tune)
    assert inv.pitches[:7] == [0, 0, -7, -7, -8, -8, -7] and [a + b for a, b in zip(M.scale_steps(tune), M.scale_steps(inv))] == [0] * len(tune)
    assert M.invert(tune, diatonic=False).pitches[:7] == [0, 0, -7, -7, -9, -9, -7]
    back = M.retrograde(tune)
    assert back.pitches == tune.pitches[::-1] and M.retrograde(back).pitches == tune.pitches and sum(back.beats) == sum(tune.beats)
    for kind in ("passing", "neighbour", "turn"):
        o = M.ornament(tune, kind)
        assert sum(o.beats) == pytest.approx(sum(tune.beats)) and len(o) > len(tune) and len(o.phrase_ends) == len(tune.phrase_ends)
        assert all(p % 12 in M.MAJOR for p in o.pitches)
    assert M.ornament(tune, "neighbour").pitches[:4] == [0, 2, 0, 7]
    names = {m.name: m for m in C}
    seq = M.sequences(names["Kuckuck, Kuckuck"], 5)
    assert seq and seq[0]["shift"] == 1                                            # the same shape, one step higher
    assert any(x["shift"] == 0 for x in M.sequences(names["Frère Jacques"], 4))    # and an exact repeat
    assert M.contour_shape([0, 4, 7, 4, 0]) == "arch" and M.contour_shape([7, 5, 4, 2, 0]) == "falling"
