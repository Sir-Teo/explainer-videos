"""Precompute everything numerical in Part 21 of *Computer Science, Built* ("Strings").

    python -m videos.cs.cs21.compute              # everything missing
    python -m videos.cs.cs21.compute --force fm

Results are cached in ``.cache/cs21/<name>.json``; scenes call ``load(name)``.  The instrument is
``explainer/cs/algo/strings.py`` (tested in tests/test_cs21_strings.py).  ``sa`` builds the suffix array of the whole
corpus (about two minutes) and saves it in the cache directory for ``fm``, ``bwt`` and ``repeats``.

Items:
    hook      "Queequeg" found four ways in the 25 MB corpus
    naive     the naive matcher's comparisons, on the novels and on its worst case
    rk        Rabin-Karp: spurious hits against the modulus
    kmp       the failure function and automaton; comparisons against 2n
    bm        Boyer-Moore and Horspool: comparisons per character against pattern length
    ac        Aho-Corasick: every character name at once
    sa        the suffix array of the corpus, its LCP array, longest repeats, searches
    stree     the suffix tree of a short word
    bwt       the BWT of a chapter: runs, move-to-front, entropy, bzip2
    fm        the FM-index of the corpus: counts, locates, sizes
    lz        LZ77 with Huffman against zlib, bzip2 and xz; LZW
    entropy   Huffman against rANS against the entropy
    align     Needleman-Wunsch and Smith-Waterman on the novels' twice-told letter
    diff      Myers' diff on this repository's own history; patience diff
    rsync     rolling checksums, fixed blocks against content-defined chunks
    period    Manacher's longest palindrome; periods; Lyndon words; repetitive text and r
"""

from __future__ import annotations

import bz2
import lzma
import math
import random
import re
import subprocess
import time
import zlib
from collections import Counter
from pathlib import Path

import numpy as np

from explainer.ai.cache import Cache

CACHE = Cache("cs21")
load = CACHE.load
ROOT = Path(__file__).resolve().parents[3]


def _full_text() -> bytes:
    from videos.cs.cs16.compute import _full_text as f
    return f()


def _books():
    import videos.ai.ai1.compute as A
    from videos.cs.cs6.compute import novels
    b = novels()
    return {A.BOOKS[k]: b[k].encode("utf-8") for k in A.BOOKS}


def _best(f, reps=3):
    best, out = math.inf, None
    for _ in range(reps):
        t0 = time.perf_counter()
        out = f()
        best = min(best, time.perf_counter() - t0)
    return best, out


def _sa():
    p = CACHE.dir / "sa.npy"
    if not p.exists():
        compute_sa()
    return np.load(p)


def compute_hook() -> dict:
    from explainer.cs.algo import strings as S
    t = _full_text()
    pat = b"Queequeg"
    t_naive, (pos, cmp_naive) = _best(lambda: S.naive_fast(t, pat), 1)
    t_kmp, (pk, cmp_kmp) = _best(lambda: S.kmp(t, pat), 1)
    t_bm, (pb, cmp_bm, win_bm) = _best(lambda: S.boyer_moore(t, pat), 1)
    assert pos == pk == pb
    t_find, _ = _best(lambda: t.count(pat))
    f = CACHE.dir / "corpus.txt"
    f.write_bytes(t)
    t_grep, out = _best(lambda: subprocess.run(["grep", "-c", "-F", "Queequeg", str(f)], capture_output=True,
                                               text=True).stdout)
    f.unlink()
    sa = _sa()
    fm = S.FMIndex(t + b"\x00", sa)
    fm.steps = 0
    t_fm, (cnt, _) = _best(lambda: fm.count(pat))
    return {"n": len(t), "pattern": pat.decode(), "hits": len(pos), "naive_cmp": cmp_naive, "kmp_cmp": cmp_kmp,
            "bm_cmp": cmp_bm, "bm_windows": win_bm, "fm_count": cnt, "fm_ranks": 2 * len(pat), "t_kmp_py": t_kmp,
            "t_bm_py": t_bm, "t_find": t_find, "t_grep": t_grep, "t_fm": t_fm, "grep_lines": int(out.strip())}


