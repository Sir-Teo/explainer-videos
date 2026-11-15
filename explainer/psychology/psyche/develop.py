"""Psyche's development (Part 30): looking as an instrument, a learner whose attention seeks the middle, number sense
that sharpens with age, an infant statistician, a dynamic neural field that makes and outgrows the A-not-B error,
and the meta-regression a multi-laboratory study needs.

* :func:`habituation`: looking time across familiarization trials falls as a memory of the display builds; a test
  display looks long again in proportion to how far it is from what was learned (dishabituation).  The criterion is
  the one laboratories use: three consecutive looks at half the first three.
* :func:`surprisal_trace` and :func:`goldilocks`: an ideal learner watches objects appear from three boxes and
  updates a Dirichlet-multinomial belief; each event's surprisal is its negative log predictive probability.  An
  observer whose chance of looking away is lowest at intermediate surprisal (Kidd, Piantadosi and Aslin 2012) stays
  longest on sequences that are neither too predictable nor too random.  The U-shaped hazard is an assumption,
  shaped after the published result, not fitted to its data.
* :func:`ans_correct` and :func:`ratio_threshold`: the approximate number system as Gaussian noise that grows with
  number (Weber's law, Part 11): the chance of telling n1 from n2 is Phi(|n1 - n2| / (w sqrt(n1^2 + n2^2))).
  :data:`WEBER` holds illustrative Weber fractions by age, consistent with 1:2 being told apart at six months and
  2:3 at about nine.
* :func:`sample_surprise`: the infant statistician (Xu and Garcia 2008): the probability of a sample of balls from a
  box of known proportions, and its surprisal.
* :func:`a_not_b`: the A-not-B error as dynamics (Thelen, Schoner, Scheier and Smith 2001): a one-dimensional
  neural field over reaching directions, with local excitation, global inhibition, a task input at both lids, a
  cue at the hiding place, and a memory trace that grows where the infant reached.  A field at a low resting level
  (younger) cannot hold a peak through the delay and falls back on its memory of A; a more cooperative field
  (older) sustains the peak at B.  Error rates are run for many simulated infants at once.
* :func:`meta_regression`: random-effects meta-regression (method-of-moments tau^2, weighted least squares), for
  moderators such as age and method in ManyBabies.

Nothing here imports manim.
"""

from __future__ import annotations

from math import erf, sqrt

import numpy as np

__all__ = ["habituation", "surprisal_trace", "goldilocks", "ans_correct", "ratio_threshold", "WEBER",
           "KINDS", "sample_surprise", "FIELD_X", "a_not_b", "field_snapshot", "meta_regression"]


def _phi(z):
    return 0.5 * (1 + np.vectorize(erf)(np.asarray(z, float) / sqrt(2)))


# --------------------------------------------------------------------------------------------- looking
def habituation(n_trials: int = 14, base: float = 14.0, floor: float = 3.0, rate: float = 0.35,
                novelty: float = 0.8, seed: int = 0, noise: float = 0.15) -> dict:
    """Looks (seconds) on familiarization trials, the trial at which the criterion is met, and the first look at
    a familiar and at a novel test display.  Memory m_k = 1 - exp(-rate k); look = floor + (base - floor)(1 - m),
    with multiplicative noise.  A novel display of distance ``novelty`` (0 to 1) from the learned one restores that
    share of the lost interest."""
    rng = np.random.default_rng(seed)
    k = np.arange(n_trials)
    m = 1 - np.exp(-rate * k)
    looks = (floor + (base - floor) * (1 - m)) * np.exp(noise * rng.standard_normal(n_trials))
    crit = None
    first3 = looks[:3].mean()
    for j in range(3, n_trials - 2):
        if (looks[j:j + 3] < first3 / 2).all():
            crit = j + 2
            break
    end = crit if crit is not None else n_trials - 1
    m_end = m[end]
    familiar = floor + (base - floor) * (1 - m_end)
    novel = floor + (base - floor) * (1 - m_end * (1 - novelty))
    return {"trial": k + 1, "looks": looks, "criterion": None if crit is None else int(crit + 1),
            "first3": float(first3), "familiar": float(familiar), "novel": float(novel)}


