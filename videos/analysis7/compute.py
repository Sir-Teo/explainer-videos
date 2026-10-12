"""Precompute everything numerical in Part 7 of the analysis series ("Complex Analysis").

    python -m videos.analysis7.compute            # everything missing (about a minute)
    python -m videos.analysis7.compute riemann    # specific items
    python -m videos.analysis7.compute --force    # recompute

Results are cached in ``.cache/analysis7/<name>.npz``; scenes call ``load(name)``.  Every number the narration
quotes is computed here and asserted against the statement it illustrates.

Items:
    exp         e^z from its series: e^(2 pi i) = 1, pi/2 as the first zero of the cosine series, periodicity
    conformal   grids under z^2 and e^z: angles preserved, Jacobians are rotation-scalings; z + 0.4i conj(z) is not
    winding     a random closed curve and the winding numbers of 24 points, from the integral, asserted integers
    goursat     nested triangles: the remainder bound for e^z shrinks like 8^-n; for conj(z) the ratio is stuck
    cauchy      Cauchy's formula at random points; the Fibonacci numbers as contour integrals; roots by the
                argument principle
    maxmod      |z^2 + e^z| on the closed unit disk: the maximum is on the boundary
    residues    three real integrals by residues, against quadrature; Rouche for z^5 + 3z + 1
    schwarz     a self-map of the disk with f(0) = 0 obeys |f(z)| <= |z|; the three-lines theorem's log-convexity
    runge       polynomial approximation of 1/z: on a horseshoe the error goes to 0, on an annulus it never
                drops below 1
    montel      sin(nz) blows up on a disk; z^n -> 0 locally uniformly; a subsequence of a bounded family
    riemann     the Schwarz-Christoffel map of the disk onto an L-shaped hexagon: vertices to 1e-12, angles kept
    poisson     the Poisson integral of boundary data on the disk, asserted harmonic
    products    sin(pi z) against its Euler product; a Blaschke product's zeros
"""

from __future__ import annotations

import argparse
import math
import time

import numpy as np

from explainer.tts import REPO_ROOT

DATA_DIR = REPO_ROOT / ".cache" / "analysis7"


def trap(y, x):
    y, x = np.asarray(y), np.asarray(x, float)
    return np.sum((y[1:] + y[:-1]) * np.diff(x)) / 2


def contour(f, center=0.0, r=1.0, n=4096):
    """(1 / 2 pi i) * integral of f over the circle |z - center| = r, by the periodic trapezoid rule."""
    th = 2 * np.pi * np.arange(n) / n
    z = center + r * np.exp(1j * th)
    dz = 1j * r * np.exp(1j * th) * (2 * np.pi / n)
    return np.sum(f(z) * dz) / (2j * np.pi)


# ---------------------------------------------------------------------------
def compute_exp():
    def exp_series(z, N=80):
        s, term = np.zeros_like(z, dtype=complex), np.ones_like(z, dtype=complex)
        for k in range(N):
            s = s + term
            term = term * z / (k + 1)
        return s

    e2pi = exp_series(np.array([2j * math.pi]))[0]
    assert abs(e2pi - 1) < 1e-12

    def cos_series(t, N=40):
        s, term = 0.0, 1.0
        for k in range(N):
            s += term
            term *= -t * t / ((2 * k + 1) * (2 * k + 2))
        return s

    a, b = 1.0, 2.0  # cos 1 > 0 > cos 2, from the series
    assert cos_series(a) > 0 > cos_series(b)
    for _ in range(80):
        m = (a + b) / 2
        a, b = (m, b) if cos_series(m) > 0 else (a, m)
    half_pi = (a + b) / 2
    assert abs(half_pi - math.pi / 2) < 1e-14
    # periodicity on a grid
    X, Y = np.meshgrid(np.linspace(-2, 2, 21), np.linspace(-3, 3, 31))
    Z = X + 1j * Y
    assert np.allclose(exp_series(Z + 2j * math.pi), exp_series(Z), rtol=1e-11)
    partial = np.array([abs(exp_series(np.array([2j * math.pi]), N)[0] - 1) for N in (10, 20, 30, 40)])
    return dict(e2pi=e2pi, half_pi=half_pi, partial=partial)


