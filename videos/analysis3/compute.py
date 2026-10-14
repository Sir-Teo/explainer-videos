"""Precompute everything numerical in Part 3 of the analysis series ("Integration and the First Function Space").

    python -m videos.analysis3.compute            # everything missing (well under a minute)
    python -m videos.analysis3.compute thomae     # specific items
    python -m videos.analysis3.compute --force    # recompute

Results are cached in ``.cache/analysis3/<name>.npz``; scenes call ``load(name)``.  Every number the narration
quotes is computed here and asserted against the statement it illustrates.

Items:
    failures    the hook's three failures: x^n (continuity lost), n^2 x (1 - x^2)^n (integral lost, Rudin 7.6),
                sin(nx)/sqrt n (derivative lost, 7.5), each under the sup, integral and pointwise lenses
    riemann     upper and lower sums of x^2 on [0, 1] with n equal pieces: U - L = 1/n exactly
    thomae      upper sums of Thomae's function on the dyadic partitions of [0, 1] (lower sums are 0): U -> 0
    stieltjes   the Cantor function as an integrator: int x dC = 1/2 and int x^2 dC = 3/8 from the depth-d Cantor
                intervals, with U - L = 3^-d
    koch        the Koch curve: polygon lengths (4/3)^n, and its vertices to depth 6
    mtest       sum sin(nx)/n^2: partial sums and the Weierstrass M-test bound sum_{n > N} 1/n^2 < 1/N
    dini        (1 + x/n)^n increasing to e^x on [0, 1]: uniform convergence (Dini), sup errors ~ e/(2n)
    cauchyc     Bernstein polynomials of |x - 1/2|: a Cauchy sequence in C[0, 1] whose limit is no polynomial
    peano       Schoenberg's space-filling curve (Rudin, Exercise 7.14): the partial curves, and exact hits on the
                square from the ternary digits
    weier       Rudin's nowhere-differentiable function (7.18) at 12 zoom levels; difference quotients >= (3^m + 1)/2
    equi        largest common delta for {sin(kx)/k} and {sin(kx) : k <= K} at eps = 0.1; Rudin 7.21's escaping bump
    arzela      Arzela-Ascoli by the diagonal process on 40,000 random 1-Lipschitz functions
    landau      Rudin's proof of Weierstrass (7.26): the Landau kernels Q_n, c_n < sqrt n, the convolutions P_n for a
                tent, and Bernstein's polynomials
    stone       the lattice step of Stone-Weierstrass (7.32) run on e^x with lines as the interpolants
    power       cos from its series, pi as twice its first zero; Abel's theorem for sum (-1)^(n+1) x^n / n
    fourier     the sawtooth's coefficients; Dirichlet kernels and their L^1 norms (Lebesgue constants); the
                best-approximation property (8.11) and Bessel's inequality (8.12) checked on random polynomials
    parseval    Parseval for the sawtooth (sum 1/n^2 = pi^2/6); mean-square errors ~ 1/(2N); Gibbs' overshoot 8.95%
"""

from __future__ import annotations

import argparse
import math
import time

import numpy as np

from explainer.tts import REPO_ROOT

DATA_DIR = REPO_ROOT / ".cache" / "analysis3"


def trap(y, x):
    """Trapezoid rule (numpy-version independent)."""
    y, x = np.asarray(y, float), np.asarray(x, float)
    return float(np.sum((y[1:] + y[:-1]) * np.diff(x)) / 2)


# ---------------------------------------------------------------------------
# The hook: three failures of interchanging limits
# ---------------------------------------------------------------------------
def compute_failures():
    x = np.linspace(0, 1, 200001)
    ns = np.array([1, 2, 3, 5, 8, 13, 21, 34, 55, 89])
    # x^n: the pointwise limit is 0 on [0, 1) and 1 at 1; sup over [0, 1) of |x^n - 0| is 1 for every n
    pw_int = np.array([trap(x**n, x) for n in ns])
    assert np.allclose(pw_int, 1 / (ns + 1), atol=1e-6)
    # Rudin 7.6: f_n = n^2 x (1 - x^2)^n -> 0 pointwise, but int_0^1 f_n = n^2 / (2n + 2) -> infinity
    bump_int = np.array([trap(n * n * x * (1 - x * x) ** n, x) for n in ns])
    assert np.allclose(bump_int, ns**2 / (2 * ns + 2), rtol=1e-6)
    # the gentler n x (1 - x^2)^n: integral n / (2n + 2) -> 1/2 while the limit is 0
    gentle_int = np.array([trap(n * x * (1 - x * x) ** n, x) for n in ns])
    assert np.allclose(gentle_int, ns / (2 * ns + 2), rtol=1e-6)
    peak_x = 1 / np.sqrt(2 * ns + 1)  # where n^2 x (1 - x^2)^n peaks
    peak = ns**2 * peak_x * (1 - peak_x**2) ** ns
    assert np.all(np.diff(peak) > 0)
    # Rudin 7.5: sin(nx)/sqrt n -> 0 uniformly (sup = 1/sqrt n), but the derivatives sqrt n cos(nx) do not converge
    sup_s = 1 / np.sqrt(ns)
    der0 = np.sqrt(ns)  # the derivative at 0
    return dict(ns=ns, pw_int=pw_int, bump_int=bump_int, gentle_int=gentle_int, peak_x=peak_x, peak=peak, sup_s=sup_s,
                der0=der0)


