"""Precompute everything in Part 39 of *Philosophy, Built* ("The Arithmetic of Democracy").

    python -m videos.philosophy.philosophy39.compute            # everything missing (about a minute)

Items:
    paradox       Condorcet's three voters and their majority cycle
    agenda        sequential voting on the cycle: every agenda elects someone different
    probs         the probability of no Condorcet winner: exact for 3 alternatives, simulated for more
    zoo           the 55-voter profile under nine rules
    mono          instant runoff is not monotonic: the smallest tie-free example, by search
    iia           the Borda count violates independence: withdraw C and D and E swap
    may           May's theorem by exhaustive search over 59,049 rules
    arrow         Arrow's theorem as SAT: unsatisfiable core, correction sets, and model counts
    manip         every profile of 3 voters and 3 alternatives searched for manipulations, rule by rule
    black         single-peaked profiles: the median voter's peak always wins
    qv            quadratic voting against one person, one vote
    jury          the Condorcet jury theorem, independent and with an opinion leader
    hongpage      diversity and ability, rebuilt on rugged and smooth landscapes
    judgment      the doctrinal paradox; List and Pettit's impossibility by enumeration
    seats         the Alabama paradox and a quota violation
    bt            Bradley-Terry fitted to comparisons from hidden groups, against Borda and Condorcet
"""

from __future__ import annotations

from explainer.ai.cache import Cache
from explainer.philosophy.reasoner import vote as V

CACHE = Cache("philosophy39")
load = CACHE.load


def compute_arrow():
    out = V.arrow_sat()
    out["models_opi"] = V.arrow_models(("ORDER", "PARETO", "IIA"))
    out["models_pi"] = V.arrow_models(("PARETO", "IIA"), limit=200)
    return out


ITEMS = {"paradox": V.condorcet_paradox, "agenda": V.agendas, "probs": V.paradox_table, "zoo": V.zoo, "iia": V.borda_iia, "mono": V.irv_monotonicity,
         "may": V.may_theorem, "arrow": compute_arrow, "manip": V.manipulation, "black": V.black, "qv": V.quadratic, "jury": V.jury,
         "hongpage": V.hong_page_runs,
         "judgment": lambda: {"doctrinal": V.doctrinal(), "list_pettit": V.list_pettit()},
         "seats": lambda: {"alabama": V.alabama(), "quota": V.quota_violation()}, "bt": V.bradley_terry}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
