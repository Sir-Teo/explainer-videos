"""Arithmetic, coding and computation, exactly: the machinery behind Gödel's and Turing's theorems.

    from explainer.philosophy.reasoner.arith import q_steps, numeral, beta_code, godel_number, run_tm, parse_tm
    q_steps(("+", numeral(2), numeral(2)))      # 2 + 2 = 4, axiom by axiom, in Robinson's Q
    beta_code([2, 3, 5])                         # (c, d) with beta(c, d, i) = the i-th term
    godel_number("0 = 0")                        # 2^21 * 3^15 * 5^21
    run_tm(parse_tm("1RB1LB_1LA1RZ"))            # the two-state busy beaver: 6 steps, 4 ones

Terms of arithmetic are tuples: ("0",), ("S", t), ("+", a, b), ("*", a, b). Primitive recursive functions are
built from the five combinators of Gödel and Kleene and evaluated directly. Turing machines use the standard
busy-beaver notation (one block per state, ``_`` between states, ``Z`` for halt). Everything is small, or fast
enough, to check exactly; ``tests/philosophy/test_arith.py`` compares it with the published values.
"""

from __future__ import annotations

import io
import itertools
import math
import re
from contextlib import redirect_stdout
from dataclasses import dataclass

# ---------------------------------------------------------------------------
# Robinson's Q: terms and evaluation, axiom by axiom
# ---------------------------------------------------------------------------
ZERO = ("0",)


def S(t):
    return ("S", t)


def numeral(n: int):
    t = ZERO
    for _ in range(n):
        t = S(t)
    return t


def value(t) -> int:
    op = t[0]
    if op == "0":
        return 0
    if op == "S":
        return value(t[1]) + 1
    if op == "+":
        return value(t[1]) + value(t[2])
    if op == "*":
        return value(t[1]) * value(t[2])
    raise ValueError(t)


def term_str(t, tex: bool = False) -> str:
    """S S 0 + S 0 style, with brackets only where needed."""
    op = t[0]
    if op == "0":
        return "0"
    if op == "S":
        inner = t[1]
        s = term_str(inner, tex)
        if inner[0] in ("+", "*"):
            s = "(" + s + ")"
        return (r"\mathsf{S}" if tex else "S") + s
    a, b = term_str(t[1], tex), term_str(t[2], tex)
    if op == "*" and t[1][0] == "+":
        a = "(" + a + ")"
    if t[2][0] in ("+", "*") and not (op == "+" and t[2][0] == "*"):
        b = "(" + b + ")"
    sym = {"+": "+", "*": r" \times " if tex else "×"}[op]
    return f"{a} {sym} {b}" if op == "+" else f"{a}{sym}{b}"


Q_AXIOMS = {
    "Q1": (r"\mathsf{S}x \neq 0", "0 is no successor"),
    "Q2": (r"\mathsf{S}x = \mathsf{S}y \to x = y", "successor is one to one"),
    "Q3": (r"x \neq 0 \to \exists y\,(x = \mathsf{S}y)", "everything else is a successor"),
    "Q4": (r"x + 0 = x", ""),
    "Q5": (r"x + \mathsf{S}y = \mathsf{S}(x + y)", ""),
    "Q6": (r"x \times 0 = 0", ""),
    "Q7": (r"x \times \mathsf{S}y = (x \times y) + x", ""),
}


def _step(t):
    """One leftmost-innermost rewrite by Q4–Q7, or None if t is a numeral."""
    op = t[0]
    if op == "0":
        return None
    if op == "S":
        r = _step(t[1])
        return None if r is None else (S(r[0]), r[1])
    for i in (1, 2):
        r = _step(t[i])
        if r is not None:
            new = list(t)
            new[i] = r[0]
            return tuple(new), r[1]
    a, b = t[1], t[2]
    if op == "+":
        return (a, "Q4") if b == ZERO else (S(("+", a, b[1])), "Q5")
    return (ZERO, "Q6") if b == ZERO else (("+", ("*", a, b[1]), a), "Q7")


