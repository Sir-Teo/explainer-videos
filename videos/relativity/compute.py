"""Precompute everything numerical in the general-relativity video.

    python -m videos.relativity.compute               # everything missing (~6 min on 4 cores)
    python -m videos.relativity.compute mercury bh80  # specific items
    python -m videos.relativity.compute --force       # recompute

Results are cached in ``.cache/relativity/<name>.npz``; scenes call ``load(name)``.  Nothing here is a cartoon:
orbits, light rays and the black-hole images are integrations of Schwarzschild geodesics, the tidal ring and the
ball of test particles are integrations of Newtonian gravity, parallel transport is an ODE solve on the sphere,
and every number the narration quotes is computed here and asserted against the formula that predicts it.
Where a picture is exaggerated (a ring hundreds of kilometres wide, a "Mercury" around a far denser star),
the item says by how much, and the scene labels it.

Items:
    consts      constants and the headline numbers (Schwarzschild radii, GPS rates, 8 pi G / c^4, ...)
    aging       proper time of candidate worldlines of a ball thrown up and caught 2 s later
    rocket      light pulses climbing an accelerating rocket (Rindler worldlines): the redshift g h / c^2
    gps         clock rate of a circular orbit vs radius: gravity, speed and their sum
    tidal       a ring of free particles falling toward the Earth (Newton), seen from its centre
    ball        a ball of free test particles: in vacuum (outside a mass) and inside uniform matter
    transport   parallel transport on a sphere: the 90-90-90 triangle, latitude circles, small loops
    sgeo        geodesics on a sphere from one point (the geodesic equation with its Christoffel symbols)
    mercury     Mercury's perihelion advance from the exact orbit integral; an exaggerated rosette
    light       light deflection at the solar limb; exact null geodesics past a black hole
    bh80, bh20  ray-traced thin-disk black hole seen at inclinations 80 and 20 degrees
    cosmo       the scale factor of a flat Lambda-CDM universe (Planck 2018) and when it starts to accelerate
    gw          GW150914: whitened LIGO strain (from data/gw150914.json), its time-frequency map, the quadrupole chirp
"""

from __future__ import annotations

import argparse
import json
import math
import time
from pathlib import Path

import numpy as np
from scipy.integrate import quad, solve_ivp

from explainer.tts import REPO_ROOT

DATA_DIR = REPO_ROOT / ".cache" / "relativity"
SNAPSHOT = Path(__file__).resolve().parent / "data" / "gw150914.json"

# ---------------------------------------------------------------------------
# Constants (CODATA 2018, IAU 2015 nominal values, IERS)
# ---------------------------------------------------------------------------
c = 299_792_458.0
G = 6.674_30e-11
GM_SUN = 1.327_124_400_18e20  # m^3/s^2 (IAU)
R_SUN = 6.957e8  # m, IAU nominal solar radius
M_SUN = GM_SUN / G
GM_EARTH = 3.986_004_418e14
R_EARTH = 6.371e6  # mean radius
g0 = 9.81
DAY = 86_400.0
CENTURY_DAYS = 36_525.0
ARCSEC = math.pi / (180 * 3600)

# Mercury, Venus, Earth: semi-major axis (m), eccentricity, sidereal period (days)  (NASA planetary fact sheet)
AU = 1.495_978_707e11
PLANETS = {
    "Mercury": (0.387_098 * AU, 0.205_630, 87.9691),
    "Venus": (0.723_332 * AU, 0.006_772, 224.701),
    "Earth": (1.000_001_018 * AU, 0.016_709, 365.256_363),
}


def rng(seed: int) -> np.random.Generator:
    return np.random.Generator(np.random.PCG64(seed))


# ---------------------------------------------------------------------------
def compute_consts():
    rs_sun = 2 * GM_SUN / c**2
    rs_earth = 2 * GM_EARTH / c**2
    kappa = 8 * math.pi * G / c**4
    earth_surface = GM_EARTH / (R_EARTH * c**2)
    assert abs(rs_sun - 2953.25) < 0.1 and abs(rs_earth * 1000 - 8.870) < 0.002
    assert abs(kappa - 2.077e-43) < 0.001e-43
    deflect = 4 * GM_SUN / (c**2 * R_SUN) / ARCSEC
    assert abs(deflect - 1.751) < 0.001
    # Pound-Rebka: 22.5 m tower
    pr = g0 * 22.5 / c**2
    assert abs(pr - 2.456e-15) < 0.01e-15
    # Light travel time Sun -> Earth
    t_sun = AU / c
    assert abs(t_sun - 499.0) < 0.1
    # LIGO: 4 km arm, peak strain 1.0e-21
    dL = 1.0e-21 * 4000.0
    proton = 2 * 0.841e-15
    assert abs(dL - 4e-18) < 1e-30 and 400 < proton / dL < 450
    return dict(rs_sun=rs_sun, rs_earth=rs_earth, kappa=kappa, earth_surface=earth_surface,
                earth_us_per_day=earth_surface * DAY * 1e6, deflect=deflect, pound_rebka=pr, t_sun=t_sun,
                ligo_dL=dL, proton_ratio=proton / dL)


# ---------------------------------------------------------------------------
# Maximal aging: a ball thrown up at t = 0 and caught at t = T, at the same place.
#   tau = int sqrt(1 + 2 g z / c^2 - v^2 / c^2) dt  ~=  T + (1/c^2) int (g z - v^2 / 2) dt
# ---------------------------------------------------------------------------
AGE_T = 2.0


def aging_excess(z, t):
    """(tau - T) for a worldline z(t), from the expansion (exact to O(c^-4), i.e. to ~1e-32 s here)."""
    v = np.gradient(z, t, edge_order=2)
    return np.trapezoid(g0 * z - 0.5 * v * v, t) / c**2


