"""Instruments for Part 26 (P versus NP).

    cdcl(n, clauses)                    conflict-driven clause learning: watched literals, 1-UIP learning, VSIDS,
                                        phase saving, Luby restarts; returns (model or None, stats)
    dpll(n, clauses)                    plain DPLL with unit propagation, for comparison (counts nodes)
    check(model, clauses)               does an assignment satisfy every clause?
    random_ksat(n, m, k, rng)           uniform random k-CNF
    to_3sat(n, clauses)                 split long clauses with fresh variables (equisatisfiable)
    sat_to_is(clauses)                  3-SAT -> independent set: a triangle per clause, edges between complements
    is_to_clique / is_to_vc             complement graph; complement set
    sat_to_3col(n, clauses)             Karp's 3-colouring gadgets (palette triangle, variable pairs, OR gadgets)
    coloring_cnf(nv, edges, k)          k-colouring as CNF
    sat_to_subset_sum(n, clauses)       Sipser's digit construction; subset_from_model maps an assignment to numbers
    cook_levin(ntm, w, T)               the tableau CNF for a tiny NTM (cells x 2x3 windows), and decode_tableau
    savitch(adj, s, t, steps)           CANYIELD by midpoint recursion: (answer, calls, max depth)
    tqbf(quants, clauses)               evaluate a fully quantified CNF by recursion (counts nodes)
    geography(adj, start)               generalized geography: does the first player win? (memoized on visited set)
    pratt(p)                            a Pratt certificate that p is prime, and verify_pratt
    pythagorean_cnf(n)                  2-colour 1..n with no monochromatic a^2 + b^2 = c^2
    schur_cnf(n, k)                     k-colour 1..n with no monochromatic x + y = z
"""

from __future__ import annotations

import heapq
import itertools
import math
import random
from collections import defaultdict


# ----------------------------------------------------------------------------------------------- SAT

def check(model, clauses) -> bool:
    """``model`` maps variable -> bool (or is a list indexed by variable)."""
    get = model.get if isinstance(model, dict) else (lambda v: model[v])
    return all(any((get(abs(l)) if l > 0 else not get(abs(l))) for l in c) for c in clauses)


def _luby(i):
    k = 1
    while (1 << k) - 1 < i:
        k += 1
    while True:
        if i == (1 << k) - 1:
            return 1 << (k - 1)
        i -= (1 << (k - 1)) - 1
        k = 1
        while (1 << k) - 1 < i:
            k += 1


