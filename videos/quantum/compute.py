"""Precompute every simulation shown in the quantum-mechanics video.

    python -m videos.quantum.compute                 # everything missing (~15 min on 4 cores)
    python -m videos.quantum.compute slits tunnel    # specific items
    python -m videos.quantum.compute --force         # recompute

Results are cached in ``.cache/quantum/<name>.npz`` (big movies as ``.npy`` next to them, memory-mapped);
scenes call ``load(name)`` and never solve anything themselves.  Nothing here is a cartoon: every wave is a
numerical solution of the Schrodinger equation (split-operator FFT, exact eigen-expansions, finite-difference
eigenproblems), every histogram is counted from seeded samples (PCG64) of the Born rule, and every number the
narration quotes is computed here and, where theory predicts it, asserted against that prediction.

Units: hbar = m = 1 in every simulation (atomic units, a0 = 1 Hartree = 1, for hydrogen), unless an item says
otherwise; physical numbers (electrons in boxes, hydrogen's spectrum) use CODATA 2022 via scipy.constants.

Items:
    slits       2D double slit: a wave packet through two slits, the arrival density on a screen, and single-slit
                runs for comparison; detection events sampled from the arrival density
    packet      a free Gaussian packet: exact evolution, width vs the spreading law, phase vs group velocity
    carpet      a packet in an infinite well: exact eigen-expansion, revivals, the quantum carpet
    fd          the Hamiltonian as a matrix: finite-difference eigenvalues and eigenvectors vs the exact box
    measure     energy measurements on the carpet's packet: 2,000 Born-rule samples vs |c_n|^2
    uncert      sigma_x * sigma_p for many states, computed on a grid with FFTs
    tunnel      a packet hitting a rectangular barrier: split-operator, transmitted probability vs theory
    oscillator  the harmonic oscillator: FD spectrum, a coherent state and a squeezed state (split-operator),
                Wigner functions (coherent, number states, a cat), the classically forbidden fraction
    hydrogen    radial FD spectrum, shooting curves, radial densities, the Balmer and Lyman lines, orbital renders,
                and the 1s + 2p superposition whose charge sloshes at the Lyman-alpha frequency
    spin        Stern-Gerlach: classical vs quantum deflections; sequential measurements at angle theta
    bell        CHSH: 10^5 singlet pairs per setting sampled from the Born rule, and a local hidden-variable model
    pair        two particles on a line: a product state and an entangled state on the (x1, x2) plane
    numbers     physical numbers the narration quotes (de Broglie wavelengths, an electron in a 1 nm box, ...)
    extras      same density / different phase; heat vs Schrodinger; Taylor translation; the barrier's stationary
                scattering state; momentum content of box states
"""

from __future__ import annotations

import argparse
import math
import time
from concurrent.futures import ProcessPoolExecutor

import numpy as np
import scipy.constants as sc
import scipy.fft as sfft
from scipy.linalg import eigh_tridiagonal
from scipy.special import eval_genlaguerre, eval_hermite, factorial, sph_harm_y, erfc

from explainer.tts import REPO_ROOT

from .colormap import BG, hue_rgb, to_uint8

DATA_DIR = REPO_ROOT / ".cache" / "quantum"
WORKERS = 4


def rng(seed: int) -> np.random.Generator:
    return np.random.Generator(np.random.PCG64(seed))


def fft(a, axes=None):
    return sfft.fftn(a, axes=axes, workers=WORKERS)


def ifft(a, axes=None):
    return sfft.ifftn(a, axes=axes, workers=WORKERS)


def trapz(y, x=None, dx=1.0, axis=-1):
    return np.trapezoid(y, x=x, dx=dx, axis=axis)


def gaussian(x, x0, sigma, k0=0.0):
    """Normalized Gaussian packet: |psi|^2 has standard deviation sigma; mean momentum k0 (hbar = 1)."""
    return (2 * np.pi * sigma**2) ** -0.25 * np.exp(-((x - x0) ** 2) / (4 * sigma**2) + 1j * k0 * x)


def moments(x, psi):
    """<x>, sigma_x, <p>, sigma_p of a 1D wavefunction on a uniform grid (momenta via FFT, hbar = 1)."""
    dx = x[1] - x[0]
    rho = np.abs(psi) ** 2
    norm = rho.sum() * dx
    mx = (x * rho).sum() * dx / norm
    sx = math.sqrt(max(((x - mx) ** 2 * rho).sum() * dx / norm, 0))
    k = 2 * np.pi * np.fft.fftfreq(len(x), dx)
    phik = np.abs(np.fft.fft(psi)) ** 2
    mk = (k * phik).sum() / phik.sum()
    sk = math.sqrt(max(((k - mk) ** 2 * phik).sum() / phik.sum(), 0))
    return mx, sx, mk, sk


# ---------------------------------------------------------------------------
# Split-operator (Strang) propagator: exp(-iV dt/2) exp(-i k^2 dt/2) exp(-iV dt/2); exactly unitary for real V.
# Absorbing boundaries are an imaginary potential -iW, which damps exactly where it is nonzero.
# ---------------------------------------------------------------------------
class SplitOperator:
    def __init__(self, V, k2, dt, W=None):
        V = np.asarray(V, dtype=np.float64)
        W = np.zeros_like(V) if W is None else np.asarray(W, dtype=np.float64)
        self.half_v = np.exp((-1j * V - W) * dt / 2).astype(np.complex64 if V.ndim == 2 else np.complex128)
        self.kin = np.exp(-1j * k2 * dt / 2).astype(self.half_v.dtype)
        self.dt = dt

    def step(self, psi, n=1):
        for _ in range(n):
            psi = psi * self.half_v
            psi = ifft(fft(psi) * self.kin)
            psi = psi * self.half_v
        return psi


def absorber(x, lo, hi, width, strength):
    """Imaginary potential: 0 on [lo, hi], rising quadratically over ``width`` outside it."""
    d = np.maximum(lo - x, 0) + np.maximum(x - hi, 0)
    return strength * np.clip(d / width, 0, 1) ** 2


# ---------------------------------------------------------------------------
# 1. The double slit (2D)
# ---------------------------------------------------------------------------
SLIT = dict(N=1024, k0=0.75, x0=180.0, sx=30.0, sy=110.0, wall=(320.0, 328.0), V0=3.0, d=60.0, w=20.0,
            screen=840.0, dt=0.5, t_end=1500.0, every=4, crop_x=(120, 900), crop_y=(-300, 300))
# (norms are logged every `every` steps; movie frames every 2 * every steps = 4 time units)
FRAME_SCALE = 100.0
TONOMURA = [10, 100, 3000, 20000, 70000]  # electrons in the five frames of Tonomura et al. (1989)


def slit_potential(which="both"):
    p = SLIT
    N = p["N"]
    x = np.arange(N, dtype=np.float64)
    y = np.arange(N, dtype=np.float64) - N / 2
    X, Y = np.meshgrid(x, y)  # rows = y, cols = x
    V = np.zeros((N, N))
    wall = (X >= p["wall"][0]) & (X < p["wall"][1])
    V[wall] = p["V0"]
    for sgn, name in ((+1, "top"), (-1, "bottom")):
        if which in ("both", name):
            open_ = wall & (np.abs(Y - sgn * p["d"] / 2) < p["w"] / 2)
            V[open_] = 0.0
    W = absorber(X, 40, 900, 80, 0.25) + absorber(Y, -400, 400, 90, 0.25)
    return x, y, V, W


