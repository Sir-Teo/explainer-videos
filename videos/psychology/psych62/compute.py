"""Precompute every number in Part 62 of *Psychology, Built* ("The Dissertation").

    python -m videos.psychology.psych62.compute            # everything missing (a few minutes)

Results are cached in ``.cache/psych62/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.  The registered
report is ``explainer.psychology.psyche.thesis``: its ``PLAN`` was written and hashed before the analysis was run.

Items:
    plan        the registered plan's hash and its decision threshold
    power       the design check: verdicts for 54 simulated people at four true reliabilities
    stage2      the registered analysis of Ganis and Kievit's (2015) data, with the one reported deviation
    explore     exploratory analyses, labelled as such
    scorecard   Psyche on the Battery, task by task
    failures    the two tasks Psyche fails with one set of parameters: search times and the serial-position curve
    board       the complete Ledger by act
"""

from __future__ import annotations

import numpy as np

from explainer.ai.cache import Cache
from explainer.psychology import ledger, opendata
from explainer.psychology.psyche import thesis as Th

CACHE = Cache("psych62")
load = CACHE.load


def compute_plan() -> dict:
    return {"hash": Th.plan_hash(), "registered_min": Th.DEVIATION["registered_min_per_cell"],
            "used_min": Th.DEVIATION["used_min_per_cell"]}


def compute_power() -> dict:
    return Th.power(reps=200, seed=6200)


def compute_stage2() -> dict:
    d = opendata.mental_rotation()
    strict = Th.person_halves(d, min_per_cell=Th.DEVIATION["registered_min_per_cell"])
    h = Th.person_halves(d, min_per_cell=Th.DEVIATION["used_min_per_cell"])
    r = Th.analyse(h)
    v = Th.verdict(r)
    return {**r, "H1": v["H1"], "H2": v["H2"], "kept_strict": len(strict["subject"]), "excluded": h["excluded"],
            "slope_odd": h["slope_odd"], "slope_even": h["slope_even"], "mean_odd": h["mean_odd"],
            "mean_even": h["mean_even"]}


def compute_explore() -> dict:
    d = opendata.mental_rotation()
    allt = dict(d)
    allt["same"] = np.ones_like(d["same"], bool)
    ha = Th.person_halves(allt, min_per_cell=2)
    ra = Th.analyse(ha, boots=2000, seed=6201)
    h = Th.person_halves(d, min_per_cell=2)
    s = (h["slope_odd"] + h["slope_even"]) / 2
    err_half = np.var(h["slope_odd"] - h["slope_even"], ddof=1) / 2
    between = float(np.sqrt(max(np.var(s, ddof=1) - err_half / 2, 0.0)))
    return {"all_n": ra["n"], "all_rel": ra["slope_rel"], "all_ci": ra["slope_ci"], "between_sd": between,
            "half_error_sd": float(np.sqrt(err_half)), "mean_slope": float(s.mean()), "share_rising": float(np.mean(s > 0))}


def compute_scorecard() -> dict:
    rows = Th.scorecard(seed=6202)
    return {"num": [str(r[0]) for r in rows], "name": [r[1] for r in rows], "signature": [r[2] for r in rows],
            "psyche": [r[3] for r in rows], "pass": [("n/a" if r[4] is None else ("yes" if r[4] else "no")) for r in rows]}


def compute_failures() -> dict:
    """The two Battery tasks Psyche fails with one set of parameters, drawn: search times by set size, and the
    serial-position curve of free recall (the same runs and seeds as the scorecard)."""
    from explainer.psychology import battery
    from explainer.psychology.psyche import memory as M
    v = battery.run("search", {}, 3200, seed=6202 + 4)
    ss = v.extra["set_size"]
    out = {}
    for key, kind, present in (("feature", "feature", True), ("present", "conjunction", True),
                               ("absent", "conjunction", False)):
        mm = v.where(kind) & (v.extra["present"] == present) & v.correct
        sizes = np.unique(ss[mm])
        out["sizes"] = sizes.tolist()
        out[key] = [float(v.rt[mm & (ss == k)].mean()) for k in sizes]
    r = battery.run("recall", {}, 400, seed=6202 + 6)
    out["spc"] = np.asarray(M.recall_summary(r.extra["recalls"], 16, max_lag=1)["spc"]).tolist()
    return out


def compute_board() -> dict:
    b = Th.ledger_by_act(ledger.rows())
    return {"acts": b["acts"], "names": b["names"], "groups": b["groups"], "table": b["table"],
            "total": int(b["table"].sum()), "counts": ledger.counts()}


def compute_decades() -> dict:
    b = Th.ledger_by_decade(ledger.rows())
    return {"labels": b["labels"], "groups": b["groups"], "table": b["table"]}


ITEMS = {"plan": compute_plan, "power": compute_power, "stage2": compute_stage2, "explore": compute_explore,
         "scorecard": compute_scorecard, "failures": compute_failures, "board": compute_board,
         "decades": compute_decades}

if __name__ == "__main__":
    CACHE.main(ITEMS)
