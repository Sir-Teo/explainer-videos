"""Precompute everything numerical in part 2 of the general-relativity video.

    python -m videos.relativity2.compute               # everything missing (~6 min on 4 cores)
    python -m videos.relativity2.compute kerr80 qnm    # specific items
    python -m videos.relativity2.compute --force       # recompute

Results are cached in ``.cache/relativity2/<name>.npz``; scenes call ``load(name)``.  Units are G = c = M = 1
unless an item says otherwise.  As in part 1, nothing is a cartoon: worldlines are integrated geodesics, the
black-hole images are ray traces of Kerr null geodesics checked pixel by pixel against Bardeen's analytic shadow,
the ringdown is a numerical solution of the Regge-Wheeler equation checked against Leaver's quasinormal frequency,
and every number the narration quotes is computed here and asserted against the formula or measurement it
illustrates.

Items:
    consts       headline numbers: infall times and tides, Gravity Probe B, Hawking temperature and entropy, ...
    infall       an astronaut dropped from rest at r = 10M: proper time, Schwarzschild t, EF and Kruskal coordinates,
                 the signals a station receives and their redshift
    bridge       Kruskal slices T = const embedded as surfaces of revolution: the Einstein-Rosen bridge pinching off
    collapse     the surface of a collapsing star (static until t = 0, then free fall) in Kruskal coordinates
    raych        null congruences and trapped spheres; Raychaudhuri focusing; light rays focused by a mass
    gpb          geodetic precession by parallel transport (spacetime, and on Flamm's paraboloid); Gravity Probe B
    kerr_orbits  ISCO and efficiency vs spin, the allowed angular velocities, zero-angular-momentum infall, the
                 Penrose process
    kerr80/20    ray traces of a thin disk around a Kerr hole (a = 0.99) at inclinations 80 and 20 degrees
    kerr80_0/20_0  the same for a non-spinning hole (a = 1e-4), traced and shaded identically
    shadows      Bardeen's shadow outline for a sequence of spins
    qnm          quasinormal modes: Leaver's continued fraction, Kerr modes, a time-domain ringdown, GW150914's
    inspiral     the leading-order inspiral and chirp; the Hulse-Taylor pulsar
    quad         the quadrupole formula's angular integral; a spinning steel beam
    hawking      an exponentially redshifted wave and its spectrum; peeling light rays; the Euclidean cigar
    cosmo2       flat Lambda-CDM with radiation: horizons, light cones, densities, a family of Friedmann universes
"""

from __future__ import annotations

import argparse
import json
import math
import time
from pathlib import Path

import numpy as np
from scipy.integrate import quad, solve_ivp
from scipy.optimize import brentq, minimize_scalar

from explainer.tts import REPO_ROOT

from . import spacetime as st

DATA_DIR = REPO_ROOT / ".cache" / "relativity2"
GW_SNAPSHOT = REPO_ROOT / "videos" / "relativity" / "data" / "gw150914.json"

# ---------------------------------------------------------------------------
# Constants (CODATA 2018, IAU 2015 nominal values), as in part 1
# ---------------------------------------------------------------------------
c = 299_792_458.0
G = 6.674_30e-11
hbar = 1.054_571_817e-34
kB = 1.380_649e-23
GM_SUN = 1.327_124_400_18e20
M_SUN = GM_SUN / G
GM_EARTH = 3.986_004_418e14
R_EARTH = 6.371e6
YEAR = 3.155_76e7  # Julian year
MAS = math.pi / (180 * 3600 * 1000)
T_SUN = GM_SUN / c**3  # 4.925 microseconds: the Sun's mass as a time
L_SUN = GM_SUN / c**2  # 1.477 km: the Sun's mass as a length
M_SGRA = 4.3e6  # GRAVITY Collaboration (2019-2022): 4.3 million solar masses
M_M87 = 6.5e9  # EHT (2019)
T_CMB = 2.7255
M_MOON = 7.342e22


def rng(seed: int) -> np.random.Generator:
    return np.random.Generator(np.random.PCG64(seed))


# ---------------------------------------------------------------------------
def compute_consts():
    out = {}
    assert abs(L_SUN - 1476.6) < 0.1 and abs(T_SUN * 1e6 - 4.9255) < 1e-3
    # Longest possible proper time from horizon to singularity: pi M
    for name, m in (("10", 10.0), ("sgra", M_SGRA), ("m87", M_M87)):
        out["taumax_" + name] = math.pi * m * T_SUN
        rs = 2 * m * L_SUN
        out["tide_" + name] = 2 * GM_SUN * m * 2.0 / rs**3  # radial stretch across 2 m at the horizon, m/s^2
        out["efold_" + name] = 4 * m * T_SUN
    assert abs(out["taumax_10"] * 1e6 - 154.7) < 0.1
    assert abs(out["taumax_sgra"] - 66.5) < 0.1
    assert abs(out["taumax_m87"] / 3600 - 27.9) < 0.05
    assert abs(out["tide_10"] / 9.81 / 1e7 - 2.1) < 0.05
    assert abs(out["tide_sgra"] - 1.11e-3) < 0.01e-3
    assert abs(out["efold_10"] * 1e6 - 197.0) < 0.1
    # Gravity Probe B (642 km polar orbit, semimajor axis 7027.4 km) and its guide star IM Pegasi (declination 16.84
    # degrees): the drift of a gyroscope pointed at the star
    r = 7.0274e6
    geo = 1.5 * GM_EARTH**1.5 / (c**2 * r**2.5) * YEAR / MAS
    I_earth, w_earth = 8.034e37, 7.292_115e-5
    J = I_earth * w_earth
    fd = G * J / (2 * c**2 * r**3) * math.cos(math.radians(16.84)) * YEAR / MAS
    assert abs(geo - 6606) < 6 and abs(fd - 39.2) < 0.3, (geo, fd)
    out.update(gpb_geo=geo, gpb_fd=fd, gpb_r=r)
    # Hawking temperature, entropy, lifetime (naive blackbody estimate), and the mass as cold as the CMB
    TH = hbar * c**3 / (8 * math.pi * G * M_SUN * kB)
    S = 4 * math.pi * G * M_SUN**2 / (hbar * c)
    life = 5120 * math.pi * G**2 * M_SUN**3 / (hbar * c**4) / YEAR
    m_cmb = hbar * c**3 / (8 * math.pi * G * kB * T_CMB)
    assert abs(TH * 1e8 - 6.17) < 0.01 and abs(S / 1e77 - 1.049) < 0.005
    assert abs(life / 1e67 - 2.10) < 0.02 and abs(m_cmb / 1e22 - 4.50) < 0.01
    assert abs(m_cmb / M_MOON - 0.61) < 0.01
    out.update(T_hawking=TH, S_sun=S, life_sun=life, m_cmb=m_cmb)
    # critical density for H0 = 67.4 km/s/Mpc
    H0 = 67.4e3 / 3.085_677_581e22
    rho_c = 3 * H0**2 / (8 * math.pi * G)
    assert abs(rho_c / 1e-26 - 0.853) < 0.002 and abs(rho_c / 1.672_62e-27 - 5.1) < 0.05
    out["rho_crit"] = rho_c
    # the luminosity scale c^5/G, and a 490-tonne, 20 m steel beam spun at 28 rad/s: L = (2/45) G M^2 l^4 w^6 / c^5
    out["c5G"] = c**5 / G
    beam = 2 / 45 * G * 4.9e5**2 * 20.0**4 * 28.0**6 / c**5
    assert abs(out["c5G"] / 1e52 - 3.63) < 0.01 and abs(beam / 1e-29 - 2.26) < 0.02
    out["beam"] = beam
    return out


# ---------------------------------------------------------------------------
# Infall from rest at r0 = 10M (an astronaut stepping off a space station)
# ---------------------------------------------------------------------------
R0_INFALL = 10.0


