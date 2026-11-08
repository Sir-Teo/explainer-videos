"""Precompute everything in Part 29 of *Philosophy, Built* ("Being and Time-Consciousness").

    python -m videos.philosophy.philosophy29.compute            # everything missing (seconds)

Items:
    adumbrations  a cube from 4000 viewpoints: faces seen at once, and in all
    eidetic       free variation of a triangle: invariants and accidents (an analogy)
    retention     knife-edge, window and retentional presents on 120 melodies
    diagram       the coordinates of Husserl's time diagram
    axioms        frame axioms against successor-state axioms
    robots        Dennett's robots in a planner; the cost of the irrelevant
    vehicles      Braitenberg's vehicles 2a, 2b, 3a, 3b
    recurrence    a reversible cellular automaton's return; Simmel's wheels
    circle        the hermeneutic circle as an iteration (an analogy)
    procrustes    word vectors under rotation; orthogonal Procrustes
    gaming        a threshold that people optimize against
    dictionary    a closed dictionary and its minimum grounding set
    frame         the Price List for the frame problem
"""

from __future__ import annotations

from explainer.ai.cache import Cache
from explainer.philosophy.reasoner import phenomenology as H
from explainer.philosophy.reasoner import prop

CACHE = Cache("philosophy29")
load = CACHE.load

FRAME = [
    ("E", r"intelligent action is guided by explicit rules over explicit representations"),
    ("R", r"no finite set of explicit rules settles what is relevant in every situation"),
    ("H", r"people pick out what is relevant in every situation they meet"),
]


def compute_frame():
    claims = {k: prop.Var(k) for k, _ in FRAME}
    bg = [prop.Not(prop.And(*[prop.Var(k) for k, _ in FRAME]))]
    res = prop.mus_mcs(claims, bg)
    return {"claims": [{"key": k, "text": t} for k, t in FRAME], "mus": [sorted(x) for x in res["mus"]],
            "mcs": [sorted(x) for x in res["mcs"]]}


def compute_diagram():
    return H.husserl_diagram()


ITEMS = {"adumbrations": H.adumbrations, "eidetic": H.eidetic, "retention": H.retention, "diagram": compute_diagram,
         "axioms": H.axiom_counts, "robots": H.robots, "vehicles": H.braitenberg, "recurrence": H.recurrence,
         "circle": H.hermeneutic, "procrustes": H.procrustes, "gaming": H.gaming, "dictionary": H.dictionary,
         "frame": compute_frame}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
