"""A small relational database (Part 35): a catalog with statistics, a SQL subset, Volcano iterators, and a
Selinger-style optimizer.

    db = Database(page_rows=100, buffer_pages=50)
    db.create("words", ["book", "pos", "word"], rows)
    db.index("words", "word")                       # a B+ tree (explainer.cs.db.bptree)
    plan = db.plan("SELECT word, COUNT(*) FROM words GROUP BY word ORDER BY 2 DESC LIMIT 20")
    print(db.explain(plan)); rows = db.run(plan)

**SQL.**  ``SELECT`` items (columns, ``t.col``, ``COUNT(*)``, ``SUM``/``MIN``/``MAX``, ``AS``) ``FROM`` tables with
aliases and ``JOIN ... ON a = b``, ``WHERE`` a conjunction of comparisons, ``GROUP BY``, ``ORDER BY`` (a name or
a position, ``DESC``), ``LIMIT``.

**Costs** are in page I/Os, with ``page_rows`` tuples to a page and ``buffer_pages`` pages of memory, as in the
textbooks (Ramakrishnan and Gehrke): a scan costs its pages; block nested loops M + ceil(M / (B - 2)) N; Grace hash
3 (M + N); sort-merge the two external sorts plus M + N; an index nested-loop join one probe of the index per outer
tuple.  Cardinalities are estimated as System R did: equality selects 1 / NDV, ranges from an equi-depth histogram,
conjunctions multiply (independence), and an equi-join keeps |R| |S| / max(NDV).

**The optimizer** is Selinger's dynamic program (1979) over left-deep join orders: the best plan for every subset of
the tables, built from the best plans of smaller subsets, keeping one plan per *interesting order*; ``exhaustive``
enumerates every left-deep order for comparison.

**Execution** is the Volcano model (Graefe 1994): each operator is an iterator pulling tuples from its children;
``run`` returns the rows and fills ``stats`` with tuples produced per operator and pages read.
"""
from __future__ import annotations

import heapq
import itertools
import math
import re
from dataclasses import dataclass, field

from explainer.cs.db.rel import Relation


# ---- the catalog ------------------------------------------------------------------------------------------------
@dataclass
class Table:
    name: str
    cols: tuple[str, ...]
    rows: list[tuple]
    ndv: dict = field(default_factory=dict)
    hist: dict = field(default_factory=dict)
    indexes: dict = field(default_factory=dict)        # column -> BPlusTree of (value -> row ids)


