"""Causation, made computable (Part 17).

* Boolean causal structure: INUS conditions as the conjuncts of prime implicants (Mackie 1965).
* Structural causal models over finite variables: structural equations plus exogenous noise; the observational
  distribution by enumeration; interventions (do); counterfactuals by abduction, action and prediction; the
  probabilities of necessity and sufficiency (Tian and Pearl 2000).
* Graphs: d-separation (by the moralized ancestral graph), the back-door and front-door criteria and adjustment
  formulas, checked against the interventional truth; Markov equivalence classes of small DAGs.
* Actual causation: the modified Halpern--Pearl definition (Halpern 2015), run on rock-throwing, the forest fires,
  double prevention and bogus prevention.
* The PC algorithm with a d-separation oracle and with data (a G-test of conditional independence).
"""

from __future__ import annotations

import itertools
import math
import random
from collections import defaultdict

import numpy as np


# ---------------------------------------------------------------------------
# INUS conditions
# ---------------------------------------------------------------------------
def prime_implicants(f, names: list[str]) -> list[dict]:
    """Minimal conjunctions of literals (name -> value) that make the Boolean function f true whatever the other
    variables are. Brute force over all partial assignments; fine for a handful of variables."""
    n = len(names)
    cands = []
    for k in range(1, n + 1):
        for vars_ in itertools.combinations(range(n), k):
            for vals in itertools.product([0, 1], repeat=k):
                fixed = dict(zip(vars_, vals))
                rest = [i for i in range(n) if i not in fixed]
                ok = True
                for rv in itertools.product([0, 1], repeat=len(rest)):
                    a = [0] * n
                    for i, v in fixed.items():
                        a[i] = v
                    for i, v in zip(rest, rv):
                        a[i] = v
                    if not f(*a):
                        ok = False
                        break
                if ok:
                    lit = {names[i]: v for i, v in fixed.items()}
                    if not any(all(lit.get(kk) == vv for kk, vv in c.items()) for c in cands):
                        cands.append(lit)
    return cands


def inus(f, names: list[str], target: str, value: int = 1) -> dict:
    """Is the literal (target = value) an INUS condition for f? An Insufficient but Non-redundant part of an
    Unnecessary but Sufficient condition: it occurs in some prime implicant (minimal sufficient condition) that is
    not the only one, and is not by itself sufficient."""
    pis = prime_implicants(f, names)
    containing = [p for p in pis if p.get(target) == value]
    alone = {target: value} in pis
    return {"prime_implicants": pis, "in": containing, "inus": bool(containing) and not alone and len(pis) > 1}


# ---------------------------------------------------------------------------
# Structural causal models
# ---------------------------------------------------------------------------
class SCM:
    """A structural causal model over finite-valued variables.

    ``exo``: {U: [(value, prob), ...]} independent exogenous variables.
    ``eqs``: ordered {V: (parents, function)}; the function takes parent values (exogenous or endogenous) in order.
    """

    def __init__(self, exo: dict, eqs: dict):
        self.exo = exo
        self.eqs = eqs
        self.endo = list(eqs)

    def parents(self, v: str) -> list[str]:
        return list(self.eqs[v][0])

    def solve(self, u: dict, do: dict | None = None) -> dict:
        do = do or {}
        val = dict(u)
        for v, (pa, fn) in self.eqs.items():
            val[v] = do[v] if v in do else fn(*[val[p] for p in pa])
        return val

    def worlds(self):
        names = list(self.exo)
        for combo in itertools.product(*[self.exo[n] for n in names]):
            u = {n: c[0] for n, c in zip(names, combo)}
            p = math.prod(c[1] for c in combo)
            if p > 0:
                yield u, p

    def prob(self, event, do: dict | None = None, given=None) -> float:
        """P(event | given) in the model under do(...); event and given are functions of the solved values."""
        num = den = 0.0
        for u, p in self.worlds():
            w = self.solve(u, do)
            if given is None or given(w):
                den += p
                if event(w):
                    num += p
        return num / den if den else float("nan")

    def joint(self, vars_: list[str], do: dict | None = None) -> dict:
        out = defaultdict(float)
        for u, p in self.worlds():
            w = self.solve(u, do)
            out[tuple(w[v] for v in vars_)] += p
        return dict(out)

    def counterfactual(self, event, do: dict, evidence) -> float:
        """P(event_{do} | evidence): abduction (condition the exogenous distribution on the evidence, in the actual
        world), action (do), prediction (solve)."""
        num = den = 0.0
        for u, p in self.worlds():
            if evidence(self.solve(u)):
                den += p
                if event(self.solve(u, do)):
                    num += p
        return num / den if den else float("nan")

    def sample(self, n: int, seed: int = 0, do: dict | None = None) -> list[dict]:
        rnd = random.Random(seed)
        names = list(self.exo)
        out = []
        for _ in range(n):
            u = {}
            for nm in names:
                r, acc = rnd.random(), 0.0
                for v, pr in self.exo[nm]:
                    acc += pr
                    if r <= acc:
                        u[nm] = v
                        break
                else:
                    u[nm] = self.exo[nm][-1][0]
            out.append(self.solve(u, do))
        return out


def bern(p: float) -> list:
    return [(1, p), (0, 1 - p)]


