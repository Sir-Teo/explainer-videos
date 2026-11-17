"""Precompute every number in Part 36 of *Psychology, Built* ("Us and Them").

    python -m videos.psychology.psych36.compute            # everything missing (a minute)
    python -m videos.psychology.psych36.compute --force iat

Results are cached in ``.cache/psych36/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.  Models are Psyche's
(``explainer.psychology.psyche.social``).  Published numbers are quoted in the scenes with their sources.
Simulations use fixed seeds; where a scene shows one simulated study, it is the median of many by a rule fixed in
advance, never chosen by its result.

Items:
    matrix      Tajfel's matrix (7..19 against 1..25) and the column each strategy picks
    illusory    Hamilton and Gifford's counts and the judged rates under distinctive encoding
    listexp     the item-count technique: 2,000 simulated surveys of 1,000 people with a true prevalence of 0.2; the
                spread of estimates, and the survey with the median estimate
    iat         two IAT studies of 400 simulated people, stable and with occasion-to-occasion variation: test-retest,
                the correlation with behaviour, the group mean; and the retest-prediction curve
    audit       how many applications an audit needs: the power to detect a callback gap of 9.6% against 6.4%
    threat      a filtered literature of small stereotype-threat studies of a null effect, against one large
                registered study
    ladder      the promotion ladder: the other group's share at each of eight levels, for advantages of 0.05, 0.1
                and 0.2 SD
"""

from __future__ import annotations

import numpy as np

from explainer.ai.cache import Cache
from explainer.psychology import evidence as E
from explainer.psychology.psyche import social as S

CACHE = Cache("psych36")
load = CACHE.load


def compute_matrix() -> dict:
    M = S.tajfel_matrix()
    picks = {"joint": S.allocate(M, joint=1), "ingroup": S.allocate(M, ingroup=1),
             "difference": S.allocate(M, difference=1), "fair": S.allocate(M, fairness=1),
             "in_plus_diff": S.allocate(M, ingroup=1, difference=1.5)}
    return {"ingroup": M[0], "outgroup": M[1], **{f"pick_{k}": v for k, v in picks.items()}}


def compute_illusory() -> dict:
    out = {}
    for b in (0.0, 0.3, 0.6, 1.0):
        r = S.illusory_correlation(boost=b)
        out[f"b{int(b * 10)}"] = [r["judged"][0], r["judged"][1]]
    out["actual"] = list(S.illusory_correlation()["actual"])
    return out


def compute_listexp() -> dict:
    runs = [S.list_experiment(n=1000, prevalence=0.2, seed=s) for s in range(2000)]
    est = np.array([r["estimate"] for r in runs])
    k = int(np.argsort(est)[len(est) // 2])
    med = runs[k]
    return {"estimates": est, "median_seed": k, "median_est": med["estimate"], "median_se": med["se"],
            "ctrl_counts": np.bincount(med["control"], minlength=5), "trt_counts": np.bincount(med["treatment"], minlength=5),
            "sd": float(est.std()), "mean": float(est.mean())}


def compute_iat() -> dict:
    stable = S.iat_study(n=400, state_sd=0.0, seed=36)
    real = S.iat_study(n=400, seed=36)
    sweep = []
    for sd in (0.0, 0.03, 0.05, 0.07, 0.1, 0.14, 0.2):
        r = S.iat_study(n=400, state_sd=sd, seed=36)
        sweep.append((sd, r["retest"], r["r_behaviour"], r["ceiling"]))
    sweep = np.array(sweep)
    return {"d1": real["d1"], "d2": real["d2"], "behaviour": real["behaviour"], "retest": real["retest"],
            "r_behaviour": real["r_behaviour"], "mean_d": real["mean_d"], "t": real["t"],
            "stable_retest": stable["retest"], "stable_r": stable["r_behaviour"],
            "sweep_sd": sweep[:, 0], "sweep_retest": sweep[:, 1], "sweep_r": sweep[:, 2], "sweep_ceiling": sweep[:, 3]}


def compute_audit() -> dict:
    from scipy.stats import norm
    p1, p2 = 0.096, 0.064
    ns = np.array([50, 100, 200, 400, 800, 1200, 1600, 2400, 3200])
    se = np.sqrt(p1 * (1 - p1) / ns + p2 * (1 - p2) / ns)
    power = norm.sf(1.96 - (p1 - p2) / se) + norm.cdf(-1.96 - (p1 - p2) / se)
    return {"ns": ns, "power": power, "p1": p1, "p2": p2,
            "n80": int(np.ceil((1.96 + 0.8416) ** 2 * (p1 * (1 - p1) + p2 * (1 - p2)) / (p1 - p2) ** 2))}


def compute_threat() -> dict:
    rng = np.random.default_rng(36)
    lit = E.literature(k=60, d=0.0, n=np.full(60, 25), rng=rng, publish_null=0.1, hack=0.2)
    pub = lit["published"]
    w = 1 / lit["se"][pub] ** 2
    pooled = float(np.sum(w * lit["est"][pub]) / np.sum(w))
    big_se = float(np.sqrt(2 / 500))
    big = float(rng.normal(0.0, big_se))
    return {"est": lit["est"], "se": lit["se"], "published": pub, "significant": lit["significant"],
            "hacked": lit["hacked"], "pooled": pooled, "pooled_se": float(1 / np.sqrt(np.sum(w))),
            "n_published": int(pub.sum()), "big_est": big, "big_se": big_se}


def compute_ladder() -> dict:
    return {f"a{int(a * 100):02d}": S.pipeline(levels=8, keep=0.5, advantage=a) for a in (0.05, 0.1, 0.2)}


ITEMS = {"matrix": compute_matrix, "illusory": compute_illusory, "listexp": compute_listexp, "iat": compute_iat,
         "audit": compute_audit, "threat": compute_threat, "ladder": compute_ladder}

if __name__ == "__main__":
    CACHE.main(ITEMS)
