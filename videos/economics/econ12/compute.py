"""Precompute every number in Part 12 of *Economics, Built* ("Competition among the Few").

    python -m videos.economics.econ12.compute            # everything missing (seconds)
    python -m videos.economics.econ12.compute --force greenporter

Results are cached in ``.cache/econ12/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.  Data: the Data Room
(``explainer.economics.data``: the BLS average price of regular gasoline and the EIA's West Texas Intermediate crude
price, both via FRED, deflated by the CPI-U; transcribed passages from Connor 1998 on lysine, Connor 2014 and Boyer
and Kotchoni 2015 on overcharges, and the 2010 and 2023 Merger Guidelines).  Models: Agora's oligopoly
(``agora.oligopoly``), with the Island's Part 12 truths.  Every random draw is seeded.

Items:
    boats        Cournot on the Island's boat market: reaction curves, the path of best replies, one to twenty yards
    bertrand     the undercutting spiral, equal and unequal costs
    playit       the reader's price against Crusoe's $40: the payoff of each choice, and Crusoe's reply
    resolve      Kreps and Scheinkman's capacities; differentiated boats; the collusive price for comparison
    beach        Hotelling's sellers drifting to the middle; Salop's circle with free entry against the planner
    variety      Dixit and Stiglitz: markup, size and the number of varieties as the economy grows
    deter        Dixit's capacity game: the entrant's profit against the incumbent's capacity, and the regimes
    collusion    the discount factor that sustains a cartel, Cournot and Bertrand, by number of firms
    greenporter  Green and Porter's price wars with nobody cheating
    lysine       the lysine cartel's prices as Connor states them
    leniency     the confession game under no, half and full leniency
    concentration  the Lerner index against HHI over elasticity; the guidelines' thresholds
    merger       the merger paradox and the saving needed; Williamson's trade-off
    contest      a contestable market: the price at average cost against the monopoly price
    common       common ownership: the modified HHI under two assumptions about the other owners
    rockets      rockets and feathers: does the pump price follow crude up faster than down? (monthly data)
    dial         the cartel-overcharge dial's rows
    film         the intermission's data film: crude and the pump, 1986-2026, in October 2026 dollars
    melody       its data melody: the real pump price, year by year
"""

from __future__ import annotations

import numpy as np

from explainer.ai.cache import Cache
from explainer.economics import data, dials, island, score
from explainer.economics.agora import oligopoly as ol
from explainer.economics.data import tables

CACHE = Cache("econ12")
load = CACHE.load
TRUTH = island.truths(12)
GALLONS_PER_BARREL = 42.0


def _boats():
    t = TRUTH["boats"]
    return t["a"], t["b"], t["c"]


def compute_boats() -> dict:
    a, b, c = _boats()
    ns = list(range(1, TRUTH["boats"]["n_max"] + 1))
    by_n = [ol.cournot(a, b, [c] * n) for n in ns]
    q1 = np.linspace(0, (a - c) / b, 121)
    reply = np.maximum((a - c - b * q1) / (2 * b), 0)            # either yard's best reply to the other's output
    path = ol.cournot_dynamics(a, b, c, c, q0=((a - c) / (2 * b), 0.0), steps=10)
    duo = by_n[1]
    mono = by_n[0]
    return {"ns": ns, "P": [d["P"] for d in by_n], "Q": [d["Q"] for d in by_n],
            "profit_each": [float(d["profits"][0]) for d in by_n],
            "industry_profit": [float(d["profits"].sum()) for d in by_n], "hhi": [10000 * d["hhi"] for d in by_n],
            "q1": q1, "reply": reply, "path": path, "duo_q": float(duo["q"][0]), "duo_P": duo["P"],
            "duo_profit": float(duo["profits"][0]), "mono_P": mono["P"], "mono_Q": mono["Q"],
            "mono_profit": float(mono["profits"][0]), "cartel_q_each": float(mono["Q"] / 2),
            "cartel_profit_each": float(mono["profits"][0] / 2), "a": a, "b": b, "c": c,
            "P20": by_n[-1]["P"]}


