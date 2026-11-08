"""Space and time, built (Part 25).

* Newton's bucket: the paraboloid water surface z = omega^2 r^2 / 2g, and a relational check: the matrix of
  distances between bodies is the same in a rotating and a non-rotating universe, though the water knows the
  difference.
* Leibniz's shifts: translations, rotations and uniform boosts of the whole universe leave every relation fixed.
* Kant's incongruent counterparts: a left and a right hand in the plane have opposite orientation (signed area), so no
  rigid motion of the plane maps one onto the other; carried once round a Möbius strip, a frame comes back reversed.
* Non-Euclidean geometry in the Poincaré disk: geodesics as arcs orthogonal to the boundary, hyperbolic distance,
  triangles whose angles sum to less than pi with area equal to the defect; Gauss's survey triangle's spherical excess
  on the curved Earth.
* Poincaré's disk world: rulers that shrink with temperature make Euclidean space measure as hyperbolic.
* Special relativity: Lorentz transformations, the relativity of simultaneity, the boost that makes a spacelike event
  simultaneous with here-now (the Rietdijk--Putnam step), Reichenbach's epsilon.
* The hole argument: a diffeomorphism that is the identity outside a region and deforms the inside.
* Deutsch's model of closed timelike curves: fixed points of the map a time-travelling (qu)bit undergoes, classical and
  quantum, for the grandfather paradox and the knowledge paradox.
* The twins: proper time along worldlines; the straight worldline is the longest (reversed triangle inequality).
* Causal sets: events sprinkled into a diamond of flat spacetime; from the causal order alone, the fraction of related
  pairs recovers the dimension (the Myrheim--Meyer estimator).
"""

from __future__ import annotations

import math

import numpy as np


# ---------------------------------------------------------------------------
# Newton's bucket and Leibniz's shifts
# ---------------------------------------------------------------------------
def bucket(omegas=(0.0, 2.0, 4.0, 6.0), radius: float = 0.15, g: float = 9.81, n: int = 41) -> dict:
    """Water in a bucket of the given radius (m) spinning at angular velocity omega (rad/s): its surface is the
    paraboloid z = omega^2 r^2 / (2 g), measured from the lowest point."""
    rs = np.linspace(-radius, radius, n)
    rows = []
    for w in omegas:
        z = w ** 2 * rs ** 2 / (2 * g)
        rows.append({"omega": w, "z": [round(float(v), 5) for v in z], "rise_mm": round(1000 * float(z.max()), 2)})
    return {"r": [round(float(r), 4) for r in rs], "rows": rows, "radius": radius}


def shifts(n: int = 6, seed: int = 1716) -> dict:
    """A small universe of n bodies. Apply a static shift (move everything 5 m), a rotation of the whole, a kinematic
    shift (give everything the same extra velocity) and a uniform rotation in time. Every inter-body distance, at every
    time, is unchanged by each, so relational facts cannot tell them apart. What does change, in Newton's physics, is
    the rotation: a rotating frame has centrifugal effects (the bucket)."""
    rng = np.random.default_rng(seed)
    p = rng.normal(size=(n, 2))
    v = rng.normal(size=(n, 2)) * 0.3
    ts = np.linspace(0, 3, 7)

    def dist(P):
        return np.linalg.norm(P[:, None, :] - P[None, :, :], axis=-1)

    def hist(f):
        return [dist(f(t)) for t in ts]

    base = hist(lambda t: p + v * t)
    th = 0.7
    R = np.array([[math.cos(th), -math.sin(th)], [math.sin(th), math.cos(th)]])

    def rot(a):
        return np.array([[math.cos(a), -math.sin(a)], [math.sin(a), math.cos(a)]])

    worlds = {
        "static shift": hist(lambda t: p + v * t + np.array([5.0, 0.0])),
        "rotated": hist(lambda t: (p + v * t) @ R.T),
        "kinematic shift": hist(lambda t: p + v * t + np.array([0.4, 0.0]) * t),
        "rotating": hist(lambda t: (p + v * t) @ rot(0.5 * t).T),
    }
    rows = []
    for name, H in worlds.items():
        dev = max(float(np.abs(a - b).max()) for a, b in zip(base, H))
        rows.append({"world": name, "max_change_in_distances": dev, "relationally_same": dev < 1e-9,
                     "inertial_effects": name == "rotating"})
    return {"n": n, "rows": rows}


