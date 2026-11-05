"""Every number in Part 43 (Can You Beat the Market?), computed and cached in .cache/quant43/.

    python -m videos.quant.quant43.compute [items] [--force]

Data: Kenneth French's daily US market (1926-2020) for adaptive efficiency; the classic factors of Part 24 for the
House's own registered ensemble, opened once on the sealed hold-out (2021-2025); the Track Record and the envelope's
registry, as every earlier part left them; and the Surface rows each pricing part cached. Everything else is
simulation with fixed seeds: zero-skill managers, a population of funds, Berk and Green's market for skill.

* ``arith``     Sharpe's arithmetic: the chance a zero-skill manager with costs beats the index, by horizon, against
                simulation;
* ``luck``      a population of 2,000 funds with known skill: the best t-statistics under luck, Storey's share of nulls,
                Barras-Scaillet-Wermers' skilled and unskilled shares against the truth;
* ``scale``     Berk and Green, simulated: assets, net alphas and value added over twenty years;
* ``adaptive``  rolling autocorrelation and variance ratios of the US market, 1926-2020;
* ``ensemble``  the House's final strategy, equal risk across Part 24's ten classic factors, registered and opened;
* ``record``    the Track Record, all rows: research against hold-out, the shrinkage slope, deflated Sharpes, the
                trial counter;
* ``surface``   the pricing scoreboard: each model's fit to the Surface, as its part computed it;
* ``research``  Storey's estimator: its bias by lambda and by alternative strength, against simulation, and applied to
                the Track Record.
"""

from __future__ import annotations

import inspect
import json
import math
import warnings

import numpy as np
from scipy import stats

from explainer.ai.cache import Cache
from explainer.quant import data
from explainer.quant.house import backtest as BT, pit, skill as SK, track

warnings.filterwarnings("ignore", category=RuntimeWarning)

CACHE = Cache("quant43")
load = pit.counted(CACHE.load, 43)


def _json(d):
    return json.loads(json.dumps(d, default=lambda o: o.tolist() if hasattr(o, "tolist") else float(o)))


def compute_arith() -> dict:
    cost, te = 0.01, 0.05
    years = [1, 3, 5, 10, 15, 20, 30]
    rng = np.random.default_rng(43)
    m = 20000
    sims = []
    for y in years:
        act = rng.normal(-cost * y, te * math.sqrt(y), m)
        sims.append(float(np.mean(act > 0)))
    return _json({"cost": cost, "te": te, "years": years, "theory": [SK.beat_prob(cost, te, y) for y in years],
                  "sim": sims, "fee_grid": [{"cost": c, "p15": SK.beat_prob(c, te, 15)} for c in (0.0025, 0.005, 0.01, 0.02)]})


