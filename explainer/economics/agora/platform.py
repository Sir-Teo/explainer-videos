"""Agora's platform (Part 61): the Island's ride-hailing and selling marketplaces, with the experiments a platform's
economists run on them.

* **Surge pricing** (:func:`surge_night`): an evening with a demand spike at midnight; riders' demand falls with the
  surge multiplier, drivers come out as it rises; with surge on the market clears, with it off requests are rationed.
* **Consumer surplus from surge** (:func:`surge_surplus`): sessions that saw random surge multipliers trace the demand
  curve; its area over spending (after Cohen, Hahn, Hall, Levitt and Metcalfe).
* **The commission** (:func:`commission`): a two-sided market in which drivers respond to their pay and riders to the
  fare and the wait; the platform's take, riders' surplus and drivers' earnings by commission.
* **Ranking** (:func:`ranking`): a position-based click model; what each slot is worth; a sponsored slot given to a
  less relevant listing.
* **Reputation** (:func:`reputation`): sellers of varying quality, buyers who rate when happy and mostly stay silent
  when not; percent positive against Nosko and Tadelis's effective percent positive.
* **Measuring advertising** (:func:`ad_power`): Lewis and Rao's arithmetic: the sample needed to detect an advertising
  return.
* **Experiments at scale** (:func:`peeking`, :func:`cuped`): A/A tests read every day; variance reduction with a
  pre-period covariate.
* **Marketplace experiments** (:func:`switchback`): a rider discount tested by user, by time period and by market.
* **Uplift** (:func:`uplift`): targeting a promotion by estimated treatment effects.
* **Flexible work** (:func:`flexibility`): drivers with hour-to-hour reservation wages, flexible against fixed shifts.

numpy and scipy only.
"""

from __future__ import annotations

import numpy as np
from scipy import optimize, stats

# ---------------------------------------------------------------------------------------------------------------
# surge


NIGHT = {"minutes": 120, "base_demand": 60.0, "spike": 280.0, "spike_at": 60, "decay": 40.0, "drivers0": 70.0,
         "supply_slope": 45.0, "lag": 6, "beta": 0.9, "m_max": 4.0}


def surge_night(surge: bool = True, params: dict | None = None) -> dict:
    """Minute by minute from 11pm: ride requests a minute (before any surge) rise from a base to a spike at midnight
    and decay; drivers available respond to the multiplier with a lag of a few minutes.  With surge, the multiplier
    m solves requests x exp(-beta (m - 1)) = drivers(m); without, m = 1 and requests beyond the drivers available go
    unfilled.  Returns the multiplier, requests, completed trips, the completion rate and a wait index (requests per
    available driver)."""
    P = {**NIGHT, **(params or {})}
    T = P["minutes"]
    t = np.arange(T)
    dem = P["base_demand"] + P["spike"] * np.exp(-np.maximum(t - P["spike_at"], 0) / P["decay"]) * (t >= P["spike_at"])
    m = np.ones(T)
    drivers = np.zeros(T)
    done = np.zeros(T)
    req = np.zeros(T)
    for k in range(T):
        lagged = m[k - P["lag"]] if k >= P["lag"] else 1.0
        sup = P["drivers0"] + P["supply_slope"] * (lagged - 1.0)
        if surge:
            f = (lambda mm: dem[k] * np.exp(-P["beta"] * (mm - 1.0)) - sup)
            m[k] = 1.0 if f(1.0) <= 0 else min(optimize.brentq(f, 1.0, 20.0), P["m_max"])
        req[k] = dem[k] * np.exp(-P["beta"] * (m[k] - 1.0))
        drivers[k] = sup
        done[k] = min(req[k], sup)
    rate = done / req
    return {"t": t.tolist(), "m": m.tolist(), "requests": req.tolist(), "demand": dem.tolist(),
            "drivers": drivers.tolist(), "done": done.tolist(), "rate": rate.tolist(),
            "wait": (req / drivers).tolist(), "surge": surge,
            "rate_peak": float(rate[P["spike_at"]:P["spike_at"] + 26].mean())}


