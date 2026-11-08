"""Precompute everything in Part 23 of *Philosophy, Built* ("God and the Philosophers").

    python -m videos.philosophy.philosophy23.compute            # everything missing (seconds)

Items:
    anselm      the skeleton of Proslogion II, checked for validity
    plantinga   the modal ontological argument and its mirror on every small reflexive frame
    godel       Gödel's and Scott's axioms on every finite model with up to four (world, individual) cells
    psr         van Inwagen: what could explain the big conjunctive contingent fact?
    tuning      fine-tuning likelihoods on two pieces of evidence, with a multiverse
    wager       Pascal's wager, Hájek's mixed strategies, and many gods
    petersburg  Bernoulli's St. Petersburg game: an infinite expectation, simulated
    rowe        Rowe's evidential argument as a Bayesian update
    hume        Hume on miracles: one witness and many
    battle      the sea battle in Peircean and Ockhamist branching time
    third       a countermodel to the third way's quantifier shift
    ghazali     al-Ghazālī's planetary revolutions over growing finite pasts
    dharma      Dharmakīrti's dilemma for a permanent creator, checked for consistency
    mackie      the logical problem (Part 2's six claims) and Plantinga's free-will defence, checked
    evil        the Price List for the evidential problem of evil
"""

from __future__ import annotations

from explainer.ai.cache import Cache
from explainer.philosophy.reasoner import prop
from explainer.philosophy.reasoner import theism as Th
from explainer.philosophy.reasoner.prop import parse

CACHE = Cache("philosophy23")
load = CACHE.load

MACKIE = [
    ("G", r"God exists", "G"),
    ("o", r"God is omnipotent", "G -> o"),
    ("k", r"God is omniscient", "G -> k"),
    ("g", r"God is wholly good", "G -> g"),
    ("B", r"a good, all-knowing, all-powerful being would prevent all evil", "(o & k & g) -> ~e"),
    ("e", r"there is evil", "e"),
]

FWD = [
    ("G", r"God exists, \ omnipotent, \ omniscient and wholly good", "G & o & k & g"),
    ("B2", r"a good being prevents every evil it can, \ unless preventing it loses a greater good", "(o & k & g) -> (~e | (F & D))"),
    ("F", r"a world with significantly free creatures is better than one without", "F"),
    ("D", r"transworld depravity: \ in every world God could actualize with free creatures, \ some do wrong",
     "D"),
    ("e", r"there is evil", "e"),
]

EVIDENTIAL = [
    ("G", r"God exists: \ all-powerful, \ all-knowing, \ wholly good", prop.Var("G")),
    ("B", r"a perfect being would permit no evil that serves no greater good", prop.Var("B")),
    ("S", r"the fawn's agony serves no greater good that we can see", prop.Var("S")),
    ("N", r"if an evil served a greater good, \ we would probably see it", prop.Var("N")),
]


def compute_anselm() -> dict:
    prem = [parse("U"), parse("~R -> C"), parse("~C")]
    ok, counter = prop.entails(prem, parse("R"))
    return {"valid": ok, "counter": counter, "valuations": 2 ** 3}


DHARMA = [
    ("P", r"the creator is permanent: \ unchanging at every moment", "P"),
    ("C", r"the creator is by itself a sufficient cause of the world's events", "C"),
    ("S", r"the world's events arise one after another, \ not all at once", "S"),
    ("R", r"an unchanging sufficient cause produces all its effects at once", "(P & C) -> ~S"),
]


def compute_dharma() -> dict:
    claims = {k: parse(f) for k, _, f in DHARMA}
    r = prop.mus_mcs(claims)
    return {"claims": [{"key": k, "text": t, "formula": f} for k, t, f in DHARMA], "mus": [list(m) for m in r["mus"]],
            "mcs": [list(m) for m in r["mcs"]]}


def compute_mackie() -> dict:
    claims = {k: parse(f) for k, _, f in MACKIE}
    r = prop.mus_mcs(claims)
    fwd = [parse(f) for _, _, f in FWD]
    model = prop.satisfiable_bf(fwd)
    return {"claims": [{"key": k, "text": t, "formula": f} for k, t, f in MACKIE], "mus": [list(m) for m in r["mus"]],
            "mcs": [list(m) for m in r["mcs"]],
            "fwd": [{"key": k, "text": t, "formula": f} for k, t, f in FWD], "fwd_consistent": model is not None,
            "fwd_model": {k: bool(v) for k, v in (model or {}).items()}}


def compute_evil() -> dict:
    claims = {k: f for k, _, f in EVIDENTIAL}
    bg = [prop.Not(prop.And(*[prop.Var(k) for k, _, _ in EVIDENTIAL]))]
    res = prop.mus_mcs(claims, bg)
    return {"claims": [{"key": k, "text": t} for k, t, _ in EVIDENTIAL], "mus": [sorted(x) for x in res["mus"]],
            "mcs": [sorted(x) for x in res["mcs"]]}


ITEMS = {"anselm": compute_anselm, "plantinga": lambda: Th.plantinga(3), "godel": Th.godel, "psr": Th.psr_collapse, "tuning": Th.fine_tuning,
         "wager": Th.pascal, "petersburg": Th.st_petersburg, "rowe": Th.rowe, "hume": Th.hume, "battle": Th.sea_battle, "third": Th.third_way, "ghazali": Th.revolutions, "dharma": compute_dharma, "mackie": compute_mackie,
         "evil": compute_evil}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
