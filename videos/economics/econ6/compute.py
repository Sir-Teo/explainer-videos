"""Precompute every number in Part 6 of *Economics, Built* ("Demand").

    python -m videos.economics.econ6.compute            # everything missing (seconds)
    python -m videos.economics.econ6.compute --force vouchers

Results are cached in ``.cache/econ6/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.  Data: the Data Room
(``explainer.economics.data``: personal consumption expenditures by type of product, 1929-2025; the transcribed tables
of Jensen and Miller, Hausman, Costa, Engel and Houthakker, the USDA's quintiles, Jaravel, the BLS).  Models: Agora's
demand systems (``agora.demand``), with the Island's Part 6 truths.  Every random draw is seeded.

Items:
    bo           Bo (Cobb-Douglas, 60% on fish) as fish falls from $10 to $6: the price-consumption curve, the demand
                 curve, the Engel curve, homogeneity, and the Hicks and Slutsky decompositions
    playit       a week's food on $21: the calorie line, the budget lines before and after coconuts go up
    diet         the subsistence household: its three zones, the coconut demand curve at fixed income, the coconut
                 Engel curve, the Slutsky equation in elasticities at the Play-it bundle
    vouchers     Jensen and Miller's design run on 1,300 simulated island households: table-3 regressions, the
                 kernel-weighted curve across coconut calorie shares, and the planted elasticities by zone
    hunan        Jensen and Miller's own numbers (transcribed)
    duality      the four functions for Bo; the expenditure function against the price of fish and its tangent;
                 the identities checked on four systems
    loop         integrability: compensated income round a loop of prices, symmetric and circular tastes
    engel        Engel curves: America's food share against real spending per head, 1929-2025; the 2024 income
                 quintiles; linear expenditure system curves for a necessity and a luxury
    hamilton     Hamilton's method on six simulated island surveys with a planted 1% a year bias in the price index
    welfare      CV, EV and Marshall's surplus for Bo; the coconut tax with Hausman's exact surplus and Willig's gap
    living       Laspeyres, Paasche and the true cost-of-living index; the Cheerios virtual price
    survey       the AIDS estimated on 6,000 simulated island households: unrestricted, homogeneous, symmetric
    cpi          substitution in the official index, on fifteen kinds of American spending, 2000-2025
    ramsey       Ramsey's inverse-elasticity rule for two goods
    frontier     inflation by income group (Jaravel); Feenstra's variety correction
    dial         the dials' rows: staples' price elasticities and food's income elasticity
    film         the intermission's data film: a century of relative prices and quantities, fifteen goods
    melody       its data melody: the relative price of recreational goods, year by year
"""

from __future__ import annotations

import numpy as np

from explainer.ai.cache import Cache
from explainer.economics import data, dials, island, score
from explainer.economics.agora import demand as dm
from explainer.economics.agora import indices
from explainer.economics.data import tables

CACHE = Cache("econ6")
load = CACHE.load
TRUTH = island.truths(6)


def _diet(**kw) -> dm.Diet:
    d = TRUTH["diet"]
    base = dict(cs=d["coconut_kcal"], cf=d["fish_kcal"], need=d["need"], beta=d["beta"], s0=d["s0"],
                other_share=d["other_share"], other_kcal=d["other_kcal"])
    base.update(kw)
    return dm.Diet(**base)


# ---------------------------------------------------------------------------------------------------------------
# Bo and the demand function

