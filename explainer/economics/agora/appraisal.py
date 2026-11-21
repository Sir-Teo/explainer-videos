"""Agora's appraisal module (Part 58): is a project, a rule or a law worth it, and what will it cost?

* **The bridge** (:data:`BRIDGE`, :func:`bridge_year`, :func:`appraise`): the Island's proposed bridge across the
  strait, against Bo's ferry.  Crossings follow a linear demand in the generalized cost of a crossing (the fare plus
  the value of the time it takes); the bridge lowers that cost, and travellers gain Dupuit's surplus: the saving on
  every trip already made, and half of it on each new trip (the rule of a half).  Bo's lost profit is subtracted, so
  the fares travellers no longer pay count only as the ferry's resources freed; lives saved are valued at the value of
  a statistical life, noise by the hedonic loss on the homes beside the approach road; construction over three years,
  maintenance, a hundred years of use and traffic growth; a shadow wage for idle labour and the marginal cost of
  public funds as options.  Net present value, the benefit-cost ratio, the internal rate of return, and the tornado of
  sensitivities (:func:`tornado`).
* **Discounting** (:func:`discount_factors`, :data:`GREEN_BOOK_2003`, :func:`stpr`, :func:`weitzman`): a constant
  rate, the Green Book's declining step schedule, the Ramsey social time preference rate, and Weitzman's certainty
  equivalent rate when the right rate is itself uncertain.
* **Values without prices** (:func:`hedonic_houses`, :func:`travel_cost`): noise priced from house prices, with the
  omitted amenity that biases the naive regression; a beach valued from the trips people make to it.
* **A statistical life** (:func:`wage_risk`, :func:`vsly`): the wage premium for risk on the Island's jobs, biased by
  unseen ability and by noisy risk data; the value of a statistical life-year.
* **Risk** (:func:`reference_class`, :func:`monte_carlo`, :func:`wait_option`): an outside view from past projects'
  cost overruns and traffic shortfalls, the uplift it implies, the distribution of the net present value, and the
  option to wait a year.
* **Scoring a bill** (:func:`taxpayers`, :func:`income_tax`, :func:`score_top_rate`, :func:`dynamic_score`): a survey
  of the Island's taxpayers, grossed up by its weights; a higher top rate scored statically and with the elasticity
  of taxable income; a dynamic score with growth and with interest rates that rise with the debt.
* **Microsimulation** (:func:`households`, :func:`net_income`, :func:`distribution_table`): a tax and benefit
  calculator run on a household survey, the reform's cost and its gains by decile.
* **General equilibrium** (:func:`cge`, :func:`sam`): two sectors, two factors and a household, a tax on manufactures,
  the social accounting matrix before and after, and the deadweight loss against Harberger's triangle.
* **Rules and targets** (:func:`rule_appraisal`, :func:`target_gaming`): a regulation's net benefits by discount rate
  and its break-even; a four-hour target and the patients moved just under it.
* **The record** (:func:`cbo_record`): the Congressional Budget Office's deficit projections since 1984 against what
  happened.
* **The frontier** (:func:`distributional_weights`).

numpy and scipy only.
"""

from __future__ import annotations

import numpy as np
from scipy import optimize

# ---------------------------------------------------------------------------------------------------------------
# the bridge

# Money in millions of Island dollars, crossings in millions a year.  Demand: crossings = a - b * generalized cost.
BRIDGE = {
    "a": 1.8, "b": 0.08,                       # demand for crossings
    "fare": 4.0, "ferry_minutes": 40.0,        # Bo's ferry: the fare and the time a crossing takes, waits included
    "toll": 0.0, "bridge_minutes": 8.0,        # the bridge: free, and eight minutes
    "wage": 24.0, "vot_share": 0.5,            # dollars an hour; time valued at half the wage (DOT's rule)
    "ferry_unit_cost": 1.5, "ferry_fixed": 0.6,   # Bo's costs: per crossing, and a year
    "risk_ferry": 0.24, "risk_bridge": 0.05,   # deaths per million crossings
    "vsl": 9.0,                                 # the Island's value of a statistical life, millions
    "build": (100.0, 100.0, 100.0),            # construction, three years
    "maintenance": 1.2, "life": 100, "growth": 0.01, "growth_years": 40,
    "homes": 200, "home_price": 0.2, "noise_db": 10.0, "noise_pct": 0.007,   # homes by the approach road
    "labour_share": 0.4, "idle_share": 0.0, "shadow_wage": 0.5,             # the shadow wage, off by default
    "mcpf": 1.0, "cost_ratio": 1.0, "traffic_ratio": 1.0,
}
COMPONENTS = ("time", "fares", "new trips", "Bo's profit", "safety", "noise", "construction", "maintenance")


def generalized_cost(fare: float, minutes: float, vot: float) -> float:
    """What a crossing costs a traveller: the fare plus the value of the minutes it takes."""
    return fare + vot * minutes / 60.0


