"""Precompute every number in Part 13 of *Statistics, Built* ("Experiments by Design").

    python -m videos.stats.stats13.compute            # everything missing (a few minutes)
    python -m videos.stats.stats13.compute --force board

Results are cached in ``.cache/stats13/<name>.json``.  The field trials run on ``statkit.design.Field`` (a hidden
fertility surface plus plot noise); the bakery is ``statkit.design.Bakery``; the hidden-covariate check uses the
World's adults (seed 1662); Darwin's pairs are the Museum's.  Everything else is a seeded simulation.

Items:
    field       the 12 x 12 field: fertility, a systematic and a random layout, replication and pairing
    balance     the World: randomizing 200 adults balances heights and incomes nobody measured
    randinf     a 20-plot trial: the exact randomization distribution (all 184,756 allocations) vs Student's t
    anova       four fertilizers, six plots each: SS decomposition, F, ANOVA as regression, orthogonal contrasts
    contrasts   five treatments: Tukey, Scheffe, Dunnett; family-wise error of unadjusted pairwise tests
    blocking    complete blocks on a gradient: RCBD vs CRD power and efficiency; Darwin's pots
    latin       a 5 x 5 Latin square on a field graded both ways
    factorial   a 2^3 NPK trial: effects by Yates' algorithm, the half-normal plot; OFAT on the bakery
    fraction    2^(4-1) with D = ABC; 2^(7-4); a 12-run Plackett-Burman design
    rsm         the bakery: a first-order design, steepest ascent, a central composite design, the optimum
    splitplot   irrigation on whole plots, varieties on subplots: the right and the wrong error
    doptimal    quadratic regression on [-1, 1]: det M over designs, the variance function, Kiefer-Wolfowitz
    power       power curves and the minimum detectable effect
    online      an A/B test with a pre-period covariate: CUPED; sample-ratio mismatch; A/A tests
    board       Coverage Board rows (sizes of tests)
"""

from __future__ import annotations

import itertools
from dataclasses import asdict

import numpy as np
from scipy import stats

from explainer.ai.cache import Cache
from explainer.stats import museum
from explainer.stats.board import Row, save_rows
from explainer.stats.kit import design as D
from explainer.stats.kit import ols
from explainer.stats.kit.tests import sign_flip_test
from explainer.stats.world import World

CACHE = Cache("stats13")
load = CACHE.load
W = World()
R_BOARD = 10_000


def rng(seed: int) -> np.random.Generator:
    return np.random.Generator(np.random.PCG64(seed))


