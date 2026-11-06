"""Changing one's mind, made computable (Part 14).

Everything is finite and semantic: a *world* is a valuation of a few atoms, written like ``"p~qr"``; a *proposition*
is a frozenset of worlds; a *belief state* is a set of worlds (the ones not ruled out), or, for iterated revision, a
Spohn ranking function (world -> rank, 0 the most plausible), whose rank-0 worlds are the beliefs and whose nested
lower sets are Grove's spheres.

* AGM: expansion, revision and contraction from a ranking; the Levi and Harper identities, checked; the eight
  revision postulates checked exhaustively for any operator, so that sphere revision, Dalal's distance revision,
  Satoh's set-inclusion revision and Winslett's update can be compared; partial meet contraction and recovery;
  epistemic entrenchment read off a ranking.
* Iterated revision: natural (Boutilier), lexicographic (Nayak), Spohn conditionalization and an amnesic operator,
  checked against the Darwiche--Pearl postulates DP1--DP4.
* Gärdenfors's impossibility theorem (1986): the Ramsey test's monotonicity and the preservation postulate, on three
  pairwise incompatible propositions, leave no consistent revision.
* Revision versus update (Katsuno and Mendelzon 1991): the book and the magazine.
"""

from __future__ import annotations

import itertools

from . import prop

INF = 10 ** 9


# ---------------------------------------------------------------------------
# Worlds and propositions
# ---------------------------------------------------------------------------
def worlds(atoms) -> list[str]:
    """All valuations of ``atoms``, most-true first: ``['pq', 'p~q', '~pq', '~p~q']``."""
    out = []
    for vals in itertools.product([True, False], repeat=len(atoms)):
        out.append("".join(a if v else "~" + a for a, v in zip(atoms, vals)))
    return out


def valuation(w: str, atoms) -> dict:
    v, i = {}, 0
    for a in atoms:
        neg = w.startswith("~", i)
        if neg:
            i += 1
        assert w.startswith(a, i), (w, a)
        i += len(a)
        v[a] = not neg
    return v


def P(formula: str, atoms) -> frozenset:
    """The proposition (set of worlds) expressed by a formula."""
    f = prop.parse(formula)
    return frozenset(w for w in worlds(atoms) if prop.evaluate(f, valuation(w, atoms)))


def all_props(W) -> list[frozenset]:
    W = list(W)
    return [frozenset(c) for r in range(len(W) + 1) for c in itertools.combinations(W, r)]


def hamming(w1: str, w2: str, atoms) -> int:
    a, b = valuation(w1, atoms), valuation(w2, atoms)
    return sum(a[x] != b[x] for x in atoms)


def diff(w1: str, w2: str, atoms) -> frozenset:
    a, b = valuation(w1, atoms), valuation(w2, atoms)
    return frozenset(x for x in atoms if a[x] != b[x])


# ---------------------------------------------------------------------------
# Rankings, spheres, and the three AGM operations
# ---------------------------------------------------------------------------
def beliefs(rank: dict) -> frozenset:
    m = min(rank.values())
    return frozenset(w for w, r in rank.items() if r == m)


def spheres(rank: dict) -> list[frozenset]:
    """Grove's system of spheres: the lower sets of the ranking, innermost (the beliefs) first."""
    return [frozenset(w for w, r in rank.items() if r <= k) for k in sorted(set(rank.values())) if k < INF]


def minimal(rank: dict, A) -> frozenset:
    A = [w for w in A if rank.get(w, INF) < INF]
    if not A:
        return frozenset()
    m = min(rank[w] for w in A)
    return frozenset(w for w in A if rank[w] == m)


def expand(K, A) -> frozenset:
    return frozenset(K) & frozenset(A)


def revise(rank: dict, A) -> frozenset:
    """Sphere revision: the most plausible A-worlds (Grove 1988)."""
    return minimal(rank, A)


def contract(rank: dict, A) -> frozenset:
    """Contract the belief A: keep the beliefs and add the most plausible not-A worlds."""
    K = beliefs(rank)
    W = frozenset(rank)
    if not K <= frozenset(A):
        return K
    return K | minimal(rank, W - frozenset(A))


def levi(rank: dict, A) -> frozenset:
    """Levi identity: K * A = (K - not-A) + A."""
    W = frozenset(rank)
    return expand(contract(rank, W - frozenset(A)), A)


def harper(rank: dict, A) -> frozenset:
    """Harper identity: K - A = K intersected with K * not-A (as theories): the union of their worlds."""
    W = frozenset(rank)
    return beliefs(rank) | revise(rank, W - frozenset(A))


