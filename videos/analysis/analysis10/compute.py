"""Precompute everything numerical in Part 10 of the analysis series ("Banach Algebras and the Spectral Theorem").

    python -m videos.analysis.analysis10.compute            # everything missing (a few minutes)
    python -m videos.analysis.analysis10.compute shift      # specific items
    python -m videos.analysis.analysis10.compute --force    # recompute

Results are cached in ``.cache/analysis10/<name>.npz``; scenes call ``load(name)``.  Every number the narration
quotes is computed here and asserted against the statement it illustrates.

Items:
    shift       the backward shift's eigenvectors (1, l, l^2, ...) for 200 l in the disc; the forward shift has none;
                the pseudospectra of N x N sections (a Jordan block: only eigenvalue 0) filling the disc
    neumann     (I - A)^-1 = sum A^n for a random A with ||A|| = 0.8, error <= 0.8^(n+1) / 0.2
    radius      ||A^n||^(1/n) -> max |eigenvalue| for random matrices; n! ||V^n|| -> 1/2 for the Volterra operator
    calculus    e^A and sqrt(A) by the Cauchy integral around the spectrum, against scipy; spectral mapping
    wiener      1/f for f = 1.2 + Li_2(e^(i theta)): its Fourier coefficients are absolutely summable (Wiener's 1/f)
    normal      for a normal matrix A* is a polynomial in A; f(A) by eigenvectors = f(A) by interpolation
    numrange    the numerical range of a non-normal 4 x 4 matrix: a convex set containing the eigenvalues
    green       the Green's operator of -d^2/dx^2 on [0, 1]: eigenvalues 1/(n pi)^2, eigenfunctions sin(n pi x);
                power iteration and deflation; the heat equation by the eigen-expansion against Crank-Nicolson
    multop      multiplication by x on L^2[0, 1]: narrowing bumps are approximate eigenvectors, none is exact
    pvm         a 50 x 50 self-adjoint H: the spectral measure E_(x,x) as weights on the eigenvalues; the ergodic
                averages of a unitary converge to the projection onto its fixed vectors
    twisted     i d/dx on [0, 1] with f(1) = e^(i theta) f(0): spectrum {2 pi n - theta}
    momentum    -i d/dx, diagonalized by the FFT: F P F^-1 = multiplication by xi
    stone       e^(-itH) for a discretized oscillator by the spectral decomposition and by split-operator steps
    hydrogen    the radial hydrogen problem (l = 0) by finite differences: bound states at -1/(2 n^2), a continuum
    commutator  [x, p] for N x N matrices has trace 0: it cannot be i I
"""

from __future__ import annotations

import argparse
import math
import time
from math import factorial

import numpy as np

from explainer.tts import REPO_ROOT

DATA_DIR = REPO_ROOT / ".cache" / "analysis10"


def trap(y, x):
    y, x = np.asarray(y), np.asarray(x, float)
    return np.sum((y[1:] + y[:-1]) * np.diff(x)) / 2


def rand_matrix(n, seed, complex_=True):
    rng = np.random.default_rng(seed)
    A = rng.normal(size=(n, n))
    if complex_:
        A = A + 1j * rng.normal(size=(n, n))
    return A


