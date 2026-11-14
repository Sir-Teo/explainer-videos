"""Precompute every number in Part 17 of *Psychology, Built* ("Reward and Prediction").

    python -m videos.psychology.psych17.compute            # everything missing (about a minute)
    python -m videos.psychology.psych17.compute --force bandit

Results are cached in ``.cache/psych17/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.  The models are
Psyche's (``explainer.psychology.psyche.rl``); simulated studies are picked by rule (a fixed seed, or the median of
many runs), never by their result.

Items:
    schultz     three conditions of a TD learner turned into firing rates and spike rasters
    migration   the TD error over trials and time within a trial; second-order conditioning
    bandit      one simulated player of a reversal bandit, its fit, and parameter recovery over 40 players
    explore     regret of five exploration policies over 5,000 plays, averaged over 100 runs
    maze        the maze, and Tolman and Honzik's three groups on a model-based learner, with a model-free one
    twostep     stay probabilities for model-free, model-based and hybrid agents
    successor   reward and transition revaluation for three learners
    distrib     a reward distribution and a population of expectile learners
    redish      a cue's value for a natural reward and for a drug
    cases       the TD error on three trials: the first, a trained one, and a trained one with the juice omitted
    steinberg   Rescorla-Wagner's blocking, with and without an added error at the reward (Steinberg's design)
    abtest      a two-version test run by Thompson sampling: the share of visitors sent to the better version
    frank       Frank's probabilistic selection task on an opponent Go/NoGo learner, at three dopamine levels
"""

from __future__ import annotations

import numpy as np

from explainer.ai.cache import Cache
from explainer.psychology.psyche import rl

CACHE = Cache("psych17")
load = CACHE.load
DT = 0.1  # seconds per time step
CUE, REW = 5, 20


def compute_schultz() -> dict:
    D, _ = rl.td_conditioning(trials=150, cue=CUE, reward=REW, omit=(149,))
    rows = {"unpredicted": D[0], "predicted": D[140], "omitted": D[149]}
    rng = np.random.default_rng(17)
    out = {"t": (np.arange(30) - CUE) * DT}
    for name, d in rows.items():
        rate = np.clip(5.0 + 30.0 * d, 0.0, None)  # spikes per second; a baseline of 5
        out[f"rate_{name}"] = rate
        spikes = []
        for k in range(10):  # ten trials, Poisson spikes in 10 ms bins
            fine = np.repeat(rate, 10) * 0.01
            hits = np.nonzero(rng.random(fine.size) < fine)[0]
            spikes.append((hits * 0.01 - CUE * DT).tolist())
        out[f"spikes_{name}"] = spikes
    return out


def compute_migration() -> dict:
    D, V = rl.td_conditioning(trials=120, cue=CUE, reward=REW)
    return {"delta": D, "V_last": V[-1], "t": (np.arange(30) - CUE) * DT, "second": rl.second_order()}


def compute_bandit() -> dict:
    P = np.r_[np.tile([0.8, 0.2], (100, 1)), np.tile([0.2, 0.8], (100, 1))]
    C, R, Q = rl.q_learning_bandit(P, trials=200, alpha=0.3, beta=5.0, rng=np.random.default_rng(5))
    a, b, ll = rl.fit_bandit(C, R)
    ws, ls = rl.win_stay_lose_shift(C, R)
    rng = np.random.default_rng(23)
    true_a, true_b, fit_a, fit_b = [], [], [], []
    for k in range(40):
        ta, tb = rng.uniform(0.1, 0.8), rng.uniform(2.0, 10.0)
        c, r, _ = rl.q_learning_bandit(P, trials=200, alpha=ta, beta=tb, rng=np.random.default_rng(1000 + k))
        fa, fb, _ = rl.fit_bandit(c, r)
        true_a.append(ta), true_b.append(tb), fit_a.append(fa), fit_b.append(fb)
    true_a, fit_a = np.array(true_a), np.array(fit_a)
    return {"choices": C, "rewards": R, "Q": Q, "fit_alpha": a, "fit_beta": b, "win_stay": ws, "lose_shift": ls,
            "true_a": true_a, "true_b": np.array(true_b), "fit_a": fit_a, "fit_b": np.array(fit_b),
            "r_alpha": float(np.corrcoef(true_a, fit_a)[0, 1]), "r_beta": float(np.corrcoef(true_b, fit_b)[0, 1])}


