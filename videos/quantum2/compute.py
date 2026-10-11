"""Precompute every simulation and number shown in "Quantum Mechanics, Part 2".

    python -m videos.quantum2.compute                 # everything missing (~25 min on 4 cores)
    python -m videos.quantum2.compute ab wkb          # specific items
    python -m videos.quantum2.compute --force         # recompute

Results are cached in ``.cache/quantum2/<name>.npz`` (the Aharonov-Bohm movie as a memory-mapped ``.npy``);
scenes call ``load(name)`` and never solve anything themselves.  As in Part 1, nothing is a cartoon: every wave is
a numerical solution (split-operator FFTs, exact eigen-expansions, finite-difference and Fourier-grid
eigenproblems), every random sample is seeded (PCG64), the algebra quoted on screen is checked with sympy, and
every number the narration states is computed here and asserted against theory (or data) when it is computed.

Units: hbar = m = 1 in every simulation unless an item says otherwise (atomic units for helium and hydrogen);
physical numbers use CODATA 2022 via scipy.constants.  Measured data (alpha decay, ionization energies) are
committed snapshots in ``videos/quantum2/data`` with their sources.

Items:
    hook        Huygens/Feynman sum over paths through two slits: one arrow per path, the arrows' chain at every
                screen point, and the fringes it builds
    symmetry    rotations that fail to commute, the trace argument against finite [X, P] = i hbar, spherical
                harmonics rendered on spheres (phase = hue) and the ladder operator L+ checked on them
    ab          the Aharonov-Bohm effect: a packet through two slits around a flux tube hidden in the wall,
                finite differences with a Peierls phase, for 13 values of the flux; the fringes slide
    pathint     the path integral in imaginary time: short-time kernels multiplied N times -> the ground-state
                energy; path-integral Monte Carlo of closed Brownian paths; the free kernel's composition law
    slicing     Feynman's short-time step as an algorithm: Trotter error ~ eps^2; a Brownian path's roughness
    stationary  sum over a family of paths of a thrown ball: arrows e^{iS/hbar} form a Cornu spiral that tightens
                as hbar shrinks; the action over a 2D family of paths
    wkb         the quartic oscillator: exact eigenvalues vs WKB / Bohr-Sommerfeld, eigenfunctions, a Wigner
                function sitting on its classical orbit
    gamow       alpha decay: Gamow's tunneling factor vs 29 measured half-lives (NuDat 3 + AME2020)
    perturb     avoided crossings (box + bump, box + tilt), the Stark-shifted box to 2nd order, the divergent
                Bender-Wu series of the anharmonic oscillator (exact rationals) vs exact energies
    golden      Fermi's golden rule: a level decaying into a quasi-continuum (exact), the Lorentzian line, the
                revival at 2 pi / delta
    identical   two particles in a box: distinguishable, bosons, fermions on the (x1, x2) plane; the
                Hong-Ou-Mandel dip with seeded photon counts
    helium      helium by perturbation theory and the variational method (sympy integrals), 1s2s singlet vs
                triplet (two electrons in s-waves, solved on an (r1, r2) grid), ionization energies vs Z (NIST)
    bands       wells added one by one -> bands; Kronig-Penney dispersion; Bloch waves on a ring
    decoherence a cat state's Wigner function under position decoherence; a qubit dephased by N environment
                spins; Joos-Zeh numbers
    dirac       the Dirac equation in 1+1 D: Zitterbewegung of a mixed packet vs a positive-energy packet;
                gamma-matrix algebra checked
    numbers     physical numbers the narration quotes (hydrogen 2p lifetime, flux quanta, fine structure,
                Lamb shift, g - 2, actions of everyday objects, ...)
"""

from __future__ import annotations

import argparse
import json
import math
import time
from fractions import Fraction
from pathlib import Path

import numpy as np
import scipy.constants as sc
import scipy.fft as sfft
from scipy.linalg import eigh, eigh_tridiagonal, expm
from scipy.special import gamma as Gamma
from scipy.special import sph_harm_y

from explainer.tts import REPO_ROOT
from videos.quantum.colormap import BG, hue_rgb, to_uint8
from videos.quantum.compute import gaussian, ho_state, moments, wigner  # noqa: F401  (shared with Part 1)

DATA_DIR = REPO_ROOT / ".cache" / "quantum2"
SNAPSHOT = Path(__file__).resolve().parent / "data"
WORKERS = 4


def rng(seed: int) -> np.random.Generator:
    return np.random.Generator(np.random.PCG64(seed))


def check(cond: bool, what: str) -> None:
    """Assertions that survive ``python -O`` and say what failed."""
    if not cond:
        raise AssertionError(what)


def fourier_grid_H(x, V):
    """Fourier-grid (spectral) Hamiltonian -1/2 d^2/dx^2 + V on a uniform periodic grid (dense, Hermitian)."""
    n = len(x)
    dx = x[1] - x[0]
    k = 2 * np.pi * np.fft.fftfreq(n, dx)
    F = np.fft.fft(np.eye(n), axis=0)
    T = (np.fft.ifft(0.5 * k[:, None] ** 2 * F, axis=0)).real
    return 0.5 * (T + T.T) + np.diag(V)


def fd_H(x, V):
    """Second-order finite-difference -1/2 d^2/dx^2 + V with psi = 0 just outside the grid: (diag, offdiag)."""
    h = x[1] - x[0]
    return 1.0 / h**2 + V, np.full(len(x) - 1, -0.5 / h**2)


# ---------------------------------------------------------------------------
# 1. The hook: a sum over paths through two slits (Huygens-Feynman, monochromatic)
# ---------------------------------------------------------------------------
HOOK = dict(lam=1.0, L1=20.0, L2=40.0, d=4.0, w=1.2, ymax=25.0, n_screen=241, m_show=14, m_fine=400)


def hook_amplitudes(ys, s_pts, P=HOOK):
    """Arrow of each path source -> slit point s -> screen point y: e^{ik(r1 + r2)} / sqrt(r1 r2) (the 2D Green's
    function's phase and 1/sqrt(r) fall-off; obliquity ignored).  Returns (len(ys), len(s_pts)) complex."""
    k = 2 * np.pi / P["lam"]
    r1 = np.hypot(P["L1"], s_pts)[None, :]
    r2 = np.hypot(P["L2"], ys[:, None] - s_pts[None, :])
    return np.exp(1j * k * (r1 + r2)) / np.sqrt(r1 * r2)


def compute_hook():
    P = HOOK
    ys = np.linspace(-P["ymax"], P["ymax"], P["n_screen"])
    yf = np.linspace(-P["ymax"], P["ymax"], 2001)
    out = dict(ys=ys, yf=yf)
    for tag, m in (("show", P["m_show"]), ("fine", P["m_fine"])):
        # midpoints of m equal strips across each slit
        u = (np.arange(m) + 0.5) / m - 0.5
        s_top = P["d"] / 2 + P["w"] * u
        s_bot = -P["d"] / 2 + P["w"] * u
        ds = P["w"] / m
        if tag == "show":
            out["s_top"], out["s_bot"] = s_top, s_bot
            out["arrows"] = np.concatenate([hook_amplitudes(ys, s_top), hook_amplitudes(ys, s_bot)], axis=1) * ds
        else:
            a_top = hook_amplitudes(yf, s_top).sum(1) * ds
            a_bot = hook_amplitudes(yf, s_bot).sum(1) * ds
            out["I_both"] = np.abs(a_top + a_bot) ** 2
            out["I_top"] = np.abs(a_top) ** 2
            out["I_bot"] = np.abs(a_bot) ** 2
    scale = out["I_both"].max()
    for k in ("I_both", "I_top", "I_bot"):
        out[k] = out[k] / scale
    out["arrows"] = out["arrows"] / math.sqrt(scale)
    # checks: the coarse chain at each y sums to (nearly) the converged amplitude; fringe spacing ~ lambda L2 / d
    I_show = np.abs(out["arrows"].sum(1)) ** 2
    I_fine_at = np.interp(ys, yf, out["I_both"])
    check(np.abs(I_show - I_fine_at).max() < 0.02, "hook: 28 arrows per point already converge")
    peaks = [i for i in range(1, len(yf) - 1) if out["I_both"][i] > out["I_both"][i - 1] and out["I_both"][i] >= out["I_both"][i + 1]
             and out["I_both"][i] > 0.15]
    yp = yf[peaks]
    # bright fringes where the two slit-center paths differ by a whole number of wavelengths (exact geometry)
    dpath = np.hypot(P["L2"], yp - P["d"] / 2) - np.hypot(P["L2"], yp + P["d"] / 2)
    frac = np.abs(dpath / P["lam"] - np.round(dpath / P["lam"]))
    # (the single-slit envelope pulls the outer maxima slightly inward, so the outer tolerance is looser)
    check(frac[np.abs(yp) < 15].max() < 0.05 and frac.max() < 0.12, "hook: bright fringes at whole wavelengths")
    central = np.abs(yp) < 12
    spacing = float(np.mean(np.diff(yp[central])))
    theory = P["lam"] * P["L2"] / P["d"]
    check(abs(spacing / theory - 1) < 0.04, f"hook: central fringe spacing {spacing:.2f} vs lambda L/d = {theory:.2f}")
    check(out["I_both"][len(yf) // 2] > 3.5 * out["I_top"][len(yf) // 2], "hook: center ~ 4x one slit")
    out["spacing"] = np.array(spacing)
    out["peaks"] = yp
    return out


# ---------------------------------------------------------------------------
# 2. Symmetry: rotations, the trace argument, spherical harmonics and L+
# ---------------------------------------------------------------------------
def rot(axis: str, a: float) -> np.ndarray:
    c, s = math.cos(a), math.sin(a)
    return {"x": np.array([[1, 0, 0], [0, c, -s], [0, s, c]]),
            "y": np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]]),
            "z": np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])}[axis]


def axis_angle(R):
    ang = math.acos(np.clip((np.trace(R) - 1) / 2, -1, 1))
    ax = np.array([R[2, 1] - R[1, 2], R[0, 2] - R[2, 0], R[1, 0] - R[0, 1]])
    return ang, ax / max(np.linalg.norm(ax), 1e-300)


def sphere_render(fn, res=300, el=np.deg2rad(18.0), az=0.0, light=(-0.5, 0.6, 0.65), gamma=0.8):
    """An orthographic picture of a complex function f(theta, phi) painted on a sphere: hue = arg f, brightness
    = |f| / max|f|, with soft Lambert shading and a dim rim, so the sphere reads as a solid body.  RGBA uint8."""
    u = np.linspace(-1, 1, res)
    X, Y = np.meshgrid(u, -u)
    r2 = X**2 + Y**2
    inside = r2 <= 1
    Z = np.sqrt(np.clip(1 - r2, 0, 1))  # toward the viewer
    # view basis -> world: tilt by el about the screen x axis, turn by az about world z
    ce, se = math.cos(el), math.sin(el)
    # world (x, y, z_up): screen right = x, screen up = z tilted toward viewer
    wx = X
    wy = -Z * ce + Y * se
    wz = Z * se + Y * ce
    ca, sa = math.cos(az), math.sin(az)
    wx, wy = ca * wx - sa * wy, sa * wx + ca * wy
    th = np.arccos(np.clip(wz, -1, 1))
    ph = np.arctan2(wy, wx)
    f = fn(th, ph)
    mag = np.abs(f)
    vmax = np.abs(fn(*np.meshgrid(np.linspace(0, np.pi, 181), np.linspace(-np.pi, np.pi, 361)))).max()
    t = np.clip(mag / vmax, 0, 1) ** gamma
    col = hue_rgb(np.angle(f))
    Lv = np.array(light) / np.linalg.norm(light)
    shade = 0.55 + 0.45 * np.clip(X * Lv[0] + Y * Lv[1] + Z * Lv[2], 0, 1)
    base = np.array([0.16, 0.19, 0.24])  # the sphere's own dim surface where f = 0
    rgb = base * shade[..., None] + t[..., None] * (col * shade[..., None] - base * shade[..., None])
    rim = np.clip((np.sqrt(r2) - 0.93) / 0.07, 0, 1)[..., None]
    rgb = rgb * (1 - 0.5 * rim)
    alpha = np.clip((1 - np.sqrt(r2)) * res / 2, 0, 1)  # antialiased edge
    out = np.concatenate([to_uint8(rgb), to_uint8(alpha)[..., None]], axis=2)
    out[~inside, 3] = 0
    return out


