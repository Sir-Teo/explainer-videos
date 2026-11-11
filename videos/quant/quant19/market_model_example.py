"""Dated caplet example: reset T_i, payment T_i+delta, terminal numeraire.

The legacy House demonstration's initial rate periods and option expiries use
inconsistent time origins. This separately named example keeps its algorithm
and original cache unchanged. It prices public-curve synthetic claims, not a
strategy trial, and accesses no forecast-return payload.

    python -m videos.quant.quant19.market_model_example market_model_example
"""
from __future__ import annotations

import numpy as np

from explainer.ai.cache import Cache
from explainer.quant.house import termstructure as TS
from .compute import _curve_2025

CACHE = Cache("quant19")


def caplets(curve, *, normal=False, n_paths=40000, seed=0, steps_per_period=50,
            n_rates=10, delta=0.5, sigma=None):
    """Euler terminal-measure model; freeze each payoff at its own reset.

    At reset T_i, the payment-date/terminal bond ratio equals the product
    of (1+delta*L_k(T_i)) for k>i. Using this ratio values the already fixed
    caplet without treating future fixings as current bond prices.
    """
    resets = np.arange(1, n_rates + 1) * delta
    payments = resets + delta
    initial = (curve.df(resets) / curve.df(payments) - 1) / delta
    sigma = (0.009 if normal else 0.25) if sigma is None else sigma
    sig = np.broadcast_to(np.asarray(sigma, float), (n_rates,))
    rates = np.tile(initial, (n_paths, 1))
    rng = np.random.default_rng(seed)
    pv = np.empty((n_paths, n_rates))
    terminal_df = float(curve.df(payments[-1]))
    dt = delta / steps_per_period
    for i in range(n_rates):
        for _ in range(steps_per_period):
            diffusion = np.broadcast_to(sig[i:], rates[:, i:].shape) if normal else rates[:, i:] * sig[i:]
            denominator = 1 + delta * rates[:, i:]
            if np.any(denominator <= 0):
                raise ValueError("Euler path left the positive bond-ratio domain")
            terms = delta * diffusion / denominator
            # Sum over later live forwards, excluding the current rate.
            reverse_sum = np.cumsum(terms[:, ::-1], axis=1)[:, ::-1] - terms
            brownian = rng.standard_normal((n_paths, 1)) * np.sqrt(dt)
            rates[:, i:] += diffusion * (-reverse_sum * dt + brownian)
        bond_ratio = np.prod(1 + delta * rates[:, i + 1:], axis=1)
        pv[:, i] = terminal_df * delta * np.maximum(rates[:, i] - initial[i], 0) * bond_ratio
    quote_formula = TS.bachelier if normal else TS.black_swaption
    exact = np.array([float(curve.df(payment)) * delta * (quote_formula(f, f, t, v) if v > 0 else 0.0)
                      for f, t, payment, v in zip(initial, resets, payments, sig)])
    return {"mc": pv.mean(0).tolist(), "se": (pv.std(0, ddof=1) / np.sqrt(n_paths)).tolist(),
            "exact": exact.tolist(), "T": resets.tolist(), "payment": payments.tolist()}


def compute_example():
    curve = _curve_2025()
    black, normal = caplets(curve), caplets(curve, normal=True)
    t = np.asarray(black["T"])
    d = 0.5
    initial = (curve.df(t) / curve.df(t + d) - 1) / d
    return {"T": t.tolist(), "payment": (t + d).tolist(), "L0": initial.tolist(),
            "black": black, "normal": normal, "seed": 0, "paths": 40000,
            "steps_per_period": 50, "curve_date": 20251231,
            "scope": "synthetic single-curve pricing example; no option-quote calibration or strategy-return test"}


if __name__ == "__main__":
    CACHE.main({"market_model_example": compute_example}, __doc__)
