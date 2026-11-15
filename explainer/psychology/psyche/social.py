"""Psyche's social world (Parts 34 and 35): how what one person does depends on what the others in the room are doing, and
the mathematics the famous influence studies never had.

* :func:`cascade` and :func:`cascade_size`: Granovetter's threshold model of collective behaviour.  Each person joins
  once the number already in has reached their threshold; the outcome depends on the whole distribution of
  thresholds, so two crowds that differ by one person can end in opposite places.  :func:`cascade_curve` sweeps the
  spread of a normal threshold distribution and finds the jump.
* :func:`degroot`: repeated weighted averaging of neighbours' opinions; with a connected, aperiodic trust matrix
  everyone converges to one consensus, a weighted average of the starting opinions whose weights are the left
  eigenvector of the matrix (:func:`influence_weights`).
* :func:`bounded_confidence`: Hegselmann and Krause's model, in which people average only the opinions within a
  distance eps of their own; small eps leaves several clusters that never meet (about 1/(2 eps) of them).
* :func:`ring_lattice`, :func:`rewire` and :func:`contagion`: simple and complex contagion on a clustered lattice and
  on a rewired, random-looking one.  A simple contagion (one contact suffices) travels faster when ties are random;
  a complex one (two contacts needed) spreads through the clustered network and stalls in the random one (Centola).
* :func:`crowd` and :func:`influence_rounds`: the diversity prediction identity, collective squared error = average
  individual squared error - diversity, and what rounds of looking at the others' mean do to a crowd: its diversity
  falls, its error does not, and the truth can fall outside the range people now give (Lorenz et al.).
* :func:`music_market`: a cumulative-advantage market in the spirit of Salganik, Dodds and Watts's Music Lab:
  independent and social worlds, with the inequality (Gini) and unpredictability of the outcomes.
* :func:`bystanders`: the chance at least one of N people helps when each one's chance falls with N as p1 N^-beta.
  With beta = 1 the group's chance barely moves: diffusion of responsibility alone need not make help rarer.
* :func:`social_impact`: Latané's psychosocial law, impact = s N^t with t < 1: each added source adds less.
* :func:`drive`: Zajonc's account of social facilitation: an audience raises drive, which multiplies response
  strengths, so the dominant response gets more likely; a well-learned task improves and a new one gets worse.
* :func:`mentions`: Stasser and Titus's information-sampling model of a hidden profile: an item known to k of the
  group is mentioned with chance 1 - (1 - p)^k, so shared items dominate the discussion.

Part 35 adds reading minds:

* :func:`grid_distances`, :func:`action_probs` and :func:`goal_posterior`: inverse planning (Baker, Saxe and
  Tenenbaum).  A noisily rational agent walks a gridworld toward one of several goals, choosing moves by a softmax
  over its planner's values (Part 17); watching its path, Bayes' rule gives the posterior over its goal.
* :func:`kelley`: Kelley's covariation cube (persons x entities x occasions) as an analysis of variance, with the
  three cues of consensus, distinctiveness and consistency.
* :func:`dunning_kruger`: the famous quartile plot produced by a modest correlation between actual and
  self-assessed skill (regression to the mean) plus a better-than-average shift, with no extra ignorance at the
  bottom.

Everything here is a simulated model and is labelled simulated; it does not stand in for any study's data.  Nothing
here imports manim.
"""

from __future__ import annotations

import numpy as np

__all__ = ["cascade", "cascade_size", "cascade_curve", "degroot", "influence_weights", "bounded_confidence",
           "clusters", "ring_lattice", "rewire", "contagion", "crowd", "influence_rounds", "gini", "music_market",
           "bystanders", "social_impact", "drive", "mentions", "grid_distances", "action_probs", "goal_posterior",
           "kelley", "dunning_kruger"]


# ---------------------------------------------------------------- thresholds

