"""Monochord's machines that compose (Part 65 of *Music, Built*): generators learnt from Bach's chorale melodies, from
counting to a transformer, and the measures that keep them honest.

A tune is a list of notes ``(key number, length in sixteenths, fermata)`` in C major; a fermata ends a phrase.

    tunes(), split()             the soprano lines of Bach's major-mode chorales, transposed to C; many chorales share a
                                 hymn tune, so tunes are grouped by melody and split by group (no tune on both sides)
    Markov                       a variable-order model of whole notes (pitch, length, fermata), after melody.NGram:
                                 bits per note on held-out tunes; sampling with a temperature
    longest_copy, copied_share   how much of a generated tune is a stretch of some training tune
    constrained                  sampling an order-2 chain exactly under constraints (a length, an ending on the
                                 tonic), by backward messages (after Pachet and Roy, 2011)
    recombine                    Cope's recombinancy: phrases cut at fermatas from different chorales, joined where
                                 they connect by step
    representations              the same tunes as note tokens, as pitch-then-length tokens, and on a sixteenth-note
                                 grid with a hold symbol (DeepBach's)
    VOCAB, encode, decode        tokens for the transformer: pitches, lengths, a fermata, begin and end
    train_transformer, transformer_bits, transformer_sample
                                 *AI, Built*'s pocket transformer on those tokens, with or without transposed copies
    intervals_kl, cadence_share  simple judges: the interval distribution against held-out Bach; endings on the tonic
    soprano_beats, harmonize     a generated tune harmonized by Part 17's chord model and voice-leading search

No manim; torch only in the transformer's functions.  Checked in ``tests/music/test_machines.py``.
"""

from __future__ import annotations

import math
from collections import Counter, defaultdict

import numpy as np

from . import chorales as BC
from .melody import NGram

TICKS = BC.TICKS                                          # per quarter note
SIX = TICKS // 4                                          # ticks per sixteenth
LENGTHS = (1, 2, 3, 4, 6, 8, 12, 16)                      # note lengths kept, in sixteenths


# --------------------------------------------------------------------------------------------- the corpus
def _snap(d16: float) -> int:
    return min(LENGTHS, key=lambda v: abs(v - d16))


def tunes(book=None) -> list[dict]:
    """Every major-mode chorale's soprano, transposed so the tonic is C and the tune sits near the treble staff.
    Each: name, notes, group (the first ten pitches, which identify the hymn tune)."""
    book = BC.load() if book is None else book
    out = []
    for c in book:
        if c.mode != "major" or c.time != (4, 4):
            continue
        sop = sorted(c.voices[0], key=lambda n: n[1])
        shift = -(c.tonic % 12)
        ps = [p + shift for p, _, _, _ in sop]
        med = float(np.median(ps))
        shift += 12 * round((69 - med) / 12)
        notes = [(int(p + shift), _snap(d / SIX), bool(f)) for p, _, d, f in sop]
        if not notes:
            continue
        notes[-1] = (notes[-1][0], notes[-1][1], True)
        out.append({"name": c.name, "notes": notes, "group": tuple(n[0] for n in notes[:10])})
    return out


def split(ts, frac: float = 0.2, seed: int = 0) -> tuple[list, list]:
    """Training and test tunes, split by hymn tune so that no melody (however harmonized) is on both sides."""
    groups = sorted({t["group"] for t in ts})
    rng = np.random.default_rng(seed)
    rng.shuffle(groups)
    test_g = set(groups[: max(1, int(round(frac * len(groups))))])
    train = [t for t in ts if t["group"] not in test_g]
    test = [t for t in ts if t["group"] in test_g]
    # one harmonization per tune in the test set: the same melody twice would count twice
    seen, test1 = set(), []
    for t in test:
        if t["group"] not in seen:
            seen.add(t["group"])
            test1.append(t)
    return train, test1