def compute_conformal():
    out = {}
    pts = np.array([0.6 + 0.4j, 1.1 + 0.3j, 0.8 + 0.9j, 1.3 + 1.1j])
    h = 1e-6
    for name, f in (("sq", lambda z: z * z), ("exp", np.exp), ("bad", lambda z: z + 0.4j * np.conj(z))):
        angs, jacs = [], []
        for p in pts:
            du = (f(p + h) - f(p - h)) / (2 * h)  # image of the horizontal direction
            dv = (f(p + 1j * h) - f(p - 1j * h)) / (2 * h)  # image of the vertical direction
            angs.append(np.degrees(np.angle(dv / du)))
            jacs.append([[du.real, dv.real], [du.imag, dv.imag]])
        angs, jacs = np.array(angs), np.array(jacs)
        if name != "bad":
            assert np.allclose(angs, 90, atol=1e-6)
            # Cauchy-Riemann: the Jacobian is [[a, -b], [b, a]]
            assert np.allclose(jacs[:, 0, 0], jacs[:, 1, 1], atol=1e-6) and np.allclose(jacs[:, 0, 1], -jacs[:, 1, 0],
                                                                                         atol=1e-6)
        else:
            assert np.all(np.abs(angs - 90) > 5)
        out[f"ang_{name}"] = angs
        out[f"jac_{name}"] = jacs
    out["pts"] = pts
    return out


def compute_winding():
    rng = np.random.default_rng(3)
    t = np.linspace(0, 2 * np.pi, 4001)
    # a closed curve with an inner loop: three Fourier modes
    z = np.exp(1j * t) + 0.7 * np.exp(2j * t) + 0.25 * np.exp(-1j * t)
    dz = np.gradient(z, t)
    cand = rng.uniform(-2, 2, 600) + 1j * rng.uniform(-2, 2, 600)
    dist = np.min(np.abs(cand[:, None] - z[None, :]), axis=1)
    cand = cand[dist > 0.12]
    wc = np.array([trap(dz / (z - a), t) / (2j * np.pi) for a in cand])
    assert np.all(np.abs(wc.imag) < 1e-6) and np.all(np.abs(wc.real - np.round(wc.real)) < 1e-4)
    vals_all = np.round(wc.real).astype(int)
    assert set(vals_all.tolist()) == {0, 1, 2}
    pick = np.concatenate([np.where(vals_all == v)[0][:8] for v in (0, 1, 2)])
    pts, w = cand[pick], wc[pick]
    vals = vals_all[pick]
    return dict(z=z[::4], pts=pts, w=vals, raw=w.real)


def compute_goursat():
    z0 = 0.37 + 0.29j
    tri = np.array([0.0 + 0.0j, 1.0 + 0.0j, 0.35 + 0.9j])

    def inside(T, p):
        a, b, c = T

        def cr(u, v):
            return u.real * v.imag - u.imag * v.real

        d1, d2, d3 = cr(b - a, p - a), cr(c - b, p - b), cr(a - c, p - c)
        return (d1 >= 0 and d2 >= 0 and d3 >= 0) or (d1 <= 0 and d2 <= 0 and d3 <= 0)

    def edge_integral(f, T, n=400):
        tot = 0
        for a, b in ((T[0], T[1]), (T[1], T[2]), (T[2], T[0])):
            s = np.linspace(0, 1, n)
            zz = a + (b - a) * s
            tot += trap(f(zz), s) * (b - a)
        return tot

    assert inside(tri, z0)
    tris, eps, ratio_bad, ints_bad = [tri], [], [], []
    T = tri
    d0 = max(abs(T[0] - T[1]), abs(T[1] - T[2]), abs(T[2] - T[0]))
    p0 = abs(T[0] - T[1]) + abs(T[1] - T[2]) + abs(T[2] - T[0])
    for n in range(8):
        d = max(abs(T[0] - T[1]), abs(T[1] - T[2]), abs(T[2] - T[0]))
        p = abs(T[0] - T[1]) + abs(T[1] - T[2]) + abs(T[2] - T[0])
        assert abs(d - d0 / 2**n) < 1e-12 and abs(p - p0 / 2**n) < 1e-12
        # e^z: |f(z) - f(z0) - f'(z0)(z - z0)| <= eps_n |z - z0| on the triangle
        s = np.linspace(0, 1, 60)
        S, U = np.meshgrid(s, s)
        m = S + U <= 1
        zz = T[0] + S[m] * (T[1] - T[0]) + U[m] * (T[2] - T[0])
        with np.errstate(invalid="ignore", divide="ignore"):
            q = np.abs(np.exp(zz) - np.exp(z0) - np.exp(z0) * (zz - z0)) / np.abs(zz - z0)
        eps.append(np.nanmax(q[np.isfinite(q)]))
        ib = edge_integral(np.conj, T)
        area = abs(((T[1] - T[0]).conjugate() * (T[2] - T[0])).imag) / 2
        assert abs(abs(ib) - 2 * area) < 1e-6  # the integral of conj(z) around a triangle is 2i * area
        ints_bad.append(abs(ib))
        ratio_bad.append(abs(ib) / (d * p))
        mids = [(T[0] + T[1]) / 2, (T[1] + T[2]) / 2, (T[2] + T[0]) / 2]
        subs = [np.array([T[0], mids[0], mids[2]]), np.array([mids[0], T[1], mids[1]]),
                np.array([mids[2], mids[1], T[2]]), np.array([mids[0], mids[1], mids[2]])]
        T = [S_ for S_ in subs if inside(S_, z0)][0]
        tris.append(T)
    eps, ratio_bad = np.array(eps), np.array(ratio_bad)
    assert np.all(np.diff(eps) < 0) and eps[-1] < 0.01
    assert np.allclose(ratio_bad, ratio_bad[0], rtol=1e-6)
    # the integral of e^z around the big triangle is 0 (to quadrature accuracy)
    assert abs(edge_integral(np.exp, tri, 4000)) < 1e-6
    return dict(tris=np.array(tris), z0=z0, eps=eps, ratio_bad=ratio_bad, ints_bad=np.array(ints_bad), d0=d0, p0=p0)


