"""Part 10's Reasoner: Spinoza's proof graph, Leibniz's analysis, Descartes's normals, Hume, and Kant's triangle."""

from fractions import Fraction

from explainer.philosophy.reasoner import modern as Mo


def test_ethics_graph():
    g = Mo.ethics_graph()
    assert len(g["nodes"]) == 51 and len(g["edges"]) == 102
    assert Mo.forward_only(g)                      # every demonstration cites only what came before
    assert Mo.unused(g) == ["A2", "A7"]
    assert Mo.unused(Mo.ethics_graph(latin=True)) == ["A2"]
    chain = Mo.longest_chain(g)
    assert chain[0] == "D3" and chain[-1] == "P32" and len(chain) == 11
    assert Mo.ancestors(g, "P11") == {"A1", "A4", "A5", "D3", "D6", "P2", "P3", "P6", "P7"}


def test_leibniz_and_descartes():
    assert Mo.continued_fraction(Fraction(355, 113)) == [3, 7, 16]
    assert Mo.sqrt_cf(2, 6) == [1, 2, 2, 2, 2, 2]
    assert Mo.convergents([1, 2, 2, 2, 2])[-1] == Fraction(41, 29)
    n = Mo.descartes_normal()
    assert n["k"] == "3/2" and n["perpendicular"]


def test_hume_and_kant():
    assert Mo.habits("1111") == [1.0, 1.0, 1.0, 1.0]
    rules = Mo.rival_rules([1] * 8)
    assert all(r["fits"] for r in rules) and len({r["tomorrow"] for r in rules}) == 2
    ex = Mo.spherical_excess(*Mo.GAUSS_TRIANGLE.values())
    assert 14 < ex["excess_arcsec"] < 16
    assert Mo.blue_shades()["shades"][0] == "#CDE1FF"


def test_hands_and_light():
    c = Mo.chirality()
    assert not any(c["rotations_match"]) and c["flip_matches"]
    lb = Mo.light_bending()
    assert abs(lb["einstein"] - 1.75) < 0.01 and abs(lb["newton"] * 2 - lb["einstein"]) < 1e-9
    lt = Mo.least_time()
    assert abs(lt["sin_i_over_v1"] - lt["sin_r_over_v2"]) < 1e-6 and lt["time"] < lt["straight_time"]
