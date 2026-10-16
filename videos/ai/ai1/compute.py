"""Precompute everything numerical in Part 1 of the AI series ("The Guessing Game").

    python -m videos.ai.ai1.compute              # everything missing (downloads ~40 MB of books and the models)
    python -m videos.ai.ai1.compute letters game # specific items
    python -m videos.ai.ai1.compute --force lms  # recompute

Results are cached in ``.cache/ai1/<name>.json`` (+ ``.npz`` for arrays); scenes call ``load(name)``.  Every number
the narration quotes is computed here and asserted against the statement it illustrates.

The text: 30 public-domain novels from Project Gutenberg (BOOKS) are the "reading" every counting model learns from.
The test passage is chapter 2 of Dashiell Hammett's *The Maltese Falcon* (1930), which entered the US public domain
on 1 January 2026 and was posted to Gutenberg that day (eBook #77600), after every language model below was trained.
Two alphabets: Shannon's 27 symbols (a-z and space: case and punctuation dropped), and the text as printed.

Items:
    corpus     download and clean the books and the passage
    letters    letter frequencies (27 symbols) and their entropy
    bigram     the 27 x 27 table of P(next letter | letter) and the conditional entropy
    orders     N-gram entropies F_N: on the books themselves (plug-in) and on the passage (add-alpha smoothing)
    samples    text sampled from letter models of order 0..7 and a word model (Shannon's 1948 approximations)
    huffman    the Huffman code for the letter frequencies: merges, codewords, average length vs entropy
    arith      arithmetic coding of a short message under the order-3 letter model, step by step, exactly
    game       Shannon's 1951 guessing game played by a counting model: guess counts, and Shannon's two bounds
    mi         mutual information between letters d apart, d = 1 .. 3000
    kl         fitting one Gaussian to a two-peaked density by forward and by reverse KL
    softmax    gradient descent on logits toward observed frequencies (the cross-entropy gradient q - p)
    raw        the passage as printed: counting models of order 0..7 and gzip / bzip2 / xz, in bits per character
    lms        language models on the passage: bits per character, and per-token surprise for one paragraph
    probes     next-token distributions for prompts that take knowledge to complete
    context    the surprise of one word with and without the paragraphs before it (memory)
    vectors    GPT-2's vectors for a few words, and random directions in 3 and 768 dimensions (Part 2's teaser)
    scoreboard the series' scoreboard rows, assembled from the items above
"""

from __future__ import annotations

import argparse
import bz2
import collections
import gzip
import heapq
import json
import lzma
import math
import os
import re
import subprocess
import time
import unicodedata
from fractions import Fraction
from pathlib import Path

import numpy as np

from explainer.tts import REPO_ROOT

DATA_DIR = REPO_ROOT / ".cache" / "ai1"
BOOK_DIR = DATA_DIR / "books"
GUTENBERG = "https://www.gutenberg.org/cache/epub/{n}/pg{n}.txt"

# The reading: 30 novels (Gutenberg eBook numbers), all long in the public domain.
BOOKS = {
    1342: "Pride and Prejudice", 98: "A Tale of Two Cities", 2701: "Moby Dick", 1661: "The Adventures of Sherlock Holmes",
    1400: "Great Expectations", 84: "Frankenstein", 345: "Dracula", 174: "The Picture of Dorian Gray",
    1260: "Jane Eyre", 145: "Middlemarch", 158: "Emma", 768: "Wuthering Heights", 2852: "The Hound of the Baskervilles",
    1184: "The Count of Monte Cristo", 2600: "War and Peace", 120: "Treasure Island", 43: "Jekyll and Hyde",
    36: "The War of the Worlds", 35: "The Time Machine", 219: "Heart of Darkness", 76: "Huckleberry Finn",
    74: "Tom Sawyer", 2554: "Crime and Punishment", 28054: "The Brothers Karamazov", 64317: "The Great Gatsby",
    1952: "The Yellow Wallpaper", 160: "The Awakening", 514: "Little Women", 46: "A Christmas Carol",
    4300: "Ulysses",
}
FALCON = 77600  # The Maltese Falcon (Hammett, 1930): Gutenberg, 1 January 2026
ALPHA27 = " abcdefghijklmnopqrstuvwxyz"
SHANNON_SENTENCE = ("there is no reverse on a motorcycle a friend of mine found this out rather dramatically the "
                    "other day")  # Shannon (1951), the example sentence of the guessing experiment


def rng(seed: int) -> np.random.Generator:
    return np.random.Generator(np.random.PCG64(seed))


# ---------------------------------------------------------------------------
# Cache helpers
# ---------------------------------------------------------------------------
def path(name: str) -> Path:
    return DATA_DIR / f"{name}.json"


_loaded: dict = {}


def load(name: str) -> dict:
    if name not in _loaded:
        p = path(name)
        if not p.exists():
            raise FileNotFoundError(f"{p} missing: run `python -m videos.ai.ai1.compute {name}`")
        _loaded[name] = json.loads(p.read_text())
        npz = p.with_suffix(".npz")
        if npz.exists():
            with np.load(npz) as z:
                _loaded[name].update({k: z[k] for k in z.files})
    return _loaded[name]


def _save(name: str, out: dict) -> None:
    arrays = {k: v for k, v in out.items() if isinstance(v, np.ndarray)}
    rest = {k: v for k, v in out.items() if k not in arrays}
    tmp = path(name).with_suffix(".tmp.json")
    tmp.write_text(json.dumps(rest, ensure_ascii=False, indent=1, default=float))
    tmp.replace(path(name))
    if arrays:
        np.savez_compressed(path(name).with_suffix(".tmp.npz"), **arrays)
        path(name).with_suffix(".tmp.npz").replace(path(name).with_suffix(".npz"))


