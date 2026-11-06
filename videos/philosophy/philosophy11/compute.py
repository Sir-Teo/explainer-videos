"""Precompute everything in Part 11 of *Philosophy, Built* ("What Is Knowledge?").

    python -m videos.philosophy.philosophy11.compute            # everything missing (a second)

Items:
    gettier     Gettier's two cases as first-order models: valid inference, true belief, a false lemma, a nearby miss
    spheres     six scenarios (barns, the vat, the chute, the coins, the clock, the lottery): worlds by distance,
                and the sensitivity and safety verdicts for each belief
    zagzebski   Zagzebski's recipe run on her doctor: every condition short of truth survives; safety fails
    generality  one barn-judgment, five process types, five reliabilities (a toy population of 1,190 looks)
    luminosity  Williamson's cold morning: 25 moments, the margin for error, and where luminosity fails
    kk          a margin model on 31 positions: p, Kp, KKp, KKKp shrink one step at a time
    bank        Lewis's rule on the bank case, in a careless context and a careful one
    coherence   two sets of three reports, the more coherent less likely true when witnesses are good
    web         Quine's web: every minimal revision when a prediction fails
    skeptic     the closure triad as a Price List
    regress     Agrippa's regress as a Price List
"""

from __future__ import annotations

from explainer.ai.cache import Cache
from explainer.philosophy.reasoner import knowledge as Kn
from explainer.philosophy.reasoner import prop

CACHE = Cache("philosophy11")
load = CACHE.load

SKEPTIC = [("S1", r"I don't know that I'm not a brain in a vat", "~v"),
           ("S2", r"if I know I have hands, \ I know I'm not a brain in a vat", "h -> v"),
           ("S3", r"I know I have hands", "h")]
REGRESS = [("R1", r"every justified belief is justified by another belief", "a"),
           ("R2", r"no belief is justified by a circle of reasons", "b"),
           ("R3", r"no infinite chain of reasons justifies", "c"),
           ("R4", r"some of our beliefs are justified", "d")]


def compute_gettier() -> dict:
    return {n: Kn.gettier(n) for n in Kn.GETTIER_CASES}


def compute_spheres() -> dict:
    out = {}
    for name, sc in Kn.SCENARIOS.items():
        out[name] = {
            "title": sc.title, "actual": sc.actual,
            "worlds": [{"name": w, "dist": sc.dist[w], "text": sc.text.get(w, w),
                        "true": {p: sc.true(p, w) for p in sc.props},
                        "believes": {p: sc.believes(p, w) for p in sc.props}} for w in sc.worlds],
            "verdicts": Kn.verdicts(sc, list(sc.props)),
        }
    return out


def compute_zagzebski() -> dict:
    return Kn.zagzebski()


def compute_generality() -> dict:
    return {"types": Kn.generality(), "population": [list(r) for r in Kn.BARN_POPULATION],
            "total": Kn.reliability(lambda r, l: True)}


def compute_luminosity() -> dict:
    return Kn.luminosity_series()


def compute_kk() -> dict:
    sets = Kn.iterate_k(range(31), lambda w: w <= 20, margin=1, depth=3)
    return {"n": 30, "bound": 20, "sets": [sorted(s) for s in sets]}


def compute_bank() -> dict:
    poss = Kn.BANK["possibilities"]
    seen = {"open, as I saw two weeks ago"}
    careless = Kn.lewis_knows(poss, seen, {nm for nm, t, *_ in poss if not t})
    careful = Kn.lewis_knows(poss, seen, set())
    return {"possibilities": [{"name": nm, "p": t} for nm, t, *_ in poss], "careless": careless,
            "careful": careful}


def compute_coherence() -> dict:
    f = Kn.coherence_flip(xs=[i / 40 for i in range(1, 40)])
    probe = Kn.coherence_flip(xs=[0.25, 0.75])
    return {"profiles": Kn.COHERENCE_PAIR, "shogenji": f["shogenji"], "overlap": f["overlap"], "curve": f["curve"],
            "cross": f["cross"], "probe": probe["curve"]}


def compute_web() -> dict:
    return {"beliefs": Kn.WEB, "revisions": Kn.revisions()}


def _price(spec, bg=()) -> dict:
    claims = {k: prop.parse(f) for k, _, f in spec}
    res = prop.mus_mcs(claims, [prop.parse(b) for b in bg])
    return {"claims": [{"key": k, "text": t} for k, t, _ in spec], "mus": [sorted(x) for x in res["mus"]],
            "mcs": [sorted(x) for x in res["mcs"]]}


def compute_skeptic() -> dict:
    return _price(SKEPTIC)


def compute_regress() -> dict:
    # If every justified belief rests on another (a), with no circles (b) and no infinite chains (c), the chain of
    # reasons behind any justified belief has nowhere to go: so no belief is justified (not d).
    return _price(REGRESS, ["(a & b & c & d) -> F", "~F"])


ITEMS = {"gettier": compute_gettier, "spheres": compute_spheres, "zagzebski": compute_zagzebski,
         "generality": compute_generality, "luminosity": compute_luminosity, "kk": compute_kk, "bank": compute_bank,
         "coherence": compute_coherence, "web": compute_web, "skeptic": compute_skeptic, "regress": compute_regress}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
