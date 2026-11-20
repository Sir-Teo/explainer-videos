"""Agora's expectations (Part 28): Phillips's curve, the expectations-augmented curve and acceleration, adaptive
forecasts, Lucas's signal-extraction islands, the Lucas critique under rational expectations, the Barro-Gordon game
with Rogoff's conservative banker, and the sacrifice ratio.  numpy only."""

from __future__ import annotations

import numpy as np


# --- Phillips (1958) -----------------------------------------------------------------------------------------------
def phillips1958(u):
    """Phillips's fitted curve for Britain, 1861-1913: ``y + 0.900 = 9.638 u^-1.394``, the percentage change in money
    wage rates against the percentage of the workforce unemployed."""
    u = np.asarray(u, float)
    return 9.638 * u ** -1.394 - 0.900


# --- the expectations-augmented curve -----------------------------------------------------------------------------
def accelerate(years: int = 15, ustar: float = 5.0, u_target: float = 4.0, beta: float = 0.5, lam: float = 1.0,
               pi0: float = 2.0) -> dict:
    """Friedman and Phelps: ``pi_t = pi^e_t - beta (u_t - u*)``.  Policy holds unemployment at ``u_target`` below the
    natural rate; expectations adapt, ``pi^e_t = pi^e_{t-1} + lam (pi_{t-1} - pi^e_{t-1})``.  Returns the paths: with
    ``lam = 1`` inflation rises by ``beta (u* - u_target)`` every year."""
    pe, pi = [pi0], []
    for t in range(years):
        p = pe[-1] - beta * (u_target - ustar)
        pi.append(p)
        pe.append(pe[-1] + lam * (p - pe[-1]))
    return {"pi": pi, "expected": pe[:-1], "u": [u_target] * years, "step": beta * (ustar - u_target)}


def adaptive_forecasts(series, lam: float) -> dict:
    """One-step-ahead forecasts by adaptive expectations, ``f_{t+1} = f_t + lam (x_t - f_t)``, started at the first
    observation; returns the forecasts for periods 1.., their errors and the root mean squared error."""
    x = np.asarray(series, float)
    f = np.empty(len(x))
    f[0] = x[0]
    for t in range(1, len(x)):
        f[t] = f[t - 1] + lam * (x[t - 1] - f[t - 1])
    err = x[1:] - f[1:]
    return {"forecast": f[1:].tolist(), "error": err.tolist(), "rmse": float(np.sqrt(np.mean(err ** 2))),
            "mean_error": float(err.mean())}


# --- Lucas's islands -----------------------------------------------------------------------------------------------
def signal_extraction(sigma_z: float, sigma_m: float) -> float:
    """The weight a producer puts on a price surprise as a change in its relative price:
    ``theta = sigma_z^2 / (sigma_z^2 + sigma_m^2)``."""
    return sigma_z ** 2 / (sigma_z ** 2 + sigma_m ** 2)


def lucas_islands(sigma_z: float, sigma_m: float, b: float = 1.0, n_islands: int = 200, years: int = 60,
                  seed: int = 0) -> dict:
    """Each year money (the price level) moves by ``m ~ N(0, sigma_m)``; each island's price is ``m + z_i``,
    ``z_i ~ N(0, sigma_z)``.  A producer sees only its own price and supplies ``b * theta * (p_i - E m)``.  Aggregate
    output is ``b * theta * m``: the more volatile money is, the less output responds to it."""
    rng = np.random.default_rng(seed)
    th = signal_extraction(sigma_z, sigma_m)
    m = rng.normal(0, sigma_m, years)
    z = rng.normal(0, sigma_z, (years, n_islands))
    y = b * th * (m[:, None] + z)
    agg = y.mean(axis=1)
    slope = float(np.polyfit(m, agg, 1)[0])
    return {"theta": th, "m": m.tolist(), "y": agg.tolist(), "slope": slope}