def surge_surplus(n_sessions: int = 200000, mu: float = 25.0, base_fare: float = 15.0, seed: int = 61) -> dict:
    """Riders open the app and see a fare of base_fare x m, with m drawn from the surge levels the system happened to
    set; a rider's value is exponential with mean ``mu`` above a floor of zero, so P(buy | fare) = exp(-fare/mu).
    Estimating that curve from the sessions (a regression of log purchase rates by surge level) gives consumer
    surplus per trip, mu, against spending, the fare; surplus per dollar spent is mu / fare."""
    rng = np.random.default_rng(seed)
    levels = np.array([1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 2.5])
    m = rng.choice(levels, n_sessions, p=[0.55, 0.12, 0.1, 0.08, 0.06, 0.05, 0.04])
    fare = base_fare * m
    buy = rng.random(n_sessions) < np.exp(-fare / mu)
    rates = np.array([buy[m == L].mean() for L in levels])
    X = np.column_stack([np.ones(len(levels)), base_fare * levels])
    b, *_ = np.linalg.lstsq(X, np.log(rates), rcond=None)
    mu_hat = -1 / b[1]
    spend = float(np.sum(fare[buy]))
    cs = float(buy.sum() * mu_hat)
    return {"levels": levels.tolist(), "rates": rates.tolist(), "mu_hat": float(mu_hat), "mu": mu,
            "cs_per_dollar": cs / spend, "trips": int(buy.sum()), "elasticity_at_base": float(-base_fare / mu_hat)}


# ---------------------------------------------------------------------------------------------------------------
# the commission


def _logistic(x):
    return 1.0 / (1.0 + np.exp(-np.clip(x, -50.0, 50.0)))


COMMISSION = {"fare": 20.0, "a_r": 3.5, "b_r": 0.08, "w_r": 0.8, "riders": 1000.0, "drivers": 2000.0, "w0": 20.0,
              "s_d": 2.0, "cap": 2.0, "w_min": 2.0, "w_k": 3.0}


def commission_market(c: float, params: dict | None = None) -> dict:
    """One commission's equilibrium.  Riders (``riders`` an hour who might ride) ride with logit probability in
    a_r - b_r fare - w_r wait; the wait, in minutes, rises with drivers' utilization u = trips / (drivers x cap) as
    w_min + w_k u / (1 - u).  Drivers (``drivers`` who might drive) drive with logit probability in
    (hourly earnings - w0) / s_d, where earnings are (1 - c) x fare x trips per driver.  For a given number of
    drivers the riders' fixed point has one solution; drivers' earnings fall as more drive, so the equilibrium is
    unique too.  Returns trips, drivers, the wait, earnings, the platform's take and both sides' surplus (logit
    inclusive values in dollars)."""
    P = {**COMMISSION, **(params or {})}

    def wait(t, D):
        u = t / (D * P["cap"])
        return P["w_min"] + P["w_k"] * u / (1 - u)

    def trips(D):
        f = (lambda t: t - P["riders"] * _logistic(P["a_r"] - P["b_r"] * P["fare"] - P["w_r"] * wait(t, D)))
        return optimize.brentq(f, 0.0, D * P["cap"] * (1 - 1e-9))

    def g(D):
        e = (1 - c) * P["fare"] * trips(D) / D
        return D - P["drivers"] * _logistic((e - P["w0"]) / P["s_d"])

    D = optimize.brentq(g, 1e-3, P["drivers"])
    t = trips(D)
    w = wait(t, D)
    e = (1 - c) * P["fare"] * t / D
    u_r = P["a_r"] - P["b_r"] * P["fare"] - P["w_r"] * w
    return {"c": float(c), "trips": float(t), "drivers": float(D), "wait": float(w), "earnings": float(e),
            "platform": float(c * P["fare"] * t),
            "rider_cs": float(P["riders"] * np.log1p(np.exp(u_r)) / P["b_r"]),
            "driver_surplus": float(P["drivers"] * P["s_d"] * np.log1p(np.exp((e - P["w0"]) / P["s_d"])))}


def commission(cs=None, params: dict | None = None) -> dict:
    """The commission's trade-off: :func:`commission_market` on a grid of commissions; the platform's best
    commission, and the commission that maximizes the sum of the platform's take and both sides' surplus."""
    cs = np.round(np.arange(0.0, 0.61, 0.01), 2) if cs is None else np.asarray(cs, float)
    rows = [commission_market(c, params) for c in cs]
    out = {k: [r[k] for r in rows] for k in rows[0]}
    total = np.array(out["platform"]) + np.array(out["rider_cs"]) + np.array(out["driver_surplus"])
    out["total"] = total.tolist()
    out["best_c"] = float(cs[int(np.argmax(out["platform"]))])
    out["best_total_c"] = float(cs[int(np.argmax(total))])
    return out


