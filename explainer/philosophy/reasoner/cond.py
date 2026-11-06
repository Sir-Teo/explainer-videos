"""Conditionals, made computable (Part 14).

* Counterfactual models: worlds, and for each world a ranking of the others by closeness (0 = itself). Lewis's
  truth condition (A > C holds at w iff C holds at all the closest A-worlds, or there are none); Stalnaker's is the
  same on models without ties. Five small named models give the classic failures of strengthening, transitivity,
  contraposition, conditional excluded middle and simplification of disjunctive antecedents.
* Adams's thesis and the triviality results: Lewis (1976) proved on a three-world credence, and an exhaustive search
  showing that no proposition X has P(X) = P(C | A) for every member of a class closed under conditioning, unless the
  model is trivial; imaging versus conditioning.
* McGee's counterexample to modus ponens (1985), from the 1980 polls.
"""

from __future__ import annotations

import itertools
import re
from fractions import Fraction

from . import prop


# ---------------------------------------------------------------------------
# Counterfactual models
# ---------------------------------------------------------------------------
class Model:
    """``facts``: world -> {atom: bool}; ``near``: world -> {world: distance} (the world itself at 0)."""

    def __init__(self, facts: dict, near: dict, actual: str):
        self.facts, self.near, self.actual = facts, near, actual

    def holds(self, f, w: str) -> bool:
        if isinstance(f, str):
            f = parse(f)
        tag = f[0]
        if tag == "cf":
            _, a, c = f
            A = [v for v in self.facts if self.holds(a, v)]
            if not A:
                return True
            m = min(self.near[w][v] for v in A)
            return all(self.holds(c, v) for v in A if self.near[w][v] == m)
        if tag == "var":
            return self.facts[w][f[1]]
        if tag == "not":
            return not self.holds(f[1], w)
        if tag == "and":
            return self.holds(f[1], w) and self.holds(f[2], w)
        if tag == "or":
            return self.holds(f[1], w) or self.holds(f[2], w)
        if tag == "imp":
            return (not self.holds(f[1], w)) or self.holds(f[2], w)
        if tag == "iff":
            return self.holds(f[1], w) == self.holds(f[2], w)
        if tag == "top":
            return True
        if tag == "bot":
            return False
        raise ValueError(f)

    def closest(self, a, w=None) -> list[str]:
        w = w or self.actual
        A = [v for v in self.facts if self.holds(a, v)]
        if not A:
            return []
        m = min(self.near[w][v] for v in A)
        return [v for v in A if self.near[w][v] == m]

    def stalnaker(self) -> bool:
        """No ties from the actual world: its ranking is strict, so each antecedent has one closest world."""
        d = self.near[self.actual]
        return len(set(d.values())) == len(d)


_TOK = re.compile(r"\s*(<->|->|>|~|&|\||\(|\)|top|bot|[A-Za-z_][A-Za-z0-9_']*)")
_BINOP = {">": ("cf", 0), "<->": ("iff", 1), "->": ("imp", 2), "|": ("or", 3), "&": ("and", 4)}


def parse(s: str):
    """Formulas with a counterfactual connective ``>``, binding loosest and to the right: ``(s & w) > l``,
    ``(k > i) | (k > ~i)``."""
    toks, pos = [], 0
    while pos < len(s):
        if s[pos].isspace():
            pos += 1
            continue
        m = _TOK.match(s, pos)
        if not m:
            raise ValueError(f"cannot parse {s!r} at {pos}")
        toks.append(m.group(1))
        pos = m.end()
    i = 0

    def atom():
        nonlocal i
        t = toks[i]
        i += 1
        if t == "~":
            return ("not", atom())
        if t == "(":
            e = expr(0)
            assert toks[i] == ")", s
            i += 1
            return e
        if t == "top":
            return prop.TOP
        if t == "bot":
            return prop.BOT
        return ("var", t)

    def expr(min_prec):
        nonlocal i
        left = atom()
        while i < len(toks) and toks[i] in _BINOP and _BINOP[toks[i]][1] >= min_prec:
            op, prec = _BINOP[toks[i]]
            i += 1
            right = expr(prec if op in ("cf", "imp", "iff") else prec + 1)
            left = (op, left, right)
        return left

    e = expr(0)
    assert i == len(toks), s
    return e


