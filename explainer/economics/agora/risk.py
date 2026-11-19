"""Time and risk (Agora, Part 7): choosing when the pay-off comes later, or may not come at all.

**Risk.**  Utility of wealth (:func:`crra`, :func:`cara`, :func:`log_u`), certainty equivalents and risk premia for
discrete lotteries (:func:`certainty_equivalent`), the Arrow-Pratt measures by central differences
(:func:`arrow_pratt`), first- and second-order stochastic dominance between discrete lotteries (:func:`fosd`,
:func:`sosd`), the probability triangle of three-outcome lotteries with expected utility's straight, parallel
indifference lines (:func:`triangle_point`, :func:`eu_slope`), Allais's two pairs and the pattern they test
(:func:`allais_eu_consistent`), insurance with a loaded premium (:func:`optimal_cover`), and Rabin's calibration made
concrete for CRRA utility (:func:`crra_gamma_to_reject`, :func:`crra_largest_gain`): the risk aversion needed to turn
down a small bet, and the large bets it then turns down.

**The St Petersburg game.**  :func:`stpetersburg_value` (the expected prize of a game cut off at n tosses),
:func:`stpetersburg_price` (what a player with wealth w and log or square-root utility would pay, Daniel Bernoulli
1738 and Cramer 1728) and :func:`stpetersburg_play` (simulated sessions, whose average prize grows like log2 of the
number of games).

**Time.**  Fisher's two periods (:func:`fisher`), with the Euler equation; discount functions (exponential,
hyperbolic, quasi-hyperbolic beta-delta: :func:`discount`) and the preference reversals the non-exponential ones
produce (:func:`reversal`); the elasticity of intertemporal substitution against relative risk aversion in an
Epstein-Zin aggregator (:func:`epstein_zin_value`).

**Measuring it.**  :func:`holt_laury_menu` (Holt and Laury's ten paired lotteries) and :func:`holt_laury_interval`
(the CRRA interval implied by the number of safe choices).

Plain numpy and scipy.
"""

from __future__ import annotations

import numpy as np
from scipy.optimize import brentq

# ---------------------------------------------------------------------------------------------------------------
# utility of wealth


def crra(x, gamma: float):
    """u(x) = x^(1 - gamma) / (1 - gamma); log x at gamma = 1.  Relative risk aversion gamma."""
    x = np.asarray(x, float)
    if abs(gamma - 1) < 1e-12:
        return np.log(x)
    return x ** (1 - gamma) / (1 - gamma)


def crra_inv(v, gamma: float):
    v = np.asarray(v, float)
    if abs(gamma - 1) < 1e-12:
        return np.exp(v)
    return (v * (1 - gamma)) ** (1 / (1 - gamma))


def cara(x, a: float):
    """u(x) = -exp(-a x) / a.  Absolute risk aversion a, whatever the wealth."""
    return -np.exp(-a * np.asarray(x, float)) / a


def cara_inv(v, a: float):
    return -np.log(-a * np.asarray(v, float)) / a


def log_u(x):
    return np.log(np.asarray(x, float))


def certainty_equivalent(outcomes, probs, gamma: float | None = None, a: float | None = None) -> float:
    """The sure amount worth as much as the lottery, under CRRA(gamma) or CARA(a) utility (risk neutral if neither)."""
    x, p = np.asarray(outcomes, float), np.asarray(probs, float)
    if gamma is not None:
        return float(crra_inv(p @ crra(x, gamma), gamma))
    if a is not None:
        return float(cara_inv(p @ cara(x, a), a))
    return float(p @ x)


def risk_premium(outcomes, probs, **kw) -> float:
    """Expected value minus the certainty equivalent: what the chooser would pay to swap the lottery for its mean."""
    return float(np.dot(outcomes, probs) - certainty_equivalent(outcomes, probs, **kw))