# ---------------------------------------------------------------------------
# Graphs and d-separation
# ---------------------------------------------------------------------------
class DAG:
    def __init__(self, edges: list[tuple[str, str]], nodes: list[str] | None = None):
        self.edges = list(edges)
        ns = set(nodes or [])
        for a, b in edges:
            ns |= {a, b}
        self.nodes = sorted(ns) if nodes is None else list(nodes)
        self.pa = {v: set() for v in self.nodes}
        self.ch = {v: set() for v in self.nodes}
        for a, b in edges:
            self.pa[b].add(a)
            self.ch[a].add(b)

    def ancestors(self, S: set) -> set:
        out, stack = set(S), list(S)
        while stack:
            v = stack.pop()
            for p in self.pa[v]:
                if p not in out:
                    out.add(p)
                    stack.append(p)
        return out

    def dsep(self, X: set, Y: set, Z: set) -> bool:
        """X independent of Y given Z in every distribution Markov to the DAG: separate X and Y in the moral graph of
        the ancestral set of X, Y, Z after removing Z (Lauritzen)."""
        A = self.ancestors(set(X) | set(Y) | set(Z))
        adj = {v: set() for v in A}
        for v in A:
            ps = [p for p in self.pa[v] if p in A]
            for p in ps:
                adj[v].add(p)
                adj[p].add(v)
            for a, b in itertools.combinations(ps, 2):
                adj[a].add(b)
                adj[b].add(a)
        seen = set(X)
        stack = list(X)
        while stack:
            v = stack.pop()
            for w in adj[v]:
                if w in Z or w in seen:
                    continue
                if w in Y:
                    return False
                seen.add(w)
                stack.append(w)
        return True

    def skeleton(self) -> set:
        return {frozenset(e) for e in self.edges}

    def vstructures(self) -> set:
        out = set()
        for c in self.nodes:
            for a, b in itertools.combinations(sorted(self.pa[c]), 2):
                if frozenset((a, b)) not in self.skeleton():
                    out.add((a, c, b))
        return out

    def remove_out_edges(self, X: set) -> "DAG":
        return DAG([(a, b) for a, b in self.edges if a not in X], self.nodes)

    def remove_in_edges(self, X: set) -> "DAG":
        return DAG([(a, b) for a, b in self.edges if b not in X], self.nodes)

    def descendants(self, S: set) -> set:
        out, stack = set(S), list(S)
        while stack:
            v = stack.pop()
            for c in self.ch[v]:
                if c not in out:
                    out.add(c)
                    stack.append(c)
        return out


def markov_equivalent(g1: DAG, g2: DAG) -> bool:
    """Verma and Pearl (1990): same skeleton and same v-structures."""
    return g1.skeleton() == g2.skeleton() and g1.vstructures() == g2.vstructures()


def equivalence_class(g: DAG) -> list[list[tuple[str, str]]]:
    """All DAGs Markov equivalent to g: orient g's skeleton every acyclic way and keep those with g's v-structures."""
    sk = [tuple(sorted(e)) for e in g.skeleton()]
    out = []
    for bits in itertools.product([0, 1], repeat=len(sk)):
        edges = [(a, b) if t == 0 else (b, a) for (a, b), t in zip(sk, bits)]
        h = DAG(edges, g.nodes)
        if is_acyclic(h) and markov_equivalent(g, h):
            out.append(sorted(edges))
    return out


def is_acyclic(g: DAG) -> bool:
    indeg = {v: len(g.pa[v]) for v in g.nodes}
    q = [v for v in g.nodes if indeg[v] == 0]
    seen = 0
    while q:
        v = q.pop()
        seen += 1
        for c in g.ch[v]:
            indeg[c] -= 1
            if indeg[c] == 0:
                q.append(c)
    return seen == len(g.nodes)


def backdoor_ok(g: DAG, X: str, Y: str, Z: set) -> bool:
    """Pearl's back-door criterion: no member of Z is a descendant of X, and Z blocks every path from X to Y that
    starts with an arrow into X (d-separation in the graph with X's outgoing edges removed)."""
    if Z & g.descendants({X}):
        return False
    return g.remove_out_edges({X}).dsep({X}, {Y}, Z)


# ---------------------------------------------------------------------------
# Adjustment formulas, checked against the interventional truth
# ---------------------------------------------------------------------------
def backdoor_adjust(m: SCM, X: str, x, Y: str, y, Z: list[str]) -> float:
    """sum_z P(Y = y | X = x, Z = z) P(Z = z), from the observational distribution of m."""
    jz = m.joint(Z)
    total = 0.0
    for z, pz in jz.items():
        cond = dict(zip(Z, z))
        pyxz = m.prob(lambda w: w[Y] == y, given=lambda w: w[X] == x and all(w[k] == v for k, v in cond.items()))
        if not math.isnan(pyxz):
            total += pyxz * pz
    return total


def frontdoor_adjust(m: SCM, X: str, x, M: str, Y: str, y) -> float:
    """sum_m P(m | x) sum_x' P(y | m, x') P(x'), from the observational distribution of m."""
    xs = sorted({k[0] for k in m.joint([X])})
    ms = sorted({k[0] for k in m.joint([M])})
    px = {xv: m.prob(lambda w, xv=xv: w[X] == xv) for xv in xs}
    total = 0.0
    for mv in ms:
        pm_x = m.prob(lambda w, mv=mv: w[M] == mv, given=lambda w: w[X] == x)
        inner = 0.0
        for xv in xs:
            pyx = m.prob(lambda w: w[Y] == y, given=lambda w, mv=mv, xv=xv: w[M] == mv and w[X] == xv)
            if not math.isnan(pyx):
                inner += pyx * px[xv]
        total += pm_x * inner
    return total


def smoking_model(seed_strength: float = 1.0) -> SCM:
    """Pearl's smoking example with a front door: a hidden genotype G raises both smoking S and cancer C; smoking
    causes tar T; only tar causes cancer. G is unobserved, so no back-door adjustment is possible; the front-door
    formula through T recovers P(C | do(S))."""
    return SCM(
        exo={"G": bern(0.4), "Us": bern(0.15), "Ut": bern(0.05), "Uc": [(0, 0.5), (1, 0.3), (2, 0.2)]},
        eqs={
            "S": (["G", "Us"], lambda g, us: int((g == 1 and us == 0) or (g == 0 and us == 1))),
            "T": (["S", "Ut"], lambda s, ut: int(s != ut)),
            "C": (["T", "G", "Uc"], lambda t, g, uc: int(uc + t + g >= 2)),
        })


def confounded_model() -> SCM:
    """A drug D, recovery R, and age A that affects both: the back-door through A."""
    return SCM(
        exo={"A": bern(0.5), "Ud": [(0, 0.7), (1, 0.3)], "Ur": [(k / 10, 0.1) for k in range(10)]},
        eqs={
            "D": (["A", "Ud"], lambda a, ud: int(ud == 1) if a == 0 else int(ud == 0)),
            "R": (["D", "A", "Ur"], lambda d, a, ur: int(ur < 0.3 + 0.2 * d - 0.25 * a + 0.1)),
        })


