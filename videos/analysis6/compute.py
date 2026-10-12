"""Precompute everything numerical in Part 6 of the analysis series ("L^p, Hilbert Space and the Geometry of
Functions").

    python -m videos.analysis6.compute            # everything missing (seconds)
    python -m videos.analysis6.compute fejer      # specific items
    python -m videos.analysis6.compute --force    # recompute

Results are cached in ``.cache/analysis6/<name>.npz``; scenes call ``load(name)``.  Every number the narration
quotes is computed here and asserted against the statement it illustrates.

Items:
    ramps       continuous ramps converging in L^1 to a step (||ramp_n - step||_1 = 1/(4n)); no continuous limit
    jensen      Jensen's inequality for exp on 10^4 random weightings
    young       Young's inequality as two areas; Hoelder and Minkowski on random vectors
    parallel    the parallelogram law in L^p[0, 1] for p = 1, 2, 3: equality only at p = 2
    stacking    Riesz-Fischer's proof run on the ramps: a subsequence with summable increments
    projection  e^x projected onto span{1, x, x^2} in L^2[0, 1]: normal equations vs orthonormal basis
    rieszh      the representer of f -> int f w found from an orthonormal basis
    legendre    Gram-Schmidt on 1, x, ..., x^6 in L^2[-1, 1] gives the normalized Legendre polynomials
    fejer       the Fejer kernel; s_N and sigma_N for the sawtooth (no overshoot) and for a continuous f
    variation   total variation of sin(5x) dx on [0, 2 pi]; the Cantor measure on a null set
    radon       the density d lambda / dm recovered as a limit of ratios, and von Neumann's g = h / (1 + h)
    dual        the dual norm of l^p is the l^q norm, with the extremal vector
    lebdiff     averages over shrinking intervals at 1000 random points; the Vitali covering lemma
    cantorac    the Cantor function: derivative 0 off the Cantor set, total rise 1; its covers of length (2/3)^n
    holder      Hoelder's proof run on two normalized functions: |FG| under |F|^p/p + |G|^q/q (area exactly 1)
    lpnorms     ||2x||_p on [0, 1] rising to the essential sup; x^(-1/2) and 1/x near 0 and at infinity
    bessel      the sign function's Legendre coefficients: Bessel's partial sums filling up ||sign||^2 = 2
    trigdense   Rudin's kernel c_k ((1 + cos t)/2)^k: trigonometric polynomials converging uniformly (4.24)
    unbounded   |x|^(-1/4) on (-pi, pi): unbounded, not Riemann integrable, its Fourier series converges in L^2
    cpath       a complex measure as a closed path in C: mu(X) = 0, |mu|(X) = 2 pi (inscribed polygons)
    probe       a functional on C[0, 1] probed with narrowing bumps reveals its measure (density plus an atom)
    maximal     the maximal function of an indicator, and the weak-type estimate
    ftc         x^2 sin(1/x^2): differentiable everywhere, f' not integrable; sqrt(x): absolutely continuous
    polar       the Gaussian integral by polar coordinates: the Jacobian r, and int e^(-x^2) = sqrt(pi)
"""

from __future__ import annotations

import argparse
import math
import time

import numpy as np

from explainer.tts import REPO_ROOT

DATA_DIR = REPO_ROOT / ".cache" / "analysis6"


def trap(y, x):
    y, x = np.asarray(y, float), np.asarray(x, float)
    return float(np.sum((y[1:] + y[:-1]) * np.diff(x)) / 2)


def ramp(x, n):
    return np.clip(n * (x - 0.5) + 0.5, 0, 1)


# ---------------------------------------------------------------------------
def compute_ramps():
    x = np.linspace(0, 1, 200001)
    step = (x > 0.5).astype(float)
    ns = np.array([1, 2, 4, 8, 16, 32, 64])
    d1 = np.array([trap(np.abs(ramp(x, n) - step), x) for n in ns])
    assert np.allclose(d1, 1 / (4 * ns), rtol=1e-3)
    # any continuous g has sup |g - step| >= 1/2 (g(1/2) is within 1/2 of 0 or 1 only on one side)
    # camera: (int over [0, 1/2], int over [1/2, 1])
    left = np.array([trap(ramp(x, n)[x <= 0.5], x[x <= 0.5]) for n in ns])
    right = np.array([trap(ramp(x, n)[x >= 0.5], x[x >= 0.5]) for n in ns])
    assert np.allclose(left, 1 / (8 * ns), rtol=1e-3) and np.allclose(right, 0.5 - 1 / (8 * ns), rtol=1e-3)
    return dict(ns=ns, d1=d1, left=left, right=right)


