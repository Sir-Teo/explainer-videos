"""Branch predictors (Part 7): each has ``predict(pc) -> bool`` and ``update(pc, taken)``.

    p = TwoBit(entries=1024)
    accuracy(p, trace)                 # trace: [(pc, taken), ...] in program order

Static ones (always taken, backward-taken/forward-not-taken), Smith's 1-bit and 2-bit counter tables (1981), McFarling's
gshare and tournament (1993), a small TAGE (Seznec and Michaud, 2006) and Jiménez and Lin's perceptron (2001).  The
correlating predictors keep a global history of the last outcomes, updated here at each resolved branch (in program
order: the trace-driven study of Part 7; the pipeline updates them when a branch resolves in EX).
"""

from __future__ import annotations

import numpy as np


class Always:
    name = "always taken"

    def predict(self, pc):
        return True

    def update(self, pc, taken):
        pass


class BTFN:
    """Backward taken, forward not taken: loops close backwards.  Needs the target, so it is given the trace's
    branch directions (``backward`` maps pc to whether its target is behind it)."""

    name = "backward taken"

    def __init__(self, backward: dict[int, bool]):
        self.backward = backward

    def predict(self, pc):
        return self.backward.get(pc, False)

    def update(self, pc, taken):
        pass


class OneBit:
    name = "1-bit"

    def __init__(self, entries=1024):
        self.n = entries
        self.t = np.zeros(entries, np.int8)

    def predict(self, pc):
        return bool(self.t[(pc >> 2) % self.n])

    def update(self, pc, taken):
        self.t[(pc >> 2) % self.n] = taken


class TwoBit:
    """Saturating counters 0..3; predict taken at 2 or 3.  A Part 5 state machine per entry."""

    name = "2-bit"

    def __init__(self, entries=1024):
        self.n = entries
        self.t = np.full(entries, 1, np.int8)

    def predict(self, pc):
        return self.t[(pc >> 2) % self.n] >= 2

    def update(self, pc, taken):
        k = (pc >> 2) % self.n
        self.t[k] = min(3, self.t[k] + 1) if taken else max(0, self.t[k] - 1)


class GShare:
    """2-bit counters indexed by the pc xor the last ``bits`` outcomes."""

    name = "gshare"

    def __init__(self, bits=12):
        self.bits = bits
        self.n = 1 << bits
        self.t = np.full(self.n, 1, np.int8)
        self.h = 0

    def _k(self, pc):
        return ((pc >> 2) ^ self.h) & (self.n - 1)

    def predict(self, pc):
        return self.t[self._k(pc)] >= 2

    def update(self, pc, taken):
        k = self._k(pc)
        self.t[k] = min(3, self.t[k] + 1) if taken else max(0, self.t[k] - 1)
        self.h = ((self.h << 1) | int(taken)) & (self.n - 1)


class Tournament:
    """A chooser (2-bit counters per pc) between a local 2-bit table and gshare."""

    name = "tournament"

    def __init__(self, bits=12):
        self.local = TwoBit(1 << bits)
        self.glob = GShare(bits)
        self.n = 1 << bits
        self.choose = np.full(self.n, 2, np.int8)  # >= 2: trust gshare

    def predict(self, pc):
        k = (pc >> 2) % self.n
        return self.glob.predict(pc) if self.choose[k] >= 2 else self.local.predict(pc)

    def update(self, pc, taken):
        k = (pc >> 2) % self.n
        g, l_ = self.glob.predict(pc) == taken, self.local.predict(pc) == taken
        if g != l_:
            self.choose[k] = min(3, self.choose[k] + 1) if g else max(0, self.choose[k] - 1)
        self.local.update(pc, taken)
        self.glob.update(pc, taken)


class Tage:
    """A small TAGE: a bimodal base and tagged tables indexed with geometrically growing histories; the longest
    matching history provides the prediction.  Simplified from Seznec and Michaud (2006): one useful bit, 3-bit
    counters, allocation of one entry on a misprediction."""

    name = "TAGE"

    def __init__(self, lengths=(4, 8, 16, 32, 64), bits=10, tag_bits=9, seed=1):
        self.base = TwoBit(1 << 12)
        self.L = lengths
        self.bits, self.tag_bits = bits, tag_bits
        self.n = 1 << bits
        self.ctr = [np.zeros(self.n, np.int8) for _ in lengths]  # -4..3: taken if >= 0
        self.tag = [np.full(self.n, -1, np.int32) for _ in lengths]
        self.u = [np.zeros(self.n, np.int8) for _ in lengths]
        self.hist = 0  # an integer of the last max(L) outcomes
        self.rng = np.random.default_rng(seed)

    def _fold(self, length, width):
        h = self.hist & ((1 << length) - 1)
        out = 0
        while h:
            out ^= h & ((1 << width) - 1)
            h >>= width
        return out

    def _idx(self, t, pc):
        return ((pc >> 2) ^ self._fold(self.L[t], self.bits) ^ (t * 0x9E5)) & (self.n - 1)

    def _tg(self, t, pc):
        return ((pc >> 2) ^ (self._fold(self.L[t], self.tag_bits) << 1)) & ((1 << self.tag_bits) - 1)

    def _lookup(self, pc):
        hits = []
        for t in range(len(self.L)):
            i = self._idx(t, pc)
            if self.tag[t][i] == self._tg(t, pc):
                hits.append((t, i))
        return hits

    def predict(self, pc):
        hits = self._lookup(pc)
        if hits:
            t, i = hits[-1]
            return self.ctr[t][i] >= 0
        return self.base.predict(pc)

    def update(self, pc, taken):
        hits = self._lookup(pc)
        pred = self.predict(pc)
        if hits:
            t, i = hits[-1]
            c = self.ctr[t][i]
            self.ctr[t][i] = min(3, c + 1) if taken else max(-4, c - 1)
            if pred == taken:
                self.u[t][i] = 1
        else:
            self.base.update(pc, taken)
        if pred != taken:  # allocate in a longer table
            start = hits[-1][0] + 1 if hits else 0
            for t in range(start, len(self.L)):
                i = self._idx(t, pc)
                if self.u[t][i] == 0:
                    self.tag[t][i] = self._tg(t, pc)
                    self.ctr[t][i] = 0 if taken else -1
                    break
                if self.rng.random() < 0.1:
                    self.u[t][i] = 0
        self.hist = ((self.hist << 1) | int(taken)) & ((1 << max(self.L)) - 1)


