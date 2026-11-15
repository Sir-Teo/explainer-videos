"""Psyche holds things in mind: span, forgetting, scanning, capacity and precision (Part 19 of *Psychology, Built*).

Span and chunks: Miller's recoding arithmetic, and a phonological loop in which each item's trace fades unless it is
rehearsed again within a lognormal decay time (about two seconds), backed by a small store of a few items that
articulatory suppression leaves alone: word length shortens the loop's span; suppression removes the length effect.
Iconic memory: Sperling's partial report as a fast-fading icon read into a store of about four and a half letters.
Short-term forgetting: Brown and Peterson's task under SIMPLE's temporal distinctiveness (Brown, Neath and Chater
2007): an item is recalled in proportion to how distinct its age is, on a log scale, from the ages of earlier items,
so the first trial shows no forgetting and forgetting grows as earlier trials pile up (Keppel and Underwood 1962).
Scanning: Sternberg's serial exhaustive comparison against unlimited- and limited-capacity parallel models, the
last of which reproduces the serial predictions exactly (Townsend 1972).  Capacity: change detection under slots,
with Cowan's and Pashler's K.  Precision: continuous report on a circle, with von Mises noise whose Fisher
information is the precision J; the mixture model (Zhang and Luck 2008) and the swap model (Bays, Catalao and Husain
2009) as descriptions, and four process models fitted by maximum likelihood across set sizes: slots, slots plus
averaging, equal precision and variable precision (van den Berg et al. 2012).  Neurons: a ring attractor whose bump
holds a remembered angle and diffuses, so that the variance of the memory grows linearly with the delay.  Training:
a simulator of brain-training trials in which near transfer is real, far transfer is zero, and expectation inflates
gains against a passive control.

Parameters make the classic patterns legible; they are not fitted to a laboratory unless a function says so, and
Part 19's scenes say which numbers are published, which are fitted to open data, and which are Psyche's.
"""

from __future__ import annotations

import numpy as np
from scipy.optimize import minimize
from scipy.special import i0e, i1e
from scipy.stats import gamma as gamma_dist

TWO_PI = 2 * np.pi


def wrap(x):
    """Angles wrapped into [-pi, pi)."""
    return (np.asarray(x) + np.pi) % TWO_PI - np.pi


# ============================================================================================== span and chunks
def recoded_span(group: int, chunks: float = 7.0, cost: float = 0.0) -> float:
    """Binary digits held when each run of ``group`` digits is recoded into one chunk (Miller 1956).

    With a span of ``chunks`` chunks, the span in binary digits is ``chunks * group``; ``cost`` chunks are lost to
    the work of recoding at each size above one (Smith's spans fell short of the ideal)."""
    return max(0.0, chunks - cost * (group > 1)) * group


def absolute_judgment(n_categories, noise: float = 0.04, span: float = 1.0) -> np.ndarray:
    """Information transmitted (bits) when ``n`` equally spaced stimuli on a line of length ``span`` are labelled.

    The percept is the stimulus plus Gaussian noise of s.d. ``noise``; the observer answers with the nearest
    category.  The confusion matrix comes from normal CDFs between category boundaries, and the transmitted
    information is the mutual information of stimulus and response with stimuli equally likely.  It rises with
    ``n`` and levels off near ``log2(span / noise)`` minus a constant: the channel capacity of absolute judgment."""
    from scipy.stats import norm

    out = []
    for n in np.atleast_1d(n_categories).astype(int):
        if n < 2:
            out.append(0.0)
            continue
        s = np.linspace(0, span, n)
        b = np.r_[-np.inf, (s[:-1] + s[1:]) / 2, np.inf]
        P = norm.cdf((b[None, 1:] - s[:, None]) / noise) - norm.cdf((b[None, :-1] - s[:, None]) / noise)
        joint = P / n
        pr = joint.sum(0)
        with np.errstate(divide="ignore", invalid="ignore"):
            t = np.where(joint > 0, joint * np.log2(joint / (pr[None, :] / n)), 0.0)
        out.append(float(t.sum()))
    return np.array(out)