def bridge_year(p: dict | None = None) -> dict:
    """One year of the bridge at the forecast traffic, before growth: the generalized costs and crossings with the
    ferry and with the bridge, and each component of the gain (millions a year)."""
    p = {**BRIDGE, **(p or {})}
    vot = p["vot_share"] * p["wage"]
    g0 = generalized_cost(p["fare"], p["ferry_minutes"], vot)
    g1 = generalized_cost(p["toll"], p["bridge_minutes"], vot)
    q0 = max(p["a"] - p["b"] * g0, 0.0)
    q1 = max(p["a"] - p["b"] * g1, 0.0)
    time = q0 * vot * (p["ferry_minutes"] - p["bridge_minutes"]) / 60.0
    fares = q0 * (p["fare"] - p["toll"])
    new = 0.5 * (q1 - q0) * (g0 - g1)
    profit = (p["fare"] - p["ferry_unit_cost"]) * q0 - p["ferry_fixed"]
    lives = p["risk_ferry"] * q0 - p["risk_bridge"] * q1
    return {"vot": vot, "g0": g0, "g1": g1, "q0": q0, "q1": q1, "time": time, "fares": fares, "new trips": new,
            "Bo's profit": -profit, "safety": lives * p["vsl"], "lives": lives,
            "surplus": q0 * (g0 - g1) + new, "toll_revenue": p["toll"] * q1}


def discount_factors(T: int, rate=None, schedule=None) -> np.ndarray:
    """Discount factors for years 0..T-1: a constant ``rate`` (a share, 0.035), or a step ``schedule`` of
    ``(first year, rate in percent)`` pairs such as :data:`GREEN_BOOK_2003`, each rate applying from its first year
    until the next one starts."""
    t = np.arange(T)
    if schedule is None:
        return (1.0 + rate) ** -t
    rates = np.zeros(T)
    for start, r in schedule:
        rates[t >= start] = r / 100.0
    df = np.ones(T)
    for k in range(1, T):
        df[k] = df[k - 1] / (1.0 + rates[k])
    return df


def bridge_streams(p: dict | None = None) -> dict:
    """The bridge's yearly streams, millions: construction in years 0-2, then ``life`` years of use; traffic grows at
    ``growth`` for ``growth_years`` and is then flat; ``traffic_ratio`` and ``cost_ratio`` scale the outturn against
    the forecast."""
    p = {**BRIDGE, **(p or {})}
    y = bridge_year(p)
    nb = len(p["build"])
    T = nb + p["life"]
    t = np.arange(T)
    use = t >= nb
    G = np.where(use, (1.0 + p["growth"]) ** np.clip(t - nb, 0, p["growth_years"]), 0.0) * p["traffic_ratio"]
    s = {k: G * y[k] for k in ("time", "fares", "new trips", "safety")}
    # Bo's profit is lost once the bridge opens: the fares above his variable cost, less the fixed cost he saves
    s["Bo's profit"] = np.where(use, -((p["fare"] - p["ferry_unit_cost"]) * y["q0"] * G - p["ferry_fixed"]), 0.0)
    noise = np.zeros(T)
    noise[nb] = -p["homes"] * p["home_price"] * p["noise_pct"] * p["noise_db"]
    s["noise"] = noise
    adj = (1.0 - p["labour_share"] * p["idle_share"] * (1.0 - p["shadow_wage"])) * p["mcpf"] * p["cost_ratio"]
    build = np.zeros(T)
    build[:nb] = -np.asarray(p["build"], float) * adj
    s["construction"] = build
    s["maintenance"] = np.where(use, -p["maintenance"] * p["mcpf"], 0.0)
    return {"t": t, "streams": s, "year": y, "opens": nb}


def appraise(p: dict | None = None, rate: float = 0.035, schedule=None) -> dict:
    """Present values by component, the net present value, the benefit-cost ratio (benefits over costs, both in
    present value; Bo's lost profit and the noise count as costs) and the internal rate of return."""
    b = bridge_streams(p)
    T = len(b["t"])
    df = discount_factors(T, rate, schedule)
    pv = {k: float(np.sum(v * df)) for k, v in b["streams"].items()}
    npv = sum(pv.values())
    ben = sum(v for v in pv.values() if v > 0)
    cost = -sum(v for v in pv.values() if v < 0)
    return {"pv": pv, "npv": npv, "bcr": ben / cost, "benefits": ben, "costs": cost, "irr": irr(p),
            "year": b["year"]}


def npv_at(p: dict | None, rate: float) -> float:
    b = bridge_streams(p)
    total = sum(b["streams"].values())
    return float(np.sum(total * (1.0 + rate) ** -b["t"]))


def irr(p: dict | None = None) -> float:
    """The discount rate at which the net present value is zero."""
    f = lambda r: npv_at(p, r)  # noqa: E731
    if f(0.0) <= 0:
        return float("nan")
    return float(optimize.brentq(f, 1e-6, 0.5))


def npv_curve(p: dict | None, rates) -> np.ndarray:
    return np.array([npv_at(p, r) for r in rates])


