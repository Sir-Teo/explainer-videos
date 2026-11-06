"""Precompute everything in Part 37 of *Philosophy, Built* ("Is and Ought").

    python -m videos.philosophy.philosophy37.compute            # everything missing (seconds)

Items:
    schurz        mixed inferences in deontic logic KD, checked on every model of up to three worlds
    gibbard       norm-world pairs and the Frege-Geach modus ponens
    equilibrium   reflective equilibrium as weighted MaxSAT, and a change of weights
    debunk        Street's Darwinian dilemma as an analogy: evolved approval against fitness and truth
    tetrad        the Price List for Mackie's triad, with the PhilPapers 2020 shares (cited)
    smith         Smith's moral problem: three claims, one minimal conflict
"""

from __future__ import annotations

from explainer.ai.cache import Cache
from explainer.philosophy.reasoner import metaethics as ME
from explainer.philosophy.reasoner import prop

CACHE = Cache("philosophy37")
load = CACHE.load

TETRAD = [
    ("OBJ", r"moral claims purport to state objective facts"),
    ("NONE", r"there are no objective moral facts"),
    ("SOME", r"some moral claims are true"),
]


def compute_tetrad():
    # OBJ: a moral claim is true only if an objective moral fact makes it so; with NONE, none is true: not SOME
    claims = {k: prop.Var(k) for k, _ in TETRAD}
    bg = [prop.Not(prop.And(*[prop.Var(k) for k, _ in TETRAD]))]
    res = prop.mus_mcs(claims, bg)
    return {"claims": [{"key": k, "text": t} for k, t in TETRAD], "mus": [sorted(x) for x in res["mus"]],
            "mcs": [sorted(x) for x in res["mcs"]],
            # PhilPapers Survey 2020 (Bourget and Chalmers 2023), target faculty, accept or lean towards
            "survey": {"moral realism": 0.621, "moral anti-realism": 0.261}}


SMITH = [
    ("COG", r"moral judgments express beliefs about objective matters of fact"),
    ("INT", r"if someone judges that she ought to act, \ she is, \ other things equal, \ motivated to"),
    ("HUME", r"motivation needs a desire, \ and belief and desire are distinct existences"),
]


def compute_smith():
    # Smith, The Moral Problem (1994): COG and HUME make moral judgments beliefs that cannot motivate by themselves;
    # INT says they do motivate
    claims = {k: prop.Var(k) for k, _ in SMITH}
    bg = [prop.Not(prop.And(*[prop.Var(k) for k, _ in SMITH]))]
    res = prop.mus_mcs(claims, bg)
    return {"claims": [{"key": k, "text": t} for k, t in SMITH], "mus": [sorted(x) for x in res["mus"]],
            "mcs": [sorted(x) for x in res["mcs"]]}


ITEMS = {"schurz": ME.schurz_table, "gibbard": ME.norm_world_pairs, "equilibrium": ME.re_experiments,
         "debunk": ME.debunking, "tetrad": compute_tetrad,
         "smith": compute_smith}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
