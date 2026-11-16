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

Part 36 adds groups:

* :func:`tajfel_matrix` and :func:`allocate`: Tajfel's allocation matrices, each column a pair of points for an
  anonymous member of one's own group and of the other.  A chooser weighing joint profit, ingroup profit and the
  difference between the groups picks a column; maximum joint profit, maximum ingroup profit and maximum difference
  pull in different directions, which is how the minimal-group studies told favouritism from greed.
* :func:`iat_d` and :func:`iat_study`: an Implicit Association Test as two blocks of decisions by a diffusion
  process whose drift is helped or hindered by an association.  The D score is the difference in mean times over
  their pooled spread.  When the association a person brings has a stable part and a part that varies with the
  occasion, the score's test-retest reliability falls, and so does any correlation with behaviour, while the
  group's average stays clear.
* :func:`list_experiment`: the item-count technique: a control group counts how many of J innocuous statements are
  true for them, a treatment group gets the sensitive one too, and the difference in means estimates its
  prevalence without anyone revealing their answer.
* :func:`pipeline`: a promotion ladder where at every level a fixed fraction is promoted on a score, and one group
  gets a small advantage; the other group's share at each level, computed exactly from normal tails.
* :func:`illusory_correlation`: Hamilton and Gifford's design, with distinctive (rare group, rare behaviour) events
  encoded more strongly; the judged rate of undesirable acts in each group.

Part 37 adds bonds and bargains:

* :func:`fs_utility`, :func:`fs_threshold` and :func:`ultimatum`: Fehr and Schmidt's inequity aversion.  A responder
  who dislikes earning less (weight alpha) rejects any share below alpha / (1 + 2 alpha); a proposer facing a
  population of such responders offers what maximizes expected payoff, which is far above the "rational" minimum.
* :func:`public_goods`: rounds of a linear public-goods game with conditional cooperators (who match a fraction of
  what the others gave last round) and free riders; contributions decay.  With costly punishment of those below the
  group's average, free riders raise their contributions and cooperation holds.
* :func:`ipd_tournament`: a round-robin of iterated prisoner's dilemmas among simple strategies, in the spirit of
  Axelrod's tournaments, with or without noise in executing moves.
* :func:`overfit_divorce`: a classifier fitted to a small sample of couples with many measured variables, scored on
  the couples it was fitted to and by leave-one-out cross-validation: in-sample accuracy is high even when the
  variables carry little real signal.

