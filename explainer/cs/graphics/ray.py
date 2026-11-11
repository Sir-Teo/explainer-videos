"""Ray tracing (Part 51): ray-sphere intersection (the quadratic), Moller-Trumbore ray-triangle intersection, bounding
volume hierarchies built with the surface-area heuristic against a median split, and a Whitted (1980) ray tracer with
mirror reflection, Snell refraction, Fresnel-Schlick reflectance and hard shadows from a point light.

Sources: Whitted, "An improved illumination model for shaded display", CACM 1980; Moller and Trumbore, "Fast, minimum
storage ray-triangle intersection", J. Graphics Tools 1997; Schlick, "An inexpensive BRDF model for physically-based
rendering", Eurographics 1994; Pharr, Jakob and Humphreys, *Physically Based Rendering* 4th ed. (PBRT), sections 6.2
(spheres), 6.5 (triangles), 7.3 (BVHs: binned SAH, MacDonald and Booth 1990) and 9.5 (specular reflection and
transmission); Marschner and Shirley, *Fundamentals of Computer Graphics*, chapter 4 (ray tracing).
"""

from __future__ import annotations

import time

import numpy as np
from numba import njit

EPS = 1e-9


# ---------------------------------------------------------------- primitives

def _dot(a, b):
    return np.einsum("...i,...i->...", a, b)


def _normalize(v):
    return v / np.linalg.norm(v, axis=-1, keepdims=True)


def ray_sphere(o, d, center, radius, tmin: float = 1e-6):
    """Nearest hit t > tmin of rays o + t d (arrays (..., 3); d need not be unit) with a sphere, inf on a miss.
    |o + t d - c|^2 = r^2 is the quadratic a t^2 + 2 b t + c = 0 with a = d.d, b = d.(o - c), c = |o - c|^2 - r^2,
    t = (-b -+ sqrt(b^2 - a c)) / a; the smaller root unless it is behind the ray (then we are inside the sphere).
    The roots are taken in the cancellation-free form q = -(b + sign(b) sqrt(disc)), t = q / a and c / q (PBRT 6.2)."""
    o, d = np.asarray(o, float), np.asarray(d, float)
    oc = o - np.asarray(center, float)
    a = _dot(d, d)
    b = _dot(d, oc)
    c = _dot(oc, oc) - radius * radius
    disc = b * b - a * c
    hit = disc >= 0
    sq = np.sqrt(np.where(hit, disc, 0.0))
    q = -(b + np.where(b >= 0, sq, -sq))
    with np.errstate(divide="ignore", invalid="ignore"):
        t1 = q / a
        t2 = np.where(q != 0, c / np.where(q != 0, q, 1.0), t1)
    lo, hi = np.minimum(t1, t2), np.maximum(t1, t2)
    t = np.where(lo > tmin, lo, np.where(hi > tmin, hi, np.inf))
    return np.where(hit, t, np.inf)


def moller_trumbore(o, d, v0, v1, v2, tmin: float = 1e-9):
    """Moller and Trumbore (1997): solve o + t d = (1 - u - v) v0 + u v1 + v v2 by Cramer's rule with scalar triple
    products.  With e1 = v1 - v0, e2 = v2 - v0, s = o - v0, p = d x e2, q = s x e1 and det = e1 . p:
    u = s . p / det, v = d . q / det, t = e2 . q / det.  Everything broadcasts over (..., 3).  Returns (t, u, v, hit),
    t = inf where there is no hit (parallel ray, outside the triangle, or behind the origin)."""
    o, d = np.asarray(o, float), np.asarray(d, float)
    v0, v1, v2 = (np.asarray(x, float) for x in (v0, v1, v2))
    e1, e2 = v1 - v0, v2 - v0
    p = np.cross(d, e2)
    det = _dot(e1, p)
    ok = np.abs(det) > 1e-14
    inv = np.where(ok, 1.0 / np.where(ok, det, 1.0), 0.0)
    s = o - v0
    u = _dot(s, p) * inv
    q = np.cross(s, e1)
    v = _dot(d, q) * inv
    t = _dot(e2, q) * inv
    hit = ok & (u >= 0) & (v >= 0) & (u + v <= 1) & (t > tmin)
    return np.where(hit, t, np.inf), u, v, hit


# ---------------------------------------------------------------- meshes