def budget_sd(set_size, bits: float, sd1: float) -> np.ndarray:
    """Error s.d. when a fixed information budget of ``bits`` is shared equally among ``set_size`` items.

    For a Gaussian source, rate-distortion theory gives a distortion s.d. falling by half for each extra bit, so an
    item given ``bits / N`` bits has s.d. ``sd1 2^(bits - bits / N)`` relative to its s.d. ``sd1`` with all of them."""
    N = np.asarray(set_size, float)
    return sd1 * 2.0 ** (bits - bits / N)


def loop_span(word_duration: float, suppress: bool = False, decay: float = 2.0, decay_cv: float = 0.25,
              store: float = 2.0, lengths=range(1, 13), n: int = 4000, rng=None) -> dict:
    """Serial recall of lists of words of spoken ``word_duration`` seconds through a phonological loop.

    Rehearsal cycles through the list: each item is refreshed once per cycle of ``len * word_duration`` seconds,
    and it survives if its trace lasts that long; trace lifetimes are lognormal with median ``decay`` s and
    coefficient of variation ``decay_cv``.  A second, non-articulatory store holds ``store`` items on average
    (Poisson-rounded), whichever loop items are lost.  Under articulatory suppression nothing is rehearsed, so only
    the store remains.  A list is correct if every item is held.  Returns ``lengths``, ``p`` (list correct) and the
    ``span``: the length at which ``p`` crosses one half, interpolated."""
    rng = rng or np.random.default_rng(0)
    lengths = np.asarray(list(lengths))
    sig = np.sqrt(np.log1p(decay_cv ** 2))
    p = np.empty(len(lengths))
    for i, L in enumerate(lengths):
        held = np.zeros((n, L), dtype=bool)
        if not suppress:
            life = decay * np.exp(sig * rng.standard_normal((n, L)))
            held |= life > L * word_duration
        cap = np.minimum(rng.poisson(store, n), L)
        lost = (~held).sum(1)
        p[i] = np.mean(lost <= cap)
    return {"lengths": lengths, "p": p, "span": _crossing(lengths, p)}


def _crossing(x, p, level=0.5) -> float:
    """Where a falling curve ``p(x)`` crosses ``level``, by linear interpolation."""
    x, p = np.asarray(x, float), np.asarray(p, float)
    below = np.nonzero(p < level)[0]
    if len(below) == 0:
        return float(x[-1])
    j = below[0]
    if j == 0:
        return float(x[0])
    return float(x[j - 1] + (p[j - 1] - level) / (p[j - 1] - p[j]) * (x[j] - x[j - 1]))


# ============================================================================================== iconic memory
def partial_report(cue_delays, n_letters: int = 12, row: int = 4, store: float = 4.5, icon: float = 0.62,
                   tau: float = 250.0) -> dict:
    """Letters available in Sperling's partial report against the cue's delay (ms), and in whole report.

    A cued letter is read from the icon with probability ``icon * exp(-delay / tau)``; otherwise it is reported
    only if it is among the ``store`` letters already transferred, a fraction ``store / n_letters``.  Letters
    available = proportion of the cued row reported times ``n_letters``.  Whole report is ``store``."""
    t = np.asarray(cue_delays, float)
    p_icon = icon * np.exp(-np.maximum(t, 0) / tau)
    base = store / n_letters
    prop = p_icon + (1 - p_icon) * base
    return {"delay": t, "available": prop * n_letters, "whole": store, "row": row}


# ============================================================================================== short-term forgetting
def simple_recall(ages, target: int, c: float = 1.0, threshold: float = 0.5, slope: float = 0.05) -> float:
    """SIMPLE's probability of recalling item ``target`` among items of the given ``ages`` (seconds since study).

    Items lie on a log-time line; the similarity of i and j is ``exp(-c |log a_i - log a_j|)``; the item's
    discriminability is ``1 / sum_j s_ij`` (Luce's choice rule); recall happens if it clears a soft threshold,
    a logistic of width ``slope`` around ``threshold``."""
    a = np.log(np.asarray(ages, float))
    s = np.exp(-c * np.abs(a - a[target]))
    d = 1.0 / s.sum()
    return float(d / (1 + np.exp(-(d - threshold) / slope))) if slope > 0 else d