def compute_bo() -> dict:
    b = TRUTH["bo"]
    sys = dm.CobbDouglas((b["a"], 1 - b["a"]))
    m, py = b["income"], b["coconut"]
    p0, p1 = b["fish"]
    prices = np.linspace(2.5, 15.0, 60)
    pcc = np.array([sys.x([p, py], m) for p in prices])                 # the price-consumption curve
    incomes = np.linspace(10, 110, 41)
    icc = np.array([sys.x([p0, py], mm) for mm in incomes])             # the income-consumption curve
    dec = {how: dm.decompose(sys, 0, [p0, py], [p1, py], m, how) for how in ("hicks", "slutsky")}
    u0, u1 = sys.v([p0, py], m), sys.v([p1, py], m)
    xs = np.linspace(0.5, 13, 300)

    def ic(u):
        a = b["a"]
        return (u / xs ** a) ** (1 / (1 - a))

    el = dm.elasticities(sys, np.array([p0, py]), m)
    double = sys.x([2 * p0, 2 * py], 2 * m)
    # the Slutsky equation at a small change, Bo's numbers
    dp = 0.01
    dx = (sys.x([p0 + dp, py], m)[0] - sys.x([p0 - dp, py], m)[0]) / (2 * dp)
    dh = (sys.h([p0 + dp, py], u0)[0] - sys.h([p0 - dp, py], u0)[0]) / (2 * dp)
    dxm = (sys.x([p0, py], m + 0.01)[0] - sys.x([p0, py], m - 0.01)[0]) / 0.02
    x0 = sys.x([p0, py], m)[0]
    return {"a": b["a"], "m": m, "py": py, "p0": p0, "p1": p1, "prices": prices, "pcc": pcc, "incomes": incomes,
            "icc": icc, "A": dec["hicks"]["A"], "C": dec["hicks"]["C"], "B_hicks": dec["hicks"]["B"],
            "B_slutsky": dec["slutsky"]["B"], "m_hicks": dec["hicks"]["m_comp"], "m_slutsky": dec["slutsky"]["m_comp"],
            "sub_hicks": dec["hicks"]["substitution"], "inc_hicks": dec["hicks"]["income"],
            "sub_slutsky": dec["slutsky"]["substitution"], "inc_slutsky": dec["slutsky"]["income"],
            "u0": u0, "u1": u1, "xs": xs, "ic0": ic(u0), "ic1": ic(u1),
            "own": float(el["marshall"][0, 0]), "cross": float(el["marshall"][1, 0]), "income_el": float(el["income"][0]),
            "hicks_own": float(el["hicks"][0, 0]), "share": float(el["shares"][0]), "double": double,
            "slutsky_check": {"dx_dp": dx, "dh_dp": dh, "x_dx_dm": x0 * dxm, "x0": x0}}


# ---------------------------------------------------------------------------------------------------------------
# the subsistence diet

def compute_playit() -> dict:
    t = TRUTH["playit"]
    d = _diet(other_share=0.0, other_kcal=0.0)
    m, pf = t["budget"], t["fish"]
    (c0, c1) = t["coconut"]
    b0, b1 = d.choose(c0, pf, m), d.choose(c1, pf, m)
    assert b0["zone"] == b1["zone"] == "subsistence"
    # calories per dollar and the trade: a fish given up frees $2, which buys 2 / p coconuts
    return {"m": m, "pf": pf, "c0": c0, "c1": c1, "need": d.need, "cs": d.cs, "cf": d.cf,
            "before": (b0["f"], b0["s"]), "after": (b1["f"], b1["s"]),
            "kcal_per_dollar": {"coconut0": d.cs / c0, "coconut1": d.cs / c1, "fish": d.cf / pf},
            "fish_only_kcal": m / pf * d.cf, "coconut_only_kcal": m / c0 * d.cs,
            "elasticity_arc": float(dm.arc_pct(b0["s"], b1["s"]) / dm.arc_pct(c0, c1))}


