"""Precompute everything numerical in Part 22 of *Computer Science, Built* ("Geometry").

    python -m videos.cs.cs22.compute              # everything missing
    python -m videos.cs.cs22.compute --force hulls

Results are cached in ``.cache/cs22/<name>.json``; scenes call ``load(name)``.  The instrument is
``explainer/cs/algo/geometry.py`` (tested in tests/test_cs22_geometry.py).

Items:
    hook      three rotations of one orientation test that disagree in floating point
    orient    Kettner's grid of float against exact signs; the adaptive filter's rate and cost
    hulls     five hull algorithms counting orientation tests on three distributions; sorting by hull
    sweep     Bentley-Ottmann: a logged small sweep, and events against brute force
    gallery   ear clipping and Fisk's three-colouring on a random polygon and on Chvátal's comb
    voronoi   Fortune's sweep: a logged small run, and event counts against n
    delaunay  empty circles, Lawson flips from a bad triangulation, incremental insertion counts
    lifting   a small set lifted to the paraboloid; its lower hull against the Delaunay triangulation
    lp        Seidel's LP: a logged run in the plane, and recomputations against exact 2 H_n
    kd        a kd-tree's cells, and range-query visits against sqrt(n) + k
    pointloc  a trapezoidal map, and trapezoid counts against 3n + 1
    highdim   distance concentration, kd-trees against dimension, a navigable small-world graph
    duality   points and lines, and a ham-sandwich cut
    planning  a translating triangle among obstacles: configuration space, the shortest path, random trees
    emst      the Euclidean minimum spanning tree inside the Delaunay triangulation, against Prim on all pairs
    welzl     Welzl's smallest enclosing circle
    frontier  the price of exactness; 3SUM as collinearity
"""

from __future__ import annotations

import functools
import hashlib
import inspect
import json
from pathlib import Path
from explainer.cache_lock import locked_item
from .measurement_references import (protocol,digest,hull_reference,crossing_pairs,triangulation_certificate,
                                      delaunay_certificate,circle_certificate,path_certificate,segment_interior_reference)

import math
import random
import time

import numpy as np

from explainer.ai.cache import Cache
from explainer.cs.algo import geometry as G

SCHEMAS = {name:2 for name in ('hook','orient','hulls','sweep','gallery','voronoi','delaunay','lifting','lp','kd','pointloc','highdim','duality','planning','emst','welzl','frontier')}

class GeometryCache(Cache):
    @locked_item(lambda self,name:self.path(name))
    def load(self,name):
        if not cache_current(name,self.path(name)):
            self.save(name,ITEMS[name]())
        return super().load(name)

CACHE = GeometryCache("cs22")

def cache_current(name,path=None):
    path = CACHE.path(name) if path is None else path
    return name not in SCHEMAS or path.exists() and json.loads(path.read_text()).get('schema') == SCHEMAS[name]

def load(name):
    return CACHE.load(name)

_TRIALS=[]

def _elapsed(start,operation):
    elapsed=time.perf_counter()-start
    _TRIALS.append(dict(operation=operation,samples=[elapsed],repeats=1,statistic='single observation',validation='checked after timer'))
    return elapsed


def _best(f,reps=3):
    samples=[];hashes=[];out=None
    for _ in range(reps):
        start=time.perf_counter();out=f();samples.append(time.perf_counter()-start)
        hashes.append(digest(out))
    assert len(set(hashes))==1, "repeated deterministic operation changed output"
    _TRIALS.append(dict(operation=inspect.currentframe().f_back.f_code.co_name,samples=samples,repeats=reps,
                        statistic='minimum',seconds=min(samples),output_sha256=hashes,
                        validation='all repeated outputs have identical canonical hashes; final output checked independently after timing'))
    return min(samples),out


def _ints(n, rng, M=10 ** 6):
    return [(rng.randint(0, M), rng.randint(0, M)) for _ in range(n)]


