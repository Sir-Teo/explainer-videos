"""Instruments for Part 27 (Proofs and Randomness).

    binom_tail(k, p, at_least)            exact P[Bin(k, p) >= at_least]: amplification by majority vote
    fingerprint_eq(x, y, q, rng)          equality of two bit strings by evaluating them as polynomials over GF(q)
    dnf_random(n, terms, width, rng)      a random width-w DNF; restrict(dnf, rho); dt_depth(f, n) exact
    arithmetize / sumcheck(...)           the sum-check protocol for #SAT over GF(p), honest and cheating provers
    gni_round(G0, G1, rng)                one round of the graph non-isomorphism protocol
    zk_colouring(...)                     GMW's zero-knowledge protocol for 3-colouring with hash commitments
    blr_rejection(f, n)                   the exact rejection probability of the BLR linearity test
    walksat(n, clauses, rng, flips)       local search for MAX-SAT
    vc_branch / buss_kernel               FPT vertex cover: bounded search tree and Buss's kernel
    permanent_ryser / det_bareiss         the permanent in O(2^n n) and the determinant in O(n^3), exactly
    ov_brute / three_sum                  orthogonal vectors and 3SUM, the fine-grained baselines
"""

from __future__ import annotations

import hashlib
import itertools
import math
from fractions import Fraction


# ----------------------------------------------------------------------------------------------- randomness

def binom_tail(k, p, at_least):
    """Computed in log space, so large k does not overflow."""
    lp, lq = math.log(p), math.log(1 - p)
    terms = [math.lgamma(k + 1) - math.lgamma(i + 1) - math.lgamma(k - i + 1) + i * lp + (k - i) * lq
             for i in range(at_least, k + 1)]
    if not terms:
        return 0.0
    m = max(terms)
    return math.exp(m) * sum(math.exp(t - m) for t in terms)


def is_prime(n):
    if n < 2:
        return False
    for q in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % q == 0:
            return n == q
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for a in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def next_prime(n):
    while not is_prime(n):
        n += 1
    return n


def poly_eval(bits, r, q):
    """The string as a polynomial b_0 + b_1 r + ... over GF(q), by Horner's rule."""
    acc = 0
    for b in reversed(bits):
        acc = (acc * r + b) % q
    return acc


def fingerprint_eq(x, y, q, rng):
    """Alice sends (r, x(r)); Bob compares with y(r). Returns (says equal?, bits sent)."""
    r = rng.randrange(q)
    return poly_eval(x, r, q) == poly_eval(y, r, q), 2 * q.bit_length()


# ----------------------------------------------------------------------------------------------- switching lemma

def dnf_random(n, terms, width, rng):
    out = []
    for _ in range(terms):
        vs = rng.sample(range(n), width)
        out.append(tuple((v, rng.random() < 0.5) for v in vs))
    return out


def dnf_eval(dnf, x):
    return any(all(x[v] == b for v, b in t) for t in dnf)


def restrict(dnf, rho):
    """rho maps variable -> 0/1 (fixed) or is absent (free). Returns the simplified DNF (True if a term is satisfied,
    False if no terms survive)."""
    out = []
    for t in dnf:
        keep = []
        dead = False
        for v, b in t:
            if v in rho:
                if rho[v] != b:
                    dead = True
                    break
            else:
                keep.append((v, b))
        if dead:
            continue
        if not keep:
            return True
        out.append(tuple(keep))
    return out if out else False


def truth_table(f, free):
    """f: DNF (or True / False) over the variables in ``free``; returns the table as a tuple."""
    if f is True or f is False:
        return tuple([bool(f)] * (1 << len(free)))
    idx = {v: i for i, v in enumerate(free)}
    tab = []
    for m in range(1 << len(free)):
        x = {v: bool(m >> idx[v] & 1) for v in free}
        tab.append(any(all(x[v] == b for v, b in t) for t in f))
    return tuple(tab)


def dt_depth(tab, k):
    """Exact decision-tree depth of a Boolean function on k variables given as a truth table (memoized)."""
    memo = {}

    def rec(t, vars_):
        if all(t) or not any(t):
            return 0
        key = (t, vars_)
        if key in memo:
            return memo[key]
        best = len(vars_)
        for i, v in enumerate(vars_):
            rest = vars_[:i] + vars_[i + 1:]
            t0 = tuple(t[m] for m in range(len(t)) if not (m >> i & 1))
            t1 = tuple(t[m] for m in range(len(t)) if m >> i & 1)
            best = min(best, 1 + max(rec(t0, rest), rec(t1, rest)))
            if best == 1:
                break
        memo[key] = best
        return best

    return rec(tab, tuple(range(k)))


