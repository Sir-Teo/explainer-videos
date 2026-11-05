"""The limit order book (Part 36): what the best quotes and their queues say about the next price.

Measurement on a regular grid of best bid and offer: order-flow imbalance (Cont, Kukanov and Stoikov 2014), queue
imbalance, the microprice (Stoikov 2018) estimated as a Markov chain on (imbalance, spread), trade-sign memory (Lillo
and Farmer 2004) and the signature plot. Simulation: a queue-reactive model of the best queues (after Huang, Lehalle and
Rosenbaum 2015), the House's order-book simulator."""

from __future__ import annotations

import math

import numpy as np


# ---------------------------------------------------------------------------
# Features on the grid
# ---------------------------------------------------------------------------
def mid(b) -> np.ndarray:
    return (np.asarray(b["bid"], float) + np.asarray(b["ask"], float)) / 2


def imbalance(b) -> np.ndarray:
    """Queue imbalance I = Q_bid / (Q_bid + Q_ask), in [0, 1]."""
    qb, qa = np.asarray(b["bq"], float), np.asarray(b["aq"], float)
    return qb / np.maximum(qb + qa, 1e-12)


def weighted_mid(b) -> np.ndarray:
    """The size-weighted mid: bid I' + ask I with I the bid imbalance (more bids pull the estimate toward the ask)."""
    i = imbalance(b)
    return np.asarray(b["bid"], float) * (1 - i) + np.asarray(b["ask"], float) * i


def ofi(b) -> np.ndarray:
    """Cont-Kukanov-Stoikov order-flow imbalance at the best quotes, per grid step: the bid side's contribution
    (size added at a higher or equal bid, removed at a lower or equal one) less the ask side's."""
    pb, qb, pa, qa = (np.asarray(b[k], float) for k in ("bid", "bq", "ask", "aq"))
    e = np.zeros(len(pb))
    e[1:] = (np.where(pb[1:] >= pb[:-1], qb[1:], 0.0) - np.where(pb[1:] <= pb[:-1], qb[:-1], 0.0)
             - np.where(pa[1:] <= pa[:-1], qa[1:], 0.0) + np.where(pa[1:] >= pa[:-1], qa[:-1], 0.0))
    return e


def aggregate(x, n: int, how: str = "sum") -> np.ndarray:
    m = len(x) // n * n
    y = np.asarray(x[:m], float).reshape(-1, n)
    return y.sum(1) if how == "sum" else y[:, -1]


# ---------------------------------------------------------------------------
# The microprice (Stoikov 2018)
# ---------------------------------------------------------------------------
def microprice_fit(b, n_imb: int = 10, max_spread: int = 2, tick: float = 0.1, symmetric: bool = True) -> dict:
    """Estimate Stoikov's microprice adjustment g(I, S) from a grid of best quotes.

    States x = (imbalance bucket, spread in ticks); between grid steps the state either stays with the mid unchanged
    (transition matrix Q), moves without a mid change, or the mid moves by dM (R the transitions on a mid move, with
    the move recorded). Then G1 = (I - Q)^{-1} R dM is the expected next mid change, B = (I - Q)^{-1} T the state after
    it, and g = sum_k B^k G1 = (I - B)^{-1} G1 once the mean drift is removed. With ``symmetric`` the data are
    augmented by their mirror image (bid and ask swapped, price negated), which makes g antisymmetric and removes drift.
    Returns the buckets, g for each state (in price units) and the state counts."""
    pb, pa = np.asarray(b["bid"], float), np.asarray(b["ask"], float)
    I = imbalance(b)
    M = (pb + pa) / 2
    S = np.rint((pa - pb) / tick).astype(int)
    ok = (S >= 1) & (S <= max_spread)
    ib = np.minimum((I * n_imb).astype(int), n_imb - 1)
    st = (S - 1) * n_imb + ib
    K = n_imb * max_spread
    dM = np.r_[np.diff(M), 0.0]
    nxt = np.r_[st[1:], st[-1]]
    v = ok & np.r_[ok[1:], False]
    moves = np.unique(np.round(dM[v & (dM != 0)] / (tick / 2)).astype(int))
    moves = moves[np.abs(moves) <= 4]
    if symmetric:
        st_all = np.r_[st[v], (S[v] - 1) * n_imb + (n_imb - 1 - ib[v])]
        nx_all = np.r_[nxt[v], ((np.r_[S[1:], S[-1]][v]) - 1) * n_imb + (n_imb - 1 - np.r_[ib[1:], ib[-1]][v])]
        dm_all = np.r_[dM[v], -dM[v]]
    else:
        st_all, nx_all, dm_all = st[v], nxt[v], dM[v]
    k_ = np.round(dm_all / (tick / 2)).astype(int)
    Q = np.zeros((K, K))
    T = np.zeros((K, K))
    R1 = np.zeros(K)
    cnt = np.bincount(st_all, minlength=K).astype(float)
    still = k_ == 0
    np.add.at(Q, (st_all[still], nx_all[still]), 1.0)
    mv = (~still) & (np.abs(k_) <= 4)
    np.add.at(T, (st_all[mv], nx_all[mv]), 1.0)
    np.add.at(R1, st_all[mv], dm_all[mv])
    c = np.maximum(cnt, 1.0)
    Q, T, R1 = Q / c[:, None], T / c[:, None], R1 / c
    A = np.linalg.inv(np.eye(K) - Q)
    G1 = A @ R1
    B = A @ T
    # g = sum_k B^k G1: B is a stochastic matrix, but the symmetrised G1 has no component on its unit eigenvector,
    # so the series converges; it is summed to 400 terms and the change over the last 200 reported
    gk = G1.copy()
    acc = G1.copy()
    for k in range(400):
        gk = B @ gk
        acc = acc + gk
        if k == 199:
            half = acc.copy()
    return {"n_imb": n_imb, "max_spread": max_spread, "tick": tick, "g1": G1, "g": acc, "count": cnt,
            "centers": (np.arange(n_imb) + 0.5) / n_imb, "converged": float(np.max(np.abs(acc - half)))}


