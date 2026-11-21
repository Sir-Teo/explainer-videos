"""Agora's solver harness (Part 51): one set of methods for economies that have no formula, each returning its
answer with a report (iterations, seconds, tolerance and Euler-equation errors).

* **The growth model** (:func:`growth`): CRRA utility, Cobb-Douglas output, depreciation; its steady state.
* **The Bellman operator** (:func:`bellman`) on a grid of capital, its contraction (:func:`contraction_path`) and
  Blackwell's two conditions checked numerically (:func:`blackwell`); value function iteration (:func:`vfi`) and
  Howard's policy iteration (:func:`howard`), timed.
* **Interpolation** (:func:`vfi_continuous`): the choice between grid points by golden-section search, with linear,
  cubic-spline or Chebyshev interpolation of the value function.
* **The household** (:func:`household`): an income-fluctuation problem with a borrowing limit and a Rouwenhorst
  income chain, solved by grid-search value iteration (:func:`household_vfi`) and by Carroll's endogenous grid
  method (:func:`egm`), with its Euler errors (:func:`household_euler_errors`).
* **Projection** (:func:`collocation`, :func:`galerkin`): the consumption rule of the growth model as a Chebyshev
  polynomial, its coefficients set so the Euler equation holds at the nodes, or on average against each basis
  function; and the derivative of the solution with respect to a parameter by the implicit function theorem
  (:func:`collocation_derivative`), what differentiable programming automates.
* **Perturbation** (:func:`perturbation`): the policy's first and second derivatives at the steady state.
* **Accuracy** (:func:`euler_errors`): Judd's unit-free Euler-equation errors, in log10.
* **Expectations** (:func:`gauss_hermite`, :func:`quadrature_error`): Gauss-Hermite nodes against Monte Carlo.
* **Continuous time** (:func:`hjb_household`): the Hamilton-Jacobi-Bellman equation of a household with two income
  states and a borrowing limit, by Achdou et al.'s implicit upwind finite differences on a sparse matrix, and the
  stationary distribution from the Kolmogorov forward equation.
* **Dimensions** (:func:`smolyak_count`, :func:`smolyak_interpolate`): the number of points of a Smolyak sparse grid
  against a tensor grid, and sparse-grid interpolation by the combination technique.

numpy and scipy only.
"""

from __future__ import annotations

import time
from itertools import product
from math import comb

import numpy as np
from numpy.polynomial import chebyshev as C
from scipy import sparse
from scipy.interpolate import CubicSpline
from scipy.optimize import root
from scipy.sparse.linalg import spsolve

# ---------------------------------------------------------------------------------------------------------------
# the growth model


def growth(alpha: float = 0.36, beta: float = 0.96, delta: float = 0.08, gamma: float = 2.0, A: float = 1.0) -> dict:
    """The neoclassical growth model: max sum beta^t u(c_t), u = c^(1-gamma)/(1-gamma) (log at 1), with
    k' = A k^alpha + (1 - delta) k - c.  Returns the parameters and the steady state."""
    kss = ((1 / beta - 1 + delta) / (alpha * A)) ** (1 / (alpha - 1))
    css = A * kss ** alpha - delta * kss
    return {"alpha": alpha, "beta": beta, "delta": delta, "gamma": gamma, "A": A, "kss": kss, "css": css}


def u(c, gamma):
    c = np.asarray(c, float)
    if abs(gamma - 1) < 1e-12:
        return np.log(c)
    return c ** (1 - gamma) / (1 - gamma)


def up(c, gamma):
    return np.asarray(c, float) ** (-gamma)


def up_inv(x, gamma):
    return np.asarray(x, float) ** (-1 / gamma)


def resources(k, m):
    """Output plus undepreciated capital."""
    k = np.asarray(k, float)
    return m["A"] * k ** m["alpha"] + (1 - m["delta"]) * k


def mpk(k, m):
    """The gross return on capital, f'(k) + 1 - delta."""
    k = np.asarray(k, float)
    return m["A"] * m["alpha"] * k ** (m["alpha"] - 1) + 1 - m["delta"]


def kgrid(m, n: int = 200, lo: float = 0.5, hi: float = 1.5) -> np.ndarray:
    return np.linspace(lo * m["kss"], hi * m["kss"], n)


# ---------------------------------------------------------------------------------------------------------------
# the Bellman operator on a grid


def _payoff(m, grid):
    c = resources(grid, m)[:, None] - grid[None, :]
    U = np.full_like(c, -np.inf)
    ok = c > 0
    U[ok] = u(c[ok], m["gamma"])
    return U


