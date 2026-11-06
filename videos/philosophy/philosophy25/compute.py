"""Precompute everything in Part 25 of *Philosophy, Built* ("Space and Time").

    python -m videos.philosophy.philosophy25.compute            # everything missing (seconds)

Items:
    bucket      Newton's bucket: the water's paraboloid at several spin rates
    shifts      Leibniz's shifts: every inter-body distance unchanged by static, kinematic and rotational shifts
    hands       Kant's incongruent counterparts; a frame carried round a Möbius strip
    disk        hyperbolic triangles in the Poincaré disk: angle sums and areas
    gauss       Gauss's survey triangle on the curved Earth
    diskworld   Poincaré's disk world: what shrinking rulers measure
    simul       the relativity of simultaneity for two lightning strikes
    rp          the Rietdijk--Putnam boost
    eps         Reichenbach's epsilon
    transport   slow clock transport and the epsilon it yields
    boost       a Galilean boost: velocities shift, accelerations stay
    hole        the hole diffeomorphism
    ctc         Deutsch's fixed points for the grandfather and knowledge paradoxes
    match       Barbour's best matching of two configurations
    twins       the twins: proper times, and random worldlines between the same two events
    causet      a causal set: sprinkled events, their links, and the dimension recovered from order alone
    holepl      the Price List for the hole argument
"""

from __future__ import annotations

from explainer.ai.cache import Cache
from explainer.philosophy.reasoner import prop
from explainer.philosophy.reasoner import spacetime as S

CACHE = Cache("philosophy25")
load = CACHE.load

HOLE = [
    ("P", r"spacetime points are real things, \ with identities of their own"),
    ("D", r"general relativity is deterministic"),
    ("M", r"diffeomorphic models represent different possible worlds"),
]


def compute_holepl() -> dict:
    claims = {k: prop.Var(k) for k, _ in HOLE}
    bg = [prop.Not(prop.And(*[prop.Var(k) for k, _ in HOLE]))]
    res = prop.mus_mcs(claims, bg)
    return {"claims": [{"key": k, "text": t} for k, t in HOLE], "mus": [sorted(x) for x in res["mus"]],
            "mcs": [sorted(x) for x in res["mcs"]]}


ITEMS = {"bucket": S.bucket, "shifts": S.shifts, "hands": S.incongruent, "disk": S.disk_triangles,
         "gauss": S.gauss_triangle, "diskworld": S.disk_world, "simul": S.simultaneity, "rp": S.rietdijk_putnam,
         "eps": S.reichenbach, "transport": S.clock_transport, "boost": S.galilean_boost, "hole": S.hole, "ctc": S.ctc, "match": S.best_matching,
         "twins": S.twins, "causet": S.causal_set, "holepl": compute_holepl}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