def run_slits(which="both", frames=True):
    p = SLIT
    x, y, V, W = slit_potential(which)
    X, Y = np.meshgrid(x, y)
    N = p["N"]
    k = 2 * np.pi * np.fft.fftfreq(N, 1.0)
    KX, KY = np.meshgrid(k, k)
    prop = SplitOperator(V, KX**2 + KY**2, p["dt"], W)
    psi = (gaussian(X, p["x0"], p["sx"], p["k0"]) * gaussian(Y, 0.0, p["sy"])).astype(np.complex64)
    n0 = float((np.abs(psi) ** 2).sum())
    assert abs(n0 - 1) < 1e-3, n0
    i_s = int(p["screen"])
    flux = np.zeros(N)
    steps = int(p["t_end"] / p["dt"])
    (cx0, cx1), (cy0, cy1) = p["crop_x"], p["crop_y"]
    rows = slice(int(cy0 + N / 2), int(cy1 + N / 2))
    cols = slice(cx0, cx1)
    out, ts, norms = [], [], []
    for s in range(steps + 1):
        if s % p["every"] == 0:
            ts.append(s * p["dt"])
            norms.append(float((np.abs(psi) ** 2).sum()))
            if frames and s % (2 * p["every"]) == 0:
                # stored as float16 (re, im), scaled by FRAME_SCALE: 1.9 MB a frame
                f = psi[rows, cols] * FRAME_SCALE
                out.append(np.stack([f.real, f.imag], axis=-1).astype(np.float16))
        # probability current through the screen column, j_x = Im(psi* d/dx psi) (hbar = m = 1)
        dpsi = (psi[:, i_s + 1] - psi[:, i_s - 1]) / 2
        flux += np.imag(np.conj(psi[:, i_s]) * dpsi) * p["dt"]
        if s < steps:
            psi = prop.step(psi)
    return y, flux, np.array(ts), np.array(norms), (np.array(out) if frames else None)


def compute_slits():
    p = SLIT
    raw = DATA_DIR / "slits_raw.npz"  # the three runs, kept so the checks below can change without re-simulating
    if raw.exists():
        r = dict(np.load(raw))
        y, flux, ts, norms, f_top, f_bot = r["y"], r["flux"], r["ts"], r["norms"], r["f_top"], r["f_bot"]
    else:
        y, flux, ts, norms, frames = run_slits("both", frames=True)
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        np.save(DATA_DIR / "slits_frames.npy", frames)
        del frames
        _, f_top, *_ = run_slits("top", frames=False)
        _, f_bot, *_ = run_slits("bottom", frames=False)
        np.savez(raw, y=y, flux=flux, ts=ts, norms=norms, f_top=f_top, f_bot=f_bot)
    through = flux.sum()
    # About a tenth of the packet gets through the slits; all of it reaches the screen.
    assert 0.05 < through < 0.3, through
    for f in (f_top, f_bot):
        assert abs(f.sum() / through - 0.5) < 0.05
    P12 = np.clip(flux, 0, None) / through
    P1, P2 = np.clip(f_top, 0, None) / through, np.clip(f_bot, 0, None) / through
    # Interference: with both slits open the central fringes go (nearly) to zero; with the sum of single slits
    # they don't.  The dark fringes sit where the two paths differ by a half-integer number of wavelengths (the
    # maxima are pulled slightly inward by the single-slit envelope that multiplies the fringes; the zeros aren't).
    lam = 2 * np.pi / p["k0"]
    L = p["screen"] - p["wall"][1]
    a = p["d"] / 2
    core = np.abs(y) < 200
    idx = np.where(core)[0][1:-1]
    peaks = [i for i in idx if P12[i] > P12[i - 1] and P12[i] >= P12[i + 1] and P12[i] > 0.15 * P12.max()]
    dips = [i for i in idx if P12[i] < P12[i - 1] and P12[i] <= P12[i + 1]]
    ypk, ydp = np.array([y[i] for i in peaks]), np.array([y[i] for i in dips])
    pdiff = lambda yy: np.sqrt(L**2 + (yy + a) ** 2) - np.sqrt(L**2 + (yy - a) ** 2)  # noqa: E731
    half = pdiff(ydp) / lam
    assert len(dips) >= 4 and np.all(np.abs(half - (np.floor(half) + 0.5)) < 0.05), half
    assert len(peaks) >= 5, peaks
    centre = np.abs(y) < 120
    mins12 = P12[centre].min() / P12[centre].max()
    mins_sum = (P1 + P2)[centre].min() / (P1 + P2)[centre].max()
    assert mins12 < 0.05 and mins_sum > 0.3, (mins12, mins_sum)  # both open: near-zeros; summed singles: none
    # Detection events: Born-rule samples from the arrival density (y), with a uniform position along the slits.
    cdf = np.cumsum(P12)
    cdf /= cdf[-1]
    g = rng(1989)
    n = TONOMURA[-1]
    ev_y = np.interp(g.uniform(0, 1, n), cdf, y) + g.uniform(-0.5, 0.5, n)
    ev_z = g.uniform(-1, 1, n)
    return dict(y=y, P12=P12, P1=P1, P2=P2, ts=ts, norms=norms, ev_y=ev_y, ev_z=ev_z, peaks=ypk, dips=ydp,
                dips_half=half, lam=np.array([lam]), L=np.array([L]), through=np.array([through]))


# ---------------------------------------------------------------------------
# 2. The free Gaussian packet (exact: each plane wave just turns at its own rate)
# ---------------------------------------------------------------------------
PACKET = dict(x=(-40.0, 160.0), N=4096, x0=0.0, s0=2.0, k0=2.0, t_end=40.0, frames=241)


def free_evolve(x, psi0, t):
    k = 2 * np.pi * np.fft.fftfreq(len(x), x[1] - x[0])
    return np.fft.ifft(np.fft.fft(psi0) * np.exp(-0.5j * k**2 * t))


def compute_packet():
    p = PACKET
    x = np.linspace(*p["x"], p["N"], endpoint=False)
    psi0 = gaussian(x, p["x0"], p["s0"], p["k0"])
    ts = np.linspace(0, p["t_end"], p["frames"])
    frames = np.array([free_evolve(x, psi0, t) for t in ts])
    m = np.array([moments(x, f) for f in frames])
    sig_th = p["s0"] * np.sqrt(1 + (ts / (2 * p["s0"] ** 2)) ** 2)
    assert np.allclose(m[:, 1], sig_th, rtol=1e-4), np.max(np.abs(m[:, 1] / sig_th - 1))
    assert np.allclose(m[:, 0], p["x0"] + p["k0"] * ts, atol=1e-6)
    assert np.allclose(m[:, 3], 1 / (2 * p["s0"]), rtol=1e-6)  # the momentum spread never changes
    # Phase velocity: follow one crest (arg psi = 0) from x = 0 at t = 0; near the peak it moves at k0 / 2, half the
    # group velocity k0, so the colors slide backward through the envelope.
    crest = [0.0]
    for f in frames[1:]:
        guess = crest[-1] + 0.5 * p["k0"] * (ts[1] - ts[0])
        w = np.abs(x - guess) < np.pi / p["k0"]
        ph = np.unwrap(np.angle(f[w]))
        xs_w = x[w]
        target = 2 * np.pi * np.round(np.interp(guess, xs_w, ph) / (2 * np.pi))
        i = np.where(np.diff(np.sign(ph - target)) != 0)[0]
        cands = xs_w[i] + (target - ph[i]) / (ph[i + 1] - ph[i]) * (xs_w[i + 1] - xs_w[i])
        crest.append(float(cands[np.argmin(np.abs(cands - guess))]))
    crest = np.array(crest)
    early = ts <= 3.0
    v_crest = np.polyfit(ts[early], crest[early], 1)[0]
    assert abs(v_crest - p["k0"] / 2) < 0.05, v_crest
    # Momentum-space amplitude (for the dual panel), on a k grid
    k = np.linspace(-1.0, 5.0, 601)
    phik = (2 * p["s0"] ** 2 / np.pi) ** 0.25 * np.exp(-((k - p["k0"]) ** 2) * p["s0"] ** 2)
    # Fourier synthesis: partial sums of plane waves with Gaussian weights (for "building a packet")
    kk = p["k0"] + np.linspace(-3, 3, 25) / p["s0"]
    w = np.exp(-((kk - p["k0"]) ** 2) * p["s0"] ** 2)
    # Real-world numbers: an electron localized to 1 angstrom; a 1-microgram grain localized to 1 micron
    rate_e = sc.hbar / (2 * sc.m_e * (1e-10) ** 2)  # 1/s
    width_e_1fs = 1e-10 * math.sqrt(1 + (rate_e * 1e-15) ** 2)
    rate_g = sc.hbar / (2 * 1e-9 * (1e-6) ** 2)
    t_double_g = math.sqrt(3) / rate_g / (365.25 * 24 * 3600)  # years until the grain's width doubles
    assert 5.5e-10 < width_e_1fs < 6.2e-10, width_e_1fs
    assert 5e5 < t_double_g < 2e6, t_double_g
    return dict(x=x, ts=ts, frames=frames.astype(np.complex64), mx=m[:, 0], sx=m[:, 1], sk=m[:, 3], sig_th=sig_th,
                crest=crest, v_crest=np.array([v_crest]),
                k=k, phik=phik, kk=kk, wk=w, width_e_1fs=np.array([width_e_1fs]),
                t_double_g=np.array([t_double_g]))