def compute_infall():
    r0 = R0_INFALL
    E = math.sqrt(1 - 2 / r0)
    eta = np.linspace(0, math.pi, 6001)[:-1]
    r, tau = st.drop_from_rest(r0, eta)
    i_h = np.searchsorted(-r, -2.0)  # first index inside the horizon
    tau_h = float(np.interp(2.0, r[::-1], tau[::-1]))
    tau_s = math.pi * math.sqrt(r0**3 / 8)
    # proper time from horizon to singularity: (r0^3/8)^(1/2) (pi - eta_h - sin eta_h), eta_h where r = 2
    eta_h = math.acos(2 * 2 / r0 - 1)
    assert abs(tau_s - tau_h - math.sqrt(r0**3 / 8) * (math.pi - eta_h - math.sin(eta_h))) < 1e-3
    # Schwarzschild coordinate time: closed form vs integrating dt/dtau = E / (1 - 2/r)
    out_ = r > 2.0
    t_closed = st.drop_coordinate_time(r0, eta[out_])

    # dt/d eta = (E / (1 - 2/r)) d tau/d eta, with d tau/d eta = sqrt(r0^3/8)(1 + cos eta): regular at the start
    eo = eta[out_]

    def rhs(e_, y):
        rr = r0 / 2 * (1 + math.cos(e_))
        return [E / (1 - 2 / rr) * math.sqrt(r0**3 / 8) * (1 + math.cos(e_))]

    sol = solve_ivp(rhs, [0, eo[-1]], [0.0], t_eval=eo, rtol=1e-12, atol=1e-12)
    t_num = sol.y[0]
    far = r[out_] > 2.05  # (t diverges logarithmically at the horizon)
    assert np.max(np.abs(t_num - t_closed)[far]) < 1e-6, np.max(np.abs(t_num - t_closed)[far])
    # ingoing EF time v: dv/dtau = 1 / (E + sqrt(E^2 - 1 + 2/r)) is regular at the horizon
    dv = 1 / (E + np.sqrt(np.maximum(2 / r - 2 / r0, 0)))
    v = st.tortoise(r0) + np.concatenate([[0], np.cumsum(0.5 * (dv[1:] + dv[:-1]) * np.diff(tau))])
    ttilde = v - r
    # consistency outside: v = t + r*
    k = np.nonzero(out_)[0][-50]
    assert abs(v[k] - (t_closed[k] + st.tortoise(r[k]))) < 2e-3
    # Kruskal: V = e^{v/4}, U = (1 - r/2) e^{r/2} / V
    V = np.exp(v / 4)
    U = st.UV_of_r(r) / V
    # Signals sent outward every 0.4 M of proper time, received at the station (static at r0)
    f0 = math.sqrt(1 - 2 / r0)
    emit_tau = np.arange(0.4, tau_h, 0.4)
    emit_r = np.interp(emit_tau, tau, r)
    emit_t = np.interp(emit_tau, tau[out_], t_closed)
    u_e = emit_t - st.tortoise(emit_r)
    recv_t = u_e + st.tortoise(r0)
    # redshift 1 + z = d tau_station / d tau = f0 du/dtau, du/dtau = (E + sqrt(E^2 - f))/f, on a grid in r that
    # reaches very close to the horizon
    rr = np.concatenate([np.linspace(r0 - 1e-6, 2.5, 400), 2 * (1 + np.geomspace(0.25, 1e-10, 600))])
    ee = np.arccos(2 * rr / r0 - 1)
    tt_ = st.drop_coordinate_time(r0, ee)
    one_z = f0 * (E + np.sqrt(np.maximum(2 / rr - 2 / r0, 0))) / (1 - 2 / rr)
    recv_tt = tt_ - st.tortoise(rr) + st.tortoise(r0)
    # late times: ln(1+z) grows with slope 1/4M in the station's coordinate time (e-folding time 4M)
    late = rr < 2 * (1 + 1e-5)
    slope = np.polyfit(recv_tt[late], np.log(one_z[late]), 1)[0]
    assert abs(slope - 0.25) < 0.002, slope
    return dict(eta=eta, r=r, tau=tau, tau_h=tau_h, tau_s=tau_s, E=E, i_h=i_h, t=t_closed, t_tau=tau[out_],
                v=v, ttilde=ttilde, U=U, V=V, emit_tau=emit_tau, emit_r=emit_r, emit_t=emit_t, recv_t=recv_t,
                z_t=recv_tt, one_z=one_z, slope=slope, r0=r0)


# ---------------------------------------------------------------------------
# The Einstein-Rosen bridge: Kruskal slices T = const
# ---------------------------------------------------------------------------
def compute_bridge():
    Ts = np.linspace(0, 0.995, 120)
    profiles_r, profiles_z, rmins = [], [], []
    for T in Ts:
        r, z = st.bridge_profile(T, r_max=10.0, n=400)
        profiles_r.append(r)
        profiles_z.append(z)
        rmins.append(r[0])
    profiles_r, profiles_z, rmins = np.array(profiles_r), np.array(profiles_z), np.array(rmins)
    # T = 0 is Flamm's paraboloid z = 2 sqrt(r_s (r - r_s)) = 2 sqrt(2 (r - 2))
    flamm = 2 * np.sqrt(2 * (profiles_r[0] - 2))
    assert np.max(np.abs(profiles_z[0] - flamm)) < 2e-3, np.max(np.abs(profiles_z[0] - flamm))
    assert abs(rmins[0] - 2) < 1e-9 and np.all(np.diff(rmins) < 0) and rmins[-1] < 0.3
    # the throat: (1 - r/2) e^{r/2} = T^2
    assert np.allclose((1 - rmins / 2) * np.exp(rmins / 2), Ts**2, atol=1e-9)
    return dict(T=Ts, r=profiles_r, z=profiles_z, rmin=rmins)


# ---------------------------------------------------------------------------
# A collapsing star: static at R0 until t = 0, then its surface falls freely (Oppenheimer-Snyder outside)
# ---------------------------------------------------------------------------
def compute_collapse():
    R0 = 5.0
    eta = np.linspace(0, math.pi * 0.999, 3000)
    r, tau = st.drop_from_rest(R0, eta)
    E = math.sqrt(1 - 2 / R0)
    dv = 1 / (E + np.sqrt(np.maximum(2 / r - 2 / R0, 0)))
    v = st.tortoise(R0) + np.concatenate([[0], np.cumsum(0.5 * (dv[1:] + dv[:-1]) * np.diff(tau))])
    V = np.exp(v / 4)
    U = st.UV_of_r(r) / V
    # static part, t from -60 to 0
    ts = np.linspace(-60, 0, 400)
    Us, Vs = st.kruskal_exterior(ts, np.full_like(ts, R0))
    U_all, V_all = np.concatenate([Us, U[1:]]), np.concatenate([Vs, V[1:]])
    # the surface crosses the horizon U = 0 at V_h; the singularity U V = 1 at the end
    k = np.argmin(np.abs(U))
    assert abs(st.r_of_UV(U[k] * V[k]) - 2) < 0.01
    assert abs(U[-1] * V[-1] - 1) < 0.01
    return dict(U=U_all, V=V_all, V_h=V[k], R0=R0, n_static=len(ts))


# ---------------------------------------------------------------------------
# Raychaudhuri: congruences and focusing
# ---------------------------------------------------------------------------
def outgoing_r(ttilde, r0, t0=0.0):
    """r(t~) of the outgoing radial light ray through (t0, r0) in ingoing EF coordinates (M = 1):
    t~ - t0 = (r - r0) + 4 ln|(r - 2)/(r0 - 2)|."""
    def g(r):
        return (r - r0) + 4 * math.log(abs((r - 2) / (r0 - 2))) - (ttilde - t0)

    if r0 > 2:
        return brentq(g, 2 + 1e-12, 1e4)
    return brentq(g, 1e-9, 2 - 1e-12) if g(1e-9) > 0 else 0.0


