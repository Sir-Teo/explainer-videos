"""Agora's revenue manager (Part 60): how firms set prices, with the Island's airline, shops and survey respondents.

* **Cost-plus** (:func:`markup_profit`, :func:`cost_plus_robustness`): the markup rule p = c e/(e - 1) against a fixed
  markup when the elasticity is only estimated.
* **Willingness to pay** (:func:`conjoint`): a choice-based conjoint survey simulated and fitted by a multinomial logit,
  with willingness to pay for each feature and its standard error.
* **Experiments with interference** (:func:`interference`): an A/B test of a discount in a market with limited rooms,
  against the global effect and a test randomized by market.
* **Revenue management** (:func:`littlewood`, :func:`emsr_b`, :func:`overbooking`): two fares with Poisson demand and
  the protection level, several fare classes by EMSR-b, the booking limit with no-shows.
* **Dynamic pricing** (:func:`flight`, :func:`dp_prices`, :func:`simulate`): a hundred seats over sixty days with
  buyers whose willingness to pay rises as departure nears; the optimal policy by dynamic programming (after Gallego
  and van Ryzin), against a fixed price and the Play-it's weekly rules.
* **Uniform pricing** (:func:`chain`): a chain of stores with different elasticities, priced store by store or
  uniformly (after DellaVigna and Gentzkow).
* **Versions and contracts** (:func:`menu`, :func:`mfn`): good, better, best by Mussa and Rosen's rule for discrete
  types; a most-favoured-customer clause.
* **Bundles** (:func:`big_bundle`): Bakos and Brynjolfsson's large bundles of goods with independent values.
* **Reference prices** (:func:`hilo`): a store's weekly sales under high-low promotions and everyday low prices, with
  shoppers who value a deal.
* **Pass-through** (:func:`passthrough_lags`): a distributed-lag regression of retail on producer prices.
* **Bandits** (:func:`bandit_pricing`): Thompson sampling against test-then-commit on a grid of prices.

numpy and scipy only.
"""

from __future__ import annotations

import numpy as np
from scipy import optimize, stats

# ---------------------------------------------------------------------------------------------------------------
# cost-plus


def markup_profit(p, eps: float, c: float = 1.0) -> np.ndarray:
    """Profit (p - c) p^(-eps) with constant-elasticity demand of scale one."""
    p = np.asarray(p, float)
    return (p - c) * p ** (-eps)


def cost_plus_robustness(eps_true: float = 2.6, sd_log: float = 0.35, markup: float = 0.5, n: int = 20000,
                         seed: int = 60) -> dict:
    """A firm that knows its cost but only estimates its elasticity (log-normal around the truth, s.d. ``sd_log``).
    Rule A sets the textbook price for its estimate, c e/(e - 1), with the estimate floored at 1.2; rule B adds a fixed
    markup.  Returns each rule's profit as a share of the profit at the true optimum, on average and at the 10th
    percentile."""
    rng = np.random.default_rng(seed)
    est = np.maximum(eps_true * np.exp(rng.normal(0.0, sd_log, n)), 1.2)
    best = markup_profit(eps_true / (eps_true - 1), eps_true)
    a = markup_profit(est / (est - 1), eps_true) / best
    b = float(markup_profit(1 + markup, eps_true) / best)
    grid = np.linspace(1.05, 3.0, 200)
    return {"eps": eps_true, "markup": markup, "rule_mean": float(a.mean()), "rule_p10": float(np.quantile(a, 0.1)),
            "rule_worst": float(a.min()), "fixed": b, "grid": grid, "curve": markup_profit(grid, eps_true) / best,
            "p_opt": eps_true / (eps_true - 1)}


# ---------------------------------------------------------------------------------------------------------------
# willingness to pay: choice-based conjoint

CONJOINT = {"price": -0.08, "wifi": 0.9, "legroom": 1.4, "bag": 0.6, "none": -9.0}


