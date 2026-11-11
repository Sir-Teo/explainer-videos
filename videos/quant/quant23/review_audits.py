"""Fixed numerical display audit; never a replacement for the original computations.

Run only after the original Part 23 public-data restores have passed their normal
hash checks. Extends the HJ display to a declared grid using the same saved sample
moments and House formula, without fitting or selecting a portfolio or strategy.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np

from explainer.quant.house import premia
from . import compute


def hj_display():
    original = compute.load("hj")
    years, market, bill, inflation = compute._annual_returns()
    keep = np.isfinite(inflation)
    returns = np.c_[(1 + market[keep]) / (1 + inflation[keep]),
                    (1 + bill[keep]) / (1 + inflation[keep])]
    mean, covariance = returns.mean(0), np.cov(returns.T)
    saved = premia.hj_gross(mean, covariance, np.asarray(original["Em"]))
    assert np.allclose(saved, original["bound"], rtol=1e-12, atol=1e-12)
    grid = np.linspace(0.5, 1.02, 301)
    points = [dict(p) for p in original["pts"]]
    bounds = premia.hj_gross(mean, covariance, np.array([p["Em"] for p in points]))
    for point, bound in zip(points, bounds):
        point["lower_bound"] = float(bound)
        point["satisfies_necessary_bound"] = bool(point["sd"] >= bound)
    return {"scope": "Fixed display grid, original annual gross-return sample and unchanged HJ formula; no positivity constraint, estimation, strategy trial or performance series",
            "years": [int(years[keep][0]), int(years[keep][-1])], "n": len(returns),
            "bill_scope": "Nominal bills deflated ex post have inflation risk; this is not a known real risk-free return",
            "original_cache_sha256": hashlib.sha256(compute.CACHE.path("hj").read_bytes()).hexdigest(),
            "mu_gross": mean.tolist(), "cov_gross": covariance.tolist(),
            "Em": grid.tolist(), "bound": premia.hj_gross(mean, covariance, grid).tolist(), "points": points}


if __name__ == "__main__":
    result = hj_display()
    path = compute.CACHE.path("hj_display_audit")
    if path.exists():
        assert json.loads(path.read_text()) == result, "Audit already exists with different bytes; investigate"
    else:
        compute.CACHE.save("hj_display_audit", result)
    print(json.dumps({"path": str(path), "years": result["years"], "n": result["n"],
                      "max_bound": max(result["bound"]), "point_bounds": result["points"]}, indent=2))
