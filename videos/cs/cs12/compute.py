"""Precompute everything numerical in Part 12 of *Computer Science, Built* ("Languages and Automata").

    python -m videos.cs.cs12.compute              # everything missing
    python -m videos.cs.cs12.compute --force blowup

Results are cached in ``.cache/cs12/<name>.json``; scenes call ``load(name)``.  Our side is ``explainer/cs/lang/``:
``regex.py`` (Thompson's construction, a backtracker, derivatives), ``automata.py`` (the subset construction,
minimization, state elimination, pushdown automata), ``grammar.py`` (FIRST/FOLLOW, LL(1), the LR family, CYK,
Earley) and ``pebble_lang.py`` (the Pebble language's lexer, parser and grammar), tested in tests/test_cs12_lang.py.
This machine's side times Python's re, Perl and GNU grep, and runs bison on the same grammars as a cross-check.

Items:
    tools      Python, Perl, grep and bison on this machine
    blowup     (a+)+b on a^n: our backtracker's steps, Thompson's work, Python re and Perl timed, grep timed
    cloudflare the shape of the 2019 outage's regex, .*.*=.*, searched in lines without '=': cubic, against grep
    thompson   the NFA for (a|b)*abb, and its set-of-states run
    subset     (a|b)*abb through the subset construction and minimization; the n-th-from-end blow-up
    kleene     a DFA for binary multiples of 3, back to a regex by state elimination, checked on 0..4095
    pumping    a^p b^p: every split xyz with |xy| <= p and |y| > 0 pumps out of the language
    myhill     the n-th-from-end language: a distinguishing suffix for every pair of 3-bit strings
    primes     a back-reference regex that recognizes composite numbers in unary
    lexer      the Job in the Pebble language, tokenized: counts, maximal munch, the combined DFA
    cfg        a leftmost derivation; ambiguity counted (Catalan numbers); the dangling else
    pda        a pushdown automaton for a^n b^n, and one for palindromes (nondeterministic)
    cyk        a CYK table; CYK and Earley timed against sentence length, ambiguous and not
    ll1        FIRST, FOLLOW, the LL(1) table and a trace, after removing left recursion
    lr         LR(0), SLR, LALR and LR(1) automata; a grammar SLR cannot handle; bison's state counts
    pebble     the Pebble language's grammar and LALR table (and bison's), its ASTs and its error messages
    frontier   Thompson's time against text x pattern; CYK's cubic time; derivative automata against minimal DFAs
    lazy       lazy determinization on Pride and Prejudice: how many of 2^n DFA states real text reaches
    indent     Python's own tokenizer on a small function: INDENT and DEDENT from a stack of levels
"""

from __future__ import annotations

import re
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

from explainer.ai.cache import Cache

CACHE = Cache("cs12")
load = CACHE.load


def _sh(cmd) -> str:
    return subprocess.run(cmd, shell=isinstance(cmd, str), capture_output=True, text=True).stdout


def compute_tools() -> dict:
    return {"python": sys.version.split()[0], "perl": _sh("perl -e 'print $^V'").strip(),
            "grep": _sh("grep --version").splitlines()[0], "bison": _sh("bison --version").splitlines()[0]}


# ---------------------------------------------------------------------------
# backtracking against automata
# ---------------------------------------------------------------------------
def _time_python(pattern: str, text_expr: str, mode: str, timeout: float = 20.0):
    code = (f"import re, time\nt = {text_expr}\np = re.compile({pattern!r})\nt0 = time.perf_counter()\n"
            f"m = p.{mode}(t)\nprint(time.perf_counter() - t0, m is not None)")
    try:
        r = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, timeout=timeout)
        dt, ok = r.stdout.split()
        return float(dt), ok == "True"
    except subprocess.TimeoutExpired:
        return None, None


def _time_perl(pattern: str, n: int, ch: str = "a", timeout: float = 20.0):
    code = (f'use Time::HiRes qw(time); my $s = "{ch}" x {n}; my $t = time; my $m = ($s =~ /^{pattern}$/) ? 1 : 0; '
            f'printf("%.6f %d\\n", time - $t, $m);')
    try:
        r = subprocess.run(["perl", "-e", code], capture_output=True, text=True, timeout=timeout)
        dt, ok = r.stdout.split()
        return float(dt), ok == "1"
    except subprocess.TimeoutExpired:
        return None, None