def microprice_apply(b, fit) -> np.ndarray:
    """The microprice M + g(I, S) on a grid, NaN where the spread is outside the fitted range."""
    pb, pa = np.asarray(b["bid"], float), np.asarray(b["ask"], float)
    I = imbalance(b)
    S = np.rint((pa - pb) / fit["tick"]).astype(int)
    ib = np.minimum((I * fit["n_imb"]).astype(int), fit["n_imb"] - 1)
    st = (S - 1) * fit["n_imb"] + ib
    ok = (S >= 1) & (S <= fit["max_spread"])
    out = np.full(len(pb), np.nan)
    out[ok] = (pb[ok] + pa[ok]) / 2 + fit["g"][st[ok]]
    return out


def forecast_mse(b, est, horizon: int) -> float:
    """Mean squared error of an estimate of the mid ``horizon`` grid steps ahead."""
    m = mid(b)
    e = np.asarray(est, float)[:-horizon] - m[horizon:]
    e = e[np.isfinite(e)]
    return float(np.mean(e * e))


# ---------------------------------------------------------------------------
# Memory and scale
# ---------------------------------------------------------------------------
def sign_acf(sign, lags) -> np.ndarray:
    s = np.asarray(sign, float)
    s = s - s.mean()
    v = float(np.dot(s, s))
    return np.array([float(np.dot(s[L:], s[:-L]) / v) for L in lags])


def signature(m, steps) -> np.ndarray:
    """The signature plot: realised variance per unit time of the mid sampled every k steps, for each k."""
    m = np.asarray(m, float)
    out = []
    for k in steps:
        d = np.diff(m[::k])
        out.append(float(np.mean(d * d) / k))
    return np.array(out)


# ---------------------------------------------------------------------------
# A queue-reactive simulator of the best queues
# ---------------------------------------------------------------------------
def qr_fit(b, unit: float, n_q: int = 20) -> dict:
    """Estimate a queue-reactive model of the best bid and ask queues, in units of ``unit`` (a typical order size):
    for each queue size q (capped at n_q), the per-step probability that the queue grows by one unit, shrinks by one,
    and, at q = 0 after a depletion, the distribution of the new queue. Both sides are pooled (symmetry)."""
    pb, pa = np.asarray(b["bid"], float), np.asarray(b["ask"], float)
    qs = [np.asarray(b["bq"], float), np.asarray(b["aq"], float)]
    up = np.zeros(n_q + 1)
    dn = np.zeros(n_q + 1)
    cnt = np.zeros(n_q + 1)
    refill = []
    mids = (pb + pa) / 2
    moved = np.r_[np.diff(mids) != 0, False]
    for q in qs:
        qq = np.minimum(np.rint(q / unit).astype(int), n_q)
        d = np.r_[np.diff(qq), 0]
        np.add.at(cnt, qq, 1.0)
        np.add.at(up, qq[(d > 0) & ~moved], 1.0)
        np.add.at(dn, qq[(d < 0) & ~moved], 1.0)
        refill += list(np.minimum(np.rint(q[1:][moved[:-1]] / unit).astype(int), n_q))
    c = np.maximum(cnt, 1)
    rf = np.bincount(np.maximum(np.asarray(refill, int), 1), minlength=n_q + 1)[1:].astype(float)
    return {"p_up": up / c, "p_dn": dn / c, "refill": rf / rf.sum(), "unit": unit, "n_q": n_q,
            "occupancy": cnt / cnt.sum()}


def qr_simulate(fit, n: int, seed: int = 0) -> dict:
    """Simulate the two best queues: each step each queue grows or shrinks by one unit with the fitted state-dependent
    probabilities; when one is emptied the mid moves half a tick that way (the other side becomes the new best and the
    emptied side is refilled from the fitted distribution). Returns queues and the mid in ticks."""
    rng = np.random.default_rng(seed)
    nq = fit["n_q"]
    pu, pd, rf = fit["p_up"], fit["p_dn"], fit["refill"]
    qb = int(rng.choice(np.arange(1, nq + 1), p=rf))
    qa = int(rng.choice(np.arange(1, nq + 1), p=rf))
    m = 0.0
    QB, QA, Mm = np.zeros(n), np.zeros(n), np.zeros(n)
    for t in range(n):
        for side in (0, 1):
            q = qb if side == 0 else qa
            r = rng.random()
            if r < pu[min(q, nq)]:
                q += 1
            elif r < pu[min(q, nq)] + pd[min(q, nq)]:
                q -= 1
            if q <= 0:
                m += -1.0 if side == 0 else 1.0           # the bid emptied: price ticks down; the ask: up
                q = int(rng.choice(np.arange(1, nq + 1), p=rf))
                other = int(rng.choice(np.arange(1, nq + 1), p=rf))
                if side == 0:
                    qb, qa = q, other
                else:
                    qa, qb = q, other
                break
            if side == 0:
                qb = q
            else:
                qa = q
        QB[t], QA[t], Mm[t] = qb, qa, m
    return {"bq": QB, "aq": QA, "mid": Mm}
