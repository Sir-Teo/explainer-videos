"""Counterparty risk, valuation adjustments and clearing (Part 21).

Exposure: a portfolio's future values along simulated paths (Hull-White, Part 19), netted, with or without
collateral (a threshold, a minimum transfer and a margin period of risk); expected exposure, expected negative
exposure and potential future exposure.

Adjustments: CVA and DVA as integrals of discounted exposure against default probabilities (Gregory; Brigo and
Masetti 2005), with first-to-default survival; FVA as the cost of funding uncollateralised exposure at a spread
(Burgard and Kjaer 2011), and the debate about whether it belongs in prices (Hull and White 2012); KVA and MVA as the
cost of holding capital and initial margin over the trade's life. Wrong-way risk by a Gaussian copula between the
counterparty's default time and the rate factor.

Sensitivities: the whole CVA computation written in torch, so one backward pass returns its derivative with respect
to every input curve node and hazard rate (adjoint algorithmic differentiation, Part 16), checked against bumping.

Margin and capital: a SIMM-style delta initial margin (risk weights and correlations by tenor; illustrative, not
ISDA's calibration), SA-CCR's exposure at default for interest-rate swaps (the Basel formula), and a CCP's default
waterfall under member defaults.
"""

from __future__ import annotations

import numpy as np

from explainer.quant.house import credit as CR


# ---------------------------------------------------------------------------
# Exposure
# ---------------------------------------------------------------------------
def swap_values_hw(hw, x, t, K, T_end, freq=1, notional=1.0, payer=True, start=0.0):
    """Mark-to-market of a swap paying (payer) or receiving fixed K, at time t on each path's Hull-White state x
    (array), for the remaining fixed dates in (max(t, start), T_end]; the floating leg is valued at par at the next
    reset (an approximation that ignores the accrued fixing, standard for exposure sketches)."""
    x = np.asarray(x, float)
    pay = start + np.arange(1, int(round((T_end - start) * freq)) + 1) / freq
    fut = pay[pay > t + 1e-12]
    if len(fut) == 0:
        return np.zeros_like(x)
    prev = max(t, fut[0] - 1 / freq)
    P = hw.zcb(t, fut[None, :], x[:, None])
    Pprev = hw.zcb(t, np.array([prev])[None, :], x[:, None])[:, 0] if prev > t + 1e-12 else np.ones_like(x)
    ann = P.sum(1) / freq
    float_leg = Pprev - P[:, -1]
    fixed_leg = K * ann
    v = float_leg - fixed_leg
    return notional * (v if payer else -v)


def exposure_profile(V, q=0.95):
    """From portfolio values V (paths, dates): expected exposure E[max(V, 0)], expected negative exposure
    E[min(V, 0)], and potential future exposure, the q-quantile of max(V, 0)."""
    V = np.asarray(V, float)
    pos = np.maximum(V, 0.0)
    return {"EE": pos.mean(0), "ENE": np.minimum(V, 0.0).mean(0), "PFE": np.quantile(pos, q, axis=0),
            "EPE": float(pos.mean())}


def collateralised(V, times, threshold=0.0, mta=0.0, mpor=10 / 252):
    """Variation margin with a threshold, a minimum transfer amount and a margin period of risk: the collateral held
    at t is what was called at t - MPOR (the last call before the counterparty stopped paying), above the
    threshold, rounded down by the MTA. Returns the exposure V(t) - C(t)."""
    V = np.asarray(V, float)
    times = np.asarray(times, float)
    lag = np.searchsorted(times, times - mpor + 1e-12, side="right") - 1
    Vl = V[:, np.clip(lag, 0, None)]
    Vl[:, lag < 0] = 0.0
    C = np.sign(Vl) * np.maximum(np.abs(Vl) - threshold, 0.0)
    if mta > 0:
        C = np.where(np.abs(C) < mta, 0.0, C)
    return V - C