def compute_naive() -> dict:
    from explainer.cs.algo import strings as S
    t = _full_text()
    rows = []
    for p in (b"the", b"whale", b"Queequeg", b"Elizabeth Bennet", b"it was the best of times"):
        pos, cmp = S.naive_fast(t, p)
        # predicted: an alignment compares character j + 1 exactly when the first j matched
        pred = sum(t.count(p[:j]) if j else len(t) for j in range(len(p))) / len(t)
        rows.append({"pattern": p.decode(), "m": len(p), "hits": len(pos), "cmp": cmp, "per_char": cmp / len(t),
                     "predicted": pred})
        print(rows[-1])
    worst = []
    for n, m in ((1000, 10), (1000, 100), (10000, 100), (100000, 1000)):
        text = b"a" * n
        pat = b"a" * (m - 1) + b"b"
        _, cmp = S.naive_fast(text, pat)
        worst.append({"n": n, "m": m, "cmp": cmp, "nm": (n - m + 1) * m})
    return {"n": len(t), "rows": rows, "worst": worst}


def compute_rk() -> dict:
    from explainer.cs.algo import strings as S
    t = _books()["Moby Dick"]
    pat = b"Queequeg"
    rows = []
    for mod in (101, 1009, 10007, 100003, 1_000_003, 1_000_000_007):
        t0 = time.perf_counter()
        pos, cmp, spur = S.rabin_karp(t, pat, mod=mod)
        rows.append({"mod": mod, "hits": len(pos), "spurious": spur, "expected": (len(t) - len(pat) + 1) / mod,
                     "cmp": cmp, "seconds": time.perf_counter() - t0})
        print(rows[-1])
    # a random prime modulus defeats any fixed text: the hash difference is a nonzero polynomial of degree m - 1
    return {"n": len(t), "pattern": pat.decode(), "rows": rows}


def compute_kmp() -> dict:
    from explainer.cs.algo import strings as S
    pats = ["ababaca", "abacabab", "Queequeg", "tatatat"]
    fails = {p: S.kmp_failure(p.encode()) for p in pats}
    pat = b"ababaca"
    delta = S.kmp_automaton(pat, b"abc")
    auto = [[delta[q][c] for c in b"abc"] for q in range(len(pat) + 1)]
    t = _full_text()
    rows = []
    for p in (b"Queequeg", b"the whale", b"tatata"):
        t0 = time.perf_counter()
        pos, cmp = S.kmp(t, p)
        rows.append({"pattern": p.decode(), "hits": len(pos), "cmp": cmp, "per_char": cmp / len(t),
                     "seconds": time.perf_counter() - t0})
        print(rows[-1])
    worst_t = b"a" * 100000
    _, wc = S.kmp(worst_t, b"a" * 99 + b"b")
    trace_text = b"abababacaba"
    trace, q = [], 0
    for c in trace_text:
        q = delta[q][c]
        trace.append(q)
    return {"fails": fails, "auto": auto, "pattern": pat.decode(), "rows": rows, "n": len(t), "worst_cmp": wc,
            "worst_n": len(worst_t), "trace_text": trace_text.decode(), "trace": trace}


def compute_bm() -> dict:
    from explainer.cs.algo import strings as S
    t = _books()["Moby Dick"]
    words = re.findall(rb"[A-Za-z]+(?: [A-Za-z]+)*", t)
    rng = random.Random(21)
    rows = []
    for m in (2, 4, 8, 16, 32, 64):
        pats = []
        while len(pats) < 3:
            k = rng.randrange(len(t) - m)
            p = t[k:k + m]
            if b"\n" not in p:
                pats.append(p)
        h = b = kc = 0
        for p in pats:
            _, c1, _ = S.horspool(t, p)
            _, c2, _ = S.boyer_moore(t, p)
            _, c3 = S.kmp(t, p)
            h += c1
            b += c2
            kc += c3
        rows.append({"m": m, "horspool": h / 3 / len(t), "bm": b / 3 / len(t), "kmp": kc / 3 / len(t)})
        print(rows[-1])
    gs = S.good_suffix(b"ANPANMAN")
    return {"n": len(t), "rows": rows, "gs_example": gs, "words": len(words)}


