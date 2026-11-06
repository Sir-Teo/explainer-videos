"""Learning theory (Part 57), computed.  Shattering by half-planes and the Sauer-Shelah growth function; PAC learning
curves for axis-aligned rectangles against the VC bound; the perceptron's mistakes against Novikoff's (R/gamma)^2 as
the dimension grows; AdaBoost's training error, test error and margins; Hedge, the halving algorithm, UCB, Thompson
sampling and epsilon-greedy against their bounds; statistical-query hardness of parity; double descent with random
features; and sample compression for rectangles.  After Shalev-Shwartz and Ben-David, *Understanding Machine
Learning*, and Lattimore and Szepesvari, *Bandit Algorithms*."""

from __future__ import annotations

import itertools
import math

import numpy as np


# ---------------------------------------------------------------- VC dimension

def separable(X: np.ndarray, y: np.ndarray) -> bool:
    """Is there a half-plane w.x + b with y (w.x + b) >= 1 for all points?  A feasibility LP."""
    from scipy.optimize import linprog
    n, d = X.shape
    A = -(y[:, None] * np.hstack([X, np.ones((n, 1))]))
    res = linprog(np.zeros(d + 1), A_ub=A, b_ub=-np.ones(n), bounds=[(None, None)] * (d + 1), method="highs")
    return res.status == 0


def shattering() -> dict:
    """Three points in general position are shattered by half-planes (all 8 labelings separable); no four points
    are: for a convex quadrilateral the diagonal labelling fails, for a triangle with a point inside the inner point
    against the rest fails."""
    three = np.array([[0.0, 0.0], [2.0, 0.3], [0.8, 1.8]])
    quad = np.array([[0.0, 0.0], [2.0, 0.0], [2.0, 2.0], [0.0, 2.0]])
    tri_in = np.array([[0.0, 0.0], [3.0, 0.0], [1.5, 2.5], [1.5, 0.9]])
    out = {}
    for name, P in (("three", three), ("square", quad), ("triangle with a point inside", tri_in)):
        rows = []
        for lab in itertools.product((-1, 1), repeat=len(P)):
            rows.append({"labels": list(lab), "separable": separable(P, np.array(lab, float))})
        out[name] = {"points": P.tolist(), "labelings": rows, "shattered": all(r["separable"] for r in rows),
                     "separable_count": sum(r["separable"] for r in rows)}
    return out


def growth(ms=range(1, 13), d: int = 3, trials: int = 3, seed: int = 0) -> list[dict]:
    """The number of labelings of m random points in the plane that half-planes realize, against 2^m and the
    Sauer-Shelah bound sum_{i<=d} C(m, i) with d = 3 (half-planes in the plane have VC dimension 3); for points in
    general position the exact count is m^2 - m + 2."""
    rng = np.random.default_rng(seed)
    rows = []
    for m in ms:
        best = 0
        for _ in range(trials if m <= 10 else 1):
            P = rng.random((m, 2))
            if m <= 10:
                cnt = sum(separable(P, np.array(lab, float)) for lab in itertools.product((-1, 1), repeat=m))
            else:
                cnt = m * m - m + 2
            best = max(best, cnt)
        rows.append({"m": m, "realized": int(best), "all": 2 ** m, "sauer": sum(math.comb(m, i) for i in range(d + 1)),
                     "exact_general": m * m - m + 2})
    return rows


# ---------------------------------------------------------------- PAC learning curves

def rectangle_curves(ms=(10, 20, 50, 100, 200, 500, 1000, 2000), trials: int = 200, delta: float = 0.05,
                     seed: int = 0) -> dict:
    """Learn an axis-aligned rectangle from uniform points in the unit square by the tightest fitting box (ERM in
    the realizable case).  The measured error's mean and 95th percentile against the classic bound for rectangles,
    (4/m) ln(4/delta), and the general VC bound (d = 4)."""
    rng = np.random.default_rng(seed)
    target = (0.2, 0.7, 0.3, 0.75)                   # x0, x1, y0, y1
    area_t = (target[1] - target[0]) * (target[3] - target[2])
    rows = []
    for m in ms:
        errs = []
        for _ in range(trials):
            P = rng.random((m, 2))
            inside = (P[:, 0] >= target[0]) & (P[:, 0] <= target[1]) & (P[:, 1] >= target[2]) & (P[:, 1] <= target[3])
            if inside.any():
                Q = P[inside]
                box = (Q[:, 0].min(), Q[:, 0].max(), Q[:, 1].min(), Q[:, 1].max())
                errs.append(area_t - (box[1] - box[0]) * (box[3] - box[2]))
            else:
                errs.append(area_t)
        d = 4
        vc = (4 / m) * (d * math.log2(2 * math.e * m / d) + math.log2(2 / delta))
        rows.append({"m": m, "mean": float(np.mean(errs)), "p95": float(np.quantile(errs, 1 - delta)),
                     "rect_bound": 4 / m * math.log(4 / delta), "vc_bound": min(1.0, vc)})
    return {"rows": rows, "target": list(target), "delta": delta}


