"""Psyche learns to act: reward and prediction (Part 17 of *Psychology, Built*).

Temporal-difference learning on Pavlov's task with a complete serial compound (a tapped delay line), whose error
moves from the reward to the cue and dips when a reward is omitted, as Schultz's dopamine neurons do; second-order
conditioning; Q-learning on a two-armed bandit with a softmax chooser, and its maximum-likelihood fit with parameter
recovery; four exploration policies and their regret; a maze in which a model-based learner shows Tolman's latent
learning and a model-free one does not; Daw's two-step task with model-free, model-based and hybrid agents and their
stay probabilities; the successor representation and revaluation; a distributional code of reward made of learners
with asymmetric rates; and Redish's model of a drug whose dopamine cannot be predicted away.

The equations are in the docstrings; parameters are chosen to make the designs legible, not fitted to a brain.
"""

from __future__ import annotations

import numpy as np
from scipy.optimize import minimize


# ============================================================================================== TD on Pavlov's task
def td_conditioning(trials=120, n_steps=30, cue=5, reward=20, alpha=0.2, gamma=0.98, omit=(), reward_size=1.0,
                    second_order=None):
    """TD(0) with a complete serial compound: after the cue, a different unit is active at each time step, so the
    value of each moment after the cue is learned separately.  V(t) = w[t − cue] for t ≥ cue, 0 before (the cue's
    onset is unpredictable, so the moment before it has no value).  The error at each step is

        δ_t = r_t + γ V(t+1) − V(t),

    and w[t − cue] += α δ_t.  ``omit`` lists trials with no reward.  Returns δ (trials × steps) and V."""
    w = np.zeros(n_steps)
    D = np.zeros((trials, n_steps))
    Vs = np.zeros((trials, n_steps + 1))
    for k in range(trials):
        V = np.zeros(n_steps + 1)
        V[cue:n_steps] = w[: n_steps - cue]
        for t in range(n_steps):
            r = reward_size if (t == reward and k not in omit) else 0.0
            d = r + gamma * V[t + 1] - V[t]
            D[k, t] = d
            if t >= cue:
                w[t - cue] += alpha * d
                V[cue:n_steps] = w[: n_steps - cue]
        Vs[k] = V
    return D, Vs


def second_order(n_first=200, n_second=60, gamma=0.98, alpha=0.2, gap=6):
    """Second-order conditioning: first cue B is followed by reward; then cue A is followed by B and no reward.  A
    acquires value, because B's onset is now predicted by A and B's value is a reward to A, through γV(t+1) − V(t).
    Rescorla-Wagner, with no time, cannot do this without an extra assumption.  Returns A's value over the second
    phase."""
    wB = np.zeros(gap + 1)
    for _ in range(n_first):  # B, then reward ``gap`` steps later
        for t in range(gap + 1):
            r = 1.0 if t == gap else 0.0
            nxt = wB[t + 1] if t + 1 <= gap else 0.0
            d = r + gamma * nxt - wB[t]
            wB[t] += alpha * d
    wA = np.zeros(gap)
    trace = []
    for _ in range(n_second):  # A for ``gap`` steps, then B, then nothing
        for t in range(gap):
            nxt = wA[t + 1] if t + 1 < gap else wB[0]
            d = gamma * nxt - wA[t]
            wA[t] += alpha * d
        trace.append(wA[0])
    return np.array(trace)


# ============================================================================================== bandits
def softmax(q, beta):
    z = beta * (q - np.max(q))
    p = np.exp(z)
    return p / p.sum()


def q_learning_bandit(p_reward, trials=200, alpha=0.3, beta=4.0, rng=None, q0=0.5):
    """A two-armed bandit (Bernoulli arms with ``p_reward``, a list, or an array of shape (trials, arms) for arms
    that change) played by Q-learning with a softmax: P(a) ∝ exp(β Q_a), Q_a ← Q_a + α (r − Q_a).  Returns choices,
    rewards and the Q values before each trial."""
    rng = rng or np.random.default_rng(0)
    P = np.asarray(p_reward, float)
    if P.ndim == 1:
        P = np.tile(P, (trials, 1))
    k = P.shape[1]
    q = np.full(k, q0)
    C = np.zeros(trials, int)
    R = np.zeros(trials)
    Q = np.zeros((trials, k))
    for t in range(trials):
        Q[t] = q
        a = rng.choice(k, p=softmax(q, beta))
        r = float(rng.random() < P[t, a])
        q[a] += alpha * (r - q[a])
        C[t], R[t] = a, r
    return C, R, Q


