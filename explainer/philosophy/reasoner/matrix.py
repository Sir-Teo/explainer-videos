"""Logics beyond true and false, exactly: matrices, four values, degrees, the sorites, resources and subspaces.

    from explainer.philosophy.reasoner.matrix import K3, LP, L3, FDE, consequence, sorites_classical
    consequence(["p", "~p"], "q", LP)          # (False, {'p': 1/2, 'q': 0}): explosion fails in LP
    consequence(["p", "p -> q"], "q", LP)      # (False, ...): so does modus ponens

A *logical matrix* (Łukasiewicz 1920; Łoś and Suszko 1958) is a set of values, a subset of *designated* values
(the ones that count as holding), and a table for each connective. An argument is valid in the matrix when every
valuation that designates all the premises designates the conclusion. Everything is decided by enumerating the
valuations, so every claim on screen can be checked by brute force; ``tests/philosophy/test_matrix.py`` does.

Formulas are the nested tuples of :mod:`prop` (``("var", "p")``, ``("not", A)``, ``("and", A, B)``, ...), parsed
by ``prop.parse``. Values of the three-valued logics are ``Fraction`` 0, 1/2, 1; FDE's are the strings
``"t" "f" "b" "n"`` (and Priest's fifth, ``"e"``).
"""

from __future__ import annotations

import itertools
from dataclasses import dataclass, field
from fractions import Fraction as Fr
from typing import Callable

import numpy as np

from explainer.philosophy.reasoner import prop

H = Fr(1, 2)
ZERO, ONE = Fr(0), Fr(1)


# ---------------------------------------------------------------------------
# Matrices
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class Matrix:
    """A finite logical matrix. ``neg`` maps a value; ``conj``, ``disj``, ``imp`` map two; ``top``/``bot`` are
    the values of ⊤ and ⊥; ``names`` gives each value a short label."""
    name: str
    values: tuple
    designated: frozenset
    neg: Callable
    conj: Callable
    disj: Callable
    imp: Callable
    top: object
    bot: object
    names: dict = field(default_factory=dict)

    def label(self, v) -> str:
        return self.names.get(v, str(v))

    def iff(self, a, b):
        return self.conj(self.imp(a, b), self.imp(b, a))


def _kleene_imp(a, b):
    return max(1 - a, b)


def _three(name, designated, imp, conj=min, disj=max):
    vals = (ZERO, H, ONE)
    return Matrix(name, vals, frozenset(designated), lambda a: 1 - a, conj, disj, imp, ONE, ZERO,
                  {ZERO: "0", H: r"\tfrac12", ONE: "1"})


def _luk_imp(a, b):
    return min(ONE, 1 - a + b)


def _godel_imp(a, b):
    return ONE if a <= b else b


def _rm3_imp(a, b):
    return max(1 - a, b) if a <= b else min(1 - a, b)


def _weak(op):
    def f(a, b):
        return H if H in (a, b) else op(a, b)
    return f


CL = Matrix("CL", (ZERO, ONE), frozenset({ONE}), lambda a: 1 - a, min, max, _kleene_imp, ONE, ZERO,
            {ZERO: "0", ONE: "1"})
K3 = _three("K3", {ONE}, _kleene_imp)            # Kleene 1938/1952: strong tables, a gap
LP = _three("LP", {ONE, H}, _kleene_imp)         # Asenjo 1966, Priest 1979: the same tables, a glut
L3 = _three("Ł3", {ONE}, _luk_imp)               # Łukasiewicz 1920
G3 = Matrix("G3", (ZERO, H, ONE), frozenset({ONE}), lambda a: ONE if a == 0 else ZERO, min, max, _godel_imp, ONE,
            ZERO, {ZERO: "0", H: r"\tfrac12", ONE: "1"})   # Gödel 1932 / Heyting's three-valued
RM3 = _three("RM3", {ONE, H}, _rm3_imp)          # Sobociński 1952: a relevant matrix
B3 = Matrix("B3", (ZERO, H, ONE), frozenset({ONE}), lambda a: 1 - a, _weak(min), _weak(max), _weak(_kleene_imp),
            ONE, ZERO, {ZERO: "0", H: r"\tfrac12", ONE: "1"})  # Bochvar 1938: weak Kleene, nonsense infects