def cdcl(n, clauses, max_conflicts=None, seed=0, restart_base=100):
    """Returns (model as list of bools indexed 1..n, or None if unsatisfiable or out of budget, stats)."""
    stats = {"decisions": 0, "conflicts": 0, "propagations": 0, "learnt": 0, "restarts": 0, "status": "sat"}
    val = [0] * (n + 1)          # 0 unassigned, 1 true, -1 false
    level = [0] * (n + 1)
    reason = [None] * (n + 1)
    phase = [-1] * (n + 1)
    act = [0.0] * (n + 1)
    inc = 1.0
    trail, lim = [], []
    cls = []
    watches = defaultdict(list)
    rng = random.Random(seed)
    for v in range(1, n + 1):
        act[v] = rng.random() * 1e-5

    def value(l):
        x = val[abs(l)]
        return x if l > 0 else -x

    def enqueue(l, r):
        v = abs(l)
        val[v] = 1 if l > 0 else -1
        level[v] = len(lim)
        reason[v] = r
        trail.append(l)

    units = []
    for c in clauses:
        c = list(dict.fromkeys(c))
        if any(-l in c for l in c):
            continue
        if not c:
            stats["status"] = "unsat"
            return None, stats
        if len(c) == 1:
            units.append(c[0])
            continue
        ci = len(cls)
        cls.append(c)
        watches[c[0]].append(ci)
        watches[c[1]].append(ci)
    for l in units:
        if value(l) == -1:
            stats["status"] = "unsat"
            return None, stats
        if value(l) == 0:
            enqueue(l, None)

    qhead = 0

    def propagate():
        nonlocal qhead
        while qhead < len(trail):
            p = trail[qhead]
            qhead += 1
            fl = -p
            ws = watches[fl]
            keep = []
            i = 0
            while i < len(ws):
                ci = ws[i]
                i += 1
                c = cls[ci]
                if c[0] == fl:
                    c[0], c[1] = c[1], c[0]
                if value(c[0]) == 1:
                    keep.append(ci)
                    continue
                for k in range(2, len(c)):
                    if value(c[k]) != -1:
                        c[1], c[k] = c[k], c[1]
                        watches[c[1]].append(ci)
                        break
                else:
                    keep.append(ci)
                    if value(c[0]) == -1:
                        keep.extend(ws[i:])
                        watches[fl] = keep
                        return ci
                    enqueue(c[0], ci)
                    stats["propagations"] += 1
            watches[fl] = keep
        return None

    heap = [(-act[v], v) for v in range(1, n + 1)]
    heapq.heapify(heap)

    def bump(v):
        nonlocal inc
        act[v] += inc
        if act[v] > 1e100:
            for u in range(1, n + 1):
                act[u] *= 1e-100
            inc *= 1e-100
        heapq.heappush(heap, (-act[v], v))

    def backtrack(lv):
        nonlocal qhead
        if len(lim) <= lv:
            return
        cut = lim[lv]
        for l in trail[cut:]:
            v = abs(l)
            phase[v] = val[v]
            val[v] = 0
            reason[v] = None
            heapq.heappush(heap, (-act[v], v))
        del trail[cut:]
        del lim[lv:]
        qhead = len(trail)

    def analyze(ci):
        seen = set()
        learnt = [0]
        counter = 0
        p = None
        idx = len(trail) - 1
        cur = len(lim)
        c = cls[ci]
        while True:
            for q in (c if p is None else c[1:]):
                v = abs(q)
                if v not in seen and level[v] > 0:
                    seen.add(v)
                    bump(v)
                    if level[v] == cur:
                        counter += 1
                    else:
                        learnt.append(q)
            while abs(trail[idx]) not in seen:
                idx -= 1
            p = trail[idx]
            idx -= 1
            counter -= 1
            if counter == 0:
                break
            c = cls[reason[abs(p)]]
        learnt[0] = -p
        if len(learnt) == 1:
            return learnt, 0
        bi = max(range(1, len(learnt)), key=lambda i: level[abs(learnt[i])])
        learnt[1], learnt[bi] = learnt[bi], learnt[1]
        return learnt, level[abs(learnt[1])]

    if propagate() is not None:
        stats["status"] = "unsat"
        return None, stats
    restart_i, until = 1, restart_base * _luby(1)
    since = 0
    while True:
        confl = propagate()
        if confl is not None:
            stats["conflicts"] += 1
            since += 1
            if not lim:
                stats["status"] = "unsat"
                return None, stats
            learnt, bl = analyze(confl)
            backtrack(bl)
            if len(learnt) == 1:
                enqueue(learnt[0], None)
            else:
                ci = len(cls)
                cls.append(learnt)
                watches[learnt[0]].append(ci)
                watches[learnt[1]].append(ci)
                stats["learnt"] += 1
                enqueue(learnt[0], ci)
            inc /= 0.95
            if max_conflicts is not None and stats["conflicts"] >= max_conflicts:
                stats["status"] = "unknown"
                return None, stats
            continue
        if since >= until:
            stats["restarts"] += 1
            restart_i += 1
            until = restart_base * _luby(restart_i)
            since = 0
            backtrack(0)
            continue
        v = 0
        while heap:
            _, u = heapq.heappop(heap)
            if val[u] == 0:
                v = u
                break
        if v == 0:
            model = [False] + [val[u] == 1 for u in range(1, n + 1)]
            return model, stats
        stats["decisions"] += 1
        lim.append(len(trail))
        enqueue(v if phase[v] == 1 else -v, None)