def finite_class(H: int = 1000, eps: float = 0.05, delta: float = 0.05) -> dict:
    """Realizable finite class: m >= (ln |H| + ln 1/delta) / eps examples suffice."""
    return {"H": H, "eps": eps, "delta": delta, "m": math.ceil((math.log(H) + math.log(1 / delta)) / eps)}


# ---------------------------------------------------------------- perceptron

def perceptron_margin(dims=(2, 10, 100, 1000), n: int = 2000, gamma: float = 0.1, seed: int = 0) -> list[dict]:
    """Separable data with margin gamma on the unit sphere: the perceptron's mistakes (cycling until no mistake)
    against Novikoff's (R / gamma)^2 = 1/gamma^2, whatever the dimension."""
    rng = np.random.default_rng(seed)
    rows = []
    for d in dims:
        w_star = rng.standard_normal(d)
        w_star /= np.linalg.norm(w_star)
        X = []
        while len(X) < n:
            x = rng.standard_normal(d)
            x /= np.linalg.norm(x)
            if abs(x @ w_star) >= gamma:
                X.append(x)
        X = np.array(X)
        y = np.sign(X @ w_star)
        w = np.zeros(d)
        mistakes = 0
        for _ in range(1000):
            changed = False
            for xi, yi in zip(X, y):
                if yi * (w @ xi) <= 0:
                    w += yi * xi
                    mistakes += 1
                    changed = True
            if not changed:
                break
        rows.append({"d": d, "mistakes": mistakes, "bound": 1 / gamma ** 2, "gamma": gamma})
    return rows


def perceptron_branches() -> dict:
    """Part 7's perceptron branch predictor (Jimenez and Lin 2001) on Part 7's traces: a perceptron per branch over
    the global history.  Branch outcomes are not separable in general, so Novikoff's bound does not apply; the
    mistake rate is what we can report."""
    from explainer.cs.pebble import predict
    try:
        rows = predict.all_predictors() if hasattr(predict, "all_predictors") else None
    except Exception:  # noqa: BLE001
        rows = None
    return {"available": rows is not None, "rows": rows if isinstance(rows, (list, dict)) else None}


# ---------------------------------------------------------------- boosting

def adaboost(T: int = 300, n: int = 400, noise: float = 0.05, seed: int = 0) -> dict:
    """AdaBoost (Freund and Schapire 1997) with decision stumps on a ring-shaped 2D problem with a share ``noise`` of
    labels flipped: training and test error per round, the margin distribution at several rounds, and the example
    weights for drawing.  Without noise, test error does not rise for hundreds of rounds after training error
    reaches zero, while the margins keep growing (Schapire, Freund, Bartlett and Lee 1998); with noise, boosting eventually spends its rounds on the
    mislabelled points and test error creeps up."""
    rng = np.random.default_rng(seed)

    def data(k):
        X = rng.uniform(-1, 1, (k, 2))
        y = np.where(np.hypot(X[:, 0], X[:, 1]) < 0.6, 1.0, -1.0)
        flip = rng.random(k) < noise
        y[flip] *= -1
        return X, y

    X, y = data(n)
    Xt, yt = data(4000)
    w = np.ones(n) / n
    F, Ft = np.zeros(n), np.zeros(len(Xt))
    alphas, train, test, margins, snaps = [], [], [], {}, {}
    thresholds = [np.unique(X[:, j]) for j in range(2)]
    total = 0.0
    for t in range(1, T + 1):
        best = (1.0, None)
        for j in range(2):
            xs = X[:, j]
            for th in thresholds[j][::2]:
                for s in (1.0, -1.0):
                    pred = np.where(xs >= th, s, -s)
                    e = w[pred != y].sum()
                    if e < best[0]:
                        best = (e, (j, th, s))
        e, (j, th, s) = best
        e = max(e, 1e-12)
        a = 0.5 * math.log((1 - e) / e)
        h = np.where(X[:, j] >= th, s, -s)
        ht = np.where(Xt[:, j] >= th, s, -s)
        F += a * h
        Ft += a * ht
        total += a
        w *= np.exp(-a * y * h)
        w /= w.sum()
        alphas.append(a)
        train.append(float((np.sign(F) != y).mean()))
        test.append(float((np.sign(Ft) != yt).mean()))
        if t in (1, 5, 20, 100, T):
            margins[str(t)] = np.sort(y * F / total).tolist()
        if t in (1, 2, 5, 20):
            snaps[str(t)] = w.tolist()
    return {"train": train, "test": test, "margins": margins, "weights": snaps, "X": X.tolist(), "y": y.tolist(),
            "noise": noise}