def compute_hook() -> dict:
    p0, q, r = (0.5, 0.5), (12.0, 12.0), (24.0, 24.0)
    n = 256
    xs = [p0[0]]
    for _ in range(n - 1):
        xs.append(math.nextafter(xs[-1], math.inf))
    disagree = 0
    example = None
    for j in range(n):
        for i in range(n):
            p = (xs[i], xs[j])
            s = [int(np.sign(G.orient_float(*t))) for t in ((p, q, r), (q, r, p), (r, p, q))]
            if len(set(s)) > 1:
                disagree += 1
                if example is None and 1 in s and -1 in s:
                    example = {"p": [repr(p[0]), repr(p[1])], "signs": s, "exact": G.orient_exact(p, q, r),
                               "i": i, "j": j}
    return {"q": q, "r": r, "n": n, "disagree": disagree, "example": example}


def compute_orient() -> dict:
    p0, q, r = (0.5, 0.5), (12.0, 12.0), (24.0, 24.0)
    fl, ex = G.kettner_grid(p0, q, r, 256)
    rng = random.Random(0)
    rand = [tuple((rng.uniform(-1, 1), rng.uniform(-1, 1)) for _ in range(3)) for _ in range(20000)]
    near = []
    for _ in range(20000):
        a = (rng.uniform(0, 1), rng.uniform(0, 1))
        b = (rng.uniform(0, 1), rng.uniform(0, 1))
        t = rng.uniform(0, 1)
        c = (a[0] + t * (b[0] - a[0]), a[1] + t * (b[1] - a[1]))
        near.append((a, b, c))
    rows = []
    for name, data in (("random", rand), ("nearly collinear", near)):
        t_f, _ = _best(lambda: [G.orient_float(*x) for x in data])
        t_a, outs = _best(lambda: [G.orient_adaptive(*x) for x in data])
        t_e, ex_s = _best(lambda: [G.orient_exact(*x) for x in data], reps=1)
        assert [sign for sign,_ in outs]==ex_s
        wrong = sum(1 for x, e in zip(data, ex_s) if int(np.sign(G.orient_float(*x))) != e)
        rows.append({"inputs": name, "n": len(data), "float_ns": t_f / len(data) * 1e9,
                     "adaptive_ns": t_a / len(data) * 1e9, "exact_ns": t_e / len(data) * 1e9,
                     "exact_share": sum(1 for _, u in outs if u) / len(data), "float_wrong": wrong})
    return {"grid_float": fl.tolist(), "grid_exact": ex.tolist(), "wrong": int((fl != ex).sum()),
            "zero_exact": int((ex == 0).sum()), "zero_float": int((fl == 0).sum()), "rows": rows,
            "errbound": G.CCW_ERRBOUND}


def compute_hulls() -> dict:
    rng = random.Random(1)

    def square(n):
        return _ints(n, rng)

    def disk(n):
        out = []
        while len(out) < n:
            x, y = rng.randint(-10 ** 6, 10 ** 6), rng.randint(-10 ** 6, 10 ** 6)
            if x * x + y * y <= 10 ** 12:
                out.append((x, y))
        return out

    def circle(n):
        out = set()
        while len(out) < n:
            t = rng.uniform(0, 2 * math.pi)
            out.add((round(10 ** 6 * math.cos(t)), round(10 ** 6 * math.sin(t))))
        return list(out)
    rows = []
    for dist, gen in (("square", square), ("disk", disk), ("circle", circle)):
        for n in (1000, 10000):
            P = gen(n)
            row = {"dist": dist, "n": n}
            for name, f in (("jarvis", G.jarvis), ("graham", G.graham), ("monotone", G.monotone_chain),
                            ("quickhull", G.quickhull), ("chan", G.chan)):
                if name == "jarvis" and dist == "circle" and n > 1000:
                    row[name] = None
                    continue
                c = G.Counter()
                t0 = time.perf_counter()
                h = f(P, c)
                seconds = _elapsed(t0,'hulls:'+dist+':'+str(n)+':'+name)
                if name == "chan":
                    h = h[0]
                assert set(h)==set(hull_reference(P))
                row[name + "_verified"] = True
                row[name] = c.n
                row[name + "_cmp"] = c.cmp
                row[name + "_s"] = seconds
                row["h"] = len(h)
            row['input_sha256']=digest(P)
            rows.append(row)
    # a small set for the animations
    small = _ints(28, random.Random(7), 1000)
    c = G.Counter()
    hull = G.graham(small, c)
    o = min(small, key=lambda p: (p[1], p[0]))
    def angular(a,b):
        turn=G.orient_int(o,a,b)
        return -turn if turn else G._sgn(G._d2(o,a)-G._d2(o,b))
    order = sorted((p for p in small if p != o), key=functools.cmp_to_key(angular))
    # the Graham scan step by step: the stack after each point
    st = [o]
    steps = []
    for p in order:
        popped = []
        while len(st) >= 2 and G.orient_int(st[-2], st[-1], p) <= 0:
            popped.append(st.pop())
        st.append(p)
        steps.append({"p": p, "popped": popped, "stack": list(st)})
    assert st==hull
    # sorting by hull
    xs = [11, -26, 38, -6, 19, -37, 3, 28, -15]        # an unsorted list, spread out enough to label
    lifted = [(x, x * x) for x in xs]
    h = G.monotone_chain(lifted)
    lo = h.index(min(h))
    return {"rows": rows, "small": small, "small_hull": hull, "graham_steps": steps, "origin": o,
            "sort_xs": xs, "sort_hull": h[lo:] + h[:lo]}


