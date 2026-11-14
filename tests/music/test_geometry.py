"""Monochord's geometry of chords (Part 32)."""

from itertools import combinations, permutations

import numpy as np
import pytest

from explainer.music.monochord import atonal as A
from explainer.music.monochord import geometry as G


def test_minimal_voice_leading():
    assert G.vl([0, 4, 7], [5, 9, 0])[0] == 3                                             # C to F: C holds, E-F, G-A
    assert G.vl([0, 4, 7], [0, 3, 7])[0] == 1
    assert G.vl([0, 4, 7], [6, 10, 1])[0] == 6                                            # the tritone-related triad
    rng = np.random.default_rng(0)
    for _ in range(50):                                                                   # against brute force with octaves
        a, b = rng.integers(0, 12, 3), rng.integers(0, 12, 3)
        brute = min(sum(abs(int(b[p[i]]) + 12 * o[i] - int(a[i])) for i in range(3))
                    for p in permutations(range(3)) for o in np.ndindex(3, 3, 3) for o in [np.array(o) - 1])
        assert G.vl(a, b)[0] == brute
    assert G.vl([0, 4, 7], [5, 9, 0], "max")[0] == 2 and G.vl([0, 4, 7], [5, 9, 0], "euclid")[0] == pytest.approx(5 ** 0.5)


def test_strip_and_triangle():
    assert G.dyad_strip(0, 4) == G.dyad_strip(16, 12) == (2.0, 4)
    assert G.dyad_strip(0, 6)[1] == 6 and G.dyad_strip(3, 3)[1] == 0
    assert len(G.dyads()) == 78
    assert G.shape([0, 4, 7]) == (3, 5, 4) and G.shape([0, 4, 8]) == (4, 4, 4)
    assert np.allclose(G.triangle_xy((4, 4, 4)), (0, 0))


def test_evenness_and_transpositions():
    assert G.evenness([0, 4, 8]) == pytest.approx(0) and G.evenness([0, 3, 6, 9]) == pytest.approx(0)
    assert G.evenness([0, 4, 7]) == pytest.approx((2 / 3) ** 0.5)
    assert G.nearest_transposition([0, 2, 4, 5, 7, 9, 11]) == (1.0, 5)
    better = [c for c in sorted({A.prime_form(x) for x in combinations(range(12), 3)}) if G.nearest_transposition(c)[0] < 3]
    assert better == [(0, 3, 7)]
    d = [0, 2, 4, 5, 7, 9, 11]
    assert [G.vl(d, [(x + 7 * k) % 12 for x in d])[0] for k in range(7)] == [0, 1, 2, 3, 4, 5, 6]


def test_optic_and_fourier():
    o = G.optic_counts(3)
    assert o["OP"] == 364 and o["OPC"] == 12 + 66 + 220 and o["OPTIC"] == 1 + 6 + 12
    assert G.optic_counts(4)["OPTIC"] == 1 + 6 + 12 + 29
    assert G.dft([0, 4, 8])[3] == pytest.approx(3) and G.dft([0, 2, 4, 6, 8, 10])[6] == pytest.approx(6)
    ch = G.dft_champions(7)
    assert ch[5]["sets"] == [A.prime_form([0, 2, 4, 5, 7, 9, 11])]
    assert G.dft([0, 4, 7])[5] == pytest.approx(G.dft([0, 3, 7])[5])                     # inversion keeps magnitudes


def test_bach_excess_is_even():
    from explainer.music.monochord import chorales as CH
    r = G.bach_voice_leading(CH.load()[:40], upper_only=True)
    assert all(v == 0 for v in r["excess_hist"][1::2])
    assert r["mean_minimal"] <= r["mean_actual"] < r["mean_shuffled"]
    assert G.semitone_path([0, 4, 7], [0, 5, 9]) == [(0, 4, 7), (0, 4, 8), (0, 4, 9), (0, 5, 9)]
