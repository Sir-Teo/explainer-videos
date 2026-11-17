"""Psyche's research community (Part 61): psychology as a system that can be redesigned.

* the predictability of life outcomes: a mass collaboration of modelling teams against a four-variable regression,
  on a simulated cohort whose outcomes are mostly noise (the Fragile Families Challenge's pattern);
* heterogeneity across many labs: one effect run in dozens of labs, with true between-lab spread or none;
* scale and selection: a huge self-selected sample shrinks the noise and keeps the bias;
* integrative experiment design: a space of experiments (ten binary design choices), a sample of its cells, and a
  surrogate model that predicts the cells nobody ran;
* the natural selection of bad science (Smaldino and McElreath): laboratories whose methods are copied in
  proportion to their publications, under two publication rules.

numpy only.
"""

from __future__ import annotations

import itertools

import numpy as np


# ----------------------------------------------------------------------------------------------------------------
# Prediction of life outcomes
# ----------------------------------------------------------------------------------------------------------------
def cohort(n: int = 4000, p: int = 400, strong=(0.25, 0.2, 0.15, 0.12), weak_r2: float = 0.06, seed: int = 0):
    """A simulated cohort: ``p`` baseline variables, four with clear effects and the rest with tiny ones adding up to
    ``weak_r2`` of the variance, and an outcome that is mostly noise.  Returns X, y and the true R^2."""
    rng = np.random.default_rng(seed)
    X = rng.standard_normal((n, p))
    beta = np.zeros(p)
    beta[:4] = strong
    w = rng.standard_normal(p - 4)
    beta[4:] = w / np.linalg.norm(w) * np.sqrt(weak_r2)
    signal = X @ beta
    r2 = float(beta @ beta)
    y = signal + rng.normal(0, np.sqrt(1 - r2), n)
    return X, y, r2


def _r2(y, yhat):
    return float(1 - np.mean((y - yhat) ** 2) / np.var(y))


def challenge(teams: int = 160, n_train: int = 2000, seed: int = 0) -> dict:
    """Teams each choose a pipeline at random (a subset of variables, which usually keeps the four obvious ones, and
    a ridge penalty); every model is fitted on the training families and scored on the held-out ones.  The benchmark is ordinary least squares on the four
    variables a social scientist would pick first."""
    rng = np.random.default_rng(seed)
    X, y, r2 = cohort(seed=seed)
    tr, te = np.arange(n_train), np.arange(n_train, len(y))
    Xa = np.column_stack([np.ones(len(y)), X])
    base = np.linalg.lstsq(Xa[tr][:, :5], y[tr], rcond=None)[0]
    base_r2 = _r2(y[te], Xa[te][:, :5] @ base)
    scores = []
    for _ in range(teams):
        k = int(rng.integers(10, X.shape[1] + 1))
        chosen = set(rng.choice(X.shape[1], k, replace=False).tolist())
        if rng.random() < 0.8:
            chosen |= {0, 1, 2, 3}
        cols = np.concatenate([[0], 1 + np.sort(np.array(sorted(chosen)))])
        lam = 10 ** rng.uniform(0, 4)
        A = Xa[tr][:, cols]
        R = lam * np.eye(len(cols))
        R[0, 0] = 0
        w = np.linalg.solve(A.T @ A + R, A.T @ y[tr])
        scores.append(_r2(y[te], Xa[te][:, cols] @ w))
    scores = np.sort(np.array(scores))
    return {"scores": scores, "best": float(scores[-1]), "median": float(np.median(scores)), "baseline": base_r2,
            "ceiling": r2}


# ----------------------------------------------------------------------------------------------------------------
# Many labs
# ----------------------------------------------------------------------------------------------------------------
def many_labs(labs: int = 40, n_per_lab: int = 100, d: float = 0.3, tau: float = 0.0, seed: int = 0) -> dict:
    """One effect run in ``labs`` labs with two groups of n/2; the true effect varies between labs with SD ``tau``.
    Returns each lab's estimate and SE, the pooled estimate, tau^2 by DerSimonian-Laird and I^2."""
    rng = np.random.default_rng(seed)
    true = rng.normal(d, tau, labs)
    se = np.sqrt(4 / n_per_lab + true ** 2 / (2 * n_per_lab))
    est = rng.normal(true, se)
    w = 1 / se ** 2
    mu = np.sum(w * est) / w.sum()
    Q = np.sum(w * (est - mu) ** 2)
    df = labs - 1
    t2 = max(0.0, (Q - df) / (w.sum() - (w ** 2).sum() / w.sum()))
    return {"est": est, "se": se, "pooled": float(mu), "tau2": float(t2), "I2": float(max(0.0, (Q - df) / Q))}


