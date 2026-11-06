"""statkit.quasi: natural experiments (Part 37 of *Statistics, Built*).

Instruments:
    ols(y, X, cluster)                  least squares with HC1 or cluster-robust covariance
    tsls(y, d, Z, X)                    two-stage least squares, first-stage F, the OLS comparison
    anderson_rubin(y, d, Z, X, b0)      the AR test of beta = b0, valid however weak the instruments
    ar_set(y, d, Z, X, grid)            the AR confidence set by test inversion (may be unbounded)
    liml(y, d, Z, X)                    limited-information maximum likelihood (the k-class with kappa = LIML)
    mr_ivw, mr_egger                    Mendelian randomization from summary statistics
Regression discontinuity:
    local_linear(x, y, c, h, p)         a one-sided local polynomial at the cutoff (triangular kernel)
    rd(x, y, c, h, p)                   the sharp RD estimate with its HC1 standard error
    rd_robust(x, y, c, h)               conventional (p = 1) and robust bias-corrected (p = 2 at rho = 1) intervals
    ik_bandwidth(x, y, c)               Imbens & Kalyanaraman's (2012) MSE-optimal bandwidth for local linear RD
    mccrary(x, c, b, h)                 McCrary's (2008) density test
    rd_fuzzy(x, y, d, c, h)             the fuzzy RD (a local Wald ratio) with a delta-method SE
Difference-in-differences (balanced panels Y[N, T], adoption times G[N], np.inf for never):
    twfe(Y, D)                          two-way fixed effects with OLS and town-clustered SEs
    event_study(Y, G, window)           TWFE with leads and lags, clustered SEs
    bacon(Y, G)                         Goodman-Bacon's decomposition into 2x2 comparisons and weights
    callaway_santanna(Y, G)             ATT(g, t) against never-treated units; the simple aggregate with an IF SE
    imputation(Y, G)                    Borusyak, Jaravel & Spiess's imputation estimator
    honest_rm(pre, post, se, Mbar)      Rambachan & Roth's relative-magnitudes bounds (a simple version)
    honest_sd(e, b, se, post, se, M)    a smoothness restriction: within M of the extrapolated linear pre-trend
Synthetic control and panels:
    simplex_ls(a, B, ridge)             min ||a - B w||^2 + ridge ||w||^2 over the simplex (projected gradient)
    synth(Y, j, T0)                     a synthetic control from pre-period outcomes; placebo ratios
    sdid(Y, j, T0)                      synthetic difference-in-differences (Arkhangelsky et al. 2021), with SC and DiD
    within(y, X, unit)                  fixed effects by the within transformation (FWL)
    nickell_bias(rho, T)                the leading term of Nickell's (1981) bias
    anderson_hsiao(Y)                   first differences instrumented by the second lag
Bounds:
    manski(y, t, r, lo, hi)             worst-case bounds on the ATE with missing outcomes
    lee_bounds(y, t, s)                 Lee's (2009) trimming bounds under monotone selection
"""

from __future__ import annotations

import math

import numpy as np
from scipy import stats

# ----------------------------------------------------------------------------------------------------------------------
# Least squares and instruments
# ----------------------------------------------------------------------------------------------------------------------


def _add_const(X, n):
    one = np.ones((n, 1))
    if X is None:
        return one
    X = np.asarray(X, float).reshape(n, -1)
    return np.hstack([one, X])


def ols(y, X, cluster=None, const: bool = True) -> dict:
    """Least squares of y on X (a constant added unless ``const=False``): coefficients, HC1 (or cluster-robust,
    with the small-sample factor G/(G-1) (n-1)/(n-k)) covariance, and the conventional covariance."""
    y = np.asarray(y, float)
    n = len(y)
    Xd = _add_const(X, n) if const else np.asarray(X, float).reshape(n, -1)
    k = Xd.shape[1]
    XtX_inv = np.linalg.pinv(Xd.T @ Xd)
    b = XtX_inv @ Xd.T @ y
    e = y - Xd @ b
    s2 = e @ e / (n - k)
    V_conv = s2 * XtX_inv
    if cluster is None:
        meat = (Xd * e[:, None] ** 2).T @ Xd * n / (n - k)
    else:
        cl = np.asarray(cluster)
        _, inv = np.unique(cl, return_inverse=True)
        G = inv.max() + 1
        S = np.zeros((G, k))
        np.add.at(S, inv, Xd * e[:, None])
        meat = S.T @ S * G / (G - 1) * (n - 1) / (n - k)
    V = XtX_inv @ meat @ XtX_inv
    return {"b": b, "V": V, "V_conv": V_conv, "resid": e, "se": np.sqrt(np.diag(V)), "se_conv": np.sqrt(np.diag(V_conv))}


def _partial(M, W):
    """Residuals of the columns of M on W (W includes the constant)."""
    coef, *_ = np.linalg.lstsq(W, M, rcond=None)
    return M - W @ coef


def first_stage_F(d, Z, X=None) -> float:
    """The (homoskedastic) first-stage F statistic for the excluded instruments Z."""
    d = np.asarray(d, float)
    n = len(d)
    W = _add_const(X, n)
    Z = np.asarray(Z, float).reshape(n, -1)
    dz, Zz = _partial(d[:, None], W)[:, 0], _partial(Z, W)
    pi, *_ = np.linalg.lstsq(Zz, dz, rcond=None)
    fit = Zz @ pi
    rss1 = np.sum((dz - fit) ** 2)
    q = Z.shape[1]
    dof = n - W.shape[1] - q
    return float((fit @ fit / q) / (rss1 / dof))


