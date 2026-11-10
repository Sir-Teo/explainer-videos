"""Strings (Part 21): matchers that count their comparisons, suffix structures, the BWT and FM-index, compressors,
alignment, Myers' diff, rolling hashes and chunking, and periodicity.

Every matcher returns (positions, work) so the scenes can compare them on the novels; the suffix array is built by
prefix doubling in numpy, fast enough for the whole 25 MB corpus.
"""

from __future__ import annotations

import heapq
import operator
from array import array
import math
from collections import Counter, deque

import numpy as np



def _integer(value, name, minimum=0, maximum=None):
    if isinstance(value, (bool, np.bool_)):
        raise ValueError(f"{name} must be an integer")
    try:
        result = operator.index(value)
    except TypeError as exc:
        raise ValueError(f"{name} must be an integer") from exc
    if result < minimum or (maximum is not None and result > maximum):
        raise ValueError(f"{name} is outside its supported range")
    return result


def _suffix_order(text, sa):
    """Check a complete suffix order by first symbols and inverse ranks of tails."""
    n = len(text)
    a = np.asarray(sa)
    if a.ndim != 1 or len(a) != n or a.dtype.kind not in 'iu':
        raise ValueError("suffix array must contain one integer per text position")
    a = a.astype(np.int64, copy=False)
    if not n:
        return a
    if a.min() < 0 or a.max() >= n:
        raise ValueError("suffix index outside text")
    rank = np.full(n + 1, -1, dtype=np.int64)
    rank[a] = np.arange(n)
    if np.any(rank[:n] < 0):
        raise ValueError("suffix array must be a permutation")
    t = np.frombuffer(text, dtype=np.uint8)
    first = t[a]
    if np.any((first[1:] < first[:-1]) | ((first[1:] == first[:-1]) & (rank[a[1:] + 1] <= rank[a[:-1] + 1]))):
        raise ValueError("suffix array is not lexicographically sorted")
    return a


def _terminal(text):
    if not text or text.count(text[-1:]) != 1 or min(text) != text[-1]:
        raise ValueError("text must end with a unique smallest sentinel")
    return text[-1]


# ------------------------------------------------------------------------------------------------- matching
def naive(text: bytes, pat: bytes):
    """Try every alignment, comparing left to right until a mismatch."""
    n, m = len(text), len(pat)
    out, cmp = [], 0
    for i in range(n - m + 1):
        j = 0
        while j < m:
            cmp += 1
            if text[i + j] != pat[j]:
                break
            j += 1
        if j == m:
            out.append(i)
    return out, cmp


def naive_fast(text: bytes, pat: bytes):
    """The same comparison count as ``naive``, computed with numpy (for megabytes of text): at each alignment, the
    number of characters compared is the length of the common prefix plus one (or m on a match)."""
    t = np.frombuffer(text, dtype=np.uint8)
    n, m = len(t), len(pat)
    if m > n:
        return [], 0
    N = n - m + 1
    alive = np.ones(N, dtype=bool)
    cmp = 0
    for j in range(m):
        cmp += int(alive.sum())
        alive &= t[j:j + N] == pat[j]
    return np.flatnonzero(alive).tolist(), cmp


def rabin_karp(text: bytes, pat: bytes, base: int = 256, mod: int = 1_000_000_007):
    """Rolling hash: compare characters only when the window's hash matches.  Returns (positions, character
    comparisons, spurious hash hits)."""
    base = _integer(base, "base", 1)
    mod = _integer(mod, "modulus", 2)
    n, m = len(text), len(pat)
    if not m:
        return list(range(n + 1)), 0, 0
    if m > n:
        return [], 0, 0
    hp = ht = 0
    for k in range(m):
        hp = (hp * base + pat[k]) % mod
        ht = (ht * base + text[k]) % mod
    top = pow(base, m - 1, mod)
    out, cmp, spurious = [], 0, 0
    for i in range(n - m + 1):
        if ht == hp:
            j = 0
            while j < m:
                cmp += 1
                if text[i + j] != pat[j]:
                    break
                j += 1
            if j == m:
                out.append(i)
            else:
                spurious += 1
        if i + m < n:
            ht = ((ht - text[i] * top) * base + text[i + m]) % mod
    return out, cmp, spurious


def kmp_failure(pat: bytes):
    """fail[j] = length of the longest proper border of pat[:j+1]."""
    m = len(pat)
    fail = [0] * m
    k = 0
    for j in range(1, m):
        while k and pat[j] != pat[k]:
            k = fail[k - 1]
        if pat[j] == pat[k]:
            k += 1
        fail[j] = k
    return fail


