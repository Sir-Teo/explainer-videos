"""Closed-form spacetime geometry for part 2 of the general-relativity video (units G = c = 1, lengths in M).

Everything here is an exact formula, shared by ``compute.py`` (which checks it against independent numerics) and
the scenes (which draw it): the tortoise coordinate, Eddington-Finkelstein and Kruskal-Szekeres coordinates, Penrose
compactification, the Einstein-Rosen bridge embedding, and the Kerr metric's horizons, ergosphere, circular orbits
and photon orbits.
"""

from __future__ import annotations

import math

import numpy as np
from scipy.special import lambertw

# ---------------------------------------------------------------------------
# Schwarzschild (M = 1, so r_s = 2)
# ---------------------------------------------------------------------------


def tortoise(r):
    """r* = r + 2 ln|r/2 - 1|: dr*/dr = 1/(1 - 2/r).  Maps (2, inf) onto (-inf, inf)."""
    r = np.asarray(r, float)
    with np.errstate(divide="ignore"):
        return r + 2 * np.log(np.abs(r / 2 - 1))


def r_of_tortoise(rs):
    """Inverse of the tortoise coordinate outside the horizon: r = 2 (1 + W(e^{r*/2 - 1}))."""
    x = np.exp(np.clip(np.asarray(rs, float) / 2 - 1, -700, 700))
    return 2 * (1 + lambertw(x).real)


def r_of_UV(UV):
    """r from the Kruskal product: (1 - r/2) e^{r/2} = U V, so r = 2 (1 + W(-U V / e)).  Valid for U V < 1."""
    y = -np.asarray(UV, float) / math.e
    return 2 * (1 + lambertw(np.maximum(y, -1 / math.e)).real)


def UV_of_r(r):
    r = np.asarray(r, float)
    return (1 - r / 2) * np.exp(r / 2)


def kruskal_exterior(t, r):
    """Region I (r > 2): U = -e^{-u/4}, V = e^{v/4} with u = t - r*, v = t + r*."""
    rs = tortoise(r)
    return -np.exp(-(t - rs) / 4), np.exp((t + rs) / 4)


def kruskal_interior(t, r):
    """Region II (r < 2, the black hole): U = +e^{-u/4} with u = t - r*, V = e^{v/4}; here t is spacelike."""
    rs = tortoise(r)
    return np.exp(-(t - rs) / 4), np.exp((t + rs) / 4)


def TX(U, V):
    return (V + U) / 2, (V - U) / 2


def penrose(U, V):
    """Compactified Kruskal coordinates: (T~, X~) = (arctan V + arctan U, arctan V - arctan U)."""
    a, b = np.arctan(U), np.arctan(V)
    return b + a, b - a


def penrose_minkowski(t, r):
    """Minkowski (t, r >= 0) -> (T, R) = (arctan v + arctan u, arctan v - arctan u), u = t - r, v = t + r."""
    a, b = np.arctan(np.asarray(t) - r), np.arctan(np.asarray(t) + r)
    return b + a, b - a


# Radial geodesic dropped from rest at r0: the cycloid r = (r0/2)(1 + cos eta), tau = sqrt(r0^3/8)(eta + sin eta).
def drop_from_rest(r0, eta):
    eta = np.asarray(eta, float)
    return r0 / 2 * (1 + np.cos(eta)), math.sqrt(r0**3 / 8) * (eta + np.sin(eta))


def drop_coordinate_time(r0, eta):
    """Schwarzschild t along the drop (MTW 31.10), valid outside the horizon."""
    k = math.sqrt(r0 / 2 - 1)
    th = np.tan(np.asarray(eta, float) / 2)
    return 2 * np.log(np.abs((k + th) / (k - th))) + 2 * k * (eta + r0 / 4 * (eta + np.sin(eta)))


# Einstein-Rosen bridge: the Kruskal slice T = const, embedded as a surface of revolution (radius r, height z).
def bridge_rmin(T):
    """Throat radius of the slice T: (1 - r/2) e^{r/2} = T^2."""
    return r_of_UV(np.asarray(T, float) ** 2)


