"""Testing as science (Part 54, chapter 13): property-based testing with shrinking, a fuzzer that finds a bug planted
in the Pebble compiler and delta-debugs the program that shows it, differential testing of the Job, and coverage.

* **Property-based testing** after QuickCheck (Claessen and Hughes, "QuickCheck: a lightweight tool for random
  testing of Haskell programs", ICFP 2000): a generator makes random inputs of growing size; when a property fails,
  the input is *shrunk*, greedily, by trying smaller candidates until none still fails, so the report is a small
  counterexample rather than a big random one.
* **Fuzzing** after Csmith (Yang, Chen, Eide and Regehr, PLDI 2011): Part 13's ``fuzz.program(seed)`` writes random,
  well-defined Pebble-language programs and ``fuzz.differential`` runs each through the IR interpreter and the
  compiler at every level.  :func:`planted_bug` breaks one optimization *for the duration of a with-block* (the
  compiler's files are not edited); the failing program is then minimized by removing statements and blocks while
  the disagreement persists (Zeller and Hildebrandt's delta debugging, 2002, in the hierarchical form of Misherghi
  and Su, 2006).
* **Differential testing of the Job**: the compiled Job at every level against the IR interpreter and against an
  independent Python reference on a few texts.  This is testing, not translation validation (Pnueli, Siegel and
  Singerman 1998; Necula 2000), which would prove each compiled program equivalent to its source for *every* input.
* **Coverage** with ``sys.settrace``: lines and branch outcomes reached by a test set.  It shows where tests have not
  been; it cannot show that the code they did reach is right.
"""

from __future__ import annotations

import ast
import contextlib
import inspect
import random
import sys
import textwrap
import time


# ---------------------------------------------------------------------------------- generators and shrinking

class Gen:
    """A generator: ``generate(rng, size)`` makes a value, ``shrink(value)`` lists smaller candidates (most
    aggressive first)."""

    def __init__(self, generate, shrink, name: str = "gen"):
        self.generate = generate
        self.shrink = shrink
        self.name = name

    def map(self, f, name=None) -> "Gen":
        """Apply f to generated values and to every shrink candidate (f should be idempotent, like sorted)."""
        return Gen(lambda r, n: f(self.generate(r, n)), lambda v: (f(c) for c in self.shrink(v)), name or self.name)


def shrink_int(x: int):
    """Towards zero: 0, then halving the distance, then one step; and the positive twin of a negative number."""
    if x == 0:
        return
    yield 0
    if x < 0:
        yield -x
    seen = {0, -x}
    d = x // 2 if x > 0 else -((-x) // 2)
    while d != 0:
        c = x - d
        if c not in seen:
            seen.add(c)
            yield c
        d = d // 2 if d > 0 else -((-d) // 2)
    c = x - 1 if x > 0 else x + 1
    if c not in seen:
        yield c


def ints(lo: int = -100, hi: int = 100) -> Gen:
    """Integers in [lo, hi], scaled by the size (small values first, as QuickCheck does)."""
    def gen(r, size):
        m = max(1, size)
        return r.randint(max(lo, -m), min(hi, m))
    return Gen(gen, shrink_int, "int")


def lists(elem: Gen, max_len: int = 30) -> Gen:
    """Lists of elem; shrinking removes chunks (halves, then smaller, down to single elements), then shrinks every
    copy of a repeated value together (as Hypothesis does), then one element at a time."""
    def gen(r, size):
        return [elem.generate(r, size) for _ in range(r.randint(0, min(max_len, size)))]

    def shrink(xs):
        n = len(xs)
        k = n // 2
        while k >= 1:
            for i in range(0, n - k + 1, k):
                yield xs[:i] + xs[i + k:]
            k //= 2
        for v in dict.fromkeys(x for x in xs if xs.count(x) > 1):   # equal elements shrink together
            for c in elem.shrink(v):
                yield [c if x == v else x for x in xs]
        for i, x in enumerate(xs):
            for c in elem.shrink(x):
                yield xs[:i] + [c] + xs[i + 1:]
    return Gen(gen, shrink, f"list({elem.name})")


