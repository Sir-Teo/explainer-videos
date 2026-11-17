"""Psyche's awareness (Part 27): masking, rivalry, ignition, integration, volition and complexity.

Small, checkable models of the questions consciousness research asks of data:

* :func:`masking`: one noisy representation of a masked target, read twice: a forced choice uses its sign, a report
  of seeing it needs its size to pass a criterion.  "Unseen" trials are then above chance with no second system,
  and how far above depends on the criterion: the criterion problem of Part 12.
* :func:`rivalry`: two populations with mutual inhibition, slow adaptation and noise, one per eye; dominance
  alternates, durations are skewed, and raising one eye's contrast shortens the other eye's dominance (Levelt).
* :func:`ignition`: a recurrent population with a sigmoid; brief inputs below a threshold fade, above it the
  network jumps to a self-sustained state: graded early activity, all-or-none late activity (Dehaene's workspace).
* :func:`phi`: integrated information in Tononi's 2004 form for small Boolean networks: effective information
  across every bipartition with maximum-entropy perturbation, the minimum information bipartition, and Φ.
* :func:`schurger`: a leaky stochastic accumulator whose threshold crossings are movements; averaged backward from
  them it rises like Libet's readiness potential (Schurger, Sitt and Dehaene 2012).
* :func:`lz76` and :func:`pci`: Lempel–Ziv complexity of a binary channels-by-time matrix, normalized as Casali
  and colleagues' perturbational complexity index, with :func:`responses` making wake-like, sleep-like and
  local-only patterns.

Nothing here imports manim.
"""

from __future__ import annotations

import itertools
import math

import numpy as np
from scipy.stats import norm

__all__ = ["masking", "visibility_curve", "rivalry", "dominance_durations", "ignition", "network", "ei",
           "bipartitions", "phi", "schurger", "back_average", "lz76", "pci", "responses"]


# ------------------------------------------------------------------------------------------------------ masking
def masking(d: float, c_seen: float) -> dict:
    """A target's direction gives evidence x ~ N(±d/2, 1).  A forced choice says the sign of x; a report says
    "seen" when |x| > c_seen.  Returns P(seen), accuracy on seen and on unseen trials, and overall accuracy."""
    mu = d / 2.0
    # P(|x| > c), and the correct-sign mass inside and outside the band, for x ~ N(mu, 1) with the target "right"
    p_seen = norm.sf(c_seen - mu) + norm.cdf(-c_seen - mu)
    right_out = norm.sf(c_seen - mu)          # x > c
    right_in = norm.cdf(c_seen - mu) - norm.cdf(-mu)   # 0 < x < c
    p_unseen = 1 - p_seen
    acc_unseen = right_in / p_unseen if p_unseen > 1e-12 else float("nan")
    acc_seen = right_out / p_seen if p_seen > 1e-12 else float("nan")
    return {"p_seen": float(p_seen), "acc_unseen": float(acc_unseen), "acc_seen": float(acc_seen),
            "acc": float(norm.cdf(mu))}


def visibility_curve(soas, d_max: float = 3.0, tau: float = 40.0, c_seen: float = 1.5) -> dict:
    """Masking across target-mask asynchronies (ms): sensitivity d(soa) = d_max (1 - exp(-soa / tau))."""
    soas = np.asarray(soas, float)
    d = d_max * (1 - np.exp(-soas / tau))
    rows = [masking(x, c_seen) for x in d]
    return {"soa": soas, "d": d, **{k: np.array([r[k] for r in rows]) for k in rows[0]}}


# ------------------------------------------------------------------------------------------------------ rivalry
def _f(x, k=0.1):
    return 1.0 / (1.0 + np.exp(-x / k))