Everything here is a simulated model and is labelled simulated; it does not stand in for any study's data.  Nothing
here imports manim.
"""

from __future__ import annotations

import numpy as np

__all__ = ["cascade", "cascade_size", "cascade_curve", "degroot", "influence_weights", "bounded_confidence",
           "clusters", "ring_lattice", "rewire", "contagion", "crowd", "influence_rounds", "gini", "music_market",
           "bystanders", "social_impact", "drive", "mentions", "grid_distances", "action_probs", "goal_posterior",
           "kelley", "dunning_kruger", "tajfel_matrix", "allocate", "iat_d", "iat_study",
           "list_experiment", "pipeline", "illusory_correlation", "fs_utility", "fs_threshold",
           "ultimatum", "public_goods", "overfit_divorce", "ipd_tournament"]


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


# ---------------------------------------------------------------- groups (Part 36)

def tajfel_matrix(k: int = 13, in0: float = 7, in_step: float = 1, out0: float = 1, out_step: float = 2) -> np.ndarray:
    """One of Tajfel's matrices: a 2 x k array of points, row 0 for a member of the chooser's own group and row 1 for
    a member of the other.  The default runs 7..19 against 1..25: the left end maximizes the difference in the
    ingroup's favour, the right end maximizes both the ingroup's points and the joint total, and the column with 13
    and 13 is fair."""
    j = np.arange(k)
    return np.vstack([in0 + in_step * j, out0 + out_step * j]).astype(float)


def allocate(matrix, joint: float = 0.0, ingroup: float = 0.0, difference: float = 0.0, fairness: float = 0.0) -> int:
    """The column a chooser picks who values the joint total, the ingroup's points, the ingroup's lead over the
    outgroup and (negatively) any inequality, with the given weights.  Ties go to the leftmost column."""
    M = np.asarray(matrix, float)
    score = joint * (M[0] + M[1]) + ingroup * M[0] + difference * (M[0] - M[1]) - fairness * np.abs(M[0] - M[1])
    return int(np.argmax(score))


def iat_d(bias: float, trials: int = 60, rng=None, drift: float = 2.0, bound: float = 1.2,
          t0: float = 0.35) -> float:
    """The D score of one simulated IAT session.  Each trial's decision time is a diffusion process's first passage,
    an inverse Gaussian with mean bound/drift and shape bound**2, plus a non-decision time t0 (seconds).  The
    association ``bias`` speeds the compatible block (drift x (1 + bias)) and slows the incompatible one (drift x
    (1 - bias)).  D = (mean incompatible - mean compatible) / SD of all trials."""
    rng = np.random.default_rng(rng)
    b = float(np.clip(bias, -0.9, 0.9))
    vc, vi = drift * (1 + b), drift * (1 - b)
    c = t0 + rng.wald(bound / vc, bound ** 2, trials)
    i = t0 + rng.wald(bound / vi, bound ** 2, trials)
    return float((i.mean() - c.mean()) / np.concatenate([c, i]).std(ddof=1))


def iat_study(n: int = 400, mean: float = 0.15, trait_sd: float = 0.10, state_sd: float = 0.07, trials: int = 60,
              behaviour_r: float = 0.3, seed: int = 0) -> dict:
    """A sample of people, each with a stable association (normal, ``mean`` and ``trait_sd``) and an
    occasion-to-occasion part (``state_sd``) drawn afresh at each of two sessions.  A behaviour correlates
    ``behaviour_r`` with the stable part.  Returns both sessions' D scores, the test-retest correlation, the
    correlation of session-1 D with the behaviour, the ceiling implied by the reliability, and the group's mean D
    with its t statistic."""
    rng = np.random.default_rng(seed)
    trait = rng.normal(mean, trait_sd, n)
    d1 = np.array([iat_d(t + rng.normal(0, state_sd), trials, rng) for t in trait])
    d2 = np.array([iat_d(t + rng.normal(0, state_sd), trials, rng) for t in trait])
    z = (trait - trait.mean()) / trait.std()
    behaviour = behaviour_r * z + np.sqrt(1 - behaviour_r ** 2) * rng.normal(size=n)
    retest = float(np.corrcoef(d1, d2)[0, 1])
    return {"d1": d1, "d2": d2, "behaviour": behaviour, "retest": retest,
            "r_behaviour": float(np.corrcoef(d1, behaviour)[0, 1]),
            "ceiling": float(behaviour_r * np.sqrt(max(retest, 0.0))),
            "mean_d": float(d1.mean()), "t": float(d1.mean() / (d1.std(ddof=1) / np.sqrt(n)))}


def list_experiment(n: int = 1000, prevalence: float = 0.2, control_p=(0.5, 0.3, 0.6), seed: int = 0) -> dict:
    """The item-count technique: half the sample counts how many of the control statements apply to them, the other
    half counts the control statements plus a sensitive one held with probability ``prevalence``.  Returns the
    difference-in-means estimate of the prevalence and its standard error."""
    rng = np.random.default_rng(seed)
    m = n // 2
    p = np.asarray(control_p, float)
    ctrl = (rng.random((m, len(p))) < p).sum(axis=1)
    trt = (rng.random((n - m, len(p))) < p).sum(axis=1) + (rng.random(n - m) < prevalence)
    est = trt.mean() - ctrl.mean()
    se = np.sqrt(trt.var(ddof=1) / len(trt) + ctrl.var(ddof=1) / len(ctrl))
    return {"estimate": float(est), "se": float(se), "control": ctrl, "treatment": trt}


def pipeline(levels: int = 8, keep: float = 0.5, advantage: float = 0.1, start: float = 0.5) -> np.ndarray:
    """A promotion ladder.  At each level everyone is scored afresh (normal, SD 1); one group's scores are shifted
    up by ``advantage``; the top ``keep`` fraction moves up.  Returns the other group's share at each level, from the
    entry level, computed exactly: the threshold c solves (1 - s) Q(c - advantage) + s Q(c) = keep, and the new
    share is s Q(c) / keep, where Q is the normal upper tail."""
    from scipy.optimize import brentq
    from scipy.stats import norm
    s = float(start)
    out = [s]
    for _ in range(levels - 1):
        c = brentq(lambda x: (1 - s) * norm.sf(x - advantage) + s * norm.sf(x) - keep, -10, 10)
        s = s * norm.sf(c) / keep
        out.append(s)
    return np.array(out)


def illusory_correlation(counts=((18, 8), (9, 4)), boost: float = 0.6) -> dict:
    """Hamilton and Gifford's design: group A with ``counts[0]`` (desirable, undesirable) acts and group B with
    ``counts[1]``, in the same ratio.  If the rarest pairing (the smaller group's undesirable acts) is encoded
    ``1 + boost`` times as strongly, the remembered share of undesirable acts in each group."""
    (a_pos, a_neg), (b_pos, b_neg) = counts
    b_neg_w = b_neg * (1 + boost)
    return {"actual": (a_neg / (a_pos + a_neg), b_neg / (b_pos + b_neg)),
            "judged": (a_neg / (a_pos + a_neg), b_neg_w / (b_pos + b_neg_w))}


# ---------------------------------------------------------------- bonds and bargains (Part 37)

def fs_utility(mine: float, theirs: float, alpha: float, beta: float) -> float:
    """Fehr and Schmidt's two-player utility: one's own payoff, minus alpha times any shortfall against the other,
    minus beta times any lead."""
    return mine - alpha * max(theirs - mine, 0.0) - beta * max(mine - theirs, 0.0)


def fs_threshold(alpha) -> np.ndarray:
    """The smallest share of a pie of 1 an inequity-averse responder accepts: s - alpha (1 - 2 s) >= 0, so
    s >= alpha / (1 + 2 alpha); a responder with alpha = 0 accepts anything."""
    a = np.asarray(alpha, float)
    return a / (1 + 2 * a)


def ultimatum(alphas, offers=None) -> dict:
    """A proposer who keeps 1 - s and faces responders with the given alphas: the acceptance rate of each offer s,
    the proposer's expected payoff (1 - s) P(accept), and the offer that maximizes it."""
    t = fs_threshold(alphas)
    s = np.linspace(0, 0.5, 51) if offers is None else np.asarray(offers, float)
    accept = np.array([(t <= x + 1e-12).mean() for x in s])
    payoff = (1 - s) * accept
    return {"offers": s, "accept": accept, "payoff": payoff, "best": float(s[int(np.argmax(payoff))])}


def public_goods(n_groups: int = 200, size: int = 4, rounds: int = 10, punishment: bool = False,
                 free_riders: float = 0.25, slope: float = 0.9, start: float = 0.6, deterrence: float = 0.35,
                 seed: int = 0) -> np.ndarray:
    """Average contribution (as a share of the endowment) in each round of a linear public-goods game.  Conditional
    cooperators give ``slope`` times what the others gave on average last round, with noise; free riders give
    nothing.  With punishment, anyone below the group's average is punished and moves ``deterrence`` of the way
    toward it next round, and cooperators, protected from being exploited, keep their level."""
    rng = np.random.default_rng(seed)
    kind = rng.random((n_groups, size)) < free_riders
    c = np.where(kind, rng.uniform(0, 0.2, (n_groups, size)), np.clip(rng.normal(start, 0.15, (n_groups, size)), 0, 1))
    out = [c.mean()]
    for _ in range(rounds - 1):
        others = (c.sum(axis=1, keepdims=True) - c) / (size - 1)
        coop = np.clip(slope * others + rng.normal(0, 0.05, c.shape), 0, 1)
        free = np.zeros_like(c)
        if punishment:
            avg = c.mean(axis=1, keepdims=True)
            coop = np.clip(np.maximum(coop, c) + rng.normal(0, 0.03, c.shape), 0, 1)
            free = np.clip(c + deterrence * np.maximum(avg - c, 0) + 0.05, 0, 1)
        c = np.where(kind, free, coop)
        out.append(c.mean())
    return np.array(out)


def overfit_divorce(n: int = 56, p: int = 30, signal: float = 0.25, seed: int = 0) -> dict:
    """``n`` couples, ``p`` measured variables of which only the first carries ``signal`` (a standardized effect on
    a latent risk); about a third divorce.  A linear discriminant (least squares on the outcome) is fitted to all n
    and scored on them, and by leave-one-out.  Returns both accuracies and the base-rate accuracy."""
    rng = np.random.default_rng(seed)
    X = rng.normal(size=(n, p))
    risk = signal * X[:, 0] + rng.normal(size=n)
    y = (risk > np.quantile(risk, 2 / 3)).astype(float)
    Z = np.column_stack([np.ones(n), X])
    beta, *_ = np.linalg.lstsq(Z, y, rcond=None)
    cut = 1 - y.mean()
    def classify(fit):
        return (fit > np.quantile(fit, cut)).astype(float)
    insample = float((classify(Z @ beta) == y).mean())
    loo = np.empty(n)
    for i in range(n):
        m = np.arange(n) != i
        b, *_ = np.linalg.lstsq(Z[m], y[m], rcond=None)
        loo[i] = Z[i] @ b
    cv = float((classify(loo) == y).mean())
    return {"insample": insample, "loo": cv, "base": float(max(y.mean(), 1 - y.mean()))}


IPD_STRATEGIES = ("tit for tat", "always cooperate", "always defect", "grim trigger", "tit for two tats",
                  "win-stay lose-shift", "random")


def _ipd_move(name, mine, theirs, rng):
    if name == "always cooperate":
        return 1
    if name == "always defect":
        return 0
    if name == "random":
        return int(rng.random() < 0.5)
    if not theirs:
        return 1
    if name == "tit for tat":
        return theirs[-1]
    if name == "grim trigger":
        return int(all(theirs))
    if name == "tit for two tats":
        return int(not (len(theirs) >= 2 and theirs[-1] == 0 and theirs[-2] == 0))
    if name == "win-stay lose-shift":
        return mine[-1] if mine[-1] == theirs[-1] else 1 - mine[-1]
    raise ValueError(name)


def ipd_tournament(strategies=IPD_STRATEGIES, rounds: int = 200, noise: float = 0.0, seed: int = 0,
                   payoff=(3, 0, 5, 1)) -> dict:
    """Every strategy plays every other (and a copy of itself) for ``rounds`` moves of the prisoner's dilemma with
    payoffs (R, S, T, P) = (3, 0, 5, 1); with probability ``noise`` an intended move is flipped.  Returns each
    strategy's average score per move over all its matches, and the matrix of average scores per move."""
    R, Sx, T, P = payoff
    rng = np.random.default_rng(seed)
    k = len(strategies)
    M = np.zeros((k, k))
    for i in range(k):
        for j in range(i, k):
            a, b, pa, pb = [], [], 0.0, 0.0
            for _ in range(rounds):
                x = _ipd_move(strategies[i], a, b, rng)
                y = _ipd_move(strategies[j], b, a, rng)
                if noise and rng.random() < noise:
                    x = 1 - x
                if noise and rng.random() < noise:
                    y = 1 - y
                a.append(x)
                b.append(y)
                pa += (R if y else Sx) if x else (T if y else P)
                pb += (R if x else Sx) if y else (T if x else P)
            M[i, j], M[j, i] = pa / rounds, pb / rounds
    return {"strategies": list(strategies), "matrix": M, "score": M.mean(axis=1)}

