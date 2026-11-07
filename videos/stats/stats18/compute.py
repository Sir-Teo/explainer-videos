"""Precompute every number in Part 18 of *Statistics, Built* ("Who Did You Ask? Sampling and Surveys").

    python -m videos.stats.stats18.compute            # everything missing (a few minutes)
    python -m videos.stats.stats18.compute --force board

Results are cached in ``.cache/stats18/<name>.json``.  The election, the registers and who answers are the World's
survey block (seed 1662); everything else is a seeded simulation on it.

Items:
    digest      the World's Literary Digest: frame, mailing, returns; frame and nonresponse bias; an SRS of 1,000
    meng        Meng's identity for the Digest's returns and a self-selected half; effective sample sizes
    srs         the finite-population correction in a middling town, sampling half
    strat       mean income by register income band: proportional vs Neyman allocation, theory and simulation
    cluster     20 towns x 50 adults: the ICC of the vote, the design effect, naive vs cluster SE
    pps         towns drawn with probability proportional to size: Hansen-Hurwitz vs equal-probability
    ratio       the ratio estimator of mean income using last year's register; Laplace's 1802 ratio
    rake        raking the Digest's returns to the census margins (region, age band, income band)
    polls       a dialled poll with MAR vs MNAR nonresponse: raw and raked
    board       Coverage Board rows
"""

from __future__ import annotations

from dataclasses import asdict

import numpy as np
from scipy import stats

from explainer.ai.cache import Cache
from explainer.stats.board import Row, save_rows
from explainer.stats.kit import survey as S
from explainer.stats.world import World

CACHE = Cache("stats18")
load = CACHE.load
W = World()
R_BOARD = 10_000


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
    """Clip line segments to a rectangle without flattening off-scale values."""
    xmin, xmax, ymin, ymax = rectangle
    points = np.column_stack((xs, ys))
    result = []
    for start, end in zip(points[:-1], points[1:]):
        if not np.isfinite([start, end]).all():
            continue
        delta = end - start
        lo, hi = 0.0, 1.0
        for k, lower, upper in ((0, xmin, xmax), (1, ymin, ymax)):
            if delta[k] == 0:
                if not lower <= start[k] <= upper:
                    hi = -1
                    break
            else:
                a, b = sorted(((lower - start[k]) / delta[k], (upper - start[k]) / delta[k]))
                lo, hi = max(lo, a), min(hi, b)
        if lo <= hi:
            result.append((start + lo * delta, start + hi * delta))
    return result



def integer_allocation(target, total):
    """Largest remainders: preserve the requested fixed sample size."""
    target = np.asarray(target, float)
    result = np.floor(target).astype(int)
    result[np.argsort(-(target-result), kind="stable")[:total-result.sum()]] += 1
    return result


def adults():
    A = W.adult
    sv = W.survey
    return {"vote": sv["vote_blue"][A].astype(float), "listed": sv["listed"][A], "prop": sv["propensity"][A],
            "town": W.town[A].astype(int), "region": W.region[A].astype(int), "income": W.income[A] / 1000,
            "age": W.age[A].astype(float)}


def digest_returns(P, seed=1936):
    g = rng(seed)
    return P["listed"] & (g.random(len(P["vote"])) < P["prop"])


def half_returns(P, seed=2018, shift=1.8):
    z = np.log(P["prop"] / (1 - P["prop"])) + shift
    return rng(seed).random(len(P["vote"])) < 1 / (1 + np.exp(-z))


def age_band(a):
    return np.digitize(a, [30, 50, 67])


def inc_band(y):
    return np.digitize(y, [30, 100])


def compute_digest():
    P = adults()
    v, L = P["vote"], P["listed"]
    R = digest_returns(P)
    srs = rng(7).choice(len(v), 1000, replace=False)
    s = S.srs_mean(v[srs], N=len(v))
    return nest({"N": len(v), "truth": v.mean(), "listed_share": L.mean(), "n_listed": int(L.sum()), "blue_listed": v[L].mean(),
                 "n_returns": int(R.sum()), "return_rate": R.sum() / L.sum(), "blue_returns": v[R].mean(),
                 "frame_bias": v[L].mean() - v.mean(), "nonresp_bias": v[R].mean() - v[L].mean(),
                 "srs_est": s["mean"], "srs_ci": s["ci"], "srs_se": s["se"],
                 "income_listed": np.median(P["income"][L]), "income_all": np.median(P["income"]),
                 "resp_blue": P["prop"][L & (v == 1)].mean(), "resp_red": P["prop"][L & (v == 0)].mean()})