# ----------------------------------------------------------------------------------------------------------------
# Scale and selection
# ----------------------------------------------------------------------------------------------------------------
def selected_sample(ns=(100, 1000, 10000, 100000, 1000000), select: float = 0.3, seed: int = 0) -> dict:
    """A population with a true mean of 0 on a standardized score; people with higher scores are more likely to
    take part (log-odds of joining rise by ``select`` per SD).  Estimates with 95% intervals at each sample size: the
    interval narrows around the wrong value."""
    rng = np.random.default_rng(seed)
    out = []
    for n in ns:
        pool = rng.standard_normal(int(n * 4))
        p = 1 / (1 + np.exp(-(np.log(0.25 / 0.75) + select * pool)))
        s = pool[rng.random(len(pool)) < p][:n]
        out.append((float(s.mean()), float(1.96 * s.std() / np.sqrt(len(s)))))
    return {"n": np.array(ns), "mean": np.array([o[0] for o in out]), "half": np.array([o[1] for o in out])}


# ----------------------------------------------------------------------------------------------------------------
# Integrative experiment design
# ----------------------------------------------------------------------------------------------------------------
def design_space(k: int = 10, base: float = 0.3, main_sd: float = 0.1, pair_sd: float = 0.05, seed: int = 0):
    """All 2^k cells of an experiment with k binary design choices; the true effect in each cell is a base plus
    main effects of each choice plus pairwise interactions.  Returns the cells (as +/-1 codes) and the effects."""
    rng = np.random.default_rng(seed)
    cells = np.array(list(itertools.product([-1, 1], repeat=k)), float)
    mains = rng.normal(0, main_sd, k)
    pairs = {(i, j): rng.normal(0, pair_sd) for i in range(k) for j in range(i + 1, k)}
    eff = base + cells @ mains
    for (i, j), v in pairs.items():
        eff = eff + v * cells[:, i] * cells[:, j]
    return cells, eff


def _features(cells):
    k = cells.shape[1]
    cols = [np.ones(len(cells))] + [cells[:, i] for i in range(k)]
    cols += [cells[:, i] * cells[:, j] for i in range(k) for j in range(i + 1, k)]
    return np.column_stack(cols)


def integrative(n_cells: int = 120, se: float = 0.08, ridge: float = 1.0, seed: int = 0) -> dict:
    """Run ``n_cells`` randomly chosen cells, each estimated with standard error ``se``; fit a ridge surrogate on
    main effects and pairwise interactions; predict every cell not run.  Also: what a single-cell study would
    report, against the spread of true effects across the space."""
    rng = np.random.default_rng(seed)
    cells, eff = design_space(seed=seed)
    run = rng.choice(len(cells), n_cells, replace=False)
    rest = np.setdiff1d(np.arange(len(cells)), run)
    obs = eff[run] + rng.normal(0, se, n_cells)
    F = _features(cells)
    R = ridge * np.eye(F.shape[1])
    R[0, 0] = 0
    w = np.linalg.solve(F[run].T @ F[run] + R, F[run].T @ obs)
    pred = F @ w
    r = float(np.corrcoef(pred[rest], eff[rest])[0, 1])
    return {"effects": eff, "run": run, "pred": pred, "held_out_r": r,
            "held_out_rmse": float(np.sqrt(np.mean((pred[rest] - eff[rest]) ** 2))),
            "spread": float(eff.std()), "range": [float(eff.min()), float(eff.max())],
            "share_negative": float(np.mean(eff < 0))}