def compute_ac() -> dict:
    from explainer.cs.algo import strings as S
    t = _full_text()
    names = [b"Elizabeth", b"Darcy", b"Ahab", b"Ishmael", b"Queequeg", b"Pip", b"Estella", b"Holmes", b"Watson",
             b"Dracula", b"Jonathan", b"Mina", b"Dorian", b"Jane", b"Rochester", b"Heathcliff", b"Catherine",
             b"Emma", b"Dantes", b"Pierre", b"Natasha", b"Andrew", b"Jim", b"Silver", b"Jekyll", b"Hyde", b"Huck",
             b"Tom", b"Raskolnikov", b"Alyosha", b"Dmitri", b"Gatsby", b"Daisy", b"Edna", b"Jo", b"Meg", b"Amy",
             b"Beth", b"Scrooge", b"Bloom", b"Stephen", b"Dorothea", b"Victor", b"Kurtz", b"Marlow"]
    t0 = time.perf_counter()
    ac = S.AhoCorasick(names)
    hits, steps = ac.search(t)
    t_ac = time.perf_counter() - t0
    sep = sum(len(t) for _ in names)
    return {"n": len(t), "patterns": len(names), "states": ac.states, "steps": steps, "seconds": t_ac,
            "top": [[p.decode(), c] for p, c in hits.most_common(12)], "separate_reads": sep,
            "tiny_trie": _tiny_trie()}


def _tiny_trie():
    from explainer.cs.algo import strings as S
    pats = [b"he", b"she", b"his", b"hers"]
    ac = S.AhoCorasick(pats)
    edges = [(s, chr(c), t) for s, d in enumerate(ac.goto) for c, t in d.items()]
    return {"patterns": [p.decode() for p in pats], "edges": edges, "fail": ac.fail,
            "out": [[p.decode() for p in o] for o in ac.out]}


def compute_sa() -> dict:
    from explainer.cs.algo import strings as S
    t = _full_text() + b"\x00"
    t0 = time.perf_counter()
    sa = S.suffix_array(t)
    t_sa = time.perf_counter() - t0
    CACHE.dir.mkdir(parents=True, exist_ok=True)
    np.save(CACHE.dir / "sa.npy", sa.astype(np.int32))
    # LCP by Kasai is linear but in Python too slow for 25 MB; use it on one novel, and adjacent comparisons in numpy
    md = _books()["Moby Dick"] + b"\x00"
    sa_md = S.suffix_array(md)
    t0 = time.perf_counter()
    lcp = S.lcp_kasai(md, sa_md)
    t_lcp = time.perf_counter() - t0
    i = int(np.argmax(lcp))
    rep = md[sa_md[i]:sa_md[i] + int(lcp[i])]
    distinct = len(md) * (len(md) + 1) // 2 - int(lcp.sum())
    searches = []
    for p in (b"Queequeg", b"whale", b"Call me Ishmael"):
        lo, hi, cmp = S.sa_search(t, sa, p)
        searches.append({"pattern": p.decode(), "count": hi - lo, "cmp": cmp, "bound": len(p) * 2 * math.log2(len(t))})
    # the first rows of the suffix array of a famous sentence, for drawing
    s = b"it was the best of times$"
    sa_s = S.suffix_array_naive(s)
    return {"n": len(t), "t_sa": t_sa, "md_n": len(md), "t_lcp": t_lcp, "md_longest_repeat": rep.decode(errors="replace"),
            "md_repeat_len": int(lcp[i]), "md_distinct_substrings": distinct, "md_mean_lcp": float(lcp.mean()),
            "searches": searches, "small": s.decode(), "small_sa": sa_s,
            "small_suffixes": [s[k:].decode() for k in sa_s], "bytes_sa": 4 * len(t)}


def compute_repeats() -> dict:
    """The longest repeated passage in the whole corpus: adjacent suffixes in the suffix array, compared in numpy."""
    t = _full_text() + b"\x00"
    sa = _sa().astype(np.int64)
    a = np.frombuffer(t, dtype=np.uint8)
    n = len(a)
    # common prefix of adjacent suffixes, doubling until no pair grows
    lcp = np.zeros(n, dtype=np.int64)
    alive = np.arange(1, n)
    step = 1
    while len(alive):
        x, y = sa[alive - 1] + lcp[alive], sa[alive] + lcp[alive]
        ok = (x + step <= n) & (y + step <= n)
        same = np.zeros(len(alive), dtype=bool)
        idx = np.flatnonzero(ok)
        if len(idx):
            # compare step characters via a rolling comparison of 8-byte words where possible
            eq = np.ones(len(idx), dtype=bool)
            for k in range(step):
                eq &= a[x[idx] + k] == a[y[idx] + k]
            same[idx] = eq
        lcp[alive[same]] += step
        alive = alive[same]
        step = min(step * 2, 64)
        if step == 64 and len(alive) < 2:
            break
    i = int(np.argmax(lcp))
    L = int(lcp[i])
    rep = t[sa[i]:sa[i] + L]
    return {"length": L, "text": rep[:400].decode(errors="replace"), "at": [int(sa[i - 1]), int(sa[i])]}


