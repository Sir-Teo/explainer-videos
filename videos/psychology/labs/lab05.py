"""Lab 5: one membrane, from the voltage clamp to a spike to a travelling wave, and then thrown away twice."""

import math

import numpy as np

from videos.coursekit import labs
from explainer.psychology.psyche import neuron as N

TITLE = "A membrane from clamp to spike to cable, and what is left when it is simplified"
GOAL = ("Compute the two batteries of a squid axon; clamp the model membrane and read off its two conductances; "
        "let it go and measure the spike, its threshold and its dead time; send it down the 1952 axon and compare "
        "the speed with the published one; then check the integrate-and-fire neuron against its formula.")
TASKS = [
    "Halve the sodium conductance (HH(g_na=60)), as a partial dose of a local anaesthetic would. What happens to "
    "the threshold, to the height of the spike and to the conduction speed? At what conductance does the signal "
    "fail to travel?",
    "Warm the membrane from 6.3 to 18.5 degrees (HH(temp_c=18.5)). Which features of the spike change by about a "
    "factor of three, which hardly change, and why does the model make the gates faster and nothing else?",
    "Give the integrate-and-fire neuron a current just below its least firing current and add noise "
    "(simulate(1.4, noise=1.2)). Measure the Fano factor of its spike counts in 200 ms windows, and compare it "
    "with a Poisson train of the same rate.",
]


def run(seed=0):
    out = labs.Lab()
    hh = N.HH()

    # 1. the batteries
    e_k, e_na = N.nernst(*N.SQUID["K"]), N.nernst(*N.SQUID["Na"])
    out.row("Nernst potentials at 6.3 C: potassium, sodium (mV)", f"{e_k:.1f}, {e_na:+.1f}")
    out.row("Goldman voltage, sodium 1/25 as permeable as potassium", f"{N.goldman(1, 0.04):.1f} mV")
    out.row("... sodium 20 times as permeable", f"{N.goldman(1, 20):+.1f} mV")
    assert e_k < N.goldman(1, 0.04) < 0 < N.goldman(1, 20) < e_na

    # 2. the clamp: step from rest to 0 mV and hold
    c = hh.clamp(0.0, 10.0)
    t_peak = c["t"][c["g_na"].argmax()]
    out.row("clamp at 0 mV: sodium conductance peaks at", f"{c['g_na'].max():.1f} mS/cm2 after {t_peak:.2f} ms")
    out.row("... and has fallen by 10 ms to", f"{c['g_na'][-1]:.2f} mS/cm2")
    out.row("... potassium conductance rises to", f"{c['g_k'][-1]:.1f} mS/cm2, half-way at "
            f"{c['t'][np.argmax(c['g_k'] >= c['g_k'][-1] / 2)]:.1f} ms")
    assert c["g_na"][-1] < 0.05 * c["g_na"].max() and np.all(np.diff(c["g_k"]) > -1e-12)

    # 3. let it go
    th = hh.threshold(0.5)
    r = hh.pulse(2 * th, 0.5, 20.0)
    peaks = [hh.pulse(k * th, 0.5, 12.0)["v"].max() for k in (0.9, 1.1, 3.0)]
    dead = hh.refractory([3.0, 8.0, 25.0])
    out.row("rest, and threshold for a 0.5 ms pulse", f"{hh.rest:.1f} mV, {th:.1f} uA/cm2")
    out.row("the spike: peak, undershoot (mV)", f"{r['v'].max():+.1f}, {r['v'].min():.1f}")
    out.row("peak for pushes of 0.9, 1.1 and 3 times threshold (mV)", ", ".join(f"{p:+.0f}" for p in peaks))
    out.row("push for a second spike after 3, 8, 25 ms (x threshold)",
            ", ".join("none" if math.isinf(d) else f"{d / th:.1f}" for d in dead))
    assert peaks[0] < -50 < 30 < peaks[1] and abs(peaks[2] - peaks[1]) < 8 and math.isinf(dead[0])

    # 4. down the axon of the 1952 paper
    p = N.propagate()
    thin = N.propagate(radius_cm=0.0238 / 4)
    out.row("conduction speed, computed here", f"{p['velocity']:.1f} m/s")
    out.row("... computed by Hodgkin and Huxley; measured", "18.8 m/s; 21.2 m/s")
    out.row("... in an axon a quarter as wide", f"{thin['velocity']:.1f} m/s")
    assert abs(p["velocity"] - 18.8) < 1.5 and abs(thin["velocity"] / p["velocity"] - 0.5) < 0.05

    # 5. thrown away twice
    f = N.FHN()
    lif = N.LIF()
    sim = 1000 / np.diff(lif.simulate(3.0, 2000.0)["spikes"]).mean()
    out.row("FitzHugh-Nagumo: rest stable; steady current 0.5 gives", "rest" if f.stable(0.5) else "firing")
    out.row("integrate-and-fire at twice its least current: formula, simulation",
            f"{float(lif.rate(3.0)):.1f}, {sim:.1f} per second")
    counts = N.counts(20.0, 1.0, 400, np.random.default_rng(seed + 5))
    out.row("Poisson train, 20 a second: Fano factor of counts", f"{N.fano(counts):.2f}")
    assert f.stable(0.0) and not f.stable(0.5) and abs(sim - float(lif.rate(3.0))) < 1.0
    out.note = ("Every number was computed from the published equations; none was fitted to a spike. The clamp "
                "shows sodium turning on fast and off by itself and potassium turning on late, and those three "
                "habits give a threshold, a spike of one size and a dead time. On a cable the spike travels at "
                "the speed Hodgkin and Huxley computed by hand. Two variables keep the behaviour, and one keeps "
                "the rate.")

    fig, ax = labs.figure(2, size=(11, 4.2))
    keep = r["t"] <= 12
    ax[0].plot(r["t"][keep], r["v"][keep], color=labs.BLUE, lw=2, label="membrane potential (mV)")
    twin = ax[0].twinx()
    twin.plot(r["t"][keep], r["g_na"][keep], color=labs.PINK, lw=1.5, label="sodium conductance")
    twin.plot(r["t"][keep], r["g_k"][keep], color=labs.GREEN, lw=1.5, label="potassium conductance")
    twin.set_ylabel("mS/cm2")
    ax[0].set(title="One spike, and the two conductances behind it", xlabel="time (ms)", ylabel="mV")
    lines = ax[0].get_lines() + twin.get_lines()
    ax[0].legend(lines, [ln.get_label() for ln in lines], loc="upper right", fontsize=8)
    for i in np.linspace(0, len(p["t"]) - 1, 5).astype(int)[1:]:
        ax[1].plot(p["x"], p["v"][i], color=labs.PURPLE, alpha=0.35 + 0.15 * (i / len(p["t"]) * 4))
    ax[1].set(title=f"The same spike on a cable: {p['velocity']:.1f} m/s", xlabel="distance along the axon (cm)",
              ylabel="mV")
    out.fig = fig
    return out
