"""An LCF-style trusted kernel (Part 54): propositional natural deduction in the style of Milner's LCF (1972), where
a theorem is a value of an abstract type that only the kernel's inference rules can construct.  Whatever program
produced a ``Thm`` (a tactic, a search, a careless script), the theorem is true if the few dozen lines of the kernel
are right.  That is the architecture of HOL, Isabelle and (with proof terms) Rocq and Lean.

    formulas                           Atom, Bot, Imp, And, Or as small immutable trees; Not(a) is a => bot; show()
    the kernel                         Thm (sequent  hyps |- concl) and the rules: assume, imp_intro, imp_elim,
                                       and_intro, and_elim_left/right, or_intro_left/right, or_elim, bot_elim and the
                                       classical double-negation rule dne; an illegal step raises KernelError
    Recorder                           outside the kernel: calls the rules and logs each application for the proof tree
    proofs()                           (A and B) => (B and A); ((A => B) and (B => C)) => (A => C); (A or B) => (B or
                                       A); Peirce's law ((A => B) => A) => A, which needs dne
    tautology(f) / kripke_holds(...)   independent checks: truth tables (every theorem is classically valid), and a
                                       two-world Kripke model in which Peirce's law fails (so no intuitionistic proof)
    kernel_size()                      source lines of the kernel against the rest of this module

Python cannot make a type truly abstract as ML does; the kernel guards construction with a private token and makes
theorems immutable, which stops every honest mistake, not a determined forger.

After Milner, "Logic for computable functions: description of a machine implementation" (Stanford AIM-169, 1972);
Gordon, "From LCF to HOL: a short history" (2000); Harrison, *Handbook of Practical Logic and Automated Reasoning*
(2009), ch. 6; Huth and Ryan, *Logic in Computer Science* (2004), ch. 1.
"""

from __future__ import annotations

import inspect
import itertools
import sys
from dataclasses import dataclass


# ------------------------------------------------------------------------------------------- formulas

@dataclass(frozen=True)
class Atom:
    name: str


@dataclass(frozen=True)
class Bot:
    pass


@dataclass(frozen=True)
class Imp:
    a: object
    b: object


@dataclass(frozen=True)
class And:
    a: object
    b: object


@dataclass(frozen=True)
class Or:
    a: object
    b: object


BOT = Bot()


def Not(a):
    return Imp(a, BOT)


_PREC = {Imp: 1, Or: 2, And: 3}


def show(f, need: int = 0) -> str:
    """Unicode, fewest parentheses: => is loosest and right-associative, then or, then and; not binds tightest."""
    if isinstance(f, Atom):
        return f.name
    if isinstance(f, Bot):
        return "⊥"
    if isinstance(f, Imp) and isinstance(f.b, Bot):
        return "¬" + show(f.a, 4)
    p = _PREC[type(f)]
    sym = {Imp: "⇒", Or: "∨", And: "∧"}[type(f)]
    if isinstance(f, Imp):
        s = f"{show(f.a, p + 1)} {sym} {show(f.b, p)}"
    else:
        s = f"{show(f.a, p + 1)} {sym} {show(f.b, p + 1)}"
    return f"({s})" if p < need else s


# ---- KERNEL BEGIN: everything from here to KERNEL END must be trusted; nothing else need be

class KernelError(Exception):
    """An inference rule was applied to premises it does not fit."""


_KEY = object()


class Thm:
    """A sequent hyps |- concl.  Only the rule functions below can make one."""
    __slots__ = ("_hyps", "_concl")

    def __init__(self, hyps, concl, key=None):
        if key is not _KEY:
            raise KernelError("theorems are made only by inference rules")
        object.__setattr__(self, "_hyps", frozenset(hyps))
        object.__setattr__(self, "_concl", concl)

    def __setattr__(self, name, value):
        raise KernelError("theorems are immutable")

    @property
    def hyps(self):
        return self._hyps

    @property
    def concl(self):
        return self._concl


def _formula(f):
    if not isinstance(f, (Atom, Bot, Imp, And, Or)):
        raise KernelError(f"not a formula: {f!r}")
    return f


def assume(a):
    """a |- a"""
    return Thm({_formula(a)}, a, _KEY)


def imp_intro(a, th):
    """from G |- b infer G - {a} |- a => b"""
    return Thm(th.hyps - {_formula(a)}, Imp(a, th.concl), _KEY)


def imp_elim(th1, th2):
    """from G |- a => b and D |- a infer G, D |- b"""
    if not isinstance(th1.concl, Imp) or th1.concl.a != th2.concl:
        raise KernelError("imp_elim: the second premise is not the antecedent of the first")
    return Thm(th1.hyps | th2.hyps, th1.concl.b, _KEY)