def compute_stree() -> dict:
    from explainer.cs.algo import strings as S
    edges, nodes = S.suffix_tree_edges("banana$")
    return {"word": "banana$", "edges": edges, "nodes": nodes}


def compute_bwt() -> dict:
    from explainer.cs.algo import strings as S
    word = b"banana\x00"
    sa = S.suffix_array(word)
    rot = sorted(range(len(word)), key=lambda i: word[i:] + word[:i])
    L = S.bwt_from_sa(word, sa)
    md = _books()["Moby Dick"]
    k = md.find(b"Call me Ishmael")
    chap = md[k:k + 12000] + b"\x00"
    sa_c = S.suffix_array(chap)
    Lc = S.bwt_from_sa(chap, sa_c)
    mtf = S.move_to_front(Lc)
    z = int(np.count_nonzero(mtf == 0))
    full = _books()["Moby Dick"] + b"\x00"
    sa_f = S.suffix_array(full)
    Lf = S.bwt_from_sa(full, sa_f)
    mtf_f = S.move_to_front(Lf)
    return {"word": "banana$", "rotations": [(word[i:] + word[:i]).decode().replace("\x00", "$") for i in rot],
            "L": L.decode().replace("\x00", "$"), "chapter_n": len(chap), "chapter_runs": S.runs(Lc),
            "chapter_bwt_sample": Lc[4000:4300].decode(errors="replace").replace("\x00", "$"),
            "chapter_text_sample": chap[:300].decode(errors="replace"), "mtf_zero_share": z / len(mtf),
            "md_n": len(full), "md_runs": S.runs(Lf), "h0_text": S.entropy(np.frombuffer(full, dtype=np.uint8)),
            "h0_mtf": S.entropy(mtf_f), "bz2_text": len(bz2.compress(full, 9)), "zlib_text": len(zlib.compress(full, 9)),
            "bz2_bwt": len(bz2.compress(Lf, 9)), "inverse_ok": S.inverse_bwt(Lf) == full, "ctx": _contexts(full)}


def _contexts(full: bytes) -> dict:
    """What precedes a two-letter context in Moby-Dick: the groups the transform lays side by side."""
    from collections import Counter
    out = {}
    for c in ("he", "hi", "ho"):
        cnt = Counter(full[m.start() - 1] for m in re.finditer(c.encode(), full) if m.start())
        out[c] = {"total": sum(cnt.values()), "top": [[chr(k), v] for k, v in cnt.most_common(6)]}
    return out


def compute_fm() -> dict:
    from explainer.cs.algo import strings as S
    t = _full_text() + b"\x00"
    sa = _sa()
    t0 = time.perf_counter()
    fm = S.FMIndex(t, sa, step=64, sa_step=32)
    t_build = time.perf_counter() - t0
    rows = []
    for p in (b"Queequeg", b"whale", b"Elizabeth", b"Mr. Darcy", b"the", b"it was the best of times",
              b"Call me Ishmael"):
        fm.steps = 0
        t1 = time.perf_counter()
        c, (lo, hi) = fm.count(p)
        tc = time.perf_counter() - t1
        locs = []
        t2 = time.perf_counter()
        for r in range(lo, min(hi, lo + 5)):
            locs.append(fm.locate(r))
        tl = (time.perf_counter() - t2) / max(1, len(locs))
        assert all(t[x:x + len(p)] == p for x in locs)
        rows.append({"pattern": p.decode(), "count": c, "ranks": fm.steps, "t_count": tc, "t_locate": tl})
        print(rows[-1])
    L = fm.L.tobytes()
    sizes = fm.bytes_used()
    bz_L = len(bz2.compress(L, 9))
    r = S.runs(L)
    # a backward-search trace on banana for drawing
    w = b"banana\x00"
    fmw = S.FMIndex(w, S.suffix_array(w), step=1, sa_step=1)
    trace = []
    lo, hi = 0, len(w)
    for c in reversed(b"ana"):
        lo = int(fmw.C[c]) + fmw.rank(c, lo)
        hi = int(fmw.C[c]) + fmw.rank(c, hi)
        trace.append([chr(c), lo, hi])
    return {"n": len(t), "t_build": t_build, "rows": rows, "sizes": sizes, "bz2_bwt": bz_L, "runs": r,
            "text_bytes": len(t), "banana_trace": trace}


