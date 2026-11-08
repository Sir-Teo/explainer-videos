"""Precompute everything in Part 42 of *Philosophy, Built* ("Aligning Reasoners").

    python -m videos.philosophy.philosophy42.compute            # everything missing (a minute)

Items:
    goodhart      best-of-N on a noisy proxy: Gaussian and heavy-tailed error
    quantilize    mild optimization: pick at random among the proxy's top fraction q
    nfl           no free lunch for preferences: planner-reward pairs that fit the same behaviour
    offswitch     the off-switch game: the incentive to defer, for a rational and a noisy human
    power         power-seeking on a small MDP; the fraction of rewards that avoid shutdown
    lob           Löb's axiom on every Kripke frame with up to four worlds
    combat        modal combat: four proof-based bots in the prisoner's dilemma
    alignment     the Price List for the alignment cluster
    wall          the 42 bricks of the Wall, sorted by what they force
    reasoner      the Reasoner, by the numbers: modules, lines and tests
"""

from __future__ import annotations

import ast
import pathlib

from explainer.ai.cache import Cache
from explainer.philosophy.reasoner import alignment as AL
from explainer.philosophy.reasoner import prop

CACHE = Cache("philosophy42")
load = CACHE.load

ALIGN = [
    ("PROXY", r"what we can write down is only a proxy for what we want"),
    ("STRONG", r"strong optimizers will optimize what we write down"),
    ("GOODHART", r"under strong optimization, a proxy and its target come apart"),
    ("SAFE", r"the result will be what we want"),
]


def compute_alignment():
    claims = {k: prop.Var(k) for k, _ in ALIGN}
    bg = [prop.Not(prop.And(*[prop.Var(k) for k, _ in ALIGN]))]
    res = prop.mus_mcs(claims, bg)
    return {"claims": [{"key": k, "text": t} for k, t in ALIGN], "mus": [sorted(x) for x in res["mus"]],
            "mcs": [sorted(x) for x in res["mcs"]]}


# What each brick forces, in five kinds (part 42 is the capstone and gets its own colour)
KINDS = {
    "A": (r"proof and calculation run out", (2, 3, 4, 6, 7, 8, 12, 29)),
    "B": (r"evidence underdetermines", (10, 13, 15, 16, 17, 18, 24)),
    "C": (r"no aggregation meets every condition", (33, 34, 35, 36, 38, 39, 41)),
    "D": (r"facts do not fix meaning, mind or value", (22, 27, 28, 30, 31, 32, 37, 40)),
    "E": (r"a paradox forces a new concept", (1, 5, 9, 11, 14, 19, 20, 21, 23, 25, 26)),
}


def compute_wall():
    from explainer.philosophy.studio import WALL
    kind = {}
    for k, (_, parts) in KINDS.items():
        for p in parts:
            assert p not in kind, p
            kind[p] = k
    assert sorted(kind) == list(range(1, 42)), sorted(set(range(1, 42)) - set(kind))
    return {"kinds": {k: {"name": n, "parts": list(ps)} for k, (n, ps) in KINDS.items()},
            "kind": {str(p): k for p, k in kind.items()},
            "years": {str(p): WALL[p][3] for p in range(1, 43)},
            "counts": {k: len(ps) for k, (_, ps) in KINDS.items()}}


def compute_reasoner():
    root = pathlib.Path(__file__).resolve().parents[3]
    mods = sorted((root / "explainer/philosophy/reasoner").glob("*.py"))
    mods = [m for m in mods if m.name != "__init__.py"]
    lines = sum(len(m.read_text().splitlines()) for m in mods)
    funcs = 0
    for m in mods:
        tree = ast.parse(m.read_text())
        funcs += sum(isinstance(n, ast.FunctionDef) and not n.name.startswith("_") for n in tree.body)
    tests = sorted((root / "tests/philosophy").glob("test_*.py"))
    ntests = 0
    for t in tests:
        tree = ast.parse(t.read_text())
        ntests += sum(isinstance(n, ast.FunctionDef) and n.name.startswith("test_") for n in tree.body)
    return {"modules": len(mods), "lines": lines, "functions": funcs, "test_files": len(tests), "tests": ntests,
            "names": [m.stem for m in mods]}


ITEMS = {"goodhart": AL.goodhart, "quantilize": AL.quantilize, "nfl": AL.no_free_lunch, "offswitch": AL.off_switch,
         "power": AL.power_seeking, "lob": AL.lob_frames, "combat": AL.modal_combat, "alignment": compute_alignment,
         "wall": compute_wall, "reasoner": compute_reasoner}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
