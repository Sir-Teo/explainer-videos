"""Agora's treasury (Part 32): the government's budget constraint and debt dynamics; the spending multiplier in the
New Keynesian model, with and without the zero bound; local projections of spending multipliers (Ramey and Zubairy);
the regional multiplier and the missing intercept; tax smoothing; the fiscal theory of the price level and Sargent and
Wallace's unpleasant arithmetic; and sovereign default by value function iteration (Eaton and Gersovitz; Arellano).
numpy and scipy only."""

from __future__ import annotations

import numpy as np

from . import dp


# --- the budget constraint ----------------------------------------------------------------------------------------
def debt_path(b0: float, r: float, g: float, pb, years: int = 30) -> list:
    """Debt to GDP, b_{t+1} = b_t (1 + r) / (1 + g) - pb_t, with a primary surplus ``pb`` (a number or a path), all as
    fractions."""
    pb = np.broadcast_to(np.asarray(pb, float), (years,))
    b = [float(b0)]
    for t in range(years):
        b.append(b[-1] * (1 + r) / (1 + g) - pb[t])
    return b


def stabilizing_surplus(b: float, r: float, g: float) -> float:
    """The primary surplus that holds debt to GDP at ``b``: (r - g) / (1 + g) * b."""
    return (r - g) / (1 + g) * b


# --- the multiplier in the New Keynesian model ---------------------------------------------------------------------
NK = {"beta": 0.99, "sigma": 1.0, "kappa": 0.1275, "phi_pi": 1.5, "phi_x": 0.125, "gy": 0.2, "gamma": 0.5}


def nk_multiplier(rho: float = 0.5, zlb: bool = False, **kw) -> dict:
    """The multiplier dY/dG of a government-spending shock that decays at rate ``rho``, in the three-equation model
    of Part 30 with spending added (Woodford 2011's simple analytics).  Output y (percent of steady-state output) and
    spending g (percent of output) enter

        IS:   y_t - g_t = E(y_{t+1} - g_{t+1}) - sigma_c (i_t - E pi_{t+1}),      sigma_c = sigma (1 - gy)
        PC:   pi_t = beta E pi_{t+1} + kappa (y_t - gamma g_t)
        rule: i_t = phi_pi pi_t + phi_x y_t,  or i_t = 0 at the zero bound

    where ``gamma`` is how far spending raises the output the economy can produce at constant marginal cost (more
    work).  At the zero bound the trap lasts as long as the spending (a Markov exit with persistence ``rho``,
    Eggertsson's device), and a bounded solution needs (1 - rho)(1 - beta rho) > sigma_c kappa rho.  The solution is
    y = m g, pi = q g; ``multiplier`` is m."""
    p = {**NK, **kw}
    s = p["sigma"] * (1 - p["gy"])
    k, b, gam = p["kappa"], p["beta"], p["gamma"]
    fp, fx = (0.0, 0.0) if zlb else (p["phi_pi"], p["phi_x"])
    A = np.array([[(1 - rho) + s * fx, s * (fp - rho)], [-k, 1 - b * rho]])
    rhs = np.array([1 - rho, -k * gam])
    m, q = np.linalg.solve(A, rhs)
    ok = (not zlb) or (1 - rho) * (1 - b * rho) > s * k * rho
    return {"multiplier": float(m) if ok else float("nan"), "inflation": float(q) if ok else float("nan"),
            "rho": rho, "zlb": zlb, "bounded": bool(ok)}


def nk_multiplier_curve(rhos=None, **kw) -> dict:
    """Multipliers over the persistence of spending, in normal times and at the zero bound (NaN where the trap has
    no bounded solution)."""
    rhos = np.linspace(0.0, 0.9, 91) if rhos is None else np.asarray(rhos, float)
    return {"rho": rhos.tolist(), "normal": [nk_multiplier(r, **kw)["multiplier"] for r in rhos],
            "zlb": [nk_multiplier(r, zlb=True, **kw)["multiplier"] for r in rhos]}


# --- local projections of spending multipliers ---------------------------------------------------------------------
def _lag(x, k):
    x = np.asarray(x, float)
    return np.concatenate([np.full(k, np.nan), x[:-k]]) if k > 0 else x


def _lead(x, k):
    x = np.asarray(x, float)
    return np.concatenate([x[k:], np.full(k, np.nan)]) if k > 0 else x


