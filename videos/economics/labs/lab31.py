"""Lab 31: the central bank: the corridor and the floor, four ways to identify a policy shock scored on the Island
against the truth, a recursive VAR on US data with and without commodity prices, output gaps from the data of the day,
the QE1 event study, the natural rate by the Kalman filter, self-fulfilling sovereign yields, and the Greenbook against
the professional forecasters."""

import numpy as np

from videos.coursekit import labs
from explainer.economics import data
from explainer.economics.agora import cb, rbc
from explainer.economics.island import truths

TITLE = "The central bank: setting a rate, and measuring what it does"
GOAL = ("Set a rate in a corridor and on a floor; score four identification methods against a planted truth; find "
        "the price puzzle in US data and shrink it; measure output gaps with the data of the day; recompute the QE1 "
        "event study; estimate a drifting natural rate; find the equilibria of a sovereign-debt market with and "
        "without a backstop; and check whether the Fed's staff forecast inflation better than the private sector.")
TASKS = [
    "Identification: set the information effect to zero and then to one. How does the high-frequency estimate of "
    "output's trough change?",
    "Real time: refit the trend of the day on the last fifteen years of each vintage only. Does the 1970s error "
    "shrink, and what happens in the 2000s?",
    "The euro: lower the backstop's yield to 2.6% and raise it to 5.5%. When does the bad equilibrium survive?",
]


def _series(key, first="0000", last="9999"):
    d = data.fred(key)
    return {x: v for x, v in zip(d["date"], d["value"]) if np.isfinite(v) and first <= x <= last}


