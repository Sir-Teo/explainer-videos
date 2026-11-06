"""This repository, measured (Part 40): its Python import graph (cycles, layers, coupling, Martin's instability)
and its git history (churn and hot spots)."""

from __future__ import annotations

import ast
import subprocess
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PACKAGES = ("explainer", "videos", "tools", "tests")


def modules(root: Path = ROOT, packages=PACKAGES):
    """Dotted module name -> path, for every .py file under the given top-level directories."""
    out = {}
    for pkg in packages:
        for p in sorted((root / pkg).rglob("*.py")):
            if "__pycache__" in p.parts:
                continue
            rel = p.relative_to(root).with_suffix("")
            parts = list(rel.parts)
            if parts[-1] == "__init__":
                parts = parts[:-1]
            out[".".join(parts)] = p
    return out


def _resolve(name: str, mods: dict) -> str | None:
    while name:
        if name in mods:
            return name
        name = name.rpartition(".")[0]
    return None


def import_graph(root: Path = ROOT, packages=PACKAGES):
    """Edges a -> b when module a imports module b (internal modules only; relative imports resolved)."""
    mods = modules(root, packages)
    edges = defaultdict(set)
    lines = {}
    for m, p in mods.items():
        src = p.read_text(encoding="utf-8", errors="replace")
        lines[m] = src.count("\n") + 1
        try:
            tree = ast.parse(src)
        except SyntaxError:
            continue
        pkg = m if p.name == "__init__.py" else m.rpartition(".")[0]
        for node in ast.walk(tree):
            targets = []
            if isinstance(node, ast.Import):
                targets = [a.name for a in node.names]
            elif isinstance(node, ast.ImportFrom):
                base = node.module or ""
                if node.level:
                    up = pkg.split(".")
                    up = up[:len(up) - node.level + 1] if node.level > 1 else up
                    base = ".".join(up + ([base] if base else []))
                targets = [base] + [f"{base}.{a.name}" for a in node.names]
            for t in targets:
                r = _resolve(t, mods)
                if r and r != m:
                    edges[m].add(r)
    return {"modules": sorted(mods), "edges": {k: sorted(v) for k, v in edges.items()}, "lines": lines}


def sccs(nodes, edges):
    """Tarjan's strongly connected components (iterative)."""
    index, low, on, st, out = {}, {}, set(), [], []
    c = [0]
    for v0 in nodes:
        if v0 in index:
            continue
        work = [(v0, iter(edges.get(v0, ())))]
        index[v0] = low[v0] = c[0]
        c[0] += 1
        st.append(v0)
        on.add(v0)
        while work:
            v, it = work[-1]
            adv = False
            for w in it:
                if w not in index:
                    index[w] = low[w] = c[0]
                    c[0] += 1
                    st.append(w)
                    on.add(w)
                    work.append((w, iter(edges.get(w, ()))))
                    adv = True
                    break
                if w in on:
                    low[v] = min(low[v], index[w])
            if adv:
                continue
            work.pop()
            if work:
                low[work[-1][0]] = min(low[work[-1][0]], low[v])
            if low[v] == index[v]:
                comp = []
                while True:
                    w = st.pop()
                    on.discard(w)
                    comp.append(w)
                    if w == v:
                        break
                out.append(comp)
    return out


def layer_of(m: str) -> str:
    p = m.split(".")
    if p[0] == "explainer":
        return "explainer (library)"
    if p[0] == "videos":
        return "videos (scenes)"
    return p[0]


