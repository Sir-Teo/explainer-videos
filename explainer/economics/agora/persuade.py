"""Agora's information and persuasion (Part 53): what a player can achieve by controlling what others learn.

* **Bayesian persuasion** (:func:`prosecutor`, :func:`concavify`, :func:`persuade_lp`): Kamenica and Gentzkow's
  (2011) prosecutor; the concave closure of a sender's value over beliefs for a binary state, drawn; the optimal
  signal for finitely many states by linear programming over a grid of posteriors.
* **Cheap talk** (:func:`cheap_talk`): Crawford and Sobel's (1982) uniform-quadratic partition equilibria, their
  boundaries and both players' expected losses.
* **Information design with many receivers** (:func:`bce_lp`): Bergemann and Morris's (2019) Bayes correlated
  equilibria of a finite game by linear programming, for any objective.
* **Blackwell's order** (:func:`garbling`, :func:`decision_value`): whether one experiment is a garbling of another,
  by linear programming, and what each is worth in a decision problem.
* **Common knowledge** (:func:`dialogue`, :func:`email_game`): Geanakoplos and Polemarchakis's (1982) dialogue to
  agreement (Aumann 1976); Rubinstein's (1989) email game and the probability that the other has seen one message
  fewer.
* **Global games** (:func:`global_game`): Morris and Shin's (2003) regime-change game with a normal prior: the
  threshold, and the condition under which it is unique.
* **Herds** (:func:`cascade_chain`, :func:`cascade_sim`): Bikhchandani, Hirshleifer and Welch's (1992) cascades,
  exactly as a Markov chain and by simulation.
* **Reputation** (:func:`chain_store`): Kreps and Wilson's (1982) sequential equilibrium of the chain store.
* **Bargaining** (:func:`nash_bargaining`, :func:`rubinstein`, :func:`coase_two_period`): Nash's solution on a
  frontier; Rubinstein's alternating offers; a seller facing a buyer of unknown value over two periods, with delay.
* **Relational contracts** (:func:`relational`): Levin's (2003) self-enforcing bonus and the effort it supports.

numpy and scipy only.
"""

from __future__ import annotations

import numpy as np
from scipy.optimize import brentq, linprog
from scipy.stats import norm

# ---------------------------------------------------------------------------------------------------------------
# Bayesian persuasion


def prosecutor(prior: float = 0.3, threshold: float = 0.5) -> dict:
    """Kamenica and Gentzkow's prosecutor. The judge convicts when the probability of guilt is at least
    ``threshold``. Full disclosure convicts the guilty only; no information convicts nobody (if prior < threshold);
    the optimal investigation recommends conviction for every guilty defendant and for just enough innocent ones that
    the judge's posterior after "convict" equals the threshold."""
    full = prior
    none = 1.0 if prior >= threshold else 0.0
    if prior >= threshold:
        p_inn = 1.0
    else:
        p_inn = prior * (1 - threshold) / (threshold * (1 - prior))
    convict = prior + (1 - prior) * p_inn
    post_c = prior / convict
    return {"prior": prior, "threshold": threshold, "full": full, "none": none, "optimal": convict,
            "signal": {"guilty": (1.0, 0.0), "innocent": (p_inn, 1 - p_inn)}, "posterior_convict": post_c,
            "posterior_acquit": 0.0, "innocent_convicted": (1 - prior) * p_inn,
            "bound": min(1.0, prior / threshold)}


def concavify(mu, v) -> np.ndarray:
    """The concave closure of the values ``v`` on the belief grid ``mu`` (sorted, in [0, 1]): the smallest concave
    function above v, as the upper convex hull of the points."""
    mu, v = np.asarray(mu, float), np.asarray(v, float)
    hull = []
    for i in range(len(mu)):
        while len(hull) >= 2:
            j, k = hull[-2], hull[-1]
            cross = (mu[k] - mu[j]) * (v[i] - v[j]) - (v[k] - v[j]) * (mu[i] - mu[j])
            if cross >= 0:
                hull.pop()
            else:
                break
        hull.append(i)
    return np.interp(mu, mu[hull], v[hull])


def persuade_lp(prior, posteriors, values) -> dict:
    """The sender's best signal for finitely many states: choose probabilities tau_k on candidate posteriors
    (rows of ``posteriors``) to maximize sum tau_k values_k subject to Bayes plausibility, sum tau_k posterior_k =
    prior. Returns the value and the posteriors used."""
    Pm = np.asarray(posteriors, float)
    vals = np.asarray(values, float)
    K, n = Pm.shape
    A_eq = np.vstack([Pm.T, np.ones(K)])
    b_eq = np.concatenate([np.asarray(prior, float), [1.0]])
    res = linprog(-vals, A_eq=A_eq, b_eq=b_eq, bounds=[(0, None)] * K, method="highs")
    tau = res.x
    used = [k for k in range(K) if tau[k] > 1e-9]
    return {"value": float(-res.fun), "tau": tau, "used": used, "posteriors": Pm[used], "weights": tau[used]}