def tsls(y, d, Z, X=None, cluster=None, alpha: float = 0.1) -> dict:
    """Two-stage least squares of y on the endogenous d, instrumented by Z, with exogenous controls X (a constant is
    always included).  Returns the coefficient on d, its robust (or clustered) and conventional SEs, the Wald interval,
    the first-stage F, and OLS for comparison."""
    y, d = np.asarray(y, float), np.asarray(d, float)
    n = len(y)
    W = _add_const(X, n)
    Z = np.asarray(Z, float).reshape(n, -1)
    ZW = np.hstack([W, Z])
    coef, *_ = np.linalg.lstsq(ZW, d, rcond=None)
    dhat = ZW @ coef
    Xh = np.hstack([dhat[:, None], W])
    Xd = np.hstack([d[:, None], W])
    A = np.linalg.pinv(Xh.T @ Xh)
    b = A @ Xh.T @ y
    e = y - Xd @ b
    k = Xd.shape[1]
    s2 = e @ e / (n - k)
    V_conv = s2 * A
    if cluster is None:
        meat = (Xh * e[:, None] ** 2).T @ Xh * n / (n - k)
    else:
        _, inv = np.unique(np.asarray(cluster), return_inverse=True)
        G = inv.max() + 1
        S = np.zeros((G, k))
        np.add.at(S, inv, Xh * e[:, None])
        meat = S.T @ S * G / (G - 1) * (n - 1) / (n - k)
    V = A @ meat @ A
    z = stats.norm.ppf(1 - alpha / 2)
    se = float(np.sqrt(V[0, 0]))
    o = ols(y, np.hstack([d[:, None], np.asarray(X, float).reshape(n, -1)]) if X is not None else d[:, None])
    return {"beta": float(b[0]), "se": se, "se_conv": float(np.sqrt(V_conv[0, 0])), "ci": (b[0] - z * se, b[0] + z * se),
            "F": first_stage_F(d, Z, X), "ols": float(o["b"][1]), "ols_se": float(o["se"][1]), "q": Z.shape[1]}


def anderson_rubin(y, d, Z, X=None, b0: float = 0.0) -> dict:
    """Anderson & Rubin's (1949) test of beta = b0: regress y - b0 d on Z (and X) and F-test the instruments.  Its size
    is exact under normal errors, and asymptotically right, whatever the strength of the instruments."""
    y, d = np.asarray(y, float), np.asarray(d, float)
    n = len(y)
    W = _add_const(X, n)
    Z = np.asarray(Z, float).reshape(n, -1)
    q = Z.shape[1]
    u = _partial((y - b0 * d)[:, None], W)[:, 0]
    Zz = _partial(Z, W)
    g, *_ = np.linalg.lstsq(Zz, u, rcond=None)
    fit = Zz @ g
    dof = n - W.shape[1] - q
    F = (fit @ fit / q) / (np.sum((u - fit) ** 2) / dof)
    return {"F": float(F), "p": float(stats.f.sf(F, q, dof))}


def ar_set(y, d, Z, X=None, grid=None, alpha: float = 0.1) -> dict:
    """The Anderson-Rubin confidence set: every b0 on ``grid`` the AR test does not reject.  With one instrument the
    acceptance region is quadratic in b0, so the set is an interval, the complement of one, or the whole line; it is
    found exactly here, and ``grid`` is used only for plotting the p-value curve."""
    y, d = np.asarray(y, float), np.asarray(d, float)
    n = len(y)
    W = _add_const(X, n)
    Z = np.asarray(Z, float).reshape(n, -1)
    q = Z.shape[1]
    yz, dz, Zz = _partial(y[:, None], W)[:, 0], _partial(d[:, None], W)[:, 0], _partial(Z, W)
    P = Zz @ np.linalg.pinv(Zz.T @ Zz) @ Zz.T
    dof = n - W.shape[1] - q
    c = stats.f.ppf(1 - alpha, q, dof) * q / dof
    # accept b iff u'Pu <= c u'(I-P)u with u = yz - b dz:  a b^2 + b1 b + c0 <= 0
    Py, Pd = P @ yz, P @ dz
    yPy, dPd, yPd = yz @ Py, dz @ Pd, yz @ Pd
    yy, dd, yd = yz @ yz, dz @ dz, yz @ dz
    a = dPd - c * (dd - dPd)
    b1 = -2 * (yPd - c * (yd - yPd))
    c0 = yPy - c * (yy - yPy)
    disc = b1 * b1 - 4 * a * c0
    if a > 0:
        kind = "interval" if disc >= 0 else "empty"
        lo = hi = None
        if disc >= 0:
            r = math.sqrt(disc)
            lo, hi = (-b1 - r) / (2 * a), (-b1 + r) / (2 * a)
    else:
        if disc < 0:
            kind, lo, hi = "line", -math.inf, math.inf
        else:
            r = math.sqrt(disc)
            r1, r2 = sorted([(-b1 - r) / (2 * a), (-b1 + r) / (2 * a)])
            kind, lo, hi = "outside", r1, r2  # accepted: (-inf, r1] U [r2, inf)
    out = {"kind": kind, "lo": lo, "hi": hi}
    if grid is not None:
        out["grid"] = np.asarray(grid, float)
        out["p"] = np.array([anderson_rubin(y, d, Z, X, b)["p"] for b in out["grid"]])
    return out


