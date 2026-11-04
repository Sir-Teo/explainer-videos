"""Precompute every number in Part 9 of *Statistics, Built* ("Estimation").

    python -m videos.stats.stats9.compute            # everything missing (about a minute)
    python -m videos.stats.stats9.compute --force tanks

Results are cached in ``.cache/stats9/<name>.json``.  The tank figures and Bortkiewicz's horse kicks are the Museum's;
everything else is a seeded simulation or an exact calculation.

Items:
    tanks        one factory (N = 300, 6 captured); the sampling distributions of four estimators of N for k = 6;
                 their bias, SD and RMSE for k = 2..20; the variance against the Cramer-Rao-type 1/k^2 rate
    moments      gamma(2.5, scale 2): method of moments vs maximum likelihood over 4,000 samples of 50; one sample
    likelihood   coin: the binomial log-likelihood for 7/10, 70/100, 700/1000; horse kicks: the Poisson likelihood
    newton       Newton's iterations for the gamma shape MLE on one sample; the score curve
    examples     exponential and uniform(0, theta) likelihoods for one sample; the uniform's boundary MLE
    curvature    horse kicks: lambda-hat, observed information, SE; simulated SDs of the Poisson MLE vs 1/sqrt(n I)
    sufficiency  Bernoulli sequences of 5 with sum 2: each of the 10 equally likely, whatever p
    raoblack     P(X = 0) for Poisson: the indicator 1{X_1 = 0} vs its Rao-Blackwellization ((n - 1)/n)^S; tanks:
                 2 xbar - 1 vs the UMVUE
    cramerrao    exponential rate: Var of the MLE and of the unbiased (n - 1)/S vs the bound, n = 5..100
    board        an MSE board for the tank estimators at k = 5 under three models (uniform capture, newer tanks
                 more often captured, serials starting at 1,000)
"""

from __future__ import annotations

import numpy as np
from scipy import optimize, special, stats

from explainer.ai.cache import Cache
from explainer.stats import museum

CACHE = Cache("stats9")
load = CACHE.load


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


def tank_estimates(s: np.ndarray) -> dict:
    """Rows of captured serials -> four estimators of N."""
    k = s.shape[1]
    m = s.max(1)
    return {"mom": 2 * s.mean(1) - 1, "max": m.astype(float), "umvue": m * (1 + 1 / k) - 1,
            "gap": m + (m - k) / k,  # max plus the average gap (the same as the UMVUE: kept as the "gap" story)
            "range": (m - s.min(1)) * (k + 1) / (k - 1) - 1}  # unbiased when the serials start at an unknown offset


def capture(g, N, k, reps, weights=None, offset=0):
    if weights is None:
        return np.array([g.choice(N, k, replace=False) + 1 + offset for _ in range(reps)])
    p = weights / weights.sum()
    return np.array([g.choice(N, k, replace=False, p=p) + 1 + offset for _ in range(reps)])


def compute_tanks():
    g = rng(1943)
    N = 300
    one = np.sort(g.choice(N, 6, replace=False) + 1)
    s = capture(g, N, 6, 20000)
    est = tank_estimates(s)
    ed = np.linspace(100, 500, 81)
    out = {"N": N, "one": one, "one_est": {k: float(v[0]) for k, v in tank_estimates(one[None, :]).items()},
           "edges": ed, "hist": {k: np.histogram(v, ed, density=True)[0] for k, v in est.items()},
           "stats6": {k: {"mean": float(v.mean()), "sd": float(v.std()), "rmse": float(np.sqrt(np.mean((v - N) ** 2)))}
                      for k, v in est.items()}}
    ks = list(range(2, 21))
    curves = {k: [] for k in ("mom", "max", "umvue")}
    for k in ks:
        e = tank_estimates(capture(g, N, k, 6000))
        for name in curves:
            curves[name].append(float(np.sqrt(np.mean((e[name] - N) ** 2))))
    out["ks"] = ks
    out["rmse"] = curves
    out["umvue_sd_theory"] = [float(np.sqrt((N - k) * (N + 1) / (k * (k + 2)))) for k in ks]
    out["mom_sd_theory"] = [float(np.sqrt((N + 1) * (N - k) / (3 * k))) for k in ks]
    out["museum"] = museum.TANKS
    return nest(out)


