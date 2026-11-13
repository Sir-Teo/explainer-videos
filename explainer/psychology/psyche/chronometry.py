"""Mental chronometry: reaction time as a chain of stages (Part 1 of *Psychology, Built*).

The oldest quantitative model in psychology.  A response is produced by stages that run one after another, each
taking a random time, so the reaction time is their sum (all times here are in milliseconds):

    RT = T_1 + T_2 + ... + T_k,        T_j independent,  T_j ~ Gamma(mean m_j, coefficient of variation c_j)

What follows from that, and is implemented here:

* **Donders' subtraction (1868).**  If a task B is task A with one stage inserted and nothing else changed
  (*pure insertion*), the inserted stage's mean duration is ``E[RT_B] - E[RT_A]``.
* **The distributional test of pure insertion.**  Under pure insertion the whole distribution of ``RT_B`` is the
  distribution of ``RT_A`` convolved with the inserted stage's, so every cumulant adds: in particular
  ``Var[RT_B] = Var[RT_A] + Var[T]`` and the third central moments add too.  Three means cannot test the
  assumption; three distributions can (:func:`insertion_test`).
* **Additive factors (Sternberg 1969).**  Two experimental factors that change the durations of *different* stages
  have additive effects on mean RT; two that change the *same* stage generally interact (:func:`factorial_means`).
* **Hick's logarithm (1952).**  A choice among ``n`` equally likely alternatives takes time proportional to the
  information gained, ``log2 n`` bits (:func:`hick`).
* **The ex-Gaussian.**  A normal stage plus an exponential one gives the right-skewed density that describes
  reaction-time distributions well (Hohle 1965): :func:`exgauss_pdf`, :func:`fit_exgauss`.

Gamma stages are used because a gamma is positive, has two free moments, and sums of gammas are easy to check:
a stage with mean ``m`` and CV ``c`` has shape ``1/c^2``, scale ``m c^2``, variance ``(m c)^2`` and third central
moment ``2 c^4 m^3``.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, replace

import numpy as np
from scipy import optimize, special, stats

__all__ = ["Stage", "StageModel", "donders_models", "prepared_models", "subtraction", "insertion_test",
           "factorial_means", "interaction", "hick", "hick_fit", "exgauss_pdf", "exgauss_sample", "fit_exgauss",
           "conduction_speed"]


@dataclass(frozen=True)
class Stage:
    """One processing stage: a name, a mean duration in ms, and a coefficient of variation (SD / mean)."""

    name: str
    mean: float
    cv: float = 0.3

    @property
    def var(self) -> float:
        return (self.mean * self.cv) ** 2

    @property
    def third(self) -> float:
        """Third central moment of a gamma with this mean and CV."""
        return 2 * self.cv ** 4 * self.mean ** 3

    def sample(self, n: int, rng: np.random.Generator) -> np.ndarray:
        if self.mean <= 0:
            return np.zeros(n)
        if self.cv <= 0:
            return np.full(n, float(self.mean))
        return rng.gamma(1 / self.cv ** 2, self.mean * self.cv ** 2, size=n)

    def scaled(self, factor: float) -> "Stage":
        return replace(self, mean=self.mean * factor)


@dataclass(frozen=True)
class StageModel:
    """Stages in series.  ``mean``, ``var`` and ``third`` are exact; ``sample`` draws reaction times."""

    stages: tuple

    @property
    def mean(self) -> float:
        return float(sum(s.mean for s in self.stages))

    @property
    def var(self) -> float:
        return float(sum(s.var for s in self.stages))

    @property
    def sd(self) -> float:
        return math.sqrt(self.var)

    @property
    def third(self) -> float:
        return float(sum(s.third for s in self.stages))

    @property
    def skew(self) -> float:
        return self.third / self.var ** 1.5

    def names(self) -> list:
        return [s.name for s in self.stages]

    def sample(self, n: int, rng: np.random.Generator, parts: bool = False):
        """``n`` reaction times; with ``parts`` also the (n, k) matrix of stage durations."""
        t = np.column_stack([s.sample(n, rng) for s in self.stages])
        return (t.sum(axis=1), t) if parts else t.sum(axis=1)

    def insert(self, stage: Stage, before: str) -> "StageModel":
        """This model with ``stage`` inserted before the stage called ``before``: pure insertion."""
        i = self.names().index(before)
        return StageModel(self.stages[:i] + (stage,) + self.stages[i:])

    def with_stage(self, name: str, **changes) -> "StageModel":
        return StageModel(tuple(replace(s, **changes) if s.name == name else s for s in self.stages))

    def pdf(self, t: np.ndarray, dt: float = 0.25) -> np.ndarray:
        """The density of the sum at times ``t`` (ms), by numerical convolution of the gamma densities."""
        t = np.asarray(t, dtype=float)
        hi = self.mean + 12 * self.sd + 5 * dt
        grid = np.arange(0.0, hi, dt)
        dens, shift, active = None, 0.0, 0
        for s in self.stages:
            if s.cv <= 0 or s.mean <= 0:
                shift += s.mean  # a constant stage only shifts the density
                continue
            k, scale = 1 / s.cv ** 2, s.mean * s.cv ** 2
            # the mass of each cell, from the CDF: exact for any shape, including densities that blow up at 0
            cell = np.diff(stats.gamma.cdf(np.append(grid, grid[-1] + dt), k, scale=scale))
            dens = cell if dens is None else np.convolve(dens, cell)[: len(grid)]
            active += 1
        if dens is None:
            raise ValueError("a model of constant stages has no density")
        # cell i of the convolution holds sums of ``active`` values whose cells start at i dt in total: its centre
        # is i dt + active dt / 2
        return np.interp(t - shift, grid + active * dt / 2, dens / dt, left=0.0, right=0.0)


# ---------------------------------------------------------------------------
# Donders' three methods
# ---------------------------------------------------------------------------
DONDERS_1868 = {"a": 201.0, "b": 284.0, "c": 237.0}  # ms; Donders (1868), his own means, as given by Roelofs (2018)


def donders_models(a: float = 201.0, discriminate: float = 36.0, choose: float = 47.0, cv_base: float = 0.12,
                   cv_stage: float = 0.6, sense_share: float = 0.6) -> dict:
    """The stage models Donders' reasoning assumes, for his methods a (simple), c (go/no-go) and b (choice).

    a:  sense -> respond
    c:  sense -> discriminate -> respond
    b:  sense -> discriminate -> choose -> respond

    The defaults reproduce his reported means (201, 237 and 284 ms).  How the 201 ms of method a divide between
    sensing and responding is *not* identified by his data; ``sense_share`` is a free choice that no prediction
    here depends on.
    """
    sense = Stage("sense", a * sense_share, cv_base)
    respond = Stage("respond", a * (1 - sense_share), cv_base)
    A = StageModel((sense, respond))
    C = A.insert(Stage("discriminate", discriminate, cv_stage), before="respond")
    B = C.insert(Stage("choose", choose, cv_stage), before="respond")
    return {"a": A, "b": B, "c": C}


def prepared_models(a: float = 201.0, b: float = 284.0, c: float = 237.0, decide: float = 30.0,
                    program: float = 25.0, cv_base: float = 0.12, cv_stage: float = 0.6,
                    sense_share: float = 0.6) -> dict:
    """A rival account with the *same three means* in which pure insertion is false (Wundt's objection to method c,
    and the modern one about response preparation).

    Go/no-go still needs a decision (respond or not), ``decide`` ms, so ``c - a`` is discrimination *plus* that
    decision.  And in a and c the single response can be prepared in advance, while in b it must be programmed
    after the choice, ``program`` ms, so ``b - c`` is the choice *plus* programming *minus* the go/no-go decision.
    The stage durations are solved so that the means equal ``a``, ``b`` and ``c``.
    """
    discriminate = (c - a) - decide
    choose = (b - c) + decide - program
    if discriminate <= 0 or choose <= 0:
        raise ValueError("these means leave no positive time for the stages")
    sense = Stage("sense", a * sense_share, cv_base)
    respond = Stage("respond", a * (1 - sense_share), cv_base)
    A = StageModel((sense, respond))
    C = StageModel((sense, Stage("discriminate", discriminate, cv_stage), Stage("go or no-go", decide, cv_stage),
                    respond))
    B = StageModel((sense, Stage("discriminate", discriminate, cv_stage), Stage("choose", choose, cv_stage),
                    Stage("program", program, cv_stage), respond))
    return {"a": A, "b": B, "c": C}


def subtraction(rt_a, rt_b, rt_c) -> dict:
    """Donders' two differences from samples of reaction times, each with its standard error."""
    rt_a, rt_b, rt_c = (np.asarray(x, dtype=float) for x in (rt_a, rt_b, rt_c))

    def diff(x, y):
        return float(x.mean() - y.mean()), float(math.sqrt(x.var(ddof=1) / len(x) + y.var(ddof=1) / len(y)))

    d, d_se = diff(rt_c, rt_a)
    ch, ch_se = diff(rt_b, rt_c)
    return {"discriminate": d, "discriminate_se": d_se, "choose": ch, "choose_se": ch_se}


