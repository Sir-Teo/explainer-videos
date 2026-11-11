"""Leverage, liquidity and crises (Part 41): how losses become forced sales, and how one firm's default becomes
another's.

* Leverage arithmetic: what a fund at a target haircut must sell after a loss.
* The loss and margin spirals of Brunnermeier and Pedersen (2009), as a fixed point: sales move the price, the price
  move costs capital and raises margins, which forces more sales.
* Fire sales among banks that target leverage (Greenwood, Landier and Thesmar 2015): first-round losses, the sales
  they force, and the second-round losses those sales cause through price impact.
* Interbank clearing (Eisenberg and Noe 2001): the clearing payment vector by the fictitious default algorithm and by
  monotone iteration from above and below; default costs (Rogers and Veraart 2013); ring and complete networks and
  the phase transition of Acemoglu, Ozdaglar and Tahbaz-Salehi (2015).
* Systemic measures: CoVaR by quantile regression (Adrian and Brunnermeier 2016), MES, LRMES and SRISK (Acharya,
  Pedersen, Philippon and Richardson 2017; Brownlees and Engle 2017)."""

from __future__ import annotations

import math

import numpy as np
from scipy import optimize


# ---------------------------------------------------------------------------
# Leverage arithmetic and spirals
# ---------------------------------------------------------------------------
def deleverage(assets: float, equity: float, loss_frac: float, haircut: float) -> dict:
    """A levered holder of ``assets`` with ``equity`` loses ``loss_frac`` of the assets' value; the lender then lends
    only (1 - haircut) of the collateral, so the holder can keep at most equity / haircut of assets. Returns the
    assets after the loss, the equity, the maximum position and the sale needed."""
    a1 = assets * (1 - loss_frac)
    e1 = equity - assets * loss_frac
    cap = max(e1, 0.0) / haircut
    sale = max(a1 - cap, 0.0)
    return {"assets": a1, "equity": e1, "max_assets": cap, "sale": sale, "sale_frac": sale / a1 if a1 > 0 else 1.0,
            "leverage_before": assets / equity, "leverage_after": a1 / e1 if e1 > 0 else float("inf")}


def spiral(shock: float, A: float = 100.0, E: float = 20.0, depth: float = 400.0, m0: float = 0.2, kappa: float = 2.0,
           rounds: int = 200) -> dict:
    """Brunnermeier and Pedersen's spirals, in a minimal fixed point. A speculator holds A units of an asset (price 1)
    with equity E, financed at a margin (haircut) m. A shock moves the price by -``shock``. Each round the margin rises
    with the cumulative fall, m = min(0.9, m0 + kappa (1 - p)) (the margin spiral; kappa = 0 leaves only the loss
    spiral), the position is cut to what the equity can carry, equity / (m p), and the sale moves the price by
    (dollars sold) / depth, which marks the remaining holding down too. Returns the paths, the total fall, its
    amplification over the initial shock, the units sold and the final equity."""
    p = 1.0 - shock
    q = A
    eq = E - A * shock
    path = {"p": [1.0, p], "m": [m0, m0], "q": [A, A], "e": [E, eq]}
    for _ in range(rounds):
        m = min(0.9, m0 + kappa * (1.0 - p))
        target = max(eq, 0.0) / (m * p)
        sale = max(q - target, 0.0)
        if sale < 1e-9:
            break
        dp = sale * p / depth
        q -= sale
        p -= dp
        eq -= q * dp
        for k_, v_ in (("p", p), ("m", m), ("q", q), ("e", eq)):
            path[k_].append(v_)
        if eq <= 0 or p <= 0:
            break
    return {"path": {k_: np.asarray(v_) for k_, v_ in path.items()}, "fall": 1.0 - p,
            "amplification": (1.0 - p) / shock, "sold": A - q, "equity": eq}