# ---------------------------------------------------------------------------
# Valuation adjustments
# ---------------------------------------------------------------------------
def default_density(times, knots, hazards):
    """P(tau in (t_{i-1}, t_i]) on the exposure grid (t_0 = 0)."""
    Q = CR.survival(np.r_[0.0, np.asarray(times, float)], knots, hazards)
    return Q[:-1] - Q[1:]


def cva(EE, times, df, knots, hazards, R=0.4, own=None):
    """Unilateral CVA = (1 - R) sum EE(t_i) P(0, t_i) P(tau in bucket i); with ``own`` = (knots, hazards) of the
    bank itself, the bilateral (first-to-default) version weights by the bank's own survival too."""
    times = np.asarray(times, float)
    dQ = default_density(times, knots, hazards)
    w = CR.survival(times, *own) if own is not None else 1.0
    return float((1 - R) * np.sum(np.asarray(EE) * df(times) * dQ * w))


def dva(ENE, times, df, own_knots, own_hazards, R=0.4, cpty=None):
    """DVA = -(1 - R) sum ENE(t_i) P(0, t_i) P(own default in bucket i): the value to the bank of its own default.
    A gain that grows as the bank's credit worsens."""
    times = np.asarray(times, float)
    dQ = default_density(times, own_knots, own_hazards)
    w = CR.survival(times, *cpty) if cpty is not None else 1.0
    return float(-(1 - R) * np.sum(np.asarray(ENE) * df(times) * dQ * w))


def fva(EE, ENE, times, df, spread_borrow, spread_lend=None, survival=None):
    """Funding value adjustment, symmetric form: the cost of funding positive uncollateralised exposure at the bank's
    borrowing spread, less the benefit of negative exposure at its lending spread (Burgard and Kjaer 2011)."""
    times = np.asarray(times, float)
    dt = np.diff(np.r_[0.0, times])
    s = 1.0 if survival is None else survival
    sl = spread_borrow if spread_lend is None else spread_lend
    fca = float(np.sum(spread_borrow * np.asarray(EE) * df(times) * dt * s))
    fba = float(np.sum(sl * np.asarray(ENE) * df(times) * dt * s))
    return {"FCA": fca, "FBA": fba, "FVA": fca + fba}


def capital_cost(profile, times, df, rate=0.10):
    """KVA (or MVA with an initial-margin profile and a funding spread as ``rate``): sum rate x profile x dt x P."""
    times = np.asarray(times, float)
    dt = np.diff(np.r_[0.0, times])
    return float(np.sum(rate * np.asarray(profile) * df(times) * dt))


def wrong_way_cva(V, x, times, df, hazard, R=0.4, rho=0.5, seed=0):
    """CVA with the counterparty's default time correlated with the rate factor: a Gaussian copula between each
    path's default time and its terminal state. rho > 0 makes default likelier on the paths where the bank's
    exposure is largest (wrong-way risk); rho < 0, right-way. Returns the CVA by simulation."""
    from scipy.stats import norm
    rng = np.random.default_rng(seed)
    V, x = np.asarray(V, float), np.asarray(x, float)
    zx = (x[:, -1] - x[:, -1].mean()) / (x[:, -1].std() + 1e-12)
    sign = np.sign(np.corrcoef(zx, np.maximum(V, 0).mean(1))[0, 1] or 1.0)
    u = rho * sign * zx + np.sqrt(1 - rho ** 2) * rng.standard_normal(len(zx))
    tau = -np.log(norm.cdf(-u)) / hazard  # high u = early default
    times = np.asarray(times, float)
    k = np.searchsorted(times, tau)
    hit = k < len(times)
    loss = np.zeros(len(tau))
    idx = np.where(hit)[0]
    loss[idx] = np.maximum(V[idx, k[idx]], 0.0) * df(times[k[idx]])
    return float((1 - R) * loss.mean())