def phrases(notes) -> list[list]:
    out, cur = [], []
    for n in notes:
        cur.append(n)
        if n[2]:
            out.append(cur)
            cur = []
    if cur:
        out.append(cur)
    return out


# --------------------------------------------------------------------------------------------- counting
class Markov:
    """A variable-order model over whole notes, blended from long contexts to short (PPM escape C, as
    ``melody.NGram``).  Order 0 knows only how common each note is; order 8 remembers eight notes back."""

    def __init__(self, order: int):
        self.order = order
        self.ng = NGram(order)

    def fit(self, ts) -> "Markov":
        self.ng.fit([t["notes"] if isinstance(t, dict) else t for t in ts])
        return self

    def bits(self, ts) -> float:
        """Bits per note on held-out tunes (notes never seen at all get the alphabet's floor)."""
        tot, n = 0.0, 0
        for t in ts:
            s = self.ng.surprise(t["notes"] if isinstance(t, dict) else t)
            tot += float(np.sum(np.minimum(s, 16.0)))
            n += len(s)
        return tot / max(n, 1)

    def sample(self, seed: int = 0, temperature: float = 1.0, start=(), max_notes: int = 64, min_phrases: int = 4) -> list:
        """Draw notes until a phrase ends after ``min_phrases`` phrases on the tonic (or ``max_notes``)."""
        rng = np.random.default_rng(seed)
        out = list(start)
        while len(out) < max_notes:
            d = self.ng.distribution(out)
            keys = list(d)
            p = np.array([d[k] for k in keys], float)
            p = p ** (1.0 / max(temperature, 1e-3))
            p /= p.sum()
            out.append(tuple(keys[int(rng.choice(len(keys), p=p))]))
            done = sum(1 for n in out if n[2])
            if out[-1][2] and done >= min_phrases and out[-1][0] % 12 == 0:
                break
        return [(int(a), int(b), bool(c)) for a, b, c in out]


def train_grams(train, nmax: int = 40) -> dict:
    """Every stretch of up to ``nmax`` notes in the training tunes, with the tune it came from."""
    grams = {}
    for t in train:
        s = [tuple(n) for n in t["notes"]]
        for i in range(len(s)):
            for L in range(1, min(nmax, len(s) - i) + 1):
                grams.setdefault(tuple(s[i:i + L]), t["name"])
    return grams


def longest_copy(seq, grams) -> dict:
    """The longest run of consecutive notes of ``seq`` that occurs in some training tune, with where it came from."""
    s = [tuple(n) for n in seq]
    best = (0, 0, None)
    for i in range(len(s)):
        j = i + best[0] + 1
        while j <= len(s) and tuple(s[i:j]) in grams:
            best = (j - i, i, grams[tuple(s[i:j])])
            j += 1
    return {"length": best[0], "start": best[1], "source": best[2]}


def copied_share(seq, grams, n: int = 8) -> float:
    """The share of notes that lie inside some run of ``n`` notes copied exactly from a training tune."""
    s = [tuple(x) for x in seq]
    cover = np.zeros(len(s), bool)
    for i in range(len(s) - n + 1):
        if tuple(s[i:i + n]) in grams:
            cover[i:i + n] = True
    return float(cover.mean()) if len(s) else 0.0