class Perceptron:
    """Jiménez and Lin (2001): per branch, a weight for each of the last h outcomes and a bias.  Predict taken when
    y = w0 + sum_i w_i x_i >= 0, with x_i = +1 for taken and -1 for not; train when wrong or |y| <= theta."""

    name = "perceptron"

    def __init__(self, entries=256, h=24, wmax=127):
        self.n, self.h = entries, h
        self.w = np.zeros((entries, h + 1), np.int32)
        self.x = np.ones(h + 1, np.int32)  # x[0] = 1, the bias input
        self.theta = int(1.93 * h + 14)
        self.wmax = wmax

    def _y(self, pc):
        return int(self.w[(pc >> 2) % self.n] @ self.x)

    def predict(self, pc):
        return self._y(pc) >= 0

    def update(self, pc, taken):
        k = (pc >> 2) % self.n
        y = self._y(pc)
        t = 1 if taken else -1
        if (y >= 0) != taken or abs(y) <= self.theta:
            self.w[k] = np.clip(self.w[k] + t * self.x, -self.wmax - 1, self.wmax)
        self.x[2:] = self.x[1:-1]
        self.x[1] = t

    def weights(self, pc) -> np.ndarray:
        return self.w[(pc >> 2) % self.n].copy()


class Unlimited:
    """A limit-study predictor: an unbounded table with one counter per (branch, last h global outcomes) context, no
    aliasing, and the majority so far as the prediction (ties: taken).  It must learn every context from scratch, so a
    longer history sees sharper patterns but learns them more slowly: no single h is best everywhere."""

    def __init__(self, h=8):
        self.h, self.name = h, f"unlimited, h = {h}"
        self.ghr = 0
        self.mask = (1 << h) - 1
        self.c: dict[tuple[int, int], list[int]] = {}

    def predict(self, pc):
        n = self.c.get((pc, self.ghr))
        return True if n is None else n[1] >= n[0]

    def update(self, pc, taken):
        self.c.setdefault((pc, self.ghr), [0, 0])[int(taken)] += 1
        self.ghr = ((self.ghr << 1) | int(taken)) & self.mask


class PPM:
    """Prediction by partial matching (Cleary and Witten, 1984), as a branch predictor (Chen, Coffey and Mudge, 1996):
    unbounded tables for every history length in ``lengths``; predict from the longest context seen at least
    ``confidence`` times whose majority is strict, falling back to shorter ones.  An idealised TAGE, with no limit on
    storage."""

    def __init__(self, lengths=(0, 1, 2, 3, 4, 6, 8, 12, 16, 24, 32, 48, 64), confidence=2):
        self.lengths, self.k = tuple(sorted(lengths)), confidence
        self.name = "PPM, unlimited"
        self.ghr = 0
        self.mask = (1 << max(self.lengths)) - 1
        self.c = [dict() for _ in self.lengths]

    def _ctx(self, pc, h):
        return pc, self.ghr & ((1 << h) - 1)

    def predict(self, pc):
        for t, h in reversed(list(enumerate(self.lengths))):
            n = self.c[t].get(self._ctx(pc, h))
            if n is not None and n[0] + n[1] >= self.k and n[0] != n[1]:
                return n[1] > n[0]
        return True

    def update(self, pc, taken):
        for t, h in enumerate(self.lengths):
            self.c[t].setdefault(self._ctx(pc, h), [0, 0])[int(taken)] += 1
        self.ghr = ((self.ghr << 1) | int(taken)) & self.mask


def in_sample(trace, h) -> tuple[float, float]:
    """The best any history-h predictor could do with hindsight: each (branch, history) context predicted by its
    majority over the whole trace.  Returns (accuracy, conditional entropy in bits per branch)."""
    c: dict[tuple[int, int], list[int]] = {}
    g, mask = 0, (1 << h) - 1
    for pc, t in trace:
        c.setdefault((pc, g), [0, 0])[int(t)] += 1
        g = ((g << 1) | int(t)) & mask
    n = len(trace)
    acc = sum(max(v) for v in c.values()) / n
    ent = 0.0
    for a, b in c.values():
        m = a + b
        for x in (a, b):
            if x:
                ent -= x / n * np.log2(x / m)
    return acc, ent


def accuracy(p, trace) -> float:
    """Fraction of a branch trace [(pc, taken), ...] predicted right, training as it goes."""
    right = 0
    for pc, t in trace:
        right += p.predict(pc) == t
        p.update(pc, t)
    return right / max(len(trace), 1)


def all_predictors(backward=None):
    out = [Always(), OneBit(), TwoBit(), GShare(), Tournament(), Tage(), Perceptron()]
    if backward is not None:
        out.insert(1, BTFN(backward))
    return out