# Belnap 1977 / Dunn 1976: a value is what a computer has been *told*: (told true, told false)
_PAIR = {"t": (1, 0), "f": (0, 1), "b": (1, 1), "n": (0, 0)}
_UNPAIR = {v: k for k, v in _PAIR.items()}


def _fde_neg(a):
    if a == "e":
        return "e"
    t, f = _PAIR[a]
    return _UNPAIR[(f, t)]


def _fde_conj(a, b):
    if "e" in (a, b):
        return "e"
    (t1, f1), (t2, f2) = _PAIR[a], _PAIR[b]
    return _UNPAIR[(t1 & t2, f1 | f2)]


def _fde_disj(a, b):
    if "e" in (a, b):
        return "e"
    (t1, f1), (t2, f2) = _PAIR[a], _PAIR[b]
    return _UNPAIR[(t1 | t2, f1 & f2)]


FDE = Matrix("FDE", ("t", "b", "n", "f"), frozenset({"t", "b"}), _fde_neg, _fde_conj, _fde_disj,
             lambda a, b: _fde_disj(_fde_neg(a), b), "t", "f", {"t": "T", "f": "F", "b": "B", "n": "N"})
# Priest 2010, `The Logic of the Catuskoti': a fifth value, emptiness, which infects whatever it touches
FDE_E = Matrix("FDE$_e$", ("t", "b", "n", "f", "e"), frozenset({"t", "b"}), _fde_neg, _fde_conj, _fde_disj,
               lambda a, b: _fde_disj(_fde_neg(a), b), "t", "f", {"t": "T", "f": "F", "b": "B", "n": "N", "e": "E"})

MATRICES = {m.name: m for m in (CL, K3, LP, L3, G3, RM3, B3, FDE)}


def _f(x):
    return prop.parse(x) if isinstance(x, str) else x


def evaluate(f, v: dict, M: Matrix):
    """The value of formula ``f`` under the valuation ``v`` (atom -> value) in matrix ``M``."""
    f = _f(f)
    op = f[0]
    if op == "var":
        return v[f[1]]
    if op == "top":
        return M.top
    if op == "bot":
        return M.bot
    if op == "not":
        return M.neg(evaluate(f[1], v, M))
    a, b = evaluate(f[1], v, M), evaluate(f[2], v, M)
    return {"and": M.conj, "or": M.disj, "imp": M.imp, "iff": M.iff}[op](a, b)


def valuations(names, M: Matrix):
    for combo in itertools.product(M.values, repeat=len(names)):
        yield dict(zip(names, combo))


def consequence(premises, conclusion, M: Matrix) -> tuple[bool, dict | None]:
    """Is ``premises ⊨ conclusion`` in ``M``? Returns (valid, the first countermodel found or None)."""
    ps = [_f(p) for p in premises]
    c = _f(conclusion)
    names = prop.atoms_of(ps + [c])
    for v in valuations(names, M):
        if all(evaluate(p, v, M) in M.designated for p in ps) and evaluate(c, v, M) not in M.designated:
            return False, v
    return True, None


def tautology(f, M: Matrix) -> tuple[bool, dict | None]:
    return consequence([], f, M)


def table(M: Matrix, op: str) -> list[list]:
    """The table of a connective: for ``not`` a list of (a, ¬a); for binary ones, rows a, columns b."""
    if op == "not":
        return [[a, M.neg(a)] for a in M.values]
    fn = {"and": M.conj, "or": M.disj, "imp": M.imp, "iff": M.iff}[op]
    return [[fn(a, b) for b in M.values] for a in M.values]


INFERENCES = {
    "explosion": (["p", "~p"], "q"),
    "LEM": ([], "p | ~p"),
    "MP": (["p", "p -> q"], "q"),
    "identity": ([], "p -> p"),
    "DS": (["p | q", "~p"], "q"),
    "weakening": (["p"], "q -> p"),
    "contraposition": (["p -> q"], "~q -> ~p"),
    "DNE": (["~~p"], "p"),
    "noncontradiction": ([], "~(p & ~p)"),
}


