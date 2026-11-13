"""The laboratory of *Psychology, Built*: designs as objects, run on the Pool (videos/psychology/SYLLABUS.md, Part 2).

    from explainer.psychology import lab, pool
    L = lab.Lab(pool.Pool())
    L.randomized(n=200, effect=0.0)            # a randomized experiment on a treatment that does nothing
    L.pre_post(n=200)                          # the same treatment "works" in a study with no comparison group
    lab.williams(4)                            # a counterbalanced order for four conditions

A design answers three questions: who gets what (assignment), in what order (counterbalancing), and what is
compared with what (the analysis).  The first part of this module is those three, as plain functions on arrays.
The second, :class:`Lab`, runs designs on the Pool, where the truth is known because we wrote it: the outcome is a
person's mean simple reaction time in a session (:meth:`explainer.psychology.pool.Pool.session_rt`), and the
"treatment" has whatever true effect the caller plants, zero by default.  Each unsound design of Campbell and
Stanley's list (selection, history, maturation, testing, regression to the mean, attrition) is one method, and
each returns the effect a study of that design would report.

Everything from the Pool is simulated; it shows what a design does, and is never evidence about people.
Nothing here imports manim.
"""

from __future__ import annotations

import itertools
import math
from dataclasses import dataclass

import numpy as np
from scipy import stats

__all__ = ["Estimate", "randomize", "alternate", "balance", "difference", "paired", "randomization_test",
           "latin_square", "williams", "all_orders", "position_counts", "power_two_group", "power_paired",
           "n_two_group", "n_paired", "interaction_2x2", "Lab", "THREATS", "alternation_rate", "longest_run",
           "predict_presses", "human_like_sequence"]


# ---------------------------------------------------------------------------
# Results
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class Estimate:
    """What a study reports: an effect, its standard error and degrees of freedom."""

    effect: float
    se: float
    df: float
    n: int
    label: str = ""

    @property
    def t(self) -> float:
        return self.effect / self.se if self.se > 0 else float("nan")

    @property
    def p(self) -> float:
        return float(2 * stats.t.sf(abs(self.t), self.df))

    def ci(self, level: float = 0.95) -> tuple:
        h = stats.t.ppf(0.5 + level / 2, self.df) * self.se
        return self.effect - h, self.effect + h

    def as_dict(self) -> dict:
        lo, hi = self.ci()
        return {"effect": self.effect, "se": self.se, "df": self.df, "n": self.n, "t": self.t, "p": self.p,
                "lo": lo, "hi": hi, "label": self.label}


# ---------------------------------------------------------------------------
# Who gets what
# ---------------------------------------------------------------------------
def randomize(n: int, k: int = 2, rng=None) -> np.ndarray:
    """A balanced random assignment of ``n`` units to ``k`` groups (labels 0..k-1): a shuffled deck, as Peirce and
    Jastrow shuffled theirs in 1884."""
    rng = np.random.default_rng() if rng is None else rng
    deck = np.arange(n) % k
    rng.shuffle(deck)
    return deck


def alternate(n: int, k: int = 2) -> np.ndarray:
    """Assignment in turn (0, 1, 0, 1, ...): balanced, and not random.  Whatever goes with arrival order goes with
    the groups."""
    return np.arange(n) % k


def balance(x, groups) -> float:
    """The standardized difference of a covariate between group 1 and group 0 (difference of means over the
    pooled standard deviation)."""
    x, groups = np.asarray(x, dtype=float), np.asarray(groups)
    a, b = x[groups == 1], x[groups == 0]
    s = math.sqrt((a.var(ddof=1) + b.var(ddof=1)) / 2)
    return float((a.mean() - b.mean()) / s)


# ---------------------------------------------------------------------------
# What is compared with what
# ---------------------------------------------------------------------------
def difference(y, groups, label: str = "") -> Estimate:
    """Group 1 minus group 0, with Welch's standard error and degrees of freedom."""
    y, groups = np.asarray(y, dtype=float), np.asarray(groups)
    a, b = y[groups == 1], y[groups == 0]
    va, vb = a.var(ddof=1) / len(a), b.var(ddof=1) / len(b)
    df = (va + vb) ** 2 / (va ** 2 / (len(a) - 1) + vb ** 2 / (len(b) - 1))
    return Estimate(float(a.mean() - b.mean()), math.sqrt(va + vb), float(df), len(y), label)


