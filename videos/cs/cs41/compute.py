"""Precompute everything numerical in Part 41 of *Computer Science, Built* ("Version Control, Builds and
Dependencies").

    python -m videos.cs.cs41.compute              # everything missing
    python -m videos.cs.cs41.compute --force objects

Results are cached in ``.cache/cs41/<name>.json``; scenes call ``load(name)``.  The instruments are
``explainer/cs/vcs/`` (git, build, deps, ci); tests in tests/test_cs41_vcs.py.

Items:
    objects     our object store against the real git: blob, tree and commit ids for a three-file project
    ripple      one changed file: which ids change up the tree, and how many objects the two snapshots share
    bases       merge bases: a criss-cross history with two, and a random history of 60 commits
    bisect      binary search over history: steps against history length
    merge       a three-way merge of a small file, with one clean region and one conflict
    delta       every committed version of this repository's syllabus: loose objects against deltas
    builds      make against verifying traces with early cutoff, on a 200-file project, for six kinds of edit
    parallel    work, span and time of a clean build on 1 to 256 workers
    deps        a diamond dependency resolved; a 3-SAT formula as packages; solver work at the threshold
    queue       a merge queue: test runs per change against batch size and failure rate
    canary      canary analysis: power and false alarms against traffic
    affected    test selection by dependency graph: which test modules a change can affect, in this repository
    corrupt     one flipped bit in a stored object, detected by rehashing
    editgraph   Myers' example: the shortest edit script between ABCABBA and CBABAC
    sizes       this repository: objects and bytes in its whole history against the current commit's files
    cache       a shared build cache (constructive traces) between two machines
    trace       a resolver's backtracking steps on the diamond
    smallgraph  a twelve-file project drawn whole: what one header change rebuilds
    selection   for every library module, the share of test modules a change to it can affect
"""

from __future__ import annotations

from explainer.ai.cache import Cache

CACHE = Cache("cs41")
load = CACHE.load

FILES = {"README.md": b"The Job: count the words in thirty novels.\n",
         "src/job.py": b"import collections, sys\nprint(collections.Counter(sys.stdin.read().split()).most_common(20))\n",
         "src/util/io.py": b"def read(path):\n    return open(path).read()\n"}


def compute_objects() -> dict:
    import os
    import subprocess
    import tempfile

    from explainer.cs.vcs import git as G
    s = G.Store()
    blobs = {p: G.obj_id("blob", d) for p, d in FILES.items()}
    root = s.write_files(FILES)
    commit = s.commit(root, [], "first")
    env = dict(os.environ, GIT_AUTHOR_NAME="Ada", GIT_AUTHOR_EMAIL="ada@example.com", GIT_COMMITTER_NAME="Ada",
               GIT_COMMITTER_EMAIL="ada@example.com", GIT_AUTHOR_DATE="1700000000 +0000",
               GIT_COMMITTER_DATE="1700000000 +0000", GIT_CONFIG_GLOBAL="/dev/null", GIT_CONFIG_NOSYSTEM="1")
    with tempfile.TemporaryDirectory() as t:
        def git(*a):
            return subprocess.run(["git", "-C", t, "-c", "commit.gpgsign=false", *a], capture_output=True, text=True,
                                  env=env, check=True).stdout.strip()
        git("init", "-q")
        for p, d in FILES.items():
            os.makedirs(os.path.join(t, os.path.dirname(p)), exist_ok=True)
            with open(os.path.join(t, p), "wb") as f:
                f.write(d)
        git("add", "-A")
        git("commit", "-q", "-m", "first")
        real = {"tree": git("rev-parse", "HEAD^{tree}"), "commit": git("rev-parse", "HEAD"),
                "blobs": {p: git("hash-object", p) for p in FILES}}
    return {"ours": {"tree": root, "commit": commit, "blobs": blobs}, "git": real, "objects": len(s.objects),
            "match": real["tree"] == root and real["commit"] == commit and real["blobs"] == blobs}


def compute_ripple() -> dict:
    from explainer.cs.vcs import git as G
    a = G.Store()
    b = G.Store()
    ra = a.write_files(FILES)
    f2 = dict(FILES)
    f2["src/util/io.py"] = FILES["src/util/io.py"].replace(b"read()", b"read().lower()")
    rb = b.write_files(f2)
    shared = set(a.objects) & set(b.objects)
    return {"objects": len(a.objects), "shared": len(shared), "changed": len(a.objects) - len(shared),
            "root_a": ra, "root_b": rb}


