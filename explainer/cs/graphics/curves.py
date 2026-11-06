"""Curves and subdivision surfaces (Part 51): Bezier curves by de Casteljau's construction and in Bernstein form,
subdivision of a cubic, B-splines by the Cox-de Boor recursion, and Catmull-Clark subdivision of a cube.

Sources: Farin, *Curves and Surfaces for CAGD* (5th ed.), ch. 3-8 (de Casteljau, Bernstein, subdivision, B-splines);
de Boor, "On calculating with B-splines" (1972) and Cox (1972) for the recursion; Catmull and Clark, "Recursively
generated B-spline surfaces on arbitrary topological meshes" (1978), with the vertex rule (F + 2R + (n - 3)P) / n;
the limit-position mask (n^2 P + 4 sum e_j + sum f_j) / (n (n + 5)) is from Halstead, Kass and DeRose (SIGGRAPH
1993).  Marschner and Shirley, *Fundamentals of Computer Graphics*, ch. 15.  Points are lists of floats of any
dimension; results are plain lists.
"""

from __future__ import annotations


import numpy as np

# --------------------------------------------------------------------------------------------------- Bezier


def de_casteljau(points, t: float) -> dict:
    """de Casteljau's construction: repeatedly replace the polygon by the points a fraction t along each of its legs.
    Returns ``levels`` (level 0 is the control polygon, the last level a single point) and ``point``, B(t)."""
    level = np.asarray(points, float)
    levels = [level.tolist()]
    while len(level) > 1:
        level = (1 - t) * level[:-1] + t * level[1:]
        levels.append(level.tolist())
    return {"t": float(t), "levels": levels, "point": levels[-1][0]}


def bezier(points, ts) -> list:
    """The Bezier curve at each t, by de Casteljau."""
    return [de_casteljau(points, t)["point"] for t in ts]


def subdivide(points, t: float = 0.5) -> dict:
    """Split a Bezier curve at t into two of the same degree: the left control points are the first point of each
    de Casteljau level, the right ones the last points read backwards.  Left(s) = B(t s), Right(s) = B(t + (1 - t) s)."""
    lv = de_casteljau(points, t)["levels"]
    return {"left": [l[0] for l in lv], "right": [l[-1] for l in lv][::-1]}


# --------------------------------------------------------------------------------------------------- B-splines


def basis(i: int, p: int, t: float, knots) -> float:
    """The Cox-de Boor recursion: N_i,0 = 1 on [k_i, k_i+1); N_i,p = (t - k_i) / (k_i+p - k_i) N_i,p-1
    + (k_i+p+1 - t) / (k_i+p+1 - k_i+1) N_i+1,p-1, with 0/0 = 0.  The last non-empty span is closed on the right so
    a clamped curve reaches its end point."""
    k = knots
    if p == 0:
        if k[i] <= t < k[i + 1]:
            return 1.0
        last = max(j for j in range(len(k) - 1) if k[j] < k[j + 1])
        return 1.0 if (i == last and t == k[i + 1]) else 0.0
    out = 0.0
    if k[i + p] != k[i]:
        out += (t - k[i]) / (k[i + p] - k[i]) * basis(i, p - 1, t, k)
    if k[i + p + 1] != k[i + 1]:
        out += (k[i + p + 1] - t) / (k[i + p + 1] - k[i + 1]) * basis(i + 1, p - 1, t, k)
    return out


def bspline(control, degree: int, knots, ts) -> list:
    """C(t) = sum_i N_i,degree(t) P_i for len(knots) = len(control) + degree + 1; t should lie in
    [knots[degree], knots[-degree - 1]]."""
    P = np.asarray(control, float)
    if len(knots) != len(P) + degree + 1:
        raise ValueError("need len(knots) = len(control) + degree + 1")
    return [(np.array([basis(i, degree, t, knots) for i in range(len(P))]) @ P).tolist() for t in ts]


def uniform_knots(n_control: int, degree: int) -> list[float]:
    """Unclamped uniform knots 0, 1, ..., n + degree; the curve lives on [degree, n]."""
    return [float(i) for i in range(n_control + degree + 1)]


def clamped_knots(n_control: int, degree: int) -> list[float]:
    """Knots repeated degree + 1 times at both ends, so the curve starts and ends on its end control points; the
    curve lives on [0, n - degree]."""
    inner = n_control - degree - 1
    return [0.0] * (degree + 1) + [float(i) for i in range(1, inner + 1)] + [float(inner + 1)] * (degree + 1)


def bspline_continuity(control=((0, 0), (1, 2), (3, 3), (4, 0), (6, -1), (7, 2), (9, 3)), h: float = 0.01) -> list[dict]:
    """At each interior knot of a uniform cubic B-spline, the jump between the left and the right polynomial piece in
    position and first, second and third derivative.  Each side is sampled only strictly inside its own span (four
    points at steps of h) and extrapolated to the knot with stencils that are exact for cubics, so the numbers are
    the true one-sided values up to rounding: C0, C1 and C2 jumps ~1e-10 (the curve is C2), the third derivative
    jumps."""
    knots = uniform_knots(len(control), 3)
    f = lambda ts: np.asarray(bspline(control, 3, knots, ts))

    def one_sided(k, s):
        f1, f2, f3, f4 = f([k + s * m * h for m in (1, 2, 3, 4)])
        f0 = 4 * f1 - 6 * f2 + 4 * f3 - f4                          # cubic extrapolation to the knot
        d1 = s * (-11 * f0 + 18 * f1 - 9 * f2 + 2 * f3) / (6 * h)
        d2 = (2 * f0 - 5 * f1 + 4 * f2 - f3) / (h * h)
        d3 = s * (-f0 + 3 * f1 - 3 * f2 + f3) / h ** 3
        return f0, d1, d2, d3

    rows = []
    for k in knots[4:len(control)]:
        L, R = one_sided(k, -1), one_sided(k, 1)
        rows.append({"knot": k, **{f"jump_c{i}": float(np.linalg.norm(R[i] - L[i])) for i in range(4)},
                     "d2_left": L[2].tolist(), "d2_right": R[2].tolist()})
    return rows