# ---------------------------------------------------------------------------------------------------------------
# ranking


def ranking(n_slots: int = 10, decay: float = 0.75, seed: int = 61) -> dict:
    """A position-based click model: the chance that a shopper examines slot k falls as k^(-decay); a listing of
    relevance r is clicked with probability examine(k) x r.  Listings sorted by relevance; then the most relevant
    listing is swapped with a sponsored listing from slot 6.  Returns each slot's examination rate, expected clicks,
    and the clicks and relevance-weighted clicks (match quality) before and after the swap."""
    rng = np.random.default_rng(seed)
    rel = np.sort(rng.beta(2, 3, n_slots))[::-1]
    k = np.arange(1, n_slots + 1)
    ex = k ** (-decay)
    clicks = ex * rel
    spon = rel.copy()
    spon[[0, 5]] = spon[[5, 0]]
    clicks_s = ex * spon
    # match quality: the expected relevance of a click
    return {"slot": k.tolist(), "examine": ex.tolist(), "relevance": rel.tolist(), "clicks": clicks.tolist(),
            "total": float(clicks.sum()), "total_sponsored": float(clicks_s.sum()),
            "quality": float((clicks * rel).sum() / clicks.sum()),
            "quality_sponsored": float((clicks_s * spon).sum() / clicks_s.sum()),
            "top_vs_fifth": float(ex[0] / ex[4])}


# ---------------------------------------------------------------------------------------------------------------
# reputation


def reputation(n_sellers: int = 2000, sales: int = 200, p_rate_happy: float = 0.6, p_rate_unhappy: float = 0.05,
               seed: int = 61) -> dict:
    """Sellers' true chance of a good transaction is spread between 0.80 and 0.99.  A happy buyer leaves a positive
    rating with probability ``p_rate_happy``; an unhappy one leaves a negative rating with probability
    ``p_rate_unhappy`` and otherwise says nothing.  Percent positive (positives over ratings) piles up near 100%;
    effective percent positive (positives over transactions) spreads sellers out, and tracks their quality better."""
    rng = np.random.default_rng(seed)
    q = rng.uniform(0.80, 0.99, n_sellers)
    good = rng.binomial(sales, q)
    pos = rng.binomial(good, p_rate_happy)
    neg = rng.binomial(sales - good, p_rate_unhappy)
    pp = pos / np.maximum(pos + neg, 1)
    epp = pos / sales
    return {"quality": q.tolist(), "pp": pp.tolist(), "epp": epp.tolist(), "pp_median": float(np.median(pp)),
            "pp_mean": float(pp.mean()), "epp_median": float(np.median(epp)),
            "corr_pp": float(np.corrcoef(q, pp)[0, 1]), "corr_epp": float(np.corrcoef(q, epp)[0, 1]),
            "share_above_98": float(np.mean(pp >= 0.98))}


# ---------------------------------------------------------------------------------------------------------------
# ad auctions


def gsp(bids=(4.0, 3.0, 2.5, 1.0), quality=(0.5, 1.0, 0.7, 0.9), ctr=(0.30, 0.18, 0.10),
        reserve: float = 0.0) -> dict:
    """The generalized second-price auction with quality scores (Part 16's slots).  Quality is the chance that a
    searcher clicks the ad relative to an average ad; the slot k click rate is ctr[k] x quality.  Advertisers are
    ranked by bid x quality; each pays per click the least bid that keeps its rank, the next score divided by its own
    quality, and at least the reserve.  Returns the ranking, prices and clicks per search, with quality scores and by
    bid alone (each paying the next bid)."""
    b, q, c = np.asarray(bids, float), np.asarray(quality, float), np.asarray(ctr, float)
    out = {}
    for name, score, qq in (("quality", b * q, q), ("bid only", b.copy(), np.ones_like(q))):
        ranked = [int(i) for i in np.argsort(-score) if b[i] >= reserve]
        order = ranked[:len(c)]
        prices = []
        for k, i in enumerate(order):
            nxt = ranked[k + 1] if k + 1 < len(ranked) else None
            prices.append(float(max(score[nxt] / qq[i] if nxt is not None else 0.0, reserve)))
        clicks = [float(c[k] * q[i]) for k, i in enumerate(order)]
        out[name] = {"order": order, "prices": prices, "clicks": clicks,
                     "revenue": float(sum(p_ * cl for p_, cl in zip(prices, clicks))),
                     "total_clicks": float(sum(clicks))}
    return out