def ar_covers(res: dict, b: float) -> bool:
    k = res["kind"]
    if k == "interval":
        return res["lo"] <= b <= res["hi"]
    if k == "outside":
        return b <= res["lo"] or b >= res["hi"]
    return k == "line"


def liml(y, d, Z, X=None) -> dict:
    """LIML for one endogenous regressor: kappa is the smallest eigenvalue of (Y'M_W Y)^-1 (Y'M_{WZ} Y) with
    Y = [y, d]; beta = the k-class estimator with that kappa.  Nearly median-unbiased with many instruments."""
    y, d = np.asarray(y, float), np.asarray(d, float)
    n = len(y)
    W = _add_const(X, n)
    Z = np.asarray(Z, float).reshape(n, -1)
    Yc = np.column_stack([y, d])
    A = _partial(Yc, W)
    B = _partial(Yc, np.hstack([W, Z]))
    S0, S1 = A.T @ A, B.T @ B
    kappa = float(np.min(np.real(np.linalg.eigvals(np.linalg.solve(S1, S0)))))
    yz, dz = A[:, 0], A[:, 1]
    rz = B[:, 1]
    # k-class: beta = (d'(I - kappa M) d)^-1 d'(I - kappa M) y, all partialled on W
    num = dz @ yz - kappa * (rz @ B[:, 0])
    den = dz @ dz - kappa * (rz @ rz)
    beta = num / den
    e = yz - beta * dz
    s2 = e @ e / (n - W.shape[1] - 1)
    return {"beta": float(beta), "kappa": kappa, "se": float(math.sqrt(s2 / den))}


def mr_ivw(bx, by, se_by) -> dict:
    """Inverse-variance-weighted Mendelian randomization: the weighted regression of by on bx through the origin."""
    bx, by, s = (np.asarray(a, float) for a in (bx, by, se_by))
    w = bx * bx / (s * s)
    ratio = by / bx
    beta = float(np.sum(w * ratio) / np.sum(w))
    resid = (by - beta * bx) / s
    phi = max(1.0, float(resid @ resid / (len(bx) - 1)))
    return {"beta": beta, "se": float(math.sqrt(phi / np.sum(bx * bx / (s * s))))}


def mr_egger(bx, by, se_by) -> dict:
    """MR-Egger (Bowden, Davey Smith & Burgess 2015): weighted regression of by on bx with an intercept (directional
    pleiotropy), the variants oriented so bx > 0."""
    bx, by, s = (np.asarray(a, float) for a in (bx, by, se_by))
    sign = np.sign(bx)
    bx, by = bx * sign, by * sign
    w = 1 / (s * s)
    Xd = np.column_stack([np.ones_like(bx), bx])
    A = np.linalg.inv((Xd * w[:, None]).T @ Xd)
    b = A @ (Xd * w[:, None]).T @ by
    r = by - Xd @ b
    phi = max(1.0, float(np.sum(w * r * r) / (len(bx) - 2)))
    se = np.sqrt(np.diag(A) * phi)
    return {"intercept": float(b[0]), "beta": float(b[1]), "se_intercept": float(se[0]), "se": float(se[1])}


# ----------------------------------------------------------------------------------------------------------------------
# Regression discontinuity
# ----------------------------------------------------------------------------------------------------------------------


def tri(u):
    return np.clip(1 - np.abs(u), 0, None)


def local_linear(x, y, c: float, h: float, p: int = 1, side: str = "right") -> dict:
    """The local polynomial of order p fitted on one side of the cutoff with triangular weights (1 - |x - c|/h)+:
    its intercept at c and the HC1 sandwich variance of that intercept."""
    x, y = np.asarray(x, float), np.asarray(y, float)
    keep = (x >= c) if side == "right" else (x < c)
    u = (x[keep] - c) / h
    w = tri(u)
    k = w > 0
    u, w, yy = u[k], w[k], y[keep][k]
    Xd = np.vander(u, p + 1, increasing=True)
    XtW = Xd.T * w
    A = np.linalg.pinv(XtW @ Xd)
    b = A @ XtW @ yy
    e = yy - Xd @ b
    n, m = len(yy), p + 1
    meat = (Xd * (w * e)[:, None]).T @ (Xd * (w * e)[:, None]) * n / max(n - m, 1)
    V = A @ meat @ A
    return {"a": float(b[0]), "var": float(V[0, 0]), "n": int(n), "coef": b}


def rd(x, y, c: float, h: float, p: int = 1, alpha: float = 0.1) -> dict:
    """The sharp RD estimate: the jump between the two one-sided local polynomials at c."""
    r, l = local_linear(x, y, c, h, p, "right"), local_linear(x, y, c, h, p, "left")
    tau = r["a"] - l["a"]
    se = math.sqrt(r["var"] + l["var"])
    z = stats.norm.ppf(1 - alpha / 2)
    return {"tau": tau, "se": se, "ci": (tau - z * se, tau + z * se), "n_left": l["n"], "n_right": r["n"],
            "left": l["coef"], "right": r["coef"]}


