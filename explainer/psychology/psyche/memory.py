"""Psyche stores, finds, forgets and invents (Parts 20 and 21 of *Psychology, Built*).

Forgetting curves: Ebbinghaus's own formula against a power law and an exponential, fitted to his savings.  Free
recall: the serial-position curve, the probability of first recall and the lag-conditional response probability
(lag-CRP), computed from recall sequences with each transition conditioned on the items still available.  Two models
of search: SAM (Raaijmakers and Shiffrin 1981), in which a rehearsal buffer builds context and inter-item strengths
that guide sampling and recovery, and the context maintenance and retrieval model, CMR (Howard and Kahana 2002;
Polyn, Norman and Kahana 2009, without semantic or source features), in which a slowly drifting context is bound to
each item, retrieval of an item reinstates its context, and recency and contiguity both follow.  CMR's likelihood is
computed exactly along each observed recall sequence (:func:`cmr_loglik`) and maximised (:func:`fit_cmr_ml`); a
distractor task is a drift toward context that belongs to no item; recall stops by a hazard that grows with output
position and by a fixed-strength competitor that wins as the support of the remaining items fades.  Attractors: a Hopfield network storing patterns by Hebb's rule and recalling by
settling, with its capacity near 0.14 patterns per unit.  ACT-R's base-level activation, its power-law forgetting and
its retrieval probability.  Recognition: the dual-process (Yonelinas) and unequal-variance signal-detection ROCs.  The
hippocampus: pattern separation by expansion and sparse coding.

Part 21 (forgetting and inventing): four forgetting laws fitted with AIC, Jost's law, and the averaging artefact (a
gamma mixture of exponentials is a power function); A-B, A-C interference in a linear associator; a two-store model of
systems consolidation and Ribot's gradient; complementary learning systems in Rumelhart's semantic network (the
penguin, learnt focused or interleaved); Pavlik and Anderson's spacing model and Cepeda's ridgeline; the bifurcation
model of the testing effect, fitted; Huttenlocher's category adjustment model; the DRM illusion by global matching;
line-ups by signal detection and the confidence-accuracy characteristic; half-life regression (Settles and Meeder).

Parameters make the classic patterns legible; they are not fitted to a laboratory unless a function says so, and
the scenes say which numbers are published, which are fitted to open data, and which are Psyche's.
"""

from __future__ import annotations

import numpy as np
from scipy.optimize import minimize
from scipy.stats import norm


# ============================================================================================== forgetting curves
def ebbinghaus_formula(t_minutes, k: float = 1.84, c: float = 1.25):
    """Ebbinghaus's fitted law of savings (percent) against time in minutes: b = 100 k / ((log10 t)^c + k)."""
    t = np.asarray(t_minutes, float)
    return 100 * k / (np.log10(t) ** c + k)


def fit_forgetting(t_minutes, savings) -> dict:
    """Least-squares fits of three forgetting laws to savings (percent) at times in minutes: Ebbinghaus's formula,
    a power law a t^-b, and an exponential a e^(-t/tau).  Returns each law's parameters and residual sum of squares."""
    t, y = np.asarray(t_minutes, float), np.asarray(savings, float)
    out = {}

    def fit(f, x0):
        r = minimize(lambda p: np.sum((f(t, *p) - y) ** 2), np.asarray(x0, float), method="Nelder-Mead",
                     options={"xatol": 1e-8, "fatol": 1e-10, "maxiter": 20000})
        return r.x, float(r.fun)

    p, s = fit(lambda t_, k, c: ebbinghaus_formula(t_, abs(k), abs(c)), (1.8, 1.2))
    out["ebbinghaus"] = {"params": np.abs(p), "sse": s}
    p, s = fit(lambda t_, a, b: a * t_ ** (-abs(b)), (60, 0.1))
    out["power"] = {"params": np.array([p[0], abs(p[1])]), "sse": s}
    p, s = fit(lambda t_, a, tau: a * np.exp(-t_ / abs(tau)), (50, 1000))
    out["exponential"] = {"params": np.array([p[0], abs(p[1])]), "sse": s}
    return out


# ============================================================================================== free recall analysis
def spc(recalls, n: int) -> np.ndarray:
    """Serial-position curve: the probability that the item at each position (1..n) is recalled.

    ``recalls`` is (lists, outputs) of serial positions 1..n, with 0 for no recall or an intrusion (repeats are
    ignored after their first occurrence)."""
    R = np.asarray(recalls)
    hit = np.zeros((len(R), n), bool)
    for i, row in enumerate(R):
        for p in row:
            if 1 <= p <= n:
                hit[i, p - 1] = True
    return hit.mean(0)


def pfr(recalls, n: int) -> np.ndarray:
    """Probability of first recall at each serial position."""
    R = np.asarray(recalls)
    first = np.array([next((p for p in row if 1 <= p <= n), 0) for row in R])
    return np.array([(first == k).mean() for k in range(1, n + 1)])


def lag_crp(recalls, n: int, max_lag: int | None = None) -> tuple[np.ndarray, np.ndarray]:
    """The lag-conditional response probability (Kahana 1996).

    For each transition between two correct, new recalls, count the actual lag, and count every lag that was
    possible: to an item not yet recalled.  CRP(lag) = actual / possible.  Returns (lags, crp) for lags -max_lag..max_lag
    (lag 0 is NaN)."""
    max_lag = max_lag or n - 1
    actual = np.zeros(2 * n - 1)
    possible = np.zeros(2 * n - 1)
    for row in np.asarray(recalls):
        seen = set()
        prev = None
        for p in row:
            if not (1 <= p <= n) or p in seen:
                prev = None if not (1 <= p <= n) else prev
                continue
            if prev is not None:
                avail = [q for q in range(1, n + 1) if q not in seen]
                for q in avail:
                    possible[q - prev + n - 1] += 1
                actual[p - prev + n - 1] += 1
            seen.add(p)
            prev = p
    with np.errstate(invalid="ignore", divide="ignore"):
        crp = actual / possible
    lags = np.arange(-(n - 1), n)
    crp[n - 1] = np.nan
    keep = np.abs(lags) <= max_lag
    return lags[keep], crp[keep]


# ============================================================================================== CMR
CMR_DEFAULT = {"B_enc": 0.7, "B_rec": 0.5, "B_start": 0.3, "gamma_fc": 0.6, "phi_s": 2.0, "phi_d": 0.8,
               "alpha": 0.01, "tau": 0.3, "stop_s": 0.02, "stop_r": 0.25, "kappa": 0.0}