POLICIES = ("greedy", "epsilon", "softmax", "ucb", "thompson")


def compute_explore() -> dict:
    out = {}
    for p in POLICIES:
        out[p] = np.mean([rl.explore_regret(p, trials=5000, rng=np.random.default_rng(s)) for s in range(100)],
                         axis=0)
    return out


def compute_maze() -> dict:
    cells, start, goal, nbrs = rl.maze_graph()
    out = {"maze": "\n".join(rl.MAZE), "floor": rl.latent_learning()[1]}
    for name, frm, agent in (("always", 0, "model"), ("never", 99, "model"), ("delayed", 10, "model"),
                             ("delayed_free", 10, "free")):
        runs = np.array([rl.latent_learning(reward_from=frm, agent=agent, rng=np.random.default_rng(s))[0]
                         for s in range(40)])
        out[name] = np.median(runs, axis=0)
    return out


def compute_twostep() -> dict:
    out = {}
    for name, w in (("model_free", 0.0), ("model_based", 1.0), ("hybrid", 0.5)):
        sp = np.mean([list(rl.stay_probabilities(rl.two_step(w, rng=np.random.default_rng(s))).values())
                      for s in range(30)], axis=0)
        out[name] = sp
    return out


def compute_successor() -> dict:
    out = {}
    for kind in ("reward", "transition"):
        r = rl.revaluation(kind)
        for learner, (v1, v2) in r.items():
            out[f"{kind}_{learner}"] = np.array([v1, v2])
    return out


def compute_distrib() -> dict:
    r = np.r_[np.full(300, 0.1), np.full(200, 0.3), np.full(150, 1.2), np.full(150, 2.5), np.full(100, 5.0),
              np.full(100, 10.0)]
    taus = np.linspace(0.05, 0.95, 13)
    v = rl.distributional_td(r, taus, lr=0.02, epochs=40, rng=np.random.default_rng(3))
    return {"rewards": np.array([0.1, 0.3, 1.2, 2.5, 5.0, 10.0]), "probs": np.array([0.3, 0.2, 0.15, 0.15, 0.1, 0.1]),
            "taus": taus, "values": v, "mean": float(r.mean())}


def compute_redish() -> dict:
    return {"natural": rl.redish(trials=200), "drug": rl.redish(trials=200, drug=0.5)}


def compute_cases() -> dict:
    D, _ = rl.td_conditioning(trials=150, cue=CUE, reward=REW, omit=(149,))
    return {"t": (np.arange(30) - CUE) * DT, "first": D[0], "trained": D[140], "omitted": D[149]}


def compute_steinberg() -> dict:
    """Rescorla-Wagner on Steinberg et al.'s groups: A then US (pretraining), then AX then US.  Light at the reward
    adds ``stim`` to the error on compound trials; light at another time arrives with no cue, so it changes nothing
    that X could learn.  A group without pretraining shows normal learning of X."""
    alpha, lam, stim = 0.2, 1.0, 0.5

    def run(pre: bool, extra: float) -> float:
        va = vx = 0.0
        if pre:
            for _ in range(100):
                va += alpha * (lam - va)
        for _ in range(40):
            d = lam + extra - va - vx
            va += alpha * d
            vx += alpha * d
        return vx

    return {"groups": ["no pretraining", "blocking", "blocking, light at the reward",
                       "blocking, light at another time"],
            "vx": [run(False, 0.0), run(True, 0.0), run(True, stim), run(True, 0.0)], "stim": stim}


