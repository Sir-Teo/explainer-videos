"""A build system, two ways (Part 41): make's timestamps against verifying traces of content hashes with early
cutoff (Mokhov, Mitchell and Peyton Jones, "Build systems à la carte", 2018), on a synthetic C-like project; and
parallel builds as work and span."""

from __future__ import annotations

import hashlib
import random


def _h(*parts) -> str:
    return hashlib.sha256("\x00".join(map(str, parts)).encode()).hexdigest()[:16]


class Project:
    """``n`` source files and ``h`` headers; each source includes a few headers.  A source has code and comments;
    compiling it depends only on its code and its headers' code (so a comment-only change compiles to an identical
    object).  Targets: one object per source, then a library linking all objects, then a test report."""

    def __init__(self, n: int = 200, headers: int = 20, includes: int = 3, seed: int = 0):
        rng = random.Random(seed)
        self.n, self.headers = n, headers
        self.files = {}
        for i in range(n):
            self.files[f"src{i}.c"] = {"code": f"code{i}", "comment": "", "mtime": 0.0}
        for j in range(headers):
            self.files[f"h{j}.h"] = {"code": f"hdr{j}", "comment": "", "mtime": 0.0}
        self.deps = {f"src{i}.o": [f"src{i}.c"] + [f"h{j}.h" for j in sorted(rng.sample(range(headers), includes))]
                     for i in range(n)}
        self.deps["lib.a"] = [f"src{i}.o" for i in range(n)]
        self.deps["tests.log"] = ["lib.a"]
        self.order = [f"src{i}.o" for i in range(n)] + ["lib.a", "tests.log"]
        self.clock = 1.0

    def value(self, name, built):
        """What a file or target contains, as a hash."""
        if name in self.files:
            f = self.files[name]
            return _h(f["code"], f["comment"])
        return built[name]["value"]

    def semantic(self, name, built):
        if name in self.files:
            return _h(self.files[name]["code"])
        return built[name]["value"]

    def run(self, target, built):
        """The recipe: an object depends on its sources' code; the library and report on their inputs."""
        ins = self.deps[target]
        return _h(target, *[self.semantic(x, built) for x in ins])

    # edits
    def touch(self, name):
        self.clock += 1
        self.files[name]["mtime"] = self.clock

    def edit_comment(self, name):
        self.files[name]["comment"] += "*"
        self.touch(name)

    def edit_code(self, name):
        self.files[name]["code"] += "+"
        self.touch(name)


def build_make(p: Project, built: dict):
    """make: rebuild a target when any input's modification time is newer than the target's."""
    ran = 0
    for t in p.order:
        ins = p.deps[t]
        mt = [p.files[x]["mtime"] if x in p.files else built[x]["mtime"] for x in ins]
        if t not in built or max(mt) > built[t]["mtime"]:
            p.clock += 1
            built[t] = {"value": p.run(t, built), "mtime": p.clock}
            ran += 1
    return ran


def build_traces(p: Project, built: dict, cutoff: bool = True):
    """Verifying traces: remember the hashes of each target's inputs when it was built; rebuild only when one of
    them differs now.  With early cutoff, a rebuilt target whose output hash did not change stops the wave."""
    ran = 0
    for t in p.order:
        ins = p.deps[t]
        now = [p.value(x, built) if cutoff else (p.value(x, built), built.get(x, {}).get("stamp")) for x in ins]
        if t not in built or built[t]["trace"] != now:
            old = built.get(t, {}).get("value")
            v = p.run(t, built)
            stamp = (built.get(t, {}).get("stamp", 0) + 1) if (not cutoff or v != old) else built[t]["stamp"]
            built[t] = {"value": v, "trace": now, "stamp": stamp}
            ran += 1
    return ran


def scenarios(n: int = 200, headers: int = 20, includes: int = 3, seed: int = 0):
    """Rebuild counts for make and for verifying traces, after: nothing; a comment in one source; a real change in
    one source; a real change in one header; touching every file (a fresh checkout); a comment in a header."""
    out = []
    for name, edit in (("nothing changed", lambda p: None),
                       ("a comment in one source", lambda p: p.edit_comment("src7.c")),
                       ("a real change in one source", lambda p: p.edit_code("src7.c")),
                       ("a real change in one header", lambda p: p.edit_code("h3.h")),
                       ("a comment in one header", lambda p: p.edit_comment("h3.h")),
                       ("every file touched \\ (fresh checkout)", lambda p: [p.touch(f) for f in list(p.files)])):
        row = {"edit": name}
        for tag, fn in (("make", build_make), ("traces", build_traces)):
            p = Project(n, headers, includes, seed)
            built: dict = {}
            fn(p, built)
            edit(p)
            row[tag] = fn(p, built)
        out.append(row)
    p = Project(n, headers, includes, seed)
    uses = sum(1 for t, ins in p.deps.items() if "h3.h" in ins)
    return {"rows": out, "targets": len(p.order), "sources": n, "headers": headers, "h3_users": uses}