def paired(after, before, label: str = "") -> Estimate:
    """The mean of the within-person differences ``after - before``."""
    d = np.asarray(after, dtype=float) - np.asarray(before, dtype=float)
    return Estimate(float(d.mean()), float(d.std(ddof=1) / math.sqrt(len(d))), len(d) - 1.0, len(d), label)


def randomization_test(y, groups, n_perm: int = 10_000, rng=None) -> dict:
    """Fisher's test of "the treatment did nothing to anyone": reshuffle the labels, and see how often a
    difference as large as the observed one arises from the shuffling alone.  Returns the observed difference,
    the two-sided p value, and the shuffled differences."""
    rng = np.random.default_rng(0) if rng is None else rng
    y, groups = np.asarray(y, dtype=float), np.asarray(groups)
    n1 = int((groups == 1).sum())
    total, n = y.sum(), len(y)
    obs = y[groups == 1].mean() - y[groups == 0].mean()
    idx = np.argsort(rng.random((n_perm, n)), axis=1)[:, :n1]
    s1 = y[idx].sum(axis=1)
    d = s1 / n1 - (total - s1) / (n - n1)
    p = (np.sum(np.abs(d) >= abs(obs) - 1e-12) + 1) / (n_perm + 1)
    return {"observed": float(obs), "p": float(p), "null": d}


# ---------------------------------------------------------------------------
# In what order
# ---------------------------------------------------------------------------
def latin_square(k: int) -> np.ndarray:
    """The cyclic ``k`` by ``k`` Latin square: row r is the order of conditions for the r-th group of subjects.
    Every condition appears once in every position."""
    return (np.arange(k)[:, None] + np.arange(k)[None, :]) % k


def williams(k: int) -> np.ndarray:
    """A Williams design: a Latin square in which every condition also follows every other condition equally
    often, so that first-order carry-over is balanced.  ``k`` rows for even ``k``, ``2k`` for odd."""
    first = [0]
    lo, hi = 1, k - 1
    while len(first) < k:
        first.append(lo)
        lo += 1
        if len(first) < k:
            first.append(hi)
            hi -= 1
    sq = (np.array(first)[None, :] + np.arange(k)[:, None]) % k
    return sq if k % 2 == 0 else np.vstack([sq, sq[:, ::-1]])


def all_orders(k: int) -> np.ndarray:
    """Complete counterbalancing: all ``k!`` orders."""
    return np.array(list(itertools.permutations(range(k))))


def position_counts(orders) -> dict:
    """How well a set of orders is balanced: ``position[c, j]`` counts condition c in position j, and
    ``follows[c, d]`` counts how often c comes immediately after d."""
    orders = np.asarray(orders)
    k = orders.max() + 1
    position = np.zeros((k, orders.shape[1]), dtype=int)
    follows = np.zeros((k, k), dtype=int)
    for row in orders:
        for j, c in enumerate(row):
            position[c, j] += 1
            if j:
                follows[c, row[j - 1]] += 1
    return {"position": position, "follows": follows}


# ---------------------------------------------------------------------------
# How many people
# ---------------------------------------------------------------------------
def power_two_group(d: float, n_per_group: int, alpha: float = 0.05) -> float:
    """Power of a two-sided test of two independent groups for a standardized effect ``d`` (normal
    approximation): the noncentrality is ``d sqrt(n / 2)``."""
    z, ncp = stats.norm.ppf(1 - alpha / 2), abs(d) * math.sqrt(n_per_group / 2)
    return float(stats.norm.sf(z - ncp) + stats.norm.cdf(-z - ncp))


