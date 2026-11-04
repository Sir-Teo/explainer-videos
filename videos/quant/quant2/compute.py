"""Every number in Part 2 (The Machinery of Markets), computed and cached in .cache/quant2/.

    python -m videos.quant.quant2.compute [items] [--force]

Items (each seeded; seconds on a laptop):

* ``margin``    leveraged long BTC perpetuals (2x, 3x, 10x) opened on 1 March 2020 on Binance, marked to market hour
                by hour with funding, through the crash of 12 March: equity, maintenance margin, liquidations;
* ``netting``   a day of trades among 25 clearing members: gross, bilateral-net and centrally netted obligations;
* ``auction``   a closing auction: 300 limit orders, demand and supply, the price that executes the most;
* ``funding``   the perpetual's funding rate through 2020 and what holding one coin long cost;
* ``repo``      the repo market in September 2019 (FRED): SOFR, fed funds, interest on reserves, bank reserves;
* ``fees``      a fund charging 2 and 20 with a high-water mark, run on the US market's 94 calendar years;
* ``basis``     Binance's coin-margined March-2021 BTC future against spot, hour by hour: basis, implied carry;
* ``hedge``     the minimum-variance hedge of ETH with BTC, fitted 2021-22 and tested in 2023, with a bootstrap;
* ``book``      a zero-intelligence limit order book (Smith-Farmer-Gillemot-Krishnamurthy 2003), seeded, simulated;
* ``auction_live``  the closing auction built order by order, and a market-on-close order's effect;
* ``rfq``       best-of-n dealer quotes against information leakage; markouts of retail and informed flow;
* ``duffie_zhu``  when a CCP for one asset class raises exposure (Duffie-Zhu 2011), Monte Carlo against the formula;
* ``waterfall`` a stressed member default run down a CCP's default waterfall, 10^5 scenarios;
* ``settlement``  the clearing deposit at T+2, T+1, T+0 for one-way and two-way flow, as volatility spikes;
* ``liq_surface``  the chance a leveraged BTC long is liquidated within H days, 2020-25 hourly lows, and the
                   reflection-principle formula;
* ``imodel``    EWMA margin on the US market 1926-2020 and on BTC: breaches, Kupiec, lambda by likelihood, 1987;
* ``squeeze``   a short squeeze against free float: 1,000 shorts with thresholds, seeded;
* ``sofr_fan``  SOFR's percentiles (FRED) through September 2019;
* ``reserve_curve``  the reserve demand curve: weekly SOFR - IOR against reserves 2018-21, fitted by Gauss-Newton;
* ``spiral``    ten funds at a haircut's leverage limit when the haircut rises: the deleveraging spiral;
* ``fire_sale`` banks racing to sell a defaulted client's shares: loss by rank, and the standstill;
* ``glm``       return smoothing: the smallest size decile's autocorrelation, and theta fitted by likelihood;
* ``index_rd``  a Russell-style regression discontinuity at rank 1000, simulated with a known jump;
* ``limits``    daily price limits and the autocorrelation they create, simulated;
* ``industry``  the disclosed numbers of the industry chapter (cited, not computed).
"""

from __future__ import annotations

from datetime import datetime, timezone

import numpy as np

from explainer.ai.cache import Cache
from explainer.quant import data
from explainer.quant.house import funding, pit

CACHE = Cache("quant2")
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


def _utc(ts):
    return datetime.fromtimestamp(float(ts), tz=timezone.utc)


# ---------------------------------------------------------------------------
MAINT = 0.005  # maintenance margin, 0.5% of notional: a typical exchange rule for the smallest BTC tier


def compute_margin() -> dict:
    k = data.binance_klines("BTCUSDT", "1h", "2020-02", "2020-04", market="futures/um")
    f = data.binance_funding("BTCUSDT", "2020-02", "2020-04")
    t0 = datetime(2020, 3, 1, tzinfo=timezone.utc).timestamp()
    t1 = datetime(2020, 3, 20, tzinfo=timezone.utc).timestamp()
    m = (k["time"] >= t0) & (k["time"] <= t1)
    t, p = k["time"][m], k["close"][m]
    # funding settles at 00:00, 08:00 and 16:00 UTC: charge each settlement at the bar that closes after it
    fr = np.zeros(len(t))
    for ft, rate in zip(f["time"], f["rate"]):
        i = np.searchsorted(t, ft)
        if 0 < i < len(t):
            fr[i] += rate
    out = {"t": t, "price": p, "low": k["low"][m], "entry": float(p[0]), "maint": MAINT, "funding": fr}
    runs = {}
    for L in (2, 3, 10):
        acc = funding.margin_account(p, 1.0, float(L), MAINT, funding=fr)
        li = acc["liquidated_at"]
        runs[str(L)] = {"equity": acc["equity"], "req": acc["maintenance_req"], "margin": acc["initial_margin"],
                        "liq_index": -1 if li is None else int(li),
                        "liq_time": None if li is None else float(t[li]),
                        "liq_price_formula": funding.liquidation_price(float(p[0]), float(L), MAINT),
                        "left": acc["left"], "funding_paid": acc["funding_paid"]}
    out["runs"] = _json(runs)
    i_min = int(np.argmin(p))
    out["min_price"], out["min_time"] = float(p[i_min]), float(t[i_min])
    out["fall"] = float(p[i_min] / p[0] - 1)
    d12 = [i for i, x in enumerate(t) if _utc(x).strftime("%Y%m%d") == "20200312"]
    out["day12_open"], out["day12_close"] = float(p[d12[0] - 1]), float(p[d12[-1]])
    return out


# ---------------------------------------------------------------------------
def compute_netting() -> dict:
    rng = np.random.default_rng(21)
    n, trades = 25, 6000
    size = np.exp(rng.normal(0, 1.2, trades)) * 1e6  # dollar values, heavy-tailed
    # a few large members trade more: draw members by a skewed weight
    w = np.exp(rng.normal(0, 0.9, n))
    w /= w.sum()
    a = rng.choice(n, trades, p=w)
    b = rng.choice(n, trades, p=w)
    keep = a != b
    a, b, size = a[keep], b[keep], size[keep]
    res = funding.netting(a, b, size, n)
    M = np.zeros((n, n))
    np.add.at(M, (a, b), size)
    return {"n": n, "trades": int(keep.sum()), "gross": res["gross"], "bilateral": res["bilateral"],
            "multilateral": res["multilateral"], "net_position": res["net_position"],
            "saved": 1 - res["multilateral"] / res["gross"], "matrix": M}