def compare(inferences=None, matrices=None) -> dict:
    """{inference: {matrix name: (valid, countermodel)}} over the chosen inferences and matrices."""
    inferences = inferences or INFERENCES
    matrices = matrices or [CL, K3, LP, L3, FDE]
    return {k: {M.name: consequence(ps, c, M) for M in matrices} for k, (ps, c) in inferences.items()}


def lpm_consequence(premises, conclusion) -> tuple[bool, dict | None]:
    """Priest's minimally inconsistent LP (1991): the conclusion must hold in every LP model of the premises whose
    set of glutted atoms (value 1/2) is minimal under inclusion. Where the premises are consistent this is classical
    consequence (disjunctive syllogism returns); where they are not, explosion still fails."""
    ps = [_f(p) for p in premises]
    c = _f(conclusion)
    names = prop.atoms_of(ps + [c])
    models = [v for v in valuations(names, LP) if all(evaluate(p, v, LP) in LP.designated for p in ps)]
    gl = [frozenset(k for k, x in v.items() if x == H) for v in models]
    minimal = [v for v, g in zip(models, gl) if not any(h < g for h in gl)]
    for v in minimal:
        if evaluate(c, v, LP) not in LP.designated:
            return False, v
    return True, None


# ---------------------------------------------------------------------------
# FOUR as a bilattice (Ginsberg 1988; Fitting 1991)
# ---------------------------------------------------------------------------
def truth_leq(a, b) -> bool:
    """The truth order on FOUR: f below n and b, both below t (more told true, less told false)."""
    (t1, f1), (t2, f2) = _PAIR[a], _PAIR[b]
    return t1 <= t2 and f1 >= f2


def info_leq(a, b) -> bool:
    """The information order: n below t and f, both below b (told more)."""
    (t1, f1), (t2, f2) = _PAIR[a], _PAIR[b]
    return t1 <= t2 and f1 <= f2


def lattice_meet(a, b, leq) -> str:
    lower = [x for x in "tbnf" if leq(x, a) and leq(x, b)]
    return next(x for x in lower if all(leq(y, x) for y in lower))


def lattice_join(a, b, leq) -> str:
    upper = [x for x in "tbnf" if leq(a, x) and leq(b, x)]
    return next(x for x in upper if all(leq(x, y) for y in upper))


# ---------------------------------------------------------------------------
# The four corners and the seven predications
# ---------------------------------------------------------------------------
CATUSKOTI = [("t", r"it is", r"\textit{asti}"), ("f", r"it is not", r"\textit{nāsti}"),
             ("b", r"it both is and is not", r"\textit{ubhaya}"), ("n", r"it neither is nor is not", r"\textit{anubhaya}")]


def saptabhangi() -> list[tuple]:
    """Priest's reconstruction (2008): from each standpoint a claim is true (t), false (f) or inexpressible (i); a
    claim's predication is the set of values it takes across standpoints. The nonempty subsets of {t, f, i} are the
    seven *bhaṅgas*, in the traditional order."""
    order = [("t",), ("f",), ("t", "f"), ("i",), ("t", "i"), ("f", "i"), ("t", "f", "i")]
    subsets = {tuple(sorted(c, key="tfi".index)) for r in (1, 2, 3) for c in itertools.combinations("tfi", r)}
    assert subsets == set(order)
    return order


# ---------------------------------------------------------------------------
# Intuitionistic logic has no finite matrix (Gödel 1932)
# ---------------------------------------------------------------------------
def godel_matrix(n: int) -> Matrix:
    """Gödel's n-valued chain 0 < 1/(n-1) < ... < 1: min, max, a → b = 1 if a ≤ b else b, ¬a = a → 0."""
    vals = tuple(Fr(i, n - 1) for i in range(n))
    return Matrix(f"G{n}", vals, frozenset({ONE}), lambda a: ONE if a == 0 else ZERO, min, max, _godel_imp, ONE,
                  ZERO)


