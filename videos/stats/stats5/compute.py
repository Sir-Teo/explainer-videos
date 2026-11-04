"""Precompute every number in Part 5 of *Statistics, Built* ("Many Variables at Once").

    python -m videos.stats.stats5.compute            # everything missing (well under a minute)
    python -m videos.stats.stats5.compute --force copulas

Results are cached in ``.cache/stats5/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.  Galton's data are the
Museum's (``museum.GALTON_*``, from Galton 1886 via HistData); everything else is the World or a seeded simulation.

Items:
    galton       Galton's 928 children: the table, its smoothed version, means, SDs, r, the three lines, the
                 fitted normal ellipse, and the mean child height in each mid-parent row
    slicer       the World's families (mid-parent, child): bivariate normal fit, slices at three mid-parent heights
                 and their renormalized conditional densities; the conditional mean and SD
    dependence   uncorrelated but dependent: Y = X^2, the ring, and the random-sign pair
    predictor    the World's incomes by age: the best constant, the best line, E[income | age]; their MSEs
    eve          the law of total variance for incomes: by region and by age group
    mvn          an affine image of iid normals; marginals; the random-sign counterexample
    regression   regression to the mean: the World's tallest parents; a test-retest (skill + luck) simulation
    lines        the three lines through Galton's ellipse
    jacobian     the sum of two uniforms (a triangle); the ratio of two normals (a Cauchy)
    latent       the World's adult heights as a mixture of men and women
    copulas      Gaussian, Clayton and Gumbel copulas with Kendall's tau 0.5: joint tails
    polya        Polya's urn: 30 runs of 1,000 draws; 4,000 limiting fractions against the uniform (Beta(1, 1))
    measures     Pearson, Spearman, Kendall, distance correlation and mutual information on six shapes
    simplex      Dirichlet samples for four parameter vectors
"""

from __future__ import annotations

import numpy as np
from scipy import stats

from explainer.ai.cache import Cache
from explainer.stats import museum
from explainer.stats.world import World

CACHE = Cache("stats5")
load = CACHE.load
W = World()


def rng(seed: int) -> np.random.Generator:
    return np.random.Generator(np.random.PCG64(seed))