TORNADO = {
    "discount rate": ("rate", 0.03, 0.07),
    "value of time (35% to 60% of the wage)": ("vot_share", 0.35, 0.60),
    "construction cost (as forecast to +45%)": ("cost_ratio", 1.0, 1.45),
    "traffic (-30% to +10%)": ("traffic_ratio", 0.7, 1.1),
    "value of a statistical life (5 to 14)": ("vsl", 5.0, 14.0),
    "cost of public funds (1.0 to 1.2)": ("mcpf", 1.0, 1.2),
}


def tornado(p: dict | None = None, rate: float = 0.035, ranges: dict | None = None) -> list:
    """Each assumption moved alone across its range, the others at their central values: ``[(name, npv at the low
    end, npv at the high end)]``, widest swing first."""
    ranges = ranges or TORNADO
    base = {**BRIDGE, **(p or {})}
    out = []
    for name, (key, lo, hi) in ranges.items():
        vals = []
        for v in (lo, hi):
            if key == "rate":
                vals.append(appraise(base, rate=v)["npv"])
            else:
                vals.append(appraise({**base, key: v}, rate=rate)["npv"])
        out.append((name, vals[0], vals[1]))
    return sorted(out, key=lambda r: -abs(r[2] - r[1]))


# ---------------------------------------------------------------------------------------------------------------
# discounting

# HM Treasury's Green Book (2003-2026): 3.5% for years 0-30, then declining
GREEN_BOOK_2003 = ((0, 3.5), (31, 3.0), (76, 2.5), (126, 2.0), (201, 1.5), (301, 1.0))


def stpr(delta: float = 0.5, catastrophe: float = 1.0, eta: float = 1.0, g: float = 2.0) -> float:
    """The Green Book's social time preference rate, percent: pure time preference plus the risk of catastrophe,
    plus the elasticity of marginal utility times the growth of consumption per head (Ramsey's rule)."""
    return delta + catastrophe + eta * g


def weitzman(rates, probs, horizons) -> dict:
    """When the right constant rate is uncertain (``rates``, shares, with ``probs``), the certainty-equivalent
    discount factor is the average of the discount factors; the rate it implies, constant from today to each horizon,
    and the year-to-year (forward) rate both fall towards the lowest rate as the horizon lengthens."""
    r = np.asarray(rates, float)
    w = np.asarray(probs, float) / np.sum(probs)
    h = np.asarray(horizons, float)
    df = np.array([np.sum(w * (1.0 + r) ** -t) for t in h])
    with np.errstate(divide="ignore", invalid="ignore"):
        avg = np.where(h > 0, df ** (-1.0 / np.where(h > 0, h, 1.0)) - 1.0, np.sum(w * r))
    fwd = np.array([np.sum(w * (1.0 + r) ** -t) / np.sum(w * (1.0 + r) ** -(t + 1)) - 1.0 for t in h])
    return {"horizon": h, "df": df, "rate": avg, "forward": fwd}


# ---------------------------------------------------------------------------------------------------------------
# small regressions

def ols(X, y) -> dict:
    """Least squares with heteroskedasticity-robust (HC1) standard errors."""
    X = np.asarray(X, float)
    y = np.asarray(y, float)
    n, k = X.shape
    b, *_ = np.linalg.lstsq(X, y, rcond=None)
    e = y - X @ b
    XtXi = np.linalg.inv(X.T @ X)
    V = XtXi @ (X.T * e ** 2) @ X @ XtXi * n / (n - k)
    return {"b": b, "se": np.sqrt(np.diag(V)), "resid": e, "r2": 1.0 - e.var() / y.var()}


# ---------------------------------------------------------------------------------------------------------------
# values without prices

def hedonic_houses(n: int = 3000, beta: float = -0.007, seed: int = 58) -> dict:
    """The Island's houses: distance to the harbour (an amenity: prices fall 6% a kilometre), rooms, and road noise
    in decibels, which is loudest by the coast road along the harbour.  Log price = ... + ``beta`` x noise.  A
    regression of price on noise alone mixes the noise with the harbour; with the harbour and rooms held fixed it
    recovers ``beta``.  Returns both fits (percent per decibel) and the data."""
    rng = np.random.default_rng(seed)
    harbour = rng.uniform(0.0, 5.0, n)
    road = np.abs(0.6 * harbour + rng.normal(0.0, 0.5, n))
    noise = 48.0 + 22.0 * np.exp(-road / 0.5) + rng.normal(0.0, 2.0, n)
    rooms = rng.integers(2, 7, n)
    lp = np.log(200000.0) + 0.10 * (rooms - 4) - 0.06 * harbour + beta * (noise - 50.0) + rng.normal(0.0, 0.12, n)
    one = np.ones(n)
    naive = ols(np.column_stack([one, noise]), lp)
    full = ols(np.column_stack([one, noise, harbour, rooms]), lp)
    return {"naive": 100 * naive["b"][1], "naive_se": 100 * naive["se"][1], "full": 100 * full["b"][1],
            "full_se": 100 * full["se"][1], "truth": 100 * beta, "noise": noise, "price": np.exp(lp),
            "harbour": harbour, "rooms": rooms, "corr": float(np.corrcoef(noise, harbour)[0, 1])}


