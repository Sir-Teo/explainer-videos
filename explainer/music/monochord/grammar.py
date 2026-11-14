"""Analysis (Part 22): reductions and grammars.

A time-span reduction of a melody (Lerdahl and Jackendoff's idea, with simple preference rules: the head of each span
is its most stable note, by harmony, scale degree and metre); a generative grammar of melodic elaboration (repetition,
neighbour and passing notes, arpeggiation) that grows a surface from a skeleton; and a probabilistic context-free
grammar of harmony (tonic, dominant and subdominant regions, after Rohrmeier 2011) in Chomsky normal form, trained by
the inside-outside algorithm, parsed by Viterbi, and scored by cross-entropy against chord n-grams.  No manim here.
"""

from __future__ import annotations

import math
from collections import Counter

import numpy as np

MAJOR = (0, 2, 4, 5, 7, 9, 11)
STABILITY = {0: 3.0, 7: 2.0, 4: 1.5, 2: 0.5, 5: 0.5, 9: 0.5, 11: 0.2}      # degree (semitones above the tonic) -> stability


# ---------------------------------------------------------------------------
# Time-span reduction
# ---------------------------------------------------------------------------
def metric_weight(t: float, bar: float = 4.0) -> float:
    """Strength of a moment in 4/4: the downbeat strongest, then beat 3, then beats 2 and 4, then off-beats."""
    x = t % bar
    if abs(x) < 1e-9:
        return 3.0
    if abs(x - bar / 2) < 1e-9:
        return 2.0
    if abs(x - round(x)) < 1e-9:
        return 1.0
    return 0.0


def importance(note, chord_pcs=None, tonic: int = 0) -> float:
    """A note's claim to be the head of a span: consonant with the harmony, a stable degree, on a strong beat."""
    p, a, d = note
    s = STABILITY.get((p - tonic) % 12, 0.0)
    c = 2.0 if chord_pcs is not None and p % 12 in chord_pcs else 0.0
    return c + s + 0.5 * metric_weight(a) + 0.1 * d


def reduce_levels(notes, chord_at=None, span: float = 1.0, tonic: int = 0) -> list[list[tuple]]:
    """Levels of a time-span reduction: level 0 is the melody; at level k every span of ``span * 2**k`` beats keeps
    one note, the more important of its two halves' heads, sounding for the whole span.  ``chord_at(t)`` gives the
    pitch classes of the harmony at time t (for consonance)."""
    T = max(a + d for _, a, d in notes)
    levels = [list(notes)]
    cur = list(notes)
    size = span
    while size < T:
        size *= 2
        nxt = []
        t = 0.0
        while t < T - 1e-9:
            inside = [n for n in cur if t - 1e-9 <= n[1] < t + size - 1e-9]
            if inside:
                best = max(inside, key=lambda n: (importance(n, chord_at(n[1]) if chord_at else None, tonic), -n[1]))
                nxt.append((best[0], t, min(size, T - t)))
            t += size
        levels.append(nxt)
        cur = nxt
    return levels


