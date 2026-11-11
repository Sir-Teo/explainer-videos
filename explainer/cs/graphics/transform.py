"""Transforms and projection for Part 51 of *Computer Science, Built*: 4 x 4 homogeneous matrices (translation becomes
linear), composition order, the OpenGL perspective matrix and the frustum squashed into the NDC cube, the depth
nonlinearity and z-fighting, Euler angles and gimbal lock, quaternions and slerp.

Conventions follow OpenGL and Marschner and Shirley, *Fundamentals of Computer Graphics* (ch. 7): column vectors,
right-handed eye space with the camera at the origin looking down -z, matrices applied right to left.  The
perspective matrix is ``gluPerspective``'s; NDC is the cube [-1, 1]^3 and window depth is (z_ndc + 1) / 2.
Quaternions are (w, x, y, z) with the Hamilton product; slerp is Shoemake's (SIGGRAPH 1985), taking the shorter arc
by flipping the sign of one endpoint when their dot product is negative (q and -q are the same rotation).  Euler
angles are yaw, pitch, roll about Z, Y, X: R = Rz(yaw) Ry(pitch) Rx(roll).

Matrix builders return numpy arrays (they are building blocks); the demo functions return plain dicts and lists of
floats for a compute script to cache.
"""

from __future__ import annotations

import math

import numpy as np

# --------------------------------------------------------------------------------------------------- matrices


def translate(tx: float, ty: float, tz: float) -> np.ndarray:
    """The 4 x 4 translation: linear in homogeneous coordinates because the point's w = 1 multiplies the last column."""
    M = np.eye(4)
    M[:3, 3] = (tx, ty, tz)
    return M


def scale(sx: float, sy: float | None = None, sz: float | None = None) -> np.ndarray:
    sy = sx if sy is None else sy
    sz = sx if sz is None else sz
    return np.diag([sx, sy, sz, 1.0])


def _rot(axis: int, deg: float) -> np.ndarray:
    c, s = math.cos(math.radians(deg)), math.sin(math.radians(deg))
    i, j = [(1, 2), (2, 0), (0, 1)][axis]
    M = np.eye(4)
    M[i, i], M[i, j], M[j, i], M[j, j] = c, -s, s, c
    return M


def rotate_x(deg: float) -> np.ndarray:
    return _rot(0, deg)


def rotate_y(deg: float) -> np.ndarray:
    return _rot(1, deg)


def rotate_z(deg: float) -> np.ndarray:
    return _rot(2, deg)


def compose(*matrices) -> np.ndarray:
    """compose(A, B, C) = A @ B @ C, which applies C first, then B, then A (right to left)."""
    M = np.eye(4)
    for A in matrices:
        M = M @ np.asarray(A, float)
    return M


def apply(M, points) -> np.ndarray:
    """Apply a 4 x 4 matrix to 3D points (rows), with w = 1 and a homogeneous divide at the end."""
    P = np.atleast_2d(np.asarray(points, float))
    H = np.c_[P, np.ones(len(P))] @ np.asarray(M, float).T
    return H[:, :3] / H[:, 3:4]


def apply_h(M, points) -> np.ndarray:
    """Apply a 4 x 4 matrix to 3D points with w = 1 and return the homogeneous (clip) coordinates, undivided."""
    P = np.atleast_2d(np.asarray(points, float))
    return np.c_[P, np.ones(len(P))] @ np.asarray(M, float).T


def composition_order_demo() -> dict:
    """The unit square's corners moved by T(2, 0, 0) R_z(90) (rotate, then translate) against R_z(90) T(2, 0, 0)
    (translate, then rotate about the origin): the two orders land in different places."""
    sq = [(0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0)]
    T, R = translate(2, 0, 0), rotate_z(90)
    return {"square": [list(map(float, p)) for p in sq],
            "rotate_then_translate": apply(compose(T, R), sq).round(12).tolist(),
            "translate_then_rotate": apply(compose(R, T), sq).round(12).tolist()}


# --------------------------------------------------------------------------------------------------- projection


def perspective(fovy_deg: float, aspect: float, near: float, far: float) -> np.ndarray:
    """OpenGL's perspective matrix (gluPerspective).  By similar triangles a point at eye depth d = -z lands at
    y_screen = f y / d with f = cot(fovy / 2); putting d into w defers that division to the hardware.  The z row is the
    unique A z + B with z_ndc = -1 at d = near and +1 at d = far:  A = (f + n) / (n - f),  B = 2 f n / (n - f)."""
    f = 1.0 / math.tan(math.radians(fovy_deg) / 2)
    return np.array([[f / aspect, 0, 0, 0],
                     [0, f, 0, 0],
                     [0, 0, (far + near) / (near - far), 2 * far * near / (near - far)],
                     [0, 0, -1, 0]], float)