# ---------------------------------------------------------------------------
# Incongruent counterparts
# ---------------------------------------------------------------------------
LEFT_HAND = [(0, 0), (3, 0), (3, 4), (2.4, 4), (2.4, 1.6), (1.8, 1.6), (1.8, 5), (1.2, 5), (1.2, 1.6), (0.6, 1.6),
             (0.6, 4.4), (0, 4.4), (0, 0.6), (-1.2, 2.0), (-1.6, 1.6), (0, 0)]


def signed_area(poly) -> float:
    P = np.array(poly, float)
    x, y = P[:, 0], P[:, 1]
    return float(0.5 * (np.dot(x, np.roll(y, -1)) - np.dot(np.roll(x, -1), y)))


def incongruent() -> dict:
    """The left hand and its mirror image. A rigid motion of the plane (rotation and translation) has determinant +1
    and preserves the sign of the signed area; the mirror image has the opposite sign, so no rigid motion of the
    plane carries one onto the other. A rotation through the third dimension does. And on a Möbius strip, carrying
    the hand once around the strip reverses it."""
    left = LEFT_HAND
    right = [(-x, y) for x, y in left]
    a_l, a_r = signed_area(left), signed_area(right)
    # try many rigid motions of the plane: none reverses the sign
    rng = np.random.default_rng(1768)
    signs = []
    for _ in range(200):
        th = rng.random() * 2 * math.pi
        R = np.array([[math.cos(th), -math.sin(th)], [math.sin(th), math.cos(th)]])
        moved = (np.array(left) @ R.T) + rng.normal(size=2)
        signs.append(np.sign(signed_area(moved)))
    # Möbius transport: frame (tangent t, width direction w) along the centre circle with a half twist
    steps = 400
    frames = []
    for k in range(steps + 1):
        u = 2 * math.pi * k / steps
        t = np.array([-math.sin(u), math.cos(u), 0.0])
        radial = np.array([math.cos(u), math.sin(u), 0.0])
        z = np.array([0.0, 0.0, 1.0])
        w = math.cos(u / 2) * radial + math.sin(u / 2) * z     # the strip's width direction, half a turn per loop
        frames.append((t, w))
    n0 = np.cross(frames[0][0], frames[0][1])
    n1 = np.cross(frames[-1][0], frames[-1][1])
    return {"left_area": round(a_l, 3), "right_area": round(a_r, 3), "rigid_motions_tried": len(signs),
            "rigid_sign_changes": int(sum(1 for s in signs if s != np.sign(a_l))),
            "mobius_width_start": [round(float(x), 3) for x in frames[0][1]],
            "mobius_width_end": [round(float(x), 3) for x in frames[-1][1]],
            "mobius_orientation_flips": bool(np.dot(n0, n1) < 0), "left": left, "right": right}


# ---------------------------------------------------------------------------
# The Poincaré disk
# ---------------------------------------------------------------------------
def hyp_dist(u, v) -> float:
    u, v = np.asarray(u, float), np.asarray(v, float)
    num = 2 * np.dot(u - v, u - v)
    den = (1 - np.dot(u, u)) * (1 - np.dot(v, v))
    return float(np.arccosh(1 + num / den))


def geodesic(u, v, n: int = 60):
    """Points on the Poincaré-disk geodesic from u to v: an arc of the circle through u and v orthogonal to the unit
    circle (a diameter if u, v and the centre are collinear)."""
    u, v = np.asarray(u, float), np.asarray(v, float)
    cross = u[0] * v[1] - u[1] * v[0]
    if abs(cross) < 1e-9:
        return [list(map(float, u + (v - u) * s)) for s in np.linspace(0, 1, n)]
    # circle centre c with |c|^2 = r^2 + 1 passing through u and v: solve 2 c.u = |u|^2 + 1, 2 c.v = |v|^2 + 1
    A = 2 * np.array([u, v])
    b = np.array([np.dot(u, u) + 1, np.dot(v, v) + 1])
    c = np.linalg.solve(A, b)
    r = math.sqrt(np.dot(c, c) - 1)
    a1 = math.atan2(u[1] - c[1], u[0] - c[0])
    a2 = math.atan2(v[1] - c[1], v[0] - c[0])
    d = (a2 - a1 + math.pi) % (2 * math.pi) - math.pi        # the short way round
    return [[float(c[0] + r * math.cos(a1 + d * s)), float(c[1] + r * math.sin(a1 + d * s))]
            for s in np.linspace(0, 1, n)]