def travel_cost(seed: int = 58) -> dict:
    """A beach valued by the trips to it: ten villages at different distances; each trip costs the fuel and the
    time of a return journey; visits per resident fall with the cost.  The fitted line is the beach's demand curve,
    and each resident's surplus is the triangle above their cost (Hotelling's suggestion of 1947, Clawson's method)."""
    rng = np.random.default_rng(seed)
    km = np.array([1.0, 2.0, 3.5, 5.0, 6.5, 8.0, 10.0, 12.0, 14.0, 16.0])
    pop = np.array([4000, 3500, 2500, 3000, 2000, 1500, 2500, 1200, 800, 1000], float)
    cost = 2.0 * km * (0.3 + 12.0 / 30.0)          # fuel at 0.3 a km, time at 12 an hour and 30 km an hour
    visits = np.maximum(6.0 - 0.25 * cost + rng.normal(0.0, 0.35, km.size), 0.0)
    fit = ols(np.column_stack([np.ones(km.size), cost]), visits)
    a, b = fit["b"][0], -fit["b"][1]
    cs = np.where(cost < a / b, (a - b * cost) ** 2 / (2.0 * b), 0.0)
    return {"km": km, "pop": pop, "cost": cost, "visits": visits, "a": a, "b": b, "choke": a / b,
            "cs_per_person": cs, "value": float(np.sum(cs * pop)), "trips": float(np.sum(visits * pop))}


# ---------------------------------------------------------------------------------------------------------------
# a statistical life

def wage_risk(n: int = 100000, vsl: float = 9.0, seed: int = 58) -> dict:
    """The Island's workers: ability raises pay and steers people, a little, to safer jobs; each job's fatal risk
    (deaths per 10,000 workers a year) carries a wage premium of ``vsl``/10 thousand a year per unit, which is what a
    value of a statistical life of ``vsl`` millions means.  Three regressions of the wage on risk: without ability
    (biased down), with it (right), and with ability but risk measured from noisy fatality counts (attenuated).
    Returns each implied value of a statistical life, millions."""
    rng = np.random.default_rng(seed)
    ability = rng.standard_normal(n)
    risk = np.clip(1.0 - 0.015 * ability + 0.5 * rng.standard_normal(n), 0.0, None)
    wage = 30.0 + 8.0 * ability + (vsl / 10.0) * risk + rng.normal(0.0, 3.0, n)
    measured = risk + rng.normal(0.0, 0.3, n)
    one = np.ones(n)
    fits = {"naive": ols(np.column_stack([one, risk]), wage),
            "controls": ols(np.column_stack([one, risk, ability]), wage),
            "noisy": ols(np.column_stack([one, measured, ability]), wage)}
    out = {k: 10.0 * f["b"][1] for k, f in fits.items()}
    out.update({f"{k}_se": 10.0 * f["se"][1] for k, f in fits.items()})
    out.update({"truth": vsl, "risk": risk, "wage": wage, "ability": ability, "mean_risk": float(risk.mean()),
                "premium": vsl / 10.0 * float(risk.mean())})
    return out


def annuity(years: float, r: float) -> float:
    return float(years) if r == 0 else (1.0 - (1.0 + r) ** -years) / r


def vsly(vsl: float, years_left: float, r: float = 0.03) -> float:
    """The value of a statistical life-year: the VSL spread evenly, with discounting, over the years left."""
    return vsl / annuity(years_left, r)


# ---------------------------------------------------------------------------------------------------------------
# risk

def lognormal_params(mean: float, sd: float) -> tuple[float, float]:
    s2 = np.log(1.0 + (sd / mean) ** 2)
    return float(np.log(mean) - s2 / 2.0), float(np.sqrt(s2))


# The Island's reference class: outturn over forecast for its last sixty public works.  Costs are planted to match
# the average and spread Flyvbjerg, Holm and Buhl found across 258 transport projects (28% over, s.d. 39 points);
# traffic is planted at 10% below forecast on average.
REFERENCE = {"cost": (1.28, 0.39), "traffic": (0.90, 0.25), "n": 60}


def reference_class(n: int | None = None, seed: int = 58) -> dict:
    rng = np.random.default_rng(seed)
    n = n or REFERENCE["n"]
    mc, sc = lognormal_params(*REFERENCE["cost"])
    mt, st = lognormal_params(*REFERENCE["traffic"])
    cost = np.exp(rng.normal(mc, sc, n))
    traffic = np.exp(rng.normal(mt, st, n))
    return {"cost": cost, "traffic": traffic, "uplift50": float(np.quantile(cost, 0.5) - 1.0),
            "uplift80": float(np.quantile(cost, 0.8) - 1.0), "share_over": float(np.mean(cost > 1.0)),
            "mean_cost": float(cost.mean()), "mean_traffic": float(traffic.mean())}


