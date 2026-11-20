"""Agora's behavioural economics (Part 45): agents who are not the agents of Part 5, and what markets do with them.

* **The gym** (:func:`gym_member`, :func:`gym_choice`, :func:`gym_contract`, :func:`island_gym`): present-biased
  members who go when today's cost is below the discounted future benefit, forecast their visits with a belief
  ``beta_hat`` about their own present bias, and choose a monthly fee or a pay-per-visit pass by the forecast; the
  contract a firm designs for them (DellaVigna and Malmendier 2004, 2006).
* **Reference dependence** (:func:`mug_market`, :func:`experienced_traders`, :func:`marathon`, :func:`golf`,
  :func:`condos`): an endowment-effect market whose volume falls short of the Coase prediction; traders whose loss
  aversion fades with experience; runners who bunch at round finishing times (a kink, measured as Part 41 measured
  taxpayers'); putts for par and for birdie; loss-averse sellers whose asking prices rise with the nominal loss.
* **Present bias** (:func:`odr`, :func:`commitment_trial`, :func:`enrolment`, :func:`smart`): O'Donoghue and
  Rabin's naifs and sophisticates; a randomized offer of a commitment savings account; defaults that stick because
  switching is put off; saving more tomorrow.
* **Inattention** (:func:`shrouded`, :func:`used_cars`, :func:`ri_choice`, :func:`sparse_weights`): shrouded
  add-on prices; left-digit bias in mileage and the estimator that recovers it; rational inattention by the
  Blahut-Arimoto iteration; sparse attention by soft thresholding.
* **Social preferences** (:func:`fehr_schmidt`, :func:`ultimatum`, :func:`gift_exchange`).
* **Evidence** (:func:`nudge_literature`, :func:`selection_mle`): a literature of nudge trials filtered by
  significance, and the step-function selection model (Andrews and Kasy 2019) that corrects it.
* **Expectations** (:func:`forecasters`): noisy-information forecasters, rational or diagnostic, and the
  forecast-error-on-revision regressions at the individual and the consensus level.
* **Welfare** (:func:`welfare_range`): the range of money-metric gains consistent with choices made in different
  frames (Bernheim and Rangel 2009).

Prospect theory's value and weighting functions are *Psychology, Built*'s (``explainer.psychology.psyche.choice``).
numpy and scipy only.
"""

from __future__ import annotations

import numpy as np
from scipy.optimize import minimize, minimize_scalar
from scipy.stats import norm

from explainer.psychology.psyche import choice as _pchoice

pt_value = _pchoice.value          # Kahneman and Tversky's value function (alpha, beta, lambda)
pt_weight = _pchoice.w_tk          # their probability weighting function


# ---------------------------------------------------------------------------------------------------------------
# the gym


def gym_member(beta: float, beta_hat: float, b: float, C: float, N: int = 30, p: float = 0.0, busy: float = 0.0,
               busy_hat: float | None = None) -> dict:
    """One member, one month.  On a share ``busy`` of the N days the member cannot go at all; on the others the cost
    of going, c, is uniform on [0, C] and paid today, and the health benefit b comes later.  The member goes when
    c + p <= beta b (p the price of a visit).  At sign-up the member forecasts with beta_hat and busy_hat (a naive
    member believes beta_hat = 1 and forgets the busy days) and values a visit by its long-run worth b - c - p:
    both cost and benefit are then in the future, so present bias enters the forecast of what the member will do,
    not the valuation."""
    busy_hat = busy if busy_hat is None else busy_hat
    x_true = float(np.clip(beta * b - p, 0, C))
    x_hat = float(np.clip(beta_hat * b - p, 0, C))
    visits = N * (1 - busy) * x_true / C
    forecast = N * (1 - busy_hat) * x_hat / C

    def value(x, free):
        # the long-run value of going whenever c <= x, on the days that are free: N free / C int_0^x (b - p - c) dc
        return N * (1 - free) / C * ((b - p) * x - x * x / 2)
    return {"visits": visits, "forecast": forecast, "perceived": value(x_hat, busy_hat),
            "realized": value(x_true, busy)}


def gym_choice(beta: float, beta_hat: float, b: float, C: float, N: int = 30, fee: float = 70.0,
               per_visit: float = 10.0, busy: float = 0.0, busy_hat: float | None = None) -> dict:
    """A member's choice among a monthly contract (fee, free visits), a pass at ``per_visit`` a visit, and staying
    home, made by the forecast surplus; and what then happens."""
    m = gym_member(beta, beta_hat, b, C, N, 0.0, busy, busy_hat)
    q = gym_member(beta, beta_hat, b, C, N, per_visit, busy, busy_hat)
    perceived = {"monthly": m["perceived"] - fee, "pass": q["perceived"], "none": 0.0}
    pick = max(perceived, key=perceived.get)
    r = {"monthly": m, "pass": q}.get(pick)
    visits = r["visits"] if r else 0.0
    paid = fee if pick == "monthly" else (per_visit * visits if pick == "pass" else 0.0)
    realized = {"monthly": m["realized"] - fee, "pass": q["realized"], "none": 0.0}
    best = max(realized, key=realized.get)
    return {"choice": pick, "visits": visits, "forecast": r["forecast"] if r else 0.0, "paid": paid,
            "per_visit_paid": paid / visits if visits > 0 else float("nan"), "perceived": perceived,
            "realized": realized, "best": best, "regret": realized[best] - realized[pick]}