def bellman(V, grid, m, U=None):
    """One application of the Bellman operator with next period's capital chosen on the grid: returns (TV, the index
    of the best choice for each point)."""
    U = _payoff(m, grid) if U is None else U
    W = U + m["beta"] * np.asarray(V)[None, :]
    j = np.argmax(W, axis=1)
    return W[np.arange(len(grid)), j], j


def vfi(m, grid, tol: float = 1e-6, max_iter: int = 5000, V0=None, keep: tuple = ()) -> dict:
    """Value function iteration to a sup-norm change below ``tol``: the value function, the policy (indices and
    values), the number of iterations, the distance at each, the seconds taken and the iterates in ``keep``."""
    t0 = time.perf_counter()
    U = _payoff(m, grid)
    V = np.zeros(len(grid)) if V0 is None else np.asarray(V0, float).copy()
    dist, kept = [], {}
    for it in range(1, max_iter + 1):
        TV, j = bellman(V, grid, m, U)
        d = float(np.max(np.abs(TV - V)))
        dist.append(d)
        if it in keep:
            kept[it] = TV.copy()
        V = TV
        if d < tol:
            break
    return {"V": V, "j": j, "kprime": grid[j], "iters": it, "dist": dist, "seconds": time.perf_counter() - t0,
            "kept": kept}


def howard(m, grid, tol: float = 1e-10, max_iter: int = 200) -> dict:
    """Howard's policy iteration: evaluate the current policy exactly (a sparse linear system), then improve it;
    stop when the policy no longer changes."""
    t0 = time.perf_counter()
    n = len(grid)
    U = _payoff(m, grid)
    _, j = bellman(np.zeros(n), grid, m, U)
    changes = []
    for it in range(1, max_iter + 1):
        P = sparse.csr_matrix((np.ones(n), (np.arange(n), j)), shape=(n, n))
        V = spsolve((sparse.identity(n, format="csr") - m["beta"] * P).tocsc(), U[np.arange(n), j])
        _, j_new = bellman(V, grid, m, U)
        changes.append(int(np.sum(j_new != j)))
        if changes[-1] == 0:
            break
        j = j_new
    return {"V": V, "j": j, "kprime": grid[j], "iters": it, "changes": changes, "seconds": time.perf_counter() - t0}


def contraction_path(m, grid, n: int = 40, V0=None) -> dict:
    """The distances ||T^{i+1} V0 - T^i V0|| and their ratios, which approach beta."""
    U = _payoff(m, grid)
    V = np.zeros(len(grid)) if V0 is None else np.asarray(V0, float)
    d = []
    for _ in range(n):
        TV, _ = bellman(V, grid, m, U)
        d.append(float(np.max(np.abs(TV - V))))
        V = TV
    d = np.array(d)
    return {"dist": d.tolist(), "ratio": (d[1:] / d[:-1]).tolist()}


def blackwell(m, grid, a: float = 1.0, seed: int = 0) -> dict:
    """Blackwell's sufficient conditions checked on random value functions: monotonicity (V <= W implies
    TV <= TW) and discounting (T(V + a) = TV + beta a)."""
    rng = np.random.default_rng(seed)
    U = _payoff(m, grid)
    V = rng.normal(0, 1, len(grid)) + u(m["css"], m["gamma"]) / (1 - m["beta"])
    W = V + np.abs(rng.normal(0, 1, len(grid)))
    TV, _ = bellman(V, grid, m, U)
    TW, _ = bellman(W, grid, m, U)
    TVa, _ = bellman(V + a, grid, m, U)
    return {"monotone": bool(np.all(TW >= TV - 1e-12)), "discount_error": float(np.max(np.abs(TVa - TV
                                                                                               - m["beta"] * a)))}


# ---------------------------------------------------------------------------------------------------------------
# continuous choice with interpolation


def _golden_max(f, lo, hi, iters: int = 60):
    """Vectorized golden-section search for the maximum of f on [lo, hi] (elementwise)."""
    g = (np.sqrt(5) - 1) / 2
    a, b = np.array(lo, float), np.array(hi, float)
    c = b - g * (b - a)
    d = a + g * (b - a)
    fc, fd = f(c), f(d)
    for _ in range(iters):
        left = fc > fd
        b = np.where(left, d, b)
        a = np.where(left, a, c)
        d_new = np.where(left, c, a + g * (b - a))
        c_new = np.where(left, b - g * (b - a), d)
        fc_old, fd_old = fc, fd
        fd = np.where(left, fc_old, f(d_new))
        fc = np.where(left, f(c_new), fd_old)
        c, d = c_new, d_new
    x = (a + b) / 2
    return x, f(x)


