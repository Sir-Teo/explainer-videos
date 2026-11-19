"""Precompute every number in Part 16 of *Economics, Built* ("Auctions").

    python -m videos.economics.econ16.compute            # everything missing (seconds)
    python -m videos.economics.econ16.compute --force formats

Results are cached in ``.cache/econ16/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.  Data: the Data Room
(``explainer.economics.data``: the 3-month Treasury bill rate from FRED; transcribed accounts of Britain's and
Europe's 3G auctions (Binmore and Klemperer 2002; Klemperer 2002), the jar of coins (Bazerman and Samuelson 1983),
signalling in spectrum auctions (Cramton and Schwartz 2000; Klemperer 2002), reserve prices (Ostrovsky and Schwarz
2009), the Treasury's change of format (Garbade and Ingber 2005) and the incentive auction (FCC 2017)).  Models:
Agora's auction house (``agora.auctions``), with the Island's Part 16 truths.

Items:
    playit      your expected profit against each bid you might make, first-price and second-price
    clock       one sale run on the English and Dutch clocks
    formats     five formats run on the same 60,000 draws of values; bid functions; revenue against bidders
    risk        risk-averse bidders: higher first-price bids and revenue
    myerson     revenue against the reserve price, two bidders; three bidders without one
    curse       the winner's expected overestimate against the number of bidders; the jar of coins
    exposure    two fishing rights, a bidder who wants both, and two locals
    gsp         the island's notice board: Vickrey prices and the generalized second price
    bonds       two bonds, a big buyer and a small one: uniform price, demand reduction and Vickrey
    spectrum    the 3G auctions of 2000 and the signals in the spectrum auctions
    dial        the reserve-price dial's rows
    film        the intermission's data film: the 3-month Treasury bill rate, 1934-2025
    melody      its data melody, year by year
"""

from __future__ import annotations

import numpy as np

from explainer.ai.cache import Cache
from explainer.economics import data, dials, island, score
from explainer.economics.agora import auctions as au
from explainer.economics.data import tables

CACHE = Cache("econ16")
load = CACHE.load
TRUTH = island.truths(16)


def compute_playit() -> dict:
    t = TRUTH["playit"]
    e = au.expected_profit(t["value"], t["rivals"], t["top"])
    return {**t, **e}


def compute_clock() -> dict:
    t = TRUTH["clock"]
    v = np.array(t["values"])
    n = len(v)
    c = au.clock(v / 100.0, step=0.01)
    dutch_bids = (n - 1) / n * v                       # the risk-neutral equilibrium, values uniform on 0-100
    k = int(np.argmax(dutch_bids))
    return {**t, "english_drops": {int(i): 100 * p for i, p in c["drops"].items()}, "english_winner": c["winner"],
            "english_price": 100 * c["price"], "dutch_bids": dutch_bids.tolist(), "dutch_winner": k,
            "dutch_price": float(dutch_bids[k]), "order": c["order"]}


def compute_formats() -> dict:
    t = TRUTH["formats"]
    sim = au.simulate_formats(n=t["n"], draws=t["draws"], seed=t["seed"])
    vs = np.linspace(0, 1, 101)
    bids = {str(n): ((n - 1) / n * vs).tolist() for n in (2, 3, 4, 10)}
    ns = np.arange(2, 21)
    first = np.array(sim["first_dist"])
    second = np.array(sim["second_dist"])
    edges = np.linspace(0, 1, 26)
    return {**sim, "vs": vs, "bids": bids, "ns": ns, "revenue_n": ((ns - 1) / (ns + 1)).tolist(),
            "hist_first": np.histogram(first, edges)[0].tolist(), "hist_second": np.histogram(second, edges)[0].tolist(),
            "edges": edges, "sd_first": float(first.std()), "sd_second": float(second.std())}


def compute_risk() -> dict:
    t, f = TRUTH["risk"], TRUTH["formats"]
    n, a = f["n"], t["alpha"]
    sim = au.simulate_formats(n=n, draws=f["draws"], seed=f["seed"], alpha=a)
    vs = np.linspace(0, 1, 101)
    return {"alpha": a, "n": n, "vs": vs, "neutral": ((n - 1) / n * vs).tolist(),
            "averse": au.first_price_bid(vs, n, alpha=a).tolist(), "share_neutral": (n - 1) / n,
            "share_averse": (n - 1) / (n - 1 + a), "first": sim["formats"]["first-price"]["mean"],
            "second": sim["formats"]["second-price"]["mean"], "theory_first": (n - 1) / (n - 1 + a) * n / (n + 1),
            "theory_second": (n - 1) / (n + 1)}


