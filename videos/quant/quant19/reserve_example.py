"""Recalibrate Hull-White volatility to one fixed European before comparing Bermudans.

Unlike post-hoc price-ratio rescaling, every scenario reprices the same strike,
expiry, underlying tenor and target European price. This is a synthetic model
sensitivity exercise, not a market calibration or accounting-reserve rule.

    python -m videos.quant.quant19.reserve_example reserve_example
"""
from __future__ import annotations

import numpy as np
from scipy.optimize import brentq

from explainer.ai.cache import Cache
from explainer.quant.house import termstructure as TS
from .compute import _curve_2025, load

CACHE = Cache("quant19")


def compute_example():
    base = load("bermudan")
    curve = _curve_2025()
    expiry = float(np.asarray(base["dates"])[np.argmax(base["europeans"])])
    tenor = 10 - expiry
    strike = base["K"]
    target = float(max(base["europeans"]))
    rows = []
    for a in (0.005, 0.02, 0.05, 0.1, 0.2):
        sigma = brentq(lambda s: TS.HullWhite(curve, a, s).swaption(strike, expiry, tenor, 1, payer=False) - target,
                       1e-5, 0.1, xtol=1e-12)
        hw = TS.HullWhite(curve, a, sigma)
        european = hw.swaption(strike, expiry, tenor, 1, payer=False)
        grid = TS.bermudan_swaption_lattice(hw, strike, 1.0, 10.0, freq=1, payer=False, n_x=1201)
        rows.append({"a": a, "sigma": sigma, "european": european, "bermudan": float(grid)})
    return {"rows": rows, "strike": strike, "hedge_expiry": expiry, "hedge_tenor": tenor,
            "target_european": target, "n_x": 1201,
            "scope": "one fixed synthetic European hedge, actual volatility recalibration; numerical grid prices, not an exact or true-price bound"}


if __name__ == "__main__":
    CACHE.main({"reserve_example": compute_example}, __doc__)