def _p_stop(p: dict, j: int, support: float) -> float:
    """The probability of ending recall after ``j`` recalls: a hazard that grows with output position, combined
    with a fixed-strength competitor ``kappa`` that wins when the words left have little support (so a recall
    that has drifted away from the list stops sooner)."""
    go = (1.0 - min(1.0 - 1e-9, p["stop_s"] * np.exp(p["stop_r"] * j)))
    if p.get("kappa", 0.0) > 0:
        go *= support / (support + p["kappa"])
    return float(min(1.0 - 1e-9, max(1e-12, 1.0 - go)))


def _drift(c, c_in, beta):
    """Move context ``c`` toward ``c_in`` (both unit length) so that it stays unit length (Howard and Kahana)."""
    nin = np.linalg.norm(c_in)
    if nin == 0:
        return c
    c_in = c_in / nin
    d = float(c @ c_in)
    rho = np.sqrt(1 + beta ** 2 * (d ** 2 - 1)) - beta * d
    return rho * c + beta * c_in


def cmr_simulate(n_items: int = 16, n_lists: int = 500, params: dict | None = None, rng=None,
                 max_out: int | None = None, end_distractor: float = 0.0, between: float = 0.0) -> np.ndarray:
    """Free recall by the context maintenance and retrieval model, without source features.

    Each item has its own feature vector; context is a unit vector over the items plus a start element.  At study,
    the item's pre-experimental context (scaled by ``1 - gamma_fc``) drives context with rate ``B_enc``; the
    item-to-context associations learn the previous context with rate ``gamma_fc``, and the context-to-item
    associations learn the current context with a primacy gain ``phi_s exp(-phi_d (i - 1)) + 1``.  At test, context
    moves toward the start of the list with rate ``B_start``; items compete by a Luce rule on their activations raised
    to ``1 / tau``; each recall reinstates the recalled item's context with rate ``B_rec``; recall stops with
    probability ``stop_s exp(stop_r j)`` after j outputs.  A distractor task is a drift toward fresh, random context:
``between`` after every item (the continual-distractor design) and ``end_distractor`` after the last one (a delay
filled with counting).  Returns (lists, outputs) of serial positions, 0-padded."""
    p = {**CMR_DEFAULT, **(params or {})}
    rng = rng or np.random.default_rng(0)
    n = n_items
    max_out = max_out or n
    out = np.zeros((n_lists, max_out), int)
    n_dist = n + 1  # distractor dimensions, one per gap
    dim = n + 1 + n_dist
    for L in range(n_lists):
        M_fc = (1 - p["gamma_fc"]) * np.eye(dim)[:, :n]  # columns: item -> context
        M_cf = p["alpha"] * np.ones((n, dim))  # rows: context -> item, a small uniform baseline
        c = np.zeros(dim)
        c[n] = 1.0  # the start-of-list element
        for i in range(n):
            c_old = c.copy()
            c = _drift(c, M_fc[:, i], p["B_enc"])
            M_fc[:, i] += p["gamma_fc"] * c_old
            phi = p["phi_s"] * np.exp(-p["phi_d"] * i) + 1.0
            M_cf[i] += phi * c
            if between > 0:
                d = np.zeros(dim)
                d[n + 1 + i] = 1.0
                c = _drift(c, d, between)
        if end_distractor > 0:
            d = np.zeros(dim)
            d[n + 1 + n] = 1.0
            c = _drift(c, d, end_distractor)
        start = np.zeros(dim)
        start[n] = 1.0
        c = _drift(c, start, p["B_start"])
        recalled = np.zeros(n, bool)
        for j in range(max_out):
            a = np.maximum(M_cf @ c, 1e-12)
            a[recalled] = 0.0
            if not a.any():
                break
            w = a ** (1.0 / p["tau"])
            if rng.random() < _p_stop(p, j, float(w.sum())):
                break
            w = w / w.sum()
            k = int(rng.choice(n, p=w))
            recalled[k] = True
            out[L, j] = k + 1
            c = _drift(c, M_fc[:, k], p["B_rec"])
    return out


def _cmr_study(n: int, p: dict):
    """Run CMR's study phase on a list of ``n`` items; return the associations and the context at test."""
    dim = n + 1
    M_fc = (1 - p["gamma_fc"]) * np.eye(dim)[:, :n]
    M_cf = p["alpha"] * np.ones((n, dim))
    c = np.zeros(dim)
    c[n] = 1.0
    for i in range(n):
        c_old = c.copy()
        c = _drift(c, M_fc[:, i], p["B_enc"])
        M_fc[:, i] += p["gamma_fc"] * c_old
        M_cf[i] += (p["phi_s"] * np.exp(-p["phi_d"] * i) + 1.0) * c
    start = np.zeros(dim)
    start[n] = 1.0
    return M_fc, M_cf, _drift(c, start, p["B_start"])


def cmr_loglik(params: dict, recalls, n: int, parts: bool = False):
    """The log-likelihood of observed recall sequences under CMR (every list studied in order, positions 1..n).

    The model is run along each observed sequence: each recall's probability is (1 - P(stop)) times its Luce share
    among the items not yet recalled, and the sequence ends with P(stop).  Intrusions and repeats are left out of
    the sequence (the model makes neither), which is the usual simplification; ending the sequence at one instead
    would teach the model that people stop sooner than they do."""
    p = {**CMR_DEFAULT, **params}
    M_fc0, M_cf, c0 = _cmr_study(n, p)  # every list has the same structure: study once
    total = 0.0
    choice, events = 0.0, 0
    for row in np.asarray(recalls):
        c = c0.copy()
        recalled = np.zeros(n, bool)
        j = 0
        for pos in row:
            if not (1 <= pos <= n) or recalled[pos - 1]:
                continue
            a = np.maximum(M_cf @ c, 1e-12)
            a[recalled] = 0.0
            w = a ** (1.0 / p["tau"])
            stop = _p_stop(p, j, float(w.sum()))
            lc = np.log(w[pos - 1] / w.sum())
            total += np.log(1 - stop) + lc
            choice += lc
            events += 1
            recalled[pos - 1] = True
            c = _drift(c, M_fc0[:, pos - 1], p["B_rec"])
            j += 1
        if j < n:
            a = np.maximum(M_cf @ c, 1e-12)
            a[recalled] = 0.0
            total += np.log(_p_stop(p, j, float((a ** (1.0 / p["tau"])).sum())))
    if parts:
        return {"total": float(total), "choice": float(choice), "recalls": events}
    return float(total)