def and_intro(th1, th2):
    """from G |- a and D |- b infer G, D |- a and b"""
    return Thm(th1.hyps | th2.hyps, And(th1.concl, th2.concl), _KEY)


def and_elim_left(th):
    """from G |- a and b infer G |- a"""
    if not isinstance(th.concl, And):
        raise KernelError("and_elim_left: not a conjunction")
    return Thm(th.hyps, th.concl.a, _KEY)


def and_elim_right(th):
    """from G |- a and b infer G |- b"""
    if not isinstance(th.concl, And):
        raise KernelError("and_elim_right: not a conjunction")
    return Thm(th.hyps, th.concl.b, _KEY)


def or_intro_left(th, b):
    """from G |- a infer G |- a or b"""
    return Thm(th.hyps, Or(th.concl, _formula(b)), _KEY)


def or_intro_right(a, th):
    """from G |- b infer G |- a or b"""
    return Thm(th.hyps, Or(_formula(a), th.concl), _KEY)


def or_elim(th, th1, th2):
    """from G |- a or b, D1 |- c and D2 |- c infer G, D1 - {a}, D2 - {b} |- c"""
    if not isinstance(th.concl, Or) or th1.concl != th2.concl:
        raise KernelError("or_elim: need a disjunction and two proofs of the same conclusion")
    return Thm(th.hyps | (th1.hyps - {th.concl.a}) | (th2.hyps - {th.concl.b}), th1.concl, _KEY)


def bot_elim(th, a):
    """from G |- bot infer G |- a (ex falso)"""
    if not isinstance(th.concl, Bot):
        raise KernelError("bot_elim: premise is not bot")
    return Thm(th.hyps, _formula(a), _KEY)


def dne(th):
    """from G |- not not a infer G |- a (the classical rule)"""
    c = th.concl
    if not (isinstance(c, Imp) and isinstance(c.b, Bot) and isinstance(c.a, Imp) and isinstance(c.a.b, Bot)):
        raise KernelError("dne: premise is not a double negation")
    return Thm(th.hyps, c.a.a, _KEY)

# ---- KERNEL END


RULES = ["assume", "imp_intro", "imp_elim", "and_intro", "and_elim_left", "and_elim_right", "or_intro_left",
         "or_intro_right", "or_elim", "bot_elim", "dne"]


def sequent(th) -> str:
    hyps = ", ".join(sorted(show(h) for h in th.hyps))
    return f"{hyps} ⊢ {show(th.concl)}" if hyps else f"⊢ {show(th.concl)}"


class Recorder:
    """Applies kernel rules and logs each step as {id, rule, premises: [ids], arg, sequent}.  It is not trusted:
    a wrong log cannot make a false Thm, because every Thm still comes from the kernel."""

    def __init__(self):
        self.steps = []
        self._ids = {}
        self._keep = []                                    # keep every Thm alive, so id() stays unique

    def __getattr__(self, rule):
        if rule not in RULES:
            raise AttributeError(rule)
        fn = getattr(sys.modules[__name__], rule)

        def apply(*args):
            th = fn(*args)
            prem = [self._ids[id(a)] for a in args if isinstance(a, Thm)]
            arg = [show(a) for a in args if not isinstance(a, Thm)]
            self._ids[id(th)] = len(self.steps)
            self.steps.append({"id": len(self.steps), "rule": rule, "premises": prem,
                               "arg": arg[0] if arg else None, "sequent": sequent(th)})
            self._keep.append(th)
            return th
        return apply

    def tree(self, step_id=None) -> dict:
        """The proof as a nested tree rooted at the last step (shared subproofs are repeated, as on paper)."""
        i = len(self.steps) - 1 if step_id is None else step_id
        s = self.steps[i]
        return {"rule": s["rule"], "sequent": s["sequent"], "above": [self.tree(p) for p in s["premises"]]}


A, B, C = Atom("A"), Atom("B"), Atom("C")


def prove_and_comm(r):
    h = r.assume(And(A, B))
    return r.imp_intro(And(A, B), r.and_intro(r.and_elim_right(h), r.and_elim_left(h)))


def prove_imp_trans(r):
    H = And(Imp(A, B), Imp(B, C))
    h = r.assume(H)
    a = r.assume(A)
    b = r.imp_elim(r.and_elim_left(h), a)
    c = r.imp_elim(r.and_elim_right(h), b)
    return r.imp_intro(H, r.imp_intro(A, c))


def prove_or_comm(r):
    h = r.assume(Or(A, B))
    left = r.or_intro_right(B, r.assume(A))
    right = r.or_intro_left(r.assume(B), A)
    return r.imp_intro(Or(A, B), r.or_elim(h, left, right))


