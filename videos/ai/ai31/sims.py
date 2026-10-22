"""The simulations of Part 31 (numpy only, seeded): arenas, judges, item response, AI control and the boat race.

Every quantity here is *simulated*, from settings written below, and the scenes say so on screen.  The point of
each is a mechanism (how ratings converge, how a biased judge distorts them, why a monitor's audit budget limits
safety, why an agent circles for points), not a claim about any real model.

* :func:`bt_fit`, :func:`bt_cov`, :func:`online_elo`: Bradley-Terry by maximum likelihood (Newton), its closed-form
  covariance, and the classic online Elo update;
* :func:`judge_battles`: pairwise verdicts from a judge with position, length and self-preference biases;
* :func:`irt_fit`: the two-parameter logistic item-response model, fitted by joint maximum likelihood;
* :func:`control_game`: the trusted-monitoring game of Greenblatt et al. (2023), in closed form;
* :class:`BoatRace`, :func:`q_learning`: a gridworld race with a gameable reward, and tabular Q-learning on it.
"""

from __future__ import annotations

import math

import numpy as np

ELO = 400 / math.log(10)  # Elo points per unit of Bradley-Terry strength (a 400-point gap = 10:1 odds)


def rng(seed: int) -> np.random.Generator:
    return np.random.Generator(np.random.PCG64(seed))


def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-x))


# ---------------------------------------------------------------------------
# Bradley-Terry and Elo
# ---------------------------------------------------------------------------
def wins_matrix(i, j, y, M, weights=None) -> np.ndarray:
    """W[a, b] = (weighted) number of battles a won against b; y = 1 if i won, 0 if j won, 0.5 for a tie."""
    w = np.ones(len(i)) if weights is None else weights
    W = np.bincount(i * M + j, w * y, M * M) + np.bincount(j * M + i, w * (1 - y), M * M)
    return W.reshape(M, M)


def bt_fit(W: np.ndarray, prior=1 / 9, iters=60) -> tuple[np.ndarray, np.ndarray]:
    """Bradley-Terry strengths (natural units, mean zero) maximizing sum_ab W_ab log sigmoid(t_a - t_b), with a weak
    Gaussian prior (variance 1/prior = 9, i.e. +-520 Elo) so that a model that has never lost stays finite.
    Returns the strengths and the observed information matrix."""
    M = len(W)
    N = W + W.T
    t = np.zeros(M)
    for _ in range(iters):
        p = sigmoid(t[:, None] - t[None, :])
        g = (W - N * p).sum(1) - prior * t
        h = N * p * (1 - p)
        info = np.diag(h.sum(1)) - h + prior * np.eye(M)
        step = np.linalg.solve(info, g)
        t = t + step
        t -= t.mean()
        if np.abs(step).max() < 1e-10:
            break
    p = sigmoid(t[:, None] - t[None, :])
    h = N * p * (1 - p)
    info = np.diag(h.sum(1)) - h + prior * np.eye(M)
    return t, info


def bt_cov(info: np.ndarray) -> np.ndarray:
    """Covariance of the centred strengths: P info^-1 P with P = I - 11^T / M (only differences are identified)."""
    M = len(info)
    P = np.eye(M) - 1.0 / M
    return P @ np.linalg.inv(info) @ P


def online_elo(i, j, y, M, K=4.0, init=1000.0, every=0) -> tuple[np.ndarray, np.ndarray]:
    """The online Elo update, battle by battle: R_a += K (S - E), E = 1 / (1 + 10^((R_b - R_a) / 400)).
    Returns the final ratings and (if ``every``) a snapshot every ``every`` battles."""
    R = np.full(M, init)
    snaps = []
    for k, (a, b, s) in enumerate(zip(i, j, y)):
        e = 1.0 / (1.0 + 10 ** ((R[b] - R[a]) / 400))
        R[a] += K * (s - e)
        R[b] -= K * (s - e)
        if every and (k + 1) % every == 0:
            snaps.append(R.copy())
    return R, np.array(snaps)