def compute_diet() -> dict:
    t = TRUTH["playit"]
    v = TRUTH["vouchers"]
    d0 = _diet(other_share=0.0, other_kcal=0.0)       # the Play-it household
    m, pf = t["budget"], t["fish"]
    # the coconut demand curve at $21 a week: standard, subsistence, deprived
    ps = np.linspace(0.45, 2.3, 400)
    s = np.array([d0.staple(p, pf, m) for p in ps])
    zones = [d0.choose(p, pf, m)["zone"] for p in ps]
    # the coconut Engel curve at $1.20
    incomes = np.linspace(4, 45, 400)
    se = np.array([d0.staple(t["coconut"][0], pf, mm) for mm in incomes])
    fe = np.array([d0.choose(t["coconut"][0], pf, mm)["f"] for mm in incomes])
    ze = [d0.choose(t["coconut"][0], pf, mm)["zone"] for mm in incomes]
    lo, hi = d0.zone_bounds(t["coconut"][0], pf)
    # the Slutsky equation in elasticities at the Play-it bundle
    c0 = t["coconut"][0]
    b = d0.choose(c0, pf, m)
    eps = d0.elasticity(c0, pf, m)
    dm_ = 1e-4 * m
    eta = (d0.staple(c0, pf, m + dm_) - d0.staple(c0, pf, m - dm_)) / (2 * dm_) * m / b["s"]
    share = c0 * b["s"] / m
    # Slutsky compensation: give the money to buy the old bundle at the new price; the household keeps it
    comp = d0.choose(t["coconut"][1], pf, t["coconut"][1] * b["s"] + pf * b["f"])
    # the island diet (with oil and greens): zones and calorie shares across incomes
    dI = _diet()
    inc = np.linspace(8, 40, 200)
    shares = np.array([dI.calorie_share(v["coconut"], v["fish"], mm) for mm in inc])
    elas = np.array([dI.elasticity(v["coconut"], v["fish"], mm) for mm in inc])
    zI = [dI.choose(v["coconut"], v["fish"], mm)["zone"] for mm in inc]
    return {"ps": ps, "s": s, "zones": zones, "incomes": incomes, "se": se, "fe": fe, "ze": ze, "lo": lo, "hi": hi,
            "eps": float(eps), "eta": float(eta), "share": float(share), "eps_hicks": float(eps + share * eta),
            "giffen": d0.giffen_elasticity(c0, pf), "comp_bundle": (comp["f"], comp["s"]), "bundle": (b["f"], b["s"]),
            "island_inc": inc, "island_share": shares, "island_elas": elas, "island_zone": zI,
            "island_bounds": dI.zone_bounds(v["coconut"], v["fish"]), "island_giffen": dI.giffen_elasticity(
                v["coconut"], v["fish"])}


def compute_vouchers() -> dict:
    v = TRUTH["vouchers"]
    ex = dm.voucher_experiment(_diet(), v["households"], v["villages"], v["cuts"], v["coconut"], v["fish"],
                               v["median"], v["sigma"], v["need_sd"], v["report_sd"], v["income_sd"], v["seed"])
    sh = ex["share0"]

    def reg(mask, y="dS"):
        r = dm.fe_regression(ex[y][mask], ex["dP"][mask], ex["cell"][mask], ex["hh"][mask])
        return (r["b"], r["se"], r["n"])

    allm = np.ones_like(sh, bool)
    rows = {"full": reg(allm), "share_le_080": reg(sh <= 0.80), "share_gt_080": reg(sh > 0.80),
            "share_060_080": reg((sh >= 0.60) & (sh <= 0.80)), "fish_060_080": reg((sh >= 0.60) & (sh <= 0.80), "dF")}
    grid = np.round(np.arange(0.40, 0.951, 0.025), 3)
    loc = dm.local_elasticity(ex, grid, 0.10)
    z = ex["zone"]
    share_hh = ex["share0_hh"]
    zone_elas = {k: float(ex["elasticity"][z == k].mean()) for k in ("standard", "subsistence", "deprived")}
    zone_n = {k: int((z == k).sum()) for k in ("standard", "subsistence", "deprived")}
    zone_share = {k: (float(np.percentile(share_hh[z == k], 10)), float(np.percentile(share_hh[z == k], 90)))
                  for k in ("standard", "subsistence", "deprived")}
    # the household-level truth across shares, for the overlay: a smoothed mean of the planted elasticities
    true_curve = []
    for g in grid:
        w = np.where(np.abs((share_hh - g) / 0.10) < 1, (1 - ((share_hh - g) / 0.10) ** 2) ** 2, 0.0)
        true_curve.append(float((w * ex["elasticity"]).sum() / max(w.sum(), 1e-12)))
    rng = np.random.default_rng(7)
    pick = rng.choice(v["households"], 260, replace=False)
    return {"rows": rows, "grid": grid, "b": loc["b"], "lo": loc["lo"], "hi": loc["hi"], "true_curve": true_curve,
            "zone_elas": zone_elas, "zone_n": zone_n, "zone_share": zone_share, "households": v["households"],
            "villages": v["villages"], "cuts": v["cuts"], "price": v["coconut"],
            "scatter_share": share_hh[pick], "scatter_zone": z[pick].tolist(), "scatter_elas": ex["elasticity"][pick],
            "mean_share": float(share_hh.mean()), "planted_giffen": _diet().giffen_elasticity(v["coconut"], v["fish"])}