def adjustment_demo() -> dict:
    """Back door: the naive conditional, the adjusted estimate, and the truth under do, for the confounded drug.
    Front door: the same for smoking and cancer, where the confounder is hidden."""
    m = confounded_model()
    naive = m.prob(lambda w: w["R"] == 1, given=lambda w: w["D"] == 1) - \
        m.prob(lambda w: w["R"] == 1, given=lambda w: w["D"] == 0)
    adj = backdoor_adjust(m, "D", 1, "R", 1, ["A"]) - backdoor_adjust(m, "D", 0, "R", 1, ["A"])
    truth = m.prob(lambda w: w["R"] == 1, do={"D": 1}) - m.prob(lambda w: w["R"] == 1, do={"D": 0})
    s = smoking_model()
    s_naive = s.prob(lambda w: w["C"] == 1, given=lambda w: w["S"] == 1) - \
        s.prob(lambda w: w["C"] == 1, given=lambda w: w["S"] == 0)
    s_front = frontdoor_adjust(s, "S", 1, "T", "C", 1) - frontdoor_adjust(s, "S", 0, "T", "C", 1)
    s_truth = s.prob(lambda w: w["C"] == 1, do={"S": 1}) - s.prob(lambda w: w["C"] == 1, do={"S": 0})
    g = DAG([("A", "D"), ("A", "R"), ("D", "R")])
    gs = DAG([("G", "S"), ("G", "C"), ("S", "T"), ("T", "C")])
    return {"backdoor": {"naive": naive, "adjusted": adj, "truth": truth,
                         "criterion_A": backdoor_ok(g, "D", "R", {"A"}),
                         "criterion_empty": backdoor_ok(g, "D", "R", set())},
            "frontdoor": {"naive": s_naive, "front": s_front, "truth": s_truth,
                          "backdoor_possible_without_G": backdoor_ok(gs, "S", "C", {"T"})}}


def simulate_adjustment(n: int = 200000, seed: int = 7) -> dict:
    """The same estimates from a finite sample, to show the formulas work on data, not only on the model."""
    m = confounded_model()
    data = m.sample(n, seed)
    cnt = defaultdict(int)
    for w in data:
        cnt[(w["A"], w["D"], w["R"])] += 1

    def p_r(d, a=None):
        num = sum(c for (aa, dd, rr), c in cnt.items() if dd == d and rr == 1 and (a is None or aa == a))
        den = sum(c for (aa, dd, rr), c in cnt.items() if dd == d and (a is None or aa == a))
        return num / den
    pa = {a: sum(c for (aa, _, _), c in cnt.items() if aa == a) / n for a in (0, 1)}
    naive = p_r(1) - p_r(0)
    adj = sum((p_r(1, a) - p_r(0, a)) * pa[a] for a in (0, 1))
    exp = m.sample(n, seed + 1, do={"D": 1})
    exp0 = m.sample(n, seed + 2, do={"D": 0})
    rct = sum(w["R"] for w in exp) / n - sum(w["R"] for w in exp0) / n
    return {"n": n, "naive": naive, "adjusted": adj, "rct": rct}


# ---------------------------------------------------------------------------
# Counterfactuals: necessity and sufficiency
# ---------------------------------------------------------------------------
def pn_ps_demo() -> dict:
    """A treatment X and outcome Y with exogenous 'types': Y = X for responders, 1 always, 0 always. PN = P(Y_{x=0}
    = 0 | X = 1, Y = 1), PS = P(Y_{x=1} = 1 | X = 0, Y = 0), computed by abduction-action-prediction, and the Tian--
    Pearl bounds from observational and experimental data alone."""
    m = SCM(exo={"T": [("resp", 0.3), ("always", 0.2), ("never", 0.5)], "Ux": bern(0.4)},
            eqs={"X": (["Ux"], lambda ux: ux),
                 "Y": (["X", "T"], lambda x, t: x if t == "resp" else (1 if t == "always" else 0))})
    pn = m.counterfactual(lambda w: w["Y"] == 0, {"X": 0}, lambda w: w["X"] == 1 and w["Y"] == 1)
    ps = m.counterfactual(lambda w: w["Y"] == 1, {"X": 1}, lambda w: w["X"] == 0 and w["Y"] == 0)
    py1_do1 = m.prob(lambda w: w["Y"] == 1, do={"X": 1})
    py1_do0 = m.prob(lambda w: w["Y"] == 1, do={"X": 0})
    pxy = m.prob(lambda w: w["X"] == 1 and w["Y"] == 1)
    py = m.prob(lambda w: w["Y"] == 1)
    # Tian and Pearl (2000) lower bound for PN, exact here (exogeneity)
    pn_lower = max(0.0, (py - py1_do0) / pxy)
    return {"PN": pn, "PS": ps, "PNS": py1_do1 - py1_do0, "pn_lower": pn_lower, "P(y|do x)": py1_do1,
            "P(y|do x')": py1_do0}


# ---------------------------------------------------------------------------
# Actual causation (modified Halpern--Pearl)
# ---------------------------------------------------------------------------
def hp_cause(m: SCM, u: dict, X: dict, phi) -> dict:
    """Is the conjunction X (variable -> actual value) an actual cause of phi in context u? Modified HP (Halpern
    2015): AC1 X = x and phi hold; AC2 there is a set W of other endogenous variables and values x' such that setting
    X = x' and W to their actual values makes phi false; AC3 no proper subset of X satisfies AC1 and AC2."""
    actual = m.solve(u)
    if not all(actual[k] == v for k, v in X.items()) or not phi(actual):
        return {"cause": False, "witness": None}

    def ac2(Xs: dict):
        others = [v for v in m.endo if v not in Xs]
        domains = {k: sorted({w[k] for w, _ in ((m.solve(uu, None), 0) for uu, _ in m.worlds())} | {0, 1})
                   for k in Xs}
        for r in range(len(others) + 1):
            for W in itertools.combinations(others, r):
                for xs in itertools.product(*[domains[k] for k in Xs]):
                    if all(a == Xs[k] for a, k in zip(xs, Xs)):
                        continue
                    do = dict(zip(Xs, xs))
                    do.update({w: actual[w] for w in W})
                    if not phi(m.solve(u, do)):
                        return {"W": list(W), "x'": dict(zip(Xs, xs))}
        return None
    wit = ac2(X)
    if wit is None:
        return {"cause": False, "witness": None}
    for r in range(1, len(X)):
        for sub in itertools.combinations(X, r):
            if ac2({k: X[k] for k in sub}) is not None:
                return {"cause": False, "witness": wit, "smaller": list(sub)}
    return {"cause": True, "witness": wit}