def q_steps(t) -> list:
    """The chain t = t1 = ... = numeral, each step justified by one axiom of Q."""
    out = [(t, None)]
    while True:
        r = _step(out[-1][0])
        if r is None:
            return out
        out.append(r)


# ---------------------------------------------------------------------------
# Primitive recursive functions
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class PR:
    kind: str           # Z, S, P, C, R
    arity: int
    args: tuple = ()

    def __call__(self, *xs):
        assert len(xs) == self.arity, (self, xs)
        k = self.kind
        if k == "Z":
            return 0
        if k == "S":
            return xs[0] + 1
        if k == "P":
            return xs[self.args[0]]
        if k == "C":
            f, gs = self.args[0], self.args[1:]
            return f(*[g(*xs) for g in gs])
        f, g = self.args
        *ps, y = xs
        acc = f(*ps)
        for i in range(y):
            acc = g(*ps, i, acc)
        return acc

    def size(self) -> int:
        return 1 + sum(a.size() for a in self.args if isinstance(a, PR))


def Zf(n=1):
    return PR("Z", n)


Sf = PR("S", 1)


def Pf(i, n):
    return PR("P", n, (i,))


def Cf(f, *gs):
    return PR("C", gs[0].arity, (f,) + gs)


def Rf(f, g):
    return PR("R", f.arity + 1, (f, g))


PR_ADD = Rf(Pf(0, 1), Cf(Sf, Pf(2, 3)))                                    # x + 0 = x;  x + Sy = S(x + y)
PR_MUL = Rf(Zf(1), Cf(PR_ADD, Pf(2, 3), Pf(0, 3)))                          # x * 0 = 0;  x * Sy = x*y + x
PR_EXP = Rf(Cf(Sf, Zf(1)), Cf(PR_MUL, Pf(2, 3), Pf(0, 3)))                  # x ^ 0 = 1;  x ^ Sy = x^y * x
PR_PRED = Cf(Rf(Zf(1), Pf(1, 3)), Pf(0, 1), Pf(0, 1))                       # pred(0) = 0; pred(Sy) = y
PR_FACT = Cf(Rf(Cf(Sf, Zf(1)), Cf(PR_MUL, Pf(2, 3), Cf(Sf, Pf(1, 3)))), Pf(0, 1), Pf(0, 1))
PR_LIBRARY = {"add": PR_ADD, "mul": PR_MUL, "exp": PR_EXP, "pred": PR_PRED, "fact": PR_FACT}


def ackermann_small(m: int, n: int) -> int:
    """Péter's two-argument Ackermann function by its defining equations (small arguments only)."""
    stack, n_ = [m], n
    while stack:
        m_ = stack.pop()
        if m_ == 0:
            n_ += 1
        elif n_ == 0:
            stack.append(m_ - 1)
            n_ = 1
        else:
            stack.append(m_ - 1)
            stack.append(m_)
            n_ -= 1
    return n_


def ackermann(m: int, n: int):
    """A(m, n) by closed forms for m <= 4 (checked against the equations for m <= 3); for m = 4 returns
    (the exponent tower height h, so that A = 2↑↑h - 3) when the value is too large to write."""
    if m == 0:
        return n + 1
    if m == 1:
        return n + 2
    if m == 2:
        return 2 * n + 3
    if m == 3:
        return 2 ** (n + 3) - 3
    if m == 4:
        h = n + 3
        if h <= 4:
            v = 1
            for _ in range(h):
                v = 2 ** v
            return v - 3
        return ("tower", h)
    raise ValueError("m <= 4 only")


def digits_of_2_pow(k: int) -> int:
    return int(k * math.log10(2)) + 1