def dpll(n, clauses, max_nodes=10 ** 7):
    """Plain DPLL with unit propagation and the first-unassigned-variable rule; returns (model or None, nodes)."""
    nodes = 0

    def simplify(cs, lit):
        out = []
        for c in cs:
            if lit in c:
                continue
            if -lit in c:
                c = [l for l in c if l != -lit]
                if not c:
                    return None
            out.append(c)
        return out

    def rec(cs, assign):
        nonlocal nodes
        nodes += 1
        if nodes > max_nodes:
            raise RuntimeError("budget")
        while True:
            unit = next((c[0] for c in cs if len(c) == 1), None)
            if unit is None:
                break
            assign[abs(unit)] = unit > 0
            cs = simplify(cs, unit)
            if cs is None:
                return None
        if not cs:
            return assign
        v = abs(cs[0][0])
        for lit in (v, -v):
            s = simplify(cs, lit)
            if s is not None:
                a = dict(assign)
                a[v] = lit > 0
                r = rec(s, a)
                if r is not None:
                    return r
        return None

    r = rec([list(c) for c in clauses], {})
    if r is None:
        return None, nodes
    return [False] + [r.get(v, False) for v in range(1, n + 1)], nodes


def random_ksat(n, m, k, rng):
    out = []
    for _ in range(m):
        vs = rng.sample(range(1, n + 1), k)
        out.append([v if rng.random() < 0.5 else -v for v in vs])
    return out


def to_3sat(n, clauses):
    """Split each clause longer than 3: (a b c d e) -> (a b y1)(-y1 c y2)(-y2 d e). Returns (n', clauses')."""
    out = []
    for c in clauses:
        if len(c) <= 3:
            out.append(list(c))
            continue
        n += 1
        out.append([c[0], c[1], n])
        for l in c[2:-2]:
            out.append([-n, l, n + 1])
            n += 1
        out.append([-n, c[-2], c[-1]])
    return n, out


# ----------------------------------------------------------------------------------------------- reductions

def sat_to_is(clauses):
    """Vertices (j, i) = the i-th literal of clause j; a triangle per clause and an edge between complementary
    literals. The formula is satisfiable iff the graph has an independent set of size len(clauses)."""
    verts = [(j, i) for j, c in enumerate(clauses) for i in range(len(c))]
    lit = {(j, i): clauses[j][i] for (j, i) in verts}
    edges = set()
    for j, c in enumerate(clauses):
        for a, b in itertools.combinations(range(len(c)), 2):
            edges.add(((j, a), (j, b)))
    for u, v in itertools.combinations(verts, 2):
        if lit[u] == -lit[v]:
            edges.add((u, v))
    return verts, sorted(edges), lit, len(clauses)


def is_from_model(clauses, model):
    """One true literal per clause: an independent set of size m."""
    out = []
    for j, c in enumerate(clauses):
        i = next(i for i, l in enumerate(c) if (model[abs(l)] if l > 0 else not model[abs(l)]))
        out.append((j, i))
    return out


def is_to_clique(verts, edges):
    es = set(edges) | {(b, a) for a, b in edges}
    return [(u, v) for u, v in itertools.combinations(verts, 2) if (u, v) not in es]


def is_independent(S, edges):
    s = set(S)
    return not any(u in s and v in s for u, v in edges)


def is_to_vc(verts, S):
    s = set(S)
    return [v for v in verts if v not in s]


def is_cover(C, edges):
    c = set(C)
    return all(u in c or v in c for u, v in edges)