def compute_jensen():
    rng = np.random.default_rng(0)
    worst = np.inf
    for _ in range(10000):
        k = rng.integers(2, 6)
        xs = rng.uniform(-2, 2, k)
        w = rng.dirichlet(np.ones(k))
        gap = np.sum(w * np.exp(xs)) - np.exp(np.sum(w * xs))
        worst = min(worst, gap)
    assert worst >= -1e-12
    # the picture: two points, weights sliding
    a, b = -1.2, 1.6
    ts = np.linspace(0, 1, 11)
    chord = (1 - ts) * np.exp(a) + ts * np.exp(b)
    curve = np.exp((1 - ts) * a + ts * b)
    assert np.all(chord >= curve - 1e-12)
    # AM-GM from Jensen with log: (abc)^(1/3) <= (a + b + c)/3
    v = rng.uniform(0.1, 5, (1000, 3))
    assert np.all(np.prod(v, axis=1) ** (1 / 3) <= v.mean(axis=1) + 1e-12)
    return dict(worst=worst, a=a, b=b)


def compute_young():
    rng = np.random.default_rng(1)
    ps = np.array([1.5, 2.0, 3.0])
    for p in ps:
        q = p / (p - 1)
        a, b = rng.uniform(0, 3, 10000), rng.uniform(0, 3, 10000)
        assert np.all(a * b <= a**p / p + b**q / q + 1e-12)
        x, y = rng.normal(size=(200, 6)), rng.normal(size=(200, 6))
        lhs = np.abs(x * y).sum(axis=1)
        rhs = (np.abs(x) ** p).sum(axis=1) ** (1 / p) * (np.abs(y) ** q).sum(axis=1) ** (1 / q)
        assert np.all(lhs <= rhs + 1e-12)
        mink = (np.abs(x + y) ** p).sum(axis=1) ** (1 / p) <= (np.abs(x) ** p).sum(axis=1) ** (1 / p) + \
            (np.abs(y) ** p).sum(axis=1) ** (1 / p) + 1e-12
        assert np.all(mink)
    # the picture for p = 3: areas under y = x^2 up to a, and under its inverse up to b
    p, a, b = 3.0, 1.2, 1.0
    q = p / (p - 1)
    A1, A2 = a**p / p, b**q / q
    assert A1 + A2 >= a * b
    return dict(p=p, a=a, b=b, A1=A1, A2=A2)


def compute_parallel():
    x = np.linspace(0, 1, 200001)
    f, g = x, 1 - x**2
    res = []
    for p in (1.0, 2.0, 3.0):
        def nrm(h):
            return trap(np.abs(h) ** p, x) ** (1 / p)
        lhs = nrm(f + g) ** 2 + nrm(f - g) ** 2
        rhs = 2 * nrm(f) ** 2 + 2 * nrm(g) ** 2
        res.append((p, lhs, rhs))
    res = np.array(res)
    assert abs(res[1, 1] - res[1, 2]) < 1e-8 and abs(res[0, 1] - res[0, 2]) > 1e-3 and abs(res[2, 1] - res[2, 2]) > 1e-3
    return dict(res=res)


def compute_stacking():
    x = np.linspace(0, 1, 200001)
    ks = np.arange(0, 8)
    nk = 2**ks
    inc = np.array([trap(np.abs(ramp(x, 2 * n) - ramp(x, n)), x) for n in nk])
    assert np.all(inc <= 0.5 ** (ks + 2) + 1e-6) and inc.sum() < 1
    # g = |f_1| + sum |f_{k+1} - f_k| has ||g||_1 <= ||f_1|| + sum ||increments|| < infinity
    return dict(nk=nk, inc=inc)


