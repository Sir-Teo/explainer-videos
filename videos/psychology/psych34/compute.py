"""Precompute every number in Part 34 of *Psychology, Built* ("Social Influence").

    python -m videos.psychology.psych34.compute            # everything missing (under a minute)
    python -m videos.psychology.psych34.compute --force market

Results are cached in ``.cache/psych34/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.  Models are Psyche's
(``explainer.psychology.psyche.social``).  Published numbers are quoted in the scenes with their sources.
Simulations use fixed seeds.

Items:
    sherif      three people judging how far a still light moves: four sessions alone, four together (each moves
                toward the group's mean), then four alone again; an illustration of Sherif's design, not his data
    riot        Granovetter's two crowds of 100: thresholds 0..99, and the same with one threshold moved; the
                cascade size as the spread of a normal threshold distribution grows
    degroot     five people's trust matrix, their opinions over time, the consensus and each person's weight
    camps       bounded-confidence paths for three values of eps, and the number of camps over eps
    contagion   a ring of 60 drawn as a circle and its rewired twin; simple and complex contagion on rings of 400,
                adopters by step, and the complex contagion's reach as the rewired fraction grows
    crowd       a guessing crowd before and after rounds of influence: collective error, individual error and
                diversity by round; where the truth sits in the range
    market      a cumulative-advantage market: independent and social worlds, shares by quality, Gini and
                unpredictability over the strength of social information
    bystanders  the chance anyone helps as the crowd grows, for three strengths of diffusion
    twins       two worlds of friend pairs with the same correlation in behaviour: in one, a friend's adoption
                causes yours (contagion); in the other, friends share a hidden trait that causes both (homophily)
    impact      Latane's psychosocial law; Zajonc's drive on an easy and a hard task; Stasser and Titus's sampling
"""

from __future__ import annotations

import numpy as np

from explainer.ai.cache import Cache
from explainer.psychology.psyche import social as S

CACHE = Cache("psych34")
load = CACHE.load


def compute_sherif() -> dict:
    rng = np.random.default_rng(1935)
    own = np.array([1.5, 4.0, 7.5])  # each person's private norm, inches
    rows = []
    x = own.copy()
    for k in range(4):  # alone: each settles on their own range
        rows.append(own + rng.normal(0, 0.35, 3))
    for k in range(4):  # together: each moves toward the group's mean
        x = 0.55 * x + 0.45 * x.mean()
        rows.append(x + rng.normal(0, 0.2, 3))
    for k in range(4):  # alone again: the group's norm persists
        rows.append(x + rng.normal(0, 0.25, 3))
    return {"est": np.array(rows), "phase": np.repeat([0, 1, 2], 4)}


def compute_riot() -> dict:
    t = np.arange(100)
    t2 = t.copy()
    t2[1] = 2
    a, b = S.cascade(t), S.cascade(t2)
    c = S.cascade_curve(n=100, mean=25, sds=np.linspace(1, 30, 117))
    jump = float(c["sd"][np.argmax(c["size"] >= 50)])
    return {"path_a": a, "path_b": b, "size_a": int(a[-1]), "size_b": int(b[-1]), "sd": c["sd"], "size": c["size"],
            "jump": jump}


def compute_degroot() -> dict:
    W = np.array([[0.6, 0.2, 0.2, 0.0, 0.0],
                  [0.3, 0.4, 0.3, 0.0, 0.0],
                  [0.1, 0.1, 0.5, 0.2, 0.1],
                  [0.0, 0.0, 0.3, 0.5, 0.2],
                  [0.0, 0.0, 0.1, 0.4, 0.5]])
    x0 = np.array([0.1, 0.3, 0.5, 0.8, 0.95])
    path = S.degroot(W, x0, steps=30)
    wts = S.influence_weights(W)
    return {"W": W, "x0": x0, "path": path, "weights": wts, "consensus": float(wts @ x0),
            "plain_mean": float(x0.mean())}


def compute_camps() -> dict:
    rng = np.random.default_rng(34)
    x0 = np.sort(rng.random(60))
    out = {"x0": x0}
    for e in (0.05, 0.12, 0.3):
        p = S.bounded_confidence(x0, e, 20)
        out[f"path_{int(e * 100)}"] = p
        out[f"camps_{int(e * 100)}"] = S.clusters(p[-1], 1e-2)
    eps = np.linspace(0.02, 0.4, 39)
    grid = np.linspace(0, 1, 201)
    out["eps"] = eps
    out["camps"] = np.array([S.clusters(S.bounded_confidence(grid, e, 120)[-1], 1e-2) for e in eps])
    return out