def _download(url: str, dst: Path) -> Path:
    if dst.exists() and dst.stat().st_size > 0:
        return dst
    dst.parent.mkdir(parents=True, exist_ok=True)
    for attempt in range(5):  # Gutenberg resets the odd connection
        r = subprocess.run(["curl", "-sS", "-L", "--retry", "5", "--retry-all-errors", "-m", "600", "-o",
                            str(dst) + ".part", url])
        if r.returncode == 0:
            break
        time.sleep(2 ** (attempt + 1))
    else:
        raise RuntimeError(f"could not download {url}")
    Path(str(dst) + ".part").replace(dst)
    return dst


# ---------------------------------------------------------------------------
# The text
# ---------------------------------------------------------------------------
QUOTES = str.maketrans({"‘": "'", "’": "'", "“": '"', "”": '"', "–": "-", " ": " "})


def strip_gutenberg(t: str) -> str:
    t = t.replace("\r", "")
    a = re.search(r"\*\*\* ?START OF (THE|THIS) PROJECT GUTENBERG EBOOK[^\n]*\n", t)
    b = re.search(r"\*\*\* ?END OF (THE|THIS) PROJECT GUTENBERG EBOOK", t)
    return t[a.end() if a else 0: b.start() if b else len(t)]


def clean(t: str) -> str:
    """Paragraphs on single lines (separated by one newline), italics marks dropped, ASCII quotes, dashes kept."""
    t = t.translate(QUOTES).replace("_", "")
    paras = [" ".join(p.split()) for p in re.split(r"\n\s*\n", t)]
    return "\n".join(p for p in paras if p)


def to27(t: str) -> str:
    """Shannon's alphabet: 26 lowercase letters and the space; accents folded, everything else a space."""
    t = unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode().lower()
    return " ".join(re.sub(r"[^a-z]+", " ", t).split())


def falcon_chapter(t: str, n: int) -> str:
    """Chapter n of The Maltese Falcon, without its number and title lines."""
    lines = t.split("\n")
    heads = [i for i, ln in enumerate(lines) if re.fullmatch(r" {20,}\d+ *", ln)]
    i, j = heads[n - 1], heads[n] if n < len(heads) else len(lines)
    body = "\n".join(lines[i + 1:j])
    body = re.sub(r"^\s*\n\s+[A-Z][A-Z ,'’.&-]+\n", "", body, count=1)  # the chapter title
    body = re.sub(r"\n\s*(\*\s+){4}\*\s*\n", "\n\n", body)  # the scene-break stars
    return clean(body)