def compute_sweep() -> dict:
    rng = random.Random(11)
    segs = []
    for _ in range(7):
        a = (rng.uniform(0, 10), rng.uniform(0, 6))
        segs.append((a, (a[0] + rng.uniform(2.5, 6), rng.uniform(0, 6))))
    found, ev, tests, log = G.bentley_ottmann(segs, log=True)
    rows = []
    for n in (100, 300, 1000, 3000):
        S = []
        for _ in range(n):
            a = (rng.random(), rng.random())
            L = 0.6 / math.sqrt(n) * 4
            t = rng.uniform(-1, 1)
            S.append((a, (a[0] + L, a[1] + t * L)))
        t0 = time.perf_counter()
        f, e, ts, _ = G.bentley_ottmann(S)
        t_bo = _elapsed(t0,'sweep:'+str(n))
        br = crossing_pairs(S)
        ok = sorted((i,j)for i,j,_ in f)==br
        assert ok
        rows.append({"n": n, "k": len(f), "events": e, "tests": ts, "pairs": n * (n - 1) // 2, "seconds": t_bo,
                     "ok": ok})
    return {"segs": segs, "found": [[i, j, list(p)] for i, j, p in found], "events": ev, "tests": tests, "log": log,
            "rows": rows}


def compute_gallery() -> dict:
    poly = G.star_polygon(22, seed=5, r0=350, r1=1000)
    if G.polygon_area2(poly) < 0:
        poly = poly[::-1]
    tris, tests = G.ear_clip(poly)
    col = G.fisk_colouring(len(poly), tris)
    counts = [col.count(c) for c in range(3)]
    cm = G.comb(5)
    ct, _ = G.ear_clip(cm)
    cc = G.fisk_colouring(len(cm), ct)
    assert triangulation_certificate(poly,tris,col)['area2']==abs(G.polygon_area2(poly))
    assert triangulation_certificate(cm,ct,cc)['area2']==abs(G.polygon_area2(cm))
    rows = []
    for seed in range(200):
        P = G.star_polygon(60, seed=100 + seed)
        if G.polygon_area2(P) < 0:
            P = P[::-1]
        T, _ = G.ear_clip(P)
        C = G.fisk_colouring(len(P), T)
        cert=triangulation_certificate(P,T,C)
        assert len(T)==len(P)-2 and cert['area2']==abs(G.polygon_area2(P))
        rows.append(min(C.count(c) for c in range(3)))
    return {"poly": poly, "tris": tris, "tests": tests, "col": col, "counts": counts, "comb": cm, "comb_tris": ct,
            "comb_col": cc, "comb_counts": [cc.count(c) for c in range(3)],
            "random_guards": {"n": 60, "mean": float(np.mean(rows)), "max": int(max(rows)), "bound": 20}}