# ---------------------------------------------------------------------------
# Fire sales among leverage-targeting banks
# ---------------------------------------------------------------------------
def glt_firesale(M, E, F, L, D=None) -> dict:
    """Greenwood, Landier and Thesmar's fire-sale model. M[i, k]: bank i's holdings of asset k (in dollars); E[i]: its
    equity; F[k]: the asset return shock; L[k]: price impact per dollar sold (return per dollar of net sales); banks
    sell assets in proportion to their holdings so as to return to their initial leverage. Returns the first-round
    loss, the sales, the second-round (fire-sale) loss for each bank, and the aggregate vulnerability: the
    second-round loss as a share of total equity."""
    M = np.asarray(M, float)
    E = np.asarray(E, float)
    F = np.asarray(F, float)
    L = np.asarray(L, float)
    A = M.sum(1)
    lev = A / E                                  # assets over equity
    first = M @ F                                # dollar loss (negative F is a loss)
    # to restore leverage b = A/E after a loss of x (dollars, negative), sell lev * |x| of assets
    sales = -lev * first                         # dollars sold by each bank (positive)
    weights = M / A[:, None]
    sold_k = (sales[:, None] * weights).sum(0)   # dollars of each asset sold
    dP = -L * sold_k                             # price impact on each asset
    second = (M * (1 + F)) @ dP
    return {"first": first, "sales": sales, "sold_k": sold_k, "dP": dP, "second": second,
            "AV": float(-second.sum() / E.sum()), "IV": -second / E}


# ---------------------------------------------------------------------------
# Interbank clearing
# ---------------------------------------------------------------------------
def eisenberg_noe(Lmat, e, alpha: float = 1.0, beta: float = 1.0) -> dict:
    """Clearing payments for nominal liabilities Lmat[i, j] (i owes j) and outside assets e, by the fictitious default
    algorithm: start with no defaults; solve for the payments of defaulters with non-defaulters paying in full; add
    any newly insolvent bank; repeat (at most n rounds). With alpha, beta < 1, Rogers and Veraart's default costs: a
    defaulter realises only alpha of its outside assets and beta of its interbank claims. Returns p, the default set,
    the rounds and equity."""
    Lmat = np.asarray(Lmat, float)
    e = np.asarray(e, float)
    n = len(e)
    pbar = Lmat.sum(1)
    Pi = np.divide(Lmat, pbar[:, None], out=np.zeros_like(Lmat), where=pbar[:, None] > 0)
    D = np.zeros(n, bool)
    p = pbar.copy()
    rounds = 0
    for rounds in range(1, n + 2):
        # payments: non-defaulters pay pbar; defaulters pay what they have
        p = pbar.copy()
        idx = np.flatnonzero(D)
        if idx.size:
            for _ in range(10_000):
                inflow = Pi.T @ p
                new = p.copy()
                new[idx] = np.minimum(pbar[idx], alpha * e[idx] + beta * inflow[idx])
                new[~D] = pbar[~D]
                if np.max(np.abs(new - p)) < 1e-12:
                    p = new
                    break
                p = new
        value = e + Pi.T @ p
        newD = value < pbar - 1e-12
        if np.array_equal(newD, D):
            break
        D = newD | D
    equity = e + Pi.T @ p - p
    return {"p": p, "pbar": pbar, "default": D, "rounds": rounds, "equity": equity}


def clearing_iterate(Lmat, e, start: str = "top", iters: int = 100_000) -> np.ndarray:
    """The monotone (Picard) iteration p -> min(pbar, e + Pi' p) from pbar ("top": converges to the greatest clearing
    vector) or from zero ("bottom": the least)."""
    Lmat = np.asarray(Lmat, float)
    e = np.asarray(e, float)
    pbar = Lmat.sum(1)
    Pi = np.divide(Lmat, pbar[:, None], out=np.zeros_like(Lmat), where=pbar[:, None] > 0)
    p = pbar.copy() if start == "top" else np.zeros_like(pbar)
    for _ in range(iters):
        new = np.minimum(pbar, e + Pi.T @ p)
        if np.max(np.abs(new - p)) < 1e-13:
            return new
        p = new
    return p


def ring(n: int, y: float) -> np.ndarray:
    """Each bank owes y to the next."""
    L = np.zeros((n, n))
    for i in range(n):
        L[i, (i + 1) % n] = y
    return L


def complete(n: int, y: float) -> np.ndarray:
    """Each bank owes y / (n - 1) to every other: the same total liabilities as the ring."""
    L = np.full((n, n), y / (n - 1))
    np.fill_diagonal(L, 0.0)
    return L


def contagion_sweep(Lmat, e_base, shocks, hit: int = 0) -> list[dict]:
    """Shock bank ``hit``'s outside assets by each amount and count defaults in the clearing equilibrium."""
    out = []
    for s in shocks:
        e = np.asarray(e_base, float).copy()
        e[hit] = max(e[hit] - s, 0.0)
        r = eisenberg_noe(Lmat, e)
        out.append({"shock": float(s), "defaults": int(r["default"].sum()),
                    "shortfall": float((r["pbar"] - r["p"]).sum())})
    return out


