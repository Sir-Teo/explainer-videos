"""Drums, bars and bells (Part 9, *Drums, Bars and Bells*).

A string and a column of air are long and thin, and their overtones are (nearly) whole multiples of the fundamental.
Things that are wide, or stiff, are not so obliging.  This module computes the overtones of the main kinds:

    membrane        a round skin: Bessel zeros; a skin of any shape, by finite elements (the isospectral drums of
                    Gordon, Webb and Wolpert); a skin loaded at the centre (the tabla); a rough estimate of what the
                    air does to a kettledrum
    bar             a free bar of any thickness profile (Euler-Bernoulli beam elements): the uniform bar, and the
                    arch cut under a marimba's bar that tunes its overtones
    bell            the partials of a tuned bell, as measured (the shell itself is not computed), and the pitch the
                    ear assigns to them
    plate           Chladni's figures on a square plate, in Ritz's approximation
    gong            one mode with a spring that stiffens or softens: the pitch glide

and ``modal`` turns any list of partials into sound.  No manim.  Checked in ``tests/music/test_percussion.py``
against Bessel zeros, Driscoll's eigenvalues for the isospectral drums, the classical bar ratios and Ramakrishna
and Sondhi's loaded membrane.
"""

from __future__ import annotations

import math
from collections import Counter

import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as sla
from scipy.linalg import eigh
from scipy.special import jn_zeros, jv

SR = 48_000


# ---------------------------------------------------------------------------
# Sound from partials
# ---------------------------------------------------------------------------
def modal(freqs, amps, decays, seconds: float, sr: int = SR, phases=None, attack: float = 0.0015) -> np.ndarray:
    """A struck thing as a sum of dying partials: ``amps[k] * exp(-decays[k] t) * sin(2 pi freqs[k] t)``, with a
    short rise so that the blow is not a click.  ``decays`` are in 1/s (amplitude)."""
    t = np.arange(int(seconds * sr)) / sr
    y = np.zeros(len(t))
    for k, (f, a, d) in enumerate(zip(freqs, amps, decays)):
        if f < 0.45 * sr:
            y += a * np.exp(-d * t) * np.sin(2 * np.pi * f * t + (0.0 if phases is None else phases[k]))
    y *= np.clip(t / attack, 0.0, 1.0)
    return y / max(np.abs(y).max(), 1e-12)


def mallet(freqs, contact_ms: float) -> np.ndarray:
    """How much of a blow each partial takes up when the mallet stays in contact for ``contact_ms``: a half-sine
    pulse's spectrum.  A soft mallet stays longer and leaves the high partials out."""
    tau = contact_ms / 1000.0
    x = np.asarray(freqs, dtype=float) * tau
    out = np.abs(np.cos(np.pi * x) / np.where(np.abs(1 - 4 * x * x) < 1e-9, 1e-9, 1 - 4 * x * x))
    return np.where(np.abs(1 - 4 * x * x) < 1e-6, np.pi / 4, out)


# ---------------------------------------------------------------------------
# Membranes
# ---------------------------------------------------------------------------
def drum_modes(count: int = 12) -> list[dict]:
    """The modes of an ideal round skin, lowest first.  Mode (m, n) has m nodal diameters and n nodal circles (the
    rim counted); its frequency is proportional to the n-th zero of the Bessel function J_m."""
    rows = []
    for m in range(0, 12):
        for n, z in enumerate(jn_zeros(m, 6), start=1):
            rows.append({"m": m, "n": n, "zero": float(z)})
    rows.sort(key=lambda r: r["zero"])
    base = rows[0]["zero"]
    for r in rows:
        r["ratio"] = r["zero"] / base
    return rows[:count]


