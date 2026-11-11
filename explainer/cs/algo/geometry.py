"""Computational geometry for Part 22 of *Computer Science, Built*: exact predicates, convex hulls, the sweep line,
polygon triangulation and guards, Fortune's Voronoi sweep, Delaunay triangulations (incremental with flips, and by
Lawson flips), Seidel's linear programming, kd-trees, vertical decompositions, a navigable small-world graph, ham
sandwiches and configuration-space planning.

Points are pairs (or numpy rows).  Every algorithm that the part measures counts its own work: orientation tests,
events, flips, triangles created, nodes visited.  Integer inputs make the integer predicates exact; ``orient_exact``
and ``incircle_exact`` decide finite binary64 inputs with rationals. The conservative filter falls back on
underflow/overflow; this teaching fallback differs from Shewchuk's floating-point expansions.
"""

from __future__ import annotations

import heapq
import math
import random
from numbers import Integral
from fractions import Fraction

import numpy as np

# --------------------------------------------------------------------------------------------------- predicates

EPS = 2.0 ** -53
CCW_ERRBOUND = (3.0 + 16.0 * EPS) * EPS          # Shewchuk's ccwerrboundA


def orient_float(p, q, r) -> float:
    """Twice the signed area of pqr in floating point: > 0 when r is left of p -> q."""
    return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])


def _sgn(x) -> int:
    return int(x > 0) - int(x < 0)


def _scalar(x):
    return x.item() if isinstance(x, np.generic) else x


def _fraction(x):
    x = _scalar(x)
    if isinstance(x, Integral):
        return Fraction(int(x))
    if not math.isfinite(x):
        raise ValueError("coordinates must be finite")
    return Fraction(x)


def _points(pts):
    points = [tuple(_scalar(x) for x in p) for p in pts]
    if any(not isinstance(x, Integral) and not math.isfinite(x) for p in points for x in p):
        raise ValueError("coordinates must be finite")
    return points


def orient_exact(p, q, r) -> int:
    """The true sign of the orientation determinant, with every float read as the rational it is."""
    F = _fraction
    px, py, qx, qy, rx, ry = (F(v) for v in (p[0], p[1], q[0], q[1], r[0], r[1]))
    return _sgn((qx - px) * (ry - py) - (qy - py) * (rx - px))


def orient_adaptive(p, q, r):
    """Conservative binary64 filter; exact fallback outside the normal finite arithmetic domain.

    Returns (sign, whether exact arithmetic ran). Nonfinite coordinates are rejected.
    This rational fallback is not Shewchuk's expansion implementation.
    """
    values = [_scalar(v) for point in (p, q, r) for v in point]
    if any(isinstance(v, Integral) for v in values):
        return orient_exact(p, q, r), True
    values = [float(v) for v in values]
    if not all(math.isfinite(v) for v in values):
        raise ValueError("coordinates must be finite")
    px, py, qx, qy, rx, ry = values
    dx, dy, ex, ey = qx-px, qy-py, rx-px, ry-py
    normal = np.finfo(float).tiny
    safe = lambda v: math.isfinite(v) and (v == 0.0 or abs(v) >= normal)
    if all(safe(v) for v in (dx, dy, ex, ey)):
        a, b = dx*ey, dy*ex
        products_safe = all(safe(v) and (v != 0.0 or u == 0.0 or w == 0.0)
                            for v, u, w in ((a, dx, ey), (b, dy, ex)))
        det, magnitude = a-b, abs(a)+abs(b)
        bound = CCW_ERRBOUND*magnitude
        if products_safe and all(safe(v) for v in (det, magnitude, bound)) and bound > 0.0 and abs(det) > bound:
            return _sgn(det), False
    return orient_exact(p, q, r), True


def orient_int(p, q, r) -> int:
    """Exact integer-coordinate predicate, promoting NumPy scalars before arithmetic."""
    values = [_scalar(x) for point in (p, q, r) for x in point]
    if not all(isinstance(x, Integral) for x in values):
        raise TypeError("orient_int requires integer coordinates")
    px, py, qx, qy, rx, ry = map(int, values)
    return _sgn((qx-px)*(ry-py)-(qy-py)*(rx-px))


def incircle_float(a, b, c, d) -> float:
    """> 0 when d is inside the circle through a, b, c (counter-clockwise): the 3 x 3 lifted determinant."""
    adx, ady = a[0] - d[0], a[1] - d[1]
    bdx, bdy = b[0] - d[0], b[1] - d[1]
    cdx, cdy = c[0] - d[0], c[1] - d[1]
    ad, bd, cd = adx * adx + ady * ady, bdx * bdx + bdy * bdy, cdx * cdx + cdy * cdy
    return adx * (bdy * cd - bd * cdy) - ady * (bdx * cd - bd * cdx) + ad * (bdx * cdy - bdy * cdx)


def incircle_exact(a, b, c, d) -> int:
    F = _fraction
    return _sgn(incircle_float(*[(F(p[0]), F(p[1])) for p in (a, b, c, d)]))


def kettner_grid(p, q, r, n: int = 256):
    """Kettner et al. (2008): move p over an n x n grid of adjacent floats and ask orient(p, q, r) in floating point
    and exactly.  Returns (float signs, exact signs) as n x n int arrays (row j = j ulps up, column i = i ulps right)."""
    xs = [p[0]]
    ys = [p[1]]
    for _ in range(n - 1):
        xs.append(math.nextafter(xs[-1], math.inf))
        ys.append(math.nextafter(ys[-1], math.inf))
    X, Y = np.meshgrid(np.array(xs), np.array(ys))
    fl = np.sign((q[0] - X) * (r[1] - Y) - (q[1] - Y) * (r[0] - X)).astype(int)
    ex = np.zeros_like(fl)
    for j, y in enumerate(ys):
        for i, x in enumerate(xs):
            ex[j, i] = orient_exact((x, y), q, r)
    return fl, ex


# ------------------------------------------------------------------------------------------------ convex hulls

class Counter:
    """Counts orientation/determinant evaluations (n) and sorting-comparator calls (cmp).

    Quickhull counts each raw determinant evaluated while selecting a farthest
    point. An orientation evaluated inside a sorting comparator counts in both
    categories. Other arithmetic, hashing, selection and tie comparisons are
    outside this deliberately limited work metric.
    """

    def __init__(self):
        self.n = 0
        self.cmp = 0

    def orient(self, p, q, r):
        self.n += 1
        return orient_int(p, q, r) if all(isinstance(_scalar(x), Integral) for point in (p,q,r) for x in point) else orient_adaptive(p,q,r)[0]


def _counted_sort(P, key, ctr):
    """Sort with a counted comparison, so the hulls' totals include the sorting the lower bound says they need."""
    import functools

    def cmp(a, b):
        ctr.cmp += 1
        ka, kb = key(a), key(b)
        return (ka > kb) - (ka < kb)
    return sorted(P, key=functools.cmp_to_key(cmp))


