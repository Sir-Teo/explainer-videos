"""Precompute everything in Part 21 of *Philosophy, Built* ("Identity and Persistence").

    python -m videos.philosophy.philosophy21.compute            # everything missing (seconds)

Items:
    discern     Quine's grades of discernibility on Black's spheres, the singlet state and three controls
    reid        Reid's brave officer: memory, its ancestral, and Locke's contradiction
    theseus     the ship of Theseus, repaired and rebuilt, plank by plank
    evans       vague identity over precisifications, with rigid and non-rigid names
    fission     a branching continuity graph and its two worms
    memory      connectedness fading and continuity holding over a toy lifetime
    fissionpl   the fission Price List
    intrinsics  the temporary intrinsics Price List
    pyid        `is' and `==' in Python: numerical identity and equality
    modal       the statue and the lump across five scenarios
    drift       a weight vector drifting through forty updates: connectedness and continuity
"""

from __future__ import annotations

from explainer.ai.cache import Cache
from explainer.philosophy.reasoner import persist as Pe
from explainer.philosophy.reasoner import prop

CACHE = Cache("philosophy21")
load = CACHE.load

FISSION = [
    ("F1", r"I survive teleportation, \ and would survive one branch of a fission", prop.Var("F1")),
    ("F2", r"identity is transitive \ (and one-one)", prop.Var("F2")),
    ("F3", r"the two branches are not identical to each other", prop.Var("F3")),
    ("F4", r"each branch has an equal claim to be me", prop.Var("F4")),
]


INTRINSICS = [
    ("I1", r"shapes are intrinsic: \ how a thing is in itself", prop.Var("I1")),
    ("I2", r"I endure: \ wholly present when I sit and when I stand", prop.Var("I2")),
    ("I3", r"I am bent, \ and I am straight", prop.Var("I3")),
    ("I4", r"nothing has both shapes simpliciter", prop.Var("I4")),
]


def compute_intrinsics() -> dict:
    claims = {k: f for k, _, f in INTRINSICS}
    bg = [prop.Not(prop.And(*[prop.Var(k) for k, _, _ in INTRINSICS]))]
    res = prop.mus_mcs(claims, bg)
    return {"claims": [{"key": k, "text": t} for k, t, _ in INTRINSICS], "mus": [sorted(x) for x in res["mus"]],
            "mcs": [sorted(x) for x in res["mcs"]]}


def compute_pyid() -> dict:
    return Pe.python_identity()


def compute_modal() -> dict:
    return Pe.modal_profiles()


def compute_drift() -> dict:
    return Pe.weight_drift()


def compute_discern() -> dict:
    return Pe.black_spheres()


def compute_reid() -> dict:
    return Pe.reid()


def compute_theseus() -> dict:
    return Pe.theseus(40)


def compute_evans() -> dict:
    return Pe.evans()


def compute_fission() -> dict:
    return Pe.fission()


def compute_memory() -> dict:
    return Pe.memory_chain()


def compute_fissionpl() -> dict:
    claims = {k: f for k, _, f in FISSION}
    bg = [prop.Not(prop.And(*[prop.Var(k) for k, _, _ in FISSION]))]
    res = prop.mus_mcs(claims, bg)
    return {"claims": [{"key": k, "text": t} for k, t, _ in FISSION], "mus": [sorted(x) for x in res["mus"]],
            "mcs": [sorted(x) for x in res["mcs"]]}


ITEMS = {"discern": compute_discern, "reid": compute_reid, "theseus": compute_theseus, "evans": compute_evans,
         "fission": compute_fission, "memory": compute_memory, "fissionpl": compute_fissionpl,
         "intrinsics": compute_intrinsics, "pyid": compute_pyid, "modal": compute_modal,
         "drift": compute_drift}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