def _time_grep(pattern: str, line: str, reps: int = 5):
    with tempfile.TemporaryDirectory() as d:
        f = Path(d) / "in.txt"
        f.write_text(line + "\n")
        best = None
        for _ in range(reps):
            t0 = time.perf_counter()
            subprocess.run(["grep", "-cE", pattern, str(f)], capture_output=True)
            dt = time.perf_counter() - t0
            best = dt if best is None else min(best, dt)
        # subtract grep's start-up cost, measured on an empty pattern match
        f.write_text("\n")
        base = min(_run_time(["grep", "-cE", "x", str(f)]) for _ in range(reps))
    return max(best - base, 0.0), base


def _run_time(cmd):
    t0 = time.perf_counter()
    subprocess.run(cmd, capture_output=True)
    return time.perf_counter() - t0


def compute_blowup() -> dict:
    from explainer.cs.lang import regex as R

    n_ = R.parse("(a+)+b")
    nfa = R.thompson(n_)
    ours = []
    for n in range(2, 25):
        try:
            ok, steps = R.backtrack(n_, "a" * n, limit=5 * 10 ** 7)
        except R.StepLimit:
            steps = None
        ours.append({"n": n, "steps": steps, "thompson": nfa.run("a" * n)[1]})
    py = []
    for n in range(14, 31, 2):
        dt, _ = _time_python("(a+)+b", f"'a' * {n}", "fullmatch", timeout=30)
        py.append({"n": n, "s": dt})
        if dt is None or dt > 12:
            break
    pl = []
    for n in range(14, 31, 2):
        dt, _ = _time_perl("(a+)+b", n, timeout=30)
        pl.append({"n": n, "s": dt})
        if dt is None or dt > 12:
            break
    gr = []
    for n in (30, 1000, 100_000, 1_000_000):
        dt, base = _time_grep("^(a+)+b$", "a" * n)
        gr.append({"n": n, "s": dt, "startup": base})
    th = []
    for n in (30, 1000, 10_000, 100_000):
        t0 = time.perf_counter()
        nfa.run("a" * n)
        th.append({"n": n, "s": time.perf_counter() - t0})
    return {"ours": ours, "python": py, "perl": pl, "grep": gr, "thompson_time": th, "nfa_states": nfa.n}


def compute_cloudflare() -> dict:
    """The 2 July 2019 outage: a WAF rule containing  .*(?:.*=.*)  ran against request text, and a backtracking
    engine took cubic time.  We time the core shape on lines with no '='."""
    rows = []
    for n in (1000, 2000, 4000, 8000):
        dt, _ = _time_python(r".*.*=.*", f"'x' * {n}", "search", timeout=60)
        g, base = _time_grep(".*.*=.*", "x" * n)
        rows.append({"n": n, "python": dt, "grep": g})
        if dt is None or dt > 20:
            break
    return {"rows": rows, "rule": r"(?:(?:\"|'|\]|\}|\\|\d|(?:nan|infinity|true|false|null|undefined|symbol|math)|"
                                  r"\`|\-|\+)+[)]*;?((?:\s|-|~|!|{}|\|\||\+)*.*(?:.*=.*)))"}


# ---------------------------------------------------------------------------
# automata
# ---------------------------------------------------------------------------
def compute_thompson() -> dict:
    from explainer.cs.lang import regex as R

    m = R.compile("(a|b)*abb")
    ok, work, seq = m.run("babbabb", trace=True)
    edges = [(s, t, "ε") for s in range(m.n) for t in m.eps[s]] + \
            [(s, t, cs.label) for s in range(m.n) for cs, t in m.edges[s]]
    sizes = {p: R.compile(p).n for p in ("a", "ab", "a|b", "a*", "(a|b)*", "(a|b)*abb")}
    return {"states": m.n, "start": m.start, "accept": m.accept, "edges": edges, "text": "babbabb",
            "sets": [sorted(S) for S in seq], "accepted": ok, "sizes": sizes}