def _central(x: np.ndarray) -> tuple:
    m = x.mean()
    return float(m), float(((x - m) ** 2).mean()), float(((x - m) ** 3).mean())


def insertion_test(rt_short, rt_long, n_boot: int = 2000, seed: int = 0) -> dict:
    """Is ``rt_long`` distributed as ``rt_short`` plus an independent, positive stage?

    Under pure insertion the differences of the first three cumulants (mean, variance, third central moment) are
    the inserted stage's own cumulants, and a positive random variable must have a positive mean, a non-negative
    variance, and (for a gamma) a third cumulant of ``2 var^2 / mean``.  Returns the three differences with
    bootstrap standard errors, the gamma stage they imply, and ``z_var``: how many standard errors the variance
    difference lies below zero (a large positive value rejects pure insertion outright).
    """
    a, b = np.asarray(rt_short, dtype=float), np.asarray(rt_long, dtype=float)
    ma, va, ta = _central(a)
    mb, vb, tb = _central(b)
    rng = np.random.default_rng(seed)
    boots = np.empty((n_boot, 3))
    for i in range(n_boot):
        ca = _central(a[rng.integers(0, len(a), len(a))])
        cb = _central(b[rng.integers(0, len(b), len(b))])
        boots[i] = [cb[0] - ca[0], cb[1] - ca[1], cb[2] - ca[2]]
    se = boots.std(axis=0, ddof=1)
    d_mean, d_var, d_third = mb - ma, vb - va, tb - ta
    cv = math.sqrt(max(d_var, 0.0)) / d_mean if d_mean > 0 else float("nan")
    return {"d_mean": d_mean, "d_var": d_var, "d_third": d_third, "se_mean": float(se[0]), "se_var": float(se[1]),
            "se_third": float(se[2]), "stage_cv": cv, "z_var": float(-d_var / se[1]) if se[1] > 0 else 0.0,
            "third_if_gamma": 2 * d_var ** 2 / d_mean if d_mean > 0 else float("nan")}