def compute_bertrand() -> dict:
    a, b, c = _boats()
    start = 40.0
    spiral = [start]
    while spiral[-1] - 1 > c:
        spiral.append(spiral[-1] - 1)
    equal = ol.bertrand(a, b, [c, c])
    unequal = ol.bertrand(a, b, [c, 20.0], tick=0.01)
    return {"spiral": spiral, "equal_P": equal["P"], "equal_profit": equal["profit"],
            "unequal_P": unequal["P"], "unequal_profit": unequal["profit"], "low_cost": c, "high_cost": 20.0,
            "cournot_P": ol.cournot(a, b, [c, c])["P"]}


def compute_playit() -> dict:
    a, b, _ = _boats()
    t = TRUTH["playit"]
    rival, cost = t["rival"], t["cost"]
    rows = []
    for p in t["prices"]:
        demand = max((a - p) / b, 0.0)
        share = 0.0 if p > rival else (0.5 if p == rival else 1.0)
        q = share * demand
        rows.append({"p": p, "share": share, "q": q, "profit": (p - cost) * q})
    best = max(rows, key=lambda r: r["profit"])
    # against twenty rivals all at $40, the same arithmetic with a twenty-first share
    q40 = (a - rival) / b
    return {"rows": rows, "best": best, "rival": rival, "cost": cost, "split_profit": (rival - cost) * q40 / 2,
            "split21": (rival - cost) * q40 / 21, "undercut": (rival - 1 - cost) * (a - rival + 1) / b}


def compute_resolve() -> dict:
    a, b, c = _boats()
    ks = ol.kreps_scheinkman(a, b, c)
    d = TRUTH["diff"]
    db = ol.bertrand_differentiated(d["alpha"], d["beta"], d["gamma"], d["c"])
    # the joint-profit price for the same differentiated demand: max (p - c)(alpha - (beta - gamma) p)
    pj = (d["alpha"] / (d["beta"] - d["gamma"]) + d["c"]) / 2
    qj = d["alpha"] - (d["beta"] - d["gamma"]) * pj
    return {"k": ks["k"], "P": ks["P"], "deviation_gain": ks["deviation_gain"], "cournot_P": ks["cournot"]["P"],
            "diff_p": db["p"], "diff_q": db["q"], "diff_profit": db["profit"], "pj": db["pj"], "br": db["br"],
            "joint_p": float(pj), "joint_profit": float((pj - d["c"]) * qj), "diff": d}


def compute_beach() -> dict:
    t = TRUTH["beach"]
    path = ol.hotelling_location(steps=12)
    h = ol.hotelling(t["t"], t["c"])
    s = ol.salop(t["t"], t["F"], t["c"])
    ns = np.arange(2, 21)
    total = ns * t["F"] + t["t"] / (4 * ns)
    profit = t["t"] / ns ** 2 - t["F"]
    return {"path": path, "end_p": h["p"], "end_profit": h["profit"], "n_free": s["n_free"], "n_opt": s["n_opt"],
            "p_free": s["p"], "cost_free": s["cost_free"], "cost_opt": s["cost_opt"], "ns": ns, "total": total,
            "profit": profit, "t": t["t"], "F": t["F"]}


def compute_variety() -> dict:
    v = TRUTH["variety"]
    base = ol.dixit_stiglitz(v["sigma"], v["f"], v["c"], v["L"])
    Ls = np.array([25.0, 50, 100, 200, 400, 800])
    n = Ls / (v["sigma"] * v["f"])
    # welfare per worker with CES love of variety: real wage times n^(1/(sigma - 1))
    real = (n / n[2]) ** (1 / (v["sigma"] - 1))
    return {"p": base["p"], "markup": base["markup"], "x": base["x"], "n": base["n"], "Ls": Ls, "ns": n,
            "welfare": real, "sigma": v["sigma"], "f": v["f"], "c": v["c"], "L": v["L"]}


def compute_deter() -> dict:
    d = TRUTH["deter"]
    base = ol.dixit_entry(d["a"], d["b"], d["c"], d["r"], d["F"])
    Fs = np.linspace(20, 400, 77)
    regimes = [ol.dixit_entry(d["a"], d["b"], d["c"], d["r"], F) for F in Fs]
    return {"ks": base["ks"], "entrant_profit": base["entrant_profit"], "S": base["S"], "T": base["T"],
            "m": base["monopoly_q"], "deter_k": base["deter_k"], "pi_deter": base["pi_deter"],
            "pi_acc": base["pi_accommodate"], "acc_q": base["acc_q"], "acc_entrant_q": base["acc_entrant_q"],
            "pi_mono": base["pi_monopoly"], "regime": base["regime"], "Fs": Fs,
            "F_regime": [r["regime"] for r in regimes],
            "F_profit": [r["pi_deter"] if r["regime"] in ("deter", "blockaded") else r["pi_accommodate"]
                         for r in regimes], "params": d}