def rivalry(T: float = 120.0, dt: float = 0.002, I=(0.6, 0.6), beta: float = 1.0, g: float = 0.25,
            tau: float = 0.02, tau_a: float = 1.0, sigma: float = 0.1, tau_n: float = 0.3, seed: int = 0) -> dict:
    """Two populations u1, u2 (one per eye) with mutual inhibition beta, adaptation a with strength g and time constant
    tau_a, and slow (Ornstein–Uhlenbeck) noise:  tau du1/dt = -u1 + f(I1 - beta u2 - g a1 + n1),
    tau_a da1/dt = -a1 + u1.  Times in seconds."""
    rng = np.random.default_rng(seed)
    n = int(T / dt)
    u = np.zeros((n, 2))
    a = np.zeros(2)
    x = np.array([0.6, 0.1])
    nz = np.zeros(2)
    I = np.asarray(I, float)
    sq = sigma * np.sqrt(2 * dt / tau_n)
    for t in range(n):
        nz += -nz * dt / tau_n + sq * rng.standard_normal(2)
        inp = I - beta * x[::-1] - g * a + nz
        x = x + dt / tau * (-x + _f(inp))
        a = a + dt / tau_a * (-a + x)
        u[t] = x
    return {"t": np.arange(n) * dt, "u": u, "dt": dt}


def dominance_durations(u: np.ndarray, dt: float, margin: float = 0.1) -> dict:
    """Durations of exclusive dominance: periods where one unit exceeds the other by ``margin``, the first and last
    (cut off by the run) dropped.  Returns durations for each eye and their pooled gamma fit (shape, scale)."""
    diff = u[:, 0] - u[:, 1]
    state = np.where(diff > margin, 1, np.where(diff < -margin, -1, 0))
    # carry the last decided state through mixed periods, and record switches
    cur, start, out = 0, 0, {1: [], -1: []}
    for k, s in enumerate(state):
        if s != 0 and s != cur:
            if cur != 0:
                out[cur].append((k - start) * dt)
            cur, start = s, k
    d1, d2 = np.array(out[1][1:]), np.array(out[-1][1:])
    allv = np.concatenate([d1, d2])
    m, v = allv.mean(), allv.var()
    return {"eye1": d1, "eye2": d2, "all": allv, "shape": float(m * m / v), "scale": float(v / m),
            "mean1": float(d1.mean()) if len(d1) else float("nan"),
            "mean2": float(d2.mean()) if len(d2) else float("nan")}


# ------------------------------------------------------------------------------------------------------ ignition
def ignition(strengths, n_trials: int = 400, T: float = 0.8, stim: float = 0.05, dt: float = 0.001,
             w: float = 6.0, theta: float = 3.0, k: float = 0.35, tau: float = 0.02, sigma: float = 0.4,
             tau_s: float = 0.03, sigma_s: float = 0.05, gain: float = 3.0, early: float = 0.06, late: float = 0.6,
             seed: int = 0) -> dict:
    """Two stages.  A sensory population follows its input linearly, tau_s ds/dt = -s + I(t) + noise, with a brief
    input I = strength for ``stim`` seconds.  A workspace population is recurrent, tau dr/dt = -r + S(w r + gain s -
    theta) + noise, S the logistic with slope 1/k; with these values it is bistable, quiet near 0 or self-sustained
    near 1.  Returns sensory activity at ``early`` seconds and workspace activity at ``late`` seconds after onset,
    for every trial and strength, the share of trials that ignite (late activity above 0.5), and mean traces."""
    rng = np.random.default_rng(seed)
    S = np.asarray(strengths, float)
    n = int(T / dt)
    ie, il = int(early / dt), int(late / dt)
    s = np.zeros((len(S), n_trials))
    r = np.zeros_like(s)
    E = np.zeros_like(s)
    L = np.zeros_like(s)
    mean_s = np.zeros((len(S), n))
    mean_r = np.zeros((len(S), n))
    for t in range(n):
        I = np.where(t * dt < stim, S, 0.0)[:, None]
        s = s + dt / tau_s * (-s + I) + sigma_s * np.sqrt(dt) * rng.standard_normal(s.shape)
        drive = w * r + gain * s - theta
        r = r + dt / tau * (-r + 1 / (1 + np.exp(-drive / k))) + sigma * np.sqrt(dt) * rng.standard_normal(r.shape)
        r = np.clip(r, 0, 1.2)
        mean_s[:, t] = s.mean(1)
        mean_r[:, t] = r.mean(1)
        if t == ie:
            E = s.copy()
        if t == il:
            L = r.copy()
    return {"strength": S, "early": E, "late": L, "p_ignite": (L > 0.5).mean(1), "t": np.arange(n) * dt,
            "mean_s": mean_s, "mean_r": mean_r}