# ---------------------------------------------------------------------------
# Systemic measures
# ---------------------------------------------------------------------------
def quantile_reg(y, x, tau: float) -> tuple[float, float]:
    """Linear quantile regression y = a + b x at level tau, by minimising the pinball loss (a linear program solved
    with scipy's HiGHS)."""
    from scipy.optimize import linprog
    y = np.asarray(y, float)
    x = np.asarray(x, float)
    n = len(y)
    # variables: a+, a-, b+, b-, u (n), v (n) >= 0; y = a + b x + u - v
    c = np.r_[0, 0, 0, 0, np.full(n, tau), np.full(n, 1 - tau)]
    A_eq = np.column_stack([np.ones(n), -np.ones(n), x, -x, np.eye(n), -np.eye(n)])
    res = linprog(c, A_eq=A_eq, b_eq=y, bounds=[(0, None)] * (4 + 2 * n), method="highs")
    a = res.x[0] - res.x[1]
    b = res.x[2] - res.x[3]
    return float(a), float(b)


def quantile_reg_fast(y, x, tau: float, iters: int = 200) -> tuple[float, float]:
    """The same by iteratively reweighted least squares, for long samples."""
    y = np.asarray(y, float)
    x = np.asarray(x, float)
    X = np.column_stack([np.ones_like(x), x])
    beta = np.linalg.lstsq(X, y, rcond=None)[0]
    for _ in range(iters):
        r = y - X @ beta
        w = np.where(r >= 0, tau, 1 - tau) / np.maximum(np.abs(r), 1e-6)
        Wx = X * w[:, None]
        new = np.linalg.solve(X.T @ Wx, Wx.T @ y)
        if np.max(np.abs(new - beta)) < 1e-10:
            beta = new
            break
        beta = new
    return float(beta[0]), float(beta[1])


def covar(sys_r, inst_r, q: float = 0.05) -> dict:
    """Adrian and Brunnermeier's CoVaR: the system's q-quantile given the institution at its q-quantile, from a quantile
    regression of the system's return on the institution's; Delta-CoVaR is the change from the institution's median
    state to its distressed one."""
    a, b = quantile_reg_fast(sys_r, inst_r, q)
    vq = float(np.quantile(inst_r, q))
    v50 = float(np.median(inst_r))
    return {"alpha": a, "beta": b, "covar": a + b * vq, "covar_median": a + b * v50, "dcovar": b * (vq - v50)}


def mes(sys_r, inst_r, q: float = 0.05) -> float:
    """Marginal expected shortfall: the institution's average return on the system's worst q of days."""
    sys_r, inst_r = np.asarray(sys_r, float), np.asarray(inst_r, float)
    cut = np.quantile(sys_r, q)
    return float(inst_r[sys_r <= cut].mean())


def lrmes(mes_daily: float) -> float:
    """Acharya, Engle and Richardson's approximation of the six-month loss in a 40% market crash from daily MES at 2%:
    LRMES = 1 - exp(-18 MES), with MES as a positive loss."""
    return 1.0 - math.exp(-18.0 * mes_daily)


def srisk(debt: float, equity: float, lrmes_: float, k: float = 0.08) -> float:
    """SRISK: the capital the firm would need in a crisis, k (debt + equity after the crash) - equity after the crash,
    = k D - (1 - k)(1 - LRMES) E. Positive values are shortfalls."""
    return k * debt - (1 - k) * (1 - lrmes_) * equity


def senior_clearing(Pi, y, a, v, eps) -> dict:
    """Acemoglu, Ozdaglar and Tahbaz-Salehi's clearing with senior outside debt: bank i holds a project worth a_i -
    eps_i, owes v (senior, to outsiders) and y_i to other banks in proportions Pi[i, j]; its interbank payment is
    x_i = min(y_i, max(0, a_i - eps_i + sum_j Pi[j, i] x_j - v)). Solved by monotone iteration from full payment
    (the greatest clearing vector). Returns x and the defaulters (x_i < y_i)."""
    Pi = np.asarray(Pi, float)
    y = np.asarray(y, float)
    val = np.asarray(a, float) - np.asarray(eps, float)
    x = y.copy()
    for _ in range(100_000):
        new = np.minimum(y, np.maximum(0.0, val + Pi.T @ x - v))
        if np.max(np.abs(new - x)) < 1e-13:
            x = new
            break
        x = new
    return {"x": x, "default": x < y - 1e-10, "shortfall": float((y - x).sum())}


