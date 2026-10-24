"""Discovery by search (Part 25, chapters 15-17): a GNoME-style active-learning flywheel on a synthetic chemistry,
with convex hulls; rank searches for matrix-multiplication algorithms (the tensor decompositions AlphaTensor and
AlphaEvolve searched); and an evolutionary search over heuristics for online bin packing, FunSearch's problem, with
random mutations standing in for the language model.  numpy and torch; seeded.
"""

from __future__ import annotations

import math
import time

import numpy as np
import torch
import torch.nn as nn

# ===========================================================================
# Materials: a synthetic chemistry, hulls, and the flywheel
# ===========================================================================
N_ELEM = 20
COMPS = (0.2, 0.25, 1 / 3, 0.4, 0.5, 0.6, 2 / 3, 0.75, 0.8)
N_PROTO = 4


def chemistry(seed=0):
    """Twenty made-up elements, each with three hidden traits (a stand-in for electronegativity, size and valence),
    and every binary compound A_x B_(1-x) at nine compositions in four structure types.  The 'DFT' energy is a hidden
    function of the traits plus an irregular part no model of the traits can predict.  Returns the candidates'
    features and their true formation energies (per atom, made-up units)."""
    rng = np.random.default_rng(seed)
    T = rng.normal(0, 1, (N_ELEM, 3))
    w_proto = rng.normal(0, 1, (N_PROTO, 4))
    rows, feats, E = [], [], []
    for a in range(N_ELEM):
        for b in range(a + 1, N_ELEM):
            for x in COMPS:
                for p in range(N_PROTO):
                    ta, tb = T[a], T[b]
                    mix = x * (1 - x)
                    chi = (ta[0] - tb[0]) ** 2
                    size = (ta[1] - tb[1]) ** 2
                    val = (x * ta[2] - (1 - x) * tb[2]) ** 2
                    pref = abs(x - (0.5 + 0.25 * math.tanh(w_proto[p, 3])))
                    e = mix * (-1.1 * chi + (0.35 + 0.25 * math.tanh(w_proto[p, 0])) * size) + 0.15 * val \
                        + 0.12 * w_proto[p, 1] * mix + 0.6 * mix * pref
                    e += 0.05 * rng.normal()  # what the traits can't explain
                    rows.append((a, b, x, p))
                    dt = ta - tb  # the surrogate reads the two elements' traits, their differences, and the mix
                    f = np.concatenate([ta, tb, [x, x * (1 - x)], np.eye(N_PROTO)[p], dt, dt ** 2, mix * dt ** 2])
                    feats.append(f)
                    E.append(e)
    return np.array(rows), np.array(feats, np.float32), np.array(E)


def lower_hull(points):
    """The lower convex hull of points (x, E) in the plane, x sorted (Andrew's monotone chain)."""
    pts = sorted(set((float(x), float(e)) for x, e in points))
    hull = []
    for p in pts:
        while len(hull) >= 2:
            (x1, y1), (x2, y2) = hull[-2], hull[-1]
            if (x2 - x1) * (p[1] - y1) - (y2 - y1) * (p[0] - x1) <= 0:
                hull.pop()
            else:
                break
        hull.append(p)
    return np.array(hull)


def e_above_hull(x, e, hull) -> float:
    return float(e - np.interp(x, hull[:, 0], hull[:, 1]))


def systems_of(rows):
    out = {}
    for i, (a, b, _, _) in enumerate(rows):
        out.setdefault((int(a), int(b)), []).append(i)
    return out


def true_stable(rows, E, tol=1e-9):
    """Candidates on the lower hull of their binary system (with the pure elements at 0): the truly stable ones."""
    st = np.zeros(len(rows), bool)
    for key, idx in systems_of(rows).items():
        pts = [(0.0, 0.0), (1.0, 0.0)] + [(rows[i, 2], E[i]) for i in idx]
        h = lower_hull(pts)
        for i in idx:
            st[i] = e_above_hull(rows[i, 2], E[i], h) <= tol and E[i] < 0
    return st


class Surrogate(nn.Module):
    def __init__(self, d, hidden=128):
        super().__init__()
        self.net = nn.Sequential(nn.Linear(d, hidden), nn.SiLU(), nn.Linear(hidden, hidden), nn.SiLU(),
                                 nn.Linear(hidden, 1))

    def forward(self, x):
        return self.net(x).squeeze(-1)


