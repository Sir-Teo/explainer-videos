"""Monochord's codecs (Part 58 of *Music, Built*): entropy and a lossless coder, the MDCT and its alias cancellation, a
masking model, a perceptual coder with rate control, window sizes and pre-echo, mid-side coding, listening-test
statistics, and residual vector quantization.

    entropy_bits(x)                         the empirical entropy of a sequence of integers, bits per symbol
    lossless_encode / lossless_decode       fixed linear prediction (orders 0 to 4) and Rice codes, block by block
    mdct_matrix(N) / mdct / imdct           the modified discrete cosine transform, frames of 2N, hop N, sine window
    frames_mdct / frames_imdct              a whole signal analysed and rebuilt (time-domain aliasing cancellation)
    bands(N, sr)                            critical bands (Bark) as MDCT bin ranges
    mask(X, sr)                             a masking threshold per band for one frame: spreading, tonality, quiet
    encode(x, kbps, ...)                    a perceptual coder: per-band step sizes from the mask, a global margin
                                            found by bisection to meet the bit rate, Rice-coded coefficients
    abx_power(n, p_true, alpha)             the chance an ABX test of n trials detects a listener who is right with p
    rvq_train / rvq_encode                  residual vector quantization: codebooks in stages, each coding the last's error

No manim here.  Checked in ``tests/music/test_codec.py``.
"""

from __future__ import annotations

import math
from functools import lru_cache

import numpy as np
from scipy.stats import binom

from explainer.music.monochord import ear as EAR

SR = 48000


# --------------------------------------------------------------------------------------------- entropy and lossless
def entropy_bits(x) -> float:
    x = np.asarray(x).ravel()
    _, counts = np.unique(x, return_counts=True)
    p = counts / counts.sum()
    return float(-(p * np.log2(p)).sum())


def zigzag(e):
    e = np.asarray(e, dtype=np.int64)
    return np.where(e >= 0, 2 * e, -2 * e - 1)