def compute_subset() -> dict:
    from explainer.cs.lang import automata as A
    from explainer.cs.lang import regex as R

    nfa = R.compile("(a|b)*abb")
    d = A.subset(nfa, "ab")
    m, rounds = A.minimize(d, trace=True)
    blow = []
    for n in range(1, 13):
        nf = R.compile(A.nth_from_end(n))
        dd = A.subset(nf, "01")
        blow.append({"n": n, "thompson": nf.n, "nfa": n + 1, "dfa": dd.n, "minimal": A.minimize(dd).n})
    return {"dfa": {"n": d.n, "delta": d.delta, "accept": sorted(d.accept), "sets": [sorted(S) for S in d.names]},
            "minimal": {"n": m.n, "delta": m.delta, "accept": sorted(m.accept), "classes": m.names},
            "rounds": rounds, "blowup": blow}


def compute_kleene() -> dict:
    from explainer.cs.lang import automata as A
    from explainer.cs.lang import regex as R

    # remainder mod 3 of a binary number read most significant bit first
    d = A.DFA(["0", "1"], [{"0": 0, "1": 1}, {"0": 2, "1": 0}, {"0": 1, "1": 2}], 0, {0})
    rx, steps = A.to_regex(d, order=[2, 1, 0], trace=True)
    m = R.compile(rx.replace("(|", "(ε|"))
    checks = all(m.run(bin(k)[2:])[0] == (k % 3 == 0) for k in range(1, 4096))
    return {"delta": d.delta, "regex": rx, "length": len(rx), "checked": checks,
            "steps": [{"removed": q, "edges": {f"{a}->{b}": v for (a, b), v in R_.items()}} for q, R_ in steps]}


def compute_pumping() -> dict:
    p = 5
    s = "a" * p + "b" * p
    rows, all_fail = [], True
    for i in range(0, p + 1):              # x = s[:i], y = s[i:j], z = s[j:]
        for j in range(i + 1, p + 1):
            x, y, z = s[:i], s[i:j], s[j:]
            w = x + y * 2 + z
            inside = w.count("a") == w.count("b") and w == "a" * w.count("a") + "b" * w.count("b")
            all_fail &= not inside
            rows.append({"x": x, "y": y, "z": z, "pumped": w, "in": inside})
    return {"p": p, "s": s, "splits": rows, "all_fail": all_fail}


def compute_myhill() -> dict:
    import itertools

    from explainer.cs.lang import automata as A

    n = 3
    m = A.minimize(A.from_regex(A.nth_from_end(n), "01"))
    words = ["".join(w) for w in itertools.product("01", repeat=n)]
    table = {}
    for u, v in itertools.combinations(words, 2):
        z = A.distinguishing_suffix(u, v, n)
        table[f"{u},{v}"] = {"z": z, "u": m.run(u + z), "v": m.run(v + z)}
    return {"n": n, "words": words, "table": table, "minimal": m.n}


def compute_primes() -> dict:
    from explainer.cs.lang import regex as R

    n_ = R.parse(r"(11+)\1+")
    rows = []
    for k in range(2, 41):
        ok, steps = R.backtrack(n_, "1" * k)
        rows.append({"k": k, "composite": ok, "steps": steps})
    py = []
    for k in (1009, 2003, 4001, 8009):           # primes: every split must be tried and fail
        dt, ok = _time_python(r"(11+)\1+", f"'1' * {k}", "fullmatch", timeout=60)
        py.append({"k": k, "s": dt, "composite": ok})
    return {"rows": rows, "python": py}


