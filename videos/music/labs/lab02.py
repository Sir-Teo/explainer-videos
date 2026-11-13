"""Lab 2: the speed of sound from the gas law alone, a bottle against Helmholtz's formula, and three horns for the ear."""

import math

import numpy as np

from videos.coursekit import labs
from explainer.music.monochord import Clip, concat
from explainer.music.monochord.partkit import resample
from explainer.music.monochord.physics import air

TITLE = "Air: its speed from the gas law, and a bottle's note"
GOAL = ("Let a row of gas parcels carry a pulse and read the speed of sound off their motion; then simulate a bottle "
        "as a neck on a body and compare its note with Helmholtz's formula and with the exact two-tube root.")
TASKS = [
    "Change LAW to 'isothermal'. What speed do the parcels give now, and what fraction of Laplace's is it?",
    "Halve the bottle's neck length. Predict the new note from Helmholtz's formula before you run it.",
    "Make the body very short and wide (same volume). Does Helmholtz's formula get better or worse, and why?",
]
LAW = "adiabatic"
SR = 48_000


def run(seed=0):
    rng = np.random.default_rng(seed)
    lab = labs.Lab()

    # 1. the speed of sound: no wave speed is written into the chain of parcels
    celsius = float(rng.uniform(-5, 35))
    run_ = air.gas_chain(6.0, 3001, lambda t: 0.01 * math.exp(-((t - 0.4e-3) / 0.12e-3) ** 2), 0.017, law=LAW,
                         celsius=celsius, probes=(500, 2000), snapshot_every=600)
    times = []
    for v in run_.velocity:
        i = int(np.argmax(v))
        a, b, c = v[i - 1], v[i], v[i + 1]
        times.append((i + 0.5 * (a - c) / (a - 2 * b + c)) * run_.dt)
    got = 1500 * run_.h / (times[1] - times[0])
    want = air.speed(celsius, LAW)
    lab.row("air at", f"{celsius:.1f} C, parcels obeying the {LAW} gas law")
    lab.row("speed of the pulse in the simulation", f"{got:.1f} m/s")
    lab.row("sqrt(gamma P / rho)" if LAW == "adiabatic" else "sqrt(P / rho)", f"{want:.1f} m/s")
    assert abs(got / want - 1) < 3e-3, "the gas law sets the speed of sound"

    # 2. a bottle: Helmholtz's formula, the exact two-tube root, and a simulation
    rn, ln = rng.uniform(0.007, 0.012), rng.uniform(0.04, 0.09)
    rb, vol = rng.uniform(0.028, 0.04), rng.uniform(250e-6, 700e-6)
    a_n, a_b = math.pi * rn ** 2, math.pi * rb ** 2
    lb = vol / a_b
    lumped, exact = air.helmholtz(a_n, ln, vol), air.bottle_exact(a_n, ln, a_b, lb)
    cells = range(max(8, int(ln / 0.0016)), int(ln / 0.00095))          # a cell of 1 to 1.6 mm: stable at 384 kHz
    k = min(cells, key=lambda j: abs(lb / (ln / j) - round(lb / (ln / j))))
    h = ln / k
    nb = int(round(lb / h))
    sim = air.tube(lambda x: a_b if x < nb * h else a_n, (nb + k) * h, 0.5, air.ricker(300.0), where=0.3 * lb,
                   left="closed", right="open", probe=0.2 * lb, n=nb + k, sr=384_000, radiation=0.006, q_loss=4.0)
    f_sim = float(air.resonances(sim.pressure, sim.sr, 1, 40, 900)[0])
    lab.row("bottle", f"{vol * 1e6:.0f} ml, neck {2000 * rn:.0f} mm wide and {100 * ln:.1f} cm long (no end corrections)")
    lab.row("Helmholtz's formula", f"{lumped:.1f} Hz")
    lab.row("two tubes, exact", f"{exact:.1f} Hz")
    lab.row("simulated", f"{f_sim:.1f} Hz   ({1200 * math.log2(f_sim / exact):+.1f} cents from exact)")
    assert abs(1200 * math.log2(f_sim / exact)) < 8 and lumped > exact

    # 3. three horns passing, in a shuffled order (Problem 3)
    speeds = np.array([10.0, 20.0, 35.0])
    order = rng.permutation(3)
    passes = [Clip(air.passing_source(392.0, speeds[j], 6.0, 5.0, harmonics=(1.0, 0.5, 0.33, 0.2))[0]).fade(0.3, 0.3)
              for j in order]
    lab.audio = concat(passes, gap=0.5).at_level(-18.0)
    lab.row("ear problem, the order (listen first)", ", ".join(f"{speeds[j]:.0f} m/s" for j in order))
    up, down = air.doppler(392.0, 35.0)
    lab.row("the fastest falls by", f"{1200 * math.log2(up / down):.0f} cents")

    fig, (a, b) = labs.figure(2)
    x = np.arange(run_.snaps.shape[1]) * run_.h
    for i, row in enumerate(run_.snaps[1:8]):
        a.plot(x, row * 1e6 + 6 * i, color=labs.GOLD, lw=1.4)
    a.set_title("A pulse in a row of gas parcels")
    a.set_xlabel("position (m)")
    a.set_ylabel("displacement (micrometres; later rows higher)")
    fills = np.linspace(0, 0.8, 17)
    b.plot(100 * fills, [air.bottle_exact(a_n, ln, a_b, lb * (1 - f)) for f in fills], color=labs.BLUE, label="two tubes, exact")
    b.plot(100 * fills, [air.helmholtz(a_n, ln, vol * (1 - f)) for f in fills], "--", color=labs.GOLD, label="Helmholtz")
    b.plot([0], [f_sim], "o", color=labs.RED, label="simulated (empty)")
    b.set_title("The bottle's note as it fills")
    b.set_xlabel("how full the body is (%)")
    b.set_ylabel("note (Hz)")
    b.legend()
    lab.fig = fig
    lab.note = ("Parcels that know only the gas law carry a pulse at sqrt(gamma P / rho). A bottle is a mass of air "
                "on a spring of air; Helmholtz's formula runs a little sharp because the body is not a point.")
    return lab