# ---------------------------------------------------------------- online learning

def hedge(T: int = 2000, N: int = 20, seed: int = 0) -> dict:
    """Hedge (multiplicative weights) against N experts with random losses, the best of them slightly better:
    regret over time against sqrt(T ln N / 2)."""
    rng = np.random.default_rng(seed)
    means = rng.uniform(0.4, 0.6, N)
    means[3] = 0.35
    L = (rng.random((T, N)) < means).astype(float)
    eta = math.sqrt(8 * math.log(N) / T)
    w = np.ones(N)
    cum, regret, follow = 0.0, [], []
    cum_follow = 0.0
    best = np.zeros(N)
    for t in range(T):
        p = w / w.sum()
        cum += p @ L[t]
        leader = int(np.argmin(best)) if t else 0
        cum_follow += L[t, leader]
        best += L[t]
        w *= np.exp(-eta * L[t])
        regret.append(float(cum - best.min()))
        follow.append(float(cum_follow - best.min()))
    bound = [math.sqrt((t + 1) * math.log(N) / 2) for t in range(T)]
    return {"regret": regret[::10], "follow_the_leader": follow[::10], "bound": bound[::10], "T": T, "N": N}


def halving(N: int = 1024, T: int = 200, seed: int = 0) -> dict:
    """The halving algorithm over N hypotheses (here, N thresholds on a line), one of which is right: it predicts by
    majority and makes at most log2 N mistakes."""
    rng = np.random.default_rng(seed)
    thresholds = np.arange(N) / N
    true = thresholds[rng.integers(N)]
    alive = np.ones(N, bool)
    mistakes = 0
    hist = []
    for t in range(T):
        x = rng.random()
        votes = x >= thresholds[alive]
        pred = votes.mean() >= 0.5
        label = x >= true
        if pred != label:
            mistakes += 1
        alive &= (x >= thresholds) == label
        hist.append(int(alive.sum()))
    return {"N": N, "mistakes": mistakes, "bound": math.log2(N), "alive": hist}


# ---------------------------------------------------------------- bandits

def bandits(T: int = 5000, means=(0.5, 0.45, 0.4, 0.3), runs: int = 100, seed: int = 0) -> dict:
    """Bernoulli arms: cumulative regret of epsilon-greedy, UCB1 (Auer et al. 2002) and Thompson sampling, averaged
    over runs, and the Lai-Robbins asymptotic rate: any consistent policy's regret grows at least like
    sum over bad arms of Delta / KL(mu_i, mu*) times ln T as T goes to infinity (at finite T a policy can sit
    below the curve; it is a statement about the growth rate)."""
    rng = np.random.default_rng(seed)
    mu = np.array(means)
    K = len(mu)
    best = mu.max()
    algos = ("epsilon-greedy", "UCB1", "Thompson")
    curves = {a: np.zeros(T) for a in algos}
    for r in range(runs):
        R = rng.random((T, K)) < mu
        for a in algos:
            n = np.zeros(K)
            s = np.zeros(K)
            reg = 0.0
            out = np.zeros(T)
            for t in range(T):
                if a == "epsilon-greedy":
                    if t < K:
                        i = t
                    elif rng.random() < 0.05:
                        i = int(rng.integers(K))
                    else:
                        i = int(np.argmax(s / n))
                elif a == "UCB1":
                    i = t if t < K else int(np.argmax(s / n + np.sqrt(2 * math.log(t + 1) / n)))
                else:
                    i = int(np.argmax(rng.beta(s + 1, n - s + 1)))
                x = R[t, i]
                n[i] += 1
                s[i] += x
                reg += best - mu[i]
                out[t] = reg
            curves[a] += out / runs

    def kl(p, q):
        return p * math.log(p / q) + (1 - p) * math.log((1 - p) / (1 - q))
    c = sum((best - m) / kl(m, best) for m in mu if m < best)
    return {"T": T, "means": list(means), "curves": {a: v[::25].tolist() for a, v in curves.items()},
            "final": {a: float(v[-1]) for a, v in curves.items()},
            "lai_robbins": [c * math.log(t + 1) for t in range(0, T, 25)], "lai_robbins_const": c}


# ---------------------------------------------------------------- the limits: parity