def brown_peterson(delays, trial: int, gap: float = 20.0, c: float = 1.0, threshold: float = 0.5,
                   slope: float = 0.05, earlier_delays=None) -> np.ndarray:
    """Recall of a trigram after a filled delay, on the ``trial``-th trial of a session (1 = the first).

    Each earlier trial studied one trigram; trials start ``gap`` s after the previous recall, and earlier trials'
    delays are ``earlier_delays`` (default: the mean of ``delays``).  Returns the recall probability for each delay
    under :func:`simple_recall`."""
    delays = np.asarray(delays, float)
    prev = np.full(trial - 1, delays.mean()) if earlier_delays is None else np.asarray(earlier_delays, float)
    out = np.empty(len(delays))
    for i, d in enumerate(delays):
        ages = [d]
        t = d
        for e in prev[::-1]:  # walk back through earlier trials: each one's recall, then its study
            t += gap + e
            ages.append(t)
        out[i] = simple_recall(ages, 0, c, threshold, slope)
    return out


# ============================================================================================== scanning
def sternberg_rts(set_size: int, positive: bool, model: str = "serial", n: int = 4000, base: float = 397.0,
                  compare: float = 38.0, base_sd: float = 60.0, rng=None) -> np.ndarray:
    """Reaction times (ms) in Sternberg's memory-scanning task.

    ``serial``: exhaustive serial comparison, ``set_size`` exponential comparisons of mean ``compare``;
    ``self``: serial but stopping at a match (half the comparisons on average on positive trials);
    ``parallel``: unlimited-capacity parallel comparisons, each of mean ``compare``, finishing at the slowest;
    ``limited``: parallel with a fixed total capacity reallocated as comparisons finish, which gives exactly the
    serial model's distribution.  A normal base time (encoding and response) is added."""
    rng = rng or np.random.default_rng(0)
    k = set_size
    if model == "serial":
        dec = rng.exponential(compare, (n, k)).sum(1)
    elif model == "self":
        dec = rng.exponential(compare, (n, k))
        if positive:  # the match sits at a uniformly random position; scanning stops there
            stop = rng.integers(1, k + 1, n)
            dec = np.where(np.arange(k)[None, :] < stop[:, None], dec, 0.0)
        dec = dec.sum(1)
    elif model == "parallel":
        dec = rng.exponential(compare, (n, k)).max(1)
    elif model == "limited":
        # k comparisons share a total rate 1/compare: with j left, each runs at rate 1/(j compare) and the next
        # one finishes after the minimum of j such exponentials
        dec = np.zeros(n)
        for j in range(k, 0, -1):
            dec += rng.exponential(compare * j, (n, j)).min(1)
    else:
        raise ValueError(model)
    return base + base_sd * rng.standard_normal(n) + dec


# ============================================================================================== capacity
def change_detection(set_size: int, K: float = 3.5, guess: float = 0.5, n: int = 4000, design: str = "single",
                     rng=None) -> dict:
    """Hits and false alarms of a slot observer in change detection.

    The observer stores ``min(K, N)`` of the ``N`` items (a fractional K stores ``floor(K)`` or ``ceil(K)``).  On
    change trials the probed item (``single`` probe) is detected if stored; otherwise, and on all unstored no-change
    trials, the observer guesses "change" with probability ``guess``.  With a ``whole`` display, a change anywhere is
    detected if that item was stored."""
    rng = rng or np.random.default_rng(0)
    N = set_size
    lo = np.floor(K)
    stored = np.minimum(lo + (rng.random(n) < K - lo), N)
    p_in = stored / N
    seen = rng.random(n) < p_in
    hit = np.where(seen, True, rng.random(n) < guess)
    # no-change: a stored probe is correctly called "same"; an unstored one is guessed
    fa = np.where(rng.random(n) < p_in, False, rng.random(n) < guess)
    return {"H": float(hit.mean()), "FA": float(fa.mean())}


def k_cowan(H, FA, N):
    """Cowan's K for a single-probe display: N (H - FA)."""
    return N * (np.asarray(H) - np.asarray(FA))


def k_pashler(H, FA, N):
    """Pashler's K for a whole-display probe: N (H - FA) / (1 - FA)."""
    return N * (np.asarray(H) - np.asarray(FA)) / (1 - np.asarray(FA))


# ============================================================================================== precision on a circle
def vm_pdf(x, kappa):
    """The von Mises density with mean 0 and concentration ``kappa`` (broadcasts)."""
    kappa = np.asarray(kappa, float)
    return np.exp(kappa * (np.cos(x) - 1)) / (TWO_PI * i0e(kappa))