def compute_projection():
    from numpy.polynomial import legendre as L
    xg, wg = L.leggauss(60)
    x, w = (xg + 1) / 2, wg / 2  # Gauss-Legendre on [0, 1]
    f = np.exp(x)
    B = np.stack([np.ones_like(x), x, x * x])
    G = (B * w) @ B.T
    c_norm = np.linalg.solve(G, (B * w) @ f)
    # orthonormal basis (shifted Legendre) and the same projection
    Q = []
    for k in range(3):
        v = B[k].copy()
        for qv in Q:
            v -= np.sum(w * v * qv) * qv
        Q.append(v / math.sqrt(np.sum(w * v * v)))
    Q = np.array(Q)
    proj_on = sum(np.sum(w * f * qv) * qv for qv in Q)
    proj_ne = c_norm @ B
    assert np.allclose(proj_on, proj_ne, atol=1e-12)
    r = f - proj_ne
    assert np.allclose((B * w) @ r, 0, atol=1e-12)  # the error is orthogonal to the subspace
    err = math.sqrt(np.sum(w * r * r))
    taylor = 1 + x + x * x / 2
    terr = math.sqrt(np.sum(w * (f - taylor) ** 2))
    assert terr > err  # the projection is the nearest point; Taylor's polynomial is a different point of M
    sup_err = np.abs(r).max()
    xs = np.linspace(0, 1, 401)
    return dict(c=c_norm, err=err, terr=terr, sup_err=sup_err, xs=xs, fx=np.exp(xs),
                px=c_norm[0] + c_norm[1] * xs + c_norm[2] * xs**2, tx=1 + xs + xs**2 / 2,
                ip=(B * w) @ r)


def compute_rieszh():
    from numpy.polynomial import legendre as L
    xg, wg = L.leggauss(200)
    wfun = np.sin(3 * xg) + xg  # Lambda f = int_{-1}^{1} f w
    coef = []
    recon = np.zeros_like(xg)
    xs = np.linspace(-1, 1, 401)
    rec_xs = np.zeros_like(xs)
    keep, errs = [], []
    for n in range(30):
        Pn = L.legval(xg, [0] * n + [1]) * math.sqrt((2 * n + 1) / 2)
        lam = np.sum(wg * Pn * wfun)  # Lambda(e_n)
        coef.append(lam)
        recon += lam * Pn
        rec_xs = rec_xs + lam * L.legval(xs, [0] * n + [1]) * math.sqrt((2 * n + 1) / 2)
        if n + 1 in (2, 4, 6, 10):
            keep.append(rec_xs.copy())
            errs.append(np.abs(rec_xs - (np.sin(3 * xs) + xs)).max())
    coef = np.array(coef)
    assert np.allclose(recon, wfun, atol=1e-10)
    errs = np.array(errs)
    assert np.all(np.diff(errs) < 0)
    # the norm of the functional is the norm of its representer
    norm = math.sqrt(np.sum(wg * wfun**2))
    assert abs(norm - math.sqrt(np.sum(coef**2))) < 1e-10
    return dict(coef=coef, xs=xs, w=np.sin(3 * xs) + xs, partials=np.array(keep), Ns=np.array([2, 4, 6, 10]),
                errs=errs, norm=norm)


def compute_legendre():
    from numpy.polynomial import legendre as L
    xg, wg = L.leggauss(80)
    Q = []
    for k in range(7):
        v = xg**k
        for qv in Q:
            v = v - np.sum(wg * v * qv) * qv
        Q.append(v / math.sqrt(np.sum(wg * v * v)))
    maxdiff = 0.0
    for n in range(7):
        Pn = L.legval(xg, [0] * n + [1]) * math.sqrt((2 * n + 1) / 2)
        maxdiff = max(maxdiff, np.abs(Q[n] - Pn).max())
    assert maxdiff < 1e-12
    xs = np.linspace(-1, 1, 401)
    curves = np.array([L.legval(xs, [0] * n + [1]) * math.sqrt((2 * n + 1) / 2) for n in range(5)])
    return dict(maxdiff=maxdiff, xs=xs, curves=curves)