def nest(obj):
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    if isinstance(obj, dict):
        return {str(k): nest(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [nest(v) for v in obj]
    if isinstance(obj, (np.floating, np.integer)):
        return obj.item()
    if isinstance(obj, np.bool_):
        return bool(obj)
    return obj


# ---------------------------------------------------------------------------------------------------------------
# 1. Three principles on the big field
# ---------------------------------------------------------------------------------------------------------------
EFFECT = 2.0  # variety B yields 2 bushels more than A, on every plot


def compute_field():
    f = D.Field()
    g = rng(1919)
    uniform = f.harvest(np.zeros((12, 12)), rng=rng(1911))  # a uniformity trial: every plot treated alike
    west = np.zeros((12, 12), int)
    west[:, 6:] = 1  # systematic: A on the west half, B on the east
    y = f.harvest(EFFECT * west, rng=g)
    sys_est = y[west == 1].mean() - y[west == 0].mean()
    flip = 1 - west
    y2 = f.harvest(EFFECT * flip, rng=rng(1920))
    sys_flip = y2[flip == 1].mean() - y2[flip == 0].mean()
    # randomized: 72 of each, anywhere
    ests, layouts = [], []
    for r in range(4000):
        a = np.zeros(144, int)
        a[g.choice(144, 72, replace=False)] = 1
        a = a.reshape(12, 12)
        yy = f.harvest(EFFECT * a, rng=g)
        ests.append(yy[a == 1].mean() - yy[a == 0].mean())
        if r < 3:
            layouts.append(a)
    ests = np.array(ests)
    # replication: n plots per variety, placed at random
    rep = {}
    for n in (1, 2, 4, 8, 16, 36, 72):
        e = []
        for _ in range(3000):
            idx = g.choice(144, 2 * n, replace=False)
            a = np.zeros(144, int)
            a[idx[:n]] = 1
            yy = f.harvest(EFFECT * a.reshape(12, 12), rng=g).ravel()
            e.append(yy[idx[:n]].mean() - yy[idx[n:]].mean())
        rep[n] = float(np.std(e))
    # local control: neighbouring east-west pairs, randomized within each pair
    pair_ests = []
    for _ in range(4000):
        a = np.zeros((12, 12), int)
        coin = g.random((12, 6)) < 0.5
        a[:, 0::2] = coin
        a[:, 1::2] = ~coin
        yy = f.harvest(EFFECT * a, rng=g)
        pair_ests.append(yy[a == 1].mean() - yy[a == 0].mean())
    pair_ests = np.array(pair_ests)
    return nest({"fertility": f.fertility, "uniform": uniform, "sys_y": y, "sys_est": sys_est, "sys_flip": sys_flip,
                 "rand_mean": ests.mean(), "rand_sd": ests.std(), "rand_ests": ests[:400], "layouts": layouts,
                 "replication": rep, "pair_mean": pair_ests.mean(), "pair_sd": pair_ests.std(),
                 "uniform_cv": uniform.std() / uniform.mean()})


# ---------------------------------------------------------------------------------------------------------------
# 2. Randomization as inference
# ---------------------------------------------------------------------------------------------------------------
def compute_balance():
    idx = W.sample(200, among=W.adult, seed=13)
    h, inc = W.height[idx], W.income[idx]
    g = rng(1884)
    dh, di = [], []
    for _ in range(5000):
        a = np.zeros(200, bool)
        a[g.choice(200, 100, replace=False)] = True
        dh.append(h[a].mean() - h[~a].mean())
        di.append(inc[a].mean() - inc[~a].mean())
    dh, di = np.array(dh), np.array(di)
    # one doctor who gives the treatment to the 100 tallest
    srt = np.argsort(h)
    chosen = np.zeros(200, bool)
    chosen[srt[100:]] = True
    return nest({"dh": dh[:1500], "di": di[:1500], "sd_h": dh.std(), "sd_i": di.std(), "big_h": np.mean(np.abs(dh) > 2 * dh.std()),
                 "chosen_h": h[chosen].mean() - h[~chosen].mean(), "h": h, "inc": inc})


def compute_randinf():
    f = D.Field(rows=4, cols=5, gradient=3.0, hump=2.0, noise=2.0, seed=1926)
    g = rng(1935)
    a = np.zeros(20, int)
    a[g.choice(20, 10, replace=False)] = 1
    a = a.reshape(4, 5)
    y = f.harvest(3.0 * a, rng=g).ravel()
    treat = a.ravel() == 1
    obs = y[treat].mean() - y[~treat].mean()
    combos = np.array(list(itertools.combinations(range(20), 10)))
    tot = y.sum()
    s_a = y[combos].sum(1)
    null = s_a / 10 - (tot - s_a) / 10
    p_exact = float(np.mean(np.abs(null) >= abs(obs) - 1e-12))
    t = stats.ttest_ind(y[treat], y[~treat])
    hist, edges = np.histogram(null, bins=60)
    return nest({"y": y.reshape(4, 5), "alloc": a, "obs": obs, "n_alloc": len(combos), "p_exact": p_exact,
                 "count": int(np.sum(np.abs(null) >= abs(obs) - 1e-12)), "t": t.statistic, "p_t": t.pvalue,
                 "hist": hist, "edges": edges, "null_sd": null.std()})


# ---------------------------------------------------------------------------------------------------------------
# 3-4. ANOVA and contrasts
# ---------------------------------------------------------------------------------------------------------------
FERT = ["none", "N", "P", "NPK"]
FERT_EFFECT = [0.0, 3.0, 1.0, 4.5]


def compute_anova():
    f = D.Field(rows=4, cols=6, gradient=0.0, hump=0.0, noise=2.0, seed=1923)
    g = rng(1925)
    alloc = g.permutation(np.repeat(np.arange(4), 6)).reshape(4, 6)
    y = f.harvest(np.array(FERT_EFFECT)[alloc], rng=g)
    groups = [y[alloc == k] for k in range(4)]
    a = D.oneway(groups)
    # ANOVA as regression on dummies
    X = np.column_stack([np.ones(24)] + [(alloc.ravel() == k).astype(float) for k in (1, 2, 3)])
    r = ols.fit(X, y.ravel())
    full_rss, null_rss = r.rss, float(((y - y.mean()) ** 2).sum())
    # orthogonal contrasts
    C = {"fertilized vs none": [-3, 1, 1, 1], "N vs P, NPK": [0, -2, 1, 1], "P vs NPK": [0, 0, -1, 1]}
    means = np.array(a["means"])
    cs = {}
    for name, c in C.items():
        c = np.array(c, float)
        est = float(c @ means)
        ss = est ** 2 / (c ** 2 / 6).sum()
        cs[name] = {"c": c, "est": est, "ss": ss, "F": ss / a["mse"], "p": float(stats.f.sf(ss / a["mse"], 1, 20))}
    fx = np.linspace(0.01, 12, 300)
    return nest({"y": y, "alloc": alloc, "groups": groups, "anova": a, "coef": r.coef, "r2": r.r2, "rss": full_rss,
                 "tss": null_rss, "contrasts": cs, "f_x": fx, "f_pdf": stats.f.pdf(fx, 3, 20), "f_crit": stats.f.ppf(0.95, 3, 20)})


def compute_contrasts():
    g = rng(1953)
    eff = [0.0, 1.0, 4.0, 4.5, 2.0]
    names = ["control", "A", "B", "C", "D"]
    groups = [g.normal(50 + e, 2.0, 6) for e in eff]
    a = D.oneway(groups)
    tk = D.tukey_hsd(groups)
    res = stats.tukey_hsd(*groups)
    pairs = []
    for i, j in itertools.combinations(range(5), 2):
        pairs.append({"i": i, "j": j, "diff": float(np.mean(groups[j]) - np.mean(groups[i])), "p_tukey": float(res.pvalue[i, j]),
                      "p_raw": float(stats.ttest_ind(groups[i], groups[j]).pvalue),
                      "sig": abs(np.mean(groups[j]) - np.mean(groups[i])) > tk["hsd"]})
    dn = stats.dunnett(*groups[1:], control=groups[0])
    t_crit = float(stats.t.ppf(0.975, a["dfw"]))
    # Dunnett's two-sided 95% multiplier for 4 comparisons with a control, 25 df, by simulation (400,000 draws)
    gd = rng(1955)
    z = gd.standard_normal((400_000, 5))
    s_ = np.sqrt(gd.chisquare(25, 400_000) / 25)
    dmax = np.abs(z[:, 1:] - z[:, [0]]).max(1) / (np.sqrt(2) * s_)
    dunnett_mult = float(np.quantile(dmax, 0.95))
    return nest({"names": names, "eff": eff, "means": a["means"], "mse": a["mse"], "q": tk["q"], "hsd": tk["hsd"], "pairs": pairs,
                 "dunnett_p": dn.pvalue, "t_crit": t_crit, "scheffe": D.scheffe_multiplier(5, a["dfw"]),
                 "tukey_mult": tk["q"] / np.sqrt(2), "bonf": float(stats.t.ppf(1 - 0.025 / 10, a["dfw"])), "dunnett_mult": dunnett_mult})


# ---------------------------------------------------------------------------------------------------------------
# 5-6. Blocking, Latin squares
# ---------------------------------------------------------------------------------------------------------------
def compute_blocking():
    f = D.Field(rows=4, cols=6, gradient=8.0, hump=0.0, noise=1.5, seed=1937)
    eff = np.array([0.0, 2.0, 3.0, 1.5])
    g = rng(1857)
    rej_rcbd = rej_crd = 0
    mse_rcbd, mse_crd = [], []
    reps = 4000
    ex_alloc = None
    for r in range(reps):
        # RCBD: each column a block of 4, treatments shuffled within it
        alloc = np.column_stack([g.permutation(4) for _ in range(6)])
        y = f.harvest(eff[alloc], rng=g)
        yt = np.array([[y[alloc[:, b] == t, b][0] for b in range(6)] for t in range(4)])
        rb = D.rcbd(yt)
        rej_rcbd += rb["p"] < 0.05
        mse_rcbd.append(rb["mse"])
        # CRD: the same field, treatments shuffled over all 24 plots, analysed one-way
        alloc2 = g.permutation(np.repeat(np.arange(4), 6)).reshape(4, 6)
        y2 = f.harvest(eff[alloc2], rng=g)
        a = D.oneway([y2[alloc2 == t] for t in range(4)])
        rej_crd += a["p"] < 0.05
        mse_crd.append(a["mse"])
        if ex_alloc is None and 0.005 < rb["p"] < 0.03:  # a typical run of a design with 74% power
            ex_alloc, ex_y, ex_rcbd = alloc, y, rb
            ex_oneway = D.oneway([y[alloc == t] for t in range(4)])
    zea = np.array(museum.DARWIN_ZEA, float)
    sf = sign_flip_test(zea)
    t = stats.ttest_1samp(zea, 0)
    return nest({"fertility": f.fertility, "alloc": ex_alloc, "y": ex_y, "rcbd": ex_rcbd, "ignore": ex_oneway,
                 "power_rcbd": rej_rcbd / reps, "power_crd": rej_crd / reps, "mse_rcbd": np.mean(mse_rcbd), "mse_crd": np.mean(mse_crd),
                 "zea": zea, "zea_mean": zea.mean(), "zea_t": t.statistic, "zea_p": t.pvalue, "zea_count": sf["count"],
                 "zea_total": sf["total"], "zea_p_perm": sf["p"]})


def compute_latin():
    g = rng(1925)
    n = 5
    r_, c_ = np.meshgrid(np.arange(n), np.arange(n), indexing="ij")
    fert = 50 + 1.6 * c_ + 1.2 * r_  # graded east-west and north-south
    eff = np.array([0.0, 1.5, 2.5, 1.0, 3.0])
    sq = D.latin_square(n, g)
    y = fert + eff[sq] + 1.0 * g.standard_normal((n, n))
    la = D.latin_anova(y, sq)
    ow = D.oneway([y[sq == k] for k in range(n)])
    rej_l = rej_c = 0
    reps = 4000
    for _ in range(reps):
        s = D.latin_square(n, g)
        yy = fert + eff[s] + g.standard_normal((n, n))
        rej_l += D.latin_anova(yy, s)["p"] < 0.05
        a2 = g.permutation(np.repeat(np.arange(n), n)).reshape(n, n)
        yy2 = fert + eff[a2] + g.standard_normal((n, n))
        rej_c += D.oneway([yy2[a2 == k] for k in range(n)])["p"] < 0.05
    # a Knut Vik square: the systematic "knight's move" layout
    vik = (np.arange(n)[:, None] * 2 + np.arange(n)[None, :]) % n
    return nest({"square": sq, "y": y, "latin": la, "oneway": ow, "power_latin": rej_l / reps, "power_crd": rej_c / reps,
                 "fert": fert, "vik": vik, "n_squares_5": 161280})


# ---------------------------------------------------------------------------------------------------------------
# 7-9. Factorials, fractions, response surfaces
# ---------------------------------------------------------------------------------------------------------------
def compute_factorial():
    g = rng(1937)
    X = D.full_factorial(3)  # A = N, B = P, C = K, standard order
    true = {"N": 6.0, "P": 2.0, "K": 0.5, "NP": 2.0, "NK": 0.0, "PK": 0.0, "NPK": 0.0}

    def mean_y(x):
        n, p, k = x
        return 40 + (true["N"] * n + true["P"] * p + true["K"] * k + true["NP"] * n * p) / 2

    mu = np.array([mean_y(x) for x in X])
    y1 = mu + 1.5 * g.standard_normal(8)
    y2 = mu + 1.5 * g.standard_normal(8)
    y = (y1 + y2) / 2  # two replicates, averaged per treatment combination
    yt = D.yates(y)
    eff = D.factorial_effects(X, y, names="NPK")
    s2 = float(((y1 - y2) ** 2).sum() / (2 * 8))  # pooled within-cell variance (1 df per cell)
    se_eff = float(np.sqrt(4 * s2 / 16))
    names = ["N", "P", "NP", "K", "NK", "PK", "NPK"]
    yates_eff = {nm: float(v / 4) for nm, v in zip(names, yt[1:])}
    # half-normal plot of |effects|
    absv = sorted([(abs(v), k) for k, v in eff.items()])
    hq = stats.halfnorm.ppf((np.arange(1, 8) - 0.5) / 7)
    # OFAT on the bakery's true surface, starting at 180 C and 20 minutes
    temps, times = np.linspace(160, 240, 81), np.linspace(10, 50, 81)
    t0 = 20.0
    q1 = D.Bakery.truth(temps, t0)
    best_temp = float(temps[np.argmax(q1)])
    q2 = D.Bakery.truth(best_temp, times)
    best_time = float(times[np.argmax(q2)])
    ofat = {"start": [180.0, t0], "after_temp": [best_temp, t0], "after_time": [best_temp, best_time],
            "quality": float(D.Bakery.truth(best_temp, best_time)), "q_start": float(D.Bakery.truth(180, t0)), "optimum": 85.0}
    # efficiency: 8 runs as a factorial vs as OFAT (baseline + 3 one-change runs, each twice)
    return nest({"X": X, "y1": y1, "y2": y2, "y": y, "yates": yt, "effects": eff, "yates_eff": yates_eff, "se": se_eff, "s2": s2,
                 "true": true, "halfnorm": {"abs": [a for a, _ in absv], "names": [k for _, k in absv], "q": hq}, "ofat": ofat})


def compute_fraction():
    true = {"A": 4.0, "B": 0.0, "C": 2.0, "D": 3.0, "AB": 1.5, "CD": 0.0, "ABC": 0.0, "BCD": 0.0}
    g = rng(1945)

    def response(X):
        A, B, C, Dd = X.T
        return 60 + (true["A"] * A + true["C"] * C + true["D"] * Dd + true["AB"] * A * B) / 2

    Xf = D.full_factorial(4)
    yf = response(Xf) + 1.0 * g.standard_normal(16)
    Xh = D.fraction(4, {"D": "ABC"})
    # the half fraction's runs are those full-factorial runs with ABCD = +1
    keep = np.prod(Xf, axis=1) == 1
    yh = yf[keep]
    Xh = Xf[keep]
    ef = D.factorial_effects(Xf, yf, names="ABCD")
    eh = D.factorial_effects(Xh, yh, names="ABCD")
    al = {w: D.aliases(w, ["ABCD"])[0] for w in ["A", "B", "C", "D", "AB", "AC", "AD"]}
    pb_row = [1, 1, -1, 1, 1, 1, -1, -1, -1, 1, -1]
    pb = np.array([np.roll(pb_row, k) for k in range(11)] + [[-1] * 11])
    sat = D.fraction(7, {"D": "AB", "E": "AC", "F": "BC", "G": "ABC"})
    return nest({"Xf": Xf, "yf": yf, "keep": keep, "Xh": Xh, "yh": yh, "full": ef, "half": eh, "aliases": al, "true": true,
                 "pb": pb, "pb_orth": bool(np.allclose(pb.T @ pb, 12 * np.eye(11))), "sat": sat})


def compute_rsm():
    b = D.Bakery(noise=1.5, seed=1951)
    g = rng(1951)
    c0 = np.array([185.0, 22.0])
    step = np.array([8.0, 3.0])
    # phase 1: a 2^2 factorial with three centre points
    F = np.array([[-1, -1], [1, -1], [-1, 1], [1, 1], [0, 0], [0, 0], [0, 0]], float)
    pts = c0 + F * step
    y = b.bake(pts[:, 0], pts[:, 1], rng=g)
    X = np.column_stack([np.ones(7), F])
    r1 = ols.fit(X, y)
    curv = float(y[:4].mean() - y[4:].mean())
    grad = r1.coef[1:]
    direction = grad / np.linalg.norm(grad)
    # phase 2: steepest ascent in coded units, one unit per step
    path = [c0 + k * direction * step for k in range(0, 9)]
    path = np.array(path)
    ypath = b.bake(path[:, 0], path[:, 1], rng=g)
    kbest = int(np.argmax(ypath))
    c1 = path[kbest]
    # phase 3: a central composite design at the new centre (factorial, axial at sqrt 2, five centres)
    step2 = np.array([8.0, 3.0])
    al = np.sqrt(2)
    C = np.array([[-1, -1], [1, -1], [-1, 1], [1, 1], [-al, 0], [al, 0], [0, -al], [0, al], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]])
    pts2 = c1 + C * step2
    y2 = b.bake(pts2[:, 0], pts2[:, 1], rng=g)
    u, v = C.T
    X2 = np.column_stack([np.ones(len(u)), u, v, u * u, v * v, u * v])
    r2 = ols.fit(X2, y2)
    b0, b1, b2, b11, b22, b12 = r2.coef
    Bm = np.array([[b11, b12 / 2], [b12 / 2, b22]])
    xs = -0.5 * np.linalg.solve(Bm, [b1, b2])
    stat_pt = c1 + xs * step2
    eig = np.linalg.eigvalsh(Bm)
    return nest({"c0": c0, "step": step, "pts": pts, "y": y, "coef1": r1.coef, "curv": curv, "dir": direction, "path": path,
                 "ypath": ypath, "kbest": kbest, "c1": c1, "step2": step2, "pts2": pts2, "y2": y2, "coef2": r2.coef,
                 "stationary": stat_pt, "pred_max": float(b0 + 0.5 * np.dot([b1, b2], xs)), "eig": eig,
                 "truth_at": float(D.Bakery.truth(*stat_pt)), "runs": 7 + 9 + 13})


# ---------------------------------------------------------------------------------------------------------------
# 10. Split plots
# ---------------------------------------------------------------------------------------------------------------
def splitplot_once(g, blocks=4, a_eff=0.0, sw=2.0, se=1.0, b_eff=(0.0, 0.5, 1.0, 0.0)):
    """Irrigation (2 levels) on whole plots, 4 varieties on subplots, ``blocks`` blocks: y[block, irrigation, variety]."""
    bl = g.normal(0, 1.0, blocks)[:, None, None]
    w = g.normal(0, sw, (blocks, 2))[:, :, None]
    A = np.array([0.0, a_eff])[None, :, None]
    B = np.array(b_eff)[None, None, :]
    y = 50 + bl + A + w + B + g.normal(0, se, (blocks, 2, 4))
    return y


def splitplot_tests(y):
    b, a, v = y.shape
    gm = y.mean()
    ya = y.mean((0, 2))
    yb = y.mean((1, 2))
    yba = y.mean(2)
    ss_a = b * v * ((ya - gm) ** 2).sum()
    ss_blk = a * v * ((yb - gm) ** 2).sum()
    ss_wp = v * ((yba - gm) ** 2).sum() - ss_a - ss_blk  # block x irrigation: the whole-plot error
    df_wp = (b - 1) * (a - 1)
    f_right = (ss_a / (a - 1)) / (ss_wp / df_wp)
    p_right = stats.f.sf(f_right, a - 1, df_wp)
    # wrong: a two-factor CRD (irrigation, variety, interaction), every plot independent
    yav = y.mean(0)
    ss_cells = b * ((yav - gm) ** 2).sum()
    sse = ((y - gm) ** 2).sum() - ss_cells
    df_e = b * a * v - a * v
    f_wrong = (ss_a / (a - 1)) / (sse / df_e)
    p_wrong = stats.f.sf(f_wrong, a - 1, df_e)
    return {"F_right": f_right, "p_right": p_right, "df_wp": df_wp, "F_wrong": f_wrong, "p_wrong": p_wrong, "df_e": df_e,
            "ms_wp": ss_wp / df_wp, "ms_e": sse / df_e}


def compute_splitplot():
    g = rng(1937)
    y = splitplot_once(g, a_eff=2.0)
    ex = splitplot_tests(y)
    return nest({"y": y, "example": ex})


# ---------------------------------------------------------------------------------------------------------------
# 11. Optimal design
# ---------------------------------------------------------------------------------------------------------------
def compute_doptimal():
    designs = {
        "thirds": [-1, 0, 1],
        "uniform 5": list(np.linspace(-1, 1, 5)),
        "uniform 21": list(np.linspace(-1, 1, 21)),
        "ends heavy": [-1, -1, 0, 1, 1],
        "inner": [-0.5, 0, 0.5],
    }
    dets = {k: D.d_criterion(v) for k, v in designs.items()}
    xs = np.linspace(-1, 1, 201)

    def varfun(pts):
        Xd = np.vander(np.asarray(pts, float), 3, increasing=True)
        Mi = np.linalg.inv(Xd.T @ Xd / len(pts))
        F = np.vander(xs, 3, increasing=True)
        return np.einsum("ij,jk,ik->i", F, Mi, F)

    vf = {k: varfun(v) for k, v in designs.items()}
    # det along two families: middle point position, and the weight on the ends
    mids = np.linspace(-0.9, 0.9, 181)
    det_mid = [D.d_criterion([-1, m, 1]) for m in mids]
    ws = np.linspace(0.02, 0.48, 185)

    def det_w(w):
        M = w * np.outer([1, -1, 1], [1, -1, 1]) + w * np.outer([1, 1, 1], [1, 1, 1]) + (1 - 2 * w) * np.outer([1, 0, 0], [1, 0, 0])
        return float(np.linalg.det(M))

    det_ws = [det_w(w) for w in ws]
    # straight-line regression: half at each end
    return nest({"designs": designs, "dets": dets, "xs": xs, "varfun": vf, "mids": mids, "det_mid": det_mid, "ws": ws, "det_ws": det_ws,
                 "best_w": float(ws[int(np.argmax(det_ws))])})


# ---------------------------------------------------------------------------------------------------------------
# 12. Power
# ---------------------------------------------------------------------------------------------------------------
def compute_power():
    ns = np.arange(2, 81)
    out = {}
    for name, sigma in (("crd", 4.0), ("blocked", 2.0)):
        delta = 2.5  # 5% of a 50-bushel yield
        d = delta / sigma
        df = 2 * ns - 2
        nc = d * np.sqrt(ns / 2)
        tc = stats.t.ppf(0.975, df)
        pw = stats.nct.sf(tc, df, nc) + stats.nct.cdf(-tc, df, nc)
        n80 = int(ns[np.argmax(pw >= 0.8)])
        out[name] = {"sigma": sigma, "d": d, "power": pw, "n80": n80}
    mde_n = np.arange(5, 201)
    mde_v = [D.mde(int(n), 4.0) for n in mde_n]
    cohen = {"small": 0.2, "medium": 0.5, "large": 0.8}
    n_cohen = {k: int(np.ceil(2 * ((stats.norm.ppf(0.975) + stats.norm.ppf(0.8)) / d) ** 2)) for k, d in cohen.items()}
    # the winner's curse: among significant results, how much is the effect exaggerated? (true 2.5, sigma 4)
    g = rng(2014)
    curse = {}
    for n in (5, 10, 20, 42, 80):
        a = g.normal(0, 4, (20_000, n))
        b = g.normal(2.5, 4, (20_000, n))
        est = b.mean(1) - a.mean(1)
        se = np.sqrt(a.var(1, ddof=1) / n + b.var(1, ddof=1) / n)
        sig = np.abs(est / se) > stats.t.ppf(0.975, 2 * n - 2)
        curse[n] = {"power": float(sig.mean()), "ratio": float(np.mean(np.abs(est[sig])) / 2.5),
                    "wrong_sign": float(np.mean(est[sig] < 0))}
    g2 = rng(2015)
    a = g2.normal(0, 4, (300, 10))
    b = g2.normal(2.5, 4, (300, 10))
    est10 = b.mean(1) - a.mean(1)
    se10 = np.sqrt(a.var(1, ddof=1) / 10 + b.var(1, ddof=1) / 10)
    sig10 = np.abs(est10 / se10) > stats.t.ppf(0.975, 18)
    return nest({"ns": ns, "curves": out, "mde_n": mde_n, "mde": mde_v, "cohen": cohen, "n_cohen": n_cohen,
                 "mde_20": D.mde(20, 4.0), "mde_80": D.mde(80, 4.0), "curse": curse, "est10": est10, "sig10": sig10})


# ---------------------------------------------------------------------------------------------------------------
# 13. Online experiments
# ---------------------------------------------------------------------------------------------------------------
def ab_sample(g, n, effect):
    x = g.normal(10, 4, n)  # last month's spend
    t = g.random(n) < 0.5
    y = 2 + 0.8 * x + g.normal(0, 2.4, n) + effect * t
    return x, y, t


def ab_analyse(x, y, t):
    plain = y[t].mean() - y[~t].mean()
    se_p = np.sqrt(y[t].var(ddof=1) / t.sum() + y[~t].var(ddof=1) / (~t).sum())
    adj, theta = D.cuped(y, x)
    cup = adj[t].mean() - adj[~t].mean()
    se_c = np.sqrt(adj[t].var(ddof=1) / t.sum() + adj[~t].var(ddof=1) / (~t).sum())
    return plain, se_p, cup, se_c, theta


def compute_online():
    g = rng(2013)
    x, y, t = ab_sample(g, 20_000, 0.15)
    plain, se_p, cup, se_c, theta = ab_analyse(x, y, t)
    rho = float(np.corrcoef(x, y)[0, 1])
    reps = []
    for _ in range(2000):
        xx, yy, tt = ab_sample(g, 20_000, 0.15)
        p_, _, c_, _, _ = ab_analyse(xx, yy, tt)
        reps.append((p_, c_))
    reps = np.array(reps)
    srm = {"a": 50_000, "b": 50_820, "p": D.srm_test(50_000, 50_820)}
    show = g.choice(20_000, 400, replace=False)
    return nest({"plain": plain, "se_plain": se_p, "cuped": cup, "se_cuped": se_c, "theta": theta, "rho": rho,
                 "z_plain": plain / se_p, "z_cuped": cup / se_c, "p_plain": 2 * stats.norm.sf(abs(plain / se_p)),
                 "p_cuped": 2 * stats.norm.sf(abs(cup / se_c)), "sd_plain": reps[:, 0].std(), "sd_cuped": reps[:, 1].std(),
                 "reps": reps[:600], "srm": srm, "x_show": x[show], "y_show": y[show], "t_show": t[show],
                 "users_equiv": float(1 / (1 - rho ** 2))})


# ---------------------------------------------------------------------------------------------------------------
# The Board
# ---------------------------------------------------------------------------------------------------------------
def compute_board():
    g = rng(13_000)
    res = {}
    R = R_BOARD
    # 1. the randomization test on a 10 + 10 trial with skewed (exponential) plot errors
    rej = 0
    perms = 999
    for _ in range(R):
        y = g.exponential(1.0, 20)
        a = np.zeros(20, bool)
        a[:10] = True
        obs = y[a].mean() - y[~a].mean()
        idx = np.argsort(g.random((perms, 20)), axis=1)
        ya = y[idx[:, :10]].mean(1) - y[idx[:, 10:]].mean(1)
        p = (1 + np.sum(np.abs(ya) >= abs(obs) - 1e-12)) / (perms + 1)
        rej += p <= 0.05
    res["perm"] = rej / R
    # 2. Student's t on a systematic layout (A west, B east) of the gradient field, no real difference
    f = D.Field()
    west = np.zeros((12, 12), bool)
    west[:, 6:] = True
    sub = np.zeros((12, 12), bool)
    sub[::3, ::2] = True  # 24 plots, 12 on each side
    rej = 0
    for _ in range(R):
        y = f.harvest(np.zeros((12, 12)), rng=g)
        rej += stats.ttest_ind(y[sub & west], y[sub & ~west]).pvalue < 0.05
    res["sys"] = rej / R
    # 3-4. five groups of 6 under the null: any unadjusted pairwise t at 5% vs Tukey's HSD
    q = float(stats.studentized_range.ppf(0.95, 5, 25))
    tc = float(stats.t.ppf(0.975, 25))
    raw = tk = 0
    for _ in range(R):
        Y = g.normal(size=(5, 6))
        m = Y.mean(1)
        mse = ((Y - m[:, None]) ** 2).sum() / 25
        d = np.abs(m[:, None] - m[None, :])
        raw += np.any(d > tc * np.sqrt(2 * mse / 6))
        tk += np.any(d > q * np.sqrt(mse / 6))
    res["raw"], res["tukey"] = raw / R, tk / R
    # 5-6. a split plot with no irrigation effect, analysed both ways
    wrong = right = 0
    for _ in range(R):
        t = splitplot_tests(splitplot_once(g, a_eff=0.0))
        wrong += t["p_wrong"] < 0.05
        right += t["p_right"] < 0.05
    res["sp_wrong"], res["sp_right"] = wrong / R, right / R
    # 7. A/A tests with CUPED, 2,000 users each
    rej = 0
    for _ in range(R):
        x, y, t = ab_sample(g, 2000, 0.0)
        _, _, c_, se_c, _ = ab_analyse(x, y, t)
        rej += abs(c_ / se_c) > 1.959964
    res["cuped"] = rej / R
    rows = [
        Row(13, r"randomization test", r"10 + 10 plots, \ skewed errors", "size", 0.05, res["perm"], R),
        Row(13, r"$t$-test, \ systematic layout", r"west vs east, \ fertility gradient", "size", 0.05, res["sys"], R),
        Row(13, r"pairwise $t$-tests, \ unadjusted", r"5 groups, \ any of 10 pairs", "size", 0.05, res["raw"], R),
        Row(13, r"Tukey's HSD", r"5 groups, \ any of 10 pairs", "size", 0.05, res["tukey"], R),
        Row(13, r"split plot as a CRD", r"whole-plot factor, \ 4 blocks", "size", 0.05, res["sp_wrong"], R),
        Row(13, r"split plot, \ whole-plot error", r"whole-plot factor, \ 4 blocks", "size", 0.05, res["sp_right"], R),
        Row(13, r"CUPED $z$-test", r"A/A, \ 2{,}000 users", "size", 0.05, res["cuped"], R),
    ]
    save_rows(13, rows)
    return {"rows": [asdict(r) | {"verdict": r.verdict, "se": r.se} for r in rows]}


ITEMS = {
    "field": compute_field, "balance": compute_balance, "randinf": compute_randinf, "anova": compute_anova,
    "contrasts": compute_contrasts, "blocking": compute_blocking, "latin": compute_latin, "factorial": compute_factorial,
    "fraction": compute_fraction, "rsm": compute_rsm, "splitplot": compute_splitplot, "doptimal": compute_doptimal,
    "power": compute_power, "online": compute_online, "board": compute_board,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