def power_paired(d: float, n: int, rho: float, alpha: float = 0.05) -> float:
    """Power when the same ``n`` people serve in both conditions and their two scores correlate ``rho``: the
    difference has standard deviation ``sqrt(2 (1 - rho))`` in units of the score's, so the noncentrality is
    ``d sqrt(n / (2 (1 - rho)))``."""
    z, ncp = stats.norm.ppf(1 - alpha / 2), abs(d) * math.sqrt(n / (2 * (1 - rho)))
    return float(stats.norm.sf(z - ncp) + stats.norm.cdf(-z - ncp))


def n_two_group(d: float, power: float = 0.8, alpha: float = 0.05) -> int:
    """People per group for the given power (normal approximation)."""
    z = stats.norm.ppf(1 - alpha / 2) + stats.norm.ppf(power)
    return int(math.ceil(2 * (z / d) ** 2))


def n_paired(d: float, rho: float, power: float = 0.8, alpha: float = 0.05) -> int:
    """People in all for a within-person design with correlation ``rho`` between a person's two scores."""
    z = stats.norm.ppf(1 - alpha / 2) + stats.norm.ppf(power)
    return int(math.ceil(2 * (1 - rho) * (z / d) ** 2))


def interaction_2x2(m) -> float:
    """The interaction contrast of a 2 by 2 table of means ``m[a][b]``: the effect of B at A = 1 minus its effect
    at A = 0.  Zero when the two factors add."""
    m = np.asarray(m, dtype=float)
    return float((m[1, 1] - m[1, 0]) - (m[0, 1] - m[0, 0]))


# ---------------------------------------------------------------------------
# Why the shuffling is left to a deck of cards: people asked to be random
# ---------------------------------------------------------------------------
def alternation_rate(seq) -> float:
    """The share of presses that differ from the one before.  A fair coin gives one half."""
    seq = np.asarray(seq)
    return float(np.mean(seq[1:] != seq[:-1]))


def longest_run(seq) -> int:
    """The length of the longest run of the same symbol."""
    seq = np.asarray(seq)
    best = run = 1
    for a, b in zip(seq[:-1], seq[1:]):
        run = run + 1 if a == b else 1
        best = max(best, run)
    return best


def predict_presses(seq, depth: int = 3) -> dict:
    """Guess each press of a two-key sequence before it is made, from the presses so far: find the longest recent
    context (up to ``depth`` presses) after which one key has led the other by at least two, and bet on that key;
    with nothing to go on, bet that the person will switch keys.  This is the predictor of the Part 2 interactive
    (after the "mind-reading machines" of Hagelbarger and Shannon, 1953).  Returns the share of presses guessed
    and the guesses."""
    seq = [int(x) for x in seq]
    counts: dict = {}
    guesses, hits = [], 0
    for i, x in enumerate(seq):
        guess = None
        for k in range(min(depth, i), 0, -1):
            c = counts.get(tuple(seq[i - k:i]))
            if c and abs(c[0] - c[1]) >= 2:  # trust a context only once it has leaned one way by two
                guess = int(c[1] > c[0])
                break
        if guess is None:
            guess = 1 - seq[i - 1] if i else 0
        guesses.append(guess)
        hits += guess == x
        for k in range(1, min(depth, i) + 1):
            counts.setdefault(tuple(seq[i - k:i]), [0, 0])[x] += 1
    return {"accuracy": hits / len(seq), "guesses": guesses}


def human_like_sequence(n: int, p_alternate: float = 0.6, rng=None) -> np.ndarray:
    """A two-key sequence from a generator that switches keys with probability ``p_alternate``: the simplest model
    of a person trying to be random (people switch too often; about 0.6 in Falk and Konold's 1997 review).  At
    0.5 it is a fair coin."""
    rng = np.random.default_rng() if rng is None else rng
    switch = rng.random(n) < p_alternate
    switch[0] = rng.random() < 0.5
    return np.cumsum(switch) % 2


# ---------------------------------------------------------------------------
# Designs on the Pool
# ---------------------------------------------------------------------------
THREATS = ("selection", "history", "maturation", "testing", "regression", "attrition")