def ring_pi(n: int) -> np.ndarray:
    P = np.zeros((n, n))
    for i in range(n):
        P[i, (i + 1) % n] = 1.0
    return P


def complete_pi(n: int) -> np.ndarray:
    P = np.full((n, n), 1.0 / (n - 1))
    np.fill_diagonal(P, 0.0)
    return P


def clusters_pi(n: int, k: int, delta: float) -> np.ndarray:
    """k complete clusters, each bank sending a share delta of its interbank lending to the other clusters."""
    P = np.zeros((n, n))
    size = n // k
    for i in range(n):
        c = i // size
        inside = [j for j in range(c * size, (c + 1) * size) if j != i]
        outside = [j for j in range(n) if j // size != c]
        for j in inside:
            P[i, j] = (1 - delta) / len(inside)
        for j in outside:
            P[i, j] = delta / len(outside)
    return P


def dd_payoffs(f, theta: float, r: float, c1: float = 1.0) -> tuple[np.ndarray, np.ndarray]:
    """Diamond-Dybvig with a fire-sale value: each unit of the bank's asset is worth ``theta`` if held to the end and
    ``r`` < 1 if sold early; a share ``f`` of depositors withdraws ``c1`` early. Returns (early, wait) payoffs: the
    bank sells f*c1/r units to pay; if that exceeds what it has it fails, pays early withdrawers pro rata and those
    who wait get nothing."""
    f = np.asarray(f, float)
    sold = f * c1 / r
    early = np.where(sold <= 1, c1, r / np.maximum(f, 1e-12))
    wait = np.where(sold < 1, theta * np.clip(1 - sold, 0, None) / np.maximum(1 - f, 1e-12), 0.0)
    return early, wait


def run_threshold(r: float, c1: float = 1.0, insured: float = 0.0, lo: float = 0.0, hi: float = 10.0,
                  n: int = 4001) -> float:
    """The global-games run threshold (Morris-Shin; Goldstein-Pauzner): as signal noise vanishes the marginal depositor
    believes the share of others running is uniform on [0, 1], so theta* solves int_0^1 (wait - early) df = 0.
    Depositors run below theta*, stay above it: one equilibrium, not two. A share ``insured`` of deposits is insured
    and never runs, so at most 1 - insured withdraws: f = (1 - insured) u, u uniform."""
    f = (1 - insured) * (np.arange(n) + 0.5) / n

    def gap(th):
        e, w = dd_payoffs(f, th, r, c1)
        return float(np.mean(w - e))
    a, b = lo, hi
    for _ in range(80):
        m = 0.5 * (a + b)
        a, b = (m, b) if gap(m) < 0 else (a, m)
    return 0.5 * (a + b)


def margin_path(r, lev: float, h, cap_lev: float | None = None) -> dict:
    """A long book at target leverage ``lev`` through daily returns ``r``, financed with margin ``h`` (a scalar, or one
    per day): each day the book gains A r, then is set to min(lev E, E / h_t), never re-levered above that.
    Returns daily equity, assets, the leverage and the forced sales (the part of each day's cut that the margin, not
    the target, required)."""
    r = np.asarray(r, float)
    h = np.broadcast_to(np.asarray(h, float), r.shape)
    E, A = 1.0, lev
    eq, ast, sold = [], [], []
    for t in range(len(r)):
        E += A * r[t]
        A *= 1 + r[t]
        if E <= 0:
            eq.append(0.0)
            ast.append(0.0)
            sold.append(A)
            E, A = 0.0, 0.0
            continue
        target = lev * E if cap_lev is None else min(lev, cap_lev) * E
        cap = E / h[t]
        new = min(target, cap)
        forced = max(0.0, min(A, target) - new)
        sold.append(forced)
        A = new
        eq.append(E)
        ast.append(A)
    return {"equity": np.array(eq), "assets": np.array(ast), "forced": np.array(sold)}


def ewma_vol(r, lam: float = 0.94, seed: float | None = None) -> np.ndarray:
    """RiskMetrics volatility, sigma_t^2 = lam sigma_{t-1}^2 + (1 - lam) r_{t-1}^2: known at the start of day t."""
    r = np.asarray(r, float)
    s2 = np.empty_like(r)
    s2[0] = np.var(r[:20]) if seed is None else seed ** 2
    for t in range(1, len(r)):
        s2[t] = lam * s2[t - 1] + (1 - lam) * r[t - 1] ** 2
    return np.sqrt(s2)
