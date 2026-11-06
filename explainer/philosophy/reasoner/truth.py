"""Truth and paradox, exactly: a small language that contains its own truth predicate, Kripke's fixed points,
revision sequences, Yablo's staircase and the surprise exam.

    from explainer.philosophy.reasoner.truth import WORLD, kripke_stages, fixed_points, revision
    kripke_stages(WORLD)          # the extension and anti-extension of T, stage by stage, to the least fixed point
    fixed_points(WORLD)           # every fixed point of the strong Kleene jump
    revision(WORLD, start)        # a revision sequence from a classical hypothesis

A *world* is a dict name -> sentence. Sentences are tuples: ("fact", bool) for a sentence about the non-semantic
world, ("T", name) for "name is true", ("not", A), ("and", A, B), ("or", A, B), ("all", [names]) for "every one of
these is true", ("some", [names]). Values are "t", "f", "n" (neither), as in Part 5's K3.
"""

from __future__ import annotations

import itertools

T, F, N = "t", "f", "n"


def k3_not(a):
    return {T: F, F: T, N: N}[a]


def k3_and(a, b):
    if a == F or b == F:
        return F
    if a == T and b == T:
        return T
    return N


def k3_or(a, b):
    return k3_not(k3_and(k3_not(a), k3_not(b)))


def value(s, interp: dict):
    """The strong Kleene value of a sentence, given a (partial) interpretation of T: name -> t/f/n."""
    op = s[0]
    if op == "fact":
        return T if s[1] else F
    if op == "T":
        return interp.get(s[1], N)
    if op == "not":
        return k3_not(value(s[1], interp))
    if op == "and":
        return k3_and(value(s[1], interp), value(s[2], interp))
    if op == "or":
        return k3_or(value(s[1], interp), value(s[2], interp))
    if op == "all":
        v = T
        for n in s[1]:
            v = k3_and(v, interp.get(n, N))
        return v
    if op == "some":
        v = F
        for n in s[1]:
            v = k3_or(v, interp.get(n, N))
        return v
    if op == "imp":
        return k3_or(k3_not(value(s[1], interp)), value(s[2], interp))
    if op == "nt":                                         # exclusion: 'A is not true' (true when A is f or n)
        return F if value(s[1], interp) == T else T
    raise ValueError(s)


def jump(world: dict, interp: dict) -> dict:
    """Kripke's jump: T applies to the sentences true under the current interpretation, its negation to those false."""
    return {name: value(s, interp) for name, s in world.items()}


def kripke_stages(world: dict) -> list:
    """Iterate the jump from the empty interpretation (every sentence 'n') to the least fixed point."""
    cur = {name: N for name in world}
    out = [cur]
    while True:
        nxt = jump(world, cur)
        if nxt == cur:
            return out
        out.append(nxt)
        cur = nxt


def least_fixed_point(world: dict) -> dict:
    return kripke_stages(world)[-1]


def is_fixed(world: dict, interp: dict) -> bool:
    return jump(world, interp) == interp


def fixed_points(world: dict) -> list:
    """Every fixed point of the jump. Each extends the least one, so only the sentences left 'n' there vary."""
    lfp = least_fixed_point(world)
    free = [n for n, v in lfp.items() if v == N]
    out = []
    for vals in itertools.product((T, F, N), repeat=len(free)):
        interp = dict(lfp)
        interp.update(zip(free, vals))
        if is_fixed(world, interp):
            out.append(interp)
    return out


def classify(world: dict) -> dict:
    """Kripke's classification. grounded: classical in the least fixed point. paradoxical: 'n' in every fixed point.
    otherwise ungrounded but not paradoxical (it can be given a value consistently, as the truth-teller can)."""
    fps = fixed_points(world)
    lfp = least_fixed_point(world)
    out = {}
    for n in world:
        if lfp[n] != N:
            out[n] = "grounded"
        elif all(fp[n] == N for fp in fps):
            out[n] = "paradoxical"
        else:
            out[n] = "ungrounded"
    return out


