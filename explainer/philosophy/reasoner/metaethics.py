"""Metaethics, built (Part 37).

* A small deontic logic (propositional logic plus O, ought, and P, may) on serial Kripke models (KD), with validity
  checked over every model of up to three worlds, vectorized. Prior's inferences and others, sorted by whether the
  premises are purely descriptive, whether the inference is valid, and whether its normative parts are idle:
  replaceable by a fresh atom salva validitate (the pattern of Schurz's is-ought theorem).
* Gibbard's norm-world pairs: factual worlds paired with systems of norms; the Frege-Geach modus ponens, valid as
  elimination of pairs.
* Reflective equilibrium as weighted MaxSAT: principles and judgments with weights and logical links; the
  maximum-weight consistent set, and how it moves when a weight changes.
* Street's Darwinian dilemma as an analogy: evaluative attitudes evolving under fitness, correlated with fitness, and
  with an independent moral truth or a truth tied to fitness by a third factor.
"""

from __future__ import annotations

import itertools

import numpy as np

from . import prop


# ---------------------------------------------------------------------------
# A deontic logic, KD, on small models
# ---------------------------------------------------------------------------
def At(n):
    return ("atom", n)


def Neg(f):
    return ("not", f)


def Conj(a, b):
    return ("and", a, b)


def Disj(a, b):
    return ("or", a, b)


def Cond(a, b):
    return ("imp", a, b)


def Ought(f):
    return ("O", f)


def May(f):
    return ("P", f)


TOP = ("top",)
BOT = ("bot",)


def show(f, top: bool = True) -> str:
    k = f[0]
    if k == "atom":
        return f[1]
    if k == "top":
        return r"\top"
    if k == "bot":
        return r"\bot"
    if k == "not":
        return r"\neg " + show(f[1], False)
    if k in ("O", "P"):
        inner = show(f[1], False)
        return f"{k}" + (inner if inner.startswith("(") or f[1][0] in ("atom", "not") else "(" + inner + ")")
    op = {"and": r"\wedge", "or": r"\vee", "imp": r"\to"}[k]
    body = show(f[1], False) + f" {op} " + show(f[2], False)
    return body if top else "(" + body + ")"


class _Models:
    """Every serial model with n worlds over the given atoms, as numpy arrays: val[atom] has shape (M, n); R has
    shape (M, n, n)."""

    def __init__(self, atoms, n: int = 3):
        vals = list(itertools.product([False, True], repeat=len(atoms) * n))
        rows = [r for r in itertools.product([False, True], repeat=n) if any(r)]       # serial: each world sees one
        rels = list(itertools.product(rows, repeat=n))
        V = np.array(vals, dtype=bool).reshape(len(vals), len(atoms), n)
        Rm = np.array(rels, dtype=bool)                                                  # (r, n, n)
        M = len(vals) * len(rels)
        self.n = n
        self.count = M
        self.val = {a: np.repeat(V[:, i, :], len(rels), axis=0) for i, a in enumerate(atoms)}
        self.R = np.tile(Rm, (len(vals), 1, 1))

    def ev(self, f):
        k = f[0]
        if k == "atom":
            return self.val[f[1]]
        if k == "top":
            return np.ones((self.count, self.n), dtype=bool)
        if k == "bot":
            return np.zeros((self.count, self.n), dtype=bool)
        if k == "not":
            return ~self.ev(f[1])
        if k == "and":
            return self.ev(f[1]) & self.ev(f[2])
        if k == "or":
            return self.ev(f[1]) | self.ev(f[2])
        if k == "imp":
            return ~self.ev(f[1]) | self.ev(f[2])
        if k == "O":
            g = self.ev(f[1])
            return (~self.R | g[:, None, :]).all(axis=2)
        if k == "P":
            g = self.ev(f[1])
            return (self.R & g[:, None, :]).any(axis=2)
        raise ValueError(k)


def _atoms(f, out=None):
    out = set() if out is None else out
    if f[0] == "atom":
        out.add(f[1])
    for x in f[1:]:
        if isinstance(x, tuple):
            _atoms(x, out)
    return out


def _has_O(f) -> bool:
    return f[0] in ("O", "P") or any(isinstance(x, tuple) and _has_O(x) for x in f[1:])


def _o_paths(f, path=()):
    """Paths to the outermost O or P subformulas."""
    if f[0] in ("O", "P"):
        return [path]
    out = []
    for i, x in enumerate(f[1:], start=1):
        if isinstance(x, tuple):
            out += _o_paths(x, path + (i,))
    return out