def terrain(n: int, seed: int = 0, roughness: float = 0.15) -> np.ndarray:
    """A random height field over the unit square made of exactly n triangles (n even): an a x b grid of cells, two
    triangles each, 2ab = n with a, b as close as possible.  Heights are a few random sinusoids plus jitter.
    Returns (n, 3, 3) vertices."""
    if n < 2 or n % 2:
        raise ValueError("terrain needs a positive even triangle count")
    m = n // 2
    a = int(np.sqrt(m))
    while m % a:
        a -= 1
    b = m // a
    rng = np.random.default_rng(seed)
    x = np.linspace(0, 1, b + 1)
    y = np.linspace(0, 1, a + 1)
    X, Y = np.meshgrid(x, y)
    Z = np.zeros_like(X)
    for k in range(6):
        f = rng.uniform(1, 6, 2)
        Z += rng.uniform(0.3, 1) / (k + 1) * np.sin(2 * np.pi * (f[0] * X + f[1] * Y) + rng.uniform(0, 2 * np.pi))
    Z = roughness * Z / np.abs(Z).max() + 0.002 * rng.standard_normal(Z.shape)
    P = np.stack([X, Y, Z], -1)
    p00, p10, p01, p11 = P[:-1, :-1], P[:-1, 1:], P[1:, :-1], P[1:, 1:]
    t1 = np.stack([p00, p10, p11], -2).reshape(-1, 3, 3)
    t2 = np.stack([p00, p11, p01], -2).reshape(-1, 3, 3)
    return np.concatenate([t1, t2])


def icosphere(level: int = 3, radius: float = 1.0) -> np.ndarray:
    """A sphere made by subdividing an icosahedron ``level`` times (20 * 4^level triangles), as (n, 3, 3)."""
    g = (1 + 5 ** 0.5) / 2
    V = [(-1, g, 0), (1, g, 0), (-1, -g, 0), (1, -g, 0), (0, -1, g), (0, 1, g), (0, -1, -g), (0, 1, -g),
         (g, 0, -1), (g, 0, 1), (-g, 0, -1), (-g, 0, 1)]
    F = [(0, 11, 5), (0, 5, 1), (0, 1, 7), (0, 7, 10), (0, 10, 11), (1, 5, 9), (5, 11, 4), (11, 10, 2), (10, 7, 6),
         (7, 1, 8), (3, 9, 4), (3, 4, 2), (3, 2, 6), (3, 6, 8), (3, 8, 9), (4, 9, 5), (2, 4, 11), (6, 2, 10),
         (8, 6, 7), (9, 8, 1)]
    T = _normalize(np.array(V, float))[np.array(F)]
    for _ in range(level):
        a, b, c = T[:, 0], T[:, 1], T[:, 2]
        ab, bc, ca = _normalize(a + b), _normalize(b + c), _normalize(c + a)
        T = np.concatenate([np.stack(x, 1) for x in ((a, ab, ca), (ab, b, bc), (ca, bc, c), (ab, bc, ca))])
    return radius * T


# ---------------------------------------------------------------- BVH (numba)

@njit(cache=True)
def _area(lo, hi):
    dx, dy, dz = hi[0] - lo[0], hi[1] - lo[1], hi[2] - lo[2]
    if dx < 0:
        return 0.0
    return 2.0 * (dx * dy + dy * dz + dz * dx)