# ---------------------------------------------------------------------------
# 3. The infinite well (L = 1): exact eigen-expansion, revivals and the quantum carpet
# ---------------------------------------------------------------------------
CARPET = dict(L=1.0, x0=0.3, s0=0.06, k0=30.0, nmax=300, nx=900, nt=1200)  # moving: the classical zigzag weaves the carpet


def box_phi(n, x, L=1.0):
    return np.sqrt(2 / L) * np.sin(n * np.pi * x / L) * ((x >= 0) & (x <= L))


def box_E(n, L=1.0):
    return (n * np.pi / L) ** 2 / 2


def box_coeffs(psi0, x, nmax, L=1.0):
    ns = np.arange(1, nmax + 1)
    return ns, np.array([trapz(box_phi(n, x, L) * psi0, x) for n in ns])


def box_evolve(cs, ns, x, t, L=1.0):
    ph = np.exp(-1j * box_E(ns, L) * t)
    return (cs * ph) @ np.array([box_phi(n, x, L) for n in ns])


def compute_carpet():
    p = CARPET
    L = p["L"]
    xf = np.linspace(0, L, 20001)
    psi0 = gaussian(xf, p["x0"], p["s0"], p["k0"])
    psi0 = psi0 * (xf > 0) * (xf < L)
    psi0 /= math.sqrt(trapz(np.abs(psi0) ** 2, xf))
    ns, cs = box_coeffs(psi0, xf, p["nmax"], L)
    assert abs(np.sum(np.abs(cs) ** 2) - 1) < 1e-7, np.sum(np.abs(cs) ** 2)
    T_rev = 4 * L**2 / np.pi  # 2 pi hbar / E_1 with hbar = m = 1
    assert abs(T_rev - 2 * np.pi / box_E(1, L)) < 1e-12
    x = np.linspace(0, L, p["nx"])
    basis = np.array([box_phi(n, x, L) for n in ns])
    ts = np.linspace(0, T_rev, p["nt"])
    phases = np.exp(-1j * np.outer(ts, box_E(ns, L)))
    carpet = (phases * cs) @ basis  # (nt, nx)
    # Revivals: exactly the initial state at T_rev; its mirror image at T_rev / 2; two half-copies at T_rev / 4.
    psi_x0 = cs @ basis
    ov = lambda a, b: abs(trapz(np.conj(a) * b, x))  # noqa: E731
    full = box_evolve(cs, ns, x, T_rev, L)
    half = box_evolve(cs, ns, x, T_rev / 2, L)
    quarter = box_evolve(cs, ns, x, T_rev / 4, L)
    assert ov(full, psi_x0) > 0.999
    assert ov(half, psi_x0[::-1]) > 0.999
    left, right = x < L / 2, x >= L / 2
    q = np.abs(quarter) ** 2
    assert abs(trapz(q * (np.abs(x - p["x0"]) < 0.2), x) - 0.5) < 0.01
    assert abs(trapz(q * (np.abs(x - (L - p["x0"])) < 0.2), x) - 0.5) < 0.01
    # Movies: the whole period (for the weave), and the first 15% densely (the packet bouncing, then dissolving)
    t_movie = np.linspace(0, T_rev, 721)
    movie = (np.exp(-1j * np.outer(t_movie, box_E(ns, L))) * cs) @ basis
    t_early = np.linspace(0, 0.15 * T_rev, 601)
    early = (np.exp(-1j * np.outer(t_early, box_E(ns, L))) * cs) @ basis
    T_cl = 2 * L / p["k0"]  # classical round trip at the mean speed k0 (hbar = m = 1)
    return dict(x=x, ts=ts, carpet=carpet.astype(np.complex64), ns=ns, cs=cs, T_rev=np.array([T_rev]),
                t_movie=t_movie, movie=movie.astype(np.complex64), t_early=t_early, early=early.astype(np.complex64),
                T_cl=np.array([T_cl]), left=left, right=right)


# ---------------------------------------------------------------------------
# 4. The Hamiltonian as a matrix
# ---------------------------------------------------------------------------
def fd_box(N, L=1.0):
    """-1/2 d^2/dx^2 on N interior points of [0, L] with psi = 0 at the walls: a tridiagonal matrix."""
    h = L / (N + 1)
    d = np.full(N, 1.0 / h**2)
    e = np.full(N - 1, -0.5 / h**2)
    E, vecs = eigh_tridiagonal(d, e)
    return h, d, e, E, vecs


def compute_fd():
    out = {}
    for N in (8, 64, 1024):
        h, d, e, E, vecs = fd_box(N)
        n = np.arange(1, N + 1)
        exact_fd = (1 - np.cos(n * np.pi / (N + 1))) / h**2  # eigenvalues of this exact matrix
        assert np.allclose(E, exact_fd, rtol=1e-9)
        j = np.arange(1, N + 1)
        for m in range(min(N, 6)):
            s = np.sin((m + 1) * np.pi * j / (N + 1))
            s /= np.linalg.norm(s)
            assert abs(abs(vecs[:, m] @ s) - 1) < 1e-9  # the eigenvectors are sampled sines, exactly
        out[f"E{N}"] = E
        out[f"vecs{N}"] = vecs[:, :8]
    ratios = {N: out[f"E{N}"][:5] / out[f"E{N}"][0] for N in (8, 64, 1024)}
    assert np.allclose(ratios[1024], np.arange(1, 6) ** 2, rtol=1e-4)
    out["E_exact"] = box_E(np.arange(1, 9))
    # Real numbers: an electron in a 1 nm box
    E1_eV = (sc.pi * sc.hbar / 1e-9) ** 2 / (2 * sc.m_e) / sc.e
    assert abs(E1_eV - 0.376) < 0.001, E1_eV
    out["E1_eV_1nm"] = np.array([E1_eV])
    return out


# ---------------------------------------------------------------------------
# 5. Measuring energy on the carpet's packet
# ---------------------------------------------------------------------------
def compute_measure():
    c = load("carpet")
    ns, cs = c["ns"], c["cs"]
    P = np.abs(cs) ** 2
    P = P / P.sum()
    g = rng(1926)
    n_shots = 2000
    shots = g.choice(ns, size=n_shots, p=P)
    counts = np.bincount(shots, minlength=ns.max() + 1)[1:]
    # chi-square over the bins with expected count >= 5
    exp_ = n_shots * P
    ok = exp_ >= 5
    chi2 = float(np.sum((counts[ok] - exp_[ok]) ** 2 / exp_[ok]))
    dof = int(ok.sum()) - 1
    assert chi2 < dof + 4 * math.sqrt(2 * dof), (chi2, dof)
    # <E> two ways: sum of E_n |c_n|^2, and <psi|H|psi> = (1/2) int |psi'|^2 on a fine grid
    E_avg = float(np.sum(box_E(ns) * P))
    xf = np.linspace(0, 1, 40001)
    psi = cs @ np.array([box_phi(n, xf) for n in ns])
    dpsi = np.gradient(psi, xf)
    E_int = float(0.5 * trapz(np.abs(dpsi) ** 2, xf))
    assert abs(E_avg / E_int - 1) < 2e-3, (E_avg, E_int)
    return dict(ns=ns, P=P, shots=shots, counts=counts, E_avg=np.array([E_avg]), E_int=np.array([E_int]),
                sample_mean=np.array([float(box_E(shots).mean())]))


