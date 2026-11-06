"""Possible worlds, built (Part 22).

* Quantified modal logic as tuples, evaluated two ways: Kripke's semantics (one domain of individuals, the same
  thing in many worlds) and Lewis's counterpart theory (world-bound individuals linked by a counterpart relation).
* Lewis's 1968 translation of modal sentences into the first-order language of counterpart theory, printed, and
  checked against the direct counterpart semantics on every model of a census.
* A census of small models: which principles of modal logic (necessity of identity, the Barcan formula, T, 4, B)
  have countermodels in each semantics.
* Quine's mathematical cyclist (de re and de dicto) and Kripke's rigid designators, on small world models.
* Two-dimensional semantics: the matrix of a sentence over worlds considered as actual and worlds considered as
  counterfactual; its diagonal (the primary intension) and its actual row (the secondary intension); the four
  classes of necessary/contingent and a priori/a posteriori.
* Ersatz worlds and alien properties: describing worlds with actual vocabulary collapses distinct possibilities.
* Necessitism and contingentism: the Barcan formula on Wittgenstein's possible child.
* Fine's counterexamples to the modal account of essence: Socrates and his singleton.
* Impossible worlds: counterpossibles that are not all vacuously true, and propositions finer than sets of possible
  worlds.
* Dispositions: the simple and the reformed conditional analyses against finks and masks.
* Counterfactual explanations of a classifier: Lewis's closest worlds, in feature space.
"""

from __future__ import annotations

import itertools
from dataclasses import dataclass, field

# ---------------------------------------------------------------------------
# Formulas of quantified modal logic
#   ("P", name, (vars...)) ("=", u, v) ("not", f) ("and", f, g) ("or", f, g) ("imp", f, g)
#   ("all", v, f) ("some", v, f) ("box", f) ("dia", f)
# ---------------------------------------------------------------------------


def Atom(name, *vs):
    return ("P", name, tuple(vs))


def Eq(u, v):
    return ("=", u, v)


def Not(f):
    return ("not", f)


def And(f, g):
    return ("and", f, g)


def Or(f, g):
    return ("or", f, g)


def Imp(f, g):
    return ("imp", f, g)


def All(v, f):
    return ("all", v, f)


def Some(v, f):
    return ("some", v, f)


def Box(f):
    return ("box", f)


def Dia(f):
    return ("dia", f)


def fv(f) -> list:
    """Free variables, in order of first occurrence."""
    out: list = []

    def go(g, bound):
        op = g[0]
        if op == "P":
            for v in g[2]:
                if v not in bound and v not in out:
                    out.append(v)
        elif op == "=":
            for v in g[1:]:
                if v not in bound and v not in out:
                    out.append(v)
        elif op == "not" or op in ("box", "dia"):
            go(g[1], bound)
        elif op in ("and", "or", "imp"):
            go(g[1], bound)
            go(g[2], bound)
        elif op in ("all", "some"):
            go(g[2], bound | {g[1]})
    go(f, frozenset())
    return out


def subst(f, m: dict):
    """Rename free variables by ``m``."""
    op = f[0]
    if op == "P":
        return ("P", f[1], tuple(m.get(v, v) for v in f[2]))
    if op == "=":
        return ("=", m.get(f[1], f[1]), m.get(f[2], f[2]))
    if op in ("not", "box", "dia"):
        return (op, subst(f[1], m))
    if op in ("and", "or", "imp"):
        return (op, subst(f[1], m), subst(f[2], m))
    if op in ("all", "some"):
        m2 = {k: v for k, v in m.items() if k != f[1]}
        return (op, f[1], subst(f[2], m2))
    # first-order counterpart vocabulary
    if op in ("W", "I", "C"):
        return (op,) + tuple(m.get(v, v) for v in f[1:])
    raise ValueError(op)


def show(f) -> str:
    """TeX for a modal or counterpart-theoretic formula."""
    op = f[0]
    if op == "P":
        return rf"\mathit{{{f[1]}}}" + ("" if not f[2] else " " + " ".join(f[2]))
    if op == "=":
        return rf"{f[1]} = {f[2]}"
    if op == "not":
        if f[1][0] == "=":
            return rf"{f[1][1]} \ne {f[1][2]}"
        return r"\lnot " + show(f[1])
    if op in ("and", "or", "imp"):
        sym = {"and": r"\land", "or": r"\lor", "imp": r"\to"}[op]
        return rf"({show(f[1])} {sym} {show(f[2])})"
    if op == "all":
        return rf"\forall {f[1]}\, " + show(f[2])
    if op == "some":
        return rf"\exists {f[1]}\, " + show(f[2])
    if op == "box":
        return r"\Box " + show(f[1])
    if op == "dia":
        return r"\Diamond " + show(f[1])
    if op == "W":
        return rf"W{f[1]}"
    if op == "I":
        return rf"I{f[1]}{f[2]}"
    if op == "C":
        return rf"C{f[1]}{f[2]}"
    raise ValueError(op)