def fisher_J(kappa):
    """The precision of a von Mises: its Fisher information about the mean, kappa I1(kappa) / I0(kappa)."""
    kappa = np.asarray(kappa, float)
    return kappa * i1e(kappa) / i0e(kappa)


_KG = np.concatenate([[0.0], np.geomspace(1e-4, 1e4, 4000)])
_JG = fisher_J(_KG)


def kappa_of_J(J):
    """The concentration whose Fisher information is ``J`` (inverted on a grid; J is increasing in kappa)."""
    return np.interp(np.asarray(J, float), _JG, _KG)


def circ_sd(kappa):
    """A von Mises's circular standard deviation, sqrt(-2 log(I1/I0)), in radians."""
    kappa = np.asarray(kappa, float)
    r = np.where(kappa > 0, i1e(kappa) / i0e(np.maximum(kappa, 1e-12)), 0.0)
    return np.sqrt(-2 * np.log(np.maximum(r, 1e-300)))


def kappa_of_sd(sd):
    """The concentration with circular standard deviation ``sd`` (radians)."""
    r = np.exp(-np.asarray(sd, float) ** 2 / 2)
    ks = _KG[1:]
    rr = i1e(ks) / i0e(ks)
    return np.interp(r, rr, ks)


def _fit(nll, x0s):
    best = None
    for x0 in x0s:
        r = minimize(nll, np.asarray(x0, float), method="Nelder-Mead",
                     options={"xatol": 1e-6, "fatol": 1e-8, "maxiter": 4000, "maxfev": 8000})
        if best is None or r.fun < best.fun:
            best = r
    return best


def fit_mixture(errors) -> dict:
    """Zhang and Luck's mixture: a von Mises around the target with probability ``1 - g`` and uniform guesses with
    probability ``g``, by maximum likelihood.  Returns ``g``, ``kappa``, ``sd`` (radians) and ``nll``."""
    e = wrap(errors)

    def nll(th):
        g = 1 / (1 + np.exp(-th[0]))
        k = np.exp(th[1])
        return -np.sum(np.log((1 - g) * vm_pdf(e, k) + g / TWO_PI))

    r = _fit(nll, [(-2, np.log(5)), (0, np.log(2)), (-4, np.log(20))])
    g, k = 1 / (1 + np.exp(-r.x[0])), float(np.exp(r.x[1]))
    return {"g": float(g), "kappa": k, "sd": float(circ_sd(k)), "nll": float(r.fun)}


def fit_swap(errors, nontarget_errors) -> dict:
    """Bays, Catalao and Husain's model: responses around the target (``pT``), around a non-target (``pN``, the
    swaps, spread over the non-targets equally) or uniform (``pU``), with one von Mises concentration.
    ``nontarget_errors`` is (trials, m) of response minus each non-target, NaN where absent."""
    e = wrap(errors)
    nt = wrap(np.asarray(nontarget_errors, float))
    have = np.isfinite(nt)
    m = have.sum(1)

    def nll(th):
        w = np.exp(np.r_[th[:2], 0.0])
        w = w / w.sum()
        k = np.exp(th[2])
        f_nt = np.where(have, vm_pdf(np.where(have, nt, 0.0), k), 0.0).sum(1) / np.maximum(m, 1)
        pn = np.where(m > 0, w[1], 0.0)
        pu = np.where(m > 0, w[2], w[1] + w[2])
        return -np.sum(np.log(w[0] * vm_pdf(e, k) + pn * f_nt + pu / TWO_PI))

    r = _fit(nll, [(2, 0, np.log(5)), (1, -1, np.log(2)), (3, 1, np.log(10))])
    w = np.exp(np.r_[r.x[:2], 0.0])
    w = w / w.sum()
    k = float(np.exp(r.x[2]))
    return {"pT": float(w[0]), "pN": float(w[1]), "pU": float(w[2]), "kappa": k, "sd": float(circ_sd(k)),
            "nll": float(r.fun)}


# ---------------------------------------------------------------------------------------------- process models
_GQ = (np.arange(40) + 0.5) / 40  # quantile midpoints for integrating over gamma-distributed precision