def kmp(text: bytes, pat: bytes):
    if not pat:
        return list(range(len(text) + 1)), 0
    fail = kmp_failure(pat)
    m = len(pat)
    out, cmp, j = [], 0, 0
    for i, c in enumerate(text):
        while True:
            cmp += 1
            if c == pat[j]:
                j += 1
                break
            if j == 0:
                break
            j = fail[j - 1]
        if j == m:
            out.append(i - m + 1)
            j = fail[j - 1]
    return out, cmp


def kmp_automaton(pat: bytes, alphabet: bytes):
    """The DFA of Part 12 built from the failure function: delta[state][c]."""
    m = len(pat)
    fail = kmp_failure(pat)
    delta = [{} for _ in range(m + 1)]
    for q in range(m + 1):
        for c in alphabet:
            if q < m and c == pat[q]:
                delta[q][c] = q + 1
            elif q == 0:
                delta[q][c] = 0
            else:
                delta[q][c] = delta[fail[q - 1]][c]
    return delta


def horspool(text: bytes, pat: bytes):
    """Boyer-Moore-Horspool: compare right to left; on a mismatch shift by the bad-character rule applied to the
    window's last character."""
    n, m = len(text), len(pat)
    if not m:
        return list(range(n + 1)), 0, n + 1
    shift = {c: m - 1 - k for k, c in enumerate(pat[:-1])}
    out, cmp, i, windows = [], 0, 0, 0
    while i <= n - m:
        windows += 1
        j = m - 1
        while j >= 0:
            cmp += 1
            if text[i + j] != pat[j]:
                break
            j -= 1
        if j < 0:
            out.append(i)
        i += shift.get(text[i + m - 1], m)
    return out, cmp, windows


def good_suffix(pat: bytes):
    """The strong good-suffix shifts (Knuth, Morris and Pratt's correction to Boyer and Moore)."""
    m = len(pat)
    shift = [0] * (m + 1)
    border = [0] * (m + 1)
    i, j = m, m + 1
    border[i] = j
    while i > 0:
        while j <= m and pat[i - 1] != pat[j - 1]:
            if shift[j] == 0:
                shift[j] = j - i
            j = border[j]
        i -= 1
        j -= 1
        border[i] = j
    j = border[0]
    for i in range(m + 1):
        if shift[i] == 0:
            shift[i] = j
        if i == j:
            j = border[j]
    return shift


def boyer_moore(text: bytes, pat: bytes):
    """Both rules: shift by the larger of the bad-character and good-suffix shifts."""
    n, m = len(text), len(pat)
    last = {c: k for k, c in enumerate(pat)}
    gs = good_suffix(pat)
    out, cmp, i, windows = [], 0, 0, 0
    while i <= n - m:
        windows += 1
        j = m - 1
        while j >= 0:
            cmp += 1
            if text[i + j] != pat[j]:
                break
            j -= 1
        if j < 0:
            out.append(i)
            i += gs[0]
        else:
            i += max(gs[j + 1], j - last.get(text[i + j], -1))
    return out, cmp, windows


class AhoCorasick:
    """A trie of the patterns with failure links (and output links): one pass finds every occurrence of every
    pattern."""

    def __init__(self, patterns):
        self.goto = [{}]
        self.fail = [0]
        self.out = [[]]
        for p in patterns:
            if not p:
                raise ValueError("Aho-Corasick patterns must be nonempty")
            s = 0
            for c in p:
                if c not in self.goto[s]:
                    self.goto.append({})
                    self.fail.append(0)
                    self.out.append([])
                    self.goto[s][c] = len(self.goto) - 1
                s = self.goto[s][c]
            self.out[s].append(p)
        q = deque(self.goto[0].values())
        while q:
            s = q.popleft()
            for c, t in self.goto[s].items():
                q.append(t)
                f = self.fail[s]
                while f and c not in self.goto[f]:
                    f = self.fail[f]
                self.fail[t] = self.goto[f].get(c, 0) if self.goto[f].get(c, 0) != t else 0
                self.out[t] = self.out[t] + self.out[self.fail[t]]

    def search(self, text: bytes):
        s, hits, steps = 0, Counter(), 0
        for c in text:
            while s and c not in self.goto[s]:
                s = self.fail[s]
                steps += 1
            s = self.goto[s].get(c, 0)
            steps += 1
            for p in self.out[s]:
                hits[p] += 1
        return hits, steps

    @property
    def states(self):
        return len(self.goto)