def _replace(f, path, g):
    if not path:
        return g
    i = path[0]
    return f[:i] + (_replace(f[i], path[1:], g),) + f[i + 1:]


def _valid(models, premises, concl):
    ok = np.ones((models.count, models.n), dtype=bool)
    for p in premises:
        ok &= models.ev(p)
    c = models.ev(concl)
    bad = ok & ~c
    if bad.any():
        m, w = np.argwhere(bad)[0]
        return False, int(m), int(w)
    return True, None, None


def analyse(premises, concl, n: int = 3) -> dict:
    """Check an inference on every serial model of up to ``n`` worlds. ``idle`` (None unless the inference is valid
    and its conclusion has an O or P) is True when each outermost O- or P-subformula of the conclusion, one at a time,
    can be swapped for a fresh atom with the inference still valid. That is a sufficient test for an ought that does
    no work, and stricter than Schurz's (1997), which replaces what stands inside the O: p |- p & O(q v ~q) is valid,
    no theorem and not ``idle`` here, though its ought is a logical truth and adds nothing. So "theorem or idle" is
    the pattern on the film's eight inferences (``schurz_table``), not a general statement of Schurz's theorem."""
    atoms = sorted(set().union(*[_atoms(p) for p in premises], _atoms(concl))) + ["fresh"]
    M = _Models(atoms, n)
    valid, m, w = _valid(M, premises, concl)
    theorem, _, _ = _valid(M, [], concl)
    descriptive = not any(_has_O(p) for p in premises)
    paths = _o_paths(concl)
    idle = None
    if valid and paths:
        idle = all(_valid(M, premises, _replace(concl, pth, At("fresh")))[0] for pth in paths)
    counter = None
    if not valid:
        counter = {"world": w, "facts": {a: bool(M.val[a][m, w]) for a in atoms if a != "fresh"},
                   "ideal": [int(v) for v in np.where(M.R[m, w])[0]],
                   "ideal_facts": [{a: bool(M.val[a][m, v]) for a in atoms if a != "fresh"}
                                   for v in np.where(M.R[m, w])[0]]}
    return {"premises": [show(p) for p in premises], "conclusion": show(concl), "descriptive": descriptive,
            "normative_conclusion": _has_O(concl), "valid": valid, "theorem": theorem, "idle": idle,
            "countermodel": counter, "models": M.count}


def schurz_table() -> dict:
    p, q = At("p"), At("q")
    cases = [
        ("Prior's tea: p, so p or Oq", [p], Disj(p, Ought(q))),
        ("Prior's second: p, so if not p then Oq", [p], Cond(Neg(p), Ought(q))),
        ("ought from is: p, so Op", [p], Ought(p)),
        ("ought from is: p and q, so O(p and q)", [Conj(p, q)], Ought(Conj(p, q))),
        ("a logical ought: so O(q or not q)", [], Ought(Disj(q, Neg(q)))),
        ("with a normative premise: p, if p then Oq, so Oq", [p, Cond(p, Ought(q))], Ought(q)),
        ("ought implies may: Op, so Pp", [Ought(p)], May(p)),
        ("is from ought: Op, so p", [Ought(p)], p),
    ]
    rows = []
    for name, prem, concl in cases:
        r = analyse(prem, concl)
        r["name"] = name
        rows.append(r)
    # Hume's pattern: every valid inference with descriptive premises and a normative conclusion is either a logical
    # truth or has idle normative parts
    pattern = all(r["theorem"] or r["idle"] for r in rows
                  if r["valid"] and r["descriptive"] and r["normative_conclusion"])
    return {"rows": rows, "hume_pattern_holds": pattern, "models_checked": rows[0]["models"]}


# ---------------------------------------------------------------------------
# Gibbard's norm-world pairs
# ---------------------------------------------------------------------------
def norm_world_pairs() -> dict:
    """Acts: L, telling a lie; G, getting your little brother to lie. A norm system forbids some subset of the acts;
    a factual world settles whether your brother is gullible (it matters to nothing here). A judgment is the set of
    pairs it leaves open. P1: lying is wrong. P2: if lying is wrong, getting your brother to lie is wrong. C: getting
    your brother to lie is wrong. Modus ponens is valid: every pair left by P1 and P2 is in C."""
    norms = [frozenset(s) for s in ([], ["L"], ["G"], ["L", "G"])]
    worlds = ["gullible", "not gullible"]
    pairs = [(w, n) for n in norms for w in worlds]

    def wrong(act):
        return {pr for pr in pairs if act in pr[1]}
    P1 = wrong("L")
    P2 = {pr for pr in pairs if ("L" not in pr[1]) or ("G" in pr[1])}
    C = wrong("G")
    left = P1 & P2
    fmt = lambda S: sorted([[w, sorted(n)] for w, n in S], key=lambda x: (len(x[1]), x[1], x[0]))   # noqa: E731
    return {"pairs": fmt(pairs), "P1": fmt(P1), "P2": fmt(P2), "left": fmt(left), "C": fmt(C),
            "valid": left <= C, "n_pairs": len(pairs), "n_left": len(left)}