def search_ads(regions: int = 210, weeks: int = 16, off_share: float = 0.3, frequent: float = 0.4,
               p_frequent: float = 0.3, p_new: float = 0.02, lift: float = 0.003, click: float = 0.5,
               cpc: float = 0.5, value: float = 50.0, noise: float = 0.15, reps: int = 200, seed: int = 61) -> dict:
    """The Island's marketplace buys search ads.  Of each region-week's searchers, a share ``frequent`` are regular
    buyers who buy with probability ``p_frequent`` whether or not an ad is shown; the rest buy with probability
    ``p_new``, raised by ``lift`` when they see the ad.  When ads run, a share ``click`` of searchers click the ad
    (otherwise they click the free link), at ``cpc`` dollars a click.  Searches vary by region and week, and so,
    by ``noise`` (a log standard deviation), does what each searcher spends.
    Three returns on a dollar of advertising (revenue gained per dollar, less one): (a) the attribution method, which
    counts every sale made through an ad click; (b) a regression of log revenue on log spending across regions and
    weeks while ads ran everywhere; (c) the experiment: ads off in a random ``off_share`` of regions for the last half
    of the weeks, by difference in differences, with a standard error from repeated experiments."""
    rng = np.random.default_rng(seed)
    true_roi = (1 - frequent) * lift * value / (click * cpc) - 1
    attributed = click * (frequent * p_frequent + (1 - frequent) * (p_new + lift)) * value / (click * cpc) - 1
    est, ols = [], []
    for _ in range(reps):
        base = np.exp(rng.normal(np.log(20000), 0.8, regions))
        S = base[:, None] * np.exp(rng.normal(0, 0.15, (regions, weeks)) + 0.1 * np.sin(np.arange(weeks) / 2.0))
        off = rng.random(regions) < off_share
        post = np.arange(weeks) >= weeks // 2
        on = ~(off[:, None] & post[None, :])
        buyers = (rng.binomial(np.round(S * frequent).astype(int), p_frequent)
                  + rng.binomial(np.round(S * (1 - frequent)).astype(int), p_new + lift * on))
        R = buyers * value * np.exp(rng.normal(0, noise, (regions, weeks)))
        spend = np.where(on, rng.binomial(np.round(S).astype(int), click) * cpc, 0.0)
        # (b) across regions and weeks, before the experiment
        pre = ~post
        x = np.log(spend[:, pre]).ravel()
        y = np.log(R[:, pre]).ravel()
        beta = np.polyfit(x, y, 1)[0]
        ols.append(beta * R[:, pre].sum() / spend[:, pre].sum() - 1)
        # (c) difference in differences in revenue per searcher, scaled by spending per searcher
        r = R / S
        d_on = r[~off][:, post].mean() - r[~off][:, pre].mean()
        d_off = r[off][:, post].mean() - r[off][:, pre].mean()
        gain = d_on - d_off
        per = (spend[~off][:, post].sum() / S[~off][:, post].sum())
        est.append(gain / per - 1)
    return {"true_roi": float(true_roi), "attributed_roi": float(attributed), "ols_roi": float(np.mean(ols)),
            "experiment_roi": float(np.mean(est)), "experiment_sd": float(np.std(est)),
            "experiment_draws": [float(v) for v in est[:60]], "frequent": frequent, "regions": regions,
            "off_share": off_share}


# ---------------------------------------------------------------------------------------------------------------
# measuring advertising


