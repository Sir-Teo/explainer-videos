"""Part 23's text experiments: byte-pair encoding, the unigram language model, small language models per tokenizer
at equal compute, and entropy patching driven by a byte model.

Everything reads Part 1's novels through its ``compute.text`` (thirty Project Gutenberg books; the scoreboard's
passage is chapter 2 of *The Maltese Falcon*).  Text is normalized the same way for every tokenizer: newlines become
spaces and runs of spaces one space, so "characters" means the same thing in every bits-per-character figure.
"""

from __future__ import annotations

import collections
import math
import os

import numpy as np

SCALE = float(os.environ.get("AI23_SCALE", "1"))  # < 1: a quick smoke test of every code path (its own cache)


def rng(seed: int) -> np.random.Generator:
    return np.random.Generator(np.random.PCG64(seed))


def norm(t: str) -> str:
    """Newlines to spaces, runs of spaces to one: the text every tokenizer here reads."""
    return " ".join(w for w in t.replace("\n", " ").split(" ") if w)


def words_of(t: str) -> list[str]:
    """The text as words, each with its leading space (so a word knows it starts a word)."""
    return [" " + w for w in norm(t).split(" ") if w]


def sample_text(n_blocks: int, block: int, seed: int) -> str:
    from videos.ai.ai1 import compute as c1

    train = c1.text("train")
    g = rng(seed)
    starts = g.integers(0, len(train) - block, n_blocks)
    return " ".join(train[s:s + block] for s in starts)


# ---------------------------------------------------------------------------
# Byte-pair encoding (Gage 1994; Sennrich, Haddow & Birch 2016)
# ---------------------------------------------------------------------------
def learn_bpe(text: str, merges: int):
    """BPE over words (a word carries its leading space): the merges in order, and how many times each pair occurred
    when it was merged (each merge shortens the text by exactly that many symbols)."""
    words = collections.Counter(words_of(text))
    seqs = [list(w) for w in words]
    counts = list(words.values())
    pairs = collections.Counter()
    where = collections.defaultdict(set)
    for i, s in enumerate(seqs):
        for a, b in zip(s, s[1:]):
            pairs[(a, b)] += counts[i]
            where[(a, b)].add(i)
    out, freq = [], []
    for _ in range(merges):
        if not pairs:
            break
        (a, b), n = pairs.most_common(1)[0]
        if n < 2:
            break
        out.append((a, b))
        freq.append(int(n))
        ab = a + b
        for i in sorted(where[(a, b)]):
            s, c = seqs[i], counts[i]
            for x, y in zip(s, s[1:]):  # remove this word's old pairs
                pairs[(x, y)] -= c
                if pairs[(x, y)] <= 0:
                    del pairs[(x, y)]
                where[(x, y)].discard(i)
            j, new = 0, []
            while j < len(s):
                if j + 1 < len(s) and s[j] == a and s[j + 1] == b:
                    new.append(ab)
                    j += 2
                else:
                    new.append(s[j])
                    j += 1
            seqs[i] = new
            for x, y in zip(new, new[1:]):
                pairs[(x, y)] += c
                where[(x, y)].add(i)
    return out, freq


def apply_bpe(word: str, ranks: dict) -> list[str]:
    s = list(word)
    while len(s) > 1:
        best = min(((ranks.get((x, y), 1e9), k) for k, (x, y) in enumerate(zip(s, s[1:]))), default=(1e9, -1))
        if best[0] == 1e9:
            break
        k = best[1]
        s = s[:k] + [s[k] + s[k + 1]] + s[k + 2:]
    return s


class BPE:
    def __init__(self, merges, n: int):
        self.ranks = {tuple(p): i for i, p in enumerate(merges[:n])}
        self.cache: dict = {}

    def word(self, w: str) -> list[str]:
        if w not in self.cache:
            self.cache[w] = apply_bpe(w, self.ranks)
        return self.cache[w]

    def __call__(self, t: str) -> list[str]:
        out = []
        for w in words_of(t):
            out += self.word(w)
        return out


def wordpiece_merges(text: str, n: int) -> list[str]:
    """The first ``n`` merges under WordPiece's rule (Schuster & Nakajima 2012, as BERT's tokenizer was built): merge
    the pair with the highest count(ab) / (count(a) count(b)), the pair whose merge raises the likelihood most."""
    words = collections.Counter(words_of(text))
    seqs = {w: list(w) for w in words}
    out = []
    for _ in range(n):
        pairs, units = collections.Counter(), collections.Counter()
        for w, s in seqs.items():
            c = words[w]
            for u in s:
                units[u] += c
            for a, b in zip(s, s[1:]):
                pairs[(a, b)] += c
        best = max(((cnt / (units[a] * units[b]), cnt, a, b) for (a, b), cnt in pairs.items() if cnt >= 50),
                   default=None)
        if best is None:
            break
        _, _, a, b = best
        out.append(a + b)
        for w, s in seqs.items():
            j, new = 0, []
            while j < len(s):
                if j + 1 < len(s) and s[j] == a and s[j + 1] == b:
                    new.append(a + b)
                    j += 2
                else:
                    new.append(s[j])
                    j += 1
            seqs[w] = new
    return out


