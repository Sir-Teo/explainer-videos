"""Precompute everything in Part 38 of *Philosophy, Built* ("Justice").

    python -m videos.philosophy.philosophy38.compute            # everything missing (seconds)

Items:
    three         three five-person societies and the principle each would choose
    veil          200 societies chosen behind the veil by maximin, average and CRRA expected utility
    difference    the difference principle on an incentive frontier
    wilt          Nozick's Wilt Chamberlain as a toy economy
    tetrad        the Price List for Nozick's argument
    ceei          competitive equilibrium from equal incomes, envy-freeness checked
    sen           Sen's liberal paradox by exhaustive search; Lady Chatterley's Lover
    cake          cut and choose; Selfridge-Conway for three
    rent          envy-free rent division that maximizes the least utility
    match         deferred acceptance for school choice; every stable matching by enumeration
"""

from __future__ import annotations

from explainer.ai.cache import Cache
from explainer.philosophy.reasoner import justice as J
from explainer.philosophy.reasoner import prop

CACHE = Cache("philosophy38")
load = CACHE.load

TETRAD = [
    ("D1", r"D1, \ the distribution you favour, \ is just"),
    ("TRANSFER", r"whatever arises from a just situation by voluntary exchange is just"),
    ("ARISES", r"D2 arises from D1 by voluntary exchange: \ paying to watch Wilt play"),
    ("UNJUST", r"D2, \ with Wilt's fortune, \ is unjust"),
]


def compute_tetrad():
    claims = {k: prop.Var(k) for k, _ in TETRAD}
    bg = [prop.Not(prop.And(*[prop.Var(k) for k, _ in TETRAD]))]
    res = prop.mus_mcs(claims, bg)
    return {"claims": [{"key": k, "text": t} for k, t in TETRAD], "mus": [sorted(x) for x in res["mus"]],
            "mcs": [sorted(x) for x in res["mcs"]]}


def compute_cake():
    return {"cut_choose": J.cut_and_choose(), "sc": J.selfridge_conway()}


ITEMS = {"three": J.three_societies, "veil": J.veil, "difference": J.difference_principle, "wilt": J.wilt, "tetrad": compute_tetrad,
         "ceei": J.ceei, "sen": J.liberal_paradox, "cake": compute_cake, "rent": J.rent_division,
         "match": J.stable_matching}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