def bandit_loglik(params, choices, rewards, k=2, q0=0.5):
    """The log-likelihood of a choice sequence under Q-learning with softmax, for (α, β)."""
    alpha, beta = params
    q = np.full(k, q0)
    ll = 0.0
    for a, r in zip(choices, rewards):
        p = softmax(q, beta)
        ll += np.log(max(p[a], 1e-12))
        q[a] += alpha * (r - q[a])
    return ll


def fit_bandit(choices, rewards, k=2):
    """Maximum-likelihood (α, β), from several starting points, bounded to α in (0.01, 1), β in (0.1, 30)."""
    best = None
    for a0 in (0.1, 0.4, 0.8):
        for b0 in (1.0, 5.0, 12.0):
            res = minimize(lambda p: -bandit_loglik(p, choices, rewards, k), x0=[a0, b0], method="L-BFGS-B",
                           bounds=[(0.01, 1.0), (0.1, 30.0)])
            if best is None or res.fun < best.fun:
                best = res
    return float(best.x[0]), float(best.x[1]), float(-best.fun)


def win_stay_lose_shift(choices, rewards):
    """P(repeat | reward) and P(switch | no reward)."""
    c, r = np.asarray(choices), np.asarray(rewards)
    stay = c[1:] == c[:-1]
    win = r[:-1] > 0
    return float(stay[win].mean()) if win.any() else np.nan, float((~stay[~win]).mean()) if (~win).any() else np.nan


def explore_regret(policy, p_reward=(0.4, 0.5, 0.6, 0.45), trials=1000, rng=None, eps=0.1, beta=8.0, alpha=None):
    """Cumulative regret (best mean minus the chosen arm's mean) of one policy on a Bernoulli bandit:
    ``greedy``, ``epsilon`` (random with probability eps), ``softmax`` (on sample means), ``ucb`` (UCB1: mean +
    √(2 ln t / n)) or ``thompson`` (sample each arm's Beta posterior and take the best)."""
    rng = rng or np.random.default_rng(0)
    p = np.asarray(p_reward, float)
    k = p.size
    n = np.zeros(k)
    s = np.zeros(k)
    regret = np.zeros(trials)
    best = p.max()
    total = 0.0
    for t in range(trials):
        mean = np.where(n > 0, s / np.maximum(n, 1), 0.5)
        if policy == "greedy":
            a = int(np.argmax(mean + 1e-9 * rng.random(k)))
        elif policy == "epsilon":
            a = int(rng.integers(k)) if rng.random() < eps else int(np.argmax(mean + 1e-9 * rng.random(k)))
        elif policy == "softmax":
            a = int(rng.choice(k, p=softmax(mean, beta)))
        elif policy == "ucb":
            a = int(np.argmin(n)) if (n == 0).any() else int(np.argmax(mean + np.sqrt(2 * np.log(t + 1) / n)))
        elif policy == "thompson":
            a = int(np.argmax(rng.beta(1 + s, 1 + n - s)))
        else:
            raise ValueError(policy)
        r = float(rng.random() < p[a])
        n[a] += 1
        s[a] += r
        total += best - p[a]
        regret[t] = total
    return regret


# ============================================================================================== maps and latent learning
MAZE = [
    "#########",
    "#S..#...#",
    "#.#.#.#.#",
    "#.#...#.#",
    "#.#####.#",
    "#...#..G#",
    "#########",
]


def maze_graph(maze=MAZE):
    """Open cells, the start, the goal, and each cell's neighbours."""
    cells = [(r, c) for r, row in enumerate(maze) for c, ch in enumerate(row) if ch != "#"]
    idx = {cell: k for k, cell in enumerate(cells)}
    start = next(idx[(r, c)] for r, row in enumerate(maze) for c, ch in enumerate(row) if ch == "S")
    goal = next(idx[(r, c)] for r, row in enumerate(maze) for c, ch in enumerate(row) if ch == "G")
    nbrs = []
    for (r, c) in cells:
        nbrs.append([idx[(r + dr, c + dc)] for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)) if (r + dr, c + dc) in idx])
    return cells, start, goal, nbrs


def shortest_steps(start, goal, nbrs):
    from collections import deque
    dist = {start: 0}
    q = deque([start])
    while q:
        u = q.popleft()
        for v in nbrs[u]:
            if v not in dist:
                dist[v] = dist[u] + 1
                q.append(v)
    return dist[goal]


