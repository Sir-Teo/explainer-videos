"""Precompute everything numerical in Part 35 of *Computer Science, Built* ("Databases").

    python -m videos.cs.cs35.compute              # everything missing
    python -m videos.cs.cs35.compute --force job

Results are cached in ``.cache/cs35/<name>.json``; scenes call ``load(name)``.  The instruments are
``explainer/cs/db/`` (rel.py: relational algebra and dependencies; engine.py: SQL, Volcano iterators, statistics
and a Selinger optimizer; joins.py: join algorithms with counted I/O; bptree.py; txn.py: serializability, 2PL,
isolation levels; aries.py) and ``sqlite3`` on this machine; tests in tests/test_cs35_db.py.

Items:
    job         the Job as one line of SQL over the thirty novels (4.6 million rows): our engine's plan and answer,
                the hand-written Job's answer, and sqlite3's answer, plan and time on this machine; ledger row 13
    algebra     small tables through selection, projection, join, union, difference and renaming
    normal      a badly designed table and its update anomalies; keys, BCNF and 3NF decompositions, lossless checks
    iterators   a Volcano pipeline: tuples per operator, the plan EXPLAIN prints
    joins       block nested loops, index nested loops, sort-merge and Grace hash: I/O counted against formulas
    optimizer   the size of plan space; Selinger's dynamic program on five tables against exhaustive search; the best
                and the worst order, executed
    estimation  the independence assumption on correlated columns, and skew against 1/NDV
    btree       levels against rows for a fanout of 400; our index on the novels; clustered against unclustered
    serial      schedules and precedence graphs; how many interleavings are conflict- and view-serializable
    locking     strict 2PL on random workloads: always serializable; waits, deadlocks, wait-die and wound-wait
    isolation   the anomalies each isolation level allows; the doctors on call under SI, SSI and 2PL
    aries       one crashed log through analysis, redo and undo; 500 random crashes, with crashes during recovery
    columns     a row store against a column store, and tuple-at-a-time against vectorized, on this machine
    frontier    the triangle query: pairwise joins against a worst-case optimal join, and the AGM bound
"""

from __future__ import annotations

import json
import math
import random
import sqlite3
import tempfile
import time
from pathlib import Path

from explainer.ai.cache import Cache

CACHE = Cache("cs35")
load = CACHE.load

JOB_SQL = "SELECT word, COUNT(*) FROM words GROUP BY word ORDER BY 2 DESC LIMIT 20"


def _corpus():
    """(book id, title, year) rows and (book id, position, word) rows for the thirty novels."""
    import videos.ai.ai1.compute as A
    from explainer.cs.pebble import programs as PR
    from videos.cs.cs6.compute import novels
    books = novels()
    brow, wrow = [], []
    for bid, (gid, title) in enumerate(A.BOOKS.items()):
        brow.append((bid, title, gid))
        for pos, w in enumerate(PR.job_words(PR.job_tape(books[gid]))):
            wrow.append((bid, pos, w.decode()))
    return brow, wrow