def gym_contract(beta: float, beta_hat: float, b: float, C: float, N: int = 30, m: float = 2.0,
                 competitive: bool = False) -> dict:
    """The two-part tariff (fee F, price per visit p) a firm with marginal cost m per visit offers a member of type
    (beta, beta_hat).  A monopolist sets F to the member's perceived surplus and chooses p to maximize
    F + (p - m) visits; under free entry F just covers the per-visit losses and p maximizes the member's perceived
    net surplus.  The two problems have the same first-order condition, and with uniform costs its solution is
    p = m - (1 - beta) b, below marginal cost for any beta < 1, whatever the member believes (DellaVigna and
    Malmendier 2004); beliefs move the fee."""
    def parts(p):
        r = gym_member(beta, beta_hat, b, C, N, p)
        return r, (p - m) * r["visits"]

    def objective(p):
        r, margin = parts(p)
        return -(r["perceived"] + margin)
    res = minimize_scalar(objective, bounds=(m - b, m + b), method="bounded", options={"xatol": 1e-10})
    p = float(res.x)
    r, margin = parts(p)
    F = -margin if competitive else r["perceived"]
    profit = F + margin
    return {"p": p, "F": float(F), "profit": float(profit), "visits": r["visits"], "forecast": r["forecast"],
            "realized_surplus": r["realized"] - F, "perceived_surplus": r["perceived"] - F,
            "p_formula": m - (1 - beta) * b}


def island_gym(n: int = 4000, fee: float = 70.0, per_visit: float = 10.0, N: int = 30, C: float = 60.0,
               b_mean: float = 24.0, b_sd: float = 0.35, beta_lo: float = 0.5, beta_hi: float = 0.95,
               naive_share: float = 0.85, busy: float = 0.55, seed: int = 0) -> dict:
    """A town of would-be members: benefits b lognormal around ``b_mean``, present bias beta uniform on
    [beta_lo, beta_hi], a share of them naive (beta_hat = 1, and forgetful of the busy days), the rest
    sophisticated.  Each picks a contract by forecast; returns the members' visits, forecasts and the price they
    pay per visit."""
    rng = np.random.default_rng(seed)
    b = b_mean * np.exp(b_sd * rng.standard_normal(n) - b_sd ** 2 / 2)
    beta = rng.uniform(beta_lo, beta_hi, n)
    naive = rng.random(n) < naive_share
    beta_hat = np.where(naive, 1.0, beta)
    rows = [gym_choice(beta[i], beta_hat[i], b[i], C, N, fee, per_visit, busy, 0.0 if naive[i] else busy)
            for i in range(n)]
    choice = np.array([r["choice"] for r in rows])
    visits = np.array([r["visits"] for r in rows])
    forecast = np.array([r["forecast"] for r in rows])
    mon = choice == "monthly"
    out = {"choice": choice.tolist(), "visits": visits.tolist(), "forecast": forecast.tolist(),
           "beta": beta.tolist(), "naive": naive.tolist(), "b": b.tolist(),
           "share": {k: float(np.mean(choice == k)) for k in ("monthly", "pass", "none")},
           "monthly_visits": float(visits[mon].mean()) if mon.any() else float("nan"),
           "monthly_forecast": float(forecast[mon].mean()) if mon.any() else float("nan"),
           "monthly_naive_share": float(naive[mon].mean()) if mon.any() else float("nan"),
           "regret_share": float(np.mean([r["regret"] > 1e-9 for r, c in zip(rows, choice) if c == "monthly"]))
           if mon.any() else float("nan")}
    out["price_per_visit"] = fee / out["monthly_visits"]
    out["fee"], out["per_visit"] = fee, per_visit
    return out


# ---------------------------------------------------------------------------------------------------------------
# reference dependence


def mug_market(n: int = 44, lam_goods: float = 2.0, lam_money: float = 1.0, mu: float = np.log(4.0),
               sigma: float = 0.5, reps: int = 2000, seed: int = 0) -> dict:
    """Half of n subjects are given a mug at random.  Each values a mug at v (lognormal); an owner who sells codes
    the mug as a loss, so asks lam_goods v; a buyer who pays codes the money as a loss only if lam_money > 1, so
    bids v / lam_money.  The market clears where the ordered asks and bids cross.  Without loss aversion, the
    mugs end with those who value them most, so about half of them change hands; returns the average share
    traded and the median ask and bid across ``reps`` sessions."""
    rng = np.random.default_rng(seed)
    k = n // 2
    traded, asks, bids, ratio = [], [], [], []
    for _ in range(reps):
        v = np.exp(rng.normal(mu, sigma, n))
        ask = np.sort(lam_goods * v[:k])
        bid = np.sort(v[k:2 * k] / lam_money)[::-1]
        traded.append(np.sum(bid > ask) / k)
        asks.append(np.median(ask))
        bids.append(np.median(bid))
        ratio.append(np.median(ask) / np.median(bid))
    return {"share_traded": float(np.mean(traded)), "median_ask": float(np.mean(asks)),
            "median_bid": float(np.mean(bids)), "ratio": float(np.mean(ratio)), "lam_goods": lam_goods,
            "n": n}


