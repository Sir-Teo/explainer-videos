"""Precompute everything in Part 30 of *Philosophy, Built* ("Mind and Machine").

    python -m videos.philosophy.philosophy30.compute            # everything missing (seconds)

Items:
    realizers     one pain role in a threshold network and a water tank, 1000 steps in lockstep
    rulebook      the Chinese room's rulebook on a narrow test and outside it
    blockhead     the size of Block's lookup table
    supervenience weak, strong and global supervenience on three sets of worlds
    life          Gosper's glider gun, 150 generations; a glider's speed
    gauge         Dretske: the bits a fuel gauge carries
    systematicity a compositional interpreter against a lookup table
    probe         decodable is not used: a probe and its removal
    exclusion     the Price List for the mind-body problem
    ramsey        the Ramsey-Lewis definition: occupants of the pain role in three systems
    proportional  Yablo's pigeon: proportional causes under interventions
    patterns      Dennett's real patterns: a bar code under noise, and its description length
    law           a law at the level of gliders: the gun's population every 30 generations, to 600
"""

from __future__ import annotations

from explainer.ai.cache import Cache
from explainer.philosophy.reasoner import mind as M
from explainer.philosophy.reasoner import prop

CACHE = Cache("philosophy30")
load = CACHE.load

TETRAD = [
    ("D", r"mental events are not physical events"),
    ("C", r"mental events cause physical events"),
    ("K", r"every physical event that has a cause has a sufficient physical cause"),
    ("O", r"the effects of mental causes are not systematically overdetermined"),
]


def compute_exclusion():
    claims = {k: prop.Var(k) for k, _ in TETRAD}
    bg = [prop.Not(prop.And(*[prop.Var(k) for k, _ in TETRAD]))]
    res = prop.mus_mcs(claims, bg)
    return {"claims": [{"key": k, "text": t} for k, t in TETRAD], "mus": [sorted(x) for x in res["mus"]],
            "mcs": [sorted(x) for x in res["mcs"]]}


ITEMS = {"realizers": M.realizers, "rulebook": M.rulebook, "blockhead": M.blockhead,
         "supervenience": M.supervenience, "life": M.life, "gauge": M.gauge, "systematicity": M.systematicity,
         "probe": M.probe_vs_use, "exclusion": compute_exclusion,
         "ramsey": M.ramsey, "proportional": M.proportional, "patterns": M.real_patterns, "law": M.glider_law}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