# ---------------------------------------------------------------------------
# Kripke semantics: S5, varying or constant domains, transworld individuals
# ---------------------------------------------------------------------------
@dataclass
class KModel:
    worlds: list
    dom: dict                       # world -> set of individuals existing there
    ext: dict                       # (world, predicate) -> set of tuples
    R: set | None = None            # accessibility; None = universal (S5)

    def access(self, w):
        return self.worlds if self.R is None else [v for v in self.worlds if (w, v) in self.R]


def kholds(f, M: KModel, w, g: dict) -> bool:
    """Kripke's semantics. Quantifiers range over the domain of the world of evaluation; atomic predicates are read
    off ``ext`` (false of things that do not exist there unless listed)."""
    op = f[0]
    if op == "P":
        return tuple(g[v] for v in f[2]) in M.ext.get((w, f[1]), set())
    if op == "=":
        return g[f[1]] == g[f[2]]
    if op == "not":
        return not kholds(f[1], M, w, g)
    if op == "and":
        return kholds(f[1], M, w, g) and kholds(f[2], M, w, g)
    if op == "or":
        return kholds(f[1], M, w, g) or kholds(f[2], M, w, g)
    if op == "imp":
        return (not kholds(f[1], M, w, g)) or kholds(f[2], M, w, g)
    if op == "all":
        return all(kholds(f[2], M, w, {**g, f[1]: d}) for d in M.dom[w])
    if op == "some":
        return any(kholds(f[2], M, w, {**g, f[1]: d}) for d in M.dom[w])
    if op == "box":
        return all(kholds(f[1], M, v, g) for v in M.access(w))
    if op == "dia":
        return any(kholds(f[1], M, v, g) for v in M.access(w))
    raise ValueError(op)


# ---------------------------------------------------------------------------
# Counterpart theory (Lewis 1968)
# ---------------------------------------------------------------------------
@dataclass
class CModel:
    """World-bound individuals. ``C`` holds pairs (x, y): x is a counterpart of y. Lewis's postulates are imposed:
    everything is in exactly one world (P1-P4), nothing is a counterpart of anything else in its own world (P5),
    everything is a counterpart of itself (P6)."""
    worlds: list
    dom: dict                       # world -> list of individuals
    C: set
    ext: dict                       # predicate -> set of tuples
    actual: str = "@"
    where: dict = field(default_factory=dict)

    def __post_init__(self):
        self.where = {x: w for w, xs in self.dom.items() for x in xs}
        self.C = set(self.C) | {(x, x) for x in self.where}
        for x, y in self.C:
            if x != y and self.where[x] == self.where[y]:
                raise ValueError(f"P5 violated: {x} is a counterpart of {y} in its own world")

    def counterparts(self, y, w) -> list:
        return [x for x in self.dom[w] if (x, y) in self.C]


def holds_cp(f, M: CModel, w, g: dict) -> bool:
    """Counterpart semantics, directly: `necessarily phi(x1..xn)' is true at w iff at every world w1, for every
    choice of counterparts y1..yn in w1 of x1..xn, phi(y1..yn) is true at w1."""
    op = f[0]
    if op == "P":
        return tuple(g[v] for v in f[2]) in M.ext.get(f[1], set())
    if op == "=":
        return g[f[1]] == g[f[2]]
    if op == "not":
        return not holds_cp(f[1], M, w, g)
    if op == "and":
        return holds_cp(f[1], M, w, g) and holds_cp(f[2], M, w, g)
    if op == "or":
        return holds_cp(f[1], M, w, g) or holds_cp(f[2], M, w, g)
    if op == "imp":
        return (not holds_cp(f[1], M, w, g)) or holds_cp(f[2], M, w, g)
    if op == "all":
        return all(holds_cp(f[2], M, w, {**g, f[1]: d}) for d in M.dom[w])
    if op == "some":
        return any(holds_cp(f[2], M, w, {**g, f[1]: d}) for d in M.dom[w])
    if op in ("box", "dia"):
        vs = fv(f[1])
        results = []
        for w1 in M.worlds:
            choices = [M.counterparts(g[v], w1) for v in vs]
            for pick in itertools.product(*choices):
                results.append(holds_cp(f[1], M, w1, {**g, **dict(zip(vs, pick))}))
        return all(results) if op == "box" else any(results)
    raise ValueError(op)