# --------------------------------------------------------------------------------- integrated information
def network(kind: str, n: int) -> list:
    """Small Boolean networks as lists of (inputs, rule) per node: ``"ring_xor"`` (each node the XOR of its two
    neighbours), ``"ring_copy"`` (each node copies its left neighbour), ``"chain"`` (a feed-forward chain from node 0,
    which keeps its own state), ``"pairs"`` (disconnected pairs that swap), ``"all_or"`` (each node the OR of all
    others)."""
    if kind == "ring_xor":
        return [(((i - 1) % n, (i + 1) % n), "xor") for i in range(n)]
    if kind == "ring_copy":
        return [(((i - 1) % n,), "copy") for i in range(n)]
    if kind == "chain":
        return [((0,), "copy")] + [((i - 1,), "copy") for i in range(1, n)]
    if kind == "pairs":
        return [((i + 1 if i % 2 == 0 else i - 1,), "copy") for i in range(n)]
    if kind == "all_or":
        return [(tuple(j for j in range(n) if j != i), "or") for i in range(n)]
    raise ValueError(kind)


def _step_all(net) -> np.ndarray:
    """Every state (rows, as bits) of the network and its successor."""
    n = len(net)
    S = np.array(list(itertools.product((0, 1), repeat=n)), dtype=np.int8)
    nxt = np.zeros_like(S)
    for i, (inp, rule) in enumerate(net):
        X = S[:, list(inp)]
        if rule == "copy":
            nxt[:, i] = X[:, 0]
        elif rule == "xor":
            nxt[:, i] = X.sum(1) % 2
        elif rule == "or":
            nxt[:, i] = (X.sum(1) > 0)
        elif rule == "and":
            nxt[:, i] = (X.sum(1) == X.shape[1])
        else:
            raise ValueError(rule)
    return S, nxt


def _mi(a_codes: np.ndarray, b_codes: np.ndarray) -> float:
    """Mutual information (bits) between two code arrays, each row equally likely."""
    n = len(a_codes)
    joint = {}
    for x, y in zip(a_codes, b_codes):
        joint[(x, y)] = joint.get((x, y), 0) + 1
    pa, pb = {}, {}
    for (x, y), c in joint.items():
        pa[x] = pa.get(x, 0) + c
        pb[y] = pb.get(y, 0) + c
    return float(sum(c / n * math.log2(c * n / (pa[x] * pb[y])) for (x, y), c in joint.items()))


def _code(S: np.ndarray, idx) -> np.ndarray:
    idx = list(idx)
    return (S[:, idx] * (1 << np.arange(len(idx)))).sum(1) if idx else np.zeros(len(S), int)


def ei(net, A, B) -> float:
    """Effective information from part A to part B (Tononi 2004): with every element set to maximum entropy (all
    states equally likely), the mutual information between A's state now and B's state one step later."""
    S, nxt = _step_all(net)
    return _mi(_code(S, A), _code(nxt, B))