def battles(g, theta, n, M=None):
    """n battles between uniformly random pairs of different models; y = 1 if the first won."""
    M = M or len(theta)
    i = g.integers(0, M, n)
    j = (i + g.integers(1, M, n)) % M
    y = (g.random(n) < sigmoid(theta[i] - theta[j])).astype(float)
    return i, j, y


def bootstrap_bt(i, j, y, M, g, boots=200) -> np.ndarray:
    """Bradley-Terry strengths refitted on ``boots`` resamples of the battles (with replacement)."""
    n = len(i)
    out = np.zeros((boots, M))
    for b in range(boots):
        k = g.integers(0, n, n)
        out[b] = bt_fit(wins_matrix(i[k], j[k], y[k], M))[0]
    return out


def best_of_k_inflation(g, theta_field, ks, n_votes, reps=400, true=0.0) -> np.ndarray:
    """The 'private variants' effect: k variants of one model, all of true strength ``true``, each rated from n_votes
    battles against a field of known strengths; the best-rated variant is published.  Returns, for each k, the mean
    of the published rating minus the truth (natural units)."""
    kmax = max(ks)
    opp = g.integers(0, len(theta_field), (reps, kmax, n_votes))
    to = theta_field[opp]
    y = (g.random((reps, kmax, n_votes)) < sigmoid(true - to)).astype(float)
    t = np.zeros((reps, kmax))
    for _ in range(30):  # one-dimensional Newton for each variant, the field held fixed
        p = sigmoid(t[..., None] - to)
        grad = (y - p).sum(-1) - t / 9
        hess = (p * (1 - p)).sum(-1) + 1 / 9
        t = t + grad / hess
    return np.array([t[:, :k].max(1).mean() - true for k in ks])


# ---------------------------------------------------------------------------
# A biased judge
# ---------------------------------------------------------------------------
def judge_battles(g, theta, length, sibling, n, pos=0.0, ln=0.0, self_pref=0.0, both_orders=False):
    """Pairwise verdicts.  Each answer's length is its model's typical length plus noise; the judge sees one answer
    first and prefers it with log-odds  (t_first - t_second) + pos + ln (L_first - L_second) + self (s_first -
    s_second),  where s = 1 for models of the judge's own family.  With ``both_orders`` each pair is judged twice,
    swapped, and an inconsistent pair counts as a tie (Zheng et al. 2023).  Returns i, j, y (y = 1 if i won, 0.5 a
    tie), the answers' length difference L_i - L_j, a flag for 'i was shown first', and the consistency rate."""
    M = len(theta)
    i = g.integers(0, M, n)
    j = (i + g.integers(1, M, n)) % M
    Li = length[i] + 0.3 * g.standard_normal(n)
    Lj = length[j] + 0.3 * g.standard_normal(n)
    si, sj = sibling[i].astype(float), sibling[j].astype(float)

    def verdict(first_is_i):
        d = np.where(first_is_i, 1.0, -1.0)  # +1: i shown first
        z = (theta[i] - theta[j]) + d * pos + ln * (Li - Lj) + self_pref * (si - sj)
        return (g.random(n) < sigmoid(z)).astype(float)  # 1 if i preferred

    if not both_orders:
        first = g.random(n) < 0.5
        return i, j, verdict(first), Li - Lj, first.astype(float), float("nan")
    a, b = verdict(np.ones(n, bool)), verdict(np.zeros(n, bool))
    consistent = a == b
    y = np.where(consistent, a, 0.5)
    return i, j, y, Li - Lj, np.full(n, 0.5), float(consistent.mean())