# ---------------------------------------------------------------------------
def compute_shift():
    rng = np.random.default_rng(1)
    r = np.sqrt(rng.uniform(0, 0.95**2, 200))
    lam = r * np.exp(2j * math.pi * rng.uniform(0, 1, 200))
    N = 4000
    k = np.arange(N)
    res = []
    for l_ in lam:
        x = l_**k  # (1, l, l^2, ...): S* x = (l, l^2, ...) = l x
        Sx = x[1:]
        res.append(np.linalg.norm(Sx - l_ * x[:-1]) / np.linalg.norm(x))
    res = np.array(res)
    assert res.max() < 1e-12
    # the forward shift: (S - l) x = 0 reads -l x_0 = 0, x_0 - l x_1 = 0, ...: only x = 0.  Numerically, the
    # (N + 1) x N section of S - l has smallest singular value >= 1 - |l| > 0
    smin = []
    for l_ in lam[:20]:
        M = np.zeros((201, 200), complex)
        M[np.arange(200), np.arange(200)] = -l_
        M[np.arange(1, 201), np.arange(200)] = 1
        smin.append(np.linalg.svd(M, compute_uv=False).min())
    smin = np.array(smin)
    assert np.all(smin >= 1 - np.abs(lam[:20]) - 1e-12)
    # pseudospectra: log10 of the smallest singular value of J_N - l, J_N the N x N truncated shift
    g = np.linspace(-1.5, 1.5, 121)
    X, Y = np.meshgrid(g, g)
    L = X + 1j * Y
    pseudo = {}
    for n in (8, 24, 64):
        J = np.diag(np.ones(n - 1), 1)
        out = np.empty(L.shape)
        for i in range(L.shape[0]):
            for j in range(L.shape[1]):
                out[i, j] = np.linalg.svd(J - L[i, j] * np.eye(n), compute_uv=False)[-1]
        pseudo[n] = np.log10(np.maximum(out, 1e-30))
        assert np.allclose(np.linalg.eigvals(J), 0)
    # inside the disc the smallest singular value is about |l|^N: at l = 0.5, N = 64 it is below 1e-18
    assert pseudo[64][60, 80] < -15 and pseudo[64][60, 120] > -1
    return dict(lam=lam, res=res, smin=smin, g=g, p8=pseudo[8], p24=pseudo[24], p64=pseudo[64])


def compute_neumann():
    A = rand_matrix(6, 3)
    A *= 0.8 / np.linalg.norm(A, 2)
    I = np.eye(6)
    inv = np.linalg.inv(I - A)
    S, P = np.zeros_like(A), I.copy()
    errs = []
    for n in range(40):
        S = S + P
        P = P @ A
        errs.append(np.linalg.norm(S - inv, 2))
    errs = np.array(errs)
    bound = 0.8 ** (np.arange(40) + 1) / 0.2
    assert np.all(errs <= bound * (1 + 1e-9)) and errs[-1] < 1e-3
    return dict(errs=errs, bound=bound)


def compute_radius():
    out = []
    for seed in range(10):
        A = rand_matrix(8, 100 + seed)
        rho = np.abs(np.linalg.eigvals(A)).max()
        B = A / rho
        P = np.eye(8, dtype=complex)
        vals = []
        for n in range(1, 1001):
            P = P @ B
            vals.append(np.linalg.norm(P, 2) ** (1 / n))
        out.append(np.array(vals))
    out = np.array(out)  # ||A^n||^(1/n) / rho(A)
    assert np.all(np.abs(out[:, -1] - 1) < 0.01) and np.all(out[:, 0] >= 1 - 1e-12)
    # the Volterra operator V f(x) = int_0^x f on L^2[0, 1]: V^n has kernel (x - y)^(n-1)/(n-1)!, ||V|| = 2/pi
    N = 600
    x = (np.arange(N) + 0.5) / N
    D = x[:, None] - x[None, :]
    ns = np.array([1, 2, 3, 4, 6, 8, 12, 16, 20])
    vn = []
    for n in ns:
        K = np.where(D > 0, D ** (n - 1), 0.0) / factorial(n - 1) / N
        if n == 1:
            K = K + np.eye(N) / (2 * N)
        vn.append(np.linalg.norm(K, 2))
    vn = np.array(vn)
    nf = vn * np.array([factorial(n) for n in ns])
    assert abs(vn[0] - 2 / math.pi) < 1e-5 and np.all(np.diff(nf) < 0) and abs(nf[-1] - 0.5) < 0.01
    roots = vn ** (1 / ns)
    return dict(ratio=out[:, [0, 9, 99, 999]], curves=out[:, ::5], ns=ns, vn=vn, nf=nf, roots=roots)