def metrics(g=None):
    """Coupling per module (afferent Ca, efferent Ce, instability I = Ce / (Ca + Ce)), cycles, edges between
    layers, and the most depended-upon modules."""
    g = g or import_graph()
    mods, edges = g["modules"], g["edges"]
    ca = Counter()
    for a, bs in edges.items():
        for b in bs:
            ca[b] += 1
    per = {}
    for m in mods:
        ce = len(edges.get(m, ()))
        per[m] = {"ca": ca[m], "ce": ce, "I": ce / (ca[m] + ce) if ca[m] + ce else 0.0, "lines": g["lines"].get(m, 0)}
    comps = [sorted(c) for c in sccs(mods, edges) if len(c) > 1]
    cross = Counter()
    for a, bs in edges.items():
        for b in bs:
            cross[(layer_of(a), layer_of(b))] += 1
    upward = sum(v for (a, b), v in cross.items() if a.startswith("explainer") and not b.startswith("explainer"))
    top = sorted(mods, key=lambda m: -ca[m])[:12]
    # dependencies between parts of the CS series: videos.cs.csN.* importing videos.cs.csM.*
    parts = Counter()
    for a, bs in edges.items():
        pa = a.split(".")
        if len(pa) < 3 or pa[:2] != ["videos", "cs"]:
            continue
        for b in bs:
            pb = b.split(".")
            if len(pb) >= 3 and pb[:2] == ["videos", "cs"] and pb[2] != pa[2]:
                parts[(pa[2], pb[2])] += 1
    return {"n_modules": len(mods), "n_edges": sum(len(v) for v in edges.values()),
            "lines": sum(g["lines"].values()), "cycles": comps, "cross": {f"{a} -> {b}": v for (a, b), v in
                                                                           sorted(cross.items())},
            "upward": upward, "top": [{"module": m, **per[m]} for m in top], "per": per,
            "part_edges": {f"{a}->{b}": v for (a, b), v in parts.items()}}


def git_history(root: Path = ROOT, limit: int | None = None):
    """Commits, and lines added and deleted per file, from ``git log --numstat``."""
    cmd = ["git", "-C", str(root), "log", "--numstat", "--format=@%H %ad", "--date=short"]
    out = subprocess.run(cmd, capture_output=True, text=True, check=True).stdout
    commits = []
    churn = Counter()
    touches = Counter()
    cur = None
    for ln in out.splitlines():
        if ln.startswith("@"):
            h, d = ln[1:].split()
            cur = {"hash": h, "date": d, "files": 0, "added": 0, "deleted": 0}
            commits.append(cur)
        elif ln.strip() and cur is not None:
            a, d, f = ln.split("\t", 2)
            if a == "-":
                continue
            cur["files"] += 1
            cur["added"] += int(a)
            cur["deleted"] += int(d)
            churn[f] += int(a) + int(d)
            touches[f] += 1
    return {"commits": len(commits), "first": commits[-1]["date"] if commits else None,
            "last": commits[0]["date"] if commits else None,
            "added": sum(c["added"] for c in commits), "deleted": sum(c["deleted"] for c in commits),
            "most_touched": touches.most_common(12), "most_churn": churn.most_common(12),
            "files_touched": len(touches)}


def co_change(root: Path = ROOT, max_files: int = 30, min_support: int = 4, exclude=("docs/", "media/", "renders/")):
    """Logical coupling (Gall, Hajek and Jazayeri 1998): pairs of files that change in the same commits.  Commits
    touching more than ``max_files`` files are skipped (bulk changes say little).  For each pair: support (commits
    changing both) and confidence (support over the commits changing the first)."""
    from itertools import combinations
    out = subprocess.run(["git", "-C", str(root), "log", "--name-only", "--format=tformat:COMMIT"], capture_output=True,
                         text=True, check=True).stdout
    commits, cur = [], []
    for ln in out.splitlines():
        if ln == "COMMIT":
            if cur:
                commits.append(cur)
            cur = []
        elif ln.strip() and not ln.startswith(exclude):
            cur.append(ln.strip())
    if cur:
        commits.append(cur)
    single = Counter()
    pairs = Counter()
    used = 0
    for files in commits:
        if len(files) > max_files:
            continue
        used += 1
        fs = sorted(set(files))
        single.update(fs)
        pairs.update(combinations(fs, 2))
    rows = []
    for (a, b), n in pairs.items():
        if n < min_support:
            continue
        rows.append({"a": a, "b": b, "support": n, "conf_ab": n / single[a], "conf_ba": n / single[b]})
    rows.sort(key=lambda r: (-r["support"], -max(r["conf_ab"], r["conf_ba"])))
    return {"commits": len(commits), "used": used, "pairs": rows[:40], "most_changed": single.most_common(12)}


