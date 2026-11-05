"""Precompute every number in Part 22 of *Statistics, Built* ("Likelihood in Depth").

    python -m videos.stats.stats22.compute            # everything missing (a few minutes)
    python -m videos.stats.stats22.compute --force board

Results are cached in ``.cache/stats22/<name>.json``.  Weldon's crabs and Bortkiewicz's horse kicks are the Museum's;
incomes are the World's; the rest are seeded simulations.

Items:
    crabs       EM for the crabs: the path, the log likelihood, the rate; Pearson's moment solutions; SEs
    consistency average log likelihood curves for Poisson samples of growing size, against the expected curve
    asymp       the Cauchy location MLE vs the median over many samples: the CLT for the MLE
    efron       observed vs expected information for the Cauchy (Efron & Hinkley 1978)
    gamma       a two-parameter gamma likelihood for the World's incomes: contours, ridge, profile and Wald intervals
    trinity     Wald, score and LR for 14 successes in 20 trials
    hauck       the Hauck-Donner effect: the Wald z shrinks as the logistic slope grows
    neyman      Neyman-Scott pairs: the MLE of sigma^2 converges to half the truth
    kl          a log-normal fitted to the World's incomes: the KL projection and the tail it misses
    sandwich    Poisson regression of overdispersed counts: model, sandwich and quasi SEs
    misbehave   the crab likelihood as one component collapses onto a point; label switching
    ising       an Ising lattice and Besag's pseudo-likelihood
    principle   binomial vs negative-binomial stopping for 9 heads and 3 tails
    board       Coverage Board rows
"""

from __future__ import annotations

from dataclasses import asdict

import numpy as np
from scipy import stats

from explainer.ai.cache import Cache
from explainer.stats import museum
from explainer.stats.board import Row, save_rows
from explainer.stats.kit import mle as M
from explainer.stats.world import World

CACHE = Cache("stats22")
load = CACHE.load
W = World()
START = [0.5, 0.6343, 0.0190, 0.6551, 0.0121]  # mixdist's starting values for these data


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
    if isinstance(obj, float) and not np.isfinite(obj):
        return None
    return obj


def compute_crabs():
    x, w = museum.crabs()
    em = M.em_mixture(x, START, w=w, iters=5000, tol=1e-13)
    th = em["theta"]
    H = M.numerical_hessian(lambda t: M.mix_loglik(x, t, w), th, h=1e-5)
    se = np.sqrt(np.diag(np.linalg.inv(-H)))
    pm = M.pearson_moments(x, w)
    one_mu = (w @ x) / w.sum()
    one_sd = np.sqrt((w @ (x - one_mu) ** 2) / w.sum())
    ll_one = float(np.sum(w * stats.norm.logpdf(x, one_mu, one_sd)))
    grid = np.linspace(0.575, 0.70, 400)
    dens = th[0] * stats.norm.pdf(grid, th[1], th[2]) + (1 - th[0]) * stats.norm.pdf(grid, th[3], th[4])
    keep = [0, 1, 2, 3, 5, 10, 20, 50, 100, 200, 400, 800, len(em["path"]) - 1]
    return nest({"x": x, "w": w, "theta": th, "se": se, "loglik": em["loglik"], "iters": len(em["loglik"]) - 1,
                 "rate": em["rate"], "path_keep": keep, "path": em["path"][keep], "resp": em["resp"],
                 "pearson": pm["solutions"], "sixth": pm["sixth"], "sixth_data": pm["sixth_data"],
                 "ll_pearson": [M.mix_loglik(x, s_, w) for s_ in pm["solutions"]], "one": [one_mu, one_sd], "ll_one": ll_one,
                 "grid": grid, "dens": dens, "comp1": th[0] * stats.norm.pdf(grid, th[1], th[2]),
                 "comp2": (1 - th[0]) * stats.norm.pdf(grid, th[3], th[4])})


def compute_consistency():
    lam0 = float(np.dot(museum.HORSEKICK_K, museum.HORSEKICK_N) / np.sum(museum.HORSEKICK_N))
    stream = rng(4).poisson(lam0, 10000)  # one growing sample: its first 10, 100, 1,000 and 10,000 draws
    th = np.linspace(0.05, 2.0, 300)
    curves = {}
    for n in (10, 100, 1000, 10000):
        x = stream[:n]
        s = x.sum()
        curves[str(n)] = {"ll": (s * np.log(th) - n * th) / n, "argmax": float(x.mean())}
    expected = lam0 * np.log(th) - th
    return nest({"lam0": lam0, "theta": th, "curves": curves, "expected": expected})