def rd_robust(x, y, c: float, h: float | None = None, alpha: float = 0.1) -> dict:
    """Conventional and robust bias-corrected RD intervals (Calonico, Cattaneo & Titiunik 2014).  The conventional
    interval centres the local-linear estimate at the MSE-optimal h and ignores its bias.  The robust interval subtracts
    an estimate of that bias from a local quadratic and widens the SE to account for it; with the pilot bandwidth equal
    to h (rho = 1) this is exactly the local-quadratic estimate with its own SE."""
    if h is None:
        h = ik_bandwidth(x, y, c)
    conv = rd(x, y, c, h, 1, alpha)
    rob = rd(x, y, c, h, 2, alpha)
    return {"h": h, "conv": conv, "robust": rob}


def ik_bandwidth(x, y, c: float) -> float:
    """Imbens & Kalyanaraman's (2012) MSE-optimal bandwidth for the local-linear RD with a triangular kernel:
    h = 3.4375 [ (s2+ + s2-) / (f(c) ((m2+ - m2-)^2 + r+ + r-)) ]^{1/5} n^{-1/5}."""
    x, y = np.asarray(x, float), np.asarray(y, float)
    n = len(x)
    sx = np.std(x)
    h1 = 1.84 * sx * n ** -0.2
    L, R = (x >= c - h1) & (x < c), (x >= c) & (x <= c + h1)
    f = (L.sum() + R.sum()) / (2 * n * h1)
    s2l = np.var(y[L], ddof=1) if L.sum() > 2 else np.var(y)
    s2r = np.var(y[R], ddof=1) if R.sum() > 2 else np.var(y)
    # global cubic with a jump to get the third derivative; then second derivatives on each side with h2
    xm = x - c
    T = (x >= c).astype(float)
    Xd = np.column_stack([np.ones(n), T, xm, xm ** 2, xm ** 3])
    m3 = 6 * np.linalg.lstsq(Xd, y, rcond=None)[0][4]
    m3 = abs(m3) if abs(m3) > 1e-12 else 1e-12
    h2l = 3.56 * (s2l / (f * m3 * m3)) ** (1 / 7) * max(L.sum(), 3) ** (-1 / 7)
    h2r = 3.56 * (s2r / (f * m3 * m3)) ** (1 / 7) * max(R.sum(), 3) ** (-1 / 7)

    def second(side, h2):
        k = (x >= c) & (x <= c + h2) if side == "right" else (x >= c - h2) & (x < c)
        if k.sum() < 5:
            return 0.0, k.sum()
        u = x[k] - c
        b = np.linalg.lstsq(np.column_stack([np.ones(k.sum()), u, u * u]), y[k], rcond=None)[0]
        return 2 * b[2], k.sum()

    m2r, nr = second("right", h2r)
    m2l, nl = second("left", h2l)
    rr = 720 * s2r / (max(nr, 1) * h2r ** 4)
    rl = 720 * s2l / (max(nl, 1) * h2l ** 4)
    h = 3.4375 * ((s2l + s2r) / (f * ((m2r - m2l) ** 2 + rr + rl))) ** 0.2 * n ** -0.2
    return float(h)


def mccrary(x, c: float, b: float | None = None, h: float | None = None) -> dict:
    """McCrary's (2008) test for a jump in the density of the running variable at c: a histogram with bin width b,
    local-linear regressions of the bin heights on each side (triangular weights, bandwidth h), and
    theta = log f+ - log f- with SE sqrt((24/5)(1/f+ + 1/f-)/(n h))."""
    x = np.asarray(x, float)
    n = len(x)
    if b is None:
        b = 2 * np.std(x) * n ** -0.5
    lo = c - b * math.ceil((c - x.min()) / b)
    hi = c + b * math.ceil((x.max() - c) / b)
    edges = np.arange(lo, hi + b / 2, b)
    counts, _ = np.histogram(x, edges)
    mids = (edges[:-1] + edges[1:]) / 2
    dens = counts / (n * b)
    if h is None:
        h = 10 * b
    res = {}
    for side in ("left", "right"):
        k = mids < c if side == "left" else mids >= c
        u = (mids[k] - c) / h
        w = tri(u)
        m = w > 0
        Xd = np.column_stack([np.ones(m.sum()), u[m]])
        A = Xd.T * w[m]
        res[side] = float(np.linalg.solve(A @ Xd, A @ dens[k][m])[0])
    fl, fr = max(res["left"], 1e-12), max(res["right"], 1e-12)
    theta = math.log(fr) - math.log(fl)
    se = math.sqrt(24 / 5 * (1 / fr + 1 / fl) / (n * h))
    z = theta / se
    return {"theta": theta, "se": se, "z": z, "p": float(2 * stats.norm.sf(abs(z))), "f_left": fl, "f_right": fr,
            "mids": mids, "dens": dens, "b": b, "h": h}


