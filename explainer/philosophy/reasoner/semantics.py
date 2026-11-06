"""Meaning, built (Part 27).

* Gongsun Long's white horse: 'is' as identity against 'is' as inclusion, on a herd of horses.
* Frege's medians: three descriptions of the point where a triangle's medians meet, one point.
* Russell's descriptions in first-order logic (via `fol`), with both scopes of negation, in four models.
* Kripke: names are rigid, descriptions are not; the Godel/Schmidt case across a few worlds.
* Two-dimensional matrices (Stalnaker, Kaplan, Chalmers): 'water = H2O' necessary a posteriori, 'water is the
  watery stuff' contingent a priori; Kaplan's character and content for 'I am here now'.
* A Tarski-Davidson truth theory for a toy language: T-sentences derived step by step.
* A typed lambda calculus with beta reduction, and a Heim-Kratzer fragment: functional application, predicate
  modification, predicate abstraction; quantifier raising and scope ambiguity, every node's term reduced.
* Generalized quantifiers: conservativity and monotonicity checked on every pair of sets; the 512 conservative
  determiner meanings among 65 536 on a two-element universe.
* Ehrenfeucht-Fraisse games on coloured sets: 'most' is not first-order definable.
* Propositions as sets of worlds, and logical omniscience.
* Dynamic predicate logic (Groenendijk and Stokhof 1991): donkey sentences and cross-sentential anaphora, checked
  against first-order translations on random models.
* Logical forms compiled to SQL and run in sqlite, against the model checker.
"""

from __future__ import annotations

import itertools
import math
import random
import sqlite3

from . import fol


# ---------------------------------------------------------------------------
# Gongsun Long's white horse
# ---------------------------------------------------------------------------
HERD = {"h1": "white", "h2": "white", "h3": "yellow", "h4": "black", "h5": "yellow", "h6": "white"}


def white_horse() -> dict:
    """'A white horse is not a horse' (Gongsun Long, c. 300 BCE). Read 'is' as inclusion and the claim is false;
    read it as identity and it is true. Gongsun Long's own argument: ask for a horse and a yellow one will do; ask for
    a white horse and it will not, so the two terms pick out different things."""
    horse = set(HERD)
    white = {h for h, c in HERD.items() if c == "white"}
    wh = white & horse
    return {"herd": HERD, "horse": sorted(horse), "white_horse": sorted(wh),
            "inclusion": wh <= horse, "identity": wh == horse,
            "yellow_answers_horse": any(HERD[h] == "yellow" for h in horse),
            "yellow_answers_white_horse": any(HERD[h] == "yellow" for h in wh)}


# ---------------------------------------------------------------------------
# Frege's medians
# ---------------------------------------------------------------------------
def _intersect(p1, p2, q1, q2):
    (x1, y1), (x2, y2), (x3, y3), (x4, y4) = p1, p2, q1, q2
    den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / den
    return (x1 + t * (x2 - x1), y1 + t * (y2 - y1))


def medians(tri=((-2.6, -1.4), (2.8, -1.0), (0.4, 2.2))) -> dict:
    """Frege (1892): let a, b, c be the lines joining each vertex of a triangle to the midpoint of the opposite side.
    'The point of intersection of a and b' and 'the point of intersection of b and c' differ in sense and share a
    reference. Computed: all three pairwise intersections, and the centroid."""
    A, B, C = tri
    mid = lambda p, q: ((p[0] + q[0]) / 2, (p[1] + q[1]) / 2)  # noqa: E731
    lines = {"a": (A, mid(B, C)), "b": (B, mid(C, A)), "c": (C, mid(A, B))}
    pts = {k: _intersect(*lines[k[0]], *lines[k[1]]) for k in ("ab", "bc", "ca")}
    cen = ((A[0] + B[0] + C[0]) / 3, (A[1] + B[1] + C[1]) / 3)
    spread = max(math.dist(p, cen) for p in pts.values())
    return {"triangle": [list(p) for p in tri], "midpoints": {k: list(v[1]) for k, v in lines.items()},
            "points": {k: [round(v[0], 6), round(v[1], 6)] for k, v in pts.items()},
            "centroid": [round(cen[0], 6), round(cen[1], 6)], "spread": spread}


# ---------------------------------------------------------------------------
# Russell's theory of descriptions
# ---------------------------------------------------------------------------
RUSSELL = {
    "the K is B": "exists x (K(x) & forall y (K(y) -> y = x) & B(x))",
    "wide: not (the K is B)": "~ exists x (K(x) & forall y (K(y) -> y = x) & B(x))",
    "narrow: the K is not B": "exists x (K(x) & forall y (K(y) -> y = x) & ~B(x))",
}
RUSSELL_MODELS = {
    "no king": ({"a", "b"}, set(), {"a"}),
    "one bald king": ({"a", "b"}, {"a"}, {"a"}),
    "one king, not bald": ({"a", "b"}, {"a"}, {"b"}),
    "two kings": ({"a", "b"}, {"a", "b"}, {"a"}),
}


def descriptions() -> dict:
    """Russell (1905): 'the K is B' says there is exactly one K and it is B. Negation can take wide scope (it is not
    the case that the K is B) or narrow scope (the K is not-B). The Reasoner evaluates all three formulas in four
    models; in the model with no king, wide negation is true and narrow negation false."""
    rows = []
    for name, (dom, K, B) in RUSSELL_MODELS.items():
        M = fol.Structure(sorted(dom), preds={"K": {(x,) for x in K}, "B": {(x,) for x in B}})
        rows.append({"model": name, "values": {k: fol.holds(fol.parse(f), M) for k, f in RUSSELL.items()}})
    return {"formulas": RUSSELL, "rows": rows}


# ---------------------------------------------------------------------------
# Kripke: rigid names, non-rigid descriptions
# ---------------------------------------------------------------------------
KRIPKE_WORLDS = {
    "actual (Kripke's story)": "schmidt",
    "as we believe": "godel",
    "Godel became a lawyer": "neumann",
    "nobody proved it": None,
}