# --------------------------------------------------------------------------------------------------- Catmull-Clark


def cube_mesh(half: float = 1.0):
    """The cube [-half, half]^3: 8 vertices and 6 outward quads."""
    V = [[x, y, z] for x in (-half, half) for y in (-half, half) for z in (-half, half)]
    F = [(0, 1, 3, 2), (4, 6, 7, 5), (0, 4, 5, 1), (2, 3, 7, 6), (0, 2, 6, 4), (1, 5, 7, 3)]
    return [list(map(float, v)) for v in V], [list(f) for f in F]


def _edges(F):
    E = {}
    for fi, f in enumerate(F):
        for a, b in zip(f, f[1:] + f[:1]):
            E.setdefault((min(a, b), max(a, b)), []).append(fi)
    return E


def catmull_clark_step(V, F):
    """One Catmull-Clark step on a closed mesh.  Face point = centroid of the face; edge point = mean of the two
    endpoints and the two adjacent face points; each old vertex P of valence n moves to (F + 2R + (n - 3) P) / n
    (F the mean of adjacent face points, R the mean of incident edge midpoints).  Every face of k sides becomes k
    quads.  New vertex order: moved old vertices (same indices), then edge points, then face points."""
    V = np.asarray(V, float)
    E = _edges(F)
    fp = np.array([V[f].mean(0) for f in F])
    ekeys = list(E)
    eidx = {e: len(V) + i for i, e in enumerate(ekeys)}
    ep = np.array([(V[a] + V[b] + fp[E[(a, b)][0]] + fp[E[(a, b)][1]]) / 4 for a, b in ekeys])
    vf = [[] for _ in V]
    ve = [[] for _ in V]
    for fi, f in enumerate(F):
        for v in f:
            vf[v].append(fi)
    for a, b in ekeys:
        ve[a].append((a, b))
        ve[b].append((a, b))
    newV = np.empty_like(V)
    for v in range(len(V)):
        n = len(ve[v])
        Fm = fp[vf[v]].mean(0)
        Rm = np.mean([(V[a] + V[b]) / 2 for a, b in ve[v]], 0)
        newV[v] = (Fm + 2 * Rm + (n - 3) * V[v]) / n
    base = len(V) + len(ekeys)
    newF = []
    for fi, f in enumerate(F):
        k = len(f)
        for j in range(k):
            a, b, c = f[j - 1], f[j], f[(j + 1) % k]
            newF.append([b, eidx[(min(b, c), max(b, c))], base + fi, eidx[(min(a, b), max(a, b))]])
    return np.vstack([newV, ep, fp]), newF


def limit_position(V, F, v: int) -> list[float]:
    """Where vertex v ends up after infinitely many steps: (n^2 P + 4 sum e_j + sum f_j) / (n (n + 5)) on a quad
    mesh, with e_j its edge neighbours and f_j the vertices diagonally across each adjacent quad."""
    V = np.asarray(V, float)
    nb = {b if a == v else a for a, b in _edges(F) if v in (a, b)}
    diag = []
    for f in F:
        if v in f:
            diag.append(f[(f.index(v) + 2) % 4])
    n = len(nb)
    return ((n * n * V[v] + 4 * V[list(nb)].sum(0) + V[diag].sum(0)) / (n * (n + 5))).tolist()


def catmull_clark(mesh=None, levels: int = 4) -> dict:
    """Subdivide ``mesh`` (vertices, faces; default the cube [-1, 1]^3) ``levels`` times.  Returns ``levels`` (per
    level 0..levels: ``V``, ``E``, ``F``, ``euler`` = V - E + F, ``vertices``, ``faces``, ``corner_radius``, the mean
    distance from the centre of the original vertices, which keep their indices) and ``limit_radius`` (the same,
    from the limit-position mask)."""
    V, F = cube_mesh() if mesh is None else mesh
    centre = np.asarray(V, float).mean(0)
    n0 = len(V)
    lim = np.mean([np.linalg.norm(np.asarray(limit_position(V, F, v)) - centre) for v in range(n0)])
    out = []
    for lv in range(levels + 1):
        if lv:
            V, F = catmull_clark_step(V, F)
        Va = np.asarray(V, float)
        nE = len(_edges(F))
        out.append({"level": lv, "V": len(Va), "E": nE, "F": len(F), "euler": len(Va) - nE + len(F),
                    "vertices": Va.tolist(), "faces": [list(f) for f in F],
                    "corner_radius": float(np.linalg.norm(Va[:n0] - centre, axis=1).mean())})
    return {"levels": out, "limit_radius": float(lim)}
