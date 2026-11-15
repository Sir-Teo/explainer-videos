"""Monochord's origins (Part 47 of *Music, Built*): what is shared, how tunes travel, and how claims are tested.

    npvi(durations)                 the normalized pairwise variability index of successive durations (Grabe and Low
                                    2002; Patel and Daniele 2003): 0 for an even rhythm, larger as neighbours differ
    melody_line(notes)              a part's melody as the top note at each onset; its inter-onset intervals
    universals(melody)              a few of Savage and colleagues' (2015) statistical universals, operationalized for
                                    one written tune
    pipe_hz(length, bore)           an open pipe's lowest note, with end corrections

    RhythmPrior, tap_back, rhythm_chains
                                    Jacoby and McDermott's (2017) iterated reproduction: a three-interval rhythm is
                                    heard, tapped back, and the tapping is heard by the same listener again; a simulated
                                    Bayesian listener samples its posterior, so (Griffiths and Kalish 2007) the chains
                                    drift to its prior
    transmit, transmission_chain, structure
                                    a melody learned and sung by one simulated singer after another (pitch and timing
                                    noise, pitch categories, a pull toward simple duration ratios, a cost on wide leaps,
                                    slips of memory that fall on whatever is new), and measures of its structure
    align, upgma, splits, robinson_foulds, tree_transmission
                                    tune families: alignment distances between melodies, a tree built from them, and a
                                    check against the tree a simulated transmission really followed
    rayleigh, bobbing               circular statistics for 'is the dancer on the beat?'
    publication_bias                many small studies of a small true effect, and what the published ones say

No manim here.  Checked in ``tests/music/test_origins.py``.
"""

from __future__ import annotations

import math
from collections import Counter
from itertools import permutations

import numpy as np

# --------------------------------------------------------------------------------------------- rhythm and language


def npvi(durations) -> float:
    """100 / (m - 1) * sum |d_k - d_k+1| / ((d_k + d_k+1) / 2)."""
    d = np.asarray(durations, dtype=float)
    if len(d) < 2:
        return 0.0
    return float(100.0 * np.mean(np.abs(d[1:] - d[:-1]) / ((d[1:] + d[:-1]) / 2.0)))


def melody_line(notes, longest: float | None = None) -> dict:
    """notes: [key, onset, duration] (any time unit).  The melody is the highest note sounding at each onset; its
    inter-onset intervals, dropping any longer than ``longest`` (a rest between phrases is not a duration)."""
    top = {}
    for p, a, _ in notes:
        top[a] = max(top.get(a, -1), p)
    t = sorted(top)
    ioi = np.diff(t)
    if longest is not None:
        ioi = ioi[ioi <= longest]
    return {"onsets": t, "pitches": [top[a] for a in t], "ioi": [float(x) for x in ioi]}


def bootstrap_diff(a, b, n: int = 20000, seed: int = 0) -> dict:
    """Difference of means b - a with a percentile bootstrap interval and a two-sided permutation p-value."""
    a, b = np.asarray(a, float), np.asarray(b, float)
    rng = np.random.default_rng(seed)
    diff = float(b.mean() - a.mean())
    boots = np.array([rng.choice(b, len(b)).mean() - rng.choice(a, len(a)).mean() for _ in range(n)])
    both = np.concatenate([a, b])
    perm = []
    for _ in range(n):
        rng.shuffle(both)
        perm.append(both[len(a):].mean() - both[:len(a)].mean())
    p = float((np.sum(np.abs(perm) >= abs(diff) - 1e-12) + 1) / (n + 1))
    return {"diff": diff, "lo": float(np.percentile(boots, 2.5)), "hi": float(np.percentile(boots, 97.5)), "p": p}


# --------------------------------------------------------------------------------------------- universals