# ---- the Job as SQL: ledger row 13 -------------------------------------------------------------------------------
def compute_job() -> dict:
    from explainer.cs.db.engine import Database
    from explainer.cs.pebble import programs as PR
    from videos.cs.cs31.compute import _full_text
    brow, wrow = _corpus()
    db = Database(page_rows=100, buffer_pages=1000)
    db.create("books", ["book_id", "title", "gutenberg"], brow)
    db.create("words", ["book_id", "pos", "word"], wrow)
    plans = {}
    for name, force in (("hash aggregate", {"agg": "hash"}), ("sort aggregate", {"agg": "sort"})):
        p = db.plan(JOB_SQL, force=force)
        plans[name] = {"cost": p.cost, "explain": db.explain(p)}
    p = db.plan(JOB_SQL)
    st = {}
    t = time.perf_counter()
    ours = db.run(p, st)
    ours_s = time.perf_counter() - t
    ref = [ln.split() for ln in PR.job_reference(_full_text()).decode().splitlines()]
    job_top = [(w, int(c)) for w, c in ref]
    with tempfile.TemporaryDirectory() as d:
        con = sqlite3.connect(str(Path(d, "novels.db")))
        con.execute("create table books(book_id integer, title text, gutenberg integer)")
        con.execute("create table words(book_id integer, pos integer, word text)")
        t = time.perf_counter()
        con.executemany("insert into books values (?,?,?)", brow)
        con.executemany("insert into words values (?,?,?)", wrow)
        con.commit()
        load_s = time.perf_counter() - t
        best = 1e9
        for _ in range(3):
            t = time.perf_counter()
            lite = con.execute(JOB_SQL).fetchall()
            best = min(best, time.perf_counter() - t)
        qplan = [r[-1] for r in con.execute("EXPLAIN QUERY PLAN " + JOB_SQL).fetchall()]
        con.execute("create index words_word on words(word)")
        best_ix = 1e9
        for _ in range(3):
            t = time.perf_counter()
            lite_ix = con.execute(JOB_SQL).fetchall()
            best_ix = min(best_ix, time.perf_counter() - t)
        qplan_ix = [r[-1] for r in con.execute("EXPLAIN QUERY PLAN " + JOB_SQL).fetchall()]
        whale = "SELECT title, COUNT(*) FROM words JOIN books ON words.book_id = books.book_id " \
                "WHERE word = 'whale' GROUP BY title ORDER BY 2 DESC LIMIT 5"
        lite_whale = con.execute(whale).fetchall()
        con.close()
    assert [tuple(r) for r in lite] == [tuple(r) for r in ours] == [tuple(r) for r in job_top]
    assert lite_ix == lite
    db.index("words", "word")
    pw = db.plan(whale)
    stw = {}
    ours_whale = db.run(pw, stw)
    assert [r[1] for r in ours_whale] == [r[1] for r in lite_whale]          # ties may come in either order
    led = json.loads((Cache("cs34").dir / "ledger.json").read_text())
    led = [r for r in led if r["part"] != 35]
    led.append({"part": 35, "label": r"one line of SQL, \ sqlite3 here", "seconds": best, "native": True,
                "load_seconds": load_s, "indexed_seconds": best_ix, "ours_seconds": ours_s})
    CACHE.dir.mkdir(parents=True, exist_ok=True)
    (CACHE.dir / "ledger.json").write_text(json.dumps(led, indent=1))
    return {"sql": JOB_SQL, "rows": len(wrow), "books": len(brow), "top": [list(r) for r in ours],
            "explain": db.explain(p), "plans": plans, "stats": st, "ours_seconds": ours_s,
            "sqlite_seconds": best, "sqlite_indexed_seconds": best_ix, "load_seconds": load_s,
            "sqlite_plan": qplan, "sqlite_plan_indexed": qplan_ix, "whale_sql": whale,
            "whale": [list(r) for r in ours_whale], "whale_explain": db.explain(pw), "whale_stats": stw,
            "ledger": led, "distinct": db.tables["words"].ndv["word"]}


# ---- the relational model ----------------------------------------------------------------------------------------
def compute_algebra() -> dict:
    from explainer.cs.db import rel as R
    books = R.table(["book", "author", "year"], [("Emma", "Austen", 1815), ("Persuasion", "Austen", 1817),
                                                 ("Dracula", "Stoker", 1897), ("Ulysses", "Joyce", 1922)])
    authors = R.table(["author", "born"], [("Austen", 1775), ("Stoker", 1847), ("Joyce", 1882)])
    sel = R.sigma(books, lambda r: r["year"] < 1900)
    proj = R.pi(books, ["author"])
    jn = R.join(books, authors)
    q = R.pi(R.sigma(R.join(books, authors), lambda r: r["year"] - r["born"] < 45), ["book"])
    later = R.table(["book", "author", "year"], [("Ulysses", "Joyce", 1922), ("Mrs Dalloway", "Woolf", 1925)])
    return {"books": {"cols": books.cols, "rows": books.rows}, "authors": {"cols": authors.cols, "rows": authors.rows},
            "select": {"cols": sel.cols, "rows": sel.rows}, "project": {"cols": proj.cols, "rows": proj.rows},
            "join": {"cols": jn.cols, "rows": jn.rows}, "young": {"cols": q.cols, "rows": q.rows},
            "union": {"cols": R.union(books, later).cols, "rows": R.union(books, later).rows},
            "minus": {"cols": R.minus(books, later).cols, "rows": R.minus(books, later).rows}}