def bt_with_covariates(i, j, y, X, M, iters=60, prior=1 / 9):
    """Bradley-Terry with extra covariates (the style-control regression): log-odds that i beats j =
    t_i - t_j + X @ beta.  Newton on (t, beta) jointly, t centred.  Returns t and beta."""
    n, k = X.shape
    D = np.zeros((n, M))
    D[np.arange(n), i] += 1
    D[np.arange(n), j] -= 1
    A = np.hstack([D, X])
    w = np.zeros(M + k)
    reg = np.r_[np.full(M, prior), np.full(k, 1e-6)]
    for _ in range(iters):
        p = sigmoid(A @ w)
        g_ = A.T @ (y - p) - reg * w
        H = (A * (p * (1 - p))[:, None]).T @ A + np.diag(reg)
        step = np.linalg.solve(H, g_)
        w += step
        w[:M] -= w[:M].mean()
        if np.abs(step).max() < 1e-10:
            break
    return w[:M], w[M:]


# ---------------------------------------------------------------------------
# Item response theory (2PL)
# ---------------------------------------------------------------------------
def irt_fit(R: np.ndarray, iters=400, lr=0.5) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Joint maximum likelihood for the 2PL model P(model m answers item q) = sigmoid(a_q (theta_m - b_q)), from a 0/1
    response matrix R (models x items).  Abilities are standardized each step (the scale is otherwise free).
    Plain gradient ascent with per-parameter step sizes from the diagonal curvature."""
    M, Q = R.shape
    th = np.zeros(M)
    a = np.ones(Q)
    b = -np.log((R.mean(0) + 0.01) / (1.01 - R.mean(0)))
    for _ in range(iters):
        z = a[None] * (th[:, None] - b[None])
        p = sigmoid(z)
        r = R - p
        w = p * (1 - p)
        th += lr * (r * a[None]).sum(1) / ((w * a[None] ** 2).sum(1) + 1e-3)
        th = (th - th.mean()) / th.std()
        z = a[None] * (th[:, None] - b[None])
        p = sigmoid(z)
        r, w = R - p, p * (1 - p)
        u = th[:, None] - b[None]
        a += lr * ((r * u).sum(0) - 0.1 * (a - 1)) / ((w * u ** 2).sum(0) + 0.1)
        a = np.clip(a, 0.15, 6.0)
        b += lr * (-(r * a[None]).sum(0) - 0.05 * b) / ((w * a[None] ** 2).sum(0) + 0.05)
    return th, a, b


def irt_ability(resp, a, b, iters=40) -> float:
    """A new model's ability from its answers to some items whose parameters are known (MAP, standard normal prior)."""
    t = 0.0
    for _ in range(iters):
        p = sigmoid(a * (t - b))
        g = (a * (resp - p)).sum() - t
        h = (a * a * p * (1 - p)).sum() + 1
        t += g / h
    return t


# ---------------------------------------------------------------------------
# AI control: trusted monitoring with an audit budget (Greenblatt et al. 2023), in closed form
# ---------------------------------------------------------------------------
def norm_sf(x):
    return 0.5 * math.erfc(x / math.sqrt(2))


def norm_isf(q, lo=-10.0, hi=10.0):
    for _ in range(100):
        mid = (lo + hi) / 2
        if norm_sf(mid) > q:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def red_win_prob(p, c1, w1, n):
    """Per problem the red team attacks with probability p; an attack is caught (blue wins, the game ends) with
    probability c1 and succeeds unnoticed (red wins) with probability w1.  Over n problems:
    P(red wins) = w / (c + w) * (1 - (1 - c - w)^n),  c = p c1, w = p w1."""
    c, w = p * c1, p * w1
    if c + w == 0:
        return 0.0
    return w / (c + w) * (1 - (1 - c - w) ** n)