def classic_cases() -> list[dict]:
    """Suzy and Billy (preemption, with the 'hits' variables of Halpern and Pearl); the disjunctive and conjunctive
    forest fires; double prevention; bogus prevention. Each with the HP verdict and the counterfactual-dependence
    (but-for) verdict."""
    cases = []
    # rock throwing: ST, BT throws; SH = ST; BH = BT and not SH; BS = SH or BH
    rock = SCM(exo={"Us": bern(1.0), "Ub": bern(1.0)},
               eqs={"ST": (["Us"], lambda u: u), "BT": (["Ub"], lambda u: u), "SH": (["ST"], lambda s: s),
                    "BH": (["BT", "SH"], lambda b, sh: int(b and not sh)),
                    "BS": (["SH", "BH"], lambda a, b: int(a or b))})
    u = {"Us": 1, "Ub": 1}
    for who in ("ST", "BT"):
        hp = hp_cause(rock, u, {who: 1}, lambda w: w["BS"] == 1)
        butfor = rock.solve(u, {who: 0})["BS"] == 0
        cases.append({"case": "rock throwing", "candidate": who, "hp": hp["cause"], "but_for": butfor,
                      "witness": hp["witness"]})
    # forest fires: lightning L, match M
    for kind, fn in (("disjunctive", lambda l, m_: int(l or m_)), ("conjunctive", lambda l, m_: int(l and m_))):
        ff = SCM(exo={"Ul": bern(1.0), "Um": bern(1.0)},
                 eqs={"L": (["Ul"], lambda x: x), "M": (["Um"], lambda x: x), "FF": (["L", "M"], fn)})
        uu = {"Ul": 1, "Um": 1}
        hp = hp_cause(ff, uu, {"L": 1}, lambda w: w["FF"] == 1)
        hpc = hp_cause(ff, uu, {"L": 1, "M": 1}, lambda w: w["FF"] == 1)
        cases.append({"case": f"forest fire ({kind})", "candidate": "L", "hp": hp["cause"],
                      "but_for": ff.solve(uu, {"L": 0})["FF"] == 0, "witness": hp["witness"],
                      "conjunction_L_and_M": hpc["cause"]})
    # double prevention: Suzy's bomber; enemy fighter E would shoot it down; Billy's escort B shoots E
    dp = SCM(exo={"Ub": bern(1.0), "Ue": bern(1.0), "Us": bern(1.0)},
             eqs={"B": (["Ub"], lambda x: x), "E": (["Ue", "B"], lambda ue, b: int(ue and not b)),
                  "SB": (["Us"], lambda x: x), "TD": (["SB", "E"], lambda sb, e: int(sb and not e))})
    uu = {"Ub": 1, "Ue": 1, "Us": 1}
    hp = hp_cause(dp, uu, {"B": 1}, lambda w: w["TD"] == 1)
    cases.append({"case": "double prevention", "candidate": "B", "hp": hp["cause"],
                  "but_for": dp.solve(uu, {"B": 0})["TD"] == 0, "witness": hp["witness"]})
    # bogus prevention: Assassin A decides not to poison; Bodyguard B puts in antidote anyway; victim survives
    bp = SCM(exo={"Ua": bern(0.0), "Ub": bern(1.0)},
             eqs={"A": (["Ua"], lambda x: x), "B": (["Ub"], lambda x: x),
                  "VS": (["A", "B"], lambda a, b: int((not a) or b))})
    uu = {"Ua": 0, "Ub": 1}
    hp = hp_cause(bp, uu, {"B": 1}, lambda w: w["VS"] == 1)
    cases.append({"case": "bogus prevention", "candidate": "B", "hp": hp["cause"],
                  "but_for": bp.solve(uu, {"B": 0})["VS"] == 0, "witness": hp["witness"]})
    return cases


# ---------------------------------------------------------------------------
# Causal discovery: PC
# ---------------------------------------------------------------------------
def pc(nodes: list[str], indep, max_cond: int = 3) -> dict:
    """The PC algorithm (Spirtes, Glymour and Scheines): start complete; remove an edge a-b when a and b are
    independent given some subset of a's current neighbours; orient v-structures a -> c <- b when c is not in the
    separating set of a and b; then apply Meek's rules R1-R3. ``indep(a, b, S)`` is the independence test. Returns
    the skeleton, directed and undirected edges of the CPDAG, and the number of tests."""
    adj = {v: set(nodes) - {v} for v in nodes}
    sepset = {}
    tests = 0
    for size in range(max_cond + 1):
        for a in nodes:
            for b in sorted(adj[a]):
                if b not in adj[a]:
                    continue
                nb = sorted(adj[a] - {b})
                if len(nb) < size:
                    continue
                for S in itertools.combinations(nb, size):
                    tests += 1
                    if indep(a, b, set(S)):
                        adj[a].discard(b)
                        adj[b].discard(a)
                        sepset[frozenset((a, b))] = set(S)
                        break
    directed = set()
    undirected = {frozenset((a, b)) for a in nodes for b in adj[a]}
    for c in nodes:
        for a, b in itertools.combinations(sorted(adj[c]), 2):
            if b not in adj[a] and c not in sepset.get(frozenset((a, b)), set()):
                directed |= {(a, c), (b, c)}
    undirected = {e for e in undirected if not any((x, y) in directed for x in e for y in e if x != y)}

    def has_dir(x, y):
        return (x, y) in directed

    changed = True
    while changed:
        changed = False
        for e in list(undirected):
            x, y = sorted(e)
            for s, t in ((x, y), (y, x)):
                # R1: a -> s - t, a not adjacent to t  =>  s -> t
                r1 = any(has_dir(a, s) and t not in adj[a] and a != t for a in nodes)
                # R2: s -> c -> t and s - t  =>  s -> t
                r2 = any(has_dir(s, c) and has_dir(c, t) for c in nodes)
                # R3: s - c1 -> t, s - c2 -> t, c1, c2 non-adjacent  =>  s -> t
                r3 = any(frozenset((s, c1)) in undirected and frozenset((s, c2)) in undirected and has_dir(c1, t)
                         and has_dir(c2, t) and c2 not in adj[c1]
                         for c1, c2 in itertools.combinations(nodes, 2))
                if r1 or r2 or r3:
                    directed.add((s, t))
                    undirected.discard(e)
                    changed = True
                    break
    return {"skeleton": sorted(tuple(sorted(e)) for e in {frozenset((a, b)) for a in nodes for b in adj[a]}),
            "directed": sorted(directed), "undirected": sorted(tuple(sorted(e)) for e in undirected),
            "tests": tests, "sepsets": {"-".join(sorted(k)): sorted(v) for k, v in sepset.items()}}