def ad_power(spend_per_user: float = 0.10, roi: float = 0.25, sales_mean: float = 7.0, sales_sd: float = 75.0,
             alpha: float = 0.05, power: float = 0.8) -> dict:
    """Lewis and Rao's arithmetic: an ad campaign spends ``spend_per_user``; a return of ``roi`` means extra sales of
    spend x (1 + roi) per exposed user (sales counted at the margin needed to break even are ignored).  With sales per
    user this noisy, the number of users per arm needed to tell the return from zero (and from -100%) at the given
    size and power."""
    za, zb = stats.norm.ppf(1 - alpha / 2), stats.norm.ppf(power)
    effect = spend_per_user * (1 + roi)

    def n_for(delta):
        return 2 * (za + zb) ** 2 * sales_sd ** 2 / delta ** 2
    return {"effect": effect, "n_detect_effect": n_for(effect), "n_tell_roi_from_zero": n_for(spend_per_user * roi),
            "sd_to_mean": sales_sd / sales_mean, "share_of_sd": effect / sales_sd}


# ---------------------------------------------------------------------------------------------------------------
# experiments at scale


def peeking(days: int = 30, users_per_day: int = 2000, reps: int = 2000, keep: int = 12, seed: int = 61) -> dict:
    """A/A tests (no true effect) on a conversion rate of 5%, read every day; the share that ever show p < 0.05,
    against the share that do on the last day only.  The first ``keep`` tests' daily z statistics are returned."""
    rng = np.random.default_rng(seed)
    p = 0.05
    ever = 0
    last = 0
    paths = []
    for r in range(reps):
        a = rng.binomial(users_per_day, p, days).cumsum()
        b = rng.binomial(users_per_day, p, days).cumsum()
        n = users_per_day * np.arange(1, days + 1)
        pa, pb = a / n, b / n
        pool = (a + b) / (2 * n)
        z = (pa - pb) / np.sqrt(pool * (1 - pool) * 2 / n)
        sig = np.abs(z) > 1.96
        ever += sig.any()
        last += sig[-1]
        if r < keep:
            paths.append(z.tolist())
    return {"ever": float(ever / reps), "last": float(last / reps), "days": days, "paths": paths}


def cuped(n: int = 20000, rho: float = 0.7, effect: float = 0.02, reps: int = 400, seed: int = 61) -> dict:
    """Spending in the test period correlates ``rho`` with spending before it; adjusting the difference in means by
    the pre-period covariate (CUPED) cuts the variance by about rho squared.  Returns both estimators' standard
    deviations across replications."""
    rng = np.random.default_rng(seed)
    plain, adj = [], []
    for _ in range(reps):
        x = rng.normal(0, 1, n)
        y = rho * x + np.sqrt(1 - rho ** 2) * rng.normal(0, 1, n)
        t = rng.random(n) < 0.5
        y = y + effect * t
        plain.append(y[t].mean() - y[~t].mean())
        th = np.cov(x, y)[0, 1] / np.var(x)
        ya = y - th * (x - x.mean())
        adj.append(ya[t].mean() - ya[~t].mean())
    return {"sd_plain": float(np.std(plain)), "sd_cuped": float(np.std(adj)),
            "ratio": float(np.var(adj) / np.var(plain)), "predicted": 1 - rho ** 2}


# ---------------------------------------------------------------------------------------------------------------
# marketplace experiments


def _rides(rng, n_t, n_c, p_t, p_c, D):
    """One market-period: n_t treated and n_c control riders want a ride with probabilities p_t and p_c; D drivers;
    when more want rides than there are drivers, the drivers go to a random subset of those who want one (so the
    treated and control riders share the shortage).  Returns rides to treated and to control riders."""
    W_t = rng.binomial(n_t, p_t)
    W_c = rng.binomial(n_c, p_c)
    S = np.minimum(W_t + W_c, D)
    S_t = np.where(S > 0, rng.hypergeometric(np.maximum(W_t, 0), np.maximum(W_c, 0), np.maximum(S, 0)), 0)
    return S_t, S - S_t


