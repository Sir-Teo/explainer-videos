"""Precompute everything in Part 31 of *Philosophy, Built* ("Consciousness").

    python -m videos.philosophy.philosophy31.compute            # everything missing (a minute)

Items:
    twod          two-dimensional semantics: 'water is H2O' and 'pain is C-fibre firing' on three scenarios
    zombie        the Price List for the zombie argument
    modal         the zombie argument in modal logic: which physicalism it refutes
    mary          what Mary can rule out, before and after she leaves the room
    introspection a self-model that cannot say what it can tell apart
    workspace     a global workspace: ignition, and the masking curve it produces
    meta          metacognition in signal detection: a normal observer and blindsight
    phi           a simplified integrated information on four small networks, with every cut
    states        the loop's simplified Phi in each of its eight states
    aaronson      an adder against structures of XOR gates
    unfolding     a recurrent loop and its feedforward unrolling
    tmaze         active inference: a T-maze agent, and free energy
    indicators    Butlin, Long et al.'s indicator properties, on the Reasoner's own toys
"""

from __future__ import annotations

from explainer.ai.cache import Cache
from explainer.philosophy.reasoner import consciousness as C
from explainer.philosophy.reasoner import modal as Mo
from explainer.philosophy.reasoner import prop

CACHE = Cache("philosophy31")
load = CACHE.load

ZOMBIE = [
    ("Z", r"a zombie world, physically like ours but without experience, is conceivable"),
    ("CP", r"whatever is ideally conceivable is metaphysically possible"),
    ("E", r"if a zombie world is possible, physicalism is false"),
    ("P", r"physicalism is true"),
]


def compute_zombie():
    claims = {k: prop.Var(k) for k, _ in ZOMBIE}
    bg = [prop.Not(prop.And(*[prop.Var(k) for k, _ in ZOMBIE]))]
    res = prop.mus_mcs(claims, bg)
    return {"claims": [{"key": k, "text": t} for k, t in ZOMBIE], "mus": [sorted(x) for x in res["mus"]],
            "mcs": [sorted(x) for x in res["mcs"]]}


def compute_modal():
    """Physicalism as necessitation, box(P -> Q), with P all the physical truths and Q a phenomenal one, is
    inconsistent with the possibility of zombies, dia(P & ~Q), on every frame up to three worlds (and in K generally);
    the weaker claim that P -> Q merely holds here is consistent with it, on an S5 frame of two worlds."""
    equiv = lambda R, n: Mo.reflexive(R, n) and Mo.symmetric(R, n) and Mo.transitive(R, n)  # noqa: E731
    strong = [Mo.parse("[](P -> Q)"), Mo.parse("<>(P & ~Q)")]
    weak = [Mo.parse("P -> Q"), Mo.parse("P"), Mo.parse("<>(P & ~Q)")]
    m = Mo.find_model(weak, 3, equiv)
    return {"strong_any": Mo.find_model(strong, 3) is None, "strong_s5": Mo.find_model(strong, 3, equiv) is None,
            "weak_worlds": len(m.worlds), "weak_P": sorted(m.V["P"]), "weak_Q": sorted(m.V["Q"])}


def compute_states():
    import numpy as np
    g, ins = C.NETWORKS["OR, AND, XOR loop"]
    states, nxt = C._step_table(g, ins)
    rows = []
    for s in states.tolist():
        pre = int(np.all(nxt == np.array(s, dtype=np.int8), axis=1).sum())
        phi = C.phi_simple(g, ins, s)["phi"] if pre else None
        rows.append({"state": s, "pasts": pre, "phi": phi})
    return {"rows": rows}


def compute_phi():
    out = C.phi_examples()
    # the cut search for the loop: every bipartition, its effective information and normalized value
    g, ins = C.NETWORKS["OR, AND, XOR loop"]
    x1 = C._reachable_state(g, ins)
    states, nxt = C._step_table(g, ins)
    import itertools
    import numpy as np
    cuts = []
    for A in itertools.combinations(range(3), 1):
        B = tuple(i for i in range(3) if i not in A)
        ei = C._ei(states, nxt, np.array(x1, dtype=np.int8), (A, B))
        cuts.append({"A": list(A), "B": list(B), "ei": round(ei, 4), "norm": round(ei / 1, 4)})
    return {"networks": out, "loop_cuts": cuts, "loop_state": list(x1)}


ITEMS = {"twod": C.two_d, "zombie": compute_zombie, "modal": compute_modal, "states": compute_states, "mary": C.mary, "introspection": C.introspection,
         "workspace": C.workspace, "meta": C.metacognition, "phi": compute_phi, "aaronson": C.aaronson,
         "unfolding": C.unfolding, "tmaze": C.tmaze, "indicators": C.indicators}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