# ------------------------------------------------------------------------------------------------- suffix structures
def suffix_array(text: bytes) -> np.ndarray:
    """Prefix doubling (Manber and Myers 1990), with numpy sorts: ranks by the first k characters, then 2k."""
    t = np.frombuffer(text, dtype=np.uint8).astype(np.int64)
    n = len(t)
    if not n:
        return np.empty(0, dtype=np.int64)
    rank = t.copy()
    k = 1
    sa = np.argsort(rank, kind="stable")
    while True:
        second = np.full(n, -1, dtype=np.int64)
        second[:n - k] = rank[k:]
        key = rank * (int(rank.max()) + 2) + (second + 1)
        sa = np.argsort(key, kind="stable")
        ks = key[sa]
        new = np.empty(n, dtype=np.int64)
        new[sa] = np.concatenate([[0], np.cumsum(ks[1:] != ks[:-1])])
        rank = new
        if rank.max() == n - 1:
            return sa.astype(np.int64)
        k *= 2


def suffix_array_naive(text: bytes):
    return sorted(range(len(text)), key=lambda i: text[i:])


def lcp_kasai(text: bytes, sa) -> np.ndarray:
    """lcp[i] = longest common prefix of the suffixes sa[i-1] and sa[i] (Kasai et al. 2001), in linear time."""
    n = len(text)
    sa = _suffix_order(text, sa)
    rank = np.empty(n, dtype=np.int64)
    rank[np.asarray(sa)] = np.arange(n)
    lcp = np.zeros(n, dtype=np.int64)
    h = 0
    sa = list(sa)
    rk = rank.tolist()
    for i in range(n):
        r = rk[i]
        if r > 0:
            j = sa[r - 1]
            while i + h < n and j + h < n and text[i + h] == text[j + h]:
                h += 1
            lcp[r] = h
            if h:
                h -= 1
        else:
            h = 0
    return lcp


def sa_search(text: bytes, sa, pat: bytes):
    """Binary search for the block of suffixes that start with pat: (lo, hi, character comparisons)."""
    n, m = len(text), len(pat)
    cmp = [0]

    def less(i):          # is text[i:] < pat (on the first m characters)?
        for k in range(m):
            cmp[0] += 1
            if i + k >= n:
                return True
            a, b = text[i + k], pat[k]
            if a != b:
                return a < b
        return False

    def leq(i):           # is text[i:i+m] <= pat?
        for k in range(m):
            cmp[0] += 1
            if i + k >= n:
                return True
            a, b = text[i + k], pat[k]
            if a != b:
                return a < b
        return True
    lo, hi = 0, n
    while lo < hi:
        mid = (lo + hi) // 2
        if less(int(sa[mid])):
            lo = mid + 1
        else:
            hi = mid
    a = lo
    hi = n
    while lo < hi:
        mid = (lo + hi) // 2
        if leq(int(sa[mid])):
            lo = mid + 1
        else:
            hi = mid
    return a, lo, cmp[0]


def suffix_tree_edges(text: str):
    """A suffix tree for a short string (with '$'), built from the suffix array and LCP array: a list of
    (parent depth, child depth, edge label, leaf suffix or None) in DFS order, for drawing."""
    if not text or text[-1] in text[:-1]:
        raise ValueError("suffix tree needs a unique terminal character")
    t = text
    sa = suffix_array_naive(t)
    lcp = [0] + [len(_common(t[sa[i - 1]:], t[sa[i]:])) for i in range(1, len(sa))]
    # build by the standard stack algorithm
    nodes = [{"depth": 0, "children": [], "leaf": None, "start": 0}]
    stack = [0]
    for i, s in enumerate(sa):
        h = lcp[i]
        last = None
        while nodes[stack[-1]]["depth"] > h:
            last = stack.pop()
        if nodes[stack[-1]]["depth"] < h:
            mid = {"depth": h, "children": [], "leaf": None, "start": nodes[last]["start"]}
            nodes.append(mid)
            mi = len(nodes) - 1
            nodes[stack[-1]]["children"].remove(last)
            nodes[stack[-1]]["children"].append(mi)
            mid["children"].append(last)
            stack.append(mi)
        leaf = {"depth": len(t) - s, "children": [], "leaf": s, "start": s}
        nodes.append(leaf)
        nodes[stack[-1]]["children"].append(len(nodes) - 1)
        stack.append(len(nodes) - 1)
    edges = []

    def walk(v):
        for c in nodes[v]["children"]:
            pd, cd = nodes[v]["depth"], nodes[c]["depth"]
            st = nodes[c]["start"]
            edges.append((v, c, text[st + pd:st + cd], nodes[c]["leaf"]))
            walk(c)
    walk(0)
    return edges, len(nodes)


