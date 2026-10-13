"""Precompute everything numerical in Part 9 of the analysis series ("Distributions and the Fourier Transform").

    python -m videos.analysis9.compute            # everything missing (a minute or two)
    python -m videos.analysis9.compute pairs      # specific items
    python -m videos.analysis9.compute --force    # recompute

Results are cached in ``.cache/analysis9/<name>.npz``; scenes call ``load(name)``.  Every number the narration
quotes is computed here and asserted against the statement it illustrates.  The Fourier transform follows Rudin
throughout: f^(t) = (1/sqrt(2 pi)) int f(x) e^(-ixt) dx.

Items:
    delta       narrowing bumps tested against 10 functions -> phi(0); smoothed steps' derivatives have integral 1
    mollifier   the C-infinity bump exp(-1/(1 - x^2)): derivatives to order 10 vanish at the edge (sympy)
    pv          <p.v. 1/x, phi> by symmetric truncation at eps = 10^-k, against the odd-part integral
    sawcomb     the sawtooth's series differentiated term by term, tested against a bump -> -1/2 int phi + pi phi(0)
    structure   delta''' + delta' as the 5th derivative of a continuous function, tested against phi
    mollify     mollified delta' blows up like eps^-2; the mollified Cantor measure like eps^(log2/log3 - 1)
    pairs       box <-> sinc, Gaussian <-> Gaussian, triangle <-> sinc^2: FFT against closed forms
    plancherel  Plancherel for random functions; inversion of the box: L^2 convergence with Gibbs' overshoot
    poisson     Poisson summation: sum e^(-pi n^2 t) = t^(-1/2) sum e^(-pi n^2 / t)
    paleywiener the transform of a bump on a complex grid: growth like e^(|Im z|)
    sobolev     the sawtooth's H^s norms: finite exactly for s < 1/2
    fundamental the heat kernel; the Newtonian potential tested against phi; u'' + u = delta with E = sin|x| / 2
    wiener      translates of a Gaussian approximate a function; translates of sinc^2 stop at the band-limit bound
    contour     u'' + u = delta by shifting the inversion contour past the zeros of 1 - t^2; u = E * f checked
    decay       the transforms of a box, a triangle and a bump: 1/t, 1/t^2, faster than every power
    pwshift     the bump's transform inverted along Im z = y: the same b(x) inside the support, 0 outside
    gevrey      sup |b^(n)| to n = 20: too fast for analyticity, inside the non-quasi-analytic class (n!)^2
    zeta        the 3-4-1 inequality for zeta, and |zeta(1 + it)| bounded away from 0
    primes      pi(x) against x / log x and li(x), and Chebyshev's psi(x) / x, up to 10^8, four points per decade
"""

from __future__ import annotations

import argparse
import math
import time

import numpy as np

from explainer.tts import REPO_ROOT

DATA_DIR = REPO_ROOT / ".cache" / "analysis9"
SQ2PI = math.sqrt(2 * math.pi)


def trap(y, x):
    y, x = np.asarray(y), np.asarray(x, float)
    return np.sum((y[1:] + y[:-1]) * np.diff(x)) / 2


def bump(x):
    """The standard mollifier profile exp(-1/(1 - x^2)) on (-1, 1), 0 outside (not normalized)."""
    x = np.asarray(x, float)
    out = np.zeros_like(x)
    m = np.abs(x) < 1
    out[m] = np.exp(-1 / (1 - x[m] ** 2))
    return out


_BUMP_MASS = None


def rho(x):
    """The normalized mollifier: int rho = 1."""
    global _BUMP_MASS
    if _BUMP_MASS is None:
        t = np.linspace(-1, 1, 200001)
        _BUMP_MASS = trap(bump(t), t)
    return bump(x) / _BUMP_MASS


