"""Precompute every number in Part 28 of *Economics, Built* ("Inflation and Expectations").

    python -m videos.economics.econ28.compute            # everything missing (seconds)
    python -m videos.economics.econ28.compute --force us

Results are cached in ``.cache/econ28/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.  Data: the Data Room
(``explainer.economics.data``: FRED's CPI, core CPI and PCE price index, the unemployment rate, the CBO's natural rate
and potential GDP, real GDP, the federal funds rate, job openings and unemployment, Michigan's expected inflation and
the 5-year breakeven rate).  Models: Agora's expectations (``agora.expectations``) with the Island's Part 28 truths.

Items:
    us           annual US inflation and unemployment, 1948-2025, and the 1960s menu
    phillips     Phillips's 1958 curve and Samuelson and Solow's menu
    play         Play it: inflation 1960-1972 and what 1973 brought
    accelerate   the Island holds unemployment below the natural rate
    adaptive     adaptive forecasts of US inflation against the outcome
    islands      Lucas's islands: output's response to money, calm and volatile
    critique     the Lucas critique under rational expectations
    bg           Barro and Gordon's inflation bias; Rogoff's conservative banker
    volcker      1977-1987 month by month; the sacrifice ratio of 1980-85
    flat         the slope of the Phillips curve, 1960-83 against 2000-19
    surge        2019-2025: core inflation, openings per unemployed, expectations
    transitory   the Fed's June 2021 projection against PCE inflation in 2022
    persistence  inflation's first-order autocorrelation, by period
    expect       Michigan's households against realized inflation, 1978-2026
    film         the intermission's data film: inflation and unemployment, month by month, 1948-2025
    melody       its data melody: inflation
"""

from __future__ import annotations

import numpy as np

from explainer.ai.cache import Cache
from explainer.economics import data, island, score
from explainer.economics.agora import expectations as ex

CACHE = Cache("econ28")
load = CACHE.load
TRUTH = island.truths(28)


def _t(d: str) -> float:
    return int(d[:4]) + (int(d[5:7]) - 1) / 12


def _monthly(key: str) -> dict:
    d = data.fred(key)
    return {x: v for x, v in zip(d["date"], d["value"]) if np.isfinite(v)}


def _yoy(key: str) -> dict:
    """Twelve-month percentage change of a monthly index, by date."""
    m = _monthly(key)
    out = {}
    for x, v in m.items():
        prev = f"{int(x[:4]) - 1}{x[4:]}"
        if prev in m:
            out[x] = 100 * (v / m[prev] - 1)
    return out


def _annual_mean(mon: dict) -> dict:
    a: dict = {}
    for x, v in mon.items():
        a.setdefault(int(x[:4]), []).append(v)
    return {y: float(np.mean(v)) for y, v in a.items() if len(v) >= 11}


def _annual_infl(key: str) -> dict:
    """December-average-free annual inflation: the change in the annual average index."""
    a = _annual_mean(_monthly(key))
    return {y: 100 * (a[y] / a[y - 1] - 1) for y in a if y - 1 in a}


def compute_us() -> dict:
    inf = _annual_infl("CPIAUCSL")
    un = _annual_mean(_monthly("UNRATE"))
    yrs = [y for y in range(1949, 2026) if y in inf and y in un]
    return {"years": yrs, "inflation": [inf[y] for y in yrs], "unemployment": [un[y] for y in yrs],
            "u1969": un[1969], "pi1969": inf[1969], "u1975": un[1975], "pi1975": inf[1975], "u1980": un[1980],
            "pi1980": inf[1980], "u1982": un[1982], "pi1982": inf[1982],
            "sixties": [y for y in yrs if 1961 <= y <= 1969]}


def compute_phillips() -> dict:
    u = np.linspace(1.0, 11.0, 201)
    return {"u": u.tolist(), "w": ex.phillips1958(u).tolist(), "w25": float(ex.phillips1958(2.5)),
            "zero": 5.5, "w55": float(ex.phillips1958(5.5)),
            # Samuelson and Solow's menu (1960): price stability at 5-6% unemployment; 3% unemployment with prices
            # rising 4-5% a year
            "menu": [(5.5, 0.0), (3.0, 4.5)]}