def rd_fuzzy(x, y, d, c: float, h: float, p: int = 1, alpha: float = 0.1) -> dict:
    """The fuzzy RD: the jump in y over the jump in take-up d, with a delta-method SE (the two jumps' covariance from
    the same local fits)."""
    x, y, d = (np.asarray(a, float) for a in (x, y, d))
    out = {}
    num = rd(x, y, c, h, p)
    den = rd(x, d, c, h, p)
    tau = num["tau"] / den["tau"]
    # influence-style SE: the RD of y - tau d, divided by the first stage
    adj = rd(x, y - tau * d, c, h, p)
    se = adj["se"] / abs(den["tau"])
    z = stats.norm.ppf(1 - alpha / 2)
    out.update(tau=tau, se=se, ci=(tau - z * se, tau + z * se), jump_y=num["tau"], jump_d=den["tau"])
    return out


# ----------------------------------------------------------------------------------------------------------------------
# Difference-in-differences on balanced panels
# ----------------------------------------------------------------------------------------------------------------------


def _twoway_demean(M):
    return M - M.mean(1, keepdims=True) - M.mean(0, keepdims=True) + M.mean()


def twfe(Y, D) -> dict:
    """The two-way fixed-effects regression Y_it = a_i + g_t + beta D_it + e on a balanced N x T panel: beta by the
    two-way within transformation, with the conventional OLS SE and the unit-clustered SE."""
    Y, D = np.asarray(Y, float), np.asarray(D, float)
    N, T = Y.shape
    Yd, Dd = _twoway_demean(Y), _twoway_demean(D)
    beta = float(np.sum(Yd * Dd) / np.sum(Dd * Dd))
    e = Yd - beta * Dd
    dof = N * T - N - T
    se_conv = math.sqrt(np.sum(e * e) / dof / np.sum(Dd * Dd))
    s = np.sum(Dd * e, 1)
    se_cl = math.sqrt(N / (N - 1) * np.sum(s * s)) / np.sum(Dd * Dd)
    return {"beta": beta, "se_conv": se_conv, "se": se_cl}


def event_study(Y, G, times, window=(-5, 5), ref: int = -1) -> dict:
    """TWFE with relative-time indicators k = t - G_i in ``window`` (ends binned), the reference k = ref omitted and
    never-treated units in the comparison: coefficients and unit-clustered SEs."""
    Y = np.asarray(Y, float)
    N, T = Y.shape
    times = np.asarray(times)
    G = np.asarray(G, float)
    ks = [k for k in range(window[0], window[1] + 1) if k != ref]
    rel = times[None, :] - G[:, None]
    cols = []
    for k in ks:
        if k == window[0]:
            m = rel <= k
        elif k == window[1]:
            m = rel >= k
        else:
            m = rel == k
        cols.append((m & np.isfinite(rel)).astype(float))
    y = Y.ravel()
    unit = np.repeat(np.arange(N), T)
    tt = np.tile(np.arange(T), N)
    Xk = np.column_stack([c.ravel() for c in cols])
    # absorb unit and time effects by alternating projections
    def demean(v):
        v = v.copy()
        for _ in range(200):
            v_old = v
            v = v - np.bincount(unit, v, N)[unit] / T
            v = v - np.bincount(tt, v, T)[tt] / N
            if np.max(np.abs(v - v_old)) < 1e-10:
                break
        return v
    yd = demean(y)
    Xd = np.column_stack([demean(Xk[:, j]) for j in range(Xk.shape[1])])
    A = np.linalg.pinv(Xd.T @ Xd)
    b = A @ Xd.T @ yd
    e = yd - Xd @ b
    S = np.zeros((N, Xd.shape[1]))
    np.add.at(S, unit, Xd * e[:, None])
    V = A @ (S.T @ S) @ A * N / (N - 1)
    return {"k": ks, "b": b, "se": np.sqrt(np.diag(V))}


def _never(G):
    return ~np.isfinite(np.asarray(G, float))


def bacon(Y, G, times) -> list:
    """Goodman-Bacon's (2021) decomposition of the TWFE coefficient (no always-treated units): every 2x2 DiD between
    timing groups, with its weight.  Comparisons: early vs later-treated (before the later group starts), later vs
    earlier-treated (after the earlier group started: the 'forbidden' ones), and each group vs the never-treated."""
    Y = np.asarray(Y, float)
    N, T = Y.shape
    times = np.asarray(times, float)
    G = np.asarray(G, float)
    groups = sorted(set(G[np.isfinite(G)]))
    nev = _never(G)
    n_u = nev.mean()
    out = []

    def dbar(g):
        return np.mean(times >= g)

    def two(a_units, b_units, tmask_pre, tmask_post):
        ya = Y[a_units][:, tmask_post].mean() - Y[a_units][:, tmask_pre].mean()
        yb = Y[b_units][:, tmask_post].mean() - Y[b_units][:, tmask_pre].mean()
        return ya - yb

    for g in groups:
        k = G == g
        nk = k.mean()
        Dk = dbar(g)
        if nev.any():
            est = two(k, nev, times < g, times >= g)
            w = (nk + n_u) ** 2 * (nk / (nk + n_u)) * (n_u / (nk + n_u)) * Dk * (1 - Dk)
            out.append({"kind": "vs never", "g": g, "c": np.inf, "est": float(est), "w": float(w)})
        for l in groups:
            if l <= g:
                continue
            m = G == l
            nl = m.mean()
            Dl = dbar(l)
            nkl = nk / (nk + nl)
            # early k vs late l, before l starts
            pre, post = times < g, (times >= g) & (times < l)
            est = two(k, m, pre, post)
            w = ((nk + nl) * (1 - Dl)) ** 2 * nkl * (1 - nkl) * ((Dk - Dl) / (1 - Dl)) * ((1 - Dk) / (1 - Dl))
            out.append({"kind": "early vs later", "g": g, "c": l, "est": float(est), "w": float(w)})
            # late l vs early k, after k started
            pre, post = (times >= g) & (times < l), times >= l
            est = two(m, k, pre, post)
            w = ((nk + nl) * Dk) ** 2 * nkl * (1 - nkl) * (Dl / Dk) * ((Dk - Dl) / Dk)
            out.append({"kind": "later vs earlier", "g": l, "c": g, "est": float(est), "w": float(w)})
    tot = sum(o["w"] for o in out)
    for o in out:
        o["w"] /= tot
    return out