def prove_peirce(r):
    P = Imp(Imp(A, B), A)
    na = r.assume(Not(A))
    a = r.assume(A)
    a_to_b = r.imp_intro(A, r.bot_elim(r.imp_elim(na, a), B))     # not A |- A => B
    got_a = r.imp_elim(r.assume(P), a_to_b)                         # not A, P |- A
    nna = r.imp_intro(Not(A), r.imp_elim(na, got_a))                # P |- not not A
    return r.imp_intro(P, r.dne(nna))


PROOFS = {"and_comm": prove_and_comm, "imp_trans": prove_imp_trans, "or_comm": prove_or_comm,
          "peirce": prove_peirce}


def atoms(f, out=None):
    out = set() if out is None else out
    if isinstance(f, Atom):
        out.add(f.name)
    elif isinstance(f, (Imp, And, Or)):
        atoms(f.a, out)
        atoms(f.b, out)
    return out


def holds(f, val: dict) -> bool:
    if isinstance(f, Atom):
        return val[f.name]
    if isinstance(f, Bot):
        return False
    if isinstance(f, Imp):
        return (not holds(f.a, val)) or holds(f.b, val)
    if isinstance(f, And):
        return holds(f.a, val) and holds(f.b, val)
    return holds(f.a, val) or holds(f.b, val)


def tautology(f) -> bool:
    """True under every assignment (truth tables)."""
    names = sorted(atoms(f))
    return all(holds(f, dict(zip(names, bits))) for bits in itertools.product((False, True), repeat=len(names)))


def kripke_holds(f, world, order, val) -> bool:
    """Intuitionistic forcing in a finite Kripke model: ``order[w]`` is the set of worlds >= w (reflexive,
    transitive), ``val[w]`` the atoms true at w (monotone).  An implication holds at w if at every later world where
    the antecedent holds, so does the consequent."""
    if isinstance(f, Atom):
        return f.name in val[world]
    if isinstance(f, Bot):
        return False
    if isinstance(f, And):
        return kripke_holds(f.a, world, order, val) and kripke_holds(f.b, world, order, val)
    if isinstance(f, Or):
        return kripke_holds(f.a, world, order, val) or kripke_holds(f.b, world, order, val)
    return all((not kripke_holds(f.a, v, order, val)) or kripke_holds(f.b, v, order, val) for v in order[world])


# Two worlds 0 <= 1; A becomes true only at 1, B never: excluded middle and Peirce's law fail at world 0.
KRIPKE_PEIRCE = {"order": {0: {0, 1}, 1: {1}}, "val": {0: set(), 1: {"A"}}}


def proofs() -> dict:
    """Each proof's theorem, rule applications (for the tree), and the independent checks."""
    out = {}
    for name, fn in PROOFS.items():
        r = Recorder()
        th = fn(r)
        out[name] = {"theorem": sequent(th), "closed": not th.hyps, "steps": r.steps, "tree": r.tree(),
                     "rules_used": sorted({s["rule"] for s in r.steps}),
                     "classical": any(s["rule"] == "dne" for s in r.steps),
                     "tautology": tautology(th.concl),
                     "holds_in_kripke_countermodel": kripke_holds(th.concl, 0, **KRIPKE_PEIRCE)}
    return out


def illegal_steps() -> list[dict]:
    """Attempts the kernel refuses, with its message."""
    attempts = [
        ("forge a theorem directly", lambda: Thm(set(), A)),
        ("modus ponens on the wrong antecedent", lambda: imp_elim(assume(Imp(A, B)), assume(B))),
        ("and_elim on an implication", lambda: and_elim_left(assume(Imp(A, B)))),
        ("dne on a single negation", lambda: dne(assume(Not(A)))),
        ("edit a theorem's conclusion", lambda: setattr(assume(A), "_concl", B)),
    ]
    out = []
    for what, f in attempts:
        try:
            f()
            out.append({"attempt": what, "refused": False, "message": None})
        except KernelError as e:
            out.append({"attempt": what, "refused": True, "message": str(e)})
    return out


def _code_lines(lines) -> int:
    return sum(1 for ln in lines if ln.strip() and not ln.strip().startswith("#"))


def kernel_size() -> dict:
    """Non-blank, non-comment source lines inside the KERNEL BEGIN / KERNEL END markers against the rest of the
    module (docstrings count as lines, being source)."""
    src = inspect.getsource(sys.modules[__name__]).splitlines()
    begin = next(i for i, ln in enumerate(src) if ln.startswith("# ---- KERNEL BEGIN"))
    end = next(i for i, ln in enumerate(src) if ln.startswith("# ---- KERNEL END"))
    kernel = _code_lines(src[begin + 1:end])
    total = _code_lines(src)
    return {"kernel_lines": kernel, "module_lines": total, "outside_kernel_lines": total - kernel,
            "kernel_share": round(kernel / total, 3), "rules": RULES}