def fit_surrogates(X, y, seed, k=4, steps=2000):
    """An ensemble of ``k`` small networks (GNoME uses an ensemble of graph networks; ours read the traits); a cosine
    learning-rate schedule, so the last step is not a random moment."""
    models = []
    Xt, yt = torch.from_numpy(X), torch.from_numpy(y.astype(np.float32))
    for j in range(k):
        torch.manual_seed(seed * 100 + j)
        gen = torch.Generator().manual_seed(seed * 100 + j)
        m = Surrogate(X.shape[1])
        opt = torch.optim.Adam(m.parameters(), 3e-3, weight_decay=1e-4)
        sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, steps)
        for _ in range(steps):
            idx = torch.randint(0, len(Xt), (min(128, len(Xt)),), generator=gen)
            loss = ((m(Xt[idx]) - yt[idx]) ** 2).mean()
            opt.zero_grad()
            loss.backward()
            opt.step()
            sched.step()
        models.append(m.eval())
    return models


def predict(models, X):
    with torch.no_grad():
        return np.mean([m(torch.from_numpy(X)).numpy() for m in models], 0)


def decomposition_energy(xs, es, k):
    """How far point k lies above (positive) or below (negative) the lower hull of all the other points of its
    system and the two pure elements: GNoME's decomposition energy, the quantity a pick is ranked by."""
    others = [(0.0, 0.0), (1.0, 0.0)] + [(xs[j], es[j]) for j in range(len(xs)) if j != k]
    return e_above_hull(xs[k], es[k], lower_hull(others))


def flywheel(rows, X, E, seed, rounds=8, per_round=60, start=0.03, policy="model"):
    """Active learning: start from a random ``start`` share of candidates 'known' (computed), then each round train
    the surrogates on everything known, predict every unknown candidate's energy, rank each by its decomposition
    energy against everything else in its system (true energies where known, predicted ones elsewhere), 'compute'
    (look up the true energy of) the ``per_round`` most promising, and add them.  ``policy='random'`` picks at random
    instead.  A hit is a pick that is truly stable (on the hull of the full chemistry); also recorded: the surrogate's
    error on the unknown candidates, and how many of the truly stable ones are known."""
    rng = np.random.default_rng(10 + seed)
    stable = true_stable(rows, E)
    known = np.zeros(len(rows), bool)
    known[rng.choice(len(rows), int(start * len(rows)), replace=False)] = True
    sys = systems_of(rows)
    hist = []
    for r in range(rounds):
        models = fit_surrogates(X[known], E[known], seed * 1000 + r)
        pred = predict(models, X)
        mae = float(np.abs(pred[~known] - E[~known]).mean())
        cand = np.flatnonzero(~known)
        if policy == "random":
            pick = rng.choice(cand, per_round, replace=False)
        else:
            est = np.where(known, E, pred)
            score = np.full(len(rows), np.inf)
            for idx in sys.values():
                xs, es = [rows[i, 2] for i in idx], [est[i] for i in idx]
                for k, i in enumerate(idx):
                    if not known[i]:
                        score[i] = decomposition_energy(xs, es, k)
            pick = cand[np.argsort(score[cand], kind="stable")[:per_round]]
        hits = int(stable[pick].sum())
        known[pick] = True
        hist.append(dict(round=r, hit_rate=hits / per_round, hits=hits, mae=mae,
                         found=int((stable & known).sum()), known=int(known.sum())))
    return hist, stable


# ===========================================================================
# Matrix multiplication as a tensor: searching for low-rank decompositions
# ===========================================================================
def matmul_tensor(n: int) -> np.ndarray:
    """T[(i,j), (j,k), (k,i)] = 1: C^T = A B written as a trilinear form; a rank-R decomposition T = sum_r u_r x v_r x
    w_r is an algorithm with R multiplications (Strassen 1969: R = 7 for n = 2)."""
    T = np.zeros((n * n, n * n, n * n))
    for i in range(n):
        for j in range(n):
            for k in range(n):
                T[i * n + j, j * n + k, k * n + i] = 1
    return T


