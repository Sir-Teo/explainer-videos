"""Precompute every number in Part 9 of *Economics, Built* ("The Invisible Hand, Proved").

    python -m videos.economics.econ9.compute            # everything missing (about a minute)
    python -m videos.economics.econ9.compute --force core

Results are cached in ``.cache/econ9/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.  Data: the Data Room
(``explainer.economics.data``: Brent and West Texas Intermediate crude, monthly, via FRED; the World Bank's WDI for
price levels; transcribed tables from Radford 1945, Edgeworth 1881, Hsieh and Klenow 2009, Bils, Klenow and Ruane
2021, and Kehoe 2014).  Models: Agora's general equilibrium (``agora.ge``), with the Island's Part 9 truths.  Every
random draw is seeded.

Items:
    box          the Edgeworth box: endowment, indifference curves, the lens, the contract curve, the equilibrium,
                 offer curves; the Play-it trades
    core         the core of the replicated box economy, and a blocking coalition
    welfare      the first welfare theorem checked; the second: a target allocation, its price and the transfer
    fact         the law of one price: Brent against WTI, and price levels against income across countries
    simplex      Sperner's labelling of the price simplex and Scarf's walk, three goods
    dynamics     tatonnement in the three-good economy, and Scarf's cycle
    island       the whole Island cleared at once: Newton against the auctioneer
    crusoe       the Robinson Crusoe economy, planned and decentralized
    smd          three equilibria, and which are stable
    risk         Arrow securities against a bond alone
    plan         Kantorovich's linear programme and its resolving multipliers
    dial         misallocation: Hsieh and Klenow's rows, the lognormal formula, plants simulated
    nafta        the 1992 forecasts of NAFTA against 1989-2009 (Kehoe's table)
    huts         the housing market and top trading cycles
    film         the intermission's data film: Brent and WTI, month by month
    melody       its data melody: Brent's premium over WTI, year by year
"""

from __future__ import annotations

import numpy as np

from explainer.ai.cache import Cache
from explainer.economics import data, dials, island, score
from explainer.economics.agora import ge
from explainer.economics.data import tables

CACHE = Cache("econ9")
load = CACHE.load
TRUTH = island.truths(9)


def traders_box() -> tuple[ge.Trader, ge.Trader]:
    b = TRUTH["box"]
    A = ge.Trader((b["ana"]["a"], 1 - b["ana"]["a"]), b["ana"]["e"], name="Ana")
    B = ge.Trader((b["bo"]["a"], 1 - b["bo"]["a"]), b["bo"]["e"], name="Bo")
    return A, B


def traders_three() -> list[ge.Trader]:
    return [ge.Trader(a, e, name=n) for n, a, e in TRUTH["three"]["traders"]]


def traders_island() -> list[ge.Trader]:
    t = TRUTH["island"]
    rng = np.random.default_rng(t["seed"])
    n = len(t["goods"])
    out = []
    for k in range(t["people"]):
        sig = float(np.exp(rng.uniform(np.log(t["sigma"][0]), np.log(t["sigma"][1]))))
        a = rng.dirichlet(np.ones(n) * 2)
        e = np.zeros(n)
        own = rng.choice(n, size=2, replace=False)
        e[own] = rng.uniform(0.5, 3.0, 2)
        out.append(ge.Trader(tuple(a), tuple(e), kind="ces", rho=1 - 1 / sig, name=f"islander {k + 1}"))
    return out


# ---------------------------------------------------------------------------------------------------------------
# the box