def latent_learning(days=20, reward_from=10, agent="model", rng=None, alpha=0.3, gamma=0.9, beta=6.0,
                    max_steps=200, beta_plan=40.0):
    """Tolman and Honzik's design on Psyche: one run a day through a maze; food in the goal box only from day
    ``reward_from`` on.  A ``model`` agent learns the maze's map on every run, rewarded or not, and when food
    appears plans to it by value iteration; a ``free`` agent learns cached values by Q-learning from reward alone.
    The planner chooses by a softmax with ``beta_plan`` on planned values.  Returns the steps taken each day and the
    shortest path, the floor."""
    rng = rng or np.random.default_rng(0)
    cells, start, goal, nbrs = maze_graph()
    n = len(cells)
    known = [set() for _ in range(n)]
    Q = {(s, a): 0.0 for s in range(n) for a in nbrs[s]}
    goal_valued = False
    out = []
    for day in range(days):
        rewarded = day >= reward_from
        s, steps = start, 0
        V = None
        if agent == "model" and goal_valued:
            V = np.zeros(n)
            for _ in range(60):
                for u in range(n):
                    if u == goal:
                        continue
                    if known[u]:
                        V[u] = max((1.0 if v == goal else 0.0) + gamma * V[v] for v in known[u])
        while s != goal and steps < max_steps:
            acts = nbrs[s]
            if agent == "model" and V is not None and known[s]:
                vals = beta_plan / beta * np.array([(1.0 if v == goal else 0.0) + gamma * V[v] if v in known[s] else 0.0
                                                    for v in acts])
            else:
                vals = np.array([Q[(s, v)] for v in acts])
            a = acts[rng.choice(len(acts), p=softmax(vals, beta))]
            known[s].add(a)
            known[a].add(s)
            r = 1.0 if (a == goal and rewarded) else 0.0
            nxt = 0.0 if a == goal else max(Q[(a, v)] for v in nbrs[a])
            Q[(s, a)] += alpha * (r + gamma * nxt - Q[(s, a)])
            s, steps = a, steps + 1
        if rewarded:
            goal_valued = True
        out.append(steps)
    return np.array(out), shortest_steps(start, goal, nbrs)


# ============================================================================================== the two-step task
def two_step(agent_w=0.5, trials=400, rng=None, alpha=0.5, beta=5.0, p_common=0.7, drift=0.025, lam=1.0):
    """Daw et al.'s (2011) two-step task.  Stage 1: choose A or B; A leads to state 1 (and B to state 2) with
    probability 0.7, the other state with 0.3.  Stage 2: choose one of two options in that state; each pays with a
    probability that drifts as a bounded random walk.  A model-free learner credits the first choice with what
    followed (SARSA with eligibility λ); a model-based learner values each first choice through the known
    transitions; the hybrid weights them, w = ``agent_w`` (1 is purely model-based).  Returns a record of first
    choices, transitions (common or rare) and rewards."""
    rng = rng or np.random.default_rng(0)
    p = rng.uniform(0.25, 0.75, size=(2, 2))
    q1 = np.zeros(2)
    q2 = np.zeros((2, 2))
    rec = []
    for _ in range(trials):
        q_mb = np.array([p_common * q2[0].max() + (1 - p_common) * q2[1].max(),
                         p_common * q2[1].max() + (1 - p_common) * q2[0].max()])
        q = agent_w * q_mb + (1 - agent_w) * q1
        a1 = int(rng.choice(2, p=softmax(q, beta)))
        common = rng.random() < p_common
        s2 = a1 if common else 1 - a1
        a2 = int(rng.choice(2, p=softmax(q2[s2], beta)))
        r = float(rng.random() < p[s2, a2])
        d1 = q2[s2, a2] - q1[a1]
        q1[a1] += alpha * d1
        d2 = r - q2[s2, a2]
        q2[s2, a2] += alpha * d2
        q1[a1] += alpha * lam * d2
        p = np.clip(p + rng.normal(0, drift, size=p.shape), 0.25, 0.75)
        rec.append((a1, common, r))
    return np.array(rec, float)