def godel_disjunction(n: int):
    """⋁_{i<j≤n} (p_i ↔ p_j): with n+1 atoms and only n values, two atoms must agree (the pigeonhole), so it is
    valid in G_n; in G_{n+1} the atoms can all differ, so it fails, and it is not intuitionistically valid."""
    ps = [prop.Var(f"p{i}") for i in range(n + 1)]
    return prop.Or(*[prop.Iff(a, b) for a, b in itertools.combinations(ps, 2)])


# ---------------------------------------------------------------------------
# Degrees: t-norms and their residua
# ---------------------------------------------------------------------------
TNORMS = {
    "Gödel": (lambda a, b: min(a, b), lambda a, b: 1.0 if a <= b else b),
    "product": (lambda a, b: a * b, lambda a, b: 1.0 if a <= b else b / a),
    "Łukasiewicz": (lambda a, b: max(0.0, a + b - 1), lambda a, b: min(1.0, 1 - a + b)),
}


def residuum_check(name: str, steps: int = 21) -> bool:
    """The residuation law t(a, c) ≤ b iff c ≤ (a → b), on a grid: what makes → the right partner of ∧."""
    t, r = TNORMS[name]
    g = [i / (steps - 1) for i in range(steps)]
    eps = 1e-12
    return all((t(a, c) <= b + eps) == (c <= r(a, b) + eps) for a in g for b in g for c in g)


# ---------------------------------------------------------------------------
# Fuzzy control: a train stopping at a platform (after Yasunobu and Miyamoto, Sendai 1987)
# ---------------------------------------------------------------------------
def tri(x, a, b, c):
    """A triangular membership function rising from a to its peak at b and falling to c (shoulders if a == b or
    b == c)."""
    if x <= a:
        return 1.0 if a == b else 0.0
    if x >= c:
        return 1.0 if b == c else 0.0
    return (x - a) / (b - a) if x < b else (c - x) / (c - b)


DIST = {"near": (0, 0, 80), "mid": (25, 180, 280), "far": (250, 400, 400)}        # metres to the stop mark
SPEED = {"slow": (0, 0, 8), "medium": (4, 11, 18), "fast": (14, 22, 22)}         # metres per second
BRAKE = {"none": (0.0, 0.0, 0.3), "light": (0.1, 0.4, 0.7), "firm": (0.5, 0.8, 1.0), "hard": (0.8, 1.0, 1.0)}
RULES = [("far", "slow", "none"), ("far", "medium", "none"), ("far", "fast", "none"),
         ("mid", "slow", "none"), ("mid", "medium", "light"), ("mid", "fast", "firm"),
         ("near", "slow", "light"), ("near", "medium", "firm"), ("near", "fast", "hard")]


def fuzzy_brake(d: float, s: float, grid: int = 101) -> dict:
    """Mamdani inference: each rule fires to the degree min(μ_dist, μ_speed), clips its output set, the clipped
    sets are combined by max, and the brake is the centroid."""
    fire = [(min(tri(d, *DIST[a]), tri(s, *SPEED[b])), c) for a, b, c in RULES]
    xs = [i / (grid - 1) for i in range(grid)]
    agg = [max([min(w, tri(x, *BRAKE[c])) for w, c in fire] + [0.0]) for x in xs]
    tot = sum(agg)
    out = sum(x * m for x, m in zip(xs, agg)) / tot if tot > 0 else 0.0
    return {"fire": fire, "agg": agg, "xs": xs, "brake": out}


