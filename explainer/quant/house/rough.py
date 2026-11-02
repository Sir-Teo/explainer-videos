"""Rough and path-dependent volatility (Part 14): rough Bergomi by the hybrid scheme, rough Heston's characteristic
function by the fractional Adams scheme, its multi-factor Markovian lift, roughness estimators, and Guyon and
Lekeufack's path-dependent volatility.

Conventions as in :mod:`stochvol`: zero rates, X = log(S_T / F), phi(u) = E[exp(i u X)].
"""
from __future__ import annotations

import numpy as np
from scipy.optimize import least_squares
from scipy.special import gamma as G

# ---------------------------------------------------------------- rough Bergomi (Bayer, Friz and Gatheral 2016)


def _b(k, a):
    return ((k ** (a + 1) - (k - 1) ** (a + 1)) / (a + 1)) ** (1 / a)


def rbergomi_paths(H, eta, rho, xi0, T, n, n_paths, seed=0, return_v=False):
    """Rough Bergomi, v_t = xi0(t) exp(eta Y_t - eta^2 t^{2H} / 2), Y_t = sqrt(2H) int_0^t (t - s)^{H - 1/2} dW_s,
    simulated by Bennedsen, Lunde and Pakkanen's (2017) hybrid scheme (kappa = 1): the kernel's singular first cell
    exactly, the rest by step functions at optimal points. ``xi0``: a number or a function of t. Returns S (n + 1,
    n_paths) with S_0 = 1 (and v)."""
    rng = np.random.default_rng(seed)
    a = H - 0.5
    dt = T / n
    t = np.linspace(0, T, n + 1)
    # the pair (dW_i, int over cell i of (t_{i+1} - s)^a dW_s), jointly Gaussian
    cov = np.array([[dt, dt ** (a + 1) / (a + 1)], [dt ** (a + 1) / (a + 1), dt ** (2 * a + 1) / (2 * a + 1)]])
    Lc = np.linalg.cholesky(cov)
    Z = rng.standard_normal((n_paths, n, 2)) @ Lc.T
    dW = Z[:, :, 0]
    Y1 = np.zeros((n_paths, n + 1))
    Y1[:, 1:] = Z[:, :, 1]
    k = np.arange(2, n + 1)
    Gk = np.zeros(n + 1)
    Gk[2:] = (_b(k, a) * dt) ** a
    Y2 = np.zeros((n_paths, n + 1))
    # Y2[:, i] = sum_{k=2}^{i} Gk[k] dW[:, i - k]  (a causal convolution, by FFT)
    m = 1 << int(np.ceil(np.log2(2 * n + 1)))
    conv = np.fft.irfft(np.fft.rfft(dW, m, axis=1) * np.fft.rfft(Gk, m)[None, :], m, axis=1)
    Y2[:, 1:] = conv[:, : n]
    Y = np.sqrt(2 * H) * (Y1 + Y2)
    xi = xi0(t) if callable(xi0) else np.full(n + 1, float(xi0))
    v = xi[None, :] * np.exp(eta * Y - 0.5 * eta ** 2 * t[None, :] ** (2 * H))
    dB = rho * dW + np.sqrt(1 - rho ** 2) * rng.standard_normal((n_paths, n)) * np.sqrt(dt)
    x = np.cumsum(np.sqrt(v[:, :-1]) * dB - 0.5 * v[:, :-1] * dt, axis=1)
    S = np.exp(np.concatenate([np.zeros((n_paths, 1)), x], axis=1)).T
    return (S, v.T) if return_v else S


# ---------------------------------------------------------------- rough Heston (El Euch and Rosenbaum 2019)


def frac_riccati(u, T, alpha, lam, rho, nu, n=200):
    """Solve D^alpha h = F(u, h) = -(u^2 + iu)/2 + (i rho nu u - lam) h + nu^2 h^2 / 2, h(0) = 0, on [0, T] by
    Diethelm's fractional Adams predictor-corrector, for a vector of u. Returns the grid and h (len(u), n + 1)."""
    u = np.atleast_1d(np.asarray(u, complex))
    dt = T / n
    t = np.linspace(0, T, n + 1)
    def F(h):
        return -0.5 * (u * u + 1j * u) + (1j * rho * nu * u - lam) * h + 0.5 * nu * nu * h * h

    h = np.zeros((len(u), n + 1), complex)
    Fh = np.zeros_like(h)
    Fh[:, 0] = F(h[:, 0])
    ga1, ga2 = G(alpha + 1), G(alpha + 2)
    j = np.arange(n + 1)
    for k in range(n):
        # predictor weights b_{j,k+1}, corrector weights a_{j,k+1}
        jj = j[: k + 1]
        bw = dt ** alpha / ga1 * ((k + 1 - jj) ** alpha - (k - jj) ** alpha)
        hp = Fh[:, : k + 1] @ bw
        aw = np.empty(k + 1)
        aw[0] = k ** (alpha + 1) - (k - alpha) * (k + 1) ** alpha
        if k >= 1:
            jj1 = jj[1:]
            aw[1:] = (k - jj1 + 2) ** (alpha + 1) + (k - jj1) ** (alpha + 1) - 2 * (k - jj1 + 1) ** (alpha + 1)
        aw *= dt ** alpha / ga2
        h[:, k + 1] = Fh[:, : k + 1] @ aw + dt ** alpha / ga2 * F(hp)
        Fh[:, k + 1] = F(h[:, k + 1])
    return t, h


