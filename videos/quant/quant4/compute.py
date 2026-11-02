"""Every number in Part 4 (Martingales and Measure), computed and cached in .cache/quant4/.

    python -m videos.quant.quant4.compute [items] [--force]

Research window: to December 2020 (the sealed envelope).  Items (seeded; seconds to a minute):

* ``doob``     Doob's decomposition: a biased coin (drift 0.1 a toss); the US market's log wealth 1926-2020 as the
               running sum of each day's drift forecast (the mean so far) plus a martingale; and that martingale's
               square, whose predictable part is the sum of each day's variance forecast (an EWMA known the day
               before);
* ``measure``  a change of measure on a coin: the likelihood-ratio martingale dQ/dP for p = 0.5, q = 0.6, its paths
               under P (mean one, median to zero) and under Q;
* ``ruin``     gambler's ruin on a fair coin, European and American roulette; bold play against timid play (Dubins and
               Savage): the chance of doubling a bankroll;
* ``stable``   stable laws: McCulloch's alpha for the US market by decade and for Bitcoin; alpha against horizon; the
               Mantegna-Stanley probability of return to the origin across time scales;
* ``nikkei``   the Nikkei 225 from July 1994 to March 1995 (FRED), the Kobe earthquake and the fall of Barings;
* ``peeking``  monitoring a fair game: a t-test checked every day rejects far more often than 5%; an e-process
               checked every day does not (Ville's inequality);
* ``eprocess`` testing by betting on real data: does the sign of yesterday's return predict today's?  US market from
               1926, from 1975 and from 2000; Bitcoin from 2018;
* ``envelope`` seals the Nikkei's hold-out and registers the two e-process tests.

The expansion (each item's docstring says what it computes): ``condexp`` (the market's conditional means by era),
``martingales``, ``systems`` (six betting systems), ``firstpassage`` (10,000 walks to 100,000 steps), ``patterns``,
``doubling``, ``nikkei_doubling`` (schematic), ``ruin_duration``, ``polya`` (and upcrossings), ``drift_posterior``,
``ivey_sim``, ``esscher``, ``radon``, ``kakutani``, ``ecf`` (and aggregation), ``stable_mle`` (resumable, the longest:
about 15 minutes), ``peeking_curve``, ``learner`` (resumable), ``confseq``, ``casino``, ``beliefs``, ``ebh``,
``numeraire``, ``envelope_ons``.
"""

from __future__ import annotations

import inspect
from datetime import datetime, timezone

import numpy as np

from explainer.ai.cache import Cache
from explainer.quant import data
from explainer.quant.house import martingale, pit

CACHE = Cache("quant4")
load = CACHE.load


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
    kf = data.ken_french_daily()
    d, r = pit.research(kf["date"], kf["mkt"])
    return d, np.log1p(r)


def _btc_daily():
    b = data.binance_klines("BTCUSDT", "1d", "2017-08", "2025-12")
    dates = np.array([int(datetime.fromtimestamp(t, tz=timezone.utc).strftime("%Y%m%d")) for t in b["time"]])
    m = dates <= pit.RESEARCH_END
    return dates[m][1:], np.diff(np.log(b["close"][m]))


def _frac(d):
    d = np.asarray(d)
    return d // 10000 + ((d // 100) % 100 - 1) / 12 + (d % 100 - 1) / 365


def _ewma_var(r, lam=0.94, warm=60):
    """Each day's variance forecast, made the day before (RiskMetrics): predictable."""
    v = np.empty_like(r)
    v[0] = np.var(r[:warm])
    for t in range(1, len(r)):
        v[t] = lam * v[t - 1] + (1 - lam) * r[t - 1] ** 2
    return v


# ---------------------------------------------------------------------------
def compute_doob() -> dict:
    rng = np.random.default_rng(19)  # a typical path: it ends near its expectation, 40
    n = 400
    steps = np.where(rng.random(n) < 0.55, 1.0, -1.0)
    x = np.concatenate([[0.0], np.cumsum(steps)])
    coin = martingale.doob_decomposition(x, np.full(n, 0.1))
    d, r = _market()
    # the drift each day as known the day before (the running mean), and the variance forecast (EWMA)
    m = np.concatenate([[r[:250].mean()], np.cumsum(r)[:-1] / np.arange(1, len(r))])
    m[:250] = r[:250].mean()
    X = np.concatenate([[0.0], np.cumsum(r)])
    dec1 = martingale.doob_decomposition(X, m)
    e = r - m
    v = _ewma_var(e)
    M = dec1["M"]
    dec2 = martingale.doob_decomposition(M ** 2, v)
    qv = np.concatenate([[0.0], np.cumsum(e ** 2)])
    step = 21
    t = np.concatenate([[_frac(d)[0]], _frac(d)])
    return _json({"coin_x": x, "coin_A": coin["A"], "coin_M": coin["M"],
                  "t": t[::step], "X": X[::step], "A": dec1["A"][::step], "M": M[::step],
                  "M2": (M ** 2)[::step], "A2": dec2["A"][::step], "N2": dec2["M"][::step], "qv": qv[::step],
                  "X_end": float(X[-1]), "A_end": float(dec1["A"][-1]), "M_end": float(M[-1]),
                  "A2_end": float(dec2["A"][-1]), "qv_end": float(qv[-1]), "M2_end": float(M[-1] ** 2),
                  "ratio_A2_qv": float(dec2["A"][-1] / qv[-1])})


# ---------------------------------------------------------------------------
def compute_measure() -> dict:
    rng = np.random.default_rng(11)
    n, k, p, q = 300, 2000, 0.5, 0.6
    under_p = rng.random((k, n)) < p
    under_q = rng.random((k, n)) < q
    Lp = np.array([martingale.likelihood_ratio(h, p, q) for h in under_p])
    Lq = np.array([martingale.likelihood_ratio(h, p, q) for h in under_q])
    show = 40
    return _json({"n": n, "p": p, "q": q, "paths_p": np.log10(Lp[:show]), "paths_q": np.log10(Lq[:show]),
                  "mean_p": Lp.mean(axis=0), "median_p": np.median(Lp, axis=0), "frac_below_001": float(np.mean(Lp[:, -1] < 0.01)),
                  "mean_end_p": float(Lp[:, -1].mean()), "median_end_p": float(np.median(Lp[:, -1])),
                  "frac_q_above_100": float(np.mean(Lq[:, -1] > 100)), "max_end_p": float(Lp[:, -1].max())})


# ---------------------------------------------------------------------------
def compute_ruin() -> dict:
    games = {"fair coin": 0.5, "European roulette": 18 / 37, "American roulette": 18 / 38}
    a = np.arange(0, 101)
    curves = {k: [martingale.gamblers_ruin(int(i), 100, p) if i > 0 else 0.0 for i in a] for k, p in games.items()}
    # the chance of doubling a bankroll of n units with one-unit bets (timid), against one all-in bet (bold)
    units = [1, 2, 5, 10, 20, 50, 100, 500]
    timid = {k: [martingale.gamblers_ruin(u, 2 * u, p) for u in units] for k, p in games.items()}
    bold = {k: p for k, p in games.items()}
    # a check by simulation: 1,000-unit bankroll, timid play on European roulette, until doubled or ruined (n small)
    rng = np.random.default_rng(3)
    sims = []
    for _ in range(4000):
        w = 10
        while 0 < w < 20:
            w += 1 if rng.random() < 18 / 37 else -1
        sims.append(w == 20)
    return _json({"a": a, "curves": curves, "units": units, "timid": timid, "bold": bold,
                  "sim_timid_10": float(np.mean(sims)), "exact_timid_10": martingale.gamblers_ruin(10, 20, 18 / 37)})


