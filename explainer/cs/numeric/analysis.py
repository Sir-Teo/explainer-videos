"""Roots, approximation, quadrature and differential equations (Part 52): bisection, secant and Newton with their
orders of convergence; Newton's fractal for z^3 - 1; Runge's phenomenon against Chebyshev points and barycentric
interpolation (Trefethen, *Approximation Theory and Approximation Practice*); Gauss, adaptive and Monte Carlo
quadrature; explicit Runge-Kutta with step control, stiffness and A-stability; and symplectic leapfrog against RK4
on a long orbit (Hairer, Lubich and Wanner, *Geometric Numerical Integration*)."""

from __future__ import annotations

import math

import numpy as np

# ---------------------------------------------------------------- roots


def root_race(f=lambda x: x * x - 2, df=lambda x: 2 * x, a=1.0, b=2.0, root=math.sqrt(2)) -> dict:
    """Correct digits after each iteration of bisection (linear: one bit a step), the secant method (order
    (1 + sqrt 5)/2) and Newton (quadratic)."""
    def digits(x):
        e = abs(x - root)
        return 16.0 if e == 0 else min(16.0, -math.log10(e))
    out = {"bisection": [], "secant": [], "newton": []}
    lo, hi = a, b
    for _ in range(40):
        mid = (lo + hi) / 2
        out["bisection"].append(digits(mid))
        if f(lo) * f(mid) <= 0:
            hi = mid
        else:
            lo = mid
    x0, x1 = a, b
    for _ in range(10):
        if f(x1) == f(x0):
            break
        x0, x1 = x1, x1 - f(x1) * (x1 - x0) / (f(x1) - f(x0))
        out["secant"].append(digits(x1))
    x = b
    for _ in range(7):
        x = x - f(x) / df(x)
        out["newton"].append(digits(x))
    return out


def newton_fractal(n: int = 300, center=(0.0, 0.0), width: float = 3.0, iters: int = 40) -> dict:
    """Newton's method for z^3 - 1 from every point of an n x n grid: which root each converges to, and in how many
    steps.  The basins' boundaries are fractal: near any boundary point all three basins meet."""
    xs = np.linspace(center[0] - width / 2, center[0] + width / 2, n)
    ys = np.linspace(center[1] - width / 2, center[1] + width / 2, n)
    Z = xs[None, :] + 1j * ys[:, None]
    roots = np.array([1, np.exp(2j * np.pi / 3), np.exp(-2j * np.pi / 3)])
    steps = np.full(Z.shape, iters, dtype=np.int16)
    done = np.zeros(Z.shape, bool)
    for k in range(iters):
        with np.errstate(all="ignore"):
            Z = Z - (Z ** 3 - 1) / (3 * Z ** 2)
        close = np.min(np.abs(Z[..., None] - roots), axis=-1) < 1e-6
        new = close & ~done
        steps[new] = k
        done |= close
    which = np.argmin(np.abs(Z[..., None] - roots), axis=-1).astype(np.int8)
    which[~done] = -1
    return {"which": which, "steps": steps, "center": list(center), "width": width,
            "unconverged": float((~done).mean())}


# ---------------------------------------------------------------- interpolation

def runge(f=lambda x: 1 / (1 + 25 * x * x), ns=(5, 10, 15, 20, 30, 40, 60, 80)) -> dict:
    """Max error of polynomial interpolation of Runge's function on [-1, 1] at equispaced points (it diverges) and at
    Chebyshev points (it converges geometrically), evaluated by the barycentric formula."""
    xx = np.linspace(-1, 1, 2001)
    rows = []
    curves = {}
    for n in ns:
        xe = np.linspace(-1, 1, n + 1)
        xc = np.cos(np.pi * np.arange(n + 1) / n)
        pe = bary(xe, f(xe), xx)
        pc = bary(xc, f(xc), xx)
        rows.append({"n": n, "equispaced": float(np.max(np.abs(pe - f(xx)))),
                     "chebyshev": float(np.max(np.abs(pc - f(xx))))})
        if n in (10, 20):
            curves[str(n)] = {"x": xx[::20].tolist(), "equi": np.clip(pe[::20], -3, 3).tolist(),
                              "cheb": pc[::20].tolist(), "nodes_e": xe.tolist(), "nodes_c": xc.tolist()}
    return {"rows": rows, "curves": curves, "f": [float(v) for v in f(xx[::20])]}