def experienced_traders(trades=(0, 1, 3, 6, 12, 25, 50), lam0: float = 2.0, half_life: float = 5.0,
                        n: int = 60, reps: int = 1500, seed: int = 1) -> dict:
    """The Island's assumption: a trader's loss aversion over goods meant for exchange fades with the number of
    trades made, lam = 1 + (lam0 - 1) 2^(-trades / half_life).  Returns the share of goods traded at each level of
    experience, against the half predicted without loss aversion."""
    out = []
    for t in trades:
        lam = 1 + (lam0 - 1) * 2 ** (-t / half_life)
        out.append(mug_market(n=n, lam_goods=lam, reps=reps, seed=seed + int(t))["share_traded"])
    return {"trades": list(trades), "share_traded": out,
            "lam": [1 + (lam0 - 1) * 2 ** (-t / half_life) for t in trades]}


def marathon(n: int = 400_000, mu: float = np.log(270.0), sigma: float = 0.17, k: float = 1.0,
             eta: float = 2.0, lam: float = 2.25, eta_hour: float = 1.0, base: float = 1.0, friction: float = 0.3,
             lo: float = 150.0, hi: float = 390.0, seed: int = 0) -> dict:
    """Runners' natural finishing times T0 (minutes, lognormal).  Effort e costs e^2 / (2 k); a minute faster is
    worth ``base``, plus gain-loss utility around a goal: eta per minute below it, eta lam per minute above it (an
    hour mark counts ``eta_hour`` times as much as a half-hour mark).  Each runner's goal is the fastest round time
    reachable with the effort a loss calls for.  Effort is then k (base + eta) if the goal is met easily, k (base +
    eta lam) if not; runners for whom the goal lies between the two finish exactly on it: a kink, like a tax
    schedule's, with bunching on round numbers and a gap just over them.  Each finish then gets a little noise
    (``friction`` minutes).  Returns the times and their one-minute histogram."""
    rng = np.random.default_rng(seed)
    T0 = np.exp(rng.normal(mu, sigma, n))
    e_gain_half, e_loss_half = k * (base + eta), k * (base + eta * lam)
    e_gain_hour, e_loss_hour = k * (base + eta * eta_hour), k * (base + eta * eta_hour * lam)
    R_half = np.ceil((T0 - e_loss_half) / 30.0) * 30.0
    R_hour = np.ceil((T0 - e_loss_hour) / 60.0) * 60.0
    hour = R_hour <= R_half
    R = np.where(hour, R_hour, R_half)
    e_gain = np.where(hour, e_gain_hour, e_gain_half)
    T_gain = T0 - e_gain
    goal = R - 0.25                          # to break four hours is to finish under 4:00:00
    T = np.minimum(T_gain, goal)             # beat the goal comfortably, or just make it
    bunched = float(np.mean(T_gain > goal))
    T = T + friction * rng.standard_normal(n)
    edges = np.arange(lo, hi + 1.0, 1.0)
    h, _ = np.histogram(T, bins=edges)
    return {"T": T, "edges": edges.tolist(), "h": h.tolist(), "share_bunched": bunched,
            "extra_minutes": float(e_loss_half - e_gain_half), "extra_minutes_hour": float(e_loss_hour - e_gain_hour),
            "k": k, "eta": eta, "lam": lam}


def bunching_at(times, mark: float, below: float = 4.0, above: float = 8.0, split: float = 0.0, span: float = 25.0,
                degree: int = 5, bin_w: float = 1.0) -> dict:
    """Saez's excess-mass estimator (Part 41) at a round time: fit a polynomial to the histogram within ``span``
    minutes of the mark, leaving out the window from ``below`` minutes under it to ``above`` minutes over it; the
    excess mass from the window's start to ``split`` minutes past the mark (the spike) and the missing mass from
    there to the window's end (the gap), both in minutes of the counterfactual density."""
    t = np.asarray(times, float)
    edges = np.arange(mark - span, mark + span + bin_w / 2, bin_w)
    h, _ = np.histogram(t, bins=edges)
    mid = (edges[:-1] + edges[1:]) / 2
    out = (mid < mark - below) | (mid > mark + above)
    x = (mid - mark) / span
    coef = np.polyfit(x[out], h[out], degree)
    cf = np.polyval(coef, x)
    spike = (~out) & (mid < mark + split)
    gap = (~out) & (mid >= mark + split)
    h0 = float(np.polyval(coef, 0.0))
    return {"mid": mid.tolist(), "h": h.tolist(), "cf": cf.tolist(),
            "excess": float(np.sum(h[spike] - cf[spike]) / h0 * bin_w),
            "missing": float(np.sum(cf[gap] - h[gap]) / h0 * bin_w)}


