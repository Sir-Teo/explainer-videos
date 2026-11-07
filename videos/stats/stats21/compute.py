"""Precompute every number in Part 21 of *Statistics, Built* ("Optimization for Statistics").

    python -m videos.stats.stats21.compute            # everything missing (about a minute)
    python -m videos.stats.stats21.compute --force board

Results are cached in ``.cache/stats21/<name>.json``.  Boscovich's arcs and Engel's households are the Museum's; the
vote is the World's survey block; the rest are seeded simulations or worked examples.

Items:
    bakery      a small linear program, solved by the simplex method, with its vertex path and shadow prices
    convex      a concave log likelihood (logistic) and a multimodal one (Cauchy location)
    kkt         a binomial MLE under the constraint p <= 1/2: the multiplier and complementary slackness
    np          the Neyman-Pearson lemma as a linear program (binomial, n = 20)
    lad         Boscovich's five arcs: least squares vs least absolute deviations; Engel's quantile regressions
    newton      Newton (Fisher scoring) vs gradient ascent for the World's vote; digits of accuracy; Cauchy failure
    mm          the median by MM: majorizers and iterates; Hunter-Lange MM on Engel against the LP optimum
    cd          a two-variable lasso: objective contours, coordinate-descent and ISTA paths
    prox        ISTA vs FISTA on an ill-conditioned lasso, with the theoretical bounds
    admm        the fused lasso by ADMM on a piecewise-constant signal; residuals
    sgd         Robbins-Monro for a median; SGD vs Polyak-Ruppert averaging vs the MLE for the World's vote
    inference   the Hessian at the optimum and the SEs; optimization error vs statistical error
    pava        isotonic regression of the World's vote on income, by pool-adjacent-violators
    bt          Bradley-Terry rankings for a toy season, by Hunter's MM
    cdcorr      coordinate-descent sweeps to convergence, against the correlation of two predictors
    sgdsteps    SGD's last iterate vs its average, across step-size exponents
    sandwich    the logistic vote model without age or region: model-based vs sandwich SEs, against the spread over samples
    board       Coverage Board rows: Wald intervals from SGD's last iterate and from its average
"""

from __future__ import annotations

from dataclasses import asdict

import numpy as np

from explainer.ai.cache import Cache
from explainer.stats import museum
from explainer.stats.board import Row, save_rows
from explainer.stats.kit import optim as O
from explainer.stats.world import World

CACHE = Cache("stats21")
load = CACHE.load
W = World()
R_BOARD = 500


def rng(seed: int) -> np.random.Generator:
    return np.random.Generator(np.random.PCG64(seed))


