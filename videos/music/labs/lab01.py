"""Lab 1: build a string from beads, measure its pitch against Mersenne's law, and its pluck against sin(n pi beta)/n."""

import numpy as np

from videos.coursekit import labs
from explainer.music.monochord import Clip, concat
from explainer.music.monochord.dsp import f0_autocorr, partials
from explainer.music.monochord.instruments import plucked
from explainer.music.monochord.physics import String, pluck_shape, simulate

TITLE = "A string from beads: its pitch and its pluck"
GOAL = ("Simulate a random string as beads obeying Newton's law, read its pitch off the motion and compare it with "
        "(1/2L) sqrt(T/mu); then compare the partials of the force on its bridge with sin(n pi beta)/n.")
TASKS = [
    "Change BETAS to (1/7,). Which partials vanish, and what does the bar chart look like at n = 7 and 14?",
    "Give the string stiffness (kappa=1.5 in String(...)). How many cents sharp is the eighth partial, and does the fundamental move?",
    "Add a struck start (Problem 4: zero shape, a velocity over 2 cm) and check that the partial levels fall as 1/n.",
]
BETAS = (1 / 2, 1 / 3, 1 / 4, 1 / 5)
SR = 48_000


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()

    # 1. a random string: its pitch from the motion alone
    L, T, mu = rng.uniform(0.4, 1.0), rng.uniform(50, 150), rng.uniform(0.001, 0.006)
    s = String(L=L, T=T, mu=mu)
    beta = BETAS[int(rng.integers(len(BETAS)))]
    out = simulate(s, lambda x: pluck_shape(x, s.L, beta, 1e-3), 0.3, sr=SR, snapshot_every=8)
    f = f0_autocorr(out.pickup, SR, 0.5 * s.f1, 2.0 * s.f1)
    cents = 1200 * np.log2(f / s.f1)
    lab.row("string", f"L = {L:.3f} m, T = {T:.1f} N, mu = {1000 * mu:.2f} g/m, {out.N - 1} beads")
    lab.row("pitch from the motion", f"{f:.2f} Hz")
    lab.row("(1/2L) sqrt(T/mu)", f"{s.f1:.2f} Hz   ({cents:+.2f} cents apart)")
    assert abs(cents) < 3.0, "the beads' pitch is Mersenne's law"

    # 2. the pluck: partials of the force on the bridge against sin(n pi beta) / n
    n = np.arange(1, 13)
    got = np.array([p["db"] for p in partials(out.force[: int(0.1 * SR)], SR, s.f1, 12)])
    want = 20 * np.log10(np.maximum(np.abs(np.sin(n * np.pi * beta)) / n, 1e-9))
    got, want = got - got.max(), want - want.max()
    strong = want > -30
    worst = float(np.abs(got - want)[strong].max())
    missing = [int(k) for k in n if abs(np.sin(k * np.pi * beta)) < 1e-9]
    lab.row("plucked at", f"1/{round(1 / beta)} of the length")
    lab.row("partials missing (theory)", ", ".join(map(str, missing)))
    lab.row("their level in the simulation", f"{max(got[k - 1] for k in missing):.0f} dB or lower")
    lab.row("other partials: worst gap", f"{worst:.2f} dB from sin(n pi beta)/n")
    assert worst < 1.5 and max(got[k - 1] for k in missing) < -40

    # 3. three plucks to listen to (Problem 3): in the middle, at a quarter, at a tenth, in a shuffled order
    order = rng.permutation(3)
    places = (1 / 2, 1 / 4, 1 / 10)
    notes = [Clip(plucked(seconds=1.6, beta=places[k])).fade(0.002, 0.1) for k in order]
    lab.audio = concat(notes, gap=0.4).at_level(-18.0)
    lab.row("ear problem, the order (listen first)", ", ".join(f"1/{round(1 / places[k])}" for k in order))

    fig, (a, b) = labs.figure(2)
    half = int(round(0.5 / s.f1 * SR / 8))
    for i, k in enumerate(np.linspace(0, half, 7).astype(int)):
        a.plot(out.x / s.L, out.snaps[k] * 1000, color=labs.GOLD, alpha=0.35 + 0.1 * i, lw=1.6)
    a.set_title("The plucked string over half a period")
    a.set_xlabel("position along the string (fraction of L)")
    a.set_ylabel("displacement (mm)")
    b.bar(n, got - (-60), bottom=-60, color=[labs.RED if k in missing else labs.BLUE for k in n], width=0.6,
          label="simulated (beads)")
    b.plot(n, np.maximum(want, -60), "o", color=labs.GOLD, ms=5, label="sin(n pi beta) / n")
    b.set_ylim(-60, 3)
    b.set_title(f"The force on the bridge, plucked at 1/{round(1 / beta)}")
    b.set_xlabel("partial")
    b.set_ylabel("level (dB below the strongest)")
    b.legend()
    lab.fig = fig
    lab.note = ("Newton's law for the beads gives Mersenne's pitch, and a pluck excites mode n in proportion to the "
                "mode's own height at the plucking point: modes with a node there are missing.")
    return lab