class Lab:
    """Studies of one treatment on the Pool.  The outcome is the mean simple reaction time of a session, in ms,
    so a treatment that helps has a *negative* effect.  ``effect`` is the true effect planted for the study (0:
    the treatment does nothing), and every method returns the :class:`Estimate` its design would publish."""

    def __init__(self, pool, seed: int = 0, n_trials: int = 20):
        self.pool, self.seed, self.n_trials = pool, seed, n_trials

    def _rng(self, *key) -> np.random.Generator:
        return np.random.Generator(np.random.PCG64([self.pool.seed, 29, self.seed, *key]))

    def _rt(self, ids, session, key, shift=0.0):
        return self.pool.session_rt(ids, session=session, n_trials=self.n_trials, seed=self.seed * 1000 + key,
                                    shift=shift)

    # --- the sound design ------------------------------------------------
    def randomized(self, n: int = 200, effect: float = 0.0, study: int = 0, pretest: bool = False) -> Estimate:
        """A randomized experiment with a control group: ``n`` people, half of them treated by the shuffle of a
        deck, everyone measured once after the treatment (and once before, if ``pretest``, in which case the
        comparison is of the changes)."""
        ids = self.pool.sample(n, seed=self.seed * 7919 + study)
        g = randomize(n, 2, self._rng(1, study))
        post = self._rt(ids, 1 if pretest else 0, 100 + study, shift=effect * g)
        if not pretest:
            return difference(post, g, "randomized, with a control group")
        pre = self._rt(ids, 0, 200 + study)
        return difference(post - pre, g, "randomized, pretest and posttest")

    # --- six ways to be fooled, each with the truth known ------------------
    def selection(self, n: int = 200, effect: float = 0.0, study: int = 0) -> Estimate:
        """The treated are the people who signed up; the comparison group is everyone else.  In the Pool the keen
        are younger and quicker, so the groups differed before anything was done to them."""
        ids = self.pool.sample(4 * n, seed=self.seed * 7919 + 10_000 + study)
        keen = self.pool.keen[ids]
        order = np.argsort(-(keen + 0.5 * self._rng(2, study).standard_normal(len(ids))))
        treated, others = ids[order[: n // 2]], ids[order[len(ids) - n // 2:]]
        y = np.concatenate([self._rt(treated, 0, 300 + study, shift=effect), self._rt(others, 0, 400 + study)])
        g = np.concatenate([np.ones(n // 2, dtype=int), np.zeros(n // 2, dtype=int)])
        return difference(y, g, "volunteers against the rest")

    def pre_post(self, n: int = 200, effect: float = 0.0, study: int = 0, history: float = 0.0) -> Estimate:
        """One group, measured before and after the treatment.  Practice at the task makes the second measurement
        faster whatever happened in between (*testing*); ``history`` is anything else that happened to everyone
        between the two sessions, in ms."""
        ids = self.pool.sample(n, seed=self.seed * 7919 + 20_000 + study)
        pre = self._rt(ids, 0, 500 + study)
        post = self._rt(ids, 1, 600 + study, shift=effect + history)
        return paired(post, pre, "one group, before and after")

    def testing(self, n: int = 200, effect: float = 0.0, study: int = 0) -> Estimate:
        return self.pre_post(n, effect, study)

    def history(self, n: int = 200, effect: float = 0.0, study: int = 0, shock: float = -6.0) -> Estimate:
        """Before and after, with something else happening in between to everyone: here the laboratory replaced
        its keyboards with faster ones (``shock`` ms).  The estimate also carries the practice effect; the
        method reports the part the shock adds by itself."""
        with_shock = self.pre_post(n, effect, study, history=shock)
        without = self.pre_post(n, effect, study)
        return Estimate(with_shock.effect - without.effect, with_shock.se, with_shock.df, n,
                        "something else changed in between")

    def maturation(self, n: int = 200, effect: float = 0.0, study: int = 0, months: float = 24.0,
                   age_range=(8, 12), ms_per_year: float = -22.0) -> Estimate:
        """Before and after, in people who are changing anyway.  The Pool's adults barely change in two years, so
        this study is run on children, whose reactions quicken by about ``ms_per_year`` each year (an
        illustrative figure): the growth is credited to the treatment."""
        rng = self._rng(3, study)
        ids = self.pool.sample(n, seed=self.seed * 7919 + 30_000 + study)
        ages = rng.uniform(*age_range, size=n)
        child = (ages - 18.0) * ms_per_year  # slower than their adult selves by this much, to first order
        pre = self._rt(ids, 0, 700 + study, shift=child)
        grown = (ages + months / 12.0 - 18.0) * ms_per_year
        # sessions two years apart: practice has faded, so both count as first sessions
        post = self._rt(ids, 0, 800 + study, shift=grown + effect)
        return paired(post, pre, "children, two years apart")

    def regression(self, n: int = 200, effect: float = 0.0, study: int = 0, screened: int = 2000,
                   washout: bool = True) -> Estimate:
        """Screen ``screened`` people, enrol the ``n`` slowest, treat them, and measure them again.  Part of what
        made them slowest was a bad day, which does not repeat: they improve with no treatment at all.  With
        ``washout`` the second measurement is taken as another first session (no practice effect), so that what
        is left is regression to the mean alone."""
        ids = self.pool.sample(screened, seed=self.seed * 7919 + 40_000 + study)
        pre = self._rt(ids, 0, 900 + study)
        worst = np.argsort(-pre)[:n]
        post = self._rt(ids[worst], 0 if washout else 1, 1000 + study, shift=effect)
        return paired(post, pre[worst], "the slowest at screening, measured again")

    def attrition(self, n: int = 200, effect: float = 0.0, study: int = 0, dropout: float = 0.35) -> Estimate:
        """A randomized experiment that loses people unevenly: in the treated group the slower people find the
        training tedious and leave before the final measurement (``dropout`` of them); the control group stays.
        The completers are compared."""
        ids = self.pool.sample(n, seed=self.seed * 7919 + 50_000 + study)
        rng = self._rng(4, study)
        g = randomize(n, 2, rng)
        post = self._rt(ids, 0, 1100 + study, shift=effect * g)
        slow = self.pool.simple_mean(ids) + 15.0 * rng.standard_normal(n)
        treated = np.flatnonzero(g == 1)
        n_out = int(round(dropout * len(treated)))
        gone = treated[np.argsort(-slow[treated])[:n_out]]
        keep = np.ones(n, dtype=bool)
        keep[gone] = False
        return difference(post[keep], g[keep], "completers only")

    def crossover(self, n: int = 40, effect: float = 0.0, study: int = 0, counterbalanced: bool = True) -> Estimate:
        """A within-person design: everyone is measured with and without the treatment, in two sessions.  If the
        order is ``counterbalanced`` (half the people, chosen by shuffle, take the treatment first), the practice
        gained between sessions falls equally on both conditions and cancels; if everyone takes the control
        session first, it is credited to the treatment."""
        ids = self.pool.sample(n, seed=self.seed * 7919 + 70_000 + study)
        first_treated = randomize(n, 2, self._rng(5, study)) if counterbalanced else np.zeros(n, dtype=int)
        s1 = self._rt(ids, 0, 1400 + study, shift=effect * first_treated)
        s2 = self._rt(ids, 1, 1500 + study, shift=effect * (1 - first_treated))
        treated = np.where(first_treated == 1, s1, s2)
        control = np.where(first_treated == 1, s2, s1)
        return paired(treated, control, "each person both ways" + ("" if counterbalanced else ", control first"))

    def threat(self, name: str, **kw) -> Estimate:
        return getattr(self, name)(**kw)

    # --- many studies at once ---------------------------------------------
    def replicate(self, design: str, studies: int = 200, **kw) -> np.ndarray:
        """The effects reported by ``studies`` independent studies of one design."""
        return np.array([getattr(self, design)(study=s, **kw).effect for s in range(studies)])

    def session_correlation(self, n: int = 5000) -> float:
        """The correlation between a person's mean reaction time in two sessions: what pairing buys."""
        ids = self.pool.sample(n, seed=self.seed * 7919 + 60_000)
        return float(np.corrcoef(self._rt(ids, 0, 1200), self._rt(ids, 1, 1300))[0, 1])