def model_pdf(model: str, params, errors, set_sizes) -> np.ndarray:
    """The density of each error under a process model, given each trial's set size.

    ``slots`` (K, J): an item is stored with probability min(1, K/N), with precision J, else a uniform guess.
    ``averaging`` (K, J): K integer slots (K rounded) are spread over the N items; a stored item with s slots has
    precision s J, and items get floor(K/N) or ceil(K/N) slots when K >= N.
    ``equal`` (J1, alpha): every item is stored with precision J1 N^-alpha.
    ``variable`` (J1, alpha, tau): precision is gamma distributed with mean J1 N^-alpha and scale tau."""
    e = wrap(errors)
    N = np.asarray(set_sizes, float)
    if model == "slots":
        K, J = params
        pm = np.minimum(1.0, K / N)
        return pm * vm_pdf(e, kappa_of_J(J)) + (1 - pm) / TWO_PI
    if model == "averaging":
        K, J = params
        K = max(1, int(round(K)))
        out = np.empty(len(e))
        for n in np.unique(N):
            m = N == n
            n = int(n)
            if K >= n:
                lo, extra = divmod(K, n)
                f = (extra / n) * vm_pdf(e[m], kappa_of_J((lo + 1) * J)) + (1 - extra / n) * vm_pdf(
                    e[m], kappa_of_J(lo * J))
            else:
                f = (K / n) * vm_pdf(e[m], kappa_of_J(J)) + (1 - K / n) / TWO_PI
            out[m] = f
        return out
    if model == "equal":
        J1, a = params
        return vm_pdf(e, kappa_of_J(J1 * N ** -a))
    if model == "variable":
        J1, a, tau = params
        mean = J1 * N ** -a
        shape = mean / tau
        Js = gamma_dist.ppf(_GQ[None, :], shape[:, None], scale=tau)
        return vm_pdf(e[:, None], kappa_of_J(Js)).mean(1)
    raise ValueError(model)


MODELS = {"slots": 2, "averaging": 2, "equal": 2, "variable": 3}


def fit_model(model: str, errors, set_sizes) -> dict:
    """Maximum-likelihood fit of a process model to one observer's errors; returns params, nll, AIC and BIC."""
    e, N = wrap(errors), np.asarray(set_sizes, float)

    if model == "slots":
        def unpack(th):
            return (np.exp(th[0]), np.exp(th[1]))
        x0s = [(np.log(3), np.log(10)), (np.log(2), np.log(4)), (np.log(5), np.log(20))]
    elif model == "averaging":
        best = None
        for K in range(1, 9):
            def nll(th, K=K):
                return -np.sum(np.log(model_pdf("averaging", (K, np.exp(th[0])), e, N) + 1e-300))
            r = _fit(nll, [(np.log(2),), (np.log(8),)])
            if best is None or r.fun < best[1]:
                best = ((float(K), float(np.exp(r.x[0]))), r.fun)
        return _scores(model, best[0], best[1], len(e))
    elif model == "equal":
        def unpack(th):
            return (np.exp(th[0]), th[1])
        x0s = [(np.log(10), 1.0), (np.log(30), 1.5), (np.log(5), 0.5)]
    elif model == "variable":
        def unpack(th):
            return (np.exp(th[0]), th[1], np.exp(th[2]))
        x0s = [(np.log(10), 1.0, np.log(5)), (np.log(30), 1.5, np.log(20)), (np.log(5), 0.5, np.log(2))]
    else:
        raise ValueError(model)

    def nll(th):
        return -np.sum(np.log(model_pdf(model, unpack(th), e, N) + 1e-300))

    r = _fit(nll, x0s)
    return _scores(model, tuple(float(v) for v in unpack(r.x)), r.fun, len(e))


def _scores(model, params, nll, n) -> dict:
    k = MODELS[model]
    return {"model": model, "params": params, "nll": float(nll), "aic": float(2 * nll + 2 * k),
            "bic": float(2 * nll + k * np.log(n))}


def simulate_report(model: str, params, set_sizes, rng=None) -> np.ndarray:
    """Errors (radians) of an observer of the given process model, one per entry of ``set_sizes``."""
    rng = rng or np.random.default_rng(0)
    N = np.asarray(set_sizes, float)
    n = len(N)
    if model == "slots":
        K, J = params
        stored = rng.random(n) < np.minimum(1, K / N)
        k = np.full(n, float(kappa_of_J(J)))
    elif model == "equal":
        J1, a = params
        stored = np.ones(n, bool)
        k = kappa_of_J(J1 * N ** -a)
    elif model == "variable":
        J1, a, tau = params
        stored = np.ones(n, bool)
        k = kappa_of_J(rng.gamma((J1 * N ** -a) / tau, tau))
    else:
        raise ValueError(model)
    e = np.where(stored, _vm_sample(k, rng), rng.uniform(-np.pi, np.pi, n))
    return wrap(e)