def golf(n: int = 200_000, effect: float = 0.025, seed: int = 0) -> dict:
    """Putts for birdie and for par.  Success falls with distance (logit in log feet); birdie putts are longer on
    average (they follow an approach shot, par putts a missed birdie or a chip).  A par putt, a putt to avoid a
    loss, gets extra care that adds ``effect`` to its chance.  The raw gap in success mixes the effect with distance;
    comparing putts of the same length recovers it."""
    rng = np.random.default_rng(seed)
    par = rng.random(n) < 0.5
    feet = np.where(par, rng.gamma(2.2, 4.0, n), rng.gamma(2.6, 6.0, n)) + 1.0
    base = 1 / (1 + np.exp(-(4.2 - 1.75 * np.log(feet))))
    p = np.clip(base + effect * par, 0, 1)
    made = rng.random(n) < p
    raw = float(made[par].mean() - made[~par].mean())
    bins = np.arange(1, 41, 1.0)
    diffs, weights = [], []
    for lo_, hi_ in zip(bins[:-1], bins[1:]):
        s = (feet >= lo_) & (feet < hi_)
        a, b_ = s & par, s & ~par
        if a.sum() > 200 and b_.sum() > 200:
            diffs.append(made[a].mean() - made[b_].mean())
            weights.append(s.sum())
    within = float(np.average(diffs, weights=weights))
    curve = {"feet": [], "par": [], "birdie": []}
    for lo_, hi_ in zip(bins[:-1:2], bins[2::2]):
        s = (feet >= lo_) & (feet < hi_)
        if (s & par).sum() > 200 and (s & ~par).sum() > 200:
            curve["feet"].append(float((lo_ + hi_) / 2))
            curve["par"].append(float(made[s & par].mean()))
            curve["birdie"].append(float(made[s & ~par].mean()))
    return {"raw": raw, "within": within, "effect": effect, "mean_feet_par": float(feet[par].mean()),
            "mean_feet_birdie": float(feet[~par].mean()), "curve": curve, "n": n}


def condos(n: int = 6000, m: float = 0.3, sd_u: float = 0.15, sd_e: float = 0.12, sd_w: float = 0.04,
           h0: float = 0.10, kappa: float = 8.0, seed: int = 0) -> dict:
    """A condominium market after a fall in prices (logs).  Owners bought in different years at the market index
    I0 (some at the peak), paying their unit's value plus luck e0; unit value is observed quality X g plus quality
    u the econometrician cannot see.  Now the index is I1; a loss-averse owner asks the unit's value plus m times
    the nominal loss, L = max(P0 - V1, 0).  The econometrician estimates the loss from a hedonic value that misses
    u, which biases the coefficient on the loss up; adding the residual of the purchase price as a control biases
    it down: the two regressions bracket m (Genesove and Mayer's two bounds).  Higher asking markups sell more
    slowly: weekly sale hazard h0 exp(-kappa markup)."""
    rng = np.random.default_rng(seed)
    years = rng.integers(0, 8, n)
    index = np.array([0.0, 0.08, 0.17, 0.28, 0.35, 0.30, 0.18, 0.08])   # rise to a peak in year 4, then a fall
    I0 = index[years]
    I1 = 0.0
    X = rng.normal(0, 1, (n, 2))
    g = np.array([0.20, 0.10])
    u = sd_u * rng.standard_normal(n)
    e0 = sd_e * rng.standard_normal(n)
    P0 = I0 + X @ g + u + e0
    V1 = I1 + X @ g + u
    L = np.maximum(P0 - V1, 0.0)
    LP = V1 + m * L + sd_w * rng.standard_normal(n)
    # the econometrician: the hedonic regression of purchase prices on X and year effects
    D = np.column_stack([X] + [(years == y).astype(float) for y in range(8)])
    coef, *_ = np.linalg.lstsq(D, P0, rcond=None)
    g_hat, i_hat = coef[:2], coef[2:]
    resid = P0 - D @ coef
    V1_hat = I1 + X @ g_hat
    L_hat = np.maximum(P0 - V1_hat, 0.0)

    def reg(cols):
        Z = np.column_stack([np.ones(n)] + cols)
        b, *_ = np.linalg.lstsq(Z, LP, rcond=None)
        return b
    upper = float(reg([V1_hat, L_hat])[2])
    lower = float(reg([V1_hat, L_hat, resid])[2])
    markup = LP - V1
    weeks = rng.geometric(np.clip(h0 * np.exp(-kappa * markup), 1e-4, 1.0))
    loser = L > 0.05
    return {"m": m, "upper": upper, "lower": lower, "share_losers": float(loser.mean()),
            "markup_losers": float(markup[loser].mean()), "markup_gainers": float(markup[~loser].mean()),
            "weeks_losers": float(weeks[loser].mean()), "weeks_gainers": float(weeks[~loser].mean()),
            "index": index.tolist(), "loss": L.tolist(), "markup": markup.tolist(), "i_hat": i_hat.tolist()}