def _model(atoms, rows, actual, near):
    facts = {}
    for name, vals in rows.items():
        facts[name] = dict(zip(atoms, vals))
    full = {}
    for w in facts:
        d = {w: 0}
        d.update(near.get(w, {}))
        for v in facts:
            d.setdefault(v, 99)
        full[w] = d
    return Model(facts, full, actual)


def classic_models() -> dict:
    """Five small models, each a countermodel to an inference that is valid for the material conditional."""
    out = {}
    # strengthening the antecedent: the match
    m = _model(("s", "w", "l"),
               {"@": (0, 0, 0), "struck, dry, lights": (1, 0, 1), "struck, wet, no light": (1, 1, 0),
                "struck, wet, lights": (1, 1, 1)},
               "@", {"@": {"struck, dry, lights": 1, "struck, wet, no light": 2, "struck, wet, lights": 3}})
    out["strengthening"] = {"model": m, "premises": ["s > l"], "conclusion": "(s & w) > l",
                            "gloss": ("if I had struck the match, it would have lit",
                                      "if I had struck it and it had been wet, it would have lit")}
    # transitivity: Stalnaker's Hoover
    m = _model(("r", "c", "t"),
               {"@": (0, 0, 0), "Russian communist": (1, 1, 0), "American communist": (0, 1, 1),
                "Russian, no communist": (1, 0, 0)},
               "@", {"@": {"American communist": 1, "Russian communist": 2, "Russian, no communist": 3}})
    out["transitivity"] = {"model": m, "premises": ["r > c", "c > t"], "conclusion": "r > t",
                           "gloss": ("if Hoover had been born in Russia, he would have been a communist",
                                     "if he had been a communist, he would have been a traitor",
                                     "if he had been born in Russia, he would have been a traitor")}
    # contraposition: Goethe
    m = _model(("l", "d"),
               {"@": (0, 1), "lived on, now dead": (1, 1), "lived on, alive now": (1, 0)},
               "@", {"@": {"lived on, now dead": 1, "lived on, alive now": 2}})
    out["contraposition"] = {"model": m, "premises": ["l > d"], "conclusion": "~d > ~l",
                             "gloss": ("if Goethe had lived past 1832, he would still be dead now",
                                       "if Goethe were alive now, he would not have lived past 1832")}
    # conditional excluded middle: Bizet and Verdi (a tie)
    m = _model(("k", "i"),
               {"@": (0, 0), "both Italian": (1, 1), "both French": (1, 0)},
               "@", {"@": {"both Italian": 1, "both French": 1}})
    out["excluded middle"] = {"model": m, "premises": [], "conclusion": "(k > i) | (k > ~i)",
                              "gloss": ("if Bizet and Verdi had been compatriots, Bizet would have been Italian",
                                        "... or he would not have been")}
    # simplification of disjunctive antecedents: Spain
    m = _model(("x", "y"),
               {"@": (0, 0), "joined the Axis": (1, 0), "joined the Allies": (0, 1)},
               "@", {"@": {"joined the Axis": 1, "joined the Allies": 2}})
    out["disjunctive antecedents"] = {"model": m, "premises": ["(x | y) > x"], "conclusion": "y > x",
                                      "gloss": ("if Spain had joined the Axis or the Allies, it would have joined "
                                                "the Axis", "if Spain had joined the Allies, it would have joined "
                                                            "the Axis")}
    for k, v in out.items():
        M = v["model"]
        v["premises_hold"] = [M.holds(p, M.actual) for p in v["premises"]]
        v["conclusion_holds"] = M.holds(v["conclusion"], M.actual)
        v["material_valid"] = _material_valid(v["premises"], v["conclusion"])
        v["stalnaker_model"] = M.stalnaker()
    return out


def _material_valid(premises, conclusion) -> bool:
    """Read > as the material conditional and test classical validity."""
    def mat(s):
        return prop.parse(s.replace(">", "->").replace("-->", "->"))
    ok, _ = prop.entails([mat(p) for p in premises], mat(conclusion))
    return ok


def cem_stalnaker() -> dict:
    """Break the Bizet--Verdi tie (Stalnaker must choose a closest world), and CEM holds at every world."""
    m = classic_models()["excluded middle"]["model"]
    d = {w: dict(v) for w, v in m.near.items()}
    d["@"]["both French"] = 2
    s = Model(m.facts, d, "@")
    return {"stalnaker": s.stalnaker(), "cem": s.holds("(k > i) | (k > ~i)", "@"), "k > i": s.holds("k > i", "@")}