def switchback(cities: int = 20, periods: int = 48, riders: int = 300, drivers: float = 170.0, p0: float = 0.5,
               lift: float = 0.4, city_sd: float = 0.15, reps: int = 400, seed: int = 61) -> dict:
    """A rider discount tested three ways in a market where drivers are shared.  In each city-period, riders want a
    ride with probability p0 (p0 x (1 + lift) with the discount); drivers number Poisson(drivers x the city's size
    x its drivers per rider).
    By user: half the riders in every city-period get the discount; compare their rides with the others'.
    Switchback: each city-period is wholly discounted or not, at random.  By city: half the cities are discounted
    for all their periods.  The truth: rides per rider with the discount for everyone minus without it."""
    rng = np.random.default_rng(seed)
    p1 = p0 * (1 + lift)
    P = cities * periods
    size = np.exp(rng.normal(0, city_sd, cities))
    slack = np.exp(rng.normal(0, city_sd, cities))      # drivers per rider differ by city too
    city_of = np.repeat(np.arange(cities), periods)
    est = {"user": [], "switchback": [], "city": []}
    truth = []
    for _ in range(reps):
        D = rng.poisson(drivers * size[city_of] * slack[city_of])
        n = np.round(riders * size[city_of]).astype(int)
        nt = n // 2
        a, b = _rides(rng, nt, n - nt, p1, p0, D)
        est["user"].append(np.mean(a / nt) - np.mean(b / (n - nt)))
        tr = rng.random(P) < 0.5
        r1, _ = _rides(rng, n, np.zeros(P, int), p1, p0, D)
        _, r0 = _rides(rng, np.zeros(P, int), n, p1, p0, D)
        truth.append(np.mean((r1 - r0) / n))
        y = np.where(tr, r1, r0) / n
        est["switchback"].append(y[tr].mean() - y[~tr].mean())
        tc = rng.permutation(cities) < cities // 2
        trc = tc[city_of]
        yc = np.where(trc, r1, r0) / n
        est["city"].append(yc[trc].mean() - yc[~trc].mean())
    return {**{k: float(np.mean(v)) for k, v in est.items()}, **{k + "_sd": float(np.std(v)) for k, v in est.items()},
            "truth": float(np.mean(truth)), "demand_off": p0 * riders, "demand_on": p1 * riders, "drivers": drivers,
            "naive_ratio": float(np.mean(est["user"]) / np.mean(truth))}


# ---------------------------------------------------------------------------------------------------------------
# uplift


def uplift(n: int = 50000, budget: float = 0.3, seed: int = 61) -> dict:
    """Users differ in how much a promotion changes their chance of buying: tau = 0.10 x a feature, negative for some
    (they would have bought anyway and the coupon only costs).  Target the top ``budget`` share by (a) the true tau,
    (b) a noisy estimate of it, (c) at random, (d) by the chance of buying without the promotion (the usual mistake).
    Returns the extra purchases per targeted user under each rule and the Qini-style curve for the estimate."""
    rng = np.random.default_rng(seed)
    x = rng.normal(0, 1, n)
    base = 1 / (1 + np.exp(-(-2.0 + 1.2 * x)))
    tau = 0.06 * (1 - x) * (x < 2.5)
    est = tau + rng.normal(0, 0.03, n)
    k = int(budget * n)
    rules = {"true effect": np.argsort(-tau), "estimated effect": np.argsort(-est),
             "at random": rng.permutation(n), "likeliest buyers": np.argsort(-base)}
    gains = {name: float(tau[idx[:k]].mean()) for name, idx in rules.items()}
    order = np.argsort(-est)
    curve_x = np.linspace(0, 1, 41)
    curve = [float(tau[order[:max(int(f * n), 1)]].sum() / n) for f in curve_x]
    return {"gains": gains, "curve_x": curve_x.tolist(), "curve": curve, "avg_tau": float(tau.mean()),
            "share_negative": float(np.mean(tau < 0)), "budget": budget}