@njit(cache=True)
def _build(bmin, bmax, cen, sah, max_leaf, nbins):
    """Top-down build.  Nodes are stored in arrays; a node with count > 0 is a leaf over idx[start:start+count], an
    interior node's children are left[i] and left[i] + 1, split along axis[i].  SAH: cost of a split =
    C_trav + (A_L N_L + A_R N_R) / A * C_isect with C_trav = C_isect = 1 (MacDonald and Booth 1990; PBRT 7.3.2),
    evaluated at nbins - 1 planes per axis over the centroid bounds; a leaf is made when it is cheaper (N C_isect) and
    small enough.  Median: split at the median centroid along the widest centroid axis."""
    n = cen.shape[0]
    idx = np.arange(n)
    cap = 2 * n + 1
    nlo = np.empty((cap, 3))
    nhi = np.empty((cap, 3))
    left = np.zeros(cap, np.int64)
    start = np.zeros(cap, np.int64)
    count = np.zeros(cap, np.int64)
    axis = np.zeros(cap, np.int64)
    depth = np.zeros(cap, np.int64)
    stack = np.empty((128, 3), np.int64)
    sp = 0
    stack[0, 0], stack[0, 1], stack[0, 2] = 0, 0, n
    sp = 1
    nn = 1
    blo = np.empty((nbins, 3))
    bhi = np.empty((nbins, 3))
    bcnt = np.zeros(nbins, np.int64)
    rarea = np.empty(nbins)
    rcnt = np.zeros(nbins, np.int64)
    tmp_lo = np.empty(3)
    tmp_hi = np.empty(3)
    binof = np.empty(n, np.int64)
    while sp > 0:
        sp -= 1
        node, s, e = stack[sp, 0], stack[sp, 1], stack[sp, 2]
        m = e - s
        lo = np.full(3, np.inf)
        hi = np.full(3, -np.inf)
        clo = np.full(3, np.inf)
        chi = np.full(3, -np.inf)
        for k in range(s, e):
            j = idx[k]
            for a in range(3):
                lo[a] = min(lo[a], bmin[j, a])
                hi[a] = max(hi[a], bmax[j, a])
                clo[a] = min(clo[a], cen[j, a])
                chi[a] = max(chi[a], cen[j, a])
        nlo[node] = lo
        nhi[node] = hi
        ext = chi - clo
        best_axis = 0
        for a in range(1, 3):
            if ext[a] > ext[best_axis]:
                best_axis = a
        leaf = m <= 1 or ext[best_axis] <= 0.0
        mid = -1
        if not leaf and sah:
            area = _area(lo, hi)
            best_cost = np.inf
            best_plane = -1
            best_axis = -1
            for a in range(3):
                if ext[a] <= 0.0:
                    continue
                for b in range(nbins):
                    bcnt[b] = 0
                    for c in range(3):
                        blo[b, c] = np.inf
                        bhi[b, c] = -np.inf
                for k in range(s, e):
                    j = idx[k]
                    b = int(nbins * (cen[j, a] - clo[a]) / ext[a])
                    if b >= nbins:
                        b = nbins - 1
                    bcnt[b] += 1
                    for c in range(3):
                        blo[b, c] = min(blo[b, c], bmin[j, c])
                        bhi[b, c] = max(bhi[b, c], bmax[j, c])
                # sweep from the right: area and count of bins b..nbins-1
                for c in range(3):
                    tmp_lo[c] = np.inf
                    tmp_hi[c] = -np.inf
                cnt = 0
                for b in range(nbins - 1, 0, -1):
                    cnt += bcnt[b]
                    for c in range(3):
                        tmp_lo[c] = min(tmp_lo[c], blo[b, c])
                        tmp_hi[c] = max(tmp_hi[c], bhi[b, c])
                    rarea[b] = _area(tmp_lo, tmp_hi)
                    rcnt[b] = cnt
                for c in range(3):
                    tmp_lo[c] = np.inf
                    tmp_hi[c] = -np.inf
                cnt = 0
                for b in range(nbins - 1):  # plane after bin b
                    cnt += bcnt[b]
                    for c in range(3):
                        tmp_lo[c] = min(tmp_lo[c], blo[b, c])
                        tmp_hi[c] = max(tmp_hi[c], bhi[b, c])
                    nr = rcnt[b + 1]
                    if cnt == 0 or nr == 0:
                        continue
                    cost = 1.0 + (cnt * _area(tmp_lo, tmp_hi) + nr * rarea[b + 1]) / area
                    if cost < best_cost:
                        best_cost, best_plane, best_axis = cost, b, a
            if best_axis < 0 or (m <= max_leaf and m <= best_cost):
                leaf = True
            else:
                a = best_axis
                for k in range(s, e):
                    j = idx[k]
                    b = int(nbins * (cen[j, a] - clo[a]) / ext[a])
                    binof[k] = nbins - 1 if b >= nbins else b
                i, r = s, e - 1
                while i <= r:  # partition in place: bins <= best_plane to the left
                    if binof[i] <= best_plane:
                        i += 1
                    else:
                        binof[i], binof[r] = binof[r], binof[i]
                        idx[i], idx[r] = idx[r], idx[i]
                        r -= 1
                mid = i
        elif not leaf:
            if m <= max_leaf:
                leaf = True
            else:
                a = best_axis
                keys = np.empty(m)
                for k in range(m):
                    keys[k] = cen[idx[s + k], a]
                order = np.argsort(keys)
                sub = idx[s:e].copy()
                for k in range(m):
                    idx[s + k] = sub[order[k]]
                mid = s + m // 2
        if leaf:
            start[node] = s
            count[node] = m
        else:
            axis[node] = best_axis
            left[node] = nn
            depth[nn] = depth[node] + 1
            depth[nn + 1] = depth[node] + 1
            stack[sp, 0], stack[sp, 1], stack[sp, 2] = nn, s, mid
            stack[sp + 1, 0], stack[sp + 1, 1], stack[sp + 1, 2] = nn + 1, mid, e
            sp += 2
            nn += 2
    return nlo[:nn], nhi[:nn], left[:nn], start[:nn], count[:nn], axis[:nn], depth[:nn], idx


