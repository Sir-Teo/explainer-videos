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
import functools
import itertools
import math
from fractions import Fraction



class _RhoBudget(Exception):
    pass

def _integer(value, name, minimum=0):
    if type(value) is not int or (minimum is not None and value<minimum):
        raise ValueError(f'{name} must be an integer'+('' if minimum is None else f' >= {minimum}'))
    return value

def _probability(p):
    if not isinstance(p,(float,int)) or isinstance(p,bool) or not math.isfinite(p) or not 0<=p<=1:
        raise ValueError('probability must be finite and in [0,1]')

@functools.lru_cache(maxsize=128)
def _field(p):
    if type(p) is not int or not is_prime(p): raise ValueError('prime field required with p < 2**64')
    return p

def _bit_values(xs):
    if any(type(v) not in (bool,int) or v not in (0,1) for v in xs): raise ValueError('Boolean values required')

def _table(f,n):
    _integer(n,'n'); _bit_values(f)
    if len(f)!=1<<n: raise ValueError('truth table must have 2**n entries')

def _cnf(clauses,n):
    _integer(n,'n'); clauses=[list(c) for c in clauses]
    if any(type(l) is not int or l==0 or abs(l)>n for c in clauses for l in c): raise ValueError('CNF literals must be nonzero integers in 1..n')
    return clauses

def _edges(edges,n=None):
    if n is not None: _integer(n,'n')
    edges=[tuple(e) for e in edges]
    if any(len(e)!=2 or any(type(v) is not int or v<0 or (n is not None and v>=n) for v in e) or e[0]==e[1] for e in edges):
        raise ValueError('simple graph edges need distinct nonnegative vertices in the domain')
    return sorted({tuple(sorted(e)) for e in edges})

def _dnf(dnf):
    out=[]
    for term in dnf:
        row=[]
        for v,b in term:
            _integer(v,'DNF variable')
            if type(b) not in (bool,int) or b not in (0,1): raise ValueError('DNF literal values must be Boolean')
            row.append((v,bool(b)))
        out.append(tuple(dict.fromkeys(row)))
    return out

def _square(A):
    A=[list(r) for r in A]; n=len(A)
    if any(len(r)!=n or any(type(v) is not int for v in r) for r in A): raise ValueError('square integer matrix required')
    return A

# ----------------------------------------------------------------------------------------------- randomness

def binom_tail(k, p, at_least):
    """Numerically evaluated binomial tail; endpoints and integer domains explicit."""
    _integer(k, 'k'); _integer(at_least, 'at_least', minimum=None); _probability(p)
    if at_least <= 0: return 1.0
    if at_least > k: return 0.0
    if p == 0: return 0.0
    if p == 1: return 1.0
    lp, lq = math.log(p), math.log1p(-p)
    terms = [math.lgamma(k+1)-math.lgamma(i+1)-math.lgamma(k-i+1)+i*lp+(k-i)*lq
             for i in range(at_least,k+1)]
    m = max(terms)
    return min(1.0, math.exp(m)*math.fsum(math.exp(t-m) for t in terms))


def is_prime(n):
    """Deterministic Miller-Rabin for integer n < 2**64 only."""
    _integer(n, 'n', minimum=None)
    if n >= 1 << 64: raise ValueError('deterministic primality requires n < 2**64')
    if n < 2: return False
    for q in (2,3,5,7,11,13,17,19,23,29,31,37):
        if n % q == 0: return n == q
    d,s=n-1,0
    while d % 2 == 0: d//=2; s+=1
    for a in (2,325,9375,28178,450775,9780504,1795265022):
        if a % n == 0: continue
        x=pow(a,d,n)
        if x in (1,n-1): continue
        for _ in range(s-1):
            x=x*x%n
            if x==n-1: break
        else: return False
    return True


def next_prime(n):
    _integer(n, 'n', minimum=None)
    n=max(2,n)
    while not is_prime(n): n+=1
    return n