def compute_myerson() -> dict:
    n = TRUTH["myerson"]["n"]
    m2 = au.myerson(n)
    m3 = au.myerson(n + 1)
    vs = np.linspace(0, 1, 101)
    return {**m2, "rev_more": m3["rev_zero"], "n_more": n + 1, "vs": vs, "virtual": (2 * vs - 1).tolist(),
            "p_no_sale": 0.5 ** n, "gain": m2["rev_star"] / m2["rev_zero"] - 1,
            "reserve_bid": au.first_price_bid(vs, n, reserve=0.5).tolist()}


def compute_curse() -> dict:
    t = TRUTH["curse"]
    w = au.winners_curse(t["ns"], t["value"], t["noise"], seed=t["seed"])
    return {**w, "jar": tables.BAZERMAN_SAMUELSON_1983.data}


def compute_exposure() -> dict:
    t = TRUTH["exposure"]
    return {"cases": [au.exposure(t["both"], t["alone"], r) for r in t["rivals"]], "both": t["both"],
            "alone": t["alone"]}


def compute_gsp() -> dict:
    t = TRUTH["gsp"]
    return au.gsp(t["values"], t["ctrs"])


def compute_bonds() -> dict:
    t = TRUTH["bonds"]
    return au.multi_unit(t["supply"], t["big"], t["small"])


def compute_spectrum() -> dict:
    return {"uk": tables.UK_3G_2000.data, "euro": tables.EURO_3G_2000.data,
            "signals": tables.COLLUSION_SIGNALS.data, "fcc": tables.INCENTIVE_AUCTION.data,
            "treasury": tables.TREASURY_FORMAT.data, "reserve": tables.RESERVE_PRICES.data}


def compute_dial() -> dict:
    rows = [(e.who, e.year, e.design, e.sample, e.value, e.lo, e.hi) for e in dials.DIALS["reserve_revenue"].estimates]
    return {"rows": rows, "reserve": tables.RESERVE_PRICES.data}


# ---------------------------------------------------------------------------------------------------------------
# the intermission: ninety years of the Treasury bill

FILM_SECONDS = 40.0
MELODY_SECONDS = 55.0


def film_time(k: int, n: int) -> float:
    return 1.5 + FILM_SECONDS * k / (n - 1)


def compute_film() -> dict:
    s = data.fred("TB3MS")
    by = {}
    for d, v in zip(s["date"], s["value"]):
        if v is None:
            continue
        by.setdefault(int(d[:4]), []).append(float(v))
    years = [y for y in sorted(by) if y <= 2025 and len(by[y]) == 12]
    rate = [float(np.mean(by[y])) for y in years]
    k = int(np.argmax(rate))
    monthly = [(d, float(v)) for d, v in zip(s["date"], s["value"]) if v is not None]
    top_m = max(monthly, key=lambda t: t[1])
    zero = [y for y, r in zip(years, rate) if r < 0.25]
    return {"years": years, "rate": rate, "times": [film_time(i, len(years)) for i in range(len(years))],
            "peak_year": years[k], "peak": rate[k], "peak_month": top_m[0][:7], "peak_month_rate": top_m[1],
            "zero_years": zero, "last_year": years[-1], "last": rate[-1], "source": data.fred_cite("TB3MS"),
            "retrieved": s.get("retrieved", "")}


def compute_melody() -> dict:
    from explainer.music.monochord.audio import Clip, ClipStore

    f = compute_film()
    times = f["times"]
    mel = score.data_melody(np.array(f["rate"]), MELODY_SECONDS, times=times, act=4, log=False, low=45, high=84)
    events = {"film_end": times[-1] + 6.0, "first": times[0], "half": times[len(times) // 2]}
    clip = Clip(mel["y"], score.SR, events=events,
                notes=[{"t": float(t), "dur": 0.3, "hz": score.hz(nn), "name": str(y)}
                       for t, nn, y in zip(times, mel["notes"], f["years"])],
                meta={"label": "the 3-month Treasury bill rate, annual average, 1934-2025 (FRED, TB3MS), as a tune "
                               "(computed)", "kind": "synthesized"})
    ClipStore("econ16").save("intermission.melody", clip)
    return {"times": times, "notes": mel["notes"], "years": f["years"], "seconds": MELODY_SECONDS}


ITEMS = {
    "playit": compute_playit,
    "clock": compute_clock,
    "formats": compute_formats,
    "risk": compute_risk,
    "myerson": compute_myerson,
    "curse": compute_curse,
    "exposure": compute_exposure,
    "gsp": compute_gsp,
    "bonds": compute_bonds,
    "spectrum": compute_spectrum,
    "dial": compute_dial,
    "film": compute_film,
    "melody": compute_melody,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