def translate(f, w: str = "@") -> tuple:
    """Lewis's translation of a modal formula into first-order counterpart theory (W: is a world; I: is in; C: is a
    counterpart of). Quantifiers are restricted to the world of evaluation; a box over a formula with free variables
    x1..xn becomes a universal quantification over worlds and over counterparts of each xi in them."""
    counter = itertools.count(1)

    def tr(g, w):
        op = g[0]
        if op in ("P", "="):
            return g
        if op == "not":
            return ("not", tr(g[1], w))
        if op in ("and", "or", "imp"):
            return (op, tr(g[1], w), tr(g[2], w))
        if op == "all":
            return ("all", g[1], ("imp", ("I", g[1], w), tr(g[2], w)))
        if op == "some":
            return ("some", g[1], ("and", ("I", g[1], w), tr(g[2], w)))
        if op in ("box", "dia"):
            k = next(counter)
            w1 = rf"w_{{{k}}}"
            vs = fv(g[1])
            new = {v: rf"{v}_{{{k}}}" for v in vs}
            body = tr(subst(g[1], new), w1)
            conds = []
            for v in vs:
                conds += [("I", new[v], w1), ("C", new[v], v)]
            if op == "box":
                inner = body
                if conds:
                    ante = conds[0]
                    for c in conds[1:]:
                        ante = ("and", ante, c)
                    inner = ("imp", ante, body)
                for v in reversed(vs):
                    inner = ("all", new[v], inner)
                return ("all", w1, ("imp", ("W", w1), inner))
            inner = body
            for c in reversed(conds):
                inner = ("and", c, inner)
            for v in reversed(vs):
                inner = ("some", new[v], inner)
            return ("some", w1, ("and", ("W", w1), inner))
        raise ValueError(op)
    return tr(f, w)


def fo_holds(f, M: CModel, g: dict) -> bool:
    """Evaluate a formula of first-order counterpart theory. The domain is everything: the worlds and every
    individual in them; ``@`` names the actual world."""
    universe = list(M.worlds) + list(M.where)
    g = {"@": M.actual, **g}
    op = f[0]
    if op == "P":
        return tuple(g[v] for v in f[2]) in M.ext.get(f[1], set())
    if op == "=":
        return g[f[1]] == g[f[2]]
    if op == "W":
        return g[f[1]] in M.worlds
    if op == "I":
        x, w = g[f[1]], g[f[2]]
        return M.where.get(x) == w
    if op == "C":
        return (g[f[1]], g[f[2]]) in M.C
    if op == "not":
        return not fo_holds(f[1], M, g)
    if op == "and":
        return fo_holds(f[1], M, g) and fo_holds(f[2], M, g)
    if op == "or":
        return fo_holds(f[1], M, g) or fo_holds(f[2], M, g)
    if op == "imp":
        return (not fo_holds(f[1], M, g)) or fo_holds(f[2], M, g)
    if op == "all":
        return all(fo_holds(f[2], M, {**g, f[1]: d}) for d in universe)
    if op == "some":
        return any(fo_holds(f[2], M, {**g, f[1]: d}) for d in universe)
    raise ValueError(op)


# test principles: (key, name, formula)
F = lambda v: Atom("F", v)  # noqa: E731
PRINCIPLES = [
    ("refl", r"necessity of self-identity", All("x", Box(Eq("x", "x")))),
    ("NI", r"necessity of identity", All("x", All("y", Imp(Eq("x", "y"), Box(Eq("x", "y")))))),
    ("ND", r"necessity of distinctness", All("x", All("y", Imp(Not(Eq("x", "y")), Box(Not(Eq("x", "y"))))))),
    ("T", r"T: \ what must be, is", All("x", Imp(Box(F("x")), F("x")))),
    ("4", r"4: \ what must be, must must be", All("x", Imp(Box(F("x")), Box(Box(F("x")))))),
    ("B", r"B: \ what is, must possibly be", All("x", Imp(F("x"), Box(Dia(F("x")))))),
    ("BF", r"the Barcan formula", Imp(All("x", Box(F("x"))), Box(All("x", F("x"))))),
    ("CBF", r"the converse Barcan formula", Imp(Box(All("x", F("x"))), All("x", Box(F("x"))))),
    ("NE", r"everything necessarily exists", All("x", Box(Some("y", Eq("y", "x"))))),
]