def chebyshev_nodes(n: int, lo: float, hi: float) -> np.ndarray:
    z = -np.cos((2 * np.arange(1, n + 1) - 1) * np.pi / (2 * n))
    return lo + (z + 1) * (hi - lo) / 2


def _interpolant(kind, grid, V):
    lo, hi = grid[0], grid[-1]
    if kind == "linear":
        return lambda x: np.interp(x, grid, V)
    if kind == "cubic":
        return CubicSpline(grid, V)
    if kind == "chebyshev":
        coef = C.chebfit(2 * (grid - lo) / (hi - lo) - 1, V, len(grid) - 1)
        return lambda x: C.chebval(2 * (np.asarray(x) - lo) / (hi - lo) - 1, coef)
    raise ValueError(kind)


def vfi_continuous(m, grid, kind: str = "linear", tol: float = 1e-7, max_iter: int = 2000) -> dict:
    """Value function iteration with next period's capital chosen anywhere in [grid[0], grid[-1]] by golden-section
    search on an interpolated value function ("linear", "cubic" or "chebyshev"; for Chebyshev the grid should be
    Chebyshev nodes).  Returns the values at the grid, the policy there and a callable policy."""
    t0 = time.perf_counter()
    grid = np.asarray(grid, float)
    V = u(resources(grid, m) - grid, m["gamma"]) / (1 - m["beta"])
    R = resources(grid, m)
    lo = np.full_like(grid, grid[0])
    hi = np.minimum(grid[-1], R - 1e-8)
    for it in range(1, max_iter + 1):
        Vh = _interpolant(kind, grid, V)
        kp, TV = _golden_max(lambda x: u(R - x, m["gamma"]) + m["beta"] * Vh(x), lo, hi)
        d = float(np.max(np.abs(TV - V)))
        V = TV
        if d < tol:
            break
    pol = _interpolant(kind if kind != "chebyshev" else "chebyshev", grid, kp)
    return {"V": V, "kprime": kp, "iters": it, "seconds": time.perf_counter() - t0,
            "c": lambda k: resources(k, m) - pol(k)}


# ---------------------------------------------------------------------------------------------------------------
# the household: an income-fluctuation problem


def rouwenhorst(n: int, rho: float, sigma: float) -> tuple:
    """Rouwenhorst's chain for an AR(1) in logs with persistence rho and innovation s.d. sigma: (states, P)."""
    p = (1 + rho) / 2
    P = np.array([[p, 1 - p], [1 - p, p]])
    for k in range(3, n + 1):
        Q = np.zeros((k, k))
        Q[:-1, :-1] += p * P
        Q[:-1, 1:] += (1 - p) * P
        Q[1:, :-1] += (1 - p) * P
        Q[1:, 1:] += p * P
        Q[1:-1] /= 2
        P = Q
    psi = sigma / np.sqrt(1 - rho ** 2) * np.sqrt(n - 1)
    return np.linspace(-psi, psi, n), P


def household(beta: float = 0.95, R: float = 1.03, gamma: float = 2.0, rho: float = 0.9, sigma: float = 0.2,
              n_y: int = 5, a_min: float = 0.0, a_max: float = 40.0, n_a: int = 200) -> dict:
    """An income-fluctuation problem: max E sum beta^t u(c), a' = R a + y - c >= a_min, log y a Rouwenhorst chain
    normalized to mean one.  The asset grid is denser near the limit."""
    z, P = rouwenhorst(n_y, rho, sigma)
    y = np.exp(z)
    pi = np.linalg.matrix_power(P, 500)[0]
    y = y / (pi @ y)
    x = np.linspace(0, 1, n_a)
    a = a_min + (a_max - a_min) * x ** 2
    return {"beta": beta, "R": R, "gamma": gamma, "y": y, "P": P, "pi": pi, "a": a, "a_min": a_min}


def egm(h, tol: float = 1e-9, max_iter: int = 5000) -> dict:
    """Carroll's endogenous grid method: from the consumption rule tomorrow on the grid of savings, the Euler
    equation gives consumption today directly, and the budget gives the assets it is chosen at; no root finding.
    Returns consumption on the asset grid for each income state, iterations and seconds."""
    t0 = time.perf_counter()
    a, y, P, R, beta, g = h["a"], h["y"], h["P"], h["R"], h["beta"], h["gamma"]
    c = (R - 1) * a[:, None] + y[None, :]                  # a first guess: eat the interest and income
    for it in range(1, max_iter + 1):
        emu = up(c, g) @ P.T                                # E[u'(c(a', y')) | y], a' on the grid
        c_end = up_inv(beta * R * emu, g)                   # consumption today at each (a', y)
        a_end = (c_end + a[:, None] - y[None, :]) / R       # the assets today that choose a'
        c_new = np.empty_like(c)
        for s in range(len(y)):
            c_new[:, s] = np.interp(a, a_end[:, s], c_end[:, s])
            bind = a < a_end[0, s]                          # below the first endogenous point the limit binds
            c_new[bind, s] = R * a[bind] + y[s] - h["a_min"]
        d = float(np.max(np.abs(c_new - c)))
        c = c_new
        if d < tol:
            break
    return {"c": c, "iters": it, "seconds": time.perf_counter() - t0}