# ---------------------------------------------------------------------------------------------------------------
# present bias


def odr(values, beta: float = 0.5, kind: str = "cost") -> dict:
    """O'Donoghue and Rabin (1999): a task done once in one of T periods.  With ``kind='cost'`` the task's cost is
    paid when it is done and its reward comes later (writing a report); with ``kind='reward'`` its reward comes
    when it is done and its cost later (seeing a film).  Returns the period (1-based) in which a time-consistent
    person (beta = 1), a naif (who believes future selves will be time-consistent) and a sophisticate (who knows
    they will not, and reasons backward) act."""
    v = np.asarray(values, float)
    T = len(v)
    sign = 1.0 if kind == "cost" else -1.0      # minimize costs, maximize rewards

    def now_beats_later(t, later_value, b):
        # cost: act now if c_t <= b * c_later; reward: act now if r_t >= b * r_later
        return v[t] <= b * later_value if kind == "cost" else v[t] >= b * later_value

    tc = int(np.argmin(sign * v)) + 1
    naif = T
    for t in range(T - 1):
        best_later = v[t + 1:].min() if kind == "cost" else v[t + 1:].max()
        if now_beats_later(t, best_later, beta):
            naif = t + 1
            break
    # sophisticate: backward induction over who will act
    doer = T - 1
    acts = [False] * T
    acts[T - 1] = True
    for t in range(T - 2, -1, -1):
        if now_beats_later(t, v[doer], beta):
            acts[t] = True
            doer = t
    soph = acts.index(True) + 1
    return {"tc": tc, "naif": naif, "soph": soph, "values": v.tolist(), "beta": beta, "kind": kind}


def commitment_trial(n: int = 1800, offer_share: float = 0.5, soph_share: float = 0.35, beta_lo: float = 0.4,
                     beta_hi: float = 1.0, target: float = 100.0, flex_mean: float = 16.0, flex_sd: float = 12.0,
                     seed: int = 0) -> dict:
    """A bank offers half of its clients, at random, an account that locks savings away until a goal is reached.
    A client with present bias beta saves beta * target without help; with the lock, the full target.  A
    sophisticate (beta_hat = beta) values the lock at (1 - beta) target less the value of flexibility (normal, mean
    ``flex_mean``, spread ``flex_sd``); a naif (beta_hat = 1) sees no use for it.  Returns take-up, the
    intention-to-treat effect on savings, the effect on those who took it (the Wald ratio) and the average present
    bias of takers and of the rest."""
    rng = np.random.default_rng(seed)
    beta = rng.uniform(beta_lo, beta_hi, n)
    soph = rng.random(n) < soph_share
    offered = rng.random(n) < offer_share
    flex = flex_mean + flex_sd * rng.standard_normal(n)
    value = np.where(soph, (1 - beta) * target, 0.0) - flex
    take = offered & (value > 0)
    savings = np.where(take, target, beta * target) * np.exp(0.25 * rng.standard_normal(n))
    itt = float(savings[offered].mean() - savings[~offered].mean())
    tu = float(take[offered].mean())
    return {"take_up": tu, "itt": itt, "tot": itt / tu if tu > 0 else float("nan"),
            "beta_takers": float(beta[take].mean()) if take.any() else float("nan"),
            "beta_others": float(beta[offered & ~take].mean()),
            "control_mean": float(savings[~offered].mean()), "n": n,
            "soph_takers": float(soph[take].mean()) if take.any() else float("nan")}


def enrolment(n: int = 20000, default: float = 0.0, months: int = 36, beta: float = 0.7, delta: float = 0.995,
              naive: bool = True, cost_mean: float = 30.0, loss_scale: float = 2500.0, zero_share: float = 0.1,
              seed: int = 0) -> dict:
    """Workers with an ideal contribution rate s* (zero for some; otherwise between 2% and 15%) start at the plan's
    default.  Each month the effort of changing, k, is drawn (exponential, mean ``cost_mean``) and paid at once;
    the gain from being at s* instead of the default is loss_scale (s* - d)^2 a month, forever after.  Acting now
    rather than next month costs k now instead of delta k later and gains one more month at s*: a naif, who
    believes next month's self will act, acts when k (1 - beta delta) <= beta g; a time-consistent worker
    (beta = 1) when k (1 - delta) <= g, that is when k is below the present value of the gains.  Returns
    participation and the share still at the default, month by month."""
    rng = np.random.default_rng(seed)
    star = np.where(rng.random(n) < zero_share, 0.0, rng.uniform(0.02, 0.15, n))
    gain_month = loss_scale * (star - default) ** 2
    b = beta if naive else 1.0
    threshold = b * gain_month / (1 - b * delta)
    moved = np.zeros(n, bool)
    rate = np.full(n, default)
    at_default, part = [], []
    for _ in range(months):
        k = rng.exponential(cost_mean, n)
        act = (~moved) & (k <= threshold) & (gain_month > 0)
        moved |= act
        rate[act] = star[act]
        at_default.append(float(np.mean(~moved)))
        part.append(float(np.mean(rate > 0)))
    return {"participation": part, "at_default": at_default, "final_participation": part[-1],
            "final_at_default": at_default[-1], "default": default}