def _cp_models():
    """Every counterpart model with three worlds, one or two individuals in the first world and one in each of the
    others, any counterpart relation across worlds, and any extension of F: 512 + 16384 models."""
    worlds = ["@", "u", "v"]
    for first in (["a"], ["a", "a2"]):
        dom = {"@": first, "u": ["b"], "v": ["c"]}
        where = {x: w for w, xs in dom.items() for x in xs}
        indiv = list(where)
        pairs = [(x, y) for x in indiv for y in indiv if where[x] != where[y]]
        for cbits in range(2 ** len(pairs)):
            C = {p for i, p in enumerate(pairs) if cbits >> i & 1}
            for fbits in range(2 ** len(indiv)):
                ext = {"F": {(x,) for i, x in enumerate(indiv) if fbits >> i & 1}}
                yield CModel(worlds, dom, C, ext)


def _k_models():
    """Every S5 Kripke model on two worlds over individuals {a, b}, with any nonempty domains (varying) and any
    extension of F inside each domain: 9 x 16 = 144 models."""
    worlds = ["@", "u"]
    subsets = [s for k in (1, 2) for s in itertools.combinations(["a", "b"], k)]
    for d0, d1 in itertools.product(subsets, repeat=2):
        dom = {"@": set(d0), "u": set(d1)}
        e0s = [set(s) for k in range(len(d0) + 1) for s in itertools.combinations(d0, k)]
        e1s = [set(s) for k in range(len(d1) + 1) for s in itertools.combinations(d1, k)]
        for e0, e1 in itertools.product(e0s, e1s):
            ext = {("@", "F"): {(x,) for x in e0}, ("u", "F"): {(x,) for x in e1}}
            yield KModel(worlds, dom, ext)


def census() -> dict:
    """For each principle: countermodels in counterpart theory (over the 16 896 models of ``_cp_models``, evaluated
    at every world) and in Kripke's S5 semantics with constant and with varying domains (``_k_models``). Also checks
    that Lewis's translation, evaluated in first-order logic, agrees with the direct counterpart semantics on a sample
    of the models."""
    out = {k: {"name": n, "formula": show(f), "cp_counter": 0, "k_const_counter": 0, "k_var_counter": 0}
           for k, n, f in PRINCIPLES}
    n_cp = 0
    agree = 0
    checked = 0
    for i, M in enumerate(_cp_models()):
        n_cp += 1
        for k, _, f in PRINCIPLES:
            if not all(holds_cp(f, M, w, {}) for w in M.worlds):
                out[k]["cp_counter"] += 1
            if i % 97 == 0:
                checked += 1
                agree += fo_holds(translate(f), M, {}) == holds_cp(f, M, M.actual, {})
    n_kc = n_kv = 0
    for M in _k_models():
        const = M.dom["@"] == M.dom["u"]
        n_kv += 1
        n_kc += const
        for k, _, f in PRINCIPLES:
            ok = all(kholds(f, M, w, {}) for w in M.worlds)
            if not ok:
                out[k]["k_var_counter"] += 1
                if const:
                    out[k]["k_const_counter"] += 1
    return {"principles": out, "cp_models": n_cp, "k_const_models": n_kc, "k_var_models": n_kv,
            "translation_checks": checked, "translation_agree": agree}


def humphrey() -> dict:
    """Lewis's islands: four worlds, world-bound people, counterpart bridges. Humphrey lost; his counterpart in w1
    won, so `Humphrey might have won' is true. In w2 Humphrey has two equally good counterparts (twins), so the
    necessity of identity fails; in w3 one person is a counterpart of both Humphrey and Nixon, so the necessity of
    distinctness fails. Each principle is evaluated at the actual world, by the direct semantics and through the
    translation."""
    dom = {"@": ["h", "n"], "w1": ["h1", "n1"], "w2": ["h2", "h2'"], "w3": ["m"]}
    C = {("h1", "h"), ("n1", "n"), ("h2", "h"), ("h2'", "h"), ("m", "h"), ("m", "n")}
    ext = {"Won": {("n",), ("h1",)}, "Ran": {("h",), ("n",), ("h1",), ("n1",), ("h2",), ("h2'",), ("m",)}}
    M = CModel(["@", "w1", "w2", "w3"], dom, C, ext)
    sents = [
        ("might", r"Humphrey might have won", Dia(Atom("Won", "h")), {"h": "h"}),
        ("must", r"Humphrey had to run", Box(Atom("Ran", "h")), {"h": "h"}),
        ("NI", r"necessity of identity", PRINCIPLES[1][2], {}),
        ("ND", r"necessity of distinctness", PRINCIPLES[2][2], {}),
        ("refl", r"necessity of self-identity", PRINCIPLES[0][2], {}),
    ]
    rows = []
    for k, name, f, g in sents:
        t = translate(f)
        direct = holds_cp(f, M, "@", g)
        via = fo_holds(t, M, g)
        rows.append({"key": k, "name": name, "formula": show(f), "translation": show(t), "direct": direct,
                     "translated": via})
    return {"worlds": M.worlds, "dom": dom, "C": sorted(C), "won": sorted(x for (x,) in ext["Won"]), "rows": rows}