def compute_lz() -> dict:
    from explainer.cs.algo import strings as S
    books = _books()
    rows = []
    for name in ("Pride and Prejudice", "Moby Dick", "Ulysses"):
        d = books[name]
        t0 = time.perf_counter()
        tok = S.lz77(d)
        t_lz = time.perf_counter() - t0
        assert S.lz77_decode(tok) == d
        sz = S.deflate_size(tok)
        codes, nd = S.lzw(d)
        lzw_bits = sum(max(9, math.ceil(math.log2(256 + i + 1))) for i in range(len(codes)))
        rows.append({"book": name, "n": len(d), "ours": sz["bytes"], "zlib": len(zlib.compress(d, 9)),
                     "bz2": len(bz2.compress(d, 9)), "xz": len(lzma.compress(d, preset=9)), "lzw": lzw_bits / 8,
                     "matches": sz["matches"], "literals": sz["literals"], "t_lz": t_lz,
                     "mean_len": float(np.mean([x[0] for x in tok if not isinstance(x, int)]))})
        print(rows[-1])
    # back-references in a famous passage, for drawing
    tt = books["A Tale of Two Cities"]
    k = tt.find(b"It was the best of times")
    passage = tt[k:k + 300]
    tok = S.lz77(passage)
    arcs, pos = [], 0
    for x in tok:
        if isinstance(x, int):
            pos += 1
        else:
            arcs.append([pos, x[0], x[1]])
            pos += x[0]
    allb = b"".join(books.values())
    t0 = time.perf_counter()
    zc = len(zlib.compress(allb, 6))
    t_z = time.perf_counter() - t0
    return {"rows": rows, "passage": passage.decode(errors="replace"), "arcs": arcs, "tokens": len(tok),
            "corpus": len(allb), "corpus_zlib": zc, "t_zlib": t_z}


def compute_entropy() -> dict:
    from explainer.cs.algo import strings as S
    d = _books()["Moby Dick"]
    sym = np.frombuffer(d, dtype=np.uint8)
    h0 = S.entropy(sym)
    lens = S.huffman_lengths(Counter(d))
    huff = sum(Counter(d)[s] * lens[s] for s in lens) / len(d)
    r = S.RANS(d)
    t0 = time.perf_counter()
    enc = r.encode(d)
    t_enc = time.perf_counter() - t0
    assert r.decode(enc, len(d)) == d
    # a skewed source where Huffman's whole bits hurt: the MTF output of the BWT
    full = d + b"\x00"
    L = S.bwt_from_sa(full, S.suffix_array(full))
    m = S.move_to_front(L)
    hm = S.entropy(m)
    lm = S.huffman_lengths(Counter(m.tolist()))
    cm = Counter(m.tolist())
    huff_m = sum(cm[s] * lm[s] for s in lm) / len(m)
    rm = S.RANS(m.tobytes())
    enc_m = rm.encode(m.tobytes())
    # a skewed two-symbol source: Huffman must spend a whole bit, rANS spends the entropy
    rng = np.random.default_rng(21)
    skew = []
    for p in (0.5, 0.8, 0.95, 0.99):
        src = (rng.random(200_000) < p).astype(np.uint8).tobytes()
        rs = S.RANS(src)
        e = rs.encode(src)
        assert rs.decode(e, len(src)) == src
        h = -(p * math.log2(p) + (1 - p) * math.log2(1 - p))
        skew.append({"p": p, "entropy": h, "huffman": 1.0, "rans": len(e) * 8 / len(src)})
    order1 = _order_k_entropy(d, 1)
    order2 = _order_k_entropy(d, 2)
    return {"n": len(d), "h0": h0, "huffman": huff, "rans": len(enc) * 8 / len(d), "t_rans": t_enc,
            "mtf_h0": hm, "mtf_huffman": huff_m, "mtf_rans": len(enc_m) * 8 / len(m), "mtf_zero": cm[0] / len(m),
            "h1": order1, "h2": order2, "skew": skew}


