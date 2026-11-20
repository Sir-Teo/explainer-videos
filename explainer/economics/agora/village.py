"""Agora's development economics (Part 46): a village with a poverty trap, a dual economy, credit, cash, risk, and
the experiments that study them.

* **Poverty traps** (:func:`trap_next`, :func:`trap_threshold`, :func:`trap_households`): a household chooses between
  a low technology and a high one with a fixed cost; savings out of output give an S-shaped capital map with two
  stable steady states and a threshold between them; a one-off asset transfer works only for those it pushes across.
* **The dual economy** (:func:`lewis`): Lewis's surplus labour at a subsistence wage, a modern sector that reinvests
  its profits, and the turning point; :func:`agri_gap` the raw agricultural productivity gap from national accounts.
* **Credit** (:func:`moneylender`, :func:`microcredit_trial`): the lender's break-even rate with default risk and
  monitoring costs; a randomized expansion of credit to firms whose returns differ, with average and quantile
  effects.
* **Cash** (:func:`local_multiplier`): a transfer spent partly in the village, the rounds of local spending, and the
  multiplier, against prices that rise when local supply is tight.
* **Risk** (:func:`townsend`, :func:`index_insurance`): villages that pool risk fully or partly, and Townsend's test
  (own income's effect on consumption with the village's average held fixed); the demand for index insurance with
  basis risk and limited trust.
* **Health, schools, history** (:func:`net_demand`, :func:`deworming`, :func:`inpres`, :func:`geo_rd`,
  :func:`panes_rd`): the demand for a bed net by price, and who uses it; a treatment with spillovers
  randomized by school, where a within-school comparison misses the externality; Duflo's difference-in-differences
  on a school-building programme, and the Wald ratio; a historical boundary studied by regression discontinuity, and
  a local linear discontinuity for real data.
* **Behaviour on the farm** (:func:`fertilizer`): present-biased farmers who mean to buy fertilizer, and a small
  discount offered at harvest that works as commitment.
* **External validity** (:func:`sites`): effects that differ by site, and what one site's trial says about another.
* **The aid budget** (:func:`aid_allocate`): six programmes with diminishing returns, and the allocation that buys the
  most.

numpy and scipy only.
"""

from __future__ import annotations

import numpy as np
from scipy.optimize import brentq


# ---------------------------------------------------------------------------------------------------------------
# poverty traps


def trap_output(k, a_low: float = 1.0, a_high: float = 4.0, alpha: float = 0.5, fixed: float = 11.0):
    """Output with the better of two technologies: a_low k^alpha, or a_high k^alpha less a fixed cost."""
    k = np.asarray(k, float)
    return np.maximum(a_low * k ** alpha, a_high * k ** alpha - fixed)


def trap_next(k, s: float = 0.3, delta: float = 0.1, **tech):
    """Next year's capital: k' = s f(k) + (1 - delta) k."""
    return s * trap_output(k, **tech) + (1 - delta) * np.asarray(k, float)


def trap_steady_states(s: float = 0.3, delta: float = 0.1, kmax: float = 400.0, **tech) -> dict:
    """The fixed points of the capital map: the low steady state, the threshold between the basins, the high
    steady state (found as sign changes of k' - k)."""
    g = np.linspace(0.01, kmax, 200001)
    d = trap_next(g, s, delta, **tech) - g
    roots = []
    for i in np.where(np.sign(d[:-1]) != np.sign(d[1:]))[0]:
        roots.append(float(brentq(lambda x: float(trap_next(x, s, delta, **tech) - x), g[i], g[i + 1])))
    out = {"roots": roots}
    if len(roots) == 3:
        out.update(low=roots[0], threshold=roots[1], high=roots[2])
    return out


def trap_threshold(**kw) -> float:
    return trap_steady_states(**kw)["threshold"]


