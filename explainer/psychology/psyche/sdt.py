"""Psyche's signal detection: telling a signal from noise, and the separate matter of saying so.

The observer of Part 11 had one number for how well it could tell two stimuli apart.  Signal detection theory
gives it two: the sensitivity ``d`` (how far apart the evidence for signal and for noise lie, in units of the
noise) and the criterion (where it draws the line to say yes).  Everything here is closed form or exact
enumeration where it can be, with simulation only where the point is the sampling.

* the equal- and unequal-variance Gaussian observer, its hit and false-alarm rates, ``d'`` and ``c`` from rates
  (with the log-linear correction for rates of 0 and 1), ``beta`` and the criterion's other names
* ROC curves in probability and z coordinates, the area under them, and the zROC's slope and intercept
* rating-scale ROCs from confidence counts, fitted by maximum likelihood (equal or unequal variance)
* the ideal observer: the likelihood ratio, the optimal criterion from base rates and payoffs
* two-alternative forced choice (``Phi(d / sqrt 2)``) and m-alternative choice by quadrature
* rival models: the high-threshold model (a straight ROC) and a dual-process mixture (Yonelinas's)
* base rates: hits, false alarms and the share of alarms that are real (the mammogram arithmetic)
* the prevalence effect: an observer who moves its criterion toward the payoff-free optimum as targets grow rare
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
from scipy import integrate, optimize, stats

Phi = stats.norm.cdf
Z = stats.norm.ppf


# ------------------------------------------------------------------------------------------- the observer
@dataclass
class Observer:
    """Evidence on a noise trial ~ N(0, 1); on a signal trial ~ N(d, sigma_s^2).  The observer says yes when the
    evidence exceeds ``criterion`` (an absolute location on the evidence axis)."""

    d: float = 1.5
    sigma_s: float = 1.0
    criterion: float = 0.75

    def rates(self, criterion=None):
        k = self.criterion if criterion is None else np.asarray(criterion, dtype=float)
        hit = 1 - Phi((k - self.d) / self.sigma_s)
        fa = 1 - Phi(k)
        return hit, fa

    def respond(self, signal: bool, rng) -> bool:
        x = (self.d + self.sigma_s * rng.standard_normal()) if signal else rng.standard_normal()
        return bool(x > self.criterion)

    def evidence(self, signal: bool, n: int, rng) -> np.ndarray:
        return (self.d + self.sigma_s * rng.standard_normal(n)) if signal else rng.standard_normal(n)


def rates(d: float, criterion, sigma_s: float = 1.0):
    return Observer(d, sigma_s, 0.0).rates(criterion)


def loglinear(k: int, n: int) -> float:
    """Hautus's log-linear correction: (k + 0.5) / (n + 1), so that rates of 0 and 1 have finite z scores."""
    return (k + 0.5) / (n + 1.0)


def dprime(hit: float, fa: float) -> float:
    return float(Z(hit) - Z(fa))


def criterion_c(hit: float, fa: float) -> float:
    """The criterion's distance from the midpoint between the two distributions (positive = conservative)."""
    return float(-0.5 * (Z(hit) + Z(fa)))


def beta(hit: float, fa: float) -> float:
    """The likelihood ratio at the criterion (equal variance)."""
    return float(math.exp(dprime(hit, fa) * criterion_c(hit, fa)))


def from_counts(hits: int, n_signal: int, fas: int, n_noise: int, correct: bool = True) -> dict:
    h = loglinear(hits, n_signal) if correct else hits / n_signal
    f = loglinear(fas, n_noise) if correct else fas / n_noise
    return {"hit": h, "fa": f, "d": dprime(h, f), "c": criterion_c(h, f), "beta": beta(h, f)}


# ------------------------------------------------------------------------------------------------- ROCs
def roc(d: float, sigma_s: float = 1.0, criteria=None):
    k = np.linspace(-4, 4 + d, 401) if criteria is None else np.asarray(criteria, dtype=float)
    hit, fa = rates(d, k, sigma_s)
    return fa, hit