def monte_carlo(p: dict | None = None, rate: float = 0.035, draws: int = 4000, seed: int = 58) -> dict:
    """The net present value when costs and traffic come out as the reference class says they do: the bridge's
    benefits scale with traffic and its construction with the cost ratio, so the NPV is linear in both."""
    base = {**BRIDGE, **(p or {})}
    rng = np.random.default_rng(seed)
    mc, sc = lognormal_params(*REFERENCE["cost"])
    mt, st = lognormal_params(*REFERENCE["traffic"])
    c = np.exp(rng.normal(mc, sc, draws))
    tr = np.exp(rng.normal(mt, st, draws))
    a = appraise(base, rate)
    pv = a["pv"]
    traffic_part = pv["time"] + pv["fares"] + pv["new trips"] + pv["safety"]
    bo_var = appraise({**base, "ferry_fixed": 0.0}, rate)["pv"]["Bo's profit"]
    bo_fixed = pv["Bo's profit"] - bo_var
    npv = (tr * (traffic_part + bo_var) + bo_fixed + pv["noise"] + pv["maintenance"] + c * pv["construction"])
    return {"npv": npv, "mean": float(npv.mean()), "p_negative": float(np.mean(npv < 0)),
            "p10": float(np.quantile(npv, 0.1)), "p90": float(np.quantile(npv, 0.9)), "forecast": a["npv"]}


def wait_option(p: dict | None = None, rate: float = 0.035, high: float = 1.3, low: float = 0.7,
                prob_high: float = 0.5) -> dict:
    """Build now, or wait a year and learn whether traffic will be high or low, and build only if it pays then?
    Waiting delays every stream a year; its value is the bad case avoided."""
    base = {**BRIDGE, **(p or {})}
    now = {s: appraise({**base, "traffic_ratio": base["traffic_ratio"] * m}, rate)["npv"]
           for s, m in (("high", high), ("low", low))}
    build_now = prob_high * now["high"] + (1 - prob_high) * now["low"]
    wait = (prob_high * max(now["high"], 0.0) + (1 - prob_high) * max(now["low"], 0.0)) / (1.0 + rate)
    return {"now": build_now, "wait": wait, "value": wait - build_now, "npv_high": now["high"],
            "npv_low": now["low"], "build_if_wait": {s: v > 0 for s, v in now.items()}}


# ---------------------------------------------------------------------------------------------------------------
# scoring a bill

# The Island's income tax: a personal allowance, then 20%, 35% and 40% (the top rate, above 150,000 of income)
SCHEDULE = ((15000.0, 0.0), (50000.0, 0.20), (150000.0, 0.35), (np.inf, 0.40))


def income_tax(z, schedule=SCHEDULE):
    """Tax on income ``z`` under a schedule of ``(upper limit, rate)`` bands."""
    z = np.asarray(z, float)
    tax = np.zeros_like(z)
    lo = 0.0
    for hi, r in schedule:
        tax += r * np.clip(z - lo, 0.0, hi - lo)
        lo = hi
    return tax


def with_top(schedule, rate: float, threshold: float | None = None):
    """The schedule with a new top rate (and optionally a new top threshold)."""
    bands = list(schedule)
    if threshold is not None:
        bands[-2] = (threshold, bands[-2][1])
    bands[-1] = (np.inf, rate)
    return tuple(bands)


# the microsimulation's reform: a higher allowance, paid for by a top rate of 45% from 80,000
def reform_schedule(allowance: float = 18000.0, top: float = 0.45, threshold: float = 80000.0, schedule=None):
    return with_top(with_allowance(schedule or SCHEDULE, allowance), top, threshold)


def with_allowance(schedule, allowance: float):
    bands = list(schedule)
    bands[0] = (allowance, 0.0)
    return tuple(bands)


def taxpayers(N: int = 400000, seed: int = 58) -> dict:
    """The Island's 400,000 taxpayers and the survey of them.  Incomes: log-normal (median 38,000, log-s.d. 0.7)
    below 150,000; above it, Pareto with exponent 1.5, with as many people up there as the log-normal puts there.
    The survey takes one in ten below 150,000 and one in two above it, so each record carries a weight of 10 or 2: the
    survey's totals are the population's only once the records are grossed up by their weights."""
    rng = np.random.default_rng(seed)
    z = 38000.0 * np.exp(0.7 * rng.standard_normal(N))
    top = z > 150000.0
    z[top] = 150000.0 * (1.0 - rng.random(top.sum())) ** (-1.0 / 1.5)
    take = np.where(top, rng.random(N) < 0.5, rng.random(N) < 0.1)
    w = np.where(top, 2.0, 10.0)
    return {"z": z[take], "w": w[take], "N": N, "pop_total": float(z.sum()), "pop_top": int(top.sum()),
            "n": int(take.sum()), "a": 1.5, "threshold": 150000.0}


