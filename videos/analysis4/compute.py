"""Precompute everything numerical in Part 4 of the analysis series ("Calculus in Many Dimensions").

    python -m videos.analysis4.compute            # everything missing (seconds)
    python -m videos.analysis4.compute picard     # specific items
    python -m videos.analysis4.compute --force    # recompute

Results are cached in ``.cache/analysis4/<name>.npz``; scenes call ``load(name)``.  Every number the narration
quotes is computed here and asserted against the statement it illustrates.

Items:
    newton      Newton's method on F(x, y) = (x^2 + y^2 - 4, xy - 1): iterates, residuals squaring each step
    linmaps     the operator norm as the largest singular value (the unit circle's image is an ellipse); the
                Neumann series for an inverse, summed (Rudin 9.8)
    derivative  the derivative as a linear map: tangent-plane residuals |f(p + h) - f(p) - Ah| / |h| -> 0; the
                contour map zoomed until its level lines are parallel and evenly spaced
    museum      xy / (x^2 + y^2) (partials at 0, not continuous) and x^2 y / (x^2 + y^2) (directional derivatives in
                every direction, not linear in the direction: not differentiable)
    contraction cos x = x by iteration, errors under c^n / (1 - c) |x1 - x0|; Newton near a simple root
    picard      Picard iterates for y' = y and y' = x + sin y, sup distances shrinking geometrically
    inverse     the inverse function theorem's contraction phi(x) = x + A^-1 (y - f(x)) for f = (e^x cos y, e^x sin y)
    implicit    the folium x^3 + y^3 = 3xy traced by continuation; its fold where f_y = 0
    mixed       f = xy(x^2 - y^2)/(x^2 + y^2): f_xy(0, 0) = -1, f_yx(0, 0) = 1; differentiation under the integral
    forms       area factors of a map on a grid against |det J|
"""

from __future__ import annotations

import argparse
import math
import time

import numpy as np

from explainer.tts import REPO_ROOT

DATA_DIR = REPO_ROOT / ".cache" / "analysis4"


def trap(y, x):
    y, x = np.asarray(y, float), np.asarray(x, float)
    return float(np.sum((y[1:] + y[:-1]) * np.diff(x)) / 2)


def cumtrap(y, x):
    out = np.zeros_like(x)
    out[1:] = np.cumsum((y[1:] + y[:-1]) * np.diff(x) / 2)
    return out


# ---------------------------------------------------------------------------
# Newton's method in two variables (the hook)
# ---------------------------------------------------------------------------
def F_newton(p):
    x, y = p
    return np.array([x * x + y * y - 4, x * y - 1])


def J_newton(p):
    x, y = p
    return np.array([[2 * x, 2 * y], [y, x]])


def compute_newton():
    p = np.array([2.5, 1.0])
    its, res = [p.copy()], [np.linalg.norm(F_newton(p))]
    for _ in range(7):
        p = p - np.linalg.solve(J_newton(p), F_newton(p))
        its.append(p.copy())
        res.append(np.linalg.norm(F_newton(p)))
    its, res = np.array(its), np.array(res)
    root = its[-1]
    x2 = 2 + math.sqrt(3)  # x^2 + 1/x^2 = 4
    assert abs(root[0] ** 2 - x2) < 1e-12 or abs(root[0] ** 2 - (2 - math.sqrt(3))) < 1e-12
    # quadratic convergence: res_{k+1} <= C res_k^2 (the number of correct digits doubles)
    ratios = res[1:5] / res[0:4] ** 2
    assert np.all(ratios < 0.1) and res[4] < 1e-10
    errs = np.linalg.norm(its - root, axis=1)
    return dict(its=its, res=res, root=root, errs=errs)