def rigidity() -> dict:
    """The name 'Godel' picks out the same man in every world; the description 'the man who proved the
    incompleteness of arithmetic' picks out whoever proved it there. In Kripke's story (1980), Schmidt actually
    proved it and Godel took the credit: the description then refers to Schmidt, the name to Godel."""
    rows = [{"world": w, "name": "godel", "description": prover} for w, prover in KRIPKE_WORLDS.items()]
    rigid_name = len({r["name"] for r in rows}) == 1
    rigid_desc = len({r["description"] for r in rows}) == 1
    actual = KRIPKE_WORLDS["actual (Kripke's story)"]
    # 'Godel might not have proved it': in some world the man named is not the prover there
    might_not = any(r["description"] != r["name"] for r in rows)
    # 'the prover might not have proved it', de re: the actual prover is not the prover in some world
    de_re = any(r["description"] != actual for r in rows)
    # ... de dicto: in some world, whoever proved it there did not prove it there: never
    de_dicto = any(r["description"] is not None and not (r["description"] == r["description"]) for r in rows)
    return {"rows": rows, "name_rigid": rigid_name, "description_rigid": rigid_desc,
            "godel_might_not_have": might_not, "prover_de_re": de_re, "prover_de_dicto": de_dicto,
            "actual_description_refers_to": actual}


# ---------------------------------------------------------------------------
# Two-dimensional matrices and Kaplan's indexicals
# ---------------------------------------------------------------------------
SCENARIOS = {"Earth": "H2O", "Twin Earth": "XYZ"}     # the watery stuff in each world


def two_d() -> dict:
    """Rows: the world taken as actual (fixing what 'water' refers to); columns: the world in which the sentence is
    then evaluated. The diagonal (primary intension) decides a priori truth; the actual row (secondary intension)
    decides necessity. 'Water = H2O' is necessary but a posteriori; 'water is the watery stuff' is a priori but
    contingent; 'H2O = H2O' is both."""
    ws = list(SCENARIOS)

    def matrix(f):
        return [[f(a, w) for w in ws] for a in ws]

    sentences = {
        "water = H2O": lambda a, w: SCENARIOS[a] == "H2O",
        "water is the watery stuff": lambda a, w: SCENARIOS[a] == SCENARIOS[w],
        "H2O = H2O": lambda a, w: True,
    }
    out = {}
    for s, f in sentences.items():
        m = matrix(f)
        diag = [m[i][i] for i in range(len(ws))]
        out[s] = {"matrix": m, "a_priori": all(diag), "necessary": all(m[0])}
    return {"worlds": ws, "sentences": out}


AGENTS, PLACES, TIMES, WORLDS = ("Ann", "Ben"), ("Paris", "Rome"), (1, 2), ("w1", "w2")
# where each agent is at each time in each world
LOC = {("Ann", 1, "w1"): "Paris", ("Ann", 2, "w1"): "Rome", ("Ben", 1, "w1"): "Rome", ("Ben", 2, "w1"): "Rome",
       ("Ann", 1, "w2"): "Rome", ("Ann", 2, "w2"): "Rome", ("Ben", 1, "w2"): "Paris", ("Ben", 2, "w2"): "Rome"}


def kaplan() -> dict:
    """Kaplan ('Demonstratives', 1977/1989): an indexical sentence has a character (a function from contexts to
    contents) and, in a context, a content (here a set of worlds). 'I am here now' is true in every proper context
    (one whose agent is at its place at its time in its world): a priori. But its content in a context is not true in
    every world: contingent. 'Necessarily, I am here now' is false in some proper contexts."""
    contexts = [(a, p, t, w) for a in AGENTS for p in PLACES for t in TIMES for w in WORLDS if LOC[(a, t, w)] == p]
    rows = []
    for a, p, t, w in contexts:
        content = sorted(v for v in WORLDS if LOC[(a, t, v)] == p)
        rows.append({"agent": a, "place": p, "time": t, "world": w, "content": content, "true": w in content,
                     "necessary": content == list(WORLDS)})
    return {"n_contexts": len(contexts), "rows": rows, "a_priori": all(r["true"] for r in rows),
            "contingent_in": sum(not r["necessary"] for r in rows)}


# ---------------------------------------------------------------------------
# A Tarski--Davidson truth theory
# ---------------------------------------------------------------------------
ATOMS = {"snow is white": "snow is white", "grass is green": "grass is green", "snow is green": "snow is green"}
FACTS = {"snow is white": True, "grass is green": True, "snow is green": False}


def _parse_toy(s: str):
    s = s.strip()
    if s.startswith("(") and s.endswith(")"):
        depth = 0
        for i, ch in enumerate(s):
            depth += ch == "("
            depth -= ch == ")"
            if depth == 0 and i < len(s) - 1:
                break
        else:
            return _parse_toy(s[1:-1])
    depth = 0
    for op in (" or ", " and "):
        for i in range(len(s)):
            depth += s[i] == "("
            depth -= s[i] == ")"
            if depth == 0 and s.startswith(op, i):
                return (op.strip(), _parse_toy(s[:i]), _parse_toy(s[i + len(op):]))
    if s.startswith("not "):
        return ("not", _parse_toy(s[4:]))
    assert s in ATOMS, s
    return ("atom", s)


def _show_toy(t) -> str:
    if t[0] == "atom":
        return t[1]
    if t[0] == "not":
        return "not (" + _show_toy(t[1]) + ")"
    a, b = _show_toy(t[1]), _show_toy(t[2])
    a = a if t[1][0] in ("atom", "not") else "(" + a + ")"
    b = b if t[2][0] in ("atom", "not") else "(" + b + ")"
    return f"{a} {t[0]} {b}"


