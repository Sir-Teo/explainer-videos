"""Lab 6: a synapse that releases by chance, a cell that learns a principal component, and three small circuits."""

import numpy as np

from videos.coursekit import labs
from explainer.psychology.psyche import circuits as C

TITLE = "A synapse, a learning rule and three circuits built on mutual inhibition"
GOAL = ("Simulate a synapse that releases packets by chance and recover n p q from its responses; add inputs on a "
        "membrane in time and divide them with a shunt; run Hebb's rule until it diverges and Oja's until it "
        "settles on the first principal component; then show an edge to a row of units with lateral inhibition, "
        "let two rivals choose and hold a choice, and make two half-centres keep time.")
TASKS = [
    "Raise the release probability of the model synapse from 0.3 to 0.6 and, separately, double the size of a "
    "packet. Both double the mean response. Which one changes the share of failures, which changes the ratio of "
    "variance to mean, and how would a recording tell the two kinds of learning apart?",
    "Train the Oja cell on inputs whose two principal components carry nearly equal variance (change the mixing "
    "matrix to [[2, 0], [0, 1.9]]). How long does it take to settle, and why does the answer depend on the gap "
    "between the two eigenvalues?",
    "Give the half-centre oscillator inhibition of 0.9, 2.5 and 4.0 (HalfCentre(a=...)). Which of the three keeps "
    "time, what do the other two do, and how does that match the condition 1 + tau/T < a < 1 + beta?",
]


def run(seed=0):
    out = labs.Lab()
    g = np.random.default_rng(seed + 60)

    # 1. packets
    n, p, q = 5, 0.3, 0.4
    k = g.binomial(n, p, 4000)
    resp = k * q
    out.row("model synapse: mean response, n p q", f"{resp.mean():.3f}, {n * p * q:.3f} mV")
    out.row("... variance, n p (1 - p) q^2", f"{resp.var():.3f}, {n * p * (1 - p) * q * q:.3f} mV^2")
    out.row("... share of failures, (1 - p)^n", f"{(k == 0).mean():.3f}, {(1 - p) ** n:.3f}")
    assert abs(resp.mean() - n * p * q) < 0.03 and abs((k == 0).mean() - (1 - p) ** n) < 0.03

    # 2. adding up
    m = C.Membrane()
    one = m.response(exc=[5.0])["peak"]
    close, apart = m.response(exc=[5.0, 8.0])["peak"], m.response(exc=[5.0, 35.0])["peak"]
    alone = m.steady_voltage(0.05) - m.e_l
    shunt = m.steady_voltage(0.05, 0.15, e_i=m.e_l) - m.e_l
    out.row("one EPSP; two 3 ms apart; two 30 ms apart (mV)", f"{one:.2f}; {close:.2f}; {apart:.2f}")
    out.row("steady response to g_E = 0.05: alone, with a shunt", f"{alone:.1f}, {shunt:.1f} mV")
    out.row("the shunt by itself moves the voltage by", f"{m.steady_voltage(0.0, 0.15, e_i=m.e_l) - m.e_l:.1f} mV")
    assert one < apart < close < 2 * one and abs(shunt / alone - 0.5) < 0.01

    # 3. Hebb and Oja
    x = g.standard_normal((4000, 2)) @ np.array([[2.0, 0.0], [1.2, 0.5]])
    h = C.hebb(x, eta=0.01, rule="hebb", rng=np.random.default_rng(seed + 61))
    o = C.hebb(x, eta=0.01, rule="oja", rng=np.random.default_rng(seed + 61))
    vals = np.linalg.eigvalsh(x.T @ x / len(x))
    out.row("Hebb's rule: length of the weights after 100, 200 steps", f"{h['norm'][100]:.1f}, {h['norm'][200]:.0f}")
    out.row("Oja's rule: final length; cosine with the first PC", f"{np.linalg.norm(o['w']):.2f}; "
            f"{abs(o['cosine'][-1]):.3f}")
    out.row("share of the inputs' variance on the first PC", f"{vals[-1] / vals.sum():.2f}")
    assert h["norm"][200] > 20 * h["norm"][50] and abs(np.linalg.norm(o["w"]) - 1) < 0.05 and abs(o["cosine"][-1]) > 0.99

    # 4. an edge
    step = np.r_[np.full(40, 1.0), np.full(40, 2.0)]
    r = C.lateral(step)
    low, high = r[15:25].mean(), r[55:65].mean()
    out.row("lateral inhibition: plateaus either side of an edge", f"{low:.2f}, {high:.2f}")
    out.row("... dark band, bright band", f"{r[34:40].min():.2f}, {r[40:46].max():.2f}")
    out.row("... ratio across the edge, in the light and in the responses", f"2.0, {r[40:46].max() / r[34:40].min():.1f}")
    assert abs(high / low - 2) < 0.01 and r[34:40].min() < low and r[40:46].max() > high

    # 5. a choice, held
    w = C.WTA()

    def then_equal(t):
        return (1.2, 1.0) if t < 150 else (1.1, 1.1)

    held = w.simulate(then_equal)
    loose = C.WTA(w_self=0.0, w_cross=0.5).simulate(then_equal)
    out.row("two rivals, inputs 1.2 and 1.0 then equal: final activities", f"{held['r'][-1, 0]:.2f}, {held['r'][-1, 1]:.2f}")
    out.row("... without self-excitation", f"{loose['r'][-1, 0]:.2f}, {loose['r'][-1, 1]:.2f}")
    assert held["margin"] > 0.9 and loose["margin"] < 0.05

    # 6. a rhythm
    hc = C.HalfCentre()
    s = hc.simulate()
    quiet = C.HalfCentre(a=0.8).simulate()
    out.row("half-centres: period; correlation of the two outputs", f"{s['period']:.0f} ms; {s['correlation']:.2f}")
    out.row("... with inhibition of 0.8: spread of each output late in the run",
            f"{np.ptp(quiet['y'][len(quiet['y']) // 2:, 0]):.3f}")
    assert hc.oscillates and s["correlation"] < -0.5 and np.ptp(quiet["y"][len(quiet["y"]) // 2:, 0]) < 0.01
    out.note = ("A synapse's failures depend on how many sites it has and how readily they release, and not on the "
                "size of a packet, which is how recordings locate a change. Inputs add when they arrive within "
                "about a time constant, and a shunt halves them without moving the voltage by itself. Hebb's rule "
                "finds the right direction and never stops growing; Oja's stops at length one on the first "
                "principal component. Mutual inhibition among neighbours exaggerates an edge; with "
                "self-excitation it holds a choice after the evidence has gone; with fatigue it alternates.")

    fig, ax = labs.figure(2, size=(11, 4.2))
    xs = np.arange(len(step))
    ax[0].plot(xs[8:72], step[8:72], color=labs.BLUE, lw=1.5, ls="--", label="the light")
    ax[0].plot(xs[8:72], r[8:72], color=labs.GREEN, lw=2, label="the units' responses")
    ax[0].set(title="An edge of light, and what a row of units makes of it", xlabel="position along the row",
              ylabel="light, response")
    ax[0].legend(loc="upper left", fontsize=8)
    ax[1].plot(s["t"] / 1000, s["y"][:, 0], color=labs.PINK, lw=1.8, label="one half-centre")
    ax[1].plot(s["t"] / 1000, s["y"][:, 1], color=labs.PURPLE, lw=1.8, label="the other")
    ax[1].set(title=f"Two half-centres, a steady drive: period {s['period']:.0f} ms", xlabel="time (s)",
              ylabel="output")
    ax[1].legend(loc="upper right", fontsize=8)
    out.fig = fig
    return out
