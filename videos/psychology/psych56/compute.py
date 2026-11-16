"""Precompute every number in Part 56 of *Psychology, Built* ("Psychology and Law").

    python -m videos.psychology.psych56.compute            # everything missing (a minute)

Results are cached in ``.cache/psych56/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.  Models are Psyche's
(``explainer.psychology.psyche.work``; the line-up is Part 21's observer).

Items:
    roc         simultaneous and sequential line-ups: ROC points, diagnosticity ratios, partial areas
    cac         the confidence-accuracy characteristic, initially and after confirming feedback
    risk        one calibrated risk score in two groups with base rates 0.3 and 0.5
    iq          the interval around an IQ score of 71
    onyou       the on-you line-up: rates at a moderate criterion for a culprit-present and a culprit-absent line-up
"""

from __future__ import annotations

import numpy as np

from explainer.ai.cache import Cache
from explainer.psychology.psyche import work as Wk

CACHE = Cache("psych56")
load = CACHE.load


def compute_roc() -> dict:
    s = Wk.lineup_roc("simultaneous", seed=5601)
    q = Wk.lineup_roc("sequential", seed=5602)
    up = float(min(s["fa"].max(), q["fa"].max()))
    i_s = int(np.argmin(np.abs(s["criteria"] - 1.0)))
    i_q = int(np.argmin(np.abs(q["criteria"] - 1.5)))
    return {"s_hit": s["hit"], "s_fa": s["fa"], "q_hit": q["hit"], "q_fa": q["fa"], "criteria": s["criteria"],
            "pauc_s": Wk.partial_auc(s["fa"], s["hit"], up), "pauc_q": Wk.partial_auc(q["fa"], q["hit"], up),
            "upto": up, "s_point": [float(s["fa"][i_s]), float(s["hit"][i_s]), float(s["dr"][i_s])],
            "q_point": [float(q["fa"][i_q]), float(q["hit"][i_q]), float(q["dr"][i_q])]}


def compute_cac() -> dict:
    return Wk.confidence_feedback(seed=5603)


def compute_risk() -> dict:
    r = Wk.risk_groups(seed=5604)
    a, b = r[0.3], r[0.5]
    return {"base": [0.3, 0.5], "fpr": [a["fpr"], b["fpr"]], "fnr": [a["fnr"], b["fnr"]], "ppv": [a["ppv"], b["ppv"]],
            "flagged": [a["flagged"], b["flagged"]]}


def compute_iq() -> dict:
    return Wk.score_interval(71, reliability=0.97)


def compute_onyou() -> dict:
    s = Wk.lineup_roc("simultaneous", criteria=[1.0], seed=5605)
    rng = np.random.default_rng(5606)
    n = 100_000
    p = rng.standard_normal((n, 6))
    p[:, 0] += 1.5
    a = rng.standard_normal((n, 6))
    pick_p = np.where(p.max(1) > 1.0, p.argmax(1), -1)
    pick_a = np.where(a.max(1) > 1.0, a.argmax(1), -1)
    return {"present_culprit": float(np.mean(pick_p == 0)), "present_filler": float(np.mean(pick_p > 0)),
            "present_none": float(np.mean(pick_p < 0)), "absent_any": float(np.mean(pick_a >= 0)),
            "absent_suspect": float(s["fa"][0]), "absent_none": float(np.mean(pick_a < 0))}


ITEMS = {"roc": compute_roc, "cac": compute_cac, "risk": compute_risk, "iq": compute_iq, "onyou": compute_onyou}

if __name__ == "__main__":
    CACHE.main(ITEMS)