def identities_hold(rank: dict) -> dict:
    W = frozenset(rank)
    props = [A for A in all_props(W) if A]
    return {"levi": all(levi(rank, A) == revise(rank, A) for A in props),
            "harper": all(harper(rank, A) == contract(rank, A) for A in props if A != W)}


def entrenchment(rank: dict, A) -> int:
    """How firmly the belief A is held: the rank of the most plausible not-A world (0 if A is not believed)."""
    W = frozenset(rank)
    notA = W - frozenset(A)
    if not notA:
        return INF
    return min(rank[w] for w in notA) - min(rank.values())


# ---------------------------------------------------------------------------
# The AGM postulates, checked
# ---------------------------------------------------------------------------
POSTULATES = [
    ("K*2", "success", r"$A \in K * A$"),
    ("K*3", "inclusion", r"$K * A \subseteq K + A$"),
    ("K*4", "vacuity", r"if $\lnot A \notin K$: \ $K + A \subseteq K * A$"),
    ("K*5", "consistency", r"$K * A$ is consistent if $A$ is"),
    ("K*7", "superexpansion", r"$K * (A \land B) \subseteq (K * A) + B$"),
    ("K*8", "subexpansion", r"if $\lnot B \notin K * A$: \ $(K * A) + B \subseteq K * (A \land B)$"),
]


def check_agm(K, op, W) -> dict:
    """``op(A)`` returns the revised world set. Returns, for each postulate (K*1 closure and K*6 extensionality are
    automatic for world sets), whether it holds and a counterexample if not. In world terms: K*2 f(A) <= A; K*3
    K & A <= f(A); K*4 K & A nonempty => f(A) <= K & A; K*5 A nonempty => f(A) nonempty; K*7 f(A) & B <= f(A & B);
    K*8 f(A) & B nonempty => f(A & B) <= f(A) & B."""
    K = frozenset(K)
    props = [A for A in all_props(W) if A]
    f = {A: frozenset(op(A)) for A in props}
    fails = {k: None for k, _, _ in POSTULATES}
    for A in props:
        R = f[A]
        if fails["K*2"] is None and not R <= A:
            fails["K*2"] = (sorted(A),)
        if fails["K*3"] is None and not (K & A) <= R:
            fails["K*3"] = (sorted(A),)
        if fails["K*4"] is None and (K & A) and not R <= (K & A):
            fails["K*4"] = (sorted(A),)
        if fails["K*5"] is None and not R:
            fails["K*5"] = (sorted(A),)
    for A in props:
        for B in props:
            AB = A & B
            if not AB:
                continue
            if fails["K*7"] is None and not (f[A] & B) <= f[AB]:
                fails["K*7"] = (sorted(A), sorted(B))
            if fails["K*8"] is None and (f[A] & B) and not f[AB] <= (f[A] & B):
                fails["K*8"] = (sorted(A), sorted(B))
    return {k: {"holds": v is None, "counterexample": v} for k, v in fails.items()}


def dalal(K, atoms):
    """Dalal (1988): the A-worlds at least Hamming distance from K. A faithful ranking, so AGM."""
    W = worlds(atoms)

    def op(A):
        d = {w: min(hamming(w, k, atoms) for k in K) for w in A}
        m = min(d.values())
        return [w for w in A if d[w] == m]
    return op, {w: min(hamming(w, k, atoms) for k in K) for w in W}


def satoh(K, atoms):
    """Satoh (1988): the A-worlds whose set of changed atoms is minimal under inclusion, over all pairs."""
    def op(A):
        if frozenset(K) & frozenset(A):
            return list(frozenset(K) & frozenset(A))
        pairs = [(a, diff(a, k, atoms)) for a in A for k in K]
        ds = {d for _, d in pairs}
        mins = {d for d in ds if not any(e < d for e in ds)}
        return sorted({a for a, d in pairs if d in mins})
    return op


def winslett(K, atoms):
    """Winslett's possible models approach, an *update*: move each K-world to its inclusion-closest A-worlds."""
    def op(A):
        out = set()
        for k in K:
            ds = {a: diff(a, k, atoms) for a in A}
            out |= {a for a, d in ds.items() if not any(e < d for e in ds.values())}
        return sorted(out)
    return op