def cascade(thresholds) -> np.ndarray:
    """Granovetter's process: at each step everyone whose threshold is at most the current number in joins.  Returns
    the number in after each step, from 0 until nothing changes.  Thresholds are counts of other people."""
    t = np.sort(np.asarray(thresholds, float))
    path = [0]
    while True:
        n = int(np.sum(t <= path[-1]))
        if n == path[-1]:
            return np.array(path)
        path.append(n)


def cascade_size(thresholds) -> int:
    """The number who end up joining: the first fixed point of n -> #{threshold <= n}, reached from 0."""
    return int(cascade(thresholds)[-1])


def cascade_curve(n: int = 100, mean: float = 25.0, sds=None, seed: int = 0, quantile: bool = True) -> dict:
    """Final cascade size as the spread of a normal threshold distribution grows.  With ``quantile`` the thresholds
    are the normal quantiles at (i + 1/2)/n (no sampling noise, so the jump is sharp); otherwise they are drawn."""
    from scipy.stats import norm
    sds = np.linspace(1, 30, 59) if sds is None else np.asarray(sds, float)
    rng = np.random.default_rng(seed)
    out = []
    for s in sds:
        if quantile:
            t = mean + s * norm.ppf((np.arange(n) + 0.5) / n)
        else:
            t = rng.normal(mean, s, n)
        out.append(cascade_size(np.maximum(t, 0)))
    return {"sd": sds, "size": np.array(out)}


# ---------------------------------------------------------------- opinions

def degroot(W, x0, steps: int = 50) -> np.ndarray:
    """DeGroot's model: x(t+1) = W x(t), with W row-stochastic (each row is whom a person listens to, and how much).
    Returns the (steps+1) x n path."""
    W = np.asarray(W, float)
    if not np.allclose(W.sum(axis=1), 1):
        raise ValueError("rows of W must sum to 1")
    x = np.asarray(x0, float)
    path = [x]
    for _ in range(steps):
        x = W @ x
        path.append(x)
    return np.array(path)


def influence_weights(W) -> np.ndarray:
    """The left eigenvector of W for eigenvalue 1, normalised to sum to 1: each person's weight in the consensus."""
    vals, vecs = np.linalg.eig(np.asarray(W, float).T)
    v = np.real(vecs[:, np.argmin(np.abs(vals - 1))])
    return v / v.sum()


def bounded_confidence(x0, eps: float, steps: int = 40) -> np.ndarray:
    """Hegselmann-Krause: each person moves to the mean of all opinions within eps of their own (their own
    included).  Returns the (steps+1) x n path."""
    x = np.asarray(x0, float)
    path = [x]
    for _ in range(steps):
        near = np.abs(x[:, None] - x[None, :]) <= eps
        x = (near @ x) / near.sum(axis=1)
        path.append(x)
    return np.array(path)


def clusters(x, tol: float = 1e-3) -> int:
    """The number of distinct opinion clusters at the end: values closer than tol count as one."""
    s = np.sort(np.asarray(x, float))
    return int(1 + np.sum(np.diff(s) > tol))


# ---------------------------------------------------------------- contagion on networks

def ring_lattice(n: int, k: int = 2) -> list:
    """A ring of n people, each tied to the k nearest on each side (degree 2k): highly clustered."""
    return [sorted({(i + d) % n for d in range(-k, k + 1) if d}) for i in range(n)]