def position_choice_loglik(weights, recalls, n: int) -> dict:
    """A baseline for the choice of each recall: pick among the words not yet recalled in proportion to a fixed
    weight per serial position (say, the serial-position curve), ignoring what was just recalled.  Returns the
    summed log probability of the observed choices and their number (intrusions and repeats skipped, as in
    :func:`cmr_loglik`)."""
    w0 = np.asarray(weights, float)
    total, events = 0.0, 0
    for row in np.asarray(recalls):
        recalled = np.zeros(n, bool)
        for pos in row:
            if not (1 <= pos <= n) or recalled[pos - 1]:
                continue
            w = np.where(recalled, 0.0, w0)
            total += np.log(w[pos - 1] / w.sum())
            events += 1
            recalled[pos - 1] = True
    return {"choice": float(total), "recalls": events}


def fit_cmr_ml(recalls, n: int, free=("B_enc", "B_rec", "B_start", "gamma_fc", "phi_s", "phi_d", "tau", "stop_s",
                                      "stop_r"), x0: dict | None = None, maxiter: int = 2000) -> dict:
    """Maximum-likelihood fit of CMR to recall sequences, with parameters kept in range by a logistic transform."""
    keys = list(free)
    lo = {"B_enc": 0.01, "B_rec": 0.01, "B_start": 0.0, "gamma_fc": 0.0, "phi_s": 0.0, "phi_d": 0.0, "alpha": 0.0,
          "tau": 0.05, "stop_s": 0.0005, "stop_r": 0.0, "kappa": 0.0}
    hi = {"B_enc": 0.99, "B_rec": 0.99, "B_start": 0.99, "gamma_fc": 0.99, "phi_s": 20.0, "phi_d": 5.0, "alpha": 0.5,
          "tau": 3.0, "stop_s": 0.5, "stop_r": 1.5, "kappa": 5.0}
    start = {**CMR_DEFAULT, **(x0 or {})}

    def to_x(v, k):
        u = (v - lo[k]) / (hi[k] - lo[k])
        u = min(max(u, 1e-4), 1 - 1e-4)
        return np.log(u / (1 - u))

    def unpack(x):
        return {k: lo[k] + (hi[k] - lo[k]) / (1 + np.exp(-v)) for k, v in zip(keys, x)}

    r = minimize(lambda x: -cmr_loglik(unpack(x), recalls, n), np.array([to_x(start[k], k) for k in keys]),
                 method="Nelder-Mead", options={"maxiter": maxiter, "xatol": 1e-4, "fatol": 1e-3, "adaptive": True})
    p = {**CMR_DEFAULT, **unpack(r.x)}
    return {"params": p, "loglik": -float(r.fun), "k": len(keys), "evals": int(r.nfev), "converged": bool(r.success)}


def recall_summary(recalls, n: int, max_lag: int = 5) -> dict:
    """The three curves models are fitted to: serial position, first recall and lag-CRP (lags 1..max_lag each way)."""
    lags, crp = lag_crp(recalls, n, max_lag)
    return {"spc": spc(recalls, n), "pfr": pfr(recalls, n), "lags": lags, "crp": crp}


def fit_cmr(target: dict, n: int, free=("B_enc", "B_rec", "B_start", "phi_s", "tau", "stop_s"), n_lists: int = 400,
            seed: int = 0, maxiter: int = 300) -> dict:
    """Fit CMR's ``free`` parameters to a recall summary by least squares over the three curves.

    Each evaluation simulates ``n_lists`` lists with the same random numbers (common random numbers), so the
    objective is smooth enough for Nelder-Mead.  Returns the parameters, the loss and the fitted summary."""
    keys = list(free)
    lo = {"B_enc": 0.05, "B_rec": 0.05, "B_start": 0.0, "gamma_fc": 0.0, "phi_s": 0.0, "phi_d": 0.0, "alpha": 0.0,
          "tau": 0.05, "stop_s": 0.001, "stop_r": 0.0}
    hi = {"B_enc": 0.99, "B_rec": 0.99, "B_start": 0.99, "gamma_fc": 0.99, "phi_s": 10.0, "phi_d": 5.0, "alpha": 0.5,
          "tau": 2.0, "stop_s": 0.5, "stop_r": 1.0}

    def unpack(x):
        return {k: float(np.clip(v, lo[k], hi[k])) for k, v in zip(keys, x)}

    def loss(x):
        p = unpack(x)
        s = recall_summary(cmr_simulate(n, n_lists, p, np.random.default_rng(seed)), n)
        m = np.isfinite(target["crp"]) & np.isfinite(s["crp"])
        return float(np.sum((s["spc"] - target["spc"]) ** 2) + np.sum((s["pfr"] - target["pfr"]) ** 2)
                     + np.sum((s["crp"][m] - target["crp"][m]) ** 2))

    x0 = np.array([CMR_DEFAULT[k] for k in keys])
    r = minimize(loss, x0, method="Nelder-Mead", options={"maxiter": maxiter, "xatol": 1e-3, "fatol": 1e-5})
    p = {**CMR_DEFAULT, **unpack(r.x)}
    return {"params": p, "loss": float(r.fun),
            "summary": recall_summary(cmr_simulate(n, 2000, p, np.random.default_rng(seed + 1)), n)}