def poly_eval(bits, r, q):
    """The string as a polynomial b_0 + b_1 r + ... over GF(q), by Horner's rule."""
    _field(q); _integer(r,'r',minimum=None); bits=list(bits); _bit_values(bits)
    acc = 0
    for b in reversed(bits):
        acc = (acc * r + b) % q
    return acc


def fingerprint_eq(x, y, q, rng, trace=None):
    """Private-coin equal-length bit strings; Alice sends (r, x(r))."""
    _field(q); x=list(x); y=list(y)
    if len(x)!=len(y): raise ValueError('fingerprints require equal-length strings')
    _bit_values(x); _bit_values(y)
    r=rng.randrange(q)
    left,right=poly_eval(x,r,q),poly_eval(y,r,q)
    if trace is not None: trace.append(dict(r=r,left=left,right=right,q=q))
    return left==right,2*(q-1).bit_length()


# ----------------------------------------------------------------------------------------------- switching lemma

def dnf_random(n, terms, width, rng):
    _integer(n,'n'); _integer(terms,'terms'); _integer(width,'width')
    if width>n: raise ValueError('DNF width exceeds variables')
    out = []
    for _ in range(terms):
        vs = rng.sample(range(n), width)
        out.append(tuple((v, rng.random() < 0.5) for v in vs))
    return out


def dnf_eval(dnf, x):
    dnf=_dnf(dnf)
    return any(all(x[v] == b for v, b in t) for t in dnf)


def restrict(dnf, rho):
    """rho maps variable -> 0/1 (fixed) or is absent (free). Returns the simplified DNF (True if a term is satisfied,
    False if no terms survive)."""
    dnf=_dnf(dnf); rho=dict(rho)
    for v,b in rho.items():
        _integer(v,'restriction variable')
        if type(b) not in (bool,int) or b not in (0,1): raise ValueError('restriction values must be Boolean')
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
    free=list(free)
    if len(set(free))!=len(free): raise ValueError('free variables must be distinct')
    for v in free: _integer(v,'free variable')
    if f is not True and f is not False:
        f=_dnf(f)
        if any(v not in free for t in f for v,b in t): raise ValueError('all DNF variables must be listed as free')
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
    _integer(k,'k'); tab=tuple(tab); _table(tab,k)
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
    _integer(n,'n'); _probability(p)
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
    _field(p); x=list(x); clauses=_cnf(clauses,len(x))
    if any(type(v) not in (bool,int) for v in x): raise ValueError('integer field coordinates required')
    return _arith_eval(clauses,x,p)


def _arith_eval(clauses, x, p):
    acc = 1
    for c in clauses:
        t = 1
        for l in c:
            t = t * (1 - lit_val(l, x, p)) % p
        acc = acc * (1 - t) % p
    return acc


def lagrange_eval(ys, r, p):
    """Evaluate the polynomial through (0, ys[0]), (1, ys[1]), ... at r, over GF(p)."""
    _field(p); ys=list(ys)
    if not ys or len(ys)>p or any(type(y) is not int for y in ys): raise ValueError('distinct interpolation points and integer values required')
    _integer(r,'r',minimum=None)
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
    clauses=_cnf(clauses,n); _field(p); _integer(deg,'deg',1)
    if deg>=p or len(prefix)>=n: raise ValueError('invalid interpolation degree or prefix')
    actual=max((sum(abs(l)==v for c in clauses for l in c) for v in range(1,n+1)),default=0)
    if deg<actual: raise ValueError('degree bound is smaller than the polynomial individual degree')
    i = len(prefix)
    rest = n - i - 1
    ys = []
    for X in range(deg + 1):
        s = 0
        for suf in itertools.product((0, 1), repeat=rest):
            s += _arith_eval(clauses, list(prefix) + [X] + list(suf), p)
        ys.append(s % p)
    return ys