def compute_meng():
    P = adults()
    v = P["vote"]
    out = {}
    for name, R in (("digest", digest_returns(P)), ("half", half_returns(P))):
        m = S.meng(v, R)
        out[name] = m
    # the error of an SRS of the same sizes, for comparison
    out["srs_sd_1000"] = float(v.std() / np.sqrt(1000))
    return nest(out)


def compute_srs():
    P = adults()
    t = int(np.argsort(np.bincount(P["town"], minlength=200))[100])  # a middling town
    k = np.flatnonzero(P["town"] == t)
    g = rng(18)
    pop = P["income"][k][:3000] if len(k) >= 3000 else P["income"][k]
    N = len(pop)
    n = N // 2
    mu = pop.mean()
    hit_fpc = hit_no = 0
    ses_fpc, ses_no = [], []
    for _ in range(4000):
        x = pop[g.choice(N, n, replace=False)]
        a, b = S.srs_mean(x, N), S.srs_mean(x)
        hit_fpc += a["ci"][0] <= mu <= a["ci"][1]
        hit_no += b["ci"][0] <= mu <= b["ci"][1]
    return nest({"town": t, "N": N, "n": n, "fpc": 1 - n / N, "cover_fpc": hit_fpc / 4000, "cover_no": hit_no / 4000,
                 "mean": mu})


def compute_strat():
    P = adults()
    y = P["income"]
    b = inc_band(y)
    Nh = np.bincount(b, minlength=3)
    Sh = np.array([y[b == k].std(ddof=1) for k in range(3)])
    n = 1000
    prop = integer_allocation(S.proportional_allocation(Nh, n), n)
    ney = integer_allocation(S.neyman_allocation(Nh, Sh, n), n)
    g = rng(34)
    est = {"srs": [], "prop": [], "ney": []}
    idx_by = [np.flatnonzero(b == k) for k in range(3)]
    for _ in range(3000):
        est["srs"].append(y[g.choice(len(y), n, replace=False)].mean())
        for key, alloc in (("prop", prop), ("ney", ney)):
            m = 0.0
            for k in range(3):
                nk = int(round(alloc[k]))
                m += Nh[k] / Nh.sum() * y[g.choice(idx_by[k], nk, replace=False)].mean()
            est[key].append(m)
    return nest({"Nh": Nh, "Sh": Sh, "means": [y[b == k].mean() for k in range(3)], "prop": prop, "ney": ney,
                 "se_srs": np.sqrt((1-n/len(y))*y.var(ddof=1)/n), "se_prop": np.sqrt(S.stratified_variance(Nh, Sh, prop)),
                 "se_ney": np.sqrt(S.stratified_variance(Nh, Sh, ney)),
                 "sim_sd": {k: float(np.std(v)) for k, v in est.items()}, "truth": y.mean()})


_POOLS: dict = {}


def town_pools(P):
    if "pools" not in _POOLS:
        order = np.argsort(P["town"], kind="stable")
        cuts = np.searchsorted(P["town"][order], np.arange(201))
        _POOLS["pools"] = [order[cuts[t]:cuts[t + 1]] for t in range(200)]
    return _POOLS["pools"]


def cluster_sample(P, g, k=20, m=50):
    pools = town_pools(P)
    towns = g.choice(200, k, replace=False)
    sel = [g.choice(pools[t], min(m, len(pools[t])), replace=False) for t in towns]
    return towns, sel


def compute_cluster():
    P = adults()
    v = P["vote"]
    g = rng(1965)
    sub = g.choice(len(v), 120_000, replace=False)
    rho = S.icc(v[sub], P["town"][sub])
    towns, sel = cluster_sample(P, g)
    ys = np.concatenate([v[s] for s in sel])
    cm = np.array([v[s].mean() for s in sel])
    naive = ys.std(ddof=1) / np.sqrt(len(ys))
    clus = cm.std(ddof=1) / np.sqrt(len(cm))
    return nest({"icc": rho, "deff": S.design_effect(50, rho), "towns": towns, "est": ys.mean(), "naive_se": naive,
                 "cluster_se": clus, "truth": v.mean(), "town_means": cm, "neff": 1000 / S.design_effect(50, rho)})