def smart(n: int = 3000, start: float = 0.035, step: float = 0.03, cap: float = 0.15, raises: int = 4,
          beta: float = 0.7, lam: float = 2.25, value_mean: float = 1.5, join_cost_sd: float = 1.0,
          seed: int = 0) -> dict:
    """Save More Tomorrow: workers asked to save more now feel the cut in take-home pay as a loss (lam) and
    today (no beta discount); asked to commit future raises, the cut never shows as a fall in pay and comes later
    (discounted by beta).  Returns the share willing to raise saving now and to commit future raises, and the saving
    rate of those who commit, raise by raise, until the cap."""
    rng = np.random.default_rng(seed)
    value = value_mean + join_cost_sd * rng.standard_normal(n)  # long-run value of saving more, per unit of pay
    now = np.mean(beta * value > lam)            # the cut is today's, and a loss; the value comes later
    later = np.mean(value > 1.0)                 # both are later, and the cut is not a fall in pay
    path = [start]
    for _ in range(raises):
        path.append(min(path[-1] + step, cap))
    return {"join_now": float(now), "join_later": float(later), "path": path}


# ---------------------------------------------------------------------------------------------------------------
# inattention


def shrouded(alpha: float = 0.7, cost: float = 20.0, addon_price: float = 18.0, addon_cost: float = 3.0,
             effort: float = 6.0) -> dict:
    """Gabaix and Laibson (2006): a base good and an add-on (a printer and its ink, a room and its minibar).  A
    share alpha of buyers are myopic and pay the add-on's price when they need it; the rest substitute away at an
    effort cost.  Competition drives profit to zero, so the base good is priced below its cost by the add-on profit
    collected from myopes: p = cost - alpha (addon_price - addon_cost).  A firm that unshrouds turns myopes into
    sophisticates, who then avoid the add-on wherever they buy: it gains no customers (the curse of debiasing)."""
    base = cost - alpha * (addon_price - addon_cost)
    myope_pays = base + addon_price
    soph_pays = base + effort
    return {"base_price": base, "myope_pays": myope_pays, "soph_pays": soph_pays,
            "subsidy_to_sophisticates": cost + addon_cost - soph_pays, "alpha": alpha,
            "below_cost": cost - base, "unshroud_gain": 0.0}


def used_cars(n: int = 400_000, theta: float = 0.3, a: float = 12000.0, b: float = 0.06, sd: float = 900.0,
              top: float = 120_000.0, seed: int = 0) -> dict:
    """Wholesale prices of used cars by mileage with left-digit bias: buyers read the ten-thousands digit and only
    a share 1 - theta of the rest, perceived mileage L + (1 - theta)(m - L), L the mileage rounded down to ten
    thousand; price a - b * perceived + noise.  Prices fall with mileage within each band and jump down at every
    10,000-mile threshold; theta = jump / (jump + slope * 10,000) recovers the inattention."""
    rng = np.random.default_rng(seed)
    m = rng.uniform(5000, top, n)
    L = np.floor(m / 10000) * 10000
    perceived = L + (1 - theta) * (m - L)
    price = a - b * perceived + sd * rng.standard_normal(n)
    # estimator: price on mileage and a step at each threshold (band fixed effects)
    bands = L.astype(int) // 10000
    ub = np.unique(bands)
    D = np.column_stack([m - L] + [(bands == k).astype(float) for k in ub])
    coef, *_ = np.linalg.lstsq(D, price, rcond=None)
    slope = -coef[0]
    level = coef[1:]
    # the jump at a threshold: the band's intercept change beyond what the within-band slope accounts for
    jumps = -(np.diff(level) + slope * 10000)
    J = float(np.mean(jumps))
    theta_hat = J / (J + slope * 10000)
    edges = np.arange(5000, top + 1, 500.0)
    idx = np.digitize(m, edges) - 1
    means = np.array([price[idx == i].mean() for i in range(len(edges) - 1)])
    return {"theta": theta, "theta_hat": float(theta_hat), "slope": float(slope), "jump": J,
            "mid": ((edges[:-1] + edges[1:]) / 2).tolist(), "mean_price": means.tolist(), "n": n}