def bary(xs, fs, x):
    """Barycentric interpolation (second form) with weights w_j = 1 / prod (x_j - x_k)."""
    xs = np.asarray(xs, float)
    n = len(xs)
    w = np.ones(n)
    for j in range(n):
        d = xs[j] - np.delete(xs, j)
        w[j] = 1.0 / np.prod(d * 2)              # scaled to avoid overflow; the scale cancels
    diff = x[:, None] - xs[None, :]
    exact = np.isclose(diff, 0.0, atol=1e-15)
    diff[exact] = 1.0
    t = w / diff
    p = (t @ np.asarray(fs, float)) / t.sum(axis=1)
    hit = exact.any(axis=1)
    if hit.any():
        p[hit] = np.asarray(fs, float)[np.argmax(exact[hit], axis=1)]
    return p


# ---------------------------------------------------------------- quadrature

def quadrature(f=lambda x: np.exp(x) * np.cos(3 * x), a: float = 0.0, b: float = 2.0, ns=(2, 4, 8, 16, 32, 64),
               seed: int = 0) -> dict:
    exact = (np.exp(2) * (np.cos(6) + 3 * np.sin(6)) - 1) / 10
    rng = np.random.default_rng(seed)
    rows = []
    for n in ns:
        x = np.linspace(a, b, n + 1)
        y = f(x)
        trap = (b - a) / n * (y.sum() - (y[0] + y[-1]) / 2)
        simp = (b - a) / (3 * n) * (y[0] + y[-1] + 4 * y[1:-1:2].sum() + 2 * y[2:-1:2].sum()) if n % 2 == 0 else None
        g, w = np.polynomial.legendre.leggauss(n)
        gauss = (b - a) / 2 * (w @ f((b - a) / 2 * g + (a + b) / 2))
        mc = [(b - a) * f(rng.uniform(a, b, n + 1)).mean() for _ in range(200)]
        rows.append({"n": n, "trapezoid": abs(trap - exact), "simpson": None if simp is None else abs(simp - exact),
                     "gauss": abs(gauss - exact), "monte_carlo": float(np.sqrt(np.mean((np.array(mc) - exact) ** 2)))})
    calls = [0]

    def g_(x):
        calls[0] += 1
        return float(f(np.array(x)))

    val = adaptive_simpson(g_, a, b, 1e-10)
    return {"exact": float(exact), "rows": rows, "adaptive": {"error": abs(val - exact), "calls": calls[0]}}


def adaptive_simpson(f, a, b, tol):
    def s(a, b, fa, fm, fb):
        return (b - a) / 6 * (fa + 4 * fm + fb)

    def rec(a, b, fa, fm, fb, whole, tol, depth):
        m = (a + b) / 2
        lm, rm = (a + m) / 2, (m + b) / 2
        flm, frm = f(lm), f(rm)
        left, right = s(a, m, fa, flm, fm), s(m, b, fm, frm, fb)
        if depth > 50 or abs(left + right - whole) <= 15 * tol:
            return left + right + (left + right - whole) / 15
        return rec(a, m, fa, flm, fm, left, tol / 2, depth + 1) + rec(m, b, fm, frm, fb, right, tol / 2, depth + 1)

    fa, fb, fm = f(a), f(b), f((a + b) / 2)
    return rec(a, b, fa, fm, fb, s(a, b, fa, fm, fb), tol, 0)


# ---------------------------------------------------------------- ODEs

def rk45(f, t0, y0, t1, tol=1e-6, h=0.01, max_steps=1_000_000):
    """Dormand-Prince 5(4) with step-size control; returns times, states and the number of rejected steps."""
    c = [0, 1 / 5, 3 / 10, 4 / 5, 8 / 9, 1, 1]
    A = [[], [1 / 5], [3 / 40, 9 / 40], [44 / 45, -56 / 15, 32 / 9],
         [19372 / 6561, -25360 / 2187, 64448 / 6561, -212 / 729],
         [9017 / 3168, -355 / 33, 46732 / 5247, 49 / 176, -5103 / 18656],
         [35 / 384, 0, 500 / 1113, 125 / 192, -2187 / 6784, 11 / 84]]
    b5 = np.array([35 / 384, 0, 500 / 1113, 125 / 192, -2187 / 6784, 11 / 84, 0])
    b4 = np.array([5179 / 57600, 0, 7571 / 16695, 393 / 640, -92097 / 339200, 187 / 2100, 1 / 40])
    t, y = t0, np.array(y0, float)
    ts, ys, rej = [t], [y.copy()], 0
    steps = 0
    while t < t1 and steps < max_steps:
        h = min(h, t1 - t)
        k = []
        for i in range(7):
            yi = y + h * sum(A[i][j] * k[j] for j in range(i)) if i else y
            k.append(np.asarray(f(t + c[i] * h, yi), float))
        K = np.array(k)
        y5 = y + h * (b5 @ K)
        y4 = y + h * (b4 @ K)
        err = np.max(np.abs(y5 - y4) / (tol + tol * np.maximum(np.abs(y), np.abs(y5))))
        steps += 1
        if err <= 1:
            t, y = t + h, y5
            ts.append(t)
            ys.append(y.copy())
        else:
            rej += 1
        h *= min(5.0, max(0.2, 0.9 * err ** (-1 / 5) if err > 0 else 5.0))
    return np.array(ts), np.array(ys), rej