def sat_to_3col(n, clauses):
    """Vertices: T, F, B (the palette triangle); x_v and ~x_v for each variable, joined to each other and to B;
    for each clause (a, b, c) an OR gadget of six vertices whose output is joined to F and B, so the output can be
    coloured T iff some input is. Returns (vertex names, edges)."""
    V = ["T", "F", "B"]
    E = [("T", "F"), ("F", "B"), ("B", "T")]
    for v in range(1, n + 1):
        V += [f"x{v}", f"~x{v}"]
        E += [(f"x{v}", f"~x{v}"), (f"x{v}", "B"), (f"~x{v}", "B")]

    def node(l):
        return f"x{l}" if l > 0 else f"~x{-l}"

    for j, c in enumerate(clauses):
        a, b, cc = (list(c) + [c[-1]] * 3)[:3]
        # or(a, b) = o1 through u1, w1; or(o1, c) = o2 through u2, w2
        u1, w1, o1, u2, w2, o2 = (f"g{j}_{k}" for k in ("u1", "w1", "o1", "u2", "w2", "o2"))
        V += [u1, w1, o1, u2, w2, o2]
        E += [(node(a), u1), (node(b), w1), (u1, w1), (u1, o1), (w1, o1),
              (o1, u2), (node(cc), w2), (u2, w2), (u2, o2), (w2, o2),
              (o2, "F"), (o2, "B")]
    return V, E


def coloring_cnf(V, E, k):
    idx = {v: i for i, v in enumerate(V)}
    var = lambda v, c: idx[v] * k + c + 1  # noqa: E731
    cl = []
    for v in V:
        cl.append([var(v, c) for c in range(k)])
        for a, b in itertools.combinations(range(k), 2):
            cl.append([-var(v, a), -var(v, b)])
    for u, v in E:
        for c in range(k):
            cl.append([-var(u, c), -var(v, c)])
    return len(V) * k, cl, var


def decode_coloring(V, model, var, k):
    return {v: next(c for c in range(k) if model[var(v, c)]) for v in V}


def sat_to_subset_sum(n, clauses):
    """Sipser's construction (Theorem 7.56). Numbers are decimal strings of n + m digits: y_i / z_i put 1 in
    variable column i and 1 in each clause column where x_i / ~x_i occurs; g_j and h_j put 1 in clause column j.
    Target: n ones then m threes. No column can carry (at most 5 ones per column)."""
    m = len(clauses)
    nums = {}
    for i in range(1, n + 1):
        y = [0] * (n + m)
        z = [0] * (n + m)
        y[i - 1] = z[i - 1] = 1
        for j, c in enumerate(clauses):
            if i in c:
                y[n + j] = 1
            if -i in c:
                z[n + j] = 1
        nums[f"y{i}"] = int("".join(map(str, y)))
        nums[f"z{i}"] = int("".join(map(str, z)))
    for j in range(m):
        g = [0] * (n + m)
        g[n + j] = 1
        nums[f"g{j + 1}"] = nums[f"h{j + 1}"] = int("".join(map(str, g)))
        nums[f"h{j + 1}"] = nums[f"g{j + 1}"]
    target = int("1" * n + "3" * m)
    return nums, target


def subset_from_model(n, clauses, model, nums):
    chosen = [f"y{i}" if model[i] else f"z{i}" for i in range(1, n + 1)]
    for j, c in enumerate(clauses):
        true = sum(1 for l in c if (model[abs(l)] if l > 0 else not model[abs(l)]))
        if true <= 2:
            chosen.append(f"g{j + 1}")
        if true <= 1:
            chosen.append(f"h{j + 1}")
    return chosen


# ----------------------------------------------------------------------------------------------- Cook-Levin