# ---------------------------------------------------------------------------
# Gödel's β-function and the Chinese remainder theorem
# ---------------------------------------------------------------------------
def crt(pairs):
    """x with x ≡ r (mod m) for every (r, m), the moduli pairwise coprime; the least such x >= 0."""
    x, M = 0, 1
    for r, m in pairs:
        # solve x + M t ≡ r (mod m)
        t = ((r - x) * pow(M, -1, m)) % m
        x, M = x + M * t, M * m
    return x % M, M


def beta(c: int, d: int, i: int) -> int:
    return c % (1 + (i + 1) * d)


def beta_code(seq) -> tuple:
    """(c, d) with beta(c, d, i) = seq[i] for every i: Gödel's lemma, by the Chinese remainder theorem."""
    s = max([len(seq)] + list(seq))
    d = math.factorial(s)
    c, _ = crt([(a, 1 + (i + 1) * d) for i, a in enumerate(seq)])
    assert all(beta(c, d, i) == a for i, a in enumerate(seq))
    return c, d


SUNZI = [(2, 3), (3, 5), (2, 7)]   # 《孙子算经》: a number leaves 2 by threes, 3 by fives, 2 by sevens


# ---------------------------------------------------------------------------
# Gödel numbering
# ---------------------------------------------------------------------------
SYMBOLS = [("¬", r"\lnot"), ("∧", r"\land"), ("∨", r"\lor"), ("→", r"\to"), ("↔", r"\leftrightarrow"),
           ("∀", r"\forall"), ("∃", r"\exists"), ("=", "="), ("(", "("), (")", ")"), ("0", "0"),
           ("S", r"\mathsf{S}"), ("+", "+"), ("×", r"\times")]
CODE = {s: 2 * i + 1 for i, (s, _) in enumerate(SYMBOLS)}
VARS = ["x", "y", "z", "u", "v", "w"]
CODE.update({v: 2 * (i + 1) for i, v in enumerate(VARS)})
DECODE = {c: s for s, c in CODE.items()}
TEX = dict(SYMBOLS)


def primes(n: int) -> list:
    out, k = [], 2
    while len(out) < n:
        if all(k % p for p in out if p * p <= k):
            out.append(k)
        k += 1
    return out


def tokens(formula: str) -> list:
    return [c for c in formula if not c.isspace()]


def godel_number(formula: str) -> int:
    ts = tokens(formula)
    return math.prod(p ** CODE[t] for p, t in zip(primes(len(ts)), ts))


def godel_decode(n: int) -> str:
    out = []
    for p in primes(64):
        if n == 1:
            break
        e = 0
        while n % p == 0:
            n //= p
            e += 1
        if e == 0:
            raise ValueError("not a Gödel number: a gap in the primes")
        out.append(DECODE[e])
    if n != 1:
        raise ValueError("too long")
    return "".join(out)


def sequence_digits(formulas) -> int:
    """Number of decimal digits of the Gödel number 2^g1 * 3^g2 * ... of a sequence of formulas (a proof)."""
    gs = [godel_number(f) for f in formulas]
    return int(sum(g * math.log10(p) for g, p in zip(gs, primes(len(gs))))) + 1


# ---------------------------------------------------------------------------
# Self-reference: quines and the diagonal
# ---------------------------------------------------------------------------
QUINE = "s='s=%r;print(s%%s)';print(s%s)"


def run_python(src: str) -> str:
    buf = io.StringIO()
    with redirect_stdout(buf):
        exec(src, {})
    return buf.getvalue().rstrip("\n")


def quine_check(src: str = QUINE) -> bool:
    return run_python(src) == src


QUINE_PHRASE = "yields falsehood when preceded by its quotation"


def quine_sentence(phrase: str = QUINE_PHRASE) -> str:
    """Quine's (1966) liar without indexicals: the phrase preceded by its own quotation."""
    return f"“{phrase}” {phrase}"


def quine_subject(sentence: str) -> str:
    """What the sentence talks about: the quoted phrase, preceded by its own quotation."""
    q = sentence[1:sentence.index("”")]
    return quine_sentence(q)