def compute_fejer():
    x = np.linspace(-np.pi, np.pi, 8001)
    Ns = np.array([5, 10, 20, 40])
    # Fejer kernel K_N = (1/(N+1)) (sin((N+1)x/2) / sin(x/2))^2, normalized by 1/(2 pi)
    K = []
    for N in Ns:
        with np.errstate(invalid="ignore", divide="ignore"):
            k = (np.sin((N + 1) * x / 2) / np.sin(x / 2)) ** 2 / (N + 1)
        k[np.isclose(x, 0)] = N + 1
        assert k.min() >= -1e-12 and abs(trap(k, x) / (2 * np.pi) - 1) < 1e-6
        K.append(k)
    K = np.array(K)
    # the sawtooth on (0, 2 pi): s_N overshoots (Gibbs), sigma_N never exceeds pi/2
    xs = np.linspace(1e-4, 2 * np.pi - 1e-4, 6001)
    f = (np.pi - xs) / 2
    n = np.arange(1, 201)
    S = np.cumsum(np.sin(np.outer(n, xs)) / n[:, None], axis=0)
    s200 = S[-1]
    sig200 = S.mean(axis=0)  # (s_0 + ... ) averages; s_0 = 0 included below
    sig200 = (S.sum(axis=0)) / 201
    assert s200.max() > np.pi / 2 + 0.25 and sig200.max() <= np.pi / 2 + 1e-9
    l2 = np.array([math.sqrt(trap((f - S[N - 1]) ** 2, xs) / (2 * np.pi)) for N in (10, 50, 200)])
    assert np.all(np.diff(l2) < 0)
    # a continuous f (a triangle wave): sigma_N -> f uniformly
    tri = np.abs(((xs + np.pi) % (2 * np.pi)) - np.pi)
    a0 = np.pi / 2
    sup_err = []
    for N in (4, 16, 64):
        k = np.arange(1, N + 1)
        ck = np.where(k % 2 == 1, -4 / (np.pi * k**2), 0.0)
        partials = a0 + np.cumsum(ck[:, None] * np.cos(np.outer(k, xs)), axis=0)
        sigma = (a0 + partials.sum(axis=0)) / (N + 1)
        sup_err.append(np.abs(sigma - tri).max())
    sup_err = np.array(sup_err)
    assert np.all(np.diff(sup_err) < 0)
    return dict(x=x, Ns=Ns, K=K, xs=xs, f=f, s200=s200, sig200=sig200, l2=l2, sup_err=sup_err)


def compute_variation():
    x = np.linspace(0, 2 * np.pi, 400001)
    tv = trap(np.abs(np.sin(5 * x)), x)
    assert abs(tv - 4) < 1e-6
    total = trap(np.sin(5 * x), x)
    assert abs(total) < 1e-9
    return dict(tv=tv, total=total)


def compute_radon():
    h = lambda t: 1 + 0.8 * np.sin(4 * t)  # noqa: E731  the density of lambda with respect to Lebesgue measure m
    pts = np.array([0.15, 0.4, 0.62, 0.85])
    rs = np.array([0.2, 0.05, 0.01, 0.001])
    ratios = []
    for p in pts:
        row = []
        for r in rs:
            t = np.linspace(p - r, p + r, 2001)
            row.append(trap(h(t), t) / (2 * r))
        ratios.append(row)
    ratios = np.array(ratios)
    assert np.allclose(ratios[:, -1], h(pts), atol=1e-5)
    # von Neumann: phi = lambda + m has d lambda / d phi = g = h / (1 + h); then h = g / (1 - g)
    t = np.linspace(0, 1, 1001)
    g = h(t) / (1 + h(t))
    assert np.all((g >= 0) & (g < 1)) and np.allclose(g / (1 - g), h(t))
    # with an atom: lambda = h dm + 0.3 delta_0.7; phi = lambda + m puts mass 0.3 at 0.7 and g(0.7) = 1 there
    x = np.linspace(0, 1, 200001)
    rng = np.random.default_rng(3)
    for _ in range(20):
        cs = rng.normal(size=4)
        f = lambda s: cs[0] + cs[1] * s + cs[2] * np.sin(5 * s) + cs[3] * np.cos(9 * s)  # noqa: E731
        lhs = trap(f(x) * h(x), x) + 0.3 * f(0.7)
        rhs = trap(f(x) * (h(x) / (1 + h(x))) * (1 + h(x)), x) + f(0.7) * 1.0 * 0.3
        assert abs(lhs - rhs) < 1e-10
    return dict(pts=pts, rs=rs, ratios=ratios, hp=h(pts), t=t, g=g, atom=0.7, atom_mass=0.3)