def g_test_indep(data: list[dict], alpha: float = 0.01):
    """A conditional independence test for binary data: the G statistic summed over strata of S, compared with the
    chi-square critical value for its degrees of freedom (Wilson--Hilferty approximation)."""
    def chi2_crit(df):
        z = 2.3263 if alpha == 0.01 else 1.6449
        return df * (1 - 2 / (9 * df) + z * math.sqrt(2 / (9 * df))) ** 3

    def test(a, b, S):
        S = sorted(S)
        strata = defaultdict(lambda: defaultdict(int))
        for w in data:
            strata[tuple(w[s] for s in S)][(w[a], w[b])] += 1
        G = 0.0
        df = 0
        for tab in strata.values():
            n = sum(tab.values())
            ra = {x: sum(c for (i, j), c in tab.items() if i == x) for x in (0, 1)}
            rb = {y: sum(c for (i, j), c in tab.items() if j == y) for y in (0, 1)}
            for (i, j), c in tab.items():
                e = ra[i] * rb[j] / n
                if c > 0 and e > 0:
                    G += 2 * c * math.log(c / e)
            df += 1
        return G < chi2_crit(max(df, 1))
    return test


def sprinkler_scm() -> SCM:
    """Season C (cloudy), sprinkler S, rain R, wet grass W, slippery L: C -> S, C -> R, S -> W, R -> W, W -> L."""
    return SCM(
        exo={"Uc": bern(0.5), "Us": [(k / 10, 0.1) for k in range(10)], "Ur": [(k / 10, 0.1) for k in range(10)],
             "Uw": [(k / 10, 0.1) for k in range(10)], "Ul": [(k / 10, 0.1) for k in range(10)]},
        eqs={"C": (["Uc"], lambda u: u),
             "S": (["C", "Us"], lambda c, u: int(u < (0.1 if c else 0.6))),
             "R": (["C", "Ur"], lambda c, u: int(u < (0.8 if c else 0.2))),
             "W": (["S", "R", "Uw"], lambda s, r, u: int(u < (0.05 + 0.85 * max(s, r) + 0.05 * (s and r)))),
             "L": (["W", "Ul"], lambda w, u: int(u < (0.8 if w else 0.1)))})


def pc_demo(n: int = 20000, seed: int = 1993) -> dict:
    g = DAG([("C", "S"), ("C", "R"), ("S", "W"), ("R", "W"), ("W", "L")])
    oracle = pc(g.nodes, lambda a, b, S: g.dsep({a}, {b}, S))
    data = sprinkler_scm().sample(n, seed)
    from_data = pc(g.nodes, g_test_indep(data))
    return {"true_edges": sorted(g.edges), "oracle": oracle, "data": from_data, "n": n,
            "class_size": len(equivalence_class(g)), "class": equivalence_class(g)}


# ---------------------------------------------------------------------------
# Mill's methods
# ---------------------------------------------------------------------------
def mill_difference(cases: list[dict], effect: str) -> dict:
    """Mill's method of difference (1843): two cases alike in every circumstance but one, the effect present in one
    and absent in the other; the differing circumstance is the cause (or part of it). And the method of agreement:
    the one circumstance common to all cases with the effect."""
    factors = [k for k in cases[0] if k != effect]
    diffs = []
    for a, b in itertools.combinations(cases, 2):
        if a[effect] != b[effect]:
            d = [f for f in factors if a[f] != b[f]]
            if len(d) == 1:
                diffs.append(d[0])
    with_e = [c for c in cases if c[effect]]
    agree = [f for f in factors if all(c[f] for c in with_e)]
    return {"difference": sorted(set(diffs)), "agreement": agree}


# ---------------------------------------------------------------------------
# Faithfulness, Berkson, and the firing squad
# ---------------------------------------------------------------------------
def hesslow() -> dict:
    """Hesslow (1976): birth-control pills P raise thrombosis T directly, and lower it by preventing pregnancy Q,
    which raises it. With these numbers the two paths cancel exactly: P and T are independent although P causes T,
    a violation of faithfulness."""
    pQ = {1: 0.0, 0: 0.5}           # pills prevent pregnancy
    pT = {(1, 0): 0.3, (0, 0): 0.1, (0, 1): 0.5, (1, 1): 0.7}   # P(T | P, Q)
    m = SCM(exo={"Up": bern(0.5), "Uq": [(k / 20, 0.05) for k in range(20)], "Ut": [(k / 20, 0.05) for k in range(20)]},
            eqs={"P": (["Up"], lambda u: u),
                 "Q": (["P", "Uq"], lambda p, u: int(u < pQ[p])),
                 "T": (["P", "Q", "Ut"], lambda p, q, u: int(u < pT[(p, q)]))})
    t1 = m.prob(lambda w: w["T"] == 1, given=lambda w: w["P"] == 1)
    t0 = m.prob(lambda w: w["T"] == 1, given=lambda w: w["P"] == 0)
    direct = m.prob(lambda w: w["T"] == 1, given=lambda w: w["P"] == 1 and w["Q"] == 0) - \
        m.prob(lambda w: w["T"] == 1, given=lambda w: w["P"] == 0 and w["Q"] == 0)
    return {"P(T|pill)": t1, "P(T|no pill)": t0, "direct_effect_given_not_pregnant": direct}


def berkson(n: int = 20000, seed: int = 1946) -> dict:
    """Talent and looks independent in the population; actors are those with talent + looks above a threshold.
    Among actors the two are negatively correlated: conditioning on a collider."""
    rng = np.random.default_rng(seed)
    t = rng.normal(size=n)
    lk = rng.normal(size=n)
    sel = t + lk > 1.5
    return {"all": float(np.corrcoef(t, lk)[0, 1]), "selected": float(np.corrcoef(t[sel], lk[sel])[0, 1]),
            "share_selected": float(sel.mean()), "sample_t": t[:600].tolist(), "sample_l": lk[:600].tolist(),
            "sample_sel": sel[:600].tolist()}