def auc(d: float, sigma_s: float = 1.0) -> float:
    """Area under the binormal ROC: P(signal evidence > noise evidence) = Phi(d / sqrt(1 + sigma_s^2))."""
    return float(Phi(d / math.sqrt(1.0 + sigma_s ** 2)))


def zroc(hit, fa) -> dict:
    """Least-squares line through (z(FA), z(H)): slope = 1 / sigma_s, intercept = d / sigma_s."""
    x, y = Z(np.asarray(fa, dtype=float)), Z(np.asarray(hit, dtype=float))
    slope, intercept = np.polyfit(x, y, 1)
    return {"slope": float(slope), "intercept": float(intercept), "zfa": x, "zhit": y}


def rating_rates(counts_signal, counts_noise):
    """Cumulative hit and false-alarm rates from confidence counts ordered from 'sure new' to 'sure old'
    (each criterion: say old at this rating or higher)."""
    s = np.asarray(counts_signal, dtype=float)
    n = np.asarray(counts_noise, dtype=float)
    hit = np.cumsum(s[::-1])[::-1][1:] / s.sum()
    fa = np.cumsum(n[::-1])[::-1][1:] / n.sum()
    return hit, fa


def simulate_ratings(obs: Observer, criteria, n_signal: int, n_noise: int, rng):
    """Confidence ratings: the evidence binned by ``criteria`` (ascending), 1 = surest noise ... K = surest signal."""
    k = np.asarray(criteria, dtype=float)
    xs = obs.evidence(True, n_signal, rng)
    xn = obs.evidence(False, n_noise, rng)
    cs = np.bincount(np.searchsorted(k, xs), minlength=len(k) + 1)
    cn = np.bincount(np.searchsorted(k, xn), minlength=len(k) + 1)
    return cs, cn


def fit_rating(counts_signal, counts_noise, equal_variance: bool = False) -> dict:
    """Maximum-likelihood binormal fit to rating counts: d, sigma_s and the K-1 criteria."""
    s = np.asarray(counts_signal, dtype=float)
    n = np.asarray(counts_noise, dtype=float)
    k_n = len(s) - 1
    h, f = rating_rates(s + 0.5, n + 0.5)
    start_k = np.sort(-Z(np.clip(f, 1e-3, 1 - 1e-3)))
    z0 = zroc(np.clip(h, 1e-3, 1 - 1e-3), np.clip(f, 1e-3, 1 - 1e-3))
    sig0 = 1.0 if equal_variance else max(0.3, 1 / max(z0["slope"], 0.2))
    d0 = max(0.05, z0["intercept"] * sig0)

    def unpack(theta):
        d = theta[0]
        sig = 1.0 if equal_variance else math.exp(theta[1])
        raw = theta[1 if equal_variance else 2:]
        crit = np.cumsum(np.concatenate([[raw[0]], np.exp(raw[1:])]))
        return d, sig, crit

    def nll(theta):
        d, sig, crit = unpack(theta)
        edges = np.concatenate([[-np.inf], crit, [np.inf]])
        pn = np.diff(Phi(edges))
        ps = np.diff(Phi((edges - d) / sig))
        pn, ps = np.clip(pn, 1e-12, 1), np.clip(ps, 1e-12, 1)
        return -float(np.sum(n * np.log(pn)) + np.sum(s * np.log(ps)))

    raw0 = np.concatenate([[start_k[0]], np.log(np.maximum(np.diff(start_k), 0.05))])
    theta0 = np.concatenate([[d0], [] if equal_variance else [math.log(sig0)], raw0])
    res = optimize.minimize(nll, theta0, method="Nelder-Mead", options={"maxiter": 40000, "xatol": 1e-7, "fatol": 1e-9})
    res = optimize.minimize(nll, res.x, method="BFGS")
    d, sig, crit = unpack(res.x)
    return {"d": float(d), "sigma_s": float(sig), "criteria": crit, "loglik": -float(res.fun), "k": k_n,
            "slope": 1 / sig, "auc": auc(d, sig), "n_params": len(res.x)}