def compute_hunan() -> dict:
    return dict(tables.JENSEN_MILLER_2008.data)


# ---------------------------------------------------------------------------------------------------------------
# duality and integrability

def compute_duality() -> dict:
    b = TRUTH["bo"]
    sys = dm.CobbDouglas((b["a"], 1 - b["a"]))
    m, py, p0 = b["income"], b["coconut"], b["fish"][0]
    u0 = sys.v([p0, py], m)
    px = np.linspace(1.0, 30.0, 300)
    e = np.array([sys.e([p, py], u0) for p in px])
    A = sys.x([p0, py], m)
    passive = px * A[0] + py * A[1]                 # the cost of the old bundle: the tangent at p0
    h = np.array([sys.h([p, py], u0)[0] for p in px])
    systems = {"Cobb-Douglas": dm.CobbDouglas((0.5, 0.3, 0.2)), "CES, sigma 0.5": dm.CES((0.5, 0.3, 0.2), 0.5),
               "linear expenditure": dm.StoneGeary((0.3, 0.5, 0.2), (5.0, 2.0, 1.0)),
               "AIDS": dm.AIDS(alpha0=np.log(100.0))}
    p, mm = np.array([2.0, 3.0, 1.5]), 100.0
    errs = {k: dm.duality_errors(s, p, mm) for k, s in systems.items()}
    worst = {k: float(max(v.values())) for k, v in errs.items()}
    return {"px": px, "e": e, "passive": passive, "h": h, "p0": p0, "py": py, "u0": u0, "m": m, "A": A,
            "errors": errs, "worst": worst, "x_fish": float(A[0])}


def compute_loop() -> dict:
    t = TRUTH["loop"]
    out = {"radius": t["radius"]}
    path = dm.circle_path((0.0, 0.0), t["radius"], steps=721)
    for key in ("symmetric", "circular"):
        g = dm.AIDS(alpha=t["alpha"], beta=(0.0, 0.0, 0.0), gamma=t[key])
        lm = dm.loop_income(g.shares, path)
        S = dm.slutsky_matrix(g, np.ones(3), 100.0)
        rep = dm.slutsky_report(S, np.ones(3))
        ga = np.array(t[key])
        out[key] = {"log_m": lm, "gap": float(lm[-1]), "green": float((ga[1, 0] - ga[0, 1]) * np.pi * t["radius"] ** 2),
                    "S": S, "asymmetry": rep["asymmetry"], "gamma": ga}
    out["path"] = path[:, :2]
    # two goods: homogeneity and adding up make the Slutsky matrix symmetric by themselves
    two = dm.AIDS(alpha=(0.6, 0.4), beta=(0.0, 0.0), gamma=((-0.05, 0.05), (0.05, -0.05)))
    out["two_asymmetry"] = dm.slutsky_report(dm.slutsky_matrix(two, np.ones(2), 50.0), np.ones(2))["asymmetry"]
    return out


# ---------------------------------------------------------------------------------------------------------------
# Engel curves

def _pce():
    d = data.pce_by_type()
    P, X = d["prices"], d["quantities"]
    years = d["years"]
    agg = indices.chained(P, X, "fisher")
    agg = agg / agg[years.index(2017)]
    return d, P, X, years, agg