def firing_squad() -> dict:
    """Pearl's firing squad: a court order U (p), the captain C signals, riflemen A and B shoot, the prisoner D
    dies. Rung 1: P(D | A). Rung 2: P(D | do(A)). Rung 3: given that the prisoner is dead, would he be dead had A
    not shot? (Yes: B shot.) And: had A shot without orders?"""
    p = 0.7
    m = SCM(exo={"U": bern(p)},
            eqs={"C": (["U"], lambda u: u), "A": (["C"], lambda c: c), "B": (["C"], lambda c: c),
                 "D": (["A", "B"], lambda a, b: int(a or b))})
    return {"p_order": p,
            "rung1_P(D|A)": m.prob(lambda w: w["D"] == 1, given=lambda w: w["A"] == 1),
            "rung1_P(D|not A)": m.prob(lambda w: w["D"] == 1, given=lambda w: w["A"] == 0),
            "rung2_P(D|do A=0)": m.prob(lambda w: w["D"] == 1, do={"A": 0}),
            "rung2_P(D|do A=1)": m.prob(lambda w: w["D"] == 1, do={"A": 1}),
            "rung3_dead_had_A_not_shot": m.counterfactual(lambda w: w["D"] == 1, {"A": 0}, lambda w: w["D"] == 1),
            "rung3_dead_if_A_shot_given_alive": m.counterfactual(lambda w: w["D"] == 1, {"A": 1},
                                                                lambda w: w["D"] == 0)}


def nonidentifiable() -> dict:
    """Two models with the same observational distribution over X, Y and different P(Y | do(X)): no amount of
    passive data decides between them (the bow arc)."""
    m1 = SCM(exo={"Ux": bern(0.5), "Uy": bern(0.2)},
             eqs={"X": (["Ux"], lambda u: u), "Y": (["X", "Uy"], lambda x, u: int(x != u))})
    m2 = SCM(exo={"U": bern(0.5), "Uy": bern(0.2)},
             eqs={"X": (["U"], lambda u: u), "Y": (["U", "Uy"], lambda u, uy: int(u != uy))})
    return {"obs1": {f"{k}": v for k, v in m1.joint(["X", "Y"]).items()},
            "obs2": {f"{k}": v for k, v in m2.joint(["X", "Y"]).items()},
            "do1": m1.prob(lambda w: w["Y"] == 1, do={"X": 1}) - m1.prob(lambda w: w["Y"] == 1, do={"X": 0}),
            "do2": m2.prob(lambda w: w["Y"] == 1, do={"X": 1}) - m2.prob(lambda w: w["Y"] == 1, do={"X": 0})}


# ---------------------------------------------------------------------------
# Potential outcomes: IV and difference in differences
# ---------------------------------------------------------------------------
def instrumental(n: int = 50000, seed: int = 1928, beta: float = 0.5) -> dict:
    """Linear model: hidden U raises both X and Y; Z shifts X only. OLS of Y on X is biased; the Wald/IV estimator
    cov(Z, Y) / cov(Z, X) recovers beta (Philip Wright 1928)."""
    rng = np.random.default_rng(seed)
    U = rng.normal(size=n)
    Z = rng.normal(size=n)
    X = 0.8 * Z + U + rng.normal(size=n)
    Y = beta * X + 1.5 * U + rng.normal(size=n)
    ols = float(np.cov(X, Y)[0, 1] / np.var(X, ddof=1))
    iv = float(np.cov(Z, Y)[0, 1] / np.cov(Z, X)[0, 1])
    return {"beta": beta, "ols": ols, "iv": iv, "n": n}


def diff_in_diff() -> dict:
    """Card and Krueger's design in miniature: employment per restaurant in New Jersey (treated: a minimum-wage
    rise) and Pennsylvania (control), before and after. Illustrative numbers close to the published means."""
    nj = (20.4, 21.0)
    pa = (23.3, 21.2)
    did = (nj[1] - nj[0]) - (pa[1] - pa[0])
    return {"NJ": nj, "PA": pa, "naive_after": nj[1] - pa[1], "before_after_NJ": nj[1] - nj[0], "did": did}


# ---------------------------------------------------------------------------
# The do-calculus, checked rule by rule
# ---------------------------------------------------------------------------
def calculus_rule(g: DAG, rule: int, Y: set, X: set, Z: set, W: set) -> bool:
    """The side condition of Pearl's (1995) rule 1, 2 or 3 for P(y | do(x), [do](z), w):
    1: (Y _||_ Z | X, W) in G with arrows into X removed;
    2: (Y _||_ Z | X, W) in G with arrows into X and out of Z removed;
    3: (Y _||_ Z | X, W) in G with arrows into X and into Z(W) removed, Z(W) = the Z not ancestors of W there."""
    gx = g.remove_in_edges(X)
    if rule == 1:
        h = gx
    elif rule == 2:
        h = DAG([(a, b) for a, b in gx.edges if a not in Z], g.nodes)
    else:
        anc = gx.ancestors(W) if W else set()
        zw = {z for z in Z if z not in anc}
        h = DAG([(a, b) for a, b in gx.edges if b not in zw], g.nodes)
    return h.dsep(Y, Z, X | W)


def frontdoor_derivation() -> dict:
    """The front-door formula derived in the do-calculus, on S -> T -> C with a hidden U into S and C. Each step's
    side condition is checked by d-separation; the bow arc (X -> Y with U into both) admits no step at all."""
    g = DAG([("U", "S"), ("U", "C"), ("S", "T"), ("T", "C")])
    steps = [
        {"step": "P(t | do(s)) = P(t | s)", "rule": 2, "ok": calculus_rule(g, 2, {"T"}, set(), {"S"}, set())},
        {"step": "P(c | do(s), t) = P(c | do(s), do(t))", "rule": 2,
         "ok": calculus_rule(g, 2, {"C"}, {"S"}, {"T"}, set())},
        {"step": "P(c | do(s), do(t)) = P(c | do(t))", "rule": 3,
         "ok": calculus_rule(g, 3, {"C"}, {"T"}, {"S"}, set())},
        {"step": "P(c | do(t)) = sum_s' P(c | t, s') P(s')", "rule": 2,
         "ok": calculus_rule(g, 2, {"C"}, {"S"}, {"T"}, set()) and backdoor_ok(g, "T", "C", {"S"})},
    ]
    bow = DAG([("U", "X"), ("U", "Y"), ("X", "Y")])
    bow_rules = {"rule 2 (do(x) to x)": calculus_rule(bow, 2, {"Y"}, set(), {"X"}, set()),
                 "rule 3 (delete do(x))": calculus_rule(bow, 3, {"Y"}, set(), {"X"}, set())}
    # a wrong step, for contrast: in the front-door graph, do(s) cannot simply become s
    wrong = calculus_rule(g, 2, {"C"}, set(), {"S"}, set())
    return {"steps": steps, "bow": bow_rules, "wrong_P(c|do s)=P(c|s)": wrong}