def random_restriction(n, p, rng):
    rho = {}
    for v in range(n):
        if rng.random() >= p:
            rho[v] = rng.random() < 0.5
    return rho


# ----------------------------------------------------------------------------------------------- sum-check

def lit_val(l, x, p):
    v = x[abs(l) - 1] % p
    return v if l > 0 else (1 - v) % p


def arith_eval(clauses, x, p):
    """The arithmetized CNF at a point of GF(p)^n: prod over clauses of 1 - prod(1 - literal)."""
    acc = 1
    for c in clauses:
        t = 1
        for l in c:
            t = t * (1 - lit_val(l, x, p)) % p
        acc = acc * (1 - t) % p
    return acc


def lagrange_eval(ys, r, p):
    """Evaluate the polynomial through (0, ys[0]), (1, ys[1]), ... at r, over GF(p)."""
    d = len(ys)
    total = 0
    for i, y in enumerate(ys):
        num, den = 1, 1
        for j in range(d):
            if j != i:
                num = num * (r - j) % p
                den = den * (i - j) % p
        total = (total + y * num * pow(den, p - 2, p)) % p
    return total


def honest_message(clauses, n, p, prefix, deg):
    """g_i(X) = sum over boolean suffixes of the arithmetized formula with x_1..x_{i-1} = prefix, x_i = X; sent as its
    values at X = 0, 1, ..., deg."""
    i = len(prefix)
    rest = n - i - 1
    ys = []
    for X in range(deg + 1):
        s = 0
        for suf in itertools.product((0, 1), repeat=rest):
            s += arith_eval(clauses, list(prefix) + [X] + list(suf), p)
        ys.append(s % p)
    return ys


def sumcheck(clauses, n, p, claim, rng, cheat=False):
    """Run the protocol. The prover claims ``claim`` satisfying assignments (mod p). An honest prover sends the true
    g_i. A cheating prover, while its current claim is false, sends g_i + d with d(0) + d(1) = the error and d having
    deg - 1 extra roots, hoping the verifier's random point is one of them. Returns (accepted, rounds, log)."""
    deg = len(clauses)
    cur = claim % p
    prefix = []
    log = []
    for i in range(n):
        g = honest_message(clauses, n, p, prefix, deg)
        if cheat:
            err = (cur - (g[0] + g[1])) % p
            if err:
                # d(X) = err * X * prod_{j=2..deg}(X - j) / prod_{j=2..deg}(1 - j): d(0) = 0, d(1) = err
                den = 1
                for j in range(2, deg + 1):
                    den = den * (1 - j) % p
                scale = err * pow(den, p - 2, p) % p
                for X in range(deg + 1):
                    d = scale * X
                    for j in range(2, deg + 1):
                        d = d * (X - j) % p
                    g[X] = (g[X] + d) % p
        if (g[0] + g[1]) % p != cur:
            log.append({"round": i + 1, "check": False})
            return False, i + 1, log
        r = rng.randrange(p)
        cur = lagrange_eval(g, r, p)
        prefix.append(r)
        log.append({"round": i + 1, "g": g, "r": r, "next": cur})
    final = arith_eval(clauses, prefix, p)
    ok = final == cur
    log.append({"final": final, "claim": cur, "ok": ok})
    return ok, n, log


def count_sat(clauses, n):
    return sum(1 for a in itertools.product((False, True), repeat=n)
               if all(any(a[abs(l) - 1] == (l > 0) for l in c) for c in clauses))


# ----------------------------------------------------------------------------------------------- interaction

def permute_graph(edges, perm):
    return frozenset(frozenset((perm[u], perm[v])) for u, v in edges)


def isomorphic(e1, e2, n):
    s2 = frozenset(frozenset(e) for e in e2)
    for perm in itertools.permutations(range(n)):
        if permute_graph(e1, perm) == s2:
            return True
    return False


def gni_round(G0, G1, n, rng):
    """Verifier picks b and a random relabelling of G_b; the all-powerful prover says which graph it came from (it
    checks isomorphism with G0 by brute force; if both match, it guesses). Returns (b, answer)."""
    b = rng.randrange(2)
    perm = list(range(n))
    rng.shuffle(perm)
    H = permute_graph(G1 if b else G0, perm)
    m0 = isomorphic(G0, H, n)
    m1 = isomorphic(G1, H, n)
    if m0 and not m1:
        ans = 0
    elif m1 and not m0:
        ans = 1
    else:
        ans = rng.randrange(2)
    return b, ans