def intrinsic(world: dict) -> dict:
    """The largest intrinsic fixed point: a sentence gets a value only if no fixed point gives it the opposite one.
    (Computed as the largest fixed point compatible with every fixed point.)"""
    fps = fixed_points(world)
    best = None
    for fp in fps:
        if all(all(fp[n] == N or other[n] in (N, fp[n]) for n in world) for other in fps):
            if best is None or sum(v != N for v in fp.values()) > sum(v != N for v in best.values()):
                best = fp
    return best


def classical_value(s, hyp: dict) -> bool:
    """Classical evaluation under a total hypothesis about T."""
    return value(s, {n: (T if b else F) for n, b in hyp.items()}) == T


def revision(world: dict, start: dict, steps: int = 8) -> list:
    """A revision sequence (Gupta and Belnap): each hypothesis h is revised to {s : s is true under h}."""
    out = [dict(start)]
    for _ in range(steps):
        h = out[-1]
        out.append({n: classical_value(s, h) for n, s in world.items()})
    return out


def revision_verdicts(world: dict, steps: int = 12) -> dict:
    """Over every starting hypothesis: 'stably true' if true from some point on in every sequence, 'stably false'
    likewise, else 'unstable' (it keeps changing in some sequence) or 'depends' (stable, but on the start)."""
    names = list(world)
    finals = {n: set() for n in names}
    unstable = set()
    for bits in itertools.product((False, True), repeat=len(names)):
        seq = revision(world, dict(zip(names, bits)), steps)
        tail = seq[steps // 2:]
        for n in names:
            vals = {h[n] for h in tail}
            if len(vals) > 1:
                unstable.add(n)
            else:
                finals[n] |= vals
    out = {}
    for n in names:
        if n in unstable:
            out[n] = "unstable"
        elif finals[n] == {True}:
            out[n] = "stably true"
        elif finals[n] == {False}:
            out[n] = "stably false"
        else:
            out[n] = "depends"
    return out


# The toy world of the part: names are short labels, glosses are what the sentences say.
WORLD = {
    "s1": ("fact", True),                                  # snow is white
    "s2": ("fact", False),                                 # grass is red
    "s3": ("T", "s1"),                                     # 's1' is true
    "s4": ("not", ("T", "s2")),                            # 's2' is not true
    "s5": ("and", ("T", "s3"), ("T", "s4")),               # 's3' and 's4' are both true
    "L": ("not", ("T", "L")),                              # this sentence is not true: the liar
    "H": ("T", "H"),                                       # this sentence is true: the truth-teller
    "s8": ("or", ("T", "L"), ("not", ("T", "L"))),         # the liar is true or not true
    "s9": ("or", ("T", "s1"), ("T", "L")),                 # s1 or the liar is true
    "s10": ("or", ("T", "s2"), ("T", "L")),                # s2 or the liar is true
    "A": ("T", "B"),                                       # 'B' is true
    "B": ("not", ("T", "A")),                              # 'A' is not true: a liar cycle
    "s13": ("not", ("T", "H")),                            # the truth-teller is not true
}
GLOSS = {
    "s1": "snow is white", "s2": "grass is red", "s3": "‘s1’ is true", "s4": "‘s2’ is not true",
    "s5": "‘s3’ and ‘s4’ are true", "L": "‘L’ is not true", "H": "‘H’ is true",
    "s8": "‘L’ is true or not true", "s9": "‘s1’ or ‘L’ is true", "s10": "‘s2’ or ‘L’ is true",
    "A": "‘B’ is true", "B": "‘A’ is not true", "s13": "‘H’ is not true",
}


def refs(world: dict) -> dict:
    """Which names each sentence mentions."""
    def walk(s):
        if s[0] == "T":
            return {s[1]}
        if s[0] in ("all", "some"):
            return set(s[1])
        if s[0] == "fact":
            return set()
        return set().union(*[walk(x) for x in s[1:]])
    return {n: sorted(walk(s)) for n, s in world.items()}


# ---------------------------------------------------------------------------
# Yablo's paradox, truncated
# ---------------------------------------------------------------------------
def yablo_world(n: int) -> dict:
    w = {}
    for k in range(1, n + 1):
        later = [f"Y{j}" for j in range(k + 1, n + 1)]
        s = ("fact", True)
        for j in later:
            s = ("and", s, ("not", ("T", j)))
        w[f"Y{k}"] = s
    return w


def yablo_solutions(n: int) -> list:
    """Every classical assignment satisfying the T-schema for the truncated sequence (a consistent world)."""
    w = yablo_world(n)
    names = list(w)
    sols = []
    for bits in itertools.product((False, True), repeat=n):
        h = dict(zip(names, bits))
        if all(classical_value(w[m], h) == h[m] for m in names):
            sols.append(h)
    return sols


# ---------------------------------------------------------------------------
# The surprise exam: backward elimination
# ---------------------------------------------------------------------------
def surprise_exam(days: int = 5) -> list:
    """The students' argument: the exam cannot be on the last remaining day, since it would not be a surprise;
    so strike it and repeat. Returns the days struck, in order."""
    left = list(range(1, days + 1))
    struck = []
    while left:
        struck.append(left.pop())
    return struck


# ---------------------------------------------------------------------------
# Revenge: an exclusion negation breaks the fixed-point construction
# ---------------------------------------------------------------------------
REVENGE = {"R": ("nt", ("T", "R"))}                        # 'this sentence is not true (it is false or neither)'


def iterate(world: dict, steps: int = 6) -> list:
    """The jump iterated from the empty interpretation, whether or not it settles."""
    cur = {name: N for name in world}
    out = [cur]
    for _ in range(steps):
        cur = jump(world, cur)
        out.append(cur)
    return out


def all_fixed_points(world: dict) -> list:
    """Brute force over every interpretation (small worlds only), for jumps that need not be monotone."""
    names = list(world)
    out = []
    for vals in itertools.product((T, F, N), repeat=len(names)):
        interp = dict(zip(names, vals))
        if is_fixed(world, interp):
            out.append(interp)
    return out


# ---------------------------------------------------------------------------
# Grelling and Nelson: autological and heterological adjectives
# ---------------------------------------------------------------------------
def _syllables(w: str) -> int:
    groups, prev = 0, False
    for ch in w.lower():
        v = ch in "aeiouy"
        if v and not prev:
            groups += 1
        prev = v
    if w.lower().endswith("e") and groups > 1:
        groups -= 1
    return max(groups, 1)


ADJECTIVES = {
    "short": lambda w: len(w) <= 5,
    "long": lambda w: len(w) >= 12,
    "polysyllabic": lambda w: _syllables(w) >= 2,
    "monosyllabic": lambda w: _syllables(w) == 1,
    "English": lambda w: True,
    "German": lambda w: False,
    "unhyphenated": lambda w: "-" not in w,
    "hyphenated": lambda w: "-" in w,
}


def grelling() -> dict:
    """For each adjective, whether it applies to itself (autological) or not (heterological); and for
    'heterological' itself, which assignments are consistent: none."""
    table = {a: ("autological" if f(a) else "heterological") for a, f in ADJECTIVES.items()}
    consistent = [v for v in (True, False) if v == (not v)]          # 'heterological' is heterological iff not
    return {"table": table, "heterological_consistent": consistent}


# ---------------------------------------------------------------------------
# Moore's paradox in doxastic logic
# ---------------------------------------------------------------------------
def moore() -> dict:
    """'p, but I don't believe p' is satisfiable; believing it is not, on serial transitive frames (KD4)."""
    from . import modal
    ok = lambda R, n: modal.serial(R, n) and modal.transitive(R, n)
    said = modal.find_model([modal.parse("p & ~[]p")], 3, ok)
    believed = modal.find_model([modal.parse("[](p & ~[]p)")], 3, ok)
    return {"said_satisfiable": said is not None, "believed_satisfiable": believed is not None}


# ---------------------------------------------------------------------------
# Priest's inclosure schema (for display)
# ---------------------------------------------------------------------------
INCLOSURE = [
    (r"Russell", r"the sets", r"$\{x \in X : x \notin x\}$"),
    (r"Burali-Forti", r"the ordinals", r"the least ordinal above all of them"),
    (r"the liar", r"the true sentences", r"`this sentence is not true'"),
    (r"Berry", r"the definable numbers", r"the least number not definable in few words"),
    (r"Grelling", r"the autological adjectives", r"`heterological'"),
]


# ---------------------------------------------------------------------------
# Tarski's definition: truth from satisfaction, for a small first-order language
# ---------------------------------------------------------------------------
TARSKI_DOMAIN = ["snow", "grass", "coal"]
TARSKI_PREDICATES = {"White": {"snow"}, "Green": {"grass"}, "Black": {"coal"}}


def satisfies(f, g: dict) -> bool:
    """Tarski's clauses: an assignment g of objects to variables satisfies a formula. f is ("P", var) for a
    predicate, ("not", A), ("and", A, B), ("or", A, B), ("all", var, A), ("some", var, A)."""
    op = f[0]
    if op in TARSKI_PREDICATES:
        return g[f[1]] in TARSKI_PREDICATES[op]
    if op == "not":
        return not satisfies(f[1], g)
    if op == "and":
        return satisfies(f[1], g) and satisfies(f[2], g)
    if op == "or":
        return satisfies(f[1], g) or satisfies(f[2], g)
    if op == "all":
        return all(satisfies(f[2], {**g, f[1]: o}) for o in TARSKI_DOMAIN)
    if op == "some":
        return any(satisfies(f[2], {**g, f[1]: o}) for o in TARSKI_DOMAIN)
    raise ValueError(f)


def tarski_true(f) -> bool:
    """A sentence is true iff every assignment satisfies it (for a sentence, one does iff all do)."""
    return satisfies(f, {v: TARSKI_DOMAIN[0] for v in "xyz"})


def tarski_sentences(depth: int = 2) -> list:
    """Every sentence of the little language up to a given depth, in one variable x plus y (for checking)."""
    atoms = [(p, v) for p in TARSKI_PREDICATES for v in "x"]
    forms = list(atoms)
    for _ in range(depth):
        new = []
        for a in forms:
            new.append(("not", a))
            new.append(("some", "x", a))
            new.append(("all", "x", a))
        for a in atoms:
            for b in atoms:
                new.append(("and", a, b))
                new.append(("or", a, b))
        forms = list(dict.fromkeys(forms + new))
    def free(f):
        if f[0] in TARSKI_PREDICATES:
            return {f[1]}
        if f[0] in ("all", "some"):
            return free(f[2]) - {f[1]}
        return set().union(*[free(x) for x in f[1:]])
    return [f for f in forms if not free(f)]


def tarski_show(f) -> str:
    op = f[0]
    if op in TARSKI_PREDICATES:
        return f"{op}({f[1]})"
    if op == "not":
        return f"¬{tarski_show(f[1])}"
    if op in ("and", "or"):
        return f"({tarski_show(f[1])} {'∧' if op == 'and' else '∨'} {tarski_show(f[2])})"
    return f"{'∀' if op == 'all' else '∃'}{f[1]} {tarski_show(f[2])}"


# ---------------------------------------------------------------------------
# Strict-tolerant consequence (Cobreros, Égré, Ripley, van Rooij)
# ---------------------------------------------------------------------------
def st_valid(premises, conclusion, world: dict) -> bool:
    """ST: whenever every premise is strictly true (t), the conclusion is tolerantly true (t or n), in every
    fixed point of the world's jump (premises and conclusion are sentences, as in WORLD)."""
    for fp in all_fixed_points(world) if len(world) <= 4 else fixed_points(world):
        if all(value(p, fp) == T for p in premises) and value(conclusion, fp) == F:
            return False
    return True


LIAR_WORLD = {"L": ("not", ("T", "L"))}


def st_demo() -> dict:
    """In ST the liar argument's two halves are valid, but chaining them (cut) is not: ST is nontransitive."""
    L = ("T", "L")
    q = ("fact", False)
    return {"proves_L": st_valid([], L, LIAR_WORLD), "L_entails_q": st_valid([L], q, LIAR_WORLD),
            "proves_q": st_valid([], q, LIAR_WORLD),
            "excluded_middle": st_valid([], ("or", L, ("not", L)), LIAR_WORLD)}


# ---------------------------------------------------------------------------
# The T-schema in K3 and in LP
# ---------------------------------------------------------------------------
def t_schema_values(world: dict) -> dict:
    """The value of each T-biconditional T('s') <-> s in the least fixed point: 'n' in K3 is not designated,
    while the same middle value read as 'both' in LP is."""
    lfp = least_fixed_point(world)
    out = {}
    for n, s in world.items():
        a, b = lfp[n], value(s, lfp)
        out[n] = k3_and(k3_or(k3_not(a), b), k3_or(k3_not(b), a))
    return out


# ---------------------------------------------------------------------------
# The surprise exam as a public announcement (Gerbrandy)
# ---------------------------------------------------------------------------
def surprise_holds(day: int, worlds: set) -> bool:
    """On the morning of the exam day, with no exam so far, the students do not know it is today."""
    left = {w for w in worlds if w >= day}
    return len(left) > 1


def exam_announcements(days: int = 5) -> list:
    """Repeatedly announce 'the exam will be a surprise', keeping the worlds where it is true: the sequence of
    remaining worlds. A single truthful announcement leaves days 1..n-1."""
    worlds = set(range(1, days + 1))
    out = [sorted(worlds)]
    while worlds:
        nxt = {w for w in worlds if surprise_holds(w, worlds)}
        if nxt == worlds:
            break
        worlds = nxt
        out.append(sorted(worlds))
    return out


# ---------------------------------------------------------------------------
# The liar as a program: ungrounded = non-terminating
# ---------------------------------------------------------------------------
def run_definitions(limit: int = 200) -> dict:
    """Evaluate each sentence of WORLD as a recursive Python function; ungrounded ones never return."""
    import sys
    world = WORLD
    out = {}

    def ev(s, depth):
        if depth > limit:
            raise RecursionError
        op = s[0]
        if op == "fact":
            return s[1]
        if op == "T":
            return ev(world[s[1]], depth + 1)
        if op == "not":
            return not ev(s[1], depth + 1)
        if op == "and":
            return ev(s[1], depth + 1) and ev(s[2], depth + 1)
        if op == "or":
            return ev(s[1], depth + 1) or ev(s[2], depth + 1)
        raise ValueError(s)
    old = sys.getrecursionlimit()
    sys.setrecursionlimit(max(old, 10 * limit + 100))
    try:
        for n, s in world.items():
            try:
                out[n] = "true" if ev(s, 0) else "false"
            except RecursionError:
                out[n] = "never returns"
    finally:
        sys.setrecursionlimit(old)
    return out


# ---------------------------------------------------------------------------
# Axiomatic theories of truth (from the literature, for display)
# ---------------------------------------------------------------------------
THEORIES = [
    ("TB", r"the T-biconditionals for sentences without $T$", r"conservative over PA", r"Tarski"),
    ("CT", r"Tarski's compositional clauses, \ with induction", r"proves $\mathrm{Con}(\mathrm{PA})$: \ not "
                                                              r"conservative", r"Tarski; Kotlarski"),
    ("KF", r"Kripke's fixed points as axioms", r"as strong as ramified analysis below $\varepsilon_0$",
     r"Feferman 1991"),
    ("FS", r"revision-style: \ $T$ commutes with every connective", r"$\omega$-inconsistent, \ yet consistent",
     r"Friedman \& Sheard 1987"),
]
