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
import functools
import json
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

from explainer.cache_lock import locked_item
from .measurement_references import (protocol, digest_bytes, find_all, naive_comparisons_reference,
                                     check_suffix_order, longest_repeat_reference, lzw_decode_reference,
                                     history_snapshot, alignment_reference, border_reference,
                                     exact_chunk_reuse, huffman_cost_reference)

SCHEMAS = {name: 2 for name in ('hook','naive','rk','kmp','bm','ac','sa','repeats','stree',
                               'bwt','fm','lz','entropy','align','diff','rsync','period')}

class StringsCache(Cache):
    @locked_item(lambda self, name: self.path(name))
    def load(self, name):
        if not cache_current(name, self.path(name)):
            self.save(name, ITEMS[name]())
        return super().load(name)

CACHE = StringsCache("cs21")

def cache_current(name, path=None):
    path = CACHE.path(name) if path is None else path
    return name not in SCHEMAS or (path.exists() and json.loads(path.read_text()).get('schema') == SCHEMAS[name])

def load(name):
    return CACHE.load(name)

_TRIALS = []

def _elapsed(start, label):
    seconds = time.perf_counter() - start
    _TRIALS.append(dict(operation=label,samples=[seconds],seconds=seconds,repeats=1,
                        statistic='single observation',validation='producer output checked after timer'))
    return seconds

def _assert(condition):
    assert condition

ROOT = Path(__file__).resolve().parents[3]


def _full_text() -> bytes:
    from videos.cs.cs16.compute import _full_text as f
    return f()


def _books():
    import videos.ai.ai1.compute as A
    from videos.cs.cs6.compute import novels
    b = novels()
    return {A.BOOKS[k]: b[k].encode("utf-8") for k in A.BOOKS}


def _best(f, reps=3, *, check, label):
    samples, out = [], None
    for _ in range(reps):
        start = time.perf_counter()
        value = f()
        samples.append(time.perf_counter() - start)
        check(value)
        out = value
    _TRIALS.append(dict(operation=label,samples=samples,repeats=reps,seconds=min(samples),
                        statistic='minimum',validation='every output checked after timer'))
    return min(samples), out


def _sa():
    metadata = load('sa')
    path = CACHE.dir / 'sa.npy'
    assert digest_bytes(path.read_bytes()) == metadata['array_sha256']
    return np.load(path, mmap_mode='r')


def compute_hook() -> dict:
    from explainer.cs.algo import strings as S
    t = _full_text()
    pat = b"Queequeg"
    expected = find_all(t, pat)
    t_naive, (pos, cmp_naive) = _best(lambda: S.naive_fast(t, pat), 1, check=lambda v: _assert(v[0] == expected), label='naive vectorized comparison instrument')
    t_kmp, (pk, cmp_kmp) = _best(lambda: S.kmp(t, pat), 1, check=lambda v: _assert(v[0] == expected), label='Python KMP search')
    t_bm, (pb, cmp_bm, win_bm) = _best(lambda: S.boyer_moore(t, pat), 1, check=lambda v: _assert(v[0] == expected), label='Python Boyer-Moore search')
    assert pos == pk == pb
    t_find, _ = _best(lambda: t.count(pat), check=lambda v: _assert(v == len(expected)), label='native bytes count for this non-self-overlapping pattern')
    f = CACHE.dir / "corpus.txt"
    f.write_bytes(t)
    t_grep, out = _best(lambda: subprocess.run(["grep", "-a", "-o", "-F", "Queequeg", str(f)],
                    capture_output=True, text=True, check=True).stdout,
                    check=lambda value: _assert(value.splitlines() == [pat.decode()] * len(expected)),
                    label='grep fixed-string matching occurrences, including process startup')
    f.unlink()
    sa = _sa()
    fm = S.FMIndex(t + b"\x00", sa)
    fm.steps = 0
    t_fm, (cnt, _) = _best(lambda: fm.count(pat), check=lambda value: _assert(value[0] == len(expected)), label='warm FM count; index build excluded')
    return {"n": len(t), "pattern": pat.decode(), "hits": len(pos), "naive_cmp": cmp_naive, "kmp_cmp": cmp_kmp,
            "bm_cmp": cmp_bm, "bm_windows": win_bm, "fm_count": cnt, "fm_ranks": 2 * len(pat), "t_kmp_py": t_kmp,
            "t_bm_py": t_bm, "t_find": t_find, "t_grep": t_grep, "t_fm": t_fm, "grep_matches": len(out.splitlines()), "grep_mode": "-a -o -F occurrence output; fixed Queequeg pattern cannot overlap itself"}


