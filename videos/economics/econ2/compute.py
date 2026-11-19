"""Precompute every number in Part 2 of *Economics, Built* ("The Scissors").

    python -m videos.economics.econ2.compute            # everything missing (a few minutes)
    python -m videos.economics.econ2.compute --force tax

Results are cached in ``.cache/econ2/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.  Data come from the
Data Room (``explainer.economics.data``: the World Bank's Pink Sheet of 3 November 2026, USDA's coffee balance sheets
and FRED's consumer prices, each frozen on 18 November 2026); models from Agora (``agora.market``: the pit and its
traders; ``agora.curves``: straight demand and supply lines); the Island's parameters from ``explainer.economics.island``
(Part 2's truths).  Every random choice is seeded, and where the film shows one simulated run it is chosen by rule
(the median of many by a stated statistic).

Items:
    diamonds     water and diamonds (illustrative): a falling marginal value, the total under it, and where each
                 good's price is read off
    demand       demand built up from reservation prices: one coffee drinker's cups, three drinkers added sideways,
                 and crowds of 10 to 10,000 buyers whose staircase becomes a line
    supply       supply built up from costs: one farm's bags, the pit's marginal traders, and the band they fix
    playit       the Play-it market: Smith's lopsided design (the sellers' surplus far larger than the buyers'),
                 41 runs by learning traders and by zero-intelligence traders, the run shown (the median by final
                 convergence), the guesses a viewer might make
    asym         is zero intelligence enough? the symmetric pit and three lopsided designs, 41 runs of each kind of
                 trader: where the final period's prices settle, and how much of the gain is made (Cliff and Bruten
                 1997)
    fish         the Island's fish market over 120 days, with storms: each day's cards cleared, the planted lines
    elasticity   elasticity along the fish market's demand line, revenue, and the midpoint formula on calm and
                 stormy days
    frost        the black frost of July 1975: Arabica and Robusta prices month by month (nominal and in 2026
                 dollars), Brazil's and the world's crops, the 1994 and 2021 frosts, and the rough elasticity the
                 1975-77 movement suggests
    film         the intermission's data film: real prices of eight commodities, 1960-2026, month by month
    melody       the intermission's data melody: the real price of Arabica coffee as a tune (saved as a clip)
    surplus      consumer and producer surplus in the pit and in the fish market; Dupuit's bridge in numbers
    tax          a 40-cent tax in the pit, remitted by the sellers and then by the buyers (41 runs each); the same on
                 the fish market's lines; how the burden splits with the two elasticities
    controls     a price cap and a price floor in the pit (41 runs each) against the triangle and the lottery
                 predictions; a cap on the fish market
"""

from __future__ import annotations

import numpy as np

from explainer.ai.cache import Cache
from explainer.economics import data, island, score
from explainer.economics.agora import curves as cv
from explainer.economics.agora import market as mk

CACHE = Cache("econ2")
load = CACHE.load
TRUTH = island.truths(2)
PIT = island.truths(1)["pit"]
SEEDS = range(41)


def _pit() -> mk.Market:
    return mk.Market(values=PIT["values"], costs=PIT["costs"])


def _design(name: str) -> mk.Market:
    d = TRUTH[name]
    return mk.Market(values=d["values"], costs=d["costs"])


def _runs(m: mk.Market, kind: str, **kw) -> list[dict]:
    return [mk.double_auction(m, kind, periods=6, seed=s, **kw) for s in SEEDS]


def _summary(runs: list[dict]) -> dict:
    """Medians over runs of the final period, and the per-period median of the mean price."""
    last = [r["periods"][-1] for r in runs]
    per = np.array([[p["mean"] for p in r["periods"]] for r in runs])
    alpha = np.array([[p["alpha"] for p in r["periods"]] for r in runs])
    return {"price": float(np.nanmedian([p["mean"] for p in last])),
            "paid": float(np.nanmedian([p["paid"] for p in last])),
            "received": float(np.nanmedian([p["received"] for p in last])),
            "efficiency": float(np.median([p["efficiency"] for p in last])),
            "efficiency_mean": float(np.mean([p["efficiency"] for p in last])),
            "n": float(np.median([p["n"] for p in last])),
            "alpha_last": float(np.nanmedian(alpha[:, -1])),
            "price_by_period": np.nanmedian(per, axis=0).tolist(),
            "alpha_by_period": np.nanmedian(alpha, axis=0).tolist()}