def trap_households(n: int = 3000, T: int = 12, transfer: float = 0.0, k_mu: float = np.log(10.0),
                    k_sd: float = 0.45, shock_sd: float = 0.08, s: float = 0.3, delta: float = 0.1,
                    seed: int = 0, **tech) -> dict:
    """Households start with assets lognormal around exp(k_mu), receive a one-off ``transfer``, and accumulate by
    the map with multiplicative shocks.  Returns the paths, the threshold, and the share above it at the end."""
    rng = np.random.default_rng(seed)
    k0 = np.exp(rng.normal(k_mu, k_sd, n))
    k = k0 + transfer
    paths = [k.copy()]
    for _ in range(T):
        k = trap_next(k, s, delta, **tech) * np.exp(shock_sd * rng.standard_normal(n) - shock_sd ** 2 / 2)
        paths.append(k.copy())
    th = trap_threshold(s=s, delta=delta, **tech)
    P = np.array(paths)
    return {"paths": P, "k0": k0, "threshold": th, "share_above_end": float(np.mean(P[-1] > th)),
            "crossed": (k0 + transfer) > th, "start_above": float(np.mean(k0 > th))}


# ---------------------------------------------------------------------------------------------------------------
# the dual economy


def lewis(T: int = 60, labour: float = 100.0, wage: float = 1.0, a: float = 1.0, alpha: float = 0.4,
          k0: float = 2.0, saving: float = 1.0, mpl_farm: float = 0.02) -> dict:
    """Lewis (1954): the modern sector produces a K^alpha L^(1-alpha) and hires at the subsistence wage while farms
    have surplus labour (their marginal product, mpl_farm per worker taken off the land, is below the wage); profits
    are reinvested at rate ``saving``.  Once the farm's surplus is gone the modern wage must rise with the farm's
    marginal product.  Returns employment, wages and the turning point."""
    K = k0
    emp, wages, cap = [], [], []
    turn = None
    for t in range(T):
        # labour demand at the subsistence wage: (1 - alpha) a (K/L)^alpha = w  ->  L = K ((1-alpha) a / w)^(1/alpha)
        L_dem = K * ((1 - alpha) * a / wage) ** (1 / alpha)
        surplus = labour * 0.6                      # workers whose farm marginal product is below the wage
        if L_dem <= surplus:
            L, w = L_dem, wage
        else:
            if turn is None:
                turn = t
            # beyond the surplus, each further worker taken from the farm raises the farm's marginal product
            def gap(Lx):
                w_farm = wage + mpl_farm * (Lx - surplus) ** 1.3
                return (1 - alpha) * a * (K / Lx) ** alpha - w_farm
            L = brentq(gap, surplus, labour - 1e-6) if gap(labour - 1e-6) < 0 else labour - 1e-6
            w = (1 - alpha) * a * (K / L) ** alpha
        Y = a * K ** alpha * L ** (1 - alpha)
        profit = Y - w * L
        emp.append(float(L))
        wages.append(float(w))
        cap.append(float(K))
        K = K + saving * profit
    return {"emp": emp, "wage": wages, "capital": cap, "turn": turn, "surplus": labour * 0.6, "labour": labour}


def agri_gap(rows) -> dict:
    """The raw agricultural productivity gap from national accounts: value added per worker outside agriculture
    over value added per worker in it, ((1 - va)/(1 - emp)) / (va / emp), with va and emp agriculture's shares."""
    out = {"code": [], "gap": [], "gdppc": [], "emp": [], "va": []}
    for r in rows:
        emp, va = r["agri_emp"] / 100, r["agri_va"] / 100
        if not (0.005 < emp < 0.99 and 0.002 < va < 0.99) or not np.isfinite(r["gdppc"]):
            continue
        out["code"].append(r["code"])
        out["gap"].append(float(((1 - va) / (1 - emp)) / (va / emp)))
        out["gdppc"].append(float(r["gdppc"]))
        out["emp"].append(float(emp))
        out["va"].append(float(va))
    g, y = np.array(out["gap"]), np.array(out["gdppc"])
    q = np.quantile(y, [0.25, 0.75])
    out["median_poorest"] = float(np.median(g[y <= q[0]]))
    out["median_richest"] = float(np.median(g[y >= q[1]]))
    out["median_all"] = float(np.median(g))
    return out