def compute_asymp():
    g = rng(1922)
    n, R = 50, 4000
    mles, meds = [], []
    for _ in range(R):
        x = g.standard_cauchy(n)
        mles.append(M.cauchy_mle(x))
        meds.append(float(np.median(x)))
    return nest({"n": n, "R": R, "mle": np.asarray(mles)[:1500], "med": np.asarray(meds)[:1500], "sd_mle": float(np.std(mles)),
                 "sd_med": float(np.std(meds)), "theory_mle": float(np.sqrt(2 / n)), "theory_med": float(np.pi / (2 * np.sqrt(n)))})


def compute_efron():
    g = rng(1978)
    n, R = 20, 8000
    t, J = [], []
    for _ in range(R):
        x = g.standard_cauchy(n)
        m = M.cauchy_mle(x)
        t.append(m)
        J.append(M.cauchy_observed_info(x, m))
    t, J = np.asarray(t), np.asarray(J)
    q = np.quantile(J, [0, 0.25, 0.5, 0.75, 1.0])
    bins = []
    for k in range(4):
        m = (J >= q[k]) & (J <= q[k + 1])
        bins.append({"J": float(J[m].mean()), "var": float(np.var(t[m])), "inv_J": float(np.mean(1 / J[m]))})
    return nest({"n": n, "R": R, "expected_var": 2 / n, "bins": bins, "J_q": q, "overall_var": float(np.var(t))})


def compute_gamma():
    idx = W.sample(150, among=W.adult, seed=2201)
    x = W.income[idx] / 1000
    x = x[x < 300]  # the Pareto tail is part of chapter ten's story; keep the body here
    a_grid = np.linspace(0.8, 4.5, 140)
    b_grid = np.linspace(0.01, 0.12, 140)
    ll = np.array([[M.gamma_loglik(x, a, b) for a in a_grid] for b in b_grid])
    pr = M.gamma_profile(x, np.linspace(0.8, 4.5, 3701))
    a_hat, b_hat = pr["a_hat"], pr["rate_hat"]
    H = M.numerical_hessian(lambda t: M.gamma_loglik(x, t[0], t[1]), [a_hat, b_hat])
    se = np.sqrt(np.diag(np.linalg.inv(-H)))
    cut = pr["profile"].max() - stats.chi2.ppf(0.95, 1) / 2
    inside = pr["shapes"][pr["profile"] >= cut]
    corr = float(np.linalg.inv(-H)[0, 1] / (se[0] * se[1]))
    return nest({"n": len(x), "a_grid": a_grid, "b_grid": b_grid, "ll": ll, "a_hat": a_hat, "b_hat": b_hat, "se": se,
                 "wald": [a_hat - 1.96 * se[0], a_hat + 1.96 * se[0]], "profile_ci": [float(inside.min()), float(inside.max())],
                 "prof_a": pr["shapes"][::37], "prof_ll": pr["profile"][::37], "corr": corr, "mean": float(x.mean())})


def compute_trinity():
    r = M.binomial_trinity(14, 20, 0.5)
    p = np.linspace(0.3, 0.92, 300)
    ll = 14 * np.log(p) + 6 * np.log(1 - p)
    return nest({**r, "x": 14, "n": 20, "p0": 0.5, "grid": p, "ll": ll,
                 "score0": 14 / 0.5 - 6 / 0.5, "info0": 20 / (0.5 * 0.5), "info_hat": 20 / (0.7 * 0.3)})


def compute_hauck():
    g = rng(1977)
    n, R = 60, 300
    betas = [0, 1, 2, 3, 4, 5, 6, 7]
    z, lr = [], []
    for b in betas:
        zs, ls = [], []
        for _ in range(R):
            x = g.normal(size=n)
            y = (g.random(n) < 1 / (1 + np.exp(-b * x))).astype(float)
            r = M.logistic_slope_tests(x, y)
            if not np.isfinite(r["z"]) or abs(r["b"][1]) > 40:  # complete separation: no finite MLE
                continue
            zs.append(abs(r["z"]))
            ls.append(np.sqrt(max(r["lr"], 0)))
        z.append(float(np.median(zs)))
        lr.append(float(np.median(ls)))
    return nest({"n": n, "betas": betas, "wald_z": z, "lr_root": lr})


def compute_neyman():
    g = rng(1948)
    ests = [M.neyman_scott(1000, 1.0, g) for _ in range(300)]
    return nest({"pairs": 1000, "sigma2": 1.0, "mle": float(np.mean([e["mle"] for e in ests])),
                 "fixed": float(np.mean([e["fixed"] for e in ests])), "mle_sd": float(np.std([e["mle"] for e in ests])),
                 "mles": [e["mle"] for e in ests], "fixeds": [e["fixed"] for e in ests]})