def simulate_stop(controller: str, d0: float = 600.0, v0: float = 20.0, dt: float = 0.25, a_max: float = 1.2,
                  t_max: float = 120.0) -> dict:
    """A train runs at v0 towards a stop mark d0 metres ahead. ``fuzzy``: the brake is the fuzzy controller's;
    ``bang``: full brake once the stopping distance v²/(2a) reaches the remaining distance, none before (a
    classical two-valued rule). Returns times, positions, speeds, accelerations, the stopping error and the worst
    jerk (change of acceleration per second, what passengers feel)."""
    t, x, v = 0.0, 0.0, v0
    ts, xs, vs, accs = [0.0], [0.0], [v0], [0.0]
    while v > 0.05 and t < t_max:
        d = d0 - x
        if controller == "fuzzy":
            b = fuzzy_brake(max(d, 0.0), v)["brake"]
        else:
            b = 1.0 if v * v / (2 * a_max) >= d - 1.0 else 0.0
        a = -a_max * b
        v = max(0.0, v + a * dt)
        x += v * dt
        t += dt
        ts.append(t)
        xs.append(x)
        vs.append(v)
        accs.append(a)
    jerk = max(abs(accs[i + 1] - accs[i]) / dt for i in range(len(accs) - 1))
    return {"t": ts, "x": xs, "v": vs, "a": accs, "error": xs[-1] - d0, "jerk": jerk, "time": t}


# ---------------------------------------------------------------------------
# The sorites
# ---------------------------------------------------------------------------
def sorites_premises(n: int):
    """Man i has i hundred hairs... any unit will do. B_i: man i is bald. B_0; B_i → B_{i+1} for i < n; ¬B_n."""
    B = [prop.Var(f"B{i}") for i in range(n + 1)]
    return B, [B[0]] + [prop.Imp(B[i], B[i + 1]) for i in range(n)] + [prop.Not(B[n])]


def sorites_classical(n: int) -> dict:
    """Classically the n + 2 premises are inconsistent, and every one of them is needed: drop any one and a
    valuation satisfies the rest. So the set is a minimal unsatisfiable set; the cutoffs are the models of what
    is left after dropping a conditional."""
    _, prem = sorites_premises(n)
    whole = prop.satisfiable(prem)
    needed = [not prop.satisfiable(prem[:i] + prem[i + 1:]) for i in range(len(prem))]
    return {"n": n, "premises": len(prem), "consistent": whole, "every_premise_needed": not any(needed)}


def sharpenings(n: int, lo: int, hi: int) -> list[int]:
    """The admissible sharpenings of `bald' on men 0..n with clear cases below lo and above hi: a cutoff k with
    lo < k ≤ hi; man i is bald on sharpening k iff i < k."""
    return list(range(lo + 1, hi + 1))


def supervaluate(f, n: int, lo: int, hi: int) -> str:
    """Fine (1975): a sentence is *super-true* if true on every admissible sharpening, *super-false* if false on
    every one, and otherwise indeterminate. Returns 'T', 'F' or 'I'."""
    f = _f(f)
    vals = {prop.evaluate(f, {f"B{i}": i < k for i in range(n + 1)}) for k in sharpenings(n, lo, hi)}
    return "T" if vals == {True} else "F" if vals == {False} else "I"


def cutoff_sentence(n: int):
    """∃i (B_i ∧ ¬B_{i+1}), as a finite disjunction: some man is bald and the next one is not."""
    return prop.Or(*[prop.And(prop.Var(f"B{i}"), prop.Not(prop.Var(f"B{i + 1}"))) for i in range(n)])


def supervaluation_report(n: int, lo: int, hi: int) -> dict:
    """The supervaluationist's verdicts on the sorites with men 0..n and the penumbra (lo, hi]."""
    B, prem = sorites_premises(n)
    cond = [supervaluate(p, n, lo, hi) for p in prem[1:-1]]
    return {"n": n, "lo": lo, "hi": hi, "sharpenings": len(sharpenings(n, lo, hi)),
            "bald": [supervaluate(b, n, lo, hi) for b in B],
            "conditionals": cond,
            "cutoff": supervaluate(cutoff_sentence(n), n, lo, hi),
            "lem": [supervaluate(prop.Or(b, prop.Not(b)), n, lo, hi) for b in B],
            "no_witness": all(supervaluate(prop.And(prop.Var(f"B{i}"), prop.Not(prop.Var(f"B{i + 1}"))), n, lo,
                                           hi) != "T" for i in range(n))}