def compute_pps():
    P = adults()
    y = P["income"]
    sizes = np.bincount(P["town"], minlength=200).astype(float)
    totals = np.bincount(P["town"], weights=y, minlength=200)
    T = totals.sum()
    p = sizes / sizes.sum()
    g = rng(1943)
    hh, eq = [], []
    for _ in range(4000):
        d = g.choice(200, 10, p=p)
        hh.append(S.hansen_hurwitz(totals[d], p[d])["total"])
        e = g.choice(200, 10, replace=False)
        eq.append(200 * totals[e].mean())
    return nest({"T": T, "sd_hh": np.std(hh), "sd_eq": np.std(eq), "mean_hh": np.mean(hh), "mean_eq": np.mean(eq),
                 "sizes_max": sizes.max(), "sizes_min": sizes.min(), "ratio_sd": np.std(eq) / np.std(hh)})


def compute_ratio():
    P = adults()
    y = P["income"]
    # the register's income for last year, correlated with this year's: an auxiliary known for everyone
    last = np.exp(np.log(y) + rng(5).normal(0, 0.25, len(y)))
    g = rng(1802)
    pr, rr = [], []
    for _ in range(3000):
        k = g.choice(len(y), 400, replace=False)
        pr.append(y[k].mean())
        rr.append(S.ratio_mean(y[k], last[k], last.mean())["mean"])
    k = g.choice(len(y), 400, replace=False)
    one = S.ratio_mean(y[k], last[k], last.mean())
    return nest({"corr_last": np.corrcoef(y, last)[0, 1], "sd_plain": np.std(pr), "sd_ratio": np.std(rr), "truth": y.mean(),
                 "mean_ratio": np.mean(rr), "mean_plain": np.mean(pr), "one": one, "one_plain": y[k].mean(), "one_indices": k, "one_last": last[k], "one_income": y[k],
                 "laplace": {"pop_sample": 2_037_615, "births_sample": 71_866, "births_all": 1_000_000,
                             "ratio": 2_037_615 / 71_866, "estimate": 1_000_000 * 2_037_615 / 71_866}})


def rake_returns(P, R):
    margins = [P["region"][R], age_band(P["age"][R]), inc_band(P["income"][R])]
    targets = []
    for var in (P["region"], age_band(P["age"]), inc_band(P["income"])):
        vals, cnt = np.unique(var, return_counts=True)
        targets.append({int(a): c / len(var) for a, c in zip(vals, cnt)})
    return S.rake(margins, targets, iters=100)


def raking_steps(P, R, passes):
    """The displayed two-margin IPF iterations, independent of the three-margin fit."""
    ib, ab = inc_band(P["income"][R]), age_band(P["age"][R])
    ti = np.bincount(inc_band(P["income"]), minlength=3) / len(P["income"])
    ta = np.bincount(age_band(P["age"]), minlength=4) / len(P["age"])
    w = np.ones(R.sum())
    out = []
    for k in range(passes + 1):
        out.append((np.bincount(ib, weights=w, minlength=3)/w.sum(),
                    np.bincount(ab, weights=w, minlength=4)/w.sum()))
        if k % 2 == 0:
            w *= (ti / out[-1][0])[ib]
        else:
            w *= (ta / out[-1][1])[ab]
    return out, ti, ta


def compute_rake():
    P = adults()
    v = P["vote"]
    R = digest_returns(P)
    w, hist = rake_returns(P, R)
    sample_share = {nm: np.bincount(var[R], minlength=k) / R.sum() for nm, var, k in
                    (("income", inc_band(P["income"]), 3), ("age", age_band(P["age"]), 4))}
    pop_share = {nm: np.bincount(var, minlength=k) / len(var) for nm, var, k in
                 (("income", inc_band(P["income"]), 3), ("age", age_band(P["age"]), 4))}
    raked = S.weighted_mean(v[R], w)
    # the 'missing' bias: Blue voters return more often at every income: raking can't see that
    return nest({"raw": v[R].mean(), "raked": raked, "truth": v.mean(), "neff": S.kish_neff(w), "n": int(R.sum()),
                 "hist": hist[:12], "sample_share": sample_share, "pop_share": pop_share,
                 "w_range": [float(w.min()), float(w.max())]})


