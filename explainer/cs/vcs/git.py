"""A small git (Part 41): content-addressed objects in git's own formats, a history DAG with merge bases, three-way
merge over Myers' diff, and bisection.  Object ids are checked against the real git in the tests."""

from __future__ import annotations

import hashlib
import random
import zlib
from collections import deque


# ---------------------------------------------------------------- objects

def obj_id(kind: str, data: bytes) -> str:
    """git's object id: SHA-1 of "<kind> <size>\\0" followed by the content."""
    return hashlib.sha1(f"{kind} {len(data)}".encode() + b"\0" + data).hexdigest()


class Store:
    """An object database: id -> (kind, content), stored zlib-compressed as git does on disk."""

    def __init__(self):
        self.objects: dict = {}

    def put(self, kind: str, data: bytes) -> str:
        oid = obj_id(kind, data)
        self.objects[oid] = zlib.compress(f"{kind} {len(data)}".encode() + b"\0" + data)
        return oid

    def get(self, oid: str):
        raw = zlib.decompress(self.objects[oid])
        head, _, data = raw.partition(b"\0")
        kind, size = head.decode().split()
        assert int(size) == len(data) and obj_id(kind, data) == oid, "corrupt object"
        return kind, data

    def blob(self, text: bytes) -> str:
        return self.put("blob", text)

    def tree(self, entries) -> str:
        """``entries``: (mode, name, oid), mode "100644" for files and "40000" for subtrees; sorted as git sorts
        (directories compare as if their name ended in "/")."""
        def key(e):
            return e[1] + ("/" if e[0] == "40000" else "")
        data = b"".join(f"{m} {n}".encode() + b"\0" + bytes.fromhex(o) for m, n, o in sorted(entries, key=key))
        return self.put("tree", data)

    def commit(self, tree: str, parents, message: str, author="Ada <ada@example.com>", when=1_700_000_000,
               tz="+0000") -> str:
        lines = [f"tree {tree}"] + [f"parent {p}" for p in parents]
        lines += [f"author {author} {when} {tz}", f"committer {author} {when} {tz}", "", message]
        return self.put("commit", ("\n".join(lines) + "\n").encode())

    def write_files(self, files: dict) -> str:
        """Build blobs and nested trees for {path: bytes}; returns the root tree id."""
        dirs: dict = {}
        for path, data in files.items():
            parts = path.split("/")
            d = dirs
            for p in parts[:-1]:
                d = d.setdefault(p, {})
            d[parts[-1]] = data

        def build(d):
            ents = []
            for name, v in d.items():
                if isinstance(v, dict):
                    ents.append(("40000", name, build(v)))
                else:
                    ents.append(("100644", name, self.blob(v)))
            return self.tree(ents)
        return build(dirs)


def changed_ids(files_a: dict, files_b: dict):
    """Which object ids differ between two snapshots that differ in one file: the blob, every tree on its path,
    and the commit."""
    sa, sb = Store(), Store()
    ta, tb = sa.write_files(files_a), sb.write_files(files_b)
    return {"objects_a": len(sa.objects), "objects_b": len(sb.objects),
            "shared": len(set(sa.objects) & set(sb.objects)), "root_a": ta, "root_b": tb}


# ---------------------------------------------------------------- the history DAG

def random_history(commits: int = 60, branch_p: float = 0.25, merge_p: float = 0.2, seed: int = 0):
    """A random DAG of commits: each new commit extends a random live branch tip, sometimes starting a branch,
    sometimes merging two tips.  Returns parents: list of tuples (commit i's parents, all < i)."""
    rng = random.Random(seed)
    parents = [()]
    tips = [0]
    for i in range(1, commits):
        r = rng.random()
        if r < merge_p and len(tips) > 1:
            a, b = rng.sample(tips, 2)
            parents.append((a, b))
            tips.remove(a)
            tips.remove(b)
            tips.append(i)
        elif r < merge_p + branch_p:
            base = rng.randrange(i)
            parents.append((base,))
            tips.append(i)
        else:
            t = rng.choice(tips)
            parents.append((t,))
            tips.remove(t)
            tips.append(i)
    return parents


def ancestors(parents, c):
    seen, q = {c}, deque([c])
    while q:
        x = q.popleft()
        for p in parents[x]:
            if p not in seen:
                seen.add(p)
                q.append(p)
    return seen


def merge_bases(parents, a, b):
    """Best common ancestors: common ancestors that are not ancestors of another common ancestor (git merge-base
    --all).  There can be more than one."""
    common = ancestors(parents, a) & ancestors(parents, b)
    out = set(common)
    for c in common:
        out -= (ancestors(parents, c) - {c})
    return sorted(out)


def criss_cross():
    """The classic history with two merge bases: two branches that each merged the other."""
    #   0 - 1 - 3 - 5
    #    \    X
    #     2 - 4 - 6
    return [(), (0,), (0,), (1, 2), (2, 1), (3,), (4,)]


def bisect(n: int, bad_from: int):
    """Binary search over a linear history of n commits where commit ``bad_from`` introduced a bug: returns the
    commits tested."""
    if n < 2 or not 1 <= bad_from < n:
        raise ValueError("bisect needs a known-good first commit and a later first bad commit")
    lo, hi = 0, n - 1            # lo known good, hi known bad
    tested = []
    while hi - lo > 1:
        mid = (lo + hi) // 2
        tested.append(mid)
        if mid >= bad_from:
            hi = mid
        else:
            lo = mid
    return {"first_bad": hi, "tested": tested, "steps": len(tested)}


# ---------------------------------------------------------------- three-way merge