def contour(phrase) -> str:
    """'arch', 'descending', 'ascending' or 'other': the middle third against the ends, and the end against the start."""
    p = np.asarray(phrase, dtype=float)
    if len(p) < 3:
        return "other"
    k = max(len(p) // 3, 1)
    first, mid, last = p[:k].mean(), p[k:len(p) - k].mean() if len(p) > 2 * k else p[k], p[-k:].mean()
    if mid > first and mid > last:
        return "arch"
    if last < first:
        return "descending"
    if last > first:
        return "ascending"
    return "other"


def universals(m) -> dict:
    """For a written tune (``Melody``): which of these hold?
    few scale degrees      at most seven pitch classes
    small intervals        most melodic intervals smaller than 750 cents (Savage's threshold)
    descending or arched   most phrases arched or falling
    few durations          the two commonest durations cover at least three notes in four
    on a beat              every onset on a grid of half beats (the notation guarantees a grid; this checks it)
    motifs                 some four-note pattern of intervals and durations comes back"""
    iv = np.diff(m.pitches)
    pcs = {p % 12 for p in m.pitches}
    shapes = [contour(ph) for ph in m.phrases if len(ph) >= 3]
    durs = Counter(round(b, 2) for b in m.beats)
    top2 = sum(n for _, n in durs.most_common(2)) / len(m.beats)
    on = np.concatenate([[0.0], np.cumsum(np.round(np.asarray(m.beats) * 12) / 12)[:-1]])     # 0.33 is written for 1/3
    grams = Counter(tuple(zip(iv[i:i + 3], m.beats[i:i + 4])) for i in range(len(iv) - 2))
    return {
        "few scale degrees": len(pcs) <= 7,
        "small intervals": bool(np.mean(np.abs(iv) < 7.5) > 0.5),
        "descending or arched": bool(shapes) and sum(s in ("arch", "descending") for s in shapes) / len(shapes) > 0.5,
        "few durations": top2 >= 0.75,
        "on a beat": bool(np.all(np.abs(on * 12 - np.round(on * 12)) < 0.1)),
        "motifs": any(n > 1 for n in grams.values()),
    }


# --------------------------------------------------------------------------------------------- the oldest pipes


def pipe_hz(length: float, bore: float, c: float = 343.0) -> float:
    """An open-open pipe of ``length`` metres and ``bore`` (diameter): f = c / 2(L + end corrections), with 0.61 of
    the radius at the far end and, for a notched or edge-blown top, about 0.85 of the radius there."""
    a = bore / 2.0
    return c / (2.0 * (length + 0.61 * a + 0.85 * a))


def holes_scale(length: float, bore: float, holes, c: float = 343.0) -> list[float]:
    """A crude flute: opening the hole nearest the top end among those open makes the pipe sound as if it ended at that
    hole (plus a correction of a bore radius).  ``holes``: distances from the top end, in metres."""
    a = bore / 2.0
    out = [pipe_hz(length, bore, c)]
    for h in sorted(holes, reverse=True):
        out.append(c / (2.0 * (h + 0.85 * a + 2.0 * a)))
    return out


# --------------------------------------------------------------------------------------------- iterated reproduction


def ratio_points(patterns) -> list[tuple]:
    """Every distinct ordering of each integer pattern, as proportions of the cycle."""
    pts = []
    for pat in patterns:
        for q in sorted(set(permutations(pat))):
            s = sum(q)
            pts.append(tuple(x / s for x in q))
    return pts


class RhythmPrior:
    """A listener's expectation about three-interval rhythms: a mixture of narrow bumps at integer-ratio rhythms, with
    a little probability spread evenly over the rest.  ``weights`` maps an integer pattern, such as (1, 1, 2), to the
    weight shared by all its orderings."""

    def __init__(self, weights: dict, width: float = 0.02, floor: float = 0.04):
        self.patterns = list(weights)
        self.points, self.w = [], []
        for pat, wt in weights.items():
            q = ratio_points([pat])
            self.points += q
            self.w += [wt / len(q)] * len(q)
        self.points = np.array(self.points)[:, :2]
        self.w = np.array(self.w) / np.sum(self.w) * (1.0 - floor)
        self.width, self.floor = width, floor

    def sample_posterior(self, x, noise: float, rng) -> np.ndarray:
        """Heard ``x`` (first two proportions) with Gaussian noise ``noise``: draw a rhythm from the posterior.  Each
        bump's posterior is Gaussian; the even floor's posterior is the likelihood itself (cut to the triangle)."""
        s2, w2 = noise ** 2, self.width ** 2
        d2 = np.sum((self.points - x) ** 2, axis=1)
        tot = s2 + w2
        lik = np.exp(-d2 / (2 * tot)) / (2 * math.pi * tot)
        post = self.w * lik
        post_floor = self.floor * 2.0                          # the even density on the triangle (area 1/2) is 2
        z = post.sum() + post_floor
        if rng.random() < post_floor / z:
            m, v = x, s2
        else:
            k = rng.choice(len(post), p=post / post.sum())
            v = s2 * w2 / tot
            m = (self.points[k] * s2 + x * w2) / tot
        for _ in range(100):
            y = m + math.sqrt(v) * rng.standard_normal(2)
            if y.min() > 0.03 and y.sum() < 0.97:
                return y
        return np.clip(m, 0.04, 0.9)

    def mass_near(self, ys, radius: float = 0.04) -> float:
        """Share of rhythms within ``radius`` of an integer-ratio rhythm."""
        ys = np.asarray(ys)[:, :2]
        d = np.sqrt(((ys[:, None, :] - self.points[None, :, :]) ** 2).sum(-1)).min(1)
        return float(np.mean(d < radius))


def tap_back(x, prior: RhythmPrior, rng, sense: float = 0.05, motor: float = 0.015) -> np.ndarray:
    """One iteration: the listener hears ``x`` with noise, reproduces a draw from its posterior, with motor noise."""
    heard = np.asarray(x, float)[:2] + sense * rng.standard_normal(2)
    y = prior.sample_posterior(heard, sense, rng)
    for _ in range(100):
        z = y + motor * rng.standard_normal(2)
        if z.min() > 0.03 and z.sum() < 0.97:
            return z
    return y


def random_rhythm(rng, low: float = 0.1) -> np.ndarray:
    """Three intervals drawn evenly from the triangle, none shorter than ``low`` of the cycle."""
    while True:
        x = rng.dirichlet([1, 1, 1])
        if x.min() >= low:
            return x[:2]


def rhythm_chains(prior: RhythmPrior, chains: int = 400, iterations: int = 5, seed: int = 0, **kw) -> np.ndarray:
    """Positions (chains, iterations + 1, 3) of every chain, starting from random rhythms."""
    rng = np.random.default_rng(seed)
    out = np.zeros((chains, iterations + 1, 3))
    for c in range(chains):
        x = random_rhythm(rng)
        out[c, 0] = [x[0], x[1], 1 - x.sum()]
        for i in range(iterations):
            x = tap_back(x, prior, rng, **kw)
            out[c, i + 1] = [x[0], x[1], 1 - x.sum()]
    return out


def nearest_pattern(prior: RhythmPrior, y, radius: float = 0.04):
    """The integer pattern nearest a rhythm (or None if none is within ``radius``)."""
    y = np.asarray(y)[:2]
    d = np.sqrt(((prior.points - y) ** 2).sum(1))
    k = int(np.argmin(d))
    if d[k] >= radius:
        return None
    pts = []
    for pat in prior.patterns:
        pts += [pat] * len(ratio_points([pat]))
    return pts[k]


# --------------------------------------------------------------------------------------------- transmission

DURATIONS = (0.5, 1.0, 1.5, 2.0, 3.0, 4.0)                      # in beats
DUR_PRIOR = (0.16, 0.42, 0.06, 0.24, 0.07, 0.05)

SINGER = {"pitch_noise": 0.08, "dur_noise": 0.12, "category": 0.4, "leap": 7.5, "leap_cost": 0.3,
          "motor": 0.05, "dur_motor": 0.04, "slip": 0.003, "novel": 0.04,
          "home": 4.0, "pull": 0.15, "choose": "best"}


def categorize(pitches, width: float) -> np.ndarray:
    """Group heard pitches into categories: sorted, a pitch joins the category before it if within ``width`` of that
    category's mean; each note then takes its category's mean."""
    p = np.asarray(pitches, float)
    order = np.argsort(p)
    out = np.empty_like(p)
    group = [order[0]]
    for i in order[1:]:
        if p[i] - np.mean(p[group]) < width:
            group.append(i)
        else:
            out[group] = np.mean(p[group])
            group = [i]
    out[group] = np.mean(p[group])
    return out


def novelty(mel) -> list:
    """For each note, how much of it is new: 1 for a pitch level not heard before (no earlier note within half a
    semitone), 1 for a new interval from the note before, 1 for a new duration (none earlier within 10 per cent)."""
    out = []
    for i, (p, d) in enumerate(mel):
        lev = all(abs(p - q) >= 0.5 for q, _ in mel[:i])
        ivl = i > 0 and all(abs((p - mel[i - 1][0]) - (mel[j][0] - mel[j - 1][0])) >= 0.5 for j in range(1, i))
        dur = all(abs(math.log(d / e)) >= 0.1 for _, e in mel[:i])
        out.append(int(lev) + int(ivl) + int(dur))
    return out


def transmit(mel, rng, singer: dict | None = None) -> list:
    """One singer hears ``mel`` (a list of [pitch in semitones, duration in beats]) and sings it back.
    1. memory: what is new is what is hard to keep.  A note slips with probability ``slip`` + ``novel`` times its
       novelty (0 to 3, see ``novelty``) / 3.  A slipped note is left out, doubled, or (most often) filled with the
       melody's most familiar continuation: what followed the previous note's pitch somewhere earlier;
    2. hearing: each pitch blurred by ``pitch_noise`` semitones, each duration by ``dur_noise`` (proportional);
    3. pitch: a leap wider than ``leap`` semitones lands short, by ``leap_cost`` of the excess (only the landing note
       moves), and the heard pitches are sorted into categories (``category`` semitones wide);
    4. timing: each heard duration, measured against the melody's median, is replaced by the most probable simple
       value (half a beat to four beats) under a prior that favours one and two beats (``choose='sample'``: a draw
       from that posterior instead, which forgets the melody much faster);
    5. singing: motor noise on pitch and duration; the melody's median pitch is kept where it was heard, moved a
       fraction ``pull`` of the way toward the singer's comfortable ``home``."""
    s = {**SINGER, **(singer or {})}
    mel = [(float(x[0]), float(x[1])) for x in mel]
    nov = novelty(mel)
    kept = []
    for i, nt in enumerate(mel):
        if rng.random() < s["slip"] + s["novel"] * nov[i] / 3.0:
            kind = rng.choice(3, p=[0.25, 0.15, 0.60])
            if kind == 0 and len(mel) > 8:
                continue
            if kind == 1:
                kept += [nt, nt]
                continue
            if kept:
                prev = kept[-1][0]
                follow = [mel[j + 1] for j in range(i - 1) if abs(mel[j][0] - prev) < 0.5]
                kept.append(follow[int(rng.integers(len(follow)))] if follow else (prev, nt[1]))
                continue
        kept.append(nt)
    p = np.array([x[0] + s["pitch_noise"] * rng.standard_normal() for x in kept])
    d = np.array([x[1] * math.exp(s["dur_noise"] * rng.standard_normal()) for x in kept])
    mid = np.median(p)
    for i in range(1, len(p)):
        iv = p[i] - p[i - 1]
        if abs(iv) > s["leap"]:
            p[i] -= math.copysign(s["leap_cost"] * (abs(iv) - s["leap"]), iv)
    p += mid - np.median(p) + s["pull"] * (s["home"] - mid)
    p = categorize(p, s["category"])
    beat = np.median(d)
    cand = np.array(DURATIONS)
    prior = np.array(DUR_PRIOR)
    dd = []
    for x in d:
        lik = np.exp(-(np.log(x / beat) - np.log(cand)) ** 2 / (2 * 0.15 ** 2))
        post = prior * lik + 1e-12
        dd.append(float(cand[int(np.argmax(post))]) if s["choose"] == "best" else
                  float(cand[rng.choice(len(cand), p=post / post.sum())]))
    p = p + s["motor"] * rng.standard_normal(len(p))
    dd = [x * math.exp(s["dur_motor"] * rng.standard_normal()) for x in dd]
    return [[float(a), float(b)] for a, b in zip(p, dd)]


def random_melody(rng, n: int = 16, low: float = -5.0, high: float = 12.0) -> list:
    """Pitches drawn evenly between ``low`` and ``high`` semitones; durations log-evenly between 0.3 and 2.5 beats."""
    return [[float(rng.uniform(low, high)), float(math.exp(rng.uniform(math.log(0.3), math.log(2.5))))] for _ in range(n)]


def transmission_chain(mel, generations: int, rng, singer: dict | None = None) -> list:
    out = [mel]
    for _ in range(generations):
        out.append(transmit(out[-1], rng, singer))
    return out


def structure(mel) -> dict:
    """levels          distinct pitch levels (pitches within a third of a semitone count as one)
    reused          share of notes whose pitch level is used by another note too
    step            mean size of a melodic interval, semitones
    simple          share of durations within 10 per cent of a simple multiple of the median (1/2, 1, 3/2, 2, 3, 4)
    durations       distinct durations (within 8 per cent count as one)
    repeats         share of three-note patterns (pitch level, duration to the half beat) heard more than once
    echo            for each passage of four notes, the alignment cost per note to the most alike other passage of
                    the melody, averaged (0: every passage has an exact twin)"""
    p = np.array([x[0] for x in mel])
    d = np.array([x[1] for x in mel])
    srt = np.sort(p)
    levels = 1 + int(np.sum(np.diff(srt) > 1 / 3))
    reused = float(np.mean([np.sum(np.abs(p - x) < 1 / 3) > 1 for x in p]))
    beat = np.median(d)
    r = d / beat
    simple = float(np.mean([np.min(np.abs(np.log(x / np.array(DURATIONS)))) < 0.1 for x in r]))
    ld = np.sort(np.log(d))
    durs = 1 + int(np.sum(np.diff(ld) > 0.08))
    order = np.argsort(p)
    lab = np.empty(len(p), int)
    lab[order] = np.concatenate([[0], np.cumsum(np.diff(p[order]) > 1 / 3)])
    q = [(int(a), round(b / beat * 2) / 2) for a, b in zip(lab, d)]
    grams = Counter(tuple(q[i:i + 3]) for i in range(len(q) - 2))
    repeats = float(sum(n for n in grams.values() if n > 1) / max(sum(grams.values()), 1))
    step = float(np.mean(np.abs(np.diff(p)))) if len(p) > 1 else 0.0
    ch = [mel[i:i + 4] for i in range(0, len(mel) - 3, 4)]
    echo = float(np.mean([min(align(a, b)["per_note"] for j, b in enumerate(ch) if j != i) for i, a in enumerate(ch)])) if len(ch) > 1 else 1.0
    return {"levels": levels, "reused": reused, "step": step, "simple": simple, "durations": durs, "repeats": repeats,
            "echo": echo}


# --------------------------------------------------------------------------------------------- tune families


def note_cost(a, b) -> float:
    """Substituting one note for another: pitch distance (a whole tone costs a half) plus duration ratio (a doubling
    costs a half), capped at 1.5."""
    dp = abs(a[0] - b[0]) / 4.0
    dd = abs(math.log2(max(a[1], 1e-6) / max(b[1], 1e-6))) / 2.0
    return min(dp + dd, 1.5)


def align(a, b, gap: float = 1.0) -> dict:
    """Needleman-Wunsch alignment of two melodies (lists of [pitch, duration]); pitches compared relative to each
    melody's median.  Returns the cost, the cost per note of the longer melody, and the aligned pairs."""
    ma = np.median([x[0] for x in a])
    mb = np.median([x[0] for x in b])
    A = [(x[0] - ma, x[1]) for x in a]
    B = [(x[0] - mb, x[1]) for x in b]
    n, m = len(A), len(B)
    D = np.zeros((n + 1, m + 1))
    D[:, 0] = gap * np.arange(n + 1)
    D[0, :] = gap * np.arange(m + 1)
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            D[i, j] = min(D[i - 1, j - 1] + note_cost(A[i - 1], B[j - 1]), D[i - 1, j] + gap, D[i, j - 1] + gap)
    pairs, i, j = [], n, m
    while i > 0 or j > 0:
        if i > 0 and j > 0 and abs(D[i, j] - D[i - 1, j - 1] - note_cost(A[i - 1], B[j - 1])) < 1e-9:
            pairs.append((i - 1, j - 1))
            i, j = i - 1, j - 1
        elif i > 0 and abs(D[i, j] - D[i - 1, j] - gap) < 1e-9:
            pairs.append((i - 1, None))
            i -= 1
        else:
            pairs.append((None, j - 1))
            j -= 1
    pairs.reverse()
    return {"cost": float(D[n, m]), "per_note": float(D[n, m] / max(n, m)), "pairs": pairs}


def distances(mels) -> np.ndarray:
    k = len(mels)
    D = np.zeros((k, k))
    for i in range(k):
        for j in range(i + 1, k):
            D[i, j] = D[j, i] = align(mels[i], mels[j])["per_note"]
    return D


def upgma(D, names) -> dict:
    """Average-linkage clustering.  Returns the merges [(a, b, height)] (clusters named by tuples of leaves) and the
    tree as nested tuples."""
    clusters = {(n,): i for i, n in enumerate(names)}
    size = {(n,): 1 for n in names}
    dist = {}
    keys = list(clusters)
    for i, a in enumerate(keys):
        for b in keys[i + 1:]:
            dist[frozenset([a, b])] = float(D[clusters[a], clusters[b]])
    tree = {(n,): n for n in names}
    merges = []
    while len(keys) > 1:
        pair = min(dist, key=dist.get)
        a, b = sorted(pair, key=lambda k: keys.index(k))
        h = dist.pop(pair)
        new = a + b
        tree[new] = (tree.pop(a), tree.pop(b))
        size[new] = size[a] + size[b]
        keys = [k for k in keys if k not in (a, b)]
        for c in keys:
            da = dist.pop(frozenset([a, c]))
            db = dist.pop(frozenset([b, c]))
            dist[frozenset([new, c])] = (da * size[a] + db * size[b]) / size[new]
        keys.append(new)
        merges.append((list(a), list(b), h))
    return {"merges": merges, "tree": tree[keys[0]]}


def leaves(t) -> list:
    return [t] if not isinstance(t, tuple) else leaves(t[0]) + leaves(t[1])


def splits(t) -> set:
    """The clades of a rooted tree, as frozensets of leaves (the whole set and single leaves left out)."""
    out = set()
    every = frozenset(leaves(t))

    def walk(x):
        if isinstance(x, tuple):
            s = frozenset(leaves(x))
            if 1 < len(s) < len(every):
                out.add(s)
            walk(x[0])
            walk(x[1])

    walk(t)
    return out


def robinson_foulds(t1, t2) -> int:
    """Clades in one tree and not the other, counted both ways (0: the same branching)."""
    return len(splits(t1) ^ splits(t2))


def tree_transmission(root, depth: int, generations: int, rng, singer: dict | None = None) -> dict:
    """The melody ``root`` passed down a binary tree ``depth`` levels deep, ``generations`` singers along each branch.
    Returns the leaves' melodies (named A, B, ...), the true tree, and every branch's chain."""
    names = iter("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    chains = {}

    def grow(mel, level, path):
        if level == depth:
            n = next(names)
            return n, {n: mel}
        kids, mels = [], {}
        for side in "01":
            ch = transmission_chain(mel, generations, rng, singer)
            chains[path + side] = ch
            t, m = grow(ch[-1], level + 1, path + side)
            kids.append(t)
            mels.update(m)
        return tuple(kids), mels

    tree, mels = grow(root, 0, "")
    return {"tree": tree, "leaves": mels, "chains": chains}


# --------------------------------------------------------------------------------------------- on the beat?


def rayleigh(phases) -> dict:
    """Mean resultant length R of angles (radians), its direction, and the Rayleigh test's p-value (with Zar's
    correction): small p means the angles cluster."""
    th = np.asarray(phases, float)
    n = len(th)
    C, S = np.cos(th).sum(), np.sin(th).sum()
    R = math.hypot(C, S) / n
    z = n * R ** 2
    p = math.exp(math.sqrt(1 + 4 * n + 4 * (n * n - (n * R) ** 2)) - (1 + 2 * n))
    return {"R": float(R), "mean": float(math.atan2(S, C)), "z": float(z), "p": float(min(max(p, 0.0), 1.0)), "n": n}


def bobbing(beats: int, period: float, own_period: float, locked: bool, rng, jitter: float = 0.035, lead: float = -0.02) -> dict:
    """Head-bob times against a beat of ``period`` seconds.  A locked dancer corrects toward each beat (phase
    correction, as in Part 43); an unlocked one keeps its own period ``own_period``.  Returns bob times and phases."""
    t = 0.0 + lead
    bobs = []
    for k in range(beats):
        bobs.append(t)
        if locked:
            err = t - k * period
            t = t + own_period - 0.6 * err + jitter * rng.standard_normal() * period
        else:
            t = t + own_period + jitter * rng.standard_normal() * period
    bobs = np.array(bobs)
    ph = 2 * math.pi * ((bobs / period) % 1.0)
    return {"times": [float(x) for x in bobs], "phases": [float(x) for x in ph]}


# --------------------------------------------------------------------------------------------- what gets published


def publication_bias(studies: int = 300, true_d: float = 0.1, n_low: int = 10, n_high: int = 60,
                     publish_null: float = 0.15, seed: int = 0) -> dict:
    """``studies`` two-group experiments of a true standardized effect ``true_d``, each with n per group drawn
    between ``n_low`` and ``n_high``.  A study is published if it finds a significant positive effect (one-sided
    alpha 0.025, the upper half of a two-sided 0.05 test), otherwise with probability ``publish_null``."""
    from scipy import stats

    rng = np.random.default_rng(seed)
    rows = []
    for _ in range(studies):
        n = int(rng.integers(n_low, n_high + 1))
        a = rng.standard_normal(n) + true_d
        b = rng.standard_normal(n)
        sp = math.sqrt((a.var(ddof=1) + b.var(ddof=1)) / 2)
        d = (a.mean() - b.mean()) / sp
        se = math.sqrt(2 / n + d * d / (4 * n))
        t, p = stats.ttest_ind(a, b)
        sig = bool(p < 0.05 and t > 0)
        pub = sig or bool(rng.random() < publish_null)
        rows.append({"n": n, "d": float(d), "se": float(se), "sig": sig, "published": pub})
    pubd = [r["d"] for r in rows if r["published"]]
    w = np.array([1 / r["se"] ** 2 for r in rows if r["published"]])
    return {"rows": rows, "true_d": true_d, "mean_all": float(np.mean([r["d"] for r in rows])),
            "mean_published": float(np.mean(pubd)), "pooled_published": float(np.sum(w * np.array(pubd)) / w.sum()),
            "published": len(pubd), "significant": sum(r["sig"] for r in rows)}
