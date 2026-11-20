"""Lab 24: looking for work: McCall's reservation wage, the matching function and Shimer's flows measured on American
data, the Diamond-Mortensen-Pissarides model and its comparative statics, Hosios's condition, and the volatility
puzzle."""

import numpy as np

from videos.coursekit import labs
from explainer.economics import data
from explainer.economics.agora import search as sr
from explainer.economics.island import truths

TITLE = "Looking for work: search, matching and the volatility puzzle"
GOAL = ("Find the best stopping rule for a job searcher; measure job finding, separation and the matching function on "
        "American data; solve the DMP model and move its parameters; find the efficient bargaining share; and see why "
        "the model's unemployment barely moves.")
TASKS = [
    "McCall: double the benefit. How much longer does the searcher expect to look, and what happens to the average "
    "accepted wage?",
    "DMP: lower matching efficiency A by a fifth. Do unemployment and vacancies both rise, as on the shifted Beveridge "
    "curve?",
    "Volatility: keep Shimer's numbers but raise b from 0.4 to 0.8. How large is the elasticity of tightness now, and "
    "how does the fundamental surplus formula predict it?",
]


def _monthly(*keys):
    out = {k: dict(zip(data.fred(k)["date"], data.fred(k)["value"])) for k in keys}
    dates = sorted(set.intersection(*[set(o) for o in out.values()]))
    return dates, {k: np.array([out[k][d] for d in dates], float) for k in keys}


def run(seed=0):
    lab = labs.Lab()
    T = truths(24)

    p = T["playit"]
    w = np.linspace(p["low"], p["high"], 1001)
    m = sr.mccall(b=p["b"], beta=p["beta"], wages=w)
    x = (-1 + np.sqrt(1 + 4 * 0.095 * 110)) / (2 * 0.095)   # the closed form: w* - 40 = 0.095 (150 - w*)^2
    assert abs(m["reservation"] - (150 - x)) < 0.2
    lab.row("McCall: reservation wage; chance an offer is taken; months of search",
            f"{m['reservation']:.1f}; {100 * m['accept']:.0f}%; {m['duration']:.1f}")

    # Shimer's flows from the CPS, 1948 to 2025
    dates, v = _monthly("UNEMPLOY", "UEMPLT5", "CLF16OV")
    keep = [k for k, d in enumerate(dates) if d < "2025-09" and all(np.isfinite(v[s][k]) for s in v)]
    corr = [1.1 if dates[k] >= "1994-02" else 1.0 for k in keep]
    fl = sr.flows(v["UNEMPLOY"][keep], v["UEMPLT5"][keep], v["CLF16OV"][keep], correction=corr)
    f, s = np.array(fl["f"]), np.array(fl["s"])
    assert 0.3 < f.mean() < 0.8 and 0.01 < s.mean() < 0.06
    lab.row("CPS flows, monthly: job finding; separation; implied steady state",
            f"{100 * f.mean():.0f}%; {100 * s.mean():.1f}%; {100 * s.mean() / (s.mean() + f.mean()):.1f}%")

    # the matching function: the job-finding rate against openings per unemployed worker, 2001-2019, quarterly
    d2, v2 = _monthly("JTSJOL", "UNEMPLOY")
    vu = {d: j / u for d, j, u in zip(d2, v2["JTSJOL"], v2["UNEMPLOY"]) if np.isfinite(j) and np.isfinite(u)}
    t = [dates[k] for k in keep][1:]
    q = {}
    for d, ff in zip(t, f):
        if d in vu and "2001" <= d[:4] <= "2019":
            q.setdefault((d[:4], (int(d[5:7]) - 1) // 3), []).append((np.log(ff), np.log(vu[d])))
    pts = np.array([np.mean(z, axis=0) for z in q.values() if len(z) == 3])
    slope = np.polyfit(pts[:, 1], pts[:, 0], 1)[0]
    assert 0.2 < slope < 0.7
    lab.row("matching: slope of ln f on ln(V/U), 2001-2019; eta", f"{slope:.2f}; {1 - slope:.2f}")

    kw = T["dmp"]
    st = sr.dmp_steady(**kw)
    lab.row("DMP Island: tightness; wage; unemployment; vacancies",
            f"{st['theta']:.2f}; {st['w']:.3f}; {100 * st['u']:.2f}%; {100 * st['v']:.2f}%")
    rows = []
    for name, ch in (("benefit +0.1", {"b": kw["b"] + 0.1}), ("productivity +5%", {"p": 1.05 * kw["p"]}),
                     ("separations x1.5", {"s": 1.5 * kw["s"]}), ("worker share +0.1", {"beta": kw["beta"] + 0.1})):
        rows.append(f"{name}: {100 * sr.dmp_steady(**{**kw, **ch})['u']:.2f}%")
    lab.row("DMP: unemployment after one change at a time", "; ".join(rows))

    h = sr.hosios(**{k: val for k, val in kw.items() if k not in ("beta", "r")})
    assert abs(h["best"] - kw["eta"]) < 0.02
    lab.row("Hosios: the bargaining share that maximizes net output", f"{h['best']:.2f} (eta = {kw['eta']})")

    sh = T["shimer"]
    cal = {"b": sh["b"], "beta": sh["beta"], "eta": sh["eta"], "A": sh["f"], "s": sh["s"], "r": sh["r"]}
    cal["c"] = (1 - cal["beta"]) * (1 - cal["b"]) / ((cal["r"] + cal["s"]) / cal["A"] + cal["beta"])
    e = sr.elasticity(**cal)["theta"]
    hm = T["hm"]
    cal2 = {**cal, "b": hm["b"], "beta": hm["beta"], "eta": hm["eta"]}
    cal2["c"] = (1 - cal2["beta"]) * (1 - cal2["b"]) / ((cal2["r"] + cal2["s"]) / cal2["A"] + cal2["beta"])
    e2 = sr.elasticity(**cal2)["theta"]
    assert e < 3 < 20 < e2
    lab.row("volatility: d ln theta / d ln p, Shimer's numbers; small surplus", f"{e:.1f}; {e2:.0f}")

    lab.note = ("A searcher stops at the first offer above a reservation wage. On American data about half the "
                "unemployed find work each month and about 3% of the employed lose or leave their jobs into "
                "unemployment; job finding rises with openings per searcher with an elasticity near a half. In the DMP "
                "model unemployment and vacancies coexist for ever, the market is efficient only if the worker's share "
                "equals the matching elasticity, and productivity barely moves unemployment unless the surplus from "
                "working is small.")

    fig, ax = labs.figure(2, size=(11, 4.4))
    yrs = [int(d[:4]) + (int(d[5:7]) - 1) / 12 for d in t]
    ax[0].plot(yrs, 100 * f, color=labs.BLUE, lw=0.8, label="job finding")
    ax[0].plot(yrs, 100 * 10 * s, color=labs.ORANGE, lw=0.8, label="separation x 10")
    ax[0].set(title="Shimer's flows from the CPS", xlabel="year", ylabel="% a month")
    ax[0].legend()
    th = np.linspace(0.1, 4, 200)
    cv = sr.dmp_curves(th, **kw)
    ax[1].plot(th, cv["jc"], color=labs.ORANGE, label="job creation")
    ax[1].plot(th, cv["wc"], color=labs.BLUE, label="wage curve")
    ax[1].scatter([st["theta"]], [st["w"]], color="black", zorder=3)
    ax[1].set(title="The DMP Island", xlabel="tightness", ylabel="wage", ylim=(0.85, 1.05))
    ax[1].legend()
    lab.fig = fig
    return lab