def drum_shape(m: int, n: int, grid: int = 161) -> np.ndarray:
    """The shape of mode (m, n) on a square grid over the disc (NaN outside): J_m(z r) cos(m theta)."""
    z = jn_zeros(m, n)[-1]
    x = np.linspace(-1, 1, grid)
    xx, yy = np.meshgrid(x, x)
    r, th = np.hypot(xx, yy), np.arctan2(yy, xx)
    u = jv(m, z * r) * np.cos(m * th)
    u[r > 1] = np.nan
    return u / np.nanmax(np.abs(u))


def strike_amounts(modes, at: float) -> np.ndarray:
    """How strongly a blow at radius ``at`` (0 centre, 1 rim) starts each mode: the mode's own shape there.  A blow
    at the centre starts only the modes with no nodal diameter."""
    return np.array([abs(float(jv(r["m"], r["zero"] * at))) for r in modes])


GWW_1 = [(0, 0), (0, 1), (2, 3), (2, 2), (3, 2), (2, 1), (1, 1), (1, 0)]      # Gordon, Webb and Wolpert's two drums:
GWW_2 = [(1, 0), (0, 1), (0, 2), (2, 2), (2, 3), (3, 2), (2, 1), (1, 1)]      # seven half-squares each, differently joined


def polygon_area(p) -> float:
    x, y = np.array([q[0] for q in p], float), np.array([q[1] for q in p], float)
    return 0.5 * abs(float(np.dot(x, np.roll(y, -1)) - np.dot(y, np.roll(x, -1))))


def polygon_perimeter(p) -> float:
    q = np.array(p, float)
    return float(np.sum(np.linalg.norm(q - np.roll(q, -1, axis=0), axis=1)))


def membrane_eigs(polygon, count: int = 12, n: int = 24, shapes: bool = False):
    """The lowest eigenvalues of a skin stretched over a polygon whose corners are whole numbers and whose sides run
    along the grid or its diagonals: the numbers lambda for which a shape u with u = 0 on the rim satisfies
    laplacian(u) + lambda u = 0.  The frequencies go as sqrt(lambda).  Linear finite elements on a criss-cross mesh
    (each small square cut by both its diagonals, so that every side of the polygon is a side of triangles).
    With ``shapes`` also returns the node positions and the mode shapes."""
    from matplotlib.path import Path

    path = Path(np.array(list(polygon) + [polygon[0]], float))
    size = int(max(max(q) for q in polygon))
    idx: dict = {}
    pts: list = []

    def node(key):
        if key not in idx:
            idx[key] = len(pts)
            pts.append((key[0] / (2 * n), key[1] / (2 * n)))
        return idx[key]

    tris = []
    for i in range(size * n):
        for j in range(size * n):
            c = (2 * i + 1, 2 * j + 1)
            corners = [(2 * i, 2 * j), (2 * i + 2, 2 * j), (2 * i + 2, 2 * j + 2), (2 * i, 2 * j + 2)]
            for a in range(4):
                p, q = corners[a], corners[(a + 1) % 4]
                if path.contains_point(((p[0] + q[0] + c[0]) / (6 * n), (p[1] + q[1] + c[1]) / (6 * n))):
                    tris.append((node(p), node(q), node(c)))
    xy = np.array(pts)
    tri = np.array(tris)
    m_nodes = len(xy)
    x = xy[tri]                                               # (T, 3, 2)
    b = np.stack([x[:, 1, 1] - x[:, 2, 1], x[:, 2, 1] - x[:, 0, 1], x[:, 0, 1] - x[:, 1, 1]], axis=1)
    c = np.stack([x[:, 2, 0] - x[:, 1, 0], x[:, 0, 0] - x[:, 2, 0], x[:, 1, 0] - x[:, 0, 0]], axis=1)
    area = 0.5 * np.abs(b[:, 0] * c[:, 1] - b[:, 1] * c[:, 0])
    ke = (b[:, :, None] * b[:, None, :] + c[:, :, None] * c[:, None, :]) / (4 * area[:, None, None])
    rows = np.repeat(tri, 3, axis=1).ravel()
    cols = np.tile(tri, (1, 3)).ravel()
    k = sp.csr_matrix((ke.ravel(), (rows, cols)), shape=(m_nodes, m_nodes))
    mass = np.zeros(m_nodes)
    np.add.at(mass, tri.ravel(), np.repeat(area / 3.0, 3))
    edges = Counter()
    for t in tri:
        for a in range(3):
            edges[tuple(sorted((int(t[a]), int(t[(a + 1) % 3]))))] += 1
    rim = {v for e, cnt in edges.items() if cnt == 1 for v in e}
    inner = np.array([i for i in range(m_nodes) if i not in rim])
    w, v = sla.eigsh(k[inner][:, inner], k=count, M=sp.diags(mass[inner]), sigma=0, which="LM")
    order = np.argsort(w)
    if not shapes:
        return w[order]
    full = np.zeros((count, m_nodes))
    full[:, inner] = v[:, order].T
    full /= np.abs(full).max(axis=1, keepdims=True)
    return w[order], xy, full