@njit(cache=True)
def _mt(ox, oy, oz, dx, dy, dz, tri):
    """Scalar Moller-Trumbore for the numba traversal; returns t or inf."""
    e1x, e1y, e1z = tri[1, 0] - tri[0, 0], tri[1, 1] - tri[0, 1], tri[1, 2] - tri[0, 2]
    e2x, e2y, e2z = tri[2, 0] - tri[0, 0], tri[2, 1] - tri[0, 1], tri[2, 2] - tri[0, 2]
    px, py, pz = dy * e2z - dz * e2y, dz * e2x - dx * e2z, dx * e2y - dy * e2x
    det = e1x * px + e1y * py + e1z * pz
    if abs(det) < 1e-14:
        return np.inf
    inv = 1.0 / det
    sx, sy, sz = ox - tri[0, 0], oy - tri[0, 1], oz - tri[0, 2]
    u = (sx * px + sy * py + sz * pz) * inv
    if u < 0.0 or u > 1.0:
        return np.inf
    qx, qy, qz = sy * e1z - sz * e1y, sz * e1x - sx * e1z, sx * e1y - sy * e1x
    v = (dx * qx + dy * qy + dz * qz) * inv
    if v < 0.0 or u + v > 1.0:
        return np.inf
    t = (e2x * qx + e2y * qy + e2z * qz) * inv
    return t if t > 1e-9 else np.inf


@njit(cache=True)
def _traverse(O, D, tris, nlo, nhi, left, start, count, axis, idx):
    """Closest-hit traversal with a stack: a node is visited when it is popped and its box tested (slab test against
    the current closest t); a leaf tests its triangles; an interior node pushes the far child first so the near child
    (by the ray direction's sign on the split axis) is visited first."""
    nr = O.shape[0]
    T = np.full(nr, np.inf)
    hit = np.full(nr, -1, np.int64)
    visits = np.zeros(nr, np.int64)
    tests = np.zeros(nr, np.int64)
    stack = np.empty(128, np.int64)
    for r in range(nr):
        ox, oy, oz = O[r, 0], O[r, 1], O[r, 2]
        dx, dy, dz = D[r, 0], D[r, 1], D[r, 2]
        ix = 1.0 / dx if dx != 0 else np.inf
        iy = 1.0 / dy if dy != 0 else np.inf
        iz = 1.0 / dz if dz != 0 else np.inf
        best = np.inf
        sp = 1
        stack[0] = 0
        while sp > 0:
            sp -= 1
            nd = stack[sp]
            visits[r] += 1
            t0, t1 = 0.0, best
            for a in range(3):
                o_ = ox if a == 0 else (oy if a == 1 else oz)
                i_ = ix if a == 0 else (iy if a == 1 else iz)
                ta = (nlo[nd, a] - o_) * i_
                tb = (nhi[nd, a] - o_) * i_
                if ta != ta:  # 0 * inf: the ray lies in the slab's plane
                    ta = -np.inf
                if tb != tb:
                    tb = np.inf
                if ta > tb:
                    ta, tb = tb, ta
                t0 = max(t0, ta)
                t1 = min(t1, tb)
            if t0 > t1:
                continue
            if count[nd] > 0:
                for k in range(start[nd], start[nd] + count[nd]):
                    j = idx[k]
                    tests[r] += 1
                    t = _mt(ox, oy, oz, dx, dy, dz, tris[j])
                    if t < best:
                        best = t
                        hit[r] = j
            else:
                a = axis[nd]
                da = dx if a == 0 else (dy if a == 1 else dz)
                l = left[nd]
                if da > 0:
                    stack[sp] = l + 1
                    stack[sp + 1] = l
                else:
                    stack[sp] = l
                    stack[sp + 1] = l + 1
                sp += 2
        T[r] = best
    return T, hit, visits, tests