def stay_probabilities(rec):
    """P(repeat the first choice) after: rewarded-common, rewarded-rare, unrewarded-common, unrewarded-rare."""
    a, common, r = rec[:, 0], rec[:, 1].astype(bool), rec[:, 2] > 0
    stay = a[1:] == a[:-1]
    out = {}
    for name, m in (("rewarded, common", r[:-1] & common[:-1]), ("rewarded, rare", r[:-1] & ~common[:-1]),
                    ("unrewarded, common", ~r[:-1] & common[:-1]), ("unrewarded, rare", ~r[:-1] & ~common[:-1])):
        out[name] = float(stay[m].mean())
    return out


# ============================================================================================== successor representation
def successor_matrix(T, gamma=0.9):
    """The successor representation of a Markov chain with transition matrix T: M = (I − γT)⁻¹, the expected
    discounted future occupancy of every state from every state.  Values are then V = M r for any reward vector."""
    T = np.asarray(T, float)
    return np.linalg.inv(np.eye(T.shape[0]) - gamma * T)


def revaluation(kind="reward", gamma=0.9):
    """Momennejad et al.'s (2017) design on two paths, 1→3→5 and 2→4→6, with 5 paying 10 and 6 paying 1.  Then a
    change is learned only from the later states: in ``reward`` revaluation 5 now pays 1 and 6 pays 10; in
    ``transition`` revaluation 3 now leads to 6 and 4 to 5.  States 1 and 2 are never revisited.

    * model-free: V(1), V(2) were cached; nothing updates them.
    * successor representation: V = M r; M's rows for 1 and 2 were learned from experience and are not revisited,
      so a new r revalues them at once, but a new transition does not.
    * model-based: plans through the current transitions and rewards, so both changes revalue it.

    Returns {learner: (V(1), V(2))} after the change (states are numbered from 1)."""
    n = 6
    T_old = np.zeros((n, n))
    T_old[0, 2] = T_old[2, 4] = T_old[1, 3] = T_old[3, 5] = 1.0
    r_old = np.array([0, 0, 0, 0, 10.0, 1.0])
    M_old = successor_matrix(T_old, gamma)
    if kind == "reward":
        T_new, r_new = T_old, np.array([0, 0, 0, 0, 1.0, 10.0])
    else:
        T_new = T_old.copy()
        T_new[2, 4] = T_new[3, 5] = 0.0
        T_new[2, 5] = T_new[3, 4] = 1.0
        r_new = r_old
    M_new = successor_matrix(T_new, gamma)
    M_sr = M_old.copy()
    M_sr[2:] = M_new[2:]  # the revisited states relearn their rows; 1 and 2 keep theirs
    v_mf = M_old @ r_old
    return {"model_free": tuple(v_mf[:2]), "successor": tuple((M_sr @ r_new)[:2]),
            "model_based": tuple((M_new @ r_new)[:2])}


# ============================================================================================== distributional code
def distributional_td(rewards, taus, lr=0.02, epochs=40, rng=None):
    """A population of value learners with asymmetric rates: unit i moves up by α τ_i on positive errors and down by
    α (1 − τ_i) on negative ones, so it settles at the τ_i-expectile of the reward distribution.  Optimistic units
    (τ near 1) sit high, pessimistic ones low: together they encode the distribution, not only its mean (Dabney
    et al. 2020).  Returns the learned values."""
    rng = rng or np.random.default_rng(0)
    r = np.asarray(rewards, float)
    v = np.full(len(taus), r.mean())
    taus = np.asarray(taus, float)
    for _ in range(epochs):
        for x in rng.permutation(r):
            d = x - v
            v += lr * np.where(d > 0, taus, 1 - taus) * d
    return v


def expectile(x, tau, iters=200):
    """The τ-expectile of a sample: the m with τ Σ(x − m)⁺ = (1 − τ) Σ(m − x)⁺."""
    x = np.asarray(x, float)
    m = x.mean()
    for _ in range(iters):
        w = np.where(x > m, tau, 1 - tau)
        m = float((w * x).sum() / w.sum())
    return m


# ============================================================================================== addiction
def redish(trials=300, drug=0.0, natural=1.0, alpha=0.1, gamma=0.9):
    """Redish (2004): a cue followed by a reward.  For a natural reward, δ = r + γV' − V shrinks to zero as V
    learns to predict it.  A drug adds a direct dopamine surge D that learning cannot cancel:
    δ = max(r + γV' − V + D, D), so δ never falls below D and the cue's value grows without bound.  Returns the
    cue's value over trials."""
    v = 0.0
    out = []
    for _ in range(trials):
        d = natural + gamma * 0.0 - v
        if drug > 0:
            d = max(d + drug, drug)
        v += alpha * d
        out.append(v)
    return np.array(out)