def household_vfi(h, tol: float = 1e-6, max_iter: int = 5000) -> dict:
    """The same household by value function iteration with savings chosen on the asset grid."""
    t0 = time.perf_counter()
    a, y, P, R, beta, g = h["a"], h["y"], h["P"], h["R"], h["beta"], h["gamma"]
    n_a, n_y = len(a), len(y)
    cons = R * a[:, None, None] + y[None, None, :] - a[None, :, None]   # (a, a', y)
    U = np.full(cons.shape, -np.inf)
    ok = cons > 0
    U[ok] = u(cons[ok], g)
    V = u(np.maximum((R - 1) * a[:, None] + y[None, :], 1e-6), g) / (1 - beta)
    for it in range(1, max_iter + 1):
        EV = V @ P.T                                        # (a', y)
        W = U + beta * EV[None, :, :]
        j = np.argmax(W, axis=1)
        TV = np.take_along_axis(W, j[:, None, :], axis=1)[:, 0, :]
        d = float(np.max(np.abs(TV - V)))
        V = TV
        if d < tol:
            break
    c = R * a[:, None] + y[None, :] - a[j]
    return {"V": V, "c": c, "iters": it, "seconds": time.perf_counter() - t0, "n": n_a * n_y}


def household_euler_errors(h, c, a_test=None) -> dict:
    """Euler-equation errors of a consumption rule ``c`` (on h's asset grid) at test points between the grid
    points, where the borrowing limit does not bind: log10 |1 - u'^{-1}(beta R E u'(c')) / c|."""
    a, y, P, R, beta, g = h["a"], h["y"], h["P"], h["R"], h["beta"], h["gamma"]
    a_test = np.linspace(a[1], a[-1] * 0.8, 400) if a_test is None else a_test
    out = []
    for s in range(len(y)):
        ct = np.interp(a_test, a, c[:, s])
        ap = R * a_test + y[s] - ct
        emu = np.zeros_like(a_test)
        for s2 in range(len(y)):
            emu += P[s, s2] * up(np.interp(ap, a, c[:, s2]), g)
        free = ap > h["a_min"] + 1e-6
        e = np.abs(1 - up_inv(beta * R * emu, g) / ct)
        out.append(np.log10(np.maximum(e[free], 1e-17)))
    allv = np.concatenate(out)
    return {"max": float(allv.max()), "mean": float(allv.mean()), "a": a_test.tolist()}


# ---------------------------------------------------------------------------------------------------------------
# projection


def _cheb_c(theta, k, lo, hi):
    return C.chebval(2 * (np.asarray(k) - lo) / (hi - lo) - 1, theta)


def _residual(theta, k, m, lo, hi):
    c = _cheb_c(theta, k, lo, hi)
    kp = resources(k, m) - c
    cp = _cheb_c(theta, kp, lo, hi)
    return up(c, m["gamma"]) - m["beta"] * up(np.maximum(cp, 1e-10), m["gamma"]) * mpk(np.maximum(kp, 1e-10), m)


def _start(m, n, lo, hi):
    g1 = perturbation(m, order=1)["g1"]
    k = chebyshev_nodes(max(n, 2), lo, hi)
    c = m["css"] + (mpk(m["kss"], m) - g1) * (k - m["kss"])
    return C.chebfit(2 * (k - lo) / (hi - lo) - 1, c, n - 1)


def collocation(m, n: int = 6, lo: float | None = None, hi: float | None = None) -> dict:
    """The consumption rule c(k) as a Chebyshev polynomial of degree n - 1 whose Euler residual is zero at the n
    Chebyshev nodes (Judd 1992)."""
    lo = 0.5 * m["kss"] if lo is None else lo
    hi = 1.5 * m["kss"] if hi is None else hi
    t0 = time.perf_counter()
    th = _start(m, 2, lo, hi)
    for deg in range(2, n + 1):                  # continuation: each degree starts from the one below
        th = np.concatenate([th, np.zeros(deg - len(th))])
        k = chebyshev_nodes(deg, lo, hi)
        sol = root(lambda t, k=k: _residual(t, k, m, lo, hi), th, method="hybr", tol=1e-14)
        th = sol.x
    resid = float(np.max(np.abs(_residual(th, chebyshev_nodes(n, lo, hi), m, lo, hi))))
    return {"theta": th, "ok": resid < 1e-9, "residual": resid, "lo": lo, "hi": hi,
            "seconds": time.perf_counter() - t0, "c": lambda kk: _cheb_c(th, kk, lo, hi)}