def compute_dual():
    rng = np.random.default_rng(4)
    p = 3.0
    q = p / (p - 1)
    g = rng.normal(size=8)
    gq = np.sum(np.abs(g) ** q) ** (1 / q)
    xstar = np.sign(g) * np.abs(g) ** (q - 1)
    xstar /= np.sum(np.abs(xstar) ** p) ** (1 / p)
    val = float(g @ xstar)
    assert abs(val - gq) < 1e-12
    best = 0.0
    for _ in range(20000):
        x = rng.normal(size=8)
        x /= np.sum(np.abs(x) ** p) ** (1 / p)
        best = max(best, float(g @ x))
    assert best <= gq + 1e-12 and best > 0.9 * gq
    return dict(p=p, q=q, g=g, gq=gq, xstar=xstar, best=best)


def compute_lebdiff():
    rng = np.random.default_rng(7)
    jumps = np.sort(rng.uniform(0, 1, 30))
    vals = rng.uniform(0, 1, 31)

    def f(t):
        return vals[np.searchsorted(jumps, t)]

    xs = rng.uniform(0, 1, 1000)
    rs = np.array([0.1, 0.01, 0.001, 1e-5])
    good = []
    for r in rs:
        ok = 0
        for x0 in xs:
            t = np.linspace(x0 - r, x0 + r, 801)
            avg = np.mean(f(np.clip(t, 0, 1)))
            ok += abs(avg - f(np.array([x0]))[0]) < 1e-9
        good.append(ok / len(xs))
    good = np.array(good)
    assert good[-1] >= 0.998 and np.all(np.diff(good) >= 0)
    # Vitali covering: random intervals; greedy disjoint subfamily by decreasing length; 3x enlargements cover
    c = rng.uniform(0, 1, 60)
    L = rng.uniform(0.01, 0.12, 60)
    order = np.argsort(-L)
    chosen = []
    for i in order:
        if all(abs(c[i] - c[j]) >= (L[i] + L[j]) / 2 for j in chosen):
            chosen.append(i)
    chosen = np.array(chosen)
    grid = np.linspace(0, 1, 20001)
    union = np.any([(np.abs(grid - c[i]) <= L[i] / 2) for i in range(60)], axis=0)
    big = np.any([(np.abs(grid - c[i]) <= 1.5 * L[i]) for i in chosen], axis=0)
    assert np.all(big[union])
    m_union = union.mean()
    m_chosen = L[chosen].sum()
    assert m_union <= 3 * m_chosen + 1e-3
    return dict(rs=rs, good=good, c=c, L=L, chosen=chosen, m_union=m_union, m_chosen=m_chosen)