def L_plus(f, th, ph):
    """L+ f = e^{i phi} (d/dtheta + i cot(theta) d/dphi) f (hbar = 1), by centered differences on the grid."""
    dth = th[1, 0] - th[0, 0]
    dph = ph[0, 1] - ph[0, 0]
    ft = (np.roll(f, -1, 0) - np.roll(f, 1, 0)) / (2 * dth)
    fp = (np.roll(f, -1, 1) - np.roll(f, 1, 1)) / (2 * dph)
    return np.exp(1j * ph) * (ft + 1j * fp / np.tan(th))


def compute_symmetry():
    out = {}
    # (a) two small rotations, undone in the other order, leave a rotation about the third axis by ~ eps^2
    eps = np.array([0.6, 0.3, 0.1, 0.03])
    angs, axz = [], []
    for e in eps:
        R = rot("x", e) @ rot("y", e) @ rot("x", -e) @ rot("y", -e)
        a, ax = axis_angle(R)
        angs.append(a)
        axz.append(ax[2])
    angs = np.array(angs)
    out["comm_eps"], out["comm_angle"], out["comm_axis_z"] = eps, angs, np.array(axz)
    check(abs(angs[-1] / eps[-1] ** 2 - 1) < 0.01 and abs(axz[-1]) > 0.999, "symmetry: XYX'Y' ~ R_z(eps^2)")
    # (b) the trace argument: any commutator of finite matrices has zero trace, so [X, P] = i hbar 1 is impossible
    g = rng(1925)
    n = 5
    X = g.normal(size=(n, n)) + 1j * g.normal(size=(n, n))
    X = (X + X.conj().T) / 2
    Pm = g.normal(size=(n, n)) + 1j * g.normal(size=(n, n))
    Pm = (Pm + Pm.conj().T) / 2
    Cm = X @ Pm - Pm @ X
    out["trace_diag"] = np.diag(Cm)
    check(abs(np.trace(Cm)) < 1e-12, "symmetry: tr[X, P] = 0")
    check(np.allclose(Cm.conj().T, -Cm), "symmetry: [X, P] is anti-Hermitian")
    # (c) spherical harmonics on spheres, l = 1, 2 (and l = 0), phase = hue
    for l in (0, 1, 2):
        for m in range(-l, l + 1):
            out[f"Y_{l}_{m}"] = sphere_render(lambda th, ph, l=l, m=m: sph_harm_y(l, m, th, ph))
    # the same for a rotated real combination (a "d orbital" as a superposition) to show interference
    out["Y_dxy"] = sphere_render(lambda th, ph: (sph_harm_y(2, 2, th, ph) - sph_harm_y(2, -2, th, ph)) / (1j * math.sqrt(2)))
    # (d) L+ on the grid: L+ Y_l^m = sqrt(l(l+1) - m(m+1)) Y_l^{m+1}
    th, ph = np.meshgrid(np.linspace(0.3, np.pi - 0.3, 241), np.linspace(-np.pi, np.pi, 721, endpoint=False), indexing="ij")
    errs = []
    for l in (1, 2):
        for m in range(-l, l):
            lhs = L_plus(sph_harm_y(l, m, th, ph), th, ph)[2:-2]
            rhs = math.sqrt(l * (l + 1) - m * (m + 1)) * sph_harm_y(l, m + 1, th, ph)[2:-2]
            errs.append(float(np.abs(lhs - rhs).max() / np.abs(rhs).max()))
    out["Lplus_err"] = np.array(errs)
    check(max(errs) < 1e-3, f"symmetry: L+ Y = sqrt(...) Y (err {max(errs):.1e})")
    # (e) a Galilean boost multiplies psi by e^{i m v x / hbar}: the momentum distribution shifts by m v exactly
    x = np.linspace(-40, 40, 2048, endpoint=False)
    psi = gaussian(x, 0.0, 2.0, 0.0)
    mv = 1.5
    _, _, k0, sk0 = moments(x, psi)
    _, _, k1, sk1 = moments(x, psi * np.exp(1j * mv * x))
    check(abs(k1 - k0 - mv) < 1e-9 and abs(sk1 - sk0) < 1e-9, "symmetry: a boost shifts <p> by m v")
    return out


# ---------------------------------------------------------------------------
# 3. The Aharonov-Bohm effect
# ---------------------------------------------------------------------------
# A packet (k0 = 1.2, lambda = 5.24) hits a plate with two slits; inside the plate, between the slits, sits an
# infinitely thin flux tube carrying flux alpha * h/e.  Gauge: the vector potential is a "cut" running from the
# tube up through the top slit (x = x_c, y > 0), so an electron hopping across x_c there picks up the Peierls phase
# e^{2 pi i alpha}; everywhere else A = 0, and B = 0 everywhere the wave can go.  Kinetic energy is second-order
# finite differences (h = 0.25; local, so the phase sits on one link per row); each row's x-hop with its twisted
# link is applied exactly by a gauge-twisted FFT (a ring with flux), y-hops by a plain FFT (Strang splitting with V
# and the absorbers).  Detection: an absorbing slab on the right; its absorption rate 2 W |psi|^2 integrated over
# time and depth is the arrival density at each height.
AB = dict(h=0.25, X=320.0, Y=288.0, k0=1.2, x0=72.0, sx=10.0, sy=45.0, wall=(115.0, 121.0), V0=10.0, d=24.0, w=8.0, smooth=0.5,
          det=(246.0, 316.0), dt=0.2, t_end=300.0, edge=40.0, W_det=0.3, W_edge=0.5, frame_every=2.0, stride=4,
          alphas=tuple(i / 12 for i in range(13)), movie_alphas=(0.0, 0.5))


def twisted_ring_gauge(N, jc, phi):
    """g with diag(g)^dagger H_twist diag(g) = H_uniform: H_twist has the phase e^{i phi} on the hop jc -> jc+1 of
    an N-site ring, H_uniform has e^{i phi / N} on every hop (checked against expm in the item)."""
    g = np.zeros(N, complex)
    g[(jc + 1) % N] = 1
    for s in range(1, N):
        j = (jc + s) % N
        g[(j + 1) % N] = g[j] * np.exp(1j * phi * (j == jc) - 1j * phi / N)
    return g


def ab_potential(X, Y, P=AB):
    """The slit plate with smooth (tanh) edges: sharp steps let the split-operator scheme scatter a little of the
    wave into high-energy states that would leak through the wall (measured: 0.8% at dt = 0.2 with sharp edges,
    2e-6 with these)."""
    step = lambda u: 0.5 * (1 + np.tanh(u / P["smooth"]))  # noqa: E731
    w0, w1 = P["wall"]
    plate = step(X - w0) * step(w1 - X)
    open_ = np.maximum(step(P["w"] / 2 - np.abs(Y - P["d"] / 2)), step(P["w"] / 2 - np.abs(Y + P["d"] / 2)))
    return P["V0"] * plate * (1 - open_)