def long_term(n: int = 40000, n_obs: int = 40000, seed: int = 61) -> dict:
    """A discount for a month raises orders now but teaches some customers to wait for the next one.  Each customer
    has a taste u; the experiment's short-term outcome is orders in the first four weeks; the long-term outcome,
    orders over a year, depends only on the first month's orders and on engagement (sessions) in weeks five to
    eight, which the discount lowers.  The surrogate index (Athey, Chetty, Imbens and Kang) is fitted on last
    year's customers, who were not in the experiment, and applied to the experiment's arms after eight weeks."""
    from explainer.stats.kit import frontier as FR
    rng = np.random.default_rng(seed)

    def people(m, treat):
        u = rng.normal(0, 1, m)
        short = rng.poisson(np.exp(0.2 + 0.5 * u + 0.35 * treat))
        sessions = rng.poisson(np.exp(1.5 + 0.4 * u - 0.35 * treat))
        year = rng.poisson(0.5 + 1.2 * short + 0.6 * sessions)
        return short, sessions, year

    t = (rng.random(n) < 0.5).astype(int)
    short, sess, year = people(n, t)
    s0, e0, y0 = people(n_obs, np.zeros(n_obs))
    S_obs = np.column_stack([s0, e0])
    S_exp = np.column_stack([short, sess])
    si = FR.surrogate_index(S_obs, y0, S_exp, t)
    base = year[t == 0].mean()
    return {"short": float(short[t == 1].mean() / short[t == 0].mean() - 1),
            "surrogate": float(si["effect"] / base), "surrogate_se": float(si["se"] / base),
            "truth": float(year[t == 1].mean() / base - 1), "base_year": float(base)}


def wta_survey(n: int = 4000, median: float = 15000.0, sd_log: float = 1.3, seed: int = 61) -> dict:
    """What a free good is worth, as Brynjolfsson, Collis and Eggers asked: each respondent is offered a random amount
    to give up a search engine for a year and accepts if it exceeds their own value.  A logit of acceptance on the
    log of the offer recovers the median valuation where half accept."""
    rng = np.random.default_rng(seed)
    wta = np.exp(rng.normal(np.log(median), sd_log, n))
    offers = np.exp(rng.uniform(np.log(100.0), np.log(1e6), n))
    acc = (offers > wta).astype(float)
    X = np.column_stack([np.ones(n), np.log(offers)])
    b = np.zeros(2)
    for _ in range(50):
        p_ = 1 / (1 + np.exp(-X @ b))
        W = p_ * (1 - p_)
        b = b + np.linalg.solve(X.T @ (X * W[:, None]), X.T @ (acc - p_))
    grid = np.exp(np.linspace(np.log(100.0), np.log(1e6), 60))
    bins = np.exp(np.linspace(np.log(100.0), np.log(1e6), 13))
    mid = np.sqrt(bins[:-1] * bins[1:])
    share = [float(acc[(offers >= lo) & (offers < hi)].mean()) for lo, hi in zip(bins[:-1], bins[1:])]
    return {"median_hat": float(np.exp(-b[0] / b[1])), "median": median, "b": b.tolist(), "grid": grid.tolist(),
            "fit": (1 / (1 + np.exp(-(b[0] + b[1] * np.log(grid))))).tolist(), "bin_mid": mid.tolist(),
            "bin_share": share, "n": n}


# ---------------------------------------------------------------------------------------------------------------
# flexible work


def flexibility(n_drivers: int = 5000, hours: int = 24, wage: float = 20.0, shift: int = 8, seed: int = 61) -> dict:
    """Each driver's reservation wage varies by hour of the day (a personal level plus hour-to-hour shocks).  With
    flexible hours a driver works every hour whose reservation wage is below the wage; with a fixed shift the driver
    chooses the best block of ``shift`` consecutive hours, or none.  Surplus is the wage less the reservation wage on
    hours worked, summed (after Chen, Chevalier, Rossi and Oehlsen)."""
    rng = np.random.default_rng(seed)
    level = rng.normal(25.0, 6.0, n_drivers)
    shock = rng.normal(0.0, 9.0, (n_drivers, hours))
    r = level[:, None] + shock
    gain = np.maximum(wage - r, 0.0)
    flex = gain.sum(axis=1)
    hours_flex = (wage > r).sum(axis=1)
    g = wage - r
    blocks = np.stack([g[:, s:s + shift].sum(axis=1) for s in range(hours - shift + 1)], axis=1)
    fixed = np.maximum(blocks.max(axis=1), 0.0)
    works_fixed = blocks.max(axis=1) > 0
    return {"flex": float(flex.mean()), "fixed": float(fixed.mean()), "ratio": float(flex.mean() / fixed.mean()),
            "hours_flex": float(hours_flex.mean()), "hours_fixed": float(shift * works_fixed.mean()),
            "share_fixed_work": float(works_fixed.mean())}


__all__ = [n for n in dir() if not n.startswith("_") and n not in ("np", "optimize", "stats", "annotations")]
