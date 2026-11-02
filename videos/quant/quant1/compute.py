"""Every number in Part 1 (The Fair Game), computed and cached in .cache/quant1/.

    python -m videos.quant.quant1.compute [items] [--force]

The research window ends on 31 December 2020 (the sealed envelope, explainer.quant.house.pit): every statistic of
US stocks and Bitcoin here uses data up to that day, except the options chapter, which reads the Surface (10 December
2025) and Bitcoin's history up to that morning.  Items (each seeded; seconds to a few minutes on a laptop):

* ``game``        the opening game: one real year of the US market among three Gaussian random walks of the same
                  mean and volatility, and what gives it away;
* ``regnault``    Regnault's square-root-of-time law on 94 years of daily returns and on Bitcoin;
* ``drag``        simple and log returns, arithmetic and geometric means, volatility drag, daily-rebalanced
                  leverage (1926-2020);
* ``vr``          Lo and MacKinlay (1988) replicated on the size deciles, 1962-1985, then 1986-2020, and the
                  smallest stocks' weekly autocorrelation decade by decade;
* ``tails``       heavy tails: kurtosis, the tail on log axes against the Gaussian, Hill exponents, US and BTC;
* ``cluster``     volatility clustering and the leverage effect: autocorrelations of returns and of their size;
* ``aggregation`` kurtosis against horizon (aggregational Gaussianity), with and without 19 October 1987;
* ``mandelbrot``  running variance and kurtosis through time against a Gaussian, a Student t(3) and a Cauchy;
* ``nagel``       Martin and Nagel (2022): investors who learn price efficiently, and in-sample tests still find
                  "predictability" that out-of-sample tests do not;
* ``pq``          two worlds: Bitcoin's risk-neutral density from the Surface (SVI, Breeden-Litzenberger) beside
                  its real-world density from history; Martin's SVIX bound;
* ``betting``     a fair game can't be beaten by betting systems (doubling, stopping rules); an edge from card
                  counting can (a six-deck shoe, Hi-Lo true counts);
* ``crisis2020``  March 2020: the US market on 16 March and Bitcoin on 12 March, measured against their own tails;
* ``envelope``    the sealed envelope: digests of the hold-out (2021 onward) of every dataset Part 1 reads.
"""

from __future__ import annotations

from datetime import date, datetime, timezone

import numpy as np
from scipy import stats as sstats

from explainer.ai.cache import Cache
from explainer.quant import data
from explainer.quant.house import pit, smile, stats, surface

CACHE = Cache("quant1")
load = CACHE.load

START, END = 19260701, pit.RESEARCH_END