def _tangent(path, at_start=True):
    P = np.array(path)
    return (P[1] - P[0]) if at_start else (P[-2] - P[-1])


def hyp_triangle(A, B, C) -> dict:
    """A hyperbolic triangle in the Poincaré disk: its sides (geodesic arcs), its angles (the disk is conformal, so
    Euclidean angles between the arcs' tangents), the angle sum, and its area, which equals the defect pi - sum."""
    sides = {"AB": geodesic(A, B), "BC": geodesic(B, C), "CA": geodesic(C, A)}

    def angle(p1, p2):
        a, b = p1 / np.linalg.norm(p1), p2 / np.linalg.norm(p2)
        return float(math.acos(max(-1.0, min(1.0, float(np.dot(a, b))))))

    alpha = angle(_tangent(sides["AB"]), _tangent(sides["CA"], at_start=False))
    beta = angle(_tangent(sides["BC"]), _tangent(sides["AB"], at_start=False))
    gamma = angle(_tangent(sides["CA"]), _tangent(sides["BC"], at_start=False))
    s = alpha + beta + gamma
    return {"A": list(A), "B": list(B), "C": list(C), "sides": sides,
            "angles_deg": [round(math.degrees(x), 2) for x in (alpha, beta, gamma)],
            "sum_deg": round(math.degrees(s), 2), "defect": round(math.pi - s, 4),
            "lengths": [round(hyp_dist(A, B), 3), round(hyp_dist(B, C), 3), round(hyp_dist(C, A), 3)]}


def disk_triangles() -> dict:
    """Triangles of growing size, centred in the disk: the angle sum falls from nearly 180 degrees toward 0 as they
    grow, and the area (= defect) approaches pi."""
    rows = []
    for rho in (0.1, 0.3, 0.5, 0.7, 0.9):
        pts = [(rho * math.cos(a), rho * math.sin(a)) for a in (math.pi / 2, math.pi / 2 + 2 * math.pi / 3,
                                                                math.pi / 2 + 4 * math.pi / 3)]
        t = hyp_triangle(*pts)
        rows.append({"rho": rho, "sum_deg": t["sum_deg"], "area": t["defect"], "side": t["lengths"][0],
                     "sides": t["sides"], "points": [list(p) for p in pts]})
    return {"rows": rows}


def gauss_triangle(a_km: float = 69.0, b_km: float = 85.0, c_km: float = 107.0, R_km: float = 6371.0) -> dict:
    """Gauss's survey triangle (Brocken, Hohenhagen, Inselsberg; sides roughly 69, 85 and 107 km). On the curved
    surface of the Earth its angles exceed 180 degrees by the area over R^2 (Girard's theorem): about 15 arcseconds."""
    s = (a_km + b_km + c_km) / 2
    area = math.sqrt(s * (s - a_km) * (s - b_km) * (s - c_km))
    excess = area / R_km ** 2
    return {"sides_km": [a_km, b_km, c_km], "area_km2": round(area, 1), "excess_arcsec": round(math.degrees(excess) * 3600, 2)}


def disk_world(rhos=(0.25, 0.5, 0.75, 0.9, 0.99)) -> dict:
    """Poincaré's disk world: temperature falls toward the rim and every ruler shrinks in proportion, so that a measured
    length element is ds = 2 |dx| / (1 - r^2). The inhabitants find the rim infinitely far, and circles whose
    circumference exceeds pi times their diameter: a hyperbolic geometry, from Euclidean space plus a universal force."""
    rows = []
    for r in rhos:
        radius = 2 * math.atanh(r)
        circ = 2 * math.pi * r * 2 / (1 - r * r)
        rows.append({"r": r, "measured_radius": round(radius, 3), "measured_circumference": round(circ, 3),
                     "ratio_over_pi": round(circ / (2 * radius) / math.pi, 4)})
    return {"rows": rows}