def callaway_santanna(Y, G, times, alpha: float = 0.1) -> dict:
    """Callaway & Sant'Anna's (2021) ATT(g, t) with the never-treated as controls and the period before adoption as
    the base: ATT(g,t) = E[Y_t - Y_{g-1} | G = g] - E[Y_t - Y_{g-1} | never].  The simple aggregate averages the
    post-adoption cells weighted by group size; its SE comes from the units' influence functions (exact here, since
    every piece is a difference of means)."""
    Y = np.asarray(Y, float)
    N, T = Y.shape
    times = np.asarray(times)
    G = np.asarray(G, float)
    nev = _never(G)
    n_c = nev.sum()
    cells = []
    psi_total = np.zeros(N)
    wsum = 0.0
    for g in sorted(set(G[np.isfinite(G)])):
        k = G == g
        n_g = k.sum()
        base = int(np.searchsorted(times, g)) - 1
        for j in range(T):
            if base < 0:
                continue
            dy = Y[:, j] - Y[:, base]
            att = dy[k].mean() - dy[nev].mean()
            psi = np.zeros(N)
            psi[k] = (dy[k] - dy[k].mean()) / n_g
            psi[nev] = -(dy[nev] - dy[nev].mean()) / n_c
            cells.append({"g": float(g), "t": float(times[j]), "e": float(times[j] - g), "att": float(att),
                          "se": float(math.sqrt(np.sum(psi * psi))), "n": int(n_g)})
            if times[j] >= g:
                psi_total += n_g * psi  # weights proportional to group size, normalised below
                wsum += n_g
    post = [c for c in cells if c["e"] >= 0]
    est = sum(c["att"] * c["n"] for c in post) / wsum
    se = math.sqrt(np.sum((psi_total / wsum) ** 2))
    z = stats.norm.ppf(1 - alpha / 2)
    # event-time aggregation
    es = {}
    for c in cells:
        es.setdefault(c["e"], []).append(c)
    event = {e: sum(c["att"] * c["n"] for c in cs) / sum(c["n"] for c in cs) for e, cs in sorted(es.items())}
    return {"att": est, "se": se, "ci": (est - z * se, est + z * se), "cells": cells, "event": event}


def imputation(Y, G, times) -> dict:
    """Borusyak, Jaravel & Spiess's imputation estimator: fit unit and time effects on the untreated cells only,
    impute Y(0) for the treated cells, and average Y - Y(0) over them."""
    Y = np.asarray(Y, float)
    N, T = Y.shape
    times = np.asarray(times)
    G = np.asarray(G, float)
    D = times[None, :] >= G[:, None]
    a, g = np.zeros(N), np.zeros(T)
    U = ~D
    for _ in range(500):
        a_new = np.array([np.mean(Y[i, U[i]] - g[U[i]]) if U[i].any() else 0.0 for i in range(N)])
        g_new = np.array([np.mean(Y[U[:, t], t] - a_new[U[:, t]]) if U[:, t].any() else 0.0 for t in range(T)])
        if np.max(np.abs(a_new - a)) + np.max(np.abs(g_new - g)) < 1e-10:
            a, g = a_new, g_new
            break
        a, g = a_new, g_new
    Y0 = a[:, None] + g[None, :]
    tau = (Y - Y0)[D]
    return {"att": float(tau.mean()), "tau": Y - Y0, "treated": D}


def honest_rm(pre, post: float, se_post: float, Mbar: float, alpha: float = 0.1) -> dict:
    """Rambachan & Roth's (2023) relative-magnitudes restriction in its simplest form: the post-period violation of
    parallel trends is at most Mbar times the largest pre-period change |delta_t - delta_{t-1}| (pre-period
    coefficients ``pre`` ending at the reference 0).  Returns the identified set for the first post-period effect and
    a conservative interval that adds the sampling error to each end."""
    pre = np.append(np.asarray(pre, float), 0.0)
    jump = float(np.max(np.abs(np.diff(pre)))) if len(pre) > 1 else 0.0
    z = stats.norm.ppf(1 - alpha / 2)
    lo, hi = post - Mbar * jump, post + Mbar * jump
    return {"set": (lo, hi), "ci": (lo - z * se_post, hi + z * se_post), "max_pre_jump": jump}


