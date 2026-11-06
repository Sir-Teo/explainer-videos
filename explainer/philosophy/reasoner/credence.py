"""Degrees of belief, made computable (Part 13): coherence and the Dutch book found by linear programming, accuracy
and the Brier projection, proper scoring rules and synthetic forecasters, conditionalization (strict, diachronic and
Jeffrey), maximum entropy, Bertrand's chords and van Fraassen's cubes, dilation of credal sets, the lottery and
Leitgeb's stable sets, Sleeping Beauty by simulation, and the Doomsday argument under SSA and SIA.

    from explainer.philosophy.reasoner import credence as Cr
    Cr.dutch_book(worlds, props, cred)       # stakes that make the agent lose in every world, or None if coherent
    Cr.project_simplex([0.5, 0.4, 0.3])      # the nearest coherent credence: it is more accurate in every world
    Cr.bertrand(100000)                      # three 'random chords', three answers

Credences are assigned to propositions, each a set of worlds from a finite list; a credence function is coherent
when some probability on the worlds gives each proposition its credence.
"""

from __future__ import annotations

import math
import random
from fractions import Fraction

import numpy as np


# ---------------------------------------------------------------------------
# Coherence and the Dutch book
# ---------------------------------------------------------------------------
def dutch_book(worlds, props: dict, cred: dict) -> dict | None:
    """``props``: name -> set of worlds; ``cred``: name -> credence. Find stakes s (between -1 and 1) on the bets
    'pay 1 if A' priced at cred(A), such that the agent, who regards each as fair, loses in every world: maximize the
    guaranteed loss. Returns None if the credences are coherent (no sure loss exists), else the stakes and the loss
    in each world. Positive stake: the agent buys the bet; negative: she sells it."""
    from scipy.optimize import linprog
    names = list(props)
    n = len(names)
    # variables: s_1..s_n, t ; minimize t subject to sum_i s_i (1_A_i(w) - c_i) <= t for all w
    A_ub, b_ub = [], []
    for w in worlds:
        A_ub.append([(1.0 if w in props[a] else 0.0) - float(cred[a]) for a in names] + [-1.0])
        b_ub.append(0.0)
    c = [0.0] * n + [1.0]
    bounds = [(-1, 1)] * n + [(None, None)]
    res = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method="highs")
    t = res.x[-1]
    if t > -1e-9:
        return None
    stakes = {a: round(float(s), 6) for a, s in zip(names, res.x[:n])}
    payoff = {w: round(sum(stakes[a] * ((1.0 if w in props[a] else 0.0) - float(cred[a])) for a in names), 6)
              for w in worlds}
    return {"stakes": stakes, "payoff": payoff, "sure_loss": round(float(-t), 6)}


def coherent(worlds, props, cred) -> bool:
    return dutch_book(worlds, props, cred) is None


# ---------------------------------------------------------------------------
# Accuracy: the Brier score and the projection onto the simplex
# ---------------------------------------------------------------------------
def brier(c, world_index: int) -> float:
    """Squared distance from the credence vector over worlds to the truth vector of the given world."""
    return sum((ci - (1.0 if i == world_index else 0.0)) ** 2 for i, ci in enumerate(c))


def project_simplex(c) -> list[float]:
    """Euclidean projection onto the probability simplex (Duchi et al. 2008)."""
    v = np.asarray(c, float)
    u = np.sort(v)[::-1]
    css = np.cumsum(u)
    rho = np.nonzero(u * np.arange(1, len(v) + 1) > (css - 1))[0][-1]
    theta = (css[rho] - 1) / (rho + 1.0)
    return [float(x) for x in np.maximum(v - theta, 0)]


def dominance(c) -> dict:
    """De Finetti, Joyce, Predd et al.: the projection of an incoherent credence is closer to the truth in every
    world."""
    p = project_simplex(c)
    return {"incoherent": [float(x) for x in c], "projection": p,
            "brier_c": [brier(c, i) for i in range(len(c))], "brier_p": [brier(p, i) for i in range(len(c))],
            "dominates": all(brier(p, i) < brier(c, i) for i in range(len(c)))}