@njit(cache=True)
def _brute(O, D, tris):
    nr = O.shape[0]
    T = np.full(nr, np.inf)
    hit = np.full(nr, -1, np.int64)
    for r in range(nr):
        for j in range(tris.shape[0]):
            t = _mt(O[r, 0], O[r, 1], O[r, 2], D[r, 0], D[r, 1], D[r, 2], tris[j])
            if t < T[r]:
                T[r] = t
                hit[r] = j
    return T, hit


def build_bvh(triangles, method: str = "sah", max_leaf: int = 4, nbins: int = 16) -> dict:
    """Build a BVH over (n, 3, 3) triangles; returns the node arrays plus build time and shape statistics."""
    tris = np.ascontiguousarray(triangles, float)
    if tris.ndim != 3 or tris.shape[1:] != (3, 3) or not len(tris) or not np.isfinite(tris).all():
        raise ValueError("BVH needs a nonempty array of finite (3, 3) triangles")
    if method not in ("sah", "median") or max_leaf < 1 or nbins < 2:
        raise ValueError("invalid BVH method, leaf size, or bin count")
    t0 = time.perf_counter()
    out = _build(tris.min(1), tris.max(1), tris.mean(1), method == "sah", max_leaf, nbins)
    build_s = time.perf_counter() - t0
    nlo, nhi, left, start, count, axis, depth, idx = out
    leaves = count > 0
    return {"tris": tris, "nlo": nlo, "nhi": nhi, "left": left, "start": start, "count": count, "axis": axis,
            "idx": idx, "build_s": build_s, "nodes": int(len(count)), "leaves": int(leaves.sum()),
            "max_depth": int(depth.max()), "mean_leaf_size": float(count[leaves].mean())}


def traverse(tree: dict, origins, dirs):
    """Closest hits of many rays: (t, triangle index or -1, node visits, triangle tests), arrays per ray."""
    O = np.ascontiguousarray(origins, float)
    D = np.ascontiguousarray(dirs, float)
    return _traverse(O, D, tree["tris"], tree["nlo"], tree["nhi"], tree["left"], tree["start"], tree["count"],
                     tree["axis"], tree["idx"])


def brute_force(triangles, origins, dirs):
    """Closest hits by testing every triangle (n tests per ray): (t, triangle index or -1)."""
    return _brute(np.ascontiguousarray(origins, float), np.ascontiguousarray(dirs, float),
                  np.ascontiguousarray(triangles, float))


def camera_rays(n_side: int = 64, eye=(0.5, -0.3, 0.7), look=(0.5, 0.55, 0.0), fov_deg: float = 50.0):
    """An n_side x n_side grid of perspective rays from ``eye`` toward ``look`` (z up)."""
    eye, look = np.asarray(eye, float), np.asarray(look, float)
    f = _normalize(look - eye)
    r = _normalize(np.cross(f, [0, 0, 1.0]))
    u = np.cross(r, f)
    s = np.tan(np.radians(fov_deg) / 2) * np.linspace(-1, 1, n_side)
    X, Y = np.meshgrid(s, s)
    D = _normalize(f + X[..., None] * r + Y[..., None] * u).reshape(-1, 3)
    return np.broadcast_to(eye, D.shape).copy(), D


def bvh(triangles, method: str = "sah", origins=None, dirs=None, max_leaf: int = 4) -> dict:
    """Build a BVH by ``method`` ("sah" or "median") and trace many rays (default: a 64 x 64 camera grid looking at
    the unit square).  Returns build_s, nodes, leaves, max_depth, mean_leaf_size, mean/max node_visits and
    tri_tests per ray, the hit fraction, and the per-ray lists node_visits and tri_tests."""
    if origins is None:
        origins, dirs = camera_rays()
    tree = build_bvh(triangles, method, max_leaf)
    t0 = time.perf_counter()
    T, hit, visits, tests = traverse(tree, origins, dirs)
    trace_s = time.perf_counter() - t0
    return {"method": method, "n": int(len(triangles)), "build_s": tree["build_s"], "trace_s": trace_s,
            "nodes": tree["nodes"], "leaves": tree["leaves"], "max_depth": tree["max_depth"],
            "mean_leaf_size": tree["mean_leaf_size"], "rays": int(len(T)), "hit_fraction": float((hit >= 0).mean()),
            "mean_node_visits": float(visits.mean()), "mean_tri_tests": float(tests.mean()),
            "max_tri_tests": int(tests.max()), "node_visits": visits.tolist(), "tri_tests": tests.tolist()}