def conjoint(n_resp: int = 400, tasks: int = 8, alts: int = 3, seed: int = 60, beta: dict | None = None) -> dict:
    """Each respondent sees ``tasks`` choice sets of ``alts`` fares (price 60-180, with or without wifi, extra legroom
    and a free bag) and may choose none.  Choices follow a logit with the planted ``beta``; the multinomial logit is
    fitted by Newton's method.  Willingness to pay for a feature is -beta_feature / beta_price, with delta-method
    errors."""
    B = {**CONJOINT, **(beta or {})}
    rng = np.random.default_rng(seed)
    names = ["price", "wifi", "legroom", "bag"]
    X, Y = [], []
    for _ in range(n_resp * tasks):
        price = rng.choice(np.arange(60, 181, 20), alts).astype(float)
        feats = rng.integers(0, 2, (alts, 3)).astype(float)
        x = np.column_stack([price, feats])
        xo = np.vstack([np.column_stack([x, np.zeros(alts)]), np.r_[np.zeros(4), 1.0]])
        u = xo @ np.array([B[k] for k in names] + [B["none"]])
        g = u + rng.gumbel(size=alts + 1)
        X.append(xo)
        Y.append(int(np.argmax(g)))
    X = np.array(X)
    Y = np.array(Y)
    b = np.zeros(5)
    for _ in range(50):
        U = X @ b
        U -= U.max(axis=1, keepdims=True)
        P = np.exp(U)
        P /= P.sum(axis=1, keepdims=True)
        xbar = np.einsum("nj,njk->nk", P, X)
        chosen = X[np.arange(len(Y)), Y]
        grad = (chosen - xbar).sum(axis=0)
        H = -np.einsum("nj,njk,njl->kl", P, X - xbar[:, None, :], X - xbar[:, None, :])
        step = np.linalg.solve(H, grad)
        b -= step
        if np.max(np.abs(step)) < 1e-10:
            break
    V = np.linalg.inv(-H)
    wtp, se = {}, {}
    for j, k in enumerate(names[1:], start=1):
        w = -b[j] / b[0]
        gvec = np.zeros(5)
        gvec[0] = b[j] / b[0] ** 2
        gvec[j] = -1 / b[0]
        wtp[k] = float(w)
        se[k] = float(np.sqrt(gvec @ V @ gvec))
    truth = {k: -B[k] / B["price"] for k in names[1:]}
    return {"beta": dict(zip(names + ["none"], b.tolist())), "se_beta": np.sqrt(np.diag(V)).tolist(), "wtp": wtp,
            "wtp_se": se, "truth": truth, "n_choices": int(len(Y)), "share_none": float(np.mean(Y == alts))}


# ---------------------------------------------------------------------------------------------------------------
# experiments with interference


def _book(values, prices, rooms):
    """Buyers in arrival order book if their value exceeds their price and a room is left."""
    booked = np.zeros(len(values), bool)
    left = rooms
    for i in range(len(values)):
        if left <= 0:
            break
        if values[i] > prices[i]:
            booked[i] = True
            left -= 1
    return booked


def interference(n_buyers: int = 600, rooms: int = 270, price: float = 100.0, discount: float = 0.10,
                 markets: int = 40, reps: int = 200, seed: int = 60) -> dict:
    """Hotel rooms in ``markets`` cities, each with ``rooms`` rooms and ``n_buyers`` arriving buyers (values
    log-normal, median 90).  The test gives a random half of buyers a discount.  The naive estimate is the difference
    in booking rates between treated and control buyers; the global effect is the change in bookings per buyer from
    giving everyone the discount instead of no one.  With rooms scarce, treated buyers take rooms control buyers would
    have had, so the naive estimate overstates the effect.  A test randomized by city compares whole markets."""
    rng = np.random.default_rng(seed)
    naive, glob, clus = [], [], []
    for _ in range(reps):
        res_ab, res_g = [], []
        treat_city = rng.random(markets) < 0.5
        city_rates = []
        for m in range(markets):
            v = np.exp(rng.normal(np.log(90.0), 0.45, n_buyers))
            t = rng.random(n_buyers) < 0.5
            p_ab = np.where(t, price * (1 - discount), price)
            bk = _book(v, p_ab, rooms)
            res_ab.append((bk[t].mean(), bk[~t].mean()))
            b0 = _book(v, np.full(n_buyers, price), rooms).mean()
            b1 = _book(v, np.full(n_buyers, price * (1 - discount)), rooms).mean()
            res_g.append(b1 - b0)
            city_rates.append(b1 if treat_city[m] else b0)
        res_ab = np.array(res_ab)
        naive.append(res_ab[:, 0].mean() - res_ab[:, 1].mean())
        glob.append(np.mean(res_g))
        cr = np.array(city_rates)
        if treat_city.any() and (~treat_city).any():
            clus.append(cr[treat_city].mean() - cr[~treat_city].mean())
    naive, glob, clus = np.array(naive), np.array(glob), np.array(clus)
    return {"naive": float(naive.mean()), "global": float(glob.mean()), "cluster": float(clus.mean()),
            "naive_runs": naive.tolist(), "cluster_runs": clus.tolist(),
            "cluster_sd": float(clus.std()), "naive_sd": float(naive.std()), "ratio": float(naive.mean() / glob.mean()),
            "rooms": rooms, "buyers": n_buyers, "discount": discount, "markets": markets}