# ---------------------------------------------------------------------------
# Proper scoring rules and forecasters
# ---------------------------------------------------------------------------
def score(rule: str, q: float, outcome: int) -> float:
    """Penalty for reporting probability q of an event that then happens (outcome 1) or not (0); lower is better."""
    if rule == "brier":
        return (q - outcome) ** 2
    if rule == "log":
        return -math.log(q if outcome else 1 - q)
    if rule == "spherical":
        norm = math.sqrt(q * q + (1 - q) ** 2)
        return -(q if outcome else 1 - q) / norm
    if rule == "linear":
        return -(q if outcome else 1 - q)
    raise ValueError(rule)


def expected_score(rule: str, q: float, p: float) -> float:
    return p * score(rule, q, 1) + (1 - p) * score(rule, q, 0)


def best_report(rule: str, p: float, grid: int = 1000) -> float:
    """The report that minimizes the expected penalty when one's credence is p: p itself for a proper rule."""
    qs = [(i + 0.5) / grid for i in range(grid)]
    return min(qs, key=lambda q: expected_score(rule, q, p))


def forecasters(n: int = 2000, seed: int = 7) -> dict:
    """Events with true chances drawn at random; four forecasters: one who reports the chance, one overconfident (pushes
    reports towards 0 and 1), one timid (pulls them towards 1/2), one who always says 1/2. Mean Brier and log
    scores, and calibration in ten bins."""
    rnd = random.Random(seed)
    chances = [rnd.random() for _ in range(n)]
    outcomes = [1 if rnd.random() < p else 0 for p in chances]

    def clip(x):
        return min(max(x, 0.01), 0.99)
    styles = {
        "calibrated": lambda p: clip(p),
        "overconfident": lambda p: clip(0.5 + 1.6 * (p - 0.5)),
        "timid": lambda p: clip(0.5 + 0.4 * (p - 0.5)),
        "always 1/2": lambda p: 0.5,
    }
    out = {}
    for name, f in styles.items():
        reps = [f(p) for p in chances]
        b = sum(score("brier", q, o) for q, o in zip(reps, outcomes)) / n
        lg = sum(score("log", q, o) for q, o in zip(reps, outcomes)) / n
        bins = []
        for k in range(10):
            idx = [i for i, q in enumerate(reps) if k / 10 <= q < (k + 1) / 10 or (k == 9 and q == 1.0)]
            if idx:
                bins.append([k, sum(reps[i] for i in idx) / len(idx), sum(outcomes[i] for i in idx) / len(idx),
                             len(idx)])
        out[name] = {"brier": b, "log": lg, "bins": bins}
    return out


# ---------------------------------------------------------------------------
# Conditionalization: strict, diachronic, Jeffrey
# ---------------------------------------------------------------------------
def diachronic_book(e: float, c: float, q: float) -> dict:
    """Lewis's book against an agent with P(E) = e, P(H | E) = c, who plans to adopt P'(H) = q != c on learning E.
    Bet 1: a bet on H conditional on E, at price c (called off if not E). Bet 2: a bet paying (c - q) if E, at price
    e (c - q). If E, the bookie buys back bet 1 at the agent's new price q. The agent's net, world by world."""
    out = {}
    for w in ("E&H", "E&~H", "~E"):
        net = 0.0
        if w == "~E":
            net += -e * (c - q)
        else:
            win1 = 1.0 if w == "E&H" else 0.0
            # bet 1 bought at c, sold back at q before H is settled: the agent's net on it is q - c
            net += q - c
            net += (c - q) - e * (c - q)
            del win1
        out[w] = net
    return out


def jeffrey(prior_partition: dict, posterior_partition: dict, cond: dict) -> dict:
    """Jeffrey conditioning: new P(A) = sum_i P(A | E_i) P_new(E_i)."""
    old = sum(prior_partition[k] * cond[k] for k in prior_partition)
    new = sum(posterior_partition[k] * cond[k] for k in posterior_partition)
    return {"old": old, "new": new}


JEFFREY_CLOTH = {"prior": {"green": 0.3, "blue": 0.3, "violet": 0.4},
                 "post": {"green": 0.7, "blue": 0.25, "violet": 0.05},
                 "sold": {"green": 0.4, "blue": 0.4, "violet": 0.8}}