def t_theory(sentence: str = "not (snow is green) and (grass is green or snow is green)") -> dict:
    """Axioms: for each atomic sentence, a clause ('snow is white' is true iff snow is white); for each connective, a
    recursive clause (A and B is true iff A is true and B is true; not A is true iff A is not true). The Reasoner
    rewrites T('...') step by step until no T remains: a T-sentence, derived. Then it evaluates both sides."""
    tree = _parse_toy(sentence)

    def rhs(t, depth):
        # the metalanguage right-hand side after `depth` rewriting steps (outermost first)
        if depth == 0:
            return "T(" + _show_toy(t) + ")"
        if t[0] == "atom":
            return ATOMS[t[1]]
        if t[0] == "not":
            return "it is not the case that " + rhs(t[1], depth - 1) if t[1][0] == "atom" or depth - 1 == 0 \
                else "it is not the case that [" + rhs(t[1], depth - 1) + "]"
        word = {"and": "and", "or": "or"}[t[0]]
        return "[" + rhs(t[1], depth - 1) + "] " + word + " [" + rhs(t[2], depth - 1) + "]"

    def height(t):
        return 1 if t[0] == "atom" else 1 + max(height(x) for x in t[1:])

    steps = [rhs(tree, d) for d in range(height(tree) + 1)]

    def val(t):
        if t[0] == "atom":
            return FACTS[t[1]]
        if t[0] == "not":
            return not val(t[1])
        return (val(t[1]) and val(t[2])) if t[0] == "and" else (val(t[1]) or val(t[2]))

    return {"sentence": _show_toy(tree), "steps": steps, "value": val(tree), "atoms": FACTS}


# ---------------------------------------------------------------------------
# A typed lambda calculus, and a Heim--Kratzer fragment
# ---------------------------------------------------------------------------
# Terms: ("v", x) variable; ("c", name) individual constant; ("lam", x, body); ("app", f, a);
# ("pred", name, (args...)) atomic predication; ("and", a, b); ("imp", a, b); ("not", a);
# ("all", x, body); ("some", x, body); ("most", x, restr, scope).
def free(t) -> set:
    k = t[0]
    if k == "v":
        return {t[1]}
    if k == "c":
        return set()
    if k == "lam" or k in ("all", "some"):
        return free(t[2]) - {t[1]}
    if k == "most":
        return (free(t[2]) | free(t[3])) - {t[1]}
    if k == "pred":
        return set().union(*[free(a) for a in t[2]]) if t[2] else set()
    return set().union(*[free(x) for x in t[1:]])


_fresh = itertools.count()


def subst(t, x: str, s):
    k = t[0]
    if k == "v":
        return s if t[1] == x else t
    if k == "c":
        return t
    if k == "pred":
        return ("pred", t[1], tuple(subst(a, x, s) for a in t[2]))
    if k in ("lam", "all", "some", "most"):
        y = t[1]
        if y == x:
            return t
        rest = t[2:]
        if y in free(s):
            z = f"{y}{next(_fresh)}"
            rest = tuple(subst(r, y, ("v", z)) for r in rest)
            y = z
        return (k, y) + tuple(subst(r, x, s) for r in rest)
    return (k,) + tuple(subst(a, x, s) for a in t[1:])


def reduce(t):
    """Beta-reduce to normal form (the fragment is simply typed, so this terminates)."""
    k = t[0]
    if k == "app":
        f, a = reduce(t[1]), reduce(t[2])
        if f[0] == "lam":
            return reduce(subst(f[2], f[1], a))
        return ("app", f, a)
    if k in ("v", "c"):
        return t
    if k == "pred":
        return ("pred", t[1], tuple(reduce(a) for a in t[2]))
    if k in ("lam", "all", "some", "most"):
        return (k, t[1]) + tuple(reduce(r) for r in t[2:])
    return (k,) + tuple(reduce(a) for a in t[1:])


def show(t, tex: bool = False) -> str:
    """Pretty-print a term; with tex=True, as LaTeX for MathTex."""
    lam, al, so, an, im, no = (r"\lambda ", r"\forall ", r"\exists ", r" \wedge ", r" \rightarrow ", r"\neg ") if tex \
        else ("λ", "∀", "∃", " ∧ ", " → ", "¬")
    k = t[0]
    if k == "v":
        return t[1]
    if k == "c":
        return (r"\mathit{" + t[1] + "}") if tex else t[1]
    if k == "pred":
        nm = (r"\textsc{" + t[1] + "}") if tex else t[1].upper()
        return nm + "(" + ", ".join(show(a, tex) for a in t[2]) + ")"
    if k == "lam":
        return lam + t[1] + ".\\," + show(t[2], tex) if tex else lam + t[1] + ". " + show(t[2], tex)
    if k == "app":
        f = show(t[1], tex)
        if t[1][0] == "lam":
            f = r"\big(" + f + r"\big)" if tex else "(" + f + ")"
        return f + "(" + show(t[2], tex) + ")"
    if k in ("all", "some"):
        q = al if k == "all" else so
        return q + t[1] + (r"\,[" if tex else "[") + show(t[2], tex) + "]"
    if k == "most":
        return (r"\textsc{most}\," if tex else "MOST ") + t[1] + "[" + show(t[2], tex) + "][" + show(t[3], tex) + "]"
    if k == "not":
        return no + show(t[1], tex)
    op = an if k == "and" else im
    return "(" + show(t[1], tex) + op + show(t[2], tex) + ")"


class Model:
    def __init__(self, domain, consts, preds):
        self.domain = list(domain)
        self.consts = dict(consts)
        self.preds = {k: set(v) for k, v in preds.items()}