def diag(template: str, var: str = "x") -> str:
    """The diagonalization of a template: replace the variable by the template's own quotation."""
    return template.replace(var, f"‘{template}’")


GODEL_TEMPLATE = "the diagonalization of x is unprovable"


def diag_subject(sentence: str) -> str:
    """The sentence names the diagonalization of the quoted template; compute it."""
    q = sentence[sentence.index("‘") + 1:sentence.rindex("’")]
    return diag(q)


# ---------------------------------------------------------------------------
# A formal system to play: Hofstadter's MIU
# ---------------------------------------------------------------------------
def miu_successors(s: str) -> list:
    out = []
    if s.endswith("I"):
        out.append((s + "U", 1))
    if s.startswith("M"):
        out.append((s + s[1:], 2))
    for i in range(len(s) - 2):
        if s[i:i + 3] == "III":
            out.append((s[:i] + "U" + s[i + 3:], 3))
    for i in range(len(s) - 1):
        if s[i:i + 2] == "UU":
            out.append((s[:i] + s[i + 2:], 4))
    return out


def miu_theorems(levels: int) -> list:
    """Theorems by number of rule applications: levels[k] = new theorems first reached in k steps."""
    seen, frontier, out = {"MI"}, ["MI"], [["MI"]]
    for _ in range(levels):
        nxt = []
        for s in frontier:
            for t, _ in miu_successors(s):
                if t not in seen:
                    seen.add(t)
                    nxt.append(t)
        out.append(sorted(nxt, key=lambda x: (len(x), x)))
        frontier = nxt
    return out


# ---------------------------------------------------------------------------
# Turing machines and busy beavers
# ---------------------------------------------------------------------------
STATES = "ABCDEFGH"


def parse_tm(code: str) -> dict:
    """Standard notation: '1RB1LB_1LA1RZ' = A0→1RB, A1→1LB, B0→1LA, B1→1R halt."""
    tm = {}
    for si, block in enumerate(code.split("_")):
        for sym in (0, 1):
            t = block[3 * sym:3 * sym + 3]
            if t == "---":
                continue
            tm[(STATES[si], sym)] = (int(t[0]), 1 if t[1] == "R" else -1, "H" if t[2] in "ZH" else t[2])
    return tm


def tm_code(tm: dict, n: int) -> str:
    blocks = []
    for st in STATES[:n]:
        b = ""
        for sym in (0, 1):
            if (st, sym) not in tm:
                b += "---"
                continue
            w, mv, nx = tm[(st, sym)]
            b += f"{w}{'R' if mv > 0 else 'L'}{'Z' if nx == 'H' else nx}"
        blocks.append(b)
    return "_".join(blocks)


def run_tm(tm: dict, max_steps: int = 10 ** 6, record: int = 0):
    """Run from a blank tape in state A. Returns dict(steps, ones, halted, history) where history holds the
    first ``record`` configurations as (tape dict copy, head, state)."""
    tape, head, state, steps, hist = {}, 0, "A", 0, []
    while state != "H" and steps < max_steps:
        if steps < record:
            hist.append((dict(tape), head, state))
        sym = tape.get(head, 0)
        if (state, sym) not in tm:
            break
        w, mv, nx = tm[(state, sym)]
        tape[head] = w
        head += mv
        state = nx
        steps += 1
    if record and steps < record:
        hist.append((dict(tape), head, state))
    return {"steps": steps, "ones": sum(tape.values()), "halted": state == "H", "history": hist}