# ---------------------------------------------------------------------------------------------------------------
# credit


def moneylender(cost_of_funds: float = 0.10, default: float = 0.15, monitoring: float = 0.20) -> dict:
    """The rate at which a lender breaks even on a loan of 1: it must recover its cost of funds and the cost of
    screening and monitoring from the borrowers who repay: (1 + i)(1 - p) = 1 + r + m."""
    i = (1 + cost_of_funds + monitoring) / (1 - default) - 1
    return {"rate": float(i), "cost_of_funds": cost_of_funds, "default": default, "monitoring": monitoring,
            "from_default": float((1 + cost_of_funds) / (1 - default) - 1 - cost_of_funds),
            "from_monitoring": float(monitoring / (1 - default))}


def microcredit_trial(n: int = 6000, share_high: float = 0.15, r_low: float = 0.05, r_high: float = 0.6,
                      loan: float = 100.0, take_up: float = 0.2, interest: float = 0.25, base_sd: float = 60.0,
                      seed: int = 0) -> dict:
    """Villages randomized to get a microlender.  Most would-be borrowers' businesses return little on extra capital
    (r_low a year), a few a great deal (r_high).  Those offered credit whose return beats the interest rate borrow
    and invest; some others (``take_up``) borrow anyway, to buy a durable good or smooth a bad month, which leaves
    their profits unchanged.  Returns the intention-to-treat effect on profits, the take-up, the effect on
    borrowers, and quantile treatment effects (the gains sit in the top tail)."""
    rng = np.random.default_rng(seed)
    high = rng.random(n) < share_high
    r = np.where(high, r_high, r_low) + 0.02 * rng.standard_normal(n)
    treat = rng.random(n) < 0.5
    invest = treat & (r > interest)
    other = treat & ~invest & (rng.random(n) < take_up)
    borrow = invest | other
    base = 200 + base_sd * rng.standard_normal(n) + 120 * high
    profit = base + invest * loan * (r - interest)
    itt = float(profit[treat].mean() - profit[~treat].mean())
    tu = float(borrow[treat].mean())
    qs = np.linspace(0.05, 0.95, 19)
    qte = np.quantile(profit[treat], qs) - np.quantile(profit[~treat], qs)
    return {"itt": itt, "take_up": tu, "tot": itt / tu, "qs": qs.tolist(), "qte": qte.tolist(),
            "mean_control": float(profit[~treat].mean()), "share_high": share_high,
            "gain_high": float(loan * (r_high - interest)), "share_investing": float(invest[treat].mean())}


# ---------------------------------------------------------------------------------------------------------------
# cash and the local economy


def local_multiplier(transfer: float = 1.0, local_share: float = 0.75, mpc: float = 0.8, slack: float = 0.98,
                     rounds: int = 30) -> dict:
    """A transfer is spent; a share ``local_share`` of each round's spending reaches local sellers, who spend
    ``mpc`` of what they receive, and so on.  Where local supply is tight, part of the extra demand raises prices
    instead of quantities: a share ``slack`` of each round is real.  Returns the rounds and the real and nominal
    multipliers."""
    spend = transfer
    nominal, real = [transfer], [transfer]
    for _ in range(rounds):
        spend = spend * local_share * mpc
        nominal.append(spend)
        real.append(spend * slack)
    m_nom = float(1 + np.sum(nominal[1:]) / transfer)
    m_real = float(1 + np.sum(real[1:]) / transfer)
    closed = 1 / (1 - local_share * mpc)
    return {"rounds": nominal, "real_rounds": real, "multiplier": m_nom, "real_multiplier": m_real,
            "closed_form": float(closed), "local_share": local_share, "mpc": mpc}


# ---------------------------------------------------------------------------------------------------------------
# risk