def weyl(area: float, perimeter: float, lam) -> np.ndarray:
    """Weyl's law with its second term: about how many modes a skin has below the eigenvalue lambda.  The count
    depends on the skin's area and the length of its rim, and on nothing else about its shape."""
    lam = np.asarray(lam, dtype=float)
    return area * lam / (4 * np.pi) - perimeter * np.sqrt(lam) / (4 * np.pi)


def loaded_membrane(patch: float = 0.4, density: float = 9.0, m: int = 0, count: int = 3, n: int = 400) -> np.ndarray:
    """The eigenfrequencies (in units where an unloaded skin's (0,1) mode is at 2.405) of a round skin whose central
    disc, out to the fraction ``patch`` of the radius, is ``density`` times as heavy as the rest: the tabla's
    black patch.  Modes with m nodal diameters; the radial equation in finite differences, which is a symmetric
    tridiagonal eigenproblem."""
    from scipy.linalg import eigh_tridiagonal

    h = 1.0 / n
    r = (np.arange(n) + 0.5) * h                               # cell centres; u = 0 at r = 1
    edge = int(round(patch * n))                               # the patch ends on a cell boundary
    sigma = np.where(np.arange(n) < edge, density, 1.0)
    rp, rm = r + 0.5 * h, r - 0.5 * h
    main = (rp + rm) / (h * h) + m * m / r
    off = -rp[:-1] / (h * h)
    main[-1] += rp[-1] / (h * h)                               # the rim: u = 0 half a cell beyond the last centre
    w = np.sqrt(r * sigma)                                     # the weight of each cell: symmetrize by it
    d = main / (w * w)
    e = off / (w[:-1] * w[1:])
    lam = eigh_tridiagonal(d, e, select="i", select_range=(0, count - 1))[0]
    return np.sqrt(lam)


def tabla_modes(patch: float = 0.4, density: float = 9.0, count: int = 9) -> list[dict]:
    """The lowest modes of the loaded skin, with their ratios to the lowest."""
    rows = []
    for m in range(0, 6):
        for n, w in enumerate(loaded_membrane(patch, density, m, 3), start=1):
            rows.append({"m": m, "n": n, "w": float(w)})
    rows.sort(key=lambda r: r["w"])
    for r in rows:
        r["ratio"] = r["w"] / rows[0]["w"]
    return rows[:count]


def harmonic_misfit(ratios, upto: int = 5) -> float:
    """How far a set of mode ratios is from the whole numbers 1, 2, 3 ...: the worst distance in cents of the
    nearest mode to each whole number up to ``upto``."""
    worst = 0.0
    for k in range(1, upto + 1):
        worst = max(worst, min(abs(1200 * math.log2(r / k)) for r in ratios))
    return worst