# ---------------------------------------------------------------------------
# Special relativity
# ---------------------------------------------------------------------------
def lorentz(v: float, events) -> list:
    """Coordinates (t', x') of events (t, x) in a frame moving at velocity v (units with c = 1)."""
    g = 1 / math.sqrt(1 - v * v)
    return [(g * (t - v * x), g * (x - v * t)) for t, x in events]


def simultaneity(vs=(0.0, 0.3, 0.6, -0.6)) -> dict:
    """Two lightning strikes, A at x = -1 and B at x = +1, both at t = 0 in the platform frame. In a frame moving at
    v their times are t' = -gamma v x: for v > 0, B happens first. Order flips with the sign of v; for timelike pairs
    it never does."""
    A, B = (0.0, -1.0), (0.0, 1.0)
    C = (2.0, 0.5)                           # a timelike-separated pair: the origin and C
    rows = []
    for v in vs:
        (ta, xa), (tb, xb), (tc, xc) = lorentz(v, [A, B, C])
        rows.append({"v": v, "tA": round(ta, 3), "tB": round(tb, 3), "first": "A" if ta < tb - 1e-12 else (
            "B" if tb < ta - 1e-12 else "together"), "timelike_order_kept": tc > 0})
    return {"rows": rows}


def rietdijk_putnam(event=(0.6, 1.0)) -> dict:
    """Given a spacelike-separated event E = (t, x) with |t| < |x|, the boost v = t / x makes E simultaneous with
    here-now. So E is `present' for an observer passing here now at speed v; if what is present for anyone present for
    me is real, E is real, and by repeating the step, every event is."""
    t, x = event
    v = t / x
    tp, xp = lorentz(v, [event])[0]
    return {"event": list(event), "v": round(v, 4), "t_prime": round(tp, 10), "spacelike": abs(t) < abs(x)}


def reichenbach(epsilons=(0.25, 0.5, 0.75), t1: float = 0.0, t3: float = 2.0) -> dict:
    """A light signal leaves at t1, reflects off a distant mirror and returns at t3. Reichenbach: the time of
    reflection is t2 = t1 + eps (t3 - t1) for any 0 < eps < 1, by convention; Einstein's choice is eps = 1/2.
    Malament (1977): eps = 1/2 is the only simultaneity relation definable from the causal structure."""
    return {"t1": t1, "t3": t3, "rows": [{"eps": e, "t2": t1 + e * (t3 - t1)} for e in epsilons]}


# ---------------------------------------------------------------------------
# The hole argument
# ---------------------------------------------------------------------------
def hole(n: int = 11, bump: float = 0.35, radius: float = 1.0) -> dict:
    """A smooth diffeomorphism of the plane that is the identity outside a disk (the hole) and swirls the inside: the
    grid lines of the deformed model. Outside the hole, and so before it, the two models agree point for point."""
    def phi(p):
        x, y = p
        r = math.hypot(x, y)
        if r >= radius:
            return (x, y)
        s = (1 - (r / radius) ** 2) ** 3            # smooth, vanishing with its derivatives at the boundary
        a = bump * 2 * math.pi * s
        return (x * math.cos(a) - y * math.sin(a), x * math.sin(a) + y * math.cos(a))

    lines = []
    for c in np.linspace(-1.5, 1.5, n):
        lines.append([list(map(float, phi((float(c), float(t))))) for t in np.linspace(-1.5, 1.5, 61)])
        lines.append([list(map(float, phi((float(t), float(c))))) for t in np.linspace(-1.5, 1.5, 61)])
    outside_fixed = all(phi((x, y)) == (x, y) for x in (-1.5, 1.2, 1.4) for y in (-1.5, 1.1))
    return {"lines": lines, "radius": radius, "outside_fixed": outside_fixed}


# ---------------------------------------------------------------------------
# Deutsch's closed timelike curves
# ---------------------------------------------------------------------------
def _ptrace_first(rho4):
    """Trace out the first qubit of a two-qubit density matrix."""
    r = rho4.reshape(2, 2, 2, 2)
    return np.einsum("ijik->jk", r)