def run_tm_fast(code: str, max_steps: int = 10 ** 8, size: int = 1 << 15) -> dict:
    """The same machine on a bytearray tape: fast enough for the five-state champion's 47 million steps."""
    tm = parse_tm(code)
    n = len(code.split("_"))
    W, M, N = [0] * (2 * n), [0] * (2 * n), [0] * (2 * n)
    for (st, sym), (w, mv, nx) in tm.items():
        i = 2 * STATES.index(st) + sym
        W[i], M[i], N[i] = w, mv, (-1 if nx == "H" else STATES.index(nx))
    tape = bytearray(size)
    head, state, steps, lo, hi = size // 2, 0, 0, size // 2, size // 2
    while state >= 0 and steps < max_steps:
        i = 2 * state + tape[head]
        tape[head] = W[i]
        head += M[i]
        state = N[i]
        steps += 1
        if head < lo:
            lo = head
        elif head > hi:
            hi = head
    return {"steps": steps, "ones": sum(tape), "halted": state < 0, "width": hi - lo + 1}


CHAMPIONS = {
    2: "1RB1LB_1LA1RZ",                               # Radó (1962): 6 steps, 4 ones
    3: "1RB1RZ_1LB0RC_1LC1LA",                        # Lin and Radó (1965): 21 steps, the most for 3
    4: "1RB1LB_1LA0LC_1RZ1LD_1RD0RA",                 # Brady (1983): 107 steps, 13 ones
    5: "1RB1LC_1RC1RB_1RD0LE_1LA1LD_1RZ0LA",          # Marxen and Buntrock (1989): 47,176,870 steps
}


def all_machines(n: int):
    """Every n-state, 2-symbol machine with all 2n transitions defined (halt allowed as a next state)."""
    choices = [(w, mv, nx) for w in (0, 1) for mv in (-1, 1) for nx in list(STATES[:n]) + ["H"]]
    keys = [(st, sym) for st in STATES[:n] for sym in (0, 1)]
    for combo in itertools.product(choices, repeat=len(keys)):
        yield dict(zip(keys, combo))


def busy_beaver_search(n: int, cap: int = 100) -> dict:
    """Run every n-state machine (n <= 2) for up to ``cap`` steps: the champions by steps and by ones."""
    best_steps, best_ones, halting, total = 0, 0, 0, 0
    for tm in all_machines(n):
        total += 1
        r = run_tm(tm, cap)
        if r["halted"]:
            halting += 1
            best_steps = max(best_steps, r["steps"])
            best_ones = max(best_ones, r["ones"])
    return {"machines": total, "halting": halting, "max_steps": best_steps, "max_ones": best_ones}


def space_time(code: str, steps: int, pad: int = 2):
    """The tape at each step as rows of 0/1 over the visited window, with the head position."""
    r = run_tm(parse_tm(code), steps, record=steps + 1)
    hist = r["history"]
    cells = [c for t, h, _ in hist for c in list(t) + [h]]
    lo, hi = min(cells) - pad, max(cells) + pad
    rows = [([t.get(c, 0) for c in range(lo, hi + 1)], h - lo, s) for t, h, s in hist]
    return rows


# ---------------------------------------------------------------------------
# Ramsey: R(3,3) = 6 by brute force
# ---------------------------------------------------------------------------
def mono_triangle_free(n: int) -> int:
    """How many red/blue colourings of the edges of K_n have no one-coloured triangle."""
    edges = list(itertools.combinations(range(n), 2))
    idx = {e: i for i, e in enumerate(edges)}
    tris = [(idx[(a, b)], idx[(a, c)], idx[(b, c)]) for a, b, c in itertools.combinations(range(n), 3)]
    count = 0
    for mask in range(1 << len(edges)):
        ok = True
        for i, j, k in tris:
            x, y, z = mask >> i & 1, mask >> j & 1, mask >> k & 1
            if x == y == z:
                ok = False
                break
        count += ok
    return count