def tune_tabla(patches=None, densities=None) -> dict:
    """The patch (its radius and how heavy it is) that brings the loaded skin's modes nearest to 1, 2, 3, 4, 5."""
    patches = np.arange(0.30, 0.56, 0.02) if patches is None else patches
    densities = np.arange(3.0, 14.01, 0.5) if densities is None else densities
    best = None
    for p in patches:
        for d in densities:
            ratios = [r["ratio"] for r in tabla_modes(float(p), float(d), 9)]
            miss = harmonic_misfit(ratios)
            if best is None or miss < best["misfit"]:
                best = {"patch": float(p), "density": float(d), "misfit": miss, "ratios": ratios}
    return best


def air_loaded(radius: float = 0.328, sigma: float = 0.26, sides: float = 2.0, count: int = 5, rho: float = 1.2) -> list[dict]:
    """A rough estimate of what the air does to a kettledrum's (m,1) modes.  A skin has to move the air next to it;
    for a wave of wavenumber k on the skin, the air it carries on each side weighs about rho/k per square metre,
    which is more for the long waves of the low modes.  So the low modes are slowed most.  (The kettle's enclosed
    air and the stiffness of the head, which real drums also need, are not in this estimate.)"""
    rows = []
    for m in range(1, count + 1):
        z = float(jn_zeros(m, 1)[0])
        k = z / radius
        rows.append({"m": m, "zero": z, "plain": z, "loaded": z / math.sqrt(1 + sides * rho / (k * sigma))})
    for key in ("plain", "loaded"):
        base = rows[0][key]
        for r in rows:
            r[key + "_ratio"] = r[key] / base
    return rows


TIMPANI_MEASURED = [1.00, 1.50, 1.98, 2.44, 2.91]      # modes (1,1) ... (5,1) of a kettledrum (Rossing, 1982)


# ---------------------------------------------------------------------------
# Bars
# ---------------------------------------------------------------------------
def bar_modes(thickness, length: float = 1.0, count: int = 4, shapes: bool = False):
    """The bending modes of a free bar whose thickness varies along it (``thickness``: one value per element, in
    units of the full thickness).  Euler-Bernoulli beam elements: stiffness goes as thickness cubed, mass as
    thickness.  Returns the frequencies in units where a uniform bar's lowest mode is 1 (and, with ``shapes``,
    the mode shapes at the nodes)."""
    t = np.asarray(thickness, dtype=float)
    ne = len(t)
    le = length / ne
    nd = 2 * (ne + 1)
    k = np.zeros((nd, nd))
    m = np.zeros((nd, nd))
    ke0 = np.array([[12, 6 * le, -12, 6 * le], [6 * le, 4 * le * le, -6 * le, 2 * le * le],
                    [-12, -6 * le, 12, -6 * le], [6 * le, 2 * le * le, -6 * le, 4 * le * le]]) / le ** 3
    me0 = np.array([[156, 22 * le, 54, -13 * le], [22 * le, 4 * le * le, 13 * le, -3 * le * le],
                    [54, 13 * le, 156, -22 * le], [-13 * le, -3 * le * le, -22 * le, 4 * le * le]]) * le / 420.0
    for e in range(ne):
        s = slice(2 * e, 2 * e + 4)
        k[s, s] += t[e] ** 3 * ke0
        m[s, s] += t[e] * me0
    w, v = eigh(k, m, subset_by_index=[0, count + 1])
    w = np.sqrt(np.maximum(w[2:], 0.0))                        # the first two are the bar moving and turning as a whole
    uniform = 22.373285448 / length ** 2                       # (4.730)^2: a uniform free bar's lowest mode
    if not shapes:
        return w / uniform
    sh = v[0::2, 2:].T
    return w / uniform, sh / np.abs(sh).max(axis=1, keepdims=True)


def arch(depth: float, width: float = 0.6, elements: int = 240, power: float = 2.0) -> np.ndarray:
    """A bar with an arch cut from its underside: over the middle ``width`` of its length the thickness dips to
    ``1 - depth`` at the centre, along a curve (a parabola for ``power`` 2)."""
    x = (np.arange(elements) + 0.5) / elements - 0.5
    u = np.clip(1 - np.abs(2 * x / width) ** power, 0.0, 1.0)
    return 1.0 - depth * u