def compute_luck() -> dict:
    pop = SK.fund_population(m=2000, seed=7)
    g = pop["group"]
    truth = {"pi0": float(np.mean(g == 0)), "minus": float(np.mean(g == 1)), "plus": float(np.mean(g == 2))}
    est = SK.bsw(pop["p"], pop["t"], gamma=0.2)
    top = np.sort(pop["t"])[::-1][:10]
    # the best t-statistic among 2,000 funds with no skill at all
    null = SK.fund_population(m=2000, shares=(1.0, 0.0, 0.0), seed=8)
    best_null = float(np.max(null["t"]))
    n_sig_null = int(np.sum(null["t"] > 1.96))
    sig = pop["t"] > 1.96
    true_sk = float(np.mean(g[sig] == 2)) if sig.any() else float("nan")
    # persistence: rank by the first ten years' t-statistic, then the next ten years' mean alpha by decile
    rng = np.random.default_rng(71)
    a_true = pop["true_alpha"]
    s_m = 0.05 / math.sqrt(12)
    r1 = a_true[:, None] / 12 + s_m * rng.standard_normal((2000, 120))
    r2 = a_true[:, None] / 12 + s_m * rng.standard_normal((2000, 120))
    t1 = r1.mean(1) / (r1.std(1, ddof=1) / math.sqrt(120))
    dec = np.digitize(t1, np.quantile(t1, np.linspace(0.1, 0.9, 9)))
    persist = [{"decile": int(k + 1), "next_alpha": float(12 * r2[dec == k].mean()),
                "share_skilled": float(np.mean(g[dec == k] == 2))} for k in range(10)]
    # a Fama-French-style bootstrap: resample each fund's months with its alpha removed, and compare percentiles
    resid = SK.fund_population(m=2000, seed=7)        # the same draws, as a check of the null's shape below
    pct = [1, 5, 10, 50, 90, 95, 99]
    act_p = np.percentile(pop["t"], pct)
    boot_p = np.percentile(null["t"], pct)
    from scipy.stats import norm as _n
    exp_fd = {"t2": 2000 * float(_n.sf(1.96)), "t3": 2000 * float(_n.sf(3.0))}
    hist_t, edges = np.histogram(pop["t"], bins=np.linspace(-8, 6, 57))
    hist_n, _ = np.histogram(null["t"], bins=edges)
    return _json({"truth": truth, "est": est, "top_t": top, "best_null": best_null, "n_sig_null": n_sig_null,
                  "n_sig": int(sig.sum()), "share_true_skilled_among_sig": true_sk, "m": 2000, "months": 240,
                  "hist": hist_t, "hist_null": hist_n, "edges": edges, "persist": persist, "pct": pct,
                  "act_pct": act_p, "null_pct": boot_p, "exp_fd": exp_fd, "n_t3_null": int(np.sum(null["t"] > 3)),
                  "check_same": bool(np.allclose(resid["t"], pop["t"]))})


def compute_scale() -> dict:
    rng = np.random.default_rng(5)
    skill = rng.normal(0.0, 0.03, 400)
    bg = SK.berk_green(skill, seed=5)
    A, net, va = bg["assets"], bg["net"], bg["value_added"]
    yrs = np.arange(1, A.shape[0] + 1)
    top = np.argsort(skill)[-40:]
    tot = A.sum(1)
    aw_net = np.where(tot > 0, (A * net).sum(1) / np.maximum(tot, 1e-12), np.nan)   # what an investor dollar earned
    active = A[-1] > 0
    gross_ret = skill - 0.002 * A[-1]                                                # gross alpha on the last year's size
    flat = SK.berk_green(skill, b=1e-6, seed=5)                                  # (almost) no decreasing returns
    fA = flat["assets"]
    f_net = np.where(fA.sum(1) > 0, (fA * flat["net"]).sum(1) / np.maximum(fA.sum(1), 1e-12), np.nan)
    flows = np.diff(A, axis=0)
    past = bg["net"][:-1] + 0.01                                               # last year's gross-of-fee return
    act = A[:-1] > 0
    flow_beta = float(np.polyfit(past[act], flows[act], 1)[0]) if act.sum() > 10 else float("nan")
    revenue = float((0.01 * A[5:]).sum(1).mean())
    return _json({"years": yrs, "aw_net": aw_net, "aw_net_mean": float(np.nanmean(aw_net[5:])),
                  "flat_net_mean": float(np.nanmean(f_net[5:])), "flow_beta": flow_beta, "revenue": revenue,
                  "va_by_year": va.sum(1), "assets_top": A[:, top].mean(1), "assets_all": A.mean(1),
                  "share_active": float(active.mean()),
                  "corr_skill_assets": float(np.corrcoef(skill[active], A[-1][active])[0, 1]),
                  "corr_skill_netalpha": float(np.corrcoef(skill[active], net[-5:].mean(0)[active])[0, 1]),
                  "gross_top": float(gross_ret[top].mean()), "skill_top": float(skill[top].mean()),
                  "va_total": float(va[5:].sum(1).mean()), "fee": 0.01, "b": 0.002, "n": len(skill)})