def cook_levin(ntm, w, T):
    """The Cook-Levin tableau as CNF. ``ntm`` = dict(states, start, accept, blank, alphabet, delta) where delta maps
    (state, symbol) -> list of (state', write, move in {-1, +1}). A tableau row is a configuration of width
    W = T + 2 cells plus a '#' border on each side; a cell holds a tape symbol or a (state, symbol) pair marking the
    head. Row 0 is the start configuration, and every 2 x 3 window must be legal. The accept state is absorbing
    (it rewrites nothing and stays put), so the formula is satisfiable iff the machine accepts w within T - 1 steps.
    Returns (number of variables, clauses, info) where info decodes a model."""
    gam = list(ntm["alphabet"])
    states = list(ntm["states"])
    cells = ["#"] + gam + [(q, a) for q in states for a in gam]
    W = T + 2
    cols = W + 2                       # including the two borders
    C = len(cells)
    cid = {c: i for i, c in enumerate(cells)}
    var = lambda r, j, s: (r * cols + j) * C + cid[s] + 1  # noqa: E731
    nv = T * cols * C
    cl = []
    # cell: exactly one symbol per cell
    for r in range(T):
        for j in range(cols):
            cl.append([var(r, j, s) for s in cells])
            for a, b in itertools.combinations(cells, 2):
                cl.append([-var(r, j, a), -var(r, j, b)])
    # borders
    for r in range(T):
        cl.append([var(r, 0, "#")])
        cl.append([var(r, cols - 1, "#")])
    # start row
    start = [(ntm["start"], w[0] if w else ntm["blank"])] + list(w[1:]) + [ntm["blank"]] * (W - max(len(w), 1))
    for j, s in enumerate(start):
        cl.append([var(0, j + 1, s)])
    # accept: some cell in the last row holds the accept state
    acc = ntm["accept"]
    cl.append([var(T - 1, j, (acc, a)) for j in range(1, cols - 1) for a in gam])
    # windows: for each position, one auxiliary variable per legal window that fits the borders there; the
    # auxiliary variable implies its six cells, and some auxiliary variable must hold (Tseitin's encoding)
    legal = legal_windows(ntm, cells)
    aux = nv
    per = []
    for r in range(T - 1):
        for j in range(cols - 2):
            fits = [wd for wd in legal if _border_ok(wd[0], j, cols) and _border_ok(wd[1], j, cols)]
            ys = []
            for top, bot in fits:
                aux += 1
                ys.append(aux)
                for k in range(3):
                    cl.append([-aux, var(r, j + k, top[k])])
                    cl.append([-aux, var(r + 1, j + k, bot[k])])
            cl.append(ys)
            per.append(len(fits))
    nv = aux
    info = {"cells": cells, "cols": cols, "T": T, "var": var, "legal": len(legal), "per_position": per}
    return nv, cl, info


def _border_ok(win, j, cols):
    """'#' may appear only at the absolute border columns."""
    for k, s in enumerate(win):
        col = j + k
        if (s == "#") != (col == 0 or col == cols - 1):
            return False
    return True


def legal_windows(ntm, cells):
    """All 2 x 3 windows that can appear in consecutive rows: generated from every 5-cell top fragment with at most
    one head (a head two cells away can still move into the middle three)."""
    gam = list(ntm["alphabet"])
    syms = ["#"] + gam
    acc = ntm["accept"]
    out = set()
    heads = [(q, a) for q in ntm["states"] for a in gam]

    def succ(frag):
        hs = [i for i, c in enumerate(frag) if isinstance(c, tuple)]
        if not hs:
            return [list(frag)]
        i = hs[0]
        q, a = frag[i]
        if q == acc:
            return [list(frag)]
        res = []
        for (q2, b, mv) in ntm["delta"].get((q, a), []):
            f = list(frag)
            f[i] = b
            k = i + mv
            if 0 <= k < len(f):
                if f[k] == "#":
                    continue
                f[k] = (q2, f[k])
            res.append(f)
        return res

    for pos in range(-1, 5):
        for base in itertools.product(syms, repeat=5):
            for h in (heads if 0 <= pos < 5 else [None]):
                frag = list(base)
                if h is not None:
                    if frag[pos] == "#":
                        continue
                    if frag[pos] != h[1]:
                        continue
                    frag[pos] = h
                for s in succ(frag):
                    out.add((tuple(frag[1:4]), tuple(s[1:4])))
    return out


def decode_tableau(model, info):
    cells, cols, T, var = info["cells"], info["cols"], info["T"], info["var"]
    rows = []
    for r in range(T):
        row = []
        for j in range(cols):
            row.append(next(s for s in cells if model[var(r, j, s)]))
        rows.append(row)
    return rows


# ----------------------------------------------------------------------------------------------- space