# ---------------------------------------------------------------------------
# lexing
# ---------------------------------------------------------------------------
def compute_lexer() -> dict:
    from collections import Counter

    from explainer.cs.lang import pebble_lang as P
    from explainer.cs.lang import regex as R

    lx = P.Lexer()
    toks = lx.tokens(P.JOB)
    kinds = Counter("keyword" if t.kind in P.KEYWORDS else ("operator" if t.kind not in
                    ("num", "charlit", "string", "ident", "$") else t.kind) for t in toks[:-1])
    sample = "if p.length == n && same(p.letters, w, n) { return p; }"
    st = lx.tokens(sample)
    # maximal munch decisions on a tricky line
    munch = []
    for s in (">=", "->", "whiles", "while", "x-->y", "a==b"):
        munch.append({"text": s, "tokens": [t.text for t in lx.tokens(s)[:-1]]})
    # one combined DFA for all the token rules (a state is a tuple of NFA state sets; it accepts the first rule
    # whose NFA accepts): its size over the characters the Job uses
    alphabet = sorted(set(P.JOB))
    nfas = [m for _, m in lx.nfas]
    start = tuple(m.closure({m.start}) for m in nfas)
    index, todo, acc = {start: 0}, [start], {}
    while todo:
        S = todo.pop()
        for c in alphabet:
            T = tuple(m.step(s, c) for m, s in zip(nfas, S))
            if not any(T):
                continue
            if T not in index:
                index[T] = len(index)
                todo.append(T)
    for S, i in index.items():
        for (name, m), s in zip(lx.nfas, S):
            if m.accept in s:
                acc[i] = name
                break
    t0 = time.perf_counter()
    for _ in range(5):
        lx.tokens(P.JOB)
    rate = 5 * len(P.JOB) / (time.perf_counter() - t0)
    return {"tokens": len(toks) - 1, "kinds": dict(kinds), "chars": len(P.JOB), "lines": P.JOB.count("\n"),
            "sample": sample, "sample_tokens": [(t.kind, t.text) for t in st[:-1]], "munch": munch,
            "rules": [(n, rx) for n, rx in P.TOKENS], "nfa_states": sum(m.n for m in nfas),
            "dfa_states": len(index), "accepting": len(acc), "chars_per_s": rate,
            "keywords": sorted(P.KEYWORDS)}


# ---------------------------------------------------------------------------
# grammars
# ---------------------------------------------------------------------------
EXPR = """
E -> E + T | T
T -> T * F | F
F -> ( E ) | id
"""
AMBIG = "E -> E + E | E * E | ( E ) | id"
DANGLE = "S -> if c then S | if c then S else S | x"
LR_SLR = """
S -> L = R | R
L -> * R | id
R -> L
"""


def compute_cfg() -> dict:
    from explainer.cs.lang import grammar as G

    g = G.Grammar.parse(EXPR)
    # a leftmost derivation of id + id * id, found by the LR parse (rightmost, reversed) is not leftmost; we derive
    # by hand-guided search: expand the leftmost nonterminal with the production the LL(1) parser chooses
    g2 = G.remove_left_recursion(g)
    table, _ = G.ll1_table(g2)
    toks = "id + id * id".split()
    form, i, out = [g2.start], 0, [[g2.start]]
    while any(g2.is_nt(s) for s in form):
        k = next(j for j, s in enumerate(form) if g2.is_nt(s))
        i = sum(1 for s in form[:k])                      # terminals before it are matched in order
        la = toks[i] if i < len(toks) else "$"
        p = table[form[k]][la][0]
        form = form[:k] + list(g2.prods[p][1]) + form[k + 1:]
        out.append(list(form))
    amb = G.to_cnf(G.Grammar.parse(AMBIG))
    cat = []
    for n in range(1, 13):
        t = " + ".join(["id"] * n).split()
        cat.append({"operands": n, "trees": G.cyk(amb, t)[1]})
    unamb = G.to_cnf(g)
    dang = G.to_cnf(G.Grammar.parse(DANGLE))
    dt = "if c then if c then x else x".split()
    return {"derivation": out, "catalan": cat, "unambiguous_trees": G.cyk(unamb, "id + id + id + id".split())[1],
            "dangling_trees": G.cyk(dang, dt)[1], "dangling": " ".join(dt)}


def compute_pda() -> dict:
    from explainer.cs.lang import automata as A

    ok, path = A.ANBN.run("aaabbb")
    res = {w: A.ANBN.run(w)[0] for w in ("", "ab", "aabb", "aaabbb", "aab", "abab", "ba")}
    pal = {w: A.PALINDROMES.run(w)[0] for w in ("abba", "aba", "abab", "baab", "aabbaa", "ab")}
    return {"anbn_path": path, "anbn": res, "palindromes": pal}