def galerkin(m, n: int = 6, lo: float | None = None, hi: float | None = None, n_quad: int = 60) -> dict:
    """The same rule with the residual made orthogonal to each of the n Chebyshev polynomials, by Gauss-Chebyshev
    quadrature."""
    lo = 0.5 * m["kss"] if lo is None else lo
    hi = 1.5 * m["kss"] if hi is None else hi
    t0 = time.perf_counter()
    zq = -np.cos((2 * np.arange(1, n_quad + 1) - 1) * np.pi / (2 * n_quad))
    kq = lo + (zq + 1) * (hi - lo) / 2
    T = np.array([C.chebval(zq, np.eye(n)[j]) for j in range(n)])

    def eqs(th):
        return T @ _residual(th, kq, m, lo, hi)

    start = collocation(m, min(n, 4), lo, hi)["theta"]
    sol = root(eqs, np.concatenate([start, np.zeros(n - len(start))]), method="hybr", tol=1e-14)
    resid = float(np.max(np.abs(eqs(sol.x))))
    return {"theta": sol.x, "ok": resid < 1e-9, "residual": resid, "lo": lo, "hi": hi,
            "seconds": time.perf_counter() - t0, "c": lambda kk: _cheb_c(sol.x, kk, lo, hi)}


def collocation_derivative(m, n: int = 8, param: str = "beta", h: float = 1e-6) -> dict:
    """The derivative of the collocation solution's coefficients (and of consumption at the steady state) with
    respect to a parameter, by the implicit function theorem, d theta = -J_theta^{-1} J_param, against finite
    differences of the whole solution."""
    lo, hi = 0.5 * m["kss"], 1.5 * m["kss"]
    s = collocation(m, n, lo, hi)
    k = chebyshev_nodes(n, lo, hi)
    th = s["theta"]

    def F(t, mm):
        return _residual(t, k, mm, lo, hi)

    J = np.empty((n, n))
    for j in range(n):
        e = np.zeros(n)
        e[j] = h
        J[:, j] = (F(th + e, m) - F(th - e, m)) / (2 * h)
    mp = {**m, param: m[param] + h}
    mm = {**m, param: m[param] - h}
    Jp = (F(th, mp) - F(th, mm)) / (2 * h)
    dth = -np.linalg.solve(J, Jp)
    dc_ift = float(_cheb_c(dth, m["kss"], lo, hi))
    big = 1e-4
    up_ = collocation({**m, param: m[param] + big}, n, lo, hi)["theta"]
    dn_ = collocation({**m, param: m[param] - big}, n, lo, hi)["theta"]
    dc_fd = float((_cheb_c(up_, m["kss"], lo, hi) - _cheb_c(dn_, m["kss"], lo, hi)) / (2 * big))
    return {"dtheta": dth.tolist(), "dc_ift": dc_ift, "dc_fd": dc_fd}


# ---------------------------------------------------------------------------------------------------------------
# perturbation


def _F(k, g, m):
    """The Euler residual along a policy g for capital: u'(c) - beta u'(c') R(k'), with c = f(k) - g(k)."""
    kp = g(k)
    c = resources(k, m) - kp
    cp = resources(kp, m) - g(kp)
    return up(c, m["gamma"]) - m["beta"] * up(cp, m["gamma"]) * mpk(kp, m)


def perturbation(m, order: int = 2) -> dict:
    """The policy k' = g(k) of the deterministic growth model expanded around the steady state: g1 = g'(kss) solves
    a quadratic (the stable root), and g2 = g''(kss) makes the second derivative of the Euler residual zero, a
    linear equation solved numerically."""
    kss, css, g, beta = m["kss"], m["css"], m["gamma"], m["beta"]
    upp = -g * css ** (-g - 1)
    fpp = m["A"] * m["alpha"] * (m["alpha"] - 1) * kss ** (m["alpha"] - 2)
    a2, a1, a0 = upp, -(upp * (1 + 1 / beta) + beta * up(css, g) * fpp), upp / beta
    roots = np.roots([a2, a1, a0])
    g1 = float(np.real(roots[np.argmin(np.abs(roots))]))
    out = {"g1": g1, "order": order}
    if order >= 2:
        h = 1e-3 * kss

        def F2(g2):
            pol = lambda k: kss + g1 * (k - kss) + 0.5 * g2 * (k - kss) ** 2  # noqa: E731
            return (_F(kss + h, pol, m) - 2 * _F(kss, pol, m) + _F(kss - h, pol, m)) / h ** 2

        f0, f1 = F2(0.0), F2(1.0)
        out["g2"] = float(-f0 / (f1 - f0))
    else:
        out["g2"] = 0.0
    g2 = out["g2"]
    out["kprime"] = lambda k: kss + g1 * (np.asarray(k) - kss) + 0.5 * g2 * (np.asarray(k) - kss) ** 2
    out["c"] = lambda k: resources(k, m) - out["kprime"](k)
    return out