def simplex_grid(n_states: int, steps: int) -> np.ndarray:
    """Every belief over ``n_states`` states with coordinates in multiples of 1/steps."""
    out = []

    def rec(prefix, left, k):
        if k == 1:
            out.append(prefix + [left])
            return
        for i in range(left + 1):
            rec(prefix + [i], left - i, k - 1)

    rec([], steps, n_states)
    return np.array(out, float) / steps


# ---------------------------------------------------------------------------------------------------------------
# cheap talk


def cheap_talk(b: float, N: int | None = None) -> dict:
    """Crawford and Sobel's uniform-quadratic game: the state is uniform on [0, 1], the receiver wants to match it,
    the sender wants the state plus a bias ``b``. A partition equilibrium with N intervals has boundaries
    a_i = i/N + 2 b i (i - N); N can be at most the largest integer below 1/2 + sqrt(1/4 + 1/(2b)). Returns the
    boundaries, the actions and both players' expected losses (the receiver's is the variance within intervals)."""
    n_max = int(np.ceil(-0.5 + 0.5 * np.sqrt(1 + 2 / b))) if b > 0 else 10 ** 6
    N = n_max if N is None else N
    if N > n_max:
        raise ValueError(f"no equilibrium with {N} intervals when b = {b}")
    i = np.arange(N + 1)
    a = i / N + 2 * b * i * (i - N)
    widths = np.diff(a)
    actions = (a[:-1] + a[1:]) / 2
    rloss = float(np.sum(widths ** 3) / 12)
    sloss = rloss + b ** 2
    return {"b": b, "N": N, "n_max": n_max, "bounds": a, "actions": actions, "receiver_loss": rloss,
            "sender_loss": sloss, "babbling_loss": 1 / 12}


# ---------------------------------------------------------------------------------------------------------------
# information design with many receivers: Bayes correlated equilibrium


def bce_lp(prior, payoffs, objective) -> dict:
    """Bayes correlated equilibria of a two-player game with finitely many states. ``payoffs[i][t]`` is player i's
    payoff matrix in state t (rows: player 0's action, columns: player 1's); ``objective[t]`` the designer's matrix.
    The designer chooses sigma(a | t) to maximize the expected objective subject to obedience: no player gains by
    deviating from a recommended action, given what the recommendation reveals about the state and the other's
    action. Returns the value and the decision rule."""
    prior = np.asarray(prior, float)
    nT = len(prior)
    U0 = [np.asarray(payoffs[0][t], float) for t in range(nT)]
    U1 = [np.asarray(payoffs[1][t], float) for t in range(nT)]
    m, n = U0[0].shape
    nv = nT * m * n

    def idx(t, i, j):
        return (t * m + i) * n + j

    c = np.zeros(nv)
    for t in range(nT):
        O = np.asarray(objective[t], float)
        for i in range(m):
            for j in range(n):
                c[idx(t, i, j)] = -prior[t] * O[i, j]
    A_ub, b_ub = [], []
    for i in range(m):
        for i2 in range(m):
            if i2 == i:
                continue
            row = np.zeros(nv)
            for t in range(nT):
                for j in range(n):
                    row[idx(t, i, j)] = -prior[t] * (U0[t][i, j] - U0[t][i2, j])
            A_ub.append(row)
            b_ub.append(0.0)
    for j in range(n):
        for j2 in range(n):
            if j2 == j:
                continue
            row = np.zeros(nv)
            for t in range(nT):
                for i in range(m):
                    row[idx(t, i, j)] = -prior[t] * (U1[t][i, j] - U1[t][i, j2])
            A_ub.append(row)
            b_ub.append(0.0)
    A_eq, b_eq = [], []
    for t in range(nT):
        row = np.zeros(nv)
        row[t * m * n:(t + 1) * m * n] = 1.0
        A_eq.append(row)
        b_eq.append(1.0)
    res = linprog(c, A_ub=np.array(A_ub), b_ub=np.array(b_ub), A_eq=np.array(A_eq), b_eq=np.array(b_eq),
                  bounds=[(0, None)] * nv, method="highs")
    sig = res.x.reshape(nT, m, n)
    return {"value": float(-res.fun), "sigma": sig, "status": res.status}