def cp_als(T, R, rng, iters=3000, lam0=1e-2):
    """Alternating least squares with a vanishing ridge (Smirnov 2013): from random factors, solve for U, V, W in turn;
    the ridge keeps the factors from blowing up early and fades away.  Returns the relative residual and factors."""
    I, J, K = T.shape
    U, V, W = (rng.normal(0, 0.5, (d, R)) for d in (I, J, K))
    T1 = T.reshape(I, -1)
    T2 = np.transpose(T, (1, 0, 2)).reshape(J, -1)
    T3 = np.transpose(T, (2, 0, 1)).reshape(K, -1)
    nT = np.linalg.norm(T)

    def kr(A, B):
        return np.einsum("ir,jr->ijr", A, B).reshape(-1, A.shape[1])

    res = 1.0
    for it in range(iters):
        lam = lam0 * (1 - it / iters) ** 2 + 1e-9
        G = kr(V, W)
        U = T1 @ G @ np.linalg.inv(G.T @ G + lam * np.eye(R))
        G = kr(U, W)
        V = T2 @ G @ np.linalg.inv(G.T @ G + lam * np.eye(R))
        G = kr(U, V)
        W = T3 @ G @ np.linalg.inv(G.T @ G + lam * np.eye(R))
        if it % 50 == 0 or it == iters - 1:
            res = np.linalg.norm(T - np.einsum("ir,jr,kr->ijk", U, V, W)) / nT
            if res < 1e-10:
                break
    return float(res), (U, V, W)


def verify_algorithm(U, V, W, n, rng, trials=20) -> float:
    """Multiply random matrices with the decomposition (R products of linear combinations) and compare with A @ B."""
    worst = 0.0
    for _ in range(trials):
        A, B = rng.normal(size=(n, n)), rng.normal(size=(n, n))
        a, b = A.reshape(-1), B.reshape(-1)
        m = (U.T @ a) * (V.T @ b)  # the R multiplications
        Ct = (W @ m).reshape(n, n)  # C^T, entry (k, i)
        worst = max(worst, float(np.abs(Ct.T - A @ B).max()))
    return worst


# ===========================================================================
# Online bin packing: evolving a priority function
# ===========================================================================
CAP = 100


def weibull_instance(rng, n_items):
    """Item sizes from a Weibull distribution (shape 3, scale 45), rounded and clipped to 1..100, bin capacity 100:
    the Weibull benchmark FunSearch used (Castineiras et al. 2012)."""
    return np.clip(np.round(rng.weibull(3.0, n_items) * 45), 1, CAP).astype(float)


def pack(items, priority) -> int:
    """Each item goes to the open bin with the highest ``priority(item, remaining)`` among those it fits in, or a new
    bin.  Returns the number of bins used."""
    rem = np.zeros(0)
    for s in items:
        fit = np.flatnonzero(rem >= s)
        if len(fit):
            p = priority(s, rem[fit])
            j = fit[int(np.argmax(p))]
            rem[j] -= s
        else:
            rem = np.append(rem, CAP - s)
    return len(rem)


def first_fit(s, r):
    return -np.arange(len(r), dtype=float)


def best_fit(s, r):
    return -(r - s)


def excess(items_list, priority) -> float:
    """Average excess over the lower bound ceil(sum / capacity), in percent."""
    out = []
    for items in items_list:
        lb = math.ceil(items.sum() / CAP)
        out.append(100.0 * (pack(items, priority) - lb) / lb)
    return float(np.mean(out))


# expression trees: ("op", child, ...) or terminal names / constants
UNARY = {"neg": "(-{0})", "sq": "({0})**2", "inv": "(1.0/(np.abs({0})+1.0))", "log": "np.log(np.abs({0})+1.0)"}
BINARY = {"add": "({0}+{1})", "sub": "({0}-{1})", "mul": "({0}*{1})", "div": "({0}/(np.abs({1})+1.0))",
          "min": "np.minimum({0},{1})", "max": "np.maximum({0},{1})"}
TERMS = ("s", "r", "g")  # the item, the bin's remaining capacity, the gap it would leave (r - s)


def random_tree(rng, depth=3):
    if depth == 0 or (depth < 3 and rng.uniform() < 0.3):
        if rng.uniform() < 0.25:
            return float(np.round(rng.uniform(-5, 5), 1))
        return TERMS[rng.integers(len(TERMS))]
    if rng.uniform() < 0.3:
        return (list(UNARY)[rng.integers(len(UNARY))], random_tree(rng, depth - 1))
    return (list(BINARY)[rng.integers(len(BINARY))], random_tree(rng, depth - 1), random_tree(rng, depth - 1))


