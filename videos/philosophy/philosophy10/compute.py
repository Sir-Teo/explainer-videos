"""Precompute everything in Part 10 of *Philosophy, Built* ("The Mind's Own Laws": Descartes to Kant).

    python -m videos.philosophy.philosophy10.compute            # everything missing (a few seconds)

Items:
    ethics      Spinoza, Ethics I: 51 items, 102 citations; depths, the longest chain, unused axioms, most cited
    normal      Descartes's method of normals for y = x^2 at (1, 1): the double-root condition, solved
    analysis    Leibniz: 355/113 analysed to the end; sqrt(2) never ends; its convergents
    leasttime   light from air into water: the crossing point of least time, and Snell's law there
    shades      Hume's missing shade of blue: eleven shades, one left out
    induction   eight sunrises: a Humean habit, and four rules that fit them all and disagree about tomorrow
    grid        Kant's grid: analytic or synthetic, a priori or a posteriori, with examples
    gauss       Gauss's survey triangle: its spherical excess, too small to see; the octant triangle
    hands       a flat 'hand' and its mirror image: no rotation in the plane matches them
    light       starlight grazing the sun: Einstein's deflection, the 'Newtonian' half, and Eddington's 1919 values
    empprice    the empiricist trilemma as a Price List
"""

from __future__ import annotations

from fractions import Fraction

from explainer.ai.cache import Cache
from explainer.philosophy.reasoner import modern as Mo
from explainer.philosophy.reasoner import prop

CACHE = Cache("philosophy10")
load = CACHE.load

EMP = [("E", r"all our knowledge comes from experience", "e"),
       ("N", r"we know some necessary truths: \ $7 + 5 = 12$ \ could not be otherwise", "n"),
       ("S", r"experience shows only what is, \ never what must be", "s")]


def compute_ethics() -> dict:
    g = Mo.ethics_graph()
    gl = Mo.ethics_graph(latin=True)
    return {"nodes": g["nodes"], "edges": g["edges"], "depth": Mo.depth(g), "chain": Mo.longest_chain(g),
            "unused": Mo.unused(g), "unused_latin": Mo.unused(gl), "most": Mo.most_cited(g, 6),
            "forward": Mo.forward_only(g), "ancestors_P36": len(Mo.ancestors(g, "P36")),
            "ancestors_P11": sorted(Mo.ancestors(g, "P11")),
            "statements": {f"P{k}": v for k, v in Mo.PROPOSITIONS.items()},
            "definitions": {f"D{k}": v for k, v in Mo.DEFINITIONS.items()},
            "axioms": {f"A{k}": v for k, v in Mo.AXIOMS.items()}}


def compute_normal() -> dict:
    return Mo.descartes_normal(Fraction(1))


def compute_analysis() -> dict:
    cf2 = Mo.sqrt_cf(2, 10)
    return {"pi_approx": Mo.continued_fraction(Fraction(355, 113)), "sqrt2": cf2,
            "convergents": [str(c) for c in Mo.convergents(cf2[:8])], "gcd_steps": Mo.continued_fraction(
                Fraction(1071, 462))}


def compute_leasttime() -> dict:
    return Mo.least_time()


def compute_shades() -> dict:
    return Mo.blue_shades(11, 6)


def compute_induction() -> dict:
    data = [1] * 8
    return {"habit": Mo.habits("11111111"), "rules": Mo.rival_rules(data, 12)}


def compute_grid() -> dict:
    return {"rows": Mo.GRID}


def compute_gauss() -> dict:
    return {"sides": Mo.GAUSS_TRIANGLE, **Mo.spherical_excess(*Mo.GAUSS_TRIANGLE.values()), "octant": {
        "angles": [90, 90, 90], "sum": 270}}


def compute_hands() -> dict:
    return Mo.chirality()


def compute_light() -> dict:
    return Mo.light_bending()


def compute_empprice() -> dict:
    claims = {k: prop.parse(f) for k, _, f in EMP}
    bg = [prop.parse("(e & n & s) -> F"), prop.parse("~F")]
    res = prop.mus_mcs(claims, bg)
    return {"claims": [{"key": k, "text": t} for k, t, _ in EMP], "mus": [sorted(x) for x in res["mus"]],
            "mcs": [sorted(x) for x in res["mcs"]]}


ITEMS = {"ethics": compute_ethics, "normal": compute_normal, "analysis": compute_analysis,
         "leasttime": compute_leasttime, "shades": compute_shades, "induction": compute_induction,
         "grid": compute_grid, "gauss": compute_gauss, "hands": compute_hands, "light": compute_light, "empprice": compute_empprice}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