def _common(a, b):
    k = 0
    while k < len(a) and k < len(b) and a[k] == b[k]:
        k += 1
    return a[:k]


# ------------------------------------------------------------------------------------------------- BWT and FM-index
def bwt_from_sa(text: bytes, sa) -> bytes:
    """text must end with a unique smallest sentinel; L[i] = text[sa[i] - 1]."""
    _terminal(text)
    sa = _suffix_order(text, sa)
    t = np.frombuffer(text, dtype=np.uint8)
    return t[(np.asarray(sa) - 1) % len(t)].tobytes()


def inverse_bwt(L: bytes, sentinel: int = 0) -> bytes:
    """The LF mapping: the i-th occurrence of c in L is the i-th occurrence of c in F."""
    sentinel = _integer(sentinel, "sentinel", 0, 255)
    if not L or L.count(bytes([sentinel])) != 1 or min(L) != sentinel:
        raise ValueError("BWT needs a unique smallest sentinel")
    n = len(L)
    Lc = np.frombuffer(L, dtype=np.uint8)
    order = np.argsort(Lc, kind="stable")          # F position -> L position
    lf = np.empty(n, dtype=np.int64)
    lf[order] = np.arange(n)                        # L position -> F position
    out = bytearray(n)
    i = int(np.flatnonzero(Lc == sentinel)[0])      # the row that ends with the sentinel is the text itself
    visited = np.zeros(n, dtype=bool)
    for k in range(n - 1, -1, -1):
        if visited[i]:
            raise ValueError("BWT LF mapping is not a single cycle")
        visited[i] = True
        out[k] = L[i]
        i = lf[i]
    return bytes(out)


class FMIndex:
    """Count and locate by backward search over the BWT, with occurrence counts sampled every ``step`` rows and the
    suffix array sampled every ``sa_step`` text positions."""

    def __init__(self, text: bytes, sa, step: int = 64, sa_step: int = 32):
        step = _integer(step, "rank step", 1)
        sa_step = _integer(sa_step, "suffix sampling step", 1)
        self.sentinel = _terminal(text)
        self.n = len(text)
        self.L = np.frombuffer(bwt_from_sa(text, sa), dtype=np.uint8)
        counts = np.bincount(self.L, minlength=256)
        self.C = np.concatenate([[0], np.cumsum(counts)[:-1]])
        self.step = step
        chars = np.flatnonzero(counts)
        self.chars = chars
        self.occ = {}
        for c in chars.tolist():
            cs = np.concatenate([[0], np.cumsum(self.L == c, dtype=np.int64)])
            self.occ[c] = cs[::step].astype(np.int32 if self.n < 2**31 else np.int64)
        sa = np.asarray(sa)
        keep = sa % sa_step == 0
        self.sa_rows = {int(r): int(p) for r, p in zip(np.flatnonzero(keep), sa[keep])}
        self.sa_step = sa_step
        self.steps = 0

    def rank(self, c: int, i: int) -> int:
        """Occurrences of c in L[0:i]."""
        c = _integer(c, "byte", 0, 255)
        i = _integer(i, "rank endpoint", 0, self.n)
        self.steps += 1
        if c not in self.occ:
            return 0
        b = i // self.step
        return int(self.occ[c][b]) + int(np.count_nonzero(self.L[b * self.step:i] == c))

    def count(self, pat: bytes):
        if self.sentinel in pat:
            raise ValueError("query patterns must exclude the terminal sentinel")
        lo, hi = 0, self.n
        for c in reversed(pat):
            if c not in self.occ:
                return 0, (0, 0)
            lo = int(self.C[c]) + self.rank(c, lo)
            hi = int(self.C[c]) + self.rank(c, hi)
            if lo >= hi:
                return 0, (lo, hi)
        return hi - lo, (lo, hi)

    def locate(self, row: int) -> int:
        row = _integer(row, "suffix row", 0, self.n - 1)
        k = 0
        while row not in self.sa_rows:
            if k >= self.sa_step:
                raise ValueError("LF walk failed to reach its suffix sample")
            c = int(self.L[row])
            row = int(self.C[c]) + self.rank(c, row)
            k += 1
        return self.sa_rows[row] + k

    def bytes_used(self, bits_per_char: float = 8.0) -> dict:
        return {"bwt": self.n * bits_per_char / 8, "occ": sum(4 * len(v) for v in self.occ.values()),
                "sa": len(self.sa_rows) * 4}


