"""Attention as a GPU computes it (Part 19's ``flash`` item): the online softmax, FlashAttention's tiles, its memory
traffic counted, and Flash-Decoding's split of the keys and values, each checked against the plain formula.

Memory traffic is counted in numbers moved between the large memory (HBM) and the small fast one (SRAM, M numbers),
for one head: by the formulas of Dao et al. (2022), and by running the loops of their Algorithm 1 with a counter in
place of the data (the two agree, which is the check).
"""

from __future__ import annotations

import math

import numpy as np


def softmax_rows(S):
    P = np.exp(S - S.max(-1, keepdims=True))
    return P / P.sum(-1, keepdims=True)


def plain_attention(Q, K, V, causal=True):
    S = Q @ K.T / math.sqrt(Q.shape[1])
    if causal:
        S = np.where(np.tril(np.ones(S.shape, bool)), S, -np.inf)
    return softmax_rows(S) @ V


def online_softmax_trace(s, tile):
    """One row of scores streamed in tiles: the running maximum m and the running sum l after each tile, and the
    final softmax (equal to the direct one)."""
    m, l, out = -np.inf, 0.0, []
    for j in range(0, len(s), tile):
        t = s[j:j + tile]
        m_new = max(m, float(t.max()))
        l = l * math.exp(m - m_new) + float(np.exp(t - m_new).sum())
        m = m_new
        out.append((m, l))
    return np.array(out), np.exp(s - m) / l


def flash_attention(Q, K, V, Br, Bc, causal=True):
    """FlashAttention, forward: blocks of Br queries; for each, stream blocks of Bc keys and values through, keeping a
    running max m, a running sum l and an unnormalized output o, rescaled whenever the max grows (the online
    softmax).  Never forms the T x T table."""
    T, d = Q.shape
    O = np.zeros_like(Q)
    for i in range(0, T, Br):
        q = Q[i:i + Br]
        m = np.full(len(q), -np.inf)
        l = np.zeros(len(q))
        o = np.zeros((len(q), d))
        for j in range(0, T, Bc):
            if causal and j > i + len(q) - 1:
                break  # blocks entirely in the future are skipped
            s = q @ K[j:j + Bc].T / math.sqrt(d)
            if causal:
                qi = np.arange(i, i + len(q))[:, None]
                kj = np.arange(j, j + s.shape[1])[None, :]
                s = np.where(kj <= qi, s, -np.inf)
            m_new = np.maximum(m, s.max(1))
            a = np.exp(m - m_new)
            p = np.exp(s - m_new[:, None])
            l = l * a + p.sum(1)
            o = o * a[:, None] + p @ V[j:j + Bc]
            m = m_new
        O[i:i + Br] = o / l[:, None]
    return O


def split_kv_decode(q, K, V, splits):
    """Flash-Decoding for one query: split the keys and values into chunks, attend within each (its max m_s, sum l_s
    and partial output o_s, computable in parallel), then combine with the log-sum-exp weights."""
    d = len(q)
    parts = []
    for idx in np.array_split(np.arange(len(K)), splits):
        s = K[idx] @ q / math.sqrt(d)
        m = s.max()
        p = np.exp(s - m)
        parts.append((m, p.sum(), p @ V[idx]))
    M = max(m for m, _, _ in parts)
    L = sum(math.exp(m - M) * l for m, l, _ in parts)
    o = sum(math.exp(m - M) * ov for m, _, ov in parts)
    return o / L, parts


# ---------------------------------------------------------------------------
# Memory traffic (numbers moved between HBM and SRAM), one head
# ---------------------------------------------------------------------------
def io_standard(N, d):
    """Standard attention (Dao et al. 2022, Algorithm 0): read Q, K, write S; read S, write P; read P, V, write O."""
    return (2 * N * d + N * N) + (2 * N * N) + (N * N + N * d + N * d)


def flash_blocks(M, d):
    Bc = math.ceil(M / (4 * d))
    Br = min(Bc, d)
    return Br, Bc


def io_flash_formula(N, d, M):
    """Algorithm 1: K and V read once (2Nd); for each of the N/Bc outer blocks, every block of Q, O, l, m read and
    O, l, m written: (N/Bc) * N * (3d + 4) more."""
    Br, Bc = flash_blocks(M, d)
    Tc, Tr = math.ceil(N / Bc), math.ceil(N / Br)
    return 2 * N * d + Tc * Tr * (3 * Br * d + 4 * Br)


def io_flash_counted(N, d, M):
    """The loops of Algorithm 1 run with a counter instead of data."""
    Br, Bc = flash_blocks(M, d)
    n = 0
    for j in range(0, N, Bc):
        bc = min(Bc, N - j)
        n += 2 * bc * d  # load K_j, V_j
        for i in range(0, N, Br):
            br = min(Br, N - i)
            n += br * d + br * d + 2 * br  # load Q_i, O_i, l_i, m_i
            n += br * d + 2 * br  # write O_i, l_i, m_i
    return n


def occupancy(units, sms):
    """A simple model of a GPU's use: ``units`` independent blocks of work on ``sms`` multiprocessors, one each."""
    waves = math.ceil(units / sms)
    return units / (waves * sms)