# ---------------------------------------------------------------------------
# Linear maps
# ---------------------------------------------------------------------------
def compute_linmaps():
    A = np.array([[1.6, 0.9], [0.3, 1.1]])
    th = np.linspace(0, 2 * np.pi, 3601)
    U = np.c_[np.cos(th), np.sin(th)]
    img = U @ A.T
    s = np.linalg.svd(A, compute_uv=False)
    assert abs(np.linalg.norm(img, axis=1).max() - s[0]) < 1e-5 and abs(np.linalg.norm(img, axis=1).min() - s[1]) < 1e-5
    # 9.8: if ||B - A|| ||A^-1|| < 1 then B is invertible: B^-1 = sum_k (A^-1 (A - B))^k A^-1
    Ainv = np.linalg.inv(A)
    E = np.array([[0.15, -0.2], [0.1, 0.12]])
    B = A + E
    q = np.linalg.norm(Ainv @ (A - B), 2)
    assert np.linalg.norm(E, 2) * np.linalg.norm(Ainv, 2) < 1 and q < 1
    S, term, errs = np.zeros((2, 2)), Ainv.copy(), []
    Binv = np.linalg.inv(B)
    for k in range(12):
        S = S + term
        errs.append(np.linalg.norm(S - Binv, 2))
        term = Ainv @ (A - B) @ term
    errs = np.array(errs)
    assert np.all(np.diff(errs) < 0) and errs[-1] < 1e-6
    safe = 1 / np.linalg.norm(Ainv, 2)  # the radius of the ball of invertible maps around A
    return dict(A=A, th=th, img=img, s=s, B=B, E=E, errs=errs, safe=safe, q=q)


# ---------------------------------------------------------------------------
# The derivative as a linear map
# ---------------------------------------------------------------------------
def f_surf(x, y):
    return np.sin(x) * np.cos(y) + 0.3 * x * y


def grad_surf(x, y):
    return np.array([np.cos(x) * np.cos(y) + 0.3 * y, -np.sin(x) * np.sin(y) + 0.3 * x])


def compute_derivative():
    p = np.array([0.6, 0.4])
    A = grad_surf(*p)
    rng = np.random.default_rng(4)
    hs = np.array([1.0, 0.3, 0.1, 0.03, 0.01, 0.003, 0.001])
    worst = []
    for r in hs:
        dirs = rng.normal(size=(200, 2))
        dirs /= np.linalg.norm(dirs, axis=1)[:, None]
        h = r * dirs
        resid = np.abs(f_surf(p[0] + h[:, 0], p[1] + h[:, 1]) - f_surf(*p) - h @ A) / r
        worst.append(resid.max())
    worst = np.array(worst)
    assert np.all(np.diff(worst) < 0) and worst[-1] < 2e-3
    return dict(p=p, A=A, hs=hs, worst=worst)


# ---------------------------------------------------------------------------
# The museum: partial derivatives are not enough
# ---------------------------------------------------------------------------
def compute_museum():
    th = np.linspace(0, 2 * np.pi, 721)
    # g = x^2 y / (x^2 + y^2): D_u g(0) = cos^2 t sin t, while grad g(0) = (0, 0) predicts 0
    Du = np.cos(th) ** 2 * np.sin(th)
    for t, dv in zip(th[::40], Du[::40]):
        h = 1e-7
        x, y = h * math.cos(t), h * math.sin(t)
        g = x * x * y / (x * x + y * y)
        assert abs(g / h - dv) < 1e-9
    # f = xy / (x^2 + y^2): f(t, t) = 1/2 for every t != 0, f(0, 0) = 0, partials at 0 both 0
    assert all(abs(t * t / (2 * t * t) - 0.5) < 1e-15 for t in (1e-3, 1e-6, 1e-9))
    return dict(th=th, Du=Du)