# ----------------------------------------------------------------------------------------------------------------
# The natural selection of bad science
# ----------------------------------------------------------------------------------------------------------------
def bad_science(generations: int = 200, labs: int = 100, steps: int = 20, power: float = 0.8, base_rate: float = 0.1,
                eta: float = 0.2, rule: str = "positive", min_effort: float = 50.0, seed: int = 0) -> dict:
    """Smaldino and McElreath (2016), simplified.  A lab's effort e (1 to 100) lowers its false-positive rate,
    alpha = W / (1 + (1 - W) e), and its output, a study per step with probability 1 - eta log10 e.  Labs are
    copied in proportion to their publications, with small mutations of effort.  Under ``rule="positive"`` only
    positive results are published; under ``rule="registered"`` every study passing a methods review (effort at
    least ``min_effort``) is published whatever its result.  Returns mean effort and the false-discovery rate of
    the published positive results over generations."""
    rng = np.random.default_rng(seed)
    e = rng.uniform(40, 80, labs) if rule == "positive" else rng.uniform(max(min_effort, 40), 80, labs)
    eff_hist, fdr_hist = [], []
    for _ in range(generations):
        alpha = power / (1 + (1 - power) * e)
        h = np.clip(1 - eta * np.log10(e), 0.05, 1)
        studies = rng.binomial(steps, h)
        true = rng.binomial(studies, base_rate)
        tp = rng.binomial(true, power)
        fp = rng.binomial(studies - true, alpha)
        pubs = tp + fp if rule == "positive" else studies
        eff_hist.append(float(e.mean()))
        fdr_hist.append(float(fp.sum() / max(tp.sum() + fp.sum(), 1)))
        p = (pubs + 1e-3) / (pubs + 1e-3).sum()
        parents = rng.choice(labs, labs, p=p)
        e = np.clip(e[parents] * np.exp(rng.normal(0, 0.1, labs)), 1, 100)
        if rule == "registered":
            e = np.maximum(e, min_effort)
    return {"effort": np.array(eff_hist), "fdr": np.array(fdr_hist)}


# ----------------------------------------------------------------------------------------------------------------
# Adaptive design: choosing the next trial to tell two theories apart
# ----------------------------------------------------------------------------------------------------------------
LAGS = np.array([1, 2, 3, 5, 8, 12, 18, 27, 40, 60], dtype=float)


def retention(lags, model: str) -> np.ndarray:
    """Two theories of forgetting with their parameters fixed: exponential, 0.95 exp(-0.08 t), and power,
    0.95 (1 + t)^-0.45.  They nearly agree at middling lags and part at short and long ones."""
    t = np.asarray(lags, dtype=float)
    if model == "exp":
        return 0.95 * np.exp(-0.08 * t)
    return 0.95 * (1.0 + t) ** -0.45


def _info(p_pow: float, a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """Mutual information (bits) between the model indicator and one recall outcome, at each lag."""
    def h(q):
        q = np.clip(q, 1e-12, 1 - 1e-12)
        return -(q * np.log2(q) + (1 - q) * np.log2(1 - q))
    m = p_pow * a + (1 - p_pow) * b
    return h(m) - p_pow * h(a) - (1 - p_pow) * h(b)


def adaptive_design(people: int = 2000, trials: int = 80, target: float = 0.95, seed: int = 0) -> dict:
    """Each simulated person forgets by the power law.  A recall test at one lag per trial; the posterior that the
    power law is right starts at 0.5.  The fixed design cycles through the ten lags in a shuffled order; the adaptive
    design picks, before each trial, the lag with the most expected information (Cavagnaro, Myung and Pitt's
    criterion).  Returns the median posterior over trials and the trials each design needs to reach ``target``."""
    rng = np.random.default_rng(seed)
    a, b = retention(LAGS, "pow"), retention(LAGS, "exp")
    la, lb = np.log(a), np.log(b)
    l1a, l1b = np.log1p(-a), np.log1p(-b)
    post = {"fixed": np.zeros((people, trials + 1)), "adaptive": np.zeros((people, trials + 1))}
    picks = np.zeros(len(LAGS))
    for design in ("fixed", "adaptive"):
        for i in range(people):
            llr = 0.0
            order = np.concatenate([rng.permutation(len(LAGS)) for _ in range(trials // len(LAGS) + 1)])
            post[design][i, 0] = 0.5
            for t in range(trials):
                p = 1.0 / (1.0 + np.exp(-llr))
                k = int(order[t]) if design == "fixed" else int(np.argmax(_info(p, a, b)))
                if design == "adaptive":
                    picks[k] += 1
                y = rng.random() < a[k]
                llr += (la[k] - lb[k]) if y else (l1a[k] - l1b[k])
                post[design][i, t + 1] = 1.0 / (1.0 + np.exp(-llr))
    out = {"lags": LAGS.tolist(), "pow": a.tolist(), "exp": b.tolist(),
           "info0": _info(0.5, a, b).tolist(), "picks": (picks / picks.sum()).tolist()}
    for design, P in post.items():
        out[f"median_{design}"] = np.median(P, axis=0).tolist()
        reached = (P >= target)
        first = np.where(reached.any(axis=1), reached.argmax(axis=1), trials + 1)
        out[f"trials_{design}"] = float(np.median(first))
        out[f"share_{design}"] = float(np.mean(P[:, -1] >= target))
    return out