# ============================================================================================== SAM
def sam_simulate(n_items: int = 16, n_lists: int = 500, r: int = 4, a: float = 0.1, b: float = 0.1, c: float = 0.1,
                 k_max: int = 8, rng=None) -> np.ndarray:
    """Free recall by the search of associative memory (SAM), with a rehearsal buffer of ``r`` items.

    Each study step strengthens every buffered item's link to the list context by ``a`` and every buffered pair's
    mutual link by ``b`` (and each item to itself by ``c``); when the buffer is full a random item leaves.  At test the
    buffer is output first, in random order; then items are sampled with probability proportional to their context
    strength (times the last recalled item's strength to them, when there is one), recovered with probability
    ``1 - exp(-strength)``, and search stops after ``k_max`` failures."""
    rng = rng or np.random.default_rng(0)
    n = n_items
    out = np.zeros((n_lists, n), int)
    for L in range(n_lists):
        ctx = np.zeros(n)
        S = np.zeros((n, n))
        buf: list[int] = []
        for i in range(n):
            if len(buf) == r:
                buf.pop(int(rng.integers(r)))
            buf.append(i)
            for x in buf:
                ctx[x] += a
                S[x, x] += c
                for y in buf:
                    if x != y:
                        S[x, y] += b
        order = list(rng.permutation(buf))
        recalled = set(order)
        j = 0
        for x in order:
            out[L, j] = x + 1
            j += 1
        last = order[-1] if order else None
        fails = 0
        while fails < k_max and j < n:
            w = ctx * (S[last] + 1e-9 if last is not None else 1.0)
            w = w.copy()
            w[list(recalled)] = 0.0
            if w.sum() <= 0:
                break
            k = int(rng.choice(n, p=w / w.sum()))
            strength = ctx[k] + (S[last, k] if last is not None else 0.0)
            if rng.random() < 1 - np.exp(-strength):
                recalled.add(k)
                out[L, j] = k + 1
                j += 1
                last = k
            else:
                fails += 1
    return out


# ============================================================================================== Hopfield
def hopfield_capacity(n_units: int = 200, loads=None, trials: int = 20, flip: float = 0.1, steps: int = 20,
                      rng=None) -> dict:
    """Recall in a Hopfield network against load P/N.

    P random +-1 patterns are stored by Hebb's rule, W = (1/N) sum xi xi^T with a zero diagonal.  Each stored pattern
    is cued with a fraction ``flip`` of its units flipped and the network settles by synchronous sign updates for
    ``steps`` steps (asynchronous sweeps would be slower and similar).  Returns the loads, the mean final overlap
    m = (1/N) xi . s, and the share of patterns recalled almost perfectly (m > 0.95)."""
    rng = rng or np.random.default_rng(0)
    loads = np.asarray(loads if loads is not None else np.linspace(0.02, 0.3, 15), float)
    N = n_units
    m_mean, ok = [], []
    for a in loads:
        P = max(1, int(round(a * N)))
        ms = []
        for _ in range(trials):
            xi = rng.choice([-1.0, 1.0], size=(P, N))
            W = xi.T @ xi / N
            np.fill_diagonal(W, 0.0)
            k = int(rng.integers(P))
            s = xi[k].copy()
            s[rng.random(N) < flip] *= -1
            for _ in range(steps):
                s_new = np.where(W @ s >= 0, 1.0, -1.0)
                if np.array_equal(s_new, s):
                    break
                s = s_new
            ms.append(float(xi[k] @ s / N))
        ms = np.array(ms)
        m_mean.append(ms.mean())
        ok.append((ms > 0.95).mean())
    return {"loads": loads, "overlap": np.array(m_mean), "recalled": np.array(ok)}


# ============================================================================================== ACT-R
def actr_activation(practice_times, now, d: float = 0.5) -> float:
    """ACT-R's base-level activation: B = ln sum_j (now - t_j)^(-d), over past uses at ``practice_times``."""
    t = now - np.asarray(practice_times, float)
    t = t[t > 0]
    return float(np.log(np.sum(t ** (-d)))) if len(t) else -np.inf


def actr_recall(activation, threshold: float = -0.5, s: float = 0.4):
    """The probability of retrieval: a logistic in activation around the threshold, with noise scale ``s``."""
    return 1.0 / (1.0 + np.exp(-(np.asarray(activation, float) - threshold) / s))


# ============================================================================================== recognition
def dual_process_roc(R: float = 0.3, d: float = 1.0, criteria=None) -> tuple[np.ndarray, np.ndarray]:
    """Yonelinas's dual-process ROC: recollection with probability ``R`` (an all-or-none hit), else familiarity, an
    equal-variance signal-detection process with sensitivity ``d``.  Returns (false alarms, hits)."""
    c = np.asarray(criteria if criteria is not None else np.linspace(-2.5, 3.0, 60), float)
    F = norm.sf(c)
    H = R + (1 - R) * norm.sf(c - d)
    return F, H


def uvsd_roc(d: float = 1.2, s_old: float = 1.25, criteria=None) -> tuple[np.ndarray, np.ndarray]:
    """The unequal-variance signal-detection ROC: old items N(d, s_old), new items N(0, 1)."""
    c = np.asarray(criteria if criteria is not None else np.linspace(-2.5, 3.5, 60), float)
    return norm.sf(c), norm.sf((c - d) / s_old)


# ============================================================================================== the hippocampus
def pattern_separation(input_overlaps, n_in: int = 200, n_out: int = 2000, active_in: float = 0.2,
                       active_out: float = 0.02, fan_in: int = 20, pairs: int = 40, rng=None) -> np.ndarray:
    """Output overlap against input overlap for an expansion to a sparse layer (a cartoon of the dentate gyrus).

    Binary input patterns with a fraction ``active_in`` of units on; pairs share a set fraction of their active
    units.  Each of ``n_out`` units sums ``fan_in`` random inputs, and only the top ``active_out`` fraction fire
    (k-winners-take-all).  Overlap is the share of active units two patterns have in common."""
    rng = rng or np.random.default_rng(0)
    W = np.zeros((n_out, n_in))
    for i in range(n_out):
        W[i, rng.choice(n_in, fan_in, replace=False)] = 1.0
    k_in, k_out = int(active_in * n_in), max(1, int(active_out * n_out))
    tie = 1e-6 * rng.standard_normal(n_out)  # a fixed tie-break, so identical inputs give identical codes

    def code(x):
        h = W @ x + tie
        y = np.zeros(n_out)
        y[np.argsort(h)[-k_out:]] = 1.0
        return y

    out = []
    for ov in np.asarray(input_overlaps, float):
        vals = []
        for _ in range(pairs):
            a_idx = rng.choice(n_in, k_in, replace=False)
            keep = int(round(ov * k_in))
            rest = np.setdiff1d(np.arange(n_in), a_idx)
            b_idx = np.r_[rng.choice(a_idx, keep, replace=False), rng.choice(rest, k_in - keep, replace=False)]
            a, b = np.zeros(n_in), np.zeros(n_in)
            a[a_idx], b[b_idx] = 1, 1
            ya, yb = code(a), code(b)
            vals.append((ya * yb).sum() / k_out)
        out.append(np.mean(vals))
    return np.array(out)