def compute_box() -> dict:
    A, B = traders_box()
    X = np.add(A.e, B.e)
    eq = ge.box_equilibrium(A, B)
    uA0 = A.utility(A.e)
    uB0 = B.utility(B.e)
    xs = np.linspace(0.05, X[0] - 0.05, 400)
    lo, hi = ge.lens_ends(A, B)
    cc_x = np.linspace(0.02, X[0] - 0.02, 400)
    # A's indifference curve through the endowment, and B's (in A's coordinates)
    ia = ge.cd_indifference(A.a[0], uA0, xs)
    ib = X[1] - ge.cd_indifference(B.a[0], uB0, X[0] - xs)
    # through the equilibrium
    xa, xb = np.array(eq["xA"]), np.array(eq["xB"])
    ia_eq = ge.cd_indifference(A.a[0], A.utility(xa), xs)
    ib_eq = X[1] - ge.cd_indifference(B.a[0], B.utility(xb), X[0] - xs)
    ps = np.geomspace(0.15, 8.0, 300)
    oa = ge.offer_curve(A, ps)
    obB = ge.offer_curve(B, ps)
    # Play it: four proposed trades from the endowment (fish Ana gives, coconut bundles she gets)
    props = {"A": (2.0, 1.0), "B": (4.2, 4.3), "C": (2.0, 6.0), "D": (6.0, 1.5)}
    play = {}
    for k, (give, get) in props.items():
        a_ = np.array([A.e[0] - give, A.e[1] + get])
        b_ = X - a_
        dA = A.utility(a_) - uA0
        dB = B.utility(b_) - uB0
        on_cc = abs(a_[1] - float(ge.contract_curve(A, B, a_[0]))) < 0.08
        play[k] = {"give": give, "get": get, "xA": a_.tolist(), "ana_gains": bool(dA > 0), "bo_gains": bool(dB > 0),
                   "on_cc": bool(on_cc), "dA": float(dA), "dB": float(dB)}
    # the competitive price line through the endowment
    p = eq["p"]
    return {"X": X.tolist(), "eA": list(A.e), "eB": list(B.e), "aA": A.a[0], "aB": B.a[0], "p": p,
            "xA": eq["xA"], "xB": eq["xB"], "xs": xs, "ia": ia, "ib": ib, "ia_eq": ia_eq, "ib_eq": ib_eq,
            "cc_x": cc_x, "cc_y": ge.contract_curve(A, B, cc_x), "lens": [lo, hi],
            "lens_y": [float(ge.contract_curve(A, B, lo)), float(ge.contract_curve(A, B, hi))],
            "offer_A": [oa[0], oa[1]], "offer_B": [X[0] - obB[0], X[1] - obB[1]], "ps": ps, "play": play,
            "value_A": float(p * A.e[0] + A.e[1]), "value_B": float(p * B.e[0] + B.e[1]),
            "trade_fish": float(A.e[0] - eq["xA"][0]), "trade_coco": float(eq["xA"][1] - A.e[1])}


def compute_core() -> dict:
    A, B = traders_box()
    reps = TRUTH["box"]["replicas"]
    xw = ge.box_equilibrium(A, B)["xA"][0]
    intervals = {}
    for r in reps:
        lo, hi = ge.core_interval(A, B, r)
        intervals[str(r)] = [lo, hi, float(ge.contract_curve(A, B, lo)), float(ge.contract_curve(A, B, hi))]
    # an example of blocking with two copies: the lens end that favours Bo most (least for Ana), blocked by
    # two Anas and one Bo
    lo1 = ge.lens_ends(A, B)[0]
    x_ex = lo1 + 0.15 * (xw - lo1)
    gain = ge.blocks(A, B, x_ex, 2, 1)
    assert gain > 0
    assert intervals[str(reps[-1])][1] - intervals[str(reps[-1])][0] < 0.1 * (intervals["1"][1] - intervals["1"][0])
    return {"intervals": intervals, "xw": xw, "example": {"x": x_ex, "y": float(ge.contract_curve(A, B, x_ex)),
                                                         "gain": gain, "s": 2, "t": 1},
            "reps": list(reps), "edgeworth": tables.EDGEWORTH_1881.data}


