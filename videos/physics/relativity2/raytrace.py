"""Backward ray tracing of a thin accretion disk around a Kerr black hole (units G = c = M = 1).

Light rays are Kerr null geodesics.  With Carter's constant Q they separate; in Mino time (d lambda_M = d lambda /
Sigma) the radial and polar motions decouple completely, and differentiating (dr/d lambda_M)^2 = R(r) and
(d theta/d lambda_M)^2 = Theta(theta) gives second-order equations with no square roots and no turning-point signs:

    r''     = R'(r) / 2,       R(r)     = (r^2 + a^2 - a L)^2 - Delta (Q + (L - a)^2)
    theta'' = Theta'(theta)/2, Theta(theta) = Q + a^2 cos^2 theta - L^2 cot^2 theta
    phi'    = -(a - L / sin^2 theta) + a (r^2 + a^2 - a L) / Delta          (E = 1)

Each pixel's ray starts at a camera (a zero-angular-momentum observer at r = 100 M, like the Schwarzschild
renders of part 1, which sat at 50 r_s) and is integrated backward with fourth-order Runge-Kutta, until it falls
into the horizon, escapes, or hits the opaque disk in the equatorial plane.
"""

from __future__ import annotations

import math

import numpy as np
from numba import njit, prange

from .spacetime import kerr_metric


def camera_rays(a, incl_deg, W, H, fov_deg=36.0, r0=100.0):
    """Constants of motion and initial Mino-time velocities of each pixel's (backward) ray.

    The camera at (r0, theta0 = incl, phi = 0) looks at the hole; screen right is +phi, screen up is -theta (toward the
    spin axis).  A photon arriving along -d (d the viewing direction) has, in the ZAMO frame, direction n = -d."""
    th0 = math.radians(incl_deg)
    gtt, gtp, gpp, S, D = kerr_metric(r0, th0, a)
    A = (r0 * r0 + a * a) ** 2 - a * a * D * math.sin(th0) ** 2
    alpha = math.sqrt(S * D / A)
    omega = 2 * a * r0 / A
    fx = math.tan(math.radians(fov_deg) / 2)
    xs = ((np.arange(W) + 0.5) / W * 2 - 1) * fx
    ys = -((np.arange(H) + 0.5) / H * 2 - 1) * fx * H / W
    X, Y = np.meshgrid(xs, ys)
    N = np.sqrt(1 + X * X + Y * Y)
    n_r, n_ph, n_th = 1 / N, -X / N, Y / N
    pt = 1 / alpha
    pph = omega / alpha + n_ph / math.sqrt(gpp)
    pr = n_r * math.sqrt(D / S)
    pth = n_th / math.sqrt(S)
    p_t = gtt * pt + gtp * pph
    p_ph = gtp * pt + gpp * pph
    E = -p_t
    L = p_ph / E
    pth_low = S * pth / E
    Q = pth_low**2 + math.cos(th0) ** 2 * (L * L / math.sin(th0) ** 2 - a * a)
    vr = S * pr / E  # Mino-time velocities of the physical photon
    vth = S * pth / E
    return dict(L=L, Q=Q, vr=-vr, vth=-vth, r0=r0, th0=th0, E_cam=1 / E, X=X, Y=Y, beta=pth_low)


@njit(cache=True, fastmath=False)
def _rhs(r, th, L, Q, a, K):
    s = math.sin(th)
    c = math.cos(th)
    P = r * r + a * a - a * L
    D = r * r - 2 * r + a * a
    dvr = 0.5 * (4 * r * P - (2 * r - 2) * K)
    dvth = 0.5 * (-2 * a * a * c * s + 2 * L * L * c / (s * s * s))
    dph = -(-(a - L / (s * s)) + a * P / D)  # backward in time
    return dph, dvr, dvth