def tune_bar(target: float = 4.0, width: float = 0.6, power: float = 3.0) -> dict:
    """The depth of arch for which the bar's second mode is ``target`` times its first (4 for a marimba, 3 for a
    xylophone), by bisection."""
    lo, hi = 0.0, 0.92
    for _ in range(40):
        mid = 0.5 * (lo + hi)
        f = bar_modes(arch(mid, width, power=power), count=3)
        if f[1] / f[0] < target:
            lo = mid
        else:
            hi = mid
    depth = 0.5 * (lo + hi)
    f = bar_modes(arch(depth, width, power=power), count=4)
    return {"depth": depth, "width": width, "modes": f, "ratios": f / f[0], "lowered": f[0]}


UNIFORM_BAR = [1.0, 2.7565, 5.4039, 8.9330]                  # a free uniform bar: (3.011, 5, 7, 9)^2 / 3.011^2, nearly


# ---------------------------------------------------------------------------
# Bells
# ---------------------------------------------------------------------------
BELL = [  # the partials of a well-tuned church bell, relative to its prime (Rossing; Lehr): name, ratio, strength, decay
    ("hum", 0.5, 0.55, 0.45), ("prime", 1.0, 0.80, 0.9), ("tierce", 1.2, 1.0, 1.1), ("quint", 1.5, 0.35, 1.6),
    ("nominal", 2.0, 0.95, 1.8), ("major third", 2.5, 0.30, 2.6), ("twelfth", 3.0, 0.55, 3.2), ("upper octave", 4.0, 0.40, 4.5),
]


def bell(prime: float, seconds: float = 4.0, tierce: float = 1.2, sr: int = SR, slow: float = 1.0) -> np.ndarray:
    """A tuned bell as its partials.  ``tierce`` is the ratio of the third partial to the prime: 1.2 for the minor
    third of every traditional bell, 1.25 for the major-third bells first cast in the 1980s."""
    f = [prime * (tierce if n == "tierce" else r) for n, r, _, _ in BELL]
    return modal(f, [a for _, _, a, _ in BELL], [d * slow * (prime / 262.0) ** 0.5 for _, _, _, d in BELL], seconds, sr, attack=0.002)


def bell_partials(prime: float, tierce: float = 1.2) -> list[dict]:
    return [{"name": n, "ratio": tierce if n == "tierce" else r, "hz": prime * (tierce if n == "tierce" else r), "amp": a} for n, r, a, _ in BELL]


# ---------------------------------------------------------------------------
# Plates
# ---------------------------------------------------------------------------
def chladni(m: int, n: int, sign: int = 1, grid: int = 201) -> np.ndarray:
    """A mode of a free square plate in Ritz's approximation (1909): cos(m pi x) cos(n pi y) plus or minus the same
    with m and n exchanged, on the square 0..1.  Sand gathers where this is zero."""
    x = np.linspace(0, 1, grid)
    xx, yy = np.meshgrid(x, x)
    return np.cos(m * np.pi * xx) * np.cos(n * np.pi * yy) + sign * np.cos(n * np.pi * xx) * np.cos(m * np.pi * yy)


def chladni_pitch(m: int, n: int) -> float:
    """Chladni's law, roughly: the frequency of the figure goes as m^2 + n^2."""
    return float(m * m + n * n)