def rz_series(D: dict, first: float = 1889.0) -> dict:
    """Ramey and Zubairy's variables: output and real government purchases divided by potential output (their sixth-
    degree trend), the military news shock divided by last quarter's nominal potential output, and the slack state
    (unemployment of 6.5% or more)."""
    q = np.array(D["quarter"], float)
    keep = q >= first
    v = {k: np.array(D[k], float)[keep] for k in ("ngov", "pgdp", "news", "rgdp", "rgdp_pott6", "unemp", "zlb_dummy")}
    pot = v["rgdp_pott6"]
    return {"quarter": q[keep], "y": v["rgdp"] / pot, "g": v["ngov"] / v["pgdp"] / pot,
            "news": v["news"] / (_lag(pot, 1) * _lag(v["pgdp"], 1)), "slack": (v["unemp"] >= 6.5).astype(float),
            "zlb": v["zlb_dummy"]}


def _ols(Y, X):
    ok = np.isfinite(Y) & np.all(np.isfinite(X), axis=1)
    b, *_ = np.linalg.lstsq(X[ok], Y[ok], rcond=None)
    return b, ok


def lp_multiplier(S: dict, shock: str = "news", H: int = 20, p: int = 4, state: str | None = None) -> dict:
    """Cumulative multipliers by local projections: for each horizon h, regress y_{t+h} and g_{t+h} on the shock and
    p lags of the controls (and of the news); the multiplier at H is the sum of y's coefficients over the sum of g's
    (Ramey and Zubairy 2018's two-step estimate).  ``shock`` is ``"news"`` or ``"bp"`` (current government purchases,
    Blanchard and Perotti's timing).  With ``state`` (``"slack"`` or ``"zlb"``), every coefficient is allowed to
    differ by last quarter's state; the result has both states."""
    y, g = S["y"], S["g"]
    sh = S["news"] if shock == "news" else g
    ctrl = [_lag(y, j) for j in range(1, p + 1)] + [_lag(g, j) for j in range(1, p + 1)]
    if shock == "news":
        ctrl += [_lag(S["news"], j) for j in range(1, p + 1)]
    n = len(y)
    if state is None:
        X = np.column_stack([np.ones(n), sh] + ctrl)
        by, bg = [], []
        for h in range(H + 1):
            by.append(_ols(_lead(y, h), X)[0][1])
            bg.append(1.0 if (shock == "bp" and h == 0) else _ols(_lead(g, h), X)[0][1])
        by, bg = np.array(by), np.array(bg)
        return {"h": list(range(H + 1)), "by": by.tolist(), "bg": bg.tolist(),
                "multiplier": (np.cumsum(by) / np.cumsum(bg)).tolist()}
    s = _lag(S[state], 1)
    X = np.column_stack([np.ones(n), s, sh * s, sh * (1 - s)] + [c * s for c in ctrl] + [c * (1 - s) for c in ctrl])
    out = {}
    for name, col in (("high", 2), ("low", 3)):
        by, bg = [], []
        for h in range(H + 1):
            by.append(_ols(_lead(y, h), X)[0][col])
            bg.append(1.0 if (shock == "bp" and h == 0) else _ols(_lead(g, h), X)[0][col])
        by, bg = np.array(by), np.array(bg)
        out[name] = (np.cumsum(by) / np.cumsum(bg)).tolist()
    return {"h": list(range(H + 1)), **out, "share_high": float(np.nanmean(S[state]))}


# --- regions: the local multiplier and the missing intercept ------------------------------------------------------
def regions(R: int = 48, T: int = 40, m_local: float = 1.5, m_agg: float = 0.6, sd_g: float = 1.0,
            sd_common: float = 0.4, sd_e: float = 1.5, seed: int = 0) -> dict:
    """A currency union of ``R`` regions over ``T`` years.  Each region's federal spending (percent of its output)
    moves with a common national programme and its own share of it; the national central bank leans against national
    spending but cannot treat regions differently.  So a region's output rises ``m_local`` per point of its spending
    relative to the national average, while the nation's rises only ``m_agg`` per point of national spending:

        y_rt = m_local (g_rt - gbar_t) + m_agg gbar_t + u_t + e_rt.

    A regression with year fixed effects recovers m_local (Nakamura and Steinsson's relative multiplier) and says
    nothing about m_agg, which sits in the year effects: the missing intercept."""
    rng = np.random.default_rng(seed)
    gbar = sd_g * rng.standard_normal(T)
    load = rng.uniform(0.3, 2.0, R)                      # regions differ in how much national spending lands there
    g = load[:, None] * gbar[None, :] + 0.5 * sd_g * rng.standard_normal((R, T))
    gb = g.mean(axis=0)
    u = sd_common * rng.standard_normal(T)
    y = m_local * (g - gb[None, :]) + m_agg * gb[None, :] + u[None, :] + sd_e * rng.standard_normal((R, T))
    # within-year regression (year fixed effects)
    gd, yd = g - g.mean(axis=0), y - y.mean(axis=0)
    b_fe = float((gd * yd).sum() / (gd * gd).sum())
    # pooled without fixed effects, and the national time series
    b_pool = float(np.polyfit(g.ravel(), y.ravel(), 1)[0])
    b_nat = float(np.polyfit(gb, y.mean(axis=0), 1)[0])
    return {"g": g.tolist(), "y": y.tolist(), "gbar": gb.tolist(), "ybar": y.mean(axis=0).tolist(), "b_fe": b_fe,
            "b_pool": b_pool, "b_nat": b_nat, "m_local": m_local, "m_agg": m_agg, "R": R, "T": T}