def compute_bg_theory() -> dict:
    """Berk and Green's no-persistence theorem, checked: with competitive flows, next year's net alpha is unpredictable
    from this year's (a martingale difference); with fixed fund sizes, skill shows up as persistence."""
    rng = np.random.default_rng(5)
    skill = rng.normal(0.0, 0.03, 400)
    bg = SK.berk_green(skill, seed=5)
    A, net = bg["assets"], bg["net"]
    x, y = [], []
    for t in range(2, A.shape[0] - 1):
        m = (A[t] > 0) & (A[t + 1] > 0)
        x += net[t][m].tolist()
        y += net[t + 1][m].tolist()
    x, y = np.array(x), np.array(y)
    sl = np.polyfit(x, y, 1)[0]
    se = float(np.sqrt(np.sum((y - np.polyval(np.polyfit(x, y, 1), x)) ** 2) / (len(x) - 2)) / (x.std() * math.sqrt(len(x))))
    # no flows: every fund keeps the same size, so its net alpha is skill - b A - f plus noise every year
    fixed = 5.0
    nets = skill[:, None] - 0.002 * fixed - 0.01 + 0.05 * rng.standard_normal((400, 20))
    x2, y2 = nets[:, 2:-1].ravel(), nets[:, 3:].ravel()
    sl2 = np.polyfit(x2, y2, 1)[0]
    se2 = float(np.sqrt(np.sum((y2 - np.polyval(np.polyfit(x2, y2, 1), x2)) ** 2) / (len(x2) - 2)) / (x2.std() * math.sqrt(len(x2))))
    # the size is a martingale while positive: mean change in assets, among funds positive in both years
    dA = []
    for t in range(2, A.shape[0] - 1):
        m = (A[t] > 0) & (A[t + 1] > 0)
        dA += (A[t + 1][m] - A[t][m]).tolist()
    return _json({"slope": float(sl), "se": se, "n": int(len(x)), "slope_fixed": float(sl2), "se_fixed": se2,
                  "theory_fixed": float(0.03 ** 2 / (0.03 ** 2 + 0.05 ** 2)), "mean_dA": float(np.mean(dA)),
                  "sd_dA": float(np.std(dA) / math.sqrt(len(dA)))})


def compute_adaptive() -> dict:
    km = data.ken_french_daily(through="2020-12-31")
    d, r = km["date"], km["mkt"]
    ac = SK.rolling_autocorr(r, 1260)
    step = 21
    yrs = d // 10000 + ((d // 100) % 100 - 1) / 12
    by_decade = {}
    for dec in range(1930, 2021, 10):
        m = (d >= dec * 10000) & (d < (dec + 10) * 10000)
        if m.sum() > 500:
            x = r[m] - r[m].mean()
            by_decade[str(dec)] = {"ac1": float(np.dot(x[:-1], x[1:]) / np.dot(x, x)), "vr5": SK.variance_ratio(r[m], 5)}
    qs = list(range(1, 21))
    vr = {}
    for dec in (1970, 2010):
        m = (d >= dec * 10000) & (d < (dec + 10) * 10000)
        vr[str(dec)] = [SK.variance_ratio(r[m], q) for q in qs]
    return _json({"t": yrs[::step], "ac": ac[::step], "by_decade": by_decade, "qs": qs, "vr": vr})


# the House's final strategy: rule fixed before the envelope is opened
RULE = {"definition": "equal risk across Part 24's ten classic factors (MKT, SMB, HML, UMD, RMW, CMA, BAB, QMJ, "
                      "TSMOM, VALMOM): weights proportional to 1 / each factor's 2011-2020 monthly volatility, "
                      "summing to one, fixed for the hold-out; costs: the weighted sum of Part 24's cost model",
        "research": "1993-01 to 2020-12 (all ten available)", "holdout": "2021-01 to 2025-12"}


def _ensemble():
    from videos.quant.quant24 import compute as C24
    cl = C24._classic()
    keys = list(cl)
    common = None
    for k in keys:
        d, x = cl[k]
        ok = np.isfinite(x)
        s = set(np.asarray(d)[ok].tolist())
        common = s if common is None else common & s
    dates = np.array(sorted(common))
    X = np.column_stack([np.asarray(cl[k][1])[np.searchsorted(np.asarray(cl[k][0]), dates)] for k in keys])
    return keys, dates, X, C24.COSTS