def evaluate(t, M: Model, g=None):
    """Evaluate a closed (or assigned) term of type e or t in M. Lambda terms of type <e,t> evaluate to the set of
    individuals they are true of; of type <e,<e,t>>, to a set of pairs."""
    g = g or {}
    k = t[0]
    if k == "v":
        return g[t[1]]
    if k == "c":
        return M.consts[t[1]]
    if k == "pred":
        args = tuple(evaluate(a, M, g) for a in t[2])
        return (args[0] if len(args) == 1 else args) in M.preds[t[1]]
    if k == "not":
        return not evaluate(t[1], M, g)
    if k == "and":
        return evaluate(t[1], M, g) and evaluate(t[2], M, g)
    if k == "imp":
        return (not evaluate(t[1], M, g)) or evaluate(t[2], M, g)
    if k == "all":
        return all(evaluate(t[2], M, {**g, t[1]: d}) for d in M.domain)
    if k == "some":
        return any(evaluate(t[2], M, {**g, t[1]: d}) for d in M.domain)
    if k == "most":
        r = [d for d in M.domain if evaluate(t[2], M, {**g, t[1]: d})]
        both = [d for d in r if evaluate(t[3], M, {**g, t[1]: d})]
        return 2 * len(both) > len(r)
    if k == "lam":
        body = t[2]
        if body[0] == "lam":                                   # a relation
            return {(a, b) for a in M.domain for b in M.domain
                    if evaluate(reduce(("app", ("app", t, ("c", "_a")), ("c", "_b"))), _with(M, a, b), g)}
        return {d for d in M.domain if evaluate(body, M, {**g, t[1]: d})}
    raise ValueError(f"cannot evaluate {show(t)}")


def _with(M, a, b):
    m = Model(M.domain, {**M.consts, "_a": a, "_b": b}, M.preds)
    return m


E, T = "e", "t"
ET = (E, T)
EET = (E, ET)
ETT = (ET, T)
ET_ETT = (ET, ETT)

v = lambda x: ("v", x)  # noqa: E731


def lex():
    """A small lexicon: word -> (type, term)."""
    def pred1(n):
        return (ET, ("lam", "z", ("pred", n, (v("z"),))))

    def pred2(n):                         # transitive verb: object first, as in Heim and Kratzer
        return (EET, ("lam", "y", ("lam", "x", ("pred", n, (v("x"), v("y"))))))

    def det(body):                        # body(P x, Q x) -> a quantified formula over x
        Px, Qx = ("app", v("P"), v("x")), ("app", v("Q"), v("x"))
        return (ET_ETT, ("lam", "P", ("lam", "Q", body(Px, Qx))))

    L = {"Ann": (E, ("c", "ann")), "Bob": (E, ("c", "bob")), "Cy": (E, ("c", "cy")),
         "smokes": pred1("smoke"), "student": pred1("student"), "book": pred1("book"), "linguist": pred1("linguist"),
         "Swiss": pred1("swiss"), "likes": pred2("like"), "read": pred2("read"),
         "every": det(lambda Px, Qx: ("all", "x", ("imp", Px, Qx))),
         "a": det(lambda Px, Qx: ("some", "x", ("and", Px, Qx))),
         "some": det(lambda Px, Qx: ("some", "x", ("and", Px, Qx))),
         "no": det(lambda Px, Qx: ("not", ("some", "x", ("and", Px, Qx)))),
         "most": det(lambda Px, Qx: ("most", "x", Px, Qx)),
         "not": ((T, T), ("lam", "p", ("not", v("p"))))}
    return L


def show_type(ty) -> str:
    if isinstance(ty, str):
        return ty
    return "<" + show_type(ty[0]) + "," + show_type(ty[1]) + ">"


def interpret(tree, M: Model):
    """Heim and Kratzer's composition rules on a binary tree. A tree is a word (a leaf), a trace 't1', 't2', ...,
    a pair (left, right), or ('lambda', n, subtree) for predicate abstraction after quantifier raising. Returns the
    nodes bottom-up: label, rule, type, reduced term (plain and TeX), and value in M."""
    L = lex()
    nodes = []

    def go(t, path):
        if isinstance(t, str):
            if t.startswith("t") and t[1:].isdigit():
                ty, term, rule, lab = E, v("x" + t[1:]), "trace", t
            else:
                ty, term = L[t]
                rule, lab = "lexicon", t
        elif t[0] == "lambda":
            n, sub = t[1], t[2]
            ty_s, term_s, _ = go(sub, path + "1")
            assert ty_s == T
            ty, term, rule, lab = ET, reduce(("lam", "x" + str(n), term_s)), "PA", f"λ{n}"
        else:
            (ta, ma, la), (tb, mb, lb) = go(t[0], path + "L"), go(t[1], path + "R")
            if isinstance(ta, tuple) and ta[0] == tb:
                ty, term, rule = ta[1], reduce(("app", ma, mb)), "FA"
            elif isinstance(tb, tuple) and tb[0] == ta:
                ty, term, rule = tb[1], reduce(("app", mb, ma)), "FA"
            elif ta == ET and tb == ET:
                ty, term, rule = ET, reduce(("lam", "z", ("and", ("app", ma, v("z")), ("app", mb, v("z"))))), "PM"
            else:
                raise TypeError(f"type mismatch {show_type(ta)} {show_type(tb)}")
            lab = la + " " + lb
        val = None
        if ty in (T, E, ET) and not (free(term) - set()):
            val = evaluate(term, M)
            if isinstance(val, set):
                val = sorted(val)
        nodes.append({"path": path, "label": lab, "rule": rule, "type": show_type(ty), "term": show(term),
                      "tex": show(term, tex=True), "value": val})
        return ty, term, lab

    ty, term, _ = go(tree, "")
    return {"type": show_type(ty), "term": show(term), "tex": show(term, tex=True),
            "value": evaluate(term, M) if ty == T else None, "nodes": nodes}


SCOPE_MODEL = Model(["ann", "bob", "cy", "b1", "b2", "b3"], {"ann": "ann", "bob": "bob", "cy": "cy"},
                    {"student": {"ann", "bob", "cy"}, "book": {"b1", "b2", "b3"}, "smoke": {"ann", "bob"},
                     "linguist": {"ann", "cy"}, "swiss": {"ann", "bob"},
                     "like": {("ann", "bob"), ("ann", "cy"), ("bob", "bob")},
                     "read": {("ann", "b1"), ("bob", "b2"), ("cy", "b3")}})

