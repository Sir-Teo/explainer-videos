"""Precompute everything in Part 24 of *Philosophy, Built* ("Laws, Chance and the Arrow").

    python -m videos.philosophy.philosophy24.compute            # everything missing (seconds)

Items:
    best        the best-system toy: polynomial laws scored by two-part description length
    undermine   Humean chance on coin tosses: undermining futures and the big bad bug
    newp        the New Principle against the Principal Principle, as the world grows
    dome        Norton's dome: the solutions (t - T)^4 / 144, checked, and Earman's determinism test
    lorenz      the Lorenz system: two paths 1e-9 apart, the Lyapunov exponent, prediction horizons
    roulette    Poincaré's roulette wheel: deterministic chance by the method of arbitrary functions
    htheorem    Boltzmann's H falling in a toy kinetic gas of colliding molecules
    freegas     Loschmidt's reversal: the coarse-grained entropy of the hook's gas, forwards and reversed
    recur       Poincaré recurrence in miniature: rotors returning to their start
    kac         the Kac ring with 200 sites: decay, recurrence at 2N, reversal
    kacsmall    a 36-site Kac ring for drawing, every state for 2N steps
    slowring    a slowly mixing Kac ring started all white: a special beginning, then entropy rising past now
    boltzmann   100 molecules in a box: microstates, entropy, the improbability of fluctuations
    landauer    kT ln 2; the bits an AND gate destroys; the Toffoli gate
    szilard     Szilard's one-molecule engine, simulated
    both        Loschmidt made visible: a typical low-entropy present, run forwards and backwards
    arrow       the Price List for the arrow of time
"""

from __future__ import annotations

from explainer.ai.cache import Cache
from explainer.philosophy.reasoner import physlaws as L
from explainer.philosophy.reasoner import prop

CACHE = Cache("philosophy24")
load = CACHE.load

ARROW = [
    ("D", r"the fundamental dynamics is time-symmetric"),
    ("R", r"entropy was lower in the past: \ our records and memories are reliable"),
    ("T", r"the rise of entropy is lawlike, \ not a fluke"),
    ("I", r"nothing about the beginning is special"),
]


def compute_arrow() -> dict:
    claims = {k: prop.Var(k) for k, _ in ARROW}
    bg = [prop.Not(prop.And(*[prop.Var(k) for k, _ in ARROW]))]
    res = prop.mus_mcs(claims, bg)
    return {"claims": [{"key": k, "text": t} for k, t in ARROW], "mus": [sorted(x) for x in res["mus"]],
            "mcs": [sorted(x) for x in res["mcs"]]}


ITEMS = {"best": L.best_system, "undermine": L.undermining, "newp": L.new_principle, "dome": L.norton_dome, "lorenz": L.lorenz, "roulette": L.arbitrary_functions,
         "htheorem": L.h_theorem, "freegas": L.free_gas, "recur": L.recurrence, "kac": L.kac_ring, "kacsmall": L.kac_states,
         "slowring": lambda: L.kac_ring(N=2000, marker_fraction=0.01, steps=80, seed=2000), "boltzmann": L.boltzmann, "landauer": L.landauer,
         "szilard": L.szilard, "both": L.kac_both_ways, "arrow": compute_arrow}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