# ---------------------------------------------------------------------------
# Gongs
# ---------------------------------------------------------------------------
def gong(hz: float, seconds: float = 3.0, glide: float = 0.12, decay: float = 1.3, partials=(1.0, 1.52, 2.03, 2.74, 3.46), sr: int = SR) -> np.ndarray:
    """A gong whose pitch moves as it dies away.  Each partial is a mode whose spring stiffens (``glide`` > 0) or
    softens (< 0) with the size of the motion, so its frequency is ``f (1 + glide A^2)`` while its amplitude A
    decays: a stiffening gong starts sharp and falls, a softening one starts flat and rises."""
    t = np.arange(int(seconds * sr)) / sr
    y = np.zeros(len(t))
    for k, r in enumerate(partials):
        a = np.exp(-decay * (1 + 0.5 * k) * t)
        f = hz * r * (1 + glide * a * a)
        y += (0.8 ** k) * a * np.sin(2 * np.pi * np.cumsum(f) / sr)
    y *= np.clip(t / 0.003, 0.0, 1.0)
    return y / max(np.abs(y).max(), 1e-12)


def gong_pitch(hz: float, glide: float, t, decay: float = 1.3) -> np.ndarray:
    """The frequency of the gong's lowest partial at time t."""
    return hz * (1 + glide * np.exp(-2 * decay * np.asarray(t, dtype=float)))


# ---------------------------------------------------------------------------
# Instruments for the Tune
# ---------------------------------------------------------------------------
def marimba(hz: float, seconds: float = 1.6, sr: int = SR, tuned: bool = True, soft: float = 1.2) -> np.ndarray:
    """A marimba bar over its resonator: the bar's partials (1 : 4 : about 10 when tuned, 1 : 2.76 : 5.40 when not),
    the lowest held up by a tube of air beneath it, struck by a yarn mallet."""
    ratios = [1.0, 4.0, 10.0] if tuned else UNIFORM_BAR[:3]
    f = [hz * r for r in ratios]
    amps = np.array([1.0, 0.28, 0.1]) * mallet(f, soft)
    return modal(f, amps, [2.4 * (hz / 262.0) ** 0.6, 9.0, 18.0], seconds, sr)


def steelpan(hz: float, seconds: float = 1.8, sr: int = SR) -> np.ndarray:
    """A steelpan note: a shallow dome hammered until its second and third partials are the octave and the twelfth
    of its first, with the slight swell of energy passing from the first into the others."""
    t = np.arange(int(seconds * sr)) / sr
    f = [hz, 2 * hz, 3 * hz, 4.0 * hz]
    swell = 1 - np.exp(-t / 0.03)
    y = (np.exp(-2.2 * t) * np.sin(2 * np.pi * f[0] * t) + 0.55 * swell * np.exp(-3.0 * t) * np.sin(2 * np.pi * f[1] * t)
         + 0.25 * swell * np.exp(-4.0 * t) * np.sin(2 * np.pi * f[2] * t) + 0.1 * swell * np.exp(-6.0 * t) * np.sin(2 * np.pi * f[3] * t))
    y *= np.clip(t / 0.002, 0.0, 1.0)
    return y / max(np.abs(y).max(), 1e-12)


def drum(hz: float, seconds: float = 1.2, at: float = 0.5, tuned: str = "ideal", sr: int = SR, damping: float = 5.0) -> np.ndarray:
    """A round drum whose lowest mode is at ``hz``, struck at radius ``at``.  ``tuned``: "ideal" for a bare skin,
    "timpani" for a kettledrum's measured modes (then ``hz`` is its principal note)."""
    if tuned == "timpani":
        f = [hz * r for r in TIMPANI_MEASURED] + [hz * 0.85]
        amps = [1.0, 0.8, 0.55, 0.35, 0.2, 0.25]
        dec = [2.0, 2.6, 3.4, 4.5, 6.0, 30.0]
        return modal(f, amps, dec, seconds, sr)
    modes = drum_modes(14)
    f = [hz * r["ratio"] for r in modes]
    amps = strike_amounts(modes, at) * mallet(f, 1.0)
    # the modes with no nodal diameter push air in and out as a whole: they radiate well, and so die quickly
    dec = [damping * (1 + 0.6 * r["ratio"]) * (4.0 if r["m"] == 0 else 1.0) for r in modes]
    return modal(f, amps, dec, seconds, sr)
