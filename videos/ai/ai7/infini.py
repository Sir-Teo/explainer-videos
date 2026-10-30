"""An infini-gram (Liu et al., 2024) over Part 1's thirty novels: a suffix array of the reading, in numpy.

    sa = suffix_array(codes)                     # codes: uint8, symbols 1..255 (0 is never used)
    idx = Index(codes[::-1].copy())              # the REVERSED text: a context grows leftward = a pattern grows at its end
    L, lo, hi = idx.longest(text_codes, i)       # the longest context ending before position i that the novels contain

The suffix array is built by prefix doubling (Manber & Myers, 1990): sort the suffixes by their first 8 symbols, then by
16, 32, ... using the ranks of the previous round, until every suffix has its own rank.  A pattern's occurrences are one
contiguous range of the array, found by binary search; the symbols that followed a context in the novels are the
symbols just before the matching suffixes of the reversed text.
"""

from __future__ import annotations

import numpy as np


def suffix_array(codes: np.ndarray, log=print) -> np.ndarray:
    """The suffix array of ``codes`` (uint8): the start of every suffix, in sorted order (int32)."""
    n = len(codes)
    pad = np.concatenate([codes.astype(np.uint64), np.zeros(8, np.uint64)])
    key = np.zeros(n, np.uint64)
    for j in range(8):  # the first eight symbols, packed into one 64-bit key
        key = (key << np.uint64(8)) | pad[j:j + n]
    del pad
    sa = np.argsort(key, kind="stable").astype(np.int32)
    ks = key[sa]
    rank = np.empty(n, np.int32)
    rank[sa] = np.cumsum(np.r_[True, ks[1:] != ks[:-1]]) - 1
    del key, ks
    h = 8
    while int(rank.max()) < n - 1:
        nxt = np.zeros(n, np.int64)
        nxt[: n - h] = rank[h:].astype(np.int64) + 1  # 0: the suffix ends within h symbols
        k = rank.astype(np.int64) * (n + 1) + nxt
        del nxt
        sa = np.argsort(k, kind="stable").astype(np.int32)
        ks = k[sa]
        del k
        rank[sa] = np.cumsum(np.r_[True, ks[1:] != ks[:-1]]) - 1
        del ks
        h *= 2
        log(f"    suffix array: sorted by the first {h} symbols, {int(rank.max()) + 1:,} distinct of {n:,}")
    return sa


class Index:
    """Counts of any pattern in a text, through its suffix array."""

    def __init__(self, codes: np.ndarray, sa: np.ndarray | None = None):
        self.codes = codes
        self.b = codes.tobytes()
        self.sa = suffix_array(codes) if sa is None else sa
        self.n = len(codes)

    def _bound(self, q: bytes, lo: int, hi: int, upper: bool) -> int:
        b, sa, m = self.b, self.sa, len(q)
        while lo < hi:
            mid = (lo + hi) // 2
            s = int(sa[mid])
            t = b[s:s + m]
            if t < q or (upper and t == q):
                lo = mid + 1
            else:
                hi = mid
        return lo

    def range(self, q: bytes, lo: int = 0, hi: int | None = None) -> tuple[int, int]:
        """The suffixes that start with ``q``: sa[lo:hi] (searched within a range already known to hold them)."""
        hi = self.n if hi is None else hi
        a = self._bound(q, lo, hi, False)
        return a, self._bound(q, a, hi, True)

    def count(self, q: bytes) -> int:
        a, b = self.range(q)
        return b - a

    def before(self, lo: int, hi: int, K: int) -> np.ndarray:
        """How often each symbol comes just before the suffixes sa[lo:hi] (in the reversed text: just after the
        context, in the original)."""
        s = self.sa[lo:hi].astype(np.int64)
        s = s[s > 0]
        return np.bincount(self.codes[s - 1], minlength=K + 1)

    def longest(self, text: np.ndarray, i: int, cap: int = 2000, lengths: list | None = None):
        """The longest context text[i-L:i] that occurs in the indexed (reversed) text, with its range.  ``lengths``,
        if given, collects the count of every context length on the way."""
        lo, hi, L = 0, self.n, 0
        q = bytearray()
        while L < min(i, cap):
            q.append(int(text[i - 1 - L]))
            a, b = self.range(bytes(q), lo, hi)
            if b <= a:
                break
            lo, hi, L = a, b, L + 1
            if lengths is not None:
                lengths.append(hi - lo)
        return L, lo, hi
