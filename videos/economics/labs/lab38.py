"""Lab 38: work and wages: Card and Krueger's difference in differences recomputed from their restaurants, labour
supply with income effects and Slutsky's equation, a competitive wage floor, monopsony with a minimum wage, the border
design run on the Island under both theories, Mincer's equation on the 1976 CPS, Card's college-distance instrument,
ability bias with IQ, and Roy's model with Heckman's correction."""

import numpy as np

from videos.coursekit import labs
from explainer.economics import data
from explainer.economics.agora import labour
from explainer.economics.island import truths

TITLE = "Work and wages"
GOAL = ("Recompute New Jersey's difference in differences; split a wage change into substitution and income effects; "
        "compare a wage floor in a competitive market and at a monopsonist; run the border design where the truth is "
        "known; estimate the return to schooling three ways; and recover a selected occupation's wages.")
TASKS = [
    "Card and Krueger: drop the six stores that closed instead of counting them at zero. How much does the "
    "difference in differences move?",
    "Monopsony: raise the supply elasticity facing the firm from 3 to 10. What happens to the markdown, and to the "
    "range of minimum wages that add jobs?",
    "Roy: set the correlation between the two occupations' wages to -0.5. Does Heckman's correction still recover "
    "the average fishing wage?",
]


def _col(D, k):
    return np.array([np.nan if v in ("", None) else float(v) for v in D[k]])