# ---------------------------------------------------------------------------
def compute_delta():
    x = np.linspace(-1, 1, 400001)
    rng = np.random.default_rng(1)
    tests = []
    for _ in range(10):
        a, b, c = rng.normal(size=3)
        tests.append((a, b, c))
    ns = np.array([1, 4, 16, 64, 256])
    vals = []
    for a, b, c in tests:
        phi = np.exp(-x * x) * (1 + a * x) * np.cos(b * x + c)
        row = [trap(phi * n * rho(n * x), x) for n in ns]
        vals.append(row)
        phi0 = math.cos(c)
        assert abs(row[-1] - phi0) < 2e-4
    vals = np.array(vals)
    phi0s = np.array([math.cos(c) for _, _, c in tests])
    # smoothed steps H_n = int_{-inf}^x n rho(n t) dt: derivative n rho(n x), integral 1
    for n in ns:
        assert abs(trap(n * rho(n * x), x) - 1) < 1e-6
    return dict(ns=ns, vals=vals, phi0=phi0s)


def compute_mollifier():
    import sympy as sp
    X = sp.symbols("x", real=True)
    f = sp.exp(-1 / (1 - X**2))
    edge = []
    d = f
    for k in range(11):
        if k:
            d = sp.diff(d, X)
        fn = sp.lambdify(X, d, "mpmath")
        import mpmath
        mpmath.mp.dps = 50
        edge.append(float(abs(fn(mpmath.mpf("0.98")))))
    edge = np.array(edge)
    # the derivatives are finite inside but tend to 0 at the edge: at 1 - 1e-3 they are astronomically small
    fn10 = sp.lambdify(X, d, "mpmath")
    tiny = float(abs(fn10(mpmath.mpf(1) - mpmath.mpf("1e-3"))))
    assert tiny < 1e-100
    xs = np.linspace(-1.2, 1.2, 1201)
    return dict(edge=edge, tiny=np.log10(tiny), xs=xs, b=bump(xs))


def compute_pv():
    phi = lambda x: np.exp(-(x - 0.5) ** 2) * (1 + 0.3 * x)  # noqa: E731
    eps = 10.0 ** -np.arange(1, 7)
    vals = []
    for e in eps:
        x = np.concatenate([np.geomspace(e, 30, 400001)])
        vals.append(trap((phi(x) - phi(-x)) / x, x))
    vals = np.array(vals)
    x = np.geomspace(1e-12, 30, 800001)
    lim = trap((phi(x) - phi(-x)) / x, x)
    assert np.all(np.abs(np.diff(vals)) > 0) and abs(vals[-1] - lim) < 1e-5
    # delta'(phi) = -phi'(0)
    h = 1e-6
    dphi0 = (phi(h) - phi(-h)) / (2 * h)
    return dict(eps=eps, vals=vals, lim=lim, dphi0=dphi0)


def compute_sawcomb():
    # phi: a bump on (-2, 2); the sawtooth f = sum sin(nx)/n, f' = -1/2 + pi sum_k delta_(2 pi k) in D'
    x = np.linspace(-2, 2, 400001)
    phi = bump(x / 2) * (1 + 0.4 * x)
    target = -0.5 * trap(phi, x) + math.pi * float(bump(np.array([0.0]))[0])
    Ns = np.array([4, 16, 64, 256, 1024])
    acts = []
    for N in Ns:
        n = np.arange(1, N + 1)
        # <sum cos(nx), phi> term by term
        acts.append(sum(trap(np.cos(k * x) * phi, x) for k in n))
    acts = np.array(acts)
    errs = np.abs(acts - target)
    assert np.all(np.diff(errs) < 0) and errs[-1] < 1e-6
    return dict(Ns=Ns, acts=acts, target=target, errs=errs)