def runs(b: bytes) -> int:
    a = np.frombuffer(b, dtype=np.uint8)
    return int(1 + np.count_nonzero(a[1:] != a[:-1])) if len(a) else 0


def move_to_front(b: bytes) -> np.ndarray:
    table = list(range(256))
    out = np.empty(len(b), dtype=np.uint8)
    for i, c in enumerate(b):
        k = table.index(c)
        out[i] = k
        if k:
            table.pop(k)
            table.insert(0, c)
    return out


def entropy(symbols) -> float:
    """Zeroth-order empirical entropy in bits per symbol."""
    values = np.asarray(symbols)
    if not values.size:
        return 0.0
    if values.dtype.kind not in "iu" or values.min() < 0:
        raise ValueError("entropy symbols must be nonnegative integers")
    c = np.bincount(values.astype(np.int64, copy=False))
    p = c[c > 0] / c.sum()
    return float(-(p * np.log2(p)).sum())


# ------------------------------------------------------------------------------------------------- compression
def lz77(data: bytes, window: int = 32768, max_len: int = 258, min_len: int = 3, chain: int = 32):
    """Greedy LZ77 with hash chains on 3-byte prefixes (DEFLATE's limits).  Tokens: ints (literals) or (length,
    distance) pairs."""
    window = _integer(window, "window", 1, 32768)
    max_len = _integer(max_len, "maximum match length", 3, 258)
    min_len = _integer(min_len, "minimum match length", 3, max_len)
    chain = _integer(chain, "chain budget", 1)
    n = len(data)
    head: dict = {}
    prev = [0] * n
    out = []
    i = 0
    while i < n:
        best_len, best_dist = 0, 0
        if i + min_len <= n:
            key = data[i:i + 3]
            j = head.get(key, -1)
            tries = 0
            while j >= 0 and i - j <= window and tries < chain:
                if data[j + best_len:j + best_len + 1] == data[i + best_len:i + best_len + 1]:
                    k = 0
                    while k < max_len and i + k < n and data[j + k] == data[i + k]:
                        k += 1
                    if k > best_len:
                        best_len, best_dist = k, i - j
                        if k == max_len:
                            break
                tries += 1
                j = prev[j] if prev[j] != j else -1
        step = best_len if best_len >= min_len else 1
        for p in range(i, min(i + step, n - 2)):
            key = data[p:p + 3]
            prev[p] = head.get(key, p)
            head[key] = p
        if best_len >= min_len:
            out.append((best_len, best_dist))
        else:
            out.append(data[i])
        i += step
    return out


def lz77_decode(tokens) -> bytes:
    out = bytearray()
    for t in tokens:
        if isinstance(t, int):
            out.append(t)
        else:
            L, D = t
            L = _integer(L, "match length", 1)
            D = _integer(D, "match distance", 1, len(out))
            s = len(out) - D
            for k in range(L):
                out.append(out[s + k])
    return bytes(out)


def huffman_lengths(freq: dict) -> dict:
    """Code lengths of a Huffman code for the given frequencies."""
    if len(freq) == 1:
        return {next(iter(freq)): 1}
    h = [(f, i, (s,)) for i, (s, f) in enumerate(freq.items())]
    heapq.heapify(h)
    depth = Counter()
    k = len(h)
    while len(h) > 1:
        f1, _, a = heapq.heappop(h)
        f2, _, b = heapq.heappop(h)
        for s in a + b:
            depth[s] += 1
        heapq.heappush(h, (f1 + f2, k, a + b))
        k += 1
    return dict(depth)


# DEFLATE's length and distance buckets: (base, extra bits)
LEN_BASE = [3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 15, 17, 19, 23, 27, 31, 35, 43, 51, 59, 67, 83, 99, 115, 131, 163, 195,
            227, 258]
LEN_EXTRA = [0] * 8 + [1] * 4 + [2] * 4 + [3] * 4 + [4] * 4 + [5] * 4 + [0]
DIST_BASE = [1, 2, 3, 4, 5, 7, 9, 13, 17, 25, 33, 49, 65, 97, 129, 193, 257, 385, 513, 769, 1025, 1537, 2049, 3073,
             4097, 6145, 8193, 12289, 16385, 24577]
DIST_EXTRA = [0, 0, 0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 10, 10, 11, 11, 12, 12, 13, 13]


def _bucket(v, bases):
    lo, hi = 0, len(bases) - 1
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if bases[mid] <= v:
            lo = mid
        else:
            hi = mid - 1
    return lo