# ============================================================================================== forgetting laws
LAWS = {
    "power": (lambda t, a, b: a * t ** (-b), (0.6, 0.15)),
    "exponential": (lambda t, a, tau: a * np.exp(-t / tau), (0.5, 2000.0)),
    "log": (lambda t, a, b: a - b * np.log(t), (0.8, 0.05)),
    "wickelgren": (lambda t, l, b, p: l * (1 + b * t) ** (-p), (0.6, 0.1, 0.3)),
}


def fit_law(name: str, t, y) -> dict:
    """Least-squares fit of one forgetting law to (t, y); returns parameters, residual SS and AIC (normal errors)."""
    f, x0 = LAWS[name]
    t, y = np.asarray(t, float), np.asarray(y, float)

    def sse(p):
        with np.errstate(all="ignore"):
            r = f(t, *np.abs(p)) - y
        v = float(np.sum(r ** 2))
        return v if np.isfinite(v) else 1e9

    best = None
    for scale in (1.0, 0.3, 3.0):
        r = minimize(sse, np.asarray(x0, float) * scale, method="Nelder-Mead",
                     options={"xatol": 1e-10, "fatol": 1e-12, "maxiter": 40000})
        if best is None or r.fun < best.fun:
            best = r
    n, k = len(t), len(x0)
    rss = max(float(best.fun), 1e-12)
    return {"params": np.abs(best.x), "sse": rss, "aic": n * np.log(rss / n) + 2 * k, "k": k}


def law_curve(name: str, params, t):
    return LAWS[name][0](np.asarray(t, float), *params)


def gamma_mixture(t, shape: float, scale: float):
    """Average of exponentials e^{-lambda t} over lambda ~ Gamma(shape, scale): exactly (1 + scale t)^(-shape)."""
    return (1.0 + scale * np.asarray(t, float)) ** (-shape)


def jost(law: str, params, t_young: float, t_old: float, horizon) -> tuple[np.ndarray, np.ndarray]:
    """Jost's second law: two memories equally strong now, one young and one old.  Returns the strength of each over
    ``horizon`` further time, along the same law (each shifted so it passes through the common value)."""
    f = LAWS[law][0]
    h = np.asarray(horizon, float)
    return f(t_young + h, *params), f(t_old + h, *params) * f(t_young, *params) / f(t_old, *params)


# ============================================================================================== interference
def associator_interference(n: int = 200, pairs: int = 20, overlap: float = 0.5, second: bool = True, rng=None) -> dict:
    """A-B, A-C interference in a linear (Hebbian) associator of dimension ``n``.

    Learn ``pairs`` cue-target pairs A->B, then (if ``second``) A'->C, where each A' shares a fraction ``overlap`` of
    A's components; test A->B.  Retroactive interference is the drop in the correlation of the retrieved vector with B.
    Returns the mean correlation after the first list alone and after both."""
    rng = rng or np.random.default_rng(0)
    A = rng.standard_normal((pairs, n)) / np.sqrt(n)
    B = rng.standard_normal((pairs, n)) / np.sqrt(n)
    C = rng.standard_normal((pairs, n)) / np.sqrt(n)
    noise = rng.standard_normal((pairs, n)) / np.sqrt(n)
    A2 = np.sqrt(overlap) * A + np.sqrt(1 - overlap) * noise
    W1 = B.T @ A
    W2 = W1 + (C.T @ A2 if second else 0.0)

    def corr(W):
        out = (W @ A.T).T
        return float(np.mean([np.corrcoef(o, b)[0, 1] for o, b in zip(out, B)]))

    return {"first": corr(W1), "both": corr(W2)}


# ============================================================================================== complementary learning systems
SEMANTIC_ITEMS = ("pine", "oak", "rose", "daisy", "robin", "canary", "sunfish", "salmon")
RELATIONS = ("isa", "is", "can", "has")
ATTRIBUTES = ("living thing", "plant", "animal", "tree", "flower", "bird", "fish", "pine", "oak", "rose", "daisy",
              "robin", "canary", "sunfish", "salmon", "pretty", "big", "living", "green", "red", "yellow", "grow",
              "move", "swim", "fly", "sing", "bark", "petals", "wings", "feathers", "scales", "gills", "roots",
              "skin", "leaves")
_FACTS = {
    ("pine", "isa"): "living thing plant tree pine", ("oak", "isa"): "living thing plant tree oak",
    ("rose", "isa"): "living thing plant flower rose", ("daisy", "isa"): "living thing plant flower daisy",
    ("robin", "isa"): "living thing animal bird robin", ("canary", "isa"): "living thing animal bird canary",
    ("sunfish", "isa"): "living thing animal fish sunfish", ("salmon", "isa"): "living thing animal fish salmon",
    ("pine", "is"): "living green", ("oak", "is"): "living big", ("rose", "is"): "living pretty red",
    ("daisy", "is"): "living pretty yellow", ("robin", "is"): "living red", ("canary", "is"): "living yellow",
    ("sunfish", "is"): "living yellow", ("salmon", "is"): "living red",
    ("pine", "can"): "grow", ("oak", "can"): "grow", ("rose", "can"): "grow", ("daisy", "can"): "grow",
    ("robin", "can"): "grow move fly", ("canary", "can"): "grow move fly sing", ("sunfish", "can"): "grow move swim",
    ("salmon", "can"): "grow move swim",
    ("pine", "has"): "roots bark leaves", ("oak", "has"): "roots bark leaves", ("rose", "has"): "roots leaves petals",
    ("daisy", "has"): "roots leaves petals", ("robin", "has"): "skin wings feathers",
    ("canary", "has"): "skin wings feathers", ("sunfish", "has"): "skin scales gills",
    ("salmon", "has"): "skin scales gills",
}
# the new item of McClelland, McNaughton and O'Reilly: a bird that swims and cannot fly
_PENGUIN = {("penguin", "isa"): "living thing animal bird", ("penguin", "is"): "living",
            ("penguin", "can"): "grow move swim", ("penguin", "has"): "skin wings feathers"}


def _attr_vec(words: str) -> np.ndarray:
    v = np.zeros(len(ATTRIBUTES))
    # multi-word attribute "living thing" first
    s = words
    if "living thing" in s:
        v[ATTRIBUTES.index("living thing")] = 1.0
        s = s.replace("living thing", "")
    for w in s.split():
        v[ATTRIBUTES.index(w)] = 1.0
    return v


