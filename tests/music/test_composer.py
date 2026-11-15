"""Monochord's composer (Part 42): operations, derivations, the funnel, the dice game, generate and test, chains,
critics and the searcher.

    python -m pytest -q tests/music/test_composer.py
"""

import itertools
import math

import numpy as np

from explainer.music.monochord import composer as K


def test_operations_are_diatonic_and_invertible():
    m = K.MOTIVE
    assert K.pitches(K.transpose(m, 1)) == [65, 64, 62, 69]                     # F E D A: steps on the scale
    assert K.invert(K.invert(m)) == m and K.retrograde(K.retrograde(m)) == m
    assert K.pitches(K.invert(m)) == [64, 65, 67, 60]
    assert K.length(K.augment(m)) == 2 * K.length(m) and K.length(K.diminish(m)) == K.length(m) / 2
    assert K.pitches(K.embellish(m)) == [64, 62, 60, 62, 64, 65, 67]            # the fifth filled with a run


def test_derive_finds_shortest_chains():
    m = K.MOTIVE
    assert K.derive(m, K.transpose(m, 3)) == []
    assert K.derive(m, K.augment(m)) == ["augment"]
    assert len(K.derive(m, K.invert(K.retrograde(m)))) == 2
    assert K.derivation(K.transpose(K.fragment(m, 3), 2), m) is not None


def _brute(n, lo, hi, rules):
    """Every n-note melody, filtered: the dynamic programme must agree."""
    out = 0
    for mel in itertools.product(range(lo, hi + 1), repeat=n):
        ok = True
        if "start and end on C" in rules and (mel[0] % 7 or mel[-1] % 7):
            continue
        for i in range(1, n):
            s = mel[i] - mel[i - 1]
            if "no leap larger than a fifth" in rules and abs(s) > 4:
                ok = False
            if "a leap is followed by a step back" in rules and i >= 2:
                p = mel[i - 1] - mel[i - 2]
                if abs(p) >= 2 and not (abs(s) == 1 and s * p < 0):
                    ok = False
            if "no note three times running" in rules and i >= 2 and mel[i] == mel[i - 1] == mel[i - 2]:
                ok = False
        if "within an octave" in rules and max(mel) - min(mel) > 7:
            ok = False
        out += ok
    return out


def test_funnel_counts_match_brute_force():
    for k in range(len(K.FUNNEL_RULES) + 1):
        rules = K.FUNNEL_RULES[:k]
        assert K.count_funnel(5, 0, 8, rules) == _brute(5, 0, 8, rules)
    assert K.count_funnel(8) == 9252 and K.count_funnel(8, rules=()) == 15 ** 8


def test_dice_game_counts():
    T = K.dice_table()
    c = K.dice_count(T)
    assert c["naive"] == 11 ** 16 and c["per_bar"][7] == c["per_bar"][15] == 1
    assert c["distinct"] == math.prod(c["per_bar"]) < c["naive"]
    assert abs(sum(K.DICE_P.values()) - 1) < 1e-12
    h2 = -sum(p * math.log2(p) for p in K.DICE_P.values())
    assert abs(h2 - 3.274) < 0.001
    assert c["entropy_bits"] < c["uniform_bits"]                                # unequal sums waste variety


def test_illiac_lines_obey_their_rules():
    rng = np.random.default_rng(0)
    for _ in range(30):
        r = K.illiac(12, rng)
        line = r["line"]
        assert len(line) == 12 and line[0] == 60 and line[-1] % 12 == 0
        for i in range(1, 12):
            assert K._illiac_ok(line[:i], line[i], 12) is None


def test_chains_copy_more_with_memory():
    seqs = {f"t{i}": list(np.random.default_rng(i).integers(0, 8, 40)) for i in range(6)}
    m1, m4 = K.markov(list(seqs.values()), 1), K.markov(list(seqs.values()), 4)
    c1 = np.mean([K.longest_copy(K.generate(m1, 30, np.random.default_rng(s)), seqs)["run"] for s in range(20)])
    c4 = np.mean([K.longest_copy(K.generate(m4, 30, np.random.default_rng(s)), seqs)["run"] for s in range(20)])
    assert c4 > c1
    assert K.longest_copy([1, 2, 3, 9], {"a": [0, 1, 2, 3, 4]})["run"] == 3


def test_critics_and_searcher():
    chords = ["I", "IV", "V", "I", "vi", "ii", "V", "I"]
    bass = K.bass_line(chords)
    r = K.compose(K.MOTIVE, chords, bass, np.random.default_rng(0), drafts=300)
    v = r["best"]["verdict"]
    assert not v["fails"] and v["cadence"] and v["parallels"] == 0 and v["span"] <= 16
    assert sum(r["rejected"].values()) + r["survivors"] == r["drafts"]
    assert all(s["why"] in K.HARD for s in r["shown"])
    # parallel octaves are caught
    mel = [(60, 0.0, 4.0), (62, 4.0, 4.0)]
    bas = [(48, 0.0, 4.0), (50, 4.0, 4.0)]
    assert K.parallels(mel, bas) == 1