def compute_play() -> dict:
    P = TRUTH["playit"]
    inf = _annual_infl("CPIAUCSL")
    a, b = P["history"]
    yrs = list(range(a, b + 1))
    hist = [inf[y] for y in yrs]
    return {**P, "years": yrs, "history": hist, "answer": inf[P["target"]], "last": hist[-1],
            "avg5": float(np.mean(hist[-5:])), "next5": [inf[y] for y in range(P["target"], P["target"] + 8)]}


def compute_accelerate() -> dict:
    A = TRUTH["accelerate"]
    fast = ex.accelerate(A["years"], A["ustar"], A["u_target"], A["beta"], A["lam"], A["pi0"])
    slow = ex.accelerate(A["years"], A["ustar"], A["u_target"], A["beta"], A["lam_slow"], A["pi0"])
    return {**A, "fast": fast, "slow": slow}


def compute_adaptive() -> dict:
    inf = _annual_infl("CPIAUCSL")
    yrs = [y for y in range(1960, 2026) if y in inf]
    x = [inf[y] for y in yrs]
    out = {}
    for lam in TRUTH["adaptive"]["lams"]:
        f = ex.adaptive_forecasts(x, lam)
        out[f"{lam}"] = f
    # errors by decade for the "last year" rule
    f1 = out["1.0"]
    err = np.array(f1["error"])
    e70 = [e for y, e in zip(yrs[1:], err) if 1966 <= y <= 1980]
    e80 = [e for y, e in zip(yrs[1:], err) if 1981 <= y <= 1986]
    return {"years": yrs, "inflation": x, "fits": out, "mean_err_70s": float(np.mean(e70)),
            "mean_err_80s": float(np.mean(e80))}


def compute_islands() -> dict:
    I = TRUTH["islands"]
    calm = ex.lucas_islands(I["sigma_z"], I["sigma_m_calm"], I["b"], I["n_islands"], I["years"], I["seed"])
    wild = ex.lucas_islands(I["sigma_z"], I["sigma_m_wild"], I["b"], I["n_islands"], I["years"], I["seed"])
    sm = np.linspace(0.05, 4.0, 80)
    return {**I, "calm": calm, "wild": wild, "sigma_m": sm.tolist(),
            "theta": [ex.signal_extraction(I["sigma_z"], s) for s in sm]}


def compute_critique() -> dict:
    C = TRUTH["critique"]
    return {**C, **ex.critique(**C)}


def compute_bg() -> dict:
    B = TRUTH["bg"]
    return {**B, "game": ex.barro_gordon(B["lam"], B["k"], B["b"]),
            "rogoff": ex.conservative_banker(B["lam"], B["k"], B["sigma"], B["b"])}


def compute_volcker() -> dict:
    ff = _monthly("FEDFUNDS")
    inf = _yoy("CPIAUCSL")
    un = _monthly("UNRATE")
    ds = sorted(d for d in ff if "1977-01-01" <= d <= "1987-12-01" and d in inf and d in un)
    gdp = dict(zip(data.fred("GDPC1")["date"], data.fred("GDPC1")["value"]))
    pot = dict(zip(data.fred("GDPPOT")["date"], data.fred("GDPPOT")["value"]))
    q = sorted(d for d in gdp if "1980-01-01" <= d <= "1985-10-01" and d in pot)
    gap_q = [100 * (gdp[d] / pot[d] - 1) for d in q]
    ann = _annual_infl("CPILFESL")
    s = ex.sacrifice_ratio(np.array(gap_q) / 4, ann[1980], ann[1985])
    peak_ff = max(ff[d] for d in ds)
    peak_inf = max(inf[d] for d in ds)
    peak_un = max(un[d] for d in ds)
    return {"t": [_t(d) for d in ds], "ff": [ff[d] for d in ds], "inflation": [inf[d] for d in ds],
            "unemployment": [un[d] for d in ds], "peak_ff": peak_ff,
            "peak_ff_date": next(d for d in ds if ff[d] == peak_ff), "peak_inf": peak_inf,
            "peak_inf_date": next(d for d in ds if inf[d] == peak_inf), "peak_un": peak_un,
            "peak_un_date": next(d for d in ds if un[d] == peak_un), "core_1980": ann[1980], "core_1985": ann[1985],
            "gap_t": [_t(d) for d in q], "gap": gap_q, **{f"sac_{k}": v for k, v in s.items()}}


