"""Precompute everything numerical in Part 26 of the AI series ("Reinforcement Learning, from Bellman to AlphaZero").

    python -m videos.ai.ai26.alphazero           # first: train AlphaZero on Connect Four (hours; resumable)
    python -m videos.ai.ai26.compute             # everything missing
    python -m videos.ai.ai26.compute --force dqn

Results are cached in ``.cache/ai26/<name>.json`` (+ ``.npz``); scenes call ``load(name)``. Every agent here learns
on this machine; the numbers about AlphaGo and its successors are the published ones, cited on screen.

Items:
    bandit     the 10-armed testbed (Sutton & Barto): greedy, epsilon-greedy, UCB and Thompson sampling, 2,000 runs of
               1,000 pulls; a two-armed coin bandit's regret over 50,000 pulls against the Lai-Robbins bound; one UCB
               run step by step (estimates, counts, confidence bounds)
    grid       the slippery gridworld: value iteration sweep by sweep from two starts (the contraction), the
               greedy policy, policy iteration, and the random policy's values
    walk       the 5-state random walk: TD(0) against Monte Carlo (RMS error over episodes); TD(lambda) on 19 states
    cliff      the cliff walk: Sarsa against Q-learning, reward per episode and the paths they learn
    maxbias    the maximization bias (Sutton & Barto, Example 6.7): Q-learning against double Q-learning; the expected
               maximum of k noisy estimates of zero
    dqn        DQN on the cart-pole: with replay and a target network, and without each; learning curves, and the
               trained policy balancing (a trajectory to draw)
    pg         policy gradients on the cart-pole: REINFORCE, with a baseline, actor-critic (GAE) and PPO; PPO's
               training replayed (its policy over the state space, and one episode, at checkpoints)
    pg_cloud   the spread of single-episode gradient estimates with and without a baseline
    alphabeta  nodes searched by minimax and by alpha-beta (random and centre-first move order) on Connect Four
    testset    400 Connect Four positions from 8 to 24 stones, every move scored by the perfect solver
    uct        plain Monte Carlo tree search: how often its move is a perfect one, against the number of simulations
    uct_tree   plain MCTS from one position: the tree after 10, 40, 160, 640 and 2,560 simulations
    az_grade   AlphaZero, generation by generation: how often the raw network and the network with search play a
               perfect move; the value head against the true result; the training log
    az_elo     ratings of AlphaZero's generations and of plain MCTS from a round robin (Bradley-Terry fit)
    az_demo    one position seen by the network across generations (policy, value, search visits); the search tree
               from it; a game by the final network, every move checked by the solver
    rps        regret matching on rock-paper-scissors: the current and the average strategy
    kuhn       counterfactual regret minimization on Kuhn poker: exploitability, and the value -1/18
    go         AlphaGo against Lee Sedol (2016): the boards at game 2, move 37, and game 4, move 78, from the game
               records (Andries Brouwer's archive), replayed with captures
"""

from __future__ import annotations

import math

import numpy as np

from explainer.ai.cache import Cache
from videos.ai.ai26 import c4
from videos.ai.ai26.envs import (ACTIONS, CLIFF_COLS, CLIFF_ROWS, CartPole, GridWorld, cliff_step,
                                 walk_episode)

CACHE = Cache("ai26")
load = CACHE.load


def rng(seed: int) -> np.random.Generator:
    return np.random.Generator(np.random.PCG64(seed))


# ---------------------------------------------------------------------------
# Bandits
# ---------------------------------------------------------------------------
def testbed(method: str, R=2000, T=1000, k=10, seed=0, eps=0.1, c=2.0):
    g = rng(seed)
    q = g.normal(0, 1, (R, k))
    best = q.argmax(1)
    Q, N = np.zeros((R, k)), np.zeros((R, k))
    mu, prec = np.zeros((R, k)), np.ones((R, k))  # Thompson: Gaussian posterior (prior N(0, 1), noise variance 1)
    reward, optimal, regret = np.zeros(T), np.zeros(T), np.zeros(T)
    rows = np.arange(R)
    for t in range(T):
        if method == "greedy":
            a = np.argmax(Q + 1e-9 * g.random((R, k)), 1)
        elif method == "eps":
            a = np.argmax(Q + 1e-9 * g.random((R, k)), 1)
            explore = g.random(R) < eps
            a[explore] = g.integers(0, k, explore.sum())
        elif method == "ucb":
            bonus = np.where(N > 0, c * np.sqrt(np.log(t + 1) / np.maximum(N, 1)), np.inf)
            a = np.argmax(Q + bonus + 1e-9 * g.random((R, k)), 1)
        elif method == "thompson":
            a = np.argmax(g.normal(mu, 1 / np.sqrt(prec)), 1)
        r = g.normal(q[rows, a], 1)
        N[rows, a] += 1
        Q[rows, a] += (r - Q[rows, a]) / N[rows, a]
        mu[rows, a] = (prec[rows, a] * mu[rows, a] + r) / (prec[rows, a] + 1)
        prec[rows, a] += 1
        reward[t] = r.mean()
        optimal[t] = (a == best).mean()
        regret[t] = (q[rows, best] - q[rows, a]).mean()
    return reward, optimal, np.cumsum(regret)


def coin_bandit(method: str, p=(0.4, 0.6), R=1000, T=50000, seed=1):
    g = rng(seed)
    p = np.array(p)
    k = len(p)
    S, N = np.zeros((R, k)), np.zeros((R, k))
    regret = np.zeros(T)
    rows = np.arange(R)
    gap = p.max() - p
    for t in range(T):
        if method == "ucb":
            m = np.where(N > 0, S / np.maximum(N, 1) + np.sqrt(2 * np.log(t + 1) / np.maximum(N, 1)), np.inf)
            a = np.argmax(m + 1e-9 * g.random((R, k)), 1)
        elif method == "thompson":
            a = np.argmax(g.beta(S + 1, N - S + 1), 1)
        elif method == "eps":
            a = np.argmax(np.where(N > 0, S / np.maximum(N, 1), 1.0) + 1e-9 * g.random((R, k)), 1)
            ex = g.random(R) < 0.1
            a[ex] = g.integers(0, k, ex.sum())
        r = (g.random(R) < p[a]).astype(float)
        S[rows, a] += r
        N[rows, a] += 1
        regret[t] = gap[a].mean()
    return np.cumsum(regret)


def kl_bern(a, b):
    return a * math.log(a / b) + (1 - a) * math.log((1 - a) / (1 - b))


def compute_bandit():
    out = {}
    for m in ("greedy", "eps", "eps01", "ucb", "thompson"):
        meth, eps = ("eps", 0.01) if m == "eps01" else (m, 0.1)
        rw, op, rg = testbed(meth, eps=eps)
        out[f"reward_{m}"], out[f"optimal_{m}"], out[f"regret_{m}"] = rw, op, rg
    p = (0.4, 0.6)
    for m in ("eps", "ucb", "thompson"):
        out[f"coin_{m}"] = coin_bandit(m, p)
    T = len(out["coin_ucb"])
    out["coin_p"] = list(p)
    out["lai_robbins_c"] = (p[1] - p[0]) / kl_bern(p[0], p[1])  # regret >= c log T, asymptotically
    # one UCB run on five arms, step by step, for the picture
    g = rng(7)
    q = np.array([0.2, 0.8, -0.3, 0.5, 0.1])
    k, steps = len(q), 300
    Q, N = np.zeros(k), np.zeros(k)
    est, cnt, ucb, act = np.zeros((steps, k)), np.zeros((steps, k)), np.zeros((steps, k)), np.zeros(steps, int)
    for t in range(steps):
        bonus = np.where(N > 0, np.sqrt(2 * np.log(t + 1) / np.maximum(N, 1)), 9.0)  # the bound derived on screen
        a = int(np.argmax(np.where(N > 0, Q, 0.0) + bonus))
        r = g.normal(q[a], 1)
        N[a] += 1
        Q[a] += (r - Q[a]) / N[a]
        est[t], cnt[t], act[t] = Q, N, a
        ucb[t] = Q + np.where(N > 0, np.sqrt(2 * np.log(t + 2) / np.maximum(N, 1)), 9.0)
    out.update(ucb_q=q, ucb_est=est, ucb_cnt=cnt, ucb_bound=ucb, ucb_act=act)
    assert out["regret_ucb"][-1] < out["regret_eps"][-1] < out["regret_greedy"][-1]
    assert out["coin_ucb"][-1] < out["coin_eps"][-1] and out["coin_thompson"][-1] < out["coin_ucb"][-1]
    assert out["optimal_greedy"][-1] < 0.5 < out["optimal_ucb"][-1]
    out["T"] = T
    return out