def score_top_rate(T: dict | None = None, t1: float = 0.45, e: float = 0.25, schedule=SCHEDULE) -> dict:
    """A higher top rate, scored on the grossed-up survey (millions a year).  Static: incomes unchanged.  With
    behaviour (the conventional score): incomes in the top band move with the net-of-tax rate, z x ((1 - t1)/(1 - t0))
    ^ e, but no lower than the threshold.  Saez's formula for the ratio of the two, 1 - e a t/(1 - t), for the Pareto
    exponent a."""
    T = T or taxpayers()
    z, w = T["z"], T["w"]
    t0 = schedule[-1][1]
    zbar = schedule[-2][0]
    new = with_top(schedule, t1)
    base = income_tax(z, schedule)
    static = float(np.sum(w * (income_tax(z, new) - base))) / 1e6
    z1 = np.where(z > zbar, np.maximum(zbar, z * ((1.0 - t1) / (1.0 - t0)) ** e), z)
    behave = float(np.sum(w * (income_tax(z1, new) - base))) / 1e6
    lost = float(np.sum(w * (z - z1))) / 1e6
    return {"static": static, "behavioural": behave, "ratio": behave / static, "income_lost": lost,
            "formula": 1.0 - e * T["a"] * t1 / (1.0 - t1), "formula_t0": 1.0 - e * T["a"] * t0 / (1.0 - t0),
            "t0": t0, "t1": t1, "e": e, "top_records": int(np.sum(z > zbar)),
            "top_people": float(np.sum(w * (z > zbar)))}


def dynamic_score(cut: float = 1.0, years: int = 10, tau: float = 0.3, gain: float = 0.4, speed: float = 0.25,
                  debt0: float = 100.0, kappa: float = 0.025, i0: float = 3.0) -> dict:
    """A tax cut of ``cut`` percent of GDP a year, scored three ways over a ten-year window (percent of GDP).
    Conventional: the cut itself.  Growth: output rises towards ``gain`` percent (at ``speed`` a year), and the tax
    take on it, at the average rate ``tau``, pays some back.  Interest rates: each point of debt to GDP added raises
    the rate on all debt by ``kappa`` points (crowding out), which costs ``debt0`` x the rise.  Debt service on the
    added debt itself is shown apart.  Returns the yearly paths and their sums."""
    t = np.arange(1, years + 1)
    conv = np.full(years, cut)
    dY = gain * (1.0 - (1.0 - speed) ** t)
    feedback = -tau * dY
    rate_cost = np.zeros(years)
    service = np.zeros(years)
    added = 0.0
    for k in range(years):
        rate_cost[k] = kappa * added * debt0 / 100.0
        service[k] = (i0 / 100.0) * added
        added += conv[k] + feedback[k] + rate_cost[k] + service[k]
    dyn = conv + feedback + rate_cost
    return {"t": t, "conventional": conv, "growth": feedback, "rates": rate_cost, "service": service, "dynamic": dyn,
            "sum_conventional": float(conv.sum()), "sum_growth": float(feedback.sum()),
            "sum_rates": float(rate_cost.sum()), "sum_dynamic": float(dyn.sum()), "sum_service": float(service.sum()),
            "debt_added": added}


def window(cost: float = 100.0, years: int = 10, sunset: int | None = None, horizon: int = 30) -> dict:
    """A tax cut costing ``cost`` a year, scored over the budget window, written to expire after ``sunset`` years or
    not; its cost over a longer horizon if it is extended when it expires, as most are."""
    inside = cost * (sunset if sunset is not None and sunset < years else years)
    return {"window": inside, "permanent": cost * years, "horizon": cost * horizon,
            "hidden": cost * years - inside}


# ---------------------------------------------------------------------------------------------------------------
# microsimulation

def households(n: int = 6000, seed: int = 58) -> dict:
    """The Island's household survey: one or two adults, none to three children, each adult's earnings log-normal
    (median 32,000) or zero (one adult in six does not work); the survey over-samples families with children, so
    weights differ (25 for families with children, 35 for the rest), and the Island's 400,000 or so people come out
    of the weights, not out of the 6,000 records."""
    rng = np.random.default_rng(seed)
    adults = rng.choice([1, 2], n, p=[0.4, 0.6])
    kids = np.where(rng.random(n) < 0.55, rng.choice([1, 2, 3], n, p=[0.45, 0.4, 0.15]), 0)
    e = 32000.0 * np.exp(0.75 * rng.standard_normal((n, 2)))
    e[rng.random((n, 2)) < 1 / 6] = 0.0
    e[:, 1] = np.where(adults == 2, e[:, 1], 0.0)
    w = np.where(kids > 0, 25.0, 35.0)
    return {"earn": e, "adults": adults, "kids": kids, "w": w, "n": n}


# The Island's benefits: 1,000 a child a year; a credit of 3,000 for families with children, withdrawn at 30% of
# household earnings above 20,000
BENEFITS = {"child": 1000.0, "credit": 3000.0, "credit_from": 20000.0, "taper": 0.30}


def net_income(H: dict, schedule=SCHEDULE, benefits: dict | None = None) -> dict:
    """The tax and benefit calculator: each adult taxed separately; child benefit; the means-tested credit."""
    b = {**BENEFITS, **(benefits or {})}
    tax = income_tax(H["earn"][:, 0], schedule) + income_tax(H["earn"][:, 1], schedule)
    gross = H["earn"].sum(axis=1)
    child = b["child"] * H["kids"]
    credit = np.where(H["kids"] > 0, np.maximum(b["credit"] - b["taper"] * np.maximum(gross - b["credit_from"], 0),
                                                0.0), 0.0)
    net = gross - tax + child + credit
    return {"gross": gross, "tax": tax, "benefits": child + credit, "net": net}