# ---------------------------------------------------------------------------
def compute_stable() -> dict:
    d, r = _market()
    years = d // 10000
    dec = {}
    for y0 in range(1930, 2020, 10):
        m = (years >= y0) & (years < y0 + 10)
        dec[str(y0)] = martingale.stable_mcculloch(r[m])["alpha"]
    full = martingale.stable_mcculloch(r)
    db, rb = _btc_daily()
    btc = martingale.stable_mcculloch(rb)
    horizons = [1, 2, 5, 10, 20, 60]
    alpha_h = []
    for h in horizons:
        n = len(r) // h
        s = r[: n * h].reshape(n, h).sum(axis=1)
        alpha_h.append(martingale.stable_mcculloch(s)["alpha"])
    alpha_hb = []
    for h in horizons[:5]:
        n = len(rb) // h
        s = rb[: n * h].reshape(n, h).sum(axis=1)
        alpha_hb.append(martingale.stable_mcculloch(s)["alpha"])
    hz = [1, 2, 4, 8, 16, 32, 64]
    ms = martingale.return_probability(r, hz)
    msb = martingale.return_probability(rb, hz[:5])
    # within one decade with no crash, the same scaling
    m70 = (years >= 1962) & (years < 1987)
    ms70 = martingale.return_probability(r[m70], hz)
    gauss = martingale.return_probability(np.random.default_rng(0).standard_normal(len(r)) * r.std(), hz)
    return _json({"decades": dec, "full": full, "btc": btc, "horizons": horizons, "alpha_h": alpha_h,
                  "horizons_btc": horizons[:5], "alpha_hb": alpha_hb, "ms": ms, "ms_btc": msb, "ms_6286": ms70,
                  "ms_gauss": gauss, "n_us": int(len(r)), "n_btc": int(len(rb))})


# ---------------------------------------------------------------------------
def compute_nikkei() -> dict:
    f = data.fred("NIKKEI225", start="1994-07-01", through="1995-03-31")
    m = np.isfinite(f["value"])
    d, v = f["date"][m], f["value"][m]
    pick = {str(k): float(v[d == k][0]) for k in (19950113, 19950117, 19950120, 19950123, 19950224, 19950227)
            if np.any(d == k)}
    return _json({"date": d, "t": _frac(d), "value": v, "pick": pick, "low_date": int(d[np.argmin(v)]),
                  "low": float(v.min()), "start": float(v[0])})


# ---------------------------------------------------------------------------
def compute_peeking() -> dict:
    """Under the null (fair +-1 increments, i.e. mean zero), check every day for 2,500 days."""
    rng = np.random.default_rng(21)
    n_paths, n = 2000, 2500
    t_reject, e_reject, t_first, e_max = 0, 0, [], []
    show_t, show_e = [], []
    for k in range(n_paths):
        x = rng.choice([-0.5, 0.5], n)
        cs = np.cumsum(x)
        idx = np.arange(1, n + 1)
        z = cs / (0.5 * np.sqrt(idx))
        hit = np.abs(z[19:]) > 1.96
        if hit.any():
            t_reject += 1
        ep = martingale.EProcess()
        hist = ep.run(x)
        e_max.append(hist.max())
        if hist.max() >= 20:
            e_reject += 1
        if k < 30:
            show_t.append(z[::10])
            show_e.append(np.log10(hist[1:][::10]))
    return _json({"n": n, "paths": n_paths, "t_reject": t_reject / n_paths, "e_reject": e_reject / n_paths,
                  "show_z": show_t, "show_loge": show_e, "e_max_median": float(np.median(e_max))})


# ---------------------------------------------------------------------------
def _sign_test(r, cap=0.9, k=4.0):
    """Bet on continuation: x_t = sign(r_{t-1}) * clip((r_t - m_{t-1}) / (k sd_{t-1}), -cap, cap), with the running
    mean m and an EWMA scale sd known the day before.  Under the null that yesterday's sign does not predict today's
    demeaned return, x has conditional mean zero (approximately: the running mean is a forecast, not the truth)."""
    r = np.asarray(r, float)
    m = np.concatenate([[0.0], np.cumsum(r)[:-1] / np.arange(1, len(r))])
    sd = np.sqrt(_ewma_var(r - m))
    x = np.sign(np.concatenate([[0.0], r[:-1]])) * np.clip((r - m) / (k * sd), -cap, cap)
    x[0] = 0.0
    e = martingale.EProcess()
    return e.run(x)


def compute_eprocess() -> dict:
    d, r = _market()
    out = {}
    for start in (19260701, 19750101, 20000101):
        m = d >= start
        h = _sign_test(r[m])
        dd = d[m]
        cross = np.flatnonzero(h[1:] >= 20)
        out[str(start)] = {"t": _frac(dd)[::5], "loge": np.log10(h[1:])[::5], "max": float(h.max()),
                           "end": float(h[-1]), "cross": int(dd[cross[0]]) if len(cross) else None,
                           "rho1": float(np.corrcoef(r[m][1:], r[m][:-1])[0, 1])}
    db, rb = _btc_daily()
    m = db >= 20180101
    hb = _sign_test(rb[m])
    cross = np.flatnonzero(hb[1:] >= 20)
    out["btc"] = {"t": _frac(db[m]), "loge": np.log10(hb[1:]), "max": float(hb.max()), "end": float(hb[-1]),
                  "cross": int(db[m][cross[0]]) if len(cross) else None, "rho1": float(np.corrcoef(rb[m][1:], rb[m][:-1])[0, 1])}
    return _json(out)


# ---------------------------------------------------------------------------
def compute_envelope() -> dict:
    f = data.fred("NIKKEI225", start="1949-05-01", through="2025-12-31")
    m = np.isfinite(f["value"])
    recs = {"Nikkei 225 (FRED)": pit.seal("fred/NIKKEI225", f["date"][m], f["value"][m])}
    reg = {"sign_continuation_eprocess_us": pit.register("sign_continuation_eprocess_us", inspect.getsource(_sign_test),
                                                         {"data": "Ken French daily market", "starts": [1926, 1975, 2000]},
                                                         trials=3),
           "sign_continuation_eprocess_btc": pit.register("sign_continuation_eprocess_btc", inspect.getsource(_sign_test),
                                                          {"data": "Binance BTCUSDT 1d", "start": 2018}, trials=1)}
    return _json({"sealed": recs, "registered": reg, "trials": pit.trials_so_far()})


# ---------------------------------------------------------------------------
# The expansion (chapters 2-18): conditional means, systems, stopping, convergence, measure, learning to bet
# ---------------------------------------------------------------------------
def _simple():
    kf = data.ken_french_daily()
    d, r = pit.research(kf["date"], kf["mkt"])
    _, rf = pit.research(kf["date"], kf["rf"])
    return d, r, rf