# ---------------------------------------------------------------------------
# Maximum entropy: Jaynes's Brandeis dice
# ---------------------------------------------------------------------------
def maxent_die(mean: float = 4.5, faces=(1, 2, 3, 4, 5, 6)) -> list[float]:
    """The distribution on the faces with the given mean and the largest entropy: p_k proportional to exp(lambda k),
    with lambda found by bisection."""
    def m(lam):
        w = [math.exp(lam * k) for k in faces]
        return sum(k * x for k, x in zip(faces, w)) / sum(w)
    lo, hi = -10.0, 10.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if m(mid) < mean:
            lo = mid
        else:
            hi = mid
    w = [math.exp(lo * k) for k in faces]
    s = sum(w)
    return [x / s for x in w]


# ---------------------------------------------------------------------------
# Bertrand's paradox (1889) and van Fraassen's cube factory
# ---------------------------------------------------------------------------
def chord_endpoints(rnd):
    a, b = rnd.uniform(0, 2 * math.pi), rnd.uniform(0, 2 * math.pi)
    return (math.cos(a), math.sin(a)), (math.cos(b), math.sin(b))


def chord_radius(rnd):
    t = rnd.uniform(0, 2 * math.pi)
    d = rnd.uniform(0, 1)
    h = math.sqrt(1 - d * d)
    cx, cy = d * math.cos(t), d * math.sin(t)
    ux, uy = -math.sin(t), math.cos(t)
    return (cx + h * ux, cy + h * uy), (cx - h * ux, cy - h * uy)


def chord_midpoint(rnd):
    while True:
        x, y = rnd.uniform(-1, 1), rnd.uniform(-1, 1)
        if x * x + y * y < 1:
            break
    d = math.hypot(x, y)
    h = math.sqrt(1 - d * d)
    ux, uy = (-y / d, x / d) if d > 0 else (1.0, 0.0)
    return (x + h * ux, y + h * uy), (x - h * ux, y - h * uy)


def bertrand(n: int = 100000, seed: int = 1889, keep: int = 300) -> dict:
    """Three ways to draw a chord 'at random' in the unit circle; the chance it is longer than the side of the
    inscribed equilateral triangle (sqrt 3). Exact answers 1/3, 1/2, 1/4."""
    side = math.sqrt(3)
    out = {}
    for name, f, exact in (("endpoints", chord_endpoints, 1 / 3), ("radius", chord_radius, 1 / 2),
                           ("midpoint", chord_midpoint, 1 / 4)):
        rnd = random.Random(seed)
        hits = 0
        sample = []
        for i in range(n):
            p, q = f(rnd)
            if math.dist(p, q) > side:
                hits += 1
            if i < keep:
                sample.append([round(p[0], 4), round(p[1], 4), round(q[0], 4), round(q[1], 4)])
        out[name] = {"freq": hits / n, "exact": exact, "sample": sample}
    return out


def cube_factory() -> dict:
    """A factory makes cubes with sides between 0 and 1 cm. Indifference over side length: P(side <= 1/2) = 1/2.
    Indifference over face area: P(area <= 1/4) = 1/4. Over volume: P(volume <= 1/8) = 1/8. The same event."""
    return {"side": 0.5, "area": 0.25, "volume": 0.125}


# ---------------------------------------------------------------------------
# Imprecise credences: dilation (Seidenfeld and Wasserman 1993)
# ---------------------------------------------------------------------------
def dilation(k: int = 11) -> dict:
    """H: a fair coin lands heads (credence exactly 1/2). G: a proposition about which one has no idea (credal set:
    every P(G) in [0, 1]), independent of the coin. Learn M: 'the coin matches G' (H iff G). Before: P(H) = 1/2 for
    every member. After: P(H | M) = P(G), anywhere in [0, 1]: learning dilates the credence."""
    rows = []
    for i in range(k):
        g = i / (k - 1)
        pm = 0.5 * g + 0.5 * (1 - g)
        ph_m = (0.5 * g) / pm
        rows.append({"P(G)": g, "P(H)": 0.5, "P(M)": pm, "P(H|M)": ph_m})
    return {"rows": rows, "before": [0.5, 0.5], "after": [min(r["P(H|M)"] for r in rows),
                                                          max(r["P(H|M)"] for r in rows)]}