# ---------------------------------------------------------------------------
# The contraction principle
# ---------------------------------------------------------------------------
def compute_contraction():
    c = math.sin(1.0)  # |cos'| <= sin 1 on [0, 1]
    x = [0.0]
    for _ in range(30):
        x.append(math.cos(x[-1]))
    x = np.array(x)
    fix = x[-1]
    for _ in range(200):
        fix = math.cos(fix)
    errs = np.abs(x - fix)
    bound = c ** np.arange(len(x)) / (1 - c) * abs(x[1] - x[0])
    assert np.all(errs <= bound + 1e-15) and abs(math.cos(fix) - fix) < 1e-15
    # Newton for x^2 = 2 from x0 = 1: g(x) = x - (x^2 - 2)/(2x) = x/2 + 1/x, |g'| <= 1/2 on [1, 2]
    xn = [1.0]
    for _ in range(5):
        xn.append(xn[-1] / 2 + 1 / xn[-1])
    xn = np.array(xn)
    nerr = np.abs(xn - math.sqrt(2))
    assert nerr[4] < 1e-11
    return dict(c=c, x=x, fix=fix, errs=errs, bound=bound, xn=xn, nerr=nerr)


# ---------------------------------------------------------------------------
# Picard iteration
# ---------------------------------------------------------------------------
def compute_picard():
    h = 1.0
    t = np.linspace(0, h, 2001)
    # y' = y, y(0) = 1: the iterates are the Taylor polynomials of e^t
    Y = [np.zeros_like(t)]
    for _ in range(9):
        Y.append(1 + cumtrap(Y[-1], t))
    Y = np.array(Y)
    exact = np.exp(t)
    err1 = np.abs(Y - exact).max(axis=1)
    for k in range(1, 8):
        taylor = sum(t**j / math.factorial(j) for j in range(k))
        assert np.abs(Y[k] - taylor).max() < 1e-6
    assert np.all(np.diff(err1) < 0)
    # y' = x + sin y, y(0) = 0.5 on [0, 1]: Lipschitz constant L = 1; on C[0, h] T is a contraction for h < 1 in the
    # sup norm, and on [0, 1] the k-th step is at most h^k / k! times the first (the usual Picard estimate)
    Z = [np.full_like(t, 0.5)]
    for _ in range(12):
        Z.append(0.5 + cumtrap(t + np.sin(Z[-1]), t))
    Z = np.array(Z)
    steps = np.abs(np.diff(Z, axis=0)).max(axis=1)
    fact = np.array([steps[0] * h**k / math.factorial(k) for k in range(len(steps))])
    assert np.all(steps <= fact + 1e-9)
    # a fine RK4 reference
    n = 20000
    tt = np.linspace(0, h, n + 1)
    yy = np.empty(n + 1)
    yy[0] = 0.5
    dt = tt[1] - tt[0]
    fz = lambda a, b: a + math.sin(b)  # noqa: E731
    for i in range(n):
        a, b = tt[i], yy[i]
        k1 = fz(a, b)
        k2 = fz(a + dt / 2, b + dt / 2 * k1)
        k3 = fz(a + dt / 2, b + dt / 2 * k2)
        k4 = fz(a + dt, b + dt * k3)
        yy[i + 1] = b + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
    ref = np.interp(t, tt, yy)
    err2 = np.abs(Z - ref).max(axis=1)
    assert err2[-1] < 1e-6
    # camera coordinates: the values at t = 0.5 and t = 1
    i5 = 1000
    assert abs(t[i5] - 0.5) < 1e-12
    cam1 = np.c_[Y[:, i5], Y[:, -1]]
    cam2 = np.c_[Z[:, i5], Z[:, -1]]
    return dict(t=t, Y=Y, err1=err1, Z=Z, steps=steps, fact=fact, ref=ref, err2=err2, cam1=cam1, cam2=cam2)


# ---------------------------------------------------------------------------
# The inverse function theorem
# ---------------------------------------------------------------------------
def f_exp(p):
    x, y = p
    return np.array([math.exp(x) * math.cos(y), math.exp(x) * math.sin(y)])