ERAS = ((19260701, 19741231), (19750101, 19991231), (20000101, 20201231))


def compute_condexp() -> dict:
    """E[r_{t+1} | sign r_t] by era (basis points), with a 20-day moving-block bootstrap (200 seeds)."""
    d, r, _ = _simple()
    out = {}
    for lo, hi in ERAS:
        m = (d >= lo) & (d <= hi)
        x = r[m]
        a, b = x[:-1], x[1:]
        up, dn = b[a > 0].mean() * 1e4, b[a < 0].mean() * 1e4
        rng = np.random.default_rng(lo % 997)
        n, blk = len(a), 20
        ups, dns = [], []
        for _ in range(200):
            starts = rng.integers(0, n - blk, n // blk + 1)
            idx = (starts[:, None] + np.arange(blk)).ravel()[:n]
            aa, bb = a[idx], b[idx]
            ups.append(bb[aa > 0].mean() * 1e4)
            dns.append(bb[aa < 0].mean() * 1e4)
        lab = np.sign(a)
        ce = martingale.cond_exp(b, lab)
        out[str(lo)] = {"rho1": float(np.corrcoef(a, b)[0, 1]), "up": float(up), "down": float(dn),
                        "mean": float(b.mean() * 1e4), "up_boot": ups, "down_boot": dns,
                        "up_ci": [float(np.percentile(ups, 2.5)), float(np.percentile(ups, 97.5))],
                        "down_ci": [float(np.percentile(dns, 2.5)), float(np.percentile(dns, 97.5))],
                        "n": int(n), "lab_first": [float(v * 1e4) for v in ce[:3]]}
    toy = martingale.cond_exp([3.0, 0.0, 1.0], np.array([0, 0, 1]), [0.5, 0.3, 0.2])
    return _json({"eras": out, "toy": toy, "toy_mean": float(np.dot([3.0, 0.0, 1.0], [0.5, 0.3, 0.2]))})


def compute_martingales() -> dict:
    """The call E(S_n - 2)^+ on a fair walk, exactly and by simulation; E|S_n| against sqrt(2n/pi)."""
    from scipy.stats import binom
    ns = np.arange(0, 51)
    call, absm = [], []
    for n in ns:
        k = np.arange(n + 1)
        s = 2 * k - n
        p = binom.pmf(k, n, 0.5) if n else np.array([1.0])
        call.append(float((np.maximum(s - 2, 0) * p).sum()))
        absm.append(float((np.abs(s) * p).sum()))
    rng = np.random.default_rng(5)
    S = np.cumsum(rng.choice([-1, 1], (20000, 50)), axis=1)
    sim = np.concatenate([[0.0], np.maximum(S - 2, 0).mean(0)])
    return _json({"n": ns, "call": call, "call_sim": sim, "abs": absm, "abs_approx": np.sqrt(2 * ns / np.pi)})


SYSTEMS = ("flat", "martingale", "dalembert", "labouchere", "fibonacci", "oscar")


def compute_systems() -> dict:
    """Six betting systems, 20,000 sessions of 200 even-money rounds each (table limit 500 units), on a fair coin
    and on European roulette (win 18/37): mean P&L, mean total staked, their ratio, and the shape of the P&L."""
    out = {}
    T, n, limit = 200, 20000, 500.0
    for game, p in (("fair", 0.5), ("roulette", 18 / 37)):
        rng = np.random.default_rng(7 if game == "fair" else 8)
        W = rng.random((n, T)) < p
        res = {}
        for s in SYSTEMS:
            H = martingale.system_stakes(s, W, limit=limit)
            g = (np.where(W, 1.0, -1.0) * H)
            pnl, staked = g.sum(1), H.sum(1)
            ratio = pnl.mean() / staked.mean()
            # the ratio's standard error (delta method)
            cov = np.cov(pnl, staked)
            se = np.sqrt((cov[0, 0] - 2 * ratio * cov[0, 1] + ratio ** 2 * cov[1, 1]) / n) / staked.mean()
            cum = np.cumsum(pnl) / np.cumsum(staked)
            k = np.unique(np.geomspace(10, n, 60).astype(int)) - 1
            q = np.percentile(pnl, [1, 5, 25, 50, 75, 95, 99])
            res[s] = {"pnl": float(pnl.mean()), "pnl_se": float(pnl.std() / np.sqrt(n)), "staked": float(staked.mean()),
                      "ratio": float(ratio), "ratio_se": float(se), "running_k": k + 1, "running": cum[k],
                      "q": q, "skew": float(((pnl - pnl.mean()) ** 3).mean() / pnl.std() ** 3),
                      "p_up": float((pnl > 0).mean()),
                      "path": np.concatenate([[0.0], np.cumsum(g[0])]), "path_staked": np.cumsum(H[0]),
                      "hist": np.histogram(np.clip(pnl, -300, 100), bins=40, range=(-300, 100))[0]}
        out[game] = res
    rng = np.random.default_rng(12)
    demo = rng.random(12) < 0.5
    return _json({"games": out, "edge": -1 / 37, "demo_wins": demo,
                  "demo_stakes": martingale.system_stakes("martingale", demo)})


def compute_firstpassage() -> dict:
    """tau_1 = first time a fair walk reaches +1: 10,000 walks followed to 100,000 steps (in chunks), and 400 short
    walks for the screen.  P(tau > n) against the exact reflection-principle value; the running mean of tau; the
    walk's position at n when it has not yet hit (the 'leaking balance' of optional stopping)."""
    rng = np.random.default_rng(41)
    W, N, G, C = 10000, 100000, 2000, 10000
    checks = [10, 100, 1000, 10000, 100000]
    tau = np.full(W, N + 1, np.int64)
    S_at = {c: np.zeros(W, np.int64) for c in checks}
    lowest = np.zeros(W, np.int64)
    for g0 in range(0, W, G):
        s = np.zeros(G, np.int64)
        hit = np.zeros(G, bool)
        low = np.zeros(G, np.int64)
        for c0 in range(0, N, C):
            steps = (rng.integers(0, 2, (G, C), dtype=np.int8) * 2 - 1)
            cs = s[:, None] + np.cumsum(steps, axis=1, dtype=np.int32)
            reach = cs >= 1
            first = np.where(reach.any(1), reach.argmax(1), C)
            new = (~hit) & (first < C)
            idx = np.arange(C)
            still = ~hit
            # the lowest point before the hit (or so far)
            masked = np.where(idx[None, :] < first[:, None], cs, np.iinfo(np.int32).max)
            low = np.where(still, np.minimum(low, masked.min(1)), low)
            tau[g0:g0 + G][new] = c0 + first[new] + 1
            for c in checks:
                if c0 < c <= c0 + C:
                    S_at[c][g0:g0 + G] = np.where(hit | (first < c - c0), 1, cs[:, c - c0 - 1])
            hit |= new
            s = cs[:, -1]
        lowest[g0:g0 + G] = low
    grid = np.unique(np.geomspace(1, N, 50).astype(int))
    surv = np.array([(tau > n).mean() for n in grid])
    exact = martingale.first_passage_survival(grid)
    order_mean = np.cumsum(np.minimum(tau, N)) / np.arange(1, W + 1)
    k = np.unique(np.geomspace(1, W, 80).astype(int)) - 1
    capped = {str(n): float(np.minimum(tau, n).mean()) for n in (100, 1000, 10000, 100000)}
    hists = {}
    for c in checks[:4]:
        v = S_at[c]
        hists[str(c)] = {"frac_hit": float((v == 1).mean()), "mean": float(v.mean()),
                         "hist": np.histogram(np.clip(v, -150, 1), bins=np.arange(-150.5, 2.5, 3))[0],
                         "min": int(v.min())}
    hit_low = lowest[tau <= N]
    # 400 short walks for the screen (hit times and paths up to 300 steps)
    rs = np.random.default_rng(42)
    short = np.cumsum(rs.choice([-1, 1], (400, 300)), axis=1)
    reach = short >= 1
    tshort = np.where(reach.any(1), reach.argmax(1) + 1, 0)
    return _json({"grid": grid, "surv": surv, "exact": exact, "p100": float((tau > 100).mean()),
                  "p100_exact": float(martingale.first_passage_survival(100)),
                  "p10000": float((tau > 10000).mean()), "frac_hit_N": float((tau <= N).mean()),
                  "running_k": k + 1, "running_mean": order_mean[k], "capped_mean": capped, "hists": hists,
                  "low_median": float(np.median(hit_low)), "low_p99": float(np.percentile(hit_low, 1)),
                  "short_paths": short[:120], "short_tau": tshort, "short_frac": [float((tshort > 0)[:k_].mean())
                                                                                for k_ in (50, 100, 200, 400)],
                  "frac_by_n": [float(((tshort > 0) & (tshort <= n)).mean()) for n in (10, 50, 100, 300)]})


def compute_patterns() -> dict:
    """Waiting times for HH, HT, HTH, HHH (200,000 fair sequences each), Penney's THH against HHT, against the
    House's pattern_wait and penney_odds."""
    rng = np.random.default_rng(13)
    n, L = 200000, 160
    out = {}
    for pat in ("HH", "HT", "HTH", "HHH"):
        X = rng.random((n, L)) < 0.5
        k = len(pat)
        hit = np.ones((n, L - k + 1), bool)
        for j, ch in enumerate(pat):
            hit &= X[:, j:L - k + 1 + j] == (ch == "H")
        found = hit.any(1)
        t = np.where(found, hit.argmax(1) + k, L)
        out[pat] = {"mean": float(t.mean()), "se": float(t.std() / np.sqrt(n)), "theory": martingale.pattern_wait(pat),
                    "unfound": int((~found).sum()), "hist": np.bincount(np.minimum(t, 30), minlength=31)[:31]}
    X = rng.random((n, L)) < 0.5
    a = X[:, :-2] & X[:, 1:-1] & ~X[:, 2:]           # HHT ending
    b = ~X[:, :-2] & X[:, 1:-1] & X[:, 2:]           # THH ending
    ta = np.where(a.any(1), a.argmax(1), L)
    tb = np.where(b.any(1), b.argmax(1), L)
    return _json({"waits": out, "penney_sim": float((tb < ta).mean()), "penney_exact": martingale.penney_odds("HHT", "THH"),
                  "abra": martingale.pattern_wait("ABRACADABRA", 26)})


def compute_doubling() -> dict:
    """1,000 doublers with bankroll 1,023 (ten doublings), 3,000 sessions each: a session wins 1 with probability
    1023/1024 and loses 1,023 otherwise (checked against the House's doubling() on real coin flips)."""
    rng = np.random.default_rng(23)
    n, S, k = 1000, 3000, 10
    lose = rng.random((n, S)) < 2.0 ** -k
    pnl = np.cumsum(np.where(lose, -(2 ** k - 1), 1.0), axis=1)
    ruined_by = np.cumsum(lose, axis=1) > 0
    check = [martingale.doubling(rng.random(60) < 0.5, bankroll=1023, target=1024) for _ in range(20000)]
    first = rng.geometric(2.0 ** -k, 200000)
    step = 10
    return _json({"sessions": np.arange(step, S + 1, step), "paths": pnl[:80, step - 1::step],
                  "mean": pnl.mean(0)[step - 1::step], "median": np.median(pnl, 0)[step - 1::step],
                  "mean_se_end": float(pnl[:, -1].std() / np.sqrt(n)), "mean_end": float(pnl[:, -1].mean()),
                  "median_end": float(np.median(pnl[:, -1])), "frac_ruined": float(ruined_by[:, -1].mean()),
                  "frac_ruined_theory": float(1 - (1 - 2.0 ** -k) ** S),
                  "check_ruin": float(np.mean([c["ruined"] for c in check])), "check_theory": 2.0 ** -k,
                  "first_ruin_mean": float(first.mean()), "hist_end": np.histogram(pnl[:, -1], bins=30)[0],
                  "hist_edges": np.histogram(pnl[:, -1], bins=30)[1]})


def compute_nikkei_doubling() -> dict:
    """Schematic, not Leeson's book: hold one unit of the Nikkei from 1 July 1994; after every down day double the
    position, and go back to one unit once the account is back at its high.  P&L in index points times units,
    against a capital of 20,000 (one unit's notional, roughly); the same rule capped at 16 units."""
    nk = load("nikkei")
    d, v = np.asarray(nk["date"]), np.asarray(nk["value"], float)
    capital = 20000.0
    res = {}
    for name, cap in (("doubling", np.inf), ("capped", 16.0)):
        u, pnl, high = 1.0, 0.0, 0.0
        U, P = [u], [0.0]
        for t in range(1, len(v)):
            pnl += u * (v[t] - v[t - 1])
            if v[t] < v[t - 1]:
                u = min(2 * u, cap)
            if pnl >= high:
                high, u = pnl, 1.0
            U.append(u)
            P.append(pnl)
        P, U = np.array(P), np.array(U)
        cross = np.flatnonzero(P <= -capital)
        res[name] = {"pnl": P, "units": U, "cross": int(d[cross[0]]) if len(cross) else None,
                     "min": float(P.min()), "min_date": int(d[np.argmin(P)]), "max_units": float(U.max()),
                     "end": float(P[-1])}
    return _json({"date": d, "t": _frac(d), "value": v, "capital": capital, **res})


def compute_ruin_duration() -> dict:
    """Expected duration from 50 between 0 and 100: a(b - a) = 2,500 on a fair coin (from S_n^2 - n); 4,000 games
    simulated, and 120 games kept for the screen (fair and European roulette)."""
    out = {}
    for game, p in (("fair", 0.5), ("roulette", 18 / 37)):
        rng = np.random.default_rng(31 if game == "fair" else 32)
        n = 4000
        w = np.full(n, 50)
        tau = np.zeros(n, int)
        alive = np.ones(n, bool)
        paths = [[50] for _ in range(120)]
        t = 0
        while alive.any():
            t += 1
            stepv = np.where(rng.random(n) < p, 1, -1)
            w = np.where(alive, w + stepv, w)
            ended = alive & ((w <= 0) | (w >= 100))
            tau[ended] = t
            alive &= ~ended
            if t % 25 == 0:
                for i in range(120):
                    paths[i].append(int(w[i]))
        q = (1 - p) / p
        theory = 2500.0 if p == 0.5 else 50 / (1 - 2 * p) - 100 / (1 - 2 * p) * (1 - q ** 50) / (1 - q ** 100)
        out[game] = {"mean": float(tau.mean()), "se": float(tau.std() / np.sqrt(n)), "theory": float(theory),
                     "frac_top": float((w >= 100).mean()), "paths": paths,
                     "tau": tau[:120], "top": (w >= 100)[:120]}
    return _json(out)


def compute_polya() -> dict:
    """10,000 Polya urns of 2,000 draws from one red and one blue; 100 kept for the screen.  The limits against
    Uniform(0, 1); and Doob's upcrossing bound for [-3, 3] on 3,000 Gaussian walks of 1,000 steps."""
    show = martingale.polya_urn(2000, n_urns=100, seed=3)
    rng = np.random.default_rng(4)
    R, tot = np.ones(10000), 2.0
    for _ in range(2000):
        R += rng.random(10000) < R / tot
        tot += 1
    lim = np.sort(R / tot)
    ks = float(np.max(np.abs(lim - (np.arange(1, 10001) - 0.5) / 10000)))
    # Gaussian steps, so a trade overshoots its levels and Doob's bound is strict; the screen's walk is the first
    # seed with three to five upcrossings of [-3, 3]
    for seed in range(9, 200):
        walk = np.concatenate([[0.0], np.cumsum(np.random.default_rng(seed).standard_normal(600))])
        u = martingale.upcrossings(walk, -3, 3)
        if 3 <= u["U"] <= 5:
            break
    walks = np.concatenate([np.zeros((3000, 1)), np.cumsum(np.random.default_rng(10).standard_normal((3000, 1000)),
                                                            axis=1)], axis=1)
    Us = np.array([martingale.upcrossings(w_, -3, 3)["U"] for w_ in walks])
    bound = np.mean(np.maximum(-3 - walks[:, -1], 0)) / 6  # E(M_n - a)^- / (b - a)
    return _json({"show": show[:, ::10], "limits_hist": np.histogram(lim, bins=20, range=(0, 1))[0], "ks": ks,
                  "p_above_09": float((lim > 0.9).mean()), "walk": walk, "U": u["U"], "trader": u["wealth"],
                  "starts": u["starts"], "ends": u["ends"], "mean_U": float(Us.mean()), "bound_U": float(bound),
                  "se_U": float(Us.std() / np.sqrt(len(Us)))})


def compute_drift_posterior() -> dict:
    """A Bayesian learner of the market's daily mean: prior N(0, (10 bp)^2), each day's return r_t ~ N(mu, s_t^2)
    with s_t the EWMA forecast made the day before.  The posterior mean is a Doob martingale under the model; its
    band narrows like 1/sqrt(t)."""
    d, r, _ = _simple()
    s2 = _ewma_var(r - r[:250].mean())
    prec0 = 1 / 0.001 ** 2
    prec = prec0 + np.cumsum(1 / s2)
    mean = np.cumsum(r / s2) / prec
    sd = 1 / np.sqrt(prec)
    t = _frac(d)
    step = 21
    return _json({"t": t[::step], "mean_ann": (mean * 252)[::step], "lo_ann": ((mean - 1.96 * sd) * 252)[::step],
                  "hi_ann": ((mean + 1.96 * sd) * 252)[::step], "end_mean": float(mean[-1] * 252),
                  "end_half": float(1.96 * sd[-1] * 252), "sample_mean": float(r.mean() * 252),
                  "half_1936": float(1.96 * sd[np.searchsorted(d, 19360101)] * 252),
                  "half_1976": float(1.96 * sd[np.searchsorted(d, 19760101)] * 252)})


def compute_ivey_sim() -> dict:
    """Simulated punto banco with the court's figures (Ivey v Genting [2014] EWHC 3394 (QB)): betting player every
    hand the drift is -1.24% per unit; a signal known before the deal (the sorted card) splits hands into two kinds
    with means +5.26% and -7.74%, so a stake that picks its side by the signal earns +6.5% per unit.  Ties ignored."""
    rng = np.random.default_rng(57)
    n = 10000
    sig = rng.random(n) < 0.5
    mu = np.where(sig, 0.0526, -0.0774)
    xi = np.where(rng.random(n) < (1 + mu) / 2, 1.0, -1.0)
    X = np.concatenate([[0.0], np.cumsum(xi)])
    AF = -0.0124 * np.arange(n + 1)
    AG = np.concatenate([[0.0], np.cumsum(mu)])
    H = np.where(sig, 1.0, -1.0)
    Y = martingale.martingale_transform(H, xi)
    AY = np.concatenate([[0.0], np.cumsum(H * mu)])
    step = 20
    return _json({"n": n, "X": X[::step], "AF": AF[::step], "AG": AG[::step], "Y": Y[::step], "AY": AY[::step],
                  "var_MF": float(np.var(np.diff(X - AF))), "var_MG": float(np.var(np.diff(X - AG))),
                  "Y_end": float(Y[-1]), "AY_end": float(AY[-1]), "X_end": float(X[-1])})


def compute_esscher() -> dict:
    """The Esscher measure of US daily log returns 1926-2020: Q tilts P by e^(theta r) so that E_Q[e^r] = e^(rf)."""
    d, r, rf = _simple()
    lr = np.log1p(r)
    target = float(np.log1p(rf).mean())
    th, w = martingale.esscher_tilt(lr, target)
    q01 = np.quantile(lr, 0.01)
    edges = np.linspace(-0.08, 0.08, 41)
    hp = np.histogram(np.clip(lr, -0.0799, 0.0799), bins=edges)[0] / len(lr)
    hq = np.histogram(np.clip(lr, -0.0799, 0.0799), bins=edges, weights=w)[0]
    return _json({"theta": float(th), "mean_p": float(lr.mean() * 1e4), "mean_q": float((w @ lr) * 1e4),
                  "rf": target * 1e4, "tail_p": float((lr < q01).mean()), "tail_q": float(w[lr < q01].sum()),
                  "q01": float(q01), "edges": edges, "hist_p": hp, "hist_q": hq,
                  "crash_1987_weight": float(w[np.argmin(lr)] * len(lr))})


def compute_radon() -> dict:
    """Dyadic Radon-Nikodym on the unit square: P uniform, Q with density (1 + 2xy)/1.5; Z_n = Q(cell)/P(cell) on
    the 2^n x 2^n grid, a P-martingale converging to dQ/dP; and a singular Q on the diagonal."""
    levels = {}
    for n in range(1, 6):
        k = 2 ** n
        e = np.linspace(0, 1, k + 1)
        gx = (e[1:] ** 2 - e[:-1] ** 2)
        Z = (np.ones((k, k)) / k ** 2 + 2 * np.outer(gx, gx) / 4) / 1.5 * k ** 2
        levels[str(n)] = Z
    # the martingale property: each parent is the average of its four children
    err = max(float(np.abs(levels[str(n)] - levels[str(n + 1)].reshape(2 ** n, 2, 2 ** n, 2).mean((1, 3))).max())
              for n in range(1, 5))
    c = (np.arange(32) + 0.5) / 32
    dens = (1 + 2 * np.outer(c, c)) / 1.5
    return _json({"levels": levels, "martingale_err": err, "max_gap_32": float(np.abs(levels["5"] - dens).max()),
                  "singular_peak": [2 ** n for n in range(1, 6)]})


def compute_kakutani() -> dict:
    """Kakutani's dichotomy, simulated: L_n = dQ/dP on n tosses under P (fair coin) for Q = 0.6 every toss
    (singular: L -> 0) and for q_k = 1/2 + 0.2/k (equivalent: L converges to a positive limit with mean one)."""
    rng = np.random.default_rng(61)
    n, m = 10000, 2000
    k = np.arange(1, n + 1)
    out = {}
    for name, q in (("constant", np.full(n, 0.6)), ("fading", 0.5 + 0.2 / k)):
        logL = np.zeros(m)
        keep = []
        for c0 in range(0, n, 1000):
            H = rng.random((m, 1000)) < 0.5
            qq = q[c0:c0 + 1000]
            stepl = np.where(H, np.log(qq / 0.5), np.log((1 - qq) / 0.5))
            cl = logL[:, None] + np.cumsum(stepl, axis=1)
            keep.append(cl[:40, ::20])
            logL = cl[:, -1]
        L = np.exp(logL)
        rho = martingale.hellinger_affinity(0.5, q)
        out[name] = {"paths": np.concatenate(keep, axis=1) / np.log(10), "median_log10": float(np.median(logL) / np.log(10)),
                     "mean_L": float(L.mean()), "frac_pos": float((L > 1e-3).mean()),
                     "log10_affinity_prod": float(np.log10(rho).sum()), "q": [float(q[0]), float(q[-1])]}
    out["kl_per_toss"] = float(0.5 * np.log(0.5 / 0.6) + 0.5 * np.log(0.5 / 0.4))
    return _json(out)


def compute_ecf() -> dict:
    """Koutrouvelis's regression on the empirical characteristic function (US daily log returns and a Gaussian of
    the same size), with 50 bootstrap resamples; kurtosis of h-day sums for h = 1..60 (a stable law keeps its shape,
    a finite variance makes the kurtosis decay)."""
    d, r = _market()
    rng = np.random.default_rng(71)
    g = rng.standard_normal(len(r))
    us, ga = martingale.ecf_alpha(r), martingale.ecf_alpha(g)
    boot = [martingale.ecf_alpha(r[rng.integers(0, len(r), len(r))])["alpha"] for _ in range(50)]
    hs = np.array([1, 2, 3, 5, 8, 10, 15, 20, 30, 40, 60])

    def kurt(x):
        x = x - x.mean()
        return float((x ** 4).mean() / (x ** 2).mean() ** 2 - 3)

    ku, kg = [], []
    for h in hs:
        n = len(r) // h
        ku.append(kurt(r[: n * h].reshape(n, h).sum(1)))
        kg.append(kurt(g[: n * h].reshape(n, h).sum(1)))
    return _json({"us": us, "gauss": ga, "boot": boot, "boot_lo": float(np.percentile(boot, 2.5)),
                  "boot_hi": float(np.percentile(boot, 97.5)), "h": hs, "kurt_us": ku, "kurt_gauss": kg})


def compute_stable_mle() -> dict:
    """Maximum likelihood for a stable law (alpha, beta, scale, location; scipy's levy_stable, S1), Nelder-Mead
    from the Gaussian corner, every iterate logged: three seeds, each a random 1,500-day subsample of US daily log
    returns (standardized by the full sample's interquartile range).  Resumable per seed."""
    from scipy.optimize import minimize
    from scipy.stats import levy_stable

    levy_stable.parameterization = "S1"
    d, r = _market()
    z = (r - np.median(r)) / (np.percentile(r, 75) - np.percentile(r, 25))
    params = {"n": 1500, "seeds": [1, 2, 3], "maxfev": 150}
    part = CACHE.partial("stable_mle", params)
    for s in params["seeds"]:
        key = str(s)
        if key in part:
            continue
        x = np.random.default_rng(100 + s).choice(z, params["n"], replace=False)
        log = []

        def nll(th):
            a, b, sc, loc = th
            if not (0.6 < a <= 2.0 and -1 <= b <= 1 and sc > 0):
                return 1e9
            v = -levy_stable.logpdf(x, a, b, loc, sc).sum()
            v = float(v) if np.isfinite(v) else 1e9
            log.append([float(a), float(b), float(sc), float(loc), v])
            return v

        x0 = np.array([1.95, 0.0, 0.45, 0.0])
        simplex = np.vstack([x0, x0 + np.diag([-0.25, 0.3, 0.1, 0.05])])
        res = minimize(nll, x0=x0, method="Nelder-Mead",
                       options={"maxfev": params["maxfev"], "xatol": 1e-3, "fatol": 1e-2, "initial_simplex": simplex})
        mc = martingale.stable_mcculloch(x)
        part[key] = {"log": log, "alpha": float(res.x[0]), "beta": float(res.x[1]), "scale": float(res.x[2]),
                     "nll": float(res.fun), "mcculloch": mc["alpha"]}
    runs = [part[str(s)] for s in params["seeds"]]
    return _json({"runs": runs, "alphas": [u["alpha"] for u in runs], "mcc": [u["mcculloch"] for u in runs]})


def compute_peeking_curve() -> dict:
    """The peeking experiment again (same seed and draws as ``peeking``), with the share of games already rejected
    on each day, for the live counters."""
    rng = np.random.default_rng(21)
    n_paths, n = 2000, 2500
    X = np.array([rng.choice([-0.5, 0.5], n) for _ in range(n_paths)])
    cs = np.cumsum(X, axis=1)
    z = cs / (0.5 * np.sqrt(np.arange(1, n + 1)))
    hit = np.abs(z) > 1.96
    hit[:, :19] = False
    t_first = np.where(hit.any(1), hit.argmax(1), n)
    lams = np.array([-0.5, -0.25, -0.1, -0.05, 0.05, 0.1, 0.25, 0.5])
    logw = np.cumsum(np.log1p(X[:, :, None] * lams[None, None, :]), axis=1)
    E = np.exp(logw).mean(2)
    eh = E >= 20
    e_first = np.where(eh.any(1), eh.argmax(1), n)
    days = np.arange(0, n + 1, 25)
    return _json({"days": days, "t_frac": [float((t_first < k).mean()) for k in days],
                  "e_frac": [float((e_first < k).mean()) for k in days],
                  "t_final": float((t_first < n).mean()), "e_final": float((e_first < n).mean())})


def _bettor_run(kind, X, mu_x=None, var_x=None):
    """Wealth paths of one bettor on the increments X (reps, T); returns the first time wealth >= 20 (or T)."""
    reps, T = X.shape
    first = np.full(reps, T)
    if kind == "mixture":
        lams = np.array([-0.5, -0.25, -0.1, -0.05, 0.05, 0.1, 0.25, 0.5])
        logw = np.zeros((reps, len(lams)))
    elif kind == "ons":
        b = martingale.ONSBettor(reps)
    elif kind == "agrapa":
        b = martingale.AGrapaBettor(reps)
    else:
        lam = np.clip(mu_x / (var_x + mu_x ** 2), -0.5, 0.5) if mu_x else 0.0
        logk = np.zeros(reps)
    for t in range(T):
        x = X[:, t]
        if kind == "mixture":
            logw += np.log1p(lams * x[:, None])
            w = np.exp(logw).mean(1)
        elif kind in ("ons", "agrapa"):
            w = b.update(x)
        else:
            logk += np.log1p(lam * x)
            w = np.exp(logk)
        newly = (w >= 20) & (first == T)
        first[newly] = t + 1
    return first


def compute_learner() -> dict:
    """Learning to bet.  (1) One ONS bettor on 10,000 days of a strategy with a daily Sharpe of 0.05 (x = 0.25 (SR +
    z), clipped): its stake and log wealth, for the replay.  (2) Four bettors (the House's fixed-stake mixture, ONS,
    aGRAPA, the oracle Kelly) x four edges x 8 seeds x 100 runs: rejection rates and times at 1/20.  (3) ONS on the
    sign-continuation test of the hook, against the mixture."""
    T = 10000
    rng = np.random.default_rng(77)
    x = np.clip(0.25 * (0.05 + rng.standard_normal(T)), -0.95, 0.95)
    b = martingale.ONSBettor()
    lam, logw = [], []
    for v in x:
        lam.append(float(b.lam))
        logw.append(float(b.update(v)))
    lam, logw = np.array(lam), np.log10(np.array(logw))
    kelly = 0.0125 / (0.0625 + 0.0125 ** 2)
    grid = {}
    params = {"T": T, "edges": [0.0, 0.02, 0.05, 0.1], "seeds": 8, "reps": 100}
    part = CACHE.partial("learner", params)
    for e in params["edges"]:
        for kind in ("mixture", "ons", "agrapa", "kelly"):
            key = f"{kind}|{e}"
            if key in part:
                continue
            per_seed = []
            for s in range(params["seeds"]):
                rs = np.random.default_rng(1000 + s)
                X = np.clip(0.25 * (e + rs.standard_normal((params["reps"], T))), -0.95, 0.95)
                f = _bettor_run(kind, X, mu_x=0.25 * e, var_x=0.0625)
                per_seed.append({"rate": float((f < T).mean()), "median": float(np.median(f))})
            part[key] = per_seed
    for k in [f"{kind}|{e}" for e in params["edges"] for kind in ("mixture", "ons", "agrapa", "kelly")]:
        grid[k] = part[k]
    real = {}
    d, r = _market()
    for start in (19260701, 19750101, 20000101):
        m = d >= start
        rr = r[m]
        mm = np.concatenate([[0.0], np.cumsum(rr)[:-1] / np.arange(1, len(rr))])
        sd = np.sqrt(_ewma_var(rr - mm))
        xs = np.sign(np.concatenate([[0.0], rr[:-1]])) * np.clip((rr - mm) / (4 * sd), -0.9, 0.9)
        xs[0] = 0.0
        bo = martingale.ONSBettor()
        w = np.array([float(bo.update(v)) for v in xs])
        cross = np.flatnonzero(w >= 20)
        real[str(start)] = {"max": float(w.max()), "cross": int(d[m][cross[0]]) if len(cross) else None,
                            "end_log10": float(np.log10(w[-1]))}
    db, rb = _btc_daily()
    m = db >= 20180101
    rr = rb[m]
    mm = np.concatenate([[0.0], np.cumsum(rr)[:-1] / np.arange(1, len(rr))])
    sd = np.sqrt(_ewma_var(rr - mm))
    xs = np.sign(np.concatenate([[0.0], rr[:-1]])) * np.clip((rr - mm) / (4 * sd), -0.9, 0.9)
    xs[0] = 0.0
    bo = martingale.ONSBettor()
    w = np.array([float(bo.update(v)) for v in xs])
    cross = np.flatnonzero(w >= 20)
    real["btc"] = {"max": float(w.max()), "cross": int(db[m][cross[0]]) if len(cross) else None,
                   "end_log10": float(np.log10(w[-1]))}
    return _json({"lam": lam[::20], "logw": logw[::20], "steps": np.arange(0, T, 20), "kelly": kelly,
                  "lam_end": float(np.mean(lam[-1000:])), "logw_end": float(logw[-1]),
                  "cross_day": int(np.argmax(logw >= np.log10(20))) if (logw >= np.log10(20)).any() else None,
                  "theory_days": float(2 * np.log(20) / 0.05 ** 2), "grid": grid, "edges": params["edges"],
                  "real": real})


def compute_confseq() -> dict:
    """A betting confidence sequence for Bitcoin's mean daily log return, 2018-2020 (returns clipped to +-20%)."""
    db, rb = _btc_daily()
    m = db >= 20180101
    r = np.clip(rb[m], -0.2, 0.2)
    x = (r + 0.2) / 0.4
    grid = np.linspace(0.3, 0.7, 401)
    cs = martingale.betting_cs(x, grid, alpha=0.05)
    lo, hi = cs["lower"] * 0.4 - 0.2, cs["upper"] * 0.4 - 0.2
    t = _frac(db[m])
    run_mean = np.cumsum(r) / np.arange(1, len(r) + 1)
    return _json({"t": t, "lo_bp": lo * 1e4, "hi_bp": hi * 1e4, "mean_bp": run_mean * 1e4,
                  "end": [float(lo[-1] * 1e4), float(hi[-1] * 1e4)], "covers0": bool(lo[-1] <= 0 <= hi[-1]),
                  "n": int(len(r))})


def compute_casino() -> dict:
    """The house's side of even-money roulette bets (European wheel): P(the house is behind after N unit bets),
    exactly (binomial), by the normal approximation, and Azuma's bound exp(-(N/37)^2 / (2N)).  And the spread of a
    month's hold that spin-by-spin luck alone would give, against Nevada's observed 3.15 points (UNLV, 2004-2026)."""
    from scipy.stats import binom, norm
    Ns = [100, 1000, 10000, 100000]
    rows = []
    for N in Ns:
        exact = float(binom.sf(N // 2, N, 18 / 37))  # the players win more than half the bets
        mu, sd = N / 37, np.sqrt(N * (1 - 1 / 37 ** 2))
        rows.append({"N": N, "exact": exact, "normal": float(norm.sf(mu / sd)), "azuma": float(np.exp(-(N / 37) ** 2 / (2 * N))),
                     "z": float(mu / sd)})
    rng = np.random.default_rng(83)
    sims = {}
    for N in (100, 1000, 10000):
        pl = rng.binomial(N, 18 / 37, 20000)
        sims[str(N)] = float((pl > N / 2).mean())
    edge_dz = 2 / 38
    turnover = 0.1734 / edge_dz
    sd_even = np.sqrt(1 - edge_dz ** 2)
    sd_straight = np.sqrt(36 ** 2 / 38 + 1 * 37 / 38 - (-edge_dz) ** 2)
    need_even = (turnover * sd_even / 0.0315) ** 2
    need_straight = (turnover * sd_straight / 0.0315) ** 2
    return _json({"rows": rows, "sims": sims, "turnover": float(turnover), "edge_dz": edge_dz,
                  "sd_even": float(sd_even), "sd_straight": float(sd_straight), "need_even": float(need_even),
                  "need_straight": float(need_straight)})


def compute_beliefs() -> dict:
    """Augenblick and Rabin's test of a martingale belief: expected squared movement = expected reduction in
    uncertainty pi(1 - pi).  Best-of-21 forecasts (Bayesian), and a forecaster who overreacts to each toss by 30%."""
    from scipy.stats import binom
    rng = np.random.default_rng(91)
    n = 20000
    h = rng.random((n, 21)) < 0.5
    heads = np.concatenate([np.zeros((n, 1)), np.cumsum(h, 1)], axis=1)
    k = np.arange(22)
    need = 11 - heads
    left = 21 - k
    p = binom.sf(need - 1, left, 0.5)
    p = np.where(need <= 0, 1.0, np.where(need > left, 0.0, p))
    over = np.empty_like(p)
    over[:, 0] = p[:, 0]
    for t in range(1, 22):
        over[:, t] = np.clip(over[:, t - 1] + 1.3 * (p[:, t] - p[:, t - 1]), 0, 1)
    over[:, -1] = p[:, -1]

    def ratio(f):
        mv = (np.diff(f, axis=1) ** 2).sum(1)
        red = f[:, 0] * (1 - f[:, 0]) - f[:, -1] * (1 - f[:, -1])
        rt = mv.mean() / red.mean()
        se = np.std(mv - rt * red) / np.sqrt(n) / red.mean()
        return float(rt), float(se)

    rb, sb = ratio(p)
    ro, so = ratio(over)
    return _json({"bayes": rb, "bayes_se": sb, "over": ro, "over_se": so})


def compute_ebh() -> dict:
    """200 strategies watched every day for 2,520 days (20 with a true daily Sharpe of 0.08, 180 with none), each by
    an ONS e-process; e-BH at 10% each day, against BH on each day's t-test p-values.  20 seeds.  The false
    discovery proportion on each day, and when the desk stops on the first day it has at least ten discoveries."""
    from scipy.stats import norm
    K, T, S, true = 200, 2520, 20, 20
    days = np.arange(21, T + 1, 21)
    fdp_e, fdp_b, disc_e, disc_b, stop_e, stop_b = [], [], [], [], [], []
    for s in range(S):
        rng = np.random.default_rng(500 + s)
        mu = np.zeros(K)
        mu[:true] = 0.08
        b = martingale.ONSBettor(K)
        csum = np.zeros(K)
        fe, fb, de, dbb = [], [], [], []
        se_, sb_ = None, None
        for t in range(1, T + 1):
            z = mu + rng.standard_normal(K)
            b.update(np.clip(0.25 * z, -0.95, 0.95))
            csum += z
            if t % 21:
                continue
            e = np.exp(b.logw)
            rej_e = martingale.e_bh(e, 0.1)
            pv = norm.sf(csum / np.sqrt(t))
            o = np.argsort(pv)
            ok = np.flatnonzero(pv[o] <= 0.1 * np.arange(1, K + 1) / K)
            rej_b = o[: ok.max() + 1] if len(ok) else o[:0]
            fe.append(float((rej_e >= true).sum() / max(len(rej_e), 1)))
            fb.append(float((rej_b >= true).sum() / max(len(rej_b), 1)))
            de.append(len(rej_e))
            dbb.append(len(rej_b))
            if se_ is None and len(rej_e) >= 10:
                se_ = fe[-1]
            if sb_ is None and len(rej_b) >= 10:
                sb_ = fb[-1]
        fdp_e.append(fe), fdp_b.append(fb), disc_e.append(de), disc_b.append(dbb)
        stop_e.append(0.0 if se_ is None else se_)
        stop_b.append(0.0 if sb_ is None else sb_)
    fdp_e, fdp_b = np.array(fdp_e), np.array(fdp_b)
    return _json({"days": days, "fdp_e": fdp_e, "fdp_b": fdp_b, "disc_e": np.array(disc_e), "disc_b": np.array(disc_b),
                  "fdr_e_max": float(fdp_e.mean(0).max()), "fdr_b_max": float(fdp_b.mean(0).max()),
                  "stop_e": float(np.mean(stop_e)), "stop_b": float(np.mean(stop_b)),
                  "end_disc_e": float(np.mean(disc_e, 0)[-1]), "end_disc_b": float(np.mean(disc_b, 0)[-1])})


def compute_numeraire() -> dict:
    """The numeraire bridge: 2,520 days of a strategy with a daily Sharpe of 0.08 (x = 0.25 (SR + z), clipped); the
    Kelly bettor's wealth at the log-optimal stake, which is also the log-optimal e-variable against the null of
    mean zero (Larsson, Ramdas and Ruf 2025)."""
    rng = np.random.default_rng(88)
    x = np.clip(0.25 * (0.08 + rng.standard_normal(2520)), -0.95, 0.95)
    grid = np.linspace(0, 0.5, 501)
    big = np.clip(0.25 * (0.08 + np.random.default_rng(89).standard_normal(200000)), -0.95, 0.95)
    g = np.array([np.log1p(l * big).mean() for l in grid])
    lam = float(grid[np.argmax(g)])
    w = np.concatenate([[0.0], np.cumsum(np.log1p(lam * x))]) / np.log(10)
    return _json({"lam": lam, "log10w": w[::5], "days": np.arange(0, 2521, 5), "growth": float(g.max())})


def compute_envelope_ons() -> dict:
    """Registers the expansion's new real-data tests: the ONS sign-continuation e-processes (US from 1926, 1975,
    2000; Bitcoin from 2018: four trials) and the Bitcoin confidence sequence (one)."""
    reg = {"sign_continuation_ons": pit.register("sign_continuation_ons", inspect.getsource(compute_learner),
                                                 {"data": "Ken French daily market; Binance BTCUSDT 1d",
                                                  "starts": [1926, 1975, 2000, 2018]}, trials=4),
           "btc_mean_confseq": pit.register("btc_mean_confseq", inspect.getsource(compute_confseq),
                                            {"data": "Binance BTCUSDT 1d", "start": 2018}, trials=1)}
    return _json({"registered": reg, "trials": pit.trials_so_far()})


ITEMS = {"doob": compute_doob, "measure": compute_measure, "ruin": compute_ruin, "stable": compute_stable,
         "nikkei": compute_nikkei, "peeking": compute_peeking, "eprocess": compute_eprocess, "envelope": compute_envelope,
         "condexp": compute_condexp, "martingales": compute_martingales, "systems": compute_systems,
         "firstpassage": compute_firstpassage, "patterns": compute_patterns, "doubling": compute_doubling,
         "nikkei_doubling": compute_nikkei_doubling, "ruin_duration": compute_ruin_duration, "polya": compute_polya,
         "drift_posterior": compute_drift_posterior, "ivey_sim": compute_ivey_sim, "esscher": compute_esscher,
         "radon": compute_radon, "kakutani": compute_kakutani, "ecf": compute_ecf, "stable_mle": compute_stable_mle,
         "peeking_curve": compute_peeking_curve, "learner": compute_learner, "confseq": compute_confseq,
         "casino": compute_casino, "beliefs": compute_beliefs, "ebh": compute_ebh, "numeraire": compute_numeraire, "envelope_ons": compute_envelope_ons}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