# ---------------------------------------------------------------------------------------------------------------
# accuracy


def euler_errors(m, c, k=None) -> dict:
    """Judd's unit-free Euler-equation errors of a consumption rule ``c`` (a callable) for the deterministic growth
    model: log10 |1 - u'^{-1}(beta u'(c(k')) R(k')) / c(k)| on a fine grid between 0.6 and 1.4 times the steady
    state.  -4 means a mistake of one dollar in ten thousand."""
    k = np.linspace(0.6 * m["kss"], 1.4 * m["kss"], 1001) if k is None else np.asarray(k)
    ck = c(k)
    kp = resources(k, m) - ck
    e = np.abs(1 - up_inv(m["beta"] * up(c(kp), m["gamma"]) * mpk(kp, m), m["gamma"]) / ck)
    le = np.log10(np.maximum(e, 1e-17))
    return {"k": k.tolist(), "log10": le.tolist(), "max": float(le.max()), "mean": float(le.mean())}


# ---------------------------------------------------------------------------------------------------------------
# expectations


def gauss_hermite(n: int) -> tuple:
    """Nodes and weights for E[f(e)] with e ~ N(0, 1)."""
    x, w = np.polynomial.hermite.hermgauss(n)
    return np.sqrt(2) * x, w / np.sqrt(np.pi)


def quadrature_error(f, exact: float, ns=(1, 2, 3, 5, 7, 10), draws=(10, 100, 1000, 10000, 100000),
                     seed: int = 0) -> dict:
    """The absolute error of E[f(e)], e ~ N(0, 1), by Gauss-Hermite with n nodes and by Monte Carlo with n draws
    (the root mean squared error over 200 repetitions)."""
    gh = []
    for n in ns:
        x, w = gauss_hermite(n)
        gh.append(abs(float(w @ f(x)) - exact))
    rng = np.random.default_rng(seed)
    mc = []
    for d in draws:
        est = [f(rng.standard_normal(d)).mean() for _ in range(200)]
        mc.append(float(np.sqrt(np.mean((np.array(est) - exact) ** 2))))
    return {"nodes": list(ns), "gh": gh, "draws": list(draws), "mc": mc}


# ---------------------------------------------------------------------------------------------------------------
# continuous time