def compute_flat() -> dict:
    inf = _annual_infl("CPILFESL")
    un = _annual_mean(_monthly("UNRATE"))
    nr = _annual_mean({d: v for d, v in _monthly_q("NROU").items()})
    out = {}
    for name, a, b in (("early", 1960, 1983), ("middle", 1984, 1999), ("late", 2000, 2019)):
        ys = [y for y in range(a, b + 1) if y in inf and y - 1 in inf and y in un and y in nr]
        dpi = np.array([inf[y] - inf[y - 1] for y in ys])
        gap = np.array([un[y] - nr[y] for y in ys])
        slope = float(np.polyfit(gap, dpi, 1)[0])
        out[name] = {"years": ys, "dpi": dpi.tolist(), "gap": gap.tolist(), "slope": slope}
    return out


def _monthly_q(key: str) -> dict:
    """A quarterly series repeated for each month of its quarter (so annual means work)."""
    d = data.fred(key)
    out = {}
    for x, v in zip(d["date"], d["value"]):
        if not np.isfinite(v):
            continue
        y, m = int(x[:4]), int(x[5:7])
        for k in range(3):
            out[f"{y}-{m + k:02d}-01"] = v
    return out


def compute_surge() -> dict:
    core = _yoy("CPILFESL")
    head = _yoy("CPIAUCSL")
    jo = _monthly("JTSJOL")
    ue = _monthly("UNEMPLOY")
    mich = _monthly("MICH")
    be = _monthly("T5YIEM")
    ds = sorted(d for d in core if "2019-01-01" <= d and d in head)
    vu = {d: jo[d] / ue[d] for d in jo if d in ue}
    ds2 = sorted(d for d in vu if "2001-01-01" <= d and d in core)
    return {"t": [_t(d) for d in ds], "core": [core[d] for d in ds], "headline": [head[d] for d in ds],
            "peak_head": max(head[d] for d in ds), "peak_head_date": max(ds, key=lambda d: head[d]),
            "peak_core": max(core[d] for d in ds), "vu_t": [_t(d) for d in ds2], "vu": [vu[d] for d in ds2],
            "vu_core": [core[d] for d in ds2], "vu_peak": max(vu[d] for d in ds2),
            "vu_peak_date": max(ds2, key=lambda d: vu[d]),
            "mich_t": [_t(d) for d in sorted(mich) if d >= "2019-01-01"],
            "mich": [mich[d] for d in sorted(mich) if d >= "2019-01-01"],
            "be_t": [_t(d) for d in sorted(be) if d >= "2019-01-01"],
            "be": [be[d] for d in sorted(be) if d >= "2019-01-01"],
            "be_max": max(be[d] for d in be if d >= "2019-01-01"), "mich_max": max(mich[d] for d in mich
                                                                                 if d >= "2019-01-01")}


def compute_transitory() -> dict:
    pce = _monthly("PCEPI")

    def q4(y):
        return np.mean([pce[f"{y}-{m:02d}-01"] for m in (10, 11, 12)])
    return {"projected_2021": 3.4, "projected_2022": 2.1, "actual_2021": float(100 * (q4(2021) / q4(2020) - 1)),
            "actual_2022": float(100 * (q4(2022) / q4(2021) - 1)),
            "actual_2023": float(100 * (q4(2023) / q4(2022) - 1))}