def deutsch_fixed_point(U, rho_in, iters: int = 400) -> np.ndarray:
    """Deutsch (1991): the CTC qubit's state rho must equal Tr_CR[U (rho_in (x) rho) U^dagger]. Solve by the linear
    fixed-point equation of the map on 2x2 matrices, choosing the maximum-entropy solution when there are many."""
    basis = [np.array([[1, 0], [0, 0]], complex), np.array([[0, 1], [0, 0]], complex),
             np.array([[0, 0], [1, 0]], complex), np.array([[0, 0], [0, 1]], complex)]

    def M(r):
        out = U @ np.kron(rho_in, r) @ U.conj().T
        return _ptrace_first(out)

    S = np.array([M(b).reshape(-1) for b in basis]).T            # the map as a 4x4 matrix on vec(rho)
    w, V = np.linalg.eig(S)
    fixed = [V[:, i].reshape(2, 2) for i in range(4) if abs(w[i] - 1) < 1e-9]
    cands = []
    for F in fixed:
        F = (F + F.conj().T) / 2
        if abs(np.trace(F)) > 1e-12:
            cands.append(F / np.trace(F))
    if len(fixed) > 1 or not cands:
        # many fixed points: average the map's action over the maximally mixed state (max entropy, Deutsch's choice)
        r = np.eye(2, dtype=complex) / 2
        for _ in range(iters):
            r = 0.5 * (r + M(r))
        return r
    return cands[0]


def ctc() -> dict:
    """Two time-travel stories as circuits. The grandfather paradox: a bit enters the CTC and comes out flipped (a NOT
    on the time-travelling bit); classically there is no consistent history, but Deutsch's rule has one, the 50/50
    mixture. The knowledge paradox: the CTC bit is copied (CNOT) onto a chronology-respecting bit; every value is
    consistent, and nothing fixes which, the problem of the unproven theorem."""
    X = np.array([[0, 1], [1, 0]], complex)
    I2 = np.eye(2, dtype=complex)
    zero = np.array([[1, 0], [0, 0]], complex)
    # grandfather: the CTC qubit (second) is flipped; the CR qubit (first) idle
    U_gf = np.kron(I2, X)
    rho_gf = deutsch_fixed_point(U_gf, zero)
    # classical check: which bit values y satisfy y = NOT y? none
    classical_gf = [y for y in (0, 1) if y == 1 - y]
    # knowledge paradox: CNOT from the CTC qubit (control) onto the CR qubit, then the CR bit goes back in time:
    # SWAP after CNOT so the copied value is what travels back
    CNOT_ctc_ctrl = np.array([[1, 0, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0], [0, 1, 0, 0]], complex)  # control 2nd
    SWAP = np.array([[1, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 1]], complex)
    U_kn = SWAP @ CNOT_ctc_ctrl
    classical_kn = [y for y in (0, 1) if y == (0 ^ y)]
    rho_kn = deutsch_fixed_point(U_kn, zero)
    return {"grandfather": {"classical_consistent": classical_gf,
                            "deutsch": [[round(float(rho_gf[i, j].real), 4) for j in range(2)] for i in range(2)]},
            "knowledge": {"classical_consistent": classical_kn,
                          "deutsch": [[round(float(rho_kn[i, j].real), 4) for j in range(2)] for i in range(2)]}}