# ---------------------------------------------------------------------------
# De re and de dicto: Quine's mathematical cyclist; rigid designators
# ---------------------------------------------------------------------------
def cyclist() -> dict:
    """Quine (1960): mathematicians are necessarily rational and not necessarily two-legged; cyclists necessarily
    two-legged and not necessarily rational. John is both. Is John necessarily rational? On a Kripke model where the
    de dicto claims hold, the de re claims about John conflict: John is rational in every world where he is a
    mathematician, and two-legged in every world where he is a cyclist, but in some world he is neither."""
    W = ["@", "u", "v"]
    # John: actual mathematician and cyclist; u: a cyclist, not a mathematician, not rational; v: a mathematician,
    # not a cyclist, one-legged.
    ext = {}
    facts = {"@": {"Math", "Cyc", "Rat", "Two"}, "u": {"Cyc", "Two"}, "v": {"Math", "Rat"}}
    for w, ps in facts.items():
        for p in ps:
            ext[(w, p)] = {("john",)}
    M = KModel(W, {w: {"john"} for w in W}, ext)
    J = {"x": "john"}
    rows = [
        (r"$\Box\, \forall x\,(\mathit{Math}\,x \to \mathit{Rat}\,x)$", r"de dicto",
         kholds(Box(All("x", Imp(Atom("Math", "x"), Atom("Rat", "x")))), M, "@", {})),
        (r"$\Box\, \forall x\,(\mathit{Cyc}\,x \to \mathit{Two}\,x)$", r"de dicto",
         kholds(Box(All("x", Imp(Atom("Cyc", "x"), Atom("Two", "x")))), M, "@", {})),
        (r"$\Box\, \mathit{Rat}\,\mathrm{john}$", r"de re", kholds(Box(Atom("Rat", "x")), M, "@", J)),
        (r"$\Box\, \mathit{Two}\,\mathrm{john}$", r"de re", kholds(Box(Atom("Two", "x")), M, "@", J)),
        (r"$\mathit{Rat}\,\mathrm{john} \land \mathit{Two}\,\mathrm{john}$", r"actual",
         kholds(And(Atom("Rat", "x"), Atom("Two", "x")), M, "@", J)),
    ]
    return {"facts": {w: sorted(v) for w, v in facts.items()},
            "rows": [{"formula": a, "reading": b, "value": c} for a, b, c in rows]}


def rigid() -> dict:
    """Kripke's modal argument: a name rigidly designates its actual bearer in every world; a description picks
    out whoever satisfies it there. Four worlds; in two of them someone else taught Alexander."""
    W = ["@", "w1", "w2", "w3"]
    teacher = {"@": "Aristotle", "w1": "Aristotle", "w2": "Xenocrates", "w3": "Speusippus"}
    name = {w: teacher["@"] for w in W}
    desc = dict(teacher)
    s1 = all(name[w] == desc[w] for w in W)
    return {"worlds": W, "name": name, "desc": desc, "same_everywhere": s1,
            "might_not_name": any(teacher[w] != name[w] for w in W),
            "might_not_desc": any(teacher[w] != desc[w] for w in W)}


# ---------------------------------------------------------------------------
# Two-dimensional semantics
# ---------------------------------------------------------------------------
WORLDS_2D = {
    "Earth": {"watery": "H2O", "evening": "Venus", "morning": "Venus", "stick": 1.00},
    "Twin Earth": {"watery": "XYZ", "evening": "Venus", "morning": "Mars", "stick": 1.01},
    "Dusk": {"watery": "H2O", "evening": "Mars", "morning": "Venus", "stick": 1.00},
}
ACTUAL_2D = "Earth"

# terms: ("rigid", key): fixed by the world considered as actual; ("desc", key): looked up in the world considered as
# counterfactual; ("const", value)
TERMS_2D = {
    "water": ("rigid", "watery"), "the watery stuff": ("desc", "watery"), "H2O": ("const", "H2O"),
    "Hesperus": ("rigid", "evening"), "Phosphorus": ("rigid", "morning"), "the evening star": ("desc", "evening"),
    "Venus": ("const", "Venus"), "one metre": ("rigid", "stick"), "the length of S": ("desc", "stick"),
}

SENTENCES_2D = [
    ("water = H2O", "water", "H2O"),
    ("Hesperus = Phosphorus", "Hesperus", "Phosphorus"),
    ("water = the watery stuff", "water", "the watery stuff"),
    ("the length of S = one metre", "the length of S", "one metre"),
    ("the evening star = Venus", "the evening star", "Venus"),
    ("H2O = H2O", "H2O", "H2O"),
]