def compute_welfare() -> dict:
    A, B = traders_box()
    X = np.add(A.e, B.e)
    eq = ge.box_equilibrium(A, B)
    xa = np.array(eq["xA"])
    mrsA = A.a[0] / A.a[1] * xa[1] / xa[0]
    xb = X - xa
    mrsB = B.a[0] / B.a[1] * xb[1] / xb[0]
    assert abs(mrsA - mrsB) < 1e-9
    # second welfare theorem: the efficient allocation giving Ana a target of fish
    tx = TRUTH["target_fish"]
    ty = float(ge.contract_curve(A, B, tx))
    t_a = np.array([tx, ty])
    price = A.a[0] / A.a[1] * ty / tx                      # the supporting price: the common MRS
    # the lump-sum transfer (in coconuts, at that price) that puts Ana's budget line through the target
    need = price * tx + ty
    have = price * A.e[0] + A.e[1]
    transfer = need - have
    # check: with the transfer, both demand the target allocation at that price
    TA = ge.Trader(A.a, (A.e[0], A.e[1] + transfer))
    TB = ge.Trader(B.a, (B.e[0], B.e[1] - transfer))
    dA = TA.demand([price, 1.0])
    dB = TB.demand([price, 1.0])
    assert np.allclose(dA, t_a, atol=1e-9) and np.allclose(dB, X - t_a, atol=1e-9)
    return {"mrsA": mrsA, "mrsB": mrsB, "p": eq["p"], "target": [tx, ty], "price": price, "transfer": transfer,
            "uA_eq": A.utility(xa), "uA_target": A.utility(t_a), "uB_eq": B.utility(xb), "uB_target": B.utility(X - t_a)}


# ---------------------------------------------------------------------------------------------------------------
# the Fact: the law of one price

def compute_fact() -> dict:
    b, w = data.fred("MCOILBRENTEU"), data.fred("MCOILWTICO")
    wd = dict(zip(w["date"], w["value"]))
    months = [d for d in b["date"] if d in wd]
    brent = np.array([v for d, v in zip(b["date"], b["value"]) if d in wd], float)
    wti = np.array([wd[d] for d in months], float)
    ok = np.isfinite(brent) & np.isfinite(wti)
    months = [m for m, k in zip(months, ok) if k]
    brent, wti = brent[ok], wti[ok]
    spread = brent - wti
    yrs = np.array([int(m[:4]) for m in months])
    by_year = {int(y): float(spread[yrs == y].mean()) for y in sorted(set(yrs))}
    before = spread[yrs <= 2010]
    glut = spread[(yrs >= 2011) & (yrs <= 2013)]
    after = spread[(yrs >= 2016) & (yrs <= 2025)]
    k = int(np.argmax(spread))
    # price levels across countries: GDP per head at market exchange rates over GDP per head at PPP (US = 1)
    rows = [r for r in data.wdi(2023) if np.isfinite(r["gdppc_usd"]) and np.isfinite(r["gdppc_ppp"])
            and r["pop"] > 1e6]
    us = next(r for r in rows if r["code"] == "USA")
    level = np.array([r["gdppc_usd"] / r["gdppc_ppp"] for r in rows]) / (us["gdppc_usd"] / us["gdppc_ppp"])
    income = np.array([r["gdppc_ppp"] for r in rows])
    order = np.argsort(income)
    poorest = level[order[:20]]
    richest = level[order[-20:]]
    slope = float(np.polyfit(np.log(income), np.log(level), 1)[0])
    r_ = dict(tables.RADFORD_1945.data)
    # Agora: two villages, the same demand (12 - p) for fish and for haircuts; fish can be carried between them at
    # a dollar a fish, haircuts cannot
    a, slope, t = 12.0, 1.0, 1.0
    s1, s2 = 9.0, 3.0                                       # fish landed in each village
    h1, h2 = 4.0, 8.0                                       # haircuts the barbers can give
    auto = ((a - s1) / slope, (a - s2) / slope)
    q = max((s1 - s2 - slope * t) / 2, 0.0)                 # fish carried from village 1 to village 2
    fish = ((a - s1 + q) / slope, (a - s2 - q) / slope)
    hair = ((a - h1) / slope, (a - h2) / slope)
    assert abs((fish[1] - fish[0]) - t) < 1e-12
    villages = {"autarky_fish": auto, "fish": fish, "carried": q, "haircuts": hair, "cost": t}
    return {"villages": villages, "months": months, "brent": brent, "wti": wti, "spread": spread, "by_year": by_year,
            "mean_before": float(before.mean()), "sd_before": float(before.std()), "mean_glut": float(glut.mean()),
            "max": float(spread[k]), "max_month": months[k], "mean_after": float(after.mean()),
            "last_month": months[-1], "last_spread": float(spread[-1]),
            "countries": [r["code"] for r in rows], "level": level, "income": income,
            "level_poorest20": float(np.median(poorest)), "level_richest20": float(np.median(richest)),
            "elasticity": slope, "n_countries": len(rows), "salmon": r_["salmon_spread"]}


