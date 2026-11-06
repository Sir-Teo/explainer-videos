"""Precompute everything in Part 18 of *Philosophy, Built* ("Theories and Reality").

    python -m videos.philosophy.philosophy18.compute            # everything missing (under a minute)

Items:
    church      Church's trivialization of Ayer's verifiability criterion, checked by truth tables
    explain     the flagpole; statistical relevance; Newton's moon test
    kuhn        anomalies and a cascade of conversions (an analogy)
    copernicus  Mars from the Earth: Ptolemy's epicycle and Copernicus's orbits give the same sky
    twins       two Newtonian worlds, at rest and moving: every relative quantity the same
    duhem       a failed prediction: the minimal sets that must give way
    miracles    P(true | successful) against the base rate of true theories
    meta        Laudan's list; the realism Price List
    fresnel     Fresnel's reflection coefficients and Brewster's angle
    kinetic     temperature recovered from molecular kinetic energy
    rg          the 2D Ising model, block-spin coarse-grained below, at and above the critical point
    magnet      simulated magnetization against Onsager's exact curve
    pendulum    how false the small-angle idealization is
    risk        the best decision threshold for three costs of error
    bacon       a miniature BACON finds Kepler's third law
"""

from __future__ import annotations

from explainer.ai.cache import Cache
from explainer.philosophy.reasoner import prop
from explainer.philosophy.reasoner import science as Sc

CACHE = Cache("philosophy18")
load = CACHE.load

REALISM = [("R1", r"predictive success is good evidence of approximate truth", "a"),
           ("R2", r"many past theories were successful, \ and are now known to be false", "b"),
           ("R3", r"our best theories are in no better position than theirs were", "c")]


def compute_church() -> dict:
    return Sc.church_ayer()


def compute_explain() -> dict:
    return {"flagpole": Sc.flagpole(), "salmon": Sc.salmon_relevance(), "moon": Sc.moon_test()}


def compute_kuhn() -> dict:
    return Sc.kuhn_toy()


def compute_copernicus() -> dict:
    return Sc.copernicus()


def compute_twins() -> dict:
    return Sc.galilean_twins()


DUHEM = [("H", r"relativity: \ nothing outruns light", "h"),
         ("A1", r"the GPS clocks at both ends agree", "a1"),
         ("A2", r"the fibre-optic timing cable is sound", "a2"),
         ("A3", r"the 730 km baseline is measured right", "a3"),
         ("E", r"OPERA \ (2011): \ neutrinos arrive 60 ns early", "~o")]


def compute_duhem() -> dict:
    claims = {k: prop.parse(f) for k, _, f in DUHEM}
    res = prop.mus_mcs(claims, [prop.parse("(h & a1 & a2 & a3) -> o")])
    return {"claims": [{"key": k, "text": t} for k, t, _ in DUHEM], "mus": [sorted(x) for x in res["mus"]],
            "mcs": [sorted(x) for x in res["mcs"]]}


def compute_miracles() -> dict:
    curve = [[k / 20, Sc.no_miracles(10 ** (k / 20))] for k in range(-80, 1)]
    return {"table": Sc.no_miracles_table(), "curve": curve}


def compute_meta() -> dict:
    claims = {k: prop.parse(f) for k, _, f in REALISM}
    res = prop.mus_mcs(claims, [prop.parse("(b & c) -> ~a")])
    return {**Sc.meta_induction(), "claims": [{"key": k, "text": t} for k, t, _ in REALISM],
            "mus": [sorted(x) for x in res["mus"]], "mcs": [sorted(x) for x in res["mcs"]]}


def compute_fresnel() -> dict:
    return Sc.fresnel()


def compute_kinetic() -> dict:
    return Sc.kinetic_temperature()


def compute_rg() -> dict:
    return Sc.rg_flow(steps=300)


def compute_magnet() -> dict:
    return Sc.magnetization_curve()


def compute_pendulum() -> dict:
    return {"rows": Sc.pendulum_idealization()}


def compute_risk() -> dict:
    return {"cases": [Sc.inductive_risk(a, b) for a, b in ((1, 1), (1, 10), (10, 1))]}


def compute_bacon() -> dict:
    return {**Sc.bacon(), "planets": Sc.PLANETS}


ITEMS = {"church": compute_church, "explain": compute_explain, "kuhn": compute_kuhn,
         "copernicus": compute_copernicus, "twins": compute_twins, "duhem": compute_duhem,
         "miracles": compute_miracles, "meta": compute_meta, "fresnel": compute_fresnel, "kinetic": compute_kinetic,
         "rg": compute_rg, "magnet": compute_magnet, "pendulum": compute_pendulum, "risk": compute_risk,
         "bacon": compute_bacon}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