def compute_cauchy():
    rng = np.random.default_rng(5)
    f = lambda z: np.exp(z) * np.cos(2 * z) + z**3  # noqa: E731
    a = 0.6 * np.sqrt(rng.uniform(0, 1, 30)) * np.exp(2j * np.pi * rng.uniform(0, 1, 30))
    vals = np.array([contour(lambda z: f(z) / (z - ak), 0, 1.0) for ak in a])
    err = np.abs(vals - f(a)).max()
    assert err < 1e-12
    # 1 / (1 - z - z^2) = sum F_(n+1) z^n: coefficients as contour integrals on |z| = 0.5
    fib = np.array([contour(lambda z: 1 / ((1 - z - z * z) * z ** (n + 1)), 0, 0.5).real for n in range(16)])
    F = [1, 1]
    while len(F) < 16:
        F.append(F[-1] + F[-2])
    assert np.allclose(fib, F, atol=1e-9)
    # argument principle: the roots of p inside |z| < r, counted by the winding of p(circle)
    p = np.poly1d([1, 0, -2, 0.3, 1.1, -0.4])
    dp = p.deriv()
    roots = np.roots(p.coeffs)
    rs = np.array([0.3, 0.6, 0.85, 1.05, 1.5])
    counts = np.array([contour(lambda z: dp(z) / p(z), 0, r, 8192).real for r in rs])
    assert np.allclose(counts, [np.sum(np.abs(roots) < r) for r in rs], atol=1e-6)
    return dict(a=a, err=err, fib=fib, roots=roots, rs=rs, counts=np.round(counts).astype(int))


def compute_maxmod():
    n = 401
    x = np.linspace(-1, 1, n)
    X, Y = np.meshgrid(x, x)
    Z = X + 1j * Y
    inside = np.abs(Z) < 1
    M = np.abs(Z**2 + np.exp(Z))
    th = np.linspace(0, 2 * np.pi, 20001)
    B = np.abs(np.exp(2j * th) + np.exp(np.exp(1j * th)))
    i = int(np.argmax(B))
    assert M[inside].max() < B.max()
    return dict(bmax=B.max(), th_max=th[i], imax=float(M[inside & (np.abs(Z) < 0.98)].max()))