def compute_collusion() -> dict:
    ns = list(TRUTH["collusion"]["ns"])
    cour = [ol.collusion_threshold(n, "cournot") for n in ns]
    bert = [ol.collusion_threshold(n, "bertrand") for n in ns]
    a, b, c = _boats()
    duo = ol.collusion_threshold(2, "cournot", a, b, c)
    return {"ns": ns, "cournot": [x["delta"] for x in cour], "bertrand": [x["delta"] for x in bert],
            "duo": duo}


def compute_greenporter() -> dict:
    t = TRUTH["collusion"]
    g = ol.green_porter(periods=t["periods"], seed=t["seed"])
    P = g["P"]
    war = g["war"]
    starts = [i for i in range(1, len(war)) if war[i] and not war[i - 1]]
    # what set off each war: the shock in the period before
    triggers = [float(g["shock"][i - 1]) for i in starts]
    return {"P": P, "war": war, "share_war": g["share_war"], "starts": starts, "trigger_shocks": triggers,
            "n_wars": len(starts), "collusive_mean": float(P[~war].mean()), "war_mean": float(P[war].mean()),
            "trigger": 3.5, "monopoly_P": 5.0, "cournot_P": 10 / 3}


def compute_lysine() -> dict:
    L = tables.LYSINE_CONNOR_1998.data

    def x(m):
        y, mo = (m.split("-") + ["07"])[:2]
        return int(y) + (int(mo) - 1) / 12

    pts = [(x(m) if "-" in m else int(m) + 0.5, p) for m, p in L["points"]]
    spans = [(x(a), x(b) + 1 / 12, lo, hi) for a, b, lo, hi in L["spans"]]
    after = (x("1994-09"), x("1995-02") + 1 / 12, 1.20, 1.20)
    lo, hi = L["overcharge_pct"]
    return {"points": pts, "spans": spans, "after": after, "cost": L["adm_cost"], "meeting": x("1992-06"),
            "mole": (x(L["mole"][0]), x(L["mole"][1])), "raid": 1995 + 5.9 / 12, "fine": L["adm_fine_musd"],
            "overcharge_musd": L["overcharge_musd"], "sales_musd": L["sales_musd"], "overcharge_pct": (lo, hi),
            "asian": L["asian_price_late_1980s"], "production": x("1991-02")}


def compute_leniency() -> dict:
    t = TRUTH["leniency"]
    rows = []
    for lam in (0.0, 0.5, 1.0):
        r = ol.leniency_race(t["fine"], t["caught"], leniency=lam)
        rows.append({"leniency": lam, "silent": r["silent"], "confess": r["confess_first"], "dominant": r["dominant"]})
    lam = np.linspace(0, 1, 101)
    return {"rows": rows, "lam": lam, "silent": t["caught"] * t["fine"] * np.ones_like(lam),
            "confess": (1 - lam) * t["fine"], "fine": t["fine"], "caught": t["caught"],
            "threshold": 1 - t["caught"]}


def compute_concentration() -> dict:
    a, b, c = _boats()
    rows = []
    for costs in ([c, c], [c, c, c], [c, 20.0], [c, 15.0, 25.0], [c] * 5, [8.0, 10.0, 12.0, 14.0]):
        d = ol.cournot(a, b, costs)
        rows.append({"costs": list(costs), "hhi": 10000 * d["hhi"], "lerner": d["lerner"],
                     "hhi_over_eps": d["lerner_hhi"], "P": d["P"], "eps": d["eps"]})
    g = tables.MERGER_GUIDELINES.data
    return {"rows": rows, "g2023": g["2023"], "g2010": g["2010"]}