def rewire(adj, q: float, seed: int = 0) -> list:
    """Degree-preserving rewiring by double-edge swaps: a fraction q of the edges are swapped with random others,
    which keeps everyone's number of ties but destroys the clustering (q = 1 is close to a random network)."""
    rng = np.random.default_rng(seed)
    nb = [set(a) for a in adj]
    edges = sorted({(min(i, j), max(i, j)) for i, a in enumerate(nb) for j in a})
    swaps = int(round(q * len(edges)))
    done, tries = 0, 0
    while done < swaps and tries < 100 * max(swaps, 1):
        tries += 1
        e1, e2 = rng.choice(len(edges), 2, replace=False)
        a, b = edges[e1]
        c, d = edges[e2]
        if rng.random() < 0.5:
            c, d = d, c
        if len({a, b, c, d}) < 4 or d in nb[a] or b in nb[c]:
            continue
        nb[a].discard(b); nb[b].discard(a); nb[c].discard(d); nb[d].discard(c)
        nb[a].add(d); nb[d].add(a); nb[c].add(b); nb[b].add(c)
        edges[e1] = (min(a, d), max(a, d))
        edges[e2] = (min(c, b), max(c, b))
        done += 1
    return [sorted(s) for s in nb]


def contagion(adj, seeds, need: int = 1, steps: int = 200) -> np.ndarray:
    """Deterministic threshold contagion: a person adopts once at least ``need`` of their ties have adopted
    (need = 1: simple contagion, like news or a disease; need = 2: complex, like a costly behaviour that needs
    reinforcement).  Returns the number adopted after each step until nothing changes."""
    n = len(adj)
    on = np.zeros(n, bool)
    on[list(seeds)] = True
    path = [int(on.sum())]
    for _ in range(steps):
        cnt = np.array([on[a].sum() for a in adj])
        new = on | (cnt >= need)
        if new.sum() == on.sum():
            break
        on = new
        path.append(int(on.sum()))
    return np.array(path)


# ---------------------------------------------------------------- crowds

def crowd(estimates, truth: float) -> dict:
    """The diversity prediction identity: (mean - truth)^2 = mean((x - truth)^2) - mean((x - mean)^2)."""
    x = np.asarray(estimates, float)
    m = x.mean()
    return {"mean": float(m), "median": float(np.median(x)), "collective": float((m - truth) ** 2),
            "individual": float(np.mean((x - truth) ** 2)), "diversity": float(np.mean((x - m) ** 2)),
            "beaten_by_mean": float(np.mean(np.abs(x - truth) > abs(m - truth)))}


def influence_rounds(n: int = 144, truth: float = 1.0, bias: float = 0.3, sd: float = 0.8, w: float = 0.4,
                     rounds: int = 5, seed: int = 0, stubborn=None) -> dict:
    """A crowd guessing a quantity on a log scale, then revising after seeing the others' mean: each round
    x <- (1 - w_i) x + w_i mean(x).  ``stubborn`` gives each person their own w_i (people far from the mean often
    move least).  Returns, per round, the collective error, the average individual error, the diversity and whether
    the truth is still inside the middle half and inside the whole range of the estimates."""
    rng = np.random.default_rng(seed)
    x = rng.normal(np.log(truth) + bias, sd, n)
    wi = np.full(n, w) if stubborn is None else np.asarray(stubborn, float)
    t = np.log(truth)
    rows = []
    for r in range(rounds + 1):
        c = crowd(x, t)
        lo, hi = np.quantile(x, [0.25, 0.75])
        rows.append((r, c["collective"], c["individual"], c["diversity"], bool(lo <= t <= hi),
                     bool(x.min() <= t <= x.max())))
        x = (1 - wi) * x + wi * x.mean()
    a = np.array([r[:4] for r in rows], float)
    return {"round": a[:, 0].astype(int), "collective": a[:, 1], "individual": a[:, 2], "diversity": a[:, 3],
            "truth_in_middle": np.array([r[4] for r in rows]), "truth_in_range": np.array([r[5] for r in rows])}


def gini(shares) -> float:
    """The Gini coefficient of non-negative shares: 0 for equality, close to 1 when one takes all."""
    s = np.sort(np.asarray(shares, float))
    n = len(s)
    if s.sum() == 0:
        return 0.0
    return float((2 * np.sum(np.arange(1, n + 1) * s) / (n * s.sum())) - (n + 1) / n)