# ---------------------------------------------------------------------------
# Barbour's best matching
# ---------------------------------------------------------------------------
def best_matching(n: int = 5, seed: int = 1999, angle: float = 1.1, shift=(2.5, -0.8), wiggle: float = 0.12) -> dict:
    """Barbour and Bertotti's best matching. Two configurations of n bodies, the second rotated and shifted as a whole
    and with a small genuine change. Slide and turn the second over the first to minimize the summed squared
    distances (the Kabsch algorithm): what is left is the intrinsic difference between the two instants, the only
    change a relationalist can recognize. The rotation and shift found are the arbitrary ones put in."""
    rng = np.random.default_rng(seed)
    P = rng.normal(size=(n, 2))
    R = np.array([[math.cos(angle), -math.sin(angle)], [math.sin(angle), math.cos(angle)]])
    change = rng.normal(size=(n, 2)) * wiggle
    Q = (P + change) @ R.T + np.array(shift)
    # Kabsch: centre both, find the rotation that best maps Q onto P
    Pc, Qc = P - P.mean(0), Q - Q.mean(0)
    H = Qc.T @ Pc
    U, _, Vt = np.linalg.svd(H)
    d = np.sign(np.linalg.det(Vt.T @ U.T))
    D = np.diag([1, d])
    Rb = Vt.T @ D @ U.T
    Qm = Qc @ Rb.T + P.mean(0)
    raw = float(np.sqrt(((P - Q) ** 2).sum()))
    resid = float(np.sqrt(((P - Qm) ** 2).sum()))
    found = math.atan2(Rb[1, 0], Rb[0, 0])
    return {"P": P.round(4).tolist(), "Q": Q.round(4).tolist(), "matched": Qm.round(4).tolist(),
            "raw_distance": round(raw, 3), "intrinsic_distance": round(resid, 3),
            "angle_put_in": round(angle, 3), "angle_found": round(-found, 3),
            "true_change": round(float(np.sqrt((change ** 2).sum())), 3)}


# ---------------------------------------------------------------------------
# Galilean boosts and slow clock transport
# ---------------------------------------------------------------------------
def galilean_boost(v: float = 0.6, n: int = 401) -> dict:
    """A Galilean boost x -> x - v t applied to a wiggling path x(t) = 0.6 sin(2.2 t) and to a body at rest. The
    velocity of everything changes by -v; the acceleration of everything is unchanged (checked by finite differences):
    rest is frame-relative, acceleration is not."""
    t = np.linspace(-1.7, 1.7, n)
    dt = t[1] - t[0]
    x = 0.6 * np.sin(2.2 * t)
    xb = x - v * t
    vel, velb = np.gradient(x, dt), np.gradient(xb, dt)
    acc, accb = np.gradient(vel, dt), np.gradient(velb, dt)
    rest = np.zeros_like(t)
    restb = rest - v * t
    return {"v": v, "t": [round(float(a), 4) for a in t[::10]], "path": [round(float(a), 4) for a in x[::10]],
            "path_boosted": [round(float(a), 4) for a in xb[::10]], "rest_boosted": [round(float(a), 4) for a in
                                                                                    restb[::10]],
            "velocity_shift": round(float(np.mean(velb - vel)), 6),
            "max_acceleration_change": float(np.max(np.abs(accb - acc)[2:-2]))}


def clock_transport(L: float = 1.0, speeds=(0.5, 0.1, 0.01, 0.001)) -> dict:
    """Synchronize a distant clock by carrying a second clock there at speed v (c = 1). It lags by the time-dilation
    deficit L/v (1 - sqrt(1 - v^2)), about L v / 2, which vanishes as v -> 0: infinitely slow transport reproduces
    Einstein's synchrony, epsilon = 1/2."""
    rows = []
    for v in speeds:
        lag = L / v * (1 - math.sqrt(1 - v * v))
        rows.append({"v": v, "lag": lag, "approx": L * v / 2, "eps": 0.5 - lag / (2 * L)})
    return {"L": L, "rows": rows}


# ---------------------------------------------------------------------------
# Causal sets: order plus number
# ---------------------------------------------------------------------------
def ordering_fraction(d: float) -> float:
    """Expected fraction of related pairs among points sprinkled in a causal diamond of d-dimensional Minkowski
    spacetime (Myrheim; Meyer): Gamma(d + 1) Gamma(d / 2) / (2 Gamma(3d / 2))."""
    return math.gamma(d + 1) * math.gamma(d / 2) / (2 * math.gamma(3 * d / 2))


def _sprinkle(n: int, d: int, rng) -> np.ndarray:
    """n points uniform in the diamond |x| < 1/2 - |t - 1/2| ... between (0, 0) and (1, 0) in d-dimensional Minkowski."""
    pts = []
    while len(pts) < n:
        t = rng.random()
        x = rng.uniform(-0.5, 0.5, size=d - 1)
        if np.linalg.norm(x) < min(t, 1 - t):
            pts.append(np.concatenate([[t], x]))
    return np.array(pts)