def compute_kl():
    idx = W.sample(5000, among=W.adult, seed=2202)
    x = W.income[idx]
    lx = np.log(x)
    mu, sd = float(lx.mean()), float(lx.std())
    pop = W.income[W.adult]
    true_mean = float(pop.mean())
    implied_mean = float(np.exp(mu + sd ** 2 / 2))
    tail_true = float(np.mean(pop > 300_000))
    tail_model = float(stats.norm.sf((np.log(300_000) - mu) / sd))
    e = np.linspace(np.log(3000), np.log(2_000_000), 61)
    h, _ = np.histogram(lx, e, density=True)
    gr = (e[:-1] + e[1:]) / 2
    return nest({"mu": mu, "sd": sd, "true_mean": true_mean, "implied_mean": implied_mean, "tail_true": tail_true,
                 "tail_model": tail_model, "edges": e, "hist": h, "grid": gr, "dens": stats.norm.pdf(gr, mu, sd),
                 "median": float(np.median(x)), "true_median": float(np.median(pop))})


def nb_data(n, g, b=(0.5, 0.4), k=1.5):
    x = g.normal(size=n)
    mu = np.exp(b[0] + b[1] * x)
    y = g.negative_binomial(k, k / (k + mu))
    return np.column_stack([np.ones(n), x]), y


def compute_sandwich():
    g = rng(1967)
    X, y = nb_data(400, g)
    r = M.poisson_regression(X, y)
    return nest({"b": r["b"], "se_model": r["se_model"], "se_sandwich": r["se_sandwich"], "se_quasi": r["se_quasi"],
                 "phi": r["phi"], "mean": float(y.mean()), "var": float(y.var()), "y_hist": np.bincount(y.astype(int))[:15]})


def compute_misbehave():
    x, w = museum.crabs()
    th = load("crabs")["theta"]
    j = int(np.argmax(w))  # put component 1's mean on the busiest interval
    sig = np.logspace(-1.5, -12, 80)
    ll = [M.mix_loglik(x, [th[0], x[j], s, th[3], th[4]], w) for s in sig]
    swapped = M.em_mixture(x, [1 - START[0], START[3], START[4], START[1], START[2]], w=w, iters=5000, tol=1e-13)["theta"]
    return nest({"sigma": sig, "ll": ll, "mu_at": float(x[j]), "ll_mle": float(load("crabs")["loglik"][-1]), "swapped": swapped})


def compute_ising():
    g = rng(1975)
    lat = M.ising_gibbs(48, 0.3, 400, g)
    hot = M.ising_gibbs(48, 0.6, 400, rng(1976))
    ests = [M.ising_pseudo_mle(M.ising_gibbs(48, 0.3, 300, rng(2000 + r)))["beta"] for r in range(12)]
    return nest({"lattice": lat, "lattice_strong": hot, "beta": 0.3, "est": ests, "est_mean": float(np.mean(ests)),
                 "est_sd": float(np.std(ests, ddof=1)), "one": M.ising_pseudo_mle(lat)["beta"], "sites": 48 * 48})


def compute_principle():
    p_bin = float(stats.binom.sf(8, 12, 0.5))  # P(X >= 9 | n = 12)
    p_nb = float(stats.nbinom.sf(8, 3, 0.5))  # heads before the 3rd tail: P(H >= 9)
    th = np.linspace(0.3, 0.98, 200)
    lik = th ** 9 * (1 - th) ** 3
    return nest({"p_binomial": p_bin, "p_negbin": p_nb, "theta": th, "lik": lik / lik.max()})


def compute_em_mm():
    """EM as minorize-maximize, along the mixing proportion alone (the other four held at the MLE)."""
    x, w = museum.crabs()
    th = np.asarray(load("crabs")["theta"])
    ps = np.linspace(0.02, 0.98, 300)

    def ll(p):
        return M.mix_loglik(x, [p, *th[1:]], w)

    f1, f2 = stats.norm.pdf(x, th[1], th[2]), stats.norm.pdf(x, th[3], th[4])
    pt, steps = 0.9, []
    for _ in range(4):
        r = pt * f1 / (pt * f1 + (1 - pt) * f2)
        a, b = w @ r, w @ (1 - r)
        q = lambda p: a * np.log(p) + b * np.log(1 - p)  # noqa: E731
        bound = ll(pt) + q(ps) - q(pt)  # touches ll at pt and lies below it everywhere
        nxt = a / (a + b)
        steps.append({"p": pt, "bound": bound, "next": float(nxt), "ll": ll(pt)})
        pt = float(nxt)
    return nest({"p": ps, "ll": np.array([ll(p) for p in ps]), "steps": steps, "p_hat": float(th[0])})