def semantic_patterns(with_penguin: bool = False):
    """Rumelhart's semantic network as (item one-hot, relation one-hot) -> attribute patterns."""
    items = list(SEMANTIC_ITEMS) + (["penguin"] if with_penguin else [])
    X_i, X_r, Y = [], [], []
    facts = dict(_FACTS)
    if with_penguin:
        facts.update(_PENGUIN)
    for (it, rel), words in facts.items():
        xi = np.zeros(len(items))
        xi[items.index(it)] = 1.0
        xr = np.zeros(len(RELATIONS))
        xr[RELATIONS.index(rel)] = 1.0
        X_i.append(xi)
        X_r.append(xr)
        Y.append(_attr_vec(words))
    return np.array(X_i), np.array(X_r), np.array(Y), items


class SemanticNet:
    """Rumelhart's network: item -> representation (8 units) -> hidden (15) <- relation; hidden -> attributes.
    Sigmoid units, squared error, plain gradient descent (the architecture of Rogers and McClelland, 2004)."""

    def __init__(self, n_items: int, rep: int = 8, hidden: int = 15, seed: int = 0, scale: float = 0.1):
        r = np.random.default_rng(seed)
        self.W1 = r.uniform(-scale, scale, (n_items, rep))
        self.b1 = np.full(rep, -2.0) * 0
        self.W2 = r.uniform(-scale, scale, (rep, hidden))
        self.W2r = r.uniform(-scale, scale, (len(RELATIONS), hidden))
        self.b2 = np.zeros(hidden)
        self.W3 = r.uniform(-scale, scale, (hidden, len(ATTRIBUTES)))
        self.b3 = np.full(len(ATTRIBUTES), -2.0)

    def add_item(self, seed: int = 1, scale: float = 0.1):
        r = np.random.default_rng(seed)
        self.W1 = np.vstack([self.W1, r.uniform(-scale, scale, (1, self.W1.shape[1]))])

    @staticmethod
    def _s(x):
        return 1.0 / (1.0 + np.exp(-x))

    def forward(self, Xi, Xr):
        h1 = self._s(Xi @ self.W1 + self.b1)
        h2 = self._s(h1 @ self.W2 + Xr @ self.W2r + self.b2)
        y = self._s(h2 @ self.W3 + self.b3)
        return h1, h2, y

    def error(self, Xi, Xr, Y) -> float:
        return float(np.mean((self.forward(Xi, Xr)[2] - Y) ** 2))

    def train(self, Xi, Xr, Y, epochs: int, lr: float = 0.1, track=None) -> list:
        """Full-batch gradient descent; ``track`` is a list of (Xi, Xr, Y) sets whose errors are recorded per epoch."""
        hist = []
        for _ in range(epochs):
            h1, h2, y = self.forward(Xi, Xr)
            d3 = (y - Y) * y * (1 - y)
            d2 = (d3 @ self.W3.T) * h2 * (1 - h2)
            d1 = (d2 @ self.W2.T) * h1 * (1 - h1)
            self.W3 -= lr * h2.T @ d3
            self.b3 -= lr * d3.sum(0)
            self.W2 -= lr * h1.T @ d2
            self.W2r -= lr * Xr.T @ d2
            self.b2 -= lr * d2.sum(0)
            self.W1 -= lr * Xi.T @ d1
            self.b1 -= lr * d1.sum(0)
            if track is not None:
                hist.append([self.error(*s) for s in track])
        return hist


def penguin_experiment(epochs_base: int = 3000, epochs_new: int = 400, lr: float = 0.1, seed: int = 0) -> dict:
    """Train on the eight items, then teach the penguin either alone (focused) or interleaved with the old facts.
    Returns the error on the old items and on the penguin over the second phase, for both regimes."""
    Xi, Xr, Y, _ = semantic_patterns(False)
    base = SemanticNet(len(SEMANTIC_ITEMS), seed=seed)
    base.train(Xi, Xr, Y, epochs_base, lr)
    Pi, Pr, PY, _ = semantic_patterns(True)
    old = (np.hstack([Xi, np.zeros((len(Xi), 1))]), Xr, Y)
    new_mask = Pi[:, -1] == 1
    new = (Pi[new_mask], Pr[new_mask], PY[new_mask])
    out = {}
    for regime in ("focused", "interleaved"):
        net = SemanticNet(len(SEMANTIC_ITEMS), seed=seed)
        net.__dict__.update({k: v.copy() for k, v in base.__dict__.items()})
        net.add_item(seed=seed + 1)
        train = new if regime == "focused" else (Pi, Pr, PY)
        h = np.array(net.train(*train, epochs_new, lr, track=[old, new]))
        out[regime] = {"old": h[:, 0], "new": h[:, 1]}
        # what the network now says a robin can do
        ri = np.zeros((1, len(SEMANTIC_ITEMS) + 1))
        ri[0, SEMANTIC_ITEMS.index("robin")] = 1
        rc = np.zeros((1, len(RELATIONS)))
        rc[0, RELATIONS.index("can")] = 1
        y = net.forward(ri, rc)[2][0]
        out[regime]["robin_can"] = {a: float(y[ATTRIBUTES.index(a)]) for a in ("grow", "move", "fly", "swim")}
    out["base_error"] = base.error(Xi, Xr, Y)
    return out


# ============================================================================================== spacing (Pavlik and Anderson)
def pa_activation(times, now, c: float = 0.25, a: float = 0.18, s_scale: float = 1.0):
    """Pavlik and Anderson (2005): each presentation j leaves a trace (now - t_j)^(-d_j), with a decay
    d_j = c exp(m_{j-1}) + a set by the activation m_{j-1} at the moment of presentation.  A presentation made while
    the memory is strong decays fast; one made after a gap, while it is weaker, decays slowly.  Times in days."""
    times = np.sort(np.asarray(times, float))
    ds = []
    for j, tj in enumerate(times):
        if j == 0:
            m = -np.inf
        else:
            ages = tj - times[:j]
            m = np.log(np.sum(ages ** (-np.array(ds))))
        ds.append(c * np.exp(m) + a if np.isfinite(m) else a)
    ages = now - times
    ages = np.maximum(ages, 1e-6)
    return float(np.log(np.sum(ages ** (-np.array(ds)))))


def pa_recall(activation, threshold: float = -0.7, s: float = 0.25):
    return 1.0 / (1.0 + np.exp(-(np.asarray(activation, float) - threshold) / s))


