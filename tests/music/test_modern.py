"""Monochord's modern toolkit (Part 28)."""

from math import comb

from explainer.music.monochord import modern as MD


def test_symmetry_census():
    c = MD.census()
    assert c["classes"] == 352 and c["n_symmetric"] == 15
    assert sum(c["by_size"].values()) == 352 and c["by_size"][6] == 80
    found = {MD.messiaen_mode(s["pcs"]) for v in c["symmetric"].values() for s in v} - {None}
    assert found == set(range(1, 8))
    assert all(MD.is_union_of_cosets(s["pcs"]) for v in c["symmetric"].values() for s in v)
    assert [MD.transpositions(MD.MESSIAEN[k]) for k in range(1, 8)] == [2, 3, 4, 6, 6, 6, 6]
    assert MD.transpositions(MD.DIATONIC) == 12


def test_fits_by_chance():
    assert len(MD.collections(MD.OCTATONIC)) == 3 and len(MD.collections(MD.WHOLE_TONE)) == 2
    assert MD.fits([0, 4, 7, 6, 10, 1], MD.OCTATONIC)                       # the Petrushka chord
    assert not MD.fits([0, 2, 4, 5], MD.WHOLE_TONE)
    # 8-note sets: exactly the three octatonic collections themselves
    assert abs(MD.chance_fits(8, MD.OCTATONIC) - 3 / comb(12, 8)) < 1e-12
    assert abs(MD.chance_fits(7, MD.DIATONIC) - 12 / comb(12, 7)) < 1e-12


def test_rhythms():
    assert MD.additive(7) == [(2, 2, 3), (2, 3, 2), (3, 2, 2)]
    a = [len(MD.additive(n)) for n in range(2, 13)]
    assert all(a[i] == a[i - 2] + a[i - 3] for i in range(3, len(a)))       # Padovan
    for n in range(1, 13):
        assert MD.count_palindromes(n) == len(MD.palindromes(n))
    assert MD.off_share([0, 4, 8, 12]) == 0.0 and MD.off_share([1, 3]) == 1.0


def test_golden_and_planing():
    assert MD.golden_window(88, 1) == 4
    assert abs(MD.golden_chance(88, 1, 1) - 4 / 88) < 1e-12
    assert MD.golden_chance(88, 2, 10) > 0.5 > MD.golden_chance(88, 1, 5)
    assert MD.fibonacci(10)[-1] == 89
    p = MD.planed([(72, 0, 1), (79, 1, 1)], shape=(-3, -7))
    assert p == [[(69, 0, 1), (76, 1, 1)], [(65, 0, 1), (72, 1, 1)]]