def music_market(songs: int = 48, listeners: int = 2700, worlds: int = 8, social: float = 0.8, seed: int = 0,
                 quality=None) -> dict:
    """A cumulative-advantage market.  Each listener picks one song to hear, with chance proportional to
    (1 - social) * appeal + social * (its share of downloads so far, plus a little), and downloads it with chance
    equal to its quality.  ``social = 0`` is the independent world.  Returns the market shares in each world, the
    Gini coefficient of each, and Salganik's unpredictability: for each song, the mean absolute difference in market
    share between pairs of worlds, averaged over songs."""
    rng = np.random.default_rng(seed)
    q = rng.beta(2, 5, songs) if quality is None else np.asarray(quality, float)
    appeal = q / q.sum()
    shares = np.zeros((worlds, songs))
    for w in range(worlds):
        d = np.zeros(songs)
        for _ in range(listeners):
            p = (1 - social) * appeal + social * (d + 1) / (d.sum() + songs)
            i = rng.choice(songs, p=p / p.sum())
            if rng.random() < q[i]:
                d[i] += 1
        shares[w] = d / max(d.sum(), 1)
    pairs = [(a, b) for a in range(worlds) for b in range(a + 1, worlds)]
    unpred = float(np.mean([np.abs(shares[a] - shares[b]).mean() for a, b in pairs])) if pairs else 0.0
    return {"quality": q, "shares": shares, "gini": np.array([gini(s) for s in shares]), "unpredictability": unpred}


# ---------------------------------------------------------------- bystanders, impact, audiences, groups

def bystanders(N, p1: float = 0.85, beta: float = 1.0) -> dict:
    """Each of N bystanders helps with chance p_N = p1 N^-beta (diffusion of responsibility when beta > 0).  Returns
    each one's chance and the chance at least one helps, 1 - (1 - p_N)^N."""
    N = np.asarray(N, float)
    p = np.clip(p1 * N ** (-beta), 0, 1)
    return {"N": N, "each": p, "any": 1 - (1 - p) ** N}


def social_impact(N, s: float = 1.0, t: float = 0.5):
    """Latané's psychosocial law: the impact of N sources is s N^t; with t < 1 each added source adds less."""
    return s * np.asarray(N, float) ** t


def drive(h_correct: float, h_wrong: float, D) -> np.ndarray:
    """Hull and Spence's drive theory as Zajonc used it: excitatory potential = drive x habit strength, and the
    chance of the correct response is the softmax of the two potentials.  Raising D (an audience) pushes the
    dominant response up, whichever it is."""
    D = np.asarray(D, float)
    return 1 / (1 + np.exp(-D * (h_correct - h_wrong)))


def mentions(p: float, k) -> np.ndarray:
    """Stasser and Titus's information-sampling model: an item known to k members, each of whom mentions it with
    chance p, comes up with chance 1 - (1 - p)^k."""
    return 1 - (1 - p) ** np.asarray(k, float)


# ---------------------------------------------------------------- Part 35: reading minds

MOVES = {"N": (-1, 0), "S": (1, 0), "W": (0, -1), "E": (0, 1)}


def grid_distances(shape, walls, goal) -> np.ndarray:
    """Shortest path lengths to ``goal`` on a grid (4-neighbour moves), by breadth-first search; walls and cells
    that cannot reach the goal are inf."""
    from collections import deque
    H, Wd = shape
    wall = np.zeros(shape, bool)
    for c in walls:
        wall[c] = True
    D = np.full(shape, np.inf)
    D[goal] = 0
    q = deque([goal])
    while q:
        r, c = q.popleft()
        for dr, dc in MOVES.values():
            rr, cc = r + dr, c + dc
            if 0 <= rr < H and 0 <= cc < Wd and not wall[rr, cc] and D[rr, cc] == np.inf:
                D[rr, cc] = D[r, c] + 1
                q.append((rr, cc))
    return D


