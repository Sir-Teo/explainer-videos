"""The arbitrage checker (Part 9, research): the fundamental theorem in one period, super-replication, static checks
on a surface of option prices, martingale optimal transport bounds, and Ross recovery.  Used on every surface the
House prices against; tested in ``tests/test_quant_house.py``.

* ``ftap``: given payoffs D (assets x states) and prices p, either strictly positive state prices psi with D psi = p
  exist, or an arbitrage portfolio does (Farkas's lemma), found by linear programming;
* ``superhedge``: the cheapest portfolio whose payoff dominates a claim, and the richest one it dominates: the
  no-arbitrage price interval in an incomplete market;
* ``static_checks``: call prices across strikes must be decreasing, convex and within their bounds, and total implied
  variance must not fall with maturity;
* ``mot_bounds``: the range of prices of a path-dependent claim consistent with two maturities' marginals and the
  martingale property (Beiglboeck, Henry-Labordere and Penkner 2013), as a linear program;
* ``ross_recovery``: Perron-Frobenius on a state-price transition matrix (Ross 2015), and what it recovers when the
  pricing kernel has a permanent component (Borovicka, Hansen and Scheinkman 2016).
"""

from __future__ import annotations

import numpy as np
from scipy import sparse
from scipy.optimize import linprog


# ---------------------------------------------------------------------------
def parity_gap(C, P, S, K, T, r=0.0, q=0.0):
    """C - P - (S e^{-qT} - K e^{-rT}): zero without arbitrage, frictions aside."""
    return np.asarray(C) - np.asarray(P) - (np.asarray(S) * np.exp(-q * np.asarray(T)) - np.asarray(K) * np.exp(-r * np.asarray(T)))


def ftap(D, p) -> dict:
    """One period, finitely many states.  Returns ``no_arbitrage`` and either strictly positive state prices ``psi``
    with D psi = p (maximizing the smallest one) or an arbitrage portfolio ``theta`` (cost theta.p <= 0 and payoff
    D^T theta >= 0, not identically zero, normalized to total payoff 1)."""
    D, p = np.asarray(D, float), np.asarray(p, float)
    n, m = D.shape
    # maximize t subject to psi_j >= t, D psi = p, t <= 1
    c = np.zeros(m + 1)
    c[-1] = -1.0
    A_ub = np.hstack([-np.eye(m), np.ones((m, 1))])
    A_eq = np.hstack([D, np.zeros((n, 1))])
    res = linprog(c, A_ub=A_ub, b_ub=np.zeros(m), A_eq=A_eq, b_eq=p, bounds=[(0, None)] * m + [(None, 1.0)],
                  method="highs")
    if res.status == 0 and res.x[-1] > 1e-10:
        return {"no_arbitrage": True, "psi": res.x[:m], "min_psi": float(res.x[-1])}
    # an arbitrage: minimize theta.p subject to D^T theta >= 0, sum(D^T theta) = 1, |theta| <= big
    res = linprog(p, A_ub=-D.T, b_ub=np.zeros(m), A_eq=D.sum(axis=1)[None, :], b_eq=[1.0],
                  bounds=[(-1e6, 1e6)] * n, method="highs")
    theta = res.x
    return {"no_arbitrage": False, "theta": theta, "cost": float(theta @ p), "payoff": D.T @ theta}


def superhedge(D, p, X) -> dict:
    """Bounds on the price of a claim with state payoffs X: upper = min theta.p s.t. D^T theta >= X, lower =
    max theta.p s.t. D^T theta <= X.  Equal when the claim is replicable."""
    D, p, X = np.asarray(D, float), np.asarray(p, float), np.asarray(X, float)
    n = D.shape[0]
    up = linprog(p, A_ub=-D.T, b_ub=-X, bounds=[(None, None)] * n, method="highs")
    lo = linprog(-p, A_ub=D.T, b_ub=X, bounds=[(None, None)] * n, method="highs")
    return {"upper": float(up.fun), "lower": float(-lo.fun), "theta_up": up.x, "theta_lo": lo.x}