def savitch(adj, s, t, steps):
    """CANYIELD(s, t, steps): reachable within ``steps`` edges, by trying every midpoint. Returns (answer, calls,
    max recursion depth). Space is depth x (one configuration), so O(log^2) for a configuration graph."""
    calls = 0
    deepest = 0
    V = list(adj)

    def can(a, b, k, d):
        nonlocal calls, deepest
        calls += 1
        deepest = max(deepest, d)
        if k <= 1:
            return a == b or b in adj[a]
        h = (k + 1) // 2
        return any(can(a, m, h, d + 1) and can(m, b, k - h, d + 1) for m in V)

    return can(s, t, steps, 1), calls, deepest


def tqbf(quants, clauses):
    """quants: list of ('E' or 'A', var) in order; evaluate by recursion. Returns (value, nodes)."""
    nodes = 0

    def rec(i, assign):
        nonlocal nodes
        nodes += 1
        if i == len(quants):
            return all(any(assign[abs(l)] == (l > 0) for l in c) for c in clauses)
        q, v = quants[i]
        a0 = rec(i + 1, {**assign, v: False})
        if q == "E" and a0:
            return True
        if q == "A" and not a0:
            return False
        return rec(i + 1, {**assign, v: True})

    return rec(0, {}), nodes


def geography(adj, start):
    """Generalized geography: players alternately move a token along an edge to a vertex not yet visited; whoever
    cannot move loses. Returns (first player to move wins?, positions evaluated). Player 1 has just placed the token
    at ``start``; it is player 2's move."""
    memo = {}

    def wins(v, visited):          # does the player to move win?
        key = (v, visited)
        if key in memo:
            return memo[key]
        r = any(not wins(u, visited | (1 << u)) for u in adj[v] if not visited >> u & 1)
        memo[key] = r
        return r

    r = wins(start, 1 << start)
    return (not r), len(memo)


# ----------------------------------------------------------------------------------------------- NP and coNP

def _factor(n):
    out, d = [], 2
    while d * d <= n:
        while n % d == 0:
            out.append(d)
            n //= d
        d += 1 if d == 2 else 2
    if n > 1:
        out.append(n)
    return sorted(set(out))


def pratt(p):
    """A Pratt certificate: a witness g of order p - 1, the prime factors of p - 1, and certificates for each."""
    if p == 2:
        return {"p": 2}
    fs = _factor(p - 1)
    g = 2
    while not all(pow(g, (p - 1) // q, p) != 1 for q in fs):
        g += 1
    return {"p": p, "g": g, "factors": [pratt(q) for q in fs]}


def verify_pratt(cert):
    p = cert["p"]
    if p == 2:
        return True, 1
    g = cert["g"]
    qs = [c["p"] for c in cert["factors"]]
    m = p - 1
    for q in qs:
        while m % q == 0:
            m //= q
    ok = m == 1 and pow(g, p - 1, p) == 1 and all(pow(g, (p - 1) // q, p) != 1 for q in qs)
    checks = 1
    for c in cert["factors"]:
        o, k = verify_pratt(c)
        ok = ok and o
        checks += k
    return ok, checks


# ----------------------------------------------------------------------------------------------- famous instances

def pythagorean_cnf(n):
    """Variable i: colour of i. For each a^2 + b^2 = c^2 with c <= n, not all three the same colour."""
    cl = []
    for a in range(1, n + 1):
        for b in range(a, n + 1):
            c2 = a * a + b * b
            c = math.isqrt(c2)
            if c > n:
                break
            if c * c == c2:
                cl.append([a, b, c])
                cl.append([-a, -b, -c])
    return n, cl


def schur_cnf(n, k):
    var = lambda i, c: (i - 1) * k + c + 1  # noqa: E731
    cl = []
    for i in range(1, n + 1):
        cl.append([var(i, c) for c in range(k)])
    for x in range(1, n + 1):
        for y in range(x, n + 1 - x):
            z = x + y
            for c in range(k):
                cl.append(list(dict.fromkeys([-var(x, c), -var(y, c), -var(z, c)])))
    # symmetry breaking: colour 1 gets 0
    cl.append([var(1, 0)])
    return n * k, cl