def compute_ensemble() -> dict:
    keys, dates, X, costs = _ensemble()
    code = inspect.getsource(_ensemble) + json.dumps(RULE, sort_keys=True)
    strat = "house_ensemble_part43"
    pit.register(strat, code, RULE, trials=1)
    res_m = (dates >= 199301) & (dates <= 202012)
    win = (dates >= 201101) & (dates <= 202012)
    w = 1 / X[win].std(0, ddof=1)
    w = w / w.sum()
    cost = float(np.dot(w, [costs[k] for k in keys]))
    port = X @ w
    hd, hx = pit.open_envelope(strat, "factors/house_ensemble_monthly", dates * 100 + 28, port)
    hx = hx[hd <= 20251231]
    row = track.record(strat, 43, port[res_m], hx, cost, note=RULE["definition"])
    return _json({"keys": keys, "weights": w, "cost": cost, "row": row, "holdout_cum": np.cumprod(1 + hx),
                  "research_cum": np.cumprod(1 + port[res_m]), "corr": np.corrcoef(X[res_m].T)})


def compute_record() -> dict:
    load("ensemble")
    rows = track.rows()
    env = pit._read()
    reg = env["registered"]
    out = []
    for k, v in rows.items():
        r, h = v["research"], v["holdout"]
        n_tr = int(reg.get(k, {}).get("trials", 1))
        # research Sharpe deflated by this strategy's own trials (monthly units), and the hold-out t-statistic
        sr_m = r["sharpe"] / math.sqrt(12)
        dsr = BT.deflated_sharpe(sr_m, max(int(r["n"]), 2), n_tr, 1 / max(int(r["n"]), 2))["dsr"]
        t_h = h["sharpe"] / h["sharpe_se"] if h["sharpe_se"] > 0 else float("nan")
        p_h = float(stats.norm.sf(t_h))
        out.append({"name": k, "part": v["part"], "res_sr": r["sharpe"], "res_se": r["sharpe_se"], "res_n": r["n"],
                    "hold_sr": h["sharpe"], "hold_se": h["sharpe_se"], "hold_net": h["sharpe_net"], "hold_n": h["n"],
                    "trials": n_tr, "dsr_research": dsr, "t_hold": t_h, "p_hold": p_h})
    x = np.array([o["res_sr"] for o in out])
    y = np.array([o["hold_sr"] for o in out])
    slope, icpt = np.polyfit(x, y, 1)
    # the same regression without the three rows whose research windows were under four years
    keep = np.array([o["res_n"] >= 48 for o in out])
    slope_k, icpt_k = np.polyfit(x[keep], y[keep], 1)
    pi0 = SK.storey_pi0([o["p_hold"] for o in out], 0.5)
    fam = {"classic factors": lambda k: "classic_" in k, "factor zoo": lambda k: "part25" in k,
           "machine learning and text": lambda k: any(x in k for x in ("part27", "part28", "part29")),
           "portfolio and risk": lambda k: any(x in k for x in ("part30", "part31")),
           "systematic and stat arb": lambda k: any(x in k for x in ("part32", "part33")),
           "crypto": lambda k: "part39" in k, "the House": lambda k: "part43" in k}
    families = []
    for nm, f in fam.items():
        sub = [o for o in out if f(o["name"])]
        if sub:
            families.append({"family": nm, "n": len(sub), "res": float(np.mean([o["res_sr"] for o in sub])),
                             "hold": float(np.mean([o["hold_sr"] for o in sub])),
                             "net": float(np.mean([o["hold_net"] for o in sub]))})
    se = float(np.median([o["hold_se"] for o in out]))
    best_null = se * BT.expected_max_sr(len(out), 1.0)
    above = [o["name"] for o in out if o["hold_sr"] > best_null]
    return _json({"rows": sorted(out, key=lambda o: (o["part"], o["name"])), "slope": slope, "intercept": icpt,
                  "slope_long": slope_k, "intercept_long": icpt_k, "n_long": int(keep.sum()),
                  "trials": pit.trials_so_far(), "n_registered": len(reg), "n_rows": len(out),
                  "mean_res": float(x.mean()), "mean_hold": float(y.mean()),
                  "share_positive": float(np.mean(y > 0)), "share_sig": float(np.mean([o["p_hold"] < 0.05 for o in out])),
                  "pi0": pi0, "families": families, "median_se": se, "best_null": best_null, "above": above})