def compute_aging():
    T = AGE_T
    t = np.linspace(0, T, 4001)
    hs = np.linspace(0, 12, 121)
    # Parabolas through both events with peak height h
    para = np.array([4 * h * t * (T - t) / T**2 for h in hs])
    excess = np.array([aging_excess(z, t) for z in para])
    closed = (2 / 3 * g0 * hs * T - 8 * hs**2 / (3 * T)) / c**2
    assert np.max(np.abs(excess - closed)) < 1e-6 * np.max(np.abs(closed))
    h_star = g0 * T**2 / 8
    best = hs[np.argmax(excess)]
    assert abs(best - h_star) < 0.06 and abs(h_star - 4.905) < 0.001
    tau_star = g0**2 * T**3 / (24 * c**2)
    assert abs(np.max(closed) - tau_star) / tau_star < 1e-3
    assert abs(tau_star - 3.57e-16) < 0.01e-16
    # Check the expansion against the exact square root at 40 digits for the Newtonian path
    import mpmath as mp

    mp.mp.dps = 40
    cc, gg, TT, hh = mp.mpf(c), mp.mpf(g0), mp.mpf(T), mp.mpf(h_star)

    def integrand(tt):
        z = 4 * hh * tt * (TT - tt) / TT**2
        v = 4 * hh * (TT - 2 * tt) / TT**2
        return mp.sqrt(1 + 2 * gg * z / cc**2 - v**2 / cc**2)

    exact = mp.quad(integrand, [0, TT]) - TT
    assert abs(float(exact) - tau_star) / tau_star < 1e-6
    # Other shapes that are not parabolas: a "hover" path (up fast, wait, down fast) and a lopsided one
    others = []
    for kind in ("hover", "lopsided", "high"):
        if kind == "hover":
            z = np.minimum(1.0, np.minimum(t, T - t) / 0.35) ** 1 * 4.0
            z = 4.0 * np.clip(np.minimum(t, T - t) / 0.4, 0, 1) ** 2 * (3 - 2 * np.clip(np.minimum(t, T - t) / 0.4, 0, 1))
        elif kind == "lopsided":
            s = t / T
            z = 4.9 * 6.75 * s**2 * (1 - s) / 1.0  # peak at s = 2/3
            z = z / z.max() * 4.9
        else:
            z = 4 * 9.0 * t * (T - t) / T**2
        others.append(z)
    others = np.array(others)
    oex = np.array([aging_excess(z, t) for z in others])
    assert np.all(oex < tau_star * 0.95)
    return dict(t=t, hs=hs, excess=excess, closed=closed, h_star=h_star, tau_star=tau_star, others=others,
                others_excess=oex)


# ---------------------------------------------------------------------------
# The accelerating rocket (units c = 1): floor at x = 1/a, ceiling at x = 1/a + h.  A point at fixed height in the
# rocket follows x^2 - t^2 = X^2.  A light pulse emitted from the floor at the floor's proper time s reaches the
# ceiling at the ceiling's proper time s * (1 + a h) * (a_top / a)... we just trace the pulses and measure.
# ---------------------------------------------------------------------------
def compute_rocket():
    a, h = 1.0, 0.5  # floor acceleration 1, rocket height 0.5 (so a h / c^2 = 0.5: exaggerated)
    X0, X1 = 1 / a, 1 / a + h
    s_floor = np.arange(0, 1.61, 0.2)  # floor proper times of emission
    te = X0 * np.sinh(s_floor / X0)
    xe = X0 * np.cosh(s_floor / X0)
    # pulse: x - t = xe - te = u (constant); meets ceiling hyperbola x^2 - t^2 = X1^2 => (x-t)(x+t) = X1^2
    u = xe - te
    v = X1**2 / u
    tr, xr = (v - u) / 2, (v + u) / 2
    s_ceiling = X1 * np.arcsinh(tr / X1)
    ratio = np.diff(s_ceiling) / np.diff(s_floor)
    assert np.allclose(ratio, X1 / X0)  # = 1 + a h exactly
    return dict(a=a, h=h, s_floor=s_floor, te=te, xe=xe, tr=tr, xr=xr, s_ceiling=s_ceiling, ratio=ratio[0])


# ---------------------------------------------------------------------------
# Clock rates in circular orbit vs a clock on the ground (Earth's rotation neglected): microseconds per day
# ---------------------------------------------------------------------------
def orbit_rates(r):
    grav = GM_EARTH * (1 / R_EARTH - 1 / r) / c**2 * DAY * 1e6
    speed = -GM_EARTH / (2 * r * c**2) * DAY * 1e6
    return grav, speed, grav + speed


def compute_gps():
    r = np.linspace(R_EARTH, 50e6, 600)
    grav, speed, net = orbit_rates(r)
    r_gps = 26_560e3
    g_gps, s_gps, n_gps = orbit_rates(r_gps)
    assert abs(g_gps - 45.7) < 0.05 and abs(s_gps + 7.2) < 0.05 and abs(n_gps - 38.5) < 0.05
    km_per_day = n_gps * 1e-6 * c / 1000
    assert abs(km_per_day - 11.5) < 0.1
    r_iss = R_EARTH + 420e3
    _, _, n_iss = orbit_rates(r_iss)
    r_zero = 1.5 * R_EARTH
    assert abs(orbit_rates(r_zero)[2]) < 1e-9
    return dict(r=r, grav=grav, speed=speed, net=net, r_gps=r_gps, gps=np.array([g_gps, s_gps, n_gps]),
                km_per_day=km_per_day, r_iss=r_iss, n_iss=n_iss, r_zero=r_zero)