def hjb_household(rho: float = 0.05, r: float = 0.03, gamma: float = 2.0, z=(0.1, 0.2), lam=(1.2, 1.2),
                  a_min: float = -0.15, a_max: float = 5.0, n: int = 500, Delta: float = 1000.0,
                  tol: float = 1e-8, max_iter: int = 100) -> dict:
    """A household in continuous time with income z1 or z2, switching at rates lam, saving at rate r above a
    borrowing limit: rho v_j = max u(c) + v_j'(a)(z_j + r a - c) + lam_j (v_-j - v_j), solved by the implicit upwind
    scheme of Achdou, Han, Lasry, Lions and Moll (2022) on a sparse matrix; then the stationary distribution from
    A' g = 0."""
    t0 = time.perf_counter()
    a = np.linspace(a_min, a_max, n)
    da = a[1] - a[0]
    zz = np.array(z)[None, :] * np.ones((n, 1))
    aa = a[:, None] * np.ones((1, 2))
    v = u(zz + r * aa, gamma) / rho
    sw = sparse.bmat([[-lam[0] * sparse.identity(n), lam[0] * sparse.identity(n)],
                      [lam[1] * sparse.identity(n), -lam[1] * sparse.identity(n)]], format="csr")
    dists = []
    for it in range(1, max_iter + 1):
        dvf = np.zeros((n, 2))
        dvb = np.zeros((n, 2))
        dvf[:-1] = (v[1:] - v[:-1]) / da
        dvf[-1] = up(zz[-1] + r * a_max, gamma)
        dvb[1:] = (v[1:] - v[:-1]) / da
        dvb[0] = up(zz[0] + r * a_min, gamma)
        cf = up_inv(np.maximum(dvf, 1e-12), gamma)
        cb = up_inv(np.maximum(dvb, 1e-12), gamma)
        sf = zz + r * aa - cf
        sb = zz + r * aa - cb
        If = sf > 0
        Ib = (sb < 0) & ~If
        I0 = ~If & ~Ib
        c = cf * If + cb * Ib + (zz + r * aa) * I0
        X = -np.minimum(sb, 0) * Ib / da
        Z = np.maximum(sf, 0) * If / da
        Y = -X - Z
        blocks = []
        for j in range(2):
            blocks.append(sparse.diags([X[1:, j], Y[:, j], Z[:-1, j]], [-1, 0, 1], shape=(n, n)))
        A = sparse.block_diag(blocks, format="csr") + sw
        B = (1 / Delta + rho) * sparse.identity(2 * n, format="csr") - A
        b = u(c, gamma).T.ravel() + v.T.ravel() / Delta
        vn = spsolve(B.tocsc(), b).reshape(2, n).T
        d = float(np.max(np.abs(vn - v)))
        dists.append(d)
        v = vn
        if d < tol:
            break
    AT = A.T.tocsr().tolil()
    rhs = np.zeros(2 * n)
    AT[0, :] = 0
    AT[0, 0] = 1
    rhs[0] = 0.1
    g = spsolve(AT.tocsc(), rhs)
    g = np.maximum(g, 0)
    g = g / (g.sum() * da)
    s = zz + r * aa - c
    return {"a": a.tolist(), "c": c.tolist(), "s": s.tolist(), "g": g.reshape(2, n).T.tolist(), "iters": it,
            "dist": dists, "seconds": time.perf_counter() - t0, "nnz": int(A.nnz), "size": 2 * n}


# ---------------------------------------------------------------------------------------------------------------
# occasionally binding constraints


def zlb_occbin(T: int = 8, rn_low: float = -2.0, H: int = 40, beta: float = 0.99, sigma: float = 1.0,
               kappa: float = 0.1275, phi_pi: float = 1.5, phi_x: float = 0.5, max_iter: int = 50) -> dict:
    """The three-equation New Keynesian model with the natural real rate at ``rn_low`` (annual percent) for ``T``
    quarters, solved under perfect foresight with the zero bound on the policy rate imposed by guess and verify, as
    in Guerrieri and Iacoviello's OccBin: guess the quarters at the bound, solve the linear model for that regime
    sequence, find where the rule would ask for a negative rate, and repeat until the guess is confirmed.  Returns the
    paths with the bound and with the bound ignored (annualized percent; the output gap in percent)."""
    n = H
    rstar = 1 / beta - 1
    t = np.arange(n)
    rn = np.where(t < T, rn_low / 400, rstar)

    def path(bound):
        A = np.zeros((3 * n, 3 * n))
        b = np.zeros(3 * n)
        X, P, I = 0, n, 2 * n
        for k in range(n):
            r = k                                      # IS: x_k - x_{k+1} + (i_k - pi_{k+1}) / sigma = rn_k / sigma
            A[r, X + k] = 1
            if k + 1 < n:
                A[r, X + k + 1] = -1
                A[r, P + k + 1] = -1 / sigma
            A[r, I + k] = 1 / sigma
            b[r] = rn[k] / sigma
            r = n + k                                  # Phillips curve: pi_k - beta pi_{k+1} - kappa x_k = 0
            A[r, P + k] = 1
            if k + 1 < n:
                A[r, P + k + 1] = -beta
            A[r, X + k] = -kappa
            r = 2 * n + k                              # the rule, or the bound
            A[r, I + k] = 1
            if not bound[k]:
                A[r, P + k] = -phi_pi
                A[r, X + k] = -phi_x
                b[r] = rstar
        z = np.linalg.solve(A, b)
        return z[:n], z[n:2 * n], z[2 * n:]

    free = path(np.zeros(n, bool))
    bound = np.zeros(n, bool)
    guesses = []
    for it in range(1, max_iter + 1):
        x, pi, i = path(bound)
        shadow = rstar + phi_pi * pi + phi_x * x
        new = shadow < 0
        guesses.append(int(new.sum()))
        if np.array_equal(new, bound):
            break
        bound = new
    ann = lambda v: (400 * np.asarray(v)).tolist()  # noqa: E731
    return {"q": t.tolist(), "x": (100 * x).tolist(), "pi": ann(pi), "i": ann(i), "shadow": ann(shadow),
            "x_free": (100 * free[0]).tolist(), "pi_free": ann(free[1]), "i_free": ann(free[2]),
            "bound_quarters": int(bound.sum()), "iters": it, "guesses": guesses, "rn": ann(rn)}