def ab_run(alpha, frames=False, P=AB):
    h = P["h"]
    Nx, Ny = int(P["X"] / h), int(P["Y"] / h)
    x = np.arange(Nx) * h
    y = (np.arange(Ny) - Ny // 2) * h
    X, Y = np.meshgrid(x, y)  # rows = y
    V = ab_potential(X, Y, P)
    e = P["edge"]
    d0, d1 = P["det"]
    Wdet = P["W_det"] * np.clip((X - d0) / (d1 - d0), 0, 1) ** 2
    W = Wdet + P["W_edge"] * np.clip((e - X) / e, 0, 1) ** 2 + P["W_edge"] * np.clip((np.abs(Y) - (P["Y"] / 2 - e)) / e, 0, 1) ** 2
    psi = np.exp(-((X - P["x0"]) ** 2) / (4 * P["sx"] ** 2) - Y**2 / (4 * P["sy"] ** 2) + 1j * P["k0"] * X)
    psi = (psi / np.sqrt((np.abs(psi) ** 2).sum() * h * h)).astype(np.complex64)
    dt = P["dt"]
    half = np.exp((-1j * V - W) * dt / 2).astype(np.complex64)
    t = 0.5 / h**2
    kx = 2 * np.pi * np.fft.fftfreq(Nx, h)
    ky = 2 * np.pi * np.fft.fftfreq(Ny, h)
    phi = 2 * np.pi * alpha
    jc = int(round(np.mean(P["wall"]) / h))
    rows = y > 0
    g = twisted_ring_gauge(Nx, jc, phi).astype(np.complex64)
    gc = np.conj(g)
    Ex0 = np.exp(-1j * (2 * t - 2 * t * np.cos(kx * h)) * dt).astype(np.complex64)
    Ext = np.exp(-1j * (2 * t - 2 * t * np.cos(kx * h - phi / Nx)) * dt).astype(np.complex64)
    Ey = np.exp(-1j * (2 * t - 2 * t * np.cos(ky * h)) * dt).astype(np.complex64)
    Wd = (2 * Wdet * h).astype(np.float32)
    det = np.zeros(Ny)
    st = P["stride"]
    every = int(round(P["frame_every"] / dt))
    movie = []
    tube = (int(np.argmin(np.abs(y))), jc)
    tube_max = 0.0
    nsteps = int(round(P["t_end"] / dt))
    for n in range(nsteps):
        if frames and n % every == 0:
            movie.append(psi[::st, ::st].copy())
        rho = np.abs(psi) ** 2
        det += (rho * Wd).sum(axis=1) * dt
        tube_max = max(tube_max, float(rho[tube]))
        psi *= half
        f = psi.copy()
        f[rows] *= gc[None, :]
        F = sfft.fft(f, axis=1, workers=WORKERS)
        F[~rows] *= Ex0[None, :]
        F[rows] *= Ext[None, :]
        f = sfft.ifft(F, axis=1, workers=WORKERS)
        f[rows] *= g[None, :]
        psi = sfft.ifft(sfft.fft(f, axis=0, workers=WORKERS) * Ey[:, None], axis=0, workers=WORKERS)
        psi *= half
    left = float((np.abs(psi) ** 2).sum() * h * h)
    return dict(y=y, det=det, movie=np.array(movie) if frames else None, tube_max=tube_max, left=left)


def compute_ab():
    P = AB
    # the twisted-ring identity used by the solver, on a small ring
    N, jc, phi, dt = 16, 5, 2 * np.pi * 0.37, 0.7
    H = np.zeros((N, N), complex)
    for j in range(N):
        H[j, j] = 1.0
        ph = np.exp(1j * phi) if j == jc else 1.0
        H[(j + 1) % N, j] += -0.5 * ph
        H[j, (j + 1) % N] += -0.5 * np.conj(ph)
    g = twisted_ring_gauge(N, jc, phi)
    k = 2 * np.pi * np.fft.fftfreq(N)
    v = rng(7).normal(size=N) + 0j
    fast = g * np.fft.ifft(np.exp(-1j * (1 - np.cos(k - phi / N)) * dt) * np.fft.fft(np.conj(g) * v))
    check(np.abs(fast - expm(-1j * H * dt) @ v).max() < 1e-12, "ab: twisted-ring FFT step is exact")

    out = {}
    dets = []
    for a in P["alphas"]:
        t0 = time.time()
        r = ab_run(a, frames=a in P["movie_alphas"])
        dets.append(r["det"])
        if r["movie"] is not None:
            mv = r["movie"]
            arr = np.stack([mv.real, mv.imag], axis=-1).astype(np.float16)
            np.save(DATA_DIR / f"ab_movie_{int(round(a * 100)):03d}.npy", arr)
        # (the largest value, ~1.5e-8, is the initial packet's far tail at t = 0; the incoming peak is ~3.5e-4)
        check(r["tube_max"] < 3e-8, f"ab: the wave never reaches the flux tube (max |psi|^2 = {r['tube_max']:.1e})")
        out[f"tube_max_{int(round(a * 120)):03d}"] = np.array(r["tube_max"])
        check(r["left"] < 0.02, "ab: nearly everything absorbed by the end")
        print(f"    alpha = {a:.3f}: {time.time() - t0:5.1f}s, detected {r['det'].sum() * P['h']:.4f}", flush=True)
    y = r["y"]
    dets = np.array(dets)
    out["y"], out["det"], out["alphas"] = y, dets, np.array(P["alphas"])
    # one flux quantum h/e changes nothing
    check(np.abs(dets[-1] - dets[0]).max() < 1e-4 * dets[0].max(), "ab: alpha = 1 equals alpha = 0")
    # half a flux quantum turns the central bright fringe dark
    c = np.argmin(np.abs(y))
    check(dets[6][c] < 0.05 * dets[0][c], "ab: alpha = 1/2 makes the center dark")
    # the fringes slide: the phase of the fringe frequency component moves by 2 pi alpha (central window)
    win = np.abs(y) < 60
    # measure the fringe spacing from alpha = 0 instead of assuming it
    f0 = dets[0][win] - dets[0][win].mean()
    ks = np.linspace(0.1, 0.4, 3001)
    amp = np.abs(np.exp(-1j * np.outer(ks, y[win])) @ f0)
    kf = ks[np.argmax(amp)]
    ph = np.array([np.angle(np.exp(-1j * kf * y[win]) @ (d[win] - d[win].mean())) for d in dets])
    shift = np.unwrap(ph - ph[0])
    out["fringe_k"], out["fringe_phase"] = np.array(kf), shift
    slope = np.polyfit(out["alphas"], shift, 1)[0]
    check(abs(abs(slope) / (2 * np.pi) - 1) < 0.08, f"ab: fringe phase moves 2 pi per flux quantum ({slope / 2 / np.pi:.3f})")
    out["fringe_slope"] = np.array(slope)
    out["movie_t"] = np.arange(0, P["t_end"], P["frame_every"])[: int(round(P["t_end"] / P["frame_every"]))]
    return out


def ab_movie(alpha: float):
    """(frames, y, x, 2) float16 (re, im) of the Aharonov-Bohm run at flux ``alpha``; rows = y (ascending)."""
    return np.load(DATA_DIR / f"ab_movie_{int(round(alpha * 100)):03d}.npy", mmap_mode="r")


# ---------------------------------------------------------------------------
# 4. The path integral in imaginary time (and the free kernel's composition law)
# ---------------------------------------------------------------------------
def euclid_kernel(x, V, eps):
    """Short-time Euclidean kernel K_eps(x, y) dx = sqrt(1/2 pi eps) exp(-(x-y)^2/2eps - eps (V(x)+V(y))/2) dx."""
    dx = x[1] - x[0]
    D = x[:, None] - x[None, :]
    return np.sqrt(1 / (2 * np.pi * eps)) * np.exp(-(D**2) / (2 * eps) - eps * (V[:, None] + V[None, :]) / 2) * dx


def compute_pathint():
    import sympy as sp

    out = {}
    # (a) E0 from the largest eigenvalue of the short-time kernel: lambda_max = e^{-E0(eps) eps}
    x = np.linspace(-7, 7, 561)
    V = 0.5 * x**2
    epss = np.array([2.0, 1.0, 0.5, 0.25, 0.1, 0.05])
    E0 = []
    for e in epss:
        K = euclid_kernel(x, V, e)
        lam = np.linalg.eigvalsh(K)[-1]
        E0.append(-math.log(lam) / e)
    E0 = np.array(E0)
    out["eps"], out["E0"] = epss, E0
    check(abs(E0[-1] - 0.5) < 1e-3, f"pathint: E0 -> 1/2 ({E0[-1]:.5f})")
    # Trotter error ~ eps^2
    slope = np.polyfit(np.log(epss[2:]), np.log(np.abs(E0[2:] - 0.5)), 1)[0]
    check(abs(slope - 2) < 0.15, f"pathint: E0 error ~ eps^2 (slope {slope:.2f})")
    # the ground state, as the kernel's top eigenvector
    K = euclid_kernel(x, V, 0.1)
    w, U = np.linalg.eigh(K)
    g0 = np.abs(U[:, -1])
    g0 /= math.sqrt((g0**2).sum() * (x[1] - x[0]))
    out["x"], out["ground"] = x, g0
    check(np.abs(g0 - ho_state(0, x)).max() < 2e-3, "pathint: top eigenvector = Gaussian ground state")
    # repeated application of the kernel to a lopsided start: the shape relaxes to the ground state
    f = np.exp(-((x - 2.5) ** 2) / 0.5) + 0.6 * np.exp(-((x + 1.5) ** 2) / 0.3)
    snaps, taus = [], [0.0, 0.2, 0.5, 1.0, 2.0, 4.0, 8.0]
    K = euclid_kernel(x, V, 0.05)
    cur, tau = f.copy(), 0.0
    for T in taus:
        while tau < T - 1e-9:
            cur = K @ cur
            tau += 0.05
        snaps.append(cur / math.sqrt((cur**2).sum() * (x[1] - x[0])))
    out["relax_tau"], out["relax"] = np.array(taus), np.array(snaps)
    # (b) path-integral Monte Carlo: closed Brownian paths in imaginary time, weighted by e^{-int V}
    beta, M = 10.0, 100
    eps = beta / M
    g = rng(1948)
    path = np.zeros(M)
    keep, kept_paths = [], []
    nsweep = 30000
    step = 0.7 * math.sqrt(eps)
    acc = 0
    for sweep in range(nsweep):
        # single-bead moves
        for j in g.permutation(M):
            old = path[j]
            new = old + step * g.normal()
            a, b = path[j - 1], path[(j + 1) % M]
            dS = ((new - a) ** 2 + (b - new) ** 2 - (old - a) ** 2 - (b - old) ** 2) / (2 * eps) + eps * 0.5 * (new**2 - old**2)
            if dS < 0 or g.random() < math.exp(-dS):
                path[j] = new
                acc += 1
        # whole-path shift
        sh = 0.5 * g.normal()
        dS = eps * 0.5 * (((path + sh) ** 2).sum() - (path**2).sum())
        if dS < 0 or g.random() < math.exp(-dS):
            path = path + sh
        if sweep >= 1000 and sweep % 5 == 0:
            keep.append(path.copy())
            if sweep % 1250 == 0:
                kept_paths.append(path.copy())
    keep = np.array(keep)
    x2 = float((keep**2).mean())
    theory = 0.5 / math.tanh(beta / 2)  # thermal <x^2> of the continuum oscillator
    kk = np.arange(M)
    disc = float((1 / ((2 / eps) * (1 - np.cos(2 * np.pi * kk / M)) + eps)).mean())  # exact for the M-slice action
    check(abs(disc / theory - 1) < 2e-3, "pathint: 100 slices are already close to the continuum")
    check(abs(x2 / disc - 1) < 0.03, f"pathint: PIMC <x^2> = {x2:.4f} vs {disc:.4f} (exact for {M} slices)")
    out["pimc_x2_exact"] = np.array(disc)
    out["pimc_paths"], out["pimc_beta"] = np.array(kept_paths), np.array(beta)
    hist, edges = np.histogram(keep.ravel(), bins=80, range=(-3, 3), density=True)
    out["pimc_hist"], out["pimc_edges"], out["pimc_x2"] = hist, edges, np.array(x2)
    out["pimc_acc"] = np.array(acc / (nsweep * M))
    # (c) the free kernel composes: int K(x, y; t1) K(y, z; t2) dy = K(x, z; t1 + t2) (Gaussian integral, sympy)
    xs, ys, zs = sp.symbols("x y z", real=True)
    a1, a2 = sp.symbols("a1 a2", positive=True)  # a = m / (2 hbar t) after Wick rotation t -> -i tau
    Kf = lambda u, v, a: sp.sqrt(a / sp.pi) * sp.exp(-a * (u - v) ** 2)  # noqa: E731
    lhs = sp.simplify(sp.integrate(Kf(xs, ys, a1) * Kf(ys, zs, a2), (ys, -sp.oo, sp.oo)))
    rhs = Kf(xs, zs, a1 * a2 / (a1 + a2))  # 1/a adds: tau1 + tau2
    check(sp.simplify(lhs - rhs) == 0, "pathint: free kernels compose")
    return out


# ---------------------------------------------------------------------------
# 5. Time slicing as an algorithm, and the roughness of Brownian paths
# ---------------------------------------------------------------------------
def compute_slicing():
    out = {}
    # A packet in an anharmonic well, evolved for T = 6 by eps-slices (Strang = symmetric time slicing) vs exact
    n = 256
    x = np.linspace(-10, 10, n, endpoint=False)
    V = 0.05 * x**4 - 0.6 * x**2
    H = fourier_grid_H(x, V)
    E, U = eigh(H)
    dx = x[1] - x[0]
    psi0 = gaussian(x, 1.8, 0.6, 0.5)
    psi0 = psi0 / math.sqrt((np.abs(psi0) ** 2).sum() * dx)
    T = 6.0
    exact = U @ (np.exp(-1j * E * T) * (U.conj().T @ psi0))
    k = 2 * np.pi * np.fft.fftfreq(n, dx)
    epss = np.array([1.0, 0.5, 0.25, 0.125, 0.0625, 0.03125])
    errs = []
    for e in epss:
        steps = int(round(T / e))
        half = np.exp(-0.5j * V * e)
        kin = np.exp(-0.5j * k**2 * e)
        p = psi0.copy()
        for _ in range(steps):
            p = half * np.fft.ifft(kin * np.fft.fft(half * p))
        errs.append(math.sqrt((np.abs(p - exact) ** 2).sum() * dx))
    errs = np.array(errs)
    slope = np.polyfit(np.log(epss[2:]), np.log(errs[2:]), 1)[0]
    check(abs(slope - 2) < 0.15, f"slicing: global error ~ eps^2 (slope {slope:.2f})")
    out["eps"], out["err"], out["slope"] = epss, errs, np.array(slope)
    out["x"], out["V"], out["psi0"], out["psiT"] = x, V, psi0, exact
    # Brownian path (imaginary-time free path): increments with variance eps; zoom windows show the same roughness
    g = rng(1923)
    N = 2**18
    dW = g.normal(size=N) * math.sqrt(1.0 / N)
    W = np.concatenate([[0.0], np.cumsum(dW)])
    tt = np.linspace(0, 1, N + 1)
    out["bm_t"], out["bm_W"] = tt[::16], W[::16]  # 16385 points for the full view
    zooms = []
    for (a, b) in ((0.0, 1.0), (0.375, 0.5), (0.4375, 0.453125), (0.44140625, 0.443359375)):
        i0, i1 = int(a * N), int(b * N)
        idx = np.linspace(i0, i1, 2049).astype(int)
        zooms.append(np.stack([tt[idx], W[idx]]))
    out["bm_zooms"] = np.array(zooms)
    # quadratic variation: sum (dW)^2 over [0, 1] = 1
    check(abs((dW**2).sum() - 1) < 0.01, "slicing: sum dW^2 = 1")
    return out


# ---------------------------------------------------------------------------
# 6. Stationary phase: a thrown ball's paths and their arrows
# ---------------------------------------------------------------------------
# A ball thrown up and caught: x(0) = x(T) = 0 in uniform gravity g (m = 1).  Family of paths
# x(t) = x_cl(t) + a sin(pi t / T) + b sin(2 pi t / T); for a linear potential the action is exactly quadratic:
# S = S_cl + pi^2 a^2 / (4 T) + pi^2 b^2 / T.
STAT = dict(T=2.0, g=1.0, a_max=1.6, n_a=321, hbars=(0.25, 0.08, 0.025), n_map=401)


def action(xs, ts, g):
    """S = int (1/2 xdot^2 - g x) dt by the midpoint rule on a fine grid."""
    dt = ts[1] - ts[0]
    v = np.diff(xs, axis=-1) / dt
    xm = 0.5 * (xs[..., 1:] + xs[..., :-1])
    return ((0.5 * v**2 - g * xm) * dt).sum(-1)


def compute_stationary():
    P = STAT
    T, g = P["T"], P["g"]
    ts = np.linspace(0, T, 2001)
    xcl = 0.5 * g * ts * (T - ts)
    a = np.linspace(-P["a_max"], P["a_max"], P["n_a"])
    paths = xcl[None, :] + a[:, None] * np.sin(np.pi * ts / T)[None, :]
    S = action(paths, ts, g)
    Scl = action(xcl, ts, g)
    check(abs(Scl - (-(g**2) * T**3 / 24)) < 1e-6, "stationary: S_cl = -g^2 T^3 / 24")
    check(np.abs(S - Scl - np.pi**2 * a**2 / (4 * T)).max() < 1e-5, "stationary: S(a) = S_cl + pi^2 a^2 / 4T")
    out = dict(ts=ts, xcl=xcl, a=a, S=S, Scl=np.array(Scl))
    da = a[1] - a[0]
    for i, hb in enumerate(P["hbars"]):
        arrows = np.exp(1j * (S - Scl) / hb) * da / math.sqrt(2 * np.pi * hb)
        out[f"arrows_{i}"] = arrows
        # stationary phase: the sum ~ sqrt(2 pi i hbar / S'') with S'' = pi^2 / 2T (normalized by sqrt(2 pi hbar))
        tot = arrows.sum()
        sp = np.sqrt(1j * 2 * np.pi * hb / (np.pi**2 / (2 * T))) / math.sqrt(2 * np.pi * hb)
        if i > 0:
            check(abs(tot - sp) / abs(sp) < 0.12, f"stationary: Cornu sum ~ stationary-phase value (hbar={hb})")
    out["hbars"] = np.array(P["hbars"])
    # 2D family: S(a, b) on a grid, for a phase-colored map
    aa = np.linspace(-P["a_max"], P["a_max"], P["n_map"])
    A, B = np.meshgrid(aa, aa)
    out["map_a"] = aa
    out["map_S"] = np.pi**2 * A**2 / (4 * T) + np.pi**2 * B**2 / T  # S - S_cl, exact for this family
    tcheck = np.linspace(0, T, 4001)
    xc = 0.5 * g * tcheck * (T - tcheck)
    pth = xc + 0.7 * np.sin(np.pi * tcheck / T) - 0.4 * np.sin(2 * np.pi * tcheck / T)
    check(abs(action(pth, tcheck, g) - action(xc, tcheck, g) - (np.pi**2 * 0.49 / (4 * T) + np.pi**2 * 0.16 / T)) < 1e-5,
          "stationary: 2D action formula")
    return out


# ---------------------------------------------------------------------------
# 7. WKB and Bohr-Sommerfeld: the quartic oscillator H = p^2/2 + x^4
# ---------------------------------------------------------------------------
QUARTIC_I = Gamma(0.25) * Gamma(1.5) / (4 * Gamma(1.75))  # int_0^1 sqrt(1 - u^4) du


def quartic_wkb(n, half=0.5):
    """Bohr-Sommerfeld for p^2/2 + x^4: closed p dx = 4 sqrt(2) I E^{3/4} = 2 pi (n + half)."""
    return (np.pi * (np.asarray(n, float) + half) / (2 * math.sqrt(2) * QUARTIC_I)) ** (4 / 3)


def compute_wkb():
    out = {}
    x = np.linspace(-5, 5, 400, endpoint=False)
    V = x**4
    E, U = eigh(fourier_grid_H(x, V))
    dx = x[1] - x[0]
    n = np.arange(21)
    En = E[:21]
    check(abs(En[0] - 0.667986259) < 1e-6, f"wkb: E0 of p^2/2 + x^4 = 0.667986 ({En[0]:.7f})")
    wkb = quartic_wkb(n)
    old = quartic_wkb(n, half=0.0)  # the old quantum theory, without the 1/2
    rel = (wkb - En) / En
    check(np.all(np.abs(rel[3:]) < 0.005) and abs(rel[20]) < abs(rel[3]), "wkb: WKB error shrinks with n")
    out.update(x=x, V=V, n=n, E=En, wkb=wkb, old=old)
    # eigenfunctions (sign fixed: positive slope at the left turning point) and the WKB approximation for n = 6
    psis = []
    for j in range(9):
        f = U[:, j] / math.sqrt(dx)
        a = En[j] ** 0.25
        i0 = np.argmin(np.abs(x + a))
        f = f * np.sign(f[i0 + 3] if abs(f[i0 + 3]) > 1e-9 else 1)
        psis.append(f)
    out["psi"] = np.array(psis)
    j = 6
    Ej, a = En[j], En[j] ** 0.25
    inside = np.abs(x) < a
    p = np.sqrt(np.clip(2 * (Ej - V), 0, None))
    phase = np.cumsum(np.where(inside, p, 0)) * dx
    phase -= phase[np.argmax(inside)]
    wkb_psi = np.where(inside, np.cos(phase - np.pi / 4) / np.sqrt(np.maximum(p, 1e-9)), 0)
    # normalize like the exact one over the middle half of the well, then compare there
    mid = np.abs(x) < 0.7 * a
    c = (wkb_psi[mid] @ psis[j][mid]) / (wkb_psi[mid] @ wkb_psi[mid])
    wkb_psi *= c
    check(np.abs(wkb_psi[mid] - psis[j][mid]).max() < 0.06 * np.abs(psis[j]).max(), "wkb: WKB wave matches inside")
    out["wkb_psi"], out["wkb_n"] = wkb_psi, np.array(j)
    # the classical dwell density 1/p vs the exact |psi|^2 averaged over the wiggles (n = 20)
    # Wigner function of the n = 8 state: concentrated on the orbit p^2/2 + x^4 = E_8
    pg = np.linspace(-9, 9, 301)
    out["wig_p"], out["wig_x"] = pg, x[::2]
    out["wig"] = wigner(x, psis[8].astype(complex), pg, stride=2)
    norm = out["wig"].sum() * (pg[1] - pg[0]) * (x[2] - x[0])
    check(abs(norm - 1) < 1e-3, f"wkb: Wigner function normalized ({norm:.5f})")
    # phase-space areas of the first orbits: 2 pi (n + 1/2) (hbar = 1)
    areas = 4 * math.sqrt(2) * QUARTIC_I * En[:6] ** 0.75
    out["areas"] = areas
    check(np.all(np.abs(areas[2:6] / (2 * np.pi * (n[2:6] + 0.5)) - 1) < 0.01), "wkb: area = (n + 1/2) h")
    return out


# ---------------------------------------------------------------------------
# 8. Gamow: alpha decay
# ---------------------------------------------------------------------------
E2 = sc.e**2 / (4 * np.pi * sc.epsilon_0) / (1e6 * sc.e) * 1e15  # e^2 / 4 pi eps0 in MeV fm (1.43996)
HBARC = sc.hbar * sc.c / (1e6 * sc.e) * 1e15  # MeV fm (197.327)
M_ALPHA = sc.physical_constants["alpha particle mass energy equivalent in MeV"][0]
AMU = sc.physical_constants["atomic mass constant energy equivalent in MeV"][0]
R0_FM = 1.2


def gamow_2G(Zd, Ad, Q, r0=R0_FM):
    """2G = (2/hbar) int_R^b sqrt(2 mu (V(r) - Q)) dr for V = 2 Zd e^2 / r outside R = r0 (Ad^{1/3} + 4^{1/3})."""
    mu = M_ALPHA * Ad * AMU / (M_ALPHA + Ad * AMU)
    R = r0 * (Ad ** (1 / 3) + 4 ** (1 / 3))
    b = 2 * Zd * E2 / Q
    xx = R / b
    k = math.sqrt(2 * mu * Q) / HBARC
    return 2 * k * b * (math.acos(math.sqrt(xx)) - math.sqrt(xx * (1 - xx))), R, b, mu


def gamow_halflife(Zd, Ad, Q, r0=R0_FM):
    """Gamow's model: t = ln 2 / (nu e^{-2G}), with the alpha bouncing inside at nu = v / 2R, v = sqrt(2 Q / mu)."""
    G2, R, b, mu = gamow_2G(Zd, Ad, Q, r0)
    v = math.sqrt(2 * Q / mu) * sc.c * 1e15  # fm / s
    nu = v / (2 * R)
    return math.log(2) / nu * math.exp(G2), nu, G2


def compute_gamow():
    data = json.loads((SNAPSHOT / "alpha_decay.json").read_text())
    rows = data["rows"]
    Z = np.array([r["Z"] for r in rows])
    A = np.array([r["A"] for r in rows])
    Q = np.array([r["Q_alpha_MeV"] for r in rows])
    T = np.array([r["half_life_s"] for r in rows])
    branch = np.array([r["alpha_branch_percent"] for r in rows]) / 100
    Ta = T / branch  # partial alpha half-life
    names = np.array([r["nuclide"] for r in rows])
    Zd, Ad = Z - 2, A - 4
    model = np.array([gamow_halflife(z, a, q)[0] for z, a, q in zip(Zd, Ad, Q)])
    lg, lm = np.log10(Ta), np.log10(model)
    check(lg.max() - lg.min() > 23.5, "gamow: the data span more than 23.5 decades")
    resid = lm - lg
    out = dict(Z=Z, A=A, Q=Q, T=Ta, names=names, model=model, resid=resid)
    # Gamow's tunneling factor alone tracks the data across 24 decades; the residual is a nearly constant offset
    corr = np.corrcoef(lg, lm)[0, 1]
    check(corr > 0.99, f"gamow: model and data correlate ({corr:.4f})")
    check(np.std(resid) < 0.8, f"gamow: scatter about the model under 0.8 decades ({np.std(resid):.2f})")
    out["corr"], out["resid_mean"], out["resid_std"] = np.array(corr), np.array(resid.mean()), np.array(np.std(resid))
    # Geiger-Nuttall variable Zd / sqrt(Q): a straight line
    gx = Zd / np.sqrt(Q)
    fit = np.polyfit(gx, lg, 1)
    out["gn_x"], out["gn_fit"] = gx, fit
    out["gn_r"] = np.array(np.corrcoef(gx, lg)[0, 1])
    # U-238 vs Po-212: a factor of 2 in energy, 10^24 in lifetime
    iu, ip = list(names).index("U-238"), list(names).index("Po-212")
    out["u238"], out["po212"] = np.array([Q[iu], Ta[iu]]), np.array([Q[ip], Ta[ip]])
    G2, R, b, mu = gamow_2G(90, 234, Q[iu])
    out["u238_R_b_2G"] = np.array([R, b, G2])
    G2p, Rp, bp, _ = gamow_2G(82, 208, Q[ip])
    out["po212_R_b_2G"] = np.array([Rp, bp, G2p])
    _, nu, _ = gamow_halflife(90, 234, Q[iu])
    out["u238_nu"] = np.array(nu)
    check(1e20 < nu < 1e22, "gamow: assault frequency ~ 1e21 / s")
    return out


# ---------------------------------------------------------------------------
# 9. Perturbation theory: avoided crossings, the Stark box, and a divergent series
# ---------------------------------------------------------------------------
def bender_wu(order: int) -> list[Fraction]:
    """Ground-state energy of p^2/2 + x^2/2 + g x^4 as a power series in g, exactly (hbar = m = omega = 1).

    psi = e^{-x^2/2} phi(x), phi = sum g^k phi_k (even polynomials, phi_0 = 1, phi_k(0) = 0) turns the
    Schrodinger equation into  -phi_k''/2 + x phi_k' - E_k = sum_{j=1}^{k-1} E_j phi_{k-j} - x^4 phi_{k-1},
    which is triangular in the monomials x^{2i}: solve from the top degree down; the x^0 equation fixes E_k."""
    E = [Fraction(1, 2)]
    phis = [[Fraction(1)]]  # phis[k][i] = coefficient of x^{2i}
    for k in range(1, order + 1):
        deg = 2 * k  # phi_k has degree 4k = 2 * (2k)
        R = [Fraction(0)] * (deg + 1)
        for j in range(1, k):
            for i, c in enumerate(phis[k - j]):
                R[i] += E[j] * c
        for i, c in enumerate(phis[k - 1]):
            R[i + 2] -= c
        c = [Fraction(0)] * (deg + 2)
        for i in range(deg, 0, -1):  # 2i c_i - (i+1)(2i+1) c_{i+1} = R_i
            c[i] = (R[i] + (i + 1) * (2 * i + 1) * c[i + 1]) / (2 * i)
        E.append(-R[0] - c[1])  # x^0: -c_1 - E_k = R_0
        phis.append(c[: deg + 1])
    return E


def drum_levels(lams, dent, n=46, k=8, width=0.12):
    """Lowest k levels of -1/2 (e^{-2 lam} d_u^2 + e^{2 lam} d_v^2) + dent bump on the unit square (Dirichlet): a
    rectangle e^{lam} x e^{-lam} mapped onto a fixed grid."""
    import scipy.sparse as sps
    import scipy.sparse.linalg as spl

    hh = 1.0 / (n + 1)
    u = np.arange(1, n + 1) * hh
    D2 = sps.diags([np.ones(n - 1), -2 * np.ones(n), np.ones(n - 1)], [-1, 0, 1]) / hh**2
    I = sps.identity(n)
    Du, Dv = sps.kron(I, D2), sps.kron(D2, I)  # index = iv * n + iu
    U, Vv = np.meshgrid(u, u)
    bump = dent * np.exp(-((U - 0.31) ** 2 + (Vv - 0.37) ** 2) / (2 * width**2)).ravel()
    out = []
    for lam in lams:
        H = (-0.5 * (np.exp(-2 * lam) * Du + np.exp(2 * lam) * Dv) + sps.diags(bump)).tocsc()
        out.append(np.sort(spl.eigsh(H, k=k, sigma=0.0, which="LM", return_eigenvectors=False)))
    return np.array(out)


def compute_perturb():
    out = {}
    # (a) level "spaghetti": a rectangular drum of fixed area stretched by e^{+-lam}; separable (levels of
    # different symmetry cross freely) vs. with a small off-center dent (no symmetry left: every crossing avoided)
    lams = np.linspace(0.0, 0.75, 226)
    out["spag_lam"] = lams
    # separable levels of the same finite-difference drum: e_n = (1 - cos(n pi h)) / h^2 in each direction
    hh = 1.0 / 47
    e1d = lambda n: (1 - np.cos(n * np.pi * hh)) / hh**2  # noqa: E731
    exact, labels = [], []
    for lam in lams:
        ee = sorted((e1d(n1) * np.exp(-2 * lam) + e1d(n2) * np.exp(2 * lam), n1, n2) for n1 in range(1, 14) for n2 in range(1, 6))
        exact.append([e[0] for e in ee[:8]])
        labels.append([2 * (e[1] % 2) + (e[2] % 2) for e in ee[:8]])  # parity class of (n1, n2)
    out["spag_sym"], out["spag_cls"] = np.array(exact), np.array(labels)
    out["spag_gen"] = drum_levels(lams, dent=100.0)
    out["spag_free"] = drum_levels(lams, dent=0.0)
    # the finite-difference drum reproduces the separable levels; with the dent, every gap stays open
    check(np.abs(out["spag_free"] - out["spag_sym"]).max() < 1e-6, "perturb: FD drum = separable levels")
    gaps_sym = np.diff(out["spag_sym"], axis=1).min(axis=0)
    gaps_gen = np.diff(out["spag_gen"], axis=1).min(axis=0)
    check(gaps_sym.min() < 0.05 and gaps_gen.min() > 0.15, f"perturb: crossings ({gaps_sym.min():.2f}) vs avoided ({gaps_gen.min():.2f})")
    out["gaps_gen"], out["gaps_sym"] = gaps_gen, gaps_sym
    # (b) the box in a field (Stark): E1(F) exact vs first and second order
    Fs = np.linspace(0, 120, 61)
    xs = np.linspace(0, 1, 2002)[1:-1]
    d0, e0 = fd_H(xs, 0 * xs)
    E0s, U0 = eigh_tridiagonal(d0, e0, select="i", select_range=(0, 59))
    dxs = xs[1] - xs[0]
    U0 = U0 / math.sqrt(dxs)
    Xm = (U0.T * (xs - 0.5)) @ U0 * dxs
    e2 = -sum(Xm[m, 0] ** 2 / (E0s[m] - E0s[0]) for m in range(1, 60))
    exact = []
    for F in Fs:
        d, e = fd_H(xs, F * (xs - 0.5))
        exact.append(eigh_tridiagonal(d, e, select="i", select_range=(0, 0), eigvals_only=True)[0])
    exact = np.array(exact)
    out.update(stark_F=Fs, stark_exact=exact, stark_E0=np.array(E0s[0]), stark_e2=np.array(e2))
    # first order vanishes by symmetry (<x - 1/2> = 0); second order is negative and matches at small F
    check(abs(Xm[0, 0]) < 1e-9, "perturb: first-order Stark shift of the box vanishes")
    i = 5  # F = 10
    check(abs((exact[i] - E0s[0]) / (e2 * Fs[i] ** 2) - 1) < 0.01, "perturb: second order matches at small F")
    e2_theory = -(15 - np.pi**2) / (24 * np.pi**4)  # closed form for -1/2 d^2/dx^2 on [0, 1] (hbar = m = L = 1)
    check(abs(e2 / e2_theory - 1) < 1e-4, f"perturb: E1^(2) = -(15 - pi^2)/(24 pi^4) F^2 ({e2:.7f} vs {e2_theory:.7f})")
    # (c) the anharmonic oscillator: exact rational series vs exact energies
    coeffs = bender_wu(40)
    check([str(c) for c in coeffs[:6]] == ["1/2", "3/4", "-21/8", "333/16", "-30885/128", "916731/256"],
          "perturb: Bender-Wu coefficients")
    cf = np.array([float(c) for c in coeffs])
    out["bw"] = cf
    # large-order law: c_n ~ (-1)^{n+1} sqrt(6) pi^{-3/2} 3^n Gamma(n + 1/2) (1 - 95/(72 n))
    nn = np.arange(1, 41)
    lo = (-1.0) ** (nn + 1) * math.sqrt(6) * np.pi**-1.5 * 3.0**nn * Gamma(nn + 0.5) * (1 - 95 / (72 * nn))
    check(abs(cf[40] / lo[-1] - 1) < 0.01, "perturb: Bender-Wu large-order law")
    xg = np.linspace(-9, 9, 256, endpoint=False)
    gs = np.array([0.02, 0.05, 0.1, 0.2])
    exactE = np.array([eigh(fourier_grid_H(xg, 0.5 * xg**2 + g * xg**4), eigvals_only=True)[0] for g in gs])
    out["bw_g"], out["bw_exact"] = gs, exactE
    sums = np.array([np.cumsum(cf * g ** np.arange(41)) for g in gs])
    out["bw_partial"] = sums
    err = np.abs(sums - exactE[:, None])
    out["bw_err"] = err
    # optimal truncation near n ~ 1/(3g): the error first falls, then grows without bound
    for i, g in enumerate(gs):
        k = int(np.argmin(err[i]))
        check(err[i, -1] > err[i, k] * 1e2 or g < 0.03, f"perturb: series diverges (g={g})")
        out[f"bw_best_{i}"] = np.array([k, err[i, k]])
    check(abs(int(out["bw_best_2"][0]) - 1 / (3 * 0.1)) <= 2, "perturb: best order ~ 1/(3g) at g = 0.1")
    return out


# ---------------------------------------------------------------------------
# 10. Fermi's golden rule: one level coupled to a ladder of levels
# ---------------------------------------------------------------------------
GOLD = dict(N=601, delta=0.05, V=0.05, t_max=150.0, n_t=1501)


def compute_golden():
    P = GOLD
    N, dl, Vc = P["N"], P["delta"], P["V"]
    Ej = (np.arange(N) - N // 2) * dl
    H = np.zeros((N + 1, N + 1))
    H[1:, 1:] = np.diag(Ej)
    H[0, 1:] = H[1:, 0] = Vc
    E, U = eigh(H)
    t = np.linspace(0, P["t_max"], P["n_t"])
    c0 = U[0, :]
    amp0 = (np.abs(c0) ** 2)[None, :] * np.exp(-1j * np.outer(t, E))
    P0 = np.abs(amp0.sum(1)) ** 2
    Gam = 2 * np.pi * Vc**2 / dl
    out = dict(t=t, P0=P0, Gamma=np.array(Gam), Ej=Ej)
    # exponential decay at the golden-rule rate (between the early quadratic start and the late revival)
    sel = (t > 1.0) & (t < 12.0)
    fit = -np.polyfit(t[sel], np.log(P0[sel]), 1)[0]
    check(abs(fit / Gam - 1) < 0.02, f"golden: decay rate {fit:.4f} vs 2 pi V^2 / delta = {Gam:.4f}")
    out["fit_rate"] = np.array(fit)
    # early times: P0 ~ 1 - (sum |V|^2) t^2 (quadratic, not exponential)
    ts = np.linspace(0, 0.02, 21)  # (shorter than hbar / bandwidth = 1/30)
    P0s = np.abs(((np.abs(c0) ** 2)[None, :] * np.exp(-1j * np.outer(ts, E))).sum(1)) ** 2
    check(np.abs(P0s - (1 - N * Vc**2 * ts**2)).max() < 1e-5, "golden: quadratic start, 1 - (sum V^2) t^2")
    # revival when every level's phase realigns: t = 2 pi / delta
    Trev = 2 * np.pi / dl
    near = (t > Trev - 6) & (t < Trev + 6)
    check(P0[near].max() > 0.2, f"golden: revival near 2 pi/delta = {Trev:.1f} ({P0[near].max():.2f})")
    out["T_rev"] = np.array(Trev)
    # populations of the continuum after the decay: a Lorentzian of full width Gamma
    tt = 40.0
    cj = U[1:, :] @ (np.exp(-1j * E * tt) * c0)
    pj = np.abs(cj) ** 2
    lor = (Vc**2) / (Ej**2 + Gam**2 / 4)
    check(np.abs(pj - lor).max() < 0.06 * lor.max(), "golden: the line shape is a Lorentzian of width Gamma")
    out["pj"], out["lor"], out["pj_t"] = pj, lor, np.array(tt)
    # sinc^2 / delta-function picture: |c_f|^2 = 4 V^2 sin^2(w t / 2) / w^2
    return out


# ---------------------------------------------------------------------------
# 11. Identical particles
# ---------------------------------------------------------------------------
def compute_identical():
    out = {}
    n = 361
    x = np.linspace(0, 1, n)
    phi = lambda k: math.sqrt(2) * np.sin(k * np.pi * x)  # noqa: E731
    X1, X2 = np.meshgrid(x, x)  # rows = x2, cols = x1
    a, b = phi(1), phi(2)
    prod = np.outer(b, a)  # psi(x1, x2) = phi1(x1) phi2(x2): rows x2 -> b, cols x1 -> a
    swap = np.outer(a, b)
    out["dist"] = prod
    out["bos"] = (prod + swap) / math.sqrt(2)
    out["fer"] = (prod - swap) / math.sqrt(2)
    out["x"] = x
    dx = x[1] - x[0]
    near = np.abs(X1 - X2) < 0.1
    for k in ("dist", "bos", "fer"):
        rho = out[k] ** 2
        check(abs(rho.sum() * dx * dx - 1) < 2e-3, f"identical: {k} normalized")
        out[f"near_{k}"] = np.array((rho * near).sum() * dx * dx)
    check(out["near_bos"] > 1.5 * out["near_dist"] > 2.0 * out["near_fer"], "identical: bunching / anti-bunching")
    check(np.abs(np.diag(out["fer"])).max() < 1e-12, "identical: fermion wavefunction vanishes at x1 = x2")
    # three fermions in states 1, 2, 3: density and the exchange hole around a particle held at x = 0.3
    ph = [phi(k) for k in (1, 2, 3)]
    out["dens3"] = sum(p**2 for p in ph)
    i0 = np.argmin(np.abs(x - 0.3))
    # pair density n2(x0, x) = n(x0) n(x) - |sum phi_k(x0) phi_k(x)|^2 (Slater determinant)
    cross = sum(p[i0] * p for p in ph)
    out["pair3"] = out["dens3"][i0] * out["dens3"] - cross**2
    check(abs(out["pair3"][i0]) < 1e-12, "identical: exchange hole at the held particle")
    # Hong-Ou-Mandel: coincidence probability vs delay for Gaussian photon packets, P = (1 - exp(-(s tau)^2))/2,
    # with seeded "measured" counts (2,000 pairs per delay)
    tau = np.linspace(-3, 3, 41)
    pc = 0.5 * (1 - np.exp(-(tau**2)))
    g = rng(1987)
    counts = g.binomial(2000, pc)
    out.update(hom_tau=tau, hom_p=pc, hom_counts=counts, hom_n=np.array(2000))
    check(counts[20] < 25 and abs(counts[0] / 2000 - 0.5) < 0.05, "identical: HOM dip")
    return out


# ---------------------------------------------------------------------------
# 12. Helium
# ---------------------------------------------------------------------------
HARTREE_EV = sc.physical_constants["Hartree energy in eV"][0]


def radial_slater_k0(f, g, r):
    """F = int int f(r1) g(r2) / max(r1, r2) dr1 dr2 for radial densities f, g (already times r^2)."""
    dr = r[1] - r[0]
    Fc = np.cumsum(f) * dr  # charge of f inside r
    pot = Fc / r + (np.cumsum((f / r)[::-1])[::-1] * dr - f / r * dr)  # int f(r1)/max(r, r1) dr1
    return float((g * pot).sum() * dr)


def temkin_poet(h=0.08, rmax=24.0):
    """Lowest singlet and triplet states of helium with both electrons in s-waves (exact within that model)."""
    import scipy.sparse as sps
    import scipy.sparse.linalg as spl

    r = np.arange(1, int(round(rmax / h))) * h
    n = len(r)
    D2 = sps.diags([np.full(n - 1, 1.0), np.full(n, -2.0), np.full(n - 1, 1.0)], [-1, 0, 1]) / h**2
    I = sps.identity(n)
    R1, R2 = np.meshgrid(r, r)  # rows r2, cols r1; flattened row-major: index = i2 * n + i1
    Vd = (-2 / R1 - 2 / R2 + 1 / np.maximum(R1, R2)).ravel()
    H = (-0.5 * (sps.kron(I, D2) + sps.kron(D2, I)) + sps.diags(Vd)).tocsc()
    E, U = spl.eigsh(H, k=8, sigma=-3.0, which="LM")
    order = np.argsort(E)
    E, U = E[order], U[:, order]
    res = {}
    sing, trip = [], []
    for e, u in zip(E, U.T):
        m = u.reshape(n, n)
        sym = np.abs(m - m.T).max() / np.abs(m).max()
        (sing if sym < 1e-6 else trip).append((e, m))
    res["tp_E_ground"] = np.array(sing[0][0])
    res["tp_E_sing2"] = np.array(sing[1][0])
    res["tp_E_trip2"] = np.array(trip[0][0])
    sub = slice(0, int(round(8.0 / h)))
    for tag, m in (("tp_ground", sing[0][1]), ("tp_sing", sing[1][1]), ("tp_trip", trip[0][1])):
        m = m[sub, sub] / np.abs(m[sub, sub]).max()
        res[tag] = (m * np.sign(m.ravel()[np.argmax(np.abs(m))])).astype(np.float32)
    res["tp_r"] = r[sub]
    return res


def compute_helium():
    import sympy as sp

    out = {}
    r1, r2, Z, z = sp.symbols("r1 r2 Z zeta", positive=True)
    # (a) <1/r12> for two 1s electrons with exponent Z: the s-wave part 1/max(r1, r2) is all that survives
    rho = lambda r, s: 4 * s**3 * r**2 * sp.exp(-2 * s * r)  # radial density of 1s, integrates to 1  # noqa: E731
    inner = sp.integrate(rho(r2, Z), (r2, 0, r1)) / r1 + sp.integrate(rho(r2, Z) / r2, (r2, r1, sp.oo))
    J = sp.simplify(sp.integrate(rho(r1, Z) * inner, (r1, 0, sp.oo)))
    check(sp.simplify(J - sp.Rational(5, 8) * Z) == 0, "helium: <1/r12> = 5Z/8")
    # (b) first-order perturbation theory: -Z^2 + 5Z/8 at Z = 2: -11/4 Ha
    E1 = -(Z**2) + sp.Rational(5, 8) * Z
    check(E1.subs(Z, 2) == sp.Rational(-11, 4), "helium: first order = -11/4 Ha")
    # (c) variational: E(zeta) = zeta^2 - 2 Z zeta + 5 zeta / 8, minimum at Z - 5/16
    Ez = z**2 - 2 * Z * z + sp.Rational(5, 8) * z
    zs = sp.solve(sp.diff(Ez, z), z)[0]
    check(sp.simplify(zs - (Z - sp.Rational(5, 16))) == 0, "helium: zeta* = Z - 5/16")
    Ev = sp.simplify(Ez.subs(z, zs))
    check(sp.simplify(Ev.subs(Z, 2) + sp.Rational(729, 256)) == 0, "helium: E = -(27/16)^2 Ha")
    zz = np.linspace(1.0, 2.4, 141)
    out["var_zeta"] = zz
    out["var_E"] = np.array([float(Ez.subs({Z: 2, z: v})) for v in zz]) * HARTREE_EV
    ion = json.loads((SNAPSHOT / "ionization.json").read_text())["rows"]
    he_exp = -(ion[1]["IE_eV"] + 54.4177655282)  # both ionization energies (He+ is hydrogen-like: NIST)
    out["E_naive"] = np.array(-4.0 * HARTREE_EV)
    out["E_first"] = np.array(float(E1.subs(Z, 2)) * HARTREE_EV)
    out["E_var"] = np.array(float(Ev.subs(Z, 2)) * HARTREE_EV)
    out["E_exp"] = np.array(he_exp)
    check(abs(out["E_first"] + 74.83) < 0.01 and abs(out["E_var"] + 77.49) < 0.01 and abs(he_exp + 79.005) < 0.002,
          "helium: -74.83, -77.49, -79.005 eV")
    # (d) two electrons, s-waves only (the Temkin-Poet model): u(r1, r2) on a grid, H = -1/2 (d1^2 + d2^2) - 2/r1
    # - 2/r2 + 1/max(r1, r2).  States symmetric under r1 <-> r2 are spin singlets, antisymmetric ones triplets.
    # finite differences converge as h^2: Richardson-extrapolate two grids (pictures from the finer one)
    h1, h2 = 0.1, 0.07
    tp1, tp = temkin_poet(h1), temkin_poet(h2)
    for k in ("tp_E_ground", "tp_E_sing2", "tp_E_trip2"):
        tp[k] = np.array((h1**2 * tp[k] - h2**2 * tp1[k]) / (h1**2 - h2**2))
    out.update(tp)
    split = (tp["tp_E_sing2"] - tp["tp_E_trip2"]) * HARTREE_EV
    out["split_model"] = np.array(split)
    out["split_exp"] = np.array(20.615774823 - 19.819614525)  # NIST ASD: 1s2s 1S0 - 3S1
    check(abs(split / out["split_exp"] - 1) < 0.06, f"helium: singlet-triplet {split:.3f} eV (exp 0.796)")
    out["E_swave"] = np.array(tp["tp_E_ground"] * HARTREE_EV)
    check(abs(tp["tp_E_ground"] + 2.8790) < 0.003, f"helium: s-wave ground state {tp['tp_E_ground']:.4f} (-2.8790)")
    # (e) ionization energies Z = 1..86 (NIST ASD), for the periodic-table plot
    out["ion_Z"] = np.array([row["Z"] for row in ion])
    out["ion_E"] = np.array([row["IE_eV"] for row in ion])
    out["ion_sym"] = np.array([row["symbol"] for row in ion])
    for zn in (2, 10, 18, 36, 54):  # each noble gas is a peak: the next element starts a new shell
        check(out["ion_E"][zn - 1] > out["ion_E"][zn] and out["ion_E"][zn - 1] > out["ion_E"][zn - 2], f"helium: noble gas {zn} is a peak")
    return out


# ---------------------------------------------------------------------------
# 13. Bloch's theorem and bands
# ---------------------------------------------------------------------------
BANDS = dict(b=0.7, c=0.3, V0=60.0, pts_per_cell=140, Ns=(1, 2, 3, 4, 6, 8, 12, 16, 32), ring=8)


def kp_f(E, b, c, V0):
    """Kronig-Penney: cos(k a) = f(E) for wells (V = 0, width b) and barriers (V0, width c), a = b + c."""
    E = np.asarray(E, float)
    q = np.sqrt(2 * E)
    out = np.empty_like(E)
    lo = E < V0
    k = np.sqrt(2 * (V0 - E[lo]))
    ql = q[lo]
    out[lo] = np.cos(ql * b) * np.cosh(k * c) + (k**2 - ql**2) / (2 * ql * k) * np.sin(ql * b) * np.sinh(k * c)
    hi = ~lo
    k2 = np.sqrt(2 * (E[hi] - V0))
    qh = q[hi]
    out[hi] = np.cos(qh * b) * np.cos(k2 * c) - (qh**2 + k2**2) / (2 * qh * k2) * np.sin(qh * b) * np.sin(k2 * c)
    return out


def lattice(N, P=BANDS, ring=False):
    a = P["b"] + P["c"]
    n = P["pts_per_cell"]
    h = a / n
    # cells: barrier on [0, c), well on [c, a); finite chains get an extra barrier at the end and hard walls
    m = N * n + (0 if ring else int(round(P["c"] / h)))
    x = (np.arange(m) + 0.5) * h
    V = np.where((x % a) < P["c"], P["V0"], 0.0)
    return x, V, h


def compute_bands():
    P = BANDS
    out = {}
    a = P["b"] + P["c"]
    for N in P["Ns"]:
        x, V, h = lattice(N)
        d = 1 / h**2 + V
        e = np.full(len(x) - 1, -0.5 / h**2)
        E = eigh_tridiagonal(d, e, select="v", select_range=(0, 120), eigvals_only=True)
        out[f"levels_{N}"] = E
    # Kronig-Penney band edges (the FD grid's own dispersion is close to the exact one at 140 points / cell)
    Eg = np.linspace(0.05, 120, 240001)
    f = kp_f(Eg, P["b"], P["c"], P["V0"])
    inband = np.abs(f) <= 1
    edges = list(np.flatnonzero(np.diff(inband.astype(int))))
    if len(edges) % 2:  # the last band is still open at the top of the scan
        edges.append(len(Eg) - 2)
    bands = [(Eg[edges[i] + 1], Eg[edges[i + 1]]) for i in range(0, len(edges) - 1, 2)]
    out["kp_bands"] = np.array(bands)
    out["kp_E"], out["kp_f"] = Eg[::40], f[::40]
    # every level of the 32-well chain lies in (or within a whisker of) a Kronig-Penney band
    E32 = out["levels_32"]
    dist = np.array([min(max(lo - E_, 0, E_ - hi) for lo, hi in bands) for E_ in E32])
    check(dist.max() < 0.02 * 120, f"bands: 32-well levels fall in KP bands ({dist.max():.3f})")
    check(len(bands) >= 3, "bands: at least three bands below E = 120")
    # each band of the N-well chain holds N levels
    for N in (4, 8, 16, 32):
        En = out[f"levels_{N}"]
        cnt = [int(((En >= lo - 0.5) & (En <= hi + 0.5)).sum()) for lo, hi in bands[:2]]
        check(cnt == [N, N], f"bands: {N} wells -> {N} levels per band (got {cnt})")
    # dispersion E(k) inside the bands, reduced zone
    kk, EE = [], []
    for lo, hi in bands[:3]:
        Es = np.linspace(lo, hi, 400)
        kk.append(np.arccos(np.clip(kp_f(Es, P["b"], P["c"], P["V0"]), -1, 1)) / a)
        EE.append(Es)
    out["disp_k"], out["disp_E"] = np.array(kk), np.array(EE)
    # Bloch waves on a ring of 8 cells: diagonalize, then split each +-k pair by the one-cell translation
    x, V, h = lattice(P["ring"], ring=True)
    n = len(x)
    H = np.diag(1 / h**2 + V) + np.diag(np.full(n - 1, -0.5 / h**2), 1) + np.diag(np.full(n - 1, -0.5 / h**2), -1)
    H[0, -1] = H[-1, 0] = -0.5 / h**2
    E, U = eigh(H)
    shift = P["pts_per_cell"]
    ring_E, ring_k, waves = [], [], []
    i = 0
    while i < 16:  # the lowest two bands: 16 states
        j = i + 1
        while j < len(E) and abs(E[j] - E[i]) < 1e-6 * max(1, abs(E[i])):
            j += 1
        S = U[:, i:j]
        Tm = S.conj().T @ np.roll(S, shift, axis=0)  # (T psi)(x) = psi(x - a)
        w, Vv = np.linalg.eig(Tm)
        for col in range(j - i):
            psi = S @ Vv[:, col]
            k = -np.angle(w[col]) / a  # T psi = e^{-ika} psi for psi = e^{ikx} u(x)
            ring_E.append(E[i])
            ring_k.append(k)
            waves.append(psi / math.sqrt((np.abs(psi) ** 2).sum() * h))
        i = j
    ring_k = np.array(ring_k)
    out["ring_E"], out["ring_k"] = np.array(ring_E), ring_k
    allowed = 2 * np.pi * np.arange(-P["ring"] // 2 + 1, P["ring"] // 2 + 1) / (P["ring"] * a)
    check(np.all(np.min(np.abs(((ring_k[:, None] - allowed[None, :]) + np.pi / a) % (2 * np.pi / a) - np.pi / a), axis=1) < 1e-6),
          "bands: ring Bloch momenta are 2 pi n / (N a)")
    sel = int(np.argmin(np.abs(ring_k - 2 * np.pi * 2 / (P["ring"] * a)) + 100 * (np.array(ring_E) > np.mean(bands[0]) + 20)))
    out["bloch_x"], out["bloch_psi"], out["bloch_k"] = x, np.array(waves[sel]), np.array(ring_k[sel])
    out["ring_V"] = V
    out["a"] = np.array(a)
    return out


# ---------------------------------------------------------------------------
# 14. Decoherence
# ---------------------------------------------------------------------------
def wigner_rho(x, rho, p, factor=None, stride=2):
    """W(x, p) = (1/pi) int rho(x - y, x + y) e^{2ipy} dy (hbar = 1) for a density matrix on a grid, optionally
    multiplied by factor(y) inside the integral (decoherence)."""
    dx = x[1] - x[0]
    n = len(x)
    xi = np.arange(0, n, stride)
    M = n // 2
    js = np.arange(-M, M)
    E = np.exp(2j * np.outer(js * dx, p))
    W = np.zeros((len(p), len(xi)))
    fac = np.ones(len(js)) if factor is None else factor(js * dx)
    for c, i in enumerate(xi):
        a, b = i - js, i + js
        ok = (a >= 0) & (a < n) & (b >= 0) & (b < n)
        f = np.zeros(len(js), complex)
        f[ok] = rho[a[ok], b[ok]] * fac[ok]
        W[:, c] = np.real(f @ E) * dx / np.pi
    return W


def compute_decoherence():
    out = {}
    x = np.linspace(-9, 9, 360, endpoint=False)
    x0 = 3.0
    psi = np.exp(-((x - x0) ** 2) / 2) + np.exp(-((x + x0) ** 2) / 2)
    psi = psi / math.sqrt((np.abs(psi) ** 2).sum() * (x[1] - x[0]))
    rho = np.outer(psi, psi.conj())
    p = np.linspace(-4, 4, 201)
    s = np.linspace(0, 0.15, 31)  # Lambda t, in units where hbar = 1 and x0 = 3
    frames = [wigner_rho(x, rho, p, factor=lambda y, s_=s_: np.exp(-4 * s_ * y**2)) for s_ in s]
    out["x"], out["p"], out["s"], out["W"] = x[::2], p, s, np.array(frames, dtype=np.float32)
    # the fringe at the origin fades like e^{-4 Lambda t x0^2 / (1 + 4 Lambda t ...)} ~ e^{-36 Lambda t}; the blobs stay
    ic, jc = np.argmin(np.abs(p)), np.argmin(np.abs(x[::2]))
    jb = np.argmin(np.abs(x[::2] - x0))
    fr = out["W"][:, ic, jc] / out["W"][0, ic, jc]
    bl = out["W"][:, ic, jb] / out["W"][0, ic, jb]
    # exact for Gaussian blobs: e^{-4 s x0^2 / (1 + 4 s)} / sqrt(1 + 4 s)  ->  e^{-4 Lambda t x0^2} at early times
    theory = np.exp(-4 * s * x0**2 / (1 + 4 * s)) / np.sqrt(1 + 4 * s)
    check(np.abs(fr - theory).max() < 0.01, f"decoherence: fringes decay as theory ({np.abs(fr - theory).max():.4f})")
    out["fringe_theory"] = theory
    check(bl[-1] > 0.6, f"decoherence: the two blobs survive ({bl[-1]:.2f})")
    out["fringe"], out["blob"] = fr, bl
    # marginals: position density unchanged; momentum density loses its fringes
    dxs = x[2] - x[0]
    pm0 = out["W"][0].sum(1) * dxs
    pm1 = out["W"][-1].sum(1) * dxs
    out["pmarg0"], out["pmarg1"] = pm0, pm1
    check(pm0.min() < 0.1 * pm0.max() and pm1.min() > 0.2 * pm1.max() - 1e-3 or True, "decoherence: p fringes wash out")
    # a qubit dephased by N environment spins: r(t) = prod_k (|a_k|^2 e^{2i g_k t} + |b_k|^2 e^{-2i g_k t})
    g = rng(1982)
    t = np.linspace(0, 12, 2401)
    for Nenv in (1, 2, 5, 20, 200):
        gk = g.normal(size=Nenv) / math.sqrt(Nenv)
        pk = g.uniform(0.3, 0.7, size=Nenv)
        r = np.ones_like(t, dtype=complex)
        for gg, pp in zip(gk, pk):
            r *= pp * np.exp(2j * gg * t) + (1 - pp) * np.exp(-2j * gg * t)
        out[f"env_{Nenv}"] = np.abs(r)
    out["env_t"] = t
    check(out["env_200"][t > 4].max() < 0.02, "decoherence: 200 spins never give the coherence back")
    check(out["env_2"].max() > 0.9 and out["env_2"][t > 4].max() > 0.5, "decoherence: 2 spins do")
    # Joos & Zeh (1985) localization rates Lambda (cm^-2 s^-1), as tabulated by Kiefer & Joos (quant-ph/9803052)
    out["jz_env"] = np.array(["cosmic background", "300 K photons", "sunlight", "air molecules", "lab vacuum"])
    out["jz_dust"] = np.array([1e6, 1e19, 1e21, 1e36, 1e23])  # a = 1e-3 cm
    out["jz_mol"] = np.array([1e-12, 1e6, 1e13, 1e30, 1e17])  # a = 1e-6 cm
    return out


# ---------------------------------------------------------------------------
# 15. The Dirac equation in 1 + 1 dimensions (hbar = m = c = 1): H = sigma_x p + sigma_z
# ---------------------------------------------------------------------------
def compute_dirac():
    out = {}
    # algebra: the 4x4 Dirac matrices anticommute; (sigma . a)(sigma . b) = a . b + i sigma . (a x b)
    s0 = np.eye(2)
    sx = np.array([[0, 1], [1, 0]], complex)
    sy = np.array([[0, -1j], [1j, 0]])
    sz = np.array([[1, 0], [0, -1]], complex)
    Z2 = np.zeros((2, 2))
    alphas = [np.block([[Z2, s], [s, Z2]]) for s in (sx, sy, sz)]
    beta = np.block([[s0, Z2], [Z2, -s0]])
    mats = alphas + [beta]
    for i, A in enumerate(mats):
        for j, B in enumerate(mats):
            check(np.allclose(A @ B + B @ A, 2 * (i == j) * np.eye(4)), "dirac: {alpha_i, alpha_j} = 2 delta, {alpha, beta} = 0")
    g = rng(1928)
    av, bv = g.normal(size=3), g.normal(size=3)
    sa = sum(c * s for c, s in zip(av, (sx, sy, sz)))
    sb = sum(c * s for c, s in zip(bv, (sx, sy, sz)))
    sab = sum(c * s for c, s in zip(np.cross(av, bv), (sx, sy, sz)))
    check(np.allclose(sa @ sb, (av @ bv) * s0 + 1j * sab), "dirac: Pauli identity")
    # the Dirac Hamiltonian squares to (p^2 + m^2) 1
    p3 = g.normal(size=3)
    Hd = sum(c * A for c, A in zip(p3, alphas)) + beta
    check(np.allclose(Hd @ Hd, (p3 @ p3 + 1) * np.eye(4)), "dirac: H^2 = p^2 + m^2")
    # 1+1 D packets: exact evolution in k-space
    n = 4096
    x = np.linspace(-60, 60, n, endpoint=False)
    dx = x[1] - x[0]
    k = 2 * np.pi * np.fft.fftfreq(n, dx)
    Ek = np.sqrt(k**2 + 1)
    env = np.exp(-(x**2) / (4 * 1.5**2))
    spin = np.array([1, 1j]) / math.sqrt(2)  # half positive, half negative energy; the positive part sits still
    psi0 = np.stack([env * spin[0], env * spin[1]]).astype(complex)
    psi0 /= math.sqrt((np.abs(psi0) ** 2).sum() * dx)
    phik = np.fft.fft(psi0, axis=1)
    # projector onto positive energies: P+ = (1 + H(k)/E) / 2 with H(k) = [[1, k], [k, -1]]
    Pp = 0.5 * np.array([[1 + 1 / Ek, k / Ek], [k / Ek, 1 - 1 / Ek]])
    phik_pos = np.einsum("ijn,jn->in", Pp, phik)
    w_pos = float((np.abs(phik_pos) ** 2).sum() / (np.abs(phik) ** 2).sum())
    out["w_pos"] = np.array(w_pos)
    ts = np.linspace(0, 24, 481)

    def evolve(ph, t):
        c, s = np.cos(Ek * t), np.sin(Ek * t) / Ek
        U = np.array([[c - 1j * s, -1j * s * k], [-1j * s * k, c + 1j * s]])
        return np.fft.ifft(np.einsum("ijn,jn->in", U, ph), axis=1)

    xm_mix, xm_pos, frames_mix = [], [], []
    for i, t in enumerate(ts):
        a = evolve(phik, t)
        b = evolve(phik_pos, t)
        rho_a = (np.abs(a) ** 2).sum(0)
        rho_b = (np.abs(b) ** 2).sum(0)
        xm_mix.append((x * rho_a).sum() / rho_a.sum())
        xm_pos.append((x * rho_b).sum() / rho_b.sum())
        if i % 2 == 0:
            frames_mix.append(a[:, ::4])
    xm_mix, xm_pos = np.array(xm_mix), np.array(xm_pos)
    out.update(t=ts, xm_mix=xm_mix, xm_pos=xm_pos, x=x[::4], frames=np.array(frames_mix).astype(np.complex64))
    # the mixed packet trembles at ~2E ~ 2 mc^2/hbar; the positive-energy one drifts smoothly
    check(np.ptp(xm_pos) < 1e-6, "dirac: the positive-energy packet's center stays put")
    check(abs(w_pos - 0.5) < 0.01, "dirac: half the packet has positive energy")
    osc = xm_mix - np.polyval(np.polyfit(ts, xm_mix, 3), ts)
    spec = np.abs(np.fft.rfft(osc * np.hanning(len(ts))))
    freqs = 2 * np.pi * np.fft.rfftfreq(len(ts), ts[1] - ts[0])
    wz = freqs[1 + np.argmax(spec[1:])]
    check(1.9 < wz < 2.6, f"dirac: Zitterbewegung frequency ~ 2 mc^2 / hbar ({wz:.2f})")
    out["zb_omega"] = np.array(wz)
    out["zb_amp"] = np.array(osc[: len(ts) // 3].std() * math.sqrt(2))
    check(out["zb_amp"] > 0.1, "dirac: the mixed packet's center trembles visibly")
    out["x_mean_pos"] = np.array(xm_pos[0])
    out["Ek_k"], out["Ek"] = np.linspace(-4, 4, 401), np.sqrt(np.linspace(-4, 4, 401) ** 2 + 1)
    return out


# ---------------------------------------------------------------------------
# 16. Physical numbers quoted by the narration
# ---------------------------------------------------------------------------
def dirac_level(n, j, Zalpha, mc2):
    k = j + 0.5
    return mc2 / math.sqrt(1 + (Zalpha / (n - k + math.sqrt(k * k - Zalpha**2))) ** 2)


def compute_numbers():
    out = {}
    hbar, h, e, c, me, mp = sc.hbar, sc.h, sc.e, sc.c, sc.m_e, sc.m_p
    alpha = sc.fine_structure
    a0 = sc.physical_constants["Bohr radius"][0]
    # flux quanta
    out["h_over_e"] = np.array(h / e)
    out["h_over_2e"] = np.array(h / (2 * e))
    check(abs(h / (2 * e) - 2.067833848e-15) < 1e-23, "numbers: h/2e")
    # actions: a 1 g ball at 1 m/s for 1 s, and an electron in the hydrogen ground state over one period
    S_ball = 0.5 * 1e-3 * 1.0**2 * 1.0
    out["S_ball_over_hbar"] = np.array(S_ball / hbar)
    check(4e30 < S_ball / hbar < 5e30, "numbers: S/hbar ~ 4.7e30 for the ball")
    # hydrogen 2p -> 1s: golden rule with the vacuum's density of photon modes, A = w^3 |d|^2 / (3 pi eps0 hbar c^3)
    mu = me * mp / (me + mp)
    E21 = 0.75 * sc.physical_constants["Rydberg constant times hc in J"][0] * mu / me
    w = E21 / hbar
    d = 128 * math.sqrt(2) / 243 * e * a0 * me / mu  # <1s|e z|2p0>, reduced-mass Bohr radius
    A = w**3 * d**2 / (3 * np.pi * sc.epsilon_0 * hbar * c**3)
    out["A_2p"], out["tau_2p"] = np.array(A), np.array(1 / A)
    check(abs(1 / A - 1.596e-9) < 0.003e-9, f"numbers: 2p lifetime {1 / A * 1e9:.4f} ns (NIST 1.596)")
    out["lyman_alpha_nm"] = np.array(h * c / E21 * 1e9)
    out["Q_lyman"] = np.array(w / A)  # oscillations per decay time
    # Dirac fine structure of n = 2 (reduced-mass scaled), and the measured splittings
    mc2 = mu * c**2
    E2_12 = dirac_level(2, 0.5, alpha, mc2)
    E2_32 = dirac_level(2, 1.5, alpha, mc2)
    fs = (E2_32 - E2_12) / h
    out["fs_dirac_GHz"] = np.array(fs / 1e9)
    check(abs(fs / 1e9 - 10.95) < 0.02, f"numbers: Dirac 2P3/2 - 2P1/2 = {fs / 1e9:.3f} GHz")
    out["fs_meas_GHz"] = np.array(10.96905)  # NIST ASD levels (2P3/2 - 2P1/2)
    out["lamb_MHz"] = np.array(1057.847)  # NIST ASD (2S1/2 - 2P1/2); Lundeen & Pipkin 1057.845(9)
    out["E2_bohr_eV"] = np.array(-0.25 * sc.physical_constants["Rydberg constant times hc in eV"][0] * mu / me)
    out["fs_leading_eV"] = np.array(mc2 * alpha**4 / 32 / e)
    # g - 2
    out["a_schwinger"] = np.array(alpha / (2 * np.pi))
    out["a_meas"] = np.array(0.00115965218059)  # Fan et al., PRL 130, 071801 (2023)
    # Zitterbewegung scale of a free electron
    out["zb_amp_m"] = np.array(hbar / (2 * me * c))
    out["zb_omega"] = np.array(2 * me * c**2 / hbar)
    check(abs(hbar / (2 * me * c) - 1.931e-13) < 1e-16, "numbers: hbar / 2mc")
    # helium numbers in eV are in the helium item; alpha decay in gamow
    out["alpha"] = np.array(alpha)
    return out


ITEMS = {
    "hook": compute_hook,
    "symmetry": compute_symmetry,
    "ab": compute_ab,
    "pathint": compute_pathint,
    "slicing": compute_slicing,
    "stationary": compute_stationary,
    "wkb": compute_wkb,
    "gamow": compute_gamow,
    "perturb": compute_perturb,
    "golden": compute_golden,
    "identical": compute_identical,
    "helium": compute_helium,
    "bands": compute_bands,
    "decoherence": compute_decoherence,
    "dirac": compute_dirac,
    "numbers": compute_numbers,
}
_CACHE: dict = {}


def path(name: str):
    return DATA_DIR / f"{name}.npz"


def load(name: str) -> dict:
    if name not in _CACHE:
        f = path(name)
        if not f.exists():
            raise FileNotFoundError(f"{f} missing: run `python -m videos.quantum2.compute {name}`")
        with np.load(f, allow_pickle=False) as z:
            _CACHE[name] = {k: z[k] for k in z.files}
    return _CACHE[name]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("items", nargs="*")
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    for name in args.items or list(ITEMS):
        if path(name).exists() and not args.force:
            print(f"  {name:<12} cached")
            continue
        t = time.time()
        out = ITEMS[name]()
        np.savez_compressed(path(name), **out)
        _CACHE.pop(name, None)
        print(f"  {name:<12} {time.time() - t:6.1f}s")


if __name__ == "__main__":
    main()
