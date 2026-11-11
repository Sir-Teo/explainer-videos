"""Every number in Part 41 (Leverage, Liquidity and Crises), computed and cached in .cache/quant41/.

    python -m videos.quant.quant41.compute [items] [--force]

Data: Kenneth French's daily market and industry returns (to 2020); FRED (TED spread, Treasury yields, commercial
paper, Baa spreads, bank deposits); Yahoo Finance (the Shanghai Composite). Models: leverage arithmetic, the loss and
margin spirals, fire sales among leverage-targeting banks, interbank clearing with and without senior debt, CoVaR, MES
and SRISK.

* ``desk``      the desk question: what a 5x fund must sell when its haircut rises, by haircut and loss;
* ``spiral``    the loss and margin spirals: amplification by margin sensitivity and shock;
* ``firesale``  Greenwood-Landier-Thesmar on five stylised banks: first and second round losses, vulnerability;
* ``network``   Eisenberg-Noe on small networks; ring, complete and clustered networks against shocks;
* ``systemic``  CoVaR and MES for banks, insurers and other finance, 1990-2020, and SRISK for Lehman's 2007 balance
                sheet;
* ``gfc``       the TED spread and Baa spread, 2006-2010;
* ``dash``      March 2020: Treasury yields, commercial paper and stocks;
* ``china``     the Shanghai Composite, 2014-2016, and the circuit-breaker days;
* ``y2023``     US bank deposits and the two-year yield, 2022-2023;
* ``dd``        Diamond-Dybvig with a fire-sale value: payoffs by the share that runs, the global-games threshold by
                fire-sale value and insured share, the noisy-signal equilibrium converging to it; SVB's 2022 balance sheet
                as reported in its annual report;
* ``house``     Rule 41: the House's book through 2008 at 1-4x with volatility-linked against through-the-cycle
                margins; the forced sale on the worst day with margins doubled, by leverage; the days to sell it;
* ``research``  the clearing theorem's checks: uniqueness against monotone iteration, the fictitious default
                algorithm's rounds, the phase transition, and fire sales added to the network.
"""

from __future__ import annotations

import json
import math
import warnings

import numpy as np

from explainer.ai.cache import Cache
from explainer.quant import data
from explainer.quant.house import crisis as C, pit

warnings.filterwarnings("ignore", category=RuntimeWarning)

CACHE = Cache("quant41")
load = pit.counted(CACHE.load, 41)


def _json(d):
    return json.loads(json.dumps(d, default=lambda o: o.tolist() if hasattr(o, "tolist") else float(o)))


def _fred(series, a, b):
    x = data.fred(series, a, b)
    d = np.asarray(x["date"])
    v = np.asarray(x["value"], float)
    ok = np.isfinite(v)
    return d[ok], v[ok]


def compute_desk() -> dict:
    base = C.deleverage(100.0, 20.0, 0.10, 0.30)
    grid = []
    for loss in (0.0, 0.05, 0.10, 0.15):
        for h in (0.20, 0.25, 0.30, 0.40):
            r = C.deleverage(100.0, 20.0, loss, h)
            grid.append({"loss": loss, "haircut": h, "sale": r["sale"], "frac": r["sale_frac"]})
    return _json({"base": base, "grid": grid})


def compute_spiral() -> dict:
    rows = []
    for kappa in (0.0, 1.0, 2.0, 3.0):
        r = C.spiral(0.03, kappa=kappa)
        rows.append({"kappa": kappa, "fall": r["fall"], "amp": r["amplification"], "sold": r["sold"], "equity": r["equity"],
                     "rounds": len(r["path"]["p"]) - 2})
    shocks = []
    for s in (0.01, 0.02, 0.03, 0.05, 0.08):
        a0 = C.spiral(s, kappa=0.0)
        a2 = C.spiral(s, kappa=2.0)
        shocks.append({"shock": s, "loss_only": a0["fall"], "both": a2["fall"]})
    p2 = C.spiral(0.03, kappa=2.0)["path"]
    p0 = C.spiral(0.03, kappa=0.0)["path"]
    deep = [{"depth": dpt, "fall": C.spiral(0.03, kappa=2.0, depth=dpt)["fall"]} for dpt in (200.0, 400.0, 800.0, 1600.0)]
    return _json({"rows": rows, "shocks": shocks, "path2": p2, "path0": p0, "deep": deep})


