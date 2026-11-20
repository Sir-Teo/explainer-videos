"""Precompute every number in Part 24 of *Economics, Built* ("Looking for Work").

    python -m videos.economics.econ24.compute            # everything missing (seconds)
    python -m videos.economics.econ24.compute --force dmp

Results are cached in ``.cache/econ24/<name>.json`` (+ ``.npz``); scenes call ``load(name)``.  Data: the Data Room
(``explainer.economics.data``: FRED's unemployment by duration, the labour force, JOLTS openings, hires, separations
and quits, CBO's natural rate, output per hour).  Models: Agora's labour market with frictions (``agora.search``),
with the Island's Part 24 truths.

Items:
    diamond      Diamond's coconut island: the share who climb against the share who expect partners
    jolts        hires and separations a month against the net change in jobs, 2001-2026
    playit       the game's ten offers and the optimal stopping rule
    mccall       the reservation wage against the benefit and against patience
    beveridge    the US Beveridge curve from JOLTS, 2000-2026, by period
    matching     the matching function estimated on JOLTS: hires against openings and unemployment, and the
                 unemployed's job-finding rate against openings per unemployed worker
    dmp          the Island's DMP steady state, its two curves, and comparative statics
    path         unemployment after a permanent fall in productivity
    hosios       net output against the bargaining share
    volatility   the volatility puzzle: elasticities under Shimer's and Hagedorn and Manovskii's calibrations, and
                 the data's volatility of tightness against productivity
    flows        Shimer's job-finding and separation rates since 1948 and the ins-and-outs decomposition
    ladder       the Burdett-Mortensen job ladder
    natural      CBO's natural rate against the unemployment rate; long-term unemployment's share
    film         the intermission's data film: the Beveridge curve month by month, 2000-2026
    melody       its data melody: openings per unemployed worker
"""

from __future__ import annotations

import numpy as np

from explainer.ai.cache import Cache
from explainer.economics import data, island, score
from explainer.economics.agora import search as sr

CACHE = Cache("econ24")
load = CACHE.load
TRUTH = island.truths(24)
RULES = (80, 100, 120, 140)   # the four stopping rules of the game


def _series(*keys):
    """Several FRED series on the dates they share."""
    out = {k: dict(zip(data.fred(k)["date"], data.fred(k)["value"])) for k in keys}
    d = sorted(set.intersection(*[set(o) for o in out.values()]))
    return d, {k: np.array([out[k][x] for x in d], float) for k in keys}


def compute_diamond() -> dict:
    """Islanders draw a climbing cost from a logistic spread around 0.6; each climbs if the cost is below the expected
    gain, ``contact x gain x e``, where e is the share who climb.  Equilibria are fixed points of
    ``e = G(contact gain e)``: one with nobody climbing, one with most climbing, and an unstable one between."""
    T = TRUTH["diamond"]
    e = np.linspace(0, 1, T["grid"] + 1)
    G = 1 / (1 + np.exp(-(T["contact"] * T["gain"] * e - 0.6) / 0.08))
    G0 = 1 / (1 + np.exp(0.6 / 0.08))
    G = (G - G0) / (1 - G0)
    cross = []
    diff = G - e
    for k in range(len(e) - 1):
        if diff[k] == 0 or diff[k] * diff[k + 1] < 0:
            cross.append(float(e[k] - diff[k] * (e[k + 1] - e[k]) / (diff[k + 1] - diff[k])))
    if 0.0 not in cross:
        cross = [0.0] + cross
    return {"e": e.tolist(), "G": G.tolist(), "equilibria": sorted(set(round(c, 4) for c in cross)), **T}