def compute_raych():
    out = {}
    # Spheres emitting a flash at t~ = 0: outside the horizon (r0 = 3) and inside (r0 = 1.5).  The area of each
    # light front is 4 pi r^2; theta = d ln A / d lambda has the sign of dr along the ray.
    tt = np.linspace(0, 3.0, 200)
    for name, r0 in (("out3", 3.0), ("in15", 1.5)):
        ro = np.array([outgoing_r(x, r0) for x in tt])
        ri = np.maximum(r0 - tt, 0.0)
        out[name + "_out"], out[name + "_in"] = ro, ri
    out["tt"] = tt
    assert np.all(np.diff(out["out3_out"]) > 0)  # outside: the outgoing front grows
    assert np.all(np.diff(out["in15_out"][out["in15_out"] > 0]) < 0)  # inside: both fronts shrink (trapped)
    # Raychaudhuri for a radial null congruence in vacuum: theta = 2/r dr/dlambda, and d theta / d lambda = -theta^2/2
    lam = np.linspace(0, 5, 20001)
    rr = 3 + lam  # dr/dlambda = E = 1
    th = 2 / rr
    dth = np.gradient(th, lam, edge_order=2)
    assert np.max(np.abs(dth + th**2 / 2)) < 1e-6
    # Focusing: d theta/d tau = -theta^2/3 - sigma^2 - R_uu, theta(0) = -1: blows up before tau = 3
    taus = np.linspace(0, 3.2, 600)
    curves = []
    for sig2, ric in ((0, 0), (0.3, 0), (0, 0.5)):
        def f(_, y, sig2=sig2, ric=ric):
            return [-y[0] ** 2 / 3 - sig2 - ric]

        ev = lambda _, y: y[0] + 60  # noqa: E731
        ev.terminal = True
        s = solve_ivp(f, [0, 3.2], [-1.0], t_eval=taus, events=ev, rtol=1e-10, atol=1e-12)
        y = np.full_like(taus, np.nan)
        y[: len(s.y[0])] = s.y[0]
        curves.append(y)
        assert s.t_events[0].size and s.t_events[0][0] < 3.0
    out["focus_tau"], out["focus_theta"] = taus, np.array(curves)
    # pure focusing (sigma = R = 0): theta = theta0 / (1 + theta0 tau / 3), caustic at tau = 3
    pure = -1 / (1 - taus / 3)
    ok = taus < 2.9
    assert np.max(np.abs(curves[0][ok] - pure[ok])) < 1e-6
    # A parallel beam of light focused by a mass (part 1's exact Schwarzschild rays; units r_s = 1)
    from videos.relativity.compute import null_ray

    bs = np.linspace(3.0, 9.0, 13)
    rays = []
    for b in bs:
        P, cap = null_ray(b, x0=-12.0, max_len=80.0)
        assert not cap
        rays.append(P)
    L = max(len(P) for P in rays)
    arr = np.full((len(rays), L, 2), np.nan)
    for i, P in enumerate(rays):
        arr[i, : len(P)] = P
    out["beam_b"], out["beam"] = bs, arr
    return out


# ---------------------------------------------------------------------------
# Gyroscopes: geodetic precession
# ---------------------------------------------------------------------------
def spin_transport_circular(r, n=4000):
    """Parallel-transport a spin vector around one circular geodesic orbit (equatorial Schwarzschild, M = 1) and
    return its angle, in the comoving frame, relative to the radial direction."""
    f = 1 - 2 / r
    ut = 1 / math.sqrt(1 - 3 / r)
    up = math.sqrt(1 / r**3) * ut
    Gt_tr, Gr_tt, Gr_pp, Gp_rp = 1 / (r * r * f), f / (r * r), -(r - 2), 1 / r

    def rhs(_, S):
        St, Sr, Sp = S
        return [-Gt_tr * ut * Sr, -Gr_tt * ut * St - Gr_pp * up * Sp, -Gp_rp * up * Sr]

    T = 2 * math.pi / up
    taus = np.linspace(0, T, n)
    sol = solve_ivp(rhs, [0, T], [0.0, math.sqrt(f), 0.0], t_eval=taus, rtol=1e-12, atol=1e-14)
    St, Sr, Sp = sol.y
    # comoving frame: e1 = sqrt(f) d_r, e2 in the t-phi plane orthogonal to u
    B = 1 / math.sqrt(-f * (r * r * up / (f * ut)) ** 2 + r * r)
    A = r * r * up * B / (f * ut)
    S1 = Sr / math.sqrt(f)
    S2 = -f * St * A + r * r * Sp * B
    ang = np.unwrap(np.arctan2(S2, S1))
    return taus, ang, up


def flamm_transport(r, n=3000):
    """Parallel transport around the circle at r on Flamm's paraboloid z = 2 sqrt(2 (r - 2)), done in 3D: dV/ds is
    the part of V's change normal to the surface removed.  Returns the turn angle after one loop and the path."""
    zr = 2 * math.sqrt(2 * (r - 2))
    dzdr = math.sqrt(2 / (r - 2))
    phis = np.linspace(0, 2 * math.pi, n)
    P = np.stack([r * np.cos(phis), r * np.sin(phis), np.full_like(phis, zr)], 1)
    # unit normal of the surface of revolution z(rho): N ~ (-z' cos, -z' sin, 1)
    N = np.stack([-dzdr * np.cos(phis), -dzdr * np.sin(phis), np.ones_like(phis)], 1)
    N /= np.linalg.norm(N, axis=1, keepdims=True)
    # start along the meridian (outward, uphill)
    m0 = np.array([1.0, 0.0, dzdr]) / math.sqrt(1 + dzdr**2)

    def rhs(phi, V):
        c_, s_ = math.cos(phi), math.sin(phi)
        Nn = np.array([-dzdr * c_, -dzdr * s_, 1.0]) / math.sqrt(1 + dzdr**2)
        dN = np.array([dzdr * s_, -dzdr * c_, 0.0]) / math.sqrt(1 + dzdr**2)
        return -(V @ dN) * Nn

    sol = solve_ivp(rhs, [0, 2 * math.pi], m0, t_eval=phis, rtol=1e-12, atol=1e-14)
    Vs = sol.y.T
    end = Vs[-1]
    ang = math.atan2(np.dot(np.cross(m0, end), N[0]), np.dot(m0, end))
    return ang, P, Vs


def compute_gpb():
    out = {}
    for r in (10.0, 20.0, 50.0):
        taus, ang, up = spin_transport_circular(r)
        # in the comoving frame the spin turns by -(2 pi - Delta) relative to the radial direction per orbit
        delta = ang[-1] - ang[0] + 2 * math.pi
        exact = 2 * math.pi * (1 - math.sqrt(1 - 3 / r))
        assert abs(delta - exact) < 1e-7, (r, delta, exact)
        out[f"geo_{int(r)}"] = delta
    taus, ang, up = spin_transport_circular(10.0, n=600)
    out["spin_tau"], out["spin_ang"] = taus, ang
    # the space part, from parallel transport on Flamm's paraboloid: the tangent cone's missing wedge
    for r in (10.0, 50.0):
        turn, P, Vs = flamm_transport(r)
        wedge = 2 * math.pi * (1 - math.sqrt(1 - 2 / r))
        assert abs(abs(turn) - wedge) < 1e-6, (turn, wedge)
        out[f"flamm_{int(r)}"] = abs(turn)
    turn, P, Vs = flamm_transport(10.0, n=361)
    out["flamm_path"], out["flamm_vecs"] = P, Vs
    # weak field: space part / total -> 2/3
    r = 1e6
    ratio = (1 - math.sqrt(1 - 2 / r)) / (1 - math.sqrt(1 - 3 / r))
    assert abs(ratio - 2 / 3) < 1e-6
    return out


# ---------------------------------------------------------------------------
# Kerr: circular orbits, the ergosphere, zero-angular-momentum infall, the Penrose process
# ---------------------------------------------------------------------------
def equatorial_geodesic(E, L, mu, a, r0, vr0, lam_end, n=3000, r_stop=None, phi0=0.0):
    """Integrate an equatorial Kerr geodesic in Mino time: r'' = R'/2, phi_K' (ingoing-Kerr phi, regular at the
    horizon), tau' = r^2.  Returns arrays (r, phi_K, tau)."""

    def R(r):
        P = E * (r * r + a * a) - a * L
        return P * P - (r * r - 2 * r + a * a) * (mu * mu * r * r + (L - a * E) ** 2)

    def dR(r):
        P = E * (r * r + a * a) - a * L
        return 4 * E * r * P - (2 * r - 2) * (mu * mu * r * r + (L - a * E) ** 2) - (r * r - 2 * r + a * a) * 2 * mu * mu * r

    def rhs(_, y):
        r, vr, ph, tau = y
        P = E * (r * r + a * a) - a * L
        D = r * r - 2 * r + a * a
        K = mu * mu * r * r + (L - a * E) ** 2
        if vr < 0 or abs(D) < 1e-9:
            dph = -(a * E - L) + a * K / (P - vr)
        else:
            dph = -(a * E - L) + a * (P + vr) / D
        return [vr, dR(r) / 2, dph, r * r]

    events = []
    if r_stop is not None:
        ev = lambda _, y: y[0] - r_stop  # noqa: E731
        ev.terminal = True
        events.append(ev)
    lam = np.linspace(0, lam_end, n)
    sol = solve_ivp(rhs, [0, lam_end], [r0, vr0, phi0, 0.0], t_eval=lam, events=events, rtol=1e-10, atol=1e-12,
                    max_step=abs(lam_end) / 200)
    return sol.y[0], sol.y[2], sol.y[3], R