def gamma_mle(x):
    lm = np.log(x.mean()) - np.log(x).mean()
    a = (3 - lm + np.sqrt((lm - 3) ** 2 + 24 * lm)) / (12 * lm)  # Minka's starting point
    for _ in range(50):
        a_new = a - (np.log(a) - special.digamma(a) - lm) / (1 / a - special.polygamma(1, a))
        if abs(a_new - a) < 1e-12:
            break
        a = a_new
    return a, x.mean() / a


def compute_moments():
    g = rng(1894)
    a0, sc0 = 2.5, 2.0
    x = g.gamma(a0, sc0, 50)
    m, v = x.mean(), x.var()
    mom_one = (m * m / v, v / m)
    mle_one = gamma_mle(x)
    am, al = [], []
    for _ in range(4000):
        y = g.gamma(a0, sc0, 50)
        mm, vv = y.mean(), y.var()
        am.append(mm * mm / vv)
        al.append(gamma_mle(y)[0])
    am, al = np.asarray(am), np.asarray(al)
    ed = np.linspace(0.5, 6, 56)
    xs = np.linspace(0.01, 20, 300)
    return nest({"a0": a0, "sc0": sc0, "x": x, "mean": float(m), "var": float(v), "mom": mom_one, "mle": mle_one,
                 "xs": xs, "pdf_true": stats.gamma.pdf(xs, a0, scale=sc0), "pdf_mom": stats.gamma.pdf(xs, mom_one[0], scale=mom_one[1]),
                 "pdf_mle": stats.gamma.pdf(xs, mle_one[0], scale=mle_one[1]),
                 "edges": ed, "h_mom": np.histogram(am, ed, density=True)[0], "h_mle": np.histogram(al, ed, density=True)[0],
                 "sd_mom": float(am.std()), "sd_mle": float(al.std()), "bias_mom": float(am.mean() - a0),
                 "bias_mle": float(al.mean() - a0), "hist_x": np.histogram(x, np.linspace(0, 20, 21), density=True)[0]})


def compute_likelihood():
    ps = np.linspace(0.3, 0.95, 300)
    out = {"ps": ps}
    for n in (10, 100, 1000):
        k = int(0.7 * n)
        ll = k * np.log(ps) + (n - k) * np.log(1 - ps)
        out[str(n)] = ll - ll.max()
    hk_k, hk_n = np.asarray(museum.HORSEKICK_K), np.asarray(museum.HORSEKICK_N)
    n = hk_n.sum()
    S = (hk_k * hk_n).sum()
    lams = np.linspace(0.4, 1.0, 300)
    ll = S * np.log(lams) - n * lams
    out["hk"] = {"n": int(n), "S": int(S), "lam_hat": float(S / n), "lams": lams, "ll": ll - ll.max(),
                 "se": float(np.sqrt(S / n / n)), "k": hk_k, "count": hk_n,
                 "expected": n * stats.poisson.pmf(hk_k, S / n)}
    return nest(out)


def compute_newton():
    x = np.asarray(load("moments")["x"])
    lm = np.log(x.mean()) - np.log(x).mean()
    a = x.mean() ** 2 / x.var()  # start at the method-of-moments value
    path = [a]
    for _ in range(6):
        a = a - (np.log(a) - special.digamma(a) - lm) / (1 / a - special.polygamma(1, a))
        path.append(a)
    aa = np.linspace(0.8, 6, 300)
    score = len(x) * (np.log(aa) - special.digamma(aa) - lm)
    return nest({"path": path, "aa": aa, "score": score, "lm": float(lm), "n": len(x)})