def compute_naive() -> dict:
    from explainer.cs.algo import strings as S
    t = _full_text()
    rows = []
    for p in (b"the", b"whale", b"Queequeg", b"Elizabeth Bennet", b"it was the best of times"):
        pos, cmp = S.naive_fast(t, p)
        # predicted: an alignment compares character j + 1 exactly when the first j matched
        predicted_count = naive_comparisons_reference(t, p)
        assert predicted_count == cmp and pos == find_all(t, p)
        pred = predicted_count / len(t)
        rows.append({"pattern": p.decode(), "m": len(p), "hits": len(pos), "cmp": cmp, "per_char": cmp / len(t),
                     "predicted": pred})
        print(rows[-1])
    worst = []
    for n, m in ((1000, 10), (1000, 100), (10000, 100), (100000, 1000)):
        text = b"a" * n
        pat = b"a" * (m - 1) + b"b"
        _, cmp = S.naive_fast(text, pat)
        assert cmp == (n-m+1)*m
        worst.append({"n": n, "m": m, "cmp": cmp, "nm": (n - m + 1) * m})
    return {"n": len(t), "rows": rows, "worst": worst}


def compute_rk() -> dict:
    from explainer.cs.algo import strings as S
    t = _books()["Moby Dick"]
    pat = b"Queequeg"
    rows = []
    expected_positions = find_all(t, pat)
    for mod in (101, 1009, 10007, 100003, 1_000_003, 1_000_000_007):
        t0 = time.perf_counter()
        pos, cmp, spur = S.rabin_karp(t, pat, mod=mod)
        seconds = _elapsed(t0, 'Python fixed-base rolling-hash search')
        assert pos == expected_positions
        rows.append({"mod": mod, "hits": len(pos), "spurious": spur, "expected": (len(t) - len(pat) + 1) / mod,
                     "cmp": cmp, "seconds": seconds})
        print(rows[-1])
    return {"n": len(t), "pattern": pat.decode(), "rows": rows, "base": 256,
            "heuristic_scope": "windows/modulus is a uniform-hash reference scale, not an expectation theorem for fixed base 256",
            "randomized_theorem": "prime p>255 and a base chosen uniformly in F_p: unequal equal-length byte strings collide with probability at most (m-1)/p"}


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
        expected_positions = find_all(t, p)
        t0 = time.perf_counter()
        pos, cmp = S.kmp(t, p)
        seconds = _elapsed(t0, "Python KMP search, prefix table included")
        assert pos == expected_positions and cmp <= 2*len(t)
        rows.append({"pattern": p.decode(), "hits": len(pos), "cmp": cmp, "per_char": cmp / len(t),
                     "seconds": seconds})
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
            expected_positions = find_all(t,p)
            ph, c1, _ = S.horspool(t, p)
            pb, c2, _ = S.boyer_moore(t, p)
            pk, c3 = S.kmp(t, p)
            assert ph == pb == pk == expected_positions
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
    expected = Counter({p:len(find_all(t,p)) for p in names})
    t0 = time.perf_counter()
    ac = S.AhoCorasick(names)
    hits, steps = ac.search(t)
    t_ac = _elapsed(t0, 'Aho-Corasick build plus complete search')
    assert hits == expected and len(t) <= steps <= 2*len(t)
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
    t_sa = _elapsed(t0, 'NumPy prefix-doubling full suffix array')
    CACHE.dir.mkdir(parents=True, exist_ok=True)
    np.save(CACHE.dir / "sa.npy", sa.astype(np.int32))
    # LCP by Kasai is linear but in Python too slow for 25 MB; use it on one novel, and adjacent comparisons in numpy
    md = _books()["Moby Dick"] + b"\x00"
    sa_md = S.suffix_array(md)
    t0 = time.perf_counter()
    lcp = S.lcp_kasai(md, sa_md)
    t_lcp = _elapsed(t0, 'Python Kasai LCP on Moby Dick')
    check_suffix_order(md,sa_md)
    assert len(lcp)==len(md) and lcp[0]==0 and np.all(lcp>=0)
    i = int(np.argmax(lcp))
    rep = md[sa_md[i]:sa_md[i] + int(lcp[i])]
    # Exclude all distinct substrings containing the artificial terminal byte.
    distinct = (len(md) - 1) * len(md) // 2 - int(lcp.sum())
    check_suffix_order(t, sa)
    searches = []
    for p in (b"Queequeg", b"whale", b"Call me Ishmael"):
        lo, hi, cmp = S.sa_search(t, sa, p)
        assert sorted(int(x) for x in sa[lo:hi]) == find_all(t[:-1],p)
        searches.append({"pattern": p.decode(), "count": hi - lo, "cmp": cmp, "bound": len(p) * 2 * math.log2(len(t))})
    # the first rows of the suffix array of a famous sentence, for drawing
    s = b"it was the best of times$"
    sa_s = S.suffix_array_naive(s)
    return {"n": len(t), "t_sa": t_sa, "md_n": len(md), "t_lcp": t_lcp, "md_longest_repeat": rep.decode(errors="replace"),
            "md_repeat_len": int(lcp[i]), "md_distinct_substrings": distinct, "md_mean_lcp": float(lcp.mean()),
            "searches": searches, "small": s.decode(), "small_sa": sa_s,
            "small_suffixes": [s[k:].decode() for k in sa_s], "bytes_sa": 4 * len(t), "array_sha256": digest_bytes((CACHE.dir / "sa.npy").read_bytes()), "md_text_bytes": len(md)-1, "terminal_excluded_from_substrings": True}