def townsend(villages: int = 3, households: int = 120, T: int = 10, pooled: float = 0.85, sd_village: float = 0.15,
             sd_own: float = 0.35, seed: int = 0) -> dict:
    """Households' log income = village shock + own shock.  A share ``pooled`` of own shocks is shared within the
    village, so log consumption = village mean income + (1 - pooled) own deviation.  Townsend's test regresses the
    change in log consumption on the change in own log income with village-year effects: 0 under full insurance,
    1 under none; and the raw regression without the village effects."""
    rng = np.random.default_rng(seed)
    rows_dc, rows_dy, rows_vt = [], [], []
    vt = 0
    for _v in range(villages):
        prev_c = prev_y = None
        for _t in range(T):
            v_shock = sd_village * rng.standard_normal()
            own = sd_own * rng.standard_normal(households)
            y = v_shock + own
            c = v_shock + (1 - pooled) * (own - own.mean())
            if prev_c is not None:
                rows_dc.append(c - prev_c)
                rows_dy.append(y - prev_y)
                rows_vt.append(np.full(households, vt))
                vt += 1
            prev_c, prev_y = c, y
    dc, dy, g = np.concatenate(rows_dc), np.concatenate(rows_dy), np.concatenate(rows_vt)
    # within village-year: demean both
    dcw, dyw = dc.copy(), dy.copy()
    for k in np.unique(g):
        s = g == k
        dcw[s] -= dc[s].mean()
        dyw[s] -= dy[s].mean()
    b_within = float(np.sum(dcw * dyw) / np.sum(dyw * dyw))
    b_raw = float(np.polyfit(dy, dc, 1)[0])
    return {"within": b_within, "raw": b_raw, "pooled": pooled, "n": int(len(dc))}


def index_insurance(basis: float = 0.3, trust: float = 0.8, load: float = 0.3, gamma: float = 2.0,
                    p_drought: float = 0.2, loss: float = 0.5, n: int = 4001) -> dict:
    """A farmer loses ``loss`` of income in a drought (probability p_drought).  Index insurance pays when the rain
    gauge says drought; with probability ``basis`` the gauge disagrees with the farm.  The farmer believes the
    insurer will pay with probability ``trust``.  Premium = (1 + load) times the expected payout.  Returns the
    CRRA farmer's best cover, from 0 to 1 of the loss."""
    covers = np.linspace(0, 1, n)
    prem = (1 + load) * p_drought * covers * loss
    # states: (drought on farm, gauge says drought)
    states = [((1, 1), p_drought * (1 - basis)), ((1, 0), p_drought * basis),
              ((0, 1), (1 - p_drought) * basis * p_drought / (1 - p_drought) if p_drought < 1 else 0.0),
              ((0, 0), None)]
    pr = [p for _, p in states[:3]]
    states[3] = ((0, 0), 1 - sum(pr))

    def u(c):
        c = np.maximum(c, 1e-6)
        return np.log(c) if gamma == 1 else c ** (1 - gamma) / (1 - gamma)
    eu = np.zeros(n)
    for (farm, gauge), p in states:
        inc = 1 - loss * farm - prem
        if gauge:
            eu += p * (trust * u(inc + covers * loss) + (1 - trust) * u(inc))
        else:
            eu += p * u(inc)
    best = float(covers[int(np.argmax(eu))])
    return {"cover": best, "basis": basis, "trust": trust, "load": load}


# ---------------------------------------------------------------------------------------------------------------
# health, schools, history