def parity(ns=(10, 14, 18, 22), k: int = 3, m: int = 400, seed: int = 0) -> list[dict]:
    """A k-sparse parity of n bits.  Every single bit, and every set of fewer than k bits, is uncorrelated with the
    label, so a learner that only measures correlations (a statistical-query learner) must search C(n, k) subsets;
    Gaussian elimination over GF(2) needs only about n examples, but breaks as soon as labels are noisy."""
    import time
    rng = np.random.default_rng(seed)
    rows = []
    for n in ns:
        S = rng.choice(n, k, replace=False)
        X = rng.integers(0, 2, (m, n))
        y = X[:, S].sum(axis=1) % 2
        corr1 = float(np.max(np.abs(((2 * X - 1) * (2 * y - 1)[:, None]).mean(axis=0))))
        t0 = time.perf_counter()
        found = None
        tried = 0
        for sub in itertools.combinations(range(n), k):
            tried += 1
            if np.all(X[:, list(sub)].sum(axis=1) % 2 == y):
                found = sub
                break
        t_search = time.perf_counter() - t0
        t0 = time.perf_counter()
        sol = _gf2_solve(X[: 2 * n], y[: 2 * n])
        t_gauss = time.perf_counter() - t0
        rows.append({"n": n, "k": k, "max_single_bit_correlation": corr1, "subsets_total": math.comb(n, k),
                     "subsets_tried": tried, "search_seconds": t_search, "found": sorted(found) == sorted(S.tolist()),
                     "gauss_seconds": t_gauss, "gauss_found": sol is not None and sorted(np.flatnonzero(sol).tolist())
                     == sorted(S.tolist())})
    return rows


def _gf2_solve(A, b):
    A = A.copy() % 2
    b = b.copy() % 2
    m, n = A.shape
    row, piv = 0, []
    for c in range(n):
        r = next((i for i in range(row, m) if A[i, c]), None)
        if r is None:
            continue
        A[[row, r]] = A[[r, row]]
        b[[row, r]] = b[[r, row]]
        for i in range(m):
            if i != row and A[i, c]:
                A[i] ^= A[row]
                b[i] ^= b[row]
        piv.append(c)
        row += 1
    x = np.zeros(n, int)
    for i, c in enumerate(piv):
        x[c] = b[i]
    return x if np.all((A @ x) % 2 == b) else None


# ---------------------------------------------------------------- double descent

def double_descent(n: int = 50, D: int = 200, ps=None, noise: float = 0.5, trials: int = 50, seed: int = 0) -> dict:
    """Ridgeless least squares (Hastie, Montanari, Rosset and Tibshirani 2019; Belkin et al. 2019): a target that
    uses all D Gaussian features, fitted from n samples by the minimum-norm solution on the first p features.  Test
    error rises to a peak at the interpolation threshold p = n, then falls again as p grows past n."""
    rng = np.random.default_rng(seed)
    ps = ps or [5, 10, 20, 30, 40, 45, 48, 50, 52, 55, 60, 80, 100, 150, 200]
    beta = rng.standard_normal(D) / math.sqrt(D)
    rows = []
    for p in ps:
        te, tr = [], []
        for t in range(trials):
            X = rng.standard_normal((n, D))
            y = X @ beta + noise * rng.standard_normal(n)
            Xt = rng.standard_normal((500, D))
            b_ = np.linalg.pinv(X[:, :p]) @ y
            tr.append(float(np.mean((X[:, :p] @ b_ - y) ** 2)))
            te.append(float(np.mean((Xt[:, :p] @ b_ - Xt @ beta) ** 2)))
        rows.append({"p": p, "train": float(np.median(tr)), "test": float(np.median(te))})
    return {"n": n, "D": D, "noise": noise, "rows": rows}


# ---------------------------------------------------------------- compression

def rectangle_compression(m: int = 200, seed: int = 0) -> dict:
    """A sample compression scheme of size 4 for rectangles: keep the leftmost, rightmost, lowest and highest
    positive points; the tightest box through them labels every training point correctly (Littlestone and Warmuth
    1986)."""
    rng = np.random.default_rng(seed)
    target = (0.2, 0.7, 0.3, 0.75)
    P = rng.random((m, 2))
    y = (P[:, 0] >= target[0]) & (P[:, 0] <= target[1]) & (P[:, 1] >= target[2]) & (P[:, 1] <= target[3])
    Q = np.flatnonzero(y)
    keep = sorted({int(Q[np.argmin(P[Q, 0])]), int(Q[np.argmax(P[Q, 0])]), int(Q[np.argmin(P[Q, 1])]),
                   int(Q[np.argmax(P[Q, 1])])})
    K = P[keep]
    box = (K[:, 0].min(), K[:, 0].max(), K[:, 1].min(), K[:, 1].max())
    pred = (P[:, 0] >= box[0]) & (P[:, 0] <= box[1]) & (P[:, 1] >= box[2]) & (P[:, 1] <= box[3])
    return {"m": m, "kept": keep, "points": P.tolist(), "labels": y.tolist(), "box": list(map(float, box)),
            "target": list(target), "consistent": bool(np.all(pred == y))}
