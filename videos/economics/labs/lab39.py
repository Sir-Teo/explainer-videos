"""Lab 39: the wage structure: Bertrand and Mullainathan's resumes recomputed, the college premium and the race
between education and technology on BLS data, Autor and Dorn's polarization, the task model with automation, robots
across the Island's commuting zones, the two-way fixed-effects model with limited-mobility bias, the union premium
within workers, Becker's and Phelps's models of discrimination, an Oaxaca-Blinder decomposition and the child
penalty."""

import numpy as np

from videos.coursekit import labs
from explainer.economics import data
from explainer.economics.agora import labour
from explainer.economics.island import truths

TITLE = "The wage structure"
GOAL = ("Recompute the call-back gap from the resumes; back out the growth of demand for skill from the premium and "
        "supply; see polarization in Autor and Dorn's data and in a task model; separate robots from other shocks; "
        "decompose wage variance into workers, firms and sorting; measure the union premium within men; and solve "
        "two models of discrimination.")
TASKS = [
    "The resumes: compute the call-back gap separately for higher- and lower-quality resumes. In which is the gap in "
    "percentage points larger, and why does that matter for Arrow's argument?",
    "The race: redo the demand index with sigma = 2.5. Does the slowdown after 2010 survive?",
    "AKM: cut the share of workers who move each year to 1%. How far off are the firm effects' variance and the "
    "correlation of worker and firm effects?",
]


def _annual(key, min_obs=1):
    d = data.fred(key)
    out = {}
    for x, v in zip(d["date"], d["value"]):
        if v == v:
            out.setdefault(int(x[:4]), []).append(v)
    return {y: float(np.mean(v)) for y, v in out.items() if len(v) >= min_obs}