def distribution_table(H: dict, base: dict, reform: dict, deciles: int = 10) -> dict:
    """The reform's average gain by decile of equivalized household income (net income over the square root of
    household size, before the reform), in money and as a percent of net income; the cost, grossed up."""
    size = H["adults"] + H["kids"]
    eq = base["net"] / np.sqrt(size)
    gain = reform["net"] - base["net"]
    w = H["w"]
    order = np.argsort(eq)
    cw = np.cumsum(w[order]) / w.sum()
    dec = np.empty(len(eq), int)
    dec[order] = np.minimum(np.searchsorted(np.linspace(0, 1, deciles + 1)[1:-1], cw, side="left"), deciles - 1)
    rows = []
    for d in range(deciles):
        m = dec == d
        rows.append({"decile": d + 1, "gain": float(np.sum(w[m] * gain[m]) / np.sum(w[m])),
                     "pct": float(100 * np.sum(w[m] * gain[m]) / np.sum(w[m] * base["net"][m])),
                     "winners": float(np.sum(w[m] * (gain > 1)[m]) / np.sum(w[m])),
                     "losers": float(np.sum(w[m] * (gain < -1)[m]) / np.sum(w[m]))})
    return {"rows": rows, "cost": float(np.sum(w * gain)) / 1e6, "households": float(w.sum()),
            "people": float(np.sum(w * size))}


# ---------------------------------------------------------------------------------------------------------------
# general equilibrium

CGE = {"L": 100.0, "K": 100.0, "alpha": {"F": 0.6, "M": 0.4}, "share": {"F": 0.4, "M": 0.6}}


def cge(t: float = 0.0, params: dict | None = None) -> dict:
    """A closed economy: food (F) and manufactures (M), each made from labour and capital with Cobb-Douglas
    technology (labour shares 0.6 and 0.4); one household that owns both factors and spends 40% on food; a tax ``t``
    on manufactures, its revenue handed back.  Capital's price is the numeraire; the wage clears the labour market.
    Returns prices, quantities, factor allocations, income and utility."""
    P = {**CGE, **(params or {})}
    L, K, al, s = P["L"], P["K"], P["alpha"], P["share"]

    def unit_cost(j, w):
        a = al[j]
        return (w / a) ** a * (1.0 / (1.0 - a)) ** (1.0 - a)

    def solve(w):
        p = {j: unit_cost(j, w) for j in "FM"}
        income = (w * L + K) / (1.0 - t * s["M"] / (1.0 + t))
        X = {"F": s["F"] * income / p["F"], "M": s["M"] * income / (p["M"] * (1.0 + t))}
        Ld = {j: al[j] * p[j] * X[j] / w for j in "FM"}
        Kd = {j: (1.0 - al[j]) * p[j] * X[j] for j in "FM"}
        return p, income, X, Ld, Kd

    w = optimize.brentq(lambda w: sum(solve(w)[3].values()) - L, 1e-3, 1e3, xtol=1e-14)
    p, income, X, Ld, Kd = solve(w)
    U = X["F"] ** s["F"] * X["M"] ** s["M"]
    revenue = t * p["M"] * X["M"]
    return {"t": t, "w": w, "r": 1.0, "p": p, "income": income, "X": X, "L": Ld, "K": Kd, "U": U,
            "revenue": revenue}


def cge_welfare(t: float, params: dict | None = None) -> dict:
    """The tax's deadweight loss in general equilibrium (equivalent variation at the untaxed prices, revenue handed
    back) against Harberger's partial-equilibrium triangle, 1/2 t^2 e p X, with the compensated demand elasticity of
    manufactures and supply taken as flat."""
    base, taxed = cge(0.0, params), cge(t, params)
    ev = base["income"] * (taxed["U"] / base["U"] - 1.0)
    sM = (params or CGE).get("share", CGE["share"])["M"]
    eps = 1.0 - sM                                # Cobb-Douglas: compensated own-price elasticity 1 - share
    tri = 0.5 * t ** 2 * eps * base["p"]["M"] * base["X"]["M"]
    return {"ev": ev, "dwl": -ev, "harberger": tri, "base": base, "taxed": taxed,
            "dwl_pct_revenue": 100 * -ev / taxed["revenue"] if taxed["revenue"] else 0.0}


def sam(eq: dict) -> dict:
    """The social accounting matrix of an equilibrium of :func:`cge`: each column pays the rows; every row total
    equals its column total.  Accounts: food, manufactures, labour, capital, household, government."""
    acc = ["food", "manufactures", "labour", "capital", "household", "government"]
    M = np.zeros((6, 6))
    pF, pM = eq["p"]["F"], eq["p"]["M"]
    M[0, 4] = pF * eq["X"]["F"]                 # the household buys food
    M[1, 4] = pM * eq["X"]["M"]                 # and manufactures, at producer prices
    M[5, 4] = eq["revenue"]                     # and pays the tax on them
    M[2, 0], M[3, 0] = eq["w"] * eq["L"]["F"], eq["K"]["F"]
    M[2, 1], M[3, 1] = eq["w"] * eq["L"]["M"], eq["K"]["M"]
    M[4, 2] = M[2, 0] + M[2, 1]                 # labour's income goes to the household
    M[4, 3] = M[3, 0] + M[3, 1]
    M[4, 5] = eq["revenue"]                     # the government hands the revenue back
    return {"accounts": acc, "M": M, "rows": M.sum(axis=1), "cols": M.sum(axis=0),
            "balanced": bool(np.allclose(M.sum(axis=1), M.sum(axis=0)))}