def _json(x):
    if isinstance(x, dict):
        return {str(k): _json(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [_json(v) for v in x]
    if isinstance(x, np.ndarray):
        return x.tolist()
    if isinstance(x, np.generic):
        return x.item()
    return x


def _market():
    """Daily log returns of the US market (Ken French: value-weighted, dividends in), research window."""
    kf = data.ken_french_daily()
    d, r = pit.research(kf["date"], kf["mkt"])
    return d, np.log1p(r), r


def _rf():
    kf = data.ken_french_daily()
    return pit.research(kf["date"], kf["rf"])[1]


def _btc_daily(until: int | None = END):
    b = data.binance_klines("BTCUSDT", "1d", "2017-08", "2025-12")
    dates = np.array([int(datetime.fromtimestamp(t, tz=timezone.utc).strftime("%Y%m%d")) for t in b["time"]])
    close = b["close"]
    if until is not None:
        m = dates <= until
        dates, close = dates[m], close[m]
    return dates[1:], np.diff(np.log(close)), close


def _year_of(d):
    return np.asarray(d) // 10000


def _frac_year(d):
    d = np.asarray(d)
    return d // 10000 + ((d // 100) % 100 - 1) / 12 + (d % 100 - 1) / 365


# ---------------------------------------------------------------------------
GAME_YEAR = 1997


def compute_game() -> dict:
    d, r, _ = _market()
    m = _year_of(d) == GAME_YEAR
    real = r[m]
    mu, sd = real.mean(), real.std(ddof=1)
    rng = np.random.default_rng(1)
    fakes = [mu + sd * rng.standard_normal(len(real)) for _ in range(3)]
    order = [fakes[0], fakes[1], real, fakes[2]]  # the real year is panel 3 (index 2)
    levels = [100 * np.exp(np.concatenate([[0.0], np.cumsum(x)])) for x in order]
    zmax = [float(np.max(np.abs((x - mu) / sd))) for x in order]
    kurt = [stats.excess_kurtosis(x) for x in order]
    worst = int(np.argmin(real))
    # the gap a Gaussian would need: how often a move as large as the year's worst
    return {"year": GAME_YEAR, "real_index": 2, "n": int(len(real)), "mu": float(mu), "sd": float(sd),
            "levels": np.array(levels), "returns": np.array(order), "zmax": zmax, "kurt": kurt,
            "worst_date": int(d[m][worst]), "worst": float(np.expm1(real[worst])),
            "worst_z": float((real[worst] - mu) / sd),
            "worst_gauss_years": stats.gaussian_tail_years((real[worst] - mu) / sd)}


# ---------------------------------------------------------------------------
REG_H = np.array([1, 2, 3, 5, 10, 21, 42, 63, 126, 252, 504])


def compute_regnault() -> dict:
    d, r, _ = _market()
    sd = np.array([np.std(stats.aggregate(r, h, overlapping=True), ddof=1) for h in REG_H])
    slope = float(np.polyfit(np.log(REG_H), np.log(sd), 1)[0])
    db, rb, _ = _btc_daily()
    hb = REG_H[REG_H <= 252]
    sdb = np.array([np.std(stats.aggregate(rb, h, overlapping=True), ddof=1) for h in hb])
    slope_b = float(np.polyfit(np.log(hb), np.log(sdb), 1)[0])
    # 94 one-year paths (non-overlapping, 252 days each), each starting at zero
    n = len(r) // 252
    yearly = np.cumsum(r[: n * 252].reshape(n, 252), axis=1)
    yearly = np.concatenate([np.zeros((n, 1)), yearly], axis=1)
    return {"h": REG_H, "sd": sd, "slope": slope, "sd1": float(sd[0]), "h_btc": hb, "sd_btc": sdb,
            "slope_btc": slope_b, "yearly": yearly, "n_years": int(n), "start": int(d[0]), "end": int(d[-1])}


# ---------------------------------------------------------------------------
def compute_drag() -> dict:
    d, r, simple = _market()
    rf = _rf()
    years = _year_of(d)
    ys = np.arange(1927, 2021)
    annual = np.array([np.prod(1 + simple[years == y]) - 1 for y in ys])
    arith, geo = annual.mean(), np.exp(np.mean(np.log1p(annual))) - 1
    sd = annual.std(ddof=1)
    # daily-rebalanced leverage, borrowing at the risk-free rate (no fees)
    wealth = {}
    for L in (1, 2, 3):
        rl = L * simple - (L - 1) * rf
        w = np.cumprod(1 + rl)
        wealth[str(L)] = w
    years_total = len(r) / 252.0
    g = {L: float(np.log(wealth[str(L)][-1]) / years_total) for L in (1, 2, 3)}
    mu_d, var_d, rf_d = simple.mean(), simple.var(), rf.mean()
    g_theory = {L: float(252 * (L * mu_d - (L - 1) * rf_d - 0.5 * L ** 2 * var_d)) for L in (1, 2, 3)}
    kelly = float((mu_d - rf_d) / var_d)
    step = 21  # keep the curves light: one point a month
    return {"years": ys, "annual": annual, "arith": float(arith), "geo": float(geo), "sd": float(sd),
            "half_var": float(0.5 * sd ** 2), "t": _frac_year(d)[::step],
            "w1": wealth["1"][::step], "w2": wealth["2"][::step], "w3": wealth["3"][::step],
            "final": {str(L): float(wealth[str(L)][-1]) for L in (1, 2, 3)},
            "low": {str(L): float(wealth[str(L)].min()) for L in (1, 2, 3)},
            "low_date": {str(L): int(d[np.argmin(wealth[str(L)])]) for L in (1, 2, 3)},
            "growth": {str(k): v for k, v in g.items()}, "growth_theory": {str(k): v for k, v in g_theory.items()},
            "kelly": kelly, "updown": [1.0, 1.5, 0.75]}


# ---------------------------------------------------------------------------
def _weekly(dates, logr):
    """Wednesday-to-Wednesday log returns (Lo and MacKinlay's convention): the cumulative return at the last
    trading day on or before each Wednesday."""
    c = np.cumsum(logr, axis=0)
    dt = [date(int(x) // 10000, (int(x) // 100) % 100, int(x) % 100) for x in dates]
    ordinal = np.array([x.toordinal() for x in dt])
    # Wednesdays from the first to the last date (date.weekday(): Monday 0, Wednesday 2)
    first = ordinal[0] + ((2 - dt[0].weekday()) % 7)
    weds = np.arange(first, ordinal[-1] + 1, 7)
    idx = np.searchsorted(ordinal, weds, side="right") - 1
    idx = idx[idx >= 0]
    lv = c[idx]
    return np.diff(lv, axis=0), np.array([dates[i] for i in idx[1:]])


VR_Q = (2, 4, 8, 16)


def compute_vr() -> dict:
    sz = data.ken_french_size_daily()
    d, dec = pit.research(sz["date"], sz["deciles"])
    d_m, r_m, _ = _market()
    lr = np.log1p(dec)
    out = {"q": list(VR_Q), "deciles": ["small", "5", "large", "market"]}
    for name, (a, b) in {"lm": (19620906, 19851226), "after": (19860101, END)}.items():
        m = (d >= a) & (d <= b)
        w, wd = _weekly(d[m], lr[m])
        mm = (d_m >= a) & (d_m <= b)
        wm, _ = _weekly(d_m[mm], r_m[mm])
        rows = {}
        for label, series in (("small", w[:, 0]), ("5", w[:, 4]), ("large", w[:, 9]), ("market", wm)):
            rows[label] = {"rho1": float(stats.autocorr(series, [1])[0]),
                           "vr": [stats.variance_ratio(series, q) for q in VR_Q], "n": int(len(series))}
        out[name] = rows
    # the smallest and largest deciles' weekly first-order autocorrelation in rolling 5-year windows
    w, wd = _weekly(d, lr)
    yrs = np.arange(1931, 2017)
    roll = {"small": [], "large": []}
    for y in yrs:
        m = (wd >= y * 10000) & (wd < (y + 5) * 10000)
        roll["small"].append(float(stats.autocorr(w[m, 0], [1])[0]))
        roll["large"].append(float(stats.autocorr(w[m, 9], [1])[0]))
    out["roll_years"] = (yrs + 2.5).tolist()
    out["roll_small"], out["roll_large"] = roll["small"], roll["large"]
    return _json(out)


# ---------------------------------------------------------------------------
def compute_tails() -> dict:
    d, r, _ = _market()
    z = (r - r.mean()) / r.std(ddof=1)
    u, p = stats.survival(z, 160)
    ks = np.unique(np.geomspace(20, 4000, 60).astype(int))
    hc = stats.hill_curve(z, ks)
    # returns scaled by their own recent volatility (a 63-day trailing standard deviation)
    sd_trail = np.sqrt(np.convolve(r ** 2, np.ones(63) / 63, mode="full")[: len(r)])
    zn = r[63:] / sd_trail[62:-1]
    zn = (zn - zn.mean()) / zn.std()
    db, rb, _ = _btc_daily()
    zb = (rb - rb.mean()) / rb.std(ddof=1)
    ub, pb = stats.survival(zb, 120)
    gauss_u = np.geomspace(0.6745, 12, 160)
    beyond = {str(k): int(np.sum(np.abs(z) > k)) for k in (3, 4, 5, 7, 10)}
    expected = {str(k): float(2 * sstats.norm.sf(k) * len(z)) for k in (3, 4, 5, 7, 10)}
    return {"n": int(len(r)), "sd": float(r.std(ddof=1)), "kurt": stats.excess_kurtosis(r),
            "u": u, "p": p, "gauss_u": gauss_u, "gauss_p": 2 * sstats.norm.sf(gauss_u),
            "ks": ks, "hill_curve": hc, "alpha": stats.hill(z, frac=0.02),
            "alpha_left": float(1 / np.mean(np.log(np.sort(-z)[::-1][:int(0.02 * len(z))] /
                                                  np.sort(-z)[::-1][int(0.02 * len(z))]))),
            "alpha_norm": stats.hill(zn, frac=0.02), "kurt_norm": stats.excess_kurtosis(zn),
            "beyond": beyond, "expected": expected,
            "btc_n": int(len(rb)), "btc_sd": float(rb.std(ddof=1)), "btc_kurt": stats.excess_kurtosis(rb),
            "btc_alpha": stats.hill(zb, frac=0.02), "btc_u": ub, "btc_p": pb,
            "hist_edges": np.linspace(-6, 6, 97), "hist": np.histogram(z, np.linspace(-6, 6, 97), density=True)[0],
            "min": float(np.expm1(r.min())), "min_date": int(d[np.argmin(r)]), "max": float(np.expm1(r.max())),
            "max_date": int(d[np.argmax(r)])}


# ---------------------------------------------------------------------------
def compute_cluster() -> dict:
    d, r, _ = _market()
    lags = np.arange(1, 251)
    acf_r = stats.autocorr(r, lags)
    acf_a = stats.autocorr(np.abs(r), lags)
    acf_2 = stats.autocorr(r ** 2, lags)
    m = lags <= 250
    beta = float(-np.polyfit(np.log(lags[m]), np.log(np.maximum(acf_a[m], 1e-4)), 1)[0])
    rng = np.random.default_rng(2)
    shuffled = rng.permutation(r)
    acf_shuf = stats.autocorr(np.abs(shuffled), lags)
    # leverage: corr(r_t, |r_{t+k}|) for k = -20..20 (positive k: today's return against future size)
    kk = np.arange(-20, 21)
    rz = (r - r.mean()) / r.std()
    a = np.abs(r)
    az = (a - a.mean()) / a.std()
    lev = []
    for k in kk:
        if k >= 0:
            lev.append(float(np.mean(rz[: len(r) - k] * az[k:])))
        else:
            lev.append(float(np.mean(rz[-k:] * az[: len(r) + k])))
    db, rb, _ = _btc_daily()
    lb = np.arange(1, 101)
    # monthly realized volatility, annualized, for the 94-year strip
    ym = d // 100
    months = np.unique(ym)
    rv = np.array([r[ym == x].std() * np.sqrt(252) for x in months])
    tm = (months // 100) + ((months % 100) - 0.5) / 12
    # one year in close-up: daily returns of 2008
    m08 = (d >= 20080101) & (d <= 20081231)
    return {"lags": lags, "acf_r": acf_r, "acf_abs": acf_a, "acf_sq": acf_2, "acf_shuffled": acf_shuf,
            "beta": beta, "lev_k": kk, "lev": np.array(lev), "btc_lags": lb,
            "btc_acf_r": stats.autocorr(rb, lb), "btc_acf_abs": stats.autocorr(np.abs(rb), lb),
            "rv_t": tm, "rv": rv, "band": float(2 / np.sqrt(len(r))),
            "y2008": r[m08], "t_all": _frac_year(d), "r_all": r}


# ---------------------------------------------------------------------------
AGG_H = np.array([1, 2, 5, 10, 21, 42, 63, 126, 252])


def compute_aggregation() -> dict:
    d, r, _ = _market()
    i87 = int(np.where(d == 19871019)[0][0])
    r_no = np.delete(r, i87)
    k = np.array([stats.excess_kurtosis(stats.aggregate(r, h)) for h in AGG_H])
    k_no = np.array([stats.excess_kurtosis(stats.aggregate(r_no, h)) for h in AGG_H])
    # overlapping windows for a smoother curve (the same expectation, more samples)
    k_ov = np.array([stats.excess_kurtosis(stats.aggregate(r, h, overlapping=True)) for h in AGG_H])
    hists = {}
    for h in (1, 21, 252):
        x = stats.aggregate(r, h, overlapping=True)
        z = (x - x.mean()) / x.std()
        hists[str(h)] = np.histogram(z, np.linspace(-5, 5, 61), density=True)[0].tolist()
    return {"h": AGG_H, "kurt": k, "kurt_no87": k_no, "kurt_overlap": k_ov, "hists": hists,
            "edges": np.linspace(-5, 5, 61)}


# ---------------------------------------------------------------------------
def compute_mandelbrot() -> dict:
    d, r, _ = _market()
    n = len(r)
    sd = r.std()
    rng = np.random.default_rng(3)
    g = r.mean() + sd * rng.standard_normal(n)
    t3 = r.mean() + sd * rng.standard_t(3, n) / np.sqrt(3.0)  # unit variance
    cau = r.mean() + sd * 0.6 * rng.standard_cauchy(n)

    def running(x):
        c1 = np.cumsum(x)
        c2 = np.cumsum(x ** 2)
        c4 = np.cumsum((x - x.mean()) ** 4)
        k = np.arange(1, len(x) + 1)
        var = c2 / k - (c1 / k) ** 2
        kurt = (c4 / k) / np.maximum(var, 1e-30) ** 2 - 3
        return var, kurt

    every = np.unique(np.geomspace(250, n, 220).astype(int)) - 1
    out = {"t": _frac_year(d)[every], "n_at": every + 1}
    for name, x in (("real", r), ("gauss", g), ("t3", t3), ("cauchy", cau)):
        v, k = running(x)
        out[f"sd_{name}"] = np.sqrt(v[every]) * np.sqrt(252)
        out[f"kurt_{name}"] = k[every]
    i87 = int(np.where(d == 19871019)[0][0])
    x4 = (r - r.mean()) ** 4
    out["share87"] = float(x4[i87] / x4.sum())
    out["kurt_all"] = stats.excess_kurtosis(r)
    out["kurt_no87"] = stats.excess_kurtosis(np.delete(r, i87))
    out["r87"] = float(np.expm1(r[i87]))
    out["alpha_mandelbrot"] = 1.7
    return out


# ---------------------------------------------------------------------------
NAGEL = {"N": 500, "J": 200, "T": 12, "tau": 1.0, "sigma": 1.0, "sims": 300}


def _nagel_once(rng, c):
    N, J, T, tau, sig = c["N"], c["J"], c["T"], c["tau"], c["sigma"]
    X = rng.standard_normal((N, J)) / np.sqrt(J)
    theta = tau * rng.standard_normal(J)
    XtX = X.T @ X
    S = np.zeros(J)
    rets = np.empty((T, N))
    for t in range(T):
        # investors' posterior mean of theta after t periods of payoffs (Gaussian prior, known noise)
        A = np.eye(J) / tau ** 2 + t * XtX / sig ** 2
        theta_hat = np.linalg.solve(A, S / sig ** 2)
        y = X @ theta + sig * rng.standard_normal(N)
        rets[t] = y - X @ theta_hat  # payoff minus the efficient price
        S += X.T @ y
    # the econometrician, afterwards: pooled regression of returns on the characteristics, all T periods
    rbar = rets.mean(axis=0)
    b = np.linalg.solve(XtX, X.T @ rbar)
    fitted = X @ b
    resid = rets - fitted
    s2 = np.sum(resid ** 2) / (N * T - J)
    F = (T * fitted @ fitted / J) / s2
    p_in = float(sstats.f.sf(F, J, N * T - J))
    r2_in = float(1 - np.sum(resid ** 2) / np.sum(rets ** 2))
    # out of sample: at each t (second half), the same regression on periods before t, applied to period t
    num = den = 0.0
    for t in range(T // 2, T):
        bt = np.linalg.solve(XtX, X.T @ rets[:t].mean(axis=0))
        num += np.sum((rets[t] - X @ bt) ** 2)
        den += np.sum(rets[t] ** 2)
    return p_in, r2_in, float(1 - num / den), rets, X, b


def compute_nagel() -> dict:
    c = NAGEL
    rng = np.random.default_rng(4)
    p, r2, oos = [], [], []
    for i in range(c["sims"]):
        pi, ri, oi, rets, X, b = _nagel_once(rng, c)
        p.append(pi)
        r2.append(ri)
        oos.append(oi)
        if i == 0:
            ex_fit, ex_ret = X @ b, rets.mean(axis=0)
    p, r2, oos = map(np.array, (p, r2, oos))
    return {**{k: v for k, v in c.items()}, "p_in": p, "r2_in": r2, "r2_oos": oos,
            "reject": float(np.mean(p < 0.05)), "oos_positive": float(np.mean(oos > 0)),
            "median_r2_in": float(np.median(r2)), "median_r2_oos": float(np.median(oos)),
            "ex_fitted": ex_fit, "ex_mean_return": ex_ret}


# ---------------------------------------------------------------------------
def compute_pq() -> dict:
    q = surface.build("2025-12-10")
    exps = q["expiries"]
    # the monthly expiry about seven weeks out (30 January 2026, 51 days, the expiry of Part 10's quote)
    best = min(exps, key=lambda e: abs(e["T"] * 365 - 45) if e["n"] >= 20 else 1e9)
    m = np.array(q["expiry"]) == best["expiry"]
    T, F = float(best["T"]), float(q["F"][m][0])
    k, iv = q["k"][m], q["iv"][m]
    p = smile.fit_svi(k, iv ** 2 * T, weights=q["vega"][m])
    K = np.linspace(F * 0.45, F * 1.7, 1201)
    dens = smile.risk_neutral_density(p, F, T, K)
    x_q = K / F - 1
    mass = float(np.trapezoid(dens, K))
    days = int(round(T * 365))
    # the real world: overlapping horizon returns of Bitcoin over the four years before that morning
    db, rb, close = _btc_daily(until=20251209)
    m4 = db >= 20211210
    lr = np.log(close[1:][m4])
    h = days
    ret = np.exp(lr[h:] - lr[:-h]) - 1
    kde = sstats.gaussian_kde(ret)
    x = np.linspace(-0.55, 0.7, 501)
    dens_p = kde(x)
    dens_q = np.interp(x, x_q, dens * F)  # density of S_T / F - 1
    var_q = smile.svix2(p, F, T)
    s0 = float(q["S"])
    left = -0.2
    return {"expiry": best["expiry"], "T": T, "days": days, "F": F, "index": s0,
            "k": k, "iv": iv, "svi": {kk: float(v) for kk, v in p.items()}, "svi_k": np.linspace(k.min(), k.max(), 200),
            "svi_iv": smile.svi_iv(p, np.linspace(k.min(), k.max(), 200), T), "x": x, "dens_q": dens_q,
            "dens_p": dens_p, "mass_q": mass, "n_p": int(len(ret)), "sd_p": float(ret.std()),
            "sd_q": float(np.sqrt(var_q)), "mean_p": float(ret.mean()),
            "left_q": float(np.trapezoid(dens_q[x < left], x[x < left])),
            "left_p": float(np.mean(ret < left)), "svix2": var_q, "bound": var_q, "bound_annual": var_q / T,
            "atm_iv": float(smile.svi_iv(p, 0.0, T))}


# ---------------------------------------------------------------------------
def _hilo_counts(rng, n_shoes=4000, decks=6, pen=0.75):
    """Hi-Lo true counts at the start of each hand, dealing a shuffled six-deck shoe to 75% penetration at about
    five cards a hand (one player and the dealer)."""
    ranks = np.array([2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11] * 4 * decks)
    val = np.where(ranks <= 6, 1, np.where(ranks >= 10, -1, 0))
    tcs = []
    for _ in range(n_shoes):
        v = rng.permutation(val)
        stop = int(pen * len(v))
        rc = 0
        i = 0
        while i < stop:
            remaining_decks = (len(v) - i) / 52.0
            tcs.append(rc / remaining_decks)
            rc += v[i: i + 5].sum()
            i += 5
    return np.array(tcs)


def compute_betting() -> dict:
    rng = np.random.default_rng(5)
    # doubling on a fair coin, bankroll 1,023 (ten doublings), each session ends at the first win or at ruin
    n_sessions = 200_000
    flips_to_win = rng.geometric(0.5, n_sessions)
    lose = flips_to_win > 10
    outcome = np.where(lose, -1023.0, 1.0)
    # show 3,000 sessions starting just after a ruin, so the staircase builds before the next cliff
    i0 = int(np.flatnonzero(lose)[0]) + 1
    path = np.cumsum(outcome[i0:i0 + 3000])
    # random stopping rules on a fair walk: stop at +a or after n steps; the mean stays at zero
    rules = []
    for a in (1, 3, 10):
        steps = rng.choice(np.array([-1, 1], dtype=np.int8), size=(100_000, 200))
        walk = np.cumsum(steps, axis=1, dtype=np.int16)
        hit = np.argmax(walk >= a, axis=1)
        hit_any = (walk >= a).any(axis=1)
        final = np.where(hit_any, a, walk[:, -1])
        rules.append({"a": a, "p_hit": float(hit_any.mean()), "mean": float(final.mean()),
                      "se": float(final.std() / np.sqrt(len(final))), "worst": int(final.min())})
    # Thorp: the count makes the game unfair in the player's favour at some times; bet more then
    tc = _hilo_counts(rng)
    edge = -0.005 + 0.005 * tc  # the standard approximation: about half a percent of edge per true count
    flat = float(edge.mean())
    spread = np.clip(np.floor(tc), 1, 8)  # bet 1 unit at counts <= 1, up to 8 units at +8
    ev_spread = float(np.sum(spread * edge) / np.sum(spread))
    per_hand = float(np.mean(spread * edge))
    hist_edges = np.arange(-8.5, 9.0, 1.0)
    return {"p_ruin": float(lose.mean()), "mean_session": float(outcome.mean()),
            "se_session": float(outcome.std() / np.sqrt(n_sessions)), "path": path, "rules": rules,
            "tc_hist": np.histogram(np.clip(tc, -8, 8), hist_edges)[0] / len(tc), "tc_edges": hist_edges,
            "edge_flat": flat, "edge_spread_per_unit": ev_spread, "edge_spread_per_hand": per_hand,
            "mean_bet": float(spread.mean()), "frac_positive": float(np.mean(edge > 0))}


# ---------------------------------------------------------------------------
def compute_crisis2020() -> dict:
    kf = data.ken_french_daily()
    d, simple = pit.research(kf["date"], kf["mkt"])
    r = np.log1p(simple)
    i = int(np.where(d == 20200316)[0][0])
    trail = r[i - 252:i].std(ddof=1)
    z = (r[i] - r[i - 252:i].mean()) / trail
    fit = r[: np.searchsorted(d, 20200101)]
    years_tail = stats.powerlaw_tail_years((fit - fit.mean()) / fit.std(), z * trail / fit.std(), frac=0.02)
    db, rb, close = _btc_daily()
    j = int(np.where(db == 20200312)[0][0])
    trail_b = rb[j - 365:j].std(ddof=1)
    zb = (rb[j] - rb[j - 365:j].mean()) / trail_b
    fit_b = rb[:j]
    years_tail_b = stats.powerlaw_tail_years((fit_b - fit_b.mean()) / fit_b.std(), zb * trail_b / fit_b.std(),
                                             frac=0.05, per_year=365)
    w = (d >= 20200201) & (d <= 20200430)
    wb = (db >= 20200201) & (db <= 20200430)
    return {"us_date": 20200316, "us_ret": float(np.expm1(r[i])), "us_z": float(z),
            "us_trail_sd": float(trail), "us_gauss_years": stats.gaussian_tail_years(z),
            "us_tail_years": years_tail, "us_window_d": d[w], "us_window_r": np.expm1(r[w]),
            "btc_date": 20200312, "btc_ret": float(np.expm1(rb[j])), "btc_z": float(zb),
            "btc_trail_sd": float(trail_b), "btc_gauss_years": stats.gaussian_tail_years(zb, per_year=365),
            "btc_tail_years": years_tail_b, "btc_window_d": db[wb], "btc_window_r": np.expm1(rb[wb]),
            "us_worst_days": [[int(x), float(np.expm1(y))] for x, y in
                              sorted(zip(d[(d >= 20200201) & (d <= 20200430)], r[w]), key=lambda t: t[1])[:3]]}


# ---------------------------------------------------------------------------
def compute_envelope() -> dict:
    kf = data.ken_french_daily()
    sz = data.ken_french_size_daily()
    b = data.binance_klines("BTCUSDT", "1d", "2017-08", "2025-12")
    bd = np.array([int(datetime.fromtimestamp(t, tz=timezone.utc).strftime("%Y%m%d")) for t in b["time"]])
    recs = {"US market, daily (Ken French)": pit.seal("kenfrench/mkt_daily", kf["date"], kf["mkt"]),
            "size deciles, daily (Ken French)": pit.seal("kenfrench/size_deciles_daily", sz["date"], sz["deciles"]),
            "Bitcoin, daily (Binance)": pit.seal("binance/BTCUSDT/1d", bd, b["close"])}
    return {"records": recs, "trials": pit.trials_so_far(), "research_end": pit.RESEARCH_END,
            "holdout_start": pit.HOLDOUT_START}


ITEMS = {"game": compute_game, "regnault": compute_regnault, "drag": compute_drag, "vr": compute_vr,
         "tails": compute_tails, "cluster": compute_cluster, "aggregation": compute_aggregation,
         "mandelbrot": compute_mandelbrot, "nagel": compute_nagel, "pq": compute_pq, "betting": compute_betting,
         "crisis2020": compute_crisis2020, "envelope": compute_envelope}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
