"""Monochord's atonal toolkit (Part 29), against the published tables."""

from explainer.music.monochord import atonal as A


def test_prime_forms_and_vectors():
    assert A.prime_form([0, 4, 7]) == A.prime_form([0, 3, 7]) == (0, 3, 7)
    assert A.prime_form([0, 4, 7, 10]) == A.prime_form([0, 3, 6, 10]) == (0, 2, 5, 8)
    assert A.prime_form([5, 11, 3, 8]) == (0, 2, 5, 8)                    # the Tristan chord
    assert A.interval_vector([0, 4, 7]) == (0, 0, 1, 1, 1, 0)
    assert A.interval_vector([0, 1, 4, 6]) == A.interval_vector([0, 1, 3, 7]) == (1, 1, 1, 1, 1, 1)
    assert A.prime_form([0, 1, 4, 6]) != A.prime_form([0, 1, 3, 7])


def test_counts_match_forte():
    sc = A.set_classes()
    assert len(sc) == 224 == A.burnside_ti()
    sizes = {k: sum(1 for p in sc if len(p) == k) for k in range(13)}
    assert [sizes[k] for k in (3, 4, 5, 6, 7, 8, 9)] == [12, 29, 38, 50, 38, 29, 12]
    z = A.z_pairs()
    assert len(z) == 23 and sum(1 for p in z if len(p[0]) == 6) == 15


def test_hexachord_theorem():
    h = A.hexachord_theorem()
    assert h["checked"] == 924 and h["holds"]
    assert A.ic_count_with_complement([0, 4, 7]) == [6, 6, 6, 6, 6, 3]


def test_rows():
    row = [0, 11, 7, 8, 3, 1, 2, 10, 6, 5, 4, 9]
    f = A.forms(row)
    assert len(f) == 48 and A.distinct_forms(row) == 48
    assert f["I0"][:3] == [0, 1, 5] and f["R0"][0] == 9
    m = A.matrix(row)
    assert m[0] == row and [r[0] for r in m] == f["I0"]
    berg = [5, 4, 0, 9, 7, 2, 8, 1, 3, 6, 10, 11]
    assert A.is_all_interval(berg)
    rows_ = A.all_interval_rows()
    assert len(rows_) == 3856 and all((r[-1] - r[0]) % 12 == 6 for r in rows_)
    assert A.all_combinatorial_hexachords() == [(0, 1, 2, 3, 4, 5), (0, 1, 2, 6, 7, 8), (0, 1, 4, 5, 8, 9), (0, 2, 3, 4, 5, 7),
                                                 (0, 2, 4, 5, 7, 9), (0, 2, 4, 6, 8, 10)]
    webern21 = [9, 6, 7, 8, 4, 5, 11, 10, 2, 1, 0, 3]                     # Webern, Op. 21: its own retrograde
    assert A.distinct_forms(webern21) == 24
    assert A.tune_row([7, 2, -2]) [:3] == [0, 7, 9]