def compute_engel() -> dict:
    d, P, X, years, agg = _pce()
    E = np.asarray(d["spending"], float)                     # dollars per head, by category
    spend = E.sum(1)
    k = d["codes"].index("DFXA")
    food = E[:, k] / spend
    real = spend / agg                                       # real spending per head, 2017 dollars
    wl = dm.working_leser(food, real)
    eta_1929, eta_2025 = wl["eta_at"](food[0]), wl["eta_at"](food[-1])
    q = tables.ERS_FOOD_2024.data
    inc = {g: q[g]["food"] / q[g]["share"] for g in ("lowest", "middle", "highest")}
    el_bm = np.log(q["middle"]["food"] / q["lowest"]["food"]) / np.log(inc["middle"] / inc["lowest"])
    el_mt = np.log(q["highest"]["food"] / q["middle"]["food"]) / np.log(inc["highest"] / inc["middle"])
    el_all = np.log(q["highest"]["food"] / q["lowest"]["food"]) / np.log(inc["highest"] / inc["lowest"])
    # the century as one Engel curve: food's relative price barely moved, so the change is mostly an income effect
    rel_food = (P[:, k] / agg)
    q_ratio = X[-1, k] / X[0, k]
    century_el = float(np.log(q_ratio) / np.log(real[-1] / real[0]))
    les = dm.StoneGeary((0.15, 0.85), (60.0, 0.0))
    ms = np.linspace(80, 600, 120)
    les_x = np.array([les.x([1.0, 1.0], mm) for mm in ms])
    return {"years": years, "food_share": food, "real": real, "wl_a": wl["a"], "wl_b": wl["b"], "wl_se": wl["se_b"],
            "eta_1929": float(eta_1929), "eta_2025": float(eta_2025), "quintile_income": inc,
            "quintile_food": {g: q[g]["food"] for g in inc}, "quintile_share": {g: q[g]["share"] for g in inc},
            "el_bottom_middle": float(el_bm), "el_middle_top": float(el_mt), "el_all": float(el_all),
            "les_m": ms, "les_x": les_x, "real_ratio": float(real[-1] / real[0]), "food_q_ratio": float(q_ratio),
            "food_rel_ratio": float(rel_food[-1] / rel_food[0]), "century_el": century_el}


def compute_hamilton() -> dict:
    h = TRUTH["hamilton"]
    rng = np.random.default_rng(h["seed"])
    W, M, Y, R, TRUE = [], [], [], [], []
    for t in h["years"]:
        region_rel = rng.normal(0, h["food_price_sd"], h["regions"])     # log relative price of food, by region
        region = np.arange(h["households"]) % h["regions"]
        lrel = region_rel[region]
        ly = np.log(h["median"]) + h["growth"] * t + h["sigma"] * rng.standard_normal(h["households"])
        w = h["a"] + h["b"] * (ly - np.log(h["median"])) + h["g"] * lrel + rng.normal(0, h["noise"],
                                                                                   h["households"])
        measured = ly - h["bias"] * t          # the official index rises too fast, so measured real income lags
        W.append(w)
        M.append(np.exp(measured))
        Y.append(np.full(h["households"], t))
        R.append(lrel)
        TRUE.append(ly)
    W, M, Y, R = map(np.concatenate, (W, M, Y, R))
    fit = dm.hamilton_drift(W, M / h["median"], Y, R)
    # Engel curves drawn on measured income, one per survey (binned means)
    curves = []
    edges = np.linspace(np.log(80), np.log(1200), 15)
    for t in h["years"]:
        k = Y == t
        lm = np.log(M[k])
        mids, means = [], []
        for a, b in zip(edges[:-1], edges[1:]):
            j = (lm >= a) & (lm < b)
            if j.sum() > 25:
                mids.append(float(np.exp((a + b) / 2)))
                means.append(float(W[k][j].mean()))
        grid = np.exp(np.linspace(np.log(120), np.log(800), 30))
        k_t = fit["years"].index(t)
        fitted = fit["a"] + fit["b"] * np.log(grid / h["median"]) + fit["dummies"][k_t]
        curves.append({"year": t, "m": mids, "w": means, "grid": grid, "fit": fitted})
    years = list(h["years"])
    slope = np.polyfit(years, fit["cumulative_bias"], 1)[0]
    return {"years": years, "bias": h["bias"], "recovered": fit["cumulative_bias"].tolist(),
            "per_year": float(slope), "b": fit["b"], "curves": curves,
            "costa": tables.COSTA_2001.data["bias_per_year"], "hamilton": tables.COSTA_2001.data["hamilton_2001"]}