def run(seed=0):
    lab = labs.Lab()
    T = truths(38)

    D = data.njmin()
    st = _col(D, "state")
    f1 = _col(D, "empft") + _col(D, "nmgrs") + 0.5 * _col(D, "emppt")
    f2 = _col(D, "empft2") + _col(D, "nmgrs2") + 0.5 * _col(D, "emppt2")
    f2 = np.where(_col(D, "status2") == 3, 0.0, f2)
    m = {s: (np.nanmean(f1[st == s]), np.nanmean(f2[st == s])) for s in (0, 1)}
    did = (m[1][1] - m[1][0]) - (m[0][1] - m[0][0])
    lab.row("full-time-equivalent employees: New Jersey and Pennsylvania, before and after",
            f"NJ {m[1][0]:.2f} to {m[1][1]:.2f}; PA {m[0][0]:.2f} to {m[0][1]:.2f}")
    lab.row("the difference in differences", f"{did:+.2f} employees per restaurant")
    assert 2.0 < did < 3.5

    S = T["supply"]
    kw = {k: S[k] for k in ("y", "gamma", "phi", "psi")}
    for w in (6.0, 30.0):
        e = labour.supply_elasticities(w, **kw)
        lab.row(f"labour supply at ${w:.0f}: Marshallian, income effect, Hicksian, Frisch",
                f"{e['marshallian']:+.2f}, {e['income_effect']:+.2f}, {e['hicksian']:+.2f}, {e['frisch']:.2f}")
        assert abs(e["hicksian"] - (e["marshallian"] - e["income_effect"])) < 1e-9

    M = T["market"]
    eq = labour.competitive(**M)
    L19 = float(labour.floor_competitive(1.188 * eq["w"], **M))
    lab.row("competitive market: wage and employment; a floor 18.8% above", f"${eq['w']:.2f}, {eq['L']:.1f}; "
                                                                          f"employment {100 * (L19 / eq['L'] - 1):+.1f}%")

    P = T["monopsony"]
    R = labour.monopsony(**P)
    grid = np.linspace(R["w_m"], R["w_c"] * 1.2, 200)
    emp = labour.floor_monopsony(grid, **P)
    best = grid[int(np.argmax(emp))]
    lab.row("monopsony: wage and hiring, and the competitive ones", f"${R['w_m']:.2f}, {R['L_m']:.0f}; "
                                                                     f"${R['w_c']:.2f}, {R['L_c']:.0f}")
    lab.row("the minimum wage that maximizes hiring", f"${best:.2f}")
    assert abs(best - R["w_c"]) < 0.05

    B = T["border"]
    bk = {k: B[k] for k in ("n_treat", "n_ctrl", "m0", "m1", "eps_d", "eta", "trend", "noise")}
    runs = {reg: np.array([labour.border_experiment(reg, seed=seed + s, **bk)["did_emp"] for s in range(40)])
            for reg in ("competitive", "monopsony")}
    lab.row("the border design on the Island, 40 runs: mean effect, competitive and monopsony",
            f"{runs['competitive'].mean():+.3f}, {runs['monopsony'].mean():+.3f}")
    assert runs["competitive"].mean() < 0 < runs["monopsony"].mean()

    W = data.wooldridge("wage1")
    y, s, x = _col(W, "lwage"), _col(W, "educ"), _col(W, "exper")
    r = labour.ols(y, np.column_stack([np.ones_like(s), s, x, x ** 2]))
    lab.row("Mincer on the 1976 CPS: return a year (s.e.); experience peaks at",
            f"{r['b'][1]:.4f} ({r['se'][1]:.4f}); {-r['b'][2] / (2 * r['b'][3]):.1f} years")

    C = data.wooldridge("card")
    yc, sc = _col(C, "lwage"), _col(C, "educ")
    ctrl = [_col(C, k) for k in ("exper", "expersq", "black", "smsa", "south", "smsa66", "reg662", "reg663",
                                 "reg664", "reg665", "reg666", "reg667", "reg668", "reg669")]
    one = np.ones_like(sc)
    X = np.column_stack([one, sc, *ctrl])
    Z = np.column_stack([one, _col(C, "nearc4"), *ctrl])
    o, iv = labour.ols(yc, X), labour.tsls(yc, X, Z)
    lab.row("Card (1995): least squares; college distance as the instrument (s.e., first-stage F)",
            f"{o['b'][1]:.4f}; {iv['b'][1]:.4f} ({iv['se'][1]:.4f}, F {iv['first_stage_F']:.1f})")
    assert abs(iv["b"][1] - 0.1315) < 0.002

    W2 = data.wooldridge("wage2")
    y2, s2, iq = _col(W2, "lwage"), _col(W2, "educ"), _col(W2, "IQ")
    c2 = [np.ones_like(s2), s2, _col(W2, "exper"), _col(W2, "tenure")]
    a, b = labour.ols(y2, np.column_stack(c2)), labour.ols(y2, np.column_stack([*c2, iq]))
    lab.row("ability bias: the return without and with IQ", f"{a['b'][1]:.4f}, {b['b'][1]:.4f}")

    Ro = T["roy"]
    rr = labour.roy(**{**Ro, "seed": Ro["seed"] + seed})
    w1, z, sec = np.array(rr["w1"]), np.array(rr["z"]), np.array(rr["second"])
    one = np.ones_like(w1)
    H = labour.heckman_two_step(w1, one[:, None], ~sec, np.column_stack([one, z]))
    lab.row("Roy: fishers' observed mean log wage, Heckman's estimate, everyone's",
            f"{H['naive'][0]:.3f}, {H['corrected'][0]:.3f}, {w1.mean():.3f}")
    assert abs(H["corrected"][0] - w1.mean()) < abs(H["naive"][0] - w1.mean())

    lab.note = ("A difference in differences assumes the two states would have moved together. Income effects can bend "
                "labour supply back, so the compensated elasticity, not the raw one, measures the incentive. A floor "
                "costs jobs in a competitive market but can add them where employers set wages. Natural experiments "
                "put the return to a year of school near or above least squares. Selection hides what people would "
                "earn in the work they did not choose, and a shifter of the choice can recover it.")

    fig, ax = labs.figure(2, size=(11, 4.4))
    ws = np.linspace(1, 50, 100)
    ax[0].plot([labour.hours(w, **kw) for w in ws], ws, color=labs.BLUE)
    ax[0].set(title="labour supply with income effects", xlabel="hours (share of time)", ylabel="wage, $")
    ax[1].plot(grid, emp, color=labs.ORANGE)
    ax[1].axvline(R["w_m"], color="grey", lw=0.8)
    ax[1].axvline(R["w_c"], color="grey", lw=0.8, ls="--")
    ax[1].set(title="monopsony: hiring against the minimum wage", xlabel="minimum wage, $", ylabel="workers")
    lab.fig = fig
    return lab