def project(P, points) -> np.ndarray:
    """Eye-space points to NDC: multiply by the projection, then divide by w."""
    return apply(P, points)


def frustum_corners(fovy_deg: float, aspect: float, near: float, far: float) -> np.ndarray:
    """The eight eye-space corners, near face then far face, each counter-clockwise from bottom-left."""
    t = math.tan(math.radians(fovy_deg) / 2)
    out = []
    for d in (near, far):
        h, w = d * t, d * t * aspect
        out += [(-w, -h, -d), (w, -h, -d), (w, h, -d), (-w, h, -d)]
    return np.array(out, float)


BOX_EDGES = [(0, 1), (1, 2), (2, 3), (3, 0), (4, 5), (5, 6), (6, 7), (7, 4), (0, 4), (1, 5), (2, 6), (3, 7)]


def frustum_to_cube(fovy_deg: float = 60.0, aspect: float = 4 / 3, near: float = 1.0, far: float = 4.0,
                    ts=(0.0, 0.2, 0.4, 0.6, 0.8, 1.0)) -> dict:
    """The frustum folding into the NDC cube.  The frames apply M(t) = (1 - t) I + t P and divide by w, a projective
    map at every t (w = 1 - t + t d > 0), so straight edges stay straight and flat faces stay flat while the far face
    shrinks and the near face grows: at t = 0 the frustum, at t = 1 the cube with every coordinate +-1.
    Returns ``corners_eye`` and ``corners_ndc`` (8 x 3), ``edges`` (12 index pairs), ``frames`` [{t, points}] and
    ``matrix``."""
    P = perspective(fovy_deg, aspect, near, far)
    C = frustum_corners(fovy_deg, aspect, near, far)
    frames = [{"t": float(t), "points": apply((1 - t) * np.eye(4) + t * P, C).tolist()} for t in ts]
    return {"fovy_deg": fovy_deg, "aspect": aspect, "near": near, "far": far, "corners_eye": C.tolist(),
            "corners_ndc": apply(P, C).tolist(), "edges": [list(e) for e in BOX_EDGES], "frames": frames,
            "matrix": P.tolist()}


# --------------------------------------------------------------------------------------------------- depth


def ndc_depth(d, near: float, far: float):
    """z_ndc for eye distance d (z = -d): (f + n) / (f - n) - 2 f n / ((f - n) d), affine in 1/d."""
    d = np.asarray(d, float)
    return (far + near) / (far - near) - 2 * far * near / ((far - near) * d)


def window_depth(d, near: float, far: float):
    """Window depth in [0, 1]: (z_ndc + 1) / 2 = f (d - n) / ((f - n) d)."""
    return (ndc_depth(d, near, far) + 1) / 2


def resolvable(d: float, near: float, far: float, bits: int = 24, iters: int = 200) -> float:
    """The smallest eye-distance gap in front of d that a ``bits``-bit fixed-point depth buffer can tell apart from d:
    the Delta with window_depth(d) - window_depth(d - Delta) = one step, 1 / (2^bits - 1).  Found by bisection on the
    depth mapping itself (it is monotone)."""
    q = 1.0 / (2 ** bits - 1)
    wd = float(window_depth(d, near, far))
    lo, hi = 0.0, d                          # window_depth(d - Delta) -> -inf as Delta -> d
    for _ in range(iters):
        mid = (lo + hi) / 2
        if wd - float(window_depth(d - mid, near, far)) < q:
            lo = mid
        else:
            hi = mid
    return hi


def resolvable_formula(d: float, near: float, far: float, bits: int = 24) -> dict:
    """The same gap in closed form, and to first order from the derivative d(window)/dd = f n / ((f - n) d^2):
    Delta ~ step / derivative = d^2 (f - n) / (f n (2^bits - 1)).  Exact: with k = (f - n) / (f n (2^bits - 1)),
    1 / (d - Delta) = 1 / d + k, so Delta = d^2 k / (1 + d k)."""
    k = (far - near) / (far * near * (2 ** bits - 1))
    return {"exact": d * d * k / (1 + d * k), "derivative": d * d * k}