def compute_jolts() -> dict:
    d, v = _series("JTSHIL", "JTSTSL", "JTSQUL", "JTSJOL")
    m = np.isfinite(v["JTSHIL"]) & np.isfinite(v["JTSTSL"])
    t = [int(x[:4]) + (int(x[5:7]) - 1) / 12 for x, ok in zip(d, m) if ok]
    H, S, Q = v["JTSHIL"][m], v["JTSTSL"][m], v["JTSQUL"][m]
    pre = np.array([x < 2020 for x in t])
    return {"t": t, "hires": H.tolist(), "seps": S.tolist(), "quits": Q.tolist(), "net": (H - S).tolist(),
            "mean_hires": float(H[pre].mean()), "mean_seps": float(S[pre].mean()),
            "mean_net": float((H - S)[pre].mean()), "mean_quits": float(Q[pre].mean()),
            "apr2020_seps": float(S[np.argmin(np.abs(np.array(t) - 2020.25))])}


def compute_playit() -> dict:
    p = TRUTH["playit"]
    w = np.linspace(p["low"], p["high"], 1001)
    m = sr.mccall(b=p["b"], beta=p["beta"], wages=w)
    offers = list(p["offers"])
    k = next((i for i, o in enumerate(offers) if o >= m["reservation"]), None)
    rules = []
    for R in RULES:
        # this draw: the first offer at or above R, and the discounted value of what it brought
        kk = next((i for i, o in enumerate(offers) if o >= R), None)
        if kk is None:
            got = p["b"] * (1 - p["beta"] ** len(offers)) / (1 - p["beta"])
        else:
            got = p["b"] * (1 - p["beta"] ** kk) / (1 - p["beta"]) + p["beta"] ** kk * offers[kk] / (1 - p["beta"])
        # before the draw: the expected value of the rule, V = (b + beta P E[w | w >= R] / (1-beta)) / (1 - beta(1-P))
        P = float(np.mean(w >= R))
        Ew = float(w[w >= R].mean())
        V = (p["b"] + p["beta"] * P * Ew / (1 - p["beta"])) / (1 - p["beta"] * (1 - P))
        rules.append({"R": R, "k": kk, "wage": offers[kk] if kk is not None else None, "value_here": float(got),
                      "value": float(V), "equivalent": float(V * (1 - p["beta"])), "accept": P,
                      "months": 1 / P})
    return {**p, "reservation": m["reservation"], "accept": m["accept"], "duration": m["duration"],
            "first_accept": k, "accepted": offers[k] if k is not None else None, "rules": rules,
            "best_value": float(m["U"]), "mean_offer": float(np.mean(w)), "best_in_hindsight": max(offers)}


def compute_mccall() -> dict:
    p = TRUTH["playit"]
    w = np.linspace(p["low"], p["high"], 1001)
    bs = np.linspace(0, 120, 49)
    by_b = [sr.mccall(b=float(b), beta=p["beta"], wages=w) for b in bs]
    betas = np.linspace(0.5, 0.99, 50)
    by_beta = [sr.mccall(b=p["b"], beta=float(x), wages=w) for x in betas]
    return {"b": bs.tolist(), "res_b": [x["reservation"] for x in by_b], "dur_b": [x["duration"] for x in by_b],
            "beta": betas.tolist(), "res_beta": [x["reservation"] for x in by_beta],
            "dur_beta": [x["duration"] for x in by_beta]}


def compute_beveridge() -> dict:
    d, v = _series("UNEMPLOY", "CLF16OV", "JTSJOL")
    out = []
    for x, u, l, j in zip(d, v["UNEMPLOY"], v["CLF16OV"], v["JTSJOL"]):
        if np.isfinite(u) and np.isfinite(l) and np.isfinite(j):
            out.append((int(x[:4]) + (int(x[5:7]) - 1) / 12, 100 * u / l, 100 * j / (l + j - u), x))
    t, ur, vr, dates = zip(*out)
    periods = [("2000-12", "2008-12", r"2001--2008"), ("2009-01", "2019-12", r"2009--2019"),
               ("2020-01", "2021-06", r"2020--mid 2021"), ("2021-07", "2026-12", r"mid 2021--2026")]
    segs = []
    for a, b, name in periods:
        idx = [k for k, x in enumerate(dates) if a <= x[:7] <= b]
        segs.append({"name": name, "u": [ur[k] for k in idx], "v": [vr[k] for k in idx]})
    vu = np.array(vr) / np.array(ur)
    k = int(np.argmax(vu))
    return {"t": list(t), "u": list(ur), "v": list(vr), "dates": list(dates), "segments": segs,
            "peak_vu": float(vu[k]), "peak_when": dates[k], "last_u": ur[-1], "last_v": vr[-1], "last": dates[-1]}