# ---------------------------------------------------------------------------------------------------------------
# revenue management


def littlewood(p_hi: float = 400.0, p_lo: float = 150.0, mean_hi: float = 30.0, seats: int = 100,
               mean_lo: float = 200.0) -> dict:
    """Two fares on one flight.  Low-fare buyers book first and are plentiful (Poisson with mean ``mean_lo``);
    high-fare buyers come later (Poisson with mean ``mean_hi``).  Protecting y seats for the high fare means selling at
    most seats - y at the low fare.  Expected revenue for every y, exactly; Littlewood's rule (1972) protects the
    smallest y with P(D_hi > y) <= p_lo/p_hi."""
    Dh = stats.poisson(mean_hi)
    Dl = stats.poisson(mean_lo)
    ys = np.arange(0, seats + 1)
    rev = []
    kk = np.arange(0, seats + 1)
    pl = Dl.pmf(kk)
    pl[-1] += Dl.sf(seats)
    for y in ys:
        lim = seats - y
        sold_lo = np.minimum(kk, lim)
        e_lo = float(np.sum(pl * sold_lo))
        # the high fare gets what is left: seats - sold_lo
        e_hi = 0.0
        for k, w in zip(kk, pl):
            cap = seats - min(k, lim)
            j = np.arange(0, cap + 1)
            ph = Dh.pmf(j)
            e_hi += w * (np.sum(ph * j) + Dh.sf(cap) * cap)
        rev.append(p_lo * e_lo + p_hi * e_hi)
    rev = np.array(rev)
    ratio = p_lo / p_hi
    y_star = int(np.argmax(Dh.sf(ys) <= ratio))
    return {"ys": ys, "revenue": rev, "y_star": y_star, "y_best": int(np.argmax(rev)), "ratio": ratio,
            "rev_star": float(rev[y_star]), "rev_none": float(rev[0]), "rev_fcfs": float(rev[0]),
            "rev_best": float(rev.max()), "p_hi": p_hi, "p_lo": p_lo, "mean_hi": mean_hi, "seats": seats,
            "sf": Dh.sf(ys)}


def emsr_b(fares=(450.0, 300.0, 200.0, 120.0), means=(15.0, 25.0, 40.0, 60.0), sds=(5.0, 8.0, 12.0, 18.0)) -> dict:
    """Belobaba's EMSR-b: for each class j, aggregate the classes above it (demand-weighted average fare, summed means
    and variances) and protect for them as Littlewood would against fare j.  Returns the nested protection levels."""
    f, mu, sd = map(lambda a: np.asarray(a, float), (fares, means, sds))
    prot = []
    for j in range(1, len(f)):
        m = mu[:j].sum()
        s = np.sqrt((sd[:j] ** 2).sum())
        fbar = (f[:j] * mu[:j]).sum() / m
        prot.append(float(stats.norm.ppf(1 - f[j] / fbar, m, s)))
    return {"fares": f.tolist(), "protect": prot}


def overbooking(seats: int = 100, show: float = 0.9, fare: float = 200.0, bump: float = 600.0,
                max_sell: int = 130) -> dict:
    """Sell b tickets (refundable, demand ample); each shows up independently with probability ``show``; revenue is
    the fare on every passenger who shows, less the cost of bumping each one beyond the seats.  The best b, and the
    marginal rule: sell one more while fare x show > bump x P(the extra passenger is bumped)."""
    bs = np.arange(seats, max_sell + 1)
    val = []
    for b in bs:
        k = np.arange(0, b + 1)
        pk = stats.binom.pmf(k, b, show)
        val.append(float(np.sum(pk * (fare * k - bump * np.maximum(k - seats, 0)))))
    val = np.array(val)
    i = int(np.argmax(val))
    deny = []
    for b in bs:
        k = np.arange(0, b + 1)
        pk = stats.binom.pmf(k, b, show)
        deny.append(float(np.sum(pk * np.maximum(k - seats, 0))))
    return {"bs": bs, "value": val, "best": int(bs[i]), "value_best": float(val[i]), "value_no": float(val[0]),
            "bumped_best": deny[i], "deny": deny}