# ---------------------------------------------------------------------------
# AAD: the CVA of a swap book in torch
# ---------------------------------------------------------------------------
def cva_torch(zero_nodes_t, zero_nodes, hazard_nodes_t, hazards, a, sigma, swaps, times, n_paths=20000, seed=0, R=0.4):
    """CVA of a book of swaps under Hull-White, written in torch so that one backward pass returns dCVA with respect
    to every zero-rate node and every hazard. The curve is piecewise-linear in zero rates; swaps are (K, T_end,
    notional, payer). Returns (cva, grad_zero, grad_hazard) as numpy."""
    import torch
    torch.manual_seed(seed)
    zt = torch.tensor(np.asarray(zero_nodes_t, float), dtype=torch.float64)
    z = torch.tensor(np.asarray(zero_nodes, float), dtype=torch.float64, requires_grad=True)
    ht = torch.tensor(np.asarray(hazard_nodes_t, float), dtype=torch.float64)
    h = torch.tensor(np.asarray(hazards, float), dtype=torch.float64, requires_grad=True)

    def zero(t):
        t = torch.as_tensor(t, dtype=torch.float64)
        idx = torch.clamp(torch.searchsorted(zt, t), 1, len(zt) - 1)
        t0, t1 = zt[idx - 1], zt[idx]
        w = torch.clamp((t - t0) / (t1 - t0), 0, 1)
        return z[idx - 1] * (1 - w) + z[idx] * w

    def P0(t):
        t = torch.as_tensor(t, dtype=torch.float64)
        return torch.exp(-zero(t) * t)

    def B(t, T):
        return (1 - torch.exp(-a * (T - t))) / a

    def Vint(t, T):
        d = T - t
        return sigma ** 2 / a ** 2 * (d + 2 / a * torch.exp(-a * d) - 1 / (2 * a) * torch.exp(-2 * a * d) - 3 / (2 * a))

    def zcb(t, T, x):
        t = torch.as_tensor(t, dtype=torch.float64)
        return P0(T) / P0(t) * torch.exp(0.5 * (Vint(t, T) - Vint(torch.zeros(()), T) + Vint(torch.zeros(()), t))
                                         - B(t, T) * x)
    times_t = torch.tensor(np.asarray(times, float), dtype=torch.float64)
    # exact OU simulation of x on the exposure dates (the noise does not depend on the inputs being differentiated)
    gen = np.random.default_rng(seed)
    xs, xp, tp = [], torch.zeros(n_paths, dtype=torch.float64), 0.0
    for t in np.asarray(times, float):
        dt = t - tp
        e = np.exp(-a * dt)
        sd = sigma * np.sqrt((1 - e ** 2) / (2 * a))
        xp = xp * e + sd * torch.tensor(gen.standard_normal(n_paths), dtype=torch.float64)
        xs.append(xp)
        tp = t
    X = torch.stack(xs, 1)
    Vtot = torch.zeros_like(X)
    for K, Tend, N, payer in swaps:
        pay = torch.arange(1, int(round(Tend)) + 1, dtype=torch.float64)
        for j, t in enumerate(np.asarray(times, float)):
            fut = pay[pay > t + 1e-12]
            if len(fut) == 0:
                continue
            P = zcb(t, fut[None, :], X[:, j:j + 1])
            prev = max(t, float(fut[0]) - 1.0)
            Pp = zcb(t, torch.tensor([prev], dtype=torch.float64)[None, :], X[:, j:j + 1])[:, 0] if prev > t + 1e-12 \
                else torch.ones(n_paths, dtype=torch.float64)
            v = (Pp - P[:, -1]) - K * P.sum(1)
            Vtot[:, j] = Vtot[:, j] + N * (v if payer else -v)
    EE = torch.clamp(Vtot, min=0).mean(0)
    # survival from piecewise-flat hazards
    edges = torch.cat([torch.zeros(1, dtype=torch.float64), ht])
    tt = torch.cat([torch.zeros(1, dtype=torch.float64), times_t])
    cum = torch.zeros_like(tt)
    for i in range(len(h)):
        lo, hi = edges[i], (edges[i + 1] if i < len(h) - 1 else torch.tensor(1e9, dtype=torch.float64))
        cum = cum + h[i] * torch.clamp(torch.minimum(tt, hi) - lo, min=0)
    Q = torch.exp(-cum)
    dQ = Q[:-1] - Q[1:]
    c = (1 - R) * torch.sum(EE * P0(times_t) * dQ)
    c.backward()
    return float(c.detach()), z.grad.numpy().copy(), h.grad.numpy().copy()