def control_game(mu=2.0, success=0.3, audit=0.02, n=5000, defer=(0.0, 0.05, 0.1, 0.2, 0.3, 0.5, 0.75, 1.0)):
    """The monitor's suspicion of honest code ~ N(0, 1) and of backdoored code ~ N(mu, 1).  The top ``audit`` share of
    suspicion (by the honest distribution) is audited by a human; with defer-to-trusted, code between that and the top
    ``f`` share is replaced by the trusted model's own solution (useful 0 on the rescaled scale, and never
    backdoored).  A backdoor that is submitted works with probability ``success``.  The red team picks the attack
    rate that maximizes its chance of winning.  Returns, per protocol, (usefulness, safety, red's best attack rate)."""
    ps = np.unique(np.r_[np.geomspace(1e-5, 1, 400), 1.0])
    t_audit = norm_isf(audit)
    rows = []
    for f in defer:
        t_def = norm_isf(max(f, audit)) if f > audit else t_audit
        caught = norm_sf(t_audit - mu)
        submitted = 1 - norm_sf(t_def - mu)  # below the deferral threshold: U's code goes out
        win = submitted * success
        red = [red_win_prob(p, caught, win, n) for p in ps]
        k = int(np.argmax(red))
        use = 1 - max(0.0, f - audit) if f > audit else 1.0
        rows.append(dict(defer=f, usefulness=use, safety=1 - red[k], p=float(ps[k]), caught=caught, win=win))
    # upfront auditing: the first `audit` share of problems are all audited, none after
    m = int(round(audit * n))
    red = [(1 - p) ** m * (1 - (1 - p * success) ** (n - m)) for p in ps]
    k = int(np.argmax(red))
    upfront = dict(usefulness=1.0, safety=1 - red[k], p=float(ps[k]))
    curve = [(float(p), float(r)) for p, r in zip(ps, [red_win_prob(p, norm_sf(t_audit - mu),
                                                                     (1 - norm_sf(t_audit - mu)) * success, n)
                                                        for p in ps])]
    return dict(rows=rows, upfront=upfront, t_audit=t_audit, red_curve=curve, mu=mu, success=success, audit=audit,
                n=n)


def control_replay(g, mu, success, audit, n, p, defer=0.0):
    """One game played out problem by problem: suspicion of each submission, attacks, audits, the outcome."""
    t_audit = norm_isf(audit)
    t_def = norm_isf(defer) if defer > audit else t_audit
    attack = g.random(n) < p
    s = g.standard_normal(n) + mu * attack
    works = g.random(n) < success
    caught = np.flatnonzero(attack & (s > t_audit))
    landed = np.flatnonzero(attack & (s <= t_def) & works)
    kc = caught[0] if len(caught) else n
    kl = landed[0] if len(landed) else n
    if kc == n and kl == n:
        outcome, at = "none", n - 1
    elif kc < kl:
        outcome, at = "caught", int(kc)
    else:
        outcome, at = "backdoor", int(kl)
    return dict(s=s[:at + 1], attack=attack[:at + 1], outcome=outcome, at=at, t_audit=t_audit, t_def=t_def)


# ---------------------------------------------------------------------------
# The boat race: a gridworld with a gameable reward (after OpenAI's CoastRunners clip, 2016)
# ---------------------------------------------------------------------------
TRACK = [
    "###########",
    "#.........#",
    "#.##...##.#",
    "#.##...##.#",
    "#.#######.#",
    "#.S#F.....#",
    "###########",
]
TARGETS = [(2, 4), (3, 5), (2, 6)]  # in the lagoon: each pays when hit, then waits until another target is hit
MOVES = [(-1, 0), (0, 1), (1, 0), (0, -1)]  # up, right, down, left