def _ngram_entropy(train, test, n: int = 3, vocab_min: int = 2):
    """Cross-entropy in bits per token of a word n-gram model with interpolated Kneser-Ney-like absolute
    discounting (Chen and Goodman), trained on ``train`` and scored on ``test``; rare tokens become <unk>."""
    import math
    freq = Counter(train)
    keep = {w for w, c in freq.items() if c >= vocab_min}

    def norm(seq):
        return [w if w in keep else "<unk>" for w in seq]
    tr, te = norm(train), norm(test)
    V = len(keep) + 1
    counts = [Counter() for _ in range(n + 1)]
    ctx = [Counter() for _ in range(n + 1)]
    follow = [defaultdict(set) for _ in range(n + 1)]
    for k in range(1, n + 1):
        for i in range(len(tr) - k + 1):
            g = tuple(tr[i:i + k])
            counts[k][g] += 1
            ctx[k][g[:-1]] += 1
            follow[k][g[:-1]].add(g[-1])
    D = 0.75

    def p(w, h):
        if not h:
            return (counts[1][(w,)] + 1) / (len(tr) + V)
        k = len(h) + 1
        c = ctx[k].get(h, 0)
        lower = p(w, h[1:])
        if c == 0:
            return lower
        a = max(counts[k].get(h + (w,), 0) - D, 0) / c
        lam = D * len(follow[k][h]) / c
        return a + lam * lower
    bits = 0.0
    for i in range(n - 1, len(te)):
        bits -= math.log2(p(te[i], tuple(te[i - n + 1:i])))
    return bits / max(1, len(te) - n + 1)


def naturalness(root: Path = ROOT, tokens: int = 400_000, seed: int = 0):
    """Hindle et al. (2012) on this repository: a trigram model's cross-entropy on held-out Python code from
    ``explainer/`` against the same model on held-out English from the thirty novels."""
    import io
    import random
    import tokenize
    files = sorted((root / "explainer").rglob("*.py"))
    random.Random(seed).shuffle(files)
    code = []
    split = []
    for f in files:
        toks = []
        try:
            for t in tokenize.generate_tokens(io.StringIO(f.read_text(encoding="utf-8")).readline):
                if t.type in (tokenize.COMMENT, tokenize.NL, tokenize.ENCODING):
                    continue
                if t.type == tokenize.STRING:
                    toks.append("<str>")
                elif t.type == tokenize.NUMBER:
                    toks.append("<num>")
                elif t.type in (tokenize.NEWLINE, tokenize.INDENT, tokenize.DEDENT):
                    toks.append(tokenize.tok_name[t.type])
                elif t.string:
                    toks.append(t.string)
        except (tokenize.TokenError, IndentationError, SyntaxError):
            continue
        split.append(len(code))
        code += toks
        if len(code) > tokens:
            break
    cut = split[int(len(split) * 0.8)]
    from videos.cs.cs31.compute import _full_text
    import re
    words = re.findall(r"[a-z']+|[.,;:!?]", _full_text().decode("latin-1").lower())[:len(code)]
    wcut = int(len(words) * 0.8)
    return {"code_tokens": len(code), "english_tokens": len(words),
            "code_bits": _ngram_entropy(code[:cut], code[cut:]),
            "english_bits": _ngram_entropy(words[:wcut], words[wcut:]),
            "code_unigram_bits": _ngram_entropy(code[:cut], code[cut:], n=1),
            "english_unigram_bits": _ngram_entropy(words[:wcut], words[wcut:], n=1)}