def compute_normal() -> dict:
    from explainer.cs.db import rel as R
    # student, course, instructor, office: course -> instructor, instructor -> office
    rows = [("ana", "db", "codd", "e12"), ("ben", "db", "codd", "e12"), ("cy", "db", "codd", "e12"),
            ("ana", "os", "ritchie", "w3"), ("cy", "os", "ritchie", "w3")]
    attrs = "SCIO"
    fds = [R.fd("C", "I"), R.fd("I", "O")]
    keys = ["".join(sorted(k)) for k in R.keys(attrs, fds)]
    bcnf = ["".join(sorted(x)) for x in R.bcnf_decompose(attrs, fds)]
    three = ["".join(sorted(x)) for x in R.synthesize_3nf(attrs, fds)]
    viol = R.bcnf_violation(attrs, fds)
    # an anomaly: Codd moves office; every row of every student of his courses must change
    moves = sum(1 for r in rows if r[2] == "codd")
    fds2 = [R.fd("S C", "I"), R.fd("I", "C")]                   # the classic: BCNF loses a dependency
    b2 = R.bcnf_decompose(["S", "C", "I"], fds2)
    return {"rows": rows, "fds": [["".join(sorted(l)), "".join(sorted(r))] for l, r in fds], "keys": keys,
            "violation": ["".join(sorted(viol[0])), "".join(sorted(viol[1]))], "bcnf": bcnf, "three": three,
            "lossless_bcnf": R.lossless(attrs, [frozenset(x) for x in bcnf], fds),
            "lossless_bad": R.lossless(attrs, [frozenset("SC"), frozenset("SIO")], fds), "office_rows": moves,
            "closure_C": "".join(sorted(R.closure("C", fds))),
            "sci": {"parts": ["".join(sorted(x)) for x in b2],
                    "preserves": all(any(l | r <= x for x in b2) for l, r in fds2)}}


# ---- query processing --------------------------------------------------------------------------------------------
def _small_db(seed=2):
    from explainer.cs.db.engine import Database
    brow, wrow = _corpus_sample(seed)
    db = Database(page_rows=100, buffer_pages=50)
    db.create("books", ["book_id", "title", "gutenberg"], brow)
    db.create("words", ["book_id", "pos", "word"], wrow)
    return db, brow, wrow


def _corpus_sample(seed=2, per_book=4000):
    """The first ``per_book`` words of each novel."""
    brow, wrow = _corpus()
    return brow, [r for r in wrow if r[1] < per_book]


def compute_iterators() -> dict:
    db, brow, wrow = _small_db()
    db.index("words", "word")
    sql = "SELECT title, COUNT(*) FROM words JOIN books ON words.book_id = books.book_id " \
          "WHERE word = 'whale' GROUP BY title ORDER BY 2 DESC LIMIT 3"
    out = {}
    for name, force in (("chosen", {}), ("hash join, full scan", {"join": "hash", "access": "Scan"}),
                        ("nested loops", {"join": "nested loops", "access": "Scan"})):
        p = db.plan(sql, force=force)
        st = {}
        rows = db.run(p, st)
        out[name] = {"explain": db.explain(p), "cost": p.cost, "stats": st, "rows": [list(r) for r in rows]}
    return {"sql": sql, "plans": out, "words": len(wrow)}