def compute_kerr_orbits():
    out = {}
    spins = np.linspace(0, 0.9999, 400)
    ip = np.array([st.isco(a, True) for a in spins])
    ir = np.array([st.isco(a, False) for a in spins])
    eff_p = 1 - np.array([st.circular_E(r, a, True) for r, a in zip(ip, spins)])
    eff_r = 1 - np.array([st.circular_E(r, a, False) for r, a in zip(ir, spins)])
    # ISCO = the minimum of E(r) along the circular orbits: check the formula by direct minimization
    for a in (0.0, 0.5, 0.9, 0.99):
        res = minimize_scalar(lambda r: st.circular_E(r, a, True), bounds=(st.photon_orbit(a) + 0.05, 12),
                              method="bounded", options={"xatol": 1e-10})
        assert abs(res.x - st.isco(a)) < 1e-4, (a, res.x, st.isco(a))
    assert abs(ip[0] - 6) < 1e-12 and abs(ir[0] - 6) < 1e-12 and abs(eff_p[0] - (1 - math.sqrt(8 / 9))) < 1e-12
    e1 = 1 - st.circular_E(st.isco(1 - 1e-12), 1 - 1e-12)
    assert abs(e1 - (1 - 1 / math.sqrt(3))) < 1e-3
    assert abs(st.isco(0.998) - 1.237) < 0.001 and abs(1 - st.circular_E(st.isco(0.998), 0.998) - 0.321) < 0.001
    out.update(spins=spins, isco_pro=ip, isco_retro=ir, eff_pro=eff_p, eff_retro=eff_r, eff_998=1 - st.circular_E(
        st.isco(0.998), 0.998))
    out["photon_pro"] = np.array([st.photon_orbit(a, True) for a in spins])
    out["photon_retro"] = np.array([st.photon_orbit(a, False) for a in spins])
    assert abs(out["photon_pro"][0] - 3) < 1e-12
    # allowed angular velocities on the equator for a = 0.9
    a = 0.9
    rr = np.linspace(st.r_plus(a) + 1e-4, 4.0, 600)
    om_min, om_max, om_z = st.omega_band(rr, a)
    assert om_min[np.argmin(np.abs(rr - 2.0))] < 1e-3 and abs(om_min[np.argmin(np.abs(rr - 2.0))]) < 2e-3
    assert np.all(om_min[rr < 1.99] > 0)  # inside the ergosphere nothing can stand still
    assert abs(om_max[0] - st.omega_horizon(a)) < 0.02 and abs(om_min[0] - st.omega_horizon(a)) < 0.02
    out.update(band_a=a, band_r=rr, band_min=om_min, band_max=om_max, band_zamo=om_z)
    # Zero-angular-momentum infall from rest at infinity (E = 1, L = 0), a = 0.99, as a distant observer describes it
    # (Boyer-Lindquist t and phi): dphi/dt = omega(r), which tends to the horizon's Omega_H, while
    # dr/dt = -Delta sqrt(2 r (r^2 + a^2)) / A -> 0.  The particle circles the hole forever in t.
    a = 0.99
    rp = st.r_plus(a)

    def zamo_rhs(_, y):
        r = y[0]
        D = r * r - 2 * r + a * a
        A = (r * r + a * a) ** 2 - a * a * D
        return [-D * math.sqrt(2 * r * (r * r + a * a)) / A, 2 * a * r / A]

    ev = lambda _, y: y[0] - (rp + 1e-7)  # noqa: E731
    ev.terminal = True
    ts = np.linspace(0, 400, 8001)
    sol = solve_ivp(zamo_rhs, [0, 400], [12.0, 0.0], t_eval=ts, events=ev, rtol=1e-10, atol=1e-12)
    zr, zphi = sol.y
    assert abs(np.gradient(zphi, ts[: len(zphi)])[-1] - st.omega_horizon(a)) < 1e-3
    out.update(zamo_a=a, zamo_t=ts[: len(zr)], zamo_r=zr, zamo_phi=zphi)
    # split at r = 1.4M: inside the ergosphere, but clear of the marginally bound orbit r_mb = 2 - a + 2 sqrt(1 - a) =
    # 1.21M, near which the incoming particle would whirl around many times
    out.update(penrose_process(0.99, 1.4))
    return out


def penrose_process(a, r_s, m12=0.05):
    """Particle 0 (mass 1, E = 1) falls from infinity to a turning point at r_s inside the ergosphere and splits
    into two fragments of mass m12, thrown back to back along phi in its rest frame at the largest speed the masses
    allow; the retrograde one has negative energy and falls in, the other escapes with more energy than came in."""
    gtt, gtp, gpp, S, D = st.kerr_metric(r_s, math.pi / 2, a)
    E0, mu0 = 1.0, 1.0

    def R(r, E, L, mu):
        P = E * (r * r + a * a) - a * L
        return P * P - (r * r - 2 * r + a * a) * (mu * mu * r * r + (L - a * E) ** 2)

    # L0: turning point at r_s; quadratic in L
    Ls = np.linspace(0, 6, 60001)
    vals = R(r_s, E0, Ls, mu0)
    idx = np.nonzero(np.diff(np.sign(vals)))[0]
    roots = [brentq(lambda L: R(r_s, E0, L, mu0), Ls[i], Ls[i + 1]) for i in idx]
    L0 = None
    for Lr in roots:
        rr = np.linspace(r_s * 1.0001, 50, 4000)
        if np.all(R(rr, E0, Lr, mu0) > 0):
            L0 = Lr
            break
    assert L0 is not None
    # ZAMO frame at r_s: E = alpha eps + omega L, L = sqrt(g_pp) pi
    A = (r_s**2 + a * a) ** 2 - a * a * D
    alpha, omega, sg = math.sqrt(S * D / A), 2 * a * r_s / A, math.sqrt(gpp)
    pi0 = L0 / sg
    eps0 = (E0 - omega * L0) / alpha
    assert abs(eps0**2 - pi0**2 - 1) < 1e-6
    beta0, gam0 = pi0 / eps0, eps0
    # fragments in particle 0's rest frame: energy 1/2 each, momentum +-p along phi
    e_ = 0.5
    p_ = math.sqrt(e_ * e_ - m12 * m12)
    frags = []
    for s in (-1, 1):
        eps = gam0 * (e_ + beta0 * s * p_)
        pi = gam0 * (s * p_ + beta0 * e_)
        L = sg * pi
        E = alpha * eps + omega * L
        frags.append((E, L))
    (E1, L1), (E2, L2) = frags
    assert E1 < 0 < E2 and abs(E1 + E2 - E0) < 1e-12 and abs(L1 + L2 - L0) < 1e-12
    assert abs(R(r_s, E1, L1, m12)) < 1e-9 and abs(R(r_s, E2, L2, m12)) < 1e-9
    dR = lambda E, L, mu: (R(r_s + 1e-6, E, L, mu) - R(r_s - 1e-6, E, L, mu)) / 2e-6  # noqa: E731
    assert dR(E1, L1, m12) < 0 < dR(E2, L2, m12)  # fragment 1 falls in, fragment 2 goes out
    rr = np.linspace(r_s * 1.001, 200, 4000)
    assert np.all(R(rr, E2, L2, m12) > 0) and E2 > m12  # ... all the way to infinity
    # crossing the horizon requires E - Omega_H L >= 0; the area grows
    OmH, kap = st.omega_horizon(a), st.surface_gravity(a)
    assert E1 - OmH * L1 > 0
    dA = 8 * math.pi / kap * (E1 - OmH * L1)
    assert dA > 0
    # trajectories (Mino time): particle 0 backward from the split (lam < 0), fragments forward
    r0, ph0, tau0, _ = equatorial_geodesic(E0, L0, mu0, a, r_s, 0.0, -0.9, n=2500, r_stop=14.0)
    r1, ph1, tau1, _ = equatorial_geodesic(E1, L1, m12, a, r_s, 0.0, 6.0, n=2500, r_stop=0.25)
    r2, ph2, tau2, _ = equatorial_geodesic(E2, L2, m12, a, r_s, 0.0, 0.9, n=2500, r_stop=14.0)
    xy = lambda r, p: np.stack(st.kerr_schild_xy(r, p, a), 1)  # noqa: E731
    return dict(pp_a=a, pp_r=r_s, pp_E=np.array([E0, E1, E2]), pp_L=np.array([L0, L1, L2]), pp_m=m12, pp_dA=dA,
                pp_in=xy(r0, ph0), pp_tau0=tau0, pp_neg=xy(r1, ph1), pp_r1=r1, pp_tau1=tau1, pp_out=xy(r2, ph2),
                pp_tau2=tau2, pp_gain=E2 - E0)