def ri_choice(prior, U, lam: float, iters: int = 5000, tol: float = 1e-12) -> dict:
    """Rational inattention with Shannon costs (Sims 2003; Matejka and McKay 2015): states x with prior g(x),
    actions a with payoffs U[x, a], information cost lam per nat.  The optimal choice rule is a logit tilted by
    the unconditional choice probabilities, P(a | x) = P(a) exp(U/lam) / sum_b P(b) exp(U_b/lam), with
    P(a) = sum_x g(x) P(a | x); solved by the Blahut-Arimoto iteration.  Returns P(a | x), P(a), the mutual
    information (nats) and the expected payoff."""
    g = np.asarray(prior, float)
    U = np.asarray(U, float)
    A = U.shape[1]
    pa = np.full(A, 1.0 / A)
    Z = np.exp((U - U.max(axis=1, keepdims=True)) / lam)
    for _ in range(iters):
        w = pa * Z
        cond = w / w.sum(axis=1, keepdims=True)
        new = g @ cond
        if np.max(np.abs(new - pa)) < tol:
            pa = new
            break
        pa = new
    w = pa * Z
    cond = w / w.sum(axis=1, keepdims=True)
    with np.errstate(divide="ignore", invalid="ignore"):
        ratio = np.where(cond > 0, cond / np.where(pa > 0, pa, 1.0), 1.0)
        info = float(np.sum(g[:, None] * cond * np.log(ratio)))
    return {"cond": cond, "pa": pa, "info": info, "payoff": float(np.sum(g[:, None] * cond * U))}


def sparse_weights(importance, kappa: float):
    """Attention to each attribute under quadratic loss and an l1 cost of attention (the simplest form of Gabaix's
    sparse max): minimizing sum (m_i - 1)^2 v_i / 2 + kappa sum |m_i| gives m_i = max(0, 1 - kappa / v_i), v_i the
    variance attribute i adds to the decision.  Attributes that matter little get exactly zero attention."""
    v = np.asarray(importance, float)
    return np.maximum(0.0, 1.0 - kappa / np.where(v > 0, v, np.inf))


# ---------------------------------------------------------------------------------------------------------------
# social preferences


def fehr_schmidt(own, other, alpha: float, beta: float):
    """Inequity-averse utility: own payoff, less alpha per unit the other has more, less beta per unit the other has
    less (Fehr and Schmidt 1999)."""
    own, other = np.asarray(own, float), np.asarray(other, float)
    return own - alpha * np.maximum(other - own, 0) - beta * np.maximum(own - other, 0)


def ultimatum(alphas, betas, pie: float = 1.0, grid: int = 201) -> dict:
    """The ultimatum game with Fehr-Schmidt players.  A responder with envy alpha rejects any offer below
    alpha / (1 + 2 alpha) of the pie.  A proposer who knows the population of responders, and has guilt beta, picks
    the offer that maximizes expected utility.  Returns the acceptance curve and each proposer's offer."""
    alphas, betas = np.asarray(alphas, float), np.asarray(betas, float)
    s = np.linspace(0, 0.5, grid)
    thresh = alphas / (1 + 2 * alphas)
    accept = np.array([np.mean(thresh <= x + 1e-12) for x in s])
    offers = []
    for b in betas:
        own = pie * (1 - s)
        u = accept * (own - b * np.maximum(own - pie * s, 0))
        offers.append(float(s[int(np.argmax(u))]))
    return {"s": s.tolist(), "accept": accept.tolist(), "offers": offers, "thresholds": thresh.tolist(),
            "dictator_gives_half": float(np.mean(betas > 0.5))}


def gift_exchange(hours: int = 6, base_effort: float = 1.0, gift: float = 0.3, half_life: float = 1.5) -> dict:
    """A one-off wage raise answered with extra effort that fades: effort = base (1 + gift 2^(-h / half_life)) in
    hour h; the Island's assumption for a one-day job."""
    h = np.arange(hours)
    eff_gift = base_effort * (1 + gift * 2.0 ** (-h / half_life))
    return {"hour": (h + 1).tolist(), "gift": eff_gift.tolist(), "flat": [base_effort] * hours}


# ---------------------------------------------------------------------------------------------------------------
# a literature filtered by significance


def nudge_literature(k: int = 400, mu: float = 1.4, tau: float = 1.0, control: float = 17.2, n_lo: int = 300,
                     n_hi: int = 20000, gamma: float = 0.1, seed: int = 0) -> dict:
    """k trials of nudges whose true effects (percentage points) are normal(mu, tau), each with two arms of a size
    drawn log-uniformly between n_lo and n_hi.  Every trial run by a unit is reported; a journal publishes a
    trial significant at 5% (one-sided, positive) and only a share gamma of the rest.  Returns the estimates, their
    standard errors, which were published, and the averages of each."""
    rng = np.random.default_rng(seed)
    theta = mu + tau * rng.standard_normal(k)
    n = np.exp(rng.uniform(np.log(n_lo), np.log(n_hi), k))
    p = control / 100
    se = 100 * np.sqrt(2 * p * (1 - p) / n)
    x = theta + se * rng.standard_normal(k)
    z = x / se
    pub = (z >= 1.96) | (rng.random(k) < gamma)
    return {"x": x.tolist(), "se": se.tolist(), "published": pub.tolist(), "theta": theta.tolist(),
            "mean_all": float(x.mean()), "mean_published": float(x[pub].mean()), "share_published": float(pub.mean()),
            "mu": mu, "tau": tau, "gamma": gamma}