def compute_matching() -> dict:
    """log(hires / U) on log(openings / U), monthly, 2001-2019: the slope is 1 - eta under constant returns; the
    unrestricted regression of log hires on log U and log V tests constant returns."""
    d, v = _series("JTSHIL", "JTSJOL", "UNEMPLOY")
    m = np.isfinite(v["JTSHIL"]) & np.isfinite(v["JTSJOL"]) & np.isfinite(v["UNEMPLOY"]) & np.array(
        ["2001" <= x[:4] <= "2019" for x in d])
    H, V, U = v["JTSHIL"][m], v["JTSJOL"][m], v["UNEMPLOY"][m]
    y, x = np.log(H / U), np.log(V / U)
    b1, b0 = np.polyfit(x, y, 1)
    X = np.column_stack([np.ones(len(H)), np.log(U), np.log(V)])
    coef = np.linalg.lstsq(X, np.log(H), rcond=None)[0]
    # the unemployed's own job-finding rate (chapter 10's f, quarterly) against openings per unemployed worker
    fl = compute_flows()
    fm = {round(t, 2): ff for t, ff in zip(fl["t"], fl["f"])}
    q = {}
    for xd, j, u in zip(d, v["JTSJOL"], v["UNEMPLOY"]):
        if np.isfinite(j) and np.isfinite(u):
            q.setdefault((int(xd[:4]), (int(xd[5:7]) - 1) // 3), []).append(j / u)
    fx, fy, ft = [], [], []
    for k_, vals in sorted(q.items()):
        tq = round(k_[0] + k_[1] / 4, 2)
        if len(vals) == 3 and tq in fm and 2001 <= k_[0] <= 2019:
            fx.append(float(np.log(np.mean(vals))))
            fy.append(float(np.log(fm[tq])))
            ft.append(tq)
    c1, c0 = np.polyfit(fx, fy, 1)
    return {"slope": float(b1), "eta": float(1 - b1), "x": x.tolist(), "y": y.tolist(), "intercept": float(b0),
            "free_u": float(coef[1]), "free_v": float(coef[2]), "sum": float(coef[1] + coef[2]), "n": int(m.sum()),
            "f_x": fx, "f_y": fy, "f_t": ft, "f_slope": float(c1), "f_eta": float(1 - c1), "f_intercept": float(c0),
            "f_n": len(fx)}


def compute_dmp() -> dict:
    T = TRUTH["dmp"]
    st = sr.dmp_steady(**T)
    th = np.linspace(0.05, 4.0, 200)
    curves = sr.dmp_curves(th, **T)
    statics = {}
    for name, change in (("benefit up", {"b": T["b"] + 0.1}), ("productivity up", {"p": T["p"] * 1.05}),
                         ("separations up", {"s": T["s"] * 1.5}), ("bargaining up", {"beta": T["beta"] + 0.1})):
        x = sr.dmp_steady(**{**T, **change})
        c = sr.dmp_curves(th, **{**T, **change})
        statics[name] = {"steady": x, "curves": c}
    rest = {k: v for k, v in T.items() if k not in ("p", "A")}
    bev = sr.beveridge(ps=np.linspace(0.8, 1.2, 41), As=(T["A"], 0.8 * T["A"]), **rest)
    return {"steady": st, "curves": curves, "statics": statics, "bev": bev["curves"], **T}


def compute_path() -> dict:
    T = TRUTH["dmp"]
    return {**sr.dmp_path(p0=T["p"], p1=0.97 * T["p"], months=36, **{k: v for k, v in T.items() if k != "p"})}


def compute_hosios() -> dict:
    T = TRUTH["dmp"]
    kw = {k: v for k, v in T.items() if k not in ("beta", "r")}
    return sr.hosios(**kw)


def _calibrated(spec):
    """Vacancy cost chosen so that tightness is one: ``c = (1-beta)(p-b) / ((r+s)/A + beta)``, with A = f."""
    A = spec["f"]
    c = (1 - spec["beta"]) * (1 - spec["b"]) / ((spec["r"] + spec["s"]) / A + spec["beta"])
    return {"b": spec["b"], "beta": spec["beta"], "eta": spec["eta"], "A": A, "s": spec["s"], "r": spec["r"], "c": c}


def compute_volatility() -> dict:
    sh = _calibrated(TRUTH["shimer"])
    hm = _calibrated(TRUTH["hm"])
    e_sh = sr.elasticity(**sh)
    e_hm = sr.elasticity(**hm)
    # the data: quarterly v/u (JOLTS) and output per hour, 2001-2019, logs, HP-filtered (lambda 1e5)
    d, v = _series("JTSJOL", "UNEMPLOY")
    q = {}
    for x, j, u in zip(d, v["JTSJOL"], v["UNEMPLOY"]):
        if np.isfinite(j) and np.isfinite(u) and "2001" <= x[:4] <= "2019":
            q.setdefault((int(x[:4]), (int(x[5:7]) - 1) // 3), []).append(j / u)
    keys = sorted(k for k in q if len(q[k]) == 3)
    vu = np.log(np.array([np.mean(q[k]) for k in keys]))
    P = data.fred("OPHNFB")
    pm = {(int(x[:4]), (int(x[5:7]) - 1) // 3): val for x, val in zip(P["date"], P["value"])}
    pr = np.log(np.array([pm[k] for k in keys]))
    c_vu = vu - sr.hp_filter(vu)
    c_p = pr - sr.hp_filter(pr)
    return {"shimer": {**sh, "elasticity": e_sh["theta"], "u": e_sh["steady"]["u"]},
            "hm": {**hm, "elasticity": e_hm["theta"], "u": e_hm["steady"]["u"]},
            "t": [k[0] + k[1] / 4 for k in keys], "c_vu": c_vu.tolist(), "c_p": c_p.tolist(),
            "sd_vu": float(c_vu.std()), "sd_p": float(c_p.std()), "ratio": float(c_vu.std() / c_p.std()),
            "quarters": len(keys), "shimer_paper": {"sd_vu": 0.382, "sd_p": 0.020}}


def compute_flows() -> dict:
    d, v = _series("UNEMPLOY", "UEMPLT5", "CLF16OV")
    idx = [k for k, x in enumerate(d) if x < "2025-09" and all(np.isfinite(v[s][k]) for s in v)]
    dates = [d[k] for k in idx]
    corr = [1.1 if x >= "1994-02" else 1.0 for x in dates]
    fl = sr.flows(v["UNEMPLOY"][idx], v["UEMPLT5"][idx], v["CLF16OV"][idx], correction=corr)
    t = dates[1:]
    q = {}
    for x, ff, ss in zip(t, fl["f"], fl["s"]):
        q.setdefault((int(x[:4]), (int(x[5:7]) - 1) // 3), []).append((ff, ss))
    keys = sorted(k for k in q if len(q[k]) == 3)
    fq = np.array([np.mean([a for a, _ in q[k]]) for k in keys])
    sq = np.array([np.mean([b for _, b in q[k]]) for k in keys])
    yr = [k[0] + k[1] / 4 for k in keys]
    io = sr.ins_outs(fq, sq)
    since87 = np.array(yr) >= 1987
    io87 = sr.ins_outs(fq[since87], sq[since87])
    return {"t": yr, "f": fq.tolist(), "s": sq.tolist(), "share_f": io["share_f"], "share_s": io["share_s"],
            "share_f_87": io87["share_f"], "share_s_87": io87["share_s"], "steady": io["steady"],
            "only_f": io["only_f"], "only_s": io["only_s"], "mean_f": float(fq.mean()), "mean_s": float(sq.mean())}


def compute_ladder() -> dict:
    return sr.burdett_mortensen(**TRUTH["ladder"])


def compute_natural() -> dict:
    U = data.fred("UNRATE")
    N = data.fred("NROU")
    nmap = {x: val for x, val in zip(N["date"], N["value"])}
    t, u, n = [], [], []
    for x, val in zip(U["date"], U["value"]):
        key = f"{x[:4]}-{(int(x[5:7]) - 1) // 3 * 3 + 1:02d}-01"
        if np.isfinite(val) and key in nmap:
            t.append(int(x[:4]) + (int(x[5:7]) - 1) / 12)
            u.append(val)
            n.append(nmap[key])
    d, v = _series("UEMP27OV", "UNEMPLOY")
    lt = [(int(x[:4]) + (int(x[5:7]) - 1) / 12, 100 * a / b) for x, a, b in zip(d, v["UEMP27OV"], v["UNEMPLOY"])
          if np.isfinite(a) and np.isfinite(b)]
    k = int(np.argmax([s for _, s in lt]))
    return {"t": t, "u": u, "nrou": n, "lt_t": [a for a, _ in lt], "lt_share": [b for _, b in lt],
            "lt_peak": lt[k][1], "lt_peak_when": lt[k][0], "nrou_last": n[-1], "u_last": u[-1],
            "nrou_1979": nmap.get("1979-01-01"), "nrou_2025": nmap.get("2025-01-01")}


FILM_SECONDS = 40.0
MELODY_SECONDS = FILM_SECONDS + 8.0


def film_time(t: float, first: float = 2000.92, last: float = 2026.75) -> float:
    return 1.5 + FILM_SECONDS * (t - first) / (last - first)


def compute_film() -> dict:
    b = compute_beveridge()
    t = np.array(b["t"])
    return {"t": t.tolist(), "u": b["u"], "v": b["v"], "times": [film_time(x) for x in t],
            "vu": (np.array(b["v"]) / np.array(b["u"])).tolist(), "first": float(t[0]), "last": float(t[-1])}


def compute_melody() -> dict:
    from explainer.music.monochord.audio import Clip, ClipStore

    f = compute_film()
    t = np.array(f["t"])
    qs = np.arange(t[0], t[-1] + 1e-9, 0.25)
    vals = np.interp(qs, t, f["vu"])
    times = [film_time(x) for x in qs]
    mel = score.data_melody(vals, MELODY_SECONDS, times=times, act=5, log=True, low=45, high=84)
    events = {"film_end": film_time(t[-1]) + 6.0, "first": times[0], "half": times[len(times) // 2]}
    clip = Clip(mel["y"], score.SR, events=events,
                notes=[{"t": float(tt), "dur": 0.2, "hz": score.hz(nn), "name": f"{x:.2f}"}
                       for tt, nn, x in zip(times, mel["notes"], qs)],
                meta={"label": "job openings per unemployed worker, quarter by quarter, 2001-2026 (BLS via FRED), as a "
                               "tune (computed)", "kind": "synthesized"})
    ClipStore("econ24").save("intermission.melody", clip)
    return {"times": times, "notes": mel["notes"], "quarters": qs.tolist(), "seconds": MELODY_SECONDS}


ITEMS = {
    "diamond": compute_diamond,
    "jolts": compute_jolts,
    "playit": compute_playit,
    "mccall": compute_mccall,
    "beveridge": compute_beveridge,
    "matching": compute_matching,
    "dmp": compute_dmp,
    "path": compute_path,
    "hosios": compute_hosios,
    "volatility": compute_volatility,
    "flows": compute_flows,
    "ladder": compute_ladder,
    "natural": compute_natural,
    "film": compute_film,
    "melody": compute_melody,
}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