def compute_repeats() -> dict:
    text = _full_text() + b"\x00"
    sa = _sa()
    check_suffix_order(text, sa)
    start = time.perf_counter()
    length, at = longest_repeat_reference(text, sa)
    seconds = _elapsed(start, 'exact full-corpus adjacent suffix LCP maximum')
    assert text[at[0]:at[0]+length] == text[at[1]:at[1]+length]
    return dict(length=length,text=text[at[0]:at[0]+min(length,600)].decode(errors='replace'),at=at,
                full_repeat_sha256=digest_bytes(text[at[0]:at[0]+length]),seconds=seconds,
                method='complete adjacent suffix pairs, exact one-byte extension until first mismatch')


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
    assert L == bytes(word[(i-1)%len(word)] for i in rot) and S.inverse_bwt(L)==word
    md = _books()["Moby Dick"]
    k = md.find(b"Call me Ishmael")
    chap = md[k:k + 12000] + b"\x00"
    sa_c = S.suffix_array(chap)
    Lc = S.bwt_from_sa(chap, sa_c)
    mtf = S.move_to_front(Lc)
    assert S.inverse_bwt(Lc)==chap
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
    t_build = _elapsed(t0, 'FM index construction with plain BWT/checkpoints/samples')
    rows = []
    for p in (b"Queequeg", b"whale", b"Elizabeth", b"Mr. Darcy", b"the", b"it was the best of times",
              b"Call me Ishmael"):
        fm.steps = 0
        t1 = time.perf_counter()
        c, (lo, hi) = fm.count(p)
        tc = _elapsed(t1, 'one FM backward-count query')
        count_ranks = fm.steps
        expected = find_all(t[:-1], p)
        assert c == len(expected)
        locs = []
        t2 = time.perf_counter()
        for r in range(lo, min(hi, lo + 5)):
            locs.append(fm.locate(r))
        tl = (_elapsed(t2, 'up to five LF locates, total observation before per-occurrence division')) / max(1, len(locs))
        assert locs == [int(x) for x in sa[lo:min(hi,lo+5)]]
        assert all(x in expected and t[x:x + len(p)] == p for x in locs)
        rows.append({"pattern": p.decode(), "count": c, "ranks": count_ranks, "locate_ranks": fm.steps - count_ranks, "locations_checked": locs, "t_count": tc, "t_locate": tl})
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
            "text_bytes": len(t), "banana_trace": trace, "storage_scope": "plain BWT and actual NumPy occurrence buffers plus modeled four-byte suffix samples; excludes Python dictionary/container overhead, input text, full suffix array and construction temporaries"}


