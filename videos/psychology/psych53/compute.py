"""Precompute every number in Part 53 of *Psychology, Built* ("People at Work").

    python -m videos.psychology.psych53.compute            # everything missing (seconds)

Results are cached in ``.cache/psych53/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.  Models are Psyche's
(``explainer.psychology.psyche.work``).

Items:
    selection   200,000 simulated applicants: observed validity among the hired and its corrections
    overcorrect the same correction applied to a study with no range restriction
    tr          Taylor-Russell success rates by validity and selection ratio (base rate 0.5)
    utility     Brogden-Cronbach-Gleser utility for the 1998 and 2022 validities
    impact      selection rates and impact ratios by group difference
    frontier    the validity-diversity frontier for an ability test and a structured interview
    interviews  test, unstructured and structured interviews, holistic and mechanical combination
    hire        the on-you hiring choice: 1,000 simulated pairs of candidates
"""

from __future__ import annotations

import numpy as np

from explainer.ai.cache import Cache
from explainer.psychology.psyche import work as Wk

CACHE = Cache("psych53")
load = CACHE.load


def compute_selection() -> dict:
    return Wk.selection(seed=5301)


def compute_overcorrect() -> dict:
    s = Wk.selection(seed=5302)
    r_obs = s["r_all_obs"]  # a concurrent study of people never selected on this test
    over = Wk.case2(r_obs / np.sqrt(0.6), s["u"])
    return {"r_obs": r_obs, "r_over": float(over), "truth": s["r_all_true"], "u": s["u"]}


def compute_tr() -> dict:
    ratios = np.array([0.05, 0.1, 0.2, 0.3, 0.5, 0.7, 0.9])
    vals = np.array([0.0, 0.2, 0.3, 0.4, 0.5])
    grid = np.array([[Wk.taylor_russell(v, 0.5, r) for r in ratios] for v in vals])
    return {"ratios": ratios, "validity": vals, "success": grid}


def compute_utility() -> dict:
    out = {}
    for name, r in (("ability_1998", 0.51), ("ability_2022", 0.31), ("structured_2022", 0.42),
                     ("unstructured_2022", 0.19)):
        out[name] = Wk.bcg_utility(r, 0.2, 20000.0, n_hired=100, years=5, cost_per_applicant=100.0)["net"]
    ratios = np.array([0.05, 0.1, 0.2, 0.4, 0.6, 0.8])
    out["ratios"] = ratios
    out["by_ratio"] = np.array([Wk.bcg_utility(0.42, r, 20000.0, n_hired=100, years=5, cost_per_applicant=100.0)["net"]
                                for r in ratios])
    out["zbar"] = np.array([Wk.bcg_utility(0.42, r, 1.0)["zbar"] for r in ratios])
    return out


def compute_impact() -> dict:
    ds = np.array([0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
    rows = [Wk.adverse_impact(float(d), 0.2) for d in ds]
    return {"d": ds, "maj": np.array([r["majority"] for r in rows]), "min": np.array([r["minority"] for r in rows]),
            "ratio": np.array([r["impact_ratio"] for r in rows])}


def compute_frontier() -> dict:
    return Wk.frontier()


def compute_interviews() -> dict:
    return Wk.interviews(n=20000, seed=5303)


def compute_hire() -> dict:
    # each pair: candidate A has the better test score, B the better unstructured-interview impression
    rng = np.random.default_rng(5304)
    n = 200000
    g = rng.standard_normal(n)
    s = rng.standard_normal(n)
    perf = 0.31 * g + 0.45 * s + np.sqrt(1 - 0.31 ** 2 - 0.45 ** 2) * rng.standard_normal(n)
    test = g + 0.4 * rng.standard_normal(n)
    imp = s + 2.2 * rng.standard_normal(n)
    i = rng.integers(0, n, (400000, 2))
    a, b = i[:, 0], i[:, 1]
    keep = (test[a] - test[b] > 1.0) & (imp[b] - imp[a] > 1.0)
    a, b = a[keep][:1000], b[keep][:1000]
    return {"pairs": len(a), "test_wins": float(np.mean(perf[a] > perf[b]))}


ITEMS = {"selection": compute_selection, "overcorrect": compute_overcorrect, "tr": compute_tr,
         "utility": compute_utility, "impact": compute_impact, "frontier": compute_frontier,
         "interviews": compute_interviews, "hire": compute_hire}

if __name__ == "__main__":
    CACHE.main(ITEMS)