def depth_precision(near: float = 0.1, far: float = 1000.0, distances=(1, 10, 100, 1000), bits: int = 24) -> list[dict]:
    """For each eye distance: ``ndc`` and ``window`` depth, and the resolvable gap by search (``resolvable``), in
    closed form (``exact``) and from the derivative (``derivative``)."""
    rows = []
    for d in distances:
        f = resolvable_formula(d, near, far, bits)
        rows.append({"near": near, "far": far, "bits": bits, "distance": float(d),
                     "ndc": float(ndc_depth(d, near, far)), "window": float(window_depth(d, near, far)) + 0.0,
                     "resolvable": resolvable(d, near, far, bits), "exact": f["exact"], "derivative": f["derivative"]})
    return rows


def depth_table(nears=(0.01, 0.1, 1.0), far: float = 1000.0, distances=(1, 10, 100, 1000), bits: int = 24) -> list[dict]:
    """``depth_precision`` rows for every near plane: pushing near out is what buys precision."""
    return [r for n in nears for r in depth_precision(n, far, distances, bits)]


def depth_curve(near: float = 0.1, far: float = 1000.0, n: int = 200) -> dict:
    """Window depth against eye distance on a log grid (for a plot: most of [0, 1] is spent just past near)."""
    d = np.geomspace(near, far, n)
    return {"near": near, "far": far, "distance": d.tolist(), "window": window_depth(d, near, far).tolist()}


def z_fighting(near: float, bits: int, far: float = 1000.0, distance: float = 50.0, gap: float = 0.01,
               W: int = 160, H: int = 120, tilt: float = 2.0) -> dict:
    """Two parallel planes ``gap`` apart, the nearer at eye distance ``distance`` +- ``tilt`` across the screen
    (d = distance + tilt x_ndc), drawn farther first, then nearer with GL_LESS against a ``bits``-bit fixed-point depth
    buffer (round to nearest).  A pixel 'flips' when the farther plane survives: the two depths round to the same
    integer, so draw order, not distance, decided.  Returns the ``flipped`` count and ``share``, and the ``mask``
    (H x W bool, an image)."""
    x = (np.arange(W) + 0.5) / W * 2 - 1
    d1 = np.broadcast_to(distance + tilt * x, (H, W))
    d2 = d1 + gap
    s = 2 ** bits - 1
    q1 = np.floor(window_depth(d1, near, far) * s + 0.5)
    q2 = np.floor(window_depth(d2, near, far) * s + 0.5)
    mask = ~(q1 < q2)
    return {"near": near, "far": far, "bits": bits, "distance": distance, "gap": gap, "pixels": W * H,
            "flipped": int(mask.sum()), "share": float(mask.mean()), "mask": mask}


def z_fighting_table(nears=(0.01, 1.0), bits=(16, 24), **kw) -> list[dict]:
    """z_fighting for every (near, bits), without the masks."""
    return [{k: v for k, v in z_fighting(n, b, **kw).items() if k != "mask"} for n in nears for b in bits]


# --------------------------------------------------------------------------------------------------- rotations


def euler_matrix(yaw: float, pitch: float, roll: float) -> np.ndarray:
    """3 x 3 rotation for Z-Y-X Euler angles in degrees: Rz(yaw) Ry(pitch) Rx(roll)."""
    return (rotate_z(yaw) @ rotate_y(pitch) @ rotate_x(roll))[:3, :3]


def rotation_angle(R) -> float:
    """The angle (radians) of a rotation matrix: cos theta = (trace - 1) / 2."""
    c = (np.trace(np.asarray(R)[:3, :3]) - 1) / 2
    return math.acos(max(-1.0, min(1.0, c)))


def _unskew(S) -> np.ndarray:
    return np.array([S[2, 1] - S[1, 2], S[0, 2] - S[2, 0], S[1, 0] - S[0, 1]]) / 2


def euler_jacobian(yaw: float, pitch: float, roll: float, h: float = 1e-6) -> np.ndarray:
    """The 3 x 3 Jacobian of the Euler map at (yaw, pitch, roll): column k is the world angular velocity produced by
    a unit rate (rad/s) of angle k, the axial vector of (dR / d angle_k) R^T, by central differences."""
    R = euler_matrix(yaw, pitch, roll)
    a = np.array([yaw, pitch, roll], float)
    hd = math.degrees(h)
    cols = []
    for k in range(3):
        e = np.zeros(3)
        e[k] = hd
        dR = (euler_matrix(*(a + e)) - euler_matrix(*(a - e))) / (2 * h)
        cols.append(_unskew(dR @ R.T))
    return np.array(cols).T