def sumcheck(clauses, n, p, claim, rng, cheat=False):
    """Run a teaching sum-check for the Boolean-cube sum modulo prime p.

    Messages are degree-bounded by their values at distinct field points.
    Repeated occurrences contribute to the individual degree. A polynomial
    upper bound of one also handles constant and empty formulas.
    """
    clauses=_cnf(clauses,n); _integer(claim,'claim',minimum=None)
    deg=max(1,len(clauses),max((sum(abs(l)==v for c in clauses for l in c) for v in range(1,n+1)),default=0))
    _field(p)
    if deg>=p: raise ValueError('field must exceed the interpolation degree bound')
    cur=claim%p; prefix=[]; log=[]
    for i in range(n):
        g=honest_message(clauses,n,p,prefix,deg)
        if cheat:
            err=(cur-g[0]-g[1])%p
            if err:
                den=math.prod(1-j for j in range(2,deg+1))%p
                scale=err*pow(den,-1,p)%p
                for X in range(deg+1):
                    delta=scale*X
                    for j in range(2,deg+1): delta=delta*(X-j)%p
                    g[X]=(g[X]+delta)%p
        if (g[0]+g[1])%p != cur:
            log.append(dict(round=i+1,check=False,g=g,previous=cur,degree_bound=deg))
            return False,i+1,log
        r=rng.randrange(p); previous=cur; cur=lagrange_eval(g,r,p); prefix.append(r)
        log.append(dict(round=i+1,g=g,r=r,next=cur,previous=previous,degree_bound=deg))
    final=arith_eval(clauses,prefix,p); ok=final==cur
    log.append(dict(final=final,claim=cur,ok=ok))
    return ok,n,log


def count_sat(clauses, n):
    clauses=_cnf(clauses,n)
    return sum(all(any(a[abs(l)-1]==(l>0) for l in c) for c in clauses)
               for a in itertools.product((False,True),repeat=n))


# ----------------------------------------------------------------------------------------------- interaction

def permute_graph(edges, perm):
    return frozenset(frozenset((perm[u], perm[v])) for u, v in edges)


def isomorphic(e1, e2, n):
    _integer(n,'n'); e1=_edges(e1,n); e2=_edges(e2,n)
    s2 = frozenset(frozenset(e) for e in e2)
    for perm in itertools.permutations(range(n)):
        if permute_graph(e1, perm) == s2:
            return True
    return False


def gni_round(G0, G1, n, rng, trace=None):
    """Verifier picks b and a random relabelling of G_b; the all-powerful prover says which graph it came from (it
    checks isomorphism with G0 by brute force; if both match, it guesses). Returns (b, answer)."""
    G0=_edges(G0,n); G1=_edges(G1,n)
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
    if trace is not None:
        trace.append(dict(bit=b,permutation=perm,challenge_edges=sorted(sorted(e) for e in H),answer=ans,matches=[m0,m1]))
    return b, ans


def commit(value, rng):
    _integer(value,'value')
    if value>255: raise ValueError('commitment value must fit one byte')
    nonce = rng.getrandbits(128).to_bytes(16, "big")
    return hashlib.sha256(nonce + bytes([value])).hexdigest(), nonce


def zk_colouring(n, edges, colouring, rounds, rng, trace=None):
    """Salted-hash teaching protocol; RNG is supplied, not assumed cryptographic.

    Optional trace retains public commitments, selected edges and openings.
    Opened-pair marginals alone do not establish full zero knowledge.
    """
    _integer(n,'n'); _integer(rounds,'rounds'); edges=_edges(edges,n)
    colouring=list(colouring)
    if len(colouring)!=n or any(type(c) is not int or not 0<=c<3 for c in colouring):
        raise ValueError('one colour in {0,1,2} is required per vertex')
    revealed=[]
    if not edges: return None,revealed
    for k in range(rounds):
        pi=[0,1,2]; rng.shuffle(pi); col=[pi[c] for c in colouring]
        coms=[commit(c,rng) for c in col]
        u,v=edges[rng.randrange(len(edges))]
        openings=[]
        for w in (u,v):
            h,nonce=coms[w]
            assert hashlib.sha256(nonce+bytes([col[w]])).hexdigest()==h
            openings.append(dict(vertex=w,colour=col[w],nonce=nonce.hex()))
        good=col[u]!=col[v]
        if trace is not None:
            trace.append(dict(round=k+1,commitments=[h for h,_ in coms],edge=[u,v],openings=openings,accepted=good))
        revealed.append((col[u],col[v]))
        if not good: return k+1,revealed
    return None,revealed