def tuples(*gens: Gen) -> Gen:
    def gen(r, size):
        return tuple(g.generate(r, size) for g in gens)

    def shrink(t):
        for i, g in enumerate(gens):
            for c in g.shrink(t[i]):
                yield t[:i] + (c,) + t[i + 1:]
    return Gen(gen, shrink, "(" + ", ".join(g.name for g in gens) + ")")


def _fails(prop, x) -> bool:
    try:
        return not prop(x)
    except Exception:                  # noqa: BLE001 — a crash is a failure too
        return True


def forall(prop, gen: Gen, trials: int = 200, seed: int = 0, max_size: int = 30, max_shrinks: int = 10_000) -> dict:
    """Test ``prop`` on ``trials`` random inputs of growing size.  On the first failure, shrink greedily: take the
    first candidate that still fails, and repeat until no candidate fails.  Returns {"ok", "trials", "original",
    "shrunk", "steps" (each accepted shrink), "candidates_tried"}."""
    r = random.Random(seed)
    for t in range(trials):
        size = 1 + t * max_size // max(1, trials - 1)
        x = gen.generate(r, size)
        if not _fails(prop, x):
            continue
        original, steps, tried = x, [x], 0
        progress = True
        while progress and tried < max_shrinks:
            progress = False
            for c in gen.shrink(x):
                tried += 1
                if _fails(prop, c):
                    x = c
                    steps.append(c)
                    progress = True
                    break
        return {"ok": False, "trials": t + 1, "original": original, "shrunk": x, "steps": steps,
                "candidates_tried": tried}
    return {"ok": True, "trials": trials}


# ---- the buggy functions and their properties

def sort_dedup(xs: list) -> list:
    """A 'sort' that goes through a set: it drops duplicates."""
    return sorted(set(xs))


def prop_sort(xs) -> bool:
    """The output is ordered and a permutation of the input."""
    ys = sort_dedup(xs)
    return all(a <= b for a, b in zip(ys, ys[1:])) and sorted(xs) == sorted(ys)


def buggy_insert(xs: list, x: int) -> list:
    """Insert x into the sorted list xs, with an off-by-one in the scan: it never looks past the second-to-last
    element, so a value larger than every element lands before the last one."""
    i = 0
    while i < len(xs) - 1 and xs[i] < x:
        i += 1
    return xs[:i] + [x] + xs[i:]


def prop_insert(arg) -> bool:
    xs, x = arg
    ys = buggy_insert(xs, x)
    return all(a <= b for a, b in zip(ys, ys[1:])) and sorted(xs + [x]) == ys


def pbt_results(seed: int = 0) -> dict:
    """Both properties tested and their counterexamples shrunk."""
    a = forall(prop_sort, lists(ints()), seed=seed)
    b = forall(prop_insert, tuples(lists(ints()).map(sorted, "sorted list(int)"), ints()), seed=seed)
    return {"sort_dedup": a, "insert": b}


# ------------------------------------------------------------------------------- fuzzing the Pebble compiler

BUGS = {
    "floor-division": "SCCP's constant folder divides with Python's floor semantics (// and %) instead of "
                      "Pebble's truncation toward zero, which only differs when exactly one operand is negative",
}