@njit(parallel=True, cache=True)
def _trace(L, Q, vr0, vth0, r0, th0, a, r_in, r_out, r_hor, r_esc, eps, max_steps):
    n = L.shape[0]
    hit_r = np.full(n, np.nan)
    hit_phi = np.full(n, np.nan)
    hit_k = np.full(n, -1, np.int64)
    captured = np.zeros(n, np.bool_)
    dirs = np.zeros((n, 3))
    nsteps = np.zeros(n, np.int64)
    for i in prange(n):
        l, q = L[i], Q[i]
        K = q + (l - a) ** 2
        r, th, ph, vr, vth = r0, th0, 0.0, vr0[i], vth0[i]
        k = 0
        for it in range(max_steps):
            dph, _, _ = _rhs(r, th, l, q, a, K)
            h = eps / (abs(vr) / r + abs(vth) + abs(dph) + 1e-9)
            # RK4
            a1, b1, c1 = _rhs(r, th, l, q, a, K)
            r2, t2, vr2, vt2 = r + 0.5 * h * vr, th + 0.5 * h * vth, vr + 0.5 * h * b1, vth + 0.5 * h * c1
            a2, b2, c2 = _rhs(r2, t2, l, q, a, K)
            r3, t3, vr3, vt3 = r + 0.5 * h * vr2, th + 0.5 * h * vt2, vr + 0.5 * h * b2, vth + 0.5 * h * c2
            a3, b3, c3 = _rhs(r3, t3, l, q, a, K)
            r4, t4, vr4, vt4 = r + h * vr3, th + h * vt3, vr + h * b3, vth + h * c3
            a4, b4, c4 = _rhs(r4, t4, l, q, a, K)
            rn = r + h / 6 * (vr + 2 * vr2 + 2 * vr3 + vr4)
            tn = th + h / 6 * (vth + 2 * vt2 + 2 * vt3 + vt4)
            pn = ph + h / 6 * (a1 + 2 * a2 + 2 * a3 + a4)
            vrn = vr + h / 6 * (b1 + 2 * b2 + 2 * b3 + b4)
            vtn = vth + h / 6 * (c1 + 2 * c2 + 2 * c3 + c4)
            # Project back onto the exact first integrals vr^2 = R(r), vth^2 = Theta(theta).  A ray falling from
            # r = 100 (R ~ 1e8) to r ~ 1 (R ~ 1) otherwise keeps the absolute error made far away, and near the hole
            # it becomes a spurious turning point.  Near a real turning point (R about to vanish within a few steps)
            # the second-order equation is left to turn the ray around by itself.
            Pn = rn * rn + a * a - a * l
            Rn = Pn * Pn - (rn * rn - 2 * rn + a * a) * K
            dRn = 4 * rn * Pn - (2 * rn - 2) * K
            if Rn > 0 and Rn > 8 * abs(dRn * vrn) * h:
                vrn = math.copysign(math.sqrt(Rn), vrn)
            sn, cn = math.sin(tn), math.cos(tn)
            Tn = q + a * a * cn * cn - l * l * cn * cn / (sn * sn)
            dTn = -2 * a * a * cn * sn + 2 * l * l * cn / (sn * sn * sn)
            if Tn > 0 and Tn > 8 * abs(dTn * vtn) * h:
                vtn = math.copysign(math.sqrt(Tn), vtn)
            # equatorial-plane crossing
            if (th - 0.5 * math.pi) * (tn - 0.5 * math.pi) < 0:
                f = (0.5 * math.pi - th) / (tn - th)
                rc = r + f * (rn - r)
                pc = ph + f * (pn - ph)
                if rc > r_in and rc < r_out:
                    hit_r[i] = rc
                    hit_phi[i] = pc
                    hit_k[i] = k
                    nsteps[i] = it
                    break
                k += 1
            r, th, ph, vr, vth = rn, tn, pn, vrn, vtn
            if r < r_hor:
                captured[i] = True
                nsteps[i] = it
                break
            if r > r_esc and vr > 0:
                s, c = math.sin(th), math.cos(th)
                sp, cp = math.sin(ph), math.cos(ph)
                dph_, _, _ = _rhs(r, th, l, q, a, K)
                # velocity = vr r_hat + r vth theta_hat + r sin(th) phi' phi_hat (flat space far away)
                vx = vr * s * cp + r * vth * c * cp - r * s * dph_ * sp
                vy = vr * s * sp + r * vth * c * sp + r * s * dph_ * cp
                vz = vr * c - r * vth * s
                nn = math.sqrt(vx * vx + vy * vy + vz * vz)
                dirs[i, 0], dirs[i, 1], dirs[i, 2] = vx / nn, vy / nn, vz / nn
                nsteps[i] = it
                break
    return hit_r, hit_phi, hit_k, captured, dirs, nsteps


def trace_kerr(a, incl_deg, W=1280, H=720, r_in=None, r_out=26.0, eps=0.012, max_steps=40000):
    from .spacetime import isco, r_plus

    cam = camera_rays(a, incl_deg, W, H)
    r_in = isco(a) if r_in is None else r_in
    r_hor = r_plus(a) * 1.0005 + 1e-4
    hit_r, hit_phi, hit_k, cap, dirs, nst = _trace(
        cam["L"].ravel(), cam["Q"].ravel(), cam["vr"].ravel(), cam["vth"].ravel(), cam["r0"], cam["th0"], a, r_in,
        r_out, r_hor, 400.0, eps, max_steps)
    sh = (H, W)
    return dict(hit_r=hit_r.reshape(sh), hit_phi=hit_phi.reshape(sh), hit_k=hit_k.reshape(sh),
                captured=cap.reshape(sh), dir=dirs.reshape(H, W, 3).astype(np.float32), L=cam["L"],
                Q=cam["Q"], beta=cam["beta"], steps=nst.reshape(sh), r_in=np.array(r_in), a=np.array(a),
                incl=np.array(incl_deg))