# ---------------------------------------------------------------------------
# The lottery; the Lockean thesis; Leitgeb's stable sets
# ---------------------------------------------------------------------------
def lottery(n: int = 1000, threshold: float = 0.99) -> dict:
    p_lose = 1 - 1 / n
    return {"n": n, "p_each_loses": p_lose, "believe_each": p_lose > threshold, "p_all_lose": 0.0,
            "believe_all": False}


def preface(n: int = 300, each: float = 0.99) -> dict:
    """An author believes each of n claims in her book, each with credence 0.99; independent, the chance all are
    true is 0.99^n."""
    return {"n": n, "each": each, "all": each ** n}


def stable_sets(probs: dict, r: float = 0.5) -> list[list]:
    """Leitgeb's P-stable^r propositions: A (with P(A) > 0) such that P(A | B) > r for every B consistent with A and
    of positive probability. For r = 1/2 these are exactly the sets each of whose worlds outweighs everything
    outside: P({w}) > P(W - A) for all w in A. Returned smallest first (they are nested)."""
    ws = sorted(probs, key=lambda w: -probs[w])
    out = []
    for k in range(1, len(ws) + 1):
        A = ws[:k]
        rest = sum(probs[w] for w in ws[k:])
        if all(probs[w] * (1 - r) > rest * r + 1e-15 or (rest == 0) for w in A):
            out.append(A)
    return out


# ---------------------------------------------------------------------------
# Sleeping Beauty (Elga 2000; Lewis 2001)
# ---------------------------------------------------------------------------
def sleeping_beauty(runs: int = 100000, seed: int = 2000) -> dict:
    """Sunday: Beauty sleeps; a fair coin is tossed. Heads: woken Monday only. Tails: woken Monday and Tuesday, the
    Monday memory erased. Count heads among experiments and among awakenings; and the break-even price for a bet on
    heads offered at every awakening."""
    rnd = random.Random(seed)
    heads_exp = 0
    awak = 0
    heads_awak = 0
    for _ in range(runs):
        h = rnd.random() < 0.5
        heads_exp += h
        k = 1 if h else 2
        awak += k
        heads_awak += h * 1
    per_exp = heads_exp / runs
    per_awak = heads_awak / awak
    # a ticket 'pays $1 if heads', sold to Beauty at price x at each awakening: profit per experiment
    # heads: 1 awakening, +1 - x; tails: 2 awakenings, -2x. Expected: 0.5(1 - x) - x = 0 at x = 1/3
    return {"runs": runs, "heads_per_experiment": per_exp, "heads_per_awakening": per_awak,
            "breakeven_per_awakening": 1 / 3, "breakeven_per_experiment": 1 / 2}


# ---------------------------------------------------------------------------
# Anthropic reasoning: the Doomsday argument; SSA and SIA
# ---------------------------------------------------------------------------
def doomsday(rank: float = 1e11, n_soon: float = 2e11, n_late: float = 2e14, prior_soon: float = 0.5) -> dict:
    """Two hypotheses about how many humans will ever live. Under SSA, your birth rank is a random draw from all
    humans who ever live (likelihood 1/N); under SIA, worlds with more observers are proportionally likelier to be
    yours, which cancels the shift exactly."""
    lik_soon = 1 / n_soon if rank <= n_soon else 0.0
    lik_late = 1 / n_late if rank <= n_late else 0.0
    ssa = prior_soon * lik_soon / (prior_soon * lik_soon + (1 - prior_soon) * lik_late)
    # SIA: multiply the prior by N first
    w_soon = prior_soon * n_soon
    w_late = (1 - prior_soon) * n_late
    sia_prior = w_soon / (w_soon + w_late)
    sia = sia_prior * lik_soon / (sia_prior * lik_soon + (1 - sia_prior) * lik_late)
    return {"prior_soon": prior_soon, "ssa_soon": ssa, "sia_prior_soon": sia_prior, "sia_soon": sia,
            "presumptuous_factor": n_late / n_soon}