def bipartitions(n: int):
    """Every split of {0..n-1} into two non-empty parts, once each."""
    for r in range(1, n // 2 + 1):
        for A in itertools.combinations(range(n), r):
            if r == n - r and 0 not in A:
                continue
            yield A, tuple(i for i in range(n) if i not in A)


def phi(net) -> dict:
    """Φ in Tononi's 2004 form: over all bipartitions, the effective information both ways, EI(A→B) + EI(B→A);
    the minimum information bipartition minimizes it normalized by min(|A|, |B|); Φ is the unnormalized value
    there."""
    n = len(net)
    best = None
    for A, B in bipartitions(n):
        e = ei(net, A, B) + ei(net, B, A)
        score = e / min(len(A), len(B))
        if best is None or score < best[0] - 1e-12:
            best = (score, e, A, B)
    return {"phi": float(best[1]), "mib": (best[2], best[3]), "normalized": float(best[0])}


# ------------------------------------------------------------------------------------------------------ volition
def schurger(T: float = 600.0, dt: float = 0.001, I: float = 0.11, k: float = 0.5, c: float = 0.1,
             threshold: float = 0.298, seed: int = 0) -> dict:
    """Schurger, Sitt and Dehaene's (2012) leaky stochastic accumulator, dx = (I - k x) dt + c dW, with a movement
    whenever x crosses the threshold, after which x restarts at 0.  Returns the trace and the crossing times."""
    rng = np.random.default_rng(seed)
    n = int(T / dt)
    noise = c * np.sqrt(dt) * rng.standard_normal(n)
    x = np.zeros(n)
    v = 0.0
    hits = []
    for t in range(n):
        v += (I - k * v) * dt + noise[t]
        if v >= threshold:
            hits.append(t)
            v = 0.0
        x[t] = v
    return {"x": x, "hits": np.array(hits), "dt": dt, "waits": np.diff(np.r_[0, hits]) * dt}


def back_average(x: np.ndarray, hits: np.ndarray, dt: float, window: float = 3.0) -> dict:
    """The average of x over the ``window`` seconds before each crossing (crossings with a full window before them,
    and no earlier crossing inside it, as one epoch per movement), as an EEG average is time-locked to movements."""
    w = int(window / dt)
    eps = [x[h - w:h] for i, h in enumerate(hits) if h >= w and (i == 0 or hits[i - 1] < h - w)]
    E = np.array(eps)
    return {"t": (np.arange(-w, 0) + 1) * dt, "mean": E.mean(0), "n": len(E), "epochs": E}


# ------------------------------------------------------------------------------------------------- complexity
def lz76(bits) -> int:
    """The Lempel–Ziv (1976) complexity of a binary sequence: the number of distinct phrases in its exhaustive
    parsing (Kaspar and Schuster's algorithm)."""
    s = np.asarray(bits, dtype=np.int8).ravel()
    n = len(s)
    if n == 0:
        return 0
    c, l, i, k, kmax = 1, 1, 0, 1, 1
    while True:
        if s[i + k - 1] == s[l + k - 1]:
            k += 1
            if l + k > n:
                c += 1
                break
        else:
            kmax = max(k, kmax)
            i += 1
            if i == l:
                c += 1
                l += kmax
                if l + 1 > n:
                    break
                i, k, kmax = 0, 1, 1
            else:
                k = 1
    return c


def pci(M) -> float:
    """The perturbational complexity index of a binary channels-by-time matrix (Casali et al. 2013): LZ complexity of
    the matrix read column by column (time-major), normalized by L H / log2 L, with L the number of entries and H the
    binary entropy of the share of ones."""
    M = np.asarray(M, dtype=np.int8)
    L = M.size
    p = M.mean()
    if p in (0.0, 1.0):
        return 0.0
    H = -(p * math.log2(p) + (1 - p) * math.log2(1 - p))
    return float(lz76(M.T.ravel()) * math.log2(L) / (L * H))


def responses(kind: str, channels: int = 30, steps: int = 300, seed: int = 0) -> np.ndarray:
    """Illustrative binary responses to a pulse (channels by time steps).  ``"wake"``: the response spreads across
    the channels with each channel following its own, varied course (integrated and differentiated); ``"sleep"``: a
    large, stereotyped wave in which every channel does the same (integrated, not differentiated); ``"local"``: a
    brief response confined to a few channels (neither); ``"noise"``: independent random activity everywhere
    (differentiated, not integrated, and not a response)."""
    rng = np.random.default_rng(seed)
    M = np.zeros((channels, steps), dtype=np.int8)
    t = np.arange(steps)
    if kind == "sleep":
        wave = (np.sin(2 * np.pi * t / 90.0) > 0.3) & (t < 200)
        M[:] = wave
        flip = rng.random(M.shape) < 0.01
        M ^= flip.astype(np.int8)
    elif kind == "local":
        M[:4, 5:30] = 1
    elif kind == "wake":
        onset = np.sort(rng.integers(5, 120, channels))
        for ch in range(channels):
            period = rng.uniform(8, 40)
            phase = rng.uniform(0, 2 * np.pi)
            dur = rng.integers(80, 200)
            seg = slice(onset[ch], min(steps, onset[ch] + dur))
            tt = t[seg]
            M[ch, seg] = (np.sin(2 * np.pi * tt / period + phase) > rng.uniform(-0.3, 0.5))
        M ^= (rng.random(M.shape) < 0.02).astype(np.int8)
    elif kind == "noise":
        M[:] = rng.random(M.shape) < 0.3
    else:
        raise ValueError(kind)
    return M
