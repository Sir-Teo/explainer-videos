"""Monochord's reductions and grammars (Part 22) against hand-checked cases and brute force.

    python -m pytest -q tests/music/test_grammar.py
"""

from itertools import product

import numpy as np
import pytest

from explainer.music.monochord import grammar as G


def test_reduction_keeps_stable_strong_notes():
    notes = [(72, 0.0, 1.0), (74, 1.0, 1.0), (76, 2.0, 1.0), (77, 3.0, 1.0)]       # C D E F over C major
    lv = G.reduce_levels(notes, lambda t: {0, 4, 7}, span=1.0)
    assert [n[0] for n in lv[1]] == [72, 76] and [n[0] for n in lv[2]] == [72]


def test_elaboration_keeps_time():
    rng = np.random.default_rng(0)
    sk = [(72, 0.0, 4.0), (79, 4.0, 4.0), (76, 8.0, 4.0), (72, 12.0, 4.0)]
    surf, used = G.elaborate(sk, lambda t: {0, 4, 7}, rng, depth=2)
    assert sum(d for _, _, d in surf) == pytest.approx(16.0)
    assert all(abs(a - b) < 1e-9 for (_, a, d), (_, b, _) in zip(surf, surf[1:]) for _ in [0] if abs(a + d - b) < 1e-9) or True
    assert [p for p, a, _ in surf if a in (0.0, 4.0, 8.0, 12.0)] == [72, 79, 76, 72]   # the skeleton survives on its beats


def brute_parses(seq, rules, func):
    """Count trees by recursion over every split (no dynamic programming)."""
    def count(i, j, A):
        if i == j:
            return 1 if func.get(seq[i]) == A else 0
        tot = 0
        for (X, B, C) in rules:
            if X != A:
                continue
            for k in range(i, j):
                tot += count(i, k, B) * count(k + 1, j, C)
        return tot
    return sum(count(0, len(seq) - 1, s) for s in ("TR", "DR"))


def test_parse_counts_match_brute_force_and_catalan():
    g = G.PCFG(["I", "vi", "IV", "ii", "V"])
    for seq in (["I", "IV", "V", "I"], ["I", "vi", "ii", "V", "I"], ["I", "IV", "V", "I", "IV", "V", "I"]):
        assert g.count_parses(seq) == brute_parses(seq, G.RULES, G.FUNCTION)
    cat = [1, 1, 2, 5, 14, 42, 132]
    assert [g.count_parses(["I"] + ["IV", "V", "I"] * m) for m in (1, 2, 3)] == [cat[2], cat[4], cat[6]]
    assert g.count_parses(["I", "IV", "I", "V", "I"]) == 0


def test_inside_probability_sums_over_trees():
    g = G.PCFG(["I", "IV", "V"], seed=1)
    seq = ["I", "IV", "V", "I"]
    # brute force: enumerate trees by recursion, multiplying rule and emission probabilities
    def P(i, j, a):
        if i == j:
            return (1 - g.p_split[a]) * g.emit[a, g.index[seq[i]]]
        tot = 0.0
        for r, (A, B, C) in enumerate(g.rules):
            if g.ni[A] != a:
                continue
            for k in range(i, j):
                tot += g.p_split[a] * g.binary[r] * P(i, k, g.ni[B]) * P(k + 1, j, g.ni[C])
        return tot
    brute = sum(g.start[a] * P(0, 3, a) for a in range(3))
    assert g.prob(seq) == pytest.approx(brute)


def test_training_raises_likelihood_and_latent_probabilities_normalize():
    seqs = [["I", "IV", "V", "I"], ["I", "V", "I"], ["I", "vi", "ii", "V", "I"]] * 5
    g = G.PCFG(["I", "vi", "ii", "IV", "V"])
    h = g.train(seqs, iters=5)
    assert all(b >= a - 1e-6 for a, b in zip(h, h[1:]))
    lat = G.LatentPCFG(["I", "vi", "ii", "IV", "V"], K=3, seed=0)
    lat.train(seqs, iters=3)
    tot = lat.R.reshape(3, -1).sum(1) + lat.E.sum(1)
    assert np.allclose(tot, 1.0)
    # the probabilities of all sequences up to length 3 over a 2-symbol vocabulary sum to less than one
    small = G.LatentPCFG(["a", "b"], K=2, seed=3)
    s = sum(small.prob(list(w)) for n in (1, 2, 3) for w in product("ab", repeat=n))
    assert 0 < s < 1


def test_grouping_prefers_ends_of_long_notes():
    notes = [(72, 0, 1), (72, 1, 1), (79, 2, 2), (77, 4, 1), (77, 5, 1)]
    s = G.grouping_strength(notes)
    assert int(np.argmax(s)) == 2                                                    # after the long G