# ---------------------------------------------------------------------------
def static_checks(K, C, F, df=1.0, tol=1e-10) -> dict:
    """Call prices C(K) on one maturity (forward F, discount df): monotone decreasing (no call spread for free),
    convex (no negative butterfly), and df max(F - K, 0) <= C <= df F.  Returns the violations."""
    K, C = np.asarray(K, float), np.asarray(C, float)
    o = np.argsort(K)
    K, C = K[o], C[o]
    slope = np.diff(C) / np.diff(K)
    mono = np.where(slope > tol)[0]
    steep = np.where(slope < -df - tol)[0]
    fly = np.where(np.diff(slope) < -tol)[0]
    lo = np.where(C < df * np.maximum(F - K, 0) - tol)[0]
    hi = np.where(C > df * F + tol)[0]
    return {"monotone": mono.tolist(), "slope": steep.tolist(), "butterfly": fly.tolist(), "lower": lo.tolist(),
            "upper": hi.tolist(), "ok": not (len(mono) or len(steep) or len(fly) or len(lo) or len(hi))}


def calendar_check(k, w_short, w_long, tol=1e-10) -> list:
    """Total implied variance at the same log-moneyness must not fall with maturity (no calendar arbitrage)."""
    return np.where(np.asarray(w_long) < np.asarray(w_short) - tol)[0].tolist()


# ---------------------------------------------------------------------------
def mot_bounds(x, mu, y, nu, cost) -> dict:
    """min and max of sum pi_ij c(x_i, y_j) over couplings pi >= 0 with row sums mu, column sums nu and the martingale
    condition sum_j pi_ij (y_j - x_i) = 0 for every i.  ``mu`` and ``nu`` must have equal means and be in convex order.
    Returns both values and both optimal couplings."""
    x, mu, y, nu = (np.asarray(a, float) for a in (x, mu, y, nu))
    n, m = len(x), len(y)
    C = np.asarray([[cost(a, b) for b in y] for a in x]).ravel()
    rows, cols, vals = [], [], []
    r = 0
    for i in range(n):  # row sums
        rows += [r] * m
        cols += list(i * m + np.arange(m))
        vals += [1.0] * m
        r += 1
    for j in range(m):  # column sums
        rows += [r] * n
        cols += list(np.arange(n) * m + j)
        vals += [1.0] * n
        r += 1
    for i in range(n):  # martingale
        rows += [r] * m
        cols += list(i * m + np.arange(m))
        vals += list(y - x[i])
        r += 1
    A = sparse.csr_matrix((vals, (rows, cols)), shape=(r, n * m))
    b = np.concatenate([mu, nu, np.zeros(n)])
    out = {}
    for name, sign in (("lower", 1.0), ("upper", -1.0)):
        res = linprog(sign * C, A_eq=A, b_eq=b, bounds=(0, None), method="highs")
        if res.status != 0:
            raise ValueError(f"MOT {name} infeasible: {res.message} (are the marginals in convex order?)")
        out[name] = float(sign * res.fun)
        out[f"pi_{name}"] = res.x.reshape(n, m)
    return out


def convex_order_fix(x, mu, y, nu):
    """Discretized marginals rarely have exactly equal means; shift the later grid so the means agree."""
    return np.asarray(y) + (np.dot(x, mu) - np.dot(y, nu))


# ---------------------------------------------------------------------------
def ross_recovery(P) -> dict:
    """Ross (2015): a state-price transition matrix P (P_ij = price today, in state i, of 1 tomorrow in state j)
    factors as P = delta D^{-1} F D if the pricing kernel is a discount factor times a ratio of a function of the
    state.  The Perron root delta and its positive eigenvector z give the recovered transition probabilities
    F_ij = P_ij z_j / (delta z_i)."""
    P = np.asarray(P, float)
    w, V = np.linalg.eig(P)
    k = int(np.argmax(w.real))
    delta = float(w[k].real)
    z = np.abs(V[:, k].real)
    F = P * z[None, :] / (delta * z[:, None])
    return {"delta": delta, "z": z, "F": F}