# ------------------------------------------------------------------------------------- the ideal observer
def likelihood_ratio(x, d: float, sigma_s: float = 1.0):
    x = np.asarray(x, dtype=float)
    return stats.norm.pdf(x, d, sigma_s) / stats.norm.pdf(x)


def optimal_beta(p_signal: float, v_hit: float = 1.0, v_cr: float = 1.0, c_miss: float = 0.0, c_fa: float = 0.0):
    """Say yes when the likelihood ratio exceeds  P(noise)/P(signal) * (V_cr + C_fa) / (V_hit + C_miss)."""
    return (1 - p_signal) / p_signal * (v_cr + c_fa) / (v_hit + c_miss)


def optimal_criterion(d: float, p_signal: float, **payoffs) -> float:
    """Equal variance: the evidence location where the likelihood ratio equals the optimal beta."""
    return d / 2 + math.log(optimal_beta(p_signal, **payoffs)) / d


def expected_value(d: float, criterion, p_signal: float, v_hit=1.0, v_cr=1.0, c_miss=0.0, c_fa=0.0):
    hit, fa = rates(d, criterion)
    return p_signal * (hit * v_hit - (1 - hit) * c_miss) + (1 - p_signal) * ((1 - fa) * v_cr - fa * c_fa)


# --------------------------------------------------------------------------------------------- choice tasks
def pc_2afc(d: float) -> float:
    return float(Phi(d / math.sqrt(2)))


def pc_mafc(d: float, m: int) -> float:
    """m-alternative forced choice: P(the signal's evidence beats m - 1 noise draws)."""
    f = lambda x: stats.norm.pdf(x - d) * Phi(x) ** (m - 1)  # noqa: E731
    return float(integrate.quad(f, -np.inf, np.inf)[0])


def d_from_2afc(pc: float) -> float:
    return float(math.sqrt(2) * Z(pc))


# ---------------------------------------------------------------------------------------------- rival models
def high_threshold_roc(p_detect: float, guess):
    """A detected signal always says yes; otherwise the observer guesses yes at rate g.  H = p + (1-p) g, F = g."""
    g = np.asarray(guess, dtype=float)
    return g, p_detect + (1 - p_detect) * g


def dual_process_roc(recollect: float, d_familiar: float, criteria):
    """Yonelinas: with probability R an old item is recollected (always yes); otherwise equal-variance familiarity."""
    k = np.asarray(criteria, dtype=float)
    fa = 1 - Phi(k)
    hit = recollect + (1 - recollect) * (1 - Phi(k - d_familiar))
    return fa, hit


# ---------------------------------------------------------------------------------------------- base rates
def natural_frequencies(prevalence: float, sensitivity: float, false_positive: float, n: int = 1000) -> dict:
    sick = prevalence * n
    tp = sensitivity * sick
    fp = false_positive * (n - sick)
    return {"n": n, "sick": sick, "true_positive": tp, "false_positive": fp, "positives": tp + fp,
            "ppv": tp / (tp + fp)}


def ppv(prevalence: float, d: float, criterion: float) -> float:
    hit, fa = rates(d, criterion)
    return float(prevalence * hit / (prevalence * hit + (1 - prevalence) * fa))


# ---------------------------------------------------------------------------------------- the prevalence effect
def prevalence_criteria(d: float, prevalences, shift: float = 1.0) -> np.ndarray:
    """An observer that moves its criterion a share ``shift`` of the way from neutral (d/2) to the
    accuracy-maximizing one for each prevalence."""
    p = np.asarray(prevalences, dtype=float)
    opt = d / 2 + np.log((1 - p) / p) / d
    return d / 2 + shift * (opt - d / 2)