def postulate_table(atoms=("p", "q", "r"), K=None) -> dict:
    """Which revision operators satisfy which AGM postulates, from one belief state K."""
    W = worlds(atoms)
    K = frozenset(K or P("p & q & r", atoms))
    dal_op, _ = dalal(K, atoms)
    rank = {w: (0 if w in K else 1 + min(hamming(w, k, atoms) for k in K)) for w in W}
    ops = {"spheres (a ranking)": lambda A: revise(rank, A), "Dalal (distance)": dal_op,
           "Satoh (set inclusion)": satoh(K, atoms), "Winslett (update)": winslett(K, atoms)}
    return {name: check_agm(K, op, W) for name, op in ops.items()}


def satoh_example() -> dict:
    """A small case where Satoh's revision breaks subexpansion (K*8), found by search: with K = {pqr}, changing
    {q} and changing {p, r} are incomparable under inclusion, so revising by the weaker B keeps both."""
    atoms = ("p", "q", "r")
    W = worlds(atoms)
    for K in itertools.chain(itertools.combinations(W, 1), itertools.combinations(W, 2)):
        res = check_agm(frozenset(K), satoh(frozenset(K), atoms), W)
        if not res["K*8"]["holds"]:
            A, B = res["K*8"]["counterexample"]
            op = satoh(frozenset(K), atoms)
            return {"K": list(K), "A": A, "B": B, "K*A": sorted(op(A)),
                    "K*(A&B)": sorted(op(sorted(set(A) & set(B))))}
    return {}


def book_and_magazine() -> dict:
    """Katsuno and Mendelzon (1991): b = 'the book is on the floor', m = 'the magazine is on the floor'. We believe
    exactly one is; then we learn (revision) or bring it about (update) that the book is not on the floor."""
    atoms = ("b", "m")
    K = P("(b & ~m) | (~b & m)", atoms)
    A = P("~b", atoms)
    rank = {w: (0 if w in K else 1) for w in worlds(atoms)}
    return {"K": sorted(K), "A": sorted(A), "revision": sorted(revise(rank, A)),
            "update": sorted(winslett(K, atoms)(sorted(A)))}


# ---------------------------------------------------------------------------
# Partial meet contraction and recovery
# ---------------------------------------------------------------------------
def remainders(K, A, W) -> list[frozenset]:
    """K's remainder sets modulo A, as world sets: the maximal subtheories of K not implying A each add exactly one
    not-A world."""
    notA = frozenset(W) - frozenset(A)
    return [frozenset(K) | {w} for w in sorted(notA)]


def partial_meet(K, A, W, select) -> frozenset:
    """The intersection of the selected remainders (as theories): the union of their worlds."""
    rem = remainders(K, A, W)
    chosen = select(rem)
    out = frozenset(K)
    for r in chosen:
        out |= r
    return out


def recovery(K, A, W, select) -> bool:
    """(K - A) + A includes K, i.e. its worlds are within K's."""
    return expand(partial_meet(K, A, W, select), A) <= frozenset(K)


# ---------------------------------------------------------------------------
# Iterated revision: four operators on rankings, and the Darwiche--Pearl postulates
# ---------------------------------------------------------------------------
def natural(rank: dict, A) -> dict:
    """Boutilier (1993): the most plausible A-worlds become rank 0; otherwise the old order is kept, one rank down."""
    best = minimal(rank, A)
    order = sorted({r for w, r in rank.items() if w not in best})
    pos = {r: i + 1 for i, r in enumerate(order)}
    return {w: (0 if w in best else pos[r]) for w, r in rank.items()}


def lexicographic(rank: dict, A) -> dict:
    """Nayak (1994): every A-world above every not-A world, each block in its old order."""
    A = frozenset(A)
    a = sorted({rank[w] for w in A})
    n = sorted({rank[w] for w in rank if w not in A})
    pa = {r: i for i, r in enumerate(a)}
    pn = {r: len(a) + i for i, r in enumerate(n)}
    return {w: (pa[r] if w in A else pn[r]) for w, r in rank.items()}


def spohn(rank: dict, A, strength: int = 1) -> dict:
    """Spohn's (A, n)-conditionalization: shift the A-worlds so the best is rank 0, the not-A worlds so the best is
    rank n."""
    A = frozenset(A)
    ka = min(rank[w] for w in A)
    notA = [w for w in rank if w not in A]
    kn = min(rank[w] for w in notA) if notA else 0
    return {w: (r - ka if w in A else strength + r - kn) for w, r in rank.items()}


def amnesic(rank: dict, A) -> dict:
    """An AGM-compliant operator with no memory: after each revision, everything but the new beliefs is equally
    plausible."""
    best = minimal(rank, A)
    return {w: (0 if w in best else 1) for w in rank}


