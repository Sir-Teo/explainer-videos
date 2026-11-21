"""Reading the economy in real time (Part 57): how a number is revised, what seasonal adjustment removes and what it
can invent, nowcasting by a dynamic factor model on the Island (where the truth is known) and by bridge equations on
American data, recession signals (the yield curve's probit and the Sahm rule), and the scoring of forecasts (bias,
root mean squared error by horizon, Diebold and Mariano's test, Greenbook against the professional forecasters,
combinations and fan charts).

numpy and scipy only; data from the Data Room (``explainer.economics.data``).
"""

from __future__ import annotations

import numpy as np
from scipy.stats import norm

from .. import data

# ---------------------------------------------------------------------------------------------------------------
# small helpers


def _qkey(q: str) -> tuple:
    """'1965:Q4' or '1965Q4' -> (1965, 4)."""
    q = q.replace(":", "")
    return int(q[:4]), int(q[-1])


def _qstr(y: int, k: int) -> str:
    return f"{y}Q{k}"


def _qadd(q: tuple, h: int) -> tuple:
    n = q[0] * 4 + q[1] - 1 + h
    return n // 4, n % 4 + 1


def _monthly(series: str) -> dict:
    d = data.fred(series)
    return {k[:7]: v for k, v in zip(d["date"], d["value"]) if v == v}