def _median_run(runs: list[dict]) -> int:
    """The run whose final-period convergence is the median of all of them (the rule for the run shown)."""
    a = np.array([r["periods"][-1]["alpha"] for r in runs])
    return int(np.argsort(a)[len(a) // 2])


# ---------------------------------------------------------------------------
def compute_diamonds() -> dict:
    """Illustrative only: a marginal value that falls with each litre a day, and the same shape for carats."""
    q = np.linspace(0, 200, 401)
    mv = 30.0 / (1 + q / 2.0) ** 2 + 0.002        # dollars for one more litre, when you already have q litres a day
    total = np.concatenate([[0.0], np.cumsum((mv[1:] + mv[:-1]) / 2 * np.diff(q))])
    used = 150.0                                     # litres a day a household might use
    k = int(np.searchsorted(q, used))
    return {"q": q, "mv": mv, "total": total, "used": used, "mv_at_used": float(mv[k]), "total_at_used": float(total[k]),
            "first_litre": float(mv[0])}


def compute_demand() -> dict:
    ana = [4.00, 2.50, 1.20, 0.40]          # one drinker's value of her first, second, third, fourth cup a day
    three = {"Ana": ana, "Bo": [3.00, 1.50, 0.60], "Chidi": [5.00, 2.00]}
    allv = sorted([v for vs in three.values() for v in vs], reverse=True)
    # crowds whose values are spread at random between 0 and $6: the staircase, drawn per head, nears the line
    crowds = {f"crowd_{n}": cv.crowd(n, 6.0, 0.5, 5.0, seed=n)[0] for n in (10, 100, 1000, 10000)}
    return {"ana": ana, "three": three, "market": allv, "crowd_n": [10, 100, 1000, 10000], "choke": 6.0, **crowds}


def compute_supply() -> dict:
    farm = [0.80, 1.10, 1.60, 2.40, 3.50]   # the cost of a coffee farm's first, second ... fifth extra bag
    m = _pit()
    eq = m.equilibrium()
    v, c, q = m.v, m.c, eq["q"]
    return {"farm": farm, "q": q, "v_last_in": float(v[q - 1]), "c_last_in": float(c[q - 1]),
            "v_first_out": float(v[q]), "c_first_out": float(c[q]), "lo": eq["p_lo"], "hi": eq["p_hi"],
            "values": v.tolist(), "costs": c.tolist()}


def compute_playit() -> dict:
    m = _design("lopsided")
    eq = m.equilibrium()
    zr, ir = _runs(m, "zip"), _runs(m, "zi")
    k = _median_run(zr)
    shown = zr[k]
    allc = np.array(list(m.values) + list(m.costs))
    return {"values": list(m.values), "costs": list(m.costs), "q": eq["q"], "lo": eq["p_lo"], "hi": eq["p_hi"],
            "p": eq["p"], "surplus": eq["surplus"], "cs": eq["cs_at_mid"], "ps": eq["ps_at_mid"],
            "guess_middle": float((allc.min() + allc.max()) / 2), "guess_mean": float(allc.mean()),
            "zip": _summary(zr), "zi": _summary(ir), "shown_seed": int(shown["seed"]),
            "shown": [[t["price"] for t in p["trades"]] for p in shown["periods"]],
            "shown_alpha": [p["alpha"] for p in shown["periods"]]}


def compute_asym() -> dict:
    out = {}
    for name in ("symmetric", "lopsided", "flat_supply", "flat_demand"):
        m = _pit() if name == "symmetric" else _design(name)
        eq = m.equilibrium()
        out[name] = {"lo": eq["p_lo"], "hi": eq["p_hi"], "p": eq["p"], "q": eq["q"],
                     "values": list(m.values), "costs": list(m.costs),
                     "zip": _summary(_runs(m, "zip")), "zi": _summary(_runs(m, "zi"))}
        z = out[name]
        z["zi_miss"] = float(z["zi"]["price"] - eq["p"])
        z["zip_miss"] = float(z["zip"]["price"] - eq["p"])
    return out


def _fish_lines() -> cv.Linear:
    f = TRUTH["fish"]
    return cv.Linear.from_crowd(f["buyers"], f["choke"], f["lowest_cost"], f["highest_cost"])


def compute_fish() -> dict:
    f = TRUTH["fish"]
    rng = np.random.default_rng(f["seed"])
    costs = np.sort(rng.uniform(f["lowest_cost"], f["highest_cost"], f["boats"]))
    days = []
    for d in range(f["days"]):
        storm = bool(rng.uniform() < f["storm_prob"])
        values = rng.uniform(0, f["choke"], f["buyers"])
        out = rng.uniform(size=f["boats"]) < (f["storm_ashore"] if storm else 0.0)
        m = mk.Market(values=tuple(values), costs=tuple(costs[~out]), ceiling=f["choke"])
        e = m.equilibrium()
        days.append({"day": d + 1, "storm": storm, "q": e["q"], "p": e["p"], "boats": int((~out).sum())})
    L = _fish_lines()
    storm_L = cv.Linear(L.a, L.b, L.c * (1 - f["storm_ashore"]), L.d * (1 - f["storm_ashore"]))
    calm = [x for x in days if not x["storm"]]
    stormy = [x for x in days if x["storm"]]
    e0, e1 = L.equilibrium(), storm_L.equilibrium()
    return {"days": days, "line": {"a": L.a, "b": L.b, "c": L.c, "d": L.d},
            "storm_line": {"a": storm_L.a, "b": storm_L.b, "c": storm_L.c, "d": storm_L.d},
            "eq": e0, "storm_eq": e1, "n_storms": len(stormy),
            "calm_p": float(np.mean([x["p"] for x in calm])), "calm_q": float(np.mean([x["q"] for x in calm])),
            "storm_p": float(np.mean([x["p"] for x in stormy])), "storm_q": float(np.mean([x["q"] for x in stormy])),
            "elasticity_true": L.elasticity()}


def compute_elasticity() -> dict:
    L = _fish_lines()
    fish = load("fish")
    p = np.linspace(0.05, L.choke - 0.05, 300)
    eps = np.array([-L.b * x / L.qd(x) for x in p])
    arc = cv.arc_elasticity(fish["calm_q"], fish["storm_q"], fish["calm_p"], fish["storm_p"])
    naive_up = ((fish["storm_q"] - fish["calm_q"]) / fish["calm_q"]) / ((fish["storm_p"] - fish["calm_p"]) / fish["calm_p"])
    naive_down = ((fish["calm_q"] - fish["storm_q"]) / fish["storm_q"]) / ((fish["calm_p"] - fish["storm_p"]) / fish["storm_p"])
    mid = 0.5 * (fish["calm_p"] + fish["storm_p"])
    return {"p": p, "eps": eps, "revenue": L.revenue(p), "unit_price": L.choke / 2, "choke": L.choke,
            "arc": float(arc), "naive_up": float(naive_up), "naive_down": float(naive_down),
            "true_at_mid": float(-L.b * mid / L.qd(mid)), "true_at_eq": L.elasticity()["demand"],
            "calm": [fish["calm_q"], fish["calm_p"]], "storm": [fish["storm_q"], fish["storm_p"]]}


def _cpi_deflator() -> tuple[dict, float, str]:
    """The US consumer price index by month, with the month BLS never published (October 2025, during the federal
    shutdown) filled log-linearly from its neighbours; :data:`CPI_FILLED` lists every month filled."""
    c = data.fred("CPIAUCNS")
    months = [d[:7] for d in c["date"]]
    vals = np.array(c["value"], float)
    ok = np.isfinite(vals)
    last = max(i for i in range(len(vals)) if ok[i])
    idx = np.arange(len(vals))
    filled = np.exp(np.interp(idx, idx[ok], np.log(vals[ok])))
    CPI_FILLED[:] = [months[i] for i in range(last + 1) if not ok[i]]
    cpi = {months[i]: float(filled[i]) for i in range(last + 1)}
    return cpi, cpi[months[last]], months[last]


CPI_FILLED: list = []


def _series(key: str, start: str, end: str, real: bool = False) -> tuple[list, np.ndarray]:
    s = data.pinksheet(key)
    cpi, base, _ = _cpi_deflator()
    months, vals = [], []
    for m, v in zip(s["month"], s["value"]):
        if start <= m <= end and np.isfinite(v):
            months.append(m)
            vals.append(v * base / cpi[m] if real else v)
    return months, np.array(vals)


def compute_frost() -> dict:
    cpi, base, base_month = _cpi_deflator()
    months, ara = _series("arabica", "1970-01", "1980-12")
    _, rob = _series("robusta", "1970-01", "1980-12")
    _, ara_real = _series("arabica", "1970-01", "1980-12", real=True)
    i = months.index
    c = data.psd_coffee()
    yrs = c["year"]
    span = [y for y in yrs if 1970 <= y <= 1980]
    prod = {k: [c[k]["production"][yrs.index(y)] for y in span] for k in ("world", "Brazil", "Colombia")}
    before, after = prod["world"][span.index(1975)], prod["world"][span.index(1976)]
    br0, br1 = prod["Brazil"][span.index(1975)], prod["Brazil"][span.index(1976)]

    def mean_year(y):
        return float(np.mean([v for m, v in zip(months, ara) if m.startswith(str(y))]))

    p75, p77 = mean_year(1975), mean_year(1977)
    peak = int(np.argmax(ara))
    # the later frosts
    m94, a94 = _series("arabica", "1993-01", "1996-12")
    m21, a21 = _series("arabica", "2019-01", "2026-10")
    _, a21r = _series("arabica", "2019-01", "2026-10", real=True)
    full_m, full_r = _series("arabica", "1960-01", "2026-10", real=True)
    out = {"months": months, "arabica": ara, "robusta": rob, "arabica_real": ara_real, "base_month": base_month,
           "cpi_filled": list(CPI_FILLED),
           "june75": float(ara[i("1975-06")]), "july75": float(ara[i("1975-07")]), "aug75": float(ara[i("1975-08")]),
           "peak_month": months[peak], "peak": float(ara[peak]), "peak_real": float(ara_real[peak]),
           "ratio_peak_june75": float(ara[peak] / ara[i("1975-06")]),
           "years": span, "production": prod, "world_1975": before, "world_1976": after,
           "world_change": float(after / before - 1), "brazil_1975": br0, "brazil_1976": br1,
           "brazil_change": float(br1 / br0 - 1), "brazil_share_1975": float(br0 / before),
           "p1975": p75, "p1977": p77,
           "arc": cv.arc_elasticity(before, after, p75, p77),
           "m94": m94, "a94": a94, "june94": float(a94[m94.index("1994-06")]), "july94": float(a94[m94.index("1994-07")]),
           "m21": m21, "a21": a21, "a21_real": a21r, "june21": float(a21[m21.index("2021-06")]),
           "max21": float(a21.max()), "max21_month": m21[int(np.argmax(a21))],
           "max21_real": float(a21r.max()),
           "real_max_month": full_m[int(np.argmax(full_r))], "real_max": float(full_r.max())}
    assert out["world_change"] < -0.1 and out["brazil_change"] < -0.5 and out["ratio_peak_june75"] > 4
    return out


FILM = ("oil", "arabica", "cocoa", "sugar", "wheat", "copper", "tin", "gold")
FILM_SECONDS = 34.0
MELODY_SECONDS = 46.0


def film_time(month: str) -> float:
    """When the data film reaches ``month`` ("YYYY-MM")."""
    y, m = int(month[:4]), int(month[5:7])
    return 1.5 + FILM_SECONDS * ((y - 1960) * 12 + (m - 1)) / ((2026 - 1960) * 12 + 9)


def compute_film() -> dict:
    cpi, base, base_month = _cpi_deflator()
    s0 = data.pinksheet("oil")
    months = [m for m in s0["month"] if "1960-01" <= m <= "2026-10"]
    out = {"months": months, "keys": list(FILM), "base_month": base_month, "cpi_filled": list(CPI_FILLED)}
    for k in FILM:
        s = data.pinksheet(k)
        d = dict(zip(s["month"], s["value"]))
        real = np.array([d.get(m, np.nan) * base / cpi[m] for m in months])
        # each line starts at 1 in its first twelve months with a price (an index of the real price)
        first = real[np.isfinite(real)][:12].mean()
        out[k] = real / first
        out[k + "_units"] = s["units"]
    return out


def compute_melody() -> dict:
    from explainer.music.monochord.audio import Clip, ClipStore

    m, r = _series("arabica", "1960-01", "2026-10", real=True)
    years = sorted({x[:4] for x in m})
    yv = np.array([np.mean([v for mm, v in zip(m, r) if mm.startswith(y)]) for y in years])
    times = [film_time(f"{y}-07") for y in years]
    mel = score.data_melody(yv, MELODY_SECONDS, times=times, act=1)
    events = {f"y{y}": float(t) for y, t in zip(years, times)}
    events["film_end"] = film_time("2026-10") + 1.0
    clip = Clip(mel["y"], score.SR, events=events,
                notes=[{"t": float(t), "dur": 1.0, "hz": score.hz(n), "name": y}
                       for t, n, y in zip(times, mel["notes"], years)],
                meta={"label": "the real price of Arabica coffee, 1960-2026, as a tune (computed)",
                      "kind": "synthesized"})
    ClipStore("econ2").save("intermission.melody", clip)
    return {"years": [int(y) for y in years], "values": yv, "times": times, "notes": mel["notes"],
            "seconds": MELODY_SECONDS, "film_seconds": FILM_SECONDS}


def compute_surplus() -> dict:
    m = _pit()
    eq = m.equilibrium()
    L = _fish_lines()
    e = L.equilibrium()
    return {"pit": {"cs": eq["cs_at_mid"], "ps": eq["ps_at_mid"], "surplus": eq["surplus"], "p": eq["p"],
                    "q": eq["q"], "values": m.v.tolist(), "costs": m.c.tolist()},
            "fish": e, "line": {"a": L.a, "b": L.b, "c": L.c, "d": L.d}, "choke": L.choke,
            "reservation": L.reservation}


def compute_tax() -> dict:
    t = TRUTH["tax"]
    m = _pit()
    eq = m.equilibrium()
    taxed_s = mk.Market(values=m.values, costs=tuple(c + t for c in m.costs)).equilibrium()
    on_s, on_b = _summary(_runs(m, "zip", tax=t, tax_on="sell")), _summary(_runs(m, "zip", tax=t, tax_on="buy"))
    zi_s, zi_b = _summary(_runs(m, "zi", tax=t, tax_on="sell")), _summary(_runs(m, "zi", tax=t, tax_on="buy"))
    lost = float(eq["surplus"] - (taxed_s["surplus"] + t * taxed_s["q"]))
    L = _fish_lines()
    fish = {"sell": L.tax(t, "sell"), "buy": L.tax(t, "buy"), "eq": L.equilibrium(), "elasticity": L.elasticity()}
    ratio = np.linspace(0.0, 4.0, 81)  # |eps_d| / eps_s
    share = 1 / (1 + ratio)
    return {"t": t, "p0": eq["p"], "q0": eq["q"], "q_taxed": taxed_s["q"],
            "band_paid": [taxed_s["p_lo"], taxed_s["p_hi"]], "band_received": [taxed_s["p_lo"] - t, taxed_s["p_hi"] - t],
            "on_sellers": on_s, "on_buyers": on_b, "zi_on_sellers": zi_s, "zi_on_buyers": zi_b,
            "lost": lost, "lost_share": lost / eq["surplus"], "buyers_share_pit": (on_s["paid"] - eq["p"]) / t,
            "fish": fish, "ratio": ratio, "share": share}


def compute_controls() -> dict:
    m = _pit()
    eq = m.equilibrium()
    v, c = m.v, m.c
    out = {"surplus": eq["surplus"]}
    cap, lo = TRUTH["cap"], TRUTH["minimum"]
    # the cap: the sellers who may sell, the buyers who want to buy at the cap
    k = int((c <= cap).sum())
    wanting = v[v >= cap]
    best = float(v[:k].sum() - c[:k].sum())
    lottery = float(k * wanting.mean() - c[:k].sum())
    s = _summary(_runs(m, "zip", cap=cap))
    out["cap"] = {"price": cap, "sellers": k, "wanting": int(len(wanting)), "best": best, "lottery": lottery,
                  "best_share": best / eq["surplus"], "lottery_share": lottery / eq["surplus"], "zip": s,
                  "zi": _summary(_runs(m, "zi", cap=cap))}
    # the floor: the buyers who may buy, the sellers who want to sell at the floor
    k = int((v >= lo).sum())
    offering = c[c <= lo]
    best = float(v[:k].sum() - c[:k].sum())
    lottery = float(v[:k].sum() - k * offering.mean())
    s = _summary(_runs(m, "zip", minimum=lo))
    out["floor"] = {"price": lo, "buyers": k, "offering": int(len(offering)), "best": best, "lottery": lottery,
                    "best_share": best / eq["surplus"], "lottery_share": lottery / eq["surplus"], "zip": s,
                    "zi": _summary(_runs(m, "zi", minimum=lo))}
    L = _fish_lines()
    out["fish_cap"] = L.cap(round(L.equilibrium()["p"] - 0.6, 2))
    out["fish_cap"]["price"] = round(L.equilibrium()["p"] - 0.6, 2)
    out["fish_eq"] = L.equilibrium()
    return out


ITEMS = {
    "diamonds": compute_diamonds,
    "demand": compute_demand,
    "supply": compute_supply,
    "playit": compute_playit,
    "asym": compute_asym,
    "fish": compute_fish,
    "elasticity": compute_elasticity,
    "frost": compute_frost,
    "film": compute_film,
    "melody": compute_melody,
    "surplus": compute_surplus,
    "tax": compute_tax,
    "controls": compute_controls,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