def compute_structure():
    # T = delta'''_(0.3) + 2 delta'_(-0.4) + g, with g a step; F with F^(5) = T, continuous
    x = np.linspace(-3, 10, 1300001)  # far enough right that phi^(5) has died out against F's polynomial growth
    pos = lambda t, k: np.where(t > 0, t**k, 0.0) / math.factorial(k)  # noqa: E731
    F = pos(x - 0.3, 1) + 2 * pos(x + 0.4, 3) + pos(x - 1.0, 5)  # the last term: the 5-fold antiderivative of H(x - 1)
    # test function phi = Gaussian; <T, phi> = -phi'''(0.3) + 2 * (-phi'(-0.4)) + int_1^inf phi
    s = 0.6
    phi = lambda t: np.exp(-t * t / (2 * s * s))  # noqa: E731
    from numpy.polynomial.hermite_e import hermeval

    def dphi(t, k):  # k-th derivative of exp(-t^2 / 2 s^2): (-1/s)^k He_k(t/s) phi
        return (-1 / s) ** k * hermeval(t / s, [0] * k + [1]) * phi(t)

    lhs = -dphi(0.3, 3) + 2 * (-dphi(-0.4, 1)) + trap(phi(x[x >= 1.0]), x[x >= 1.0])
    rhs = (-1) ** 5 * trap(F * dphi(x, 5), x)  # <F^(5), phi> = (-1)^5 <F, phi^(5)>
    assert abs(lhs - rhs) < 1e-6
    keep = x <= 3
    return dict(x=x[keep][::600], F=F[keep][::600], lhs=lhs, rhs=rhs)


