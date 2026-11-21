"""Lab 68: the dissertation: New York's congestion charge from the MTA's open data, by year-on-year differences in
differences with placebo years, bus speeds and miles, discontinuities at 9 pm and 5 am, a calibrated congestion
model and the $15 counterfactual with its uncertainty, and the same study on the Island."""

import numpy as np

from videos.coursekit import labs
from explainer.economics import data
from explainer.economics.agora import congestion as C

TITLE = "The dissertation"
GOAL = ("Carry one question from data to design to model: what New York's congestion charge did, and what a higher "
        "toll would do, with every assumption in view.")
TASKS = [
    "Drop the Verrazzano and the RFK Bridge from the controls (pass controls=... to C.yoy_did). Does the placebo "
    "drift change, and the net effect?",
    "Fit the 9 pm discontinuity within one hour instead of two (C.time_rd(T, 21.0, width=1.0)). Is the jump robust?",
    "Make time worth $35 an hour and trips 5 miles in the zone (C.congestion_model(..., vot=35, miles=5)). What "
    "toll equals the marginal external cost now?",
]


def run(seed=0):
    lab = labs.Lab()
    P = C.crossings_panel(data.mta_crossings())
    D = C.yoy_did(P)
    net = D["effect"] - D["placebo_mean"]
    assert D["effect"] < 0 and D["placebo_mean"] < 0 and D["effect"] < net < 0      # the drift explains part
    lab.row("tunnels minus other crossings, year on year: 2025, placebo years, net",
            f"{100 * D['effect']:.1f}%, {100 * D['placebo_mean']:.1f}%, {100 * net:.1f}%")
    Bu = C.bus_speeds(data.cbd_bus())
    V = C.vmt(data.cbd_vmt())
    assert Bu["effect"] > Bu["placebo"] and V["crz_change"] < 0
    lab.row("bus speeds in the district against outside (2025, placebo 2024); miles in the zone",
            f"{100 * Bu['effect']:+.1f}% ({100 * Bu['placebo']:+.1f}%); {100 * V['crz_change']:+.1f}%")
    T = data.crz_tod()
    n9, n5 = C.time_rd(T, 21.0), C.time_rd(T, 5.0)
    assert n9["jump"] > 0 > n5["jump"]                                           # retiming around the cutoffs
    lab.row("car entries at the cutoffs: 9 pm and 5 am jumps", f"{100 * (np.exp(n9['jump']) - 1):+.0f}% and "
            f"{100 * (np.exp(n5['jump']) - 1):+.0f}%")
    bc = [r["cbd"] for r in Bu["rows"] if r["year"] == 2025]
    M = C.congestion_model(V["crz_change"], -float(np.mean(bc)), 9.0, 20.0)
    opt = C.optimal_toll(M)
    assert M["eta"] < 0 and abs(opt["toll"] - opt["mec"]) < 0.01
    lab.row("the model: time elasticity, demand elasticity, a car's delay cost, the toll equal to it",
            f"{M['e_tv']:.2f}, {M['eta']:.2f}, ${M['mec_old']:.2f}, ${opt['toll']:.2f}")
    I0, It = C.island_study(sims=150), C.island_study(pretrend=-0.015, sims=150)
    assert abs(I0["mean"] - I0["truth"]) < 0.005 and abs(It["adjusted"] - It["truth"]) < 0.005 < abs(It["bias"])
    lab.row("the Island: parallel trends, a drift, the drift net of the placebo (truth -4%)",
            f"{100 * I0['mean']:.1f}%, {100 * It['mean']:.1f}%, {100 * It['adjusted']:.1f}%")

    lab.note = ("A design measures against its counterfactual; the placebo years show when that counterfactual is "
                "wrong, and a model is needed for any toll that was never charged.")

    fig, ax = labs.figure(2, size=(11, 4.4))
    rows = [r for r in D["rows"] if r["year"] >= 2023]
    ax[0].bar(range(len(rows)), [100 * r["did"] for r in rows],
              color=["0.6" if r["year"] < 2025 else ("tab:red" if r["year"] == 2025 else labs.ORANGE) for r in rows])
    ax[0].axhline(100 * D["placebo_mean"], color="k", ls="--", lw=1)
    ax[0].set(title="tunnels minus other crossings", xlabel="month (2023-2026)", ylabel="year-on-year change, %")
    t, y = np.array(n9["t"]), np.array(n9["y"])
    m = (t >= 19) & (t <= 23)
    ax[1].scatter(t[m], y[m], s=12, color="0.4")
    ax[1].axvline(21, color="tab:red", lw=1)
    ax[1].set(title="car entries around 9 pm", xlabel="hour", ylabel="per ten minutes, average weekday")
    lab.fig = fig
    return lab