# ---------------------------------------------------------------------------
# Riemann sums
# ---------------------------------------------------------------------------
def compute_riemann():
    from fractions import Fraction as Fr
    ns = 2 ** np.arange(1, 15)
    U, L = [], []
    for n in ns:
        i = np.arange(n, dtype=float)
        L.append(float(np.sum((i / n) ** 2) / n))
        U.append(float(np.sum(((i + 1) / n) ** 2) / n))
    U, L = np.array(U), np.array(L)
    assert np.allclose(U - L, 1 / ns, rtol=1e-12)  # telescopes: (f(1) - f(0)) / n
    assert np.all(L < 1 / 3) and np.all(U > 1 / 3)
    # exact values for the small cases shown on screen
    for n in (4, 8):
        Ue = sum(Fr(k + 1, n) ** 2 for k in range(n)) / n
        Le = sum(Fr(k, n) ** 2 for k in range(n)) / n
        assert Ue - Le == Fr(1, n)
    return dict(ns=ns, U=U, L=L)


def smallest_denominators(N: int) -> np.ndarray:
    """For each interval [i/N, (i+1)/N], the smallest q such that some p/q lies in it (closed interval)."""
    i = np.arange(N, dtype=np.int64)
    qmin = np.zeros(N, dtype=np.int64)
    todo = np.ones(N, dtype=bool)
    q = 1
    while todo.any():
        idx = np.nonzero(todo)[0]
        lo = -((-i[idx] * q) // N)  # ceil(i q / N)
        hi = ((i[idx] + 1) * q) // N  # floor((i+1) q / N)
        hit = lo <= hi
        qmin[idx[hit]] = q
        todo[idx[hit]] = False
        q += 1
    return qmin


def compute_thomae():
    ks = np.arange(1, 15)
    U = []
    for k in ks:
        N = 2**k
        U.append(float(np.sum(1.0 / smallest_denominators(N)) / N))
    U = np.array(U)
    assert np.all(np.diff(U) < 0) and U[-1] < 0.02  # U(P) -> 0; every lower sum is 0, so the integral is 0
    # a small partition, drawn on screen: 16 pieces
    q16 = smallest_denominators(16)
    assert q16[0] == 1 and q16[7] == 2 and q16[8] == 2  # [0, 1/16] contains 0/1; [7/16, 8/16] contains 1/2
    return dict(ks=ks, U=U, q16=q16)


# ---------------------------------------------------------------------------
# Riemann-Stieltjes with the Cantor function
# ---------------------------------------------------------------------------
def cantor_intervals(depth: int):
    a = np.array([0.0])
    w = 1.0
    for _ in range(depth):
        w /= 3
        a = np.concatenate([a, a + 2 * w])
    return np.sort(a), w


def cantor_fn(x, depth=30):
    """The Cantor function, by ternary digits."""
    x = np.clip(np.asarray(x, float), 0, 1)
    out = np.zeros_like(x)
    scale = 0.5
    y = x.copy()
    done = np.zeros(x.shape, bool)
    for _ in range(depth):
        y = 3 * y
        d = np.floor(y)
        y = y - d
        mid = (d == 1) & ~done
        out[mid] += scale
        done |= mid
        two = (d >= 2) & ~done
        out[two] += scale
        scale /= 2
    out[x >= 1] = 1.0
    return out


def compute_stieltjes():
    ds = np.arange(1, 21)
    I1, I2, gap = [], [], []
    for d in ds:
        a, w = cantor_intervals(int(d))
        m = 0.5**d  # C rises by 2^-d across each depth-d interval
        L1, U1 = float(np.sum(a) * m), float(np.sum(a + w) * m)
        I1.append((L1 + U1) / 2)
        gap.append(U1 - L1)
        I2.append(float(np.sum(((a + w / 2) ** 2)) * m))
        assert abs((U1 - L1) - 3.0**-d) < 1e-12 and L1 <= 0.5 <= U1
    I1, I2, gap = np.array(I1), np.array(I2), np.array(gap)
    assert abs(I1[-1] - 0.5) < 1e-12 and abs(I2[-1] - 3 / 8) < 1e-8  # 3/8 by self-similarity
    # the integrator alpha = the Cantor function, drawn
    xs = np.linspace(0, 1, 3**8 + 1)
    C = cantor_fn(xs)
    assert np.all(np.diff(C) >= -1e-15) and C[0] == 0 and C[-1] == 1
    return dict(ds=ds, I1=I1, I2=I2, gap=gap, xs=xs, C=C)


# ---------------------------------------------------------------------------
# The Koch curve
# ---------------------------------------------------------------------------
def koch_points(depth: int) -> np.ndarray:
    pts = np.array([[0.0, 0.0], [1.0, 0.0]])
    rot = np.array([[0.5, -math.sqrt(3) / 2], [math.sqrt(3) / 2, 0.5]])
    for _ in range(depth):
        out = [pts[0]]
        for p, q in zip(pts[:-1], pts[1:]):
            d = (q - p) / 3
            a, b = p + d, p + 2 * d
            c = a + rot @ d
            out += [a, c, b, q]
        pts = np.array(out)
    return pts


def compute_koch():
    lengths = []
    for k in range(0, 13):
        lengths.append((4 / 3) ** k)
    pts = {f"p{k}": koch_points(k) for k in range(0, 7)}
    for k in range(0, 7):
        seg = np.linalg.norm(np.diff(pts[f"p{k}"], axis=0), axis=1)
        assert abs(seg.sum() - (4 / 3) ** k) < 1e-9
    lengths = np.array(lengths)
    assert lengths[12] > 31  # depth 12: longer than 31 times the base
    return dict(lengths=lengths, **pts)


# ---------------------------------------------------------------------------
# Uniform convergence
# ---------------------------------------------------------------------------
def compute_mtest():
    x = np.linspace(0, 2 * np.pi, 4001)
    Nmax = 400
    n = np.arange(1, Nmax + 1)
    S = np.cumsum(np.sin(np.outer(n, x)) / n[:, None] ** 2, axis=0)  # S[N-1] = partial sum to N
    ref = S[-1]
    Ns = np.array([1, 2, 3, 5, 10, 20, 50])
    err = np.array([np.abs(ref - S[N - 1]).max() for N in Ns])
    tail = np.array([np.sum(1.0 / n[N:] ** 2) for N in Ns])
    assert np.all(err <= tail + 1e-12) and np.all(tail < 1 / Ns)
    return dict(x=x, S=S[[0, 1, 2, 4, 9, 19, 49, -1]], Ns=Ns, err=err, tail=tail)


def compute_dini():
    x = np.linspace(0, 1, 2001)
    ns = np.array([1, 2, 3, 4, 6, 10, 20, 50, 100])
    err = np.array([np.abs(np.exp(x) - (1 + x / n) ** n).max() for n in ns])
    assert np.all(np.diff(err) < 0)
    # increasing in n at every x (so Dini applies), and the error is largest at x = 1
    for a, b in zip(ns[:-1], ns[1:]):
        assert np.all((1 + x / b) ** b >= (1 + x / a) ** a - 1e-15)
    assert np.allclose(err, np.e - (1 + 1 / ns) ** ns)
    return dict(ns=ns, err=err)


def bernstein(fvals, x):
    """Bernstein polynomial B_n f at points x from f(k/n), k = 0..n (by de Casteljau, stable for large n)."""
    n = len(fvals) - 1
    from scipy.stats import binom
    k = np.arange(n + 1)
    return np.array([np.sum(fvals * binom.pmf(k, n, t)) for t in x])


def compute_cauchyc():
    x = np.linspace(0, 1, 601)  # 1/3 and 2/3 are grid points 200 and 400
    f = np.abs(x - 0.5)
    ns = [2, 4, 8, 16, 32, 64, 128, 256, 512]
    B = np.array([bernstein(np.abs(np.arange(n + 1) / n - 0.5), x) for n in ns])
    err = np.abs(B - f).max(axis=1)
    assert np.all(np.diff(err) < 0) and err[-1] < 0.02  # ~ 1/sqrt(2 pi n)
    # Cauchy: sup |B_m - B_n| <= err_m + err_n
    for i in range(len(ns) - 1):
        assert np.abs(B[i] - B[i + 1]).max() <= err[i] + err[i + 1] + 1e-12
    # coordinates for the camera: values at 1/2 (the corner) and 0.4 (the limit is the point (0, 0.1))
    i5, i4 = 300, 240
    assert abs(x[i5] - 0.5) < 1e-12 and abs(x[i4] - 0.4) < 1e-12
    coords = np.c_[B[:, i5], B[:, i4]]
    lim = np.array([f[i5], f[i4]])
    # every later dot stays in the square of half-width err[k] around the limit
    for k in range(len(ns)):
        assert np.all(np.abs(coords[k:] - lim).max(axis=1) <= err[k] + 1e-12)
    return dict(x=x, ns=np.array(ns), B=B, err=err, coords=coords, lim=lim)


# ---------------------------------------------------------------------------
# Schoenberg's space-filling curve (Rudin, Exercise 7.14)
# ---------------------------------------------------------------------------
def sfc_f(t):
    """f: period 2, even, 0 on [0, 1/3], 3t - 1 on [1/3, 2/3], 1 on [2/3, 1]."""
    t = np.mod(np.asarray(t, float), 2.0)
    t = np.where(t > 1, 2 - t, t)
    return np.clip(3 * t - 1, 0, 1)


def sfc(t, terms):
    x = sum(0.5**n * sfc_f(3.0 ** (2 * n - 1) * t) for n in range(1, terms + 1))
    y = sum(0.5**n * sfc_f(3.0 ** (2 * n) * t) for n in range(1, terms + 1))
    return x, y


def compute_peano():
    out = {}
    for terms in range(1, 5):
        t = np.linspace(0, 1, 3 ** (2 * terms + 2) + 1)
        x, y = sfc(t, terms)
        out[f"x{terms}"], out[f"y{terms}"] = x, y
    # Rudin's hint: for x0 = sum a_n 2^-n, y0 = sum b_n 2^-n (digits 0/1), t0 = sum 2 c_i 3^-(i+1) with
    # c_{2n-1} = a_n, c_{2n} = b_n hits (x0, y0) exactly
    # (checked in exact rational arithmetic: floating point cannot resolve 3^24 t0)
    from fractions import Fraction as Fr

    def f_exact(t):
        t = t % 2
        t = 2 - t if t > 1 else t
        return min(max(3 * t - 1, Fr(0)), Fr(1))

    rng = np.random.default_rng(3)
    for _ in range(200):
        a, b = rng.integers(0, 2, 12), rng.integers(0, 2, 12)
        c = np.empty(24, dtype=int)
        c[0::2], c[1::2] = a, b
        t0 = sum(Fr(2 * int(c[i]), 3 ** (i + 2)) for i in range(24))
        x0 = sum(Fr(int(a[n]), 2 ** (n + 1)) for n in range(12))
        y0 = sum(Fr(int(b[n]), 2 ** (n + 1)) for n in range(12))
        xx = sum(Fr(1, 2**n) * f_exact(3 ** (2 * n - 1) * t0) for n in range(1, 13))
        yy = sum(Fr(1, 2**n) * f_exact(3 ** (2 * n) * t0) for n in range(1, 13))
        assert xx == x0 and yy == y0
    return out


# ---------------------------------------------------------------------------
# Weierstrass's nowhere-differentiable function, Rudin's version (7.18)
# ---------------------------------------------------------------------------
def rough(x, terms: int = 24):
    """sum_n (3/4)^n phi(4^n x), phi(x) = |x| on [-1, 1], extended with period 2."""
    x = np.asarray(x, dtype=float)
    out = np.zeros_like(x)
    for n in range(terms):
        y = 4.0**n * x
        out += 0.75**n * np.abs(y - 2 * np.round(y / 2))
    return out


def compute_weier():
    x0 = 0.3
    quot, dms = [], []
    for m in range(1, 11):
        dm = 0.5 * 4.0**-m
        if math.floor(4**m * x0) != math.floor(4**m * x0 + 4**m * dm - 1e-12):
            dm = -dm
        qm = (rough(np.array([x0 + dm]), 30)[0] - rough(np.array([x0]), 30)[0]) / dm
        quot.append(qm)
        dms.append(dm)
        assert abs(qm) >= (3**m + 1) / 2 - 1e-6
    # the m-th term alone has slope +-3^m on the segment; the earlier terms add at most 3^m - 1 / 2 in total
    quot = np.array(quot)
    return dict(x0=x0, quot=quot, dms=np.array(dms))


# ---------------------------------------------------------------------------
# Equicontinuity
# ---------------------------------------------------------------------------
def compute_equi():
    eps = 0.1
    # {sin(kx)/k}: sup_x |f(x + d) - f(x)| = 2 sin(k d / 2)/k, largest at k = 1: delta = 2 arcsin(eps / 2)
    d_soft = 2 * math.asin(eps / 2)
    Ks = np.array([1, 10, 100, 1000])
    d_hard = d_soft / Ks  # {sin(kx) : k <= K}: 2 sin(K d / 2) < eps
    # check by brute force on a grid
    x = np.linspace(0, 2 * np.pi, 20001)
    for K, dh in zip(Ks[:3], d_hard[:3]):
        worst = max(np.abs(np.sin(k * (x + dh * 0.999)) - np.sin(k * x)).max() for k in range(1, K + 1))
        assert worst < eps
        worst2 = max(np.abs(np.sin(k * (x + dh * 1.01)) - np.sin(k * x)).max() for k in range(1, K + 1))
        assert worst2 >= eps
    worst_soft = max(np.abs(np.sin(k * (x + d_soft * 0.999)) / k - np.sin(k * x) / k).max() for k in range(1, 200))
    assert worst_soft < eps
    # Rudin 7.21: f_n = x^2 / (x^2 + (1 - n x)^2): |f_n| <= 1, f_n -> 0 pointwise, f_n(1/n) = 1
    xs = np.linspace(0, 1, 100001)
    ns = np.array([1, 2, 4, 8, 16, 32])
    sups = np.array([(xs**2 / (xs**2 + (1 - n * xs) ** 2)).max() for n in ns])
    assert np.allclose(sups, 1.0, atol=1e-6)
    return dict(eps=eps, d_soft=d_soft, Ks=Ks, d_hard=d_hard, ns=ns, sups=sups)


def compute_arzela():
    """The diagonal process run on a big random family: f(x) = a0/2 + sum_j a_j sin(j pi x)/(j pi), sum |a_j| <= 1,
    so |f| <= 1 and |f'| <= 1 (uniformly bounded, equicontinuous).  At stage i we keep the functions whose value at
    the i-th dyadic point lies in the fullest bin of width 0.25 (0.55)^i (the finite stand-in for 'infinitely
    many'); the diagonal sequence takes the i-th survivor at stage i."""
    rng = np.random.default_rng(11)
    K, J = 400000, 3
    a = rng.normal(size=(K, J)) / np.arange(1, J + 1) ** 0.5
    a /= np.abs(a).sum(axis=1, keepdims=True) * rng.uniform(1.0, 1.4, size=(K, 1))
    a0 = rng.uniform(-1, 1, size=K) * (1 - np.abs(a).sum(axis=1))
    j = np.arange(1, J + 1)

    def curves(rows, x):
        return a0[rows, None] / 2 + (a[rows] / (j * np.pi)) @ np.sin(np.outer(j * np.pi, x))

    pts = np.array([0.5, 0.25, 0.75, 0.125, 0.375, 0.625, 0.875])
    V = curves(np.arange(K), pts)
    idx = np.arange(K)
    stages, diag, survivors, bin_lo, bin_w = [], [], [], [], []
    for i in range(len(pts)):
        v = V[idx, i]
        w = 0.25 * 0.55**i
        bins = np.floor(v / w)
        vals, counts = np.unique(bins, return_counts=True)
        best = vals[np.argmax(counts)]
        idx = idx[bins == best]
        stages.append(len(idx))
        diag.append(idx[min(i, len(idx) - 1)])
        survivors.append(idx[:12])
        bin_lo.append(best * w)
        bin_w.append(w)
    # the values of the first 12 survivors of each stage at that stage's point: all inside the stage's bin
    surv_vals = np.array([V[survivors[i], i] for i in range(len(pts))])
    bin_lo, bin_w = np.array(bin_lo), np.array(bin_w)
    assert np.all(surv_vals >= bin_lo[:, None] - 1e-12) and np.all(surv_vals <= (bin_lo + bin_w)[:, None] + 1e-12)
    stages = np.array(stages)
    x = np.linspace(0, 1, 401)
    G = curves(np.array(diag), x)
    sample = curves(np.arange(60), x)
    assert np.abs(sample).max() <= 1 + 1e-9 and np.abs(np.diff(sample, axis=1)).max() / (x[1] - x[0]) <= 1 + 1e-6
    gaps = np.array([np.abs(G[k + 1:] - G[k]).max() for k in range(len(G) - 1)])  # sup over all later terms
    assert np.all(stages[1:] < stages[:-1]) and stages[-1] >= len(pts)
    assert np.all(np.diff(gaps) < 0) and gaps[-1] < gaps[0] / 4
    return dict(x=x, G=G, gaps=gaps, stages=stages, pts=pts, sample=sample, survivors=np.array(survivors),
                diag=np.array(diag), surv_vals=surv_vals, bin_lo=bin_lo, bin_w=bin_w)


# ---------------------------------------------------------------------------
# Weierstrass approximation, Rudin's proof (7.26), and Bernstein's
# ---------------------------------------------------------------------------
def tent(x):
    x = np.asarray(x, float)
    return np.clip(np.minimum(1.6 * x, np.minimum(0.55 + 0.0 * x, 1.25 * (1 - x))), 0, None) * ((x >= 0) & (x <= 1))


def c_landau(n: int) -> float:
    # int_{-1}^{1} (1 - x^2)^n dx = 2 * 4^n (n!)^2 / (2n + 1)!  (computed in logs)
    lg = math.log(2) + n * math.log(4) + 2 * math.lgamma(n + 1) - math.lgamma(2 * n + 2)
    return math.exp(-lg)


def compute_landau():
    ns = np.array([10, 30, 100, 300, 1000, 3000, 10000])
    cn = np.array([c_landau(int(n)) for n in ns])
    assert np.all(cn < np.sqrt(ns))  # Rudin's estimate
    x = np.linspace(0, 1, 401)
    t = np.linspace(0, 1, 40001)
    ft = tent(t)
    P, err = [], []
    for n, c in zip(ns, cn):
        # P_n(x) = int_0^1 f(t) Q_n(t - x) dt, a polynomial in x of degree 2n
        Q = c * np.clip(1 - (t[None, :] - x[:, None]) ** 2, 0, None) ** n
        Pn = np.array([trap(ft * Q[i], t) for i in range(len(x))])
        P.append(Pn)
        err.append(np.abs(Pn - tent(x)).max())
    P, err = np.array(P), np.array(err)
    assert np.all(np.diff(err) < 0) and err[-1] < 0.01
    # the kernel's mass outside [-delta, delta] -> 0: Rudin bounds it by sqrt(n) (1 - delta^2)^n
    delta = 0.1
    outside = np.array([1 - c * trap((1 - np.linspace(-delta, delta, 20001) ** 2) ** n, np.linspace(-delta, delta, 20001))
                        for n, c in zip(ns, cn)])
    assert np.all(outside <= 2 * np.sqrt(ns) * (1 - delta**2) ** ns + 1e-12)
    # Bernstein: B_n f(x) = sum f(k/n) C(n, k) x^k (1-x)^(n-k)
    bns = np.array([10, 30, 100, 300, 1000])
    Bv = np.array([bernstein(tent(np.arange(n + 1) / n), x) for n in bns])
    berr = np.abs(Bv - tent(x)).max(axis=1)
    assert np.all(np.diff(berr) < 0)
    return dict(ns=ns, cn=cn, x=x, P=P, err=err, outside=outside, bns=bns, Bv=Bv, berr=berr)


# ---------------------------------------------------------------------------
# Stone-Weierstrass: the lattice step
# ---------------------------------------------------------------------------
def compute_stone():
    """f = e^x on [0, 1].  For points x, y, g_{xy} is the line through (x, f(x)) and (y, f(y)) (in the algebra).
    Fix x: h_x = max over finitely many y of g_{xy} has h_x(x) = f(x) and h_x > f - eps everywhere.  Then
    min over finitely many x of h_x lies within eps of f."""
    eps = 0.1
    t = np.linspace(0, 1, 2001)
    f = np.exp(t)

    def line(x, y):
        if abs(x - y) < 1e-12:
            return np.full_like(t, math.exp(x))
        s = (math.exp(y) - math.exp(x)) / (y - x)
        return math.exp(x) + s * (t - x)

    ys = np.linspace(0, 1, 9)
    xs = np.linspace(0, 1, 21)
    H = []
    for x in xs:
        h = np.max([line(x, y) for y in ys], axis=0)
        assert abs(np.interp(x, t, h) - math.exp(x)) < 1e-9 and np.all(h > f - eps)
        H.append(h)
    H = np.array(H)
    approx = H.min(axis=0)
    err = np.abs(approx - f).max()
    assert err < eps
    # step 1 of 7.32: |y| on [-1, 1] by polynomials (Bernstein's, in u = (y + 1)/2), then |f| = lim P(f)
    y = np.linspace(-1, 1, 1201)
    absdeg = np.array([4, 16, 64])
    absP = np.array([bernstein(np.abs(2 * np.arange(n + 1) / n - 1), (y + 1) / 2) for n in absdeg])
    abserr = np.abs(absP - np.abs(y)).max(axis=1)
    f1 = 0.95 * np.sin(5 * t - 1)
    Pf1 = np.array([bernstein(np.abs(2 * np.arange(n + 1) / n - 1), (f1 + 1) / 2) for n in absdeg])
    assert np.all(np.diff(abserr) < 0)
    assert np.all(np.abs(Pf1 - np.abs(f1)).max(axis=1) <= abserr + 1e-12)
    # 7.33: polynomials in z on the unit circle cannot approximate conj(z): |conj z - P(z)| = |1 - z P(z)|, whose
    # mean over the circle is exactly 1, so its maximum is at least 1
    rng = np.random.default_rng(33)
    th = np.linspace(0, 2 * np.pi, 2001)
    z = np.exp(1j * th)
    W = []
    for _ in range(3):
        c = (rng.normal(size=7) + 1j * rng.normal(size=7)) * 0.16
        w = 1 - z * np.polyval(c[::-1], z)
        mean = complex(trap(w.real, th), trap(w.imag, th)) / (2 * np.pi)
        assert abs(mean - 1) < 1e-9 and np.abs(w).max() >= 1
        W.append(w)
    # the even polynomials on [0, 1] (polynomials in x^2) approximate f(x) = x: least-squares fits of degree 2k
    xe = np.linspace(0, 1, 2001)
    ek = np.array([1, 2, 4, 8, 16])
    EV, eerr = [], []
    for k in ek:
        V = np.polynomial.chebyshev.chebvander(2 * xe * xe - 1, int(k))
        c, *_ = np.linalg.lstsq(V, xe, rcond=None)
        EV.append(V @ c)
        eerr.append(np.abs(V @ c - xe).max())
    eerr = np.array(eerr)
    assert np.all(np.diff(eerr) < 0) and eerr[-1] < 0.02
    return dict(t=t, f=f, H=H, approx=approx, err=err, eps=eps, xs=xs, ys=ys, y=y, absdeg=absdeg, absP=absP,
                abserr=abserr, f1=f1, Pf1=Pf1, th=th, W=np.array(W), xe=xe, ek=ek, EV=np.array(EV), eerr=eerr)


# ---------------------------------------------------------------------------
# Power series: cos and pi; Abel's theorem
# ---------------------------------------------------------------------------
def cos_series(x, terms=40):
    s, term = 0.0, 1.0
    for k in range(terms):
        s += term
        term *= -x * x / ((2 * k + 1) * (2 * k + 2))
    return s


def compute_power():
    assert cos_series(0.0) == 1 and cos_series(2.0) < 0  # Rudin 8.7: cos changes sign on (0, 2)
    a, b = 0.0, 2.0
    mids = []
    for _ in range(60):
        m = (a + b) / 2
        mids.append(m)
        if cos_series(m) > 0:
            a = m
        else:
            b = m
    zero = (a + b) / 2
    assert abs(2 * zero - math.pi) < 1e-12
    # the brackets [a_k, b_k] of the bisection, for the picture
    a, b, br = 0.0, 2.0, []
    for _ in range(60):
        br.append((a, b))
        m = (a + b) / 2
        a, b = (m, b) if cos_series(m) > 0 else (a, m)
    br = np.array(br)
    assert np.all(br[:, 0] <= math.pi / 2) and np.all(br[:, 1] >= math.pi / 2 - 1e-15)
    xs = np.array([0.5, 0.9, 0.99, 0.999, 0.9999])
    n = np.arange(1, 2_000_001)
    abel = np.array([np.sum((-1.0) ** (n + 1) * x**n / n) for x in xs])
    assert np.allclose(abel, np.log1p(xs), atol=1e-9) and abs(abel[-1] - math.log(2)) < 1e-4
    # alternating partial sums of 1 - 1/2 + 1/3 - ... at x = 1
    alt = np.cumsum((-1.0) ** (np.arange(1, 41) + 1) / np.arange(1, 41))
    assert abs(alt[-1] - math.log(2)) < 1 / 41
    # 8.1: the geometric series on [-r, r]: sup |1/(1-x) - s_N| = r^(N+1) / (1 - r)
    r = 0.8
    xx = np.linspace(-r, r, 4001)
    Ng = np.array([2, 4, 8, 16, 32])
    gerr = np.array([np.abs(1 / (1 - xx) - sum(xx**k for k in range(N + 1))).max() for N in Ng])
    assert np.allclose(gerr, r ** (Ng + 1) / (1 - r), rtol=1e-9)
    # e^{it} as a sum of rotating terms (it)^n / n!, at t = 2.0
    tt = 2.0
    terms = np.array([(1j * tt) ** k / math.factorial(k) for k in range(20)])
    heads = np.cumsum(terms)
    assert abs(heads[-1] - complex(math.cos(tt), math.sin(tt))) < 1e-9
    # 8.8, d'Alembert's step: near a point z0 with P(z0) != 0, |P| takes smaller values
    P = np.array([1, 0, -2, 2], dtype=complex)  # z^3 - 2z + 2
    z0 = 0.35 + 0.25j
    th = np.linspace(0, 2 * np.pi, 721)
    rad = 0.25
    img = np.polyval(P, z0 + rad * np.exp(1j * th))
    assert np.abs(img).min() < abs(np.polyval(P, z0))
    roots = np.roots(P)
    return dict(zero=zero, mids=np.array(mids[:12]), brackets=br, xs=xs, abel=abel, alt=alt, r=r, Ng=Ng, gerr=gerr,
                tt=tt, terms=terms, heads=heads, P=P, z0=z0, rad=rad, th=th, img=img, roots=roots)


# ---------------------------------------------------------------------------
# Fourier series
# ---------------------------------------------------------------------------
def saw(x):
    """(pi - x)/2 on (0, 2 pi), 0 at the jumps, period 2 pi."""
    y = np.mod(np.asarray(x, float), 2 * np.pi)
    return np.where(y == 0, 0.0, (np.pi - y) / 2)


def compute_fourier():
    rng = np.random.default_rng(5)
    x = np.linspace(-np.pi, np.pi, 8001)
    f = saw(x)
    N = 6
    n = np.arange(1, N + 1)
    sN = (np.sin(np.outer(n, x)) / n[:, None]).sum(axis=0)  # the sawtooth's s_N: b_n = 1/n
    best = trap((f - sN) ** 2, x)
    worse, samples = [], []
    for i in range(500):
        a0 = rng.normal() * 0.2
        an = rng.normal(size=N) * 0.2
        bn = 1 / n + rng.normal(size=N) * 0.2
        t = a0 + (an[:, None] * np.cos(np.outer(n, x)) + bn[:, None] * np.sin(np.outer(n, x))).sum(axis=0)
        worse.append(trap((f - t) ** 2, x))
        if i < 3:
            samples.append(t)
    worse = np.array(worse)
    assert worse.min() > best  # 8.11: s_N is the best mean-square approximation of degree N
    # Pythagoras behind 8.11: int |f - t|^2 = int |f - s_N|^2 + int |s_N - t|^2 for each t of degree <= N
    for t in samples:
        assert abs(trap((f - t) ** 2, x) - best - trap((sN - t) ** 2, x)) < 1e-6
    # orthonormality (8.9): (1/2pi) int e^{imx} e^{-inx} dx = delta_mn, for |m|, |n| <= 3
    ks = np.arange(-3, 4)
    E = np.exp(1j * np.outer(ks, x))
    gram = np.array([[trap((E[i] * np.conj(E[j])).real, x) / (2 * np.pi) for j in range(len(ks))]
                     for i in range(len(ks))])
    assert np.allclose(gram, np.eye(len(ks)), atol=1e-6)
    # Dini's test (8.14) where the sawtooth is smooth: s_N(pi/2) -> pi/4 and s_N(1) -> (pi - 1)/2
    dN = np.array([1, 2, 5, 10, 100, 1000, 10000])
    dini = np.array([[np.sum(np.sin(np.arange(1, M + 1) * p_) / np.arange(1, M + 1)) for p_ in (np.pi / 2, 1.0)]
                     for M in dN])
    assert abs(dini[-1, 0] - np.pi / 4) < 1e-4 and abs(dini[-1, 1] - (np.pi - 1) / 2) < 1e-3
    # Bessel: sum_{|n| <= N} |c_n|^2 <= (1/2pi) int |f|^2 = pi^2/12, for every N
    tot = np.pi**2 / 12
    bessel = np.array([0.5 * np.sum(1.0 / np.arange(1, M + 1) ** 2) for M in (1, 2, 5, 10, 100, 1000)])
    assert np.all(bessel < tot)
    # Dirichlet kernels D_N(x) = sin((N + 1/2) x) / sin(x/2) and their L^1 norms (1/2pi) int |D_N|
    xx = np.linspace(-np.pi, np.pi, 400001)
    Ns = np.array([1, 2, 5, 10, 20, 50, 100, 200, 500])
    leb = []
    for M in Ns:
        with np.errstate(invalid="ignore", divide="ignore"):
            D = np.sin((M + 0.5) * xx) / np.sin(xx / 2)
        D[np.isclose(xx, 0)] = 2 * M + 1
        leb.append(trap(np.abs(D), xx) / (2 * np.pi))
    leb = np.array(leb)
    assert np.all(np.diff(leb) > 0)
    assert np.allclose(leb[-3:], 4 / np.pi**2 * np.log(Ns[-3:]) + 1.27, atol=0.05)  # ~ (4/pi^2) log N
    return dict(x=x, best=best, worse=worse, samples=np.array(samples), sN=sN, bessel=bessel, tot=tot, Ns=Ns,
                leb=leb, gram=gram, dN=dN, dini=dini)


def compute_parseval():
    x = np.linspace(1e-6, 2 * np.pi - 1e-6, 400001)
    f = (np.pi - x) / 2
    Ns = np.array([1, 2, 5, 10, 20, 50, 100])
    mse = []
    for N in Ns:
        n = np.arange(1, N + 1)
        sN = np.zeros_like(x)
        for k in n:
            sN += np.sin(k * x) / k
        mse.append(trap((f - sN) ** 2, x) / (2 * np.pi))
    mse = np.array(mse)
    tail = np.array([0.5 * (np.pi**2 / 6 - np.sum(1.0 / np.arange(1, N + 1) ** 2)) for N in Ns])
    assert np.allclose(mse, tail, rtol=2e-3, atol=1e-6)  # Parseval: the error is the missing energy
    assert np.all(tail < 1 / (2 * Ns))
    # Parseval's two sides: (1/2pi) int f^2 = pi^2 / 12 = sum |c_n|^2 = (1/2) sum 1/n^2
    lhs = trap(f**2, x) / (2 * np.pi)
    rhs = 0.5 * np.sum(1.0 / np.arange(1, 10**6 + 1) ** 2)
    assert abs(lhs - np.pi**2 / 12) < 1e-6 and abs(lhs - rhs) < 1e-6
    # Gibbs: the first peak of s_N right of the jump at 0, minus the limit value pi/2, as a fraction of the jump pi
    gibbs = []
    GNs = np.array([10, 30, 100, 300, 1000])
    for N in GNs:
        xs = np.linspace(1e-5, 3 * np.pi / (N + 0.5), 4001)
        n = np.arange(1, N + 1)
        s = (np.sin(np.outer(n, xs)) / n[:, None]).sum(axis=0)
        gibbs.append((s.max() - np.pi / 2) / np.pi)
    gibbs = np.array(gibbs)
    from scipy.special import gammaln, sici
    limit = (sici(np.pi)[0] - np.pi / 2) / np.pi
    assert abs(limit - 0.0895) < 1e-4 and abs(gibbs[-1] - limit) < 1e-3
    # 8.15: trigonometric polynomials are dense in C(T).  One explicit choice: Fejer's averages
    # sigma_N = sum_{|n| <= N} (1 - |n|/(N + 1)) c_n e^{inx}, whose kernel is positive (like Landau's)
    xf = np.linspace(-np.pi, np.pi, 4001)
    ff = np.maximum(0.0, 1 - np.abs(xf) / 1.2) + 0.35 * np.maximum(0.0, 1 - np.abs(xf - 2.2) / 0.5)
    FN = np.array([1, 2, 4, 8, 16, 32, 64])
    nmax = int(FN.max())
    cn = np.array([trap(ff * np.cos(n * xf), xf) / (2 * np.pi) for n in range(nmax + 1)]) + 0j
    cn = cn - 1j * np.array([trap(ff * np.sin(n * xf), xf) / (2 * np.pi) for n in range(nmax + 1)])
    sig = []
    for N in FN:
        n = np.arange(1, N + 1)
        w = 1 - n / (N + 1)
        terms = 2 * (w[:, None] * (cn[n, None] * np.exp(1j * np.outer(n, xf))).real).sum(axis=0)
        sig.append(cn[0].real + terms)
        K = 1 + 2 * (w[:, None] * np.cos(np.outer(n, xf))).sum(axis=0)  # the Fejer kernel
        assert K.min() > -1e-9
    sig = np.array(sig)
    ferr = np.abs(sig - ff).max(axis=1)
    assert np.all(np.diff(ferr) < 0)
    # the gamma function (8.17-8.22): Stirling's ratio n! / ((n/e)^n sqrt(2 pi n)) -> 1
    sn = np.array([1, 2, 5, 10, 100, 1000])
    stirling = np.exp(gammaln(sn + 1) - (sn * np.log(sn) - sn + 0.5 * np.log(2 * np.pi * sn)))
    assert np.all(np.diff(stirling) < 0) and abs(stirling[-1] - 1) < 1e-3
    return dict(Ns=Ns, mse=mse, tail=tail, lhs=lhs, rhs=rhs, GNs=GNs, gibbs=gibbs, limit=limit, xf=xf, ff=ff, FN=FN,
                sig=sig, ferr=ferr, sn=sn, stirling=stirling)


ITEMS = {
    "failures": compute_failures,
    "riemann": compute_riemann,
    "thomae": compute_thomae,
    "stieltjes": compute_stieltjes,
    "koch": compute_koch,
    "mtest": compute_mtest,
    "dini": compute_dini,
    "cauchyc": compute_cauchyc,
    "peano": compute_peano,
    "weier": compute_weier,
    "equi": compute_equi,
    "arzela": compute_arzela,
    "landau": compute_landau,
    "stone": compute_stone,
    "power": compute_power,
    "fourier": compute_fourier,
    "parseval": compute_parseval,
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