def compute_lrboot():
    """Two normals against one: the likelihood-ratio statistic's null distribution by parametric bootstrap."""
    x, w = museum.crabs()
    d = load("crabs")
    mu, sd = d["one"]
    up = np.array(museum.CRAB_UPPER)
    g = rng(1985)
    lrs = []
    for _ in range(200):
        y = g.normal(mu, sd, int(w.sum()))
        cnt = np.bincount(np.searchsorted(up, y), minlength=len(up))[: len(up)].astype(float)
        m1 = (cnt @ x) / cnt.sum()
        s1 = np.sqrt((cnt @ (x - m1) ** 2) / cnt.sum())
        best = -np.inf
        for start in ([0.5, m1 - 0.5 * s1, 0.8 * s1, m1 + 0.5 * s1, 0.8 * s1], [0.3, m1 - s1, 0.7 * s1, m1 + 0.3 * s1, 0.8 * s1]):
            best = max(best, M.em_mixture(x, start, w=cnt, iters=3000, tol=1e-10)["loglik"][-1])
        l1 = float(np.sum(cnt * stats.norm.logpdf(x, m1, s1)))
        lrs.append(2 * (best - l1))
    lrs = np.asarray(lrs)
    obs = 2 * (d["loglik"][-1] - d["ll_one"])
    return nest({"lr": lrs, "q95": float(np.quantile(lrs, 0.95)), "obs": float(obs), "R": len(lrs),
                 "p_boot": float((1 + np.sum(lrs >= obs)) / (len(lrs) + 1)), "chi2_1": 3.84, "chi2_3": 7.81})


def compute_board():
    g = rng(2222)
    R = 1000
    # (1) logistic slope, strong effect: Wald vs profile-likelihood intervals
    n, b_true = 50, 2.5
    wald_hit = lr_hit = 0
    for _ in range(R):
        x = g.normal(size=n)
        y = (g.random(n) < 1 / (1 + np.exp(-b_true * x))).astype(float)
        r = M.logistic_slope_tests(x, y)
        wald_hit += abs(r["b"][1] - b_true) <= 1.96 * r["se"]
        lo, hi = M.logistic_profile_ci(x, y)
        lr_hit += lo <= b_true <= hi
    # (2) Neyman-Scott: Wald interval for sigma^2 from the MLE, 200 pairs
    ns_hit = 0
    for _ in range(R):
        e = M.neyman_scott(200, 1.0, g)
        se = e["mle"] * np.sqrt(2 / 200)  # the MLE's own SE: sigma^2-hat sqrt(2/n), n pairs
        ns_hit += abs(e["mle"] - 1.0) <= 1.96 * se
    # (3) Poisson regression of overdispersed counts: model-based vs sandwich
    mod_hit = sand_hit = 0
    for _ in range(R):
        X, y = nb_data(400, g)
        r = M.poisson_regression(X, y)
        mod_hit += abs(r["b"][1] - 0.4) <= 1.96 * r["se_model"][1]
        sand_hit += abs(r["b"][1] - 0.4) <= 1.96 * r["se_sandwich"][1]
    rows = [
        Row(22, r"Wald CI, logistic slope", r"$\beta = 2.5$, \ $n = 50$", "coverage", 0.95, wald_hit / R, R),
        Row(22, r"profile-likelihood CI", r"$\beta = 2.5$, \ $n = 50$", "coverage", 0.95, lr_hit / R, R),
        Row(22, r"MLE of $\sigma^2$, Wald CI", r"Neyman--Scott, \ 200 pairs", "coverage", 0.95, ns_hit / R, R),
        Row(22, r"Poisson model SE", r"overdispersed counts, \ $n = 400$", "coverage", 0.95, mod_hit / R, R),
        Row(22, r"sandwich SE", r"overdispersed counts, \ $n = 400$", "coverage", 0.95, sand_hit / R, R),
    ]
    save_rows(22, rows)
    return {"rows": [asdict(r) | {"verdict": r.verdict, "se": r.se} for r in rows]}


ITEMS = {
    "crabs": compute_crabs, "consistency": compute_consistency, "asymp": compute_asymp, "efron": compute_efron,
    "gamma": compute_gamma, "trinity": compute_trinity, "hauck": compute_hauck, "neyman": compute_neyman, "kl": compute_kl,
    "sandwich": compute_sandwich, "misbehave": compute_misbehave, "ising": compute_ising, "principle": compute_principle,
    "em_mm": compute_em_mm, "lrboot": compute_lrboot, "board": compute_board,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