# --------------------------------------------------------------------------------------------- constraints
def constrained(train, length: int = 32, seed: int = 0, end_long: int = 8) -> dict:
    """An order-2 chain over whole notes sampled *exactly* under constraints: exactly ``length`` notes, the last a
    tonic of at least ``end_long`` sixteenths under a fermata, and no other fermata on a note that is not a step of
    the tonic triad.  Backward messages give, for each state and number of notes left, the probability of finishing
    legally; sampling forward in proportion to them draws from the chain conditioned on the constraints (Pachet and
    Roy's Markov constraints).  Also an unconstrained draw of the same length for comparison."""
    seqs = [[tuple(n) for n in t["notes"]] for t in train]
    trans = defaultdict(Counter)
    starts = Counter()
    for s in seqs:
        if len(s) >= 2:
            starts[(s[0], s[1])] += 1
        for i in range(2, len(s)):
            trans[(s[i - 2], s[i - 1])][s[i]] += 1
    triad = {0, 4, 7}

    def legal(x, last):
        if last:
            return x[2] and x[0] % 12 == 0 and x[1] >= end_long
        return (not x[2]) or (x[0] % 12 in triad)
    states = set(trans) | set(starts)
    # beta[k][state] = P(the next k notes can be chosen legally | state), the last of them the end
    beta = [defaultdict(float) for _ in range(length + 1)]
    for st in states:
        beta[0][st] = 1.0
    for k in range(1, length - 1):
        for st in states:
            c = trans.get(st)
            if not c:
                continue
            tot = sum(c.values())
            v = 0.0
            for x, n in c.items():
                if legal(x, k == 1):
                    v += n / tot * beta[k - 1][(st[1], x)]
            beta[k][st] = v
    rng = np.random.default_rng(seed)
    left = length - 2
    st_list = [s for s in starts if all(legal(x, False) for x in s)]
    w = np.array([starts[s] * beta[left][s] for s in st_list], float)
    if w.sum() == 0:
        raise ValueError("no sequence satisfies the constraints")
    cur = st_list[int(rng.choice(len(st_list), p=w / w.sum()))]
    out = [cur[0], cur[1]]
    for k in range(left, 0, -1):
        c = trans[cur]
        tot = sum(c.values())
        xs = [x for x in c if legal(x, k == 1)]
        p = np.array([c[x] / tot * beta[k - 1][(cur[1], x)] for x in xs], float)
        x = xs[int(rng.choice(len(xs), p=p / p.sum()))]
        out.append(x)
        cur = (cur[1], x)
    # the unconstrained chain, the same length, for comparison
    st = list(starts)
    cur = st[int(rng.choice(len(st), p=np.array([starts[s] for s in st], float) / sum(starts.values())))]
    free = [cur[0], cur[1]]
    while len(free) < length:
        c = trans.get(cur)
        if not c:
            break
        xs = list(c)
        p = np.array([c[x] for x in xs], float)
        x = xs[int(rng.choice(len(xs), p=p / p.sum()))]
        free.append(x)
        cur = (cur[1], x)
    p_ok = float(sum(starts[s] * beta[left][s] for s in starts) / sum(starts.values()))
    fix = lambda s: [(int(a), int(b), bool(c)) for a, b, c in s]
    return {"notes": fix(out), "free": fix(free), "p_legal": p_ok}


# --------------------------------------------------------------------------------------------- recombination
def recombine(train, seed: int = 0, n_phrases: int = 4, max_join: int = 2) -> dict:
    """A new chorale tune from phrases of different chorales (Cope's recombinancy): an opening phrase, middle phrases
    and a closing phrase ending on the tonic, each joined to the next by a step (at most ``max_join`` semitones), no two
    from the same hymn tune."""
    rng = np.random.default_rng(seed)
    pool = []
    for t in train:
        ph = phrases(t["notes"])
        for k, p in enumerate(ph):
            pool.append({"name": t["name"], "group": t["group"], "k": k, "last": k == len(ph) - 1, "notes": p})
    openers = [p for p in pool if p["k"] == 0]
    closers = [p for p in pool if p["last"] and p["notes"][-1][0] % 12 == 0 and p["k"] > 0]
    middles = [p for p in pool if 0 < p["k"] and not p["last"]]
    for _ in range(2000):
        a = openers[int(rng.integers(len(openers)))]
        chosen, used = [a], {a["group"]}
        ok = True
        for k in range(n_phrases - 1):
            src = closers if k == n_phrases - 2 else middles
            prev = chosen[-1]["notes"][-1][0]
            cand = [p for p in src if p["group"] not in used and abs(p["notes"][0][0] - prev) <= max_join]
            if not cand:
                ok = False
                break
            p = cand[int(rng.integers(len(cand)))]
            chosen.append(p)
            used.add(p["group"])
        if ok:
            notes = [n for p in chosen for n in p["notes"]]
            return {"notes": notes, "sources": [(p["name"], p["k"]) for p in chosen], "joins": [abs(chosen[i + 1]["notes"][0][0] - chosen[i]["notes"][-1][0]) for i in range(len(chosen) - 1)]}
    raise ValueError("no recombination found")