# ---------------------------------------------------------------------------------------------------------------
# dynamic pricing

FLIGHT = {"seats": 100, "days": 60, "early": 5.0, "late": 4.0, "mu_early": 90.0, "mu_late": 260.0, "switch": 21}


def flight(params: dict | None = None) -> dict:
    """The Island's flight: each day t (days before departure 60..1) buyers arrive as a Poisson stream whose size
    and willingness to pay change as departure nears: leisure buyers (mean value ``mu_early``) early, business buyers
    (``mu_late``) in the last ``switch`` days; values are exponential.  At price p the day's demand is Poisson with
    mean lambda_t exp(-p / mu_t)."""
    P = {**FLIGHT, **(params or {})}
    days = np.arange(P["days"], 0, -1)
    lam = np.where(days > P["switch"], P["early"], P["late"]).astype(float)
    mu = np.where(days > P["switch"], P["mu_early"], P["mu_late"]).astype(float)
    return {**P, "dleft": days, "lam": lam, "mu": mu}


def _sales_matrix(means, x):
    """P(sales = k), k = 0..x, for Poisson demands with the given means (one row per mean) and x seats left."""
    k = np.arange(0, x + 1)
    m = np.asarray(means, float)[:, None]
    P = stats.poisson.pmf(k[None, :], m)
    P[:, -1] = stats.poisson.sf(x - 1, m[:, 0]) if x > 0 else 1.0
    return P


def dp_prices(F: dict | None = None, grid=None) -> dict:
    """The optimal price for every day and every number of seats left, by backward induction on
    V_t(x) = max_p E[p min(D, x) + V_{t+1}(x - min(D, x))], D ~ Poisson(lambda_t exp(-p/mu_t)).  Also the best single
    price for the whole sale, found by the same recursion with the price held fixed."""
    F = F or flight()
    grid = np.arange(40.0, 501.0, 5.0) if grid is None else np.asarray(grid, float)
    T, C = F["days"], F["seats"]
    V = np.zeros(C + 1)
    policy = np.zeros((T, C + 1))
    values = np.zeros((T + 1, C + 1))
    for t in range(T - 1, -1, -1):
        means = F["lam"][t] * np.exp(-grid / F["mu"][t])
        newV = np.zeros(C + 1)
        for x in range(1, C + 1):
            P = _sales_matrix(means, x)
            k = np.arange(0, x + 1)
            val = P @ V[x - k] + grid * (P @ k)
            i = int(np.argmax(val))
            newV[x] = val[i]
            policy[t, x] = grid[i]
        V = newV
        values[t] = V
    return {"V0": float(V[C]), "policy": policy, "values": values, "grid": grid, "fixed": fixed_price_value(F, grid)}


def fixed_price_value(F: dict, grid) -> dict:
    """Expected revenue of holding one price for the whole sale, for each price in ``grid``; the best of them."""
    T, C = F["days"], F["seats"]
    grid = np.asarray(grid, float)
    V = np.zeros((len(grid), C + 1))
    for t in range(T - 1, -1, -1):
        means = F["lam"][t] * np.exp(-grid / F["mu"][t])
        newV = np.zeros_like(V)
        for x in range(1, C + 1):
            P = _sales_matrix(means, x)
            k = np.arange(0, x + 1)
            newV[:, x] = np.sum(P * (V[:, x - k] + grid[:, None] * k[None, :]), axis=1)
        V = newV
    vals = V[:, C]
    i = int(np.argmax(vals))
    return {"grid": grid.tolist(), "value": vals.tolist(), "best_price": float(grid[i]), "best": float(vals[i])}