def compute_mollify():
    ks = np.arange(1, 7)
    eps = 2.0 ** -ks
    t = np.linspace(-1, 1, 200001)
    drho = np.gradient(rho(t), t)
    sup1 = np.abs(drho).max()
    sups = sup1 / eps**2  # (rho_eps)' = eps^-2 rho'(x / eps)
    # check one directly
    e = eps[2]
    xx = np.linspace(-e, e, 200001)
    direct = np.abs(np.gradient(rho(xx / e) / e, xx)).max()
    assert abs(direct - sups[2]) / sups[2] < 1e-3
    # the Cantor measure mollified: density sup over x of mu([x - e, x + e]) / (2 e) grows like e^(d - 1), d = log2/log3
    d = math.log(2) / math.log(3)
    grid = np.linspace(0, 1, 3**9 + 1)
    # Cantor function on the grid, exactly at triadic points
    F = np.zeros_like(grid)
    for i, x0 in enumerate(grid):
        y, v, sc = x0, 0.0, 0.5
        for _ in range(12):
            y *= 3
            dg = min(int(y + 1e-12), 2)
            y -= dg
            if dg == 1:
                v += sc
                break
            v += sc * (dg // 2)
            sc /= 2
        F[i] = v
    F[-1] = 1.0
    dens = []
    for k in range(1, 7):
        w = 3**-k
        step = int(round(w * (len(grid) - 1)))
        dens.append(np.max(F[step:] - F[:-step]) / w)
    dens = np.array(dens)
    ratios = dens[1:] / dens[:-1]
    assert np.allclose(ratios, 3 ** (1 - d), rtol=0.05)
    return dict(eps=eps, sups=sups, dens=dens, d=d)


def fourier(fx, x, t):
    """Rudin's transform (1/sqrt(2 pi)) int f(x) e^(-ixt) dx by quadrature, for an array of t."""
    return np.array([trap(fx * np.exp(-1j * x * tt), x) for tt in t]) / SQ2PI


def compute_pairs():
    x = np.linspace(-30, 30, 120001)
    t = np.linspace(-12, 12, 481)
    box = np.where(np.isclose(np.abs(x), 1), 0.5, (np.abs(x) < 1).astype(float))  # the jump's midpoint value
    gauss = np.exp(-x * x / 2)
    tri = np.clip(1 - np.abs(x), 0, None)
    with np.errstate(invalid="ignore", divide="ignore"):
        box_hat = np.where(t == 0, 2 / SQ2PI, 2 * np.sin(t) / (SQ2PI * t))
        tri_hat = np.where(t == 0, 1 / SQ2PI, (2 - 2 * np.cos(t)) / (SQ2PI * t * t))
    g_hat = np.exp(-t * t / 2)
    # FFT-free check by quadrature (the box's edges are exact grid points)
    nb = fourier(box, x, t)
    ng = fourier(gauss, x, t)
    nt = fourier(tri, x, t)
    eb, eg, et = np.abs(nb - box_hat).max(), np.abs(ng - g_hat).max(), np.abs(nt - tri_hat).max()
    assert eb < 1e-6 and eg < 1e-8 and et < 1e-6
    return dict(t=t, box_hat=box_hat, g_hat=g_hat, tri_hat=tri_hat, eb=eb, eg=eg, et=et)


def compute_plancherel():
    rng = np.random.default_rng(9)
    N = 1 << 14
    L = 40.0
    x = (np.arange(N) - N / 2) * (L / N)
    dx = L / N
    ratios = []
    for _ in range(20):
        c = rng.normal(size=6)
        f = sum(c[k] * np.exp(-((x - rng.uniform(-3, 3)) ** 2) * rng.uniform(0.5, 3)) * np.cos(rng.uniform(0, 6) * x)
                for k in range(6))
        F = np.fft.fft(f) * dx / SQ2PI
        dt = 2 * math.pi / L
        ratios.append(np.sum(np.abs(F) ** 2) * dt / (np.sum(np.abs(f) ** 2) * dx))
    ratios = np.array(ratios)
    assert np.allclose(ratios, 1, atol=1e-10)
    # inversion of the box from |t| <= T: s_T(x) = (1/pi) int_0^T 2 sin t cos(xt) / t dt
    from scipy.special import sici
    xs = np.linspace(-3, 3, 3001)
    Ts = np.array([5, 20, 80])
    curves, over = [], []
    for T in Ts:
        s = (sici(T * (1 + xs))[0] + sici(T * (1 - xs))[0]) / math.pi
        curves.append(s)
        over.append(s.max() - 1)
    over = np.array(over)
    assert abs(over[-1] - 0.0895) < 0.003
    return dict(ratios=ratios, xs=xs, Ts=Ts, curves=np.array(curves), over=over)


def compute_poisson():
    ts = np.array([0.1, 0.5, 1.0, 2.0, 7.0])
    n = np.arange(-60, 61)
    lhs = np.array([np.sum(np.exp(-math.pi * n * n * t)) for t in ts])
    rhs = np.array([np.sum(np.exp(-math.pi * n * n / t)) / math.sqrt(t) for t in ts])
    assert np.allclose(lhs, rhs, rtol=1e-12, atol=0)
    return dict(ts=ts, lhs=lhs, rhs=rhs)


def compute_paleywiener():
    x = np.linspace(-1, 1, 200001)
    b = bump(x)
    ys = np.array([0.0, 2.0, 4.0, 8.0, 16.0, 32.0, 64.0, 128.0, 256.0])
    vals = np.array([abs(trap(b * np.exp(-1j * x * (1j * y)), x)) / SQ2PI for y in ys])
    # growth rate log|f^(iy)| / y -> 1 = A (the support is [-1, 1]), from below and slowly (the bump is flat at its
    # edges, so the growth is like e^(y - c sqrt(y)))
    rates = np.log(vals[1:]) / ys[1:]
    assert np.all(np.diff(rates) > 0) and rates[-1] < 1 and rates[-1] > 0.85
    # along the real axis: faster than any power
    # along the real axis |f^| oscillates; its envelope (the max over [t, 2t]) dies faster than any power of t
    tr = np.array([10.0, 20.0, 40.0, 80.0, 160.0])
    real = np.array([max(abs(trap(b * np.exp(-1j * x * u), x)) / SQ2PI for u in np.linspace(t, 2 * t, 41)) for t in tr])
    assert np.all(np.diff(real) < 0) and real[-1] * tr[-1] ** 4 < real[-3] * tr[-3] ** 4
    return dict(ys=ys, vals=vals, rates=rates, tr=tr, real=real)


def compute_sobolev():
    N = 10**6
    n = np.arange(1, N + 1, dtype=float)
    ss = np.array([0.3, 0.45, 0.5, 0.55])
    checkpoints = np.array([10**2, 10**3, 10**4, 10**5, 10**6])
    out = []
    for s in ss:
        terms = (1 + n * n) ** s / n**2
        cs = np.cumsum(terms)
        out.append(cs[checkpoints - 1])
    out = np.array(out)
    # the increase per decade of N behaves like 10^(2s - 1) times the previous one: a convergent geometric series
    # for s < 1/2, a constant log 10 at s = 1/2 (log divergence), a growing one for s > 1/2
    inc = np.diff(out, axis=1)
    for i, sv in enumerate(ss):
        ratio = inc[i, 1:] / inc[i, :-1]
        assert np.allclose(ratio, 10 ** (2 * sv - 1), rtol=0.03)
    assert np.allclose(inc[2], math.log(10), rtol=3e-3)
    return dict(ss=ss, checkpoints=checkpoints, sums=out, inc=inc)


def compute_fundamental():
    # heat kernel in 1D: integral 1 for every t
    x = np.linspace(-40, 40, 400001)
    for t in (0.01, 0.1, 1.0, 10.0):
        K = np.exp(-x * x / (4 * t)) / math.sqrt(4 * math.pi * t)
        assert abs(trap(K, x) - 1) < 1e-8
    # Newtonian potential E = -1/(4 pi r) in R^3: <E, Delta phi> = phi(0) for radial phi = exp(-r^2 / 2 s^2)
    s = 0.7
    r = np.linspace(1e-9, 12, 600001)
    phi = np.exp(-r * r / (2 * s * s))
    lap = (r * r / s**4 - 3 / s**2) * phi  # the Laplacian of a radial Gaussian in 3D
    val = trap(-1 / (4 * math.pi * r) * lap * 4 * math.pi * r * r, r)
    assert abs(val - 1) < 1e-6
    # u'' + u = delta: E = sin|x| / 2; <E, phi'' + phi> = phi(0)
    xx = np.linspace(-3, 3, 600001)
    tests = []
    for a in (0.0, 0.4, -0.7):
        ph = bump((xx - a) / 1.5)
        d2 = np.gradient(np.gradient(ph, xx), xx)
        lhs = trap(0.5 * np.sin(np.abs(xx)) * (d2 + ph), xx)
        tests.append((lhs, float(bump(np.array([-a / 1.5]))[0])))
    tests = np.array(tests)
    assert np.allclose(tests[:, 0], tests[:, 1], atol=1e-5)
    return dict(newton=val, tests=tests)


def compute_wiener():
    # least squares by 241 translates on [-40, 40] (where the target and both fits have died out)
    x = np.linspace(-40, 40, 16001)
    target = np.exp(-x * x) * np.cos(5 * x)  # frequencies near +-5
    shifts = np.linspace(-6, 6, 241)

    def fit(kernel):
        A = np.stack([kernel(x - s_) for s_ in shifts], 1)
        coef, *_ = np.linalg.lstsq(A, target, rcond=None)
        approx = A @ coef
        return math.sqrt(trap((approx - target) ** 2, x) / trap(target**2, x)), approx

    gauss = lambda u: np.exp(-u * u / 0.08)  # noqa: E731  transform: a Gaussian, never 0
    sinc2 = lambda u: np.sinc(u / math.pi) ** 2  # noqa: E731  transform: a triangle on [-2, 2]
    eg, ag = fit(gauss)
    es, as_ = fit(sinc2)
    # a combination of translates of sinc^2 has its transform inside [-2, 2]; the best it can do in L^2 is to
    # match the part of the target's spectrum there, so the relative error is at least sqrt(1 - inside)
    t = np.linspace(-2, 2, 40001)
    th = (np.exp(-((t - 5) ** 2) / 4) + np.exp(-((t + 5) ** 2) / 4)) / (2 * math.sqrt(2))
    inside = trap(th**2, t) / (math.sqrt(math.pi / 2) / 2 * (1 + math.exp(-25 / 2)))  # Plancherel: = int f^2
    bound = math.sqrt(1 - inside)
    assert eg < 1e-12 and abs(es - bound) < 1e-5 and es >= bound - 1e-6
    keep = np.abs(x) <= 4
    return dict(eg=eg, es=es, bound=bound, inside=inside, x=x[keep][::4], target=target[keep][::4],
                ag=ag[keep][::4], as_=as_[keep][::4])


def compute_contour():
    # u'' + u = delta: the symbol 1 - t^2 vanishes at t = +-1, so 1/P is not integrable on the real line.  Shift the
    # inversion integral E(x) = (1/2 pi) int e^(ix zeta) / (1 - zeta^2) d zeta to Im zeta = sigma.  The tail is made
    # integrable exactly: 1/(1 - z^2) = 5 / ((1 - z^2)(z^2 + 4)) - 1/(z^2 + 4), and the last term inverts to
    # -e^(-2|x|)/4 on every line |sigma| < 2.
    xs = np.linspace(-6, 6, 241)
    dt, T = 0.002, 300.0
    t = np.arange(-T, T + dt / 2, dt)

    def E(sig):
        z = t + 1j * sig
        g = 5 / ((1 - z * z) * (z * z + 4))
        return np.array([trap(np.exp(1j * x_ * z) * g, t).real / (2 * math.pi) - math.exp(-2 * abs(x_)) / 4
                         for x_ in xs])

    below, above, below2 = E(-0.5), E(0.5), E(-1.0)
    H = np.where(xs > 0, 1.0, 0.0)
    eb = np.abs(below - H * np.sin(xs)).max()  # below the poles: the causal solution H(x) sin x
    ea = np.abs(above + (1 - H) * np.sin(xs)).max()  # above: -H(-x) sin x
    ec = np.abs(below2 - below).max()  # Cauchy: any line below the poles gives the same answer
    assert eb < 1e-7 and ea < 1e-7 and ec < 1e-7
    # solve u'' + u = f by u = E * f with E = sin|x| / 2, and check by finite differences
    x = np.linspace(-8, 8, 8001)
    h = x[1] - x[0]
    f = bump((x + 1.5) / 0.8) - 0.7 * bump((x - 2.0) / 0.6)
    Es = np.sin(np.abs(np.arange(-8000, 8001) * h)) / 2
    u = np.convolve(f, Es)[8000:16001] * h  # the kernel is centered at index 8000
    Ec = np.where(np.arange(-8000, 8001) > 0, np.sin(np.arange(-8000, 8001) * h), 0.0)
    uc = np.convolve(f, Ec)[8000:16001] * h
    res = np.abs((u[2:] - 2 * u[1:-1] + u[:-2]) / h**2 + u[1:-1] - f[1:-1])[1000:-1000].max()
    resc = np.abs((uc[2:] - 2 * uc[1:-1] + uc[:-2]) / h**2 + uc[1:-1] - f[1:-1])[1000:-1000].max()
    assert res < 1e-4 and resc < 1e-4 and np.abs(uc[x < -3]).max() < 1e-12
    return dict(xs=xs, below=below, above=above, eb=eb, ea=ea, ec=ec, x=x[::8], f=f[::8], u=u[::8], uc=uc[::8],
                res=max(res, resc))


def compute_decay():
    # the size of the transform against smoothness: a jump (box), a kink (triangle), C-infinity (the bump)
    # all three curves are the same kind of envelope: the largest |f^(u)| for u in [t, 2t], from the exact transforms
    t = np.geomspace(1, 200, 300)
    u = np.linspace(0, 400, 16001)
    with np.errstate(invalid="ignore", divide="ignore"):
        fb = np.where(u > 0, math.sqrt(2 / math.pi) * np.sin(u) / u, math.sqrt(2 / math.pi))  # box on [-1, 1]
        ft = np.where(u > 0, (2 - 2 * np.cos(u)) / (SQ2PI * u * u), 1 / SQ2PI)  # triangle 1 - |x|
    x = np.linspace(-1, 1, 4001)
    bw = bump(x) * (x[1] - x[0])  # the trapezoid weights (the bump vanishes at the ends)
    w = np.concatenate([np.cos(np.outer(u[i:i + 2000], x)) @ bw for i in range(0, len(u), 2000)]) / SQ2PI  # even
    win = [(u >= tt) & (u <= 2 * tt) for tt in t]
    box = np.array([np.abs(fb[m]).max() for m in win])
    tri = np.array([np.abs(ft[m]).max() for m in win])
    env = np.array([np.abs(w[m]).max() for m in win])
    # the exact formulas, checked against quadrature at a few points
    for uu in (0.7, 3.0, 11.0):
        assert abs(np.sum(np.where(np.abs(x) <= 1, 1.0, 0.0) * np.cos(uu * x)) * (x[1] - x[0]) / SQ2PI
                   - math.sqrt(2 / math.pi) * math.sin(uu) / uu) < 2e-3
        assert abs(np.sum((1 - np.abs(x)) * np.cos(uu * x)) * (x[1] - x[0]) / SQ2PI - (2 - 2 * math.cos(uu)) / (SQ2PI * uu * uu)) < 1e-5
    assert tri.max() <= 1 / SQ2PI + 1e-12 and np.all(tri[t > 6] < box[t > 6])  # the kink wins only from t ~ 6 on
    # faster than every power: t^k * env(t) eventually decreases, for k = 1..6
    for k in range(1, 7):
        y = t**k * env
        assert y[-1] < 0.6 * y.max()  # the peak of t^k env(t) moves out (to t = 2, 7, 21, 42, 69, 106) but exists
    return dict(t=t, box=box, tri=tri, bump=env)


def compute_zeta():
    from mpmath import mpc, zeta
    # the 3-4-1 inequality: |zeta(s)^3 zeta(s + it)^4 zeta(s + 2it)| >= 1 for s > 1, because
    # 3 + 4 cos a + cos 2a = 2 (1 + cos a)^2 >= 0
    ts = np.array([1.0, 14.134725, 30.0])
    sig = np.array([1.5, 1.1, 1.01, 1.001])
    Q = np.array([[float(abs(zeta(s)) ** 3 * abs(zeta(mpc(s, t_))) ** 4 * abs(zeta(mpc(s, 2 * t_)))) for s in sig]
                  for t_ in ts])
    assert np.all(Q >= 1)
    # and Q (s - 1)^3 -> |zeta(1 + it)|^4 |zeta(1 + 2it)| > 0: a zero on Re s = 1 would force Q -> 0
    lim = np.array([float(abs(zeta(mpc(1, t_))) ** 4 * abs(zeta(mpc(1, 2 * t_)))) for t_ in ts])
    assert np.allclose(Q[:, -1] * (sig[-1] - 1) ** 3, lim, rtol=0.02)
    tg = np.linspace(0.5, 40, 400)
    one = np.array([float(abs(zeta(mpc(1, t_)))) for t_ in tg])
    half = np.array([float(abs(zeta(mpc(0.5, t_)))) for t_ in tg])
    assert one.min() > 0.3 and half.min() < 0.05
    return dict(ts=ts, sig=sig, Q=Q, lim=lim, tg=tg, one=one, half=half)


def compute_pwshift():
    # Paley-Wiener's converse in action: invert the bump's transform along the line Im z = y instead of the real
    # axis.  By Cauchy the answer does not depend on y; for x outside the support the integrand is bounded by
    # C e^((A - x) y), which forces f(x) = 0 as y -> infinity.
    s = np.linspace(-1, 1, 1601)
    ws = bump(s) * (s[1] - s[0])
    t = np.arange(-200, 200.0001, 0.01)
    ys = np.array([0.0, 2.0, 4.0, 8.0])
    inside, outside = [], []
    for y in ys:
        z = t + 1j * y
        F = np.concatenate([np.exp(-1j * np.outer(z[i:i + 4000], s)) @ ws for i in range(0, len(z), 4000)]) / SQ2PI
        inside.append(trap(F * np.exp(0.5j * z), t).real / SQ2PI)
        outside.append(trap(F * np.exp(1.5j * z), t).real / SQ2PI)
    inside, outside = np.array(inside), np.array(outside)
    b05 = math.exp(-1 / (1 - 0.25))
    assert np.allclose(inside, b05, atol=1e-6) and np.abs(outside).max() < 1e-7
    return dict(ys=ys, inside=inside, outside=outside, b05=b05)


def compute_gevrey():
    # sup |b^(n)| for the bump b = exp(-1/(1 - x^2)): b^(n) = b P_n / (1 - x^2)^(2n) with
    # P_(n+1) = (1 - x^2)^2 P_n' + (4n x (1 - x^2) - 2x) P_n (exact integers), evaluated in 60-digit arithmetic
    from mpmath import mp, mpf
    from mpmath import exp as mexp
    mp.dps = 60

    def mul(a, b):
        out = [0] * (len(a) + len(b) - 1)
        for i, ai in enumerate(a):
            for j, bj in enumerate(b):
                out[i + j] += ai * bj
        return out

    def add(a, b):
        n = max(len(a), len(b))
        return [(a[i] if i < len(a) else 0) + (b[i] if i < len(b) else 0) for i in range(n)]

    Ps = [[1]]
    for n in range(20):
        p = Ps[-1]
        dp = [i * p[i] for i in range(1, len(p))] or [0]
        Ps.append(add(mul([1, 0, -2, 0, 1], dp), mul([0, 4 * n - 2, 0, -4 * n], p)))
    ns = np.arange(21)
    sups = []
    for n, p in enumerate(Ps):
        def ev(x):
            x = mpf(x)
            v = mpf(0)
            for c in reversed(p):
                v = v * x + c
            return abs(v / (1 - x * x) ** (2 * n) * mexp(-1 / (1 - x * x)))
        grid = np.linspace(0, 0.9995, 2000)  # |b^(n)| is even
        vals = [ev(x) for x in grid]
        i = int(np.argmax([float(v) for v in vals]))
        fine = np.linspace(grid[max(i - 1, 0)], grid[min(i + 1, len(grid) - 1)], 81)
        sups.append(float(max(ev(x) for x in fine)))
    sups = np.array(sups)
    fact = np.array([float(math.factorial(n)) for n in ns])
    a = (sups[1:] / fact[1:]) ** (1 / ns[1:])  # bounded for an analytic function; here it grows like n
    b = (sups[1:] / fact[1:] ** 2) ** (1 / ns[1:])  # bounded: the bump is in the class M_n = (n!)^2
    assert abs(sups[0] - math.exp(-1)) < 1e-12 and a[-1] > 3 * a[4] and b[-1] < 5 and np.all(np.diff(a[3:]) > 0)
    return dict(ns=ns, sups=sups, a=a, b=b)


def compute_primes():
    from mpmath import li

    from videos.riemann.compute import prime_count_checkpoints
    xs = [round(10 ** (k / 4)) for k in range(8, 33)]  # 10^2 .. 10^8, four per decade
    pc = prime_count_checkpoints(xs[-1], xs)
    pi_ = np.array([pc[x] for x in xs], float)
    xs_ = np.array(xs, float)
    r1 = pi_ / (xs_ / np.log(xs_))
    r2 = pi_ / np.array([float(li(x)) for x in xs])
    assert pc[10**8] == 5761455 and abs(r2[-1] - 1) < 1e-3 and np.all(np.diff(r1[4:]) < 0)
    # Chebyshev's psi(x) = sum over prime powers p^k <= x of log p = sum_k theta(x^(1/k))
    from videos.riemann.compute import sieve
    pr = np.flatnonzero(sieve(xs[-1])).astype(float)
    cth = np.cumsum(np.log(pr))

    def theta(y):
        i = np.searchsorted(pr, y, side="right")
        return float(cth[i - 1]) if i else 0.0

    psi = np.array([sum(theta(x ** (1 / k) + 1e-9) for k in range(1, int(math.log2(x)) + 1)) for x in xs])
    r3 = psi / xs_
    assert abs(r3[-1] - 1) < 1e-3 and abs(r3[-1] - 1) < abs(r1[-1] - 1) / 10
    return dict(xs=xs_, pi=pi_, r1=r1, r2=r2, r3=r3)


ITEMS = {
    "delta": compute_delta,
    "mollifier": compute_mollifier,
    "pv": compute_pv,
    "sawcomb": compute_sawcomb,
    "structure": compute_structure,
    "mollify": compute_mollify,
    "pairs": compute_pairs,
    "plancherel": compute_plancherel,
    "poisson": compute_poisson,
    "paleywiener": compute_paleywiener,
    "sobolev": compute_sobolev,
    "fundamental": compute_fundamental,
    "wiener": compute_wiener,
    "contour": compute_contour,
    "decay": compute_decay,
    "zeta": compute_zeta,
    "pwshift": compute_pwshift,
    "gevrey": compute_gevrey,
    "primes": compute_primes,
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
