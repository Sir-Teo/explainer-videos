"""The firm's own arithmetic (Part 34): drawdown stops, pods and platforms, and what a disclosed statistic implies.

The drawdown-stop formulas are the classical ones for Brownian motion with drift (Taylor 1975; Lehoczky 1977): for
P&L X_t = mu t + sigma W_t, running peak M_t and drawdown D_t = M_t - X_t, the stop time tau = inf{t : D_t >= d}
has E[tau] = sigma^2/(2 mu^2) (e^a - 1 - a) with a = 2 mu d / sigma^2, and the peak at the stop M_tau is exponential
with mean sigma^2/(2 mu) (e^a - 1).  Everything here is in the units of the caller: time in years when mu and sigma
are annual."""

from __future__ import annotations

import math

import numpy as np


# ---------------------------------------------------------------------------
# The drawdown stop
# ---------------------------------------------------------------------------
def stop_time(mu: float, sigma: float, d: float) -> float:
    """E[tau_d], the expected time until the P&L first falls ``d`` below its running peak:
    sigma^2/(2 mu^2) (e^a - 1 - a), a = 2 mu d/sigma^2; d^2/sigma^2 when mu = 0. Finite for every mu."""
    if abs(mu) < 1e-12:
        return d * d / (sigma * sigma)
    a = 2 * mu * d / (sigma * sigma)
    return sigma * sigma / (2 * mu * mu) * (math.expm1(a) - a)


def peak_at_stop(mu: float, sigma: float, d: float) -> float:
    """E[M_tau], the expected running peak when the stop is hit; M_tau is exponential with this mean:
    sigma^2/(2 mu) (e^a - 1); d when mu = 0. The P&L at the stop is M_tau - d."""
    if abs(mu) < 1e-12:
        return d
    a = 2 * mu * d / (sigma * sigma)
    return sigma * sigma / (2 * mu) * math.expm1(a)


def stop_time_sharpe(S: float, delta: float) -> float:
    """E[tau] in years for a book with annual Sharpe ratio S and a stop ``delta`` annual volatilities deep:
    (e^{2 S delta} - 1 - 2 S delta)/(2 S^2)."""
    return stop_time(S, 1.0, delta)


def simulate_stop(mu: float, sigma: float, d: float, n: int = 4000, dt: float = 1 / 252, horizon: float = 50.0,
                  seed: int = 0) -> dict:
    """Monte Carlo of the stop: ``n`` paths stepped at ``dt`` until the drawdown reaches ``d`` (or ``horizon``).
    Returns the mean stop time, the mean peak at the stop, the share stopped and the stop times themselves."""
    rng = np.random.default_rng(seed)
    T = int(horizon / dt)
    x = np.zeros(n)
    m = np.zeros(n)
    alive = np.ones(n, bool)
    tau = np.full(n, np.nan)
    peak = np.full(n, np.nan)
    sd = sigma * math.sqrt(dt)
    for k in range(T):
        if not alive.any():
            break
        x[alive] += mu * dt + sd * rng.standard_normal(alive.sum())
        m = np.maximum(m, x)
        hit = alive & (m - x >= d)
        tau[hit] = (k + 1) * dt
        peak[hit] = m[hit]
        alive &= ~hit
    ok = np.isfinite(tau)
    return {"tau": float(np.mean(tau[ok])), "peak": float(np.mean(peak[ok])), "stopped": float(ok.mean()),
            "taus": tau[ok]}


def apply_stop(r, d: float, wait: int, vol=None):
    """A drawdown stop on a return series ``r`` (one per period): trade at full size until the cumulative P&L since the
    last peak falls ``d`` (in units of ``vol`` per period if given, else in return units), then stand aside for
    ``wait`` periods and restart with a fresh peak. Returns the stopped series and the number of stops."""
    r = np.asarray(r, float)
    out = np.zeros_like(r)
    pk, x, off, stops = 0.0, 0.0, 0, 0
    for t, v in enumerate(r):
        if off > 0:
            off -= 1
            if off == 0:
                pk, x = 0.0, 0.0
            continue
        out[t] = v
        x += v
        pk = max(pk, x)
        thr = d * (vol[t] if vol is not None else 1.0)
        if pk - x >= thr:
            stops += 1
            off = wait
    return out, stops