def bvh_experiment(ns=(100, 1000, 10_000, 100_000), mesh: str = "terrain", n_side: int = 64, check_rays: int = 256,
                   seed: int = 0) -> list[dict]:
    """For meshes of n triangles (a random terrain, or with mesh="sphere" the icosphere closest in size), the mean
    triangle tests per ray for brute force (n), the median-split BVH and the SAH BVH, with node visits, build times
    and log2 n for comparison.  ``agree`` is the fraction of ``check_rays`` rays whose closest hit by the SAH BVH
    equals brute force's."""
    _warm()
    O, D = camera_rays(n_side)
    rows = []
    for n in ns:
        if mesh == "sphere":
            level = int(round(np.log(n / 20) / np.log(4)))
            tris = icosphere(max(level, 0), 0.4) + np.array([0.5, 0.5, 0.0])
        else:
            tris = terrain(n, seed)
        med = bvh(tris, "median", O, D)
        sah = bvh(tris, "sah", O, D)
        k = min(check_rays, len(O))
        sel = np.linspace(0, len(O) - 1, k).astype(int)
        tb, hb = brute_force(tris, O[sel], D[sel])
        ts, hs, _, _ = traverse(build_bvh(tris, "sah"), O[sel], D[sel])
        same = (hb == hs) | (np.isclose(tb, ts) & np.isfinite(tb)) | (~np.isfinite(tb) & ~np.isfinite(ts))
        agree = float(np.mean(same))
        rows.append({"n": int(len(tris)), "log2_n": float(np.log2(len(tris))), "brute_tests": int(len(tris)),
                     "median_tests": med["mean_tri_tests"], "sah_tests": sah["mean_tri_tests"],
                     "median_visits": med["mean_node_visits"], "sah_visits": sah["mean_node_visits"],
                     "median_build_s": med["build_s"], "sah_build_s": sah["build_s"],
                     "median_trace_s": med["trace_s"], "sah_trace_s": sah["trace_s"],
                     "median_depth": med["max_depth"], "sah_depth": sah["max_depth"],
                     "hit_fraction": sah["hit_fraction"], "agree": agree})
    return rows


def _warm():
    """Compile the numba kernels on a tiny mesh so build times exclude compilation."""
    tris = terrain(8)
    O, D = camera_rays(2)
    for m in ("sah", "median"):
        traverse(build_bvh(tris, m), O, D)
    brute_force(tris, O, D)


# ---------------------------------------------------------------- Whitted ray tracer

def reflect(d, n):
    """Mirror direction of incoming d about normal n: r = d - 2 (d.n) n."""
    return d - 2 * _dot(d, n)[..., None] * n


def refract(d, n, eta):
    """Snell's law in vector form (PBRT 9.5.2; Marschner and Shirley 4.8): d unit and incoming, n unit on the incident
    side (d.n < 0), eta = n1 / n2.  With cos_i = -d.n and sin_t^2 = eta^2 (1 - cos_i^2),
    t = eta d + (eta cos_i - sqrt(1 - sin_t^2)) n.  Returns (t, cos_t, tir) where tir marks total internal
    reflection (sin_t^2 > 1)."""
    cos_i = -_dot(d, n)
    sin2_t = eta * eta * (1 - cos_i * cos_i)
    tir = sin2_t > 1
    cos_t = np.sqrt(np.clip(1 - sin2_t, 0, None))
    t = eta[..., None] * d + (eta * cos_i - cos_t)[..., None] * n if np.ndim(eta) else \
        eta * d + (eta * cos_i - cos_t)[..., None] * n
    return t, cos_t, tir


def schlick(cos, n1, n2):
    """Fresnel-Schlick reflectance R = R0 + (1 - R0)(1 - cos)^5, R0 = ((n1 - n2)/(n1 + n2))^2 (Schlick 1994).
    ``cos`` is the cosine on the less dense side (the incident angle entering glass, the transmitted angle leaving
    it)."""
    r0 = ((n1 - n2) / (n1 + n2)) ** 2
    return r0 + (1 - r0) * (1 - cos) ** 5