# ---------------------------------------------------------------------------
def compute_auction() -> dict:
    rng = np.random.default_rng(22)
    nb = na = 150
    bp = np.round(100 + rng.normal(-0.15, 0.6, nb), 2)
    ap = np.round(100 + rng.normal(0.15, 0.6, na), 2)
    bq = np.round(np.exp(rng.normal(5, 0.8, nb)))
    aq = np.round(np.exp(rng.normal(5, 0.8, na)))
    au = funding.call_auction(bp, bq, ap, aq)
    return {"bid_px": bp, "bid_qty": bq, "ask_px": ap, "ask_qty": aq, "price": au["price"], "volume": au["volume"],
            "candidates": au["candidates"], "demand": au["demand"], "supply": au["supply"],
            "total_bid": float(bq.sum()), "total_ask": float(aq.sum())}


# ---------------------------------------------------------------------------
def compute_funding() -> dict:
    f = data.binance_funding("BTCUSDT", "2020-01", "2020-12")
    k = data.binance_klines("BTCUSDT", "1d", "2020-01", "2020-12", market="futures/um")
    # the cost of holding one coin long: each settlement pays rate x the price at that time
    px = np.interp(f["time"], k["time"], k["close"])
    paid = f["rate"] * px
    return {"time": f["time"], "rate": f["rate"], "annualized": float(f["rate"].mean() * 3 * 365),
            "cum_paid": np.cumsum(paid), "paid_total": float(paid.sum()), "px_start": float(k["close"][0]),
            "px_end": float(k["close"][-1]), "max_rate": float(f["rate"].max()), "min_rate": float(f["rate"].min()),
            "share_positive": float(np.mean(f["rate"] > 0))}


# ---------------------------------------------------------------------------
def compute_repo() -> dict:
    out = {}
    for s in ("SOFR", "DFF", "IOER"):
        x = data.fred(s, "2018-01-01", "2025-12-31")
        m = (x["date"] >= 20190801) & (x["date"] <= 20191031)
        out[s] = {"date": x["date"][m], "value": x["value"][m]}
    r = data.fred("WRESBAL", "2018-01-01", "2025-12-31")
    m = (r["date"] >= 20180101) & (r["date"] <= 20201231)
    out["reserves"] = {"date": r["date"][m], "value": r["value"][m] / 1e6}  # trillions of dollars
    sofr = dict(zip(out["SOFR"]["date"].tolist(), out["SOFR"]["value"].tolist()))
    ioer = dict(zip(out["IOER"]["date"].tolist(), out["IOER"]["value"].tolist()))
    dff = dict(zip(out["DFF"]["date"].tolist(), out["DFF"]["value"].tolist()))
    out["key"] = {str(d): {"sofr": sofr.get(d), "ioer": ioer.get(d), "dff": dff.get(d)}
                  for d in (20190912, 20190913, 20190916, 20190917, 20190918, 20190919)}
    rr = out["reserves"]
    i19 = int(np.argmin(np.where((rr["date"] >= 20190101) & (rr["date"] <= 20191031), rr["value"], 1e9)))
    out["reserves_low"], out["reserves_low_date"] = float(rr["value"][i19]), int(rr["date"][i19])
    j = int(np.argmax(np.where(rr["date"] <= 20190101, rr["value"], -1)))
    out["reserves_2018"] = float(rr["value"][0])
    return {k: (_json(v) if isinstance(v, dict) else v) for k, v in out.items()}


# ---------------------------------------------------------------------------
def compute_fees() -> dict:
    kf = data.ken_french_daily()
    d, simple = pit.research(kf["date"], kf["mkt"])
    years = d // 10000
    ys = np.arange(1927, 2021)
    gross = np.array([np.prod(1 + simple[years == y]) - 1 for y in ys])
    f = funding.fund_fees(gross, mgmt=0.02, perf=0.20)
    wg = np.cumprod(1 + gross)
    wn = np.cumprod(1 + f["net"])
    f1 = funding.fund_fees(gross, mgmt=0.01, perf=0.0)
    return {"years": ys, "gross": gross, "net": f["net"], "fees": f["fees"], "wealth_gross": wg, "wealth_net": wn,
            "final_gross": float(wg[-1]), "final_net": float(wn[-1]), "final_1pct": float(np.prod(1 + f1["net"])),
            "geo_gross": float(wg[-1] ** (1 / len(ys)) - 1), "geo_net": float(wn[-1] ** (1 / len(ys)) - 1),
            "share_kept": float((wn[-1] - 1) / (wg[-1] - 1))}




# ---------------------------------------------------------------------------
# Part 2, expanded
# ---------------------------------------------------------------------------
EXPIRY_210326 = datetime(2021, 3, 26, 8, tzinfo=timezone.utc).timestamp()  # Binance quarterly: 08:00 UTC delivery


def compute_basis() -> dict:
    fut = data.binance_klines("BTCUSD_210326", "1h", "2020-12", "2021-03", market="futures/cm")
    spot = data.binance_klines("BTCUSDT", "1h", "2020-12", "2021-03")
    t = np.intersect1d(fut["time"], spot["time"])
    t = t[t < EXPIRY_210326]
    F = fut["close"][np.searchsorted(fut["time"], t)]
    S = spot["close"][np.searchsorted(spot["time"], t)]
    days = (EXPIRY_210326 - (t + 3600)) / 86400  # the close of the bar that opens at t
    basis = F / S - 1
    ann = funding.implied_carry(F, S, np.maximum(days, 1e-6) / 365)
    keep = days > 10
    table = {}
    for d in ("2020-12-01", "2021-01-10", "2021-02-10", "2021-02-19", "2021-03-21"):
        ts = datetime.fromisoformat(d).replace(tzinfo=timezone.utc).timestamp()
        i = int(np.searchsorted(t, ts))
        table[d] = {"S": float(S[i]), "F": float(F[i]), "days": float(days[i]), "basis": float(basis[i]),
                    "ann": float(ann[i])}
    step = 4  # every 4 hours for drawing
    return {"t": t[::step], "S": S[::step], "F": F[::step], "days": days[::step], "basis": basis[::step],
            "ann": ann[::step], "table": table, "mean_ann": float(ann[keep].mean()), "max_ann": float(ann[keep].max()),
            "last_basis": float(basis[-1]), "last_days": float(days[-1]), "n_hours": int(len(t))}