def unzigzag(u):
    u = np.asarray(u, dtype=np.int64)
    return np.where(u % 2 == 0, u // 2, -(u + 1) // 2)


def rice_cost(u, k: int) -> int:
    u = np.asarray(u, dtype=np.int64)
    return int(np.sum((u >> k) + 1 + k))


def best_k(u) -> int:
    return min(range(0, 24), key=lambda k: rice_cost(u, k))


class BitWriter:
    def __init__(self):
        self.out = bytearray()
        self.acc = 0
        self.n = 0

    def write(self, value: int, bits: int):
        self.acc = (self.acc << bits) | (value & ((1 << bits) - 1))
        self.n += bits
        while self.n >= 8:
            self.n -= 8
            self.out.append((self.acc >> self.n) & 0xFF)
        self.acc &= (1 << self.n) - 1

    def unary(self, q: int):
        while q >= 16:
            self.write(0, 16)
            q -= 16
        self.write(1, q + 1)

    def bytes(self) -> bytes:
        if self.n:
            return bytes(self.out) + bytes([(self.acc << (8 - self.n)) & 0xFF])
        return bytes(self.out)


class BitReader:
    def __init__(self, data: bytes):
        self.data = data
        self.pos = 0                                      # in bits

    def read(self, bits: int) -> int:
        v = 0
        for _ in range(bits):
            byte = self.data[self.pos >> 3]
            v = (v << 1) | ((byte >> (7 - (self.pos & 7))) & 1)
            self.pos += 1
        return v

    def unary(self) -> int:
        q = 0
        while True:
            byte = self.data[self.pos >> 3]
            bit = (byte >> (7 - (self.pos & 7))) & 1
            self.pos += 1
            if bit:
                return q
            q += 1


def residual(x, order: int):
    """Shorten's fixed predictors: order 1 predicts x[n-1], 2 predicts 2x[n-1] - x[n-2], and so on (the residual is
    the order-th difference)."""
    e = np.asarray(x, dtype=np.int64)
    for _ in range(order):
        e = np.diff(e)
    return e


def undo_residual(warm, e, order: int):
    """Rebuild a block from its first ``order`` samples and its residual."""
    x = np.asarray(warm, dtype=np.int64)
    # differences of each order at the block's start
    starts = []
    d = x.copy()
    for o in range(order):
        starts.append(int(d[0]))
        d = np.diff(d)
    y = np.asarray(e, dtype=np.int64)
    for o in reversed(range(order)):
        y = np.r_[starts[o], starts[o] + np.cumsum(y)]
    return y


def lossless_encode(x, block: int = 4096) -> dict:
    """16-bit integer samples, block by block: the best fixed predictor (order 0 to 4), its residual zigzagged and
    Rice-coded with the best parameter k.  Returns the bytes and what was chosen."""
    x = np.asarray(x, dtype=np.int64)
    bw = BitWriter()
    bw.write(len(x), 32)
    chosen = []
    for a in range(0, len(x), block):
        seg = x[a:a + block]
        best = None
        for order in range(0, min(5, len(seg))):
            u = zigzag(residual(seg, order))
            k = best_k(u)
            cost = rice_cost(u, k) + 16 * order
            if best is None or cost < best[0]:
                best = (cost, order, k, u)
        _, order, k, u = best
        chosen.append((order, k))
        bw.write(order, 3)
        bw.write(k, 5)
        for s in seg[:order]:
            bw.write(int(s) & 0xFFFF, 16)
        for v in u.tolist():
            bw.unary(v >> k)
            if k:
                bw.write(v & ((1 << k) - 1), k)
    data = bw.bytes()
    return {"data": data, "bits": 8 * len(data), "chosen": chosen, "block": block}


def lossless_decode(data: bytes, block: int = 4096) -> np.ndarray:
    br = BitReader(data)
    n = br.read(32)
    out = []
    left = n
    while left > 0:
        m = min(block, left)
        order = br.read(3)
        k = br.read(5)
        warm = []
        for _ in range(min(order, m)):
            v = br.read(16)
            warm.append(v - 65536 if v >= 32768 else v)
        u = []
        for _ in range(m - order):
            q = br.unary()
            r = br.read(k) if k else 0
            u.append((q << k) | r)
        e = unzigzag(np.array(u, dtype=np.int64))
        out.append(undo_residual(np.array(warm, dtype=np.int64), e, order) if order else e)
        left -= m
    return np.concatenate(out)


# --------------------------------------------------------------------------------------------- the MDCT
@lru_cache(maxsize=8)
def mdct_matrix(N: int):
    n = np.arange(2 * N)
    k = np.arange(N)
    C = np.cos(np.pi / N * (n[None, :] + 0.5 + N / 2) * (k[:, None] + 0.5))
    w = np.sin(np.pi * (n + 0.5) / (2 * N))
    return C, w


def mdct(frame, N: int) -> np.ndarray:
    C, w = mdct_matrix(N)
    return C @ (w * frame)


def imdct(X, N: int) -> np.ndarray:
    """The inverse of one frame, windowed: on its own it is the frame plus time-domain aliases (a mirrored copy in
    each half); overlapped and added with its neighbours, the aliases cancel."""
    C, w = mdct_matrix(N)
    return w * (C.T @ X) * (2.0 / N)


def frames_mdct(x, N: int) -> np.ndarray:
    """MDCT frames of a whole signal, hop N, padded by N at each end so that every sample is covered twice."""
    x = np.r_[np.zeros(N), np.asarray(x, float), np.zeros(N + (-len(x)) % N)]
    F = (len(x) - N) // N
    C, w = mdct_matrix(N)
    idx = np.arange(F)[:, None] * N + np.arange(2 * N)[None, :]
    return (w[None, :] * x[idx]) @ C.T


def frames_imdct(X, N: int, length: int) -> np.ndarray:
    C, w = mdct_matrix(N)
    F = X.shape[0]
    y = np.zeros((F + 1) * N)
    blocks = (X @ C) * w[None, :] * (2.0 / N)
    for i in range(F):
        y[i * N: i * N + 2 * N] += blocks[i]
    return y[N: N + length]


# --------------------------------------------------------------------------------------------- the masking model
FULL_SCALE_SPL = 96.0       # a full-scale sine is taken to play at 96 dB SPL
QUIET_CAP_DB = 60.0         # Terhardt's fit rises without limit above 16 kHz; above 60 dB SPL it is no longer a threshold


@lru_cache(maxsize=8)
def bands(N: int, sr: int = SR, per_bark: float = 1.0):
    """MDCT bins grouped into bands one Bark wide (wider at the top for a minimum of 4 bins): [(lo, hi)]."""
    f = (np.arange(N) + 0.5) * sr / (2 * N)
    z = EAR.bark(f)
    edges = [0]
    start_z = z[0]
    for i in range(1, N):
        if z[i] - start_z >= per_bark and i - edges[-1] >= 4:
            edges.append(i)
            start_z = z[i]
    edges.append(N)
    return tuple(zip(edges[:-1], edges[1:]))


def spreading_db(dz):
    """Schroeder's spreading function (1979): how far masking reaches across critical bands, dB."""
    dz = np.asarray(dz, float)
    return 15.81 + 7.5 * (dz + 0.474) - 17.5 * np.sqrt(1 + (dz + 0.474) ** 2)


def mask(X, N: int, sr: int = SR) -> dict:
    """One frame's allowed noise per band (power in MDCT units).  Band energies are spread across the Bark scale,
    lowered by an offset that depends on how tonal the frame is (Johnston, 1988: 14.5 + z dB below a tone, 5.5 below
    noise; tonality from the spectral flatness), and never put below the threshold in quiet (Part 4)."""
    B = bands(N, sr)
    P = np.asarray(X, float) ** 2
    E = np.array([P[a:b].sum() for a, b in B]) + 1e-20
    fc = np.array([(a + b) / 2 * sr / (2 * N) for a, b in B])
    z = EAR.bark(fc)
    S = 10 ** (spreading_db(z[:, None] - z[None, :]) / 10)            # S[i, j]: masker j's reach into band i
    spread = S @ E
    gm = np.exp(np.mean(np.log(P[P > 0] + 1e-30))) if np.any(P > 0) else 1e-30
    sfm = 10 * math.log10(gm / (P.mean() + 1e-30) + 1e-30)
    alpha = min(sfm / -60.0, 1.0)                                       # 1: tonal, 0: noisy
    offset = alpha * (14.5 + z) + (1 - alpha) * 5.5
    T = spread * 10 ** (-offset / 10)
    # the threshold in quiet, from dB SPL to MDCT power: a full-scale sine has MDCT power about N^2 / 4 in its bin
    width = np.array([b - a for a, b in B])
    quiet = 10 ** ((np.minimum(EAR.threshold_db(np.maximum(fc, 20.0)), QUIET_CAP_DB) - FULL_SCALE_SPL) / 10) * (N ** 2 / 4) * width
    allowed = np.maximum(T, quiet)
    return {"bands": B, "energy": E, "spread": spread, "allowed": allowed, "quiet": quiet, "alpha": alpha, "fc": fc}


# --------------------------------------------------------------------------------------------- the perceptual coder
LOWPASS = {12: 5000.0, 24: 7000.0, 32: 9000.0, 48: 12000.0, 64: 14000.0, 96: 16000.0, 128: 18000.0, 192: 20000.0, 256: 20000.0}


def rice_bits(q) -> int:
    u = zigzag(q)
    if not np.any(u):
        return 1
    return rice_cost(u, best_k(u)) + 5


def code_frames(X, N: int, margin_db: float, cutoff: float, sr: int = SR, masks=None):
    """Quantize every frame's bands with step sizes that put the quantization noise ``margin_db`` below the allowed
    noise; return the decoded coefficients and the bits (Rice-coded values, 6-bit scale factors)."""
    masks = masks or [mask(x, N, sr) for x in X]
    Y = np.zeros_like(X)
    bits = 0
    for i, (x, m) in enumerate(zip(X, masks)):
        for (a, b), Nb in zip(m["bands"], m["allowed"]):
            if (a + b) / 2 * sr / (2 * N) > cutoff:
                bits += 1
                continue
            step = math.sqrt(12.0 * Nb / (b - a)) * 10 ** (-margin_db / 20)
            q = np.round(x[a:b] / step)
            bits += 6 + rice_bits(q)
            Y[i, a:b] = q * step
    return Y, bits, masks


def encode(x, kbps: float, N: int = 1024, sr: int = SR, cutoff: float | None = None, tol: float = 0.02) -> dict:
    """A perceptual coder: MDCT frames, a mask per frame, step sizes from the mask, and a global margin found by
    bisection so that the average bit rate meets ``kbps``.  Returns the decoded signal, the margin, the bit rate and the
    noise-to-mask ratio."""
    x = np.asarray(x, float)
    X = frames_mdct(x, N)
    cutoff = cutoff or LOWPASS.get(int(kbps), 18000.0)
    target = kbps * 1000 * len(x) / sr
    masks = [mask(f, N, sr) for f in X]
    lo, hi = -40.0, 60.0
    best = None
    for _ in range(26):
        mid = (lo + hi) / 2
        Y, bits, _ = code_frames(X, N, mid, cutoff, sr, masks)
        if bits > target:
            hi = mid
        else:
            lo = mid
            best = (mid, Y, bits)
        if best and abs(bits - target) / target < tol:
            break
    if best is None:
        best = (lo,) + code_frames(X, N, lo, cutoff, sr, masks)[:2]
    margin, Y, bits = best
    y = frames_imdct(Y, N, len(x))
    # the noise-to-mask ratio, averaged over coded bands
    nmr = []
    for f, g, m in zip(X, Y, masks):
        for (a, b), Nb in zip(m["bands"], m["allowed"]):
            if (a + b) / 2 * sr / (2 * N) <= cutoff:
                nmr.append(10 * math.log10((np.sum((f[a:b] - g[a:b]) ** 2) + 1e-20) / Nb))
    nmr = np.array(nmr)
    return {"y": y, "margin_db": margin, "kbps": bits * sr / len(x) / 1000, "cutoff": cutoff, "nmr_db": float(np.mean(nmr)),
            "over": float(np.mean(nmr > 0.0)), "N": N, "frames": len(X)}


def encode_at(x, margin_db: float, N: int = 1024, sr: int = SR, cutoff: float = 16000.0) -> dict:
    """Code at a fixed margin to the mask (0 dB: the noise exactly at the allowed level) and report the bit rate it
    takes: how block length trades bits against where the noise falls."""
    x = np.asarray(x, float)
    X = frames_mdct(x, N)
    Y, bits, _ = code_frames(X, N, margin_db, cutoff, sr)
    return {"y": frames_imdct(Y, N, len(x)), "kbps": bits * sr / len(x) / 1000, "N": N}


# --------------------------------------------------------------------------------------------- listening tests
def abx_threshold(n: int, alpha: float = 0.05) -> int:
    """The fewest correct answers out of n that a guesser reaches with probability under alpha."""
    for c in range(n + 1):
        if binom.sf(c - 1, n, 0.5) < alpha:
            return c
    return n + 1


def abx_power(n: int, p_true: float, alpha: float = 0.05) -> float:
    """The chance that a listener who is right with probability p_true passes an n-trial ABX test at level alpha."""
    c = abx_threshold(n, alpha)
    return float(binom.sf(c - 1, n, p_true))


# --------------------------------------------------------------------------------------------- residual vector quantization
def kmeans(V, k: int, iters: int = 25, seed: int = 0):
    rng = np.random.default_rng(seed)
    C = V[rng.choice(len(V), size=k, replace=False)].copy()
    for _ in range(iters):
        d = ((V[:, None, :] - C[None, :, :]) ** 2).sum(axis=2)
        a = d.argmin(axis=1)
        for j in range(k):
            sel = V[a == j]
            C[j] = sel.mean(axis=0) if len(sel) else V[rng.integers(len(V))]
    return C


def nearest(V, C):
    out = np.empty(len(V), dtype=int)
    for a in range(0, len(V), 4096):
        d = ((V[a:a + 4096, None, :] - C[None, :, :]) ** 2).sum(axis=2)
        out[a:a + 4096] = d.argmin(axis=1)
    return out


def rvq_train(V, stages: int, k: int, seed: int = 0):
    """Train ``stages`` codebooks of k vectors: each on the error the previous stages leave."""
    books = []
    R = np.asarray(V, float).copy()
    for s in range(stages):
        C = kmeans(R, k, seed=seed + s)
        R = R - C[nearest(R, C)]
        books.append(C)
    return books


def rvq_encode(V, books, stages: int | None = None):
    """Code vectors with the first ``stages`` codebooks; return the reconstruction and the codes."""
    R = np.asarray(V, float).copy()
    Y = np.zeros_like(R)
    codes = []
    for C in books[: stages or len(books)]:
        a = nearest(R, C)
        Y += C[a]
        R -= C[a]
        codes.append(a)
    return Y, codes
