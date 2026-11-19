"""Precompute every number in Part 10 of *Economics, Built* ("The Price Maker").

    python -m videos.economics.econ10.compute            # everything missing (seconds)
    python -m videos.economics.econ10.compute --force bundle

Results are cached in ``.cache/econ10/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.  Data: the Data Room
(``explainer.economics.data``: the World Bank's Pink Sheet price of arabica coffee and the BLS average retail price
of ground coffee via FRED, monthly, 1980-2026; transcribed tables from De Loecker, Eeckhout and Unger 2020, Traina
2018, Nakamura and Zerom 2010 and Dube and Misra 2023).  Models: Agora's price maker (``agora.pricing``), with the
Island's Part 10 truths.  Every random draw is seeded.

Items:
    ferry        Bo's ferry: a hundred islanders' values, the fares of Play it, revenue and what is lost
    monopoly     demand, marginal revenue, the optimum, the Lerner index, deadweight loss
    passthrough  Agora's pass-through for linear and constant-elasticity demand; coffee from bean to shelf
    first        perfect discrimination
    third        students and townsfolk: one price or two
    screen       deck and cabin: the screening menu
    rides        Oi's two-part tariff
    bundle       the crossing and the reef tour, bundled or not
    durable      Crusoe's boats and the Coase conjecture
    ramsey       the waterworks: Ramsey-Boiteux prices
    aj           Averch and Johnson's over-capitalized waterworks
    monopsony    the yard as the only employer, and a minimum wage
    littlewood   two fare classes on the ferry
    dial         markups: De Loecker, Eeckhout and Unger's rows
    film         the intermission's data film: green coffee and the shelf price, month by month
    melody       its data melody: the shelf price, year by year
"""

from __future__ import annotations

import numpy as np

from explainer.ai.cache import Cache
from explainer.economics import data, dials, island, score
from explainer.economics.agora import pricing as pr
from explainer.economics.data import tables

CACHE = Cache("econ10")
load = CACHE.load
TRUTH = island.truths(10)
LB_PER_KG = 2.20462


def _values():
    f = TRUTH["ferry"]
    rng = np.random.default_rng(f["seed"])
    return rng.uniform(0, f["top"], f["people"])


def compute_ferry() -> dict:
    f = TRUTH["ferry"]
    v = _values()
    out = pr.ferry(v, f["fares"])
    grid = np.linspace(0, f["top"], 201)
    rev = [float(g * np.sum(v >= g)) for g in grid]
    out.update({"values": np.sort(v)[::-1], "grid": grid, "revenue_curve": rev})
    return out


def compute_monopoly() -> dict:
    d0 = TRUTH["demand"]
    d = pr.Linear(d0["a"], d0["b"])
    c = 0.0
    m = pr.monopoly(d, c)
    qs = np.linspace(0, d0["a"], 201)
    mc2 = pr.monopoly(d, d0["c"])
    return {**m, "c": c, "qs": qs, "p_of_q": d.p(qs), "mr": (d0["a"] - 2 * qs) / d0["b"], "a": d0["a"],
            "b": d0["b"], "with_cost": mc2, "c2": d0["c"]}