def monotone_chain(pts, ctr: Counter | None = None):
    """Andrew's monotone chain (1979): sort, then a lower and an upper hull.  Counter-clockwise, no collinear points."""
    ctr = ctr or Counter()
    P = _counted_sort(set(_points(pts)), lambda p: p, ctr)
    if len(P) <= 2:
        return P
    lo, up = [], []
    for p in P:
        while len(lo) >= 2 and ctr.orient(lo[-2], lo[-1], p) <= 0:
            lo.pop()
        lo.append(p)
    for p in reversed(P):
        while len(up) >= 2 and ctr.orient(up[-2], up[-1], p) <= 0:
            up.pop()
        up.append(p)
    return lo[:-1] + up[:-1]


def jarvis(pts, ctr: Counter | None = None):
    """Gift wrapping (Jarvis 1973): O(nh) orientation tests."""
    ctr = ctr or Counter()
    P = list(dict.fromkeys(_points(pts)))
    if len(P) <= 2:
        return P
    hull = []
    a = min(P)
    while True:
        hull.append(a)
        b = P[0] if P[0] != a else P[1]
        for c in P:
            if c == a or c == b:
                continue
            o = ctr.orient(a, b, c)
            if o < 0 or (o == 0 and _d2(a, c) > _d2(a, b)):
                b = c
        a = b
        if a == hull[0]:
            break
    return hull


def _d2(a, b):
    return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2


def graham(pts, ctr: Counter | None = None):
    """Graham's scan (1972): sort by angle around the lowest point, then one stack pass."""
    ctr = ctr or Counter()
    P = list(set(_points(pts)))
    if len(P) <= 2:
        return sorted(P)
    o = min(P, key=lambda p: (p[1], p[0]))
    import functools
    def angular(a, b):
        ctr.cmp += 1
        turn = ctr.orient(o, a, b)
        return -turn if turn else _sgn(_d2(o, a)-_d2(o, b))
    rest = sorted((p for p in P if p != o), key=functools.cmp_to_key(angular))
    st = [o]
    for p in rest:
        while len(st) >= 2 and ctr.orient(st[-2], st[-1], p) <= 0:
            st.pop()
        st.append(p)
    return st


def quickhull(pts, ctr: Counter | None = None):
    ctr = ctr or Counter()
    P = list(dict.fromkeys(_points(pts)))
    if len(P) <= 2:
        return P
    a, b = min(P), max(P)

    def hull(u, v, S):
        """Points of S lie strictly right of u -> v; returns the hull chain strictly between u and v."""
        if not S:
            return []
        # Equal-distance points share a supporting line. Choose its extreme
        # endpoint, rather than an arbitrary interior point in input order.
        far = min(S, key=lambda p: ((v[0] - u[0]) * (p[1] - u[1]) - (v[1] - u[1]) * (p[0] - u[0]), p))
        ctr.n += len(S)
        s1 = [p for p in S if ctr.orient(u, far, p) < 0]
        s2 = [p for p in S if ctr.orient(far, v, p) < 0]
        return hull(u, far, s1) + [far] + hull(far, v, s2)
    right = [p for p in P if ctr.orient(a, b, p) < 0]
    left = [p for p in P if ctr.orient(a, b, p) > 0]
    lower = hull(a, b, right)            # a -> b along the bottom, counter-clockwise
    upper = hull(b, a, left)             # b -> a along the top
    return [a] + lower + [b] + upper


def _turn(p, q, r):
    return orient_int(p, q, r) if all(isinstance(_scalar(x), Integral) for point in (p,q,r) for x in point) else orient_adaptive(p,q,r)[0]


def _binary_tangent(hull, p, ctr):
    """Binary search the right tangent of a strictly convex CCW polygon from outside."""
    n = len(hull)
    if n <= 2:
        if n == 1:
            return 0
        o = ctr.orient(p,hull[0],hull[1])
        return 1 if o < 0 or o == 0 and _d2(p,hull[1]) > _d2(p,hull[0]) else 0
    def turn(i,j):
        return ctr.orient(p,hull[i%n],hull[j%n])
    if turn(1,0) <= 0 and turn(n-1,0) <= 0:
        return 0
    a,b = 0,n
    for _ in range(n.bit_length()+3):
        c = (a+b)//2
        down = turn(c+1,c) <= 0
        if down and turn(c-1,c) <= 0:
            return c%n
        up_a = turn(a+1,a) > 0
        if up_a:
            if down or turn(a,c) > 0:
                b = c
            else:
                a = c
        else:
            if not down or turn(a,c) >= 0:
                a = c
            else:
                b = c
    raise AssertionError(("tangent search did not converge",p,hull,a,b))


def _tangent(hull, p, ctr):
    """Resolve collinear tangent endpoints by the farther endpoint, including two-point groups."""
    i = _binary_tangent(hull,p,ctr)
    for j in ((i-1)%len(hull),(i+1)%len(hull)):
        if ctr.orient(p,hull[i],hull[j]) == 0 and _d2(p,hull[j]) > _d2(p,hull[i]):
            i = j
    return i


def chan(pts, ctr: Counter | None = None):
    """Chan (1996): guess h by squaring; hull groups with monotone chain, then wrap them with binary-search
    tangents.  O(n log h) orientation tests.  Returns (hull, the guesses tried)."""
    ctr = ctr or Counter()
    P = list(dict.fromkeys(_points(pts)))
    n = len(P)
    if n <= 3:
        return monotone_chain(P, ctr), [n]
    tried = []
    t = 1
    while True:
        m = min(2 ** (2 ** t), n)
        tried.append(m)
        groups = [monotone_chain(P[i:i + m], ctr) for i in range(0, n, m)]
        positions = [{point:i for i,point in enumerate(g)} for g in groups]
        start = min(P)
        hull = [start]
        ok = False
        for _ in range(m):
            p = hull[-1]
            best = None
            for g, pos in zip(groups, positions):
                i = pos.get(p)
                q = g[_tangent(g, p, ctr)] if i is None else g[(i + 1) % len(g)]
                if q == p:
                    continue
                if best is None:
                    best = q
                    continue
                o = ctr.orient(p, best, q)
                if o < 0 or (o == 0 and _d2(p, q) > _d2(p, best)):
                    best = q
            if best is None or best == start:
                ok = True
                break
            hull.append(best)
        if ok:
            return hull, tried
        t += 1


# ---------------------------------------------------------------------------------------------- the sweep line