def zk_simulate(rounds, rng):
    """The simulator's transcript: a uniformly random pair of distinct colours for a random edge."""
    _integer(rounds,'rounds')
    out = []
    for _ in range(rounds):
        a = rng.randrange(3)
        b = (a + 1 + rng.randrange(2)) % 3
        out.append((a, b))
    return out


# ----------------------------------------------------------------------------------------------- PCP flavour

def blr_rejection(f, n):
    """f: list of 2^n bits. Exact probability that f(x) + f(y) != f(x xor y) over uniform x, y."""
    _table(f,n)
    N = 1 << n
    bad = 0
    for x in range(N):
        fx = f[x]
        for y in range(N):
            if fx ^ f[y] != f[x ^ y]:
                bad += 1
    return bad / (N * N)


def distance_to_linear(f, n):
    _table(f,n)
    N = 1 << n
    best = N
    for a in range(N):
        d = sum(1 for x in range(N) if f[x] != (bin(a & x).count("1") & 1))
        best = min(best, d)
    return best / N


def walksat(n, clauses, rng, flips=20000, noise=0.5):
    """Bounded MAX-SAT local search; empty clauses remain unsatisfied."""
    clauses=_cnf(clauses,n); _integer(flips,'flips'); _probability(noise)
    a=[False]+[rng.random()<0.5 for _ in range(n)]
    def sat(c): return any(a[abs(l)]==(l>0) for l in c)
    score=lambda:sum(sat(c) for c in clauses)
    best=score(); best_a=a[:]
    occ={}
    for i,c in enumerate(clauses):
        for v in {abs(l) for l in c}: occ.setdefault(v,[]).append(i)
    for _ in range(flips):
        unsat=[c for c in clauses if c and not sat(c)]
        if not unsat: break
        c=rng.choice(unsat)
        if rng.random()<noise: v=abs(rng.choice(c))
        else:
            def breaks(v):
                a[v]=not a[v]; b=sum(not sat(clauses[i]) for i in occ.get(v,[])); a[v]=not a[v]; return b
            v=min({abs(l) for l in c},key=breaks)
        a[v]=not a[v]; value=score()
        if value>best: best=value; best_a=a[:]
    return best,best_a


# ----------------------------------------------------------------------------------------------- parameterized

def vc_branch(edges, k):
    """Bounded search tree: pick an uncovered edge (u, v); one of them is in the cover. Returns (cover or None,
    nodes)."""
    _integer(k,'k'); edges=_edges(edges)
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
    _integer(k,'k'); edges=_edges(edges)
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
    _integer(n,'n'); _integer(k,'k'); edges=_edges(edges,n)
    k=min(k,n)
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
    A=_square(A)
    if not A: return 1
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
    A=_square(A)
    n = len(A)
    return sum(math.prod(A[i][s[i]] for i in range(n)) for s in itertools.permutations(range(n)))


def det_bareiss(A):
    """Exact integer determinant by fraction-free elimination, O(n^3)."""
    A=_square(A)
    if not A: return 1
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
    A=list(A); B=list(B)
    if any(type(v) is not int or v<0 for v in A+B): raise ValueError('nonnegative bit masks required')
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
    _integer(n,'n'); _integer(k,'k')
    if k>n: raise ValueError('clique size exceeds graph size')
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
    """Degree heuristic: select k highest-degree vertices, score adjacency to this set
    (including membership), and return the k highest scores. No recovery theorem
    or threshold-based selection is claimed for this teaching variant."""
    _integer(k,'k')
    if k>len(adj) or any(type(a) is not int or a<0 or a>=1<<len(adj) for a in adj): raise ValueError('invalid bitmask graph or clique size')
    n = len(adj)
    deg = [bin(a).count("1") for a in adj]
    top = sorted(range(n), key=lambda v: -deg[v])[:k]
    mask = 0
    for v in top:
        mask |= 1 << v
    score = [bin(adj[v] & mask).count("1") + ((mask >> v) & 1) for v in range(n)]
    return set(sorted(range(n), key=lambda v: -score[v])[:k])