# ---------------------------------------------------------------------------------------------------------------
# existence and computation

def compute_simplex() -> dict:
    T3 = traders_three()

    def z(p):
        return ge.excess(T3, p)

    exact = np.array(ge.newton(z, [1.0, 1.0, 1.0])["p"])
    exact /= exact.sum()
    out = {"exact": exact.tolist(), "grids": {}}
    for N in TRUTH["three"]["grids"]:
        lab = ge.sperner_labels(z, N)
        walk = ge.sperner_walk(lab, N)
        out["grids"][str(N)] = {"labels": [[i, j, k] for (i, j), k in lab.items()], "walk": walk,
                                "error": float(np.max(np.abs(np.array(walk["p"]) - exact)))}
    # excess demand on a coarse grid, for the arrows
    arrows = []
    M = 10
    for i in range(1, M):
        for j in range(1, M - i):
            p = np.array([i, j, M - i - j], float) / M
            arrows.append([p.tolist(), z(p).tolist()])
    out["arrows"] = arrows
    return out


def compute_dynamics() -> dict:
    T3 = traders_three()

    def z(p):
        return ge.excess(T3, p)

    paths = []
    for p0 in TRUTH["three"]["starts"]:
        p0 = np.array(p0) / np.linalg.norm(p0)
        tt = ge.tatonnement(z, p0, T=12.0, n=300)
        paths.append(tt["p"])
    sc = ge.scarf_path(np.array(TRUTH["scarf_start"]), T=60.0, n=900)
    P = np.array(sc["p"])
    # one full turn: the first return near the start
    d = np.linalg.norm(P - P[0], axis=1)
    k0 = int(np.argmax(d))
    turn = k0 + int(np.argmin(d[k0:]))
    period = float(sc["t"][turn])
    return {"paths": paths, "scarf": sc["p"], "scarf_t": sc["t"], "scarf_norm": [min(sc["norm"]), max(sc["norm"])],
            "scarf_product": [min(sc["product"]), max(sc["product"])], "period": period,
            "scarf_eq": [1 / 3] * 3}