# ---------------------------------------------------------------------------
# Initial margin, capital and clearing
# ---------------------------------------------------------------------------
SIMM_TENORS = np.array([0.5, 1, 2, 3, 5, 10, 15, 20, 30])
SIMM_RW = np.array([65, 56, 52, 49, 49, 51, 51, 51, 54], float)  # bp per bp of DV01, illustrative SIMM-style


def simm_like_ir_delta(dv01_by_tenor, rw=SIMM_RW, tenors=SIMM_TENORS, decay=0.3):
    """A SIMM-style interest-rate delta margin: weighted sensitivities WS_k = RW_k s_k (s_k the DV01 at tenor k), and
    IM = sqrt(sum_kl rho_kl WS_k WS_l) with correlations falling with tenor distance. Illustrative weights; ISDA's
    calibration differs by currency and version."""
    s = np.asarray(dv01_by_tenor, float)
    WS = rw * s
    lt = np.log(tenors)
    rho = np.exp(-decay * np.abs(lt[:, None] - lt[None, :]))
    return float(np.sqrt(max(WS @ rho @ WS, 0.0)))


def sa_ccr_ir_ead(trades, collateral=0.0, margined=False, mpor_days=10):
    """SA-CCR exposure at default for a netting set of interest-rate swaps in one currency (Basel, 2014):
    EAD = 1.4 (RC + multiplier x AddOn). Trades are dicts with notional, start S, end E (years), delta +1 payer
    or -1 receiver, and mtm. Supervisory factor 0.5%; supervisory duration (e^{-0.05 S} - e^{-0.05 E})/0.05;
    maturity buckets < 1y, 1-5y, > 5y with the Basel cross-bucket correlations."""
    sf = 0.005
    D = {0: 0.0, 1: 0.0, 2: 0.0}
    V = 0.0
    for tr in trades:
        S, E = tr.get("S", 0.0), tr["E"]
        SD = (np.exp(-0.05 * S) - np.exp(-0.05 * E)) / 0.05
        M = E
        mf = 1.5 * np.sqrt(mpor_days / 250) if margined else np.sqrt(min(max(M, 10 / 250), 1.0))
        b = 0 if E < 1 else (1 if E <= 5 else 2)
        D[b] += tr["delta"] * tr["notional"] * SD * mf
        V += tr["mtm"]
    eff = np.sqrt(D[0] ** 2 + D[1] ** 2 + D[2] ** 2 + 1.4 * D[0] * D[1] + 1.4 * D[1] * D[2] + 0.6 * D[0] * D[2])
    addon = sf * eff
    C = collateral
    RC = max(V - C, 0.0)
    floor = 0.05
    mult = min(1.0, floor + (1 - floor) * np.exp((V - C) / (2 * (1 - floor) * addon))) if addon > 0 else 1.0
    return {"EAD": 1.4 * (RC + mult * addon), "RC": RC, "AddOn": addon, "multiplier": mult}


def ccp_waterfall(losses, im_defaulter, df_defaulter, skin, df_survivors, assessments):
    """Allocate each scenario's loss from member defaults through a CCP's waterfall: the defaulters' initial margin,
    their default-fund contributions, the CCP's own capital ('skin in the game'), the surviving members' default
    fund, then assessments; whatever remains is uncovered. Returns the loss absorbed by each layer, per scenario."""
    L = np.asarray(losses, float).copy()
    out = {}
    for name, cap in (("defaulter IM", im_defaulter), ("defaulter fund", df_defaulter), ("CCP capital", skin),
                      ("survivors' fund", df_survivors), ("assessments", assessments)):
        cap = np.broadcast_to(np.asarray(cap, float), L.shape)
        take = np.minimum(L, cap)
        out[name] = take
        L = L - take
    out["uncovered"] = L
    return out