def arrow_pratt(u, x: float, h: float = 1e-3) -> dict:
    """Absolute (-u''/u') and relative (-x u''/u') risk aversion of a utility function at x."""
    u1 = (u(x + h) - u(x - h)) / (2 * h)
    u2 = (u(x + h) - 2 * u(x) + u(x - h)) / h ** 2
    return {"absolute": float(-u2 / u1), "relative": float(-x * u2 / u1)}


# ---------------------------------------------------------------------------------------------------------------
# stochastic dominance and the probability triangle


def _cdf(x, p, grid):
    x, p = np.asarray(x, float), np.asarray(p, float)
    return np.array([p[x <= g].sum() for g in grid])


def fosd(x, px, y, py) -> bool:
    """Does lottery (x, px) first-order dominate (y, py)?  Its CDF is nowhere above the other's, and they differ."""
    grid = np.unique(np.r_[x, y])
    F, G = _cdf(x, px, grid), _cdf(y, py, grid)
    return bool(np.all(F <= G + 1e-12) and np.any(F < G - 1e-12))


def sosd(x, px, y, py) -> bool:
    """Second-order dominance: the integral of the CDF is nowhere above the other's (every risk averter prefers it)."""
    grid = np.unique(np.r_[x, y])
    F, G = _cdf(x, px, grid), _cdf(y, py, grid)
    dx = np.diff(grid)
    IF = np.r_[0.0, np.cumsum(F[:-1] * dx)]
    IG = np.r_[0.0, np.cumsum(G[:-1] * dx)]
    return bool(np.all(IF <= IG + 1e-12) and (np.any(IF < IG - 1e-12) or np.any(F != G)))


def triangle_point(p_low: float, p_high: float):
    """A three-outcome lottery in the Marschak-Machina triangle: the chance of the worst outcome across, of the best
    up (the middle outcome gets the rest)."""
    return float(p_low), float(p_high)


def eu_slope(u_low: float, u_mid: float, u_high: float) -> float:
    """The slope of expected utility's indifference lines in the triangle: (u_mid - u_low) / (u_high - u_mid).  The
    same everywhere (independence makes them straight and parallel); steeper for a more risk-averse chooser."""
    return float((u_mid - u_low) / (u_high - u_mid))


def allais_eu_consistent(choose_1a: bool, choose_2a: bool) -> bool:
    """Allais's pairs: 1A $1M for sure vs 1B (10% $5M, 89% $1M, 1% $0); 2A (11% $1M, 89% $0) vs 2B (10% $5M, 90% $0).
    Expected utility requires 1A with 2A or 1B with 2B: both pairs differ by the same common consequence."""
    return choose_1a == choose_2a


ALLAIS = {"1A": ((1e6,), (1.0,)), "1B": ((5e6, 1e6, 0.0), (0.10, 0.89, 0.01)),
          "2A": ((1e6, 0.0), (0.11, 0.89)), "2B": ((5e6, 0.0), (0.10, 0.90))}


# ---------------------------------------------------------------------------------------------------------------
# insurance


def optimal_cover(w: float, loss: float, p: float, loading: float, gamma: float, grid: int = 4001) -> dict:
    """The share of a loss to insure when cover costs (1 + loading) times its expected payout; CRRA utility.  At a fair
    price (loading 0) a risk averter insures fully (Mossin 1968); with any loading, less than fully."""
    q = np.linspace(0, 1, grid)
    prem = (1 + loading) * p * loss * q
    eu = (1 - p) * crra(w - prem, gamma) + p * crra(w - prem - loss + q * loss, gamma)
    k = int(np.argmax(eu))
    return {"cover": float(q[k]), "premium": float(prem[k]), "eu": eu, "q": q}


# ---------------------------------------------------------------------------------------------------------------
# Rabin's calibration, for CRRA utility (his theorem needs only concavity; its tables are transcribed, not computed)