def commit(value, rng):
    nonce = rng.getrandbits(128).to_bytes(16, "big")
    return hashlib.sha256(nonce + bytes([value])).hexdigest(), nonce


def zk_colouring(n, edges, colouring, rounds, rng):
    """GMW: each round the prover permutes the three colours at random, commits to every vertex's colour, and opens
    the two ends of an edge the verifier picks. Returns (caught in round or None, revealed pairs)."""
    revealed = []
    for k in range(rounds):
        pi = [0, 1, 2]
        rng.shuffle(pi)
        col = [pi[c] for c in colouring]
        coms = [commit(c, rng) for c in col]
        u, v = edges[rng.randrange(len(edges))]
        # the verifier checks the openings against the commitments
        for w in (u, v):
            h, nonce = coms[w]
            assert hashlib.sha256(nonce + bytes([col[w]])).hexdigest() == h
        revealed.append((col[u], col[v]))
        if col[u] == col[v]:
            return k + 1, revealed
    return None, revealed


def zk_simulate(rounds, rng):
    """The simulator's transcript: a uniformly random pair of distinct colours for a random edge."""
    out = []
    for _ in range(rounds):
        a = rng.randrange(3)
        b = (a + 1 + rng.randrange(2)) % 3
        out.append((a, b))
    return out


# ----------------------------------------------------------------------------------------------- PCP flavour

def blr_rejection(f, n):
    """f: list of 2^n bits. Exact probability that f(x) + f(y) != f(x xor y) over uniform x, y."""
    N = 1 << n
    bad = 0
    for x in range(N):
        fx = f[x]
        for y in range(N):
            if fx ^ f[y] != f[x ^ y]:
                bad += 1
    return bad / (N * N)


def distance_to_linear(f, n):
    N = 1 << n
    best = N
    for a in range(N):
        d = sum(1 for x in range(N) if f[x] != (bin(a & x).count("1") & 1))
        best = min(best, d)
    return best / N


def walksat(n, clauses, rng, flips=20000, noise=0.5):
    """Local search for MAX-SAT; returns the best number of satisfied clauses seen and the assignment."""
    a = [False] + [rng.random() < 0.5 for _ in range(n)]

    def sat(c):
        return any(a[abs(l)] == (l > 0) for l in c)

    unsat = [c for c in clauses if not sat(c)]
    best = len(clauses) - len(unsat)
    best_a = a[:]
    occ = {}
    for i, c in enumerate(clauses):
        for l in c:
            occ.setdefault(abs(l), []).append(i)
    for _ in range(flips):
        if not unsat:
            break
        c = unsat[rng.randrange(len(unsat))]
        if rng.random() < noise:
            v = abs(rng.choice(c))
        else:
            def breaks(v):
                a[v] = not a[v]
                b = sum(1 for i in occ.get(v, []) if not sat(clauses[i]))
                a[v] = not a[v]
                return b
            v = min((abs(l) for l in c), key=breaks)
        a[v] = not a[v]
        unsat = [c for c in clauses if not sat(c)] if len(clauses) < 2000 else [c for c in clauses if not sat(c)]
        if len(clauses) - len(unsat) > best:
            best = len(clauses) - len(unsat)
            best_a = a[:]
    return best, best_a


# ----------------------------------------------------------------------------------------------- parameterized

def vc_branch(edges, k):
    """Bounded search tree: pick an uncovered edge (u, v); one of them is in the cover. Returns (cover or None,
    nodes)."""
    nodes = 0

    def rec(es, k, chosen):
        nonlocal nodes
        nodes += 1
        if not es:
            return chosen
        if k == 0:
            return None
        u, v = es[0]
        for w in (u, v):
            r = rec([e for e in es if w not in e], k - 1, chosen + [w])
            if r is not None:
                return r
        return None

    return rec(list(edges), k, []), nodes


def buss_kernel(edges, k):
    """A vertex of degree > k must be in any cover of size <= k; after taking them all, more than k^2 edges left
    means no. Returns (forced vertices, remaining edges, remaining k) or None if impossible."""
    es = [tuple(e) for e in edges]
    forced = []
    changed = True
    while changed:
        changed = False
        deg = {}
        for u, v in es:
            deg[u] = deg.get(u, 0) + 1
            deg[v] = deg.get(v, 0) + 1
        for w, d in deg.items():
            if d > k:
                forced.append(w)
                es = [e for e in es if w not in e]
                k -= 1
                changed = True
                break
        if k < 0:
            return None
    if len(es) > k * k:
        return None
    return forced, es, k