# ---------------------------------------------------------------------------
# Tides: a ring of 24 particles (radius 800 km) released at rest around a point 4 Earth radii from the centre.
# ---------------------------------------------------------------------------
def compute_tidal():
    n = 24
    R0, ring = 4 * R_EARTH, 800e3
    ang = np.linspace(0, 2 * np.pi, n, endpoint=False)
    pos0 = np.stack([np.concatenate([[0.0], ring * np.cos(ang)]), np.concatenate([[R0], R0 + ring * np.sin(ang)])], 1)

    def rhs(_, y):
        p = y[: 2 * (n + 1)].reshape(-1, 2)
        r = np.linalg.norm(p, axis=1, keepdims=True)
        acc = -GM_EARTH * p / r**3
        return np.concatenate([y[2 * (n + 1):], acc.ravel()])

    y0 = np.concatenate([pos0.ravel(), np.zeros(2 * (n + 1))])
    # fall until the centre reaches 1.6 Earth radii
    t_end = 0.0

    def hit(_, y):
        return y[1] - 1.6 * R_EARTH

    hit.terminal = True
    sol = solve_ivp(rhs, [0, 20000], y0, rtol=1e-11, atol=1e-3, events=hit, dense_output=True)
    t_end = sol.t_events[0][0]
    ts = np.linspace(0, t_end, 300)
    Y = sol.sol(ts)[: 2 * (n + 1)].T.reshape(len(ts), n + 1, 2)
    rel = Y[:, 1:, :] - Y[:, :1, :]
    # Linear tidal prediction at the start: d2 xi / dt2 = (GM/r^3) diag(-1, 2) xi
    # (checked on a 1 km ring, where the linear tidal law is exact to ~1e-4)
    k = GM_EARTH / R0**3
    small = np.stack([np.concatenate([[0.0], 1e3 * np.cos(ang)]), np.concatenate([[R0], R0 + 1e3 * np.sin(ang)])], 1)
    acc0 = rhs(0, np.concatenate([small.ravel(), np.zeros(2 * (n + 1))]))[2 * (n + 1):].reshape(-1, 2)
    rel_acc = acc0[1:] - acc0[:1]
    pred = k * np.stack([-1e3 * np.cos(ang), 2 * 1e3 * np.sin(ang)], 1)
    assert np.max(np.abs(rel_acc - pred)) < 1e-3 * np.max(np.abs(pred))
    # Area is preserved to first order (traceless tidal tensor); the ring stretches along the radius
    def area(P):
        x, y = P[:, 0], P[:, 1]
        return 0.5 * abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)))

    a0 = area(rel[0])
    stretch = (rel[:, :, 1].max(axis=1) - rel[:, :, 1].min(axis=1)) / (2 * ring)
    squeeze = (rel[:, :, 0].max(axis=1) - rel[:, :, 0].min(axis=1)) / (2 * ring)
    assert stretch[-1] > 1.3 and squeeze[-1] < 0.85
    return dict(ts=ts, pos=Y, rel=rel, ring=ring, R0=R0, t_end=t_end, stretch=stretch, squeeze=squeeze,
                area=np.array([area(P) / a0 for P in rel]))


