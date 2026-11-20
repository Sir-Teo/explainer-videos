"""Precompute every number in Part 42 of *Economics, Built* ("Social Insurance").

    python -m videos.economics.econ42.compute            # everything missing (about half a minute)
    python -m videos.economics.econ42.compute --force baily

Results are cached in ``.cache/econ42/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.  Data: the Data Room
(``explainer.economics.data``: from FRED, continued and initial claims for unemployment insurance, the insured
unemployment rate, benefits paid and the median duration of unemployment, with the number unemployed; the tables of
the Oregon experiment, RAND, Arrow, Baily and Chetty, Meyer, Card, Chetty and Weber, Schmieder, von Wachter and
Bender, Gruber, Ganong and Noel, Madrian and Shea, Chetty et al., Maestas, Mullen and Strand, the IRS and Eissa and
Liebman, Robins, the basic income trials, Hendren and Sprung-Keyser, Finkelstein, Hendren and Luttmer, the Social
Security trustees and the 1983 amendments).  Models: Agora's insurance (``agora.insurance``) with the Island's Part
42 truths.

Items:
    pooling      the spread of the claim per member against the pool's size, independent and correlated risks
    claims       America's continued claims against the unemployed: the share receiving benefits
    baily        the static model: welfare, both sides of the formula, the optimum, the liquidity split
    formula      the formula with Gruber's and Ganong and Noel's drops: the risk aversion that justifies benefits
    weekly       the weekly model: the hazard by week, durations against the benefit and its length
    health       coinsurance: spending, risk premium and overuse; the optimum; RAND-style elasticities
    lottery      the Island's Oregon: 200 lotteries, the first stage and the Wald estimates
    pensions     pay-as-you-go arithmetic: replacement, returns, the implicit debt
    defaults     enrolment month by month under opt-in and automatic enrolment
    examiners    disability examiners: the naive gap against the leniency instrument
    eitc         the 2025 schedule, marginal rates, the Island's EITC and its MVPF; tagging
    ubi          a basic income financed by a flat tax on the Island
    mvpf         the MVPF of the Island's policies
    film         the intermission's data film: continued claims, 1967-2026
    melody       its data melody
"""

from __future__ import annotations

import numpy as np

from explainer.ai.cache import Cache
from explainer.economics import data, island, score
from explainer.economics.agora import insurance as I
from explainer.economics.data import tables

CACHE = Cache("econ42")
load = CACHE.load
TRUTH = island.truths(42)
FILM_SECONDS = 52.0
MELODY_SECONDS = FILM_SECONDS + 8.0
B_GRID = np.round(np.linspace(0.02, 0.60, 59), 4)


def baily_model() -> I.Baily:
    return I.Baily(**TRUTH["baily"])


def health_model() -> I.Health:
    return I.Health(**TRUTH["health"])


def weekly_kw() -> dict:
    W = dict(TRUTH["weekly"])
    W.pop("b")
    W.pop("K")
    return W


def compute_pooling() -> dict:
    P = TRUTH["pooling"]
    ns = np.unique(np.round(np.logspace(1, 6, 60)))
    r = I.pooling(ns, **P)
    marks = {str(int(n)): I.pooling([n], **P) for n in (100, 10000, 1000000)}
    return {**r, **P, "marks": {k: {"independent": v["independent"][0], "correlated": v["correlated"][0]}
                                 for k, v in marks.items()}}


def _monthly(series: str) -> dict:
    d = data.fred(series)
    out: dict = {}
    for t, v in zip(d["date"], d["value"]):
        if np.isfinite(v):
            out.setdefault(t[:7], []).append(v)
    return {k: float(np.mean(v)) for k, v in out.items()}