def _vm_sample(kappa, rng):
    kappa = np.asarray(kappa, float)
    out = rng.vonmises(0.0, np.maximum(kappa, 1e-9))
    return np.where(kappa < 1e-6, rng.uniform(-np.pi, np.pi, kappa.shape), out)


# ============================================================================================== a ring attractor
def ring_attractor(cue_angle=0.0, delay: float = 3000.0, n_units: int = 96, trials: int = 200, J0: float = -1.0,
                   J1: float = 6.0, noise: float = 0.06, tau: float = 20.0, dt: float = 1.0, cue_ms: float = 250.0,
                   cue_gain: float = 1.5, drive: float = 0.1, record_every: float = 50.0, rng=None) -> dict:
    """A rate model of delay activity: units on a ring with cosine connectivity hold a bump after the cue is gone.

    ``tau dr/dt = -r + f(J0 <r> + J1 <r cos(theta - theta')> + drive + cue + noise)``, with ``f`` a rectified tanh
    and white noise of strength ``noise`` per unit.  The remembered angle is the bump's population vector; across
    trials it diffuses, so its variance grows about linearly with time.  Returns the recorded ``t`` (ms), the decoded
    angles ``(trials, len(t))`` and the final rates of the first trial."""
    rng = rng or np.random.default_rng(0)
    th = np.linspace(-np.pi, np.pi, n_units, endpoint=False)
    c, s = np.cos(th), np.sin(th)
    r = np.zeros((trials, n_units))
    steps = int(round((cue_ms + delay) / dt))
    every = max(1, int(round(record_every / dt)))
    cue = cue_gain * np.maximum(0, np.cos(th - cue_angle)) ** 2
    ts, angs = [], []
    sq = np.sqrt(dt / tau)
    for k in range(steps):
        mean = r.mean(1, keepdims=True)
        rc = (r * c).mean(1, keepdims=True)
        rs = (r * s).mean(1, keepdims=True)
        inp = J0 * mean + J1 * (rc * c + rs * s) + drive
        if k * dt < cue_ms:
            inp = inp + cue
        r = r + dt / tau * (-r + np.maximum(0, np.tanh(inp))) + noise * sq * rng.standard_normal(r.shape)
        r = np.maximum(r, 0)
        if (k + 1) % every == 0 and (k + 1) * dt >= cue_ms:
            ts.append((k + 1) * dt - cue_ms)
            angs.append(np.arctan2((r * s).sum(1), (r * c).sum(1)))
    return {"t": np.array(ts), "angle": wrap(np.array(angs).T - cue_angle), "rates": r[0], "theta": th}


# ============================================================================================== training
def training_trial(n: int = 40, near: float = 0.6, far: float = 0.0, expectancy: float = 0.25,
                   control: str = "passive", reliability: float = 0.8, rng=None) -> dict:
    """One simulated brain-training trial: pre-post gains on a trained-task measure (near) and a reasoning measure
    (far), trained group against a ``passive`` (no-contact) or ``active`` (placebo training) control.

    True effects in standard-deviation units: ``near`` on the trained task, ``far`` on reasoning, and an
    ``expectancy`` boost on any outcome for people who believe they were trained (the trained group, and an active
    control).  Measures have the given ``reliability``.  Returns Cohen's d for each outcome."""
    rng = rng or np.random.default_rng(0)
    err = np.sqrt(1 / reliability - 1)

    def gain(effect):
        pre = rng.standard_normal(n)
        post = pre + effect + err * rng.standard_normal(n)
        pre_obs = pre + err * rng.standard_normal(n)
        return post - pre_obs

    exp_c = expectancy if control == "active" else 0.0
    out = {}
    for name, eff in (("near", near), ("far", far)):
        t, c = gain(eff + expectancy), gain(exp_c)
        sp = np.sqrt((t.var(ddof=1) + c.var(ddof=1)) / 2)
        out[name] = float((t.mean() - c.mean()) / sp)
    return out