def compute_surface() -> dict:
    from pathlib import Path

    def get(part, item):
        return json.loads((Path(__file__).resolve().parents[3] / ".cache" / f"quant{part}" / f"{item}.json").read_text())
    c13 = get(13, "calibrate")
    lv = get(13, "levy_fits")
    c12 = get(12, "surface")
    rb = get(14, "rbergomi")
    rh = get(14, "rheston")
    rows = [
        {"model": "Black--Scholes, one volatility", "part": 13, "rmse": c13["fits"]["BS"]["rmse"]},
        {"model": "Merton jumps", "part": 13, "rmse": lv["fits"]["Merton"]["rmse"]},
        {"model": "Kou jumps", "part": 13, "rmse": lv["fits"]["Kou"]["rmse"]},
        {"model": "variance gamma", "part": 13, "rmse": lv["fits"]["VG"]["rmse"]},
        {"model": "NIG", "part": 13, "rmse": lv["fits"]["NIG"]["rmse"]},
        {"model": "Heston", "part": 13, "rmse": c13["fits"]["Heston"]["rmse"]},
        {"model": "rough Heston", "part": 14, "rmse": rh["rmse"]},
        {"model": "rough Bergomi", "part": 14, "rmse": rb["rmse"]},
        {"model": "SSVI (one surface)", "part": 12, "rmse": c12["rmse_ssvi"]},
    ]
    q10 = get(10, "implied")["surface_row"]
    rbr = get(14, "rb_replay")
    sv = get(14, "sigvol")
    seeds = rbr["seeds"]
    rb_fit = float(np.mean([v["fit_rmse"] for v in seeds.values()]))
    rb_oos = float(np.mean([v["oos_rmse"] for v in seeds.values()]))
    oos = [{"model": "Black--Scholes, a vol per expiry (Part 10)", "in": q10["rmse_in"], "out": q10["rmse_out"]},
           {"model": "rough Bergomi, replayed (Part 14)", "in": rb_fit, "out": rb_oos},
           {"model": "path-dependent volatility (Part 14)", "in": sv["rmse_in"], "out": sv["rmse_out"]}]
    return _json({"rows": sorted(rows, key=lambda x: -x["rmse"]), "unit": "vega-weighted implied-vol RMSE, vol points",
                  "day": "10 December 2025", "oos": oos})


def compute_research() -> dict:
    rng = np.random.default_rng(431)
    lams = [0.1, 0.3, 0.5, 0.7, 0.9]
    reps = 400
    m = 1000
    pi0 = 0.8
    rows = []
    for mu in (1.0, 2.0, 3.0):        # the alternatives' mean z-statistic
        for lam in lams:
            est = []
            for _ in range(reps):
                n1 = rng.binomial(m, 1 - pi0)
                z = np.r_[rng.standard_normal(m - n1), mu + rng.standard_normal(n1)]
                p = 2 * stats.norm.sf(np.abs(z))
                est.append(SK.storey_pi0(p, lam))
            est = np.array(est)
            # the exact expectation: pi0 + (1 - pi0) P(p_alt > lam) / (1 - lam)
            c = stats.norm.isf(lam / 2)
            p_alt = stats.norm.cdf(c - mu) - stats.norm.cdf(-c - mu)
            rows.append({"mu": mu, "lam": lam, "mean": float(est.mean()), "sd": float(est.std()),
                         "theory": float(min(1.0, pi0 + (1 - pi0) * p_alt / (1 - lam))),
                         "below": float(np.mean(est < pi0))})
    # dependence: equicorrelated z-statistics leave the mean of pi0_hat unchanged (linearity) but inflate its spread
    dep = []
    for rho in (0.0, 0.3, 0.6):
        est = []
        for _ in range(reps):
            n1 = int(round(m * (1 - pi0)))
            common = rng.standard_normal()
            z = math.sqrt(rho) * common + math.sqrt(1 - rho) * rng.standard_normal(m)
            z[:n1] += 2.0
            p = 2 * stats.norm.sf(np.abs(z))
            est.append(SK.storey_pi0(p, 0.5))
        dep.append({"rho": rho, "mean": float(np.mean(est)), "sd": float(np.std(est))})
    rec = load("record")
    pr = np.array([o["p_hold"] for o in rec["rows"]])
    boot = [SK.storey_pi0(rng.choice(pr, len(pr)), 0.5) for _ in range(4000)]
    return _json({"pi0": pi0, "m": m, "reps": reps, "rows": rows, "dep": dep, "record_pi0": rec["pi0"],
                  "record_p": pr, "record_boot_sd": float(np.std(boot)),
                  "record_boot_q": np.quantile(boot, [0.05, 0.95])})