def compute_residues():
    from scipy import integrate, special
    # 1. int_R dx / (1 + x^4): residues at e^(i pi/4), e^(3 i pi/4) are 1 / (4 z^3)
    poles = np.exp(1j * np.pi * np.array([0.25, 0.75]))
    res = 1 / (4 * poles**3)
    I1 = (2j * np.pi * res.sum()).real
    Q1 = integrate.quad(lambda x: 1 / (1 + x**4), -np.inf, np.inf)[0]
    assert abs(I1 - np.pi / np.sqrt(2)) < 1e-14 and abs(Q1 - I1) < 1e-9
    # the semicircle's contribution shrinks
    semis = []
    for R in (2.0, 5.0, 20.0):
        t = np.linspace(0, np.pi, 20001)
        z = R * np.exp(1j * t)
        semis.append(abs(trap(1j * z / (1 + z**4), t)))
    semis = np.array(semis)
    assert np.all(np.diff(semis) < 0)
    # 2. int_R sin x / x = pi (indented contour; e^(iz)/z has residue 1 at 0)
    I2 = np.pi
    Q2 = 2 * special.sici(1e8)[0]
    assert abs(Q2 - I2) < 1e-7
    # 3. int_R e^(-x^2) cos(2bx) dx = sqrt(pi) e^(-b^2) (shift the contour by ib: Cauchy's theorem on a rectangle)
    b = 0.7
    I3 = math.sqrt(math.pi) * math.exp(-b * b)
    Q3 = integrate.quad(lambda x: math.exp(-x * x) * math.cos(2 * b * x), -np.inf, np.inf)[0]
    assert abs(Q3 - I3) < 1e-9
    # Rouche: z^5 + 3z + 1 has exactly one root in |z| < 1 (|z^5 + 1| <= 2 < 3 = |3z| on |z| = 1)
    roots = np.roots([1, 0, 0, 0, 3, 1])
    inside = int(np.sum(np.abs(roots) < 1))
    assert inside == 1
    th = np.linspace(0, 2 * np.pi, 2001)
    z = np.exp(1j * th)
    assert np.all(np.abs(z**5 + 1) < np.abs(3 * z))
    return dict(poles=poles, res=res, I1=I1, Q1=Q1, semis=semis, I2=I2, Q2=Q2, b=b, I3=I3, Q3=Q3, roots=roots,
                inside=inside)


def compute_schwarz():
    a = 0.5
    f = lambda z: z * (z - a) / (1 - a * z)  # noqa: E731
    r = np.sqrt(np.random.default_rng(1).uniform(0, 1, 20000)) * 0.999
    th = np.random.default_rng(2).uniform(0, 2 * np.pi, 20000)
    z = r * np.exp(1j * th)
    assert np.all(np.abs(f(z)) <= np.abs(z) + 1e-12)
    d0 = abs((f(1e-7) - f(-1e-7)) / 2e-7)
    assert abs(d0 - a) < 1e-6
    # images of circles |z| = r stay inside |w| <= r
    rs = np.array([0.3, 0.6, 0.9])
    tt = np.linspace(0, 2 * np.pi, 721)
    imgs = np.array([f(rr * np.exp(1j * tt)) for rr in rs])
    assert np.all(np.abs(imgs) <= rs[:, None] + 1e-12)
    # three lines: f(z) = e^(2z) / (z + 1)^2 on 0 <= Re z <= 1: log M(x) is convex
    xs = np.linspace(0, 1, 101)
    ys = np.linspace(-40, 40, 8001)
    M = np.array([np.abs(np.exp(2 * (x + 1j * ys)) / (x + 1j * ys + 1) ** 2).max() for x in xs])
    logM = np.log(M)
    chord = (1 - xs) * logM[0] + xs * logM[-1]
    assert np.all(logM <= chord + 1e-12) and np.all(np.diff(logM, 2) > -1e-9)
    return dict(a=a, d0=d0, rs=rs, imgs=imgs, xs=xs, logM=logM)


def _arnoldi_fit(zk, fk, zeval, deg):
    """Least-squares polynomial fit of degree deg (Vandermonde with Arnoldi orthogonalization, stable)."""
    m = len(zk)
    Q = np.zeros((m, deg + 1), dtype=complex)
    H = np.zeros((deg + 1, deg), dtype=complex)
    Q[:, 0] = 1
    for k in range(deg):
        q = zk * Q[:, k]
        for j in range(k + 1):
            H[j, k] = np.vdot(Q[:, j], q) / m
            q = q - H[j, k] * Q[:, j]
        H[k + 1, k] = np.linalg.norm(q) / math.sqrt(m)
        Q[:, k + 1] = q / H[k + 1, k]
    c = np.linalg.lstsq(Q, fk, rcond=None)[0]
    W = np.zeros((len(zeval), deg + 1), dtype=complex)
    W[:, 0] = 1
    for k in range(deg):
        w = zeval * W[:, k]
        for j in range(k + 1):
            w = w - H[j, k] * W[:, j]
        W[:, k + 1] = w / H[k + 1, k]
    return W @ c


