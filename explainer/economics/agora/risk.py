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

**Insurance and portfolios.**  :func:`deductible_gamma` (the risk aversion a deductible choice implies),
:func:`merton_share` and :func:`portfolio_eu` (the demand for a risky asset).

**Time meets risk.**  :func:`ez_resolution` (Kreps-Porteus and Epstein-Zin: a preference for early resolution),
:func:`beta_delta_path` (a present-biased self's plan against what its later selves do, and a commitment), and
:func:`euler_regression` (Hall's regression of consumption growth on the real interest rate, by OLS and 2SLS).

**Paradoxes.**  :func:`ellsberg_maxmin` (Ellsberg's urn under maxmin expected utility), Chew's weighted utility in
the triangle (:func:`weighted_utility_line`, :func:`weighted_utility_value`: indifference lines that fan out),
Tversky and Kahneman's value and weighting functions (:func:`tk_value`, :func:`tk_weight`).

**Measuring it.**  :func:`holt_laury_menu` (Holt and Laury's ten paired lotteries), :func:`holt_laury_interval`
(the CRRA interval implied by the number of safe choices), :func:`holt_laury_respond` and :func:`switches_back`
(noisy simulated respondents), :func:`hrs_threshold` (the risk aversion at each of the HRS's income gambles) and
:func:`stpetersburg_median_prize` (Hayden and Platt's median heuristic).

Plain numpy and scipy.
"""

from __future__ import annotations

import numpy as np
from scipy.optimize import brentq
from scipy.special import expit

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


def deductible_gamma(w: float, p: float, d_low: float, d_high: float, extra: float) -> float:
    """The relative risk aversion at which a CRRA chooser with wealth w is just willing to pay ``extra`` a year to cut
    the deductible from d_high to d_low, when a claim comes with chance p.  Expected saving p (d_high - d_low); anything
    paid above it is a risk premium, and over stakes this small it implies enormous risk aversion (Sydnor 2010)."""

    if extra <= p * (d_high - d_low):
        return 0.0                                               # no more than the expected saving: risk neutral

    def gap(gm):
        a = (1 - p) * crra(1 - extra / w, gm) + p * crra(1 - (extra + d_low) / w, gm)
        b = (1 - p) * crra(1.0, gm) + p * crra(1 - d_high / w, gm)
        return float(a - b)

    with np.errstate(over="ignore", divide="ignore", invalid="ignore"):
        return float(brentq(gap, 1e-6, 2000.0))


def merton_share(mu: float, r: float, sigma: float, gamma: float) -> float:
    """The share of wealth in a risky asset with mean return mu and volatility sigma, against a safe rate r, for CRRA
    utility (Merton 1969, Samuelson 1969): (mu - r) / (gamma sigma^2), whatever the wealth."""
    return float((mu - r) / (gamma * sigma ** 2))


def portfolio_eu(share, w: float, r: float, outcomes, probs, gamma: float):
    """Expected CRRA utility of putting ``share`` of w in a risky asset with gross returns ``outcomes`` (the rest at
    1 + r), for a grid of shares: the curve whose top is the demand for the risky asset."""
    share = np.atleast_1d(np.asarray(share, float))
    R = np.asarray(outcomes, float)
    p = np.asarray(probs, float)
    wealth = w * ((1 - share)[:, None] * (1 + r) + share[:, None] * R[None, :])
    return (crra(np.maximum(wealth, 1e-9), gamma) * p[None, :]).sum(axis=1)


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
    hi = 5 * 2 * w * (g - l) / (g * g + l * l) + 10           # five times the small-bet approximation
    return float(brentq(lambda gm: _crra_gain(l, g, w, gm), 1e-3, hi))


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


def stpetersburg_value(n: int, first: float = 2.0) -> float:
    """The expected prize of a game cut off after n tosses (heads on toss k pays first * 2^(k-1), with chance 2^-k):
    n * first / 2 dollars, which grows without bound."""
    return float(sum(2.0 ** -k * first * 2.0 ** (k - 1) for k in range(1, n + 1)))


def stpetersburg_truncated_value(n: int, first: float = 1.0) -> float:
    """Hayden and Platt's truncated game: the coin is tossed at most n times, and if it never shows heads the player
    gets the maximum prize first * 2^n.  Expected prize first * (n / 2 + 1): $2.50 for three tosses (first = 1)."""
    return float(stpetersburg_value(n, first) + 0.5 ** n * first * 2.0 ** n)


def _prizes(first: float, kmax: int):
    ks = np.arange(1, kmax + 1)
    return ks, 0.5 ** ks, first * 2.0 ** (ks - 1)


def stpetersburg_price(w: float, utility: str = "log", kmax: int = 200, first: float = 2.0) -> float:
    """The most a player with wealth w would pay to play, under log utility (Bernoulli) or the square root (Cramer):
    the price c solving sum_k 2^-k u(w - c + prize_k) = u(w).  Bernoulli's own game (1738) has ``first`` = 1: one
    ducat for heads on the first toss, two on the second, four on the third."""
    _, pk, prize = _prizes(first, kmax)
    u = np.log if utility == "log" else np.sqrt

    def gap(c):
        return float(np.sum(pk * u(w - c + prize)) - u(w))

    return float(brentq(gap, -1e9 if w <= 0 else 0.0, w + first * 0.999999))


def stpetersburg_ce_alone(utility: str = "sqrt", kmax: int = 200, first: float = 2.0) -> float:
    """The game's certainty equivalent ignoring wealth: u^-1(sum_k 2^-k u(prize_k)).  Cramer's square root gives
    about 2.9 for prizes 1, 2, 4, ...; the logarithm gives exactly 2 * ``first``."""
    _, pk, prize = _prizes(first, kmax)
    if utility == "sqrt":
        return float(np.sum(pk * np.sqrt(prize)) ** 2)
    return float(np.exp(np.sum(pk * np.log(prize))))


def stpetersburg_play(games: int, rng, first: float = 2.0) -> np.ndarray:
    """Prizes of simulated games: toss until heads; heads on toss k pays first * 2^(k-1)."""
    k = rng.geometric(0.5, size=games)
    return first * 2.0 ** (k - 1)


def stpetersburg_median_prize(games: int, first: float = 1.0, reps: int = 4000, seed: int = 0) -> float:
    """The median, over many sessions, of the average prize per game in a session of ``games`` games: what Hayden and
    Platt's median heuristic says a player bids per game.  It grows like log2(games) / 2 dollars (for first = 1)."""
    rng = np.random.default_rng(seed)
    means = [stpetersburg_play(games, rng, first).mean() for _ in range(reps)]
    return float(np.median(means))


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


def ez_resolution(c0: float, c1: float, c2_states, probs, beta: float, gamma: float, psi: float) -> dict:
    """Kreps and Porteus (1978), Epstein and Zin (1989): the same lottery over consumption at t = 2, its outcome learnt
    at t = 1 (early) or at t = 2 (late).  Expected utility (gamma = 1/psi) does not care; Epstein-Zin prefers early
    resolution when gamma > 1/psi.  ``premium`` is the share of c0 the chooser would give up to learn early."""
    rho = 1 - 1 / psi
    p = np.asarray(probs, float)
    c2 = np.asarray(c2_states, float)

    def agg(c, ce):
        return ((1 - beta) * c ** rho + beta * ce ** rho) ** (1 / rho)

    def ce(v):
        if abs(gamma - 1) < 1e-12:
            return float(np.exp(p @ np.log(v)))
        return float((p @ v ** (1 - gamma)) ** (1 / (1 - gamma)))

    early = agg(c0, ce(np.array([agg(c1, x) for x in c2])))
    late = agg(c0, agg(c1, ce(c2)))

    def v0(c):
        return agg(c, ce(np.array([agg(c1, x) for x in c2])))

    target = late
    prem = 0.0 if early <= late else float(brentq(lambda k: v0(c0 * (1 - k)) - target, 0.0, 0.999))
    return {"early": float(early), "late": float(late), "premium": prem, "prefers_early": bool(early > late + 1e-12)}


def beta_delta_path(w: float, T: int, beta: float, delta: float = 1.0, plan_only: bool = False) -> dict:
    """A cake of size w eaten over T periods with log utility and quasi-hyperbolic discounting (1, beta delta, beta
    delta^2, ...) and no interest.  ``plan`` is what the self at t = 0 plans for every period; ``naive`` what each
    self actually eats when it re-plans (with log utility the sophisticated self eats the same: Pollak 1968).
    ``commit`` is the plan locked in at t = 0 (a savings box that only opens on schedule)."""
    d = np.array([delta ** k for k in range(T)])

    def first_share(n):  # share of what is left that the current self eats, with n periods to go
        weights = np.r_[1.0, beta * d[1:n]]
        return 1.0 / weights.sum()

    wts = np.r_[1.0, beta * d[1:T]]
    plan = w * wts / wts.sum()
    eaten, left = [], w
    for t in range(T):
        c = left * first_share(T - t)
        eaten.append(c)
        left -= c
    return {"plan": plan, "naive": np.array(eaten), "commit": plan.copy(),
            "exponential": w * d / d.sum()}


def euler_regression(growth, rate, instruments=None) -> dict:
    """Hall (1988): consumption growth on the real interest rate.  The slope estimates the elasticity of
    intertemporal substitution.  OLS, and two-stage least squares on ``instruments`` (lagged variables: the ex post
    real rate is measured with error and time-averaged data make adjacent errors correlated, so Hall used lags of
    two years or more), with the first stage's F statistic."""
    g, r = np.asarray(growth, float), np.asarray(rate, float)
    X = np.c_[np.ones_like(r), r]
    b_ols = np.linalg.lstsq(X, g, rcond=None)[0]
    out = {"ols": float(b_ols[1]), "ols_const": float(b_ols[0]), "corr": float(np.corrcoef(r, g)[0, 1]), "n": len(g)}
    e = g - X @ b_ols
    XtXi = np.linalg.inv(X.T @ X)
    out["ols_se"] = float(np.sqrt(XtXi[1, 1] * (e @ e) / (len(g) - 2)))
    if instruments is not None:
        Z = np.c_[np.ones_like(r), np.asarray(instruments, float)]
        pi = np.linalg.lstsq(Z, r, rcond=None)[0]
        rh = Z @ pi
        u = r - rh
        k = Z.shape[1] - 1
        rss_u, rss_r = u @ u, ((r - r.mean()) @ (r - r.mean()))
        out["first_F"] = float(((rss_r - rss_u) / k) / (rss_u / (len(r) - k - 1)))
        Xh = np.c_[np.ones_like(r), rh]
        b = np.linalg.lstsq(Xh, g, rcond=None)[0]
        e2 = g - X @ b
        XhXi = np.linalg.inv(Xh.T @ Xh)
        out["iv"] = float(b[1])
        out["iv_const"] = float(b[0])
        out["iv_se"] = float(np.sqrt(XhXi[1, 1] * (e2 @ e2) / (len(g) - 2)))
    return out


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


def holt_laury_respond(gammas, noise: float, rng, scale: float = 1.0) -> np.ndarray:
    """Simulated respondents on the menu: each row, option A with probability Lambda((CE_A - CE_B) / noise) (a logit
    in certainty-equivalent dollars).  Returns a (people, 10) array of booleans, True for the safe choice."""
    menu = holt_laury_menu(scale)
    out = np.zeros((len(gammas), 10), bool)
    for i, gm in enumerate(gammas):
        for j, row in enumerate(menu):
            pa = (row["p"], 1 - row["p"])
            ca = certainty_equivalent(row["A"], pa, gamma=float(gm)) if abs(gm) > 1e-9 else float(np.dot(row["A"], pa))
            cb = certainty_equivalent(row["B"], pa, gamma=float(gm)) if abs(gm) > 1e-9 else float(np.dot(row["B"], pa))
            out[i, j] = rng.random() < expit((ca - cb) / noise)
    return out


def switches_back(choices) -> np.ndarray:
    """Which respondents switch from B back to A somewhere on the menu (inconsistent with any single gamma)."""
    c = np.asarray(choices, bool)
    return np.array([np.any(~row[:-1] & row[1:]) for row in c])


def hrs_threshold(cut: float) -> float:
    """Barsky, Juster, Kimball and Shapiro (1997): the CRRA chooser indifferent between a sure income and a 50-50
    chance of doubling it or cutting it by ``cut``.  Cuts of a half, a third and a fifth give 1, 2 and about 3.76."""

    def gap(gm):
        if abs(gm - 1) < 1e-12:
            return 0.5 * np.log(2) + 0.5 * np.log(1 - cut)
        return (0.5 * 2.0 ** (1 - gm) + 0.5 * (1 - cut) ** (1 - gm) - 1) / (1 - gm)

    if abs(gap(1.0)) < 1e-12:
        return 1.0
    return float(brentq(gap, 1e-6, 200.0))


def ellsberg_maxmin(black_range=(0.0, 2.0 / 3.0)) -> dict:
    """Ellsberg's urn (30 red; 60 black and yellow in unknown proportion), $100 bets, under maxmin expected utility
    (Gilboa and Schmeidler 1989): each bet valued at its worst chance of winning over the priors with p(black) in
    ``black_range``.  Bets: I red, II black, III red or yellow, IV black or yellow."""
    lo, hi = black_range
    grid = np.linspace(lo, hi, 201)
    red = 1 / 3
    bets = {"I": np.full_like(grid, red), "II": grid, "III": red + (2 / 3 - grid), "IV": np.full_like(grid, 2 / 3)}
    return {k: float(v.min()) for k, v in bets.items()} | {"single_prior_consistent": False}


def weighted_utility_line(k: float, u, w, n: int = 2):
    """Chew's weighted utility, V = sum p_i w_i u_i / sum p_i w_i, on three outcomes (worst, middle, best): its
    indifference curve V = k in the probability triangle is the straight line sum_i p_i w_i (u_i - k) = 0.  Returns
    two points (p_worst, p_best) on it, at p_worst = 0 and 1 (outside the triangle where they fall)."""
    (u1, u2, u3), (w1, w2, w3) = u, w
    pts = []
    for p1 in (0.0, 1.0):
        # p1 w1 (u1-k) + (1 - p1 - p3) w2 (u2-k) + p3 w3 (u3-k) = 0
        a = w3 * (u3 - k) - w2 * (u2 - k)
        b = p1 * w1 * (u1 - k) + (1 - p1) * w2 * (u2 - k)
        pts.append((p1, float(-b / a)))
    return pts


def weighted_utility_value(p_low: float, p_high: float, u, w) -> float:
    p = np.array([p_low, 1 - p_low - p_high, p_high])
    u, w = np.asarray(u, float), np.asarray(w, float)
    return float((p * w * u).sum() / (p * w).sum())


def tk_value(x, alpha: float = 0.88, lam: float = 2.25):
    """Tversky and Kahneman's (1992) value function: x^alpha for gains, -lam (-x)^alpha for losses."""
    x = np.asarray(x, float)
    return np.where(x >= 0, np.abs(x) ** alpha, -lam * np.abs(x) ** alpha)


def tk_weight(p, gamma: float = 0.61):
    """Their probability weighting function for gains: p^g / (p^g + (1 - p)^g)^(1/g)."""
    p = np.asarray(p, float)
    return p ** gamma / (p ** gamma + (1 - p) ** gamma) ** (1 / gamma)