# ---------------------------------------------------------------------------------------------------------------
# welfare and the cost of living

def compute_welfare() -> dict:
    b = TRUTH["bo"]
    sys = dm.CobbDouglas((b["a"], 1 - b["a"]))
    m, py = b["income"], b["coconut"]
    p0, p1 = b["fish"]
    # a fall in the price of fish: gains (positive numbers)
    cvb = -dm.cv(sys, [p0, py], [p1, py], m)
    evb = -dm.ev(sys, [p0, py], [p1, py], m)
    csb = -dm.cs(sys, 0, [p0, py], [p1, py], m)
    u0, u1 = sys.v([p0, py], m), sys.v([p1, py], m)
    ps = np.linspace(4.0, 12.0, 200)
    marsh = np.array([sys.x([p, py], m)[0] for p in ps])
    h0 = np.array([sys.h([p, py], u0)[0] for p in ps])
    h1 = np.array([sys.h([p, py], u1)[0] for p in ps])
    t = TRUTH["tax"]
    L = dm.LinearDemand(t["alpha"], t["delta"], t["c"])
    x0 = L.x(t["price"], t["income"])
    eta = t["delta"] * t["income"] / x0
    taxes = []
    for tx in t["taxes"]:
        r = L.tax(t["price"], tx, t["income"])
        r["t"] = tx
        r["willig"] = dm.willig_gap(eta, r["cs"], t["income"])
        r["cv_gap"] = (r["cv"] - r["cs"]) / r["cs"]
        taxes.append(r)
    pt = np.linspace(0.6, 2.4, 100)
    k0 = L.k(t["price"], t["income"])
    return {"cv": cvb, "ev": evb, "cs": csb, "ps": ps, "marshall": marsh, "hicks0": h0, "hicks1": h1, "p0": p0,
            "p1": p1, "m": m, "eta_bo": 1.0, "willig_bo": dm.willig_gap(1.0, csb, m), "cv_gap_bo": (csb - cvb) / csb,
            "tax": t, "x0": x0, "eta": eta, "share": t["price"] * x0 / t["income"], "taxes": taxes,
            "tax_pt": pt, "tax_marshall": L.x(pt, t["income"]), "tax_hicks": np.array([L.h(p, k0) for p in pt])}


def compute_living() -> dict:
    b = TRUTH["bo"]
    out = {}
    for key, sys in (("bo", dm.CobbDouglas((b["a"], 1 - b["a"]))), ("ces_low", dm.CES((0.6, 0.4), 0.3)),
                     ("ces_high", dm.CES((0.6, 0.4), 3.0))):
        p0 = np.array([b["fish"][0], b["coconut"]])
        p1 = np.array([b["fish"][1], b["coconut"]])
        m = b["income"]
        u0, u1 = sys.v(p0, m), sys.v(p1, m)
        out[key] = {"laspeyres": dm.laspeyres(p0, p1, sys.x(p0, m)), "paasche": dm.paasche(p0, p1, sys.x(p1, m)),
                    "coli0": dm.coli(sys, p0, p1, u0), "coli1": dm.coli(sys, p0, p1, u1)}
    # a rise as well as a fall, for Bo: fish from $10 to $15
    sys = dm.CobbDouglas((b["a"], 1 - b["a"]))
    p0, p2 = np.array([10.0, 6.0]), np.array([15.0, 6.0])
    m = b["income"]
    out["rise"] = {"laspeyres": dm.laspeyres(p0, p2, sys.x(p0, m)), "coli": dm.coli(sys, p0, p2, sys.v(p0, m)),
                   "paasche": dm.paasche(p0, p2, sys.x(p2, m))}
    hz = tables.HAUSMAN_1997.data
    # a schematic straight demand curve through the observed price with Hausman's virtual price as its choke price
    q = 1.0
    out["cheerios"] = {"virtual": hz["virtual_price"], "price": hz["average_price"], "cs_year": hz["cs_us_year_million"],
                       "per_person": hz["cs_per_person_year"], "imperfect": hz["cs_imperfect_us_year_million"],
                       "cpi_over": hz["cereal_cpi_overstated"], "cpi_over_imperfect":
                       hz["cereal_cpi_overstated_imperfect"], "brands": hz["new_brands_1980_92"],
                       "existing": hz["existing_brands"], "q": q}
    boskin = dials.DIALS["cpi_bias"].estimates[0]
    out["boskin"] = {"total": boskin.value, "lo": boskin.lo, "hi": boskin.hi, "substitution": 0.40, "outlets": 0.10,
                     "new_quality": 0.60}
    return out