def compute_voronoi() -> dict:
    rng = random.Random(21)
    sites = [(round(rng.uniform(-6, 6), 3), round(rng.uniform(-3.2, 3.2), 3)) for _ in range(14)]
    F = G.fortune(sites)
    rows = []
    for n in (250, 500, 1000, 2000):
        P = _ints(n, rng)
        t0 = time.perf_counter()
        R = G.fortune(P)
        t = _elapsed(t0,'fortune:'+str(n))
        ref = G.lifting_delaunay(P)
        assert R['triangles']==ref and R['counts']['site']==n
        assert R['counts']['circle']==2*n-2-len(hull_reference(P))
        h = len(G.monotone_chain(P))
        rows.append({"n": n, "site": R["counts"]["site"], "circle": R["counts"]["circle"],
                     "false": R["counts"]["false"], "expected": 2 * n - 2 - h, "match": R["triangles"] == ref,
                     "seconds": t})
    return {"sites": sites, "vertices": [[v[0], v[1], list(v[2])] for v in F["vertices"]], "tris": F["triangles"],
            "log": F["log"], "counts": F["counts"], "rows": rows}


def compute_delaunay() -> dict:
    rng = random.Random(31)
    P = _ints(16, rng, 1000)
    T0 = G.sweep_triangulation(P)
    L, flips, angles = G.lawson(P, T0)
    ref = G.lifting_delaunay(P)
    # Lawson's flips, one at a time, for the animation
    seq = []
    E = {}

    def add(a, b, c):
        if G.orient_int(P[a], P[b], P[c]) < 0:
            b, c = c, b
        E[(a, b)] = c
        E[(b, c)] = a
        E[(c, a)] = b

    def rem(a, b, c):
        for e in ((a, b), (b, c), (c, a)):
            E.pop(e, None)
    for t in T0:
        add(*t)
    changed = True
    while changed:
        changed = False
        for (a, b), c in list(E.items()):
            if E.get((a, b)) != c:
                continue
            d = E.get((b, a))
            if d is None:
                continue
            if G._sgn(G.incircle_float(P[a], P[b], P[c], P[d])) > 0:
                rem(a, b, c)
                rem(b, a, d)
                add(a, d, c)
                add(d, b, c)
                seq.append([a, b, c, d])
                changed = True
    # incremental insertion, random order against an adversarial order
    rows = []
    for n in (1000, 4000, 16000):
        Q = _ints(n, rng)
        D = G.delaunay(Q, seed=n)
        cert=delaunay_certificate(Q,D.triangles())
        rows.append({"n": n, "order": "random", "created": D.created, "flips": D.flips, "walk": D.walk})
    for k in (100, 200, 400, 800):
        # a flat convex chain, then points above its middle, inserted from the top down: each new one sees them all
        A = [(i * 10000, i * i) for i in range(k)]
        B = [(k * 5000 + j * 3, 2 * 10 ** 5 + 10 ** 9 // (j + 1)) for j in range(k)]
        Q = A + B
        D = G.delaunay(Q, order=list(range(2 * k)))
        Dr = G.delaunay(Q, seed=1)
        delaunay_certificate(Q,D.triangles());delaunay_certificate(Q,Dr.triangles())
        rows.append({"n": 2 * k, "order": "adversarial", "created": D.created, "flips": D.flips, "walk": D.walk,
                     "created_random": Dr.created, "flips_random": Dr.flips})
    assert L==ref
    delaunay_certificate(P,L)
    return {"P": P, "T0": [list(t) for t in T0], "flips": flips, "seq": seq, "L": L, "match": L == ref,
            "angles": [math.degrees(a) for a in angles], "min0": math.degrees(G.min_angle(P, T0)),
            "min1": math.degrees(G.min_angle(P, L)), "rows": rows}


def compute_lifting() -> dict:
    rng = random.Random(41)
    P = [(round(rng.uniform(-1.6, 1.6), 3), round(rng.uniform(-1.6, 1.6), 3)) for _ in range(18)]
    from scipy.spatial import ConvexHull, Delaunay as SD
    L = np.c_[np.asarray(P), (np.asarray(P) ** 2).sum(1)]
    H = ConvexHull(L)
    lower = sorted(tuple(sorted(s)) for s, e in zip(H.simplices, H.equations) if e[2] < 0)
    upper = sorted(tuple(sorted(s)) for s, e in zip(H.simplices, H.equations) if e[2] >= 0)
    sd = sorted(tuple(sorted(s)) for s in SD(np.asarray(P)).simplices)
    assert lower==sd
    # the in-circle determinant equals an orientation test in 3D on the lifted points
    a, b, c, d = (0.0, 0.0), (4.0, 0.0), (0.0, 4.0), (1.0, 1.0)
    M = np.array([[*p, p[0] ** 2 + p[1] ** 2, 1.0] for p in (a, b, c, d)])
    return {"P": P, "lower": lower, "upper": upper, "match": lower == sd, "det4": float(np.linalg.det(M)),
            "incircle": G.incircle_float(a, b, c, d)}


def compute_lp() -> dict:
    rng = random.Random(51)
    H = []
    for k in range(9):
        t = 2 * math.pi * k / 9 + rng.uniform(-0.25, 0.25)
        H.append((round(math.cos(t), 4), round(math.sin(t), 4), round(rng.uniform(1.4, 2.6), 3)))
    c = (0.55, 1.0)
    # a logged run: the optimum after each constraint, in the order given
    trace = []
    order = list(range(len(H)))
    random.Random(187).shuffle(order)          # three moves in nine: about the most a random order gives
    for k in range(1, len(order) + 1):
        x, rc, _ = G.seidel_lp([H[i] for i in order[:k]], c, box=2.8, seed=10 ** 9)
        trace.append({"added": order[k - 1], "x": list(x)})
    rows = []
    from scipy.optimize import linprog
    for n in (10, 100, 1000, 10000, 100000):
        recs, works = [], []
        for s in range(20 if n <= 10000 else 5):
            Hs = []
            for _ in range(n):
                t = rng.uniform(0, 2 * math.pi)
                Hs.append((math.cos(t), math.sin(t), 1 + rng.random()))
            x, rc, w = G.seidel_lp(Hs, (1.0, 0.3), seed=s)
            reference=linprog([-1,-0.3],A_ub=[h[:2]for h in Hs],b_ub=[h[2]for h in Hs],bounds=[(-1e6,1e6)]*2)
            assert reference.success and x is not None
            assert np.all(np.asarray(Hs)[:,:2]@np.asarray(x)<=np.asarray(Hs)[:,2]+1e-7)
            assert abs(x[0]+.3*x[1]+reference.fun)<1e-6
            recs.append(rc)
            works.append(w)
        ok=True
        rows.append({"n": n, "recompute": float(np.mean(recs)), "bound": 2 * math.fsum(1/i for i in range(1,n+1)),
                     "work_per_n": float(np.mean(works)) / n, "ok": ok})
    return {"H": H, "c": c, "order": order, "trace": trace, "rows": rows}


def compute_kd() -> dict:
    rng = np.random.default_rng(61)
    P = rng.random((60, 2))
    T = G.KDTree(P)
    cells = []

    def walk(nd, lo, hi, depth):
        if nd[0] == "leaf":
            return
        _, ax, s, Lc, Rc = nd
        if ax == 0:
            cells.append([float(s), float(lo[1]), float(s), float(hi[1]), depth])
        else:
            cells.append([float(lo[0]), float(s), float(hi[0]), float(s), depth])
        h2 = list(hi)
        h2[ax] = s
        walk(Lc, lo, h2, depth + 1)
        l2 = list(lo)
        l2[ax] = s
        walk(Rc, l2, hi, depth + 1)
    walk(T.root, [0.0, 0.0], [1.0, 1.0], 0)
    T.visited = 0
    box = ((0.22, 0.28), (0.68, 0.7))
    got = T.range(*box)
    assert sorted(got)==np.flatnonzero(np.all(P>=box[0],axis=1)&np.all(P<=box[1],axis=1)).tolist()
    rows = []
    for n in (1000, 10000, 100000, 300000):
        Q = rng.random((n, 2))
        t0 = time.perf_counter()
        K = G.KDTree(Q)
        tb = _elapsed(t0,'kd build:'+str(n))
        vis, ks = [], []
        for _ in range(40):
            x, y = rng.random(2) * 0.9
            w = 0.02
            K.visited = 0
            out = K.range((x, y), (x + w, y + w))
            ref=np.flatnonzero(np.all(Q>=(x,y),axis=1)&np.all(Q<=(x+w,y+w),axis=1)).tolist()
            assert sorted(out)==ref
            vis.append(K.visited)
            ks.append(len(out))
        rows.append({"n": n, "visited": float(np.mean(vis)), "k": float(np.mean(ks)), "sqrt_n": math.sqrt(n),
                     "build_s": tb})
    return {"P": P.tolist(), "cells": cells, "box": box, "inside": got, "visited": T.visited, "rows": rows}


def compute_pointloc() -> dict:
    rng = random.Random(71)
    segs = []
    while len(segs) < 7:
        a = (round(rng.uniform(0, 10), 2), round(rng.uniform(0, 6), 2))
        b = (round(a[0] + rng.uniform(1.5, 4), 2), round(a[1] + rng.uniform(-1.2, 1.2), 2))
        if b[0] > 11:
            continue
        if any(G._seg_x_cross((a, b), s) is not None or min(abs(a[0] - p[0]) for p in s) < 0.15 for s in segs):
            continue
        segs.append((a, b))
    walls, nt = G.vertical_decomposition(segs, (-0.5, -1.5, 11.5, 7.5))
    rows = []
    for n in (5, 20, 80):
        counts = []
        for _ in range(20):
            S = []
            tries = 0
            while len(S) < n and tries < 20000:
                tries += 1
                a = (rng.uniform(0, 100), rng.uniform(0, 100))
                b = (a[0] + rng.uniform(1, 12), a[1] + rng.uniform(-5, 5))
                if any(G._seg_x_cross((a, b), s) is not None for s in S):
                    continue
                S.append((a, b))
            assert len(S)==n and not crossing_pairs(S)
            count=G._trapezoids(S,(-1,-10,120,110))
            assert count<=3*n+1
            counts.append(count)
        rows.append({"n": n, "max": max(counts), "mean": float(np.mean(counts)), "bound": 3 * n + 1})
    return {"segs": segs, "walls": walls, "trapezoids": nt, "rows": rows}


def compute_highdim() -> dict:
    rng = np.random.default_rng(81)
    conc = []
    for d in (1, 2, 5, 10, 20, 50, 100, 300, 1000):
        X = rng.random((2000, d))
        q = rng.random(d)
        dist = np.sqrt(((X - q) ** 2).sum(1))
        conc.append({"d": d, "ratio": float(dist.max() / dist.min()), "spread": float((dist.max() - dist.min())
                                                                                    / dist.min())})
    kd = []
    n = 20000
    for d in (2, 4, 8, 12, 16, 24):
        X = rng.random((n, d))
        T = G.KDTree(X)
        vis = []
        for _ in range(20):
            T.visited = 0
            query=rng.random(d);index,distance=T.nearest(query)
            ds=((X-query)**2).sum(1);assert abs(distance**2-ds.min())<=1e-10
            assert abs(ds[index]-ds.min())<=1e-10
            vis.append(T.visited)
        kd.append({"d": d, "visited": float(np.mean(vis)), "nodes": 2 * n - 1, "share": float(np.mean(vis)) /
                   (2 * n - 1)})
    # navigable small-world graphs on 16-dimensional data with structure: points near a few hundred centres
    centres = rng.standard_normal((200, 16)) * 3
    X = (centres[rng.integers(0, 200, 20000)] + rng.standard_normal((20000, 16))).astype(np.float64)
    Q = (centres[rng.integers(0, 200, 100)] + rng.standard_normal((100, 16)))
    truth = [set(np.argsort(((X - q) ** 2).sum(1),kind='stable')[:10].tolist()) for q in Q]
    assert len(Q)==100 and sum(map(len,truth))==1000
    t0 = time.perf_counter()
    adj, build_evals = G.nsw_build(X, M=12, ef=80)
    t_nsw = _elapsed(t0,'single-layer NSW build')
    t0 = time.perf_counter()
    H = G.HNSW(X, M=12, ef_construction=80)
    t_h = _elapsed(t0,'hierarchical NSW build')
    nsw, hn = [], []
    for ef in (10, 20, 40, 80, 160):
        rec, ev = 0.0, 0
        for q, tr in zip(Q, truth):
            e = [0]
            r = G.nsw_search(X, adj, q, ef, entry=0, evals=e)
            ev += e[0]
            rec += len(tr & {j for _, j in r[:10]}) / 10
        nsw.append({"ef": ef, "recall": rec / len(Q), "evals": ev / len(Q)})
        rec = 0.0
        H.evals = 0
        for q, tr in zip(Q, truth):
            r = H.query(q, 10, ef)
            rec += len(tr & {j for _, j in r}) / 10
        hn.append({"ef": ef, "recall": rec / len(Q), "evals": H.evals / len(Q)})
    assert all(0<=r['recall']<=1 and r['evals']>=10 for r in nsw+hn)
    return {"measurement_scope":"mean recall@10 on100 seeded clustered queries; query distance evaluations exclude construction and are not elapsed CPU time; simplified teaching NSW/HNSW-style implementations", "query_count":len(Q),"truth_neighbors":1000,"input_sha256":digest(X),"queries_sha256":digest(Q),"conc": conc, "kd": kd, "kd_n": n, "nsw": nsw, "hnsw": hn, "nsw_n": 20000, "nsw_build_s": t_nsw,
            "hnsw_build_s": t_h, "nsw_build_evals": build_evals, "levels": [len(L) for L in H.levels]}


def compute_duality() -> dict:
    rng = random.Random(91)
    red = [(rng.randint(-50, 50), rng.randint(-30, 30)) for _ in range(9)]
    blue = [(rng.randint(-50, 50), rng.randint(-30, 30)) for _ in range(9)]
    p, q, tests = G.ham_sandwich(red, blue)
    pts = [(-2, 1), (-1, -1), (0, 0.5), (1, 2), (2, -0.5)]
    return {"red": red, "blue": blue, "p": p, "q": q, "tests": tests, "dual_pts": pts}


def compute_planning() -> dict:
    robot = [(0, 0), (1.2, 0), (0.6, 1.0)]
    obs = [[(2.0, 1.0), (4.0, 1.2), (3.6, 3.2), (2.2, 2.8)],
           [(5.0, -2.5), (6.6, -2.0), (6.2, 0.4)],
           [(5.4, 2.2), (7.6, 2.0), (7.2, 4.0), (5.8, 3.8)],
           [(-1.5, -2.8), (0.8, -2.6), (0.2, -1.4)]]
    cs = [G.minkowski_cspace(o, robot) for o in obs]
    start, goal = (-2.5, 3.5), (9.0, -2.5)
    path, length, edges = G.visibility_path(start, goal, cs)
    box = (-3.5, -4.5, 10.5, 5.0)
    runs = []
    for sd in range(20):
        nodes, par, rp, it = G.rrt(start, goal, cs, box, step=0.5, iters=4000, seed=sd)
        for i,parent in enumerate(par):
            if parent>=0:assert not any(segment_interior_reference(nodes[parent],nodes[i],P)for P in cs)
        rl = path_certificate(rp,cs) if rp else None
        runs.append({"seed": sd, "nodes": len(nodes), "iters": it, "length": rl})
    assert abs(path_certificate(path,cs)-length)<1e-8
    successes=[r for r in runs if r['length'] is not None]
    assert successes
    show = min(successes,key=lambda r:abs(r['length']/length-1.3))['seed']
    nodes, par, rp, it = G.rrt(start, goal, cs, box, step=0.5, iters=4000, seed=show)
    ok = [r for r in runs if r["length"]]
    return {"robot": robot, "obs": obs, "cspace": cs, "start": start, "goal": goal, "path": path, "length": length,
            "edges": edges, "rrt_nodes": nodes, "rrt_parent": par, "rrt_path": rp, "rrt_runs": runs,
            "rrt_mean_ratio": float(np.mean([r["length"] / length for r in ok])),
            "rrt_mean_nodes": float(np.mean([r["nodes"] for r in ok])), "rrt_found": len(ok)}


def compute_emst() -> dict:
    rng = random.Random(111)
    P = _ints(70, rng, 1000)
    tris = G.lifting_delaunay(P)
    e, w, ne = G.emst_delaunay(P, tris)
    D = set()
    for a, b, c in tris:
        D |= {(min(a, b), max(a, b)), (min(b, c), max(b, c)), (min(a, c), max(a, c))}
    rows = []
    for n in (500, 2000, 8000):
        Q = _ints(n, rng)
        t0 = time.perf_counter()
        T = G.lifting_delaunay(Q)
        ed, wd, nd = G.emst_delaunay(Q, T)
        t_delaunay = _elapsed(t0,'EMST triangulation plus Kruskal:'+str(n))
        t0 = time.perf_counter()
        wp = G.emst_prim(Q)
        t_prim = _elapsed(t0,'complete graph Prim:'+str(n))
        assert abs(wd-wp)<=1e-6*max(1.,wp)
        rows.append({"n": n, "delaunay_edges": nd, "pairs": n * (n - 1) // 2, "w_delaunay": wd, "w_prim": wp,
                     "same": abs(wd - wp) < 1e-6 * wp, "t_delaunay": t_delaunay, "t_prim": t_prim})
    return {"P": P, "delaunay": sorted(D), "mst": e, "rows": rows}


def compute_welzl() -> dict:
    rng = random.Random(121)
    P = [(round(rng.gauss(0, 1.1), 3), round(rng.gauss(0, 0.8), 3)) for _ in range(40)]
    # the circle after each point, for the animation
    steps = []
    Q = list(P)
    random.Random(0).shuffle(Q)
    for k in range(2, len(Q) + 1):
        c, r, _ = G.welzl(Q[:k], seed=10 ** 6)
        steps.append([c[0], c[1], r])
    c, r, rb = G.welzl(P)
    circle_certificate(P,c,r)
    rows = []
    for n in (100, 1000, 10000, 100000):
        X = [(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(n)]
        t0 = time.perf_counter()
        cc, rr, rb2 = G.welzl(X, seed=n)
        tw = _elapsed(t0,'Welzl:'+str(n))
        certificate=circle_certificate(X,cc,rr)
        far = max(math.dist(cc, x) for x in X)
        rows.append({"n": n, "rebuilt": rb2, "ln_n": math.log(n), "seconds": tw, "ok": abs(far - rr) < 1e-9 * rr})
    return {"P": Q, "steps": steps, "c": list(c), "r": r, "rows": rows}


def compute_frontier() -> dict:
    rng = random.Random(101)
    # the price of exactness on near-degenerate input: float, adaptive, exact (all rationals)
    near = []
    for _ in range(5000):
        a = (rng.uniform(0, 1), rng.uniform(0, 1))
        b = (rng.uniform(0, 1), rng.uniform(0, 1))
        t = rng.uniform(0, 1)
        near.append((a, b, (a[0] + t * (b[0] - a[0]), a[1] + t * (b[1] - a[1]))))
    t_f, _ = _best(lambda: [G.orient_float(*x) for x in near])
    t_e, _ = _best(lambda: [G.orient_exact(*x) for x in near], reps=1)
    # 3SUM as collinearity: a + b + c = 0 exactly when (a, a^3), (b, b^3), (c, c^3) are collinear
    nums = rng.sample(range(-60, 61), 14)
    trip = [(a, b, c) for i, a in enumerate(nums) for j, b in enumerate(nums) for k, c in enumerate(nums)
            if i < j < k and a + b + c == 0]
    col = [(a, b, c) for i, a in enumerate(nums) for j, b in enumerate(nums) for k, c in enumerate(nums)
           if i < j < k and G.orient_int((a, a ** 3), (b, b ** 3), (c, c ** 3)) == 0]
    assert sorted(trip)==sorted(col)
    return {"float_ns": t_f / len(near) * 1e9, "exact_ns": t_e / len(near) * 1e9, "nums": nums, "triples": trip,
            "collinear": col}


def _checked_producer(name,function):
    @functools.wraps(function)
    def checked():
        global _TRIALS
        previous=_TRIALS;_TRIALS=[]
        try:
            start=time.perf_counter();data=function();total=time.perf_counter()-start
            data.update(schema=SCHEMAS[name],protocol=protocol(),timed_trials=list(_TRIALS),
                        producer_wall_seconds=total,producer_wall_scope='includes input generation and post-timer references; not an algorithm benchmark',
                        validation='producer invariants and independent finite references checked outside algorithm timers')
            return data
        finally:_TRIALS=previous
    return checked

ITEMS = {k[8:]:_checked_producer(k[8:],v) for k,v in list(globals().items()) if k.startswith("compute_")}
if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