# ---------------------------------------------------------------------------
# Dynamic programming on the gridworld
# ---------------------------------------------------------------------------
def compute_grid():
    env = GridWorld()
    V0 = np.zeros(env.n)
    Vs, pis = env.value_iteration(V0)
    Vstar = Vs[-1]
    V0b = rng(3).uniform(-1, 1, env.n) * 3  # a second, arbitrary start
    V0b[env.terminal] = env.exit_reward[env.terminal]
    Vsb, _ = env.value_iteration(V0b)
    err_a = np.abs(Vs - Vstar).max(1)
    err_b = np.abs(Vsb - Vstar).max(1)
    # the contraction: every sweep shrinks the distance between the two runs by at least gamma
    K = min(len(Vs), len(Vsb))
    gap = np.abs(Vs[:K] - Vsb[:K]).max(1)
    ratios = gap[1:40] / gap[:39]
    assert (ratios <= env.gamma + 1e-9).all(), ratios.max()
    pi_rand = np.full((env.n, 4), 0.25)
    V_rand = env.evaluate(pi_rand)
    pi0 = np.zeros(env.n, int)  # "always up"
    pis_pi, Vs_pi = env.policy_iteration(pi0)
    assert np.allclose(Vs_pi[-1], Vstar, atol=1e-6)
    pistar = pis[-1]
    # a greedy rollout of the optimal policy from the start (most likely path, ignoring slips)
    path, s = [env.start], env.start
    for _ in range(40):
        if env.terminal[s]:
            break
        s = int(np.argmax(env.P[pistar[s], s]))
        path.append(s)
    return {"rows": env.rows, "cols": env.cols, "layout": env.layout, "gamma": env.gamma, "slip": env.slip,
            "cells": [list(rc) for rc in env.cells], "terminal": env.terminal.astype(int).tolist(),
            "start": env.start, "V": Vs, "pi": pis, "Vb": Vsb, "err_a": err_a, "err_b": err_b, "gap": gap,
            "V_rand": V_rand, "pi_iter": np.array(pis_pi), "V_iter": np.array(Vs_pi), "pistar": pistar,
            "path": path, "sweeps": len(Vs) - 1}


# ---------------------------------------------------------------------------
# Temporal differences
# ---------------------------------------------------------------------------
def walk_rms(method, alpha, n=5, episodes=100, runs=100, seed=0):
    g = rng(seed)
    true = np.arange(1, n + 1) / (n + 1)
    out = np.zeros(episodes + 1)
    for _ in range(runs):
        V = np.full(n + 2, 0.5)
        V[0] = V[n + 1] = 0.0
        out[0] += np.sqrt(((V[1:n + 1] - true) ** 2).mean())
        for e in range(episodes):
            states, rewards = walk_episode(n, g)
            if method == "td":
                nxt = states[1:] + [None]
                for s, r, s2 in zip(states, rewards, nxt):
                    target = r + (V[s2] if s2 is not None else 0.0)
                    V[s] += alpha * (target - V[s])
            else:  # every-visit Monte Carlo: the return is the final reward (no discount)
                G = rewards[-1]
                for s in states:
                    V[s] += alpha * (G - V[s])
            out[e + 1] += np.sqrt(((V[1:n + 1] - true) ** 2).mean())
    return out / runs


def td_lambda_rms(lam, alpha, n=19, episodes=10, runs=50, seed=0):
    """Online TD(lambda) with accumulating traces on the 19-state walk (rewards -1 left, +1 right)."""
    g = rng(seed)
    true = np.linspace(-1, 1, n + 2)[1:-1]
    tot = 0.0
    for _ in range(runs):
        V = np.zeros(n + 2)
        for _ in range(episodes):
            s = (n + 1) // 2
            z = np.zeros(n + 2)
            while True:
                s2 = s + (1 if g.random() < 0.5 else -1)
                r = 1.0 if s2 == n + 1 else (-1.0 if s2 == 0 else 0.0)
                v2 = 0.0 if s2 in (0, n + 1) else V[s2]
                delta = r + v2 - V[s]
                z *= lam
                z[s] += 1
                V += alpha * delta * z
                if s2 in (0, n + 1):
                    break
                s = s2
            err = np.sqrt(((V[1:n + 1] - true) ** 2).mean())
            if not np.isfinite(err) or err > 10:  # diverged (large step sizes with lambda near 1)
                return np.inf
            tot += err
    return tot / (runs * episodes)


def compute_walk():
    out = {}
    for a in (0.05, 0.1, 0.15):
        out[f"td_{a}"] = walk_rms("td", a)
    for a in (0.01, 0.02, 0.03, 0.04):
        out[f"mc_{a}"] = walk_rms("mc", a)
    # one TD run, for the picture: the estimates after 0, 1, 10 and 100 episodes
    g = rng(5)
    V = np.full(7, 0.5)
    V[0] = V[6] = 0.0
    snaps = {0: V[1:6].copy()}
    for e in range(1, 101):
        states, rewards = walk_episode(5, g)
        for s, r, s2 in zip(states, rewards, states[1:] + [None]):
            V[s] += 0.1 * (r + (V[s2] if s2 is not None else 0.0) - V[s])
        if e in (1, 10, 100):
            snaps[e] = V[1:6].copy()
    out["snap_eps"] = [0, 1, 10, 100]
    out["snaps"] = np.array([snaps[e] for e in (0, 1, 10, 100)])
    lams = [0.0, 0.4, 0.8, 0.9, 0.95, 0.975, 1.0]
    alphas = np.linspace(0.05, 1.0, 12)
    table = np.array([[td_lambda_rms(l, a) for a in alphas] for l in lams])
    out.update(lams=lams, alphas=alphas, lam_rms=np.minimum(table, 0.7))
    best = table.min(1)
    print("  best RMS by lambda:", dict(zip(lams, np.round(best, 3))))
    assert best[2] < best[0] and best[2] < best[-1]  # an intermediate lambda beats both TD(0) and Monte Carlo
    assert out["td_0.1"][-1] < out["mc_0.02"][-1]
    return out


CLIFF_SNAPS = (1, 5, 10, 25, 50, 100, 200, 500)


def cliff_greedy_path(Q, limit=60):
    r, c, path = CLIFF_ROWS - 1, 0, [(CLIFF_ROWS - 1, 0)]
    for _ in range(limit):
        r, c, _, done = cliff_step(r, c, int(np.argmax(Q[r, c])))
        path.append((r, c))
        if done:
            break
    return path