def fresnel_dielectric(cos_i, n1, n2):
    """Exact Fresnel reflectance for unpolarized light (the mean of the s and p terms), for comparison with Schlick."""
    cos_i = np.asarray(cos_i, float)
    sin_t = n1 / n2 * np.sqrt(np.clip(1 - cos_i ** 2, 0, None))
    tir = sin_t >= 1
    cos_t = np.sqrt(np.clip(1 - sin_t ** 2, 0, None))
    rs = ((n1 * cos_i - n2 * cos_t) / (n1 * cos_i + n2 * cos_t)) ** 2
    rp = ((n1 * cos_t - n2 * cos_i) / (n1 * cos_t + n2 * cos_i)) ** 2
    return np.where(tir, 1.0, (rs + rp) / 2)


WHITTED_SCENE = {
    "spheres": [  # center, radius, kind, color
        ((-1.25, 1.0, 1.6), 1.0, "mirror", (0.9, 0.9, 0.92)),
        ((0.35, 0.75, -0.2), 0.75, "glass", (1.0, 1.0, 1.0)),
        ((1.85, 0.6, 1.1), 0.6, "diffuse", (0.85, 0.25, 0.15)),
    ],
    "floor": ((0.92, 0.92, 0.88), (0.12, 0.14, 0.2)),  # checker colors, unit squares on the plane y = 0
    "light": (-3.0, 6.0, -3.5),
    "light_intensity": 1.0,
    "ambient": 0.08,
    "eye": (0.0, 1.7, -5.2),
    "look": (0.1, 0.7, 0.6),
    "fov_deg": 48.0,
    "ior": 1.5,
}


def _sky(d):
    s = np.clip(d[:, 1], 0, 1)[:, None]
    return (1 - s) * np.array([0.75, 0.82, 0.95]) + s * np.array([0.25, 0.4, 0.75])