# ---------------------------------------------------------------------------
# Berry: the least number a toy language cannot name in k symbols
# ---------------------------------------------------------------------------
def rpn_values(max_tokens: int, limit: int = 10 ** 7) -> dict:
    """Shortest RPN description of each number from digits 1–9 and + × ^ (results capped at ``limit``):
    value -> (length, expression)."""
    by_len = {1: {d: str(d) for d in range(1, 10)}}
    best = {d: (1, str(d)) for d in range(1, 10)}
    for L in range(3, max_tokens + 1, 2):
        cur = {}
        for la in range(1, L - 1, 2):
            lb = L - 1 - la
            if la not in by_len or lb not in by_len:
                continue
            for a, ea in by_len[la].items():
                for b, eb in by_len[lb].items():
                    for op in "+*^":
                        if op == "^":
                            if b > 64 or a ** min(b, 64) > limit:
                                continue
                            v = a ** b
                        else:
                            v = a + b if op == "+" else a * b
                        if v > limit or v in best or v in cur:
                            continue
                        cur[v] = f"{ea} {eb} {op}"
        by_len[L] = cur
        for v, e in cur.items():
            best[v] = (L, e)
    return best


def berry(max_tokens: int) -> int:
    best = rpn_values(max_tokens)
    n = 1
    while n in best:
        n += 1
    return n


def infix(rpn: str) -> str:
    st = []
    for t in rpn.split():
        if t in "+*^":
            b, a = st.pop(), st.pop()
            sym = {"+": "+", "*": r"\times", "^": "^"}[t]
            if t == "^":
                st.append(f"{{{a}}}^{{{b}}}" if len(a) == 1 else f"({a})^{{{b}}}")
            else:
                st.append(f"({a} {sym} {b})")
        else:
            st.append(t)
    s = st[0]
    return s[1:-1] if s.startswith("(") and s.endswith(")") else s


# ---------------------------------------------------------------------------
# Provability logic: GL on finite strict partial orders
# ---------------------------------------------------------------------------
def gl_frames(n: int):
    """Every transitive, irreflexive relation on n worlds: the finite frames of GL (Segerberg 1971)."""
    from . import modal
    pairs = [(a, b) for a in range(n) for b in range(n) if a != b]
    for mask in range(1 << len(pairs)):
        R = {pairs[i] for i in range(len(pairs)) if mask >> i & 1}
        if modal.transitive(R, n):
            yield R


def gl_valid(formula: str, max_worlds: int = 4):
    """Is the formula true in every world of every GL frame with at most ``max_worlds`` worlds? Returns
    (valid, frames checked)."""
    from . import modal
    f = modal.parse(formula)
    count = 0
    for n in range(1, max_worlds + 1):
        for R in gl_frames(n):
            count += 1
            if not modal.valid_on_frame(f, R, n):
                return False, count
    return True, count


GL_FACTS = {
    "second": "~[]bot -> ~[]~[]bot",                          # if consistent, consistency is unprovable
    "godel_fixed": "~[]bot <-> ~[](~[]bot)",                  # G := Con solves G <-> ~Prov(G)
    "henkin_fixed": "top <-> []top",                          # H := ⊤ solves H <-> Prov(H)
    "lob": "[]([]p -> p) -> []p",
    "reflection": "[]p -> p",                                 # not valid: soundness is unprovable
    "unique": "(p <-> ~[]p) & [](p <-> ~[]p) & (q <-> ~[]q) & [](q <-> ~[]q) -> (p <-> q)",
}


# ---------------------------------------------------------------------------
# Truth for bounded sentences: a Δ0 truth predicate, decided by finite search
# ---------------------------------------------------------------------------
_D0 = re.compile(r"\s*(∀|∃|¬|∧|∨|→|↔|≤|<|=|\+|×|\*|\(|\)|S|[a-z]|\d+)")