def honest_sd(pre_e, pre_b, pre_se, post: float, se_post: float, M: float, alpha: float = 0.1) -> dict:
    """A smoothness restriction in the spirit of Rambachan & Roth's Delta^SD, for the first post-period effect: the
    violation of parallel trends continues the linear pre-trend (fitted to the event-study leads ``pre_b`` at
    ``pre_e`` < -1, through the reference e = -1 normalised to 0) up to a deviation of at most M at e = 0.  Identified
    set post - slope +- M; the conservative interval adds z sqrt(se_post^2 + se_slope^2) to each end (treating the
    leads as independent)."""
    x = np.asarray(pre_e, float) + 1
    b, se = np.asarray(pre_b, float), np.asarray(pre_se, float)
    slope = float(np.sum(x * b) / np.sum(x * x))
    se_slope = float(math.sqrt(np.sum((x * se) ** 2)) / np.sum(x * x))
    z = stats.norm.ppf(1 - alpha / 2)
    mid = post - slope
    s_ = math.sqrt(se_post ** 2 + se_slope ** 2)
    return {"set": (mid - M, mid + M), "ci": (mid - M - z * s_, mid + M + z * s_), "mid": mid, "slope": slope,
            "se_slope": se_slope}


# ----------------------------------------------------------------------------------------------------------------------
# Synthetic control and synthetic DiD
# ----------------------------------------------------------------------------------------------------------------------


def project_simplex(v):
    """Euclidean projection onto {w >= 0, sum w = 1} (Duchi et al. 2008)."""
    u = np.sort(v)[::-1]
    css = np.cumsum(u)
    rho = np.nonzero(u * np.arange(1, len(v) + 1) > (css - 1))[0][-1]
    theta = (css[rho] - 1) / (rho + 1.0)
    return np.maximum(v - theta, 0)


def simplex_ls(a, B, ridge: float = 0.0, iters: int = 20000, tol: float = 1e-12) -> np.ndarray:
    """min ||a - B w||^2 + ridge ||w||^2 over the simplex, by accelerated projected gradient."""
    a, B = np.asarray(a, float), np.asarray(B, float)
    J = B.shape[1]
    Q = B.T @ B + ridge * np.eye(J)
    r = B.T @ a
    L = np.linalg.eigvalsh(Q).max() * 2
    w = np.full(J, 1 / J)
    z, t = w.copy(), 1.0
    f_old = np.inf
    for _ in range(iters):
        grad = 2 * (Q @ z - r)
        w_new = project_simplex(z - grad / L)
        t_new = (1 + math.sqrt(1 + 4 * t * t)) / 2
        z = w_new + (t - 1) / t_new * (w_new - w)
        w, t = w_new, t_new
        f = w @ Q @ w - 2 * r @ w
        if abs(f_old - f) < tol * (1 + abs(f)):
            break
        f_old = f
    return w


def synth(Y, j: int, T0: int, X=None, v=None) -> dict:
    """A synthetic control for unit j: simplex weights on the other units matching j's pre-period outcomes (the first
    T0 columns of Y), optionally with extra standardized predictors X (rows = units) weighted by v.  Returns the
    weights, the synthetic path, the gap and the pre/post RMSPE."""
    Y = np.asarray(Y, float)
    donors = [i for i in range(Y.shape[0]) if i != j]
    A = Y[j, :T0]
    B = Y[donors, :T0].T
    if X is not None:
        X = np.asarray(X, float)
        sd = X.std(0) + 1e-12
        vv = np.ones(X.shape[1]) if v is None else np.asarray(v, float)
        A = np.concatenate([A, X[j] / sd * np.sqrt(vv)])
        B = np.vstack([B, (X[donors] / sd * np.sqrt(vv)).T])
    w = simplex_ls(A, B)
    path = w @ Y[donors]
    gap = Y[j] - path
    pre = math.sqrt(np.mean(gap[:T0] ** 2))
    post = math.sqrt(np.mean(gap[T0:] ** 2))
    return {"w": w, "donors": donors, "path": path, "gap": gap, "rmspe_pre": pre, "rmspe_post": post,
            "ratio": post / pre}


def sdid(Y, j: int, T0: int) -> dict:
    """Synthetic difference-in-differences (Arkhangelsky, Athey, Hirshberg, Imbens & Wager 2021) for one treated unit:
    unit weights omega (simplex, with an intercept and the ridge zeta^2 T0, zeta = (T_post)^{1/4} sd of the controls'
    first differences), time weights lambda (simplex, with an intercept), and the weighted double difference.  Also
    returns the synthetic-control estimate (no intercept, no ridge, uniform time weights over the post period vs the
    weighted pre-period) and plain DiD, as in the paper's Table 1."""
    Y = np.asarray(Y, float)
    N, T = Y.shape
    donors = np.array([i for i in range(N) if i != j])
    Yc = Y[donors]
    T1 = T - T0
    sigma = np.std(np.diff(Yc[:, :T0], axis=1), ddof=1)
    zeta = T1 ** 0.25 * sigma
    # unit weights: intercept by demeaning over pre-period time
    B = Yc[:, :T0].T
    a = Y[j, :T0]
    Bc, ac = B - B.mean(0), a - a.mean()
    omega = simplex_ls(ac, Bc, ridge=zeta ** 2 * T0)
    # time weights: regress each control's post mean on its pre-period outcomes (intercept by demeaning over units)
    P = Yc[:, :T0]
    q = Yc[:, T0:].mean(1)
    Pc, qc = P - P.mean(0), q - q.mean()
    lam = simplex_ls(qc, Pc, ridge=(1e-6 * sigma) ** 2 * len(donors))

    def dd(w_units, w_pre):
        tr = Y[j, T0:].mean() - w_pre @ Y[j, :T0]
        co = w_units @ (Yc[:, T0:].mean(1) - Yc[:, :T0] @ w_pre)
        return float(tr - co)

    tau = dd(omega, lam)
    w_sc = simplex_ls(a, B, ridge=(1e-6 * sigma) ** 2 * T0)
    sc = float(Y[j, T0:].mean() - w_sc @ Yc[:, T0:].mean(1))
    did = dd(np.full(len(donors), 1 / len(donors)), np.full(T0, 1 / T0))
    return {"tau": tau, "omega": omega, "lam": lam, "donors": donors, "sc": sc, "w_sc": w_sc, "did": did, "zeta": zeta}