def run(seed=0):
    lab = labs.Lab()
    T = truths(39)

    R = data.resume()
    cb, race = np.array(R["received_callback"]), np.array(R["race"])
    rw, rb = cb[race == "white"].mean(), cb[race == "black"].mean()
    lab.row("call-backs: White names, African-American names, ratio", f"{100 * rw:.2f}%, {100 * rb:.2f}%, "
                                                                       f"{rw / rb:.2f}")
    assert abs(rw / rb - 1.5) < 0.01

    c, h = _annual("LEU0252918500A"), _annual("LEU0252917300A")
    nc, nh = _annual("LNU02027662", 11), _annual("LNU02027660", 11)
    ys = [y for y in range(1992, 2026) if y in nc and y in nh]
    w = np.array([np.log(c[y] / h[y]) for y in ys])
    n = np.array([np.log(nc[y] / nh[y]) for y in ys])
    km = labour.katz_murphy(w, n, ys)
    D = labour.implied_demand(w, n, 1.41)
    lab.row("college premium 1979, 1992, 2025", f"{c[1979] / h[1979]:.2f}, {c[1992] / h[1992]:.2f}, "
                                                f"{c[2025] / h[2025]:.2f}")
    lab.row("naive Katz-Murphy on 1992-2025: corr(trend, supply), implied sigma",
            f"{km['corr_trend_supply']:.3f}, {km['sigma']:.1f}")
    lab.row("demand growth with sigma 1.41: 1992-2000, 2010-2025 (% a year)",
            f"{100 * (D[ys.index(2000)] - D[0]) / 8:.1f}, {100 * (D[-1] - D[ys.index(2010)]) / 15:.1f}")

    A = data.autor_dorn("pctile")
    d = np.array(A["emp2005"]) - np.array(A["emp1980"])
    lab.row("employment share change 1980-2005: bottom fifth, 20th-50th, top fifth (points per percentile)",
            f"{d[:20].mean():+.3f}, {d[20:50].mean():+.3f}, {d[80:].mean():+.3f}")

    Tk = T["tasks"]
    kw = {k: Tk[k] for k in ("L", "M", "H", "beta")}
    b, a = labour.task_model(**kw), labour.task_model(**kw, auto=Tk["auto"])
    lab.row("task model: middle/low and high/middle wages, before and after automation",
            f"{b['wM_wL']:.3f} -> {a['wM_wL']:.3f}; {b['wH_wM']:.3f} -> {a['wH_wM']:.3f}")

    Rz = labour.robot_zones(**{**T["robots"], "seed": T["robots"]["seed"] + seed})
    lab.row("robots: naive slope, with the manufacturing share held fixed, planted",
            f"{Rz['naive']:.2f}, {Rz['ctrl']:.2f} ({Rz['ctrl_se']:.2f}), {Rz['beta']:.2f}")

    F = {**T["firms"], "n_workers": 10000, "n_firms": 250, "seed": T["firms"]["seed"] + seed}
    E = labour.worker_firm_economy(**F)
    Ak = labour.akm(E["y"], E["firm"])
    lab.row("AKM: firm-effect variance and worker-firm correlation, estimate (truth)",
            f"{Ak['var_psi']:.4f} ({E['truth']['var_psi']:.4f}); {Ak['corr']:.3f} ({E['truth']['corr']:.3f})")

    W = data.wooldridge("wagepan")
    y, u, yr = np.array(W["lwage"]), np.array(W["union"]), np.array(W["year"])
    yd = [(yr == t).astype(float) for t in range(1981, 1988)]
    X = np.column_stack([u, np.array(W["expersq"]), np.array(W["married"]), *yd])
    fe = labour.within(y, X, np.array(W["nr"]))
    pooled = labour.ols(y, np.column_stack([np.ones_like(y), u, np.array(W["exper"]), np.array(W["expersq"]),
                                            np.array(W["married"]), np.array(W["educ"]), np.array(W["black"]),
                                            np.array(W["hisp"]), *yd]))
    lab.row("union premium: pooled least squares, within men (s.e.)", f"{pooled['b'][1]:.3f}, {fe['b'][0]:.3f} "
                                                                      f"({fe['se'][0]:.3f})")
    assert fe["b"][0] < pooled["b"][1]

    Bk = labour.becker(T["becker"]["share_minority"], 0.05, d_scale=T["becker"]["d_scale"])
    lab.row("Becker: market gap with 5% unprejudiced employers, and with 20%",
            f"{100 * Bk['gap']:.1f}%, {100 * labour.becker(T['becker']['share_minority'], 0.2)['gap']:.1f}%")

    C = data.wooldridge("cps78_85")
    m = (np.array(C["year"]) == 85)
    f = np.array(C["female"]) == 1

    def Xm(mm):
        return np.column_stack([np.ones(mm.sum()), *(np.array(C[k])[mm] for k in ("educ", "exper", "expersq",
                                                                                   "union", "nonwhite"))])
    O = labour.oaxaca(np.array(C["lwage"])[m & ~f], Xm(m & ~f), np.array(C["lwage"])[m & f], Xm(m & f))
    lab.row("Oaxaca-Blinder, 1985: gap, explained, unexplained", f"{O['gap']:.3f}, {O['explained']:.3f}, "
                                                                 f"{O['unexplained']:.3f}")

    cp = labour.child_penalty(**{**T["child"], "n": 1500, "seed": T["child"]["seed"] + seed})
    lab.row("the child penalty: estimated long run, planted",
            f"{cp['long_run']:.3f}, {np.mean(cp['planted'][-5:]):.3f}")

    lab.note = ("Randomized names measure discrimination directly; decompositions only describe. The college premium "
                "is a race: supply pulls it down by its growth over sigma, demand pushes it up, and recent national "
                "data cannot separate demand's trend from supply. Automation of middle tasks hollows out the middle. "
                "Where you work matters, but few movers make firms look more different and sorting weaker than they "
                "are. Comparing the same men in and out of unions halves the union premium.")

    fig, ax = labs.figure(2, size=(11, 4.4))
    ax[0].plot(A["pctile"], d, color=labs.BLUE, lw=0.8)
    ax[0].axhline(0, color="grey", lw=0.8)
    ax[0].set(title="employment share change, 1980-2005", xlabel="1980 occupational wage percentile")
    sw = []
    for mv in (0.005, 0.01, 0.02, 0.05, 0.1):
        Ei = labour.worker_firm_economy(**{**F, "n_workers": 4000, "n_firms": 120, "move": mv})
        sw.append((mv, labour.akm(Ei["y"], Ei["firm"])["var_psi"], Ei["truth"]["var_psi"]))
    ax[1].plot([100 * s[0] for s in sw], [s[1] for s in sw], "o-", color=labs.ORANGE, label="AKM")
    ax[1].plot([100 * s[0] for s in sw], [s[2] for s in sw], color="grey", label="truth")
    ax[1].set(xscale="log", title="variance of firm effects", xlabel="% of workers moving each year")
    ax[1].legend()
    lab.fig = fig
    return lab
