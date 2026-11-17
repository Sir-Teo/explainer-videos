"""Psychophysics: thresholds, scales and the methods that measure them (videos/psychology/SYLLABUS.md, Part 11).

**The observer.**  A stimulus of intensity ``I`` arrives in the head as a noisy number, ``I + e`` with
``e ~ N(0, sigma(I)^2)`` and

    sigma(I)^2 = sigma0^2 + (k I)^2 ,

a fixed floor (``sigma0``) plus noise that grows in proportion to the signal (``k``).  In a two-alternative trial
(which of two patches is brighter?) the observer picks the interval with the larger number, so it is right with
probability ``Phi(Delta / sqrt(sigma(I)^2 + sigma(I + Delta)^2))``, about ``Phi(d' / sqrt 2)`` with ``d' = Delta / sigma(I)``.
It also lapses (presses at random) on a share ``lapse`` of trials.  Far above the floor the just noticeable
difference is a fixed fraction of ``I``: Weber's law.  Near the floor the fraction grows: the law's known failure.
An optional ``near_miss`` exponent lets ``k`` fall slowly with level, as it does for the loudness of tones.

**The psychometric function** in its usual four parameters, for a stimulus level ``x``,

    psi(x) = gamma + (1 - gamma - lam) F(x; alpha, beta),

with ``F`` a cumulative Gaussian, a logistic or a Weibull, ``alpha`` the threshold, ``beta`` the slope, ``gamma``
the guess rate (0.5 in two-alternative forced choice) and ``lam`` the lapse rate.

**The methods.**  Fechner's three classical methods (limits, adjustment, constant stimuli); maximum-likelihood
fitting of the psychometric function with a parametric bootstrap (Wichmann and Hill 2001); the transformed
up-down staircases (Levitt 1971: a k-down 1-up rule converges where p^k = 1/2); a QUEST-style Bayesian placement of
each trial (Watson and Pelli 1983).

**The scales.**  Fechner's integral of Weber's fraction (``S = log(I/I0) / log(1 + w)`` in units of JNDs);
Stevens's power law (``S = c I^a``) with simulated magnitude estimation and cross-modality matching.

Nothing here imports manim.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
from scipy import optimize, stats

__all__ = ["Observer", "psychometric", "fit", "bootstrap", "constant_stimuli", "method_of_limits",
           "method_of_adjustment", "staircase", "updown_target", "quest", "jnd", "weber_fractions", "fechner",
           "stevens", "magnitude_estimation", "fit_power", "cross_modality", "STEVENS_EXPONENTS", "two_afc"]

Z75 = stats.norm.ppf(0.75)

# Stevens's table of exponents, as it is reproduced in textbooks (Stevens 1957, 1975): (continuum, exponent, stimulus)
STEVENS_EXPONENTS = (
    ("brightness", 0.33, "a 5-degree target in the dark"),
    ("loudness", 0.67, "sound pressure of a 3,000 Hz tone"),
    ("vibration", 0.95, "amplitude of 60 Hz on a finger"),
    ("visual length", 1.0, "a line projected on a screen"),
    ("heaviness", 1.45, "lifted weights"),
    ("electric shock", 3.5, "current through the fingers"),
)


# ----------------------------------------------------------------------------------------------- the observer
@dataclass(frozen=True)
class Observer:
    """A noisy observer of intensity.  ``k`` is Weber's fraction of the noise, ``sigma0`` the noise floor,
    ``lapse`` the share of random presses, ``near_miss`` an exponent by which ``k`` falls with level
    (``k(I) = k (I / ref)^(-near_miss)``), and ``poisson`` a variance that grows in proportion to intensity, as a
    count of photons or spikes does (the de Vries-Rose regime, where the JND grows as the square root)."""

    k: float = 0.08
    sigma0: float = 0.5
    lapse: float = 0.02
    near_miss: float = 0.0
    ref: float = 100.0
    poisson: float = 0.0

    def sigma(self, intensity) -> np.ndarray:
        i = np.asarray(intensity, dtype=float)
        k = self.k * (np.maximum(i, 1e-12) / self.ref) ** (-self.near_miss)
        return np.sqrt(self.sigma0 ** 2 + self.poisson * np.maximum(i, 0.0) + (k * i) ** 2)

    def p_correct(self, standard, delta) -> np.ndarray:
        """Two-alternative forced choice: the chance of picking the more intense of ``standard`` and
        ``standard + delta`` (``delta`` may be negative; the observer is then asked for the weaker)."""
        d = np.abs(np.asarray(delta, dtype=float))
        spread = np.sqrt(self.sigma(standard) ** 2 + self.sigma(np.asarray(standard, dtype=float) + d) ** 2)
        p = stats.norm.cdf(d / spread)
        return 0.5 * self.lapse + (1 - self.lapse) * p

    def respond(self, standard: float, delta: float, rng) -> bool:
        """One simulated 2AFC trial: True if correct."""
        if rng.random() < self.lapse:
            return bool(rng.random() < 0.5)
        s = float(self.sigma(standard))
        a = standard + s * rng.standard_normal()
        b = standard + abs(delta) + float(self.sigma(standard + abs(delta))) * rng.standard_normal()
        return bool(b > a)

    def says_more(self, standard: float, comparison: float, rng, criterion: float = 1.0) -> bool:
        """Yes-no: does the comparison look noticeably more intense than the standard?  The observer says yes when
        the difference of the two impressions exceeds ``criterion`` standard deviations of that difference, so
        with no increment it says yes on 1 - Phi(criterion) of trials.  (No lapses: used by the classical methods.)"""
        a = standard + float(self.sigma(standard)) * rng.standard_normal()
        b = comparison + float(self.sigma(comparison)) * rng.standard_normal()
        spread = math.sqrt(float(self.sigma(standard)) ** 2 + float(self.sigma(comparison)) ** 2)
        return bool(b - a > criterion * spread)


def jnd(observer: Observer, standard, criterion: float = 0.75) -> np.ndarray:
    """The increment a lapse-free version of ``observer`` detects on ``criterion`` of 2AFC trials (by default 75%,
    at d' = sqrt(2) z(0.75)), using the noise at the standard."""
    z = stats.norm.ppf(criterion)
    return math.sqrt(2.0) * z * observer.sigma(standard)


def weber_fractions(observer: Observer, standards) -> np.ndarray:
    """JND / I at each standard: flat where Weber's law holds, rising near the floor."""
    s = np.asarray(standards, dtype=float)
    return jnd(observer, s) / s


def two_afc(standard: float, deltas, observer: Observer, n_per: int, rng) -> dict:
    """A block of 2AFC trials at fixed increments: the Battery's threshold task.  Returns per-trial arrays."""
    deltas = np.asarray(deltas, dtype=float)
    level = np.repeat(deltas, n_per)
    rng.shuffle(level)
    correct = np.array([observer.respond(standard, d, rng) for d in level])
    return {"delta": level, "correct": correct}


# ----------------------------------------------------------------------------------------------- the function
def _core(x, alpha, beta, form):
    x = np.asarray(x, dtype=float)
    if form == "gauss":
        return stats.norm.cdf((x - alpha) / beta)
    if form == "logistic":
        return 1.0 / (1.0 + np.exp(-(x - alpha) / beta))
    if form == "weibull":
        xx = np.maximum(x, 0.0)
        return 1.0 - np.exp(-(xx / alpha) ** beta)
    raise ValueError(form)


def psychometric(x, alpha: float, beta: float, gamma: float = 0.5, lam: float = 0.0, form: str = "gauss"):
    """psi(x) = gamma + (1 - gamma - lam) F(x; alpha, beta)."""
    return gamma + (1 - gamma - lam) * _core(x, alpha, beta, form)


def _nll(params, x, k, n, gamma, form, fixed_lam):
    alpha, log_beta = params[0], params[1]
    lam = fixed_lam if fixed_lam is not None else params[2]
    if fixed_lam is None and not (0.0 <= lam <= 0.1):
        return 1e12
    if form == "weibull" and alpha <= 0:
        return 1e12
    p = np.clip(psychometric(x, alpha, math.exp(log_beta), gamma, lam, form), 1e-9, 1 - 1e-9)
    return -float(np.sum(k * np.log(p) + (n - k) * np.log(1 - p)))


def fit(x, k, n, gamma: float = 0.5, form: str = "gauss", lam: float | None = None, start=None) -> dict:
    """Maximum likelihood fit of the psychometric function to ``k`` successes of ``n`` trials at levels ``x``.
    ``lam`` fixes the lapse rate; None fits it (bounded to [0, 0.1], as Wichmann and Hill advise).  Returns alpha,
    beta, lam, the log-likelihood and the deviance against the saturated model."""
    x, k, n = (np.asarray(v, dtype=float) for v in (x, k, n))
    if start is None:
        a0 = float(np.median(x)) if form != "weibull" else float(np.median(x[x > 0]) if np.any(x > 0) else 1.0)
        b0 = float(np.std(x)) / 2 if form != "weibull" else 2.0
        start = [a0, math.log(max(b0, 1e-3))] + ([] if lam is not None else [0.01])
    best = None
    for jitter in (1.0, 0.6, 1.6):
        s = list(start)
        s[0] *= jitter
        r = optimize.minimize(_nll, s, args=(x, k, n, gamma, form, lam), method="Nelder-Mead",
                              options={"xatol": 1e-7, "fatol": 1e-9, "maxiter": 6000})
        if best is None or r.fun < best.fun:
            best = r
    alpha, beta = float(best.x[0]), float(math.exp(best.x[1]))
    lam_hat = float(lam if lam is not None else best.x[2])
    ll = -float(best.fun)
    p_sat = np.clip(k / n, 1e-9, 1 - 1e-9)
    ll_sat = float(np.sum(k * np.log(p_sat) + (n - k) * np.log(1 - p_sat)))
    return {"alpha": alpha, "beta": beta, "lam": lam_hat, "gamma": gamma, "form": form, "loglik": ll,
            "deviance": 2 * (ll_sat - ll), "lam_free": lam is None}


def threshold_at(fitted: dict, p: float) -> float:
    """The level at which the fitted function reaches ``p`` (between gamma and 1 - lam)."""
    g, lam = fitted["gamma"], fitted["lam"]
    q = (p - g) / (1 - g - lam)
    a, b, form = fitted["alpha"], fitted["beta"], fitted["form"]
    if form == "gauss":
        return a + b * stats.norm.ppf(q)
    if form == "logistic":
        return a + b * math.log(q / (1 - q))
    return a * (-math.log(1 - q)) ** (1 / b)


def bootstrap(x, k, n, fitted: dict, n_boot: int = 1000, rng=None, p_target: float = 0.75) -> dict:
    """Parametric bootstrap: refit to binomial counts drawn from the fitted function; percentile intervals for
    the threshold (the level at ``p_target``) and the slope parameter."""
    rng = rng or np.random.default_rng(0)
    x, n = np.asarray(x, dtype=float), np.asarray(n, dtype=int)
    p = psychometric(x, fitted["alpha"], fitted["beta"], fitted["gamma"], fitted["lam"], fitted["form"])
    lam = None if fitted.get("lam_free", True) else fitted["lam"]
    th, sl, dev = [], [], []
    for _ in range(n_boot):
        kb = rng.binomial(n, p)
        f = fit(x, kb, n, fitted["gamma"], fitted["form"], lam=lam,
                start=[fitted["alpha"], math.log(fitted["beta"])] + ([] if lam is not None else [max(fitted["lam"], 0.005)]))
        th.append(threshold_at(f, p_target))
        sl.append(f["beta"])
        dev.append(f["deviance"])
    th, sl, dev = np.array(th), np.array(sl), np.array(dev)
    # goodness of fit (Wichmann and Hill's part I): how often a curve that really is the fitted one gives counts
    # that fit worse than the data did
    p_fit = float(np.mean(dev >= fitted["deviance"])) if "deviance" in fitted else float("nan")
    return {"threshold": th, "beta": sl, "threshold_ci": np.percentile(th, [2.5, 97.5]),
            "beta_ci": np.percentile(sl, [2.5, 97.5]), "deviance": dev, "p_fit": p_fit}


# ----------------------------------------------------------------------------------------------- the methods
def constant_stimuli(observer: Observer, standard: float, deltas, n_per: int, rng) -> dict:
    """Fechner's 'right and wrong cases': every increment ``n_per`` times, in random order (2AFC)."""
    t = two_afc(standard, deltas, observer, n_per, rng)
    deltas = np.asarray(deltas, dtype=float)
    k = np.array([int(t["correct"][t["delta"] == d].sum()) for d in deltas])
    return {"delta": deltas, "k": k, "n": np.full(len(deltas), n_per), "trials": t}


def method_of_limits(observer: Observer, standard: float, top: float, step: float, n_series: int, rng,
                     criterion: float = 1.0) -> dict:
    """Fechner's 'just noticeable differences': series of comparisons, alternately descending from ``standard +
    top`` until the observer stops saying 'more', and ascending from the standard until it starts.  The
    threshold is the mean of the transition points: the 50% point of 'yes, more', which depends on the
    observer's ``criterion`` as well as on its sensitivity (the problem signal detection theory solves, Part 12)."""
    levels = np.arange(0.0, top + 1e-9, step)
    points, series = [], []
    for s in range(n_series):
        order = levels[::-1] if s % 2 == 0 else levels
        answers = []
        for d in order:
            more = observer.says_more(standard, standard + d, rng, criterion)
            answers.append(more)
            if (s % 2 == 0 and not more) or (s % 2 == 1 and more):
                break
        last = order[len(answers) - 1]
        prev = order[len(answers) - 2] if len(answers) > 1 else last
        points.append(0.5 * (last + prev))
        series.append((order[:len(answers)], np.array(answers)))
    points = np.array(points)
    return {"points": points, "threshold": float(points.mean()), "descending": float(points[::2].mean()),
            "ascending": float(points[1::2].mean()) if n_series > 1 else float("nan"), "series": series}


def method_of_adjustment(observer: Observer, standard: float, n: int, rng, start_spread: float = 0.3) -> dict:
    """Fechner's 'average error': the observer turns a knob until the comparison matches the standard.  Each
    setting is where the two noisy impressions cross; its spread is proportional to the JND, and its mean is the
    point of subjective equality."""
    settings = []
    for _ in range(n):
        settings.append(standard + float(observer.sigma(standard)) * math.sqrt(2.0) * rng.standard_normal())
    settings = np.array(settings)
    return {"settings": settings, "pse": float(settings.mean()), "sd": float(settings.std(ddof=1)),
            "jnd_from_sd": float(settings.std(ddof=1) * Z75)}


def updown_target(k_down: int) -> float:
    """The proportion correct a k-down 1-up staircase converges to: p^k = 1/2."""
    return 0.5 ** (1.0 / k_down)


def staircase(observer: Observer, standard: float, start: float, factor: float = 1.25, k_down: int = 2,
              n_trials: int = 80, rng=None, n_reversals_used: int = 8) -> dict:
    """A k-down 1-up staircase on the increment, in multiplicative steps (``factor``): k correct in a row makes
    the next trial harder, one error makes it easier.  The estimate is the geometric mean of the last
    ``n_reversals_used`` reversal levels."""
    rng = rng or np.random.default_rng(0)
    level, run, direction = start, 0, 0
    levels, correct, reversals = [], [], []
    for _ in range(n_trials):
        ok = observer.respond(standard, level, rng)
        levels.append(level)
        correct.append(ok)
        if ok:
            run += 1
            if run == k_down:
                run = 0
                if direction == +1:
                    reversals.append(level)
                direction = -1
                level /= factor
        else:
            run = 0
            if direction == -1:
                reversals.append(level)
            direction = +1
            level *= factor
    rev = np.array(reversals)
    use = rev[-n_reversals_used:] if len(rev) >= 2 else np.array(levels[-10:])
    return {"levels": np.array(levels), "correct": np.array(correct), "reversals": rev,
            "estimate": float(np.exp(np.mean(np.log(use))))}


def quest(observer: Observer, standard: float, n_trials: int = 40, rng=None, grid=None, beta: float = 3.5,
          prior_mean: float = None, prior_sd: float = 1.0, p_target: float = 0.82, lam: float = 0.02) -> dict:
    """A QUEST-style Bayesian staircase (after Watson and Pelli 1983).  The unknown is the log threshold ``t``; the
    assumed function is a Weibull in the increment with slope ``beta``, guess 0.5 and lapse ``lam``.  Each trial is
    placed at the posterior mean, the response updates the posterior on a grid, and the final estimate is the
    posterior mean with its standard deviation."""
    rng = rng or np.random.default_rng(0)
    if grid is None:
        grid = np.linspace(math.log(standard * 0.002 + 1e-6), math.log(standard * 2.0 + 1.0), 401)
    if prior_mean is None:
        prior_mean = float(np.mean(grid))
    logpost = stats.norm.logpdf(grid, prior_mean, prior_sd)
    # the Weibull is placed so that p(threshold) = p_target
    q = (p_target - 0.5) / (1 - 0.5 - lam)
    shift = (-math.log(1 - q)) ** (1 / beta)
    placed, correct, means, sds = [], [], [], []
    for _ in range(n_trials):
        w = np.exp(logpost - logpost.max())
        w /= w.sum()
        m = float(np.sum(w * grid))
        x = math.exp(m)
        ok = observer.respond(standard, x, rng)
        alpha = np.exp(grid) / shift
        p = 0.5 + (0.5 - lam) * (1 - np.exp(-(x / alpha) ** beta))
        logpost += np.log(p if ok else 1 - p)
        placed.append(x)
        correct.append(ok)
        w = np.exp(logpost - logpost.max())
        w /= w.sum()
        mm = float(np.sum(w * grid))
        means.append(math.exp(mm))
        sds.append(float(math.sqrt(np.sum(w * (grid - mm) ** 2))))
    return {"placed": np.array(placed), "correct": np.array(correct), "estimate": means[-1],
            "estimates": np.array(means), "log_sd": np.array(sds), "grid": grid, "posterior": w}


# ----------------------------------------------------------------------------------------------- the scales
def fechner(intensity, i0: float, w: float) -> np.ndarray:
    """Sensation in JND steps above the absolute threshold ``i0``, if every JND is one unit and each is the
    fraction ``w`` of the intensity below it: S = log(I / I0) / log(1 + w).  (For small ``w`` this is
    (1 / w) ln(I / I0), Fechner's law.)"""
    i = np.asarray(intensity, dtype=float)
    return np.log(i / i0) / math.log(1.0 + w)


def stevens(intensity, a: float, c: float = 1.0) -> np.ndarray:
    """Stevens's power law: S = c I^a."""
    return c * np.asarray(intensity, dtype=float) ** a


def magnitude_estimation(intensities, a: float, n_people: int, rng, noise: float = 0.25, c: float = 10.0,
                         person_sd: float = 0.15) -> dict:
    """Simulated magnitude estimation: each person reports c_p I^a_p times log-normal noise, with exponents that
    differ a little between people (``person_sd``).  The group's geometric means are what Stevens plotted."""
    i = np.asarray(intensities, dtype=float)
    a_p = a * np.exp(person_sd * rng.standard_normal(n_people))
    c_p = c * np.exp(0.3 * rng.standard_normal(n_people))
    reports = c_p[:, None] * i[None, :] ** a_p[:, None] * np.exp(noise * rng.standard_normal((n_people, len(i))))
    geo = np.exp(np.log(reports).mean(axis=0))
    return {"intensity": i, "reports": reports, "geometric_mean": geo, "exponents": a_p}


def fit_power(intensity, response) -> dict:
    """Least squares on log-log axes: slope = exponent."""
    lx, ly = np.log(np.asarray(intensity, float)), np.log(np.asarray(response, float))
    slope, intercept = np.polyfit(lx, ly, 1)
    return {"exponent": float(slope), "c": float(math.exp(intercept))}


def cross_modality(a_matched: float, a_adjusted: float) -> float:
    """If sensations follow power laws, matching the strength of continuum 1 by adjusting continuum 2 gives a
    power law between the two physical intensities with exponent a_matched / a_adjusted."""
    return a_matched / a_adjusted


# ------------------------------------------------------------------------------- the triangle test (industry)
def triangle_critical(n: int, alpha: float = 0.05, guess: float = 1.0 / 3.0) -> int:
    """The smallest number of correct answers out of ``n`` that a one-sided exact binomial test calls a difference
    at level ``alpha``, when guessing picks the odd sample with chance ``guess`` (1/3 for three samples)."""
    for c in range(n + 1):
        if stats.binom.sf(c - 1, n, guess) <= alpha:
            return c
    return n + 1


def triangle_power(n: int, distinguishers: float, alpha: float = 0.05, guess: float = 1.0 / 3.0) -> float:
    """The chance that a panel of ``n`` finds the difference when a share ``distinguishers`` of tasters really can
    tell (they answer right; everyone else guesses): p = d + (1 - d) guess."""
    p = distinguishers + (1 - distinguishers) * guess
    return float(stats.binom.sf(triangle_critical(n, alpha, guess) - 1, n, p))


# ------------------------------------------------------------------ Thurstone: a scale with no physical stimulus
def paired_comparisons(values, n_judges: int, rng, sd: float = 1.0) -> np.ndarray:
    """Every judge compares every ordered pair once: item i is judged above item j when its impression,
    ``values[i]`` plus normal noise of ``sd``, exceeds j's.  Returns the share of judges preferring i over j."""
    v = np.asarray(values, dtype=float)
    m = len(v)
    wins = np.zeros((m, m))
    for _ in range(n_judges):
        imp = v[:, None] + sd * rng.standard_normal((m, m))
        wins += imp > imp.T
    p = wins / n_judges
    np.fill_diagonal(p, 0.5)
    return p


def thurstone_case_v(p, clip: float = 0.02) -> np.ndarray:
    """Thurstone's Case V: turn each proportion into a normal deviate and average across columns.  The result is
    a scale in units of the standard deviation of a difference, centred at zero."""
    z = stats.norm.ppf(np.clip(np.asarray(p, dtype=float), clip, 1 - clip))
    s = z.mean(axis=1)
    return s - s.mean()