def _frac_integral(f, t, order):
    """Riemann-Liouville integral I^order f at the last grid point, by the trapezoid-in-kernel rule on a uniform grid."""
    T = t[-1]
    n = len(t) - 1
    dt = T / n
    # piecewise-linear f, exact integration of (T - s)^(order - 1)
    j = np.arange(n + 1)
    a = order
    k = n - j
    w = np.zeros(n + 1)
    # product-trapezoid weights: f linear between grid points, the kernel (T - s)^(a - 1) / Gamma(a) exact
    w[1:-1] = (k[1:-1] + 1) ** (a + 1) - 2 * k[1:-1] ** (a + 1) + (k[1:-1] - 1) ** (a + 1)
    w[0] = (n - 1) ** (a + 1) - (n - a - 1) * n ** a
    w[-1] = 1.0
    w *= dt ** a / G(a + 2)
    return f @ w


def rough_heston_cf(u, T, v0, lam, theta, nu, rho, H, n=200):
    """The characteristic function of log(S_T / F) in rough Heston with alpha = H + 1/2 (El Euch and Rosenbaum 2019):
    phi(u) = exp(theta lam I^1 h(T) + v0 I^{1 - alpha} h(T)), h from the fractional Riccati equation."""
    alpha = H + 0.5
    u = np.atleast_1d(np.asarray(u, complex))
    out = np.zeros(len(u), complex)
    # frequencies where even the calmest variance leaves |phi| < e^-40 contribute nothing to a price, and there the
    # explicit Adams scheme is unstable (the Riccati equation is stiff in u^2): skip them
    v_lo = max(min(v0, theta), 1e-4) * 0.25
    keep = 0.5 * v_lo * T * (u.real ** 2) < 40
    if keep.any():
        with np.errstate(all="ignore"):
            t, h = frac_riccati(u[keep], T, alpha, lam, rho, nu, n=n)
        I1 = np.array([_frac_integral(hh, t, 1) for hh in h])
        I1a = np.array([_frac_integral(hh, t, 1 - alpha) for hh in h])
        with np.errstate(all="ignore"):
            z = np.exp(theta * lam * I1 + v0 * I1a)
        out[keep] = np.where(np.isfinite(z), z, 0.0)
    return out


def lifted_heston_cf(u, T, v0, lam, theta, nu, rho, H, N=20, rN=None, n_steps=400):
    """Abi Jaber and El Euch's (2019) lifted Heston: the fractional kernel t^{alpha-1}/Gamma(alpha) replaced by
    sum_i c_i exp(-x_i t) over N geometric nodes, which makes the model an N-factor Markovian Heston. Solved by an
    explicit Riccati system (Runge-Kutta 4). The theta here is the long-run level of the rough model's drift term."""
    u = np.atleast_1d(np.asarray(u, complex))
    alpha = H + 0.5
    rN = rN or 1 + 10 * N ** (-0.9)
    c = (rN ** (1 - alpha) - 1) * rN ** ((alpha - 1) * (1 + N / 2)) / (G(alpha) * G(2 - alpha)) * \
        rN ** ((1 - alpha) * np.arange(1, N + 1))
    x = (1 - alpha) / (2 - alpha) * (rN ** (2 - alpha) - 1) / (rN ** (1 - alpha) - 1) * rN ** (np.arange(1, N + 1) - 1 - N / 2)
    dt = T / n_steps

    def F(psi):
        s = psi @ c
        return (-0.5 * (u * u + 1j * u) + (1j * rho * nu * u - lam) * s + 0.5 * nu * nu * s * s)

    psi = np.zeros((len(u), N), complex)
    integ = np.zeros(len(u), complex)
    # g0(t) = v0 + lam theta int_0^t K(s) ds; we keep the classical lifted form with initial curve v0 + lam*theta*int K
    Kint = lambda tt: (c / x * (1 - np.exp(-x * tt))).sum()  # noqa: E731

    def g0(tt):
        return v0 + lam * theta * Kint(tt)

    def rhs(p):  # in time to maturity: d psi_j / d tau = -x_j psi_j + F(sum_i c_i psi_i)
        return -x[None, :] * p + F(p)[:, None]

    for i in range(n_steps):
        k1 = rhs(psi)
        k2 = rhs(psi + 0.5 * dt * k1)
        k3 = rhs(psi + 0.5 * dt * k2)
        k4 = rhs(psi + dt * k3)
        tau_mid = (i + 0.5) * dt
        integ += dt * F(psi + 0.5 * dt * k1) * g0(T - tau_mid)
        psi = psi + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
    return np.exp(integ)