# ---------------------------------------------------------------------------------------------------------------
# Blackwell's order


def garbling(P, Q) -> dict:
    """Is experiment Q a garbling of experiment P? P and Q are row-stochastic matrices of signal probabilities given
    the state (states in rows). Q is a garbling if Q = P M for a row-stochastic M; then P is more informative in
    Blackwell's sense: every decision maker weakly prefers it. Feasibility by linear programming."""
    P, Q = np.asarray(P, float), np.asarray(Q, float)
    nS, nP = P.shape
    nQ = Q.shape[1]
    nv = nP * nQ
    A_eq, b_eq = [], []
    for s in range(nS):
        for q in range(nQ):
            row = np.zeros(nv)
            for p in range(nP):
                row[p * nQ + q] = P[s, p]
            A_eq.append(row)
            b_eq.append(Q[s, q])
    for p in range(nP):
        row = np.zeros(nv)
        row[p * nQ:(p + 1) * nQ] = 1.0
        A_eq.append(row)
        b_eq.append(1.0)
    res = linprog(np.zeros(nv), A_eq=np.array(A_eq), b_eq=np.array(b_eq), bounds=[(0, None)] * nv, method="highs")
    ok = res.status == 0
    return {"garbling": ok, "M": res.x.reshape(nP, nQ) if ok else None}


def decision_value(prior, P, U) -> float:
    """The expected payoff of a decision maker with ``prior`` over states who sees a signal from experiment ``P``
    (states x signals) and then chooses the action maximizing U (states x actions) given the posterior."""
    prior, P, U = np.asarray(prior, float), np.asarray(P, float), np.asarray(U, float)
    joint = prior[:, None] * P
    total = 0.0
    for s in range(P.shape[1]):
        col = joint[:, s]
        if col.sum() <= 0:
            continue
        total += float(np.max(col @ U))
    return total


# ---------------------------------------------------------------------------------------------------------------
# common knowledge


def dialogue(prior, event, part_a, part_b, true_state: int, rounds: int = 20) -> dict:
    """Geanakoplos and Polemarchakis's dialogue. Two people share a ``prior`` over finitely many states and know the
    state only up to their partitions (lists of cells, each a list of states). They take turns announcing their
    posterior probability of ``event`` (a set of states); each announcement is common knowledge and refines what the
    other knows. Returns the announced posteriors, round by round, until they agree."""
    prior = np.asarray(prior, float)
    n = len(prior)
    ev = np.zeros(n, bool)
    ev[list(event)] = True

    def cell_of(part, s):
        for c in part:
            if s in c:
                return c
        raise ValueError(s)

    public = np.ones(n, bool)
    history = []
    parts = [part_a, part_b]
    for r in range(rounds):
        who = r % 2
        post = {}
        for s in range(n):
            if not public[s]:
                continue
            info = np.zeros(n, bool)
            info[cell_of(parts[who], s)] = True
            info &= public
            post[s] = float(prior[info & ev].sum() / prior[info].sum())
        said = post[true_state]
        history.append({"round": r, "who": "AB"[who], "posterior": said})
        public = np.array([public[s] and abs(post.get(s, -1) - said) < 1e-12 for s in range(n)])
        if len(history) >= 2 and abs(history[-1]["posterior"] - history[-2]["posterior"]) < 1e-12:
            break
    return {"history": history, "agreed": abs(history[-1]["posterior"] - history[-2]["posterior"]) < 1e-12}


def email_game(eps: float = 0.1, p: float = 0.2, a: float = 2.0, b: float = 3.0, L: float = 3.5) -> dict:
    """Rubinstein's email game. In the rare state (probability p) both gain ``a`` by attacking together; attacking
    alone costs ``L``; the safe action pays 0. Each message confirming the last is lost with probability eps. A
    player who has seen t messages puts probability z = 1 / (2 - eps) > 1/2 on the other having seen one fewer.
    Attacking needs a belief of at least L / (a + L) that the other attacks. The player who has seen nothing plays
    safe; so a player with one message thinks the other safe with probability z, and so on up: if 1 - z falls short
    of L / (a + L) the induction unravels and nobody ever attacks, however many messages were exchanged."""
    z = 1.0 / (2.0 - eps)
    need = L / (a + L)
    unravels = (1 - z) < need
    return {"z": z, "need": need, "unravels": bool(unravels), "eps": eps, "p": p}


# ---------------------------------------------------------------------------------------------------------------
# global games