def compute_persistence() -> dict:
    inf = _annual_infl("CPIAUCSL")
    out = {}
    for name, a, b in (("all", 1950, 2025), ("1960_1983", 1960, 1983), ("1984_2019", 1984, 2019)):
        out[name] = ex.persistence([inf[y] for y in range(a, b + 1) if y in inf])
    q = _yoy("CPIAUCSL")
    qs = sorted(d for d in q if d.endswith(("-01-01", "-04-01", "-07-01", "-10-01")) and d >= "1960-01-01")
    out["quarterly_all"] = ex.persistence([q[d] for d in qs])
    return out


def compute_expect() -> dict:
    mich = _monthly("MICH")
    head = _yoy("CPIAUCSL")
    ds = sorted(d for d in mich if d in head)
    # what households expected for the next twelve months against what happened over them
    later = {}
    for d in ds:
        y, m = int(d[:4]), int(d[5:7])
        nxt = f"{y + 1}-{m:02d}-01"
        if nxt in head:
            later[d] = head[nxt]
    dl = sorted(later)
    err = np.array([mich[d] - later[d] for d in dl])
    return {"t": [_t(d) for d in ds], "mich": [mich[d] for d in ds], "actual": [head[d] for d in ds],
            "mean_gap": float(err.mean()), "mean_abs": float(np.abs(err).mean()), "n": len(dl),
            "mich_mean_2010s": float(np.mean([mich[d] for d in ds if "2010-01-01" <= d < "2020-01-01"])),
            "cpi_mean_2010s": float(np.mean([head[d] for d in ds if "2010-01-01" <= d < "2020-01-01"]))}


FILM_SECONDS = 40.0
MELODY_SECONDS = FILM_SECONDS + 8.0


def film_time(t: float, first: float = 1948.0, last: float = 2026.0) -> float:
    return 1.5 + FILM_SECONDS * (t - first) / (last - first)


def compute_film() -> dict:
    inf = _yoy("CPIAUCSL")
    un = _monthly("UNRATE")
    ds = sorted(d for d in inf if d in un and d >= "1948-01-01")
    return {"t": [_t(d) for d in ds], "inflation": [inf[d] for d in ds], "unemployment": [un[d] for d in ds],
            "times": [film_time(_t(d)) for d in ds]}


def compute_melody() -> dict:
    from explainer.music.monochord.audio import Clip, ClipStore

    f = compute_film()
    t = np.array(f["t"])
    vals = np.array(f["inflation"])
    times = [film_time(x) for x in t]
    mel = score.data_melody(vals - vals.min() + 1.0, MELODY_SECONDS, times=times, act=6, log=False, low=42,
                            high=86)
    events = {"film_end": film_time(t[-1]) + 6.0, "first": times[0], "half": times[len(times) // 2]}
    clip = Clip(mel["y"], score.SR, events=events,
                notes=[{"t": float(tt), "dur": 0.2, "hz": score.hz(nn), "name": f"{x:.1f}"}
                       for tt, nn, x in zip(times, mel["notes"], vals)],
                meta={"label": "American consumer-price inflation over twelve months, month by month, 1948-2025 (BLS "
                               "via FRED), as a tune (computed)", "kind": "synthesized"})
    ClipStore("econ28").save("intermission.melody", clip)
    return {"times": times, "notes": mel["notes"], "seconds": MELODY_SECONDS}


ITEMS = {
    "us": compute_us,
    "phillips": compute_phillips,
    "play": compute_play,
    "accelerate": compute_accelerate,
    "adaptive": compute_adaptive,
    "islands": compute_islands,
    "critique": compute_critique,
    "bg": compute_bg,
    "volcker": compute_volcker,
    "flat": compute_flat,
    "surge": compute_surge,
    "transitory": compute_transitory,
    "persistence": compute_persistence,
    "expect": compute_expect,
    "film": compute_film,
    "melody": compute_melody,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