def m_bias() -> dict:
    """M-bias: a pre-treatment variable M that is a collider of two hidden causes, one of X and one of Y. M is not a
    confounder; adjusting for it opens the path X <- U1 -> M <- U2 -> Y and creates bias."""
    m = SCM(
        exo={"U1": bern(0.5), "U2": bern(0.5), "Ux": bern(0.2), "Ur": [(k, 0.05) for k in range(20)]},
        eqs={"X": (["U1", "Ux"], lambda u1, ux: int(u1 != ux)),
             "M": (["U1", "U2"], lambda u1, u2: int(u1 == 1 and u2 == 1)),
             "Y": (["X", "U2", "Ur"], lambda x, u2, ur: int(ur < 4 + 6 * x + 8 * u2))})
    naive = m.prob(lambda w: w["Y"] == 1, given=lambda w: w["X"] == 1) - \
        m.prob(lambda w: w["Y"] == 1, given=lambda w: w["X"] == 0)
    adj = backdoor_adjust(m, "X", 1, "Y", 1, ["M"]) - backdoor_adjust(m, "X", 0, "Y", 1, ["M"])
    truth = m.prob(lambda w: w["Y"] == 1, do={"X": 1}) - m.prob(lambda w: w["Y"] == 1, do={"X": 0})
    g = DAG([("U1", "X"), ("U1", "M"), ("U2", "M"), ("U2", "Y"), ("X", "Y")])
    return {"naive": naive, "adjusted_M": adj, "truth": truth, "criterion_empty": backdoor_ok(g, "X", "Y", set()),
            "criterion_M": backdoor_ok(g, "X", "Y", {"M"})}


def responsibility(n_for: int, n_against: int) -> dict:
    """Chockler and Halpern (2004): a voter's degree of responsibility for a majority outcome is 1 / (k + 1), where k
    is the least number of other votes that must change before the outcome depends on hers. Brute force over the
    other voters, with a model per election."""
    n = n_for + n_against
    need = n // 2 + 1
    votes = [1] * n_for + [0] * n_against
    others = list(range(1, n_for))           # voter 0 voted for the winner; flip others who also did
    for k in range(len(others) + 1):
        for flip in itertools.combinations(others, k):
            v = list(votes)
            for i in flip:
                v[i] = 0
            if sum(v) >= need and sum(v) - 1 < need:
                return {"n_for": n_for, "n_against": n_against, "k": k, "degree": 1 / (k + 1)}
    return {"n_for": n_for, "n_against": n_against, "k": None, "degree": 0.0}


# ---------------------------------------------------------------------------
# The common cause principle and its limits
# ---------------------------------------------------------------------------
def yule_walks(pairs: int = 2000, T: int = 100, seed: int = 1926) -> dict:
    """Yule's (1926) nonsense correlations: pairs of independent random walks are often strongly correlated, with no
    common cause at all; their increments are not."""
    rng = np.random.default_rng(seed)
    rs, rds, best = [], [], None
    for i in range(pairs):
        a = np.cumsum(rng.normal(size=T))
        b = np.cumsum(rng.normal(size=T))
        r = float(np.corrcoef(a, b)[0, 1])
        rd = float(np.corrcoef(np.diff(a), np.diff(b))[0, 1])
        rs.append(r)
        rds.append(rd)
        if best is None and r > 0.85:
            best = {"a": a.round(3).tolist(), "b": b.round(3).tolist(), "r": r, "r_diff": rd}
    rs, rds = np.array(rs), np.array(rds)
    hist = np.histogram(rs, bins=20, range=(-1, 1))[0].tolist()
    hist_d = np.histogram(rds, bins=20, range=(-1, 1))[0].tolist()
    return {"pairs": pairs, "T": T, "frac_abs_r_gt_0.5": float(np.mean(np.abs(rs) > 0.5)),
            "frac_diff_abs_r_gt_0.5": float(np.mean(np.abs(rds) > 0.5)), "hist": hist, "hist_diff": hist_d,
            "example": best}


def chsh() -> dict:
    """Bell's theorem in the CHSH form. Any local common cause (a hidden variable fixing each side's outcome for each
    setting, here every deterministic strategy and so every mixture) gives |S| <= 2; the singlet state, with
    E(a, b) = -cos(a - b) at the optimal angles, gives 2 sqrt 2."""
    best = 0
    for a0, a1, b0, b1 in itertools.product([-1, 1], repeat=4):
        s = a0 * b0 + a0 * b1 + a1 * b0 - a1 * b1
        best = max(best, abs(s))
    A, A2, B, B2 = 0.0, math.pi / 2, math.pi / 4, -math.pi / 4

    def E(x, y):
        return -math.cos(x - y)
    q = abs(E(A, B) + E(A, B2) + E(A2, B) - E(A2, B2))
    return {"local_max": best, "quantum": q, "tsirelson": 2 * math.sqrt(2), "strategies": 16}


def lingam_demo(n: int = 5000, seed: int = 2006) -> dict:
    """Beyond the equivalence class (Shimizu et al. 2006): in a linear model with non-Gaussian noise, only the true
    direction leaves a residual independent of the regressor. Dependence is scored by the correlation of squares
    (zero under independence; ordinary correlation is zero either way). With Gaussian noise both directions fit."""
    rng = np.random.default_rng(seed)

    def fit(a, b):
        beta = float(np.cov(a, b)[0, 1] / np.var(a, ddof=1))
        r = b - beta * a
        return r, float(abs(np.corrcoef(r ** 2, a ** 2)[0, 1])), float(abs(np.corrcoef(r, a)[0, 1]))
    out = {}
    for kind in ("uniform", "gaussian"):
        if kind == "uniform":
            X = rng.uniform(-1, 1, n)
            Y = X + 0.8 * rng.uniform(-1, 1, n)
        else:
            X = rng.normal(size=n)
            Y = X + 0.8 * rng.normal(size=n)
        rf, df, cf = fit(X, Y)
        rb, db, cb = fit(Y, X)
        out[kind] = {"forward_dep": df, "backward_dep": db, "forward_corr": cf, "backward_corr": cb,
                     "forward_pts": np.c_[X[:400], rf[:400]].round(3).tolist(),
                     "backward_pts": np.c_[Y[:400], rb[:400]].round(3).tolist()}
    return out