def degrees(n: int, lo: int, hi: int) -> list[float]:
    """A degree theory's `bald': 1 up to lo, 0 from hi, falling linearly between."""
    return [1.0 if i <= lo else 0.0 if i >= hi else (hi - i) / (hi - lo) for i in range(n + 1)]


def degree_report(n: int, lo: int, hi: int) -> dict:
    """Łukasiewicz values of the conditionals B_i → B_{i+1} (each 1 − drop, so nearly 1), and what chained modus
    ponens guarantees: from x and x → y one may infer only y ≥ x + (x→y) − 1 (the Łukasiewicz t-norm), so the
    guarantee falls by the drop at every step and is used up long before the end."""
    d = degrees(n, lo, hi)
    cond = [min(1.0, 1 - d[i] + d[i + 1]) for i in range(n)]
    bound = [1.0]
    for c in cond:
        b = bound[-1] + c - 1
        bound.append(0.0 if b < 1e-9 else b)
    return {"degrees": d, "conditionals": cond, "min_conditional": min(cond), "mp_bound": bound}


def margin_report(n: int, cutoff: int, margin: int) -> dict:
    """Williamson (1994): `bald' has a sharp cutoff, but knowledge needs a margin for error: one knows man i is
    bald only if men within the margin are bald too. So the known cases stop short of the cutoff on both sides,
    and no one can know where it is."""
    bald = [i < cutoff for i in range(n + 1)]
    known_bald = [all(bald[j] for j in range(max(0, i - margin), min(n, i + margin) + 1)) for i in range(n + 1)]
    known_not = [all(not bald[j] for j in range(max(0, i - margin), min(n, i + margin) + 1)) for i in range(n + 1)]
    return {"bald": bald, "known_bald": known_bald, "known_not": known_not,
            "unknown": sum(1 for i in range(n + 1) if not known_bald[i] and not known_not[i])}


def tolerance_table(n: int = 10, lo: int = 3, hi: int = 7) -> dict:
    """The sorites quartet against five theories, each computed in its own semantics: does each theory keep
    (1) tolerance, every conditional B_i → B_{i+1}; (2) the extremes, B_0 and ¬B_n; (3) bivalence, every B_i
    true or false; (4) classical consequence (modus ponens chained)?"""
    B, prem = sorites_premises(n)
    conds = prem[1:-1]
    out = {}
    # epistemicism: one classical model with a cutoff in the penumbra
    k = (lo + hi + 1) // 2
    v = {f"B{i}": i < k for i in range(n + 1)}
    out["epistemicism"] = {"tolerance": all(prop.evaluate(c, v) for c in conds), "extremes": True,
                           "bivalence": True, "logic": True}
    # supervaluationism: conditionals super-true?
    sv = supervaluation_report(n, lo, hi)
    out["supervaluationism"] = {"tolerance": all(c == "T" for c in sv["conditionals"]),
                                "extremes": sv["bald"][0] == "T" and sv["bald"][-1] == "F",
                                "bivalence": all(b != "I" for b in sv["bald"]), "logic": True}
    # degree theory (Łukasiewicz, designated = 1): each conditional fully true?
    dr = degree_report(n, lo, hi)
    out["degrees"] = {"tolerance": dr["min_conditional"] == 1.0, "extremes": True,
                      "bivalence": all(x in (0.0, 1.0) for x in dr["degrees"]), "logic": True}
    # glut theory (LP, designated {1, 1/2}): borderline men are both bald and not
    val = {f"B{i}": ONE if i <= lo else ZERO if i >= hi else H for i in range(n + 1)}
    lp_conds = all(evaluate(c, val, LP) in LP.designated for c in conds)
    mp_ok, _ = consequence(["p", "p -> q"], "q", LP)
    out["gluts (LP)"] = {"tolerance": lp_conds, "extremes": True,
                         "bivalence": all(x != H for x in val.values()), "logic": mp_ok}
    # nihilism (Unger 1979): nobody is bald, or everyone; give up the extremes
    out["nihilism"] = {"tolerance": True, "extremes": False, "bivalence": True, "logic": True}
    return out