# ---------------------------------------------------------------------------
# Added for Part 9's expansion: the forward from parity on raw trades, a teaching simplex, dynamic
# super-replication on a trinomial tree, power iteration for Ross recovery, MOT duals, and entropic MOT.
# ---------------------------------------------------------------------------
def implied_forward(trades, window=600.0, max_logm=0.2, min_T=1 / 365) -> list:
    """Put-call parity on raw Deribit option trades (inverse options, prices in BTC): C - P = 1 - K/F, so every call
    trade with a put trade at the same expiry and strike within ``window`` seconds reveals F = K / (1 - (C - P)).
    Returns rows (T, K / index, F / index from mark prices, F / index from trade prices, expiry 'YYYY-MM-DD')."""
    from collections import defaultdict
    from explainer.quant.house import surface

    by = defaultdict(list)
    for t in trades:
        exp, K, cp = surface.parse_instrument(t["instrument_name"])
        s = t["timestamp"] / 1e3
        T = (exp.timestamp() - s) / surface.YEAR
        if T > min_T:
            by[(exp, K, cp)].append((s, t["mark_price"], t["price"], t["index_price"], T))
    rows = []
    for (e, K, cp), calls in by.items():
        if cp != 1 or (e, K, -1) not in by:
            continue
        puts = by[(e, K, -1)]
        pt = np.array([p[0] for p in puts])
        for s, cm, cpx, ci, T in calls:
            j = int(np.argmin(np.abs(pt - s)))                      # the nearest put trade in time
            if abs(pt[j] - s) > window or abs(np.log(K / ci)) > max_logm:
                continue
            ind = 0.5 * (ci + puts[j][3])
            dm, dt = cm - puts[j][1], cpx - puts[j][2]                # C - P, on marks and on trade prices
            if dm < 1 - 1e-9 and dt < 1 - 1e-9:
                rows.append((T, K / ind, K / (1 - dm) / ind, K / (1 - dt) / ind, e.strftime("%Y-%m-%d")))
    return rows


def simplex(c, A_eq, b_eq, trace=True, max_iter=500, tol=1e-10) -> dict:
    """A teaching simplex: minimize c.x subject to A x = b, x >= 0, on a dense tableau, two phases, Bland's rule
    (the lowest-index improving column enters, ties in the ratio test leave by lowest basis index), so it never
    cycles.  Returns ``status`` ('optimal', 'infeasible', 'unbounded'), ``x``, ``fun`` and, with ``trace``, every
    pivot as (phase, entering, leaving, objective, x).  When infeasible, ``farkas`` is a y with A^T y >= 0 and
    b.y < 0, read from the phase-1 duals: the certificate that no x >= 0 solves A x = b (Farkas's lemma; for the
    fundamental theorem's LP its first rows are an arbitrage portfolio: negative cost, payoff never negative)."""
    A, b, c = np.array(A_eq, float), np.array(b_eq, float), np.array(c, float)
    m, n = A.shape
    sgn = np.where(b < 0, -1.0, 1.0)
    A, b = A * sgn[:, None], b * sgn
    T = np.hstack([A, np.eye(m), b[:, None]])                         # [A | I | b], artificials in the basis
    basis = list(range(n, n + m))
    steps = []

    def x_now():
        x = np.zeros(n + m)
        x[basis] = T[:, -1]
        return x

    def run(cost, cols, phase):
        for _ in range(max_iter):
            r = cost - cost[basis] @ T[:, :-1]                        # reduced costs
            enter = [j for j in cols if r[j] < -tol]
            if not enter:
                return "optimal"
            j = enter[0]                                              # Bland: the first improving column
            col = T[:, j]
            if not (col > tol).any():
                return "unbounded"
            ratio = np.where(col > tol, T[:, -1] / np.where(col > tol, col, 1.0), np.inf)
            i = min((k for k in range(m) if ratio[k] <= ratio.min() + tol), key=lambda k: basis[k])
            T[i] /= T[i, j]                                           # pivot on (i, j)
            for k in range(m):
                if k != i:
                    T[k] -= T[k, j] * T[i]
            left, basis[i] = basis[i], j
            if trace:
                x = x_now()
                steps.append((phase, j, left, float(cost @ x), x[:n].copy()))
        raise RuntimeError("simplex: iteration limit")

    c1 = np.r_[np.zeros(n), np.ones(m)]
    run(c1, range(n + m), 1)
    if c1[basis] @ T[:, -1] > 1e-8:
        y = c1[basis] @ T[:, n:n + m]                                 # phase-1 duals: c_B B^-1
        return {"status": "infeasible", "farkas": -y * sgn, "steps": steps}
    for i, j in enumerate(basis):                                     # drive leftover artificials out
        if j >= n:
            nz = [k for k in range(n) if abs(T[i, k]) > tol]
            if nz:
                k = nz[0]
                T[i] /= T[i, k]
                for r_ in range(m):
                    if r_ != i:
                        T[r_] -= T[r_, k] * T[i]
                basis[i] = k
    c2 = np.r_[c, np.zeros(m)]
    status = run(c2, range(n), 2)
    x = x_now()[:n]
    return {"status": status, "x": x, "fun": float(c @ x), "steps": steps}