def _quarterly_growth(series: str) -> dict:
    """Annualized quarter-on-quarter growth in percent, keyed (year, quarter)."""
    d = data.fred(series)
    lv = {(int(k[:4]), (int(k[5:7]) - 1) // 3 + 1): v for k, v in zip(d["date"], d["value"]) if v == v}
    out = {}
    for q, v in lv.items():
        p = _qadd(q, -1)
        if p in lv:
            out[q] = 100 * ((v / lv[p]) ** 4 - 1)
    return out


def hac_mean_test(d, lags: int) -> dict:
    """The mean of a loss differential and its Newey-West t statistic (Diebold and Mariano 1995)."""
    d = np.asarray(d, float)
    n = len(d)
    m = d.mean()
    e = d - m
    lrv = e @ e / n
    for k in range(1, lags + 1):
        lrv += 2 * (1 - k / (lags + 1)) * (e[k:] @ e[:-k]) / n
    t = m / np.sqrt(lrv / n) if lrv > 0 else 0.0
    return {"mean": float(m), "t": float(t), "p": float(2 * (1 - norm.cdf(abs(t)))), "n": n}


# ---------------------------------------------------------------------------------------------------------------
# revisions


def revisions() -> dict:
    """Each quarter's annualized real GDP growth as first published and as the latest vintage has it (the
    Philadelphia Fed's real-time data set), and the 2008Q4 estimate vintage by vintage."""
    rt = data.rtdsm()
    fl = rt["first_latest"]
    q = [r["quarter"] for r in fl]
    first = np.array([r["first"] for r in fl])
    latest = np.array([r["latest"] for r in fl])
    rev = latest - first
    sign = (np.sign(first) != np.sign(latest)) & (np.abs(first) > 0) & (np.abs(latest) > 0)
    years = np.array([_qkey(x)[0] for x in q])
    by_decade = {}
    for d in range(1960, 2030, 10):
        m = (years >= d) & (years < d + 10)
        if m.sum() > 4:
            by_decade[str(d)] = {"mae": float(np.mean(np.abs(rev[m]))), "n": int(m.sum())}
    k = int(np.argmax(np.abs(rev)))
    # 2008Q4 vintage by vintage: growth from 2008Q3 to 2008Q4 in each vintage that has both
    qs = rt["quarters"]
    i3, i4 = qs.index("2008:Q3"), qs.index("2008:Q4")
    path = []
    for v in rt["vintages"]:
        a, b = rt["level"][v][i4], rt["level"][v][i3]
        if a == a and b == b:
            path.append({"vintage": v, "growth": 100 * ((a / b) ** 4 - 1)})
    return {"quarters": q, "first": first.tolist(), "latest": latest.tolist(), "mean_rev": float(rev.mean()),
            "mae": float(np.mean(np.abs(rev))), "sd": float(rev.std()), "sign_flips": int(sign.sum()),
            "n": len(q), "biggest": {"quarter": q[k], "first": float(first[k]), "latest": float(latest[k])},
            "by_decade": by_decade, "path_2008q4": path,
            "corr": float(np.corrcoef(first, latest)[0, 1])}


# ---------------------------------------------------------------------------------------------------------------
# seasonal adjustment: a simplified X-11


def _ma2x12(x):
    w = np.r_[0.5, np.ones(11), 0.5] / 12
    out = np.full(len(x), np.nan)
    for t in range(6, len(x) - 6):
        out[t] = w @ x[t - 6:t + 7]
    return out


def _seasonal_3x3(si, months):
    """For each calendar month, a 3x3 moving average (weights 1, 2, 3, 2, 1 over 9) of that month's values across
    years; shorter at the ends."""
    s = np.full(len(si), np.nan)
    w = np.array([1, 2, 3, 2, 1], float)
    for m in range(12):
        idx = np.where((months == m) & np.isfinite(si))[0]
        v = si[idx]
        for j, t in enumerate(idx):
            lo, hi = max(0, j - 2), min(len(v), j + 3)
            ww = w[(lo - j + 2):(hi - j + 2)]
            s[t] = ww @ v[lo:hi] / ww.sum()
    return s


def x11(levels, start_month: int = 0, robust: bool = True, sigma: float = 2.5) -> dict:
    """A simplified X-11 (Shiskin, Young and Musgrave 1967) in logs: the trend by a centred 2x12 moving average,
    seasonal-irregular values, 3x3 seasonal averages by calendar month, centring, and (``robust``) replacement of
    seasonal-irregular values more than ``sigma`` standard deviations from the seasonal by the seasonal itself, as
    X-11 does with extreme values.  Returns log seasonal factors and the adjusted series."""
    y = np.log(np.asarray(levels, float))
    n = len(y)
    months = (np.arange(n) + start_month) % 12
    trend = _ma2x12(y)
    si = y - trend
    s = _seasonal_3x3(si, months)
    replaced = np.zeros(n, bool)
    if robust:
        for _ in range(3):
            irr = si - s
            med = np.nanmedian(np.abs(irr))
            sd = 1.4826 * med                       # a robust scale, which the outliers cannot inflate
            bad = np.abs(irr) > sigma * sd
            replaced |= bad & np.isfinite(si)
            si = np.where(bad, np.nan, si)          # left out of the seasonal averages, as X-11 does
            s = _seasonal_3x3(si, months)
    # carry the factors to the six months at each end, where the centred average is not defined
    for t in range(n):
        if not np.isfinite(s[t]):
            same = np.where((months == months[t]) & np.isfinite(s))[0]
            s[t] = s[same[np.argmin(np.abs(same - t))]]
    s = s - np.nan_to_num(_ma2x12(s), nan=np.nanmean(s))
    return {"seasonal": s, "adjusted": y - s, "replaced": int(replaced.sum()), "months": months}


def seasonal_payrolls() -> dict:
    """Payrolls not seasonally adjusted and as the BLS adjusts them; this module's simplified X-11 run on the
    unadjusted series, with and without its outlier step, against the official adjustment."""
    nsa, sa = _monthly("PAYNSA"), _monthly("PAYEMS")
    keys = sorted(k for k in nsa if k in sa and k >= "1948-01")
    x = np.array([nsa[k] for k in keys])
    off = np.array([sa[k] for k in keys])
    m0 = int(keys[0][5:7]) - 1
    rob, raw = x11(x, m0, robust=True), x11(x, m0, robust=False)
    ch_nsa = np.diff(x)
    ch_off = np.diff(off)
    ch_rob = np.diff(np.exp(rob["adjusted"]))
    ch_raw = np.diff(np.exp(raw["adjusted"]))
    pre = np.array([k < "2020-01" for k in keys[1:]])
    post = np.array([k >= "2021-01" for k in keys[1:]])
    # seasonal factors for April, estimated with the 2020 collapse in the data, robust and not
    apr = [i for i, k in enumerate(keys) if k[5:7] == "04"]
    return {"months": keys, "nsa": x.tolist(), "official": off.tolist(), "adj_robust": np.exp(rob["adjusted"]).tolist(),
            "adj_raw": np.exp(raw["adjusted"]).tolist(), "ch_nsa": ch_nsa.tolist(), "ch_official": ch_off.tolist(),
            "ch_robust": ch_rob.tolist(), "ch_raw": ch_raw.tolist(),
            "rms_robust_pre": float(np.sqrt(np.mean((ch_rob - ch_off)[pre] ** 2))),
            "rms_raw_post": float(np.sqrt(np.mean((ch_raw - ch_off)[post] ** 2))),
            "rms_robust_post": float(np.sqrt(np.mean((ch_rob - ch_off)[post] ** 2))),
            "sd_nsa_change": float(np.std(ch_nsa[pre])), "sd_off_change": float(np.std(ch_off[pre])),
            "apr_years": [keys[i][:4] for i in apr],
            "apr_raw": [float(100 * raw["seasonal"][i]) for i in apr],
            "apr_robust": [float(100 * rob["seasonal"][i]) for i in apr],
            "replaced": rob["replaced"],
            "month_effect": [float(100 * np.mean(rob["seasonal"][rob["months"] == m])) for m in range(12)]}


# ---------------------------------------------------------------------------------------------------------------
# nowcasting on the Island: a small dynamic factor model with a known truth


ISLAND_DFM = {"phi": 0.6, "lam": (1.0, 0.8, 0.7, 0.5), "sd_e": (0.6, 0.7, 0.8, 1.0), "mu": 2.0, "beta": 3.0,
              "sd_q": 0.8}


def dfm_simulate(quarters: int = 400, seed: int = 57, par=None) -> dict:
    """A monthly factor f_t = phi f_{t-1} + eta_t (unit variance shocks), four monthly indicators x_it = lam_i f_t +
    e_it (payrolls, industrial production, retail sales, a business survey), and quarterly GDP growth (annualized,
    percent) y_q = mu + beta * mean(f over the quarter's three months) + eps_q."""
    p = {**ISLAND_DFM, **(par or {})}
    rng = np.random.default_rng(seed)
    T = 3 * quarters + 24
    f = np.zeros(T)
    for t in range(1, T):
        f[t] = p["phi"] * f[t - 1] + rng.standard_normal()
    f = f[24:]
    lam, sd = np.array(p["lam"]), np.array(p["sd_e"])
    X = f[:, None] * lam[None, :] + rng.standard_normal((len(f), 4)) * sd[None, :]
    fq = f.reshape(quarters, 3).mean(axis=1)
    y = p["mu"] + p["beta"] * fq + p["sd_q"] * rng.standard_normal(quarters)
    return {"f": f, "X": X, "y": y, "par": p}


def _kalman_quarter_mean(X, avail, par, t0: int):
    """Kalman filter over months 0..t0+2 with the state (f_t, f_{t-1}, f_{t-2}); ``avail`` (months x 4) marks which
    observations are in the information set.  Returns the mean and variance of the average factor over months
    t0, t0+1, t0+2 given the information."""
    phi = par["phi"]
    lam, R = np.array(par["lam"]), np.diag(np.array(par["sd_e"]) ** 2)
    F = np.array([[phi, 0, 0], [1, 0, 0], [0, 1, 0]])
    Q = np.diag([1.0, 0, 0])
    a = np.zeros(3)
    P = np.eye(3) * (1 / (1 - phi ** 2))
    for t in range(max(0, t0 - 60), t0 + 3):        # the factor forgets fast: five years of history are enough
        a, P = F @ a, F @ P @ F.T + Q
        if t < len(X):
            m = avail[t]
            if m.any():
                Z = np.zeros((m.sum(), 3))
                Z[:, 0] = lam[m]
                v = X[t, m] - Z @ a
                S = Z @ P @ Z.T + R[np.ix_(m, m)]
                K = P @ Z.T @ np.linalg.inv(S)
                a, P = a + K @ v, P - K @ Z @ P
    w = np.array([1, 1, 1]) / 3            # at month t0+2 the state holds f_{t0+2}, f_{t0+1}, f_{t0}
    return float(w @ a), float(w @ P @ w)


RELEASES = ("before the quarter", "month 1: the survey", "month 1: payrolls, production, retail",
            "month 2: everything", "month 3: everything")


def info_set(k: int, t0: int, n_months: int):
    """Availability (months x 4) at release ``k`` for the quarter starting at month t0: everything before the
    quarter, then the survey for month 1, then month 1's hard data, month 2, month 3."""
    A = np.zeros((n_months, 4), bool)
    A[:t0] = True
    if k >= 1:
        A[t0, 3] = True
    if k >= 2:
        A[t0] = True
    if k >= 3:
        A[t0 + 1] = True
    if k >= 4:
        A[t0 + 2] = True
    return A


def dfm_nowcasts(sim: dict, q: int) -> list:
    """The nowcast of quarter ``q``'s GDP growth, with its standard deviation, at each release."""
    par = sim["par"]
    t0 = 3 * q
    out = []
    for k in range(len(RELEASES)):
        A = info_set(k, t0, t0 + 3)
        m, v = _kalman_quarter_mean(sim["X"][:t0 + 3], A, par, t0)
        out.append({"mean": par["mu"] + par["beta"] * m,
                    "sd": float(np.sqrt(par["beta"] ** 2 * v + par["sd_q"] ** 2))})
    return out


def island_nowcast(quarters: int = 400, seed: int = 57, eval_from: int = 20) -> dict:
    """Nowcast every quarter of a simulated Island history at each release; the root mean squared error falls as
    the data arrive.  Also picks the Play-it quarter by rule: the first quarter, after the first 40, whose GDP fell
    while the nowcast before the quarter was above 1%."""
    sim = dfm_simulate(quarters, seed)
    y = sim["y"]
    errs = np.zeros((quarters - eval_from, len(RELEASES)))
    means = np.zeros_like(errs)
    sds = np.zeros_like(errs)
    for j, q in enumerate(range(eval_from, quarters)):
        nc = dfm_nowcasts(sim, q)
        means[j] = [r["mean"] for r in nc]
        sds[j] = [r["sd"] for r in nc]
        errs[j] = means[j] - y[q]
    rmse = np.sqrt((errs ** 2).mean(axis=0))
    cover = (np.abs(errs) <= sds).mean(axis=0)          # one-s.d. bands: about 68% if calibrated
    pick = None
    for j, q in enumerate(range(eval_from, quarters)):
        if q >= 40 and y[q] < 0 and means[j, 0] > 1.0:
            pick = q
            break
    nc = dfm_nowcasts(sim, pick)
    t0 = 3 * pick
    return {"rmse": rmse.tolist(), "coverage": cover.tolist(), "releases": list(RELEASES), "pick": pick,
            "pick_truth": float(y[pick]), "pick_nowcasts": nc,
            "pick_months": sim["X"][t0 - 6:t0 + 3].tolist(), "pick_factor": sim["f"][t0 - 6:t0 + 3].tolist(),
            "sd_y": float(np.std(y)), "par": sim["par"], "n": quarters - eval_from,
            "p_neg": [float(norm.cdf(-r["mean"] / r["sd"])) for r in nc]}


# ---------------------------------------------------------------------------------------------------------------
# nowcasting American GDP with bridge equations (pseudo real time: today's data, the release calendar imposed)


def bridge_nowcast(start: str = "1985Q1", end: str = "2026Q3", window: int = 0) -> dict:
    """GDP growth (annualized) regressed on the quarterly averages of monthly payroll and industrial production
    growth (annualized), fitted on the quarters before the one being nowcast.  Within the quarter, months not yet
    released are filled with each indicator's AR(1) forecast.  Information sets: before the quarter (an AR(1) in GDP
    growth), after month 1, month 2 and month 3 of indicators.  Pseudo real time: today's vintage of every series,
    with the release calendar imposed."""
    gdp = _quarterly_growth("GDPC1")
    mon = {}
    for s in ("PAYEMS", "INDPRO"):
        lv = _monthly(s)
        ks = sorted(lv)
        mon[s] = {ks[i]: 1200 * np.log(lv[ks[i]] / lv[ks[i - 1]]) for i in range(1, len(ks))}
    months = sorted(set(mon["PAYEMS"]) & set(mon["INDPRO"]))
    Xm = np.array([[mon["PAYEMS"][k], mon["INDPRO"][k]] for k in months])
    midx = {k: i for i, k in enumerate(months)}

    def qmonths(q):
        return [f"{q[0]}-{3 * (q[1] - 1) + j + 1:02d}" for j in range(3)]

    qs = sorted(q for q in gdp if all(m in midx for m in qmonths(q)) and q >= (1960, 1))
    s0, e0 = _qkey(start), _qkey(end)
    target = [q for q in qs if s0 <= q <= e0]
    res = {k: [] for k in ("ar", "m1", "m2", "m3")}
    truth = []
    for q in target:
        past = [p for p in qs if p < q]
        if window:
            past = past[-window:]
        # bridge regression on past quarters (all three months known)
        Z = np.array([[1.0, *Xm[[midx[m] for m in qmonths(p)]].mean(axis=0)] for p in past])
        yv = np.array([gdp[p] for p in past])
        b = np.linalg.lstsq(Z, yv, rcond=None)[0]
        # AR(1) for GDP
        yl = np.array([gdp[_qadd(p, -1)] for p in past if _qadd(p, -1) in gdp])
        yc = np.array([gdp[p] for p in past if _qadd(p, -1) in gdp])
        a = np.linalg.lstsq(np.column_stack([np.ones(len(yl)), yl]), yc, rcond=None)[0]
        prev = gdp.get(_qadd(q, -1), np.nan)
        res["ar"].append(a[0] + a[1] * prev)
        mq = [midx[m] for m in qmonths(q)]
        for k, key in ((1, "m1"), (2, "m2"), (3, "m3")):
            known = mq[:k]
            # AR(1) per indicator, fitted on months before the quarter, to fill the months not yet out
            fill = []
            for j in range(2):
                hist = Xm[:mq[0], j]
                c = np.linalg.lstsq(np.column_stack([np.ones(len(hist) - 1), hist[:-1]]), hist[1:], rcond=None)[0]
                last = Xm[known[-1], j]
                vals = list(Xm[known, j])
                for _ in range(3 - k):
                    last = c[0] + c[1] * last
                    vals.append(last)
                fill.append(np.mean(vals))
            res[key].append(b[0] + b[1] * fill[0] + b[2] * fill[1])
        truth.append(gdp[q])
    truth = np.array(truth)
    covid = np.array([(2020, 2) <= q <= (2020, 3) for q in target])
    out = {"quarters": [_qstr(*q) for q in target], "truth": truth.tolist()}
    for key in res:
        e = np.array(res[key]) - truth
        out[key] = np.array(res[key]).tolist()
        out[f"rmse_{key}"] = float(np.sqrt(np.mean(e[~covid] ** 2)))
        out[f"rmse_{key}_all"] = float(np.sqrt(np.mean(e ** 2)))
    out["n"] = int((~covid).sum())
    return out


# ---------------------------------------------------------------------------------------------------------------
# recession signals


def _probit(y, X, iters: int = 60):
    b = np.zeros(X.shape[1])
    for _ in range(iters):
        xb = X @ b
        p = np.clip(norm.cdf(xb), 1e-10, 1 - 1e-10)
        phi = norm.pdf(xb)
        g = X.T @ (phi * (y - p) / (p * (1 - p)))
        W = phi ** 2 / (p * (1 - p))
        H = (X * W[:, None]).T @ X
        step = np.linalg.solve(H, g)
        b = b + step
        if np.max(np.abs(step)) < 1e-10:
            break
    se = np.sqrt(np.diag(np.linalg.inv(H)))
    return b, se


def auc(score, y) -> float:
    score, y = np.asarray(score), np.asarray(y).astype(bool)
    pos, neg = score[y], score[~y]
    s = np.concatenate([pos, neg])
    r = np.argsort(np.argsort(s)) + 1
    return float((r[:len(pos)].sum() - len(pos) * (len(pos) + 1) / 2) / (len(pos) * len(neg)))


def yield_curve_probit(lead: int = 12, start: str = "1959-01") -> dict:
    """Estrella and Mishkin's (1998) probit: the chance that month t + lead is in an NBER recession, given the
    10-year Treasury yield minus the 3-month bill rate in month t; estimated on every month whose outcome is known."""
    g10, tb, rec = _monthly("GS10"), _monthly("TB3MS"), _monthly("USREC")
    ks = sorted(k for k in g10 if k in tb and k >= start)
    spread = np.array([g10[k] - tb[k] for k in ks])
    rk = sorted(rec)
    ridx = {k: i for i, k in enumerate(rk)}
    yv, xs, used = [], [], []
    for i, k in enumerate(ks):
        j = ridx.get(k)
        if j is None or j + lead >= len(rk):
            continue
        yv.append(rec[rk[j + lead]])
        xs.append(spread[i])
        used.append(k)
    yv, xs = np.array(yv), np.array(xs)
    X = np.column_stack([np.ones(len(xs)), xs])
    b, se = _probit(yv, X)
    prob_all = norm.cdf(b[0] + b[1] * spread)
    # episodes of inversion lasting at least three months, and whether a recession began within two years
    starts = [rk[i] for i in range(1, len(rk)) if rec[rk[i]] > 0.5 and rec[rk[i - 1]] < 0.5]
    inv, cur = [], None
    for k, s in zip(ks, spread):
        if s < 0 and cur is None:
            cur = [k, k]
        elif s < 0:
            cur[1] = k
        elif cur is not None:
            inv.append(cur)
            cur = None
    if cur is not None:
        inv.append(cur)
    episodes = []
    for a, z in inv:
        n = (int(z[:4]) - int(a[:4])) * 12 + int(z[5:7]) - int(a[5:7]) + 1
        if n < 3:
            continue
        nxt = [s for s in starts if s >= a]
        lead_m = None
        if nxt:
            lead_m = (int(nxt[0][:4]) - int(a[:4])) * 12 + int(nxt[0][5:7]) - int(a[5:7])
        episodes.append({"from": a, "to": z, "months": n, "recession_after": lead_m
                         if lead_m is not None and lead_m <= 24 else None})
    i22 = [i for i, k in enumerate(ks) if "2022-01" <= k <= "2024-12"]
    peak = int(i22[int(np.argmax(prob_all[i22]))]) if i22 else None
    return {"months": ks, "spread": spread.tolist(), "prob": prob_all.tolist(), "b": b.tolist(), "se": se.tolist(),
            "auc": auc(norm.cdf(X @ b), yv), "n": len(yv), "lead": lead, "episodes": episodes,
            "recession_starts": starts, "peak_2022": {"month": ks[peak], "prob": float(prob_all[peak])}
            if peak is not None else None, "last_month": ks[-1], "last_prob": float(prob_all[-1])}


def sahm_rule(threshold: float = 0.5) -> dict:
    """Claudia Sahm's rule: the three-month average of the unemployment rate minus its lowest three-month average
    over the previous twelve months; a signal when it first reaches ``threshold``.  On today's data (UNRATE) and as
    computed in real time (SAHMREALTIME), against the NBER's recession start months."""
    u = _monthly("UNRATE")
    ks = sorted(u)
    v = np.array([u[k] for k in ks])
    ma = np.convolve(v, np.ones(3) / 3, mode="valid")
    mk = ks[2:]
    ind = np.full(len(ma), np.nan)
    for t in range(12, len(ma)):
        ind[t] = ma[t] - ma[t - 12:t].min()
    rec = _monthly("USREC")
    starts = [k for i, k in enumerate(sorted(rec)) if i and rec[k] > 0.5 and rec[sorted(rec)[i - 1]] < 0.5]

    def triggers(keys, vals):
        """First crossings of the threshold; the rule re-arms only once the indicator is back near zero, and a
        series that starts above the threshold does not count as crossing it."""
        out = []
        on = None
        for k, x in zip(keys, vals):
            if x != x:
                continue
            if on is None:
                on = x >= threshold
                continue
            if x >= threshold and not on:
                out.append(k)
                on = True
            elif x < 0.1:
                on = False
        return out

    def score(trig):
        rows = []
        for k in trig:
            near = [s for s in starts if -12 <= (int(k[:4]) - int(s[:4])) * 12 + int(k[5:7]) - int(s[5:7]) <= 12]
            if near:
                s = near[0]
                lag = (int(k[:4]) - int(s[:4])) * 12 + int(k[5:7]) - int(s[5:7])
                rows.append({"month": k, "recession": s, "lag": lag})
            else:
                rows.append({"month": k, "recession": None, "lag": None})
        return rows

    rt = _monthly("SAHMREALTIME")
    rk = sorted(rt)
    return {"months": mk, "indicator": [float(x) if x == x else None for x in ind],
            "triggers": score(triggers(mk, ind)), "rt_months": rk, "rt": [rt[k] for k in rk],
            "rt_triggers": score(triggers(rk, [rt[k] for k in rk])), "recession_starts": starts}


# ---------------------------------------------------------------------------------------------------------------
# scoring forecasts


def score_spf(h_max: int = 4, start: str = "1968Q4", skip=((2020, 2), (2020, 3))) -> dict:
    """The Survey of Professional Forecasters' median forecasts of real GDP growth for the survey quarter (h = 0)
    and the four after, against each quarter's first-published growth (the real-time data set); with two
    benchmarks that use only what was known: the average of the previous 40 quarters' first estimates, and the last
    first estimate (the previous quarter's).  Bias, root mean squared error by horizon, Diebold and Mariano's test
    against the historical mean, the share of forecasts below zero, and the errors' quantiles for a fan chart.
    Target quarters in ``skip`` (by default the pandemic's 2020Q2 and Q3, whose swings of -30 and +30 points would
    swamp every average) are left out.""" 
    rt = data.rtdsm()["first_latest"]
    first = {_qkey(r["quarter"]): r["first"] for r in rt}
    latest = {_qkey(r["quarter"]): r["latest"] for r in rt}
    spf = data.spf_long()["growth"]
    order = sorted(first)
    out = {"h": list(range(h_max + 1))}
    rows = []
    for h in range(h_max + 1):
        e_spf, e_mean, e_rw, fc, act, tq = [], [], [], [], [], []
        for r in spf:
            s = _qkey(r["quarter"])
            if s < _qkey(start):
                continue
            t = _qadd(s, h)
            f = r["f"][h]
            if f != f or t not in first or t in skip:
                continue
            hist = [first[p] for p in order if p < _qadd(s, -1)][-40:]
            prev = first.get(_qadd(s, -1))
            if len(hist) < 8 or prev is None:
                continue
            a = first[t]
            e_spf.append(f - a)
            e_mean.append(np.mean(hist) - a)
            e_rw.append(prev - a)
            fc.append(f)
            act.append(a)
            tq.append(_qstr(*t))
        e_spf, e_mean, e_rw = np.array(e_spf), np.array(e_mean), np.array(e_rw)
        dm = hac_mean_test(e_mean ** 2 - e_spf ** 2, lags=max(h, 1) + 1)
        rows.append({"h": h, "n": len(e_spf), "bias": float(e_spf.mean()), "rmse": float(np.sqrt(np.mean(e_spf ** 2))),
                     "rmse_mean": float(np.sqrt(np.mean(e_mean ** 2))), "rmse_rw": float(np.sqrt(np.mean(e_rw ** 2))),
                     "dm_t": dm["t"], "dm_p": dm["p"], "share_neg_fc": float(np.mean(np.array(fc) < 0)),
                     "share_neg_act": float(np.mean(np.array(act) < 0)),
                     "q": np.quantile(e_spf, [0.05, 0.25, 0.5, 0.75, 0.95]).tolist(),
                     "fc": fc, "act": act, "target": tq})
    out["rows"] = rows
    last = spf[-1]
    out["latest_survey"] = last["quarter"]
    out["latest_forecast"] = last["f"]
    out["latest_vs_first"] = float(np.mean([abs(first[k] - latest[k]) for k in first]))
    return out


def anxious_index() -> dict:
    """The professional forecasters' median probability of a decline in real GDP in the quarter after the survey
    (the Philadelphia Fed's anxious index, RECESS2), with the NBER's recession quarters."""
    rec = data.spf_long()["recess"]
    q = [r["quarter"] for r in rec]
    p = [r["p"][1] for r in rec]
    usrec = _monthly("USREC")
    rq = {}
    for k, v in usrec.items():
        key = _qstr(int(k[:4]), (int(k[5:7]) - 1) // 3 + 1)
        rq[key] = max(rq.get(key, 0), v)
    starts = [x for i, x in enumerate(q) if i and rq.get(x, 0) > 0.5 and rq.get(q[i - 1], 0) < 0.5]
    before = []
    for s in starts:
        i = q.index(s)
        before.append({"start": s, "p_before": p[i - 1] if i else None, "p_at": p[i],
                       "p_peak": max(p[i:i + 4])})
    return {"quarters": q, "p": p, "recession_quarters": [x for x in q if rq.get(x, 0) > 0.5],
            "starts": before, "mean": float(np.nanmean(p))}


def greenbook_vs_spf(h_max: int = 4) -> dict:
    """Romer and Romer's (2000) comparison: the Federal Reserve staff's Greenbook forecasts of GDP-price inflation
    against the professional forecasters', for the same quarters, scored against today's GDP deflator.  For each
    survey quarter the Greenbook closest to the middle of the quarter's second month is used.  Root mean squared
    errors by horizon, Diebold and Mariano's test, and the equal-weight average of the two."""
    gb = data.greenbook()
    infl = _quarterly_growth("GDPDEF")
    by_q = {}
    for r in gb["gb"]:
        y, mo, d = int(r["date"][:4]), int(r["date"][5:7]), int(r["date"][8:10])
        q = (y, (mo - 1) // 3 + 1)
        mid = (q[1] - 1) * 3 + 2
        dist = abs((mo - mid) * 30 + d - 15)
        if q not in by_q or dist < by_q[q][0]:
            by_q[q] = (dist, r["f"])
    spf = {_qkey(r["quarter"]): r["f"] for r in gb["spf"]}
    rows = []
    for h in range(h_max + 1):
        e_gb, e_spf, e_avg = [], [], []
        for q, (_, fg) in sorted(by_q.items()):
            if q not in spf:
                continue
            t = _qadd(q, h)
            if t not in infl:
                continue
            a, g, s = infl[t], fg[h], spf[q][h]
            if g != g or s != s or s == 0:
                continue
            e_gb.append(g - a)
            e_spf.append(s - a)
            e_avg.append((g + s) / 2 - a)
        e_gb, e_spf, e_avg = map(np.array, (e_gb, e_spf, e_avg))
        dm = hac_mean_test(e_spf ** 2 - e_gb ** 2, lags=h + 1)
        # Bates and Granger (1969): the weight on the Greenbook that minimizes the combination's squared error
        dd = e_gb - e_spf
        w = float(np.clip(-(e_spf @ dd) / (dd @ dd), 0, 1)) if dd @ dd > 0 else 0.5
        e_bg = w * e_gb + (1 - w) * e_spf
        rows.append({"h": h, "n": len(e_gb), "rmse_gb": float(np.sqrt(np.mean(e_gb ** 2))), "w_gb": w,
                     "rmse_bg": float(np.sqrt(np.mean(e_bg ** 2))), "corr": float(np.corrcoef(e_gb, e_spf)[0, 1]),
                     "rmse_spf": float(np.sqrt(np.mean(e_spf ** 2))), "rmse_avg": float(np.sqrt(np.mean(e_avg ** 2))),
                     "dm_t": dm["t"], "dm_p": dm["p"]})
    years = sorted({q[0] for q in by_q if q in spf})
    return {"rows": rows, "first_year": years[0], "last_year": years[-1]}


def epu_peaks(k: int = 6, gap: int = 6) -> dict:
    """The news-based economic policy uncertainty index (Baker, Bloom and Davis 2016) and its ``k`` highest months,
    at least ``gap`` months apart."""
    d = _monthly("USEPUINDXM")
    ks = sorted(d)
    v = np.array([d[x] for x in ks])
    order = np.argsort(-v)
    picked = []
    for i in order:
        if all(abs(i - j) >= gap for j in picked):
            picked.append(int(i))
        if len(picked) == k:
            break
    return {"months": ks, "value": v.tolist(), "peaks": [{"month": ks[i], "value": float(v[i])} for i in picked],
            "mean": float(v.mean())}


# ---------------------------------------------------------------------------------------------------------------
# why recessions are hard to forecast: a regime-switching economy


def regime_forecasts(T: int = 4000, seed: int = 57, mu=(3.0, -3.0), p_stay=(0.95, 0.75), sd: float = 2.0,
                     h_max: int = 4) -> dict:
    """Hamilton's (1989) economy: annualized growth is mu[s] + noise, with s an expansion or a recession that
    persists with probabilities ``p_stay``.  A forecaster who knows the model and the current state perfectly makes
    the best squared-error forecast E[y_{t+h} | s_t].  How often is that forecast below zero, against how often growth
    is?  And with the state only inferred from growth (Hamilton's filter), when does the probability of recession
    cross a half?"""
    rng = np.random.default_rng(seed)
    P = np.array([[p_stay[0], 1 - p_stay[0]], [1 - p_stay[1], p_stay[1]]])
    st = np.zeros(T, int)
    for t in range(1, T):
        st[t] = st[t - 1] if rng.random() < P[st[t - 1], st[t - 1]] else 1 - st[t - 1]
    mu = np.array(mu)
    y = mu[st] + sd * rng.standard_normal(T)
    rows = []
    for h in range(h_max + 1):
        Ph = np.linalg.matrix_power(P, h)
        f = Ph[st] @ mu                      # E[y_{t+h} | s_t], the best forecast given the true state
        rows.append({"h": h, "f_exp": float(Ph[0] @ mu), "f_rec": float(Ph[1] @ mu),
                     "share_neg": float(np.mean(f < 0))})
    # Hamilton's filter on growth alone
    pr = np.zeros(T)
    xi = np.array([0.5, 0.5])
    for t in range(T):
        xi = P.T @ xi
        lik = norm.pdf(y[t], mu, sd)
        xi = xi * lik / (xi @ lik)
        pr[t] = xi[1]
    starts = [t for t in range(1, T) if st[t] == 1 and st[t - 1] == 0]
    lags = []
    for t0 in starts:
        k = next((k for k in range(0, 8) if t0 + k < T and pr[t0 + k] > 0.5), None)
        lags.append(k)
    found = [k for k in lags if k is not None]
    pi_rec = (1 - p_stay[0]) / (2 - p_stay[0] - p_stay[1])
    return {"rows": rows, "share_neg_growth": float(np.mean(y < 0)), "share_rec": float(np.mean(st == 1)),
            "pi_rec": pi_rec, "mean_lag": float(np.mean(found)) if found else None,
            "found": len(found), "starts": len(starts), "false": int(np.sum((pr > 0.5) & (st == 0))),
            "y": y[:160].tolist(), "s": st[:160].tolist(), "prob": pr[:160].tolist(), "mu": mu.tolist(),
            "p_stay": list(p_stay), "sd": sd}
