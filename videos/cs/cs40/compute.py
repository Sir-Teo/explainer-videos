"""Precompute everything numerical in Part 40 of *Computer Science, Built* ("Software Engineering").

    python -m videos.cs.cs40.compute              # everything missing
    python -m videos.cs.cs40.compute --force repo

Results are cached in ``.cache/cs40/<name>.json``; scenes call ``load(name)``.  The instruments are
``explainer/cs/se/`` (kwic, repo, testing, process); tests in tests/test_cs40_se.py.

Items:
    kwic        Parnas's KWIC index built both ways; four changes; modules and lines touched in each
    repo        this repository's import graph: modules, edges, cycles, layer crossings, coupling, instability
    history     this repository's git history: commits, lines, the most-changed files
    lsp         a property test finds that Square is not a behavioural subtype of Rectangle, and shrinks it
    flaky       a 189-test suite with eight planted flaky tests, run in 400 random orders; retries; isolation
    polluter    bisection finds the test that pollutes shared state
    mutation    mutation testing of the Pebble assembler against this repository's tests; statement coverage
    debt        a model of technical debt: features delivered against the time spent refactoring
    brooks      Brooks' law as a simulation: adding people at different months; team size from the start
    estimate    Monte Carlo schedules of lognormal tasks: plan, P50, P80, P95, chance of meeting the plan
    kanban      work in progress as a queue: limits, throughput, cycle and lead time, Little's law
    cochange    logical coupling in this repository's history: files that change in the same commits
    merges      merge conflicts against how often branches are integrated
    fuzz        random programs against the Pebble assembler: crashes that should have been clean errors
    natural     the naturalness of software: a trigram model's bits per token on this repository's code and on
                the novels
"""

from __future__ import annotations

from explainer.ai.cache import Cache

CACHE = Cache("cs40")
load = CACHE.load


def compute_kwic() -> dict:
    from explainer.cs.se import kwic as K
    e = K.experiment()
    e["d1_lines"] = {m: src.strip().count("\n") + 1 for m, src in K.D1.items()}
    e["d2_lines"] = {m: src.strip().count("\n") + 1 for m, src in K.D2.items()}
    return e


def compute_repo() -> dict:
    from explainer.cs.se import repo as R
    m = R.metrics()
    per = m.pop("per")
    by_pkg = {}
    for name, v in per.items():
        top = ".".join(name.split(".")[:2])
        d = by_pkg.setdefault(top, {"modules": 0, "lines": 0})
        d["modules"] += 1
        d["lines"] += v["lines"]
    inst = sorted(v["I"] for v in per.values() if v["ca"] + v["ce"])
    m["by_package"] = dict(sorted(by_pkg.items(), key=lambda kv: -kv[1]["lines"]))
    m["instability_hist"] = [sum(1 for x in inst if lo <= x < lo + 0.1 or (lo == 0.9 and x == 1.0))
                             for lo in [i / 10 for i in range(10)]]
    m["isolated"] = sum(1 for v in per.values() if v["ca"] + v["ce"] == 0)
    m["upward_edges"] = [[a, b] for a, bs in R.import_graph(packages=("explainer", "videos"))["edges"].items()
                         for b in bs if a.startswith("explainer") and b.startswith("videos")]
    return m


def compute_history() -> dict:
    from explainer.cs.se import repo as R
    return R.git_history()


def compute_lsp() -> dict:
    from explainer.cs.se import testing as T
    return {"rectangle": T.property_test(lambda: T.Rectangle(1, 1), T.rect_property),
            "square": T.property_test(lambda: T.Square(1), T.rect_property)}


def compute_flaky() -> dict:
    from explainer.cs.se import testing as T
    return T.flaky_campaign()


def compute_polluter() -> dict:
    from explainer.cs.se import testing as T
    return T.find_polluter()


def compute_mutation() -> dict:
    import explainer.cs.pebble.asm as A
    from explainer.cs.se import testing as T
    r = T.mutation_run("explainer.cs.pebble.asm", T.pebble_asm_check, timeout_s=5)
    c = T.line_coverage("explainer.cs.pebble.asm", lambda: T.pebble_asm_check(A))
    return _mutation_summary(r, c)


def _mutation_summary(r, c):
    import inspect

    import explainer.cs.pebble.asm as A
    src = inspect.getsource(A).splitlines()
    missed = set(c["missed_lines"])
    for s in r["survivors"]:
        s["covered"] = s["line"] not in missed
        s["code"] = src[s["line"] - 1].strip()
    r["survivors_covered"] = sum(s["covered"] for s in r["survivors"])
    return {"mutation": r, "coverage": c}


def compute_debt() -> dict:
    from explainer.cs.se import process as P
    return P.debt_table()


def compute_brooks() -> dict:
    from explainer.cs.se import process as P
    return P.brooks_table()


def compute_estimate() -> dict:
    from explainer.cs.se import process as P
    return P.estimation_table()


def compute_kanban() -> dict:
    from explainer.cs.se import process as P
    return {"rows": P.kanban_table(), "workers": 4, "arrivals": 0.8, "work_mean": 4.0}


def compute_cochange() -> dict:
    from explainer.cs.se import repo as R
    return R.co_change()


def compute_merges() -> dict:
    from explainer.cs.se import process as P
    r = P.merge_conflicts()
    for x in r["rows"]:
        x["hunks_per_week"] = x["hunks_per_merge"] * 168.0 / x["interval_h"]
    return r


def compute_natural() -> dict:
    from explainer.cs.se import repo as R
    return R.naturalness(tokens=400_000)


def compute_fuzz() -> dict:
    from explainer.cs.se import testing as T
    return T.fuzz_asm()


ITEMS = {k[8:]: v for k, v in globals().items() if k.startswith("compute_")}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