# ---------------------------------------------------------------------------
# 6. Uncertainty products for many states
# ---------------------------------------------------------------------------
def compute_uncert():
    x = np.linspace(-60, 60, 2**15, endpoint=False)
    rows = []
    # Gaussians of several widths: always exactly 1/2
    for s in (0.5, 1.0, 2.0):
        _, sx, _, sp = moments(x, gaussian(x, 0, s))
        rows.append(("gauss", s, sx, sp))
        assert abs(sx * sp - 0.5) < 1e-6
    # Box eigenstates (L = 1): (1/2) sqrt(n^2 pi^2 / 3 - 2).  The box's kinks make the momentum tails heavy,
    # so sigma_p is taken from the derivative: sigma_p^2 = int |psi'|^2 (the mean momentum is 0).
    xb = np.linspace(0, 1, 200001)
    for n in range(1, 6):
        phi = box_phi(n, xb)
        sx = math.sqrt(trapz(xb**2 * phi**2, xb) - trapz(xb * phi**2, xb) ** 2)
        sp = math.sqrt(trapz(np.gradient(phi, xb) ** 2, xb))
        th = 0.5 * math.sqrt(n**2 * np.pi**2 / 3 - 2)
        assert abs(sx * sp - th) < 1e-4, (n, sx * sp, th)
        rows.append(("box", n, sx, sp))
    # Oscillator eigenstates (m = omega = 1): sigma_x sigma_p = n + 1/2
    for n in range(0, 4):
        psi = ho_state(n, x)
        _, sx, _, sp = moments(x, psi)
        assert abs(sx * sp - (n + 0.5)) < 1e-6, (n, sx * sp)
        rows.append(("ho", n, sx, sp))
    # A spreading free Gaussian: sigma_x grows, sigma_p stays
    s0 = 1.0
    traj = []
    dxg = x[1] - x[0]
    for t in np.linspace(0, 6, 61):
        psi = free_evolve(x, gaussian(x, 0, s0), t)
        mx, sx, mp, sp = moments(x, psi)
        # covariance (1/2)<xp + px> - <x><p> = Re <psi| x p |psi> - <x><p>, with p = -i d/dx
        cov = float(np.real(np.sum(np.conj(psi) * x * (-1j) * np.gradient(psi, dxg)) * dxg)) - mx * mp
        traj.append((t, sx, sp, cov))
    traj = np.array(traj)
    assert np.allclose(traj[:, 1] * traj[:, 2], 0.5 * np.sqrt(1 + (traj[:, 0] / 2) ** 2), rtol=1e-5)
    # the Schrodinger-Robertson bound stays saturated: sigma_x^2 sigma_p^2 - cov^2 = 1/4 exactly
    assert np.allclose((traj[:, 1] * traj[:, 2]) ** 2 - traj[:, 3] ** 2, 0.25, atol=1e-5)
    kind = np.array([r[0] for r in rows])
    par = np.array([r[1] for r in rows], float)
    sx = np.array([r[2] for r in rows])
    sp = np.array([r[3] for r in rows])
    return dict(kind=kind, par=par, sx=sx, sp=sp, traj=traj)


# ---------------------------------------------------------------------------
# 7. Tunneling through a rectangular barrier
# ---------------------------------------------------------------------------
TUNNEL = dict(x=(-400.0, 400.0), N=8000,  # dx = 0.1: the barrier is exactly 25 cells wide
              x0=-110.0, s0=6.0, k0=1.0, V0=0.7, a=2.5, dt=0.01, t_end=260.0, every=100)
# (dt = 0.01 resolves the kinetic phase k^2 dt / 2 up to the grid's highest k; at dt = 0.05 a 0.15% numerical
#  splitting artifact at |k| ~ 20 appears and biases <k^2>)


def barrier_T(E, V0, a):
    """Transmission probability of a rectangular barrier (hbar = m = 1), for E < V0, E = V0 and E > V0."""
    E = np.asarray(E, dtype=np.float64)
    out = np.empty_like(E)
    lo, hi = E < V0, E > V0
    kap = np.sqrt(2 * (V0 - E[lo]))
    out[lo] = 1 / (1 + V0**2 * np.sinh(kap * a) ** 2 / (4 * E[lo] * (V0 - E[lo])))
    q = np.sqrt(2 * (E[hi] - V0))
    out[hi] = 1 / (1 + V0**2 * np.sin(q * a) ** 2 / (4 * E[hi] * (E[hi] - V0)))
    eq = ~(lo | hi)
    out[eq] = 1 / (1 + V0 * a**2 / 2)
    return out


def compute_tunnel():
    p = TUNNEL
    x = np.linspace(*p["x"], p["N"], endpoint=False)
    dx = x[1] - x[0]
    V = np.where(np.abs(x) < p["a"] / 2, p["V0"], 0.0)
    W = absorber(x, -330, 330, 60, 0.05)
    k = 2 * np.pi * np.fft.fftfreq(p["N"], dx)
    prop = SplitOperator(V, k**2, p["dt"], W)
    psi = gaussian(x, p["x0"], p["s0"], p["k0"])
    frames, ts, PT, PR = [], [], [], []
    steps = int(p["t_end"] / p["dt"])
    for s in range(steps + 1):
        if s % p["every"] == 0:
            frames.append(psi.copy())
            ts.append(s * p["dt"])
            rho = np.abs(psi) ** 2 * dx
            PT.append(rho[x > p["a"] / 2].sum())
            PR.append(rho[x < -p["a"] / 2].sum())
        if s < steps:
            psi = prop.step(psi)
    PT, PR = np.array(PT), np.array(PR)
    # The barrier is an energy filter: the transmitted part carries *more* momentum on average than the incoming
    # packet (fast components tunnel more easily), the reflected part less.  Nothing loses energy.
    kf = 2 * np.pi * np.fft.fftfreq(p["N"], dx)
    order = np.argsort(kf)
    kf = kf[order]
    # split the final wave with smooth windows far from the barrier (a sharp cut would add spurious high-k tails)
    phT = np.abs(np.fft.fft(psi * 0.5 * (1 + np.tanh((x - 20) / 3)))[order]) ** 2
    phR = np.abs(np.fft.fft(psi * 0.5 * (1 - np.tanh((x + 20) / 3)))[order]) ** 2
    ph0 = np.abs(np.fft.fft(frames[0])[order]) ** 2
    mT = float((kf * phT).sum() / phT.sum())
    mR = float((-kf * phR).sum() / phR.sum())
    m0 = float((kf * ph0).sum() / ph0.sum())
    assert mT > m0 + 0.02 and mR < m0, (mT, m0, mR)
    E_ratio = float(((kf**2 * phT).sum() / phT.sum()) / ((kf**2 * ph0).sum() / ph0.sum()))  # <E> transmitted / incoming
    assert 1.05 < E_ratio < 1.09, E_ratio
    win = (kf > -1.6) & (kf < 1.6)
    norm_ = (kf[1] - kf[0])
    k_hist = dict(kf=kf[win], phT=phT[win] / (ph0.sum() * norm_), phR=phR[win] / (ph0.sum() * norm_),
                  ph0=ph0[win] / (ph0.sum() * norm_), kT=np.array([mT]), kR=np.array([mR]), k0m=np.array([m0]),
                  E_ratio=np.array([E_ratio]))
    # Theory: each momentum component k tunnels with probability T(k^2 / 2).
    kk = np.linspace(p["k0"] - 8 / (2 * p["s0"]), p["k0"] + 8 / (2 * p["s0"]), 4001)
    w = np.exp(-2 * p["s0"] ** 2 * (kk - p["k0"]) ** 2)
    w /= trapz(w, kk)
    T_pred = float(trapz(barrier_T(kk**2 / 2, p["V0"], p["a"]) * w, kk))
    T_k0 = float(barrier_T(np.array([p["k0"] ** 2 / 2]), p["V0"], p["a"])[0])
    assert abs(PT[-1] - T_pred) < 0.003, (PT[-1], T_pred)
    assert abs(PT[-1] + PR[-1] - 1) < 1e-3  # nothing absorbed yet: the packets are still on screen
    E = np.linspace(0.01, 2.0, 600)
    TE = barrier_T(E, p["V0"], p["a"])
    # A real electron: 1 eV below the top of a barrier, through 0.5 nm and 1 nm (exp(-2 kappa a) estimates)
    kap = math.sqrt(2 * sc.m_e * 1.0 * sc.e) / sc.hbar
    e_half, e_one = math.exp(-2 * kap * 0.5e-9), math.exp(-2 * kap * 1e-9)
    # STM: a 4.5 eV work function; the current changes by exp(2 kappa * 1 angstrom) per angstrom
    kap_stm = math.sqrt(2 * sc.m_e * 4.5 * sc.e) / sc.hbar
    stm = math.exp(2 * kap_stm * 1e-10)
    assert 8 < stm < 10, stm
    return dict(x=x, V=V, ts=np.array(ts), frames=np.array(frames).astype(np.complex64), PT=PT, PR=PR,
                T_pred=np.array([T_pred]), T_k0=np.array([T_k0]), E=E, TE=TE, kk=kk, wk=w,
                kappa_1eV=np.array([kap]), e_half=np.array([e_half]), e_one=np.array([e_one]), stm=np.array([stm]),
                **k_hist)