def deworming(schools: int = 75, pupils: int = 200, share_treated: float = 0.5, take: float = 0.75,
              base_infect: float = 0.5, cure: float = 0.9, spill: float = 0.5, absence_if_infected: float = 0.25,
              absence_base: float = 0.15, seed: int = 0) -> dict:
    """Schools randomized to mass deworming.  In treated schools a share ``take`` of pupils are treated and cured;
    infection among the rest falls with the share cured in their school (``spill``).  Absence is higher when
    infected.  Returns the within-school comparison of treated and untreated pupils in treatment schools (which
    misses the spillover) and the school-level comparison of treatment and control schools (which captures it)."""
    rng = np.random.default_rng(seed)
    t_school = rng.random(schools) < share_treated
    rows = []
    for s in range(schools):
        treated = (rng.random(pupils) < take) if t_school[s] else np.zeros(pupils, bool)
        cured_share = take * cure if t_school[s] else 0.0
        p_inf_untreated = base_infect * (1 - spill * cured_share)
        p_inf = np.where(treated, base_infect * (1 - cure), p_inf_untreated)
        inf = rng.random(pupils) < p_inf
        absent = absence_base + absence_if_infected * inf + 0.05 * rng.standard_normal(pupils)
        rows.append((t_school[s], treated, absent))
    within = np.mean([a[tr].mean() - a[~tr].mean() for ts, tr, a in rows if ts])
    school_t = np.mean([a.mean() for ts, tr, a in rows if ts])
    school_c = np.mean([a.mean() for ts, tr, a in rows if not ts])
    untreated_in_t = np.mean([a[~tr].mean() for ts, tr, a in rows if ts])
    return {"within": float(within), "between_schools": float(school_t - school_c),
            "spillover": float(untreated_in_t - school_c), "absence_control": float(school_c)}


def inpres(regions: int = 280, per_cell: int = 800, schools_mean: float = 2.0, effect_years: float = 0.15,
           return_school: float = 0.08, seed: int = 0) -> dict:
    """A school-building programme: regions receive different numbers of new schools per 1,000 children; children
    young enough to attend get more schooling where more schools were built, older cohorts do not.  The
    difference-in-differences on years of school and on log wages, and their ratio (the Wald estimate of the
    return to schooling)."""
    rng = np.random.default_rng(seed)
    intensity = np.maximum(rng.normal(schools_mean, 0.9, regions), 0.0)
    region_fe = rng.normal(0, 0.3, regions)
    rows = []
    for r in range(regions):
        for young in (0, 1):
            ability = rng.normal(0, 1, per_cell)
            school = 6 + 1.2 * ability + region_fe[r] * 3 + young * (0.6 + effect_years * intensity[r]) + \
                rng.normal(0, 1.5, per_cell)
            lw = 1.0 + return_school * school + 0.05 * ability + region_fe[r] + 0.1 * young + \
                rng.normal(0, 0.4, per_cell)
            rows.append((intensity[r], young, school.mean(), lw.mean()))
    a = np.array(rows)
    # regress cell means on intensity x young with region and cohort effects: do it by first differences per region
    I = a[0::2, 0]
    ds = a[1::2, 2] - a[0::2, 2]
    dw = a[1::2, 3] - a[0::2, 3]
    bs = float(np.polyfit(I, ds, 1)[0])
    bw = float(np.polyfit(I, dw, 1)[0])
    return {"school_per_school": bs, "wage_per_school": bw, "wald": bw / bs, "truth": return_school,
            "intensity": I.tolist(), "dschool": ds.tolist(), "dwage": dw.tolist()}


def geo_rd(n: int = 3000, effect: float = -0.25, slope: float = 0.004, bandwidth: float = 50.0,
           seed: int = 0) -> dict:
    """Districts on either side of a historical boundary (distance in km, negative inside).  Log consumption
    changes smoothly with distance and jumps at the boundary by ``effect``.  Local linear fits within the bandwidth
    on each side; the jump between them."""
    rng = np.random.default_rng(seed)
    d = rng.uniform(-150, 150, n)
    y = 5.0 + slope * d + effect * (d < 0) + 0.25 * rng.standard_normal(n)
    sel_in = (d < 0) & (d > -bandwidth)
    sel_out = (d >= 0) & (d < bandwidth)
    bi = np.polyfit(d[sel_in], y[sel_in], 1)
    bo = np.polyfit(d[sel_out], y[sel_out], 1)
    jump = float(np.polyval(bi, 0) - np.polyval(bo, 0))
    edges = np.arange(-150, 151, 10)
    mids, means = [], []
    for lo, hi in zip(edges[:-1], edges[1:]):
        s = (d >= lo) & (d < hi)
        mids.append(float((lo + hi) / 2))
        means.append(float(y[s].mean()))
    return {"jump": jump, "effect": effect, "mids": mids, "means": means, "fit_in": bi.tolist(),
            "fit_out": bo.tolist(), "bandwidth": bandwidth}