def superhedge_tree(S0, K, T, sigma, N, cp=1, r=0.0, payoff=None) -> dict:
    """Dynamic super- and sub-replication with only the stock and the bond on a recombining trinomial tree (moves
    u = e^{sigma sqrt(dt)}, 1, 1/u): at each node the price is the max (min) of the discounted expectation over every
    one-step martingale measure, a segment whose ends are the two-point measures, so the max over it is at an end
    (Kramkov 1996; Foellmer and Schied, ch. 7).  For a convex payoff the super-price is the CRR price at sigma:
    Black-Scholes at the largest volatility the tree allows (Avellaneda, Levy and Paras 1995)."""
    dt = T / N
    u = np.exp(sigma * np.sqrt(dt))
    d, g, disc = 1 / u, np.exp(r * dt), np.exp(-r * dt)
    if not d < g < u:
        raise ValueError("need d < e^{r dt} < u")
    j = np.arange(-N, N + 1)
    S = S0 * u ** j
    pay = payoff(S) if payoff is not None else np.maximum(cp * (S - K), 0.0)
    hi, lo = pay.copy(), pay.copy()
    qe = (g - d) / (u - d)                                            # the outer branches only
    if g >= 1:                                                        # the other end: no down move
        qm_u, qm_m, qm_d = (g - 1) / (u - 1), 1 - (g - 1) / (u - 1), 0.0
    else:                                                             # or no up move
        qm_u, qm_m, qm_d = 0.0, 1 - (1 - g) / (1 - d), (1 - g) / (1 - d)
    for _ in range(N):
        def ends(V):
            outer = qe * V[2:] + (1 - qe) * V[:-2]
            mid = qm_u * V[2:] + qm_m * V[1:-1] + qm_d * V[:-2]
            return outer, mid
        o, mm = ends(hi)
        hi = disc * np.maximum(o, mm)
        o, mm = ends(lo)
        lo = disc * np.minimum(o, mm)
    return {"upper": float(hi[0]), "lower": float(lo[0]), "u": float(u)}


def power_iteration(P, k=40, z0=None) -> dict:
    """The Perron vector of a positive matrix by repeated multiplication: z <- P z / |P z|.  Returns every iterate
    and the eigenvalue estimate (the growth of the sum) at each step."""
    P = np.asarray(P, float)
    z = np.ones(len(P)) if z0 is None else np.asarray(z0, float)
    z = z / z.sum()
    zs, lam = [z.copy()], []
    for _ in range(k):
        w = P @ z
        lam.append(float(w.sum() / z.sum()))
        z = w / w.sum()
        zs.append(z.copy())
    return {"z": np.array(zs), "delta": np.array(lam)}