# --------------------------------------------------------------------------------------------- representations
def representations(ts) -> dict:
    """The same tunes three ways: one token per note (pitch, length and fermata together), two or three tokens per
    note (pitch, then length, then a fermata if any), and a sixteenth-note grid with a hold symbol."""
    note_vocab = {tuple(n) for t in ts for n in t["notes"]}
    pitches = {n[0] for t in ts for n in t["notes"]}
    lengths = {n[1] for t in ts for n in t["notes"]}
    n_notes = [len(t["notes"]) for t in ts]
    n_split = [sum(2 + n[2] for n in t["notes"]) for t in ts]
    n_grid = [sum(n[1] for n in t["notes"]) for t in ts]
    return {"note": {"vocab": len(note_vocab), "mean_length": float(np.mean(n_notes))},
            "split": {"vocab": len(pitches) + len(lengths) + 1, "mean_length": float(np.mean(n_split))},
            "grid": {"vocab": len(pitches) + 2, "mean_length": float(np.mean(n_grid))}}


# --------------------------------------------------------------------------------------------- the transformer
PITCH_LO, PITCH_HI = 48, 96
VOCAB = (["<pad>", "<bos>", "<eos>", "<ferm>"] + [f"p{m}" for m in range(PITCH_LO, PITCH_HI + 1)] + [f"d{v}" for v in LENGTHS])
IDX = {t: i for i, t in enumerate(VOCAB)}


def encode(notes, bos: bool = True, eos: bool = True) -> list[int]:
    out = [IDX["<bos>"]] if bos else []
    for p, d, f in notes:
        out += [IDX[f"p{min(max(p, PITCH_LO), PITCH_HI)}"], IDX[f"d{d}"]] + ([IDX["<ferm>"]] if f else [])
    return out + ([IDX["<eos>"]] if eos else [])


def decode(ids) -> list:
    notes, p, d = [], None, None
    for i in ids:
        t = VOCAB[int(i)]
        if t == "<eos>":
            break
        if t.startswith("p"):
            if p is not None and d is not None:
                notes.append((p, d, False))
            p, d = int(t[1:]), None
        elif t.startswith("d") and p is not None:
            d = int(t[1:])
        elif t == "<ferm>" and p is not None and d is not None:
            notes.append((p, d, True))
            p, d = None, None
    if p is not None and d is not None:
        notes.append((p, d, False))
    return notes


def _stream(ts, transpose=(0,)) -> np.ndarray:
    ids = []
    for t in ts:
        for k in transpose:
            ids += encode([(p + k, d, f) for p, d, f in t["notes"]])
    return np.array(ids, np.int64)