def panes_rd(score, outcome, bandwidth: float | None = None) -> dict:
    """A local linear regression discontinuity at zero (eligible below): the jump in the outcome at the cutoff,
    eligible minus ineligible, with a heteroskedasticity-robust standard error from the two separate fits."""
    x, y = np.asarray(score, float), np.asarray(outcome, float)
    ok = np.isfinite(x) & np.isfinite(y)
    x, y = x[ok], y[ok]
    h = bandwidth if bandwidth is not None else float(np.max(np.abs(x)))
    res = {}
    for side, s in (("in", (x < 0) & (x > -h)), ("out", (x >= 0) & (x < h))):
        X = np.column_stack([np.ones(s.sum()), x[s]])
        b, *_ = np.linalg.lstsq(X, y[s], rcond=None)
        e = y[s] - X @ b
        XtX = np.linalg.inv(X.T @ X)
        V = XtX @ (X.T * e ** 2) @ X @ XtX
        res[side] = (b, V)
    jump = float(res["in"][0][0] - res["out"][0][0])
    se = float(np.sqrt(res["in"][1][0, 0] + res["out"][1][0, 0]))
    return {"jump": jump, "se": se, "bandwidth": h, "n": int(len(x))}


def net_demand(prices=(0.0, 0.15, 0.22, 0.3, 0.6), n: int = 20000, wtp_median: float = 0.42, wtp_sigma: float = 1.2,
               zero_share: float = 0.05, use: float = 0.65, use_slope: float = 0.0, seed: int = 0) -> dict:
    """Demand for a bed net at a clinic.  Willingness to pay is lognormal (most households are cash-poor; a share
    ``zero_share`` would not take one even free); a household that has a net uses it with probability ``use`` plus
    ``use_slope`` times its willingness to pay (0: paying screens nobody, as Cohen and Dupas found).  For each
    price: the share who take a net, the share of those who use it, the share of all households protected, and the
    subsidy cost per household protected if a net costs 6."""
    rng = np.random.default_rng(seed)
    wtp = wtp_median * np.exp(wtp_sigma * rng.standard_normal(n))
    wtp[rng.random(n) < zero_share] = -1.0
    p_use = np.clip(use + use_slope * (wtp - wtp_median), 0, 1)
    uses = rng.random(n) < p_use
    out = {"price": [], "take": [], "use_if_taken": [], "protected": [], "cost_per_protected": []}
    for p in prices:
        take = wtp >= p
        prot = take & uses
        out["price"].append(float(p))
        out["take"].append(float(take.mean()))
        out["use_if_taken"].append(float(prot.sum() / max(take.sum(), 1)))
        out["protected"].append(float(prot.mean()))
        out["cost_per_protected"].append(float((6.0 - p) * take.sum() / max(prot.sum(), 1)))
    return out


# ---------------------------------------------------------------------------------------------------------------
# behaviour on the farm, external validity