# ---------------------------------------------------------------------------
# Quantum logic: the lattice of subspaces (Birkhoff and von Neumann 1936)
# ---------------------------------------------------------------------------
def span(*vectors) -> np.ndarray:
    """An orthonormal basis (as rows) of the span of the vectors (rank by SVD)."""
    A = np.array([np.asarray(v, float) for v in vectors]) if vectors else np.zeros((0, 3))
    if A.size == 0:
        return np.zeros((0, A.shape[1] if A.ndim == 2 else 3))
    u, s, vt = np.linalg.svd(A)
    r = int((s > 1e-9).sum())
    return vt[:r]


def join(U: np.ndarray, V: np.ndarray) -> np.ndarray:
    """U ∨ V: the smallest subspace containing both (the span of the union)."""
    rows = [r for r in U] + [r for r in V]
    return span(*rows) if rows else U


def complement(U: np.ndarray, dim: int) -> np.ndarray:
    """U⊥: the orthogonal complement, quantum negation."""
    if len(U) == 0:
        return np.eye(dim)
    u, s, vt = np.linalg.svd(U)
    r = int((s > 1e-9).sum())
    return vt[r:]


def meet(U: np.ndarray, V: np.ndarray, dim: int) -> np.ndarray:
    """U ∧ V: the intersection, computed as (U⊥ ∨ V⊥)⊥."""
    return complement(join(complement(U, dim), complement(V, dim)), dim)


def same(U: np.ndarray, V: np.ndarray) -> bool:
    return len(U) == len(V) and (len(U) == 0 or np.linalg.matrix_rank(np.vstack([U, V]), tol=1e-9) == len(U))


def distributivity_counterexample() -> dict:
    """Three lines through the origin of a plane: p the x-axis, q the y-axis, r the diagonal. Then q ∨ r is the
    whole plane, so p ∧ (q ∨ r) = p; but p ∧ q and p ∧ r are both the zero space, so (p ∧ q) ∨ (p ∧ r) = 0."""
    dim = 2
    p, q, r = span([1, 0]), span([0, 1]), span([1, 1])
    lhs = meet(p, join(q, r), dim)
    rhs = join(meet(p, q, dim), meet(p, r, dim))
    return {"lhs_dim": len(lhs), "rhs_dim": len(rhs), "equal": same(lhs, rhs), "q_or_r_dim": len(join(q, r))}


# ---------------------------------------------------------------------------
# What is a logical notion? Permutation invariance (Tarski 1966; Sher 1991)
# ---------------------------------------------------------------------------
def invariant_relations(n: int) -> list[frozenset]:
    """The binary relations on {0..n-1} that every permutation maps to themselves: for n ≥ 2, exactly four (the
    empty relation, identity, distinctness, everything)."""
    D = range(n)
    pairs = [(a, b) for a in D for b in D]
    perms = list(itertools.permutations(D))
    out = []
    for mask in range(1 << len(pairs)):
        R = frozenset(p for i, p in enumerate(pairs) if mask >> i & 1)
        if all(frozenset((s[a], s[b]) for a, b in R) == R for s in perms):
            out.append(R)
    return out


def invariant_quantifiers(n: int) -> dict:
    """Quantifiers of type ⟨1⟩ on a domain of n things are sets of subsets (∀ = {D}, ∃ = every nonempty subset).
    Of the 2^(2^n), the permutation-invariant ones are exactly those that depend only on how many things are in
    the subset: 2^(n+1) of them."""
    D = range(n)
    subsets = [frozenset(c) for r in range(n + 1) for c in itertools.combinations(D, r)]
    perms = list(itertools.permutations(D))
    inv = 0
    for mask in range(1 << len(subsets)):
        Q = {subsets[i] for i in range(len(subsets)) if mask >> i & 1}
        if all({frozenset(s[x] for x in A) for A in Q} == Q for s in perms):
            inv += 1
    return {"n": n, "all": 1 << len(subsets), "invariant": inv, "by_cardinality": 1 << (n + 1)}