def simulate(policy, F: dict | None = None, reps: int = 2000, seed: int = 60) -> dict:
    """Monte Carlo of a pricing rule ``policy(t, x, sold_week)`` (t = day index from 0, x = seats left): revenue, seats
    sold and the share of flights that sell out before the last week."""
    F = F or flight()
    rng = np.random.default_rng(seed)
    rev, sold, early_out = np.zeros(reps), np.zeros(reps), 0
    for r in range(reps):
        x, total, week_sales = F["seats"], 0.0, 0
        out_day = None
        for t in range(F["days"]):
            if t % 7 == 0:
                week_sales = 0
            if x <= 0:
                if out_day is None:
                    out_day = t
                break
            p = float(policy(t, x, week_sales))
            d = rng.poisson(F["lam"][t] * np.exp(-p / F["mu"][t]))
            s = min(d, x)
            x -= s
            week_sales += s
            total += p * s
        rev[r] = total
        sold[r] = F["seats"] - x
        if out_day is not None and F["days"] - out_day >= 7:
            early_out += 1
    return {"mean": float(rev.mean()), "sd": float(rev.std()), "sold": float(sold.mean()),
            "sold_out_early": early_out / reps}


def playit_rules(F: dict | None = None, D: dict | None = None) -> dict:
    """The Play-it's four weekly rules, simulated: one price all along (the best fixed price); start high and cut when
    a week sells fewer than its share; start low and raise as departure nears; and the optimal policy."""
    F = F or flight()
    D = D or dp_prices(F)
    fixed = D["fixed"]["best_price"]
    pol = D["policy"]
    grid = D["grid"]

    def opt(t, x, ws):
        return pol[t, x]

    def one(t, x, ws):
        return fixed

    def high_cut():
        st = {"p": 320.0, "x_week": F["seats"]}

        def f(t, x, ws):
            if t == 0:
                st["p"], st["x_week"] = 320.0, x
            if t % 7 == 0 and t > 0:
                sold = st["x_week"] - x
                if sold < F["seats"] * 7 / F["days"]:
                    st["p"] = max(60.0, st["p"] * 0.85)
                st["x_week"] = x
            return st["p"]
        return f

    def low_raise(t, x, ws):
        week = t // 7
        return float(np.interp(week, [0, 8], [90.0, 300.0]))

    rules = {"one price": one, "start high, cut": high_cut(), "start low, raise": low_raise, "optimal": opt}
    out = {k: simulate(v, F) for k, v in rules.items()}
    del grid
    return {"rules": out, "fixed_price": fixed, "V0": D["V0"]}


# ---------------------------------------------------------------------------------------------------------------
# versions and contracts


def menu(thetas=(1.0, 1.5, 2.0), shares=(0.5, 0.3, 0.2)) -> dict:
    """Good, better, best: Mussa and Rosen's menu for discrete types.  A buyer of type theta values quality q at
    theta q; quality costs q^2/2.  The top type gets the efficient quality; each lower type's quality is cut by the
    share of buyers above it over its own share, times the gap to the next type (the rent it would hand them), and
    prices make each type indifferent to the version just below.  Against: one version for everyone, priced and sized
    to maximize profit."""
    th = np.asarray(thetas, float)
    sh = np.asarray(shares, float)
    n = len(th)
    q = np.zeros(n)
    for i in range(n):
        above = sh[i + 1:].sum()
        q[i] = th[i] if i == n - 1 else max(th[i] - above / sh[i] * (th[i + 1] - th[i]), 0.0)
    q = np.maximum.accumulate(q)
    p = np.zeros(n)
    p[0] = th[0] * q[0]
    for i in range(1, n):
        p[i] = p[i - 1] + th[i] * (q[i] - q[i - 1])
    profit = float(np.sum(sh * (p - q ** 2 / 2)))
    full = float(np.sum(sh * th ** 2 / 2))
    best1 = 0.0
    for k in range(n):
        # one version aimed at types k and above: quality and price that maximize profit from them
        mass = sh[k:].sum()
        qq = th[k]
        val = mass * (th[k] * qq - qq ** 2 / 2)
        best1 = max(best1, val)
    return {"thetas": th.tolist(), "shares": sh.tolist(), "q": q.tolist(), "p": p.tolist(), "profit": profit,
            "profit_full_info": full, "profit_one": float(best1),
            "rents": [float(th[i] * q[i] - p[i]) for i in range(n)]}