def compute_firesale() -> dict:
    # five stylised banks; three assets: mortgage securities, corporate loans, government bonds ($bn)
    names = ["A", "B", "C", "D", "E"]
    M = np.array([[300, 200, 100], [200, 300, 200], [100, 100, 400], [400, 100, 100], [50, 250, 300]], float)
    lev = np.array([25, 20, 15, 30, 18], float)
    E = M.sum(1) / lev
    L = np.array([5e-5, 2.5e-5, 5e-6])         # price impact per $bn sold
    F = np.array([-0.05, 0.0, 0.0])            # a 5% fall in mortgage securities
    r = C.glt_firesale(M, E, F, L)
    # a doubling of the illiquid asset's impact
    r2 = C.glt_firesale(M, E, F, L * np.array([2, 1, 1]))
    return _json({"names": names, "M": M, "E": E, "lev": lev, "L": L, "F": F, **r, "AV_double": r2["AV"],
                  "first_share": float(-r["first"].sum() / E.sum())})


def _acemoglu(kind, n=10, y=6.0, v=1.0, a=1.5, shocks=None, delta=0.02):
    P = {"ring": C.ring_pi(n), "complete": C.complete_pi(n), "clusters": C.clusters_pi(n, 2, delta)}[kind]
    shocks = np.linspace(0, 8, 65) if shocks is None else shocks
    out = []
    for s in shocks:
        eps = np.zeros(n)
        eps[0] = s
        r = C.senior_clearing(P, np.full(n, y), np.full(n, a), v, eps)
        out.append(int(r["default"].sum()))
    return np.asarray(shocks), np.asarray(out)


def compute_network() -> dict:
    # a five-bank example with the fictitious default algorithm
    Lm = np.array([[0, 3, 0, 0, 2], [0, 0, 4, 0, 0], [2, 0, 0, 3, 0], [0, 1, 0, 0, 2], [1, 0, 2, 0, 0]], float)
    e = np.array([0.5, 1.0, 1.5, 0.2, 2.5])
    en = C.eisenberg_noe(Lm, e)
    sweeps = {}
    for kind in ("ring", "complete", "clusters"):
        s, d = _acemoglu(kind)
        sweeps[kind] = {"shock": s, "defaults": d}
    return _json({"L": Lm, "e": e, "p": en["p"], "pbar": en["pbar"], "default": en["default"], "rounds": en["rounds"],
                  "equity": en["equity"], "sweeps": sweeps, "y": 6.0, "v": 1.0, "a": 1.5, "n": 10})


def compute_systemic() -> dict:
    k = data.ken_french_industries_daily(49, through="2020-12-31")
    d, X, cols = k["date"], k["returns"], k["columns"]
    km = data.ken_french_daily(through="2020-12-31")
    mk = dict(zip(km["date"].tolist(), km["mkt"].tolist()))
    m = np.array([mk.get(int(x), np.nan) for x in d])
    out = {"series": {}, "full": {}}
    for nm in ("Banks", "Insur", "Fin"):
        x = X[:, cols.index(nm)]
        ok = np.isfinite(x) & np.isfinite(m) & (d >= 19900101)
        full = C.covar(m[ok], x[ok], 0.05)
        out["full"][nm] = {**full, "mes": C.mes(m[ok], x[ok], 0.05)}
        yrs, dc, ms = [], [], []
        for y0 in range(1990, 2020, 2):
            s = ok & (d >= y0 * 10000) & (d < (y0 + 2) * 10000)
            c = C.covar(m[s], x[s], 0.05)
            yrs.append(y0 + 1)
            dc.append(c["dcovar"])
            ms.append(C.mes(m[s], x[s], 0.05))
        out["series"][nm] = {"year": yrs, "dcovar": dc, "mes": ms}
    # SRISK on Lehman's 2007 balance sheet (fiscal year to 30 Nov 2007, as reported): assets $691bn, equity $22.5bn
    xb = X[:, cols.index("Fin")]                 # Lehman was a broker-dealer: "other finance" as its proxy
    s07 = np.isfinite(xb) & np.isfinite(m) & (d >= 20070101) & (d <= 20071231)
    mes07 = -C.mes(m[s07], xb[s07], 0.05)
    lr = C.lrmes(mes07)
    D, Eq = 691.0 - 22.5, 22.5
    out["srisk"] = {"mes": mes07, "lrmes": lr, "debt": D, "equity": Eq, "srisk": C.srisk(D, Eq, lr),
                    "leverage": 691.0 / 22.5}
    return _json(out)