def parallel_times(n: int = 200, compile_s: float = 1.0, link_s: float = 8.0, test_s: float = 20.0,
                   workers=(1, 2, 4, 8, 16, 32, 64, 128, 256), seed: int = 0):
    """Work and span of a clean build: n independent compiles of random length (mean ``compile_s``), then a link and
    a test run.  Greedy list scheduling on P workers; Brent's bound max(W/P, S) <= T_P <= W/P + S."""
    rng = random.Random(seed)
    comp = [rng.expovariate(1 / compile_s) for _ in range(n)]
    work = sum(comp) + link_s + test_s
    span = max(comp) + link_s + test_s
    rows = []
    for P in workers:
        free = [0.0] * P
        for c in sorted(comp, reverse=True):
            i = min(range(P), key=lambda k: free[k])
            free[i] += c
        T = max(free) + link_s + test_s
        rows.append({"workers": P, "time": T, "lower": max(work / P, span), "upper": work / P + span})
    return {"work": work, "span": span, "rows": rows}


def build_cached(p: Project, built: dict, cache: dict):
    """Constructive traces: like verifying traces, but outputs are also stored in a cache shared between machines,
    keyed by (target, hashes of inputs).  A task whose key is in the cache is downloaded instead of run."""
    ran = fetched = 0
    for t in p.order:
        ins = p.deps[t]
        key = (t, tuple(p.value(x, built) for x in ins))
        if t in built and built[t]["key"] == key:
            continue
        if key in cache:
            built[t] = {"value": cache[key], "key": key}
            fetched += 1
        else:
            v = p.run(t, built)
            cache[key] = v
            built[t] = {"value": v, "key": key}
            ran += 1
    return ran, fetched


def shared_cache_story(n: int = 200, headers: int = 20, includes: int = 3, seed: int = 0):
    """Machine A builds; machine B builds the same commit; A edits a header and builds; B pulls that commit and
    builds.  Tasks run and downloaded at each step."""
    cache: dict = {}
    pa, pb = Project(n, headers, includes, seed), Project(n, headers, includes, seed)
    ba, bb = {}, {}
    rows = []
    r = build_cached(pa, ba, cache)
    rows.append({"step": "machine A: clean build", "ran": r[0], "fetched": r[1]})
    r = build_cached(pb, bb, cache)
    rows.append({"step": "machine B: same commit", "ran": r[0], "fetched": r[1]})
    pa.edit_code("h3.h")
    r = build_cached(pa, ba, cache)
    rows.append({"step": "A changes a header", "ran": r[0], "fetched": r[1]})
    pb.edit_code("h3.h")
    r = build_cached(pb, bb, cache)
    rows.append({"step": "B pulls A's change", "ran": r[0], "fetched": r[1]})
    return {"rows": rows, "cache_entries": len(cache), "targets": len(pa.order)}


def small_graph_rebuild(sources: int = 12, headers: int = 4, includes: int = 2, seed: int = 4,
                        changed: str = "h1.h"):
    """A project small enough to draw: its graph, and which targets a change to one header forces to rebuild."""
    p = Project(sources, headers, includes, seed)
    built: dict = {}
    build_traces(p, built)
    before = {t: built[t]["value"] for t in p.order}
    p.edit_code(changed)
    rebuilt = []
    for t in p.order:
        ins = p.deps[t]
        now = [p.value(x, built) for x in ins]
        if built[t]["trace"] != now:
            v = p.run(t, built)
            built[t] = {"value": v, "trace": now, "stamp": 0}
            rebuilt.append(t)
    return {"deps": p.deps, "order": p.order, "headers": [f"h{j}.h" for j in range(headers)],
            "sources": [f"src{i}.c" for i in range(sources)], "changed": changed, "rebuilt": rebuilt,
            "unchanged_outputs": [t for t in rebuilt if built[t]["value"] == before[t]]}