# ---------------------------------------------------------------------------
# A grammar of melodic elaboration
# ---------------------------------------------------------------------------
def scale_step(p: int, k: int, tonic: int = 0) -> int:
    rel = (p - tonic) % 12
    octv = (p - tonic) // 12
    idx = min(range(7), key=lambda i: abs(MAJOR[i] - rel))
    j = idx + k
    return tonic + 12 * (octv + j // 7) + MAJOR[j % 7]


def elaborate(skeleton, chord_at, rng, depth: int = 2, min_dur: float = 1.0, tonic: int = 0, weights=None):
    """Grow a surface from a skeleton by rewriting each note (or pair of notes) in ``depth`` rounds; each rule halves a
    note's time: repeat (x -> x x), upper or lower neighbour (x -> x n), passing (x, y a third apart -> x p, y),
    arpeggiation (x -> x c, c another tone of the chord).  Returns the surface and the rules used, in order."""
    weights = weights or {"repeat": 1.0, "neighbour": 1.0, "passing": 1.5, "arpeggio": 1.0, "keep": 1.0}
    notes = [tuple(n) for n in skeleton]
    used = []
    for _ in range(depth):
        out = []
        for i, (p, a, d) in enumerate(notes):
            nxt = notes[i + 1][0] if i + 1 < len(notes) else None
            if d < 2 * min_dur - 1e-9:
                out.append((p, a, d))
                continue
            opts = ["keep", "repeat", "neighbour", "arpeggio"]
            if nxt is not None and abs(nxt - p) in (3, 4):
                opts.append("passing")
            w = np.array([weights[o] for o in opts], dtype=float)
            r = opts[int(rng.choice(len(opts), p=w / w.sum()))]
            h = d / 2
            if r == "keep":
                out.append((p, a, d))
            elif r == "repeat":
                out += [(p, a, h), (p, a + h, h)]
            elif r == "neighbour":
                out += [(p, a, h), (scale_step(p, int(rng.choice([-1, 1])), tonic), a + h, h)]
            elif r == "passing":
                out += [(p, a, h), (scale_step(p, 1 if nxt > p else -1, tonic), a + h, h)]
            else:
                pcs = [x for x in chord_at(a) if x != p % 12]
                c = min((q for q in range(p - 9, p + 10) if q % 12 in pcs), key=lambda q: abs(q - p) + 0.01 * q)
                out += [(p, a, h), (c, a + h, h)]
            used.append(r)
        notes = out
    return notes, used


# ---------------------------------------------------------------------------
# Grouping (a few of Lerdahl and Jackendoff's preference rules)
# ---------------------------------------------------------------------------
def grouping_strength(notes) -> list[float]:
    """For each gap between notes, how strongly it invites a group boundary: a long note before it (GPR 2b, the
    'attack-point' rule), a large leap across it (GPR 3a), and a change of note length (GPR 3d)."""
    out = []
    for i in range(len(notes) - 1):
        p0, a0, d0 = notes[i]
        p1, a1, d1 = notes[i + 1]
        prev_d = notes[i - 1][2] if i > 0 else d0
        s = 0.0
        s += 1.0 if d0 > prev_d + 1e-9 else 0.0
        s += min(abs(p1 - p0), 12) / 6.0
        s += 0.5 if abs(d1 - d0) > 1e-9 else 0.0
        out.append(s)
    return out


# ---------------------------------------------------------------------------
# A probabilistic grammar of harmony
# ---------------------------------------------------------------------------
NT = ("TR", "DR", "SR")
RULES = [("TR", "TR", "TR"), ("TR", "DR", "TR"), ("DR", "SR", "DR"), ("DR", "DR", "DR"), ("SR", "SR", "SR"), ("TR", "TR", "DR")]
FUNCTION = {"I": "TR", "vi": "TR", "iii": "TR", "V": "DR", "V7": "DR", "vii°": "DR", "vii°7": "DR", "IV": "SR", "ii": "SR",
            "ii7": "SR", "IV7": "SR", "ii°": "SR"}


class PCFG:
    """A probabilistic context-free grammar in Chomsky normal form over the chord vocabulary: each nonterminal is a
    region (tonic, dominant, subdominant); a region either splits into two (``RULES``) or emits a chord."""

    def __init__(self, vocab, rules=RULES, start=("TR", "DR"), seed: int = 0, prior: float = 4.0):
        self.vocab = list(vocab)
        self.index = {v: i for i, v in enumerate(self.vocab)}
        self.nt = list(NT)
        self.ni = {a: i for i, a in enumerate(self.nt)}
        self.rules = [r for r in rules]
        rng = np.random.default_rng(seed)
        K, V = len(self.nt), len(self.vocab)
        self.emit = np.full((K, V), 0.1) + 0.05 * rng.random((K, V))
        for v, i in self.index.items():
            f = FUNCTION.get(v)
            if f:
                self.emit[self.ni[f], i] += prior
        self.emit /= self.emit.sum(1, keepdims=True)
        self.p_split = np.full(K, 0.5)
        self.binary = np.zeros(len(self.rules))
        for k in range(K):
            idx = [j for j, r in enumerate(self.rules) if r[0] == self.nt[k]]
            self.binary[idx] = 1.0 / len(idx)
        self.start = np.zeros(K)
        for s in start:
            self.start[self.ni[s]] = 1.0 / len(start)

    # inside probabilities: I[i, j, A] = P(A =>* w_i .. w_j)
    def inside(self, seq):
        n, K = len(seq), len(self.nt)
        I = np.zeros((n, n, K))
        for i, w in enumerate(seq):
            v = self.index.get(w)
            if v is not None:
                I[i, i] = (1 - self.p_split) * self.emit[:, v]
        for length in range(2, n + 1):
            for i in range(n - length + 1):
                j = i + length - 1
                for r, (A, B, C) in enumerate(self.rules):
                    a, b, c = self.ni[A], self.ni[B], self.ni[C]
                    p = self.p_split[a] * self.binary[r]
                    s = 0.0
                    for k in range(i, j):
                        s += I[i, k, b] * I[k + 1, j, c]
                    I[i, j, a] += p * s
        return I

    def prob(self, seq) -> float:
        if not seq:
            return 0.0
        I = self.inside(seq)
        return float(self.start @ I[0, len(seq) - 1])

    def outside(self, seq, I):
        n, K = len(seq), len(self.nt)
        O = np.zeros((n, n, K))
        O[0, n - 1] = self.start
        for length in range(n, 1, -1):
            for i in range(n - length + 1):
                j = i + length - 1
                for r, (A, B, C) in enumerate(self.rules):
                    a, b, c = self.ni[A], self.ni[B], self.ni[C]
                    p = self.p_split[a] * self.binary[r] * O[i, j, a]
                    if p == 0:
                        continue
                    for k in range(i, j):
                        O[i, k, b] += p * I[k + 1, j, c]
                        O[k + 1, j, c] += p * I[i, k, b]
        return O

    def train(self, seqs, iters: int = 30, smooth: float = 0.01) -> list[float]:
        """Inside-outside EM; returns the training log-likelihood (bits) after each iteration."""
        hist = []
        K, V, R = len(self.nt), len(self.vocab), len(self.rules)
        for _ in range(iters):
            ce = np.full((K, V), smooth)
            cr = np.full(R, smooth)
            cs = np.full(K, smooth)
            cl = np.full(K, smooth)
            ll = 0.0
            for seq in seqs:
                n = len(seq)
                I = self.inside(seq)
                Z = float(self.start @ I[0, n - 1])
                if Z <= 0:
                    continue
                ll += math.log2(Z)
                O = self.outside(seq, I)
                for i, w in enumerate(seq):
                    v = self.index.get(w)
                    if v is None:
                        continue
                    post = O[i, i] * I[i, i] / Z
                    ce[:, v] += post
                    cl += post
                for r, (A, B, C) in enumerate(self.rules):
                    a, b, c = self.ni[A], self.ni[B], self.ni[C]
                    base = self.p_split[a] * self.binary[r]
                    tot = 0.0
                    for i in range(n):
                        for j in range(i + 1, n):
                            if O[i, j, a] == 0:
                                continue
                            s = 0.0
                            for k in range(i, j):
                                s += I[i, k, b] * I[k + 1, j, c]
                            tot += O[i, j, a] * base * s
                    cr[r] += tot / Z
                    cs[a] += tot / Z
            self.emit = ce / ce.sum(1, keepdims=True)
            for k in range(K):
                idx = [j for j, r in enumerate(self.rules) if r[0] == self.nt[k]]
                if idx:
                    self.binary[idx] = cr[idx] / cr[idx].sum()
            self.p_split = cs / (cs + cl)
            hist.append(ll)
        return hist

    def viterbi(self, seq):
        """The most probable tree: nested tuples (region, left, right) or (region, chord)."""
        n, K = len(seq), len(self.nt)
        B = np.zeros((n, n, K))
        back = {}
        for i, w in enumerate(seq):
            v = self.index.get(w)
            if v is not None:
                B[i, i] = (1 - self.p_split) * self.emit[:, v]
        for length in range(2, n + 1):
            for i in range(n - length + 1):
                j = i + length - 1
                for r, (A, Bn, C) in enumerate(self.rules):
                    a, b, c = self.ni[A], self.ni[Bn], self.ni[C]
                    p0 = self.p_split[a] * self.binary[r]
                    for k in range(i, j):
                        p = p0 * B[i, k, b] * B[k + 1, j, c]
                        if p > B[i, j, a]:
                            B[i, j, a] = p
                            back[(i, j, a)] = (k, b, c)

        def build(i, j, a):
            if i == j:
                return (self.nt[a], seq[i])
            k, b, c = back[(i, j, a)]
            return (self.nt[a], build(i, k, b), build(k + 1, j, c))

        top = int(np.argmax(self.start * B[0, n - 1]))
        if B[0, n - 1, top] == 0:
            return None
        return build(0, n - 1, top)

    def count_parses(self, seq) -> int:
        """How many different trees the grammar allows for a sequence (every rule and emission allowed by function)."""
        n = len(seq)
        K = len(self.nt)
        C = np.zeros((n, n, K), dtype=object)
        for i, w in enumerate(seq):
            for a in range(K):
                C[i, i, a] = 1 if FUNCTION.get(w) == self.nt[a] else 0
        for length in range(2, n + 1):
            for i in range(n - length + 1):
                j = i + length - 1
                for (A, Bn, Cn) in self.rules:
                    a, b, c = self.ni[A], self.ni[Bn], self.ni[Cn]
                    for k in range(i, j):
                        C[i, j, a] += C[i, k, b] * C[k + 1, j, c]
        return int(sum(C[0, n - 1, self.ni[s]] for s in ("TR", "DR")))


def tree_depth(t) -> int:
    if t is None:
        return 0
    if len(t) == 2:
        return 1
    return 1 + max(tree_depth(t[1]), tree_depth(t[2]))


def bigram_bits(train, test, vocab, alpha: float = 0.1) -> float:
    """Bits per chord of an add-alpha bigram model with start and end symbols, on test sequences."""
    V = list(vocab) + ["<e>"]
    cnt, ctx = Counter(), Counter()
    for s in train:
        seq = ["<s>"] + list(s) + ["<e>"]
        for a, b in zip(seq, seq[1:]):
            cnt[(a, b)] += 1
            ctx[a] += 1
    bits, n = 0.0, 0
    for s in test:
        seq = ["<s>"] + list(s) + ["<e>"]
        for a, b in zip(seq, seq[1:]):
            p = (cnt[(a, b)] + alpha) / (ctx[a] + alpha * len(V))
            bits -= math.log2(p)
            n += 1
    return bits / n


def pcfg_bits(g: PCFG, test, length_model=None) -> float:
    """Bits per chord of the grammar on test sequences, counting the end as a symbol as the bigram model does; a
    sequence the grammar cannot parse is skipped and counted (see ``coverage``)."""
    bits, n = 0.0, 0
    for s in test:
        p = g.prob(s)
        if p <= 0:
            continue
        bits -= math.log2(p)
        n += len(s) + 1
    return bits / n if n else float("inf")


def coverage(g: PCFG, seqs) -> float:
    return sum(1 for s in seqs if g.prob(s) > 0) / max(1, len(seqs))


class LatentPCFG:
    """A grammar induced from data: ``K`` unnamed symbols, every binary rule A -> B C allowed, every symbol able to
    emit every chord; the probabilities learned by inside-outside, vectorized.  For each A the rule and emission
    probabilities together sum to one."""

    def __init__(self, vocab, K: int = 6, seed: int = 0, start_prior=None):
        self.vocab = list(vocab)
        self.index = {v: i for i, v in enumerate(self.vocab)}
        self.K = K
        rng = np.random.default_rng(seed)
        R = rng.random((K, K, K)) + 0.5
        E = rng.random((K, len(self.vocab))) + 0.5
        tot = R.reshape(K, -1).sum(1) + E.sum(1)
        self.R = R / tot[:, None, None] * 0.5 / (R.reshape(K, -1).sum(1) / tot)[:, None, None]
        self.E = E / E.sum(1, keepdims=True) * 0.5
        self.S = np.full(K, 1.0 / K)

    def inside(self, seq):
        n, K = len(seq), self.K
        I = np.zeros((n, n, K))
        for i, w in enumerate(seq):
            I[i, i] = self.E[:, self.index[w]]
        for length in range(2, n + 1):
            for i in range(n - length + 1):
                j = i + length - 1
                acc = np.zeros((K, K))
                for k in range(i, j):
                    acc += np.outer(I[i, k], I[k + 1, j])
                I[i, j] = np.einsum("abc,bc->a", self.R, acc)
        return I

    def prob(self, seq) -> float:
        return float(self.S @ self.inside(seq)[0, len(seq) - 1])

    def train(self, seqs, iters: int = 30, smooth: float = 1e-3) -> list[float]:
        hist = []
        K, V = self.K, len(self.vocab)
        for _ in range(iters):
            cR = np.full((K, K, K), smooth)
            cE = np.full((K, V), smooth)
            cS = np.full(K, smooth)
            ll = 0.0
            for seq in seqs:
                n = len(seq)
                I = self.inside(seq)
                Z = float(self.S @ I[0, n - 1])
                if Z <= 0:
                    continue
                ll += math.log2(Z)
                O = np.zeros((n, n, K))
                O[0, n - 1] = self.S
                cS += self.S * I[0, n - 1] / Z
                for length in range(n, 1, -1):
                    for i in range(n - length + 1):
                        j = i + length - 1
                        o = O[i, j]
                        for k in range(i, j):
                            l, r = I[i, k], I[k + 1, j]
                            cR += np.einsum("a,b,c->abc", o, l, r) * self.R / Z
                            O[i, k] += np.einsum("a,abc,c->b", o, self.R, r)
                            O[k + 1, j] += np.einsum("a,abc,b->c", o, self.R, l)
                for i, w in enumerate(seq):
                    cE[:, self.index[w]] += O[i, i] * I[i, i] / Z
            tot = cR.reshape(K, -1).sum(1) + cE.sum(1)
            self.R = cR / tot[:, None, None]
            self.E = cE / tot[:, None]
            self.S = cS / cS.sum()
            hist.append(ll)
        return hist

    def bits(self, seqs) -> float:
        b, n = 0.0, 0
        for s in seqs:
            b -= math.log2(self.prob(s))
            n += len(s) + 1
        return b / n


def ngram_bits(train, test, vocab, n: int = 3, alpha: float = 0.1) -> float:
    """Bits per chord of an add-alpha n-gram model with start and end symbols."""
    V = len(vocab) + 1
    cnt, ctx = Counter(), Counter()
    for s in train:
        seq = ["<s>"] * (n - 1) + list(s) + ["<e>"]
        for i in range(n - 1, len(seq)):
            h = tuple(seq[i - n + 1:i])
            cnt[(h, seq[i])] += 1
            ctx[h] += 1
    bits, m = 0.0, 0
    for s in test:
        seq = ["<s>"] * (n - 1) + list(s) + ["<e>"]
        for i in range(n - 1, len(seq)):
            h = tuple(seq[i - n + 1:i])
            bits -= math.log2((cnt[(h, seq[i])] + alpha) / (ctx[h] + alpha * V))
            m += 1
    return bits / m