def _crra_gain(l: float, g: float, w: float, gamma: float) -> float:
    """Expected CRRA utility of (lose l, gain g) at wealth w minus that of standing pat, scaled by w^(1 - gamma)
    (computed on wealth relative to w, so no power overflows)."""
    a, b = 1 + g / w, 1 - l / w
    if abs(gamma - 1) < 1e-12:
        return 0.5 * (np.log(a) + np.log(b))
    return (0.5 * (a ** (1 - gamma) + b ** (1 - gamma)) - 1) / (1 - gamma)


def crra_rejects(l: float, g: float, w: float, gamma: float) -> bool:
    """Does a CRRA(gamma) chooser with wealth w turn down a 50-50 bet of losing l or gaining g?"""
    return bool(_crra_gain(l, g, w, gamma) < 0)


def crra_gamma_to_reject(l: float, g: float, w: float) -> float:
    """The relative risk aversion at which a CRRA chooser with wealth w is just indifferent to (lose l, gain g)."""
    return float(brentq(lambda gm: _crra_gain(l, g, w, gm), 1e-3, 1e5))


def crra_largest_gain(L: float, w: float, gamma: float, cap: float = 1e15) -> float:
    """The largest G for which a CRRA(gamma) chooser with wealth w still turns down (lose L, gain G); inf if every G is
    turned down (for gamma > 1 utility is bounded above, so a large enough loss outweighs any gain)."""
    b = 1 - L / w
    if abs(gamma - 1) < 1e-12:
        return float(w * (1 / b - 1))
    # 0.5 (a^(1-gm) + b^(1-gm)) = 1  ->  a^(1-gm) = 2 - b^(1-gm)
    rhs = 2 - b ** (1 - gamma)
    if gamma > 1 and rhs <= 0:
        return float("inf")
    a = rhs ** (1 / (1 - gamma))
    return float(min(w * (a - 1), cap))


# ---------------------------------------------------------------------------------------------------------------
# the St Petersburg game


def stpetersburg_value(n: int) -> float:
    """The expected prize of a game cut off after n tosses (prize 2^k with chance 2^-k): n dollars."""
    return float(sum(2.0 ** -k * 2.0 ** k for k in range(1, n + 1)))


def stpetersburg_price(w: float, utility: str = "log", kmax: int = 200) -> float:
    """The most a player with wealth w would pay to play, under log utility (Bernoulli) or the square root (Cramer):
    the price c solving sum_k 2^-k u(w - c + 2^k) = u(w)."""
    ks = np.arange(1, kmax + 1)
    pk = 0.5 ** ks
    prize = 2.0 ** ks
    u = np.log if utility == "log" else np.sqrt

    def gap(c):
        return float(np.sum(pk * u(w - c + prize)) - u(w))

    return float(brentq(gap, -1e9 if w <= 0 else 0.0, w + 1.999999))


def stpetersburg_ce_alone(utility: str = "sqrt", kmax: int = 200) -> float:
    """The game's certainty equivalent ignoring wealth: u^-1(sum_k 2^-k u(2^k)).  Cramer's square root gives about 2.9."""
    ks = np.arange(1, kmax + 1)
    if utility == "sqrt":
        return float(np.sum(0.5 ** ks * 2.0 ** (ks / 2)) ** 2)
    return float(np.exp(np.sum(0.5 ** ks * ks * np.log(2))))


def stpetersburg_play(games: int, rng) -> np.ndarray:
    """Prizes of simulated games: toss until heads; heads on toss k pays 2^k."""
    k = rng.geometric(0.5, size=games)
    return 2.0 ** k


# ---------------------------------------------------------------------------------------------------------------
# time


def fisher(y1: float, y2: float, r: float, beta: float, gamma: float) -> dict:
    """Fisher's two periods: incomes y1, y2; borrow or lend at r; maximize u(c1) + beta u(c2) with CRRA(gamma).
    The Euler equation u'(c1) = beta (1 + r) u'(c2) gives c2 / c1 = (beta (1 + r))^(1 / gamma)."""
    wealth = y1 + y2 / (1 + r)
    k = (beta * (1 + r)) ** (1 / gamma)
    c1 = wealth / (1 + k / (1 + r))
    c2 = k * c1
    return {"c1": c1, "c2": c2, "saving": y1 - c1, "wealth": wealth, "growth": k,
            "euler_gap": float(c1 ** -gamma - beta * (1 + r) * c2 ** -gamma)}