def critique(ystar: float = 100.0, b: float = 2.0, pibar_old: float = 2.0, pibar_new: float = 6.0, sd: float = 1.5,
             years: int = 40, seed: int = 0) -> dict:
    """The Lucas critique with rational expectations.  Under the old rule inflation is ``pibar_old + e``, people
    expect ``pibar_old``, and output is ``y* + b (pi - pi^e) + u``.  An econometrician fits ``y = a + c pi`` on the old
    rule's data and predicts that the new rule (``pibar_new``) raises output by ``c (pibar_new - pibar_old)``; under
    the new rule people expect ``pibar_new`` and output does not rise at all."""
    rng = np.random.default_rng(seed)
    e1, e2 = rng.normal(0, sd, years), rng.normal(0, sd, years)
    u1, u2 = rng.normal(0, 0.5, years), rng.normal(0, 0.5, years)
    pi1, pi2 = pibar_old + e1, pibar_new + e2
    y1, y2 = ystar + b * e1 + u1, ystar + b * e2 + u2
    c, a = np.polyfit(pi1, y1, 1)
    predicted = a + c * pibar_new
    return {"pi_old": pi1.tolist(), "y_old": y1.tolist(), "pi_new": pi2.tolist(), "y_new": y2.tolist(),
            "slope": float(c), "intercept": float(a), "predicted": float(predicted), "actual": float(y2.mean()),
            "old_mean": float(y1.mean())}


# --- Barro and Gordon, Rogoff -----------------------------------------------------------------------------------
def barro_gordon(lam: float, k: float, b: float = 1.0) -> dict:
    """Society's loss ``pi^2 / 2 + (lam / 2)(y - y* - k)^2`` with ``y - y* = b (pi - pi^e)``.  Under discretion the
    central bank takes ``pi^e`` as given; in equilibrium ``pi^e = pi``, so output stays at ``y*`` and inflation is
    ``lam b k``: all cost, no gain.  Under a rule ``pi = 0`` with the same output."""
    pi_d = lam * b * k
    loss_d = 0.5 * pi_d ** 2 + 0.5 * lam * k ** 2
    loss_r = 0.5 * lam * k ** 2
    # the temptation: from the rule, surprise inflation pays off once
    pi_cheat = lam * b * k / (1 + lam * b * b)
    y_cheat = b * pi_cheat
    loss_cheat = 0.5 * pi_cheat ** 2 + 0.5 * lam * (y_cheat - k) ** 2
    return {"pi_discretion": pi_d, "loss_discretion": loss_d, "loss_rule": loss_r, "pi_cheat": pi_cheat,
            "loss_cheat": loss_cheat}


def conservative_banker(lam: float, k: float, sigma: float, b: float = 1.0, weights=None) -> dict:
    """Rogoff (1985): society (weight ``lam`` on output) appoints a central banker with weight ``w``.  With supply
    shocks ``y - y* = b (pi - pi^e) + e``, ``e ~ (0, sigma^2)``, the banker's discretionary inflation is
    ``w b k - (w b / (1 + w b^2)) e`` and the output gap ``e / (1 + w b^2)``.  Society's expected loss is
    ``[(w b k)^2 + (w b / (1 + w b^2))^2 sigma^2] / 2 + (lam / 2)(k^2 + sigma^2 / (1 + w b^2)^2)``; it is smallest at
    some ``w`` between 0 and ``lam``."""
    ws = np.linspace(0.0, 1.5 * lam, 301) if weights is None else np.asarray(weights, float)

    def loss_at(w):
        w = np.asarray(w, float)
        d = 1 + w * b * b
        return 0.5 * ((w * b * k) ** 2 + (w * b / d) ** 2 * sigma ** 2) + 0.5 * lam * (k ** 2 + sigma ** 2 / d ** 2)
    loss = loss_at(ws)
    i = int(np.argmin(loss))
    return {"w": ws.tolist(), "loss": loss.tolist(), "best": float(ws[i]), "best_loss": float(loss[i]),
            "loss_at_lam": float(loss_at(lam)), "loss_at_zero": float(loss_at(0.0))}


# --- disinflation ---------------------------------------------------------------------------------------------------
def sacrifice_ratio(output_gap, inflation_start: float, inflation_end: float) -> dict:
    """Point-years of output lost (the sum of negative output gaps, in percent of potential, over years) per point
    by which trend inflation fell."""
    g = np.asarray(output_gap, float)
    lost = float(-g[g < 0].sum())
    fall = inflation_start - inflation_end
    return {"lost": lost, "fall": float(fall), "ratio": lost / fall if fall else float("nan")}


def persistence(series) -> float:
    """The first-order autocorrelation of a series."""
    x = np.asarray(series, float)
    x = x[np.isfinite(x)]
    return float(np.corrcoef(x[:-1], x[1:])[0, 1])