def spacing_ridge(gaps, retention, **kw) -> np.ndarray:
    """Recall after a study at 0 and a restudy at ``gap`` days, tested ``retention`` days after the restudy: a matrix
    (retention x gaps).  Its row maxima trace the ridgeline of Cepeda et al. (2008)."""
    out = np.zeros((len(retention), len(gaps)))
    pk = {k: v for k, v in kw.items() if k in ("threshold", "s")}
    ak = {k: v for k, v in kw.items() if k in ("c", "a")}
    for i, ri in enumerate(retention):
        for j, g in enumerate(gaps):
            times = [0.0, max(g, 1e-3)]
            out[i, j] = pa_recall(pa_activation(times, g + ri, **ak), **pk)
    return out


# ============================================================================================== testing: the bifurcation model
def bifurcation(params=None, delays=(5 / 1440, 2.0, 7.0), n: int = 4000, rng=None) -> dict:
    """The bifurcation model of the testing effect (Kornell, Bjork and Garcia 2011, after Halamish and Bjork).

    Item strengths start N(0, 1).  Restudy adds ``restudy`` to every item.  An initial test retrieves the items above
    ``theta_test`` and adds ``gain`` to those only; the others gain nothing.  After ``d`` days strength has fallen by
    ``loss * log(1 + d / tau)``, and an item is recalled with probability Phi((strength - 0.5) / 0.5).  So restudy
    lifts every item a little, testing lifts a subset a lot: restudy wins at once, testing wins later.  Returns recall
    by delay for each condition, the share retrieved on the initial test, and the strengths after learning."""
    from scipy.stats import norm

    p = {"restudy": 1.0, "gain": 1.6, "theta_test": 0.3, "loss": 0.35, "tau": 0.05, **(params or {})}
    rng = rng or np.random.default_rng(0)
    s0 = rng.standard_normal(n)
    hit = s0 > p["theta_test"]
    strengths = {"restudy": s0 + p["restudy"], "test": s0 + np.where(hit, p["gain"], 0.0)}
    d = np.asarray(delays, float)
    out = {"delays": d, "initial_test": float(hit.mean()), "params": p}
    for name, s in strengths.items():
        drop = p["loss"] * np.log1p(d / p["tau"])
        out[name] = np.array([float(norm.cdf((s - x - 0.5) / 0.5).mean()) for x in drop])
        out[name + "_strength"] = s
    return out


def fit_bifurcation(observed: dict, delays=(5 / 1440, 2.0, 7.0)) -> dict:
    """Least-squares fit of the bifurcation model's five parameters to recall proportions by condition and delay
    (``observed = {"restudy": [...], "test": [...]}``), with common random numbers."""
    keys = ("restudy", "gain", "theta_test", "loss", "tau")
    obs = np.r_[observed["restudy"], observed["test"]]

    def unpack(x):
        p = dict(zip(keys, np.abs(x)))
        p["theta_test"] = float(x[2])  # may be negative: most items can be retrieved
        return p

    def loss(x):
        p = unpack(x)
        b = bifurcation(p, delays, n=3000, rng=np.random.default_rng(1))
        return float(np.sum((np.r_[b["restudy"], b["test"]] - obs) ** 2))

    best = None
    for x0 in ((1.0, 1.0, -0.5, 0.35, 0.05), (0.6, 2.0, -0.8, 0.25, 0.2), (1.4, 1.2, 0.0, 0.5, 0.02)):
        r = minimize(loss, np.array(x0), method="Nelder-Mead", options={"maxiter": 3000, "xatol": 1e-4,
                                                                        "fatol": 1e-7})
        if best is None or r.fun < best.fun:
            best = r
    p = unpack(best.x)
    return {"params": p, "sse": float(best.fun), "model": bifurcation(p, delays)}


