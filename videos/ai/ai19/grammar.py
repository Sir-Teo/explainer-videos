"""Constrained decoding with an automaton (Part 19's ``grammar`` item), in the manner of Outlines (Willard & Louf 2023):
a pattern compiled to a deterministic finite automaton over characters, then an index from (automaton state, token)
to the next state, built once for the model's whole vocabulary.  At each step the allowed tokens are a table lookup;
the rest get probability zero.

The pattern is a list of atoms: a literal string, or a character class repeated between a minimum and a maximum
number of times (enough for the records generated here; regular expressions in general compile the same way).
"""

from __future__ import annotations

import re

import numpy as np

# a one-line record: {"name": "Holmes", "age": 47}
RECORD = [("lit", '{"name": "'), ("cls", "A-Z", 1, 1), ("cls", "a-z", 1, 11), ("lit", '", "age": '),
          ("cls", "1-9", 1, 1), ("cls", "0-9", 0, 1), ("lit", "}")]
RECORD_RE = re.compile(r'\{"name": "[A-Z][a-z]{1,11}", "age": [1-9][0-9]?\}')
EXAMPLES = ['{"name": "Holmes", "age": 47}', '{"name": "Watson", "age": 39}', '{"name": "Irene", "age": 30}']
PROMPT = "The register of the inn, one guest to a line:\n" + "\n".join(EXAMPLES) + "\n"


def _in(cls: str, c: str) -> bool:
    lo, hi = cls.split("-")
    return lo <= c <= hi


class Automaton:
    """States are sets of (atom, count) positions; built lazily (the subset construction)."""

    def __init__(self, atoms):
        self.atoms = atoms
        self.start = self.close({(0, 0)})
        self.accept = (len(atoms), 0)

    def complete(self, i, k):
        a = self.atoms[i]
        return k == len(a[1]) if a[0] == "lit" else k >= a[2]

    def close(self, S):
        S, todo = set(S), list(S)
        while todo:
            i, k = todo.pop()
            if i < len(self.atoms) and self.complete(i, k) and (i + 1, 0) not in S:
                S.add((i + 1, 0))
                todo.append((i + 1, 0))
        return frozenset(S)

    def step(self, S, c):
        out = set()
        for i, k in S:
            if i >= len(self.atoms):
                continue
            a = self.atoms[i]
            if a[0] == "lit":
                if k < len(a[1]) and a[1][k] == c:
                    out.add((i, k + 1))
            elif k < a[3] and _in(a[1], c):
                out.add((i, k + 1))
        return self.close(out) if out else None

    def run(self, S, text):
        for c in text:
            S = self.step(S, c)
            if S is None:
                return None
        return S

    def accepting(self, S):
        return self.accept in S

    def final(self, S):
        """Accepting with nothing more allowed: the record is complete."""
        return self.accepting(S) and all(i >= len(self.atoms) for i, _ in S)


def token_strings():
    from explainer.ai import novels as N

    tok = N.tokenizer()
    V = tok.get_vocab_size()
    out = []
    for i in range(V):
        s = N.decode([i])
        out.append(None if ("�" in s or s.startswith("<|") or s == "") else s)
    return out


def build_index(auto: Automaton, strings):
    """For every reachable state: the next state of every token (or -1 where the token is not allowed)."""
    states = {auto.start: 0}
    order = [auto.start]
    table = []
    q = 0
    while q < len(order):
        S = order[q]
        row = np.full(len(strings), -1, np.int32)
        for t, s in enumerate(strings):
            if s is None:
                continue
            nxt = auto.run(S, s)
            if nxt is None:
                continue
            if nxt not in states:
                states[nxt] = len(order)
                order.append(nxt)
            row[t] = states[nxt]
        table.append(row)
        q += 1
    return np.stack(table), order


def generate(engine, prompt_ids, n_max, seed, index=None, order=None, auto=None, stop_newline=None, temp=1.0):
    """Sample up to ``n_max`` tokens; with ``index``, only tokens the automaton allows (stopping once the record is
    complete); without, stopping at the first newline.  Returns the token ids."""
    import torch

    g = np.random.default_rng(seed)
    with torch.inference_mode():
        c = engine.new_cache(1, len(prompt_ids) + n_max + 1)
        z = engine.forward(torch.tensor([prompt_ids]), c, logits="last")[0]
        out, st = [], 0
        for _ in range(n_max):
            p = torch.softmax(z.double() / temp, -1).numpy()
            if index is not None:
                allowed = index[st] >= 0
                p = np.where(allowed, p, 0.0)
                if p.sum() <= 0:
                    break
            cdf = np.cumsum(p)
            t = int(min(np.searchsorted(cdf, g.random() * cdf[-1], side="right"), len(p) - 1))
            out.append(t)
            if index is not None:
                st = int(index[st][t])
                if auto.final(order[st]):
                    break
            elif stop_newline is not None and stop_newline(t):
                break
            z = engine.forward(torch.tensor([[t]]), c, logits="last")[0]
    return out


# ---------------------------------------------------------------------------
# How masking reweights: a small language on Part 13's character model
# ---------------------------------------------------------------------------
NAMES = ["Spade", "Sam", "Samuel", "Archer", "Effie"]


def masked_vs_exact(probs_at, names=NAMES):
    """``probs_at(prefix)`` gives the character model's next-character distribution (a dict char -> p) after the
    context + ``prefix``.  A name ends where the next character is not a letter.  Exact: P(name) P(end | name),
    renormalized over the names (sampling the model and keeping only names).  Masked: at every character only the
    continuations some name allows are kept and renormalized, as constrained decoding does."""
    def end_p(d):
        return sum(p for ch, p in d.items() if not ch.isalpha())

    exact, masked = {}, {}
    for nm in names:
        pr, mk = 1.0, 1.0
        for k in range(len(nm) + 1):
            d = probs_at(nm[:k])
            allowed = {n[k] for n in names if n.startswith(nm[:k]) and len(n) > k}
            ends_here = nm[:k] in names
            tot = sum(d.get(ch, 0.0) for ch in allowed) + (end_p(d) if ends_here else 0.0)
            if k < len(nm):
                pr *= d.get(nm[k], 0.0)
                mk *= d.get(nm[k], 0.0) / tot
            else:
                pr *= end_p(d)
                mk *= end_p(d) / tot
        exact[nm], masked[nm] = pr, mk
    Z = sum(exact.values())
    return {k: v / Z for k, v in exact.items()}, masked