def compute_cantorac():
    # removed intervals to depth 12: the Cantor function is constant on each, so its increments there are 0
    iv = [(0.0, 1.0)]
    removed = []
    for _ in range(12):
        new = []
        for a, b in iv:
            l = (b - a) / 3
            removed.append((a + l, b - l))
            new += [(a, a + l), (b - l, b)]
        iv = new
    removed = np.array(removed)
    total_removed = np.diff(removed, axis=1).sum()
    assert abs(total_removed - (1 - (2 / 3) ** 12)) < 1e-12
    # the Cantor function on a grid (ternary digits up to the first 1, read in binary), to depth 20
    xs = np.linspace(0, 1, 4001)
    F = np.zeros_like(xs)
    for i, x0 in enumerate(xs):
        y, v, scale = x0, 0.0, 0.5
        for _ in range(20):
            y *= 3
            d = min(int(y), 2)
            y -= d
            if d == 1:
                v += scale
                break
            v += scale * (d // 2)
            scale /= 2
        F[i] = v
    F[-1] = 1.0
    assert np.all(np.diff(F) >= -1e-12) and F[0] == 0
    # the 2^n covering intervals of level n: total length (2/3)^n, and F rises by 2^-n across each, 1 in all
    lens = (2 / 3) ** np.arange(0, 9)
    return dict(total_removed=total_removed, removed=removed[:63], xs=xs, F=F, lens=lens)


def compute_holder():
    x = np.linspace(0, 1, 20001)
    p = 3.0
    q = p / (p - 1)
    f, g = x, np.cos(np.pi * x / 2) + 0.15
    F = f / trap(np.abs(f) ** p, x) ** (1 / p)
    G = g / trap(np.abs(g) ** q, x) ** (1 / q)
    U = np.abs(F) ** p / p + np.abs(G) ** q / q
    L = np.abs(F * G)
    assert np.all(L <= U + 1e-12)
    iL, iU = trap(L, x), trap(U, x)
    assert abs(iU - 1) < 1e-8 and iL < 1
    # the raw inequality for f, g themselves
    lhs = trap(np.abs(f * g), x)
    rhs = trap(np.abs(f) ** p, x) ** (1 / p) * trap(np.abs(g) ** q, x) ** (1 / q)
    assert lhs <= rhs and abs(lhs / rhs - iL) < 1e-9
    return dict(x=x[::40], F=F[::40], G=G[::40], U=U[::40], L=L[::40], iL=iL, iU=iU, lhs=lhs, rhs=rhs, p=p, q=q)


def compute_lpnorms():
    x = np.linspace(0, 1, 400001)
    ps = np.array([1, 2, 4, 10, 100])
    norms = np.array([trap((2 * x) ** p, x) ** (1 / p) for p in ps])
    assert np.allclose(norms, 2 / (ps + 1) ** (1 / ps), rtol=1e-6)
    assert np.all(np.diff(norms) > 0) and norms[-1] < 2
    # near 0: int_eps^1 x^(-1/2) = 2 - 2 sqrt(eps) -> 2;  int_eps^1 x^(-1) = log(1/eps) -> infinity
    eps = np.array([1e-2, 1e-4, 1e-8])
    half = 2 - 2 * np.sqrt(eps)
    one = np.log(1 / eps)
    # at infinity: int_1^R x^(-2) = 1 - 1/R -> 1;  int_1^R x^(-1) = log R
    R = np.array([1e2, 1e4, 1e8])
    two = 1 - 1 / R
    return dict(ps=ps, norms=norms, eps=eps, half=half, one=one, R=R, two=two)


def compute_bessel():
    from numpy.polynomial import legendre as L
    xg, wg = L.leggauss(200)
    t, w = (xg + 1) / 2, wg / 2  # [0, 1]; sign is odd, so <sign, e_n> = 2 int_0^1 e_n for odd n
    N = 40
    c = np.zeros(N)
    for n in range(1, N, 2):
        en = L.legval(t, [0] * n + [1]) * math.sqrt((2 * n + 1) / 2)
        c[n] = 2 * np.sum(w * en)
    partial = np.cumsum(c**2)
    assert np.all(partial <= 2 + 1e-12) and np.all(np.diff(partial) >= -1e-15)
    # exact: c_1 = sqrt(3/2), so c_1^2 = 3/2
    assert abs(c[1] ** 2 - 1.5) < 1e-12
    xs = np.linspace(-1, 1, 801)
    curves = []
    for M in (2, 4, 8, 16, 40):
        s_ = sum(c[n] * L.legval(xs, [0] * n + [1]) * math.sqrt((2 * n + 1) / 2) for n in range(M))
        curves.append(s_)
    return dict(c=c, partial=partial, xs=xs, curves=np.array(curves), Ms=np.array([2, 4, 8, 16, 40]))


def compute_trigdense():
    M = 4096
    t = np.linspace(-np.pi, np.pi, M, endpoint=False)
    f = np.abs(t)  # the triangle wave: continuous on the circle
    ks = np.array([1, 4, 16, 64, 256])
    errs, kerns, smooths = [], [], []
    for k in ks:
        Q = ((1 + np.cos(t)) / 2) ** k
        Q /= Q.mean()  # (1 / 2 pi) int Q = 1
        assert Q.min() >= 0
        conv = np.real(np.fft.ifft(np.fft.fft(f) * np.fft.fft(np.fft.ifftshift(Q)))) / M
        errs.append(np.abs(conv - f).max())
        kerns.append(Q)
        smooths.append(conv)
        # Q_k * f is a trigonometric polynomial of degree k
        spec = np.abs(np.fft.fft(conv))
        assert spec[k + 1: M - k].max() < 1e-8 * spec.max()
    errs = np.array(errs)
    assert np.all(np.diff(errs) < 0) and errs[-1] < 0.1
    return dict(t=t[::8], ks=ks, errs=errs, kerns=np.array(kerns)[:, ::8], smooths=np.array(smooths)[:, ::8],
                f=f[::8])


def compute_unbounded():
    # f(x) = |x|^(-1/4) on (-pi, pi); c_n = (1/pi) int_0^pi x^(-1/4) cos(nx) dx = (1/pi) int_0^(pi^(1/4)) 4u^2 cos(n u^4) du
    from numpy.polynomial import legendre as L
    xg, wg = L.leggauss(64)
    U = math.pi ** 0.25
    edges = np.linspace(0, U, 6001)
    a, b = edges[:-1], edges[1:]
    u = ((b - a)[:, None] * (xg[None, :] + 1) / 2 + a[:, None]).ravel()
    wu = ((b - a)[:, None] / 2 * wg[None, :]).ravel()
    Nmax = 1024
    n = np.arange(0, Nmax + 1)
    c = np.array([np.sum(wu * 4 * u**2 * np.cos(k * u**4)) / math.pi for k in n])
    norm2 = 2 / math.sqrt(math.pi)  # (1 / 2 pi) int |x|^(-1/2)
    assert abs(c[0] - (4 / 3) * math.pi ** -0.25) < 1e-10  # (1/2pi) int |x|^(-1/4) = (4/3) pi^(-1/4)
    partial = c[0] ** 2 + 2 * np.cumsum(c[1:] ** 2)  # sum over |n| <= N of |c_n|^2, N = 1, 2, ...
    assert np.all(partial < norm2)
    Ns = np.array([4, 16, 64, 256, 1024])
    l2 = np.sqrt(norm2 - partial[Ns - 1])
    assert np.all(np.diff(l2) < 0)
    # c_n ~ C n^(-3/4), so the squared tail is ~ N^(-1/2) and the L^2 error ~ N^(-1/4): x 0.707 per factor 4
    ratio = l2[1:] / l2[:-1]
    assert np.all(np.abs(ratio - 4 ** -0.25) < 0.02)
    xs = np.linspace(-np.pi, np.pi, 2001)
    curves = np.array([c[0] + 2 * np.sum(c[1:N + 1, None] * np.cos(np.outer(n[1:N + 1], xs)), axis=0) for N in (4, 16, 64)])
    return dict(c=c[:65], norm2=norm2, Ns=Ns, l2=l2, xs=xs, curves=curves)


def compute_cpath():
    x = np.linspace(0, 2 * np.pi, 240001)
    h = (1 + 0.5 * np.cos(x)) * np.exp(3j * x)
    P = np.concatenate([[0], np.cumsum((h[1:] + h[:-1]) / 2 * np.diff(x))])
    assert abs(P[-1]) < 1e-8
    tv = trap(np.abs(h), x)
    assert abs(tv - 2 * np.pi) < 1e-8
    ns = np.array([3, 6, 12, 24, 48, 384])
    lengths = []
    for k in ns:
        idx = np.linspace(0, len(x) - 1, k + 1).astype(int)
        lengths.append(np.abs(np.diff(P[idx])).sum())
    lengths = np.array(lengths)
    assert np.all(np.diff(lengths) > 0) and lengths[-1] < tv and tv - lengths[-1] < 0.01
    return dict(P=P[::200], ns=ns, lengths=lengths, tv=tv)


def compute_probe():
    # Phi(f) = 0.5 f(0.3) + int_0^1 f(x) w(x) dx, w(x) = 1 + 0.5 sin(2 pi x): a measure with an atom
    x = np.linspace(0, 1, 200001)
    w = 1 + 0.5 * np.sin(2 * np.pi * x)
    a = np.linspace(0.02, 0.98, 481)
    rs = np.array([0.1, 0.03, 0.01])
    D = []
    for r in rs:
        row = []
        for a0 in a:
            phi = np.clip(1 - np.abs(x - a0) / r, 0, 1)
            m = trap(phi, x)
            val = 0.5 * max(0.0, 1 - abs(0.3 - a0) / r) + trap(phi * w, x)
            row.append(val / m)
        D.append(row)
    D = np.array(D)
    far = np.abs(a - 0.3) > 0.12
    wa = 1 + 0.5 * np.sin(2 * np.pi * a)
    assert np.abs(D[-1][far] - wa[far]).max() < 2e-3
    assert D[-1].max() > 40  # the atom shows up as a spike of height ~ 0.5 / r
    return dict(a=a, rs=rs, D=D, wa=wa)


def compute_maximal():
    # f = 1_[0.4, 0.6] on R: Mf(x) = 1 on I, (b - a) / (2 (x - a)) for x > b, symmetric for x < a
    a_, b_ = 0.4, 0.6

    def M(x0):
        r = np.geomspace(1e-4, 5, 4000)
        lo, hi = np.maximum(x0 - r, a_), np.minimum(x0 + r, b_)
        return float((np.clip(hi - lo, 0, None) / (2 * r)).max())

    xs = np.linspace(-1.0, 2.0, 601)
    Mf = np.array([M(x0) for x0 in xs])
    exact = np.where(xs > b_, (b_ - a_) / (2 * (xs - a_) + 1e-300),
                     np.where(xs < a_, (b_ - a_) / (2 * (b_ - xs) + 1e-300), 1.0))
    exact[np.isclose(xs, a_) | np.isclose(xs, b_)] = 0.5  # at an endpoint the best ball is half inside
    assert np.allclose(Mf, exact, atol=3e-3)
    lams = np.array([0.5, 0.25, 0.1])
    level = (b_ - a_) * (1 / lams - 1)  # m{Mf > lambda}
    assert np.all(level <= 3 * (b_ - a_) / lams)
    return dict(xs=xs, Mf=exact, lams=lams, level=level)


def compute_ftc():
    # x^2 sin(1/x^2): int_eps^1 |f'| = int_1^(1/eps^2) |sin u / u^2 - cos u / u| du  (u = 1/x^2)
    eps = np.array([0.3, 0.1, 0.03, 0.01])
    var = []
    for e in eps:
        Umax = 1 / e**2
        u = np.linspace(1, Umax, int(max(2e5, Umax * 200)))
        var.append(trap(np.abs(np.sin(u) / u**2 - np.cos(u) / u), u))
    var = np.array(var)
    assert np.all(np.diff(var) > 0)
    # growth like (2/pi) log(1/eps^2): each tenfold step in eps adds about (4/pi) log 10 = 2.93
    assert abs((var[3] - var[1]) - (4 / math.pi) * math.log(10)) < 0.1
    xs = np.linspace(1e-3, 1, 20001)
    fx = xs**2 * np.sin(1 / xs**2)
    return dict(eps=eps, var=var, xs=xs[::4], fx=fx[::4])


def compute_polar():
    from math import erf
    R = 3.0
    sq = math.pi * erf(R) ** 2
    disk = math.pi * (1 - math.exp(-R * R))
    # Riemann sums: on the square grid, and on the polar grid with the Jacobian r
    n = 1200
    g = (np.arange(n) + 0.5) / n * 2 * R - R
    X, Y = np.meshgrid(g, g)
    cart = np.exp(-X**2 - Y**2).sum() * (2 * R / n) ** 2
    rr = (np.arange(n) + 0.5) / n * R
    pol = (np.exp(-rr**2) * rr).sum() * (R / n) * 2 * math.pi
    assert abs(cart - sq) < 1e-6 and abs(pol - disk) < 1e-5 and disk < sq < math.pi
    # area of one polar patch [r, r + dr] x [t, t + dt] is (r + dr/2) dr dt exactly: the factor r
    r0, dr, dt = np.array([0.5, 1.0, 2.0]), 0.25, math.pi / 12
    exact_area = ((r0 + dr) ** 2 - r0**2) / 2 * dt
    assert np.allclose(exact_area, (r0 + dr / 2) * dr * dt)
    return dict(R=R, sq=sq, disk=disk, cart=cart, pol=pol, r0=r0, dr=dr, dt=dt, exact_area=exact_area)


ITEMS = {
    "ramps": compute_ramps,
    "jensen": compute_jensen,
    "young": compute_young,
    "parallel": compute_parallel,
    "stacking": compute_stacking,
    "projection": compute_projection,
    "rieszh": compute_rieszh,
    "legendre": compute_legendre,
    "fejer": compute_fejer,
    "variation": compute_variation,
    "radon": compute_radon,
    "dual": compute_dual,
    "lebdiff": compute_lebdiff,
    "cantorac": compute_cantorac,
    "holder": compute_holder,
    "lpnorms": compute_lpnorms,
    "bessel": compute_bessel,
    "trigdense": compute_trigdense,
    "unbounded": compute_unbounded,
    "cpath": compute_cpath,
    "probe": compute_probe,
    "maximal": compute_maximal,
    "ftc": compute_ftc,
    "polar": compute_polar,
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