def train_transformer(train, valid, transpose=(0,), steps: int = 1200, d: int = 96, layers: int = 3, seq: int = 320,
                      seed: int = 0, threads: int = 2) -> dict:
    """*AI, Built*'s pocket transformer (RMSNorm, rotary positions, SwiGLU) trained on the tunes' tokens; with
    ``transpose`` = several shifts, each training tune also appears in other keys."""
    import torch
    from explainer.lm import pocket
    torch.manual_seed(seed)
    tr, va = _stream(train, transpose), _stream(valid, (0,))
    cfg = pocket.Config(vocab=len(VOCAB), d=d, layers=layers, heads=4, seq=seq)
    batch = 16
    run = pocket.Run(model=cfg, lr=3e-3, batch=batch, tokens=steps * batch * seq, seed=seed, warmup=60, eval_every=max(1, steps // 30), eval_batches=4)
    res = pocket.train(run, pocket.TokenStream(tr, va, seq, seed=seed), threads=threads)
    return {"model": res["_model"], "curve": [[float(s), float(v)] for s, _, v in res["evals"]], "train_tokens": int(len(tr)),
            "params": int(res["counts"]["total"]), "seconds": float(res["seconds"])}


def transformer_bits(model, ts) -> float:
    """Bits per note on held-out tunes: each tune's tokens scored from its beginning, summed, over its notes."""
    import torch
    import torch.nn.functional as F
    tot, n = 0.0, 0
    model.eval()
    with torch.no_grad():
        for t in ts:
            ids = encode(t["notes"])
            x = torch.tensor([ids[:-1]])
            logp = F.log_softmax(model(x)[0], -1)
            tot += float(-logp[torch.arange(len(ids) - 1), torch.tensor(ids[1:])].sum()) / math.log(2)
            n += len(t["notes"])
    model.train()
    return tot / max(n, 1)


def transformer_sample(model, prompt_notes=(), temperature: float = 1.0, seed: int = 0, max_tokens: int = 200, min_tokens: int = 0) -> list:
    """Continue a prompt (notes) until the end token (not allowed before ``min_tokens`` new tokens); returns the notes
    after the prompt."""
    import torch
    g = torch.Generator().manual_seed(seed)
    ids = encode(list(prompt_notes), eos=False)
    start = len(ids)
    model.eval()
    with torch.no_grad():
        for _ in range(max_tokens):
            x = torch.tensor([ids[-model.cfg.seq:]])
            logits = model(x)[0, -1] / max(temperature, 1e-4)
            logits[IDX["<pad>"]] = -float("inf")
            logits[IDX["<bos>"]] = -float("inf")
            if len(ids) - start < min_tokens:
                logits[IDX["<eos>"]] = -float("inf")
            nxt = int(torch.multinomial(logits.softmax(-1), 1, generator=g))
            ids.append(nxt)
            if nxt == IDX["<eos>"]:
                break
    model.train()
    full = decode(ids)
    return full[len(list(prompt_notes)):]


# --------------------------------------------------------------------------------------------- judges
def intervals_kl(samples, reference, lo: int = -12, hi: int = 12) -> float:
    """KL divergence, in bits, from the reference's melodic-interval distribution to the samples' (add-one smoothed)."""
    def hist(ts):
        h = np.ones(hi - lo + 1)
        for t in ts:
            ps = [n[0] for n in (t["notes"] if isinstance(t, dict) else t)]
            for a, b in zip(ps, ps[1:]):
                if lo <= b - a <= hi:
                    h[b - a - lo] += 1
        return h / h.sum()
    p, q = hist(reference), hist(samples)
    return float(np.sum(p * np.log2(p / q)))


def cadence_share(samples) -> float:
    """The share of phrases (fermatas) that end on a note of the tonic triad."""
    ends = [n for t in samples for n in (t["notes"] if isinstance(t, dict) else t) if n[2]]
    return float(np.mean([n[0] % 12 in (0, 4, 7) for n in ends])) if ends else 0.0


def soprano_beats(notes) -> tuple[list, list, list]:
    """The tune as Part 17's harmonizer wants it: the soprano at each quarter-note beat, the beats under a fermata, and
    the tune as a voice (key, onset tick, duration ticks, fermata)."""
    voice, t = [], 0
    for p, d, f in notes:
        voice.append((p, t, d * SIX, f))
        t += d * SIX
    sop, ferm = [], []
    for k, b in enumerate(range(0, t, TICKS)):
        n = next(n for n in voice if n[1] <= b < n[1] + n[2])
        sop.append(n[0])
        if n[3]:
            ferm.append(k)
    return sop, ferm, voice
