"""Precompute every number in Part 37 of *Psychology, Built* ("Bonds and Bargains").

    python -m videos.psychology.psych37.compute            # everything missing (about a minute)
    python -m videos.psychology.psych37.compute --force tournament

Results are cached in ``.cache/psych37/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.  Models are Psyche's
(``explainer.psychology.psyche.social``).  Published numbers are quoted in the scenes with their sources.
Simulations use fixed seeds; where a scene shows one simulated sample, it is the median of many by a rule fixed in
advance.

Items:
    ultimatum   inequity-averse responders (30% with alpha = 0, the rest uniform on 0.3..1.5): acceptance by offer,
                the proposer's expected payoff and best offer, against a population of purely selfish responders
    tournament  a round-robin of seven iterated prisoner's dilemma strategies, 200 moves, without and with 5% noise
    goods       ten rounds of a public-goods game in 200 groups of four, without and with punishment
    divorce     a classifier on 56 couples and 30 variables (one weakly informative): in-sample against leave-one-out
                accuracy over 200 samples, and the sample with the median in-sample accuracy
    market      a marriage market of 200 + 200 people solved by deferred acceptance, 50 seeds each way: everyone
                wants the most attractive partner (plus private taste, SD 0.5), or everyone wants someone like
                themselves; the partners' correlation in attractiveness, and the median-r sample of each
    hamilton    Hamilton's rule rB > C: the benefit-to-cost ratio needed to help kin of each relatedness
"""

from __future__ import annotations

import numpy as np

from explainer.ai.cache import Cache
from explainer.psychology.psyche import social as S

CACHE = Cache("psych37")
load = CACHE.load

ALPHAS = np.r_[np.zeros(30), np.linspace(0.3, 1.5, 70)]


def compute_ultimatum() -> dict:
    u = S.ultimatum(ALPHAS)
    return {"offers": u["offers"], "accept": u["accept"], "payoff": u["payoff"], "best": u["best"],
            "thresholds": S.fs_threshold(ALPHAS), "best_payoff": float(u["payoff"].max()),
            "selfish_best": 0.0}


def compute_tournament() -> dict:
    out = {}
    for tag, nz in (("clean", 0.0), ("noisy", 0.05)):
        r = S.ipd_tournament(noise=nz, seed=37)
        out[f"{tag}_score"] = r["score"]
        out[f"{tag}_matrix"] = r["matrix"]
    out["names"] = list(S.IPD_STRATEGIES)
    return out


def compute_goods() -> dict:
    return {"plain": S.public_goods(seed=37), "punish": S.public_goods(punishment=True, seed=37)}


def compute_divorce() -> dict:
    rs = [S.overfit_divorce(seed=s) for s in range(200)]
    ins = np.array([r["insample"] for r in rs])
    loo = np.array([r["loo"] for r in rs])
    k = int(np.argsort(ins)[len(ins) // 2])
    return {"insample": ins, "loo": loo, "base": float(np.mean([r["base"] for r in rs])),
            "median_insample": float(ins[k]), "median_loo": float(loo[k]), "mean_insample": float(ins.mean()),
            "mean_loo": float(loo.mean())}


def compute_market() -> dict:
    out = {}
    for tag, sim in (("best", False), ("alike", True)):
        rs = [S.stable_matching(n=200, taste=0.5, similar=sim, seed=s) for s in range(50)]
        r = np.array([x["r"] for x in rs])
        k = int(np.argsort(r)[len(r) // 2])
        out[f"{tag}_r"] = r
        out[f"{tag}_median"] = float(r[k])
        out[f"{tag}_a"], out[f"{tag}_b"] = rs[k]["a"], rs[k]["b"]
    return out


def compute_hamilton() -> dict:
    r = np.array([1.0, 0.5, 0.25, 0.125])
    return {"r": r, "ratio": 1 / r}


ITEMS = {"ultimatum": compute_ultimatum, "tournament": compute_tournament, "goods": compute_goods,
         "divorce": compute_divorce, "market": compute_market, "hamilton": compute_hamilton}

if __name__ == "__main__":
    CACHE.main(ITEMS)