def perfect_doctor() -> dict:
    """Rubin's perfect doctor (after Imbens and Rubin 2015): eight patients with both potential outcomes (years
    lived) known. The doctor gives each patient the better option; the observed comparison misleads. Every balanced
    randomization (70 of them) is enumerated: their differences in means average exactly to the true ATE."""
    y0 = [13, 6, 4, 5, 6, 6, 8, 8]
    y1 = [14, 0, 1, 2, 3, 1, 10, 9]
    n = len(y0)
    ate = sum(a - b for a, b in zip(y1, y0)) / n
    doc = [int(a > b) for a, b in zip(y1, y0)]
    obs = [y1[i] if doc[i] else y0[i] for i in range(n)]
    t = [obs[i] for i in range(n) if doc[i]]
    c = [obs[i] for i in range(n) if not doc[i]]
    naive = sum(t) / len(t) - sum(c) / len(c)
    diffs = []
    for T in itertools.combinations(range(n), n // 2):
        tt = [y1[i] for i in T]
        cc = [y0[i] for i in range(n) if i not in T]
        diffs.append(sum(tt) / len(tt) - sum(cc) / len(cc))
    return {"y0": y0, "y1": y1, "ate": ate, "doctor": doc, "observed": obs, "naive": naive,
            "rand_mean": sum(diffs) / len(diffs), "rand_diffs": sorted(diffs), "n_assign": len(diffs),
            "frac_wrong_sign": sum(1 for x in diffs if x > 0) / len(diffs)}


# ---------------------------------------------------------------------------
# Causes at work
# ---------------------------------------------------------------------------
def cuped(n: int = 20000, rho: float = 0.7, effect: float = 0.03, reps: int = 400, seed: int = 2013) -> dict:
    """CUPED (Deng, Xu, Kohavi and Walker 2013): subtract theta * (pre-period metric - its mean) from each user's
    metric. The estimate stays unbiased and its variance falls by the factor 1 - rho^2."""
    rng = np.random.default_rng(seed)
    plain, adj = [], []
    for _ in range(reps):
        pre = rng.normal(size=n)
        y = rho * pre + math.sqrt(1 - rho ** 2) * rng.normal(size=n)
        t = rng.integers(0, 2, n)
        y = y + effect * t
        theta = np.cov(pre, y)[0, 1] / np.var(pre, ddof=1)
        ya = y - theta * (pre - pre.mean())
        plain.append(y[t == 1].mean() - y[t == 0].mean())
        adj.append(ya[t == 1].mean() - ya[t == 0].mean())
    plain, adj = np.array(plain), np.array(adj)
    return {"rho": rho, "effect": effect, "n": n, "reps": reps, "mean_plain": float(plain.mean()),
            "mean_cuped": float(adj.mean()), "sd_plain": float(plain.std()), "sd_cuped": float(adj.std()),
            "var_ratio": float(adj.var() / plain.var()), "theory": 1 - rho ** 2}


def uplift_demo(n: int = 200000, seed: int = 2002, budget: float = 0.2) -> dict:
    """Uplift modelling on a randomized campaign. Customers fall into 16 segments, each a mix of four types: sure
    things (buy anyway), persuadables (buy only if contacted), lost causes, and sleeping dogs (contact puts them off).
    From the trial data, rank segments by response rate when contacted, or by uplift (response contacted minus not),
    contact the top `budget` share, and count the purchases the contact actually caused."""
    rng = np.random.default_rng(seed)
    segs = []
    for i in range(16):
        a, b = divmod(i, 4)
        w = np.array([0.05 + 0.15 * a, 0.02 + 0.08 * b * (3 - a) / 3, 0.5, 0.03 + 0.07 * a])
        segs.append(w / w.sum())
    seg = rng.integers(0, 16, n)
    u = rng.random(n)
    typ = np.array([np.searchsorted(np.cumsum(segs[s]), x) for s, x in zip(seg, u)])
    typ = np.minimum(typ, 3)
    t = rng.integers(0, 2, n)
    y1 = np.isin(typ, [0, 1]).astype(int)
    y0 = np.isin(typ, [0, 3]).astype(int)
    y = np.where(t == 1, y1, y0)
    resp, upl, true_upl, size = [], [], [], []
    for s in range(16):
        m = seg == s
        r1 = y[m & (t == 1)].mean()
        r0 = y[m & (t == 0)].mean()
        resp.append(r1)
        upl.append(r1 - r0)
        true_upl.append(float(segs[s][1] - segs[s][3]))
        size.append(m.mean())
    k = int(round(budget * 16))

    def gain(order):
        return float(sum(true_upl[s] * size[s] for s in order[:k]) * n)
    by_resp = list(np.argsort(resp)[::-1])
    by_upl = list(np.argsort(upl)[::-1])
    return {"n": n, "segments": 16, "contacted_segments": k, "gain_response": gain(by_resp),
            "gain_uplift": gain(by_upl), "gain_random": float(sum(true_upl[s] * size[s] for s in range(16)) * n * k / 16),
            "best_possible": gain(list(np.argsort(true_upl)[::-1])),
            "resp": [float(x) for x in resp], "uplift": [float(x) for x in upl], "true_uplift": true_upl}


def icp_demo(n: int = 5000, seed: int = 2016) -> dict:
    """Invariant causal prediction (Peters, Buhlmann and Meinshausen 2016) in miniature: X causes Y, Y causes Z. In a
    second environment X's distribution is shifted and Z's mechanism changes. Regressing Y on its cause gives the same
    coefficient in both; regressing Y on its effect does not."""
    rng = np.random.default_rng(seed)
    out = {}
    for env, (sx, mx, gz) in {"1": (1.0, 0.0, 1.0), "2": (2.0, 1.5, 0.4)}.items():
        X = mx + sx * rng.normal(size=n)
        Y = 1.0 * X + rng.normal(size=n)
        Z = gz * Y + 0.5 * rng.normal(size=n)
        bx = float(np.cov(X, Y)[0, 1] / np.var(X, ddof=1))
        bz = float(np.cov(Z, Y)[0, 1] / np.var(Z, ddof=1))
        out[env] = {"Y_on_X": bx, "Y_on_Z": bz}
    return out