def compute_gfc() -> dict:
    d, ted = _fred("TEDRATE", "2006-01-01", "2010-12-31")
    d2, baa = _fred("BAA10Y", "2006-01-01", "2010-12-31")
    i = int(np.argmax(ted))
    return _json({"ted": {"d": d, "v": ted, "max": float(ted[i]), "max_day": str(d[i]), "pre": float(np.median(ted[:250]))},
                  "baa": {"d": d2, "v": baa, "max": float(np.max(baa)), "pre": float(np.median(baa[:250]))}})


def compute_dash() -> dict:
    d10, y10 = _fred("DGS10", "2020-02-01", "2020-04-30")
    dcp, cp = _fred("DCPF3M", "2020-02-01", "2020-04-30")
    db, baa = _fred("BAA10Y", "2020-02-01", "2020-04-30")
    km = data.ken_french_daily(through="2020-12-31")
    s = (km["date"] >= 20200201) & (km["date"] <= 20200430)
    eq = np.cumprod(1 + km["mkt"][s])

    def at(dd, vv, day):
        k = [i for i, x in enumerate(dd) if str(x).replace("-", "")[:8] >= day]
        return float(vv[k[0]]) if k else float("nan")
    return _json({"y10": {"d": d10, "v": y10, "m9": at(d10, y10, "20200309"), "m18": at(d10, y10, "20200318")},
                  "cp": {"d": dcp, "v": cp, "max": float(np.max(cp)), "pre": at(dcp, cp, "20200214")},
                  "baa": {"d": db, "v": baa, "max": float(np.max(baa)), "pre": at(db, baa, "20200214")},
                  "mkt": {"d": km["date"][s], "v": eq, "low": float(eq.min())}})


def compute_china() -> dict:
    y = data.yahoo_daily("000001.SS", "2014-06-01", "2016-03-31")
    d, c = np.asarray(y["date"]), np.asarray(y["close"], float)
    i_pk = int(np.argmax(c))
    after = c[i_pk:]
    i_lo = i_pk + int(np.argmin(after[:80]))
    r = np.r_[np.nan, c[1:] / c[:-1] - 1]
    cb = {}
    for day in (20160104, 20160107):
        k = int(np.searchsorted(d, day))
        cb[str(day)] = float(r[k])
    i0 = int(np.searchsorted(d, 20140701))
    return _json({"d": d, "c": c, "peak": float(c[i_pk]), "peak_day": int(d[i_pk]), "low": float(c[i_lo]),
                  "low_day": int(d[i_lo]), "fall": float(c[i_lo] / c[i_pk] - 1), "start": float(c[i0]),
                  "rise": float(c[i_pk] / c[i0] - 1), "cb": cb})


def compute_y2023() -> dict:
    dd, dep = _fred("DPSACBW027SBOG", "2022-06-01", "2023-12-31")
    d2, y2 = _fred("DGS2", "2022-01-01", "2023-12-31")
    k8 = [i for i, x in enumerate(dd) if str(x).replace("-", "")[:8] >= "20230301"][0]
    k22 = [i for i, x in enumerate(dd) if str(x).replace("-", "")[:8] >= "20230322"][0]
    return _json({"dep": {"d": dd, "v": dep, "mar1": float(dep[k8]), "mar22": float(dep[k22]), "peak": float(np.max(dep))},
                  "y2": {"d": d2, "v": y2, "start": float(y2[0]), "max": float(np.max(y2))}})


