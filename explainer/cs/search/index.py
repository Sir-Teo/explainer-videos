"""The inverted index (Part 47): postings with positions built from the novels' passages; Boolean intersection by
linear merge, with skip pointers every sqrt(n), and by galloping (exponential) search, each counting comparisons;
phrase queries over positions; and postings compressed as gaps with variable-byte, Elias gamma and delta, and
Golomb-Rice codes."""

from __future__ import annotations

import math
from collections import defaultdict

from explainer.cs.search import text as T


def build(docs, stem=True, stop=False):
    """term -> list of (doc id, [positions]); also document lengths."""
    post = defaultdict(list)
    lengths = []
    for did, _, txt in docs:
        toks = T.tokens(txt)
        lengths.append(len(toks))
        pos = defaultdict(list)
        for i, t in enumerate(toks):
            if stop and t in T.STOP:
                continue
            pos[T.porter(t) if stem else t].append(i)
        for t, ps in pos.items():
            post[t].append((did, ps))
    return dict(post), lengths


def docs_of(post, term):
    return [d for d, _ in post.get(term, [])]


# ---------------------------------------------------------------- intersection

def merge(a, b):
    i = j = c = 0
    out = []
    while i < len(a) and j < len(b):
        c += 1
        if a[i] == b[j]:
            out.append(a[i])
            i += 1
            j += 1
        elif a[i] < b[j]:
            i += 1
        else:
            j += 1
    return out, c


def skips(a, b):
    """Linear merge, but either list may jump sqrt(n) ahead when the skip target is still not past the other."""
    sa, sb = max(1, int(math.sqrt(len(a)))), max(1, int(math.sqrt(len(b))))
    i = j = c = 0
    out = []
    while i < len(a) and j < len(b):
        c += 1
        if a[i] == b[j]:
            out.append(a[i])
            i += 1
            j += 1
        elif a[i] < b[j]:
            if i % sa == 0 and i + sa < len(a):
                c += 1
                if a[i + sa] <= b[j]:
                    i += sa
                    continue
            i += 1
        else:
            if j % sb == 0 and j + sb < len(b):
                c += 1
                if b[j + sb] <= a[i]:
                    j += sb
                    continue
            j += 1
    return out, c


def gallop(a, b):
    """For each element of the shorter list, find it in the longer by doubling steps then binary search: about
    m log(n/m) comparisons."""
    if len(a) > len(b):
        a, b = b, a
    out, c, lo = [], 0, 0
    for x in a:
        step, hi = 1, lo
        while hi < len(b) and b[hi] < x:
            c += 1
            lo = hi + 1
            hi = lo + step
            step *= 2
        hi = min(hi, len(b))
        l, r = lo, hi
        while l < r:
            c += 1
            m = (l + r) // 2
            if b[m] < x:
                l = m + 1
            else:
                r = m
        lo = l
        if lo < len(b):
            c += 1
            if b[lo] == x:
                out.append(x)
    return out, c


def intersect_experiment(post, pairs):
    rows = []
    for t1, t2 in pairs:
        a, b = docs_of(post, t1), docs_of(post, t2)
        m, cm = merge(a, b)
        s, cs = skips(a, b)
        g, cg = gallop(a, b)
        assert m == s == g
        rows.append({"terms": (t1, t2), "sizes": (len(a), len(b)), "hits": len(m), "merge": cm, "skips": cs,
                     "gallop": cg})
    return rows


def phrase(post, words):
    """Documents containing the words consecutively."""
    terms = [T.porter(w) for w in words]
    lists = [dict(post.get(t, [])) for t in terms]
    common = set(lists[0])
    for L in lists[1:]:
        common &= set(L)
    out = []
    for d in sorted(common):
        starts = set(lists[0][d])
        for k, L in enumerate(lists[1:], 1):
            starts &= {p - k for p in L[d]}
        if starts:
            out.append((d, sorted(starts)))
    return out


# ---------------------------------------------------------------- compression

def vbyte_bits(g):
    return 8 * max(1, math.ceil(g.bit_length() / 7))


def gamma_bits(g):
    return 2 * int(math.log2(g)) + 1


def delta_bits(g):
    n = int(math.log2(g)) + 1
    return n - 1 + gamma_bits(n)


def rice_bits(g, k):
    return ((g - 1) >> k) + 1 + k


def gamma_code(g):
    b = bin(g)[2:]
    return "0" * (len(b) - 1) + b


def delta_code(g):
    b = bin(g)[2:]
    return gamma_code(len(b)) + b[1:]


def rice_code(g, k):
    q, r = (g - 1) >> k, (g - 1) & ((1 << k) - 1)
    return "1" * q + "0" + (format(r, f"0{k}b") if k else "")


def compress(post, n_docs):
    """Total size of all doc-id postings under each code, with gaps (first id + 1, then differences).  Rice uses
    the parameter k = floor(log2(0.69 * mean gap)) per list, the Golomb optimum for geometric gaps."""
    tot = {"raw32": 0, "vbyte": 0, "gamma": 0, "delta": 0, "rice": 0}
    postings = 0
    for t, ps in post.items():
        ids = [d for d, _ in ps]
        gaps = [ids[0] + 1] + [b - a for a, b in zip(ids, ids[1:])]
        postings += len(gaps)
        tot["raw32"] += 32 * len(gaps)
        tot["vbyte"] += sum(vbyte_bits(g) for g in gaps)
        tot["gamma"] += sum(gamma_bits(g) for g in gaps)
        tot["delta"] += sum(delta_bits(g) for g in gaps)
        mean = n_docs / len(gaps)
        k = max(0, int(math.log2(max(1.0, 0.69 * mean))))
        tot["rice"] += sum(rice_bits(g, k) for g in gaps)
    return {"postings": postings, "bits": tot, "bits_per_posting": {k: v / postings for k, v in tot.items()}}
