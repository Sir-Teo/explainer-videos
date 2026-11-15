"""Monochord's listener (Part 46 of *Music, Built*): expectation as prediction, in bits.

A melody is a list of key numbers relative to its tonic (0 = the tonic; octaves kept).  The model predicts each next
note from the notes before it, as Pearce's IDyOM does in outline: a variable-order Markov model whose orders are
blended by prediction by partial matching (PPM, escape method C), with a long-term model trained on a corpus and a
short-term model trained on the piece so far, the two combined by their uncertainty.

    PPM(max_order)                    the blended variable-order model: fit(sequences), distribution(context)
    Listener(corpus, max_order)       long-term + short-term models; listen(melody) -> per-note surprise (information
                                      content, -log2 p, bits) and uncertainty (entropy of the prediction, bits)
    syncopation(pattern, ...)         Longuet-Higgins and Lee's (1984) syncopation index on a 16-step bar
    saffran(words, n, rng)            a stream of tone 'words' concatenated at random (Saffran and colleagues 1999), and
                                      the transitional probabilities inside and across words

No manim here.  Checked in ``tests/music/test_listener.py``.
"""

from __future__ import annotations

import math
from collections import Counter, defaultdict

import numpy as np

ALPHABET = list(range(-12, 25))                      # pitches a melody may use, relative to the tonic


class PPM:
    """Prediction by partial matching over orders 0..max_order, escape method C, with exclusion; a uniform order -1
    over ``alphabet`` underneath, so every symbol has some probability."""

    def __init__(self, max_order: int = 4, alphabet=ALPHABET):
        self.k = max_order
        self.alphabet = list(alphabet)
        self.counts = [defaultdict(Counter) for _ in range(max_order + 1)]

    def update(self, seq, upto: int | None = None):
        seq = list(seq)
        for i in range(len(seq) if upto is None else upto):
            for o in range(self.k + 1):
                if i - o < 0:
                    break
                self.counts[o][tuple(seq[i - o:i])][seq[i]] += 1
        return self

    def fit(self, seqs):
        for s in seqs:
            self.update(s)
        return self

    def add(self, context, symbol):
        context = list(context)
        for o in range(self.k + 1):
            if len(context) < o:
                break
            self.counts[o][tuple(context[len(context) - o:])][symbol] += 1

    def distribution(self, context) -> dict:
        """P(next | context) by PPM-C with exclusion: start at the longest context seen, escape to shorter ones."""
        context = list(context)
        probs = {}
        mass = 1.0
        excluded = set()
        for o in range(min(self.k, len(context)), -1, -1):
            c = self.counts[o].get(tuple(context[len(context) - o:]) if o else ())
            if not c:
                continue
            items = {s: n for s, n in c.items() if s not in excluded}
            if not items:
                continue
            total = sum(items.values())
            types = len(items)
            esc = types / (total + types)
            for s, n in items.items():
                probs[s] = probs.get(s, 0.0) + mass * (1 - esc) * n / total
            excluded |= set(items)
            mass *= esc
        rest = [s for s in self.alphabet if s not in excluded]
        for s in rest:
            probs[s] = probs.get(s, 0.0) + mass / len(rest)
        z = sum(probs.values())
        return {s: p / z for s, p in probs.items()}


def entropy(dist: dict) -> float:
    return float(-sum(p * math.log2(p) for p in dist.values() if p > 0))


def combine(dists, bias: float = 2.0) -> dict:
    """IDyOM-style combination: weight each distribution by its relative entropy raised to -bias, so the more certain
    model counts for more."""
    hmax = math.log2(len(ALPHABET))
    ws = [(entropy(d) / hmax + 1e-9) ** (-bias) for d in dists]
    keys = set().union(*dists)
    out = {k: sum(w * d.get(k, 0.0) for w, d in zip(ws, dists)) / sum(ws) for k in keys}
    z = sum(out.values())
    return {k: v / z for k, v in out.items()}


class Listener:
    """A long-term model trained on a corpus, and a short-term model that learns the piece as it is heard."""

    def __init__(self, corpus, max_order: int = 4, short: bool = True):
        self.ltm = PPM(max_order).fit(corpus)
        self.k = max_order
        self.short = short

    def listen(self, melody) -> dict:
        stm = PPM(self.k)
        ic, h, p = [], [], []
        for i, x in enumerate(melody):
            ctx = melody[:i]
            d_l = self.ltm.distribution(ctx)
            d = combine([d_l, stm.distribution(ctx)]) if (self.short and i > 0) else d_l
            q = d.get(x, 1e-12)
            ic.append(float(-math.log2(q)))
            h.append(entropy(d))
            p.append(float(q))
            stm.add(ctx, x)
        return {"ic": ic, "entropy": h, "p": p, "mean_ic": float(np.mean(ic)), "mean_entropy": float(np.mean(h))}

    def expect(self, context, top: int = 5) -> list:
        d = self.ltm.distribution(context)
        return sorted(d.items(), key=lambda kv: -kv[1])[:top]


# --------------------------------------------------------------------------------------------- groove
METRIC_16 = [0, -4, -3, -4, -2, -4, -3, -4, -1, -4, -3, -4, -2, -4, -3, -4]       # Longuet-Higgins and Lee weights


def syncopation(onsets, steps: int = 16) -> int:
    """Longuet-Higgins and Lee's index: for each note followed by a rest (no onset) on a metrically stronger position
    before the next note, add the weight difference; summed over a cyclic bar."""
    on = sorted(set(int(o) % steps for o in onsets))
    if not on:
        return 0
    total = 0
    for i, a in enumerate(on):
        b = on[(i + 1) % len(on)] + (steps if i + 1 == len(on) else 0)
        rests = [r % steps for r in range(a + 1, b)]
        if not rests:
            continue
        strongest = max(METRIC_16[r] for r in rests)
        if strongest > METRIC_16[a]:
            total += strongest - METRIC_16[a]
    return int(total)


# --------------------------------------------------------------------------------------------- statistical learning
def saffran(words, n: int = 40, rng=None) -> dict:
    """Concatenate ``n`` tone words at random (no word twice in a row) and measure transitional probabilities:
    P(next tone | this tone) inside words and across word boundaries."""
    rng = rng or np.random.default_rng(0)
    seq, order = [], []
    last = None
    for _ in range(n):
        choices = [i for i in range(len(words)) if i != last]
        w = int(rng.choice(choices))
        order.append(w)
        seq += list(words[w])
        last = w
    pair = Counter(zip(seq, seq[1:]))
    first = Counter(seq[:-1])
    tp = {f"{a},{b}": pair[(a, b)] / first[a] for a, b in pair}
    inside = [pair[(w[i], w[i + 1])] / first[w[i]] for w in words for i in range(len(w) - 1)]
    across = [pair[(words[a][-1], words[b][0])] / first[words[a][-1]] for a in range(len(words)) for b in range(len(words))
              if a != b and pair[(words[a][-1], words[b][0])]]
    return {"sequence": seq, "order": order, "tp_inside": float(np.mean(inside)), "tp_across": float(np.mean(across)), "tp": tp}