def J_exp(p):
    x, y = p
    e = math.exp(x)
    return np.array([[e * math.cos(y), -e * math.sin(y)], [e * math.sin(y), e * math.cos(y)]])


def compute_inverse():
    a = np.array([0.0, 0.6])
    A = J_exp(a)
    Ainv = np.linalg.inv(A)
    target = f_exp(a) + np.array([0.25, -0.18])
    x = a.copy()
    its, res = [x.copy()], [np.linalg.norm(f_exp(x) - target)]
    for _ in range(25):
        x = x + Ainv @ (target - f_exp(x))
        its.append(x.copy())
        res.append(np.linalg.norm(f_exp(x) - target))
    its, res = np.array(its), np.array(res)
    assert res[-1] < 1e-12 and np.all(np.diff(res[:15]) < 0)
    # phi is a contraction near a: ||phi'(x)|| = ||I - A^-1 f'(x)|| < 1/2 on the closed ball |x - a| <= r, which
    # holds every iterate. As complex numbers A^-1 f'(x) = e^(x - a), so the norm is |1 - e^w|, |w| <= r: largest at
    # w = r (on the circle, by the maximum principle), e^r - 1. Sample the disk and its edge.
    r = 0.35
    rng = np.random.default_rng(9)
    rad, ang = r * np.sqrt(rng.uniform(0, 1, 600)), rng.uniform(0, 2 * math.pi, 600)
    edge = np.linspace(0, 2 * math.pi, 720, endpoint=False)
    pts = a + np.column_stack([np.r_[rad * np.cos(ang), r * np.cos(edge)], np.r_[rad * np.sin(ang), r * np.sin(edge)]])
    lips = np.array([np.linalg.norm(np.eye(2) - Ainv @ J_exp(p), 2) for p in pts])
    assert lips.max() < 0.5 and abs(lips.max() - (math.exp(r) - 1)) < 1e-4
    assert np.all(np.linalg.norm(its - a, axis=1) < r)
    return dict(a=a, A=A, target=target, its=its, res=res, r=r, lip=lips.max())


# ---------------------------------------------------------------------------
# The implicit function theorem: the folium of Descartes
# ---------------------------------------------------------------------------
def compute_implicit():
    f = lambda x, y: x**3 + y**3 - 3 * x * y  # noqa: E731
    fx = lambda x, y: 3 * x * x - 3 * y  # noqa: E731
    fy = lambda x, y: 3 * y * y - 3 * x  # noqa: E731
    # trace the loop by pseudo-arclength continuation from (3/2, 3/2), both ways, down to the origin
    def trace(direction):
        p = np.array([1.5, 1.5])
        tan = np.array(direction, float) / math.sqrt(2)
        out = [p.copy()]
        ds = 0.02
        for _ in range(400):
            q = p + ds * tan
            for _ in range(20):  # Newton on f = 0 along the gradient
                g = np.array([fx(*q), fy(*q)])
                q = q - f(*q) * g / (g @ g)
            new_tan = np.array([-fy(*q), fx(*q)])
            new_tan /= np.linalg.norm(new_tan)
            if new_tan @ tan < 0:
                new_tan = -new_tan
            tan, p = new_tan, q
            out.append(p.copy())
            if np.linalg.norm(p) < 0.04:
                break
        return np.array(out)

    a_, b_ = trace((1, -1)), trace((-1, 1))
    pts = np.concatenate([a_[::-1], b_[1:]])
    assert np.abs(f(pts[:, 0], pts[:, 1])).max() < 1e-10
    fold = np.array([2 ** (2 / 3), 2 ** (1 / 3)])  # f_y = 0 on the curve: y^2 = x, y^3 = 2
    assert abs(f(*fold)) < 1e-12 and abs(fy(*fold)) < 1e-12 and abs(fx(*fold)) > 1
    fold2 = fold[::-1]  # f_x = 0 there (the curve is symmetric)
    # the implicit derivative y' = -f_x / f_y along the upper branch near (1.5, 1.5): equals the curve's slope
    q = np.array([1.5, 1.5])
    slope = -fx(*q) / fy(*q)
    assert abs(slope + 1) < 1e-12
    return dict(pts=pts, fold=fold, fold2=fold2)