def _related(p: np.ndarray) -> np.ndarray:
    dt = p[None, :, 0] - p[:, None, 0]
    dx = np.linalg.norm(p[None, :, 1:] - p[:, None, 1:], axis=2)
    return dt > dx                                              # R[i, j]: j is in the causal future of i


def causal_set(n: int = 400, dims=(2, 3, 4), n_draw: int = 90, seed: int = 1987) -> dict:
    """Bombelli, Lee, Meyer and Sorkin (1987): sprinkle events at random into a diamond of flat spacetime, keep only
    the causal order, forget the coordinates. The fraction of related pairs, inverted through ordering_fraction,
    recovers the dimension (the Myrheim--Meyer estimator). Also a small 2-d sprinkling and its links (relations not
    implied by transitivity), for drawing."""
    rng = np.random.default_rng(seed)
    rows = []
    for d in dims:
        p = _sprinkle(n, d, rng)
        R = _related(p)
        r = float(R.sum()) / (n * (n - 1) / 2)
        lo, hi = 1.0, 8.0                                         # ordering_fraction decreases in d
        for _ in range(60):
            mid = (lo + hi) / 2
            if ordering_fraction(mid) > r:
                lo = mid
            else:
                hi = mid
        rows.append({"d": d, "fraction": round(r, 4), "theory": round(ordering_fraction(d), 4),
                     "estimate": round((lo + hi) / 2, 2)})
    p = _sprinkle(n_draw, 2, rng)
    R = _related(p)
    Ri = R.astype(int)
    links = [(int(i), int(j)) for i, j in zip(*np.nonzero(R & ((Ri @ Ri) == 0)))]
    return {"n": n, "rows": rows, "points": [[round(float(t), 4), round(float(x), 4)] for t, x in p],
            "links": links, "n_relations": int(R.sum()), "n_links": len(links)}


# ---------------------------------------------------------------------------
# The twins: proper time along worldlines
# ---------------------------------------------------------------------------
def proper_time(path) -> float:
    """Proper time along a polygonal timelike worldline [(t, x), ...] (c = 1)."""
    tau = 0.0
    for (t0, x0), (t1, x1) in zip(path, path[1:]):
        dt, dx = t1 - t0, x1 - x0
        assert dt > abs(dx), "not timelike"
        tau += math.sqrt(dt * dt - dx * dx)
    return tau


def twins(T: float = 10.0, speeds=(0.0, 0.3, 0.6, 0.8, 0.95, 0.99), n_wiggly: int = 200, seed: int = 1905) -> dict:
    """One twin stays home from (0, 0) to (T, 0); the other flies out at speed v and back. Proper time T sqrt(1 - v^2).
    In Minkowski geometry the triangle inequality is reversed: of all timelike worldlines between two events, the
    straight one has the most proper time. Checked on random wiggly worldlines."""
    rows = []
    for v in speeds:
        path = [(0.0, 0.0), (T / 2, v * T / 2), (T, 0.0)]
        rows.append({"v": v, "tau": round(proper_time(path), 4), "formula": round(T * math.sqrt(1 - v * v), 4)})
    rng = np.random.default_rng(seed)
    taus, examples = [], []
    while len(taus) < n_wiggly:
        k = int(rng.integers(3, 9))
        ts = np.sort(rng.uniform(0, T, k - 1))
        ts = np.concatenate([[0.0], ts, [T]])
        xs = [0.0]
        for a, b in zip(ts[:-1], ts[1:]):
            xs.append(xs[-1] + rng.uniform(-0.9, 0.9) * (b - a))
        xs[-1] = 0.0
        path = list(zip(ts.tolist(), xs))
        try:
            tau = proper_time(path)
        except AssertionError:
            continue
        taus.append(tau)
        if len(examples) < 12:
            examples.append([[round(t, 3), round(x, 3)] for t, x in path])
    return {"T": T, "rows": rows, "n_wiggly": len(taus), "max_wiggly": round(max(taus), 4),
            "min_wiggly": round(min(taus), 4), "examples": examples}