def compute_board():
    P = adults()
    v = P["vote"]
    N = len(v)
    truth = v.mean()
    g = rng(18_000)
    hits = {"srs": 0, "half": 0, "clus_naive": 0, "clus": 0, "raked": 0}
    zc = 1.96
    for r in range(R_BOARD):
        k = g.choice(N, 1000, replace=False)
        s = S.srs_mean(v[k], N)
        hits["srs"] += s["ci"][0] <= truth <= s["ci"][1]
        towns, sel = cluster_sample(P, g)
        ys = np.concatenate([v[q] for q in sel])
        cm = np.array([v[q].mean() for q in sel])
        m = ys.mean()
        hits["clus_naive"] += abs(m - truth) <= zc * ys.std(ddof=1) / np.sqrt(len(ys))
        hits["clus"] += abs(m - truth) <= stats.t.ppf(0.975, 19) * cm.std(ddof=1) / np.sqrt(20)
    # self-selected halves and raked returns are huge: their sampling variation is tiny, so 200 replicates suffice
    reps = 200
    for r in range(reps):
        R = half_returns(P, seed=50_000 + r)
        x = v[R]
        se = x.std(ddof=1) / np.sqrt(len(x))
        hits["half"] += abs(x.mean() - truth) <= zc * se
        Rd = digest_returns(P, seed=60_000 + r)
        w, _ = rake_returns(P, Rd)
        mw = S.weighted_mean(v[Rd], w)
        se_w = np.sqrt(np.sum((w / w.sum()) ** 2 * (v[Rd] - mw) ** 2))
        hits["raked"] += abs(mw - truth) <= zc * se_w
    rows = [
        Row(18, r"SRS of 1,000, \ Wald interval", r"the World's vote for Blue", "coverage", 0.95, hits["srs"] / R_BOARD, R_BOARD),
        Row(18, r"a self-selected half, \ $n \approx 364{,}000$", r"the World's vote for Blue", "coverage", 0.95, hits["half"] / reps, reps),
        Row(18, r"20 towns $\times$ 50, \ SRS formula", r"the World's vote for Blue", "coverage", 0.95, hits["clus_naive"] / R_BOARD, R_BOARD),
        Row(18, r"20 towns $\times$ 50, \ cluster SE", r"the World's vote for Blue", "coverage", 0.95, hits["clus"] / R_BOARD, R_BOARD),
        Row(18, r"Digest returns, \ raked", r"the World's vote for Blue", "coverage", 0.95, hits["raked"] / reps, reps),
    ]
    save_rows(18, rows)
    return {"rows": [asdict(r) | {"verdict": r.verdict, "se": r.se} for r in rows]}


def compute_polls():
    """A modern poll: 20,000 numbers dialled at random, about 8% answer.  MAR: answering depends on income and age
    only; MNAR: it also depends on the vote, as the World's propensity does.  Raw and raked estimates, 200 polls each."""
    P = adults()
    v, y, a = P["vote"], P["income"], P["age"]
    N = len(v)
    li = np.log(y) - np.log(30.0)
    p_mar = 1 / (1 + np.exp(-(-2.6 + 0.35 * li + 0.015 * (a - 45))))
    z = np.log(P["prop"] / (1 - P["prop"]))
    p_mnar = 1 / (1 + np.exp(-(z - 0.3)))
    targets = []
    for var in (inc_band(y), age_band(a), P["region"]):
        vals, cnt = np.unique(var, return_counts=True)
        targets.append({int(k): c / N for k, c in zip(vals, cnt)})
    g = rng(2016)
    out = {}
    for name, pr in (("mar", p_mar), ("mnar", p_mnar)):
        raw, raked, ns = [], [], []
        for _ in range(200):
            dial = g.choice(N, 20_000, replace=False)
            resp = dial[g.random(20_000) < pr[dial]]
            raw.append(v[resp].mean())
            w, _ = S.rake([inc_band(y[resp]), age_band(a[resp]), P["region"][resp]], targets, iters=60)
            raked.append(S.weighted_mean(v[resp], w))
            ns.append(len(resp))
        out[name] = {"raw": float(np.mean(raw)), "raked": float(np.mean(raked)), "raked_sd": float(np.std(raked)),
                     "n": float(np.mean(ns))}
    out["truth"] = float(v.mean())
    return nest(out)


ITEMS = {
    "digest": compute_digest, "meng": compute_meng, "srs": compute_srs, "strat": compute_strat, "cluster": compute_cluster,
    "pps": compute_pps, "ratio": compute_ratio, "rake": compute_rake, "polls": compute_polls, "board": compute_board,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