# ---------------------------------------------------------------------------------------------------------------
# dimensions


def _cc_nodes(i: int) -> np.ndarray:
    """The Clenshaw-Curtis (Chebyshev extrema) nodes of level i: 1 point at level 1, 2^(i-1) + 1 above."""
    if i == 1:
        return np.array([0.0])
    m_ = 2 ** (i - 1) + 1
    return -np.cos(np.pi * np.arange(m_) / (m_ - 1))


def smolyak_count(d: int, mu: int) -> int:
    """The number of distinct points of the Smolyak sparse grid of dimension d and level mu, built from nested
    Clenshaw-Curtis nodes."""
    new = {1: 1, 2: 2}

    def dm(i):
        return new.get(i, 2 ** (i - 2))

    # count multi-indices with |i| <= d + mu, weighting each by the product of new points
    poly = {0: 1}                                   # sum of (i_j - 1) -> weighted count
    for _ in range(d):
        nxt = {}
        for s, w in poly.items():
            for i in range(1, mu + 2):
                t = s + i - 1
                if t <= mu:
                    nxt[t] = nxt.get(t, 0) + w * dm(i)
        poly = nxt
    return int(sum(poly.values()))


def tensor_count(d: int, mu: int) -> int:
    return (2 ** mu + 1) ** d if mu > 0 else 1


def _interp1(nodes, vals_axis, x):
    """Polynomial interpolation through ``nodes`` (barycentric for Chebyshev extrema) along the first axis of
    ``vals_axis`` evaluated at x."""
    m_ = len(nodes)
    if m_ == 1:
        return np.repeat(vals_axis[:1], len(x), axis=0)
    w = np.ones(m_)
    w[1::2] = -1
    w[0] *= 0.5
    w[-1] *= 0.5
    diff = x[:, None] - nodes[None, :]
    exact = np.isclose(diff, 0)
    diff[exact] = 1
    t = w[None, :] / diff
    t[exact.any(axis=1)] = exact[exact.any(axis=1)].astype(float)
    t = t / t.sum(axis=1, keepdims=True)
    return np.tensordot(t, vals_axis, axes=(1, 0))


def _tensor_interp(f, levels, X):
    """Tensor-product interpolation of f on the Clenshaw-Curtis grid of the given levels, evaluated at X (n x d)."""
    nodes = [_cc_nodes(i) for i in levels]
    grid = np.array(list(product(*nodes)))
    vals = f(grid).reshape([len(n_) for n_ in nodes])
    out = np.empty(len(X))
    for r_, x in enumerate(X):
        v = vals
        for j in range(len(levels)):
            v = _interp1(nodes[j], v, np.array([x[j]]))[0]
        out[r_] = v
    return out, len(grid)


def smolyak_interpolate(f, d: int, mu: int, X) -> dict:
    """Smolyak's sparse-grid interpolant of f on [-1, 1]^d at level mu by the combination technique: the sum over
    multi-indices with d + mu - d + 1 <= |i| <= d + mu of (-1)^(d + mu - |i|) C(d - 1, d + mu - |i|) times the
    tensor interpolant of levels i.  Returns the values at X and the number of distinct points used."""
    X = np.atleast_2d(X)
    total = np.zeros(len(X))
    pts = set()
    q = d + mu
    for levels in product(range(1, mu + 2), repeat=d):
        s = sum(levels)
        if q - d + 1 <= s <= q:
            coef = (-1) ** (q - s) * comb(d - 1, q - s)
            val, _ = _tensor_interp(f, levels, X)
            total += coef * val
            for p in product(*[_cc_nodes(i) for i in levels]):
                pts.add(tuple(np.round(p, 12)))
    return {"values": total, "points": len(pts)}


def tensor_interpolate(f, d: int, level: int, X) -> dict:
    """The full tensor-product Chebyshev-extrema interpolant of the given level in every dimension."""
    val, n = _tensor_interp(f, [level] * d, np.atleast_2d(X))
    return {"values": val, "points": n}


__all__ = ["growth", "u", "up", "up_inv", "resources", "mpk", "kgrid", "bellman", "vfi", "howard",
           "contraction_path", "blackwell", "chebyshev_nodes", "vfi_continuous", "rouwenhorst", "household", "egm",
           "household_vfi", "household_euler_errors", "collocation", "galerkin", "collocation_derivative",
           "perturbation", "euler_errors", "gauss_hermite", "quadrature_error", "hjb_household", "zlb_occbin",
           "smolyak_count",
           "tensor_count", "smolyak_interpolate", "tensor_interpolate"]
