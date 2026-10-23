"""A finite-precision arithmetic coder (Witten, Neal & Cleary 1987), in integers, as real compressors use it.

The interval is a pair of integers ``low .. high`` inside ``0 .. 2^precision - 1``.  Each symbol narrows it in
proportion to its share of an integer frequency table (``cum_lo .. cum_hi`` out of ``total``); then, while the
interval sits inside one half of the range, the leading bit of every number in it is decided: that bit is sent and the
half is doubled ("zoomed") back to full size.  An interval that straddles the middle but sits inside the middle two
quarters is zoomed about the middle, and the bit it will decide is remembered as *pending* (Witten, Neal & Cleary's
"underflow" case).  ``total`` must be at most a quarter of the range, so every symbol keeps a nonempty slice.

    enc = Encoder(32)
    for lo, hi, tot in slices: enc.encode(lo, hi, tot)
    bits = enc.finish()                      # a list of 0/1
    dec = Decoder(bits, 32)
    sym = dec.find(cdf)                      # the symbol whose slice of the cumulative table holds the code value
    dec.consume(cdf[sym], cdf[sym + 1], cdf[-1])

Plain Python integers, so any precision works; ``trace`` records every narrowing and every zoom (Chapter 8's picture).
"""

from __future__ import annotations

from bisect import bisect_right


class Encoder:
    def __init__(self, precision: int = 32, trace: bool = False):
        self.P = precision
        self.full = 1 << precision
        self.half, self.quarter = self.full >> 1, self.full >> 2
        self.low, self.high = 0, self.full - 1
        self.pending = 0
        self.bits: list[int] = []
        self.trace = [] if trace else None

    def _emit(self, b: int) -> None:
        self.bits.append(b)
        self.bits.extend([1 - b] * self.pending)
        self.pending = 0

    def encode(self, cum_lo: int, cum_hi: int, total: int) -> None:
        assert 0 <= cum_lo < cum_hi <= total <= self.quarter, (cum_lo, cum_hi, total, self.quarter)
        rng = self.high - self.low + 1
        self.high = self.low + rng * cum_hi // total - 1
        self.low = self.low + rng * cum_lo // total
        if self.trace is not None:
            self.trace.append(("narrow", self.low, self.high, ""))
        while True:
            if self.high < self.half:
                self._emit(0)
                kind = "0"
            elif self.low >= self.half:
                self._emit(1)
                self.low -= self.half
                self.high -= self.half
                kind = "1"
            elif self.low >= self.quarter and self.high < self.half + self.quarter:
                self.pending += 1
                self.low -= self.quarter
                self.high -= self.quarter
                kind = "p"
            else:
                break
            self.low, self.high = 2 * self.low, 2 * self.high + 1
            if self.trace is not None:
                self.trace.append(("zoom", self.low, self.high, kind))

    def finish(self) -> list[int]:
        """Two more bits (and any pending ones) pin down a number inside the final interval."""
        self.pending += 1
        self._emit(0 if self.low < self.quarter else 1)
        return self.bits


class Decoder:
    def __init__(self, bits: list[int], precision: int = 32):
        self.P = precision
        self.full = 1 << precision
        self.half, self.quarter = self.full >> 1, self.full >> 2
        self.low, self.high = 0, self.full - 1
        self.bits, self.pos = bits, 0
        self.value = 0
        for _ in range(precision):
            self.value = 2 * self.value + self._next()

    def _next(self) -> int:
        b = self.bits[self.pos] if self.pos < len(self.bits) else 0
        self.pos += 1
        return b

    def target(self, total: int) -> int:
        """Where the code value falls, on the scale of the frequency table: ``cum_lo <= target < cum_hi``."""
        rng = self.high - self.low + 1
        return ((self.value - self.low + 1) * total - 1) // rng

    def find(self, cdf) -> int:
        """The symbol s with ``cdf[s] <= target < cdf[s + 1]`` (``cdf`` starts at 0 and ends at the total)."""
        t = self.target(int(cdf[-1]))
        return bisect_right(cdf, t) - 1 if isinstance(cdf, list) else int(_searchsorted(cdf, t))

    def consume(self, cum_lo: int, cum_hi: int, total: int) -> None:
        rng = self.high - self.low + 1
        self.high = self.low + rng * cum_hi // total - 1
        self.low = self.low + rng * cum_lo // total
        while True:
            if self.high < self.half:
                pass
            elif self.low >= self.half:
                self.low -= self.half
                self.high -= self.half
                self.value -= self.half
            elif self.low >= self.quarter and self.high < self.half + self.quarter:
                self.low -= self.quarter
                self.high -= self.quarter
                self.value -= self.quarter
            else:
                break
            self.low, self.high = 2 * self.low, 2 * self.high + 1
            self.value = 2 * self.value + self._next()


def _searchsorted(cdf, t: int) -> int:
    import numpy as np

    return int(np.searchsorted(cdf, t, side="right")) - 1


def quantize(probs, freq_bits: int):
    """Integer frequencies for a distribution: every symbol at least 1, the rest shared in proportion, total at most
    2^freq_bits.  Returns the cumulative table [0, f_0, f_0 + f_1, ..., total] (numpy int64)."""
    import numpy as np

    p = np.asarray(probs, np.float64)
    budget = (1 << freq_bits) - len(p)
    assert budget > 0, (freq_bits, len(p))
    f = 1 + np.floor(p / p.sum() * budget).astype(np.int64)
    return np.concatenate([[0], np.cumsum(f)])