def bridge_dzdr(r, T):
    """dz/dr of the embedding of the Kruskal slice T = const (M = 1)."""
    q = T * T * np.exp(-r / 2)
    return np.sqrt(np.clip(1 - q, 0, None) / np.clip(q + r / 2 - 1, 1e-300, None))


def bridge_profile(T, r_max=10.0, n=400):
    """(r, z) of one half of the bridge, from the throat (z = 0) out to r_max: z = int dz/dr dr, with r = r_min + s^2
    so the integrable 1/sqrt(r - r_min) at the throat becomes a smooth integrand."""
    r0 = float(bridge_rmin(T))
    s = np.linspace(0, math.sqrt(r_max - r0), n)
    r = r0 + s * s
    g = 2 * s * bridge_dzdr(r, T)
    # at s = 0 the integrand tends to 2 / sqrt(d/dr (q + r/2 - 1) / (1 - q)) evaluated at the throat
    q0 = T * T * math.exp(-r0 / 2)
    deriv = 0.5 - q0 / 2  # d/dr (T^2 e^{-r/2} + r/2 - 1) at r0
    g[0] = 2 * math.sqrt((1 - q0) / deriv) if deriv > 0 else g[1]
    z = np.concatenate([[0.0], np.cumsum(0.5 * (g[1:] + g[:-1]) * np.diff(s))])
    return r, z


# ---------------------------------------------------------------------------
# Kerr (M = 1), Boyer-Lindquist coordinates
# ---------------------------------------------------------------------------


def r_plus(a):
    return 1 + math.sqrt(1 - a * a)


def r_minus(a):
    return 1 - math.sqrt(1 - a * a)


def r_ergo(a, th):
    return 1 + np.sqrt(1 - a * a * np.cos(th) ** 2)


def kerr_metric(r, th, a):
    """(g_tt, g_tphi, g_phiphi, Sigma, Delta) in Boyer-Lindquist coordinates."""
    s2 = np.sin(th) ** 2
    S = r * r + a * a * np.cos(th) ** 2
    D = r * r - 2 * r + a * a
    gtt = -(1 - 2 * r / S)
    gtp = -2 * a * r * s2 / S
    gpp = (r * r + a * a + 2 * a * a * r * s2 / S) * s2
    return gtt, gtp, gpp, S, D


def omega_band(r, a, th=math.pi / 2):
    """The allowed angular velocities d phi/dt of a worldline at fixed (r, theta): it is timelike iff
    g_tt + 2 Omega g_tphi + Omega^2 g_phiphi < 0.  Returns (Omega_min, Omega_max, omega_ZAMO)."""
    gtt, gtp, gpp, _, _ = kerr_metric(r, th, a)
    disc = np.sqrt(np.clip(gtp * gtp - gtt * gpp, 0, None))
    return (-gtp - disc) / gpp, (-gtp + disc) / gpp, -gtp / gpp


def omega_horizon(a):
    rp = r_plus(a)
    return a / (rp * rp + a * a)


def surface_gravity(a):
    rp = r_plus(a)
    return (rp - 1) / (rp * rp + a * a)


def horizon_area(a):
    rp = r_plus(a)
    return 4 * math.pi * (rp * rp + a * a)


def isco(a, prograde=True):
    """Bardeen, Press & Teukolsky (1972)."""
    z1 = 1 + (1 - a * a) ** (1 / 3) * ((1 + a) ** (1 / 3) + (1 - a) ** (1 / 3))
    z2 = math.sqrt(3 * a * a + z1 * z1)
    s = -1 if prograde else 1
    return 3 + z2 + s * math.sqrt((3 - z1) * (3 + z1 + 2 * z2))


def circular_E(r, a, prograde=True):
    """Specific energy of a circular equatorial geodesic orbit."""
    s = 1 if prograde else -1
    r = np.asarray(r, float)
    return (r**1.5 - 2 * r**0.5 + s * a) / (r**0.75 * np.sqrt(r**1.5 - 3 * r**0.5 + 2 * s * a))


def circular_L(r, a, prograde=True):
    s = 1 if prograde else -1
    r = np.asarray(r, float)
    return s * (r * r - 2 * s * a * r**0.5 + a * a) / (r**0.75 * np.sqrt(r**1.5 - 3 * r**0.5 + 2 * s * a))