# --- tax smoothing ------------------------------------------------------------------------------------------------
def tax_smoothing(g, r: float = 0.03, growth: float = 0.0, b0: float = 0.0) -> dict:
    """Barro (1979): with the deadweight loss of a tax rising with the square of its rate, the government that must
    pay for spending ``g`` (a share of output each year, a war in the middle) does best by a constant tax rate equal
    to the annuity value of spending, letting debt absorb the war.  Compared: a balanced budget each year (tax = g)
    and the smooth rate, with the debt path and the present value of the squared rates (the deadweight loss up to a
    constant)."""
    g = np.asarray(g, float)
    T = len(g)
    R = (1 + r) / (1 + growth)
    disc = R ** -np.arange(T)
    tau = float((b0 + (g * disc).sum()) / disc.sum())
    b = [b0]
    for t in range(T):
        b.append(b[-1] * R + g[t] - tau)
    loss_bal = float((g ** 2 * disc).sum())
    loss_smooth = float((tau ** 2 * disc).sum())
    return {"t": list(range(T)), "g": g.tolist(), "tau_smooth": tau, "debt": b, "loss_balanced": loss_bal,
            "loss_smooth": loss_smooth, "ratio": loss_bal / loss_smooth}


# --- the fiscal theory of the price level, and unpleasant arithmetic -----------------------------------------------
def ftpl_price_level(B: float = 100.0, surplus: float = 2.0, r: float = 0.02) -> float:
    """The price level at which nominal debt ``B`` equals the present value of a constant real surplus: B / P =
    surplus / r."""
    return B * r / surplus


def unpleasant(T_tight: int = 5, years: int = 20, deficit: float = 0.02, b0: float = 0.4, r: float = 0.03,
               g: float = 0.02, base: float = 0.10, mu_tight: float = 0.02, mu_loose: float = 0.06) -> dict:
    """Sargent and Wallace (1981), in a simple form.  The treasury runs a primary deficit fixed in shares of output.
    The central bank's money growth mu earns seigniorage ``base * mu / (1 + mu)`` (a money base of ``base`` times
    output); bonds cover the rest.  Tight money (mu_tight) until year ``T_tight`` lets debt pile up; from then on, money
    growth must rise to the rate whose seigniorage pays the deficit plus the interest on the larger debt, so as to hold
    debt steady.  Returns the paths for a loose and a tight central bank."""
    def run(T):
        b, mu_path, b_path = b0, [], [b0]
        for t in range(years):
            if t < T:
                mu = mu_tight
            else:
                need = deficit + (r - g) / (1 + g) * b
                mu = need / max(base - need, 1e-9)
            seig = base * mu / (1 + mu)
            b = b * (1 + r) / (1 + g) + deficit - seig
            mu_path.append(mu)
            b_path.append(b)
        return {"mu": mu_path, "debt": b_path}
    loose = run(0)
    tight = run(T_tight)
    return {"years": list(range(years)), "loose": loose, "tight": tight, "T": T_tight,
            "mu_after_tight": tight["mu"][-1], "mu_loose": loose["mu"][-1]}


# --- sovereign default (Eaton and Gersovitz 1981; Arellano 2008) ----------------------------------------------------
ARELLANO = {"beta": 0.953, "sigma": 2.0, "r": 0.017, "theta": 0.282, "ycost": 0.969, "rho": 0.945, "eta": 0.025,
            "ny": 21, "nb": 200, "bmin": -0.35, "bmax": 0.0}