def global_game(c: float = 0.4, sigma: float = 0.1, prior_mean: float | None = None, prior_sd: float | None = None
                ) -> dict:
    """Morris and Shin's regime change. A continuum of players each attack (cost c, gain 1 if the regime falls) or
    not; the regime falls if the share attacking is at least the fundamental theta. Each sees x = theta + sigma eps.
    With a flat prior: theta* = 1 - c and x* = theta* + sigma Phi^-1(theta*). With a normal prior N(y, 1/alpha) and
    private precision beta = 1/sigma^2, the threshold solves a fixed point that is unique when
    alpha / sqrt(beta) < sqrt(2 pi); otherwise there can be several."""
    if prior_mean is None:
        th = 1 - c
        return {"theta": th, "x": th + sigma * norm.ppf(th), "unique": True, "flat": True}
    alpha, beta = 1 / prior_sd ** 2, 1 / sigma ** 2
    y = prior_mean
    gamma = alpha / (alpha + beta)

    def g(th):
        x = th + sigma * norm.ppf(th)
        m = gamma * y + (1 - gamma) * x
        s = 1 / np.sqrt(alpha + beta)
        return norm.cdf((th - m) / s) - c

    grid = np.linspace(1e-4, 1 - 1e-4, 4001)
    vals = np.array([g(t) for t in grid])
    roots = []
    for i in range(len(grid) - 1):
        if vals[i] == 0 or vals[i] * vals[i + 1] < 0:
            roots.append(float(brentq(g, grid[i], grid[i + 1])))
    unique = alpha / np.sqrt(beta) < np.sqrt(2 * np.pi)
    return {"thetas": roots, "unique_condition": bool(unique), "ratio": float(alpha / np.sqrt(beta)),
            "bound": float(np.sqrt(2 * np.pi)), "flat": False}


# ---------------------------------------------------------------------------------------------------------------
# herds and cascades


def cascade_chain(q: float = 0.7, n: int = 20) -> dict:
    """Bikhchandani, Hirshleifer and Welch's cascade with a prior of one half and private signals right with
    probability ``q``; an indifferent person follows their own signal. Track d, the number of revealed signals for
    the true state minus against it: a cascade starts when |d| reaches 2 and then nobody's action reveals anything.
    Returns, person by person, the probabilities of being in a right cascade, a wrong one, or none yet."""
    right, wrong, none = [], [], []
    dist = {0: 1.0}
    pr, pw = 0.0, 0.0
    for t in range(n):
        new = {}
        for d, pmass in dist.items():
            for step, ps in ((1, q), (-1, 1 - q)):
                nd = d + step
                if nd >= 2:
                    pr += pmass * ps
                elif nd <= -2:
                    pw += pmass * ps
                else:
                    new[nd] = new.get(nd, 0.0) + pmass * ps
        dist = new
        right.append(pr)
        wrong.append(pw)
        none.append(sum(dist.values()))
    limit_right = q * q / (q * q + (1 - q) ** 2)
    return {"right": right, "wrong": wrong, "none": none, "limit_right": limit_right,
            "limit_wrong": 1 - limit_right}


def cascade_sim(q: float = 0.7, n: int = 30, runs: int = 10000, seed: int = 0) -> dict:
    """The same cascade by simulation: the share of runs ending in the right action, and a few runs' actions."""
    rng = np.random.default_rng(seed)
    correct = np.zeros(runs, bool)
    examples = []
    for r in range(runs):
        d = 0
        acts = []
        for _ in range(n):
            s = 1 if rng.random() < q else -1
            if d >= 2:
                a = 1
            elif d <= -2:
                a = -1
            else:
                a = s
                d += s
            acts.append(a)
        correct[r] = acts[-1] == 1
        if r < 6:
            examples.append(acts)
    return {"share_right": float(correct.mean()), "examples": examples}


# ---------------------------------------------------------------------------------------------------------------
# reputation


def chain_store(n: int = 20, delta: float = 0.05, b: float = 0.5, a: float = 2.0) -> dict:
    """Kreps and Wilson's chain store, ``n`` markets, a prior ``delta`` that the incumbent is tough (always fights),
    entrants who gain b if accommodated, b - 1 if fought, 0 if out. With k markets left and reputation p, an entrant
    stays out if p > b^k; a weak incumbent fights (or randomizes so that the reputation after a fight is b^(k-1)).
    Returns, along the path where every fight is observed, the reputation, the entrants' choice and the weak
    incumbent's probability of fighting; and k_star, the number of final markets in which entry can occur (b^k >=
    delta)."""
    p = delta
    rows = []
    for k in range(n, 0, -1):
        thresh = b ** k
        if p > thresh:
            enter = 0.0
        elif abs(p - thresh) < 1e-12:
            enter = 1 / a
        else:
            enter = 1.0
        nxt = b ** (k - 1)
        if k == 1:
            fight = 0.0
        elif p >= nxt:
            fight = 1.0
        else:
            fight = p * (1 - nxt) / ((1 - p) * nxt)
        rows.append({"k": k, "reputation": p, "threshold": thresh, "enter": enter, "weak_fights": fight})
        if enter > 0 and k > 1:
            p = p / (p + (1 - p) * fight) if fight > 0 else p
    k_star = int(np.floor(np.log(delta) / np.log(b)))
    return {"rows": rows, "k_star": k_star, "delta": delta, "b": b}