def selection_mle(x, se, cut: float = 1.96) -> dict:
    """The step-function selection model (Andrews and Kasy 2019) for a set of published estimates: true effects
    normal(mu, tau^2); estimates x ~ normal(effect, se^2); an estimate with z = x / se >= cut is published with
    probability 1, any other with probability gamma.  Maximum likelihood of (mu, tau, gamma) from the published
    estimates alone."""
    x, se = np.asarray(x, float), np.asarray(se, float)
    sig_obs = (x / se) >= cut

    def nll(par):
        mu, ltau, lg = par
        tau = np.exp(ltau)
        gamma = 1 / (1 + np.exp(-lg))
        s = np.sqrt(tau ** 2 + se ** 2)
        dens = norm.logpdf(x, mu, s)
        p_sig = 1 - norm.cdf((cut * se - mu) / s)
        pub = p_sig + gamma * (1 - p_sig)
        return -np.sum(dens + np.where(sig_obs, 0.0, np.log(gamma)) - np.log(pub))
    best = None
    for start in ((np.mean(x), 0.0, 0.0), (0.0, 0.0, -2.0), (np.median(x) / 2, -1.0, -1.0)):
        r = minimize(nll, start, method="Nelder-Mead", options={"xatol": 1e-8, "fatol": 1e-10, "maxiter": 20000})
        if best is None or r.fun < best.fun:
            best = r
    mu, ltau, lg = best.x
    naive = float(np.mean(x))
    return {"mu": float(mu), "tau": float(np.exp(ltau)), "gamma": float(1 / (1 + np.exp(-lg))), "naive": naive,
            "loglik": float(-best.fun)}


# ---------------------------------------------------------------------------------------------------------------
# expectations


def forecasters(T: int = 400, n: int = 40, rho: float = 0.8, sd_shock: float = 1.0, sd_signal: float = 1.5,
                theta: float = 0.0, h: int = 1, seed: int = 0) -> dict:
    """Forecasters of an AR(1) who each see the state through private noise.  Each runs the steady-state Kalman
    filter; a diagnostic forecaster (theta > 0) overweights news, x_hat + theta K (s - rho x_hat_prev) (Bordalo,
    Gennaioli, Ma and Shleifer 2020).  Regress the forecast error on the forecast revision (Coibion and
    Gorodnichenko 2015): pooled over individuals, and for the average forecast.  Rational individuals give zero
    individually and a positive slope for the consensus (information is sticky across people); diagnostic ones
    give a negative individual slope (overreaction)."""
    rng = np.random.default_rng(seed)
    q, r = sd_shock ** 2, sd_signal ** 2
    P = q
    for _ in range(500):
        P_pred = rho ** 2 * P + q
        K = P_pred / (P_pred + r)
        P = (1 - K) * P_pred
    x = np.zeros(T + h + 1)
    for t in range(1, T + h + 1):
        x[t] = rho * x[t - 1] + sd_shock * rng.standard_normal()
    xh = np.zeros(n)
    F = np.zeros((T + 1, n))                # forecast made at t of x[t + h]
    F_prev = np.zeros((T + 1, n))           # forecast made at t - 1 of x[t + h]
    for t in range(1, T + 1):
        s = x[t] + sd_signal * rng.standard_normal(n)
        prior = rho * xh
        news = K * (s - prior)
        xh = prior + news
        F[t] = rho ** h * (xh + theta * news)
        F_prev[t] = rho * F[t - 1]          # the forecast of x[t + h] made at t - 1
    burn = 20
    ts = np.arange(burn, T + 1)
    err = x[ts + h][:, None] - F[ts]
    rev = F[ts] - F_prev[ts]

    def slope(e, v):
        v = v - v.mean()
        return float(np.sum(v * (e - e.mean())) / np.sum(v * v))
    return {"individual": slope(err.ravel(), rev.ravel()), "consensus": slope(err.mean(axis=1), rev.mean(axis=1)),
            "K": float(K), "theta": theta}


# ---------------------------------------------------------------------------------------------------------------
# welfare


def welfare_range(values_by_frame: dict, gain_by_policy: float | None = None) -> dict:
    """Bernheim and Rangel (2009): when a person's choices differ across frames that should not matter, welfare
    is read only where the choices agree.  Given the money value a person reveals for something under each frame,
    the welfare-relevant range is [min, max]; a policy costing less than the minimum is an improvement whatever
    the frame, one costing more than the maximum is not, and between them the choices do not say."""
    v = np.array(list(values_by_frame.values()), float)
    lo, hi = float(v.min()), float(v.max())
    verdict = None
    if gain_by_policy is not None:
        verdict = "improves" if gain_by_policy < lo else ("worsens" if gain_by_policy > hi else "ambiguous")
    return {"lo": lo, "hi": hi, "verdict": verdict}