def deflate_size(tokens) -> dict:
    """Bits for the tokens under one static-per-file pair of Huffman codes, as DEFLATE's dynamic block would use
    (code-table overhead ignored): literal/length alphabet 0-285, distances 0-29, plus extra bits."""
    ll, dd, extra = Counter(), Counter(), 0
    for t in tokens:
        if isinstance(t, int):
            ll[t] += 1
        else:
            L, D = t
            L = _integer(L, "DEFLATE length", 3, 258)
            D = _integer(D, "DEFLATE distance", 1, 32768)
            b = _bucket(L, LEN_BASE)
            ll[257 + b] += 1
            extra += LEN_EXTRA[b]
            c = _bucket(D, DIST_BASE)
            dd[c] += 1
            extra += DIST_EXTRA[c]
    ll[256] += 1
    lla = huffman_lengths(ll)
    bits = sum(ll[s] * lla[s] for s in ll) + extra
    if dd:
        dla = huffman_lengths(dd)
        bits += sum(dd[s] * dla[s] for s in dd)
    return {"bits": bits, "bytes": bits / 8, "literals": sum(1 for t in tokens if isinstance(t, int)),
            "matches": sum(1 for t in tokens if not isinstance(t, int))}


def lzw(data: bytes):
    """LZ78's LZW variant: returns the code sequence; the dictionary grows by one phrase per code."""
    d = {bytes([i]): i for i in range(256)}
    w = b""
    out = []
    for c in data:
        wc = w + bytes([c])
        if wc in d:
            w = wc
        else:
            out.append(d[w])
            d[wc] = len(d)
            w = bytes([c])
    if w:
        out.append(d[w])
    return out, len(d)


def rans_size(symbols, freq_bits: int = 12) -> float:
    """Bits an ideal static model would need (sum of -log2 p), which rANS reaches to within a fraction of a bit
    per symbol; computed directly."""
    c = Counter(symbols)
    n = sum(c.values())
    return float(sum(-v * math.log2(v / n) for v in c.values()))