# ---------------------------------------------------------------------------
# Additive factors
# ---------------------------------------------------------------------------
def factorial_means(model: StageModel, stage_1: str, factor_1: float, stage_2: str, factor_2: float) -> np.ndarray:
    """Exact mean RTs of a 2 x 2 design: factor 1 multiplies the mean of ``stage_1`` by ``factor_1`` at its hard
    level, factor 2 that of ``stage_2`` by ``factor_2``.  Rows: factor 1 easy, hard; columns: factor 2 easy, hard.

    Different stages: the two effects add.  The same stage: the stage's mean is multiplied by both factors, and
    the effects interact by ``m (f1 - 1)(f2 - 1)``."""
    out = np.empty((2, 2))
    for i, f1 in enumerate((1.0, factor_1)):
        for j, f2 in enumerate((1.0, factor_2)):
            m = model
            m = m.with_stage(stage_1, mean=dict(zip(m.names(), [s.mean for s in m.stages]))[stage_1] * f1)
            m = m.with_stage(stage_2, mean=dict(zip(m.names(), [s.mean for s in m.stages]))[stage_2] * f2)
            out[i, j] = m.mean
    return out


def interaction(means: np.ndarray) -> float:
    """The interaction contrast of a 2 x 2 table of means: (hard, hard) - (hard, easy) - (easy, hard) + (easy,
    easy).  Zero when the factors are additive."""
    means = np.asarray(means, dtype=float)
    return float(means[1, 1] - means[1, 0] - means[0, 1] + means[0, 0])