TREES = {
    "Ann smokes": ("Ann", "smokes"),
    "every student smokes": (("every", "student"), "smokes"),
    "most students smoke": (("most", "student"), "smokes"),
    "a Swiss linguist smokes": (("a", ("Swiss", "linguist")), "smokes"),
    "Ann likes every student (QR)": (("every", "student"), ("lambda", 1, ("Ann", ("likes", "t1")))),
    "every student read a book (surface)": (("every", "student"),
                                            ("lambda", 1, (("a", "book"), ("lambda", 2, ("t1", ("read", "t2")))))),
    "every student read a book (inverse)": (("a", "book"),
                                            ("lambda", 2, (("every", "student"), ("lambda", 1, ("t1", ("read", "t2")))))),
}


def fragment() -> dict:
    """Every tree in TREES interpreted in SCOPE_MODEL, where each student read a different book: the surface scope
    of 'every student read a book' is true, the inverse scope false."""
    return {k: interpret(t, SCOPE_MODEL) for k, t in TREES.items()}


# ---------------------------------------------------------------------------
# Generalized quantifiers
# ---------------------------------------------------------------------------
GQ = {
    "every": lambda A, B: A <= B,
    "some": lambda A, B: bool(A & B),
    "no": lambda A, B: not (A & B),
    "most": lambda A, B: len(A & B) > len(A - B),
    "exactly two": lambda A, B: len(A & B) == 2,
    "at least half": lambda A, B: 2 * len(A & B) >= len(A),
    "only": lambda A, B: B <= A,
}


def _subsets(U):
    U = sorted(U)
    return [frozenset(c) for r in range(len(U) + 1) for c in itertools.combinations(U, r)]


def quantifiers(n: int = 4) -> dict:
    """On every pair of subsets of a universe of n elements, check conservativity (Q(A, B) iff Q(A, A & B)) and the
    four monotonicity properties. 'Only' is the classic failure of conservativity: it is not a determiner."""
    S = _subsets(range(n))
    rows = {}
    for name, Q in GQ.items():
        cons = all(Q(A, B) == Q(A, A & B) for A in S for B in S)
        up_r = all(not Q(A, B) or Q(A, B2) for A in S for B in S for B2 in S if B <= B2)
        dn_r = all(not Q(A, B) or Q(A, B2) for A in S for B in S for B2 in S if B2 <= B)
        up_l = all(not Q(A, B) or Q(A2, B) for A in S for A2 in S for B in S if A <= A2)
        dn_l = all(not Q(A, B) or Q(A2, B) for A in S for A2 in S for B in S if A2 <= A)
        rows[name] = {"conservative": cons, "left_up": up_l, "left_down": dn_l, "right_up": up_r,
                      "right_down": dn_r}
    return {"n": n, "pairs": len(S) ** 2, "rows": rows}


def count_conservative(n: int = 2) -> dict:
    """All relations between subsets of an n-element universe (2^(4^n) of them) and how many are conservative
    (2^(3^n): Keenan and Stavi 1986). For n = 2: 65 536 and 512, by brute force."""
    S = _subsets(range(n))
    pairs = [(A, B) for A in S for B in S]
    idx = {p: i for i, p in enumerate(pairs)}
    # conservativity identifies (A, B) with (A, A & B): count the classes
    cls = {}
    for A, B in pairs:
        cls.setdefault((A, A & B), []).append(idx[(A, B)])
    total = 2 ** len(pairs)
    cons = 0
    for mask in range(total):
        if all(len({(mask >> i) & 1 for i in group}) == 1 for group in cls.values()):
            cons += 1
    return {"n": n, "pairs": len(pairs), "all": total, "conservative": cons, "formula": 2 ** (3 ** n)}


# ---------------------------------------------------------------------------
# Ehrenfeucht--Fraisse games: 'most' is not first-order
# ---------------------------------------------------------------------------
def ef_duplicator_wins(m1, m2, k: int, state=None) -> bool:
    """The k-round EF game on two structures with one unary predicate P (m = (number of P, number of non-P)).
    Spoiler picks an element of either structure; Duplicator answers in the other; Duplicator wins if the pebbled
    elements always form a partial isomorphism. Elements of one colour are interchangeable, so a position is
    exactly the number of distinct pebbled elements of each colour, in both structures alike."""
    state = state or (0, 0)
    if k == 0:
        return True
    for colour in (0, 1):
        for side in (0, 1):
            here, there = (m1, m2) if side == 0 else (m2, m1)
            # Spoiler picks a new element of this colour on `side` (re-picking a pebbled one changes nothing)
            if state[colour] < here[colour]:
                if state[colour] >= there[colour]:
                    return False                     # Duplicator has no new element of that colour to answer with
                nxt = list(state)
                nxt[colour] += 1
                if not ef_duplicator_wins(m1, m2, k - 1, tuple(nxt)):
                    return False
    return True


def ef_most(k_max: int = 4) -> dict:
    """For each k: M1 has k + 1 P's and k non-P's ('most things are P' true); M2 has k P's and k + 1 non-P's
    (false). Duplicator wins the k-round game, so no first-order sentence of quantifier rank k tells them apart;
    Spoiler wins with k + 1 rounds. As k is arbitrary, no first-order sentence expresses 'most'."""
    rows = []
    for k in range(1, k_max + 1):
        m1, m2 = (k + 1, k), (k, k + 1)
        rows.append({"k": k, "M1": list(m1), "M2": list(m2), "most_M1": m1[0] > m1[1], "most_M2": m2[0] > m2[1],
                     "duplicator_k": ef_duplicator_wins(m1, m2, k),
                     "duplicator_k_plus_1": ef_duplicator_wins(m1, m2, k + 1)})
    return {"rows": rows}