# ---------------------------------------------------------------------------------------------------------------
# demand systems

def compute_survey() -> dict:
    s = TRUTH["survey"]
    a0 = float(np.log(s["median"]))
    truth = dm.AIDS(alpha=s["alpha"], beta=s["beta"], gamma=s["gamma"], alpha0=a0)
    sv = dm.Survey(truth, s["villages"], s["months"], s["per_cell"], s["price_sd"], s["median"], s["m_sigma"],
                   s["share_sd"], s["seed"])
    d = sv.draw()
    p, m = np.ones(3), s["median"]
    out = {"goods": list(s["goods"]), "n": int(len(d["W"])), "cells": d["cells"], "truth": {}}
    te = truth.elasticities(p, m)
    out["truth"] = {"marshall": te["marshall"], "income": te["income"], "hicks": te["hicks"], "shares": te["shares"]}
    for r in ("none", "symmetry"):
        f = dm.aids_fit(d["W"], d["logP"], d["logm"], restrict=r, alpha0=a0)
        el = f["model"].elasticities(p, m)
        out[r] = {"marshall": el["marshall"], "income": el["income"], "hicks": el["hicks"], "alpha": f["alpha"],
                  "beta": f["beta"], "gamma": f["gamma"], "tests": f["tests"]}
    # a scatter for the screen: fish's share against log spending, a sample of households
    rng = np.random.default_rng(3)
    k = rng.choice(len(d["W"]), 500, replace=False)
    out["scatter"] = {"logm": d["logm"][k], "w": d["W"][k]}
    return out


def compute_cpi() -> dict:
    d, P, X, years, agg = _pce()
    i0 = years.index(2000)
    Ps, Xs = P[i0:], X[i0:]
    lasp = indices.fixed_base(Ps, Xs, "laspeyres")
    torn = indices.chained(Ps, Xs, "tornqvist")
    fish = indices.chained(Ps, Xs, "fisher")
    n = len(Ps) - 1
    gap = (np.log(lasp[-1]) - np.log(torn[-1])) / n
    # the same over the century, base 1929
    lasp_c = indices.fixed_base(P, X, "laspeyres")
    torn_c = indices.chained(P, X, "tornqvist")
    return {"years": years[i0:], "laspeyres": lasp, "tornqvist": torn, "fisher": fish, "gap_per_year": float(gap),
            "century_ratio": float(lasp_c[-1] / torn_c[-1]),
            "century_gap": float((np.log(lasp_c[-1]) - np.log(torn_c[-1])) / (len(P) - 1)),
            "methods": tables.BLS_CPI_METHODS.data}