# ---------------------------------------------------------------------------
# Hick's logarithm
# ---------------------------------------------------------------------------
def hick(n, intercept: float, per_bit: float) -> np.ndarray:
    """Mean choice reaction time for ``n`` equally likely alternatives: ``intercept + per_bit * log2(n)``."""
    return intercept + per_bit * np.log2(np.asarray(n, dtype=float))


def hick_fit(n, rt) -> dict:
    """Least-squares intercept and slope (ms per bit) of mean RT on ``log2 n``, with R^2."""
    x, y = np.log2(np.asarray(n, dtype=float)), np.asarray(rt, dtype=float)
    X = np.column_stack([np.ones_like(x), x])
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    res = y - X @ beta
    r2 = 1 - float(res @ res) / float(((y - y.mean()) ** 2).sum()) if len(y) > 2 else 1.0
    return {"intercept": float(beta[0]), "per_bit": float(beta[1]), "r2": r2}


# ---------------------------------------------------------------------------
# The ex-Gaussian
# ---------------------------------------------------------------------------
def exgauss_pdf(t, mu: float, sigma: float, tau: float) -> np.ndarray:
    """Density of Normal(mu, sigma^2) + Exponential(mean tau):

        f(t) = (1 / tau) exp( sigma^2 / (2 tau^2) - (t - mu) / tau ) Phi( (t - mu) / sigma - sigma / tau )
    """
    t = np.asarray(t, dtype=float)
    z = (t - mu) / sigma - sigma / tau
    return np.exp(sigma ** 2 / (2 * tau ** 2) - (t - mu) / tau + special.log_ndtr(z)) / tau


def exgauss_sample(n: int, mu: float, sigma: float, tau: float, rng: np.random.Generator) -> np.ndarray:
    return rng.normal(mu, sigma, n) + rng.exponential(tau, n)


def fit_exgauss(rt) -> dict:
    """Maximum-likelihood ex-Gaussian fit, started from the method of moments
    (tau = sd (skew / 2)^(1/3), mu = mean - tau, sigma^2 = var - tau^2).  Returns mu, sigma, tau and the
    log-likelihood."""
    x = np.asarray(rt, dtype=float)
    m, v = x.mean(), x.var()
    skew = float(((x - m) ** 3).mean() / v ** 1.5)
    tau0 = math.sqrt(v) * (max(skew, 0.05) / 2) ** (1 / 3)
    tau0 = min(tau0, 0.95 * math.sqrt(v))
    start = np.array([m - tau0, math.log(math.sqrt(max(v - tau0 ** 2, 1e-6 * v))), math.log(tau0)])

    def nll(p):
        mu, sigma, tau = p[0], math.exp(p[1]), math.exp(p[2])
        z = (x - mu) / sigma - sigma / tau
        return -float(np.sum(sigma ** 2 / (2 * tau ** 2) - (x - mu) / tau + special.log_ndtr(z) - math.log(tau)))

    best = optimize.minimize(nll, start, method="Nelder-Mead",
                             options={"xatol": 1e-4, "fatol": 1e-6, "maxiter": 4000, "maxfev": 4000})
    mu, sigma, tau = float(best.x[0]), float(math.exp(best.x[1])), float(math.exp(best.x[2]))
    return {"mu": mu, "sigma": sigma, "tau": tau, "loglik": -float(best.fun), "mean": mu + tau,
            "sd": math.sqrt(sigma ** 2 + tau ** 2)}


# ---------------------------------------------------------------------------
# Helmholtz's arithmetic
# ---------------------------------------------------------------------------
def conduction_speed(length_mm: float, delay_s: float) -> float:
    """Speed in metres per second of a signal that takes ``delay_s`` longer over ``length_mm`` more nerve."""
    return (length_mm / 1000.0) / delay_s