# ---------------------------------------------------------------------------
# The unigram language model (Kudo 2018), trained by EM and pruned
# ---------------------------------------------------------------------------
class Unigram:
    """A vocabulary of pieces with probabilities; a word's segmentation is the most probable way to write it as a
    sequence of pieces (Viterbi), and the word's probability sums over every way (the forward algorithm)."""

    MAXLEN = 12

    def __init__(self, logp: dict[str, float]):
        self.logp = dict(logp)
        self.cache: dict = {}

    def word(self, w: str) -> list[str]:
        if w not in self.cache:
            self.cache[w] = viterbi(w, self.logp, self.MAXLEN)[1]
        return self.cache[w]

    def __call__(self, t: str) -> list[str]:
        out = []
        for w in words_of(t):
            out += self.word(w)
        return out

    def sample(self, w: str, g: np.random.Generator, alpha: float = 1.0) -> list[str]:
        """A random segmentation of ``w`` with probability proportional to its pieces' probabilities to the power
        ``alpha`` (subword regularization): forward filtering, backward sampling."""
        n = len(w)
        a = [0.0] + [-math.inf] * n
        for j in range(1, n + 1):
            terms = [a[i] + alpha * self.logp[w[i:j]] for i in range(max(0, j - self.MAXLEN), j) if w[i:j] in self.logp]
            a[j] = _lse(terms)
        out, j = [], n
        while j > 0:
            cand = [(i, a[i] + alpha * self.logp[w[i:j]]) for i in range(max(0, j - self.MAXLEN), j) if w[i:j] in self.logp]
            z = _lse([c for _, c in cand])
            p = np.array([math.exp(c - z) for _, c in cand])
            i = cand[int(g.choice(len(cand), p=p / p.sum()))][0]
            out.append(w[i:j])
            j = i
        return out[::-1]


def _lse(xs):
    if not xs:
        return -math.inf
    m = max(xs)
    return m + math.log(sum(math.exp(x - m) for x in xs)) if m > -math.inf else -math.inf


def viterbi(w: str, logp: dict, maxlen: int, exclude: str | None = None):
    """The most probable segmentation of ``w`` (and its log-probability), optionally without the piece ``exclude``."""
    n = len(w)
    best = [0.0] + [-math.inf] * n
    back = [0] * (n + 1)
    for j in range(1, n + 1):
        for i in range(max(0, j - maxlen), j):
            piece = w[i:j]
            p = None if piece == exclude else logp.get(piece)
            if p is not None and best[i] + p > best[j]:
                best[j], back[j] = best[i] + p, i
    out, j = [], n
    while j > 0:
        out.append(w[back[j]:j])
        j = back[j]
    return best[n], out[::-1]


def learn_unigram(text: str, sizes=(4096, 1024), seed_size=40_000, shrink=0.75, em_iters=2, log=print):
    """Kudo's recipe: a big seed vocabulary of frequent substrings, then alternate EM (expected piece counts over all
    segmentations; probabilities from the counts) with pruning (drop the pieces whose loss costs the likelihood least,
    keeping every single character).  Returns the vocabularies at each size in ``sizes`` and a replay of the
    pruning: (vocabulary size, average log-likelihood per character)."""
    words = collections.Counter(words_of(text))
    L = Unigram.MAXLEN
    sub = collections.Counter()
    for w, c in words.items():
        for i in range(len(w)):
            for j in range(i + 1, min(len(w), i + L) + 1):
                sub[w[i:j]] += c
    chars = {ch for w in words for ch in w}
    multi = sorted((s for s in sub if len(s) > 1 and sub[s] >= 2), key=lambda s: (-sub[s] * len(s), s))[:seed_size]
    pieces = sorted(chars) + multi
    total = sum(sub[s] for s in pieces)
    logp = {s: math.log(sub[s] / total) for s in pieces}
    n_chars = sum(len(w) * c for w, c in words.items())
    wl = list(words.items())
    replay, out = [], {}
    targets = sorted(sizes, reverse=True)
    while True:
        for _ in range(em_iters):
            expected = collections.defaultdict(float)
            ll = 0.0
            for w, c in wl:  # forward-backward over the word's lattice of pieces
                n = len(w)
                a = [0.0] + [-math.inf] * n
                arcs = []
                for j in range(1, n + 1):
                    terms = []
                    for i in range(max(0, j - L), j):
                        p = logp.get(w[i:j])
                        if p is not None:
                            arcs.append((i, j, p))
                            terms.append(a[i] + p)
                    a[j] = _lse(terms)
                b = [-math.inf] * n + [0.0]
                for i, j, p in sorted(arcs, key=lambda t: -t[0]):
                    b[i] = _lse([b[i], p + b[j]])
                z = a[n]
                ll += c * z
                for i, j, p in arcs:
                    expected[w[i:j]] += c * math.exp(a[i] + p + b[j] - z)
            tot = sum(expected.values())
            logp = {s: math.log(max(expected.get(s, 0.0), 1e-6) / tot) for s in logp
                    if expected.get(s, 0) > 1e-3 or s in chars}
        replay.append((len(logp), ll / n_chars))
        log(f"    unigram: {len(logp)} pieces, {ll / n_chars:.4f} nats per character")
        while targets and len(logp) <= targets[0] * 1.0001:
            out[targets[0]] = dict(logp)
            targets.pop(0)
        if not targets:
            break
        # the loss of each piece: its expected count times how much worse its best re-segmentation without it is
        loss = {}
        for s, p in logp.items():
            if len(s) == 1:
                continue
            alt, _ = viterbi(s, logp, L, exclude=s)
            loss[s] = math.exp(p) * (p - alt)
        keep_n = max(targets[0], int(len(logp) * shrink)) - len(chars)
        kept = sorted(loss, key=lambda s: (-loss[s], s))[:keep_n]
        logp = {s: logp[s] for s in sorted(chars) + kept}
    return out, replay