def compute_island() -> dict:
    T = traders_island()

    def z(p):
        return ge.excess(T, p)

    n = len(T[0].e)
    nw = ge.newton(z, np.ones(n))
    pn = np.array(nw["p"])
    assert nw["history"][-1]["err"] < 1e-10
    # the auctioneer: Euler steps of dp = 0.1 z(p), counted until the largest excess demand is below 1e-6
    p = np.ones(n) / np.sqrt(n) * np.linalg.norm(pn) / np.linalg.norm(np.ones(n)) * np.sqrt(n)
    p = np.ones(n)
    steps, errs = 0, []
    while steps < 20000:
        zz = z(p)
        errs.append(float(np.max(np.abs(zz))))
        if errs[-1] < 1e-6:
            break
        p = np.maximum(p + 0.1 * zz, 1e-9)
        steps += 1
    pt = p / p[0]
    assert np.allclose(pt, pn, rtol=1e-4)
    total = np.sum([t.e for t in T], axis=0)
    return {"goods": list(TRUTH["island"]["goods"]), "people": len(T), "p": pn.tolist(),
            "newton": [h["err"] for h in nw["history"]], "newton_iterations": nw["iterations"],
            "auctioneer_steps": steps, "auctioneer_errs": errs[::max(1, len(errs) // 200)],
            "total": total.tolist(), "sigmas": [1 / (1 - t.rho) for t in T]}


def compute_crusoe() -> dict:
    c = TRUTH["crusoe"]
    r = ge.crusoe(c["A"], c["alpha"], c["hours"], c["b"])
    Ls = np.linspace(0, c["hours"], 300)
    ppf_leisure = c["hours"] - Ls
    ppf_c = c["A"] * Ls ** c["alpha"]
    m = r["market"]
    u = c["b"] * np.log(m["c"]) + (1 - c["b"]) * np.log(m["leisure"])
    lei = np.linspace(0.5, c["hours"], 300)
    ind = np.exp((u - (1 - c["b"]) * np.log(lei)) / c["b"])
    return {**r, "hours": c["hours"], "ppf_leisure": ppf_leisure, "ppf_c": ppf_c, "ind_leisure": lei, "ind_c": ind,
            "A": c["A"], "alpha": c["alpha"], "b": c["b"]}


def compute_smd() -> dict:
    q = ge.quasilinear_three()
    qs = np.geomspace(0.25, 4.0, 400)
    z2 = q["z2"](qs)
    z1 = -z2 / qs                       # Walras's law, with p2 = 1: q z1 + z2 = 0
    roots = ge.equilibria_2good(q["z2"], 0.05, 20.0)
    stable = []
    for r in roots:
        h = 1e-4
        dz1 = (-q["z2"](r * (1 + h)) / (r * (1 + h)) + q["z2"](r * (1 - h)) / (r * (1 - h))) / (2 * h * r)
        stable.append(bool(dz1 < 0))
    assert stable == [True, False, True]
    return {"qs": qs, "z1": z1, "z2": z2, "roots": roots, "stable": stable, "r": q["r"]}


def compute_risk() -> dict:
    t = TRUTH["risk"]
    ad = ge.arrow_debreu(t["e0"], t["E"], t["probs"], t["beta"], t["gamma"])
    bo = ge.bond_only(t["e0"], t["E"], t["probs"], t["beta"], t["gamma"])
    gain = [a / b - 1 for a, b in zip(ad["ce"], bo["ce"])]
    return {"ad": ad, "bond": bo, "gain": gain, **{k: t[k] for k in ("e0", "E", "probs", "beta", "gamma")}}


def compute_plan() -> dict:
    k = TRUTH["plan"]
    res = ge.kantorovich(k["rates"], k["kit"])
    # comparison: every machine splits its day to make complete sets on its own
    R = np.array(k["rates"])
    kit = np.array(k["kit"])
    alone = float(np.sum(1 / np.sum(kit[None, :] / R, axis=1)))
    return {**res, "machines": list(k["machines"]), "parts": list(k["parts"]), "rates": R.tolist(),
            "kit": kit.tolist(), "alone": alone}


# ---------------------------------------------------------------------------------------------------------------
# the dial: misallocation

def compute_dial() -> dict:
    hk = tables.HSIEH_KLENOW_2009.data
    sig = hk["sigma"]
    lognormal = {c: {int(y): float(np.exp(sig / 2 * s ** 2) - 1) for y, s in v.items()}
                 for c, v in hk["sd_log_tfpr"].items()}
    t = TRUTH["plants"]
    rng = np.random.default_rng(t["seed"])
    la = rng.normal(0, t["sd_A"], t["n"])
    sims = {}
    for name, sd in (("US 1997", hk["sd_log_tfpr"]["US"][1997]), ("China 2005", hk["sd_log_tfpr"]["China"][2005]),
                     ("India 1994", hk["sd_log_tfpr"]["India"][1994])):
        lt = rng.normal(0, sd, t["n"])
        sims[name] = ge.misallocation(la, lt, sig)
    rows = [(e.who, e.year, e.design, e.sample, e.value, e.lo, e.hi) for e in dials.DIALS["misallocation"].estimates]
    return {"hk": {k: v for k, v in hk.items() if k != "abstract"}, "lognormal": lognormal, "sims": sims,
            "rows": rows, "bkr": tables.BILS_KLENOW_RUANE_2021.data}


def compute_nafta() -> dict:
    k = tables.KEHOE_2014.data
    a, s, l_ = (np.array(k[x], float) for x in ("actual", "sobarzo", "ltp"))
    return {"industries": list(k["industries"]), "actual": a, "sobarzo": s, "ltp": l_,
            "corr_sobarzo": float(np.corrcoef(a, s)[0, 1]), "corr_ltp": float(np.corrcoef(a, l_)[0, 1]),
            "weighted": k["weighted_corr"], "median_actual": float(np.median(a)), "median_sobarzo": float(np.median(s)),
            "max_sobarzo": float(s.max()), "years": k["years"], "quote": k["quote"]}


def compute_huts() -> dict:
    h = TRUTH["huts"]
    res = ge.top_trading_cycles([list(x) for x in h["prefs"]])
    ranks = [list(h["prefs"][i]).index(res["assign"][i]) for i in range(len(h["names"]))]
    return {**res, "names": list(h["names"]), "prefs": [list(x) for x in h["prefs"]], "ranks": ranks}


# ---------------------------------------------------------------------------------------------------------------
# the intermission: Brent against WTI

FILM_SECONDS = 40.0
MELODY_SECONDS = 55.0


def film_time(k: int, n: int) -> float:
    return 1.5 + FILM_SECONDS * k / (n - 1)


def compute_film() -> dict:
    f = compute_fact()
    n = len(f["months"])
    years = sorted(f["by_year"])
    return {"months": f["months"], "brent": f["brent"], "wti": f["wti"], "times": [film_time(k, n) for k in range(n)],
            "years": years, "year_times": [film_time(f["months"].index(f"{y}-01-01") if f"{y}-01-01" in f["months"]
                                                     else 0, n) for y in years]}


def compute_melody() -> dict:
    from explainer.music.monochord.audio import Clip, ClipStore

    f = compute_fact()
    fl = compute_film()
    years = fl["years"]
    gap = np.array([f["by_year"][y] for y in years])
    times = fl["year_times"]
    mel = score.data_melody(gap, MELODY_SECONDS, times=times, act=3, log=False, low=45, high=84)
    events = {"film_end": fl["times"][-1] + 6.0, "first": times[0], "glut": times[years.index(2011)]}
    clip = Clip(mel["y"], score.SR, events=events,
                notes=[{"t": float(t), "dur": 0.3, "hz": score.hz(nn), "name": str(y)}
                       for t, nn, y in zip(times, mel["notes"], years)],
                meta={"label": "Brent's premium over West Texas Intermediate crude, year by year, 1987-2026, as a "
                               "tune (computed)", "kind": "synthesized"})
    ClipStore("econ9").save("intermission.melody", clip)
    return {"times": times, "notes": mel["notes"], "gap": gap, "years": years, "seconds": MELODY_SECONDS}


ITEMS = {
    "box": compute_box,
    "core": compute_core,
    "welfare": compute_welfare,
    "fact": compute_fact,
    "simplex": compute_simplex,
    "dynamics": compute_dynamics,
    "island": compute_island,
    "crusoe": compute_crusoe,
    "smd": compute_smd,
    "risk": compute_risk,
    "plan": compute_plan,
    "dial": compute_dial,
    "nafta": compute_nafta,
    "huts": compute_huts,
    "film": compute_film,
    "melody": compute_melody,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