def gimbal_lock(pitches=(0, 45, 89, 90), yaw: float = 30.0, roll: float = 20.0) -> list[dict]:
    """Singular values of the Euler Jacobian as pitch climbs (closed form 1, sqrt(1 + sin p), sqrt(1 - sin p)): at
    pitch 90 the yaw and roll axes align, one singular value is 0 and the rank falls from 3 to 2."""
    rows = []
    for p in pitches:
        sv = np.linalg.svd(euler_jacobian(yaw, p, roll), compute_uv=False)
        rows.append({"pitch": float(p), "singular_values": sv.tolist(), "rank": int((sv > 1e-6).sum())})
    return rows


def quat_from_axis_angle(axis, deg: float) -> np.ndarray:
    """q = (cos(theta / 2), sin(theta / 2) n) for the unit axis n."""
    n = np.asarray(axis, float)
    n = n / np.linalg.norm(n)
    h = math.radians(deg) / 2
    return np.r_[math.cos(h), math.sin(h) * n]


def quat_mul(a, b) -> np.ndarray:
    """The Hamilton product a b (apply b, then a)."""
    w1, x1, y1, z1 = a
    w2, x2, y2, z2 = b
    return np.array([w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2,
                     w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2,
                     w1 * y2 - x1 * z2 + y1 * w2 + z1 * x2,
                     w1 * z2 + x1 * y2 - y1 * x2 + z1 * w2])


def quat_conj(q) -> np.ndarray:
    return np.array([q[0], -q[1], -q[2], -q[3]], float)


def quat_to_matrix(q) -> np.ndarray:
    """3 x 3 rotation of a unit quaternion (Shoemake 1985)."""
    w, x, y, z = np.asarray(q, float) / np.linalg.norm(q)
    return np.array([[1 - 2 * (y * y + z * z), 2 * (x * y - w * z), 2 * (x * z + w * y)],
                     [2 * (x * y + w * z), 1 - 2 * (x * x + z * z), 2 * (y * z - w * x)],
                     [2 * (x * z - w * y), 2 * (y * z + w * x), 1 - 2 * (x * x + y * y)]])


def quat_rotate(q, v) -> np.ndarray:
    """v' = q (0, v) q*."""
    return quat_mul(quat_mul(q, np.r_[0.0, np.asarray(v, float)]), quat_conj(q))[1:]


def quat_from_euler(yaw: float, pitch: float, roll: float) -> np.ndarray:
    return quat_mul(quat_mul(quat_from_axis_angle((0, 0, 1), yaw), quat_from_axis_angle((0, 1, 0), pitch)),
                    quat_from_axis_angle((1, 0, 0), roll))


def slerp(a, b, t: float) -> np.ndarray:
    """Shoemake's slerp: sin((1 - t) theta) / sin theta a + sin(t theta) / sin theta b, with cos theta = a . b, after
    flipping b when a . b < 0 so the path takes the shorter arc; normalized lerp when the ends nearly coincide."""
    a = np.asarray(a, float) / np.linalg.norm(a)
    b = np.asarray(b, float) / np.linalg.norm(b)
    c = float(a @ b)
    if c < 0:
        b, c = -b, -c
    if c > 0.9999995:
        q = (1 - t) * a + t * b
        return q / np.linalg.norm(q)
    th = math.acos(c)
    return (math.sin((1 - t) * th) * a + math.sin(t * th) * b) / math.sin(th)


def slerp_vs_euler(a=(0.0, 0.0, 0.0), b=(150.0, 80.0, -100.0), steps: int = 40) -> dict:
    """Interpolate between Euler orientations a and b (degrees, Z-Y-X) two ways: linearly in the three angles, and by
    slerp between their quaternions.  Returns, per method (``euler``, ``slerp``): ``per_step_deg`` (angle swept in
    each of ``steps`` steps; slerp's is constant), ``total_deg`` (summed), and ``path`` (the image of (1, 0, 0), as
    steps + 1 points on the unit sphere); and ``geodesic_deg``, the angle of R_b R_a^T."""
    a, b = np.asarray(a, float), np.asarray(b, float)
    ts = np.linspace(0, 1, steps + 1)
    qa, qb = quat_from_euler(*a), quat_from_euler(*b)
    Rs = {"euler": [euler_matrix(*((1 - t) * a + t * b)) for t in ts],
          "slerp": [quat_to_matrix(slerp(qa, qb, t)) for t in ts]}
    out = {"a": a.tolist(), "b": b.tolist(), "steps": steps,
           "geodesic_deg": math.degrees(rotation_angle(euler_matrix(*b) @ euler_matrix(*a).T))}
    for k, R in Rs.items():
        per = [math.degrees(rotation_angle(R[i + 1] @ R[i].T)) for i in range(steps)]
        out[k] = {"per_step_deg": per, "total_deg": sum(per), "path": [(Ri @ [1.0, 0, 0]).tolist() for Ri in R]}
    return out