def compute_calculus():
    from scipy.linalg import expm, sqrtm
    A = rand_matrix(6, 7) * 0.5
    ev = np.linalg.eigvals(A)
    R = np.abs(ev).max() + 1.0
    M = 128
    th = 2 * math.pi * (np.arange(M) + 0.5) / M
    z = R * np.exp(1j * th)
    I = np.eye(6)
    # (1/2 pi i) oint f(l) (l - A)^-1 dl, dl = i l dtheta: the trapezoid rule on a circle converges geometrically
    E = sum(np.exp(l_) * np.linalg.inv(l_ * I - A) * l_ for l_ in z) / M
    err_exp = np.abs(E - expm(A)).max()
    assert err_exp < 1e-10
    # the spectral mapping theorem: the eigenvalues of e^A are e^(eigenvalues of A)
    sm = np.sort_complex(np.linalg.eigvals(E))
    assert np.allclose(sm, np.sort_complex(np.exp(ev)), atol=1e-9)
    # a square root, with a contour around the spectrum that stays in the right half plane
    B = A + (np.abs(ev).max() + 1.5) * I
    evb = np.linalg.eigvals(B)
    c = evb.real.mean()
    rb = np.abs(evb - c).max() + 0.6
    assert c - rb > 0.2
    zb = c + rb * np.exp(1j * th)
    Sq = sum(np.sqrt(l_) * np.linalg.inv(l_ * I - B) * (l_ - c) for l_ in zb) / M
    err_sq = np.abs(Sq @ Sq - B).max()
    assert err_sq < 1e-9 and np.abs(Sq - sqrtm(B)).max() < 1e-8
    return dict(ev=ev, R=R, err_exp=err_exp, evb=evb, c=c, rb=rb, err_sq=err_sq, A=A)