def to_src(t) -> str:
    if isinstance(t, float):
        return f"({t})"
    if isinstance(t, str):
        return {"s": "s", "r": "r", "g": "(r-s)"}[t]
    if t[0] in UNARY:
        return UNARY[t[0]].format(to_src(t[1]))
    return BINARY[t[0]].format(to_src(t[1]), to_src(t[2]))


def to_text(t) -> str:
    """A readable formula: s is the item, r the bin's room, g = r - s the gap."""
    if isinstance(t, float):
        return f"{t:g}"
    if isinstance(t, str):
        return t
    a = [to_text(c) for c in t[1:]]
    return {"neg": f"-{a[0]}", "sq": f"({a[0]})^2", "inv": f"1/(|{a[0]}|+1)", "log": f"log(|{a[0]}|+1)"}.get(t[0]) \
        or {"add": f"({a[0]} + {a[1]})", "sub": f"({a[0]} - {a[1]})", "mul": f"{a[0]}*{a[1]}",
            "div": f"{a[0]}/(|{a[1]}|+1)", "min": f"min({a[0]}, {a[1]})", "max": f"max({a[0]}, {a[1]})"}[t[0]]


def compile_tree(t):
    f = eval("lambda s, r: " + to_src(t), {"np": np})  # noqa: S307 (our own trees)

    def pr(s, r):
        with np.errstate(all="ignore"):
            v = np.broadcast_to(np.asarray(f(s, r), float), r.shape)
        return np.nan_to_num(v, nan=-1e18, posinf=1e18, neginf=-1e18)
    return pr


def size(t) -> int:
    return 1 if not isinstance(t, tuple) else 1 + sum(size(c) for c in t[1:])


def subtrees(t, path=()):
    yield path, t
    if isinstance(t, tuple):
        for k, c in enumerate(t[1:], 1):
            yield from subtrees(c, path + (k,))


def replace(t, path, new):
    if not path:
        return new
    lst = list(t)
    lst[path[0]] = replace(t[path[0]], path[1:], new)
    return tuple(lst)


def mutate(t, rng):
    paths = list(subtrees(t))
    path, sub = paths[rng.integers(len(paths))]
    if isinstance(sub, float) and rng.uniform() < 0.5:
        return replace(t, path, float(np.round(sub + rng.normal(0, 1), 1)))
    return replace(t, path, random_tree(rng, int(rng.integers(1, 3))))


def crossover(a, b, rng):
    pa = list(subtrees(a))
    pb = list(subtrees(b))
    path, _ = pa[rng.integers(len(pa))]
    _, sub = pb[rng.integers(len(pb))]
    return replace(a, path, sub)


def evolve(train, seed, pop=40, gens=25, max_size=25, log=None):
    """A small genetic-programming loop: a population of priority functions, each scored by packing the training
    instances (fewer bins is better, bigger formulas lose a tie), the best kept, the rest bred from tournaments by
    crossover and mutation.  Best fit and first fit are in the first population, as FunSearch started from a
    trivial program.  Returns the best formula of every generation and its score."""
    rng = np.random.default_rng(seed)
    population = [("neg", "g"), ("neg", "g"), ("neg", "r")] + [random_tree(rng) for _ in range(pop - 3)]
    cache = {}

    def fitness(t):
        k = repr(t)
        if k not in cache:
            cache[k] = excess(train, compile_tree(t)) + 0.002 * size(t)
        return cache[k]

    history = []
    for g in range(gens):
        scored = sorted(population, key=fitness)
        best = scored[0]
        history.append(dict(gen=g, best=to_text(best), tree=repr(best), score=fitness(best) - 0.002 * size(best),
                            median=float(np.median([fitness(t) for t in population]))))
        if log:
            log(f"binpack gen {g}: {history[-1]['score']:.3f}% excess, {to_text(best)}")
        elite = scored[:4]
        children = list(elite) + [random_tree(rng) for _ in range(pop // 10)]  # a few newcomers keep it diverse
        while len(children) < pop:
            a = min(rng.choice(len(scored), 3), key=lambda i: fitness(scored[i]))
            child = scored[a]
            if rng.uniform() < 0.5:
                b = min(rng.choice(len(scored), 3), key=lambda i: fitness(scored[i]))
                child = crossover(child, scored[b], rng)
            if rng.uniform() < 0.9:
                child = mutate(child, rng)
            if size(child) <= max_size:
                children.append(child)
        population = children
    return history, sorted(population, key=fitness)[0]