def _matches(a, b):
    """Pairs (i, j) with a[i] == b[j] along a shortest edit script (Myers)."""
    from explainer.cs.algo.strings import myers
    _, script, _, _ = myers(a, b)
    i = j = 0
    out = []
    for op, _ in script:
        if op == "=":
            out.append((i, j))
            i += 1
            j += 1
        elif op == "-":
            i += 1
        else:
            j += 1
    return out


def merge3(base, ours, theirs):
    """diff3-style merge of lists of lines.  Regions where only one side changed take that side; where both
    changed identically take it; otherwise emit a conflict.  Returns (lines, conflicts) with conflict markers."""
    mo = dict(_matches(base, ours))
    mt = dict(_matches(base, theirs))
    # stable lines: base lines matched in both; they synchronize the three files
    sync = [(i, mo[i], mt[i]) for i in range(len(base)) if i in mo and i in mt]
    sync.append((len(base), len(ours), len(theirs)))
    out, conflicts = [], 0
    pb = po = pt = 0
    for ib, io, it in sync:
        b, o, t = base[pb:ib], ours[po:io], theirs[pt:it]
        if o == b:
            out += t
        elif t == b or o == t:
            out += o
        else:
            conflicts += 1
            out += ["<<<<<<< ours"] + o + ["======="] + t + [">>>>>>> theirs"]
        if ib < len(base):
            out.append(base[ib])
        pb, po, pt = ib + 1, io + 1, it + 1
    return out, conflicts


# ---------------------------------------------------------------- deltas on a real file's history

def delta_history(path: str, root=None, limit: int = 40):
    """Every committed version of ``path`` in this repository: its zlib size as a loose object, against the size
    of a line delta from the previous version (what a packfile stores instead)."""
    import difflib
    import subprocess
    from pathlib import Path
    root = Path(root) if root else Path(__file__).resolve().parents[3]
    revs = subprocess.run(["git", "-C", str(root), "log", "--format=%H", "--reverse", "--", path],
                          capture_output=True, text=True, check=True).stdout.split()[-limit:]
    rows, prev = [], None
    for r in revs:
        data = subprocess.run(["git", "-C", str(root), "show", f"{r}:{path}"], capture_output=True,
                              check=True).stdout
        loose = len(zlib.compress(b"blob " + str(len(data)).encode() + b"\0" + data))
        if prev is None:
            delta = loose
        else:
            a, b = prev.decode(errors="replace").splitlines(True), data.decode(errors="replace").splitlines(True)
            ops = "".join(f"{tag}{i1},{i2},{j1},{j2}\n" + ("".join(b[j1:j2]) if tag in ("replace", "insert") else "")
                          for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes()
                          if tag != "equal")
            delta = len(zlib.compress(ops.encode(errors="replace")))
        rows.append({"rev": r[:8], "bytes": len(data), "loose": loose, "delta": delta})
        prev = data
    return {"path": path, "versions": len(rows), "rows": rows, "loose_total": sum(r["loose"] for r in rows),
            "delta_total": sum(r["delta"] for r in rows)}


def corruption_demo():
    """Flip one bit in one stored object and ask for it back: the content no longer hashes to its name."""
    s = Store()
    oid = s.blob(b"The Job: count the words in thirty novels.\n")
    raw = bytearray(zlib.decompress(s.objects[oid]))
    raw[-5] ^= 0x01
    s.objects[oid] = zlib.compress(bytes(raw))
    try:
        s.get(oid)
        return {"detected": False}
    except AssertionError:
        head, _, data = bytes(raw).partition(b"\0")
        return {"detected": True, "name": oid, "rehash": obj_id("blob", data), "text": data.decode(errors="replace")}


def edit_graph(a: str = "ABCABBA", b: str = "CBABAC"):
    """Myers' example (1986): the shortest edit script between two strings, its length D and its path."""
    from explainer.cs.algo.strings import myers
    d, script, trace, snakes = myers(list(a), list(b))
    x = y = 0
    path = [(0, 0)]
    for op, _ in script:
        if op == "=":
            x, y = x + 1, y + 1
        elif op == "-":
            x += 1
        else:
            y += 1
        path.append((x, y))
    return {"a": a, "b": b, "D": d, "script": script, "path": path, "lcs": len(a) - sum(op == "-" for op, _ in script)}


def repo_sizes(root=None):
    """This repository: objects and bytes in its whole history, against the files of the current commit."""
    import subprocess
    from pathlib import Path
    root = Path(root) if root else Path(__file__).resolve().parents[3]

    def run(*a):
        return subprocess.run(["git", "-C", str(root), *a], capture_output=True, text=True, check=True).stdout
    objs = run("rev-list", "--objects", "--all").splitlines()
    sizes = run("cat-file", "--batch-check=%(objecttype) %(objectsize) %(objectsize:disk)", "--batch-all-objects")
    total = disk = 0
    kinds: dict = {}
    for ln in sizes.splitlines():
        k, sz, dk = ln.split()
        total += int(sz)
        disk += int(dk)
        kinds[k] = kinds.get(k, 0) + 1
    head_files = run("ls-tree", "-r", "-l", "HEAD").splitlines()
    head_bytes = sum(int(ln.split()[3]) for ln in head_files if ln.split()[3] != "-")
    commits = int(run("rev-list", "--count", "HEAD").strip())
    return {"reachable_objects": len(objs), "objects": sum(kinds.values()), "kinds": kinds,
            "uncompressed_bytes": total, "on_disk_bytes": disk, "head_files": len(head_files),
            "head_bytes": head_bytes, "commits": commits}