def surprisal_trace(seq, k: int = 3, alpha: float = 1.0) -> np.ndarray:
    """Surprisal (bits) of each event in ``seq`` (ints 0..k-1) under a Dirichlet(alpha)-multinomial ideal learner."""
    counts = np.zeros(k)
    out = []
    for e in seq:
        p = (counts[e] + alpha) / (counts.sum() + k * alpha)
        out.append(-np.log2(p))
        counts[e] += 1
    return np.array(out)


KINDS = {"predictable": (0.92, 0.04, 0.04), "intermediate": (0.65, 0.25, 0.10), "random": (1 / 3, 1 / 3, 1 / 3)}


def goldilocks(n_seq: int = 400, length: int = 30, seed: int = 0, best: float = 1.1, curvature: float = 2.5,
               floor: float = 0.03, top: float = 0.35) -> dict:
    """Sequences from three boxes, ``n_seq`` of each kind in :data:`KINDS`; an observer looks away after each
    event with probability floor + (top - floor)(1 - exp(-curvature (s - best)^2)), lowest when surprisal s is near
    ``best`` bits.  Returns, binned by surprisal, the observed look-away rate, and the mean number of events
    watched for each kind of sequence."""
    rng = np.random.default_rng(seed)
    S, A = [], []
    lengths = {}
    for kind, p in KINDS.items():
        ls = []
        for i in range(n_seq):
            seq = rng.choice(3, size=length, p=p)
            s = surprisal_trace(seq)
            haz = floor + (top - floor) * (1 - np.exp(-curvature * (s - best) ** 2))
            haz[0] = floor
            look_away = rng.random(length) < haz
            S.extend(s[1:])
            A.extend(look_away[1:])
            ls.append(int(np.argmax(look_away)) + 1 if look_away.any() else length)
        lengths[kind] = float(np.mean(ls))
    S, A = np.array(S), np.array(A, float)
    edges = np.linspace(0.0, 4.0, 17)
    mid = (edges[:-1] + edges[1:]) / 2
    rate = np.array([A[(S >= a) & (S < b)].mean() if ((S >= a) & (S < b)).sum() > 30 else np.nan
                     for a, b in zip(edges[:-1], edges[1:])])
    return {"surprisal": mid, "rate": rate, "best": best, "mean_length": lengths}


# --------------------------------------------------------------------------------------------- number
WEBER = {"6 months": 0.66, "9 months": 0.41, "3 years": 0.29, "adult": 0.15}


def ans_correct(n1, n2, w):
    """Chance of judging which of two sets is larger, under Gaussian number noise with Weber fraction w."""
    n1, n2 = np.asarray(n1, float), np.asarray(n2, float)
    return _phi(np.abs(n1 - n2) / (w * np.sqrt(n1 ** 2 + n2 ** 2)))


def ratio_threshold(w: float, target: float = 0.75) -> float:
    """The ratio r (larger over smaller) told apart with probability ``target``, by bisection."""
    lo, hi = 1.0, 20.0
    for _ in range(80):
        mid = (lo + hi) / 2
        if float(ans_correct(mid, 1.0, w)) < target:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


# --------------------------------------------------------------------------------------------- statistics
def sample_surprise(p_red: float, n_red: int, n: int) -> dict:
    """The binomial probability of drawing ``n_red`` red balls in ``n`` draws from a box with share ``p_red`` red,
    and its surprisal in bits."""
    from math import comb
    p = comb(n, n_red) * p_red ** n_red * (1 - p_red) ** (n - n_red)
    return {"p": float(p), "bits": float(-np.log2(p))}


# --------------------------------------------------------------------------------------------- A not B
FIELD_X = np.linspace(-12, 12, 61)
_DX = FIELD_X[1] - FIELD_X[0]


def _g(x, mu, s):
    return np.exp(-0.5 * ((x - mu) / s) ** 2)


def _sig(u):
    return 1 / (1 + np.exp(-4.0 * u))


_K = 2.2 * _g(FIELD_X[:, None] - FIELD_X[None, :], 0, 1.6) - 0.35
_SM = _g(FIELD_X[:, None] - FIELD_X[None, :], 0, 1.0)
_SM /= np.sqrt((_SM ** 2).sum(1, keepdims=True))


