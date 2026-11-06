"""Testing instruments for Part 40: a suite with planted flaky tests run in random orders, order-dependence found by
isolation and bisection, and mutation testing of a real module of this repository."""

from __future__ import annotations

import ast
import copy
import random
import types


# ---------------------------------------------------------------- a flaky suite

class World:
    """What tests share: a global cache, a clock, a scheduler with random latency."""

    def __init__(self, rng: random.Random):
        self.rng = rng
        self.cache: dict = {}
        self.clock = 0.0


def _make_suite(n_ok: int = 180, seed: int = 0):
    """``n_ok`` deterministic tests plus planted flaky ones of the kinds Luo et al. (2014) found most common:
    asynchronous waits, order dependence (a polluter and its victim, a test that needs a setter), time, and
    unordered collections.  Each test is (name, kind, function(world) -> bool)."""
    tests = []
    for i in range(n_ok):
        tests.append((f"test_ok_{i:03d}", "deterministic", lambda w, i=i: (i * 7919) % 13 != 99))

    def async_wait(w, budget=50.0):
        # sleeps a fixed 50 ms for a reply whose latency is random
        return w.rng.lognormvariate(3.0, 0.45) < budget
    for k in range(3):
        tests.append((f"test_async_{k}", "async wait", async_wait))

    def polluter(w):
        w.cache["user"] = "admin"
        return True

    def victim(w):
        return w.cache.get("user") is None          # assumes a clean cache

    def setter(w):
        w.cache["config"] = {"retries": 3}
        return True

    def needs_setter(w):
        return w.cache.get("config", {}).get("retries") == 3   # silently depends on test_setter running first
    tests += [("test_polluter", "order (polluter)", polluter), ("test_victim", "order (victim)", victim),
              ("test_setter", "order (setter)", setter), ("test_needs_setter", "order (needs setter)", needs_setter)]

    def time_dep(w):
        # fails when the run crosses an hour boundary between two reads of the clock
        t0 = w.clock + w.rng.uniform(0, 3600)
        return int(t0 // 3600) == int((t0 + 40) // 3600)
    tests.append(("test_report_date", "time", time_dep))

    def unordered(w):
        s = list({w.rng.random() for _ in range(3)})
        return s == sorted(s) or w.rng.random() < 0.9    # passes unless the set order differs and luck runs out
    tests.append(("test_tags_order", "unordered collection", unordered))
    return tests


def run_suite(tests, order, rng):
    w = World(rng)
    return {name: fn(w) for name, _, fn in (tests[i] for i in order)}


def flaky_campaign(runs: int = 400, seed: int = 0, retries: int = 2):
    """Run the suite ``runs`` times in random orders.  Report per-test failure rates, the fraction of suite runs
    with at least one failure, the fraction still red with ``retries`` automatic re-runs of failing tests, and which
    failures disappear in isolation (order dependence)."""
    rng = random.Random(seed)
    tests = _make_suite(seed=seed)
    idx = list(range(len(tests)))
    fails = {t[0]: 0 for t in tests}
    red = red_retry = 0
    for _ in range(runs):
        rng.shuffle(idx)
        res = run_suite(tests, idx, rng)
        bad = [n for n, ok in res.items() if not ok]
        for n in bad:
            fails[n] += 1
        if bad:
            red += 1
            still = []
            for n in bad:
                k = next(i for i, t in enumerate(tests) if t[0] == n)
                ok = any(run_suite(tests, [k], rng)[n] for _ in range(retries))
                if not ok:
                    still.append(n)
            if still:
                red_retry += 1
    isolated = {}
    for n, c in fails.items():
        if c:
            k = next(i for i, t in enumerate(tests) if t[0] == n)
            isolated[n] = sum(not run_suite(tests, [k], rng)[n] for _ in range(200)) / 200
    kinds = {t[0]: t[1] for t in tests}
    rows = [{"test": n, "kind": kinds[n], "fail_rate": c / runs, "isolated_fail_rate": isolated.get(n, 0.0)}
            for n, c in fails.items() if c]
    rows.sort(key=lambda r: -r["fail_rate"])
    return {"tests": len(tests), "runs": runs, "red_runs": red / runs, "red_after_retry": red_retry / runs,
            "rows": rows, "retries": retries}


def find_polluter(seed: int = 3):
    """Given an order in which the victim fails, bisect the tests before it to find the one that pollutes."""
    rng = random.Random(seed)
    tests = _make_suite()
    names = [t[0] for t in tests]
    v = names.index("test_victim")
    while True:
        order = list(range(len(tests)))
        rng.shuffle(order)
        if order.index(v) > order.index(names.index("test_polluter")):
            break
    before = order[:order.index(v)]
    steps = 0
    cand = before
    while len(cand) > 1:
        half = cand[:len(cand) // 2]
        steps += 1
        if not run_suite(tests, half + [v], rng)["test_victim"]:
            cand = half
        else:
            cand = cand[len(cand) // 2:]
    return {"before": len(before), "steps": steps, "found": names[cand[0]]}


# ---------------------------------------------------------------- mutation testing

class _Mutator(ast.NodeTransformer):
    SWAP = {ast.Lt: ast.LtE, ast.LtE: ast.Lt, ast.Gt: ast.GtE, ast.GtE: ast.Gt, ast.Eq: ast.NotEq, ast.NotEq: ast.Eq,
            ast.Add: ast.Sub, ast.Sub: ast.Add, ast.Mult: ast.FloorDiv, ast.FloorDiv: ast.Mult, ast.BitAnd: ast.BitOr,
            ast.BitOr: ast.BitAnd, ast.LShift: ast.RShift, ast.RShift: ast.LShift, ast.And: ast.Or, ast.Or: ast.And}

    def __init__(self, target: int):
        self.target, self.k, self.desc = target, -1, None

    def _hit(self, node, what):
        self.k += 1
        if self.k == self.target:
            self.desc = (getattr(node, "lineno", 0), what)
            return True
        return False

    def visit_Compare(self, node):
        self.generic_visit(node)
        op = node.ops[0]
        if type(op) in self.SWAP and self._hit(node, f"{type(op).__name__} -> {self.SWAP[type(op)].__name__}"):
            node.ops[0] = self.SWAP[type(op)]()
        return node

    def visit_BinOp(self, node):
        self.generic_visit(node)
        if type(node.op) in self.SWAP and self._hit(node, f"{type(node.op).__name__} -> "
                                                          f"{self.SWAP[type(node.op)].__name__}"):
            node.op = self.SWAP[type(node.op)]()
        return node

    def visit_BoolOp(self, node):
        self.generic_visit(node)
        if type(node.op) in self.SWAP and self._hit(node, f"{type(node.op).__name__} -> "
                                                          f"{self.SWAP[type(node.op)].__name__}"):
            node.op = self.SWAP[type(node.op)]()
        return node

    def visit_Constant(self, node):
        if isinstance(node.value, int) and not isinstance(node.value, bool) and self._hit(node, f"{node.value} -> "
                                                                                                 f"{node.value + 1}"):
            return ast.copy_location(ast.Constant(node.value + 1), node)
        return node


def count_sites(tree) -> int:
    m = _Mutator(-1)
    m.visit(copy.deepcopy(tree))
    return m.k + 1


def mutate(tree, k):
    m = _Mutator(k)
    t = m.visit(copy.deepcopy(tree))
    ast.fix_missing_locations(t)
    return t, m.desc


def mutation_run(module_name: str, check, max_mutants: int | None = None, seed: int = 0, timeout_s: float = 2.0):
    """Mutate ``module_name`` one site at a time (comparison, arithmetic and boolean operators, integer constants),
    load each mutant as a fresh module and run ``check(module) -> bool`` (True = the tests pass).  A mutant is
    killed if the tests fail, raise, or run past ``timeout_s``.  Returns the mutation score and the survivors."""
    import importlib
    import inspect
    mod = importlib.import_module(module_name)
    src = inspect.getsource(mod)
    tree = ast.parse(src)
    n = count_sites(tree)
    sites = list(range(n))
    if max_mutants and n > max_mutants:
        sites = sorted(random.Random(seed).sample(sites, max_mutants))
    assert check(mod), "the tests must pass on the original"
    killed, survivors = 0, []
    for k in sites:
        t, desc = mutate(tree, k)
        m = types.ModuleType(module_name)
        m.__dict__["__name__"] = module_name
        import signal

        def _alarm(*_):
            raise TimeoutError
        old = signal.signal(signal.SIGALRM, _alarm)
        signal.setitimer(signal.ITIMER_REAL, timeout_s)
        try:
            exec(compile(t, module_name, "exec"), m.__dict__)
            ok = check(m)
        except BaseException as e:      # a failure, an exception or a timeout all kill the mutant
            if isinstance(e, KeyboardInterrupt):
                raise
            ok = False
        finally:
            signal.setitimer(signal.ITIMER_REAL, 0)
            signal.signal(signal.SIGALRM, old)
        if ok:
            survivors.append({"line": desc[0], "mutation": desc[1]})
        else:
            killed += 1
    return {"module": module_name, "sites": n, "mutants": len(sites), "killed": killed,
            "score": killed / len(sites) if sites else 1.0, "survivors": survivors}


def pebble_asm_check(m) -> bool:
    """Run this repository's Pebble core tests (tests/test_cs_pebble_core.py) against module ``m`` standing in for
    explainer.cs.pebble.asm."""
    import importlib
    import io
    import unittest
    import explainer.cs.pebble as P
    tmod = importlib.import_module("tests.test_cs_pebble_core")
    saved = (P.assemble, tmod.assemble, tmod.AsmError)
    try:
        P.assemble = tmod.assemble = m.assemble
        tmod.AsmError = m.AsmError
        suite = unittest.TestSuite(unittest.defaultTestLoader.loadTestsFromTestCase(getattr(tmod, c))
                                   for c in ("EncodingTests", "AluTests", "ProgramTests"))
        res = unittest.TextTestRunner(stream=io.StringIO(), verbosity=0).run(suite)
        return res.wasSuccessful()
    finally:
        P.assemble, tmod.assemble, tmod.AsmError = saved


def line_coverage(module_name: str, run_tests) -> dict:
    """Statement coverage of a module while ``run_tests()`` runs, by tracing line events."""
    import importlib
    import inspect
    import sys
    mod = importlib.import_module(module_name)
    path = inspect.getsourcefile(mod)
    src = inspect.getsource(mod)
    tree = ast.parse(src)
    stmts = {n.lineno for n in ast.walk(tree) if isinstance(n, ast.stmt) and not isinstance(
        n, (ast.FunctionDef, ast.ClassDef, ast.Import, ast.ImportFrom)) and not (
        isinstance(n, ast.Expr) and isinstance(getattr(n, "value", None), ast.Constant))}
    hit = set()

    def tracer(frame, event, arg):
        if frame.f_code.co_filename == path:
            if event == "line":
                hit.add(frame.f_lineno)
            return tracer
        return None
    sys.settrace(tracer)
    try:
        run_tests()
    finally:
        sys.settrace(None)
    covered = stmts & hit
    return {"statements": len(stmts), "covered": len(covered), "coverage": len(covered) / len(stmts),
            "missed_lines": sorted(stmts - hit)}


# ---------------------------------------------------------------- behavioural subtyping, found by a property test

class Rectangle:
    def __init__(self, w, h):
        self.w, self.h = w, h

    def set_width(self, w):
        self.w = w

    def set_height(self, h):
        self.h = h

    def area(self):
        return self.w * self.h


class Square(Rectangle):
    """A square is-a rectangle in geometry, but not in behaviour: setting one side sets both."""

    def __init__(self, s):
        super().__init__(s, s)

    def set_width(self, w):
        self.w = self.h = w

    def set_height(self, h):
        self.w = self.h = h


def rect_property(r, w, h) -> bool:
    """What every client of Rectangle may rely on: after set_width(w) and set_height(h), area() == w * h."""
    r.set_width(w)
    r.set_height(h)
    return r.area() == w * h


def property_test(make, prop, trials: int = 1000, seed: int = 0, lo: int = 0, hi: int = 1000):
    """Random testing with shrinking, in the style of QuickCheck (Claessen and Hughes 2000): try random (w, h);
    on a failure, shrink each argument towards ``lo`` while the property still fails."""
    rng = random.Random(seed)
    for k in range(1, trials + 1):
        w, h = rng.randint(lo, hi), rng.randint(lo, hi)
        if not prop(make(), w, h):
            found = (w, h)
            changed = True
            while changed:
                changed = False
                for i in (0, 1):
                    for cand in (lo, found[i] // 2, found[i] - 1):
                        if cand < lo or cand == found[i]:
                            continue
                        t = list(found)
                        t[i] = cand
                        if not prop(make(), *t):
                            found = tuple(t)
                            changed = True
                            break
            return {"failed_after": k, "first": (w, h), "shrunk": found}
    return {"failed_after": None, "trials": trials}


# ---------------------------------------------------------------- fuzzing the assembler

FUZZ_OPS = ["add", "sub", "addi", "li", "la", "lw", "sw", "lb", "sb", "beq", "bne", "beqz", "j", "jal", "call",
            "ret", "not", "neg", "mv", "nop", "halt", ".word", ".byte", ".ascii", ".asciiz", ".space", ".align",
            ".org", ".equ", "lui", "ori", "jr", "slt"]
FUZZ_ARGS = ["a0", "a1", "t0", "zero", "sp", "ra", "0", "1", "-1", "4", "0x10", "64(zero)", "-4(sp)", "x", "x+4",
             "x-1", "'a'", "'\\n'", "\"hi\"", "\"\"", "label", "99999999", "-99999999", "()", "(a0)", "8(a9)", ""]


def fuzz_asm(trials: int = 20000, seed: int = 0):
    """Random programs of one to five lines built from real mnemonics and operand shapes.  The assembler's contract:
    accept, or raise AsmError with a line number.  Any other exception is a crash.  Returns crashes grouped by the
    source line that raised them, with the shortest input for each."""
    import traceback
    from explainer.cs.pebble import AsmError, assemble
    rng = random.Random(seed)
    groups: dict = {}
    ok = rejected = crashed = 0
    for _ in range(trials):
        lines = []
        for _ in range(rng.randint(1, 5)):
            lab = "x: " if rng.random() < 0.3 else ""
            op = rng.choice(FUZZ_OPS)
            a = ", ".join(rng.choice(FUZZ_ARGS) for _ in range(rng.randint(0, 3)))
            lines.append(f"{lab}{op} {a}".rstrip())
        src = "\n".join(lines)
        try:
            assemble(src)
            ok += 1
        except AsmError:
            rejected += 1
        except Exception as e:      # the contract says AsmError only
            crashed += 1
            tb = traceback.extract_tb(e.__traceback__)[-1]
            k = f"{type(e).__name__}@{tb.lineno}"
            g = groups.setdefault(k, {"error": type(e).__name__, "line": tb.lineno, "count": 0, "example": src,
                                      "message": str(e)[:90]})
            g["count"] += 1
            if len(src) < len(g["example"]):
                g["example"] = src
    # shrink each example to the single offending line where possible
    for g in groups.values():
        for ln in g["example"].splitlines():
            try:
                assemble(ln)
            except AsmError:
                continue
            except Exception as e:
                if type(e).__name__ == g["error"]:
                    g["example"] = ln
                    break
            except BaseException:
                pass
    rows = sorted(groups.values(), key=lambda g: -g["count"])
    return {"trials": trials, "accepted": ok, "rejected": rejected, "crashed": crashed, "sites": len(rows),
            "rows": rows}