# ---------------------------------------------------------------------------
# A ball of test particles (Baez & Bunn).  Units: lengths in ball radii, times in units where the relevant rate is 1.
#   vacuum: released near a point mass; acceleration relative to the centre from the exact inverse square law
#   matter: inside a uniform-density body, where g = -(4 pi G rho / 3) r exactly
# ---------------------------------------------------------------------------
def compute_ball():
    r = rng(7)
    n = 260
    # points on a Fibonacci sphere (the surface of the ball) plus a few inside
    i = np.arange(n) + 0.5
    phi = np.arccos(1 - 2 * i / n)
    th = np.pi * (1 + 5**0.5) * i
    surf = np.stack([np.cos(th) * np.sin(phi), np.sin(th) * np.sin(phi), np.cos(phi)], 1)
    inner = r.normal(size=(60, 3))
    inner = inner / np.linalg.norm(inner, axis=1, keepdims=True) * r.uniform(0, 1, (60, 1)) ** (1 / 3)
    pts = np.concatenate([surf, inner])

    # vacuum: point mass at distance D below (along -z), GM chosen so the tidal rate GM/D^3 = 1
    D = 6.0
    GM = D**3
    ts = np.linspace(0, 1.2, 160)

    def accel(p):
        q = p + np.array([0, 0, D])
        return -GM * q / np.linalg.norm(q, axis=-1, keepdims=True) ** 3

    def rhs(_, y):
        p = y[: y.size // 2].reshape(-1, 3)
        a = accel(p) - accel(np.zeros((1, 3)))  # relative to the freely falling centre (to tidal order)
        return np.concatenate([y[y.size // 2:], a.ravel()])

    y0 = np.concatenate([pts.ravel(), np.zeros(pts.size)])
    sol = solve_ivp(rhs, [0, ts[-1]], y0, t_eval=ts, rtol=1e-9, atol=1e-11)
    vac = sol.y[: pts.size].T.reshape(len(ts), -1, 3)
    # volume from the principal axes of the surface points (an ellipsoid fit)
    def vol(P):
        S = P[:n]
        cov = np.cov(S.T, bias=True)
        return float(np.sqrt(np.linalg.det(cov * 3)))  # = a b c for an ellipsoid surface sample
    v_vac = np.array([vol(P) for P in vac]) / vol(pts)
    # Volume preserved to second order in t at first: V''(0) = 0 (traceless tidal tensor)
    dt = ts[1] - ts[0]
    vdd = (v_vac[2] - 2 * v_vac[1] + v_vac[0]) / dt**2
    assert abs(vdd) < 0.05
    # matter: a(r) = -(4 pi G rho / 3) r with 4 pi G rho = 1 => every distance shrinks as cos(t / sqrt(3))
    mat = np.array([pts * np.cos(t / np.sqrt(3)) for t in ts])
    v_mat = np.cos(ts / np.sqrt(3)) ** 3
    vdd_m = (v_mat[2] - 2 * v_mat[1] + v_mat[0]) / dt**2
    assert abs(vdd_m + 1.0) < 0.01  # V''/V = -4 pi G rho
    return dict(ts=ts, pts=pts, vac=vac, v_vac=v_vac, mat=mat, v_mat=v_mat, n_surf=n)


# ---------------------------------------------------------------------------
# Parallel transport on the unit sphere.  Coordinates (theta = colatitude, phi).  A vector V = V^th e_th + V^ph e_ph
# transported along x(s) obeys dV^l/ds + Gamma^l_mn x'^m V^n = 0 with Gamma^th_phph = -sin cos, Gamma^ph_thph = cot.
# We store orthonormal components (V^th, sin(theta) V^ph) and the 3D vector along each path.
# ---------------------------------------------------------------------------
def sph(th, ph):
    return np.stack([np.sin(th) * np.cos(ph), np.sin(th) * np.sin(ph), np.cos(th)], -1)


def basis(th, ph):
    e_th = np.stack([np.cos(th) * np.cos(ph), np.cos(th) * np.sin(ph), -np.sin(th)], -1)
    e_ph = np.stack([-np.sin(ph), np.cos(ph), np.zeros_like(ph)], -1)
    return e_th, e_ph


def transport(th_of_s, ph_of_s, dth, dph, s_span, V0, n=400):
    """Integrate parallel transport along (th(s), ph(s)); V0 = (V^th, V^ph) coordinate components."""

    def rhs(s, V):
        th, ph = th_of_s(s), ph_of_s(s)
        a, b = dth(s), dph(s)
        Vth, Vph = V
        dVth = np.sin(th) * np.cos(th) * b * Vph
        dVph = -(np.cos(th) / np.sin(th)) * (a * Vph + b * Vth)
        return [dVth, dVph]

    ss = np.linspace(*s_span, n)
    sol = solve_ivp(rhs, s_span, V0, t_eval=ss, rtol=1e-11, atol=1e-12)
    th, ph = th_of_s(ss), ph_of_s(ss)
    e_th, e_ph = basis(th, ph)
    V3 = sol.y[0][:, None] * e_th + sol.y[1][:, None] * np.sin(th)[:, None] * e_ph
    return ss, th, ph, V3


def compute_transport():
    eps = 1e-6
    out = {}
    # The 90-90-90 triangle: pole -> (equator, phi = 0) -> (equator, phi = pi/2) -> pole.  Start just off the pole.
    legs = []
    # leg 1: down the meridian phi = 0 from theta = eps to pi/2, vector pointing along +phi-direction initially
    V = None
    paths, vecs = [], []
    s1 = transport(lambda s: s, lambda s: 0 * s, lambda s: 1 + 0 * s, lambda s: 0 * s, (eps, np.pi / 2),
                   [1.0, 0.0])  # starts pointing along e_theta (south)
    paths.append(sph(s1[1], s1[2]))
    vecs.append(s1[3])
    v_end = s1[3][-1]
    e_th, e_ph = basis(np.array(np.pi / 2), np.array(0.0))
    V0 = [float(v_end @ e_th), float(v_end @ e_ph)]
    s2 = transport(lambda s: np.pi / 2 + 0 * s, lambda s: s, lambda s: 0 * s, lambda s: 1 + 0 * s, (0, np.pi / 2), V0)
    paths.append(sph(s2[1], s2[2]))
    vecs.append(s2[3])
    v_end = s2[3][-1]
    e_th, e_ph = basis(np.array(np.pi / 2), np.array(np.pi / 2))
    V0 = [float(v_end @ e_th), float(v_end @ e_ph)]
    s3 = transport(lambda s: np.pi / 2 - s, lambda s: np.pi / 2 + 0 * s, lambda s: -1 + 0 * s, lambda s: 0 * s,
                   (0, np.pi / 2 - eps), V0)
    paths.append(sph(s3[1], s3[2]))
    vecs.append(s3[3])
    start, end = vecs[0][0], vecs[2][-1]
    turn = math.degrees(math.atan2(np.dot(np.cross(start, end), [0, 0, 1]), np.dot(start, end)))
    assert abs(abs(turn) - 90) < 0.01, turn
    out["tri_paths"] = np.array(paths)
    out["tri_vecs"] = np.array(vecs)
    out["tri_turn"] = turn

    # Latitude circles: colatitude th0, once around eastward; holonomy 2 pi (1 - cos th0)
    th0s = np.radians([30, 60, 90, 120])
    lat_paths, lat_vecs, hol = [], [], []
    for th0 in th0s:
        ss, th, ph, V3 = transport(lambda s, th0=th0: th0 + 0 * s, lambda s: s, lambda s: 0 * s, lambda s: 1 + 0 * s,
                                   (0, 2 * np.pi), [1.0, 0.0], n=600)
        e_th, e_ph = basis(np.array(th0), np.array(0.0))
        ang = math.atan2(V3[-1] @ e_ph, V3[-1] @ e_th)
        expect = (2 * np.pi * (1 - np.cos(th0)) + np.pi) % (2 * np.pi) - np.pi
        assert abs(((ang - expect + np.pi) % (2 * np.pi)) - np.pi) < 1e-6 or abs(((ang + expect + np.pi) % (2 * np.pi)) - np.pi) < 1e-6
        lat_paths.append(sph(th, ph))
        lat_vecs.append(V3)
        hol.append(2 * np.pi * (1 - np.cos(th0)))
    out["lat_th0"] = th0s
    out["lat_paths"] = np.array(lat_paths)
    out["lat_vecs"] = np.array(lat_vecs)
    out["lat_holonomy"] = np.array(hol)

    # Small loops: caps of half-angle a; rotation angle vs enclosed area (unit sphere: slope K = 1)
    caps = np.radians(np.linspace(5, 60, 12))
    areas = 2 * np.pi * (1 - np.cos(caps))
    angles = []
    for th0 in caps:
        ss, th, ph, V3 = transport(lambda s, th0=th0: th0 + 0 * s, lambda s: s, lambda s: 0 * s, lambda s: 1 + 0 * s,
                                   (0, 2 * np.pi), [1.0, 0.0], n=50)
        e_th, e_ph = basis(np.array(th0), np.array(0.0))
        ang = math.atan2(V3[-1] @ e_ph, V3[-1] @ e_th)
        angles.append(abs(ang))
    angles = np.array(angles)
    assert np.allclose(angles, areas, rtol=1e-6)
    out["cap_areas"] = areas
    out["cap_angles"] = angles

    # Foucault's pendulum in Paris (Pantheon, 48.846 N): degrees per sidereal day, and the period
    lat = math.radians(48.846)
    out["foucault_deg"] = 360 * math.sin(lat)
    out["foucault_hours"] = 23.9345 / math.sin(lat)
    assert abs(out["foucault_deg"] - 271.1) < 0.1 and abs(out["foucault_hours"] - 31.8) < 0.05
    return out


# ---------------------------------------------------------------------------
# Geodesics on the unit sphere from one point, by integrating x'' + Gamma x' x' = 0
# ---------------------------------------------------------------------------
def compute_sgeo():
    th0, ph0 = np.radians(55), np.radians(-20)

    def rhs(_, y):
        th, ph, dth, dph = y
        return [dth, dph, np.sin(th) * np.cos(th) * dph**2, -2 * (np.cos(th) / np.sin(th)) * dth * dph]

    heads = np.radians(np.arange(0, 360, 30))
    curves = []
    ss = np.linspace(0, np.pi, 300)
    for h in heads:
        # unit-speed initial velocity: dth = cos(h), sin(th) dph = sin(h)
        y0 = [th0, ph0, np.cos(h), np.sin(h) / np.sin(th0)]
        sol = solve_ivp(rhs, [0, np.pi], y0, t_eval=ss, rtol=1e-10, atol=1e-12)
        P = sph(sol.y[0], sol.y[1])
        curves.append(P)
    curves = np.array(curves)
    anti = -sph(np.array(th0), np.array(ph0))
    assert np.max(np.linalg.norm(curves[:, -1] - anti, axis=1)) < 1e-6  # all meet at the antipode
    # each is a great circle: points lie in a plane through the origin
    for P in curves:
        n_ = np.cross(P[10], P[60])
        assert np.max(np.abs(P @ n_)) < 1e-7
    # Great circle vs latitude arc between (60 N, 0 E) and (60 N, 90 E) on the unit sphere
    lat = math.radians(60)
    arc_lat = (math.pi / 2) * math.cos(lat)
    arc_gc = math.acos(math.sin(lat) ** 2 + math.cos(lat) ** 2 * math.cos(math.pi / 2))
    assert abs(arc_lat - 0.7854) < 1e-4 and abs(arc_gc - 0.7227) < 1e-4
    return dict(curves=curves, start=sph(np.array(th0), np.array(ph0)), arc_lat=arc_lat, arc_gc=arc_gc)


# ---------------------------------------------------------------------------
# Mercury.  Orbit equation u'' + u = A + B u^2 (u = 1/r, B = 3 GM / c^2).  Its first integral is a cubic
#   u'^2 = (2B/3)(u - u1)(u2 - u)(u3 - u),  u1 = 1/r_aphelion, u2 = 1/r_perihelion,
# so the angle from aphelion to aphelion is 2 int du / sqrt(cubic): exact, no time stepping.
# ---------------------------------------------------------------------------
def apsidal_angle(a: float, e: float, B: float) -> float:
    u1, u2 = 1 / (a * (1 + e)), 1 / (a * (1 - e))
    u3 = 3 / (2 * B) - u1 - u2
    k = 2 * B / 3

    def f(psi):
        u = u1 + (u2 - u1) * (1 - np.cos(psi)) / 2
        # du = (u2 - u1)/2 sin psi dpsi; (u - u1)(u2 - u) = ((u2 - u1)/2)^2 sin^2 psi
        return 1 / np.sqrt(k * (u3 - u))

    val, err = quad(f, 0, np.pi, epsabs=0, epsrel=2e-14, limit=200)
    return 2 * val


def precession_per_century(name: str):
    a, e, P = PLANETS[name]
    B = 3 * GM_SUN / c**2
    dphi = apsidal_angle(a, e, B) - 2 * np.pi
    first_order = 6 * np.pi * GM_SUN / (c**2 * a * (1 - e**2))
    per_century = dphi * CENTURY_DAYS / P / ARCSEC
    return dphi, first_order, per_century, CENTURY_DAYS / P


def rosette(scale_B: float, a=1.0, e=0.45, orbits=7, n=4000):
    """An exaggerated orbit: same equation with B large enough to see; integrate u(phi), and time along it."""
    B = scale_B
    u1, u2 = 1 / (a * (1 + e)), 1 / (a * (1 - e))
    u3 = 3 / (2 * B) - u1 - u2
    A = (B / 3) * (u1 * u2 + u1 * u3 + u2 * u3)  # from matching the u coefficient: 2A = (2B/3)(u1u2 + u1u3 + u2u3)

    def rhs(_, y):
        return [y[1], A + B * y[0] ** 2 - y[0]]

    # start at perihelion: u = u2, u' = 0
    span = orbits * apsidal_angle(a, e, B)
    phis = np.linspace(0, span, n)
    sol = solve_ivp(rhs, [0, span], [u2, 0.0], t_eval=phis, rtol=1e-11, atol=1e-13)
    u = sol.y[0]
    # time: dphi/dt ~ L u^2 with L^2 = A^-1 (units GM = 1)
    L = 1 / math.sqrt(A)
    dt = np.diff(phis) / (L * (0.5 * (u[1:] + u[:-1])) ** 2)
    tt = np.concatenate([[0], np.cumsum(dt)])
    # Newtonian ellipse with the same A (B = 0): u = A (1 + e' cos phi) through the same perihelion
    eN = u2 / A - 1
    uN = A * (1 + eN * np.cos(phis))
    return phis, u, tt, uN, apsidal_angle(a, e, B) - 2 * np.pi, A


def compute_mercury():
    out = {}
    for name in PLANETS:
        dphi, first, cent, per = precession_per_century(name)
        out[name + "_dphi"] = dphi
        out[name + "_first"] = first
        out[name + "_century"] = cent
        out[name + "_orbits"] = per
    assert abs(out["Mercury_century"] - 42.98) < 0.01
    assert abs(out["Mercury_dphi"] / out["Mercury_first"] - 1) < 1e-6
    assert abs(out["Venus_century"] - 8.62) < 0.01 and abs(out["Earth_century"] - 3.84) < 0.01
    assert abs(out["Mercury_orbits"] - 415.2) < 0.05
    # Exaggerated rosette: B chosen so the ellipse turns ~17 degrees per orbit (590,000 times Mercury's)
    phis, u, tt, uN, dphi_x, A = rosette(scale_B=0.035)
    out.update(ros_phi=phis, ros_u=u, ros_t=tt, ros_uN=uN, ros_dphi=dphi_x, ros_A=A)
    exag = dphi_x / out["Mercury_dphi"]
    out["ros_exaggeration"] = exag
    # Moon's mean angular diameter, 31.1' -> 43" is ~1/43 of it
    out["moon_arcsec"] = 31.1 * 60
    return out


# ---------------------------------------------------------------------------
# Light: deflection at the solar limb, exactly; null rays past a black hole (units r_s = 1)
# ---------------------------------------------------------------------------
def deflection_exact(b_over_rs: float) -> float:
    """Total deflection of a null ray with impact parameter b (units r_s = 1):
    delta = 2 int_0^{u0} du / sqrt(1/b^2 - u^2 + u^3) - pi, u0 = 1 / r_min.  With u = u0 sin(psi) and
    1/b^2 = u0^2 - u0^3 the integrand becomes sqrt(1 + s) / sqrt(1 + s - u0 (1 + s + s^2)), s = sin(psi),
    which has no cancellation even for b = 235,000 r_s (the Sun's limb)."""
    from scipy.optimize import brentq

    f = lambda u: 1 / b_over_rs**2 - u**2 + u**3  # noqa: E731
    u0 = brentq(f, 0, 2 / 3, xtol=1e-300, rtol=1e-15)

    def g(psi):
        s = np.sin(psi)
        return np.sqrt(1 + s) / np.sqrt(1 + s - u0 * (1 + s + s * s))

    val, _ = quad(g, 0, np.pi / 2, epsabs=0, epsrel=1e-13, limit=400)
    return 2 * val - np.pi


def null_ray(b, x0=-14.0, max_len=60.0, step=0.01):
    """Trace a ray coming from the left at height b, with the 'Binet' force x'' = -1.5 h^2 x / r^5 (r_s = 1)."""
    p = np.array([x0, b], float)
    v = np.array([1.0, 0.0])
    h2 = (p[0] * v[1] - p[1] * v[0]) ** 2
    pts = [p.copy()]
    s = 0.0

    def acc(q):
        r = np.hypot(*q)
        return -1.5 * h2 * q / r**5

    while s < max_len:
        r = np.hypot(*p)
        if r < 1.0:
            return np.array(pts), True
        if r > 20 and np.dot(p, v) > 0:
            break
        dt = step * max(0.15, min(1.0, r / 3))
        k1v = acc(p); k1x = v
        k2v = acc(p + 0.5 * dt * k1x); k2x = v + 0.5 * dt * k1v
        k3v = acc(p + 0.5 * dt * k2x); k3x = v + 0.5 * dt * k2v
        k4v = acc(p + dt * k3x); k4x = v + dt * k3v
        p = p + dt / 6 * (k1x + 2 * k2x + 2 * k3x + k4x)
        v = v + dt / 6 * (k1v + 2 * k2v + 2 * k3v + k4v)
        s += dt
        pts.append(p.copy())
    return np.array(pts), False


def compute_light():
    out = {}
    b = R_SUN / (2 * GM_SUN / c**2)  # solar limb in units of r_s
    d = deflection_exact(b) / ARCSEC
    weak = 4 * GM_SUN / (c**2 * R_SUN) / ARCSEC
    assert abs(d - weak) < 1e-4 and abs(d - 1.751) < 0.001
    out["sun_exact"], out["sun_weak"] = d, weak
    # strong field: compare exact deflection to 2/b (weak) for a range of b
    bs = np.array([3.0, 4.0, 6.0, 10.0, 20.0, 50.0])
    out["bs"] = bs
    out["defl_exact"] = np.array([deflection_exact(x) for x in bs])
    out["defl_weak"] = 2 / bs
    # weak field plus the known second-order term (15 pi / 16) / b^2 matches to O(1/b^3)
    second = out["defl_weak"] + 15 * np.pi / 16 / bs**2
    assert abs(out["defl_exact"][-1] / second[-1] - 1) < 2e-3
    # Fan of rays (units r_s = 1)
    bc = 1.5 * math.sqrt(3)
    assert abs(bc - 2.598) < 1e-3
    fan_b = np.concatenate([np.linspace(0.3, 2.4, 8), [bc - 0.02, bc + 0.02], np.linspace(2.9, 6.5, 8)])
    rays, captured = [], []
    for bb in fan_b:
        P, cap = null_ray(bb)
        rays.append(P)
        captured.append(cap)
    captured = np.array(captured)
    assert np.all(captured == (fan_b < bc))
    L = max(len(P) for P in rays)
    arr = np.full((len(rays), L, 2), np.nan)
    for i, P in enumerate(rays):
        arr[i, : len(P)] = P
    out.update(fan_b=fan_b, fan=arr, fan_captured=captured, bc=bc)
    return out


# ---------------------------------------------------------------------------
# Ray-traced black hole with a thin disk (units r_s = 1; G M = 1/2, c = 1).
# Rays are traced backward from a pinhole camera with x'' = -1.5 h^2 x / r^5 (h = |x x v|), which reproduces the
# Schwarzschild light-ray shapes exactly.  For every pixel we record where the ray crosses the disk plane (first and
# second time), the photon's angular momentum about the disk axis (for the Doppler factor), and, if it escapes,
# its final direction (to lens a background star field).
# ---------------------------------------------------------------------------
BH_W, BH_H = 1280, 720
BH_DIST = 50.0
BH_FOV = 36.0  # horizontal, degrees
R_IN, R_OUT = 3.0, 13.0


def trace_bh(incl_deg: float, W=BH_W, H=BH_H):
    inc = math.radians(incl_deg)
    # disk in the x-y plane; camera in the x-z plane at angle inc from the disk axis (+z), looking at the origin
    cam = BH_DIST * np.array([math.sin(inc), 0.0, math.cos(inc)])
    fwd = -cam / np.linalg.norm(cam)
    up0 = np.array([-math.cos(inc), 0.0, math.sin(inc)])  # in the x-z plane, perpendicular to fwd, "up" on screen
    right = np.cross(fwd, up0)
    fx = math.tan(math.radians(BH_FOV) / 2)
    xs = (np.arange(W) + 0.5) / W * 2 - 1
    ys = ((np.arange(H) + 0.5) / H * 2 - 1) * H / W
    X, Y = np.meshgrid(xs * fx, -ys * fx)
    d = fwd[None, None] + X[..., None] * right[None, None] + Y[..., None] * up0[None, None]
    d = d.reshape(-1, 3)
    d /= np.linalg.norm(d, axis=1, keepdims=True)
    N = d.shape[0]
    p = np.repeat(cam[None], N, 0)
    v = d.copy()
    h = np.cross(p, v)
    h2 = np.sum(h * h, axis=1)
    Lz_phys = -h[:, 2]  # the photon travels opposite to the traced ray
    alive = np.ones(N, bool)
    captured = np.zeros(N, bool)
    cross_r = np.full((2, N), np.nan)
    cross_phi = np.full((2, N), np.nan)
    n_cross = np.zeros(N, int)
    for it in range(3000):
        idx = np.nonzero(alive)[0]
        if idx.size == 0:
            break
        P, V, hh = p[idx], v[idx], h2[idx]
        r = np.linalg.norm(P, axis=1)
        dt = np.clip(0.04 * r, 0.004, 0.6)[:, None]

        def acc(Q):
            rr = np.linalg.norm(Q, axis=1, keepdims=True)
            return -1.5 * hh[:, None] * Q / rr**5

        k1x, k1v = V, acc(P)
        k2x, k2v = V + 0.5 * dt * k1v, acc(P + 0.5 * dt * k1x)
        k3x, k3v = V + 0.5 * dt * k2v, acc(P + 0.5 * dt * k2x)
        k4x, k4v = V + dt * k3v, acc(P + dt * k3x)
        Pn = P + dt / 6 * (k1x + 2 * k2x + 2 * k3x + k4x)
        Vn = V + dt / 6 * (k1v + 2 * k2v + 2 * k3v + k4v)
        # disk-plane crossings
        cr = (P[:, 2] * Pn[:, 2] < 0)
        if cr.any():
            ci = np.nonzero(cr)[0]
            f = P[ci, 2] / (P[ci, 2] - Pn[ci, 2])
            Q = P[ci] + f[:, None] * (Pn[ci] - P[ci])
            rq = np.hypot(Q[:, 0], Q[:, 1])
            gi = idx[ci]
            k = n_cross[gi]
            ok = k < 2
            cross_r[k[ok], gi[ok]] = rq[ok]
            cross_phi[k[ok], gi[ok]] = np.arctan2(Q[ok, 1], Q[ok, 0])
            n_cross[gi] += 1
        p[idx], v[idx] = Pn, Vn
        rn = np.linalg.norm(Pn, axis=1)
        cap = rn < 1.0
        esc = (rn > BH_DIST + 6) & (np.sum(Pn * Vn, axis=1) > 0)
        captured[idx[cap]] = True
        alive[idx[cap | esc | (n_cross[idx] >= 3)]] = False
    vdir = v / np.linalg.norm(v, axis=1, keepdims=True)
    return dict(cross_r=cross_r.reshape(2, H, W), cross_phi=cross_phi.reshape(2, H, W),
                captured=captured.reshape(H, W), Lz=Lz_phys.reshape(H, W), dir=vdir.reshape(H, W, 3).astype(np.float32),
                incl=incl_deg)


def doppler_g(r, Lz):
    """nu_obs / nu_emit for gas on circular Keplerian orbits (prograde about +z), units r_s = 1."""
    omega = np.sqrt(0.5 / r**3)
    ut = 1 / np.sqrt(np.clip(1 - 1.5 / r, 1e-6, None))
    return 1 / (ut * (1 - omega * Lz))


def compute_bh(incl):
    d = trace_bh(incl)
    g = np.full_like(d["cross_r"], np.nan)
    for k in range(2):
        ok = np.isfinite(d["cross_r"][k])
        g[k][ok] = doppler_g(d["cross_r"][k][ok], d["Lz"][ok])
    d["g"] = g
    # Checks: the shadow (captured rays) has the size predicted by the critical impact parameter b_c = 2.598 r_s:
    # rays aimed within angle asin(b_c / D) (approximately) of the centre are captured.
    H, W = d["captured"].shape
    row = d["captured"][H // 2]
    fx = math.tan(math.radians(BH_FOV) / 2)
    xs = ((np.arange(W) + 0.5) / W * 2 - 1) * fx
    halfw = np.max(np.abs(xs[row])) if row.any() else 0.0
    # exact relation for a camera at finite distance D: sin(angle) = b_c sqrt(1 - 1/D) / D
    pred = math.tan(math.asin(1.5 * math.sqrt(3) * math.sqrt(1 - 1 / BH_DIST) / BH_DIST))
    assert abs(halfw - pred) < 3 * (2 * fx / W), (halfw, pred)
    if incl > 45:
        # approaching side (x<0 on screen for prograde rotation seen from this side) is blueshifted
        gg = d["g"][0]
        left = np.nanmean(gg[:, : W // 2][np.isfinite(gg[:, : W // 2])])
        rightm = np.nanmean(gg[:, W // 2:][np.isfinite(gg[:, W // 2:])])
        assert abs(left - rightm) > 0.1
        d["approaching_left"] = np.array(left > rightm)
    d["shadow_half_tan"] = np.array(halfw)
    d["shadow_pred"] = np.array(pred)
    return d


# ---------------------------------------------------------------------------
# Cosmology: flat Lambda-CDM (Planck 2018: H0 = 67.4 km/s/Mpc, Omega_m = 0.315), radiation neglected
# ---------------------------------------------------------------------------
def compute_cosmo():
    H0 = 67.4 * 1000 / 3.085_677_581e22  # 1/s
    Om, OL = 0.315, 0.685
    Gyr = 3.155_76e16
    a = np.logspace(-4, math.log10(3.0), 4000)
    Ha = H0 * np.sqrt(Om / a**3 + OL)
    # t(a) = int da / (a H)
    integrand = 1 / (a * Ha)
    t = np.concatenate([[0], np.cumsum(0.5 * (integrand[1:] + integrand[:-1]) * np.diff(a))]) + a[0] / (a[0] * Ha[0]) * (2 / 3)
    t_gyr = t / Gyr
    age = np.interp(1.0, a, t_gyr)
    assert abs(age - 13.8) < 0.1
    a_acc = (Om / (2 * OL)) ** (1 / 3)
    z_acc = 1 / a_acc - 1
    t_acc = np.interp(a_acc, a, t_gyr)
    assert abs(z_acc - 0.632) < 0.01
    # second derivative sign: a''/a = -H0^2 (Om/2 a^-3 - OL)
    add = -H0**2 * (Om / 2 / a**3 - OL) * a
    return dict(a=a, t=t_gyr, add=add, age=age, a_acc=a_acc, z_acc=z_acc, t_acc=t_acc)


# ---------------------------------------------------------------------------
# GW150914 from the committed snapshot (videos/relativity/data/gw150914.json, made by fetch.py)
# ---------------------------------------------------------------------------
def compute_gw():
    from scipy.signal import butter, sosfiltfilt

    snap = json.loads(SNAPSHOT.read_text())
    fs = snap["fs"]
    t = np.array(snap["t"])
    H1 = np.array(snap["H1_white"])
    L1 = np.array(snap["L1_white"])
    sos = butter(4, [35, 350], btype="band", fs=fs, output="sos")
    Hb, Lb = sosfiltfilt(sos, H1), sosfiltfilt(sos, L1)
    # Livingston saw it ~7 ms earlier, with the opposite sign (the detectors' arms are rotated)
    shift = snap["L1_shift_s"]
    Ls = -np.interp(t - shift, t, Lb)
    win = (t > -0.25) & (t < 0.05)
    corr = np.corrcoef(Hb[win], Ls[win])[0, 1]
    assert corr > 0.5, corr
    # Morlet-wavelet time-frequency map of the whitened Hanford strain
    freqs = np.geomspace(20, 500, 90)
    tsel = (t > -0.35) & (t < 0.08)
    w0 = 6.0
    power = []
    for f in freqs:
        s = w0 / (2 * np.pi * f)
        tt = np.arange(-4 * s, 4 * s, 1 / fs)
        wav = np.exp(2j * np.pi * f * tt) * np.exp(-tt**2 / (2 * s * s)) / np.sqrt(s)
        conv = np.convolve(H1, wav[::-1].conj(), mode="same")
        power.append(np.abs(conv[tsel]) ** 2)
    power = np.array(power)
    power /= np.median(power)
    # Leading-order chirp, f(tau) = (1/pi) (5 / (256 tau))^(3/8) (G Mc / c^3)^(-5/8): detector-frame chirp mass
    Mc = snap["chirp_mass_source"] * (1 + snap["redshift"])
    tM = G * Mc * M_SUN / c**3
    tau = np.geomspace(1e-3, 0.35, 400)
    f_chirp = (1 / np.pi) * (5 / (256 * tau)) ** (3 / 8) * tM ** (-5 / 8)
    # time from 35 Hz to coalescence
    tau35 = (5 / 256) * tM ** (-5 / 3) * (np.pi * 35) ** (-8 / 3)
    assert 0.1 < tau35 < 0.25
    # Place the chirp line on the map: the coalescence time t_c is the one free parameter (the chirp mass comes
    # from LIGO's catalog); pick the t_c that maximizes the map's power summed along the line between 40 and 200 Hz.
    tf_t = t[tsel]
    band = (f_chirp > 40) & (f_chirp < 200)
    fi = np.interp(np.log(f_chirp[band]), np.log(freqs), np.arange(len(freqs)))
    best, t_c = -1.0, 0.0
    for tc in np.arange(-0.03, 0.02, 0.0005):
        ti = np.interp(tc - tau[band], tf_t, np.arange(len(tf_t)))
        score = power[np.rint(fi).astype(int), np.rint(ti).astype(int)].sum()
        if score > best:
            best, t_c = score, tc
    assert -0.02 < t_c < 0.01, t_c
    return dict(t=t, H1=Hb, L1=Ls, corr=corr, freqs=freqs, tf_t=tf_t, power=power, tau=tau, f_chirp=f_chirp,
                Mc_det=Mc, tau35=tau35, t_c=t_c)


# ---------------------------------------------------------------------------
ITEMS = {
    "consts": compute_consts,
    "aging": compute_aging,
    "rocket": compute_rocket,
    "gps": compute_gps,
    "tidal": compute_tidal,
    "ball": compute_ball,
    "transport": compute_transport,
    "sgeo": compute_sgeo,
    "mercury": compute_mercury,
    "light": compute_light,
    "bh80": lambda: compute_bh(80.0),
    "bh20": lambda: compute_bh(20.0),
    "cosmo": compute_cosmo,
    "gw": compute_gw,
}

_loaded: dict[str, dict] = {}


def path(name: str):
    return DATA_DIR / f"{name}.npz"


def load(name: str) -> dict:
    if name not in _loaded:
        p = path(name)
        if not p.exists():
            raise FileNotFoundError(f"Missing '{name}'. Run: python -m videos.relativity.compute {name}")
        with np.load(p, allow_pickle=False) as data:
            _loaded[name] = {k: data[k] for k in data.files}
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
        out = {k: np.asarray(v) for k, v in out.items()}
        tmp = DATA_DIR / f"{name}.tmp.npz"
        np.savez_compressed(tmp, **out)
        tmp.replace(path(name))
        _loaded.pop(name, None)
        print(f"  done    {name} in {time.time() - t:.0f}s", flush=True)


if __name__ == "__main__":
    main()