# ---------------------------------------------------------------------------
# Propositions as sets of worlds: logical omniscience
# ---------------------------------------------------------------------------
def omniscience(depth: int = 2) -> dict:
    """Take worlds to be the four valuations of p, q. Every formula built from p, q with not, and, or, -> up to
    the given depth denotes one of 16 sets of worlds; every tautology denotes the set of all worlds. An agent whose
    beliefs are a set of worlds believes every tautology, and every consequence of what she believes."""
    worlds = list(itertools.product((False, True), repeat=2))
    level = {("p",): frozenset(w for w in worlds if w[0]), ("q",): frozenset(w for w in worlds if w[1])}
    forms = dict(level)
    for _ in range(depth):
        new = {}
        items = list(forms.items())
        for f, s in items:
            new[("not", f)] = frozenset(worlds) - s
        for (f, s), (g, t) in itertools.product(items, repeat=2):
            new[("and", f, g)] = s & t
            new[("or", f, g)] = s | t
            new[("imp", f, g)] = (frozenset(worlds) - s) | t
        forms.update(new)
    props = set(forms.values())
    taut = [f for f, s in forms.items() if len(s) == len(worlds)]
    return {"worlds": len(worlds), "formulas": len(forms), "propositions": len(props), "tautologies": len(taut)}


# ---------------------------------------------------------------------------
# Dynamic predicate logic
# ---------------------------------------------------------------------------
# Formulas: ("P", name, (vars)), ("ex", x, f), ("and", f, g), ("not", f), ("imp", f, g), ("all", x, f)
def dpl(f, M, g: dict) -> list:
    """Groenendijk and Stokhof: the meaning of a formula is a relation between assignments. Returns the outputs
    for input g. Existentials reset a variable and pass it on; conjunction composes; negation, implication and the
    universal are tests."""
    k = f[0]
    if k == "P":
        return [g] if tuple(g[x] for x in f[2]) in M[f[1]] else []
    if k == "ex":
        return [h for d in M["_dom"] for h in dpl(f[2], M, {**g, f[1]: d})]
    if k == "and":
        return [h2 for h in dpl(f[1], M, g) for h2 in dpl(f[2], M, h)]
    if k == "not":
        return [] if dpl(f[1], M, g) else [g]
    if k == "imp":
        return [g] if all(dpl(f[2], M, h) for h in dpl(f[1], M, g)) else []
    if k == "all":
        return [g] if all(dpl(f[2], M, {**g, f[1]: d}) for d in M["_dom"]) else []
    raise ValueError(k)


def _fo(f, M, g) -> bool:
    k = f[0]
    if k == "P":
        return tuple(g[x] for x in f[2]) in M[f[1]]
    if k == "ex":
        return any(_fo(f[2], M, {**g, f[1]: d}) for d in M["_dom"])
    if k == "all":
        return all(_fo(f[2], M, {**g, f[1]: d}) for d in M["_dom"])
    if k == "and":
        return _fo(f[1], M, g) and _fo(f[2], M, g)
    if k == "not":
        return not _fo(f[1], M, g)
    if k == "imp":
        return (not _fo(f[1], M, g)) or _fo(f[2], M, g)
    raise ValueError(k)


P_ = lambda n, *xs: ("P", n, xs)  # noqa: E731
DONKEY_DPL = ("all", "x", ("imp", ("and", P_("farmer", "x"), ("ex", "y", ("and", P_("donkey", "y"),
                                                                            P_("owns", "x", "y")))),
                           P_("beats", "x", "y")))
DONKEY_FO = ("all", "x", ("all", "y", ("imp", ("and", P_("farmer", "x"), ("and", P_("donkey", "y"),
                                                                             P_("owns", "x", "y"))),
                                       P_("beats", "x", "y"))))
DISCOURSE_DPL = ("and", ("ex", "x", ("and", P_("farmer", "x"), ("ex", "y", ("and", P_("donkey", "y"),
                                                                              P_("owns", "x", "y"))))),
                 P_("beats", "x", "y"))
DISCOURSE_FO = ("ex", "x", ("ex", "y", ("and", P_("farmer", "x"), ("and", P_("donkey", "y"),
                                                                      ("and", P_("owns", "x", "y"),
                                                                       P_("beats", "x", "y"))))))


def _random_model(rng, n):
    dom = list(range(n))
    M = {"_dom": dom}
    for p in ("farmer", "donkey"):
        M[p] = {(d,) for d in dom if rng.random() < 0.5}
    for r in ("owns", "beats"):
        M[r] = {(a, b) for a in dom for b in dom if rng.random() < 0.35}
    return M


def donkeys(trials: int = 400, seed: int = 1991) -> dict:
    """On random models: the DPL donkey sentence agrees with the first-order 'for all x, y' translation every
    time; the static translation, with y left free (here: y assigned the first individual), disagrees often. The
    DPL discourse 'A farmer owns a donkey. He beats it.' agrees with 'exists x, y (... and beats x y)'."""
    rng = random.Random(seed)
    agree = naive = disc = 0
    for _ in range(trials):
        M = _random_model(rng, rng.randint(2, 4))
        g0 = {"x": 0, "y": 0}
        d = bool(dpl(DONKEY_DPL, M, g0))
        agree += d == _fo(DONKEY_FO, M, g0)
        naive += d == _fo(DONKEY_DPL, M, g0)
        disc += bool(dpl(DISCOURSE_DPL, M, g0)) == _fo(DISCOURSE_FO, M, g0)
    return {"trials": trials, "dpl_vs_fo": agree, "dpl_vs_naive": naive, "discourse": disc}


# ---------------------------------------------------------------------------
# Logical forms to SQL
# ---------------------------------------------------------------------------
def _sql_db(M: Model):
    con = sqlite3.connect(":memory:")
    con.execute("create table ent(id text)")
    con.executemany("insert into ent values (?)", [(d,) for d in M.domain])
    for p, ext in M.preds.items():
        sample = next(iter(ext), None)
        if isinstance(sample, tuple):
            con.execute(f"create table {p}(a text, b text)")
            con.executemany(f"insert into {p} values (?, ?)", list(ext))
        else:
            con.execute(f"create table {p}(a text)")
            con.executemany(f"insert into {p} values (?)", [(x,) for x in ext])
    return con