# ---------------------------------------------------------------------------------------------------------------
# bargaining


def nash_bargaining(frontier_x, frontier_y, d=(0.0, 0.0)) -> dict:
    """Nash's solution: the point on the frontier maximizing (x - d1)(y - d2)."""
    x, y = np.asarray(frontier_x, float), np.asarray(frontier_y, float)
    prod = np.where((x > d[0]) & (y > d[1]), (x - d[0]) * (y - d[1]), -np.inf)
    k = int(np.argmax(prod))
    return {"x": float(x[k]), "y": float(y[k]), "product": float(prod[k])}


def rubinstein(delta1: float, delta2: float | None = None) -> dict:
    """Rubinstein's alternating offers over a pie of one: the first proposer gets (1 - delta2)/(1 - delta1 delta2),
    at once."""
    delta2 = delta1 if delta2 is None else delta2
    x = (1 - delta2) / (1 - delta1 * delta2)
    return {"first": x, "second": 1 - x, "delay": 0}


def coase_two_period(v_high: float = 1.0, v_low: float = 0.4, share_high: float = 0.5, delta: float = 0.8) -> dict:
    """A seller who cannot commit sells to a buyer of value v_high or v_low over two periods, discount delta. Once
    the high type has bought, the seller cuts the price to v_low, and a high-value buyer foresees it: it accepts p1
    only if v_high - p1 >= delta (v_high - v_low). So the seller either screens (high buys now at that price, low
    later: delay for the low type) or sells to both at once at v_low; screening pays when share_high > v_low.
    A seller who could commit never to cut the price would sell to the high type alone at v_high. Returns the best
    plan, the prices and the probability of delay."""
    p1 = v_high - delta * (v_high - v_low)
    plans = [{"plan": "screen", "p1": p1, "p2": v_low,
              "profit": share_high * p1 + (1 - share_high) * delta * v_low, "delay": 1 - share_high},
             {"plan": "pool", "p1": v_low, "p2": None, "profit": v_low, "delay": 0.0}]
    best = max(plans, key=lambda r: r["profit"])
    commit = max(share_high * v_high, v_low)
    return {"best": best, "plans": plans, "commitment_profit": commit}


# ---------------------------------------------------------------------------------------------------------------
# relational contracts


def relational(delta, theta: float = 1.0, c: float = 0.5, outside: float = 0.0) -> dict:
    """A relational contract in the spirit of Bull (1987) and Levin (2003): effort e produces theta e and costs the
    worker c e^2 / 2; it is rewarded by a bonus the firm could refuse to pay. The bonus must cover the cost of the
    effort, b = c e^2 / 2, and the firm pays only if the bonus is no more than the discounted value of the
    relationship: b <= delta/(1 - delta) (theta e - c e^2/2 - outside). Returns the highest enforceable effort
    for each delta (first best theta / c; with outside = 0 it is 2 delta theta / c up to delta = 1/2)."""
    deltas = np.atleast_1d(np.asarray(delta, float))
    first = theta / c
    out = []
    for d in deltas:
        k = d / (1 - d)

        def slack(e):
            return k * (theta * e - c * e * e / 2 - outside) - c * e * e / 2

        if slack(first) >= 0:
            out.append(first)
            continue
        grid = np.linspace(1e-6, first, 2001)
        ok = grid[[slack(e) >= 0 for e in grid]]
        out.append(float(ok.max()) if len(ok) else 0.0)
    need = theta ** 2 / (2 * c)
    surplus = theta ** 2 / (2 * c) - outside
    return {"delta": deltas.tolist(), "effort": out, "first_best": first,
            "delta_star": float(need / (need + surplus)) if surplus > 0 else None}


__all__ = ["prosecutor", "concavify", "persuade_lp", "simplex_grid", "cheap_talk", "bce_lp", "garbling",
           "decision_value", "dialogue", "email_game", "global_game", "cascade_chain", "cascade_sim", "chain_store",
           "nash_bargaining", "rubinstein", "coase_two_period", "relational"]