def compute_passthrough() -> dict:
    d0 = TRUTH["demand"]
    lin = pr.Linear(d0["a"], d0["b"])
    ce = pr.ConstantElasticity(1000.0, d0["eps"])
    cs = np.linspace(0.5, 6.0, 40)
    lin_p = [pr.monopoly(lin, c)["p"] for c in cs]
    ce_p = [pr.monopoly(ce, c)["p"] for c in cs]
    rho_lin = pr.pass_through(lin, d0["c"])
    rho_ce = pr.pass_through(ce, d0["c"])
    # coffee: green arabica (Pink Sheet, $/kg -> $/lb) and the shelf price of ground coffee (BLS, $/lb)
    r = data.fred("APU0000717311")
    a = data.pinksheet("arabica")
    rm = {d[:7]: v for d, v in zip(r["date"], r["value"])}
    am = dict(zip(a["month"], a["value"]))
    months = [m for m in sorted(rm) if m in am and np.isfinite(rm[m]) and np.isfinite(am[m])]
    shelf = np.array([rm[m] for m in months])
    bean = np.array([am[m] for m in months]) / LB_PER_KG
    q = {}
    for m, x, y in zip(months, shelf, bean):
        k = m[:4] + "Q" + str((int(m[5:7]) - 1) // 3 + 1)
        q.setdefault(k, []).append((x, y))
    ks = [k for k in sorted(q) if len(q[k]) == 3]
    S = np.array([np.mean([t[0] for t in q[k]]) for k in ks])
    B = np.array([np.mean([t[1] for t in q[k]]) for k in ks])
    L = 6

    def lags(y, x):
        Y = y[L:]
        X = np.column_stack([np.ones(len(Y))] + [x[L - j:len(x) - j] for j in range(L + 1)])
        b, *_ = np.linalg.lstsq(X, Y, rcond=None)
        return b[1:]

    el = lags(np.diff(np.log(S)), np.diff(np.log(B)))
    dol = lags(np.diff(S), np.diff(B))
    share = float(np.mean(B / S))
    return {"cs": cs, "lin_p": lin_p, "ce_p": ce_p, "rho_lin": rho_lin, "rho_ce": rho_ce, "eps": d0["eps"],
            "months": months, "shelf": shelf, "bean": bean, "quarters": ks, "elasticity_lags": el,
            "elasticity": float(el.sum()), "elasticity_first": float(el[0]), "dollar_lags": dol,
            "dollars": float(dol.sum()), "bean_share": share, "nz": tables.NAKAMURA_ZEROM_2010.data,
            "first": months[0], "last": months[-1]}


def compute_first() -> dict:
    d0 = TRUTH["demand"]
    d = pr.Linear(d0["a"], d0["b"])
    return {"first": pr.first_degree(d, 0.0), "one": pr.monopoly(d, 0.0), "total": float(d.cs(0.0))}


def compute_third() -> dict:
    g = TRUTH["groups"]
    s, t = pr.Linear(*g["students"]), pr.Linear(*g["town"])
    out = pr.third_degree(s, t, g["c"])
    ps = np.linspace(0, 20, 201)
    return {**out, "c": g["c"], "students": list(g["students"]), "town": list(g["town"]), "ps": ps,
            "q_students": s.q(ps), "q_town": t.q(ps)}


def compute_screen() -> dict:
    s = TRUTH["screen"]
    return {**pr.screening(s["lo"], s["hi"], s["share_hi"]), **s}


def compute_rides() -> dict:
    r = TRUTH["rides"]
    one = pr.two_part([pr.Linear(*r["small"])], r["c"])
    ns, nb = r["mix"]
    two = pr.two_part([pr.Linear(*r["small"])] * ns + [pr.Linear(*r["big"])] * nb, r["c"])
    mono = pr.monopoly(pr.Linear(*r["small"]), r["c"])
    return {"one": one, "two": two, "mono": mono, **r}


def compute_bundle() -> dict:
    b = TRUTH["bundle"]
    rng = np.random.default_rng(b["seed"])
    v1 = rng.uniform(0, b["top"], b["people"])
    neg = np.clip(b["top"] - v1 + rng.normal(0, b["noise"] * 2, b["people"]), 0, None)
    pos = np.clip(v1 + rng.normal(0, b["noise"] * 2, b["people"]), 0, None)
    return {"v1": v1, "neg": neg, "pos": pos, "negative": pr.bundling(v1, neg), "positive": pr.bundling(v1, pos)}


def compute_durable() -> dict:
    d = TRUTH["durable"]
    rows = []
    for n in d["per_year"]:
        delta = float(np.exp(-d["r"] / n))
        c = pr.coase(delta, int(d["years"] * n))
        rows.append({"per_year": n, "delta": delta, "first_price": c["first_price"], "path": c["path"][:8],
                     "sold": c["sold"][:8]})
    return {"rows": rows, "static": 0.5, **d}


def compute_ramsey() -> dict:
    r = TRUTH["ramsey"]
    d1, d2 = (pr.ConstantElasticity(A, e) for A, e in zip(r["A"], r["eps"]))
    out = pr.ramsey(d1, d2, r["c"][0], r["c"][1], r["F"])
    return {**out, **r}


def compute_aj() -> dict:
    a = TRUTH["aj"]
    return {**pr.averch_johnson(a["A"], a["a"], a["b"], a["p"], a["w"], a["r"], a["s"]), **a}


def compute_monopsony() -> dict:
    m = TRUTH["monopsony"]
    return {**pr.monopsony(m["w0"], m["slope"], m["mrp"], m["min_wage"]), **m}


def compute_littlewood() -> dict:
    lw = pr.littlewood(40, 4.0, 10.0, 12, 5)
    return {**lw, "seats": 40, "p_lo": 4.0, "p_hi": 10.0, "mean_hi": 12, "sd_hi": 5}


def compute_dlw() -> dict:
    """The production approach to markups checked on one Agora firm: output K^a M^b with capital fixed, materials
    bought at a given price, demand of constant elasticity, so the true markup is eps / (eps - 1)."""
    from scipy.optimize import brentq

    a, b, K, pm, eps, A0 = 0.3, 0.5, 100.0, 2.0, 5.0, 1000.0

    def mc(Q):
        return pm / b * Q ** (1 / b - 1) * K ** (-a / b)

    Q = brentq(lambda q: A0 * (eps / (eps - 1) * mc(q)) ** -eps - q, 1e-9, 1e6, xtol=1e-14)
    p = (Q / A0) ** (-1 / eps)
    M = (Q / K ** a) ** (1 / b)
    return {"theta": b, "sales": p * Q, "cogs": pm * M, "ratio": p * Q / (pm * M), "measured": b * p * Q / (pm * M),
            "true": eps / (eps - 1), "p": p, "mc": mc(Q), "eps": eps}


def compute_personal() -> dict:
    r = pr.personalized()
    return {k: r[k] for k in ("p_uniform", "uniform", "personal", "first_degree", "share_pay_less", "profit_gain",
                              "cs_change", "hist", "grid", "p_personal_quantiles", "coef")}


def compute_dial() -> dict:
    rows = [(e.who, e.year, e.design, e.sample, e.value, e.lo, e.hi) for e in dials.DIALS["markups"].estimates]
    return {"rows": rows, "dleu": tables.DLEU_2020.data, "traina": tables.TRAINA_2018.data,
            "dube_misra": tables.DUBE_MISRA_2023.data}


# ---------------------------------------------------------------------------------------------------------------
# the intermission: coffee, bean to shelf

FILM_SECONDS = 40.0
MELODY_SECONDS = 55.0


def film_time(k: int, n: int) -> float:
    return 1.5 + FILM_SECONDS * k / (n - 1)


def compute_film() -> dict:
    p = compute_passthrough()
    n = len(p["months"])
    years = sorted({int(m[:4]) for m in p["months"]})
    jan = {int(m[:4]): k for k, m in reversed(list(enumerate(p["months"]))) if m.endswith("-01")}
    return {"months": p["months"], "shelf": p["shelf"], "bean": p["bean"], "times": [film_time(k, n) for k in range(n)],
            "years": years, "year_times": [film_time(jan.get(y, 0), n) for y in years]}


def compute_melody() -> dict:
    from explainer.music.monochord.audio import Clip, ClipStore

    f = compute_film()
    years = f["years"]
    shelf = np.array(f["shelf"])
    yr = np.array([int(m[:4]) for m in f["months"]])
    annual = np.array([shelf[yr == y].mean() for y in years])
    times = f["year_times"]
    mel = score.data_melody(annual, MELODY_SECONDS, times=times, act=3, log=True, low=45, high=84)
    events = {"film_end": f["times"][-1] + 6.0, "first": times[0], "half": times[len(times) // 2]}
    clip = Clip(mel["y"], score.SR, events=events,
                notes=[{"t": float(t), "dur": 0.3, "hz": score.hz(nn), "name": str(y)}
                       for t, nn, y in zip(times, mel["notes"], years)],
                meta={"label": "the average shelf price of ground coffee in the United States, year by year, "
                               "1980-2026, as a tune (computed)", "kind": "synthesized"})
    ClipStore("econ10").save("intermission.melody", clip)
    return {"times": times, "notes": mel["notes"], "annual": annual, "years": years, "seconds": MELODY_SECONDS}


ITEMS = {
    "ferry": compute_ferry,
    "monopoly": compute_monopoly,
    "passthrough": compute_passthrough,
    "first": compute_first,
    "third": compute_third,
    "screen": compute_screen,
    "rides": compute_rides,
    "bundle": compute_bundle,
    "durable": compute_durable,
    "ramsey": compute_ramsey,
    "aj": compute_aj,
    "monopsony": compute_monopsony,
    "littlewood": compute_littlewood,
    "dlw": compute_dlw,
    "personal": compute_personal,
    "dial": compute_dial,
    "film": compute_film,
    "melody": compute_melody,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