def compute_claims() -> dict:
    cc = _monthly("CCSA")
    un = _monthly("UNEMPLOY")
    ms = sorted(set(cc) & set(un))
    years = sorted({int(m[:4]) for m in ms})
    share = {y: float(np.mean([cc[m] / (un[m] * 1000) for m in ms if int(m[:4]) == y])) for y in years}
    ys = [y for y in years if sum(1 for m in ms if int(m[:4]) == y) >= 6]
    med = _monthly("UEMPMED")
    my = {y: float(np.mean([v for m, v in med.items() if int(m[:4]) == y])) for y in ys if
          any(int(m[:4]) == y for m in med)}
    s = np.array([share[y] for y in ys])
    k = int(np.argmax(s))
    return {"years": ys, "share": s.tolist(), "mean": float(s.mean()), "peak_y": ys[k], "peak": float(s[k]),
            "last_y": ys[-1], "last": float(s[-1]), "median_weeks": [my.get(y) for y in ys],
            "y2019": share.get(2019), "y2009": share.get(2009), "y2020": share.get(2020)}


def compute_baily() -> dict:
    m = baily_model()
    rows = [m.sides(float(b)) for b in B_GRID]
    bstar = m.optimum()
    at = m.sides(bstar)
    split = m.split(bstar)
    shares = [m.split(float(b))["share"] for b in B_GRID]
    mv = [I.ui_mvpf(m, float(b)) for b in B_GRID]
    half = m.sides(0.5)
    return {"b": B_GRID.tolist(), "welfare": [r["welfare"] for r in rows], "gain": [r["gain"] for r in rows],
            "cost": [r["cost"] for r in rows], "e": [r["e"] for r in rows], "drop": [r["drop"] for r in rows],
            "tau": [r["tau"] for r in rows], "bstar": bstar, "at": at, "split": split, "shares": shares,
            "mvpf": mv, "half": half, "elasticity_half": m.elasticity(0.5, total=False),
            "options": [0.1, round(bstar, 2), 0.5, 0.75], **TRUTH["baily"]}


def compute_formula() -> dict:
    E = tables.UI_EVIDENCE.data
    drops = {"gruber": E["gruber_drop"] / 100, "exhaust": E["gn_exhaust"] / 100}
    eps = (E["meyer_lo"], E["meyer_hi"])
    need = {k: [e / d for e in eps] for k, d in drops.items()}
    gammas = [1, 2, 4, 8]
    gains = {k: [g * d for g in gammas] for k, d in drops.items()}
    # Chetty's route: a liquidity share L makes the gain L / (1 - L)
    L = tables.UI_THEORY.data["liquidity"] / 100
    return {"drops": drops, "eps": list(eps), "need": need, "gammas": gammas, "gains": gains, "L": L,
            "chetty_gain": L / (1 - L)}


def compute_weekly() -> dict:
    W = TRUTH["weekly"]
    kw = weekly_kw()
    base = I.weekly(W["b"], W["K"], **kw)
    el = I.weekly_elasticities(W["b"], W["K"], **kw)
    bs = np.round(np.linspace(0.3, 0.7, 9), 3)
    durs = [I.weekly(float(b), W["K"], **kw)["duration"] for b in bs]
    a20, a30 = I.weekly(W["b"], 20, **kw), I.weekly(W["b"], 30, **kw)
    f20 = 1 - a20["survival"][20]
    f30 = 1 - a30["survival"][20]
    b10 = I.weekly(W["b"] * 1.1, W["K"], **kw)
    return {"hazard": base["hazard"][:60], "survival": base["survival"][:61], "duration": base["duration"],
            "exhaust": base["exhaust"], "level": el["level"], "length": el["length"], "b_grid": bs.tolist(),
            "durations": durs, "find20_20": f20, "find20_30": f30, "ccw": f30 / f20 - 1,
            "ten_pct": b10["duration"] / base["duration"] - 1, "h0": base["hazard"][0],
            "h_before": base["hazard"][W["K"] - 1], "h_after": base["hazard"][W["K"]], **W}