def _order_k_entropy(d: bytes, k: int) -> float:
    ctx = Counter(d[i:i + k + 1] for i in range(len(d) - k))
    pre = Counter()
    for s, c in ctx.items():
        pre[s[:k]] += c
    n = sum(ctx.values())
    return float(-sum(c * math.log2(c / pre[s[:k]]) for s, c in ctx.items()) / n)


def compute_align() -> dict:
    from explainer.cs.algo import strings as S
    a, b = "INTENTION", "EXECUTION"
    nw = S.needleman_wunsch(a, b)
    mc = _books()["The Count of Monte Cristo"].decode()
    key = "The king's attorney is informed by a friend to the throne"
    i1 = mc.find(key)
    i2 = mc.find(key, i1 + 100)
    x = mc[i1 - 40:i1 + 260]
    y = mc[i2 - 40:i2 + 260]
    t0 = time.perf_counter()
    best, end, start, H = S.smith_waterman(x, y)
    t_sw = time.perf_counter() - t0
    return {"nw_a": a, "nw_b": b, "nw": nw.tolist(), "nw_score": int(nw[-1, -1]), "sw_x": x, "sw_y": y,
            "sw_best": best, "sw_end": list(end), "sw_start": list(start),
            "sw_x_part": x[start[0]:end[0]], "sw_y_part": y[start[1]:end[1]], "cells": len(x) * len(y),
            "t_sw": t_sw, "found": i1 >= 0 and i2 >= 0}


def compute_diff() -> dict:
    from explainer.cs.algo import strings as S
    path = "videos/cs/SYLLABUS.md"
    revs = subprocess.run(["git", "log", "--format=%h", "--", path], cwd=ROOT, capture_output=True,
                          text=True).stdout.split()[::-1]
    rows = []
    prev = pph = None
    for h in revs:
        cur = subprocess.run(["git", "show", f"{h}:{path}"], cwd=ROOT, capture_output=True, text=True).stdout
        cur = cur.split("\n")
        if cur and cur[-1] == "":
            cur.pop()
        if prev is not None:
            t0 = time.perf_counter()
            D, ops, trace, snake = S.myers(prev, cur)
            tm = time.perf_counter() - t0
            num = subprocess.run(["git", "diff", "--numstat", "--minimal", pph, h, "--", path], cwd=ROOT,
                                 capture_output=True, text=True).stdout.split()
            g = int(num[0]) + int(num[1]) if num else 0
            minimal = D == len(prev) + len(cur) - 2 * S.lcs_len(prev, cur)
            rows.append({"rev": h, "n": len(prev), "m": len(cur), "D": D, "git": g, "snake": snake, "seconds": tm,
                         "nd": (len(prev) + len(cur)) * D, "minimal": minimal})
        prev, pph = cur, h
    # a small example for the edit graph
    a, b = list("ABCABBA"), list("CBABAC")
    D, ops, trace, _ = S.myers(a, b)
    return {"path": path, "revisions": len(revs), "rows": rows, "ex_a": "".join(a), "ex_b": "".join(b), "ex_D": D,
            "ex_ops": ops, "ex_trace": [{str(k): v for k, v in t.items()} for t in trace]}