DP = [("DP1", r"if $C \vDash \mu$: \ $(\Psi * \mu) * C = \Psi * C$", "order among mu-worlds kept"),
      ("DP2", r"if $C \vDash \lnot\mu$: \ $(\Psi * \mu) * C = \Psi * C$", "order among not-mu worlds kept"),
      ("DP3", r"if $\Psi * C \vDash \mu$: \ $(\Psi * \mu) * C \vDash \mu$", "a mu-world below a not-mu stays below"),
      ("DP4", r"if $\Psi * C \nvDash \lnot\mu$: \ $(\Psi * \mu) * C \nvDash \lnot\mu$", "and never sinks behind it")]


def check_dp(rank: dict, op) -> dict:
    """DP1--DP4 over every pair of nonempty propositions mu, C."""
    W = frozenset(rank)
    props = [A for A in all_props(W) if A]
    fails = {k: None for k, _, _ in DP}
    for mu in props:
        new = op(rank, mu)
        for C in props:
            before = revise(rank, C)
            after = revise(new, C)
            if C <= mu and after != before and fails["DP1"] is None:
                fails["DP1"] = (sorted(mu), sorted(C))
            if not (C & mu) and after != before and fails["DP2"] is None:
                fails["DP2"] = (sorted(mu), sorted(C))
            if before <= mu and not after <= mu and fails["DP3"] is None:
                fails["DP3"] = (sorted(mu), sorted(C))
            if (before & mu) and not (after & mu) and fails["DP4"] is None:
                fails["DP4"] = (sorted(mu), sorted(C))
    return {k: {"holds": v is None, "counterexample": v} for k, v in fails.items()}


def dp_table(rank: dict | None = None) -> dict:
    """A small ranking over two atoms (the beliefs p and q, ~p a little less likely, ~p~q least), and four operators."""
    rank = rank or {"pq": 0, "p~q": 1, "~pq": 2, "~p~q": 4}
    ops = {"natural (Boutilier)": natural, "lexicographic (Nayak)": lexicographic,
           "Spohn, strength 1": lambda r, A: spohn(r, A, 1), "amnesic": amnesic}
    return {name: check_dp(rank, op) for name, op in ops.items()}


def iterate_demo() -> dict:
    """The bird example of Darwiche and Pearl: we see a red bird (r) that flies (f); told it is not red, then that it
    is red after all, the amnesic agent has forgotten that it flies."""
    atoms = ("r", "f")
    rank = {"rf": 0, "r~f": 1, "~rf": 1, "~r~f": 2}
    W = frozenset(rank)
    notr = P("~r", atoms)
    red = P("r", atoms)
    out = {}
    for name, op in (("natural", natural), ("amnesic", amnesic)):
        k1 = op(rank, notr)
        k2 = op(k1, red)
        out[name] = {"after ~r": sorted(beliefs(k1)), "after r": sorted(beliefs(k2)),
                     "still believes f": beliefs(k2) <= P("f", atoms), "rank": k2}
    del W
    return out


# ---------------------------------------------------------------------------
# Gärdenfors's impossibility theorem
# ---------------------------------------------------------------------------
def gardenfors() -> dict:
    """Three worlds a, b, c; A, B, C the propositions {a}, {b}, {c}, pairwise incompatible, each consistent with K.
    Preservation fixes K1 * (B v C) = {b} for K1 = K + (A v B), and K2 * (B v C) = {c} for K2 = K + (A v C). The
    Ramsey test makes revision monotone: H = K + A extends K1 and K2, conditionals included, so H * (B v C) must lie
    within both {b} and {c}. Every candidate fails."""
    K = frozenset("abc")
    K1, K2, H = frozenset("ab"), frozenset("ac"), frozenset("a")
    BC = frozenset("bc")
    r1, r2 = K1 & BC, K2 & BC                       # preservation: consistent revisions are expansions
    cands = [frozenset(x) for x in ("b", "c", "bc")]
    rows = []
    for X in cands:
        rows.append({"H*(BvC)": sorted(X), "within K1*(BvC)": X <= r1, "within K2*(BvC)": X <= r2,
                     "consistent": bool(X)})
    return {"K": sorted(K), "K1": sorted(K1), "K2": sorted(K2), "H": sorted(H), "K1*(BvC)": sorted(r1),
            "K2*(BvC)": sorted(r2), "candidates": rows,
            "survivors": [r["H*(BvC)"] for r in rows if r["within K1*(BvC)"] and r["within K2*(BvC)"]]}