def _term(t, w, v):
    kind, x = TERMS_2D[t]
    if kind == "rigid":
        return WORLDS_2D[w][x]
    if kind == "desc":
        return WORLDS_2D[v][x]
    return x


def matrix_2d(a: str, b: str) -> dict:
    """The two-dimensional matrix of `a = b': rows are worlds considered as actual (which fix what the rigid terms
    pick out), columns worlds considered as counterfactual. The diagonal is the primary intension; the actual row is
    the secondary intension. Necessary iff the actual row is all true; a priori (Chalmers's core thesis) iff the
    diagonal is."""
    W = list(WORLDS_2D)
    M = [[_term(a, w, v) == _term(b, w, v) for v in W] for w in W]
    diag = [M[i][i] for i in range(len(W))]
    actual_row = M[W.index(ACTUAL_2D)]
    return {"worlds": W, "matrix": M, "diagonal": diag, "actual_row": actual_row, "necessary": all(actual_row),
            "a_priori": all(diag)}


def twod() -> dict:
    out = []
    for s, a, b in SENTENCES_2D:
        m = matrix_2d(a, b)
        cls = ("necessary" if m["necessary"] else "contingent") + " " + ("a priori" if m["a_priori"] else
                                                                          "a posteriori")
        out.append({"sentence": s, **m, "class": cls})
    return {"worlds": list(WORLDS_2D), "actual": ACTUAL_2D, "facts": WORLDS_2D, "sentences": out}


# ---------------------------------------------------------------------------
# Ersatz worlds and alien properties
# ---------------------------------------------------------------------------
def alien_properties(individuals=("a", "b"), actual=("F", "G"), alien=("X", "Y")) -> dict:
    """Genuine worlds: every distribution of the actual and the alien properties over the individuals. Ersatz
    descriptions: what can be said with actual vocabulary, which names F and G but can only say of alien properties
    that there is one with a given extension. Worlds that differ only by swapping the alien properties get the same
    description: linguistic ersatzism undercounts the possibilities (Lewis 1986, 3.2)."""
    props = list(actual) + list(alien)
    cells = [(p, x) for p in props for x in individuals]
    genuine = list(itertools.product([0, 1], repeat=len(cells)))
    descs = {}
    for g in genuine:
        val = dict(zip(cells, g))
        named = tuple(val[(p, x)] for p in actual for x in individuals)
        ext_alien = sorted(tuple(val[(p, x)] for x in individuals) for p in alien)   # multiset of alien extensions
        d = (named, tuple(ext_alien))
        descs.setdefault(d, []).append(g)
    collapsed = sum(1 for v in descs.values() if len(v) > 1)
    no_alien = len(list(itertools.product([0, 1], repeat=len(actual) * len(individuals))))
    return {"genuine": len(genuine), "ersatz": len(descs), "collapsed_descriptions": collapsed,
            "worlds_in_collapsed": sum(len(v) for v in descs.values() if len(v) > 1), "actual_only": no_alien}


# ---------------------------------------------------------------------------
# Necessitism and contingentism: the Barcan formula
# ---------------------------------------------------------------------------
def barcan() -> dict:
    """Wittgenstein might have had a child. Contingentist model: varying domains; in u there is a child, b, who does
    not exist at the actual world. Necessitist model (Williamson 2013): the same domain everywhere; b exists actually
    as a merely possible, non-concrete object, and is concrete and a child only at u. The Barcan formula
    (possibly something is F, so something is possibly F) fails on the first and holds on the second."""
    W = ["@", "u"]
    child = {("u", "Child"): {("b",)}, ("u", "Concrete"): {("w",), ("b",)}, ("@", "Concrete"): {("w",)}}
    cont = KModel(W, {"@": {"w"}, "u": {"w", "b"}}, child)
    nec = KModel(W, {"@": {"w", "b"}, "u": {"w", "b"}}, child)
    bf = Imp(Dia(Some("x", Atom("Child", "x"))), Some("x", Dia(Atom("Child", "x"))))
    nne = Box(All("x", Box(Some("y", Eq("y", "x")))))
    conc = Some("x", And(Not(Atom("Concrete", "x")), Dia(Atom("Concrete", "x"))))
    rows = []
    for name, f in ((r"Barcan: $\Diamond \exists x\, \mathit{Child}\,x \to \exists x \Diamond \mathit{Child}\,x$", bf),
                    (r"$\Box \forall x \Box \exists y\, (y = x)$", nne),
                    (r"$\exists x\,(\lnot \mathit{Concrete}\,x \land \Diamond \mathit{Concrete}\,x)$", conc)):
        rows.append({"formula": name, "contingentist": kholds(f, cont, "@", {}),
                     "necessitist": kholds(f, nec, "@", {})})
    return {"rows": rows}