def compute_rsync() -> dict:
    from explainer.cs.algo import strings as S
    d = _books()["Moby Dick"]
    mid = len(d) // 2
    edited = d[:mid] + b"Call me Ishmael, again. " + d[mid:]
    B = 2048
    fixed_old = {d[i:i + B] for i in range(0, len(d), B)}
    fixed_new = [edited[i:i + B] for i in range(0, len(edited), B)]
    fixed_reused = sum(1 for x in fixed_new if x in fixed_old)
    # rsync: the receiver's blocks, found anywhere in the new file by the rolling checksum
    weak = S.adler32_rolling(edited, B)
    old_blocks = {}
    for i in range(0, len(d) - B + 1, B):
        old_blocks.setdefault(int(S.adler32_rolling(d[i:i + B], B)[0]), []).append(d[i:i + B])
    i, matched, literal = 0, 0, 0
    while i <= len(edited) - B:
        w = int(weak[i])
        if w in old_blocks and edited[i:i + B] in old_blocks[w]:
            matched += 1
            i += B
        else:
            literal += 1
            i += 1
    literal += len(edited) - i
    cuts_o = S.cdc_chunks(d)
    cuts_n = S.cdc_chunks(edited)
    ho, hn = S.chunk_hashes(d, cuts_o), S.chunk_hashes(edited, cuts_n)
    so = set(ho)
    new_chunks = [k for k, h in enumerate(hn) if h not in so]
    sizes = np.diff([0] + cuts_o)
    return {"n": len(d), "insert": 24, "block": B, "fixed_blocks": len(fixed_new), "fixed_reused": fixed_reused,
            "rsync_matched": matched, "rsync_literal": literal, "cdc_chunks": len(cuts_o), "cdc_new": len(new_chunks),
            "cdc_mean": float(sizes.mean()), "cdc_min": int(sizes.min()), "cdc_max": int(sizes.max()),
            "cdc_new_bytes": int(sum(np.diff([0] + cuts_n)[k] for k in new_chunks)),
            "cdc_sizes_old": [int(x) for x in sizes], "cdc_sizes_new": [int(x) for x in np.diff([0] + cuts_n)],
            "cdc_new_idx": [int(k) for k in new_chunks], "mid": mid}


def compute_period() -> dict:
    from explainer.cs.algo import strings as S
    t = _full_text()
    letters = bytes(re.sub(rb"[^a-z]", b"", t.lower()))
    t0 = time.perf_counter()
    rad = S.manacher(letters, all_=True)
    t_m = time.perf_counter() - t0
    st, ln = 0, 0
    for k in np.flatnonzero(np.asarray(rad) >= 12):     # the longest palindrome with at least four letters in it
        r = rad[k]
        cand = letters[(k - r) // 2:(k - r) // 2 + r]
        if len(set(cand)) >= 4 and r > ln:
            st, ln = (k - r) // 2, r
    pal = letters[st:st + ln].decode()
    per = {w: S.periods(w.encode()) for w in ("abaababaab", "abcabcab", "aaaa", "tatatat")}
    lyn = {w: S.duval(w) for w in ("banana", "mississippi", "abracadabra")}
    # repetitiveness: the suffix-array runs r for ordinary text against versions of one file
    path = "videos/cs/SYLLABUS.md"
    revs = subprocess.run(["git", "log", "--format=%h", "--", path], cwd=ROOT, capture_output=True,
                          text=True).stdout.split()
    vers = b"".join(subprocess.run(["git", "show", f"{h}:{path}"], cwd=ROOT, capture_output=True).stdout
                    for h in revs) + b"\x00"
    Lv = S.bwt_from_sa(vers, S.suffix_array(vers))
    novel = t[:len(vers) - 1] + b"\x00"
    Ln = S.bwt_from_sa(novel, S.suffix_array(novel))
    return {"palindrome": pal, "pal_len": ln, "t_manacher": t_m, "scanned": len(letters),
            "where": t.lower().find(pal[:12].encode()) if False else None,
            "periods": per, "lyndon": lyn, "versions": len(revs), "vers_n": len(vers), "vers_runs": S.runs(Lv),
            "novel_runs": S.runs(Ln), "vers_bz2": len(bz2.compress(vers, 9)), "vers_xz": len(lzma.compress(vers)),
            "novel_strip": _strip(Ln), "vers_strip": _strip(Lv)}


def _strip(L: bytes, width: int = 480) -> list:
    """Run lengths of a typical window of the transform, for drawing: [character, length] pairs. The window is the
    one, of 400 evenly spaced, whose number of runs is closest to the transform's average."""
    target = width * _bwt_runs(L) / len(L)

    def runs_of(w):
        out = []
        for c in w:
            if out and out[-1][0] == c:
                out[-1][1] += 1
            else:
                out.append([c, 1])
        return out
    best = None
    for k in range(400):
        i = (len(L) - width) * k // 400
        r = runs_of(L[i:i + width])
        if best is None or abs(len(r) - target) < abs(len(best) - target):
            best = r
    return best


def _bwt_runs(L: bytes) -> int:
    from explainer.cs.algo import strings as S
    return S.runs(L)


ITEMS = {k[8:]: v for k, v in globals().items() if k.startswith("compute_")}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