def mfn(a=(100.0, 60.0), b=(1.0, 1.0), c: float = 20.0) -> dict:
    """Two groups of buyers with linear demands q_i = a_i - b_i p.  Without constraints the seller charges each its
    own monopoly price; a most-favoured-customer clause promising the first group any lower price given to anyone
    forces one price.  Returns both sets of prices, quantities and profits."""
    a = np.asarray(a, float)
    b = np.asarray(b, float)
    p_sep = (a / b + c) / 2
    q_sep = a - b * p_sep
    prof_sep = float(np.sum((p_sep - c) * q_sep))
    p_one = (a.sum() + c * b.sum()) / (2 * b.sum())
    q_one = np.maximum(a - b * p_one, 0.0)
    prof_one = float(np.sum((p_one - c) * q_one))
    return {"p_sep": p_sep.tolist(), "q_sep": q_sep.tolist(), "profit_sep": prof_sep, "p_one": float(p_one),
            "q_one": q_one.tolist(), "profit_one": prof_one}


# ---------------------------------------------------------------------------------------------------------------
# uniform pricing


def chain(n_stores: int = 200, eps_mean: float = 2.5, eps_sd: float = 0.23, cost: float = 1.0, seed: int = 60) -> dict:
    """A chain's stores face constant-elasticity demand A_s p^(-e_s) with elasticities normal around ``eps_mean``
    (the 10th and 90th percentiles near DellaVigna and Gentzkow's -2.22 and -2.81) and sizes A_s.  Store-by-store
    prices are c e/(e - 1); the best uniform price maximizes total profit.
    Returns the prices, the profit forgone by uniform pricing, and who pays more under it."""
    rng = np.random.default_rng(seed)
    e = np.clip(rng.normal(eps_mean, eps_sd, n_stores), 1.6, 4.0)
    A = np.exp(rng.normal(0.0, 0.3, n_stores))
    p_s = cost * e / (e - 1)

    def total(p):
        return float(np.sum(A * (p - cost) * p ** (-e)))
    res = optimize.minimize_scalar(lambda p: -total(p), bounds=(1.05, 3.0), method="bounded")
    pu = float(res.x)
    flex = float(np.sum(A * (p_s - cost) * p_s ** (-e)))
    lo, hi = np.quantile(e, [0.1, 0.9])
    return {"eps": e.tolist(), "p_store": p_s.tolist(), "uniform": pu, "loss": 1 - total(pu) / flex,
            "gap_10_90": float((lo / (lo - 1)) / (hi / (hi - 1)) - 1),
            "share_pay_more": float(np.mean(pu > p_s)), "e10": float(lo), "e90": float(hi)}


# ---------------------------------------------------------------------------------------------------------------
# bundles


def big_bundle(ns=(1, 2, 5, 10, 20, 50, 100), consumers: int = 20000, seed: int = 60) -> dict:
    """Bakos and Brynjolfsson (1999): goods with zero marginal cost and values uniform on [0, 1], independent across
    goods and consumers.  Sold separately, each good earns 1/4 per consumer (price 1/2).  Sold as one bundle at the best
    price, revenue per good per consumer rises towards the mean value, 1/2, as the bundle grows, and deadweight loss
    falls towards nothing."""
    rng = np.random.default_rng(seed)
    out = []
    for n in ns:
        v = rng.random((consumers, n)).sum(axis=1)
        vs = np.sort(v)[::-1]
        rev = vs * np.arange(1, consumers + 1)
        i = int(np.argmax(rev))
        price = float(vs[i])
        per_good = float(rev[i] / consumers / n)
        buyers = (i + 1) / consumers
        surplus_total = float(v.mean() / n)
        out.append({"n": int(n), "price_per_good": price / n, "revenue_per_good": per_good, "buyers": buyers,
                    "deadweight": float(np.mean(np.where(v < price, v, 0.0)) / n), "total_value": surplus_total})
    return {"rows": out, "separate": 0.25}


# ---------------------------------------------------------------------------------------------------------------
# reference prices