# ---------------------------------------------------------------------------
# Essence (Fine 1994)
# ---------------------------------------------------------------------------
def essence() -> dict:
    """Worlds that differ in which concrete things exist; in each, the pure sets over its things exist too. A property
    is modally essential to Socrates iff he has it in every world where he exists. The modal account counts as
    essential his membership of {Socrates}, his distinctness from the Eiffel Tower and his existing-if-2+2=4; Fine:
    none of these is part of what Socrates is. Conversely {Socrates} has Socrates as a member essentially, which the
    modal account counts the same way: the asymmetry of essence is invisible to modality."""
    worlds = {"@": {"Socrates", "Eiffel"}, "w1": {"Socrates"}, "w2": {"Eiffel"}, "w3": {"Socrates", "Plato"}}
    props = [
        ("human", lambda w: True, True),
        ("a member of $\\{\\text{Socrates}\\}$", lambda w: True, False),
        ("distinct from the Eiffel Tower", lambda w: True, False),
        ("such that $2 + 2 = 4$", lambda w: True, False),
        ("a teacher of Plato", lambda w: "Plato" in worlds[w] or w == "@", False),
        ("seated", lambda w: w == "@", False),
    ]
    rows = []
    for name, has, real in props:
        modal = all(has(w) for w, xs in worlds.items() if "Socrates" in xs)
        rows.append({"property": name, "modal": modal, "real": real})
    return {"worlds": {w: sorted(v) for w, v in worlds.items()}, "rows": rows,
            "mismatch": sum(r["modal"] != r["real"] for r in rows)}


# ---------------------------------------------------------------------------
# Impossible worlds and counterpossibles
# ---------------------------------------------------------------------------
def counterpossibles() -> dict:
    """Worlds as assignments of truth to sentences. Possible worlds respect mathematics: Hobbes never squares the
    circle. Impossible worlds need not: in i1 he squares it and nothing else changes; in i2 he squares it and the
    children care; the trivial world makes everything true. Distances: every possible world is closer than every
    impossible one (Nolan's strangeness of impossibility). A counterfactual `if A, C' is true iff C holds at every
    closest A-world, and vacuously true if there are none."""
    S = ["square", "care", "2+2=4", "FLT"]
    worlds = [
        ("@", True, {"square": False, "care": False, "2+2=4": True, "FLT": True}, 0),
        ("w1", True, {"square": False, "care": True, "2+2=4": True, "FLT": True}, 1),
        ("i1", False, {"square": True, "care": False, "2+2=4": True, "FLT": True}, 10),
        ("i2", False, {"square": True, "care": True, "2+2=4": True, "FLT": True}, 11),
        ("i3", False, {"square": False, "care": False, "2+2=4": True, "FLT": False}, 12),
        ("trivial", False, {s: True for s in S}, 100),
    ]

    def cf(a, c, impossible: bool):
        pool = [w for w in worlds if (impossible or w[1]) and w[2][a]]
        if not pool:
            return None
        d = min(w[3] for w in pool)
        return all(w[2][c] for w in pool if w[3] == d)

    rows = []
    for name, c, neg in ((r"\ldots the children would have cared", "care", False),
                         (r"\ldots the children would not have cared", "care", True)):
        std = cf("square", c, False)
        imp = cf("square", c, True)
        rows.append({"consequent": name, "standard": True if std is None else (not std if neg else std),
                     "vacuous": std is None, "impossible": (not imp) if neg else imp})
    poss = [w for w in worlds if w[1]]
    same_possible = all(w[2]["2+2=4"] == w[2]["FLT"] for w in poss)
    same_all = all(w[2]["2+2=4"] == w[2]["FLT"] for w in worlds)
    return {"worlds": [{"name": n, "possible": p, "facts": f, "distance": d} for n, p, f, d in worlds],
            "rows": rows, "same_possible": same_possible, "same_all": same_all}