def to_sql(t, env=None) -> str:
    """Compile a reduced first-order term to a SQL boolean expression over tables ent, and one table per
    predicate. Quantifiers become EXISTS / NOT EXISTS subqueries over ent."""
    env = env or {}
    k = t[0]
    if k == "pred":
        args = [env[a[1]] if a[0] == "v" else repr(a[1]) for a in t[2]]
        cols = ["a", "b"][:len(args)]
        cond = " and ".join(f"{c} = {x}" for c, x in zip(cols, args))
        return f"exists (select 1 from {t[1]} where {cond})"
    if k == "not":
        return f"not ({to_sql(t[1], env)})"
    if k == "and":
        return f"({to_sql(t[1], env)} and {to_sql(t[2], env)})"
    if k == "imp":
        return f"(not ({to_sql(t[1], env)}) or {to_sql(t[2], env)})"
    if k in ("some", "all"):
        alias = f"e{len(env)}"
        inner = to_sql(t[2], {**env, t[1]: f"{alias}.id"})
        if k == "some":
            return f"exists (select 1 from ent {alias} where {inner})"
        return f"not exists (select 1 from ent {alias} where not ({inner}))"
    if k == "most":
        alias = f"e{len(env)}"
        e2 = {**env, t[1]: f"{alias}.id"}
        r, s = to_sql(t[2], e2), to_sql(t[3], e2)
        return (f"(select 2 * count(*) from ent {alias} where {r} and {s}) > "
                f"(select count(*) from ent {alias} where {r})")
    raise ValueError(k)


def sql_check() -> dict:
    """Every sentence of the fragment compiled to SQL, run in sqlite on the model's tables, and compared with the
    model checker."""
    M = SCOPE_MODEL
    con = _sql_db(M)
    rows = []
    for name, tree in TREES.items():
        r = interpret(tree, M)
        term = reduce(_term_of(tree))
        q = "select " + to_sql(_consts_to_names(term)) + ";"
        got = bool(con.execute(q).fetchone()[0])
        rows.append({"sentence": name, "model": r["value"], "sql": got, "query": q})
    con.close()
    return {"rows": rows, "all_agree": all(r["model"] == r["sql"] for r in rows)}


def _term_of(tree):
    L = lex()

    def go(t):
        if isinstance(t, str):
            if t.startswith("t") and t[1:].isdigit():
                return E, v("x" + t[1:])
            return L[t]
        if t[0] == "lambda":
            ty, m = go(t[2])
            return ET, ("lam", "x" + str(t[1]), m)
        (ta, ma), (tb, mb) = go(t[0]), go(t[1])
        if isinstance(ta, tuple) and ta[0] == tb:
            return ta[1], reduce(("app", ma, mb))
        if isinstance(tb, tuple) and tb[0] == ta:
            return tb[1], reduce(("app", mb, ma))
        return ET, reduce(("lam", "z", ("and", ("app", ma, v("z")), ("app", mb, v("z")))))

    return go(tree)[1]


def _consts_to_names(t):
    k = t[0]
    if k == "c":
        return ("name", t[1])
    if k == "pred":
        return ("pred", t[1], tuple(("lit", a[1]) if a[0] == "c" else a for a in t[2]))
    if k in ("v",):
        return t
    if k in ("all", "some", "most"):
        return (k, t[1]) + tuple(_consts_to_names(x) for x in t[2:])
    return (k,) + tuple(_consts_to_names(x) for x in t[1:])


# ---------------------------------------------------------------------------
# Beta reduction, one step at a time
# ---------------------------------------------------------------------------
def step(t):
    """One leftmost-outermost beta step, or None if t is normal."""
    k = t[0]
    if k == "app":
        if t[1][0] == "lam":
            return subst(t[1][2], t[1][1], t[2])
        s = step(t[1])
        if s is not None:
            return ("app", s, t[2])
        s = step(t[2])
        return None if s is None else ("app", t[1], s)
    if k in ("v", "c"):
        return None
    if k == "pred":
        for i, a in enumerate(t[2]):
            s = step(a)
            if s is not None:
                return ("pred", t[1], t[2][:i] + (s,) + t[2][i + 1:])
        return None
    start = 2 if k in ("lam", "all", "some", "most") else 1
    for i in range(start, len(t)):
        s = step(t[i])
        if s is not None:
            return t[:i] + (s,) + t[i + 1:]
    return None


def beta_steps(t, limit: int = 20) -> list:
    out = [t]
    while len(out) <= limit:
        s = step(out[-1])
        if s is None:
            break
        out.append(s)
    return out


def beta_demo() -> dict:
    """[[every]]([[student]])([[smokes]]) reduced step by step, then evaluated in the scope model."""
    L = lex()
    t = ("app", ("app", L["every"][1], L["student"][1]), L["smokes"][1])
    steps = beta_steps(t)
    return {"steps": [show(s) for s in steps], "tex": [show(s, tex=True) for s in steps],
            "value": evaluate(steps[-1], SCOPE_MODEL)}


# ---------------------------------------------------------------------------
# Strawson, Donnellan, Twin Earth
# ---------------------------------------------------------------------------
def strawson() -> dict:
    """Strawson (1950): if there is no unique K, 'the K is B' is neither true nor false (its presupposition fails),
    and so is its negation. Russell's values against Strawson's, in the four models of `descriptions`."""
    rows = []
    for name, (dom, K, B) in RUSSELL_MODELS.items():
        r = descriptions()["rows"]
        russell = next(x["values"] for x in r if x["model"] == name)
        if len(K) == 1:
            s = next(iter(K)) in B
            straw = {"the K is B": s, "the K is not B": not s}
        else:
            straw = {"the K is B": None, "the K is not B": None}
        rows.append({"model": name, "russell": {"the K is B": russell["the K is B"],
                                                "the K is not B": russell["narrow: the K is not B"]},
                     "strawson": straw})
    return {"rows": rows}


PARTY = {"drinks": {"jones": "water in a martini glass", "smith": "martini", "brown": "beer"},
         "philosopher": {"jones"}, "speaker_means": "jones"}