def compute_contagion() -> dict:
    small = S.ring_lattice(60, 2)
    small_r = S.rewire(small, 1.0, seed=34)
    out = {"edges_l": [(i, j) for i, a in enumerate(small) for j in a if i < j],
           "edges_r": [(i, j) for i, a in enumerate(small_r) for j in a if i < j]}
    for name, adj in (("l", small), ("r", small_r)):
        for need in (1, 2):
            on = np.zeros(60, int) - 1
            seeds = [0, 1, 2, 3]
            on[seeds] = 0
            state = np.zeros(60, bool)
            state[seeds] = True
            for step in range(1, 60):
                cnt = np.array([state[a].sum() for a in adj])
                new = state | (cnt >= need)
                on[new & ~state] = step
                if new.sum() == state.sum():
                    break
                state = new
            out[f"when_{name}{need}"] = on
    big = S.ring_lattice(400, 2)
    for need in (1, 2):
        out[f"path_l{need}"] = S.contagion(big, [0, 1, 2, 3], need)
        out[f"path_r{need}"] = S.contagion(S.rewire(big, 1.0, seed=35), [0, 1, 2, 3], need)
    qs = np.array([0, 0.01, 0.02, 0.05, 0.1, 0.2, 0.3, 0.5, 0.75, 1.0])
    reach = []
    for q in qs:
        r = [S.contagion(S.rewire(big, q, seed=100 + s), [0, 1, 2, 3], 2)[-1] / 400 for s in range(8)]
        reach.append(float(np.mean(r)))
    out["q"], out["reach"] = qs, np.array(reach)
    return out


def compute_crowd() -> dict:
    r = S.influence_rounds(n=144, truth=1.0, bias=0.3, sd=0.8, w=0.4, rounds=5, seed=34)
    rng = np.random.default_rng(34)
    x0 = rng.normal(0.3, 0.8, 144)
    xs = [x0]
    for _ in range(5):
        xs.append(0.6 * xs[-1] + 0.4 * xs[-1].mean())
    return {**r, "x": np.array(xs), "identity": S.crowd(x0, 0.0)}


def compute_market() -> dict:
    rng = np.random.default_rng(34)
    q = np.sort(rng.beta(2, 5, 48))
    ind = S.music_market(listeners=2700, worlds=8, social=0.0, seed=34, quality=q)
    soc = S.music_market(listeners=2700, worlds=8, social=0.8, seed=34, quality=q)
    levels = np.array([0.0, 0.2, 0.4, 0.6, 0.8, 0.9])
    g, u = [], []
    for s in levels:
        m = S.music_market(listeners=2700, worlds=8, social=float(s), seed=35, quality=q)
        g.append(m["gini"].mean())
        u.append(m["unpredictability"])
    best = int(np.argmax(q))
    return {"quality": q, "ind": ind["shares"], "soc": soc["shares"], "gini_ind": ind["gini"], "gini_soc": soc["gini"],
            "u_ind": ind["unpredictability"], "u_soc": soc["unpredictability"], "levels": levels, "gini": np.array(g),
            "unpredictability": np.array(u), "best_rank_soc": [int(np.sum(s > s[best])) + 1 for s in soc["shares"]],
            "best_rank_ind": [int(np.sum(s > s[best])) + 1 for s in ind["shares"]]}


def compute_bystanders() -> dict:
    N = np.arange(1, 21)
    return {"N": N, **{f"any_{int(b * 10)}": S.bystanders(N, 0.85, b)["any"] for b in (0.5, 1.0, 1.5)},
            **{f"each_{int(b * 10)}": S.bystanders(N, 0.85, b)["each"] for b in (0.5, 1.0, 1.5)}}


def compute_twins() -> dict:
    rng = np.random.default_rng(2011)
    n = 4000
    # contagion: A adopts on its own; B adopts with a boost if A did
    a1 = rng.random(n) < 0.3
    b1 = rng.random(n) < np.where(a1, 0.55, 0.193)
    # homophily: a shared hidden trait h drives both, no influence at all
    h = rng.random(n) < 0.5
    pa = np.where(h, 0.57, 0.03)
    a2, b2 = rng.random(n) < pa, rng.random(n) < pa
    r1, r2 = np.corrcoef(a1, b1)[0, 1], np.corrcoef(a2, b2)[0, 1]
    return {"r_contagion": float(r1), "r_homophily": float(r2), "p_contagion": [float(b1[a1].mean()), float(b1[~a1].mean())],
            "p_homophily": [float(b2[a2].mean()), float(b2[~a2].mean())]}


def compute_impact() -> dict:
    N = np.arange(0, 16)
    D = np.linspace(0.5, 3, 26)
    return {"N": N, "impact": S.social_impact(N, 1.0, 0.5), "D": D, "easy": S.drive(1.0, 0.0, D),
            "hard": S.drive(-0.6, 0.0, D), "k": np.arange(1, 6), "mention": S.mentions(0.3, np.arange(1, 6))}


ITEMS = {"sherif": compute_sherif, "riot": compute_riot, "degroot": compute_degroot, "camps": compute_camps, "contagion": compute_contagion,
         "crowd": compute_crowd, "market": compute_market, "bystanders": compute_bystanders, "twins": compute_twins, "impact": compute_impact}


if __name__ == "__main__":
    CACHE.main(ITEMS)