def compute_runge():
    # the horseshoe: the annulus 0.75 <= |z| <= 1 with the sector |arg z| < 1 removed (0 is reachable from outside)
    def boundary(gap):
        t1 = np.linspace(gap, 2 * np.pi - gap, 1500)
        outer = np.exp(1j * t1)
        inner = 0.75 * np.exp(1j * t1[::-1])
        cap1 = np.linspace(1, 0.75, 80) * np.exp(1j * (2 * np.pi - gap))
        cap2 = np.linspace(0.75, 1, 80) * np.exp(1j * gap)
        return np.concatenate([outer, cap1, inner, cap2]) if gap > 0 else np.concatenate([outer, inner])

    out = {}
    degs = np.array([4, 8, 16, 32, 64, 128])
    for name, gap in (("horse", 1.0), ("annulus", 0.0)):
        zb = boundary(gap)
        f = 1 / zb
        errs = []
        for deg in degs:
            p = _arnoldi_fit(zb, f, zb, int(deg))
            errs.append(np.abs(p - f).max())
        out[f"err_{name}"] = np.array(errs)
        out[f"bd_{name}"] = zb
    eh, ea = out["err_horse"], out["err_annulus"]
    assert eh[-1] < 1e-3 and np.all(np.diff(eh) < 0)
    assert np.all(ea >= 1 - 1e-6)  # on |z| = 1, the integral of 1/z - p is 2 pi i, so sup |1/z - p| >= 1
    # the best fit of degree 32 on the horseshoe, for drawing |1/z - p| along the boundary
    zb = out["bd_horse"]
    out["fit32"] = _arnoldi_fit(zb, 1 / zb, zb, 32)
    out["degs"] = degs
    return out


def compute_montel():
    ns = np.arange(1, 13)
    th = np.linspace(0, 2 * np.pi, 2001)
    z = 0.5 * np.exp(1j * th)
    sin_sup = np.array([np.abs(np.sin(n * z)).max() for n in ns])
    # on |z| = 1/2 the largest value of |sin nz| is at z = +-i/2: sinh(n/2)
    assert np.allclose(sin_sup, np.sinh(ns / 2), rtol=1e-3)
    assert np.all(np.diff(sin_sup) > 0) and sin_sup[-1] > 100
    # f_n(z) = (cos n z + sin n z^2)/2 + z^n / 2 is bounded by 1 on the disk; along n_k with n_k mod 2 pi -> 0
    # it converges to z/2 locally uniformly (not uniformly on the closed disk)
    nk = np.array([6, 44, 710, 103993])  # near multiples of 2 pi (continued fraction convergents of pi)
    errs_in, errs_out = [], []
    for n in nk:
        for r, lst in ((0.9, errs_in), (1.0, errs_out)):
            zz = r * np.exp(1j * th)
            fn = (math.cos(n) * zz + math.sin(n) * zz * zz) / 2 + zz ** int(n) / 2
            lst.append(np.abs(fn - zz / 2).max())
    errs_in, errs_out = np.array(errs_in), np.array(errs_out)
    assert np.all(np.diff(errs_in) < 0) and errs_in[-1] < 1e-3 and np.all(errs_out > 0.45)
    return dict(ns=ns, sin_sup=sin_sup, nk=nk, errs_in=errs_in, errs_out=errs_out)