class Database:
    def __init__(self, page_rows: int = 100, buffer_pages: int = 50, hist_buckets: int = 20):
        self.page_rows, self.B, self.nb = page_rows, buffer_pages, hist_buckets
        self.tables: dict[str, Table] = {}

    def create(self, name: str, cols, rows) -> Table:
        t = Table(name, tuple(cols), [tuple(r) for r in rows])
        self.tables[name] = t
        self.analyze(name)
        return t

    def analyze(self, name: str) -> None:
        """Statistics: distinct values per column, and an equi-depth histogram for each numeric column."""
        t = self.tables[name]
        for i, c in enumerate(t.cols):
            vals = [r[i] for r in t.rows]
            t.ndv[c] = len(set(vals)) or 1
            if vals and all(isinstance(v, (int, float)) for v in vals[:1000]):
                s = sorted(vals)
                t.hist[c] = [s[min(len(s) - 1, (k * len(s)) // self.nb)] for k in range(self.nb + 1)]

    def index(self, name: str, col: str) -> None:
        from explainer.cs.db.bptree import BPlusTree
        t = self.tables[name]
        i = t.cols.index(col)
        bt = BPlusTree(order=64)
        groups: dict = {}
        for rid, r in enumerate(t.rows):
            groups.setdefault(r[i], []).append(rid)
        for k in sorted(groups, key=_sortkey):
            bt.insert(k, groups[k])
        t.indexes[col] = bt

    def pages(self, n: float) -> float:
        return max(1.0, math.ceil(n / self.page_rows))

    # -- parsing, planning, running ---------------------------------------------------------------------------
    def plan(self, sql: str, exhaustive: bool = False, force: dict | None = None):
        q = parse(sql)
        return plan_query(self, q, exhaustive=exhaustive, force=force or {})

    def run(self, plan, stats: dict | None = None) -> list[tuple]:
        stats = {} if stats is None else stats
        return list(plan.iterate(self, stats))

    def query(self, sql: str, stats: dict | None = None) -> list[tuple]:
        return self.run(self.plan(sql), stats)

    def explain(self, plan, depth: int = 0) -> str:
        line = "  " * depth + f"{plan.label()}   (rows ~{plan.rows:,.0f}, cost ~{plan.cost:,.0f} pages)"
        return "\n".join([line] + [self.explain(c, depth + 1) for c in plan.children()])


def _sortkey(v):
    return (0, v) if isinstance(v, (int, float)) else (1, str(v))


# ---- SQL --------------------------------------------------------------------------------------------------------
TOK = re.compile(r"\s*(?:(\d+\.\d+|\d+)|('(?:[^']|'')*')|([A-Za-z_][A-Za-z_0-9]*(?:\.[A-Za-z_][A-Za-z_0-9]*)?|\*)|"
                 r"(<=|>=|<>|!=|[=<>(),]))")
KW = {"SELECT", "FROM", "WHERE", "GROUP", "BY", "ORDER", "LIMIT", "JOIN", "ON", "AND", "AS", "DESC", "ASC"}


def tokenize(s: str) -> list:
    out, pos = [], 0
    s = s.strip().rstrip(";")
    while pos < len(s):
        m = TOK.match(s, pos)
        if not m or m.end() == pos:
            raise SyntaxError(f"at {s[pos:pos + 20]!r}")
        num, st, word, op = m.groups()
        if num is not None:
            out.append(("num", float(num) if "." in num else int(num)))
        elif st is not None:
            out.append(("str", st[1:-1].replace("''", "'")))
        elif word is not None:
            out.append(("kw", word.upper()) if word.upper() in KW else ("id", word))
        else:
            out.append(("op", op))
        pos = m.end()
    return out


@dataclass
class Query:
    select: list                 # [(kind, arg, alias)]: ("col", name) or ("agg", (fn, col or "*"))
    tables: list                 # [(table, alias)]
    joins: list                  # [(left col, right col)] from ON clauses
    where: list                  # [(left, op, right)]: names or ("lit", value)
    group: list
    order: list                  # [(item, desc)]: a name or a 1-based position
    limit: int | None


def parse(sql: str) -> Query:
    toks = tokenize(sql)
    i = 0

    def peek(k=0):
        return toks[i + k] if i + k < len(toks) else (None, None)

    def take(kind=None, val=None):
        nonlocal i
        t = peek()
        if kind and t[0] != kind or val and t[1] != val:
            raise SyntaxError(f"expected {val or kind}, got {t}")
        i += 1
        return t
    take("kw", "SELECT")
    sel = []
    while True:
        t = peek()
        if t[0] == "id" and t[1].upper() in ("COUNT", "SUM", "MIN", "MAX") and peek(1) == ("op", "("):
            fn = take()[1].lower()
            take("op", "(")
            arg = take()[1]
            take("op", ")")
            item = ("agg", (fn, arg))
        else:
            item = ("col", take()[1])
        alias = None
        if peek() == ("kw", "AS"):
            take()
            alias = take("id")[1]
        sel.append((item[0], item[1], alias))
        if peek() == ("op", ","):
            take()
            continue
        break
    take("kw", "FROM")
    tables, joins = [], []

    def tref():
        name = take("id")[1]
        alias = name
        if peek()[0] == "id":
            alias = take()[1]
        elif peek() == ("kw", "AS"):
            take()
            alias = take("id")[1]
        return name, alias
    tables.append(tref())
    while peek() == ("kw", "JOIN") or peek() == ("op", ","):
        take()
        tables.append(tref())
        if peek() == ("kw", "ON"):
            take()
            a = take("id")[1]
            take("op", "=")
            b = take("id")[1]
            joins.append((a, b))
    where = []
    if peek() == ("kw", "WHERE"):
        take()
        while True:
            a = take()
            op = take("op")[1]
            b = take()
            L = a[1] if a[0] == "id" else ("lit", a[1])
            R = b[1] if b[0] == "id" else ("lit", b[1])
            if isinstance(L, str) and isinstance(R, str) and op == "=":
                joins.append((L, R))
            else:
                where.append((L, op, R))
            if peek() == ("kw", "AND"):
                take()
                continue
            break
    group = []
    if peek() == ("kw", "GROUP"):
        take()
        take("kw", "BY")
        while True:
            group.append(take("id")[1])
            if peek() == ("op", ","):
                take()
                continue
            break
    order = []
    if peek() == ("kw", "ORDER"):
        take()
        take("kw", "BY")
        while True:
            t = take()
            desc = False
            if peek()[0] == "kw" and peek()[1] in ("DESC", "ASC"):
                desc = take()[1] == "DESC"
            order.append((t[1], desc))
            if peek() == ("op", ","):
                take()
                continue
            break
    limit = None
    if peek() == ("kw", "LIMIT"):
        take()
        limit = take("num")[1]
    if i != len(toks):
        raise SyntaxError(f"unexpected {toks[i]}")
    return Query(sel, tables, joins, where, group, order, limit)


# ---- plans ------------------------------------------------------------------------------------------------------
OPS = {"=": lambda a, b: a == b, "<": lambda a, b: a < b, ">": lambda a, b: a > b, "<=": lambda a, b: a <= b,
       ">=": lambda a, b: a >= b, "<>": lambda a, b: a != b, "!=": lambda a, b: a != b}


class Plan:
    rows: float = 0.0
    cost: float = 0.0
    cols: tuple = ()
    order: str | None = None          # the column the output is sorted by, if any

    def children(self):
        return []

    def label(self):
        return type(self).__name__

    def pos(self, name: str) -> int:
        if name in self.cols:
            return self.cols.index(name)
        hits = [k for k, c in enumerate(self.cols) if c.split(".")[-1] == name.split(".")[-1]]
        if len(hits) == 1:
            return hits[0]
        raise KeyError(f"{name} in {self.cols}")

    def count(self, stats, n=1):
        k = self.label().split("(")[0].strip()
        stats[k] = stats.get(k, 0) + n


class Scan(Plan):
    def __init__(self, db, t: Table, alias: str, preds):
        self.t, self.alias, self.preds = t, alias, preds
        self.cols = tuple(f"{alias}.{c}" for c in t.cols)
        sel = 1.0
        for p in preds:
            sel *= selectivity(t, p)
        self.rows = max(1.0, len(t.rows) * sel)
        self.cost = db.pages(len(t.rows))

    def label(self):
        w = " and ".join(_pstr(p) for p in self.preds)
        return f"Scan {self.t.name}" + (f" where {w}" if w else "")

    def iterate(self, db, stats):
        fs = _compile(self.preds, self.t.cols)
        stats["pages"] = stats.get("pages", 0) + db.pages(len(self.t.rows))
        for r in self.t.rows:
            if fs(r):
                self.count(stats)
                yield r


class IndexScan(Plan):
    """Equality on an indexed column: the B+ tree's levels, then the matching rows (unclustered: a page each)."""

    def __init__(self, db, t: Table, alias: str, col: str, value, preds):
        self.t, self.alias, self.col, self.value, self.preds = t, alias, col, value, preds
        self.cols = tuple(f"{alias}.{c}" for c in t.cols)
        sel = 1.0 / t.ndv[col]
        for p in preds:
            sel *= selectivity(t, p)
        self.rows = max(1.0, len(t.rows) * sel)
        match = len(t.rows) / t.ndv[col]
        self.cost = t.indexes[col].height() + match

    def label(self):
        return f"IndexScan {self.t.name}.{self.col} = {self.value!r}"

    def iterate(self, db, stats):
        bt = self.t.indexes[self.col]
        rids = bt.search(self.value) or []
        stats["pages"] = stats.get("pages", 0) + bt.height() + len(rids)
        fs = _compile(self.preds, self.t.cols)
        for rid in rids:
            r = self.t.rows[rid]
            if fs(r):
                self.count(stats)
                yield r


class Join(Plan):
    def __init__(self, db, left: Plan, right: Plan, on: list, method: str):
        self.l, self.r, self.on, self.method = left, right, on, method
        self.cols = left.cols + right.cols
        self.rows = join_card(left, right, on)
        M, N, B = db.pages(left.rows), db.pages(right.rows), db.B
        if method == "nested loops":                  # read the inner once, then rescan it per block of the outer
            self.cost = left.cost + right.cost + max(0, math.ceil(M / max(1, B - 2)) - 1) * N
        elif method == "hash":
            self.cost = left.cost + right.cost + 2 * (M + N) if max(M, N) > B else left.cost + right.cost
        elif method == "sort-merge":
            self.cost = left.cost + right.cost + sort_cost(M, B) + sort_cost(N, B)
            self.order = on[0][0] if on else None
        elif method == "index nested loops":
            self.cost = left.cost + left.rows * (right.t.indexes[_bare(on[0][1])].height() + 1)
        else:
            raise ValueError(method)

    def children(self):
        return [self.l, self.r]

    def label(self):
        cond = " and ".join(f"{a} = {b}" for a, b in self.on)
        return f"{self.method.capitalize()} join on {cond}"

    def iterate(self, db, stats):
        li = [self.l.pos(a) for a, _ in self.on]
        ri = [self.r.pos(b) for _, b in self.on]
        if self.method == "index nested loops":
            t = self.r.t
            bt = t.indexes[_bare(self.on[0][1])]
            fs = _compile(self.r.preds, t.cols)
            for lr in self.l.iterate(db, stats):
                rids = bt.search(lr[li[0]]) or []
                stats["pages"] = stats.get("pages", 0) + bt.height() + len(rids)
                for rid in rids:
                    rr = t.rows[rid]
                    if fs(rr) and all(lr[a] == rr[b] for a, b in zip(li, ri)):
                        self.count(stats)
                        yield lr + rr
            return
        if self.method == "nested loops":
            inner = list(self.r.iterate(db, stats))
            for lr in self.l.iterate(db, stats):
                for rr in inner:
                    if all(lr[a] == rr[b] for a, b in zip(li, ri)):
                        self.count(stats)
                        yield lr + rr
            return
        if self.method == "sort-merge":
            L = sorted(self.l.iterate(db, stats), key=lambda r: tuple(_sortkey(r[a]) for a in li))
            R = sorted(self.r.iterate(db, stats), key=lambda r: tuple(_sortkey(r[b]) for b in ri))
            j = 0
            for lr in L:
                k = tuple(_sortkey(lr[a]) for a in li)
                while j < len(R) and tuple(_sortkey(R[j][b]) for b in ri) < k:
                    j += 1
                jj = j
                while jj < len(R) and tuple(_sortkey(R[jj][b]) for b in ri) == k:
                    self.count(stats)
                    yield lr + R[jj]
                    jj += 1
            return
        h: dict = {}
        for rr in self.r.iterate(db, stats):
            h.setdefault(tuple(rr[b] for b in ri), []).append(rr)
        for lr in self.l.iterate(db, stats):
            for rr in h.get(tuple(lr[a] for a in li), ()):
                self.count(stats)
                yield lr + rr


class Filter(Plan):
    def __init__(self, child: Plan, preds):
        self.c, self.preds = child, preds
        self.cols, self.order = child.cols, child.order
        self.rows = max(1.0, child.rows * 0.3 ** len(preds))
        self.cost = child.cost

    def children(self):
        return [self.c]

    def label(self):
        return "Filter " + " and ".join(_pstr(p) for p in self.preds)

    def iterate(self, db, stats):
        idx = []
        for L, op, R in self.preds:
            idx.append((self.c.pos(L) if isinstance(L, str) else None, L, OPS[op],
                        self.c.pos(R) if isinstance(R, str) else None, R))
        for r in self.c.iterate(db, stats):
            ok = True
            for li, L, f, ri, R in idx:
                a = r[li] if li is not None else L[1]
                b = r[ri] if ri is not None else R[1]
                if not f(a, b):
                    ok = False
                    break
            if ok:
                self.count(stats)
                yield r


class Aggregate(Plan):
    """GROUP BY with aggregates, by hashing (one pass, memory for the groups) or over sorted input (streaming)."""

    def __init__(self, db, child: Plan, keys, aggs, method: str, ngroups: float):
        self.c, self.keys, self.aggs, self.method = child, keys, aggs, method
        self.cols = tuple(keys) + tuple(f"{fn}({a})" for fn, a in aggs)
        self.rows = ngroups
        M = db.pages(child.rows)
        if method == "hash":
            self.cost = child.cost + (0 if db.pages(ngroups) <= db.B else 2 * M)
        else:
            self.cost = child.cost + (0 if child.order == keys[0] else sort_cost(M, db.B))
            self.order = keys[0] if keys else None

    def children(self):
        return [self.c]

    def label(self):
        return f"{'Hash' if self.method == 'hash' else 'Sort'} aggregate by {', '.join(self.keys)}"

    def iterate(self, db, stats):
        ki = [self.c.pos(k) for k in self.keys]
        ai = [(fn, None if a == "*" else self.c.pos(a)) for fn, a in self.aggs]

        def fold(acc, r):
            for j, (fn, x) in enumerate(ai):
                v = 1 if fn == "count" else r[x]
                if acc[j] is None:
                    acc[j] = v
                elif fn in ("count", "sum"):
                    acc[j] += v
                elif fn == "min":
                    acc[j] = min(acc[j], v)
                else:
                    acc[j] = max(acc[j], v)
        if self.method == "hash":
            groups: dict = {}
            for r in self.c.iterate(db, stats):
                k = tuple(r[i] for i in ki)
                acc = groups.get(k)
                if acc is None:
                    acc = groups[k] = [None] * len(ai)
                fold(acc, r)
            for k, acc in groups.items():
                self.count(stats)
                yield k + tuple(acc)
            return
        rows = self.c.iterate(db, stats)
        if self.c.order != (self.keys[0] if self.keys else None):
            rows = iter(sorted(rows, key=lambda r: tuple(_sortkey(r[i]) for i in ki)))
        cur, acc = None, None
        for r in rows:
            k = tuple(r[i] for i in ki)
            if k != cur:
                if cur is not None:
                    self.count(stats)
                    yield cur + tuple(acc)
                cur, acc = k, [None] * len(ai)
            fold(acc, r)
        if cur is not None:
            self.count(stats)
            yield cur + tuple(acc)


class Project(Plan):
    def __init__(self, child: Plan, items):
        self.c, self.items = child, items
        self.cols = tuple(a or n for n, a in items)
        self.rows, self.cost, self.order = child.rows, child.cost, child.order

    def children(self):
        return [self.c]

    def label(self):
        return "Project " + ", ".join(a or n for n, a in self.items)

    def iterate(self, db, stats):
        ix = [self.c.pos(n) for n, _ in self.items]
        for r in self.c.iterate(db, stats):
            yield tuple(r[i] for i in ix)


class Sort(Plan):
    def __init__(self, db, child: Plan, keys, limit=None):
        self.c, self.keys, self.limit = child, keys, limit
        self.cols = child.cols
        self.rows = min(child.rows, limit) if limit else child.rows
        M = db.pages(child.rows)
        self.cost = child.cost + (0 if limit and limit <= db.B * db.page_rows else sort_cost(M, db.B))

    def children(self):
        return [self.c]

    def label(self):
        ks = ", ".join(f"{k}{' desc' if d else ''}" for k, d in self.keys)
        return (f"Top {self.limit} by {ks} (a heap)" if self.limit else f"Sort by {ks}")

    def iterate(self, db, stats):
        ki = [(self.c.pos(k) if isinstance(k, str) else k - 1, d) for k, d in self.keys]

        def key(r):
            return tuple((-r[i] if d else r[i]) if isinstance(r[i], (int, float)) else _sortkey(r[i]) for i, d in ki)
        rows = self.c.iterate(db, stats)
        out = heapq.nsmallest(self.limit, rows, key=key) if self.limit else sorted(rows, key=key)
        for r in out:
            self.count(stats)
            yield r


# ---- estimation -----------------------------------------------------------------------------------------------
def _bare(c: str) -> str:
    return c.split(".")[-1]


def _pstr(p) -> str:
    L, op, R = p
    f = (lambda x: repr(x[1]) if isinstance(x, tuple) else x)
    return f"{f(L)} {op} {f(R)}"


def _compile(preds, cols):
    if not preds:
        return lambda r: True
    tests = []
    for L, op, R in preds:
        li = cols.index(_bare(L)) if isinstance(L, str) else None
        ri = cols.index(_bare(R)) if isinstance(R, str) else None
        tests.append((li, L, OPS[op], ri, R))

    def f(r):
        for li, L, g, ri, R in tests:
            if not g(r[li] if li is not None else L[1], r[ri] if ri is not None else R[1]):
                return False
        return True
    return f


def selectivity(t: Table, p) -> float:
    L, op, R = p
    col = _bare(L) if isinstance(L, str) else _bare(R)
    v = R[1] if isinstance(R, tuple) else (L[1] if isinstance(L, tuple) else None)
    if op == "=":
        return 1.0 / t.ndv.get(col, 10)
    if op in ("<>", "!="):
        return 1 - 1.0 / t.ndv.get(col, 10)
    h = t.hist.get(col)
    if h is None or v is None:
        return 1 / 3
    below = sum(1 for b in h[1:] if b <= v) / (len(h) - 1)
    return max(1e-6, below if op in ("<", "<=") else 1 - below)


def join_card(l: Plan, r: Plan, on) -> float:
    if not on:
        return l.rows * r.rows
    n = l.rows * r.rows
    for a, b in on:
        n /= max(_ndv(l, a), _ndv(r, b))
    return max(1.0, n)


def _ndv(p: Plan, col: str) -> float:
    for s in _scans(p):
        if col.split(".")[0] == s.alias or col in s.cols:
            return min(s.rows, s.t.ndv.get(_bare(col), 10))
    return 10.0


def _scans(p: Plan):
    if isinstance(p, (Scan, IndexScan)):
        yield p
    for c in p.children():
        yield from _scans(c)


def sort_cost(M: float, B: int) -> float:
    """External merge sort: 2M per pass; passes 1 + ceil(log_{B-1} ceil(M / B))."""
    if M <= B:
        return 0.0
    runs = math.ceil(M / B)
    passes = 1 + math.ceil(math.log(runs, B - 1)) if runs > 1 else 1
    return 2 * M * passes


# ---- planning and the optimizer -----------------------------------------------------------------------------------
def plan_query(db: Database, q: Query, exhaustive: bool = False, force: dict | None = None) -> Plan:
    force = force or {}
    aliases = {a: db.tables[t] for t, a in q.tables}

    def owner(col):
        if "." in col:
            return col.split(".")[0]
        hits = [a for a, t in aliases.items() if col in t.cols]
        if len(hits) != 1:
            raise KeyError(f"column {col} is ambiguous or unknown")
        return hits[0]

    def qual(col):
        return col if "." in col else f"{owner(col)}.{col}"
    local = {a: [] for a in aliases}
    for L, op, R in q.where:
        side = L if isinstance(L, str) else R
        local[owner(side)].append((L, op, R))
    edges = [(qual(a), qual(b)) for a, b in q.joins]

    def access(a):
        t = aliases[a]
        eq = [p for p in local[a] if p[1] == "=" and isinstance(p[2], tuple) and _bare(p[0]) in t.indexes]
        options = [Scan(db, t, a, local[a])]
        if eq:
            p = eq[0]
            rest = [x for x in local[a] if x is not p]
            options.append(IndexScan(db, t, a, _bare(p[0]), p[2][1], rest))
        if "access" in force:
            options = [o for o in options if type(o).__name__ == force["access"]] or options
        return min(options, key=lambda o: o.cost)

    def joins_between(left_set, a):
        on = []
        for x, y in edges:
            if x.split(".")[0] in left_set and y.split(".")[0] == a:
                on.append((x, y))
            elif y.split(".")[0] in left_set and x.split(".")[0] == a:
                on.append((y, x))
        return on

    def extend(left: Plan, left_set, a):
        on = joins_between(left_set, a)
        right = access(a)
        methods = ["nested loops", "hash", "sort-merge"] if on else ["nested loops"]
        t = aliases[a]
        if on and _bare(on[0][1]) in t.indexes:
            methods.append("index nested loops")
        if "join" in force:
            methods = [m for m in methods if m == force["join"]] or methods
        out = []
        for m in methods:
            r = Scan(db, t, a, local[a]) if m == "index nested loops" else right
            out.append(Join(db, left, r, on, m))
        return out
    names = list(aliases)
    db.considered = 0
    if exhaustive or len(names) == 1:
        best = None
        for perm in itertools.permutations(names):
            p = access(perm[0])
            seen = {perm[0]}
            ok = True
            for a in perm[1:]:
                cands = extend(p, seen, a)
                db.considered += len(cands)
                p = min(cands, key=lambda c: c.cost)
                seen.add(a)
                if not joins_between(seen - {a}, a):
                    ok = ok and len(names) <= 3
            if best is None or p.cost < best.cost:
                best = p
        root = best
    else:
        # Selinger: best[(subset, order)] built from smaller subsets
        best: dict = {}
        for a in names:
            p = access(a)
            best[(frozenset([a]), p.order)] = p
        for k in range(2, len(names) + 1):
            for subset in itertools.combinations(names, k):
                S = frozenset(subset)
                for a in subset:
                    rest = S - {a}
                    for (s, o), lp in list(best.items()):
                        if s != rest:
                            continue
                        if not joins_between(rest, a) and any(joins_between(rest, b) for b in S - rest):
                            continue                     # avoid Cartesian products while a join exists
                        for c in extend(lp, rest, a):
                            db.considered += 1
                            key = (S, c.order)
                            if key not in best or c.cost < best[key].cost:
                                best[key] = c
        full = frozenset(names)
        root = min((p for (s, o), p in best.items() if s == full), key=lambda p: p.cost)
    # grouping, ordering, projection
    sel_cols = [(item[1] if item[0] == "col" else None) for item in q.select]
    aggs = [item[1] for item in q.select if item[0] == "agg"]
    if q.group or aggs:
        keys = [qual(g) for g in q.group]
        ng = 1.0
        for g in keys:
            ng *= aliases[owner(g)].ndv.get(_bare(g), 10)
        ng = min(ng, root.rows)
        aggq = [(fn, "*" if a == "*" else qual(a)) for fn, a in aggs]
        methods = ["hash", "sort"]
        if "agg" in force:
            methods = [force["agg"]]
        root = min((Aggregate(db, root, keys, aggq, m, ng) for m in methods), key=lambda p: p.cost)
        names_out = []
        for item in q.select:
            if item[0] == "col":
                names_out.append((qual(item[1]), item[2] or _bare(item[1])))
            else:
                fn, a = item[1]
                names_out.append((f"{fn}({'*' if a == '*' else qual(a)})", item[2] or f"{fn.upper()}({a})"))
    else:
        names_out = [(qual(c), _bare(c)) for c in sel_cols if c != "*"] if sel_cols != ["*"] else \
            [(c, c) for c in root.cols]
    if q.order:
        keys = []
        for item, desc in q.order:
            if isinstance(item, int):
                keys.append((names_out[item - 1][0], desc))
            else:
                hit = [n for n, a in names_out if a == item or _bare(n) == item]
                keys.append((hit[0] if hit else qual(item), desc))
        root = Sort(db, root, keys, q.limit)
    root = Project(root, names_out)
    if q.limit and not q.order:
        root.limit = q.limit
    return root


def count_plans(n: int) -> dict:
    """Join orders of n tables: left-deep n!, all binary trees n! C(n-1) (Catalan), Selinger's subsets 2^n."""
    cat = math.comb(2 * (n - 1), n - 1) // n
    return {"n": n, "left_deep": math.factorial(n), "bushy": math.factorial(n) * cat, "subsets": 2 ** n}


def to_relation(plan: Plan, rows) -> Relation:
    return Relation(plan.cols, list(rows))