def delta0_eval(sentence: str, env=None) -> bool:
    """Decide a sentence of arithmetic whose quantifiers are all bounded (∀x<t, ∃x<t), e.g.
    '∀x<10 ∃y<10 (x+y=9)'. Bounded quantifiers are finite conjunctions and disjunctions, so this always halts:
    truth for Δ0 sentences is computable, and definable in arithmetic itself."""
    toks = _D0.findall(sentence)
    if "".join(toks) != sentence.replace(" ", ""):
        raise ValueError(f"cannot tokenize {sentence!r}")
    pos = [0]

    def peek():
        return toks[pos[0]] if pos[0] < len(toks) else None

    def eat(t=None):
        x = peek()
        if t is not None and x != t:
            raise ValueError(f"expected {t}, got {x}")
        pos[0] += 1
        return x

    # terms evaluate to functions of the environment
    def primary():
        t = peek()
        if t == "S":
            eat()
            f = primary()
            return lambda e: f(e) + 1
        if t == "(":
            eat()
            f = term()
            eat(")")
            return f
        eat()
        if t.isdigit():
            n = int(t)
            return lambda e: n
        return lambda e, v=t: e[v]

    def factor():
        f = primary()
        while peek() in ("×", "*"):
            eat()
            g, h = f, primary()
            f = lambda e, g=g, h=h: g(e) * h(e)
        return f

    def term():
        f = factor()
        while peek() == "+":
            eat()
            g, h = f, factor()
            f = lambda e, g=g, h=h: g(e) + h(e)
        return f

    def atom():
        a = term()
        op = eat()
        b = term()
        return {"=": lambda e: a(e) == b(e), "<": lambda e: a(e) < b(e), "≤": lambda e: a(e) <= b(e)}[op]

    def unary():
        t = peek()
        if t == "¬":
            eat()
            f = unary()
            return lambda e: not f(e)
        if t in ("∀", "∃"):
            eat()
            v = eat()
            eat("<")
            bound = primary()
            body = unary()
            if t == "∀":
                return lambda e: all(body({**e, v: i}) for i in range(bound(e)))
            return lambda e: any(body({**e, v: i}) for i in range(bound(e)))
        if t == "(":
            save = pos[0]
            try:
                eat()
                f = formula()
                eat(")")
                return f
            except (ValueError, KeyError, IndexError, AttributeError):
                pos[0] = save
        return atom()

    def formula():
        f = unary()
        t = peek()
        if t in ("∧", "∨"):
            eat()
            g = formula()
            return (lambda e: f(e) and g(e)) if t == "∧" else (lambda e: f(e) or g(e))
        if t == "→":
            eat()
            g = formula()
            return lambda e: (not f(e)) or g(e)
        if t == "↔":
            eat()
            g = formula()
            return lambda e: f(e) == g(e)
        return f

    f = formula()
    if peek() is not None:
        raise ValueError(f"trailing {peek()}")
    return bool(f(env or {}))


DELTA0_EXAMPLES = [
    ("∀x<10 ∃y<10 (x+y=9)", "every number below 10 has a partner summing to 9"),
    ("∃x<100 (x×x=2)", "2 has a whole square root below 100"),
    ("∀x<30 ∃y<30 (x=2×y ∨ x=2×y+1)", "every number below 30 is even or odd"),
    ("∃p<100 (90<p ∧ ∀a<p ∀b<p ¬(a×b=p))", "there is a prime between 90 and 100"),
]


# ---------------------------------------------------------------------------
# Proof-theoretic ordinals (from the literature, for display)
# ---------------------------------------------------------------------------
ORDINALS = [
    (r"$\mathrm{RCA}_0$, \ $\mathrm{WKL}_0$, \ $\mathrm{I}\Sigma_1$", r"\omega^\omega"),
    (r"Peano arithmetic \ (Gentzen 1936)", r"\varepsilon_0"),
    (r"$\mathrm{ATR}_0$ \ (Feferman, Schütte 1964)", r"\Gamma_0"),
    (r"$\mathrm{ID}_1$, \ Kripke--Platek set theory", r"\psi(\varepsilon_{\Omega + 1})"),
    (r"$\Pi^1_1\text{-}\mathrm{CA}_0$ \ (Buchholz, Pohlers, Takeuti)", r"\psi(\Omega_\omega)"),
]