def fertilizer(n: int = 20000, value_mean: float = 1.1, value_sd: float = 0.5, cost: float = 1.0,
               hassle_mean: float = 0.15, cash_cost: float = 0.35, beta_lo: float = 0.7, beta_hi: float = 1.0,
               naive: float = 0.7, discount: float = 0.0, seed: int = 0) -> dict:
    """Duflo, Kremer and Robinson's farmers.  Fertilizer bought for next season costs ``cost``, returns a value v
    (lognormal, mean value_mean) at the following harvest, and takes a trip to buy (a hassle h, felt when it is
    made).  At harvest the farmer has cash; buying later, just before planting, costs ``cash_cost`` more because the
    cash has gone.  Seen from harvest, buying now gives -h - c + beta v; buying later, beta (v - h - c - x).  A
    share ``naive`` of the present-biased farmers expect to be patient later and so put the purchase off; when
    later comes they buy only if -h - c - x + beta v >= 0.  Sophisticates know they will procrastinate.

    Four arms: no offer; at harvest, free delivery at the regular price (the commitment offer, with an optional
    ``discount``); the same free delivery offered only just before planting; a 50% subsidy just before planting.
    Returns the adoption rate in each, and the shares of procrastinators."""
    rng = np.random.default_rng(seed)
    sig = np.sqrt(np.log(1 + (value_sd / value_mean) ** 2))
    v = value_mean * np.exp(sig * rng.standard_normal(n) - sig ** 2 / 2)
    h = rng.exponential(hassle_mean, n)
    beta = rng.uniform(beta_lo, beta_hi, n)
    is_naif = rng.random(n) < naive
    c, x = cost, cash_cost

    def run(c_now, h_now, c_later, h_later):
        later_buys = (-h_later - c_later - x + beta * v) >= 0              # what the later self actually does
        # what the harvest self expects of the later self: naifs expect patience, sophisticates the truth
        expect_later = np.where(is_naif, (v - h_later - c_later - x) >= 0, later_buys)
        value_later = beta * np.where(expect_later, v - h_later - c_later - x, 0.0)
        now = (-h_now - c_now + beta * v) >= np.maximum(value_later, 0.0)
        return now | (~now & later_buys), now

    base, now0 = run(c, h, c, h)
    offer, _ = run(c * (1 - discount), 0.0 * h, c, h)
    late, _ = run(c, h, c, 0.0 * h)                    # the same free delivery, offered only before planting
    planting, _ = run(c, h, 0.5 * c, h)
    # procrastinators: those who would buy if patient but under no offer do not
    patient = (v - c - np.minimum(h, h + x)) >= 0
    return {"base": float(base.mean()), "harvest_offer": float(offer.mean()), "late_offer": float(late.mean()),
            "planting_subsidy": float(planting.mean()),
            "patient_would": float(patient.mean()), "procrastinate": float(np.mean(patient & ~base))}


def sites(k: int = 12, mu: float = 0.2, tau: float = 0.15, se: float = 0.05, seed: int = 0) -> dict:
    """k sites with true effects normal(mu, tau); each trial estimates its site's effect with error se.  The
    spread of the estimates, the partial pooling of each toward the mean (the shrinkage of Part 26 of Statistics,
    Built), and the interval for the next site's effect, which reflects tau, not se."""
    rng = np.random.default_rng(seed)
    theta = mu + tau * rng.standard_normal(k)
    x = theta + se * rng.standard_normal(k)
    tau2 = max(np.var(x, ddof=1) - se ** 2, 0.0)
    w = tau2 / (tau2 + se ** 2)
    pooled = float(np.mean(x))
    shrunk = pooled + w * (x - pooled)
    pred_sd = float(np.sqrt(tau2 + np.var(x, ddof=1) / k))
    return {"theta": theta.tolist(), "x": x.tolist(), "shrunk": shrunk.tolist(), "mean": pooled,
            "tau_hat": float(np.sqrt(tau2)), "next_lo": pooled - 1.96 * pred_sd, "next_hi": pooled + 1.96 * pred_sd,
            "se": se}


# ---------------------------------------------------------------------------------------------------------------
# the aid budget


def aid_benefit(spend, scale: float, saturation: float):
    """Benefit of spending ``spend`` (millions) on a programme: scale (1 - exp(-spend / saturation)) saturation,
    so the first million buys ``scale`` units and returns diminish."""
    spend = np.asarray(spend, float)
    return scale * saturation * (1 - np.exp(-spend / saturation))


def aid_allocate(programmes: dict, budget: float = 10.0, step: float = 0.1) -> dict:
    """Spend the budget in small steps, each on the programme with the largest marginal benefit: the allocation
    that maximizes the total when returns diminish."""
    alloc = {k: 0.0 for k in programmes}
    for _ in range(int(round(budget / step))):
        best = max(programmes, key=lambda k: float(aid_benefit(alloc[k] + step, *programmes[k])
                                                   - aid_benefit(alloc[k], *programmes[k])))
        alloc[best] += step
    total = float(sum(aid_benefit(alloc[k], *programmes[k]) for k in programmes))
    return {"alloc": {k: round(v, 6) for k, v in alloc.items()}, "total": total}