def mot_dual(x, mu, y, nu, cost, sign=1.0) -> dict:
    """The dual of martingale optimal transport, read off HiGHS's equality multipliers: functions u (of the first
    price), v (of the second) and h (the delta held from the first date to the second) with u(x) + v(y) +
    h(x)(y - x) >= c(x, y) everywhere (``sign`` = -1) or <= c (``sign`` = 1), whose cost sum u mu + sum v nu is the
    bound (Beiglboeck, Henry-Labordere and Penkner 2013): a static portfolio of vanillas plus one dynamic trade."""
    x, mu, y, nu = (np.asarray(a, float) for a in (x, mu, y, nu))
    n, m = len(x), len(y)
    C = np.asarray([[cost(a, b) for b in y] for a in x])
    rows, cols, vals = [], [], []
    r = 0
    for i in range(n):
        rows += [r] * m; cols += list(i * m + np.arange(m)); vals += [1.0] * m; r += 1
    for j in range(m):
        rows += [r] * n; cols += list(np.arange(n) * m + j); vals += [1.0] * n; r += 1
    for i in range(n):
        rows += [r] * m; cols += list(i * m + np.arange(m)); vals += list(y - x[i]); r += 1
    A = sparse.csr_matrix((vals, (rows, cols)), shape=(r, n * m))
    b = np.concatenate([mu, nu, np.zeros(n)])
    res = linprog(sign * C.ravel(), A_eq=A, b_eq=b, bounds=(0, None), method="highs")
    if res.status != 0:
        raise ValueError(f"MOT infeasible: {res.message}")
    lam = sign * np.asarray(res.eqlin.marginals)
    u, v, h = lam[:n], lam[n:n + m], lam[n + m:]
    slack = u[:, None] + v[None, :] + h[:, None] * (y[None, :] - x[:, None]) - C
    return {"value": float(sign * res.fun), "u": u, "v": v, "h": h, "pi": res.x.reshape(n, m),
            "dual_value": float(u @ mu + v @ nu), "slack": slack}


def entropic_mot(x, mu, y, nu, cost, eps=0.01, iters=500, sign=-1.0, newton=3, log_every=10) -> dict:
    """Entropic martingale optimal transport by coordinate ascent on the dual (Sinkhorn with a martingale step): u
    and v in closed form (log-sum-exp), the delta h_i by a few Newton steps on sum_j pi_ij (y_j - x_i) = 0.  ``sign``
    = -1 approximates the upper bound (maximize sum pi c), +1 the lower.  The coupling is pi_ij = mu_i nu_j
    exp((s c_ij - u_i - v_j - h_i (y_j - x_i)) / eps) with s = -sign.  Returns the trace of the transport value and
    of the marginal and martingale errors."""
    from scipy.special import logsumexp

    x, mu, y, nu = (np.asarray(a, float) for a in (x, mu, y, nu))
    C = -sign * np.asarray([[cost(a, b) for b in y] for a in x])     # maximize sum pi C (so sum pi c = -sign sum pi C)
    D = y[None, :] - x[:, None]
    lmu, lnu = np.log(np.maximum(mu, 1e-300)), np.log(np.maximum(nu, 1e-300))
    u, v, h = np.zeros(len(x)), np.zeros(len(y)), np.zeros(len(x))
    tr = []

    def logpi():
        return np.minimum(lmu[:, None] + lnu[None, :] + (C - u[:, None] - v[None, :] - h[:, None] * D) / eps, 700.0)

    for it in range(iters + 1):
        if it % log_every == 0 or it == iters:
            P = np.exp(logpi())
            tr.append((it, float((P * C).sum() * (-sign)),
                       float(np.abs(P.sum(1) - mu).sum() + np.abs(P.sum(0) - nu).sum()),
                       float(np.abs((P * D).sum(1)).sum())))
        if it == iters:
            break
        for _ in range(newton):                                       # h: the martingale condition, row by row
            L = logpi()
            w = np.exp(L - L.max(1, keepdims=True))
            h += eps * (w * D).sum(1) / np.maximum((w * D * D).sum(1), 1e-300)
        u = eps * logsumexp(lnu[None, :] + (C - v[None, :] - h[:, None] * D) / eps, axis=1)
        v = eps * logsumexp(lmu[:, None] + (C - u[:, None] - h[:, None] * D) / eps, axis=0)
    P = np.exp(logpi())
    # the transport value sum pi c, in the claim's own sign
    return {"value": float((P * C).sum() * (-sign)), "pi": P, "trace": np.array(tr), "u": u, "v": v, "h": h}