def kepler_omega(r, a, prograde=True):
    s = 1 if prograde else -1
    return s / (np.asarray(r, float) ** 1.5 + s * a)


def photon_orbit(a, prograde=True):
    """Radius of the circular equatorial photon orbit: 2 (1 + cos(2/3 arccos(-+a)))."""
    return 2 * (1 + math.cos(2 / 3 * math.acos(-a if prograde else a)))


def bardeen_xi_eta(r, a):
    """Constants of motion (xi = L/E, eta = Q/E^2) of the spherical photon orbit at radius r (Bardeen 1973)."""
    r = np.asarray(r, float)
    xi = (r * r * (3 - r) - a * a * (r + 1)) / (a * (r - 1))
    eta = r**3 * (4 * a * a - r * (r - 3) ** 2) / (a * a * (r - 1) ** 2)
    return xi, eta


def shadow_curve(a, incl, n=800):
    """The shadow's edge on the sky of a distant observer at inclination incl (radians from the spin axis):
    (alpha, beta) = (-xi / sin i, +-sqrt(eta + a^2 cos^2 i - xi^2 cot^2 i)), traced around as one closed curve.
    (As a -> 0 the parametrization cancels catastrophically; below a = 1e-3 the exact limit, a circle of radius
    sqrt(27), is returned.)"""
    if a < 1e-3:
        u = np.linspace(0, 2 * np.pi, n)
        return math.sqrt(27) * np.cos(u), math.sqrt(27) * np.sin(u)
    r1, r2 = photon_orbit(a, True), photon_orbit(a, False)
    r = np.linspace(r1, r2, 20000)
    xi, eta = bardeen_xi_eta(r, a)
    b2 = eta + a * a * math.cos(incl) ** 2 - xi**2 / math.tan(incl) ** 2
    ok = b2 >= 0
    al, be = -xi[ok] / math.sin(incl), np.sqrt(b2[ok])
    # resample by arclength so the curve is evenly spaced
    al = np.concatenate([al, al[::-1]])
    be = np.concatenate([be, -be[::-1]])
    seg = np.hypot(np.diff(al), np.diff(be))
    s = np.concatenate([[0], np.cumsum(seg)])
    u = np.linspace(0, s[-1], n)
    return np.interp(u, s, al), np.interp(u, s, be)


def kerr_schild_xy(r, phi_k, a):
    """Equatorial Kerr-Schild Cartesian position from (r, ingoing-Kerr phi)."""
    return r * np.cos(phi_k) - a * np.sin(phi_k), r * np.sin(phi_k) + a * np.cos(phi_k)


def kerr_schild_xyz(r, th, phi_k, a):
    s = np.sin(th)
    return np.stack([(r * np.cos(phi_k) - a * np.sin(phi_k)) * s, (r * np.sin(phi_k) + a * np.cos(phi_k)) * s,
                     r * np.cos(th)], -1)


def page_thorne_kerr(r, a):
    """Novikov-Thorne / Page-Thorne flux of a thin Kerr disk, up to a constant (Page & Thorne 1974), zero at the ISCO."""
    x = np.sqrt(np.asarray(r, float))
    x0 = math.sqrt(isco(a))
    ac = math.acos(a)
    x1 = 2 * math.cos((ac - math.pi) / 3)
    x2 = 2 * math.cos((ac + math.pi) / 3)
    x3 = -2 * math.cos(ac / 3)
    with np.errstate(invalid="ignore", divide="ignore"):
        bracket = (x - x0 - 1.5 * a * np.log(x / x0)
                   - 3 * (x1 - a) ** 2 / (x1 * (x1 - x2) * (x1 - x3)) * np.log((x - x1) / (x0 - x1))
                   - 3 * (x2 - a) ** 2 / (x2 * (x2 - x1) * (x2 - x3)) * np.log((x - x2) / (x0 - x2))
                   - 3 * (x3 - a) ** 2 / (x3 * (x3 - x1) * (x3 - x2)) * np.log((x - x3) / (x0 - x3)))
        F = bracket / (x**4 * (x**3 - 3 * x + 2 * a))
    return np.nan_to_num(np.where(x > x0, F, 0.0))
