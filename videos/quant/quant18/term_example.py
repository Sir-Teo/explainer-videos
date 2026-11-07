"""Scoped descriptive term-premium example on the pinned GSW yield curve.

Run ``python -m videos.quant.quant18.term_example term_example``.
The legacy ``compute_term`` cannot complete because the live NY Fed comparison
file no longer matches its pinned historical hash. This separately named example
retains the legacy regression and ACM settings, omits that unavailable comparison,
and makes no strategy, forecast or independent-replication claim. It never invokes
the legacy fly/envelope items, registers a strategy, or opens a sealed fly window.
The original compute driver and House algorithms remain unchanged.
"""
from __future__ import annotations

import numpy as np

from explainer.ai.cache import Cache
from explainer.quant import data
from explainer.quant.house import rates as R
from .compute import _frac_year, _json, _monthly_logp


LEGACY_COMPUTE_SHA256 = 'c10cbd61fc78726fc171bbe617501b1c9d0c6225eff044e3a4f450dd0370d9f8'


def compute_example() -> dict:
    g = data.gsw()
    md, lp = _monthly_logp(g)
    n = np.arange(1, lp.shape[1] + 1)
    Y = -lp / n * 1200  # percent a year
    # Campbell-Shiller (1991): y(n-1, t+1) - y(n, t) on the slope (y(n) - y(1)) / (n - 1); 1 under expectations
    cs = {}
    for nn in (12, 24, 36, 60, 120):
        lhs = Y[1:, nn - 2] - Y[:-1, nn - 1]
        x = (Y[:-1, nn - 1] - Y[:-1, 0]) / (nn - 1)
        X = np.c_[np.ones(len(x)), x]
        coef = np.linalg.lstsq(X, lhs, rcond=None)[0]
        e = lhs - X @ coef
        V = np.linalg.inv(X.T @ X) * (e @ e) / (len(x) - 2)
        cs[str(nn)] = {"b": float(coef[1]), "se": float(np.sqrt(V[1, 1]))}
    # Fama-Bliss (1987): one-year excess return of an n-year bond on the forward-spot spread; annual, overlapping
    fb = {}
    for ny in (2, 3, 4, 5):
        nm = 12 * ny
        rx = (lp[12:, nm - 13] - lp[:-12, nm - 1]) + lp[:-12, 11]  # log return minus the 1-year yield
        fwd = lp[:-12, nm - 13] - lp[:-12, nm - 1]  # forward rate from n-1 to n years (log)
        x = fwd + lp[:-12, 11]
        X = np.c_[np.ones(len(x)), x]
        coef = np.linalg.lstsq(X, rx, rcond=None)[0]
        e = rx - X @ coef
        # Newey-West with 12 lags (overlapping annual returns)
        Xe = X * e[:, None]
        S = Xe.T @ Xe
        for L in range(1, 13):
            w = 1 - L / 13
            G = Xe[L:].T @ Xe[:-L]
            S += w * (G + G.T)
        XX = np.linalg.inv(X.T @ X)
        V = XX @ S @ XX
        fb[str(ny)] = {"b": float(coef[1]), "se": float(np.sqrt(V[1, 1])),
                       "r2": float(1 - e.var() / rx.var())}
    # ACM re-estimated
    acm = R.acm_decompose(lp, K=5, rx_mats=np.arange(6, 121, 6), pc_from=3)
    tp_ours = acm["tp"][:, 119] * 100
    y_ours = acm["y"][:, 119] * 100
    rn_ours = acm["rny"][:, 119] * 100
    return _json({"cs": cs, "fb": fb, "t": _frac_year(md), "y10": y_ours,
                  "tp10": tp_ours, "rn10": rn_ours,
                  "fit_rmse_bp": acm["fit_rmse"] * 1e4,
                  "since_cut": {k: {"y": float(y_ours[np.where(md // 100 == ym)[0][0]]),
                                    "rn": float(rn_ours[np.where(md // 100 == ym)[0][0]]),
                                    "tp": float(tp_ours[np.where(md // 100 == ym)[0][0]])}
                                for k, ym in (("2024-08", 202408), ("2025-12", 202512))},
                  "tp_1981": float(tp_ours[np.where(md // 100 == 198109)[0][0]]),
                  "tp_min": {"t": float(_frac_year(md)[int(np.argmin(tp_ours))]),
                             "v": float(np.min(tp_ours))},
                  "scope": "Full-sample descriptive GSW fit; NY Fed reference unavailable and omitted.",
                  "legacy_compute_sha256": LEGACY_COMPUTE_SHA256,
                  "sample_first": int(md[0]), "sample_last": int(md[-1]),
                  "settings": {"K": 5, "rx_mats_months": list(range(6, 121, 6)), "pc_from": 3}})


if __name__ == "__main__":
    Cache("quant18").main({"term_example": compute_example}, __doc__)