def compute_ramsey() -> dict:
    # two goods with demand elasticities from the dial's range: a staple (-0.3) and a treat (-1.2); raise $10 of
    # revenue with the least deadweight loss (small taxes: the loss is about 1/2 eps t^2 p x)
    e = np.array([-0.3, -1.2])
    spend = np.array([100.0, 100.0])
    R = 10.0
    # minimize sum 1/2 |e| t^2 spend subject to sum t spend = R  ->  t proportional to 1 / |e|
    t = (1 / np.abs(e)) / np.sum(spend / np.abs(e)) * R
    loss = 0.5 * np.abs(e) * t ** 2 * spend
    t_u = np.full(2, R / spend.sum())
    loss_u = 0.5 * np.abs(e) * t_u ** 2 * spend
    return {"elasticity": e, "spend": spend, "revenue": R, "t": t, "loss": float(loss.sum()), "t_uniform": t_u,
            "loss_uniform": float(loss_u.sum())}


def compute_frontier() -> dict:
    j = tables.JARAVEL_2019.data
    lam = np.linspace(0.80, 1.0, 81)
    sig = (2.0, 4.0, 8.0)
    curves = {f"{s:g}": [dm.feenstra(1.0, l_, s) for l_ in lam] for s in sig}
    return {"jaravel": j, "lam": lam, "sigmas": sig, "curves": curves, "example": dm.feenstra(1.0, 0.95, 4.0)}


def compute_dial() -> dict:
    out = {}
    for key in ("elasticity_staples", "engel_food"):
        dl = dials.DIALS[key]
        out[key] = [(e.who, e.year, e.design, e.sample, e.value, e.lo, e.hi) for e in dl.estimates]
    return out


# ---------------------------------------------------------------------------------------------------------------
# the intermission

FILM_SECONDS = 40.0
MELODY_SECONDS = 55.0


def film_time(k: int, n: int) -> float:
    """When the data film reaches the k-th year (0-based) of n."""
    return 1.5 + FILM_SECONDS * k / (n - 1)


def compute_film() -> dict:
    d, P, X, years, agg = _pce()
    R = P / agg[:, None]
    R = R / R[0]                                  # relative prices, 1929 = 1
    Q = X / X[0]                                  # quantities per head, 1929 = 1
    n = len(years)
    dr, dq = np.log(R[-1]), np.log(Q[-1])
    slope, icept = np.polyfit(dr, dq, 1)
    return {"years": years, "codes": d["codes"], "names": d["names"], "rel": R, "qty": Q,
            "times": [film_time(k, n) for k in range(n)], "slope": float(slope), "intercept": float(icept),
            "corr": float(np.corrcoef(dr, dq)[0, 1]), "real_ratio": float(((P[-1] @ X[-1]) / agg[-1]) /
                                                                        ((P[0] @ X[0]) / agg[0]))}


def compute_melody() -> dict:
    from explainer.music.monochord.audio import Clip, ClipStore

    f = compute_film()
    k = f["codes"].index("DREQ")
    rel = np.array(f["rel"])[:, k]
    times = f["times"]
    mel = score.data_melody(rel, MELODY_SECONDS, times=times, act=2, log=True, low=45, high=84)
    events = {"film_end": times[-1] + 6.0, "first": times[0], "half": times[len(times) // 2]}
    clip = Clip(mel["y"], score.SR, events=events,
                notes=[{"t": float(t), "dur": 0.3, "hz": score.hz(nn), "name": str(y)}
                       for t, nn, y in zip(times, mel["notes"], f["years"])],
                meta={"label": "a century of relative prices: the price of recreational goods relative to all "
                               "spending, 1929-2025, as a tune (computed)", "kind": "synthesized"})
    ClipStore("econ6").save("intermission.melody", clip)
    return {"times": times, "notes": mel["notes"], "rel": rel, "seconds": MELODY_SECONDS}


ITEMS = {
    "bo": compute_bo,
    "playit": compute_playit,
    "diet": compute_diet,
    "vouchers": compute_vouchers,
    "hunan": compute_hunan,
    "duality": compute_duality,
    "loop": compute_loop,
    "engel": compute_engel,
    "hamilton": compute_hamilton,
    "welfare": compute_welfare,
    "living": compute_living,
    "survey": compute_survey,
    "cpi": compute_cpi,
    "ramsey": compute_ramsey,
    "frontier": compute_frontier,
    "dial": compute_dial,
    "film": compute_film,
    "melody": compute_melody,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