def hilo(weeks: int = 52, regular: float = 50.0, sale: float = 35.0, edlp: float = 40.0, every: int = 2,
         eta: float = 0.8, shoppers: int = 1000, seed: int = 60) -> dict:
    """Shoppers value an item at log-normal values (median 42); each week they buy if value - price + eta x (reference
    - price)^+ > 0, where the reference is the store's posted regular price.  High-low: the regular price, with a sale
    every ``every`` weeks; everyday low pricing: one price, which becomes its own reference, so no deal is ever felt.
    Weekly units and revenue under each, and the eta at which they break even."""
    rng = np.random.default_rng(seed)
    v = np.exp(rng.normal(np.log(42.0), 0.35, shoppers))

    def units(price, ref, eta_):
        return int(np.sum(v - price + eta_ * max(ref - price, 0.0) > 0))

    def revenues(eta_):
        hl = [(sale if w % every == every - 1 else regular) for w in range(weeks)]
        r_hl = sum(p * units(p, regular, eta_) for p in hl)
        r_ed = weeks * edlp * units(edlp, edlp, eta_)
        return r_hl, r_ed
    r_hl, r_ed = revenues(eta)
    etas = np.linspace(0.0, 1.5, 31)
    diff = [revenues(x)[0] - revenues(x)[1] for x in etas]
    return {"revenue_hilo": float(r_hl), "revenue_edlp": float(r_ed), "etas": etas.tolist(), "diff": diff,
            "units_regular": units(regular, regular, eta), "units_sale": units(sale, regular, eta),
            "units_edlp": units(edlp, edlp, eta), "eta": eta}


# ---------------------------------------------------------------------------------------------------------------
# pass-through


def passthrough_lags(retail, producer, lags: int = 12) -> dict:
    """Monthly log changes of a retail price on the current and ``lags`` past log changes of a producer price, by least
    squares; the cumulative pass-through after each month (the elasticity of the retail price to the producer price)."""
    r = np.diff(np.log(np.asarray(retail, float)))
    q = np.diff(np.log(np.asarray(producer, float)))
    n = len(r)
    X = np.column_stack([np.ones(n - lags)] + [q[lags - k:n - k] for k in range(lags + 1)])
    y = r[lags:]
    b, *_ = np.linalg.lstsq(X, y, rcond=None)
    e = y - X @ b
    XtXi = np.linalg.inv(X.T @ X)
    V = XtXi @ (X.T * e ** 2) @ X @ XtXi
    cum = np.cumsum(b[1:])
    # the standard error of the cumulative sum at the last lag
    w = np.r_[0.0, np.ones(lags + 1)]
    return {"coef": b[1:].tolist(), "cum": cum.tolist(), "cum_se": float(np.sqrt(w @ V @ w)),
            "const": float(b[0])}


# ---------------------------------------------------------------------------------------------------------------
# bandits


def bandit_pricing(prices=(60.0, 80.0, 100.0, 120.0, 140.0, 160.0), mu: float = 70.0, horizon: int = 20000,
                   test: int = 1200, reps: int = 40, seed: int = 60) -> dict:
    """Customers arrive one at a time and buy at price p with probability exp(-p/mu).  Thompson sampling keeps a Beta
    posterior on each price's purchase rate and charges the price with the highest sampled revenue; test-then-commit
    spreads ``test`` customers evenly over the prices and then charges the best.  Average revenue per customer over
    time, and each rule's regret against always charging the best price."""
    rng = np.random.default_rng(seed)
    P = np.asarray(prices, float)
    q = np.exp(-P / mu)
    best = float((P * q).max())
    ts_curve, tc_curve = np.zeros(horizon), np.zeros(horizon)
    for _ in range(reps):
        a, b = np.ones(len(P)), np.ones(len(P))
        cum = 0.0
        for t in range(horizon):
            th = rng.beta(a, b)
            k = int(np.argmax(P * th))
            buy = rng.random() < q[k]
            a[k] += buy
            b[k] += 1 - buy
            cum += P[k] * buy
            ts_curve[t] += cum
        cum = 0.0
        sales = np.zeros(len(P))
        tries = np.zeros(len(P))
        choice = None
        for t in range(horizon):
            if t < test:
                k = t % len(P)
            else:
                if choice is None:
                    choice = int(np.argmax(P * sales / np.maximum(tries, 1)))
                k = choice
            buy = rng.random() < q[k]
            if t < test:
                sales[k] += buy
                tries[k] += 1
            cum += P[k] * buy
            tc_curve[t] += cum
    ts_curve /= reps
    tc_curve /= reps
    t = np.arange(1, horizon + 1)
    return {"prices": P.tolist(), "buy": q.tolist(), "best_price": float(P[np.argmax(P * q)]), "best": best,
            "ts_regret": (best * t - ts_curve).tolist(), "tc_regret": (best * t - tc_curve).tolist(),
            "ts_avg": float(ts_curve[-1] / horizon), "tc_avg": float(tc_curve[-1] / horizon)}


__all__ = [n for n in dir() if not n.startswith("_") and n not in ("np", "optimize", "stats", "annotations")]