# ---------------------------------------------------------------------------
# Mixed partials, and differentiation under the integral sign
# ---------------------------------------------------------------------------
def compute_mixed():
    import sympy as sp
    x, y, h, k = sp.symbols("x y h k", real=True)
    f = x * y * (x**2 - y**2) / (x**2 + y**2)
    fx_0y = sp.limit((f.subs({x: h}) - 0) / h, h, 0)  # f_x(0, y) = -y for y != 0 (f(0, y) = 0)
    fy_x0 = sp.limit((f.subs({y: k}) - 0) / k, k, 0)  # f_y(x, 0) = x
    fxy = sp.diff(fx_0y, y)
    fyx = sp.diff(fy_x0, x)
    assert sp.simplify(fx_0y + y) == 0 and sp.simplify(fy_x0 - x) == 0 and fxy == -1 and fyx == 1
    # the second difference on an h-by-k rectangle at 0: [f(h, k) - f(0, k) - f(h, 0) + f(0, 0)] / (hk) is
    # (h^2 - k^2)/(h^2 + k^2): -1 for a tall thin rectangle (h << k: f_xy), +1 for a flat one (k << h: f_yx)
    fn = sp.lambdify((x, y), f, "numpy")

    def F(a, b):
        return 0.0 if a == 0 and b == 0 else float(fn(a, b))

    ratios = np.geomspace(0.01, 100, 81)  # h / k
    kk = 1e-3
    q_xy = np.array([(F(r * kk, kk) - F(0, kk) - F(r * kk, 0) + F(0, 0)) / (r * kk * kk) for r in ratios])
    assert np.allclose(q_xy, (ratios**2 - 1) / (ratios**2 + 1), atol=1e-9)
    assert q_xy[0] < -0.999 and q_xy[-1] > 0.999 and abs(q_xy[40]) < 1e-9
    # Rudin 9.42: d/dt int_0^1 x^t dx = int_0^1 x^t log x dx = -1/(t + 1)^2
    xs = np.linspace(1e-9, 1, 400001)
    ts = np.array([0.5, 1.0, 2.0])
    lhs = np.array([(1 / (t + 1.0001) - 1 / (t + 0.9999)) / 0.0002 for t in ts])
    rhs = np.array([trap(xs**t * np.log(xs), xs) for t in ts])
    assert np.allclose(lhs, -1 / (ts + 1) ** 2, atol=1e-6) and np.allclose(rhs, lhs, atol=1e-5)
    return dict(fxy=-1.0, fyx=1.0, ratios=ratios, q_xy=q_xy, ts=ts, lhs=lhs, rhs=rhs)