def discount(t, kind: str = "exponential", rate: float = 0.05, a: float = 1.0, b: float = 1.0, beta: float = 0.7,
             delta: float = 0.96):
    """Discount factors at delays t (years): exponential e^(-rate t); hyperbolic (1 + a t)^(-b / a) (Loewenstein and
    Prelec 1992); quasi-hyperbolic: 1 at t = 0, beta delta^t after (Laibson 1997)."""
    t = np.asarray(t, float)
    if kind == "exponential":
        return np.exp(-rate * t)
    if kind == "hyperbolic":
        return (1 + a * t) ** (-b / a)
    if kind == "beta-delta":
        return np.where(t <= 0, 1.0, beta * delta ** t)
    raise ValueError(kind)


def reversal(small: float, large: float, gap: float, push: float, **kw) -> bool:
    """Does the chooser take the smaller reward now over the larger one ``gap`` years later, yet prefer the larger
    when both are pushed ``push`` years into the future?  (Exponential discounting never reverses.)"""
    now = small * discount(0.0, **kw) > large * discount(gap, **kw)
    later = small * discount(push, **kw) > large * discount(push + gap, **kw)
    return bool(now and not later)


def epstein_zin_value(c_path, probs_next, beta: float, gamma: float, psi: float) -> float:
    """A two-period Epstein-Zin value: V = [(1 - beta) c0^(1 - 1/psi) + beta (E[c1^(1 - gamma)])^((1 - 1/psi)/(1 -
    gamma))]^(1 / (1 - 1/psi)).  gamma (risk aversion) and psi (the EIS) are separate; with gamma = 1/psi it is
    expected utility."""
    c0, c1 = c_path[0], np.asarray(c_path[1], float)
    rho = 1 - 1 / psi
    ce = (np.dot(probs_next, c1 ** (1 - gamma))) ** (1 / (1 - gamma)) if abs(gamma - 1) > 1e-12 else \
        np.exp(np.dot(probs_next, np.log(c1)))
    return float(((1 - beta) * c0 ** rho + beta * ce ** rho) ** (1 / rho))


# ---------------------------------------------------------------------------------------------------------------
# Holt and Laury's menu


def holt_laury_menu(scale: float = 1.0) -> list:
    """The ten paired lotteries of Holt and Laury (2002): option A pays $2.00 or $1.60, option B $3.85 or $0.10, the
    high prize with chance k/10 in decision k; times ``scale``."""
    rows = []
    for k in range(1, 11):
        p = k / 10
        rows.append({"k": k, "p": p, "A": (2.00 * scale, 1.60 * scale), "B": (3.85 * scale, 0.10 * scale)})
    return rows


def _crra_prefers_a(row, gamma: float) -> bool:
    p = row["p"]
    ua = p * crra(row["A"][0], gamma) + (1 - p) * crra(row["A"][1], gamma)
    ub = p * crra(row["B"][0], gamma) + (1 - p) * crra(row["B"][1], gamma)
    return bool(ua > ub)


def safe_choices(gamma: float, scale: float = 1.0) -> int:
    """How many safe (A) choices a CRRA(gamma) chooser makes on the menu."""
    return int(sum(_crra_prefers_a(r, gamma) for r in holt_laury_menu(scale)))


def holt_laury_interval(n_safe: int, scale: float = 1.0) -> tuple:
    """The range of CRRA coefficients that makes exactly ``n_safe`` safe choices (switching to B after them)."""
    gs = np.linspace(-1.5, 3.0, 9001)
    hits = [g for g in gs if safe_choices(g, scale) == n_safe]
    return (float(min(hits)), float(max(hits))) if hits else (float("nan"), float("nan"))