# ---------------------------------------------------------------- roughness estimators


def log_rv_scaling(log_v, lags=(1, 2, 3, 4, 5, 7, 10, 15, 20, 30, 50), qs=(0.5, 1.0, 1.5, 2.0, 3.0)):
    """Gatheral, Jaisson and Rosenbaum's (2018) estimator: m(q, lag) = mean |log v_{t+lag} - log v_t|^q ~ lag^{q H}.
    Returns the slope zeta(q) for each q and H from the regression of zeta on q."""
    x = np.asarray(log_v, float)
    x = x[np.isfinite(x)]
    lags = np.asarray(lags)
    out = {}
    zeta = []
    for q in qs:
        m = np.array([np.mean(np.abs(x[L:] - x[:-L]) ** q) for L in lags])
        s = np.polyfit(np.log(lags), np.log(m), 1)[0]
        zeta.append(s)
        out[f"m_{q}"] = m
    zeta = np.array(zeta)
    H = float(np.polyfit(np.asarray(qs), zeta, 1)[0])
    out.update({"lags": lags, "qs": np.asarray(qs), "zeta": zeta, "H": H})
    return out


# ---------------------------------------------------------------- path-dependent volatility (Guyon and Lekeufack 2023)


def tspl_kernel(tau, alpha, delta):
    """Time-shifted power law K(tau) = (tau + delta)^(-alpha), normalized to integrate to one over tau >= 0."""
    z = delta ** (1 - alpha) / (alpha - 1)
    return (tau + delta) ** (-alpha) / z


def pdv_features(r, dt, a1, d1, a2, d2, lookback=1000):
    """R1_t = sum_i K1(t - t_i) r_i (a trend), R2_t = sum_i K2(t - t_i) r_i^2 (an activity), using the last
    ``lookback`` returns; r[i] is the return over day i, the features at the end of day i. With K integrating to one,
    R1 is an annualized drift and R2 an annualized variance."""
    r = np.asarray(r, float)
    tau = (np.arange(lookback) + 1) * dt - dt  # the latest return is at lag 0
    k1 = tspl_kernel(tau, a1, d1) * dt  # weights K(tau_i) dt, summing to about one ...
    k2 = tspl_kernel(tau, a2, d2) * dt
    n = len(r)
    R1 = np.convolve(r / dt, k1)[:n]  # ... on annualized quantities: R1 a drift, R2 a variance (Guyon-Lekeufack's units)
    R2 = np.convolve(r * r / dt, k2)[:n]
    return R1, R2


def fit_pdv(r, vol, dt=1 / 365, lookback=1000, burn=None):
    """Fit sigma_t = b0 + b1 R1_t + b2 sqrt(R2_t) to an implied-volatility index (Guyon and Lekeufack 2023, the
    4-factor PDV's parsimonious core): kernel shapes by least squares, betas by OLS inside. ``r`` and ``vol`` are
    aligned daily (vol at the end of day i). Returns the fit, R^2 and the fitted series."""
    r = np.asarray(r, float)
    vol = np.asarray(vol, float)
    burn = burn if burn is not None else min(lookback, len(r) // 3)

    def design(p):
        a1, d1, a2, d2 = p
        R1, R2 = pdv_features(r, dt, a1, d1, a2, d2, lookback)
        return np.column_stack([np.ones_like(R1), R1, np.sqrt(np.maximum(R2, 0))])

    def resid(p):
        X = design(p)[burn:]
        y = vol[burn:]
        b, *_ = np.linalg.lstsq(X, y, rcond=None)
        return X @ b - y

    r0 = least_squares(resid, [1.5, 0.02, 1.5, 0.05], bounds=([1.01, 1e-4, 1.01, 1e-4], [5, 1.0, 5, 1.0]))
    X = design(r0.x)
    b, *_ = np.linalg.lstsq(X[burn:], vol[burn:], rcond=None)
    fit = X @ b
    y = vol[burn:]
    r2 = 1 - np.sum((fit[burn:] - y) ** 2) / np.sum((y - y.mean()) ** 2)
    return {"alpha1": r0.x[0], "delta1": r0.x[1], "alpha2": r0.x[2], "delta2": r0.x[3], "beta": b.tolist(),
            "r2": float(r2), "fit": fit, "burn": burn}