def compute_wiener():
    from mpmath import polylog
    M = 1 << 18
    th = 2 * math.pi * np.arange(M) / M
    n = np.arange(1, M // 2)
    # f = 1.2 + sum_{n >= 1} e^(in theta) / n^2 = 1.2 + Li_2(e^(i theta)); Re f >= 1.2 - pi^2/12 > 0
    f = 1.2 + np.fft.ifft(np.concatenate([[0], 1 / n.astype(float) ** 2, np.zeros(M // 2)])) * M
    probe = [0.3, 2.0, math.pi]
    for t_ in probe:
        i = int(round(t_ / (2 * math.pi) * M))
        assert abs(f[i] - (1.2 + complex(polylog(2, complex(math.cos(th[i]), math.sin(th[i])))))) < 1e-5
    assert f.real.min() > 1.2 - math.pi**2 / 12 - 1e-6
    d = np.fft.fft(1 / f) / M  # Fourier coefficients of 1/f, d[k] for k = 0..M-1 (negative k wrap around)
    k = np.fft.fftfreq(M, 1 / M).astype(int)
    order = np.argsort(k)
    k, d = k[order], d[order]
    absd = np.abs(d)
    Ns = np.array([10, 100, 1000, 10000, 100000])
    partial = np.array([absd[np.abs(k) <= N_].sum() for N_ in Ns])
    # the coefficients decay like 1/n^2 (f has the same kind of singularity at theta = 0), so the tail past N is
    # about 2C/N: the partial sums settle
    pos = (k >= 100) & (k <= 10000)
    C = np.max(absd[pos] * k[pos].astype(float) ** 2)
    assert np.all(np.diff(partial) > 0) and partial[-1] - partial[-2] < 2 * C / 10000 * 1.5
    keep = np.abs(k) <= 60
    nl = np.unique(np.geomspace(1, 100000, 60).astype(int))
    tail = absd[np.searchsorted(k, nl)]
    return dict(theta=th[::256], f=f[::256], k=k[keep], d=d[keep], Ns=Ns, partial=partial, C=C, nl=nl, tail=tail)


def compute_normal():
    rng = np.random.default_rng(5)
    Q, _ = np.linalg.qr(rng.normal(size=(6, 6)) + 1j * rng.normal(size=(6, 6)))
    lam = rng.normal(size=6) + 1j * rng.normal(size=6)
    A = Q @ np.diag(lam) @ Q.conj().T
    assert np.allclose(A @ A.conj().T, A.conj().T @ A)
    # A* = p(A) where p interpolates conj(z) at the eigenvalues
    V = np.vander(lam, 6, increasing=True)
    coef = np.linalg.solve(V, lam.conj())
    pA = sum(c_ * np.linalg.matrix_power(A, j) for j, c_ in enumerate(coef))
    err_star = np.abs(pA - A.conj().T).max()
    # f(z) = |z| e^(i arg z / 2) style continuous f: f(A) by eigenvectors vs by interpolation
    f = np.abs(lam) ** 0.5 * np.exp(0.5j * np.angle(lam))
    fe = Q @ np.diag(f) @ Q.conj().T
    cf = np.linalg.solve(V, f)
    fp = sum(c_ * np.linalg.matrix_power(A, j) for j, c_ in enumerate(cf))
    err_f = np.abs(fe - fp).max()
    assert err_star < 1e-9 and err_f < 1e-9
    return dict(lam=lam, err_star=err_star, err_f=err_f)


def compute_numrange():
    rng = np.random.default_rng(12)
    T = rng.normal(size=(4, 4)) + 1j * rng.normal(size=(4, 4))
    T = np.triu(T)  # non-normal: eigenvalues on the diagonal
    ths = np.linspace(0, 2 * math.pi, 721)
    pts = []
    for t_ in ths:
        Hm = (np.exp(-1j * t_) * T + np.exp(1j * t_) * T.conj().T) / 2
        w, v = np.linalg.eigh(Hm)
        x = v[:, -1]
        pts.append(np.vdot(x, T @ x))
    pts = np.array(pts)
    ev = np.diag(T)
    # convexity check: every random <Tx, x> lies inside the boundary polygon (support function test)
    X = rng.normal(size=(4, 2000)) + 1j * rng.normal(size=(4, 2000))
    X /= np.linalg.norm(X, axis=0)
    vals = np.einsum("ij,ij->j", X.conj(), T @ X)
    for t_ in ths[::10]:
        Hm = (np.exp(-1j * t_) * T + np.exp(1j * t_) * T.conj().T) / 2
        top = np.linalg.eigvalsh(Hm)[-1]
        assert np.all((np.exp(-1j * t_) * vals).real <= top + 1e-9)
        assert np.all((np.exp(-1j * t_) * ev).real <= top + 1e-9)
    # ||T*T|| = ||T||^2, and a self-adjoint matrix has a real numerical range
    assert abs(np.linalg.norm(T.conj().T @ T, 2) - np.linalg.norm(T, 2) ** 2) < 1e-9
    Hs = T + T.conj().T
    assert np.abs(np.einsum("ij,ij->j", X.conj(), Hs @ X).imag).max() < 1e-12
    return dict(pts=pts, ev=ev, vals=vals[:400])


def compute_green():
    from scipy.linalg import eigh
    N = 2000
    x = (np.arange(N) + 0.5) / N
    X, Y = np.meshgrid(x, x, indexing="ij")
    G = np.minimum(X, Y) * (1 - np.maximum(X, Y)) / N  # (Gf)(x) = int g(x, y) f(y) dy, -(Gf)'' = f
    w, v = eigh(G, subset_by_index=[N - 8, N - 1])
    w, v = w[::-1], v[:, ::-1]
    ns = np.arange(1, 9)
    exact = 1 / (ns * math.pi) ** 2
    assert np.allclose(w, exact, rtol=1e-4)
    modes = []
    for i, n_ in enumerate(ns):
        s = np.sin(n_ * math.pi * x)
        s /= np.linalg.norm(s)
        vi = v[:, i] * np.sign(np.dot(v[:, i], s))
        assert np.abs(vi - s).max() < 3e-4
        modes.append(vi * math.sqrt(N))
    # power iteration (with deflation) from a lopsided start, on a coarse grid, for the animation
    Nc = 200
    xc = (np.arange(Nc) + 0.5) / Nc
    Xc, Yc = np.meshgrid(xc, xc, indexing="ij")
    Gc = np.minimum(Xc, Yc) * (1 - np.maximum(Xc, Yc)) / Nc
    u = np.exp(-((xc - 0.25) ** 2) / 0.005) + 0.3 * xc
    iters, rq = [], []
    found = []
    for mode in range(3):
        y = u.copy()
        for _ in range(6):
            for f_ in found:
                y = y - np.dot(y, f_) * f_
            y = Gc @ y
            y /= np.linalg.norm(y)
            iters.append(y * math.sqrt(Nc))
            rq.append(float(y @ Gc @ y))
        found.append(y)
    rq = np.array(rq)
    assert abs(rq[5] - 1 / math.pi**2) < 1e-3 and abs(rq[11] - 1 / (4 * math.pi**2)) < 1e-3
    # heat: u_t = u_xx, u(0) = 1 on [0.2, 0.5], by the eigen-expansion and by Crank-Nicolson
    Nh = 400
    xh = (np.arange(1, Nh)) / Nh
    u0 = ((xh >= 0.2) & (xh <= 0.5)).astype(float)
    u0[np.isclose(xh, 0.2) | np.isclose(xh, 0.5)] = 0.5  # the jumps' midpoints, as the sine series has them
    ts = np.array([0.001, 0.005, 0.02, 0.08])
    nn = np.arange(1, 4001)
    bn = 2 * (np.cos(nn * math.pi * 0.2) - np.cos(nn * math.pi * 0.5)) / (nn * math.pi)
    series = np.array([(bn * np.exp(-((nn * math.pi) ** 2) * t_)) @ np.sin(np.outer(nn, xh) * math.pi) for t_ in ts])
    h = 1 / Nh
    Lap = (np.diag(-2 * np.ones(Nh - 1)) + np.diag(np.ones(Nh - 2), 1) + np.diag(np.ones(Nh - 2), -1)) / h**2
    dt = 1e-5
    Am = np.eye(Nh - 1) - dt / 2 * Lap
    Bm = np.eye(Nh - 1) + dt / 2 * Lap
    step = np.linalg.solve(Am, Bm)
    cn, u_, t_now = [], u0.copy(), 0.0
    for t_ in ts:
        k = int(round((t_ - t_now) / dt))
        u_ = np.linalg.matrix_power(step, k) @ u_
        t_now = t_
        cn.append(u_.copy())
    cn = np.array(cn)
    err_heat = np.abs(cn[1:] - series[1:]).max()  # t = 0.001 still feels the jumps
    assert err_heat < 2e-3
    return dict(x=x[::10], w=w, exact=exact, modes=np.array(modes)[:, ::10], xc=xc, iters=np.array(iters), rq=rq,
                xh=xh, ts=ts, series=series, cn=cn, err_heat=err_heat)


def compute_multop():
    lam = 0.4
    x = np.linspace(0, 1, 400001)
    ws = 0.2 / 2 ** np.arange(6)
    ratios = []
    for w_ in ws:
        psi = np.where(np.abs(x - lam) < w_, np.cos(math.pi * (x - lam) / (2 * w_)), 0.0)
        ratios.append(math.sqrt(trap(((x - lam) * psi) ** 2, x) / trap(psi**2, x)))
    ratios = np.array(ratios)
    # ||(M - l) psi|| / ||psi|| = w sqrt(1/3 - 2/pi^2) for this profile: proportional to the width
    c = math.sqrt(1 / 3 - 2 / math.pi**2)
    assert np.allclose(ratios, c * ws, rtol=1e-4)
    # a wave packet's spectral measure |psi|^2 dx integrates to 1
    psi = np.exp(-((x - 0.55) ** 2) / (2 * 0.08**2)) * np.cos(40 * x)
    psi /= math.sqrt(trap(psi**2, x))
    mass = trap(psi**2, x)
    mean = trap(x * psi**2, x)
    assert abs(mass - 1) < 1e-12
    return dict(ws=ws, ratios=ratios, c=c, mean=mean, xs=x[::400], dens=(psi**2)[::400])


def compute_pvm():
    rng = np.random.default_rng(21)
    B = rng.normal(size=(50, 50))
    H = (B + B.T) / math.sqrt(200)
    lam, V = np.linalg.eigh(H)
    xv = rng.normal(size=50)
    weights = (V.T @ xv) ** 2  # E_(x,x)({l_i}) = |<x, v_i>|^2
    assert abs(weights.sum() - xv @ xv) < 1e-10 and abs(lam @ weights - xv @ H @ xv) < 1e-10
    # E(omega) for omega = (-inf, 0]: a projection commuting with H
    P = V[:, lam <= 0] @ V[:, lam <= 0].T
    assert np.allclose(P @ P, P) and np.allclose(P @ H, H @ P)
    # ergodic averages of a unitary with a 2-dimensional fixed space
    Q, _ = np.linalg.qr(rng.normal(size=(8, 8)) + 1j * rng.normal(size=(8, 8)))
    ph = np.concatenate([[0, 0], rng.uniform(0.3, 2 * math.pi - 0.3, 6)])
    U = Q @ np.diag(np.exp(1j * ph)) @ Q.conj().T
    Pf = Q[:, :2] @ Q[:, :2].conj().T
    y = rng.normal(size=8) + 1j * rng.normal(size=8)
    ns = np.unique(np.geomspace(1, 10000, 40).astype(int))
    errs, acc, Uk, k = [], np.zeros(8, complex), y.copy(), 0
    for n in ns:
        while k < n:
            acc += Uk
            Uk = U @ Uk
            k += 1
        errs.append(np.linalg.norm(acc / n - Pf @ y))
    errs = np.array(errs)
    assert errs[-1] < 1e-3 and np.all(errs * ns <= 2 * np.linalg.norm(y) / np.min(np.abs(np.sin(ph[2:] / 2))) + 1e-9)
    return dict(lam=lam, weights=weights, x2=float(xv @ xv), ns=ns, errs=errs, ph=ph)


def compute_twisted():
    N = 256
    x = np.arange(N) / N
    k = np.fft.fftfreq(N, 1 / N) * 2 * math.pi
    F = np.fft.fft(np.eye(N), axis=0)
    out = {}
    for th in (0.0, math.pi / 2, math.pi):
        # f(x) = e^(i theta x) g(x), g periodic: d/dx f = e^(i theta x) (g' + i theta g); spectral differentiation
        Dg = np.fft.ifft(1j * k[:, None] * F, axis=0)
        E = np.diag(np.exp(1j * th * x))
        D = E @ (Dg + 1j * th * np.eye(N)) @ E.conj().T
        ev = np.linalg.eigvals(1j * D)
        ev = np.sort(ev.real[np.abs(ev) < 30])
        expect = np.array([2 * math.pi * n - th for n in range(-6, 7)])
        expect = np.sort(expect[np.abs(expect) < 30])
        assert len(ev) == len(expect) and np.abs(ev - expect).max() < 1e-4
        out[f"t{th:.3f}"] = ev
    # the boundary condition is really used: f = e^(-i l x) satisfies it only for l in 2 pi Z - theta
    return dict(t0=out["t0.000"], t1=out["t1.571"], t2=out["t3.142"])


def compute_momentum():
    N, L = 4096, 80.0
    x = (np.arange(N) - N / 2) * (L / N)
    h = L / N
    psi = np.exp(-((x + 3) ** 2) / 4 + 2.5j * x) + 0.6 * np.exp(-((x - 4) ** 2) / 2 - 1.0j * x)
    # P psi = -i psi' by sixth-order central differences
    c = [-1 / 60, 3 / 20, -3 / 4, 0, 3 / 4, -3 / 20, 1 / 60]  # for psi(x - 3h), ..., psi(x + 3h)
    dpsi = sum(cc * np.roll(psi, s) for cc, s in zip(c, range(3, -4, -1))) / h
    Ppsi = -1j * dpsi
    xi = np.fft.fftfreq(N, h) * 2 * math.pi
    lhs = np.fft.fft(Ppsi)
    rhs = xi * np.fft.fft(psi)
    m = np.abs(xi) < 8
    err = np.abs(lhs[m] - rhs[m]).max() / np.abs(rhs[m]).max()
    assert err < 1e-8
    order = np.argsort(xi)
    return dict(x=x[::8], psi=psi[::8], xi=xi[order], ft=np.abs(np.fft.fft(psi))[order] * h / math.sqrt(2 * math.pi),
                err=err)


def compute_stone():
    N, L = 512, 24.0
    x = (np.arange(N) - N / 2) * (L / N)
    h = L / N
    k = np.fft.fftfreq(N, h) * 2 * math.pi
    V = x**2 / 2
    F = np.fft.fft(np.eye(N), axis=0)
    T = np.fft.ifft(0.5 * (k**2)[:, None] * F, axis=0)
    H = T + np.diag(V)
    H = (H + H.conj().T) / 2
    E, W = np.linalg.eigh(H)
    assert np.allclose(E[:6], np.arange(6) + 0.5, atol=1e-8)
    psi0 = np.exp(-((x - 2.5) ** 2) / 2).astype(complex)  # a displaced ground state: a coherent state
    psi0 /= np.linalg.norm(psi0)
    c0 = W.conj().T @ psi0
    t1 = 2.0
    exact = W @ (np.exp(-1j * E * t1) * c0)
    dt = 5e-4
    nsteps = int(round(t1 / dt))
    half = np.exp(-0.5j * V * dt)
    kin = np.exp(-0.5j * k**2 * dt)
    p = psi0.copy()
    for _ in range(nsteps):
        p = half * np.fft.ifft(kin * np.fft.fft(half * p))
    err = np.abs(p - exact).max()
    assert err < 1e-5 and abs(np.linalg.norm(p) - 1) < 1e-12
    weights = np.abs(c0[:12]) ** 2
    # coherent state: Poisson weights with mean |alpha|^2 = 2.5^2 / 2
    a2 = 2.5**2 / 2
    pois = np.exp(-a2) * a2 ** np.arange(12) / np.array([factorial(n) for n in range(12)])
    assert np.allclose(weights, pois, atol=1e-8)
    ts = np.linspace(0, 2 * math.pi, 9)
    frames = np.array([np.abs(W @ (np.exp(-1j * E * t_) * c0)) ** 2 / h for t_ in ts])
    return dict(x=x, E=E[:12], weights=weights, err=err, ts=ts, frames=frames)


def compute_hydrogen():
    from scipy.sparse import diags
    from scipy.sparse.linalg import eigsh
    R, N = 120.0, 24000
    h = R / (N + 1)
    r = h * np.arange(1, N + 1)
    main = 1 / h**2 - 1 / r
    off = -0.5 / h**2 * np.ones(N - 1)
    Hm = diags([off, main, off], [-1, 0, 1], format="csc")
    vals = eigsh(Hm, k=40, sigma=-0.6, which="LM", return_eigenvectors=False)
    vals = np.sort(vals)
    bound = vals[vals < 0]
    n = np.arange(1, 6)
    assert np.allclose(bound[:5], -1 / (2 * n**2), atol=1e-3)
    cont = vals[vals > 0]
    assert len(cont) > 5 and cont[0] < 0.01
    return dict(bound=bound, cont=cont)


def compute_commutator():
    N = 64
    x = np.linspace(-4, 4, N, endpoint=False)
    h = x[1] - x[0]
    k = np.fft.fftfreq(N, h) * 2 * math.pi
    F = np.fft.fft(np.eye(N), axis=0)
    P = np.fft.ifft(k[:, None] * F, axis=0)  # p = -i d/dx on periodic samples
    X = np.diag(x)
    Cm = -1j * (X @ P - P @ X)  # would be the identity if [x, p] = i I
    Cm = (Cm + Cm.conj().T) / 2
    w = np.linalg.eigvalsh(Cm)
    near = int(np.sum(np.abs(w - 1) < 0.05))
    assert abs(w.sum()) < 1e-9 and near > 50 and w.min() < -100
    return dict(w=w, near=near, N=N)


ITEMS = {
    "shift": compute_shift,
    "neumann": compute_neumann,
    "radius": compute_radius,
    "calculus": compute_calculus,
    "wiener": compute_wiener,
    "normal": compute_normal,
    "numrange": compute_numrange,
    "green": compute_green,
    "multop": compute_multop,
    "pvm": compute_pvm,
    "twisted": compute_twisted,
    "momentum": compute_momentum,
    "stone": compute_stone,
    "hydrogen": compute_hydrogen,
    "commutator": compute_commutator,
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
