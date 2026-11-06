"""Precompute everything in Part 20 of *Philosophy, Built* ("What There Is").

    python -m videos.philosophy.philosophy20.compute            # everything missing (under a minute)

Items:
    gk          the Geach-Kaplan sentence on three admiration graphs
    goodman     resemblance classes against property extensions
    census      every poset on up to six elements, up to isomorphism, tested axiom by axiom
    boolean     Boolean algebras minus bottom as models of classical extensional mereology
    counter     two failures of supplementation
    compose     how many objects among six blocks, on three answers to the special composition question
    putnam      Putnam's three individuals
    gunk        dyadic bisection
    grounding   a grounding graph: strict partial order, fundamental facts, levels; and a cycle
    many        the problem of the many, as a Price List
    family      the family TBox and four questions, decided by the ALC tableau
    ontoclean   rigidity and identity constraints on a taxonomy
    transe      a two-dimensional TransE embedding of a toy knowledge graph
    ground      Fine's truth-functional logic of ground, unfolded to the literals
    abox        instance checking on a small family ABox, with open-world answers
"""

from __future__ import annotations

from explainer.ai.cache import Cache
from explainer.philosophy.reasoner import dl as D
from explainer.philosophy.reasoner import mereo as M
from explainer.philosophy.reasoner import prop

CACHE = Cache("philosophy20")
load = CACHE.load

MANY = [
    ("M1", r"each candidate in the crowd is a cloud: \ they are equally good", prop.Var("M1")),
    ("M2", r"the candidates are many: \ they differ by a few droplets", prop.Var("M2")),
    ("M3", r"there is exactly one cloud in the sky", prop.Var("M3")),
]


def compute_gk() -> dict:
    return M.geach_kaplan_demo()


def compute_goodman() -> dict:
    return M.goodman_demo()


def compute_census() -> dict:
    return M.mereology_census(6)


def compute_boolean() -> dict:
    return {str(k): v for k, v in M.boolean_check(4).items()}


def compute_counter() -> dict:
    return M.counterexamples()


def compute_compose() -> dict:
    return M.composition_counts(2, 3)


def compute_putnam() -> dict:
    return M.putnam_world(3)


def compute_gunk() -> dict:
    return M.gunk(6)


def compute_grounding() -> dict:
    g = M.grounding_check()
    c = M.grounding_cycle_demo()
    return {**g, "cycle": {"cyclic": c["cyclic"], "irreflexive": c["irreflexive"]}}


def compute_many() -> dict:
    claims = {k: f for k, _, f in MANY}
    bg = [prop.Not(prop.And(prop.Var("M1"), prop.Var("M2"), prop.Var("M3")))]
    res = prop.mus_mcs(claims, bg)
    return {"claims": [{"key": k, "text": t} for k, t, _ in MANY], "mus": [sorted(x) for x in res["mus"]],
            "mcs": [sorted(x) for x in res["mcs"]]}


def compute_family() -> dict:
    return D.family_demo()


def compute_ontoclean() -> dict:
    return D.ontoclean()


def compute_transe() -> dict:
    return D.transe()


def compute_ground() -> dict:
    return M.ground_demo()


def compute_abox() -> dict:
    return D.abox_demo()


ITEMS = {"gk": compute_gk, "goodman": compute_goodman, "census": compute_census, "boolean": compute_boolean,
         "counter": compute_counter, "compose": compute_compose, "putnam": compute_putnam, "gunk": compute_gunk,
         "grounding": compute_grounding, "many": compute_many, "family": compute_family,
         "ontoclean": compute_ontoclean, "transe": compute_transe, "ground": compute_ground, "abox": compute_abox}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