def compute_examples():
    g = rng(1922)
    x = g.exponential(2.0, 12)
    rates = np.linspace(0.1, 1.5, 300)
    ll = len(x) * np.log(rates) - rates * x.sum()
    u = np.sort(g.uniform(0, 10, 8))
    th = np.linspace(5, 16, 400)
    lik = np.where(th >= u.max(), th ** -len(u), 0.0)
    return nest({"exp_x": x, "rates": rates, "exp_ll": ll - ll.max(), "rate_hat": float(1 / x.mean()),
                 "u": u, "th": th, "u_lik": lik / lik.max(), "u_max": float(u.max())})


def compute_curvature():
    hk = load("likelihood")["hk"]
    lam = 0.7
    g = rng(1898)
    ns = [20, 50, 200, 1000]
    sims = {}
    for n in ns:
        est = g.poisson(lam, (20000, n)).mean(1)
        sims[str(n)] = {"sd": float(est.std()), "bound": float(np.sqrt(lam / n))}
    return nest({"hk": hk, "lam": lam, "sims": sims, "info": hk["S"] / hk["lam_hat"] ** 2})


def compute_sufficiency():
    from itertools import combinations
    seqs = []
    for c in combinations(range(5), 2):
        s = [0] * 5
        for i in c:
            s[i] = 1
        seqs.append(s)
    out = {"seqs": seqs}
    for p in (0.2, 0.5, 0.8):
        each = p ** 2 * (1 - p) ** 3
        out[str(p)] = {"each": each, "total": 10 * each, "cond": each / (10 * each)}
    return nest(out)


def compute_raoblack():
    g = rng(1945)
    lam, n = 0.7, 10
    x = g.poisson(lam, (20000, n))
    naive = (x[:, 0] == 0).astype(float)
    S = x.sum(1)
    rb = ((n - 1) / n) ** S
    truth = np.exp(-lam)
    tk = load("tanks")
    s = capture(g, 300, 6, 20000)
    e = tank_estimates(s)
    return nest({"truth": float(truth), "naive_mean": float(naive.mean()), "naive_sd": float(naive.std()),
                 "rb_mean": float(rb.mean()), "rb_sd": float(rb.std()), "rb_values": np.unique(np.round(rb, 4))[:12],
                 "tank_mom_sd": float(e["mom"].std()), "tank_umvue_sd": float(e["umvue"].std()), "N": tk["N"]})


def compute_cramerrao():
    g = rng(1946)
    lam = 0.5  # exponential rate
    ns = [5, 10, 20, 50, 100]
    out = {"lam": lam, "ns": ns, "mle": [], "unb": [], "bound": [], "mle_bias": []}
    for n in ns:
        S = g.exponential(1 / lam, (40000, n)).sum(1)
        mle = n / S
        unb = (n - 1) / S
        out["mle"].append(float(mle.var()))
        out["unb"].append(float(unb.var()))
        out["bound"].append(lam ** 2 / n)
        out["mle_bias"].append(float(mle.mean() - lam))
    out["unb_exact"] = [lam ** 2 / (n - 2) for n in ns]
    return nest(out)


def compute_board():
    g = rng(2024)
    N, k, R = 300, 5, 10000
    models = {}
    models["uniform"] = capture(g, N, k, R)
    w = np.linspace(1, 3, N)  # newer tanks (higher serials) at the front, captured more often
    models["newer"] = capture(g, N, k, R, weights=w)
    models["offset"] = capture(g, N, k, R, offset=1000)  # serials 1001..1300; the estimators assume they start at 1
    out = {"N": N, "k": k, "R": R, "rows": {}}
    for name, s in models.items():
        e = tank_estimates(s)
        out["rows"][name] = {m: {"bias": float(e[m].mean() - N), "sd": float(e[m].std()),
                                 "rmse": float(np.sqrt(np.mean((e[m] - N) ** 2)))} for m in ("mom", "max", "umvue", "range")}
    return nest(out)


ITEMS = {
    "tanks": compute_tanks, "moments": compute_moments, "likelihood": compute_likelihood, "newton": compute_newton,
    "examples": compute_examples, "curvature": compute_curvature, "sufficiency": compute_sufficiency,
    "raoblack": compute_raoblack, "cramerrao": compute_cramerrao, "board": compute_board,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