# ---------------------------------------------------------------------------
# 8. The harmonic oscillator (m = omega = hbar = 1)
# ---------------------------------------------------------------------------
def ho_state(n, x):
    return (1 / math.sqrt(2.0**n * math.factorial(n))) * np.pi**-0.25 * eval_hermite(n, x) * np.exp(-(x**2) / 2)


def wigner(x, psi, p, stride=1):
    """W(x, p) = (1/pi) int psi*(x + y) psi(x - y) e^{2ipy} dy on the grid (hbar = 1); rows = p, cols = x[::stride]."""
    dx = x[1] - x[0]
    n = len(x)
    xi = np.arange(0, n, stride)
    M = n // 2
    js = np.arange(-M, M)
    W = np.zeros((len(p), len(xi)))
    E = np.exp(2j * np.outer(js * dx, p))  # (y, p)
    for c, i in enumerate(xi):
        a, b = i + js, i - js
        ok = (a >= 0) & (a < n) & (b >= 0) & (b < n)
        f = np.zeros(len(js), complex)
        f[ok] = np.conj(psi[a[ok]]) * psi[b[ok]]
        W[:, c] = np.real(f @ E) * dx / np.pi
    return W


def compute_oscillator():
    out = {}
    # FD spectrum on a fine grid: E_n = n + 1/2
    xg = np.linspace(-12, 12, 4001)
    h = xg[1] - xg[0]
    E, vecs = eigh_tridiagonal(1 / h**2 + xg**2 / 2, np.full(len(xg) - 1, -0.5 / h**2), select="i", select_range=(0, 11))
    assert np.allclose(E, np.arange(12) + 0.5, atol=2e-4), E
    out["E_fd"] = E
    # Probability of being outside the classical turning points in the ground state: erfc(1)
    x = np.linspace(-10, 10, 20001)
    p0 = ho_state(0, x) ** 2
    xo = np.linspace(1, 10, 90001)  # integrate the tail from the turning point x = 1 outward, both sides
    outside = float(2 * trapz(ho_state(0, xo) ** 2, xo))
    assert abs(outside - erfc(1)) < 1e-7, (outside, erfc(1))
    out["outside0"] = np.array([outside])
    # n = 30 vs the classical density 1 / (pi sqrt(A^2 - x^2)), A = sqrt(2n + 1)
    out["x30"] = x
    out["p30"] = ho_state(30, x) ** 2
    # Split-operator runs: a coherent state (displaced ground state) and a squeezed one, two periods each
    xs = np.linspace(-16, 16, 1024, endpoint=False)
    dx = xs[1] - xs[0]
    k = 2 * np.pi * np.fft.fftfreq(len(xs), dx)
    dt = 2 * np.pi / 2000
    prop = SplitOperator(xs**2 / 2, k**2, dt)
    runs = {"coherent": gaussian(xs, 4.0, 1 / math.sqrt(2)), "squeezed": gaussian(xs, 4.0, 0.35)}
    for name, psi in runs.items():
        frames, mom = [], []
        for s in range(4001):
            if s % 25 == 0:
                frames.append(psi.copy())
                mom.append(moments(xs, psi))
            if s < 4000:
                psi = prop.step(psi)
        mom = np.array(mom)
        ts = np.arange(len(frames)) * 25 * dt
        assert np.allclose(mom[:, 0], 4 * np.cos(ts), atol=2e-3), np.max(np.abs(mom[:, 0] - 4 * np.cos(ts)))
        if name == "coherent":
            assert np.allclose(mom[:, 1], 1 / math.sqrt(2), atol=1e-3)  # it never spreads
        else:
            assert mom[:, 1].max() / mom[:, 1].min() > 1.8  # it breathes, twice per period
        out[f"{name}_frames"] = np.array(frames).astype(np.complex64)
        out[f"{name}_mom"] = mom
        out["t_frames"] = ts
    out["xs"] = xs
    # Wigner functions on a phase-space grid
    pw = np.linspace(-6, 6, 241)
    xw = np.linspace(-8, 8, 2001)
    sw = 5  # every 5th x: 401 columns, x = 0 in the middle
    W1 = wigner(xw, ho_state(1, xw).astype(complex), pw, sw)
    assert abs(W1[120, len(W1[0]) // 2] + 1 / np.pi) < 2e-3  # W_1(0, 0) = -1/pi: negative "probability"
    Wc = wigner(xw, gaussian(xw, 0.0, 1 / math.sqrt(2)).astype(complex), pw, sw)
    assert abs(Wc.max() - 1 / np.pi) < 2e-3
    cat = ho_state(0, xw - 3.0) + ho_state(0, xw + 3.0)
    cat = cat / math.sqrt(trapz(np.abs(cat) ** 2, xw))
    Wcat = wigner(xw, cat.astype(complex), pw, sw)
    # marginal: integrating over p gives |psi(x)|^2
    marg = trapz(Wcat, pw, axis=0)
    assert np.allclose(marg, np.abs(cat[::sw]) ** 2, atol=2e-3)
    out.update(pw=pw, xw=xw[::sw], W1=W1, Wcoh=Wc, Wcat=Wcat, W0=Wc)
    # The coherent state's Wigner function along its orbit (computed from the evolved psi, every 8th frame)
    xs_w = np.linspace(-8, 8, 801)
    coh = out["coherent_frames"]
    Wt = []
    for f in coh[::2]:
        psi = np.interp(xs_w, xs, f.real) + 1j * np.interp(xs_w, xs, f.imag)
        Wt.append(wigner(xs_w, psi, pw, 3))
    out["W_orbit"] = np.array(Wt).astype(np.float32)
    out["xs_w"] = xs_w[::3]
    return out


# ---------------------------------------------------------------------------
# 9. Hydrogen (atomic units: a0 = 1, energies in Hartree = 2 Ry)
# ---------------------------------------------------------------------------
def R_nl(n, l, r):
    rho = 2 * r / n
    norm = math.sqrt((2 / n) ** 3 * math.factorial(n - l - 1) / (2 * n * math.factorial(n + l)))
    return norm * np.exp(-rho / 2) * rho**l * eval_genlaguerre(n - l - 1, 2 * l + 1, rho)


def psi_nlm(n, l, m, x, y, z):
    r = np.sqrt(x * x + y * y + z * z)
    theta = np.arccos(np.clip(z / np.maximum(r, 1e-12), -1, 1))
    phi = np.arctan2(y, x)
    return R_nl(n, l, r) * sph_harm_y(l, m, theta, phi)


def numerov_out(E, l, r):
    """Integrate u'' = (l(l+1)/r^2 - 2/r - 2E) u outward from u ~ r^{l+1} (Numerov)."""
    h = r[1] - r[0]
    f = l * (l + 1) / r**2 - 2 / r - 2 * E
    u = np.zeros_like(r)
    u[0], u[1] = r[0] ** (l + 1), r[1] ** (l + 1)
    c = h * h / 12
    for i in range(1, len(r) - 1):
        u[i + 1] = (2 * u[i] * (1 + 5 * c * f[i]) - u[i - 1] * (1 - c * f[i - 1])) / (1 - c * f[i + 1])
    return u


# Air refractive index (Edlen 1966 form, as used for the standard air wavelengths of spectroscopy)
def n_air(lam_vac_nm):
    s2 = (1e3 / lam_vac_nm) ** 2  # (1/um)^2
    return 1 + 1e-8 * (8342.13 + 2406030 / (130 - s2) + 15997 / (38.9 - s2))


VIEW_EL = np.deg2rad(32.0)  # camera elevation above the xy-plane for orbital renders (high enough to see donuts)


def render_orbital(fn, extent, res=440, samples=200, az=0.0, el=VIEW_EL, optical_depth=1.0, absorb=None):
    """Volume render of a complex 3D amplitude: each pixel integrates |psi|^2 along its ray (emission), colored by
    the density-weighted mean phase color, with a little self-absorption (the densest ray is ``optical_depth``
    thick) so nearer lobes cover farther ones.  Returns RGB float (res, res, 3) and the emitted-density image."""
    if absorb is None:
        _, a0 = render_orbital(fn, extent, res=64, samples=96, az=az, el=el, absorb=0.0)
        absorb = optical_depth / max(float(a0.max()), 1e-30)
    u = np.linspace(-extent, extent, res)
    s = np.linspace(-extent, extent, samples)
    ds = s[1] - s[0]
    # camera basis: view direction d, right r, up v (z is "up" in the scene, tilted toward us by el)
    # the camera sits at (cos el sin az, -cos el cos az, sin el) * infinity, looking at the origin
    d = np.array([-math.cos(el) * math.sin(az), math.cos(el) * math.cos(az), -math.sin(el)])
    rgt = np.array([math.cos(az), math.sin(az), 0.0])
    up = np.cross(rgt, d)
    up = -up if up[2] < 0 else up
    acc_rgb = np.zeros((res, res, 3))
    acc = np.zeros((res, res))
    chunk = 24
    for r0 in range(0, res, chunk):
        rows = u[::-1][r0: r0 + chunk]
        V, Uu, S = np.meshgrid(rows, u, s, indexing="ij")
        P = Uu[..., None] * rgt + V[..., None] * up + S[..., None] * d
        psi = fn(P[..., 0], P[..., 1], P[..., 2])
        rho = np.abs(psi) ** 2
        if absorb > 0:
            tau = np.cumsum(rho, axis=2) * ds * absorb
            rho = rho * np.exp(-tau)
        col = hue_rgb(np.angle(psi))
        acc[r0: r0 + chunk] = rho.sum(axis=2) * ds
        acc_rgb[r0: r0 + chunk] = (rho[..., None] * col).sum(axis=2) * ds
    mean_col = acc_rgb / np.maximum(acc[..., None], 1e-30)
    return mean_col, acc


def tone(mean_col, acc, gain, white=0.25):
    a = 1 - np.exp(-gain * acc)
    hot = np.clip(gain * acc - 1.2, 0, 3)[..., None] / 3 * white
    col = mean_col + (1 - mean_col) * hot
    return to_uint8(BG + a[..., None] * (col - BG))


ORBITALS = [  # (n, l, m, extent in a0)
    (1, 0, 0, 5.0), (2, 0, 0, 13.0), (2, 1, 0, 11.0), (2, 1, 1, 11.0), (3, 0, 0, 24.0), (3, 1, 0, 22.0),
    (3, 1, 1, 22.0), (3, 2, 0, 20.0), (3, 2, 1, 20.0), (3, 2, 2, 20.0), (4, 3, 0, 32.0), (4, 3, 2, 32.0),
]


def _orbital_job(args):
    n, l, m, ext = args
    mean_col, acc = render_orbital(lambda x, y, z: psi_nlm(n, l, m, x, y, z), ext)
    return (n, l, m), mean_col.astype(np.float32), acc.astype(np.float32)


def _px_job(args):
    kind, ext, az = args
    if kind == "px":
        fn = lambda x, y, z: (psi_nlm(2, 1, -1, x, y, z) - psi_nlm(2, 1, 1, x, y, z)) / math.sqrt(2)  # noqa: E731
    else:
        sgn = 1 if kind == "p+" else -1
        fn = lambda x, y, z: psi_nlm(2, 1, sgn, x, y, z)  # noqa: E731
    mean_col, acc = render_orbital(fn, ext, res=360, samples=180, az=az)
    return mean_col.astype(np.float32), acc.astype(np.float32)


def _slosh_job(args):
    t, ext = args
    E1, E2 = -0.5, -0.125
    fn = lambda x, y, z: (psi_nlm(1, 0, 0, x, y, z) * np.exp(-1j * E1 * t)  # noqa: E731
                          + psi_nlm(2, 1, 0, x, y, z) * np.exp(-1j * E2 * t)) / math.sqrt(2)
    mean_col, acc = render_orbital(fn, ext, res=360, samples=180)
    return mean_col.astype(np.float32), acc.astype(np.float32)


def compute_hydrogen():
    out = {}
    # 1. The radial equation as a matrix: u'' with the effective potential, on r in (0, 160]
    r = np.linspace(0.02, 160, 8000)
    h = r[1] - r[0]
    for l in (0, 1, 2):
        Veff = -1 / r + l * (l + 1) / (2 * r**2)
        E, _ = eigh_tridiagonal(1 / h**2 + Veff, np.full(len(r) - 1, -0.5 / h**2), select="i", select_range=(0, 4))
        n = np.arange(l + 1, l + 6)
        assert np.allclose(E, -0.5 / n**2, rtol=6e-3), (l, E, -0.5 / n**2)
        out[f"E_l{l}"] = E
    # 2. Shooting: integrate outward at E slightly above / at / below -1/2; only the eigenvalue decays
    rs = np.linspace(1e-4, 10, 10001)
    shots = {}
    for tag, E in (("lo", -0.5 * 1.04), ("ex", -0.5), ("hi", -0.5 * 0.96)):
        u = numerov_out(E, 0, rs)
        shots[tag] = u / np.abs(u[: 2000]).max()
    assert shots["lo"][-1] < 0 < shots["hi"][-1] or shots["hi"][-1] < 0 < shots["lo"][-1]
    out.update(r_shoot=rs, u_lo=shots["lo"], u_ex=shots["ex"], u_hi=shots["hi"])
    # 3. Radial probability densities r^2 R^2, normalized
    rr = np.linspace(0, 40, 4001)
    for n, l in ((1, 0), (2, 0), (2, 1), (3, 0), (3, 1), (3, 2)):
        P = rr**2 * R_nl(n, l, rr) ** 2
        assert abs(trapz(P, rr) - 1) < 1e-3, (n, l, trapz(P, rr))
        out[f"P{n}{l}"] = P
    out["rr"] = rr
    assert abs(rr[np.argmax(out["P10"])] - 1.0) < 0.011  # most probable radius = a0
    # 4. Spectrum: Rydberg with the reduced mass; standard air wavelengths for the Balmer lines
    R_inf = sc.physical_constants["Rydberg constant"][0]  # 1/m
    mu = 1 / (1 + 1 / sc.physical_constants["proton-electron mass ratio"][0])
    RH = R_inf * mu
    balmer_vac = np.array([1e9 / (RH * (1 / 4 - 1 / n**2)) for n in (3, 4, 5, 6)])
    balmer_air = balmer_vac / n_air(balmer_vac)
    assert abs(balmer_air[0] - 656.28) < 0.02, balmer_air  # H-alpha, the red line
    assert abs(balmer_air[1] - 486.13) < 0.02, balmer_air
    lyman_a = 1e9 / (RH * (1 - 1 / 4))
    assert abs(lyman_a - 121.567) < 0.003, lyman_a
    nu_lya = sc.c / (lyman_a * 1e-9)
    Ry_eV = sc.physical_constants["Rydberg constant times hc in eV"][0]
    out.update(balmer_vac=balmer_vac, balmer_air=balmer_air, lyman_a=np.array([lyman_a]), nu_lya=np.array([nu_lya]),
               Ry_eV=np.array([Ry_eV]), Ry_eV_H=np.array([Ry_eV * mu]), a0=np.array([sc.physical_constants["Bohr radius"][0]]))
    # 5. Orbital renders (fixed view), the p_x superposition, and the 1s + 2p_z slosh
    with ProcessPoolExecutor(WORKERS) as pool:
        for (n, l, m), col, acc in pool.map(_orbital_job, ORBITALS):
            out[f"orb_{n}{l}{m}_col"] = col
            out[f"orb_{n}{l}{m}_acc"] = acc
        for kind in ("p+", "p-", "px"):
            col, acc = list(pool.map(_px_job, [(kind, 11.0, 0.0)]))[0]
            out[f"{kind}_col"], out[f"{kind}_acc"] = col, acc
        period = 2 * np.pi / (0.5 - 0.125)
        ts = np.linspace(0, period, 49)[:-1]
        res = list(pool.map(_slosh_job, [(t, 9.0) for t in ts]))
    out["slosh_col"] = np.array([c for c, _ in res])
    out["slosh_acc"] = np.array([a for _, a in res])
    out["slosh_t"] = ts
    # The charge centroid <z> of the superposition oscillates: <z>(t) = <100|z|210> cos(dE t)
    z12 = 128 * math.sqrt(2) / 243  # <100|z|210> in a0
    out["z12"] = np.array([z12])
    return out


# ---------------------------------------------------------------------------
# 10. Spin: Stern-Gerlach
# ---------------------------------------------------------------------------
def compute_spin():
    g = rng(1922)
    n = 6000
    # Deflection on the screen (arbitrary units: full deflection +-1), plus the beam's own width
    beam = g.normal(0, 0.12, (n, 2))
    classical = g.uniform(-1, 1, n)  # isotropic moments: cos(theta) is uniform on [-1, 1]
    quantum = g.choice([-1.0, 1.0], n)
    # Sequential: prepare up along z, measure along an axis at angle theta: P(up) = cos^2(theta / 2)
    thetas = np.deg2rad(np.arange(0, 181, 15))
    m = 1000
    ups = np.array([g.binomial(m, math.cos(t / 2) ** 2) for t in thetas])
    se = np.sqrt(np.cos(thetas / 2) ** 2 * np.sin(thetas / 2) ** 2 / m)
    assert np.all(np.abs(ups / m - np.cos(thetas / 2) ** 2) <= 4 * se + 1e-9)
    # z -> x -> z: after selecting up-x, the second z measurement is 50/50 again
    zxz = g.binomial(m, 0.5)
    return dict(beam=beam, classical=classical, quantum=quantum, thetas=thetas, ups=ups, m=np.array([m]),
                zxz=np.array([zxz]))


# ---------------------------------------------------------------------------
# 11. Bell / CHSH
# ---------------------------------------------------------------------------
CHSH_ANGLES = dict(a=0.0, a2=90.0, b=45.0, b2=135.0)  # degrees, in the plane perpendicular to the beam


def compute_bell():
    g = rng(1964)
    n = 100_000
    ang = {k: np.deg2rad(v) for k, v in CHSH_ANGLES.items()}

    def quantum(alpha, beta):
        # singlet: P(same) = sin^2(theta / 2), outcomes individually 50/50
        th = alpha - beta
        A = g.choice([-1, 1], n)
        same = g.uniform(size=n) < math.sin(th / 2) ** 2
        B = np.where(same, A, -A)
        return A, B

    def lhv(alpha, beta):
        # each pair carries a hidden direction lam; A = sign(a . lam), B = -sign(b . lam)
        lam = g.uniform(0, 2 * np.pi, n)
        A = np.sign(np.cos(alpha - lam))
        B = -np.sign(np.cos(beta - lam))
        return A, B

    out = {}
    for model, fn in (("q", quantum), ("lhv", lhv)):
        E = {}
        for (ka, kb) in (("a", "b"), ("a", "b2"), ("a2", "b"), ("a2", "b2")):
            A, B = fn(ang[ka], ang[kb])
            E[ka + kb] = float(np.mean(A * B))
            if model == "q":
                assert abs(np.mean(A)) < 0.02  # no signaling: Alice alone always sees 50/50
        S = E["ab"] - E["ab2"] + E["a2b"] + E["a2b2"]
        out[f"S_{model}"] = np.array([S])
        out[f"E_{model}"] = np.array([E["ab"], E["ab2"], E["a2b"], E["a2b2"]])
    assert abs(abs(out["S_q"][0]) - 2 * math.sqrt(2)) < 0.03, out["S_q"]
    assert abs(abs(out["S_lhv"][0]) - 2) < 0.03, out["S_lhv"]
    # correlation curves E(theta): quantum -cos(theta); the hidden-variable model -1 + 2 theta / pi; sampled
    th = np.deg2rad(np.arange(0, 181, 10))
    Eq, El = [], []
    for t in th:
        A, B = quantum(0.0, t)
        Eq.append(np.mean(A * B))
        A, B = lhv(0.0, t)
        El.append(np.mean(A * B))
    Eq, El = np.array(Eq), np.array(El)
    assert np.allclose(Eq, -np.cos(th), atol=0.015)
    assert np.allclose(El, -1 + 2 * th / np.pi, atol=0.015)
    out.update(th=th, Eq_curve=Eq, El_curve=El, n=np.array([n]))
    return out


# ---------------------------------------------------------------------------
# 14. Smaller pieces: same density / different phase, heat vs Schrodinger, Taylor translation, the stationary
#     scattering state of the barrier, and the momentum content of box states
# ---------------------------------------------------------------------------
def compute_extras():
    out = {}
    # (a) Three packets with the same |psi|^2 and different phase winding: k = +1.5, 0, -1.5
    x = np.linspace(-40, 40, 2048, endpoint=False)
    ts = np.linspace(0, 12, 121)
    for name, k0 in (("kp", 1.5), ("k0", 0.0), ("km", -1.5)):
        psi0 = gaussian(x, 0.0, 1.5, k0)
        fr = np.array([free_evolve(x, psi0, t) for t in ts])
        m = np.array([moments(x, f) for f in fr])
        assert np.allclose(m[:, 0], k0 * ts, atol=1e-6)  # each moves at its own k
        out[f"trio_{name}"] = fr.astype(np.complex64)
    out["trio_x"], out["trio_t"] = x, ts
    assert np.allclose(np.abs(out["trio_kp"][0]), np.abs(out["trio_km"][0]))
    # (b) Heat equation vs Schrodinger equation from the same bump: du/dt = (1/2) u''  vs  dpsi/dt = (i/2) psi''
    k = 2 * np.pi * np.fft.fftfreq(len(x), x[1] - x[0])
    u0 = np.exp(-(x**2) / 4)  # the amplitude of a sigma = 1 Gaussian
    th = np.linspace(0, 6, 61)
    heat = np.array([np.real(np.fft.ifft(np.fft.fft(u0) * np.exp(-0.5 * k**2 * t))) for t in th])
    schr = np.array([np.fft.ifft(np.fft.fft(u0) * np.exp(-0.5j * k**2 * t)) for t in th])
    dx = x[1] - x[0]
    n_heat = (heat**2).sum(axis=1) * dx
    n_schr = (np.abs(schr) ** 2).sum(axis=1) * dx
    assert n_heat[-1] < 0.5 * n_heat[0]  # the heat equation loses "length"
    assert np.allclose(n_schr, n_schr[0], rtol=1e-10)  # Schrodinger keeps it exactly
    out.update(heat=heat.astype(np.float32), schr=schr.astype(np.complex64), th=th, n_heat=n_heat, n_schr=n_schr)
    # (c) Momentum generates translations: partial Taylor sums of psi(x - a) for psi = exp(-x^2/4)
    xt = np.linspace(-6, 9, 1201)
    a = 2.5
    terms = np.array([(a / 2) ** n / math.factorial(n) * eval_hermite(n, xt / 2) * np.exp(-(xt**2) / 4) for n in range(31)])
    partial = np.cumsum(terms, axis=0)
    target = np.exp(-((xt - a) ** 2) / 4)
    assert np.max(np.abs(partial[30] - target)) < 1e-6
    assert np.max(np.abs(partial[3] - target)) > 0.1
    out.update(xt=xt, taylor=partial[[0, 1, 2, 3, 4, 6, 8, 12, 16, 24, 30]].astype(np.float64), taylor_n=np.array(
        [0, 1, 2, 3, 4, 6, 8, 12, 16, 24, 30]), taylor_a=np.array([a]))
    # (d) The stationary scattering state of the rectangular barrier (V0 on 0 < x < a) at E = 1/2
    V0, aw, E = TUNNEL["V0"], TUNNEL["a"], 0.5
    kk = math.sqrt(2 * E)
    kap = math.sqrt(2 * (V0 - E))
    # unknowns r, C, D, t:  psi = e^{ikx} + r e^{-ikx};  C e^{kap x} + D e^{-kap x};  t e^{ikx}
    A = np.array([
        [-1, 1, 1, 0],
        [1j * kk, kap, -kap, 0],
        [0, math.exp(kap * aw), math.exp(-kap * aw), -np.exp(1j * kk * aw)],
        [0, kap * math.exp(kap * aw), -kap * math.exp(-kap * aw), -1j * kk * np.exp(1j * kk * aw)],
    ], dtype=complex)
    b = np.array([1, 1j * kk, 0, 0], dtype=complex)
    r, Cc, Dd, t = np.linalg.solve(A, b)
    assert abs(abs(r) ** 2 + abs(t) ** 2 - 1) < 1e-12
    assert abs(abs(t) ** 2 - barrier_T(np.array([E]), V0, aw)[0]) < 1e-12
    xs = np.linspace(-14, 14 + aw, 2801)
    psi = np.where(xs < 0, np.exp(1j * kk * xs) + r * np.exp(-1j * kk * xs),
                   np.where(xs < aw, Cc * np.exp(kap * xs) + Dd * np.exp(-kap * xs), t * np.exp(1j * kk * xs)))
    out.update(sc_x=xs, sc_psi=psi.astype(np.complex128), sc_T=np.array([abs(t) ** 2]), sc_R=np.array([abs(r) ** 2]),
               sc_kappa=np.array([kap]))
    # (e) Momentum content of box eigenstates (L = 1): phi_n(p) = (2 pi)^{-1/2} int_0^1 sqrt2 sin(n pi x) e^{-ipx} dx
    xb = np.linspace(0, 1, 4001)
    p = np.linspace(-30, 30, 1201)
    E_ = np.exp(-1j * np.outer(p, xb))
    for n in (1, 2, 3):
        amp = trapz(E_ * (math.sqrt(2) * np.sin(n * np.pi * xb))[None, :], xb, axis=1) / math.sqrt(2 * np.pi)
        dens = np.abs(amp) ** 2
        assert abs(trapz(dens, p) - 1) < 0.01, trapz(dens, p)
        if n >= 2:
            pk = p[np.argmax(dens * (p > 0))]
            assert 0.75 * n * np.pi < pk < 1.02 * n * np.pi, (n, pk)  # near +-n pi (the two lobes overlap and pull inward)
        out[f"boxp{n}"] = dens
    out["boxp_p"] = p
    return out


# ---------------------------------------------------------------------------
# 13. Physical numbers quoted by the narration
# ---------------------------------------------------------------------------
def compute_numbers():
    h, hbar, me, e, c = sc.h, sc.hbar, sc.m_e, sc.e, sc.c
    # de Broglie wavelength of a 50 kV electron (Tonomura's microscope), relativistic momentum
    T = 50e3 * e
    p = math.sqrt(T * (T + 2 * me * c**2)) / c
    lam50 = h / p
    assert 5.3e-12 < lam50 < 5.4e-12, lam50
    # a 1 eV electron
    lam1 = h / math.sqrt(2 * me * e)
    assert abs(lam1 - 1.226e-9) < 2e-12, lam1
    # electron in a 1 nm box: E1, the 1->2 sloshing period h / (E2 - E1), the revival time 4 m L^2 / (pi hbar)
    L = 1e-9
    E1 = (np.pi * hbar / L) ** 2 / (2 * me)
    slosh = h / (3 * E1)
    Trev = 4 * me * L**2 / (np.pi * hbar)
    assert abs(E1 / e - 0.376) < 1e-3 and abs(slosh - 3.67e-15) < 0.02e-15 and abs(Trev - 11.0e-15) < 0.1e-15
    # the oscillator: a CO molecule's vibration, hbar omega for 2143 cm^-1 (for scale)
    # spin: electron gyromagnetic ratio |gamma_e| / 2 pi in GHz/T
    gam = abs(sc.physical_constants["electron gyromag. ratio in MHz/T"][0]) / 1e3
    assert abs(gam - 28.02) < 0.01, gam
    return dict(lam50=np.array([lam50]), lam1=np.array([lam1]), E1_eV=np.array([E1 / e]), slosh=np.array([slosh]),
                Trev=np.array([Trev]), gamma_e=np.array([gam]), hbar=np.array([hbar]), h=np.array([h]))


# ---------------------------------------------------------------------------
# 12. Two particles on a line: the wavefunction lives on configuration space (x1, x2)
# ---------------------------------------------------------------------------
def compute_pair():
    """A product state and an entangled ("EPR-like") Gaussian state of two particles in 1D, on the (x1, x2) plane,
    with the conditional density of particle 2 after particle 1 is found at x1 = 1.5, and the marginals."""
    u = np.linspace(-5, 5, 401)
    X1, X2 = np.meshgrid(u, u)  # rows = x2, cols = x1
    du = u[1] - u[0]
    prod = gaussian(X1, -1.0, 0.9, 1.5) * gaussian(X2, 1.2, 0.7, -1.0)
    s_plus, s_minus = 1.6, 0.2  # wide in x1 + x2, narrow in x1 - x2: the particles are close to each other
    ent = np.exp(-((X1 + X2) ** 2) / (8 * s_plus**2) - ((X1 - X2) ** 2) / (8 * s_minus**2) + 1.0j * (X1 + X2))
    ent /= np.sqrt((np.abs(ent) ** 2).sum() * du * du)
    out = dict(u=u, prod=prod.astype(np.complex64), ent=ent.astype(np.complex64))
    for name, psi in (("prod", prod), ("ent", ent)):
        rho = np.abs(psi) ** 2
        assert abs(rho.sum() * du * du - 1) < 1e-3
        m2 = rho.sum(axis=1) * du  # density of x2 (rows)
        m2 = m2 / (m2.sum() * du)
        i1 = np.argmin(np.abs(u - 1.5))
        cond = rho[:, i1] / (rho[:, i1].sum() * du)  # density of x2 given x1 = 1.5
        out[f"{name}_m2"], out[f"{name}_cond"] = m2, cond
        sd_m = math.sqrt((u**2 * m2).sum() * du - ((u * m2).sum() * du) ** 2)
        sd_c = math.sqrt((u**2 * cond).sum() * du - ((u * cond).sum() * du) ** 2)
        if name == "prod":
            assert abs(sd_c / sd_m - 1) < 1e-6  # independent: learning x1 tells you nothing about x2
        else:
            assert sd_c < 0.3 * sd_m  # entangled: learning x1 pins down x2
        out[f"{name}_sd"] = np.array([sd_m, sd_c])
    return out


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------
ITEMS = {
    "slits": compute_slits,
    "packet": compute_packet,
    "carpet": compute_carpet,
    "fd": compute_fd,
    "measure": compute_measure,
    "uncert": compute_uncert,
    "tunnel": compute_tunnel,
    "oscillator": compute_oscillator,
    "hydrogen": compute_hydrogen,
    "spin": compute_spin,
    "bell": compute_bell,
    "pair": compute_pair,
    "numbers": compute_numbers,
    "extras": compute_extras,
}
_CACHE: dict = {}


def path(name: str):
    return DATA_DIR / f"{name}.npz"


def load(name: str) -> dict:
    if name not in _CACHE:
        f = path(name)
        if not f.exists():
            raise FileNotFoundError(f"{f} missing: run `python -m videos.quantum.compute {name}`")
        with np.load(f, allow_pickle=False) as z:
            _CACHE[name] = {k: z[k] for k in z.files}
    return _CACHE[name]


def slit_frames():
    """The double-slit movie, memory-mapped: (frames, y, x, 2) float16, (re, im) * FRAME_SCALE; frame k is at
    t = 4 k (time units of the simulation)."""
    return np.load(DATA_DIR / "slits_frames.npy", mmap_mode="r")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("items", nargs="*")
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    for name in args.items or list(ITEMS):
        if path(name).exists() and not args.force:
            print(f"  {name:<11} cached")
            continue
        t = time.time()
        out = ITEMS[name]()
        np.savez_compressed(path(name), **out)
        _CACHE.pop(name, None)
        print(f"  {name:<11} {time.time() - t:6.1f}s")


if __name__ == "__main__":
    main()