def whitted(W: int = 160, H: int = 120, max_depth: int = 6, min_weight: float = 0.01,
            scene: dict | None = None) -> dict:
    """A Whitted (1980) ray tracer on a checkerboard floor, a mirror sphere, a glass sphere (Snell refraction, reflected
    and transmitted in the proportions R and 1 - R of Fresnel-Schlick, total internal reflection), a diffuse sphere
    with a Blinn-Phong highlight and one point light with hard shadows.  The ray tree is traced breadth first: every
    pass intersects all live rays with the scene at once (numpy).  Rays stop at ``max_depth`` bounces or when their
    weight falls below ``min_weight``.  Returns the linear H x W x 3 image (``image``), ray counts by kind
    (primary, shadow, reflection, refraction, total), ``tir`` (refraction rays lost to total internal reflection) and
    the time in seconds."""
    sc = scene or WHITTED_SCENE
    t_start = time.perf_counter()
    eye, look = np.asarray(sc["eye"], float), np.asarray(sc["look"], float)
    f = _normalize(look - eye)
    r = _normalize(np.cross([0, 1.0, 0], f))
    u = np.cross(f, r)
    th = np.tan(np.radians(sc["fov_deg"]) / 2)
    xs = ((np.arange(W) + 0.5) / W * 2 - 1) * th * W / H
    ys = (1 - (np.arange(H) + 0.5) / H * 2) * th
    X, Y = np.meshgrid(xs, ys)
    D = _normalize(f + X[..., None] * r + Y[..., None] * u).reshape(-1, 3)
    O = np.broadcast_to(eye, D.shape).copy()
    Wt = np.ones_like(D)
    pix = np.arange(W * H)
    depth = np.zeros(W * H, int)
    inside = np.zeros(W * H, bool)  # ray travels inside the glass
    img = np.zeros((W * H, 3))
    counts = {"primary": W * H, "shadow": 0, "reflection": 0, "refraction": 0}
    tir_count = 0
    C = np.array([s[0] for s in sc["spheres"]], float)
    R = np.array([s[1] for s in sc["spheres"]], float)
    kinds = [s[2] for s in sc["spheres"]]
    cols = np.array([s[3] for s in sc["spheres"]], float)
    L = np.asarray(sc["light"], float)
    ior = sc["ior"]

    def nearest(O, D):
        ts = [ray_sphere(O, D, C[k], R[k]) for k in range(len(R))]
        with np.errstate(divide="ignore", invalid="ignore"):
            tp = np.where(D[:, 1] != 0, -O[:, 1] / D[:, 1], np.inf)
        ts.append(np.where(tp > 1e-6, tp, np.inf))
        ts = np.stack(ts, 1)
        k = ts.argmin(1)
        return ts[np.arange(len(k)), k], k

    while len(D):
        t, k = nearest(O, D)
        miss = ~np.isfinite(t)
        np.add.at(img, pix[miss], Wt[miss] * _sky(D[miss]))
        keep = ~miss
        O, D, Wt, pix, depth, inside, t, k = (a[keep] for a in (O, D, Wt, pix, depth, inside, t, k))
        P = O + t[:, None] * D
        nsph = len(R)
        N = np.where((k < nsph)[:, None], (P - C[np.minimum(k, nsph - 1)]) / R[np.minimum(k, nsph - 1)][:, None],
                     np.array([0, 1.0, 0]))
        kind = np.array([kinds[j] if j < nsph else "floor" for j in k]) if len(k) else np.array([], str)
        new = []
        # diffuse surfaces: local shading with a shadow ray
        dif = (kind == "diffuse") | (kind == "floor")
        if dif.any():
            p, n, d, w = P[dif], N[dif], D[dif], Wt[dif]
            n = np.where((_dot(n, d) > 0)[:, None], -n, n)
            fl = kind[dif] == "floor"
            chk = (np.floor(p[:, 0]) + np.floor(p[:, 2])) % 2 == 0
            col = np.where(fl[:, None], np.where(chk[:, None], sc["floor"][0], sc["floor"][1]),
                           cols[np.minimum(k[dif], nsph - 1)])
            tol = L - p
            dist = np.linalg.norm(tol, axis=1)
            ldir = tol / dist[:, None]
            so = p + 1e-6 * n
            ts, _ = nearest(so, ldir)
            counts["shadow"] += int(len(p))
            lit = (ts > dist) & (_dot(n, ldir) > 0)
            ndl = np.clip(_dot(n, ldir), 0, None)
            hv = _normalize(ldir - d)
            spec = np.where(fl, 0.0, 0.5 * np.clip(_dot(n, hv), 0, None) ** 60)
            shade = sc["ambient"] * col + lit[:, None] * sc["light_intensity"] * (col * ndl[:, None] + spec[:, None])
            np.add.at(img, pix[dif], w * shade)
        # mirror: one reflection ray
        mir = kind == "mirror"
        if mir.any():
            n = N[mir]
            rd = reflect(D[mir], n)
            new.append((P[mir] + 1e-6 * n, rd, Wt[mir] * cols[k[mir]], pix[mir], depth[mir] + 1, inside[mir],
                        "reflection"))
        # glass: reflection and refraction weighted by Fresnel-Schlick
        gl = kind == "glass"
        if gl.any():
            d, n, p, w, ins = D[gl], N[gl], P[gl], Wt[gl], inside[gl]
            n = np.where(ins[:, None], -n, n)  # normal on the incident side
            n1 = np.where(ins, ior, 1.0)
            n2 = np.where(ins, 1.0, ior)
            tdir, cos_t, tir = refract(d, n, n1 / n2)
            cos_i = -_dot(d, n)
            Rf = np.where(tir, 1.0, schlick(np.where(ins, cos_t, cos_i), n1, n2))
            tir_count += int(tir.sum())
            new.append((p + 1e-6 * n, reflect(d, n), w * Rf[:, None], pix[gl], depth[gl] + 1, ins, "reflection"))
            ok = ~tir
            new.append((p[ok] - 1e-6 * n[ok], _normalize(tdir[ok]), w[ok] * (1 - Rf[ok])[:, None], pix[gl][ok],
                        depth[gl][ok] + 1, ~ins[ok], "refraction"))
        parts = []
        for (o2, d2, w2, p2, dp2, in2, kd) in new:
            live = (dp2 <= max_depth) & (w2.max(1) >= min_weight)
            counts[kd] += int(live.sum())
            parts.append((o2[live], d2[live], w2[live], p2[live], dp2[live], in2[live]))
        if not parts:
            break
        O, D, Wt, pix, depth, inside = (np.concatenate([p_[i] for p_ in parts]) for i in range(6))
    counts["total"] = sum(counts.values())
    return {"image": img.reshape(H, W, 3), "counts": counts, "tir": tir_count, "W": W, "H": H,
            "seconds": time.perf_counter() - t_start}