# ---------------------------------------------------------------------------
# A platform of pods
# ---------------------------------------------------------------------------
def platform(n_pm: int, years: int, skill_mean: float, skill_sd: float, vol: float, halve: float | None,
             cut: float | None, payout: float = 0.2, seed: int = 0, steps: int = 12, rho: float = 0.0) -> dict:
    """Simulate a multi-manager platform: ``n_pm`` seats, each filled by a manager with true Sharpe ratio drawn from
    N(skill_mean, skill_sd); each manager runs ``vol`` annual volatility, is halved after a drawdown of ``halve`` from
    their peak and fired at ``cut`` (both in return units, None for no rule); a fired manager is replaced by a new
    draw. Monthly steps; managers' shocks share a common factor with correlation ``rho``; the manager is paid
    ``payout`` of each positive calendar-year P&L (no claw-back).
    Returns the platform's gross and investors' P&L series, firings, and the skill of those fired against those kept."""
    rng = np.random.default_rng(seed)
    dt = 1.0 / steps
    S = rng.normal(skill_mean, skill_sd, n_pm)
    size = np.ones(n_pm)
    cum = np.zeros(n_pm)
    pk = np.zeros(n_pm)
    year_pnl = np.zeros(n_pm)
    gross, paid = [], []
    fired_skill, fired = [], 0
    for t in range(years * steps):
        z = math.sqrt(rho) * rng.standard_normal() + math.sqrt(1 - rho) * rng.standard_normal(n_pm)
        r = size * (S * vol * dt + vol * math.sqrt(dt) * z)
        cum += r
        year_pnl += r
        pk = np.maximum(pk, cum)
        dd = pk - cum
        gross.append(float(r.mean()))
        if halve is not None:
            size = np.where((dd >= halve) & (size == 1.0), 0.5, size)
        if cut is not None:
            out = dd >= cut
            if out.any():
                fired += int(out.sum())
                fired_skill += S[out].tolist()
                S[out] = rng.normal(skill_mean, skill_sd, int(out.sum()))
                size[out], cum[out], pk[out] = 1.0, 0.0, 0.0
                year_pnl[out] = 0.0
        if (t + 1) % steps == 0:
            paid.append(float(np.maximum(year_pnl, 0).mean() * payout))
            year_pnl[:] = 0.0
            # a manager whose drawdown has healed is restored to full size at the year end
            size = np.where(pk - cum < (halve or np.inf) / 2, 1.0, size)
    g = np.asarray(gross)
    ann = g.reshape(years, steps).sum(1)
    net = ann - np.asarray(paid)
    return {"gross_mean": float(ann.mean()), "gross_vol": float(g.std() * math.sqrt(steps)),
            "net_mean": float(net.mean()), "payout_share": float(np.sum(paid) / max(np.sum(ann), 1e-12)),
            "fired_per_year": fired / years / n_pm, "fired_skill": float(np.mean(fired_skill)) if fired_skill else
            float("nan"), "final_skill": float(np.mean(S)), "annual": ann, "net": net}


# ---------------------------------------------------------------------------
# What a disclosed statistic implies
# ---------------------------------------------------------------------------
def implied_daily_sharpe(losing_days: int, days: int, df: float | None = None) -> float:
    """The daily mean/sd ratio that makes P(loss) = losing_days/days, for normal daily P&L (df None) or Student-t
    with ``df`` degrees of freedom scaled to unit variance."""
    from scipy import stats

    p = losing_days / days
    if df is None:
        return float(-stats.norm.ppf(p))
    return float(-stats.t.ppf(p, df) * math.sqrt((df - 2) / df))


def binomial_upper(losing_days: int, days: int, level: float = 0.95) -> float:
    """The one-sided ``level`` upper confidence bound (Clopper-Pearson) on the daily loss probability."""
    from scipy import stats

    return float(stats.beta.ppf(level, losing_days + 1, days - losing_days))