# ---------------------------------------------------------------------------
# A tour of chapter 10: area factors
# ---------------------------------------------------------------------------
def compute_forms():
    def T(p):
        x, y = p[..., 0], p[..., 1]
        return np.stack([x + 0.25 * np.sin(2 * y), y + 0.2 * x * x], axis=-1)

    def detJ(x, y):
        return 1 * 1 - 0.5 * np.cos(2 * y) * 0.4 * x

    hgrid = 0.25
    cs = np.arange(-1.0, 1.0, hgrid)
    ratios = []
    for x0 in cs:
        for y0 in cs:
            sq = np.array([[x0, y0], [x0 + hgrid, y0], [x0 + hgrid, y0 + hgrid], [x0, y0 + hgrid]])
            # image polygon with many points per side
            side = [np.linspace(sq[i], sq[(i + 1) % 4], 50, endpoint=False) for i in range(4)]
            poly = T(np.concatenate(side))
            area = 0.5 * abs(np.dot(poly[:, 0], np.roll(poly[:, 1], -1)) - np.dot(poly[:, 1], np.roll(poly[:, 0], -1)))
            # average |det J| over the square
            g = np.linspace(0, 1, 41)
            X, Y = np.meshgrid(x0 + hgrid * g, y0 + hgrid * g)
            avg = np.trapezoid(np.trapezoid(np.abs(detJ(X, Y)), g, axis=1), g)
            ratios.append(area / (avg * hgrid * hgrid))
    ratios = np.array(ratios)
    assert np.abs(ratios - 1).max() < 1e-3
    # Green's theorem: the folium's loop has area (1/2) closed-integral (x dy - y dx) = 3/2
    t = np.linspace(0, 400, 2_000_001)  # t in [0, inf): the loop (3t/(1 + t^3), 3t^2/(1 + t^3)), closed at 0
    x, y = 3 * t / (1 + t**3), 3 * t**2 / (1 + t**3)
    area = 0.5 * float(np.sum(x[:-1] * np.diff(y) - y[:-1] * np.diff(x)))
    assert abs(area - 1.5) < 1e-3
    # the closed form w = (x dy - y dx)/(x^2 + y^2): 2 pi around the origin, 0 around a loop that misses it
    th = np.linspace(0, 2 * np.pi, 200001)

    def winding(cx, cy, r):
        X, Y = cx + r * np.cos(th), cy + r * np.sin(th)
        return float(np.sum((X[:-1] * np.diff(Y) - Y[:-1] * np.diff(X)) / (X[:-1] ** 2 + Y[:-1] ** 2)))

    w_around, w_off = winding(0.2, -0.1, 1.0), winding(1.6, 0.8, 0.6)
    assert abs(w_around - 2 * np.pi) < 1e-3 and abs(w_off) < 1e-3
    # a partition of unity on [0, 1]: smooth bumps divided by their sum
    xs = np.linspace(0, 1, 1201)
    cs = np.linspace(0, 1, 6)
    wdt = 0.32

    def bump(u):
        out = np.zeros_like(u)
        m = np.abs(u) < 1
        out[m] = np.exp(-1 / (1 - u[m] ** 2))
        return out

    B = np.array([bump((xs - c) / wdt) for c in cs])
    psi = B / B.sum(axis=0)
    assert B.sum(axis=0).min() > 0 and np.allclose(psi.sum(axis=0), 1)
    return dict(ratios=ratios, h=hgrid, area=area, w_around=w_around, w_off=w_off, xs=xs, psi=psi, cs=cs)


ITEMS = {
    "newton": compute_newton,
    "linmaps": compute_linmaps,
    "derivative": compute_derivative,
    "museum": compute_museum,
    "contraction": compute_contraction,
    "picard": compute_picard,
    "inverse": compute_inverse,
    "implicit": compute_implicit,
    "mixed": compute_mixed,
    "forms": compute_forms,
}

_loaded: dict[str, dict] = {}


def path(name: str):
    return DATA_DIR / f"{name}.npz"


def load(name: str) -> dict:
    if name not in _loaded:
        p = path(name)
        if not p.exists():
            DATA_DIR.mkdir(parents=True, exist_ok=True)
            np.savez_compressed(p, **ITEMS[name]())
        with np.load(p, allow_pickle=True) as z:
            _loaded[name] = {k: z[k] for k in z.files}
    return _loaded[name]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("names", nargs="*", default=list(ITEMS))
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    for name in args.names:
        if path(name).exists() and not args.force:
            print(f"  cached  {name}")
            continue
        t = time.time()
        print(f"  compute {name} ...", flush=True)
        out = ITEMS[name]()
        tmp = DATA_DIR / f"{name}.tmp.npz"
        np.savez_compressed(tmp, **out)
        tmp.replace(path(name))
        _loaded.pop(name, None)
        print(f"  done    {name} in {time.time() - t:.1f}s", flush=True)


if __name__ == "__main__":
    main()