def compute_merger() -> dict:
    a, b, c = _boats()
    t = TRUTH["merger"]
    ns = list(range(2, 11))
    gains = [ol.merger_cournot(n, a, b, c)["merger_gain"] for n in ns]
    # the share of the market a merger of k of n firms must reach to be profitable (Salant, Switzer, Reynolds):
    # merge k of 5 symmetric firms
    k_of_5 = []
    for k in range(2, 6):
        before = ol.cournot(a, b, [c] * 5)
        after = ol.cournot(a, b, [c] * (5 - k + 1))
        k_of_5.append(float(after["profits"][0] - k * before["profits"][0]))
    m = ol.merger_cournot(t["n"], a, b, c)
    w = ol.williamson(t["eps"], t["dp"], 0.0)
    dps = np.linspace(0, 0.3, 61)
    breakeven = 0.5 * t["eps"] * dps ** 2
    return {"ns": ns, "gains": gains, "k_of_5": k_of_5, "n": t["n"], "gain": m["merger_gain"],
            "before_P": m["before"]["P"], "after_P": m["after"]["P"], "before_profit": float(m["before"]["profits"][0]),
            "after_profit": float(m["after"]["profits"][0]), "saving_needed": m["saving_needed"],
            "price_if_free": m["price_if_free"], "cost": c, "eps": t["eps"], "dp": t["dp"],
            "breakeven_dc": w["breakeven_dc"], "dps": dps, "breakeven": breakeven}


def compute_contest() -> dict:
    a, b, c = _boats()
    F = 1000.0
    disc = (a - c) ** 2 - 4 * b * F
    Q = ((a - c) + np.sqrt(disc)) / (2 * b)
    P = a - b * Q
    qm = (a - c) / (2 * b)
    Pm = a - b * qm
    qs = np.linspace(5, 95, 181)
    return {"F": F, "Q": float(Q), "P": float(P), "Pm": float(Pm), "Qm": float(qm),
            "pi_m": float((Pm - c) * qm - F), "qs": qs, "ac": c + F / qs, "demand": a - b * qs, "c": c}


def compute_common() -> dict:
    t = TRUTH["common"]
    s = list(t["shares"])
    funds, stake, small = t["funds"], t["stake"], t["small"]
    rest = 1 - funds * stake
    # owners: the funds (stake in both), then each airline's other owners
    def build(n_other):
        rows = [[stake, stake] for _ in range(funds)]
        for j in range(2):
            for _ in range(n_other):
                r = [0.0, 0.0]
                r[j] = rest / n_other
                rows.append(r)
        g = np.array(rows)
        return ol.mhhi(s, g, g)

    one = build(1)
    many = build(small)
    xs = np.linspace(0, 0.5, 51)
    curve_one, curve_many = [], []
    for x in xs:
        st = x / funds
        r = 1 - x

        def mk(n_other):
            rows = [[st, st] for _ in range(funds)]
            for j in range(2):
                for _ in range(n_other):
                    v = [0.0, 0.0]
                    v[j] = r / n_other
                    rows.append(v)
            g = np.array(rows)
            return ol.mhhi(s, g, g)["mhhi"]

        curve_one.append(mk(1))
        curve_many.append(mk(small))
    return {"hhi": one["hhi"], "mhhi_one": one["mhhi"], "mhhi_many": many["mhhi"], "delta_one": one["delta"],
            "delta_many": many["delta"], "funds": funds, "stake": stake, "small": small, "common_share": funds * stake,
            "xs": xs, "curve_one": curve_one, "curve_many": curve_many}


def _monthly(series):
    r = data.fred(series)
    return {d[:7]: v for d, v in zip(r["date"], r["value"]) if np.isfinite(v)}


def compute_rockets() -> dict:
    g, w = _monthly("APU000074714"), _monthly("MCOILWTICO")
    months = [m for m in sorted(g) if m in w]
    G = np.array([g[m] for m in months])
    W = np.array([w[m] for m in months]) / GALLONS_PER_BARREL
    dg, dw = np.diff(G), np.diff(W)
    up, dn = np.clip(dw, 0, None), np.clip(dw, None, 0)
    L = 3
    X, y = [], []
    for t in range(L, len(dg)):
        X.append([1.0] + [up[t - j] for j in range(L)] + [dn[t - j] for j in range(L)] + [dg[t - 1]])
        y.append(dg[t])
    X, y = np.array(X), np.array(y)
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    resid = y - X @ beta
    s2 = resid @ resid / (len(y) - X.shape[1])
    cov = s2 * np.linalg.inv(X.T @ X)

    def response(sign, T=6):
        lev, prev, out = 0.0, 0.0, []
        for t in range(T):
            x = beta[1 + t] if (sign > 0 and t < L) else (beta[1 + L + t] if (sign < 0 and t < L) else 0.0)
            yv = x + beta[-1] * prev
            lev += yv
            prev = yv
            out.append(float(lev))
        return out

    # the test of equal first-month responses: up0 - dn0
    d0 = beta[1] - beta[1 + L]
    se0 = float(np.sqrt(cov[1, 1] + cov[1 + L, 1 + L] - 2 * cov[1, 1 + L]))
    return {"first": months[0], "last": months[-1], "n": len(y), "up": response(1), "down": response(-1),
            "up0": float(beta[1]), "down0": float(beta[1 + L]), "diff0": float(d0), "se0": se0,
            "lags": L}