class BoatRace:
    """State: (row, col, the last target hit, or 3 for none).  The finish F lies behind a wall from the start S, so
    finishing takes a lap.  Proxy reward: +1 per target hit (a target pays again only after another one is hit) and
    +5 at the finish.  The race ends at the finish, or after ``horizon`` steps."""

    def __init__(self, horizon=120):
        self.grid = [list(r) for r in TRACK]
        self.R, self.C = len(TRACK), len(TRACK[0])
        self.start = next((r, c) for r in range(self.R) for c in range(self.C) if TRACK[r][c] == "S")
        self.finish = next((r, c) for r in range(self.R) for c in range(self.C) if TRACK[r][c] == "F")
        self.horizon = horizon
        # progress along the lap (for the potential), by breadth-first distance to the finish around the track
        self.dist = self._dist_to_finish()

    def free(self, r, c):
        return 0 <= r < self.R and 0 <= c < self.C and TRACK[r][c] != "#"

    def _dist_to_finish(self):
        from collections import deque

        d = {self.finish: 0}
        q = deque([self.finish])
        while q:
            r, c = q.popleft()
            for dr, dc in MOVES:
                n = (r + dr, c + dc)
                if self.free(*n) and n not in d:
                    d[n] = d[(r, c)] + 1
                    q.append(n)
        return d

    def n_states(self):
        return self.R * self.C * 4

    def index(self, r, c, last):
        return (r * self.C + c) * 4 + last

    def step(self, r, c, last, a):
        dr, dc = MOVES[a]
        nr, nc = r + dr, c + dc
        if not self.free(nr, nc):
            nr, nc = r, c
        reward, done = 0.0, False
        if (nr, nc) in TARGETS:
            k = TARGETS.index((nr, nc))
            if k != last:
                reward += 1.0
                last = k
        if (nr, nc) == self.finish:
            reward += 5.0
            done = True
        return nr, nc, last, reward, done


def q_learning(env: BoatRace, mode="proxy", episodes=3000, alpha=0.3, gamma=0.98, eps=0.1, seed=0, snaps=(),
               eval_every=50):
    """Tabular Q-learning.  ``mode``: 'proxy' (targets and finish), 'sparse' (finish only), or 'shaped' (finish
    plus the potential-based shaping gamma Phi(s') - Phi(s), with Phi = 5 x the share of the lap done, and Phi = 0
    once the race is over: Ng, Harada & Russell 1999).
    Returns the learning curves (episode, proxy return of the greedy policy, finished?, steps), and greedy
    trajectories at the snapshot episodes."""
    g = rng(seed)
    Q = np.zeros((env.n_states(), 4))
    D = max(env.dist.values())
    phi = lambda r, c: 5.0 * (1 - env.dist[(r, c)] / D)  # noqa: E731
    curves, trajs = [], {}

    def greedy_run():
        r, c, last = *env.start, 3
        path, ret, fin = [(r, c)], 0.0, False
        for _ in range(env.horizon):
            s = env.index(r, c, last)
            a = int(np.argmax(Q[s] + 1e-9 * g.random(4)))
            r, c, last, rew, done = env.step(r, c, last, a)
            path.append((r, c))
            ret += rew
            if done:
                fin = True
                break
        return path, ret, fin

    for ep in range(episodes + 1):
        if ep in snaps:
            trajs[ep] = greedy_run()[0]
        if ep % eval_every == 0:
            path, ret, fin = greedy_run()
            curves.append((ep, ret, float(fin), len(path) - 1))
        if ep == episodes:
            break
        r, c, last = *env.start, 3
        for _ in range(env.horizon):
            s = env.index(r, c, last)
            a = int(g.integers(4)) if g.random() < eps else int(np.argmax(Q[s] + 1e-9 * g.random(4)))
            nr, nc, nl, rew, done = env.step(r, c, last, a)
            if mode == "sparse":
                rew = 5.0 if done else 0.0
            elif mode == "shaped":
                rew = (5.0 if done else 0.0) + (gamma * (0.0 if done else phi(nr, nc)) - phi(r, c))
            s2 = env.index(nr, nc, nl)
            target = rew + (0.0 if done else gamma * Q[s2].max())
            Q[s, a] += alpha * (target - Q[s, a])
            r, c, last = nr, nc, nl
            if done:
                break
    return np.array(curves), trajs, Q