def stiffness(lams=(-1.0, -100.0, -10000.0), t1: float = 2.0) -> list[dict]:
    """y' = lam (y - cos t) - sin t, y(0) = 0, whose solution is cos t - e^(lam t): cos t once the transient dies.
    The explicit RK45 needs ever
    more steps as lam grows (stability, not accuracy, sets its step); backward Euler takes the same 200 steps for
    every lam, because its stability region contains the whole left half-plane (A-stability)."""
    rows = []
    for lam in lams:
        f = lambda t, y: lam * (y - np.cos(t)) - np.sin(t)  # noqa: E731
        ts, ys, rej = rk45(f, 0.0, [0.0], t1, tol=1e-6)
        h = t1 / 200
        y = 0.0
        for k in range(200):
            t = (k + 1) * h
            y = (y + h * (-lam * np.cos(t) - np.sin(t))) / (1 - h * lam)
        exact = np.cos(t1) - np.exp(lam * t1)
        rows.append({"lam": lam, "rk45_steps": len(ts) - 1, "rk45_rejected": rej,
                     "rk45_error": float(abs(ys[-1][0] - exact)), "backward_euler_steps": 200,
                     "backward_euler_error": float(abs(y - exact))})
    return rows


def stability_regions(n: int = 161, span: float = 4.0) -> dict:
    """|R(z)| <= 1 on a grid of the complex plane for explicit Euler (1 + z), RK4 (its Taylor polynomial) and
    backward Euler (1 / (1 - z))."""
    x = np.linspace(-span, span / 2, n)
    y = np.linspace(-span * 0.75, span * 0.75, n)
    Z = x[None, :] + 1j * y[:, None]
    R = {"euler": np.abs(1 + Z) <= 1, "rk4": np.abs(1 + Z + Z ** 2 / 2 + Z ** 3 / 6 + Z ** 4 / 24) <= 1,
         "backward_euler": np.abs(1 / (1 - Z)) <= 1}
    return {"x": x.tolist(), "y": y.tolist(), **{k: v.astype(np.uint8) for k, v in R.items()}}


def kepler(orbits: int = 1000, steps_per_orbit: int = 100, e: float = 0.5) -> dict:
    """A Kepler orbit (GM = 1, period 2 pi) integrated with RK4 and with leapfrog (velocity Verlet) at the same step:
    RK4's energy drifts steadily; leapfrog's oscillates but stays bounded, because it is symplectic."""
    q0 = np.array([1 - e, 0.0])
    p0 = np.array([0.0, math.sqrt((1 + e) / (1 - e))])
    h = 2 * math.pi / steps_per_orbit

    def acc(q):
        return -q / np.linalg.norm(q) ** 3

    def energy(q, p):
        return 0.5 * p @ p - 1 / np.linalg.norm(q)

    E0 = energy(q0, p0)
    out = {}
    for method in ("rk4", "leapfrog"):
        q, p = q0.copy(), p0.copy()
        drift, path = [], []
        a = acc(q)
        for k in range(orbits * steps_per_orbit):
            if method == "rk4":
                def F(s):
                    return np.concatenate([s[2:], acc(s[:2])])
                s = np.concatenate([q, p])
                k1 = F(s)
                k2 = F(s + h / 2 * k1)
                k3 = F(s + h / 2 * k2)
                k4 = F(s + h * k3)
                s = s + h / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
                q, p = s[:2], s[2:]
            else:
                p_half = p + h / 2 * a
                q = q + h * p_half
                a = acc(q)
                p = p_half + h / 2 * a
            if (k + 1) % steps_per_orbit == 0:
                drift.append(float((energy(q, p) - E0) / abs(E0)))
            if k >= (orbits - 3) * steps_per_orbit and k % 2 == 0:
                path.append(q.tolist())
        out[method] = {"energy_drift": drift, "last_orbits": path}
    return {"orbits": orbits, "steps_per_orbit": steps_per_orbit, "e": e, **out}