def compute_joins() -> dict:
    from explainer.cs.db.joins import compare
    rows = []
    for B in (5, 10, 20, 40, 80):
        r = compare(n_r=20_000, n_s=10_000, page_rows=50, B=B, keys=5_000)
        rows.append(r)
    return {"rows": rows}


def compute_optimizer() -> dict:
    from explainer.cs.db.engine import Database, count_plans
    rng = random.Random(7)
    db = Database(page_rows=100, buffer_pages=20)
    # a chain of five tables with very different sizes
    sizes = {"a": 50, "b": 20_000, "c": 500, "d": 30_000, "e": 200}
    keys = {"a": 50, "b": 500, "c": 500, "d": 200, "e": 200}
    for t, n in sizes.items():
        db.create(t, ["id", "k1", "k2"], [(i, rng.randrange(keys[t]), rng.randrange(keys[t])) for i in range(n)])
    sql = ("SELECT COUNT(*) FROM a JOIN b ON a.k1 = b.k1 JOIN c ON b.k2 = c.k1 JOIN d ON c.k2 = d.k1 "
           "JOIN e ON d.k2 = e.k1 WHERE a.id < 10")
    t0 = time.perf_counter()
    best = db.plan(sql)
    dp_considered = db.considered
    dp_s = time.perf_counter() - t0
    t0 = time.perf_counter()
    ex = db.plan(sql, exhaustive=True)
    ex_considered = db.considered
    ex_s = time.perf_counter() - t0
    st = {}
    ans = db.run(best, st)
    # the worst left-deep order with hash joins: e d c b a without the filter first
    from itertools import permutations
    from explainer.cs.db.engine import Join, Scan, parse
    q = parse(sql)
    aliases = {a: db.tables[t] for t, a in q.tables}
    costs = []
    for perm in permutations(aliases):
        p = Scan(db, aliases[perm[0]], perm[0], [x for x in q.where if x[0].split(".")[0] == perm[0]])
        seen = {perm[0]}
        for a in perm[1:]:
            on = []
            for x, y in q.joins:
                if x.split(".")[0] in seen and y.split(".")[0] == a:
                    on.append((x, y))
                elif y.split(".")[0] in seen and x.split(".")[0] == a:
                    on.append((y, x))
            r = Scan(db, aliases[a], a, [w for w in q.where if w[0].split(".")[0] == a])
            p = Join(db, p, r, on, "hash" if on else "nested loops")
            seen.add(a)
        costs.append({"order": "".join(perm), "cost": p.cost, "rows": p.rows})
    costs.sort(key=lambda c: c["cost"])
    return {"sizes": sizes, "sql": sql, "explain": db.explain(best), "best_cost": best.cost,
            "exhaustive_cost": ex.cost, "dp_considered": dp_considered, "ex_considered": ex_considered,
            "dp_seconds": dp_s, "ex_seconds": ex_s, "answer": ans[0][0], "stats": st,
            "orders": {"best": costs[0], "median": costs[len(costs) // 2], "worst": costs[-1], "n": len(costs)},
            "plan_space": [count_plans(n) for n in range(2, 13)]}


def compute_estimation() -> dict:
    from explainer.cs.db.engine import Database
    rng = random.Random(3)
    cities = [(f"city{i}", f"country{i // 10}") for i in range(200)]     # 10 cities per country
    rows = []
    for i in range(100_000):
        c, k = rng.choice(cities)
        rows.append((i, c, k, rng.randrange(100)))
    db = Database()
    db.create("people", ["id", "city", "country", "age"], rows)
    out = []
    for desc, sql in (("one city", "SELECT COUNT(*) FROM people WHERE city = 'city42'"),
                      ("city and its country", "SELECT COUNT(*) FROM people WHERE city = 'city42' AND "
                                               "country = 'country4'"),
                      ("city and age", "SELECT COUNT(*) FROM people WHERE city = 'city42' AND age < 50"),
                      ("age range", "SELECT COUNT(*) FROM people WHERE age < 20")):
        p = db.plan(sql)
        scan = p
        while scan.children():
            scan = scan.children()[0]
        actual = db.run(p)[0][0]
        out.append({"desc": desc, "sql": sql, "estimate": scan.rows, "actual": actual})
    # skew: words
    brow, wrow = _corpus_sample()
    db2 = Database()
    db2.create("words", ["book_id", "pos", "word"], wrow)
    ndv = db2.tables["words"].ndv["word"]
    est = len(wrow) / ndv
    from collections import Counter
    cnt = Counter(r[2] for r in wrow)
    skew = [{"word": w, "actual": cnt[w], "estimate": est} for w in ("the", "whale", "ship", "zeal")]
    return {"rows": out, "skew": skew, "ndv": ndv, "n": len(wrow)}


def compute_btree() -> dict:
    from explainer.cs.db.bptree import BPlusTree, levels_for
    levels = [{"rows": 10 ** k, "levels": levels_for(10 ** k, 400)} for k in range(3, 13)]
    brow, wrow = _corpus()
    t = BPlusTree(order=400)
    groups: dict = {}
    for rid, r in enumerate(wrow):
        groups.setdefault(r[2], []).append(rid)
    for k in sorted(groups):
        t.insert(k, len(groups[k]))
    t.check()
    # clustered against unclustered: a range of words, rows on 100-row pages
    lo, hi = "whale", "whales"
    hits = [rid for rid, r in enumerate(wrow) if lo <= r[2] <= hi]
    pages_unclustered = len({rid // 100 for rid in hits})
    pages_clustered = math.ceil(len(hits) / 100)
    return {"levels": levels, "distinct": len(groups), "height": t.height(), "nodes": t.nodes(),
            "range": [lo, hi], "hits": len(hits), "pages_unclustered": pages_unclustered,
            "pages_clustered": pages_clustered, "rows": len(wrow)}


# ---- transactions ---------------------------------------------------------------------------------------------------
def compute_serial() -> dict:
    from explainer.cs.db import txn as X
    lost = [(1, "r", "x"), (2, "r", "x"), (1, "w", "x"), (2, "w", "x"), (1, "c", None), (2, "c", None)]
    ok = [(1, "r", "x"), (1, "w", "x"), (2, "r", "x"), (2, "w", "x"), (1, "r", "y"), (1, "w", "y"), (2, "r", "y"),
          (2, "w", "y"), (1, "c", None), (2, "c", None)]
    blind = [(1, "r", "x"), (2, "w", "x"), (1, "w", "x"), (3, "w", "x"), (1, "c", None), (2, "c", None),
             (3, "c", None)]
    ex = {}
    for name, s in (("lost update", lost), ("serializable", ok), ("blind writes", blind)):
        cs, w = X.conflict_serializable(s)
        vs, order = X.view_serializable(s)
        ex[name] = {"schedule": [[t, a, x] for t, a, x in s], "edges": sorted(map(list, X.precedence(s))),
                    "conflict": cs, "witness": w, "view": vs, "view_order": order}
    # every interleaving of three transactions of two steps
    import itertools
    T = {1: [("r", "x"), ("w", "y")], 2: [("r", "y"), ("w", "x")], 3: [("w", "x"), ("w", "y")]}
    seqs = set()
    for perm in itertools.permutations([1, 1, 2, 2, 3, 3]):
        seqs.add(perm)
    total = conf = view = 0
    for perm in seqs:
        idx = {t: 0 for t in T}
        s = []
        for t in perm:
            a, x = T[t][idx[t]]
            idx[t] += 1
            s.append((t, a, x))
        s += [(t, "c", None) for t in T]
        total += 1
        conf += X.conflict_serializable(s)[0]
        view += X.view_serializable(s)[0]
    return {"examples": ex, "interleavings": total, "conflict": conf, "view": view}


def compute_locking() -> dict:
    from explainer.cs.db import txn as X
    rng = random.Random(11)
    res = {}
    for policy in ("detect", "wait-die", "wound-wait"):
        n = ser = aborts = waits = dl = 0
        for _ in range(400):
            ts = {t: [(rng.choice("rw"), rng.choice("ABCD")) for _ in range(4)] for t in (1, 2, 3, 4)}
            order = [rng.choice((1, 2, 3, 4)) for _ in range(40)]
            r = X.run_2pl(ts, order, policy=policy)
            n += 1
            ser += X.conflict_serializable(r["schedule"])[0]
            aborts += len(r["aborted"])
            waits += r["waits"]
            dl += r["deadlocks"]
        res[policy] = {"runs": n, "serializable": ser, "aborts": aborts, "waits": waits, "deadlocks": dl}
    ex = X.run_2pl({1: [("r", "A"), ("w", "B")], 2: [("r", "B"), ("w", "A")]}, [1, 2, 1, 2, 1, 2])
    return {"policies": res, "deadlock_example": ex}


def compute_isolation() -> dict:
    from explainer.cs.db import txn as X
    table = X.anomaly_table()
    case = X.CASES()["write skew"]
    doctors = {}
    for lv in ("snapshot", "snapshot + SSI", "serializable", "read committed"):
        r = X.run_level(lv, case["init"], case["programs"], case["order"])
        doctors[lv] = {"db": r["db"], "committed": r["committed"], "aborted": r["aborted"]}
    return {"levels": list(X.LEVELS), "table": table, "doctors": doctors, "anomalies": list(X.CASES())}


def compute_aries() -> dict:
    from explainer.cs.db import aries as A
    s = A.System(npages=4, seed=12)
    total = A.workload(A.System(npages=4, seed=12), n_txn=3, ops=3, ckpt_every=0)
    s = A.System(npages=4, seed=12)
    A.workload(s, n_txn=3, ops=3, crash_at=total - 1, ckpt_every=0)
    s.crash()
    survived = [{"lsn": r.lsn, "kind": r.kind, "txn": r.txn, "page": r.page, "before": r.before, "after": r.after,
                 "prev": r.prev} for r in s.log]
    disk = {p: list(v) for p, v in s.disk.items()}
    expect = A.committed_state(s, 4)
    r = A.recover(s)
    got = {p: v for p, (v, _) in s.disk.items()}
    after = [{"lsn": x.lsn, "kind": x.kind, "txn": x.txn, "page": x.page, "undo_next": x.undo_next}
             for x in s.log[len(survived):]]
    stats = {"runs": 0, "ok": 0, "ok_undo_crash": 0, "recrashed": 0, "redone": 0, "skipped": 0, "undone": 0}
    for seed in range(500):
        a = A.crash_and_recover(seed)
        b = A.crash_and_recover(seed, crash_in_undo=True)
        stats["runs"] += 1
        stats["ok"] += a["ok"]
        stats["ok_undo_crash"] += b["ok"]
        stats["recrashed"] += b.get("recrashed", False)
        stats["redone"] += a.get("redone", 0)
        stats["skipped"] += a.get("skipped", 0)
        stats["undone"] += a.get("undone", 0)
    return {"log": survived, "disk_at_crash": disk, "expect": expect, "recovered": got, "ok": got == expect,
            "passes": {k: v for k, v in r.items() if k != "analysis"}, "analysis": r["analysis"], "appended": after,
            "random": stats}


# ---- analytics ---------------------------------------------------------------------------------------------------
def compute_columns() -> dict:
    import numpy as np
    n, cols = 1_000_000, 16
    rng = np.random.default_rng(0)
    rows = rng.integers(0, 1000, size=(n, cols), dtype=np.int64)        # a row store: each row contiguous
    colstore = [np.ascontiguousarray(rows[:, j]) for j in range(cols)]  # a column store

    def best(f, k=5):
        b = 1e9
        for _ in range(k):
            t = time.perf_counter()
            v = f()
            b = min(b, time.perf_counter() - t)
        return b, v
    t_row, v1 = best(lambda: int(rows[rows[:, 7] < 100, 3].sum()))
    t_col, v2 = best(lambda: int(colstore[3][colstore[7] < 100].sum()))
    assert v1 == v2
    small = rows[:200_000].tolist()
    t0 = time.perf_counter()
    s = 0
    for r in small:                                                     # tuple at a time, in Python
        if r[7] < 100:
            s += r[3]
    t_tuple = (time.perf_counter() - t0) * (n / len(small))
    # compression: a sorted, low-cardinality column (the book id of each word)
    brow, wrow = _corpus()
    book = np.array([r[0] for r in wrow], dtype=np.int64)
    runs = int(1 + np.count_nonzero(np.diff(book)))
    words = [r[2] for r in wrow]
    vocab = {w: i for i, w in enumerate(sorted(set(words)))}
    raw_bytes = sum(len(w) + 1 for w in words)
    dict_bits = math.ceil(math.log2(len(vocab)))
    dict_bytes = len(words) * dict_bits / 8 + sum(len(w) + 1 for w in vocab)
    return {"n": n, "cols": cols, "row_s": t_row, "col_s": t_col, "tuple_s": t_tuple, "answer": v1,
            "bytes_row": n * cols * 8, "bytes_col": n * 2 * 8, "book_runs": runs, "book_rows": len(book),
            "rle_bytes": runs * 16, "plain_bytes": len(book) * 8, "vocab": len(vocab), "dict_bits": dict_bits,
            "raw_word_bytes": raw_bytes, "dict_word_bytes": dict_bytes}


# ---- frontier --------------------------------------------------------------------------------------------------------
def compute_frontier() -> dict:
    """Triangles in a graph: R(a, b) S(b, c) T(a, c) = the same edge list three times.  A binary join builds every
    path of two edges first; a worst-case optimal join intersects neighbour sets one variable at a time.  The AGM
    bound for three relations of N tuples is N^{3/2}."""
    rng = random.Random(5)
    out = []
    for n_hub, n_rand in ((1, 3000), (2, 6000), (4, 12000)):
        edges = set()
        hubs = list(range(n_hub))
        for h in hubs:                                  # stars: a few nodes joined to many
            for v in range(1000, 1000 + 1500):
                edges.add((h, v))
        nodes = 4000
        while len(edges) < n_hub * 1500 + n_rand:
            a, b = rng.randrange(nodes), rng.randrange(nodes)
            if a != b:
                edges.add((min(a, b), max(a, b)))
        E = sorted(edges)
        N = len(E)
        adj: dict = {}
        for a, b in E:
            adj.setdefault(a, set()).add(b)
            adj.setdefault(b, set()).add(a)
        # binary: (R join S on b) then filter by T
        by_first: dict = {}
        for a, b in E:
            by_first.setdefault(b, []).append(a)
            by_first.setdefault(a, []).append(b)
        paths = sum(len(v) * (len(v) - 1) // 2 for v in by_first.values())
        # worst-case optimal (generic join): for each edge (a, b), intersect the smaller neighbour set
        work = 0
        tri = 0
        for a, b in E:
            x, y = (adj[a], adj[b]) if len(adj[a]) < len(adj[b]) else (adj[b], adj[a])
            work += len(x)
            tri += sum(1 for c in x if c in y and c > b)
        out.append({"edges": N, "paths": paths, "wcoj_work": work, "agm": N ** 1.5, "triangles": tri,
                    "hubs": n_hub})
    return {"rows": out}


ITEMS = {k[8:]: v for k, v in globals().items() if k.startswith("compute_")}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