def arellano(tol: float = 1e-7, max_iter: int = 2000, **kw) -> dict:
    """Arellano's (2008) model of default, quarterly, by value function iteration.  Endowment y follows a log AR(1)
    (Tauchen, 21 states); the government chooses next period's assets B' (negative: debt) at the price q(B', y), or
    defaults, losing access to markets (re-entry with probability theta) and suffering output y_def = min(y, ycost *
    E[y]).  Risk-neutral lenders price q = (1 - delta(B', y)) / (1 + r), with delta the probability of default next
    quarter.  Returns the value functions, the bond price schedule, the default set and the debt policy."""
    p = {**ARELLANO, **kw}
    ch = dp.tauchen(p["ny"], p["rho"], p["eta"], m=3.0)
    ly, P = np.array(ch["z"]), np.array(ch["P"])
    y = np.exp(ly)
    B = np.linspace(p["bmin"], p["bmax"], p["nb"])
    i0 = int(np.argmin(np.abs(B)))
    ydef = np.minimum(y, p["ycost"] * float(np.dot(np.linalg.matrix_power(P, 500)[0], y)))
    s, beta = p["sigma"], p["beta"]

    def u(c):
        out = np.full(np.shape(c), -1e10)
        ok = c > 0
        out[ok] = c[ok] ** (1 - s) / (1 - s)
        return out

    Vd = u(ydef) / (1 - beta)
    Vc = np.zeros((p["ny"], p["nb"]))
    q = np.full((p["ny"], p["nb"]), 1 / (1 + p["r"]))
    for it in range(max_iter):
        Vo = np.maximum(Vc, Vd[:, None])
        EVo = P @ Vo                                   # (ny, nb'): expected value of entering next period with B'
        EVd = P @ Vd
        # consumption c[iy, iB, iB'] = y + B - q[iy, iB'] B'
        c = y[:, None, None] + B[None, :, None] - (q * B[None, :])[:, None, :]
        obj = u(c) + beta * EVo[:, None, :]
        Vc_new = obj.max(axis=2)
        pol = obj.argmax(axis=2)
        Vd_new = u(ydef) + beta * (p["theta"] * EVo[:, i0] + (1 - p["theta"]) * EVd)
        default = Vc_new < Vd_new[:, None]
        delta = P @ default.astype(float)              # (ny, nb'): probability of default next quarter
        q_new = (1 - delta) / (1 + p["r"])
        err = max(np.abs(Vc_new - Vc).max(), np.abs(Vd_new - Vd).max(), np.abs(q_new - q).max())
        Vc, Vd, q = Vc_new, Vd_new, 0.5 * q + 0.5 * q_new
        if err < tol:
            break
    return {"y": y.tolist(), "ly": ly.tolist(), "P": P.tolist(), "B": B.tolist(), "q": q.tolist(),
            "default": default.tolist(), "policy": pol.tolist(), "iterations": it + 1, "ydef": ydef.tolist(),
            "params": p}


def arellano_simulate(M: dict, T: int = 20000, seed: int = 0, burn: int = 1000) -> dict:
    """Simulate the solved model: output, debt, spreads (annualized, over the risk-free rate) and default episodes."""
    rng = np.random.default_rng(seed)
    y, P, B = np.array(M["y"]), np.array(M["P"]), np.array(M["B"])
    q, D, pol = np.array(M["q"]), np.array(M["default"], bool), np.array(M["policy"])
    p = M["params"]
    cdf = np.cumsum(P, axis=1)
    iy, ib = len(y) // 2, int(np.argmin(np.abs(B)))
    excluded = False
    ys, bs, spreads, defaults, excl = [], [], [], [], []
    for t in range(T + burn):
        dflt = False
        if excluded:
            if rng.random() < p["theta"]:
                excluded = False
                ib = int(np.argmin(np.abs(B)))
        if not excluded:
            if D[iy, ib]:
                dflt, excluded = True, True
                ib = int(np.argmin(np.abs(B)))
            else:
                nb = pol[iy, ib]
                sp = (1 / q[iy, nb]) ** 4 - (1 + p["r"]) ** 4 if q[iy, nb] > 0 else np.nan
                if t >= burn:
                    spreads.append(sp)
                ib = nb
        if t >= burn:
            ys.append(y[iy])
            bs.append(B[ib])
            defaults.append(dflt)
            excl.append(excluded)
        iy = int(np.searchsorted(cdf[iy], rng.random()))
        iy = min(iy, len(y) - 1)
    d = np.array(defaults)
    return {"y": ys[:400], "b": bs[:400], "default": d[:400].tolist(), "excluded": excl[:400],
            "default_rate_annual": float(4 * d.mean()), "mean_spread": float(np.nanmean(spreads)),
            "mean_debt": float(-np.mean([b for b, e in zip(bs, excl) if not e]))}
