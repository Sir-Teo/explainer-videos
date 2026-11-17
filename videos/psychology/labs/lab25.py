"""Lab 25: Wald's test against a fixed sample; the diffusion model's closed forms against simulation; EZ diffusion
on 17 people's speed and accuracy blocks; the stop-signal race and the stop time recovered."""

import numpy as np

from videos.coursekit import labs
from explainer.psychology import opendata
from explainer.psychology.psyche import decide as D

TITLE = "Deciding in time"
GOAL = ("Run Wald's test and count the shots it saves; check the diffusion model's formulas against simulated "
        "trials; fit 17 people's speed and accuracy blocks by EZ diffusion; and recover a stop time from a race.")
TASKS = [
    "Change Wald's error rates to alpha = beta = 0.01. How many more shots does the sequential test need on average, "
    "and how many more the fixed test?",
    "Give the simulated decision maker a start that varies from trial to trial (sw = 0.6 in D.simulate). Are its "
    "errors now faster or slower than its correct answers, and does EZ still recover the drift?",
    "Fit EZ separately to word and non-word trials in the open data. Is the drift for non-words lower, and does "
    "the bound change between them?",
]


def run(seed=0):
    out = labs.Lab()

    # 1. Wald's test
    oc0, n0 = D.sprt_oc_asn(0.5, 0.5, 0.7)
    oc1, n1 = D.sprt_oc_asn(0.7, 0.5, 0.7)
    nf = D.fixed_n(0.5, 0.7)
    sim = D.sprt_simulate(0.7, 0.5, 0.7, reps=4000, seed=seed)
    out.row("Wald's test, p = 0.5 against 0.7: average shots (Wald) under each", f"{n0:.1f}, {n1:.1f}")
    out.row("simulated under p = 0.7: accepts 0.7; average shots", f"{sim['accept_h1']:.3f}; {sim['mean_n']:.1f}")
    out.row("a fixed test with the same error rates", f"{nf} shots")
    assert max(n0, n1) < 0.6 * nf

    # 2. the diffusion model
    v, a, w = 1.2, 1.4, 0.5
    rt, up = D.simulate(v, a, w, 0.3, n=20000, seed=seed + 1, dt=0.0005)
    out.row("P(upper): formula, simulation", f"{D.p_upper(v, a, w):.3f}, {up.mean():.3f}")
    out.row("mean decision time, s: formula, simulation", f"{D.mean_dt(v, a, w):.3f}, {np.nanmean(rt) - 0.3:.3f}")
    e = D.ez(up.mean(), np.var(rt[up]), np.mean(rt[up]), s=1.0)
    out.row("EZ recovers v, a, t0 (true 1.2, 1.4, 0.3)", f"{e['v']:.2f}, {e['a']:.2f}, {e['t0']:.3f}")

    # 3. EZ on the open data
    d = opendata.speed_acc()
    ids = sorted(set(d["id"]), key=int)
    ab = np.zeros((len(ids), 2))
    vb = np.zeros((len(ids), 2))
    for k, i in enumerate(ids):
        for j, sp in enumerate((True, False)):
            m = (d["id"] == i) & (d["speed"] == sp)
            c, r = d["correct"][m], d["rt"][m]
            f = D.ez(c.mean(), np.var(r[c]), np.mean(r[c]), s=1.0)
            ab[k, j], vb[k, j] = f["a"], f["v"]
    out.row("17 people: EZ bound lower under speed", f"{int((ab[:, 0] < ab[:, 1]).sum())} of {len(ids)}; median "
            f"ratio {np.median(ab[:, 0] / ab[:, 1]):.2f}")
    out.row("EZ drift, speed against accuracy: median ratio", f"{np.median(vb[:, 0] / vb[:, 1]):.2f}")

    # 4. stopping
    rng = np.random.default_rng(seed + 2)
    go = 0.25 + rng.gamma(4.0, 0.06, 50000)
    ssds = np.array([0.1, 0.2, 0.3])
    r = D.stop_race(go, ssds, 0.22, seed=seed + 3)
    est = [D.ssrt_integration(go, s_, p) for s_, p in zip(ssds, r["p_respond"])]
    out.row("stop race, delays 0.1, 0.2, 0.3 s: P(respond)", ", ".join(f"{p:.2f}" for p in r["p_respond"]))
    out.row("stop time by the integration method (true 0.220 s)", ", ".join(f"{x:.3f}" for x in est))

    out.note = ("Wald's test needs about half the shots of a fixed test; the diffusion model's formulas match its "
                "simulation; telling people to hurry lowers their bound in all 17 by EZ (16 of 17 in the full fits); and a "
                "stop time you never observe can be read off the race.")

    fig, ax = labs.figure(2, size=(11, 4.2))
    ag = np.linspace(0.3, 2.6, 60)
    ax[0].plot(D.mean_dt(1.5, ag) + 0.3, D.p_upper(1.5, ag), color=labs.GOLD)
    ax[0].set(title="One mind, every caution", xlabel="mean response time (s)", ylabel="proportion correct")
    ax[1].scatter(ab[:, 1], ab[:, 0], color=labs.BLUE)
    lim = [0, max(ab.max(), 0.1) * 1.05]
    ax[1].plot(lim, lim, ls="--", color="#888888")
    ax[1].set(title="17 people: EZ bound", xlabel="accuracy blocks", ylabel="speed blocks")
    out.fig = fig
    return out