def compute_corpus():
    books = {}
    for n, title in BOOKS.items():
        raw = _download(GUTENBERG.format(n=n), BOOK_DIR / f"{n}.txt").read_text(encoding="utf-8", errors="replace")
        books[n] = clean(strip_gutenberg(raw))
        assert len(books[n]) > 30_000, (n, title, len(books[n]))
    raw = _download(GUTENBERG.format(n=FALCON), BOOK_DIR / f"{FALCON}.txt").read_text(encoding="utf-8")
    assert "Release date: January 1, 2026" in raw and "The Maltese falcon" in raw
    body = strip_gutenberg(raw)
    passage = falcon_chapter(body, 2)
    assert passage.startswith("A TELEPHONE-BELL rang in darkness.") and len(passage) > 20_000, passage[:80]
    # 5% of the reading (every 20th paragraph block) is held back to choose the smoothing
    train, valid = [], []
    for n in BOOKS:
        paras = books[n].split("\n")
        for k in range(0, len(paras), 40):
            (valid if (k // 40) % 20 == 7 else train).append("\n".join(paras[k:k + 40]))
    train_t, valid_t = "\n".join(train), "\n".join(valid)
    (DATA_DIR / "train.txt").write_text(train_t)
    (DATA_DIR / "valid.txt").write_text(valid_t)
    (DATA_DIR / "passage.txt").write_text(passage)
    return dict(n_books=len(BOOKS), titles=[BOOKS[n] for n in BOOKS], train_chars=len(train_t),
                valid_chars=len(valid_t), passage_chars=len(passage), passage_head=passage[:600],
                train27_chars=len(to27(train_t)), passage27_chars=len(to27(passage)))


_text_cache: dict = {}


def text(kind: str) -> str:
    """'train', 'valid', 'passage' (as printed) or the same + '27' (Shannon's alphabet)."""
    if kind not in _text_cache:
        base = kind.removesuffix("27")
        if not (DATA_DIR / f"{base}.txt").exists():
            _save("corpus", compute_corpus())
        t = (DATA_DIR / f"{base}.txt").read_text()
        _text_cache[kind] = to27(t) if kind.endswith("27") else t
    return _text_cache[kind]


def codes27(t: str) -> np.ndarray:
    lut = np.zeros(128, np.int64)
    for i, ch in enumerate(ALPHA27):
        lut[ord(ch)] = i
    return lut[np.frombuffer(t.encode("ascii"), np.uint8)]


# ---------------------------------------------------------------------------
# Counting models
# ---------------------------------------------------------------------------
def entropy(p) -> float:
    p = np.asarray(p, float)
    p = p[p > 0]
    return float(-(p * np.log2(p)).sum())


def multiplier(order: int, K: int) -> int:
    """Contexts are numbers in base K while they fit in 63 bits, and hashed (wrapping arithmetic) beyond."""
    return K if K ** (order + 1) < 2**62 else 1_000_003


def context_keys(a: np.ndarray, order: int, K: int) -> np.ndarray:
    """For each position i >= order: the integer encoding of a[i-order:i] (the context of a[i])."""
    n, mult = len(a), multiplier(order, K)
    key = np.zeros(n - order, np.int64)
    with np.errstate(over="ignore"):
        for j in range(order):
            key = key * mult + a[j:n - order + j]
    return key


class NGram:
    """Counts of (context of `order` symbols, next symbol); probabilities with add-alpha smoothing."""

    def __init__(self, a: np.ndarray, order: int, K: int):
        self.order, self.K, self.mult = order, K, multiplier(order, K)
        ctx = context_keys(a, order, K)
        with np.errstate(over="ignore"):
            joint = ctx * K + a[order:]
        self.jk, self.jc = np.unique(joint, return_counts=True)
        self.ck, self.cc = np.unique(ctx, return_counts=True)

    def key(self, context) -> int:
        ctx = np.int64(0)
        with np.errstate(over="ignore"):
            for s in list(context)[len(context) - self.order:] if self.order else []:
                ctx = ctx * np.int64(self.mult) + np.int64(s)
        return ctx

    def counts(self, ctx: np.ndarray, nxt: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        def look(keys, table, cnt):
            i = np.searchsorted(table, keys)
            i = np.minimum(i, len(table) - 1)
            return np.where(table[i] == keys, cnt[i], 0)
        with np.errstate(over="ignore"):
            joint = ctx * self.K + nxt
        return look(joint, self.jk, self.jc), look(ctx, self.ck, self.cc)

    def bits(self, b: np.ndarray, alpha: float) -> np.ndarray:
        """-log2 P(b[i] | b[i-order:i]) for i >= order."""
        ctx = context_keys(b, self.order, self.K)
        nj, nc = self.counts(ctx, b[self.order:])
        return -np.log2((nj + alpha) / (nc + alpha * self.K))

    def dist(self, context: np.ndarray, alpha: float) -> np.ndarray:
        assert len(context) >= self.order
        nj, nc = self.counts(np.full(self.K, self.key(context), np.int64), np.arange(self.K))
        return (nj + alpha) / (nc + alpha * self.K)


ALPHAS = [1.0, 0.3, 0.1, 0.03, 0.01, 0.003, 0.001]


def fit_orders(train: np.ndarray, valid: np.ndarray, test: np.ndarray, K: int, orders) -> list[dict]:
    """For each order: the plug-in entropy on the training text, the best alpha on the validation text, and the
    cross-entropy (bits per symbol) on the test text with that alpha."""
    out = []
    for N in orders:
        m = NGram(train, N, K)
        # plug-in conditional entropy on the training text itself: H(joint) - H(context)
        n = m.jc.sum()
        h_joint = entropy(m.jc / n)
        h_ctx = entropy(m.cc / m.cc.sum())
        plug = h_joint - h_ctx
        val = {a: float(m.bits(valid, a).mean()) for a in ALPHAS}
        best = min(val, key=val.get)
        out.append(dict(order=N, plugin=plug, alpha=best, valid=val[best], test=float(m.bits(test, best).mean()),
                        contexts=int(len(m.ck)), seen_frac=float(np.isin(context_keys(test, N, K), m.ck).mean())))
        print(f"    order {N}: plug-in {plug:.3f}  alpha {best:g}  valid {val[best]:.3f}  test {out[-1]['test']:.3f}",
              flush=True)
    return out


# ---------------------------------------------------------------------------
# Letters
# ---------------------------------------------------------------------------
def compute_letters():
    a = codes27(text("train27"))
    cnt = np.bincount(a, minlength=27)
    p = cnt / cnt.sum()
    H = entropy(p)
    assert 4.0 < H < 4.2, H  # English letters with the space: about 4.1 bits (Shannon's F1 = 4.03 for 27 letters)
    order = np.argsort(-p)
    surprise = -np.log2(p)
    # the passage's own letter frequencies, coded with the books' frequencies (and with no knowledge at all)
    pc = np.bincount(codes27(text("passage27")), minlength=27)
    pp = pc / pc.sum()
    H_pass = entropy(pp)
    CE_books = float(-(pp * np.log2(p)).sum())
    CE_uniform = math.log2(27)
    assert 0 < CE_books - H_pass < 0.05 and abs(CE_uniform - H_pass - (math.log2(27) - H_pass)) < 1e-12
    return dict(counts=cnt, p=p, H=H, H_uniform=math.log2(27), order=order, surprise=surprise,
                n=int(cnt.sum()), top="".join(ALPHA27[i] for i in order[:12]), passage_p=pp, H_passage=H_pass,
                CE_books=CE_books, KL_books=CE_books - H_pass, KL_uniform=CE_uniform - H_pass)


def compute_bigram():
    a = codes27(text("train27"))
    joint = np.bincount(a[:-1] * 27 + a[1:], minlength=729).reshape(27, 27).astype(float)
    cond = joint / joint.sum(1, keepdims=True)
    p1 = joint.sum(1) / joint.sum()
    H_cond = float(sum(p1[i] * entropy(cond[i]) for i in range(27)))
    H1 = entropy(p1)
    assert H_cond < H1 - 0.6, (H_cond, H1)
    after_q = cond[ALPHA27.index("q")]
    assert after_q[ALPHA27.index("u")] > 0.95  # q is almost always followed by u
    row_H = np.array([entropy(cond[i]) for i in range(27)])
    return dict(cond=cond, joint=joint / joint.sum(), H_cond=H_cond, H1=H1, row_H=row_H,
                q_u=float(after_q[ALPHA27.index("u")]))


def compute_orders():
    tr, va, te = codes27(text("train27")), codes27(text("valid27")), codes27(text("passage27"))
    rows = fit_orders(tr, va, te, 27, range(0, 15))
    plug = [r["plugin"] for r in rows]
    test = [r["test"] for r in rows]
    best = int(np.argmin(test))
    assert all(x > y for x, y in zip(plug, plug[1:]))  # on the books themselves, more context always helps...
    assert plug[-1] < 0.5  # ...until the books are nearly memorized
    assert 3 <= best <= 6 and test[-1] > test[best] + 0.5  # on new text, too much context hurts
    return dict(rows=rows, best=best, best_bits=test[best], shannon_27=[4.76, 4.03, 3.32, 3.1])


def compute_samples():
    tr = codes27(text("train27"))
    g = rng(1948)
    out = {}
    out["0"] = "".join(ALPHA27[i] for i in g.integers(0, 27, 90))
    seed = list(codes27("it was the "))
    models = {N: NGram(tr, N - 1, 27) for N in range(1, 8)}
    for N in (1, 2, 3, 5, 7):
        seq = list(seed)
        for _ in range(120):
            for M in range(N, 0, -1):  # an unseen context (rare) backs off to a shorter one
                ctx = np.array(seq[len(seq) - (M - 1):] if M > 1 else [], np.int64)
                d = models[M].dist(ctx, 0.0)
                if np.isfinite(d).all() and d.sum() > 0:
                    break
            seq.append(int(g.choice(27, p=d / d.sum())))
        out[str(N)] = "".join(ALPHA27[i] for i in seq[len(seed):]).strip()
    # Shannon's word approximations: words drawn by frequency, then each word given the previous one
    words = text("train27").split()
    wc = collections.Counter(words)
    vocab = list(wc)
    pw = np.array([wc[w] for w in vocab], float)
    pw /= pw.sum()
    out["w1"] = " ".join(vocab[i] for i in g.choice(len(vocab), 18, p=pw))
    follow = collections.defaultdict(collections.Counter)
    for x, y in zip(words, words[1:]):
        follow[x][y] += 1
    w, seq = "the", []
    for _ in range(18):
        nxt = follow[w]
        cand = list(nxt)
        pr = np.array([nxt[c] for c in cand], float)
        w = cand[int(g.choice(len(cand), p=pr / pr.sum()))]
        seq.append(w)
    out["w2"] = " ".join(seq)
    for k, v in out.items():
        print(f"    {k}: {v[:100]}")
    return dict(samples=out, vocab=len(vocab), words=len(words))


# ---------------------------------------------------------------------------
# Codes
# ---------------------------------------------------------------------------
def compute_huffman():
    p = load("letters")["p"]
    # Huffman: repeatedly merge the two least likely nodes; ties broken by node id, so the code is reproducible
    heap = [(float(p[i]), i, i) for i in range(27)]
    heapq.heapify(heap)
    children, merges, nid = {}, [], 27
    while len(heap) > 1:
        pa, _, a = heapq.heappop(heap)
        pb, _, b = heapq.heappop(heap)
        children[nid] = (a, b)
        merges.append([a, b, nid, pa + pb])
        heapq.heappush(heap, (pa + pb, nid, nid))
        nid += 1
    root = heap[0][2]
    code = {}

    def walk(n, prefix):
        if n < 27:
            code[n] = prefix or "0"
            return
        a, b = children[n]
        walk(a, prefix + "0")
        walk(b, prefix + "1")

    walk(root, "")
    lengths = np.array([len(code[i]) for i in range(27)])
    L = float((p * lengths).sum())
    H = entropy(p)
    kraft = float((2.0 ** -lengths).sum())
    assert abs(kraft - 1) < 1e-12  # a full binary tree: Kraft's sum is exactly 1
    assert H <= L < H + 1 and L - H < 0.05, (H, L)
    shannon_len = np.ceil(-np.log2(p)).astype(int)
    L_shannon = float((p * shannon_len).sum())
    assert H <= L_shannon < H + 1 and L <= L_shannon
    word = "the falcon"
    bits = "".join(code[ALPHA27.index(c)] for c in word)
    return dict(codes=[code[i] for i in range(27)], lengths=lengths, L=L, H=H, merges=merges, root=root,
                shannon_len=shannon_len, L_shannon=L_shannon, word=word, word_bits=bits,
                fixed_bits=5 * len(word))


def compute_arith():
    """Arithmetic coding of MESSAGE under the order-3 letter model (add-alpha counts), in exact fractions."""
    tr = codes27(text("train27"))
    alpha = Fraction(1, 100)
    m = NGram(tr, 3, 27)
    msg = "the falcon"
    a = codes27(msg)
    low, width = Fraction(0), Fraction(1)
    steps = []
    hist = list(codes27("he said "))[-3:]  # the context before the message: "...id "
    pad = [int(x) for x in hist]
    for i, s in enumerate(a):
        ctx = (pad + list(a[:i]))[-3:]
        nj, nc = m.counts(np.full(27, m.key(ctx), np.int64), np.arange(27))
        probs = [Fraction(int(nj[k]) * 100 + 1, int(nc[k]) * 100 + 27) for k in range(27)]
        assert sum(probs) == 1
        cum = sum(probs[:s], Fraction(0))
        steps.append(dict(symbol=ALPHA27[s], context="".join(ALPHA27[c] for c in ctx),
                          probs=[float(q) for q in probs], low=float(low), width=float(width),
                          log2_width=math.log2(width), p=float(probs[s]), bits=-math.log2(probs[s])))
        low, width = low + width * cum, width * probs[s]
    # the shortest binary fraction 0.b1...bn whose whole dyadic interval [x, x + 2^-n) lies inside [low, low + width)
    n = 1
    while True:
        x = math.ceil(low * 2**n)
        if Fraction(x + 1, 2**n) <= low + width:
            break
        n += 1
    bits = format(x, f"0{n}b")
    total = -math.log2(width)
    assert total <= n <= total + 2
    # decoding: read the bits back as a number and replay the subdivision
    v = Fraction(x, 2**n) + Fraction(1, 2**(n + 1))
    lo2, w2, out = Fraction(0), Fraction(1), []
    for i in range(len(a)):
        ctx = (pad + [ALPHA27.index(c) for c in out])[-3:]
        nj, nc = m.counts(np.full(27, m.key(ctx), np.int64), np.arange(27))
        probs = [Fraction(int(nj[k]) * 100 + 1, int(nc[k]) * 100 + 27) for k in range(27)]
        cum = Fraction(0)
        for k in range(27):
            if v < lo2 + w2 * (cum + probs[k]):
                out.append(ALPHA27[k])
                lo2, w2 = lo2 + w2 * cum, w2 * probs[k]
                break
            cum += probs[k]
    assert "".join(out) == msg
    return dict(message=msg, steps=steps, bits=bits, n_bits=n, info=total, final_low=float(low),
                final_width=float(width), huffman_bits=len(load("huffman")["word_bits"]))


# ---------------------------------------------------------------------------
# Shannon's guessing game
# ---------------------------------------------------------------------------
def backoff_ranks(models: list[NGram], b: np.ndarray, start: int = 0, guesses: list | None = None) -> np.ndarray:
    """The guess number of each symbol of b: letters ranked by their count after the longest context, ties broken
    by the next shorter context, and so on down to single-letter frequency (a deterministic guesser).  If
    ``guesses`` is a list, each position's guesses up to the right one are appended to it."""
    top = max(m.order for m in models)
    by_order = sorted(models, key=lambda m: m.order)  # np.lexsort's last key is its primary one: the longest context
    ranks = []
    for i in range(max(start, top), len(b)):
        keys = []
        for m in by_order:
            nj, _ = m.counts(np.full(27, m.key(b[i - m.order:i]), np.int64), np.arange(27))
            keys.append(-nj)
        order = np.lexsort(keys)
        r = int(np.where(order == b[i])[0][0]) + 1
        ranks.append(r)
        if guesses is not None:
            guesses.append("".join(ALPHA27[j] for j in order[:r]))
    return np.array(ranks)


def shannon_bounds(ranks: np.ndarray) -> tuple[float, float, np.ndarray]:
    q = np.bincount(ranks, minlength=29)[1:28] / len(ranks)
    upper = entropy(q)
    qq = np.append(q, 0.0)
    lower = float(sum((i + 1) * (qq[i] - qq[i + 1]) * math.log2(i + 1) for i in range(27)))
    return upper, lower, q


def compute_game():
    tr = codes27(text("train27"))
    models = [NGram(tr, N, 27) for N in range(0, 7)]
    # Shannon's sentence, with the six letters before it given as context
    sent = SHANNON_SENTENCE
    prefix = "he said "  # context for the first letters
    b = codes27(prefix + sent)
    guess_lists: list = []
    r_sent = backoff_ranks(models, b, start=len(prefix), guesses=guess_lists)
    assert all(g[-1] == c and len(g) == r for g, c, r in zip(guess_lists, sent, r_sent))
    assert len(r_sent) == len(sent)
    # the surprise of each letter of the sentence under the best counting model (context of `best` letters)
    orders = load("orders")
    k = orders["best"]
    row = orders["rows"][k]
    m = NGram(tr, k, 27)
    sent_bits = m.bits(codes27(prefix[-k:] + sent), row["alpha"]) if k else m.bits(codes27(sent), row["alpha"])
    assert len(sent_bits) == len(sent)
    te = codes27(text("passage27"))[:12000]
    r = backoff_ranks(models, te, start=6)
    upper, lower, q = shannon_bounds(r)
    best = load("orders")["best_bits"]
    assert lower < upper and lower < best
    print(f"    first-guess rate {q[0]:.3f}; bounds {lower:.2f} .. {upper:.2f}; model {best:.2f}")
    return dict(sentence=sent, sentence_ranks=r_sent, sentence_guesses=guess_lists, passage_ranks_q=q, upper=upper,
                lower=lower, first=q[0],
                n=len(r), shannon_human=[0.6, 1.3], sentence_bits=sent_bits, sentence_order=k,
                sentence_total=float(sent_bits.sum()))


# ---------------------------------------------------------------------------
# Mutual information
# ---------------------------------------------------------------------------
def compute_mi():
    a = codes27(text("train27"))
    p1 = np.bincount(a, minlength=27) / len(a)
    ds = np.unique(np.round(np.logspace(0, 3, 40)).astype(int))
    mi = []
    for d in ds:
        j = np.bincount(a[:-d] * 27 + a[d:], minlength=729).reshape(27, 27) / (len(a) - d)
        nz = j > 0
        I = float((j[nz] * np.log2(j[nz] / np.outer(p1, p1)[nz])).sum())
        I -= 26 * 26 / (2 * (len(a) - d) * math.log(2))  # the plug-in estimate's bias (Miller-Madow)
        mi.append(I)
    mi = np.array(mi)
    # the same letters, shuffled: no dependence at any distance (what the estimator reads as "nothing")
    sh = a.copy()
    rng(7).shuffle(sh)
    j = np.bincount(sh[:-1] * 27 + sh[1:], minlength=729).reshape(27, 27) / (len(sh) - 1)
    floor = float((j[j > 0] * np.log2(j[j > 0] / np.outer(p1, p1)[j > 0])).sum()) - 26 * 26 / (2 * len(sh) * math.log(2))
    # three quarters of a bit between neighbours; a fast fall inside a word, then a long, slow tail
    assert mi[0] > 0.7 and mi[ds.tolist().index(10)] < 0.002 and mi[-1] > 20 * abs(floor)
    sel = (ds >= 20) & (ds <= 1000)
    slope, icept = np.polyfit(np.log10(ds[sel]), np.log10(mi[sel]), 1)
    return dict(d=ds, mi=mi, floor=floor, slope=float(slope), intercept=float(icept))


# ---------------------------------------------------------------------------
# KL: mode-covering and mode-seeking
# ---------------------------------------------------------------------------
KL_X = np.linspace(-6, 6, 2401)


def kl_target(x):
    def n(x, m, s):
        return np.exp(-0.5 * ((x - m) / s) ** 2) / (s * math.sqrt(2 * math.pi))
    return 0.62 * n(x, -2.0, 0.65) + 0.38 * n(x, 2.2, 0.75)


def gauss(x, m, s):
    return np.exp(-0.5 * ((x - m) / s) ** 2) / (s * math.sqrt(2 * math.pi))


def kl_forward(m, s):  # KL(p || q), in bits
    p, q = kl_target(KL_X), gauss(KL_X, m, s)
    dx = KL_X[1] - KL_X[0]
    return float(np.sum(p * np.log2(np.maximum(p, 1e-300) / np.maximum(q, 1e-300))) * dx)


def kl_reverse(m, s):  # KL(q || p)
    p, q = kl_target(KL_X), gauss(KL_X, m, s)
    dx = KL_X[1] - KL_X[0]
    return float(np.sum(q * np.log2(np.maximum(q, 1e-300) / np.maximum(p, 1e-300))) * dx)


def descend(f, m, ls, lr=0.08, steps=220, clip=2.0):
    """Gradient descent on (mu, log sigma), the gradient's length capped at ``clip`` (so a far-off start takes
    even steps instead of one leap)."""
    path_ = [(m, math.exp(ls), f(m, math.exp(ls)))]
    for _ in range(steps):
        h = 1e-4
        gm = (f(m + h, math.exp(ls)) - f(m - h, math.exp(ls))) / (2 * h)
        gs = (f(m, math.exp(ls + h)) - f(m, math.exp(ls - h))) / (2 * h)
        g = math.hypot(gm, gs)
        if g > clip:
            gm, gs = gm * clip / g, gs * clip / g
        m, ls = m - lr * gm, ls - lr * gs
        path_.append((m, math.exp(ls), f(m, math.exp(ls))))
    return np.array(path_)


def compute_kl():
    p = kl_target(KL_X)
    dx = KL_X[1] - KL_X[0]
    mean = float(np.sum(KL_X * p) * dx)
    sd = float(math.sqrt(np.sum((KL_X - mean) ** 2 * p) * dx))
    fwd = descend(kl_forward, 2.0, math.log(0.8), lr=0.05, steps=400)
    assert abs(fwd[-1, 0] - mean) < 0.02 and abs(fwd[-1, 1] - sd) < 0.02  # forward KL matches the moments
    rev_a = descend(kl_reverse, -0.9, math.log(1.0), lr=0.05, steps=320)
    rev_b = descend(kl_reverse, 1.5, math.log(0.7), lr=0.05, steps=320)
    assert abs(rev_a[-1, 0] + 2.0) < 0.15 and abs(rev_b[-1, 0] - 2.2) < 0.15  # reverse KL picks one peak
    ms, ss = np.linspace(-3.5, 3.5, 71), np.linspace(0.3, 3.3, 61)
    F = np.array([[kl_forward(m, s) for m in ms] for s in ss])
    R = np.array([[kl_reverse(m, s) for m in ms] for s in ss])
    return dict(x=KL_X[::8], p=p[::8], mean=mean, sd=sd, fwd=fwd, rev_a=rev_a, rev_b=rev_b, grid_m=ms, grid_s=ss,
                F=F, R=R, fwd_kl=float(fwd[-1, 2]), rev_kl_a=float(rev_a[-1, 2]), rev_kl_b=float(rev_b[-1, 2]),
                rev_at_fwd=kl_reverse(mean, sd), fwd_at_rev=kl_forward(rev_a[-1, 0], rev_a[-1, 1]))


# ---------------------------------------------------------------------------
# Cross-entropy and its gradient
# ---------------------------------------------------------------------------
def compute_softmax():
    """Five outcomes seen 40, 25, 18, 12, 5 times: gradient descent on the logits of a softmax model."""
    counts = np.array([40, 25, 18, 12, 5], float)
    phat = counts / counts.sum()
    z = np.zeros(5)
    lr = 1.5
    zs, qs, ces = [], [], []
    for _ in range(61):
        q = np.exp(z - z.max())
        q /= q.sum()
        zs.append(z.copy())
        qs.append(q)
        ces.append(float(-(phat * np.log2(q)).sum()))
        z = z - lr * (q - phat)  # d/dz of the cross-entropy (in nats) is q - p
    qs, ces = np.array(qs), np.array(ces)
    H = entropy(phat)
    assert np.abs(qs[-1] - phat).max() < 0.01 and abs(ces[-1] - H) < 0.01 and np.all(np.diff(ces) <= 1e-12)
    # check the gradient formula by finite differences at the start
    def ce(z):
        q = np.exp(z - z.max())
        q /= q.sum()
        return float(-(phat * np.log(q)).sum())
    g = np.array([(ce(np.eye(5)[k] * 1e-6) - ce(-np.eye(5)[k] * 1e-6)) / 2e-6 for k in range(5)])
    assert np.allclose(g, 0.2 - phat, atol=1e-6)
    return dict(counts=counts, phat=phat, z=np.array(zs), q=qs, ce=ces, H=H, lr=lr)


# ---------------------------------------------------------------------------
# The passage as printed: counting models and compressors
# ---------------------------------------------------------------------------
def compute_raw():
    train, valid, passage = text("train"), text("valid"), text("passage")
    chars = sorted(set(train) | set(passage))
    idx = {c: i for i, c in enumerate(chars)}
    K = len(chars)
    enc = lambda t: np.array([idx[c] for c in t], np.int64)  # noqa: E731
    rows = fit_orders(enc(train), enc(valid), enc(passage), K, range(0, 8))
    best = int(np.argmin([r["test"] for r in rows]))
    data = passage.encode("utf-8")
    n = len(passage)
    comp = {
        "gzip": len(gzip.compress(data, 9)) * 8 / n,
        "bzip2": len(bz2.compress(data, 9)) * 8 / n,
        "xz": len(lzma.compress(data, preset=9 | lzma.PRESET_EXTREME)) * 8 / n,
    }
    assert comp["xz"] < comp["gzip"] and rows[best]["test"] < comp["bzip2"]
    print(f"    K={K}  best order {best}: {rows[best]['test']:.3f}  {comp}")
    return dict(K=K, rows=rows, best=best, best_bits=rows[best]["test"], compressors=comp, n_chars=n,
                n_bytes=len(data), uniform=math.log2(len(set(passage))), passage_symbols=len(set(passage)))


# ---------------------------------------------------------------------------
# Language models
# ---------------------------------------------------------------------------
LMS = [
    # (id, label, parameters, year, context window used here)
    ("openai-community/gpt2", "GPT-2 small", 124e6, 2019, 1024),
    ("openai-community/gpt2-xl", "GPT-2 XL", 1.56e9, 2019, 1024),
    ("Qwen/Qwen3-0.6B-Base", "Qwen3-0.6B", 0.6e9, 2025, 2048),
    ("Qwen/Qwen3-1.7B-Base", "Qwen3-1.7B", 1.7e9, 2025, 2048),
    ("Qwen/Qwen3-4B-Base", "Qwen3-4B", 4.0e9, 2025, 2048),
]
SURPRISE_PARA = 2  # the paragraph of the passage shown with each token's surprise


def lm_bits(model_id: str, window: int, passage: str) -> dict:
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer

    torch.set_grad_enabled(False)
    tok = AutoTokenizer.from_pretrained(model_id)
    dtype = torch.float32 if "gpt2" in model_id else torch.bfloat16
    model = AutoModelForCausalLM.from_pretrained(model_id, dtype=dtype).eval()
    enc = tok(passage, return_offsets_mapping=True, add_special_tokens=False)
    ids, offs = enc["input_ids"], enc["offset_mapping"]
    bos = tok.convert_tokens_to_ids("<|endoftext|>")
    seq = [bos] + ids
    bits = np.zeros(len(ids))
    done = 0  # tokens of `ids` scored so far
    stride = window // 2
    while done < len(ids):
        start = max(0, done + 1 - (window - stride)) if done else 0  # positions in seq; keep >= half a window
        end = min(len(seq), start + window)
        x = torch.tensor([seq[start:end]])
        logits = model(x).logits[0]
        # seq[t + 1] is predicted at position t; ids[k] = seq[k + 1].  -log p = logsumexp(logits) - logit[target]
        ks = torch.arange(done, min(len(ids), end - 1))
        rows = logits[ks - start].float()
        target = torch.tensor([seq[k + 1] for k in ks.tolist()])
        nats = torch.logsumexp(rows, -1) - rows[torch.arange(len(ks)), target]
        bits[done:done + len(ks)] = nats.numpy() / math.log(2)
        done = min(len(ids), end - 1)
        del logits, rows
    # every character belongs to exactly one token
    assert sum(b - a for a, b in offs) == len(passage) or tok.decode(ids) == passage
    del model
    return dict(bits=bits, offsets=np.array(offs), tokens=[tok.decode([i]) for i in ids])


def compute_lms():
    passage = text("passage")
    paras = passage.split("\n")
    p0 = sum(len(p) + 1 for p in paras[:SURPRISE_PARA])
    p1 = p0 + len(paras[SURPRISE_PARA])
    out, rows = {}, []
    for mid, lab, params, year, window in LMS:
        t = time.time()
        r = lm_bits(mid, window, passage)
        bpc = float(r["bits"].sum() / len(passage))
        rows.append(dict(id=mid, label=lab, params=params, year=year, bpc=bpc, tokens=len(r["bits"]),
                         chars_per_token=len(passage) / len(r["bits"]), bits_per_token=float(r["bits"].mean())))
        sel = [k for k, (a, b) in enumerate(r["offsets"]) if a >= p0 and b <= p1]
        out[lab] = dict(tokens=[r["tokens"][k] for k in sel], bits=[float(r["bits"][k]) for k in sel],
                        starts=[int(r["offsets"][k][0]) - p0 for k in sel])
        print(f"    {lab:<14} {bpc:.3f} bits/char  {len(r['bits'])} tokens  {time.time() - t:.0f}s", flush=True)
    bpcs = [r["bpc"] for r in rows]
    assert bpcs[0] > bpcs[3]  # GPT-2 XL beats GPT-2 small
    assert min(bpcs) < 1.3
    return dict(rows=rows, surprise=out, paragraph=paras[SURPRISE_PARA])


PROBES = [
    "The Eiffel Tower is located in the city of",
    "Two plus two equals",
    "The author of Pride and Prejudice is Jane",
    "The chemical symbol for gold is",
    "She opened the door and said: \"Come",
]


def compute_probes():
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer

    torch.set_grad_enabled(False)
    out = {}
    for mid, lab in (("openai-community/gpt2", "GPT-2 small"), ("Qwen/Qwen3-4B-Base", "Qwen3-4B")):
        tok = AutoTokenizer.from_pretrained(mid)
        model = AutoModelForCausalLM.from_pretrained(mid, dtype=torch.float32 if "gpt2" in mid else torch.bfloat16)
        res = []
        for prompt in PROBES:
            ids = tok(prompt, add_special_tokens=False)["input_ids"]
            p = torch.softmax(model(torch.tensor([ids])).logits[0, -1].float(), -1).numpy()
            top = np.argsort(-p)[:8]
            res.append(dict(prompt=prompt, tokens=[tok.decode([int(i)]) for i in top], probs=[float(p[i]) for i in top]))
            print(f"    {lab}: {prompt!r} -> {res[-1]['tokens'][:3]} {np.round(res[-1]['probs'][:3], 3)}")
        out[lab] = res
        del model
    return out


def compute_context():
    """The surprise of " telephone" in the paragraph shown by `lms`, with and without the two paragraphs before it
    (the first of which begins "A TELEPHONE-BELL rang"): what remembering the context is worth."""
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer

    torch.set_grad_enabled(False)
    paras = text("passage").split("\n")
    assert paras[0].startswith("A TELEPHONE-BELL") and " telephone " in paras[SURPRISE_PARA]
    out = {}
    for mid, lab in (("openai-community/gpt2", "GPT-2 small"), ("Qwen/Qwen3-4B-Base", "Qwen3-4B")):
        tok = AutoTokenizer.from_pretrained(mid)
        model = AutoModelForCausalLM.from_pretrained(mid, dtype=torch.float32 if "gpt2" in mid else torch.bfloat16)
        res = {}
        for name, ctx in (("alone", ""), ("with context", "\n".join(paras[:SURPRISE_PARA]) + "\n")):
            full = ctx + paras[SURPRISE_PARA]
            enc = tok(full, return_offsets_mapping=True, add_special_tokens=False)
            ids = [tok.convert_tokens_to_ids("<|endoftext|>")] + enc["input_ids"]
            logp = torch.log_softmax(model(torch.tensor([ids])).logits[0].float(), -1)
            i = full.index(" telephone", len(ctx))
            k = next(j for j, (a, b) in enumerate(enc["offset_mapping"]) if a == i)
            res[name] = -float(logp[k, ids[k + 1]]) / math.log(2)
        out[lab] = res
        print(f"    {lab}: {res}")
        del model
    assert out["Qwen3-4B"]["alone"] - out["Qwen3-4B"]["with context"] > 6
    return out


WORDS = [" dog", " puppy", " wolf", " cat", " tobacco", " cigarette", " telephone", " phone"]


def compute_vectors():
    """A teaser for Part 2: cosine similarities between GPT-2's input vectors for a few words, and between random
    directions in 3 and in 768 dimensions (GPT-2's width)."""
    from transformers import AutoModelForCausalLM, AutoTokenizer

    tok = AutoTokenizer.from_pretrained("openai-community/gpt2")
    E = AutoModelForCausalLM.from_pretrained("openai-community/gpt2").transformer.wte.weight.detach().numpy()
    ids = []
    for w in WORDS:
        i = tok(w)["input_ids"]
        assert len(i) == 1, w
        ids.append(i[0])
    V = E[ids]
    V = V / np.linalg.norm(V, axis=1, keepdims=True)
    cos = V @ V.T
    d = dict(zip(WORDS, range(len(WORDS))))
    assert cos[d[" dog"], d[" puppy"]] > cos[d[" dog"], d[" tobacco"]] + 0.1
    g = rng(2)
    out = dict(words=WORDS, cos=cos, width=int(E.shape[1]))
    for dim in (3, 768):
        a = g.normal(size=(20000, dim))
        b = g.normal(size=(20000, dim))
        c = (a * b).sum(1) / np.linalg.norm(a, axis=1) / np.linalg.norm(b, axis=1)
        out[f"random{dim}"] = np.histogram(c, bins=40, range=(-1, 1))[0]
        out[f"sd{dim}"] = float(c.std())
    assert abs(out["sd768"] - 1 / math.sqrt(768)) < 0.002
    return out


# ---------------------------------------------------------------------------
# The scoreboard
# ---------------------------------------------------------------------------
def compute_scoreboard():
    raw, lms = load("raw"), load("lms")
    rows = [
        dict(key="ascii", label="plain text file", bits=8.0, part=1, kind="baseline"),
        dict(key="uniform", label=f"uniform over its {raw['passage_symbols']} symbols", bits=raw["uniform"], part=1,
             kind="count"),
        dict(key="order0", label="letter frequencies", bits=raw["rows"][0]["test"], part=1, kind="count"),
        dict(key="order1", label="the previous character", bits=raw["rows"][1]["test"], part=1, kind="count"),
        dict(key="gzip", label="gzip", bits=raw["compressors"]["gzip"], part=1, kind="compressor"),
        dict(key="xz", label="xz", bits=raw["compressors"]["xz"], part=1, kind="compressor"),
        dict(key="bzip2", label="bzip2", bits=raw["compressors"]["bzip2"], part=1, kind="compressor"),
        dict(key="best", label=f"the previous {raw['best']} characters", bits=raw["best_bits"], part=1,
             kind="count"),
    ]
    for r in lms["rows"]:
        if r["label"] in ("GPT-2 small", "GPT-2 XL", "Qwen3-0.6B", "Qwen3-4B"):
            rows.append(dict(key=r["label"], label=f"{r['label']} ({r['year']})", bits=r["bpc"], part=1, kind="lm"))
    # Shannon's subjects, guessing letters with 100 letters of context: a band, measured on the 27-letter alphabet
    rows.append(dict(key="human", label="people (Shannon 1951, letters only)", lo=0.6, hi=1.3, part=1, kind="human"))
    return dict(rows=rows, passage="The Maltese Falcon (1930), chapter 2", chars=raw["n_chars"])


ITEMS = {
    "corpus": compute_corpus,
    "letters": compute_letters,
    "bigram": compute_bigram,
    "orders": compute_orders,
    "samples": compute_samples,
    "huffman": compute_huffman,
    "arith": compute_arith,
    "game": compute_game,
    "mi": compute_mi,
    "kl": compute_kl,
    "softmax": compute_softmax,
    "raw": compute_raw,
    "lms": compute_lms,
    "probes": compute_probes,
    "context": compute_context,
    "vectors": compute_vectors,
    "scoreboard": compute_scoreboard,
}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("names", nargs="*", default=list(ITEMS))
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    os.environ.setdefault("TOKENIZERS_PARALLELISM", "true")
    for name in args.names:
        if path(name).exists() and not args.force:
            print(f"  cached  {name}")
            continue
        t = time.time()
        print(f"  compute {name} ...", flush=True)
        _save(name, ITEMS[name]())
        _loaded.pop(name, None)
        print(f"  done    {name} in {time.time() - t:.0f}s", flush=True)


if __name__ == "__main__":
    main()