def vc_brute(edges, n, k):
    tried = 0
    for S in itertools.combinations(range(n), k):
        tried += 1
        s = set(S)
        if all(u in s or v in s for u, v in edges):
            return list(S), tried
    return None, tried


# ----------------------------------------------------------------------------------------------- counting

def permanent_ryser(A):
    """Ryser's formula with Gray-code updates: O(2^n n)."""
    n = len(A)
    total = 0
    rowsum = [0] * n
    prev = 0
    for k in range(1, 1 << n):
        g = k ^ (k >> 1)
        diff = g ^ prev
        j = diff.bit_length() - 1
        add = 1 if g >> j & 1 else -1
        for i in range(n):
            rowsum[i] += add * A[i][j]
        prev = g
        prod = 1
        for i in range(n):
            prod *= rowsum[i]
            if prod == 0:
                break
        bits = bin(g).count("1")
        total += (-1) ** bits * prod
    return total * (-1) ** n


def permanent_brute(A):
    n = len(A)
    return sum(math.prod(A[i][s[i]] for i in range(n)) for s in itertools.permutations(range(n)))


def det_bareiss(A):
    """Exact integer determinant by fraction-free elimination, O(n^3)."""
    M = [row[:] for row in A]
    n = len(M)
    sign, prev = 1, 1
    for k in range(n - 1):
        if M[k][k] == 0:
            sw = next((i for i in range(k + 1, n) if M[i][k] != 0), None)
            if sw is None:
                return 0
            M[k], M[sw] = M[sw], M[k]
            sign = -sign
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                M[i][j] = (M[i][j] * M[k][k] - M[i][k] * M[k][j]) // prev
        prev = M[k][k]
    return sign * M[n - 1][n - 1]


# ----------------------------------------------------------------------------------------------- fine-grained

def ov_brute(A, B):
    """Is there a in A, b in B with a . b = 0 (vectors as int bitmasks)? O(n^2) word operations."""
    for a in A:
        for b in B:
            if a & b == 0:
                return True
    return False


def three_sum(xs):
    """O(n^2): sort, then two pointers for each first element. Returns a triple summing to 0 or None."""
    s = sorted(xs)
    n = len(s)
    for i in range(n - 2):
        lo, hi = i + 1, n - 1
        while lo < hi:
            t = s[i] + s[lo] + s[hi]
            if t == 0:
                return s[i], s[lo], s[hi]
            if t < 0:
                lo += 1
            else:
                hi -= 1
    return None


def fraction_str(x):
    return str(Fraction(x).limit_denominator(10 ** 6))


# ----------------------------------------------------------------------------------------------- average case

def planted_clique(n, k, rng):
    """G(n, 1/2) with a clique planted on k random vertices: (adjacency as a list of int bitmasks, planted set)."""
    adj = [0] * n
    for u in range(n):
        for v in range(u + 1, n):
            if rng.random() < 0.5:
                adj[u] |= 1 << v
                adj[v] |= 1 << u
    S = set(rng.sample(range(n), k))
    for u in S:
        for v in S:
            if u != v:
                adj[u] |= 1 << v
    return adj, S


def degree_recover(adj, k):
    """Kucera's degree heuristic plus one clean-up round: the k highest-degree vertices, then every vertex
    adjacent to at least 3k/4 of them. Returns a set of k vertices (or fewer)."""
    n = len(adj)
    deg = [bin(a).count("1") for a in adj]
    top = sorted(range(n), key=lambda v: -deg[v])[:k]
    mask = 0
    for v in top:
        mask |= 1 << v
    score = [bin(adj[v] & mask).count("1") + ((mask >> v) & 1) for v in range(n)]
    return set(sorted(range(n), key=lambda v: -score[v])[:k])