def compute_research() -> dict:
    rng = np.random.default_rng(41)
    # 1. random regular networks: the fictitious default algorithm against monotone iteration from above and below
    agree, rounds = 0, []
    trials = 200
    for _ in range(trials):
        n = 12
        Lm = rng.exponential(1.0, (n, n)) * (rng.random((n, n)) < 0.3)
        np.fill_diagonal(Lm, 0.0)
        e = rng.exponential(0.6, n)
        en = C.eisenberg_noe(Lm, e)
        top = C.clearing_iterate(Lm, e, "top")
        bot = C.clearing_iterate(Lm, e, "bottom")
        if np.max(np.abs(en["p"] - top)) < 1e-8 and np.max(np.abs(top - bot)) < 1e-8:
            agree += 1
        rounds.append(en["rounds"])
    # 2. the non-unique cycle: two banks owe each other 1 and hold nothing else
    Lc = np.array([[0, 1.0], [1.0, 0]])
    top = C.clearing_iterate(Lc, np.zeros(2), "top")
    bot = C.clearing_iterate(Lc, np.zeros(2), "bottom")
    # 3. the phase transition, finely: the threshold shock at which each network's defaults jump
    sw = {}
    for kind in ("ring", "complete", "clusters"):
        s, dft = _acemoglu(kind, shocks=np.linspace(0, 8, 161))
        sw[kind] = {"shock": s, "defaults": dft}
    comp = sw["complete"]
    jump = float(comp["shock"][int(np.argmax(comp["defaults"] == 10))])
    # the threshold in closed form for the complete network: bank 0's shortfall y - x0 spread over n - 1 banks must
    # exceed each one's buffer a - v; x0 = max(0, a - eps + y - v) when others pay in full
    n, y, v, a = 10, 6.0, 1.0, 1.5
    thr = n * (a - v)        # eps - (a - v), the shortfall, over n - 1 creditors must exceed each one's buffer a - v
    # 4. fire sales added: banks hold a common illiquid asset; defaulters sell; the price falls with sales
    def cascade(kind, s, alpha):
        P = {"ring": C.ring_pi(n), "complete": C.complete_pi(n)}[kind]
        h = np.full(n, 1.0)                         # units of the illiquid asset each holds
        cash = np.full(n, a - 1.0)                   # the rest of the project, so assets = cash + h * price
        price, sold = 1.0, 0.0
        eps = np.zeros(n)
        eps[0] = s
        for _ in range(50):
            r = C.senior_clearing(P, np.full(n, y), cash + h * price, v, eps)
            new_sold = float(h[r["default"]].sum())
            if abs(new_sold - sold) < 1e-12:
                break
            sold = new_sold
            price = math.exp(-alpha * sold)
        return int(r["default"].sum()), price
    fs = []
    for s in (2.0, 4.0, 5.0):
        row = {"shock": s}
        for kind in ("ring", "complete"):
            row[kind] = cascade(kind, s, 0.0)[0]
            row[kind + "_fs"] = cascade(kind, s, 0.15)[0]
        fs.append(row)
    return _json({"trials": trials, "agree": agree, "rounds_max": int(max(rounds)), "rounds_mean": float(np.mean(rounds)),
                  "cycle": {"top": top, "bottom": bot}, "sweeps": sw, "jump": jump, "thr": thr, "firesale": fs,
                  "params": {"n": n, "y": y, "v": v, "a": a}})


def compute_ltcm() -> dict:
    d1, baa = _fred("BAA10Y", "1998-01-01", "1998-12-31")
    d2, y10 = _fred("DGS10", "1998-01-01", "1998-12-31")
    km = data.ken_french_daily(through="2020-12-31")
    s = (km["date"] >= 19980701) & (km["date"] <= 19981231)
    eq = np.cumprod(1 + km["mkt"][s])
    ks = [i for i, x in enumerate(d1) if str(x).replace("-", "")[:8] >= "19980801"]
    pre = float(baa[ks[0]]) if ks else float("nan")
    # balance-sheet leverage, as reported (President's Working Group, 1999): $125bn assets on $4.7bn equity
    A, E = 125.0, 4.7
    return _json({"baa": {"d": d1, "v": baa, "pre": pre, "max": float(np.max(baa))},
                  "y10": {"d": d2, "v": y10, "min": float(np.min(y10))},
                  "mkt": {"d": km["date"][s], "v": eq, "low": float(eq.min())},
                  "A": A, "E": E, "lev": A / E, "wipe": E / A})


def compute_dd() -> dict:
    from scipy.stats import norm
    f = np.linspace(0, 1, 201)
    th, r = 1.3, 0.85
    e, w = C.dd_payoffs(f, th, r)
    cross = float(f[np.argmax(w < e)])
    rs = np.round(np.linspace(0.5, 0.99, 50), 3)
    thr = {str(s): [C.run_threshold(float(x), insured=s) for x in rs] for s in (0.0, 0.5, 0.9)}

    def eq_signal(sig, r_=0.85):
        z = norm.ppf((np.arange(4000) + 0.5) / 4000)

        def gap(xs):
            tt = xs - sig * z
            u = norm.cdf(z)
            ee, _ = C.dd_payoffs(u, 0.0, r_)
            ww = np.where(u / r_ < 1, tt * np.clip(1 - u / r_, 0, None) / (1 - u), 0.0)
            return float(np.mean(ww - ee))
        a, b = 0.0, 10.0
        for _ in range(80):
            m = 0.5 * (a + b)
            a, b = (m, b) if gap(m) < 0 else (a, m)
        return 0.5 * (a + b)
    sigs = [0.3, 0.1, 0.03, 0.01]
    noisy = [eq_signal(s_) for s_ in sigs]
    # SVB Financial Group, end-2022 ($bn): annual report (Form 10-K) and the Fed's April 2023 review, as reported
    svb = {"htm_book": 91.3, "htm_fair": 76.2, "equity": 16.0, "deposits": 173.1, "out_9mar": 42.0, "q_10mar": 100.0}
    svb["loss"] = svb["htm_book"] - svb["htm_fair"]
    svb["equity_fair"] = svb["equity"] - svb["loss"]
    return _json({"f": f, "early": e, "wait": w, "theta": th, "r": r, "cross": cross, "rs": rs, "thr": thr,
                  "thr85": C.run_threshold(0.85), "thr85_half": C.run_threshold(0.85, insured=0.5),
                  "thr60": C.run_threshold(0.6), "sigs": sigs, "noisy": noisy, "svb": svb})