# ---------------------------------------------------------------------------
# Dispositions
# ---------------------------------------------------------------------------
def dispositions() -> dict:
    """Four objects, each struck in a tiny causal model. `B' is the intrinsic breakable microstructure. A fink
    removes B when the object is struck (Martin 1994); a reverse fink supplies it; a mask (packing) stops the break
    while B stays (Johnston 1992; Bird 1998). The simple conditional analysis: fragile iff it would break if struck.
    Lewis's reformed analysis (1997): fragile iff it has an intrinsic property that, if it were struck and kept that
    property, would together with the striking cause it to break."""
    cases = [
        ("plain glass", {"B": True, "fink": False, "reverse": False, "mask": False}),
        ("finked glass", {"B": True, "fink": True, "reverse": False, "mask": False}),
        ("reverse-finked steel", {"B": False, "fink": False, "reverse": True, "mask": False}),
        ("masked glass", {"B": True, "fink": False, "reverse": False, "mask": True}),
    ]

    def breaks_if_struck(s, keep_b=False):
        b = s["B"]
        if not keep_b:
            if s["fink"]:
                b = False
            if s["reverse"]:
                b = True
        return b and not s["mask"]

    rows = []
    for name, s in cases:
        truth = s["B"]
        simple = breaks_if_struck(s)
        reformed = s["B"] and breaks_if_struck(s, keep_b=True)
        rows.append({"case": name, "fragile": truth, "simple": simple, "reformed": reformed})
    return {"rows": rows}


# ---------------------------------------------------------------------------
# Counterfactual explanations: the closest world where the decision flips
# ---------------------------------------------------------------------------
def counterfactual_explanation() -> dict:
    """A toy credit model scores applicants on income (thousands), debt (thousands) and years employed; it approves
    when the score is at least 0. An applicant is refused. Search every change of the features on a grid and keep
    those that flip the decision with the least cost (an L1 distance scaled per feature): Wachter, Mittelstadt and
    Russell's (2017) counterfactual explanation, which is a Lewis closest world. Several worlds tie: there is no
    unique closest world, as Lewis said against Stalnaker."""
    def score(inc, debt, yrs):
        return 0.08 * inc - 0.1 * debt + 0.4 * yrs - 4.0

    x = (35, 10, 2)                 # income 35k, debt 10k, 2 years
    scale = {"income": 5.0, "debt": 2.5, "years": 1.0}
    best, cands = None, []
    for di in range(0, 31, 5):
        for dd in range(-10, 1, 1):
            for dy in range(0, 6):
                inc, debt, yrs = x[0] + di, x[1] + dd, x[2] + dy
                if debt < 0 or score(inc, debt, yrs) < 0:
                    continue
                cost = di / scale["income"] + (-dd) / scale["debt"] + dy / scale["years"]
                cands.append((round(cost, 6), di, dd, dy))
    cands.sort()
    best = cands[0][0]
    closest = [c for c in cands if c[0] == best]
    return {"applicant": {"income": x[0], "debt": x[1], "years": x[2]}, "score": round(score(*x), 3),
            "weights": {"income": 0.08, "debt": -0.1, "years": 0.4, "bias": -4.0}, "scale": scale, "best_cost": best,
            "closest": [{"income": di, "debt": dd, "years": dy} for _, di, dd, dy in closest],
            "flips": len(cands), "searched": 7 * 11 * 6,
            "next": [{"cost": c, "income": di, "debt": dd, "years": dy} for c, di, dd, dy in cands[len(closest):
                                                                                                 len(closest) + 3]]}


# ---------------------------------------------------------------------------
# Probabilities over possible worlds: the distribution semantics
# ---------------------------------------------------------------------------
def distribution_semantics() -> dict:
    """Sato's (1995) distribution semantics, the core of ProbLog (De Raedt, Kimmig and Toivonen 2007): independent
    probabilistic facts choose a possible world; rules then fix everything else in it; the probability of a query is
    the total probability of the worlds where it holds.

        0.1 :: burglary.   0.2 :: earthquake.   0.7 :: hears(mary).
        alarm :- burglary.   alarm :- earthquake.   calls(mary) :- alarm, hears(mary)."""
    facts = [("burglary", 0.1), ("earthquake", 0.2), ("hears", 0.7)]
    worlds = []
    for bits in itertools.product([True, False], repeat=len(facts)):
        val = {f: b for (f, _), b in zip(facts, bits)}
        p = 1.0
        for (f, q), b in zip(facts, bits):
            p *= q if b else 1 - q
        alarm = val["burglary"] or val["earthquake"]
        calls = alarm and val["hears"]
        worlds.append({"facts": val, "p": round(p, 6), "alarm": alarm, "calls": calls})
    p_alarm = sum(w["p"] for w in worlds if w["alarm"])
    p_calls = sum(w["p"] for w in worlds if w["calls"])
    p_burg_given_calls = sum(w["p"] for w in worlds if w["calls"] and w["facts"]["burglary"]) / p_calls
    return {"facts": facts, "worlds": worlds, "p_alarm": round(p_alarm, 6), "p_calls": round(p_calls, 6),
            "p_burglary_given_calls": round(p_burg_given_calls, 4)}