def pollard_rho(n, rng):
    """A non-trivial factor of composite n by Pollard's rho with Brent's cycle detection; also the steps taken."""
    if n % 2 == 0:
        return 2, 1
    steps = 0
    while True:
        y, c, m = rng.randrange(1, n), rng.randrange(1, n), 128
        g, r, q = 1, 1, 1
        while g == 1:
            x = y
            for _ in range(r):
                y = (y * y + c) % n
            k = 0
            while k < r and g == 1:
                ys = y
                for _ in range(min(m, r - k)):
                    y = (y * y + c) % n
                    q = q * abs(x - y) % n
                    steps += 1
                g = math.gcd(q, n)
                k += m
            r *= 2
        if g == n:
            g = 1
            while g == 1:
                ys = (ys * ys + c) % n
                g = math.gcd(abs(x - ys), n)
                steps += 1
        if g != n:
            return g, steps


# ----------------------------------------------------------------------------------------------- unique games

def ug_instance(n, m, k, eps, rng):
    """A unique game on n vertices and m random edges over Z_k: each edge (a, b, c) demands x_b = x_a + c (mod k).
    Constraints agree with a planted labelling except on a random eps fraction, which get a wrong shift."""
    planted = [rng.randrange(k) for _ in range(n)]
    edges, seen = [], set()
    # a random spanning path first, so the graph is connected
    order = list(range(n))
    rng.shuffle(order)
    pairs = list(zip(order, order[1:]))
    while len(pairs) < m:
        a, b = rng.sample(range(n), 2)
        if (a, b) not in seen and (b, a) not in seen:
            pairs.append((a, b))
            seen.add((a, b))
    rng.shuffle(pairs)
    bad = set(rng.sample(range(m), round(eps * m)))
    for i, (a, b) in enumerate(pairs[:m]):
        c = (planted[b] - planted[a]) % k
        if i in bad:
            c = (c + rng.randrange(1, k)) % k
        edges.append((a, b, c))
    return edges, planted


def ug_value(edges, x, k):
    return sum((x[b] - x[a] - c) % k == 0 for a, b, c in edges) / len(edges)


def ug_propagate(n, edges, k, root):
    """Fix the root's label to 0 and propagate along a BFS tree (each label is then forced): the easy algorithm."""
    adj = [[] for _ in range(n)]
    for a, b, c in edges:
        adj[a].append((b, c))
        adj[b].append((a, -c))
    x = [None] * n
    x[root] = 0
    queue = [root]
    for u in queue:
        for v, c in adj[u]:
            if x[v] is None:
                x[v] = (x[u] + c) % k
                queue.append(v)
    return [0 if t is None else t for t in x]


# ----------------------------------------------------------------------------------------------- SAT to OV

def sat_to_ov(clauses, n):
    """Williams' reduction: split the variables into halves; each half-assignment becomes a bit vector with bit j set
    iff that half does NOT satisfy clause j. A pair is orthogonal iff together the halves satisfy every clause."""
    h = n // 2
    halves = [list(range(1, h + 1)), list(range(h + 1, n + 1))]
    out = []
    for vars_ in halves:
        vs = set(vars_)
        vecs = []
        for bits in range(1 << len(vars_)):
            val = {v: (bits >> i) & 1 for i, v in enumerate(vars_)}
            vec = 0
            for j, cl in enumerate(clauses):
                if not any(abs(l) in vs and val[abs(l)] == (l > 0) for l in cl):
                    vec |= 1 << j
            vecs.append(vec)
        out.append(vecs)
    return out[0], out[1]


# ----------------------------------------------------------------------------------------------- identity testing

def det_mod(A, p):
    """Determinant mod a prime p by Gaussian elimination: O(n^3) field operations."""
    A = [[x % p for x in row] for row in A]
    n, det = len(A), 1
    for c in range(n):
        piv = next((r for r in range(c, n) if A[r][c]), None)
        if piv is None:
            return 0
        if piv != c:
            A[c], A[piv] = A[piv], A[c]
            det = -det
        det = det * A[c][c] % p
        inv = pow(A[c][c], p - 2, p)
        for r in range(c + 1, n):
            f = A[r][c] * inv % p
            if f:
                A[r] = [(a - f * b) % p for a, b in zip(A[r], A[c])]
    return det % p


def vandermonde_test(xs, p, wrong=False):
    """Does det[x_i^j] equal prod_{i<j} (x_j - x_i) at this point, mod p? With wrong=True the product's first
    factor is replaced by (x_1 + x_0), a false identity."""
    n = len(xs)
    lhs = det_mod([[pow(x, j, p) for j in range(n)] for x in xs], p)
    rhs = 1
    for j in range(n):
        for i in range(j):
            f = (xs[j] + xs[i]) if (wrong and (i, j) == (0, 1)) else (xs[j] - xs[i])
            rhs = rhs * f % p
    return lhs == rhs