# ---------------------------------------------------------------------------------------------------------------
# rules and targets

def rule_appraisal(upfront: float = 60.0, yearly_cost: float = 40.0, deaths: float = 4.0, vsl: float = 9.0,
                   tonnes: float = 0.1, scc: float = 120.0, years: int = 20, rates=(0.02, 0.03, 0.07)) -> dict:
    """A regulation (scrubbers at the Island's two power stations), appraised as a regulatory impact analysis:
    costs up front and each year; benefits from deaths avoided at the VSL and from carbon (millions of tonnes a year)
    at a social cost of carbon (dollars a tonne).  Net benefits at each rate; the deaths a year at which it would
    break even."""
    t = np.arange(years + 1)
    out = []
    for r in rates:
        df = (1.0 + r) ** -t
        cost = upfront + yearly_cost * df[1:].sum()
        lives = deaths * vsl * df[1:].sum()
        carbon = tonnes * scc * df[1:].sum()
        out.append({"rate": r, "cost": cost, "lives": lives, "carbon": carbon, "net": lives + carbon - cost,
                    "breakeven_deaths": (cost - carbon) / (vsl * df[1:].sum())})
    return {"rows": out, "deaths": deaths, "vsl": vsl, "scc": scc}


def target_gaming(n: int = 20000, target: float = 240.0, reach: float = 120.0, effort: float = 0.8,
                  seed: int = 58) -> dict:
    """An emergency department's times from arrival to admission or discharge, minutes (log-normal, median 160).
    Under a four-hour target, a patient who would breach it by less than ``reach`` minutes is, with probability
    ``effort``, moved on in the last quarter of an hour before the deadline: the share within the target jumps, the
    histogram grows a spike just under it, and the typical wait barely moves."""
    rng = np.random.default_rng(seed)
    t0 = 160.0 * np.exp(0.5 * rng.standard_normal(n))
    moved = (t0 > target) & (t0 < target + reach) & (rng.random(n) < effort)
    t1 = np.where(moved, target - rng.uniform(0.0, 15.0, n), t0)
    return {"before": t0, "after": t1, "within_before": float(np.mean(t0 <= target)),
            "within_after": float(np.mean(t1 <= target)), "moved": float(moved.mean()),
            "median_before": float(np.median(t0)), "median_after": float(np.median(t1)),
            "spike_before": float(np.mean((t0 > target - 15) & (t0 <= target))),
            "spike_after": float(np.mean((t1 > target - 15) & (t1 <= target)))}


# ---------------------------------------------------------------------------------------------------------------
# the record

def cbo_record() -> dict:
    """CBO's deficit projections since 1984 (the Data Room's ``cbo``): errors by year of the projection, in percent of
    GDP, after removing the effects of laws enacted later (CBO's own adjustment); and each baseline's path."""
    from explainer.economics import data  # noqa: PLC0415

    D = data.cbo()
    rows = D["projections"]
    by = {}
    for r in rows:
        by.setdefault(r["year_number"], []).append(r["error_pct_gdp"])
    horizon = []
    for k in sorted(by):
        e = np.array(by[k])
        horizon.append({"year": k, "n": len(e), "mean": float(e.mean()), "mae": float(np.abs(e).mean()),
                        "rmse": float(np.sqrt(np.mean(e ** 2)))})
    paths = {}
    for r in rows:
        paths.setdefault(r["baseline"], []).append((r["fiscal_year"], 100.0 * r["projected"] / r["gdp"],
                                                    100.0 * r["adjusted"] / r["gdp"]))
    return {"horizon": horizon, "paths": {k: sorted(v) for k, v in paths.items()}, "actual": D["actual"],
            "stats": D["stats"]}


# ---------------------------------------------------------------------------------------------------------------
# the frontier

def distributional_weights(income, median: float, eps: float = 1.4):
    """Weights for a dollar to people at each income: (median/income)^eps, the elasticity of the marginal utility of
    income (1.4 in OMB's 2023 Circular A-4, since rescinded)."""
    return (median / np.asarray(income, float)) ** eps


def harberger_check(t: float = 0.1) -> dict:
    """Small helper for tests and the lab: the general-equilibrium deadweight loss against the triangle."""
    w = cge_welfare(t)
    return {"dwl": w["dwl"], "triangle": w["harberger"], "ratio": w["dwl"] / w["harberger"]}


__all__ = [n for n in dir() if not n.startswith("_") and n not in ("np", "optimize", "annotations")]