def run(seed=0):
    lab = labs.Lab()
    T = truths(31)

    rs = T["reserves"]
    cf = cb.corridor_and_floor(rs["floor"], rs["ceiling"], rs["need"], rs["spread"])
    lab.row("the corridor: reserves at mid-corridor, and the rate's slope per unit", f"{cf['corridor_R']:.0f}, "
            f"{cf['slope_per_unit']:+.3f} points")
    lab.row("the floor: the rate with 300 units of reserves", f"{cf['floor_i']:.3f}%")
    assert abs(cf["corridor_R"] - rs["need"]) < 1e-6 and abs(cf["floor_i"] - rs["floor"]) < 1e-3

    M = T["mc"]
    R = cb.identification_mc(reps=60, T=M["T"], h=12, seed=M["seed"] + seed, info=M["info"],
                             proxy_noise=M["proxy_noise"])
    tr = cb.peak(R["truth"]["y"])
    assert R["methods"]["naive"]["y"]["mean"][1] > 0 > tr["value"], "the naive regression should get the sign wrong"
    assert abs(cb.peak(R["methods"]["narrative"]["y"]["mean"])["value"] - tr["value"]) < 0.1
    lab.row("the truth: output's trough after a one-point shock (quarter)", f"{tr['value']:+.2f}% ({tr['h']})")
    for m in ("naive", "var", "var_news", "narrative", "hf_clean", "hf_info"):
        v = R["methods"][m]
        pk = cb.peak(v["y"]["mean"])
        lab.row(f"{m}: output after one quarter; trough; inflation after three years",
                f"{v['y']['mean'][1]:+.2f}%; {pk['value']:+.2f}% at {pk['h']}; {v['pi']['mean'][-1]:+.2f}")

    ip, cpi, ppi, ff = (_series(k, "1965-01-01", "2007-12-01") for k in ("INDPRO", "CPIAUCSL", "PPIACO", "FEDFUNDS"))
    ds = sorted(set(ip) & set(cpi) & set(ppi) & set(ff))
    X3 = np.column_stack([100 * np.log([ip[d] for d in ds]), 100 * np.log([cpi[d] for d in ds]),
                          [ff[d] for d in ds]])
    X4 = np.column_stack([X3[:, :2], 100 * np.log([ppi[d] for d in ds]), X3[:, 2]])
    for name, X, k in (("without commodity prices", X3, 2), ("with commodity prices", X4, 3)):
        fit = rbc.var_ols(X, 12)
        L = np.linalg.cholesky(fit["Sigma"])
        r = np.array([P @ L[:, k] for P in rbc._ma(fit["A"], 48)]) / L[k, k]
        lab.row(f"US VAR {name}: CPI at 24 and 48 months; industrial production's trough",
                f"{r[24, 1]:+.2f}%, {r[48, 1]:+.2f}%; {r[:, 0].min():+.2f}%")
    r_last = r

    V = data.rtdsm_q1()
    Y, P = _series("GDPC1"), _series("GDPPOT")
    errs = []
    for v in V["vintages"]:
        if not "1971Q1" <= v <= "1982Q1":
            continue
        lv = np.array(V["level"][v])
        ok = np.isfinite(lv)
        y = np.log(lv[ok])
        t = np.arange(len(y))
        b = np.polyfit(t, y, 1)
        last = [q for q, o in zip(V["quarters"], ok) if o][-1]
        yy, kq = last.split(":Q")
        key = f"{yy}-{3 * (int(kq) - 1) + 1:02d}-01"
        errs.append(100 * (y[-1] - np.polyval(b, t[-1])) - 100 * (np.log(Y[key]) - np.log(P[key])))
    lab.row("real time, 1970-81: the gap of the day minus today's, on average", f"{np.mean(errs):+.1f} points")

    y10 = _series("DGS10", "2008-01-01", "2010-12-31")
    ev = cb.event_changes(("2008-11-25", "2008-12-01", "2008-12-16", "2009-01-28", "2009-03-18", "2009-08-12",
                           "2009-09-23", "2009-11-04"), y10)
    lab.row("QE1: the 10-year yield over the eight announcement days", f"{100 * sum(e['change'] for e in ev):+.0f} bp")

    isl = cb.rstar_island(**T["rstar"])
    lab.row("the Island's r*: the filter's 90% band, and its coverage", f"+/-{1.645 * isl['steady_se']:.2f} points, "
            f"{100 * isl['coverage90']:.0f}%")
    H = data.hlw()
    k2000 = H["date"].index("2000-01-01")
    lab.row("Holston-Laubach-Williams, US r*: 2000Q1 and the latest", f"{H['rstar_us'][k2000]:.2f}%, "
            f"{H['rstar_us'][-1]:.2f}%")

    D = T["debt"]
    pr = cb.debt_params(D["debt"], D["rf"], D["r_good"], D["r_bad"])
    free = cb.debt_game(D["debt"], D["rf"], cap=None, **pr)
    capped = cb.debt_game(D["debt"], D["rf"], cap=D["cap"], **pr)
    assert len(free["equilibria"]) == 2 and len(capped["equilibria"]) == 1
    lab.row("the debt game: equilibria without and with a backstop", ", ".join(f"{100 * x:.2f}%" for x in
                                                                                free["equilibria"]) + "; " +
            ", ".join(f"{100 * x:.2f}%" for x in capped["equilibria"]))

    G = data.greenbook()
    spf = {r["quarter"]: r for r in G["spf"]}
    seen, rows = set(), []
    for g in G["gb"]:
        q = g["quarter"]
        if q in seen or q not in spf:
            continue
        seen.add(q)
        s = spf[q]
        if not (np.all(np.isfinite(g["f"][1:5])) and np.all(np.isfinite(s["f"][1:5]))):
            continue
        rows.append((q, np.mean(g["f"][1:5]), np.mean(s["f"][1:5])))
    gd = _series("GDPDEF")
    err = {"gb": [[], []], "spf": [[], []]}
    for q, fg, fs in rows:
        yq, kq = int(q[:4]), int(q[-1])
        a0 = f"{yq}-{3 * (kq - 1) + 1:02d}-01"
        a4 = f"{yq + 1}-{3 * (kq - 1) + 1:02d}-01"
        if a0 in gd and a4 in gd:
            act = 100 * (gd[a4] / gd[a0] - 1)
            e = 0 if q <= "1991Q4" else 1
            err["gb"][e].append(act - fg)
            err["spf"][e].append(act - fs)
    rm = {k: [np.sqrt(np.mean(np.square(x))) for x in v] for k, v in err.items()}
    lab.row("Greenbook against SPF, inflation a year ahead (each quarter's first Greenbook): RMSE to 1991, after",
            f"{rm['gb'][0]:.2f} vs {rm['spf'][0]:.2f}; {rm['gb'][1]:.2f} vs {rm['spf'][1]:.2f}")

    lab.note = ("A central bank sets its rate by the scarcity of reserves in a corridor, or by the rate it pays on "
                "them on a floor. Measuring what its decisions do needs the part that is its own: on the Island, naive "
                "regressions and VARs that miss the bank's news get the sign or the timing wrong, while narrative "
                "shocks and clean surprises recover the truth, and surprises that reveal news understate it. Rules "
                "need gaps and natural rates that the data of the day misjudge. A backstop removes a bad equilibrium "
                "without being used.")

    fig, ax = labs.figure(2, size=(11, 4.4))
    h = np.arange(len(R["truth"]["y"]))
    ax[0].plot(h, R["truth"]["y"], color="black", ls="--", label="truth")
    for m, c in (("var", labs.BLUE), ("narrative", labs.ORANGE), ("hf_info", "red")):
        ax[0].plot(h, R["methods"][m]["y"]["mean"], color=c, label=m)
    ax[0].axhline(0, color="grey", lw=0.8)
    ax[0].set(title="The Island: output after a policy shock", xlabel="quarters", ylabel="%")
    ax[0].legend()
    ax[1].plot(np.arange(49), r_last[:, 0], color=labs.BLUE, label="industrial production")
    ax[1].plot(np.arange(49), r_last[:, 1], color=labs.ORANGE, label="CPI")
    ax[1].axhline(0, color="grey", lw=0.8)
    ax[1].set(title="US VAR with commodity prices, 1965-2007", xlabel="months", ylabel="%")
    ax[1].legend()
    lab.fig = fig
    return lab