def compute_cliff(runs=100, episodes=500, alpha=0.5, eps=0.1, seed=0):
    g = rng(seed)
    curves = {"sarsa": np.zeros(episodes), "q": np.zeros(episodes)}
    finals = {}
    snaps = {m: {"V": [], "path": [], "episode": []} for m in ("sarsa", "q")}  # run 0, as it learns
    for method in ("sarsa", "q"):
        for run in range(runs):
            Q = np.zeros((CLIFF_ROWS, CLIFF_COLS, 4))

            def act(r, c):
                if g.random() < eps:
                    return int(g.integers(4))
                v = Q[r, c]
                return int(g.choice(np.flatnonzero(v == v.max())))

            for e in range(episodes):
                r, c = CLIFF_ROWS - 1, 0
                a = act(r, c)
                total = 0.0
                walked = [(r, c)]
                for _ in range(1000):
                    r2, c2, rew, done = cliff_step(r, c, a)
                    walked.append((r2, c2) if rew > -100 else (CLIFF_ROWS - 1, max(c + ACTIONS[a][1], 1)))
                    if rew <= -100:
                        walked.append((r2, c2))
                    total += rew
                    a2 = act(r2, c2)
                    target = rew + (0.0 if done else (Q[r2, c2, a2] if method == "sarsa" else Q[r2, c2].max()))
                    Q[r, c, a] += alpha * (target - Q[r, c, a])
                    r, c, a = r2, c2, a2
                    if done:
                        break
                curves[method][e] += total / runs
                if run == 0 and e + 1 in CLIFF_SNAPS:
                    snaps[method]["V"].append(Q.max(2).copy())
                    snaps[method]["path"].append(cliff_greedy_path(Q))
                    snaps[method]["episode"].append(walked[:400])
            if run == 0:
                finals[method] = Q.copy()
    paths = {m: cliff_greedy_path(Q) for m, Q in finals.items()}
    # the safe path keeps away from the edge; the optimal one runs along it
    assert min(p[0] for p in paths["sarsa"][1:-1]) < CLIFF_ROWS - 2
    assert all(p[0] >= CLIFF_ROWS - 2 for p in paths["q"])
    late = slice(episodes // 2, None)
    assert curves["sarsa"][late].mean() > curves["q"][late].mean()
    out = {"sarsa": curves["sarsa"], "q": curves["q"], "path_sarsa": paths["sarsa"], "path_q": paths["q"],
           "rows": CLIFF_ROWS, "cols": CLIFF_COLS, "alpha": alpha, "eps": eps, "snap_episodes": list(CLIFF_SNAPS)}
    for m in ("sarsa", "q"):
        out[f"snapV_{m}"] = np.array(snaps[m]["V"])
        out[f"snap_path_{m}"] = snaps[m]["path"]
        out[f"snap_walk_{m}"] = snaps[m]["episode"]
    return out


def compute_maxbias(runs=5000, episodes=300, n_b=10, alpha=0.1, eps=0.1, seed=0):
    g = rng(seed)
    left = {"q": np.zeros(episodes), "double": np.zeros(episodes)}
    for method in ("q", "double"):
        for _ in range(runs):
            QA = np.zeros((2, 2))  # [table, action] at A: 0 = left (to B), 1 = right (end, reward 0)
            QB = np.zeros((2, n_b))
            for e in range(episodes):
                qa = QA[0] + QA[1]
                a = int(g.integers(2)) if g.random() < eps else int(g.choice(np.flatnonzero(qa == qa.max())))
                left[method][e] += (a == 0) / runs
                if a == 1:
                    i = int(g.integers(2)) if method == "double" else 0
                    QA[i, 1] += alpha * (0 - QA[i, 1])
                    continue
                # step to B with reward 0, bootstrap from B
                if method == "q":
                    QA[0, 0] += alpha * (QB[0].max() - QA[0, 0])
                else:
                    i = int(g.integers(2))
                    QA[i, 0] += alpha * (QB[1 - i, int(np.argmax(QB[i]))] - QA[i, 0])
                qb = QB[0] + QB[1]
                b = int(g.integers(n_b)) if g.random() < eps else int(g.choice(np.flatnonzero(qb == qb.max())))
                r = g.normal(-0.1, 1.0)
                i = int(g.integers(2)) if method == "double" else 0
                QB[i, b] += alpha * (r - QB[i, b])
    # E[max of k independent N(0, 1)] (Monte Carlo, 10^6 draws): the bias of trusting the largest of k noisy zeros
    z = rng(9).normal(size=(1_000_000, 10))
    emax = [float(z[:, :k].max(1).mean()) for k in range(1, 11)]
    assert left["q"][5:50].max() > 0.55 and left["double"][20:60].mean() < 0.2
    return {"left_q": left["q"], "left_double": left["double"], "optimal_left": eps / 2, "emax": emax}


# ---------------------------------------------------------------------------
# Deep RL on the cart-pole
# ---------------------------------------------------------------------------
DQN_STEPS = 50_000
DQN_SEEDS = 5


def mlp(sizes, act="tanh"):
    import torch.nn as nn

    layers = []
    for a, b in zip(sizes[:-1], sizes[1:]):
        layers += [nn.Linear(a, b), nn.Tanh() if act == "tanh" else nn.ReLU()]
    return nn.Sequential(*layers[:-1])


def run_dqn(seed, steps=DQN_STEPS, replay=True, target=True, gamma=0.99, snap_steps=(), lr=2.3e-3, batch=64,
            buffer=100_000, start=1000, every=256, grad_steps=128, target_every=10, eps_end=0.04, eps_frac=0.16,
            hidden=256):
    """DQN with the tuned cart-pole settings of RL Baselines3 Zoo: a replay memory, Huber loss, a target network
    copied from the online one every ``target_every`` environment steps (so it holds still through each burst of
    ``grad_steps`` updates, made every ``every`` environment steps).  ``replay=False`` trains on the latest ``batch``
    steps only; ``target=False`` bootstraps from the online network itself."""
    import torch
    import torch.nn.functional as F

    torch.manual_seed(seed)
    g = rng(seed)
    env = CartPole(g)
    q = mlp([4, hidden, hidden, 2], "relu")
    qt = mlp([4, hidden, hidden, 2], "relu")
    qt.load_state_dict(q.state_dict())
    opt = torch.optim.Adam(q.parameters(), lr=lr)
    cap = buffer if replay else batch
    S, A, Rw, S2, D = (np.zeros((cap, 4), np.float32), np.zeros(cap, np.int64), np.zeros(cap, np.float32),
                       np.zeros((cap, 4), np.float32), np.zeros(cap, np.float32))
    n = ptr = 0
    s = env.reset()
    ep_ret, returns, snaps = 0.0, [], []
    for t in range(steps):
        if t in snap_steps:
            snaps.append((t, {k: v.clone() for k, v in q.state_dict().items()}))
        eps = max(eps_end, 1.0 - (1.0 - eps_end) * t / (eps_frac * steps))
        if g.random() < eps:
            a = int(g.integers(2))
        else:
            with torch.no_grad():
                a = int(q(torch.from_numpy(s.astype(np.float32))).argmax())
        s2, r, fell, trunc = env.step(a)
        S[ptr], A[ptr], Rw[ptr], S2[ptr], D[ptr] = s, a, r, s2, float(fell)
        ptr = (ptr + 1) % cap
        n = min(n + 1, cap)
        ep_ret += r
        s = s2
        if fell or trunc:
            returns.append((t + 1, ep_ret))
            s, ep_ret = env.reset(), 0.0
        if target and (t + 1) % target_every == 0:
            qt.load_state_dict(q.state_dict())
        if t + 1 >= start and (t + 1) % every == 0 and n >= batch:
            for _ in range(grad_steps):
                i = g.integers(0, n, batch) if replay else np.arange(n)  # without replay: just the latest steps
                sb, ab, rb, s2b, db = (torch.from_numpy(x[i]) for x in (S, A, Rw, S2, D))
                with torch.no_grad():
                    nxt = (qt if target else q)(s2b).max(1).values
                    y = rb + gamma * (1 - db) * nxt
                pred = q(sb).gather(1, ab[:, None]).squeeze(1)
                loss = F.smooth_l1_loss(pred, y)
                opt.zero_grad()
                loss.backward()
                torch.nn.utils.clip_grad_norm_(q.parameters(), 10.0)
                opt.step()
    if steps in snap_steps:
        snaps.append((steps, {k: v.clone() for k, v in q.state_dict().items()}))
    return np.array(returns), q, snaps


# the slice of state space the policy maps show: cart centred and still, pole angle x angular velocity
MAP_TH = np.linspace(-0.21, 0.21, 41)
MAP_THD = np.linspace(-2.0, 2.0, 41)


def map_states():
    TH, THD = np.meshgrid(MAP_TH, MAP_THD)  # rows: angular velocity, columns: angle
    S = np.zeros((TH.size, 4), np.float32)
    S[:, 2], S[:, 3] = TH.ravel(), THD.ravel()
    return S, TH.shape


def pad_trajs(trajs):
    L = max(len(t) for t in trajs)
    out = np.full((len(trajs), L, 4), np.nan)
    for i, t in enumerate(trajs):
        out[i, :len(t)] = t
    return out, np.array([len(t) for t in trajs])


def smooth_curve(returns, steps, grid):
    """Mean return of the episodes finishing in each window of the step grid."""
    out = np.full(len(grid), np.nan)
    if len(returns) == 0:
        return out
    t, r = returns[:, 0], returns[:, 1]
    w = grid[1] - grid[0]
    for j, x in enumerate(grid):
        m = (t > x - 2 * w) & (t <= x)
        if m.any():
            out[j] = r[m].mean()
    # carry the last value across empty windows
    for j in range(1, len(out)):
        if np.isnan(out[j]):
            out[j] = out[j - 1]
    return out


def rollout(policy, seed, steps=500):
    """States of one episode under ``policy(state) -> action`` (for drawing the cart and pole)."""
    env = CartPole(rng(seed))
    s = env.reset()
    traj = [s]
    for _ in range(steps):
        s, _, fell, trunc = env.step(policy(s))
        traj.append(s)
        if fell or trunc:
            break
    return np.array(traj)


def compute_dqn():
    import torch

    grid = np.arange(2000, DQN_STEPS + 1, 2000)
    out = {"grid": grid}
    snap_steps = (0, 2000, 5000, 8000, 12_000, 16_000, 20_000, 25_000, 30_000, 35_000, 40_000, 45_000, 50_000)
    runs = []
    for name, kw in (("full", {}), ("no_target", {"target": False}), ("no_replay", {"replay": False})):
        curves = []
        for seed in range(DQN_SEEDS):
            ret, q, snaps = run_dqn(seed, snap_steps=snap_steps if name == "full" else (), **kw)
            curves.append(smooth_curve(ret, DQN_STEPS, grid))
            if name == "full":
                runs.append((q, snaps, ret))
        out[name] = np.array(curves)
    # the replay shows the full DQN run that ends best (the ablation shows them all)
    late = np.nanmean(out["full"][:, -len(grid) // 5:], 1)
    best_run = int(np.argmax(late))
    net, saved, run0 = runs[best_run]
    out["replay_seed"] = best_run
    # the training, replayed: at each snapshot, the greedy policy over (angle, angular velocity) and one episode
    S, shape = map_states()
    qmaps, vmaps, trajs = [], [], []
    for t, sd in saved:
        m = mlp([4, 256, 256, 2], "relu")
        m.load_state_dict(sd)
        with torch.no_grad():
            Qs = m(torch.from_numpy(S)).numpy()
        qmaps.append((Qs[:, 1] - Qs[:, 0]).reshape(shape))
        vmaps.append(Qs.max(1).reshape(shape))
        trajs.append(rollout(lambda s, m=m: int(m(torch.from_numpy(s.astype(np.float32))).argmax()), 11))
    out["snap_steps"] = np.array([t for t, _ in saved])
    out["snap_qdiff"], out["snap_v"] = np.array(qmaps), np.array(vmaps)
    out["snap_traj"], out["snap_len"] = pad_trajs(trajs)
    out["run0"] = run0
    out["map_th"], out["map_thd"] = MAP_TH, MAP_THD
    pol = lambda s: int(net(torch.from_numpy(s.astype(np.float32))).argmax())
    out["traj_trained"] = rollout(pol, 11)
    coin = rng(0)
    out["traj_random"] = rollout(lambda s: int(coin.integers(2)), 11)
    return out


def compute_dqn_div():
    """The deadly triad, live: the largest value the network predicts, with and without a target network."""
    import torch

    S, _ = map_states()
    snaps = tuple(range(0, DQN_STEPS + 1, 1000))
    out = {"steps": np.array(snaps), "bound": 1 / (1 - 0.99)}  # returns here are at most 1 / (1 - gamma)
    for name, kw in (("full", {}), ("no_target", {"target": False})):
        _, _, saved = run_dqn(0, snap_steps=snaps, **kw)
        qmax = []
        for _, sd in saved:
            m = mlp([4, 256, 256, 2], "relu")
            m.load_state_dict(sd)
            with torch.no_grad():
                qmax.append(float(m(torch.from_numpy(S)).abs().max()))
        out[name] = np.array(qmax)
    return out


def pg_episodes(pi, env, n, g):
    import torch

    batch = []
    for _ in range(n):
        s = env.reset()
        S, A, Rw = [], [], []
        while True:
            with torch.no_grad():
                p = torch.softmax(pi(torch.from_numpy(s.astype(np.float32))), -1).numpy()
            a = int(g.random() < p[1])
            s2, r, fell, trunc = env.step(a)
            S.append(s)
            A.append(a)
            Rw.append(r)
            s = s2
            if fell or trunc:
                batch.append((np.array(S, np.float32), np.array(A), np.array(Rw, np.float32), fell, s.astype(np.float32)))
                break
    return batch


def discount(r, gamma):
    out = np.zeros_like(r)
    acc = 0.0
    for i in range(len(r) - 1, -1, -1):
        acc = r[i] + gamma * acc
        out[i] = acc
    return out



_PG = {"lr": 3e-3, "epochs": 1, "minibatches": 1, "episodes": 8, "vf_lr": 1e-3, "vf_epochs": 4}
PG_SEEDS = 8
PG_SETTINGS = {"reinforce": _PG, "baseline": _PG, "ac": _PG, "ppo": {**_PG, "lr": 1e-3, "epochs": 4, "minibatches": 4}}


def pg_train(method, seed, total=100_000, gamma=0.99, lam=0.95, snap_at=(), **kw):
    """One cart-pole run of a policy-gradient method; returns [(steps so far, episode return)] (and snapshots)."""
    import torch
    import torch.nn.functional as F

    cfg = {**PG_SETTINGS[method], **kw}
    torch.manual_seed(seed)
    g = rng(100 + seed)
    env = CartPole(g)
    pi, vf = mlp([4, 64, 64, 2]), mlp([4, 64, 64, 1])
    opt_pi, opt_vf = torch.optim.Adam(pi.parameters(), lr=cfg["lr"]), torch.optim.Adam(vf.parameters(), lr=cfg["vf_lr"])
    done_steps, returns, snaps = 0, [], []
    todo = list(snap_at)
    while done_steps < total:
        while todo and done_steps >= todo[0]:
            snaps.append((done_steps, {k: v.clone() for k, v in pi.state_dict().items()}))
            todo.pop(0)
        batch = pg_episodes(pi, env, cfg['episodes'], g)
        S = torch.from_numpy(np.concatenate([b[0] for b in batch]))
        A = torch.from_numpy(np.concatenate([b[1] for b in batch]))
        G = np.concatenate([discount(b[2], gamma) for b in batch])
        for b in batch:
            done_steps += len(b[2])
            returns.append((done_steps, float(b[2].sum())))
        with torch.no_grad():
            V = vf(S).squeeze(-1).numpy()
        if method in ("ac", "ppo"):  # generalized advantage estimation
            adv, k = np.zeros(len(V), np.float32), 0
            for b in batch:
                n = len(b[2])
                v = V[k:k + n]
                with torch.no_grad():
                    last = 0.0 if b[3] else float(vf(torch.from_numpy(b[4])).squeeze())
                v2 = np.append(v[1:], last)
                delta = b[2] + gamma * v2 - v
                adv[k:k + n] = discount(delta, gamma * lam)
                k += n
            ret = adv + V
        else:
            adv, ret = (G - V if method == "baseline" else G).astype(np.float32), G
        advt = torch.from_numpy(adv)
        if method in ("ac", "ppo", "baseline"):
            advt = (advt - advt.mean()) / (advt.std() + 1e-8)
        else:  # plain REINFORCE: the returns only rescaled (subtracting their mean would be a baseline)
            advt = advt / (advt.std() + 1e-8)
        rett = torch.from_numpy(ret.astype(np.float32))
        with torch.no_grad():
            old = torch.log_softmax(pi(S), -1).gather(1, A[:, None]).squeeze(1)
        n = len(A)
        for _ in range(cfg["epochs"]):  # PPO reuses each batch for several epochs; the others take one step
            for idx in torch.randperm(n).chunk(cfg["minibatches"]):
                logp = torch.log_softmax(pi(S[idx]), -1).gather(1, A[idx, None]).squeeze(1)
                if method == "ppo":
                    ratio = torch.exp(logp - old[idx])
                    lp = -torch.min(ratio * advt[idx], torch.clamp(ratio, 0.8, 1.2) * advt[idx]).mean()
                else:
                    lp = -(logp * advt[idx]).mean()
                opt_pi.zero_grad()
                lp.backward()
                opt_pi.step()
        if method != "reinforce":  # every critic gets the same fitting: regression on the batch's returns
            for _ in range(cfg["vf_epochs"]):
                for idx in torch.randperm(n).chunk(max(1, n // 256)):
                    opt_vf.zero_grad()
                    F.mse_loss(vf(S[idx]).squeeze(-1), rett[idx]).backward()
                    opt_vf.step()
    if todo:
        snaps.append((done_steps, {k: v.clone() for k, v in pi.state_dict().items()}))
    return (np.array(returns), snaps) if snap_at else np.array(returns)


def compute_pg():
    import torch


    grid = np.arange(4000, 100_001, 4000)
    out = {"grid": grid}
    for m in ("reinforce", "baseline", "ac", "ppo"):
        curves = []
        for s in range(PG_SEEDS):
            if m == "ppo" and s == 0:
                ret, snaps = pg_train(m, s, snap_at=(0, 4000, 8000, 15_000, 25_000, 40_000, 70_000, 100_000))
                out["run0"] = ret
            else:
                ret = pg_train(m, s)
            curves.append(smooth_curve(ret, 100_000, grid))
        out[m] = np.array(curves)
    # PPO's training, replayed: the probability of pushing right over (angle, angular velocity), and one episode
    S, shape = map_states()
    pmaps, trajs = [], []
    for t, sd in snaps:
        net = mlp([4, 64, 64, 2])
        net.load_state_dict(sd)
        with torch.no_grad():
            pmaps.append(torch.softmax(net(torch.from_numpy(S)), -1)[:, 1].numpy().reshape(shape))
            coin = rng(11)  # the policy as it acts in training: sampled, not its most likely action

            def act(s, net=net, coin=coin):
                p = torch.softmax(net(torch.from_numpy(s.astype(np.float32))), -1)[1].item()
                return int(coin.random() < p)

            trajs.append(rollout(act, 11))
    out["snap_steps"] = np.array([t for t, _ in snaps])
    out["snap_p"] = np.array(pmaps)
    out["snap_traj"], out["snap_len"] = pad_trajs(trajs)
    out["map_th"], out["map_thd"] = MAP_TH, MAP_THD
    return out


def compute_pg_cloud():
    """The spread of single-episode policy-gradient estimates, with and without a baseline."""
    import torch

    episodes = pg_episodes
    out = {}
    # the spread of one-episode gradient estimates at a fixed, half-trained policy: with and without a baseline
    torch.manual_seed(3)
    g = rng(3)
    env = CartPole(g)
    pi = mlp([4, 16, 2])
    warm = torch.optim.Adam(pi.parameters(), lr=1e-2)
    for _ in range(15):  # a little REINFORCE first, so episodes vary in length
        batch = episodes(pi, env, 8, g)
        S = torch.from_numpy(np.concatenate([b[0] for b in batch]))
        A = torch.from_numpy(np.concatenate([b[1] for b in batch]))
        G = torch.from_numpy(np.concatenate([discount(b[2], 0.99) for b in batch]))
        loss = -(torch.log_softmax(pi(S), -1).gather(1, A[:, None]).squeeze(1) * (G - G.mean())).mean()
        warm.zero_grad()
        loss.backward()
        warm.step()

    def grad_of(batch, base):
        b = batch[0]
        S, A = torch.from_numpy(b[0]), torch.from_numpy(b[1])
        G = discount(b[2], 0.99)
        w = torch.from_numpy((G - base(len(G))).astype(np.float32))
        pi.zero_grad()
        (torch.log_softmax(pi(S), -1).gather(1, A[:, None]).squeeze(1) * w).sum().backward()
        return torch.cat([p.grad.flatten() for p in pi.parameters()]).numpy().copy()

    eps_ = episodes(pi, env, 600, g)
    lengths = np.array([len(b[2]) for b in eps_])
    # the baseline: the average return-to-go at each time step (estimated from other episodes)
    maxT = lengths.max()
    gsum, gcnt = np.zeros(maxT), np.zeros(maxT)
    for b in eps_[300:]:
        G = discount(b[2], 0.99)
        gsum[:len(G)] += G
        gcnt[:len(G)] += 1
    bt = gsum / np.maximum(gcnt, 1)
    raw = np.array([grad_of([b], lambda n: np.zeros(n)) for b in eps_[:300]])
    based = np.array([grad_of([b], lambda n: bt[:n]) for b in eps_[:300]])
    mean = 0.5 * (raw.mean(0) + based.mean(0))
    u = mean / np.linalg.norm(mean)
    v = rng(4).normal(size=len(u))
    v -= (v @ u) * u
    v /= np.linalg.norm(v)
    out["cloud_raw"] = np.stack([raw @ u, raw @ v], 1)
    out["cloud_base"] = np.stack([based @ u, based @ v], 1)
    out["var_raw"] = float(((raw - raw.mean(0)) ** 2).sum(1).mean())
    out["var_base"] = float(((based - based.mean(0)) ** 2).sum(1).mean())
    out["mean_norm"] = float(np.linalg.norm(mean))
    assert out["var_base"] < out["var_raw"]
    return out


# ---------------------------------------------------------------------------
# Search on Connect Four
# ---------------------------------------------------------------------------
from numba import njit  # noqa: E402


@njit(cache=True)
def _heuristic(pos, mask):
    """A simple evaluation: (mover's open three-in-a-rows) - (opponent's), via the cells that would complete four."""
    mine = c4.popcount(c4.winning_cells(pos, mask))
    theirs = c4.popcount(c4.winning_cells(pos ^ mask, mask))
    return mine - theirs


@njit(cache=True)
def _search(pos, mask, depth, alpha, beta, prune, order_kind, counter, seed):
    """Depth-limited negamax. ``order_kind`` 0: a fresh random order at every node; 1: best-looking move first
    (children sorted by the static evaluation, the usual move ordering)."""
    counter[0] += 1
    if depth == 0:
        return float(_heuristic(pos, mask))
    cols = np.empty(7, np.int64)
    keys = np.empty(7, np.float64)
    n = 0
    for c in range(7):
        if c4.can_play(mask, c):
            cols[n] = c
            if order_kind == 1:
                if c4.is_winning_move(pos, mask, c):
                    keys[n] = -1e6
                else:
                    p2, m2 = c4.play(pos, mask, c)
                    keys[n] = _heuristic(p2, m2) - 0.01 * abs(c - 3)  # the opponent's view: low is good for us
            else:
                h = (counter[0] * 6364136223846793005 + seed * 1442695040888963407 + c * 2654435761) & 0x7FFFFFFF
                keys[n] = float(h)
            n += 1
    if n == 0:
        return 0.0
    idx = np.argsort(keys[:n])
    best = -1e9
    for k in range(n):
        c = cols[idx[k]]
        if c4.is_winning_move(pos, mask, c):
            v = 1000.0 + depth
        else:
            p2, m2 = c4.play(pos, mask, c)
            v = -_search(p2, m2, depth - 1, -beta, -alpha, prune, order_kind, counter, seed)
        if v > best:
            best = v
        if prune:
            if v > alpha:
                alpha = v
            if alpha >= beta:
                break
    return best


def compute_alphabeta():
    openings = [[3, 3, 2, 4], [3, 2, 3, 3, 4], [2, 3, 4, 3], [3, 3, 3, 2, 4, 4]]
    depths = list(range(1, 10))
    out = {"depths": depths}
    for name, prune, order in (("minimax", False, 0), ("ab_random", True, 0), ("ab_ordered", True, 1)):
        rows = []
        for d in depths:
            tot = 0
            for i, seq in enumerate(openings):
                b = c4.Board.from_moves(seq)
                cnt = np.zeros(1, np.int64)
                _search(np.int64(b.pos), np.int64(b.mask), d, -1e9, 1e9, prune, order, cnt, i + 1)
                tot += int(cnt[0])
            rows.append(tot / len(openings))
        out[name] = rows
    # b^d against b^(d/2): perfect ordering would search about 2 b^(d/2) positions
    out["branching"] = {"connect four": 7, "chess": 35, "go": 250}
    out["game_length"] = {"chess": 80, "go": 150}
    assert out["ab_ordered"][-1] < out["ab_random"][-1] < out["minimax"][-1]
    return out


def blunder_free_move(b: c4.Board, g) -> int:
    legal = b.legal()
    for c in legal:
        if b.wins_with(c):
            return c
    opp = c4.Board(b.pos ^ b.mask, b.mask, b.moves)
    blocks = [c for c in legal if opp.wins_with(c)]
    if blocks:
        return blocks[0]
    return int(legal[g.integers(len(legal))])


def compute_testset(n=400, seed=0):
    g = rng(seed)
    S = c4.Solver(24)
    out_moves, out_scores = [], []
    tries = 0
    while len(out_moves) < n:
        tries += 1
        stones = int(g.integers(8, 25))
        b = c4.Board()
        ok = True
        while b.moves < stones:
            c = blunder_free_move(b, g)
            nb = b.play(c)
            if c4.last_mover_won(nb) or nb.full():
                ok = False
                break
            b = nb
        if not ok:
            continue
        S.reset()
        sc = S.move_scores(b.pos, b.mask, b.moves)
        legal = ~np.isnan(sc)
        best = np.nanmax(sc)
        if (np.sign(sc[legal]) == np.sign(best)).all():  # no move throws anything away: nothing to test
            continue
        out_moves.append(list(b.history))
        out_scores.append(sc)
    scores = np.array(out_scores)
    best = np.nanmax(scores, 1)
    return {"histories": out_moves, "scores": scores, "value": np.sign(best).astype(int),
            "stones": np.array([len(h) for h in out_moves]), "tries": tries}


def is_right(scores_row, c) -> bool:
    """Does column c keep the best result the position allows (the win, the draw)?  How fast a win comes is not
    asked: AlphaZero's value, like the rules, only knows win, draw or loss."""
    return np.sign(scores_row[c]) == np.sign(np.nanmax(scores_row))


def compute_uct(sims_list=(10, 30, 100, 300, 1000, 3000), n_pos=400):
    t = load("testset")
    g = rng(11)
    hist = t["histories"][:n_pos]
    scores = np.asarray(t["scores"])[:n_pos]
    acc = []
    for sims in sims_list:
        ok = 0
        for h, sc in zip(hist, scores):
            b = c4.Board.from_moves(h)
            ok += is_right(sc, c4.uct_move(b, sims, g))
        acc.append(ok / len(hist))
    # a random legal move is right this often
    blind = float(np.mean([(np.sign(sc) == np.sign(np.nanmax(sc))).sum() / np.isfinite(sc).sum() for sc in scores]))
    return {"sims": list(sims_list), "acc": acc, "random": blind, "n_pos": len(hist)}


def compute_uct_tree(seq=(3, 3, 3, 2, 4), snaps=(10, 40, 160, 640, 2560)):
    """Plain MCTS from one position: the tree after more and more simulations (for drawing it grow)."""
    b = c4.Board.from_moves(seq)

    def dump(node, depth, min_n):
        d = {"N": int(node.N), "W": float(node.W), "move": node.move, "children": []}
        if depth:
            for ch in sorted(node.children, key=lambda c: c.move):
                if ch.N >= min_n:
                    d["children"].append(dump(ch, depth - 1, min_n))
        return d

    out = {"seq": list(seq), "snaps": list(snaps), "trees": []}
    for n in snaps:
        root = c4.uct_search(b, n, rng(4))
        out["trees"].append(dump(root, 3, max(1, n // 200)))
    S = c4.Solver(24)
    out["truth"] = S.move_scores(b.pos, b.mask, b.moves)
    return out


# ---------------------------------------------------------------------------
# AlphaZero (trained by alphazero.py)
# ---------------------------------------------------------------------------
def _gens():
    from videos.ai.ai26.alphazero import GENS, OUT, ensure_trained

    ensure_trained()
    return sorted(g for g in (int(p.stem.split("_")[1]) for p in OUT.glob("gen_*.pt")) if g <= GENS)


def _save_json(path, obj) -> None:
    import json

    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(obj))
    tmp.replace(path)


def _grade_gen(gnum: int, n_pos: int) -> dict:
    """One generation graded on the test positions: the network's own choice, its choice after search, its value.
    Kept on its own (``az/grade/``), so the grading resumes generation by generation."""
    import json

    import torch

    from videos.ai.ai26.alphazero import OUT, SIMS, Evaluator, Node, load_gen, search

    f = OUT / "grade" / f"gen_{gnum:03d}_{n_pos}.json"
    if f.exists():
        return json.loads(f.read_text())
    torch.set_num_threads(1)
    t = load("testset")
    scores = np.asarray(t["scores"])[:n_pos]
    value = np.asarray(t["value"])[:n_pos]
    boards = [c4.Board.from_moves(h) for h in t["histories"][:n_pos]]
    ev = Evaluator(load_gen(gnum))
    pri, v = ev(boards)
    roots = [Node(b) for b in boards]
    search(roots, ev, SIMS, rng(gnum), noise=False)
    out = {"raw": float(np.mean([is_right(sc, int(np.argmax(p))) for sc, p in zip(scores, pri)])),
           "value_acc": float(np.mean(np.sign(np.round(v * 1.5)) == value)),
           "mcts": float(np.mean([is_right(sc, int(np.argmax(r.N))) for sc, r in zip(scores, roots)]))}
    _save_json(f, out)
    return out


def _workers() -> int:
    import os

    return max(1, min(4, os.cpu_count() or 1))


def compute_az_grade(n_pos=400):
    import json
    from concurrent.futures import ProcessPoolExecutor

    from videos.ai.ai26.alphazero import GAMES_PER_GEN, OUT, SIMS

    gens = _gens()
    load("testset")  # computed here once, not by every worker
    with ProcessPoolExecutor(_workers()) as pool:
        res = list(pool.map(_grade_gen, gens, [n_pos] * len(gens)))
    log = json.loads((OUT / "log.json").read_text())
    return {"gens": gens, "raw": [r["raw"] for r in res], "mcts": [r["mcts"] for r in res],
            "value_acc": [r["value_acc"] for r in res], "sims": SIMS,
            "loss_policy": [e["loss_policy"] for e in log], "loss_value": [e["loss_value"] for e in log],
            "first_wins": [e["first_wins"] for e in log], "draws": [e["draws"] for e in log],
            "mean_length": [e["mean_length"] for e in log], "games_per_gen": GAMES_PER_GEN,
            "hours": float(sum(e["selfplay_s"] + e["train_s"] for e in log) / 3600)}


def _play_pair(a, b, games, sims) -> list:
    """``games`` games between players ``a`` and ``b`` ((name, ("az", gen) | ("uct", sims))), alternating who moves
    first: [a's points, games].  Seeded by the two names, so the result doesn't depend on how the round robin is
    split across processes; kept on its own (``az/elo/``), so the tournament resumes pairing by pairing."""
    import json
    import re
    import zlib

    import torch

    from videos.ai.ai26.alphazero import OUT, Evaluator, Node, load_gen, search

    tag = re.sub(r"\W+", "_", f"{a[0]}__{b[0]}")
    f = OUT / "elo" / f"{tag}_{games}_{sims}.json"
    if f.exists():
        return json.loads(f.read_text())
    torch.set_num_threads(1)
    g = rng(zlib.crc32(f"{a[0]}|{b[0]}".encode()))
    evs = {name: Evaluator(load_gen(kind[1])) for name, kind in (a, b) if kind[0] == "az"}
    pts = 0.0
    for k in range(games):
        first, second = (a, b) if k % 2 == 0 else (b, a)
        bd = c4.Board()
        for _ in range(2):  # two random opening moves, so the games differ
            bd = bd.play(int(g.integers(7)))
        turn = [first, second]
        result = 0.5  # for the first player
        while True:
            name, kind = turn[bd.moves % 2]
            if kind[0] == "az":
                root = Node(bd)
                search([root], evs[name], sims, g, noise=False)
                c = int(np.argmax(root.N))
            else:
                c = c4.uct_move(bd, kind[1], g)
            bd = bd.play(c)
            if c4.last_mover_won(bd):
                result = 1.0 if name == first[0] else 0.0
                break
            if bd.full():
                break
        pts += result if first is a else 1 - result
    out = [pts, games]
    _save_json(f, out)
    return out


def compute_az_elo(games_per_pair=20):
    from concurrent.futures import ProcessPoolExecutor

    from videos.ai.ai26.alphazero import SIMS

    gens = _gens()
    pick = sorted(set([0, 1, 2, 3, 5, 8, 12, 16] + list(range(20, gens[-1] + 1, 10)) + [gens[-1]]))
    pick = [p for p in pick if p in gens]
    players = [(f"gen {p}", ("az", p)) for p in pick] + [("MCTS 200", ("uct", 200)), ("MCTS 1000", ("uct", 1000))]
    names = [p[0] for p in players]
    n = len(players)
    pairs = [(i, j) for i in range(n) for j in range(i + 1, n)]
    with ProcessPoolExecutor(_workers()) as pool:
        res = list(pool.map(_play_pair, [players[i] for i, _ in pairs], [players[j] for _, j in pairs],
                            [games_per_pair] * len(pairs), [SIMS] * len(pairs)))
    Wt, Nt = np.zeros((n, n)), np.zeros((n, n))
    for (i, j), (pts, games) in zip(pairs, res):
        Wt[i, j], Wt[j, i] = pts, games - pts
        Nt[i, j] = Nt[j, i] = games
    R = bradley_terry(Wt, Nt)
    R = R - R[names.index("gen 0")]  # the untrained network is 0
    return {"names": names, "elo": R, "wins": Wt, "games": Nt, "gens": pick, "sims": SIMS}


def bradley_terry(Wt, Nt, iters=2000):
    """Maximum-likelihood ratings: P(i beats j) = 1 / (1 + 10^((R_j - R_i) / 400)); mean rating 0."""
    n = len(Wt)
    R = np.zeros(n)
    for _ in range(iters):
        E = 1 / (1 + 10 ** ((R[None, :] - R[:, None]) / 400))
        grad = (Wt - Nt * E).sum(1)
        R += 40 * grad / np.maximum(Nt.sum(1), 1)
        R -= R.mean()
    return R


def compute_az_demo():
    from videos.ai.ai26.alphazero import SIMS, Evaluator, Node, load_gen, search

    gens = _gens()
    show = [g for g in (0, 1, 3, 10, gens[-1]) if g in gens]
    seq = [3, 3, 3, 3, 2, 4, 4, 2]  # a position with a real choice to make
    b = c4.Board.from_moves(seq)
    S = c4.Solver(24)
    truth = S.move_scores(b.pos, b.mask, b.moves)
    pri, val, visits = [], [], []
    for gnum in show:
        ev = Evaluator(load_gen(gnum))
        p, v = ev([b])
        root = Node(b)
        search([root], ev, SIMS, rng(0), noise=False)
        pri.append(p[0])
        val.append(float(v[0]))
        visits.append(root.N / root.N.sum())
    # the final network's search tree from this position, three levels deep (for drawing)
    ev = Evaluator(load_gen(gens[-1]))
    root = Node(b)
    search([root], ev, 400, rng(1), noise=False)

    def dump(node, depth):
        d = {"N": int(node.N.sum()), "P": node.P.tolist() if node.P is not None else None, "kids": {}}
        if depth:
            for a, ch in node.children.items():
                if node.N[a] >= 3:
                    d["kids"][str(a)] = {"n": int(node.N[a]), "q": float(node.Wsum[a] / max(node.N[a], 1)),
                                         "node": dump(ch, depth - 1)}
        return d

    tree = dump(root, 3)
    # every generation's first look at the position (the training, replayed), and the solver's verdicts
    prior_all, value_all = [], []
    for gnum in gens:
        p, v = Evaluator(load_gen(gnum))([b])
        prior_all.append(p[0])
        value_all.append(float(v[0]))
    # each of several generations plays a position out against itself, every move checked by the solver: the first
    # test position (in order, chosen by rule, not by result) where exactly one move keeps a win
    t = load("testset")
    start = next(list(h) for h, sc in zip(t["histories"], t["scores"])
                 if np.nanmax(sc) > 0 and int((np.sign(sc) == 1).sum()) == 1)
    games = {}
    for gnum in [x for x in (1, 3, 10, 30, gens[-1]) if x in gens]:
        evg = Evaluator(load_gen(gnum))
        gg = rng(100 + gnum)
        bb = c4.Board.from_moves(start)
        mv, ok = list(start), []
        while True:
            r_ = Node(bb)
            search([r_], evg, SIMS, gg, noise=False)
            cc = int(np.argmax(r_.N))
            if bb.moves >= 8:
                S.reset()
                ok.append(bool(is_right(S.move_scores(bb.pos, bb.mask, bb.moves), cc)))
            mv.append(cc)
            bb = bb.play(cc)
            if c4.last_mover_won(bb) or bb.full():
                break
        games[str(gnum)] = {"moves": mv, "perfect": ok, "won": bool(c4.last_mover_won(bb)), "length": len(mv)}
    # a self-play game by the final network, every move scored by the solver
    g = rng(5)
    gb = c4.Board()
    moves, perfect = [], []
    while True:
        root = Node(gb)
        search([root], ev, SIMS, g, noise=False)
        c = int(np.argmax(root.N))
        if gb.moves >= 8:
            S.reset()
            sc = S.move_scores(gb.pos, gb.mask, gb.moves)
            perfect.append(bool(is_right(sc, c)))
        moves.append(c)
        gb = gb.play(c)
        if c4.last_mover_won(gb) or gb.full():
            break
    winner = 0 if gb.full() and not c4.last_mover_won(gb) else (1 if gb.moves % 2 == 1 else 2)
    return {"seq": seq, "gens": show, "prior": np.array(pri), "value": val, "visits": np.array(visits),
            "all_gens": gens, "prior_all": np.array(prior_all), "value_all": np.array(value_all), "games": games,
            "game_start": start,
            "truth": truth, "tree": tree, "game": moves, "game_perfect": perfect, "game_winner": winner}


# ---------------------------------------------------------------------------
# Games of imperfect information
# ---------------------------------------------------------------------------
def compute_rps(T=3000):
    # payoff to the row player: rock, paper, scissors
    A = np.array([[0, -1, 1], [1, 0, -1], [-1, 1, 0]], float)
    reg = [np.array([0.0, 0.0, 0.0]), np.array([0.0, 0.0, 0.0])]
    start = [np.array([0.7, 0.2, 0.1]), np.array([0.2, 0.2, 0.6])]
    cur_hist, avg_hist = [], []
    s_sum = [np.zeros(3), np.zeros(3)]
    for t in range(T):
        strat = []
        for p in range(2):
            pos = np.maximum(reg[p], 0)
            strat.append(pos / pos.sum() if pos.sum() > 0 else start[p])
        u0 = A @ strat[1]  # value of each action for player 0
        u1 = -(A.T @ strat[0])  # for player 1 (zero-sum)
        reg[0] += u0 - strat[0] @ u0
        reg[1] += u1 - strat[1] @ u1
        for p in range(2):
            s_sum[p] += strat[p]
        cur_hist.append(strat[0])
        avg_hist.append(s_sum[0] / (t + 1))
    avg = np.array(avg_hist)
    assert np.abs(avg[-1] - 1 / 3).max() < 0.02
    return {"current": np.array(cur_hist), "average": avg}


KUHN_CARDS = (0, 1, 2)  # jack, queen, king


def kuhn_cfr(T=20000):
    """Vanilla CFR on Kuhn poker. Information sets: card + history ('', 'p', 'b', 'pb')."""
    regret, ssum = {}, {}

    def strategy(I):
        r = np.maximum(regret.setdefault(I, np.zeros(2)), 0)
        return r / r.sum() if r.sum() > 0 else np.array([0.5, 0.5])

    def payoff(h, cards):  # terminal utility for player 0
        if h in ("pp",):
            return 1 if cards[0] > cards[1] else -1
        if h in ("bb", "pbb"):
            return 2 if cards[0] > cards[1] else -2
        if h == "bp":
            return 1
        if h == "pbp":
            return -1
        return None

    def cfr(h, cards, p0, p1):
        u = payoff(h, cards)
        if u is not None:
            return u
        player = len(h) % 2
        I = (cards[player], h)
        s = strategy(I)
        util = np.zeros(2)
        for a, ch in enumerate("pb"):
            util[a] = cfr(h + ch, cards, p0 * s[a], p1) if player == 0 else cfr(h + ch, cards, p0, p1 * s[a])
        node = s @ util
        if player == 0:
            regret[I] = regret.setdefault(I, np.zeros(2)) + p1 * (util - node)
            ssum[I] = ssum.setdefault(I, np.zeros(2)) + p0 * s
        else:
            regret[I] = regret.setdefault(I, np.zeros(2)) + p0 * (node - util)  # player 1 minimizes player 0's utility
            ssum[I] = ssum.setdefault(I, np.zeros(2)) + p1 * s
        return node

    deals = [(a, b) for a in KUHN_CARDS for b in KUHN_CARDS if a != b]
    checkpoints, expl, values = [], [], []
    for t in range(1, T + 1):
        for d in deals:
            cfr("", d, 1.0, 1.0)
        if t in (1, 2, 3, 5, 10, 20, 30, 50, 100, 200, 300, 500, 1000, 2000, 3000, 5000, 10000, 20000):
            avg = {I: s / s.sum() for I, s in ssum.items()}
            checkpoints.append(t)
            e, v = kuhn_exploitability(avg)
            expl.append(e)
            values.append(v)
    return checkpoints, expl, values, {f"{'JQK'[I[0]]}{I[1] or '-'}": (s / s.sum()).tolist() for I, s in ssum.items()}


def kuhn_exploitability(avg):
    """How much a best response gains against the average strategy, averaged over the two seats; and the value."""
    deals = [(a, b) for a in KUHN_CARDS for b in KUHN_CARDS if a != b]

    def strat(I):
        return avg.get(I, np.array([0.5, 0.5]))

    def value(h, cards):
        terminal = {"pp": None, "bb": None, "pbb": None, "bp": 1, "pbp": -1}
        if h in terminal:
            if terminal[h] is not None:
                return terminal[h]
            stake = 1 if h == "pp" else 2
            return stake if cards[0] > cards[1] else -stake
        player = len(h) % 2
        s = strat((cards[player], h))
        return sum(s[a] * value(h + ch, cards) for a, ch in enumerate("pb"))

    game_value = np.mean([value("", d) for d in deals])

    def best_response(br_player):
        # enumerate the best responder's pure strategies over its 6 information sets (2^6 = 64)
        sets = [(c, h) for c in KUHN_CARDS for h in (["", "pb"] if br_player == 0 else ["p", "b"])]
        best = -np.inf
        for bits in range(2 ** len(sets)):
            pure = {I: np.eye(2)[(bits >> k) & 1] for k, I in enumerate(sets)}

            def val(h, cards):
                terminal = {"pp": None, "bb": None, "pbb": None, "bp": 1, "pbp": -1}
                if h in terminal:
                    if terminal[h] is not None:
                        return terminal[h]
                    stake = 1 if h == "pp" else 2
                    return stake if cards[0] > cards[1] else -stake
                player = len(h) % 2
                I = (cards[player], h)
                s = pure[I] if player == br_player else strat(I)
                return sum(s[a] * val(h + ch, cards) for a, ch in enumerate("pb"))

            u = np.mean([val("", d) for d in deals])
            best = max(best, u if br_player == 0 else -u)
        return best

    gain0 = best_response(0) - game_value
    gain1 = best_response(1) + game_value
    return float((gain0 + gain1) / 2), float(game_value)


def compute_kuhn():
    t, e, v, strat = kuhn_cfr()
    assert abs(v[-1] + 1 / 18) < 2e-3
    assert e[-1] < e[3] / 20
    return {"iters": t, "exploitability": e, "value": v, "strategy": strat}


# ---------------------------------------------------------------------------
# AlphaGo's games against Lee Sedol (Seoul, March 2016): the records, replayed with captures
# ---------------------------------------------------------------------------
SGF_URL = "https://homepages.cwi.nl/~aeb/go/games/games/AlphaGo/LeeSedol/{n}.sgf"


def go_replay(moves, upto):
    """Board after ``upto`` moves: 19 x 19, rows from the top; 1 black, -1 white. Captures removed."""
    B = np.zeros((19, 19), int)

    def group(r, c):
        col, seen, libs, stack = B[r, c], {(r, c)}, set(), [(r, c)]
        while stack:
            y, x = stack.pop()
            for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                yy, xx = y + dy, x + dx
                if 0 <= yy < 19 and 0 <= xx < 19:
                    if B[yy, xx] == 0:
                        libs.add((yy, xx))
                    elif B[yy, xx] == col and (yy, xx) not in seen:
                        seen.add((yy, xx))
                        stack.append((yy, xx))
        return seen, libs

    captured = 0
    for color, x, y in moves[:upto]:
        v = 1 if color == "B" else -1
        B[y, x] = v
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            yy, xx = y + dy, x + dx
            if 0 <= yy < 19 and 0 <= xx < 19 and B[yy, xx] == -v:
                st, libs = group(yy, xx)
                if not libs:
                    for a in st:
                        B[a] = 0
                    captured += len(st)
    return B, captured


def compute_go():
    import re
    import urllib.request

    out = {}
    for n, upto in ((2, 37), (4, 78)):
        raw = urllib.request.urlopen(SGF_URL.format(n=n), timeout=60).read().decode("utf-8", "replace")
        mv = [(c, ord(a) - 97, ord(b) - 97) for c, a, b in re.findall(r";([BW])\[([a-s])([a-s])\]", raw)]
        info = dict(re.findall(r"(PB|PW|DT|RE)\[([^\]]*)\]", raw))
        B, cap = go_replay(mv, upto)
        out[f"game{n}"] = {"board": B.tolist(), "move": list(mv[upto - 1][1:]), "color": mv[upto - 1][0],
                           "number": upto, "black": info.get("PB"), "white": info.get("PW"), "date": info.get("DT"),
                           "result": info.get("RE"), "moves_total": len(mv), "captured": cap}
    # the famous moves: game 2, Black (AlphaGo) at 'oj', a fifth-line shoulder hit; game 4, White (Lee Sedol) at L11 ('ki')
    assert out["game2"]["color"] == "B" and out["game2"]["black"] == "AlphaGo"
    assert out["game4"]["color"] == "W" and out["game4"]["white"] == "Lee Sedol"
    x = out["game2"]["move"][0]
    assert min(x, 18 - x) == 4  # the fifth line from the edge
    return out


ITEMS = {
    "bandit": compute_bandit,
    "grid": compute_grid,
    "walk": compute_walk,
    "cliff": compute_cliff,
    "maxbias": compute_maxbias,
    "dqn": compute_dqn,
    "dqn_div": compute_dqn_div,
    "pg": compute_pg,
    "pg_cloud": compute_pg_cloud,
    "alphabeta": compute_alphabeta,
    "testset": compute_testset,
    "uct": compute_uct,
    "uct_tree": compute_uct_tree,
    "rps": compute_rps,
    "kuhn": compute_kuhn,
    "go": compute_go,
    "az_grade": compute_az_grade,
    "az_elo": compute_az_elo,
    "az_demo": compute_az_demo,
}
CACHE.items = ITEMS


if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