class RANS:
    """A small byte-wise rANS coder (Duda) with a static model: encode and decode, to show it round-trips and how
    close it gets to the entropy."""

    def __init__(self, data: bytes, prob_bits: int = 12):
        prob_bits = _integer(prob_bits, "probability bits", 1, 16)
        if not data:
            raise ValueError("rANS model needs at least one observed byte")
        if len(set(data)) > 1 << prob_bits:
            raise ValueError("model precision cannot give every observed byte a positive frequency")
        self.M = 1 << prob_bits
        cnt = np.bincount(np.frombuffer(data, dtype=np.uint8), minlength=256).astype(np.float64)
        scaled = cnt / cnt.sum() * self.M
        f = np.floor(scaled).astype(np.int64)
        f[(cnt > 0) & (f == 0)] = 1
        while f.sum() > self.M:
            f[np.argmax(np.where(f > 1, f - scaled, -np.inf))] -= 1
        while f.sum() < self.M:
            f[np.argmax(np.where(cnt > 0, scaled - f, -np.inf))] += 1
        self.f = f.tolist()
        self.cum = np.concatenate([[0], np.cumsum(f)]).tolist()
        self.slot = []
        for s in range(256):
            self.slot += [s] * self.f[s]
        self.prob_bits = prob_bits

    def encode(self, data: bytes):
        if any(self.f[s] == 0 for s in set(data)):
            raise ValueError("input includes a byte absent from the rANS model")
        L = 1 << 23
        x = L
        out = []
        for s in reversed(data):
            fs, cs = self.f[s], self.cum[s]
            xmax = ((L >> self.prob_bits) << 8) * fs
            while x >= xmax:
                out.append(x & 255)
                x >>= 8
            x = (x // fs) * self.M + (x % fs) + cs
        for _ in range(4):
            out.append(x & 255)
            x >>= 8
        return bytes(reversed(out))

    def decode(self, enc: bytes, n: int) -> bytes:
        n = _integer(n, "decoded byte count", 0)
        if len(enc) < 4:
            raise ValueError("rANS stream is missing its initial state")
        L = 1 << 23
        pos = 0
        x = 0
        for _ in range(4):
            x = (x << 8) | enc[pos]
            pos += 1
        if x < L:
            raise ValueError("invalid rANS initial state")
        out = bytearray()
        mask = self.M - 1
        for _ in range(n):
            r = x & mask
            s = self.slot[r]
            out.append(s)
            x = self.f[s] * (x >> self.prob_bits) + r - self.cum[s]
            while x < L:
                if pos >= len(enc):
                    raise ValueError("truncated rANS stream")
                x = (x << 8) | enc[pos]
                pos += 1
        if x != L or pos != len(enc):
            raise ValueError("rANS stream does not match its decoded length")
        return bytes(out)


# ------------------------------------------------------------------------------------------------- alignment
def needleman_wunsch(a, b, match=1, mismatch=-1, gap=-1):
    n, m = len(a), len(b)
    S = np.zeros((n + 1, m + 1), dtype=np.int64)
    S[:, 0] = gap * np.arange(n + 1)
    S[0, :] = gap * np.arange(m + 1)
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            s = match if a[i - 1] == b[j - 1] else mismatch
            S[i, j] = max(S[i - 1, j - 1] + s, S[i - 1, j] + gap, S[i, j - 1] + gap)
    return S


def smith_waterman(a, b, match=2, mismatch=-1, gap=-2):
    """Local alignment: (best score, end cell, start cell), with numpy over anti-diagonals avoided for clarity."""
    n, m = len(a), len(b)
    H = np.zeros((n + 1, m + 1), dtype=np.int64)
    best, at = 0, (0, 0)
    for i in range(1, n + 1):
        ai = a[i - 1]
        row, up = H[i], H[i - 1]
        for j in range(1, m + 1):
            v = max(0, up[j - 1] + (match if ai == b[j - 1] else mismatch), up[j] + gap, row[j - 1] + gap)
            row[j] = v
            if v > best:
                best, at = v, (i, j)
    # trace back to the start
    i, j = at
    while i > 0 and j > 0 and H[i, j] > 0:
        s = match if a[i - 1] == b[j - 1] else mismatch
        if H[i, j] == H[i - 1, j - 1] + s:
            i, j = i - 1, j - 1
        elif H[i, j] == H[i - 1, j] + gap:
            i -= 1
        else:
            j -= 1
    return int(best), at, (i, j), H


# ------------------------------------------------------------------------------------------------- diff
def myers(a, b):
    """Myers (1986): the shortest edit script by greedy furthest-reaching D-paths.  Returns (D, the edit script as
    a list of (op, line), the trace of V arrays for drawing, and the number of snake steps)."""
    n, m = len(a), len(b)
    mx = n + m
    v = {1: 0}
    trace = []
    snake = 0
    for d in range(mx + 1):
        trace.append(dict(v))
        for k in range(-d, d + 1, 2):
            if k == -d or (k != d and v.get(k - 1, -1) < v.get(k + 1, -1)):
                x = v.get(k + 1, 0)
            else:
                x = v.get(k - 1, 0) + 1
            y = x - k
            while x < n and y < m and a[x] == b[y]:
                x, y = x + 1, y + 1
                snake += 1
            v[k] = x
            if x >= n and y >= m:
                trace.append(dict(v))
                return d, _script(a, b, trace[:-1]), trace, snake
    raise AssertionError


def _script(a, b, trace):
    """Walk the saved V arrays back from (n, m): each D-path is a (D-1)-path, one edit, then a snake."""
    x, y = len(a), len(b)
    ops = []
    for d in range(len(trace) - 1, -1, -1):
        v = trace[d]
        k = x - y
        if k == -d or (k != d and v.get(k - 1, -1) < v.get(k + 1, -1)):
            pk = k + 1
        else:
            pk = k - 1
        px = v.get(pk, 0)
        py = px - pk
        while x > px and y > py:
            ops.append(("=", a[x - 1]))
            x, y = x - 1, y - 1
        if d > 0:
            if x == px:
                ops.append(("+", b[y - 1]))
            else:
                ops.append(("-", a[x - 1]))
            x, y = px, py
    return ops[::-1]


def lcs_len(a, b):
    """Classic quadratic LCS length (for checking: D = n + m - 2 LCS)."""
    prev = [0] * (len(b) + 1)
    for x in a:
        cur = [0]
        for j, y in enumerate(b):
            cur.append(prev[j] + 1 if x == y else max(prev[j + 1], cur[j]))
        prev = cur
    return prev[-1]


def patience_anchors(a, b):
    """Patience diff's anchors: lines unique in both files, in a longest increasing run."""
    ca, cb = Counter(a), Counter(b)
    pos_b = {line: j for j, line in enumerate(b) if cb[line] == 1}
    seq = [(i, pos_b[line]) for i, line in enumerate(a) if ca[line] == 1 and line in pos_b]
    # longest increasing subsequence on the b positions (patience sorting)
    piles, back = [], []
    tops = []
    for idx, (_, j) in enumerate(seq):
        lo, hi = 0, len(tops)
        while lo < hi:
            mid = (lo + hi) // 2
            if seq[tops[mid]][1] < j:
                lo = mid + 1
            else:
                hi = mid
        if lo == len(tops):
            tops.append(idx)
        else:
            tops[lo] = idx
        back.append(tops[lo - 1] if lo else -1)
        piles.append(lo)
    out = []
    k = tops[-1] if tops else -1
    while k >= 0:
        out.append(seq[k])
        k = back[k]
    return out[::-1]


# ------------------------------------------------------------------------------------------------- rolling hashes
def adler32_rolling(data: bytes, block: int):
    """rsync's weak checksum for every window of length ``block`` (numpy)."""
    block = _integer(block, "block size", 1)
    if block > len(data):
        return np.empty(0, dtype=np.int64)
    t = np.frombuffer(data, dtype=np.uint8).astype(np.int64)
    c = np.concatenate([[0], np.cumsum(t)])
    a = (c[block:] - c[:-block]) % 65536
    w = np.concatenate([[0], np.cumsum(t * np.arange(len(t), 0, -1))])
    # b(k) = sum_{i=k}^{k+block-1} (k + block - i) t_i
    idx = np.arange(len(t) - block + 1)
    s = w[idx + block] - w[idx]                       # sum (n - i) t_i over the window
    b = (s - (len(t) - idx - block) * (c[idx + block] - c[idx])) % 65536
    return (b << 16) | a


def gear_table(seed: int = 21):
    rng = np.random.default_rng(seed)
    return rng.integers(0, 2 ** 32, 256, dtype=np.uint64)


def cdc_chunks(data: bytes, mask_bits: int = 13, min_size: int = 2048, max_size: int = 65536, seed: int = 21):
    """Content-defined chunking with a gear hash (as in FastCDC): cut where the rolling hash's top bits are zero.
    Returns the chunk boundaries."""
    mask_bits = _integer(mask_bits, "mask bits", 1, 32)
    min_size = _integer(min_size, "minimum chunk size", 1)
    max_size = _integer(max_size, "maximum chunk size", min_size)
    G = gear_table(seed).tolist()
    mask = ((1 << mask_bits) - 1) << (32 - mask_bits)
    cuts, h, start = [], 0, 0
    for i, c in enumerate(data):
        h = ((h << 1) + G[c]) & 0xFFFFFFFF
        size = i - start + 1
        if (size >= min_size and (h & mask) == 0) or size >= max_size:
            cuts.append(i + 1)
            start = i + 1
            h = 0
    if start < len(data):
        cuts.append(len(data))
    return cuts


def chunk_hashes(data: bytes, cuts):
    import hashlib
    cuts = list(cuts)
    previous = 0
    for c in cuts:
        c = _integer(c, "chunk endpoint", previous + 1, len(data))
        previous = c
    if previous != len(data):
        raise ValueError("chunk endpoints must partition the entire input")
    out, s = [], 0
    for c in cuts:
        out.append(hashlib.blake2b(data[s:c], digest_size=8).digest())
        s = c
    return out


# ------------------------------------------------------------------------------------------------- periodicity
def manacher(s: bytes, all_: bool = False):
    """Longest palindromic substring in linear time: (start, length); with ``all_``, every centre's radius."""
    # Values above 255 cannot collide with arbitrary input bytes.
    t = array("H", [257, 256])
    for c in s:
        t.append(c)
        t.append(256)
    t.append(258)
    n = len(t)
    p = [0] * n
    c = r = 0
    for i in range(1, n - 1):
        if i < r:
            p[i] = min(r - i, p[2 * c - i])
        while t[i + 1 + p[i]] == t[i - 1 - p[i]]:
            p[i] += 1
        if i + p[i] > r:
            c, r = i, i + p[i]
    if all_:
        return p
    k = max(range(n), key=lambda i: p[i])
    length = p[k]
    start = (k - length) // 2
    return start, length


def periods(s: bytes):
    """All periods p of s (s[i] = s[i + p] for all valid i), from the border chain of the failure function."""
    if not s:
        return []
    fail = kmp_failure(s)
    n = len(s)
    out = []
    b = fail[-1] if n else 0
    while True:
        out.append(n - b)
        if b == 0:
            break
        b = fail[b - 1]
    return out


def duval(s: str):
    """Lyndon factorization (Duval 1983): s = w1 w2 ... with w1 >= w2 >= ... Lyndon words."""
    n, i, out = len(s), 0, []
    while i < n:
        j, k = i + 1, i
        while j < n and s[k] <= s[j]:
            k = i if s[k] < s[j] else k + 1
            j += 1
        while i <= k:
            out.append(s[i:i + j - k])
            i += j - k
    return out