def _sc_setup():
    from scipy.optimize import least_squares
    from scipy.special import roots_jacobi
    V = np.array([0, 2, 2 + 1j, 1 + 1j, 1 + 2j, 2j])
    n = len(V)
    alpha = np.array([(np.angle((V[k - 1] - V[k]) / (V[(k + 1) % n] - V[k])) % (2 * np.pi)) / np.pi
                      for k in range(n)])
    beta = alpha - 1
    assert abs(beta.sum() + 2) < 1e-12
    NG = 40

    def integral_to(k, zs):
        x, wts = roots_jacobi(NG, beta[k], 0.0)
        t = (x + 1) / 2
        w = t * zs[k]
        rest = np.ones_like(w, dtype=complex)
        for j in range(n):
            if j != k:
                rest = rest * (1 - w / zs[j]) ** beta[j]
        return zs[k] * np.sum(wts * rest) * 0.5 ** beta[k] * 0.5

    def zs_from(p):
        g = np.exp(p)
        g = g / g.sum() * 2 * np.pi
        th = np.concatenate([[0.0], np.cumsum(g[:-1])])
        return np.exp(1j * th)

    target = np.abs(np.diff(np.concatenate([V, V[:1]])))
    w0 = 0.8 + 0.8j  # the conformal center f(0) = w0, chosen near the reflex corner so the prevertices spread out

    def resid(p):
        zs = zs_from(p)
        F = np.array([integral_to(k, zs) for k in range(n)])
        sides = np.abs(np.diff(np.concatenate([F, F[:1]])))
        A = (V[1] - V[0]) / (F[1] - F[0])
        C = V[0] - A * F[0]
        r = list(sides[1:] / sides[0] - target[1:] / target[0])
        r += [(C - w0).real, (C - w0).imag]
        return np.array(r)

    sol = least_squares(resid, np.zeros(n), xtol=1e-15, ftol=1e-15, gtol=1e-15, max_nfev=2000)
    zs = zs_from(sol.x)
    F = np.array([integral_to(k, zs) for k in range(n)])
    A = (V[1] - V[0]) / (F[1] - F[0])
    C = V[0] - A * F[0]
    assert np.abs(A * F + C - V).max() < 1e-10 and abs(C - w0) < 1e-10
    return V, zs, beta, A, C


def compute_riemann():
    V, zs, beta, A, C = _sc_setup()

    def fprime(w):
        out = A * np.ones_like(w, dtype=complex)
        for zk, bk in zip(zs, beta):
            out = out * (1 - w / zk) ** bk
        return out

    xg, wg = np.polynomial.legendre.leggauss(60)

    def fmap(z):
        z = np.asarray(z, dtype=complex)
        t = (xg + 1) / 2
        W = z[..., None] * t
        return C + z * np.sum(wg / 2 * fprime(W), axis=-1)

    # images of circles and rays
    rs = np.array([0.2, 0.4, 0.6, 0.75, 0.85, 0.92, 0.96])
    th = np.linspace(0, 2 * np.pi, 721)
    circles = np.array([fmap(r * np.exp(1j * th)) for r in rs])
    angs = np.linspace(0, 2 * np.pi, 24, endpoint=False)
    rr = np.linspace(0, 0.985, 200)
    rays = np.array([fmap(rr * np.exp(1j * a)) for a in angs])
    # conformality: the images of the radial and angular directions stay perpendicular, with equal stretch
    rng = np.random.default_rng(9)
    zt = np.sqrt(rng.uniform(0, 0.9, 200)) * np.exp(2j * np.pi * rng.uniform(0, 1, 200))
    h = 1e-6
    dr = (fmap(zt * (1 + h)) - fmap(zt * (1 - h))) / (2 * h)
    dth = (fmap(zt * np.exp(1j * h)) - fmap(zt * np.exp(-1j * h))) / (2 * h)
    ang_err = np.abs(np.degrees(np.angle(dth / dr)) - 90).max()
    assert ang_err < 1e-4
    # the boundary circle goes onto the polygon: points of |z| = 0.9999 land within 0.01 of the edges
    tb = np.linspace(0, 2 * np.pi, 400, endpoint=False)
    wb = fmap(0.9999 * np.exp(1j * tb))

    def dist_to_poly(w):
        best = np.inf
        for a, b in zip(V, np.roll(V, -1)):
            s = np.clip(((w - a) * np.conj(b - a)).real / abs(b - a) ** 2, 0, 1)
            best = min(best, abs(w - (a + s * (b - a))))
        return best

    bd = max(dist_to_poly(w) for w in wb)
    assert bd < 0.02
    # f'(0) > 0 picks the map up to nothing: the conformal center and the derivative there
    return dict(V=V, zs=zs, rs=rs, circles=circles, angs=angs, rays=rays, ang_err=ang_err, bd=bd, C=C,
                d0=abs(fprime(np.array([0j]))[0]))