def _trials(cues, h, n, delay, rng, dt=0.04, tau=1.2, noise=0.25, cue_amp=6.0, cue_dur=1.0, task=2.2, cm=1.6,
            build=0.25, record=False):
    """Run the field for ``n`` simulated infants through the hiding places ``cues``; returns the reaches
    (n x trials) and, if asked, the field over time on the last trial."""
    X = FIELD_X
    s_task = task * (_g(X, -4, 1.2) + _g(X, 4, 1.2))
    mem = np.zeros((n, len(X)))
    reaches = np.zeros((n, len(cues)))
    rec = []
    steps = int(round((cue_dur + delay) / dt))
    for j, cue in enumerate(cues):
        u = np.full((n, len(X)), h, float)
        s_cue = cue_amp * _g(X, cue, 1.2)
        for i in range(steps):
            inp = s_task + (s_cue if i * dt < cue_dur else 0.0)
            f = _sig(u)
            du = (-u + h + inp + cm * mem + (f @ _K.T) * _DX) / tau
            u = u + dt * du + noise * np.sqrt(dt / tau) * (rng.standard_normal(u.shape) @ _SM.T)
            if record and j == len(cues) - 1 and i % 5 == 0:
                rec.append(u[0].copy())
        near_a = (_sig(u) * _g(X, -4, 1.5)).sum(1) + 1e-3 * (u * _g(X, -4, 1.5)).sum(1)
        near_b = (_sig(u) * _g(X, 4, 1.5)).sum(1) + 1e-3 * (u * _g(X, 4, 1.5)).sum(1)
        reach = np.where(near_a > near_b, -4.0, 4.0)
        reaches[:, j] = reach
        mem = mem + build * (_g(X[None, :], reach[:, None], 1.2) - mem)
    return reaches, (np.array(rec) if record else None), mem


def a_not_b(h: float, delay: float, n_a: int = 6, n: int = 200, seed: int = 0) -> dict:
    """Share of simulated infants reaching to A on the B trial, and their accuracy on the A trials, for a field
    with resting level ``h`` (lower: less cooperative, younger) after ``n_a`` A trials and a ``delay`` in seconds."""
    rng = np.random.default_rng(seed)
    cues = [-4.0] * n_a + [4.0]
    r, _, _ = _trials(cues, h, n, delay, rng)
    return {"error": float((r[:, -1] == -4).mean()), "a_correct": float((r[:, :-1] == -4).mean())}


def field_snapshot(h: float, delay: float, n_a: int = 6, seed: int = 1) -> dict:
    """The field on the B trial for one simulated infant (every fifth step), and its memory trace before it."""
    rng = np.random.default_rng(seed)
    cues = [-4.0] * n_a + [4.0]
    r, rec, mem = _trials(cues, h, 1, delay, rng, record=True)
    return {"x": FIELD_X, "u": rec, "reach": float(r[0, -1]), "dt": 0.2}


# --------------------------------------------------------------------------------------------- meta-regression
def meta_regression(y, v, X) -> dict:
    """Random-effects meta-regression: y_i = X_i b + u_i + e_i, u ~ N(0, tau^2), e_i ~ N(0, v_i).  tau^2 by the
    method of moments (DerSimonian-Laird generalized), then weighted least squares with weights 1/(v + tau^2).
    ``X`` should include a column of ones.  Returns coefficients, standard errors, z and tau^2."""
    y, v, X = np.asarray(y, float), np.asarray(v, float), np.asarray(X, float)
    W = np.diag(1 / v)
    XtWX = X.T @ W @ X
    b_fe = np.linalg.solve(XtWX, X.T @ W @ y)
    Q = float((y - X @ b_fe) @ W @ (y - X @ b_fe))
    P = W - W @ X @ np.linalg.solve(XtWX, X.T @ W)
    df = len(y) - X.shape[1]
    tau2 = max(0.0, (Q - df) / float(np.trace(P)))
    W2 = np.diag(1 / (v + tau2))
    cov = np.linalg.inv(X.T @ W2 @ X)
    b = cov @ X.T @ W2 @ y
    se = np.sqrt(np.diag(cov))
    return {"b": b, "se": se, "z": b / se, "tau2": float(tau2), "Q": Q, "df": df}
