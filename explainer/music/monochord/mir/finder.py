"""Monochord's finders (Part 63, *Finding Music*).

    peaks, hashes, Index                 Wang's constellation fingerprint (2003): spectrogram peaks, paired into hashes
                                         (f1, f2, dt), stored with their time; a query votes for (track, offset) pairs
    false_match_rate                     the arithmetic of chance agreement between hashes
    embed                                a small content embedding: log-band energies and their spread, chroma, flux
    horse_test                           a classifier right for the wrong reason, and how to catch it (Sturm, 2014)
    listeners, implicit_als, recall_at_k simulated listeners with known tastes; Hu, Koren and Volinsky's implicit ALS (2008)
    feedback_loop                        recommending what is already played: popularity's runaway
    playlist                             an order through a set of songs in which neighbours sound alike
    contour, melody_distance             query by humming: a pitch contour, matched by dynamic time warping

No manim.  Checked in ``tests/music/test_finder.py``.
"""

from __future__ import annotations

import math
from collections import defaultdict

import numpy as np
from scipy.ndimage import maximum_filter

SR_FP = 8000                                   # fingerprints are taken at 8 kHz, as phones send


def to_8k(y, sr: int):
    y = np.asarray(y, float)
    if y.ndim == 2:
        y = y.mean(axis=1)
    if sr == SR_FP:
        return y
    from scipy.signal import resample_poly
    g = math.gcd(int(sr), SR_FP)
    return resample_poly(y, SR_FP // g, int(sr) // g)


# --------------------------------------------------------------------------------------------- fingerprints
def spectrogram(y, n: int = 1024, hop: int = 256):
    y = np.asarray(y, float)
    if len(y) < n:
        y = np.r_[y, np.zeros(n - len(y))]
    count = 1 + (len(y) - n) // hop
    idx = np.arange(n)[None, :] + hop * np.arange(count)[:, None]
    S = np.abs(np.fft.rfft(y[idx] * np.hanning(n)[None, :], axis=1)).T
    return 20 * np.log10(S + 1e-9)


def peaks(S, size=(15, 11), floor_db: float = -60.0, density: float = 20.0, hop_s: float = 256 / SR_FP) -> np.ndarray:
    """Constellation points: local maxima of the dB spectrogram in a ``size`` (frequency x time) neighbourhood,
    above ``floor_db`` relative to the loudest point, keeping about ``density`` a second (the strongest).
    Returns (frame, bin) pairs sorted by frame."""
    mx = maximum_filter(S, size=size, mode="constant", cval=-1e9)
    cand = np.argwhere((S == mx) & (S > S.max() + floor_db))
    if len(cand) == 0:
        return np.zeros((0, 2), int)
    secs = S.shape[1] * hop_s
    keep = int(max(1, density * secs))
    vals = S[cand[:, 0], cand[:, 1]]
    cand = cand[np.argsort(-vals)[:keep]]
    pts = np.stack([cand[:, 1], cand[:, 0]], axis=1)          # (frame, bin)
    return pts[np.argsort(pts[:, 0])]


def hashes(pts, fan: int = 5, dt_max: int = 63, df_max: int = 127) -> list:
    """Pair each anchor with up to ``fan`` later peaks within ``dt_max`` frames: hash = (f1, f2, dt), packed into an
    integer (9 + 9 + 6 bits); stored with the anchor's frame."""
    out = []
    for i in range(len(pts)):
        t1, f1 = int(pts[i, 0]), int(pts[i, 1])
        n = 0
        for j in range(i + 1, len(pts)):
            t2, f2 = int(pts[j, 0]), int(pts[j, 1])
            dt = t2 - t1
            if dt <= 0:
                continue
            if dt > dt_max:
                break
            if abs(f2 - f1) > df_max:
                continue
            out.append(((f1 & 511) << 15 | (f2 & 511) << 6 | (dt & 63), t1))
            n += 1
            if n >= fan:
                break
    return out


def fingerprint(y, sr: int) -> list:
    return hashes(peaks(spectrogram(to_8k(y, sr))))


class Index:
    """A hash table from hash to (track, anchor frame)."""

    def __init__(self):
        self.table = defaultdict(list)
        self.names: list = []
        self.frames: list = []

    def add(self, name: str, y, sr: int) -> int:
        k = len(self.names)
        self.names.append(name)
        hs = fingerprint(y, sr)
        for h, t in hs:
            self.table[h].append((k, t))
        self.frames.append(len(hs))
        return len(hs)

    def query(self, y, sr: int, top: int = 3, shifts: int = 4) -> list:
        """Each query hash votes for (track, track frame - query frame); a true match piles its votes on one offset.
        The query is fingerprinted at ``shifts`` sub-frame starts (a query rarely begins on the library's frame grid,
        and a peak moved by one frame changes its hashes), and the votes are pooled.  Returns the best tracks with their
        aligned vote counts and offsets (seconds)."""
        y8 = to_8k(y, sr)
        votes = defaultdict(int)
        for s in range(shifts):
            off = int(round(s * 256 / shifts))
            for h, t in hashes(peaks(spectrogram(y8[off:]))):
                for k, tt in self.table.get(h, ()):
                    votes[(k, tt - t)] += 1
        best = defaultdict(lambda: (0, 0))
        for (k, off), v in votes.items():
            if v > best[k][0]:
                best[k] = (v, off)
        ranked = sorted(best.items(), key=lambda kv: -kv[1][0])[:top]
        return [{"track": self.names[k], "votes": v, "offset_s": off * 256 / SR_FP} for k, (v, off) in ranked]

    def matches(self, y, sr: int, track: str, shifts: int = 4) -> np.ndarray:
        """Every hash of the query that is also in ``track``, pooled over the same sub-frame starts as ``query``:
        (query frame, track frame) pairs.  For the true track most fall on one diagonal line, the offset; for any other
        they scatter."""
        k = self.names.index(track)
        y8 = to_8k(y, sr)
        out = []
        for s in range(shifts):
            off = int(round(s * 256 / shifts))
            for h, t in hashes(peaks(spectrogram(y8[off:]))):
                for kk, tt in self.table.get(h, ()):
                    if kk == k:
                        out.append((t, tt))
        return np.array(out, float).reshape(-1, 2)

    @property
    def size(self) -> int:
        return sum(len(v) for v in self.table.values())


def false_match_rate(bits: int = 24, query_hashes: int = 400, db_hashes: int = 5_000_000, tracks: int = 1000, offsets: int = 2000) -> dict:
    """Idealized uniform independent hash model: a specified stored hash matches with probability 2^-bits.
    Expected hits are query x database / 2^bits, distributed uniformly over tracks x offsets bins. The returned
    tails are union bounds from a Poisson approximation, not measured false-positive rates for correlated music
    fingerprints. Thresholds for a real index require empirical calibration."""
    p = 2.0 ** -bits
    hits = query_hashes * db_hashes * p
    per_bin = hits / (tracks * offsets)
    # the chance that some bin collects at least m chance hits (Poisson tail, union bound over bins)
    tail = {}
    for m in (2, 3, 4, 5, 6, 8, 10):
        lam = per_bin
        upper = sum(math.exp(-lam) * lam ** j / math.factorial(j) for j in range(m, m + 40))     # P(X >= m), summed directly
        tail[m] = min(1.0, tracks * offsets * upper)
    return {"p_hash": p, "chance_hits": hits, "per_bin": per_bin, "p_some_bin_at_least": tail}


# --------------------------------------------------------------------------------------------- content features
def embed(y, sr: int) -> np.ndarray:
    """A small content embedding: the mean and spread of 24 log-band energies, a 12-bin chroma, and the mean and spread
    of spectral flux; each block standardized later across a collection."""
    y = to_8k(y, sr)
    S = np.abs(np.fft.rfft(np.lib.stride_tricks.sliding_window_view(np.r_[y, np.zeros(2048)], 1024)[::256] * np.hanning(1024), axis=1)).T
    f = np.fft.rfftfreq(1024, 1 / SR_FP)
    edges = np.geomspace(60, 3900, 25)
    bands = np.array([S[(f >= a) & (f < b)].sum(axis=0) for a, b in zip(edges, edges[1:])])
    L = np.log(bands + 1e-6)
    chroma = np.zeros(12)
    good = f > 60
    pc = (np.round(12 * np.log2(f[good] / 261.63)) % 12).astype(int)
    e = (S[good] ** 2).mean(axis=1)
    for k in range(12):
        chroma[k] = e[pc == k].sum()
    chroma /= chroma.sum() + 1e-12
    flux = np.maximum(np.diff(np.log1p(S), axis=1), 0).sum(axis=0)
    return np.r_[L.mean(axis=1), L.std(axis=1), chroma, [flux.mean(), flux.std()]]


def standardize(X):
    X = np.asarray(X, float)
    return (X - X.mean(axis=0)) / (X.std(axis=0) + 1e-9)


def knn_predict(Xtr, ytr, Xte, k: int = 3):
    D = ((Xte[:, None, :] - Xtr[None, :, :]) ** 2).sum(axis=2)
    nn = np.argsort(D, axis=1)[:, :k]
    out = []
    for row in nn:
        vals, counts = np.unique(np.asarray(ytr)[row], return_counts=True)
        out.append(vals[np.argmax(counts)])
    return np.array(out)


def logistic(X, y, l2: float = 1e-2, iters: int = 400, lr: float = 0.5):
    X = np.c_[np.ones(len(X)), X]
    w = np.zeros(X.shape[1])
    y = np.asarray(y, float)
    for _ in range(iters):
        p = 1 / (1 + np.exp(-X @ w))
        w -= lr * (X.T @ (p - y) / len(y) + l2 * np.r_[0, w[1:]])
    return w


def logistic_predict(w, X):
    return (np.c_[np.ones(len(X)), X] @ w > 0).astype(int)


# --------------------------------------------------------------------------------------------- listeners
def listeners(n_users: int = 600, n_items: int = 300, k: int = 6, seed: int = 0, popularity: float = 1.0, plays: float = 40.0) -> dict:
    """Simulated listeners with known tastes: users and items have k latent factors; a user's affinity for an item is
    their dot product plus the item's popularity; plays are Poisson with that affinity's softmax as the rate.
    Returns the play matrix, the true affinities, and the factors."""
    rng = np.random.default_rng(seed)
    U = rng.normal(0, 1, (n_users, k))
    V = rng.normal(0, 1, (n_items, k))
    pop = popularity * rng.normal(0, 1, n_items)
    A = U @ V.T / math.sqrt(k) + pop[None, :]
    P = np.exp(A - A.max(axis=1, keepdims=True))
    P /= P.sum(axis=1, keepdims=True)
    R = rng.poisson(plays * P)
    return {"R": R, "A": A, "U": U, "V": V, "pop": pop}


def implicit_als(R, k: int = 8, alpha: float = 20.0, reg: float = 0.1, iters: int = 10, seed: int = 0) -> dict:
    """Hu, Koren and Volinsky (2008): preference p = [r > 0], confidence c = 1 + alpha r; minimize
    sum c (p - x.y)^2 + reg (|x|^2 + |y|^2) by alternating least squares."""
    rng = np.random.default_rng(seed)
    n_u, n_i = R.shape
    X = rng.normal(0, 0.1, (n_u, k))
    Y = rng.normal(0, 0.1, (n_i, k))
    Pm = (R > 0).astype(float)
    Cm = 1 + alpha * R
    I = np.eye(k)
    for _ in range(iters):
        YtY = Y.T @ Y
        for u in range(n_u):
            c = Cm[u]
            A = YtY + (Y.T * (c - 1)) @ Y + reg * I
            X[u] = np.linalg.solve(A, (Y.T * c) @ Pm[u])
        XtX = X.T @ X
        for i in range(n_i):
            c = Cm[:, i]
            A = XtX + (X.T * (c - 1)) @ X + reg * I
            Y[i] = np.linalg.solve(A, (X.T * c) @ Pm[:, i])
    return {"X": X, "Y": Y}


def recall_at_k(scores, held, train, k: int = 10) -> float:
    """For each user with held-out items: the share of them in the top k of the scores, excluding items seen in
    training."""
    s = np.where(train > 0, -np.inf, scores)
    top = np.argsort(-s, axis=1)[:, :k]
    hits, total = 0, 0
    for u in range(len(held)):
        h = np.flatnonzero(held[u] > 0)
        if len(h) == 0:
            continue
        hits += len(set(top[u]) & set(h))
        total += min(len(h), k)
    return hits / max(total, 1)


def split(R, frac: float = 0.2, seed: int = 0):
    rng = np.random.default_rng(seed)
    train, held = R.copy(), np.zeros_like(R)
    for u in range(R.shape[0]):
        items = np.flatnonzero(R[u] > 0)
        if len(items) < 3:
            continue
        pick = rng.choice(items, size=max(1, int(frac * len(items))), replace=False)
        held[u, pick] = R[u, pick]
        train[u, pick] = 0
    return train, held


def feedback_loop(n_users: int = 400, n_items: int = 200, rounds: int = 30, seed: int = 0, explore: float = 0.0, k: int = 5) -> dict:
    """A service recommends each user the k items with the most plays so far (popularity), each replaced, with
    probability ``explore``, by a random item; users play a recommendation if it suits them (their true affinity's logistic).  The
    plays feed the next round's popularity.  Returns the Gini of plays over rounds and the share of the top 1% of
    items, against a world where users find items on their own."""
    rng = np.random.default_rng(seed)
    L = listeners(n_users, n_items, seed=seed, popularity=0.3)
    A = L["A"]
    like = 1 / (1 + np.exp(-(A - np.median(A))))
    plays = np.ones(n_items)
    own = np.ones(n_items)
    ginis, own_g = [], []
    from .. import business as B
    for _ in range(rounds):
        order = np.argsort(-plays)[:k]
        for u in range(n_users):
            recs = [int(rng.integers(n_items)) if rng.random() < explore else int(i) for i in order]
            for i in recs:
                if rng.random() < like[u, i]:
                    plays[i] += 1
            j = int(rng.integers(n_items))                    # the world without a recommender: users browse
            if rng.random() < like[u, j]:
                own[j] += 1
        ginis.append(B.gini(plays))
        own_g.append(B.gini(own))
    return {"gini": ginis, "gini_own": own_g, "top1": B.top_share(plays, 0.01), "top1_own": B.top_share(own, 0.01), "plays": plays, "own": own}


# --------------------------------------------------------------------------------------------- playlists
def playlist(X, start: int = 0) -> list:
    """An order through the items in which neighbours are close: nearest neighbour from ``start``, then 2-opt
    improvement of the total path length."""
    X = np.asarray(X, float)
    n = len(X)
    D = np.sqrt(((X[:, None, :] - X[None, :, :]) ** 2).sum(axis=2))
    order, left = [start], set(range(n)) - {start}
    while left:
        last = order[-1]
        nxt = min(left, key=lambda j: D[last, j])
        order.append(nxt)
        left.remove(nxt)
    improved = True
    while improved:
        improved = False
        for i in range(1, n - 2):
            for j in range(i + 1, n - 1):
                a, b, c, d = order[i - 1], order[i], order[j], order[j + 1]
                if D[a, c] + D[b, d] < D[a, b] + D[c, d] - 1e-12:
                    order[i:j + 1] = order[i:j + 1][::-1]
                    improved = True
    return order


def path_length(X, order) -> float:
    X = np.asarray(X, float)
    return float(sum(np.linalg.norm(X[a] - X[b]) for a, b in zip(order, order[1:])))


# --------------------------------------------------------------------------------------------- query by humming
def contour(f0, voiced, every: int = 4) -> np.ndarray:
    """A pitch track as semitones, voiced frames only, kept one in ``every``: the shape a hummed query searches with."""
    f = np.asarray(f0, float)[np.asarray(voiced, bool)]
    return 12 * np.log2(f[::every] / 440.0) + 69


def melody_distance(q, r) -> float:
    """Dynamic time warping between two pitch contours, each centred on its median so that the key does not matter,
    with |difference| in semitones as the local cost; normalized by the lengths.  Small for the same tune at any tempo."""
    q = np.asarray(q, float) - np.median(q)
    r = np.asarray(r, float) - np.median(r)
    n, m = len(q), len(r)
    C = np.minimum(np.abs(q[:, None] - r[None, :]), 3.0)        # a wrong note costs at most three semitones
    D = np.full((n + 1, m + 1), np.inf)
    D[0, 0] = 0.0
    for i in range(1, n + 1):
        row = D[i - 1]
        cur = D[i]
        ci = C[i - 1]
        for j in range(1, m + 1):
            cur[j] = ci[j - 1] + min(row[j - 1], row[j], cur[j - 1])
    return float(D[n, m] / (n + m))