# ----------------------------------------------------------------------------------------------------------------------
# Panels
# ----------------------------------------------------------------------------------------------------------------------


def within(y, X, unit) -> dict:
    """Fixed effects by the within transformation: demean y and X by unit and regress (FWL: the same slope as the
    regression with a dummy for every unit).  Unit-clustered SEs."""
    y = np.asarray(y, float)
    X = np.asarray(X, float).reshape(len(y), -1)
    _, inv = np.unique(np.asarray(unit), return_inverse=True)
    N = inv.max() + 1
    cnt = np.bincount(inv, minlength=N)
    yd = y - (np.bincount(inv, y, N) / cnt)[inv]
    Xd = X - np.column_stack([np.bincount(inv, X[:, k], N) / cnt for k in range(X.shape[1])])[inv]
    A = np.linalg.pinv(Xd.T @ Xd)
    b = A @ Xd.T @ yd
    e = yd - Xd @ b
    S = np.zeros((N, X.shape[1]))
    np.add.at(S, inv, Xd * e[:, None])
    V = A @ (S.T @ S) @ A * N / (N - 1)
    return {"b": b, "se": np.sqrt(np.diag(V))}


def nickell_bias(rho: float, T: int) -> float:
    """The large-N bias of the within estimator of rho in y_it = rho y_i,t-1 + a_i + e_it with T periods of
    regressors (Nickell 1981), exact in T."""
    num = -(1 + rho) / (T - 1) * (1 - (1 - rho ** T) / (T * (1 - rho)))
    den = 1 - 2 * rho / ((1 - rho) * (T - 1)) * (1 - (1 - rho ** T) / (T * (1 - rho)))
    return float(num / den)


def anderson_hsiao(Y) -> dict:
    """Anderson & Hsiao's estimator for a dynamic panel Y[N, T]: regress dy_t on dy_{t-1}, instrumenting dy_{t-1} by
    y_{t-2} (no constant)."""
    Y = np.asarray(Y, float)
    dy = np.diff(Y, axis=1)
    yv = dy[:, 1:].ravel()
    xv = dy[:, :-1].ravel()
    zv = Y[:, :-2].ravel()
    beta = float(zv @ yv / (zv @ xv))
    e = yv - beta * xv
    N = Y.shape[0]
    unit = np.repeat(np.arange(N), dy.shape[1] - 1)
    s = np.bincount(unit, zv * e, N)
    se = math.sqrt(np.sum(s * s)) / abs(zv @ xv)
    return {"rho": beta, "se": se}


# ----------------------------------------------------------------------------------------------------------------------
# Bounds
# ----------------------------------------------------------------------------------------------------------------------


def manski(y, t, r, lo: float, hi: float) -> dict:
    """Worst-case (no-assumption) bounds on E[Y(1)] - E[Y(0)] when outcomes are missing for some units (r = 0) and
    Y lies in [lo, hi] (Manski 1990): fill the missing outcomes with lo or hi."""
    y, t, r = np.asarray(y, float), np.asarray(t, bool), np.asarray(r, bool)
    out = {}
    for arm, m in (("1", t), ("0", ~t)):
        obs = r & m
        p = obs.sum() / m.sum()
        mean = y[obs].mean() if obs.any() else 0.0
        out[arm] = (p * mean + (1 - p) * lo, p * mean + (1 - p) * hi)
    return {"lo": out["1"][0] - out["0"][1], "hi": out["1"][1] - out["0"][0], "arms": out}


def lee_bounds(y, t, s) -> dict:
    """Lee's (2009) bounds on the effect for the always-observed, under monotone selection (treatment never stops
    anyone being observed): trim the arm with more observed outcomes by the excess share, from the top or the bottom."""
    y, t, s = np.asarray(y, float), np.asarray(t, bool), np.asarray(s, bool)
    q1, q0 = s[t].mean(), s[~t].mean()
    if q1 >= q0:
        big, small, sign = t, ~t, 1.0
        p = (q1 - q0) / q1
    else:
        big, small, sign = ~t, t, -1.0
        p = (q0 - q1) / q0
    yb = np.sort(y[big & s])
    m = len(yb)
    cut = int(round(p * m))
    low_mean = yb[: m - cut].mean()
    high_mean = yb[cut:].mean()
    ys = y[small & s].mean()
    if sign > 0:
        lo, hi = low_mean - ys, high_mean - ys
    else:
        lo, hi = ys - high_mean, ys - low_mean
    return {"lo": float(lo), "hi": float(hi), "trim": float(p), "naive": float(y[t & s].mean() - y[~t & s].mean())}