def opal_subject(rho: float, rng, beta: float = 2.0, a_c: float = 0.1, a_g: float = 0.3, trials: int = 360):
    """One subject of the probabilistic selection task on an opponent actor learner (after Collins and Frank's
    OpAL, 2014).  A critic learns each symbol's value V; the Go and NoGo weights of the chosen symbol learn from the
    critic's error, G += a_g G delta and N += a_g N (-delta).  Choice is a softmax of beta_G G - beta_N N, with
    beta_G = beta (1 + rho) and beta_N = beta (1 - rho): rho > 0 is more dopamine (Go dominates), rho < 0 less.
    The critic starts at 0.5, the average payoff.  This learner reproduces the direction of Frank et al.'s
    interaction (less dopamine favours avoiding B, more favours choosing A), not its size."""
    p = np.array([0.8, 0.2, 0.7, 0.3, 0.6, 0.4])  # A B C D E F
    pairs = [(0, 1), (2, 3), (4, 5)]
    V, G, N = np.full(6, 0.5), np.ones(6), np.ones(6)
    bg, bn = beta * (1 + rho), beta * (1 - rho)
    for k in range(trials):
        i, j = pairs[k % 3] if rng.random() < 0.5 else pairs[k % 3][::-1]
        act = bg * G[[i, j]] - bn * N[[i, j]]
        pi = 1.0 / (1.0 + np.exp(act[1] - act[0]))
        c = i if rng.random() < pi else j
        r = 1.0 if rng.random() < p[c] else 0.0
        d = r - V[c]
        V[c] += a_c * d
        G[c] = max(G[c] + a_g * G[c] * d, 0.0)
        N[c] = max(N[c] + a_g * N[c] * (-d), 0.0)
    act = bg * G - bn * N
    others = [2, 3, 4, 5]
    choose_a = np.mean([1.0 / (1.0 + np.exp(act[o] - act[0])) for o in others])
    avoid_b = np.mean([1.0 / (1.0 + np.exp(act[1] - act[o])) for o in others])
    return choose_a, avoid_b


def compute_frank() -> dict:
    rng = np.random.default_rng(2004)
    out = {"levels": ["off medication", "healthy", "on medication"], "rho": [-0.5, 0.0, 0.5]}
    ca, ab = [], []
    for rho in out["rho"]:
        res = np.array([opal_subject(rho, rng) for _ in range(300)])
        ca.append(float(res[:, 0].mean()))
        ab.append(float(res[:, 1].mean()))
    out["choose_a"], out["avoid_b"] = ca, ab
    return out


def compute_abtest() -> dict:
    """Two page versions with click rates of 5% and 6%; 20,000 visitors; Thompson sampling against an even split.
    The share of each block of 1,000 visitors shown the better version, averaged over 50 runs, and the clicks each
    design collected."""
    p = np.array([0.05, 0.06])
    n_vis, block, runs = 20000, 1000, 50
    shares, clicks_ts = [], []
    for run in range(runs):
        rng = np.random.default_rng(run)
        a, b = np.ones(2), np.ones(2)
        chose = np.zeros(n_vis, int)
        got = 0
        for t in range(n_vis):
            k = int(np.argmax(rng.beta(a, b)))
            r = rng.random() < p[k]
            a[k] += r
            b[k] += 1 - r
            chose[t] = k
            got += r
        shares.append(chose.reshape(-1, block).mean(axis=1))
        clicks_ts.append(got)
    return {"share": np.mean(shares, axis=0), "block": block, "clicks_thompson": float(np.mean(clicks_ts)),
            "clicks_even": float(n_vis * p.mean()), "clicks_best": float(n_vis * p.max())}


ITEMS = {
    "schultz": compute_schultz,
    "migration": compute_migration,
    "bandit": compute_bandit,
    "explore": compute_explore,
    "maze": compute_maze,
    "twostep": compute_twostep,
    "successor": compute_successor,
    "distrib": compute_distrib,
    "redish": compute_redish,
    "cases": compute_cases,
    "steinberg": compute_steinberg,
    "frank": compute_frank,
    "abtest": compute_abtest,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