def compute_dial() -> dict:
    rows = [(e.who, e.year, e.design, e.sample, e.value, e.lo, e.hi) for e in dials.DIALS["cartel_overcharge"].estimates]
    return {"rows": rows}


# ---------------------------------------------------------------------------------------------------------------
# the intermission: crude and the pump

FILM_SECONDS = 40.0
MELODY_SECONDS = 55.0


def film_time(k: int, n: int) -> float:
    return 1.5 + FILM_SECONDS * k / (n - 1)


def compute_film() -> dict:
    g, w, cpi = _monthly("APU000074714"), _monthly("MCOILWTICO"), _monthly("CPIAUCNS")
    months = [m for m in sorted(g) if m in w and m in cpi]
    base = cpi[months[-1]]
    pump = np.array([g[m] * base / cpi[m] for m in months])
    crude = np.array([w[m] / GALLONS_PER_BARREL * base / cpi[m] for m in months])
    n = len(months)
    years = sorted({int(m[:4]) for m in months})
    jan = {int(m[:4]): k for k, m in reversed(list(enumerate(months))) if m.endswith("-01")}
    k_max = int(np.argmax(pump))
    gap = pump - crude
    return {"months": months, "pump": pump, "crude": crude, "gap": gap, "times": [film_time(k, n) for k in range(n)],
            "years": years, "year_times": [film_time(jan.get(y, 0), n) for y in years], "base": months[-1],
            "peak": (months[k_max], float(pump[k_max])), "last": (months[-1], float(pump[-1]), float(crude[-1])),
            "first": (months[0], float(pump[0]), float(crude[0])), "gap_mean": float(gap.mean())}


def compute_melody() -> dict:
    from explainer.music.monochord.audio import Clip, ClipStore

    f = compute_film()
    years = f["years"]
    pump = np.array(f["pump"])
    yr = np.array([int(m[:4]) for m in f["months"]])
    annual = np.array([pump[yr == y].mean() for y in years])
    times = f["year_times"]
    mel = score.data_melody(annual, MELODY_SECONDS, times=times, act=3, log=True, low=45, high=84)
    events = {"film_end": f["times"][-1] + 6.0, "first": times[0], "half": times[len(times) // 2]}
    clip = Clip(mel["y"], score.SR, events=events,
                notes=[{"t": float(t), "dur": 0.3, "hz": score.hz(nn), "name": str(y)}
                       for t, nn, y in zip(times, mel["notes"], years)],
                meta={"label": "the average American pump price of regular gasoline in October 2026 dollars, year "
                               "by year, 1986-2026, as a tune (computed)", "kind": "synthesized"})
    ClipStore("econ12").save("intermission.melody", clip)
    return {"times": times, "notes": mel["notes"], "annual": annual, "years": years, "seconds": MELODY_SECONDS}


ITEMS = {
    "boats": compute_boats,
    "bertrand": compute_bertrand,
    "playit": compute_playit,
    "resolve": compute_resolve,
    "beach": compute_beach,
    "variety": compute_variety,
    "deter": compute_deter,
    "collusion": compute_collusion,
    "greenporter": compute_greenporter,
    "lysine": compute_lysine,
    "leniency": compute_leniency,
    "concentration": compute_concentration,
    "merger": compute_merger,
    "contest": compute_contest,
    "common": compute_common,
    "rockets": compute_rockets,
    "dial": compute_dial,
    "film": compute_film,
    "melody": compute_melody,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