def compute_hedge() -> dict:
    btc = data.binance_klines("BTCUSDT", "1d", "2021-01", "2023-12")
    eth = data.binance_klines("ETHUSDT", "1d", "2021-01", "2023-12")
    t = np.intersect1d(btc["time"], eth["time"])
    b = np.diff(np.log(btc["close"][np.searchsorted(btc["time"], t)]))
    e = np.diff(np.log(eth["close"][np.searchsorted(eth["time"], t)]))
    tt = t[1:]
    cut = datetime(2023, 1, 1, tzinfo=timezone.utc).timestamp()
    ins, oos = tt < cut, tt >= cut
    h, eff_in = funding.min_var_hedge(e[ins], b[ins])
    h23, eff23 = funding.min_var_hedge(e[oos], b[oos])
    eff_out = funding.hedge_effectiveness(e[oos], b[oos], h)
    rho = float(np.corrcoef(e[ins], b[ins])[0, 1])
    ratio = float(e[ins].std() / b[ins].std())
    rng = np.random.default_rng(23)
    boots = []
    n = int(ins.sum())
    for _ in range(400):  # a block bootstrap, 20-day blocks
        starts = rng.integers(0, n - 20, n // 20)
        idx = (starts[:, None] + np.arange(20)).ravel()
        boots.append(funding.min_var_hedge(e[ins][idx], b[ins][idx])[0])
    boots = np.array(boots)
    # the hedge ratio fitted on a rolling 90-day window, to draw how it moved
    roll_t, roll_h = [], []
    for i in range(90, len(e), 5):
        roll_t.append(float(tt[i]))
        roll_h.append(funding.min_var_hedge(e[i - 90:i], b[i - 90:i])[0])
    return {"h": h, "eff_in": eff_in, "eff_out": eff_out, "h_2023": h23, "eff_2023_refit": eff23, "rho": rho,
            "vol_ratio": ratio, "h_ci": [float(np.percentile(boots, 2.5)), float(np.percentile(boots, 97.5))],
            "boots": boots, "roll_t": roll_t, "roll_h": roll_h, "eth": e[ins][:400], "btc": b[ins][:400],
            "n_in": n, "n_out": int(oos.sum())}


# ---------------------------------------------------------------------------
class ZIBook:
    """A zero-intelligence limit order book on a tick grid (Smith, Farmer, Gillemot and Krishnamurthy 2003): limit
    orders of one share arrive at rate ``alpha`` per price level within ``window`` ticks of the opposite best quote,
    market orders at rate ``mu`` (each side half), and every resting share is cancelled at rate ``delta``."""

    def __init__(self, alpha=1.0, mu=10.0, delta=0.2, window=20, n=600, seed=0):
        self.a, self.mu, self.d, self.W, self.n = alpha, mu, delta, window, n
        self.rng = np.random.default_rng(seed)
        self.bid = np.zeros(n, int)
        self.ask = np.zeros(n, int)
        mid = n // 2
        for k in range(1, 6):
            self.bid[mid - k] = 3
            self.ask[mid + k] = 3

    def best(self):
        b = np.flatnonzero(self.bid)
        a = np.flatnonzero(self.ask)
        return (b[-1] if len(b) else 0), (a[0] if len(a) else self.n - 1)

    def step(self):
        r = self.rng
        bb, ba = self.best()
        nb, na = self.bid.sum(), self.ask.sum()
        rates = np.array([self.a * self.W, self.a * self.W, self.mu / 2, self.mu / 2, self.d * nb, self.d * na])
        k = r.choice(6, p=rates / rates.sum())
        if k == 0:    # limit buy below the best ask
            p = ba - 1 - r.integers(0, self.W)
            if p > 0:
                self.bid[p] += 1
        elif k == 1:  # limit sell above the best bid
            p = bb + 1 + r.integers(0, self.W)
            if p < self.n - 1:
                self.ask[p] += 1
        elif k == 2:  # market buy: takes a share at the best ask
            if na:
                self.ask[ba] -= 1
        elif k == 3:
            if nb:
                self.bid[bb] -= 1
        elif k == 4 and nb:  # cancel a random resting bid share
            i = r.choice(self.n, p=self.bid / nb)
            self.bid[i] -= 1
        elif k == 5 and na:
            i = r.choice(self.n, p=self.ask / na)
            self.ask[i] -= 1
        return k

    def recentre(self):
        bb, ba = self.best()
        shift = (bb + ba) // 2 - self.n // 2
        if abs(shift) > self.n // 6:
            self.bid = np.roll(self.bid, -shift)
            self.ask = np.roll(self.ask, -shift)
            if shift > 0:
                self.bid[-shift:] = 0
                self.ask[-shift:] = 0
            else:
                self.bid[:-shift] = 0
                self.ask[:-shift] = 0


def _walk_cost(ask, ba, Q):
    """Average price paid above the best ask, in ticks, by a market buy of Q shares walking the asks."""
    got, cost, p = 0, 0.0, ba
    while got < Q and p < len(ask):
        take = min(ask[p], Q - got)
        cost += take * (p - ba)
        got += take
        p += 1
    return cost / max(got, 1)


def compute_book() -> dict:
    out = {"ratios": [0.5, 1.0, 2.0, 4.0], "seeds": 4}
    base = {"alpha": 1.0, "delta": 0.2, "window": 20}
    part = CACHE.partial("book", {"v": 2, **base})
    events, burn = 60000, 10000
    Qs = np.arange(1, 41)
    for ratio in out["ratios"]:
        for seed in range(out["seeds"]):
            key = f"{ratio}_{seed}"
            if key in part:
                continue
            bk = ZIBook(mu=ratio * base["alpha"] * base["window"] / 2, seed=seed, **base)
            spreads, depth, walk = [], np.zeros(12), np.zeros(len(Qs))
            ns = 0
            for i in range(events):
                bk.step()
                if i % 200 == 0:
                    bk.recentre()
                if i > burn and i % 50 == 0:
                    bb, ba = bk.best()
                    spreads.append(int(ba - bb))
                    depth += bk.ask[ba:ba + 12] if ba + 12 <= bk.n else 0
                    walk += np.array([_walk_cost(bk.ask, ba, q) for q in Qs])
                    ns += 1
            part[key] = {"spread": spreads, "depth": (depth / ns).tolist(), "walk": (walk / ns).tolist()}
    sp = {str(r): [float(np.mean(part[f"{r}_{s}"]["spread"])) for s in range(out["seeds"])] for r in out["ratios"]}
    out["mean_spread"] = sp
    b = "1.0"
    out["spread_hist"] = np.bincount(np.concatenate([part[f"{b}_{s}"]["spread"] for s in range(out["seeds"])]),
                                     minlength=12)[:12]
    out["depth"] = np.mean([part[f"{b}_{s}"]["depth"] for s in range(out["seeds"])], axis=0)
    out["walk"] = np.array([part[f"{b}_{s}"]["walk"] for s in range(out["seeds"])])
    out["Q"] = Qs
    d1 = float(out["depth"][0])
    out["walk_uniform"] = 0.5 * (Qs / max(d1, 1e-9) - 1).clip(0)  # the uniform-depth formula, delta = 1 tick
    # a short movie for the ladder: the 8 levels each side, event by event
    bk = ZIBook(mu=base["alpha"] * base["window"] / 2, seed=11, **base)
    for _ in range(burn):
        bk.step()
    bk.recentre()
    frames, kinds = [], []
    mid0 = (bk.best()[0] + bk.best()[1]) // 2
    for _ in range(240):
        kinds.append(int(bk.step()))
        frames.append(np.r_[bk.bid[mid0 - 8:mid0], bk.ask[mid0:mid0 + 8]].tolist())
    out["frames"], out["kinds"] = np.array(frames), np.array(kinds)
    return out


# ---------------------------------------------------------------------------
def compute_auction_live() -> dict:
    a = load("auction")
    bp, bq, ap, aq = (np.asarray(a[k]) for k in ("bid_px", "bid_qty", "ask_px", "ask_qty"))
    rng = np.random.default_rng(24)
    side = np.r_[np.zeros(len(bp), int), np.ones(len(ap), int)]
    idx = np.r_[np.arange(len(bp)), np.arange(len(ap))]
    order = rng.permutation(len(side))
    price, vol, imb = [], [], []
    for k in range(1, len(order) + 1):
        sel = order[:k]
        b = idx[sel][side[sel] == 0]
        s = idx[sel][side[sel] == 1]
        if len(b) == 0 or len(s) == 0 or bp[b].max() < ap[s].min():
            price.append(np.nan), vol.append(0.0), imb.append(0.0)
            continue
        au = funding.call_auction(bp[b], bq[b], ap[s], aq[s])
        i = int(np.searchsorted(au["candidates"], au["price"]))
        i = min(i, len(au["candidates"]) - 1)
        price.append(au["price"]), vol.append(au["volume"]), imb.append(float(au["demand"][i] - au["supply"][i]))
    moc = funding.call_auction(np.r_[bp, 1e6], np.r_[bq, 2000], ap, aq)
    # the same 2,000 shares bought in the continuous market: walk the asks above the auction price
    asks = np.sort(ap)
    q_sorted = aq[np.argsort(ap)]
    m = asks >= a["price"]
    got, cost = 0.0, 0.0
    for p_, q_ in zip(asks[m], q_sorted[m]):
        take = min(q_, 2000 - got)
        cost += take * p_
        got += take
        if got >= 2000:
            break
    return {"order": order, "side": side[order], "price": np.array(price), "volume": np.array(vol),
            "imbalance": np.array(imb), "moc_price": moc["price"], "moc_volume": moc["volume"],
            "moc_demand": moc["demand"], "moc_candidates": moc["candidates"], "base_price": a["price"],
            "walk_avg": float(cost / got), "walk_last": float(p_)}


# ---------------------------------------------------------------------------
def compute_rfq() -> dict:
    rng = np.random.default_rng(25)
    Z = rng.standard_normal((100000, 20))
    emax = np.array([Z[:, :n].max(1).mean() for n in range(1, 21)])
    n = np.arange(1, 21)
    lam_grid = np.linspace(0.02, 0.5, 25)
    nstar = [int(n[np.argmin(-emax + l * (n - 1))]) for l in lam_grid]
    lam0 = 0.15
    cost = -emax + lam0 * (n - 1)
    hist = {str(k): np.histogram(-Z[:, :k].max(1), bins=40, range=(-4, 2))[0] for k in (1, 3, 10)}
    # markouts: a dealer fills buys and sells; a share phi of the flow knows the price 60 s ahead
    T, sig = 400000, 1.0
    P = np.cumsum(rng.normal(0, sig, T))
    hs = np.arange(0, 301, 10)
    mk = {}
    for name, phi in (("retail", 0.02), ("institutional", 0.30)):
        t0 = rng.integers(0, T - 400, 50000)
        informed = rng.random(len(t0)) < phi
        s = np.where(informed, np.sign(P[t0 + 60] - P[t0]), rng.choice([-1, 1], len(t0)))
        mk[name] = np.array([float(np.mean(-s * (P[t0 + h] - P[t0]))) for h in hs])
    return {"n": n, "emax": emax, "sqrt2ln": np.sqrt(2 * np.log(np.maximum(n, 1))), "cost": cost, "lam0": lam0,
            "nstar0": int(n[np.argmin(cost)]), "lam_grid": lam_grid, "nstar": nstar, "hist": _json(hist),
            "hist_edges": np.linspace(-4, 2, 41), "hs": hs, "markout": _json(mk)}


# ---------------------------------------------------------------------------
def compute_duffie_zhu() -> dict:
    rng = np.random.default_rng(26)
    Ns = np.arange(5, 51, 5)
    Ks = np.arange(1, 11)
    gain_mc = np.zeros((len(Ns), len(Ks)))
    for i, N in enumerate(Ns):
        for j, K in enumerate(Ks):
            X = rng.standard_normal((4000, N - 1, K))   # dealer 0's exposure to each counterparty in each class
            bil = np.maximum(X.sum(2), 0).sum(1).mean()  # bilateral netting across all K classes
            if K > 1:
                rest = np.maximum(X[:, :, 1:].sum(2), 0).sum(1).mean()
            else:
                rest = 0.0
            ccp = np.maximum(X[:, :, 0].sum(1), 0).mean()  # class 0 cleared: net against all counterparties
            gain_mc[i, j] = (bil - rest - ccp) / bil       # > 0: the CCP lowers expected exposure
    phi0 = 1 / np.sqrt(2 * np.pi)
    NN, KK = np.meshgrid(Ns, Ks, indexing="ij")
    bil_f = (NN - 1) * np.sqrt(KK) * phi0
    gain_f = (bil_f - (NN - 1) * np.sqrt(KK - 1) * phi0 - np.sqrt(NN - 1) * phi0) / bil_f
    Nmin = [float(1 + 1 / (np.sqrt(k) - np.sqrt(k - 1)) ** 2) for k in Ks]
    return {"N": Ns, "K": Ks, "gain_mc": gain_mc, "gain_formula": gain_f, "N_min": Nmin}


def compute_waterfall() -> dict:
    rng = np.random.default_rng(27)
    n, S = 25, 100000
    size = np.exp(rng.normal(0, 0.8, n))
    size = size / size.sum() * 100.0                # positions, $ billion of exposure
    sign = np.where(rng.random(n) < 0.6, 1.0, -1.0)
    beta = 0.9 + 0.2 * rng.random(n)
    vol2 = 0.01 * np.sqrt(2)                        # 2-day close-out, 1% daily
    im = 2.326 * vol2 * size                        # 99% 2-day Gaussian VaR margin
    # stress: market moves from a Student t(3) scaled to the 2-day vol, plus member-specific noise
    M = rng.standard_t(3, S) * vol2 / np.sqrt(3.0)
    eps = rng.standard_normal((S, n)) * vol2 * 0.5
    loss = -(sign * size)[None, :] * (beta[None, :] * M[:, None] + eps)
    excess = loss - im[None, :]
    # cover 2: the fund covers the two largest losses beyond margin in an extreme but plausible scenario (5x vol)
    stress = np.abs(size) * 5 * vol2 * 1.0 - im
    df_total = float(np.sort(stress)[-2:].sum())
    df_share = df_total * size / size.sum()
    skin = 0.25 * df_total * 0.1
    d = np.argmax(excess, axis=1)                   # the member hit hardest defaults
    uncovered_after_im = np.maximum(excess[np.arange(S), d], 0)
    own_df = df_share[d]
    layers = np.column_stack([own_df, np.full(S, skin), df_total - own_df, np.full(S, df_total)])
    left = uncovered_after_im.copy()
    taken = []
    for k in range(4):
        tk = np.minimum(left, layers[:, k])
        taken.append(tk)
        left = left - tk
    taken = np.column_stack(taken + [left])
    reach = [float(np.mean(excess[np.arange(S), d] > 0))] + [float(np.mean(taken[:, k] > 0)) for k in range(5)]
    # five named stress days: market moves of 2 to 10 daily standard deviations against the biggest long
    big = int(np.argmax(size * (sign > 0)))
    named = []
    for k in (2, 4, 6, 8, 12):
        L_ = size[big] * beta[big] * k * 0.01
        named.append(funding.ccp_waterfall(L_, [im[big], df_share[big], skin, df_total - df_share[big], df_total])[0])
    return {"im_total": float(im.sum()), "df_total": df_total, "skin": skin, "reach": reach,
            "layers_named": np.array(named), "named_sigmas": [2, 4, 6, 8, 12], "big_im": float(im[big]),
            "big_df": float(df_share[big]), "big_size": float(size[big]), "n": n, "S": S}


# ---------------------------------------------------------------------------
def compute_settlement() -> dict:
    days = 120
    sig = np.full(days, 0.60 / np.sqrt(252))
    sig[60:75] = 4.0 / np.sqrt(252)                 # a spike, stated: 60% -> 400% annualized
    runs = {}
    for flow in ("one_way", "two_way"):
        for h in (2, 1, 0):
            rr = []
            for seed in range(8):
                rng = np.random.default_rng(100 + seed)
                f = rng.normal(1.0 if flow == "one_way" else 0.0, 0.5 if flow == "one_way" else 1.0, days)
                E = np.array([abs(f[max(t - h + 1, 0):t + 1].sum()) if h > 0 else 0.0 for t in range(days)])
                rr.append(2.326 * sig * np.sqrt(2) * E)
            runs[f"{flow}_{h}"] = np.array(rr)
    cut = {f: float(1 - runs[f"{f}_1"].mean() / runs[f"{f}_2"].mean()) for f in ("one_way", "two_way")}
    return {"days": np.arange(days), "sig": sig, "runs": _json(runs), "cut": cut,
            "spike": float(runs["one_way_2"][:, 60:75].mean() / runs["one_way_2"][:, :60].mean())}


# ---------------------------------------------------------------------------
def compute_liq_surface() -> dict:
    k = data.binance_klines("BTCUSDT", "1h", "2020-01", "2025-12")
    day = (k["time"] // 86400).astype(int)
    u, start = np.unique(day, return_index=True)
    opens = k["open"][start]
    lows = np.minimum.reduceat(k["low"], start)
    closes = k["close"][np.r_[start[1:] - 1, len(day) - 1]]
    Ls = np.unique(np.round(np.geomspace(1.5, 50, 30), 2))
    Hs = np.arange(1, 91)
    n = len(opens) - Hs[-1]
    runmin = lows[:n].copy()
    dd = np.zeros((len(Hs), n))
    for j, H in enumerate(Hs):
        if H > 1:
            runmin = np.minimum(runmin, lows[H - 1:H - 1 + n])
        dd[j] = np.log(runmin / opens[:n])
    d = -np.log((1 - 1 / Ls) / (1 - MAINT))
    P = np.array([[float(np.mean(dd[j] <= -d[i])) for j in range(len(Hs))] for i in range(len(Ls))])
    sig = float(np.std(np.diff(np.log(closes))))
    Pf = funding.liquidation_probability(Ls[:, None], Hs[None, :], sig, MAINT)
    i10 = int(np.argmin(np.abs(Ls - 10)))
    return {"L": Ls, "H": Hs, "P": P, "P_formula": Pf, "sigma_daily": sig, "d": d, "n_entries": n,
            "slice_L10": P[i10], "slice_L10_formula": Pf[i10], "L10": float(Ls[i10]),
            "p_L10_H19": float(P[i10, 18]), "pf_L10_H19": float(Pf[i10, 18]),
            "p_L5_H30": float(P[int(np.argmin(np.abs(Ls - 5)))][29]),
            "p_L10_H30": float(P[i10, 29]), "d5": float(-np.log((1 - 1 / 5) / (1 - MAINT))),
            "d10": float(-np.log((1 - 1 / 10) / (1 - MAINT)))}


# ---------------------------------------------------------------------------
def compute_imodel() -> dict:
    kf = data.ken_french_daily()
    d, simple = pit.research(kf["date"], kf["mkt"])
    r = np.log1p(simple)
    lam, z = 0.97, 2.326
    v = funding.ewma_var(r, lam)
    m1 = z * np.sqrt(v)                       # 1-day 99% margin
    m2 = funding.ewma_margin(r, lam, z, 2.0)   # 2-day
    br = r[20:] < -m1[20:]
    T = int(len(br))
    kup = funding.kupiec(int(br.sum()), T, 0.01)
    sd = r.std()
    br_c = r[20:] < -z * sd
    kup_c = funding.kupiec(int(br_c.sum()), T, 0.01)
    yrs = d // 10000

    def at(dd):
        return float(m2[int(np.searchsorted(d, dd))])
    key = {k: at(k) for k in (19870901, 19871016, 19871019, 19871020, 19871030)}
    ratios = {}
    for y in (1987, 2008, 2020):
        mm = m2[yrs == y]
        dd_ = d[yrs == y]
        i_lo, i_hi = int(np.argmin(mm[:int(np.argmax(mm)) + 1])), int(np.argmax(mm))
        ratios[str(y)] = {"lo": float(mm[i_lo]), "hi": float(mm[i_hi]), "lo_date": int(dd_[i_lo]),
                          "hi_date": int(dd_[i_hi]), "ratio": float(mm[i_hi] / mm[i_lo])}
    m87 = (d >= 19870701) & (d <= 19871231)
    fit = funding.fit_ewma_lambda(r)
    grid = np.linspace(0.90, 0.995, 40)
    ll = np.array([funding.ewma_loglik(r, g) for g in grid])
    eras = []
    for a_, b_ in ((1926, 1945), (1945, 1964), (1964, 1983), (1983, 2002), (2002, 2021)):
        mm = (yrs >= a_) & (yrs < b_)
        e = np.array([funding.ewma_loglik(r[mm], g) for g in grid])
        eras.append((e - e.max()) / mm.sum() * 1000)
    btc = data.binance_klines("BTCUSDT", "1d", "2018-01", "2025-12")
    rb = np.diff(np.log(btc["close"]))
    fb = funding.fit_ewma_lambda(rb)
    vb = funding.ewma_var(rb, 0.97)
    brb = rb[20:] < -z * np.sqrt(vb[20:])
    return {"date87": d[m87], "r87": r[m87], "m87": m2[m87], "key": {str(k): v_ for k, v_ in key.items()},
            "breach_rate": float(br.mean()), "breaches": int(br.sum()), "T": T, "kupiec": kup,
            "breach_rate_const": float(br_c.mean()), "kupiec_const": kup_c, "ratios": _json(ratios),
            "lam_hat": fit["lam"], "lam_path": fit["path"], "lam_ll": fit["loglik"], "grid": grid, "ll": ll,
            "eras": np.array(eras), "btc_lam": fb["lam"], "btc_breach": float(brb.mean()),
            "r_2020": r[yrs == 2020], "m_2020": m2[yrs == 2020], "d_2020": d[yrs == 2020]}


# ---------------------------------------------------------------------------
def _squeeze_run(f, s, rng, kappa=0.5, b0=0.02, n=1000, rounds=60):
    """Free float f, short interest s (both as shares of the company). Covering buys B drain the float:
    P/P0 = (1 - B/f)^-kappa, capped at 50x. Each short covers once the price passes its threshold."""
    theta = np.exp(rng.normal(np.log(1.5), 0.35, n))
    per = s / n
    B = b0 * f
    path, covered = [], []
    for _ in range(rounds):
        P = min((1 - min(B / f, 0.999999)) ** -kappa, 50.0) if B < f else 50.0
        c = int(np.sum(theta <= P))
        path.append(P)
        covered.append(c)
        Bn = b0 * f + c * per
        if abs(Bn - B) < 1e-12:
            break
        B = Bn
    return np.array(path), np.array(covered)


def compute_squeeze() -> dict:
    floats = [0.06, 0.2, 0.5]
    rel = np.linspace(0.2, 1.4, 25)
    peak = {}
    for f in floats:
        runs = []
        for seed in range(8):
            rng = np.random.default_rng(300 + seed)
            runs.append([float(_squeeze_run(f, x * f, rng)[0][-1]) for x in rel])
        peak[str(f)] = np.array(runs)
    rng = np.random.default_rng(42)
    p_lo, c_lo = _squeeze_run(0.2, 0.5 * 0.2, rng)
    rng = np.random.default_rng(42)
    p_hi, c_hi = _squeeze_run(0.2, 1.2 * 0.2, rng)
    vw_free = 1 - 0.426 - 0.315 - 0.20
    return {"rel": rel, "peak": _json(peak), "floats": floats, "movie_lo": p_lo, "cov_lo": c_lo, "movie_hi": p_hi,
            "cov_hi": c_hi, "vw_free": vw_free,
            "short_pnl_gc": funding.short_pnl(100, 90, 0.05, 0.0025, 1.0),
            "short_pnl_special": funding.short_pnl(100, 90, 0.05, 0.20, 1.0)}


# ---------------------------------------------------------------------------
def compute_sofr_fan() -> dict:
    out = {}
    for s in ("SOFR1", "SOFR25", "SOFR", "SOFR75", "SOFR99", "IOER"):
        x = data.fred(s, "2018-01-01", "2025-12-31")
        m = (x["date"] >= 20190826) & (x["date"] <= 20191004)
        out[s] = {"date": x["date"][m], "value": x["value"][m]}
    key = {}
    for d in (20190913, 20190916, 20190917, 20190918, 20190919):
        key[str(d)] = {s: float(out[s]["value"][list(out[s]["date"]).index(d)]) for s in out
                       if d in list(out[s]["date"])}
    return {"series": _json(out), "key": key}


def _weekly(dates, values, wk_dates):
    """Mean of daily ``values`` in the 7 days ending on each date of ``wk_dates`` (YYYYMMDD ints)."""
    from datetime import date as _d
    o = np.array([_d(x // 10000, (x // 100) % 100, x % 100).toordinal() for x in dates])
    out = []
    for w in wk_dates:
        e = _d(w // 10000, (w // 100) % 100, w % 100).toordinal()
        m = (o > e - 7) & (o <= e)
        out.append(values[m].mean() if m.any() else np.nan)
    return np.array(out)


def compute_reserve_curve() -> dict:
    sofr = data.fred("SOFR", "2018-01-01", "2025-12-31")
    ioer = data.fred("IOER", "2018-01-01", "2025-12-31")
    iorb = data.fred("IORB", "2018-01-01", "2025-12-31")
    res = data.fred("WRESBAL", "2018-01-01", "2025-12-31")
    ior_d = np.r_[ioer["date"], iorb["date"]]
    ior_v = np.r_[ioer["value"], iorb["value"]]
    m = (res["date"] >= 20180411) & (res["date"] <= 20211229)
    wk = res["date"][m]
    R = res["value"][m] / 1e6
    s = (_weekly(sofr["date"], sofr["value"], wk) - _weekly(ior_d, ior_v, wk)) * 100  # basis points
    ok = np.isfinite(s)
    wk, R, s = wk[ok], R[ok], s[ok]

    def gn(Rx, sx, record=False):
        th = np.array([-5.0, 60.0, 1.0])   # a + b exp(-c (R - 1.3))
        path, loss = [th.copy()], []
        for _ in range(40):
            e = np.exp(-th[2] * (Rx - 1.3))
            f = th[0] + th[1] * e
            r_ = sx - f
            loss.append(float(np.mean(r_ ** 2)))
            J = np.column_stack([np.ones_like(Rx), e, -th[1] * (Rx - 1.3) * e])
            step = np.linalg.lstsq(J.T @ J + 1e-3 * np.eye(3), J.T @ r_, rcond=None)[0]
            th = th + step
            path.append(th.copy())
        loss.append(float(np.mean((sx - th[0] - th[1] * np.exp(-th[2] * (Rx - 1.3))) ** 2)))
        return th, np.array(path), np.array(loss)
    th, path, loss = gn(R, s)
    grid = np.linspace(1.3, 4.3, 80)
    rng = np.random.default_rng(28)
    boot_curves, boot_losses = [], []
    for _ in range(8):
        i = rng.integers(0, len(R), len(R))
        tb, _, lb = gn(R[i], s[i])
        boot_curves.append(tb[0] + tb[1] * np.exp(-tb[2] * (grid - 1.3)))
        boot_losses.append(lb)
    lin = np.polyfit(R, s, 1)
    bins = [(1.3, 1.5), (1.5, 1.7), (1.7, 2.0), (2.5, 3.5), (3.5, 5.0)]
    table = []
    for a_, b_ in bins:
        mm = (R >= a_) & (R < b_)
        table.append({"lo": a_, "hi": b_, "mean": float(s[mm].mean()) if mm.any() else None,
                      "max": float(s[mm].max()) if mm.any() else None, "n": int(mm.sum())})
    i17 = int(np.argmax(s))
    return {"week": wk, "R": R, "s": s, "theta": th, "path": path, "loss": loss, "grid": grid,
            "fit": th[0] + th[1] * np.exp(-th[2] * (grid - 1.3)), "boot": np.array(boot_curves),
            "boot_loss": np.array(boot_losses), "linear": lin, "table": table,
            "mse_fit": float(loss[-1]), "mse_lin": float(np.mean((s - np.polyval(lin, R)) ** 2)),
            "peak_week": int(wk[i17]), "peak_s": float(s[i17]), "peak_R": float(R[i17])}


# ---------------------------------------------------------------------------
def compute_spiral() -> dict:
    out = {}
    h0 = 0.02
    for hn in (0.03, 0.04, 0.06):
        amps, drops = [], []
        for seed in range(8):
            rng = np.random.default_rng(400 + seed)
            E = rng.uniform(0.02, 0.03, 10) * 100       # ten funds, $100 of assets each, near the 2% limit
            q = np.full(10, 100.0)
            D = q - E
            p, first, total = 1.0, None, 0.0
            impact = 0.00004                             # price falls 0.004% per unit sold (stated)
            h = hn
            for _ in range(100):
                eq = q * p - D
                alive = eq > 0
                need = np.where(alive, np.maximum(q - eq / (h * p), 0), q)   # a fund under water sells all
                s = need.sum()
                if s < 1e-9:
                    break
                if first is None:
                    first = s
                total += s
                p_new = p * (1 - impact * s)
                D = D - need * p_new
                q = q - need
                h = hn * (1 + 5 * (1 - p_new))             # haircuts rise with the fall (stated)
                p = p_new
            amps.append(total / first)
            drops.append(1 - p)
        out[str(hn)] = {"amp": amps, "drop": drops}
    tower = funding.deleverage(2.0, 100.0, 0.04, 0.0002)
    return {"runs": _json(out), "tower": _json(tower), "h0": h0, "levels": [(1 - h0) ** k for k in range(12)]}


def compute_fire_sale() -> dict:
    Ks = list(range(2, 9))
    by_rank = {}
    for K in Ks:
        runs = []
        for seed in range(8):
            rng = np.random.default_rng(500 + seed)
            q = rng.uniform(0.5, 1.5, K)                  # each bank's block, random sizes
            res = np.zeros(K)
            for _ in range(200):
                order = rng.permutation(K)
                X = np.r_[0, np.cumsum(q[order])]
                loss = (X[1:] ** 1.5 - X[:-1] ** 1.5) * 2 / 3 / q[order]   # sqrt impact, loss per share
                res += loss
            runs.append(res / 200)
        # loss per share by selling rank, averaged over who sold in that rank
        by_rank[str(K)] = np.array([np.sort(r) for r in runs])
    lin = funding.fire_sale(4, 1.0, 1.0)
    payoff = {"SS": 1.0, "SH": 0.5, "HS": 1.5, "HH": 0.75}   # losses in units of lam q^2 (linear impact)
    return {"K": Ks, "by_rank": _json(by_rank), "linear4": lin, "payoff": payoff,
            "last_over_first_linear": float(lin[-1] / lin[0])}


# ---------------------------------------------------------------------------
def compute_glm() -> dict:
    sz = data.ken_french_size_daily()
    d, D = sz["date"], sz["deciles"]
    out = {}
    for name, a_, b_ in (("early", 19630101, 19891231), ("late", 19900101, 20201231)):
        m = (d >= a_) & (d <= b_)
        x = D[m]
        out[name] = {"small": float(np.corrcoef(x[:-1, 0], x[1:, 0])[0, 1]),
                     "big": float(np.corrcoef(x[:-1, 9], x[1:, 9])[0, 1])}
    th = np.array([0.5, 0.3, 0.2])
    inflate = float(1 / np.sqrt(np.sum(th ** 2)))
    fits, paths, moms = [], [], []
    for seed in range(5):
        rng = np.random.default_rng(600 + seed)
        R = rng.normal(0.008, 0.04, 602)
        Ro = funding.glm_smooth(R, th)
        f = funding.glm_fit(Ro, record=True)
        fits.append(f["theta"]), paths.append(f["path"]), moms.append(f["theta_moment"])
    L = max(len(p) for p in paths)
    paths = np.array([np.vstack([p, np.repeat(p[-1:], L - len(p), 0)]) for p in paths])
    rng = np.random.default_rng(650)
    R = rng.normal(0.008, 0.04, 242)
    Ro = funding.glm_smooth(R, th)
    # the smallest decile, monthly (compounded), 1963-89: fit its smoothing profile
    m = (d >= 19630101) & (d <= 19891231)
    mon = d[m] // 100
    u, st = np.unique(mon, return_index=True)
    mr = np.exp(np.add.reduceat(np.log1p(D[m, 0]), st)) - 1
    fs = funding.glm_fit(mr)
    return {"ac1": out, "theta_true": th, "inflate": inflate, "fits": np.array(fits), "paths": paths,
            "moments": np.array(moms), "R": R, "Ro": Ro, "small_theta": fs["theta"],
            "small_inflate": float(1 / np.sqrt(fs["smoothing_index"]))}


# ---------------------------------------------------------------------------
def compute_index_rd() -> dict:
    jump = 0.015
    bws = [50, 100, 200, 300, 500]
    est = np.zeros((8, len(bws)))
    for seed in range(8):
        rng = np.random.default_rng(700 + seed)
        ranks = np.tile(np.arange(1, 3001), 30)
        vol = 0.04 + 0.06 * (ranks / 3000)
        trend = -0.002 * (ranks - 1000) / 1000         # a smooth relation, the same on both sides
        y = trend + jump * (ranks > 1000) + vol * rng.standard_normal(len(ranks))
        for j, b in enumerate(bws):
            lo = (ranks > 1000 - b) & (ranks <= 1000)
            hi = (ranks > 1000) & (ranks <= 1000 + b)
            fl = np.polyfit(ranks[lo] - 1000, y[lo], 1)
            fh = np.polyfit(ranks[hi] - 1000, y[hi], 1)
            est[seed, j] = fh[1] - fl[1]
        if seed == 0:
            near = (ranks > 500) & (ranks <= 1500)
            edges = np.arange(500, 1501, 20)
            idx = np.digitize(ranks[near], edges) - 1
            binned = np.array([y[near][idx == k].mean() for k in range(len(edges) - 1)])
            centers = (edges[:-1] + edges[1:]) / 2
    # cap-weighted demand: the same passive money spread over two indices of very different size (illustrative)
    caps = 1 / np.arange(1, 3001) ** 1.1
    caps = caps / caps.sum()
    c1, c2 = caps[:1000].sum(), caps[1000:].sum()
    return {"jump": jump, "bw": bws, "est": est, "centers": centers, "binned": binned, "cap_r1000": float(c1),
            "cap_r2000": float(c2), "w_tail_r1000": float(caps[999] / c1), "w_head_r2000": float(caps[1000] / c2)}


def compute_limits() -> dict:
    res = {}
    rng0 = np.random.default_rng(800)
    for L in (0.10, 0.20):
        acs, at_lim, acs_true = [], [], []
        for seed in range(8):
            rng = np.random.default_rng(810 + seed)
            n = 5000
            r = rng.normal(0, 0.03, n) + (rng.random(n) < 0.05) * rng.normal(0, 0.12, n)
            ro = np.zeros(n)
            c = 0.0
            for t in range(n):
                want = r[t] + c
                ro[t] = np.clip(want, -L, L)
                c = want - ro[t]
            acs.append(float(np.corrcoef(ro[:-1], ro[1:])[0, 1]))
            acs_true.append(float(np.corrcoef(r[:-1], r[1:])[0, 1]))
            at_lim.append(float(np.mean(np.abs(ro) >= L - 1e-12)))
        res[f"{L:.2f}"] = {"ac1": acs, "ac1_true": acs_true, "at_limit": at_lim}
    n = 40
    r = rng0.normal(0, 0.03, n)
    r[8], r[25] = 0.27, -0.24
    ro = np.zeros(n)
    c = 0.0
    for t in range(n):
        want = r[t] + c
        ro[t] = np.clip(want, -0.10, 0.10)
        c = want - ro[t]
    return {"res": res, "true_path": np.cumsum(r), "obs_path": np.cumsum(ro), "r": r, "ro": ro}


def compute_industry() -> dict:
    """Disclosed numbers, cited in the scene; stored so the chapter draws them from one place."""
    return {"cme_rev_2024_bn": 6.1, "cme_adv_2024_m": 26.9, "virtu_rev_2024_m": 2876.9, "virtu_mm_2024_m": 2374.1,
            "virtu_ni_2024_m": 534.5, "hood_q4_tx_m": 672, "hood_q4_crypto_m": 358, "hood_q4_options_m": 222,
            "hood_q4_equities_m": 61, "citadel_retail_share": 0.35, "basis_trade_bn": 830, "hf_repo_tn": 3.0,
            "sebi_jane_cr": 4843.57, "nscc_netting": 0.98, "t1_cf_cut_bn": 2.4, "t1_cf_from": 12.2, "t1_cf_to": 9.8}


def compute_backtest_theory() -> dict:
    """The research chapter: likelihood-ratio backtests of a margin model.  Wilks's chi-squared limit for Kupiec's
    LR against the exact law at 250 and 1,000 days; Christoffersen's independence and conditional-coverage tests;
    their power against a margin that gets the count right but the timing wrong (a constant margin under GARCH);
    and both margins on the US market, 1926-2020."""
    from scipy import stats as st
    rng = np.random.default_rng(202)
    p, M = 0.01, 20000
    out = {"p": p, "M": M, "size": {}}
    for T in (250, 1000):
        x = rng.binomial(T, p, M)
        lr = np.array([funding.kupiec(int(k), T, p)["LR"] for k in x])
        exact = {k: funding.kupiec(k, T, p)["LR"] for k in range(0, 40)}
        pk = st.binom.pmf(np.arange(40), T, p)
        rej = [k for k in range(40) if exact[k] > 3.841]
        out["size"][str(T)] = {"sim": float(np.mean(lr > 3.841)), "exact": float(pk[rej].sum()),
                               "support": int(len(set(np.round(lr, 6)))), "lr_hist": np.histogram(lr, 30, (0, 12))[0],
                               "pmf": st.binom.pmf(np.arange(16), T, p)}
    out["traffic"] = {"green_max": 4, "red_min": 10, "p_yellow_or_worse": float(st.binom.sf(4, 250, p)),
                      "p_red": float(st.binom.sf(9, 250, p))}
    # power: GARCH(1,1) daily returns; an EWMA margin and a constant margin with the right long-run variance
    w, a, b = 1e-6, 0.09, 0.90
    lv = w / (1 - a - b)
    z = st.norm.ppf(1 - p)
    T, Mp = 1000, 2000
    pw = {k: {"uc": 0, "ind": 0, "cc": 0, "hits": 0.0, "p11": 0.0} for k in ("ewma", "constant")}
    for m in range(Mp):
        r_ = np.random.default_rng(5000 + m)
        N = T + 500
        e = r_.standard_normal(N)
        h = lv
        x = np.empty(N)
        for t_ in range(N):
            x[t_] = np.sqrt(h) * e[t_]
            h = w + a * x[t_] ** 2 + b * h
        x = x[500:]
        v = funding.ewma_var(x, 0.97, v0=lv)
        hits = {"ewma": (x < -z * np.sqrt(v)).astype(int), "constant": (x < -z * np.sqrt(lv)).astype(int)}
        for k, hh in hits.items():
            c = funding.christoffersen(hh, p)
            pw[k]["uc"] += c["LR_uc"] > 3.841
            pw[k]["ind"] += c["p_ind"] < 0.05
            pw[k]["cc"] += c["p_cc"] < 0.05
            pw[k]["hits"] += c["hits"] / T
            pw[k]["p11"] += c["p11"]
    out["power"] = {k: {kk: float(vv / Mp) for kk, vv in d.items()} for k, d in pw.items()}
    out["garch"] = [w, a, b]
    # the US market, 1926-2020: EWMA(0.97) against a constant margin from the full-sample standard deviation
    kf = data.ken_french_daily()
    d, simple = pit.research(kf["date"], kf["mkt"])
    r = np.log1p(simple)
    v = funding.ewma_var(r, 0.97)
    real = {}
    for k, thr in (("ewma", z * np.sqrt(v)), ("constant", z * r.std() * np.ones(len(r)))):
        hh = (r[20:] < -thr[20:]).astype(int)
        real[k] = funding.christoffersen(hh, p)
        yrs = (d[20:] // 10000)
        real[k]["by_decade"] = {str(dec): int(hh[(yrs >= dec) & (yrs < dec + 10)].sum()) for dec in range(1920, 2030, 10)}
    out["us"] = real
    out["us_T"] = int(len(r) - 20)
    return _json(out)


ITEMS = {"margin": compute_margin, "netting": compute_netting, "auction": compute_auction, "funding": compute_funding,
         "repo": compute_repo, "fees": compute_fees, "basis": compute_basis, "hedge": compute_hedge,
         "book": compute_book, "auction_live": compute_auction_live, "rfq": compute_rfq,
         "duffie_zhu": compute_duffie_zhu, "waterfall": compute_waterfall, "settlement": compute_settlement,
         "liq_surface": compute_liq_surface, "imodel": compute_imodel, "squeeze": compute_squeeze,
         "sofr_fan": compute_sofr_fan, "reserve_curve": compute_reserve_curve, "spiral": compute_spiral,
         "fire_sale": compute_fire_sale, "glm": compute_glm, "index_rd": compute_index_rd, "limits": compute_limits,
         "industry": compute_industry, "backtest_theory": compute_backtest_theory}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