# ============================================================================================== false memory: global matching
def drm_global_matching(lists: int = 24, length: int = 12, dim: int = 300, assoc: float = 0.55, noise_items: int = 24,
                        criterion: float = None, rng=None) -> dict:
    """A global-matching account of the DRM illusion.

    Each list has a theme vector (the lure); each studied word is the theme scaled by ``assoc`` plus its own features.
    Memory is the sum of the studied words.  A test item's familiarity is its summed similarity to memory.  The lure,
    which resembles every studied word a little, matches the sum about as well as a studied word does.  Returns the
    familiarity of studied words, lures, related-unstudied and unrelated words, and the yes rates at a criterion set
    to give 0.80 hits."""
    rng = rng or np.random.default_rng(0)

    def unit(v):
        return v / np.linalg.norm(v, axis=-1, keepdims=True)

    fam = {"studied": [], "lure": [], "unrelated": []}
    for _ in range(lists):
        theme = unit(rng.standard_normal(dim))
        own = unit(rng.standard_normal((length, dim)))
        a_i = rng.uniform(0.0, 2.0 * assoc, length)[:, None]  # associative strength varies from word to word
        words = unit(a_i * theme + np.sqrt(1 - a_i ** 2) * own)
        memory = words.sum(0)
        fam["studied"] += list(words @ memory)
        fam["lure"].append(float(theme @ memory))
        other = unit(rng.standard_normal((noise_items // lists + 1, dim)))
        fam["unrelated"] += list(other @ memory)
    fam = {k: np.array(v) for k, v in fam.items()}
    crit = criterion if criterion is not None else float(np.quantile(fam["studied"], 0.2))
    rates = {k: float(np.mean(v > crit)) for k, v in fam.items()}
    return {"familiarity": fam, "criterion": crit, "yes": rates}


# ============================================================================================== consolidation: two stores
def two_store(age, a: float = 0.3, k: float = 0.08, b: float = 0.004, lesion: bool = False):
    """A two-store sketch of systems consolidation (after Alvarez and Squire, 1994).  A memory is laid down in the
    hippocampus with strength 1, which fades at rate ``a`` per unit time; while it lasts it teaches the cortex at rate
    ``k`` times its strength; the cortical trace fades at the slow rate ``b``:
        dh/dt = -a h,   dc/dt = k h - b c,   h(0) = 1, c(0) = 0
        h(t) = e^{-a t},  c(t) = k (e^{-b t} - e^{-a t}) / (a - b).
    Retrieval strength is h + c; after a hippocampal lesion only c is left, so the oldest memories are spared and the
    newest lost: Ribot's gradient, with a peak at intermediate ages."""
    t = np.asarray(age, float)
    h = np.exp(-a * t)
    c = k * (np.exp(-b * t) - np.exp(-a * t)) / (a - b)
    return c if lesion else h + c


# ============================================================================================== reconstruction: the category adjustment model
def category_adjustment(positions, trace_sd: float, cat_sd: float, edges=(0.0, 90.0), n: int = 4000, rng=None) -> dict:
    """Huttenlocher, Hedges and Duncan (1991): a remembered location is a blend of a noisy fine-grained trace and the
    centre of its category.  With trace noise ``trace_sd`` and the category's spread ``cat_sd``, the best blend weights
    the trace by  lambda = cat_sd^2 / (cat_sd^2 + trace_sd^2)  and the prototype by 1 - lambda, and the estimate is kept
    inside the category.  Returns, for each true position, the mean bias and the root-mean-square error of the blended
    estimate and of the raw trace."""
    rng = rng or np.random.default_rng(0)
    lo, hi = edges
    proto = (lo + hi) / 2
    lam = cat_sd ** 2 / (cat_sd ** 2 + trace_sd ** 2)
    x = np.asarray(positions, float)
    trace = x[:, None] + trace_sd * rng.standard_normal((len(x), n))
    est = np.clip(lam * trace + (1 - lam) * proto, lo, hi)
    return {"positions": x, "lambda": lam, "bias": (est - x[:, None]).mean(1),
            "rmse": np.sqrt(((est - x[:, None]) ** 2).mean(1)), "rmse_trace": np.sqrt(((trace - x[:, None]) ** 2).mean(1))}


# ============================================================================================== eyewitness confidence: lineups by signal detection
def lineup_cac(d_prime: float = 1.5, size: int = 6, criteria=(0.5, 1.0, 1.5, 2.0, 2.5), n: int = 200_000,
               rng=None) -> dict:
    """A lineup by signal detection with the max rule (Clark 2003; Wixted and Mickes 2014).  Every face gives a
    memory-match signal: the culprit N(d', 1), every other face N(0, 1).  The witness picks the best-matching face if
    its signal passes the lowest criterion, and their confidence is the number of criteria it passes.  In
    culprit-present lineups the culprit is the suspect; in culprit-absent lineups an innocent suspect is one of the
    ``size`` faces.  The confidence-accuracy characteristic is, at each confidence level, the share of suspect
    identifications that are of the culprit (equal numbers of the two kinds of lineup).  Returns that, the counts,
    and the overall share."""
    rng = rng or np.random.default_rng(0)
    c = np.asarray(criteria, float)
    present = rng.standard_normal((n, size))
    present[:, 0] += d_prime  # the culprit is face 0
    absent = rng.standard_normal((n, size))  # the innocent suspect is face 0
    out = {"criteria": c, "levels": np.arange(1, len(c) + 1)}
    for name, L in (("present", present), ("absent", absent)):
        pick = L.argmax(1)
        best = L.max(1)
        conf = np.searchsorted(c, best, side="right")  # 0 = no identification
        out[name + "_suspect"] = np.array([np.sum((pick == 0) & (conf == k)) for k in out["levels"]])
        out[name + "_filler"] = np.array([np.sum((pick != 0) & (conf == k)) for k in out["levels"]])
    tp, ti = out["present_suspect"], out["absent_suspect"]
    out["cac"] = tp / np.maximum(tp + ti, 1)
    out["overall"] = float(tp.sum() / (tp.sum() + ti.sum()))
    return out


# ============================================================================================== industry: half-life regression
def hlr_simulate(learners: int = 400, words: int = 60, reviews: int = 12, theta=(0.9, -0.6, 2.2), rng=None) -> dict:
    """Simulated practice data in the form of Settles and Meeder (2016).  Each learner reviews words at random gaps;
    the true half-life of a word for a learner is h = 2^{theta . x} days with x = (sqrt(times right), sqrt(times
    wrong), 1) plus a per-word difficulty; recall after a gap Delta is p = 2^{-Delta / h}.  Returns the rows (the
    features, the gap, whether it was recalled) for fitting."""
    rng = rng or np.random.default_rng(0)
    th = np.asarray(theta, float)
    diff = rng.normal(0.0, 0.5, words)
    rows = []
    for _ in range(learners):
        for w in rng.choice(words, size=min(words, 8), replace=False):
            right = wrong = 0
            for _ in range(reviews):
                gap = float(rng.exponential(3.0)) + 0.02
                x = np.array([np.sqrt(right), np.sqrt(wrong), 1.0])
                h = 2.0 ** (x @ th - diff[w])
                ok = rng.random() < 2.0 ** (-gap / h)
                rows.append((np.sqrt(right), np.sqrt(wrong), 1.0, gap, float(ok), w))
                right, wrong = right + ok, wrong + (not ok)
    R = np.array(rows)
    return {"x": R[:, :3], "gap": R[:, 3], "recalled": R[:, 4], "word": R[:, 5].astype(int), "theta": th,
            "difficulty": diff}


def fit_hlr(x, gap, recalled, ridge: float = 0.1, alpha: float = 0.0) -> dict:
    """Half-life regression (Settles and Meeder 2016): choose theta to minimise
    sum (p - 2^{-Delta/h})^2 + alpha (h_obs - h)^2 + ridge |theta|^2, with h = 2^{theta . x} and h_obs the half-life a
    single observation implies (recall clipped to [0.0001, 0.9999]).  The half-life term suits recall proportions per
    session, as in the paper; with single right-or-wrong outcomes it pulls theta upward, so it is off by default.
    Returns theta and the predicted recall."""
    x, gap, y = np.asarray(x, float), np.asarray(gap, float), np.asarray(recalled, float)
    yc = np.clip(y, 1e-4, 1 - 1e-4)
    h_obs = -gap / np.log2(yc)

    def loss(th):
        h = 2.0 ** (x @ th)
        p = 2.0 ** (-gap / h)
        return float(np.mean((y - p) ** 2) + alpha * np.mean((np.log2(h_obs) - x @ th) ** 2) + ridge * th @ th / len(y))

    r = minimize(loss, np.zeros(x.shape[1]), method="BFGS")
    th = r.x
    return {"theta": th, "predicted": 2.0 ** (-gap / 2.0 ** (x @ th)), "loss": float(r.fun)}