def nest(obj):
    if isinstance(obj, np.ndarray):
        return nest(obj.tolist())
    if isinstance(obj, dict):
        return {str(k): nest(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [nest(v) for v in obj]
    if isinstance(obj, (np.floating, np.integer)):
        return obj.item()
    if isinstance(obj, np.bool_):
        return bool(obj)
    return obj


def clipped_segments(xs, ys, rectangle):
    """Intersect segments with the viewport, preserving crossings and missing breaks."""
    xmin, xmax, ymin, ymax = rectangle
    points = np.column_stack((xs, ys))
    result = []
    for start, end in zip(points[:-1], points[1:]):
        if not np.isfinite([start, end]).all():
            continue
        delta = end-start
        lo, hi = 0., 1.
        for j, lower, upper in ((0, xmin, xmax), (1, ymin, ymax)):
            if delta[j] == 0:
                if not lower <= start[j] <= upper:
                    hi = -1
                    break
            else:
                a, b = sorted(((lower-start[j])/delta[j], (upper-start[j])/delta[j]))
                lo, hi = max(lo, a), min(hi, b)
        if lo <= hi:
            result.append((start+lo*delta, start+hi*delta))
    return result

BAKERY_C = [3.0, 4.0]  # profit per tray of loaves, per tray of cakes
BAKERY_A = [[1.0, 2.0], [3.0, 2.0], [1.0, 1.0]]  # flour (sacks), oven (hours), staff (shifts) per tray
BAKERY_B = [14.0, 24.0, 9.0]


def compute_bakery():
    r = O.simplex(BAKERY_C, BAKERY_A, BAKERY_B)
    A, b = np.array(BAKERY_A), np.array(BAKERY_B)
    # every vertex of the feasible polygon, for the drawing
    verts = []
    lines = [(A[i], b[i]) for i in range(3)] + [(np.array([1.0, 0.0]), 0.0), (np.array([0.0, 1.0]), 0.0)]
    for i in range(len(lines)):
        for j in range(i + 1, len(lines)):
            M = np.vstack([lines[i][0], lines[j][0]])
            if abs(np.linalg.det(M)) < 1e-12:
                continue
            v = np.linalg.solve(M, [lines[i][1], lines[j][1]])
            if np.all(v >= -1e-9) and np.all(A @ v <= b + 1e-9):
                verts.append(v)
    verts = np.unique(np.round(verts, 9), axis=0)
    c = np.array(BAKERY_C)
    ang = np.arctan2(verts[:, 1] - verts[:, 1].mean(), verts[:, 0] - verts[:, 0].mean())
    verts = verts[np.argsort(ang)]
    return nest({"c": BAKERY_C, "A": BAKERY_A, "b": BAKERY_B, "path": r["path"], "x": r["x"], "value": r["value"],
                 "dual": r["dual"], "verts": verts, "vert_values": verts @ c})


def compute_convex():
    from scipy.optimize import brentq
    from scipy.special import expit
    x = np.array([-2.1, -1.6, -1.2, 3.4, 4.0, 4.6, 5.1])
    f, _, _ = O.cauchy_location(x)
    th = np.linspace(-6, 10, 401)
    cl = np.array([f([t]) for t in th])
    # logistic regression slope for the World's vote, intercept fixed at its MLE
    X, v = vote_data(800, 21)
    z = X[:, 1]
    fit = O.logistic_scoring(X, v)
    bs = np.linspace(-0.5, 1.5, 301)
    ll = [float(np.sum(v * (fit["b"][0] + b * z) - np.logaddexp(0, fit["b"][0] + b * z))) for b in bs]
    profile = []
    for b in bs:
        a = brentq(lambda a: np.sum(v - expit(a + b * z)), -50, 50)
        eta = a + b * z
        profile.append(float(np.sum(v * eta - np.logaddexp(0, eta))))
    loc_max = [float(th[i]) for i in range(1, len(th) - 1) if cl[i] > cl[i - 1] and cl[i] > cl[i + 1]]
    return nest({"x": x, "theta": th, "cauchy": cl, "local_max": loc_max, "b": bs, "logistic": ll,
                 "profile": profile, "profile_se": fit["se"][1], "logistic_max": fit["loglik"][-1],
                 "b_hat": fit["b"][1]})


def compute_kkt():
    out = {}
    for name, (n, k) in {"binding": (50, 30), "slack": (50, 20)}.items():
        p = np.linspace(0.01, 0.99, 197)
        ll = k * np.log(p) + (n - k) * np.log(1 - p)
        phat = k / n
        pc = min(phat, 0.5)
        mult = max(0.0, k / 0.5 - (n - k) / 0.5)  # d loglik / dp at the boundary, if the constraint binds
        out[name] = {"n": n, "k": k, "p": p, "ll": ll, "phat": phat, "pc": pc, "mult": mult if phat > 0.5 else 0.0,
                     "ll_c": float(k * np.log(pc) + (n - k) * np.log(1 - pc))}
    return nest(out)


def compute_np():
    from scipy.stats import binom

    k = np.arange(21)
    p0, p1 = binom.pmf(k, 20, 0.5), binom.pmf(k, 20, 0.7)
    r = O.neyman_pearson_lp(p0, p1, 0.05)
    return nest({"x": k, "p0": p0, "p1": p1, "lr": p1 / p0, **r})


def compute_lad():
    lat = np.array([b[1] for b in museum.BOSCOVICH])
    arc = np.array([b[2] for b in museum.BOSCOVICH], float)
    s2 = np.sin(np.radians(lat)) ** 2
    X = np.column_stack([np.ones(5), s2])
    lad = O.quantile_lp(X, arc)
    ls = np.linalg.lstsq(X, arc, rcond=None)[0]
    inc, food = museum.engel()
    Xe = np.column_stack([np.ones(len(inc)), inc / 1000])
    taus = [0.1, 0.25, 0.5, 0.75, 0.9]
    qr = {str(t): O.quantile_lp(Xe, food, t)["b"] for t in taus}
    ols = np.linalg.lstsq(Xe, food, rcond=None)[0]
    return nest({"names": [b[0] for b in museum.BOSCOVICH], "lat": lat, "s2": s2, "arc": arc, "lad": lad["b"],
                 "lad_through": lad["basic"], "ls": ls, "lad_sum": float(np.sum(np.abs(arc - X @ lad["b"]))),
                 "ls_sum": float(np.sum(np.abs(arc - X @ ls))), "income": inc, "food": food, "taus": taus, "qr": qr, "ols": ols})


_li = np.log10(W.income[W.adult] / 1000)
Z_MEAN, Z_SD = float(_li.mean()), float(_li.std())


def vote_data(n, seed, raw: bool = False):
    """The World's vote on log income: standardized (per SD of log10 income), or ``raw`` (log10 income in thousands,
    uncentred, so the intercept and slope are strongly correlated and the problem is ill-conditioned)."""
    idx = W.sample(n, among=W.adult, seed=seed)
    li = np.log10(W.income[idx] / 1000)
    z = li if raw else (li - Z_MEAN) / Z_SD
    v = W.survey["vote_blue"][idx].astype(float)
    return np.column_stack([np.ones(n), z]), v


def compute_newton():
    X, y = vote_data(2000, 2101, raw=True)
    sc = O.logistic_scoring(X, y, iters=12)
    bhat = sc["b"]
    err = [float(np.linalg.norm(b - bhat)) for b in sc["path"]]
    # Gradient ascent with a globally safe fixed step 1/L, not an optimal fixed step.
    L = float(np.linalg.eigvalsh(X.T @ X / 4).max())
    b = np.zeros(2)
    gpath = [b.copy()]
    for _ in range(400):
        p = 1 / (1 + np.exp(-X @ b))
        b = b + X.T @ (y - p) / L
        gpath.append(b.copy())
    gerr = [float(np.linalg.norm(v - bhat)) for v in gpath]
    b0s = np.linspace(-5.0, 1.0, 121)
    b1s = np.linspace(-0.5, 3.5, 121)
    ll = np.array([[float(np.sum(y * (X @ [a, c]) - np.logaddexp(0, X @ [a, c]))) for a in b0s] for c in b1s])
    # Cauchy: plain Newton from a poor start, and with a line search
    x = np.array([-2.1, -1.6, -1.2, 3.4, 4.0, 4.6, 5.1])
    f, g, h = O.cauchy_location(x)
    plain = O.newton(f, g, h, [1.2], line_search=False, maximize=True, max_iter=8)
    safe = O.newton(f, g, h, [1.2], line_search=True, maximize=True, max_iter=30)
    return nest({"bhat": bhat, "path": sc["path"], "err": err, "gpath": gpath[:60], "gerr": gerr, "L": L, "b0s": b0s,
                 "b1s": b1s, "ll": ll, "ll_max": float(sc["loglik"][-1]), "se": sc["se"], "n": 2000,
                 "cauchy_plain": plain["path"][:, 0], "cauchy_safe": safe["path"][:, 0], "cauchy_x": x})


def compute_mm():
    x = np.array([1.0, 2.0, 2.5, 4.0, 7.0, 8.0, 11.0])
    th = 9.0
    steps = []
    for _ in range(8):
        w = 1 / np.abs(x - th)  # these eight illustrative iterates never coincide with an observation
        steps.append({"theta": th, "w": w})
        th = float(np.sum(w * x) / np.sum(w))
    grid = np.linspace(-1, 13, 281)
    f = np.array([np.sum(np.abs(x - t)) for t in grid])
    inc, food = museum.engel()
    Xe = np.column_stack([np.ones(len(inc)), inc / 1000])
    lp = O.quantile_lp(Xe, food, 0.5)
    mm = O.quantile_mm(Xe, food, 0.5, iters=60, eps=1e-6)
    return nest({"x": x, "steps": [{"theta": s["theta"], "f": float(np.sum(np.abs(x - s["theta"])))} for s in steps],
                 "thetas": [s["theta"] for s in steps], "weights": [s["w"] for s in steps], "grid": grid, "f": f,
                 "median": float(np.median(x)), "engel_lp": lp["objective"], "engel_mm": mm["objective"]})


def lasso2(seed=2101):
    g = rng(seed)
    n = 200
    z = g.normal(size=n)
    X = np.column_stack([z + 0.5 * g.normal(size=n), z + 0.5 * g.normal(size=n)])
    X = (X - X.mean(0)) / X.std(0)
    y = X @ [1.5, 0.3] + g.normal(size=n)
    return X, y - y.mean()


def compute_cd():
    X, y = lasso2()
    lam = 0.3
    cd = O.cd_lasso(X, y, lam, sweeps=60, b0=[-1.0, 2.0])
    ist = O.ista(X, y, lam, iters=40, b0=[-1.0, 2.0])
    b0s = np.linspace(-1.5, 2.5, 101)
    b1s = np.linspace(-1.5, 2.5, 101)
    obj = np.array([[O.lasso_objective(X, y, np.array([a, c]), lam) for a in b0s] for c in b1s])
    gaps = [O.lasso_dual_gap(X, y, b, lam)["gap"] for b in cd["path"]]
    return nest({"lam": lam, "b0s": b0s, "b1s": b1s, "obj": obj, "cd_path": cd["path"][::1][:25], "ista_path": ist["path"][:41],
                 "bhat": cd["b"], "fmin": float(cd["objective"][-1]), "gaps": gaps, "corr": float(np.corrcoef(X.T)[0, 1])})


def compute_prox():
    g = rng(2009)
    n, p = 300, 40
    z = g.normal(size=(n, 1))
    X = z + 0.15 * g.normal(size=(n, p))
    beta = np.zeros(p)
    beta[:4] = [2, -1.5, 1, 0.5]
    y = X @ beta + g.normal(size=n)
    lam = 0.05
    best = O.cd_lasso(X, y, lam, sweeps=4000)
    fstar = float(best["objective"][-1])
    K = 400
    ist = O.ista(X, y, lam, iters=K)
    fis = O.ista(X, y, lam, iters=K, accelerate=True)
    L = ist["L"]
    R2 = float(np.sum(best["b"] ** 2))
    k = np.arange(1, K + 1)
    return nest({"K": K, "ista": ist["objective"][1:] - fstar, "fista": fis["objective"][1:] - fstar,
                 "bound_ista": L * R2 / (2 * k), "bound_fista": 2 * L * R2 / (k + 1) ** 2, "L": L, "p": p, "n": n,
                 "cond": float(np.linalg.cond(X.T @ X / n))})


def fused_lasso(y, lam, rho=1.0, iters=800):
    """TV denoising with one O(n) banded factorization; record both ADMM residuals."""
    from scipy.linalg import cholesky_banded, cho_solve_banded

    y = np.asarray(y, float)
    if y.ndim != 1 or not len(y) or not np.isfinite(y).all() or not np.isfinite([lam, rho]).all() or lam < 0 or rho <= 0 or iters < 1:
        raise ValueError("Require finite nonempty y, lambda >= 0, rho > 0, and positive iterations")
    if len(y) == 1:
        return {"b": y.copy(), "primal_res": np.zeros(iters), "dual_res": np.zeros(iters),
                "objective": np.zeros(iters)}
    ab = np.zeros((2, len(y)))
    ab[0] = 1 + 2 * rho
    ab[0, [0, -1]] = 1 + rho
    ab[1, :-1] = -rho
    factor = cholesky_banded(ab, lower=True)
    transpose = lambda v: np.r_[-v[0], v[:-1] - v[1:], v[-1]]  # noqa: E731
    z, u = np.zeros(len(y) - 1), np.zeros(len(y) - 1)
    objectives, primal, dual = [], [], []
    for _ in range(iters):
        b = cho_solve_banded((factor, True), y + rho * transpose(z - u))
        Db = np.diff(b)
        previous = z
        z = O.prox_l1(Db + u, lam / rho)
        u += Db - z
        objectives.append(0.5 * np.sum((y - b) ** 2) + lam * np.abs(Db).sum())
        primal.append(np.linalg.norm(Db - z))
        dual.append(rho * np.linalg.norm(transpose(z - previous)))
    return {"b": b, "objective": np.asarray(objectives), "primal_res": np.asarray(primal),
            "dual_res": np.asarray(dual)}


def compute_admm():
    g = rng(2011)
    levels = [(0, 30, 0.0), (30, 55, 2.0), (55, 70, -1.0), (70, 120, 1.0)]
    truth = np.concatenate([np.full(b - a, v) for a, b, v in levels])
    y = truth + g.normal(0, 0.6, len(truth))
    fits = {}
    for lam in (0.5, 3.0, 20.0):
        r = fused_lasso(y, lam, rho=1.0, iters=800)
        fits[str(lam)] = {"b": r["b"], "res": r["primal_res"][:400], "dual_res": r["dual_res"][:400],
                          "obj": r["objective"][:400]}
    return nest({"y": y, "truth": truth, "fits": fits})


def compute_sgd():
    g = rng(1951)
    xs = g.normal(10, 3, 5000)
    rm = O.robbins_monro_quantile(xs, 0.5, step0=10.0, power=1.0, theta0=0.0)
    X, y = vote_data(20_000, 2102)
    mle = O.logistic_scoring(X, y)
    s = O.sgd_logistic(X, y, step0=1.0, power=0.6)
    ks = np.unique(np.round(np.logspace(1, np.log10(20_000), 120)).astype(int)) - 1
    return nest({"rm_path": rm["path"][:2000], "rm_true": 10.0, "mle": mle["b"], "se": mle["se"], "k": ks + 1,
                 "last": s["path"][ks, 1], "avg": s["avg_path"][ks, 1], "n": 20_000})


def compute_inference():
    X, y = vote_data(2000, 2101, raw=True)
    sc = O.logistic_scoring(X, y)
    info = sc["info"]
    se = sc["se"]
    # gradient ascent: optimization error vs the statistical error (SE)
    L = float(np.linalg.eigvalsh(X.T @ X / 4).max())
    b = np.zeros(2)
    opt_err = []
    for _ in range(3000):
        p = 1 / (1 + np.exp(-X @ b))
        b = b + X.T @ (y - p) / L
        opt_err.append(float(abs(b[1] - sc["b"][1])))
    # the bootstrap SE, for comparison
    g = rng(5)
    bs = []
    for _ in range(300):
        i = g.integers(0, len(y), len(y))
        bs.append(O.logistic_scoring(X[i], y[i], iters=15)["b"][1])
    below = np.flatnonzero(np.asarray(opt_err) < se[1] / 10)
    return nest({"b": sc["b"], "se": se, "info": info, "opt_err": opt_err[::10],
                 "opt_iters": np.arange(1, len(opt_err) + 1)[::10], "boot_se": float(np.std(bs, ddof=1)),
                 "first_below": int(below[0] + 1) if len(below) else None})


def compute_pava():
    idx = W.sample(1500, among=W.adult, seed=2104)
    inc = W.income[idx]
    v = W.survey["vote_blue"][idx].astype(float)
    q = np.quantile(inc, np.linspace(0, 1, 26))
    b = np.clip(np.searchsorted(q, inc, side="right") - 1, 0, 24)
    share = np.array([v[b == j].mean() for j in range(25)])
    cnt = np.array([np.sum(b == j) for j in range(25)], float)
    mid = np.array([np.median(inc[b == j]) for j in range(25)]) / 1000
    r = O.pava(share, cnt)
    # the World's truth in each bin: the population share at that income
    A = W.adult
    pi, pv = W.income[A], W.survey["vote_blue"][A]
    truth = np.array([pv[(pi >= q[j]) & (pi < q[j + 1])].mean() for j in range(25)])
    return nest({"mid": mid, "share": share, "fit": r["fit"], "blocks": r["blocks"], "truth": truth,
                 "violations": int(np.sum(np.diff(share) < 0))})


BT_TEAMS = ["Harbour", "Mill", "Orchard", "Quarry"]
BT_WINS = [[0, 7, 8, 9], [3, 0, 6, 7], [2, 4, 0, 6], [1, 3, 4, 0]]


def compute_bt():
    r = O.bradley_terry_mm(BT_WINS, iters=60)
    g = r["g"]
    P = g[:, None] / (g[:, None] + g[None, :])
    return nest({"teams": BT_TEAMS, "wins": BT_WINS, "g": g, "path": r["path"], "loglik": r["loglik"], "P": P})


def compute_cdcorr():
    out = []
    for rho in (0.0, 0.3, 0.6, 0.8, 0.9, 0.95, 0.99):
        g = rng(77)
        n = 400
        z = g.normal(size=n)
        e = g.normal(size=(n, 2))
        X = np.sqrt(rho) * z[:, None] + np.sqrt(1 - rho) * e
        X = (X - X.mean(0)) / X.std(0)
        y = X @ [1.0, 0.5] + g.normal(size=n)
        y = y - y.mean()
        cd = O.cd_lasso(X, y, 0.05, sweeps=4000)
        gaps = np.array([O.lasso_dual_gap(X, y, b, 0.05)["gap"] for b in cd["path"][::2]])
        sweeps = int(np.argmax(gaps < 1e-8)) if np.any(gaps < 1e-8) else 4000
        out.append({"rho": rho, "corr": float(np.corrcoef(X.T)[0, 1]), "sweeps": sweeps})
    return nest({"runs": out})


def compute_sgdsteps():
    powers = [0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    last, avg = {p: [] for p in powers}, {p: [] for p in powers}
    for r in range(30):
        X, y = vote_data(5000, 40_000 + r)
        mle = O.logistic_scoring(X, y)["b"][1]
        for p in powers:
            s = O.sgd_logistic(X, y, step0=1.0, power=p)
            last[p].append((s["b"][1] - mle) ** 2)
            avg[p].append((s["avg"][1] - mle) ** 2)
    se2 = float(O.logistic_scoring(*vote_data(5000, 40_000))["se"][1] ** 2)
    return nest({"powers": powers, "rmse_last": [float(np.sqrt(np.mean(last[p]))) for p in powers],
                 "rmse_avg": [float(np.sqrt(np.mean(avg[p]))) for p in powers], "se": float(np.sqrt(se2))})


def compute_sandwich():
    X, y = vote_data(2000, 2105)
    sc = O.logistic_scoring(X, y)
    p = 1 / (1 + np.exp(-X @ sc["b"]))
    A = X.T @ ((p * (1 - p))[:, None] * X)
    U = X * (y - p)[:, None]
    Ai = np.linalg.inv(A)
    sand = Ai @ (U.T @ U) @ Ai
    reps = [O.logistic_scoring(*vote_data(2000, 50_000 + r), iters=15)["b"][1] for r in range(400)]
    return nest({"b": sc["b"], "se_model": float(np.sqrt(Ai[1, 1])), "se_sandwich": float(np.sqrt(sand[1, 1])),
                 "sd_reps": float(np.std(reps, ddof=1))})


def population_vote_target():
    """Census logistic projection for the fixed finite World, including its nuisance intercept."""
    # Exact finite-population projection: no sampled reference error shared by all replicates.
    truth_X = np.column_stack([np.ones(len(_li)), (_li - Z_MEAN) / Z_SD])
    truth_y = W.survey["vote_blue"][W.adult].astype(float)
    return O.logistic_scoring(truth_X, truth_y)["b"]


def compute_board():
    hits_last = hits_avg = 0
    beta = population_vote_target()[1]
    for r in range(R_BOARD):
        X, y = vote_data(2000, 30_000 + r)
        s = O.sgd_logistic(X, y, step0=1.0, power=0.6)
        for b, key in ((s["b"], "last"), (s["avg"], "avg")):
            p = 1 / (1 + np.exp(-X @ b))
            info = X.T @ ((p * (1 - p))[:, None] * X)
            se = float(np.sqrt(np.linalg.inv(info)[1, 1]))
            hit = abs(b[1] - beta) <= 1.96 * se
            if key == "last":
                hits_last += hit
            else:
                hits_avg += hit
    rows = [Row(21, r"SGD last iterate, Wald CI", r"logistic slope, \ the World's vote, \ $n = 2{,}000$", "coverage", 0.95,
                hits_last / R_BOARD, R_BOARD),
            Row(21, r"Polyak--Ruppert average, Wald CI", r"logistic slope, \ the World's vote, \ $n = 2{,}000$", "coverage", 0.95,
                hits_avg / R_BOARD, R_BOARD)]
    save_rows(21, rows)
    return {"rows": [asdict(r) | {"verdict": r.verdict, "se": r.se} for r in rows], "beta": float(beta)}


ITEMS = {
    "bakery": compute_bakery, "convex": compute_convex, "kkt": compute_kkt, "np": compute_np, "lad": compute_lad,
    "newton": compute_newton, "mm": compute_mm, "cd": compute_cd, "prox": compute_prox, "admm": compute_admm,
    "sgd": compute_sgd, "inference": compute_inference, "pava": compute_pava, "bt": compute_bt, "cdcorr": compute_cdcorr, "sgdsteps": compute_sgdsteps, "sandwich": compute_sandwich, "board": compute_board,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