def compute_health() -> dict:
    h = health_model()
    cs = np.round(np.linspace(0, 1, 41), 4)
    rows = [h.plan(float(c)) for c in cs]
    cstar = h.optimum()
    at = h.plan(cstar)
    plans = {str(c): h.plan(c) for c in (0.0, 0.25, 0.5, 0.95)}
    sp = {k: v["spending"] for k, v in plans.items()}
    return {"c": cs.tolist(), "spending": [r["spending"] for r in rows], "ce": [r["ce"] for r in rows],
            "risk_premium": [r["risk_premium"] for r in rows], "overuse": [r["overuse"] for r in rows],
            "cstar": cstar, "at": at, "plans": plans, "less95": 1 - sp["0.95"] / sp["0.0"],
            "less25": 1 - sp["0.25"] / sp["0.0"], "arc": I.arc_elasticity(sp["0.25"], sp["0.95"], 0.25, 0.95),
            "rand": tables.RAND_HIE.data, **TRUTH["health"]}


def compute_lottery() -> dict:
    L = dict(TRUTH["lottery"])
    runs, seed = L.pop("runs"), L.pop("seed")
    res = [I.lottery(seed=seed + k, **L) for k in range(runs)]
    keys = list(res[0]["outcomes"])
    est = {k: np.array([r["outcomes"][k]["wald"] for r in res]) for k in keys}
    ses = {k: np.array([r["outcomes"][k]["se"] for r in res]) for k in keys}
    fs = np.array([r["first_stage"] for r in res])
    # the run shown is chosen by rule: the one whose first stage is the median, never by its outcomes
    j = int(np.argsort(fs)[len(fs) // 2])
    shown = res[j]
    summary = {}
    for k in keys:
        e, s = est[k], ses[k]
        true = shown["outcomes"][k]["true"]
        cover = float(np.mean(np.abs(e - true) <= 1.96 * s))
        detect = float(np.mean(np.abs(e) > 1.96 * s))
        summary[k] = {"true": true, "mean": float(e.mean()), "sd": float(e.std()), "q05": float(np.quantile(e, 0.05)),
                      "q95": float(np.quantile(e, 0.95)), "se": float(np.median(s)), "coverage": cover,
                      "power": detect, "mde": float(2.8 * np.median(s)), "draws": e.tolist()}
    return {"shown": shown, "first_stage": float(np.median(fs)), "summary": summary, "runs": runs,
            "oregon": tables.OREGON_2008.data, **L}


def compute_pensions() -> dict:
    P = tables.PENSIONS.data
    rows = {str(r): I.payg(workers_per_retiree=r) for r in (P["r1960"], P["r2024"], P["r2035"])}
    return {"rows": rows, "base": I.payg(), **P}


def compute_defaults() -> dict:
    D = dict(TRUTH["defaults"])
    r = I.defaults(**D)
    return {**r, "m15_opt": r["opt_in"][15], "m15_auto": r["auto"][15], "m15_default": r["at_default"][15],
            "ms": tables.MADRIAN_SHEA_2001.data, "dk": tables.CHETTY_DK_2014.data}


def compute_examiners() -> dict:
    X = TRUTH["examiners"]
    return {**I.examiners(**X), "mms": tables.DISABILITY_2013.data}


def compute_eitc() -> dict:
    E = tables.EITC_2025.data
    z = np.linspace(0, 70000, 281)
    credit = I.eitc(z, E["rate_in"], E["top"], E["start_out"], E["rate_out"])
    marg = -np.gradient(credit, z)
    T = TRUTH["tagging"]
    return {"z": z.tolist(), "credit": credit.tolist(), "marginal": marg.tolist(), "check_max": float(credit.max()),
            "check_end": float(E["start_out"] + E["max"] / E["rate_out"]), "mvpf": I.eitc_mvpf(),
            "tagging": I.tagging(**T), "table": E, "nit": tables.NIT_1968.data}


def compute_ubi() -> dict:
    U = TRUTH["ubi"]
    rng = np.random.default_rng(U["seed"])
    x = np.exp(rng.normal(np.log(U["median"]), U["sigma"], U["n"]))
    ts = np.round(np.linspace(0.0, 0.9, 46), 3)
    B0 = [I.basic_income(x, float(t))["B"] for t in ts]
    B1 = [I.basic_income(x, float(t), e=U["e"])["B"] for t in ts]
    at30 = I.basic_income(x, 0.3)
    at30e = I.basic_income(x, 0.3, e=U["e"])
    dec = np.quantile(x, np.linspace(0, 1, 11))
    net = [float(np.mean(at30["B"] - 0.3 * x[(x >= dec[k]) & (x <= dec[k + 1])])) for k in range(10)]
    k = int(np.argmax(B1))
    return {"t": ts.tolist(), "B0": B0, "B1": B1, "at30": at30, "at30e": at30e, "net_by_decile": net,
            "best_t": float(ts[k]), "best_B": float(B1[k]), "trials": tables.UBI_TRIALS.data, **U}


def compute_mvpf() -> dict:
    m = baily_model()
    bstar = m.optimum()
    pts = {"ui_low": {"b": 0.2, "mvpf": I.ui_mvpf(m, 0.2)}, "ui_best": {"b": bstar, "mvpf": I.ui_mvpf(m, bstar)},
           "ui_high": {"b": 0.5, "mvpf": I.ui_mvpf(m, 0.5)}, "eitc": {"mvpf": I.eitc_mvpf()["mvpf"]}}
    # a children's programme that pays for itself: costs 1, raises later earnings whose taxes repay it
    child = {"cost": 1.0, "tax_back": 1.3, "mvpf": I.mvpf(2.0, 1.0, -1.3)}
    return {"points": pts, "child": child, "hs": tables.MVPF_2020.data}


def film_time(t: float, first: float = 1967.0, last: float = 2026.75) -> float:
    return 1.5 + FILM_SECONDS * (t - first) / (last - first)


def compute_film() -> dict:
    cc = _monthly("CCSA")
    q: dict = {}
    for m, v in cc.items():
        y, mo = int(m[:4]), int(m[5:7])
        q.setdefault(y + (mo - 1) // 3 / 4, []).append(v)
    ts = sorted(t for t in q if len(q[t]) == 3 or t == max(q))
    v = [float(np.mean(q[t])) / 1e6 for t in ts]
    k = int(np.argmax(v))
    return {"t": ts, "v": v, "times": [film_time(t) for t in ts], "peak": v[k], "peak_t": ts[k],
            "first": v[0], "last": v[-1], "y1982": float(np.max([x for t, x in zip(ts, v) if 1982 <= t < 1984])),
            "y2009": float(np.max([x for t, x in zip(ts, v) if 2009 <= t < 2010]))}


def compute_melody() -> dict:
    from explainer.music.monochord.audio import Clip, ClipStore

    f = compute_film()
    vals = np.array(f["v"])
    times = f["times"]
    mel = score.data_melody(vals, MELODY_SECONDS, times=times, act=8, log=True, low=40, high=84)
    events = {"film_end": film_time(f["t"][-1]) + 6.0, "first": times[0], "peak": film_time(f["peak_t"])}
    clip = Clip(mel["y"], score.SR, events=events,
                notes=[{"t": float(tt), "dur": 0.3, "hz": score.hz(nn), "name": f"{x:.2f}"}
                       for tt, nn, x in zip(times, mel["notes"], vals)],
                meta={"label": "continued claims for state unemployment insurance, quarterly averages, 1967-2026 "
                               "(U.S. Employment and Training Administration, via FRED), on a log scale, as a tune "
                               "(computed)", "kind": "synthesized"})
    ClipStore("econ42").save("intermission.melody", clip)
    return {"times": times, "notes": mel["notes"], "seconds": MELODY_SECONDS}


ITEMS = {
    "pooling": compute_pooling,
    "claims": compute_claims,
    "baily": compute_baily,
    "formula": compute_formula,
    "weekly": compute_weekly,
    "health": compute_health,
    "lottery": compute_lottery,
    "pensions": compute_pensions,
    "defaults": compute_defaults,
    "examiners": compute_examiners,
    "eitc": compute_eitc,
    "ubi": compute_ubi,
    "mvpf": compute_mvpf,
    "film": compute_film,
    "melody": compute_melody,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