# ---------------------------------------------------------------------------
# Kerr ray traces
# ---------------------------------------------------------------------------
KERR_A = 0.99
KERR_R_OUT = 26.0  # the same outer edge as part 1's disk (13 r_s)


def shadow_mask_from_constants(d, a, incl_deg, with_distance=False):
    """Which pixels Bardeen's analytic curve says are in the shadow, from each ray's exact constants of motion:
    (alpha, beta) = (-L / sin i, p_theta).  With ``with_distance``, also each pixel's distance from the edge (in M,
    measured radially from the curve's center)."""
    inc = math.radians(incl_deg)
    al = -d["L"] / math.sin(inc)
    be = d["beta"]
    ca, cb = st.shadow_curve(max(a, 1e-3), inc, 4000)
    cx = 0.5 * (ca.max() + ca.min())
    ang_c, rad_c = np.arctan2(cb, ca - cx), np.hypot(ca - cx, cb)
    o = np.argsort(ang_c)
    rc = np.interp(np.arctan2(be, al - cx), ang_c[o], rad_c[o], period=2 * np.pi)
    rad = np.hypot(al - cx, be)
    if with_distance:
        return rad < rc, np.abs(rad - rc)
    return rad < rc


def compute_kerr(incl, a=KERR_A):
    """Ray trace of the disk around a Kerr hole of spin a (a = 1e-4: effectively Schwarzschild, traced and shaded
    exactly like the spinning one, for side-by-side comparisons)."""
    from .raytrace import trace_kerr

    d = trace_kerr(a, incl, r_out=KERR_R_OUT)
    pred, dist = shadow_mask_from_constants(d, a, incl, with_distance=True)
    free = ~np.isfinite(d["hit_r"])  # rays that don't hit the disk first
    mism = (pred != d["captured"]) & free
    # every pixel agrees, except possibly rays grazing the edge itself (within 0.02M, a tenth of a pixel)
    assert not np.any(mism & (dist > 0.02)), int((mism & (dist > 0.02)).sum())
    # Doppler + gravitational shift of the disk light: g = 1 / (u^t (1 - Omega L)), photon E = 1
    ok = np.isfinite(d["hit_r"])
    g = np.full(d["hit_r"].shape, np.nan)
    r = d["hit_r"][ok]
    Om = st.kepler_omega(r, a)
    gtt, gtp, gpp, _, _ = st.kerr_metric(r, math.pi / 2, a)
    ut = 1 / np.sqrt(-(gtt + 2 * gtp * Om + gpp * Om**2))
    g[ok] = 1 / (ut * (1 - Om * d["L"][ok]))
    d["g"] = g
    if incl > 45:
        H, W = g.shape
        left = np.nanmean(g[:, : W // 2])
        right = np.nanmean(g[:, W // 2:])
        assert left > right + 0.1  # the approaching (left) side is blueshifted
    # Page-Thorne flux: tends to part 1's Schwarzschild flux as a -> 0
    from videos.relativity.common import page_thorne

    rs_ = np.linspace(6.5, 26, 200)
    k0 = st.page_thorne_kerr(rs_, 1e-9)
    k1 = page_thorne(rs_ / 2)
    assert np.max(np.abs(k0 / k0.max() - k1 / k1.max())) < 1e-3
    d["mismatch"] = np.array(mism.sum())
    for k in ("L", "beta"):
        d[k] = d[k].astype(np.float32)
    return d


def compute_shadows():
    out = {}
    spins = np.array([0.0, 0.01, 0.2, 0.4, 0.6, 0.8, 0.9, 0.95, 0.99, 0.998])
    for incl in (90, 80):
        curves = np.array([np.stack(st.shadow_curve(a, math.radians(incl), 600), 1) for a in spins])
        out[f"curves_{incl}"] = curves
    out["spins"] = spins
    # a -> 0: a circle of radius sqrt(27) M
    c1 = out["curves_90"][1]  # a = 0.01: within O(a) of the Schwarzschild circle of radius sqrt(27)
    rad = np.hypot(c1[:, 0] - 0.5 * (c1[:, 0].max() + c1[:, 0].min()), c1[:, 1])
    assert np.max(np.abs(rad - math.sqrt(27))) < 0.03
    # a = 0.998 edge-on: the flat side at alpha ~ -2 (prograde photons), the round side at ~ +7
    c9 = out["curves_90"][-1]
    assert -2.3 < c9[:, 0].min() < -1.6 and 6.8 < c9[:, 0].max() < 7.1
    return out


# ---------------------------------------------------------------------------
# Quasinormal modes and the ringdown
# ---------------------------------------------------------------------------
def leaver_schwarzschild(l=2, s=2, guess=0.747 - 0.178j, n_terms=400):
    """Leaver (1985) continued fraction for the fundamental Schwarzschild mode (units 2M = 1, time dependence
    e^{-i omega t}): 0 = beta_0 - alpha_0 gamma_1 / (beta_1 - alpha_1 gamma_2 / (beta_2 - ...))."""
    from scipy.optimize import fsolve

    def cf(w):
        rho = -1j * w
        eps = s * s - 1
        alpha = lambda n: n * n + (2 * rho + 2) * n + 2 * rho + 1  # noqa: E731
        beta = lambda n: -(2 * n * n + (8 * rho + 2) * n + 8 * rho * rho + 4 * rho + l * (l + 1) - eps)  # noqa: E731
        gamma = lambda n: n * n + 4 * rho * n + 4 * rho * rho - eps - 1  # noqa: E731
        val = 0j
        for n in range(n_terms, 0, -1):
            val = alpha(n - 1) * gamma(n) / (beta(n) - val)
        return beta(0) - val

    def f(x):
        v = cf(x[0] + 1j * x[1])
        return [v.real, v.imag]

    x = fsolve(f, [guess.real, guess.imag], xtol=1e-13)
    return (x[0] + 1j * x[1])


def regge_wheeler(l=2, x_min=-300.0, x_max=600.0, dx=0.1, t_end=420.0, x0=30.0, sigma=3.0, x_obs=60.0):
    """Evolve psi_tt = psi_xx - V(x) psi on the tortoise coordinate x = r* (M = 1), with the axial gravitational
    potential V = (1 - 2/r)(l(l+1)/r^2 - 6/r^3), from an ingoing Gaussian pulse.  The observer sits behind the
    pulse (farther out), so it records only what the potential barrier sends back."""
    x = np.arange(x_min, x_max, dx)
    r = st.r_of_tortoise(x)
    V = (1 - 2 / r) * (l * (l + 1) / r**2 - 6 / r**3)
    dt = 0.5 * dx
    psi = np.exp(-((x - x0) ** 2) / (2 * sigma**2))
    # ingoing: psi(t, x) = F(x + t)  =>  psi(-dt) = F(x - dt)
    psi_prev = np.exp(-((x - dt - x0) ** 2) / (2 * sigma**2))
    k_obs = int(round((x_obs - x_min) / dx))
    nsteps = int(t_end / dt)
    obs = np.zeros(nsteps)
    snaps, snap_t = [], []
    lam = (dt / dx) ** 2
    for n in range(nsteps):
        lap = np.zeros_like(psi)
        lap[1:-1] = psi[2:] - 2 * psi[1:-1] + psi[:-2]
        new = 2 * psi - psi_prev + lam * lap - dt * dt * V * psi
        new[0], new[-1] = psi[1], psi[-2]  # crude outgoing edges (far away: reflections arrive after t_end)
        psi_prev, psi = psi, new
        obs[n] = psi[k_obs]
        if n % 20 == 0:
            snaps.append(psi[::10].copy())
            snap_t.append((n + 1) * dt)
    return dict(x=x[::10], V=V[::10], obs_t=(np.arange(nsteps) + 1) * dt, obs=obs, snaps=np.array(snaps, np.float32),
                snap_t=np.array(snap_t), r=r[::10])


def fit_ringdown(t, y, t0, t1):
    """Least-squares fit of A e^{-w_i t} cos(w_r t + phi) on [t0, t1] (log-linear start, then nonlinear)."""
    from scipy.optimize import least_squares

    m = (t > t0) & (t < t1)
    tt, yy = t[m], y[m]

    def res(p):
        A, wr, wi, ph = p
        return A * np.exp(-wi * (tt - t0)) * np.cos(wr * (tt - t0) + ph) - yy

    best = None
    for ph in np.linspace(0, 2 * np.pi, 8, endpoint=False):
        s = least_squares(res, [np.max(np.abs(yy)), 0.37, 0.09, ph], x_scale=[np.max(np.abs(yy)), 0.1, 0.03, 1])
        if best is None or s.cost < best.cost:
            best = s
    return best.x


def compute_qnm():
    out = {}
    w = leaver_schwarzschild()  # 2M = 1 units
    wM = w / 2
    assert abs(wM.real - 0.37367) < 2e-5 and abs(-wM.imag - 0.08896) < 2e-5, wM
    out["w_schw"] = np.array([wM.real, wM.imag])
    # eikonal (photon-sphere) estimate: omega ~ (l + 1/2) Omega_ph - i/2 lambda, Omega_ph = lambda = 1/(3 sqrt 3)
    out["w_eik"] = np.array([2.5 / math.sqrt(27), -0.5 / math.sqrt(27)])
    # Kerr (2,2,0) as a function of spin (qnm package: Leaver's method, Cook & Zalutskiy's spectral angular solver)
    import qnm as qnm_pkg

    seq = qnm_pkg.modes_cache(s=-2, l=2, m=2, n=0)
    spins = np.linspace(0, 0.99, 34)
    ws = np.array([seq(a=float(a))[0] for a in spins])
    assert abs(ws[0].real - wM.real) < 1e-5 and abs(ws[0].imag - wM.imag) < 1e-5
    # Berti-Cardoso-Will fits (2006): within their stated accuracy (f: 1.85%, Q: 0.88%)
    fit_w = 1.5251 - 1.1568 * (1 - spins) ** 0.1292
    fit_Q = 0.7000 + 1.4187 * (1 - spins) ** (-0.4990)
    Q = ws.real / (2 * -ws.imag)
    assert np.max(np.abs(fit_w / ws.real - 1)) < 0.02 and np.max(np.abs(fit_Q / Q - 1)) < 0.01
    out["kerr_spins"], out["kerr_w"] = spins, np.stack([ws.real, ws.imag], 1)
    # GW150914 (LVK 2016 test of GR: detector-frame M_f = 68, chi_f = 0.67 -> 251 +- 8 Hz, 4.0 +- 0.3 ms)
    # GW250114 (detector-frame M_f = 68.1, chi_f = 0.68 -> measured 251.7 +- 5 Hz, 4.09 ms)
    for name, Mf, chi in (("gw150914", 68.0, 0.67), ("gw250114", 68.1, 0.68)):
        wk = seq(a=chi)[0]
        f = wk.real / (2 * math.pi * Mf * T_SUN)
        tau = Mf * T_SUN / -wk.imag
        out[name + "_f"], out[name + "_tau"] = f, tau
    assert abs(out["gw150914_f"] - 251) < 8 and abs(out["gw150914_tau"] * 1e3 - 4.0) < 0.3
    assert abs(out["gw250114_f"] - 251.7) < 5 and abs(out["gw250114_tau"] * 1e3 - 4.09) < 0.4
    # time domain: a pulse scattering off the Regge-Wheeler barrier rings at the quasinormal frequency
    rw = regge_wheeler()
    t, y = rw["obs_t"], rw["obs"]
    peak = t[np.argmax(np.abs(y))]
    # a single damped sinusoid fitted over several windows after the peak (earlier: overtones; later: the tail)
    for w0, w1 in ((20, 60), (25, 85), (30, 80), (35, 90)):
        A, wr, wi, ph = fit_ringdown(t, y, peak + w0, peak + w1)
        assert abs(wr - wM.real) < 0.015 * wM.real and abs(wi - (-wM.imag)) < 0.03 * (-wM.imag), (w0, wr, wi)
    A, wr, wi, ph = fit_ringdown(t, y, peak + 30, peak + 80)
    out.update({"rw_" + k: v for k, v in rw.items()})
    out["rw_fit"] = np.array([A, wr, wi, ph, peak + 30])
    # Price's late-time tail ~ t^-(2l+3) = t^-7 for l = 2
    late = (t > peak + 200) & (t < t[-1] - 5)
    out["tail_slope"] = np.polyfit(np.log(t[late]), np.log(np.abs(y[late]) + 1e-300), 1)[0]
    # the overtone (n = 1) is more strongly damped
    w1 = qnm_pkg.modes_cache(s=-2, l=2, m=2, n=1)(a=0.0)[0]
    assert abs(w1.real - 0.34671) < 1e-4 and abs(-w1.imag - 0.27391) < 1e-4
    out["w_overtone"] = np.array([w1.real, w1.imag])
    # GW150914's whitened, band-passed Hanford strain after the peak, with the fundamental mode's f and tau fixed
    # (only an amplitude and a phase fitted): whitening at ~250 Hz is close to a constant gain and phase shift.
    from videos.relativity.compute import compute_gw

    g = compute_gw()
    tt, H = g["t"], g["H1"]
    k = np.argmax(np.abs(H) * ((tt > -0.02) & (tt < 0.02)))
    t_peak = tt[k]
    f0, tau0 = out["gw150914_f"], out["gw150914_tau"]
    win = (tt > t_peak + 0.003) & (tt < t_peak + 0.020)
    X = np.stack([np.exp(-(tt[win] - t_peak) / tau0) * np.cos(2 * np.pi * f0 * (tt[win] - t_peak)),
                  np.exp(-(tt[win] - t_peak) / tau0) * np.sin(2 * np.pi * f0 * (tt[win] - t_peak))], 1)
    coef, *_ = np.linalg.lstsq(X, H[win], rcond=None)
    model = X @ coef
    resid = np.sqrt(np.mean((H[win] - model) ** 2)) / np.sqrt(np.mean(H[win] ** 2))
    out.update(gw_t=tt, gw_H=H, gw_peak=t_peak, gw_coef=coef, gw_resid=resid)
    return out


# ---------------------------------------------------------------------------
# The inspiral and the binary pulsar
# ---------------------------------------------------------------------------
def compute_inspiral():
    out = {}
    # GW150914-like masses (GWTC-1, detector frame: (35.6, 30.6) x 1.09), leading order, in seconds
    m1, m2 = 35.6 * 1.09, 30.6 * 1.09
    M, mu = m1 + m2, m1 * m2 / (m1 + m2)
    Mc = mu ** 0.6 * M ** 0.4
    tM, tMc = M * T_SUN, Mc * T_SUN
    tau = np.geomspace(0.2, 2e-3, 3000)  # seconds before coalescence
    f = (1 / np.pi) * (5 / (256 * tau)) ** (3 / 8) * tMc ** (-5 / 8)
    phase = -2 * (tau / (5 * tMc)) ** (5 / 8)  # GW phase
    amp = (np.pi * f * tMc) ** (2 / 3)
    sep = (256 / 5 * mu * M**2 * T_SUN**3 * tau) ** 0.25 / T_SUN  # separation in units of M_sun c^2/G... in seconds
    # consistency: Kepler: (pi f)^2 = M / a^3
    a_s = (tM / (np.pi * f) ** 2) ** (1 / 3)  # separation in light-seconds
    a_peters = (256 / 5 * (mu * T_SUN) * tM**2 * tau) ** 0.25
    assert np.max(np.abs(a_s / a_peters - 1)) < 1e-9
    out.update(m1=m1, m2=m2, Mc=Mc, tau=tau, f=f, phase=phase, amp=amp, sep_km=a_s * c / 1e3)
    assert abs(Mc / 1.09 - 28.6) < 0.4
    # Hulse-Taylor (Weisberg & Huang 2016)
    Pb, e, mp, mc_ = 0.322997448918 * 86400, 0.6171340, 1.438, 1.390
    fe = (1 + 73 / 24 * e**2 + 37 / 96 * e**4) / (1 - e**2) ** 3.5
    Pdot = -192 * np.pi / 5 * (Pb / (2 * np.pi * T_SUN)) ** (-5 / 3) * fe * mp * mc_ * (mp + mc_) ** (-1 / 3)
    assert abs(fe - 11.857) < 0.001 and abs(Pdot / 1e-12 + 2.4026) < 0.001, Pdot
    wdot = 3 * (2 * np.pi / Pb) ** (5 / 3) * ((mp + mc_) * T_SUN) ** (2 / 3) / (1 - e**2)
    wdot_deg = math.degrees(wdot) * YEAR
    assert abs(wdot_deg - 4.226585) < 0.001
    # cumulative shift of periastron time: Delta T(t) = (Pdot / 2 Pb) t^2
    years = np.linspace(0, 52, 300)
    shift = Pdot / (2 * Pb) * (years * YEAR) ** 2
    assert abs(shift[np.argmin(np.abs(years - 30))] + 38.5) < 1.0
    # merger time: Peters' equations for a(t), e(t)
    Mtot = (mp + mc_) * GM_SUN
    beta = 64 / 5 * G**3 * mp * mc_ * (mp + mc_) * M_SUN**3 / c**5
    a0 = (Mtot * (Pb / (2 * np.pi)) ** 2) ** (1 / 3)

    def rhs(_, y):
        a, e = y
        da = -beta / a**3 * (1 + 73 / 24 * e**2 + 37 / 96 * e**4) / (1 - e**2) ** 3.5
        de = -19 / 12 * beta / a**4 * e * (1 + 121 / 304 * e**2) / (1 - e**2) ** 2.5
        return [da, de]

    ev = lambda _, y: y[0] - 1e6  # noqa: E731
    ev.terminal = True
    sol = solve_ivp(rhs, [0, 1e18], [a0, e], events=ev, rtol=1e-10, atol=1)
    t_merge = sol.t_events[0][0] / YEAR / 1e6
    assert abs(t_merge - 301) < 5, t_merge
    out.update(ht_Pdot=Pdot, ht_fe=fe, ht_wdot=wdot_deg, ht_years=years, ht_shift=shift, ht_merge=t_merge,
               ht_ratio=np.array([0.9983, 0.0016]))
    return out


# ---------------------------------------------------------------------------
# The quadrupole formula's angular integral
# ---------------------------------------------------------------------------
def compute_quad():
    r = rng(5)
    A = r.normal(size=(3, 3))
    Q = A + A.T
    Q -= np.eye(3) * np.trace(Q) / 3
    # integrate the TT projection of Q over the sphere: Lambda_ij,kl Q_ij Q_kl, with P = 1 - n n
    th = np.linspace(0, np.pi, 401)
    ph = np.linspace(0, 2 * np.pi, 801)
    T_, P_ = np.meshgrid(th, ph, indexing="ij")
    n = np.stack([np.sin(T_) * np.cos(P_), np.sin(T_) * np.sin(P_), np.cos(T_)], -1)
    Pm = np.eye(3) - n[..., :, None] * n[..., None, :]
    PQP = np.einsum("...ij,jk,...kl->...il", Pm, Q, Pm)
    tr = np.einsum("...ii->...", PQP)
    QTT = PQP - 0.5 * Pm * tr[..., None, None]
    integrand = np.einsum("...ij,...ij->...", QTT, QTT) * np.sin(T_)
    val = np.trapezoid(np.trapezoid(integrand, ph, axis=1), th)
    assert abs(val / (8 * np.pi / 5 * np.sum(Q * Q)) - 1) < 1e-4
    return dict(ratio=np.array(val / (8 * np.pi / 5 * np.sum(Q * Q))))


# ---------------------------------------------------------------------------
# Hawking radiation
# ---------------------------------------------------------------------------
def compute_hawking():
    out = {}
    kappa, b, eps = 1.0, 5.0, 0.01
    # phi(u) = exp(i b e^{-kappa u}) (regulated by e^{-eps e^{-kappa u}}): a wave stretched exponentially in time.
    # Its Fourier transform is exactly F(w) = Gamma(-i w/kappa) (eps - i b)^{i w/kappa} / kappa, so
    # |F(-w)|^2 / |F(w)|^2 = exp(-4 (w/kappa) arctan(b/eps)) -> exp(-2 pi w/kappa) as eps -> 0: a Boltzmann factor.
    from scipy.special import loggamma

    u = np.linspace(-40, 30, 4_000_001)
    x = np.exp(-kappa * u)
    phi = np.exp((1j * b - eps) * x)
    S = 0.5 * (1 + np.tanh(u / 2.0))  # smooth step, FT known: subtracted so the integrand decays at both ends
    omegas = np.linspace(0.25, 2.5, 19)
    Fp, Fm = [], []
    for w in omegas:
        vals = []
        for s_ in (1, -1):
            I = np.trapezoid((phi - S) * np.exp(1j * s_ * w * u), u)
            I += 0.5 * 1j * np.pi * 2.0 / np.sinh(np.pi * s_ * w)  # FT of S: (i/2) pi w0 / sinh(pi w w0 / 2), w0 = 2
            exact = np.exp(loggamma(-1j * s_ * w / kappa) + (1j * s_ * w / kappa) * np.log(eps - 1j * b)) / kappa
            assert abs(I / exact - 1) < 1e-4, (w, s_, I, exact)
            vals.append(I)
        Fp.append(vals[0])
        Fm.append(vals[1])
    Fp, Fm = np.array(Fp), np.array(Fm)
    ratio = np.abs(Fm) ** 2 / np.abs(Fp) ** 2
    boltz = np.exp(-2 * np.pi * omegas / kappa)
    assert np.max(np.abs(np.log(ratio / boltz))) < 0.03
    out.update(omegas=omegas, Fp2=np.abs(Fp) ** 2, Fm2=np.abs(Fm) ** 2, ratio=ratio, boltz=boltz)
    uu = np.linspace(-3, 6, 3000)
    out["wave_u"], out["wave"] = uu, np.cos(b * np.exp(-kappa * uu))
    # Peeling: outgoing rays launched at t~ = 0 from r = 2(1 + 10^-k) reach r = 10 at times spaced by 4M ln 10
    ks = np.arange(1, 9)
    arrive = np.array([outgoing_tt(10.0, 2 * (1 + 10.0 ** -k)) for k in ks])
    gaps = np.diff(arrive)
    assert np.allclose(gaps[-3:], 4 * math.log(10), rtol=1e-3)
    out.update(peel_k=ks, peel_t=arrive)
    # The Euclidean cigar: (r, tau_E) with period beta, embedded as a surface of revolution (M = 1)
    rr = np.linspace(2, 14, 1500)
    for name, frac in (("smooth", 1.0), ("cone", 0.55)):
        beta = frac * 8 * np.pi
        R = beta / (2 * np.pi) * np.sqrt(1 - 2 / rr)
        dz = np.sqrt(np.clip(1 / (1 - 2 / rr[1:]) - np.gradient(R, rr)[1:] ** 2, 0, None))
        z = np.concatenate([[0], np.cumsum(0.5 * (dz[1:] + dz[:-1]) * np.diff(rr[1:]))])
        z = np.concatenate([[0], z])
        out[f"cigar_{name}_R"], out[f"cigar_{name}_z"] = R, z
    # near the tip: circumference / (2 pi x proper distance from the tip) -> 1 only for beta = 8 pi M
    r_ = 2 + 1e-6
    rho = math.sqrt(r_ * (r_ - 2)) + 2 * math.log((math.sqrt(r_) + math.sqrt(r_ - 2)) / math.sqrt(2))
    for frac in (1.0, 0.55):
        assert abs(frac * 4 * math.sqrt(1 - 2 / r_) / rho - frac) < 1e-5
    # T(M) for a log-log plot
    Ms = np.geomspace(1e11, 1e41, 300)  # kg
    out["TM_M"], out["TM_T"] = Ms, hbar * c**3 / (8 * np.pi * G * Ms * kB)
    return out


def outgoing_tt(r_target, r_start):
    """EF time t~ for an outgoing ray from r_start at t~ = 0 to reach r_target (M = 1)."""
    return (r_target - r_start) + 4 * math.log((r_target - 2) / (r_start - 2))


# ---------------------------------------------------------------------------
# Cosmology: flat Lambda-CDM with radiation (Planck 2018, as in part 1: H0 = 67.4, Omega_m = 0.315)
# ---------------------------------------------------------------------------
def compute_cosmo2():
    out = {}
    h = 0.674
    H0 = 100 * h * 1e3 / 3.085_677_581e22  # 1/s
    Gyr = 3.155_76e16
    Gly = 9.460_730_472_580_8e24  # m
    Om, Or = 0.315, 4.18e-5 / h**2
    OL = 1 - Om - Or
    out.update(Om=Om, Or=Or, OL=OL, H0_kms=67.4)

    def H(a):
        return H0 * np.sqrt(Or / a**4 + Om / a**3 + OL)

    a = np.geomspace(1e-9, 1e3, 200_001)
    # t(a) = int da/(a H), eta(a) = int da/(a^2 H) (comoving distance light travels, in units of c)
    dt = 1 / (a * H(a))
    deta = 1 / (a * a * H(a))
    la = np.log(a)
    t = np.concatenate([[0], np.cumsum(0.5 * (dt[1:] * a[1:] + dt[:-1] * a[:-1]) * np.diff(la))]) + a[0] ** 2 / (2 * H0 * math.sqrt(Or))
    eta = np.concatenate([[0], np.cumsum(0.5 * (deta[1:] * a[1:] + deta[:-1] * a[:-1]) * np.diff(la))]) + a[0] / (H0 * math.sqrt(Or))
    t_gyr = t / Gyr
    eta_gly = eta * c / Gly
    age = float(np.interp(0.0, la, t_gyr))
    eta0 = float(np.interp(0.0, la, eta_gly))
    # eta at a -> infinity: the remaining integral beyond a = 1e3 is ~ 1/(a H0 sqrt(OL))
    eta_inf = eta_gly[-1] + c / (H0 * math.sqrt(OL)) / a[-1] / Gly
    assert abs(age - 13.79) < 0.03, age
    assert abs(eta0 - 46.1) < 0.4, eta0  # particle horizon today (comoving), Gly
    ev_now = eta_inf - eta0
    assert abs(ev_now - 16.7) < 0.2, ev_now  # event horizon today
    hub_now = c / H0 / Gly
    assert abs(hub_now - 14.5) < 0.05
    # z where the comoving distance equals c/H0 (recession speed = c today)
    chi_of_z = lambda z: eta0 - float(np.interp(-math.log(1 + z), la, eta_gly))  # noqa: E731
    z_c = brentq(lambda z: chi_of_z(z) - hub_now, 0.5, 3)
    assert abs(z_c - 1.48) < 0.02, z_c
    # last scattering, z = 1090: comoving distance, horizon size then, and the angle between
    z_ls = 1090.0
    a_ls = 1 / (1 + z_ls)
    D_ls = chi_of_z(z_ls)
    eta_ls = float(np.interp(math.log(a_ls), la, eta_gly))
    theta_h = math.degrees(eta_ls / D_ls)
    t_ls = float(np.interp(math.log(a_ls), la, t_gyr)) * 1e9
    assert abs(D_ls * 0.306_601 - 13.87 * 1000 / 1000 * 1) < 0.15, D_ls  # 13.87 Gpc = 45.2 Gly
    assert 1.05 < theta_h < 1.25, theta_h
    assert 3.5e5 < t_ls < 4.0e5, t_ls
    z_eq = Om / Or - 1
    z_mL = (OL / Om) ** (1 / 3) - 1
    assert abs(z_eq - 3400) < 40 and abs(z_mL - 0.30) < 0.01
    out.update(age=age, eta0=eta0, eta_inf=eta_inf, event_now=ev_now, hubble_now=hub_now, z_c=z_c, D_ls=D_ls,
               eta_ls=eta_ls, theta_h=theta_h, t_ls=t_ls, z_eq=z_eq, z_mL=z_mL)
    # curves on a time grid (Gyr), for the Davis-Lineweaver diagrams
    tg = np.linspace(1e-4, 60, 3000)
    ag = np.exp(np.interp(tg, t_gyr, la))
    etag = np.interp(tg, t_gyr, eta_gly)
    Hg = H(ag) * Gyr  # 1/Gyr
    out.update(tg=tg, ag=ag, etag=etag)
    out["particle_com"] = etag
    out["event_com"] = eta_inf - etag
    out["hubble_com"] = (c / (ag * Hg / Gyr)) / Gly
    out["cone_com"] = np.where(tg <= age, eta0 - etag, np.nan)  # our past light cone
    # the light cone in proper distance has its maximum where it crosses the Hubble sphere
    pc = ag * out["cone_com"]
    k = np.nanargmax(pc)
    assert abs(pc[k] - (ag * out["hubble_com"])[k]) / pc[k] < 0.01
    out["cone_max_t"], out["cone_max_d"] = tg[k], pc[k]
    # component densities vs a (in units of today's critical density)
    aa = np.geomspace(1e-6, 10, 600)
    out.update(rho_a=aa, rho_r=Or / aa**4, rho_m=Om / aa**3, rho_L=np.full_like(aa, OL))
    # a family of Friedmann universes, all with today's H0, plotted against time from today (Gyr)
    fam = {}
    for name, (om, ol, orr) in {"closed": (3.0, 0.0, 0.0), "flat_matter": (1.0, 0.0, 0.0), "open": (0.3, 0.0, 0.0),
                                "lcdm": (Om, OL, Or), "desitter": (0.0, 1.0, 0.0)}.items():
        ok_ = 1 - om - ol - orr

        def adot(a_, om=om, ol=ol, orr=orr, ok_=ok_):
            return H0 * Gyr * a_ * np.sqrt(np.maximum(orr / a_**4 + om / a_**3 + ok_ / a_**2 + ol, 0))

        # integrate forward and backward from a = 1 in time; a closed universe turns around (use the
        # second-order acceleration equation there)
        def rhs(_, y):
            a_, v = y
            return [v, (H0 * Gyr) ** 2 * a_ * (-orr / a_**4 - om / (2 * a_**3) + ol)]

        y0 = [1.0, float(adot(1.0))]
        ev = lambda _, y: y[0] - 1e-3  # noqa: E731
        ev.terminal = True
        fw = solve_ivp(rhs, [0, 80], y0, events=ev, max_step=0.02, rtol=1e-9)
        bw = solve_ivp(rhs, [0, -40], y0, events=ev, max_step=0.02, rtol=1e-9)
        T = np.concatenate([bw.t[::-1], fw.t[1:]])
        A = np.concatenate([bw.y[0][::-1], fw.y[0][1:]])
        fam[name] = np.stack([T, A], 1)
    flat_age = -fam["flat_matter"][0, 0]
    assert abs(flat_age - 2 / 3 / (H0 * Gyr)) < 0.05  # Einstein-de Sitter: t0 = 2/(3 H0) = 9.7 Gyr
    assert fam["closed"][-1, 1] < 0.01  # the closed universe recollapses
    for k_, v in fam.items():
        out["fam_" + k_] = v
    return out


# ---------------------------------------------------------------------------
ITEMS = {
    "consts": compute_consts,
    "infall": compute_infall,
    "bridge": compute_bridge,
    "collapse": compute_collapse,
    "raych": compute_raych,
    "gpb": compute_gpb,
    "kerr_orbits": compute_kerr_orbits,
    "kerr80": lambda: compute_kerr(80.0),
    "kerr20": lambda: compute_kerr(20.0),
    "kerr80_0": lambda: compute_kerr(80.0, 1e-4),
    "kerr20_0": lambda: compute_kerr(20.0, 1e-4),
    "shadows": compute_shadows,
    "qnm": compute_qnm,
    "inspiral": compute_inspiral,
    "quad": compute_quad,
    "hawking": compute_hawking,
    "cosmo2": compute_cosmo2,
}

_loaded: dict[str, dict] = {}


def path(name: str):
    return DATA_DIR / f"{name}.npz"


def load(name: str) -> dict:
    if name not in _loaded:
        p = path(name)
        if not p.exists():
            raise FileNotFoundError(f"Missing '{name}'. Run: python -m videos.relativity2.compute {name}")
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
