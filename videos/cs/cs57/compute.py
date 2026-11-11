"""Precompute everything numerical in Part 57 of *Computer Science, Built* ("Learning Theory").

    python -m videos.cs.cs57.compute              # everything missing
    python -m videos.cs.cs57.compute --force boost

Results are cached in ``.cache/cs57/<name>.json``; scenes call ``load(name)``.  The instrument is
``explainer/cs/learn/theory.py``; tests in tests/test_cs57_learning.py.

Items:
    shatter     half-planes shatter three points, never four: every labelling checked by an LP
    growth      the growth function of half-planes against 2^m and the Sauer-Shelah bound
    rect        PAC learning curves for rectangles against the rectangle and VC bounds
    finite      the finite-class sample bound
    perceptron  mistakes against Novikoff's 1/gamma^2 as the dimension grows to 1,000
    boost       AdaBoost without and with label noise: errors and margins over rounds, example weights
    hedge       Hedge's regret against sqrt(T ln N / 2), and follow-the-leader
    halving     the halving algorithm's mistakes against log2 N
    bandits     epsilon-greedy, UCB1 and Thompson sampling against the Lai-Robbins rate
    parity      sparse parity: no single bit correlates; subset search against Gaussian elimination
    descent     double descent with random ReLU features
    compress    a size-4 compression scheme for rectangles
"""

from __future__ import annotations

from explainer.ai.cache import Cache

CACHE = Cache("cs57")
load = CACHE.load


def _T():
    from explainer.cs.learn import theory
    return theory


def compute_shatter() -> dict:
    return _T().shattering()


def compute_growth() -> dict:
    return {"rows": _T().growth()}


def compute_rect() -> dict:
    return _T().rectangle_curves()


def compute_finite() -> dict:
    return _T().finite_class()


def compute_perceptron() -> dict:
    return {"rows": _T().perceptron_margin()}


def compute_boost() -> dict:
    return {"clean": _T().adaboost(noise=0.0), "noisy": _T().adaboost(noise=0.05)}


def compute_hedge() -> dict:
    return _T().hedge()


def compute_halving() -> dict:
    return _T().halving()


def compute_bandits() -> dict:
    return _T().bandits()


def compute_parity() -> dict:
    return {"rows": _T().parity()}


def compute_descent() -> dict:
    return _T().double_descent()


def compute_compress() -> dict:
    return _T().rectangle_compression()


ITEMS = {k[8:]: v for k, v in globals().items() if k.startswith("compute_")}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