def compute_cyk() -> dict:
    from explainer.cs.lang import grammar as G

    g = G.to_cnf(G.Grammar.parse(EXPR))
    toks = "id + id * id".split()
    T, trees = G.cyk(g, toks)
    cells = {f"{i},{l}": sorted(T[i][l]) for i in range(len(toks)) for l in range(1, len(toks) - i + 1)}
    timing = []
    amb_g = G.Grammar.parse(AMBIG)
    amb = G.to_cnf(amb_g)
    expr = G.Grammar.parse(EXPR)
    for n in (5, 9, 17, 33, 65):
        t = " + ".join(["id"] * ((n + 1) // 2)).split()
        t0 = time.perf_counter()
        G.cyk(g, t, count=False)
        c = time.perf_counter() - t0
        t0 = time.perf_counter()
        _, chart, _ = G.earley(expr, t)
        e = time.perf_counter() - t0
        t0 = time.perf_counter()
        _, chart2, _ = G.earley(amb_g, t)
        e2 = time.perf_counter() - t0
        timing.append({"n": len(t), "cyk": c, "earley": e, "earley_items": sum(map(len, chart)),
                       "earley_ambiguous": e2, "earley_ambiguous_items": sum(map(len, chart2))})
    return {"tokens": toks, "cells": cells, "trees": trees, "cnf": [list(p) for p in g.prods], "timing": timing}


def compute_ll1() -> dict:
    from explainer.cs.lang import grammar as G

    g = G.Grammar.parse(EXPR)
    _, conflicts = G.ll1_table(g)
    g2 = G.remove_left_recursion(g)
    table, c2 = G.ll1_table(g2)
    ok, steps = G.ll1_parse(g2, "id + id * id".split(), trace=True)
    return {"left_recursive_conflicts": len(conflicts), "prods": [G.show_prod(p) for p in g2.prods],
            "first": {a: sorted(v) for a, v in g2.first().items()}, "follow": {a: sorted(v) for a, v in
                                                                              g2.follow().items()},
            "nullable": sorted(g2.nullable()),
            "table": {a: {t: ps for t, ps in row.items()} for a, row in table.items()}, "conflicts": len(c2),
            "trace": [{"stack": s, "input": i, "action": a} for s, i, a in steps], "accepted": ok}


def _bison_states(g, conflicts_ok: bool = True) -> dict:
    """Write g as a bison grammar, run bison -v, and read the number of states and conflicts it reports."""
    if not shutil.which("bison"):
        return {}
    names = {}

    def tok(s):
        if s in names:
            return names[s]
        if len(s) == 1 and not s.isalnum():
            names[s] = f"'{s}'" if s not in ("'", "\\") else f"'\\{s}'"
        else:
            names[s] = "T_" + re.sub(r"\W", lambda m: f"_{ord(m.group())}_", s).upper()
        return names[s]
    nts = {a: "n_" + re.sub(r"\W", "_q", a) for a in g.nonterms}
    lines = []
    toks = [tok(t) for t in g.terms]
    decl = " ".join(t for t in toks if not t.startswith("'"))
    for a in g.nonterms:
        alts = [" ".join(nts[s] if g.is_nt(s) else tok(s) for s in r) or "%empty" for r in g.alts(a)]
        lines.append(f"{nts[a]} : " + "\n    | ".join(alts) + " ;")
    src = (f"%token {decl}\n" if decl else "") + f"%start {nts[g.start]}\n%%\n" + "\n".join(lines) + "\n%%\n"
    with tempfile.TemporaryDirectory() as d:
        f = Path(d) / "g.y"
        f.write_text(src)
        r = subprocess.run(["bison", "-v", "-o", str(Path(d) / "g.c"), str(f)], capture_output=True, text=True)
        out = (Path(d) / "g.output").read_text()
    states = len(re.findall(r"^State \d+$", out, re.M))
    conf = re.findall(r"(\d+) (shift/reduce|reduce/reduce) conflicts?", r.stderr)
    return {"states": states, "conflicts": [(int(n), k) for n, k in conf], "stderr": r.stderr.strip().splitlines()}


def compute_lr() -> dict:
    from explainer.cs.lang import grammar as G

    g = G.Grammar.parse(EXPR).augmented()
    s0, t0 = G.lr0_automaton(g)
    s1, t1 = G.lr1_automaton(g)
    sl, tl = G.lalr_automaton(g)
    a0, go0, c0 = G.lr_table(g, s0, t0, "lr0")
    a, go, cf = G.lr_table(g, s0, t0, "slr")
    ok, steps, tree = G.lr_parse(g, a, go, "id * id + id".split(), trace=True)

    def items(I):
        out = []
        for it in sorted(I):
            p, d = it[0], it[1]
            lhs, r = g.prods[p]
            out.append(f"{lhs} → " + " ".join(list(r[:d]) + ["•"] + list(r[d:])))
        return out
    lrs = G.Grammar.parse(LR_SLR).augmented()
    q0, u0 = G.lr0_automaton(lrs)
    slr_conf = G.lr_table(lrs, q0, u0, "slr")[2]
    ql, ul = G.lalr_automaton(lrs)
    lalr_conf = G.lr_table(lrs, ql, ul, "lr1")[2]
    dg = G.Grammar.parse(DANGLE).augmented()
    qd, ud = G.lr0_automaton(dg)
    dang = G.lr_table(dg, qd, ud, "slr")[2]
    action = {s: {t: sorted(v) for t, v in row.items()} for s, row in enumerate(a)}
    return {"lr0": {"states": [items(I) for I in s0], "trans": [[s, X, t] for (s, X), t in t0.items()],
                    "conflicts": [[c[0], c[1], c[2]] for c in c0]},
            "slr": {"action": action, "goto": [dict(x) for x in go], "conflicts": len(cf)},
            "trace": [{"stack": st, "symbols": sy, "input": inp, "action": list(act)} for st, sy, inp, act in steps],
            "accepted": ok, "lr1_states": len(s1), "lalr_states": len(sl), "lr0_states": len(s0),
            "slr_fails": [[c[0], c[1], c[2]] for c in slr_conf], "lalr_ok": not lalr_conf,
            "lslr_lalr_states": len(ql), "dangling_states": len(qd),
            "dangling": [[c[0], c[1], c[2]] for c in dang],
            "bison": {"expr": _bison_states(G.Grammar.parse(EXPR)), "lslr": _bison_states(G.Grammar.parse(LR_SLR)),
                      "dangling": _bison_states(G.Grammar.parse(DANGLE))}}


def compute_pebble() -> dict:
    from explainer.cs.lang import grammar as G
    from explainer.cs.lang import pebble_lang as P

    g = G.Grammar.parse(P.BNF)
    gg = g.augmented()
    sl, tl = G.lalr_automaton(gg)
    a, go, cf = G.lr_table(gg, sl, tl, "lr1")
    s0, t0 = G.lr0_automaton(gg)
    slr = G.lr_table(gg, s0, t0, "slr")[2]
    toks = P.lex(P.JOB)
    t1 = time.perf_counter()
    prog = P.parse(P.JOB)
    rd = time.perf_counter() - t1
    t1 = time.perf_counter()
    okl = G.lr_parse(gg, a, go, [t.kind for t in toks[:-1]])
    lr = time.perf_counter() - t1
    lookup = next(f for f in prog.funcs if f.name == "lookup")
    errors = {}
    for src in ("fn f() { var x: int = ; }", "fn f() { if x { return 1 }", "fn f( { }", "struct S { a int; }"):
        try:
            P.parse(src)
            errors[src] = "ok"
        except (P.ParseError, P.LexError) as e:
            errors[src] = str(e)
    pratt = {s: P.show(P.parse_expr(s)) for s in ("a + b * c - d", "1 - 2 - 3", "-x.f[2] * *p",
                                                  "p.length == n && same(p.letters, w, n)")}
    return {"prods": len(g.prods), "nonterms": len(g.nonterms), "terms": len(g.terms), "lalr_states": len(sl),
            "lalr_conflicts": len(cf), "slr_conflicts": len(slr), "bison": _bison_states(g),
            "tokens": len(toks) - 1, "nodes": P.count_nodes(prog), "funcs": [f.name for f in prog.funcs],
            "lookup_nodes": P.count_nodes(lookup), "lr_accepts": okl, "rd_s": rd, "lr_s": lr,
            "errors": errors, "pratt": pratt, "bnf": P.BNF.strip().splitlines()}


# ---------------------------------------------------------------------------
# the frontier
# ---------------------------------------------------------------------------
def compute_frontier() -> dict:
    from explainer.cs.lang import automata as A
    from explainer.cs.lang import grammar as G
    from explainer.cs.lang import regex as R

    # Thompson simulation: work grows like (text length) x (pattern size)
    grid = []
    for m in (8, 16, 32, 64):
        pat = "(a|b)*" + "a" * (m // 2) + "(a|b)" * (m // 2 - 1) + "b"
        nfa = R.compile(pat)
        for n in (1000, 2000, 4000):
            text = "a" * n
            _, work, _ = nfa.run(text)
            grid.append({"m": R.size(R.parse(pat)), "states": nfa.n, "n": n, "work": work})
    # CYK: time against length (cubic), to set against Valiant's matrix-multiplication bound
    g = G.to_cnf(G.Grammar.parse(EXPR))
    cyk = []
    for k in (8, 16, 32, 64):
        t = " + ".join(["id"] * k).split()
        t0 = time.perf_counter()
        G.cyk(g, t, count=False)
        cyk.append({"n": len(t), "s": time.perf_counter() - t0})
    der = []
    for p in ("(a|b)*abb", "a(b|c)*d", "(a|b)*a(a|b)(a|b)", "(ab|a)*", "((a|b)(a|b))*", "(a|b)*a(a|b)(a|b)(a|b)"):
        al = sorted(set(c for c in p if c.isalpha()))
        st, _, _ = R.brzozowski_dfa(R.parse(p), al)
        der.append({"regex": p, "derivatives": len(st), "minimal": A.minimize(A.from_regex(p, al)).n})
    return {"thompson": grid, "cyk": cyk, "derivatives": der}


def compute_lazy() -> dict:
    """What grep and RE2 actually do: determinize lazily, building a DFA state only when the text reaches it.  On
    real English, how many of the 2^n states of 'the n-th character back is e' are ever built?"""
    import videos.ai.ai1.compute as A
    from explainer.cs.lang import regex as R

    text = (A.BOOK_DIR / "1342.txt").read_text(encoding="utf-8").lower()[:300_000]
    rows = []
    for n in (4, 8, 12, 16):
        nfa = R.compile("(.)*e" + "." * (n - 1))
        cur = nfa.closure({nfa.start})
        seen = {cur}
        hits = 0
        t0 = time.perf_counter()
        for c in text:
            cur = nfa.step(cur, c)
            seen.add(cur)
            hits += nfa.accept in cur
        dt = time.perf_counter() - t0
        check = sum(1 for i in range(n - 1, len(text)) if text[i - n + 1] == "e")
        rows.append({"n": n, "built": len(seen), "possible": 2 ** n, "hits": hits, "check": check, "s": dt})
    return {"chars": len(text), "rows": rows}


INDENT_SRC = """def lookup(word):
    for node in table:
        if node.word == word:
            return node
    return None
"""


def compute_indent() -> dict:
    """Python's lexer keeps a stack of indentation levels and turns changes into INDENT and DEDENT tokens."""
    import io
    import tokenize

    toks = []
    stack = [0]
    for t in tokenize.generate_tokens(io.StringIO(INDENT_SRC).readline):
        name = tokenize.tok_name[t.type]
        if name in ("NL", "ENDMARKER", "COMMENT"):
            continue
        if name == "INDENT":
            stack.append(len(t.string))
        elif name == "DEDENT":
            stack.pop()
        toks.append({"kind": name, "text": t.string if name not in ("NEWLINE", "INDENT", "DEDENT") else "",
                     "line": t.start[0], "stack": list(stack)})
    return {"source": INDENT_SRC.rstrip("\n").splitlines(), "tokens": toks}


ITEMS = {
    "tools": compute_tools, "blowup": compute_blowup, "cloudflare": compute_cloudflare, "thompson": compute_thompson,
    "subset": compute_subset, "kleene": compute_kleene, "pumping": compute_pumping, "myhill": compute_myhill,
    "primes": compute_primes, "lexer": compute_lexer, "cfg": compute_cfg, "pda": compute_pda, "cyk": compute_cyk,
    "ll1": compute_ll1, "lr": compute_lr, "pebble": compute_pebble, "frontier": compute_frontier,
    "lazy": compute_lazy, "indent": compute_indent,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