def compute_house() -> dict:
    km = data.ken_french_daily(through="2020-12-31")
    d, r = km["date"], km["mkt"]
    vol = C.ewma_vol(r)
    calm = (d >= 20050101) & (d <= 20061231)
    s0 = float(np.median(vol[calm]))
    hist = d <= 20071231
    s_stress = float(np.quantile(vol[hist & (d >= 19900101)], 0.99))
    h0 = 0.15
    w = (d >= 20080101) & (d <= 20091231)
    h_pro = np.clip(h0 * vol[w] / s0, h0, 0.9)
    h_ttc = np.full(w.sum(), max(h0, min(0.9, h0 * s_stress / s0 * 0.5)))
    paths = {}
    for lev in (1.0, 2.0, 3.0, 4.0):
        a = C.margin_path(r[w], lev, h_pro)
        b = C.margin_path(r[w], lev, h_ttc)
        paths[str(lev)] = {"pro_eq": a["equity"], "ttc_eq": b["equity"], "pro_sold": float(a["forced"].sum()),
                           "ttc_sold": float(b["forced"].sum()), "pro_lev": a["assets"] / np.maximum(a["equity"], 1e-9),
                           "ttc_lev": b["assets"] / np.maximum(b["equity"], 1e-9), "pro_min": float(a["equity"].min()),
                           "ttc_min": float(b["equity"].min()), "pro_end": float(a["equity"][-1]),
                           "ttc_end": float(b["equity"][-1]),
                           "pro_fall_share": float(a["forced"][d[w] <= 20090309].sum() / max(a["forced"].sum(), 1e-12))}
    y08 = (d >= 20080101) & (d <= 20081231)
    k = int(np.argmin(np.where(y08, r, 1.0)))
    worst, worst_day = float(r[k]), int(d[k])
    h1 = 0.25
    sweep = []
    for lev in np.round(np.arange(1.0, 8.01, 0.25), 2):
        row = {"lev": float(lev)}
        for mult in (1.0, 2.0, 3.0):
            x = C.deleverage(lev, 1.0, -worst, h1 * mult)
            row[str(mult)] = x["sale_frac"]
        sweep.append(row)
    part, pos_adv = 0.10, 0.5

    def days(frac, adv_mult):
        return frac * adv_mult / part

    s2 = C.deleverage(2.0, 1.0, -worst, 2 * h1)
    s5 = C.deleverage(5.0, 1.0, -worst, 2 * h1)
    lev_max = max(x["lev"] for x in sweep if days(x["2.0"], pos_adv) <= 1.0)
    return _json({"d": d[w], "vol": vol[w], "s0": s0, "s_stress": s_stress, "h0": h0, "h_pro": h_pro, "h_ttc": h_ttc,
                  "paths": paths, "worst": worst, "worst_day": worst_day, "h1": h1, "sweep": sweep,
                  "part": part, "pos_adv": pos_adv, "s2": s2, "s5": s5, "days2": days(s2["sale_frac"], pos_adv),
                  "days5": days(s5["sale_frac"], 5.0), "lev_max": lev_max})


ITEMS = {"desk": compute_desk, "spiral": compute_spiral, "firesale": compute_firesale, "network": compute_network,
         "systemic": compute_systemic, "gfc": compute_gfc, "dash": compute_dash, "china": compute_china,
         "y2023": compute_y2023, "research": compute_research, "ltcm": compute_ltcm,
         "dd": compute_dd, "house": compute_house}


if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
