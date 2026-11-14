"""Monochord's mathematics of rhythm and scale (Part 33)."""

from fractions import Fraction
from math import log2

from explainer.music.monochord import mathmusic as MM


def test_euclid_and_catalogue():
    assert "".join("x" if x else "." for x in MM.euclid(3, 8)) == "x..x..x."
    assert "".join("x" if x else "." for x in MM.euclid(5, 13)) == "x..x.x..x.x.."
    for k in range(1, 12):
        for n in range(k, 17):
            p = MM.euclid(k, n)
            assert sum(p) == k and len(p) == n
            st = MM.steps(p)
            assert max(st) - min(st) <= 1                                                  # maximally even
    assert all(r["rotation"] for r in MM.named_euclidean())
    assert MM.is_rotation(MM.parse("x.x.xx.x.x.x"), MM.euclid(7, 12))


def test_scales_and_fractions():
    assert MM.mos_sizes(log2(1.5), 60) == [2, 3, 5, 7, 12, 17, 29, 41, 53]
    assert MM.mos_sizes((5 ** 0.5 - 1) / 2, 60) == [2, 3, 5, 8, 13, 21, 34, 55]
    c = MM.convergents(log2(1.5), 8)
    assert Fraction(7, 12) in c and Fraction(31, 53) in c


def test_oddity_and_homometry():
    assert MM.oddity(MM.onsets(MM.euclid(5, 12)), 12) and not MM.oddity(MM.onsets(MM.euclid(7, 12)), 12)
    assert MM.homometric_pairs(4, 8) == [((0, 1, 2, 5), (0, 1, 3, 4))]
    a, b = MM.homometric_pairs(4, 8)[0]
    assert MM.interval_content(a, 8) == MM.interval_content(b, 8)


def test_tiling():
    assert MM.is_tiling((0, 1, 4, 5), (0, 2), 8)
    chk = MM.vuza_check()
    assert chk["tiles"] and not chk["A_periodic"] and not chk["B_periodic"]
    assert MM.is_periodic((0, 1, 4, 5), 8)


def test_prosody_ringing_temperaments():
    assert MM.prosody_counts(10) == [1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
    assert len(set(MM.windows(MM.YAMATA_BITS, 3))) == 8
    assert sorted(MM.de_bruijn(2, 3)) == [0, 0, 0, 0, 1, 1, 1, 1]
    bob = MM.plain_bob_minimus()
    assert len(set(bob[:-1])) == 24 and bob[-1] == bob[0]
    assert all(sum(1 for i in range(4) if abs(a.index(b_) - c.index(b_)) > 1) == 0 for a, c in zip(bob, bob[1:]) for b_ in [1])
    assert len(MM.plain_hunt(6)) == 12
    assert MM.patent_val(12) == (12, 19, 28) and MM.tempers_out((12, 19, 28), Fraction(81, 80))
    assert MM.tempers_out(MM.patent_val(31), Fraction(81, 80)) and not MM.tempers_out(MM.patent_val(53), Fraction(81, 80))
    assert [e["n"] for e in MM.best_edos(60)] == [5, 7, 9, 10, 12, 19, 22, 31, 34, 53]
    bp = MM.bohlen_pierce()
    assert abs(bp["step_cents"] - 146.3) < 0.01 and bp["ratios"]["7/5"]["steps"] == 4