def compute_bachelier() -> dict:
    from explainer.quant.house import bs as BS

    def bach(S, K, sn):
        d = (S - K) / sn
        return float((S - K) * stats.norm.cdf(d) + sn * stats.norm.pdf(d))
    S, T = 10.0, 1 / 12
    sig_ln = 2.0                       # a lognormal vol that matches the normal vol at the money: sigma_N = sigma S
    sn = sig_ln * S * math.sqrt(T)
    rows = []
    for K in (-5.0, 0.0, 5.0, 10.0, 15.0):
        b = bach(S, K, sn)
        c = float(BS.price(S, K, T, sig_ln)) if K > 0 else float("nan")
        rows.append({"K": K, "bachelier": b, "bs": c})
    return _json({"S": S, "T": T, "sigma_ln": sig_ln, "sigma_n_sqrtT": sn, "rows": rows,
                  "wti": {"settle": -37.63, "date": "20 April 2020", "switch": "22 April 2020"}})


def compute_fdr() -> dict:
    pop = SK.fund_population(m=2000, seed=7)
    p1 = stats.t.sf(pop["t"], 239)                     # one-sided: is alpha positive?
    g = pop["group"]
    m = len(p1)
    out = {}
    for q in (0.05, 0.1, 0.2):
        order = np.argsort(p1)
        ps = p1[order]
        k_bh = np.nonzero(ps <= q * np.arange(1, m + 1) / m)[0]
        n_bh = int(k_bh[-1] + 1) if len(k_bh) else 0
        pi0 = SK.storey_pi0(2 * np.minimum(p1, 1 - p1), 0.5)
        k_st = np.nonzero(ps <= q * np.arange(1, m + 1) / (m * pi0))[0]
        n_st = int(k_st[-1] + 1) if len(k_st) else 0
        sel_bh, sel_st = order[:n_bh], order[:n_st]
        out[str(q)] = {"bh": n_bh, "storey": n_st,
                       "bh_fdr": float(np.mean(g[sel_bh] != 2)) if n_bh else 0.0,
                       "storey_fdr": float(np.mean(g[sel_st] != 2)) if n_st else 0.0,
                       "n_skilled": int(np.sum(g == 2))}
    naive = p1 < 0.05
    # Storey's q-values: q_(i) = min_{k >= i} pi0 m p_(k) / k
    order = np.argsort(p1)
    pi0 = SK.storey_pi0(2 * np.minimum(p1, 1 - p1), 0.5)
    qv = pi0 * m * p1[order] / np.arange(1, m + 1)
    qv = np.minimum.accumulate(qv[::-1])[::-1]
    top = [{"rank": i + 1, "t": float(pop["t"][order[i]]), "q": float(qv[i]), "skilled": bool(g[order[i]] == 2)}
           for i in range(15)]
    return _json({"q": out, "naive_n": int(naive.sum()), "naive_fdr": float(np.mean(g[naive] != 2)), "top": top,
                  "pi0": pi0})


ITEMS = {"arith": compute_arith, "luck": compute_luck, "scale": compute_scale, "adaptive": compute_adaptive,
         "ensemble": compute_ensemble, "record": compute_record, "surface": compute_surface, "research": compute_research,
         "bachelier": compute_bachelier, "fdr": compute_fdr, "bg_theory": compute_bg_theory}


if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