def compute_poisson():
    # boundary data g(theta) = a square wave in cos(3 theta) smoothed slightly; u = sum r^|n| g_n e^(i n theta)
    M = 1024
    th = 2 * np.pi * np.arange(M) / M
    g = np.tanh(4 * np.cos(3 * th)) + 0.4 * np.sin(th) + 0.3
    G = np.fft.fft(g) / M
    nfreq = np.fft.fftfreq(M, 1 / M)
    rs = np.linspace(0, 1, 121)
    U = np.array([np.real(np.fft.ifft(G * M * r ** np.abs(nfreq))) for r in rs])
    # Laplacian in polar coordinates by finite differences, at interior points
    dr = rs[1] - rs[0]
    dth = th[1] - th[0]
    lap = []
    for i in range(10, 110, 10):
        r = rs[i]
        u_rr = (U[i + 1] - 2 * U[i] + U[i - 1]) / dr**2
        u_r = (U[i + 1] - U[i - 1]) / (2 * dr)
        u_tt = (np.roll(U[i], -1) - 2 * U[i] + np.roll(U[i], 1)) / dth**2
        lap.append(np.abs(u_rr + u_r / r + u_tt / r**2).max() / np.abs(U[i]).max())
    lap = np.array(lap)
    assert np.all(lap < 5e-2)
    # pointwise, from the series itself: u(z) = sum_{n >= 0} G_n z^n + sum_{n < 0} G_n conj(z)^|n|, 5-point Laplacian

    def u_at(z):
        z = np.asarray(z, dtype=complex)
        out = np.zeros(z.shape)
        for gn, k in zip(G * M, nfreq):
            if abs(gn) < 1e-14:
                continue
            out = out + (gn * (z ** int(k) if k >= 0 else np.conj(z) ** int(-k))).real
        return out / M  # (G * M) / M = the Fourier coefficients of g

    rng = np.random.default_rng(6)
    zt = 0.8 * np.sqrt(rng.uniform(0, 1, 12)) * np.exp(2j * np.pi * rng.uniform(0, 1, 12))
    hh = 1e-3
    lap_pt = np.abs(u_at(zt + hh) + u_at(zt - hh) + u_at(zt + 1j * hh) + u_at(zt - 1j * hh) - 4 * u_at(zt)) / hh**2
    assert lap_pt.max() < 1e-4
    # the exact Laplacian of each mode r^n e^(in theta) is 0; check the spectral version too
    assert np.allclose(U[-1], g, atol=1e-8)
    assert abs(U[0].mean() - g.mean()) < 1e-12  # the mean value property: u(0) is the average of g
    return dict(th=th[::4], g=g[::4], rs=rs, U=U[:, ::4], lap=lap, lap_pt=lap_pt, u0=U[0, 0], gmean=g.mean())


def compute_products():
    x = np.linspace(-3.2, 3.2, 161)
    X, Y = np.meshgrid(x, np.linspace(-1.2, 1.2, 61))
    Z = X + 1j * Y
    S = np.sin(np.pi * Z)
    Ns = np.array([10, 100, 1000, 10000])
    errs = []
    P = np.pi * Z.copy()
    n = 1
    for N in Ns:
        while n <= N:
            P = P * (1 - Z * Z / (n * n))
            n += 1
        errs.append(np.abs(P - S).max() / np.abs(S).max())
    errs = np.array(errs)
    assert np.all(np.diff(np.log10(errs)) < -0.9)  # about one digit per factor 10
    # a Blaschke product with zeros a_k = (1 - 1/(k+1)^2) e^(i k): sum (1 - |a_k|) < infinity
    ks = np.arange(1, 41)
    ak = (1 - 1 / (ks + 1) ** 2) * np.exp(1j * ks)
    s = np.sum(1 - np.abs(ak))
    assert s < np.pi**2 / 6
    return dict(Ns=Ns, errs=errs, ak=ak, blaschke_sum=s)


ITEMS = {
    "exp": compute_exp,
    "conformal": compute_conformal,
    "winding": compute_winding,
    "goursat": compute_goursat,
    "cauchy": compute_cauchy,
    "maxmod": compute_maxmod,
    "residues": compute_residues,
    "schwarz": compute_schwarz,
    "runge": compute_runge,
    "montel": compute_montel,
    "riemann": compute_riemann,
    "poisson": compute_poisson,
    "products": compute_products,
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