def action_probs(D, cell, beta: float = 1.0) -> dict:
    """A noisily rational agent heading for a goal (distance map D): it picks each legal move with probability
    proportional to exp(-beta * (1 + distance after the move)), Part 17's softmax over the planner's values."""
    H, Wd = D.shape
    vals = {}
    for a, (dr, dc) in MOVES.items():
        r, c = cell[0] + dr, cell[1] + dc
        if 0 <= r < H and 0 <= c < Wd and np.isfinite(D[r, c]):
            vals[a] = -beta * (1 + D[r, c])
    m = max(vals.values())
    z = {a: np.exp(v - m) for a, v in vals.items()}
    s = sum(z.values())
    return {a: v / s for a, v in z.items()}


def goal_posterior(path, shape, walls, goals, beta: float = 1.0, prior=None) -> np.ndarray:
    """Inverse planning (Baker, Saxe and Tenenbaum): the posterior over which goal an agent is heading for, after
    each step of its path, by Bayes' rule with the planner above as the likelihood.  ``path`` is a list of cells;
    returns a (len(path)) x (number of goals) array, row 0 being the prior."""
    Ds = [grid_distances(shape, walls, g) for g in goals]
    p = np.full(len(goals), 1 / len(goals)) if prior is None else np.asarray(prior, float) / np.sum(prior)
    out = [p.copy()]
    for a_, b_ in zip(path[:-1], path[1:]):
        move = next(k for k, (dr, dc) in MOVES.items() if (a_[0] + dr, a_[1] + dc) == tuple(b_))
        like = np.array([action_probs(D, a_, beta).get(move, 0.0) for D in Ds])
        p = p * like
        p = p / p.sum()
        out.append(p.copy())
    return np.array(out)


def kelley(table) -> dict:
    """Kelley's covariation cube as an analysis of variance: ``table`` is persons x entities x occasions (1 if the
    behaviour happened).  Returns the share of the variance carried by each main effect and the rest, and the three
    cues: consensus (do others do it too?), distinctiveness (only for this entity?) and consistency (every time?)
    for person 0 and entity 0."""
    X = np.asarray(table, float)
    m = X.mean()
    p = X.mean(axis=(1, 2)) - m
    e = X.mean(axis=(0, 2)) - m
    o = X.mean(axis=(0, 1)) - m
    total = np.sum((X - m) ** 2)
    ss = {"person": X.shape[1] * X.shape[2] * np.sum(p ** 2), "entity": X.shape[0] * X.shape[2] * np.sum(e ** 2),
          "occasion": X.shape[0] * X.shape[1] * np.sum(o ** 2)}
    ss["rest"] = total - sum(ss.values())
    shares = {k: (v / total if total > 0 else 0.0) for k, v in ss.items()}
    return {"shares": shares, "consensus": float(X[1:, 0, :].mean()), "distinctiveness": float(1 - X[0, 1:, :].mean()),
            "consistency": float(X[0, 0, :].mean())}


def dunning_kruger(n: int = 4000, rho: float = 0.3, shift: float = 15.0, seed: int = 0) -> dict:
    """The Dunning-Kruger plot from noise: actual and self-assessed skill correlate rho, everyone rates themselves
    ``shift`` percentile points better than they are (better-than-average), and people are grouped by quartile of
    actual score.  Returns each quartile's mean actual and mean perceived percentile."""
    from scipy.stats import norm, rankdata
    rng = np.random.default_rng(seed)
    a = rng.normal(size=n)
    s = rho * a + np.sqrt(1 - rho ** 2) * rng.normal(size=n)
    pa = 100 * (rankdata(a) - 0.5) / n
    ps = np.clip(100 * norm.cdf(s) + shift, 0, 100)
    q = np.minimum((pa // 25).astype(int), 3)
    return {"actual": np.array([pa[q == k].mean() for k in range(4)]),
            "perceived": np.array([ps[q == k].mean() for k in range(4)]), "rho": rho, "shift": shift}