# ---------------------------------------------------------------------------
# Adams's thesis and Lewis's triviality
# ---------------------------------------------------------------------------
def lewis_proof(probs=None) -> dict:
    """Lewis (1976) on one credence over three worlds: AC, A~C, ~A~C (no ~AC world). If P(A -> C) = P(C | A) for P
    and for P conditioned on C and on ~C, then X = 'A -> C' must contain every C-world and no ~C world, so P(X) =
    P(C), which differs from P(C | A)."""
    probs = probs or {"AC": Fraction(1, 3), "A~C": Fraction(1, 3), "~A~C": Fraction(1, 3)}
    pa = probs["AC"] + probs["A~C"]
    pc = probs["AC"]
    p_c_given_a = probs["AC"] / pa
    return {"probs": {k: str(v) for k, v in probs.items()}, "P(C|A)": str(p_c_given_a), "P(C)": str(pc),
            "P(X|C)": "1", "P(X|~C)": "0", "P(X)": str(pc), "contradiction": p_c_given_a != pc}


def triviality_search(types=("AC", "A~C", "~AC", "~A~C")) -> dict:
    """Worlds of the given A/C types. The class: the uniform credence on every nonempty set of worlds (closed under
    conditioning). Search every proposition X for one with P(X) = P(C | A) for every member that gives A positive
    credence."""
    W = list(range(len(types)))
    isA = {w: types[w].startswith("A") for w in W}
    isC = {w: ("~C" not in types[w]) for w in W}
    members = [frozenset(S) for r in range(1, len(W) + 1) for S in itertools.combinations(W, r)]
    members = [S for S in members if any(isA[w] for w in S)]
    best, best_n, winners = None, -1, []
    for r in range(len(W) + 1):
        for X in itertools.combinations(W, r):
            X = frozenset(X)
            n = 0
            for S in members:
                a = [w for w in S if isA[w]]
                lhs = Fraction(len(X & S), len(S))
                rhs = Fraction(sum(isC[w] for w in a), len(a))
                n += lhs == rhs
            if n > best_n:
                best, best_n = X, n
            if n == len(members):
                winners.append(sorted(X))
    return {"types": list(types), "propositions": 2 ** len(W), "members": len(members), "winners": winners,
            "best": sorted(best), "best_fits": best_n}


def imaging(probs: dict, closest: dict, A: set, C: set) -> dict:
    """Lewis's imaging on A: each world's credence moves to its closest A-world. Compare with conditioning."""
    img = {}
    for w, p in probs.items():
        img[closest[w]] = img.get(closest[w], 0) + p
    pa = sum(p for w, p in probs.items() if w in A)
    cond = {w: (p / pa if w in A else 0) for w, p in probs.items()}
    return {"imaged": img, "conditioned": cond, "P_A(C)": sum(p for w, p in img.items() if w in C),
            "P(C|A)": sum(p for w, p in cond.items() if w in C)}


def imaging_demo() -> dict:
    probs = {"AC": 0.2, "A~C": 0.2, "~AC": 0.4, "~A~C": 0.2}
    closest = {"AC": "AC", "A~C": "A~C", "~AC": "AC", "~A~C": "A~C"}
    return imaging(probs, closest, {"AC", "A~C"}, {"AC", "~AC"})


# ---------------------------------------------------------------------------
# McGee (1985)
# ---------------------------------------------------------------------------
def mcgee(reagan=0.8, carter=0.18, anderson=0.02) -> dict:
    """1980: Reagan and Anderson are Republicans; Carter a Democrat. 'If a Republican wins, then if Reagan doesn't,
    Anderson will' is certain; 'a Republican will win' is likely; yet 'if Reagan doesn't win, Anderson will' is
    unlikely."""
    rep = reagan + anderson
    p_nested = 1.0                                     # given Republican & not Reagan, it is Anderson
    p_inner = anderson / (carter + anderson)
    return {"P(Republican)": rep, "P(if R then (if not Reagan then Anderson))": p_nested,
            "P(if not Reagan then Anderson)": p_inner}