def donnellan() -> dict:
    """Donnellan (1966): 'the man drinking a martini is a philosopher'. Used attributively, it is about whoever
    uniquely drinks a martini (Smith, unnoticed in the corner) and is false; used referentially, the speaker means
    Jones, whose glass holds water, and says something true of him. Kripke (1977): semantic against speaker's
    reference."""
    martini = [p for p, d in PARTY["drinks"].items() if d == "martini"]
    semantic = martini[0] if len(martini) == 1 else None
    speaker = PARTY["speaker_means"]
    return {"semantic_referent": semantic, "speaker_referent": speaker,
            "attributive_true": semantic in PARTY["philosopher"], "referential_true": speaker in PARTY["philosopher"],
            "drinks": PARTY["drinks"]}


def twin() -> dict:
    """Putnam (1975): Oscar and Twin Oscar are molecule-for-molecule alike, with the same thoughts 'in the head'
    about the clear, drinkable stuff in the lakes. The extension of 'water' is fixed by the environment: H2O on Earth,
    XYZ on Twin Earth. Same internal state, different extension: meanings ain't in the head."""
    inner = "clear, drinkable, fills the lakes"
    rows = [{"speaker": s, "inner": inner, "world": w, "extension": SCENARIOS[w]}
            for s, w in (("Oscar", "Earth"), ("Twin Oscar", "Twin Earth"))]
    return {"rows": rows, "same_inner": len({r["inner"] for r in rows}) == 1,
            "same_extension": len({r["extension"] for r in rows}) == 1}


# ---------------------------------------------------------------------------
# Foster's problem for truth theories
# ---------------------------------------------------------------------------
def _sentences(depth: int = 2):
    atoms = [("atom", a) for a in ATOMS]
    out = list(atoms)
    for _ in range(depth):
        new = [("not", s) for s in out]
        new += [(op, a, b) for op in ("and", "or") for a in out[:6] for b in out[:6]]
        out = out + new
    seen, uniq = set(), []
    for s in out:
        k = repr(s)
        if k not in seen:
            seen.add(k)
            uniq.append(s)
    return uniq


def foster(depth: int = 2) -> dict:
    """Foster (1976): a truth theory whose clause for 'snow is white' reads '... is true iff grass is green' issues
    T-sentences that are all true, since in the actual world both sides agree; yet it does not say what the sentence
    means. Computed: the two theories agree on every sentence (to the given depth) in the actual world, and disagree
    on many in a world where grass is not green."""
    sents = _sentences(depth)

    def val(t, facts, swap):
        if t[0] == "atom":
            a = t[1]
            if swap and a == "snow is white":
                a = "grass is green"
            return facts[a]
        if t[0] == "not":
            return not val(t[1], facts, swap)
        x, y = val(t[1], facts, swap), val(t[2], facts, swap)
        return (x and y) if t[0] == "and" else (x or y)

    other = {**FACTS, "grass is green": False}
    agree_actual = sum(val(s, FACTS, False) == val(s, FACTS, True) for s in sents)
    agree_other = sum(val(s, other, False) == val(s, other, True) for s in sents)
    return {"n": len(sents), "agree_actual": agree_actual, "agree_other": agree_other}


# ---------------------------------------------------------------------------
# An inference suite whose gold labels are computed
# ---------------------------------------------------------------------------
NLI_EDITS = {
    "narrow the noun": ("A", "down"),        # dogs -> small dogs
    "widen the noun": ("A", "up"),           # small dogs -> dogs
    "narrow the verb": ("B", "down"),        # make noise -> bark
    "widen the verb": ("B", "up"),           # bark -> make noise
}


def nli_suite(n: int = 4) -> dict:
    """For each determiner and each edit (narrow or widen the noun or the verb), is the edited sentence entailed?
    Gold labels by brute force: entailment iff it holds for every choice of sets on an n-element universe. These
    are exactly the monotonicity profiles; benchmarks such as FraCaS (1996) and MED (Yanaka et al. 2019) test them."""
    S = _subsets(range(n))
    rows = {}
    for q in ("every", "some", "no", "most"):
        Q = GQ[q]
        r = {}
        for edit, (arg, direction) in NLI_EDITS.items():
            ok = True
            for X in S:
                for Y in S:
                    if direction == "down" and not Y <= X:
                        continue
                    if direction == "up" and not X <= Y:
                        continue
                    for Z in S:
                        prem = Q(X, Z) if arg == "A" else Q(Z, X)
                        hyp = Q(Y, Z) if arg == "A" else Q(Z, Y)
                        if prem and not hyp:
                            ok = False
                            break
                    if not ok:
                        break
                if not ok:
                    break
            r[edit] = ok
        rows[q] = r
    return {"n": n, "rows": rows}


# ---------------------------------------------------------------------------
# Incomplete descriptions and domain restriction
# ---------------------------------------------------------------------------
def incomplete() -> dict:
    """'The table is covered with books', said in a room with one table, in a world with three. Russell's analysis
    over the whole domain is false (no unique table); restricted to the contextually relevant domain, true."""
    f = fol.parse("exists x (T(x) & forall y (T(y) -> y = x) & C(x))")
    world = fol.Structure(["t1", "t2", "t3", "b"], preds={"T": {("t1",), ("t2",), ("t3",)}, "C": {("t1",)}})
    room = fol.Structure(["t1", "b"], preds={"T": {("t1",)}, "C": {("t1",)}})
    return {"tables_in_world": 3, "unrestricted": fol.holds(f, world), "restricted": fol.holds(f, room)}


def burge() -> dict:
    """Burge (1979): a patient, with the same body, history and inner states in both communities, says 'I have
    arthritis in my thigh'. In ours, 'arthritis' means inflammation of the joints, so the belief is false; in a
    community whose experts apply the word to ailments of the thigh too, the same words express a true belief."""
    uses = {"ours": {"joints"}, "counterfactual": {"joints", "thigh"}}
    rows = [{"community": c, "applies_to": sorted(u), "belief_true": "thigh" in u} for c, u in uses.items()]
    return {"rows": rows, "same_patient": True}