def compute_bases() -> dict:
    from explainer.cs.vcs import git as G
    cc = G.criss_cross()
    h = G.random_history(60, seed=3)
    multi = []
    for a in range(30, 60):
        for b in range(a + 1, 60):
            mb = G.merge_bases(h, a, b)
            if len(mb) > 1:
                multi.append((a, b, mb))
    return {"criss_cross": {"parents": cc, "bases": G.merge_bases(cc, 5, 6)}, "random": {"parents": h},
            "pairs_with_several": len(multi), "pairs": 30 * 29 // 2, "example": multi[0] if multi else None}


def compute_bisect() -> dict:
    from explainer.cs.vcs import git as G
    rows = [{"commits": n, "steps": G.bisect(n, n * 2 // 3)["steps"]} for n in (10, 100, 1000, 10_000, 100_000,
                                                                               1_000_000)]
    ex = G.bisect(1000, 637)
    return {"rows": rows, "example": ex}


def compute_merge() -> dict:
    from explainer.cs.vcs import git as G
    base = ["def count(text):", "    words = text.split()", "    c = Counter(words)", "    return c.most_common(20)"]
    ours = ["def count(text):", "    words = text.lower().split()", "    c = Counter(words)",
            "    return c.most_common(20)"]
    theirs = ["def count(text):", "    words = text.split()", "    c = Counter(words)", "    return c.most_common(10)"]
    clash = ["def count(text):", "    words = text.casefold().split()", "    c = Counter(words)",
             "    return c.most_common(20)"]
    m1, c1 = G.merge3(base, ours, theirs)
    m2, c2 = G.merge3(base, ours, clash)
    return {"base": base, "ours": ours, "theirs": theirs, "clean": m1, "clean_conflicts": c1, "clash": clash,
            "conflicted": m2, "conflicts": c2}


def compute_delta() -> dict:
    from explainer.cs.vcs import git as G
    return G.delta_history("videos/cs/SYLLABUS.md")


def compute_builds() -> dict:
    from explainer.cs.vcs import build as B
    return B.scenarios()


def compute_parallel() -> dict:
    from explainer.cs.vcs import build as B
    return B.parallel_times()


def compute_deps() -> dict:
    from explainer.cs.vcs import deps as D
    u, root = D.diamond()
    chosen, stats, ncl = u.solve(root)
    cls = [[1, -2, 3], [-1, 2, -3], [2, 3, -4], [-2, -3, 4], [1, 4, 2]]
    u2, r2 = D.from_3sat(4, cls)
    ch2, st2, nc2 = u2.solve(r2)
    unsat = [[1, 2], [1, -2], [-1, 2], [-1, -2]]
    u3, r3 = D.from_3sat(2, unsat)
    ch3, _, _ = u3.solve(r3)
    return {"diamond": {"chosen": chosen, "clauses": ncl}, "formula": cls, "gadget": {"chosen": ch2,
            "clauses": nc2, "ok": D.check_assignment(cls, ch2), "packages": len(u2.pkgs)},
            "unsat_installable": ch3 is not None, "hardness": D.hardness(ns=(20, 40, 60, 80), trials=10)}


def compute_queue() -> dict:
    from explainer.cs.vcs import ci as C
    return {"rows": C.merge_queue_table(), "test_hours": 0.5}


def compute_canary() -> dict:
    from explainer.cs.vcs import ci as C
    return C.canary()


def compute_affected() -> dict:
    from collections import defaultdict

    from explainer.cs.se import repo as R
    g = R.import_graph()
    rev = defaultdict(set)
    for a, bs in g["edges"].items():
        for b in bs:
            rev[b].add(a)
    tests = [m for m in g["modules"] if m.startswith("tests.")]

    def affected(m):
        seen, st = {m}, [m]
        while st:
            x = st.pop()
            for y in rev[x]:
                if y not in seen:
                    seen.add(y)
                    st.append(y)
        return seen
    rows = []
    for m in ("explainer.cs.pebble.asm", "explainer.cs.dist.raft", "explainer.cs.se.kwic", "explainer.cs",
              "explainer.tts"):
        if m not in g["modules"]:
            continue
        s = affected(m)
        rows.append({"module": m, "modules_affected": len(s) - 1, "tests_affected": sum(1 for t in tests if t in s)})
    return {"rows": rows, "tests": len(tests), "modules": len(g["modules"])}


def compute_corrupt() -> dict:
    from explainer.cs.vcs import git as G
    return G.corruption_demo()


def compute_editgraph() -> dict:
    from explainer.cs.vcs import git as G
    return G.edit_graph()


def compute_sizes() -> dict:
    from explainer.cs.vcs import git as G
    return G.repo_sizes()


def compute_cache() -> dict:
    from explainer.cs.vcs import build as B
    return B.shared_cache_story()


def compute_trace() -> dict:
    from explainer.cs.vcs import deps as D
    u, r = D.diamond()
    return D.backtracking_trace(u, r)


def compute_selection() -> dict:
    from collections import defaultdict

    from explainer.cs.se import repo as R
    g = R.import_graph()
    rev = defaultdict(set)
    for a, bs in g["edges"].items():
        for b in bs:
            rev[b].add(a)
    tests = {m for m in g["modules"] if m.startswith("tests.")}
    fr = []
    for m in g["modules"]:
        if not m.startswith("explainer."):
            continue
        seen, st = {m}, [m]
        while st:
            x = st.pop()
            for y in rev[x]:
                if y not in seen:
                    seen.add(y)
                    st.append(y)
        fr.append(len(seen & tests) / len(tests))
    fr.sort()
    n = len(fr)
    buckets = [sum(1 for x in fr if lo <= x < lo + 0.1 or (lo >= 0.9 and x == 1.0)) for lo in [i / 10 for i in range(10)]]
    return {"modules": n, "tests": len(tests), "median": fr[n // 2], "mean": sum(fr) / n,
            "under_5pct": sum(1 for x in fr if x < 0.05) / n, "hist": buckets}


def compute_smallgraph() -> dict:
    from explainer.cs.vcs import build as B
    return B.small_graph_rebuild()


ITEMS = {k[8:]: v for k, v in globals().items() if k.startswith("compute_")}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