def pollard_rho(n, rng, max_steps=10**7):
    """Bounded Brent rho; count every modular orbit update, including advances.

    Return (None, steps) on exhaustion. Prime inputs below 2**64 are rejected;
    larger inputs have a finite budget, without an unsupported primality claim.
    """
    _integer(n,'n',2); _integer(max_steps,'max_steps')
    if n < 1<<64 and is_prime(n): raise ValueError('a composite input is required')
    if max_steps==0: return None,0
    if n%2==0: return 2,0
    steps=0
    def advance(y,c):
        nonlocal steps
        if steps>=max_steps: raise _RhoBudget
        steps+=1
        return (y*y+c)%n
    try:
        while True:
            y,c,m=rng.randrange(1,n),rng.randrange(1,n),128
            g,r,q=1,1,1
            while g==1:
                x=y
                for _ in range(r): y=advance(y,c)
                k=0
                while k<r and g==1:
                    ys=y
                    for _ in range(min(m,r-k)):
                        y=advance(y,c); q=q*abs(x-y)%n
                    g=math.gcd(q,n); k+=m
                r*=2
            if g==n:
                g=1
                while g==1: ys=advance(ys,c); g=math.gcd(abs(x-ys),n)
            if 1<g<n: return g,steps
    except _RhoBudget: return None,steps


# ----------------------------------------------------------------------------------------------- unique games

def ug_instance(n, m, k, eps, rng):
    """Connected simple shift game; exactly round(eps*m) nonzero corruptions."""
    _integer(n,'n',1); _integer(m,'m'); _integer(k,'k',2); _probability(eps)
    if not n-1<=m<=n*(n-1)//2: raise ValueError('connected simple graph requires n-1 <= m <= n choose 2')
    planted=[rng.randrange(k) for _ in range(n)]
    order=list(range(n)); rng.shuffle(order)
    pairs=list(zip(order,order[1:])); seen={tuple(sorted(e)) for e in pairs}
    while len(pairs)<m:
        a,b=rng.sample(range(n),2); edge=tuple(sorted((a,b)))
        if edge not in seen: pairs.append((a,b)); seen.add(edge)
    rng.shuffle(pairs); bad=set(rng.sample(range(m),round(eps*m))); edges=[]
    for i,(a,b) in enumerate(pairs):
        c=(planted[b]-planted[a])%k
        if i in bad: c=(c+rng.randrange(1,k))%k
        edges.append((a,b,c))
    return edges,planted


def ug_value(edges, x, k):
    _integer(k,'k',2); edges=list(edges); x=list(x)
    if any(type(v) is not int or not 0<=v<k for v in x): raise ValueError('labels must belong to Z_k')
    for a,b,c in edges:
        if any(type(v) is not int for v in (a,b,c)) or not 0<=a<len(x) or not 0<=b<len(x) or a==b or not 0<=c<k: raise ValueError('invalid shift constraint')
    if not edges: return 1.0
    return sum((x[b] - x[a] - c) % k == 0 for a, b, c in edges) / len(edges)


def ug_propagate(n, edges, k, root):
    """Fix the root's label to 0 and propagate along a BFS tree (each label is then forced): the easy algorithm."""
    _integer(n,'n',1); _integer(k,'k',2); _integer(root,'root')
    if root>=n: raise ValueError('root outside graph')
    edges=list(edges); ug_value(edges,[0]*n,k)
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
    clauses=_cnf(clauses,n)
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
    A=_square(A); _field(p)
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
    _field(p); xs=list(xs)
    if any(type(x) is not int for x in xs): raise ValueError('integer field elements required')
    if wrong and len(xs)<2: raise ValueError('false variant needs at least two variables')
    n = len(xs)
    lhs = det_mod([[pow(x, j, p) for j in range(n)] for x in xs], p)
    rhs = 1
    for j in range(n):
        for i in range(j):
            f = (xs[j] + xs[i]) if (wrong and (i, j) == (0, 1)) else (xs[j] - xs[i])
            rhs = rhs * f % p
    return lhs == rhs