# ---------------------------------------------------------------------------
# Language models per tokenizer, at equal compute
# ---------------------------------------------------------------------------
LM_CFG = dict(d=96, layers=3, heads=4, seq=128)
LM_BATCH = 16
LM_BUDGET_STEPS = 1000  # the byte model's steps; every other model gets the same FLOPs


def byte_ids(t: str) -> np.ndarray:
    return np.frombuffer(t.encode("utf-8"), np.uint8).astype(np.int64)


def ids_for(tok, t: str, table: dict) -> np.ndarray:
    pieces = tok(t)
    unk = table["<unk>"]
    return np.array([table.get(p, unk) for p in pieces], np.int64)


def train_lm(name: str, ids_train: np.ndarray, ids_valid: np.ndarray, vocab: int, seed: int, ckpt=None, threads=1):
    """One small transformer (explainer.lm.pocket), its training horizon set so it spends the byte model's FLOPs."""
    import torch

    from explainer.lm import pocket

    cfg = pocket.Config(vocab=vocab, **LM_CFG)
    torch.manual_seed(seed)
    counts = pocket.PocketGPT(cfg).count()
    byte_cfg = pocket.Config(vocab=256, **LM_CFG)
    budget = pocket.flops_per_token(pocket.PocketGPT(byte_cfg).count(), byte_cfg) * LM_BATCH * cfg.seq * \
        max(20, int(LM_BUDGET_STEPS * SCALE))
    tokens = int(budget / pocket.flops_per_token(counts, cfg))
    run = pocket.Run(model=cfg, lr=3e-3, batch=LM_BATCH, tokens=tokens, warmup=50, schedule="cosine", seed=seed,
                     eval_batches=8, log_every=10)
    data = pocket.TokenStream(ids_train, ids_valid, cfg.seq, seed=seed)
    res = pocket.train(run, data, threads=threads, ckpt=ckpt, ckpt_every=100)
    return res, budget


def nll_per_token(model, ids: np.ndarray, seq: int) -> np.ndarray:
    """The surprise (nats) of every token after the first, scored with sliding windows of ``seq`` tokens: each token
    is predicted with at least half a window of context (all of it, at the start)."""
    import torch
    import torch.nn.functional as F

    out = np.full(len(ids), np.nan)
    stride = seq // 2
    model.eval()
    with torch.no_grad():
        start = 0
        while True:
            x = torch.tensor(ids[start:start + seq + 1])[None]
            if x.shape[1] < 2:
                break
            lp = F.log_softmax(model(x[:, :-1]), -1)[0]
            nll = -lp.gather(1, x[0, 1:, None])[:, 0].numpy()
            first = 0 if start == 0 else stride
            out[start + 1 + first:start + 1 + len(nll)] = nll[first:]
            if start + seq + 1 >= len(ids):
                break
            start += stride
    return out


def entropies(model, ids: np.ndarray, seq: int):
    """Per-position next-symbol entropy (bits) and the surprise of what came (bits), sliding windows as above."""
    import torch
    import torch.nn.functional as F

    H = np.full(len(ids), np.nan)
    S = np.full(len(ids), np.nan)
    stride = seq // 2
    model.eval()
    with torch.no_grad():
        start = 0
        while True:
            x = torch.tensor(ids[start:start + seq + 1])[None]
            lp = F.log_softmax(model(x[:, :-1]), -1)[0]
            h = -(lp.exp() * lp).sum(-1).numpy() / math.log(2)
            s = -lp.gather(1, x[0, 1:, None])[:, 0].numpy() / math.log(2)
            first = 0 if start == 0 else stride
            H[start + 1 + first:start + 1 + len(s)] = h[first:]
            S[start + 1 + first:start + 1 + len(s)] = s[first:]
            if start + seq + 1 >= len(ids):
                break
            start += stride
    return H, S