def nest(obj):
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    if isinstance(obj, dict):
        return {k: nest(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [nest(v) for v in obj]
    if isinstance(obj, (np.floating, np.integer)):
        return obj.item()
    return obj


def galton_points():
    P, C, T = np.array(museum.GALTON_PARENT), np.array(museum.GALTON_CHILD), np.array(museum.GALTON_TABLE)
    x = np.repeat(np.repeat(P, len(C)), T.ravel())
    y = np.repeat(np.tile(C, len(P)), T.ravel())
    return x, y


# ---------------------------------------------------------------------------
def compute_galton():
    P, C, T = np.array(museum.GALTON_PARENT), np.array(museum.GALTON_CHILD), np.array(museum.GALTON_TABLE)
    x, y = galton_points()
    mx, my, sx, sy = x.mean(), y.mean(), x.std(), y.std()
    r = float(np.corrcoef(x, y)[0, 1])
    b_yx = r * sy / sx
    b_xy = r * sx / sy  # x on y, as dx/dy
    S = np.cov(np.vstack([x, y]))
    ev, V = np.linalg.eigh(S)
    major = float(V[1, 1] / V[0, 1])
    # Galton's smoothing: the average of each 2 x 2 block of the table
    Ts = (T[:-1, :-1] + T[1:, :-1] + T[:-1, 1:] + T[1:, 1:]) / 4.0
    row_means = [float((T[i] * C).sum() / T[i].sum()) if T[i].sum() else None for i in range(len(P))]
    return nest({"P": P, "C": C, "T": T, "Ts": Ts, "x": x, "y": y, "mx": mx, "my": my, "sx": sx, "sy": sy, "r": r,
                 "b_yx": b_yx, "b_xy": b_xy, "major": major, "S": S, "eig": ev, "V": V, "row_means": row_means,
                 "n": int(T.sum()), "n_fam": 205})


def compute_slicer():
    f = W.families
    son = f["son"]
    mid = ((f["father"] + f["mother"]) / 2)[son]
    ch = f["child"][son]
    mx, my = mid.mean(), ch.mean()
    S = np.cov(np.vstack([mid, ch]))
    sx, sy = np.sqrt(S[0, 0]), np.sqrt(S[1, 1])
    rho = S[0, 1] / (sx * sy)
    slices = []
    for x0 in (162.0, 170.0, 178.0):
        cm = my + S[0, 1] / S[0, 0] * (x0 - mx)
        cs = np.sqrt(S[1, 1] - S[0, 1] ** 2 / S[0, 0])
        near = np.abs(mid - x0) < 0.5
        slices.append({"x0": x0, "cm": cm, "cs": cs, "emp_mean": float(ch[near].mean()), "emp_sd": float(ch[near].std()),
                       "n": int(near.sum()), "emp": ch[near][:3000]})
    return nest({"mx": mx, "my": my, "S": S, "sx": sx, "sy": sy, "rho": rho, "slices": slices,
                 "sample_x": mid[:1500], "sample_y": ch[:1500], "n": int(len(ch))})


def compute_dependence():
    g = rng(5)
    x = g.normal(size=2000)
    y = x ** 2 + 0.1 * g.normal(size=2000)
    t = g.uniform(0, 2 * np.pi, 2000)
    rad = 1 + 0.08 * g.normal(size=2000)
    cx, cy = rad * np.cos(t), rad * np.sin(t)
    s = g.choice([-1.0, 1.0], 2000)
    z = s * x
    return nest({"x": x[:1200], "y": y[:1200], "cx": cx[:1200], "cy": cy[:1200], "z": z[:1200],
                 "r_par": float(np.corrcoef(x, y)[0, 1]), "r_ring": float(np.corrcoef(cx, cy)[0, 1]),
                 "r_sign": float(np.corrcoef(x, z)[0, 1]),
                 "p_big": float(np.mean(np.abs(x) > 1.5)), "p_big_given": float(np.mean((np.abs(z) > 1.5)[np.abs(x) > 1.5]))})


def compute_predictor():
    a = W.adult & ~np.isnan(W.income)
    age, inc = W.age[a].astype(float), np.log(W.income[a] / 1000)
    g = rng(6)
    idx = g.choice(len(age), 3000, replace=False)
    ages = np.arange(18, 96)
    cond = np.array([inc[age == k].mean() for k in ages])
    const = inc.mean()
    b1, b0 = np.polyfit(age, inc, 1)
    mse_const = float(((inc - const) ** 2).mean())
    mse_line = float(((inc - (b0 + b1 * age)) ** 2).mean())
    cm_all = np.interp(age, ages, cond)
    mse_cond = float(((inc - cm_all) ** 2).mean())
    return nest({"age": age[idx], "inc": inc[idx], "ages": ages, "cond": cond, "const": const, "b0": b0, "b1": b1,
                 "mse_const": mse_const, "mse_line": mse_line, "mse_cond": mse_cond,
                 "r2_line": 1 - mse_line / mse_const, "r2_cond": 1 - mse_cond / mse_const})


def compute_eve():
    a = W.adult & ~np.isnan(W.income)
    inc = W.income[a] / 1000
    reg = W.region[a]
    age = W.age[a]
    out = {"total": float(inc.var())}
    for name, grp in (("region", reg), ("age", np.digitize(age, [25, 35, 45, 55, 65]))):
        ks = np.unique(grp)
        w = np.array([np.mean(grp == k) for k in ks])
        m = np.array([inc[grp == k].mean() for k in ks])
        v = np.array([inc[grp == k].var() for k in ks])
        within = float((w * v).sum())
        between = float((w * (m - inc.mean()) ** 2).sum())
        out[name] = {"within": within, "between": between, "share": between / out["total"], "means": m, "w": w}
    # also on log income, which is less heavy-tailed
    li = np.log(inc)
    grp = np.digitize(age, [25, 35, 45, 55, 65])
    ks = np.unique(grp)
    w = np.array([np.mean(grp == k) for k in ks])
    m = np.array([li[grp == k].mean() for k in ks])
    v = np.array([li[grp == k].var() for k in ks])
    out["logage"] = {"within": float((w * v).sum()), "between": float((w * (m - li.mean()) ** 2).sum()), "total": float(li.var())}
    # Galton: child height within and between mid-parent rows
    x, y = galton_points()
    ks = np.unique(x)
    w = np.array([np.mean(x == k) for k in ks])
    m = np.array([y[x == k].mean() for k in ks])
    v = np.array([y[x == k].var() for k in ks])
    out["galton"] = {"within": float((w * v).sum()), "between": float((w * (m - y.mean()) ** 2).sum()),
                     "total": float(y.var()), "r2": float(np.corrcoef(x, y)[0, 1] ** 2)}
    return nest(out)


def compute_mvn():
    g = rng(7)
    z = g.normal(size=(2500, 2))
    A = np.array([[1.5, 0.0], [1.2, 0.8]])
    mu = np.array([1.0, -0.5])
    x = z @ A.T + mu
    return nest({"z": z[:1200], "x": x[:1200], "A": A, "mu": mu, "Sigma": A @ A.T, "emp": np.cov(x.T)})


def compute_regression():
    f = W.families
    son = f["son"]
    mid = ((f["father"] + f["mother"]) / 2)[son]
    ch = f["child"][son]
    q90 = np.quantile(mid, 0.9)
    top = mid >= q90
    mid_dev = float(mid[top].mean() - mid.mean())
    ch_dev = float(ch[top].mean() - ch.mean())
    # test-retest: score = skill + luck
    g = rng(1973)
    n = 10_000
    skill = g.normal(0, 1, n)
    t1 = skill + g.normal(0, 1, n)
    t2 = skill + g.normal(0, 1, n)
    best = t1 >= np.quantile(t1, 0.9)
    worst = t1 <= np.quantile(t1, 0.1)
    return nest({"mid_dev": mid_dev, "ch_dev": ch_dev, "ratio": ch_dev / mid_dev,
                 "slope": float(np.cov(mid, ch)[0, 1] / mid.var()),
                 "t1": t1[:1500], "t2": t2[:1500], "best_t1": float(t1[best].mean()), "best_t2": float(t2[best].mean()),
                 "worst_t1": float(t1[worst].mean()), "worst_t2": float(t2[worst].mean()),
                 "r12": float(np.corrcoef(t1, t2)[0, 1])})


def compute_jacobian():
    g = rng(8)
    u = g.uniform(size=(40_000, 2))
    s = u.sum(axis=1)
    z = g.normal(size=(40_000, 2))
    ratio = z[:, 0] / z[:, 1]
    return nest({"s": s[:20000], "ratio": ratio[np.abs(ratio) < 6][:20000], "u": u[:800]})


def compute_latent():
    h = W.height[W.adult]
    m = W.male[W.adult]
    xs = np.linspace(140, 205, 300)
    pm = float(m.mean())
    fm = stats.norm.pdf(xs, h[m].mean(), h[m].std())
    ff = stats.norm.pdf(xs, h[~m].mean(), h[~m].std())
    return nest({"xs": xs, "fm": pm * fm, "ff": (1 - pm) * ff, "mix": pm * fm + (1 - pm) * ff, "pm": pm,
                 "mu_m": float(h[m].mean()), "mu_f": float(h[~m].mean()), "sd_m": float(h[m].std()),
                 "sd_f": float(h[~m].std()), "hist": np.histogram(h, np.linspace(140, 205, 66), density=True)[0],
                 "edges": np.linspace(140, 205, 66), "sd_all": float(h.std())})


def compute_copulas():
    g = rng(2000)
    n = 4000
    tau = 0.5
    out = {}
    # Gaussian: rho = sin(pi tau / 2)
    rho = np.sin(np.pi * tau / 2)
    z = g.multivariate_normal([0, 0], [[1, rho], [rho, 1]], n)
    out["gauss"] = stats.norm.cdf(z)
    # Clayton: theta = 2 tau / (1 - tau); Marshall-Olkin with a gamma frailty
    th = 2 * tau / (1 - tau)
    v = g.gamma(1 / th, 1, n)
    e = g.exponential(size=(n, 2))
    out["clayton"] = (1 + e / v[:, None]) ** (-1 / th)
    # Gumbel: theta = 1 / (1 - tau); positive stable frailty (Chambers-Mallows-Stuck)
    thg = 1 / (1 - tau)
    a = 1 / thg
    U = g.uniform(0, np.pi, n)
    Ew = g.exponential(size=n)
    S = (np.sin(a * U) / np.sin(U) ** (1 / a)) * (np.sin((1 - a) * U) / Ew) ** ((1 - a) / a)
    e2 = g.exponential(size=(n, 2))
    out["gumbel"] = np.exp(-(e2 / S[:, None]) ** a)
    res = {}
    for k, uv in out.items():
        lo = float(np.mean((uv[:, 0] < 0.05) & (uv[:, 1] < 0.05)) / 0.05)
        hi = float(np.mean((uv[:, 0] > 0.95) & (uv[:, 1] > 0.95)) / 0.05)
        res[k] = {"uv": uv[:1500], "tau": float(stats.kendalltau(uv[:, 0], uv[:, 1])[0]), "lower": lo, "upper": hi}
    res["indep_tail"] = 0.05
    return nest(res)


def compute_polya():
    g = rng(1923)
    runs = []
    for _ in range(30):
        r, b = 1, 1
        frac = []
        for t in range(1000):
            if g.random() < r / (r + b):
                r += 1
            else:
                b += 1
            frac.append(r / (r + b))
        runs.append(frac[::5])
    limits = []
    for _ in range(4000):
        r, b = 1, 1
        draws = g.random(500)
        for u in draws:
            if u < r / (r + b):
                r += 1
            else:
                b += 1
        limits.append(r / (r + b))
    # exchangeability: P(R, R, B) = P(R, B, R) = P(B, R, R) = 1/12
    from fractions import Fraction as F

    def seq_p(seq):
        r, b, p = 1, 1, F(1)
        for c in seq:
            if c == "R":
                p *= F(r, r + b)
                r += 1
            else:
                p *= F(b, r + b)
                b += 1
        return p
    perms = {s: str(seq_p(s)) for s in ("RRB", "RBR", "BRR")}
    return nest({"runs": np.array(runs), "limits": np.array(limits), "perms": perms})


def dcor(x, y):
    def centred(a):
        d = np.abs(a[:, None] - a[None, :])
        return d - d.mean(axis=0) - d.mean(axis=1)[:, None] + d.mean()
    A, B = centred(x), centred(y)
    dcov = (A * B).mean()
    return float(np.sqrt(dcov / np.sqrt((A * A).mean() * (B * B).mean())))


def mutual_info(x, y, bins=12):
    h, _, _ = np.histogram2d(x, y, bins)
    p = h / h.sum()
    px, py = p.sum(axis=1, keepdims=True), p.sum(axis=0, keepdims=True)
    nz = p > 0
    return float((p[nz] * np.log(p[nz] / (px @ py)[nz])).sum())


def compute_measures():
    g = rng(2007)
    n = 500
    x = g.uniform(-1, 1, n)
    shapes = {
        "line": (x, x + 0.25 * g.normal(size=n)),
        "parabola": (x, x ** 2 + 0.08 * g.normal(size=n)),
        "circle": tuple(np.array([np.cos(t), np.sin(t)]) + 0.05 * g.normal(size=(2, n)) for t in [g.uniform(0, 2 * np.pi, n)])[0],
        "cross": (x, np.where(g.random(n) < 0.5, x, -x) + 0.05 * g.normal(size=n)),
        "step": (x, np.where(x > 0, 1.0, 0.0) + 0.15 * g.normal(size=n)),
        "noise": (x, g.normal(size=n)),
    }
    out = {}
    for k, (a, b) in shapes.items():
        out[k] = {"x": a, "y": b, "pearson": float(np.corrcoef(a, b)[0, 1]), "spearman": float(stats.spearmanr(a, b)[0]),
                  "kendall": float(stats.kendalltau(a, b)[0]), "dcor": dcor(a, b), "mi": mutual_info(a, b)}
    return nest(out)


def compute_simplex():
    g = rng(1930)
    out = {}
    for name, a in (("flat", [1, 1, 1]), ("centre", [8, 8, 8]), ("corner", [0.3, 0.3, 0.3]), ("skew", [6, 2, 1])):
        out[name] = {"alpha": a, "p": g.dirichlet(a, 1500)}
    return nest(out)


ITEMS = {
    "galton": compute_galton, "slicer": compute_slicer, "dependence": compute_dependence, "predictor": compute_predictor,
    "eve": compute_eve, "mvn": compute_mvn, "regression": compute_regression, "jacobian": compute_jacobian,
    "latent": compute_latent, "copulas": compute_copulas, "polya": compute_polya, "measures": compute_measures,
    "simplex": compute_simplex,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