def _seg_x_cross(s1, s2):
    """The intersection point of two segments if they properly cross, else None."""
    (x1, y1), (x2, y2) = s1
    (x3, y3), (x4, y4) = s2
    d = (x2 - x1) * (y4 - y3) - (y2 - y1) * (x4 - x3)
    if d == 0:
        return None
    t = ((x3 - x1) * (y4 - y3) - (y3 - y1) * (x4 - x3)) / d
    u = ((x3 - x1) * (y2 - y1) - (y3 - y1) * (x2 - x1)) / d
    if 0 < t < 1 and 0 < u < 1:
        return (x1 + t * (x2 - x1), y1 + t * (y2 - y1))
    return None


def brute_intersections(segs):
    out = []
    for i in range(len(segs)):
        for j in range(i + 1, len(segs)):
            p = _seg_x_cross(segs[i], segs[j])
            if p is not None:
                out.append((i, j, p))
    return out


def bentley_ottmann(segs, log: bool = False):
    """Bentley and Ottmann (1979): a vertical line sweeps left to right; the status holds the segments it crosses,
    ordered by height; only neighbours in the status are ever tested.  Segments are ((x1, y1), (x2, y2)) with x1 < x2,
    in general position.  Returns (intersections as (i, j, point), events processed, pair tests, optional log)."""
    segs = [tuple(sorted(s)) for s in segs]
    ev = []
    for i, (a, b) in enumerate(segs):
        heapq.heappush(ev, (a[0], 0, i, -1))
        heapq.heappush(ev, (b[0], 2, i, -1))
    status: list[int] = []
    found = {}
    tests = 0
    events = 0
    trace = []

    def y_at(i, x):
        (x1, y1), (x2, y2) = segs[i]
        return y1 + (y2 - y1) * (x - x1) / (x2 - x1)

    def check(i, j, x):
        nonlocal tests
        tests += 1
        key = (min(i, j), max(i, j))
        if key in found:
            return
        p = _seg_x_cross(segs[i], segs[j])
        if p is not None and p[0] > x - 1e-12:
            found[key] = p
            heapq.heappush(ev, (p[0], 1, key[0], key[1]))
    while ev:
        x, kind, i, j = heapq.heappop(ev)
        events += 1
        if kind == 0:
            y = segs[i][0][1]
            k = 0
            while k < len(status) and y_at(status[k], x) < y:
                k += 1
            status.insert(k, i)
            if k > 0:
                check(status[k - 1], i, x)
            if k + 1 < len(status):
                check(i, status[k + 1], x)
        elif kind == 2:
            k = status.index(i)
            status.pop(k)
            if 0 < k < len(status):
                check(status[k - 1], status[k], x)
        else:
            a, b = status.index(i), status.index(j)
            lo, hi = min(a, b), max(a, b)
            status[lo], status[hi] = status[hi], status[lo]
            if lo > 0:
                check(status[lo - 1], status[lo], x)
            if hi + 1 < len(status):
                check(status[hi], status[hi + 1], x)
        if log:
            trace.append({"x": x, "kind": ["left end", "crossing", "right end"][kind], "seg": i, "other": j,
                          "status": list(status), "found": len(found)})
    out = [(i, j, p) for (i, j), p in sorted(found.items())]
    return out, events, tests, trace


# ----------------------------------------------------------------------------- polygons: ears and three colours

def polygon_area2(poly):
    return sum(poly[i][0] * poly[(i + 1) % len(poly)][1] - poly[(i + 1) % len(poly)][0] * poly[i][1]
               for i in range(len(poly)))


def _in_tri(p, a, b, c):
    return orient_int(a, b, p) >= 0 and orient_int(b, c, p) >= 0 and orient_int(c, a, p) >= 0


def ear_clip(poly):
    """Triangulate a simple counter-clockwise polygon (integer vertices) by cutting ears (Meisters 1975).
    Returns (triangles as vertex-index triples, tests made)."""
    if len(poly) < 3:
        return [], 0
    idx = list(range(len(poly)))
    tris = []
    tests = 0
    while len(idx) > 3:
        m = len(idx)
        for k in range(m):
            i, j, l = idx[k - 1], idx[k], idx[(k + 1) % m]
            a, b, c = poly[i], poly[j], poly[l]
            tests += 1
            if orient_int(a, b, c) <= 0:
                continue
            ok = True
            for o in idx:
                if o in (i, j, l):
                    continue
                tests += 1
                if _in_tri(poly[o], a, b, c):
                    ok = False
                    break
            if ok:
                tris.append((i, j, l))
                idx.pop(k)
                break
        else:
            raise ValueError("no ear: the polygon is not simple and counter-clockwise")
    tris.append(tuple(idx))
    return tris, tests


def fisk_colouring(n, tris):
    """Fisk (1978): the triangulation's dual is a tree, so a walk through it three-colours the vertices.  Returns the
    colour of each vertex (0, 1, 2)."""
    col = [-1] * n
    edge_tri = {}
    for t, (a, b, c) in enumerate(tris):
        for u, v in ((a, b), (b, c), (c, a)):
            edge_tri.setdefault((min(u, v), max(u, v)), []).append(t)
    a, b, c = tris[0]
    col[a], col[b], col[c] = 0, 1, 2
    seen = {0}
    stack = [0]
    while stack:
        t = stack.pop()
        a, b, c = tris[t]
        for u, v in ((a, b), (b, c), (c, a)):
            for s in edge_tri[(min(u, v), max(u, v))]:
                if s in seen:
                    continue
                seen.add(s)
                w = next(x for x in tris[s] if x not in (u, v))
                col[w] = 3 - col[u] - col[v]
                stack.append(s)
    return col