# ---------------------------------------------------------------------------
# Reflective equilibrium as weighted MaxSAT
# ---------------------------------------------------------------------------
RE_COMMITMENTS = [
    ("U", "principle", "the right act maximizes total welfare", 3),
    ("D", "principle", "never kill an innocent, even to save more", 3),
    ("DDE", "principle", "harm as a side effect may be allowed; as a means, not", 2),
    ("S", "judgment", "switching the trolley is permissible", 4),
    ("F", "judgment", "pushing the man is forbidden", 5),
    ("H", "judgment", "the surgeon may not harvest one patient's organs for five", 5),
]
RE_LINKS = ["U -> S", "U -> ~F", "U -> ~H", "D -> ~S", "D -> F", "D -> H", "DDE -> S", "DDE -> F", "DDE -> H"]


def reflective_equilibrium(weights: dict | None = None) -> dict:
    """Keep the set of commitments of greatest total weight that is consistent with the links (the links are hard
    constraints: what each principle implies about the cases). Exhaustive over all 64 subsets, with the Reasoner's
    satisfiability checker."""
    w = {k: v for k, _, _, v in RE_COMMITMENTS}
    if weights:
        w.update(weights)
    keys = [k for k, *_ in RE_COMMITMENTS]
    links = [prop.parse(s) for s in RE_LINKS]
    best, best_w, ties = None, -1, []
    conflicts = []
    for r in range(len(keys) + 1):
        for keep in itertools.combinations(keys, r):
            fs = links + [prop.Var(k) for k in keep]
            if prop.satisfiable(fs):
                tw = sum(w[k] for k in keep)
                if tw > best_w:
                    best, best_w, ties = keep, tw, [keep]
                elif tw == best_w:
                    ties.append(keep)
    for a, b in itertools.combinations(keys, 2):
        if not prop.satisfiable(links + [prop.Var(a), prop.Var(b)]):
            conflicts.append([a, b])
    return {"weights": w, "keep": list(best), "drop": [k for k in keys if k not in best], "weight": best_w,
            "ties": [list(t) for t in ties], "conflicts": conflicts}


def re_experiments() -> dict:
    base = reflective_equilibrium()
    # after Greene: confidence in the footbridge and surgeon judgments falls, confidence in the principle of welfare
    # rises
    greene = reflective_equilibrium({"F": 1, "H": 2, "U": 6})
    return {"base": base, "greene": greene, "commitments": [list(c) for c in RE_COMMITMENTS], "links": RE_LINKS}


# ---------------------------------------------------------------------------
# Street's Darwinian dilemma: an analogy
# ---------------------------------------------------------------------------
def debunking(n_acts: int = 200, gens: int = 400, rate: float = 0.05, seed: int = 2006) -> dict:
    """Two hundred kinds of act, each with a fitness effect f. The share of a population approving of each act evolves
    by the replicator equation da = rate a (1 - a) f. Compare the evolved approval with a moral truth that is (i)
    independent of fitness, or (ii) tied to it by a third factor: t = f + noise. Labelled an analogy: it models only
    the structure of Street's argument."""
    rng = np.random.default_rng(seed)
    f = rng.normal(0, 1, n_acts)
    a = np.full(n_acts, 0.5)
    for _ in range(gens):
        a = a + rate * a * (1 - a) * f
        a = np.clip(a, 1e-6, 1 - 1e-6)
    t_indep = rng.normal(0, 1, n_acts)
    t_third = f + rng.normal(0, 0.7, n_acts)
    c = lambda x, y: float(np.corrcoef(x, y)[0, 1])     # noqa: E731
    return {"n": n_acts, "corr_fitness": round(c(a, f), 3), "corr_independent": round(c(a, t_indep), 3),
            "corr_third_factor": round(c(a, t_third), 3),
            "approval": [round(float(x), 3) for x in a], "fitness": [round(float(x), 3) for x in f],
            "t_indep": [round(float(x), 3) for x in t_indep], "t_third": [round(float(x), 3) for x in t_third]}