def compute_lz() -> dict:
    from explainer.cs.algo import strings as S
    books = _books()
    rows = []
    for name in ("Pride and Prejudice", "Moby Dick", "Ulysses"):
        d = books[name]
        t0 = time.perf_counter()
        tok = S.lz77(d)
        t_lz = _elapsed(t0, 'Python LZ77 tokens')
        assert S.lz77_decode(tok) == d
        sz = S.deflate_size(tok)
        codes, nd = S.lzw(d)
        assert lzw_decode_reference(codes) == d
        lzw_bits = sum(max(9, math.ceil(math.log2(256 + i + 1))) for i in range(len(codes)))
        compressed = [zlib.compress(d,9),bz2.compress(d,9),lzma.compress(d,preset=9)]
        assert all(decode(blob)==d for decode,blob in zip([zlib.decompress,bz2.decompress,lzma.decompress],compressed))
        rows.append({"book": name, "n": len(d), "ours": sz["bytes"], "zlib": len(compressed[0]),
                     "bz2": len(compressed[1]), "xz": len(compressed[2]), "lzw": lzw_bits / 8,
                     "lz_huffman_bits": sz["bits"], "lzw_bits": lzw_bits, "lz_tokens_sha256": digest_bytes(repr(tok).encode()),
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
    packed = zlib.compress(allb,6)
    zc = len(packed)
    t_z = _elapsed(t0, 'zlib level-6 full-corpus compression')
    assert zlib.decompress(packed)==allb
    assert S.lz77_decode(tok)==passage
    return {"size_scope": "ours: unconstrained Huffman token cost plus extra bits, excludes code tables/block framing and is not an emitted DEFLATE stream; LZW: growing-width bit-cost model, no clear/reset/framing; library codecs: actual complete byte streams",
            "rows": rows, "passage": passage.decode(errors="replace"), "arcs": arcs, "tokens": len(tok),
            "corpus": len(allb), "corpus_zlib": zc, "t_zlib": t_z}


def compute_entropy() -> dict:
    from explainer.cs.algo import strings as S
    d = _books()["Moby Dick"]
    sym = np.frombuffer(d, dtype=np.uint8)
    h0 = S.entropy(sym)
    frequencies = Counter(d)
    lens = S.huffman_lengths(frequencies)
    huff = sum(frequencies[s] * lens[s] for s in lens) / len(d)
    r = S.RANS(d)
    t0 = time.perf_counter()
    enc = r.encode(d)
    t_enc = _elapsed(t0, 'rANS static-model encoding; model construction excluded')
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
    assert rm.decode(enc_m,len(m))==m.tobytes()
    assert abs(huff-huffman_cost_reference(frequencies)/len(d))<1e-12
    assert abs(huff_m-huffman_cost_reference(cm)/len(m))<1e-12
    # A finite sample is coded against its quantized empirical model, not the ideal Bernoulli parameter.
    rng = np.random.default_rng(21)
    skew = []
    for p in (0.5, 0.8, 0.95, 0.99):
        src = (rng.random(200_000) < p).astype(np.uint8).tobytes()
        rs = S.RANS(src)
        e = rs.encode(src)
        assert rs.decode(e, len(src)) == src
        h = -(p * math.log2(p) + (1 - p) * math.log2(1 - p))
        empirical = S.entropy(np.frombuffer(src, dtype=np.uint8))
        skew.append({"p": p, "entropy": h, "empirical_entropy": empirical, "sample_sha256": digest_bytes(src), "huffman": 1.0, "rans": len(e) * 8 / len(src)})
    order1 = _order_k_entropy(d, 1)
    order2 = _order_k_entropy(d, 2)
    return {"model_scope": "rANS bytes include terminal state; frequency table and output length are external metadata. Huffman numbers are payload bit costs excluding code tables. Empirical entropies are benchmarks, not complete-file lower bounds.",
            "n": len(d), "h0": h0, "huffman": huff, "rans": len(enc) * 8 / len(d), "t_rans": t_enc,
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
    assert i1 >= 40 and i2 >= 40, "both repeated letters must actually exist"
    x = mc[i1 - 40:i1 + 260]
    y = mc[i2 - 40:i2 + 260]
    t0 = time.perf_counter()
    best, end, start, H = S.smith_waterman(x, y)
    t_sw = _elapsed(t0, 'Smith-Waterman complete 300-by-300 table')
    reference = alignment_reference(x,y,local=True)
    assert H.tolist()==reference and best==max(map(max,reference))
    assert nw.tolist()==alignment_reference(a,b)
    assert 0<=start[0]<=end[0]<=len(x) and 0<=start[1]<=end[1]<=len(y)
    return {"nw_a": a, "nw_b": b, "nw": nw.tolist(), "nw_score": int(nw[-1, -1]), "sw_x": x, "sw_y": y,
            "sw_best": best, "sw_end": list(end), "sw_start": list(start),
            "sw_x_part": x[start[0]:end[0]], "sw_y_part": y[start[1]:end[1]], "cells": len(x) * len(y),
            "t_sw": t_sw, "found": i1 >= 0 and i2 >= 0}


def compute_diff() -> dict:
    from explainer.cs.algo import strings as S
    path = "videos/cs/SYLLABUS.md"
    history = history_snapshot(ROOT, path)
    revs = [row['commit'] for row in history]
    contents = {row['commit']: row['raw'].decode() for row in history}
    rows = []
    prev = pph = None
    for h in revs:
        cur = contents[h]
        cur = cur.split("\n")
        if cur and cur[-1] == "":
            cur.pop()
        if prev is not None:
            t0 = time.perf_counter()
            D, ops, trace, snake = S.myers(prev, cur)
            tm = _elapsed(t0, 'Myers edit script on adjacent full-ID revisions')
            num = subprocess.run(["git", "diff", "--numstat", "--minimal", pph, h, "--", path], cwd=ROOT,
                                 capture_output=True, text=True, check=True).stdout.split()
            g = int(num[0]) + int(num[1]) if num else 0
            minimal = D == len(prev) + len(cur) - 2 * S.lcs_len(prev, cur)
            assert minimal and [x for op,x in ops if op != "+"] == prev and [x for op,x in ops if op != "-"] == cur
            rows.append({"previous_rev": pph, "rev": h, "n": len(prev), "m": len(cur), "D": D, "git": g, "snake": snake, "seconds": tm,
                         "nd": (len(prev) + len(cur)) * D, "minimal": minimal})
        prev, pph = cur, h
    # a small example for the edit graph
    a, b = list("ABCABBA"), list("CBABAC")
    D, ops, trace, _ = S.myers(a, b)
    return {"history": [{k:v for k,v in row.items() if k != "raw"} for row in history], "path": path, "revisions": len(revs), "rows": rows, "ex_a": "".join(a), "ex_b": "".join(b), "ex_D": D,
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
    hash_new = [k for k,h in enumerate(hn) if h not in so]
    new_chunks = exact_chunk_reuse(d,cuts_o,edited,cuts_n)
    assert hash_new==new_chunks, "unexpected truncated-digest collision; use full bytes as the reference"
    assert matched*B+literal==len(edited)
    sizes = np.diff([0] + cuts_o)
    return {"chunk_equality": "all reuse decisions checked by exact chunk bytes; digest collision check retained",
            "n": len(d), "insert": len(edited)-len(d), "block": B, "fixed_blocks": len(fixed_new), "fixed_reused": fixed_reused,
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
    t_m = _elapsed(t0, 'Manacher all radii on normalized letters')
    st, ln = 0, 0
    for k in np.flatnonzero(np.asarray(rad) >= 12):     # the longest palindrome with at least four letters in it
        r = rad[k]
        cand = letters[(k - r) // 2:(k - r) // 2 + r]
        if len(set(cand)) >= 4 and r > ln:
            st, ln = (k - r) // 2, r
    pal = letters[st:st + ln].decode()
    assert len(set(pal))>=4 and pal==pal[::-1] and len(pal)==ln
    per = {w: S.periods(w.encode()) for w in ("abaababaab", "abcabcab", "aaaa", "tatatat")}
    lyn = {w: S.duval(w) for w in ("banana", "mississippi", "abracadabra")}
    # repetitiveness: the suffix-array runs r for ordinary text against versions of one file
    path = "videos/cs/SYLLABUS.md"
    history = history_snapshot(ROOT, path)[::-1]
    revs = [row['commit'] for row in history]
    vers = b"".join(row['raw'] for row in history) + b"\x00"
    Lv = S.bwt_from_sa(vers, S.suffix_array(vers))
    novel = t[:len(vers) - 1] + b"\x00"
    Ln = S.bwt_from_sa(novel, S.suffix_array(novel))
    return {"history": [{k:v for k,v in row.items() if k != "raw"} for row in history], "history_order": "reverse chronological git traversal, literal concatenation followed by one sentinel", "palindrome": pal, "pal_len": ln, "t_manacher": t_m, "scanned": len(letters),
            "where": t.lower().find(pal[:12].encode()) if False else None,
            "periods": per, "lyndon": lyn, "versions": len(revs), "vers_n": len(vers), "history_bytes_sha256": digest_bytes(vers), "novel_prefix_sha256": digest_bytes(novel), "vers_runs": S.runs(Lv),
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



def _validate_payload(name, data):
    from explainer.cs.algo import strings as S
    if name == 'hook':
        assert data['hits'] == data['fm_count'] == data['grep_matches']
    elif name == 'naive':
        assert all(r['predicted']==r['per_char'] for r in data['rows'])
        assert all(r['cmp']==r['nm'] for r in data['worst'])
    elif name == 'rk':
        assert all(r['hits']==len(find_all(_books()['Moby Dick'],data['pattern'].encode())) for r in data['rows'])
        assert data['base']==256 and data['heuristic_scope']
    elif name == 'kmp':
        assert all(fail==border_reference(pat.encode()) for pat,fail in data['fails'].items())
        assert data['worst_cmp']<=2*data['worst_n']
    elif name == 'bm':
        assert len(data['rows'])==6 and all(r['kmp']<=2 for r in data['rows'])
    elif name == 'ac':
        assert data['patterns']==45 and data['separate_reads']==data['patterns']*data['n']
        assert data['n']<=data['steps']<=2*data['n']
    elif name == 'sa':
        assert data['terminal_excluded_from_substrings']
        assert digest_bytes((CACHE.dir/'sa.npy').read_bytes())==data['array_sha256']
        assert all(r['count']==len(find_all(_full_text(),r['pattern'].encode())) for r in data['searches'])
    elif name == 'repeats':
        text=_full_text()+b'\0';a,b=data['at'];n=data['length']
        assert a!=b and text[a:a+n]==text[b:b+n] and digest_bytes(text[a:a+n])==data['full_repeat_sha256']
    elif name == 'stree':
        assert data['word']=='banana$' and len([e for e in data['edges'] if e[3] is not None])==7
    elif name == 'bwt':
        assert data['inverse_ok'] and data['L']=='annb$aa' and 0<=data['mtf_zero_share']<=1
    elif name == 'fm':
        assert all(r['count']==len(find_all(_full_text(),r['pattern'].encode())) for r in data['rows'])
        assert data['banana_trace']==[['a',1,4],['n',5,7],['a',2,4]] and data['storage_scope']
    elif name == 'lz':
        assert data['size_scope'] and all(r['matches']+r['literals']>0 and r['lz_huffman_bits']>0 for r in data['rows'])
    elif name == 'entropy':
        assert data['model_scope'] and all(0<=r['empirical_entropy']<=1 for r in data['skew'])
        assert data['h0']<=data['huffman']<data['h0']+1
    elif name == 'align':
        assert data['found'] and data['cells']==len(data['sw_x'])*len(data['sw_y'])
    elif name == 'diff':
        assert all(r['minimal'] for r in data['rows']) and len(data['history'])==data['revisions']==len(data['rows'])+1
    elif name == 'rsync':
        assert data['rsync_matched']*data['block']+data['rsync_literal']==data['n']+data['insert']
        assert sum(data['cdc_sizes_old'])==data['n'] and sum(data['cdc_sizes_new'])==data['n']+data['insert']
    elif name == 'period':
        assert len(data['history'])==data['versions'] and data['palindrome']==data['palindrome'][::-1]
        assert all(S.periods(w.encode())==[k for k in range(1,len(w)+1) if w[k:]==w[:-k]] for w in data['periods'])
        assert all(''.join(parts)==w and all(parts[i]>=parts[i+1] for i in range(len(parts)-1)) for w,parts in data['lyndon'].items())
    else:
        raise AssertionError('unvalidated producer '+name)
    return True


def _checked_producer(name, function):
    @functools.wraps(function)
    def checked():
        global _TRIALS
        previous = _TRIALS
        _TRIALS = []
        try:
            data = function()
            assert _validate_payload(name,data)
            data.update(schema=SCHEMAS[name],protocol=protocol(),timed_trials=list(_TRIALS),
                        validation='producer invariants and independent references checked outside timers',
                        corpus_sha256=digest_bytes(_full_text()))
            return data
        finally:
            _TRIALS = previous
    return checked

ITEMS = {k[8:]: _checked_producer(k[8:],v) for k,v in list(globals().items()) if k.startswith("compute_")}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