def comb(k: int, tooth: int = 4, gap: int = 2, depth: int = 12):
    """Chvátal's comb with k teeth, counter-clockwise: 3k + 2 vertices, and every tooth's tip needs its own guard."""
    W = k * (tooth + gap) - gap
    P = [(0, 0), (W, 0)]
    for i in reversed(range(k)):
        x0 = i * (tooth + gap)
        P += [(x0 + tooth, 2), (x0 + tooth // 2, depth), (x0, 2)]
    return P


def star_polygon(n: int, seed: int = 1, r0: int = 400, r1: int = 1000):
    """A random simple polygon: n integer points at sorted angles around the origin with random radii."""
    rng = random.Random(seed)
    angs = sorted(rng.uniform(0, 2 * math.pi) for _ in range(n))
    rs = [rng.uniform(r0, r1) for _ in angs]
    P = [(round(r * math.cos(a)), round(r * math.sin(a))) for r, a in zip(rs, angs)]
    out = []
    for p in P:
        if not out or p != out[-1]:
            out.append(p)
    return out


# --------------------------------------------------------------------------------- Delaunay, incrementally

class Delaunay:
    """Randomized incremental Delaunay triangulation with Lawson's flips (Guibas, Knuth and Sharir 1992), over integer
    points, so that every predicate is exact.  A huge enclosing triangle starts it; the walk locates each point.
    Counts triangles created and flips."""

    def __init__(self, pts):
        values = _points(pts)
        if any(len(p) != 2 or not all(isinstance(x, Integral) for x in p) for p in values):
            raise TypeError("Delaunay requires integer coordinate pairs")
        self.P = [tuple(map(int,p)) for p in values]
        if len(set(self.P)) != len(self.P):
            raise ValueError("Delaunay requires distinct points")
        self._inserted = set()
        n = len(self.P)
        # Integer noncollinear triples have area determinant at least one.
        # Their circumcenters/radii are bounded by a constant times (bound+1)^3;
        # these artificial vertices also lie outside all original circumcircles.
        bound = max((abs(x) for p in self.P for x in p), default=0)
        M = 256*(bound+1)**3
        self.P += [(-3 * M, -3 * M), (3 * M, 0), (0, 3 * M)]
        self.S = (n, n + 1, n + 2)
        self.E: dict[tuple[int, int], int] = {}
        self.created = 0
        self.flips = 0
        self.walk = 0
        self._last = self.S
        self._add(*self.S)

    def _add(self, a, b, c):
        self.E[(a, b)] = c
        self.E[(b, c)] = a
        self.E[(c, a)] = b
        self.created += 1
        self._last = (a, b, c)

    def _del(self, a, b, c):
        for e in ((a, b), (b, c), (c, a)):
            self.E.pop(e, None)

    def _incircle(self, a, b, c, d):
        P = self.P
        return _sgn(incircle_float(P[a], P[b], P[c], P[d]))

    def locate(self, p):
        a, b, c = self._last
        if (a, b) not in self.E:
            a, b = next(iter(self.E))
            c = self.E[(a, b)]
        P = self.P
        while True:
            self.walk += 1
            for u, v in ((a, b), (b, c), (c, a)):
                if orient_int(P[u], P[v], p) < 0:
                    w = self.E[(v, u)]
                    a, b, c = v, u, w
                    break
            else:
                return a, b, c

    def insert(self, i):
        if not isinstance(i, Integral) or not 0 <= i < self.S[0] or i in self._inserted:
            raise ValueError("insert a valid input index exactly once")
        self._inserted.add(i)
        a, b, c = self.locate(self.P[i])
        self._del(a, b, c)
        self._add(a, b, i)
        self._add(b, c, i)
        self._add(c, a, i)
        self._legalize(i, a, b)
        self._legalize(i, b, c)
        self._legalize(i, c, a)

    def _legalize(self, p, a, b):
        pending = [(a,b)]
        while pending:
            a,b = pending.pop()
            d = self.E.get((b,a))
            if d is None:
                continue
            if self._incircle(a,b,p,d) > 0:
                self._del(a,b,p)
                self._del(b,a,d)
                self._add(a,d,p)
                self._add(d,b,p)
                self.flips += 1
                pending.extend(((d,b),(a,d)))

    def triangles(self):
        """The triangles not touching the enclosing triangle, each as a sorted triple."""
        out = set()
        for (a, b), c in self.E.items():
            if max(a, b, c) < self.S[0]:
                out.add(tuple(sorted((a, b, c))))
        return sorted(out)


def delaunay(pts, order=None, seed: int = 0):
    """Insert the points in a random order (or the given one).  Returns the Delaunay object."""
    n = len(pts)
    if order is None:
        order = list(range(n))
        random.Random(seed).shuffle(order)
    order = list(order)
    if len(order) != n or set(order) != set(range(n)):
        raise ValueError("order must be a permutation of all input indices")
    D = Delaunay(pts)
    for i in order:
        D.insert(i)
    return D


def lifting_delaunay(pts):
    """Delaunay by the lifting map: the lower hull of (x, y, x^2 + y^2), with scipy's 3D hull."""
    from scipy.spatial import ConvexHull
    P = np.asarray(pts, dtype=float)
    L = np.c_[P, (P ** 2).sum(1)]
    H = ConvexHull(L)
    tris = [tuple(sorted(s)) for s, eq in zip(H.simplices, H.equations) if eq[2] < 0]
    return sorted(tris)


def min_angle(pts, tris):
    best = math.pi
    P = np.asarray(pts, dtype=float)
    for t in tris:
        A, B, C = P[list(t)]
        for u, v, w in ((A, B, C), (B, C, A), (C, A, B)):
            e1, e2 = v - u, w - u
            c = float(np.dot(e1, e2) / (np.linalg.norm(e1) * np.linalg.norm(e2)))
            best = min(best, math.acos(max(-1.0, min(1.0, c))))
    return best


def lawson(pts, tris):
    """Lawson (1977): flip illegal edges of any triangulation until none is left.  Returns (triangles, flips, the
    minimum angle after each flip)."""
    P = [tuple(map(int, p)) for p in pts]
    E = {}

    def add(a, b, c):
        if orient_int(P[a], P[b], P[c]) < 0:
            b, c = c, b
        E[(a, b)] = c
        E[(b, c)] = a
        E[(c, a)] = b

    def rem(a, b, c):
        for e in ((a, b), (b, c), (c, a)):
            E.pop(e, None)
    for t in tris:
        add(*t)
    flips = 0
    angles = []
    changed = True
    while changed:
        changed = False
        for (a, b), c in list(E.items()):
            if E.get((a, b)) != c:
                continue
            d = E.get((b, a))
            if d is None:
                continue
            if _sgn(incircle_float(P[a], P[b], P[c], P[d])) > 0:
                rem(a, b, c)
                rem(b, a, d)
                add(a, d, c)
                add(d, b, c)
                flips += 1
                changed = True
                if flips % 1 == 0:
                    cur = sorted({tuple(sorted((u, v, w))) for (u, v), w in E.items()})
                    angles.append(min_angle(P, cur))
    out = sorted({tuple(sorted((u, v, w))) for (u, v), w in E.items()})
    return out, flips, angles


def sweep_triangulation(pts):
    """Some triangulation of a point set (not Delaunay): sort by x and join each new point to every hull edge it can
    see.  Lawson's flips start from this."""
    P = [tuple(map(int, p)) for p in pts]
    order = sorted(range(len(P)), key=lambda i: P[i])
    a, b, c = order[:3]
    if orient_int(P[a], P[b], P[c]) < 0:
        b, c = c, b
    tris = [(a, b, c)]
    hull = [a, b, c]                     # counter-clockwise
    for i in order[3:]:
        m = len(hull)
        vis = [orient_int(P[hull[k]], P[hull[(k + 1) % m]], P[i]) < 0 for k in range(m)]
        for k in range(m):
            if vis[k]:
                tris.append((hull[k], i, hull[(k + 1) % m]))
        s0 = next(k for k in range(m) if vis[k] and not vis[k - 1])      # the first visible edge
        e0 = s0
        while vis[e0 % m]:
            e0 += 1
        # keep hull[e0 .. s0] (going round), then i
        out = [hull[(e0 + t) % m] for t in range((s0 - e0) % m + 1)]
        hull = out + [i]
    return tris


# ----------------------------------------------------------------------------------------- Fortune's sweep

def _parabola_y(s, x, L):
    sx, sy = s
    if sy == L:
        return math.inf if x != sx else sy
    return ((x - sx) ** 2 + sy * sy - L * L) / (2.0 * (sy - L))


def beach_line(sites, L, xs):
    """The beach line for a sweep line at height L moving down: the lower envelope of the parabolas of the sites
    above it.  Returns y for each x (inf where no site is above)."""
    ys = np.full(len(xs), np.inf)
    for s in sites:
        if s[1] > L:
            ys = np.minimum(ys, ((xs - s[0]) ** 2 + s[1] ** 2 - L * L) / (2.0 * (s[1] - L)))
    return ys


def _breakpoint(p, q, L):
    """x of the breakpoint with p's arc on the left and q's arc on the right, for a sweep at L (below both)."""
    px, py = p
    qx, qy = q
    if py == qy:
        return (px + qx) / 2.0
    if py == L:
        return px
    if qy == L:
        return qx
    dp, dq = 2.0 * (py - L), 2.0 * (qy - L)
    a = 1.0 / dp - 1.0 / dq
    b = -2.0 * (px / dp - qx / dq)
    c = (px * px + py * py - L * L) / dp - (qx * qx + qy * qy - L * L) / dq
    disc = max(b * b - 4 * a * c, 0.0)
    r1 = (-b - math.sqrt(disc)) / (2 * a)
    r2 = (-b + math.sqrt(disc)) / (2 * a)
    # of the two crossings, the one with p's arc on the left: p lower just left of it
    for r in sorted((r1, r2)):
        if _parabola_y(p, r - 1e-7 * (1 + abs(r)), L) <= _parabola_y(q, r - 1e-7 * (1 + abs(r)), L):
            if _parabola_y(p, r + 1e-7 * (1 + abs(r)), L) >= _parabola_y(q, r + 1e-7 * (1 + abs(r)), L):
                return r
    return min(r1, r2) if py < qy else max(r1, r2)


def _circumcircle(a, b, c):
    ax, ay = a
    bx, by = b
    cx, cy = c
    d = 2.0 * (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by))
    if d == 0:
        return None
    ux = ((ax * ax + ay * ay) * (by - cy) + (bx * bx + by * by) * (cy - ay) + (cx * cx + cy * cy) * (ay - by)) / d
    uy = ((ax * ax + ay * ay) * (cx - bx) + (bx * bx + by * by) * (ax - cx) + (cx * cx + cy * cy) * (bx - ax)) / d
    return ux, uy, math.hypot(ax - ux, ay - uy)


def fortune(sites):
    """Fortune's sweep (1986), with the beach line as a plain list of arcs (so O(n^2) here, O(n log n) with a balanced
    tree).  The sweep line moves down.  Returns a dict: Voronoi vertices (with the three sites of each), Delaunay
    triangles, and counts of site events, circle events and false alarms."""
    S = [tuple(map(float, s)) for s in sites]
    n = len(S)
    q = [(-S[i][1], 0, i, None) for i in range(n)]       # max-heap by y: (-y, kind, payload, arc id)
    heapq.heapify(q)
    arcs: list[list] = []          # [site, arc id, circle event key or None]
    next_id = [0]
    valid: dict[int, tuple] = {}   # arc id -> the circle event it is waiting for
    verts = []
    tris = []
    counts = {"site": 0, "circle": 0, "false": 0}
    log = []

    def new_arc(s):
        next_id[0] += 1
        return [s, next_id[0]]

    def check(k, L):
        if k <= 0 or k >= len(arcs) - 1:
            return
        a, b, c = arcs[k - 1][0], arcs[k][0], arcs[k + 1][0]
        if a == c:
            return
        if orient_float(S[a], S[b], S[c]) >= 0:       # breakpoints diverge
            return
        cc = _circumcircle(S[a], S[b], S[c])
        if cc is None:
            return
        ux, uy, r = cc
        y = uy - r
        if y > L + 1e-9:
            return
        aid = arcs[k][1]
        valid[aid] = (a, b, c, ux, uy, y)
        heapq.heappush(q, (-y, 1, aid, (a, b, c)))

    while q:
        ny, kind, payload, extra = heapq.heappop(q)
        L = -ny
        if kind == 0:
            counts["site"] += 1
            s = payload
            if not arcs:
                arcs.append(new_arc(s))
                continue
            x = S[s][0]
            k = 0
            while k < len(arcs) - 1 and _breakpoint(S[arcs[k][0]], S[arcs[k + 1][0]], L) < x:
                k += 1
            a = arcs[k][0]
            valid.pop(arcs[k][1], None)
            if S[a][1] == L:                    # two sites at the same first height: put the new one beside
                arcs.insert(k + 1, new_arc(s))
                continue
            arcs[k:k + 1] = [new_arc(a), new_arc(s), new_arc(a)]
            check(k, L)
            check(k + 2, L)
        else:
            aid = payload
            ev = valid.get(aid)
            if ev is None or ev[:3] != extra:
                counts["false"] += 1
                continue
            k = next(i for i, ar in enumerate(arcs) if ar[1] == aid)
            a, b, c, ux, uy, y = ev
            counts["circle"] += 1
            verts.append((ux, uy, (a, b, c)))
            tris.append(tuple(sorted((a, b, c))))
            log.append((L, ux, uy))
            valid.pop(aid, None)
            valid.pop(arcs[k - 1][1], None)
            valid.pop(arcs[k + 1][1], None)
            arcs.pop(k)
            check(k - 1, L)
            check(k, L)
    return {"vertices": verts, "triangles": sorted(set(tris)), "counts": counts, "log": log}


# --------------------------------------------------------------------------------------- Seidel's 2D LP

def seidel_lp(H, c, box: float = 1e6, seed: int = 0):
    """Maximize c . x subject to half-planes a . x <= b (rows of H = (a1, a2, b)), inside a big box, by Seidel's
    randomized incremental algorithm (1991).  Returns (x, recomputations, total 1D work)."""
    H = [tuple(h) for h in H]
    if not math.isfinite(box) or box <= 0:
        raise ValueError("box must be finite and positive")
    if len(c) != 2 or not all(math.isfinite(v) for v in c):
        raise ValueError("finite two-dimensional objective required")
    if any(len(h) != 3 or not all(math.isfinite(v) for v in h) for h in H):
        raise ValueError("finite half-plane triples required")
    rng = random.Random(seed)
    H = [tuple(h) for h in H]
    rng.shuffle(H)
    cons = [(1.0, 0.0, box), (-1.0, 0.0, box), (0.0, 1.0, box), (0.0, -1.0, box)]
    # the box optimum
    x = (box if c[0] > 0 else -box, box if c[1] > 0 else -box)
    recompute = 0
    work = 0
    seen = list(cons)
    for i, (a1, a2, b) in enumerate(H):
        if a1 == 0 and a2 == 0:
            if b < 0:
                return None, recompute, work
            continue
        if a1 * x[0] + a2 * x[1] <= b + 1e-9:
            seen.append((a1, a2, b))
            continue
        recompute += 1
        # the new optimum lies on the line a1 x + a2 y = b: a 1D LP over the constraints seen so far
        # parametrize: point p0 + t d with d perpendicular to (a1, a2)
        nrm = a1 * a1 + a2 * a2
        p0 = (a1 * b / nrm, a2 * b / nrm)
        d = (-a2, a1)
        lo, hi = -math.inf, math.inf
        for (e1, e2, f) in seen:
            work += 1
            den = e1 * d[0] + e2 * d[1]
            num = f - (e1 * p0[0] + e2 * p0[1])
            if abs(den) < 1e-15:
                if num < -1e-9:
                    return None, recompute, work
                continue
            t = num / den
            if den > 0:
                hi = min(hi, t)
            else:
                lo = max(lo, t)
        if lo > hi + 1e-9:
            return None, recompute, work
        g = c[0] * d[0] + c[1] * d[1]
        t = hi if g > 0 else lo
        x = (p0[0] + t * d[0], p0[1] + t * d[1])
        seen.append((a1, a2, b))
    return x, recompute, work


# --------------------------------------------------------------------------------------------------- kd-trees

class KDTree:
    """Bentley's kd-tree (1975): split at the median, cycling through coordinates.  Counts nodes visited."""

    def __init__(self, P):
        self.P = np.asarray(P, dtype=float)
        self.d = self.P.shape[1]
        self.visited = 0
        self.root = self._build(np.arange(len(self.P)), 0)

    def _build(self, idx, depth):
        if len(idx) <= 1:
            return ("leaf", idx)
        ax = depth % self.d
        vals = self.P[idx, ax]
        m = len(idx) // 2
        order = idx[np.argpartition(vals, m)]
        split = self.P[order[m], ax]
        return ("node", ax, split, self._build(order[:m], depth + 1), self._build(order[m:], depth + 1))

    def range(self, lo, hi):
        """Report the points in the box [lo, hi]."""
        out = []
        lo, hi = np.asarray(lo, float), np.asarray(hi, float)

        def go(nd, blo, bhi):
            self.visited += 1
            if nd[0] == "leaf":
                for i in nd[1]:
                    if np.all(self.P[i] >= lo) and np.all(self.P[i] <= hi):
                        out.append(int(i))
                return
            _, ax, s, L, R = nd
            if lo[ax] <= s:
                b2 = bhi.copy()
                b2[ax] = s
                go(L, blo, b2)
            if hi[ax] >= s:
                b2 = blo.copy()
                b2[ax] = s
                go(R, b2, bhi)
        go(self.root, np.full(self.d, -np.inf), np.full(self.d, np.inf))
        return out

    def nearest(self, q):
        q = np.asarray(q, float)
        best = [math.inf, -1]

        def go(nd):
            self.visited += 1
            if nd[0] == "leaf":
                for i in nd[1]:
                    dd = float(((self.P[i] - q) ** 2).sum())
                    if dd < best[0]:
                        best[0], best[1] = dd, int(i)
                return
            _, ax, s, L, R = nd
            first, second = (L, R) if q[ax] < s else (R, L)
            go(first)
            if (q[ax] - s) ** 2 < best[0]:
                go(second)
        go(self.root)
        return best[1], math.sqrt(best[0])


# ------------------------------------------------------------------------------- vertical decomposition

def vertical_decomposition(segs, box):
    """The trapezoidal map of non-crossing segments, built by brute force: from every endpoint shoot rays up and down
    to the first segment (or the box).  Returns the vertical walls as ((x, y_low), (x, y_high)) and the number of
    trapezoids (3n + 1 at most)."""
    x0, y0, x1, y1 = box
    walls = []

    def hit(x, y, up):
        best = y1 if up else y0
        for (a, b) in segs:
            (ax, ay), (bx, by) = sorted((a, b))
            if ax < x < bx:
                yy = ay + (by - ay) * (x - ax) / (bx - ax)
                if up and y < yy < best:
                    best = yy
                if not up and best < yy < y:
                    best = yy
        return best
    for s in segs:
        for (x, y) in s:
            walls.append(((x, hit(x, y, False)), (x, hit(x, y, True))))
    return walls, _trapezoids(segs, box)


def _y_at(s, x):
    (ax, ay), (bx, by) = sorted(s)
    return ay + (by - ay) * (x - ax) / (bx - ax)


def _trapezoids(segs, box):
    """Count trapezoids: sweep slabs; a trapezoid is a maximal run of slabs with the same floor and ceiling that no wall
    separates.  A wall at x separates the (floor, ceiling) pair that contains its endpoint."""
    x0, y0, x1, y1 = box
    xs = sorted({p[0] for s in segs for p in s})
    edges = [x0] + xs + [x1]
    prev = {}
    total = 0
    for xa, xb in zip(edges, edges[1:]):
        xm = (xa + xb) / 2
        cross = sorted([i for i, s in enumerate(segs) if min(s[0][0], s[1][0]) < xm < max(s[0][0], s[1][0])],
                       key=lambda i: _y_at(segs[i], xm))
        pairs = list(zip([-1] + cross, cross + [-2]))
        cur = {}
        for pr in pairs:
            if pr in prev:
                # same floor and ceiling: is there an endpoint at xa strictly between them? then a wall splits it
                fl, ce = pr
                yfl = y0 if fl < 0 else _y_at(segs[fl], xa)
                yce = y1 if ce < 0 else _y_at(segs[ce], xa)
                wall = any(p[0] == xa and yfl < p[1] < yce for s in segs for p in s)
                if not wall:
                    cur[pr] = prev[pr]
                    continue
            total += 1
            cur[pr] = total
        prev = cur
    return total


# --------------------------------------------------------------------------- navigable small-world graphs

def nsw_build(X, M: int = 8, ef: int = 32, seed: int = 0):
    """A navigable small-world graph (Malkov et al., the single layer of HNSW): insert points one at a time, linking
    each to the M nearest found by a greedy beam search.  Returns adjacency lists and the distance evaluations used."""
    rng = random.Random(seed)
    n = len(X)
    order = list(range(n))
    rng.shuffle(order)
    adj: dict[int, list[int]] = {order[0]: []}
    evals = [0]
    for k in range(1, n):
        i = order[k]
        cand = nsw_search(X, adj, X[i], ef, entry=order[0], evals=evals)
        nb = [j for _, j in cand[:M]]
        adj[i] = list(nb)
        for j in nb:
            adj[j].append(i)
            if len(adj[j]) > 2 * M:
                dj = [(float(((X[j] - X[t]) ** 2).sum()), t) for t in adj[j]]
                adj[j] = [t for _, t in sorted(dj)[:2 * M]]
    return adj, evals[0]


def nsw_search(X, adj, q, ef: int, entry: int, evals=None):
    """Greedy beam search from the entry point; returns [(squared distance, index)] sorted, at most ef."""
    evals = evals if evals is not None else [0]
    d0 = float(((X[entry] - q) ** 2).sum())
    evals[0] += 1
    visited = {entry}
    cand = [(d0, entry)]
    best = [(-d0, entry)]
    while cand:
        d, c = heapq.heappop(cand)
        if d > -best[0][0] and len(best) >= ef:
            break
        for nb in adj.get(c, ()):
            if nb in visited:
                continue
            visited.add(nb)
            dn = float(((X[nb] - q) ** 2).sum())
            evals[0] += 1
            if len(best) < ef or dn < -best[0][0]:
                heapq.heappush(cand, (dn, nb))
                heapq.heappush(best, (-dn, nb))
                if len(best) > ef:
                    heapq.heappop(best)
    return sorted((-d, i) for d, i in best)


class HNSW:
    """Hierarchical navigable small worlds (Malkov and Yashunin 2016), plainly: every point gets a random level
    (geometric, mean 1/ln M); each level is a small-world graph; a query descends greedily from the top, then runs a
    beam search on level 0.  Counts distance evaluations."""

    def __init__(self, X, M: int = 12, ef_construction: int = 80, seed: int = 0):
        self.X = X
        self.M = M
        rng = random.Random(seed)
        mL = 1.0 / math.log(M)
        self.levels: list[dict[int, list[int]]] = []
        self.entry = None
        self.top = -1
        self.evals = 0
        order = list(range(len(X)))
        rng.shuffle(order)
        for i in order:
            lv = int(-math.log(1.0 - rng.random()) * mL)
            self._insert(i, lv, ef_construction)

    def _d(self, i, q):
        self.evals += 1
        v = self.X[i] - q
        return float(np.dot(v, v))

    def _search(self, q, entry, ef, level):
        d0 = self._d(entry, q)
        visited = {entry}
        cand = [(d0, entry)]
        best = [(-d0, entry)]
        adj = self.levels[level]
        while cand:
            d, c = heapq.heappop(cand)
            if d > -best[0][0] and len(best) >= ef:
                break
            for nb in adj.get(c, ()):
                if nb in visited:
                    continue
                visited.add(nb)
                dn = self._d(nb, q)
                if len(best) < ef or dn < -best[0][0]:
                    heapq.heappush(cand, (dn, nb))
                    heapq.heappush(best, (-dn, nb))
                    if len(best) > ef:
                        heapq.heappop(best)
        return sorted((-d, i) for d, i in best)

    def _insert(self, i, lv, efc):
        q = self.X[i]
        while len(self.levels) <= lv:
            self.levels.append({})
        if self.entry is None:
            for L in range(lv + 1):
                self.levels[L][i] = []
            self.entry, self.top = i, lv
            return
        ep = self.entry
        for L in range(self.top, lv, -1):
            ep = self._search(q, ep, 1, L)[0][1]
        for L in range(min(lv, self.top), -1, -1):
            res = self._search(q, ep, efc, L)
            m = self.M * (2 if L == 0 else 1)
            nb = self._select(res, m)
            self.levels[L][i] = list(nb)
            for j in nb:
                lst = self.levels[L].setdefault(j, [])
                lst.append(i)
                if len(lst) > m:
                    dj = sorted((float(np.dot(self.X[j] - self.X[t], self.X[j] - self.X[t])), t) for t in lst)
                    self.levels[L][j] = self._select(dj, m)
            ep = res[0][1]
        for L in range(self.top + 1, lv + 1):
            self.levels[L][i] = []
        if lv > self.top:
            self.entry, self.top = i, lv

    def _select(self, cand, m):
        """The neighbour heuristic: keep a candidate only if it is closer to the new point than to every neighbour
        already kept, so that links fan out in different directions (and bridge clusters)."""
        out = []
        for d, e in cand:
            if all(d < float(np.dot(self.X[e] - self.X[r], self.X[e] - self.X[r])) for r in out):
                out.append(e)
                if len(out) >= m:
                    break
        return out

    def query(self, q, k: int = 10, ef: int = 40):
        ep = self.entry
        for L in range(self.top, 0, -1):
            ep = self._search(q, ep, 1, L)[0][1]
        return self._search(q, ep, max(ef, k), 0)[:k]


# ----------------------------------------------------------------------------- duality and ham sandwiches

def ham_sandwich(red, blue):
    """A line through one red and one blue point with at most half of each colour strictly on either side (odd
    counts), by trying every pair: the ham-sandwich cut, brute force.  Returns (red point, blue point, tests)."""
    tests = 0
    hr, hb = len(red) // 2, len(blue) // 2
    for p in red:
        for q in blue:
            if p == q:
                continue
            lr = sum(1 for r in red if r != p and orient_int(p, q, r) > 0)
            rr = sum(1 for r in red if r != p and orient_int(p, q, r) < 0)
            lb = sum(1 for b in blue if b != q and orient_int(p, q, b) > 0)
            rb = sum(1 for b in blue if b != q and orient_int(p, q, b) < 0)
            tests += len(red) + len(blue)
            if lr <= hr and rr <= hr and lb <= hb and rb <= hb:
                return p, q, tests
    return None, None, tests


# --------------------------------------------------------------------------- configuration space planning

def minkowski_cspace(obstacle, robot):
    """The configuration-space obstacle of a convex obstacle for a translating convex robot (reference point at the
    robot's origin): obstacle (+) (-robot), as the hull of all pairwise differences."""
    pts = [(o[0] - r[0], o[1] - r[1]) for o in obstacle for r in robot]
    return monotone_chain(pts)


def _seg_hits_poly(a, b, poly):
    """Intersect a segment with the strict interior of a convex CCW polygon.

    Boundary contact and travel along edges are allowed. Half-plane interval clipping
    checks the complete segment, including paths through two polygon vertices.
    Arithmetic is floating point; this is not an exact collision certificate.
    """
    if len(poly) < 3:
        raise ValueError("a convex polygon needs at least three vertices")
    lo, hi = 0.0, 1.0
    for u, v in zip(poly, (*poly[1:], poly[0])):
        f0, f1 = orient_float(u, v, a), orient_float(u, v, b)
        slope = f1-f0
        if slope == 0.0:
            if f0 <= 0.0:
                return False
        elif slope > 0.0:
            lo = max(lo, -f0/slope)
        else:
            hi = min(hi, -f0/slope)
        if lo >= hi:
            return False
    return lo < hi


def _strictly_inside(p, poly):
    return all(orient_float(u,v,p) > 0 for u,v in zip(poly,(*poly[1:],poly[0])))


def visibility_path(start, goal, polys):
    """The shortest path among polygonal obstacles runs along the visibility graph of their vertices (Lozano-Pérez and
    Wesley 1979): build it and run Dijkstra.  Returns (path, length, edges in the graph)."""
    if any(_strictly_inside(p, poly) for p in (start,goal) for poly in polys):
        raise ValueError("start and goal must lie outside obstacle interiors")
    V = [tuple(start), tuple(goal)] + [tuple(p) for poly in polys for p in poly]
    n = len(V)
    adj = [[] for _ in range(n)]
    edges = 0
    for i in range(n):
        for j in range(i + 1, n):
            a, b = V[i], V[j]
            if any(_seg_hits_poly(a, b, P) for P in polys):
                continue
            w = math.dist(a, b)
            adj[i].append((j, w))
            adj[j].append((i, w))
            edges += 1
    dist = [math.inf] * n
    prev = [-1] * n
    dist[0] = 0.0
    h = [(0.0, 0)]
    while h:
        d, u = heapq.heappop(h)
        if d > dist[u]:
            continue
        for v, w in adj[u]:
            if d + w < dist[v]:
                dist[v] = d + w
                prev[v] = u
                heapq.heappush(h, (d + w, v))
    if not math.isfinite(dist[1]):
        return [], math.inf, edges
    path = []
    u = 1
    while u != -1:
        path.append(V[u])
        u = prev[u]
    return path[::-1], dist[1], edges


# ----------------------------------------------------------------------------- sampling planners, EMST, Welzl

def rrt(start, goal, polys, box, step: float = 0.6, iters: int = 4000, goal_bias: float = 0.05, seed: int = 0):
    """LaValle's rapidly-exploring random tree in a 2D configuration space: sample a point (sometimes the goal), find
    the nearest tree node, step towards the sample, keep the step if it is collision-free.  Returns (nodes, parent,
    path to the goal or None, iterations used)."""
    if not math.isfinite(step) or step <= 0 or not isinstance(iters, Integral) or iters < 0:
        raise ValueError("positive finite step and nonnegative integer iteration limit required")
    if not 0 <= goal_bias <= 1 or len(box) != 4 or not all(math.isfinite(x) for x in box) or box[0] >= box[2] or box[1] >= box[3]:
        raise ValueError("invalid sampling box or goal probability")
    if any(_strictly_inside(p, poly) for p in (start,goal) for poly in polys):
        raise ValueError("start and goal must lie outside obstacle interiors")
    if tuple(start) == tuple(goal):
        return [tuple(start)], [-1], [tuple(start)], 0
    rng = random.Random(seed)
    x0, y0, x1, y1 = box
    nodes = [tuple(start)]
    parent = [-1]
    for it in range(1, iters + 1):
        q = tuple(goal) if rng.random() < goal_bias else (rng.uniform(x0, x1), rng.uniform(y0, y1))
        k = min(range(len(nodes)), key=lambda i: (nodes[i][0] - q[0]) ** 2 + (nodes[i][1] - q[1]) ** 2)
        a = nodes[k]
        d = math.dist(a, q)
        if d < 1e-9:
            continue
        b = q if d <= step else (a[0] + (q[0] - a[0]) * step / d, a[1] + (q[1] - a[1]) * step / d)
        if any(_seg_hits_poly(a, b, P) for P in polys):
            continue
        nodes.append(b)
        parent.append(k)
        if math.dist(b, goal) <= step and not any(_seg_hits_poly(b, tuple(goal), P) for P in polys):
            nodes.append(tuple(goal))
            parent.append(len(nodes) - 2)
            path = []
            u = len(nodes) - 1
            while u != -1:
                path.append(nodes[u])
                u = parent[u]
            return nodes, parent, path[::-1], it
    return nodes, parent, None, iters


def emst_delaunay(pts, tris):
    """The Euclidean minimum spanning tree by Kruskal over the Delaunay edges only.  Returns (edges, weight)."""
    E = set()
    for a, b, c in tris:
        E |= {(min(a, b), max(a, b)), (min(b, c), max(b, c)), (min(a, c), max(a, c))}
    P = np.asarray(pts, dtype=float)
    order = sorted(E, key=lambda e: float(np.hypot(*(P[e[0]] - P[e[1]]))))
    par = list(range(len(P)))

    def find(x):
        while par[x] != x:
            par[x] = par[par[x]]
            x = par[x]
        return x
    out, w = [], 0.0
    for a, b in order:
        ra, rb = find(a), find(b)
        if ra != rb:
            par[ra] = rb
            out.append((a, b))
            w += float(np.hypot(*(P[a] - P[b])))
    return out, w, len(E)


def emst_prim(pts):
    """Prim's algorithm on the complete graph, O(n^2) with numpy: the reference answer."""
    P = np.asarray(pts, dtype=float)
    n = len(P)
    if n == 0:
        return 0.0
    inside = np.zeros(n, bool)
    best = np.full(n, np.inf)
    best[0] = 0.0
    w = 0.0
    for _ in range(n):
        u = int(np.argmin(np.where(inside, np.inf, best)))
        inside[u] = True
        w += best[u]
        d = np.hypot(*(P - P[u]).T)
        best = np.where(~inside & (d < best), d, best)
    return w


def welzl(pts, seed: int = 0):
    """Welzl (1991): the smallest circle enclosing the points, by randomized incremental construction (iterative
    form).  Returns ((cx, cy), r, the number of times the circle was rebuilt)."""
    P = [tuple(map(float, p)) for p in pts]
    if not P:
        return (0.0,0.0), 0.0, 0
    random.Random(seed).shuffle(P)
    rebuilt = 0

    def circ2(a, b):
        c = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
        return c, math.dist(a, c)

    def circ3(a, b, c):
        cc = _circumcircle(a, b, c)
        if cc is None:
            pts3 = sorted((a, b, c))
            return circ2(pts3[0], pts3[-1])
        return (cc[0], cc[1]), cc[2]

    def inside(c, p):
        return math.dist(c[0], p) <= c[1] * (1 + 1e-12) + 1e-12
    c = (P[0], 0.0)
    for i in range(1, len(P)):
        if inside(c, P[i]):
            continue
        rebuilt += 1
        c = (P[i], 0.0)
        for j in range(i):
            if inside(c, P[j]):
                continue
            c = circ2(P[i], P[j])
            for k in range(j):
                if not inside(c, P[k]):
                    c = circ3(P[i], P[j], P[k])
    return c[0], c[1], rebuilt