class _BuggyFolder:
    """Stands in for the interpreter module that ``opt.sccp`` folds constants with (``opt.interp``)."""

    def __init__(self, real):
        self._real = real

    def binop(self, op, a, b):
        s32 = self._real.s32
        a, b = s32(a), s32(b)
        if op in ("div", "rem") and b != 0 and (a < 0) != (b < 0):
            return s32(a // b if op == "div" else a % b)
        return self._real.binop(op, a, b)

    def __getattr__(self, name):
        return getattr(self._real, name)


@contextlib.contextmanager
def planted_bug(kind: str = "floor-division"):
    """Inside the block, the compiler's SCCP pass folds constants wrongly (see :data:`BUGS`).  Only the folder
    seen by ``opt.py`` is replaced; the IR interpreter that serves as the reference keeps the right semantics."""
    if kind not in BUGS:
        raise ValueError(kind)
    from explainer.cs.lang.compiler import opt as O
    saved = O.interp
    O.interp = _BuggyFolder(saved)
    try:
        yield
    finally:
        O.interp = saved


def _disagreeing(r: dict, levels) -> list:
    return [lv for lv in levels if r.get(lv) != r["ref"]]


def hunt(kind: str = "floor-division", seeds=range(0, 60), levels=(0, 1, 2, 3)) -> dict:
    """Generate programs seed by seed and run each differentially with the bug planted, until one disagrees.  Then
    rerun every seed tried without the bug: they must all agree (the fuzzer's finding is the bug, not noise)."""
    from explainer.cs.lang.compiler import fuzz
    t0 = time.perf_counter()
    tried, stuck, found = [], 0, None
    with planted_bug(kind):
        for s in seeds:
            src = fuzz.program(s)
            r = fuzz.differential(src, levels)
            tried.append(s)
            if r["ok"] is None:
                stuck += 1
                continue
            if r["ok"] is False:
                found = (s, src, r)
                break
    t_hunt = time.perf_counter() - t0
    clean = {}
    for s in tried:
        r = fuzz.differential(fuzz.program(s), levels)
        clean[s] = r["ok"]
    out = {"bug": kind, "description": BUGS[kind], "programs": len(tried), "skipped_stuck": stuck,
           "hunt_seconds": round(t_hunt, 2), "clean_agree": all(v is not False for v in clean.values()),
           "clean": clean, "found": None}
    if found:
        s, src, r = found
        bad = _disagreeing(r, levels)
        ref = r["ref"]
        got = r[bad[0]]
        first = next((i for i, (a, b) in enumerate(zip(ref, got)) if a != b), min(len(ref), len(got))) \
            if isinstance(got, bytes) else None
        out["found"] = {"seed": s, "levels_disagree": bad, "levels_agree": [lv for lv in levels if lv not in bad],
                        "lines": len(src.splitlines()), "chars": len(src), "statements": src.count(";"),
                        "functions": src.count("fn "), "output_bytes": len(ref), "first_difference": first,
                        "ref": ref.hex(), "got": got.hex() if isinstance(got, bytes) else got, "src": src}
    return out


def _interesting(src: str, kind: str, levels, max_steps: int) -> bool:
    """The program is valid, its reference run finishes, some level disagrees with the bug planted, and every
    level agrees without it."""
    from explainer.cs.lang.compiler import fuzz
    try:
        with planted_bug(kind):
            r = fuzz.differential(src, levels, max_steps=max_steps)
        if r["ok"] is not False:
            return False
        return fuzz.differential(src, levels, max_steps=max_steps)["ok"] is True
    except Exception:                  # noqa: BLE001 — a candidate that does not parse or check is not interesting
        return False


def _units(lines: list[str]) -> list[tuple[int, int]]:
    """Removable units [i, j): a statement line, or a block from a line ending in '{' to its closing brace (for
    '} else {' lines: the else part, leaving the brace that closes the then-part)."""
    out = []
    for i, l in enumerate(lines):
        s = l.strip()
        if not s or s == "}":
            continue
        if s.endswith("{"):
            depth = 0
            for j in range(i, len(lines)):
                depth += lines[j].count("{") - lines[j].count("}")
                if j > i and depth <= 0 or (j == i and depth < 0):
                    break
            if s.startswith("}"):                   # "} else {": drop through the line before the else's "}"
                out.append((i, j))
            else:
                out.append((i, j + 1))
        elif s.endswith(";") or s.endswith("}"):
            out.append((i, i + 1))
    return out


def shrink_program(src: str, kind: str = "floor-division", levels=(3,), max_steps: int = 100_000,
                   max_tests: int = 600) -> dict:
    """Hierarchical delta debugging: sweep the units from the bottom up (callers sit below their callees, so calls
    go before the functions they call), removing each one whose removal keeps the program interesting; repeat the
    sweep until it removes nothing.  Returns {"src", "lines", "tests", "accepted", "seconds", "history"}."""
    t0 = time.perf_counter()
    lines = src.splitlines()
    if not _interesting(src, kind, levels, max_steps):
        raise ValueError("the program does not show the bug")
    cache = {}
    tests = 0
    history = [len(lines)]
    changed = True
    while changed and tests < max_tests:
        changed = False
        k = len(_units(lines)) - 1
        while k >= 0 and tests < max_tests:
            units = _units(lines)
            if k >= len(units):
                k = len(units) - 1
                continue
            i, j = units[k]
            cand = lines[:i] + lines[j:]
            key = "\n".join(cand)
            if key not in cache:
                tests += 1
                cache[key] = _interesting(key, kind, levels, max_steps)
            if cache[key]:
                lines = cand
                history.append(len(lines))
                changed = True
            k -= 1
    out = "\n".join(ln for ln in lines if ln.strip())       # blank lines carry no meaning
    from explainer.cs.lang.compiler import fuzz
    with planted_bug(kind):
        r = fuzz.differential(out, (0, 1, 2, 3), max_steps=max_steps)
    clean = fuzz.differential(out, (0, 1, 2, 3), max_steps=max_steps)
    bad = _disagreeing(r, (0, 1, 2, 3))
    return {"src": out, "lines_before": len(src.splitlines()), "lines": len(out.splitlines()),
            "statements": out.count(";"),
            "tests": tests, "accepted": len(history) - 1, "history": history,
            "seconds": round(time.perf_counter() - t0, 2), "levels_disagree": bad,
            "ref": r["ref"].hex(), "got": {lv: (r[lv].hex() if isinstance(r[lv], bytes) else r[lv]) for lv in bad},
            "clean_ok": clean["ok"]}


def fuzz_results(kind: str = "floor-division") -> dict:
    h = hunt(kind)
    out = {"hunt": {k: v for k, v in h.items() if k != "clean"}}
    if h["found"]:
        out["shrunk"] = shrink_program(h["found"]["src"], kind, tuple(h["found"]["levels_disagree"]))
    return out


# ------------------------------------------------------------------------------- differential testing of the Job

JOB_TAPES = [
    b"",
    b"the cat sat on the mat",
    b"It was the best of times, it was the worst of times, it was the age of wisdom, it was the age of foolishness.",
    b"A man, a plan, a canal: Panama!  A MAN, A PLAN.\nNo 'x' in Nixon; x x x.",
    b"one two two three three three four four four four five five five five five six six six six six six "
    b"seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen twenty "
    b"twentyone twentytwo one",
]


def job_differential(tapes=None, levels=(0, 1, 2, 3)) -> dict:
    """The Job (Part 13's Pebble-language source) compiled at each level and run on the emulator, against the IR
    interpreter (what the program means) and against Python's ``job_reference`` (what it should print).  Agreement
    on these inputs is evidence, not proof: this is differential testing, not translation validation."""
    from explainer.cs.lang import pebble_lang as P
    from explainer.cs.lang.compiler import check as C
    from explainer.cs.lang.compiler import driver as D
    from explainer.cs.lang.compiler import interp as IT
    from explainer.cs.lang.compiler import lower as L
    from explainer.cs.pebble import programs as PR
    tapes = JOB_TAPES if tapes is None else tapes
    prog = P.parse(P.JOB)
    m = L.lower(prog, C.check(prog))
    compiled = {lv: D.compile_program(P.JOB, lv) for lv in levels}
    rows = []
    for tape in tapes:
        it = IT.run(m, tape)
        ref = bytes(it.out)
        py = PR.job_reference(tape)
        row = {"bytes": len(tape), "words": len(PR.job_words(tape)), "output": ref.decode(), "interp_matches_python":
               ref == py, "levels": {}}
        for lv in levels:
            mm = D.run(compiled[lv], tape)
            row["levels"][lv] = {"agree": bytes(mm.output) == ref, "steps": mm.steps}
        rows.append(row)
    return {"tapes": len(tapes), "rows": rows,
            "all_agree": all(r["interp_matches_python"] and all(v["agree"] for v in r["levels"].values())
                             for r in rows)}


# ------------------------------------------------------------------------------------------------------ coverage

def triangle(a: int, b: int, c: int) -> str:
    """Myers' triangle classifier (*The Art of Software Testing*, 1979)."""
    if a <= 0 or b <= 0 or c <= 0:
        return "invalid"
    if a + b <= c or a + c <= b or b + c <= a:
        return "invalid"
    if a == b and b == c:
        return "equilateral"
    if a == b or b == c or a == c:
        return "isosceles"
    return "scalene"


def _branches(fn) -> list[tuple[int, int]]:
    """(condition line, first line of the true branch) for each if / elif / while in fn."""
    src = textwrap.dedent(inspect.getsource(fn))
    first = fn.__code__.co_firstlineno
    out = []
    for node in ast.walk(ast.parse(src)):
        if isinstance(node, (ast.If, ast.While)):
            out.append((node.lineno + first - 1, node.body[0].lineno + first - 1))
    return sorted(out)


def coverage(fn, inputs) -> dict:
    """Run fn on each input (a tuple of arguments) under ``sys.settrace`` and report line coverage (over the lines
    that carry bytecode) and branch coverage (each condition's true and false outcomes: the true outcome is the
    next line being the first line of the branch body)."""
    code = fn.__code__
    lines = sorted({ln for _, _, ln in code.co_lines() if ln is not None and ln != code.co_firstlineno})
    hit, arcs = set(), set()
    prev = [None]

    def local(frame, event, arg):
        if event == "line":
            if prev[0] is not None:
                arcs.add((prev[0], frame.f_lineno))
            hit.add(frame.f_lineno)
            prev[0] = frame.f_lineno
        elif event == "return":
            if prev[0] is not None:
                arcs.add((prev[0], -1))
        return local

    def tracer(frame, event, arg):
        if event == "call" and frame.f_code is code:
            prev[0] = None
            return local
        return None
    outputs = []
    old = sys.gettrace()
    sys.settrace(tracer)
    try:
        for args in inputs:
            outputs.append(fn(*args))
    finally:
        sys.settrace(old)
    br = _branches(fn)
    srclines = inspect.getsource(fn).splitlines()
    outcomes = []
    for cond, body in br:
        succ = {b for a, b in arcs if a == cond}
        outcomes.append({"line": cond - code.co_firstlineno, "true": body in succ, "false": bool(succ - {body})})
    covered = sum(o["true"] + o["false"] for o in outcomes)
    return {"tests": len(inputs), "lines": len(lines), "lines_hit": len(hit & set(lines)),
            "line_coverage": len(hit & set(lines)) / len(lines),
            "missed_lines": [ln - code.co_firstlineno for ln in lines if ln not in hit],
            "missed_source": [srclines[ln - code.co_firstlineno].strip() for ln in lines if ln not in hit],
            "branches": 2 * len(br), "branches_hit": covered, "branch_coverage": covered / (2 * len(br)) if br else 1.0,
            "outcomes": outcomes, "outputs": outputs}


def coverage_results(seed: int = 0, tests: int = 300) -> dict:
    """What coverage tells you: random triangles (sides 1..100) never reach 'equilateral', and coverage points at
    the line.  What it does not: three passing unit tests cover every line and branch of buggy_insert, which is
    still wrong (and the property test of :func:`pbt_results` finds it)."""
    r = random.Random(seed)
    rand = [(r.randint(1, 100), r.randint(1, 100), r.randint(1, 100)) for _ in range(tests)]
    tri = coverage(triangle, rand)
    tri["kinds"] = {k: tri["outputs"].count(k) for k in sorted(set(tri["outputs"]))}
    tri.pop("outputs")
    unit = [([1, 3, 5], 4), ([], 2), ([2, 4], 1)]
    ins = coverage(buggy_insert, unit)
    ins["unit_tests_pass"] = all(buggy_insert(xs, x) == sorted(xs + [x]) for xs, x in unit)
    ins.pop("outputs")
    ins["property"] = forall(prop_insert, tuples(lists(ints()).map(sorted), ints()), seed=seed)
    return {"triangle_random": tri, "insert_unit": ins}


def all_results() -> dict:
    return {"pbt": pbt_results(), "coverage": coverage_results(), "job": job_differential(), "fuzz": fuzz_results()}
